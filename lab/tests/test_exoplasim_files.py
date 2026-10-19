"""The namelists of a GCM run, written by the lab's ExoPlaSim adapter: their format, the rules each entry follows,
Terluna's design run A28_corrected_970 with each difference's cause, and ExoPlaSim's own configure, run in the lab's
environment."""
import hashlib
import io
import json
import math
import re
import subprocess

import numpy as np
import pytest

from worldlab import derive, exoplasim as ex, sunlight
from worldlab.data import DataError, Manifest
from worldlab.geography import ModelSurface
from worldlab.roots import root
from worldlab.spec import LAB, Library, SpecError

LIB = Library()
MOON, EARTH = LIB.world('moon'), LIB.world('earth')
OPEN_MOON, CONTROL = LIB.scenario('moon/open-moon'), LIB.scenario('earth/control')
SEED, SEED_AIR = LIB.world('waterworld-seed'), LIB.scenario('waterworld-seed/gaean-1bar')
STUDY = LIB.study('open-moon')
DESIGN, LW_ICE = STUDY.gcm['design'].settings, STUDY.gcm['design_lw_ice'].settings
DEFAULTS = LIB.defaults('exoplasim/defaults')
RECORDED = LAB.parent / 'models' / 'exoplasim' / 'design_case'
STORE, TERLUNA, ENV = root('store'), root('terluna'), root('env')
PYTHON = ENV / 'bin' / 'python' if ENV is not None else None
FIRST = ex.TopOfAir(1236.0, 1.0, 'identity')          # a first run's sunlight on the Open Moon, made up
LATER = ex.TopOfAir(1199.0, 0.97, 'calibration')      # with the target stage's scale of `_given`
INTEGER = re.compile(r'[+-]?\d+')


def _stored(*pins) -> bool:
    try:
        return STORE is not None and all(Manifest().paths(pin, store=STORE) for pin in pins)
    except DataError:
        return False


needs_archive = pytest.mark.skipif(not ex.ARCHIVE.exists(), reason='upstream/ lacks the pinned ExoPlaSim archive')
needs_terluna = pytest.mark.skipif(TERLUNA is None, reason="Terluna's repository is unset (lab/local.example.toml)")
needs_sunlight = pytest.mark.skipif(not _stored(MOON['star']['spectrum'], OPEN_MOON['sunlight']['filter']),
                                    reason="the store lacks the Sun's spectrum or the shield's transmission")
needs_env = pytest.mark.skipif(PYTHON is None or not PYTHON.exists(),
                               reason="the lab's environment is unset (lab/local.example.toml)")


def _same(a: str, b: str, rel: float = 1e-12) -> bool:
    """Two namelist values that agree: equal as written, or each number within `rel` of the other's, an integer
    matching an integer alone, since Fortran reads an integer entry written as a float as an error."""
    if a == b:
        return True
    xs, ys = a.split(','), b.split(',')
    if len(xs) != len(ys):
        return False
    for x, y in zip(xs, ys):
        x, y = x.strip(), y.strip()
        if INTEGER.fullmatch(x) or INTEGER.fullmatch(y):
            if not (INTEGER.fullmatch(x) and INTEGER.fullmatch(y) and int(x) == int(y)):
                return False
            continue
        try:
            if not math.isclose(float(x), float(y), rel_tol=rel, abs_tol=0.0):
                return False
        except ValueError:
            return False
    return True


def _entries(text: str) -> dict:
    return {key.upper(): value for key, value in ex.parse(text)[1]}


def _compare(lab: dict, other: dict) -> tuple[dict, dict, dict]:
    """The entries that differ, those only the lab writes and those only the other writes."""
    differ = {k: (lab[k], other[k]) for k in lab.keys() & other.keys() if not _same(lab[k], other[k])}
    return differ, {k: lab[k] for k in lab.keys() - other.keys()}, {k: other[k] for k in other.keys() - lab.keys()}


def terluna_calibrations() -> ex.Calibrations:
    """Terluna's calibrations of its design run A28_corrected_970, read in place: the ledger's full terms
    (climate/results/gcm/twilight.json, as its runner summed them for its "full" mode, exoplasim_run.py:885-902), the
    gas bands (shortwave_gases.json) and the longwave correction (longwave_A28_corrected_970_heating.json), with the
    values its runner typed in (MODEL, exoplasim_run.py:98-145: RAYSCALE 2.237, SWH2OSCALE 1.292, TH2OC 0.004) and
    its session script's sunlight scale, 0.970."""
    results = TERLUNA / 'climate' / 'results' / 'gcm'
    product = json.loads((results / 'twilight.json').read_text())
    term, cone, longwave = product['gcm_term'], product['gcm_term_cone'], product['longwave']
    ledger = ex.Ledger(
        elevation_deg=tuple(term['elevation_deg']), ground=tuple(term['ground']),
        layers=tuple(tuple(q + c for q, c in zip(lq, lc)) for lq, lc in zip(term['layers'], cone['layers'])),
        escape_w_m2=tuple(a + b for a, b in zip(longwave['gcm_layers']['curved'], longwave['gcm_layers']['cone']))
        + (longwave['ground_curved_w_m2'],),
        escape_temperature_k=tuple(longwave['gcm_layers']['temperature_k']) + (longwave['ground_temperature_k'],),
        slant=tuple(product['magnification'][k] for k in 'abc'),
        slant_air=tuple(product['magnification_air'][k] for k in 'abc'))
    fits = json.loads((results / 'shortwave_gases.json').read_text())['fits']
    correction = json.loads((results / 'longwave_A28_corrected_970_heating.json').read_text())['correction']
    return ex.Calibrations(sunlight_scale=0.970, rayleigh_scale=2.237, water_absorption_scale=1.292,
                           water_continuum=0.004, ledger=ledger,
                           gas_bands=tuple(tuple(fits[k]) for k in ('co2_nir', 'o2_nir', 'o2_vis')),
                           longwave=ex.Longwave(tuple(correction['land']), tuple(correction['sea']),
                                                tuple(correction['tref'])))


