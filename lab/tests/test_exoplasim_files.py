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

from atmosphere.rain import fall_law
from climate.gcm import levels
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


def _rain(**changes) -> ex.RainDrops:
    """The rain's drops with every value patch 14 reads: the Open Moon's entries as Terluna's patch set them, and for
    the fall law the closed forms of Morrison's own power law at Earth's gravity, a table made without the solver."""
    first, last, points = fall_law.TABLE_LAMBDA
    moments = np.log(fall_law.closed_forms(841.99667, 0.8, fall_law.table_lambda()))
    table = dict(points=points, ln_lambda_first=math.log(first), ln_lambda_step=math.log(last / first) / (points - 1),
                 ln_mass_weighted=[float(x) for x in moments[0]], ln_number_weighted=[float(x) for x in moments[1]],
                 ln_ventilation=[float(x) for x in moments[2]])
    values = dict(table=table, self_collection_m3_kg_s=2.919, density_exponent=0.687, birth_rule='share',
                  new_rain_m=0.439e-3, melted_rain_m=2.95e-3)
    return ex.RainDrops(**{**values, **changes})


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

def test_the_switches_resolve_to_what_the_build_does():
    assert ex.series(DESIGN)[10:] == ('11-ice-weights.patch', ex.PATCH_12, ex.PATCH_13, ex.PATCH_14)
    assert len(ex.series(DESIGN)) == 14
    first, later = ex.resolve(DESIGN, ex.Calibrations.identity()), ex.resolve(LW_ICE, _given())
    assert (first['twilight'], first['gas_bands'], first['ice_weights']) == ('none', False, 'from-spectrum')
    assert (later['twilight'], later['gas_bands'], later['ice_weights'], later['ice_optics']) == \
        ('full', True, 'from-spectrum', True)
    deployed = {**DESIGN, 'patches': list(ex.series(DESIGN))[:10]}      # Terluna's ten patches, before patch 11
    assert ex.resolve(deployed, _given())['ice_weights'] == 'patch-10'
    assert ex.resolve(_with(DESIGN, switches={'ice_weights': 'patch-10'}), _given())['ice_weights'] == 'patch-10'
    with pytest.raises(SpecError, match='ice_weights'):
        ex.resolve(_with(DESIGN, switches={'ice_weights': 'measured'}), _given())
    # The surface gust: the released model's transfer by default, on any point of the series; a gust whose patches
    # the series lacks is refused.
    assert first['surface_gust'] == later['surface_gust'] == ex.resolve(deployed, _given())['surface_gust'] == 'none'
    gusty = _with(DESIGN, switches={'surface_gust': 'beljaars_similarity'})
    assert ex.resolve(gusty, _given())['surface_gust'] == 'beljaars_similarity'
    twelve = {**gusty, 'patches': list(ex.series(DESIGN))[:12]}         # the gust's patch without the similarity's
    assert ex.resolve(_with(twelve, switches={'surface_gust': 'beljaars'}), _given())['surface_gust'] == 'beljaars'
    for run, lacking in ((twelve, ex.PATCH_13),
                         ({**gusty, 'patches': deployed['patches']}, f'{ex.PATCH_12} and {ex.PATCH_13}')):
        with pytest.raises(SpecError, match=f"takes {re.escape(lacking)}, which the run's series lacks"):
            ex.resolve(run, _given())
    with pytest.raises(SpecError, match='surface_gust'):
        ex.resolve(_with(DESIGN, switches={'surface_gust': 'coare'}), _given())
    # The rain's evaporation: PlaSim's constant by default, on any point of the series; the drops' sizes on a series
    # that lacks patch 14 are refused.
    assert first['rain_evaporation'] == later['rain_evaporation'] == 'gamma'
    assert ex.resolve(deployed, _given())['rain_evaporation'] == 'gamma'
    sized = _with(DESIGN, switches={'rain_evaporation': 'drop_sizes'})
    assert ex.resolve(sized, _given())['rain_evaporation'] == 'drop_sizes'
    with pytest.raises(SpecError, match=f"takes {re.escape(ex.PATCH_14)}, which the run's series lacks"):
        ex.resolve({**sized, 'patches': list(ex.series(DESIGN))[:13]}, _given())
    with pytest.raises(SpecError, match='rain_evaporation'):
        ex.resolve(_with(DESIGN, switches={'rain_evaporation': 'kessler'}), _given())


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
    lit = ex.TopOfAir(1199.0, 0.97, 'calibration', {'ice_weights': (0.6, 0.2, 0.15, 0.05)})
    entries = ex.namelists(MOON, OPEN_MOON, switched, top=lit, calibrations=calibrations)
    rain, radmod, plasim = entries['rainmod_namelist'], entries['radmod_namelist'], entries['plasim_namelist']
    assert rain == {'CWGREF': 9.80665, 'CWSCALE': 1.0, 'CONVDAY': 0.0, 'RCRIT(10)': 0.9, 'NEVAPPREC': 1}
    assert (radmod['NSUNCLOCK'], radmod['NLWCORR'], radmod['NICEOPT'], radmod['TICEOPT']) == (0, 1, 1, 235.15)
    assert [radmod[f'ZICEW({i})'] for i in (1, 2, 3, 4)] == [0.6, 0.2, 0.15, 0.05]     # patch 11's weights
    with pytest.raises(SpecError, match='ice weights of the sunlight'):
        ex.namelists(MOON, OPEN_MOON, switched, top=LATER, calibrations=calibrations)
    deployed = {**switched, 'patches': list(ex.series(switched))[:10]}
    assert 'ZICEW(1)' not in ex.namelists(MOON, OPEN_MOON, deployed, top=LATER, calibrations=calibrations)['radmod_namelist']
    assert plasim['NDIAGGP'] == 1 and plasim['NDIAGCF'] == 1
    assert ex.cloud_water('earth_path', 1.6) == (9.80665, 1.6 / 9.80665) and ex.cloud_water('plasim', 1.6) == (0.0, 1.0)
    glow = _with(OPEN_MOON, forcing={'top_infrared_w_m2': {'day': 10.1718, 'night': 0.5165}})
    radmod = ex.namelists(MOON, glow, DESIGN, top=LATER, calibrations=_given())['radmod_namelist']
    assert (radmod['IRTOPDAY'], radmod['IRTOPNIGHT']) == (10.1718, 0.5165)


