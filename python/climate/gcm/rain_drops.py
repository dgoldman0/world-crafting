"""PlaSim's falling rain evaporated from its drops' sizes and fall speeds at a world's gravity, in place of the constant
gamma: the Python copy of patch 14 of models/exoplasim/patches, and what a run of that patch takes for a world.

    from atmosphere.radiative_convective.thermodynamics import earthlike_air
    from atmosphere.rain import drops, fall_law
    from climate.gcm import rain_drops
    world = drops.Column(gravity_m_s2=1.6242, surface_pressure_pa=121590.0, surface_temperature_k=300.4,
                         surface_relative_humidity=0.61, air=earthlike_air(121590.0, 400.0))
    found = rain_drops.settings(world, rain_drops.TERLUNA_OPEN_MOON_BIRTHS)    # about three seconds on one thread
    found['namelist']                                 # the entries of rainmod's namelist
    fall_law.table_text(found['table'])               # the text of lab_rain_law.txt, the table CM1's patch 04 reads

PlaSim's mkrain (rainmod.f90) takes the precipitation each column forms down through its layers, turns it to snow
where the air is below freezing and back to rain where it is above, and with nevapprec 1 evaporates in each unsaturated
layer a share gamma of the layer's saturation deficit each step, at most the precipitation there. gamma, 0.01, was set
for Earth, and the scheme takes no account of the drops' sizes or fall speeds (defect log B30). With nevapprec 2
(patch 14) the rain has, beside its mass flux F, the flux of its drops' number F_N. Its spectrum is Morrison's
exponential one, N0 exp(-lambda D), whose slope follows from the two fluxes:
F_N/F = lambda^3 V_n(lambda) / (pi rho_w V_m(lambda)). Through each layer, in midpoint steps of at most rdrop_step
metres:

- evaporation, Morrison's equation as CM1 applies it: the rain loses k F per metre of fall,
      k = 2 rho D_v lambda^4 W (q_s - q) / (rho_w V_m AB),  W = F1R/lambda^2 + F2R (dens rho/mu)^(1/2) Sc^(1/3) T3,
  with AB PlaSim's own latent-heat factor, and its drops go in proportion to its water (Morrison's NSUBR), so that
  dF_N/ds = -k F_N V_m/V_n;
- collisions, Morrison's self-collection with breakup: dF_N/ds = -K dum (F/V_m)(F_N/V_n), K the world's rate from the
  drops' collision kernels (fall_law.self_collection), dum = 1 below the breakup cutoff D_b and
  2 - exp(KB (1/lambda - D_b)) above it, D_b and KB CM1's Earth values scaled as the rain limits of CM1's patch 03
  scale them, by sqrt(9.81/g) times the column's surface pressure over 1013.25 hPa to the power rdrop_rhoexp; only on
  rain of at least 1e-8 kg/kg;
- V_m, V_n and the ventilation integral T3 from the fall law of the world's rain (fall_law.table, the table that
  CM1's patch 04 reads), times Morrison's density factor dens = (RHOSU/rho)^0.54 and its square root, the mean speeds
  capped at 9.1 (g/9.81)^(1/4) m/s times dens, lambda held between the cap on the mean diameter,
  2.8 mm sqrt(9.81/g), and 20 um.

New rain enters each layer at its middle. Rain melted from snow there comes as new drops of mean diameter rdrop_melt.
Rain formed as rain there, W, comes as new drops of rdrop_warm with nrdrop_join 0; with nrdrop_join 1 it joins the rain
already falling through the layer, as accretion adds water to drops and leaves their number, and makes new drops where
none falls; and with nrdrop_join 2 the share W/(W + F) of it makes new drops and the rest joins, F the rain arriving
at the layer's middle, so that rain makes its own drops where little falls in, as autoconversion does, and grows the
falling drops where much does. The layer evaporates at most what would saturate it over the step, as gamma's form
does. The snow sublimates with gamma, and mkrain's phase rule, which makes each layer's precipitation all rain or all
snow, stays as released.

What is the world's and what is Earth's. Gravity, the gas constant, the pressures and the latent-heat factor are the
model's own. The table, the self-collection rate and the density exponent come from the world's air at 2 m
(fall_law.settings). Morrison's ventilation coefficients, his fits for the vapour's diffusivity and the air's
viscosity, and the breakup law's form are Earth's, for air of Earth-like composition (atmosphere/rain/morrison.py).
The birth rule and the two birth sizes are a calibration that a study supplies for its world, fitted on
cloud-resolving boxes of that world. TERLUNA_OPEN_MOON_BIRTHS records Terluna's for the Open Moon.

Evidence. A runnable calculation with its tests: the copy keeps each column's water, agrees with hand arithmetic on
a power law's closed forms, and the Fortran of patch 14 gives its numbers to 1e-10 (climate/tests/test_rain_drops.py).
Terluna tested the scheme offline on its three CM1 boxes of the Open Moon, before and after building it, and its own
record gives the outcomes (climate/gcm/README.md at 39c5ee04, "PlaSim's rain from its drops"): from the boxes' mean air
with CM1's own sizes for the new rain, the size taken down a column gave CM1's column evaporation within 1.01-1.12;
on CM1's levels and on PlaSim's fifteen, every new drop at one size gave 1.15-1.31 and rain formed as rain joining
whatever falls 0.64-0.80; and on the fifteen levels the share rule gave 0.96-1.05 with melted rain at CM1's own
0.865 mm and 0.91-0.98 at the lunar 2.95 mm. The lab has run none of them. The share depends on the layers' thickness,
so another level set tests the rule again, and the collisions follow a similarity that no measurement at another
gravity tests (atmosphere/rain/breakup.py).

`mkrain` is the patched mkrain's Python copy with nevapprec 2, columns as rows and levels top first, for the tests.

Brought from Terluna's climate/gcm/rain_drops.py at 39c5ee04 (python/provenance.json). lookup, limits, inverse,
slope_of, number_per_flux, rates, rdropevap and mkrain are Terluna's, taking the fall law and the settings as
arguments where Terluna's module read its lunar products at import; law_of, law_from_text, check and settings are the
lab's. The Fortran edit lists stay in Terluna, the patch being models/exoplasim/patches/14-rain-from-drop-sizes.patch,
and the snow's sublimation by its flakes, which Terluna's mkrain also calls, awaits its assessment (PLAN.md).
"""
from __future__ import annotations

