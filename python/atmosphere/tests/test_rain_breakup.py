"""Raindrop breakup at a world's gravity: Morrison's rain as the pinned CM1 source sets it, the limits by hand arithmetic
at the Moon's gravity and Earth's, the similarity the scale rests on (the capillary length at equal air density, the
air's density beyond it), and the numbers Terluna's breakup product gave for the Open Moon."""
import math
import tarfile
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from shared.constants import MOON_SURFACE_GRAVITY, STANDARD_GRAVITY
from atmosphere.radiative_convective.thermodynamics import earthlike_air
from atmosphere.rain import breakup, drops, morrison

ARCHIVE = Path(__file__).resolve().parents[3] / 'upstream' / 'cm1r22.0.tar.gz'   # the pin in models/cm1/README.md
DESIGN_PA = 1.2 * breakup.ATMOSPHERE_PA
# The Open Moon's air at 2 m as Terluna's rain products take it: the median over land of its resort climate at 301 K
# (atmosphere/rain/results/rain_drops.json at 39c5ee04, targets.resort).
RESORT_K, RESORT_HUMIDITY = 300.4274941880408, 0.6083150136678477


def column(gravity, atmospheres):
    """The design air's composition at a pressure, at the resort's temperature and humidity, under a gravity."""
    pressure = atmospheres * breakup.ATMOSPHERE_PA
    return drops.Column(gravity_m_s2=gravity, surface_pressure_pa=pressure, surface_temperature_k=RESORT_K,
                        surface_relative_humidity=RESORT_HUMIDITY, air=earthlike_air(pressure, 400.0))


@pytest.fixture(scope='module')
def moon():
    world = column(MOON_SURFACE_GRAVITY, 1.2)
    return dict(column=world, speeds=breakup.Speeds(world), earth=breakup.Speeds(breakup.earth_column(world)))


@pytest.fixture(scope='module')
def comparison(moon):
    return breakup.comparison(moon['speeds'], moon['earth'])


def test_morrisons_rain_is_the_pinned_sources():
    """Each constant of morrison.py on its line of the pinned cm1r22.0, as released."""
    if not ARCHIVE.exists():
        pytest.skip('the pinned cm1r22.0 archive is missing (upstream/ is kept outside Git)')
    with tarfile.open(ARCHIVE) as tar:
        text = tar.extractfile('cm1r22.0/src/morrison.F').read().decode('latin-1')
        constants = tar.extractfile('cm1r22.0/src/constants.F').read().decode('latin-1')
    assert (morrison.GRAVITY, morrison.FALL_COEFFICIENT, morrison.FALL_EXPONENT) == (9.81, 841.99667, 0.8)
    assert (morrison.DENSITY_REFERENCE_PRESSURE, morrison.DENSITY_REFERENCE_TEMPERATURE) == (85000.0, 273.15)
    assert (morrison.DENSITY_EXPONENT, morrison.FALL_CAP, morrison.SELF_COLLECTION) == (0.54, 9.1, 5.78)
    assert (morrison.BREAKUP_CUTOFF, morrison.BREAKUP_RATE) == (300.0e-6, 2300.0)
    assert (morrison.MEAN_DIAMETER_CAP, morrison.MEAN_DIAMETER_FLOOR) == (2800.0e-6, 20.0e-6)
    assert morrison.VENTILATION == (0.78, 0.308)
    for line, count in (('         AR = 841.99667\n', 1), ('         BR = 0.8\n', 1), ('         R = 287.04\n', 1),
                        ('         TMELT = 273.15\n', 1), ('         RHOSU = 85000./(R*TMELT)\n', 1),
                        ('            DUM = (RHOSU/RHO(K))**0.54\n', 1),
                        ('        UMR=MIN(UMR,9.1*dum)\n        UNR=MIN(UNR,9.1*dum)\n', 1),
                        ('         LAMMAXR = 1./20.E-6\n', 1), ('         LAMMINR = 1./2800.E-6\n', 1),
                        ('         cm1db = 300.e-6  ! default cutoff diameter for breakup\n', 1),
                        ('            dum=2.-exp(2300.*(1./lamr(k)-dum1))\n', 2),
                        ('            nragg(k) = -5.78*dum*qr3d(k)*nr3d(k)*rho(k)\n', 2),
                        ('         F1R = 0.78\n', 1), ('         F2R = 0.308\n', 1), ('         G = 9.81\n', 1)):
        assert text.count(line) == count, line
    assert 'g      = 9.81' in constants.split('!  cm1 defaults:')[1].split('ENDIF')[0]
    # The factors on the fall speeds, by hand: the air at 850 hPa and 0 C over air of 1.2 kg/m3, and the Moon's gravity.
    assert morrison.density_factor(1.2) == pytest.approx((85000.0 / (287.04 * 273.15) / 1.2)**0.54, rel=1e-15)
    assert morrison.density_factor(1.2) == pytest.approx(0.9466, abs=5e-5)          # (1.0841 / 1.2)^0.54
    assert morrison.gravity_factor(MOON_SURFACE_GRAVITY) == pytest.approx(0.33992673875932056, rel=1e-12)
    assert morrison.gravity_factor(9.81) == 1.0


