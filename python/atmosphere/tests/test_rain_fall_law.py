"""The fall law of a world's rain: the quadrature gives a power law's closed forms back, by hand arithmetic at Earth's
gravity and the Moon's; the table is the solver's moments as the patched scheme reads them; rain's self-collection
follows the collision kernels; and the Open Moon's table and rate are those of Terluna's fall-law product."""
import math

import numpy as np
import pytest

from shared.constants import MOON_SURFACE_GRAVITY, STANDARD_GRAVITY
from atmosphere.radiative_convective.thermodynamics import DryAir, earthlike_air
from atmosphere.rain import breakup, drops, fall_law, morrison

# The Open Moon's air at 2 m as Terluna's rain products take it: the median over land of its resort climate at 301 K
# (atmosphere/rain/results/rain_drops.json at 39c5ee04, targets.resort).
RESORT_K, RESORT_HUMIDITY = 300.4274941880408, 0.6083150136678477


def column(gravity, atmospheres, air=None):
    pressure = atmospheres * breakup.ATMOSPHERE_PA
    return drops.Column(gravity_m_s2=gravity, surface_pressure_pa=pressure, surface_temperature_k=RESORT_K,
                        surface_relative_humidity=RESORT_HUMIDITY, air=air or earthlike_air(pressure, 400.0))


@pytest.fixture(scope='module')
def moon():
    world = column(MOON_SURFACE_GRAVITY, 1.2)
    return world, fall_law.settings(world)


@pytest.fixture(scope='module')
def earth():
    world = column(STANDARD_GRAVITY, 1.0, DryAir(breakup.ATMOSPHERE_PA))
    return world, fall_law.settings(world)


def fortran_rain(table, lam, m):
    """LAB_RAIN as patch 04 writes it: Fortran's INT truncates toward zero, its arrays count from 1."""
    rows = [table['ln_mass_weighted'], table['ln_number_weighted'], table['ln_ventilation']][m - 1]
    x = (math.log(lam) - table['ln_lambda_first']) / table['ln_lambda_step']
    i = min(max(int(x), 0), table['points'] - 2)
    w = min(max(x - i, 0.0), 1.0)
    return math.exp((1.0 - w) * rows[i] + w * rows[i + 1])


def test_the_quadrature_gives_a_power_laws_closed_forms_back():
    lam = fall_law.table_lambda()
    lunar = morrison.FALL_COEFFICIENT * morrison.gravity_factor(MOON_SURFACE_GRAVITY)
    for a, b in ((morrison.FALL_COEFFICIENT, morrison.FALL_EXPONENT), (lunar, morrison.FALL_EXPONENT), (150.0, 0.68),
                 (2000.0, 1.09)):
        found = fall_law.moments(fall_law.power_law(a, b), lam)
        assert np.allclose(found, fall_law.closed_forms(a, b, lam), rtol=1e-5, atol=0.0), (a, b)
    # Morrison's law by hand at a slope of 1000/m, a mean diameter of 1 mm, with Gamma(4.8) = 17.8378620,
    # Gamma(1.8) = 0.93138377, Gamma(2.9) = 1.82735508 and 1000^-0.8 = 0.0039810717:
    # at Earth's gravity A = 841.99667: 841.99667 x 17.8378620 / 6 x 0.0039810717 = 9.9656 m/s by mass,
    # 841.99667 x 0.93138377 x 0.0039810717 = 3.1220 m/s by number, 841.99667^(1/2) x 1.82735508 x 1000^-2.9 by the
    # ventilation; at the Moon's gravity A = 841.99667 x 0.33992674 = 286.21718, and 3.3876 and 1.0613 m/s.
    point = np.array([1000.0])
    at_earth = fall_law.moments(fall_law.power_law(841.99667, 0.8), point)[:, 0]
    assert at_earth == pytest.approx([9.965564924, 3.122044149, 1.0579816422e-07], rel=3e-6)
    at_moon = fall_law.moments(fall_law.power_law(286.21718208, 0.8), point)[:, 0]
    assert at_moon == pytest.approx([3.387561984, 1.061266286, 6.168375391e-08], rel=3e-6)
    assert lunar == pytest.approx(286.21718208, rel=1e-9)


