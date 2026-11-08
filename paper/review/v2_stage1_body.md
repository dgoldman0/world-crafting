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

## The light reading

Pending: one fresh reviewer reads the body against the author's direction and the writing rules.