import math

import numpy as np

from atmosphere.rain import breakup, fall_law, morrison

INVERSE_POINTS = 2001             # the slope's inverse table, uniform in ln lambda across the scheme's range
EXPONENT_LIMIT = 50.0             # the most a step's exponent may change the rain's water or drops (e^50)
TINY_FLUX = 1.0e-30               # kg/m2/s: rain below it is gone
STEP_M = 1000.0                   # the longest midpoint step through a layer: on the fifteen-layer columns of Terluna's
                                  # boxes it stayed within 0.25% of 50 m steps (Terluna's record)
RULES = {'one_size': 0, 'join': 1, 'share': 2}        # nrdrop_join by the birth rule's name
NAMELIST_NAMES = ('nrdrop_join', 'rdrop_warm', 'rdrop_melt', 'rdrop_ksc', 'rdrop_rhoexp', 'rdrop_step')
# Terluna's calibration of the births for the Open Moon, which a study of that world supplies and another world
# replaces with its own (Terluna climate/gcm/rain_drops.py and climate/gcm/README.md at 39c5ee04). The rule: the share
# rule, adopted on PlaSim's fifteen levels 'l15', where it gave CM1's column evaporation within 0.96-1.05 on three
# boxes. New rain, 0.439 mm: where CM1's sea box forms rain as rain afresh, the mean of its rain-mass-weighted
# 1/lambda over the levels and outputs of days 29.5-59.0 at which the rain's gain less its melting outran the rain
# arriving from above, weighted by that excess. Melted rain, 2.95 mm: the rain lunar snow melts into, one drop of each
# melted particle as Morrison counts CM1's, from Terluna's corrected McSnow run at 1 mm/h (domain/atmosphere aceddfa),
# the snowfall nearest its boxes'; light snow gave 1.25-1.37 mm and heavy snow 3.34-3.42 mm. The calibration holds
# for that gravity, that surface pressure of 1.2 atm, that level set and CM1's microphysics as those boxes ran it.
TERLUNA_OPEN_MOON_BIRTHS = dict(rule='share', new_rain_m=0.439e-3, melted_rain_m=2.95e-3)