def test_the_default_keeps_cm1s_limits_at_any_gravity():
    for gravity in (morrison.GRAVITY, MOON_SURFACE_GRAVITY, 3.7):
        for found in (breakup.limits(gravity, scaled=False), breakup.limits(gravity, 1.3, 0.7, scaled=False),
                      breakup.limits(gravity, 1.3, 0.7, scaled=False, cutoff_m=0.0)):
            assert found['breakup_cutoff_m'] == 300.0e-6 and found['breakup_rate_per_m'] == 2300.0
            assert found['mean_diameter_cap_m'] == 2800.0e-6
            assert found['fall_speed_cap_m_s'] == pytest.approx(9.1 * (gravity / 9.81)**0.6)     # core patch 04's cap
            assert found['equilibrium_m'] == pytest.approx(0.6013683393738892e-3, rel=1e-12)   # 0.3 mm + ln 2 / 2300 m
    assert breakup.limits(MOON_SURFACE_GRAVITY, scaled=False)['fall_speed_cap_m_s'] == pytest.approx(3.0933, abs=5e-5)
    assert breakup.limits(9.81, scaled=False, cutoff_m=500.0e-6)['breakup_cutoff_m'] == 500.0e-6   # the namelist's own


def test_the_limits_by_hand_at_the_moons_gravity_and_earths():
    """With s = (9.81/g)^(1/2): the breakup's lengths times s rho^alpha, the cap times s, the fall cap 9.1 (g/9.81)^(1/4)."""
    # The Moon, g = 1.6242188765608128 m/s2, at 1.2 times Earth's pressure with alpha = 0.687:
    # s = (9.81 / 1.6242188765608128)^(1/2) = 2.4576058205, 1.2^0.687 = 1.1334373402, their product 2.7855422045.
    moon = breakup.limits(1.6242188765608128, 1.2, 0.687)
    assert moon['breakup_cutoff_m'] == pytest.approx(0.3e-3 * 2.7855422045, rel=1e-9)             # 0.8357 mm
    assert moon['breakup_rate_per_m'] == pytest.approx(2300.0 / 2.7855422045, rel=1e-9)           # 825.7 /m
    assert moon['equilibrium_m'] == pytest.approx(0.83566266e-3 + 0.693147181 / 825.692031, rel=1e-8)   # 1.6751 mm
    assert moon['mean_diameter_cap_m'] == pytest.approx(2.8e-3 * 2.4576058205, rel=1e-9)          # 6.8813 mm
    assert moon['fall_speed_cap_m_s'] == pytest.approx(9.1 * 0.6378871985, rel=1e-9)              # 5.8048 m/s
    assert (round(moon['breakup_cutoff_m'] * 1e3, 2), round(moon['mean_diameter_cap_m'] * 1e3, 2),
            round(moon['fall_speed_cap_m_s'], 2), round(moon['equilibrium_m'] * 1e3, 2)) == (0.84, 6.88, 5.80, 1.68)
    # The capillary length alone, the exponent 0: 0.3 mm x 2.4576 = 0.737 mm, the lab's first scaling.
    assert breakup.limits(1.6242188765608128)['breakup_cutoff_m'] == pytest.approx(0.737282e-3, rel=1e-6)
    # Earth's gravity, CM1's 9.81 m/s2: in Earth's air CM1's own limits come back whatever the exponent;
    earth = breakup.limits(9.81, 1.0, 0.71)
    assert earth == breakup.limits(9.81, 1.0, 0.0)
    assert (earth['breakup_cutoff_m'], earth['breakup_rate_per_m'], earth['mean_diameter_cap_m'],
            earth['fall_speed_cap_m_s']) == (300.0e-6, 2300.0, 2800.0e-6, 9.1)
    # in air 1.2 times as dense, with alpha = 0.71, the breakup's lengths take 1.2^0.71 = 1.1382002710 alone.
    dense = breakup.limits(9.81, 1.2, 0.71)
    assert dense['breakup_cutoff_m'] == pytest.approx(0.3e-3 * 1.1382002710, rel=1e-9)            # 0.3415 mm
    assert dense['breakup_rate_per_m'] == pytest.approx(2300.0 / 1.1382002710, rel=1e-9)          # 2020.7 /m
    assert (dense['mean_diameter_cap_m'], dense['fall_speed_cap_m_s']) == (2800.0e-6, 9.1)
    # Between them, 3.7 m/s2: s = 1.6282970710, the cap 4.5592 mm and the fall cap 9.1 x 0.3771661^(1/4) = 7.1314 m/s.
    between = breakup.limits(3.7)
    assert between['mean_diameter_cap_m'] == pytest.approx(4.5592318e-3, rel=1e-7)
    assert between['fall_speed_cap_m_s'] == pytest.approx(7.1313963, rel=1e-7)
    with pytest.raises(ValueError):
        breakup.limits(1.6242188765608128, 0.0, 0.687)


