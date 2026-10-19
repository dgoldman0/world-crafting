"""A world's heights above its geoid through the data manifest: the Moon's LOLA heights over GRAIL's geoid, against
the shape its gravity field gives, published landing heights and Terluna's levels, and the tide the world states."""
import csv
import json
import math

import numpy as np
import pytest

from geography import atlas, basins as bs, topography as tp
from worldlab import geography
from worldlab.data import DataError, Manifest
from worldlab.roots import root
from worldlab.spec import Library, SpecError

LIB = Library()
MOON = LIB.world('moon')
STORE, TERLUNA = root('store'), root('terluna')
# Five near-side maria's centres in the IAU gazetteer (MOON_nomenclature_center_pts.zip, sha256 404a951d51482159, as
# Terluna retrieved it on 2026-09-25), as latitude and east longitude.
MARIA = {'Oceanus Procellarum': (20.6714, -56.6774), 'Mare Imbrium': (34.7244, -14.9086),
         'Mare Serenitatis': (27.2879, 18.3596), 'Mare Crisium': (16.1774, 59.1037), 'Mare Nectaris': (-15.1852, 34.6021)}


def _stored() -> bool:
    try:
        return STORE is not None and bool(Manifest().paths(MOON['surface']['geometry'], store=STORE))
    except DataError:
        return False


needs_heights = pytest.mark.skipif(not _stored(), reason="the store lacks the Moon's heights (lab/worldlab/data.py)")
needs_terluna = pytest.mark.skipif(TERLUNA is None, reason="Terluna's repository is unset (lab/local.example.toml)")


@pytest.fixture(scope='module')
def moon():
    return geography.heights(MOON, LIB, store=STORE)


def _with(**tables):
    return {**MOON, **{name: {**MOON[name], **fields} for name, fields in tables.items()}}


@needs_heights
def test_the_files_are_found_by_what_their_labels_describe():
    files = geography.surface_files(MOON, store=STORE)
    assert {kind: (label.name, data.name) for kind, (label, data) in files.items()} == {
        'heights': ('ldem_16.lbl', 'ldem_16.img'), 'gravity': ('jggrx_0420a_sha.lbl', 'jggrx_0420a_sha.tab')}


@needs_heights
def test_the_moons_geoid_holds_its_flattening_and_its_topography_its_deepest_basin(moon):
    area, lat = moon.grid.cell_area_m2, moon.grid.lat_deg
    assert abs((moon.geoid_m * area).sum() / area.sum()) < 0.5
    # The Moon's flattening (J2) dominates: high equator, low poles.
    assert moon.geoid_m[np.abs(lat) < 1].mean() > 150.0 and moon.geoid_m[np.abs(lat) > 89].mean() < -250.0
    i, j = np.unravel_index(np.argmin(moon.height_m), moon.height_m.shape)
    assert lat[i] < -60.0 and 170.0 < moon.grid.lon_deg[j] < 200.0              # South Pole-Aitken's floor
    assert -9000.0 < moon.height_m.min() < -7500.0 and 9000.0 < moon.height_m.max() < 11000.0
    assert moon.record['geoid_degree'] == 330 and moon.record['frame'] == 'MEAN EARTH/POLAR AXIS OF DE421'
    assert moon.grid.radius_m == MOON['body']['radius_m'] and moon.grid.pixels_per_degree == 16


@needs_heights
def test_landing_heights_match_published_values(moon):
    # Chang'e 4 and Chang'e 3 landing sites, published at -5,935 m and -2,640 m on the 1737.4 km sphere.
    i, j = atlas.cell_index(moon.grid, np.array([-45.444, 44.121]), np.array([177.599, -19.512]))
    sphere = (moon.height_m + moon.geoid_m)[i, j]
    assert sphere[0] == pytest.approx(-5935.0, abs=40.0) and sphere[1] == pytest.approx(-2640.0, abs=40.0)


@needs_heights
def test_the_near_side_maria_form_one_sea_at_28_percent(moon):
    area = moon.grid.cell_area_m2
    _, labels = bs.seas(moon.height_m, area, bs.level_for_area(moon.height_m, area, 0.28), min_area_fraction=0.0)
    found = {int(labels[atlas.cell_index(moon.grid, lat, lon)]) for lat, lon in MARIA.values()}
    assert len(found) == 1 and 0 not in found


@needs_heights
@needs_terluna
def test_the_levels_of_the_seas_agree_with_terlunas(moon):
    area = moon.grid.cell_area_m2
    terluna_atlas = json.loads((TERLUNA / 'geography' / 'results' / 'atlas.json').read_text())
    # Within 0.5 m, the causes being LOLA's 16 pixels per degree where Terluna's atlas took 4, the geoid to degree 330
    # on the heights' own grid where Terluna's took degree 200 interpolated from 4 pixels per degree, and the tide at
    # the orbit's mean 1/r^3 where Terluna's took the mean distance.
    level = bs.level_for_area(moon.height_m, area, terluna_atlas['share'])
    assert level == pytest.approx(terluna_atlas['sea_level_m'], abs=0.5)
    with open(TERLUNA / 'geography' / 'results' / 'water_levels.csv') as handle:
        fine = {round(float(r['area_fraction']), 2): float(r['level_m']) for r in csv.DictReader(handle)}
    for share in (0.25, 0.35):          # within Terluna's own tolerance for its levels against this table
        assert bs.level_for_area(moon.height_m, area, share) == pytest.approx(fine[share], abs=10.0)


