# The second integration: the porting decisions, 8 November 2026

Main at `de52271` took one commit from each line of work: the paper's branch at `32cde03`, which moves the paper's
version 2 onto the paper's branch in the open, unreleased until the CM1 results are realigned, and the lab's branch at
`ac78c97`, which weighs Terluna's fixes for the lab in `lab/design/terluna_fixes.md`. The round writes the decisions
taken before the fixes are ported into `PLAN.md`, under "Decisions", and gives each fix's confidence, form, cost and
what it waits on in a new section, "Porting: confidence, form and cost".

## The commits

| Commit | What it does |
|---|---|
| `c68e182` | Merges the paper's branch |
| `95836ff` | Merges the lab's branch |
| The round's commit | The porting decisions in `PLAN.md`, and this record |

## How the shared files were joined

Only `PLAN.md` changed in more than one place: the paper's branch moved version 2's drafting onto that branch, and the
round adds the decisions, the porting table and the order of the ports, in other passages.

## Checks

On the merged tree, `make check` applied every patch series and gave 473 passed and 1 skipped, and `make paper` built
the released draft's PDF byte for byte, SHA-256 `1ce697ac…f871`.

## The review

One fresh reviewer read the round against its direction, the decisions and the writing rules, and spot-checked the
porting table against `lab/design/terluna_fixes.md`. It confirmed the decisions and the numbers it checked, and
raised three findings, each answered:

| Finding | Answer |
|---|---|
| This record's opening chained the decisions as a string of equal clauses | It names the sections of `PLAN.md` that hold them |
| The first row's 0.01 K/day differs from the 0.013 K/day cited elsewhere | The two figures compare CM1 with different codes; the row names both comparisons |
| The twilight row's 1.0–1.2 K of cooling went beyond the cited source | About 1 K, as the source gives it |