def test_the_table_is_the_solvers_moments_in_the_reference_air(moon):
    world, found = moon
    table, air = found['table'], found['air']
    lam = fall_law.table_lambda()
    assert table['points'] == lam.size == 301
    assert table['ln_lambda_first'] == pytest.approx(math.log(100.0), abs=1e-12)
    assert table['ln_lambda_step'] == pytest.approx(math.log(1000.0) / 300, rel=1e-12)
    d, v, screen = fall_law.solved_speeds(world)
    reference = fall_law.speed_law(d, v / air['density_factor'])
    nodes = fall_law.moments(reference, lam)
    assert np.allclose(fall_law.interpolate(table, lam), nodes, rtol=1e-9, atol=0.0)
    middle = np.sqrt(lam[1:] * lam[:-1])
    assert np.allclose(fall_law.interpolate(table, middle), fall_law.moments(reference, middle), rtol=1e-4, atol=0.0)
    # Constant beyond the table's ends.
    ends = fall_law.interpolate(table, np.array([10.0, 1e7]))
    assert np.allclose(ends[:, 0], nodes[:, 0]) and np.allclose(ends[:, 1], nodes[:, -1])
    assert air['density_factor'] == pytest.approx(morrison.density_factor(air['density_kg_m3']), rel=1e-15)
    assert (air['stability_screen_m'], air['screen_speed_m_s']) == (screen, v[-1])


def test_the_moments_behave_as_a_fall_law_must(moon, earth):
    for world, found in (moon, earth):
        table, air = found['table'], found['air']
        mass, number = np.exp(table['ln_mass_weighted']), np.exp(table['ln_number_weighted'])
        assert np.all(np.diff(mass) < 0) and np.all(np.diff(number) < 0)        # wider spectra fall faster
        assert np.all(number < mass)                                              # small drops are many and slow
        assert mass.max() * air['density_factor'] < air['screen_speed_m_s']      # never faster than the largest drop
        # Stokes's law by hand at the smallest mean diameter, 10 um: a drop falls at (rho_w - rho_a) g D^2 / (18 mu),
        # and D^2 averages 2 / lambda^2 over the spectrum's drops. The spectrum's largest drops fall short of the law,
        # by 0.9% of the mean on the Moon and 2.4% on Earth.
        state = world.state(0.0)
        stokes = ((drops.WATER_DENSITY - state['density_kg_m3']) * world.gravity_m_s2 / (18.0 * state['viscosity_pa_s'])
                  * 2.0 / 1.0e5**2 / air['density_factor'])
        assert 0.97 < number[-1] / stokes <= 1.0
    assert np.exp(moon[1]['table']['ln_number_weighted'][-1]) / (
        (drops.WATER_DENSITY - 1.3938769667041175) * MOON_SURFACE_GRAVITY / (18.0 * 1.807851743125031e-05)
        * 2.0e-10 / 0.8730909031428553) == pytest.approx(0.9914537709930595, rel=1e-9)        # Terluna's check


def test_the_open_moons_table_and_rate_are_terlunas(moon):
    """The numbers of Terluna's rain_fall_law.json at 39c5ee04, which the same calculation gave for the same air."""
    world, found = moon
    air, table, rate = found['air'], found['table'], found['self_collection']
    assert air['density_kg_m3'] == pytest.approx(1.3938769667041175, rel=1e-12)
    assert air['density_factor'] == pytest.approx(0.8730909031428553, rel=1e-12)
    assert air['stability_screen_m'] * 1e3 == pytest.approx(16.291601399784245, rel=1e-12)
    assert air['screen_speed_m_s'] == pytest.approx(5.329992138213767, rel=1e-9)
    for key, first, middle, last in (
            ('ln_mass_weighted', 1.8066862859137531, 0.4607166728421694, -4.504261376594509),
            ('ln_number_weighted', 1.5043742356834322, -1.0054043022345411, -6.78557335704011),
            ('ln_ventilation', -10.33954357639864, -19.91833043396332, -31.322067423410257)):
        assert (table[key][0], table[key][150], table[key][300]) == pytest.approx((first, middle, last), abs=1e-10), key
    assert found['limits']['equilibrium_m'] * 1e3 == pytest.approx(1.6751368897938144, rel=1e-12)
    assert rate['kernel_ratio'] == pytest.approx(1.9801118353303497, rel=1e-9) and round(rate['kernel_ratio'], 2) == 1.98
    assert rate['largest_m'] * 1e3 == pytest.approx(6.629425990797777, rel=1e-12)         # Earth's stability screen
    assert rate['rate_m3_kg_s'] == 2.919 == round(5.78 / 1.9801118353303497, 4)
    assert found['namelist'] == dict(brkup_db=300.0e-6, brkup_gscale=1, brkup_rhor=1.2, brkup_rhoexp=0.687,
                                     rain_fall_law=1, rain_selfcoll=2.919)
    # Earth's kernel exceeds the Moon's by a factor that falls as the drops grow.
    home = breakup.earth_column(world)
    ratios = [fall_law.self_collection(world, home, mm * 1e-3)['kernel_ratio'] for mm in (0.6, 1.0, 2.5)]
    assert ratios == pytest.approx([2.6500857741804946, 2.289470594605618, 1.8097211761847414], rel=1e-9)
    # At the lunar equilibrium the solver brings rain's water down at 4.22 m/s at 2 m and its drops at 1.58 m/s.
    at = fall_law.interpolate(table, np.array([1.0 / found['limits']['equilibrium_m']]))[:, 0] * air['density_factor']
    assert at[:2] == pytest.approx([4.223020834697148, 1.5800796943615028], rel=1e-4)
    # Morrison's law at the Moon's gravity over the solver's moments for mean diameters of 0.2 to 3 mm, by mass, by
    # number and in the ventilation: the spans of Terluna's product (power_laws.present).
    lam = 1.0 / np.geomspace(0.2e-3, 3.0e-3, 29)
    law = fall_law.closed_forms(morrison.FALL_COEFFICIENT * morrison.gravity_factor(MOON_SURFACE_GRAVITY),
                                morrison.FALL_EXPONENT, lam)
    d, v, _ = fall_law.solved_speeds(world)
    solver = fall_law.moments(fall_law.speed_law(d, v / air['density_factor']), lam)
    spans = [x for r in law / solver for x in (r.min(), r.max())]
    assert spans == pytest.approx([0.835188718514658, 1.4395348619916735, 0.8830935757591335, 1.4107351532537356,
                                   0.9239881682330117, 1.0505972470376328], rel=1e-9)


