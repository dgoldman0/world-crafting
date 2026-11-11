"""Raindrop breakup at a world's gravity: the size scale by which the rain limits of CM1's Morrison scheme follow a
world's gravity and air, and the limits as patch 03 of the lab's CM1 series computes them from its namelist.

    from atmosphere.radiative_convective.thermodynamics import earthlike_air
    from atmosphere.rain import breakup, drops
    world = drops.Column(gravity_m_s2=1.6242, surface_pressure_pa=121590.0, surface_temperature_k=300.4,
                         surface_relative_humidity=0.61, air=earthlike_air(121590.0, 400.0))
    found = breakup.density_exponent(world)                              # about a second on one thread
    breakup.limits(world.gravity_m_s2, 1.2, round(found['alpha'], 3))    # the namelist's brkup_rhor and brkup_rhoexp

CM1's Morrison scheme gives rain an exponential spectrum and limits its mean diameter D_m = 1/lambda twice. Rain's
self-collection is offset by collisional breakup above a cutoff D_b of 300 um, by the factor
2 - exp(2300 m^-1 (D_m - D_b)) (Verlinde and Cotton 1993), so that D_m settles at D_b + ln 2 / 2300 m^-1 = 0.60 mm;
and D_m is capped at 2.8 mm. The rain's mean fall speeds are capped at 9.1 m/s in the scheme's reference air. All
three are Earth's (morrison.py).

Two drops that collide coalesce or come apart as the collision's kinetic energy against surface tension decides. The
outcome follows the collision's Weber number, We = CKE / S_c, its kinetic energy over the surface energy of the
coalesced drop: the pair coalesces with efficiency exp(-1.15 We) (Straub et al. 2010), the liquid's viscosity entering
only through an Ohnesorge number of a few thousandths. At a lower gravity the same drops fall more slowly and meet more
gently. A pair of drops on another world collides as an Earth pair of the same size ratio does when it is s times that
pair's size, s set by the Weber number through each world's terminal speeds, which the single-drop solver gives
(drops.py). Weighted by the breakup each Earth pair makes in Morrison's spectra at the cutoff and at the equilibrium,
the pairs' s gives the size scale of the breakup law on that world.

At equal air density s is the ratio of the worlds' capillary lengths sqrt(sigma / (rho_w g)), to within 0.2% at the
equilibrium and 4% at the cutoff in Terluna's cases, the Moon's gravity and 3.7 m/s2: a drop's shape follows that
length, its inertial fall the speed (g sigma / rho_w)^(1/4) (rho_w / rho_air)^(1/2) it implies, and the Weber numbers
of its collisions both. Denser air slows the drops and softens their collisions, so s grows with the air's density as
(rho_air / rho_air,Earth)^alpha: at the equilibrium Terluna found alpha between 0.69 and 0.71 for gravities from the
Moon's to Earth's at 1.2 times Earth's density, and 0.61 at the Moon's gravity and 1.5 times. The cap on D_m bounds
thin rain sorted by its fall, where breakup is too slow to act; it follows the largest drop that keeps together, the
stability screen, which scales with the capillary length alone. The cap on the mean fall speed follows that drop's
terminal speed, which under the same similarity scales as (g / 9.81)^(1/4). Low and List's (1982) fit of the
coalescence efficiency, read with its dimensional constants at lunar sizes and speeds, makes the Moon's drops break at
smaller sizes: its exponent contains an absolute length of about 5 mm, which on Earth's terminal speeds serves in place
of the Weber number, and lunar pairs lie beyond the 0.4-4.6 mm it was measured over. Its weights check the Weber
law's, and comparison() gives its literal reading beside them.

Evidence. A runnable calculation: the single-drop solver's terminal speeds, which reproduce Earth's measured fall
speeds to 0.20 m/s, in each world's air, with the collision outcome taken to follow the Weber number alone, the law of
Straub et al. (2010) for raindrop pairs, which Terluna took from that paper's abstract (sources.json records how far
each source was read). A world's values are Earth's breakup scaled by that similarity, which no laboratory has
measured at another gravity.

Assumptions. Drops collide at their terminal speeds in still air, with the geometric kernel
pi/4 (D_L + D_s)^2 |V_L - V_s| (collision efficiency 1), between 0.1 mm and the stability screen. Each pair's outcome
is set by its Weber number and size ratio; the impact parameter averages alike on both worlds; the Ohnesorge number of
a 1 mm drop, 0.004 on Earth, and the denser gas film between the drops are left out. Morrison's exponential spectra
serve for the rain whose breakup the scheme's law was fitted to, and the law's two lengths, the cutoff and its
e-folding length, scale together by the equilibrium's s. Earth's air is at 1 atm under standard gravity, at the world's
temperature and relative humidity at 2 m.

From Terluna's atmosphere/rain/breakup.py at 39c5ee04 (domain/atmosphere dd89cef), whose product builder, bound to
Terluna's three target climates, stays there. Speeds, collision, straub, low_list, rising_size, pair_scale,
breakup_weights, scale, low_list_literal, comparison and mass_weighted_speed are Terluna's; earth_column and
density_exponent give its calculation for any world, and limits is Terluna's lunar_limits for any gravity, joined with
the mirror of the patch in its runner (climate/crm/cm1_run.py, rain_limits).
"""
from __future__ import annotations

