# Version 2, stage 1: the body, 8 November 2026

Kept by Claude Opus 5.5, the drafting assistant.

## The author's direction

For version 2, the author asked that the paper stay standalone and be "updated to ONLY the current best
understanding", which "avoids turning it back into a log", with one added section covering "how models have been
refined and improvement to our undestanding of how these models function and work", placed before the Conclusion.
It remains "a paper about the software", with Terluna as provenance only. The update uses the turned Moon, takes the
physics confirmed as corrected, and goes where it can: "We should update where we can and note what still needs to
be realigned." For this pass: "Remember evaluate and edit in sections, compare against the whole paper to make sure
it works consistently, work in the prescribed order established for paper editing." The order is the body, then
the Introduction, then the Conclusion, and the abstract last, with a light reading by one fresh reviewer at each
stage and a full editorial review to close (`AGENTS.md`, "Review of the paper").

## What the stage changed

The numbers come from Terluna's `main` at `bdda5a07` and its research drive, registered in `claims.json` as
`terluna@bdda5a07:` sources; `tools/check.py` now checks that form. What waits on ports or runs is listed in
`../notes/v2_realignment.md`.

| Section | Evaluation | Change |
|---|---|---|
| `worlds.tex` | The scenario named the 295 K design case at sunlight 0.970 and today's orientation and grid | The design case is the turned Moon at 0.924 (1,141 W/m²) and 301 K; its grid's water (667 cells, 38%) and pressures (1.03–1.21 atm); the turn stated once (S17); the tilt 1.61°; the regime table at 301 K (53 km, 0.031, 7.1), from `regime_calc.py` and the worlds extract rerun at 301.25 K, with `fig_regimes` regenerated; the design case's vapour 303 kg/m² |
| `assumptions.tex` | Four defects; PlaSim's convection, mixing, surface exchange and rain evaporation, and CM1's gust over water, absent as Earth values; RRTMG's extrapolation unmeasured | Five defects, the fifth CM1's boundary-layer density fault (H34); a paragraph on the Earth values of convection, mixing and surface exchange (H37, H38); γ (H36); the extrapolation's 0.002–0.003 K/day (H35); the vertical grid without "the design case"; inventory rows added and updated |
| `repairs.tex` | The new repairs absent; the forcing described as the hold from 8–16 km | The density fix (R17); the raindrop limits (R18); the gust and similarity over water (R19); a paragraph on levels, convection and rain (R20–R23); the 301 K curved-air table and the clear share (R24); the longwave refit per state (R25); the whole-column forcing (R14), with the ten-level runs' hold stated |
| `verification.tex` | V08 read CM1's tendencies at constant pressure | V08 at constant volume, within 0.013 K/day; five adaptation defects in reported runs, the hold from 8 km among them (H39) |
| `results.tex` | The chain ended at the 295 K design; the gap section rested on the 45° N ring with the density fault and the hold | Three states added (refined physics, turned, design case) with their effects (G18, G19, G24); the gap section rewritten on the boxes at three sites against the test set before them (G20–G23), Figure `fig_gap` removed until the ring is rerun; the rings' and storms' conditions stated |
| `reach.tex` | Drop limits Earth's; the orientation absent | The density fault in other configurations; the drop limits and gust scaled; RRTMG's extrapolation measured; a paragraph and a table row on worlds turned by their water (W07) |
| `next.tex` | Led by the longwave at 295 K against 307 K and by cloud | Reordered: convection's closure (N05), the upper air's temperature (N06), cloud (N07), a reduced radiation scheme; radiation in CM1 (N08), microphysics (N03) and the independent GCM restated |
| `refinement.tex` (new) | — | Refinement of the models, before the Conclusion: the forcing and the test, CM1's defect, Earth values and output reading, the GCM's lower air and the open convection, the Moon's turn and the practice it implies |
| `appendix.tex` | Configurations and switches of the first version | Fifteen levels and the boxes on the refined state; new switch rows; the verification rows for RRTMG and the longwave refit |

Checks: `make paper` builds without warnings; `tools/check.py` passes (133 claims cited, two registered and
uncited); the excluded words were searched for in every edited section, with no match. `tools/lint.py` screens only.

## The light reading (87881f0)

