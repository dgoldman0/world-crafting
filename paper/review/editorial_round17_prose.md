# Editorial round 17: the whole paper, for prose and the author's direction

- **Snapshot.** Commit `1278887`. The working tree matched it (`git diff HEAD` empty). Files read: `paper/main.tex`
  and the twelve files in `paper/sections/`, in the order `main.tex` inputs them, captions and tables included.
- **Reviewer.** A fresh Claude Opus 5.5 subagent, reading for prose and for the author's direction. I edited no
  paper file; this record is the only file I wrote.
- **Date.** 18 October 2026.
- **Read before the paper.** `AGENTS.md` in full; `paper/review/README.md`; `editorial_round16_light.md`; for
  context, `editorial_round15_dispositions.md`, `editorial_round14_whole_prose.md` and
  `abstract_and_repository_2026-10-18.md`; the four Terluna sources behind the writing rules
  (`STYLE_NOTES.md`, `Jewish_Papers_Updated_Style_Notes.md`, `Agent_Working_State_Editorial_Gates.md`,
  `Open_Moon_Editorial_Charter_control-01.md`). I then read the round-16 changes as a word diff, `8826e6a..1278887`.
- **Cadence.** Read silently. No read-aloud review was made.

## Overall judgment

The paper carries out the author's direction. It reads as a field paper on modelling Gaean worlds, its purpose the
ensemble from global climate to storms and seas, with the Open Moon as the worked case and Terluna as provenance.
The title is the author's; the abstract keeps the accepted opening and the approved rewrite, and leaves the
repository to Availability, which names it with the author's condition. The Conclusion, which the author accepted,
discusses what the code makes possible along one line of argument and ends in the vision the author asked for. The
prose contains no "not" or "rather than", marks its transitions, and develops most paragraphs as a mechanism, a
sequence or a comparison. Most of the round-16 additions sit naturally where they were placed. I found nothing
blocking. Three findings are MAJOR. In Results, the spreads measured among exoplanet models, added in round 16, now
stand inside the paragraph of lunar sensitivities and strand the longwave test after a review of other worlds'
cloud. The Introduction, which the author directed to synthesize the whole, ends on the lunar evidence state and
leaves out the path that the abstract promises and the Conclusion develops: the fits replaced by a reduced
radiation scheme and by cloud calibrated against resolved runs, then tests on worlds that other studies model.
And a few evidence limits are told two or three times across the body, the pattern the author judged defensive in
the earlier statement of where the codes had run. The 40 MINOR findings are local: figurative or empty verbs,
terms used before they are introduced, garden-path clauses, repeated sentence frames, and four labels that blur
technical meaning.

**Counts:** 0 BLOCKING, 3 MAJOR, 40 MINOR; 43 findings in all.

## Findings

### Across sections

**F1 · MAJOR · `worlds.tex`:96–98, `verification.tex`:13–15, 55–56, 121–124, `reach.tex`:33–35**

*What fails.* The author judged the statement of where the repaired codes had run, repeated through the paper, to
be defensive from the start, and directed that an evidence limit inform once, where it informs. Three limits are
still told in that repeated way.

| Limit | Told at | Where its evidence is reported |
|---|---|---|
| The gravity-similarity pair failed to convect | `worlds.tex`:96–98; `verification.tex`:55–56; `reach.tex`:34–35; Table 7 | Verification, with `\claim{V06}` |
| Threaded box runs compare as realisations | `assumptions.tex`:126–130; `repairs.tex`:53–54; `verification.tex`:37–38 and again 122–124; `results.tex`:121–123, 184 | Assumptions (the defect) and each Results comparison it qualifies |
| The third step's standards: a clear-sky reference, fits near their state, Earth benchmarks | `verification.tex`:13–15, then `verification.tex`:66–67 and the Benchmarks paragraph | Verification's subsections |

The failed pair is narrated three times in nearly the same words, once for the grid, once for the check and once
for the reach. Verification states the threaded runs' standing twice, at 37–38 and 122–124. Its overview lists the
third step's limits, phrased as what each check "leaves ... untested", and its subsections then state each again.
Each statement is accurate; read together, they lend the body the defensive cast the author rejected, and under
the redundancy pass of the style sources they would be cut. `reach.tex`:45–49 also repeats `verification.tex`:61–66 almost
word for word, though there the limit bounds the reach claim, the place the author chose for such statements; a
clause pointing to the check would serve.

*Fix.* Tell each failure once, where its check is reported, and elsewhere state only its consequence for the claim
at hand. Sample rewrites:

`worlds.tex`:96–98:

> How far lunar convection departs from Earth's, stretched sixfold, however, remains unmeasured, so the 6~km grid
> is justified by the dry similarity alone.\claim{S12}

