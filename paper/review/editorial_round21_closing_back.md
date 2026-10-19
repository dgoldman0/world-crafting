# Editorial round 21, closing review: the back half, for its verbs

- **Snapshot.** Commit `a50e0b1` (`a50e0b177d089b6ccb232eafbf94cd157ae4a4af`), branch `paper/conclusion-development`.
  HEAD was that commit and `git status --short` printed nothing, at the start of the reading and again before this
  record was written. The PDF built from these sources, `paper/build/main.pdf`, has SHA256
  `f6ff147f7fb291d4acf5e80c24185bf8a006a7be3d64bc17c179b7507888623f`, as round 20 recorded. As directed, I ran
  neither make nor LaTeX; line numbers below are the snapshot's source lines.
- **Reviewer.** A fresh Claude Opus 5.5 subagent, reading the back half for its verbs, at the close of round 21.
  Another fresh reviewer read the front half at the same time. This record is the only file I wrote.
- **Date.** 19 October 2026.
- **Read.** `AGENTS.md` in full; the four Terluna sources behind its writing rules (`STYLE_NOTES.md`,
  `Jewish_Papers_Updated_Style_Notes.md`, `Agent_Working_State_Editorial_Gates.md`,
  `Open_Moon_Editorial_Charter_control-01.md`); the drafting assistant's notes of the author's directions
  (writing-style-rules, author-direction-overrides-rules, paper-standalone-field-framing, abstract-attracts-reader,
  conclusion-as-discussion, credit-prior-work, standalone-paper-no-process-logs); `editorial_round18_closing_prose.md`,
  `editorial_round19.md` and `editorial_round20.md`; the whole paper in the order `main.tex` inputs it; and
  `git diff ffdedfe a50e0b1 -- paper/main.tex paper/sections`. For the fixes: every entry of `paper/claims.json`;
  `notes/verification_record.md`, `cm1.md`, `exoplasim.md`, `waves.md` and `electrification.md` in full;
  `notes/defect_log.md` sections A, B and C1–C14; `notes/reference_radiation.md` lines 1–40, 260–350 and 440–480; the
  READMEs of `models/cm1`, `models/exoplasim` and `models/swan`; in Terluna at 186b294, `climate/crm/README.md`
  2138–2172 and 2385–2392, `climate/waves/README.md` 10–50 and `climate/gcm/README.md` 1119–1136; and the source
  record of `yang2023cloud` in `paper/sources/manifest.json`.
- **Verb pass.** `verification.tex`, `results.tex`, `reach.tex`, `next.tex`, `conclusions.tex`, `appendix.tex` and
  `availability.tex`, every sentence, with captions, table cells and table notes; these files have no footnotes.
- **Cadence.** Read silently, with no read-aloud review.

## Judgment

The author's remaining criticism of the paper was its "verbs that don't really work well", with two examples in
Assumptions, "Earth's day enters..." and "Earth's day in its Sun and its soil". The back half has the same habit
throughout. In 87 places an abstraction is made to do what only a code, a run, a person or the air does: a value
enters, a gap closes, a defect bears on a comparison, a spectrum brings a difference, a sign decides between laws,
a world needs repairs. In a few places a verb names an operation different from the one the records name. The most
frequent verbs are the ones the author's examples use or resemble: "enter" (three places), "lie" and "lie in"
(nine), "keep", "hold", "take", "bring", "decide" and "need". For each, the claims register, the notes or the code
names the operation, so most fixes change one verb or move the subject to the agent that acts. One fix also
corrects a claim. Next steps says hail "carried" most of the charge, while the records count the charging that hail
did (V59).

In two passages the figures form a pattern. Reach to other worlds uses "need" as its working verb, with worlds and
schemes as subjects in six sentences and two headings (V42). In the Conclusion, abstractions act: a development
joins an ability to a reference, a choice sharpens a use, designs deliver water and drive winds. Its 19 findings are
for the author. In its closing vision the verbs are physical: rain arriving in a basin, swell along a coast, a storm
passing over a lake.

Beyond the verbs, nothing in the back half is BLOCKING or MAJOR. The text changed in rounds 19 and 20 has two MINOR
problems, both in Next steps: its overview omits two of the section's steps, and one clause is compressed (F1, F2).

**Counts.** 87 verb findings: 47 clear (a listed figure verb on an abstraction, or a verb naming the wrong
operation) and 40 mild (a dead metaphor or generic verb whose meaning is plain, where an exact verb is at hand).
19 of them, V69–V87, are in the Conclusion and go to the author. Other findings: 0 BLOCKING, 0 MAJOR, 2 MINOR.

## Verb findings

Each finding gives the clause with its verb in bold, what happens by the records, and the replacement as it would
stand in the file.

### verification.tex

**V1** · `verification.tex`:7–9 · clear
*As it stands.* "a similarity check comparing in dimensionless form a run at scaled gravity, lengths and times with
the original, to test whether gravity **enters** the code consistently."
*What happens.* A scaled run reproduces the Earth run in dimensionless form only if every gravity-dependent term in
the code scales with the gravity it is given. With SWAN's 1 Hz knee, an Earth constant, the scaled run differed by
5.44%, and with the knee scaled, by 0.303% (V04; `models/swan/README.md`; `notes/waves.md`:62–63).
*Fix.*
> In the second, arithmetic and similarity checks test the code against a formula, a direct solution or itself, a
> similarity check comparing in dimensionless form a run at scaled gravity, lengths and times with the original, to
> test whether every term in the code that depends on gravity scales with the gravity the code is given.

**V2** · `verification.tex`:11–13 · mild
*As it stands.* "although a similarity test **runs** Earth's empirical laws at the scaled gravity with their Earth
coefficients, which it leaves untested there."
*What happens.* The scaled run of the test computes with Earth's fitted coefficients (verification record,
Similarity: the check leaves open "that the empirical laws hold at lunar gravity").
*Fix.*
> The checks of the first two steps concern properties of the code that hold on any world, although in a
> similarity test the scaled run applies Earth's empirical laws at the scaled gravity with their Earth coefficients,
> which the test leaves untested there.

**V3** · `verification.tex`:20–21 and 24; `appendix.tex`:130 · mild
*As it stands.* "The first three **link back** to the released model in sequence"; "so the chain from these two
checks to the released model **closes** once they are"; in Table 7, "the chain to the release **closes** for patches
01--03".
*What happens.* The patch-01 run was compared with the unpatched build, the patch-02 run with run A's build (patch 01
alone) and the patch-03 run with the build holding patches 01–02. The infrared and ice-optics runs were compared
with builds holding patches 04, 05 and 07–09, whose off settings have yet to be run (verification record, section 1;
V01).
*Fix.*
> The first three were run in sequence from the released model, each against a build that holds only the patches
> checked before it.

> ... those patches were written to reproduce the released code at their off settings and have yet to be run that
> way, so these two checks establish identity with the released model only once they are, while for the water
> scaling at its default the identity already follows from arithmetic on this spectrum.\claim{V01}

> Restart identical to the build before the patch; identity with the release established for patches 01--03

**V4** · `verification.tex`:34–36 · mild
*As it stands.* "a GCM year killed a minute in and resumed **repeats** the uninterrupted year's restart and every
variable of its output"
*What happens.* The run `A_kill`, killed a minute into a model year and resumed, wrote the same restart as the
uninterrupted `A_ref` and the same values in all 39 output variables (verification record, section 1).
*Fix.*
> In the last kind of check the runs themselves are restarted or repeated: a GCM run killed a minute into a model
> year and resumed writes the same restart and the same values in every output variable as the uninterrupted run,
> runs of CM1 repeat bit for bit on one thread, and the Earth supercell, restarted on four threads and on two,
> repeats its fields and its 41 flashes.

