"""The reproduction's contours over gravity and the distance from a star, from the steam columns' table (Arnscheidt,
Wordsworth and Ding 2019, section 3).

For a star of a given temperature and luminosity, a world at a distance d receives F = S (AU / d)^2, S being the
star's flux at 1 AU. Along the table's surface temperatures at each of its gravities, the instellation F(T_s) of
eq. 12 holds each surface temperature, linear in T_s between the table's points. Each contour is computed gravity by
gravity: the 273 K contour lies where F(273 K) is received, and a lifetime's contour where F(T_life) is, T_life being
the temperature at which the water lasts that long. The habitable zone lies between them, and the transition from
planet-like to comet-like worlds at the gravity where they meet, which depends on the escape alone. A temperature
outside the table's range, or a lifetime no temperature of the bracket gives, yields NaN.

The table's columns end below the critical radius of the isothermal wind (steam.py); the contours may take the wind
at other sound speeds, whose critical radii lie lower, so that at 1.1 to 1.2 m/s^2 above about 395 K the columns
stand taller than those winds' hydrostatic regions.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy.optimize import brentq

from atmosphere.waterworlds import balance as bl, escape as es
from atmosphere.waterworlds.body import Waterworld


@dataclass(frozen=True)
class Star:
    """A star as the reproduction takes it: a blackbody's temperature and its flux at 1 AU."""
    name: str
    temperature_k: float
    flux_1au_w_m2: float

    def distance_au(self, flux):
        return np.sqrt(self.flux_1au_w_m2 / np.asarray(flux, dtype=float))


def _star_index(table: dict, star: Star) -> int:
    stars = [float(s) for s in table['stars']]
    if float(star.temperature_k) not in stars:
        raise ValueError(f'the table holds the stars {stars} K, where {star.name} is {star.temperature_k} K')
    return stars.index(float(star.temperature_k))


def instellations(table: dict, star: Star, *, albedo: float = bl.ALBEDO, factor: float = 1.0) -> np.ndarray:
    """F(g, T_s), W/m^2, over the table's grid for one of its stars, at one albedo."""
    k = _star_index(table, star)
    olr, lw, sw = (np.asarray(table[name], dtype=float) for name in ('olr', 'lw_factor', 'sw_factor'))
    out = np.zeros_like(olr)
    for i, g in enumerate(table['gravities']):
        world = Waterworld.from_gravity(g)
        for j, t_s in enumerate(table['temperatures']):
            out[i, j] = bl.instellation(world, t_s, olr[i, j], lw[i, j], sw[k, i, j], albedo=albedo, factor=factor)
    return out


def contour_distance(table: dict, star: Star, temperatures_k, *, albedo: float = bl.ALBEDO,
                     factor: float = 1.0) -> np.ndarray:
    """For each gravity of the table, the distance (AU) at which the steady surface stands at the temperature given
    for that gravity, F interpolated linearly in T_s along the table; NaN where that temperature lies outside the
    table's range or is NaN."""
    f = instellations(table, star, albedo=albedo, factor=factor)
    t = np.asarray(table['temperatures'], dtype=float)
    out = np.full(len(table['gravities']), np.nan)
    for i, target in enumerate(np.asarray(temperatures_k, dtype=float)):
        if t[0] <= target <= t[-1]:
            out[i] = star.distance_au(np.interp(target, t, f[i]))
    return out


def lifetime_temperatures(gravities, lifetime_s: float, factor: float = 1.0, bracket=(150.0, 640.0)) -> np.ndarray:
    """For each gravity, the surface temperature at which the water lasts `lifetime_s`; NaN where no temperature in
    the bracket gives that lifetime."""
    out = []
    for g in gravities:
        world = Waterworld.from_gravity(g)

        def excess(t):
            return math.log(es.water_lifetime(world, t, factor) / lifetime_s)
        if excess(bracket[0]) * excess(bracket[1]) > 0:
            out.append(math.nan)
        else:
            out.append(brentq(excess, *bracket, xtol=1e-9))
    return np.array(out)
