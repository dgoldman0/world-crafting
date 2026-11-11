"""CM1's surface-layer similarity over water in PlaSim's surface transfer, beside Beljaars's gust: the Python copy of
models/exoplasim/patches/13-similarity-over-water.patch (the record is notes/exoplasim.md, "The gust and the
similarity over water").

PlaSim's surflx (fluxmod.f90) gives each surface its transfer of heat and vapour |U| C_N F_h and of momentum |U| C_N F_m,
C_N = (kappa / ln(z_l / z0 + 1))^2 at its lowest level's height z_l and F the Louis-ECHAM factors of the bulk Richardson
number; with Beljaars's gust (surface_gust.py, ngust 1) |U| includes the boundary layer's convective velocity. Set beside
Monin-Obukhov similarity integrated to the same height on the same air and wind, that transfer evaporated 0.72 of the
similarity's over the air of Terluna's Near-side Sea box and 0.82 over its GCM's own, most of the difference in light
wind over warm water, where similarity's free-convection functions and its roughness lengths for heat and vapour transfer
more than Louis's factors and one Charnock roughness. With nsimw 1 (fluxmod), over ice-free water the transfer comes
from CM1's own surface layer (sfclay.F, sfcmodel 2 with isftcflx 0), carried to the lowest level's height:

- the bulk Richardson number Ri_b = g/theta z_l (thv_l - thv_s) / U^2 sets the regime: psi = -10 ln(z_l/z0) at least
  -10 for Ri_b >= 0.2, -5 Ri_b ln(z_l/z0) / (1.1 - 5 Ri_b) at least -10 below it, nil at Ri_b = 0, and in unstable air
  Paulson's functions of z_l/L from CM1's tables at steps of 0.01, at most 0.9 ln(z_l/z0), z_l/L from the step before's
  u* and temperature scale; air that was unstable the step before stays out of the stable regimes;
- Charnock's roughness 0.0185 u*^2/g at the planet's gravity with the smooth-flow term 0.11 nu/u*, at most 2.85 mm, and
  Fairall's roughness for heat and vapour 5.5e-5 (u* z0/nu)^-0.6 within 2e-9 and 1e-4 m,
  psi_q = max(ln((z_l + z0q)/z0q) - psi_h, 2);
- u* = (u*_old + kappa U/(ln(z_l/z0) - psi_m)) / 2 as CM1 averages it, the temperature scale kappa (theta_l - theta_s)/psi_q,
  and the roughness from the new u*, each carried to the next step as CM1 carries UST, MOL and ZNT;
- the transfer velocities kappa u*/psi_q for heat and vapour and u*^2/U for momentum, U the gust's wind at least 0.1 m/s.

The air's kinematic viscosity nu is the world's: its dynamic viscosity by Sutherland's law over the density that the
surface pressure, the gas constant and the lowest level's temperature give (`kinematic_viscosity`). CM1's code sets
the viscosity of Earth's sea-level air there, (1.32 + 0.009 (T - 273.15)) 1e-5 m2/s in the Reynolds number and 1.5e-5
m2/s in the smooth-flow term (`cm1_viscosity`), as Terluna's module did. Charnock's constant, the 2.85 mm cap,
Fairall's roughness and Paulson's functions stay Earth's.

These enter surflx as its stability factors against the neutral |U| C_N, so mkstress, mkshfl, mkevap and the debug
output take them unchanged. Land, sea ice and partly frozen sea keep PlaSim's transfer. CM1's subgrid wind (Mahrt and
Sun's, 0.19 m/s at its 6 km grid) is left out. `similarity_column` is one step of one column (simwcol in Fortran);
`surface_transfer` is surflx's transfer with it.

Brought from Terluna's climate/gcm/surface_similarity.py at 39c5ee04 (python/provenance.json): the patch's Fortran
is in models/exoplasim/patches/, and the viscosity is derived for the world.
"""
from __future__ import annotations

import math

import numpy as np

from climate.gcm import surface_gust as sg

KARMAN = 0.4                     # CM1's karman and PlaSim's vonkarman
CHARNOCK = 0.0185                # sfclay's CZO
SMOOTH = 0.11                    # sfclay's smooth-flow roughness, 0.11 nu/u*
Z0_MAX = 2.85e-3                 # m: sfclay's cap on the roughness over water, Earth's
Z0Q_COEFF, Z0Q_EXPONENT = 5.5e-5, -0.60    # Fairall's roughness for heat and vapour (m), on the roughness Reynolds number
Z0Q_MIN, Z0Q_MAX = 2.0e-9, 1.0e-4
PSI_FLOOR = 2.0                  # sfclay's least psi_q
ZOL_MIN = -9.9999                # its range of z/L in unstable air
WIND_MIN = 0.1                   # m/s: its least wind
START = dict(ust=0.1, mol=0.0, z0=1.0e-4)   # the state before a column's first step
# Sutherland's law for the dynamic viscosity of Earth's dry air, mu = B T^1.5 / (T + S), with the constants of the
# 1976 US Standard Atmosphere (fluxmod's simw_mub and simw_mus).
SUTHERLAND_B = 1.458e-6          # kg m-1 s-1 K-1/2
SUTHERLAND_S = 110.4             # K


def kinematic_viscosity(t: float, p_pa: float, gascon: float, b: float = SUTHERLAND_B, s: float = SUTHERLAND_S) -> float:
    """The air's kinematic viscosity (m2/s) at temperature t (K) and pressure p_pa (Pa): Sutherland's dynamic
    viscosity over the ideal gas's density p / (gascon t), as simwcol forms it."""
    return b * t ** 1.5 / (t + s) * gascon * t / p_pa