def test_the_surface_gust_sets_the_switches_of_the_patches_the_series_holds():
    """Patches 12 and 13: NGUST and NSIMW in fluxmod's namelist, each written where the run's series holds its patch,
    so that a build at an earlier point reads a namelist of the names it knows."""
    fluxmod = lambda run: ex.namelists(MOON, OPEN_MOON, run, top=LATER, calibrations=_given()).get('fluxmod_namelist')
    setting = lambda choice, patches=None: _with({**DESIGN, 'patches': patches or DESIGN['patches']},
                                                 switches={'surface_gust': choice})
    assert DEFAULTS['switches']['surface_gust'] == 'none' and fluxmod(DESIGN) == {'NGUST': 0, 'NSIMW': 0}
    assert fluxmod(setting('beljaars')) == {'NGUST': 1, 'NSIMW': 0}
    assert fluxmod(setting('beljaars_similarity')) == {'NGUST': 1, 'NSIMW': 1}
    twelve, eleven = (list(ex.series(DESIGN))[:n] for n in (12, 11))
    assert fluxmod(setting('none', twelve)) == {'NGUST': 0} and fluxmod(setting('beljaars', twelve)) == {'NGUST': 1}
    assert fluxmod(setting('none', eleven)) is None
    for choice, patches in (('beljaars_similarity', twelve), ('beljaars', eleven)):
        with pytest.raises(SpecError, match="which the run's series lacks"):
            fluxmod(setting(choice, patches))


@needs_archive
def test_the_surface_gusts_switches_are_written_into_fluxmods_namelist():
    run = _with(DESIGN, switches={'surface_gust': 'beljaars_similarity'})
    entries = ex.namelists(MOON, OPEN_MOON, run, top=LATER, calibrations=_given())
    assert ex.namelist_texts(entries)['fluxmod_namelist'] == ' &fluxmod_nl\n NGUST = 1\n NSIMW = 1\n /END\n'