def test_earth_against_itself_is_scale_one(moon):
    earth = moon['earth']
    large, small, weights = breakup.breakup_weights(earth, breakup.EQUILIBRIUM_M)
    keep = weights['straub'] > 1e-9 * weights['straub'].max()
    s, reached = breakup.pair_scale(earth, earth, large[keep], small[keep])
    assert reached.all() and np.allclose(s, 1.0, rtol=1e-9)
    home = breakup.density_exponent(breakup.earth_column(moon['column']))
    assert home['scale'] == pytest.approx(1.0, rel=1e-9) and home['alpha'] is None and home['unreached_share'] == 0.0


def test_both_coalescence_laws_coalesce_more_in_gentler_lunar_collisions(moon):
    """Over Low and List's own sizes, a pair meets more gently on the Moon than on Earth, and both laws let it
    coalesce at least as often there."""
    earth, lunar = moon['earth'], moon['speeds']
    large, small = np.meshgrid(np.linspace(1.2e-3, 4.6e-3, 8), np.linspace(0.4e-3, 1.0e-3, 4))
    large, small = large.ravel(), small.ravel()
    for world in (earth, lunar):
        assert np.all(breakup.collision(world, large, small)[3] > 0)
    assert np.all(breakup.collision(lunar, large, small)[3] < breakup.collision(earth, large, small)[3])
    assert np.all(breakup.straub(breakup.collision(lunar, large, small)[3])
                  > breakup.straub(breakup.collision(earth, large, small)[3]))
    assert np.all(breakup.low_list(lunar, large, small)[0] >= breakup.low_list(earth, large, small)[0] - 1e-12)