**V5** · `verification.tex`:45–48 · mild
*As it stands.* "differs from the Earth run it **scales** by 5.44\% in significant wave height"
*What happens.* The lunar-gravity run was made from the Earth run by scaling its gravity, lengths, depths, durations
and frequencies (V04; `models/swan/README.md`, Verification).
*Fix.*
> Stock SWAN, run at a sixth of Earth's gravity with lengths, depths and durations six times longer and frequencies
> six times lower, differs from the Earth run from which it was scaled by 5.44\% in significant wave height and
> 3.91\% in mean period; patched, it differs by 0.303\% and 0.326\%, against a 1\% criterion.\claim{V04}

**V6** · `verification.tex`:61–64 · clear
*As it stands.* "and a 303~K column carrying 338~kg\,m$^{-2}$ of vapour, warmer and wetter than any fitted, **fell**
0.7 points short"
*What happens.* On that column the calibrated scheme's share of sunlight absorbed in the air was 0.7 points below the
reference's. The column is the case; the calibration is what fell short (V07; `notes/exoplasim.md`:209–211).
*Fix.*
> on eleven columns outside the fit's set it held within 0.6 percentage points rms, and on a 303~K column carrying
> 338~kg\,m$^{-2}$ of vapour, warmer and wetter than any fitted, it fell 0.7 points short, where the scheme before
> its water recalibration fell 9.7 short.\claim{V07}

**V7** · `verification.tex`:74–76 · clear
*As it stands.* "RRTMG, checked against the same reference and left uncalibrated, **lies** within 2.5 points of the
line-by-line shares of reflected, air-absorbed and ground-absorbed sunlight"
*What happens.* RRTMG computes the three shares on its clear column at the crossing within 2.5 points of the
line-by-line model's (V08; `notes/cm1.md`:42–44).
*Fix.*
> RRTMG, checked against the same reference and left uncalibrated, computes shares of reflected, air-absorbed and
> ground-absorbed sunlight within 2.5 points of the line-by-line model's at the site where the rings cross the
> equator at 0\textdegree~E, and on 990 cloud-free columns of the 45\textdegree\,N ring it cools the air ...

**V8** · `verification.tex`:85–86 and 112–113 · mild
*As it stands.* "its median charge per flash **falls** inside the range of \textcite{macgorman2001lightning}"; "so
their 0.013--0.021~K difference **falls** below what the pair resolves".
*What happens.* The median, 9.4 C, is within the published 2.7–39.6 C (`notes/electrification.md`:47–49); the
twilight pair's difference is smaller than the spread between builds (`notes/cm1.md`:16–22; defect log C8).
*Fix.*
> its median charge per flash is inside the range of \textcite{macgorman2001lightning}

> so their 0.013--0.021~K difference is below what the pair resolves.\claim{H31}

**V9** · `verification.tex`:89–92 · mild
*As it stands.* "the conductivity column through which the code leaks charge **comes from** an ion chain"
*What happens.* `conductivity.py` computes the column from ion production, recombination, mobility and attachment
(`notes/electrification.md`:105–110; V11).
*Fix.*
> The leakage added for the lunar runs has an Earth benchmark of its own: the conductivity column through which the
> code leaks charge is computed by an ion chain that, run for Earth at a geomagnetic cutoff rigidity of 3~GV,
> reproduces Earth's measured fair-weather positive conductivity \autocite{nicoll2012measurements} within 2--8\% from
> 5 to 30~km.\claim{V11}

**V10** · `verification.tex`:95–97 · clear
*As it stands.* "the GCM runner's first solar spectrum, whose tail **held** its last value past 2.73~\textmu m,
**put** 86\% of the sunlight in the near infrared and **warmed** the first run past 320~K;"
*What happens.* The runner extended the TSIS-1 spectrum past its 2.73 µm end at its last value; 86% of that
spectrum's energy was above 0.75 µm, in PlaSim's near-infrared band, and the first run on it warmed past 320 K
(defect log C1; H28).
*Fix.*
> Six were removed before the runs reported here: the GCM runner's first solar spectrum, extended past
> 2.73~\textmu m at its last value, had 86\% of its energy in the near infrared, and the first run on it warmed past
> 320~K;\claim{H28} the first electrified build ...

**V11** · `verification.tex`:101–104; `results.tex`:28 · mild
*As it stands.* "The first channels of the curved-air table, bisected on the whole column alone, **put**
near-infrared sunlight too high"; in Table 3, "Curved-air terms on the table's first channels, which **put**
near-infrared sunlight too high".
*What happens.* With the Sun overhead, those channels absorbed 19.0 W m⁻² at 66–85 km, where the fine grid absorbs
10.7 (defect log C3; H30).
*Fix.*
> The first channels of the curved-air table, bisected on the whole column alone, absorbed near-infrared sunlight
> too high, 19.0 against 10.7~W\,m$^{-2}$ at 66--85~km, and the curved-air and gas-band runs of
> Table~\ref{tab:states} ran on them.\claim{H30}

> Curved-air terms on the table's first channels, which absorbed near-infrared sunlight too high

**V12** · `verification.tex`:104–106 · clear
*As it stands.* "started from soundings that **held** the vapour of the GCM's top level, near 130~km, constant above
it"
*What happens.* CM1's set-up kept the top level's vapour unchanged above 130 km while the temperature fell (defect log
C4).
*Fix.*
> Every CM1 case set up before 2026-10-17, and so every CM1 run reported here, started from soundings with the
> vapour of the GCM's top level, near 130~km, held constant above it, and on the 45\textdegree\,N rings, ...

**V13** · `verification.tex`:107–108 · clear
*As it stands.* "The other two **bear on** single comparisons."
*What happens.* The ventilation omission affected the windows that compare the charging laws, and the mixed builds
affected the twilight pair (H29; H31).
*Fix.*
> The other two affect single comparisons.

**V14** · `verification.tex`:108–111 · clear
*As it stands.* "after the windows of the storm results that **compare** charging laws had run"
*What happens.* The author compared the charging laws across those windows. They ran before 2026-10-06, when a code
review found the omission (defect log C12).
*Fix.*
> ... and a code review found the omission after the windows used in the storm results to compare the charging laws
> had run, though before the main electrified run began.\claim{H29}

**V15** · `verification.tex`:116–119 · clear
*As it stands.* "so the step's error **lies in** the sea states below 1~m."
*What happens.* In the weather week, halving the step changed seas of 1 m and more by 0.446% and 1.760%, and small
seas by 12.95% and 26.73% (`notes/waves.md`, convergence table; V12).
*Fix.*
> ... and in the weather runs small seas fail their 5\% time-step criterion where seas above 1~m pass, so the step's
> error is large only in the sea states below 1~m.

### results.tex

**V16** · `results.tex`:36 · mild
*As it stands.* "**Fitting** the first calibration **cooled** the climate more than any later change."
*What happens.* The fitting was done offline on global-mean columns; the calibrated run A then settled at 295.5 K, at
least 20 K below the uncalibrated run (R09; G14).
*Fix.*
> The first calibration cooled the climate more than any later change.

**V17** · `results.tex`:44–45 · clear
*As it stands.* "From the Earth-orbit state, which **holds** both cloud repairs,"
*What happens.* The Earth-orbit run was made with both cloud repairs switched on (Table 3).
*Fix.*
> From the Earth-orbit state, run with both cloud repairs, four changes were made in one step:

