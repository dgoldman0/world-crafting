"""Derived quantities: what the models need, computed from a world, its scenario and a model's defaults.

`planet()` gathers them into the planet record, under the names the registry's tests use (world_spec.md, "The
first derived quantities"), with each stated value beside its derivation. The functions it calls are the
derivations, one for each quantity, each written in its plainest form. ExoPlaSim's calendar follows the model's
own rounding, as its configure and plasim.f90 count it, since the lab predicts the days and steps the model will
take.
"""
from __future__ import annotations

import math

from .spec import SpecError, unchosen

DAY_S = 86400.0
R_GAS = 8.314462618                      # J mol-1 K-1, CODATA 2018
MOLAR_MASS = {'N2': 28.0134, 'O2': 31.9988, 'Ar': 39.948, 'CO2': 44.0095}             # g/mol
CM1_EARTH_G = 9.81                       # CM1's and Morrison's Earth gravity
STANDARD_G = 9.80665
# A stated value must lie this close to its derivation (world_spec.md, rule 2), relatively; a breach refuses.
TOLERANCE = {'gravity_m_s2': 2e-3, 'solar_day_days': 1e-5}


# The planet record.

def planet(world: dict, scenario: dict, *, exoplasim: dict | None = None) -> dict:
    """The planet record: the quantities of world_spec.md's table that the world and scenario fix, under the
    registry's names, and ExoPlaSim's calendar where its defaults are given. `stated` holds each stated value
    beside its derivation. The sunlight at the top, the ice-optics weights and the pressure at the surface's
    lowest point come with the derivations that read the manifest's data."""
    g = gravity(world)
    stated = {}
    if world['body'].get('gravity_m_s2') is not None:
        stated['gravity_m_s2'] = dict(stated=world['body']['gravity_m_s2'], derived=gravity_derived(world))
    if world['rotation'].get('solar_day_days') is not None:
        stated['solar_day_days'] = dict(stated=world['rotation']['solar_day_days'], derived=solar_day_derived(world))
    day = solar_day_days(world)
    fractions = mole_fractions(scenario)
    pressures, molar_mass = partial_pressures_bar(scenario), molar_mass_g_mol(fractions)
    record = dict(gravity_m_s2=g, rotation_rate_rad_s=rotation_rate(world), solar_day_days=day,
                  exoplasim_rotationperiod_days=exoplasim_rotationperiod_days(world),
                  partial_pressures_bar=pressures, mole_fractions=fractions, molar_mass_g_mol=molar_mass,
                  zgasw=zgasw(fractions), specific_gas_constant=specific_gas_constant(molar_mass),
                  capillary_factor=capillary_factor(g), soil_factor=soil_factor(day), stated=stated)
    if scenario['air']['reference_temperature_k'] != 'settled':
        radius = world['body']['radius_m']
        h = scale_height_m(reference_temperature_k(scenario), molar_mass, g)
        record.update(scale_height_m=h, scale_height_over_radius=h / radius, chapman_horizon=chapman_horizon(radius, h),
                      column_mass_kg_m2=column_mass_kg_m2(scenario['air']['surface_pressure_pa'], g))
    if exoplasim is not None:
        cal = calendar(world, exoplasim)
        record.update(calendar=cal, model_day_days=cal['model_day_s'] / DAY_S)
    return record


# The body.

def gravity(world: dict, *, rule: str = 'with-spin') -> float:
    """Surface gravity: GM/R² less the spin term (2/3)Ω²R, the area mean, unless the world states it with its
    basis. `rule` 'gm-over-r2' gives GM/R² alone, the basis of the paper's regime data."""
    body = world['body']
    if rule == 'gm-over-r2':
        return body['gm_m3_s2'] / body['radius_m'] ** 2
    if rule != 'with-spin':
        raise SpecError(f'gravity rule {rule!r}: "with-spin" or "gm-over-r2"')
    return _checked(body.get('gravity_m_s2'), gravity_derived(world), 'gravity_m_s2', world['id'])