def _given(**changes) -> ex.Calibrations:
    """Calibrations with every value the design run reads, made up, and `changes` on top."""
    ledger = ex.Ledger(elevation_deg=(0.0,), ground=(0.0,), layers=((0.0,),) * 10, escape_w_m2=(0.0,) * 11,
                       escape_temperature_k=(250.0,) * 11, slant=(0.1, 0.2, 0.3), slant_air=(0.4, 0.5, 0.6))
    values = dict(sunlight_scale=0.97, rayleigh_scale=2.0, water_absorption_scale=1.3, water_continuum=0.004,
                  ledger=ledger, gas_bands=((1.0,) * 5,) * 3)
    return ex.Calibrations(**{**values, **changes})


def _with(item: dict, **tables) -> dict:
    return {**item, **{name: {**item[name], **fields} for name, fields in tables.items()}}


# The format.

def test_values_are_written_as_configure_writes_them():
    assert [ex.text(v) for v in (1, 30.0, 1.6242107, 'sun.dat', (0.4, 0.8), -1.0, np.float64(0.5))] == \
        ['1', '30.0', '1.6242107', "'sun.dat'", '0.4,0.8', '-1.0', '0.5']
    for bad in (True, float('nan'), float('inf'), [1.0], None, np.int64(3)):
        with pytest.raises(SpecError):
            ex.text(bad)


def test_entries_replace_the_templates_own_whatever_their_case_and_the_rest_follow():
    template = ' &x_nl\n A = 1\n b   =   2\n NSTPW  =  160 \n /END\n'
    assert ex.merged(template, {'B': 3, 'NSTPW': 143, 'C': 4.0}) == \
        ' &x_nl\n A = 1\n b = 3\n NSTPW = 143\n C = 4.0\n /END\n'
    assert ex.parse(ex.merged(template, {})) == ('x_nl', [('A', '1'), ('b', '2'), ('NSTPW', '160')])
    assert ex.parse(' &x_nl\n A = 1\n &END\n') == ('x_nl', [('A', '1')])
    with pytest.raises(SpecError, match='repeat a name'):
        ex.merged(template, {'C': 1, 'c': 2})
    for broken, match in ((' A = 1\n &x_nl\n /END\n', 'outside its group'), (' &x_nl\n A 1\n /END\n', 'without'),
                          (' A = 1\n', 'outside its group'), (' &x_nl\n &y_nl\n /END\n', 'second group'),
                          (' &x_nl\n A = 1 /\n', 'one line'), ('\n', 'without its &group')):
        with pytest.raises(DataError, match=match):
            ex.parse(broken)
    assert _same('143', '143') and not _same('143', '143.0') and _same('0.5', '0.50000000000000001')


@needs_archive
def test_the_templates_come_from_the_pinned_archive_alone(tmp_path):
    templates = ex.templates()
    assert set(templates) == set(ex.NAMELISTS)
    assert ex.parse(templates['planet_namelist'])[1][:2] == [('ECCEN', '0.0'), ('MVELP', '102.7')]
    pins = tmp_path / 'pins.sha256'
    pins.write_text('# a comment\n\n' + ex.PINS.read_text())
    assert ex.templates(ex.ARCHIVE, pins) == templates
    fake = tmp_path / ex.ARCHIVE.name
    fake.write_bytes(b'something else')
    with pytest.raises(DataError, match='differs from its pin'):
        ex.templates(fake)
    with pytest.raises(DataError, match='missing'):
        ex.templates(tmp_path / 'absent' / ex.ARCHIVE.name)


# The switches as the build and the calibrations make them.

def test_planned_settings_resolve_to_what_the_build_does():
    assert ex.series(DESIGN)[-1] == '10-ice-optics.patch' and len(ex.series(DESIGN)) == 10
    first, later = ex.resolve(DESIGN, ex.Calibrations.identity()), ex.resolve(LW_ICE, _given())
    assert (first['twilight'], first['gas_bands'], first['ice_weights']) == ('none', False, 'patch-10')
    assert (later['twilight'], later['gas_bands'], later['ice_weights'], later['ice_optics']) == \
        ('full', True, 'patch-10', True)
    with_11 = {**DESIGN, 'patches': list(ex.series(DESIGN)) + ['11-ice-weights.patch']}
    assert ex.resolve(with_11, _given())['ice_weights'] == 'from-spectrum'
    assert ex.resolve(_with(DESIGN, switches={'ice_weights': 'patch-10'}), _given())['ice_weights'] == 'patch-10'
    with pytest.raises(SpecError, match='ice_weights'):
        ex.resolve(_with(DESIGN, switches={'ice_weights': 'measured'}), _given())


# The rules each entry follows.

def test_a_first_run_holds_every_calibration_at_the_released_models_own_value():
    entries = ex.namelists(MOON, OPEN_MOON, DESIGN, top=FIRST, calibrations=ex.Calibrations.identity())
    radmod = entries['radmod_namelist']
    assert {k: radmod[k] for k in ('RAYSCALE', 'SWH2OSCALE', 'TH2OC', 'NTWILIGHT', 'NTWILW', 'NGASBANDS', 'NLWCORR')} \
        == dict(RAYSCALE=1.0, SWH2OSCALE=1.0, TH2OC=0.024, NTWILIGHT=0, NTWILW=0, NGASBANDS=0, NLWCORR=0)
    assert not [k for k in radmod if k.startswith(('ZMLUNAR', 'ZGASQ', 'ZGASW', 'ZMAIRLUNAR'))]
    assert radmod['NSUNCLOCK'] == 2 and radmod['NICEOPT'] == 0 and 'TICEOPT' not in radmod
    assert entries['planet_namelist']['GSOL0'] == 1236.0
    with pytest.raises(SpecError, match='first run takes every calibration'):
        ex.Calibrations(first_run=True, water_continuum=0.004)
    with pytest.raises(SpecError, match='longwave correction off'):
        ex.namelists(MOON, OPEN_MOON, LW_ICE, top=FIRST, calibrations=ex.Calibrations.identity())


