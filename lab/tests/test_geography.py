"""A world's heights above its geoid through the data manifest: the Moon's LOLA heights over GRAIL's geoid, against
the shape its gravity field gives, published landing heights and Terluna's levels, and the tide the world states."""
import csv
import hashlib
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
OPEN_MOON = LIB.scenario('moon/open-moon')
STORE, TERLUNA, ENV = root('store'), root('terluna'), root('env')
PYTHON = ENV / 'bin' / 'python' if ENV is not None else None
# Five near-side maria's centres in the IAU gazetteer (MOON_nomenclature_center_pts.zip, sha256 404a951d51482159, as
# Terluna retrieved it on 2026-09-25), as latitude and east longitude.
MARIA = {'Oceanus Procellarum': (20.6714, -56.6774), 'Mare Imbrium': (34.7244, -14.9086),
         'Mare Serenitatis': (27.2879, 18.3596), 'Mare Crisium': (16.1774, 59.1037), 'Mare Nectaris': (-15.1852, 34.6021)}


def _stored(pin) -> bool:
    try:
        return STORE is not None and bool(Manifest().paths(pin, store=STORE))
    except DataError:
        return False


needs_heights = pytest.mark.skipif(not _stored(MOON['surface']['geometry']),
                                   reason="the store lacks the Moon's heights (lab/worldlab/data.py)")
needs_runoff = pytest.mark.skipif(not _stored(OPEN_MOON['water']['lakes_start']),
                                  reason="the store lacks the Open Moon's first runoff (lab/worldlab/data.py)")
needs_terluna = pytest.mark.skipif(TERLUNA is None, reason="Terluna's repository is unset (lab/local.example.toml)")
needs_env = pytest.mark.skipif(PYTHON is None or not PYTHON.exists(),
                               reason="the lab's environment is unset (lab/local.example.toml)")


@pytest.fixture(scope='module')
def moon():
    return geography.heights(MOON, LIB, store=STORE)


@pytest.fixture(scope='module')
def open_moon(moon):
    return geography.water(MOON, OPEN_MOON, moon, LIB, store=STORE)


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


@needs_heights
@needs_runoff
def test_the_open_moons_seas_cover_their_share_and_its_lakes_stand_above_them(open_moon):
    assert open_moon.record['seas']['share'] == pytest.approx(0.28, abs=1e-6)
    assert open_moon.level_m == pytest.approx(-1653.84, abs=0.01)
    assert not open_moon.sea.ravel()[open_moon.lake_cell].any()
    assert (open_moon.lake_level_m >= np.float32(open_moon.level_m)).all()
    runoff = open_moon.record['runoff']
    assert (runoff['run'], runoff['years']) == ('A28_dim5_moon', [20, 29])
    assert runoff['sha256'] == Manifest().files(OPEN_MOON['water']['lakes_start'])[0].sha256


@needs_heights
def test_a_scenario_without_lakes_takes_its_seas_alone(moon):
    scenario = {**OPEN_MOON, 'water': {**OPEN_MOON['water'], 'lakes': 'none', 'lakes_start': 'unchosen'}}
    seas = geography.water(MOON, scenario, moon, LIB, store=STORE)
    assert seas.lake_cell.size == 0 and seas.record['lakes'] is None
    assert seas.record['seas']['share'] == pytest.approx(0.28, abs=1e-6)


@needs_heights
@needs_runoff
@needs_terluna
def test_the_lakes_agree_with_terlunas_routing_of_the_same_runoff(open_moon, moon):
    terluna = json.loads((TERLUNA / 'geography' / 'results' / 'drainage.json').read_text())
    sha256 = Manifest().files(OPEN_MOON['water']['lakes_start'])[0].sha256
    if terluna['sources'].get('climate/gcm/products/climatology_A28_dim5_moon.npz') != sha256:
        pytest.skip("Terluna's lakes now come from other runoff than the pinned climatology")
    with np.load(TERLUNA / 'geography' / 'products' / 'drainage_28pct_16ppd.npz') as products:
        assert json.loads(str(products['metadata']))['sources'] == terluna['sources']
        cells, levels = products['lake_cell'], products['lake_level_m']
    # Within 1%, the causes being the lab's heights (the geoid to degree 330 on LOLA's own grid, the tide averaged
    # over the orbit), 1.9 m rms from Terluna's, and its sea level, 0.36 m above Terluna's.
    flat = moon.grid.cell_area_m2.ravel()
    shared, terlunas, labs = np.intersect1d(cells, open_moon.lake_cell, return_indices=True)
    assert flat[shared].sum() / flat[cells].sum() > 0.99
    assert open_moon.record['lakes']['share'] == pytest.approx(flat[cells].sum() / flat.sum(), rel=0.01)
    for table, key in (('lakes', 'bodies'), ('lakes', 'closed_bodies'), ('lakes', 'volume_km3'),
                       ('rivers', 'discharge_to_sea_m3s')):
        assert open_moon.record[table][key] == pytest.approx(terluna[table][key], rel=0.01), key
    # The lakes' surfaces move with the heights, by metres; where a pass between depressions moves, a lake spills
    # at another level, by up to kilometres over 0.05% of the shared area.
    near = np.abs(open_moon.lake_level_m[labs].astype(float) - levels[terlunas]) <= 10.0
    assert flat[shared][near].sum() / flat[shared].sum() > 0.99


