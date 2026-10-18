"""The derived quantities: world_spec.md's table, the paper's data, and comparisons with Terluna's records where its
research drive is at hand."""
import json
import re
import warnings

import pytest

from worldlab import derive
from worldlab.roots import root
from worldlab.spec import LAB, Library, SpecError

LIB = Library()
MOON, EARTH, MARS = (LIB.world(w) for w in ('moon', 'earth', 'mars'))
OPEN_MOON, CONTROL = LIB.scenario('moon/open-moon'), LIB.scenario('earth/control')
EXOPLASIM, CM1 = LIB.defaults('exoplasim/defaults'), LIB.defaults('cm1/defaults')
STUDY = LIB.study('open-moon')
PAPER = LAB.parent / 'paper' / 'data'
DRIVE = root('terluna-drive')
needs_drive = pytest.mark.skipif(DRIVE is None, reason="Terluna's research drive is not set (lab/local.example.toml)")


def _with(tree, **tables):
    """A copy of a world or scenario with some of its tables' fields replaced."""
    return {**tree, **{t: {**tree[t], **fields} for t, fields in tables.items()}}


# The planet record, against world_spec.md's table for the Open Moon.

def test_the_moons_planet_record():
    record = derive.planet(MOON, OPEN_MOON, exoplasim=EXOPLASIM)
    assert record['gravity_m_s2'] == pytest.approx(1.6242107, abs=5e-8)
    assert record['rotation_rate_rad_s'] == pytest.approx(2.6616995e-6, rel=1e-7)
    assert record['stated'] == {'solar_day_days': {'stated': 29.53059, 'derived': pytest.approx(29.5305882, abs=5e-8)}}
    assert record['solar_day_days'] == 29.53059 and record['exoplasim_rotationperiod_days'] == 27.321661
    assert record['partial_pressures_bar'] == pytest.approx(
        {'pN2': 0.99128639, 'pO2': 0.21227, 'pAr': 0.01185725, 'pCO2': 0.00048636}, abs=5e-9)
    assert record['mole_fractions']['O2'] == pytest.approx(0.17457850, abs=5e-9) and record['mole_fractions']['CO2'] == 4e-4
    assert record['molar_mass_g_mol'] == pytest.approx(28.8319, abs=5e-5)
    assert record['zgasw'] == pytest.approx({'CO2': 6.1057e-4, 'O2': 0.19375}, abs=5e-6)
    assert record['specific_gas_constant'] == pytest.approx(288.38, abs=5e-3)
    assert record['scale_height_m'] / 1e3 == pytest.approx(52.4, abs=0.05)
    assert record['scale_height_over_radius'] == pytest.approx(0.03015, abs=5e-6)
    assert record['column_mass_kg_m2'] == pytest.approx(74861, abs=0.5) and record['chapman_horizon'] == pytest.approx(7.2, abs=0.05)
    assert record['capillary_factor'] == pytest.approx(2.4576, abs=5e-5) and record['soil_factor'] == pytest.approx(5.4342, abs=5e-5)
    assert record['model_day_days'] == pytest.approx(29.8054, abs=5e-5)


def test_exoplasims_calendar_on_the_moon():
    cal = derive.calendar(MOON, EXOPLASIM)
    assert {k: v for k, v in cal.items() if k not in ('model_day_s', 'stepped_model_day_s')} == dict(
        rotationperiod=27.321661, n_days_per_year=12, step_s=1800.0, steps_per_model_day=1430, steps_per_mean=143,
        run_steps_per_year=17160, means_per_year=120, whole_means=True)
    assert cal['stepped_model_day_s'] == 1430 * 1800.0


@pytest.mark.parametrize('timestep_min, steps', [(30.0, 1430), (50.0, 834), (25.0, 1728)])
def test_plasim_evens_its_steps_before_it_counts_the_model_day(timestep_min, steps):
    assert derive.steps_per_model_day(derive.model_day_days(27.321661, 12) * derive.DAY_S, timestep_min) == steps


def test_without_whole_model_days_configure_runs_a_360_day_year():
    cal = derive.calendar(MOON, {**EXOPLASIM, 'whole_model_days': False})
    assert (cal['run_steps_per_year'], cal['whole_means']) == (17280, False)