def test_the_open_moons_scale_is_terlunas(moon, comparison):
    """The numbers of Terluna's rain_breakup.json at 39c5ee04 (scale.resort.surface), which the same calculation gave
    for the same air."""
    assert comparison['density_ratio'] == pytest.approx(1.1961528842466684, rel=1e-12)
    assert comparison['capillary'] == pytest.approx(2.4574678746543683, rel=1e-12)
    assert comparison['stability_screen_mm']['world'] == pytest.approx(16.291601399784245, rel=1e-12)
    assert comparison['stability_screen_mm']['earth'] == pytest.approx(6.629425990797777, rel=1e-12)
    cutoff, balance = comparison['cutoff'], comparison['equilibrium']
    assert cutoff['scale'] == pytest.approx(2.567135399424826, rel=1e-9)
    assert balance['scale'] == pytest.approx(2.779363090474592, rel=1e-9)
    assert (balance['p10'], balance['p90']) == pytest.approx((2.5031337933145696, 3.3037413996567833), rel=1e-9)
    assert balance['unreached_share'] == pytest.approx(0.3032824703528363, rel=1e-9)
    assert balance['alpha'] == pytest.approx(0.6872311368220949, rel=1e-9) and round(balance['alpha'], 3) == 0.687
    assert balance['low_list_weights'] == pytest.approx(2.8628531732667715, rel=1e-9)
    # density_exponent gives the equilibrium's row of the comparison.
    found = breakup.density_exponent(moon['column'])
    for key in ('scale', 'unreached_share', 'alpha', 'over_capillary'):
        assert found[key] == balance[key], key
    assert (found['capillary'], found['density_ratio']) == (comparison['capillary'], comparison['density_ratio'])
    # Low and List's fit, read with its dimensional constants, breaks lunar drops at smaller sizes than the Weber law.
    for spectrum in (cutoff, balance):
        assert 1.5 < spectrum['low_list_literal']['scale'] < 2.0 < spectrum['scale']
        assert spectrum['low_list_literal']['breakup_share_covered'] > 0.6
    assert cutoff['scale'] < balance['scale']


def test_the_scale_follows_the_capillary_length_and_the_air(moon, comparison):
    lunar, earth = moon['speeds'], moon['earth']
    expected = math.sqrt(STANDARD_GRAVITY * (drops.WATER_DENSITY - earth.density)
                         / (MOON_SURFACE_GRAVITY * (drops.WATER_DENSITY - lunar.density)))
    assert comparison['capillary'] == pytest.approx(expected, rel=1e-3)
    assert lunar.screen / earth.screen == pytest.approx(comparison['capillary'], rel=2e-3)
    # At Earth's air density the equilibrium's scale is the capillary ratio, at the Moon's gravity and between.
    for gravity, over in ((MOON_SURFACE_GRAVITY, 1.0021008301981489), (3.7, 0.9989222700891599)):
        found = breakup.density_exponent(column(gravity, 1.0))
        assert found['alpha'] is None and found['over_capillary'] == pytest.approx(1.0, abs=0.01)
        assert found['over_capillary'] == pytest.approx(over, rel=1e-9)                     # Terluna's general rows
    # Denser air raises it as the density to a power near 0.7 at each gravity Terluna tried, the Moon's to Earth's.
    alphas = [comparison['equilibrium']['alpha'], breakup.density_exponent(column(3.7, 1.2))['alpha'],
              breakup.density_exponent(column(STANDARD_GRAVITY, 1.2))['alpha']]
    assert alphas == pytest.approx([0.6872311368220949, 0.6861367038425359, 0.7097963450670449], rel=1e-9)
    assert all(0.6 < a < 0.8 for a in alphas) and max(alphas) - min(alphas) < 0.05