def law_of(table: dict) -> dict:
    """A fall-law table (fall_law.table) as the copy reads it: its first ln lambda, its step and its three rows."""
    rows = np.array([table['ln_mass_weighted'], table['ln_number_weighted'], table['ln_ventilation']], float)
    if rows.shape != (3, table['points']) or table['points'] < 2 or not table['ln_lambda_step'] > 0:
        raise ValueError('The fall law holds two rows or more of three moments, on a positive step in ln lambda')
    return dict(x0=float(table['ln_lambda_first']), dx=float(table['ln_lambda_step']), table=rows)


def law_from_text(text: str) -> dict:
    """The fall law as rdropini reads it from the text of fall_law.TABLE_FILE (fall_law.table_text): the count of its
    rows with the first ln lambda and the step, then three logs for each lambda. The text states each number to ten
    significant digits, so the moments read back lie within 1e-8 of the table's own. A text that rdropini stops on
    is refused."""
    words = text.split()
    try:
        points, first, step = int(words[0]), float(words[1]), float(words[2])
    except (IndexError, ValueError):
        raise ValueError("The fall law's first line holds the count of its rows, its first ln lambda and its step") \
            from None
    if points < 2 or not step > 0:
        raise ValueError('The fall law holds two rows or more, on a positive step in ln lambda')
    if len(words) != 3 + 3 * points:
        raise ValueError(f'The fall law states {points} rows of three logs, where its text holds {len(words) - 3} '
                         'numbers')
    rows = np.array([float(word) for word in words[3:]]).reshape(points, 3).T
    return dict(x0=first, dx=step, table=rows)


def lookup(lnlam, law):
    """The table's three moments at ln lambda (mass-weighted and number-weighted speeds in the reference air, the
    ventilation integral), linear in ln lambda and held at the ends, as rdroptab reads them."""
    x = (lnlam - law['x0']) / law['dx']
    n = law['table'].shape[1]
    i = min(max(int(x), 0), n - 2)
    w = min(max(x - i, 0.0), 1.0)
    t = law['table']
    return tuple(math.exp((1.0 - w) * t[m, i] + w * t[m, i + 1]) for m in range(3))


def limits(g: float) -> dict:
    """The limits that every column of a world shares: the slope's range and the cap on the mean speeds."""
    scap = math.sqrt(morrison.GRAVITY / g)
    return dict(lnlam_min=math.log(1.0 / (morrison.MEAN_DIAMETER_CAP * scap)),
                lnlam_max=math.log(1.0 / morrison.MEAN_DIAMETER_FLOOR),
                vcap=morrison.FALL_CAP * (g / morrison.GRAVITY) ** 0.25)


def inverse(g: float, law: dict) -> dict:
    """ln(F_N/F) on INVERSE_POINTS slopes uniform in ln lambda over the scheme's range (the speeds capped), from which
    the slope of a rain of given fluxes is read back; the density factor cancels. A law whose F_N/F fails to rise
    with lambda is refused, as rdropini stops on it."""
    lim = limits(g)
    lnl = np.array([lim['lnlam_min'] + (lim['lnlam_max'] - lim['lnlam_min']) * i / (INVERSE_POINTS - 1)
                    for i in range(INVERSE_POINTS)])
    lnr = np.empty(INVERSE_POINTS)
    for i, x in enumerate(lnl):
        vm, vn, _ = lookup(x, law)
        lnr[i] = 3.0 * x + math.log(min(vn, lim['vcap'])) - math.log(min(vm, lim['vcap'])) \
            - math.log(math.pi * morrison.WATER_DENSITY)
    if not np.all(np.diff(lnr) > 0):
        raise ValueError('The fall law gives a number of drops per unit of rain that fails to rise with lambda')
    return dict(lim, lnl=lnl, lnr=lnr, step=(lim['lnlam_max'] - lim['lnlam_min']) / (INVERSE_POINTS - 1), law=law)


