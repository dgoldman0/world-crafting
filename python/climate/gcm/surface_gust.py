"""Beljaars's gust in PlaSim's surface transfer, in place of its free-convection term over water and its least wind of
1 m/s: the Python copy of models/exoplasim/patches/12-surface-gust.patch (the record is notes/exoplasim.md, "The
gust and the similarity over water").

PlaSim's surflx (fluxmod.f90) gives the surface its transfer of heat and vapour |U| C_N F_h and of momentum |U| C_N F_m:
|U| the lowest level's wind, at least zumin (1 m/s); C_N = (kappa / ln(z_l / z0 + 1))^2 at that level's height z_l; F the
Louis-ECHAM factors of the bulk Richardson number. In unstable air over water F_h is instead Miller, Beljaars and
Palmer's (1992) interpolation toward the free convection of tank experiments, (1 + (cfree dthv^(1/3) / (|U| C_N))^1.25)^0.8,
whose constant 0.0016 m s-1 K-1/3 is a tank law's still-air limit at Earth's gravity and sea-level air. Beljaars (1995),
a co-author of that interpolation, took the large eddies of the convective boundary layer instead: they sweep the
surface air at about their convective velocity w*, which joins the mean wind in the bulk formulas. CM1's surface layer
takes that form over land and, with the lab's CM1 patch, over water; COARE's ocean algorithm takes it too (Fairall and
others 2003). With the gust (fluxmod's ngust = 1) the wind in surflx's bulk formulas is

    |U|_eff = max( sqrt(|U|^2 + (beta w*)^2), u_min ),   w* = (g / theta_v,n  h  (w'theta_v')_0)^(1/3)

with w* in unstable air and none in stable or neutral air, beta 1 and u_min 0.1 m/s as in CM1's sfclay (its vconvc and
its least wind). The bulk Richardson number takes |U|_eff, and every surface takes Louis's unstable factors, the
free-convection term over water dropped. The surface buoyancy flux (w'theta_v')_0 comes from the surface fluxes of the
step before (dshfl and devap), and the boundary layer's depth h from the rule of Terluna's nonlocal scheme (Holtslag
and Boville 1993, as CAM3 has it): the bulk Richardson number from the lowest level up, B u*^2 in its shear, zero at h
for a parcel carrying the thermals' excess b (w'theta_v')_0 / w_m. zumin keeps its other use, the least wind shear in
vdiff's diffusivities. Gravity, the gas constant, kappa and the vapour's share of the gas constant are the model's own;
the gust's and the depth rule's constants are dimensionless but for u_min.

`surface_transfer` is surflx's transfer on one of PlaSim's columns, with or without the gust; `gust_column` the depth and
convective velocity of a column. Arrays run top first, as PlaSim's levels do.

Brought from Terluna's climate/gcm/surface_gust.py at 39c5ee04 (python/provenance.json): the patch's Fortran is in
models/exoplasim/patches/, and this module includes the parts of Terluna's pbl_scheme.py and pbl_fortran.py that the
depth rule shares, those modules staying in Terluna.
"""
from __future__ import annotations

import math

import numpy as np

from shared.constants import EXOPLASIM_VON_KARMAN

KARMAN = EXOPLASIM_VON_KARMAN  # fluxmod's vonkarman, 0.4
STABILITY = 5.0          # fluxmod's vdiff_b = vdiff_c = vdiff_d, the Louis-ECHAM stability constants
GUST_BETA = 1.0          # the gust's factor on w*: CM1's vconvc (sfclay.F), Beljaars (1995)
GUST_UMIN = 0.1          # m/s: the least wind in CM1's bulk formulas (sfclay.F)
EXOPLASIM_ZUMIN = 1.0    # fluxmod's zumin, compared there with the squared wind (m2/s2), so 1 m/s
EXOPLASIM_CFREE = 0.0016  # m s-1 K-1/3: Miller, Beljaars and Palmer's constant, in surflx

# The depth rule's constants, each dimensionless, with its source (Holtslag and Boville 1993, HB93; CAM3's technical
# description, Collins and others 2004, and CAM's hb_diff.F90; Hong, Noh and Dudhia 2006, YSU): the five of Terluna's
# nonlocal scheme (pbl_scheme.PARAMETERS) that the depth reads, under the names fluxmod gives them.
PARAMETERS = dict(
    b_excess=8.5,           # pbl_b: thermals' excess b (w'theta_v')_0 / w_m: HB93 (3.12), (A14), b = 0.85 d; CAM fak
    eps_surface=0.1,        # pbl_eps: the surface layer's share of h: HB93 (A13); CAM sffrac
    beta_m=15.0,            # pbl_betam: phi_m = (1 - 15 z/L)^(-1/3), unstable (Dyer 1974): HB93 (A8); CAM betam
    ricr_unstable=0.0,      # pbl_ricru: critical bulk Richardson number, unstable: YSU (A12), h the inversion's base
    b_ustar=100.0,          # pbl_bu: B u*^2 in the bulk number's shear: Vogelezang and Holtslag (1996) as CAM3 (4.471)
)
TINY = 1.0e-36            # CAM's least squared wind difference in the bulk number (hb_diff.F90, tiny): a numerical guard