def test_cm1_scales_by_one_at_its_reference_state():
    at_reference = _with(MOON, body={'gravity_m_s2': CM1['reference']['gravity_m_s2']})
    factors = derive.cm1_factors(at_reference, OPEN_MOON, CM1)
    assert (factors['length'], factors['time'], factors['rate']) == (1.0, 1.0, 1.0)
    assert derive.cm1_factors(MOON, OPEN_MOON, CM1)['length'] - 1 == pytest.approx(5.05e-6, rel=0.01)   # the spin term
    hotter = derive.cm1_factors(at_reference, OPEN_MOON, CM1, temperature_k=305.0)
    assert hotter['length'] == pytest.approx(305.0 / 295.0)


def test_cm1_at_earths_state_with_cm1s_gravity():
    earth = _with(EARTH, body={'gravity_m_s2': 9.81})
    ring = STUDY.crm['ring_45n']
    values = derive.cm1_values(ring.settings, derive.cm1_factors(earth, CONTROL, CM1))
    assert values['column_target_m'] == pytest.approx(965, abs=0.5) and values['ztop_m'] / 1e3 == pytest.approx(24.1, abs=0.05)
    assert (values['nudge_start_m'], values['nudge_full_m']) == pytest.approx((1287, 2574), abs=1.0)
    assert values['time_step_s'] == pytest.approx(6.53, abs=5e-3) and values['pbl_length_m'] == pytest.approx(72.9, abs=0.05)
    assert 1 / values['rayleigh_rate_per_s'] == pytest.approx(296, abs=0.5)


def test_a_studys_own_values_stand_unscaled():
    ring = STUDY.crm['ring_45n']
    factors = derive.cm1_factors(MOON, OPEN_MOON, CM1)
    assert derive.cm1_values(ring.settings, factors)['soil_top_layer_m'] == pytest.approx(0.054342, abs=5e-7)
    stated = _with(ring.settings, diurnal={'soil_top_layer_m': 0.05})
    assert derive.cm1_values(stated, factors, set_paths=frozenset({'diurnal.soil_top_layer_m'}))['soil_top_layer_m'] == 0.05
    capillary = derive.cm1_values(ring.settings, factors)
    assert capillary['rain_max_mean_diameter_m'] == pytest.approx(6.88e-3, abs=5e-6)
    earth = derive.cm1_values(_with(ring.settings, physics={'rain_size_limits': 'earth'}), factors)
    assert (earth['breakup_diameter_m'], earth['rain_max_mean_diameter_m']) == (3.0e-4, 2.8e-3)     # Morrison's own
    breakup = _with(ring.settings, physics={'rain_size_limits': 'breakup-only'})
    assert derive.cm1_values(breakup, factors)['rain_max_mean_diameter_m'] == 2.8e-3


def test_the_suns_season_and_sunrise():
    assert derive.declination_deg(1.5424, 0.0) == 0.0 and derive.sunrise_hour_angle_deg(45.0, 0.0) == -90.0
    mars_summer = derive.declination_deg(25.19, 90.0)
    assert mars_summer == pytest.approx(25.19) and derive.sunrise_hour_angle_deg(45.0, mars_summer) == pytest.approx(-118.06, abs=0.01)
    for latitude in (80.0, -80.0):                                   # polar day, then polar night
        with pytest.raises(SpecError, match='neither rises nor sets'):
            derive.sunrise_hour_angle_deg(latitude, 20.0)


def test_the_moons_ring():
    ring = derive.ring_grid(MOON['body']['radius_m'], 45.0, 6000.0, CM1['ranks_multiple'])
    assert ring['nx'] == 1288 and ring['dx_m'] == pytest.approx(5993.06, abs=5e-3)
    with pytest.raises(SpecError, match='fewer columns'):
        derive.ring_grid(MOON['body']['radius_m'], 89.99, 6000.0, CM1['ranks_multiple'])


# Earth and Mars.

