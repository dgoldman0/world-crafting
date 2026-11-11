"""The size-dependent fall law of a world's rain for CM1's Morrison scheme, and the rate of rain's self-collection on
that world: the table and the rate that patch 04 of the lab's CM1 series reads.

    from atmosphere.radiative_convective.thermodynamics import earthlike_air
    from atmosphere.rain import drops, fall_law
    world = drops.Column(gravity_m_s2=1.6242, surface_pressure_pa=121590.0, surface_temperature_k=300.4,
                         surface_relative_humidity=0.61, air=earthlike_air(121590.0, 400.0))
    found = fall_law.settings(world)                  # about two seconds on one thread
    found['namelist']                                 # the entries of &param3
    fall_law.table_text(found['table'])               # the text of lab_rain_law.txt

Morrison's scheme gives rain one fall law, V = A (RHOSU / rho)^0.54 D^B with A = 842 m^0.2/s and B = 0.8 on Earth, and
core patch 04 slows it at every size by (g / 9.81)^((B + 1) / 3), 2.94 times at the Moon's gravity. The single-drop
solver (drops.py) slows each size by its own factor, there from 5.3 at 0.1 mm to 1.9 at 6 mm. The scheme reads its law
only through three moments of rain's exponential spectrum N0 exp(-lambda D): the mass-weighted and the number-weighted
mean fall speeds, A Gamma(4 + B) / 6 lambda^-B and A Gamma(1 + B) lambda^-B, by which its water and its drops fall,
and the integral that ventilates its evaporation, A^(1/2) Gamma(5/2 + B/2) lambda^-(5/2 + B/2). One exponent serves
either the viscous fall of drizzle or the inertial fall of large drops: the closest power law of Terluna's search
stood off the solver's mass-weighted speed by up to 27% and its number-weighted speed by up to a factor of two. This
law takes the three moments from the solver itself and tabulates them in log lambda over the scheme's range. The
speeds are the solver's terminal speeds in the world's air at 2 m, continued below the smallest size solved by
Stokes's D^2 and beyond the stability screen at the screen's speed, and divided by Morrison's density factor there, so
that the scheme's own factor gives them back.

Rain's self-collection, 5.78 m3/kg/s in the scheme (Seifert and Beheng 2001), scales with the gravitational collision
kernel pi/4 (D1 + D2)^2 |V1 - V2|. A world's rate is Earth's over the ratio of the kernels in Earth's air and the
world's, summed over pairs of the spectrum at the world's breakup equilibrium (breakup.limits) from the scheme's
smallest rain, 80 um, to the smaller of the two stability screens, the sizes at which both worlds keep drops.
Autoconversion and accretion stay Earth's fits here; warm_rain.py gives the factors that patch 05 of the series puts
on them.

Evidence. A runnable calculation: the solver's terminal speeds, which reproduce Earth's measured fall speeds to
0.20 m/s, in the world's air at 2 m, integrated over Morrison's exponential spectra. The quadrature reproduces the
closed forms of a power law to within 3e-6. The self-collection rate scales Seifert and Beheng's Earth constant by the
ratio of geometric collision kernels with collision efficiency 1; no collision has been measured at another gravity.

Assumptions and limits. The speeds are the solver's at 2 m, at one temperature and humidity; at each level above, the
scheme multiplies them by its density factor (RHOSU / rho)^0.54 alone. Below 1 um the speeds follow Stokes's D^2;
beyond the stability screen, where Morrison's untruncated spectrum still places mass, they keep the screen's speed,
the largest drop's. The table spans mean diameters from 10 um to 10 mm, and the scheme reads its end values beyond
them; the scheme's cap on the mean diameter, 2.8 mm (9.81 / g)^(1/2) with the lab's patch 03, exceeds 10 mm below
0.77 m/s2. The solver bounds drops at 30 mm, which the stability screen exceeds below about 0.48 m/s2, and takes a
ground between 273.15 and 313.15 K with air of N2, O2, Ar and CO2.

From Terluna's atmosphere/rain/fall_law.py at 39c5ee04 (domain/climate 5a44e5e), whose product builder, bound to
Terluna's resort climate and its breakup product, stays there with its search for the closest power law.
solved_speeds, speed_law, power_law, moments, closed_forms, table_lambda, interpolate and kernel_sum are Terluna's;
table, self_collection and settings give its calculation for any world, and table_text writes the table as Terluna's
runner does (climate/crm/cm1_run.py, rain_law_settings).
"""
from __future__ import annotations

import math

import numpy as np

from atmosphere.rain import breakup, drops, morrison

