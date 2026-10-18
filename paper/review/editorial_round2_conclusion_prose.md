# Editorial reading, round 2: "Discussion and conclusions" and the reach heading

## 1. Record

| Item | Value |
|---|---|
| Reviewer | A fresh Claude subagent, Claude Opus 5.5 (`claude-opus-5-5[1m]`), launched for this reading alone. It saw no earlier review and opened nothing under `paper/review/` (apart from writing this file) or `paper/notes/`. |
| Date | 2026-10-17 |
| Snapshot | Commit `bb5d0f00992515295bcaa10ce9ebe4b1a0f19641`, "Rewrite the conclusions as discussion and conclusions, and keep the reach section's heading to what has run". The working tree matched it for `AGENTS.md` and `paper/sections/`. |
| In scope | `paper/sections/conclusions.tex`, the whole section. `paper/sections/reach.tex`, lines 47–56 (the run-in heading and its paragraph), read with the group headings at lines 58 and 72 and the paragraph before it, lines 27–45. |
| Rule files, read in full | `AGENTS.md` at the snapshot. In Terluna at commit `f03b839`: `ensemble/planning/Open_Moon_Editorial_Charter_control-01.md` and, in `ensemble/planning/source_controls/`, `STYLE_NOTES.md`, `Jewish_Papers_Updated_Style_Notes.md` and `Agent_Working_State_Editorial_Gates.md`. |
| Paper read in full | `abstract.tex`, `introduction.tex`, `conclusions.tex`, `reach.tex`, `results.tex`, `next.tex`, `verification.tex`, `worlds.tex`, `assumptions.tex`, `repairs.tex`, `main.tex`. |
| Read in part | `appendix.tex`, lines 1–20 and 36–60 (the classes of change); `paper/tools/lint.py`, its header and patterns; `paper/sources/manifest.json`, the records of vincendon2010spherical, way2018climates, yang2014strong and yang2023cloud; the archived original of Way et al. (2018), searched in its text layer for the rotation periods run; the commit message of bb5d0f0 and its diff of `reach.tex`, for the heading's previous wording. |
| Method | Each paragraph read whole, then sentence by sentence, under the ten passes of the charter's section 11 and the rules in AGENTS.md "Writing". Each figure and claim in scope was traced to the body section that reports it. |
| Cadence | Silent reading only. An audible reading, or the author's own reading, of this section remains pending. |
| Screening | `lint.py` run on both files, reported as screening only: no "not" and no "rather than" in either file in scope; three negations in the conclusion (lines 5, 7, 59), each required by its proposition. The other hits were read, and those that hold appear below as findings. |
| PDF | Outside this reading (G7). |

sha256 of each file cited, at bb5d0f0 unless stated:

| File | sha256 |
|---|---|
| `paper/sections/conclusions.tex` (in scope) | `a191f07ede146003ce1664863ad9c81dd824436e95610ec8531764e880f5a32d` |
| `paper/sections/reach.tex` (in scope) | `483668bcbfa5c3800e198a211fe8bde23a049621a433b076707731f39277f6d2` |
| `AGENTS.md` | `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32` |
| Terluna `Open_Moon_Editorial_Charter_control-01.md` (agrees with the hash AGENTS.md cites) | `aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0` |
| Terluna `STYLE_NOTES.md` | `659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46` |
| Terluna `Jewish_Papers_Updated_Style_Notes.md` | `18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab` |
| Terluna `Agent_Working_State_Editorial_Gates.md` | `553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464` |
| `paper/sections/abstract.tex` | `77110b76b51fe6344a42ce39269f79f40f0ce13b84b45a34d379bc108d05fcb7` |
| `paper/sections/introduction.tex` | `b8325d641b56d6da32cffbcaa143e26461495322235c2de3b0709402f1ef5b72` |
| `paper/sections/results.tex` | `84222578242a78e05394215ed333b71fd81633a5d6e99eeeb6556e603039fa71` |
| `paper/sections/next.tex` | `c0efe8d232f6d8c592829d5b9d3a553555e6be460ba652f87447e0e04d15d3b7` |
| `paper/sections/verification.tex` | `4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00` |
| `paper/sections/worlds.tex` | `453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112` |
| `paper/sections/assumptions.tex` | `01d5eea0744342fba7ef3eea7d274976cc88744f5d97e4a3ca16b2e1751fb50e` |
| `paper/sections/repairs.tex` | `bb1d22c01616fdaf454280acded56316b7995af2a8fc3bb5a255af52c92e793c` |
| `paper/sections/appendix.tex` | `20cc69d4ef20554c2667c37f8654dcc3814b43a662ace234c709741581bc5004` |
| `paper/main.tex` | `be6759e766899797bd11d33ba9663dbea68a9b6938d741c9a1dd4dea9b70eeca` |
| `paper/sources/manifest.json` | `334f5973fe6339026237ca7953369c34e5f4a1cce89ef935bccd7ccfa76a66a4` |
| `paper/tools/lint.py` | `27f9b47a1f4837583b75eb750e302531f3e07a44e452983dd9ddce2b35657367` |
| `paper/sources/originals/way2018climates.pdf` (local, ignored by Git; agrees with the manifest) | `476e3e967e5d7eeafea1f386fc801851106365653bd3d9132c5821edb7164820` |