`verification.tex`:13–15, stated as what each standard covers:

> Each check of the third step measures the code against a standard with a range of its own: a clear-sky reference
> built on HITRAN lines and the MT\_CKD continuum, a fit near its fitted state, and benchmarks run in Earth's air.

`verification.tex`:121–124:

> The third shortfall is CM1's: rebuilt at a higher optimisation, CM1 departs from its first build by
> 0.28--0.32~\textdegree C rms in the air at 2~m within a model day, inside the spread of last-bit nudges, so runs
> from different builds compare as realisations, as the threaded box runs do.

`reach.tex`:33–35:

> its drop limits and breakup, however, remain Earth's, with their effect at other gravities unmeasured.

`verification.tex`:55–56 keeps the full account and `\claim{V06}`.

### Abstract

No findings. See "What I checked and found sound".

### Introduction

**F2 · MAJOR · `introduction.tex`:105–107, with `abstract.tex`:23–26 and `conclusions.tex`:34–52**

*What fails.* The author directed that the Introduction synthesize the whole, after the body, and the rules require
the abstract, the opening pages and the Conclusion to promise, develop and land on the same contribution. The
abstract promises a path: a radiation scheme reduced with existing tools and cloud calibrated against
cloud-resolving runs "would replace those fits", after which the ensemble follows a world's consequences into its
basins and shores. The Conclusion develops that path in its paragraphs on the reduced radiation scheme and the cloud exchange
(lines 34–52), and Next steps lays out its order:
consistent heating and cloud first, then tests of the general repairs on worlds that other studies model. The
Introduction ends one step short of it, on the evidence state of the lunar numbers, and took in none of round 16's
fourth step, the existing tools. A reader of the opening pages learns which fits moved the climate furthest and
nothing of what the ensemble does about them.

*Fix.* Keep the conditional-result clause, which round 15 joined to the fits' weight on purpose, and add one
sentence that names the next step and its test.

*Sample rewrite* (lines 105–107; the passage has no claim markers or citations of its own):

> Of the four forms, moreover, the fits moved the test world's climate furthest, by amounts of the order of the
> spreads measured among exoplanet GCMs, and every lunar climate number is therefore a conditional model result,
> holding given the scenario and the Earth values that remain. Replacing those fits comes first in the ensemble's
> further development: a radiation scheme reduced with existing tools from the reference model's spectroscopy
> \autocite{hogan2022tool,hogan2020evaluating}, and cloud calibrated against cloud-resolving runs of each world,
> would take their place, after which runs on planets that other studies model, among them the slowly rotating
> planets of \textcite{way2018climates} and the cases of the SAMOSA intercomparison \autocite{haqqmisra2022samosa},
> would test how far the general repairs hold.

**F3 · MINOR · `introduction.tex`:20–25**

*What fails.* The new sentence joins three precedents with "and", "while" and a semicolon. "While a GCM's winds
drive a wave model" switches to the present among past-tense acts and uses "while" as a plain "and"; the closing
"so that the global and resolved calculations share their physics" belongs to the LMD clause alone, yet lands the
whole sentence.

*Fix.* Two sentences:

> On Titan, \textcite{rafkin2022interaction} started a cloud-resolving model from a GCM's unstable profiles,
> \textcite{battalio2022interaction} tuned the GCM's convection scheme with its runs and observations, and a GCM's
> winds have driven a wave model over the polar lakes \autocite{detelich2026modeling}. The LMD has gone further:
> its GCM physics runs on WRF's core, in a mesoscale model on Mars and a convection-resolving model over
> Proxima~b, so that the global and resolved calculations share their physics
> \autocite{spiga2009new,lefevre2021convection}.

**F4 · MINOR · `introduction.tex`:27–31**

