# Editorial review, round 1: the whole paper

**Reviewer.** A fresh Claude subagent (Claude Opus 5.5), assigned the paper as a whole while four other reviewers
read its parts line by line. Date: 2026-10-17.

**Text reviewed.** The paper at commit 4d03a81. HEAD moved to a06a4ab during the review; that commit changes
`paper/notes/plan.md` and files in `paper/review/` alone, and `git status` reports the section files, `main.tex` and
`claims.json` unchanged, so the sources reviewed are identical at both commits.

| File | sha256 |
|---|---|
| `main.tex` | `87c1cddb6bc6a68d5a7666d4f310f250389600a5e640c3ffd8470d9ada41371c` |
| `sections/abstract.tex` | `b8b0f6fd8c184465454f7265f6870d2b5f8ac2c56386654d827c6f5595834921` |
| `sections/introduction.tex` | `5d1b9cf839ea398370c884d828d54fe45951ab79492e9f3c7a3fce6a70aff9e0` |
| `sections/worlds.tex` | `46dc5b00bfd347693c0f57929ee690f4db4cd1a4ac97b996b82af07f010ff0b2` |
| `sections/assumptions.tex` | `4b0f209c6aebcbc4c907778548d27c5dca9512e3d44347ccf7cdff2f98b9cfd7` |
| `sections/repairs.tex` | `3bcef8a3a813e83b33cf4f954da68c05ce6bd78f8d31375808a955162dca81ef` |
| `sections/verification.tex` | `a3ca68dc2de6007d42e0081a2bbbb4e1308dfea16e406b8d577fdee65ad3cfa5` |
| `sections/results.tex` | `a864fc868d6f3cd0aaa23015813cb2b5b7fbe214573be229c4ec3c0b7ee7bdc6` |
| `sections/reach.tex` | `817ee9ed88c4d9471d313708a4fc1b186d1e903e692c40c3d7e2d5bdf756a42f` |
| `sections/next.tex` | `2c36f239634b8562ce7e5294e16ff4178e571163b50035ed303185f5973e24cb` |
| `sections/conclusions.tex` | `596dda2e4e628233793e76f972c37e7ba78ff3b7fe8681224c13373a0afca910` |
| `sections/appendix.tex` | `eaf27468e42bc1a28a57a6fdcafd8b7fa58365254e5ad965a794862237e196c6` |
| `sections/availability.tex` | `44f67347836075fb4b6f99d1670ca52bf7ec30499170a87d6a2d19679ac95e3e` |
| `claims.json` | `81d5ddce23c25b9accea366278fd7260c450799d6356aeaee46e6c210ac9202f` |
| `build/main.pdf` (28 pages; the page numbers below) | `d16da0aeaedf1b96ae3988a28509d845a0edb3ca5f9ba4bfaa38a99675a47919` |

**How read.** First, in full: the current `AGENTS.md` on disk (with "The paper", "Writing" and "Review"), Terluna's
editorial charter control-01 (gates G1–G7, section 11, E4) and `STYLE_NOTES.md`. Then the paper once, continuously,
as LaTeX source, in the order `main.tex` assembles it: the title, abstract, introduction, worlds, assumptions,
repairs, verification, results, reach, next, conclusions, appendix, availability. I read as a planetary climate
modeller new to the project. After that single read, to locate and check findings, I consulted `paper/claims.json`
(claims H15, H23, H26, H28, V02, V10, V11, V16, W01, W02, W03, W06, G02, G05, G10, N02), the text of
`build/main.pdf` through pdftotext for page numbers, Figures 1 and 5 as rendered PNGs, text searches of the section
files (negations, stock transitions, run-in heads, repeated numbers, the words "form" and "class") and a cross-count
of Table 2's Form and Repair columns. The reading was silent. `paper/review/` and `paper/notes/` stayed unread: a
directory listing at the start of the session showed the file names in `paper/review/`, and I opened none of those
files. I ran no build, lint or check.

**Counts.** 26 findings: 3 BLOCKING, 16 MAJOR, 7 MINOR. Each finding's heading states what is wrong, with a
"Problem" paragraph where the heading needs detail; "Where" gives the locations, "Why" the rule or evidence at
stake, and "Repair" a proposed change. Line numbers refer to the section files at 4d03a81, page numbers to the PDF
above.

## Findings

### 1. BLOCKING — The reach of the repairs appears as a result; by the paper's own evidence it is a prediction

