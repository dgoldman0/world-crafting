# Editorial round 14: whole-manuscript prose and framing

Reviewer: fresh Codex reviewer agent `/root/round14_whole_prose`.
Date: 2026-10-18.
Activity: full silent reading of the frozen manuscript, followed by review of the current working diff and the two changed lines in the figure script. The manuscript remained unchanged throughout this review.

## Author direction and review scope

The controlling direction supplied to this reviewer was:

> Terracompatible is a good one. The conclusion is quite good except it should use terracompatible instead of Earth-like and just maybe one sentence best place just so it’s clear that the ensemble could also eventually be useful for modeling other worlds beyond just terracompatible ones and the ensemble work gets us closer to that too. Other than that the conclusion is good.

The accompanying direction requests an early definition and a whole-manuscript check of terminology and central framing. The purpose is development of a model ensemble for exoplanets and constructed worlds; the Moon supplies the worked evidence and Terluna its provenance. The author's acceptance of the Conclusion confines revisions there to the term replacement and the single prospective sentence.

I read `AGENTS.md` and the four required editorial controls in full before the manuscript. I then read `paper/main.tex` and every file in `paper/sections/`, in manuscript order, including captions, tables, appendix and availability material. This was one continuous source reading across tool calls. I opened no past-draft or review files. After that reading I examined the working diff to identify the changed prose and the figure-label change, and read the complete `fig_regimes` function with its helper and imports.

The review covers terminology, the model-ensemble frame, paragraph and section movement, and the changed prose. Cadence was assessed silently. External source admission, numerical revalidation, the historical review counts in Availability and exact-build visual clearance remain outside this review's evidence. No automated prose linter or test suite was run by this reviewer.

## Findings requiring correction

| ID | Severity | Location | Finding and correction |
|---|---|---|---|
| R14-P1 | Minor copy correction | `paper/sections/introduction.tex:12–13` | The composition replacement produced “placed an nitrogen--oxygen atmosphere”. Change the article at line 12 to “a”. The cited world's stated composition and the paragraph's argument remain unchanged. |

No substantive blocker was found in the requested terminology and framing scope. No optional rewriting is recommended for the author-approved Conclusion.

## Reading findings

The title and abstract identify development of an ensemble for climate, storms and seas as the contribution. The abstract defines terracompatible at first use, then proceeds from planetary departures to the lunar adaptation, its checks and sensitivities, and the next radiation and cloud work. Its wording “As a start toward that ensemble” and its sole-away-from-Earth-case qualification preserve the distinction between the purpose and the tested implementation.

The Introduction's opening definition specifies nitrogen–oxygen air, water as the principal condensable, broadly terrestrial surface pressures and temperatures, liquid surface water and an active water cycle. Its second sentence makes the differing gravity, size, rotation and starlight the reason for adapting the models and exchanged fields. The next paragraphs develop that premise through scoped examples from the literature, constructed worlds, retained Earth values, and the actual coupled calculations. “We use” introduces a term whose meaning determines the paper's scope. The early definition earns its place for the expert audience.

The distinction between the physical class and the implementation's range remains explicit in `reach.tex:73–82`: Titan, Mars and Venus require further radiation and condensation physics, while the following restrictions apply within the terracompatible class. The illustrative worlds in `worlds.tex:10–14` and its figure caption are described by their actual held parameters. The nitrogen-dominated and oxygen-free cases cited in the Introduction and Results retain their stated compositions. The manuscript uses them as related modelling examples, preserving their distinction from the defined nitrogen–oxygen class.

Across the main development, the four planetary ratios motivate the inventory of Earth values; the inventory determines the repair classes; Verification distinguishes code checks, fitted agreement and Earth benchmarks; and Results measures the effects on the worked case. The opening of Reach then converts those distinctions into operations needed for another world. This order has inferential work: moving Reach ahead of the evidence would remove the measured basis for its separation of general repairs, computed tables and calibrations. The catalogues of configurations, switches and checks are explicit tables or method passages.

The revised opening of Next steps links the shared radiation reference, consistency between global and resolved calculations, and tests across planetary parameters. Its local experiments specify the process or approximation being tested and the consequence of the outcome. The added drop-size sentence makes the microphysical comparison's cross-world purpose explicit. These passages keep the lunar experiments connected to development of the ensemble.

The Conclusion uses terracompatible in its opening and preserves the author-approved development. The single added sentence at `conclusions.tex:64–65` follows the need for additional physics, names radiation and cloud microphysics for other gases and condensables, and states the extension prospectively through “could”. Its placement follows from the preceding comparison across planetary cases and leaves the terrestrial-experiment paragraph's opening reference to those cases intelligible. The diff contains the term replacement and this one sentence as the Conclusion's entire substantive change.

Terluna occurs as the source of the case, code, records and AI-assistance history, with the accepted Conclusion's brief attribution of the breathable Moon. The abstract, opening and Conclusion concern the same model ensemble. A screening search after the reading found zero occurrences of `Earth-like` or `Earth like` in `main.tex` and the section sources; this search confirms vocabulary coverage within those files and adds no source-admission evidence.

## Ordinary review of the figure-script diff

