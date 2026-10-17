# CM1 on a breathable Moon: correctness, limits and room for improvement

Notes on the CM1 r22.0 patches in [../models/cm1/](../models/cm1/) other than the electrification
(see [electrification.md](electrification.md)). References to Terluna are at commit 186b294; to CM1, at
the pinned r22.0 source. Evidence states: **reproduction**, **identity**, **calibration** and
**sensitivity**, as in [exoplasim.md](exoplasim.md); none is a physical validation of a lunar climate.

## The series as a whole

Applied with GNU patch to pristine CM1 r22.0, the series reproduce every Fortran source of the
deployed builds behind Terluna's current results: the corrected and twilight 45° rings, the sideways
ring, the highland and Jura boxes, the Earth-fall box and the main electrified run
(`models/check_patches.sh`; [../models/cm1/builds.json](../models/cm1/builds.json)). Three facts about the
deployed builds matter for reading results:

- `moon_omp` was compiled on 2026-09-28 at CM1's own -O2 and never rebuilt after the 2026-09-30
  decision to compile OpenMP builds at -O3 -march=native. `ring_45n_corrected` and
  `ring_45n_corrected_sideways` ran on it; `ring_45n_corrected_twilight` ran on `moon_omp_twilight` at
  -O3. The twilight pair therefore differs in its compile flags as well as its twilight hook; Terluna's
  own test found -O3 runs departing from -O2 runs by 0.28–0.32 °C rms at 2 m within a day, with domain
  means within 0.04 °C, so the pair's reported 0.013–0.021 K effect of the twilight lies below what the
  pair can resolve. The sideways pair shares one build.
- `earth_g_omp_elec` predates the 2026-10-06 ventilation scaling; at Earth's gravity that scaling is the
  identity, so the Earth benchmarks stand.
- The MPI builds `moon` and `earth_g` (2026-09-26) predate core patches 10–17; no recorded case ran them.

Runs on more than one thread are realizations: CM1's own threaded loops race on the cases' paths (a
restarted box parted from itself 50–85 steps in on four threads), while one-thread runs repeat bit for
bit (Terluna `climate/crm/README.md` 80–110).

## Gravity (core patches 01–03)

**The hidden Earth.** CM1 r22.0 sets g = 9.81 in `constants.F` (the dynamics), separately in
`module_ra_etc.F`'s `module_model_constants` (whence RRTMG's `rrtmg_lw_ini`/`rrtmg_sw_ini` take their
`grav` for absorber mass per layer and for heating rates, and MYNN its gravity), in `getcape.F`, and as
`G` in `morrison.F`. Changing only `constants.F` would leave RRTMG putting a sixth of the lunar air over
each pascal into its gas columns.

**Correctness.** Checked in the pinned source on 2026-10-17: RRTMG's internal `grav` is set from the
patched constant (`module_ra_rrtmg_lw.F` 8092, `_sw.F` 4763, via `use module_model_constants, only : cp,
grv => g`). Calibration: on each model's own clear column at the equatorial crossing, RRTMG's shares of
sunlight reflected, absorbed in the air and reaching the ground lie within 2.5 points of the in-house
line-by-line model, and within 8 W/m² each over the lunar day; on 990 cloud-free columns of the 45° N
ring, RRTMG cools the air 0.15, 0.12 and 0.11 K a day more than the correlated-k model in its three lowest
GCM layers (4.5, 8.5 and 10.2 W/m²).

**Earth's gravity left in CM1 outside the lunar cases' paths.** The pinned source still sets Earth's
gravity in schemes the lunar cases do not select: the MYNN surface layer (`module_sf_mynn.F` 1294, 1320,
1348, 1375, 1582), the GFS EDMF boundary layer and GFDL surface layer (`module_gfs_physcons.F` 13,
`module_sf_gfdl.F` 918, in cgs), the exchange coefficients for hurricane runs (`module_sf_exchcoef.F` 38–208),
the P3 (`module_mp_p3.F` 206), WSM6 (`mp_wsm6.F` 106), Jensen–Ishmael (`module_mp_jensen_ishmael.F` 37) and
LFO (`lfoice.F` 122) microphysics, and the Goddard radiation (`radtrns3d.F` 1725). CM1's `omega` is Earth's
2π/86,400 s and its `earth_radius` 6,370 km; both enter only the stock beta plane, which the tilted rings
replace and the boxes leave off. A case that switches to any of these options brings Earth's gravity
back, and a port to another world should either patch them or refuse them.