**Where.** abstract.tex:10–11 ("General repairs ... serve other worlds unchanged"); introduction.tex:59–60 and 63–65
("which another world takes unchanged"; "the three classes set which other worlds the adapted models can reach");
repairs.tex:15–16; reach.tex:4 and 13–14 ("Another world therefore takes the general repairs unchanged");
reach.tex:38–41 ("the adapted CM1 runs storms in Earth-like air at any gravity on its Morrison and NSSL paths, SWAN
and SWASH run water seas at any gravity"); Table 4, row "Gravity other than Earth's" (p19); conclusions.tex:12.
Against them: next.tex:57 ("The repairs have run on the Moon alone"); verification.tex:38–40 and Table 7 (the CM1
gravity pair failed to convect; microphysics similarity open); repairs.tex:53–55 (snow and ice take a larger gravity
exponent than the patch gives them); the "Beyond them" cell of the same Table 4 row (drop limits and breakup);
reach.tex:52–53 ("though none has been run"); claim W01, whose state is "documented", and claim W03, which records
the slow-rotator reach as untested.

**Problem.** The paper's answer to the introduction's second question, which repairs made for one world hold on
another (introduction.tex:29–30), is phrased in the indicative of a measured result. The CM1 sentence states as
achieved a reach that the verification section records as untested and that the same table row places partly beyond
the adaptations.

**Why.** AGENTS.md separates a proposed design from empirical validation and keeps claims within their evidence;
under G5 the evidence state survives at every use. A reader who takes the abstract at its word will treat the
general repairs as validated on other worlds.

**Repair.** State the reach once, as the construction of each repair gives it, with its evidence state, where it
first appears, and keep that state at each later use. Abstract: "General repairs correct units, apply scaling laws
or remove defects and contain no lunar coefficient, so they are built to apply unchanged on another world; every
repair has so far run on the Moon alone." Introduction 63–65: "... and by its class each repair needs nothing, a
table of the new world's column, or a refit before a modeller can use it on another world; the author has run the
repairs on the Moon alone." Reach 38–41: "Taken model by model, the adapted CM1 computes fall speeds, ventilation
and the breakdown field for any gravity on its Morrison and NSSL paths, while its drop limits, breakup and crystal
sizes stay Earth's and its gravity-scaled microphysics is untested; SWAN at a sixth of Earth's gravity and SWASH at
lunar, four times lunar and Earth gravity reproduce their Earth runs under gravity scaling, with Earth's empirical
laws." Table 4 caption: add "The middle column gives the reach each repair was built for; every run so far is
lunar."

### 2. BLOCKING — The paper's central relation is drawn from two comparisons that mix the repair classes

**Where.** reach.tex:3–6; conclusions.tex:11–17; abstract.tex:13–14; results.tex:39–42 with Table 3, row "Sun and
tilt" (p14); results.tex:66–69 with Table 3, row "Longwave test"; Tables 2 and 6 (the ice optics classed General,
the near-infrared water multiplier classed Calibration); reach.tex:9 (the ice optics among the general repairs);
results.tex:44; Figure 5 and its caption (results.tex:52–58, p15).

**Problem.** The conclusions open their second paragraph on the relation that the general repairs moved the Moon
little while the parts another world must remake moved it most ("the two orders run against each other"). Two of the
steps behind it combine classes. The step from the pre-correction run applied the synodic clock and the fixed orbit
(general) together with the recalibrated split of sunlight (a calibration), and the abstract (L13–14) and
conclusions (L12–15) credit its rain change, 2.91 to 2.24 mm a day with dry land rising from 9 to 42%, to the
general repairs alone; claim G02 records the three changes as one step. The longwave test switched on the longwave
correction (a calibration) with the ice optics (General in Tables 2 and 6 and in reach.tex:9), and the conclusions
(L15–17) credit its 11.5 K to "the parts another world must remake", while results.tex:68–69 place most of that
run's cloud gain in high cloud, where the ice optics act. The gas-band calibration moved the Moon 2.2 K, the size of
the cloud-water (2.3 K) and convective-cover (1.8 K) general repairs. Figure 5, the figure for this relation,
colours its bars by sign, marks no class, and leaves out the first calibration, the largest single change (more than
20 K) and the one comparison that separates the classes cleanly.

**Why.** The abstract's result sentence, the opening of the reach section and the conclusions' second paragraph all
depend on this relation. On the runs as reported, the separation is clean for the first calibration against single
general repairs and mixed elsewhere. G5 and AGENTS.md: each claim keeps its conditions and stays within its
evidence.

**Repair.** State the relation on the clean comparisons and name the components of the two mixed steps wherever
their numbers appear; for conclusions.tex:11–17, for example: "Single general repairs moved the Moon's global mean
by 1.6–2.5 K, and the first calibration of its Earth-fitted radiation moved it by more than 20 K. Two steps combined
the classes: the removal of the Sun-clock and orbit defects came with a refit of the split of sunlight and cut the
rain by nearly a quarter, and the longwave correction ran with the ice optics and warmed the Moon by 11.5 K." Add
the two separating runs (the split refit alone; the ice optics alone) to Next work, or bound each share from
existing runs. Redraw Figure 5 with one colour per class and the first calibration as its own bar, on a broken axis
if needed.

### 3. BLOCKING — The class scheme appears in three versions, and the introduction's version contradicts the paper's tables

**Where.** introduction.tex:58–62 ("Each repair falls into one of three classes"); abstract.tex:10–12;
repairs.tex:14–25 (three classes, with settings, capabilities, a bound, a mitigation, avoidances by configuration
and a coupling method "beside" them); Table 2 caption and Repair column (assumptions.tex:143–147; ten kinds,
including "bypassed" and "open"); Table 6 caption (appendix.tex:29–30, "Class:" followed by nine kinds); Table 6
rows "Orbit" and "Whole model days" (General) beside "Breaking, initial state" (Avoidance); the beta plane,
"Bypassed" in Table 2 and "Capability" in Table 6; the ice optics (General) and the leader's crossing (Bound) in the
paragraph headed "Processes and capabilities added" (repairs.tex:134–146); reach.tex:6–9, whose list of general
repairs leaves out Table 2's General rows "Damping, mixing length" and "Flash reach"; the Figure 5 caption
(results.tex:52, "each general repair and calibration after the first") beside a figure that plots the curved air, a
method.

**Problem.** The introduction assigns every repair to one of three classes; the repairs section and both tables
assign many changes to six or seven further kinds. "Class" names three kinds in the prose and nine in Table 6. The
use of an existing configuration switch counts as a general repair for ExoPlaSim's `fixedorbit` and `runsteps` and
as an avoidance for SWAN's breaking. The beta-plane change has two labels.

**Why.** The reach argument is built on the classes, so the reader needs one scheme applied one way. AGENTS.md
records the author's rejection of this overstatement ("The repairs follow one rule ...") with the direction "The
main rule, with the other kinds of repair beside it".