def test_earth_keeps_plasims_24_hour_path():
    cal = derive.calendar(EARTH, EXOPLASIM)
    assert (cal['rotationperiod'], cal['n_days_per_year'], cal['model_day_s'], cal['steps_per_model_day']) == (1.0, 365, 86400.0, 48)
    assert (cal['steps_per_mean'], cal['means_per_year']) == (48, 365)          # 3 days rounds to 1, a divisor of 365
    record = derive.planet(EARTH, CONTROL)
    assert record['gravity_m_s2'] == 9.80665
    assert record['stated']['gravity_m_s2']['derived'] == pytest.approx(9.7977, abs=5e-5)


def test_stated_values_far_from_their_derivations_are_refused():
    with pytest.raises(SpecError, match='gravity_m_s2'):
        derive.gravity(_with(EARTH, body={'gravity_m_s2': 9.9}))
    with pytest.raises(SpecError, match='solar_day_days'):
        derive.solar_day_days(_with(MOON, rotation={'solar_day_days': 29.6}))
    with pytest.raises(SpecError, match='solar_day_days'):                       # also through the calendar
        derive.calendar(_with(MARS, rotation={'solar_day_days': 1.0}), EXOPLASIM)


def test_worlds_that_would_mislead_exoplasim_are_refused():
    with pytest.raises(SpecError, match='24-hour path'):
        derive.exoplasim_rotationperiod_days(_with(MARS, rotation={'sidereal_period_days': 1.0}))
    with pytest.raises(SpecError, match='locked to the year'):
        derive.synodic_period_days(10.0, 10.0)


def test_mars():
    record = derive.planet(MARS, LIB.scenario('mars/breathable-1bar'), exoplasim=EXOPLASIM)
    assert record['gravity_m_s2'] == pytest.approx(3.7165, abs=5e-5) and record['capillary_factor'] == pytest.approx(1.62, abs=5e-3)
    assert record['calendar']['n_days_per_year'] == 348 and record['model_day_days'] == pytest.approx(1.0289, abs=5e-5)
    assert 'scale_height_m' not in record                           # its temperature is the fixpoint's to find
    with pytest.raises(SpecError, match='settled'):
        derive.reference_temperature_k(LIB.scenario('mars/breathable-1bar'))


@pytest.mark.parametrize('air, message', [
    ({'balance': 'Ar'}, 'balance'),
    ({'o2_mole_fraction': 0.2}, 'exactly one'),
    ({'co2_ppm': 'unchosen'}, 'unchosen'),
])
def test_ill_formed_air_is_refused(air, message):
    with pytest.raises(SpecError, match=message):
        derive.mole_fractions(_with(OPEN_MOON, air=air))


def test_air_whose_stated_gases_exceed_its_total_is_refused():
    with pytest.raises(SpecError, match='exceed the total'):
        derive.mole_fractions(_with(OPEN_MOON, air={'o2_partial_pressure_pa': 125000.0}))


@pytest.mark.parametrize('air, message', [({'surface_pressure_pa': 'unchosen'}, 'unchosen'), ({'surface_pressure_pa': None}, 'states no')])
def test_partial_pressures_refuse_air_without_a_total(air, message):
    scenario = _with(OPEN_MOON, air=air)
    scenario['air'] = {k: v for k, v in scenario['air'].items() if v is not None}
    with pytest.raises(SpecError, match=message):
        derive.partial_pressures_bar(scenario)


def test_the_air_takes_each_gas_in_either_form():
    mixed = {k: v for k, v in OPEN_MOON['air'].items() if k != 'ar_per_n2'} | {'ar_mole_fraction': 0.00975}
    pressures = derive.partial_pressures_bar({**OPEN_MOON, 'air': mixed})
    assert pressures['pAr'] == pytest.approx(0.00975 * 1.2159) and sum(pressures.values()) == pytest.approx(1.2159)


def test_the_advective_limit_of_exoplasims_step():
    assert derive.advective_limit_wind_m_s(1737400.0, 21, 1800.0) == pytest.approx(45.96, abs=5e-3)


