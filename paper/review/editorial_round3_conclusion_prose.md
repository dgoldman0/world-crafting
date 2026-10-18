# Editorial round 3: prose reading of "Discussion and conclusions" and five revised passages

## 1. Record

- **Reviewer.** A fresh Claude subagent, Claude Opus 5.5 (model id `claude-opus-5-5[1m]`), launched for this
  reading. It had seen no earlier review of the paper.
- **Date.** 2026-10-17.
- **Snapshot.** Commit `e89a394` (`e89a394dff2ce9ce2a570c016ee6357adfec3ec9`). Every file was read with
  `git show e89a394:<path>`. During the reading the working tree moved on (eleven modified paths, among them
  `reach.tex`, `results.tex`, `assumptions.tex` and `main.tex`); every line number below is the snapshot's.
- **Method.** The ten passes of the charter's section 11, applied to a closing section, and the rules of
  AGENTS.md "Writing", judged against the author's direction of 2026-10-17 for the closing section (remind and
  excite through real discussion; the work's reach kept to the kinds of world it has run).
- **Cadence.** Silent. The conclusion was read continuously twice, then paragraph by paragraph and sentence by
  sentence; each other passage was read in its paragraph. No audible reading was made.

**Files in scope (sha256 at e89a394)**

| File | Scope | sha256 |
|---|---|---|
| paper/sections/conclusions.tex | whole section | 0ceab5bc3331bb70f1e9cd9e863d259ac0c2aa15bb80576592e584686091cfc4 |
| paper/sections/reach.tex | sentence at 41–43; paragraph at 45–58 | 6c455cb802b9a13a11336f9d18e664a31f92f64a29f375ef239934f510f048c2 |
| paper/sections/next.tex | paragraph at 35–42 | 7075a036e4f497191070019df134a055d1c5c0bad25b5cb6217f1426198195a2 |
| paper/sections/abstract.tex | sentences at 4–6 and 15–16 | 299a4e7b1a849c7b9291469ae8152e50567f1dbd83cf7d78625cf064b27da11a |
| paper/sections/results.tex | sentences at 48–52 and 82–86 | 1764084dcd3a7ab1f902f0b161cbbc24f4e23c6987db94b142a3e871b35c12b7 |

The hashes of conclusions.tex and reach.tex match those in the brief.

**Rule files read in full**

| File | sha256 |
|---|---|
| world-crafting AGENTS.md (working tree identical to e89a394) | e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32 |
| terluna ensemble/planning/Open_Moon_Editorial_Charter_control-01.md | aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0 |
| terluna ensemble/planning/source_controls/STYLE_NOTES.md | 659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46 |
| terluna ensemble/planning/source_controls/Jewish_Papers_Updated_Style_Notes.md | 18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab |
| terluna ensemble/planning/source_controls/Agent_Working_State_Editorial_Gates.md | 553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464 |

The charter's hash matches the one AGENTS.md cites (aac4a4f2…0b0).

**Context read at e89a394**

| File | How read | sha256 |
|---|---|---|
| paper/sections/introduction.tex | in full | b8325d641b56d6da32cffbcaa143e26461495322235c2de3b0709402f1ef5b72 |
| paper/sections/worlds.tex | in full | 453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112 |
| paper/sections/assumptions.tex | in full | 01d5eea0744342fba7ef3eea7d274976cc88744f5d97e4a3ca16b2e1751fb50e |
| paper/sections/repairs.tex | in full | bb1d22c01616fdaf454280acded56316b7995af2a8fc3bb5a255af52c92e793c |
| paper/sections/verification.tex | in full | 4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00 |
| paper/main.tex | in full, for the section order | be6759e766899797bd11d33ba9663dbea68a9b6938d741c9a1dd4dea9b70eeca |
| models/exoplasim/README.md | lines 57 and 61, on the orbit default | 7af8415bebd7733da42bb34c1f47bb9f5411408a243523cae5524be4b17c7149 |
| paper/tools/lint.py | header read; run on snapshot copies | 27f9b47a1f4837583b75eb750e302531f3e07a44e452983dd9ddce2b35657367 |

**Also seen.** The commit message of e89a394 appeared in a `git show --stat` listing; in two paragraphs it
summarises what the second round found and what the commit changed. The file names in `paper/review/` were
listed once, to place this record; those files, and everything under `paper/notes/`, stayed unopened. The
session context held the author's memory index, one line per entry; the memory files stayed unopened.

**Screening, reported as screening only.** `paper/tools/lint.py`, run on snapshot copies, finds no "not" and no
"rather than" in any scoped passage. Its other hits in the conclusion were read: the negative contrasts at 5 and
7 are required by meaning; "reach" at 45 names what laboratories attain and "reached" at 62 a physical fall; the
universal words at 10, 11, 14, 15, 35 and 40 hold in context, and those at 37, 70 and 74 are taken up in m6,
m12 and B1. In results.tex it flags "reached" at 48 (R1). A word 5-gram count puts 17.9% of the conclusion's
1,169 5-grams in the nine sections before it, highest in the sentences at 58–59 (64%, from Verification), 46–48
(46%, Results), 71–74 (35%, Next steps), 41–46 (31%, Results and Next steps) and 54–58 (30%, Abstract). The
count measures verbatim repetition alone; paraphrase raises the real overlap (M1).

## 2. Findings

BLOCKING breaks the author's direction or a rule as the author would reject it; MAJOR is a clear breach;
MINOR is polish. Each rewrite was checked against the snapshot's own numbers and conditions, screened for "not"
and "rather than", and counted in words; the length change is given with each.

### B1. BLOCKING. The closing sentence opens the method to any new world

**Location.** conclusions.tex:74–76.