**Repair.** Introduction 58–62: "Most repairs fall into three classes with different reach: ...; settings,
capabilities, a bound, a mitigation, avoidances by configuration and a coupling method make up the rest, and Table 6
assigns each change." Reserve "class" for the three and use "kind" for the rest in the captions of Tables 2 and 6.
Apply one rule to configuration switches (`fixedorbit`, `runsteps`, SWAN's breaking): all three as avoidances by
configuration, or all three as general repairs with the definition widened to include them. Give the beta plane one
label, move the ice optics to the paragraph on physical and scaling laws, and let reach.tex:6–9 refer to Table 6 for
the full list of general repairs or list every General row.

### 4. MAJOR — The arc drops three lines the opening promises

**Where.** abstract.tex:6–7, introduction.tex:56–58 and assumptions.tex:8 (the four forms); introduction.tex:29–30
(the two questions); introduction.tex:65–67 ("the strongest test open to these numbers is agreement among
independent models"); reach.tex:42–44 and 71–75; results.tex:75–97; conclusions.tex:3–27; abstract.tex:4–17 (no wave
result).

**Problem.** (a) The abstract's third sentence and the whole assumptions section are built on the four forms of
Earth value, and no later section uses them. Table 2 contains the relation the conclusions could state: 13 of its 14
rows marked General correct a constant or a unit of time, all four rows marked Calibration correct fits, both rows
marked Method correct geometry, and five of its eleven fits stay open. The conclusions mention none of the forms.
(b) The text states its answer to the second question, by kind of world, at reach.tex:42–44 (of the found worlds
only Earth lies within the adapted models' reach; constructed worlds and exoplanets with air close to Earth's make
up the rest of it) and in the four limits of reach.tex:71–75; the abstract and the conclusions state neither. (c)
The introduction names agreement among independent models as the strongest test open to the lunar numbers; Results
report CM1 3.7 K warmer than the GCM near the ground with the transport imposed, and a box raining about a quarter
of the GCM's rain; the conclusions leave the comparison out. (d) The title names SWAN and SWASH and Results report
the waves, while the abstract reports no wave result.

**Why.** AGENTS.md, "Conclusions and the arc": the abstract, the opening pages and the conclusion promise, develop
and land on the same contribution; charter section 11, pass 10.

**Repair.** End the abstract and the conclusions on the relation among form, class and effect, in substance: "Of the
repairs, 13 of the 14 general ones in Table 2 correct constants or units of time, the methods correct geometry and
the calibrations correct fits; on the Moon, correcting the Earth fits in the radiation changed the climate most, and
another world must refit them." Add one sentence on the reach by kind of world (from reach.tex:42–44, with the
evidence state of finding 1), one on the CM1–GCM comparison as the inter-model test the introduction names, and one
abstract clause on the waves.

### 5. MAJOR — The conclusions replay the paper, and their landing sentence claims more than its steps deliver

**Where.** conclusions.tex:3–9 (restates abstract.tex:7–10 and reach.tex:18–27); conclusions.tex:11–20 (restates
reach.tex:3–6, then lists results in section order: storms, evaporation, lightning, waves); conclusions.tex:22–23
(restates abstract.tex:16–17); conclusions.tex:23–27.

**Problem.** Two of the three paragraphs recite earlier sentences, and the relation that opens the second paragraph
first appears at reach.tex:3–6. The landing sentence states that three steps "would each turn a part that holds near
one column into one that holds wherever its physics does". A radiation scheme built from the reference's
spectroscopy does so. Cloud fitted to lunar cloud-resolving runs yields a new calibration, or a per-world method if
the runs are repeated for each world. An independent code run on the design column tests the accuracy of every
calibration, and each part's reach stays as it was.

**Why.** AGENTS.md: a conclusion gathers the developed lines into a new relation; replaying the section order and
reciting the inventory are excluded; each universal word is checked against what was examined.

**Repair.** Build the conclusions on the relation of finding 4 with its evidence states, let the storm, rain and
wave results enter as measures of what the remaining fits and the gravity scaling change (each with its forcing
state, finding 11), and end on the slow-rotator test of next.tex:57–61, which decides the reach. Split the landing
sentence by what each step changes: "A radiation scheme built from the reference's own spectroscopy would turn the
radiation calibrations into general repairs; cloud fitted to cloud-resolving runs of each world would become a
method with a per-world table; and an independent code run on the design column would bound the accuracy of every
calibration."

### 6. MAJOR — The inventory leaves out the Earth values that moved the Moon most after the radiation

**Where.** Table 2 (assumptions.tex:142–203, p7) and the fits paragraph (assumptions.tex:68–87); results.tex:63–66
("Two of PlaSim's Earth-tuned cloud settings": thinner convective cloud, more low cloud); reach.tex:6; next.tex:19
("PlaSim's humidity thresholds and its cloud-water profile"); conclusions.tex:16.

**Problem.** The cloud settings that Results test, and that the conclusions rank among the largest movers (up to
about 6 K), have no row in Table 2 and no sentence in the assumptions section, and the parameters the tests varied
go unnamed.

**Why.** The assumptions section is where the paper gives its answer to the introduction's first question, where a
model's Earth values lie; an inventory that omits the values found to matter most gives a partial answer.

**Repair.** Add rows to Table 2 for the PlaSim cloud parameters the tests varied, by name, with Form "Fit" and
Repair "open", and give them one sentence in the fits paragraph with their Earth tuning.

### 7. MAJOR — Terms and results appear before the paper defines or gives them

**Where and what.**
- (a) "Earth value" and "defect" run through the abstract, the introduction and the worlds section, which opens on
  "An Earth value in a model holds where ..." (worlds.tex:3); the definitions arrive at assumptions.tex:3–8.
- (b) "PlaSim" first appears at introduction.tex:40 beside "ExoPlaSim"; the relation between them appears only as
  Table 2's header "ExoPlaSim 3.4.2 (PlaSim)". The Sun-clock defect is "ExoPlaSim's" at abstract.tex:8,
  assumptions.tex:102–103 and reach.tex:18, "PlaSim's own Sun clock" in Figure 2's caption (assumptions.tex:133) and
  "PlaSim's Sun clock" in Table 3. A defect report addressed to other users needs one attribution.