import math

import numpy as np

from shared.constants import STANDARD_GRAVITY
from atmosphere.radiative_convective.thermodynamics import DryAir
from atmosphere.rain import drops, morrison

# Straub, Beheng, Seifert, Schlottke and Weigand (2010, part II): colliding raindrops coalesce with efficiency
# exp(-1.15 We), We = CKE / S_c.
STRAUB_DECAY = 1.15
# Low and List (1982a): E = a (1 + p)^-2 exp(-b sigma E_T^2 / S_c) for E_T = CKE + S_T - S_c below 5 uJ, 0 above,
# fitted to pairs of 0.395-4.6 mm and 0.395-1.8 mm.
LOW_LIST_A, LOW_LIST_B, LOW_LIST_TOP_J = 0.778, 2.61e6, 5.0e-6
LOW_LIST_LARGE_M, LOW_LIST_SMALL_M = (0.395e-3, 4.6e-3), (0.395e-3, 1.8e-3)
EQUILIBRIUM_M = morrison.BREAKUP_CUTOFF + math.log(2.0) / morrison.BREAKUP_RATE   # where breakup balances, 0.60 mm
SPECTRA = (('cutoff', morrison.BREAKUP_CUTOFF), ('equilibrium', EQUILIBRIUM_M))
TABLE_POINTS, TABLE_SMALLEST_M = 320, 0.02e-3     # terminal speeds on a log grid up to just below the screen
SCREEN_MARGIN = 0.998
PAIR_POINTS, PAIR_SMALLEST_M = 200, 0.1e-3        # Earth's drops in the spectra, from drizzle to the screen
LINE_SAMPLES, BISECTIONS = 160, 60
ATMOSPHERE_PA = 101325.0                          # Earth's sea-level air, the reference of the namelist's brkup_rhor


class Speeds:
    """Terminal speeds in still air at one height of a column on a log grid of sizes up to just below its stability
    screen, with the air's density and water's surface tension there."""

    def __init__(self, column, altitude_m=0.0):
        state = column.state(altitude_m)
        self.gravity = column.gravity_m_s2
        self.density = state['density_kg_m3']
        self.sigma = drops.surface_tension(state['temperature_k'])
        self.screen = drops.stable_diameter(column, altitude_m)
        self.diameter = np.geomspace(TABLE_SMALLEST_M, SCREEN_MARGIN * self.screen, TABLE_POINTS)
        self.speed = np.array([drops.terminal_speed(d, column, altitude_m) for d in self.diameter])
        self._log = (np.log(self.diameter), np.log(self.speed))

    def __call__(self, diameter_m):
        return np.exp(np.interp(np.log(diameter_m), *self._log))

    @property
    def capillary_length(self):
        return math.sqrt(self.sigma / (self.gravity * (drops.WATER_DENSITY - self.density)))


def collision(speeds, large, small):
    """Pairs of drops falling at their terminal speeds: the collision's kinetic energy CKE, the coalesced drop's surface
    energy S_c, the two drops' surface energy S_T (J) and the Weber number CKE / S_c."""
    reduced = math.pi / 12 * drops.WATER_DENSITY * large**3 * small**3 / (large**3 + small**3)
    cke = reduced * (speeds(large) - speeds(small))**2
    s_c = math.pi * speeds.sigma * (large**3 + small**3)**(2 / 3)
    s_t = math.pi * speeds.sigma * (large**2 + small**2)
    return cke, s_c, s_t, cke / s_c