def cm1_viscosity(t: float) -> float:
    """CM1's kinematic viscosity of Earth's sea-level air in its roughness Reynolds number (sfclay.F), m2/s; its
    smooth-flow term holds 1.5e-5 m2/s, this line's value at 20 degrees C."""
    return (1.32 + 0.009 * (t - 273.15)) * 1.0e-5


def tables():
    """CM1's sfclayinit: Paulson's functions for momentum and heat at z/L = -0.01 n, n = 0..1000."""
    zoln = -np.arange(1001, dtype=float) * 0.01
    x = (1.0 - 16.0 * zoln) ** 0.25
    psim = 2.0 * np.log(0.5 * (1.0 + x)) + np.log(0.5 * (1.0 + x * x)) - 2.0 * np.arctan(x) + 2.0 * np.arctan(1.0)
    psih = 2.0 * np.log(0.5 * (1.0 + (1.0 - 16.0 * zoln) ** 0.5))
    return psim, psih


PSIM_TABLE, PSIH_TABLE = tables()


def similarity_column(za: float, tha: float, thg: float, thva: float, thvg: float, visc: float, absu: float, g: float,
                      state: dict = START) -> dict:
    """One step of CM1's surface layer over water on one column (simwcol, line for line): the lowest level's height za
    (m), its potential and virtual potential temperature tha and thva against the surface's thg and thvg (K, on one
    reference pressure), the air's kinematic viscosity visc (m2/s), the wind in the bulk formulas absu (m/s) and
    gravity g, from the state of the step before (u*, the temperature scale and the roughness). Returns the transfer
    velocities of heat and vapour (transh) and of momentum (transm), the parts, and the state for the next step."""
    ust, mol, znt = float(state['ust']), float(state['mol']), float(state['z0'])
    gz1oz0 = math.log(za / znt)
    wspd = max(absu, WIND_MIN)
    br = g / tha * za * (thva - thvg) / (wspd * wspd)
    if mol < 0.0:
        br = min(br, 0.0)
    if br >= 0.2:
        regime = 1
        psim = max(-10.0 * gz1oz0, -10.0)
        psih = psim
    elif br > 0.0:
        regime = 2
        psim = max(-5.0 * br * gz1oz0 / (1.1 - 5.0 * br), -10.0)
        psih = psim
    elif br == 0.0:
        regime = 3
        psim = 0.0
        psih = 0.0
    else:
        regime = 4
        zol = br * gz1oz0 if ust < 0.01 else KARMAN * g / tha * za * mol / (ust * ust)
        zol = max(min(zol, 0.0), ZOL_MIN)
        n = int(-zol * 100.0)
        r = -zol * 100.0 - n
        psim = PSIM_TABLE[n] + r * (PSIM_TABLE[n + 1] - PSIM_TABLE[n])
        psih = PSIH_TABLE[n] + r * (PSIH_TABLE[n + 1] - PSIH_TABLE[n])
        psih = min(psih, 0.9 * gz1oz0)
        psim = min(psim, 0.9 * gz1oz0)
    psix = gz1oz0 - psim
    restar = ust * znt / visc
    z0q = min(max(Z0Q_COEFF * restar ** Z0Q_EXPONENT, Z0Q_MIN), Z0Q_MAX)
    psiq = max(math.log((za + z0q) / z0q) - psih, PSI_FLOOR)
    ust = 0.5 * ust + 0.5 * KARMAN * wspd / psix
    mol = KARMAN * (tha - thg) / psiq
    znt = min(CHARNOCK * ust * ust / g + SMOOTH * visc / ust, Z0_MAX)
    return dict(transh=ust * KARMAN / psiq, transm=ust * ust / wspd, regime=regime, br=br, psim=float(psim),
                psih=float(psih), psix=psix, psiq=psiq, z0q=z0q, wspd=wspd, state=dict(ust=ust, mol=mol, z0=znt))


def applies(col: dict) -> bool:
    """Ice-free water: PlaSim's land share below 1 and no ice cover."""
    return col['dls'] < 1.0 and col.get('dicec', 0.0) <= 0.0


def surface_transfer(col: dict, sigma, sigmah, c: dict, state: dict = START, nsimw: int = 1, **gust) -> dict:
    """surflx's transfer with the gust (surface_gust.surface_transfer, ngust 1) and, with nsimw 1 over ice-free water,
    CM1's similarity in its place, entered as the stability factors against PlaSim's neutral transfer; col as
    surface_gust takes it, with dicec its ice cover (0 if absent). The viscosity is the world's, from the column's
    surface pressure, the gas constant and the lowest level's temperature."""
    out = sg.surface_transfer(col, sigma, sigmah, c, ngust=1, **gust)
    if nsimw != 1 or not applies(col):
        return out
    cc = sg.plasim_constants(c)
    sigma = np.asarray(sigma, float)
    n = sigma.size
    dt, dq = np.asarray(col['dt'], float), np.asarray(col['dq'], float)
    eps_v = 1.0 / cc['rdbrv'] - 1.0
    tha = dt[n - 1] * sigma[n - 1] ** (-cc['akap'])
    visc = kinematic_viscosity(dt[n - 1], col['dp'], cc['gascon'])
    s = similarity_column(out['znl'], tha, dt[n], tha * (1.0 + eps_v * dq[n - 1]), dt[n] * (1.0 + eps_v * dq[n]),
                          visc, math.sqrt(out['absu2']), cc['ga'], state)
    ztrans = math.sqrt(out['absu2']) * (KARMAN / math.log(out['znl'] / col['dz0'] + 1.0)) ** 2
    rifh, rifm = s['transh'] / ztrans, s['transm'] / ztrans
    out.update(rifh=rifh, rifm=rifm, dtransh=ztrans * rifh, dtransm=ztrans * rifm, similarity=s, viscosity=visc)
    return out