- (c) RRTMG appears in Table 1 (p4) ahead of its introduction and citation at assumptions.tex:18.
- (d) The reference model goes by six names: "an in-house line-by-line radiative–convective model"
  (introduction.tex:51), "the in-house reference models" (assumptions.tex:61), "the correlated-k reference"
  (assumptions.tex:80), "the in-house radiative–convective model and its correlated-k emulation"
  (repairs.tex:102–103, which describes it), "the line-by-line model" (repairs.tex:22; verification.tex:51–52) and
  "the in-house correlated-k scheme" (next.tex:43); "an in-house sky solver" (repairs.tex:78–79) enters with its
  relation to the reference unstated.
- (e) Figure 2's caption (p8) uses "the pre-correction run of Table 3" and "the synodic clock" six pages before
  Table 3 (p14) and ahead of the repair's description (repairs.tex:27).
- (f) "CM1's warm offset from the GCM" with its one-third share (repairs.tex:155–156) and "the gap between the two
  models" (verification.tex:106) precede the result itself (results.tex:76–79).
- (g) Table 1 lists CM1 storm results (the freezing level, the storm tops), and worlds.tex:91–92 reports the failed
  gravity pair, ahead of Verification and Results.
- (h) "eleven columns" (assumptions.tex:72), "a water multiplier calibrated on the column's total"
  (assumptions.tex:77) and "the first calibration" (assumptions.tex:79) precede the calibration sequence at
  repairs.tex:107–113.
- (i) "the water scaling" (repairs.tex:11; verification.tex:26; next.tex:80) names the near-infrared water
  multiplier only by way of Table 6, while the cloud-water patch also scales water (`CWSCALE`).

**Why.** G1 (a term used before its definition, a result needed before it is given) and G2.

**Repair.** Define Earth value and defect in the introduction's last paragraph, where the four forms and five
defects first appear. At introduction.tex:42 write "ExoPlaSim 3.4.2 ..., whose physics is the Planet Simulator's
(PlaSim)", and attribute each defect to the layer of code that contains it. Describe the reference once at its first
use (introduction.tex:51–53) with one short name for later use, and name the sky solver as part of it. Move Table 3
to the first use of a state, or describe Figure 2's run in words. Give the 45°N offset in Results alone, and keep
Table 1 to scenario quantities and calculations from them.

### 8. MAJOR — The GCM states go by several names, and two different runs share one

**Where.** assumptions.tex:74 ("the first design run", which is Table 3's "Uncalibrated" state at 315.5 K in year
12, claim H15) against verification.tex:76 ("the first run", a different run with the invented infrared tail, past
320 K, claim H28, absent from Table 3); worlds.tex:74 ("its warmest test"), verification.tex:107 ("a test that
settled near 307 K"), results.tex:72 ("The 307 K state") and next.tex:8–10 ("the settled state", "the warm state"),
all for Table 3's "Longwave test"; verification.tex:85–86 ("the first two 20-year GCM tests of the curved air") for
Table 3's "Curved air" and "Gas bands"; verification.tex:105–106 ("CM1 has yet to be forced from the
longwave-corrected GCM") against next.tex:17–18 ("Forcing CM1 from the design case, with the transport across each
ring imposed, tests first whether the near-ground gap closes"), while results.tex:76–79 already report CM1 forced
from the design case with the transport imposed on the 45°N ring.

**Why.** A reader matches the runs in the prose to Table 3 by name. Two "first" runs with different temperatures
read as a contradiction, and the next CM1 step reads two ways.

**Repair.** Use Table 3's names everywhere. Name the infrared-tail run distinctly ("the run with the extended
spectrum") or add it to Table 3. In Verification and in Next work, state the GCM state the next CM1 forcing comes
from and what it adds to the 45°N runs already made.

### 9. MAJOR — Statements about the field, and universal words, exceed what was examined

**Where.**
- abstract.tex:2–4: "Exoplanets and constructed worlds ... are studied with models built for Earth", a statement
  about the whole field, while introduction.tex:3 scopes the same point to "Some exoplanet climate studies" and
  introduction.tex:25–26 cites THOR, a model written for other planets from the start.
- introduction.tex:9: "Many of the models used in such work", from three examples.
- introduction.tex:8: "Work on constructed worlds asks ...", from McKay et al. (1991) and the author's own project.
- reach.tex:52: "common subjects of exoplanet GCMs", from two studies.
- introduction.tex:63 and results.tex:3–4: "how far each Earth value moved the climate"; the GCM pairs cover six
  repair steps, some of which combine several rows, and four sensitivity tests, against the 38 rows of Table 2.
- reach.tex:29: "each Earth value fails along its own direction".
- reach.tex:36–38: "Released CM1 fails at any gravity but Earth's ..."; the paper shows Earth's constants in four
  routines and leaves unmeasured how far a released run at another gravity departs.
- results.tex:62: "move the Moon further than any general repair did"; thinner convective cloud moved it 1.7 K, less
  than cloud water by pressure (2.3 K).
- verification.tex:3: "each testing something further from the code than the one before"; identity and reproduction
  both test the code alone.
- availability.tex:21–23: "Every number in the prose carries a claim in the register"; Earth's 5–30 C per ground
  strike and Earth's average flash density (results.tex:111–114) appear in no claim text (claim G10 lists the lunar
  values alone).
- availability.tex:26: "every part that may be made public is public", beside model runs held on a private research
  drive and a repository whose address the text omits.
- next.tex:76: "reports that would serve every user of those codes".

**Why.** AGENTS.md, "Claims stay within their evidence", and its first-draft example rejecting a field characterised
from four studies.

**Repair.** Scope each statement to what was examined. Abstract: "Several of the models used for exoplanets and
constructed worlds with air and water close to Earth's descend from Earth models, and an Earth value left in their
code runs to completion with a plausible result." Introduction 8–9: "McKay and colleagues asked how a planet could
be made habitable, and an open project designed a world and asked what its climate would be"; "Several of the models
used in such work descend from Earth models". Reach 52: "the subjects of the slow-rotation studies cited above".
Results 3–4: "how far the case's climate moved as the GCM's Earth values and defects were removed in six steps".
Reach 36–38: "Released CM1 computes with 9.81 m s⁻² in four routines at any gravity, with Earth's 24-hour Sun under
any day, and with Earth's carbon dioxide for the calendar year in any air." Results 62: name the tests that moved
the Moon further. Availability: add the missing claims with their sources, or state the coverage the check tool
measures; give the repository's address and say which records stay private.

