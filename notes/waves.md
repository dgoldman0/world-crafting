# SWAN and SWASH on a breathable Moon: correctness, limits and room for improvement

Notes on the two SWAN patches in [../models/swan/](../models/swan/), SWASH's lunar settings in
[../models/swash/](../models/swash/), the input settings and Python coupling that carry the Moon into
both, and what in them stays Earth's. References to Terluna are at commit 186b294; to SWAN, at the
41.51 archive; to SWASH, at the 12.01 archive (pins in the two READMEs).

Statements marked **Terluna** are the project's own documented claims, cited by file and line.
Statements marked **Finding** come from the review of 2026-10-17: reading the pinned sources, rereading
the committed products, and a few statistics computed from the recorded atmospheric archive. Unmarked
statements are direct observations of source code or files.

Evidence states used below:

- **integrity**: archives, sources, executables, inputs and outputs match recorded hashes;
- **reproduction**: identical inputs give identical outputs (repeat runs, hotstarts, thread counts, replays);
- **identity**: a patched build at Earth values reproduces the unpatched build's output exactly;
- **implementation**: the code computes what it states, checked against an analytic answer;
- **similarity**: a run at scaled gravity, lengths and times reproduces the original run in dimensionless
  form. This shows that the configured equations and the executable are gravity-consistent, which makes
  each lunar run the gravity-scaled image of an Earth run with the same Earth-fitted coefficients. It
  does not test those coefficients;
- **numerical convergence**: results hold under finer time steps, grids, directions, frequency bands and
  solver tolerances;
- **calibration**: none. No wave quantity was fitted to anything: SWAN and SWASH run with their shipped
  coefficients. The only cross-model checks are consistency checks (the GCM's roughness against its own
  stated law; GCM against CM1 winds);
- **physical validation**: impossible without lunar seas; nothing here claims it.

## What carries the Moon

| Element | Kind | Where |
|---|---|---|
| AGROW bend at `GRAV/9.80665` Hz | source patch 01, general repair | `swancom3.ftn:1800` |
| Air density 1.40390062332 kg/m³ | source patch 02, value substitution | `swanmain.ftn:1740` |
| `SET GRAV 1.62421887656`, `RHO 1025`; SWASH `GRAV`, `RHOWAT` | input | Terluna `nearside.py:199`; `runup.py:144` |
| `COORDINATES SPHERICAL 1737400 CCM` | input | Terluna `nearside.py:198` |
| Band 0.03–3 Hz × g/9.80665, 36 directions | input | Terluna `model.py:82–85` |
| Komen/Wu/DIA/AGROW, breaking kept on, `INIT ZERO` | input choices that avoid Earth constants and a defect | `models/swan/README.md` |
| GCM stress → Wu-equivalent wind | Python, before SWAN | Terluna `weather.py:20–42` |
| SWAN spectrum → 1-D SWASH boundary | Python, between the models | Terluna `runup.py:52–129` |
| ρ·g and √g conversions with the lunar g | Python, after the models | Terluna `shore.py:204–205`; `review_checks.py:69–78` |

## The checks and what each establishes

