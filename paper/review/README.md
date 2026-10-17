# Review records

The records of every review made on the paper, by whom and with what findings, following the editorial
charter's gates (G1–G7), its ten separate prose passes and its release integrity rule (E4). A record
states what was done; a pass listed here was performed, and a pass not yet performed is marked pending.

## Reviewers

| Reviewer | Role | Records |
|---|---|---|
| Claude Opus 5.5 (the drafting assistant, main session) | Drafted every section; performed the ten prose passes per section in sequence after drafting, each pass read for its own question | `passes_<section>.md` |
| Claude subagents acting as technical referees | Checked every claim and table row against its sources; read-only | `referee_technical_part1.md`, `referee_technical_part2.md` |
| The author | Audible cadence review, author resolution of exceptions, competing-interest declaration | pending |

The same assistant drafted and reviewed the prose, so the passes are self-review recorded as such. Cadence
was reviewed silently; the audible review the charter requires for major transitions, the conclusion and
dense passages is pending and is credited to no one until performed.

## Files

| File | Holds |
|---|---|
| `passes_<section>.md` | The ten passes for one section: findings by line, dispositions, before and after where a passage changed |
| `referee_technical_part*.md` | The technical referees' claim-by-claim findings and their dispositions |
| `whole_manuscript.md` | The whole-manuscript challenge, after the section passes |
| `release_register.md` | PASS / BLOCKED / DEFERRED by gate, with the exact PDF and source hashes |

The automated checks (`tools/check.py`, `tools/lint.py`) establish record completeness and list candidate
places; they clear no gate.