def gravity_derived(world: dict) -> float:
    body = world['body']
    return body['gm_m3_s2'] / body['radius_m'] ** 2 - (2.0 / 3.0) * rotation_rate(world) ** 2 * body['radius_m']


def rotation_rate(world: dict) -> float:
    """Ω, rad/s, from the sidereal period."""
    return 2.0 * math.pi / (world['rotation']['sidereal_period_days'] * DAY_S)


def solar_day_days(world: dict) -> float:
    """The solar day: stated with its basis and checked against its derivation, or derived."""
    return _checked(world['rotation'].get('solar_day_days'), solar_day_derived(world), 'solar_day_days', world['id'])


def solar_day_derived(world: dict) -> float:
    return synodic_period_days(world['rotation']['sidereal_period_days'], world['orbit']['sidereal_year_days'])


def synodic_period_days(sidereal_days: float, year_days: float) -> float:
    """1/(1/P_rot − 1/P_year), for prograde rotation."""
    if sidereal_days == year_days:
        raise SpecError('a rotation locked to the year has no solar day; synchronous rotation is a field still to add')
    return 1.0 / (1.0 / sidereal_days - 1.0 / year_days)


def _checked(stated, derived: float, name: str, where: str) -> float:
    if stated is None:
        return derived
    gap = abs(stated - derived) / abs(derived)
    if gap > TOLERANCE[name]:
        raise SpecError(f'{where}: stated {name} {stated} lies {gap:.3g} from its derivation, {derived:.10g}, '
                        f'beyond the tolerance of {TOLERANCE[name]:.3g}')
    return stated


# The air.

def _air(scenario: dict) -> dict:
    """The scenario's air, refused where a field it needs is unchosen, its balance other than N2, or a gas given
    in two forms."""
    air = scenario['air']
    missing = [k for k in ('surface_pressure_pa', 'co2_ppm') if k not in air]
    if missing:
        raise SpecError(f'{scenario["id"]}: the air states no {missing}')
    if air.get('balance') != 'N2':
        raise SpecError(f'{scenario["id"]}: the balance gas is {air.get("balance")!r}; the lab builds N2-balanced air')
    for gas, forms in (('O2', ('o2_partial_pressure_pa', 'o2_mole_fraction')), ('Ar', ('ar_per_n2', 'ar_mole_fraction'))):
        given = [f for f in forms if f in air]
        if len(given) != 1:
            raise SpecError(f'{scenario["id"]}: {gas} is given as {given or "nothing"}; give exactly one of {forms}')
    needed = [k for k in air if k in {'surface_pressure_pa', 'co2_ppm', 'o2_partial_pressure_pa', 'o2_mole_fraction',
                                      'ar_per_n2', 'ar_mole_fraction'}]
    unset = unchosen({k: air[k] for k in needed})
    if unset:
        raise SpecError(f'{scenario["id"]}: the air needs {unset}, which are unchosen')
    return air


def mole_fractions(scenario: dict) -> dict:
    """The dry air's mole fractions: CO2 as ppm of the total, O2 as given, and the rest N2 and Ar, split by
    their ratio or with Ar as given and N2 the balance. Stated gases beyond the total are refused."""
    air = _air(scenario)
    co2 = air['co2_ppm'] / 1e6
    o2 = (air['o2_partial_pressure_pa'] / air['surface_pressure_pa'] if 'o2_partial_pressure_pa' in air
          else air['o2_mole_fraction'])
    rest = 1.0 - o2 - co2
    if 'ar_per_n2' in air:
        n2 = rest / (1.0 + air['ar_per_n2'])
        ar = n2 * air['ar_per_n2']
    else:
        ar = air['ar_mole_fraction']
        n2 = rest - ar
    fractions = dict(N2=n2, O2=o2, Ar=ar, CO2=co2)
    if min(fractions.values()) < 0.0:
        raise SpecError(f'{scenario["id"]}: the stated gases exceed the total pressure, leaving {fractions}')
    return fractions