| Check | Where | Result | State |
|---|---|---|---|
| Archive, source and executable pins | Terluna `build.py:25–30`, `swash_build.py:16–17, 36–46`; this repository | all match (2026-10-17); patches 01–02 reproduce every deployed patched source byte for byte | integrity |
| Repeat of identical runs | Terluna `run.py:94–99` | exact for stock and patched builds with breaking on; with `OFF BREAKING` repeats differed by ~2.5% in Hs (`audit.md:70–73`) | reproduction |
| Earth output of patch 01 | Terluna `run.py:117–120` | stock and patched Earth strips identical at `GRAV 9.80665` | identity |
| Sixfold gravity similarity | Terluna `run.py:83–109` | patched: largest Hs and Tm01 differences 0.303%, 0.326%; stock 5.44%, 3.91% | similarity |
| Lunar radius | Terluna `climate/tests/test_wave_pilot.py:96` | a 2 km basin in metres and in lunar degrees agrees within 1% | implementation (degree length; curvature turning is negligible at 2 km and untested) |
| Energy flux before breaking | `test_wave_pilot.py:129` | Hs²·c_g constant within 2% on a 1:100 slope, c_g from the lunar dispersion relation | implementation |
| Stress inversion | `test_wave_weather.py:11`; `weather.py:207–216` | round trip within 3×10⁻¹⁴ in both drag regimes; SWAN's printed friction velocity equals `sqrt(Cd)·U` in every run | implementation |
| GCM roughness against Charnock at lunar g | Terluna `review_checks.py:138–149`; `review.md:22–30` | ratio 1.000000 (5th–95th percentile 0.999999–1.000001) over 203,389 open-sea samples; 6.04 at Earth's g | consistency of the GCM with its own formula, not a test of the formula |
| Energy transport | `shore_checks.py:63–86` | SWAN's `TRANSP` against the integrated spectra within 0.093% over 49 station records (`shore.md:57–59`) and 0.552% through the cycle (`coastal_history.md:186–187`) | implementation |
| Group delay | `history_controls.py:58–92` | pulse centroid delay within 0.0041 min of the analytic lunar group speed at 900 s; the half-peak front arrives 11.0, 6.59 and 3.55 min early at 900, 450 and 150 s (`coastal_history.md:177–184`) | implementation; numerical diffusion measured |
| Hotstart, threads, replays | `nearside.md:159–161`; `cycle.md:138–145`; `shore.md:105–107`; `coastal_history.md:134–137` | restarts bit for bit; 1 = 2 threads and 2 = 4 threads exactly; replays reproduce 3,103,551 and 4,076,820 values exactly; the `-O3 -march=native` build differs from `-O` by ≤0.512% Hs and ≤1.62% Tm | reproduction |
| Spectral band edges | `model.py:142–185`; `pilot_checks.py:16–50`; `cycle_checks.py:76–112` | metre-scale spectra pass; weak seas fail (below) | numerical convergence |
| SWASH controls | [../models/swash/README.md](../models/swash/README.md) | linear dispersion at three gravities ≤1.76%, ≤0.289%; linear similarity 9.1×10⁻⁶; nonlinear similarity with breaking 1.20%; irregular input 5.22%/6.28% (fails 5%) | implementation, similarity |

Reading rule: the similarity checks are the strongest statements about the adaptation. They show that
nothing on the code paths they exercise still assumes Earth's gravity (for SWAN, only after patch 01):
for SWAN, Komen input and whitecapping with Wu drag at a fixed wind, AGROW, DIA and depth breaking, on
Cartesian strips started from rest; for SWASH, the non-hydrostatic solver, the spectral wavemaker,
breaking and wetting. Spherical geometry, nesting and stationary iteration were checked separately or
not at all. The similarity checks cannot show that wind input, whitecapping or breaking calibrated on
Earth's seas apply to the Moon's.

### Numerical convergence, what passes and what does not