SOLVED_POINTS, SMALLEST_SOLVED_M, SCREEN_MARGIN = 400, 1.0e-6, 0.998
QUADRATURE_POINTS, QUADRATURE_M = 8000, (1.0e-8, 1.0)   # the log grid the spectra are integrated over
TABLE_LAMBDA = (100.0, 1.0e5, 301)                 # 1/m, uniform in log: mean diameters from 10 mm to 10 um
SMALLEST_RAIN_M = 80.0e-6                          # Seifert and Beheng's rain, drops above 2.6e-10 kg
KERNEL_POINTS = 600
TABLE_FILE = 'lab_rain_law.txt'                    # the name by which patch 04 opens the table in a run's folder


def solved_speeds(column):
    """The solver's still-air terminal speeds at 2 m on a log grid from 1 um to just below the stability screen."""
    screen = drops.stable_diameter(column)
    diameter = np.geomspace(SMALLEST_SOLVED_M, SCREEN_MARGIN * screen, SOLVED_POINTS)
    return diameter, np.array([drops.terminal_speed(d, column) for d in diameter]), screen


def speed_law(diameter, speed):
    """Speed (m/s) at any diameter (m): the solved speeds interpolated in log-log, Stokes's D^2 below the smallest and
    the largest's speed beyond."""
    ld, lv = np.log(diameter), np.log(speed)

    def law(d):
        x = np.log(np.asarray(d, float))
        return np.exp(np.where(x < ld[0], lv[0] + 2.0 * (x - ld[0]), np.interp(x, ld, lv)))

    return law


def power_law(a, b):
    return lambda d: a * np.asarray(d, float)**b


GRID = np.geomspace(*QUADRATURE_M, QUADRATURE_POINTS)
LOG_STEP = math.log(QUADRATURE_M[1] / QUADRATURE_M[0]) / (QUADRATURE_POINTS - 1)


def moments(speed, lam, chunk=40):
    """Morrison's three moments of a fall law speed(D) for rain's exponential spectrum of slope lam (1/m): the
    mass-weighted and the number-weighted mean speeds (m/s) and the ventilation integral of D^(3/2) V^(1/2)
    exp(-lam D) dD (m3 s^-1/2), by the trapezoid rule in ln D."""
    lam = np.atleast_1d(np.asarray(lam, float))
    v = speed(GRID)
    parts = (GRID**3 * v, v, GRID**1.5 * np.sqrt(v))
    out = np.empty((3, lam.size))
    for start in range(0, lam.size, chunk):
        part = lam[start:start + chunk, None]
        weight = np.exp(-part * GRID) * GRID * LOG_STEP
        weight[:, (0, -1)] *= 0.5
        mass, number, vent = (weight @ f for f in parts)
        out[:, start:start + chunk] = (mass * part[:, 0]**4 / 6.0, number * part[:, 0], vent)
    return out


def closed_forms(a, b, lam):
    """The same moments of the power law a D^b, in closed form."""
    lam = np.asarray(lam, float)
    return np.array([a * math.gamma(4 + b) / 6 * lam**-b, a * math.gamma(1 + b) * lam**-b,
                     math.sqrt(a) * math.gamma(2.5 + b / 2) * lam**-(2.5 + b / 2)])


def table_lambda():
    first, last, points = TABLE_LAMBDA
    return np.geomspace(first, last, points)


def interpolate(table, lam):
    """The table's moments at lam, linear in ln lambda and held at its ends, as the patched scheme reads it."""
    x = (np.log(lam) - table['ln_lambda_first']) / table['ln_lambda_step']
    rows = np.array([table['ln_mass_weighted'], table['ln_number_weighted'], table['ln_ventilation']])
    i = np.clip(np.floor(x).astype(int), 0, rows.shape[1] - 2)
    w = np.clip(x - i, 0.0, 1.0)
    return np.exp((1.0 - w) * rows[:, i] + w * rows[:, i + 1])


def kernel_sum(speed, mean_m, smallest_m, largest_m, points=KERNEL_POINTS):
    """Collisions per unit time and volume among an exponential spectrum's drops, per N0^2: the geometric kernel
    pi/4 (D1 + D2)^2 |V1 - V2| over pairs of sizes from smallest_m to largest_m."""
    d = np.geomspace(smallest_m, largest_m, points)
    w = np.exp(-d / mean_m) * np.gradient(d)
    v = speed(d)
    kernel = np.pi / 4 * (d[:, None] + d[None, :])**2 * np.abs(v[:, None] - v[None, :])
    return 0.5 * float(w @ kernel @ w)


