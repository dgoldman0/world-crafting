# World-crafting

The models, patches and in-house tools for modelling terracompatible worlds beyond Earth's range — planets
and constructed worlds with nitrogen–oxygen air, water as the principal condensable, and broadly terrestrial
surface pressures and temperatures, while their gravity, size, day or starlight differ — and the paper that
describes them. The work so far comes from one case, a breathable Moon
designed in the Terluna project (github.com/dgoldman0/Terluna). The machinery here was brought from
Terluna at commit 186b294 (2026-10-17), and `PROVENANCE.md` records its provenance file by file.

## Commits

Use informative commit messages. Multiple phrases for a commit message.

## System usage limits

Be mindful of system resource availability, especially when other sessions run tests or models on the
same machine. The GCM, CM1 and SWAN runs themselves stay in Terluna; work here runs patches, offline
tools and tests.

## Where work goes

| Work | Home |
|---|---|
| A patch to an upstream model, or Fortran written for one | `models/<model>/` with its README: what each patch changes, its switch and default, its verification and its limits |
| An in-house reference or calibration tool | `python/`, under the package path it had in Terluna so its imports and history stay traceable |
| Notes on correctness, limitations and room for improvement | `notes/`, one file per component |
| The paper | `paper/`: notes, sections, figures, data extracts, source records, review records |

Case set-up, run bookkeeping and analysis scripts stay in Terluna. Upstream source code is never
committed whole: patches are applied to the pinned upstream archives named in each model's README.

## File and evidence practice

These follow Terluna's AGENTS.md (sha256 7fac1ca0…be6 at 186b294):

- A runnable calculation, numerical convergence, an input hash, a proposed design and empirical
  validation are different evidence states. State assumptions and boundaries near outputs.
- Never fill an empty topic with invented results or mark future work complete. Never silently
  substitute data after a failed download or hash mismatch.
- Review redistribution rights before adding outside datasets, source code or full papers, and
  record their source, hash and credit. Full papers archived for reading stay outside Git
  (`paper/sources/originals/` is ignored); their records are committed.
- Report actual checks and unperformed work.

## The paper

The paper stands alone as a field paper on modelling terracompatible worlds beyond Earth's range: exoplanets
and constructed worlds with nitrogen–oxygen atmospheres and water as the principal condensable, at surface
pressures and temperatures broadly comparable to Earth's and permitting liquid surface water and an active
water cycle. Their gravity, size, rotation and starlight may differ substantially from Earth's. Terracompatible
names this physical class; the tested range of each code is specified separately. The paper's central purpose is the
development of an ensemble of models for those worlds, connecting
global climate to storms and seas. That purpose, and the work toward it, frame the paper. The breathable
Moon is its worked case, the world on which the work so far was done and existing systems' limitations
became apparent. Terluna enters as provenance only: the origin of the case, the code and data records,
and the history of AI assistance. Terluna's paper IDs and five-paper ensemble stay out of this paper;
the model ensemble is the subject. The Conclusion develops that broader purpose throughout, with the
lunar work as evidence and a starting point. Further physics for other gases and condensables could extend
the ensemble beyond the terracompatible class; that extension remains prospective.

Evidence and release follow Terluna's editorial charter
(`ensemble/planning/Open_Moon_Editorial_Charter_control-01.md`, sha256 aac4a4f2…0b0): technical meaning
and evidence states (G5), full-document source admission (G6), exact-build visual review by PDF hash
(G7) and release integrity (E4). Each section is drafted and reviewed with its neighbours, its reviews are
recorded in `paper/review/`, and the release register uses PASS, BLOCKED and DEFERRED with exact
artifact hashes; nothing is prefilled. Author metadata: Daniel S. Goldman, ORCID 0000-0003-2835-3521,
no affiliation label. Final releases carry an accurate AI-assistance disclosure and the actual review
history, in which each of the author's own readings is recorded as the author's review.

## Writing

These rules govern the paper and everything written here for its author: notes, READMEs, review
records, commit messages and replies. They consolidate the charter's gates G1–G4 and the three style
notes it was built from, in Terluna's `ensemble/planning/source_controls/` (`STYLE_NOTES.md`,
`Jewish_Papers_Updated_Style_Notes.md`, `Agent_Working_State_Editorial_Gates.md`), with the author's
corrections of 2026-10-17. Read those four sources in full once before writing for the paper; the rules
below are their working form.