| Calculation | Refinement | Result | Terluna |
|---|---|---|---|
| Strip, 4 m/s, 100 km, 48 h | Δt 300→150 s, Δx 1000→500 m, 36→72 directions, wider band | endpoint within 0.3% | `first_experiments.md:40–51` |
| Strip, early growth | Δt 300→1 s | one-hour Hs 0.132 → 0.309 m; 20 min–2 h window still 12.2% in Tm between 2 and 1 s | `first_experiments.md:95–116` |
| Smythii pilot, 12 h | Δt, frequency count; 1°→0.5° grid | <0.6%; grid 41.3% Hs and 22.7% Tm locally, <0.002% offshore | `first_experiments.md:132–140` |
| Smythii weather week | Δt 150→75 s; 48→96 h history | fails 5% in small seas (12.95%, 26.73%); ≥1 m seas 0.446%, 1.760%; history passes (2.42%, 2.24%) | `weather.md:125–144` |
| Smythii cycle | Δt 150→75 s over the stormiest week | fails in small seas (16.29%, 29.37%); ≥1 m seas 0.376%, 0.870%; time above 1 m within 0.32 h; 129 of 708 spectra fail the band-edge test | `cycle.md:109–136` |
| Nearside cycle | Δt 300→150 s over the stormiest three days | ≥1 m seas within 3.6% Hs and 9.0% Tm; decimetre seas up to 86% and 145% at single nodes; time above 1 m within 2.6 h of 72; 24 of 1,888 reference spectra fail the band-edge test | `nearside.md:144–166` |
| Coastal resolution | 7.6→3.8→1.9 km; directions | grids fail (16.2%, 118%); directions pass (0.57%) | `coastal.md:68–86` |
| Shore exposure | 948→474→237→118 m and seven other controls | grids fail their maximum bounds (46.7%, 35.1%, 39.1%; 95th percentiles 6.2%, 3.6%, 2.8%); local solver accuracy fails; directions, domain, regional spacing, interpolation, regional accuracy and upper frequency pass | `shore.md:200–219` |
| Coastal history | 900→450 s in two windows; iterations | first window passes; eastern transport 13.8% at the 95th percentile fails; the nests never meet SWAN's 99% accuracy criterion at any step | `coastal_history.md:139–165` |

## Limits

### Coefficients fitted to Earth's seas

**Terluna.** Under Froude similarity the dimensionless coefficients (breaking indices, whitecapping,
four-wave interactions) transfer unchanged; three parts of the physics change with gravity: air–sea
momentum transfer, capillary waves and sediment (`README.md:117–123`; `review.md:122–128`).

**Finding.** Similarity transfers the coefficients by construction. Whether they hold depends on the
processes that do not scale with gravity:
- **Viscosity.** For the lunar friction velocities (0.07–0.35 m/s), the roughness Reynolds number
  α·u*³/(g·ν) is 0.3–36. Earth seas reach that range at 10 m winds of about 4–16 m/s.
- **Surface tension.** The capillary wavelength grows from 1.7 cm on Earth to 4.2 cm on the Moon, far
  below the band top (1.05 m), where it changes the dispersion by 0.16%.
- **Air–water density ratio.** 1.37×10⁻³ for the lunar runs, against 1.25×10⁻³ in stock SWAN.

These regimes lie inside or beside the ranges Earth's data sampled, so the transfer is plausible. It is
untested. The DIA is the best-founded term because it approximates the exact four-wave integral, a
property of the gravity-wave equations. These are fits to Earth data, used as shipped:
- Komen's input (0.25 and 28, `swancom3.ftn:2068`, `2073`);
- Komen's whitecapping (`swanmain.ftn:1602–1607`);
- AGROW (0.0015, `swanpre1.ftn:3064`);
- the depth-breaking index 0.73 (`swanmain.ftn:1665`);
- SWASH's breaking α and β;
- Wu drag;
- the GCM's Charnock constant 0.018 and its 1.5×10⁻⁵ m roughness floor (Terluna
  `shared/constants.json:50–58`). The floor is dimensional; smooth-flow roughness is physically ~0.11ν/u*.

### The forcing

**Terluna.** The GCM is T21 with its lowest level about 885 m above the sea. A 10–20% wind difference
between models becomes 20–45% in the height of a developed sea (`review.md:102–104`). Over the
equatorial seas the GCM and CM1 agree within about 20% (`review.md:32–36`).

**Finding.** The 885 m follows from the σ grid. The lowest level σ = 0.9833 sits at a height of
H·(−ln σ), and the scale height H = RT/g is 52.5 km at lunar gravity (`results/review_checks.json`,
`gcm_lowest_level`). An Earth-designed σ grid therefore puts the lowest level about six times higher on
the Moon, and the GCM's bulk surface-layer law spans 885 m. This lies under the forcing uncertainty
that Terluna ranks among its largest, and it is the least examined part of it.