def test_the_rains_evaporation_sets_its_entries_where_the_series_holds_patch_14():
    """Patch 14: NEVAPPREC in rainmod's namelist where the run's series holds the patch, PlaSim's own 1 by default, so
    that a build at an earlier point reads a namelist of the names it knows. With the drops' sizes it is 2, beside the
    six entries the patch reads: the birth rule and the two birth sizes from their calibration, and the
    self-collection rate, the density exponent and the step."""
    rainmod = lambda run, cal=None: ex.namelists(MOON, OPEN_MOON, run, top=LATER,
                                                 calibrations=cal or _given())['rainmod_namelist']
    assert DEFAULTS['switches']['rain_evaporation'] == 'gamma' and rainmod(DESIGN)['NEVAPPREC'] == 1
    thirteen = {**DESIGN, 'patches': list(ex.series(DESIGN))[:13]}
    assert 'NEVAPPREC' not in rainmod(thirteen)
    sized = _with(DESIGN, switches={'rain_evaporation': 'drop_sizes'})
    names = ('NEVAPPREC', 'NRDROP_JOIN', 'RDROP_WARM', 'RDROP_MELT', 'RDROP_KSC', 'RDROP_RHOEXP', 'RDROP_STEP')
    entries = rainmod(sized, _given(rain_drops=_rain()))
    assert {name: entries[name] for name in names} == dict(
        NEVAPPREC=2, NRDROP_JOIN=2, RDROP_WARM=0.439e-3, RDROP_MELT=2.95e-3, RDROP_KSC=2.919, RDROP_RHOEXP=0.687,
        RDROP_STEP=1000.0)
    assert set(names) <= set(ex.ADDITIONS['rainmod_namelist'])
    for rule, value in (('one_size', 0), ('join', 1), ('share', 2)):
        assert rainmod(sized, _given(rain_drops=_rain(birth_rule=rule, step_m=250.0)))['NRDROP_JOIN'] == value
    assert rainmod(sized, _given(rain_drops=_rain(step_m=250.0)))['RDROP_STEP'] == 250.0
    # The drops' sizes take their calibration, which a first run lacks, and patch 14.
    with pytest.raises(SpecError, match='rain_drops'):
        rainmod(sized)
    with pytest.raises(SpecError, match="first run evaporates its rain by PlaSim's constant"):
        ex.namelists(MOON, OPEN_MOON, sized, top=FIRST, calibrations=ex.Calibrations.identity())
    with pytest.raises(SpecError, match="which the run's series lacks"):
        rainmod({**sized, 'patches': thirteen['patches']}, _given(rain_drops=_rain()))
    for change, match in ((dict(birth_rule='largest'), 'birth rule'), (dict(new_rain_m=0.0), 'new_rain_m'),
                          (dict(melted_rain_m=-1.0e-3), 'melted_rain_m'), (dict(step_m=0.0), 'step_m'),
                          (dict(self_collection_m3_kg_s=-1.0), 'self_collection_m3_kg_s'),
                          (dict(density_exponent=float('nan')), 'density_exponent')):
        with pytest.raises(SpecError, match=match):
            _rain(**change)
    # What python/climate/gcm/rain_drops.settings gives for a world becomes the record the adapter reads.
    found = dict(namelist=dict(rdrop_ksc=5.78, rdrop_rhoexp=0.0, rdrop_step=500.0), table=_rain().table,
                 births=dict(rule='join', new_rain_m=0.4e-3, melted_rain_m=0.8e-3))
    assert ex.RainDrops.from_settings(found) == _rain(self_collection_m3_kg_s=5.78, density_exponent=0.0,
                                                      birth_rule='join', new_rain_m=0.4e-3, melted_rain_m=0.8e-3,
                                                      step_m=500.0)


def test_the_rains_table_is_the_text_cm1_reads_and_a_table_the_model_would_stop_on_is_refused():
    rain, g = _rain(), derive.gravity(MOON)
    text = ex.rain_table(rain, g)
    assert text == fall_law.table_text(rain.table) and ex.RAIN_TABLE == fall_law.TABLE_FILE
    lines = text.splitlines()
    assert lines[0].split()[0] == '301' and len(lines) == 302 and all(len(line.split()) == 3 for line in lines)
    table = rain.table
    falling = [-6.0 * (table['ln_lambda_first'] + i * table['ln_lambda_step']) for i in range(table['points'])]
    for change, match in (({'ln_ventilation': table['ln_ventilation'][:-1]}, 'states 301 rows'),
                          ({'points': 300}, 'states 300 rows'),
                          ({'ln_mass_weighted': [float('nan')] + table['ln_mass_weighted'][1:]}, 'finite numbers'),
                          ({'ln_lambda_step': 0.0}, 'positive step'),
                          ({'ln_number_weighted': falling}, 'fails to rise with lambda')):
        with pytest.raises(SpecError, match=match):
            ex.rain_table(_rain(table={**table, **change}), g)
    with pytest.raises(SpecError, match='three rows of logs'):
        ex.rain_table(_rain(table={k: v for k, v in table.items() if k != 'ln_ventilation'}), g)