def test_the_sunlights_scale_agrees_with_the_scenario_and_the_calibrations():
    for top, calibrations in ((LATER, ex.Calibrations.identity()), (FIRST, _given()),
                              (ex.TopOfAir(1199.0, 0.96, 'calibration'), _given()),
                              (ex.TopOfAir(1199.0, 0.97, 'scenario'), _given())):
        with pytest.raises(SpecError, match='takes scale'):
            ex.namelists(MOON, OPEN_MOON, DESIGN, top=top, calibrations=calibrations)
    with pytest.raises(SpecError, match='takes scale'):
        ex.namelists(EARTH, CONTROL, DEFAULTS, top=ex.TopOfAir(1361.0, 1.0, 'identity'),
                     calibrations=ex.Calibrations.identity())
    with pytest.raises(SpecError, match="target stage's scale is missing"):
        ex.top_of_air(MOON, OPEN_MOON, _given(sunlight_scale=None))
    with pytest.raises(SpecError, match='states its sunlight scale'):
        ex.top_of_air(EARTH, CONTROL, ex.Calibrations(sunlight_scale=0.97))


def test_a_later_run_reads_every_calibration_its_switches_use():
    entries = ex.namelists(MOON, OPEN_MOON, DESIGN, top=LATER, calibrations=_given())
    radmod = entries['radmod_namelist']
    assert [radmod[f'ZMLUNAR({i})'] for i in (1, 2, 3)] == [0.1, 0.2, 0.3]
    assert [radmod[f'ZMAIRLUNAR({i})'] for i in (1, 2, 3)] == [0.4, 0.5, 0.6]
    assert len([k for k in radmod if k.startswith('ZGASQ(')]) == 15
    mass = derive.zgasw(derive.mole_fractions(OPEN_MOON))
    assert (radmod['ZGASW(1)'], radmod['ZGASW(2)']) == (mass['CO2'], mass['O2'])
    for missing, run in (('ledger', DESIGN), ('gas_bands', DESIGN), ('water_continuum', DESIGN), ('longwave', LW_ICE)):
        with pytest.raises(SpecError, match=missing):
            ex.namelists(MOON, OPEN_MOON, run, top=LATER, calibrations=_given(**{missing: None}))
    plain = _with(DESIGN, switches={'twilight': 'none', 'gas_bands': False})
    radmod = ex.namelists(MOON, OPEN_MOON, plain, top=LATER, calibrations=_given(ledger=None))['radmod_namelist']
    assert radmod['NTWILIGHT'] == 0 and radmod['NGASBANDS'] == 0 and 'ZMLUNAR(1)' not in radmod
    with pytest.raises(SpecError, match='five coefficients'):
        _given(gas_bands=((1.0,) * 4,) * 3)
    with pytest.raises(SpecError, match='positive number'):
        _given(water_continuum=0.0)


def test_the_switches_set_their_patches_entries():
    switched = _with(LW_ICE, switches={'sun_clock': 'plasim', 'cloud_water': 'full_column', 'surface_cloud_rcrit': 0.9,
                                       'convective_day_s': 0.0})
    calibrations = _given(longwave=ex.Longwave((0.0,) * 11, (0.0,) * 11, (250.0,) * 11))
    entries = ex.namelists(MOON, OPEN_MOON, switched, top=LATER, calibrations=calibrations)
    rain, radmod, plasim = entries['rainmod_namelist'], entries['radmod_namelist'], entries['plasim_namelist']
    assert rain == {'CWGREF': 9.80665, 'CWSCALE': 1.0, 'CONVDAY': 0.0, 'RCRIT(10)': 0.9}
    assert (radmod['NSUNCLOCK'], radmod['NLWCORR'], radmod['NICEOPT'], radmod['TICEOPT']) == (0, 1, 1, 235.15)
    assert plasim['NDIAGGP'] == 1 and plasim['NDIAGCF'] == 1
    assert ex.cloud_water('earth_path', 1.6) == (9.80665, 1.6 / 9.80665) and ex.cloud_water('plasim', 1.6) == (0.0, 1.0)
    glow = _with(OPEN_MOON, forcing={'top_infrared_w_m2': {'day': 10.1718, 'night': 0.5165}})
    radmod = ex.namelists(MOON, glow, DESIGN, top=LATER, calibrations=_given())['radmod_namelist']
    assert (radmod['IRTOPDAY'], radmod['IRTOPNIGHT']) == (10.1718, 0.5165)


def test_an_eccentric_orbit_states_its_longitude_of_perihelion():
    planet = ex.namelists(MOON, OPEN_MOON, DESIGN, top=LATER, calibrations=_given())['planet_namelist']
    assert planet['MVELP'] == 102.7 and MOON['orbit']['perihelion_longitude_deg'] == 102.7   # Earth's, through its host
    plain = {k: v for k, v in EARTH['orbit'].items() if k != 'perihelion_longitude_deg'}
    with pytest.raises(SpecError, match='longitude of perihelion'):
        ex.perihelion_longitude({**EARTH, 'orbit': plain})
    assert ex.perihelion_longitude({**EARTH, 'orbit': {**plain, 'eccentricity': 0.0}}) is None
    with pytest.raises(SpecError, match='from 0 to 360'):
        ex.perihelion_longitude(_with(EARTH, orbit={'perihelion_longitude_deg': 360.0}))


