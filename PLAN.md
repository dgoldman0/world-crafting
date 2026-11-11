# Plan

This plan orders the work across the repository's lines: the models' patches and tools, the lab (`lab/`, on the
branch `lab`) and the paper (`paper/`, on `paper/conclusion-development`). It is kept on main and brought up to date
in each integration round ([integration/](integration/)). Each line keeps its detailed plan with it: the lab's stages
in [lab/design/plan.md](lab/design/plan.md), the paper's drafts and readings in `paper/review/`.

## The work in hand: the ensemble brought to the Open Moon's later findings

The Open Moon's work in Terluna up to 8 November 2026 (Terluna `main` at `bdda5a07`) established two things about
the models.

**The Moon's turn.** Seas and lakes load the Moon unevenly: 0.02% of its mass, with products of inertia 13% of
C − A. Since angular momentum holds the spin axis fixed in space, the body turns beneath it until its axis of
greatest moment lies along the spin and, under the tidal lock, its axis of least moment points to Earth. Within
years the pole moves 8.05° toward 167° W, the point beneath Earth moves to 8.0° N, 6.1° E, and the spin axis's
tilt rises from 1.54° to 1.61°: an offline calculation, reproduced independently (Terluna
`research/studies/moon_orientation/`). The order in which the basins fill sets the path. Over geological time the
mantle's response eases the turn, to 6.6° at 10 million years in the central case of the present thermal state. A
shallow mantle as warm as the warmest published profile would bring it to 1.9° within about a thousand years, and
the measured heat flow favours the cooler profiles (Terluna `geology/`, `45c3d817`). At the same sunlight the turned Moon's climate runs
0.8 K warmer, its global rain and dry-land share unchanged while the near side's north grows wetter and the
southern highlands drier (model runs). Terluna's runner checks a turned surface's record when a run is started with
`--frame`; a run started without it takes today's orientation with no warning.

**The GCM–CM1 comparison.** Terluna's GCM runs on fifteen σ levels with simplified Betts–Miller convection,
Beljaars's gust with similarity theory over ice-free water, and rain evaporated from drop sizes at lunar fall
speeds. CM1's builds take the density fix of the simple boundary layer, the gust over water at lunar gravity and
the lunar raindrop limits, and CM1's boxes take the GCM's forcing through the whole column. On the design years the
boxes rain 82–84% of the GCM's rain at three sites. Three differences remain: at sea, 22–41% of CM1's rain falls in
another quarter of the lunar day; CM1's air at 40–60 km runs 3.5–10 K colder than the GCM's; and no refinement of
the GCM's convection has passed Terluna's agreement test, so every one stays off. Every CM1 run behind the paper's
first version used CM1's gust over water, a formula with no gravity in it, which made the sea box's surface wind
1.6–1.8 times stronger. The design climate is the turned Moon at sunlight 0.924
(`A28R_301k_design_l15_snow_s924_turned_refit`): 301.33 K over years 10–19, and 301.20 K with 1.97 mm/day of rain
over years 10–49.

**Since 8 November.** Terluna corrected its design climate and handed over the gap (Terluna `main` at `59dcda1c`,
`domain/climate` at `39c5ee04`). With the night's twilight counted once and the equinox regressing with the orbit's
node, its design case holds the target at sunlight 0.938: 301.0 K and 1.95 mm/day of rain over years 10–49
(`A28R_301k_design_l15_snow_s938_turned_refit_precession`). Boxes forced with the GCM's ascent rain 75–84% of its
rain, boxes that make their own ascent rain more than the GCM at the sea and at 0° E, and no closure has passed.
Terluna carries the difference as a range in its own studies and, on 9 November, moved the work of closing it to
this project. A pass over the models here on 9 November, with Terluna's records of 10 November, added a fault in
ExoPlaSim's output and five open entries to the defect log on the lab's branch (A10, B36–B39, C22).

## Decisions