def straub(weber):
    """Coalescence efficiency by Straub et al. (2010): exp(-1.15 We)."""
    return np.exp(-STRAUB_DECAY * weber)


def low_list(speeds, large, small):
    """Low and List's (1982a) coalescence efficiency and its limit at no collision energy, a (1 + p)^-2."""
    cke, s_c, s_t, _ = collision(speeds, large, small)
    energy = cke + s_t - s_c
    ceiling = LOW_LIST_A * (1 + small / large)**-2
    return np.where(energy < LOW_LIST_TOP_J, ceiling * np.exp(-LOW_LIST_B * speeds.sigma * energy**2 / s_c), 0.0), ceiling


def rising_size(speeds, ratio, weber):
    """For pairs of size ratio p = D_s / D_L, the smallest large drop on a world whose pair reaches a Weber number:
    along D_s = p D_L the Weber number rises with size to a largest value below the stability screen and may fall
    beyond it, so the size is sought on the rising branch. Returns the size (nan where the line never reaches the Weber
    number), the size of the line's largest Weber number and that number."""
    lo = np.log(np.maximum(TABLE_SMALLEST_M / ratio, TABLE_SMALLEST_M) * 1.0001)
    hi = np.full_like(lo, math.log(SCREEN_MARGIN * speeds.screen * 0.9999))
    line = np.exp(lo[:, None] + (hi - lo)[:, None] * np.linspace(0.0, 1.0, LINE_SAMPLES))
    w = collision(speeds, line, ratio[:, None] * line)[3]
    rows, top = np.arange(len(ratio)), np.argmax(w, axis=1)

    def at(log_size):
        return collision(speeds, np.exp(log_size), ratio * np.exp(log_size))[3]

    # the line's largest Weber number, sampled finely between the samples beside the largest sample (the speeds'
    # interpolation leaves the top of the line flat and slightly uneven, so a search for one maximum can stop short)
    a = np.log(line[rows, np.maximum(top - 1, 0)])
    b = np.log(line[rows, np.minimum(top + 1, LINE_SAMPLES - 1)])
    fine = a[:, None] + (b - a)[:, None] * np.linspace(0.0, 1.0, LINE_SAMPLES)
    w_fine = collision(speeds, np.exp(fine), ratio[:, None] * np.exp(fine))[3]
    top_log = fine[rows, np.argmax(w_fine, axis=1)]
    peak = np.maximum(w_fine.max(axis=1), w[rows, top])
    a, b = lo.copy(), top_log
    for _ in range(BISECTIONS):
        middle = 0.5 * (a + b)
        lower = at(middle) < weber
        a, b = np.where(lower, middle, a), np.where(lower, b, middle)
    size = np.where(weber <= w[:, 0], np.exp(lo), np.exp(0.5 * (a + b)))
    return np.where(weber <= peak * (1.0 + 1e-4), size, np.nan), np.exp(top_log), peak


def pair_scale(world, earth, large, small):
    """Size factor s for Earth pairs: the smallest pair of the same size ratio on the world reaching the Earth pair's
    Weber number over the smallest such pair on Earth. Pairs the world cannot match take the size of its largest Weber
    number at that ratio, and are flagged."""
    ratio = small / large
    weber = collision(earth, large, small)[3]
    on_earth, earth_top, _ = rising_size(earth, ratio, weber)
    on_earth = np.where(np.isfinite(on_earth), on_earth, earth_top)    # at the sampled peak of Earth's own line
    on_world, top_size, _ = rising_size(world, ratio, weber)
    reached = np.isfinite(on_world)
    return np.where(reached, on_world, top_size) / on_earth, reached


