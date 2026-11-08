# The second integration: the porting decisions, 8 November 2026

Main at `de52271` took one commit from each line of work: the paper's branch at `32cde03`, which moves the paper's
version 2 onto the paper's branch in the open, unreleased until the CM1 results are realigned, and the lab's branch at
`ac78c97`, which weighs Terluna's fixes for the lab in `lab/design/terluna_fixes.md`. The round writes into `PLAN.md`
the decisions taken before the fixes are ported: components run when a study calls for them, with cost and checks
reported before compute; the Earth control decides which fixes serve every world; level sets follow each world's scale
height; carried weather is an option; the unified interface gets its own design step; and the porting table gives each
fix's confidence, form, cost and what it waits on.

## The commits

| Commit | What it does |
|---|---|
| `c68e182` | Merges the paper's branch |
| `95836ff` | Merges the lab's branch |
| The round's commit | The porting decisions in `PLAN.md`, and this record |

## How the shared files were joined

Only `PLAN.md` changed in more than one place: the paper's branch moved version 2's drafting onto that branch, and the
round adds the decisions, the porting table and the order of the ports, in other passages.
