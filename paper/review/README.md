# Review records

The records of every review made on the paper, by whom and with what findings, following the editorial
charter's gates (G1–G7), its ten separate prose passes and its release integrity rule (E4), and the writing
rules in the repository's `AGENTS.md`. A record states what was done; a review still to be performed is
marked pending.

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

The first editorial round read the second draft: five fresh reviewers, four by part and one across the whole
paper, raised 172 findings, 20 blocking. While it ran, the author read the second draft and found it still
centred on the Moon. The third draft (c63df43) acts on both; its dispositions are in
`editorial_round1_dispositions.md`. The author then read the third draft, judged the rest of the paper to stand
for now, and rejected its conclusions as a summary that implied reach to untested worlds. The closing section was
rewritten as discussion and conclusions (bb5d0f0) and read again in rounds of two fresh reviewers, one for prose
and the author's direction and one for evidence and scope: round 2 (bb5d0f0), round 3 (e89a394), round 4
(798f68b), round 5 (11026a8), round 6 (8bfd069), round 7 (654ebdf) and round 8 (44d67d4). The blocking findings by
round were 6, 3, 1, 3, 2, 3 and 0; most concerned the reach of the closing sentence and of what laboratories and similarity runs can
test. Each round's records name the snapshot they read, and the revisions between rounds are in the commits that
follow them. The dispositions of rounds 2 to 5 were reconstructed afterwards from those commits by a subagent, since
the drafting assistant acted on those rounds without writing a dispositions record; the dispositions of rounds 6
to 8 were written with their revisions. Round 7's evidence record found a factual error that the earlier
rounds had passed: Next steps gave one charging law positive ground strikes, where the runs show the storms'
arrangement of charge inverted and every ground strike in those windows negative. Round 8 found nothing blocking,
which closes the rounds; its findings were acted on in 94d337a, unread by a further round, and the author's reading
is the next review. The PDF built from 94d337a was then inspected page by page by its hash (`g7_visual_review.md`),
and `release_register.md` records each gate's status for it.

On 18 October 2026 the author read the conclusion of 94d337a and rejected it as a summary and data dump, and in the
directions that followed asked for a discussion rooted in the code and technology built, exciting throughout and
ending in pure inspiration. The drafting assistant rewrote it (0cb4f50), and round 9 read the rewrite with two
fresh reviewers, one for prose and the author's direction and one for evidence
(`editorial_round9_conclusion_*.md`); 04a6c27 acted on its findings, and its commit message records the
dispositions. Round 10, one fresh reviewer for evidence alone, checked that revision
(`editorial_round10_conclusion_evidence.md`). The author then read the conclusion of 04a6c27 and rejected it as
still a summary, noting a witticism, an overstatement of what a code's checks need from the world it models, and
wording that slighted ExoPlaSim's developers, who had extended PlaSim to other worlds. Round 10's findings on that
conclusion lapsed with its replacement, except finding 12: Results and `notes/cm1.md` gave the 1.5 K as the GCM's
own over-cooling, where it is the GCM's over-cooling beyond CM1's, and both were corrected in the check recorded in
`terracompatible_check_2026-10-18.md`.

The author then asked Codex for a fresh conclusion and supplied the direction quoted in round 12's records:
developed discussion across as many paragraphs as needed, sustained excitement, and an ending of pure inspiration.
Codex drafted the replacement. Fresh Codex agents read its prose and evidence in rounds 11 and 12, prompting a
structural revision and then local revisions. The reviewed drafts are retained under `drafts/`; the findings,
dispositions and checks are recorded in `conclusion_rewrite_2026-10-18.md`. The author's reading of the revised
draft comes next, following the priority made explicit in AGENTS.md at 15ad8de. The earlier release register
remains tied to its stated PDF.