- The paper and the lab study the Open Moon on the turned Moon.
- The physics the comparison confirmed as corrections enters this repository's patches and tools, and the lab and
  the paper take it together. Physics still under test enters as options, each at its released model's default.
- Each fix is recorded as general or as the Moon's, with the range within which it holds (the table below), in the
  defect log, the lab's registry and the paper's repairs.
- Terluna's methods enter the lab generalised: its tools take any world's figure, loads and gravity.
- The lab validates configurations, the orientation included. It derives a world's orientation from its surface
  loads whenever they change, and it warns or refuses when a run's orientation departs from the derived one.
- CM1's gust over water is an Earth value: an empirical formula, right at Earth's gravity, in a surface layer that
  scales its gust with gravity over land. It joins the inventory of Earth values with its repair. The released
  codes' defects number six: the first version's four, the simple boundary layer's density fault (A9) and the
  humidity held in ExoPlaSim's mean output (A10, counted on 11 November 2026).
- The paper's version 2 states the current understanding throughout and adds one section, just before the
  Conclusion, that summarises for its readers what changed in the paper from the first version (corrected on
  11 November 2026 from a section on how the models were refined). It is developed on the paper's branch and
  released once the CM1 results are realigned (below); the tag `paper-v1` keeps the first version.
- Components run when a study calls for them. Each fix enters with its released model's behaviour as its default;
  before anything runs, `lab plan` reports a task's estimated cost and the results of its checks, and compute runs
  once the user starts it and the checks clear.
- A fix serves every world as one component when the Earth control stays within 2σ of the released model's yearly
  means with it on; otherwise it becomes a switch that stays off for Earth.
- The Earth control takes the fixes together. If it leaves the 2σ range, they are added back singly, in the order
  its evaluation indicates (11 November 2026).
- Level sets are generated for each world from its scale height, and a world whose scale height is near Earth's
  keeps ten levels.
- CM1 boxes that carry the GCM's weather are an option for the studies that need them.
- The unified interface, in which a user describes a world, chooses its components, sees their cost and checks and
  starts the compute, gets its own design step before any user-facing work.
- The lab's design temperature for the Open Moon is 301 K, Terluna's, so that results found here, a closure of the
  gap among them, can be carried back to Terluna's studies (11 November 2026).
