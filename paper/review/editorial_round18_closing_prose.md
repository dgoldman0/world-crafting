# Editorial round 18, closing review: the whole paper, for prose and the author's direction

- **Snapshot.** Commit `ffdedfe` (`ffdedfef8b373301c7597d0385d779f23798c2d5`); the working tree matched it
  (`git status --short` printed nothing). Files read: `paper/main.tex` and the thirteen files in `paper/sections/`,
  in the order `main.tex` inputs them, from the abstract and the note on terms to Availability, captions and tables
  included.
- **Reviewer.** A fresh Claude Opus 5.5 subagent, reading for prose and for the author's direction, at the close of
  round 18. This record is the only file I wrote; the paper's files stand as committed.
- **Date.** 19 October 2026.
- **Read before the paper.** `AGENTS.md` in full, its order of synthesis included; `editorial_round18.md`;
  `editorial_round17_dispositions.md`; from `editorial_round17_prose.md`, its judgment, its findings on the abstract,
  the Introduction and the Conclusion, its table of round-16 additions and its closing checks; the four Terluna
  sources behind the writing rules (`STYLE_NOTES.md`, `Jewish_Papers_Updated_Style_Notes.md`,
  `Agent_Working_State_Editorial_Gates.md`, `Open_Moon_Editorial_Charter_control-01.md`); the drafting assistant's
  notes of the author's directions on the abstract, the Conclusion, flow and the paper's framing. I then read round
  18's changes as a diff, `406549d..ffdedfe`, and the changes made after round 17's reading as a word diff,
  `1278887..406549d`.
- **Build.** `make -C paper clean && make -C paper pdf`: 38 pages, sha256
  `a86c38b483e7e17721126e3fc5161d54b1b14d3d8e26ea7348a127ba13eec4bf`, zero overfull boxes and one underfull line,
  a hash in the bibliography. I inspected pages 1, 2, 27 and 28 as images (pdftoppm, 70–90 dpi) and the extracted
  text of pages 1–3 and 26–28.
- **Cadence.** Read silently, with no read-aloud review.

## Judgment

