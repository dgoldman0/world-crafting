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
  codes' defects number five: the first version's four and the simple boundary layer's density fault (A9).
- The paper's version 2 states the current understanding throughout and adds one section, just before the
  Conclusion, on how the models were refined. It is developed on the paper's branch and
  released once the CM1 results are realigned (below); the tag `paper-v1` keeps the first version.
- Components run when a study calls for them. Each fix enters with its released model's behaviour as its default;
  before anything runs, `lab plan` reports a task's estimated cost and the results of its checks, and compute runs
  once the user starts it and the checks clear.
- A fix serves every world as one component when the Earth control stays within 2σ of the released model's yearly
  means with it on; otherwise it becomes a switch that stays off for Earth.
- Level sets are generated for each world from its scale height, and a world whose scale height is near Earth's
  keeps ten levels.
- CM1 boxes that carry the GCM's weather are an option for the studies that need them.
- The unified interface, in which a user describes a world, chooses its components, sees their cost and checks and
  starts the compute, gets its own design step before any user-facing work.
- The lab's design temperature for the Open Moon (295 K, beside Terluna's 301 K) is decided separately, later.

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
| Simplified Betts–Miller convection | Low to medium | A setting with Kuo's scheme its default; the depth test a fraction of the surface pressure | ×1 | Terluna's CM1 analysis |
| The box forcings: converging inflow, carried weather and the box's own ascent | Low to medium | Case variants; carried weather an option for the studies that need it | Carried weather ×3.5–7 a box, up to about 380 GB for a large one; the ascent ×2 | Terluna's CM1 analysis |
| The cold cloud's factors and the longwave refit | Medium, for Terluna's climate | The Moon's calibrations; stage 5 fits the lab's own | A refit of about three hours | Terluna's CM1 analysis |
| Snow sublimed from capped flakes | Low: unassessed | Assessed before any port | — | Its assessment |

The type of world sets CM1's cost more than any fix. Under rule 9 of `lab/design/world_spec.md` CM1's grid follows
the scale height, so per simulated second a box costs in proportion to gravity and a ring to the radius times the
square of gravity: a ring on Earth costs about 130 times the Moon's, and the Moon's solar day, 29.5 times Earth's,
offsets most of that over a day and night. Columns of 3 or 2 km in place of 6 would cost 8 or 27 times as much.

## The sequence

The work runs in five steps. Each change in them is small and tested and gets one review (AGENTS.md,
"Software work"), and each patch keeps an identity default.

**1. The records.** The defect log, `notes/cm1.md`, `notes/exoplasim.md`, `notes/verification_record.md` and the
root README's "Where current understanding differs from the paper" take the findings above.

- The defect log's entries for PlaSim take these states:
  - B29, Kuo's convection: replaced in Terluna's design runs by simplified Betts–Miller, under test;
  - B30, the evaporation constant γ: replaced by drop sizes and fall speeds;
  - B31, the ten levels: fifteen, as an option;
  - B32, the mixing lengths and the 1 m/s wind floor: the lengths still Earth's, the floor replaced by the gust;
  - B33, the free-convection constant: replaced by Beljaars's gust with similarity theory;
  - B34, shallow convection's cap at 700 hPa: kept.

  A9, C19 and C20 stand as recorded.
- A new Earth value: CM1's gust over water, in every CM1 run behind the paper's first version. CM1's clipped water
  is examined before it is classed.
- The README's rows: CM1's quiet sea nights came with the forcing of the GCM that ran Kuo's scheme; the longwave row
  takes sunlight 0.924 on the turned Moon; the near-ground row's boxes ran on that same forcing; a new row gives the
  turn.

Acceptance: the records agree with each other and with the table above, `make check` passes, and one review reads
the change.

**2. The ports.** Terluna's code for the corrected physics enters `models/` as patches at the next numbers of each
series, and `python/` at Terluna's package paths. Each README states its fix's kind and limits from the tables above. The
ports run in the order of "Porting: confidence, form and cost", the three CM1 fixes rated high first.

- CM1: the density fix, beside the report drafted in `models/cm1/upstream-ipbl2-density.md`; the gust over water at
  the build's gravity; the raindrop limits (the lab's stage 3); the whole-column forcing,
  `python/climate/crm/gcm_site.py`.
- ExoPlaSim: Beljaars's gust with similarity over water; rain evaporation from drop sizes; the fifteen-level set as
  an option; simplified Betts–Miller with its depth test as an option, Kuo's scheme its default; snow sublimation
  once assessed.
- The lab's readers of CM1's radiative output take the constant-volume conversions.

