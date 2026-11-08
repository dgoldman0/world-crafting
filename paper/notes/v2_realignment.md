# Version 2: what still needs realigning before release

Version 2 is drafted on the paper's branch from Terluna's `main` at `bdda5a07` (8 November 2026) and this
repository's records. Its text states the current understanding wherever runs and records exist. The passages below
state what the runs did, and wait on work in this repository, or on new runs, before the release tagged `paper-v2`
(`PLAN.md`, "The paper's version 2"). Each row is cleared when its work lands and the passage is read again.

| Passage | What the draft states | Waits on |
|---|---|---|
| `repairs.tex`, "Switches and builds" (claim R01) | Ten PlaSim patches; the density, gust and raindrop-limit switches of CM1 | The PlaSim ports (the gust and similarity over water, rain from drop sizes, the level sets, simplified Betts–Miller as an option, the clear share, the cold cloud's factors, and snow sublimation if its assessment admits it) entering `models/exoplasim/` with their patch numbers, and the raindrop limits entering the CM1 series; the patch count and the identity statement are then restated |
| `appendix.tex`, Table `tab:repairs`, the new rows | Switch names as Terluna's runner and builds use them (`ngust`, `nsimw`, `nevapprec`, `nprc`, `nsnowsub`, `NTWLCLEAR`, `ZICEWF`, `ZICERF`, `brkup_gscale`); the boxes' hold under `var14` and `var15` | The ports' own names and defaults; the switches that hold the boxes on the refined-physics state above the convection top, confirmed from `gcm_site.py` |
| `verification.tex`, "Identity and reproduction"; Table `tab:verification` | Identity and source rebuilds of the first version's patches and builds | Identity at default for each new patch, and the series rebuilding the builds behind the boxes on the refined-physics state (the lab's stage 3) |
| `results.tex`, "The gap between the models"; Figure `fig_gap` removed | The boxes on the refined-physics state, at today's orientation | CM1 on the turned design years with the density fix, the gust at lunar gravity, the raindrop limits and the whole-column forcing: the 45° N ring, whose figure takes `fig_gap`'s place, and a comparison near the ground with the GCM |
| `results.tex`, Figure `fig_repairs` | Bars for the repairs of the ten-level states; the refined physics' single changes in the text | Single-change runs of the refined physics on one baseline, if the figure is to carry them |
| `results.tex`, the slice's direction and the storms (claims G09–G11, G15) | Results conditional on the hold from 8 km and CM1's density fault | Reruns that size the bias, if the realignment takes them; otherwise the condition stands |
| `reach.tex`, "Worlds turned by their water"; `refinement.tex`, last paragraph | The practice of deriving a world's orientation from its loads | The lab's orientation check (`PLAN.md`, step 3), which the text then names |
| `worlds.tex` (claims S07, S08), `results.tex` (G18, G24), `verification.tex` (H40) | The design case and the states before it as run, with the night's twilight counted twice; the scenario's sunlight scale 0.924 (1,141 W/m²) | Terluna's corrected design run, with each sunlight pass starting from zero where the Sun is down (about 0.938 at first order); its scale, temperature, rain and vapour then replace the design case's, and the refined and turned states' figures follow if they are rerun |
| `results.tex`, the curved air's 0.65 K (claim G03) | Measured with the double count in the curved-air run alone, stated as too small | A corrected pair, if the realignment runs one; otherwise the statement stands |
| `verification.tex`, the double count; `notes/defect_log.md` C21 | Terluna's finding, uncommitted on 8 November; the mechanism checked here in the pinned `radmod.f90` and patch 07 | The Terluna commit that records the finding and its fix, cited in `claims.json`; the fix ported into patch 07 with its switch |
| `availability.tex` | The first version's statement | Terluna's commit for version 2 (`bdda5a07`, or the commit the realignment reaches) beside 186b294; the AI-use statement checked against version 2's work |

At release, `corrections_after_v1.md` becomes the record of what version 2 changed, and the root README's
"Where current understanding differs from the paper" lists what differs from version 2.