The revision follows the author's directions. The definition of Gaean worlds now stands, word for word as the
author moved it, in a small note set like the abstract between the abstract and the Introduction, and the
Introduction opens on what some exoplanet climate studies do, then runs as before from the field's codes through
constructed worlds and the Earth values found in ported codes to the test world, the ensemble and the path ahead.
Read in order, the front matter is continuous: the abstract ends on "the Gaean class", the note defines the term
next, and the Introduction's first sentence receives the rotation, gravity and starlight the note lists, while the
abstract, the opening pages and the Conclusion still promise, develop and land on the ensemble that follows a
world's gravity, day and starlight into its storms and seas. The sentence added to Next steps presents columns of
the lakes and seas as a use of the ensemble's winds and sea states whose transfer and mixing laws are Earth fits to
test, keeping Terluna's lake results in Terluna as the author agreed, and the Conclusion's vision now includes the
exchange of oxygen between those waters and the air, in a clause that leaves the Earth-fit condition to Next steps
and sets up the ending's places where life may already have developed. I found nothing blocking anywhere in the
paper and nothing MAJOR. The six MINOR findings are local: two on the note's moved wording, which go to the author
(its closing clause makes a third statement of an argument the abstract and the Introduction already make, and its
"We" is the paper's only first-person form); the Next steps overview, whose list omits the new sentence's subject,
and the precision of that sentence; a garden path in the Conclusion's new clause; and the review history in
Availability, which stops before the author approved round 17's five fixes and before this round.

**Counts:** 0 BLOCKING, 0 MAJOR, 6 MINOR.

## Findings

### F1 · MINOR · for the author · `terms.tex`:5–7, with `abstract.tex`:6–8 and `introduction.tex`:52–57

*What fails.* The note ends on an argument: "Their gravity, size, rotation and starlight may differ substantially
from Earth's, so modelling their climate, storms and seas requires adapting both the component models and the
fields exchanged within an ensemble." At the head of the Introduction this clause stated a thesis that the following
paragraphs developed. In a note on terms it makes the second of three statements of one point within two pages: the
abstract has just said that the models joined in an ensemble "have to be adapted to one another before they
describe one world", and the Introduction's third paragraph derives the point from the ported codes and the THAI
spread, ending "so the retained Earth values affect both the individual calculations and the fields exchanged
between them". The note's "so" draws the requirement from the worlds' departures alone, whereas the abstract and the
Introduction also state its premise, that the models were built for Earth. Stage 2's light reading raised the clause
and left it for the author. I concur, for two further reasons: the Introduction's third paragraph states the
argument with its evidence, so a note that ends on the definition loses nothing; and a note ending on "may differ
substantially from Earth's" ends on the rotation, gravity and starlight that the Introduction's first sentence
receives ("Some exoplanet climate studies hold a planet's air close to Earth's and vary its rotation, gravity or
star").

*Fix.* The author moved this wording as it stands, so the choice is the author's: end the note at the definition.

> \noindent\textbf{Note on terms.} We use \emph{Gaean} for worlds with nitrogen--oxygen atmospheres and water as the
> principal condensable, at surface pressures and temperatures broadly comparable to Earth's and permitting liquid
> surface water and an active water cycle. Their gravity, size, rotation and starlight may differ substantially from
> Earth's.

### F2 · MINOR · for the author · `terms.tex`:3

*What fails.* "We use" is the only first-person form in the paper. Everywhere else the single author appears in the
third person ("The author reported the Sun clock to ExoPlaSim's maintainers", `next.tex`:126, and Availability
throughout), and Availability separates the author's part from that of the AI assistants. Set apart at the head of
the paper, the plural changes the voice, and a reader of Availability could take it to include the assistants. The
authorial "we" is a common convention in definitions, which leaves the choice to the author.

*Fix.* Give the substance first and the name after, as the abstract does:

> \noindent\textbf{Note on terms.} Worlds with nitrogen--oxygen atmospheres and water as the principal condensable,
> at surface pressures and temperatures broadly comparable to Earth's and permitting liquid surface water and an
> active water cycle, are named \emph{Gaean}.

`AGENTS.md` phrases the same definition as "Gaean names this physical class", and "\emph{Gaean} names worlds with
..." would serve as well. The note's second sentence follows either form unchanged, or as F1 shortens it.

### F3 · MINOR · `next.tex`:13–14

*What fails.* The section's overview gives the remaining experiments' subjects as "the dynamics, microphysics and
wave physics". The new sentence at lines 121–124 adds the mixing of the lakes and seas and their exchange of gases
with the air, physics outside all three, so the overview now lists less than the section holds.

*Fix.* "The remaining experiments use the lunar departures from Earth to test specific approximations in the
dynamics, the microphysics, the waves and the mixing of the lakes and seas beneath them."

### F4 · MINOR · `next.tex`:121–124

*What fails.* Three words leave the reader to supply what the sentence means. "For their mixing and their exchange
of gases with the air" names a purpose where the operation is a computation: the columns would compute the mixing
and the exchange. "Column" means a column of air everywhere else in the paper, a table's column apart, so "columns
of the lakes and seas" first suggests the air over them until the next phrase settles the sense. "The transfer ...
laws" leaves the transferred quantity, gas, to inference from the clause before.

*Fix.*

> Beneath the waves, the same winds and sea states could force one-dimensional models of the lakes and seas, which
> would compute their mixing and their exchange of gases with the air; since at lower gravity a given contrast of
> temperature resists the wind's mixing more weakly, the gas-transfer and mixing laws those models take, fitted on
> Earth's lakes, would be among the Earth values to test.

### F5 · MINOR · `conclusions.tex`:94–97

*What fails.* After the relative clause, ", and the same winds and waves" first reads as a second object of
"determine" ("would determine the waves reaching a particular shore, and the same winds and waves"), and the reader
parses the sentence again at "mixing the lakes and seas, would drive". "The same ... waves" also names the waves
reaching a shore of the sea, whereas the lakes have the waves the same winds raise on them.

*Fix.* Give the exchange its own sentence, opening on the mixing that ties it to the winds and waves before it:

> Simulated rain would constrain the water budgets of prescribed lakes; the winds transporting moisture would force
> the sea, whose spectra would determine the waves reaching a particular shore. Mixing the lakes and seas, the same
> winds and the waves they raise would drive the exchange of oxygen between the waters and the air.

"Whose" entered at stage 3 in place of the accepted "and its spectra", because the clause had made the sentence a
list of three. With the exchange in a sentence of its own, that list is gone, and the accepted "and its" could
return if the drafting assistant prefers to keep the wording the author accepted.

### F6 · MINOR · `availability.tex`:79–84

*What fails.* The review history ends with round 17's findings on approved wording "left for the author". The
author then approved the five, and they were applied as proposed (`51ea569`; `editorial_round17_dispositions.md`);
round 18 followed, with the lakes and seas in Next steps and the Conclusion, the note on terms at the author's
direction, a light reading of each change and this closing reading. `AGENTS.md` ("The paper") requires a release to
give the actual review history; round 17's F43 made the same point for rounds 16 and 17.

*Fix.* When this round's dispositions are recorded, continue the sentence, for instance:

> ..., which were left for the author; the author approved those five, and they were applied as proposed. In an
> eighteenth round, with the author's agreement, one sentence in the next steps and a clause in the conclusion took
> up the lakes and seas beneath the waves, and at the author's direction the introduction's definition of Gaean
> worlds moved above it as a note on terms; a fresh agent read each change, and the whole paper was read again to
> close the round.

## Round 18's changes, one by one

| Change | Location | Judgment |
|---|---|---|
| The lakes and seas beneath the waves | `next.tex`:121–124 | As the paragraph's last sentence, it turns from the waves to the water beneath them with a transition drawn from the subject ("Beneath the waves"), takes its forcing from the paragraph's winds and sea states, and writes the reason for testing the laws into a "since" clause; the reason is physically right, since the buoyancy of a temperature contrast scales with gravity; Terluna's lake numbers stay in Terluna; F3, F4 |
| The definition moved to a note | `terms.tex`; `main.tex`:51 | Word for word as removed from the Introduction (checked); set in the abstract's width and type size, with a bold run-in head like the paper's others; F1, F2 |
| The Introduction's new opening | `introduction.tex`:3–19 | Opens on the field and names the Terluna project once, at line 27, as `AGENTS.md`'s table of rejected openings directs; "Gaean" first appears in the Introduction at line 47, after the note; the first paragraph's line from global to resolved to joined models gives the field's precedents, and the Introduction's statement of what the field needs comes, as before, at the end of its third paragraph |
| Oxygen in the Conclusion's vision | `conclusions.tex`:96–97 | Stays within the paragraph's line from surface water to a geographically specific design; names oxygen where Next steps says gases; adds no number and leaves the Earth-fit condition to Next steps, where it is stated once; sets up the final paragraph's places "where life has already developed"; F5 |
| The abstract left unchanged | `abstract.tex` | Agreed: its account already includes the rain in the basins and the waves on the shores, and its own definition must serve readers of the abstract alone |

## What I checked and found sound

- **The author's directions.** The note holds the paragraph the author called "indeed a note", in its own words; the
  Introduction opens on the field; the abstract's text is as the author approved it on 18 October, unchanged since
  `51ea569`; the Conclusion keeps its accepted line of argument and its final paragraph, and its penultimate
  paragraph gains one clause. The paper remains a field paper whose subject is the ensemble, with the Open Moon as the
  worked case and Terluna as provenance.
- **The order of synthesis.** Next steps (the body), then the note (from the Introduction), then the Conclusion,
  with the abstract judged to need no change; one fresh agent read each change before the next began (`868cfc2`,
  `cba6d60`, `ffdedfe`), and the text shows the fixes those readings applied (`next.tex`:123–124;
  `conclusions.tex`:95). This reading closes the sequence.
- **The arc.** The abstract's prospect (a world's gravity, day and starlight followed from its global climate into
  the rain in its basins and the waves on its shores, for a world found or designed, and beyond the Gaean class), the
  note's definition, the Introduction's close on replacing the fits and testing the general repairs on planets that
  other studies model, and the Conclusion's opening and ending agree in subject and in their conditional mood. The
  waters run through the abstract's basins and shores, Next steps and the Conclusion's vision and ending ("the passage
  of a storm over a lake"); the lake columns enter as a prospect, which the Introduction can leave to Next steps.
- **The note against the abstract.** The note's first sentence restates the abstract's description of the class in
  fuller terms (liquid surface water, an active water cycle); since the abstract has to stand alone and the note
  gives the paper's own definition, the repetition is justified. The abstract writes "day" where the note writes
  "rotation"; both are apt, the class being defined by rotation and the models depending on the solar day, and both
  are approved wording.
- **Layout.** Page 1 sets the note under the abstract, with the Introduction's heading and first two lines at its
  foot; page 2 continues the first paragraph. The Conclusion's last two paragraphs open page 28 after about six lines
  of white space at the foot of page 27; a build of `cba6d60`'s sources, made in a scratch folder before the clause,
  breaks at the same place, so the clause leaves the layout as it was.
- **Word screen.** The section files contain no "not", "rather than", "Notably", "It is worth noting" or "Turning
  to"; "we" occurs only at `terms.tex`:3 (F2); no text refers back to the removed paragraph, and "codes like those
  named above" (`introduction.tex`:34) points to the first paragraph's codes, as before.
- **Lint screen** (`paper/tools/lint.py`, screening only): 277 candidates (18 negative contrast, 2 self-reference,
  35 possible empty action, 12 coined term, 187 universal claim, 23 generic verb). `terms.tex` gives none, and none
  falls in the new sentence or the new clause; the two at `next.tex`:120 are physical uses ("spectra reach", "swell
  carries") in text round 17 read.
- **Check script** (`paper/tools/check.py`): 14 TeX files, the note among them; 96 cited keys of 167; 107 claims
  cited of 109; its standing warnings (the web source of H23 and N02 unchecked offline; S01 and V14 uncited).
- **Nothing blocking elsewhere.** I read every section in full, the passages revised after round 17's reading among
  them (its dispositions and the five approved fixes, `1278887..406549d`), for errors of fact, meaning or direction.
  The numbers that recur across sections agree: 295.5 and 315.5 K between Assumptions and Results; the abstract's
  1.6–2.5 K and "up to about 6 K" with Results' 2.3 and 1.8 K over the years averaged, 2.5 and 1.6 K settled, and
  5.0 and 5.9 K; the Introduction's 7.25 and 23 with Table 1; the factor of about four in rain with Next steps'
  "near a quarter".

## Noticed outside this reading's scope

- `paper/review/README.md`: its History also ends at round 17, with the five findings "left for the author"; the
  update in F6 applies there too.
- `release_register.md`: its newest build is `9a4810d9…` at `406549d`; the sources at `ffdedfe` build `a86c38b4…`
  (38 pages), whose exact-build review is still to be recorded.
- `results.tex`:88–89, written after round 17's reading and outside this round's changes: in "the longwave
  correction with the ice optics, a calibration and a general repair switched on together and the one change fitted
  to the cooling by height", the last "and" joins a description of the correction alone to a description of the
  pair, so the phrase first reads as a list of three. A minor point for a later round.
