# Editorial round 18: the lakes beneath the waves, and the note on terms, 19 October 2026

Kept by Claude Opus 5.5, the drafting assistant.

## The author's directions

The author's Terluna project added one-dimensional lake and sea studies on 17–18 October (oxygen, anoxia, kinds of
lake, methane and the seas' oxygen), forced by the GCM, with gas exchange and deep mixing from laws fitted on Earth's
lakes; at lunar gravity the same warmth resists the wind's mixing about six times more weakly. The author asked
whether any of it belonged in this paper. The assistant advised keeping the results and their numbers in Terluna,
since this paper's subject is the model ensemble and Terluna enters as provenance, and adding one forward-looking
sentence in Next steps and a phrase in the Conclusion, framing lake and sea columns as a use of the ensemble's winds
and sea states whose transfer and mixing laws are Earth fits to test. The author agreed, and asked in the same
message that the Introduction's opening paragraph, the definition of Gaean worlds, move above the Introduction as a
note: "It's not a good start to an introduction. It is indeed a note."

The revision follows the order of synthesis in `AGENTS.md`: the body (Next steps), then the Introduction (the note),
then the Conclusion; the abstract needs no change for either direction. Each stage has a light reading by one fresh
Claude Opus 5.5 subagent, and a closing review reads the whole paper.

## Stage 1: Next steps (e6174ba)

One sentence closes the paragraph on the seas' Earth laws. Verdict: two MINOR fixes, content ready. The reader
found the physics right (buoyancy g·α·ΔT), "fitted on Earth's lakes" fair against Terluna's lake model (Cole and
Caraco's transfer, the General Lake Model's energy balance, Earth's measured share of the wind's energy), the
sentence in keeping with the paragraph, and the lake results kept out.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1 | `next.tex`:123 | "And" joined the gravity point to its consequence as equals, leaving the reason for testing the laws unwritten | Applied: "since at lower gravity a given contrast of temperature resists the wind's mixing more weakly, the transfer and mixing laws ... would be ..." |
| 2 | `next.tex`:124 | "Would join the Earth values" gave the laws an action | Applied: "would be among the Earth values to test" |

## Stage 2: the note on terms (bce55ed)

The Introduction's opening paragraph moved, word for word, into `paper/sections/terms.tex`, set between the abstract
and the Introduction as a small, indented "Note on terms." Verdict: ready. The reader confirmed the wording identical
to the removed paragraph, the note set like the abstract with a run-in head like the paper's others, the Introduction
opening on the field as `AGENTS.md`'s table of repairs directs, "Gaean" in the body used only after the note, nothing
pointing back to the removed paragraph, and the check script covering the new file.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1 | `terms.tex`:5–7 | The note's closing clause, "so modelling their climate, storms and seas requires adapting both the component models and the fields exchanged within an ensemble", is argument more than a term, and echoes the abstract printed above it | For the author: the note could end at "... may differ substantially from Earth's."; it stands as the author moved it |
| 2 | `paper/Makefile`:10–13 | A build made before a commit keeps the earlier commit's date, and latexmk then skips the rebuild | Noted for the records: every recorded hash comes from `make -C paper clean` followed by `make -C paper pdf` |