### The fixed air density

**Terluna.** The build holds one representative CM1 density; spatial and temporal density effects are a
separate sensitivity (`build.py:158`; `weather.md:77–81`). The synthesis says SWAN's friction velocity
equals the GCM's (`README.md:107–108`).

**Finding.** The GCM's stress-closure density (`climate/gcm/wave_snapshots.py:194`) varies more than one
value can represent:

| Region (481 snapshots of `research/runs/waves/cycle/atmosphere.npz`) | Density range (kg/m³) |
|---|---|
| Ice-free open sea, global | 1.2214–1.4504 |
| Open-sea cells inside the nearside sea's bounding box | 1.3345–1.4364 |
| Smythii–Marginis wet nodes, recorded by Terluna (`results/cycle.json`) | 1.3824–1.4095 |

With ρ_SWAN fixed at 1.4039:
- SWAN's friction velocity √(τ/ρ_SWAN) differs from the GCM's by −2.5% to +1.2% over the nearside sea,
  and by −6.7% at the global minimum;
- Komen's density ratio is off by −2.3% to +5.2%;
- where 28u*/c ≫ 1 the input rate ∝ ε·u* ∝ √(ρ_SWAN·τ), so the net error is −1.1% to +2.6%.

The equality in the README holds to this accuracy. A run for another sea should check its own range.

### A density correction described but not applied

**Terluna.** `shore.md:174–175` ("its fixed-density SWAN build and spatial density correction"),
`shore_checks.py:284` ("spatial surface-density wind correction") and `shore_region.py:110` ("Local
winds retain the atmospheric surface-density correction").

**Finding.** The code applies no such correction:
- `weather.py:102` interpolates the GCM density only for the forcing record's statistics
  (`weather.py:159–160`);
- the inversion uses the fixed build density (`weather.py:127`; `nearside.py:179`, `244`).

The fixed-density part of those sentences is right; the spatial correction does not exist.

### The AGROW bend switches on damping inside the lunar band

**Terluna.** The patch restores dimensional similarity and changes the main lunar endpoints by at most
0.11%; it also changes early lunar heights; it is a numerical choice, not lunar validation
(`first_experiments.md:36–38`, `51–54`, `84–87`; `build.py:79–80`; `audit.md:54–60`).

**Finding.** At lunar gravity the stock 1 Hz bend lies above the band (top 0.497 Hz) and never acts. The
patch applies f⁻³ damping from 0.166 Hz upward, over the top 11.5 of 48 intervals and by up to 27 times
at the band top. One-hour heights at 100 km fall by 51%, 26% and 13% at the three strip winds (0.073 →
0.036, 0.179 → 0.132, 0.306 → 0.266 m; `results/waves.json`).

The patched model matches Earth SWAN in dimensionless terms. Neither version says how wind starts waves
on the Moon, and the bend itself is arbitrary upstream (`swancom3.ftn:1722–1725`). In the GCM-forced
runs the spin-up cycle is discarded, so the bend matters where new wind meets calm or nearly calm
water. Its effect on the reported statistics is unmeasured: no forced run used the stock build.

### Runs on the Wu path

**Terluna.** At lunar gravity Charnock's law gives drag 0.85, 1.11 and 1.34 times Wu's at the strip's
three winds, so the strip's lunar heights are 8–15% high, 5–11% low and 16–34% low (`review.md:107–113`).
"Wu's Earth calibration therefore enters only the first strip experiment" (`review.md:29–30`).

**Finding.** That sentence is wrong. These runs also drive SWAN with CM1's 10 m winds through Wu:
- the basin pilot (`pilot.py:144–146`, `157–160`);
- the coastal-resolution episode (`coastal.py:65–66`);
- the early-growth runs (`early_growth.py:43`, which also keep 1.28 kg/m³).

Their quoted numbers carry the 4 m/s bias, roughly 5–11% low in Hs: the pilot's 1.222 m basin maximum
and slope-breaking table (`first_experiments.md:118–157`) and the coastal spur values
(`coastal.md:62–92`).

The synthesis headline, waves "4–5 times as high as on Earth" under the same wind
(`README.md:14–19`), uses Wu at both gravities. With Charnock's law at each gravity, lunar drag exceeds
Earth's by 1.23, 1.45 and 1.51 times at the three winds (`results/review_checks.json`,
`drag_against_wu`). That raises the lunar/Earth height ratio by about 11–23% for fetch-limited seas and
23–51% for developed seas (heights grow between the first and second power of u*, `review.md:109–111`),
on the condition that Charnock's constant does not depend on gravity.