def slope_of(r: float, inv: dict) -> float:
    """ln lambda for ln(F_N/F) = r: a search of the inverse table, linear between its points, held at its ends."""
    lnr, lnl = inv['lnr'], inv['lnl']
    if r <= lnr[0]:
        return float(lnl[0])
    if r >= lnr[-1]:
        return float(lnl[-1])
    lo, hi = 0, len(lnr) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if lnr[mid] <= r:
            lo = mid
        else:
            hi = mid
    return float(lnl[lo] + (r - lnr[lo]) / (lnr[hi] - lnr[lo]) * (lnl[hi] - lnl[lo]))


def number_per_flux(d: float, inv: dict) -> float:
    """F_N/F of rain whose mean diameter is d, its slope held within the scheme's range."""
    x = min(max(-math.log(d), inv['lnlam_min']), inv['lnlam_max'])
    i = min(int((x - inv['lnl'][0]) / inv['step']), INVERSE_POINTS - 2)
    w = (x - inv['lnl'][i]) / inv['step']
    return math.exp((1.0 - w) * inv['lnr'][i] + w * inv['lnr'][i + 1])


def rates(f, n, air, inv, prm):
    """The share of its water, a, and of its drops, b, that rain loses per metre of fall at fluxes f (kg/m2/s) and n
    (per m2 per s)."""
    if f <= TINY_FLUX or n <= 0.0:
        return 0.0, 0.0
    lnlam = slope_of(math.log(n / f), inv)
    lam = math.exp(lnlam)
    vm0, vn0, t3 = lookup(lnlam, inv['law'])
    dens = (morrison.REFERENCE_DENSITY / air['rho']) ** morrison.DENSITY_EXPONENT
    vm = min(dens * vm0, inv['vcap'] * dens)
    vn = min(dens * vn0, inv['vcap'] * dens)
    w = morrison.VENTILATION[0] / lam**2 + morrison.VENTILATION[1] * math.sqrt(dens * air['rho'] / air['mu']) \
        * air['sc'] ** (1.0 / 3.0) * t3
    a = 0.0
    if air['q'] < air['qs']:
        a = 2.0 * air['rho'] * air['dv'] * lam**4 * w * (air['qs'] - air['q']) \
            / (morrison.WATER_DENSITY * vm * air['ab'])
    d = 1.0 / lam
    dum = 1.0 if d < air['db'] else 2.0 - math.exp(air['kb'] * (d - air['db']))
    c = 0.0
    if f / vm / air['rho'] >= morrison.SELF_COLLECTION_FLOOR:
        c = prm['rdrop_ksc'] * dum * (f / vm) / vn
    return a, a * vm / vn + c