def test_the_time_step_guard_warns_past_its_share_of_the_limit():
    limit = derive.advective_limit_wind_m_s(1737400.0, 21, 1800.0)
    quiet, loud = (derive.time_step_guard(f * limit, 1737400.0, EXOPLASIM) for f in (0.89, 0.91))
    assert quiet['limit_m_s'] == pytest.approx(limit, rel=1e-12) and not quiet['warns'] and loud['warns']
    at = derive.time_step_guard(30.0, 1737400.0, EXOPLASIM)['share_of_limit']        # a wind at the share itself
    assert not derive.time_step_guard(30.0, 1737400.0, {**EXOPLASIM, 'guards': {'wind_share_of_limit': at}})['warns']
    assert derive.truncation('T42') == 42


@pytest.mark.parametrize('resolution', ['R15', 'T0', 'T31', 21, 'T'])
def test_resolutions_off_exoplasims_grids_are_refused(resolution):
    with pytest.raises(SpecError, match="ExoPlaSim's grids"):
        derive.truncation(resolution)


GUARD_RECORD = json.loads((LAB / 'validation' / 'timestep_guard.json').read_text())


def test_the_guard_stays_silent_on_each_of_terlunas_scanned_runs():
    """Terluna's 45 lunar runs scanned in lab/validation/timestep_guard.json ran stable at 30 minutes. At 90% of
    the advective limit the guard warns on none of them; the 80% first proposed would warn on the hottest."""
    shares = {}
    for run, best in GUARD_RECORD['runs'].items():
        defaults = {**EXOPLASIM, 'resolution': f"T{best['truncation']}", 'timestep_min': best['timestep_min']}
        guard = derive.time_step_guard(best['m_s'], best['radius_m'], defaults)
        assert not guard['warns'], run
        shares[run] = guard['share_of_limit']
    hottest = max(shares, key=shares.get)
    assert len(shares) == 45 and hottest == 'A28_corrected_970_lw_ice' and 0.8 < shares[hottest] < 0.9


# The paper's data (paper/data/regime_calc.json, worlds.json), each derived from the basis it states.

REGIME = json.loads((PAPER / 'regime_calc.json').read_text())


def _paper(value):
    """A paper value, matched to one part in 10¹²."""
    return pytest.approx(value, rel=1e-12, abs=0.0)


def test_the_papers_regime_quantities_agree_with_the_derivations():
    gm = derive.gravity(MOON, rule='gm-over-r2')
    assert gm == _paper(REGIME['gravity']['moon_surface_m_s2'])
    fractions = derive.mole_fractions(OPEN_MOON)
    air = REGIME['air']
    assert (fractions['O2'], fractions['N2'], fractions['Ar']) == _paper((air['o2_fraction'], air['n2_fraction'], air['ar_fraction']))
    molar_mass = derive.molar_mass_g_mol(fractions)
    assert molar_mass == _paper(air['molar_mass_g_mol'])
    assert derive.column_mass_kg_m2(121590.0, gm) == _paper(REGIME['column_mass']['moon_kg_m2'])
    h_moon = derive.scale_height_m(295.0, molar_mass, gm)
    h_earth = derive.scale_height_m(288.0, 28.9647, derive.STANDARD_G)
    assert (h_moon / 1e3, h_earth / 1e3) == _paper((REGIME['scale_height']['moon_km'], REGIME['scale_height']['earth_km']))
    assert derive.chapman_horizon(1737400.0, h_moon) == _paper(REGIME['horizon_air_mass_chapman']['moon'])
    assert derive.chapman_horizon(6371000.0, h_earth) == _paper(REGIME['horizon_air_mass_chapman']['earth'])
    assert derive.capillary_factor(gm, derive.STANDARD_G) == _paper(REGIME['capillary_length_ratio']['value'])
    omega = derive.rotation_rate(MOON)
    assert omega == _paper(REGIME['rotation']['omega_s'])
    assert derive.coriolis(omega, 80.0) == _paper(REGIME['rotation']['coriolis_80deg_s'])
    assert derive.soil_factor(29.53059) == _paper(REGIME['soil_wave_depth_ratio']['value'])