### Water density 1025 against the fresh-sea decision

**Terluna.** `shared/scenarios/waves.json:4` sets 1,025 kg/m³ seawater "for this calculation family";
the seas' composition is undecided and changes the waves by 2.5% (`review.md:150–153`;
`README.md:170`).

**Finding.** The author directed fresh seas on 2026-10-13 ("hard fresh water near 0.14 g/kg",
`research/decisions.md:352`) and on 2026-10-15 ("The seas stay fresh or near fresh", `:385`), after the
wave runs of 2–4 October. Pure water at the GCM's mean sea-surface temperature, 296 K
(`results/review_checks.json`), is 997.6 kg/m³ (Tanaka et al. 2001); 0.14 g/kg adds about 0.1. That
raises SWAN's air–water ratio by 2.7% and lowers every ρg power conversion by 2.7%. The scenario and
`README.md:170` are out of date. In SWASH the density cancels.

### Swell decay

**Terluna.** Swell carries 34–64% of the energy at the nearside reference points (`nearside.md:63–69`).

**Finding.** Komen's input is zero for components faster than 28u*·cosθ and never negative
(`swancom3.ftn:2083–2084`). Komen's whitecapping removes swell only in proportion to the mean steepness
of the whole spectrum (`swancom2.ftn:2485–2491`, `2611–2615`). Later source-term packages add
dissipation of swell by air–sea friction. Long-period lunar swell crossing thousands of kilometres may
therefore decay too slowly here; by how much is unknown.

### Early growth depends on the time step

**Terluna.** The one-hour height depends on the step (0.132 m at 300 s, 0.309 m at 1 s); the first
minutes need still smaller steps (`first_experiments.md:95–116`; `audit.md:120–126`).

**Finding.** This is consistent with SWAN's default action limiter (`PHILIM`, `swancom1.ftn:7980`). It
caps the change per time step, not per second, so longer steps slow early growth. The sensitivity
matters for gust response and for the onset of events from calm water. Late, metre-scale results
converge (`cycle.md:109–113`).

### The 1° basin grid

**Terluna.** Refining the pilot basin from 1° to 0.5° changed local heights by up to 41.3% and the
offshore node by less than 0.002% (`first_experiments.md:132–140`; `review.md:99–101`). The cycle,
nearside and coastal histories use 1°. Coastal power at 1° nodes measures sea-scale exposure of 30 km
of coast (`nearside.md:92–96`).

### One lunar cycle

**Terluna.** One measured cycle, after one cycle of spin-up, supplies each sea's statistics
(`README.md:147–148`; `review.md:105–106`). Further cycles cost seconds of GCM time per month and about
3.3 hours of SWAN per two nearside cycles (`README.md:160–161`). No variability between months is
measured.

### Further limits recorded by Terluna

- **Weak seas.** Seas under about 0.75 m put more than 1% of their variance in the top two intervals in
  37% of coastal spectra (`README.md:144–146`).
- **Evolving nests.** They run one iteration per step and never meet SWAN's 99% accuracy criterion;
  boundary warnings are frequent (`coastal_history.md:158–175`).