The author then read that draft and rejected its lunar framing, restating the central purpose as an ensemble
of models for exoplanets and constructed worlds. Codex read the relevant Claude memory notes and rewrote the
conclusion around that purpose. Round 13's fresh prose and evidence readings prompted alignment of the
introduction and a local cloud-calibration qualification. The abstract's purpose statement was aligned as
well. The author's direction, revisions, checks and build are recorded in
`conclusion_ensemble_rewrite_2026-10-18.md`; that record supersedes the earlier draft's pending-author status.

The author then accepted the ensemble-centred Conclusion, selected *terracompatible* for the intended class
and requested its definition and use throughout, a whole-manuscript framing check and one sentence on the
ensemble's prospective extension beyond that class. The author's review and the resulting revision are
recorded in `terracompatible_revision_2026-10-18.md`, with the fresh round 14 records beside it.

Claude Opus 5.5 then checked Codex's revision at the author's request. The check corrected the review history in
Availability and three sentences of Results, Reach and Next steps; `terracompatible_check_2026-10-18.md` records
the checks, the corrections and the rebuilt PDF. The author then judged the statement of where the repaired codes had
run, repeated through the paper, to be defensive and badly phrased; it was recast to inform once, in Reach, as
the same record sets out.

Round 15 followed the author's direction of the same day on flow: after transitions had been cut from a drafted
abstract sentence, the author asked that the paper's prose flow, with transition words wherever they move the
reader on, and that paratactic paragraphs, facts chained like bullet points, be found. Three fresh Claude subagents
read the paper by thirds for flow alone at 64d04e0, later reworded as 2800b68 over the same tree, and returned 101
findings, 28 MAJOR and 73 MINOR: 9 and 21 in the abstract, Introduction, Worlds and Assumptions; 15 and 28 in
Repairs, Verification and Results; 4 and 24 in Reach, Next steps, the Conclusion, the appendix's prose and
Availability, the Conclusion's three marked for the author. Each MAJOR finding carries a sample rewrite that keeps
its passage's claims, numbers, citations and claim markers. The records are `editorial_round15_flow_opening.md`,
`editorial_round15_flow_middle.md` and `editorial_round15_flow_closing.md`; the author then asked for the findings
to be acted on section by section, and `editorial_round15_dispositions.md` records what was done with each, the
Conclusion's three left for the author.

After the related-work scan noted that the paper gave no reason for running CM1 in slices, the author gave the
reason, the hardware's limits and a best guess at the features of interest, and directed that the paper state it;
one sentence in the Introduction now does, with its record in `slice_reason_2026-10-18.md`.

The author then read the abstract, accepted its opening and judged the rest a summary of the paper, whereas an
abstract should draw the reader in. The drafting assistant rewrote the rest, and the author approved it with one
clarification. The author had also made the world-crafting repository public, and Availability now names it as
the place where work on the ensemble will continue; `abstract_and_repository_2026-10-18.md` records both.

The related-work scan (`paper/notes/related_work_scan_2026-10-18.md`) then entered the paper at the author's
direction, in the order the author set as a general pattern: the body first, in four steps (corrections and
missing citations, the ensemble beside its nearest neighbours, the lunar numbers beside the field's measured
spreads, existing tools for the next steps), then the Introduction, the Conclusion and the abstract, each step
followed by a light reading by one fresh Claude Opus 5.5 subagent. Those seven readings form round 16,
`editorial_round16_light.md`, with their dispositions. Round 17 then read the whole paper with two fresh agents,
one for prose and the author's direction and one for evidence and scope (`editorial_round17_prose.md`,
`editorial_round17_evidence.md`); nothing was blocking, five findings were MAJOR, and
`editorial_round17_dispositions.md` records what was done with each; the five findings on wording the author had
approved were applied once the author had read them (51ea569).

On 19 October, at the author's direction, a sentence in Next steps and a clause in the Conclusion took up the lakes
and seas beneath the waves, keeping Terluna's new lake results in Terluna, and the definition of Gaean worlds moved
from the Introduction into a note on terms above it. Round 18 (`editorial_round18.md`) holds the light reading of
each stage and the dispositions of a closing whole-paper review by two fresh agents
(`editorial_round18_closing_prose.md`, `editorial_round18_closing_evidence.md`), with four findings on approved
wording applied once the author had read them.