*What fails.* Three figurative phrases in one paragraph. "Constructed worlds reach further from Earth" gives
worlds the verb "reach", which the rules list among empty actions, where the abstract's accepted wording has
"depart ... further". "Only for a geological moment" is a figure where the source gives a duration (about 70 million
years, by Needham and Kring's estimate, as `paper/notes/literature.md`:380 records). "The known exoplanets crowd
against the same divide extended" is figurative, and the trailing "extended" parses with difficulty.

*Fix.* "Constructed worlds can depart further from Earth, for ..."; "for about 70 million years" (the number would
need its register entry); "Beyond the Solar System, the known exoplanets cluster near the same divide, extended to
them \autocite{zahnle2017cosmic}."

**F5 · MINOR · `introduction.tex`:40–41**

*What fails.* "Modelling such worlds means adapting codes like those named above, and the developers who ported
Earth models to other planets found values fixed for Earth in the code." The "and" coordinates a definition with
the evidence for it; the second clause tells what adapting such codes meets.

*Fix.* "Modelling such worlds means adapting codes like those named above, in which the developers who ported
Earth models to other planets found values fixed for Earth."

**F6 · MINOR · `introduction.tex`:56–57**

*What fails.* "Four GCMs ... all keep it temperate" gives the models a figurative act on the planet.

*Fix.* "four GCMs given the same moist cases of TRAPPIST-1e all simulate a temperate climate, yet differ ..."

### Worlds beyond Earth's range and the test world

**F7 · MINOR · `worlds.tex`:3–9**

*What fails.* "Set" occurs seven times in five lines ("set where", "Two set", "sets the absorber paths", "sets
how far", "Two set", "sets the height", "sets whatever"). The repeated frame makes the opening read as a list of
equal assignments, and it hides the different relations: a column fixes path length, the scale height over the
radius measures the departure from a flat column, and the day counts a formula's input.

*Fix.* Keep "set" where it fits and name the relation elsewhere, for instance "Four ratios between a world and Earth
determine where ...", "the scale height over the radius measures how far ...", "and the solar day fixes whatever a
formula counts per day".

**F8 · MINOR · `worlds.tex`:105–106**

*What fails.* "ExoPlaSim's default orbit puts Earth's tilt of 23.7\textdegree" stands in the same section as
Table 1, which gives Earth's tilt as 23.44\textdegree. The 23.7\textdegree\ is Earth's tilt for 1 AD from Berger's series (`H24`),
which the reader learns only at `assumptions.tex`:118–120.

*Fix.* "where ExoPlaSim's default orbit puts Earth's tilt of 1~AD, 23.7\textdegree."

### Earth values and defects in the released codes

**F9 · MINOR · `assumptions.tex`:23–27**

*What fails.* "the lower of the two knees" has one knee in view, the code's 1 Hz. The second, the
$g/g_\mathrm{E}$ Hz that similarity would give, appears only in the closing apposition.

*Fix.* "... wherever its frequency band reaches past the lower of two knees, the code's 1~Hz and the
$g/g_\mathrm{E}$~Hz that similarity would give it: $g/g_\mathrm{E}$~Hz under weaker gravity and 1~Hz under
stronger."

**F10 · MINOR · `assumptions.tex`:31–35**

*What fails.* The colon after "The air's density enters the storms as well" opens a sentence that ends on the
ground-strike rule, a temperature level unrelated to density. The fact rides on a frame that excludes it.

*Fix.* End the sentence at "... lowers the field by 44\% at the ground." and give the rule its own sentence: "Its
rule for ground strikes is set at Earth's scale too: the code declares a ground strike when a channel reaches air
warmer than $-7$\,\textdegree C, about 5~km above Earth's ground but 27--34~km above the Moon's.\claim{H03}"

**F11 · MINOR · `assumptions.tex`:50–51**

*What fails.* "a 0.7~W\,m$^{-2}$ gain from the curved light and escape" uses a term that Repairs glosses only at
`repairs.tex`:102 ("the twilight and the low Sun's side light").

*Fix.* "a 0.7~W\,m$^{-2}$ gain from the twilight and the low Sun's side light".

**F12 · MINOR · `assumptions.tex`:64**

*What fails.* "The radiation schemes were fitted to Earth's columns and Earth's Sun, and the test world's columns
lie far outside both." Columns can lie outside Earth's columns; they can lie outside Earth's Sun only loosely.

*Fix.* "... and the test world's columns and filtered sunlight lie far from both."

**F13 · MINOR · `assumptions.tex`:64–85**

*What fails.* The paragraph announces its frame, PlaSim's fits erring "first in the column's totals, then in its
split of sunlight, then in the heights", and then runs past it into cloud phase, the humidity threshold and CM1's
RRTMG tables and ice optics. It runs to about 22 source lines, and the turn to a second code arrives
mid-paragraph.

*Fix.* Start a paragraph at line 82 with a sentence that inherits the columns: "CM1's RRTMG meets the same columns
at the edges of its tables: its reference pressures begin at 1,053.63~hPa, and ..."

**F14 · MINOR · `assumptions.tex`:87**

*What fails.* "Below the clouds" opens a paragraph whose laws include charging inside the clouds and fall speeds
within them, so the spatial frame misplaces part of its content.

*Fix.* "Beyond radiation and cloud, the laws of particles, seas and charge were fitted to Earth's data."

**F15 · MINOR · `assumptions.tex`:31, 41, 59, 76, 94**

*What fails.* Five sentences in this section share one frame, "[X] is Earth's / errs / enters ... as well:"
followed by particulars ("enters the storms as well:", "keeps Earth's day as well:", "is Earth's as well:", "errs by
height as well:", "are Earth's calibrations as well:"). Each transition works alone; together they mark the section
as an inventory, the effect the style sources name for mechanically parallel frames.

*Fix.* Vary at least three: "CM1 keeps Earth's day in its Sun and its soil: ..."; "PlaSim's vertical grid was laid
out for Earth's air: its ten $\sigma$ levels ..."; "The wave and storm laws come from Earth's calibrations: Wu's
drag ...".

**F16 · MINOR · `assumptions.tex`:112–122**

*What fails.* The convective-cover sentence runs to about 90 words through "which ..., a conversion ..., so ...,
and adds ..., up to ..., and on any world ...". In the next sentence, "149~W\,m$^{-2}$ of sunlight on 86\textdegree\
of latitude" reads for a moment as a band 86\textdegree\ wide.

*Fix.* Break after the developers' clause: "... in its unit conversions \autocite{paradise2022exoplasim}. With a
model day of 29.8 Earth days, the formula therefore reads lunar rain as about 30 times heavier than it is and adds
$0.125\ln 29.8 = 0.42$ to the cover, up to its cap of 0.8; on any world it adds
$0.125\ln(\text{day}/1\,\text{d})$.\claim{H07}" Then "at 86\textdegree\ latitude".

### Repairs

**F17 · MINOR · `repairs.tex`:96–99**

*What fails.* "the 282 thin enough to scatter by spherical successive orders of scattering" parses with difficulty:
"thin enough to scatter" reads as the channels' own act, and the verb ("were traced") is elided across a long
clause.

*Fix.* "... the 282 weakly absorbing channels by spherical successive orders of scattering from an in-house sky
solver, and the rest by a direct beam ..." (the appendix gives the criterion, an absorption depth under 3).

**F18 · MINOR · `repairs.tex`:173**

*What fails.* "The bound sits between them" gives an abstraction the verb "sits", which the rules list among empty
actions. Round 15 introduced it.

*Fix.* "Between them, the bound counts a downward channel that reaches the $-7$\,\textdegree C level as a strike
only if its potential can carry a leader the rest of the way down, ..."

**F19 · MINOR · `repairs.tex`:196–203**

*What fails.* The section closes on "Since the ensemble's methods impose only the GCM's fields and the slice's
geometry, they are built for a slice of any world's GCM." Two sentences on the seas, the second the round-16 Titan
precedent, now stand between it and the slice forcing it generalizes, and "the ensemble's methods" takes in the wave
coupling, which converts the stress through Wu's drag law and forces no slice.

*Fix.* Name the subject: "Since the methods that force CM1 impose only the GCM's fields and the slice's geometry,
they are built for a slice of any world's GCM." The Titan precedent then reads as the seas' comparison, as
intended.

### Verification

**F20 · MINOR · `verification.tex`:41–45**

*What fails.* The colon's claim is that gravity stays fixed in a laboratory study of a wind sea. The round-16
example, a centrifuge raising gravity twentyfold, counters that claim, and the sentence leaves the reason it still
holds unwritten: the centrifuge waves were forced mechanically, with no wind to raise a sea (as
`paper/notes/related_work_scan_2026-10-18.md`:148–150 records). The two examples are joined by "and", as if they
made the same point.

*Fix.* "... varied the air's density and the wind \autocite{banfield2015winds}, and although
\textcite{cazaubiel2019wave} raised gravity up to twentyfold in a centrifuge, the waves they studied were forced
mechanically in a container, so a wave model's response to gravity under wind is checked numerically, by a
similarity test."

**F21 · MINOR · `verification.tex`:74–75**

*What fails.* "Against the same reference RRTMG, checked and left uncalibrated, lies within ..." first reads as "the
same reference RRTMG".

*Fix.* "RRTMG, checked against the same reference and left uncalibrated, lies within ..."

### Results on the test world

**F22 · MAJOR · `results.tex`:78–110**

*What fails.* The paragraph develops the lunar sensitivities: the cloud settings, the ranking by form, the
longwave test, and the conclusion on where the climate is least certain. Round 16 inserted four sentences on the
spreads measured among exoplanet models before the existing comparison with Yang et al. 2023, so a review of other
worlds now runs from line 87 to line 103, and the paragraph returns to the test world with "A test of the cooling
by height moves the global mean more than any cloud setting", which compares with cloud settings named twenty
lines earlier. The swap test fails: the longwave sentence can move above the review without loss. The paragraph is
now about 33 lines long. "Intercomparisons have measured" also gives the studies' act to an abstraction.

*Fix.* Keep the lunar line whole and give the field's measured spreads a paragraph of their own, which then hands
on to "The gap between the models".

*Sample rewrite.* First paragraph: lines 78–87 as they stand, through "... by 0.65~K.", followed directly by the
longwave sentence and the uncertainty sentence, unchanged:

> ... and the geometry's curved-air terms, on the table's first channels, by 0.65~K. A test of the cooling by
> height moves the global mean more than any cloud setting: the longwave correction with the ice optics, a
> calibration and a general repair switched on together and the one change that moves the cooling by height, warms
> the design case by 11.5~K over years 10--19, toward a balance near 307~K, a sensitivity reached with a correction
> fitted at 295~K, with the warmer run's water vapour over years 15--19 twice the design case's, 348 against
> 170~kg\,m$^{-2}$, and its cloud covering 38\% of the sky in place of 20\%, most of the gain in high
> cloud.\claim{G05} Given the reference's spectroscopy and these tests, the test world's climate is least certain
> in its cloud amount and in the height at which its longwave cools the air, both set by Earth fits open to
> constraint by cloud-resolving runs, the reference model and an independent GCM.

Second paragraph, opening on the fits it inherits:

> The fits' effects are of the order of the spreads measured in intercomparisons of exoplanet models. The radiation
> codes themselves disagree on moist air: five band codes used in GCMs and two line-by-line codes, on clear-sky
> columns of 250--360~K, differ by up to 60~W\,m$^{-2}$ in the shortwave and, in outgoing longwave, by amounts that
> grow with the surface temperature to 10--20~W\,m$^{-2}$ \autocite{yang2016differences}. Among whole GCMs the
> spread widens as water and cloud enter: [lines 92–96 unchanged, through \autocite{yang2019simulations}].
> Parameterized and resolved cloud have been set side by side on other worlds. [Lines 97–103 unchanged, through
> "... the authors judged the three models' climates broadly similar."]

`\claim{G05}` and `\claim{G16}` stay where they are in lines 78–83, and every citation of the inserted passage stays
with its sentence.

**F23 · MINOR · `results.tex`:37–39**

*What fails.* "the uncalibrated run passed 310~K and was still warming at 315.5~K in model year 12" repeats
`assumptions.tex`:68–69 nearly word for word, so the reader meets the same clause twice.

*Fix.* In Results, keep the comparison and drop the repeated clause: "In the first design runs, with 25\% seas
under the undimmed shield and with PlaSim's Sun clock and Earth's orbit, the same configuration, calibrated,
settled at 295.5~K, at least 20~K below the uncalibrated run, which was still warming at 315.5~K in model year
12.\claim{H15}\claim{G14}"

**F24 · MINOR · `results.tex`:116–120**

*What fails.* "Two further terms are radiative" is followed by a sentence holding two radiative errors, PlaSim's
and RRTMG's, so "A third term, from the ice ..." reads as a third radiative term against the count of two.

*Fix.* "The second radiative term, from the ice that the ring's starting sounding left above 107~km, remains
unquantified."

**F25 · MINOR · `results.tex`:162–163**

*What fails.* "0.022 per square kilometre per year over the box, about a hundredth of Earth's average of 44 flashes
a second" sets a density beside a global rate, so the reader must convert to see the hundredth.

*Fix.* Give Earth's density beside the global rate, "about a hundredth of Earth's average, 44 flashes a second or
about 2.7 per square kilometre per year"; the derived 2.7 would need its register entry or a stated calculation.

**F26 · MINOR · `results.tex`:167–172**

*What fails.* The paragraph ends on two exoplanet estimates that use Earth-fitted flash-rate laws. Its relation to
the lunar run, which separates charge and computes each flash, stays unwritten, so the sentence reads as an
appended fact. Round 15 marked the storms' heights; the contrast in method remains implicit.

*Fix.* Write the contrast into the opening: "Where the lunar runs separate charge and compute each flash, two
exoplanet estimates of lightning use laws fitted to Earth's storms, whose tops stand far below the lunar runs'
55--80~km: ..."

### Reach to other worlds

**F27 · MINOR · `reach.tex`:12–13**

*What fails.* "The three ExoPlaSim defects that the general repairs remove" contradicts Repairs (`repairs.tex`:42–44),
Table 2 ("Avoided") and Table 6 ("Avoidance"): the orbit default is avoided by configuration with `fixedorbit`.

*Fix.* "The three ExoPlaSim defects, two removed by general repairs and one avoided by configuration, remain in the
released code, ..."

**F28 · MINOR · `reach.tex`:12–36**

*What fails.* The first two subsections restate much of Earth values and defects: the Sun clock's 33\textdegree\
skip beyond 20 days, the cover's $0.125\ln(\text{day}/1\,\text{d})$, the cloud water too dry under weaker gravity
and too wet under stronger, and CM1's and SWAN's Earth values, which Table 4 also lists. The new matter (the
synchronous mode's model day, the TRAPPIST-1e and Proxima~b numbers, the Chapman factors for Mars, Venus and Titan,
and what the adapted CM1 and wave models represent) is diluted by it.

*Fix.* Point to the earlier statements in a clause and keep the new matter; for instance, open the second
subsection on the Chapman factors and drop the sentence "The other released codes contain Earth values of their
own: ...", which Table 4's second column carries.

**F29 · MINOR · `reach.tex`:60–61**

*What fails.* "Synchronous planets of M dwarfs ... add a spectrum outside the near-infrared water fit" gives the
planets the act of adding a spectrum.

*Fix.* "... receive a spectrum outside the near-infrared water fit".

**F30 · MINOR · `reach.tex`:78–83**

*What fails.* Under the heading "Worlds that need new physics", the second sentence turns to four restrictions
within the Gaean class, worlds that need no new physics. "Further" marks the addition and leaves the turn of
subject unmarked.

*Fix.* Mark the turn: "Within the Gaean class itself, four restrictions on the current implementation limit its
use: ..."

### Next steps

**F31 · MINOR · `next.tex`:9–11**

*What fails.* "its longwave correction and PlaSim's cloud, the two Earth fits whose tests moved its climate most,
are the first calibrations to revisit" mislabels both: the longwave correction is a lunar calibration of Sasamori's
Earth fit, and PlaSim's cloud has no calibration yet to revisit. "The lunar case supplies the first experiments"
also gives the act to an abstraction.

*Fix.* "The first experiments take up the two Earth fits whose tests moved the test world's climate most: PlaSim's
longwave by height, under its correction, and its cloud, still uncalibrated."

**F32 · MINOR · `next.tex`:21–26**

*What fails.* One sentence carries the humidity predictor, the reduced scheme, "both the correction and Sasamori's
and Lacis and Hansen's fits" (three items after "both", with three "and"s), and the conditions under which the
scheme would hold.

*Fix.* Two sentences: "... would go further, replacing the correction and the fits of Sasamori and of Lacis and
Hansen. Once that spectroscopy is checked, and the reduction checked against it layer by layer, such a scheme would
hold on columns within the gases, pressures and temperatures of the checks, under the starlight its shortwave would
be built for, on another world as on the test world."

**F33 · MINOR · `next.tex`:38–39**

*What fails.* "this way" closes one sentence and the round-16 Titan sentence repeats it.

*Fix.* "On Titan a GCM's convection has been tuned by the same route: ..."

**F34 · MINOR · `next.tex`:47–48**

*What fails.* "the calibration residuals, 0.97~W\,m$^{-2}$ rms by layer or 0.6 points in the split" labels as a
residual the split's error on columns outside its fit (`V07`); its fit residual is 0.3 points rms (`R09`). The label
blurs a fit state with a test beyond it.

*Fix.* "by more than the calibration's residual by layer, 0.97~W\,m$^{-2}$ rms, or the split's 0.6 points rms on
columns outside its fit".

**F35 · MINOR · `next.tex`:58–62**

*What fails.* The round-16 SAMOSA sentence holds a subject of about 40 words before its verb, "would test", and
"Released and repaired ExoPlaSim run on the sixteen cases" first reads as a main clause. It also repeats the
previous sentence's opening and leaves its relation to that test unmarked.

*Fix.* Open on the relation: "A second set of runs would test the convective-cover repair in synchronous rotation,
where the released unit biases the cover by ExoPlaSim's own arithmetic: released and repaired ExoPlaSim on the
sixteen cases of the SAMOSA intercomparison, a planet rotating once in 15 days around a 3000~K blackbody star,
sampled across surface pressure and instellation from a survey made with ExoPlaSim and compared with ExoCAM
\autocite{haqqmisra2022samosa}."

**F36 · MINOR · `next.tex`:75–76**

*What fails.* "before adopting them a first step corrects the GCM's column mass and heights" leaves "adopting"
without an actor and gives a step the act of correcting.

*Fix.* "and before they are adopted, a first step would correct the GCM's column mass and heights, while a test of
the circulation's sensitivity would show whether the full equations are needed."

**F37 · MINOR · `next.tex`:100–114**

*What fails.* (a) Lines 100–104 retell `results.tex`:174–182 at length, with the same qualifiers ("made before the
ventilation repair and with leakage off"). (b) "Under Saunders and Peck's law hail, striking ..." first reads as "law
hail". (c) "would complete what decides the arrangement" is convoluted. (d) "with a rate, and from the rate would
follow the number of strikes the ground receives" restates "rate".

*Fix.* (a) Keep the cause and the new detail, and point to Results for the windows: "The lunar storms' arrangement
of charge turns over with the laboratory charging law chosen, since the laws disagree on the charge rimed ice takes
in the storms' little cloud water: in the two windows that Results describes, the normal arrangement under Saunders and Peck's law
held in most of the second window's outputs and about half of the first's.\claim{G11}" (b) "Under Saunders and
Peck's law, hail, striking ice and snow at 4--8~m\,s$^{-1}$, carried most of the charge, and under Takahashi's,
graupel, striking at about 1--4~m\,s$^{-1}$." (c) "and graupel's sign at its own speeds would complete the
measurements that decide the arrangement the model's lunar storms take." (d) "would replace the bound on ground
strikes, now between none and a fifth of flashes, with a rate of strikes, each lowering a median 149~C."

**F38 · MINOR · `next.tex`:119–120**

*What fails.* "the small seas that fail the band-edge test" names a test the paper never introduces; Verification
mentions only the time-step criterion.

*Fix.* "a wider frequency band for the small seas whose spectra reach its upper edge", or one clause in Verification
introducing the band-edge test.

**F39 · MINOR · `next.tex`:128–129**

*What fails.* One bullet joins locating and reporting CM1's thread race with "a proposal for one gravity parameter
read by every scheme", an unrelated change, so the proposal reads as part of the race report.

*Fix.* Two bullets: "locating CM1's thread race, placed by elimination in CM1's own loops, and reporting it;" and "a
proposal to CM1's developers for one gravity parameter read by every scheme;".

### Conclusion

The author accepted this section. The three findings below are for the author's decision.

**F40 · MINOR · `conclusions.tex`:12–13**

*What fails.* "Such a comparison could follow a change ..." has no comparison before it; the sentence before
describes exploring a range with the GCM and concentrating resolved runs. The comparison also takes the act of
following.

*Fix.* "Run together, the global and resolved calculations could follow a change in a planet's climate down to the
water arriving in a basin and the waves arriving at its coast, through the circulation that determines both."

**F41 · MINOR · `conclusions.tex`:26**

*What fails.* "The ensemble's reference and calibration tools make that distinction useful when specifying another
world" uses a generic verb where the next sentences name the operations.

*Fix.* "With the ensemble's reference and calibration tools, that distinction becomes a procedure for specifying
another world: its radius and atmospheric column determine a new curved-air table, while its spectrum and columns
determine the targets for the radiation fits."

**F42 · MINOR · `conclusions.tex`:76–77**

*What fails.* "Their disagreement identifies collision speeds, ..." gives an abstraction the act of identifying.

*Fix.* "Comparing runs under each law locates the collision speeds, water contents and temperatures at which
further measurements would discriminate between the laws."

### Availability, authorship and review

**F43 · MINOR · `availability.tex`:201–239**

*What fails.* The review history ends at the abstract's rewrite. Round 16, the related-work scan and its four steps
in the body, the Introduction, the Conclusion and the abstract, each read lightly by a fresh agent, goes unrecorded
there, and this round will need its entry too. The charter requires the actual review history in a release. `review/README.md`'s History also
ends at the abstract's rewrite.

*Fix.* Add round 16 and round 17 to both when this round's dispositions are recorded.

## Round 16's additions, one by one

| Addition | Location | Judgment |
|---|---|---|
| Earth-built models joined to GCMs off Earth | `introduction.tex`:20–25 | Sits in the paragraph's line from global to resolved to joined models; F3 |
| Escape calculations named as the design's | `introduction.tex`:35–37 | Sound |
| The THAI spread | `introduction.tex`:56–58 | Sits, with the concession marked by "still"; F6 |
| "the retained Earth values" | `introduction.tex`:60 | Sound |
| The fits set against measured spreads | `introduction.tex`:106 | Sound; F2 proposes a sentence to follow it |
| "made for air a tenth of a percent of the radius tall"; the Mars example removed | `assumptions.tex`:47, 25 | Sound |
| Pseudo-spherical two-stream and its twilight gap | `repairs.tex`:99–100 | Sound |
| Earth's curvature figures as the curved-air landing | `repairs.tex`:117–119 | Sits; "Even on Earth" marks the gradation from Mars and Titan |
| Citations for the emulation, MT\_CKD 4.3 and collision-induced absorption | `repairs.tex`:132–134 | Sound |
| PlanetWaves over Titan's lakes | `repairs.tex`:200–202 | Sits as a comparison; F19 for the sentence after it |
| The centrifuge experiment | `verification.tex`:43–44 | F20 |
| Spreads measured among exoplanet models | `results.tex`:87–96 | F22 |
| Song et al.'s two-dimensional runs | `results.tex`:141–143 | Sits; "likewise" ties it to the models' difference on rain |
| "Two exoplanet estimates", with their laws cited | `results.tex`:167–172 | Scope sound; F26 |
| The LMD's shared physics and Lefèvre et al. | `next.tex`:4–9 | Sits; "Codes built separately, as here" answers it |
| ecCKD and CKDMIP | `next.tex`:27–30 | Sits; the sentence takes up "checked against it" |
| The Titan tuning | `next.tex`:39–41 | Sits as the paragraph's landing; F33 |
| SAMOSA | `next.tex`:58–62 | F35 |
| LMD sentence; free tools; Titan "much as"; THAI and SAMOSA | `conclusions.tex`:18–20, 35–37, 47–49, 66–67 | Each sits inside its paragraph's argument; none reads as recap or data |
| The fits beside the spreads; tools attached to the reduction | `abstract.tex`:19–23 | Sound; the comparison now ends its sentence, and the numbers follow in their own |

## What I checked and found sound

- **The author's framing.** The title is "Modelling Gaean worlds and beyond", with a subtitle. The abstract's text
  through "Constructed worlds can depart from Earth further than natural ones" is identical, line breaks aside, at
  `9d555e6`, `90753d2` and `1278887`, so the accepted opening stands as the author read it. The
  repository appears in Availability alone, with "as a standalone project, if resources allow". Terluna enters as
  the source of the case (`introduction.tex`:33, `conclusions.tex`:5) and of the records and assistance
  (Availability). Gaean is defined at first use in the abstract and again, with "We use", in the Introduction. The
  Conclusion's prospective sentence on worlds beyond the Gaean class stands, and the abstract's last sentence
  matches it.
- **Excluded words.** A search of the section files found no "not", "rather than", "Notably", "It is worth noting"
  or "Turning to". The six uses of "moreover" each open an added point after related matter (`introduction.tex`:59,
  105; `assumptions.tex`:81; `results.tex`:136; `reach.tex`:55; the abstract's, in the accepted opening).
- **Scoped claims.** "Some exoplanet climate studies", "by the account of THOR's developers", "a spread their
  authors relate to the models' parameterization choices", "Two exoplanet estimates", "the authors judged the three
  models' climates broadly similar" each say what the cited works did. "Each team" (`introduction.tex`:49) refers
  to the three teams named.
- **The arc between abstract and Conclusion.** Both promise and land on the ensemble that follows a world's gravity,
  day and starlight into its storms, basins and shores, with the fits as the remaining Earth content and the class
  beyond the Gaean as a prospect. F2 concerns the Introduction alone.
- **The Conclusion against the author's direction.** It opens with a reminder of two sentences, discusses the code's
  consequences along one line (consistency by repair, the tools, the reduced radiation, the cloud exchange, the
  similarity questions, constructed worlds as experiments, laboratory experiments, design and interpretation), and
  ends in concrete images. I found no recap, inventory or data dump in it.
- **Transitions between sections.** Worlds ends on ExoPlaSim's default orbit and the next section opens on it;
  Verification's last sentence assigns its open checks to the next steps; Results ends on the run-up and Reach opens on the Open Moon
  as the first world simulated; Next steps ends on the record and the Conclusion opens on the ensemble's purpose.
- **The lint screen** (`paper/tools/lint.py`): 274 candidates (17 negative contrast, 2 self-reference, 35 possible
  empty action, 12 coined term, 186 universal claim, 22 generic verb). I went through the list against the text,
  which I had read in full, and judged each negative-contrast, self-reference, coined-term and empty-action
  candidate; the universal-claim and generic-verb flags I judged where they fell in passages under close reading.
  Those that became findings are F4, F18, F37 and F38; the rest
  are physical uses ("a channel reaches", "the thermal wave reaches"), negations the claim requires ("failed to
  convect", "no ozone", "no competing interests"), or universals scoped by their own clauses.
- **Sources behind six findings**, checked against `paper/claims.json` and the notes: `R09` and `V07` (F34), `H24`
  (F8), `G11` (F37), Needham and Kring's duration (F4), the centrifuge's mechanical forcing (F20), and the band-edge
  test in `notes/waves.md` (F38).

## Noticed outside this reading's scope

- `next.tex`:105–106 says graupel "carried most of the charge" under Takahashi's law. The register entry `N01`
  gives hail 37--43\% of the non-inductive charging under that law and graupel "most of the rest", which leaves
  graupel's share between about 30 and 63\%. An evidence reviewer should confirm "most".
- I read the LaTeX sources and built no PDF; page layout and float placement remain for the exact-build review.