@pytest.mark.parametrize('world, run, scenario, match', [
    (MOON, _with(DESIGN, switches={'twilight': 'curved'}), OPEN_MOON, 'switches.twilight'),
    (MOON, _with(DESIGN, switches={'sun_clock': 'solar'}), OPEN_MOON, 'switches.sun_clock'),
    (MOON, _with(DESIGN, switches={'cloud_water': 'wet'}), OPEN_MOON, 'switches.cloud_water'),
    (MOON, _with(DESIGN, switches={'top_infrared': 'from-glow'}), OPEN_MOON, 'glow producer'),
    (MOON, _with(DESIGN, switches={'surface_cloud_rcrit': 1.0}), OPEN_MOON, 'surface_cloud_rcrit'),
    (MOON, _with(DESIGN, switches={'convective_day_s': -1.0}), OPEN_MOON, 'convective_day_s'),
    (MOON, {**DESIGN, 'clear_sky': 1}, OPEN_MOON, 'clear_sky'),
    (MOON, {**DESIGN, 'seed': 1.5}, OPEN_MOON, 'seed'),
    (MOON, DESIGN, _with(OPEN_MOON, air={'reference_level': 'mean-radius'}), 'level its heights start from'),
    (MOON, DESIGN, _with(OPEN_MOON, air={'ozone': 'terluna:atmosphere/ozone.json'}), 'ozone'),
    (MOON, DESIGN, _with(OPEN_MOON, air={'water_vapour': 'none'}), 'prognostic'),
    (MOON, DESIGN, _with(OPEN_MOON, air={'co2_ppm': -1.0}), 'exceed the total'),   # the derivation refuses it first
    (MOON, DESIGN, _with(OPEN_MOON, water={'ocean': {'kind': 'dynamic', 'mixed_layer_m': 50.0, 'sea_ice': True}}),
     'slab'),
    (MOON, DESIGN, _with(OPEN_MOON, land={'albedo': 'unchosen'}), 'land.albedo'),
    (_with(SEED, rotation={'substellar_longitude_deg': None}), DESIGN, SEED_AIR, 'substellar_longitude_deg'),
    (_with(SEED, rotation={'locked_to': 'host'}), DESIGN, SEED_AIR, 'locked_to is "star"'),
    (_with(SEED, rotation={'obliquity_deg': 1.0}), DESIGN, SEED_AIR, 'obliquity 0 and eccentricity 0'),
    (_with(SEED, orbit={'eccentricity': 0.01, 'perihelion_longitude_deg': 0.0}), DESIGN, SEED_AIR,
     'obliquity 0 and eccentricity 0'),
])
def test_settings_the_adapter_cannot_write_are_refused(world, run, scenario, match):
    top = LATER if scenario is not SEED_AIR else ex.TopOfAir(1275.9, 1.0, 'scenario')
    calibrations = _given() if scenario is not SEED_AIR else _given(sunlight_scale=None)
    with pytest.raises(SpecError, match=match):
        ex.namelists(world, scenario, run, top=top, calibrations=calibrations)


@needs_sunlight
def test_the_sunlight_at_the_top_is_the_filtered_light_times_its_scale():
    first = ex.top_of_air(MOON, OPEN_MOON, ex.Calibrations.identity(), store=STORE)
    later = ex.top_of_air(MOON, OPEN_MOON, _given(), store=STORE)
    assert (first.scale, first.basis, later.scale, later.basis) == (1.0, 'identity', 0.97, 'calibration')
    assert first.w_m2 == first.sunlight['filtered_w_m2'] == pytest.approx(1236.12, abs=0.005)
    assert later.w_m2 == first.w_m2 * 0.97


def test_earths_control_keeps_the_released_models_day_ozone_and_surface():
    top = ex.TopOfAir(1361.0, 1.0, 'scenario')
    entries = ex.namelists(EARTH, CONTROL, DEFAULTS, top=top, calibrations=ex.Calibrations.identity())
    plasim, planet, radmod = entries['plasim_namelist'], entries['planet_namelist'], entries['radmod_namelist']
    assert (plasim['N_DAYS_PER_YEAR'], plasim['NSTPW'], plasim['N_RUN_STEPS'], plasim['PSURF']) == (365, 48, 17520, 101325.0)
    assert 'ROTSPD' not in planet and planet['GA'] == 9.80665 and planet['PLARAD'] == 6371000.0
    assert planet['SIDEREAL_YEAR'] == 365.25636 * 86400.0 and (planet['ECCEN'], planet['OBLIQ']) == (0.0167, 23.4393)
    assert radmod['NO3'] == 1 and radmod['CO2'] == 400.0
    assert entries['landmod_namelist'] == {'NWETSOIL': 0, 'DSOILZ': (0.4, 0.8, 1.6, 3.2, 6.4)}   # its albedo map stays
    m = sum(x * ex.MOLAR_MASS[gas] for gas, x in derive.mole_fractions(CONTROL).items())
    assert planet['GASCON'] == ex.GAS_CONSTANT / m == pytest.approx(287.04, abs=0.01)
    assert set(ex.departures(CONTROL)) == set(ex.DEPARTURES)
    assert set(ex.departures(_with(CONTROL, air={'co2_ppm': 0.0}))) == set(ex.DEPARTURES) | {ex.CO2_FREE[0]}


# Terluna's design run.