### 10. MAJOR — "Other users' runs": a calculation stated as an observation

**Where.** abstract.tex:7–8 ("affect other users' runs"); reach.tex:18 (heading "The defects in other users' runs")
and 18–27; conclusions.tex:7 ("All three act in other users' runs as well"); next.tex:74 (the Sun-clock report, with
its issue record uncited).

**Problem.** The paper derives from the code's arithmetic the conditions under which each defect biases a run (claim
H23, a finding on the lunar runs; claims W02 and W06, calculations), and reports no examination of a run made by
anyone else.

**Why.** Claims stay within their evidence; G5 keeps a calculation distinct from an observation.

**Repair.** "By the code's arithmetic, the three defects bias any run that meets their conditions: ..."; heading
"The defects in other configurations"; cite ExoPlaSim issue #69 (claim N02) where the paper reports the Sun clock to
its maintainers.

### 11. MAJOR — Conditions drop out of the storm, rain and curved-air results

**Where.** results.tex:84–85, 91 and 110 with Table 3: the electrified box and the small box were forced from the
pre-correction run, which ran with the Sun-clock and orbit defects and brought 12% too little sunlight to 0°E.
abstract.tex:15–16 and conclusions.tex:17–20 state the storm, evaporation and lightning results with that condition
gone, generalise "lightning rarer" from one box over two lunar days, and write "five to six times higher than
Earth's" where results.tex:109 compares with Earth's tropics. results.tex:42–46, with Table 3's rows "Curved air"
and "Gas bands" and verification.tex:84–86: both states ran on the ledger's first channels, which put near-infrared
sunlight too high at 66–85 km (19.0 against 10.7 W m⁻²), and the −0.65 K, the −2.2 K and the top layer's 7 K warming
appear with that condition left out.

**Why.** AGENTS.md: technical meaning survives editing, each statement keeps its conditions, and assumptions and
boundaries are stated near the outputs.

**Repair.** Write the forcing state into each sentence that reports these results. Abstract: "... and in a box
forced from a GCM state that still had the Sun-clock and orbit defects, the freezing level stood five to six times
higher than in Earth's tropics and the lightning ...". Results 42–46: "On the ledger's first channels, which put
near-infrared sunlight too high at 66–85 km, the curved air cooled it by 0.65 K ...".

### 12. MAJOR — Two statements about CM1's threads contradict each other as written

**Where.** assumptions.tex:123–126 ("CM1 on several threads departs from itself after a few thousand seconds ..., in
the plain Morrison build as in the electrified one"); verification.tex:21–23 ("the electrified supercell, restarted
on four threads and on two, repeats its fields and its 41 flashes"); Table 7, row "Electrified supercell restarted
on 4 and 2 threads", whose open item is "The lunar boxes' race"; claim H26 (the departures appear in the lunar boxes
at 3,000–7,400 s).

**Why.** The condition that would reconcile the two, the configuration and the time at which the race appears (claim
H26: the lunar boxes, after 3,000 s), is written in the claims register and in one table cell, and in neither
sentence.

**Repair.** Write the condition into both sentences: "In the lunar boxes, CM1 on several threads departs from itself
after 3,000–7,400 s ..."; "the Earth supercell, restarted on four threads and on two over [its window], repeats its
fields and its 41 flashes".

### 13. MAJOR — The expected outcome of the RRTMG step runs the wrong way

**Where.** next.tex:41–46, with verification.tex:45–49 and results.tex:76–82.