def test_self_collection_follows_the_kernels(moon, earth):
    world, home = moon[0], breakup.earth_column(moon[0])
    assert fall_law.self_collection(home, home, 1.0e-3)['kernel_ratio'] == pytest.approx(1.0, rel=1e-12)
    assert fall_law.self_collection(home, home, 1.0e-3)['rate_m3_kg_s'] == 5.78
    # A heavier world's drops meet faster than Earth's, up to the smaller of the two stability screens, its own.
    heavy = column(15.0, 1.0)
    found = fall_law.self_collection(heavy, breakup.earth_column(heavy), 0.5e-3)
    assert found['kernel_ratio'] < 1.0 and found['rate_m3_kg_s'] > 5.78
    assert found['largest_m'] == drops.stable_diameter(heavy) < drops.stable_diameter(home)
    assert fall_law.self_collection(world, home, 1.0e-3)['largest_m'] == drops.stable_diameter(home)


def test_earths_own_air_gives_cm1s_limits_and_rate(earth):
    """Under standard gravity in Earth's own air the limits and the rate are CM1's, to the 0.02% by which its 9.81 m/s2
    exceeds 9.80665; the table is the solver's, which Morrison's Earth fit follows only in part."""
    world, found = earth
    assert found['namelist'] == dict(brkup_db=300.0e-6, brkup_gscale=1, brkup_rhor=1.0, brkup_rhoexp=0.0,
                                     rain_fall_law=1, rain_selfcoll=5.78)
    assert found['breakup']['alpha'] is None and found['self_collection']['kernel_ratio'] == pytest.approx(1.0)
    own = breakup.limits(STANDARD_GRAVITY, scaled=False)
    for key in ('breakup_cutoff_m', 'breakup_rate_per_m', 'equilibrium_m', 'mean_diameter_cap_m', 'fall_speed_cap_m_s'):
        assert found['limits'][key] == pytest.approx(own[key], rel=3e-4), key
    # At CM1's own 9.81 m/s2 the limits are CM1's to the last digit, and the rate comes to 5.7808 m3/kg/s, 0.01% above
    # CM1's 5.78, since the Earth it is measured against stands at the standard 9.80665 m/s2.
    at_cm1 = fall_law.settings(column(morrison.GRAVITY, 1.0, DryAir(breakup.ATMOSPHERE_PA)))
    assert at_cm1['limits'] == breakup.limits(morrison.GRAVITY, scaled=False)
    assert at_cm1['namelist']['rain_selfcoll'] == 5.7808 and at_cm1['namelist']['brkup_rhoexp'] == 0.0
    assert at_cm1['self_collection']['kernel_ratio'] == pytest.approx(0.99986, abs=2e-5)
    # Morrison's law over the solver's moments for mean diameters of 0.2 to 3 mm: by mass 0.87 to 2.51, and 0.87 to
    # 1.12 under the scheme's 9.1 m/s cap; by number 0.93 to 1.23; in the ventilation 0.95 to 1.31.
    lam = 1.0 / np.geomspace(0.2e-3, 3.0e-3, 29)
    law = fall_law.closed_forms(morrison.FALL_COEFFICIENT, morrison.FALL_EXPONENT, lam)
    solver = fall_law.interpolate(found['table'], lam)
    spans = [x for r in (law[0] / solver[0], np.minimum(law[0], morrison.FALL_CAP) / solver[0], law[1] / solver[1],
                         law[2] / solver[2]) for x in (r.min(), r.max())]
    assert spans == pytest.approx([0.8721, 2.5125, 0.8721, 1.1222, 0.9273, 1.2330, 0.9453, 1.3069], abs=2e-4)
    # At Earth's breakup equilibrium of 0.60 mm the law's three moments are 0.98, 0.93 and 0.95 of the solver's.
    at = 1.0 / np.array([breakup.EQUILIBRIUM_M])
    ratio = (fall_law.closed_forms(morrison.FALL_COEFFICIENT, morrison.FALL_EXPONENT, at)
             / fall_law.interpolate(found['table'], at))[:, 0]
    assert ratio == pytest.approx([0.9839, 0.9322, 0.9530], abs=2e-4)