On 19 October 2026, the author requested a final skim for substantial errors, missed central points and
novelty overclaims. Codex and two fresh reader agents assessed the current manuscript at that threshold,
with targeted technical checks, and returned PASS. `final_skim_2026-10-19.md` records the reviewed source
and PDF, the actual checks and the bounded decision; the manuscript remains as reviewed.

The author then read the paper and judged the review history in its Availability section out of place in a
standalone paper, together with other accounts of the paper's own making. Following the assistant's proposal, the
review history left the paper, the account of assistance became a short AI-use statement, Code and data was trimmed
to where things are, Next steps lost its list of reports and reruns, and AGENTS.md now keeps the review and
drafting history in this folder. One fresh reader read the change, and its fixes followed;
`editorial_round19.md` records the round. The manuscript has changed since the final skim, which no longer
describes it.

The author's subsequent request for a final reader review was carried out by Codex and two fresh reviewer
agents at `6a35a24`. The removal of internal editorial history resolved that objection, while three causal
claims exceeded the recorded evidence: the upstream attribution of CM1's threaded divergence, the residual
temperature gap's attribution to heat transport, and the diagnostic promise of a third GCM. The current
decision and findings returned to the author are in `final_reader_review_2026-10-19.md`; manuscript revisions
remain pending the author's reading.

Codex's final reader review (`final_reader_review_2026-10-19.md`) then found three inferences beyond their
evidence. The author had all three narrowed, choosing to class CM1's threaded parting as a fault of uncertain cause,
which leaves four defects in the released codes; `editorial_round20.md` records the assessment, the changes in the
order of synthesis and their light readings.

Having read the paper whole, the author judged it good overall and named one remaining weakness: verbs that give a
subject an act it cannot perform. The closing review, held until that reading, became round 21. Two fresh agents
each tested every verb in half the paper against its subject (`editorial_round21_closing_front.md`,
`editorial_round21_closing_back.md`); the fixes outside the abstract and the Conclusion were applied and given a
light reading. The author accepted the 21 fixes on approved wording, and then asked that the paper say plainly why the
ensemble builds on ExoPlaSim when generic planetary GCMs exist; three sentences followed, in Next steps, the
Introduction and the Conclusion. `editorial_round21.md` records the dispositions, the three light readings and the
added sentences with their sources. Code and data then named the release tags, `paper-v1` here and
`world-crafting-paper-v1` in Terluna, for the first released draft. The author's final reading changed one phrase of the AI-use statement.

## Reviewers