def rdropevap(jlev, zq, zt, zqsat, zcor, zpra, zmelt, zprc, zprl, zprn, zdqdtl, zdtdt, s, c, prm, inv):
    """One layer of every column: the rain's evaporation and drops through it (rdropevap in Fortran, step for step).
    zprc, zprl (sigma-weighted mixing ratio per second), zprn (per m2 per s) and the layer's tendency columns change in
    place."""
    for j in range(zprc.size):
        mass = s['dp'][j] / c['ga']
        ftot = (zprc[j] + zprl[j]) * mass
        if ftot <= 0.0:
            zprn[j] = 0.0
            continue
        farr = min(max(zpra[j], 0.0), zprc[j] + zprl[j]) * mass
        bm = min(max(zmelt[j], 0.0) * mass, ftot - farr)
        bw = max(ftot - farr - bm, 0.0)
        if farr <= 0.0:
            zprn[j] = 0.0
        tv = zt[j] * (1.0 + (1.0 / c['rdbrv'] - 1.0) * zq[j])
        p = s['dp'][j] * s['sigma'][jlev]
        rho = p / (c['gascon'] * tv)
        dz = c['gascon'] * tv / c['ga'] * s['dsigma'][jlev] / s['sigma'][jlev]
        lcpe = c['ALV'] / (c['acpd'] * (1.0 + c['ADV'] * s['dq'][j, jlev]))
        ab = 1.0 + lcpe * c['ra2'] * (c['TMELT'] - c['ra4']) * zqsat[j] * zcor[j] / (zt[j] - c['ra4']) ** 2
        mu = morrison.VISCOSITY[0] * zt[j] ** 1.5 / (zt[j] + morrison.VISCOSITY[1])
        dv = morrison.VAPOUR_DIFFUSIVITY[0] * zt[j] ** morrison.VAPOUR_DIFFUSIVITY[1] / p
        scol = math.sqrt(morrison.GRAVITY / c['ga']) * (s['dp'][j] / breakup.ATMOSPHERE_PA) ** prm['rdrop_rhoexp']
        air = dict(q=zq[j], qs=zqsat[j], rho=rho, ab=ab, mu=mu, dv=dv, sc=mu / (rho * dv),
                   db=morrison.BREAKUP_CUTOFF * scol, kb=morrison.BREAKUP_RATE / scol)
        f, n = farr, zprn[j]
        if f > 0.0 and n <= 0.0:
            n = f * number_per_flux(prm['rdrop_warm'], inv)
        ratio = n / f if f > 0.0 else 0.0            # the rain's last drops per unit of its flux
        nstep = max(1, math.ceil(0.5 * dz / prm['rdrop_step']))
        ds = 0.5 * dz / nstep
        for half in (1, 2):
            if half == 2:                                  # the layer's new rain, at its middle
                if bm > 0.0:
                    n = n + bm * number_per_flux(prm['rdrop_melt'], inv)
                if bw > 0.0:
                    if prm['nrdrop_join'] == 2:                # the share bw/(bw + f) as drops, the rest joining
                        n = n + bw * bw / (bw + f) * number_per_flux(prm['rdrop_warm'], inv)
                    elif not (prm['nrdrop_join'] == 1 and f > 0.0):
                        n = n + bw * number_per_flux(prm['rdrop_warm'], inv)
                f = f + bm + bw
                if f > 0.0:
                    ratio = n / f
            for _ in range(nstep):
                if f <= TINY_FLUX:
                    f, n = 0.0, 0.0
                    break
                a1, b1 = rates(f, n, air, inv, prm)
                fm = f * math.exp(-min(0.5 * a1 * ds, EXPONENT_LIMIT))
                if fm <= TINY_FLUX:                       # gone within the half step
                    f, n = 0.0, 0.0
                    break
                nm = n * math.exp(-max(min(0.5 * b1 * ds, EXPONENT_LIMIT), -EXPONENT_LIMIT))
                a2, b2 = rates(fm, nm, air, inv, prm)
                f = f * math.exp(-min(a2 * ds, EXPONENT_LIMIT))
                n = n * math.exp(-max(min(b2 * ds, EXPONENT_LIMIT), -EXPONENT_LIMIT))
                if f > TINY_FLUX:
                    ratio = n / f
        evap = max(ftot - f, 0.0) / mass
        cap = max(zqsat[j] - zq[j], 0.0) * s['dsigma'][jlev] / c['deltsec2'] / ab
        if evap > cap:                                    # the layer saturates: the rest keeps its last size
            n = (ftot - cap * mass) * ratio
            evap = cap
        fc = zprc[j] / (zprc[j] + zprl[j])
        zprc[j] = max(zprc[j] - evap * fc, 0.0)
        zprl[j] = max(zprl[j] - evap * (1.0 - fc), 0.0)
        zprn[j] = n
        dq = evap / s['dsigma'][jlev]
        zdtdt[j] = zdtdt[j] - dq * lcpe
        zdqdtl[j] = zdqdtl[j] + dq