## 2. Findings

Severity: BLOCKING breaks the author's direction or a rule in a way the author would reject; MAJOR is a clear
breach; MINOR is polish. Locations are file:line at bb5d0f0, and "P1" to "P6" are the conclusion's paragraphs
(lines 3–9, 11–20, 22–34, 36–49, 51–57, 59–69). Each rewrite was checked against AGENTS.md "Writing" and against
the body sections that hold its evidence.

### F1. BLOCKING. The section reads the results a second time

**Location.** `conclusions.tex`:3–69, the whole section.

**Rule.** AGENTS.md, "Conclusions and the arc": a conclusion gathers the developed lines into a new relation or
consequence, and replaying the section order and reciting the inventory are excluded; charter section 11, the
same requirement; G1, the swap test; the author's direction of 2026-10-17, an actual conclusion with real
discussion, which reminds and excites.

**What the text does.** The paragraphs keep the paper's own order, and most sentences restate a sentence from
an earlier section:

| Paragraph | Restates |
|---|---|
| P1 (3–9) | abstract:8–13, the forms, defects and classes in the same gapped sentence; introduction:70–83 |
| P2 (11–20) | assumptions:100–118 (Sun clock, orbit default); results:44–48 (rain, 0.6 K); reach:17–19 (33°) |
| P3 (22–34) | results:86–89, the ranking, nearly word for word; results:94–122 (the gap between the models); results:78–82 (Yang et al.); next:14–16 (the scheme from spectroscopy) |
| P4 (36–49) | results:151–156 and next:77–82 (charging laws); assumptions:85–88 (capillary length); results:146–149 (flash-rate laws); results:134–143 (cloud tops, flash density) |
| P5 (51–57) | abstract:15–16 and verification:41–44 (SWAN); assumptions:24–26 (Mars); repairs:105–108 (curved air, Titan) |
| P6 (59–69) | introduction:15–26 and 46–52 (constructed worlds); repairs:3–9 (the record); next:35–39 (the slow-rotator runs) |

P2 to P5 take the subsections of `results.tex` in their order: what each repair changed, the gap between the
models, storms and lightning, seas. The section carries 43 numerals in about 1,100 words, most at the precision
of the results (270° to 57° E, 164° E, the lowest 1.8 km at 45° N) where its argument needs only a size, and
the silent reading slows under them in P2 to P4.

The discussion is real and confined to about six sentences and tail clauses: P2's first sentence (errors that
keep a global quantity and move its distribution); P3's last two (the radiation's fits replaceable, cloud a
calibration whose own source is Earth-fitted); P4's first (laws that laboratories on Earth can test); the last
clause of P4 (resolved storms as the test of flash-rate laws); the first clause of P6's third sentence
(constructed worlds as tests of the tools used for natural ones); and P6's fourth (the bound).

Four lines that the body develops stay ungathered:

- The defects' arithmetic bias on natural exoplanets, +0.23 in convective cover for a synchronous run of
  TRAPPIST-1e and +0.31 for Proxima Centauri b (reach:20–24), is the most direct consequence of the work for
  other worlds, and the conclusion omits it.
- verification:39–41 makes gravity the property of a sea that stays fixed in a laboratory on Earth, and records
  that the wind-tunnel tests for SWAN's runs on ancient Mars varied the air's density; that passage joins P4's
  laboratory line to P5's similarity line.
- P3 ranks the changes by the global mean, and P2 has just shown errors that the global mean misses; the
  relation between the two paragraphs stays unwritten.
- The constructed-world half of the classes, what a designer can vary with the repairs as they stand and what
  needs refitting (reach:47–49, 60–62), is absent.

**Why it matters.** The author rejected the previous version as a summary of what was done. The present version
reminds well and discusses in places, and its frame is still the results read a second time.

**Rewrite.** Appendix A gives a model section of six paragraphs, about 1,050 words, built on the developed lines:
the defects exact at Earth's values and their bias on other worlds' runs; what the global mean of sunlight keeps
and what moves; what can be computed for each world's column and what stays a calibration; what laboratories on
Earth and resolved storms can test; gravity tested by similarity; and the bound, the design consequence and the
first test off the test world. F2 to F20 give local repairs for the present structure, and the model takes them
all in.

### F2. BLOCKING. A model limit stated as a property of low-gravity worlds

**Location.** `conclusions.tex`:41–44.

**Text.** "with 85\% of the water falling from the clouds of a box forced from the GCM evaporating before it
reached the ground, those limits help set how much rain a low-gravity world receives."