@pytest.mark.parametrize('scenario, message', [
    (dict(water=dict(seas='model-default')), 'floods the heights'),
    (dict(water=dict(lakes='terluna:lakes.npz')), 'routes runoff'),
    (dict(water=dict(seas_share='unchosen')), 'seas_share is a number'),
    (dict(water=dict(seas_share=1.0)), 'seas_share is a number below 1.0'),
    (dict(water=dict(lakes_start='unchosen')), 'lakes_start is a pinned climatology'),
    (dict(water=dict(lakes_start='terluna:climate.npz#runoff')), 'takes no # entry'),
    (dict(world='mars'), "a scenario of the world 'mars' on the world 'moon'"),
])
def test_the_water_refuses_what_this_function_leaves_unflooded_or_unrouted(scenario, message):
    changed = {**OPEN_MOON, **{k: ({**OPEN_MOON[k], **v} if isinstance(v, dict) else v) for k, v in scenario.items()}}
    with pytest.raises(SpecError, match=message):
        geography.water(MOON, changed, object(), LIB, store=STORE)


class _One:
    """A stand-in for the manifest, holding one pin's file."""
    def __init__(self, path):
        self.found = path

    def path(self, pin, store=None):
        return self.found


def _climate(lat=(-45.0, 45.0), lon=(0.0, 180.0), shape=(2, 2)):
    return dict(lat=np.array(lat), lon=np.array(lon), **{k: np.zeros(shape) for k in ('lsm', 'pr_mm_day', 'evap_mm_day')})


@pytest.mark.parametrize('schema, fields, message', [
    ('other/1', _climate(), 'of schema'),
    (geography.CLIMATOLOGY_SCHEMAS[0], {k: v for k, v in _climate().items() if k != 'evap_mm_day'}, 'without'),
    (geography.CLIMATOLOGY_SCHEMAS[0], _climate(shape=(2, 3)), 'fields of shapes'),
    (geography.CLIMATOLOGY_SCHEMAS[0], _climate(lon=(180.0, 0.0)), 'ascending from 0 E'),
    (geography.CLIMATOLOGY_SCHEMAS[0], _climate(lat=(45.0, 45.0)), 'latitudes in order'),
])
def test_a_climatology_is_refused_where_its_schema_fields_or_grid_differ(tmp_path, schema, fields, message):
    path = tmp_path / 'climatology.npz'
    np.savez(path, metadata=json.dumps(dict(schema=schema)), **fields)
    with pytest.raises(SpecError, match=message):
        geography.climatology('x.npz', manifest=_One(path))


def test_a_climatology_reads_its_fields_and_its_hash(tmp_path):
    path = tmp_path / 'climatology.npz'
    np.savez(path, metadata=json.dumps(dict(schema=geography.CLIMATOLOGY_SCHEMAS[0], run='R')), **_climate())
    fields, meta, sha256 = geography.climatology('x.npz', manifest=_One(path))
    assert set(fields) == set(geography.CLIMATOLOGY_FIELDS) and meta['run'] == 'R'
    assert sha256 == hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope='module')
def open_moon_t21(open_moon, moon):
    return geography.model_surface(open_moon, moon, 32)