def test_outside_the_gravities_terluna_computed_the_calculation_runs_on():
    """Under the gravities Terluna computed, where the lab's registry warns (cm1-rain-limits-range): at the 1.21 m/s2
    of the smallest waterworld the exponent is 0.692 at 1.2 times Earth's density, and at 1.3 m/s2 and Earth's density
    the scale is 0.4% above the capillary ratio. More of Earth's breakup lies beyond the hardest collisions the
    world's drops make under their stability screen: 33% at 1.21 m/s2, against 30% on the Open Moon. Above Earth's
    gravity, where the registry is silent, the scale at 15 m/s2 and Earth's density is 0.3% above the capillary ratio,
    and every Earth pair finds its match."""
    dense = breakup.density_exponent(column(1.21, 1.2))
    assert dense['alpha'] == pytest.approx(0.6916, abs=5e-4) and dense['unreached_share'] == pytest.approx(0.329, abs=2e-3)
    thin = breakup.density_exponent(column(1.3, 1.0))
    assert thin['alpha'] is None and thin['over_capillary'] == pytest.approx(1.0038, abs=5e-4)
    assert thin['capillary'] == pytest.approx(math.sqrt(STANDARD_GRAVITY / 1.3), rel=1e-3)
    heavy = breakup.density_exponent(column(15.0, 1.0))
    assert heavy['alpha'] is None and heavy['over_capillary'] == pytest.approx(1.0031, abs=5e-4)
    assert heavy['capillary'] == pytest.approx(math.sqrt(STANDARD_GRAVITY / 15.0), rel=1e-3) and heavy['unreached_share'] == 0.0


def test_the_open_moons_limits_are_terlunas(moon, comparison):
    """Terluna's lunar_limits: the patch's scale at the design pressure against the drop physics' own, the limits, and
    the checks on the fall-speed cap."""
    alpha = round(comparison['equilibrium']['alpha'], 3)
    found = breakup.limits(MOON_SURFACE_GRAVITY, DESIGN_PA / breakup.ATMOSPHERE_PA, alpha)
    assert found['breakup_cutoff_m'] * 1e3 == pytest.approx(0.8356626613588631, rel=1e-12)
    assert found['breakup_rate_per_m'] == pytest.approx(825.6920308943772, rel=1e-12)
    assert found['equilibrium_m'] * 1e3 == pytest.approx(1.6751368897938144, rel=1e-12)
    assert found['mean_diameter_cap_m'] * 1e3 == pytest.approx(6.881296297537753, rel=1e-12)
    assert found['fall_speed_cap_m_s'] == pytest.approx(5.804773506060524, rel=1e-12)
    collisional = math.sqrt(morrison.GRAVITY / MOON_SURFACE_GRAVITY) * 1.2**alpha
    assert collisional == pytest.approx(comparison['equilibrium']['scale'], rel=5e-3)     # 2.7855 against 2.7794
    # The largest drop's speed follows the quarter power of gravity in the same air within 2%.
    lunar = moon['speeds']
    same_air = breakup.Speeds(replace(moon['column'], gravity_m_s2=STANDARD_GRAVITY, lapse_k_m=None, cloud_base_m=None))
    quarter = (MOON_SURFACE_GRAVITY / morrison.GRAVITY)**0.25
    assert lunar.speed[-1] / same_air.speed[-1] == pytest.approx(0.628659739694896, rel=1e-9)
    assert lunar.speed[-1] / same_air.speed[-1] == pytest.approx(quarter, rel=0.02)
    # At the lunar equilibrium, in the air at 2 m, Morrison's mass-weighted speed and the solver's pass the cap core
    # patch 04 sets (2.70 m/s) and lie under the one the similarity gives (5.07 m/s).
    factor = morrison.density_factor(lunar.density)
    core_cap = morrison.FALL_CAP * morrison.gravity_factor(MOON_SURFACE_GRAVITY) * factor
    similar_cap = found['fall_speed_cap_m_s'] * factor
    law = (morrison.FALL_COEFFICIENT * morrison.gravity_factor(MOON_SURFACE_GRAVITY) * factor
           * math.gamma(4 + morrison.FALL_EXPONENT) / 6 * found['equilibrium_m']**morrison.FALL_EXPONENT)
    solver = breakup.mass_weighted_speed(lunar, found['equilibrium_m'])
    assert (core_cap, similar_cap) == pytest.approx((2.7007611844466037, 5.068094942946102), rel=1e-9)
    assert (law, solver) == pytest.approx((4.468759228262068, 4.208875129423873), rel=1e-9)
    assert core_cap < solver < similar_cap and core_cap < law < similar_cap