| Reviewer | Role | Records |
|---|---|---|
| Claude Opus 5.5, the drafting assistant (main session) | Drafted the paper's drafts and their conclusions to 04a6c27; silent prose passes on the first draft; dispositions of rounds 1, 6, 7 and 8, and of round 9 in 04a6c27's commit message; the exact-build page review; the release register; the check of Codex's revision | `passes_<section>.md` (first draft), `*_dispositions.md`, `g7_visual_review.md`, `release_register.md`, `terracompatible_check_2026-10-18.md` |
| Claude subagents, technical referees | Checked every claim and table row of the first draft against its sources | `referee_technical_part1.md`, `referee_technical_part2.md`, `referee_dispositions.md` |
| A Claude subagent, whole-manuscript challenger | Challenged the first draft as a whole against G1–G5 | `whole_manuscript.md`, `whole_manuscript_dispositions.md` |
| Fresh Claude subagents, editorial reviewers | Read the second draft against the rules, by part and as a whole (round 1), then the rewritten closing section and the passages revised with it, for prose and for evidence (rounds 2–9), the revised conclusion's evidence alone (round 10), the whole paper's flow alone, by thirds (round 15), each stage of later revisions in light readings, the whole paper in closing reviews (rounds 16–21), and every verb against its subject, by halves (round 21) | `editorial_round<n>_<part>.md` |
| Codex, drafting assistant | Wrote a fresh conclusion on 18 October 2026, revised it after rounds 11 and 12, and replaced its lunar framing after the author's review | `conclusion_rewrite_2026-10-18.md`, `conclusion_ensemble_rewrite_2026-10-18.md` |
| Fresh Codex reviewer agents | Separate prose and evidence readings in rounds 11–13; bounded verification of round 13's dispositions; whole-manuscript terminology and framing review in round 14 | `editorial_round11_conclusion_*.md`, `editorial_round12_conclusion_*.md`, `editorial_round13_conclusion_*.md`, `editorial_round14_whole_*.md` |
| Claude subagents, record keepers | Reconstructed the dispositions of rounds 2–5 from the revision commits | `editorial_round<n>_dispositions.md`, n = 2–5 |
| The author | Readings of the drafts, decisive on framing and prose; resolution of exceptions; the competing-interests declaration | First draft read 2026-10-17 (framing and prose rejected; the author counts this stream-of-thought reading as its cadence review); second draft read during round 1 (still Moon-centred); third draft read 2026-10-17 (the rest stands for now; conclusions rejected); conclusion of 94d337a read 2026-10-18 (rejected as a summary); conclusion of 04a6c27 read 2026-10-18 (still a summary; a witticism, an overstatement and a slight to ExoPlaSim's developers); Codex conclusion read 2026-10-18 (lunar framing rejected; model ensemble restated as the purpose); ensemble Conclusion read 2026-10-18 (accepted; terracompatible to be defined early and used throughout, with one prospective sentence); abstract read 2026-10-18 (opening accepted, the rest a walk through the sections; the rewrite approved); the paper read 2026-10-19 (the review history and other accounts of its own making out of place in a standalone paper), then read whole after round 20 (good overall; verbs that give a subject an act it cannot perform remain); the final reading before release, 2026-10-19 (the AI-use statement to open "The author", as the competing-interests statement does; otherwise final) |

The Claude and Codex agent readings are AI-assisted editorial reviews. Review by a person other than the
author, or by a journal, remains pending; the records identify the reviewer and activity of each pass.

## Files

| File | Holds |
|---|---|
| `passes_<section>.md` | The first draft's ten passes for one section (historical; the sections were rewritten) |
| `referee_technical_part*.md`, `referee_dispositions.md` | The technical referees' findings on the first draft and what was done with each |
| `whole_manuscript.md`, `whole_manuscript_dispositions.md` | The whole-manuscript challenge of the first draft and its dispositions in the second |
| `editorial_round<n>_*.md` | Each editorial round's records by reviewer, and the round's dispositions |
| `drafts/` | The exact conclusion drafts read in rounds 11–13 |
| `conclusion_*_2026-10-18.md`, `terracompatible_*_2026-10-18.md`, `terracompatible_visual_pages*.md` | The records of 18 October 2026: Codex's drafting and revisions, the check of them, their builds and page inspections |
| `slice_reason_2026-10-18.md` | The author's reason for CM1's slices, the sentence that gives it, its claim, checks and build |
| `abstract_and_repository_2026-10-18.md` | The author's reading of the abstract, its rewrite, the public repository in Availability, checks and build |
| `final_skim_2026-10-19.md`, `editorial_round19.md`, `final_reader_review_2026-10-19.md`, `editorial_round20.md` | Codex's final skim and final reader review of 19 October, the removal of the paper's account of its own making, and the three inferences narrowed after the second review |
| `final_reader_review_2026-10-19.md` | The subsequent whole-paper reading, three unresolved inference claims, and checks of the revised declarations |
| `g7_visual_review.md` | The exact-build page review: renderers, the PDF hash and page-by-page observations |
| `release_register.md` | PASS / BLOCKED / DEFERRED by gate, with the exact PDF and source hashes |

The automated checks (`tools/check.py`, `tools/lint.py`) establish record completeness and list candidate
places for reading; they clear no gate.