## Fall speeds (core patch 04)

**The repair.** In Morrison's scheme a particle regime V = A·D^B has a Reynolds number growing as the
Best number X to the power (B + 1)/3; X is proportional to g, so at a fixed size V ∝ g^((B+1)/3): cloud
droplets (Stokes, B = 2) fall 6.0 times slower at lunar gravity, rain (B = 0.8) 2.9 times, graupel
(B = 0.37) 2.3 times. The caps on mean fall speeds scale alike.

**Correctness.** The scaling is exact for particles whose mass grows as D³ and whose area grows as D²
(drops, graupel, hail) within the fitted power-law regime. For snow and ice crystals, whose mass and area
follow other power laws, the gravity exponent is (B + 1)/(β_m + 2 − σ_A) and is larger than the patch's.
Sensitivity: with Earth's fall speeds (the `earth-fall` control) the same box brings 77% more rain to the
ground (60 against 34 mm per lunar day), evaporates 64% of its falling water against 85%, and runs 1.0 °C
warmer and more humid near the ground.

**Limits (found 2026-10-17, not in Terluna's record).** Morrison's size limits stay Earth's: the slope
bounds cap rain's mean diameter at 2.8 mm and graupel's at 2 mm, and raindrop self-collection is cut
above a 300 µm breakup diameter (the scheme's breakup term, CM1's default `brkup_db`). The largest stable raindrop scales as
(σ/(Δρ g))^½, about 2.5 times larger at lunar gravity, and slower drops collide more gently. Earth's
caps and breakup therefore keep lunar drops small, and small drops evaporate faster, which bears on the
85% evaporation and on the gap with the GCM. Autoconversion and accretion rates carry no gravity and
stay Earth's fits.

## The Sun, the rings and the boxes (core patches 05, 15, 16)

**Correctness.** Reproduction: a six-hour test of ring A gives the Sun's elevation within 8×10⁻⁷ of the
spherical formula and the Coriolis parameter within 3×10⁻¹² s⁻¹ of 2Ω sin(latitude); the rebuilt CM1
reproduced the first model day of `ring_80n_lsw` bit for bit, and again with its vertical wind given as a
table of identical columns.

**Limits.** The rings keep the equinox (the 1.54° tilt's quarter swing of 80° sunlight over the year is
left out). They are two-dimensional, so storms organise into lines, air crosses mountains only over the
top (the terrain ring turned to gales along its whole length), and a ring at a latitude has no
north–south flow. Rain and cloud at a place depend on the slice's direction by a factor of several, while
temperature, humidity and wind at a place agree within about a degree and 0.3 m/s between crossing
rings. A tilted ring holds one upper-air profile along its whole path. A box takes one Sun across 385 km,
12.7° of longitude or about a day of local time. Patch 16 changes the stock beta plane for every run that
uses it.

## Soil (core patch 08)

The slab soil's five layers are 5–80 cm thick in place of 1–16 cm, reaching below the month-long day's
thermal wave (about 0.6 m deep). The change is unconditional in the patched builds. It is a general
repair for any day of more than a few Earth days.

## Forcing a slice of the GCM (core 09–14, 17; terrain 01–09)

**Repairs and capabilities.** Nudging only above 8–16 km leaves the boundary layer and convection free,
as weak-temperature-gradient experiments do; the GCM's mean vertical wind enters CM1's own large-scale
advection, by column along tilted rings and at each column's own height over terrain; a heating and
moistening by local time and height carries the day–night circulation a box lacks and, as one local-time
bin, the GCM's sideways transport a ring lacks; over terrain each column is nudged and forced at its own
height above sea level.

**Correctness.** Reproduction: two three-hour box runs delivered a prescribed heating and moistening at
98% and 99.8% of the expected amounts (the nudging takes back the rest); the terrain build gave surface
pressure 1,087 hPa over ground at 5.6 km against 1,211 hPa at sea level, as the Moon's 52 km scale height
implies; the sideways ring's inputs match its control's byte for byte apart from the forcing file and its
switch, and its first two hours cooled the lowest 2 km 0.021 K and dried it 0.015 g/kg, as the forcing
gives.

**What the forcing revealed.** Without the GCM's sideways transport the 45° N ring drifts warm: its lowest
1.8 km warm from 20.0 to 26.7 °C over two lunar days. The GCM's circulation carries about 15 W/m² of heat
out of the air below 8 km at that latitude; imposed, it removes about a third of the offset (5.9 → 3.7 K
in the lowest 1.8 km). The GCM's eddies faster than its 3-day means add 2%. PlaSim's longwave
over-cooling of its own lowest layers accounts for about 1.5 K of what remains; the rest lies in how the
two models carry the ground's heat upward (CM1 mixes 14–19 km deep by day where the GCM stays stable).
Neither two dimensions (a 3-D box ran warmer), nor the land surface (at most 0.3 °C), nor the slow fall of
rain explains the gap.

**Limits.** The forcing is one-way and prescribed: a box's day–night forcing cannot answer its own warmth,
and no CM1 case has yet been forced from the longwave-corrected GCM. Over terrain the imposed vertical
wind is advected on the first column's metrics, understating vertical gradients by the factor 1 − z/ztop
(under 6% up to 8.3 km of a 150 km model). Cases set up before 2026-10-17 started with the GCM's top
vapour held constant above its top level, 6–15 times ice-saturated at 140–150 km; the ice that formed
stayed through both lunar days. The runner now keeps the top level's share of ice saturation above it
(`held_share_above`), for new cases only.

## The twilight hook (series-twilight)

**Correctness.** In a two-hour test, columns 2–10° past sunset gained 0.016–0.036 K a day of sunlight's
heating, averaged over their levels, where RRTMG gives none. **Sensitivity.** Below what the 45° N pair
can resolve (above). Shells above the model's 150 km top are left out with the air they stand for.

## Radiation inputs and range (found 2026-10-17 unless noted)

- RRTMG's absorption tables run from 1,053.63 hPa down (`module_ra_rrtmg_lw.F` 3845–3848). At the lunar
  sea level, 1,216 hPa, its pressure interpolation extrapolates (fp ≈ −0.72 of a table interval),
  through about the lowest 7.5 km of air; those are the layers where RRTMG over-cools against the
  correlated-k model. The extrapolation is a candidate cause, untested.
- RRTMG takes the Sun's own spectrum scaled to the shield's total (1,198 W/m² for the corrected design
  case), not the shield's filtered spectrum: about 5 W/m² of the air's absorbed sunlight at the crossing
  (Terluna's record).
- Ozone, methane, N2O and CFCs are zero, as the titania shield's design requires; cloud-ice radii reach
  RRTMG capped at 140 µm (logged above the cap in the NSSL runs).

## Constant gravity and a thin shell

CM1, like PlaSim, holds gravity constant with height. The cases reach 150 km, where lunar gravity is 15%
lower than at the ground and constant-g heights read about 8% low. Terluna's radiative–convective model,
which uses g(z), finds the column holding about 5% more air per unit area than p_s/g_s.

## Improvements in order of value

1. Force rings and boxes from the longwave-corrected GCM, with the sideways transport, and test whether
   the near-ground gap closes.
2. Scale Morrison's (and NSSL's) size limits and breakup with gravity, and test the rain's evaporation.
3. Extend RRTMG's tables past 1,054 hPa or replace RRTMG by the in-house correlated-k scheme; give RRTMG
   the shield's spectrum.
4. Two-way coupling, or nesting in the GCM, so the forcing answers the slice's own state.
5. Find and fix CM1's thread race.
6. Gravity falling with height in the base state and hydrostatics for a 150 km domain.
7. Upstream: gravity as one namelist parameter in CM1, honoured by every scheme.