The author's explicit direction for a piece outranks these rules. Where a direction and a rule conflict,
carry out the direction; where the conflict is unclear, ask the author once, naming both. A rule is never
grounds for setting a direction aside.

**Say what is.** State what a thing is, does or includes.

- The words "not" and "rather than" are excluded from authorial prose. Other negative contrasts
  ("X, never Y", "instead of", "unlike", "without", "fails to") are judged by meaning: negation stays
  only where the proposition requires it (a run that failed to convect, a scheme that lacks ice).
- Defensive posturing is excluded: pre-emptive disclaimers, anticipatory apologies, objection
  catalogues, caveat walls, hedges stacked ahead of a claim. A qualification attaches once to the claim
  it bounds, stated positively ("the fit holds between 0.5 and 2 bar").
- Promotional framing, self-praise, generic importance claims and inflated contribution verbs are
  excluded.

**No witticisms.** Titles, headings, coined terms and paragraph landings say what they name. Aphorisms,
puns, personified coinages, quotable closing lines and rhetorical questions are excluded. These bans, like
the ban on promotional framing, aim at cheap wit and hype; vision is welcome, and the Conclusion's ending
is meant to inspire.

**Write for the expert.** The reader models planetary atmospheres, convection or waves and knows the
general concepts.

- A familiar concept enters through its specific use, consequence or test in this work.
- Delete-test each explanatory sentence: it stays if it supplies a premise, a mechanism or an
  inferential step this reader lacks.
- Excluded: tutorial exposition, explaining what the reader already knows, telling the reader what to
  notice, recognise or conclude, and restating an implication the evidence already makes plain.
- Self-reference ("this paper", "here we", "the present analysis") only for real disclosure of method.

**Exact action.** A verb names something that happens.

- Verbs of action belong to agents that act. An abstraction (a model, Earth, the uncertainty, the
  evidence, a section, a class of repair) that carries, sits, hides, answers, divides, stands behind,
  asks, exposes or reaches is an empty action. Name the actual agent and operation: the code
  multiplies, the scheme integrates, the run warmed 2.3 K, the author fitted. Passive voice serves
  where the agent is known or beside the point.
- Generic analytical verbs (show, provide, support, demonstrate, allow, give, establish, reflect,
  enable, address) earn their place; where the evidence names an operation, the prose names it.
- Nouns are precise: the variable, the scheme, the switch, the run, the layer.
- Physical processes, and the people who did the work, stay visible where they belong.

**Sentences carry their dependencies.** Paratactic prose is excluded: a string of equal-weight declaratives
(proposition, stop, proposition), or a paragraph that chains facts like bullet points, is a list disguised as
prose.

- Write the causal, temporal, constitutive, comparative, concessive or evidentiary relation into the
  syntax: subordination, apposition, participial phrases, relative clauses, periodic sentences.
- Coordination joins only propositions of equal weight.
- Short sentences serve as hinges and landings, where their finality is earned.
- Vary openings, subjects, lengths and stress. Repeated subject–verb resets, and consecutive sentences
  opening on the same abstract noun, mark an inventory.
- Length and connectives cure nothing: a long sentence holding the same inventory still fails.

**Inheritance and order.**

- Each sentence receives something from the one before (an actor, object, quantity, condition, term or
  unresolved implication) and transforms it, except at a deliberate turn.
- Swap test: when two sentences or paragraphs can trade places without loss, the relation between them
  is unwritten, and the passage is rebuilt.
- Each paragraph develops a question, mechanism, sequence, comparison, consequence or tension; its last
  sentence completes that movement or sets up the next paragraph.
- Writing flows and transitions smoothly. Each move from one thought to the next is marked: by the relation
  written into the syntax, by a transition drawn from the subject matter, or by a transition word
  ("moreover", "even though", "however", "in addition") used where it moves the reader on. A new or
  independent point is marked as one, so that it reads as an addition and never as a consequence of the
  sentence before. The author's own transitions stay.
- Stock signposts are filler and are excluded: "It is worth noting", "Notably", "Turning to", or a
  "Moreover" that opens a point with no relation to what came before.