**V18** · `results.tex`:57 · mild
*As it stands.* "computed cloud-free, the column's ground **moves** 0.57~K with the bands"
*What happens.* The cloud-free column's ground temperature changes by 0.57 K (G03; Terluna `climate/gcm/README.md`
1121–1123). The ground itself stays put, and "moves" first reads as motion.
*Fix.*
> computed cloud-free, the column's ground temperature changes by 0.57~K with the bands, while the high deck fell ...

**V19** · `results.tex`:59–61 · clear
*As it stands.* "The corrected terms **have run** only together with the bands and the eased dimming, in the design
case: holding the design temperature on them **took** easing the dimming from 5.0 to 3.0\%"
*What happens.* The GCM was run with the corrected terms only in the design case, and the author chose the sunlight
scale 0.970 to hold 295 K (G04).
*Fix.*
> The corrected terms have been run only together with the bands and the eased dimming, in the design case: to hold
> the design temperature on them, the dimming was eased from 5.0 to 3.0\%, and at that dimming the design case
> settles at 295.0~K, with 2.31~mm of rain a day.\claim{G04}

**V20** · `results.tex`:73–74 (Figure 5 caption) · mild
*As it stands.* "and the longwave test **extrapolates** to balance at 306.8--307.1~K."
*What happens.* The run ends at 306.77 K in year 19, warming 0.08 K a year; extrapolated, its warming ends at a
balance of 306.8–307.1 K (G13).
*Fix.*
> several runs were still drifting, and the longwave test, extrapolated to balance, would settle at
> 306.8--307.1~K.\claim{G13}

**V21** · `results.tex`:83–84 · mild
*As it stands.* "the largest effects on the test world **came from** the fits"
*What happens.* The changes to the fits moved the global mean most, by at least 20 K and up to about 6 K (G14; G05).
*Fix.*
> Ranked by form, then, the largest effects on the test world were those of the fits:

**V22** · `results.tex`:87–88 · mild
*As it stands.* "A **test** of the cooling by height **moves** the global mean more than any cloud setting:"
*What happens.* The change switched on in the test, the longwave correction with the ice optics, warmed the design
case by 11.5 K (G05).
*Fix.*
> A change to the cooling by height moves the global mean more than any cloud setting:

**V23** · `results.tex`:101 · clear
*As it stands.* "Among whole GCMs the spread widens as water and cloud **enter**:"
*What happens.* THAI's four GCMs spread by 7 and 6 K in the dry cases and by 14 and 24 K in the moist cases, which
include water and cloud (turbet2022thai; sergeev2022thai).
*Fix.*
> Among whole GCMs the spread widens when the cases include water and cloud:

**V24** · `results.tex`:107–109 · mild
*As it stands.* "CAM3 **covered** 94.8 and 81.7\% of the sky and ExoCAM 90.4 and 97.4\%, their cover **following**
relative humidity, stability and large-scale ascent"
*What happens.* The models' cloud covered the sky. Yang et al. write that in CAM3 and ExoCAM "cloud coverages are
empirically parameterized based on relative humidity, atmospheric stratification, and large-scale updrafts" (arXiv v1
pp. 3–4; source record in `paper/sources/manifest.json`).
*Fix.*
> CAM3's cloud covered 94.8 and 81.7\% of the sky and ExoCAM's 90.4 and 97.4\%, their cover computed from relative
> humidity, stability and large-scale ascent, against 26.9 and 41.1\% in a quasi-global cloud-permitting model, ...

**V25** · `results.tex`:111 · clear
*As it stands.* "The planetary albedos **lay** closer, however,"
*What happens.* The models' albedos were closer to one another than their cover was (yang2023cloud, as the sentence
reports).
*Fix.*
> The planetary albedos were closer, however, 22.1--29.1 and 39.0--47.0\% in the GCMs against 18.1 and 37.4\%, ...

**V26** · `results.tex`:123–124 · clear
*As it stands.* "from the ice that the ring's starting sounding **left** above 107~km"
*What happens.* The sounding held vapour 6–15 times saturated over ice at 140–150 km. Ice formed within three days and
stayed above 107 km through both lunar days (defect log C4).
*Fix.*
> The second radiative term, from the ice that formed above 107~km out of the ring's starting sounding, remains
> unquantified.

**V27** · `results.tex`:124–129 · clear
*As it stands.* "in boxes forced from the Earth-orbit state, which **brought** 12\% too little sunlight there, and run
on several threads, so each pair **compares** two realisations: ...; the land surface, which **moved** the air by at
most 0.3~\textdegree C;"
*What happens.* Under PlaSim's Sun clock and Earth's orbit, 0°E received 328 of the 373 W m⁻² due (defect log A1–A2).
The two runs of each pair are realisations (A6). The land test changed the air's temperature by at most 0.3 °C (G07);
"moved the air" first reads as wind.
*Fix.*
> Three other explanations were tested at the site where the rings cross the equator at 0\textdegree~E, in boxes
> forced from the Earth-orbit state, in which the site received 12\% too little sunlight, and run on several
> threads, so each comparison is between two realisations: the ring's two dimensions, since a three-dimensional box
> ran warmer still; the land surface, which changed the air's temperature by at most 0.3~\textdegree C; and the slow
> fall of lunar rain, since rain falling at Earth's speeds warmed the air by a further 1.0~\textdegree C.

**V28** · `results.tex`:130–131 (changed in round 20) · mild
*As it stands.* "The remainder, a degree or two, plausibly **comes from** the two models' upward transport of the
ground's heat"
*What happens.* The register gives the remainder as "plausibly from boundary-layer transport" (G07); "results from"
states that relation exactly.
*Fix.*
> The remainder, a degree or two, plausibly results from the two models' upward transport of the ground's heat:

**V29** · `results.tex`:137–138 · clear
*As it stands.* "A small box forced from the Earth-orbit state **brought** 34~mm to the ground per lunar day"
*What happens.* The box's rain at the ground was 34 mm per lunar day (G08); the same sentence already says the GCM
"rained 129~mm".
*Fix.*
> A small box forced from the Earth-orbit state rained 34~mm onto the ground per lunar day, where the GCM that forced
> it rained 129~mm and the Sun-and-tilt run 180~mm, ...

**V30** · `results.tex`:170–172 · mild
*As it stands.* "Part of the difference from Earth may **come from** the grid, ... and on the Earth benchmark a
coarser grid **gave** fewer, larger flashes."
*What happens.* On the benchmark, the storm on a coarser grid made fewer, larger flashes (G10;
`notes/electrification.md`:97–98).
*Fix.*
> Part of the difference from Earth may result from the grid, since the box's 6~km columns correspond to about 1~km
> at Earth's scale and on the Earth benchmark the storm made fewer, larger flashes on a coarser grid.\claim{G10}

**V31** · `results.tex`:172–173 · mild
*As it stands.* "two exoplanet **estimates** of lightning **use** laws fitted to Earth's storms"
*What happens.* Braam et al. and Sergeev et al. estimated lightning with laws fitted to Earth's storms, as the
sentence goes on to say.
*Fix.*
> Where the lunar runs separate charge and compute each flash, two exoplanet studies estimate lightning with laws
> fitted to Earth's storms, whose tops stand far below the lunar runs' 55--80~km: ...