def test_the_papers_plasim_calendar_and_slow_rotators_agree_with_the_derivations():
    cal = derive.calendar(MOON, {**EXOPLASIM, 'whole_model_days': False})
    stepped_day = cal['stepped_model_day_s'] / derive.DAY_S
    calendar = REGIME['plasim_calendar']
    assert stepped_day == _paper(calendar['model_day_days'])
    assert cal['run_steps_per_year'] / cal['steps_per_model_day'] == _paper(calendar['model_days_per_360d_year'])
    assert cal['run_steps_per_year'] - 12 * cal['steps_per_model_day'] == calendar['slip_steps_per_year']
    assert derive.sun_clock_sweep_deg(stepped_day, 27.321661) == _paper(REGIME['sun_clock_skip']['moon_sweep_deg'])
    for label, row in REGIME['exoplasim_slow_rotators'].items():
        if label == 'formula':
            continue
        period = 27.321661 if label == '27.3217d' else float(label[:-1])
        n = derive.days_per_year(period, 365.25)
        assert n == row['N'] and derive.sun_clock_skip_deg(n) == _paper(row['skip_deg'])
        assert derive.model_day_days(period, n) == _paper(row['model_day_days'])
        assert derive.synodic_period_days(period, 365.25) == _paper(row['solar_day_days'])


def test_each_row_of_the_papers_worlds_follows_from_its_stated_basis():
    for row in json.loads((PAPER / 'worlds.json').read_text())['rows']:
        h = derive.scale_height_m(row['temperature_k'], row['molar_mass_g_mol'], row['g_m_s2'])
        radius = row['radius_km'] * 1e3
        derived = dict(scale_height_km=h / 1e3, h_over_r=h / radius,
                       column_mass_t_m2=derive.column_mass_kg_m2(row['surface_pressure_bar'] * 1e5, row['g_m_s2']) / 1e3,
                       chapman_horizon=derive.chapman_horizon(radius, h))
        for key, value in derived.items():
            stated = row[key]
            places = len(repr(stated).split('.')[1]) if '.' in repr(stated) else 0
            assert abs(value - stated) <= 0.6 * 10 ** -places, (row['name'], key, value, stated)


# The roots.

def test_a_root_counts_only_as_a_folder_that_holds_something(tmp_path, monkeypatch):
    monkeypatch.delenv('TERLUNA_DRIVE', raising=False)
    (tmp_path / 'empty').mkdir()
    (tmp_path / 'full').mkdir()
    (tmp_path / 'full' / 'gcm-runs').mkdir()
    for value, expected in (('empty', None), ('full', tmp_path / 'full'), ('missing', None)):
        (tmp_path / 'local.toml').write_text(f'[roots]\n"terluna-drive" = "{value}"\n')
        assert root('terluna-drive', lab=tmp_path) == expected
    (tmp_path / 'local.toml').write_text('[roots\n')
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        assert root('terluna-drive', lab=tmp_path) is None
    assert caught and 'ignored' in str(caught[0].message)


# Comparisons with Terluna's records, read where its research drive is at hand. The lab's own derivations take the
# spin term in the gravity, 5 parts per million on the Moon, where Terluna took GM/R²: CM1's lengths and times grow,
# and its rates shrink, by the ratio of the two gravities. The comparisons put that cause into Terluna's values and
# then hold each to the rounding of Terluna's writer, or to 10⁻¹² where the arithmetic alone differs.

G_TERLUNA = derive.gravity(MOON, rule='gm-over-r2')
RATIO = G_TERLUNA / derive.gravity(MOON)  # 1 + 5.05e-6: the lab's lengths and times against Terluna's
TERLUNA_CASES = {'ring_45n': 'ring_45n_corrected', 'ring_45n_twilight': 'ring_45n_corrected_twilight', 'box_jura': 'box_jura'}
TERLUNA_BUILDS = ('moon_omp_o3', 'moon_omp_twilight', 'moon_omp_terrain_sea_twilight')


@needs_drive
def test_the_planet_and_gases_agree_with_terlunas_design_run():
    cfg = json.loads((DRIVE / 'gcm-runs' / 'A28_corrected_970' / 'progress.json').read_text())['configuration']
    record = derive.planet(MOON, OPEN_MOON)
    assert record['partial_pressures_bar'] == pytest.approx(cfg['gases_bar'], rel=1e-12)
    assert record['zgasw'] == pytest.approx(cfg['gas_bands']['mass_fractions'], rel=1e-12)
    assert cfg['planet']['gravity'] == pytest.approx(G_TERLUNA, rel=1e-12)
    spin = 2.0 / 3.0 * derive.rotation_rate(MOON) ** 2 * MOON['body']['radius_m']
    assert record['gravity_m_s2'] == pytest.approx(cfg['planet']['gravity'] - spin, rel=1e-12)
    assert record['exoplasim_rotationperiod_days'] == cfg['planet']['rotationperiod']


