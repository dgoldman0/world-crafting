# Version 2, the closing full review, 8 November 2026

Kept by Claude Opus 5.5, the drafting assistant. The author's direction is quoted in `v2_stage1_body.md`.

Two fresh Claude Opus 5.5 subagents read the whole paper at f17e44f, a frozen snapshot, and edited nothing: one for
prose and the author's direction (no BLOCKING finding, 5 MAJOR, 9 MINOR), one for evidence, consistency and scope
(3 BLOCKING, 8 MAJOR, 7 MINOR). The evidence reviewer recomputed the design, turned and refined states' means from
`progress.json`, and the design case's vapour, pressure, water cells and absorbed sunlight from its output, and found
them all as stated; it checked the 50 new or changed claims against their cited Terluna lines, the defect log and
the repository's patch records. The prose reviewer judged that version 2 carries out the direction in substance,
with no dates or correction log outside the new section and Terluna as the design's origin alone.

## Evidence and scope

| Finding | Disposition |
|---|---|
| B1. The faults were said to be found by closing budgets under the agreement test; the defect log records other routes (the rain limits in the code, the reading error by an offline RRTMG run, the density fault in a box still held from 8 km, the gust beside the GCM's wind), and the test was fixed on 1 November | Each fault given its route in the new section; the Introduction says they were found by setting one model against another or against its own surface fluxes; the test tied to the boxes on the refined-physics state (G20) |
| B2. The cold upper air was put down to CM1's plume dilution, where the dilution study gave no verdict and Terluna's record gives the band's causes as radiation at sea and in the dry box and the imposed ascent on land, with the band still cooling; boxes making their own ascent change the result | Results restated from the records (G23) with the self-made-ascent boxes (G26, new); Next steps' upper-air item gives the proposed target and the dilution rates by layer as a proposal; the abstract, Introduction and Conclusion state the gap as both comparisons show it and put the boxes' ascent beside the GCM's convection |
| B3. The rebuild and patch-series statements covered the first version's builds alone | Scoped to the ten-level states and the CM1 builds behind their results; the refined physics and the boxes' build stated as the runners' own |
| M4. Ten patches where the repository holds eleven | Eleven; patch 11's ice weights added to `tab:repairs` |
| M5. The boxes ran a Terluna build with the density fix and the gust compiled in, where the table gave the lab's switches | The build named; the rows say "compiled into the boxes' build" |
| M6. The boxes also pull their wind toward the GCM's and draw in its air where the mean wind converges; the hold's heights belonged to earlier boxes | Read from the boxes' namelists: wind from about 0.3 km over two hours (`var8`, `var10`), inflow (`var7`), hold from 94.3 km to 130.6 km above a convection top near 73 km; prose and both tables corrected |
| M7. The weather box's shortfall is unresolved and the box reads as observations | Stated so |
| M8. The anvil gap's attribution | As the record gives it: the convective cover's formula, closed on land by a lunar intercept, the sea's gap following the rain's timing, the lunar-day cloud effects within 4–14 W/m² |
| M9. The shallow convection's cap is replaced in the design case | Inventory row "Setting"; `nshcap_bm` in Repairs and `tab:repairs` |
| M10. The longwave fits named; the turned run's fit strays to 3.56 W/m² | Each fit named; the turn's 0.80 K given with the stray fit |
| M11. "About 20%" on Earth is the code's arithmetic, untested | "By the code's arithmetic up to about 20%" |
| Minor findings | PlaSim's gust over every surface and the 1 m/s kept as least shear; the design case's slow cooling; the twilight fix as a runner switch still to be ported; the orientation row removed from `tab:reach` and the cold-cloud row updated; the seas' and lakes' shares kept apart; the correlated-k emulation named |

## Prose and direction

| Finding | Disposition |
|---|---|
| M1. The new section's night-rain paragraph lacked its forcing states and mechanism | Both states named, both forced through the whole column; the mechanism stated; the lesson follows the comparison; the surface law tied to the comparison |
| M2. Two design temperatures without an account | The 295 K state's dimming given without a target; 301 K named where the refined-physics state's dimming is set |
| M3. The turn told six times, the mantle's geophysics as Terluna reporting, the reach row claiming the models represent the turn | The mantle reduced to the clause that justifies the elastic state; the Introduction and Reach trimmed; the abstract's clause cut to the condition the runs take; the reach row removed |
| M4. The double count stated six times | Dropped from the Conclusion and from the Results' gap paragraph; Verification states it |
| M5. Verbs given to abstractions | Operations named throughout ("the two models differ…", "set with the excess present", "giving RRTMG the shield's spectrum is the step that remains") |
| Minor findings | The four faults' plausibility restated; the boxes compared named in the Introduction; "The reference's accuracy"; repeated numbers trimmed; Reach's recipe as a numbered list in its order; undefined terms defined; the new section's opening says what changed and adds the cold cloud; the Conclusion's orientation sentence placed with the lakes; the abstract's compound subject and the Next steps' dimming sentence placed; the drop limits' effect moved to Repairs |

## For the author

Unchanged wording approved in the first version, left as it stands:

- Verification: "a code review found the omission after the windows … had run, though before the main electrified
  run began" is process history in the body.
- Conclusion: "Those limits also define physical questions" gives a verb to "limits".
- Points left for the author in `v2_stage3_conclusion.md` and `v2_stage4_abstract.md` stand.

The fixes of this round are unread by a further reviewer. The draft goes to the author for reading; the passages in
`../notes/v2_realignment.md` wait as recorded there.