The diff in `paper/figures/figures.py` changes exactly two text lines: the comment at line 28 and the annotation string at line 62. The replacement label, “Earth parameters, longer days”, agrees with the held-parameter explanation in the manuscript and caption. The conditional, data selection, coordinates, marker properties, axes and save call retain their operations. No code correction is required for this diff. This is a source-diff review; the rendered figure and final PDF require their own visual review.

## Bounded readiness judgment

After R14-P1's article correction, the terminology and ensemble-framing revision is ready for the author's reading within this review's scope. The frozen Conclusion already carries out the author's two requested changes. This judgment records the reading performed here; source admission, physical validation and release clearance require their own evidence.

## Exact inputs

SHA-256 values identify the bytes read before any correction from this report.

| File | SHA-256 |
|---|---|
| `paper/main.tex` | `09ddc294b8a441ff534e9533760d93660d4fac677470d16240b50d4ab2b7b04a` |
| `paper/sections/abstract.tex` | `db3ca84e02f667d08628e9bae52969b95c338607ecbdaf67c2c07ad20b3a2a85` |
| `paper/sections/introduction.tex` | `a5652b8fb1e671994157720010940850bf04450d6190e5ee43d92a83d7f3c23a` |
| `paper/sections/worlds.tex` | `97c0952df1a968079e8033e10320c1c7b1b383632ac11c310f13a2f502de8623` |
| `paper/sections/assumptions.tex` | `77bc704fe58d964ff2567a39ffbdf6e2af9b0cc422bfb88e04d25e949b877107` |
| `paper/sections/repairs.tex` | `c846dbbf4dbaf39ae194d7bb93a26204aaa1b12f4b24e7aa1accdd948b281102` |
| `paper/sections/verification.tex` | `4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00` |
| `paper/sections/results.tex` | `fcbef4a5eb6874fe1bb923eff8c42a356a0c56a6d60f28f210934cc4caa473eb` |
| `paper/sections/reach.tex` | `09354c0ec1ee5e62ab86cffbd922995cfe1658f6ec0f7c07a45f0d6fa8235bd6` |
| `paper/sections/next.tex` | `94f6ee4626048b283736456078691007340767e321a7cf2786e6c62ad4a3cfdf` |
| `paper/sections/conclusions.tex` | `0916f8f0315fdcae73a93f17a04b2a90d19d19d36da1e6c04b8967908764f277` |
| `paper/sections/appendix.tex` | `17abe050d20a86031b7f3b1e426afcca0050cb9928bdb6500d84850d73013bbc` |
| `paper/sections/availability.tex` | `425bfcee91cf0a18ffca0855eb613f5f269a99ac9cb66b9b9a8a7c68ee90a7d7` |
| `paper/figures/figures.py` | `f18e20731c6f076b955df863252ddf87e5bd31a5f1fd497d40483c930cf5b308` |
| `AGENTS.md` | `9ff1dafe482f1d47627d8734eae489905513896496abe474047694b80d1aa2c1` |

The following control paths are relative to `/home/kir/Documents/Projects/terluna/ensemble/planning/`.

| Control | SHA-256 |
|---|---|
| `Open_Moon_Editorial_Charter_control-01.md` | `aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0` |
| `source_controls/STYLE_NOTES.md` | `659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46` |
| `source_controls/Jewish_Papers_Updated_Style_Notes.md` | `18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab` |
| `source_controls/Agent_Working_State_Editorial_Gates.md` | `553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464` |

## Disposition verification, 2026-10-18

The same reviewer performed a bounded follow-up on the four reported changes. R14-P1 is closed: the Introduction now reads “placed a nitrogen--oxygen atmosphere”. The Conclusion's prose remains identical to the frozen reviewed version; its changes remove `\enlargethispage{2\baselineskip}` and insert `\needspace{3\baselineskip}` before the penultimate paragraph. Those commands concern pagination, whose rendered effect belongs to visual review.

Availability now records round 14's two-agent whole-manuscript reading and the completed article correction, retaining the distinction between the author's acceptance and the agents' silent cadence reviews. The account matches this reviewer's actual reading and finding; the composition source checks are part of the round's combined activity. The wording “The paper's central purpose” in `AGENTS.md` makes the purpose statement's subject explicit.

For each of these four files, reversing only the reported edits in memory reproduced its frozen SHA-256 above. Recomputed hashes of `main.tex`, the remaining section files and `figures.py` match the original input table. This check verifies the stated change boundary.

The requested terminology and ensemble-framing scope is ready for the author's reading. This follow-up adds disposition verification to the original full reading; its evidence remains bounded to that scope.

| Changed file | Final SHA-256 |
|---|---|
| `paper/sections/introduction.tex` | `cde16ec94a7e376fb1a34043f7118d24d95cedba9071f527ae071799f8cb7898` |
| `paper/sections/conclusions.tex` | `4663c7a2c64163ca8de355fb2b11631547e11a51a25d49374845ba0c0d1ae2a7` |
| `paper/sections/availability.tex` | `7c258ecc5a01304a12a797b0cb2bda19b3c2ea08b4faa76a42243838f7a575b6` |
| `AGENTS.md` | `c445cf51a745325343989ce4043504db82bc2a0decef255efd5a7478cb9228ac` |

The final hashes of every other manuscript file and the figure script are the unchanged values in the original input table.
