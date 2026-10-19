# Round 19: the paper's account of its own making, 19 October 2026

Kept by Claude Opus 5.5, the drafting assistant.

## The author's direction

Reading the paper after Codex's final skim (`final_skim_2026-10-19.md`, which passed the manuscript at e7c1c66),
the author objected to its Availability section: "Why.. would you include review history in the paper itself?
There are a few other things that are just stupid as well. This paper is a standalone paper.. That's kind of
almost embarassing. Nobody logs a review history of the paper writing process itself in the paper.. Who does
that?" The assistant traced the history to AGENTS.md's line that final releases carry "the actual review history",
which the agents had read as the manuscript, and proposed five changes: delete the review history; cut the account
of assistance to a brief AI-use statement pointing to the repository; trim Code and data to where things are; cut
Next steps' list of reports and reruns to the issue already filed; and fix the rule in AGENTS.md. The author: "You
spotted more than I did so far so let's start by fixing those places." The changes below therefore follow the final
skim, whose statement that the manuscript remains as reviewed no longer holds.

## The changes

| Commit | Change |
|---|---|
| ec8140e | Next steps loses "Reports and the record", a list of issues to file and reruns to make; the Sun clock's report stays where Repairs cites it, now with claim N02 |
| e29789c | The review history leaves the paper; "Author and assistance" becomes a short statement of AI assistance; Code and data says where things are; the section becomes "Availability and declarations", about 380 words from about 1,500; AGENTS.md now says the paper carries what a journal paper carries, with the review and drafting history in `paper/review/` |
| c8a1731 | The light reading's fixes, below |

## Light reading (ec8140e, e29789c)

One fresh Claude Opus 5.5 subagent read both commits. It found no remaining account of the paper's making in the
rendered text beyond the code-and-data and AI-use statements a journal paper carries. Verdict: one MAJOR, six MINOR.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1, MAJOR | `verification.tex`:127–128 | "The checks still open are taken up with the next steps" became untrue for three checks that only the cut list took up | Applied: the sentence is dropped, since each open check is stated where it arises |
| 2 | `availability.tex`:19–20 | Claude "drafted the text" and Codex "reviewed parts of the text" disagreed with the records: Codex drafted the present conclusion, revised the terminology across the manuscript, read it whole in round 14 and the final skim, and in Terluna reviewed research branches | Applied: "drafted most of the text"; "OpenAI's Codex drafted the conclusion, revised and reviewed the whole text and, in Terluna, reviewed research branches of the code" |
| 3 | `availability.tex`:22–23 | The records of the assisted code and analyses are in Terluna as well | Applied: "The records of this assistance are kept in the Terluna and world-crafting repositories, those of the manuscript's reviews in world-crafting." |
| 4 | `availability.tex`:6 | "A register tracing each number in the text" claimed too much; cited studies' numbers and proposed runs' settings lie outside it | Applied: "a register tracing the work's own numbers to their sources" |
| 5 | `availability.tex`:19 | Claim Z01 became uncited | Applied: `\claim{Z01}` after "most of the code and analyses" |
| 6 | `availability.tex`:12–13 | SWASH 12.01 was listed among the patched sources; it runs unmodified (`models/swash/README.md`) | Applied: "SWASH 12.01 runs unmodified from its pinned archive" |
| 7 | `paper/review/README.md` | The history ended on the final skim's "the manuscript remains as reviewed" | Applied: a paragraph records this round |

## Build

Two clean builds from `c8a17315dfcaa86d61a5c6e612d0ba42d7299dff` gave the same PDF, 37 pages, SHA256 `d8df63f4a390bd7a27540f29ea50c3eff14bc1629d40c03894b36676b98bb2ef`, with zero overfull boxes and
every font embedded. The paper is two pages shorter than at the final skim, and its last page now carries several
references. The closing whole-paper review that the order of synthesis calls for is held until the author has
finished reading the paper, so that one review covers this pass and whatever the author finds next.

## Code and data split between the repositories (1da5034)

The author asked whether the Code and data statement had confused the two repositories, since most of the data is
in Terluna. The list was accurate for this repository (`PROVENANCE.md` records each file brought from Terluna on
17 October), and the statement already placed the runs in Terluna, but the evidence behind the numbers lies mostly
outside it: the claims register cites 161 sources in Terluna and 24 on the research drive against 186 here, and
the drive is private. The author agreed to a split, and said readers would have to reach out for the raw runs, with
no archive planned. Code and data now gives world-crafting the ensemble's code and records, gives Terluna's public
repository at 186b294 the scenario, runners, case set-up, analyses and run products, and makes the raw model output
"available from the author on reasonable request". Both repositories answered publicly on 19 October. This
one-paragraph change is left to the held closing review. Two clean builds from `1da5034c5cd9342d052222fa665deb4f6af293af` gave the same PDF,
37 pages, SHA256 `9f6744e43bb561358aaf0b276b8665e78120efdbe9d51d859877ed8cb864be16`, with zero overfull boxes.
