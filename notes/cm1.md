# CM1 on a breathable Moon: correctness, limits and room for improvement

Notes on the CM1 r22.0 patches in [../models/cm1/](../models/cm1/) other than the electrification
(see [electrification.md](electrification.md)). References to Terluna are at commit 186b294 unless another commit
is named; to CM1, at the pinned r22.0 source. Evidence states: **reproduction**, **identity**, **calibration** and
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

Runs on more than one thread are realizations: on the cases' paths, runs on several threads part, most likely
through CM1's own threaded loops, though the cause remains unlocated (a
restarted box parted from itself 50–85 steps in on four threads), while one-thread runs repeat bit for
bit (Terluna `climate/crm/README.md` 80–110).

## Gravity (core patches 01–03)

**The Earth value.** CM1 r22.0 sets g = 9.81 in `constants.F` (the dynamics), separately in
`module_ra_etc.F`'s `module_model_constants` (whence RRTMG's `rrtmg_lw_ini`/`rrtmg_sw_ini` take their
`grav` for absorber mass per layer and for heating rates, and MYNN its gravity), in `getcape.F`, and as
`G` in `morrison.F`. Changing only `constants.F` would leave RRTMG putting a sixth of the lunar air over
each pascal into its gas columns.

**Correctness.** Checked in the pinned source on 2026-10-17: RRTMG's internal `grav` is set from the
patched constant (`module_ra_rrtmg_lw.F` 8092, `_sw.F` 4763, via `use module_model_constants, only : cp,
grv => g`). Calibration: on each model's own clear column at the equatorial crossing, RRTMG's shares of
sunlight reflected, absorbed in the air and reaching the ground lie within 2.5 points of the in-house
line-by-line model, and within 8 W/m² each over the lunar day. On 990 cloud-free columns of the 45° N ring,
CM1's longwave comes within 0.013 K a day of the correlated-k model in every layer (0.2–1.3 W/m²), and within
0.008 K a day of the same RRTMG run offline (Terluna `domain/atmosphere` fe49ad9).

**Reading CM1's radiative output.** Under `eqtset = 2`, the equation set of the lunar cases,
`radiation_driver.F` stores RRTMG's heating as `lwten = hr*cp/cvm`, and `swten` alike, with cp/cvm 1.38–1.39 in
this air; the tendency CM1 applies converts it back, so the air takes RRTMG's own heating. To compare a stored
tendency with another radiation code, a reader multiplies it by cvm/cp, and in a heat budget beside CM1's other θ
tendencies by cv/cp. CM1 also hands RRTMG the ground's temperature for the air at the ground, which an offline
column has to match (Terluna keeps these conventions in `climate/crm/cm1_output.py`, `domain/atmosphere` fe49ad9).
Terluna's earlier analyses read the stored tendencies as rates at constant pressure, overstating the radiation by
38–40%, and extrapolated the air at the ground from the two lowest layers; the extra cooling of 4.5, 8.5 and
10.2 W/m² in the three lowest GCM layers that the paper's first released draft reports (claim V08) came from those
readings.

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

**Limits.** Morrison's size limits in this series stay Earth's: the slope bounds cap rain's mean diameter at
2.8 mm and graupel's at 2 mm, and raindrop self-collection turns to breakup above a 300 µm mean diameter (CM1's
default `brkup_db`). The largest stable raindrop scales as (σ/(Δρ g))^½, about 2.5 times larger at lunar gravity,
and slower drops collide more gently, so Earth's caps and breakup keep lunar drops small, and small drops evaporate
faster. Autoconversion and accretion rates carry no gravity and stay Earth's fits.

**The lunar limits, in Terluna.** Terluna's later patches read the limits' scaling from `&param3` (`brkup_gscale`,
`brkup_rhor`, `brkup_rhoexp`; 0 gives stock CM1 bit for bit): the breakup lengths and the cap on the mean diameter
grow as (9.81/g)^½, the cap on the mean fall speed shrinks as (g/9.81)^¼, and a density-ratio refinement follows
from the drops' Weber number (after Straub et al. 2010), giving breakup from 0.84 mm, a 6.88 mm cap and a
5.80 m/s fall-speed cap on the Open Moon (Terluna `domain/atmosphere` dd89cef, 8b55847). Over the small box's
second lunar day the lunar limits nearly doubled the rain at the ground, from 33 to 63 mm a lunar day while the box
condensed 43% less water, cut the share of falling water evaporated from 86% to 48% and the cloud cover from 47% to
36%, and warmed the air at 2 m by 1.47 K (90% range 1.24–1.71 K, against a spread of 0.13 K between realizations;
21529d2). A second patch gives Morrison's rain the single-drop solver's fall law as a table and self-collection its
lunar rate, 1.98 times slower than Earth's (Terluna `domain/climate` 5a44e5e). Both are edit lists in Terluna's
runner (`climate/crm/cm1_run.py`), outside this repository's series.

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