@needs_archive
@needs_terluna
@needs_sunlight
def test_the_design_runs_namelists_are_terlunas_but_for_five_entries_each_with_its_cause(tmp_path):
    calibrations = terluna_calibrations()
    top = ex.top_of_air(MOON, OPEN_MOON, calibrations, store=STORE)
    ex.write_namelists(tmp_path, ex.namelists(MOON, OPEN_MOON, DESIGN, top=top, calibrations=calibrations))
    found, lab_only, recorded = {}, {}, sorted((RECORDED / 'A28_corrected_970').glob('*_namelist'))
    assert len(recorded) == 7                          # Terluna recorded seven of the sixteen files
    for path in recorded:
        differ, mine, theirs = _compare(_entries((tmp_path / path.name).read_text()), _entries(path.read_text()))
        assert not theirs, (path.name, theirs)
        found.update({(path.name, k): v for k, v in differ.items()})
        lab_only.update({(path.name, k): v for k, v in mine.items()})
    # The entries the lab adds hold the values PlaSim and the patches take without them.
    assert lab_only == {('plasim_namelist', 'NDIAGGP'): '0', ('radmod_namelist', 'IRTOPDAY'): '0.0',
                        ('radmod_namelist', 'IRTOPNIGHT'): '0.0', ('radmod_namelist', 'NICEOPT'): '0',
                        ('radmod_namelist', 'NLWCORR'): '0'}
    assert set(found) == {('planet_namelist', k) for k in ('GA', 'PLARAD', 'ECCEN', 'GSOL0')} | \
        {('rainmod_namelist', 'CWSCALE')}
    lab, terluna = ({key: float(pair[i]) for key, pair in found.items()} for i in (0, 1))
    planet = lambda name: ('planet_namelist', name)
    # Gravity: the lab's has the spin term, Terluna's GM/R² (world_spec.md, the derived quantities).
    assert lab[planet('GA')] == derive.gravity(MOON) and terluna[planet('GA')] == derive.gravity(MOON, rule='gm-over-r2')
    # Cloud water: Earth's path at each world's own gravity (patch 02).
    for side in (lab, terluna):
        assert side[('rainmod_namelist', 'CWSCALE')] == pytest.approx(side[planet('GA')] / 9.80665, rel=1e-15)
    # The radius: Terluna's runner divided by 6,371,000 m where ExoPlaSim's unit is 6,371,220 m (rule 7).
    assert lab[planet('PLARAD')] == 1737400.0
    assert terluna[planet('PLARAD')] == pytest.approx(1737400.0 / 6371000.0 * 6371220.0, rel=1e-15)
    # The eccentricity: Earth's 0.0167, where Terluna's runner typed 0.016715 (world_spec.md, the Moon worked through).
    assert (lab[planet('ECCEN')], terluna[planet('ECCEN')]) == (0.0167, 0.016715)
    # The sunlight: the spectrum's tails pass at the shield's own transmission, 0.070% more (sunlight.py).
    assert terluna[planet('GSOL0')] == pytest.approx(1235.2508281698022 * 0.970, rel=1e-12)
    assert lab[planet('GSOL0')] / terluna[planet('GSOL0')] - 1.0 == pytest.approx(7.0e-4, abs=2e-5)


@needs_archive
@needs_terluna
@needs_sunlight
def test_the_longwave_and_ice_run_switches_on_what_terlunas_pair_switched_on(tmp_path):
    calibrations = terluna_calibrations()
    top = ex.top_of_air(MOON, OPEN_MOON, calibrations, store=STORE)
    for name, run in (('design', DESIGN), ('lw_ice', LW_ICE)):
        ex.write_namelists(tmp_path / name, ex.namelists(MOON, OPEN_MOON, run, top=top, calibrations=calibrations))
    pair = [_entries((tmp_path / name / 'radmod_namelist').read_text()) for name in ('design', 'lw_ice')]
    recorded = [_entries((RECORDED / folder / 'radmod_namelist').read_text())
                for folder in ('A28_corrected_970', 'A28_corrected_970_lw_ice')]
    changed = lambda a, b: {k: b[k] for k in b if a.get(k) != b[k]}
    assert changed(*pair) == changed(*recorded) == {'NLWCORR': '1', 'NICEOPT': '1', 'TICEOPT': '235.15'}


# ExoPlaSim's own configure.

CONFIGURE = r'''
import hashlib, json, os, sys, tempfile
import exoplasim
spec = json.loads(sys.argv[1])
out = []
for case in spec['cases']:
    with tempfile.TemporaryDirectory(prefix='worldlab-configure-') as folder:
        os.chdir(folder)
        for name in ('sun.dat', 'sun_hr.dat'):
            with open(name, 'w') as handle:
                handle.write(' Wavelength    Flux  \n0.5 1.0\n')
        model = exoplasim.Model(workdir='run', modelname='run', resolution=spec['resolution'], layers=spec['levels'],
                                ncpus=spec['ranks'], precision=spec['precision'])
        model.configure(**dict(case, starspec=os.path.join(folder, 'sun.dat')))
        files = {name: open(os.path.join('run', name)).read() for name in spec['namelists']}
        files['sra'] = {name: hashlib.sha256(open(os.path.join('run', name), 'rb').read()).hexdigest()
                        for name in sorted(os.listdir('run')) if name.endswith('.sra')}
        out.append(files)
        os.chdir('/')
print('worldlab-configure ' + json.dumps(out))
'''


@needs_env
@needs_archive
def test_configure_writes_the_labs_namelists_but_for_the_departures_and_the_labs_additions(tmp_path):
    other_moon = _with(OPEN_MOON, air={'ozone': 'model-default'}, land={'albedo': 'model-default'},
                       water={'ocean': {'kind': 'slab', 'mixed_layer_m': 20.0, 'sea_ice': False}})
    slow_free = {**_with(DESIGN, switches={'sun_clock': 'plasim'}), 'timestep_min': 45.0, 'fixed_orbit': False,
                 'whole_model_days': False, 'mean_interval_days': 10.0}
    cases = [(MOON, OPEN_MOON, DESIGN, FIRST),
             (EARTH, CONTROL, DEFAULTS, ex.TopOfAir(1361.0, 1.0, 'scenario')),
             (MOON, other_moon, slow_free, FIRST),
             (EARTH, _with(CONTROL, air={'co2_ppm': 0.0, 'ozone': 'none'}, land={'albedo': 0.3}),
              DEFAULTS, ex.TopOfAir(1361.0, 1.0, 'scenario')),
             (SEED, SEED_AIR, DEFAULTS, ex.TopOfAir(1275.9375, 1.0, 'scenario'))]
    arguments, written = [], []
    for i, (world, scenario, run, top) in enumerate(cases):
        arguments.append(ex.configure_arguments(world, scenario, run, top=top, starspec='sun.dat'))
        ex.write_namelists(tmp_path / str(i), ex.namelists(world, scenario, run, top=top,
                                                           calibrations=ex.Calibrations.identity()))
        written.append({name: (tmp_path / str(i) / name).read_text() for name in ex.NAMELISTS})
    spec = dict({k: DEFAULTS[k] for k in ('resolution', 'levels', 'ranks', 'precision')}, cases=arguments,
                namelists=list(ex.NAMELISTS))
    done = subprocess.run([PYTHON, '-c', CONFIGURE, json.dumps(spec)], capture_output=True, text=True, timeout=600)
    assert done.returncode == 0, done.stderr[-3000:]
    line = next(l for l in reversed(done.stdout.splitlines()) if l.startswith('worldlab-configure '))
    configured = json.loads(line.removeprefix('worldlab-configure '))
    for i, ((world, scenario, *_), lab_files, theirs) in enumerate(zip(cases, written, configured, strict=True)):
        found = set()
        for name in ex.NAMELISTS:
            differ, mine, only_configure = _compare(_entries(lab_files[name]), _entries(theirs[name]))
            assert not only_configure, (i, name, only_configure)
            assert {k.split('(')[0] for k in mine} <= set(ex.ADDITIONS.get(name, ())), (i, name, mine)
            found |= {(name, k) for k in differ}
        assert found == set(ex.departures(scenario)), (i, found)
        if world['surface']['geometry'] == 'model-default':            # configure leaves ExoPlaSim's own files
            ours = ex.model_surfaces(DEFAULTS['resolution'], albedo_map=scenario['land']['albedo'] == 'model-default')
            assert theirs['sra'] == {name: hashlib.sha256(data).hexdigest() for name, data in ours.items()}, i
        if world['surface']['geometry'] == 'ocean':                    # configure's aquaplanet removes every one
            assert theirs['sra'] == {}, i


