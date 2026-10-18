"""The derived quantities: world_spec.md's table, the paper's data, and Terluna's records where the drive is at hand."""
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
REPRODUCTION = LIB.study('open-moon', reproduce=True)
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
    assert record['partial_pressures_bar'] == {
        'pN2': 0.9912863902624719, 'pO2': 0.21227, 'pAr': 0.011857249737528157, 'pCO2': 0.00048635999999999997}
    assert record['mole_fractions']['O2'] == pytest.approx(0.17457850, abs=5e-9) and record['mole_fractions']['CO2'] == 4e-4
    assert record['molar_mass_g_mol'] == pytest.approx(28.8319, abs=5e-5)
    assert record['zgasw'] == pytest.approx({'CO2': 6.1057e-4, 'O2': 0.19375}, abs=5e-6)
    assert record['specific_gas_constant'] == pytest.approx(288.38, abs=5e-3)
    assert record['scale_height_m'] / 1e3 == pytest.approx(52.4, abs=0.05)
    assert record['scale_height_over_radius'] == pytest.approx(0.03015, abs=5e-6)
    assert record['column_mass_kg_m2'] == pytest.approx(74861, abs=0.5) and record['chapman_horizon'] == pytest.approx(7.2, abs=0.05)
    assert record['capillary_factor'] == pytest.approx(2.4576, abs=5e-5) and record['soil_factor'] == pytest.approx(5.4342, abs=5e-5)
    assert record['model_day_days'] == pytest.approx(29.8054, abs=5e-5)


def test_a_reproduction_takes_terlunas_gravity():
    record = derive.planet(MOON, REPRODUCTION.scenario, compat=REPRODUCTION.compatibility)
    assert record['gravity_m_s2'] == 1.6242188765608128 and record['stated'].keys() == {'solar_day_days'}


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


def test_cm1_scales_by_exactly_one_at_its_reference_state():
    factors = derive.cm1_factors(MOON, OPEN_MOON, CM1, gravity_rule='gm-over-r2')
    assert (factors['length'], factors['time'], factors['rate']) == (1.0, 1.0, 1.0)
    assert derive.cm1_factors(MOON, OPEN_MOON, CM1)['length'] - 1 == pytest.approx(5.05e-6, rel=0.01)
    hotter = derive.cm1_factors(MOON, OPEN_MOON, CM1, gravity_rule='gm-over-r2', temperature_k=305.0)
    assert hotter['length'] == pytest.approx(305.0 / 295.0)


def test_cm1_at_earths_state_with_cm1s_gravity():
    earth = _with(EARTH, body={'gravity_m_s2': 9.81})
    ring = LIB.study('open-moon').crm['ring_45n_corrected']
    values = derive.cm1_values(ring.settings, derive.cm1_factors(earth, CONTROL, CM1))
    assert values['column_target_m'] == pytest.approx(965, abs=0.5) and values['ztop_m'] / 1e3 == pytest.approx(24.1, abs=0.05)
    assert (values['nudge_start_m'], values['nudge_full_m']) == pytest.approx((1287, 2574), abs=1.0)
    assert values['time_step_s'] == pytest.approx(6.53, abs=5e-3) and values['pbl_length_m'] == pytest.approx(72.9, abs=0.05)
    assert 1 / values['rayleigh_rate_per_s'] == pytest.approx(296, abs=0.5)


def test_a_studys_own_values_stand_unscaled():
    own, reproduction = LIB.study('open-moon').crm['ring_45n_corrected'], REPRODUCTION.crm['ring_45n_corrected']
    factors = derive.cm1_factors(MOON, OPEN_MOON, CM1)
    assert derive.cm1_values(own.settings, factors)['soil_top_layer_m'] == pytest.approx(0.054342, abs=5e-7)
    assert 'diurnal.soil_top_layer_m' in reproduction.set_paths
    rep = derive.cm1_values(reproduction.settings, factors, set_paths=reproduction.set_paths)
    assert rep['soil_top_layer_m'] == 0.05                       # patch 08's, as set
    assert (rep['breakup_diameter_m'], rep['rain_max_mean_diameter_m']) == (3.0e-4, 2.8e-3)   # Morrison's own
    capillary = derive.cm1_values(own.settings, factors)
    assert capillary['rain_max_mean_diameter_m'] == pytest.approx(6.88e-3, abs=5e-6)
    breakup = _with(own.settings, physics={'rain_size_limits': 'breakup-only'})
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