def test_a_gaussian_grid_splits_the_sphere_by_its_weights():
    lat, edges = geography.gaussian_latitudes(32)
    weights = np.polynomial.legendre.leggauss(32)[1]
    assert edges[0] == 1.0 and edges[-1] == pytest.approx(-1.0, abs=1e-14) and np.all(np.diff(edges) < 0)
    assert np.allclose(-np.diff(edges), weights, atol=1e-15)          # symmetric, so in either order
    assert np.allclose(lat, -lat[::-1], atol=1e-12) and np.all((np.sin(np.radians(lat)) < edges[:-1]) & (np.sin(np.radians(lat)) > edges[1:]))


@needs_heights
@needs_runoff
def test_the_model_grid_keeps_the_shares_of_water_and_land(open_moon_t21, open_moon):
    wet = open_moon.record['seas']['share'] + open_moon.record['lakes']['share']
    assert open_moon_t21.record['land_share'] == pytest.approx(1.0 - wet, abs=1e-12)
    assert open_moon_t21.cell_area_fraction.sum() == pytest.approx(1.0, abs=1e-12)
    assert (open_moon_t21.land_elevation_m >= 0).all() and (open_moon_t21.water_surface_m >= 0).all()
    assert (open_moon_t21.water_depth_m >= 0).all() and ((open_moon_t21.land_fraction >= 0) & (open_moon_t21.land_fraction <= 1)).all()


def _terluna_t21(name):
    from scipy.io import netcdf_file
    with netcdf_file(TERLUNA / 'climate' / 'gcm' / 'products' / name, 'r', mmap=False) as f:
        return {k: np.array(v[:], dtype=float) for k, v in f.variables.items()}


@needs_heights
@needs_terluna
@pytest.mark.parametrize('percent', [25, 35])
def test_the_seas_alone_match_terlunas_surfaces_on_its_t21_grid(moon, percent):
    scenario = {**OPEN_MOON, 'water': {**OPEN_MOON['water'], 'seas_share': percent / 100, 'lakes': 'none'}}
    surface = geography.model_surface(geography.water(MOON, scenario, moon, LIB, store=STORE), moon, 32)
    terluna = _terluna_t21(f'moon_{percent}pct_water_gaussian_T21.nc')
    assert np.allclose(surface.lat_deg, terluna['lat'], atol=1e-4) and np.allclose(surface.lon_deg, terluna['lon'], atol=1e-9)
    assert np.allclose(surface.cell_area_fraction, terluna['cell_area_fraction'], atol=1e-9)
    # Terluna's surfaces average its 1-degree land-sea products of LOLA's 4-pixel heights over its degree-200 geoid;
    # the lab's, LOLA's 16-pixel heights over its degree-330 geoid.
    weights = surface.cell_area_fraction
    difference = surface.land_fraction - terluna['land_fraction']
    assert abs((difference * weights).sum()) < 1e-3
    assert np.sqrt((difference**2 * weights).sum()) < 0.01 and np.abs(difference).max() < 0.06
    for labs, terlunas, share in ((surface.land_elevation_m, terluna['land_elevation_m'], surface.land_fraction),
                                  (surface.water_depth_m, terluna['ocean_depth_m'], 1.0 - surface.land_fraction)):
        terluna_share = terluna['land_fraction'] if share is surface.land_fraction else 1.0 - terluna['land_fraction']
        both = (share > 0.05) & (terluna_share > 0.05)            # where each holds a twentieth of its cell or more
        part = weights[both] / weights[both].sum()
        offset = (labs - terlunas)[both]
        assert abs((offset * part).sum()) < 10.0 and np.sqrt((offset**2 * part).sum()) < 50.0


@needs_heights
@needs_runoff
@needs_terluna
def test_the_seas_agree_with_terlunas_atlas(open_moon):
    with np.load(TERLUNA / 'geography' / 'products' / 'atlas_28pct_4ppd.npz') as products:
        meta, terlunas = json.loads(str(products['metadata'])), products['water_label'] > 0
    if meta['share'] != OPEN_MOON['water']['seas_share']:
        pytest.skip("Terluna's atlas now floods another share")
    # Within 1% of the surface, the cause being LOLA's 4-pixel grid under Terluna's atlas, a gridding of its own,
    # where the lab floods the 16-pixel heights, here taken a block of 16 cells at a time.
    labs = open_moon.sea.reshape(720, 4, 1440, 4).mean(axis=(1, 3)) > 0.5
    weights = np.cos(np.radians(90.0 - (np.arange(720) + 0.5) / 4))[:, None] * np.ones((1, 1440))
    assert (weights * (labs != terlunas)).sum() / weights.sum() < 0.01