**V32** · `results.tex`:193–195 · mild
*As it stands.* "the same 10~m wind, fetch and duration **build** waves 4--5 times as high as on Earth"
*What happens.* The wind builds the waves over a fetch and a duration (G12).
*Fix.*
> ... and with Wu's drag law at both gravities, the same 10~m wind, blowing over the same fetch for the same duration,
> builds waves 4--5 times as high as on Earth, with periods five times as long, ...

**V33** · `results.tex`:200 · clear
*As it stands.* "The waves **keep** Earth's steepness."
*What happens.* Under the similarity, the lunar waves have Earth's steepness, height 4–5% of wavelength (Terluna
`climate/waves/README.md` 42–43, at 186b294).
*Fix.*
> The waves are as steep as Earth's.

### reach.tex

**V34** · `reach.tex`:14–15 · mild
*As it stands.* "The Sun clock **acts** in any non-synchronous run on the default solar geometry whose rotation
differs from one day."
*What happens.* In such a run PlaSim's clock skips the Sun back each model day (H23).
*Fix.*
> The Sun clock skips the Sun back in any non-synchronous run on the default solar geometry whose rotation differs
> from one day.

**V35** · `reach.tex`:15–18 · clear
*As it stands.* "since ExoPlaSim's synchronous mode, even as it fixes the Sun in the sky, keeps the model day its
rotation period **sets**"
*What happens.* The synchronous mode sets only `NFIXED` and `FIXEDLON`, and the code still computes N and the model
day P·N/(N−1) from the rotation period (W06).
*Fix.*
> The convective-cover unit, by contrast, biases synchronous runs as well, since ExoPlaSim's synchronous mode fixes
> the Sun in the sky while the code still computes the model day from the rotation period, so the cover rises by
> about $+0.23$ for TRAPPIST-1e's rotation of 6.1 days \autocite{yang2023cloud} and $+0.31$ for Proxima
> Centauri~b's 11.2 days \autocite{boutle2017exploring}.

**V36** · `reach.tex`:18–20 · mild
*As it stands.* "The third defect, the orbit default, **gives** Earth's seasons to any run that sets an obliquity or
an eccentricity without fixing the orbit."
*What happens.* PlaSim replaces the configured obliquity and eccentricity with Earth's orbit for 1 AD (defect log A2;
W06).
*Fix.*
> The third defect, the orbit default, replaces a configured obliquity or eccentricity with Earth's, so that any run
> that sets one without fixing the orbit has Earth's seasons.\claim{W06}

**V37** · `reach.tex`:36–37 · clear
*As it stands.* "whereas SWAN's ST6 drag, exact quadruplets and bottom friction, and SWASH's rotation, all outside
that configuration, **keep** Earth's constants."
*What happens.* These routines set Earth's gravity, Earth's air and water densities, a dimensional friction
coefficient and Earth's rotation in their source (`notes/waves.md`:265–276; defect log B26). This is the form of the
author's CM1 example.
*Fix.*
> ..., whereas SWAN's ST6 drag, exact quadruplets and bottom friction, and SWASH's rotation, all outside that
> configuration, are coded with Earth's constants.

**V38** · `reach.tex`:39–40 · mild
*As it stands.* "Earth alone **lies near** the fits in the adapted models."
*What happens.* Earth's columns and conditions are near those the fits were made on (W02).
*Fix.*
> Of the natural worlds in Figure~\ref{fig:regimes}, then, Earth alone has conditions near those on which the
> adapted models' fits were made.

**V39** · `reach.tex`:46–51 · clear
*As it stands.* "ExoPlaSim would **need** its general repairs, its fixed-orbit setting and its released radiation,
... while its cloud **keeps** Slingo's fit to Earth's convection and PlaSim's Earth-tuned thresholds"
*What happens.* A modeller would run ExoPlaSim with those settings; no such run has been made (W03). PlaSim computes
convective cover from Slingo's formula and large-scale cover from relative-humidity thresholds
(`notes/exoplasim.md`:267–271).
*Fix.*
> For slowly rotating planets with Earth's gravity and air around a Sun-like star near Earth's insolation, such as
> those of the cooler runs that \textcite{yang2014strong} and \textcite{way2018climates} made with CAM3 and ROCKE-3D,
> a modeller would run ExoPlaSim with its general repairs, its fixed-orbit setting and its released radiation, which
> was fitted on columns and a spectrum like theirs, while its cloud would still be computed from Slingo's fit to
> Earth's convection and PlaSim's Earth-tuned thresholds, Earth fits of a process through which those studies found
> the climate to change with rotation.

**V40** · `reach.tex`:51 · clear
*As it stands.* "Their warmer runs, however, at up to 2.9 times Earth's insolation, **lie** beyond the radiation's
fits."
*What happens.* The released radiation was fitted on columns and a spectrum near Earth's, and those runs' insolation
is outside that range (W03).
*Fix.*
> Their warmer runs, however, at up to 2.9 times Earth's insolation, are outside the range of the radiation's fits.

**V41** · `reach.tex`:52–53 · mild
*As it stands.* "unless the year **holds** about twelve rotations"
*What happens.* The model day matches the solar day only when the year is about twelve rotations long (W03).
*Fix.*
> At rotations slower than 20 days, moreover, ExoPlaSim's model day departs from the solar day unless the year is
> about twelve rotations long, 69.8 against 77.6 days ...

**V42** · `reach.tex`:57–72 · clear
*As it stands.* Six sentences and two headings make worlds and schemes need things: the heading "Worlds that **need**
refitted calibrations"; "so their shortwave **needs** refitting"; "Even the Open Moon **needs** its calibrations
refitted"; "and so **needs** the general repairs"; "nitrogen--oxygen air **needs** the same steps"; "a breathable moon
**needs**, besides its column, the downward infrared that PlaSim now **takes** at its top"; the heading "Worlds that
**need** new physics".
*What happens.* A modeller refits, computes or builds what the modelling of each world requires (W03–W05). PlaSim's
patch 06 adds a downward infrared flux at the model top (`models/exoplasim/README.md`, patch 06).
*Fix.* The two headings are optional changes, since headings commonly omit the agent:
> \textbf{Worlds for which the calibrations have to be refitted.} \textbf{Worlds for which new physics has to be built.}

The sentences:
> ..., receive a spectrum outside the near-infrared water fit, so for them PlaSim's shortwave has to be refitted
> against the reference with the star's spectrum. Even for the Open Moon, the calibrations have to be refitted and the
> cloud settings checked at 1.0~atm, a case yet to be run, or behind another shield that blocks the ultraviolet, while
> under a shield that passes the ultraviolet the Moon's air would form ozone, which every patched CM1 build sets to
> zero.

> ..., and so modelling it requires the general repairs, a curved-air table of its own column and calibrations
> refitted to it.

> On a larger planet, modelling nitrogen--oxygen air requires the same steps, a slant factor from its own column
> among them, though ...

> Around a giant planet, modelling a breathable moon requires, besides its column, the downward infrared that PlaSim
> now adds at its top for the host's glow.\claim{W04}

**V43** · `reach.tex`:64–66 · clear
*As it stands.* "its 1~bar level **stays** inside RRTMG's pressure range, while the pressure on ground below that
level **lies** past RRTMG's tables"
*What happens.* RRTMG's tables start at 1,053.63 hPa; the 1 bar level is inside them, and higher pressures are
extrapolated (H20; W04).
*Fix.*
> For CM1's radiation, its 1~bar level is inside RRTMG's pressure range, while the pressure on ground below that level
> exceeds the highest pressure in RRTMG's tables, as it does over the lunar seas.

