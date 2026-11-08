"""The isothermal transonic wind of steam from a waterworld, after Arnscheidt, Wordsworth and Ding (2019).

The wind leaves a surface of saturated steam at the surface temperature T_s and stays at that temperature, so that
its sound speed is w_c = sqrt(f k T_s / m), with f = 1 for the isothermal sound speed of the paper (section 2.4). It
passes that speed at the critical radius r_c = GM / (2 w_c^2) (eq. 8). Integrating the wind equation (eq. 7) from
the surface to r_c, with the kinetic term at the surface dropped, gives the mass flux at the surface,

    Phi = rho_s w_c (r_c / r_s)^2 exp(-1/2 + GM / w_c^2 (1 / r_c - 1 / r_s))      (eq. 9),

where rho_s is the density of saturated steam at T_s, an ideal gas at the vapour pressure over liquid water at or
above 273.16 K and over ice below. The world loses 4 pi r_s^2 Phi each second (eq. 10), and its water lasts its mass
over that rate (eq. 11). Appendix A gives the integrated wind equation (eq. A3), the wind's speed below the critical
radius with its kinetic term dropped (eq. A4) and its inertia against gravity (eq. A5), with which the paper checks
that the air stands hydrostatic up to its radiating surfaces. Equation numbers are those of the arXiv version.

The derivation holds where the critical radius lies above the surface, as it does across the size relation's range
up to water's critical temperature, at the isothermal sound speed and at the factors of the comparison; the flux
refuses other cases. f is 1 for the paper's equations as printed; notes/waterworlds.md records the values with which
eq. 9 gives the water lifetimes of the paper's figures.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq
from scipy.special import lambertw

from shared.constants import AVOGADRO, BOLTZMANN, JULIAN_DAY, JULIAN_YEAR_DAYS
from atmosphere.radiative_convective.thermodynamics import MOLAR_MASS, saturation_pressure
from atmosphere.waterworlds.body import WATER_MASS_FRACTION, Waterworld

WATER_MOLECULE_KG = MOLAR_MASS['H2O'] / AVOGADRO
YEAR_S = JULIAN_YEAR_DAYS * JULIAN_DAY          # the paper leaves its year unstated
# The size relation's range, 0.01 to 1 Earth mass (Sotin et al. 2007), in surface gravity.
RELATION_GRAVITY = (Waterworld(0.01).gravity_m_s2, Waterworld(1.0).gravity_m_s2)


def sound_speed(t_s: float, factor: float = 1.0) -> float:
    """The wind's sound speed w_c, m/s, at the surface temperature (the isothermal one where factor is 1)."""
    if not factor > 0:
        raise ValueError(f'the sound speed takes a positive factor, where it has {factor!r}')
    return math.sqrt(factor * BOLTZMANN * t_s / WATER_MOLECULE_KG)


def critical_radius(world: Waterworld, t_s: float, factor: float = 1.0) -> float:
    """r_c = GM / (2 w_c^2), m, where the wind reaches its sound speed (eq. 8)."""
    return world.gm_m3_s2 / (2 * sound_speed(t_s, factor) ** 2)


def surface_density(t_s: float) -> float:
    """Saturated steam's density at the surface, kg/m^3, as an ideal gas."""
    return float(saturation_pressure(t_s)) * WATER_MOLECULE_KG / (BOLTZMANN * t_s)


def mass_flux(world: Waterworld, t_s: float, factor: float = 1.0) -> float:
    """Phi, kg m^-2 s^-1, the wind's mass flux through the surface (eq. 9)."""
    w_c, r_s = sound_speed(t_s, factor), world.radius_m
    r_c = critical_radius(world, t_s, factor)
    if not r_c > r_s:
        raise ValueError(f'the critical radius, {r_c:.4g} m, lies at or below the surface, {r_s:.4g} m, where eq. 9 '
                         'has no derivation')
    exponent = -0.5 + world.gm_m3_s2 / w_c ** 2 * (1 / r_c - 1 / r_s)
    return surface_density(t_s) * w_c * (r_c / r_s) ** 2 * math.exp(exponent)


def loss_rate(world: Waterworld, t_s: float, factor: float = 1.0) -> float:
    """The world's loss of water, kg/s (eq. 10)."""
    return 4 * math.pi * world.radius_m ** 2 * mass_flux(world, t_s, factor)


