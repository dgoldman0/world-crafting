"""Waterworlds after Arnscheidt, Wordsworth and Ding (2019): the size relation and the isothermal wind."""
import math

import numpy as np
import pytest

from atmosphere.waterworlds import escape as es
from atmosphere.waterworlds.body import EARTH_MASS_KG, Waterworld

BILLION_YEARS = 1e9 * es.YEAR_S


def test_the_size_relation_gives_the_papers_masses():
    # The paper's transition, g = 1.48 m/s^2 at 0.0268 Earth masses, and its g = 2.3 m/s^2 at about 0.08 (eq. 1).
    transition, figure_3 = Waterworld.from_gravity(1.48), Waterworld.from_gravity(2.3)
    assert transition.earth_masses == pytest.approx(0.0268, rel=1e-3)
    assert figure_3.earth_masses == pytest.approx(0.08, rel=0.03)
    for world in (transition, figure_3, Waterworld(0.05)):
        assert world.gravity_m_s2 == pytest.approx(world.gm_m3_s2 / world.radius_m ** 2, rel=1e-14)
        assert world.radius_m / 6.371e6 == pytest.approx(1.258 * world.earth_masses ** 0.302, rel=1e-14)
        assert world.mass_kg == pytest.approx(world.earth_masses * EARTH_MASS_KG, rel=1e-14)
        assert Waterworld.from_gravity(world.gravity_m_s2).earth_masses == pytest.approx(world.earth_masses, rel=1e-12)
        assert world.water_mass_kg == pytest.approx(0.4 * world.mass_kg, rel=1e-14)
    assert transition.planet.surface_gravity == pytest.approx(1.48, rel=1e-12)


@pytest.mark.parametrize('mass, water', [(0.0, 0.4), (-0.1, 0.4), (0.05, 0.0), (0.05, 1.2)])
def test_a_waterworld_refuses_a_mass_or_a_water_share_it_cannot_have(mass, water):
    with pytest.raises(ValueError):
        Waterworld(mass, water)
    with pytest.raises(ValueError):
        Waterworld.from_gravity(-1.0)


@pytest.mark.parametrize('g, t_s', [(1.48, 273.0), (2.3, 450.0), (2.0, 350.0)])
def test_the_full_wind_solves_the_wind_equation_and_passes_its_sound_speed_at_the_critical_radius(g, t_s):
    world = Waterworld.from_gravity(g)
    w_c, r_c = es.sound_speed(t_s), es.critical_radius(world, t_s)
    assert r_c == pytest.approx(world.gm_m3_s2 / (2 * w_c ** 2), rel=1e-14)
    assert float(es.transonic_speed(world, t_s, r_c)) == pytest.approx(w_c, rel=1e-7)
    # (w^2 - w_c^2) (1/w) dw/dr = 2 w_c^2 / r - GM / r^2 (eq. 7), by central differences on the subsonic branch.
    r = np.linspace(0.3, 0.8, 11) * r_c
    h = 1e-5 * r
    w = es.transonic_speed(world, t_s, r)
    dw = (es.transonic_speed(world, t_s, r + h) - es.transonic_speed(world, t_s, r - h)) / (2 * h)
    left = (w ** 2 - w_c ** 2) * dw / w
    right = 2 * w_c ** 2 / r - world.gm_m3_s2 / r ** 2
    assert np.allclose(left, right, rtol=1e-6)


@pytest.mark.parametrize('g, t_s', [(1.48, 273.0), (2.3, 450.0)])
def test_eq_9_and_eq_a4_are_the_full_wind_with_its_kinetic_term_dropped(g, t_s):
    world = Waterworld.from_gravity(g)
    w_c, r_c, r_s = es.sound_speed(t_s), es.critical_radius(world, t_s), world.radius_m
    # At the surface the kinetic term is below one part in 10^12, so eq. 9 is the full wind's flux.
    full = float(es.transonic_speed(world, t_s, r_s))
    assert es.mass_flux(world, t_s) / es.surface_density(t_s) == pytest.approx(full, rel=1e-12)
    # Dropping (w/w_c)^2 / 2 from eq. A3 multiplies the speed by exp(-(w/w_c)^2 / 2) at every radius.
    r = np.linspace(r_s, 0.95 * r_c, 50)
    exact = es.transonic_speed(world, t_s, r)
    assert np.allclose(es.outflow_speed(world, t_s, r), exact * np.exp(-0.5 * (exact / w_c) ** 2), rtol=1e-10)