def partial_pressures_bar(scenario: dict) -> dict:
    """The dry air's partial pressures, bar: each gas's mole fraction of the total."""
    fractions = mole_fractions(scenario)
    total = scenario['air']['surface_pressure_pa'] / 1e5
    return {f'p{gas}': x * total for gas, x in fractions.items()}


def molar_mass_g_mol(fractions: dict) -> float:
    return (fractions['N2'] * MOLAR_MASS['N2'] + fractions['O2'] * MOLAR_MASS['O2']
            + fractions['Ar'] * MOLAR_MASS['Ar'] + fractions['CO2'] * MOLAR_MASS['CO2'])


def zgasw(fractions: dict) -> dict:
    """The mass fractions of CO2 and O2 that PlaSim's ZGASW takes (patch 08): x_i M_i / Σ x_j M_j."""
    molar_mass = molar_mass_g_mol(fractions)
    return {gas: fractions[gas] * MOLAR_MASS[gas] / molar_mass for gas in ('CO2', 'O2')}


def specific_gas_constant(molar_mass: float) -> float:
    """J kg-1 K-1."""
    return R_GAS / (molar_mass / 1000)


def reference_temperature_k(scenario: dict) -> float:
    value = scenario['air']['reference_temperature_k']
    if value == 'settled':
        raise SpecError(f'{scenario["id"]}: its reference temperature is the fixpoint\'s settled global mean, '
                        'which no derivation gives before the GCM has run')
    if value == 'unchosen':
        raise SpecError(f'{scenario["id"]}: its reference temperature is unchosen')
    return value


def scale_height_m(temperature_k: float, molar_mass: float, gravity_m_s2: float) -> float:
    """H = RT/(Mg)."""
    return R_GAS * temperature_k / (molar_mass / 1000 * gravity_m_s2)


def column_mass_kg_m2(pressure_pa: float, gravity_m_s2: float) -> float:
    return pressure_pa / gravity_m_s2


def chapman_horizon(radius_m: float, scale_height: float) -> float:
    """√(πR/2H): the horizon's air mass in an exponential atmosphere, 35 for Earth's air in PlaSim."""
    return math.sqrt(math.pi * radius_m / (2 * scale_height))


# ExoPlaSim's calendar (exoplasim/__init__.py:2609-2622; plasim.f90:1287-1348).

def exoplasim_rotationperiod_days(world: dict) -> float:
    """1 for a world whose solar day is stated as exactly one day, which keeps PlaSim's 24-hour path, and the
    sidereal period otherwise (world_spec.md, rule 7). A sidereal period of exactly one day would take that
    path unasked, and is refused."""
    stated = world['rotation'].get('solar_day_days')
    if stated == 1.0 and solar_day_days(world) == 1.0:
        return 1.0
    period = world['rotation']['sidereal_period_days']
    if period == 1.0:
        raise SpecError(f'{world["id"]}: a sidereal period of exactly 1 d takes ExoPlaSim\'s 24-hour path; '
                        'state the solar day as 1 d with its basis, or give the period its own digits')
    return period


def days_per_year(rotationperiod: float, year_days: float) -> int:
    """N_DAYS_PER_YEAR as ExoPlaSim's configure writes it."""
    if rotationperiod == 1.0:
        return int(year_days)
    return max(int(360.0 / rotationperiod / 12 + 0.5), 1) * 12


def model_day_days(rotationperiod: float, n_days: int) -> float:
    """PlaSim's solar_day, in days: one day at a rotation period of 1, otherwise P·N/(N − 1), or P where N is 1
    (plasim.f90:1287-1300)."""
    if rotationperiod == 1.0:
        return 1.0
    return rotationperiod * n_days / (n_days - 1) if n_days != 1 else rotationperiod


def plasim_step_s(timestep_min: float) -> float:
    """The time step PlaSim runs: it rounds the steps of a 24-hour day to an even count and divides the day by
    them (plasim.f90:1343-1347)."""
    per_day = _nint(DAY_S) // _nint(timestep_min * 60)
    per_day += per_day % 2
    return DAY_S / per_day