**V44** · `reach.tex`:72–74 · clear
*As it stands.* "Titan's nitrogen--methane air at 94~K, present Mars's thin carbon dioxide and Venus's 92~bar **lie**
outside what PlaSim's and RRTMG's radiation and Morrison's water-only microphysics represent"
*What happens.* Those atmospheres are outside the gases, pressures and condensables the schemes compute (W05).
*Fix.*
> Titan's nitrogen--methane air at 94~K, present Mars's thin carbon dioxide and Venus's 92~bar are outside what
> PlaSim's and RRTMG's radiation and Morrison's water-only microphysics represent, so ...

**V45** · `reach.tex`:86–87, 101, 105, 106 (Table 4) · mild
*As it stands.* Caption: "and what **lies** beyond them". Cells: "ExoPlaSim's default **puts in** Earth's orbit";
"PlaSim's sunlight lacking CO$_2$ and O$_2$", where the shortwave bands lack them; "where the radius table **falls**
under the fitted 10~\textmu m".
*What happens.* PlaSim replaces the configured orbit with Earth's (defect log A2). PlaSim's two shortwave bands carry
no CO₂ or O₂ (defect log B15). Below 190 K the radius table gives radii under 10 µm (`notes/exoplasim.md`:137–139).
*Fix.*
> and what is beyond them.

> ExoPlaSim's default replaces the configured orbit with Earth's

> PlaSim's shortwave lacking CO$_2$ and O$_2$

> ice optics below 190~K, where the radius table gives radii under the fitted 10~\textmu m

### next.tex

**V46** · `next.tex`:7–8 · mild
*As it stands.* "where the resolved cloud feedback **came out** much weaker than the GCMs'"
*What happens.* In Lefèvre et al.'s runs the resolved feedback was weaker, as the sentence reports.
*Fix.*
> where the resolved cloud feedback was much weaker than the GCMs' \autocite{lefevre2021convection}.

**V47** · `next.tex`:9–11 · clear
*As it stands.* "The first experiments **take up** the two Earth fits whose **tests moved** the test world's climate
most:"
*What happens.* The first two experiments refit the longwave correction at the settled state and fit PlaSim's cloud
to CM1's resolved cloud (the next two paragraphs; `notes/exoplasim.md`:290–291). The changes made in the tests moved
the climate (G05).
*Fix.*
> In the first experiments, the two Earth fits that moved the test world's climate most when changed in the tests are
> refitted: PlaSim's longwave by height, under its correction, and its cloud, still uncalibrated.

**V48** · `next.tex`:19–22 · clear
*As it stands.* "Refitting the correction ..., **decides** whether the warm state holds: if the consistent state
returns near 295~K, the design's dimming **stands**, and if it stays near 307~K, the dimming that **holds** the design
temperature must grow"
*What happens.* The refit and its iteration determine the settled climate (`notes/exoplasim.md`:239–241). The author
chose the dimming to hold the design temperature (G04).
*Fix.*
> Refitting the correction on the settled state's cloud-free columns, and iterating to a consistent pair of fit and
> climate, determines whether the warm state holds: if the consistent state returns near 295~K, the design's dimming
> is kept, and if it stays near 307~K, the dimming chosen to hold the design temperature must grow, and the rain and
> cloud change with it.

**V49** · `next.tex`:22–25 · mild
*As it stands.* "a reduced correlated-$k$ scheme built from the reference model's own spectroscopy would **go
further**, replacing the correction and the fits"
*What happens.* The scheme would replace Sasamori's scheme and the correction fitted to it (`notes/exoplasim.md`:239–241);
the participle already names the operation.
*Fix.*
> Beyond the refit, a correction with humidity among its predictors would extend the fit, and a reduced
> correlated-$k$ scheme built from the reference model's own spectroscopy would replace the correction and the fits
> of Sasamori and of Lacis and Hansen.

**V50** · `next.tex`:32–33 and 36–38 · clear
*As it stands.* "PlaSim's cloud amount and cloud water **move** the test world by several kelvin"; "Refitted cloud
could **move** the test world as far as the cloud settings do, up to about 6~K, and the design's dimming with it."
*What happens.* Changing the cloud settings changed the global-mean surface temperature by up to about 6 K (G05,
G16). After a change of climate, the author would reset the dimming (`next.tex`:51 says so of the reference).
*Fix.*
> Changing PlaSim's cloud amount and cloud water moves the test world's temperature by several kelvin, and both
> remain uncalibrated for it.

> Refitted cloud could move the test world's temperature as far as the cloud settings do, up to about 6~K, and the
> design's dimming would be reset with it.

**V51** · `next.tex`:35–36 · mild
*As it stands.* "the same runs test whether the corrected longwave **closes** the 3.7~K by which CM1's lowest 1.8~km
at 45\textdegree\,N stays warmer than the GCM's."
*What happens.* The runs would test whether the corrected GCM removes the 3.7 K offset (G06; `notes/cm1.md`:161–162).
*Fix.*
> and the same runs test whether the corrected longwave removes the 3.7~K by which CM1's lowest 1.8~km at
> 45\textdegree\,N stays warmer than the GCM's.

**V52** · `next.tex`:49–50 · mild
*As it stands.* "before it **serves** further worlds"
*What happens.* Modellers would use the corrected reference to calibrate the models for further worlds.
*Fix.*
> would require the multipliers and the gas bands to be refitted against a corrected reference before it is used
> for further worlds;

