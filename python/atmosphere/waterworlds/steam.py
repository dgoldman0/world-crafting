"""Columns of steam alone, saturated at every height above a waterworld's ocean or ice.

The air is water vapour in equilibrium with the surface reservoir, so its pressure at the surface is the vapour
pressure at the surface temperature and its temperature follows the vapour curve at every pressure above, as
Arnscheidt, Wordsworth and Ding (2019, section 2.3) set it: over liquid water at or above 273.16 K and over ice below,
by the radiative-convective column's own curves (Wagner and Pruss 2002; Wagner et al. 2011). The column's levels are
one grid of pressures, fixed per decade from the top down, below the surface's own pressure, so that columns of
every surface temperature and gravity share their layers' states above their lowest layer, and with them the
layers' cross-sections. Heights follow from hydrostatic balance with gravity falling as GM/r^2, as in the paper's
eq. 3. The layers' masses, from which their optical depths follow, are computed either with the same gravity at each
layer's middle height ('local') or with the surface's ('surface'), the usual choice of a plane-parallel radiative
transfer. The paper's authors computed their heights from eq. 3 after a radiative transfer for a given surface
gravity, and the comparison with their Figure 3 suggests that its optical depths took the surface's gravity
(notes/waterworlds.md).

Above the critical radius of the isothermal wind at the surface temperature the steam flows outward faster than
sound and stands hydrostatic no longer, so a column ends at the last level below that radius where the grid's top
lies beyond it, as it does at low gravity and high temperature.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from atmosphere.radiative_convective.thermodynamics import (DryAir, R_VAPOUR, TRIPLE_POINT_K, column_from_levels,
                                                             latent_heat, saturation_pressure)
from atmosphere.waterworlds import escape as es
from atmosphere.waterworlds.body import Waterworld

# The air of a steam column: column_from_levels weighs the dry part of each layer by (1 - x_H2O), which is zero.
STEAM_AIR = DryAir(1.0)
_T_TABLE = np.linspace(100.0, 647.0, 54_701)
_LNP_TABLE = np.log(saturation_pressure(_T_TABLE))


def saturation_temperature(p_pa):
    """The temperature, K, at which water's vapour pressure (over ice below 273.16 K) equals p_pa."""
    lnp = np.log(np.asarray(p_pa, dtype=float))
    if np.any(lnp < _LNP_TABLE[0]) or np.any(lnp > _LNP_TABLE[-1]):
        raise ValueError('the pressure lies outside the vapour curve from 100 K to 647 K')
    t = np.interp(lnp, _LNP_TABLE, _T_TABLE)
    for _ in range(3):           # Newton steps on ln p, whose slope is L / (R_v T^2)
        t = t - (np.log(saturation_pressure(t)) - lnp) * R_VAPOUR * t * t / latent_heat(t)
    return t


@dataclass(frozen=True)
class Levels:
    """The shared grid of pressures: `per_decade` levels in each decade, from `top_pa` down to the surface."""
    top_pa: float = 1e-2
    per_decade: int = 10
    sliver: float = 0.05         # a grid level within this share of a decade above the surface is dropped

    def pressures(self, surface_pa: float) -> np.ndarray:
        """The column's level pressures, Pa, the surface first."""
        if not surface_pa > self.top_pa:
            raise ValueError(f'the surface pressure {surface_pa!r} Pa lies above the top, {self.top_pa!r} Pa')
        top = round(math.log10(self.top_pa) * self.per_decade)
        bottom = math.floor(math.log10(surface_pa) * self.per_decade - self.sliver * self.per_decade)
        grid = 10.0 ** (np.arange(bottom, top - 1, -1) / self.per_decade)
        return np.concatenate([[surface_pa], grid[grid < surface_pa]])


OPTICAL_GRAVITIES = ('local', 'surface')


def column(world: Waterworld, t_s: float, levels: Levels = Levels(), *, optical_gravity: str = 'local') -> dict:
    """The saturated steam column over a surface at t_s, as the radiative-convective column's dictionary, its heights
    from gravity falling as GM/r^2 and its layers' masses from the `optical_gravity` named."""
    if optical_gravity not in OPTICAL_GRAVITIES:
        raise ValueError(f'optical_gravity is one of {OPTICAL_GRAVITIES}, where it is {optical_gravity!r}')
    p = levels.pressures(float(saturation_pressure(t_s)))
    t = saturation_temperature(p)
    t[0] = t_s
    keep = below_critical_radius(world, t_s, p, t)
    capped = keep < p.size
    p, t = p[:keep], t[:keep]
    col = column_from_levels(world.planet, STEAM_AIR, p, t, np.ones_like(p))
    if optical_gravity == 'surface':
        flat = column_from_levels(world.planet, STEAM_AIR, p, t, np.ones_like(p), constant_gravity=True)
        col.update(layer_mass_kg_m2=flat['layer_mass_kg_m2'], layer_column_cm2=flat['layer_column_cm2'])
    col.update(surface_temperature_k=t_s, world=world, over='liquid' if t_s >= TRIPLE_POINT_K else 'ice',
               optical_gravity=optical_gravity, top_pa=float(p[-1]), capped=bool(capped))
    return col


def below_critical_radius(world: Waterworld, t_s: float, p: np.ndarray, t: np.ndarray) -> int:
    """How many of the levels, the surface first, stand below the critical radius of the isothermal wind at t_s, by
    the geopotential column_from_levels integrates; at least the surface and one level above it."""
    dphi = -0.5 * R_VAPOUR * (t[1:] + t[:-1]) * np.diff(np.log(p))
    phi = np.concatenate([[0.0], np.cumsum(dphi)])
    r_s, r_c = world.radius_m, es.critical_radius(world, t_s)
    # A level stands below r_c where its geopotential is below g_s r_s (r_c - r_s) / r_c.
    below = phi < world.gravity_m_s2 * r_s * (r_c - r_s) / r_c
    return max(2, int(np.argmin(below)) if not below.all() else p.size)
