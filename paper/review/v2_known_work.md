# Version 2: known work stated as the paper's own, 8 November 2026

Kept by Claude Opus 5.5, the drafting assistant.

## The author's reading

Reading the draft at 72029b4, the author found the paragraph on the Moon's turn in "Refinement of the models"
"written as if it is a new discovery. It's obviously a known phenomenon though perhaps because we don't spend our
careers building planets it MIGHT be an easy thing to over look. So writing it as a 'be sure to check and those
kinds of checks will be built into the lab if the work continues' type thing is one thing." The author asked for one
subagent to look for similar phrasing first, so that every such fix goes into the same round.

## The scan (72029b4)

One fresh Claude Opus 5.5 subagent read every section against the paper-v1 diff and edited nothing. It found the
fault concentrated in version 2's new prose: every paragraph of the new section closed on a general rule that the
literature or the paper's own premises already state, the Results' closing sentence on the boxes' ascent repeated
it, the turn appeared seven times without the literature on true polar wander, and the damped gravity wave appeared
without Kuang's name.

| Finding | Disposition |
|---|---|
| The turn as a discovery (new section; Reach) | Named as true polar wander and cited (Matsuyama, Nimmo and Mitrovica 2014; for the Moon's own, Keane and Matsuyama 2014); the mechanics cut; the Moon's computed turn kept as the scenario's; the practice stated as a check the ensemble's set-up is to make if the work continues |
| Tuning absorbing other errors stated as a lesson | Cited (Hourdin et al. 2017); the twilight fault and the cold cloud's 2.8 K kept as this work's; the last sentence made the check after each retune |
| The forcing's hold on CM1's result as a general rule; the damped gravity wave uncited | The general sentence cut; prescribed ascent setting a column's rain attributed (Sobel and Bretherton 2000); Kuang (2008) named in Results and the new section; "thus" dropped from Results |
| The coupling height as a general lesson | Stated as a defect of the adaptation and its fix, the hold now read from the GCM's convection top at each site |
| The turn elsewhere | Cited at its first mention in the Introduction; the abstract's clause removed, the abstract back to its approved wording there |
| "Each fault … found by setting CM1 against something outside it" overreached its list | Each fault's route given; budgets closed against a model's surface and a second model stated as the check |
| Known laws uncited | The capillary length cited (Loftus and Wordsworth 2021); CM1's grid dependence (Bryan, Wyngaard and Fritsch 2003); the moisture-supply view behind Kuo's scheme (Emanuel, Neelin and Bretherton 1994) |

The seven new sources are in `references.bib` and `sources/manifest.json`: Keane and Matsuyama's accepted manuscript
archived and read at the claim's locators, the other six blocked by browser challenges or closed access and read at
their abstracts.

## For the author

Wording approved in version 1, left as it stands:

- Conclusion: "Agreement in total outgoing radiation can coexist with different cooling profiles, so matching the
  layers matters", and Repairs' "which a scheme can match while misplacing its cooling by 10 W/m² in a layer":
  radiation intercomparisons check cooling profiles beside fluxes for that reason; a citation (Ellingson et al.
  1991, to verify) and the layer-by-layer framing as a check would fit.
- Abstract, "hold near the columns they were fitted on", and Reach, "Earth alone has conditions near those on which
  the adapted models' fits were made": general points stated as findings; the measured magnitudes are this work's.
- Introduction, "every lunar climate number is therefore a conditional model result": "therefore" could go.
- Results, "which arrangement the storms take therefore depends on laboratory laws": Mansell et al. (2005), in
  `references.bib`, showed simulated charge structure changing with the charging scheme and is uncited.
- Results, the waves "4–5 times as high as on Earth": Ghafoor et al. (2000), Lorenz and Hayes (2012) and Hayes et al.
  (2013), in `references.bib`, treat gravity in wind-wave growth on Titan and are uncited.
- Assumptions leaves the capillary length uncited, and Reach and the regime table's caption name Chapman's factor
  without citing `chapman1931absorption`.
