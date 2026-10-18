# Editorial round 15: dispositions

The flow findings of round 15 (`editorial_round15_flow_opening.md`, `editorial_round15_flow_middle.md`,
`editorial_round15_flow_closing.md`) are acted on section by section, at the author's direction, and each section
goes to the author before the next. Kept by Claude Opus 5.5, the drafting assistant, from 18 October 2026. A
finding marked applied took the reviewer's sample rewrite or one-line repair; where the text differs from the
proposal, the reason is given.

## Abstract (opening record, F01–F03)

Acted on in commit 9d555e6, together with the abstract's new opening.

| Finding | Disposition |
|---|---|
| F01 | Superseded: the new opening sets out the worlds in plain words, then the two problems, with the author's concessive and additive turns. |
| F02 | Applied: "though they produce little or no error at Earth's values". |
| F03 | Applied in part. "With the repairs in place" opens the checks and "Applied in the lunar runs" opens their effects on the climate; a hinge sentence names the two Earth fits revisited next; "Water cloud, in turn" marks the second plan. The proposal kept "whose climate is unobserved", which the author had judged defensive; "Applied in the lunar runs" replaces it. |

## Introduction (opening record, F04–F13)

| Finding | Disposition |
|---|---|
| F04 | Applied: "For such work, by the account of THOR's developers, …". |
| F05 | Applied: "for". |
| F06 | Applied: the Moon and Titan follow the Solar System's clause, the exoplanets close in a sentence of their own, and "An engineered world, by contrast" marks the turn. |
| F07 | Applied, folding in the proposal's "one such world": the Open Moon "is a design of that kind for the Moon". |
| F08 | Applied: "Modelling such worlds means adapting codes like those named above, and the developers who ported …". |
| F09 | Applied with "but", "then", "because", "moreover" and "therefore", and one addition from the abstract: the ensemble's models were built separately and tuned to Earth in different ways, so the Introduction and the abstract set out the same two problems. |
| F10 | Applied: "Toward such an ensemble". |
| F11 | Applied: "whereas". |
| F12 | Applied: "Alongside these couplings". |
| F13 | Applied, with "therefore" in place of the proposal's "Even after these repairs", which read as a caveat; the last two sentences are joined so that the conditional state follows from the fits' weight. |

## Worlds (opening record, F14–F20)

| Finding | Disposition |
|---|---|
| F14 | Applied: "Along these four ratios". |
| F15 | Applied as proposed. |
| F16 | Applied: "As modelled, …". |
| F17 | Applied as "In this scenario's air, every absorber path is longer …", since the proposal's "With this scenario's …" would open two sentences in a row on "With". |
| F18 | Applied, with "The curvature matters because the air is tall" in place of "The curvature comes from the air's height". |
| F19 | Applied as proposed. |
| F20 | Applied with a different bridge, "The solar day sets the scale of time as gravity sets that of height", which takes up the pairing of the section's opening; "The rotation is nearly as slow" and "The tilt, by contrast, is small" follow. |

## Assumptions (opening record, F21–F30)

| Finding | Disposition |
|---|---|
| F21 | Applied as proposed. |
| F22 | Applied as proposed; the other constants now form a paragraph of their own, and `\claim{H05}` precedes `\claim{H03}`, each beside its claims. |
| F23 | Applied: "CM1 keeps Earth's day as well". |
| F24 | Applied, with the bridge as a short sentence of its own: "The test world's air is far taller." |
| F25 | Applied: "Beyond the gases". |
| F26 | Applied as a separate Earth value: "Moreover, the relative-humidity threshold above which it forms cloud in each layer was set for Earth". |
| F27 | Applied: "but". |
| F28 | Applied: "The first is the Sun clock" and "The second lies in Slingo's convective cover". |
| F29 | Applied: "whereas". |
| F30 | Applied: "although". |
| Also | In the same paragraphs, three semicolons that hid a consequence or an addition now read "so that", "so" and "PlaSim's longwave errs by height as well", and CM1's thread race opens "CM1's defect is a race between threads". |

## Repairs (middle record, findings 1–16)

| Finding | Disposition |
|---|---|
| 1 | Applied with 4: the record of the patch series moves into Switches and builds. |
| 2 | Applied, with a different bridge: Switches and builds now stands between the rule and the classes, so the paragraph opens "Whatever their switches, most repairs fall into three classes". The definitions take "since", "therefore", "One step nearer the world" and "by contrast"; "A second convention" and "Beyond the three classes and the settings" mark the turns. |
| 3 | Applied as proposed: the range of the three ExoPlaSim repairs sits beside them, the calendar and SWAN's avoidances are grouped as avoidances by configuration, and "however" marks the two faults left open. |
| 4 | Applied: Switches and builds follows the rule directly. The folded record keeps every detail of the old sentence: pinned upstream archives, each change's switch or condition, its default and its checks, and the released settings listed beside them. |
| 5 | Applied: "Because gravity enters the fall-speed laws …". |
| 6 | Applied: "whereas". |
| 7 | Applied, except that "the repairs follow the sixfold stretch" would give the repairs an action; the text reads "CM1's Rayleigh damping rate and its boundary-layer length are scaled with the sixfold stretch of the dry dynamics". |
| 8 | Applied as proposed, grouped by code; `\claim{R16}`, which covers the soil, the flash log and the cloud water, follows the cloud-water clause. |
| 9 | Applied: "Both atmospheric models, PlaSim and CM1, take the curved geometry from the general method, …". |
| 10 | Applied: the appendix pointer sits beside the channels, and "The infrared escape, for its part" marks the parallel. |
| 11 | Applied as proposed. |
| 12 | Applied: "In a third step". |
| 13 | Applied: "To place that cooling by layer" and "although it runs only in the longwave test". |
| 14 | Applied: the leakage keeps its own sentence, and the ground strikes open on their reason. WRF-ELEC's two Earth rules bracket them widely on the Moon: under the stopping field every lunar channel stops 15–25 km up, while the −7 °C rule alone counts every channel that reaches that level, as Assumptions sets out. |
| 15 | Applied, with "The bound sits between them". |
| 16 | Applied with one change: the proposal filled stock CM1's absences "from the same fields", yet the Sun and the Coriolis parameter come from CM1's own set-up; they are "filled in turn". "While on the 45° N ring" marks the second absence that showed, and the seas open "Beyond the storms, the seas take their forcing from the GCM as well". |

Checks: a script found the numbers, inline mathematics, citations, cross-references and claim markers of
`repairs.tex` identical before and after; `make -C paper check` passed with its existing warnings; the PDF built at
35 pages with zero overfull boxes, and pages 9–14 were read. Page 13 now ends about six lines short, with
Verification opening page 14.
