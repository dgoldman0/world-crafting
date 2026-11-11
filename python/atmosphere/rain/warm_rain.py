"""Factors on the warm rain of CM1's Morrison scheme at a world's gravity: the entries rain_autoconv_fac and
rain_accr_fac of &param3 that patch 05 of the lab's CM1 series reads.

    from atmosphere.rain import warm_rain
    warm_rain.factors(1.6242)                         # {'rain_autoconv_fac': 0.1656, 'rain_accr_fac': 0.3399}

Morrison's scheme turns cloud water into rain by two fits of Khairoutdinov and Kogan (2000): the autoconversion
1350 qc^2.47 N^-1.79 kg/kg/s, with N the cloud droplets per cm3, and the accretion 67 (qc qr)^1.15 kg/kg/s. Gravity
appears in neither, while in the collisions they describe it sets the closing speed. A particle of the regime
V = A D^B falls as g^((B + 1) / 3) at a fixed size, the scaling by which core patch 04 of models/cm1 slows the
scheme's fall speeds. Cloud droplets fall in the Stokes regime, B = 2, so the speed at which one droplet overtakes
another goes as g, and the autoconversion's factor is g / 9.81. Rain sweeps up cloud at its own fall speed, B = 0.8,
so the accretion's factor is (g / 9.81)^0.6. Both are 1 at CM1's 9.81 m/s2, and 0.166 and 0.340 at the Moon's
1.6242 m/s2.

Evidence. A scaling law, computed from the scheme's two fall-speed exponents. No run has taken the factors, so their
effect on a cloud and its rain is unmeasured until a sea box runs with them (PLAN.md, block 4, step 2).

Limits. The scaling omits the collision efficiency's own dependence on the closing speed, and collisions driven by
turbulence, which are independent of gravity. The two fits were made on drop spectra of Earth's clouds, and a factor
multiplies each fit whole, with its exponents on the cloud's water and droplet number as they are.
"""
from __future__ import annotations

from atmosphere.rain import morrison


def factors(gravity_m_s2):
    """The two entries for a world's gravity: rain_autoconv_fac = g / 9.81, by the droplets' Stokes exponent, and
    rain_accr_fac = (g / 9.81)^0.6, by rain's, each 1 at CM1's own 9.81 m/s2."""
    if not gravity_m_s2 > 0:
        raise ValueError('The gravity must be positive')
    ratio = gravity_m_s2 / morrison.GRAVITY
    return dict(rain_autoconv_fac=ratio**((morrison.CLOUD_FALL_EXPONENT + 1) / 3),
                rain_accr_fac=ratio**((morrison.FALL_EXPONENT + 1) / 3))