@needs_archive
@needs_sunlight
def test_a_run_with_the_drops_sizes_holds_its_entries_and_the_rains_table(tmp_path):
    """Earth's control with its calibrations at the released model's values and the rain's drops given: the run's
    folder gains the table and rainmod's namelist the seven entries, and with PlaSim's constant the folder holds
    no table."""
    plain = _with(DEFAULTS, switches={'twilight': 'none', 'gas_bands': False})
    released = dict(rayleigh_scale=1.0, water_absorption_scale=1.0, water_continuum=ex.PLASIM_TH2OC)
    record = ex.write_run(tmp_path / 'sized', EARTH, CONTROL, _with(plain, switches={'rain_evaporation': 'drop_sizes'}),
                          calibrations=ex.Calibrations(**released, rain_drops=_rain()), store=STORE)
    assert record['switches']['rain_evaporation'] == 'drop_sizes' and ex.RAIN_TABLE in record['files']
    assert (tmp_path / 'sized' / ex.RAIN_TABLE).read_text() == fall_law.table_text(_rain().table)
    lines = (tmp_path / 'sized' / 'rainmod_namelist').read_text().splitlines()
    assert lines[-8:] == [' NEVAPPREC = 2', ' NRDROP_JOIN = 2', ' RDROP_WARM = 0.000439', ' RDROP_MELT = 0.00295',
                          ' RDROP_KSC = 2.919', ' RDROP_RHOEXP = 0.687', ' RDROP_STEP = 1000.0', ' /END']
    record = ex.write_run(tmp_path / 'gamma', EARTH, CONTROL, plain, calibrations=ex.Calibrations(**released),
                          store=STORE)
    assert record['switches']['rain_evaporation'] == 'gamma' and not (tmp_path / 'gamma' / ex.RAIN_TABLE).exists()
    assert ' NEVAPPREC = 1' in (tmp_path / 'gamma' / 'rainmod_namelist').read_text().splitlines()
    assert {p.name for p in (tmp_path / 'sized').iterdir()} - {p.name for p in (tmp_path / 'gamma').iterdir()} == \
        {ex.RAIN_TABLE}


# The level set.

# Terluna's values for the Open Moon as a study's table states them, and the run that takes them.
OPEN_MOON_LEVELS = {**levels.TERLUNA_OPEN_MOON_LEVELS,
                    'interfaces_m': list(levels.TERLUNA_OPEN_MOON_LEVELS['interfaces_m'])}
FIFTEEN = {**DESIGN, 'levels': OPEN_MOON_LEVELS}
# The two entries as the plasim_namelist of Terluna's fifteen-level runs states them
# (gcm-runs/A28R_301k_cold_sbm_rh07_deep200_l15cap/model on Terluna's drive, read on 2026-11-11).
TERLUNA_TFRC = '1728000.0,8640000.0,' + ','.join(['0.0'] * 13)
TERLUNA_SIGH = ('0.07660000000000002,0.16160000000000002,0.2601,0.3736000000000001,0.5,0.6335999999999999,0.7379,'
                '0.7981,0.8382,0.8717,0.9066,0.941,0.9666000000000001,0.9883,1.0')


def _laid(half, layers: int, **changes) -> ex.Calibrations:
    """`_given`'s calibrations with the ledger and a longwave correction of `layers` layers, laid on `half`."""
    ledger = ex.Ledger(elevation_deg=(0.0, 5.0), ground=(0.0, 0.1), layers=((0.0, 0.2),) * layers,
                       escape_w_m2=(0.5,) * (layers + 1), escape_temperature_k=(250.0,) * (layers + 1),
                       slant=(0.1, 0.2, 0.3), slant_air=(0.4, 0.5, 0.6), half_levels=half)
    longwave = ex.Longwave((0.0,) * (layers + 1), (1.0,) * (layers + 1), (250.0,) * (layers + 1), half)
    return _given(**{'ledger': ledger, 'longwave': longwave, **changes})