**Repairs and capabilities.** The GCM's mean vertical wind enters CM1's own large-scale advection, by column along
tilted rings and at each column's own height over terrain; a heating and moistening by local time and height
carries the day–night circulation a box lacks and, as one local-time bin, the GCM's sideways transport a ring
lacks; over terrain each column is nudged and forced at its own height above sea level. The rings and boxes that
the paper's first released draft reports held their air to the GCM's from 8 km, fully from 16 km, and a box's
day–night table reached 16 km, so that, as in weak-temperature-gradient experiments, the boundary layer and
convection would develop freely below.

**Correctness.** Reproduction: two three-hour box runs delivered a prescribed heating and moistening at
98% and 99.8% of the expected amounts (the nudging takes back the rest); the terrain build gave surface
pressure 1,087 hPa over ground at 5.6 km against 1,211 hPa at sea level, as the Moon's 52 km scale height
implies; the sideways ring's inputs match its control's byte for byte apart from the forcing file and its
switch, and its first two hours cooled the lowest 2 km 0.021 K and dried it 0.015 g/kg, as the forcing
gives.

**The nudging and the convection.** Lunar convection reaches 55–80 km, so a hold from 8 km covers most of the
convecting column. In Terluna's box over the Near-side Sea (5° S, 45° W), forced that way from Terluna's design
climate with the cold cloud's factors (a branch that settles near 298.5 K), the nudging supplied 89 of the 107 W/m² the box's radiation removed, standing in for the deep convection
that forms the GCM's rain at 18–72 km, and the box rained 0.06 mm/day against the GCM's 2.72. The table's stop at
16 km left out the 35.5 W/m² the GCM's circulation takes from the air above, and its interpolation between the
GCM's layers dried the column by 0.55 mm/day (Terluna `domain/climate` 13e7123). Terluna's boxes now take their
forcing from the GCM's own budget at the site, each GCM layer's tendency laid on CM1's levels with its total kept,
through the whole column; they hold their temperature and vapour to the GCM's only above the top of the GCM's
convection, 72 km at both sites, from its next level up at 93 km, and nudge their mean wind toward the GCM's by local
time
(`climate/crm/gcm_site.py`; 2cc5179, 5a44e5e, 13e7123). How far the 8–16 km hold restrained the rings' convection
is unmeasured.

