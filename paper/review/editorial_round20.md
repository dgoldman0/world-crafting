# Round 20: three inferences narrowed after Codex's final reader review, 19 October 2026

Kept by Claude Opus 5.5, the drafting assistant.

## Codex's findings and the assessment

Codex's final reader review (`final_reader_review_2026-10-19.md`, at 6a35a24) marked the manuscript BLOCKED by three
inferences. The author asked whether they held. The assistant's assessment:

1. **CM1's "race between threads" in released CM1: holds in part.** Codex argued that OpenMP leaves a reduction's
   order unspecified, so repeated threaded runs may differ without a race. CM1 r22.0's source has no OpenMP reduction
   clauses (a search of `src/*.F` on the research drive found none; two CRITICAL blocks, WRF logging and NSSL), so
   that argument leaves this build aside. The rest holds: the parting was seen in patched lunar builds only, stock CM1
   never ran on these cases, the Earth supercell repeated on 4 and 2 threads, and the electrified graft had held two
   thread-dependent faults of other kinds (uninitialised memory, a misplaced private variable; defect log C10, C11).
   The patches' threaded writes were checked as local, which makes CM1's own loops the likeliest place, yet a race,
   and its place in the released code, remain inferences.
2. **"Attributed by elimination" in Results: holds.** The text before it leaves the ice above 107 km unquantified and
   the dry-ground test at 45 N unrun.
3. **An independent GCM "would show" and "would place the error": holds.** Agreement with a third model can set
   priorities; shared biases leave the cause open.

The author chose the fuller fix for the first, classing CM1's threaded parting as a fault of uncertain cause beside
PlaSim's cold lowest level, which leaves four defects in the released codes and changes the approved count in the
abstract and the Introduction, and agreed to the other two. Codex's optional suggestion to trim Availability's
sentence on the repository's continuing work was left, since that sentence carries the author's direction.

## Changes, in the order of synthesis

| Commit | Stage | Change |
|---|---|---|
| 873a204 | Body | Assumptions counts four defects and two faults of uncertain cause; the inventory table's Threads row becomes "?"; Repairs, Table 7, claim H26, the defect log, the verification record and the CM1 notes follow. Results: "plausibly comes from". Next steps: "would indicate", "would point to", "each then to be tested directly" |
| c3d4fd8 | Body | The light reading's fixes, below |
| 96ddac1 | Introduction, abstract | "four defects" |

## Light readings

**Body (873a204).** One fresh Claude Opus 5.5 subagent found the body consistent on four defects and two faults, and
one MAJOR and four MINOR problems, all applied in c3d4fd8:

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1, MAJOR | `next.tex`:84–87 | The RRTMG step still said the remaining near-ground range "measures the two models' boundary layers", the elimination Results now calls plausible | Applied: the range "would test the boundary-layer explanation, beside the ice above 107 km and the dry ground at 45 N" |
| 2 | `claims.json` G07; `notes/cm1.md`:122–125 | Both still attributed the remainder by elimination | Applied: "plausibly from boundary-layer transport, with the high ice and the 45 N dry-ground test open"; "plausibly lies" in the note |
| 3 | `claims.json` V14 | "The unlocated thread race" | Applied: "the unlocated source of CM1's threaded parting" |
| 4 | `assumptions.tex`:133–134; `notes/cm1.md`:167 | "A run of stock CM1 on these cases" names a run stock CM1 cannot make, lacking lunar gravity, Sun and forcing | Applied: "a threaded run of stock CM1 with these boxes' options would test whether it lies there" |
| 5 | `notes/defect_log.md`:104–110 | The classification paragraph was dated to the draft that counted five, and implied stock runs had been made | Applied: "as revised 2026-10-19", and "since stock CM1 has yet to run with these cases' options" |

**Introduction and abstract (96ddac1).** One fresh reader found both count sentences correct and in agreement with
the body (four D rows and two ? rows in the inventory), nothing in the Introduction, abstract or Conclusion depending
on five defects, and no disagreeing count or remaining "race" in the paper. Verdict: ready.

## Build

Two clean builds from `96ddac1203dfe3328d43d2c99063398b1ffa93bb` gave the same PDF, 37 pages, SHA256 `f6ff147f7fb291d4acf5e80c24185bf8a006a7be3d64bc17c179b7507888623f`, with zero overfull boxes and
every font embedded. The stranded line closing page 24 remains for the final layout. The closing whole-paper review
stays held until the author finishes reading.