def test_the_released_models_own_levels_add_nothing_to_the_namelists():
    """The identity default: a run that keeps the released model's levels states configure's NEQSIG 0 and neither
    half levels nor friction, so that PlaSim computes its levels and presets its friction as released."""
    assert DEFAULTS['levels'] == 10 and derive.level_count(DEFAULTS) == 10
    released = derive.levels(DEFAULTS)
    assert released == dict(count=10, half_levels=tuple(float(x) for x in levels.plasim_half(10)), basis='released')
    assert ex.level_entries(released, DEFAULTS, 'a run') == {}
    for world, scenario, run, top, calibrations in ((EARTH, CONTROL, DEFAULTS, ex.TopOfAir(1361.0, 1.0, 'scenario'),
                                                     ex.Calibrations.identity()),
                                                    (MOON, OPEN_MOON, DESIGN, FIRST, ex.Calibrations.identity()),
                                                    (MOON, OPEN_MOON, DESIGN, LATER, _laid(None, 10))):
        plasim = ex.namelists(world, scenario, run, top=top, calibrations=calibrations)['plasim_namelist']
        assert plasim['NEQSIG'] == 0 and 'SIGH' not in plasim and 'TFRC' not in plasim
        assert ex.departures(scenario, run) == ex.departures(scenario)
    assert derive.levels({**DEFAULTS, 'levels': 5})['half_levels'] == tuple(float(x) for x in levels.plasim_half(5))


def test_a_generated_set_states_its_half_levels_and_the_top_friction_and_changes_nothing_else():
    """The Open Moon's design run on Terluna's values for its fifteen levels: plasim_namelist gains NEQSIG -1, SIGH and
    TFRC, and every other entry of every namelist stays as on the released ten."""
    ten = ex.namelists(MOON, OPEN_MOON, DESIGN, top=LATER, calibrations=_given())
    fifteen = ex.namelists(MOON, OPEN_MOON, FIFTEEN, top=LATER, calibrations=_given())
    half = levels.generate(51000.0, OPEN_MOON_LEVELS['interfaces_m'], 6)
    assert set(ten) == set(fifteen) and {name for name in ten if ten[name] != fifteen[name]} == {'plasim_namelist'}
    plasim = fifteen['plasim_namelist']
    assert {k: v for k, v in plasim.items() if ten['plasim_namelist'].get(k) != v} == dict(
        NEQSIG=-1, SIGH=tuple(float(x) for x in half), TFRC=(1728000.0, 8640000.0) + (0.0,) * 13)
    assert set(ten['plasim_namelist']) == set(plasim) - {'SIGH', 'TFRC'}
    assert {'SIGH', 'TFRC'} <= set(ex.ADDITIONS['plasim_namelist'])
    assert set(ex.departures(OPEN_MOON, FIFTEEN)) - set(ex.departures(OPEN_MOON)) == {('plasim_namelist', 'NEQSIG')}
    # As written: Terluna's friction to the character, and its half levels but for the last bit of two, 0.3736 and
    # 0.9666, where the lab keeps the compiled model's doubles (python/climate/gcm/levels.py, plasim_half).
    assert ex.text(plasim['TFRC']) == TERLUNA_TFRC and ex.text(plasim['NEQSIG']) == '-1'
    ours, theirs = ex.text(plasim['SIGH']).split(','), TERLUNA_SIGH.split(',')
    assert [(a, b) for a, b in zip(ours, theirs, strict=True) if a != b] == [
        ('0.37360000000000004', '0.3736000000000001'), ('0.9666', '0.9666000000000001')]
    # The lowest layer's cloud threshold follows the set's count.
    cloudy = _with(FIFTEEN, switches={'surface_cloud_rcrit': 0.9})
    rainmod = ex.namelists(MOON, OPEN_MOON, cloudy, top=LATER, calibrations=_given())['rainmod_namelist']
    assert rainmod['RCRIT(15)'] == 0.9 and 'RCRIT(10)' not in rainmod
    # The record of the set: its count, its half levels and what generated them.
    found = derive.levels(FIFTEEN, MOON, OPEN_MOON)
    assert found == dict(count=15, half_levels=tuple(float(x) for x in half), basis='generated',
                         scale_height_m=51000.0, scale_height_basis='stated', upper=6,
                         interfaces_m=tuple(OPEN_MOON_LEVELS['interfaces_m']))
    assert derive.level_count(FIFTEEN) == 15 and derive.levels(FIFTEEN) == found      # a stated height needs no world


