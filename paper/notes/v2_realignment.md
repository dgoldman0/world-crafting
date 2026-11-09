# Version 2: what still needs realigning before release

Version 2 is drafted on the paper's branch from Terluna's `main` at `bdda5a07` (8 November 2026) and this
repository's records. Its text states the current understanding wherever runs and records exist. The passages below
state what the runs did, and wait on work in this repository, or on new runs, before the release tagged `paper-v2`
(`PLAN.md`, "The paper's version 2"). Each row is cleared when its work lands and the passage is read again.

| Passage | What the draft states | Waits on |
|---|---|---|
| `repairs.tex`, "Switches and builds" (claim R01) | Ten PlaSim patches; the density, gust and raindrop-limit switches of CM1 | The PlaSim ports (the gust and similarity over water, rain from drop sizes, the level sets, simplified Betts–Miller as an option, the clear share, the cold cloud's factors, and snow sublimation if its assessment admits it) entering `models/exoplasim/` with their patch numbers, and the raindrop limits entering the CM1 series; the patch count and the identity statement are then restated |
| `appendix.tex`, Table `tab:repairs`, the new rows | Switch names as Terluna's runner and builds use them (`ngust`, `nsimw`, `nevapprec`, `nprc`, `nshcap_bm`, `nsnowsub`, `NTWLCLEAR`, `ZICEW`, `ZICEWF`, `ZICERF`, `brkup_gscale`); the boxes' build with the density fix and the gust compiled in; their `var7`, `var8`, `var10`, `var14` and `var15` read from the boxes' namelists | The ports' own names and defaults, and the lab's switches for the density fix and the gust (`ipbl2_per_mass`, `gust_over_water`, lab branch f99b7e6) once integrated |
| `verification.tex`, "Identity and reproduction"; Table `tab:verification` | Identity and source rebuilds of the first version's patches and builds | Identity at default for each new patch, and the series rebuilding the builds behind the boxes on the refined-physics state (the lab's stage 3) |
| `results.tex`, "The gap between the models"; Figure `fig_gap` removed | The boxes on the refined-physics state, the turned sea box (forced by the turned state at the target, which carries the twilight's double count) and the boxes making their own ascent, the two couplings bracketing the GCM's rain; the land and dry boxes on the turned climate paused at day 3 | CM1 on the design case with the density fix, the gust at lunar gravity, the raindrop limits and the whole-column forcing: the 45° N ring, whose figure takes `fig_gap`'s place, and a comparison near the ground; the work of closing the gap, which Terluna moved to this project on 9 November |
| `results.tex`, Figure `fig_repairs` | Bars for the repairs of the ten-level states; the refined physics' single changes in the text | Single-change runs of the refined physics on one baseline, if the figure is to carry them |
| `results.tex`, the slice's direction and the storms (claims G09–G11, G15) | Results conditional on the hold from 8 km and CM1's density fault | Reruns that size the bias, if the realignment takes them; otherwise the condition stands |
| `reach.tex`, "Worlds turned by their water"; `refinement.tex`, last paragraph | The practice of deriving a world's orientation from its loads | The lab's orientation check (`PLAN.md`, step 3), which the text then names |
| `results.tex`, the curved air's 0.65 K (claim G03) | Measured with the double count in the curved-air run alone, stated as too small | A corrected pair, if the realignment runs one; otherwise the statement stands |
| `verification.tex`, the double count; `notes/defect_log.md` C21 | Terluna's finding and fix (`NTWLZERO`, `domain/climate` 2762669e), the mechanism checked here in the pinned `radmod.f90` and patch 07; the design case runs with the fix | The fix ported into patch 07 with its switch |
| `repairs.tex`, the equinox's regression (claim R26); Table `tab:repairs` | Terluna's precession patch (`domain/climate` 39ac7f0c), run in the design case | The patch ported into `models/exoplasim/` with its switch and identity default |
| `availability.tex` | The first version's statement | Terluna's commit for version 2 (`bdda5a07`, or the commit the realignment reaches) beside 186b294; the AI-use statement checked against version 2's work |

At release, `corrections_after_v1.md` becomes the record of what version 2 changed, and the root README's
"Where current understanding differs from the paper" lists what differs from version 2.

Cleared on 9 November: the design case's numbers now come from Terluna's corrected run
(`A28R_301k_design_l15_snow_s938_turned_refit_precession`, the twilight counted once and the equinox regressing, at
sunlight 0.938; Terluna `main` 03da9585 and `domain/climate` 79d0fefa), and the states before it are stated as run,
with the double count.