> For any new world, the geometry and the gas absorption can be computed from the world's own column, and cloud
> remains the part to be calibrated for that world, against cloud-resolving runs whose microphysics laboratories
> and similarity runs can test.

**Rule.** The author's direction (a conclusion suggesting the work "already extends to kinds of worlds that we
have not tested at all" is rejected); "Claims stay within their evidence"; "Technical meaning survives editing"
and G5 (a proposed design kept apart from a runnable calculation).

**Why.** The section's landing overreaches three times. "Any new world" drops the bound the section states at
35–36, "on any column whose gases, pressures and temperatures that spectroscopy covers", and contradicts
reach.tex:74–77, where the radiation of Titan, present Mars and Venus "would have to be built". "The gas
absorption can be computed" turns the scheme of 34–37 and next.tex:14–16, a proposal written with "would", into
a present capability; the GCM's gas absorption today comes from PlaSim's broadband fits, calibrated against the
reference on the test world's columns. "The part to be calibrated" makes cloud the one calibration left, while
paragraphs 4 and 5 of this section and the reach table list Earth's laws of charge, sea and drop size, RRTMG's
pressure range and the thin-shell dynamics among the limits. The phrase "whose microphysics laboratories and
similarity runs can test" also parses first as the compound noun "microphysics laboratories".

**Rewrite.**

> For a new world whose gases, pressures and temperatures the line-by-line spectroscopy covers, the geometry of
> its air can be computed from the world's own column and, once a scheme is built from that spectroscopy, the gas
> absorption as well, while cloud remains to be calibrated for that world against cloud-resolving runs whose
> microphysics can be tested in laboratories and by similarity runs.

**Checked.** The bound from conclusions.tex:35–36; the scheme's evidence state from next.tex:14–16; "remains to
be calibrated" fits PlaSim's uncalibrated cloud (verification.tex:62); the landing and the abstract's last
sentence (abstract.tex:19–21) still state the same contribution. Adds 23 words.

### B2. BLOCKING. The SWAN sentence places the ancient seas of Mars within the patched code's reach

**Location.** conclusions.tex:54–58; the same claim stands at reach.tex:39–40, in the paragraph of a scoped
sentence.

> Patched, SWAN reproduces a sixfold gravity scaling of an Earth sea to 0.3\% in wave height, where the released
> code missed it by 5.4\%, so in a sea under another gravity, the ancient seas of Mars among them, SWAN's gravity
> follows that scaling, as tested at a sixth of Earth's gravity on the code paths those tests ran, and what stays
> uncertain is Earth's empirical laws of drag, wind input and breaking at that sea's ratio of air to water
> density.

**Rule.** The author's direction on untested worlds; "Claims stay within their evidence"; G5; "Exact action".

**Why.** The "so" draws a present-tense claim about a world the work has yet to run, the ancient seas of Mars,
from one test at a sixth of Earth's gravity, and the qualification after it reads as the manner of the claim
("follows that scaling, as tested at…"). "What stays uncertain is" closes the list of uncertainties at Earth's
empirical laws, while verification.tex:48–51 records the lunar runs' spherical grids, nests and GCM forcing as
checked separately or left unchecked. "SWAN's gravity follows that scaling" names no operation; the code keeps
the scaling through its knee, moved to $g/g_\mathrm{E}$~Hz (repairs.tex:67–69). The consequence for Mars
survives in two forms the paper already uses: the released code's arithmetic, which departs from the scaling at
any other gravity (assumptions.tex:22–26), and the "built to" form of a general repair (abstract.tex:11–12).

**Rewrite.**

> Patched, SWAN reproduces a sixfold gravity scaling of an Earth sea to 0.3\% in wave height, where the released
> code missed it by 5.4\% and departs from it on any sea under another gravity, the ancient seas of Mars among
> them; the patch, built to keep the scaling at any gravity, has been tested at a sixth of Earth's on the code
> paths those tests ran, and Earth's empirical laws of drag, wind input and breaking remain uncertain at each such
> sea's ratio of air to water density.

At reach.tex:39–40 the same form serves: "SWAN and SWASH are built to run water seas at any gravity as the
scaled image of an Earth sea, and have been tested at a sixth of Earth's gravity, with Earth's empirical laws."

**Checked.** 0.3% and 5.4% from verification.tex:41–44; the released code's departure from assumptions.tex:22–26;
the patch's design from repairs.tex:67–69; the code-path bound kept. Adds 7 words (reach.tex: adds 4).

### M1. MAJOR. Three passages repeat Next steps, the section the reader has just finished

**Location.** (a) conclusions.tex:41–46; (b) conclusions.tex:58–63; (c) conclusions.tex:71–74, taken up in M4.

> (a) In two windows of an earlier electrified run, made before the ventilation repair and with leakage off, the
> test world's storms separated as much charge under Takahashi's charging law as under Saunders and Peck's,
> within the spread of the Saunders and Peck runs, with the opposite sign, since the two laws disagree on the sign
> that rimed ice takes in little cloud water; a measurement of that sign at 4--8~m\,s$^{-1}$ in
> 0.02--0.2~g\,m$^{-3}$ of cloud water between $-5$ and $-16$\,\textdegree C, conditions laboratories reach, would
> decide the polarity of the lightning.

Against results.tex:155–160 and next.tex:77–81.

> (b) … 85\% of the water falling from the clouds of a box forced from the Earth-orbit state evaporated before it
> reached the ground, against 57--73\% in the rings, and a run with limits scaled to the capillary length would
> measure how much of that evaporation the small drops cause.