Acceptance: each patch at its default reproduces the build without it byte for byte, a test pins its effect,
`models/check_patches.sh` covers the new patches, and `make check` passes.

**3. The lab's orientation check.** Stage 2 derives a world's orientation, and stage 4 tracks it.

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

**4. The lab's documents and settings.** `lab/design/plan.md` takes stages 2, 3, 4, 5, 6 and 8 and the section
"The GCM's convection, boundary layer and levels", which names simplified Betts–Miller as the scheme of Terluna's
design runs. `lab/configs/` gains each new setting at its released model's default; `lab/studies/open-moon.toml`
takes the turned Moon and the whole-column forcing; `lab/registry/` takes the states of B29–B34, CM1's gust and the
orientation check.

**5. The paper's version 2**, on the paper's branch, below.

## The paper's version 2

Version 2 states the current understanding in every section; earlier readings, corrections and dates stay in the
repository's records. Since it describes the ensemble in this repository, it follows the ports. Terluna enters as
provenance, in the source records and the code and data statement. The revision runs in the order of synthesis: the
body, then the Introduction, then the Conclusion, and the abstract last, with one fresh reviewer's light reading at
each stage and a full editorial review to close, each recorded in `paper/review/`.

| Passage | What version 2 states | Ready, or waiting on |
|---|---|---|
| `abstract.tex` 15, `introduction.tex` 85, `assumptions.tex` 92 and its inventory | Five defects in the released codes, the fifth the simple boundary layer's density fault (A9); CM1's gust over water among the Earth values | Ready |
| `introduction.tex` 67 | The GCM's convection, levels, gust and rain evaporation as run, convection the open item | The ports |
| `worlds.tex` 97 (H24), `appendix.tex` 62 | The turned Moon: its tilt of 1.61° and its orientation | Ready; the settled orientation if step 3 moves it |
| `repairs.tex` and the appendix's repairs table | The repairs above, each with its kind and limits | The ports |
| `repairs.tex` 184–186 (R14), `appendix.tex` 84, `conclusions.tex` 37–39 | CM1 forced through the whole column, its air held only above the GCM's convection | Ready |
| `verification.tex` 70–72 (V08), `appendix.tex` 147 | CM1's longwave, read at constant volume, within 0.013 K/day of the correlated-k model in every layer (0.2–1.3 W/m²) | Ready |
| `results.tex` 36–60, Table `tab:states`, Figure `fig_repairs` | The design case on the turned Moon at sunlight 0.924: 301.20 K and 1.97 mm/day over forty years | Ready; the figure's bars for each repair wait on runs |
| `results.tex` 110–136 (G06–G11, G15), Figure `fig_gap` | CM1's boxes on the design years: 82–84% of the GCM's rain, the timing at sea, the upper air 3.5–10 K colder; the comparison near the ground | The realignment below |
| `next.tex` 3–32 | The open items in order: convection's closure, the upper air's temperature, cloud from CM1's resolved cloud, the reduced radiation scheme | Ready |
| `next.tex` 71–85 (N03) | The tables' edge computed at 0.002–0.003 K/day, with the shield's spectrum for RRTMG a next step; the raindrop limits applied | Ready |
| `reach.tex` | Surface water that turns a body, and the orientation check of step 3 | Step 3 |
| A new section before `conclusions.tex` | How the models were refined (below) | The ports and step 3 |
| `availability.tex` | Terluna's commit for version 2 beside 186b294; the AI-use statement checked against version 2's work | Last |

**The new section.** Its working title, "Refinement of the models", names its subject. Its paragraphs take in turn:

- the GCM: what replacing Kuo's scheme, the ten levels, the Earth free-convection term and the constant γ changed,
  and why convection remains the open item;
- CM1: the constant-volume reading of its radiative tendencies, the density fault, the gust over water and the
  raindrop limits;
- forcing a cloud-resolving model from a GCM: through the whole column, its air held only above the GCM's
  convection, judged by an agreement test set before the runs, and where the two models agree and differ;
- the orientation: angular momentum fixes the spin axis, and the body turns beneath it until its principal axes
  align with the spin and the host; the Moon's turn within years and its long-term range; the turned climate's
  0.8 K; and the practice that follows, a world's orientation derived from its loads whenever water is added, as
  the lab's check derives it.

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

- The lab's design temperature for the Open Moon.
- The numbers for the orientation check's warning and refusal, and the reproduction's tolerance, proposed above and
  set at their stages.
- Snow sublimation's assessment, and CM1's clipped water, before either is classed.
- The unified interface's design.
