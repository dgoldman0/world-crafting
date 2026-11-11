"""Rain in CM1's Morrison scheme, as the pinned cm1r22.0 source sets it: its fall law, the limits on its size, the
rate of its self-collection and the two fits by which cloud turns into rain, with the two factors the scheme and
Terluna's core patch 04 put on its fall speeds.

Morrison's raindrops fall at V = AR (RHOSU / rho)^0.54 D^BR, D in metres, with RHOSU the air at 850 hPa and 0 C; the
mean fall speeds of rain's exponential spectrum N0 exp(-lambda D) are capped at 9.1 m/s in that reference air. The
spectrum's mean diameter 1/lambda lies between 20 um and 2.8 mm, and rain's self-collection, 5.78 m3/kg/s (the source
credits Seifert and Beheng 2001), turns to breakup above a mean diameter D_b of 300 um by the factor
2 - exp(2300 m^-1 (1/lambda - D_b)) (credited to Verlinde and Cotton 1993). All are Earth's values, set at CM1's
gravity of 9.81 m/s2. Core patch 04 of models/cm1 multiplies AR and the cap by (g / 9.81)^((BR + 1) / 3) at a build's
gravity. Cloud water turns into rain by Khairoutdinov and Kogan's (2000) autoconversion and accretion, the formulas
the scheme's IRAIN = 0 selects, and cloud droplets fall by Stokes's law, V = AC D^2.

The values are those of Terluna's shared/constants.json at 39c5ee04 (model_closures, cm1_r22_morrison_rain and
cm1_r22_morrison_rain_limits), which the lab's pinned copy of that file predates; the warm rain's are the lab's
reading of the source. A test reads each from the pinned archive's morrison.F (atmosphere/tests/test_rain_breakup.py
and test_rain_warm.py).
"""
from __future__ import annotations

from shared.constants import CM1_DRY_AIR_GAS_CONSTANT

GRAVITY = 9.81                              # m/s2, CM1's own (constants.F)
FALL_COEFFICIENT = 841.99667                # AR, m^(1 - BR)/s
FALL_EXPONENT = 0.8                         # BR
DENSITY_REFERENCE_PRESSURE = 85000.0        # Pa: RHOSU = 85000 / (R TMELT)
DENSITY_REFERENCE_TEMPERATURE = 273.15      # K, TMELT
DENSITY_EXPONENT = 0.54
FALL_CAP = 9.1                              # m/s on rain's mean fall speeds, in the reference air
BREAKUP_CUTOFF = 300.0e-6                   # m, D_b where the namelist's brkup_db is 0
BREAKUP_RATE = 2300.0                       # 1/m
MEAN_DIAMETER_CAP = 2800.0e-6               # m, 1/LAMMINR
MEAN_DIAMETER_FLOOR = 20.0e-6               # m, 1/LAMMAXR
SELF_COLLECTION = 5.78                      # m3/kg/s
VENTILATION = (0.78, 0.308)                 # F1R and F2R: f = 0.78 + 0.308 Sc^(1/3) Re^(1/2)
CLOUD_FALL_EXPONENT = 2.0                   # BC: cloud droplets fall in the Stokes regime
AUTOCONVERSION = (1350.0, 2.47, -1.79)      # PRC = 1350 qc^2.47 N^-1.79 kg/kg/s, N the cloud droplets per cm3
ACCRETION = (67.0, 1.15)                    # PRA = 67 (qc qr)^1.15 kg/kg/s
NEW_RAIN_RADIUS = 25.0e-6                   # m: the drops autoconversion forms (CONS29)


def density_factor(density_kg_m3):
    """Morrison's (RHOSU / rho)^0.54 on the fall speeds, with RHOSU the air at 850 hPa and 0 C."""
    reference = DENSITY_REFERENCE_PRESSURE / (CM1_DRY_AIR_GAS_CONSTANT * DENSITY_REFERENCE_TEMPERATURE)
    return (reference / density_kg_m3)**DENSITY_EXPONENT


def gravity_factor(gravity_m_s2):
    """Core patch 04's factor on rain's fall law and cap at a build's gravity, (g / 9.81)^((BR + 1) / 3)."""
    return (gravity_m_s2 / GRAVITY)**((FALL_EXPONENT + 1) / 3)