Against next.tex:68–72 ("in the boxes 85% of the falling water evaporates, in the rings 57–73% … limits scaled
with the capillary length would show how much of the evaporation the small drops cause") and results.tex:120–122.

> (c) Released and repaired ExoPlaSim on Earth-air planets rotating once in 16 and 64 days, two of the sidereal
> periods at which \textcite{way2018climates} ran ROCKE-3D, with the released radiation, would measure …

Against next.tex:35–40, the same sentence in another order.

**Rule.** AGENTS.md "Conclusions and the arc" (replaying the section order and reciting the inventory are
excluded); charter section 3 (copied conclusions require a substantive reason); the author's rejection of the
earlier version as "largely a laundry list of summary of what was done".

**Why.** Next steps stands directly before this section (main.tex:47–48), so the reader meets these sentences
twice within two pages. Each time the conclusion uses less than it repeats: in (a) the polarity's dependence on
one laboratory measurement, with the charge magnitude and its spread left to Results; in (b) Earth's drop-size
limits against the capillary length, with the evaporation fractions and the scaled-limit run left to Next steps;
in (c) the step that would turn the defects' arithmetic into a measured effect (M4). Most restated material in
the section serves as premise for a relation the body lacks; these three passages develop nothing their
paragraphs use.

**Rewrite (a).**

> In two windows of an earlier electrified run, made before the ventilation repair and with leakage off, the test
> world's storms took opposite polarities under Takahashi's charging law and Saunders and Peck's, which disagree
> on the sign that rimed ice takes in little cloud water; a measurement of that sign at 4--8~m\,s$^{-1}$ in
> 0.02--0.2~g\,m$^{-3}$ of cloud water between $-5$ and $-16$\,\textdegree C, conditions laboratories reach, would
> decide the polarity of the lightning.

**Checked.** results.tex:155–160: the polarity inverted between the laws in those windows, under the conditions
kept here. 18 words shorter.

**Rewrite (b)**, replacing 58–63 from "CM1's":

> CM1's gravity-scaled microphysics remains untested this way, since the pair of runs designed for it failed to
> convect, and its drop-size limits stay Earth's while the largest raindrop that survives its fall scales with the
> capillary length, 2.46 times longer at a sixth of Earth's gravity.

**Checked.** verification.tex:51–52 and assumptions.tex:85–88. 47 words shorter; paragraph 5 then ends on the
physical law a modeller of any low-gravity world needs.

**Map of restated material**, for the judgement in section 4:

| Paragraph | Lines restating the body (source) | Lines carrying a relation the body lacks |
|---|---|---|
| 1 | 3–6 (abstract.tex:8–13; introduction.tex:70–83); 6–11 (assumptions.tex:98–113; reach.tex:16–24) | 8–11 as reminder: the consequence for natural planets |
| 2 | 15–17 numbers (assumptions.tex:105–117); 18–20 (results.tex:47–52); 22–25 (results.tex:82–86) | 13–14, 14–15 (the defects keep the arriving global mean); 20–22 (maps by longitude and season) |
| 3 | 27–29 (abstract.tex:16–19; results.tex:91–94; reach.tex:3–8); 30–32 (assumptions.tex:42–47); 34–37 (abstract.tex:19–21; next.tex:14–16) | 29–30 hinge; 32–34 Titan's haze; 37–38 cloud calibration resting on Earth-fitted microphysics |
| 4 | 41–46 (results.tex:155–160; next.tex:77–81); 46–48 (results.tex:150–153); 48–51 (results.tex:138–150) | 40–41 (laws testable apart from any world); 51–52 (resolved storms at other gravities test the flash-rate laws) |
| 5 | 54 (verification.tex:39–41); 54–58 (abstract.tex:15–16; verification.tex:41–50); 58–59 (verification.tex:51–52); 60–63 (assumptions.tex:85–88; next.tex:68–72) | 56–58, the Mars clause (B2) |
| 6 | 65–68 (introduction.tex:19–26); 68–69 (introduction.tex:50–52); 69–70 (reach.tex:62–63); 70–74 (next.tex:35–40); 74–76 (abstract.tex:19–21) | 66–67 (lost natural air and departing ratios on one body); 69–70 framed for designers |

### M2. MAJOR. Paragraph 2 ends on a comparison whose relation to the test world's finding stays unwritten

**Location.** conclusions.tex:20–25.

> An error of this kind leaves a check of the arriving sunlight's global mean unchanged, and it shows in maps of
> sunlight by longitude and of rain by season. Models can agree in their global means and still disagree widely
> in where cloud lies: on two tidally locked planets, …

**Rule.** G1 and "Inheritance and order" (swap test); "Sentences carry their dependencies"; G2 (redundancy).

**Why.** The first clause restates the paragraph's opening (13–14). The two sentences trade places with little
loss, so the relation between them stays unwritten, and that relation is the paragraph's consequence for the
field: on the test world the defects moved the global means through cloud while keeping the arriving sunlight's
global mean, and in Yang et al.'s comparison models whose cloud cover differed by two to three and a half times
agreed in their global means, so a check by global means passes errors of this kind, whether it compares the
arriving sunlight or the models' climates. The rewrite states that relation with an evidentiary colon, names the
modeller as the one who reads the maps, and leaves the implication for model comparisons implicit, as the
direction asks. "It shows in maps" uses a generic verb where the operation is a modeller reading maps.

**Rewrite.**

> A modeller finds such an error in maps of sunlight by longitude and of rain by season, and a comparison of
> models by their global means can pass it: on two tidally locked planets, the quasi-global cloud-permitting runs
> of \textcite{yang2023cloud} covered 27 and 41\% of the sky with cloud and two GCMs whose cover follows relative
> humidity, stability and large-scale ascent covered 82--97\%, while the three models' global-mean surface
> temperatures and albedos came out broadly alike.

**Checked.** Numbers from results.tex:84–86; "can pass" states a possibility that the alike global means
support, and the sentence names only Yang et al.'s comparison. 15 words shorter.

### M3. MAJOR. Paragraph 4 leaves its point on exoplanet lightning unwritten and names a field from two studies

**Location.** conclusions.tex:46–52.

> The flash-rate laws used for tidally locked planets were fitted to Earth's storms and set the flash rate from
> the cloud-top height or from the graupel and ice aloft \autocite{braam2022lightning,sergeev2025lightning}. At a
> sixth of Earth's gravity the freezing levels of six Morrison runs stood five to six times their heights in
> Earth's tropics, and the main electrified run, forced from the Earth-orbit state, flashed at about a hundredth
> of Earth's average density, …

**Rule.** "Claims stay within their evidence" (a statement about a field says what the cited works did; compare
the rejected "Exoplanet climate studies compute…"); "Sentences carry their dependencies" (coordination joins
equal-weight propositions); G3.

**Why.** "The flash-rate laws used for tidally locked planets" reads as the field's laws, and the citations name
two studies. The next sentence joins with "and" a premise, storms five to six times taller, and a result in
tension with the laws' predictor, a resolved storm flashing at a hundredth of Earth's density; and the freezing
level is the predictor of neither law. The six Morrison runs' cloud tops, 55–80 km (results.tex:140–141), are
the cloud-top law's own predictor. Written as a contrast on that predictor, the sentence states the evidence
from which exoplanet modellers draw the consequence: a law fitted on Earth's storms, read at cloud tops far
outside them.

**Rewrite.**

> The flash-rate laws with which \textcite{braam2022lightning} and \textcite{sergeev2025lightning} estimated
> lightning on tidally locked planets were fitted to Earth's storms and set the flash rate from the cloud-top
> height or from the graupel and ice aloft. At a sixth of Earth's gravity the cloud tops of six Morrison runs rose
> to 55--80~km, far above the storms the cloud-top law was fitted on, while the main electrified run, forced from
> the Earth-orbit state, flashed at about a hundredth of Earth's average density, part of the difference possibly
> from its grid; electrified storms resolved at other gravities, computed with the same laboratory charging laws,
> could test those flash-rate laws, a route \textcite{sergeev2025lightning} also propose.

**Checked.** Cloud tops from results.tex:138–141, which belong to the six Morrison runs and stay apart from the
electrified run; flash density and grid from results.tex:145–150; "far above" rests on the premise that both laws
were fitted to Earth's storms (results.tex:150–153). The freezing-level comparison stays in Results. Adds 8 words.

### M4. MAJOR. Paragraph 6 joins two movements at an unmarked turn and restates the opening pages

**Location.** conclusions.tex:65–74, with B1 at 74–76.

> On such a world the Earth values that depend on those ratios err together. For its designers the calibrations
> hold near the columns they were fitted on, so a lower pressure or another shield would need them refitted. Away
> from Earth's values every change made for the test world has run on it alone. Released and repaired ExoPlaSim
> on Earth-air planets …

**Rule.** "Inheritance and order" (each sentence receives and transforms); G2 (delete test); "Conclusions and the
arc"; "Exact action" and the human-presence pass.

**Why.** The paragraph moves at 70 from the constructed world to natural planets with the relation between the
two left out: "Away from Earth's values every change made for the test world has run on it alone" receives
nothing from the designers' sentence before it and opens the second movement as a fresh declarative. The
sentence at 68–69 restates introduction.tex:50–52 and the implication of the clause before it, and fails the
delete test. "For its designers the calibrations hold" sets the calibrations holding for people, where the
operation is a designer changing the design and refitting. The test sentence repeats next.tex:35–40 (M1 c).
Joined by "since", the evidence state becomes the reason for the test, and the test becomes the step that would
turn paragraph 1's arithmetic biases into measured effects on worlds other studies model, the relation the
paragraph lacks.

**Rewrite (whole paragraph, with B1).**

> By one design's own models, a shield in space that removes the ultraviolet heating the upper air would keep
> Earth-like air on the Moon for tens of billions of years, on a body whose escape velocity let its natural
> atmosphere go, so that gravity, column and the air's height against the radius depart from Earth's together,
> and the Moon's tidal lock adds a 29.53-day day. A designer who lowers the pressure or changes the shield moves
> the columns off those the calibrations were fitted on, and would need the calibrations refitted. On natural
> planets the three defects' biases are known so far from the code's arithmetic, since away from Earth's values
> every change made for the test world has run on it alone; released and repaired ExoPlaSim on Earth-air planets
> rotating once in 16 and 64 days, two of the sidereal periods at which \textcite{way2018climates} ran ROCKE-3D,
> with the released radiation, would measure them in the climate of worlds that other studies model and test the
> Sun-clock and convective-cover repairs there. For a new world whose gases, pressures and temperatures the
> line-by-line spectroscopy covers, the geometry of its air can be computed from the world's own column and, once
> a scheme is built from that spectroscopy, the gas absorption as well, while cloud remains to be calibrated for
> that world against cloud-resolving runs whose microphysics can be tested in laboratories and by similarity
> runs.

**Checked.** The design's numbers unchanged (introduction.tex:21–25); refits for another pressure or shield from
reach.tex:62–63; the test and its conditions from next.tex:35–40; "the code's arithmetic" from conclusions.tex:8.
Adds 22 words, all from B1's bound.

### R1. MAJOR. "Reached" in the new Results sentence is an empty action the rules name

**Location.** results.tex:48–52.

> The Sun and tilt reached the global means through the clouds: in a two-year test of the two alone, with the old
> split, the clouds' effect in sunlight weakened …

**Rule.** AGENTS.md "Exact action" (an abstraction that "reaches" performs an empty action); "Nouns are precise".

**Why.** The synodic clock and the Moon's tilt, as changes to the run, changed the global means by changing the
clouds; "reached" names no operation. "The old split" leaves the reader to work out which split; in the table of
GCM states it is the Earth-orbit state's split, before the recalibration that came with the Sun-and-tilt state. The
inserted sentence also stands between the Sun-and-tilt step and "The curved air, on the table's first channels,
then cooled it by 0.65~K" (52–53), whose baseline is the Sun-and-tilt run (results.tex:68–69), so "then" now
appears to follow the two-year test.

**Rewrite.**

> The Sun and tilt changed the global means through the clouds: in a two-year test of the two alone, with the
> Earth-orbit state's split of sunlight, the clouds' effect in sunlight weakened …

and at 52–53: "From the Sun-and-tilt state, the curved air, on the table's first channels, cooled it by 0.65~K, …"

**Checked.** Table states rows at results.tex:26–27; the baselines in the caption at results.tex:65–70. Adds 3
words, and 3 more for the second change.

### m1. MINOR. A premise the expert reader holds

**Location.** conclusions.tex:14–15.

> At any instant the sunlight a latitude circle receives depends on the Sun's declination and distance alone, so
> the Sun clock, which errs in the Sun's longitude, keeps every zonal mean …

**Rule.** "Write for the expert" (delete test); G2.

**Why.** A modeller of atmospheres holds the premise that a zonal mean of insolation is independent of the Sun's
longitude; "errs in the Sun's longitude alone" supplies the inference in one added word.

**Rewrite.** "The Sun clock, which errs in the Sun's longitude alone, keeps every zonal mean of the arriving
sunlight, while the test world's equator received up to 17\% more than its mean in one sector and 8\% less in
another; …"

**Checked.** assumptions.tex:100–107. 17 words shorter.

### m2. MINOR. "Keep the global mean" holds on the test world; the orbit default also replaces eccentricity

**Location.** conclusions.tex:13–14.

> Two of the three keep the global mean of the sunlight arriving at the top of the air and move that sunlight
> between places.

**Rule.** "Claims stay within their evidence"; G5.

**Why.** ExoPlaSim's orbit default replaces the configured obliquity and eccentricity with Berger's values for
1 AD, 23.695° and 0.0175 (models/exoplasim/README.md:57). The obliquity leaves the global mean as it was; the
eccentricity changes the annual mean by the factor $(1-e^2)^{-1/2}$, which on the test world, configured at
0.016715 (README:61), moves it by about $1.3\times10^{-5}$ (the reviewer's arithmetic), and on a world
configured with a larger eccentricity moves it more. Every number in the paragraph comes from the test world, so
the scope costs nothing.

**Rewrite.** "On the test world two of the three kept the global mean of the sunlight arriving at the top of the
air and moved that sunlight between places."

**Checked.** Adds 4 words.

### m3. MINOR. The dry-land share is offered as a global-mean effect through cloud

**Location.** conclusions.tex:18–20.

> The moved sunlight changed the clouds, and through them the global means: in a two-year test of the Sun and
> tilt alone, the clouds' effect in sunlight weakened by 2.4~W\,m$^{-2}$, the test world ran 0.9~K warmer while
> still gaining heat, and the share of land under half a millimetre of rain a day rose from 9 to 36\%.

**Rule.** "Sentences carry their dependencies"; G1.

**Why.** The colon's claim concerns global means moved through cloud; its third item is a seasonal-rain effect,
which results.tex:47–48 explains by Earth's tilt bringing summer rain to 60°. Placed with the orbit default, the
item becomes the evidence for the "rain by season" maps of the sentence after.

**Rewrite.** "… the orbit default, which put Earth's tilt in place of the configured one, brought Earth's seasons
and summer rain to 60\textdegree, and in a two-year test of the Sun and tilt alone the share of land under half a
millimetre of rain a day rose from 9 to 36\%. The moved sunlight changed the clouds, and through them the global
means: in the same test the clouds' effect in sunlight weakened by 2.4~W\,m$^{-2}$, and the test world ran 0.9~K
warmer while still gaining heat."

**Checked.** results.tex:47–52. About the same length.

### m4. MINOR. The scope of "runs of natural planets"

**Location.** conclusions.tex:8–9.

> … and by the code's own arithmetic they bias ExoPlaSim's runs of natural planets: …

**Rule.** "Claims stay within their evidence".

**Why.** The examples after the colon state the conditions, while the clause before it reads as every run of a
natural planet; reach.tex:16–17 states the scope as "any run that meets their conditions".

**Rewrite.** "… they bias ExoPlaSim's runs of natural planets that meet their conditions. The convective-cover
unit adds …" The split at the colon also serves m8.

**Checked.** Adds 4 words.

### m5. MINOR. Paragraph 3's hinge and its drifting referents

**Location.** conclusions.tex:29–30 and 35.

> The parts differ in what a modeller of a new world would need.
>
> … the radiation's gas fits, the largest of them, …

**Rule.** Precise nouns; G3 (inheritance).

**Why.** "The parts" inherits "the parts fitted to Earth's atmosphere" from 27, while the next sentence opens on
the geometry, a part with no fit; "them" at 35 refers back past Titan's aerosol codes to 27. The paragraph's
order runs from what the world's column fixes (geometry), through what spectroscopy could fix (gas absorption),
to what each world must calibrate (cloud), and the hinge can state that order.

**Rewrite.** "What a modeller of a new world needs for each part depends on how far the world's own column
determines it." and "… the radiation's gas fits, the largest of the Earth fits, …"

**Checked.** Adds 10 words.

### m6. MINOR. "Stays a calibration" for a cloud that is uncalibrated today

**Location.** conclusions.tex:37.

> Cloud amount stays a calibration for each world, fitted to cloud-resolving runs of that world, …

**Rule.** G5 (evidence state).

**Why.** PlaSim's cloud amount is uncalibrated (verification.tex:62), and fitting it to CM1 is a next step
(next.tex:18–25); "stays" reads as a calibration in hand. The sentence continues the conditional of 34–37.

**Rewrite.** "Cloud amount would stay a calibration for each world, …"

**Checked.** Adds 1 word.

### m7. MINOR. Paragraph 5's hinge: relation and scope

**Location.** conclusions.tex:54.

> Gravity stays fixed in a laboratory on Earth, and a model's dependence on it is tested by similarity runs.

**Rule.** "Sentences carry their dependencies"; "Claims stay within their evidence".

**Why.** The second clause follows from the first, and "and" leaves the cause unwritten. Verification scoped
the premise to a sea's laboratory (verification.tex:39–41); the paragraph covers a sea and falling drops.

**Rewrite.** "Gravity stays fixed in a wave tank or a cloud laboratory on Earth, so a model's dependence on it is
tested by similarity runs."

**Checked.** Adds 5 words.

### m8. MINOR. Cadence of paragraph 1 and a recurring frame

**Location.** conclusions.tex:3–11, and the section.

> Earth values in four forms and five defects were found in four Earth-built codes adapted to a world that
> departs from Earth along four ratios at once, …

**Rule.** G3 (cadence, silent reading); "Vary openings, subjects, lengths and stress".

**Why.** The reminder runs as two sentences of 74 and 95 words, and its first clause counts four, five, four and
four within its first 25 words. Across the section a claim followed by a colon and a list of evidence recurs at
5, 9, 18, 22 and 27; the m4 split removes one of these. With the ratios named, the reader has the quantities the
later paragraphs use.

**Rewrite.** "… adapted to a world that departs from Earth at once in gravity, column mass, scale height over
radius and day, …", with the second sentence split at its colon (m4).

**Checked.** Names from abstract.tex:7–8 and worlds.tex:3–9. Adds 6 words.

### m9. MINOR. Results: Yang et al.'s comparison compares schemes with runs

**Location.** results.tex:82–86.

> GCM cloud schemes of this kind, which set the cover from relative humidity, stability and large-scale ascent,
> differ widely from cloud-permitting runs on tidally locked planets as well: …

**Rule.** Precise nouns; G3.

**Why.** Schemes are set against runs, and "as well" lacks a stated antecedent, since the paragraph compares
PlaSim's cover with no cloud-permitting cover on the test world. Stating what the GCMs computed removes both.

**Rewrite.** "On two tidally locked planets, TRAPPIST-1e and K2-72e, GCMs with cloud schemes of this kind, which
set the cover from relative humidity, stability and large-scale ascent, covered 94.8 and 81.7\% of the sky in
CAM3 and 90.4 and 97.4\% in ExoCAM, against 26.9 and 41.1\% in a quasi-global cloud-permitting model, while the
three models' global-mean surface temperatures and albedos came out broadly alike \autocite{yang2023cloud}."

**Checked.** Numbers unchanged; about 10 words shorter. The sentence after (86–91) opens on the longwave
correction with nothing inherited from this one; that sentence lies outside the scope.

### m10. MINOR. Abstract: the constructed-worlds sentence

**Location.** abstract.tex:4–6.

> Constructed worlds widen that range, since, by one design's own models, an engineered shield can hold
> Earth-like air under a gravity too weak to keep it naturally.

**Rule.** "Exact action"; precise nouns.

**Why.** "That range" has no named antecedent in the sentence before; "worlds widen" assigns an action to a class
of worlds; and a shield in space holds no air, the design's mechanism being the removal of the ultraviolet that
heats the upper air (introduction.tex:21–24).

**Rewrite.** "A constructed world can depart further: by one design's own models, a shield in space that removes
the ultraviolet heating the upper air keeps Earth-like air under a gravity too weak to hold it naturally."

**Checked.** The evidence state "by one design's own models" kept. Adds 7 words.

### m11. MINOR. Abstract: the place of the SWAN sentence

**Location.** abstract.tex:13–16.

> Identity, reproduction, arithmetic and gravity-similarity checks and Earth benchmarks test the code, and the
> calibrations test it against the line-by-line model; the lunar climate is unobserved. Patched, SWAN reproduces
> a sixfold gravity scaling of an Earth sea to 0.3\% in wave height, where the released code misses it by 5.4\%.

**Rule.** G3 (inheritance).

**Why.** The SWAN result is the instance of the gravity-similarity checks named in the sentence before, and the
evidence-state clause stands between them, so the SWAN sentence reads as an addition. With the clause after the
SWAN result, it closes the checks and the next sentence's model results open on it.

**Rewrite.** "Identity, reproduction, arithmetic and gravity-similarity checks and Earth benchmarks test the code,
and the calibrations test it against the line-by-line model. Patched, SWAN reproduces a sixfold gravity scaling
of an Earth sea to 0.3\% in wave height, where the released code misses it by 5.4\%; the lunar climate is
unobserved."

**Checked.** Same length. The SWAN sentence itself is exact and within its evidence.

### m12. MINOR. Reach: "every run … is of the test world"

**Location.** reach.tex:41–43.

> Of the natural worlds in Figure~\ref{fig:regimes}, Earth alone lies near the fits in the adapted models, and
> every run of those models away from Earth's values is of the test world.

**Rule.** "Claims stay within their evidence".

**Why.** SWASH's dispersion checks ran at four times lunar gravity (verification.tex:44–46), runs away from
Earth's values that model no world. The claim the sentence needs concerns the worlds simulated. The same wording
recurs in the Table reach caption (reach.tex:86–87); at next.tex:35 and conclusions.tex:70–71 it is written for
"the repaired models" and "every change made for the test world" and holds as written.

**Rewrite.** "… and the test world is the only world those models have simulated away from Earth's values."

**Checked.** Adds 1 word.

### m13. MINOR. Reach: the slow rotators' sentence

**Location.** reach.tex:49–55.

> For slowly rotating planets with Earth's gravity and air around a Sun-like star near Earth's insolation, such as
> the cooler runs that \textcite{yang2014strong} and \textcite{way2018climates} made with CAM3 and ROCKE-3D,
> ExoPlaSim needs …, while its cloud keeps Slingo's fit to Earth's convection and PlaSim's Earth-tuned thresholds,
> and cloud is among the processes through which those studies found the climate to change with rotation; their
> warmer runs, at up to 2.9 times Earth's insolation, lie beyond the radiation's fits, and the runs have yet to be
> made.

**Rule.** Precise nouns; "Sentences carry their dependencies"; G5.

**Why.** "Planets … such as the cooler runs" sets planets beside runs. "And cloud is among the processes" joins,
as an equal, the reason the cloud's Earth fits matter for these planets. "The runs have yet to be made" follows
"their warmer runs", which Way et al. made, so the sentence's evidence state can attach to the wrong runs.

**Rewrite.** "… such as those of the cooler runs that \textcite{yang2014strong} and \textcite{way2018climates}
made with CAM3 and ROCKE-3D, … while its cloud keeps Slingo's fit to Earth's convection and PlaSim's Earth-tuned
thresholds, Earth fits of a process through which those studies found the climate to change with rotation; their
warmer runs, at up to 2.9 times Earth's insolation, lie beyond the radiation's fits, and ExoPlaSim's runs of these
planets have yet to be made."

**Checked.** Adds 4 words.

### m14. MINOR. Next steps: "Earth-sized columns"

**Location.** next.tex:37–38.

> … with the released radiation, which suits their Earth-sized columns, …

**Rule.** Precise nouns; "Exact action".

**Why.** The columns are Earth's in mass and composition, and "suits" stands for "was fitted on";
reach.tex:51–52 states it exactly.

**Rewrite.** "… with the released radiation, fitted on columns like theirs, …"

**Checked.** Same length.

### Assembled paragraphs

These combine the rewrites above for the paragraphs where several interact, so they can be read as prose.

**Paragraph 2** (m2, m1, m3, M2; 250 words to 227):

> On the test world two of the three kept the global mean of the sunlight arriving at the top of the air and moved
> that sunlight between places. The Sun clock, which errs in the Sun's longitude alone, keeps every zonal mean of
> the arriving sunlight, while the test world's equator received up to 17\% more than its mean in one sector and
> 8\% less in another; the orbit default, which put Earth's tilt in place of the configured one, brought Earth's
> seasons and summer rain to 60\textdegree, and in a two-year test of the Sun and tilt alone the share of land
> under half a millimetre of rain a day rose from 9 to 36\%. The moved sunlight changed the clouds, and through
> them the global means: in the same test the clouds' effect in sunlight weakened by 2.4~W\,m$^{-2}$, and the test
> world ran 0.9~K warmer while still gaining heat. A modeller finds such an error in maps of sunlight by longitude
> and of rain by season, and a comparison of models by their global means can pass it: on two tidally locked
> planets, the quasi-global cloud-permitting runs of \textcite{yang2023cloud} covered 27 and 41\% of the sky with
> cloud and two GCMs whose cover follows relative humidity, stability and large-scale ascent covered 82--97\%,
> while the three models' global-mean surface temperatures and albedos came out broadly alike.

**Paragraph 4** (M1 a, M3; 216 words to 206):

> Some of those Earth-fitted laws can be tested apart from any one world, in laboratories on Earth or in runs at
> other gravities. In two windows of an earlier electrified run, made before the ventilation repair and with
> leakage off, the test world's storms took opposite polarities under Takahashi's charging law and Saunders and
> Peck's, which disagree on the sign that rimed ice takes in little cloud water; a measurement of that sign at
> 4--8~m\,s$^{-1}$ in 0.02--0.2~g\,m$^{-3}$ of cloud water between $-5$ and $-16$\,\textdegree C, conditions
> laboratories reach, would decide the polarity of the lightning. The flash-rate laws with which
> \textcite{braam2022lightning} and \textcite{sergeev2025lightning} estimated lightning on tidally locked planets
> were fitted to Earth's storms and set the flash rate from the cloud-top height or from the graupel and ice
> aloft. At a sixth of Earth's gravity the cloud tops of six Morrison runs rose to 55--80~km, far above the storms
> the cloud-top law was fitted on, while the main electrified run, forced from the Earth-orbit state, flashed at
> about a hundredth of Earth's average density, part of the difference possibly from its grid; electrified storms
> resolved at other gravities, computed with the same laboratory charging laws, could test those flash-rate laws,
> a route \textcite{sergeev2025lightning} also propose.

**Paragraph 5** (m7, B2, M1 b; 193 words to 158):

> Gravity stays fixed in a wave tank or a cloud laboratory on Earth, so a model's dependence on it is tested by
> similarity runs. Patched, SWAN reproduces a sixfold gravity scaling of an Earth sea to 0.3\% in wave height,
> where the released code missed it by 5.4\% and departs from it on any sea under another gravity, the ancient
> seas of Mars among them; the patch, built to keep the scaling at any gravity, has been tested at a sixth of
> Earth's on the code paths those tests ran, and Earth's empirical laws of drag, wind input and breaking remain
> uncertain at each such sea's ratio of air to water density. CM1's gravity-scaled microphysics remains untested
> this way, since the pair of runs designed for it failed to convect, and its drop-size limits stay Earth's while
> the largest raindrop that survives its fall scales with the capillary length, 2.46 times longer at a sixth of
> Earth's gravity.

**Paragraph 6** is given whole in M4 (212 words to 234).

With every rewrite applied, paragraphs 1 and 3 add 10 and 11 words, and the section goes from 1,250 words to
about 1,225.

### Observations outside the scope

- results.tex:93 has "moved it by more than 20~K", beside "at least 20~K" at results.tex:39, abstract.tex:18,
  conclusions.tex:28 and reach.tex:4.
- abstract.tex:19–21 has "physics that holds across worlds". With B1 bounded, this would be the paper's only
  unbounded form of the claim, and the final-page pass asks the abstract and the conclusion to land alike.
- repairs.tex:106–108 attributes Titan's 65° to Titan's air, "taller in proportion", where
  conclusions.tex:32–34 ties it to the haze and worlds.tex:77–78 puts Titan's air at about a quarter of the test
  world's height in proportion.

## 3. What works

- **The section argues.** Its paragraphs follow one line: the defects whose errors pass a global-mean check (2),
  what a modeller of a new world computes and what each world calibrates (3), how the Earth-fitted laws inside
  those calibrations can be tested apart from any world, by laboratory and by runs at other gravities (4, 5),
  and the constructed world with the first test off the test world (6). Paragraphs 2, 4 and 5 open on what the
  paragraph before ends with (the three defects; "Earth-fitted microphysics of their own"; "runs at other
  gravities"), and paragraph 6 opens a deliberate final turn.
- **Paragraph 1 reminds** in two sentences and lands on a consequence for natural planets, with its evidence
  state named ("by the code's own arithmetic"): with TRAPPIST-1e's convective cover and the Sun clock of any slow
  rotator, modellers of exoplanets have a check for their own runs.
- **Paragraph 2 is the section's strongest discussion.** It develops a mechanism and a diagnostic: errors that
  keep the arriving sunlight's global mean moved the global means through cloud, and a modeller finds them in
  maps by longitude and by season.
- **Paragraph 3's order is an argument**, from computed geometry through spectroscopy to calibrated cloud, and
  in the Titan haze comparison the paragraph names a natural world whose haze stands as tall against its radius
  as the test world's air, leaving the use of the curved-air geometry there implicit.
- **Paragraph 4 names work others can take up:** a laboratory measurement with the speeds, cloud water and
  temperatures it needs, and resolved storms at other gravities as a test of the flash-rate laws.
- **Evidence states are marked** where they bound a claim: "by one design's own models", "by the code's own
  arithmetic", "would", "could", "has run on it alone", "part of the difference possibly from its grid".
- **Diction is clean.** No "not", no "rather than"; the three negations ("no coefficient", "little or no error",
  "failed to convect") are required by meaning; no stock transitions, self-reference, promotional words or
  witticisms.
- **The arc holds.** The abstract's last sentence and the section's last sentence land on the same contribution,
  gas absorption from spectroscopy and cloud calibrated for each world, and the introduction's two questions
  (where a model's Earth values lie; which repairs made for one world hold on another) are answered in
  paragraphs 1 to 3.
- **The other passages.** The reach sentence at 41–43 serves as the hinge into "Worlds near the existing fits"
  by naming Earth as the only natural world near the fits; that paragraph attaches each calibration's evidence
  state to its claim (45–49). Next steps' "A test of the reach" names the question, the outputs, the comparison
  and the result that would change Table reach, the question-to-test mapping G5 asks for, and lands on that
  result. The new Results sentence attaches "while still gaining 1.9~W\,m$^{-2}$" to the warming it bounds. The
  abstract's SWAN sentence is exact.

## 4. Counts and judgement

**Counts.** BLOCKING 2 (B1, B2); MAJOR 5 (M1, M2, M3, M4, R1); MINOR 14 (m1–m14). By file: conclusions.tex 2
BLOCKING, 4 MAJOR and 8 MINOR; results.tex 1 MAJOR and 1 MINOR; abstract.tex 2 MINOR; reach.tex 2 MINOR;
next.tex 1 MINOR. Proposals that add length: B1 (+23 words), B2 (+7), M3 (+8), M4 (+22, from B1), R1 (+6), m2,
m4, m5, m6, m7, m8, m10, m12, m13 (+1 to +10 each); proposals that shorten: M1 (−18 and −47), M2 (−15), m1 (−17),
m9 (about −10).

**Judgement.** The section now meets most of the author's direction: it reminds in its first paragraph and then
argues, paragraph by paragraph, toward what a modeller of an exoplanet or a constructed world can compute from a
world's column and what each world must calibrate, drawing consequences for both kinds of world in the evidence
itself (biased ExoPlaSim runs of TRAPPIST-1e and of slow rotators, errors that pass a check of the arriving
sunlight's global mean, Earth-fitted laws that laboratories and runs at other gravities can test, a refit at
each change of design). Two sentences
break the direction as the author stated it: the closing sentence opens the method to "any new world" and drops
the bound the section states twelve lines earlier, and the SWAN sentence places the ancient seas of Mars inside
the patched code's reach by inference from one test. One habit remains, and it is the one the author named:
three passages repeat Next steps, the section the reader has just read, nearly word for word, and much of the
rest restates Results and Verification as premises, so that nearly a fifth of the section's five-word sequences
recur verbatim. With B1 and B2 bounded, the three repeated passages cut to what each paragraph uses, and the relations
of M2 to M4 written into the syntax, the section would read as real discussion and land on the abstract's
contribution at about its present length.