# The input files.

DRIVE = root('terluna-drive')
DESIGN_INPUTS = DRIVE / 'gcm-runs' / 'A28_corrected_970' / 'inputs' if DRIVE is not None else None
needs_drive = pytest.mark.skipif(DESIGN_INPUTS is None or not DESIGN_INPUTS.is_dir(),
                                 reason="Terluna's research drive lacks the design run's inputs")


def _star(text: str) -> tuple[list, np.ndarray]:
    rows = [line.split() for line in text.splitlines()[1:]]
    return [r[0] for r in rows], np.array([float(r[1]) for r in rows])


@needs_archive
@needs_sunlight
def test_the_star_files_follow_exoplasims_own_converter():
    texts = ex.star_files(MOON, OPEN_MOON, store=STORE)
    coarse = np.loadtxt(io.BytesIO(ex.archive_files(('wvref.txt',))['wvref.txt']))
    spectrum, _ = sunlight.star_spectrum(MOON, store=STORE)
    shield = sunlight.scenario_filter(OPEN_MOON, store=STORE)
    for name, grid in (('sun.dat', coarse), ('sun_hr.dat', ex.FINE_GRID_UM)):
        assert texts[name].startswith(ex.STAR_HEADER)
        wavelengths, values = _star(texts[name])
        assert [float(w) for w in wavelengths] == list(grid) and len(grid) == {'sun.dat': 965, 'sun_hr.dat': 2048}[name]
        light = sunlight.through(spectrum, shield, grid * 1000.0)
        assert np.array_equal(values, np.interp(grid * 1000.0, light.wavelength_nm, light.irradiance) * 1000.0 / ex.SPEED_OF_LIGHT)


MINWAVEL_M = 316.036116751e-9          # PlaSim takes no light below this (radmod.f90:77, 222-224)
HC_K = 0.0143877735383                 # PlaSim's hc/k, m K (radmod.f90:173)


def _split(w_m: np.ndarray, f: np.ndarray) -> float:
    """PlaSim's share of the light below 0.75 µm: its trapezoids on each half of a 2048-point spectrum and the step
    between them (radmod.f90:274-296, 356-368)."""
    z1 = np.trapezoid(f[:1024], w_m[:1024]) + 0.5 * (f[1023] + f[1024]) * (w_m[1024] - w_m[1023])
    return float(z1 / (z1 + np.trapezoid(f[1024:], w_m[1024:])))


@needs_archive
@pytest.mark.parametrize('temperature', [5772.0, 3400.0])
def test_a_blackbody_stars_file_splits_its_light_as_plasims_own_planck(temperature):
    star = _with(EARTH, star={'spectrum': 'blackbody', 'temperature_k': temperature})
    w_um, f = (np.array(v, dtype=float) for v in _star(ex.star_files(star, CONTROL)['sun_hr.dat']))
    w = w_um * 1e-6
    lab = _split(w, np.where(w < MINWAVEL_M, 0.0, f))
    lwmin, hinge = np.log10(MINWAVEL_M), np.log10(7.5e-7)            # PlaSim's own grid (radmod.f90:197-208)
    grid = np.concatenate([10 ** (lwmin + np.arange(1024) * (hinge - lwmin) / 1024),
                           10 ** (hinge + np.arange(1024) * (-4 - hinge) / 1024)])
    plasim = _split(grid, (1e6 * grid) ** -5 / np.expm1(HC_K / (temperature * grid)))
    assert lab == pytest.approx(plasim, abs=1e-5)


@needs_archive
@needs_sunlight
@pytest.mark.parametrize('world, scenario', [(MOON, OPEN_MOON), (EARTH, CONTROL)])
def test_the_fine_file_holds_the_filtered_light_of_its_range(world, scenario):
    w_um, f = (np.array(v, dtype=float) for v in _star(ex.star_files(world, scenario, store=STORE)['sun_hr.dat']))
    spectrum, _ = sunlight.star_spectrum(world, store=STORE)
    light = sunlight.through(spectrum, sunlight.scenario_filter(scenario, store=STORE))
    # Its 2,048 points sample the measured spectrum's lines, which puts the trapezoids 0.45% above the light itself.
    assert np.trapezoid(f, w_um) * ex.SPEED_OF_LIGHT / light.light(200.0, 1e5) - 1.0 == pytest.approx(0.0045, abs=5e-4)