**Rule.** Claims stay within their evidence; G5, model results kept distinct from physical claims; the
author's direction that no sentence present an untested world as within the work's reach.

**Why.** The paper records the limits' effect as unmeasured: reach:37–38, "their effect at other gravities is
unmeasured, since the similarity pair failed to convect", and next:70–72, "limits scaled with the capillary
length would show how much of the evaporation the small drops cause". The sentence turns a limit inside
Morrison's scheme into a cause of the rain on every low-gravity world.

**Rewrite.** "…; with 85\% of the water falling from the clouds of a box forced from the GCM evaporating before
it reached the ground, how much of CM1's rain reaches the ground at lunar gravity depends on those limits, whose
effect there is unmeasured."

### F3. MAJOR. "The global means" and an unreported check

**Location.** `conclusions.tex`:11 and 19–20.

**Text.** "Several of these errors leave the global means nearly intact and change where sunlight and rain
fall." … "A check of the global energy balance passes with such errors in place; they show in a map of sunlight
by longitude or of rain by season."

**Rule.** Claims within evidence; report actual checks; a landing that restates its paragraph (AGENTS.md,
table of examples); G2, an implication restated after the evidence has made it.

**Why.**

- The step that set the Sun and the tilt right, with the refit of the split, also cut the global-mean rain from
  2.91 to 2.24 mm a day, by 23% (results:44–46). The evidence supports two global means, the arriving sunlight,
  kept by geometry, and the surface temperature, moved 0.6 K; "the global means" as a whole overstates it.
- No check of the global energy balance appears in `verification.tex` or elsewhere in the paper, and the
  sentence reads as a reported check.
- Its second clause restates the paragraph's first sentence after the second and third have given the map
  evidence.

**Rewrite.** First sentence: "Two of these errors keep the global mean of the arriving sunlight and move that
sunlight, and the rain, between places." Delete the last sentence, so that the paragraph ends on its evidence,
9 to 36% of the land against 0.6 K; P3's first sentence then takes up the global-mean temperature (F17).

### F4. MAJOR. P3's order

**Location.** `conclusions.tex`:22–34.

**Rule.** G1, the swap test; replay (F1).

**Why.** The second sentence restates results:86–89 nearly word for word, and abstract:16–19. The third and
fourth (the CM1–GCM gap; Yang et al.) interrupt the line from the ranking to replaceability and can move after
the sixth with no loss; the fourth's "as well" then ties cloud cover to a comparison of temperature and rain
(F14). The movement that works runs through the second, fifth and sixth sentences: the larger fit can be
replaced, and the second leads back to Earth-fitted microphysics.

**Rewrite.**

> Changes to the parts fitted to Earth's atmosphere moved the test world's global-mean surface temperature
> furthest: calibrating the radiation's Earth fits, used beyond the range they were fitted over, moved it by more
> than 20~K, and PlaSim's Earth-tuned cloud settings, pushed to the ends of their tests, by up to about 6~K, while
> the two general repairs measured singly, of a unit and of a constant, moved it by 1.6--2.5~K. The radiation's
> fits can be replaced, since a scheme built from line-by-line spectroscopy would hold on any column whose gases,
> pressures and temperatures that spectroscopy covers, on a natural world as on a constructed one. Cloud is harder
> to replace: the cloud-resolving runs to which a GCM's cloud could be fitted for a new world compute with
> Earth-fitted microphysics of their own. The gaps such a fit would close are wide: a box forced from the test
> world's GCM brought a quarter of its rain to the ground, each model computing its rain from Earth fits of its
> own, and on two tidally locked planets a global cloud-permitting model covered 27 and 41\% of the sky with
> cloud, where two GCMs whose cover follows relative humidity, stability and large-scale ascent covered 82--97\%
> \autocite{yang2023cloud}.

### F5. MAJOR. P4's first sentence governs one sentence of four

**Location.** `conclusions.tex`:36–49.

**Rule.** G1, the governing relation; the swap test.

**Why.** "Some of the Earth laws in the cloud-resolving model can be tested in laboratories on Earth" governs
the second sentence alone. The third (drop limits) concerns a dependence on gravity, which a laboratory on Earth
holds fixed (verification:39); the fourth and fifth concern flash-rate laws used in GCMs, to be tested against
resolved storms. The third and the pair after it can trade places without loss.

**Rewrite.** A first sentence that governs both tests, with the drop limits moved to the gravity paragraph (F7);
this also repairs F6 and F13.

