"""Waterworlds sized by the relation of Sotin et al. (2007), as Arnscheidt, Wordsworth and Ding (2019) use it.

A waterworld's radius follows from its mass, R/R_E = 1.258 (M/M_E)^0.302, which Sotin, Grasset and Mocquet (2007,
Icarus 191, 337) fitted to interior models of waterworlds of 0.01 to 1 Earth mass and Arnscheidt, Wordsworth and
Ding (2019, ApJ 881, 60, eq. 1) took for their low-gravity worlds, 40% of whose mass is water (their section 2.1).
Surface gravity g = GM/R^2 then grows as M^0.396, so a world is fixed by its gravity alone. Earth's mass is its GM
over G and its radius the mean radius, both from shared/constants.json; the papers leave theirs unstated.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from shared.constants import EARTH_GM, EARTH_RADIUS, GRAVITATIONAL_CONSTANT
from atmosphere.radiative_convective.thermodynamics import Planet

SOTIN_COEFFICIENT = 1.258
SOTIN_EXPONENT = 0.302
WATER_MASS_FRACTION = 0.4
EARTH_MASS_KG = EARTH_GM / GRAVITATIONAL_CONSTANT
# The gravity of a world of one Earth mass on the relation: g = REFERENCE_GRAVITY (M/M_E)^(1 - 2 x 0.302).
REFERENCE_GRAVITY = EARTH_GM / (SOTIN_COEFFICIENT * EARTH_RADIUS) ** 2
GRAVITY_EXPONENT = 1 - 2 * SOTIN_EXPONENT


@dataclass(frozen=True)
class Waterworld:
    """A body of the relation, by its mass in Earth masses, with its water's share of that mass."""
    earth_masses: float
    water_mass_fraction: float = WATER_MASS_FRACTION

    def __post_init__(self):
        if not self.earth_masses > 0:
            raise ValueError(f'a waterworld needs a positive mass, where it has {self.earth_masses!r} Earth masses')
        if not 0 < self.water_mass_fraction <= 1:
            raise ValueError(f'the water is a share of the mass in (0, 1], where it is {self.water_mass_fraction!r}')

    @classmethod
    def from_gravity(cls, gravity_m_s2: float, water_mass_fraction: float = WATER_MASS_FRACTION) -> 'Waterworld':
        """The world of the relation whose surface gravity is `gravity_m_s2`."""
        if not gravity_m_s2 > 0:
            raise ValueError(f'a waterworld needs a positive surface gravity, where it has {gravity_m_s2!r}')
        return cls((gravity_m_s2 / REFERENCE_GRAVITY) ** (1 / GRAVITY_EXPONENT), water_mass_fraction)

    @property
    def mass_kg(self) -> float:
        return self.earth_masses * EARTH_MASS_KG

    @property
    def radius_m(self) -> float:
        return SOTIN_COEFFICIENT * self.earth_masses ** SOTIN_EXPONENT * EARTH_RADIUS

    @property
    def gm_m3_s2(self) -> float:
        return self.earth_masses * EARTH_GM

    @property
    def gravity_m_s2(self) -> float:
        return self.gm_m3_s2 / self.radius_m ** 2

    @property
    def escape_speed_m_s(self) -> float:
        return math.sqrt(2 * self.gm_m3_s2 / self.radius_m)

    @property
    def water_mass_kg(self) -> float:
        return self.water_mass_fraction * self.mass_kg

    @property
    def planet(self) -> Planet:
        """The body as the radiative-convective column's planet, whose gravity falls as GM/r^2."""
        return Planet(f'waterworld-{self.earth_masses:.6g}', self.radius_m, self.gm_m3_s2)