@needs_archive
@needs_sunlight
@needs_drive
def test_the_star_files_are_terlunas_in_the_measured_spectrum_and_differ_in_its_tails_by_their_cause():
    texts = ex.star_files(MOON, OPEN_MOON, store=STORE)
    for name, theirs in (('sun.dat', 'sun_titania_stack.dat'), ('sun_hr.dat', 'sun_titania_stack_hr.dat')):
        (lab_w, lab), (their_w, terluna) = _star(texts[name]), _star((DESIGN_INPUTS / theirs).read_text())
        assert lab_w == their_w                                   # the same wavelengths, as written
        w = np.array([float(x) for x in lab_w]) * 1000.0           # nm
        spectrum, (first, last) = sunlight.star_spectrum(MOON, store=STORE)
        tail_start = spectrum.wavelength_nm[np.searchsorted(spectrum.wavelength_nm, last, side='right')]
        measured = (w >= first) & (w <= last)                    # TSIS-1's own points, 202.0-2729.9 nm
        assert np.array_equal(lab[measured] == 0, terluna[measured] == 0)
        lit = measured & (terluna > 0)
        assert np.abs(lab[lit] / terluna[lit] - 1).max() < 1e-11
        # Past the measured spectrum the lab's tail holds the rest of the Sun's constant (sunlight.py), where Terluna's
        # runner matched the 5772 K blackbody to the last measured value, 11.45% brighter (exoplasim_run.py:954-963);
        # a point between the last measured value and the tail's first takes a share between the two.
        tail = (w >= tail_start) & (terluna > 0)
        ratio = lab[tail] / terluna[tail]
        assert ratio.max() - ratio.min() < 1e-7 and ratio.mean() == pytest.approx(0.89725, abs=1e-5)
        junction = (w > last) & (w < tail_start)
        assert np.all((lab[junction] / terluna[junction] > ratio.min()) & (lab[junction] / terluna[junction] < 1.0))
        assert not lab[w < first].any() and not terluna[w < first].any()   # the shield passes nothing there


def _terluna_surface(name: str) -> ModelSurface:
    from scipy.io import netcdf_file
    with netcdf_file(TERLUNA / 'climate' / 'gcm' / 'products' / name, 'r', mmap=False) as f:
        v = {k: np.array(x[:], dtype=float) for k, x in f.variables.items()}
    return ModelSurface(v['lat'], v['lon'], v['land_fraction'], v['land_elevation_m'], v['water_surface_m'],
                           v['ocean_depth_m'], v['cell_area_fraction'], {})


@needs_terluna
@needs_drive
def test_the_surface_files_written_from_terlunas_own_surface_are_terlunas_byte_for_byte():
    files, shares = ex.surface_files(_terluna_surface('moon_28pct_water_lakes_gaussian_T21.nc'),
                                     derive.gravity(MOON, rule='gm-over-r2'))           # Terluna's gravity, GM/R²
    assert files['N032_surf_0172.sra'] == (DESIGN_INPUTS / 'moon_landmask.sra').read_text()
    assert files['N032_surf_0129.sra'] == (DESIGN_INPUTS / 'moon_topography.sra').read_text()
    assert shares['mask_land_share'] == pytest.approx(0.5995, abs=5e-5)


def test_the_surface_files_follow_plasims_format_and_the_masks_rule():
    field = np.arange(16.0).reshape(2, 8) * 1000.0
    text = ex.sra(129, field).splitlines()
    assert text[0] == '       129         0  20090101         0         8         2         0         0'
    assert text[1].startswith('     0.000  1000.000  2000.000') and len(text) == 3
    assert ex.sra(129, np.array([[-9999.999, 99999.999]])).splitlines()[1] == ' -9999.999 99999.999'
    for bad in (1e5, 99999.9996, -10000.0, float('nan'), float('inf')):
        with pytest.raises(SpecError, match='blank before its digits'):
            ex.sra(129, np.full((1, 8), bad))
    square = ModelSurface(None, None, *(np.ones((32, 32)),) * 3, None, np.ones((32, 32)), {})
    with pytest.raises(SpecError, match='Gaussian grid of 32 latitudes'):
        ex.surface_files(square, 1.6)
    land = np.array([[0.9, 0.1], [0.4, 0.6]])
    area = np.array([[1.0, 1.0], [2.0, 2.0]])
    mask = ex.land_mask(land, area, 1.0 - float((land * area).sum() / area.sum()))   # 50% water
    assert mask.tolist() == [[1.0, 0.0], [0.0, 1.0]]                                 # the two least-land cells, 3/6


@needs_terluna
def test_the_curved_air_and_longwave_tables_are_terlunas_byte_for_byte():
    calibrations = terluna_calibrations()
    assert ex.twilight_table(calibrations.ledger, 10) == (RECORDED / 'A28_corrected_970' / 'twilight.dat').read_text()
    assert ex.longwave_table(calibrations.longwave, 10) == \
        (RECORDED / 'A28_corrected_970_lw_ice' / 'lwcorr.dat').read_text()
    with pytest.raises(SpecError, match='layers'):
        ex.twilight_table(calibrations.ledger, 11)
    with pytest.raises(SpecError, match='values a row'):
        ex.longwave_table(calibrations.longwave, 9)


@needs_archive
@needs_sunlight
def test_earths_control_keeps_exoplasims_own_surface_files(tmp_path):
    record = ex.write_run(tmp_path, EARTH, CONTROL, DEFAULTS, calibrations=ex.Calibrations.identity(), store=STORE)
    surfaces = sorted(p.name for p in tmp_path.glob('*.sra'))
    assert len(surfaces) == 15 and 'N032_surf_0174.sra' in surfaces and record['surface']['kind'] == 'model-default'
    assert set(record['files']) == set(ex.NAMELISTS) | {'sun.dat', 'sun_hr.dat'} | set(surfaces)
    assert record['sunlight'] == dict(top_w_m2=pytest.approx(1361.0, rel=1e-9), scale=1.0, basis='scenario')
    assert not (tmp_path / 'twilight.dat').exists() and record['switches']['twilight'] == 'none'
    whitened = _with(CONTROL, land={'albedo': 0.3})
    ex.write_run(tmp_path / 'albedo', EARTH, whitened, DEFAULTS, calibrations=ex.Calibrations.identity(), store=STORE)
    assert 'N032_surf_0174.sra' not in {p.name for p in (tmp_path / 'albedo').glob('*.sra')}   # as configure removes it