def plasim_constants(c: dict) -> dict:
    """The constants the routines read: gravity ga, gascon, akap (gascon / acpd unless given), rdbrv, acpd and ADV."""
    out = dict(ga=float(c['ga']), gascon=float(c['gascon']), rdbrv=float(c['rdbrv']), acpd=float(c['acpd']),
               ADV=float(c.get('ADV', 0.0)))
    out['akap'] = float(c.get('akap', out['gascon'] / out['acpd']))
    return out


def full_sigma(sigmah) -> np.ndarray:
    """PlaSim's full levels, midway in sigma between the half levels that bound each layer (plasim.f90, initpm)."""
    sigmah = np.asarray(sigmah, float)
    return 0.5 * (np.r_[0.0, sigmah[:-1]] + sigmah)


def heights(t, q, sigma, sigmah, g: float, gascon: float, rdbrv: float):
    """Heights (m) above the ground of the full levels and of each layer's lower half level, from the layers' virtual
    temperatures (hydrostatic in sigma; the top layer's upper boundary, sigma 0, is left out)."""
    tv = np.asarray(t, float) * (1.0 + (1.0 / rdbrv - 1.0) * np.asarray(q, float))
    sigma, sigmah = np.asarray(sigma, float), np.asarray(sigmah, float)
    n = tv.size
    zh = np.zeros(n)
    for k in range(n - 1, 0, -1):
        zh[k - 1] = zh[k] + gascon * tv[k] / g * math.log(sigmah[k] / sigmah[k - 1])
    zf = zh + gascon * tv / g * np.log(sigmah / sigma)
    return zf, zh


def surface_from_plasim(dshfl: float, devap: float, dust3: float, ts: float, ps_pa: float, q_low: float, c: dict):
    """gustnl's arithmetic: the kinematic surface fluxes of potential temperature (K m/s) and vapour (kg/kg m/s), upward,
    and the friction velocity, from surflx's dshfl (W/m2, downward), devap (m/s of water, downward) and dust3 (u*^3),
    the surface temperature, the surface pressure and the lowest level's vapour before this step."""
    rho = ps_pa / (c['gascon'] * ts)
    return dict(wth0=-dshfl / (rho * c['acpd'] * max(1.0, 1.0 + c['ADV'] * q_low)), wq0=-1000.0 * devap / rho,
                ustar=dust3 ** (1.0 / 3.0))


def bulk_depth(u, v, thv, zf, thref: float, ricr: float, ustar: float, g: float, b_ustar: float) -> float:
    """The depth rule (CAM's pblintd): the bulk Richardson number between the lowest level and each level above,
    g (thv_k - thref) (z_k - z_n) / (thv_n (|V_k - V_n|^2 + b u*^2)), from the lowest level up; h where it reaches ricr,
    linear in the number between levels, or the top level's height."""
    nb = len(thv) - 1
    ri_below = 0.0
    for k in range(nb - 1, -1, -1):
        vvk = max((u[k] - u[nb]) ** 2 + (v[k] - v[nb]) ** 2 + b_ustar * ustar * ustar, TINY)
        ri = g * (thv[k] - thref) * (zf[k] - zf[nb]) / (thv[nb] * vvk)
        if ri >= ricr:
            if ri - ri_below <= 0.0:
                return float(zf[k + 1])
            return float(zf[k + 1] + (ricr - ri_below) / (ri - ri_below) * (zf[k] - zf[k + 1]))
        ri_below = ri
    return float(zf[0])


def gust_column(t, q, u, v, sigma, sigmah, wth0: float, wq0: float, ustar: float, c: dict, prm=PARAMETERS) -> dict:
    """One column's boundary-layer depth h (m) and convective velocity w* = (g / thv_n * (w'thv')0 * h)^(1/3) (m/s) in
    unstable air, from its state (top first), its kinematic surface fluxes of potential temperature (K m/s) and vapour
    (kg/kg m/s), upward, and its friction velocity; h and w* are 0 in stable or neutral air. The depth is the nonlocal
    scheme's in unstable air: a first depth from the lowest level's own thv, w_m = (u*^3 + beta_m eps kappa B h)^(1/3)
    from it, and the depth again for a parcel carrying the excess b (w'thv')0 / w_m."""
    c = plasim_constants(c)
    g, gascon, akap, rdbrv = c['ga'], c['gascon'], c['akap'], c['rdbrv']
    t, q, u, v = (np.asarray(a, float) for a in (t, q, u, v))
    sigma, sigmah = np.asarray(sigma, float), np.asarray(sigmah, float)
    nb = t.size - 1
    eps_v = 1.0 / rdbrv - 1.0
    theta = t / sigma ** akap
    thv = theta * (1.0 + eps_v * q)
    zf, _ = heights(t, q, sigma, sigmah, g, gascon, rdbrv)
    wthv0 = wth0 * (1.0 + eps_v * q[nb]) + eps_v * theta[nb] * wq0
    if not wthv0 > 0.0:
        return dict(unstable=False, wthv0=float(wthv0), h=0.0, wstar=0.0)
    buoy = g / thv[nb] * wthv0
    depth = lambda thref: bulk_depth(u, v, thv, zf, thref, prm['ricr_unstable'], ustar, g, prm['b_ustar'])
    h0 = depth(thv[nb])
    wm0 = (ustar ** 3 + prm['beta_m'] * prm['eps_surface'] * KARMAN * buoy * h0) ** (1.0 / 3.0)
    excess = prm['b_excess'] * wthv0 / wm0
    h = depth(thv[nb] + excess)
    return dict(unstable=True, wthv0=float(wthv0), buoyancy=float(buoy), h_first=h0, excess=float(excess), h=h,
                wstar=float((buoy * h) ** (1.0 / 3.0)))