@needs_heights
@needs_runoff
def test_the_open_moons_lowest_point_is_its_sea(open_moon, moon):
    lowest = geography.lowest_level_pressure(MOON, OPEN_MOON, open_moon, moon)
    assert lowest['lowest_level_pressure_hpa'] == 1215.9 and lowest['lowest_surface_m'] == open_moon.level_m


def _dry(depth_m, lake=None):
    """A globe at 1 pixel per degree, flat at 0 m but for one hollow of `depth_m`, without seas; `lake` (surface, bed)
    floods a second hollow."""
    grid = tp.Grid.globe(1, MOON['body']['radius_m'])
    height = np.zeros((180, 360))
    height[90, 180] = -depth_m
    cells, levels = np.zeros(0, np.int32), np.zeros(0, np.float32)
    if lake is not None:
        height[45, 90] = lake[1]
        cells, levels = np.array([45 * 360 + 90], np.int32), np.array([lake[0]], np.float32)
    return (geography.Heights(height, np.zeros_like(height), grid, {}),
            geography.Water(10.0, np.zeros(height.shape, bool), cells, levels, np.zeros(cells.size, bool), {}))


# The Open Moon's gravity and its air's molar mass, as world_spec.md's table gives them.
G_MOON, M_AIR = 1.6242107, 0.0288319


def test_the_pressure_at_a_dry_hollow_follows_isothermal_hydrostatics():
    topography, water = _dry(500.0)
    scenario = {**OPEN_MOON, 'air': {**OPEN_MOON['air'], 'reference_level': 'sea'}}
    lowest = geography.lowest_level_pressure(MOON, scenario, water, topography)
    expected = 1215.9 * math.exp(M_AIR * G_MOON * 500.0 / (8.314462618 * 295.0))
    assert lowest['lowest_level_pressure_hpa'] == pytest.approx(expected, rel=1e-6) and lowest['lowest_surface_m'] == -500.0


def test_a_lakes_bed_stays_under_its_water():
    topography, water = _dry(50.0, lake=(-100.0, -500.0))
    scenario = {**OPEN_MOON, 'air': {**OPEN_MOON['air'], 'reference_level': 'sea'}}
    lowest = geography.lowest_level_pressure(MOON, scenario, water, topography)
    expected = 1215.9 * math.exp(M_AIR * G_MOON * 100.0 / (8.314462618 * 295.0))
    assert lowest['lowest_surface_m'] == -100.0 and lowest['lowest_level_pressure_hpa'] == pytest.approx(expected, rel=1e-6)


@pytest.mark.parametrize('level, message', [('mean-radius', 'names a sphere'), ('unchosen', 'is "water"')])
def test_the_pressure_takes_its_reference_at_an_equipotential(level, message):
    topography, water = _dry(500.0)
    scenario = {**OPEN_MOON, 'air': {**OPEN_MOON['air'], 'reference_level': level}}
    with pytest.raises(SpecError, match=message):
        geography.lowest_level_pressure(MOON, scenario, water, topography)


def _strip_and_lake():
    """A globe at 1 pixel per degree: land 1,000 m above a water level of -1,000 m; a sea strip 1,000 m deep from
    359 to 360 E; and a lake whose surface stands 900 m above that level, over a bed 400 m below its surface."""
    grid = tp.Grid.globe(1, MOON['body']['radius_m'])
    height = np.zeros((180, 360))
    sea = np.zeros(height.shape, bool)
    sea[:, 359] = True
    height[sea] = -2000.0
    lake = (np.arange(85, 90)[:, None] * 360 + np.arange(100, 104)[None, :]).ravel().astype(np.int32)
    height.ravel()[lake] = -500.0
    water = geography.Water(-1000.0, sea, lake, np.full(lake.size, -100.0, np.float32), np.ones(lake.size, bool), {})
    return geography.Heights(height, np.zeros_like(height), grid, {}), water


