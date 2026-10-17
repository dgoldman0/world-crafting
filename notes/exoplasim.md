# ExoPlaSim on a breathable Moon: correctness, limits and room for improvement

Notes on the ten patches in [../models/exoplasim/](../models/exoplasim/), the settings that carry the
Moon, the offline copies of PlaSim's radiation in `python/climate/gcm/`, and what in PlaSim stays
Earth's. References to Terluna are at commit 186b294; to ExoPlaSim, at the 3.4.2 source distribution.

Evidence states used below: **reproduction** (the same code or arithmetic gives the same numbers),
**identity** (a switch at its default gives the unpatched model's output byte for byte), **calibration**
(agreement with the in-house line-by-line model on the GCM's own columns, by construction near the
fitted columns), **sensitivity** (what the change does to the simulated climate). None of these is a
physical validation of a lunar climate, which no observation can supply.

## How the series was checked as a whole

- Applied with GNU patch to pristine ExoPlaSim 3.4.2, the series reproduces the copy every Terluna run
  imported on 2026-10-17 byte for byte (`models/check_patches.sh`; `models/exoplasim/expected.sha256`).
- Prefixes of the series reproduce the source hashes 32 Terluna runs recorded, so each reported result
  can be rebuilt from the series (`models/exoplasim/runs.json`). The two exceptions are explained there.
- The deployed copy compiled and ran (Terluna's runs); this repository compiles nothing itself.

## Defects and hidden Earth repaired

### The Sun's clock (patch 04, `NSUNCLOCK`)

**The defect.** `solang` (radmod.f90, upstream lines 1336–1444) computes the hour angle as
`zmins * zrtim` with `zrtim = rotspd * TWOPI / 1440` and `zmins` the minutes since the start of the
current model day. For `rotspd` ≠ 1 the clock turns at the sidereal rotation rate while the model day
is the solar day `sidereal_day * N/(N-1)`, with N the rotations per 360-day year that ExoPlaSim's
Python rounds to a multiple of 12 (`__init__.py` 2615–2620). Each model day the Sun therefore sweeps
1 + 1/(N−1) turns and jumps back 1/(N−1) of a turn: 1.0° for N = 360, 2.0° at a 2-day rotation, 10°
at 10 days, 33° for any rotation period of about 21–60 days (N = 12). At exactly one day (`rotspd` = 1)
the clock is consistent. On the Moon the sweep left longitudes from 270° E through 0° to 57° E 8.3%
short of their sunlight and the far side near 164° E up to 17% over (Terluna `climate/gcm/README.md`
182–200).

**Correctness.** Reproduction: `sun_check.py` rebuilds the uneven pattern of `A28_dim5` from `solang`'s
arithmetic alone with correlation 1.0000 (`sun_check_A28_dim5.json`). With the synodic clock the
two-year test `A28_dim5_sun_test` gives equatorial sunlight 0.991–1.017 of its row mean, what the new
arithmetic predicts for 12.1 lunar days in a year. Identity: `NSUNCLOCK` 0 is upstream's code path.

**Limits.** Mode 2 assumes a steady, non-synchronous rotation with ExoPlaSim's `slowdown` unused, and
counts turns from step 0, so a run restarted under a different clock setting changes phase. Mode 1 (a
turn per model day) is exact only when the model day equals the solar day.

**Improvement.** Report upstream: the runner's comment (Terluna `exoplasim_run.py` 251) says the bug
was reported, but no issue or record of a report exists in Terluna. The upstream fix is one line of
arithmetic for any non-synchronous planet.

### The orbit default (setting `fixed_orbit=True`)

**The defect.** With `fixedorbit=False`, ExoPlaSim's default, `radmod.f90` (upstream 873–879) passes
`iyrad = 1950 - iyrbp` to `orb_params`, which computes Berger's (1978) orbit of the Earth for that
year and discards the configured obliquity and eccentricity. ExoPlaSim's docstring describes the switch
only as freezing Milankovitch variations (`__init__.py` 2188–2190). Every Terluna run before
2026-09-29 had Earth's 23.695° tilt and 0.0175 eccentricity in place of the Moon's 1.5424° and the
Earth–Moon system's 0.016715: at 86° the rows received 149 W/m² of mean sunlight in place of 29.

**Correctness.** Reproduction: the runs' logs report the orbit used; with `fixed_orbit` the test's log
reports 1.5424° and 0.016715, and the rows' sunlight follows the Moon's orbit within 0.1 W/m² rms
(`sun_check_A28_dim5_sun_test.json`).

**Limits and improvement.** None in the repair. Worth an upstream documentation change: any
exoplanet run that sets an obliquity without `fixedorbit=True` has Earth's seasons.

### Cloud water in metres (patch 02, `CWGREF`, `CWSCALE`)

**The hidden Earth.** `mkclouds` (rainmod.f90, upstream ~1950–1980) diagnoses the water clouds hold
for radiation from CCM3's formula, 0.21 g/m³ at the ground decaying with *geometric* height on a scale
of 700 ln(1 + PW) m (PW the precipitable water in kg/m²). At a sixth of Earth's gravity a pressure level
stands six times higher while 700 ln(1 + PW) grows only logarithmically, so clouds above about 20 km,
most of the model's cover, carried almost no water (Terluna `climate/gcm/README.md` 367–394).

**Repair.** `CWGREF` counts heights and PW at a reference gravity (9.80665), putting the formula in
pressure terms; `CWSCALE` scales the diagnosed mixing ratio. `earth_path` (CWSCALE = g/9.80665) gives
each cloud the water path it would hold at the same pressures on Earth; `full_column` (CWSCALE = 1)
keeps Earth's mixing ratio over a column six times heavier, the upper bound.

**Correctness.** Identity: with `plasim` (0, 1) the patched build reran year 39 of run A byte for byte
(`A_patch_check`). Sensitivity: on run A (25% water, the undimmed shield) the bracket spans 292.0 K
(`full_column`) to 298.0 K (`earth_path`), with PlaSim as released at 295.5 K, a value that rests on two
cancelling errors.

**Limits.** The repair keeps CCM3's Earth fit, now in pressure terms: Earth's cloud water at Earth's
pressures. Cloud water stays diagnostic and radiative only (rain comes from the condensation and
convection schemes). Where CM1's ring makes its own ice at 63–107 km it holds 1.5–3.5 times the water
PlaSim gives its clouds there.

**Improvement.** Calibrate cloud water by pressure against a cloud-resolving model at the same forcing,
or carry prognostic condensate.

### Convective cover counted per model day (patch 03, `CONVDAY`)

**The hidden Earth.** Slingo's convective cover, 0.245 + 0.125 ln P with P the convective rain in mm per
day, capped at 0.8, converts rain with `zrfac = solar_day * 1000` (rainmod.f90 upstream 1890). On the
Moon the model's solar day is 29.8 Earth days, so the formula read the rain about 30 times too heavy and
added 0.125 ln 29.8 = 0.42 to the cover, up to the cap. The bias for any world is 0.125 ln(day/1 d).

**Correctness.** Identity: with 0 the patched build reproduced year 14 of `A_earth_path_clouds` byte for
byte; with 86,400 it reproduced the corrected run's first year (`regression_convday_off`, `_on`).
Sensitivity: +1.6 K, cover 22% → 20%.

**Limits.** The repair restores Slingo's unit; the formula itself remains an Earth fit. A run counting
rain per 2,400 s (cover near its floor) warmed the Moon another 1.7 K, so the convective cover's
calibration is a live uncertainty.

### Liquid-only cloud optics (patch 10, `NICEOPT`, `TICEOPT`)

**The weakness.** PlaSim gives every cloud Stephens' (1978) fit of reflection to water path and
0.1 m²/g of infrared absorption. On the Moon the high cloud is cold (165–217 K after the longwave
correction) and thin; liquid optics reflect a seventh to a half of what ice with the same water would
and, at 63–81 km, trap about twice the infrared (`ice_optics.json`).

**Repair.** Below `TICEOPT` (235.15 K, where cloud water freezes by itself), Ebert and Curry's (1992)
extinction, single-scattering co-albedo and asymmetry, as CAM3 and RRTMG carry them, through a
delta-scaled PIFM two-stream for PlaSim's visible band and its near-infrared band as the TSIS-1-weighted
sum of their four bands; in the infrared their grey absorption 0.005 + 1/r m²/g. The effective radius
comes from Kristjánsson and Mitchell's table for hexagonal columns at 180–274 K (CAM3/WRF `reicalc`).

**Correctness.** Reproduction: the patch's Fortran, compiled as PlaSim compiles, matches the Python copy
(`python/climate/gcm/plasim_ice_optics.py`) to nine figures. Identity: with `NICEOPT` 0 the rebuilt
model repeats the longwave check year exactly (`A28_corrected_970_lwcheck_rebuilt`). Sensitivity: in a
year from the design case with the longwave correction, ice keeps 27% of the sky at 81–107 km (30%
without) and halves the high cloud's net warming, 5.7 W/m² in place of 12.4.

**Limits.** Below 180 K the radius follows the table's own trend (5.5% smaller per kelvin) to 2.6 µm at
165 K; Ebert and Curry fitted crystals of 10 µm and more, which the table reaches only from 190 K, so
the top two layers' optics are extrapolated in size. Crystal size has no gravity dependence: in a sixth
of Earth's gravity crystals can grow larger before they fall, which would reflect less and trap less.
The threshold is a step at −38 °C with no mixed phase, and the cloud's amount still comes from humidity
thresholds over liquid water.

### Flat, sunlit-only radiation and Earth's slant path (patch 07)

**The weakness.** PlaSim lights a column only while its Sun stands above the horizon and treats it as
flat layers, and it stretches the low Sun's water path by 35/√(1 + 1224 μ²), whose horizon value 35 is
Earth's Chapman factor √(πR/2H) for H ≈ 8 km. The Moon's air is tall against its radius (mass-weighted
height 48.6 km; a shell 50 km up has 5.8% more area than the ground under it), its horizon factors are
13.5 for water and 7.1 for well-mixed air, and its twilight is long and bright.

**Repair.** A table by solar elevation (−40° to 90°, 167 elevations) of the sunlight the curved air
adds to each layer and the ground (the ground's share in the column's clear share), and of each layer's
and the ground's extra infrared escape, scaled with temperature to the fourth power; and the Moon's
slant factor as (μ + a)/(μ² + bμ + c), a = 0.184013, b = 0.170061, c = 0.0135932 for water (within 0.30%
at every elevation, 1 overhead). The table comes from the curved-air ledger (`python/climate/gcm/twilight.py`;
[reference_radiation.md](reference_radiation.md)).

**Correctness.** Reproduction of the ledger's geometry: a thin shell at 46 km lets out 1.2250 times its
flat escape against the exact 1.2253; its flat side matches the radiative–convective solver within
0.7%. Sensitivity: the 20-year test settles 0.65 K cooler than the design case, the clouds returning
3.5 of the clear sky's 5.4 W/m² loss; a branch with only the curved sunlight warmed 3.7 K in four years.

**Limits.** One clear design column over ground of albedo 0.1 stands for every column and climate; the
infrared terms scale with each layer's temperature alone; no refraction; the ledger's multiple
scattering records `orders_converged = false`, its residual unquantified; clouds enter only through the
ground's clear share. The two 20-year tests flew the first ledger's terms; the standard since 2026-10-14
uses the corrected ledger.

### CO2 and O2 in the sunlight (patch 08)

**The weakness.** PlaSim's two solar bands absorb by Rayleigh scattering and ozone (visible) and water
vapour alone (near infrared). The Moon's column holds 7.2 times Earth's air over each square metre, so
the strongest CO2 and O2 lines go dark high up: with the Sun overhead CO2 alone takes 6.1 W/m² in the
GCM's top layer, where PlaSim took nothing, and the water multiplier had absorbed their share low down.

**Repair.** Three bands (CO2 near infrared at 2.0, 2.7 and 4.3 µm; the O2 A band; O2 B and γ), each an
absorptivity a·u/((1 + b·u)^c + d·u) of its own pressure-scaled path u (mass weighted by (p/1 bar)^n),
fitted to the line-by-line direct beam's loss above each of 100 levels at slant factors 1–13, multiplied
into PlaSim's layer transmissions as water's are, along the well-mixed air's slant path.

**Correctness.** Calibration: largest fit errors 0.06%, 0.13% and 0.04% of each band's energy; by layer
PlaSim comes within 0.97 W/m² rms of the line-by-line column, against 1.71 before. Sensitivity: the
20-year test cools 2.2 K beyond the curved air's test, mostly through PlaSim's cloud: the top layer warms
7 K and its cirrus falls from 2.0% to 0.05%; the cloud-free column moves its ground only 0.57 K.

**Limits.** The fits hold for the design composition (CO2 mass fraction 6.1×10⁻⁴, O2 0.194) and the
paths they span; overlap with water is multiplicative; water's visible bands and the collision-induced
bands stay out of PlaSim and inside the water multiplier.

## Calibrations

### Rayleigh, water continuum and near-infrared water (patches 01 and 05, `TH2OC`)

**What they correct.** Unmodified, PlaSim on a warm, moist lunar column (310 K, 450 kg/m² of vapour)
reflected 0.203 of the clear-sky sunlight against line-by-line's 0.248 and emitted 12 ± 2 W/m² too
little: about 26 W/m² of spurious heating, which carried the uncalibrated design case past 310 K.
ExoPlaSim derives its Rayleigh coefficient from the spectrum normalised to a 5,772 K blackbody's
ultraviolet (0.21 for the filtered Sun); PlaSim's Rayleigh reflectance is an Earth fit compounded by the
column-mass ratio and applied in the lowest layer only; Lacis and Hansen's water absorptivity, fitted to
Earth's water paths, levels off toward half the sunlight and absorbed too little over the Moon's paths,
several times Earth's.

**Values.** `RAYSCALE` 1.8 → 2.215 → 2.237; `TH2OC` 0.024 → 0.004; `SWH2OSCALE` 1.356 → 1.292, refitted
with the slant factors and the gas bands. On the design case's own output the clear air takes
line-by-line's share within 0.6 points rms on 11 new columns; refitted with the bands the daily-mean
split holds within 0.014 points on average and 0.24 rms.

**Limits.** Each is one scalar fitted on the Moon's design columns: valid near this column mass, water
range, spectrum and surface. A larger absorptivity carried over best of three forms tried to columns
the fit did not see (a 303 K column 0.7 points short against 9.7 before; a cooler one 0.2 short). By
layer about 2 W/m² of water's sunlight still lands at 35–66 km in place of 66–85 km and the lowest 7 km,
worth 0.19 K of ground in the column; a pressure exponent on the water path makes the layers worse.

### Longwave by height (patch 09, `NLWCORR`)

**What it corrects.** PlaSim's broadband longwave (Sasamori's absorptivities, its continuum fitted to
the outgoing longwave alone) cools the Moon's moist, massive lower air too much and its upper air too
little: against the correlated-k model on about 2,100 cloud-free 3-day-mean columns, −9.7, −11.9 W/m² in
the lowest two layers (−16 over the sea) and +9.7, +12.0 W/m² in the top two. Refitting PlaSim's own
continuum or path exponents cannot move the cooling by height.

**Repair and correctness.** An extra escape to space for each layer and the ground, over land and over
sea, at reference temperatures and scaled with temperature to the fourth power, the top layer carrying
the outgoing longwave to correlated-k's. The offline copy reproduces PlaSim's heating within 0.01 K a
day; the correction removes every layer's mean error, leaving 1–5 W/m² column to column and within
2.5 W/m² in every band of latitude; in the GCM the patch reproduces the copy within 0.02 K a day.

**Sensitivity and limits.** With ice optics the 20-year test settles near 307 K, 11.5 K above the design
case, with high cloud from 20% to about 40% of the sky. The correction was fitted at 295 K on clear
columns and scales with temperature alone: water vapour, which doubles at the settled state (a global
mean of 170 kg/m² in the design case against 348 kg/m² in the test, years 15–19 of each, read from
their output on 2026-10-17), does not enter it, and Terluna's plan records that its layers stray
5–7 W/m² at 302 K. The 307 K state is therefore a
sensitivity of the model to its longwave's vertical placement, conditional on a correction used beyond
its fit; its check at the settled state is open.

**Improvement, in order.** (1) Refit at the settled state and iterate to consistency (offline, minutes);
(2) carry humidity in the correction; (3) replace Sasamori's scheme with a reduced correlated-k scheme
built from the same spectroscopy.

## Capability

### Infrared from space (patch 06)

Identity: at zero the patched build repeats the unpatched one exactly (`A28_cal_control_patched`). The
flux enters as broadband downward longwave at the top and is carried down with PlaSim's broadband
transmissivities, so its spectrum is ignored; about 4% of the ring fleet's glow reaches the ground and
the dimming that offsets it is 0.71 of its watts on the earlier radiation, about 0.59 on the corrected
radiation. The same hook carries any infrared source above the air: a host planet's glow for a moon.

## Settings and inputs

- **Whole model days** (`runsteps` 17,160): before 2026-09-29 each year ran 17,280 steps and the output
  means slipped 120 steps against the Sun each year. The orbit and seasons follow the sidereal year
  (`n_steps_per_year = sidereal_year / timestep`, plasim.f90 upstream 1354), so the shorter model year
  affects only output bookkeeping.
- **The spectrum's tail**: the first runs held the last measured flux constant past 2.7 µm, which put
  86% of the sunlight in the near-infrared band, an albedo of 0.14 and a Moon past 320 K; a 5,772 K tail
  matched at the spectrum's end fixed it, and the runner now stops if the split falls outside 0.3–0.7.
- **Radius convention**: ExoPlaSim multiplies the radius in Earth radii by 6,371,220 m; the runner
  divided by 6,371,000 m, so PlaSim's radius is 60 m (0.0035%) long. Negligible.
- **Placeholder land** (albedo 0.2, roughness 2 m, a 0.5 m bucket), a 50 m slab ocean without ocean heat
  transport, no ozone (the titania shield's design).

## What stays Earth's in PlaSim

| Part | Consequence on the Moon | Route |
|---|---|---|
| Cloud cover from relative humidity, thresholds `max(0.85, σ, 1−σ)`, saturation over liquid at all temperatures | High cloud starts at 136–149% of ice saturation; cover 17–46% depending on settings; moves the Moon between about 289 and 297 K across tested settings | CRM-informed cover; saturation over ice below freezing |
| Earth's σ levels | The top three layers span 0–9, 9–20 and 20–32 kPa (above 107 km, 81–107 km, 63–81 km); each spans about 25 K and ice saturation changes 55-fold across the 81–107 km layer, where the coldest, most saturated air lies | More levels in the upper troposphere and tropopause region |
| Instant rain-out | No fall or evaporation of rain; CM1 finds 85% of the falling water evaporating at lunar gravity | Rain evaporation with fall time; CRM calibration |
| Two layers in the lowest 6.5 km | The boundary layer's day–night shape is unresolved; the GCM stays stable by day where CM1 mixes 14–19 km deep | More levels; a boundary-layer scheme tested on long days |
| Constant gravity and a thin shell | The column holds about 5% more air per unit area than p_s/g_s (the radiative–convective model's g(z) column); constant-g heights read about 5% low at 86 km; g there is 9% lower | Deep-atmosphere dynamics (White et al. 2005); or correct the mass and heights |
| Top layer from 112 km to the top of the air (575 km for 0.1 Pa) | One layer carries the whole upper atmosphere's radiation | A higher-resolution top; the middle-atmosphere model for the base of the thermosphere |
| Sasamori longwave, Lacis–Hansen shortwave | Calibrated near the design column only | k-distributions from the same spectroscopy |

## Offline copies of PlaSim's radiation

`python/climate/gcm/plasim_shortwave.py` and `plasim_longwave.py` repeat PlaSim's clear-sky shortwave and
longwave arithmetic for one column so their corrections can be fitted against the line-by-line and
correlated-k models without running the GCM. Reproduction: the shortwave copy matches the GCM's own
clear-sky split within 0.4 points on all 11 columns of the corrected Sun's test; the longwave copy
matches PlaSim's own heating within 0.01 K a day on the run's cloud-free 3-day means. Their fitting
drivers read GCM output (netCDF) and Terluna's column choices; their column arithmetic runs alone.

## Improvements in order of value

1. Check and refit the longwave correction at the settled state before the target climate is chosen.
2. Constrain PlaSim's cloud amount and water with cloud-resolving runs forced from the same GCM state.
3. Add upper-tropospheric levels where the lunar cold trap lies (60–110 km).
4. Replace the broadband schemes with reduced k-distributions built from the in-house spectroscopy.
5. Correct the column mass and heights for gravity falling with height, or move to a deep-atmosphere core.
6. An independent GCM (ROCKE-3D or the LMD Generic PCM) on the same scenario.
7. Upstream: the Sun clock, the orbit default's documentation, and the switches whose defaults are identity.