> The Earth-fitted laws that set a model's lightning can be tested in laboratories on Earth and against storms
> resolved at another world's gravity. In two windows of an earlier electrified run, the storms separated as much
> charge under Takahashi's charging law as under Saunders and Peck's, with the opposite sign, since the two laws
> disagree on the sign that rimed ice takes in the little cloud water of those storms; a measurement of that sign
> at 4--8~m\,s$^{-1}$ in 0.02--0.2~g\,m$^{-3}$ of cloud water between $-5$ and $-16$\,\textdegree C, conditions
> laboratories reach, would decide the polarity of the lightning. Flash rates on tidally locked planets have been
> estimated with laws fitted to Earth's storms, from the cloud-top height or from the graupel and ice aloft
> \autocite{braam2022lightning,sergeev2025lightning}, and at a sixth of Earth's gravity such a law would be
> applied far from the storms it was fitted on: in six Morrison runs cloud tops reached 55--80~km, with the
> freezing levels five to six times their heights in Earth's tropics, and flashes in the main electrified run came
> at about a hundredth of Earth's average density, part of the difference possibly from its grid, so resolved
> storms at other gravities can test those laws.

### F6. MAJOR. Results of six Morrison runs placed in the electrified box

**Location.** `conclusions.tex`:46–49.

**Text.** "In the one electrified box, cloud tops reached 55--80~km, with the freezing levels five to six times
their heights in Earth's tropics, and the flashes came at about a hundredth of Earth's average density".

**Rule.** Technical meaning survives editing; G5.

**Why.** results:134–137 give the cloud tops and freezing levels for six Morrison runs, three boxes and three
rings. The flash density comes from the main electrified run, a box with the NSSL scheme (results:138–143), and
the charging-law windows of P4's second sentence came from an earlier electrified run, so "the one electrified
box" also miscounts the electrified runs. The grid's possible share in the low flash density (results:144–146)
dropped out.

**Rewrite.** "In six Morrison runs cloud tops reached 55--80~km, with the freezing levels five to six times their
heights in Earth's tropics, and flashes in the main electrified run came at about a hundredth of Earth's average
density, part of the difference possibly from its grid, so a law fitted at Earth's gravity would be applied there
far from the storms it was fitted on, and resolved storms at other gravities can test it."

### F7. MAJOR. A maxim opens P5, and P5 joins two unrelated items

**Location.** `conclusions.tex`:51–57.

**Text.** "Once a model scales correctly with gravity, its Earth-fitted laws are what remains uncertain."

**Rule.** No aphorisms or quotable lines; universal claims checked against what was examined; G1.

**Why.** The sentence draws a rule for every model from one, SWAN. The paper's own account lists more than the
fits once gravity is handled: the thin-shell, constant-gravity dynamics and the vertical grid (assumptions:51–57;
reach:75–80). The paragraph's third sentence, on curved air and Titan, belongs to neither the maxim nor the SWAN
sentence, and restates repairs:105–108.

**Rewrite.** A paragraph on gravity tested by similarity, taking the drop limits from P4 and the wind-tunnel link
from verification:39–41; the curved-air sentence moves to P3, beside the scheme from spectroscopy, as the other
quantity computed from a world's own column (Appendix A, third paragraph).

> Gravity stays fixed in a laboratory on Earth, so a model's response to it is tested numerically, by similarity.
> Patched, SWAN reproduces a sixfold gravity scaling of an Earth sea within 0.3\% in wave height, where the
> released code missed it by 5.4\%, so in a sea under another gravity, the ancient seas of Mars among them, the
> Earth values left on SWAN's path are its empirical laws of drag, wind input and breaking, applied at that sea's
> own ratio of air to water density, a ratio that wind tunnels on Earth can vary, as the tests made for SWAN's runs
> on those seas varied the air's density \autocite{banfield2015winds}. CM1's gravity-scaled microphysics remains
> untested in this way, since the pair of runs designed for it failed to convect, and the largest raindrop that
> survives its own fall scales with the capillary length, 2.46 times longer at a sixth of Earth's gravity, while
> Morrison's scheme keeps Earth's limits on drop size and breakup; with 85\% of the water falling from the clouds
> of a box forced from the GCM evaporating before it reached the ground, how much of CM1's rain reaches the ground
> at lunar gravity depends on those limits, whose effect there is unmeasured.

### F8. MAJOR. The last paragraph restates the introduction and the next steps

**Location.** `conclusions.tex`:59–69.

**Rule.** Conclusions and the arc; replay; claims within evidence; G5, evidence states.

**Why.**

- The first sentence restates introduction:25–26, "Such worlds combine Earth-like air with a gravity, a size and
  a day that no known natural world combines with it."
- The second restates introduction:15–26 and 46–52 and drops their evidence state, "By the design's own models".
  The "day" in its list comes from the Moon's own rotation, apart from any escape velocity.
- The third repeats P1's claim about the defects, now without "ExoPlaSim's", so that "bias runs of slowly
  rotating and tidally locked planets" reads as every run of such planets, and then describes how the record
  serves a reader.
- The fifth restates next:35–39, so the paper's last sentence copies its fourth next step.
- Arc (pass 10): the abstract lands on radiation physics that holds across worlds against cloud calibrated for
  each world (abstract:19–21); the conclusion lands on the slow-rotator runs.