def test_the_model_grid_averages_a_strip_across_the_seam_and_a_lake_exactly():
    topography, water = _strip_and_lake()
    surface = geography.model_surface(water, topography, 32)
    # Column 0 spans 2.8125 degrees either side of 0 E, so the strip from 359 to 360 E is 1/5.625 of its width.
    assert np.allclose(1.0 - surface.land_fraction[:, 0], 1.0 / 5.625, rtol=0, atol=1e-12)
    assert np.allclose(surface.water_depth_m[:, 0], 1000.0, atol=1e-9) and np.allclose(surface.water_surface_m[:, 0], 0.0)
    assert np.allclose(surface.land_elevation_m, 1000.0, atol=1e-9)
    row = int(np.argmin(np.abs(surface.lat_deg - 2.5)))
    column = int(np.argmin(np.abs(surface.lon_deg - 102.0)))
    assert surface.water_surface_m[row, column] == pytest.approx(900.0, abs=1e-6)
    assert surface.water_depth_m[row, column] == pytest.approx(400.0, abs=1e-6)
    land = topography.grid.cell_area_m2.ravel()
    wet = water.sea.ravel().copy()
    wet[water.lake_cell] = True
    assert surface.record['land_share'] == pytest.approx(land[~wet].sum() / land.sum(), abs=1e-12)


def test_the_model_grid_refuses_other_row_counts_and_grids():
    topography, water = _strip_and_lake()
    with pytest.raises(SpecError, match='a Gaussian grid of 21 rows'):
        geography.model_surface(water, topography, 21)
    half = geography.Heights(topography.height_m[:90], topography.geoid_m[:90], topography.grid, {})
    with pytest.raises(SpecError, match='takes a global grid'):
        geography.model_surface(water, half, 32)


EXOPLASIM_GRID = r'''
import json, os, sys
import netCDF4, numpy as np
import exoplasim
with netCDF4.Dataset(os.path.join(os.path.dirname(exoplasim.__file__), 'T21.nc')) as grid:
    print(json.dumps(dict(lat=np.asarray(grid['lat'][:]).tolist(), lon=np.asarray(grid['lon'][:]).tolist())))
'''


@needs_env
def test_the_model_grid_is_exoplasims_own_t21():
    import subprocess
    done = subprocess.run([PYTHON, '-c', EXOPLASIM_GRID], capture_output=True, text=True, timeout=120)
    assert done.returncode == 0, done.stderr[-2000:]
    exoplasims = json.loads(done.stdout)
    topography, water = _strip_and_lake()
    surface = geography.model_surface(water, topography, 32)
    assert np.allclose(surface.lat_deg, exoplasims['lat'], rtol=0, atol=1e-12)
    assert np.allclose(surface.lon_deg, exoplasims['lon'], rtol=0, atol=1e-12)


@pytest.fixture(scope='module')
def open_moon_run(open_moon_t21, tmp_path_factory):
    """The Open Moon's first design run, written by the ExoPlaSim adapter over the lab's own surface."""
    from worldlab import exoplasim as ex
    if not ex.ARCHIVE.exists():
        pytest.skip('upstream/ lacks the pinned ExoPlaSim archive')
    folder = tmp_path_factory.mktemp('open-moon') / 'design'
    design = LIB.study('open-moon').gcm['design'].settings
    record = ex.write_run(folder, MOON, OPEN_MOON, design, calibrations=ex.Calibrations.identity(),
                          surface=open_moon_t21, store=STORE)
    return folder, record


@needs_heights
@needs_runoff
@pytest.mark.skipif(STORE is None, reason="the lab's store is unset (lab/local.example.toml)")
def test_the_open_moons_first_run_takes_its_own_surface(open_moon_run, open_moon_t21):
    from worldlab import exoplasim as ex
    folder, record = open_moon_run
    assert {p.name for p in folder.iterdir()} == \
        set(ex.NAMELISTS) | {'sun.dat', 'sun_hr.dat', 'N032_surf_0172.sra', 'N032_surf_0129.sra'}
    assert (record['sunlight']['scale'], record['sunlight']['basis'], record['surface']['kind']) == \
        (1.0, 'identity', 'heights')
    shares = record['surface']
    assert shares['surface_land_share'] == pytest.approx(0.6167, abs=5e-5)
    assert abs(shares['mask_land_share'] - shares['surface_land_share']) < open_moon_t21.cell_area_fraction.max()


def _sra(path) -> np.ndarray:
    return np.array([float(x) for line in path.read_text().splitlines()[1:] for x in line.split()]).reshape(32, 64)