- The work of closing the gap between the GCM and CM1 is this project's. Terluna carries the gap as a range in its
  own studies and runs no further work toward closure (Terluna's decision of 9 November 2026).
- MITgcm stays out of the lab for now (9 November 2026). `lab/design/gap_series.md` keeps the assessment, which
  places it later, as the lab's ocean.
- The lab's work runs in the five blocks of "The sequence", in that order (11 November 2026).
- The machinery of the lab's stages 3 to 7 is built as a thin path first, the least of each stage that runs one GCM
  run and one CM1 box under the lab's own bookkeeping, and widened afterwards (11 November 2026).
- The waterworld twin of the gap's series takes the Moon's 29.5-day solar day and the Open Moon's air at 1.2 atm
  (11 November 2026).
- Sunlight taken at the Earth–Moon barycentre's distance is an idealisation of the scenario as run, stated in its
  set-up, and stays outside the count of defects. The lab offers the Moon's monthly swing in sunlight as an option
  that a study switches on or off (11 November 2026).

## Each fix: general or the Moon's

| Fix | Code | Kind | Holds within | State | Source in Terluna |
|---|---|---|---|---|---|
| Tendencies of the simple boundary layer (`ipbl = 2`) passed per unit mass, without the density weighting | CM1 | General: a coding defect, up to about 20% at Earth's air densities | Every run with `ipbl = 2` | Corrected | `domain/climate` 13e7123; checked in cm1r22.0, `lab` 0a2496f |
| Radiative tendencies read at constant volume under `eqtset = 2`: × cvm/cp beside another radiation code, × cv/cp in a heat budget | Readers of CM1's output | General | Every run with `eqtset = 2` | Corrected | `domain/atmosphere` fe49ad9 |
| The convective gust over water at the run's gravity, in Beljaars's form, which CM1 already uses over land | CM1 | General | Convective surface layers where similarity theory holds | Corrected | `research/decisions.md` lines 560–561; `climate/crm/cm1_run.py` |
| Beljaars's gust with similarity theory over ice-free water, replacing the Earth free-convection term and the least wind of 1 m/s | PlaSim | General | As above | Corrected | `climate/gcm/surface_gust.py`, `surface_similarity.py` |
| Morrison's raindrop limits scaled by gravity: the breakup lengths and the mean-diameter cap by (9.81/g)^½, the fall-speed cap by (g/9.81)^¼, with a density-ratio refinement | CM1 | General in gravity and air density | Liquid drops in air of Earth-like composition; the refinement within the range of Straub et al. (2010) | Corrected | `domain/atmosphere` dd89cef, 8b55847, 21529d2 |
| Rain evaporated from drop sizes at the world's fall speeds, replacing PlaSim's Earth constant γ | PlaSim | General | Air of Earth-like composition, under the scheme's drop-size distribution | Corrected | `climate/gcm/rain_drops.py` |
| CM1 forced by the GCM through the whole column, its air held to the GCM's only above the GCM's convection | CM1's set-up | General | A GCM whose convection top is known | Corrected | `climate/crm/gcm_site.py`; the lab's stage 3 |
| Fifteen σ levels, the lowest near 0.3 km | PlaSim | The Moon's level set; for another world, levels placed to resolve its boundary layer in its own scale height | — | Option | `climate/gcm/exoplasim_run.py`, `--levels l15` |
| Simplified Betts–Miller convection at 0.7 with a 200 hPa depth test, and its closures | PlaSim | Under test; the depth test, set in pressure, needs scaling to a world's pressure | — | Under test: Terluna's design runs use the scheme, and no closure has passed | the `SBM_*` edits in `climate/gcm/exoplasim_run.py` |
| Snow sublimed from McSnow's capped flakes | PlaSim | To be assessed | — | Under assessment | `climate/gcm/snow_sublimation.py` |
| The cold cloud's factors and the longwave refit `l15_turned` | PlaSim | The Moon's calibrations | The states they were fitted on, the orientation included | Calibration | `research/decisions.md` line 741 |
| RRTMG's tables past 1,053.63 hPa | CM1 | General | Computed to the Open Moon's 1.2 atm, where the extrapolation moves the lowest layers' cooling by 0.002–0.003 K/day | Computed offline | `domain/atmosphere` 6f7d7b0 |
| Reorientation by surface loads | The set-up of any GCM run | General | Degree-2 loads small beside the body's figure; the elastic turn within years; the long-term turn given an interior model | Computed offline, reproduced independently | `geology/orientation.py`, `climate/gcm/turned.py`, `climate/gcm/carry.py` |

## Porting: confidence, form and cost

Each fix enters the lab opt-in, as the decisions above set out, in the form below.
[lab/design/terluna_fixes.md](lab/design/terluna_fixes.md) holds the analysis behind the table, with its derivations.

| Fix | Confidence | Form in the lab | Cost of a run | Waits on |
|---|---|---|---|---|
| CM1's radiative tendencies read at constant volume | High: CM1's code; read so, CM1 comes within 0.01 K/day of RRTMG run offline and within 0.013 K/day of the correlated-k model | One rule for every reader, keyed on `eqtset` | ×1 | — |
| CM1's density fault under `ipbl = 2` | High: the fault in the lab's own CM1 source; the boxes' boundary layer took 1.32–1.35 times the surface's evaporation and 1.46–1.51 times its sensible heat | One patch, which the registry's A9 requires in every run with `ipbl = 2` | ×1 | — |
| CM1's gust over water at the run's gravity | High: CM1's own form over land; the old formula made the sea box's wind 1.6–1.8 times stronger | One component, for convective surface layers | ×1 | The Earth control's test |
| PlaSim's gust with similarity theory over water | High on the physics; over one lunar day it raised the sea's evaporation 17% and the rain 5% | One component, its air's viscosity derived for each world and its 2.85 mm roughness cap stated as Earth's; it ports with the depth rule it shares with the nonlocal scheme | ×1, with a calculation in each column | The Earth control's test |
| CM1's raindrop limits | High on the scaling, medium on its factors | One component, with a warning below 1.62 m/s², under the gravities its density refinement was computed for | ×1 | — |
| CM1 forced through the whole column | High that the hold from 8–16 km was wrong | One method; a case whose damping layer begins below the GCM's convection top plus one layer is refused (proposed) | ×1; forcing runs up to ×1.3 | The choice among the box forcings, below |
| Reorientation by surface loads | High within years, medium over geological time | One tool, rebuilt from the Moon's constants with branches for the rotation state, the source of the moments and the interior's response; the long-term branch assessed first | Offline minutes; one or two extra GCM passes for a world with land | — |
| PlaSim's rain evaporated from drop sizes | Medium | One scheme with tables for each world; its starting drop sizes a calibration fitted on the Moon's CM1 boxes, with γ outside that calibration's envelope | ×1; the calibration takes CM1 boxes of 2–27 hours each | The Earth control's test |
| Level sets | Medium | Generated for each world from its scale height, the calibrations keyed to the set | ×1.5–2.25 at fifteen levels, ×3–9 at thirty | The Earth control's test |
| PlaSim's clear-share twilight | Medium: one paired run, about 1 K of cooling | One component, its ledger computed for each world | ×1; the ledger about 50 minutes on six threads | — |
| PlaSim's 10 m wind | High: a diagnostic | One output | ×1 | — |
| Simplified Betts–Miller convection | Low to medium | A setting with Kuo's scheme its default; the depth test a fraction of the surface pressure | ×1 | The gap's work here (block 4) |
| The box forcings: converging inflow, carried weather and the box's own ascent | Low to medium | Case variants; carried weather an option for the studies that need it | Carried weather ×3.5–7 a box, up to about 380 GB for a large one; the ascent ×2 | The gap's work here (block 4) |
| The cold cloud's factors and the longwave refit | Medium, for Terluna's climate | The Moon's calibrations; stage 5 fits the lab's own | A refit of about three hours | The gap's work here (block 4) |
| Snow sublimed from capped flakes | Low: unassessed | Assessed before any port | — | Its assessment |

The type of world sets CM1's cost more than any fix. Under rule 9 of `lab/design/world_spec.md` CM1's grid follows
the scale height, so per simulated second a box costs in proportion to gravity and a ring to the radius times the
square of gravity: a ring on Earth costs about 130 times the Moon's, and the Moon's solar day, 29.5 times Earth's,
offsets most of that over a day and night. Columns of 3 or 2 km in place of 6 would cost 8 or 27 times as much.

## The sequence

The lab's work runs in five blocks, each resting on the one before: the ports, the machinery that runs the models,
the first simulations, the gap between the GCM and CM1, and the flagship waterworlds. The paper's version 2 moves
beside them and takes its CM1 results from the third. Each change is small and tested and gets one review
(AGENTS.md, "Software work"), each patch keeps an identity default, and compute runs at the author's word, once a
task's cost and checks are reported.

**State on 11 November 2026.** The records took the findings of 8 November. Three CM1 fixes are in the lab's series:
the density fault, the gust over water and the reading of the radiative output (`lab` f99b7e6). Version 2 is drafted
on the paper's branch. The lab's stages 1 and 2 have passed, and stage 9 is under way.

### 1. The ports

Terluna's code for the corrected physics enters `models/` as patches at the next numbers of each series, and
`python/` at Terluna's package paths, in the order of "Porting: confidence, form and cost"; the entries logged since
that table was made follow in the same lists. Each README states its fix's kind and limits. The block is code and
tests, and its compute is the tests' short runs.

| Order | ExoPlaSim (`models/exoplasim`, patch 12 on) | Waits on | State |
|---|---|---|---|
| 1 | Beljaars's gust with similarity theory over ice-free water | — | Under way |
| 2 | Rain evaporated from drop sizes, its fall-law tables computed for each world (`python/climate/gcm/rain_drops.py`) | — | To start |
| 3 | Level sets generated from a world's scale height, with the restart's remap (the input writer; `python/climate/gcm/levels.py`) | — | To start |
| 4 | The clear share of the twilight, and the night's twilight counted once in patch 07 (defect log C21) | — | To start |
| 5 | The 10 m wind | — | To start |
| 6 | Simplified Betts–Miller convection as an option beside Kuo's scheme, its depth test a fraction of the surface pressure and its relaxation time a setting scaled with the world (B39) | — | To start |
| 7 | The equinox's regression, its count carried through restarts and branches | — | To start |
| 8 | The cold cloud's factors as namelist values with identity defaults | — | To start |
| 9 | The humidity held in the output (A10): the reader's rule in `python/climate/gcm/year_files.py` first, then the true mean as a further output, Terluna's switch `nhusmean` (`domain/climate` b93a046e) | — | To start |
| 10 | The Sun's distance through a moon's month (C22), an option that a study switches on or off | — | To start |
| 11 | Snow sublimed from capped flakes | Its assessment | Waiting |

| Order | CM1 (`models/cm1`, series-lab 03 on) | Waits on | State |
|---|---|---|---|
| 1 | The raindrop limits, with the fall law and self-collection at the world's gravity | — | Next |
| 2 | Factors on autoconversion and accretion (B38) | — | To start |
| 3 | Gravity, CO2 and O2 read from the namelist, with the soil's layers and the Sun's declination, so that one build serves every world (planned in the lab's stage 3) | — | To start |
| 4 | The whole-column forcing with the wind by local time and the inflow, and the extraction that writes it (`python/climate/crm/gcm_site.py`), which reads the GCM's humidity by the rule of A10 | — | To start |
| 5 | The damped gravity wave, by which a box makes its own ascent | — | To start, for block 4 |
| 6 | The sea's temperature by local time (B37) | — | To start |

The slab sea's depth and the diffusion's damping times are namelist values of the released model, so they need no
patch: `lab/configs/` gains them as settings by world, with the registry's entries (B36, B37).

Acceptance: each patch at its default reproduces the build without it byte for byte, a test pins its effect,
`models/check_patches.sh` covers the new patches, and `make check` passes.

### 2. The machinery

The lab can describe a world and write ExoPlaSim's inputs (stages 1 and 2 of `lab/design/plan.md`). Stages 3 to 7
build the rest, and they are built as a thin path first: the least of each stage that runs one GCM run and one CM1
box under the lab's own bookkeeping, widened afterwards to the stage's full acceptance check.

| Piece | Thin path | Widened afterwards |
|---|---|---|
| CM1 builds and cases (stage 3) | Build keys; one build of the core and lab series, with its identity and timing checks on one-day segments; the case writer for a site box and the extraction from a GCM run | Rings, terrain and electrified builds; every case of the study |
| Jobs (stage 7) | A wrapper that runs one job within the machine's budget, records its producer, its inputs and the values it read, and resumes | The runner's service and queue |
| Keys and the planner (stage 4) | A key and header on every product; `lab plan` listing a study's tasks with their estimated cost and their checks' results | Staleness across the stage graph |
| The registry (stage 6) | The entries the first runs meet, each with its check before a run: A9, A10, B28, B35–B39 and C22 | Every entry of classes (a) and (b); the reach report |
| Calibrations (stage 5) | The released model's values for Earth; for the Moon, the ledger, the gas bands and the shortwave and longwave fits of a first pass | Every producer with its envelope; the cold cloud and rain's sizes |
| The orientation check | The tools below, generalised, and the turned Moon derived by the lab's own tool | Tracking in the stage graph; the lakes' loop |

Acceptance of the thin path: from the lab's commands, one year of the Earth control and one day of a CM1 box run
with their records, and a run that fails a registry check is refused. The block's compute is small: one-day CM1
segments of about five minutes each, three for each build timed, and the ledger's fifty minutes. The unified
interface gets its design step once the thin path runs.

**The orientation check.** Stage 2 derives a world's orientation, and stage 4 tracks it.

- `geology/orientation.py`, `climate/gcm/turned.py` and `climate/gcm/carry.py` enter `python/` and extend to any
  body: moments measured or hydrostatic, rotation free or locked, every surface load with its self-gravity and
  elastic response, the principal axes, the Cassini obliquity of a locked body, the surface's remap and the
  restart's carry.
- A world states the age of its water. Young water takes the elastic turn within years, which needs only the loads,
  the body's figure and its stiffness. Old water takes the long-term turn, which also needs an interior model; a
  world with old water and no interior model gets a warning, and its runs record which turn they used.
- The orientation's record enters every run's key, so a change of seas or lakes makes the runs on the earlier
  orientation stale. A run whose orientation departs from the derived one gets a warning once the pole's shift
  exceeds a tenth of the GCM's grid spacing, and a refusal past half of it: 0.6° and 2.8° on the T21 grid. The
  tilt's change is judged by its effect on the sunlight at the poles. An explicit override runs such a case with the
  warning recorded, as outside a calibration's envelope (`lab/design/architecture.md`).
- "Lakes from runoff" re-derives the orientation at each pass, until the lakes and the orientation settle.
- The longwave refit's envelope includes the orientation.
- `lab/design/world_spec.md` names the rotation state "orientation"; "frame" keeps its meaning for the heights'
  coordinates.

Acceptance: from Terluna's loads (`geology` `45c3d817`), the port reproduces the pole's move of 8.05° toward
167° W, the point beneath Earth at 8.0° N, 6.1° E, and the tilt of 1.61°, within a tolerance the stage sets
(0.01° in each angle and 0.5% in the products of inertia, proposed). Terluna's turns of 8.4° and 8.1° come from
different loads, the seas alone and the seas with the lakes, and test each load separately. Earth with its measured
moments shows no turn, and Mars with an illustrative sea has its turn computed and reported.

**The lab's documents and settings.** `lab/design/plan.md` takes stages 2, 3, 4, 5, 6 and 8 and the section
"The GCM's convection, boundary layer and levels", which names simplified Betts–Miller as the scheme of Terluna's
design runs. `lab/configs/` gains each new setting at its released model's default; `lab/studies/open-moon.toml`
takes the turned Moon and the whole-column forcing; `lab/registry/` takes the states of B29–B34, CM1's gust and the
orientation check. The Open Moon's scenario and CM1's reference state take the design temperature of 301 K in place
of 295 K (`lab/worlds/moon/scenarios/open-moon.toml`, `lab/configs/cm1/defaults.toml`).

### 3. The first simulations

The Earth control comes first, since a fix serves every world only once Earth has passed with it on. The Moon
follows, and its settled design run forces the CM1 cases that the paper's realignment waits on (stage 8 of
`lab/design/plan.md`).

| Order | Runs | Rough cost | Decides or gives |
|---|---|---|---|
| 1 | The Earth control with the released model: two runs of 20 years | 75 minutes each | Whether the lab's pipeline reproduces the released run |
| 2 | The Earth control with the fixes that change Earth's physics switched on together; if it leaves the range, the fixes added back singly, in the order its evaluation indicates | One 20-year run of about 75 minutes on Earth's ten levels; further runs only if it leaves the range | Whether the fixes serve every world as one component, within 2σ of the released model's yearly means, and otherwise which of them stays off for Earth |
| 3 | The Open Moon's design run at identity calibrations, then the fixpoint's passes, each refitting the calibrations on the lab's own run | About three hours a pass for 20 years on fifteen levels, and the fits beside it; three or four passes | The lab's own design climate, its lakes and orientation settled |
| 4 | CM1's cases forced from the settled design run: the three site boxes, the 45° N ring and the raindrop sensitivity | A box of two lunar days about two hours on four threads; a ring about 4.5 hours on six | The paper's realignment: the ring for Figure `fig_gap`, and the comparison near the ground |

Together the block is of the order of fifty machine hours, an estimate from Terluna's timings.

### 4. The gap

The work of closing the gap is this project's. It opens with four runs that size the entries of the pass of
9 November (B36–B39), the mixed layer and the warm rain first, and goes on to the series of
`lab/design/gap_series.md`, which sets Earth and an all-ocean twin of the Moon beside the Moon. A change to either
model enters only on evidence apart from the comparison, as the agreement test requires.

| Order | Step | Rough cost | Decides |
|---|---|---|---|
| 1 | The slab sea at 15 m | One GCM run of 10–20 years, 1.5–3 hours | The size of the sea's swing through the lunar day, and its share of the rain's timing |
| 2 | The warm-rain factors at 0.166 and 0.34 | One sea box of two lunar days, about two hours | What Earth's rates cost the boxes' cloud and rain |
| 3 | The design scheme's relaxation time at 12 h, which Terluna's closures ran only with reference profiles of their own | One GCM run | Its share of the rain's timing and of the upper air's temperature |
| 4 | The diffusion's times multiplied by 0.27, read beside the Earth control's spectra | One GCM run | Whether Earth's times leave noise at the Moon's truncation |
| 5 | CM1's RCEMIP output read through the zero-buoyancy inversion | No runs; a rights review first | Whether the Earth twin of the lunar grid dilutes as ERA5 does |
| 6 | The Earth control with the Moon's refinements beside Kuo's scheme; CM1 under observed forcing; Earth boxes, forced and making their own ascent | About 16 four-thread hours | Whether the two models pass the agreement test on Earth |
| 7 | The gravity pair, each member then making its own ascent | About 24 four-thread hours | The microphysics against similarity |
| 8 | The waterworld twin: the GCM, then sea boxes | 11–12 four-thread hours | Whether the sea's night-rain gap needs land |

Steps 6 to 8 follow the series' own order and costs. The twin of step 8 takes the Moon's 29.5-day solar day and the
Open Moon's air at 1.2 atm.

### 5. The waterworlds

The flagship study takes stages 9 to 13 of `lab/design/plan.md`. Its one-dimensional stages need stage 1 alone and
move beside the other blocks: the steam column and the reproduction (stage 9, under way), escape and the upper air
for any world (stage 10) and the survey (stage 11). The anchors in three dimensions (stage 12) follow block 3 and
the survey, and they take the settings that the Moon's comparison supports. Protection (stage 13) follows where the
survey and the anchors call for it.

### Beside every block

- **The records.** A defect that stays unfixed acts through the registry, which warns or refuses a run outside its
  tested range. The upstream reports go out as their fixes land: ExoPlaSim's Sun clock (reported as issue 69), its
  convective cover counted per model day and its held humidity (A10), and CM1's density fault, whose report is
  drafted in `models/cm1/upstream-ipbl2-density.md`.
- **Integration.** A joint integration brings the lab's and the paper's work to main at the author's word. The next
  one follows this version's draft of the paper and the first ports (11 November 2026), and it joins the defect
  log's entries that the two branches added: A10, B35–B39, C21 and C22.
- **The machine.** Half the machine's cores are the lab's budget (`lab/design/architecture.md`), and Terluna's runs
  share the laptop, so the long runs go overnight.
- **The paper's version 2**, on the paper's branch, below.

## The paper's version 2

Version 2 states the current understanding in every section; earlier readings, corrections and dates stay in the
repository's records. Since it describes the ensemble in this repository, it follows the ports. Terluna enters as
provenance, in the source records and the code and data statement. The revision runs in the order of synthesis: the
body, then the Introduction, then the Conclusion, and the abstract last, with one fresh reviewer's light reading at
each stage and a full editorial review to close, each recorded in `paper/review/`.

| Passage | What version 2 states | Ready, or waiting on |
|---|---|---|
| `abstract.tex` 15, `introduction.tex` 85, `assumptions.tex` 92 and its inventory | Six defects in the released codes, the fifth the simple boundary layer's density fault (A9) and the sixth the humidity held in ExoPlaSim's mean output (A10); CM1's gust over water among the Earth values | Ready (paper branch ff378e2) |
| `introduction.tex` 67 | The GCM's convection, levels, gust and rain evaporation as run, convection the open item | The ports |
| `worlds.tex` 97 (H24), `appendix.tex` 62 | The turned Moon: its tilt of 1.61° and its orientation | Ready; the settled orientation if the orientation check moves it |
| `repairs.tex` and the appendix's repairs table | The repairs above, each with its kind and limits | The ports |
| `repairs.tex` 184–186 (R14), `appendix.tex` 84, `conclusions.tex` 37–39 | CM1 forced through the whole column, its air held only above the GCM's convection | Ready |
| `verification.tex` 70–72 (V08), `appendix.tex` 147 | CM1's longwave, read at constant volume, within 0.013 K/day of the correlated-k model in every layer (0.2–1.3 W/m²) | Ready |
| `results.tex` 36–60, Table `tab:states`, Figure `fig_repairs` | The design case on the turned Moon at sunlight 0.924: 301.20 K and 1.97 mm/day over forty years | Ready; the figure's bars for each repair wait on runs |
| `results.tex` 110–136 (G06–G11, G15), Figure `fig_gap` | CM1's boxes on the design years: 82–84% of the GCM's rain, the timing at sea, the upper air 3.5–10 K colder; the comparison near the ground | The realignment below |
| `next.tex` 3–32 | The open items in order: convection's closure, the upper air's temperature, cloud from CM1's resolved cloud, the reduced radiation scheme | Ready |
| `next.tex` 71–85 (N03) | The tables' edge computed at 0.002–0.003 K/day, with the shield's spectrum for RRTMG a next step; the raindrop limits applied | Ready |
| `reach.tex` | Surface water that turns a body, and the lab's orientation check | The orientation check (block 2) |
| The section before `conclusions.tex`, "Changes from the first version" (`changes.tex`) | What the first version stated and what version 2 states, side by side (below) | Drafted (paper branch c7f0465); for the author's reading |
| `availability.tex` | Terluna's commit for version 2 beside 186b294; the AI-use statement checked against version 2's work | Last |

**The new section.** "Changes from the first version" tells a reader how the paper changed, whether the reader
comes from the first version or reads the second first. A table sets the two versions' statements side by side:
CM1's longwave against the reference model, its forcing from the GCM, the count of defects in the released codes,
the two models as run, the design case, the rain in CM1 against the GCM, the air near the ground, RRTMG beyond its
tables and the order of the next steps. Two paragraphs follow, on what version 2 adds and on what stands under a
condition or is withdrawn. The section is the paper's summary of its own changes; an account of how the models were
refined, which the section held until 11 November, belongs to the notes.

**Realignment before release.** Version 2 waits on CM1 runs with the density fix, the gust at lunar gravity, the
raindrop limits and the whole-column forcing on the turned design years: the 45° N ring for Figure `fig_gap`, and a
comparison near the ground with the GCM. The sea's rain timing and the upper air stay open items in `next.tex`, and
the release proceeds with them open. Once the realignment lands, the
release is tagged `paper-v2` and deposited as a new Zenodo version, with the release register's rows (PASS,
BLOCKED, DEFERRED) on exact hashes. Until then version 2 stays unreleased, and the tag `paper-v1` marks the
released draft.

**The records at release.** `paper/notes/corrections_after_v1.md` becomes the record of what version 2 changed, and
the root README's "Where current understanding differs from the paper" then lists what differs from version 2.

## Open items

- The rights review of RCEMIP's output, before block 4's step 5 brings the data in.
- The numbers for the orientation check's warning and refusal, and the reproduction's tolerance, proposed above and
  set at their stages.
- Snow sublimation's assessment, and CM1's clipped water, before either is classed.
- The unified interface's design.
