"""The warm rain's two factors at a world's gravity, by hand at the Moon's gravity, at CM1's own and at two others, and
the fits and fall-speed exponents they rest on, each on its line of the pinned CM1 source."""
import re
import tarfile
from pathlib import Path

import pytest

from shared.constants import MOON_SURFACE_GRAVITY
from atmosphere.rain import morrison, warm_rain

ARCHIVE = Path(__file__).resolve().parents[3] / 'upstream' / 'cm1r22.0.tar.gz'   # the pin in models/cm1/README.md


def test_the_factors_by_hand_at_the_moons_gravity_and_at_cm1s():
    moon = warm_rain.factors(MOON_SURFACE_GRAVITY)
    assert moon['rain_autoconv_fac'] == pytest.approx(1.6242188765608128 / 9.81, rel=1e-15)
    assert moon['rain_accr_fac'] == pytest.approx((1.6242188765608128 / 9.81)**0.6, rel=1e-15)
    assert (round(moon['rain_autoconv_fac'], 3), round(moon['rain_accr_fac'], 3)) == (0.166, 0.340)
    # At CM1's own gravity both are exactly 1, the patch's defaults.
    assert warm_rain.factors(9.81) == dict(rain_autoconv_fac=1.0, rain_accr_fac=1.0)
    # The accretion's factor is the one core patch 04 puts on rain's fall speeds.
    assert moon['rain_accr_fac'] == morrison.gravity_factor(MOON_SURFACE_GRAVITY)
    # Mars's 3.72 m/s2, and twice CM1's gravity, where cloud turns into rain faster than on Earth.
    assert list(warm_rain.factors(3.72).values()) == pytest.approx([0.379205, 0.558887], abs=5e-7)
    assert list(warm_rain.factors(19.62).values()) == pytest.approx([2.0, 2.0**0.6], rel=1e-15)
    for gravity in (0.0, -1.0):
        with pytest.raises(ValueError, match='positive'):
            warm_rain.factors(gravity)


def test_the_two_fits_and_the_exponents_are_the_pinned_sources():
    """Each constant of the warm rain on its line of the pinned cm1r22.0, as released: the two fits of Khairoutdinov and
    Kogan, above freezing and below, the 25 um drops of the new rain, the two fall-speed exponents, and IRAIN, which
    the scheme sets to 0 and reads from no namelist."""
    if not ARCHIVE.exists():
        pytest.skip('the pinned cm1r22.0 archive is missing (upstream/ is kept outside Git)')
    with tarfile.open(ARCHIVE) as tar:
        text = tar.extractfile('cm1r22.0/src/morrison.F').read().decode('latin-1')
        inputs = tar.extractfile('cm1r22.0/src/input.F').read().decode('latin-1')
    assert (morrison.AUTOCONVERSION, morrison.ACCRETION) == ((1350.0, 2.47, -1.79), (67.0, 1.15))
    assert (morrison.CLOUD_FALL_EXPONENT, morrison.FALL_EXPONENT, morrison.NEW_RAIN_RADIUS) == (2.0, 0.8, 25.0e-6)
    autoconversion = '                PRC(K)=1350.*QC3D(K)**2.47*  &\n           (NC3D(K)/1.e6*RHO(K))**(-1.79)\n'
    for line, count in ((autoconversion, 2),
                        ('           DUM=(QC3D(K)*QR3D(K))\n           PRA(K) = 67.*(DUM)**1.15\n', 2),
                        ('         CONS29=4./3.*PI*RHOW*(25.E-6)**3\n', 1), ('         BC = 2.\n', 1),
                        ('         BR = 0.8\n', 1), ('      IRAIN = 0\n', 1)):
        assert text.count(line) == count, line
    assert re.findall(r'^ +IRAIN *= *(\d)', text, flags=re.M) == ['0'] and 'irain' not in inputs.lower()
