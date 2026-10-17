"""Every number the paper calculates from stated constants; model results come from the runs.

    python3 paper/tools/regime_calc.py      # writes paper/data/regime_calc.json and prints it

Constants are Terluna's shared/constants.json at 186b294 (Moon radius and GM, the months, Earth's sidereal
day) and the design air of climate/gcm/boundary.py (1.2 atm at the water level, Earth's O2 partial pressure,
Earth's Ar/N2 ratio, 400 ppm CO2, N2 the balance). Each entry names its formula. These are calculations: they
hold for the stated idealisations (an isothermal or exponential atmosphere where named) and say nothing about
what the models do.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'data' / 'regime_calc.json'

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
    out['column_with_falling_gravity'] = dict(mass_over_ps_over_gs=num / den,
                                              formula='int rho dz / int rho (R/r)^2 dz, exponential rho')

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