def test_the_air_takes_each_gas_in_either_form():
    mixed = {k: v for k, v in OPEN_MOON['air'].items() if k != 'ar_per_n2'} | {'ar_mole_fraction': 0.00975}
    pressures = derive.partial_pressures_bar({**OPEN_MOON, 'air': mixed})
    assert pressures['pAr'] == pytest.approx(0.00975 * 1.2159) and sum(pressures.values()) == pytest.approx(1.2159)


def test_the_advective_limit_of_exoplasims_step():
    assert derive.advective_limit_wind_m_s(1737400.0, 21, 1800.0) == pytest.approx(45.96, abs=5e-3)


# The paper's data (paper/data/regime_calc.json, worlds.json), each derived from the basis it states.

REGIME = json.loads((PAPER / 'regime_calc.json').read_text())


def test_the_papers_regime_quantities_come_out_unchanged():
    gm = derive.gravity(MOON, rule='gm-over-r2')
    assert gm == REGIME['gravity']['moon_surface_m_s2']
    fractions = derive.mole_fractions(OPEN_MOON)
    air = REGIME['air']
    assert (fractions['O2'], fractions['N2'], fractions['Ar']) == (air['o2_fraction'], air['n2_fraction'], air['ar_fraction'])
    molar_mass = derive.molar_mass_g_mol(fractions)
    assert molar_mass == air['molar_mass_g_mol']
    assert derive.column_mass_kg_m2(121590.0, gm) == REGIME['column_mass']['moon_kg_m2']
    h_moon = derive.scale_height_m(295.0, molar_mass, gm)
    h_earth = derive.scale_height_m(288.0, 28.9647, derive.STANDARD_G)
    assert (h_moon / 1e3, h_earth / 1e3) == (REGIME['scale_height']['moon_km'], REGIME['scale_height']['earth_km'])
    assert derive.chapman_horizon(1737400.0, h_moon) == REGIME['horizon_air_mass_chapman']['moon']
    assert derive.chapman_horizon(6371000.0, h_earth) == REGIME['horizon_air_mass_chapman']['earth']
    assert derive.capillary_factor(gm, derive.STANDARD_G) == REGIME['capillary_length_ratio']['value']
    omega = derive.rotation_rate(MOON)
    assert omega == REGIME['rotation']['omega_s']
    assert derive.coriolis(omega, 80.0) == REGIME['rotation']['coriolis_80deg_s']
    assert derive.soil_factor(29.53059) == REGIME['soil_wave_depth_ratio']['value']


def test_the_papers_plasim_calendar_and_slow_rotators_come_out_unchanged():
    cal = derive.calendar(MOON, {**EXOPLASIM, 'whole_model_days': False})
    stepped_day = cal['stepped_model_day_s'] / derive.DAY_S
    calendar = REGIME['plasim_calendar']
    assert stepped_day == calendar['model_day_days']
    assert cal['run_steps_per_year'] / cal['steps_per_model_day'] == calendar['model_days_per_360d_year']
    assert cal['run_steps_per_year'] - 12 * cal['steps_per_model_day'] == calendar['slip_steps_per_year']
    assert derive.sun_clock_sweep_deg(stepped_day, 27.321661) == REGIME['sun_clock_skip']['moon_sweep_deg']
    for label, row in REGIME['exoplasim_slow_rotators'].items():
        if label == 'formula':
            continue
        period = 27.321661 if label == '27.3217d' else float(label[:-1])
        n = derive.days_per_year(period, 365.25)
        assert n == row['N'] and derive.sun_clock_skip_deg(n) == row['skip_deg']
        assert derive.model_day_days(period, n) == row['model_day_days']
        assert derive.synodic_period_days(period, 365.25) == row['solar_day_days']


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


# Terluna's records, read where its research drive is at hand.