def test_the_pressure_ratio_stands_in_for_the_density_ratio_of_the_exponents_fit(moon):
    """settings gives CM1 the surface pressure over 1013.25 hPa as brkup_rhor, with an exponent fitted on the ratio of
    the two airs' densities. The two ratios agree for dry air of Earth's molar mass, CM1's air having Earth's gas
    constant. The breakup scale patch 03 then sets, (9.81 / g)^(1/2) brkup_rhor^brkup_rhoexp, over the collisions' own:
    0.2% above it in the Open Moon's air, of 17.5% oxygen; 0.9% above and 1.3% below it with 10% and 35% oxygen at the
    Moon's gravity and 1.2 atm; 1.2% above and 1.5% below it with those shares at CM1's gravity and 1 atm."""
    def departure(found):
        return found['limits']['breakup_cutoff_m'] / morrison.BREAKUP_CUTOFF / found['breakup']['scale'] - 1.0

    lunar = moon[1]
    assert departure(lunar) == pytest.approx(0.0022, abs=1e-4)
    assert lunar['namelist']['brkup_rhor'] == 1.2
    assert lunar['breakup']['density_ratio'] == pytest.approx(1.1962, abs=1e-4)      # under the pressures' 1.2
    for gravity, atmospheres, oxygen, expected in ((MOON_SURFACE_GRAVITY, 1.2, 0.10, 0.0091),
                                                   (MOON_SURFACE_GRAVITY, 1.2, 0.35, -0.0133),
                                                   (morrison.GRAVITY, 1.0, 0.10, 0.0119),
                                                   (morrison.GRAVITY, 1.0, 0.35, -0.0145)):
        pressure = atmospheres * breakup.ATMOSPHERE_PA
        found = fall_law.settings(column(gravity, atmospheres, earthlike_air(pressure, 400.0, oxygen * pressure)))
        assert found['namelist']['brkup_rhor'] == atmospheres and found['air']['pressure_pa'] == pytest.approx(pressure)
        assert departure(found) == pytest.approx(expected, abs=1e-4), (gravity, oxygen)


def test_the_table_text_is_what_cm1_reads(moon):
    table = moon[1]['table']
    lines = fall_law.table_text(table).splitlines()
    head = lines[0].split()
    assert int(head[0]) == table['points'] == len(lines) - 1
    assert float(head[1]) == pytest.approx(table['ln_lambda_first'], rel=1e-9)
    assert float(head[2]) == pytest.approx(table['ln_lambda_step'], rel=1e-9)
    rows = np.array([[float(x) for x in line.split()] for line in lines[1:]])
    for k, key in enumerate(('ln_mass_weighted', 'ln_number_weighted', 'ln_ventilation')):
        assert np.allclose(rows[:, k], table[key], rtol=1e-9, atol=1e-12), key
    # The Fortran's reading, step for step, against interpolate, inside the table and beyond its ends.
    for lam in (1.0, 99.0, 100.0, 145.3, 597.0, 1000.0, 2.0e4, 5.0e4, 1.0e5, 3.0e5):
        mirror = fall_law.interpolate(table, np.array([lam]))[:, 0]
        for m in (1, 2, 3):
            assert fortran_rain(table, lam, m) == pytest.approx(mirror[m - 1], rel=1e-12), (lam, m)
    assert fall_law.TABLE_FILE == 'lab_rain_law.txt'


def test_the_solver_bounds_the_worlds_it_serves():
    """Below about 0.48 m/s2 the largest stable drop exceeds the solver's 30 mm, and a ground above 313.15 K lies
    outside its water's range."""
    with pytest.raises(ValueError, match='diameter'):
        fall_law.table(column(0.4, 1.0))
    with pytest.raises(ValueError, match='warm-water'):
        drops.Column(gravity_m_s2=9.81, surface_pressure_pa=101325.0, surface_temperature_k=320.0,
                     surface_relative_humidity=0.5, air=DryAir(101325.0))
    assert len(fall_law.table(column(0.6, 1.0))['ln_mass_weighted']) == 301