def steps_per_model_day(model_day_s: float, timestep_min: float) -> int:
    """ntspd = nint(solar_day) ÷ nint(mpstep·60), as an integer division (plasim.f90:1348)."""
    steps = _nint(model_day_s) // _nint(plasim_step_s(timestep_min))
    if steps < 1:
        raise SpecError(f'a model day of {model_day_s} s holds no time step of {timestep_min} min')
    return steps


def configure_year_steps(timestep_min: float) -> int:
    """The run steps ExoPlaSim's configure writes for a rotation period other than 1: a 360-day year."""
    return max(1, int(round(360.0 * 1440.0 / timestep_min + 0.49999)))


def output_steps(mean_interval_days: float, model_day_s: float, steps: int, n_days: int) -> int:
    """NSTPW, so that whole means fill each model day and each year: below a model day, the divisor of the
    model day's steps whose mean lies nearest the interval; from a model day up, the divisor of the year's
    model days nearest it, the shorter at a tie."""
    interval = mean_interval_days * DAY_S
    if interval < model_day_s:
        means = min((m for m in range(1, steps + 1) if steps % m == 0), key=lambda m: (abs(model_day_s / m - interval), m))
        return steps // means
    days = min((d for d in range(1, n_days + 1) if n_days % d == 0), key=lambda d: (abs(d * model_day_s - interval), d))
    return steps * days


def calendar(world: dict, defaults: dict) -> dict:
    """ExoPlaSim's calendar for a world under its defaults."""
    rotationperiod = exoplasim_rotationperiod_days(world)
    n_days = days_per_year(rotationperiod, world['orbit']['sidereal_year_days'])
    day_s = model_day_days(rotationperiod, n_days) * DAY_S
    step_s = plasim_step_s(defaults['timestep_min'])
    steps = steps_per_model_day(day_s, defaults['timestep_min'])
    per_mean = output_steps(defaults['mean_interval_days'], day_s, steps, n_days)
    if defaults['whole_model_days']:
        run_steps = n_days * steps
    elif rotationperiod != 1.0:
        run_steps = configure_year_steps(defaults['timestep_min'])
    else:
        raise SpecError(f'{world["id"]}: the lab runs a one-day rotation in whole model days')
    # In whole model days the output rule makes the means fill the year; configure's 360-day year slips
    # against them, as the paper's calendar records, and its means then fall short of a whole count.
    return dict(rotationperiod=rotationperiod, n_days_per_year=n_days, model_day_s=day_s, step_s=step_s,
                steps_per_model_day=steps, stepped_model_day_s=steps * step_s, steps_per_mean=per_mean,
                run_steps_per_year=run_steps, means_per_year=run_steps / per_mean,
                whole_means=run_steps % per_mean == 0)


def sun_clock_sweep_deg(stepped_model_day_days: float, rotationperiod: float) -> float:
    """The turn PlaSim's own Sun clock makes in a model day: 360 × model day / rotation period (defect log A1)."""
    return 360 * stepped_model_day_days / rotationperiod


def sun_clock_skip_deg(n_days: int) -> float:
    """The clock's skip back each model day, 1/(N − 1) of a turn."""
    return 360.0 / (n_days - 1)


def advective_limit_wind_m_s(radius_m: float, truncation: int, timestep_s: float) -> float:
    """The wind above which u·Δt·N/a exceeds 1, the guard on ExoPlaSim's time step."""
    return radius_m / (truncation * timestep_s)


def _nint(x: float) -> int:
    """Fortran's nint: the nearest integer, halves away from zero."""
    return int(math.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)


# CM1.

SCALED_TABLES = {'scaled_length': 'length', 'scaled_time': 'time', 'scaled_rate': 'rate',
                 'capillary': 'capillary', 'diurnal': 'soil'}