- A genuine catalogue goes in a table or a list.

**Conclusions and the arc.** The paper has no separate discussion, so its Conclusion is the discussion. It
reminds the reader of the work in a line or two at most, then discusses what the findings mean and open up,
rooted in the code and technology built, in as many paragraphs as the ideas need and with one line of argument
across them. It excites throughout, and its ending ties the section together in pure inspiration: the vision
of what this work makes possible, in concrete images and prospects. Numbers enter only where they make a
point, and a condition is stated once. Recaps, data dumps, replaying the section order, reciting the inventory
and delivering a generic lesson are excluded. The abstract, the opening pages and the conclusion promise,
develop and land on the same contribution.

**Technical meaning survives editing.** Each edit keeps the claim's conditions, numbers, scope and
evidence state. Reproducibility and physical validation stay distinct.

**Claims stay within their evidence.** A statement about a field or its literature says what the cited
works did, scoped to them ("some", "these", the authors by name); characterising a whole field takes
evidence about the whole field. The same holds for "each", "every", "most" and "all" anywhere: each
universal claim is checked against what was actually examined.

**Examples from the first draft**, rejected by the author on 2026-10-17:

| First draft | What fails | Direction of repair |
|---|---|---|
| Title "Earth inside the models: ..." | Witticism | Name the subject: modelling Earth-like worlds beyond Earth's range |
| "Terluna asks what weather, climate, storms and seas a breathable Moon would offer ..." | A project presented as known; the paper framed around it | Open on the field's need; name the project once, as the source of the case |
| "The microphysical and surface laws carry Earth in the same way." | Empty action on an abstraction | Say which laws were fitted to which Earth data, and what follows on the Moon |
| "... and where the uncertainty that remains now sits." | Empty action | Name the assumptions that still move the result most, and by how much |
| "Three model families divide the work, each answering where the previous one stops." | Empty action | Say what each model computes and what it takes from the others |
| "Carrying these models to the Moon exposed Earth inside them in five forms" | Witticism and empty action | Name the five forms of Earth value found in the code |
| "The repairs follow one rule ..." | Overstatement | The main rule, with the other kinds of repair beside it |
| "Exoplanet climate studies compute the temperature, cloud and rain of rocky planets whose air resembles Earth's ..." | A whole field characterised from four studies | Say what the cited studies did: some hold the air near Earth's and vary rotation, gravity or star |
| "Each constant is right for Earth, and can be made right for the Moon as far as its lunar value is known." | Landing that restates the paragraph | Land on a consequence, or end at the evidence |

## Review of the paper

The paper alone is written in drafts and review rounds. Its editorial quality is judged by reading: after
a section is drafted, fresh reviewer agents that see the text, the author's direction for it in the author's
own words, and these rules read it whole and return located findings. They judge the text against the
author's direction first and the rules second, and no finding overrides that direction. The author's
readings are the decisive review and come ahead of further rounds: once a draft carries out the author's
direction, it goes to the author, and later rounds follow the author's reading. Otherwise the text is
revised and read again by fresh reviewers until a round finds nothing blocking. `paper/tools/lint.py` screens
for candidate places, and its output is reported as screening only. Each round's reviewers, findings and
dispositions go in `paper/review/`.

## Software work

Code, patches and tools follow a conventional software workflow, in small tested changes:

- **One branch for each line of work.** Work stays on its line's branch, the lab's on `lab`; a separate
  branch serves a separate line of work. Each change is a commit or a short series of them, committed once
  it passes.
- **Tests with the code.** A change adds or updates the tests that pin its behaviour, and `make check`
  passes before it is committed; a bug fix starts from a failing test.
- **Review of the change.** A change of more than a few lines gets one code review of its diff, by the
  author or a fresh reviewer agent. Its fixes land in the same change, and the change's commit message
  records the review.
- **Living documents.** Design documents, READMEs and notes change in the same commit as the code they
  describe.
- **Evidence.** The file and evidence practice above holds for code: a passing test checks the code, and
  validation of the physics is recorded separately.

## Checks

`make check` runs the Python tests and the patch checks (each patch series applies cleanly to its
pinned upstream source). The paper builds with `make paper`.