@needs_drive
def test_the_air_and_gravity_agree_with_terlunas_cm1_builds():
    record = derive.planet(MOON, OPEN_MOON)
    for label in TERLUNA_BUILDS:
        flags = json.loads((DRIVE / 'cm1' / 'build' / label / 'build.json').read_text())['flags']
        macros = {k: float(v) for k, v in re.findall(r'-DTERLUNA_(\w+)=(\S+)', flags)}
        assert macros['G'] == pytest.approx(G_TERLUNA, rel=1e-12)
        assert macros['CO2'] == pytest.approx(record['mole_fractions']['CO2'], rel=5e-7)       # written %.6e
        assert macros['O2'] == pytest.approx(record['mole_fractions']['O2'], abs=5e-7)         # written %.6f


@needs_drive
@pytest.mark.parametrize('name', sorted(TERLUNA_CASES))
def test_each_cases_grid_and_settings_agree_with_terlunas_case(name):
    case = STUDY.crm[name]
    folder = DRIVE / 'crm-runs' / TERLUNA_CASES[name]
    record = json.loads((folder / 'case.json').read_text())
    namelist = {k: float(v) for k, v in re.findall(r'^\s*(\w+)\s*=\s*([-+0-9.eE]+)\s*,', (folder / 'namelist.input').read_text(), re.M)}
    values = derive.cm1_values(case.settings, derive.cm1_factors(MOON, OPEN_MOON, CM1), set_paths=case.set_paths)
    ring_name = case.settings['site']['ring'] if case.settings['kind'] == 'box' else name
    latitude = STUDY.crm[ring_name].settings['latitude_deg']
    ring = derive.ring_grid(MOON['body']['radius_m'], latitude, values['column_target_m'], CM1['ranks_multiple'])
    assert record['grid']['dx_m'] == pytest.approx(ring['dx_m'], rel=1e-12) and namelist['dx'] == pytest.approx(ring['dx_m'], abs=5e-4)
    sunrise = derive.sunrise_hour_angle_deg(latitude, derive.declination_deg(MOON['rotation']['obliquity_deg'],
                                                                              case.settings['solar_longitude_deg']))
    if case.settings['kind'] == 'ring':
        assert record['grid']['nx'] == ring['nx'] and record['grid']['length_m'] == pytest.approx(ring['length_m'], rel=1e-12)
        assert (namelist['var16'], namelist['var18']) == pytest.approx((ring['length_m'], sunrise), abs=5e-4)
    else:                                  # a box: its own columns, at its site's longitude
        assert (namelist['nx'], namelist['ny']) == (case.settings['columns']['nx'], case.settings['columns']['ny'])
        assert (namelist['var16'], namelist['var18']) == pytest.approx((0.0, sunrise + case.settings['site']['longitude_deg']))
    assert namelist['var19'] == pytest.approx(derive.solar_day_days(MOON) * derive.DAY_S, abs=0.05)
    assert namelist['fcor'] == pytest.approx(derive.coriolis(derive.rotation_rate(MOON), latitude), rel=5e-7)
    for key, value in (('ztop', 'ztop_m'), ('dtl', 'time_step_s'), ('var14', 'nudge_start_m'), ('var15', 'nudge_full_m')):
        assert values[value] == pytest.approx(namelist[key] * RATIO, rel=1e-12), key
    assert values['pbl_length_m'] == pytest.approx(namelist['l_inf'] * RATIO, abs=0.0501)            # written to 0.1 m
    assert values['rayleigh_rate_per_s'] == pytest.approx(namelist['rdalpha'] / RATIO, abs=5.01e-9)   # written to 1e-8
    assert case.settings['unscaled']['damping_base_fraction'] * values['ztop_m'] == pytest.approx(namelist['zd'] * RATIO, rel=1e-12)