- **SWASH.** The irregular-input control fails its 5% bounds; the eastern 4→6-layer sensitivity is 6.75%;
  one phase realisation per case; 30-minute windows (`runup.md:48–60`, `169–175`, `219–232`).
- **Water level.** It is fixed in the coastal and run-up runs, while the monthly tide ranges 0.55–7.7 m
  (`README.md:64–73`, `163–164`).
- **Shore material.** Regolith shores, sediment and porous beds are not modelled (`README.md:83–86`).
- **Coupling.** One-way throughout: no wave-dependent roughness, no wave–current or wave–level
  feedback (`weather.md:72–75`).

**Finding.** The wave runs are forced by the climate `A28_dim5_moon` (`README.md:9–10`), near 295 K.
Since the GCM corrections of 2026-10-17, the design sunlight takes the Moon near 307 K, and the author
is weighing a warmer Moon (`research/decisions.md:67`; the paper's ideation treats 307 K as a
sensitivity). The wave statistics are conditional on the forcing climate. At the same pressure, the
representative air density would be about 3.6% lower at 307 K.

### Constants that are inactive but would act if the features were switched on

- **SWAN:**
  - `INIT DEFAULT`'s 2 s period, 0.05 m and 0.02 m (`swanmain.ftn:9410`, `9417`);
  - default gravity and radius (`:1267`, `:1449`);
  - ST6 drag routines with `G`, `RHOW` and `RHOA` (`SdsBabanin.ftn90:2305`, `2466`, `2470`, `2471`);
  - XNL's `g=9.81` (`mod_xnl4v5.ftn90:8540`, `8563`);
  - JONSWAP bottom friction 0.038 m²/s³ (`swanmain.ftn:1658`). It is dimensional, with the scaling of
    C_f·g·u_orb, so used unscaled it would overstate lunar bottom friction about six times.
- **SWASH:**
  - Earth's rotation, hard-coded (`SwashCheckPrep.ftn90:3243`);
  - default radius and air density (`SwashInit.ftn90:160`, `137`).

Details are in the two READMEs.

### Builds

**Finding.** The strip ran on executables (stock `b22dc0e6…`, patched `0a32101d…`) other than those of
the later builds of identical sources with identical commands (`683cc283…`, `a7d809de…`). The cause is
not recorded. Rebuilding from these patches reproduces the sources exactly, not necessarily the
executable bytes. Output differences of the size measured between optimisation levels (≤0.5% in Hs,
≤1.6% in Tm, `cycle.md:138–143`) are the expected scale. `-march=native` ties the production executable
to its processor.

## Room for improvement, ordered by value

Value here is the uncertainty in the reported lunar wave results removed per unit of effort.
Corrections to the record come first because they cost nothing.

1. **Correct the record.**
   - `review.md:29–30`: the Wu path also covers the pilot, coastal-resolution and early-growth runs.
   - `shore.md:174–175`, `shore_checks.py:284`, `shore_region.py:110`: there is no spatial density
     correction.
   - `README.md:107–108`: the friction velocity matches only to −2.5…+1.2% over the nearside sea.
   - `shared/scenarios/waves.json` and `README.md:170`: fresh water.
   - Add the in-band AGROW effect to the patch's description.
2. **Bound the forcing.** Rerun one stormy week with u* scaled by ±10% and ±20%: hours of computing,
   and a direct measure of the largest quantified sensitivity. Compare GCM and CM1 surface stress at
   matched sea points. Test the GCM with a lower first level, since the σ grid puts it at 885 m.