def breakup_weights(earth, mean_diameter_m):
    """Earth's drop pairs (large, small) in Morrison's exponential spectrum of a mean diameter, from 0.1 mm to the
    stability screen, each weighted by the breakup it carries: the geometric kernel times both drops' numbers times the
    share that does not coalesce, by Straub et al.'s law and by Low and List's energetic breakup (their limit at no
    energy less their efficiency)."""
    d = np.geomspace(PAIR_SMALLEST_M, SCREEN_MARGIN * 0.999 * earth.screen, PAIR_POINTS)
    number = np.gradient(np.log(d)) * d * np.exp(-d / mean_diameter_m)
    i, j = np.triu_indices(PAIR_POINTS, k=1)
    large, small = d[j], d[i]
    kernel = math.pi / 4 * (large + small)**2 * np.abs(earth(large) - earth(small)) * number[j] * number[i]
    weber = collision(earth, large, small)[3]
    efficiency, ceiling = low_list(earth, large, small)
    return large, small, dict(straub=kernel * (1.0 - straub(weber)), low_list=kernel * (ceiling - efficiency))


def scale(world, earth, mean_diameter_m, law='straub'):
    """The breakup-weighted size factor carrying an Earth spectrum of a mean diameter to the world: geometric mean, 10,
    50 and 90% points, the share of the weight the world cannot match, and the breaking pairs' mean sizes."""
    large, small, weights = breakup_weights(earth, mean_diameter_m)
    w = weights[law]
    keep = w > 1e-9 * w.max()
    large, small, w = large[keep], small[keep], w[keep]
    s, reached = pair_scale(world, earth, large, small)
    log_s = np.log(s)
    order = np.argsort(log_s)
    cumulative = np.cumsum(w[order]) / w.sum()

    def point(f):
        return float(np.exp(log_s[order][min(int(np.searchsorted(cumulative, f)), len(order) - 1)]))

    return dict(scale=float(np.exp(np.sum(w * log_s) / w.sum())), p10=point(0.1), p50=point(0.5), p90=point(0.9),
                unreached_share=float(w[~reached].sum() / w.sum()),
                breaking_large_mm=float(np.sum(w * large) / w.sum() * 1e3),
                breaking_small_mm=float(np.sum(w * small) / w.sum() * 1e3))


def low_list_literal(world, earth, mean_diameter_m):
    """Low and List's fit read with its dimensional constants on both worlds: for the Earth pairs within its measured
    sizes that sometimes coalesce, the factor s at which the world's pair of the same size ratio has the Earth pair's
    efficiency, weighted by their energetic breakup in the spectrum; and the share of that breakup the check covers."""
    large, small, weights = breakup_weights(earth, mean_diameter_m)
    w = weights['low_list']
    target = low_list(earth, large, small)[0]
    inside = ((large >= LOW_LIST_LARGE_M[0]) & (large <= LOW_LIST_LARGE_M[1]) & (small >= LOW_LIST_SMALL_M[0])
              & (small <= LOW_LIST_SMALL_M[1]))
    use = inside & (target > 0.0) & (w > 0.0)
    large, small, target, weight = large[use], small[use], target[use], w[use]
    a = np.full(large.shape, math.log(0.5))
    b = np.log(SCREEN_MARGIN * 0.9999 * world.screen / large)
    above = low_list(world, np.exp(a) * large, np.exp(a) * small)[0] >= target
    below = low_list(world, np.exp(b) * large, np.exp(b) * small)[0] <= target
    bracketed = above & below
    for _ in range(BISECTIONS):                         # the efficiency falls as the pair grows at a fixed ratio
        middle = 0.5 * (a + b)
        high = low_list(world, np.exp(middle) * large, np.exp(middle) * small)[0] > target
        a, b = np.where(high, middle, a), np.where(high, b, middle)
    log_s = 0.5 * (a + b)
    covered = weight[bracketed].sum() / w.sum()
    return dict(scale=float(np.exp(np.sum(weight[bracketed] * log_s[bracketed]) / weight[bracketed].sum())),
                breakup_share_covered=float(covered))


def comparison(world, earth):
    """The scale at the cutoff and at the equilibrium by both laws' weights, the capillary ratio and alpha."""
    density_ratio = world.density / earth.density
    capillary = world.capillary_length / earth.capillary_length
    out = dict(density_kg_m3=dict(world=world.density, earth=earth.density), density_ratio=density_ratio,
               capillary=capillary, stability_screen_mm=dict(world=world.screen * 1e3, earth=earth.screen * 1e3))
    for name, dm in SPECTRA:
        row = scale(world, earth, dm)
        row['low_list_weights'] = scale(world, earth, dm, law='low_list')['scale']
        row['low_list_literal'] = low_list_literal(world, earth, dm)
        row['over_capillary'] = row['scale'] / capillary
        row['alpha'] = (math.log(row['over_capillary']) / math.log(density_ratio)
                        if abs(density_ratio - 1.0) > 1e-3 else None)
        out[name] = row
    return out


