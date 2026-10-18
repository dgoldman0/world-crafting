# Conclusion centred on the model ensemble, 18 October 2026

## Author's review and direction

The author read the Codex conclusion recorded in `conclusion_rewrite_2026-10-18.md`, whose final TeX
hash was `a151c8a9af9a67d7af82e64f5a4d36de90f3c0380b1d99e53f5c194da31cb815`, and rejected its framing:

> This is still not right. You probably don't have the claude memory notes or maybe it didn't include it but the core should not be about this Moon. Did we not set up a central position of this paper about an ensemble that can work with broader exoplanets and constructed worlds, where Terluna's work just gave us the start and shed light on issues with current systems?

This is an author's review. It supersedes the earlier record's statement that the author's reading comes
next. The earlier agent findings remain attached to their reviewed artifacts.

The drafting assistant read the relevant Claude memory notes in the author's local project memory:
`paper-standalone-field-framing.md`, `conclusion-as-discussion.md`, `author-direction-overrides-rules.md`,
`credit-prior-work.md`, `editorial-review-by-reading.md` and `world-crafting-lab.md`, with their index.
The framing note records two earlier rejections of Moon-centred framing. The lab note describes a separate
workstream; its planned implementation is kept distinct from the capabilities documented in the paper.
An independent Codex agent, `ensemble_scope_reading`, read the manuscript's framing and technical sections,
excluding the conclusion and previous reviews, and distinguished existing couplings from future work.

## Replacement and review scope

Codex replaced `sections/conclusions.tex` again. Its organising subject is the model ensemble for Earth-like
exoplanets and constructed worlds: the connection between scales, consistent physical parameters,
radiative reference calculations, calibration through resolved clouds, comparative planetary tests,
and the environments that could be investigated or designed. The lunar work supplies starting evidence.
AGENTS.md now states this central purpose and distinguishes the model ensemble from Terluna's five papers.

The replacement was committed before review at `f8da448`. Its frozen copy is
`drafts/conclusion_round13.tex`, SHA-256
`cd56eada14d0af03138008f1107afa6449a8741475e9326f10cab0a52f6cc97b`.
AGENTS.md at that snapshot has SHA-256
`bb2301a81fe73cfd272ee55cb8b8c9162962d1df3fa9913def2e995e36d5c6e5`.

Fresh Codex agents `conclusion_round13_prose` and `conclusion_round13_evidence` received the author's latest
correction and earlier direction about development across paragraphs, sustained excitement and an ending
of pure inspiration, in the author's words. They were directed to judge that direction first and to read
the whole conclusion with its context. The frozen text remained unchanged while they read it. Their
records identify their read sets and findings.

## Dispositions

| Finding | Revision |
|---|---|
| Prose F1: the Introduction still frames the contribution around finding Earth values and transferring repairs | Its purpose statements now connect those tasks to developing an ensemble from global climate through resolved storms and coastal waves. The next paragraph identifies the lunar case as the start of those adaptations and couplings. The abstract's model list receives the same purpose. |
| Evidence E1: empirical microphysics described as the remaining physical limit of the cloud comparison | Replaced the exclusive claim with the reviewer's wording: CM1's empirical microphysics still limits the cloud target. The proposed calibration and its role in the broader ensemble remain. |

The drafting assistant also changed the illumination paragraph's general claim from “still changes” to
“can change,” preserving its status as a possible response across worlds. These are the only changes to
the reviewed Conclusion. Its final source hash is
`9e6e4ea705dee3a93352474dbec8c8eb1ca1a7c31f7c01ae64bacea0075ce36c`.
The revised abstract and Introduction hashes are respectively
`77f452b63c40f2e0c682b657c13fcb9ea4c0c1dcdddfa7e2ac0b2f43528adb22` and
`c40f7d58211ee6436673ebe9b74b52d4cff86c21c80831df131856e1d30e90f2`.

The original reviewers were asked to verify these bounded dispositions against the final source hashes,
with their follow-ups appended to their own records. Those follow-ups are distinct from a fresh round.
The author reads the revised Conclusion next, under the priority in AGENTS.md. The availability statement
and review index now record the author's rejection, the subsequent rewrite and the actual agent reviews.

Both reviewers verified their dispositions on the final hashes and recorded PASS within those bounded
scopes. Their initial judgments and the frozen draft remain preserved. The drafting assistant read the
revised section continuously after those local changes.

## Checks

- `make -C paper check` passed: 13 TeX files, 73 cited keys, 106 of 108 claims cited. Existing warnings
  concern the offline source record for H23 and N02 and the uncited S01 and V14 entries.
- `python3 paper/tools/lint.py paper/sections/conclusions.tex` screened one candidate, “this work” in the
  proposed radiation paragraph. It names the development just described. This was screening, followed
  by reading, and carries no editorial judgment.
- `git diff --check` passed.
- `make paper` built the 34-page PDF. Its source-commit build and visual inspection are recorded below.

The changes in this revision concern prose and review records. The software checks from the preceding
rewrite remain recorded in `conclusion_rewrite_2026-10-18.md`; model code and tests retain that state.

## Layout adjustment

The build after the opening's alignment placed the final sentence of the Conclusion on page 26, separated
from the rest of its paragraph. A local `enlargethispage` command adds two baselines on page 25. The drafting
assistant inspected the rendered page after rebuilding: the final paragraph now remains together and
retains separation from the page number. The reviewed wording is unchanged. The final source hash and
exact committed build are recorded with the visual inspection below.