**Rewrite.** Compact, with the evidence state and "ExoPlaSim's" restored; Appendix A's last paragraph is the
fuller alternative, with the design consequence.

> Constructed worlds can join Earth-like air to gravities, sizes and days that no known natural world combines
> with it, and on the test world, which by its design's own models keeps 1.2~atm under a sixth of Earth's gravity
> behind a shield in space, the Earth values that depend on gravity, column, day and the air's height against the
> radius erred together, while its slow rotation and small tilt made large the three defects that bias ExoPlaSim's
> runs of slowly rotating and tidally locked planets. Away from Earth's values, the general repairs have run on the
> test world alone, though they were built to hold on other worlds. Released and repaired ExoPlaSim on Earth-air
> planets rotating once in 16 and 64 days, two of the periods at which ROCKE-3D has simulated such planets
> \autocite{way2018climates}, would measure how far the three defects move ExoPlaSim's climate of a world that
> other studies model, and would be the general repairs' first test there.

### F9. MAJOR. The reach heading fits all three groups

**Location.** `reach.tex`:47.

**Text.** "Worlds that need the repairs as they stand."

**Rule.** Say what is; nouns precise; technical meaning.

**Why.**

- The worlds under the next two headings need the repairs as well: Mars held at 1 bar "needs the general repairs"
  (reach:64–65), and for Titan, present Mars and Venus "the general repairs of units, clocks and gravity would
  apply to them unchanged" (reach:73–74). What sets the first group apart is that nothing in it needs refitting.
- For the slow rotators the paragraph prescribes "ExoPlaSim's general repairs alone" with the released radiation
  (reach:52–53). "The repairs as they stand" include the lunar calibrations, which those planets would set aside.
- The heading repeats "as they stand" in the paragraph's first words.

**What works.** The change from "Worlds the repaired models simulate as they stand" removed the claim that the
models simulate worlds yet to be run.

**Rewrite.** "Worlds that need no refitting." The negation defines the group against the next heading, "Worlds
that need refitted calibrations", and the proposition requires it. A positive alternative, naming the condition
that the paragraph states: "Worlds near the existing fits."

### F10. MAJOR. The expectation for slow rotators sets cloud aside

**Location.** `reach.tex`:50–53.

**Text.** "ExoPlaSim's general repairs alone should suffice, since the released radiation was fitted on columns
and a spectrum like theirs; the runs have yet to be made."

**Rule.** Claims within evidence; the author's direction on untested worlds.

**Why.** The reason given covers the radiation alone. On those planets PlaSim's cloud keeps Slingo's fit to
Earth's convection and its Earth-tuned thresholds, and the paper's own table puts "Slingo's fit itself" beyond
the adapted models for a solar day other than Earth's (reach:95). The cited studies trace much of their change
with rotation to cloud: Yang et al. (2014), "the cloud albedo is much higher on slowly [rotating planets]"
(manifest locator, arXiv v1 p. 4), and Way et al. (2018), cloud forcing and water vapour by rotation period
(their Figure 11).

**Rewrite.** "For slowly rotating planets with Earth's gravity and air around a Sun-like star, such as those that
\textcite{yang2014strong} and \textcite{way2018climates} simulated with CAM3 and ROCKE-3D, ExoPlaSim needs its
general repairs and its released radiation, which was fitted on columns and a spectrum like theirs, while its
cloud keeps Slingo's fit to Earth's convection and PlaSim's Earth-tuned thresholds, and cloud is among the
processes through which those studies found the climate to change with rotation; the runs have yet to be made."

### F11. MINOR. "Several"

**Location.** `conclusions.tex`:11. **Text.** "Several of these errors". **Why.** Two of the three, the Sun clock and
the orbit default; the convective-cover unit moved the global mean by 1.6–1.8 K. **Rewrite.** "Two of these
errors", with the rest of the sentence as in F3.

### F12. MINOR. A deduction found only in the conclusion

**Location.** `conclusions.tex`:11–13. **Text.** "keeps every zonal and global mean of sunlight exact, since the
share of a latitude circle in sunlight depends on the Sun's declination alone". **Why.** The deduction appears
nowhere else in the paper, and the lit share sets only the lit fraction; a circle's mean sunlight also takes the
mean cosine over the lit arc and the Sun's distance. **Rewrite.** "ExoPlaSim's Sun clock shifts the Sun in
longitude alone, and a latitude circle's mean sunlight depends on the Sun's declination and distance, so the
clock keeps every zonal and global mean of sunlight and moves the sunlight between longitudes: …". If the claim
stays, assumptions:100–107 is the place to state it once; the author should confirm the reasoning, which this
record proposes.

### F13. MINOR. Which electrified run

**Location.** `conclusions.tex`:36–37. **Text.** "In two windows of the test world's electrified run". **Why.**
results:151–153 place the windows in "an earlier electrified run, … made before the ventilation repair and with
leakage off"; the definite article points at the main run. **Rewrite.** "In two windows of an earlier electrified
run, made before the ventilation repair, …".