def check(prm: dict) -> None:
    """The settings that rdropini stops on."""
    if prm['nrdrop_join'] not in (0, 1, 2):
        raise ValueError(f"nrdrop_join is 0, 1 or 2, where the settings give {prm['nrdrop_join']!r}")
    if not (prm['rdrop_warm'] > 0 and prm['rdrop_melt'] > 0):
        raise ValueError('rdrop_warm and rdrop_melt are positive mean diameters in metres')
    if not prm['rdrop_ksc'] >= 0 or not prm['rdrop_step'] > 0:
        raise ValueError('rdrop_ksc is zero or more and rdrop_step is positive')


def mkrain(s: dict, c: dict, prm: dict, law: dict) -> dict:
    """The patched mkrain with nevapprec 2 on columns (rows) and levels (top first): s holds dt and dq (with the ground
    after the levels), dtdt, dqdt, dp, sigma, dsigma and the precipitation formed by level (dprcl, dprscl, dprll,
    dprsll), and its tendencies are added in place; c holds PlaSim's constants, prm the six settings of the namelist
    and law the fall law (law_of). Returns the precipitation at the ground (m/s of water), the drops' number flux
    there and the rain's evaporation and the snow's sublimation by layer."""
    check(prm)
    n, nlev = s['dprcl'].shape
    inv = inverse(c['ga'], law)
    zprc, zprl, zprsc, zprsl, zprn = (np.zeros(n) for _ in range(5))
    zdtdt, zdqdts, zdqdtl = (np.zeros((n, nlev)) for _ in range(3))
    for jlev in range(nlev):
        zpra = zprc + zprl
        zprc = zprc + s['dprcl'][:, jlev] - s['dprscl'][:, jlev]
        zprl = zprl + s['dprll'][:, jlev] - s['dprsll'][:, jlev]
        zprsc = zprsc + s['dprscl'][:, jlev]
        zprsl = zprsl + s['dprsll'][:, jlev]
        zpsa = zprsc + zprsl
        # rain and snow by the layer's temperature, and in the lowest layer by the ground's as well (mkrain's where
        # and elsewhere: the snow melts where the air is above freezing, the rain freezes where it is at or below)
        conversions = [(s['dt'][:, jlev], False)] + ([(s['dt'][:, nlev], True)] if jlev == nlev - 1 else [])
        for tcol, add in conversions:
            warm = (zprsc + zprsl > 0.0) & (tcol > c['TMELT'])
            cold = ~warm & (zprc + zprl > 0.0) & (tcol <= c['TMELT'])
            zlcp = (c['ALS'] - c['ALV']) / (c['acpd'] * (1.0 + c['ADV'] * s['dq'][:, jlev]))
            base = zdtdt[:, jlev] if add else 0.0
            zdtdt[:, jlev] = np.where(warm, -(zprsc + zprsl) / s['dsigma'][jlev] * zlcp + base,
                                      np.where(cold, (zprc + zprl) / s['dsigma'][jlev] * zlcp + base, zdtdt[:, jlev]))
            zprc, zprl, zprsc, zprsl = (np.where(warm, zprsc + zprc, np.where(cold, 0.0, zprc)),
                                        np.where(warm, zprsl + zprl, np.where(cold, 0.0, zprl)),
                                        np.where(warm, 0.0, np.where(cold, zprc + zprsc, zprsc)),
                                        np.where(warm, 0.0, np.where(cold, zprl + zprsl, zprsl)))
        zq = s['dq'][:, jlev] + s['dqdt'][:, jlev] * c['deltsec2']
        zt = s['dt'][:, jlev] + s['dtdt'][:, jlev] * c['deltsec2']
        zqsat = c['rdbrv'] * c['ra1'] * np.exp(c['ra2'] * (zt - c['TMELT']) / (zt - c['ra4'])) \
            / (s['dp'] * s['sigma'][jlev])
        zqsat = np.minimum(zqsat, c['rdbrv'])
        zcor = 1.0 / (1.0 - (1.0 / c['rdbrv'] - 1.0) * zqsat)
        zqsat = zqsat * zcor
        zqsat = np.where(zqsat < 0.0, 0.0, zqsat)
        zmelt = np.maximum(zpsa - zprsc - zprsl, 0.0)
        rdropevap(jlev, zq, zt, zqsat, zcor, zpra, zmelt, zprc, zprl, zprn, zdqdtl[:, jlev], zdtdt[:, jlev], s, c,
                  prm, inv)
        for key in ('l', 'c'):                            # the snow, by gamma as released
            zprs = zprsl if key == 'l' else zprsc
            sub = (zq < zqsat) & (zprs > 0.0)
            zlcpe = c['ALS'] / (c['acpd'] * (1.0 + c['ADV'] * s['dq'][:, jlev]))
            zdqdt = np.minimum(c['gamma'] * (zqsat - zq) * s['dsigma'][jlev] / c['deltsec2']
                               / (1.0 + zlcpe * c['ra2'] * (c['TMELT'] - c['ra4']) * zqsat * zcor
                                  / (zt - c['ra4']) ** 2), zprs)
            zdqdt = np.where(sub, zdqdt, 0.0)
            zprs[:] = zprs - zdqdt
            zdqdt = zdqdt / s['dsigma'][jlev]
            zdtdt[:, jlev] = np.where(sub, zdtdt[:, jlev] - zdqdt * zlcpe, zdtdt[:, jlev])
            zdqdts[:, jlev] = np.where(sub, zdqdts[:, jlev] + zdqdt, zdqdts[:, jlev])
    s['dqdt'][:, :nlev] += zdqdtl + zdqdts
    s['dtdt'][:, :nlev] += zdtdt
    to_ms = s['dp'] / c['ga'] / 1000.0
    return dict(dprc=(zprc + zprsc) * to_ms, dprl=(zprl + zprsl) * to_ms, dprs=(zprsc + zprsl) * to_ms,
                number=zprn, rain_evaporation=zdqdtl, snow_sublimation=zdqdts)


