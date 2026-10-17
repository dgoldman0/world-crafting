# Review records

The records of every review made on the paper, by whom and with what findings, following the editorial
charter's gates (G1–G7), its ten separate prose passes and its release integrity rule (E4), and the writing
rules in the repository's `AGENTS.md`. A record states what was done; a review not yet performed is marked
pending.

## History

The first draft (17 October 2026, up to commit 6c8a68f) was framed around the Terluna project and titled
"Earth inside the models". The drafting assistant made the ten prose passes on it as silent self-review; two
technical referees checked its claims; a whole-manuscript challenger raised 5 blocking, 11 major and 21 minor
findings. The author then read it and rejected its framing and much of its prose: the paper is to stand alone
as a field paper on modelling Earth-like worlds beyond Earth's range, and its prose broke the writing rules
the author holds (empty actions on abstractions, witticisms, explaining the obvious, strings of declaratives,
a field characterised from four studies). The author's reading served as the cadence review of that draft.

The second draft (commit e018be0 and after) reframes the paper and rewrites every section to the rules now
written out in `AGENTS.md`, acting on the challenge at the same time. Its prose is judged by reading, in rounds
of fresh reviewer agents who see only the text and the rules, until a round finds nothing blocking; the
author's own readings are the decisive review.

## Reviewers

| Reviewer | Role | Records |
|---|---|---|
| Claude Opus 5.5, the drafting assistant (main session) | Drafted both drafts; silent prose passes on the first draft; dispositions | `passes_<section>.md` (first draft), `*_dispositions.md` |
| Claude subagents, technical referees | Checked every claim and table row of the first draft against its sources | `referee_technical_part1.md`, `referee_technical_part2.md`, `referee_dispositions.md` |
| A Claude subagent, whole-manuscript challenger | Challenged the first draft as a whole against G1–G5 | `whole_manuscript.md`, `whole_manuscript_dispositions.md` |
| Fresh Claude subagents, editorial reviewers | Read the second draft against the rules, by part and as a whole, round by round | `editorial_round<n>_<part>.md`, `editorial_round<n>_dispositions.md` |
| The author | Readings of the drafts, decisive on framing and prose; resolution of exceptions; the competing-interests declaration | First draft read 2026-10-17 (framing and prose rejected; served as its cadence review) |

Every reviewer above except the author is the same model as the drafting assistant, so none of these records
is independent review in the sense of a person or a journal; each separate pass is recorded as such.

## Files

| File | Holds |
|---|---|
| `passes_<section>.md` | The first draft's ten passes for one section (historical; the sections were rewritten) |
| `referee_technical_part*.md`, `referee_dispositions.md` | The technical referees' findings on the first draft and what was done with each |
| `whole_manuscript.md`, `whole_manuscript_dispositions.md` | The whole-manuscript challenge of the first draft and its dispositions in the second |
| `editorial_round<n>_*.md` | Each editorial round's records by reviewer, and the round's dispositions |
| `release_register.md` | PASS / BLOCKED / DEFERRED by gate, with the exact PDF and source hashes |

The automated checks (`tools/check.py`, `tools/lint.py`) establish record completeness and list candidate
places for reading; they clear no gate.