def water_lifetime(world: Waterworld, t_s: float, factor: float = 1.0) -> float:
    """The time, s, in which the wind takes the world's water at its present rate (eq. 11); infinite where the loss
    falls below the smallest floating-point number."""
    rate = loss_rate(world, t_s, factor)
    return world.water_mass_kg / rate if rate > 0 else math.inf


def lifetime_gravity(t_s: float, lifetime_s: float, factor: float = 1.0, *,
                     water_mass_fraction: float = WATER_MASS_FRACTION) -> float:
    """The surface gravity, m/s^2, at which a world of the size relation keeps its water `lifetime_s` at `t_s`.

    Over the relation's range of 0.01 to 1 Earth mass, worlds of higher gravity keep their water longer. At the
    paper's 273 K and 10^9 years this gravity is the paper's transition from planet-like to comet-like worlds
    (section 3.3), where the 273 K contour meets the lifetime's.
    """
    def excess(g):
        return math.log(water_lifetime(Waterworld.from_gravity(g, water_mass_fraction), t_s, factor) / lifetime_s)
    low, high = RELATION_GRAVITY
    if excess(low) > 0 or excess(high) < 0:
        raise ValueError(f'at {t_s} K no world of the relation\'s range, {low:.3f} to {high:.3f} m/s^2, keeps its '
                         f'water {lifetime_s:.4g} s')
    return brentq(excess, low, high, xtol=1e-12, rtol=1e-12)


def outflow_speed(world: Waterworld, t_s: float, r, factor: float = 1.0):
    """The wind's speed w(r), m/s, below the critical radius, by eq. A4, in which the kinetic term is dropped."""
    w_c, r_c = sound_speed(t_s, factor), critical_radius(world, t_s, factor)
    r = np.asarray(r, dtype=float)
    return w_c * (r_c / r) ** 2 * np.exp(1.5 - 2 * r_c / r)


def transonic_speed(world: Waterworld, t_s: float, r, factor: float = 1.0):
    """The wind's speed w(r), m/s, below the critical radius, from the integrated wind equation in full:
    ln(w/w_c) - (w/w_c)^2 / 2 = -2 r_c/r - 2 ln(r/r_c) + 3/2 (eq. A3), solved on its subsonic branch."""
    w_c, r_c = sound_speed(t_s, factor), critical_radius(world, t_s, factor)
    r = np.asarray(r, dtype=float)
    if np.any(r > r_c):
        raise ValueError('the subsonic branch holds below the critical radius')
    # With u = (w/w_c)^2: ln u - u = 2 rhs, so u = -W0(-exp(2 rhs)). Far below r_c, u = exp(2 rhs + u) differs
    # from exp(2 rhs) by less than one part in 10^13, and the exponential alone keeps its precision.
    log_arg = 2 * (-2 * r_c / r - 2 * np.log(r / r_c) + 1.5)
    deep = log_arg < -30
    u = -np.real(lambertw(-np.exp(np.where(deep, -30.0, log_arg)), 0))
    # Near r_c the argument nears -1/e, W0's branch point, where W0 = -1 + p - p^2/3 + 11 p^3/72 - ... with
    # p = sqrt(2 (1 - exp(2 rhs + 1))) and, for r = r_c (1 + e), 2 rhs + 1 = 4 e / (1 + e) - 4 ln(1 + e), written so
    # that nothing cancels. The series serves where p < 1e-3, to 1e-13.
    e = r / r_c - 1
    p = np.sqrt(2 * np.maximum(-np.expm1(4 * e / (1 + e) - 4 * np.log1p(e)), 0.0))
    u = np.where(p < 1e-3, 1 - p + p * p / 3 - 11 * p ** 3 / 72, u)
    return w_c * np.where(deep, np.exp(0.5 * log_arg), np.sqrt(u))


def inertia_ratio(world: Waterworld, t_s: float, r, factor: float = 1.0):
    """|w dw/dr| / g(r) by eq. A5: the wind's inertia against gravity. Where this ratio is far below one, the air
    stands hydrostatic."""
    w_c, r_c = sound_speed(t_s, factor), critical_radius(world, t_s, factor)
    r = np.asarray(r, dtype=float)
    w_dw = 2 * w_c ** 2 * (r_c ** 5 / r ** 6 - r_c ** 4 / r ** 5) * np.exp(3 - 4 * r_c / r)
    return np.abs(w_dw) / (world.gm_m3_s2 / r ** 2)