def surface_transfer(col: dict, sigma, sigmah, c: dict, ngust: int = 0, cfree: float = EXOPLASIM_CFREE,
                     zumin: float = EXOPLASIM_ZUMIN, b: float = STABILITY, cc: float = STABILITY,
                     d: float = STABILITY, beta: float = GUST_BETA, umin: float = GUST_UMIN,
                     prm=PARAMETERS) -> dict:
    """surflx's transfer on one column (ntsa 2), step for step. col holds PlaSim's dt and dq (the levels top first, then
    the surface's), du and dv (the levels), dz0 (m), dls (the land share: below 1 the column counts as water), dp (Pa),
    and the surface fluxes of the step before: dshfl (W/m2) and devap (m/s of water), downward, and dust3 (u*^3).
    Returns the squared wind in the bulk formulas (m2/s2), the lowest level's height, the bulk Richardson number, the
    factors F_h and F_m, the transfer coefficients dtransh and dtransm (m/s) and, with the gust, its h and w*."""
    c = plasim_constants(c)
    ga, gascon, akap, rdbrv = c['ga'], c['gascon'], c['akap'], c['rdbrv']
    sigma, sigmah = np.asarray(sigma, float), np.asarray(sigmah, float)
    n = sigma.size
    dt, dq = np.asarray(col['dt'], float), np.asarray(col['dq'], float)
    du, dv = np.asarray(col['du'], float), np.asarray(col['dv'], float)
    eps_v = 1.0 / rdbrv - 1.0
    dtsa = dt[n - 1] * sigma[n - 1] ** (-akap) * (1.0 + eps_v * dq[n - 1])
    wind2 = du[n - 1] * du[n - 1] + dv[n - 1] * dv[n - 1]
    out = dict(h=0.0, wstar=0.0)
    if ngust == 1:
        s = surface_from_plasim(col['dshfl'], col['devap'], col['dust3'], dt[n], col['dp'], dq[n - 1], c)
        gust = gust_column(dt[:n], dq[:n], du, dv, sigma, sigmah, s['wth0'], s['wq0'], s['ustar'], c, prm)
        out.update(h=gust['h'], wstar=gust['wstar'])
        absu2 = max(umin * umin, wind2 + (beta * gust['wstar']) ** 2)
    else:
        absu2 = max(zumin, wind2)
    znl = -gascon * 0.5 * (dt[n - 1] + dtsa) * np.log(sigma[n - 1]) / ga
    bz0 = znl / col['dz0']
    ri = ga * znl / (absu2 * dtsa) * (dtsa - dt[n] * (1.0 + eps_v * dq[n]))
    kblnz2 = (KARMAN / np.log(bz0 + 1.0)) ** 2
    if ri <= 0.0:
        denom = 1.0 + 3.0 * cc * b * np.sqrt(-1.0 * ri * (bz0 + 1.0)) * kblnz2
        rifm = 1.0 - 2.0 * b * ri / denom
        if col['dls'] < 1.0 and ngust != 1:
            dth = -(dtsa - dt[n] * (1.0 + eps_v * dq[n]))
            rifh = (1.0 + (cfree * dth ** (1.0 / 3.0) / np.sqrt(absu2) / kblnz2) ** 1.25) ** 0.8
        else:
            rifh = 1.0 - 3.0 * b * ri / denom
    else:
        denom = np.sqrt(1 + d * ri)
        rifh = 1.0 / (1.0 + 3.0 * b * ri * denom)
        rifm = 1.0 / (1.0 + 2.0 * b * ri / denom)
    trans = np.sqrt(absu2) * kblnz2
    out.update(absu2=float(absu2), znl=float(znl), ri=float(ri), rifh=float(rifh), rifm=float(rifm),
               dtransh=float(trans * rifh), dtransm=float(trans * rifm), dtsa=float(dtsa))
    return out