def cm1_factors(world: dict, scenario: dict, defaults: dict, *, temperature_k: float | None = None) -> dict:
    """The factors on CM1's scaled values (world_spec.md, rule 9): lengths by H/H_ref, times by (H/c)/(H/c)_ref
    and rates by its inverse, with H = RT/(Mg) and c = (RT/M)^½ at the scenario's reference temperature, or at
    `temperature_k`, the fixpoint's, where given; raindrop limits by the capillary factor, soil layers by the
    soil factor. The reference state is derived from the defaults' [reference] as a scenario's is, so that a
    case at that state scales by 1."""
    ref = defaults['reference']
    m_ref = molar_mass_g_mol(mole_fractions({'id': 'cm1/defaults [reference]', 'air': ref['air']}))
    h_ref = scale_height_m(ref['temperature_k'], m_ref, ref['gravity_m_s2'])
    c_ref = math.sqrt(R_GAS * ref['temperature_k'] / (m_ref / 1000))
    g = gravity(world)
    t = reference_temperature_k(scenario) if temperature_k is None else temperature_k
    m = molar_mass_g_mol(mole_fractions(scenario))
    h, c = scale_height_m(t, m, g), math.sqrt(R_GAS * t / (m / 1000))
    time = (h / c) / (h_ref / c_ref)
    return dict(length=h / h_ref, time=time, rate=1.0 / time, capillary=capillary_factor(g),
                soil=soil_factor(solar_day_days(world)))


def cm1_values(settings: dict, factors: dict, *, set_paths: frozenset = frozenset()) -> dict:
    """A case's scaled values: each field of its scaled tables times its factor, unless the case's chain sets it,
    when it stands as set (rule 9). The raindrop limits follow the case's
    `physics.rain_size_limits`: `earth` keeps Morrison's own, `breakup-only` scales the breakup diameter alone."""
    limits = settings['physics']['rain_size_limits']
    out = {}
    for table, factor_name in SCALED_TABLES.items():
        for name, value in settings[table].items():
            if name in out:
                raise SpecError(f'{name!r} appears in two of the scaled tables')
            factor = factors[factor_name]
            if table == 'capillary' and (limits == 'earth' or (limits == 'breakup-only' and name != 'breakup_diameter_m')):
                factor = 1.0
            out[name] = value if f'{table}.{name}' in set_paths else value * factor
    return out


def capillary_factor(gravity_m_s2: float, earth_gravity: float = CM1_EARTH_G) -> float:
    """(g_Earth/g)^½: the largest stable raindrop's size against Earth's, at the Earth gravity Morrison's
    values were set at, CM1's 9.81 m/s²."""
    return math.sqrt(earth_gravity / gravity_m_s2)


def soil_factor(solar_day: float) -> float:
    """(solar day in days)^½: the depth the day's heat reaches, against Earth's."""
    return math.sqrt(solar_day)


def declination_deg(obliquity_deg: float, solar_longitude_deg: float) -> float:
    return math.degrees(math.asin(math.sin(math.radians(obliquity_deg)) * math.sin(math.radians(solar_longitude_deg))))


def sunrise_hour_angle_deg(latitude_deg: float, declination: float) -> float:
    """−acos(−tan φ tan δ): −90° at the equinox. In polar day and polar night the Sun neither rises nor sets,
    and a case that starts at sunrise is refused there."""
    x = -math.tan(math.radians(latitude_deg)) * math.tan(math.radians(declination))
    if not -1.0 < x < 1.0:
        raise SpecError(f'at latitude {latitude_deg} and declination {declination} the Sun neither rises nor sets')
    return -math.degrees(math.acos(x)) + 0.0


def ring_grid(radius_m: float, latitude_deg: float, column_target_m: float, ranks: int) -> dict:
    """A ring on a circle of latitude: its length, and its columns, a multiple of the ranks
    (Terluna climate/crm/cm1_run.py:2051-2056)."""
    length = 2.0 * math.pi * radius_m * math.cos(math.radians(latitude_deg))
    nx = int(round(length / column_target_m / ranks)) * ranks
    if nx < ranks:
        raise SpecError(f'a ring at {latitude_deg}° holds fewer columns of {column_target_m} m than its {ranks} ranks')
    return dict(length_m=length, nx=nx, dx_m=length / nx)


def coriolis(omega: float, latitude_deg: float) -> float:
    return 2.0 * omega * math.sin(math.radians(latitude_deg))