@needs_archive
def test_a_generated_sets_entries_are_written_into_plasims_namelist():
    entries = ex.namelists(MOON, OPEN_MOON, FIFTEEN, top=LATER, calibrations=_given())
    lines = ex.namelist_texts(entries)['plasim_namelist'].splitlines()
    assert ' NEQSIG = -1' in lines and lines[-3:] == [
        ' SIGH = 0.07660000000000002,0.16160000000000002,0.2601,0.37360000000000004,0.5,0.6335999999999999,0.7379,'
        '0.7981,0.8382,0.8717,0.9066,0.941,0.9666,0.9883,1.0', f' TFRC = {TERLUNA_TFRC}', ' /END']
    assert len([line for line in lines if line.split()[0] in ('NEQSIG', 'SIGH', 'TFRC')]) == 3


def test_a_set_counted_at_the_scenarios_scale_height_follows_its_reference_temperature():
    """With "scenario" the heights are counted at the scenario's own scale height: 52.4 km for the Open Moon at 295 K,
    where 600 m stands at exp(-600/52,377) = 0.98861, 0.9886 to four places, against 0.9883 at Terluna's 51 km."""
    run = {**DESIGN, 'levels': {**OPEN_MOON_LEVELS, 'scale_height_m': 'scenario'}}
    found = derive.levels(run, MOON, OPEN_MOON)
    scale_height = derive.planet(MOON, OPEN_MOON)['scale_height_m']
    assert found['scale_height_m'] == scale_height == pytest.approx(52377.0, abs=0.5)
    assert (found['scale_height_basis'], found['count'], found['half_levels'][13]) == ('scenario', 15, 0.9886)
    by_hand = levels.generate(scale_height, OPEN_MOON_LEVELS['interfaces_m'], 6)
    assert found['half_levels'] == tuple(float(x) for x in by_hand)
    assert math.exp(-600.0 / scale_height) == pytest.approx(0.98861, abs=5e-6)
    plasim = ex.namelists(MOON, OPEN_MOON, run, top=LATER, calibrations=_given())['plasim_namelist']
    assert plasim['SIGH'] == found['half_levels'] and plasim['NEQSIG'] == -1
    # A scenario whose reference temperature the fixpoint is still to find gives no scale height, and neither does a
    # run alone.
    with pytest.raises(SpecError, match='settled global mean'):
        derive.levels(run, LIB.world('mars'), LIB.scenario('mars/breathable-1bar'))
    with pytest.raises(SpecError, match='takes the world and its scenario'):
        derive.levels(run)