**Problem.** RRTMG cools CM1's lowest 1.8 km 4.5 W m⁻² more than the reference, so removing that extra cooling warms
CM1's lowest air, by about a kelvin at the ring's 4 W m⁻² per kelvin. CM1 already runs 3.7 K warmer than the GCM
there, so this step alone widens the near-ground range between the models; the range narrows when PlaSim's longwave
correction warms the GCM as well (results.tex:79–81 estimate PlaSim's share of the offset at about 1.5 K).
next.tex:44–45 state that the range "narrows with it".

**Why.** G5: each proposed study names the result that would change the design, and a reversed expectation
misdirects the test.

**Repair.** "If extended tables remove most of the 4.5 W m⁻², the extrapolation was the cause, and CM1's lowest air
warms by about a kelvin; with PlaSim's longwave correction warming the GCM, the near-ground range that remains
measures the two models' boundary layers."

### 14. MAJOR — Benchmark comparators and external Earth values go uncited

**Where.** verification.tex:60–63 and Table 7 ("published runs of the same charging and lightning schemes", "a
published 27–40", "0.33% in a published run"); verification.tex:52–53 ("PyRADS", "a Monte Carlo reference");
verification.tex:65–66 ("Earth's measured fair-weather positive conductivity"); results.tex:111–114 (Earth's average
flash density; Earth's 5–30 C per ground strike); next.tex:28 (LBLRTM, a DISORT-based solver); next.tex:74 (the
Sun-clock report).

**Why.** A reader weighs a benchmark by its comparator and finds the comparator through the citation.
`references.bib` already contains Koll and Cronin (2018) and Mansell et al. (2002, 2005), uncited in the text, and
the introduction cites Mansell et al. (2010) and Fierro et al. (2013) for WRF-ELEC.

**Repair.** Cite each comparator at its comparison: the published electrification runs by author and year, the
PyRADS paper, the Monte Carlo reference, the source of the measured conductivity, of Earth's flash density and of
Earth's charge per ground strike, LBLRTM and DISORT, and ExoPlaSim issue #69.

### 15. MAJOR — The same numbers and caveats recur across sections, and two pairs of sections cover the same ground

**Where.**
- The longwave correction fitted at 295 K and used near 307 K with twice the vapour: worlds.tex:74;
  verification.tex:107; results.tex:58, 68 and 72; reach.tex:48; next.tex:8–9 and 13; conclusions.tex:17; Table 7.
  Home: Results, with one clause in Next work.
- The reference unchecked by an independent code for carbon dioxide, oxygen, collision-induced absorption and
  sunlight: verification.tex:54–55 and 104–105; next.tex:26–27; Table 7. Home: Verification; Next work names the
  test.
- CM1's thread race: assumptions.tex:123–126; repairs.tex:33–34; verification.tex:100 and 109; next.tex:76; Tables 2
  and 7.
- The horizon air mass (35 against about 7 and 13.5): introduction.tex:40; Figure 1 caption; Table 1;
  worlds.tex:77–78; assumptions.tex:57–59; Table 2; repairs.tex:86–88; Figure 3 caption; reach.tex:30–31; Table 4.
- SWAN's wind-input patch identical to stock at standard gravity: repairs.tex:9–10, 41–42 and 64–66;
  verification.tex:23; Table 6.
- The 45°N transport as a third of the warm offset: repairs.tex:155–156; results.tex:76–79; Figure 6 caption.
- The failed gravity pair: worlds.tex:91–92; verification.tex:38–40; Table 7.
- Fall speeds at lunar gravity: worlds.tex:86–87; repairs.tex:52–53; Tables 1 and 2.
- The 0.6 m soil wave: worlds.tex:92–94; assumptions.tex:44–45; Table 2; repairs.tex:69–70; Table 4.
- The curved-geometry budget: assumptions.tex:52–56; repairs.tex:81–83; Table 2; results.tex:43.
- The uncalibrated run passing 310 K: assumptions.tex:74–75; results.tex:34–35; Table 3.
- The byte-for-byte rebuild: repairs.tex:43–47; verification.tex:23–26; Table 7.
- RRTMG's 1,053.63 hPa and the 7.5 km extrapolated: Table 1; assumptions.tex:84–85; Table 2; reach.tex:72–73; Table
  4; next.tex:41–43.
- Section level: worlds.tex:72–96 (paths, gravity and day as they bear on code) and the geometry, constants and
  units-of-time paragraphs of the assumptions section; verification.tex:104–111 ("Checks still to make") and Next
  work, item by item.

**Why.** G2 and charter pass 8 (redundancy); AGENTS.md's delete test. Spread over five sections, the repeated 307 K
caveat forms a caveat wall.

**Repair.** Give each number and caveat one home and refer to it elsewhere. Let the worlds section keep the ratios
and the scenario, and give their consequences for the code in the assumptions section alone. Merge "Checks still to
make" into Next work.

### 16. MAJOR — Section boundaries join by sequence alone, and run-in heads appear where transitions belong

**Where.** worlds.tex:96 → assumptions.tex:3 (the lunar tilt, then a definition); assumptions.tex:126–128 →
repairs.tex:3 (the sixth fault, then the rule for switches); repairs.tex:162–166 → verification.tex:3 (SWASH's
inputs, then six kinds of check); verification.tex:110–111 → results.tex:3 (an independent GCM, then sensitivities);
reach.tex:75–76 → next.tex:3 (Table 4's narrower limits, then the two largest sensitivities); next.tex:79–81 →
conclusions.tex:3 (the record's open items, then the Moon recapitulated). Of the section openings, Reach's
(reach.tex:3) alone receives a relation from the section before. The body has 37 bold run-in heads (assumptions 5,
repairs 7, verification 7, results 4, reach 5, next 9), and next.tex:3–4 declares the items after the third
unordered.

**Why.** Under G3, inheritance applies across paragraphs and sections; under AGENTS.md, transitions come from the
subject matter and a genuine catalogue goes in a table or a list.

**Repair.** Close each section on the question the next takes up. Worlds: "The code of a model built for Earth fixes
these ratios at Earth's values in four ways: through constants, units of time, geometric simplifications and fits."
Assumptions: one closing sentence on what each form needs from a repair (a law or a unit for constants and time, a
table of the column for geometry, a refit for fits), which the class paragraph of Repairs then develops. Repairs:
what each class needs as evidence (identity for switches, similarity for the gravity scaling, the reference for
calibrations). Verification: what the checks leave to the climate runs. Reach: the untested transfer and the
slow-rotator test that would decide it. Give Next work's unordered steps a table with the columns question,
comparison, and result that would change the design or the reach, and keep prose for the ordered steps.

### 17. MAJOR — Project chronicle and bookkeeping make several passages read as an internal report

**Where.** Chronology: assumptions.tex:74 ("the first design run, with 25% seas"); repairs.tex:107–113 ("Each
calibration was made to remove the residual of the one before"; "Once the Sun-clock and orbit defects were found");
repairs.tex:153–155 ("The first box"); verification.tex:73–92, the whole paragraph "What the checks caught" (the
runner's spectrum, the first electrified build, the first lunar gravity patch "until a code review found the
omission", the first terrain build, "The last two remain in the runs made before they were found"). Bookkeeping:
patch numbers in prose (repairs.tex:27–29; verification.tex:27; next.tex:80); runners inserting changes "at a marked
anchor", "the deployed ExoPlaSim installation", "the eight lunar CM1 builds", under the heading "Constants to
parameters" (repairs.tex:42–47); "condensed from the code repository's record" (appendix.tex:5); "awaits a reply",
"await reports", "The record itself needs ..." (next.tex:74–81); an unaddressed "world-crafting repository", "the
project's research drive" and "Terluna's decisions register" (availability.tex:3–16). Local names: "the twilight
pair", "the electrified box", "the site where the rings cross the equator at 0°E". Table 3's run names, "those of
the data extracts".

**Why.** AGENTS.md, "The paper": the paper stands alone as a field paper on modelling Earth-like worlds beyond
Earth's range, and Terluna enters as provenance only.

**Repair.** Recast verification.tex:73–92 as the kinds of adaptation error a modeller should test for, each with the
check that caught it (a solar spectrum extended past its tabulated end; a discharge applied once per step after all
of the step's charging; a gravity scaling of fall speeds that left the ventilation at Earth's; a spectral grid
averaged over windows and opaque lines), and say which reported results still contain an uncorrected error. Move
build mechanics and patch numbers to Table 6 and Availability, and the open reports and the record's to-do list to
the repository; give the repository its address. Replace project nicknames with descriptions at first use.

### 18. MAJOR — Inventory and method are heavy; reach and the inter-model test are thin

**Where.** assumptions.tex:15–128 with Table 2 (pp. 4–8; the prose walks through many rows the table already lists);
repairs.tex:72–121 (channel counts, shell counts, elevation grids, the calibration's history); the reach section
(about two pages of inference and one table, answering the introduction's second question); results.tex:127–134 (the
waves in one paragraph, while the six figures concern the ratios and the atmosphere, though two of the four models
are wave models); the conclusions (three paragraphs).

**Why.** G2 (explanatory economy) and the charter's E1 (scope proportionate to the contribution): the abstract and
introduction promise a field contribution on reach, and most of the paper's length goes to the case's inventory and
method.

**Repair.** Let Table 2 contain the inventory, and let the prose develop each form through one or two cases with
their consequence on the Moon. Move the ledger's and the calibration's numerical method to the appendix. Give the
reach section the relation of finding 4, the evidence states of finding 1 and the slow-rotator test.

### 19. MAJOR — Empty actions, witticisms and defensive phrases recur after the author rejected the same patterns

**Where (representative).**
- Empty actions on abstractions: "The adaptation found" (abstract.tex:6); "Adapting the four models found"
  (introduction.tex:56); "Work on constructed worlds asks" (introduction.tex:8); "the three classes set which other
  worlds the adapted models can reach" (introduction.tex:64–65); "Five defects sit in the released codes"
  (assumptions.tex:101); "The other two lie outside the Earth values" (assumptions.tex:120); "The results sort ...
  and the classes of repair sort" (reach.tex:3–4); "travel with their inputs", "travels as a bound", "travel as a
  method" (reach.tex:10–12) and "how far each travels" (conclusions.tex:11–12); "rests on" (next.tex:8, 26 and 63;
  results.tex:94); "await reports" (next.tex:76); "The adaptation introduced defects of its own"
  (verification.tex:73); "The strongest evidence about gravity comes from" (verification.tex:30).
- Witticisms and informal turns: "the two orders run against each other" (conclusions.tex:11); "three other suspects
  were tested and cleared" (results.tex:85); "big, slow waves" (results.tex:128); "for one" (introduction.tex:40);
  Figure 1's annotations "35: right here" and "per-day formulas right".
- Defensive phrases: "Such a value is a limitation of the code, which does what it was written to do, for the world
  and range it was written for" (assumptions.tex:4–5); "an unfunded personal project that earns the author nothing"
  (availability.tex:25–26).
- Reader management: next.tex:3–6 ("The first two steps below ... Each names the question it settles ...");
  results.tex:4–5.

**Why.** AGENTS.md, "Exact action" and "No witticisms", with the first-draft examples "Terluna asks ..." and "Three
model families divide the work ...", which these sentences repeat in pattern.

**Repair (examples).** "The author found Earth values in four forms ..."; "McKay and colleagues asked how a planet
could be made habitable"; "by its class each repair needs nothing, a table of the new world's column, or a refit";
"The author found five defects in the released codes"; "On the Moon, correcting Earth fits changed the climate most,
and another world must refit them"; "Leakage and the forcing methods take a conductivity column or a GCM's fields as
input"; "Rain in each model depends on Earth fits of its own"; "three other causes were tested and excluded"; "large
waves of long period"; "Such a value is a limitation of the code."

### 20. MINOR — Names and terms that a reader outside the project needs defined

**Where.** "Sun clock" (abstract.tex:8, defined at assumptions.tex:102–107); "lunar model day" (abstract.tex:9;
ExoPlaSim's day of 29.8 Earth days against the 29.53-day solar day, explained at assumptions.tex:41–42 and 112);
"the ledger" (repairs.tex:72); "the split of sunlight" (repairs.tex:111); "points" for percentage points
(assumptions.tex:71); "the leader's crossing" and "leakage" (repairs.tex:142–143); "the knee" (assumptions.tex:31);
"the design" for the world's design (worlds.tex:32–33; next.tex:13); "a tall air" (introduction.tex:61); "Earth
assumptions" for Earth values (Figure 1 caption, worlds.tex:18); "cone" in Figure 5's label "Curved air: twilight,
cone and slant path", absent from the text; "0.19 K of ground from water's lines" (Table 7, appendix.tex:116),
absent from the prose; "The Sun's clock" in Figure 5 against "Sun clock" in the text.

**Repair.** Define each at first use in one phrase or use the plain term ("percentage points", "a tall atmosphere",
"ExoPlaSim's model day of 29.8 Earth days").

### 21. MINOR — Prose catalogues and bead strings (representative)

**Where.** worlds.tex:85–89 (four gravity consequences in a semicolon chain); assumptions.tex:15–38 (constants model
by model); reach.tex:6–9 (the general repairs listed in prose); results.tex:110–117 (530 flashes, a fifth to ground,
149 C, the charge arrangement, hail's share, each a separate proposition); next.tex:74–81.

**Repair.** Use tables or lists where the order is arbitrary; elsewhere write the relation into the syntax. In the
storm paragraph, for example, let the charge arrangement at five to six times Earth's height account for the flash
heights and for the charge each ground strike lowers.

### 22. MINOR — The kinds of check differ between abstract and verification, and the announced order differs from the order given

**Where.** abstract.tex:12 (four kinds: identity, reproduction, similarity, benchmark); verification.tex:3–12 (six
kinds, "each testing something further from the code than the one before", arithmetic third); verification.tex:57–71
(arithmetic last, merged with benchmarks); verification.tex:8–10 and 42–55 ("calibration" as a kind of check, while
a fit's residual on its own columns tests the fit alone and the comparison on the eleven unseen columns is the
check).

**Repair.** One list of kinds in one order in both places; call the out-of-sample comparison "a check of the
calibration on unseen columns".

### 23. MINOR — Numbers that differ between places, with the reason unstated

**Where.** The curved geometry's clear-sky loss, 5.8 W m⁻² (assumptions.tex:54) against 5.4 (results.tex:43, from
the first channels); the horizon air mass, 7.1 by straight rays (worlds.tex:78) against 7.2 by Chapman's factor
(Table 1; reach.tex:31); 8.3% short over 270–57°E (Figure 2) against "12% too little sunlight" at 0°E
(results.tex:84); high cloud at 180–204 K (assumptions.tex:83) against 165–217 K (Table 2); CM1's rain "near a fifth
of the GCM's" (next.tex:54) against 34 mm beside the forcing GCM's 129 mm, about a quarter (results.tex:92); "a test
of convergence in frequency" (next.tex:70) against a "time-step criterion" (verification.tex:97); "Both dynamical
cores hold gravity constant in a thin shell" (next.tex:33) against CM1's flat slab (assumptions.tex:60); "Two of the
storm results" (results.tex:119), the second of which concerns night fog and the 2 m temperature; "Each ground
strike lowered a median 149 C" (results.tex:113).

**Repair.** State the condition that separates each pair, or use one number.

### 24. MINOR — The worlds section is headed for the field and written mostly about the case, and its dimming convention differs from the one Results use

**Where.** worlds.tex:1 (heading) against worlds.tex:29–96 (the lunar scenario, paths, gravity and day);
worlds.tex:32–33 ("a change in the physics therefore appears as a change in the dimming the design needs") against
results.tex:33–47 and Table 3, which report each change as a temperature change at fixed sunlight and reset the
dimming once, for the design case.

**Repair.** Title the section for both parts (e.g. "Worlds beyond Earth's range and the lunar case") or split it;
state that sunlight is held fixed in the sensitivity runs and reset once, for the design case.

### 25. MINOR — Layout and figures (for the G7 review)

**Where.** The appendix section contains one sentence on p21, and its three tables float to pp. 22–24 among the
availability statement and the references; Table 5 is cited in the introduction (p2) ahead of Tables 1–4; the right
panel of Figure 1 shows present Mars as an open marker, which the caption reserves for constructed or illustrative
worlds.

**Repair.** Place the appendix tables after a page break as a block; cite the configuration table from the appendix,
or number it first; draw present Mars as a filled marker.

### 26. MINOR — Availability and review history

**Where.** availability.tex:5–7 (the world-crafting repository, whose address the text omits, "whose release commit
will be recorded"); availability.tex:33–35 ("Its editorial rounds by fresh reviewer agents ... are recorded in the
repository's review folder", in the present tense while round 1 is under way at this commit).

**Repair.** Give the repository's address and record the release commit when it exists; write the review history in
the tense of the work done at each release.

## Gate notes for the whole paper

**G1, argument and reorderability.** The sections follow the order of a method report (setting, inventory, repairs,
checks, results, reach, next work), and of the section openings, Reach's alone receives a relation from the section
before. Swap tests: the four form paragraphs of the assumptions section trade places without loss; in Repairs,
"Defects removed or avoided" trades places with "Constants to parameters", and "Processes and capabilities added"
with "Forcing a slice of the GCM"; in Reach, "The defects in other users' runs" fits at any position; Next work
declares its later items unordered; Verification announces an order its subsections leave. Definitions and results
arrive after their first use (finding 7), the central relation is drawn from mixed comparisons (finding 2), and the
conclusions replay (finding 5).

**G2, audience and explanatory economy.** The content addresses specialists, and several explanatory sentences
supply premises such a reader needs (the capillary length of the largest stable drop, the Best-number scaling of
fall speeds, the Chapman factor). Internal names (finding 20), project chronology and bookkeeping (finding 17),
method detail in Repairs (finding 18), repeated caveats (finding 15) and reader management in the openings of
Results and Next work (finding 19) fall outside that economy.

**G3, inheritance, transitions and cadence.** Searches of the section files find none of the excluded stock
signposts ("Moreover", "In addition", "Notably", "Furthermore", "It is worth"); "therefore" appears six times.
Section boundaries join by sequence (finding 16), 37 run-in heads in the body appear where transitions belong, and
prose catalogues and bead strings recur (finding 21). This was a silent reading; the read-aloud requirement for the
major transitions, the dense passages and the conclusions remains open.

**G4, affirmative stance and exact action.** A search of the twelve section files finds no "not" and no "rather
than"; the remaining negations ("without a warning", "without the patch", "without fixing the orbit", "without
refitting") express propositions, and "runs without failing" (abstract.tex:4) has its affirmative form, "runs to
completion", at introduction.tex:28–29. Physical processes stay visible through most of the text; the people who did
the work appear in the introduction (the developers of earlier ports) and in Availability, and elsewhere the
author's operations are written in the passive. Empty actions, witticisms, defensive phrases and promotional
universals recur (findings 9 and 19).

**G5, technical meaning, evidence status and discriminating tests.** The introduction and Verification keep
reproducibility apart from physical validation, Verification lists the checks still to make, and most steps of Next
work name a question, a comparison and the result that would change the design or the reach. The reach appears at a
stronger evidence state than the paper's evidence supports (finding 1); the central relation is drawn from
comparisons that mix classes (finding 2); conditions drop from the storm, rain and curved-air results (finding 11);
the defects' effect on other users' runs is a calculation stated as an observation (finding 10); one expected
outcome runs the wrong way (finding 13); and two statements on CM1's threads contradict each other as written
(finding 12).