def table(column):
    """The fall-law table of a world's air at 2 m, as patch 04 reads it: on ln lambda from ln_lambda_first in steps of
    ln_lambda_step (lambda in 1/m), the natural logs of the mass-weighted and number-weighted mean fall speeds (m/s)
    and of the ventilation integral (the integral of D^(3/2) V^(1/2) exp(-lambda D) dD, m3 s^-1/2) of rain's
    exponential spectrum in Morrison's reference air. The scheme multiplies the speeds by its density factor and the
    integral by that factor's square root, and interpolates linearly in ln lambda (interpolate)."""
    factor = morrison.density_factor(column.state(0.0)['density_kg_m3'])
    d, v, _ = solved_speeds(column)
    found = moments(speed_law(d, v / factor), table_lambda())
    first, last, points = TABLE_LAMBDA
    return dict(ln_lambda_first=math.log(first), ln_lambda_step=math.log(last / first) / (points - 1), points=points,
                ln_mass_weighted=[float(x) for x in np.log(found[0])],
                ln_number_weighted=[float(x) for x in np.log(found[1])],
                ln_ventilation=[float(x) for x in np.log(found[2])])


def table_text(table):
    """The table as CM1 reads it from TABLE_FILE in a run's folder: the count of its rows with the first ln lambda and
    the step, then a row of the three logs for each lambda."""
    rows = zip(table['ln_mass_weighted'], table['ln_number_weighted'], table['ln_ventilation'])
    return (f"{table['points']} {table['ln_lambda_first']:.9e} {table['ln_lambda_step']:.9e}\n"
            + ''.join(f'{a:.9e} {b:.9e} {c:.9e}\n' for a, b, c in rows))


def self_collection(column, earth, mean_diameter_m):
    """Rain's self-collection on a world: Earth's kernel over the world's for an exponential spectrum of a mean
    diameter, over pairs from 80 um to the smaller of the two stability screens, each in its own air at 2 m, and the
    rate that ratio leaves of the scheme's 5.78 m3/kg/s, rounded to four decimals as the namelist takes it."""
    d, v, screen = solved_speeds(column)
    ed, ev, earth_screen = solved_speeds(earth)
    largest = min(screen, earth_screen)
    ratio = (kernel_sum(speed_law(ed, ev), mean_diameter_m, SMALLEST_RAIN_M, largest)
             / kernel_sum(speed_law(d, v), mean_diameter_m, SMALLEST_RAIN_M, largest))
    return dict(kernel_ratio=ratio, rate_m3_kg_s=round(morrison.SELF_COLLECTION / ratio, 4),
                mean_diameter_m=mean_diameter_m, smallest_m=SMALLEST_RAIN_M, largest_m=largest)


def settings(column):
    """What a CM1 case takes for the rain of a world, from the world's air at 2 m (a drops.Column): the entries of
    &param3 for patches 03 and 04 of the lab's CM1 series, the limits they give, the breakup scale behind the density
    exponent, the self-collection rate with its kernel ratio, the fall-law table and the air it was computed in.

    brkup_rhor is the column's surface pressure over 1013.25 hPa and brkup_rhoexp the exponent of
    breakup.density_exponent, each rounded as Terluna's runner rounds it, 0 where the world's air has Earth's density;
    brkup_db stays CM1's own 300 um, which the patch scales. A case whose surface pressure differs from the column's
    takes its own brkup_rhor (breakup.limits). The exponent is fitted on the ratio of the two airs' densities, which
    the pressure ratio equals for dry air of Earth's molar mass alone: the breakup scale the patch sets from the two
    entries is 0.2% above the collisions' own in the Open Moon's air, and up to 1.5% from it in air of 10% or 35%
    oxygen (models/cm1/README.md, the limits; tests/test_rain_fall_law.py)."""
    earth = breakup.earth_column(column)
    found = breakup.density_exponent(column, earth)
    exponent = 0.0 if found['alpha'] is None else round(found['alpha'], 3)
    ratio = round(column.surface_pressure_pa / breakup.ATMOSPHERE_PA, 4)
    limits = breakup.limits(column.gravity_m_s2, ratio, exponent)
    rate = self_collection(column, earth, limits['equilibrium_m'])
    state = column.state(0.0)
    d, v, screen = solved_speeds(column)
    return dict(
        namelist=dict(brkup_db=morrison.BREAKUP_CUTOFF, brkup_gscale=1, brkup_rhor=ratio, brkup_rhoexp=exponent,
                      rain_fall_law=1, rain_selfcoll=rate['rate_m3_kg_s']),
        limits=limits, breakup=found, self_collection=rate, table=table(column),
        air=dict(gravity_m_s2=column.gravity_m_s2, pressure_pa=state['pressure_pa'],
                 temperature_k=state['temperature_k'], relative_humidity=state['relative_humidity'],
                 density_kg_m3=state['density_kg_m3'],
                 density_factor=morrison.density_factor(state['density_kg_m3']),
                 stability_screen_m=screen, screen_speed_m_s=float(v[-1])))
