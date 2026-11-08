# World-crafting

An ensemble in development for modelling the climate, storms and seas of Gaean exoplanets and
constructed worlds. Gaean worlds have nitrogen–oxygen air and water as the principal condensable,
at broadly terrestrial surface pressures and temperatures permitting liquid surface water and an active
water cycle; their gravity, size, rotation and starlight may differ substantially from Earth's.

The ensemble connects ExoPlaSim (a general circulation model), CM1 (a cloud-resolving model, here with
WRF-ELEC's storm electrification), SWAN (a spectral wave model) and SWASH (a phase-resolving shore model).
The repository holds their patches and new Fortran, the in-house reference and calibration tools, and the
paper describing their development and tests.

The first world is Terluna's Open Moon (github.com/dgoldman0/Terluna): 1.2 atm of nitrogen and oxygen
at the water level, seas over 28% of the surface with rain-fed lakes above them, sunlight filtered by a
shield, lunar gravity and the 29.53-day solar day. The machinery came from Terluna at commit 186b294 (2026-10-17).

## Where current understanding differs from the paper

The paper's first released draft (tag `paper-v1`) reports the models as they stood at Terluna's commit 186b294.
Terluna, comparing CM1 boxes with the GCM at two sites budget against budget, explains the two models' differences
in other terms than the paper does. A defect in CM1's simple boundary layer biases every ring and box the paper
reports, and all of them were nudged toward the GCM from 8 km, a hold that in a box over the sea did the work of its
deep convection. Of the difference that remains, Terluna traces the sea's night rain to PlaSim's Kuo convection and
most of the colder upper air to the mixing in CM1's updrafts, and it is testing PlaSim's vertical levels and
boundary-layer mixing as further causes. In the table, each
affected passage of the paper is paired with the current understanding; the notes in `notes/` hold the detail and
the evidence, and `paper/notes/corrections_after_v1.md`, on the `paper/conclusion-development` branch, lists the
passages a revision of the paper would change.

| Passage in the paper | Current understanding | Detail |
|---|---|---|
| Abstract, Introduction and "Earth values and defects": four defects in the released codes on the lunar runs' path | Five. CM1 r22's simple boundary layer (`ipbl = 2`) hands the solver its tendencies multiplied by the air's density, so Terluna's boxes took 1.3–1.5 times the surface's heat and water into their boundary layer; the error grows with the air's density and reaches Earth's runs as well | [defect_log.md](notes/defect_log.md) A9; [cm1.md](notes/cm1.md), "The simple boundary layer's density" |
| Repairs, "Forcing from the GCM", and the Conclusion: nudging toward the GCM only above 8–16 km leaves CM1's boundary layer and convection to develop freely | Lunar convection reaches 55–80 km, so that hold covers most of the convecting column: in a box over the Near-side Sea the nudging supplied 89 of the 107 W/m² the box's radiation removed, and the box rained 0.06 mm/day against the GCM's 2.72. Terluna's boxes now take the GCM's own tendencies through the whole column and hold their air only above the top of the GCM's convection | defect_log.md C19; cm1.md, "The nudging and the convection" |
| Verification, claim V08: RRTMG cools the 45° N ring's three lowest GCM layers 4.5, 8.5 and 10.2 W/m² more than the correlated-k model | Under `eqtset = 2`, CM1 stores its radiative tendencies at constant volume and hands RRTMG the ground's temperature for the air at the ground. Read so, its longwave comes within 0.013 K a day (0.2–1.3 W/m²) of the correlated-k model in every layer; the paper's figures came from reading them at constant pressure, 38–40% too large, with the air at the ground extrapolated | defect_log.md C20; cm1.md, "Reading CM1's radiative output" |
| Results, "The gap between the models": CM1's lowest 1.8 km at 45° N run 3.7 K warmer than the GCM, about 1.5 K of it the GCM's longwave over-cooling and the rest plausibly upward transport of heat | With CM1's radiation read correctly, the GCM's over-cooling is worth about 2.7 K of the 3.7 K. Terluna's boxes, with the boundary layer fixed and the forcing taken through the column, run 0.23 K (sea) and 1.15 K (land) warmer than the GCM at 2 m, against 1.8–4.7 °C in the rings; they also differ in site and forcing state and carry the lunar drop limits, Terluna reads most of the rings' warmth as the boundary layer's fault, and the 45° N ring has yet to be rerun | cm1.md, "What the forcing revealed" |
| Results: CM1's box rains about a quarter of the GCM's rain, with 85% of its falling water evaporating | Terluna traces most of that gap to the forcing, the boundary layer's fault and Morrison's Earth drop limits. Lunar drop limits nearly doubled the rain at the ground and cut the evaporated share from 86% to 48%; with all three changed, the land box rains 92% of the GCM's rain at the GCM's hours, and the sea box 31–49%, nearly all between noon and midnight, while PlaSim's Kuo scheme keeps raining after midnight under sinking air | cm1.md, "Fall speeds" and "Rain against the GCM" |
| Results: the storms, the lightning, NSSL against Morrison, and the effect of a slice's direction | Records of runs made with the 8–16 km nudging and the boundary layer's fault; reruns would size the bias | cm1.md |
| Next steps, "Radiation in CM1": extend RRTMG's tables past 1,053.63 hPa to test the extrapolation | Measured offline, the table's edge moves the lowest layers' cooling by 0.002–0.003 K a day. Giving RRTMG the shield's spectrum remains to be done | defect_log.md B22; cm1.md, "Radiation inputs and range" |
| Next steps, "The longwave at the settled state" | The 295 K fit leaves layers up to 6.8 W/m² off at 301 K, and a refit on 301 K columns holds within 0.3 W/m² there; each state, level set and convection scheme takes its own refit. Terluna's design climate is now 301 K, held at a sunlight scale of 0.897, where the paper's design case took 0.970 for 295 K; with the cold cloud's factors, which the design case takes, the same sunlight settles near 298.5 K, the state that forced Terluna's boxes | [exoplasim.md](notes/exoplasim.md), "Longwave by height"; defect_log.md B18 |
| Next steps, "Cloud from the cloud-resolving model" | With the cold cloud's water and crystal size worked out at lunar gravity, the climate settled 2.8 K cooler, with 19% less rain, the cover's response being the run's least certain part; by a first-order estimate, halving or doubling the top three layers' cloud water or crystal size moves the ground 5–7 K | exoplasim.md, "Cloud water in metres" |
| Abstract, Introduction, Next steps and Conclusion: radiation and cloud as the fits to replace first | Matching CM1 depends as much on PlaSim's Kuo convection, its ten σ levels (on the Moon the lowest layer is 1.73 km deep), its Earth mixing lengths and wind floor, its free-convection constant over water and its 700 hPa shallow-convection top, each an Earth value in the paper's sense. CM1's upper air runs 7.7–10 K colder than the GCM's at 42–56 km, mostly from its updrafts' mixing. Terluna's replacement schemes, level sets and a nonlocal boundary layer so far leave CM1's rain by time of day unmatched at one site or both; in its latest single-column test the sea's night layer is lost under deep convection whichever boundary layer the column has | exoplasim.md, "What stays Earth's in PlaSim"; defect_log.md B29–B34 |

## Layout

| Folder | Holds |
|---|---|
| `models/exoplasim/` | Patches to ExoPlaSim 3.4.2's PlaSim source |
| `models/cm1/` | Patches to CM1 r22, the Fortran written for its electrified build, and the build variants |
| `models/swan/`, `models/swash/` | Patches to SWAN 41.51; SWASH 12.01's lunar settings |
| `python/` | In-house reference and calibration tools, under their Terluna package paths |
| `notes/` | Each component's correctness, limits and room for improvement |
| `paper/` | The paper: notes, sections, figures, data extracts, source records, review records |

`PROVENANCE.md` records every brought file's Terluna path and hash and every upstream pin.

## The paper

`paper/` builds with `make pdf` (LaTeX with biber) and checks with `make check` (every input, figure,
citation key and claim source present) and `make lint` (candidate places for the editorial passes). Every
number in the text carries a `\claim{}` marker traced in `paper/claims.json` to a file in Terluna at
186b294, a file here, a run on Terluna's research drive, a web record or a calculation in
`paper/tools/regime_calc.py`. The review records are in `paper/review/`: the ten prose passes for each
section, two technical referees' reports with their dispositions, and the whole-manuscript challenge.
`paper/notes/plan.md` holds the build stages and their state; the release register records what has
passed, what is blocked and what is deferred.

## Checks

`make check` applies every patch series to its pinned upstream source and runs the Python tests. The sky
solver's tests need numba; on this machine the environment `/media/projectspace/terluna-research/venvs/optics`
carries it, and the radiative–convective model's spectroscopic inputs must be restored by its fetcher.
