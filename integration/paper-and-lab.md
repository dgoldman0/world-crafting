# The first integration: the paper and the lab, 8 November 2026

Three states of the work became one on 8 November 2026: main at `04a6c27` (18 October), the paper's branch
`paper/conclusion-development` at `4d041bc` and the lab's branch `lab` at `b4e091d`. Both branches had left main at
`04a6c27`, the paper's 97 commits ahead and the lab's 39, so main held neither the released paper nor the lab. The
round ran on the standing branch `maintenance/integration`, in `../world-crafting-integration`.

## The commits

| Commit | What it does |
|---|---|
| `4d163db` | Merges the paper's branch, of which main is an ancestor |
| `0bd4d8a` | Merges the lab's branch; Git joins the three files both branches changed without conflict |
| The round's commit | The integration procedure in `AGENTS.md`, the plan in `PLAN.md`, the README's layout and this record |

## How the shared files were joined

Both branches had changed three files since `04a6c27`. In `AGENTS.md` the paper's branch had brought the framing of
Gaean worlds and the rule that commit messages quote the author nowhere, and the lab's branch its rules on the lab's
own runs and store, the row for Fortran in the in-house tools and the row for the lab. In `README.md` the lab had
added its row to the layout table, and in `notes/exoplasim.md` the notes on its patch 11. Git combined each file,
and read through, each holds both branches' entries as one text. The root README's row for the lab described it at
its design stage, and this round gives its builds and runner. `notes/cm1.md`, `notes/defect_log.md` and
`notes/verification_record.md` were the same on both branches.

## Checks

On the merged tree, `make check` applied every patch series to its pinned source and reproduced its builds'
sources, and the Python tests gave 473 passed and 1 skipped. `make paper` built the PDF of the first released draft
byte for byte, SHA-256 `1ce697ac…f871`, so the merge leaves the paper as released.

In the integration's worktree, the pinned upstream sources and three input folders are linked: the upstream
sources and the waterworld inputs from the main and lab checkouts, the radiative-convective inputs from the lab's
copy, and the middle atmosphere's from Terluna's. The electricity inputs, the radiative-convective cache and the
lab's `local.toml` are copied.

## The review

One fresh reviewer read the round's commit and the three merged files against the direction for the round, the
decisions the plan carries and the writing rules, and checked the plan's numbers against Terluna at `bdda5a07`. It
confirmed the decisions, the numbers, the cited commits and paths, and the merged files' coherence, and it raised
three findings, each answered in the plan:

| Finding | Answer |
|---|---|
| The plan's count of five defects read as if CM1's gust over water made the fifth | The count stands at five, the first version's four and the simple boundary layer's density fault (A9), as `notes/defect_log.md` and the root README record it. Both passages name A9 as the fifth and the gust as an Earth value |
| The defect log's states for B29–B34 ran as a string of fragments | A list, each entry with its name |
| The turn's 1.9° lacked its condition | It comes with a shallow mantle as warm as the warmest published profile, within about a thousand years, and the measured heat flow favours the cooler profiles |