### F14. MINOR. "As well" across two quantities

**Location.** `conclusions.tex`:28. **Text.** "Models of natural planets differ widely in cloud as well". **Why.**
"As well" ties cloud cover to the previous sentence's comparison of near-ground temperature and rain.
**Rewrite.** If P3 keeps its order: "On natural planets GCMs and cloud-permitting models part widely in cloud:
…". In the rebuilt P3 (F4) the comparison follows the cloud sentence directly.

### F15. MINOR. "Earth fits of its own"

**Location.** `conclusions.tex`:26. **Text.** "The two atmospheric models disagree where each computes with Earth
fits of its own". **Why.** results:98–113 attribute about 1.5 K of the 3.7 K to radiative over-cooling and the
rest, by elimination, to the upward transport of the ground's heat, with the GCM's two layers in its lowest
6.5 km, which come from Earth's σ levels, a value of geometry. **Rewrite.** "… where each computes with Earth
values of its own: …", or confine the clause to rain, which results:118–119 attribute to each model's own Earth
fits.

### F16. MINOR. "Outright", and the spectroscopy's bound

**Location.** `conclusions.tex`:30–32. **Text.** "The radiation's fits can be replaced outright, since a scheme
built from line-by-line spectroscopy would hold on any column whose gases and pressures that spectroscopy
covers". **Why.** "Outright" overstates a scheme yet to be built, and the bound leaves out temperature, over
which line strengths and the MT_CKD continuum hold their own validated range; the reference's emulation is
checked at 288–330 K (repairs:123–125). **Rewrite.** "The radiation's fits can be replaced, since a scheme built
from line-by-line spectroscopy would hold on any column whose gases, pressures and temperatures that
spectroscopy covers, on a natural world as on a constructed one." The author should confirm the temperature
bound; the same bound stands in abstract:19–21 and next:14–16.

### F17. MINOR. "By size"

**Location.** `conclusions.tex`:22. **Text.** "By size, changes to the parts fitted to Earth's atmosphere moved the
test world furthest." **Why.** "By size" leaves the measure unnamed, and the quantity moved is a temperature.
**Rewrite.** "Changes to the parts fitted to Earth's atmosphere moved the test world's global-mean surface
temperature furthest: …", which also takes up P2's last figure, 0.6 K in the same quantity.

### F18. MINOR. Runs as the calibrating agent

**Location.** `conclusions.tex`:33. **Text.** "the cloud-resolving runs that could calibrate a GCM's cloud for a
new world". **Why.** A modeller fits the GCM to the runs. **Rewrite.** "the cloud-resolving runs to which a GCM's
cloud could be fitted for a new world compute with Earth-fitted microphysics of their own".

### F19. MINOR. SWAN's verb and "the open questions"

**Location.** `conclusions.tex`:51–54. **Text.** "Patched, SWAN scales an Earth sea sixfold in gravity … where the
released code missed by 5.4\%, so … the open questions are Earth's empirical laws for drag, wind input and
breaking". **Why.** The test scaled the sea, and SWAN reproduced the scaling; "missed" lacks its object; "the
open questions are" claims a complete list, where next:89–91 adds the air's density as a field, a wider band for
small seas and swell decay. The inventory table (assumptions:202–206) supports the narrower claim. **Rewrite.**
"Patched, SWAN reproduces a sixfold gravity scaling of an Earth sea within 0.3\% in wave height, where the
released code missed it by 5.4\%, so in a sea under another gravity, the ancient seas of Mars among them, the
Earth values left on SWAN's path are its empirical laws for drag, wind input and breaking, applied at that sea's
ratio of air to water density."

### F20. MINOR. "The periods" of the ROCKE-3D runs

**Location.** `conclusions.tex`:66–67. **Text.** "the periods at which ROCKE-3D has simulated such planets".
**Why.** Way et al. (2018) ran sidereal periods of 1, 2, 4, 8, 16, 32, 64, 128 and 256 days (archived original,
Figure 1 and the tables beside it); 16 and 64 days are two of them. **Rewrite.** "two of the periods at which
ROCKE-3D has simulated such planets".

### Outside the scope, uncounted

- `reach.tex`:43–45: "Of the found worlds in Figure~\ref{fig:regimes}, Earth alone lies within the adapted
  models' reach; the other worlds within it are constructed worlds and exoplanets whose air is taken to be close
  to Earth's." With reach defined at reach:3 as "the set of worlds on which its repaired code holds", the sentence
  places untested classes of worlds within reach, while the table caption (reach:85) records that, apart from the
  Earth benchmarks, every run so far is of the test world. It stands directly before the heading in scope and
  meets the author's objection to presenting untested worlds as within reach.
- `next.tex`:37: "the sidereal periods of the ROCKE-3D runs of \textcite{way2018climates}" carries the
  exclusivity of F20.

## 3. What works