@pytest.mark.parametrize('change, match', [
    ({'levels': 0}, "released model's count"), ({'levels': True}, "released model's count"),
    ({'levels': 10.0}, "released model's count"), ({'levels': '10'}, "released model's count"),
    ({'levels': {}}, 'a generated level set states'),
    ({'levels': {**OPEN_MOON_LEVELS, 'lowest_m': 300.0}}, 'a generated level set states'),
    ({'levels': {k: v for k, v in OPEN_MOON_LEVELS.items() if k != 'scale_height_m'}}, 'a generated level set states'),
    ({'levels': {**OPEN_MOON_LEVELS, 'upper': 6.0}}, 'a generated level set states'),
    ({'levels': {**OPEN_MOON_LEVELS, 'interfaces_m': 600.0}}, 'a generated level set states'),
    ({'levels': {**OPEN_MOON_LEVELS, 'interfaces_m': []}}, 'a generated level set states'),
    ({'levels': {**OPEN_MOON_LEVELS, 'upper': 1}}, 'keeps from 2 to 9'),
    ({'levels': {**OPEN_MOON_LEVELS, 'upper': 7}}, 'at or above'),          # 15.5 km stands above the seventh, 0.7651
    ({'levels': {**OPEN_MOON_LEVELS, 'scale_height_m': 'world'}}, 'scale height is a positive number'),
    ({'levels': {**OPEN_MOON_LEVELS, 'scale_height_m': 8430.0}}, 'at or above'),         # the Moon's heights on Earth
    ({'levels': {**OPEN_MOON_LEVELS, 'interfaces_m': [600.0, 3100.0]}}, 'from the highest down'),
    # PlaSim's presets by truncation and count: at T42 for ten levels, at T21 for five.
    ({'levels': OPEN_MOON_LEVELS, 'resolution': 'T42'}, 'presets .* for 10 levels at T42'),
    ({'levels': {'scale_height_m': 51000.0, 'upper': 3, 'interfaces_m': [20000.0]}}, 'presets .* for 5 levels at T21'),
])
def test_level_settings_the_adapter_cannot_write_are_refused(change, match):
    with pytest.raises(SpecError, match=match):
        ex.namelists(MOON, OPEN_MOON, {**DESIGN, **change}, top=LATER, calibrations=_given())


def test_plasims_presets_decide_where_a_generated_set_runs():
    """A generated set runs on the released ten's presets of rainmod: at T21 every count but five, on which PlaSim
    switches its shallow convection off; at T42 a set of ten levels alone, the count whose gamma is 0.007; and at
    T63, where rainmod presets nothing, every count."""
    ten_levels = {'scale_height_m': 51000.0, 'upper': 6, 'interfaces_m': [15500.0, 9000.0, 600.0]}
    entries = lambda run: ex.level_entries(derive.levels(run), run, 'a run')
    for run in ({**DESIGN, 'levels': ten_levels}, {**DESIGN, 'levels': ten_levels, 'resolution': 'T42'},
                {**DESIGN, 'levels': OPEN_MOON_LEVELS, 'resolution': 'T63'}):
        assert entries(run)['NEQSIG'] == -1 and len(entries(run)['SIGH']) == derive.level_count(run)
    assert ex.PRESET_LEVELS == {21: (5,), 42: (10,)} and ex.PRESETS_FOR == 10


def test_a_calibration_by_layer_is_read_on_the_half_levels_it_is_laid_on():
    fifteen, ten = derive.levels(FIFTEEN), derive.levels(DESIGN)
    other = derive.levels({**DESIGN, 'levels': {**OPEN_MOON_LEVELS, 'scale_height_m': 52000.0}})
    assert other['count'] == 15 and other['half_levels'] != fifteen['half_levels']
    ex.laid_on(fifteen['half_levels'], fifteen, 'the rows')
    ex.laid_on(list(fifteen['half_levels']), fifteen, 'the rows')
    ex.laid_on(None, ten, 'the rows')                       # a calibration made before the lab generated sets
    ex.laid_on(ten['half_levels'], ten, 'the rows')
    # Terluna's doubles for the same set, whose last bit differs at two half levels, bound the same layers.
    terlunas = tuple(float(x) for x in TERLUNA_SIGH.split(','))
    assert terlunas != fifteen['half_levels'] and ex.SAME_LEVEL == 1e-9
    ex.laid_on(terlunas, fifteen, 'the rows')
    nudged = fifteen['half_levels'][:13] + (0.9883 + 2e-9, 1.0)
    for stated, level_set, match in ((None, fifteen, 'state no half levels'),
                                     (other['half_levels'], fifteen, 'laid on other half levels'),
                                     (ten['half_levels'], fifteen, 'laid on other half levels'),
                                     (fifteen['half_levels'], ten, 'laid on other half levels'),
                                     (nudged, fifteen, 'laid on other half levels'),
                                     (fifteen['half_levels'][:13] + (float('nan'), 1.0), fifteen, 'laid on other')):
        with pytest.raises(SpecError, match=match):
            ex.laid_on(stated, level_set, 'the rows')


