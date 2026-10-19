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

## Stage 3: the Conclusion (904c4a3)

One clause entered the sentence on rain, the sea and the waves: "and the same winds and waves, mixing the lakes and
seas, would drive the exchange of oxygen between their waters and the air". Verdict: one MINOR fix, content ready.
The reader found that the clause ends the sentence on the waters it began with, claims no oxygen content (only the
exchange the winds and waves drive), adds no numbers, and agrees with Next steps, which states the Earth-fit
condition once.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1 | `conclusions.tex`:95 | Three coordinated clauses read as a list, though the waves at the shore follow from the forced sea | Applied: "would force the sea, whose spectra would determine the waves reaching a particular shore, and the same winds and waves, ... would drive ..." |

## Stage 4: the abstract

No change: the abstract's account of the ensemble and its prospect already covers the seas, and the note on terms
leaves the abstract's own definition of Gaean worlds in place.

## Closing review (ffdedfe)

Two fresh Claude Opus 5.5 subagents read the whole paper, one for prose and the author's direction
(`editorial_round18_closing_prose.md`: 0 BLOCKING, 0 MAJOR, 6 MINOR) and one for evidence and scope
(`editorial_round18_closing_evidence.md`: 0 BLOCKING, 0 MAJOR, 7 MINOR), each reporting what the revision caused or
touched and anything blocking elsewhere.

### For the author's decision

The author read these four and agreed with each; all four were applied as proposed on 19 October 2026.

| Finding | Wording | The reader's proposal |
|---|---|---|
| Prose F1 | `terms.tex`:5–7, the note's closing clause, "so modelling their climate, storms and seas requires adapting both the component models and the fields exchanged within an ensemble" | End the note at "... may differ substantially from Earth's."; the clause states for the third time what the abstract says above it and the Introduction reaches with evidence. Stage 2's reader proposed the same |
| Prose F2 | `terms.tex`:3, "We use \emph{Gaean} for worlds ..." | The paper's only first person; elsewhere the author is "the author", and "we" could be read to include the AI assistants: "Worlds with ... are named \emph{Gaean}." |
| Evidence 4 | `conclusions.tex`:12–14, "Run together, the global and resolved calculations could follow a change ..." | Every coupling in the body is one-way and offline, so "Run together" can read as two-way coupling: "Chained through their forcing, ..." |
| Evidence 5 | `conclusions.tex`:27–29, "its radius and atmospheric column determine a new curved-air table, while its spectrum and columns determine the targets for the radiation fits" | The table's sunlight terms were computed with the shield-filtered spectrum, so another star needs its own table: "its radius, atmospheric column and starlight determine a new curved-air table, ..." The same gap in the body was closed (below) |

### Prose (`editorial_round18_closing_prose.md`)

| Finding | Disposition |
|---|---|
| F1, F2 | For the author (above) |
| F3 | Applied: Next steps' overview now names "the lakes and seas beneath the waves" among the approximations its experiments test |
| F4 | Applied with evidence 1–3: "one-dimensional models of the lakes and seas, which would compute their mixing and their exchange of gases with the air", and "the gas-transfer and mixing laws such models take" |
| F5 | Applied with evidence 1: the exchange of oxygen has a sentence of its own, "Mixing the lakes and seas, the same winds and the waves they raise would drive the exchange of oxygen between the waters and the air", and the accepted "and its spectra would determine the waves reaching a particular shore" returns |
| F6 | Applied with evidence 6: the review history in Availability and `README.md` records that round 17's five findings were applied once the author had read them, and records this round |

### Evidence (`editorial_round18_closing_evidence.md`)

| Finding | Disposition |
|---|---|
| 1 | Applied: the lake and sea models are forced by "the GCM's winds and surface heat fluxes, with SWAN's sea states over the seas"; in the Conclusion the lakes take "the waves they raise", their own |
| 2 | Applied: "fitted on Earth's lakes and seas" |
| 3 | Applied: "and so would the one-dimensional form itself", since weaker stratification gives basin-scale motions more weight; the paper's fourth form of Earth value covers such a simplification |
| 4, 5 | For the author (above); for 5, the body's two statements now recompute the curved-air table "from that world's own column and starlight" (`repairs.tex`:113, `reach.tex`:6), checked against `python/climate/gcm/twilight.py`, which builds the table's sunlight from the shielded spectrum |
| 6 | Applied with prose F6 |
| 7 | Applied: "for an estimated 70 million years or more", from Needham and Kring's "may have taken ∼70 million years to fully dissipate" and "The actual duration of the atmosphere may exceed this estimate", read in the archived original and recorded as a locator and use in the manifest |