- **P2's first and third sentences (11, 16–19).** The governing relation, errors that keep a global quantity and
  move its distribution, matters to anyone modelling a slow rotator, and "while" writes the evidentiary contrast
  into the syntax: 9 to 36% of nearly rainless land against 0.6 K.
- **P3's last two sentences (30–34)** hold the section's strongest discussion: the larger fit can give way to
  physics computed for each world, and cloud stays a calibration whose own source runs on Earth-fitted
  microphysics. "Cloud is harder to replace" is an earned hinge, and P4 opens on the term P3 closes on, a
  transition grown from the subject.
- **P4's second sentence (36–40)** names an experiment, its conditions and what it would decide, in the
  conditional; it excites within the evidence.
- **The Titan clause (56–57)** carries a cited result for a natural world, stated implicitly, as the author asked.
- **P6's fourth sentence (65–66),** "The general repairs were built to hold off the test world and have run on it
  alone.", is a short hinge that states the evidence state positively and keeps every untested world outside the
  claim; P6's last sentence keeps unrun work in the conditional.
- **Across the section:** no "not" or "rather than", no stock transitions, no promotional words, no rhetorical
  questions, one self-reference ("found here"), and qualifications attached once to the claims they bound.
- **reach.tex:47–56:** the heading now states a need and claims no simulation, and the paragraph marks its
  evidence states once and positively ("the runs have yet to be made"; "is unchecked").

## 4. Counts and overall judgement

| Severity | Count | Findings |
|---|---|---|
| BLOCKING | 2 | F1, F2 |
| MAJOR | 8 | F3–F10 |
| MINOR | 10 | F11–F20 |

Two further observations lie outside the scope and are uncounted.

The section has moved from summary toward discussion. About six sentences now develop relations that matter
beyond the test world: errors that keep a global quantity and move its distribution, radiation that physics could
replace against cloud that stays a calibration, laws that laboratories on Earth or resolved storms can test, and
constructed worlds as tests of the tools used for natural ones; and the last paragraph keeps every untested world
outside its claim. The section still falls short of the author's direction. It reads the results a second time in
their order, with some forty figures at their original precision; P1 and P6 restate the abstract, the
introduction and the next steps, so that the paper ends on a copy of its fourth next step; the consequence for
natural exoplanets that the body computes, the defects' bias on TRAPPIST-1e and Proxima Centauri b, is missing;
and five passages claim more than the body supports (F2, F3, F6, F7, F8). F2 presents an unmeasured model effect
as a property of every low-gravity world, the kind of extension the author rejected. The reach heading now claims
no simulation, but its wording fits all three groups and prescribes the lunar calibrations for planets that need
the released radiation, and the paragraph's expectation for slow rotators sets aside the cloud to which the cited
studies trace much of their change with rotation. A section rebuilt on the lines of Appendix A, or the local
repairs F2 to F20 within the present frame, followed by a fresh reading, would show whether the direction is met.

## Appendix A. Model rewrite for F1

A proposal for the author, in the paper's voice; it carries the local repairs of F2 to F20.