def test_the_moons_tide_is_earths_over_the_orbit_its_host_table_states():
    host = MOON['host']
    assert host['inclination_to_equator_deg'] == pytest.approx(5.145 + 1.5424, abs=1e-12)     # Cassini's laws
    assert geography.static_tide(MOON, LIB) == tp.Tide(LIB.world('earth')['body']['gm_m3_s2'], host['semi_major_axis_m'],
                                                       host['eccentricity'], host['inclination_to_equator_deg'], 0.0248, 0.0)


@needs_heights
def test_the_record_holds_the_tides_terms_and_its_mean_coefficients(moon):
    tide = moon.record['tide']
    assert tide['coefficients'] == list(tp.tide_coefficients(tide['eccentricity'], tide['inclination_deg']))
    assert (tide['semi_major_axis_m'], tide['love_k2'], tide['sub_longitude_deg']) == (384400000.0, 0.0248, 0.0)


@pytest.mark.parametrize('tables, message', [
    (dict(surface=dict(tide={**MOON['surface']['tide'], 'from': 'star'})), "comes from the world's host"),
    (dict(surface=dict(tide='host')), 'surface.tide is a table'),
    (dict(rotation=dict(sidereal_period_days=29.53)), 'synchronous with the orbit'),
    (dict(host=dict(eccentricity=1.0)), 'eccentricity is a number below 1.0'),
    (dict(host=dict(inclination_to_equator_deg=95.0)), 'inclination_to_equator_deg is a number below 90.0'),
    (dict(surface=dict(tide={**MOON['surface']['tide'], 'sub_longitude_deg': '0 E'})), 'sub_longitude_deg is a number'),
    (dict(surface=dict(tide={**MOON['surface']['tide'], 'love_k2': -0.1})), 'love_k2 is a number of at least 0.0'),
])
def test_the_tide_refuses_what_the_world_misstates(tables, message):
    with pytest.raises(SpecError, match=message):
        geography.static_tide(_with(**tables), LIB)


def test_a_world_that_states_no_tide_takes_none():
    surface = {k: v for k, v in MOON['surface'].items() if k != 'tide'}
    assert geography.static_tide({**MOON, 'surface': surface}, LIB) is None


@pytest.mark.parametrize('surface, message', [
    (dict(geometry='unchosen'), 'pinned set of files'),
    (dict(geometry='model-default'), 'pinned set of files'),
    (dict(geoid_degree=1), 'a degree from 2'),
    (dict(geoid_degree=330.0), 'a degree from 2'),
])
def test_heights_need_a_pinned_geometry_and_a_degree(surface, message):
    with pytest.raises(SpecError, match=message):
        geography.heights(_with(surface=surface), LIB, store=STORE)


@needs_heights
@pytest.mark.parametrize('body, message', [
    (dict(gm_m3_s2=4.282837e13), 'a gravity field of GM'),                # Mars's GM on the Moon's files
    (dict(radius_m=3389500.0), 'heights above a 1737400.0 m sphere'),     # and Mars's radius
])
def test_heights_refuse_files_of_another_world(body, message):
    with pytest.raises(SpecError, match=message):
        geography.heights(_with(body=body), LIB, store=STORE)


class _Files:
    """A stand-in for the manifest, holding a pin's files by name."""
    def __init__(self, paths):
        self.found = paths

    def paths(self, pin, store=None):
        return self.found


@pytest.mark.parametrize('labels, message', [
    ({'a.lbl': 'A.IMG', 'b.lbl': 'B.IMG', 'g.lbl': None}, 'two labels describe heights'),
    ({'a.lbl': 'C.IMG', 'g.lbl': None}, 'a.lbl describes C.IMG, which the pin holds no file of'),
    ({'a.lbl': 'A.IMG'}, 'describe no gravity'),
])
def test_the_files_are_refused_where_their_labels_misdescribe_them(tmp_path, labels, message):
    paths = {}
    for name, image in labels.items():
        text = '^SHADR_HEADER_TABLE = ("G.TAB",1)\nEND\n' if image is None else f'^IMAGE = "{image}"\nEND\n'
        (tmp_path / name).write_text(text)
        paths[name] = tmp_path / name
    for name in ('a.img', 'b.img', 'g.tab'):
        (tmp_path / name).write_bytes(b'')
        paths[name] = tmp_path / name
    with pytest.raises(SpecError, match=message):
        geography.surface_files(MOON, manifest=_Files(paths))
