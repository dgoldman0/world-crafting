# ExoPlaSim on a breathable Moon: correctness, limits and room for improvement

Notes on the fourteen patches in [../models/exoplasim/](../models/exoplasim/), Terluna's ten, the lab's patch 11 and
patches 12 to 14, which the lab wrote from Terluna's surface transfer and its rain from drop sizes, the settings that
carry the Moon, the offline copies of PlaSim's radiation, surface transfer and falling rain in `python/climate/gcm/`,
and what in PlaSim stays Earth's. References to Terluna are at commit 186b294 unless another commit is named; to
ExoPlaSim, at the 3.4.2 source distribution.

Evidence states used below: **reproduction** (the same code or arithmetic gives the same numbers),
**identity** (a switch at its default gives the output of the build without the patch byte for byte, the unpatched
model's for patches 01–10), **calibration**
(agreement with the in-house line-by-line model on the GCM's own columns, by construction near the
fitted columns), **sensitivity** (what the change does to the simulated climate). None of these is a
physical validation of a lunar climate, which no observation can supply.

## How the series was checked as a whole

- Applied with GNU patch to pristine ExoPlaSim 3.4.2, patches 01–10 reproduce the copy every Terluna run
  imported on 2026-10-17 byte for byte (`models/check_patches.sh`; `models/exoplasim/expected.sha256`), and the
  series of fourteen gives the sources of `models/exoplasim/expected-series.sha256`.
- Prefixes of the series reproduce the source hashes 32 Terluna runs recorded, so each reported result
  can be rebuilt from the series (`models/exoplasim/runs.json`). The two exceptions are explained there.
- The deployed copy compiled and ran in Terluna's runs. The lab compiles each point of the series in its store
  (`lab/worldlab/builds.py`), and its build of patches 01–10 compiles the deployed sources byte for byte.

## Defects and Earth values repaired

### The Sun's clock (patch 04, `NSUNCLOCK`)

**The defect.** `solang` (radmod.f90, upstream lines 1336–1444) computes the hour angle as
`zmins * zrtim` with `zrtim = rotspd * TWOPI / 1440` and `zmins` the minutes since the start of the
current model day. For `rotspd` ≠ 1 the clock turns at the sidereal rotation rate while the model day
is the solar day `sidereal_day * N/(N-1)`, with N the rotations per 360-day year that ExoPlaSim's
Python rounds to a multiple of 12 (`__init__.py` 2615–2620). Each model day the Sun therefore sweeps
1 + 1/(N−1) turns and jumps back 1/(N−1) of a turn: 1.0° for N = 360, 2.0° at a 2-day rotation, 10°
at 10 days, 16° for rotations of 12–20 days (N = 24) and 33° for any rotation slower than 20 days, since N is floored at 12
(corrected 2026-10-17; `paper/data/regime_calc.json`, `exoplasim_slow_rotators`). At exactly one day (`rotspd` = 1)
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

**Improvement.** The author reported the defect upstream as ExoPlaSim issue #69 on 2026-09-29
(github.com/alphaparrot/ExoPlaSim/issues/69), which places it in non-synchronous runs with `rotationperiod`
≠ 1 and `keplerian=False`; it was open and unanswered on 2026-10-17, and Terluna's record does not link it.
The upstream fix is one line of arithmetic for any non-synchronous planet.

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

**The Earth value.** `mkclouds` (rainmod.f90, upstream ~1950–1980) diagnoses the water clouds hold
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

**The cold cloud at lunar gravity, in Terluna.** Terluna's factors for the cold cloud, worked out from slabs of
rising air at lunar gravity, give the cloud at 63–107 km 37–42 times PlaSim's Earth water path, with crystals
1.6–1.7 times as large (Terluna `domain/climate` f999492). In a 20-year run from Terluna's 301 K design years the
thicker ice warms its own layer, PlaSim's cover at 81–107 km falls from a third of the sky to a seventh, the ground
absorbs 14 W/m² less sunlight, and the climate settles near 298.5 K, 2.8 K cooler, with 19% less rain; Terluna judges
the cover's response, a diagnosis from humidity that a lasting lunar ice cloud would outlast, the run's least
certain part (79dd316).
Halving or doubling the top three layers' cloud water or crystal size moves the top of the air by 8–11 W/m² and the
ground by 5–7 K, to first order (8641746).

**Improvement.** Calibrate cloud water by pressure against a cloud-resolving model at the same forcing,
or carry prognostic condensate.

### Convective cover counted per model day (patch 03, `CONVDAY`)

**The Earth value.** Slingo's convective cover, 0.245 + 0.125 ln P with P the convective rain in mm per
day, capped at 0.8, converts rain with `zrfac = solar_day * 1000` (rainmod.f90 upstream 1890). On the
Moon the model's solar day is 29.8 Earth days, so the formula read the rain about 30 times too heavy and
added 0.125 ln 29.8 = 0.42 to the cover, up to the cap. The bias for any world is 0.125 ln(day/1 d).

**Correctness.** Identity: with 0 the patched build reproduced year 14 of `A_earth_path_clouds` byte for
byte; with 86,400 it reproduced the corrected run's first year (`regression_convday_off`, `_on`).
Sensitivity: +1.6 K, cover 22% → 20%.

**Limits.** The repair restores Slingo's unit; the formula itself remains an Earth fit. A run counting
rain per 2,400 s (cover near its floor) warmed the Moon another 1.7 K, so the convective cover's
calibration is a live uncertainty.

**A defect by ExoPlaSim's own design (finding, 2026-10-17).** ExoPlaSim's description says it replaced the
solar day with a standard 86,400 s in its unit conversions (Paradise et al. 2022, Sect. 2.1); this
conversion is one that replacement left in place, so the paper classes it with the upstream defects, exact at
a one-day model day. It also acts in synchronous runs: `configure(synchronous=True)` sets only `NFIXED` and
`FIXEDLON` (`__init__.py` 2628–2630), while the rotation period still sets `ROTSPD` and
N = max(int(360/P/12 + 0.5), 1) × 12 (2616–2619), so `plasim.f90` (1296–1300) gives a model day of P·N/(N−1)
and the cover gains 0.125 ln of it: +0.23 for TRAPPIST-1e's 6.1-day rotation and +0.31 for Proxima Centauri b's
11.2 days (`paper/tools/regime_calc.py`, `exoplasim_synchronous_cover_bias`). It deserves an upstream report
alongside the Sun clock's.

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

**The weights (patch 11, `ZICEW`).** Patch 10 weights its four near-infrared bands within PlaSim's band 2
by constants Terluna computed from the unfiltered TSIS-1 Sun, with a tail 11% brighter than the rest of
the Sun's constant: 0.6164, 0.2283, 0.0811 and 0.0742. Patch 11, the world-crafting lab's, reads them from
the namelist with those constants as its default, and the lab writes the shares of the light at the top of
the air, the filter included (`lab/worldlab/sunlight.py`): 0.6295, 0.2276, 0.0752 and 0.0677 through the
Open Moon's shield, and 0.6202, 0.2297, 0.0816 and 0.0685 for the unfiltered Sun. Identity: at its default
the build of patches 01–11 runs Earth's control with ice optics on, over 96 steps, byte for byte as the
build of patches 01–10, output and status alike, and the Sun's own weights change the output
(`lab/tests/test_builds.py`), where the two run folders differ in the four weights alone, which shows the ice
path ran. The broadcast of the weights
to every rank is correct by reading, since a run whose root alone held them would pass the test as well. The weights stay one set for the whole planet, from the light at the top;
the light that reaches a cloud below other absorbers is redder.

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

### The gust and the similarity over water (patches 12 and 13, `NGUST`, `NSIMW`)

**The Earth values.** Over unstable water `surflx` multiplies its transfer of heat and vapour by Miller, Beljaars
and Palmer's (1992) factor, (1 + (0.0016 Δθ_v^⅓/(|U| C_N))^1.25)^0.8, whose constant is the still-air limit of a tank
law at Earth's gravity and sea-level air, and it holds the wind of every bulk formula at 1 m/s or more. On the
3-day means of Terluna's fifteen-level runs, which smooth the wind and so overstate the term, the factor raised the
transfer at the Near-side Sea site 1.71–2.14 times, where the tank law carried to lunar gravity and the design air's
pressure gives 1.33–1.53 (Terluna `climate/gcm/README.md` at `39c5ee04`; defect log B33).

**Repair.** Patch 12 puts in their place the physics that Beljaars (1995), a co-author of the 1992 factor, proposed:
under a convective boundary layer the layer's large eddies sweep the surface at about their convective velocity
w* = (g/θ_v · h · (w′θ_v′)₀)^⅓, which joins the mean wind in the bulk formulas, so that gravity, the layer's depth
and the buoyancy flux each enter explicitly. With `NGUST` 1 every surface takes Louis's factors under that wind, its
least value CM1's 0.1 m/s, with the buoyancy flux from the step before's fluxes and the depth from the bulk
Richardson rule of Terluna's nonlocal boundary layer. Patch 13 then takes, over ice-free water, the transfer of CM1's
own surface layer at the lowest level's height (`NSIMW` 1): under the same gust Louis's factors evaporated 0.72–0.74
of that similarity's water on the air of Terluna's sea box and 0.82 on its GCM's, most of the difference in light
wind over warm water. The similarity's viscosity is each column's own, from the model's pressure, temperature and
gas constant with Sutherland's law, where CM1's code sets the viscosity of Earth's sea-level air;
[../models/exoplasim/README.md](../models/exoplasim/README.md) lists which of the two patches' values are the
world's and which stay Earth's.

**Correctness.** Identity: on Earth's control over 96 steps, each patch at its default gives the output and the
restart of the build before it byte for byte, patch 13 with the gust off and with it on (`lab/tests/test_builds.py`).
Reproduction: `surflx` from the patched source gives the transfer of the Python copies
(`python/climate/gcm/surface_gust.py`, `surface_similarity.py`) to 10⁻¹⁰ at the Moon's gravity and Earth's; the
gust's copy gave Terluna's module's numbers bit for bit on its 24 test columns, and the similarity's gives them to
10⁻¹² at the one viscosity both of CM1's lines share (`python/climate/tests/`). On one column in σ the gust's depth
goes as 1/g and its velocity keeps its value, since the heights go as 1/g and the buoyancy as g. Sensitivity, in
Terluna's runs with its own patches: the gust lowered the sea site's transfer coefficient for vapour to 0.67 of the
baseline's over four years, the sea warming 1.2 K and the globe 0.18–0.55 K with 6% less rain, and the similarity
then raised the sea's evaporation 17% and the globe's rain 5% over one lunar day. In the lab's two-day test on
Earth's control from a cold start, the gust changes the output and the similarity changes it again
(`lab/tests/test_builds.py`).

**Limits.** The similarity takes a constant flux up to the lowest level, 0.15 km on Earth's ten levels and 0.9 km
on the Open Moon's, where Terluna's fifteen-level set stands at 0.3 km. The depth comes from the model's levels, is
at least the lowest level's height, and is untested against CM1's depths. The step before's fluxes and the
similarity's carried state stay outside the restart, so each restarted segment begins with one step that takes no
gust and with the similarity at its start values. Charnock's constant, the 2.85 mm cap on the sea's roughness, Fairall's
roughness for heat and vapour and Paulson's functions remain fits to Earth's seas and surface layer. The Earth
control's test, which decides whether the two switches serve every world, is still to be run, and until then the
lab's default keeps the released model's transfer.

**Improvement.** The Earth control's test; the carried state and the fluxes in the restart; a warning where the
lowest level stands above a tenth of the boundary layer's depth; and the sea's roughness from the ensemble's wave
model at the world's gravity in place of Charnock's constant and its cap.

### Rain from its drops' sizes (patch 14, `NEVAPPREC` 2)

**The Earth value.** `mkrain` evaporates falling rain by one constant, `gamma`: in each unsaturated layer the rain
loses the share 0.01 of the layer's saturation deficit in each step, whatever its drops' sizes, their fall speeds or
the layer's depth. The constant was set for Earth. On the Moon PlaSim evaporated 29% of its rain where CM1's boxes
with lunar drops evaporated 61% over the sea and over land, and one constant matched the sea box at 0.027 and the
land box near 0.046 (Terluna `domain/climate` 05b1384, 30e7f83; defect log B30).

**Repair.** Patch 14 gives the rain its drops. With `NEVAPPREC` 2 each column's rain takes a number flux down beside
its mass flux, so that the slope of Morrison's exponential spectrum follows from the two, and through each layer the
rain evaporates by the ventilated diffusion of its drops, as CM1's Morrison scheme evaporates its own, while the
drops collect one another and break up toward the breakup's equilibrium size. The mean fall speeds and the
ventilation integral come from the fall law of the world's rain, a table of the single-drop solver's speeds in the
world's air that the run's folder holds and that CM1's rain law reads as well; gravity scales the bounds on the mean
diameter, the cap on the fall speeds and the breakup's lengths; and the namelist gives the world's self-collection
rate and the breakup's density exponent. New rain enters each layer at its middle, melted rain at one size and rain
formed as rain by a rule: every new drop at one size, all of it added to the drops falling, or the share W/(W + F)
of it as new drops. That rule and the two sizes are a calibration on cloud-resolving boxes, which a study supplies
for its world; [../models/exoplasim/README.md](../models/exoplasim/README.md) lists which of the patch's values are
the world's and which stay Earth's, and records Terluna's calibration for the Open Moon, the share rule with
0.439 mm and 2.95 mm.

**Correctness.** By evidence state:

| Evidence | What it shows | Where |
|---|---|---|
| Identity | On Earth's control over 96 steps the whole series' build gives the output and the restart of the build of patches 01–13 byte for byte, with `NEVAPPREC` unstated and stated as 1; `mkrain` alone prints the same digits with 1 and with 0, under ExoPlaSim's flags and under `-O3 -march=native` | `lab/tests/test_builds.py`; `python/climate/tests/test_rain_drops.py` |
| Reproduction | `mkrain` from the patched source gives the Python copy's tendencies and precipitation to 10⁻¹⁰ under each birth rule at the Moon's gravity and Earth's; the copy agrees with hand arithmetic on a power law's closed forms to 10⁻⁹ and keeps each column's water; from the Open Moon's air it gives the sums of Terluna's module on that module's test columns | `python/climate/tests/test_rain_drops.py` |
| Reproduction, single scratch runs of 11 November 2026 | The copy gave every field of Terluna's module at `39c5ee04` bit for bit on 72 columns; twelve wrong statements put one at a time into the patch each failed the suite | `models/exoplasim/README.md` |
| Sensitivity, in the lab's tests | With the drops' sizes Earth's control changes its output over two days, and Earth's control under the Moon's gravity runs two days under floating-point traps and ends in another state than with `gamma` | `lab/tests/test_builds.py` |
| Sensitivity, in Terluna's runs with its own patch | Offline on three CM1 boxes of the Open Moon the share rule gave 0.96–1.05 of CM1's column evaporation with CM1's melted size and 0.91–0.98 with the lunar one; in PlaSim over one lunar day it evaporated 45% of the rain formed against `gamma`'s 20% and brought 1.71 mm/day to the ground against 2.00, the ground ending the day 0.2 K cooler | Terluna `climate/gcm/README.md` at `39c5ee04` |

**Limits.** The births are the Moon's calibration, fitted on three boxes on fifteen levels, and the share of new
drops depends on the layers' thickness, so another world, level set or box microphysics takes its own; the lab
has none besides Terluna's, and its writer refuses the drops' sizes without one. The boxes behind it ran Earth's
rates of autoconversion and accretion (defect log B38) and ice sized by Earth's limits. The collisions follow
Morrison's self-collection and breakup, taken to another gravity by a similarity that no measurement there tests,
and the vapour's diffusivity and the air's viscosity are fits for Earth's air. The scheme evaporates and collects at
the grid cell's mean air and rain content, and the snow still sublimates by `gamma`. The Earth control's test, which
decides whether the scheme serves every world, is still to be run, and until then the lab's default keeps `gamma`.

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
case, with cloud cover from 20% to 38% of the sky, most of the gain in the high layers (the 81–107 km layer from
5.6% to 27% in the check year; corrected 2026-10-17 from "high cloud from 20% to about 40%"). The correction was fitted at 295 K on clear
columns and scales with temperature alone, so water vapour, which doubles at the settled state (a global
mean of 170 kg/m² in the design case against 348 kg/m² in the test, years 15–19 of each, read from
their output on 2026-10-17), stays outside it. The 307 K state is therefore a
sensitivity of the model to its longwave's vertical placement, conditional on a correction used beyond
its fit.

**At the settled state, in Terluna.** Checked near 301 K, the 295 K fit leaves layers up to 5.9 W/m² off over land
and 6.8 over the sea at 301.2 K, and 4.2–7.6 W/m² in the worst layers at 302.5 K; a refit on 301 K columns holds
within 0.3 W/m² there (Terluna `domain/climate` 6fb0958). Each fit is tied to its state, level set and convection
scheme: on Terluna's settled 301 K design years the refit holds within 1.9–2.65 W/m² by layer against Terluna's
2.5 W/m² rule (8641746), the Betts–Miller scheme's climate leaves it 3.38 W/m² off (5578b55), and carried onto 14 or
15 levels it leaves 6.4–8.8 W/m², so runs on those sets take a refit on their own columns (6c78965, 805691b,
00da68d, 3fd43d5). With the 301 K refit, rebuilt lakes and the curved air rebuilt on a 301 K column, Terluna's design case
holds 301 K at a sunlight scale of 0.897, where the design case here took 0.970 for 295 K (8641746, b73fa08).

**Improvement, in order.** (1) Refit for each state, level set and convection scheme, as Terluna now does;
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
- **The humidity in the output**: in low-I/O mode with spectral humidity, `hus` holds the humidity at the end of
  the interval before each record, where every other field is a mean, and each year file's first record holds about
  2% of the vapour. A reader takes each interval's mean as the average of a record and the next and leaves out each
  file's first and last records, Terluna's rule; Terluna's switch `nhusmean` writes the true mean as a further field
  (defect log A10).
- **The equinox's regression**: Terluna's precession patch (`domain/climate` 39ac7f0c, awaiting its port) counts
  the regression from a starting step. A branch from a precessing run inherits its parent's count; started again at
  zero, the equinox would have jumped back 189° in Terluna's first such branch (43b14b38). The port carries the count
  through restarts and branches.
- **The Sun's distance**: the set-up takes the Earth–Moon barycentre's orbit, so the Moon's monthly swing toward
  and away from the Sun is left out. That swing moves the sunlight ±0.51% in step with the lunar day, and the far
  side's noon receives 1.0% more than the near side's. The set-up states the choice, an idealisation of the scenario,
  and the lab offers the swing as an option (defect log C22).

## What stays Earth's in PlaSim

| Part | Consequence on the Moon | Route |
|---|---|---|
| Cloud cover from relative humidity, thresholds `max(0.85, σ, 1−σ)`, saturation over liquid at all temperatures | High cloud starts at 136–149% of ice saturation; cover 17–46% depending on settings; moves the Moon between about 289 and 297 K across tested settings | CRM-informed cover; saturation over ice below freezing |
| Earth's σ levels | The top three layers span 0–9, 9–20 and 20–32 kPa (above 107 km, 81–107 km, 63–81 km); each spans about 25 K and ice saturation changes 55-fold across the 81–107 km layer, where the coldest, most saturated air lies | More levels in the upper troposphere and tropopause region |
| Kuo-type deep convection (`nprc` 1), its parcel lifted undiluted from the surface | It rains a column's moisture supply, the surface's evaporation included, wherever the parcel is buoyant: over the Near-side Sea 2.9 mm/day after midnight under sinking air, where CM1's box rains 0.14–0.17 mm/day; it holds the upper air within 1.3 K of the undiluted adiabat, where CM1's mixing updrafts hold theirs 3.0–6.3 K below, and CM1's air at 42–56 km runs 7.7–10 K colder (Terluna `domain/climate` f07ad8d, 467a146) | A scheme fitted to CM1's mixing and timing: Terluna's simplified Betts–Miller (`nprc` 2) and mass-flux (`nprc` 3) schemes, behind PlaSim's own switch; so far each setting misses CM1's rain by time of day at one site or both, and in single columns the mass-flux scheme goes deep on every step of the sea's night (6d0c707; defect log B29) |
| Rain evaporation by one constant (`gamma` 0.01 in `mkrain`), at the series' defaults | Falling rain evaporates a share of each layer's saturation deficit per step, with no drop size or fall speed: 29% of PlaSim's rain on the Moon, an ordinary share on Earth, against 61% in CM1's corrected boxes; matching them takes 0.027 over the sea and about 0.046 over land (05b1384, 30e7f83) | Rain evaporated from its drops' sizes and fall speeds, patch 14 (`NEVAPPREC` 2), with the fall law computed for the world; it stays off until the Earth control's test, and the snow's sublimation keeps `gamma` (defect log B30) |
| With `NEVAPPREC` 2: the rule and the two sizes of the rain's births, a calibration; Morrison's ventilation coefficients, his fits for the vapour's diffusivity and the air's viscosity, the breakup law's form and the density factor's exponent 0.54 | The lab has one calibration of the births, Terluna's for the Open Moon on fifteen levels, from CM1 boxes that ran Earth's warm-rain rates and Earth-sized ice. Gravity enters the layers' depths, the fall law's table, the bounds, the cap and the breakup's lengths explicitly, and the fits are for air of Earth-like composition | A calibration of the births for each world and level set, from boxes with the warm rain and the ice at the world's gravity; the snow's sublimation by its flakes, once assessed |
| Earth's σ levels near the ground | At the Moon's 51 km scale height the lowest layer spans 0–1.73 km and one layer 6.4–13.7 km: the bottom layer averages away the 1.4–2.3 kJ/kg of moist static energy that CM1's afternoon and evening updraughts draw from the surface layer, and CM1's 6 km night boundary layer and its clouds' 7–8 km tops fall inside one layer (697ac36, 03e7c41) | More levels near the ground: Terluna's 14- and 15-level sets, the lowest level near 0.3 km, at about 1.5 times the run's cost, each with a longwave refit on its own columns (defect log B31) |
| Vertical diffusion's mixing lengths (160 m for momentum, 438 m for heat and vapour) and its least wind shear of 1 m/s (`zumin`) | Over the Near-side Sea after midnight CM1 mixes to 6.5 km and the GCM to 4.3 km; through the day CM1 carries 28–112 W/m² of vapour up through 5.2 km, mostly by resolved motion, where PlaSim's median diffusivity is 0.1–0.3 m²/s (21d98fc) | Lengths scaled with gravity, an untested scaling; a nonlocal scheme with explicit entrainment, tested in single columns, brings the land's afternoon mixed layer down toward CM1's and misses the sea's night, where Terluna reads CM1's 10–12 W/m² of heat carried down through 6–7 km as entrainment driven from the cloud's top (6d0c707; defect log B32). In the surface transfer, where the same `zumin` floors the wind, patch 12's gust takes its place with `NGUST` 1 |
| Free-convection constant over water, 0.0016 m s⁻¹ K⁻¹ᐟ³ (Miller, Beljaars and Palmer 1992), at the series' defaults | Its tank law goes as (g/p_s)^⅓, 0.00083 on the Moon; at that value the Near-side Sea's evaporation falls from 3.82 to 3.62 mm/day, against CM1's 2.98 (b182515) | Beljaars's gust with the similarity over ice-free water, patches 12 and 13 (`NGUST`, `NSIMW`), which drop the term; they stay off until the Earth control's test, and Terluna's lunar value of the constant has no patch here (defect log B33) |
| With `NSIMW` 1: Charnock's 0.0185, the 2.85 mm cap on the sea's roughness, Fairall's roughness for heat and vapour, Paulson's functions, and Sutherland's two constants for the dynamic viscosity of Earth's dry air (`SIMW_MUB`, `SIMW_MUS`), which the lab's writer leaves at the patch's defaults in every run; with `NGUST` 1: β = 1 and the depth rule's constants | Unmeasured. Gravity enters w*, the Richardson numbers, z/L and Charnock's relation explicitly, and the kinematic viscosity takes each column's own density under Earth's dry air's dynamic viscosity, while the cap and Fairall's lengths are fits to Earth's seas | The sea's roughness from the ensemble's wave model at the world's gravity; large-eddy runs at that gravity for β and the depth; the dynamic viscosity of the scenario's own air, written by the adapter |
| Shallow convection's tops capped at 700 hPa | An Earth height, near 28 km in the Moon's air; binds in 1–1.4% of cells (1d05c3d) | A cap tied to the deep-convection depth test (defect log B34) |
| Horizontal diffusion's damping times at the truncation scale: 0.2, 1.1, 5.6 and 0.1 days for divergence, vorticity, temperature and humidity, counted in 24-hour days | Earth's T21 times on a wave 3.7 times shorter: a given wind crosses the Moon's smallest wave 3.7 times faster while the damping keeps its time. The design run's spectra fall smoothly to the truncation except in the vertical motion, flat to wavenumber 18 | The Earth control's spectra as the comparison; one run with the times multiplied by 0.27 (defect log B36) |
| A slab sea 50 m deep (`MLDEPTH`) | Earth's seasonal mixed layer under a 29.5-day cycle of sunlight: the Near-side Sea site's surface swings 0.63 K through the lunar day, and by estimate two to four times that if the heat stays in the top 10–20 m; the sea's rain by time of day depends on the swing | One run at 15 m; the depth as a setting by world (defect log B37) |
| The simplified Betts–Miller scheme's relaxation time, 2 h (`tau_bm`, with Terluna's `nprc` 2) | Frierson's value for Earth; 12 h by the similarity that scales CM1's times | One run at 12 h; the time as a setting scaled with the world (defect log B39) |
| Constant gravity and a thin shell | The column holds about 5% more air per unit area than p_s/g_s (the radiative–convective model's g(z) column), and about 12% more over a square metre of ground once the shells' growing area is counted (defect log B21); constant-g heights read about 5% low at 86 km; g there is 9% lower | Deep-atmosphere dynamics (White et al. 2005); or correct the mass and heights |
| Top layer from 112 km to the top of the air (575 km for 0.1 Pa) | One layer carries the whole upper atmosphere's radiation | A higher-resolution top; the middle-atmosphere model for the base of the thermosphere |
| Sasamori longwave, Lacis–Hansen shortwave | Calibrated near the design column only | k-distributions from the same spectroscopy |

## Offline copies of PlaSim's radiation, surface transfer and falling rain

`python/climate/gcm/plasim_shortwave.py` and `plasim_longwave.py` repeat PlaSim's clear-sky shortwave and
longwave arithmetic for one column so their corrections can be fitted against the line-by-line and
correlated-k models without running the GCM. Reproduction: the shortwave copy matches the GCM's own
clear-sky split within 0.4 points on all 11 columns of the corrected Sun's test; the longwave copy
matches PlaSim's own heating within 0.01 K a day on the run's cloud-free 3-day means. Their fitting
drivers read GCM output (netCDF) and Terluna's column choices; their column arithmetic runs alone.

`python/climate/gcm/surface_gust.py` and `surface_similarity.py` repeat `surflx`'s transfer on one column, as
released and with patches 12 and 13, so that the patches' Fortran can be tested against them without the GCM.
Reproduction: `surflx` from the patched source, compiled alone, gives their transfer coefficients to 10⁻¹⁰ ("The gust
and the similarity over water", above).

`python/climate/gcm/rain_drops.py` repeats `mkrain` with patch 14's rain on columns of any world, and computes what
a run of the patch takes for a world from its air at 2 m: the namelist's entries and, through
`python/atmosphere/rain/fall_law.py`, the table. Reproduction: `mkrain` from the patched source, compiled alone,
gives the copy's tendencies and precipitation to 10⁻¹⁰ ("Rain from its drops' sizes", above).

## Improvements in order of value

1. Constrain PlaSim's cloud amount and water with cloud-resolving runs forced from the same GCM state; by a
   first-order estimate the high cloud alone moves the ground 5–7 K per factor of two in its water or crystal size.
2. Replace the Kuo closure with a scheme fitted to CM1's mixing and timing, on levels that resolve the lowest
   kilometres, with a boundary layer that mixes through its whole depth, including entrainment driven from a cloud
   layer's top.
3. Refit the longwave correction for each state, level set and convection scheme.
4. Add upper-tropospheric levels where the lunar cold trap lies (60–110 km).
5. Replace the broadband schemes with reduced k-distributions built from the in-house spectroscopy.
6. Correct the column mass and heights for gravity falling with height, or move to a deep-atmosphere core.
7. An independent GCM (ROCKE-3D or the LMD Generic PCM) on the same scenario.
8. Take the gust and the similarity over water through the Earth control's test, carry their state in the restart,
   and warn where the lowest level stands above the surface layer.
9. Take the rain from its drops' sizes through the Earth control's test, and fit its births for each world and
   level set on boxes whose warm rain and ice follow the world's gravity.
10. Upstream: the Sun clock, the orbit default's documentation, the free-convection constant's gravity, and the
   switches whose defaults are identity.