```latex
\section{Discussion and conclusions}

Three of the five defects found in the released codes produce little or no error at Earth's values and an error
that grows as a world departs from Earth's rotation, day or tilt, and the test world's slow rotation and small
tilt made all three large. By the code's own arithmetic they bias ExoPlaSim's runs of other worlds as well: the
convective-cover unit, which read the test world's rain as about thirty times heavier than it is, adds about 0.23
to the convective cover of a synchronous run of TRAPPIST-1e and 0.31 to that of Proxima Centauri~b, and the Sun
clock sets the Sun back about 33\textdegree\ each model day in any non-synchronous run, on ExoPlaSim's default
solar geometry, of a planet rotating more slowly than once in 20 days.

Two of the three keep the global mean of the arriving sunlight and move that sunlight, and the rain, between
places. The Sun clock shifts the Sun in longitude alone, and a latitude circle's mean sunlight depends on the
Sun's declination and distance, so the skip kept every zonal mean of sunlight while it left the test world's
equator, by longitude, between 8.3\% short of its mean and 17\% over it; the orbit default's Earth tilt, put in
place of the configured one, brought Earth's seasons and summer rain to 60\textdegree. With the Sun and the tilt
set right, 36\% of the land received under half a millimetre of rain a day within two years, against 9\% before,
while the step in which both were corrected, with a refit of the split of sunlight, moved the global-mean surface
temperature by 0.6~K.

Changes to the parts fitted to Earth's atmosphere moved that temperature furthest: calibrating the radiation's
Earth fits, used beyond the range they were fitted over, moved it by more than 20~K, and PlaSim's Earth-tuned
cloud settings, pushed to the ends of their tests, by up to about 6~K, while the two general repairs measured
singly, of a unit and of a constant, moved it by 1.6--2.5~K. The radiation, like the geometry of tall air, can be
computed from a world's own column. The curved-air table already is, recomputed for each world, and Titan, whose
air is a quarter as tall against its radius as the test world's, needs one beyond about 65\textdegree\ from the
zenith, where a flat treatment fails \autocite{vincendon2010spherical}; a scheme built from line-by-line
spectroscopy would replace the radiation's fits in the same way, holding on any column whose gases, pressures and
temperatures that spectroscopy covers, on a natural world as on a constructed one. Cloud would remain a
calibration for each world, fitted to cloud-resolving runs that compute with Earth-fitted microphysics of their
own, and the gaps such a fit would close are wide: on two tidally locked planets a global cloud-permitting model
covered 27 and 41\% of the sky with cloud, where two GCMs whose cover follows relative humidity, stability and
large-scale ascent covered 82--97\% \autocite{yang2023cloud}, and on the test world a box forced from the GCM
brought a quarter of the GCM's rain to the ground, each model computing its rain from Earth fits of its own.

The Earth-fitted laws that set a model's lightning can be tested in laboratories on Earth and against storms
resolved at another world's gravity. In two windows of an earlier electrified run, the test world's storms
separated as much charge under Takahashi's charging law as under Saunders and Peck's, with the opposite sign,
since the two laws disagree on the sign that rimed ice takes in the little cloud water of those storms; a
measurement of that sign at 4--8~m\,s$^{-1}$ in 0.02--0.2~g\,m$^{-3}$ of cloud water between $-5$ and
$-16$\,\textdegree C, conditions laboratories reach, would decide the polarity of the lightning. Flash rates on
tidally locked planets have been estimated with laws fitted to Earth's storms, from the cloud-top height or from
the graupel and ice aloft \autocite{braam2022lightning,sergeev2025lightning}, and at a sixth of Earth's gravity
such a law would be applied far from the storms it was fitted on: in six Morrison runs cloud tops reached
55--80~km, with the freezing levels five to six times their heights in Earth's tropics, and flashes in the main
electrified run came at about a hundredth of Earth's average density, part of the difference possibly from its
grid, so resolved storms at other gravities can test those laws.

Gravity stays fixed in a laboratory on Earth, so a model's response to it is tested numerically, by similarity.
Patched, SWAN reproduces a sixfold gravity scaling of an Earth sea within 0.3\% in wave height, where the
released code missed it by 5.4\%. The Earth values left on SWAN's path through a sea at another gravity, the
ancient seas of Mars among them, are its empirical laws of drag, wind input and breaking, applied at that sea's
own ratio of air to water density, a ratio that wind tunnels on Earth can vary, as the tests made for SWAN's runs
on those seas varied the air's density \autocite{banfield2015winds}. CM1's gravity-scaled microphysics remains
untested in this way, since the pair of runs designed for it failed to convect, and Morrison's scheme keeps
Earth's limits on the size and breakup of rain, where the largest drop that survives its fall scales with the
capillary length, 2.46 times longer at a sixth of Earth's gravity; with 85\% of the water falling from the clouds
of a box forced from the GCM evaporating before it reached the ground, how much of CM1's rain reaches the ground
at lunar gravity depends on those limits, whose effect there is unmeasured.

Away from Earth's values, every change made for the test world has run on it alone, the general repairs among
them, though they were built to hold on other worlds. A modeller of the test world can vary its dimming with the
repairs as they stand while its columns stay near those fitted, and needs the calibrations refitted for a lower
pressure or another shield, as for any change in a constructed world's design that moves its columns away from
the fitted ones. Released and repaired ExoPlaSim on Earth-air planets rotating once in 16 and 64 days, two of the
periods at which ROCKE-3D has simulated such planets \autocite{way2018climates}, would measure how far the three
defects move ExoPlaSim's climate of a world that other studies model, and would be the general repairs' first
test on a world beyond the one they were made on.
```

**Checks made on the model.**

- Each sentence traced to the body: assumptions:98–118 and reach:17–24 (first paragraph); assumptions:100–107,
  117 and results:44–48 (second); results:36–44, 86–89, 115–119, worlds:77, repairs:105–108, next:14–16 and
  results:78–82 (third); results:134–156 and next:77–82 (fourth); verification:39–44, 51–52, assumptions:24–26,
  85–88, reach:37–38 and results:116–117 (fifth); next:35–39, reach:47–49, 60–62, introduction:76–78 and Way et
  al. (2018) (sixth).
- `lint.py`, as screening: no "not" or "rather than"; one negation, "little or no error", required by its
  proposition; the other hits read and kept.
- Size: about 1,060 words and 39 numerals, against about 1,100 and 43; the figures kept carry a size, a contrast
  or an experiment's conditions.
- Three points for the author to confirm: the zonal-mean deduction (F12); the temperature bound (F16); and "keep
  the global mean of the arriving sunlight" for the orbit default, which rests on a tilt leaving the global-mean
  insolation unchanged at a given orbit.
- Cadence: silent reading only.