3. **Bracket the Earth-fitted source terms.** Nothing tests them yet.
   - Run Janssen (`GEN3 JANSSEN`) with an inversion consistent with its stress solve
     (`swancom3.ftn:2561–2569`), or with a physically diagnosed 10 m wind such as Terluna's
     Charnock-neutral wind (`review_checks.py:63–66`).
   - Run ST6 after patching its drag routines' `G`, `RHOW` and `RHOA` to `GRAV`, `PWIND(17)` and
     `PWIND(16)`. ST6 also brings swell dissipation, which addresses the swell-decay limit.
   - Use exact XNL (patch `xc_hh`'s `g`) as a reference for the DIA on a few saved spectra.
   - The spread between packages is the first estimate of the physics uncertainty.
4. **A 0.5° basin parent** for Smythii–Marginis's cycle and the coastal histories: the largest measured
   numerical sensitivity (41% locally).
5. **Further lunar cycles.** Cheap in the atmosphere, and the only route to variability between months.
6. **A wider frequency band** for weak seas: the band-edge failures concentrate below 0.75 m.
7. **Density.** Switch the scenario to fresh water. Either feed the inversion the GCM's local density
   (giving the GCM's u* exactly, with ε still fixed) or patch SWAN to read an air-density field. Worth
   about −1…+3% in input rate over the nearside sea, more for seas whose air is lighter.
8. **Turn both patches into run-time switches with stock defaults**: a `SET` keyword for air density in
   the `SET` parser (`swanpre1.ftn:2173–2185`), and an AGROW bend option (1 Hz, scaled with g, or a
   multiple of FPM). Identity regressions and bend sensitivities would then need no rebuild, and the
   patches would match the paper's definition of a general repair: a parameter whose default reproduces
   the original. In this repository, a short sixfold similarity run and an Earth identity run would make
   cheap regression checks (minutes on one thread).
9. **Coastal convergence**: 118 m maxima still change by 39%. Also iterations per step in the evolving
   nests, SWASH's irregular-input reconstruction (5–6%), and more phase realisations for extremes.
10. **Size the AGROW bend's effect on statistics** with one forced week on the stock build, and converge
    early growth in Δt where gust response matters.
11. **Water level and shore material.** The monthly tide in the coastal and run-up runs; porous regolith
    and sediment on the profiles; a 2-D wave-resolving patch for oblique waves.
12. **Latent constants**, when their features are used: scale JONSWAP friction with g (or use Madsen's
    roughness formulation); patch SWASH's rotation rate for 2-D spherical runs with Coriolis.

## Python wave tools that stay in Terluna

The wave package (`climate/waves/`) is one tightly coupled set of run scripts: its runners import `build.py`,
which downloads and patches SWAN, so a subset cannot be brought without it, and the inserting helpers stay in
Terluna by the repository's rule. Its numerical pieces worth a port, with what they need (from the review of
2026-10-17):

| Tool | Where (Terluna 186b294) | Needs | Portable as |
|---|---|---|---|
| Stress-to-Wu-equivalent-wind inversion | `weather.py` 20–42 (`drag_coefficient`, `stress_equivalent_wind`) | numpy; the four Wu coefficients | functions |
| Ocean-only bilinear remap and the 0° seam | `weather.py` 45–86; `nearside.py` 128–135 | numpy | functions |
| SWAN to SWASH spectral reduction (normal incidence, conserving shoreward energy flux) | `runup.py` 40–129 | numpy, scipy; Terluna's run manifests and profiles | after splitting the maths from the file handling |
| Group velocity and directional energy flux | `shore_checks.py` 44–86 | numpy | functions |
| SWAN 2-D spectrum reader and boundary writer | `coastal_checks.py` 16–114; `shore.py` 37–54 | numpy | functions (spherical files only) |
| Verification harnesses: SWAN sixfold similarity, SWASH linear and 4×-gravity controls, reflection, nonlinear similarity, group-delay pulse | `run.py` 83–109 with `model.py` 35–259; `runup.py` 132–217; `runup_controls.py` 18–41, 107–143; `history_controls.py` | numpy, scipy, an executable path; a fixed wind in place of the CM1 ring file | after substituting a fixed wind and a reference case |

A port would gather these into a small package with its own tests, keeping the similarity harnesses as the
regression suite for any change to the patched SWAN or to SWASH's settings.