def mass_weighted_speed(speeds, mean_diameter_m):
    """The mass-weighted mean terminal speed of an exponential spectrum, up to the stability screen."""
    d = np.geomspace(1e-5, speeds.diameter[-1], 2000)
    weight = np.gradient(d) * d**3 * np.exp(-d / mean_diameter_m)
    return float(np.sum(weight * speeds(d)) / np.sum(weight))


def earth_column(column):
    """Earth's air beside a world's: Earth's dry air at 1 atm under standard gravity, at the world's temperature and
    relative humidity at 2 m."""
    return drops.Column(gravity_m_s2=STANDARD_GRAVITY, surface_pressure_pa=ATMOSPHERE_PA,
                        surface_temperature_k=column.surface_temperature_k,
                        surface_relative_humidity=column.surface_relative_humidity, air=DryAir(ATMOSPHERE_PA))


def density_exponent(column, earth=None):
    """The breakup law's size scale on a world, from its air at 2 m, and the exponent alpha that the air's density
    takes in it: the scale of Morrison's spectrum at the breakup equilibrium by Straub et al.'s weights, the ratio of
    the capillary lengths, the worlds' ratio of air density, and alpha = ln(scale / capillary) / ln(density ratio),
    None where the two airs' densities agree within a thousandth. earth defaults to earth_column(column)."""
    world, home = Speeds(column), Speeds(earth_column(column) if earth is None else earth)
    density_ratio = world.density / home.density
    capillary = world.capillary_length / home.capillary_length
    row = scale(world, home, EQUILIBRIUM_M)
    over = row['scale'] / capillary
    return dict(scale=row['scale'], capillary=capillary, density_ratio=density_ratio, over_capillary=over,
                alpha=math.log(over) / math.log(density_ratio) if abs(density_ratio - 1.0) > 1e-3 else None,
                unreached_share=row['unreached_share'])


def limits(gravity_m_s2, density_ratio=1.0, exponent=0.0, *, scaled=True, cutoff_m=morrison.BREAKUP_CUTOFF):
    """Rain's limits in CM1's Morrison scheme at a build's gravity, as patch 03 of the lab's CM1 series sets them from
    its namelist: the breakup cutoff (m), the breakup law's rate (1/m), the mean diameter at which self-collection and
    breakup balance (m), the cap on the mean diameter (m) and the cap on the mean fall speeds in the scheme's reference
    air (m/s).

    scaled False is brkup_gscale = 0: CM1's own limits, with the fall-speed cap core patch 04 sets. scaled True is
    brkup_gscale = 1 with brkup_rhor = density_ratio and brkup_rhoexp = exponent: with s = (9.81 / g)^(1/2), the
    breakup's two lengths times s density_ratio^exponent, the cap on the mean diameter times s, and the fall-speed cap
    9.1 (g / 9.81)^(1/4) m/s. density_ratio is the surface air's density over that of Earth's sea-level air at the same
    temperature: in CM1, whose air has Earth's gas constant, the surface pressure over 1013.25 hPa. cutoff_m is the
    namelist's brkup_db, 300 um where it is 0."""
    cutoff = cutoff_m if cutoff_m >= 1.0e-20 else morrison.BREAKUP_CUTOFF        # GRAUPEL_INIT's rule for brkup_db
    rate, cap = morrison.BREAKUP_RATE, morrison.MEAN_DIAMETER_CAP
    fall = morrison.FALL_CAP * morrison.gravity_factor(gravity_m_s2)
    if scaled:
        if not density_ratio > 0:
            raise ValueError('The density ratio must be positive')
        capillary = math.sqrt(morrison.GRAVITY / gravity_m_s2)
        collisional = capillary * density_ratio**exponent
        cutoff, rate, cap = cutoff * collisional, rate / collisional, cap * capillary
        fall = morrison.FALL_CAP * (gravity_m_s2 / morrison.GRAVITY)**0.25
    return dict(breakup_cutoff_m=cutoff, breakup_rate_per_m=rate, equilibrium_m=cutoff + math.log(2.0) / rate,
                mean_diameter_cap_m=cap, fall_speed_cap_m_s=fall)
