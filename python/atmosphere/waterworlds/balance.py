"""The energy balance of a waterworld under steam, after Arnscheidt, Wordsworth and Ding (2019, eqs. 2 and 12).

Sunlight absorbed at the absorbing surface's radius, less the energy the wind carries away, balances the outgoing
longwave emitted from the emitting surface's radius, per unit area of the planet's surface:

    (r_SW / r_s)^2 (1 - A) F / 4 - (g_s r_s + L) Phi = (r_LW / r_s)^2 F_out          (eq. 2),

so that the instellation holding a surface at T_s is

    F(T_s) = [(r_LW / r_s)^2 F_out + (g_s r_s + L) Phi] / [(r_SW / r_s)^2 (1 - A) / 4]  (eq. 12).

A is the planetary albedo, the paper's 0.2 for a surface of open water and clouds. For its hysteresis the paper steps
A to the ice's albedo below 273 K (eq. 13); the step is handled here as two branches, the water's curve F(T_s) at 0.2
holding at and above 273 K and the ice's at its own albedo below, each computed with its albedo over the whole table,
so that no interpolation runs across the jump. Phi is the wind's flux of escape.py. L is the heat that turns the
surface's water into the escaping vapour: over liquid water, the heat of vaporisation by the Clapeyron equation with
the saturated liquid's and vapour's densities of Wagner and Pruss (2002, eqs. 2.6 and 2.7); over ice, below
273.16 K, the heat of sublimation from the ice's vapour curve, the vapour there an ideal gas. The paper names the heat
of vaporisation and leaves its value unstated.
"""
from __future__ import annotations

import numpy as np

from atmosphere.radiative_convective.thermodynamics import (R_VAPOUR, TRIPLE_POINT_K, latent_heat,
                                                             saturation_pressure)
from atmosphere.waterworlds import escape as es
from atmosphere.waterworlds.body import Waterworld

ALBEDO = 0.2
FREEZING_K = 273.0          # the paper's boundary between open water and a snowball

# Wagner and Pruss (2002), J. Phys. Chem. Ref. Data 31, 387, eqs. 2.6 and 2.7: the saturated liquid's and vapour's
# densities from the triple point to the critical point.
_TC, _RHOC = 647.096, 322.0
_LIQUID = ((1.99274064, 1 / 3), (1.09965342, 2 / 3), (-0.510839303, 5 / 3), (-1.75493479, 16 / 3),
           (-45.5170352, 43 / 3), (-6.74694450e5, 110 / 3))
_VAPOUR = ((-2.03150240, 2 / 6), (-2.68302940, 4 / 6), (-5.38626492, 8 / 6), (-17.2991605, 18 / 6),
           (-44.7586581, 37 / 6), (-63.9201063, 71 / 6))


def saturated_densities(t: float) -> tuple[float, float]:
    """The saturated liquid's and vapour's densities, kg/m^3, at or above 273.16 K (Wagner and Pruss 2002)."""
    tau = 1 - t / _TC
    liquid = _RHOC * (1 + sum(b * tau ** e for b, e in _LIQUID))
    vapour = _RHOC * np.exp(sum(c * tau ** e for c, e in _VAPOUR))
    return float(liquid), float(vapour)


def escape_heat(t_s: float) -> float:
    """L, J/kg: the heat of vaporisation over liquid water, T (1/rho_v - 1/rho_l) dp/dT, and of sublimation over ice."""
    if t_s < TRIPLE_POINT_K:
        return float(latent_heat(t_s))
    liquid, vapour = saturated_densities(t_s)
    # latent_heat is R_v T^2 dln(p)/dT of the vapour curve, so dp/dT = p latent_heat / (R_v T^2).
    dp_dt = float(saturation_pressure(t_s)) * float(latent_heat(t_s)) / (R_VAPOUR * t_s * t_s)
    return t_s * (1 / vapour - 1 / liquid) * dp_dt


def escape_power(world: Waterworld, t_s: float, factor: float = 1.0) -> float:
    """(g_s r_s + L) Phi, W/m^2: the power per unit area of surface that lifts and evaporates the escaping water."""
    return (world.gravity_m_s2 * world.radius_m + escape_heat(t_s)) * es.mass_flux(world, t_s, factor)


def instellation(world: Waterworld, t_s: float, olr: float, lw_factor: float, sw_factor: float, *,
                 albedo: float = ALBEDO, factor: float = 1.0) -> float:
    """F(T_s), W/m^2, the instellation at which the surface stays at t_s (eq. 12)."""
    return (lw_factor * olr + escape_power(world, t_s, factor)) / (sw_factor * (1 - albedo) / 4)


def steady_temperatures(flux: float, t_grid, f_grid) -> list[float]:
    """Every surface temperature at which F(T_s) = flux, by linear interpolation between the table's points; a point
    the curve meets exactly counts once."""
    t_grid, f_grid = np.asarray(t_grid, dtype=float), np.asarray(f_grid, dtype=float)
    d = f_grid - flux
    roots = []
    for i in range(len(t_grid) - 1):
        if d[i] == 0:
            roots.append(float(t_grid[i]))
        elif d[i] * d[i + 1] < 0:
            roots.append(float(t_grid[i] - d[i] * (t_grid[i + 1] - t_grid[i]) / (d[i + 1] - d[i])))
    if d[-1] == 0:
        roots.append(float(t_grid[-1]))
    return roots


def branch_temperatures(flux: float, t_grid, f_water, f_ice, freezing: float = FREEZING_K) -> dict:
    """The steady temperatures of the paper's hysteresis (eq. 13): the water's at and above `freezing` on the curve
    at the water's albedo, and the ice's below it on the curve at the ice's albedo."""
    water = [t for t in steady_temperatures(flux, t_grid, f_water) if t >= freezing]
    ice = [t for t in steady_temperatures(flux, t_grid, f_ice) if t < freezing]
    return dict(water=water, ice=ice)