def test_eq_a5_is_the_inertia_of_the_wind_of_eq_a4():
    world, t_s = Waterworld.from_gravity(1.8), 320.0
    r = np.linspace(1.0, 4.0, 13) * world.radius_m
    h = 1e-6 * r
    w = es.outflow_speed(world, t_s, r)
    dw = (es.outflow_speed(world, t_s, r + h) - es.outflow_speed(world, t_s, r - h)) / (2 * h)
    assert np.allclose(es.inertia_ratio(world, t_s, r), np.abs(w * dw) / (world.gm_m3_s2 / r ** 2), rtol=1e-6)


def test_the_water_lasts_longer_on_heavier_and_colder_worlds():
    heavy, light = Waterworld.from_gravity(2.3), Waterworld.from_gravity(1.5)
    for t_s in (250.0, 300.0, 400.0):
        assert es.water_lifetime(heavy, t_s) > es.water_lifetime(light, t_s)
    assert es.water_lifetime(heavy, 300.0) > es.water_lifetime(heavy, 350.0) > es.water_lifetime(heavy, 450.0)
    assert es.water_lifetime(heavy, 300.0, factor=1.3) < es.water_lifetime(heavy, 300.0)


def test_by_the_printed_wind_the_billion_year_lifetime_meets_273_k_below_the_papers_transition():
    """By the paper's eqs. 9-11 as printed, its transition world, g = 1.48 m/s^2 at 273 K, keeps its water about
    6 x 10^11 years, and the 10^9-year lifetime meets 273 K at g = 1.29 m/s^2, 0.019 Earth masses, where the paper
    finds 1.48 m/s^2 and 0.0268 (section 3.3). With the square of the sound speed taken as 1.272 kT/m the transition
    falls at the paper's (notes/waterworlds.md). A record of the printed equations against the paper's stated
    values, from a calculation; reading the authors' code would confirm or correct it."""
    transition = Waterworld.from_gravity(1.48)
    assert es.water_lifetime(transition, 273.0) / es.YEAR_S == pytest.approx(5.96e11, rel=2e-3)
    printed = es.lifetime_gravity(273.0, BILLION_YEARS)
    assert printed == pytest.approx(1.2916, abs=2e-4)
    assert Waterworld.from_gravity(printed).earth_masses == pytest.approx(0.0190, abs=2e-4)
    assert es.lifetime_gravity(273.0, BILLION_YEARS, factor=1.2722) == pytest.approx(1.48, abs=2e-4)
    assert es.water_lifetime(transition, 273.0, factor=1.2722) == pytest.approx(BILLION_YEARS, rel=0.01)


def test_a_lifetime_beyond_the_floating_point_range_is_infinite_and_impossible_inputs_are_refused():
    assert es.water_lifetime(Waterworld(1.0), 100.0) == math.inf
    with pytest.raises(ValueError):
        es.sound_speed(300.0, factor=0.0)
    with pytest.raises(ValueError):
        world = Waterworld.from_gravity(2.0)
        es.transonic_speed(world, 300.0, 2 * es.critical_radius(world, 300.0))
    with pytest.raises(ValueError):
        es.mass_flux(Waterworld(1e-6), 600.0)            # the critical radius below the surface
    with pytest.raises(ValueError):
        es.lifetime_gravity(150.0, BILLION_YEARS)        # every world of the relation's range keeps it longer


def test_the_full_wind_holds_its_precision_across_its_three_methods():
    """Lambert's W, the series at its branch point near r_c and the exponential far below r_c each meet eq. A3's
    solution in 50-digit arithmetic to 1e-9, on both sides of each switch."""
    mp = pytest.importorskip('mpmath')
    mp.mp.dps = 50
    world, t_s = Waterworld.from_gravity(2.0), 300.0
    w_c, r_c = es.sound_speed(t_s), es.critical_radius(world, t_s)
    # From the surface (0.041 r_c) through the deep shortcut's edge (2 rhs = -30 at 0.0942 r_c) and the series' edge
    # (p = 1e-3 at 0.9995 r_c) to r_c.
    shares = np.concatenate([[world.radius_m / r_c], np.linspace(0.085, 0.105, 9), np.linspace(0.2, 0.9, 4),
                             1 - np.logspace(-2, -9, 15), [1.0]])
    assert shares[0] == pytest.approx(0.041, abs=1e-3)
    for share in shares:
        r = share * r_c
        x = mp.mpf(r) / mp.mpf(r_c)
        rhs = -2 / x - 2 * mp.log(x) + mp.mpf(3) / 2
        u = -mp.lambertw(-mp.exp(2 * rhs), 0).real
        got = float(es.transonic_speed(world, t_s, r))
        assert got == pytest.approx(w_c * float(mp.sqrt(u)), rel=1e-9), share
