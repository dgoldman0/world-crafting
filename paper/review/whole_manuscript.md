# Whole-manuscript challenge

**Scope.** The manuscript as `paper/main.tex` assembles it from the eleven files in `paper/sections/`, at
world-crafting HEAD d090154; the section sources are unchanged since d1c067a. Sources reviewed (sha256):
`main.tex` a693a6b2…653e; `abstract.tex` eb0ef5cc…9c30; `introduction.tex` eea9d2dd…c82d; `regime.tex`
a805c60f…77e9; `hidden_earth.tex` 44b40cdd…ea98; `repairs.tex` 9c808a71…6a21; `verification.tex`
f945dab4…f331; `results.tex` cd52505e…8138; `reach.tex` 88db8a8e…238e; `next.tex` d016d6d1…4042;
`conclusions.tex` b63062b6…eae5; `availability.tex` bebcd367…97c2; `claims.json` d437d9b4…3ea1. The existing
build, `build/main.pdf` (sha256 475c9cb9…f95d, 24 pages, built 16:47), was read as text and left unrebuilt.
Line numbers below are those of the section files.

**Date.** 2026-10-17.

**Reviewer.** A Claude subagent (Claude Opus 5.5) acting as whole-manuscript challenger. It is the same model as
the drafting assistant and the two technical referees, so this record is a separate pass by the same model and
counts as no independent or human review. It also differs from the fresh-reader review AGENTS.md now requires:
this reviewer read the review records, the notes and Terluna's records along with the text.

**Read.** In order: `main.tex` and the eleven section files; the PDF's text (`pdftotext`); the editorial charter at
Terluna 186b294 (sha256 aac4a4f2…80b0), gates G1–G5, section 11 and E4; the author's brief as the main session
gave it; for context, `review/README.md`, `referee_dispositions.md` and the nine `passes_*.md` records. To test
specific points: `claims.json`; `notes/reference_radiation.md`, `exoplasim.md`, `cm1.md`, `electrification.md`,
`defect_log.md` (summary table), `verification_record.md` (sections 4–7); `models/exoplasim/README.md`;
`paper/data/repairs.json`; and, by `git show` at 186b294, Terluna's `climate/crm/README.md` (lines 120–132,
362–372, 945–960, 1100–1215, 1845–1856, 2355–2400) and `climate/waves/README.md` (lines 10–64).

AGENTS.md changed while this review ran (d090154: the paper's standalone framing, the writing rules, and eight
first-draft passages the author rejected on 2026-10-17). It was read and applied as the latest author
instruction; B1 rests on it, and the writing rules also governed this record.