**What the forcing revealed.** Without the GCM's sideways transport the 45° N ring drifts warm: its lowest
1.8 km warm from 20.0 to 26.7 °C over two lunar days. The GCM's circulation carries about 15 W/m² of heat
out of the air below 8 km at that latitude; imposed, it removes about a third of the offset (5.9 → 3.7 K
in the lowest 1.8 km), and the GCM's eddies faster than its 3-day means add 2%. PlaSim's longwave over-cools its
lowest layer by 10.6 W/m² against the correlated-k model, where CM1's departs by 0.2 W/m², and at the ring's
3.9 W/m² per kelvin that difference is worth about 2.7 K of the 3.7 K (Terluna fe49ad9; the paper's first
released draft gives 1.5 K, from the readings of CM1's radiation above). The ring also ran the boundary layer's
density fault (below), which hands the air 1.3–1.5 times the ground's heat and water. Terluna's boxes with that
fault removed and the forcing taken through the column run 1.15 K warmer than the GCM at 2 m over land at 0° E and
0.23 K over the Near-side Sea, over their second lunar day, where the September rings ran 2.4–4.7 °C warmer over
land and 1.8–2.4 °C over the seas. The boxes also differ from the rings in site and forcing state, and they carry
the lunar drop limits, which on their own warmed a box's air at 2 m by 1.47 K; Terluna reads most of the rings'
warmth as the boundary layer's fault (`domain/climate` 30e7f83, `climate/crm/README.md`, "Boxes on the design
climate"). The 45° N ring has yet to be rerun with both changes. Earlier tests at the 0° E crossing found the gap
little moved by two dimensions (a 3-D box ran warmer), by the land surface (at most 0.3 °C) or by the slow fall of
rain.

**Rain against the GCM.** The small box at 0° E forced from the Earth-orbit state rained 34 mm a lunar day where
the GCM rained 129 mm, a factor of about four, with 85% of its falling water evaporating. Terluna traces most of that
gap, by budgets and tests, to the forcing above, the boundary layer's density fault and Morrison's Earth drop
limits (Fall speeds, above). With all three changed, on Terluna's design climate, the land box at 0° E rains 92%
of the GCM's rain on the same cells and at the same hours, mostly in the afternoon, and the sea box rains 31% of it
over its second lunar day and 49% over its third, nearly all between noon and midnight; both evaporate 61% of
their falling water (Terluna 30e7f83, f07ad8d, ac0ee15). After midnight, under the GCM's sinking air, the sea box keeps a 6 km boundary layer with 1,300–1,500
J/kg of CAPE and under 1 J/kg of inhibition; nearly all that CAPE lies above 10 km, and the cloudy updrafts, mixing
in their surroundings four to five times as fast as in the afternoon, stop by 8.3 km. The quiet nights hold on 3
and 2 km grids (b80a012, b29112a), and the night layer, topped by cloud that radiation cools, carries 10–12 W/m²
of heat down through 6–7 km, at least two-thirds of it by CM1's subgrid mixing (6d0c707). PlaSim's Kuo scheme
rains the sea's evaporation through those hours ([exoplasim.md](exoplasim.md), "What stays Earth's in PlaSim").

**The upper air.** Over its third lunar day the settled sea box runs 7.7 K colder than the GCM that forced it at
42 km and 10.0 K colder at 56 km. Its updrafts mix in their surroundings and hold its air at 19–56 km 3.0–6.3 K
below the undiluted moist adiabat of its lowest 0.5 km, as a plume entraining 0.5–1 × 10⁻⁴ per metre would; the
GCM's air stays within 1.3 K of its own adiabat, and the GCM's lowest level carries 4.6 kJ/kg more moist static
energy, worth 3.1–4.0 K aloft. On the GCM's air the two models' longwave codes agree at 35–48 km and part by
2.7–3.8 W/m² at 48–63 km (Terluna 467a146).

**Limits.** The forcing is one-way and prescribed, so the slice's own state leaves its forcing unchanged. Over
terrain the imposed vertical wind is advected on the first column's metrics, understating vertical gradients by
the factor 1 − z/ztop (under 6% up to 8.3 km of a 150 km model). Cases set up before 2026-10-17 started with the
GCM's top vapour held constant above its top level, 6–15 times ice-saturated at 140–150 km; the ice that formed
stayed through both lunar days. The runner now keeps the top level's share of ice saturation above it
(`held_share_above`), for new cases only.

## The simple boundary layer's density

With `ipbl = 2`, CM1's simple boundary-layer scheme hands the solver its tendencies of θ, the mixing ratios and the
wind multiplied by the air's density (`turbtend.F`'s `turbsz`, `turbuz` and `turbvz`), and `solve1.F` adds them as
changes per second. YSU, MYNN and MYJ fill the same arrays with WRF's tendencies per second, so the fault is the
simple scheme's alone; it stands in the released cm1r22.0 and in NCAR's main branch. At the Open Moon's surface,
near 1.4 kg/m³, Terluna's boxes passed 1.32 to 1.35 times the surface's evaporation and 1.46 to 1.51 times its
sensible heat into their boundary layer, with the drag inflated alike; with the density divided out (Terluna's
build `moon_omp_rain_law_pbl`, `domain/climate` 13e7123), the boundary layer's water comes to 0.995–1.000 of the
evaporation. On Earth, where the boundary layer's air weighs 1.0 to 1.2 kg/m³, the same lines inflate the
tendencies by up to about 20%, a figure from the code, untested on an Earth case. Of Terluna's 59 CM1 runs, 51 used
the scheme, every ring and box the paper reports among them, and each carries the bias until a rerun with the fix
sizes it. The series in [../models/cm1/](../models/cm1/) holds the stock scheme; the `lab` branch drafts the
report to CM1's developer (`models/cm1/upstream-ipbl2-density.md`) and adds the fix before any lab case runs (its
plan, stage 3).

## The twilight hook (series-twilight)

**Correctness.** In a two-hour test, columns 2–10° past sunset gained 0.016–0.036 K a day of sunlight's
heating, averaged over their levels, where RRTMG gives none. **Sensitivity.** Below what the 45° N pair
can resolve (above). Shells above the model's 150 km top are left out with the air they stand for.

## Radiation inputs and range

- RRTMG's absorption tables run from 1,053.63 hPa down (`module_ra_rrtmg_lw.F` 3845–3848). At the lunar
  sea level, 1,216 hPa, its pressure interpolation extrapolates (fp ≈ −0.72 of a table interval)
  through about the lowest 7.5 km of air. Measured offline, the table's edge moves the lowest layers' cooling by
  0.002–0.003 K a day (Terluna `domain/atmosphere` 6f7d7b0), so the extrapolation is harmless for this air.
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

1. Divide the density out of the simple boundary layer's tendencies in this repository's series, as Terluna's
   build does.
2. Rerun a reference ring with that fix and the forcing taken through the column, to size the bias the rings'
   results carry.
3. Bring the lunar rain limits, the solver's fall law and lunar self-collection into the series, and give NSSL's
   rain the same treatment.
4. Give RRTMG the shield's spectrum.
5. Two-way coupling, or nesting in the GCM, so that the slice's own state feeds back on its forcing.
6. Find and fix the source of CM1's threaded parting, first by a threaded run of stock CM1 with these boxes' options.
7. Gravity falling with height in the base state and hydrostatics for a 150 km domain.
8. Upstream: report the boundary layer's density fault, and make gravity one namelist parameter in CM1, honoured by
   every scheme.