@needs_heights
@needs_runoff
@needs_terluna
@pytest.mark.skipif(STORE is None or root('terluna-drive') is None, reason="the lab's store or Terluna's drive is unset")
def test_the_open_moons_mask_differs_from_terlunas_where_their_lakes_differ(open_moon_run, open_moon, open_moon_t21):
    folder, record = open_moon_run
    ours = _sra(folder / 'N032_surf_0172.sra')
    theirs = _sra(root('terluna-drive') / 'gcm-runs' / 'A28_corrected_970' / 'inputs' / 'moon_landmask.sra')
    area = open_moon_t21.cell_area_fraction
    terluna = _terluna_t21('moon_28pct_water_lakes_gaussian_T21.nc')
    # Both masks keep their surfaces' land, the 28% seas and their lakes taken away: the lab's lakes are routed from
    # run A28_dim5_moon's runoff over its own heights, and those of Terluna's design surface from run A's over Terluna's.
    lab_lakes = open_moon.record['lakes']['share']
    terluna_lakes = 1.0 - 0.28 - float((terluna['land_fraction'] * terluna['cell_area_fraction']).sum())
    assert (lab_lakes, terluna_lakes) == (pytest.approx(0.1033, abs=5e-5), pytest.approx(0.1202, abs=5e-5))
    assert float((theirs * area).sum()) == pytest.approx(0.5995, abs=5e-5)
    assert record['surface']['mask_land_share'] - float((theirs * area).sum()) == \
        pytest.approx(terluna_lakes - lab_lakes, abs=1e-3)
    # Cell by cell the masks part over 111 cells, 7.2% of the surface: 4.45% land in the lab's mask where Terluna's holds
    # water, and 2.75% the reverse, where the two surfaces' land fractions differ with their lakes.
    lab_only, terluna_only = (ours > theirs), (theirs > ours)
    assert int(lab_only.sum() + terluna_only.sum()) == 111
    assert (float(area[lab_only].sum()), float(area[terluna_only].sum())) == \
        (pytest.approx(0.0445, abs=5e-4), pytest.approx(0.0275, abs=5e-4))
    gap = open_moon_t21.land_fraction - terluna['land_fraction']
    assert float(np.median(gap[lab_only])) > 0 > float(np.median(gap[terluna_only]))


@needs_heights
@needs_runoff
@pytest.mark.skipif(STORE is None or ENV is None, reason="the lab's store or environment is unset (lab/local.example.toml)")
def test_plasim_compiled_by_the_lab_runs_the_open_moons_first_run(open_moon_run, tmp_path):
    import re
    import shutil
    import subprocess
    from worldlab import builds, derive, exoplasim as ex
    if shutil.which('mpif90') is None or not ex.ARCHIVE.exists():
        pytest.skip('a build needs MPI and the pinned archive')
    design = LIB.study('open-moon').gcm['design'].settings
    folder, _ = open_moon_run
    run = tmp_path / 'design'
    shutil.copytree(folder, run)
    executable = builds.build(design, store=STORE, env=ENV) / 'exoplasim' / 'plasim' / 'run' / builds.executable_name(design)
    shutil.copy2(executable, run / executable.name)
    text = (run / 'plasim_namelist').read_text()
    for name, value in (('N_RUN_YEARS', 0), ('N_RUN_MONTHS', 0), ('N_RUN_DAYS', 0), ('N_RUN_STEPS', 4)):
        text, count = re.subn(rf'^ {name} = .*$', f' {name} = {value}', text, flags=re.M)
        assert count == 1, name
    (run / 'plasim_namelist').write_text(text)
    done = subprocess.run(['nice', '-n', '10', 'mpirun', '-np', str(design['ranks']), './' + executable.name], cwd=run,
                          capture_output=True, text=True, timeout=900)
    # PlaSim aborts through MPI_ABORT with an error code of 0, which mpirun reports as success (mpimod.f90:385).
    assert done.returncode == 0 and 'MPI_ABORT' not in done.stdout + done.stderr, done.stderr[-2000:]
    assert not (run / 'Abort_Message').exists() and (run / 'plasim_status').is_file()
    diag = (run / 'plasim_diag').read_text()
    found = {label: float(re.search(r'\* ' + re.escape(label) + r'[^:]*:\s*([-0-9.]+)', diag).group(1))
             for label in ('Solar    day', 'Timesteps / day', 'Days / Year')}
    calendar = derive.calendar(MOON, design)
    assert found['Solar    day'] == pytest.approx(calendar['model_day_s'], abs=0.0501)
    assert (found['Timesteps / day'], found['Days / Year']) == (calendar['steps_per_model_day'], calendar['n_days_per_year'])
    assert (run / 'plasim_output').stat().st_size > 0