@needs_archive
def test_a_run_needs_the_surface_its_world_names(tmp_path):
    surface = ModelSurface(None, None, np.ones((32, 64)), np.zeros((32, 64)), np.zeros((32, 64)), None,
                           np.ones((32, 64)), {})
    with pytest.raises(SpecError, match="keeps ExoPlaSim's own surface"):
        ex.write_run(tmp_path / 'a', EARTH, CONTROL, DEFAULTS, calibrations=ex.Calibrations.identity(), surface=surface)
    with pytest.raises(SpecError, match="seas of the model's own"):
        ex.write_run(tmp_path / 'a', EARTH, _with(CONTROL, water={'seas': 'from-heights'}), DEFAULTS,
                     calibrations=ex.Calibrations.identity())
    small = ModelSurface(None, None, np.ones((64, 128)), None, None, None, np.ones((64, 128)), {})
    for given in (None, small):
        with pytest.raises(SpecError, match='grid of 32 latitudes'):
            ex.write_run(tmp_path / 'a', MOON, OPEN_MOON, DESIGN, calibrations=ex.Calibrations.identity(),
                         surface=given)
    with pytest.raises(SpecError, match='heights start at the water level'):
        ex.write_run(tmp_path / 'a', MOON, _with(OPEN_MOON, air={'reference_level': 'sea'}), DESIGN,
                     calibrations=ex.Calibrations.identity(), surface=surface)
    with pytest.raises(SpecError, match='surface.geometry'):
        ex.write_run(tmp_path / 'a', _with(MOON, surface={'geometry': 'unchosen'}), OPEN_MOON, DESIGN,
                     calibrations=ex.Calibrations.identity(), surface=surface)
    with pytest.raises(SpecError, match='all ocean takes no surface'):
        ex.write_run(tmp_path / 'a', SEED, SEED_AIR, DEFAULTS, calibrations=ex.Calibrations.identity(), surface=surface)
    (tmp_path / 'full').mkdir()
    (tmp_path / 'full' / 'N032_surf_0169.sra').write_text('an earlier run\n')
    with pytest.raises(SpecError, match='new or empty folder'):
        ex.write_run(tmp_path / 'full', EARTH, CONTROL, DEFAULTS, calibrations=ex.Calibrations.identity())
    assert sorted(p.name for p in tmp_path.iterdir()) == ['full']      # a refused run leaves nothing behind


@needs_archive
@needs_terluna
@needs_sunlight
def test_the_longwave_and_ice_run_writes_terlunas_tables_and_mask(tmp_path):
    surface = _terluna_surface('moon_28pct_water_lakes_gaussian_T21.nc')
    record = ex.write_run(tmp_path / 'run', MOON, OPEN_MOON, LW_ICE, calibrations=terluna_calibrations(),
                          surface=surface, store=STORE)
    run = tmp_path / 'run'
    assert (run / 'twilight.dat').read_text() == (RECORDED / 'A28_corrected_970' / 'twilight.dat').read_text()
    assert (run / 'lwcorr.dat').read_text() == (RECORDED / 'A28_corrected_970_lw_ice' / 'lwcorr.dat').read_text()
    assert set(record['files']) == set(ex.NAMELISTS) | {'sun.dat', 'sun_hr.dat', 'twilight.dat', 'lwcorr.dat',
                                                        'N032_surf_0172.sra', 'N032_surf_0129.sra'}
    assert record['switches']['ice_weights'] == 'patch-10' and record['sunlight']['basis'] == 'calibration'
    if DESIGN_INPUTS is not None and DESIGN_INPUTS.is_dir():
        assert (run / 'N032_surf_0172.sra').read_text() == (DESIGN_INPUTS / 'moon_landmask.sra').read_text()


# The seed waterworld: all ocean, locked to a red dwarf.

@needs_archive
def test_the_seed_waterworld_runs_all_ocean_under_a_fixed_star(tmp_path):
    record = ex.write_run(tmp_path / 'run', SEED, SEED_AIR, DEFAULTS, calibrations=ex.Calibrations.identity())
    run = tmp_path / 'run'
    assert {p.name for p in run.iterdir()} == set(ex.NAMELISTS) | {'sun.dat', 'sun_hr.dat'}   # no surface files
    assert record['surface'] == {'kind': 'ocean', 'mask_land_share': 0.0}
    assert record['sunlight'] == dict(top_w_m2=pytest.approx(32.664 / 0.16 ** 2, rel=1e-9), scale=1.0, basis='scenario')
    assert record['switches']['sun_clock'] == 'plasim'           # patch 04's synodic clock replaces the fixed hour angle
    plasim, planet, radmod = (_entries((run / name).read_text())
                              for name in ('plasim_namelist', 'planet_namelist', 'radmod_namelist'))
    year = derive.year_days(SEED)
    assert (plasim['NAQUA'], plasim['FIXEDLON'], radmod['NFIXED'], radmod['NSUNCLOCK']) == ('1', '180.0', '1', '0')
    assert float(planet['ROTSPD']) == 1.0 / year and float(planet['SIDEREAL_YEAR']) == year * 86400.0
    assert (planet['ECCEN'], planet['OBLIQ'], planet['MVELP']) == ('0.0', '0.0', '102.7')   # the template's, idle
    assert float(planet['GA']) == derive.gravity(SEED) and (plasim['N_DAYS_PER_YEAR'], plasim['N_RUN_STEPS']) == \
        ('12', str(12 * derive.calendar(SEED, DEFAULTS)['steps_per_model_day']))
    w_um, f = (np.array(v, dtype=float) for v in _star((run / 'sun_hr.dat').read_text()))
    w = w_um * 1e-6
    lwmin, hinge = np.log10(MINWAVEL_M), np.log10(7.5e-7)
    grid = np.concatenate([10 ** (lwmin + np.arange(1024) * (hinge - lwmin) / 1024),
                           10 ** (hinge + np.arange(1024) * (-4 - hinge) / 1024)])
    assert _split(w, np.where(w < MINWAVEL_M, 0.0, f)) == \
        pytest.approx(_split(grid, (1e6 * grid) ** -5 / np.expm1(HC_K / (3400.0 * grid))), abs=1e-5)