def settings(column, births: dict, step_m: float = STEP_M) -> dict:
    """What a GCM run of patch 14 takes for the rain of a world, from the world's air at 2 m (a drops.Column) and a
    calibration of the births: the entries of rainmod's namelist, the fall-law table that the run's folder holds as
    fall_law.TABLE_FILE (fall_law.table_text writes it), the limits the scheme sets from the world's gravity, and the
    records of fall_law.settings behind the rate and the exponent.

    births holds the rule by which rain formed as rain makes drops, one of RULES, and the mean diameters in metres of
    new rain and of rain melted from snow (new_rain_m, melted_rain_m). rdrop_ksc is the world's self-collection rate
    and rdrop_rhoexp the exponent of breakup.density_exponent, 0 where the world's air has Earth's density, each as
    CM1's patches 03 and 04 take them (fall_law.settings); the scheme raises each column's own surface pressure over
    1013.25 hPa to that exponent."""
    if births.get('rule') not in RULES:
        raise ValueError(f"The birth rule is one of {tuple(RULES)}, where the calibration gives {births.get('rule')!r}")
    found = fall_law.settings(column)
    namelist = dict(nevapprec=2, nrdrop_join=RULES[births['rule']], rdrop_warm=float(births['new_rain_m']),
                    rdrop_melt=float(births['melted_rain_m']), rdrop_ksc=found['namelist']['rain_selfcoll'],
                    rdrop_rhoexp=found['namelist']['brkup_rhoexp'], rdrop_step=float(step_m))
    check(namelist)
    lim = limits(column.gravity_m_s2)
    return dict(namelist=namelist, table=found['table'],
                limits=dict(mean_diameter_cap_m=math.exp(-lim['lnlam_min']),
                            mean_diameter_floor_m=math.exp(-lim['lnlam_max']), fall_speed_cap_m_s=lim['vcap'],
                            breakup=found['limits']),
                self_collection=found['self_collection'], breakup=found['breakup'], air=found['air'],
                births=dict(rule=births['rule'], new_rain_m=float(births['new_rain_m']),
                            melted_rain_m=float(births['melted_rain_m'])))