@needs_archive
@needs_sunlight
def test_a_run_on_a_generated_set_holds_its_tables_by_the_sets_layers(tmp_path):
    """The design run with the longwave correction on Terluna's values for the Open Moon's fifteen levels: the folder
    holds the files of the ten-level run, the namelist states the set, the two tables hold fifteen layers, and the
    record states the half levels. Calibrations laid on other half levels, or on none stated, are refused."""
    fifteen, run = derive.levels(FIFTEEN), {**LW_ICE, 'levels': OPEN_MOON_LEVELS}
    surface = ModelSurface(None, None, np.ones((32, 64)), np.zeros((32, 64)), np.zeros((32, 64)), None,
                           np.ones((32, 64)), {})                       # level ground, made up for the test
    record = ex.write_run(tmp_path / 'fifteen', MOON, OPEN_MOON, run, calibrations=_laid(fifteen['half_levels'], 15),
                          surface=surface, store=STORE)
    plain = ex.write_run(tmp_path / 'ten', MOON, OPEN_MOON, LW_ICE, calibrations=_laid(None, 10), surface=surface,
                         store=STORE)
    assert record['levels'] == fifteen and plain['levels'] == derive.levels(LW_ICE)
    assert set(record['files']) == set(plain['files'])
    differing = {name for name in plain['files'] if record['files'][name] != plain['files'][name]}
    assert differing == {'plasim_namelist', 'twilight.dat', 'lwcorr.dat'}
    rows = (tmp_path / 'fifteen' / 'twilight.dat').read_text().splitlines()
    assert rows[0] == '2' and [len(row.split()) for row in rows[1:]] == [17, 17, 16, 16]
    assert [len(row.split()) for row in (tmp_path / 'fifteen' / 'lwcorr.dat').read_text().splitlines()] == [16] * 3
    rows = (tmp_path / 'ten' / 'twilight.dat').read_text().splitlines()
    assert [len(row.split()) for row in rows[1:]] == [12, 12, 11, 11]
    ours, theirs = ((tmp_path / name / 'plasim_namelist').read_text().splitlines() for name in ('fifteen', 'ten'))
    assert [line for line in ours if line not in theirs] == [' NEQSIG = -1'] + ours[-3:-1]
    assert [line for line in theirs if line not in ours] == [' NEQSIG = 0']
    ten = derive.levels(LW_ICE)
    for name, calibrations, levels_run, match in (
            ('unstated', _laid(None, 15), run, "the ledger's terms state no half levels"),
            ('other', _laid(fifteen['half_levels'], 15, ledger=_laid(ten['half_levels'], 15).ledger), run,
             "the ledger's terms are laid on other half levels"),
            ('longwave', _laid(fifteen['half_levels'], 15, longwave=_laid(None, 15).longwave), run,
             "the longwave correction's rows state no half levels"),
            ('count', _laid(fifteen['half_levels'], 10), run, 'holds the ground and 15 layers'),
            ('released', _laid(fifteen['half_levels'], 10), LW_ICE, 'laid on other half levels')):
        with pytest.raises(SpecError, match=match):
            ex.write_run(tmp_path / name, MOON, OPEN_MOON, levels_run, calibrations=calibrations, surface=surface,
                         store=STORE)
        assert not (tmp_path / name).exists()


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
    (MOON, _with(DESIGN, switches={'surface_gust': 'similarity'}), OPEN_MOON, 'switches.surface_gust'),
    (MOON, _with(DESIGN, switches={'rain_evaporation': 'none'}), OPEN_MOON, 'switches.rain_evaporation'),
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
                        ('radmod_namelist', 'NLWCORR'): '0', ('rainmod_namelist', 'NEVAPPREC'): '1'}
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
    switched = {'NLWCORR': '1', 'NICEOPT': '1', 'TICEOPT': '235.15'}
    assert changed(*recorded) == switched
    # Patch 11 adds the ice weights of the light through the shield, where Terluna's patch 10 held the unfiltered
    # Sun's constants, 0.6164, 0.2283, 0.0811 and 0.0742 (world_spec.md, "Ice-optics weights").
    weights = {f'ZICEW({i})': ex.text(float(w)) for i, w in enumerate(top.sunlight['ice_weights'], 1)}
    assert changed(*pair) == switched | weights
    assert [round(float(weights[f'ZICEW({i})']), 4) for i in (1, 2, 3, 4)] == [0.6295, 0.2276, 0.0752, 0.0677]


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
    assert record['switches']['ice_weights'] == 'from-spectrum' and record['sunlight']['basis'] == 'calibration'
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
