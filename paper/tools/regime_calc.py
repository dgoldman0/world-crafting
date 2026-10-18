"""Every number the paper calculates from stated constants; model results come from the runs.

    python3 paper/tools/regime_calc.py      # writes paper/data/regime_calc.json and prints it

Constants are Terluna's shared/constants.json at 186b294 (Moon radius and GM, the months, Earth's sidereal
day) and the design air of climate/gcm/boundary.py (1.2 atm at the water level, Earth's O2 partial pressure,
Earth's Ar/N2 ratio, 400 ppm CO2, N2 the balance). Each entry names its formula. These are calculations: they
hold for the stated idealisations (an isothermal or exponential atmosphere where named) and say nothing about
what the models do.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'data' / 'regime_calc.json'
PROFILE = (Path(__file__).resolve().parents[2] / 'python' / 'atmosphere' / 'middle_atmosphere' / 'results'
           / 'profiles' / 'moon_1.2atm_titania_stack.csv')

G0 = 9.80665                      # standard gravity, m/s2
CM1_G_EARTH = 9.81                # CM1's and Morrison's Earth gravity
R_GAS = 8.314462618               # J/mol/K
MOON_R = 1_737_400.0              # m
MOON_GM = 4.902800118e12          # m3/s2
MOON_SIDEREAL_D = 27.321661
MOON_SYNODIC_D = 29.53059
EARTH_R = 6_371_000.0
EARTH_SIDEREAL_S = 86164.0905
DAY_S = 86400.0
P_EARTH = 101_325.0
P_MOON = 1.2 * P_EARTH            # 121,590 Pa at the water level
P_O2 = 21_227.0                   # Earth's O2 partial pressure, Pa
AR_PER_N2 = 0.00934 / 0.78084     # Earth's ratio
CO2 = 400e-6
M = dict(N2=28.0134, O2=31.9988, Ar=39.948, CO2=44.0095)   # g/mol
M_EARTH_AIR = 28.9647
T_MOON_S = 295.0                  # design-case surface, K
T_EARTH_S = 288.0
PLASIM_STEP_S = 1800.0
PLASIM_MODEL_DAY_STEPS = 1430
PLASIM_YEAR_STEPS = 17280         # ExoPlaSim's 360-day year
RRTMG_P_TOP_OF_TABLE_HPA = 1053.63


def g_moon(z: float = 0.0) -> float:
    return MOON_GM / (MOON_R + z) ** 2


def main() -> dict:
    gm = g_moon()
    out: dict = {'about': __doc__.strip().splitlines()[0]}

    # Design air
    x_o2 = P_O2 / P_MOON
    x_n2 = (1 - x_o2 - CO2) / (1 + AR_PER_N2)
    x_ar = x_n2 * AR_PER_N2
    m_air = x_n2 * M['N2'] + x_o2 * M['O2'] + x_ar * M['Ar'] + CO2 * M['CO2']
    out['air'] = dict(o2_fraction=x_o2, n2_fraction=x_n2, ar_fraction=x_ar, molar_mass_g_mol=m_air,
                      formula='mole fractions from partial pressures; M = sum x_i M_i')

    # Gravity and column mass
    col_moon = P_MOON / gm
    col_earth = P_EARTH / G0
    out['gravity'] = dict(moon_surface_m_s2=gm, ratio_to_standard=gm / G0, ratio_to_cm1_earth=gm / CM1_G_EARTH,
                          formula='g = GM/R^2')
    out['column_mass'] = dict(moon_kg_m2=col_moon, earth_kg_m2=col_earth, ratio=col_moon / col_earth,
                              formula='p_s / g_s (constant gravity)')

    # Scale heights, H/R, horizon air mass (Chapman's grazing-incidence factor for an exponential atmosphere)
    h_moon = R_GAS * T_MOON_S / (m_air / 1000 * gm)
    h_earth = R_GAS * T_EARTH_S / (M_EARTH_AIR / 1000 * G0)
    out['scale_height'] = dict(moon_km=h_moon / 1e3, earth_km=h_earth / 1e3, moon_T_K=T_MOON_S, earth_T_K=T_EARTH_S,
                               moon_over_radius=h_moon / MOON_R, earth_over_radius=h_earth / EARTH_R,
                               ratio_of_ratios=(h_moon / MOON_R) / (h_earth / EARTH_R),
                               formula='H = R T / (M g)')
    out['horizon_air_mass_chapman'] = dict(moon=math.sqrt(math.pi * MOON_R / (2 * h_moon)),
                                           earth=math.sqrt(math.pi * EARTH_R / (2 * h_earth)),
                                           formula='sqrt(pi R / 2H), exponential atmosphere')

    # Twilight: the Sun's depression one Earth day after sunset, the geometric shadow height above a place,
    # and the share of an isothermal column's mass above it
    dep = 360.0 / MOON_SYNODIC_D
    shadow = MOON_R * (1 / math.cos(math.radians(dep)) - 1)
    out['one_day_after_sunset'] = dict(sun_depression_deg=dep, shadow_height_km=shadow / 1e3,
                                       mass_above_isothermal=math.exp(-shadow / h_moon),
                                       formula='h = R (sec d - 1); mass above exp(-h/H), refraction ignored')

    # Shell geometry and gravity with height
    out['shell'] = dict(area_ratio_at_50km=((MOON_R + 50e3) / MOON_R) ** 2,
                        g_drop_at_48_6km=1 - g_moon(48.6e3) / gm, g_drop_at_86km=1 - g_moon(86e3) / gm,
                        g_drop_at_100km=1 - g_moon(100e3) / gm, g_drop_at_150km=1 - g_moon(150e3) / gm,
                        formula='(r/R)^2; g(z) = GM/(R+z)^2')
    # Air per unit area of a constant-area column whose gravity falls as GM/r^2, against p_s/g_s, for an
    # exponential density profile with the surface scale height (numerical integral to 1,000 km)
    dz, num, den = 100.0, 0.0, 0.0
    for i in range(10000):
        z = (i + 0.5) * dz
        rho = math.exp(-z / h_moon)
        num += rho * dz
        den += rho * (MOON_R / (MOON_R + z)) ** 2 * dz
    # The same from the reference model's design column (python/atmosphere/middle_atmosphere/results/profiles/
    # moon_1.2atm_titania_stack.csv: 100 layers to 0.1 Pa, heights with g(z)), whose cooling with height
    # shortens the scale height aloft; layer masses dp/g(z) with interfaces at the layers' geometric means
    rows = list(csv.DictReader(PROFILE.open()))
    p = [float(r['p_pa']) for r in rows]
    z = [float(r['z_km']) * 1e3 for r in rows]
    edges = [P_MOON] + [math.sqrt(p[i] * p[i + 1]) for i in range(len(p) - 1)] + [0.0]
    mass = [(edges[i] - edges[i + 1]) / g_moon(z[i]) for i in range(len(p))]
    out['column_with_falling_gravity'] = dict(
        exponential=num / den, design_profile=sum(mass) / (P_MOON / gm),
        design_profile_mass_mean_height_km=sum(m * h for m, h in zip(mass, z)) / sum(mass) / 1e3,
        formula='int rho dz / int rho (R/r)^2 dz for an exponential rho; sum(dp/g(z)) / (p_s/g_s) for the profile')
    # The share of the design column's air above the geometric shadow one Earth day after sunset
    above = sum(m for m, h in zip(mass, z) if h > shadow)
    out['one_day_after_sunset']['mass_above_design_profile'] = above / sum(mass)
    out['constant_g_height_error'] = {f'{h:.0f}km': 1 - MOON_R / (MOON_R + h * 1e3) for h in (86, 150)}
    out['constant_g_height_error']['formula'] = 'z_const = R z/(R+z): heights from geopotential at surface g'

    # Gravity's scalings
    rg = gm / CM1_G_EARTH
    out['fall_speed_slowdown'] = {name: 1 / rg ** ((b + 1) / 3) for name, b in
                                  (('cloud_droplets_B2', 2.0), ('rain_B0.8', 0.8), ('graupel_B0.37', 0.37))}
    out['fall_speed_slowdown']['formula'] = 'V proportional to g^((B+1)/3) at fixed size; CM1 reference 9.81'
    out['sea'] = dict(charnock_roughness_ratio=G0 / gm, deep_water_speed_ratio=math.sqrt(gm / G0),
                      formula='z0 = a u*^2/g; c = sqrt(g L / 2 pi)')
    out['capillary_length_ratio'] = dict(value=math.sqrt(G0 / gm), formula='sqrt(sigma/(rho_w g)), lunar over Earth')

    # Rotation and the day
    omega = 2 * math.pi / (MOON_SIDEREAL_D * DAY_S)
    f80 = 2 * omega * math.sin(math.radians(80))
    out['rotation'] = dict(omega_s=omega, coriolis_80deg_s=f80, inertial_period_days=2 * math.pi / f80 / DAY_S,
                           formula='f = 2 Omega sin(lat); 2 pi / f')
    out['soil_wave_depth_ratio'] = dict(value=math.sqrt(MOON_SYNODIC_D), formula='depth proportional to sqrt(period)')

    # PlaSim's calendar and its Sun clock
    model_day_d = PLASIM_MODEL_DAY_STEPS * PLASIM_STEP_S / DAY_S
    sweep = 360 * model_day_d / MOON_SIDEREAL_D
    earth_sweep = 360 * DAY_S / EARTH_SIDEREAL_S
    out['plasim_calendar'] = dict(model_day_days=model_day_d,
                                  model_days_per_360d_year=PLASIM_YEAR_STEPS / PLASIM_MODEL_DAY_STEPS,
                                  slip_steps_per_year=PLASIM_YEAR_STEPS - 12 * PLASIM_MODEL_DAY_STEPS,
                                  slip_days_per_year=(PLASIM_YEAR_STEPS - 12 * PLASIM_MODEL_DAY_STEPS) * PLASIM_STEP_S / DAY_S,
                                  formula='1,430 half-hour steps a model day; 17,280 steps a 360-day year')
    out['sun_clock_skip'] = dict(moon_sweep_deg=sweep, moon_skip_deg=sweep - 360,
                                 earth_sweep_deg=earth_sweep, earth_skip_deg=earth_sweep - 360,
                                 formula='360 x model day / rotation period, then back to the clock start')
    out['slingo_cover_bias'] = dict(model_day=0.125 * math.log(model_day_d), formula='0.125 ln(day / 1 d)')

    # ExoPlaSim's count of rotations per 360-day year, its model day, and the true solar day, for slow rotators
    # (exoplasim/__init__.py: N = max(int(360/P/12 + 0.5), 1) * 12; plasim.f90: solar_day = sidereal_day N/(N-1))
    slow = {}
    for period in (2.0, 10.0, 16.0, 20.0, 21.0, 27.321661, 64.0, 243.0):
        n = max(int(360.0 / period / 12 + 0.5), 1) * 12
        slow[f'{period:g}d'] = dict(N=n, skip_deg=360.0 / (n - 1), model_day_days=period * n / (n - 1),
                                    solar_day_days=1.0 / (1.0 / period - 1.0 / 365.25))
    out['exoplasim_slow_rotators'] = slow
    out['exoplasim_slow_rotators']['formula'] = ('N = max(int(360/P/12 + 0.5), 1) x 12; skip 1/(N-1) turn; model day '
                                                 'P N/(N-1); solar day 1/(1/P - 1/365.25) for prograde rotation')

    # The convective-cover unit in ExoPlaSim's synchronous runs. configure(synchronous=True) sets only NFIXED and
    # FIXEDLON (exoplasim/__init__.py 2628-2630); the rotation period sets ROTSPD and N as for any run (2616-2619),
    # so plasim.f90 1296-1300 gives solar_day = P N/(N-1), and rainmod.f90 1890 converts rain with it
    # (zrfac = solar_day * 1000), biasing Slingo's cover by 0.125 ln(model day / 1 d), capped at 0.8.
    sync = {}
    for name, period in (('TRAPPIST-1e', 6.0996), ('Proxima Centauri b', 11.1868)):
        n = max(int(360.0 / period / 12 + 0.5), 1) * 12
        day = period * n / (n - 1)
        sync[name] = dict(rotation_period_days=period, N=n, model_day_days=day, cover_bias=0.125 * math.log(day))
    out['exoplasim_synchronous_cover_bias'] = sync
    out['exoplasim_synchronous_cover_bias']['formula'] = ('synchronous runs keep N = max(int(360/P/12 + 0.5), 1) x 12 '
                                                          'and model day P N/(N-1); cover bias 0.125 ln(model day / 1 d)')

    # Retention: the atmosphere's mass against the design's loss rates over a solar cycle (Terluna
    # research/decisions.md 125: 0.61-0.80 kg/s in the cooler titania cases, 1.4 kg/s in the warmest, without magnets),
    # as the time each loss would take to remove the whole atmosphere (column at constant g; the shells' 11.5% more
    # air lengthens it)
    mass = col_moon * 4 * math.pi * MOON_R ** 2
    year_s = 365.25 * 86400
    out['retention'] = dict(atmosphere_mass_kg=mass,
                            removal_time_years={f'{q:g} kg/s': mass / q / year_s for q in (0.61, 0.80, 1.0, 1.4)},
                            formula='M = (p_s/g_s) 4 pi R^2; t = M / loss rate')
    out['shell']['area_ratio_at_48_6km'] = ((MOON_R + 48.6e3) / MOON_R) ** 2

    # Earth's average flash density from the Optical Transient Detector's global rate (Christian et al. 2003: 44
    # flashes a second) over Earth's surface, against the lunar electrified box's 0.022 per km2 per year
    earth_area_km2 = 4 * math.pi * (EARTH_R / 1e3) ** 2
    fd = 44.0 * year_s / earth_area_km2
    out['flash_density'] = dict(earth_per_km2_yr=fd, lunar_box_per_km2_yr=0.022, ratio=0.022 / fd,
                                formula='44 flashes/s x seconds per year / Earth surface area')

    # RRTMG's table edge: depth of the lunar air below 1053.63 hPa at the water level
    p_hpa = P_MOON / 100
    out['rrtmg_extrapolated_depth_km'] = {f'{t:.0f}K': R_GAS * t / (m_air / 1000 * gm) * math.log(
        p_hpa / RRTMG_P_TOP_OF_TABLE_HPA) / 1e3 for t in (290.0, 295.0)}
    out['rrtmg_extrapolated_depth_km']['formula'] = 'H ln(p_s / 1053.63 hPa), dry air at 1,215.9 hPa'
    return out


if __name__ == '__main__':
    result = main()
    OUT.write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps(result, indent=1))