**Done and left undone.** Read-only work: no build, model run or test. The commands were `grep`, `sed`,
`pdftotext` on the existing PDF, `git show` and small word counts in Python. Claims the technical referees
dispositioned were taken as settled, except where two places in the manuscript disagree. Left undone: the
audible cadence review (the author's), G6 source admission, G7 visual review of the PDF, and a claim-by-claim
re-referee.

## BLOCKING

### B1. The framing and the eight passages the author rejected on 2026-10-17 remain

**Location.** `main.tex`:1, 31 (title), 2 and 33 (Paper ID, printed under the title); abstract.tex:2–7;
introduction.tex:3, 11, 23, 36; regime.tex:3, 16, 24, 56, 70, 76; hidden_earth.tex:1, 18, 24, 28, 30–31, 87,
161; repairs.tex:3; results.tex:3–4; reach.tex:3, 15, 39–40, 47, 57; next.tex:3; conclusions.tex:11, 21.

**Problem.** AGENTS.md (d090154) sets the paper as a standalone field paper on modelling Earth-like worlds beyond
Earth's range: exoplanets and constructed worlds whose air and water resemble Earth's while their gravity, size,
day or starlight differ. The breathable Moon is its worked case, Terluna enters as provenance only, and Paper IDs
and ensemble language stay outside the paper. The manuscript runs the other way. The title ends "adapted to a
breathable Moon", the abstract and the introduction open on Terluna's Moon and its question, and the worlds the
work serves first appear in the eighth section. All eight rejected passages stand in the text:

| Rejected passage | Where it stands |
|---|---|
| Title "Earth inside the models: ..." | `main.tex`:31, and the comment at :1 |
| "Terluna asks what weather, climate, storms and seas ..." | introduction.tex:3 |
| "The microphysical and surface laws carry Earth in the same way." | hidden_earth.tex:87 |
| "... and where the uncertainty that remains now sits." | results.tex:4; the same phrase at next.tex:3 |
| "Three model families divide the work, each answering where the previous one stops." | introduction.tex:23 |
| "Carrying these models to the Moon exposed Earth inside them in five forms" | introduction.tex:36; abstract.tex:3–6 in the same form |
| "The repairs follow one rule ..." | repairs.tex:3 |
| "Each constant is right for Earth, and can be made right for the Moon as far as its lunar value is known." | hidden_earth.tex:30–31 |

The Paper ID prints under the title (`main.tex`:33). "Open Moon", the ensemble's name, labels Table 1
(regime.tex:16, 24), Figure 6's legend and caption (reach.tex:39–40) and a reach group (reach.tex:47). Terluna
appears beyond provenance at abstract.tex:2, introduction.tex:3, regime.tex:3 and reach.tex:57 ("as Terluna's
analyses already allow for"). The empty action the author named, an abstraction acting, recurs beyond the eight
examples: the heading "Where Earth hides in the models" (hidden_earth.tex:1); "Earth sets two thresholds" (:18);
"Earth's seas set SWAN's constants" (:24); "Earth's composition and rotation complete the set" (:28); "The Moon
makes that question hard" (introduction.tex:11); "Gravity and the calendar strain everything else"
(regime.tex:56); "The questions each model owns" (regime.tex:70); "The line-by-line model stands behind"
(regime.tex:76); "The two classes of repair reach differently. A general repair carries to other worlds"
(reach.tex:3); "The adapted models place the climate's largest remaining uncertainty" (abstract.tex:16); "The
repairs that removed this Earth" and "The adapted models have located the uncertainty" (conclusions.tex:11, 21).
The coined term "hidden Earth" (Table 2's caption, hidden_earth.tex:161; reach.tex:15) carries the title's
witticism through the body.

**Repair.** Reframe first, since the later passes would otherwise polish text that must change.
(a) A title that names the subject in the author's direction, for example "Modelling Earth-like worlds beyond
Earth's range: ExoPlaSim 3.4.2, CM1 r22 with WRF-ELEC, SWAN 41.51 and SWASH 12.01 on a breathable Moon"; drop the
Paper ID from `\date` and from the source comment.
(b) Open the abstract and the introduction on the field's need, with the stakes for other users of these codes
that B3 and M8 locate; name the breathable Moon as the worked case, and Terluna once, as the project that designed
it, with its citation.
(c) Replace "Open Moon" with "the breathable Moon" or "the lunar design case".
(d) Name the forms of Earth value for what they are (B3), and retitle the section and Table 2 to match, for
example "Earth values in the released codes".
(e) Rewrite each rejected passage along AGENTS.md's direction, and give each empty action its agent and
operation: hidden_earth.tex:18 becomes "WRF-ELEC's lightning holds two thresholds and a time step set for Earth's
air"; reach.tex:3 becomes "A general repair takes its value from a unit, a scaling law or corrected code, so
another world can use it unchanged; a calibration was fitted to one column".
(f) Then run the fresh-reader round AGENTS.md requires. This challenge read the records with the text and so
stands outside that round.

### B2. The repair classes disagree between the defining sentences, the reach section and the tables

**Location.** abstract.tex:9–13; introduction.tex:39–44; repairs.tex:12–17, 19–22; reach.tex:3–12;
conclusions.tex:11–14; Table 2's State column (hidden_earth.tex:162–165, 175–217); Table 3's Class column
(repairs.tex:144–149, 159–203).

**Problem.** The headline claim is two classes of repair with different reach, and the class of a change differs
by place:

- *The curved geometry.* General in the abstract ("restore the curved geometry ...; they carry to other worlds",
  :11–13), the introduction ("restores a missing geometry", :40), repairs.tex:13 and the conclusions ("a
  geometry", :12). "Method, lunar table" in Tables 2 and 3, and "between the two" at reach.tex:8–9, where another
  world "needs ... its ledger ... made again" (:10–11).
- *Added processes.* General in the same four sentences ("add missing processes"; "restores a missing ...
  process"; "a missing process"). Table 3 classes leakage, infrared from space, the WRF-ELEC graft, point
  discharge and every forcing method as Capability, a kind that introduction.tex:43–44 and repairs.tex:15–17 set
  beside the two classes, while ice optics, also an added process, is General. The text gives no criterion that
  separates a missing process from a capability.
- *Reach's list.* reach.tex:4–7 counts leakage and "the methods that force a slice of a GCM" among the general
  repairs; Table 3 classes them Capability.
- *Sun clock, fixed orbit, whole model days.* "three settings that carry the Moon's orbit and calendar" at
  repairs.tex:20–22; General in Tables 2 and 3 and at reach.tex:4–5. The Sun clock is patch 04, a source change
  (`models/exoplasim/README.md`), and verification.tex:88 calls it a patch. The year of 17,160 steps is a lunar
  value, which repairs.tex:14–16 defines as a setting.
- *Soil.* Setting in Table 3 (repairs.tex:178); a repair that restores "the quantity each formula was written for"
  at repairs.tex:48–52; reached by the adaptations in Table 5 (reach.tex:88).
- *The other kinds.* Four at introduction.tex:43–44 and five at repairs.tex:15–17; Table 2's caption adds
  "bypassed" and "open", Table 3's "a coupling method", and both captions carry "a general method with a lunar
  table", a third class the prose omits. The beta plane is Bypassed in Table 2 (hidden_earth.tex:200) and
  Capability in Table 3 (repairs.tex:186).

A reader of the text alone has no way to learn which changes another world can take unchanged, and the reach
statements of the abstract and the conclusions rest on exactly that.

**Repair.** Settle one taxonomy and apply it in every place listed. A form that fits the tables: three repair
classes, each with its reach — general (a unit, a scaling law or corrected code; carries unchanged); general
method with a per-world table (the curved air; carries as a method, its table recomputed for each column);
calibration (coefficients fitted to the reference on the design columns; refitted for each world) — and the other
kinds defined once (setting, capability, bound, mitigation, avoidance, coupling method). State the criterion that
puts a computed table (the curved air) and a fitted coefficient (the gas bands) in different classes. Then rewrite
abstract.tex:9–13, introduction.tex:39–44, repairs.tex:12–17 and conclusions.tex:11–14 to that list; correct
repairs.tex:19–22 (ten patches with the Sun clock among them, and two settings, `fixedorbit` and `runsteps`, each
with its class); move leakage and the forcing methods at reach.tex:4–7 to the capabilities, which carry with their
inputs; settle the soil and the beta plane; give both captions the same list.

### B3. The defect–limitation distinction rests on a definition its own defects fail, and folds defects into the forms of Earth value

This is part (2) of the brief.

**Location.** hidden_earth.tex:3–10, 33–39, 99–117 and Table 2's Form column (:175–217); abstract.tex:6–9;
introduction.tex:36–39; conclusions.tex:5–6; verification.tex:74–75; next.tex:55–58.

**Problem.**

- *Definition against examples.* "In a defect the code is wrong on its own terms, on every world"
  (hidden_earth.tex:8–9). The two headline defects hold on Earth: the Sun clock skips "none at ExoPlaSim's default
  of one day" (:103) and "is exact at a one-day rotation" (conclusions.tex:5–6); the orbit substitution "on Earth
  ... is invisible" (:110).
- *Two axes in one list.* Four forms say where an Earth value sits (constant, unit of time, geometry, fit); the
  fifth, defect, is a verdict on the code. The Sun clock is itself a units-of-time error (the hour angle runs at
  the sidereal rate within a model solar day), and the orbit default is an Earth constant; Table 2's single Form
  column records one or the other.
- *Defects outside Earth.* The section counts as Earth's a value that "agrees with Earth because Earth set it"
  (:3). Two of the five released-code defects have "their tie to Earth's values unknown" (:113: CM1's thread race,
  PlaSim's cold lowest level), and SWAN's breaker parameter was hidden by a usual configuration and exposed by a
  repeatability test with breaking off (:110–113; verification.tex:74–75), independently of the lunar conditions.
  The abstract (:6–9) still counts "latent defects" as a form of Earth inside the models and names SWAN's among
  them, and Table 2 lists all five as "hidden Earth".
- *The criterion applied unevenly.* ExoPlaSim converts convective rain with the model's solar day
  (`zrfac = solar_day * 1000`; `notes/exoplasim.md`, convective cover) for a fit made per Earth day: a unit error
  wherever the day differs from one Earth day, with the same structure as the Sun clock's. The paper classes it a
  limitation (Time; hidden_earth.tex:33–39, 178), and the upstream reports omit it (next.tex:55–58). The stated
  definition places it among the defects, while the defect log's classes put unit errors with the Earth values;
  the text has to decide the case.

**Repair.** Make kind (defect or limitation) an axis separate from form. Define a limitation as code that is
correct for the world and range it was written for, and a defect as code that contradicts its own inputs, units
or intent (it ignores a configured value, restarts a clock it should carry, reads memory never set), even where
Earth's values or usual settings make the error vanish. Keep four forms of Earth value
(constants, units of time, geometry, fits beyond their range) and add a Kind column to Table 2: the Sun clock,
Time and Defect; the orbit default, Constant and Defect; SWAN's breaker parameter, a defect a configuration hides;
the thread race and the cold lowest level, defects outside the Earth inventory, in a short paragraph of their own;
the convective-day conversion decided explicitly, either as a defect with an upstream report or as a limitation
with the reason given. Rewrite abstract.tex:6–9 and introduction.tex:36–39 to match, for example "Earth's values
sit in four forms ...; the codes also held five latent defects, two of which Earth's own values hide". Part (2)
of the brief is weakest here, and with the axis separated it becomes the paper's clearest result.

### B4. Verification omits the reference model's own checks and the cross-check it still lacks

This fails G5 and AGENTS.md's "Report actual checks and unperformed work".

**Location.** verification.tex:9–10, 53–56, 84–93; Table 4's calibration rows (verification.tex:119–123);
next.tex; introduction.tex:31–34; repairs.tex:84–89; the ranking of uncertainties at abstract.tex:16–19,
results.tex:35–43 and conclusions.tex:21–25.

**Problem.** Every GCM calibration and the CM1 radiation check rest on the in-house line-by-line model.
verification.tex:53–56 states "The reference bounds them all" and that the model "rests on the HITRAN lines and
MT_CKD". The record holds more: its only cross-code check, PyRADS, covers water-only longwave at constant gravity;
no independent code checks its CO2, O2, collision-induced or solar calculation on the lunar column; the Monte
Carlo Rayleigh reference stops at Rayleigh depth 1.5, where the lunar column reaches about 4 at 360 nm
(`notes/reference_radiation.md`:20–26, and first under "Room for improvement", :271–276). Verification, its
"Checks still missing" (:84–93), Table 4 and Next work all leave this out, so the ranking of the climate's
uncertainties rests on a reference whose own cross-check the reader never meets.

**Repair.** (a) In Verification's calibration paragraph, give the reference's checks with their scope:
correlated-k against line-by-line (as now), PyRADS for water-only longwave at constant gravity, Monte Carlo
Rayleigh to depth 1.5, and no independent check of CO2, O2, collision-induced absorption or sunlight on the lunar
column. (b) Add the full-column cross-check to "Checks still missing" and to the "Leaves open" cells of Table 4's
calibration rows. (c) Add it to Next work with its discriminating result: the design column against an
independent code (LBLRTM for the longwave and a DISORT-based solver for the sunlight, as the note proposes); layer
heating or a sunlight split departing from the reference by more than the calibration residuals (0.97 W m⁻² rms by
layer, 0.6 points in the split) would require refitting the multipliers and the gas bands and resetting the
dimming. (d) Attach "given the reference's spectroscopy" once to the ranking of uncertainties.

### B5. Next work states that each step names its question, comparison and design-changing result; five of its seven paragraphs fall short

This fails G5's test for proposed studies.

**Location.** next.tex:3–5 (the statement), 20–22, 32–36, 38–44, 46–53, 55–61.

**Problem.** G5 asks every proposed study to name what it discriminates and the result that would alter the
design, and next.tex:4–5 states that each step does. Three steps meet it: the longwave at the settled state
(:7–13), the cloud refit (:15–20) and the tall air's dynamics (:24–30). The rest fall short:

- The independent GCM (:20–22) names what it would show and no outcome that changes the design.
- Radiation in CM1 (:32–36) ends on a consequence ("would move the near-ground temperatures") with no threshold
  or decision.
- Microphysics (:38–44) gives an expected outcome ("larger drops ... would narrow the rain gap") in place of a
  design consequence.
- The charging measurement (:46–49) settles the sign and names no use of the sign; the finer box and the leader
  model (:49–51) name neither alternatives nor a decision; the seas (:51–53) list four needs with no question,
  comparison or result.
- "Upstream and the record" (:55–61) holds reports and record repairs, which are outside the definition of a
  study, inside the ordered list.

The ordering claim at :3–4 ("how much of it each step would remove") has a stated basis for the first three
steps only.

**Repair.** Give each short step its missing clause, with thresholds the author sets from the record: for the
independent GCM, which agreement pattern near the ground would clear PlaSim's boundary layer and which would make
it the next repair; for RRTMG, what share of the 4.5 W m⁻² excess in the lowest 1.8 km must vanish with extended
tables for the extrapolation to count as the cause, and how far the near-ground range would then narrow; for the
microphysics, the change in surface rain that would matter to the design (the scenario's rain-fed lakes,
regime.tex:7, are one use); for the charging law, which ground-strike polarity and charge per strike each law
gives and what the design uses them for; for each need of the seas, what it decides. Move "Upstream and the
record" out of the ordered list into a closing paragraph on record work, and either state the order's basis (the
size of the sensitivity, where one is known) or drop the ordering claim for steps four to six.

## MAJOR

### M1. The dimming holds a design temperature that the text first states in Results

**Location.** regime.tex:9–11; results.tex:19–20, 99–100; next.tex:12–13, 19–20; verification.tex:86.

**Problem.** The sunlight scale 0.970 holds the GCM's global-mean surface at 295 K (claims S07 and G04; Terluna
`research/decisions.md`:370–372). regime.tex:9–11 gives 1,198 W m⁻² as a scenario value, and the target first
appears at results.tex:19 ("Held at the design temperature by dimming"). Every sensitivity, and every "the
design's dimming with it" in Next work, depends on this premise: the global mean is a target set by tuning.

**Repair.** At regime.tex:9–11: "dimmed evenly ... to 1,198 W m⁻², a scale (0.970) chosen so that the GCM's
global-mean surface settles at the design temperature of 295 K; a change in the physics therefore appears as a
change in the dimming it needs". Shorten results.tex:99–100 to a reference back.

### M2. The model configurations are missing, among them a GCM vertical grid set for Earth

**Location.** The text gives no resolution, level count, grid spacing, domain size or run length; regime.tex:38
(the 6 km grid, called nominal in the caption); hidden_earth.tex:187 ("Earth's top levels", unexplained);
results.tex:49–52.

**Problem.** Specialists read every result through the configuration: ExoPlaSim at T21 (the 2,048 cells of
regime.tex:7) with ten σ levels, half-hour steps and a 50 m slab ocean (`models/exoplasim/README.md`); CM1 on
6.0 km columns with 111 levels to 150 km, 100 m apart near the ground and 2 km apart above 27 km for the
equatorial ring (Terluna `climate/crm/README.md`:120–121), the ring lengths, the electrified box's 148,000 km²
and runs of two lunar days; SWAN's grids and 60 days of forcing; SWASH's grids. Two of these choices hold Earth
and bear on results. The GCM's top three σ layers sit at Earth's pressures (above 107 km, 81–107 km and 63–81 km
on the Moon, with a 55-fold change in ice saturation across 81–107 km), and two layers span the lowest 6.5 km,
which leaves the boundary layer's day–night shape unresolved (`notes/exoplasim.md`:262–264). results.tex:49–52
attributes "a degree or two" of the CM1–GCM gap to how the GCM carries the ground's heat upward, without that
premise.

**Repair.** A compact configuration table (model; grid; levels and top; time step; run length; forcing source;
schemes selected), in the regime section or an appendix. Add the GCM's vertical grid to the inventory of Earth
values (Table 2 and one sentence of text), and cite its two lowest layers where the gap is attributed.

### M3. Which GCM state forced which result is unrecoverable, and two conditions on the CM1 results are missing

**Location.** "The first design run" names two runs (hidden_earth.tex:69–70, the uncalibrated run;
results.tex:10, run A) and "the first run" a third (hidden_earth.tex:134). "Corrected" names four states:
results.tex:20 (the design case), :57 and :96 (the run with the Sun and tilt corrected), next.tex:16 (the
longwave-corrected run), repairs.tex:177 ("corrected rings") and verification.tex:44. Also results.tex:12–13,
25–31, 46–49, 52, 56, 73 and abstract.tex:18–19.

**Problem.**

- At least nine GCM states underlie the results (`paper/data/repairs.json` lists twelve runs), and the text
  names them with overlapping words.
- results.tex:12–13 attaches the effect of the Sun clock, the tilt and the split (+0.6 K; rain 2.91 to 2.24 mm a
  day) to "it", the first design run with 25% seas. Its baseline is `A28_dim5`, with 28% seas and 5% dimming
  (`repairs.json`; Figure 4's caption, results.tex:27–28, gives it correctly).
- "Forced from the GCM before its corrections" (results.tex:52, 56, 73) means `A28_dim5`, which carried the
  Sun-clock skip and Earth's tilt and brought 12% too little sunlight to 0° E (Terluna
  `climate/crm/README.md`:947–955, 1849–1851). The main electrified run and the rain box both sit at 0° E, and the
  text leaves out that their forcing carried the two defects the paper reports.
- The 45° N rings behind the abstract's 3.7 K carry the starting-sounding ice: every column holds 1.1 g m⁻² of
  ice above 107 km through both lunar days (Terluna `climate/crm/README.md`:1197–1206). hidden_earth.tex:145–148
  records the defect and that it remains "in the runs made before they were found"; the results omit it, and its
  effect on the near-ground gap is unquantified.

**Repair.** A short table of GCM states (the name the text uses; what the state includes; the years averaged;
which CM1 and SWAN cases it forced), with one name per state throughout. Correct the baseline at
results.tex:12–13. At each CM1 result, state the forcing's content ("forced from the run that still carried the
Sun-clock skip and Earth's tilt, 12% short of sunlight at 0° E"). At the 3.7 K (results.tex:46–49, 101–103;
abstract.tex:18–19), add the starting-sounding ice, with its effect bounded or marked unquantified.

### M4. Table 1 and the regime text set model outputs among the scenario's ratios

This is a G5 matter of evidence state.

**Location.** regime.tex:15–41 (Table 1), 44–46.

**Problem.** Table 1 sets out "the ratios that separate" the Moon from Earth. Its rows "Height of the 0 °C level,
25 km" and "Tops of deep storm cloud, 55–80 km" are CM1 outputs (claim G09, conditional model), and the 170 and
348 kg m⁻² of vapour at regime.tex:45 are GCM outputs (S08). Outputs of the models that the next sections repair
enter, unmarked, as premises of the regime that motivates the repairs.

**Repair.** Mark each row's evidence state (scenario input, calculation, model result), or move the two CM1 rows
to the storms paragraph of Results and put a calculated estimate in Table 1; at regime.tex:44–46 write "the design
case's GCM holds ...".

### M5. Results place the cloud settings "farther than any repair", while a calibration moved the Moon by more than 20 K and goes unreported there

**Location.** results.tex:8–20, 35–38; hidden_earth.tex:67–70; Figure 4 (results.tex:22–33).

**Problem.** By the paper's own taxonomy a calibration is a repair. The uncalibrated run of the first design
configuration (25% seas, undimmed shield) passed 310 K and was still warming at 315.5 K in year 12
(hidden_earth.tex:67–70; claim H15); after the first calibration, run A of the same configuration stands at
295.5 K (Figure 4's baseline; `paper/data/repairs.json`). "What each repair moved" lists the general repairs,
folds one calibration into the Sun-clock bar, and treats the longwave correction (11.5 K), also a calibration,
as a test. The comparison the section draws, that the climate moves most where the models stay Earth's, holds in
direction and understates the paper's own evidence: the largest movements belong to the calibrations and the
Earth-tuned cloud, the parts another world must remake.

**Repair.** Add the first calibration's effect to the text with its condition (the uncalibrated run had yet to
settle), restrict "farther than any repair" to the general repairs, and carry the relation into the conclusions
(M6).

### M6. The arc: the opening omits what the abstract and the conclusions deliver, and the conclusions follow the section order

This is the charter's tenth pass and its rule for conclusions.

**Location.** introduction.tex:7–9, 36–44, 57–62; abstract.tex:16–21; conclusions.tex:3–26.

**Problem.**

- The introduction promises two answers: what must change before an answer "can be trusted", and how far the
  changed model reaches (:7–9). The abstract and the conclusions land on a third, the located uncertainty, which
  the opening never promises, and they answer "trusted" for the code alone ("show the code doing what it
  states", conclusions.tex:17–18).
- The abstract and the conclusions leave out what the repairs moved beyond the uncertainty ranking. The Sun-clock
  and tilt repairs changed the global mean by 0.6 K yet cut rain from 2.91 to 2.24 mm a day and raised the land
  under 0.5 mm a day from 9 to 42% (results.tex:12–15). The storms, the lightning and the seas
  (results.tex:70–97), the output of three of the title's five models, appear in neither.
- The conclusions run exposure, then repairs and checks, then uncertainty and next work: the section order. Their
  first paragraph restates the introduction's thesis (introduction.tex:52–55) with the same examples. The new
  relation the developed lines support stays implicit: the parts another world must remake (the calibrations,
  the Earth-tuned cloud) are the parts that moved the lunar climate most (M5), while the general repairs, small in
  the global mean, moved where sunlight and rain fall; so the work that would narrow the Moon's uncertainty
  (radiation built from the reference's spectroscopy, cloud constrained by cloud-resolving runs) is the same work
  that would extend the models to other Earth-like worlds. conclusions.tex:25–26 names "a longwave fit at the
  settled state" as the step that loosens the tie to one case, though a refit ties the correction to another
  state; the correlated-k scheme of next.tex:10–11 is the step that loosens it.

**Repair.** With B1's framing, write the promise into the opening (the class of worlds; what the worked case
revealed; what the repaired models then show on the Moon; which worlds they reach). Land the conclusions on the
relation above. Add one sentence each to the abstract and the conclusions on what the repairs moved and on the
storms and seas.

### M7. Between Results, Reach and Next work the inheritance breaks twice, and no step tests the reach

This concerns G1 and G3 at the level of sections, and part (4) of the brief.

**Location.** reach.tex:3 (opens on the classes, taken from Repairs); next.tex:3 (opens on the uncertainty, taken
from Results); abstract.tex:19–20; reach.tex:51–53; the whole of next.tex.

**Problem.** Reach takes nothing from Results, and Next work takes nothing from Reach. Part (4) asks where to go
next to improve the ensemble; every next step concerns the lunar case, while the abstract and the conclusions
claim a reach that no run has tested (reach.tex:52, "though none has been run").

**Repair.** Under B1's framing the target worlds frame the paper. Consider moving Figure 6 into the introduction
as the map of those worlds, with the Moon as the worked point, and returning to it in Reach. Open Reach from the
results (the parts that moved the Moon most are the parts another world must remake). Add a next step that tests
the reach: released against repaired ExoPlaSim on the Earth-air slow rotators already on Figure 6 (16- and 64-day
solar days), which discriminates whether the general repairs carry without refitting; the result that would
change the classification is a general repair that needs retuning off the Moon, which then moves to the
calibrations.

### M8. Reach under-develops the worlds the paper now serves

This is part (4) of the brief, with one G5 bound.

**Location.** reach.tex:44–74; Table 5 (reach.tex:76–98); repairs.tex:128–130; hidden_earth.tex:39, 106–110;
abstract.tex:19–21.

**Problem.**

- Every found world on Figure 6 except Earth stands beyond reach (reach.tex:66–69); within reach as adapted are
  the Moon under other dimmings and Earth-air slow rotators, the latter untested. The text leaves this for the
  reader to assemble.
- Synchronous rotators, the commonest use of ExoPlaSim, go unmentioned. The Sun-clock defect is scoped to
  non-synchronous runs, but the convective-cover bias applies "on any world" whose day differs from an Earth day
  (hidden_earth.tex:39); whether ExoPlaSim's synchronous mode takes its model day from the orbit is for the code to
  settle and the text to state.
- The orbit default puts Earth's orbit into any ExoPlaSim run that sets an obliquity or eccentricity without
  `fixedorbit` (`notes/exoplasim.md`:64–65); the text gives its effect for the Moon only
  (hidden_earth.tex:106–110) and in Table 5. With the Sun clock and the convective-cover unit, these are the
  field-level stakes of parts (1) and (4).
- Per-model reach stays outside the world groups. Table 5 gives CM1 any gravity on its Morrison and NSSL paths,
  and SWAN and SWASH any gravity by similarity, which reaches storms in Earth-like air and water seas at any
  gravity, wider than the ExoPlaSim-centred groups suggest.
- The infrared-from-space capability exists for "a host planet's glow for a moon" (repairs.tex:128–130), and no
  reach group mentions moons of giant planets.
- "The Open Moon under other dimmings runs in all four models with the repairs as they stand" (reach.tex:47–48)
  carries no bound, though the calibrations hold near their fitted columns and the longwave correction's accuracy
  at 307 K is unchecked (verification.tex:86–87).

**Repair.** Rebuild Reach around the class of worlds AGENTS.md names, per model and per property: state the split
between found and constructed worlds, address synchronous rotators and moons, give the consequences of the Sun
clock, the orbit default and the convective-cover unit for other users' runs, and bound reach.tex:47–48 to
dimmings that keep the columns near the fitted ones (the sunlight split holds to 0.7 points at 303 K,
verification.tex:45–47).

### M9. The repairs prose leaves out how the released-code defects were repaired

This is part (3) of the brief.

**Location.** repairs.tex:19–22; Table 3 (repairs.tex:159–161, 202).

**Problem.** The headline defect, the Sun clock, is repaired by a mode that turns the Sun at the synodic rate
continuously from step 0 (patch 04, `NSUNCLOCK` 2), with limits the record names: a steady non-synchronous
rotation, and a phase counted from step 0 (`notes/exoplasim.md`). The text gives it as "2: synodic, continuous" in
Table 3 and as a "setting" at repairs.tex:22. The fixed orbit (an existing switch whose docstring describes only
the freezing of Milankovitch variations) and SWAN's avoidance (breaking always on, `INIT ZERO`) appear only in the
tables. The repairs section is organised by general repairs and calibrations and holds no place for repairs of
defects.

**Repair.** A short paragraph in Repairs on the defects removed or avoided: the synodic clock and its limits, the
fixed orbit with the upstream documentation point, the year of whole model days, SWAN's breaking on with
`INIT ZERO`, and the two defects left open (the thread race, the cold lowest level).

### M10. Internal names a reader outside the project has no way to follow

This is G2.

| Location | Term or object | Proposed |
|---|---|---|
| abstract.tex:2; introduction.tex:3; regime.tex:3; reach.tex:57 | Terluna, unexplained | Name once as the project that designed the case, with its citation; elsewhere provenance only (B1) |
| regime.tex:16, 24; reach.tex:39–40, 47 | "Open Moon" | "the breathable Moon" or "the lunar design case" |
| hidden_earth.tex:123, 126 | Runs `A28_dim5`, `A28_dim5_sun_test` | Describe the runs; keep their names in the data extracts |
| results.tex:26–29, 38; verification.tex:44 | "run A", "the corrected run of 2026-09-29", "the curved-air run", "the corrected run" | Names from M3's table of states |
| hidden_earth.tex:140 | "The sky model's 114 production channels" | Defined nowhere: gloss (the spherical sky solver's production spectral grid) or give the effect alone |
| hidden_earth.tex:142 | "the curved-air ledger" | Used before its definition at repairs.tex:54–55: gloss at first use, or move the paragraph (M11) |
| hidden_earth.tex:132; repairs.tex:25; availability.tex:7 | "The GCM runner", "Terluna's runners" | Gloss once: the scripts that configure, compile and run each model |
| hidden_earth.tex:146–147; verification.tex:87–88; next.tex:59–60 | "the 45° N twilight pair" | Defined nowhere, its result never given: define it (CM1's 45° N rings with and without the curved-air terms) and report it (an effect of 0.013–0.021 K, below what the pair resolves; `notes/cm1.md`:15–21), or cut all three mentions |
| verification.tex:89–90 | "the separate copy that carries the last four" | "the separate ExoPlaSim installation that carries patches 07–10" |
| verification.tex:107, 131 | "patches 07–09"; `solang` | Name the patches; "PlaSim's solar-position routine" |
| verification.tex:51; results.tex:52 | "the equatorial crossing" | Define it (in the record, the 0° E site on the equator) |
| repairs.tex:177 | "corrected rings" | Define them (the 45° rings forced from the design case) |
| introduction.tex:27–28 | "rings and boxes" | Gloss at first use (rings of columns along latitude circles or tilted great circles; doubly periodic boxes); the text defines them only at hidden_earth.tex:151 and repairs.tex:132 |
| reach.tex:14, 38–39 | "found and crafted worlds" | Gloss once, or use AGENTS.md's "exoplanets and constructed worlds" |
| hidden_earth.tex:187, 216 | "Earth's top levels"; "$g$ in ST6, XNL" | Explain (M2) or cut |
| Table 3 (repairs.tex:159–203) | Switch names, `var1`–`var20`, `initsfc` 9, `INIT ZERO` | Right for a reproducibility table; move the table to an appendix (M11) |

### M11. Duplication and balance

This concerns G2's delete test and the paper's length.

**Location.** introduction.tex:11–21 against regime.tex:43–68 and Table 1; introduction.tex:31–34 against
regime.tex:76–77; repairs.tex:96–103, the Figure 3 caption (repairs.tex:110–112), verification.tex:47–49 and
Table 4 (verification.tex:121–122); verification.tex:13–82 against Table 4; verification.tex:84–93 against
next.tex:55–61; conditionality at introduction.tex:58–60, regime.tex:12–13, results.tex:5–6 and 99–106,
verification.tex:9–11, conclusions.tex:17–19; Table 2's State against Table 3's Class; hidden_earth.tex:131–148
and 150–158.

**Problem.** The introduction's second paragraph gives the ratios that the regime section and Table 1 give again,
and the two sentences on the reference model are near-identical. The calibration residuals (0.13%, 0.97 against
1.71 W m⁻², 1–5 W m⁻²) appear in four places; Verification's prose, about 1,390 words, repeats Table 4 row by
row; the missing checks and the record work appear twice; conditionality is stated six times, the closest the
text comes to a caveat wall. Table 2's State repeats Table 3's Class for every repaired row. Two paragraphs of the
hidden-Earth section concern something other than Earth values in code: the adaptation's own defects
(:131–148, dense with internal objects) and the slice's limits (:150–158).

Balance: about 11,100 words of prose, 2,200 in five tables and 530 in six captions, over 21 pages before the
references. Heavy: the hidden-Earth section (2,190 words and a full-page table), Verification (1,390 words and
Table 4), and the ledger's channel detail (repairs.tex:54–72). Light: Results (1,300 words for five models), the
configurations (M2) and Reach for the paper's stated purpose (M8).

**Repair.** Fold the regime section into the second half of the introduction under B1's framing, keeping Table 1
marked by evidence state (M4), or cut introduction.tex:11–21 to two sentences that point to Table 1; cut
regime.tex:76–77. Keep the calibration residuals in Repairs and Table 4 only, and cut Verification's prose to the
evidence ladder, the results outside the fitted columns, the shortfalls and the missing checks. Keep the
conditionality in the introduction and in the closing ranking of Results. Merge Tables 2 and 3 into one inventory
(part, Earth value, effect on the Moon, form, kind, repair class), and move the switch-level Table 3, with Table 4,
to an appendix as the reproducibility record. Move the adaptation's defects to Verification, as what the checks
caught with their effects, or to the defect log with a two-sentence summary; open "Forcing a slice of the GCM"
with the slice's limits.

## MINOR

1. **Figure 4 against the text.** results.tex:36–38 gives about 2.2, 5.9 and 3.5 K as the runs settle; the bars
   read +1.71, −4.98 and −3.21 K (PDF page 15). Quote both in the text, or mark the settled values on the figure.
2. **One term for the transport.** "Sideways transport" (abstract.tex:19; Figure 5's legend) against "transport
   across the circle" (results.tex:47, 65; hidden_earth.tex:151, 156).
3. **The forms' names.** Three sets: abstract.tex:6–7 ("formulas counted per day", "flat and sunlit-only
   geometry"), introduction.tex:36–38 ("units of time", "geometry"), and the bold heads with Table 2. B3's repair
   settles them.
4. **Cloud water's form.** The prose places it under "Fits and simplifications" (hidden_earth.tex:76–79), Table 2
   under Constant (:179), the form referee disposition 34 set. Move the sentence to the constants paragraph.
5. **The high cloud's temperatures.** "180–204 K in the second layer from the top" (hidden_earth.tex:80–81)
   against "Ice cloud at 165–204 K" (Table 2, :186): name the layer or quantity each range describes.
6. **The 11.5% column.** regime.tex:52–54 assigns it to "the widening shells"; next.tex:25–26 measures it against
   "a flat column of constant gravity". The record's figure is the spherical shells with gravity falling as
   $GM/r^2$, against the ledger column's $p_s/g_s$ (`notes/reference_radiation.md`, section 1.2). State the
   baseline once.
7. **The gravity pair's purpose.** "Meant to test the stretch" of the dry dynamics (regime.tex:62–63), and
   "designed for" the gravity-scaled microphysics (verification.tex:40–41; Table 4, :117; next.tex:41–42). Give
   one purpose.
8. **The count of kinds of check.** "Five kinds of check" (verification.tex:3) against a sixth, the arithmetic
   checks (:68–72; Table 4, :130). Set arithmetic in the ladder beside reproduction and correct the count.
9. **An estimate stated as an attribution.** "PlaSim's longwave over-cooling ... accounts for about 1.5 K"
   (results.tex:49–50) comes from a 6 W m⁻² difference at about 4 W m⁻² per kelvin (Terluna
   `climate/crm/README.md`:1190–1194), and the direct test is missing (verification.tex:84–86). Write "is
   estimated at about 1.5 K".
10. **One box against Earth's global mean.** "The lightning the storms make is rarer and larger than Earth's"
    (results.tex:72) compares one box at 0° E over two lunar days, on the forcing M3 describes, with Earth's
    observed global mean. State it as that box's flash density.
11. **Rain and the slice's direction.** Rain at a place in the CM1 rings changes by a factor of several with the
    slice's direction (`notes/cm1.md`:88–90). The rain comparison (results.tex:55–59) and the ring range at
    next.tex:40 should carry it.
12. **Identity by construction.** "whose defaults reproduce the released code" (abstract.tex:10) against five of
    the ten ExoPlaSim patches without a runtime identity run (verification.tex:87–90): "written to reproduce", or
    give the number tested.
13. **One hedge on reach.** "they carry to other worlds within stated limits" (abstract.tex:12–13) stands
    unhedged beside "should extend" (abstract.tex:19) and "should need ... though none has been run"
    (reach.tex:51–53).
14. **The 11.5 K in the abstract.** "a correction worth about 11.5 K with the ice optics" (abstract.tex:17–18)
    reads as the size of an established correction; results.tex:100–101 calls the 307 K state a sensitivity
    resting on a correction used beyond its fit. For example: "a correction that, with the ice optics, warms the
    design case by about 11.5 K in a run outside its fitted state".
15. **Claims for table numbers.** "Every number in the text carries a claim in the register"
    (availability.tex:21–23): numbers that appear only in tables have none (Table 2's 5 W m⁻², 300 s, 75 m,
    50 MV and 10 kV m⁻¹; Table 3's 1,173.5 W m⁻² and 1.40390 kg m⁻³). Extend the register or restrict the sentence
    to the prose. Add this challenge to the review history (availability.tex:27–32) once acted on.
16. **The fifth defect's next step.** PlaSim's cold lowest level (hidden_earth.tex:116–117) has neither a next
    step nor a report (next.tex:55–58).
17. **The GCM's top.** "the GCM's 130 km top" (hidden_earth.tex:146) against Figure 3's top layer, 112–575 km:
    "the GCM's top level, near 130 km".
18. **"Exact" for approximations.** reach.tex:16, 19 and 36–37 call an isothermal approximation and an Earth fit
    "exact"; use "right" or "consistent in its units", as the conclusions do.
19. **Table-only items.** Table 5's "SWASH's Earth rotation" (reach.tex:95) and Table 2's "Earth's radius,
    rotation" for SWAN (hidden_earth.tex:216) appear in no prose: explain or cut.
20. **SWASH in the title.** The title calls SWASH 12.01 "adapted"; it runs unmodified with lunar gravity as input
    (repairs.tex:140–141). B1's title ("on a breathable Moon") covers it.
21. **Abstract length.** About 315 words; many journals in the field set 250.

## The challenge questions, answered

**The brief's four parts.**

- *(1) The need.* Stated as one project's question (introduction.tex:3–9), with the field's gap at
  introduction.tex:46–55. Under AGENTS.md's framing this part is the weakest (B1); the stakes for other users of
  these codes sit late, at reach.tex:23–29 and in Table 5 (M8).
- *(2) Defects against limitations.* Drawn explicitly (hidden_earth.tex:7–10, 99–117), and the adaptation's own
  defects are reported with them. Weakest at the definition and in the single axis (B3).
- *(3) The solutions.* Clear for the general repairs, the curved air and the calibration sequence
  (repairs.tex:31–114). Weakest where the classes disagree (B2) and where the defect repairs go unstated (M9).
- *(4) What the work gave, the worlds, the next steps.* Results carry the GCM sensitivities, the gap between the
  models, the storms and the seas. Weakest in the missing calibration effect (M5), the thin reach for the target
  worlds (M8), and a next-work list confined to the Moon and partly short of G5 (B5, M7).

**Argument.** From the introduction through Results, each section raises the question the next one takes up; the
chain breaks at Results, Reach and Next work (M7). Out of order: the adaptation's defects use objects defined
later (the ledger) or nowhere (the sky model, the twilight pair; M10, M11), and the design temperature first
appears in Results (M1). Duplicated: M11. Missing steps: the design temperature (M1), the configurations (M2), the
GCM states (M3), the reference's own checks (B4), the calibrations' effect on the climate (M5), the twilight
pair's result (M10), the dependence of ring rain on the slice's direction (minor 11), a test of the reach (M7).

**Consistency.** Disagreements: B2 (the classes, six sub-items), B3 (the defects: definition against examples,
Earth-tied and otherwise), M3 ("first design run", "corrected", the Sun-clock baseline), M5 ("farther than any
repair"), and minor items 1–8 and 12–15. Checked and in agreement across the abstract, the introduction, the
sections, the tables and the conclusions: 1.2 atm; 29.53 days; 7.25 times Earth's column; 52 km against
1,737 km; the 32.5° skip; 11.5 K; 3.7 K; about 6 K for the cloud settings; five released-code defects, three
named in the abstract.

**Audience.** The method passages suit specialists in climate and storm modelling, and no passage fails G2 as
tutorial: the fall-speed scaling (repairs.tex:31–35) and the evidence ladder (verification.tex:3–11) each supply a
premise a specialist lacks. The internal names are listed in M10; the configurations a specialist needs are
missing (M2).

**Evidence status.** No passage calls reproducibility, identity, similarity or calibration validation: the
abstract (:14–16), Verification (:3–11, 38–40) and the conclusions (:17–19) keep them apart from physical
validation. The gaps lie elsewhere: B4; M1; M3; M4; the unbounded reach in M8; minor items 9, 10, 12, 13 and 14.

**The arc.** M6, with B1.

**Length and balance.** M11.

**G4.** The eleven section files contain neither "not" nor "rather than". The negations present ("lacks",
"none", "yet to", "without") state absences the propositions require, and no stock signposts appear. The
patterns that remain excluded are the empty actions and the coined "hidden Earth" (B1) and the repeated
conditionality (M11).

## Verdict

With B1–B5 repaired, the manuscript would meet the brief's four parts in substance, though part (4) also needs
M5, M7 and M8 before its account of the worlds within reach and of the next steps holds. At the level of the
whole manuscript:

- **G1.** The argument holds section to section through Results; the break at Results, Reach and Next work (M7)
  and the mixed contents of the hidden-Earth section (M11) keep it short of PASS.
- **G2.** Short of PASS until M2, M10 and M11 are done.
- **G3.** Short of PASS until B1's empty actions are rewritten and M7's boundaries repaired; the audible cadence
  review stays pending.
- **G4.** The excluded phrases are absent. With B1 (empty actions, coined terms) and M11's repeated
  conditionality done, the text is ready for the fresh-reader round.
- **G5.** B4 and B5 are necessary, and M1, M3, M4 and M8's bound are also needed before PASS.

On the sources hashed above, G1–G5 stand at BLOCKED for the release register. After the blocking and major
repairs, the next steps are the fresh-reader round AGENTS.md requires, the author's audible review, and G7 on the
final PDF.