One fresh Claude Opus 5.5 subagent read the body whole against the author's direction and `AGENTS.md`, spot-checking
numbers in `claims.json`, and edited nothing. It found 3 BLOCKING, 12 MAJOR and 13 MINOR findings, and judged that
the body states the current understanding with no dates, correction log or Terluna in the prose outside the new
section, the defect counts, the hold and the boxes' 82–84% agreeing across sections.

| Finding | Disposition |
|---|---|
| B1. The dry south-east box, a land box, puts 24% of its rain in another quarter; the text gave the sea alone | Fixed in Results, Next steps and the new section |
| B2. The new fits (drop sizes, cold cloud, snow) contradict "every calibration is clear-sky" and a calibration defined against the reference model alone | Calibration widened in Repairs; Verification and Next steps restated for the radiation; Reach's recipe takes the orientation, the level set and the new refits |
| B3. The Earth-values section gave the 295 K column's curvature figures as the design case's | The design case's 301 K column in Assumptions and the inventory (net 8.0 W/m²); Repairs names the 295 K column as the method's and the slant factors' source |
| M4. "Design" still named the 295 K state and its column | The state renamed "Corrected curved air"; "the 295 K column" throughout; "the refined-physics state" matches the table; the change of target stated once, in the scenario |
| M5. Evaporation shares from different runs | One comparable pair for PlaSim (a fifth against half); CM1's 86→48% tied to its box; 0.69 against 0.51 tied to the sea box |
| M6. General repairs singly 1.6–2.5 K left out the gust and the clear share | 0.7–2.5 K, the gust least; the curved-air terms and their clear share about a kelvin each |
| M7. MM5's gust ×1.6–1.8 without Beljaars's ×1.1–1.2 | Both given, in prose and inventory |
| M8. The new section's night-rain inference lacked the Kuo-forced box's 0.14 mm/day | Both forcings given, each GCM named |
| M9. One 303 K column compared with global means | The shortwave calibration stated as checked on the 295 K state's columns alone |
| M10. Empty actions opening the new section | Rewritten with the operations named |
| M11. The new section repeated body numbers, lacked the state-specific calibration and ended on orientation alone | Rewritten: fewer numbers, each paragraph ending on what it shows; the calibration's dependence on state and the double count added |
| M12. Reach's comparison without a second term | "On a body as nearly spherical as the Moon …" |
| M13. "Convects 0.93–0.95 of the boxes' rain", target undefined | The closure's shares stated: 0.87–0.95 by convection at the boxes' sites, 58–74% of the tropics' rain to large-scale condensation |
| M14. A 70-word sentence; "test set" read as a noun; processes unnamed; "carrying the weather" opaque | "An agreement test fixed before they ran", its quantities named; the weather forcing described |
| M15. Betts–Miller, Beljaars's gust, MM5's gust and McSnow uncited | `frierson2007dynamics` (original archived, read at the claim's locators), `beljaars1995parametrization` and `brdar2018mcsnow` (blocked, read at their abstracts) added to `references.bib` and `sources/manifest.json`; MM5's gust cited to CM1's code |
| Minor findings | Tilt 1.61° in the orbit row; "opt-in" dropped; the RRTMG Sun row reworded; the hold's start at 93 km; CM1's least wind of 0.1 m/s; the dimming's reset stated once; the anvils clause; the lakes clause; the first version named by its tag; heating rates in place of "every comparison"; "within years" replaced by the filling and the crust's elastic response; "Near-side Sea" throughout; the later routing of the lakes; three passives joined |

The conflicts the reviewer listed with the abstract, the Introduction and the Conclusion go to the next stages.

## The double count of the night's twilight

During the reading, Terluna's work on the polar sunlight found that every run with the curved-air terms counted the
night's twilight twice, through PlaSim's cloud-forcing diagnostic and this repository's patch 07; the mechanism was
checked here in the pinned `radmod.f90` and the patch. The body now states it as an adaptation defect in reported
runs (claim H40, defect log C21), with its bearing on the curved air's 0.65 K, the design case's dimming and the
GCM's side of the comparison with CM1. The design case's numbers wait on Terluna's corrected run
(`../notes/v2_realignment.md`).

The fixes are unread by a further reviewer; the full editorial review that closes the sequence reads them.