**V53** · `next.tex`:68–71 (changed in round 20) · mild
*As it stands.* "an independent GCM's air as warm as CM1's would **point to** PlaSim's boundary layer and longwave as
the next repairs, and air as cool as PlaSim's to the slices' forcing and CM1's microphysics"
*What happens.* With a third model's result, the author could rank the candidates, and each would then be tested
directly (round 20, Codex's third finding). "Suggest" is the generic verb for that, without the figure.
*Fix.*
> ...: an independent GCM's air as warm as CM1's would suggest PlaSim's boundary layer and longwave as the next
> repairs, and air as cool as PlaSim's would suggest the slices' forcing and CM1's microphysics, each then to be
> tested directly.

**V54** · `next.tex`:76–78 · mild
*As it stands.* "a first **step** would **correct** the GCM's column mass and heights"
*What happens.* The modeller would correct the column mass and heights before adopting a deep core
(`notes/exoplasim.md`:294).
*Fix.*
> ... include both effects, and before they are adopted, the GCM's column mass and heights would first be corrected,
> while a test of the circulation's sensitivity would show whether the full equations are needed.

**V55** · `next.tex`:88–89 · clear
*As it stands.* "if they remove little, the cause **lies in** RRTMG's other approximations"
*What happens.* The extrapolation is one candidate cause, untested; RRTMG's other approximations are the rest
(`notes/cm1.md`:143–146).
*Fix.*
> if they remove little, the cause is among RRTMG's other approximations, and replacing RRTMG with the in-house
> correlated-$k$ scheme becomes the step.

**V56** · `next.tex`:89–91 · clear
*As it stands.* "the difference of about 5~W\,m$^{-2}$ in the air's absorbed sunlight that the Sun's unfiltered
spectrum **brings**."
*What happens.* RRTMG computes with the Sun's own spectrum scaled to the shield's total; at 0°E, about 5 W m⁻² of the
difference in clear-air absorption between CM1 and the GCM results from it (defect log B9).
*Fix.*
> Separately, giving RRTMG the shield's spectrum, in a run of its own, would correct the difference of about
> 5~W\,m$^{-2}$ in the air's absorbed sunlight that results from the Sun's unfiltered spectrum.

**V57** · `next.tex`:95–98 · clear
*As it stands.* "and **limits** scaled with the capillary length **would show** how much of the evaporation the small
drops cause, testing whether the drop-size treatment **needs** a gravity dependence as well as the fall speeds."
*What happens.* Runs with the limits scaled would measure the share of evaporation due to small drops (N03;
`notes/cm1.md`:72–78 and 163).
*Fix.*
> and runs with limits scaled with the capillary length would show how much of the evaporation the small drops cause,
> testing whether the drop-size treatment, like the fall speeds, has to depend on gravity.\claim{N03}

**V58** · `next.tex`:99–101 · clear
*As it stands.* "If larger drops **bring** CM1's surface rain toward the GCM's, the rain gap **closes** on the GCM's
side and the rain-fed lakes of the design **keep** their source; if CM1's rain stays near a quarter of the forcing
GCM's, the lakes' water budget has to be **drawn** from the cloud-resolving rain."
*What happens.* CM1's surface rain would rise toward the GCM's, and the two models would agree near the GCM's amount;
the design's lakes are fed by rain, and their budget is computed from a model's rain (G08).
*Fix.*
> If larger drops raise CM1's surface rain toward the GCM's, the two models agree near the GCM's rain and the
> rain-fed lakes receive the rain the design assumed; if CM1's rain stays near a quarter of the forcing GCM's, the
> lakes' water budget has to be computed from the cloud-resolving rain.

**V59** · `next.tex`:107–109 · clear; the verb also changes the claim
*As it stands.* "Under Saunders and Peck's law, hail, striking ice and snow at 4--8~m\,s$^{-1}$, **carried** most of
the charge, and under Takahashi's, hail **carried** 37--43\%"
*What happens.* The records count each particle's share of the non-inductive charging: hail did 82–88% of it under
Saunders and Peck's law and 37–43% under Takahashi's, with graupel most of the rest (N01; Terluna
`climate/crm/README.md` 2145–2149, "hail, which does 82–88 % of the charging under Saunders and Peck"). The charge each
particle carried is a different quantity, which the records leave unreported. Results states the main run's figure
as charging ("does 87% of the non-inductive charging", `results.tex`:166).
*Fix.*
> Under Saunders and Peck's law, hail, striking ice and snow at 4--8~m\,s$^{-1}$, did most of the non-inductive
> charging, and under Takahashi's, hail did 37--43\% and graupel, striking at about 1--4~m\,s$^{-1}$, most of the
> rest.

**V60** · `next.tex`:109–112 · clear
*As it stands.* "the sign of that charge would **decide** between the two laws for hail, and graupel's sign at its own
speeds would complete the measurements that **decide** the arrangement the model's lunar storms take."
*What happens.* A measured sign would show which law is right for hail; the model computes the sign rimed ice takes
from the chosen law, and with it the arrangement (N01).
*Fix.*
> Measured in a laboratory at hail's speeds in 0.02--0.2~g\,m$^{-3}$ of cloud water at $-5$ to $-16$\,\textdegree C,
> the sign of that charge would determine which of the two laws holds for hail, and graupel's sign at its own speeds
> would complete the measurements that determine the arrangement the model's lunar storms take.\claim{N01}

**V61** · `next.tex`:112–113 · clear
*As it stands.* "The sign of the ground strikes under Takahashi's law also **stays open** in the windows:"
*What happens.* The first window's rule let no channel reach the ground, and the second window's strikes carried
charge left from a run with leakage off, so the sign under Takahashi's law is undetermined (G11).
*Fix.*
> The windows also leave the sign of the ground strikes under Takahashi's law undetermined: the first window ran
> under a rule that let no lunar channel reach the ground, ...

**V62** · `next.tex`:119–121 · clear
*As it stands.* "the spread between source-term packages, Komen's against Janssen's and ST6, would **decide** whether
the similarity image of an Earth sea holds on the test world"
*What happens.* The checks and the spread between packages would test the Earth-fitted source terms
(`notes/waves.md`:301–311).
*Fix.*
> ..., would test whether the similarity image of an Earth sea holds on the test world; a wide spread would make the
> lunar wave heights a range.

**V63** · `next.tex`:127 · mild
*As it stands.* "the gas-transfer and mixing laws such models **take**"
*What happens.* A one-dimensional model of a lake computes its mixing and gas transfer from laws fitted on Earth's
waters; it applies them.
*Fix.*
> the gas-transfer and mixing laws such models apply, fitted on Earth's lakes and seas, would be among the Earth
> values to test, and so would the one-dimensional form itself.

### appendix.tex

**V64** · `appendix.tex`:7–14 · clear
*As it stands.* "The channels of the curved-air table **group** the design column's wavenumbers"; "until each group's
energy-weighted mean optical depths **absorb** a direct beam"; "a group must also **keep**, within the same 1\%, the
beam's loss above the bottom of every layer"; "the 282 below 1,250~nm ... **take** spherical successive orders of
scattering".
*What happens.* The code sorts and bisects wavenumbers into groups; a group, at its mean optical depths, absorbs the
beam; above 1,250 nm the group must reproduce the beam's loss above each layer; the sky solver computes the 282
channels by successive orders (R05; `notes/reference_radiation.md`, section 2.2).
*Fix.*
> \textbf{The curved-air table's channels.} Each channel is a group of the design column's wavenumbers within bands
> 10--40~nm wide up to 1,250~nm and 50~cm$^{-1}$ wide beyond. Within each band the
> wavenumbers are sorted by whole-column absorption and bisected by energy until each group, at its energy-weighted
> mean optical depths, absorbs a direct beam, on slant columns of 0.03 to 13 vertical columns, within 1\% of the
> group's sunlight of what its members absorb; beyond 1,250~nm a group must also reproduce, within the same 1\%, the
> beam's loss above the bottom of every layer, while below 500~nm each band is one channel. Of the 10,697 channels,
> the 282 below 1,250~nm whose whole-column absorption depth is under 3 are solved by spherical successive orders of
> scattering, continued until the newest order adds less than $2\times10^{-5}$, with a cap of 100.\claim{R05}

**V65** · `appendix.tex`:45–50 (Table 6 caption) · mild
*As it stands.* "A **default** in parentheses **reproduces** the released code unless the row says otherwise"; "Where
a general repair **takes** a lunar value, the value is its setting."
*What happens.* At the default, the patched code reproduces the released code; a lunar value is entered in the
parameter into which a repair turns an Earth value (`models/exoplasim/README.md`; `repairs.tex`:31–34).
*Fix.*
> At a default in parentheses, the patched code reproduces the released code unless the row says otherwise; changes
> marked unconditional act in every build that has them.

> Where a lunar value is entered in a general repair, the value is its setting.

**V66** · `appendix.tex`:147 · mild
*As it stands.* "0.6 points rms on 11 **unseen** columns"
*What happens.* The columns were outside the set the split was fitted on (V07; `verification.tex`:62).
*Fix.*
> 0.6 points rms on 11 columns outside the fit

### availability.tex

**V67** · `availability.tex`:21–23 (changed in round 19) · mild
*As it stands.* "and the scenario's early planning and the style rules applied to the text **drew on** the author's
conversations with ChatGPT (OpenAI)."
*What happens.* By Terluna's records, the knowledge bundle from which the scenario's earlier decisions were
recovered, and the editorial controls that the style rules consolidate, were written in the author's conversations
with ChatGPT (the Availability text at `ffdedfe`; the charter, section 2). The fix states that source relation and
adds no operation the records leave unnamed.
*Fix.*
> ...; and the author's conversations with ChatGPT (OpenAI) were a source for the scenario's early planning and for
> the style rules applied to the text.

**V68** · `availability.tex`:26–28 · mild
*As it stands.* "The work is an unfunded personal project that **brings** the author no income"
*What happens.* The author receives no income from the work, by the author's own declaration.
*Fix.*
> The work is an unfunded personal project from which the author receives no income, and the author's practice is to
> make public every part of it that its licences and sources allow.

### conclusions.tex, for the author

The author approved this text; each fix below is offered for the author to accept or leave.

**V69** · `conclusions.tex`:18–19 · clear
*As it stands.* "as the day lengthens, the conversion from rain to convective cover has to **retain** its intended
physical time interval."
*What happens.* The repaired code counts convective rain per 86,400 s in place of the model day (`repairs.tex`:42;
H07).
*Fix.*
> as the day lengthens, the conversion from rain to convective cover has to count rain over its intended physical
> time interval.

**V70** · `conclusions.tex`:19–20 · mild
*As it stands.* "Where one physics package **serves** the global and the resolved calculations"
*What happens.* In the LMD's models both calculations run the same physics code (`next.tex`:4–8; spiga2009new).
*Fix.*
> Where the global and the resolved calculations use one physics package, as in the LMD's models, its parameters are
> shared by construction \autocite{spiga2009new};

**V71** · `conclusions.tex`:32–33 · clear
*As it stands.* "Otherwise the comparison **mixes** the response of the convection schemes with a change in where the
air gains and loses heat."
*What happens.* When the models place their cooling differently, a comparison of CM1 with the GCM that forces it
measures both effects at once; "confounded" is the exact term for that.
*Fix.*
> Otherwise the response of the convection schemes is confounded in the comparison with a change in where the air
> gains and loses heat.

**V72** · `conclusions.tex`:35–36 · clear
*As it stands.* "A reduced radiation scheme built from the reference spectroscopy would **extend this work beyond**
successive adjustments of the inherited broadband fits."
*What happens.* The scheme would replace the broadband fits and the corrections fitted to them (`next.tex`:22–25).
*Fix.*
> A reduced radiation scheme built from the reference spectroscopy would replace the inherited broadband fits and
> their successive adjustments.

**V73** · `conclusions.tex`:40–41 · clear
*As it stands.* "A different stellar spectrum would then **enter** through the spectral calculation, with its effects
followed into circulation and cloud."
*What happens.* The spectral calculation would take the star's spectrum as an input (`next.tex`:25–27: such a scheme
would hold "under the starlight its shortwave would be built for"). "Enter" is the verb of the author's first
example.
*Fix.*
> The spectral calculation would then take a different stellar spectrum as an input, with the spectrum's effects
> followed into circulation and cloud.

**V74** · `conclusions.tex`:42–43 · clear
*As it stands.* "That development would **join** the existing ability to explore climates quickly to a physical
reference that can be recomputed for the worlds being explored."
*What happens.* The reduced scheme would run in the GCM, whose speed lets a modeller explore climates quickly
(`conclusions.tex`:8–9), and the reference it is built from can be recomputed for each world (`next.tex`:22–30).
*Fix.*
> With that development, a modeller could still explore climates quickly, with the radiation computed from a
> physical reference that can be recomputed for the worlds being explored.

**V75** · `conclusions.tex`:45 · mild
*As it stands.* "Cloud **requires** a further exchange between the models."
*What happens.* The cloud calibration fits PlaSim's cloud to CM1 runs forced from the GCM (`next.tex`:32–41).
*Fix.*
> Calibrating cloud requires a further exchange between the models.

**V76** · `conclusions.tex`:58–60 · mild
*As it stands.* "The scaled wave tests **offer** a complementary case"
*What happens.* The tests themselves are the case: scaled runs that agree in dimensionless form (V04; V05).
*Fix.*
> The scaled wave tests are a complementary case, in which dimensionless sea states agree closely along the tested
> paths, with Earth's empirical coefficients retained.

**V77** · `conclusions.tex`:60–62 · clear
*As it stands.* "An ensemble that computes both can **examine** which properties of an environment follow a
similarity law"
*What happens.* The ensemble computes storms and seas; the modeller examines its results.
*Fix.*
> With an ensemble that computes both, a modeller can examine which properties of an environment follow a similarity
> law and which emerge from competing processes whose relative rates change.

**V78** · `conclusions.tex`:64–65 · mild
*As it stands.* "Constructed worlds **permit** these comparisons over combinations of parameters"
*What happens.* Modellers can make the comparisons on constructed worlds, which can hold air where a natural world
would lose it (`introduction.tex`:56–67).
*Fix.*
> On constructed worlds, these comparisons can be made over combinations of parameters that atmospheric escape would
> exclude from a natural temperate planet.

**V79** · `conclusions.tex`:65–67 · clear
*As it stands.* "A massive atmosphere on a small body **separates** the consequences of low gravity from those of thin
air"
*What happens.* On such a body a modeller varies the pressure at fixed gravity, so the column mass changes alone, as
the sentence's second clause says.
*Fix.*
> On a small body with a massive atmosphere, the consequences of low gravity can be separated from those of thin air,
> and varying the atmosphere's pressure then changes the column mass while leaving gravity fixed.

**V80** · `conclusions.tex`:75 · clear
*As it stands.* "The **choice** of those cases can also **sharpen** the use of terrestrial experiments."
*What happens.* The modeller chooses the cases, and comparing runs locates the conditions at which measurements would
discriminate between laws (`conclusions.tex`:77–79; N01).
*Fix.*
> A modeller can also choose those cases to direct terrestrial experiments.

**V81** · `conclusions.tex`:79–80 · mild
*As it stands.* "A storm's planetary **scale** can thus be **combined** with experiments on the particles composing it"
*What happens.* The modeller combines a storm simulated at planetary scale with laboratory results on its particles.
*Fix.*
> A storm simulated at planetary scale can thus be combined with experiments on the particles composing it, and the
> revised particle physics tested in the climates where its consequences are largest.

**V82** · `conclusions.tex`:80–81 · clear
*As it stands.* "**Comparisons** across worlds would help select the experiments as well as **use** their results."
*What happens.* Modellers compare worlds, select experiments and use their results.
*Fix.*
> Comparing worlds, modellers could select the experiments as well as use their results.

**V83** · `conclusions.tex`:83–85 · mild
*As it stands.* "those **developments** would **refine** the climate predicted under its prescribed starlight. For a
constructed world, **they** could **change** the illumination chosen to sustain a desired climate, as the radiation
corrections already changed the dimming in the lunar design."
*What happens.* The developed models would refine the predicted climate; after the radiation corrections, the author
chose a new dimming for the lunar design (G04).
*Fix.*
> For a natural planet, the models so developed would refine the climate predicted under its prescribed starlight.
> For a constructed world, the illumination chosen to sustain a desired climate could change with them, as the dimming
> of the lunar design changed with the radiation corrections.

**V84** · `conclusions.tex`:86–87 · clear
*As it stands.* "so the storm and sea calculations have to **follow** the revised climate."
*What happens.* CM1, SWAN and SWASH would be rerun with forcing from the revised GCM climate.
*Fix.*
> so the storm and sea calculations have to be rerun from the revised climate.

**V85** · `conclusions.tex`:87–88 · clear
*As it stands.* "Designs with similar mean warmth could then be compared through the water **they deliver** to the
land and the winds **they drive** over the seas."
*What happens.* In the designed world, rain falls on the land and winds blow over the seas.
*Fix.*
> Designs with similar mean warmth could then be compared through the rain on their land and the winds over their
> seas.

**V86** · `conclusions.tex`:89–90 · mild
*As it stands.* "The same ensemble would **serve** the interpretation of a world found around another star and the
design of an environment"
*What happens.* People would use the ensemble to interpret a found world and to design a constructed one.
*Fix.*
> The same ensemble could be used to interpret a world found around another star and to design an environment whose
> boundary conditions people could choose.

**V87** · `conclusions.tex`:97–99 · clear
*As it stands.* "**Comparing** changes in illumination or surface-water distribution through these connected
calculations could **turn** a broad temperature requirement into a geographically specific design."
*What happens.* A designer compares the connected calculations' results and turns the requirement into a design.
*Fix.*
> By comparing changes in illumination or surface-water distribution through these connected calculations, a
> designer could turn a broad temperature requirement into a geographically specific design.

## Figures let stand

- **"Hold" as validity** (`verification.tex`:62; `reach.tex`:37; `next.tex`:20, 26): a fit or a state holds within a
  range. The approved abstract uses the verb this way ("hold near the columns they were fitted on").
- **"Err" and "depart from"** (`reach.tex`:22–28, 52; `next.tex`:20): the paper's terms for a value that differs from
  the world's own. The approved abstract uses "depart".
- **"Meet their conditions"** (`reach.tex`:13): to meet a condition is to satisfy it, and the abstract's approved
  sentence uses the phrase.
- **Patches and builds as code** (`verification.tex`:5, 21–22, 33): a patch at its default repeats arithmetic, and a
  build holds its patches. A patch is code, and a build contains it.
- **Radiation codes and channels** (`verification.tex`:77, 100; `results.tex`:120–121): a scheme cools the model air
  through the heating it computes, and in radiative transfer a band or channel absorbs.
- **Runs as the simulated world** (throughout `results.tex`): a run warms, rains, settles and parts, as this
  review's brief allows; Repairs already says a box "rained".
- **Physical position, extent and persistence** (`results.tex`:50, 161–164, 173, 181–187, 200; `next.tex`:104, 123;
  `reach.tex`:33; `verification.tex`:107, 126): charge lies at 40–42 km, levels and cloud tops stand at heights,
  spectra reach a band's edge, rimed ice takes a charge, a column keeps its ice, a series reaches its cap. Each subject
  is physical or a series that grows to a limit.
- **Physical causation** (`results.tex`:118; `next.tex`:123, 127; `reach.tex`:60; `appendix.tex`:102): circulation
  carries heat, swell carries energy, a temperature contrast resists mixing, a shield passes the ultraviolet, a flash
  hands charge to the ions.
- **Checks and data as tests** (`verification.tex`:115, 120; `next.tex`:56–57, 86): a check falls short of or misses
  its criterion; a pair of runs measures, and compared outputs test a repair's arithmetic. Each sentence names the
  criterion or the comparison.
- **Texts and code inputs** (`verification.tex`:38; `reach.tex`:4, 8; `next.tex`:29, 83, 90, 105; `appendix.tex`:46):
  a table lists and gives, a row says, Results describes, a code takes, reads and receives its inputs, and the
  reference model supplies spectra to the tools.
- **People acting on a figurative object** (`results.tex`:116; `next.tex`:8): the disagreement "was taken apart term
  by term", and codes "are brought toward that consistency". Both agents are modellers, and the same sentence or the
  next names the operation.
- **Relations stated as measures** (`results.tex`:135; `verification.tex`:122): a bracket measures a disagreement;
  runs from different builds compare as realisations.
- **Idioms with exact meanings** (`reach.tex`:42; `availability.tex`:8, 14): "as they stand", a register "tracing"
  numbers to their sources, patches that "inherit their licences".
- **"Follow" in the Conclusion's opening** (`conclusions.tex`:3, 12; with the followed effects in V73): the abstract's
  approved verb for the chained computation from global climate into storms and seas, in which the GCM's fields force
  CM1 and the wave models. It works as the paper's governing image; the author may still prefer "compute".
- **The Conclusion's vision** (`conclusions.tex`:93–109): rain arriving in basins, winds forcing the sea, waves
  arriving at a coast, light reorganising clouds. Physical verbs on physical subjects, as directed.

## Other findings

### F1 · MINOR · `next.tex`:13–15

*What fails.* The overview, changed after round 18, says the remaining experiments test approximations "in the
dynamics, the microphysics, the wave physics and the lakes and seas beneath the waves". Two of the section's steps
are left out: the comparison with an independent GCM (lines 67–71) and the radiation in CM1 (lines 82–91). So the
overview again lists fewer steps than the section has, as round 18's F3 found before. The phrase "approximations in
... the lakes and seas" also names the waters, where the section's last paragraph tests the models of the waters.

*Fix.*

> The remaining experiments compare the present models with an independent GCM and use the lunar departures from
> Earth to test specific approximations in the dynamics, CM1's radiation, the microphysics and the wave physics, and in
> the models of the lakes and seas beneath the waves.

### F2 · MINOR · `next.tex`:84–88

*What fails.* Round 20's clause "the near-ground range that remains would test the boundary-layer explanation, beside
the ice above 107~km and the dry ground at 45\textdegree\,N" leaves out the relation of the last two items. On a
first reading "beside the ice" names a place. The intended sense is that the range would test the boundary-layer
explanation against the two candidates that Results reports as open (`results.tex`:123–130).

*Fix.*

> ... the near-ground range that remains would test the boundary-layer explanation against the two candidates still
> open, the ice above 107~km and the dry ground at 45\textdegree\,N; if they remove little, ...

## Checks

- **Snapshot and tree.** `git rev-parse HEAD` gave `a50e0b177d089b6ccb232eafbf94cd157ae4a4af` and
  `git status --short` printed nothing, at the start and before this record was written. At the end it lists two
  untracked files, this record and the other reviewer's `editorial_round21_closing_front.md`. `sha256sum` of
  `paper/build/main.pdf` gave `f6ff147f…3f`, round 20's hash.
- **Excluded words.** A search of the seven files found no "not", "rather than" or "n't" in authorial prose. Every fix
  above was checked for both and adds neither.
- **Lint** (`paper/tools/lint.py` on the seven files, screening only; it wrote nothing): 6 negative-contrast, 2
  self-reference, 21 possible-empty-action, 5 coined-term, 81 universal-claim and 9 generic-verb candidates. Four of
  the empty-action lines have verb findings above (`results.tex`:200; `reach.tex`:87; `next.tex`:107–108, 113). The
  others are physical uses or the noun "reach". The lint's verb list has "carry", "reach", "sit" and a few others,
  and leaves out "enter", "lie", "keep", "hold", "take", "bring", "decide" and "need", the verbs of most findings
  here; adding them to its pattern would screen these figures in later rounds.
- **Evidence for each fix.** Each "what happens" line cites the claim, note, README, defect-log entry or Terluna record
  read for it. Where a fix states an operation, the record names it: the charging shares (V59), the steepness (V33),
  Yang et al.'s cover (V24) and the channel construction (V64) were each read in their source.
- **Changed text.** The diff `ffdedfe..a50e0b1` for `paper/main.tex` and `paper/sections` was read in full. In this
  half the diff changes Verification (one sentence removed), Results (V28), Reach (line 6), Next steps (F1, F2, V53 and the
  lakes and seas), the Conclusion (lines 12, 28, 95–97), Table 7 (line 133) and Availability (V67).
- **Unperformed.** No build, no visual inspection of the PDF and no read-aloud review.