@needs_drive
def test_the_design_runs_recorded_planet_and_gases():
    cfg = json.loads((DRIVE / 'gcm-runs' / 'A28_corrected_970' / 'progress.json').read_text())['configuration']
    record = derive.planet(MOON, REPRODUCTION.scenario, compat=REPRODUCTION.compatibility)
    assert cfg['gases_bar'] == record['partial_pressures_bar']
    assert cfg['gas_bands']['mass_fractions'] == record['zgasw']
    assert cfg['planet']['gravity'] == record['gravity_m_s2']
    assert cfg['planet']['rotationperiod'] == record['exoplasim_rotationperiod_days']
    assert cfg['planet']['radius'] == MOON['body']['radius_m'] / REPRODUCTION.compatibility['exoplasim_radius_divisor_m']


@needs_drive
def test_the_cm1_builds_macros():
    record = derive.planet(MOON, REPRODUCTION.scenario, compat=REPRODUCTION.compatibility)
    fractions = record['mole_fractions']
    flags = f"-DTERLUNA_G={record['gravity_m_s2']!r} -DTERLUNA_CO2={fractions['CO2']:.6e} -DTERLUNA_O2={fractions['O2']:.6f}"
    for label in REPRODUCTION.compatibility['cm1_build_labels'].values():
        assert json.loads((DRIVE / 'cm1' / 'build' / label / 'build.json').read_text())['flags'] == flags


@needs_drive
@pytest.mark.parametrize('name', ['ring_45n_corrected', 'ring_45n_corrected_twilight', 'box_jura'])
def test_each_cases_recorded_grid_and_settings(name):
    case = REPRODUCTION.crm[name]
    folder = DRIVE / 'crm-runs' / name
    record = json.loads((folder / 'case.json').read_text())
    namelist = {k: float(v) for k, v in re.findall(r'^\s*(\w+)\s*=\s*([-+0-9.eE]+)\s*,', (folder / 'namelist.input').read_text(), re.M)}
    factors = derive.cm1_factors(MOON, REPRODUCTION.scenario, CM1, gravity_rule='gm-over-r2')
    values = derive.cm1_values(case.settings, factors, set_paths=case.set_paths)
    ring_name = case.settings['site']['ring'] if case.settings['kind'] == 'box' else name
    latitude = REPRODUCTION.crm[ring_name].settings['latitude_deg']
    ring = derive.ring_grid(MOON['body']['radius_m'], latitude, values['column_target_m'], CM1['ranks_multiple'])
    assert record['grid']['dx_m'] == ring['dx_m'] and namelist['dx'] == round(ring['dx_m'], 3)
    sunrise = derive.sunrise_hour_angle_deg(latitude, derive.declination_deg(MOON['rotation']['obliquity_deg'],
                                                                              case.settings['solar_longitude_deg']))
    if case.settings['kind'] == 'ring':
        assert (record['grid']['nx'], record['grid']['length_m']) == (ring['nx'], ring['length_m'])
        assert (namelist['var16'], namelist['var18']) == (round(ring['length_m'], 3), sunrise)
    else:                                  # a box: its own columns, at its site's longitude
        assert (namelist['nx'], namelist['ny']) == (case.settings['columns']['nx'], case.settings['columns']['ny'])
        assert (namelist['var16'], namelist['var18']) == (0.0, sunrise + case.settings['site']['longitude_deg'])
    assert namelist['var19'] == round(derive.solar_day_days(MOON) * derive.DAY_S, 1)
    assert namelist['fcor'] == float(f'{derive.coriolis(derive.rotation_rate(MOON), latitude):.6e}')
    assert (namelist['ztop'], namelist['dtl']) == (values['ztop_m'], values['time_step_s'])
    assert (namelist['var14'], namelist['var15']) == (values['nudge_start_m'], values['nudge_full_m'])
    assert namelist['l_inf'] == round(values['pbl_length_m'], 1)
    assert namelist['rdalpha'] == round(values['rayleigh_rate_per_s'], 8)
    assert namelist['zd'] == case.settings['unscaled']['damping_base_fraction'] * values['ztop_m']
