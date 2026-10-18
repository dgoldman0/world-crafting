# Editorial round 17: evidence and scope, 18 October 2026

Snapshot: commit `127888759c7b6db0d37565de68f8c0e0e5211f4d` (1278887); the working tree of `paper/` is identical to it.
Reader: a fresh Claude Opus 5.5 subagent, reading the whole paper for evidence and scope, with priority on the
passages changed since 50c3e35, the round-16 additions among them. This record is the only file the reader wrote.

**What was read and sampled.** `AGENTS.md`; `paper/review/editorial_round16_light.md`; the related-work scan;
`git diff 50c3e35 1278887 -- paper/sections`; every section of the paper in full. Each statement about the 23 sources
cited or re-cited in round 16 was set against the abstract held in the scratchpad file of abstracts, the source's
manifest record and its `paper_use` statements, and, where an original is archived, that original: Lefèvre et al.
2021, Spiga and Forget 2009, Braam et al. 2022, Sergeev et al. 2025, Mlawer et al. 2023, Banfield et al. 2015 and Tan
et al. 2021. Older citations were sampled in their archived originals: Richardson et al. 2007, Deitrick et al. 2020,
Way et al. 2017, Way et al. 2018 and Tsigaridis et al. 2025. Numbers were sampled against `paper/claims.json` and
its sources: S02–S04, S09–S11, S13–S16, H03, H07, H08, H11–H14, H20, H21, H23, H24, R05, R06, R09, R10, V07,
V10, G01–G06, G08, G10, G12, G14, W02–W04, W06, N01, N03, N04 and Z01, through `paper/data/*.json`,
`python/climate/results/gcm/twilight.json`, the reference model's code and notes, and Terluna at 186b294 (the
decisions register, the GCM, CRM and wave READMEs, and the atmospheric-electricity sources); Z01 was recounted from
Terluna's log. `python3 paper/tools/check.py` ran with its standing warnings only.

**Overall judgment.** The round-16 additions hold to their sources. Every number they bring in matches its abstract
(7 and 6 K, 14 and 24 K, 20–30 K against 8 K, 60 and 10–20 W m⁻², 2.5 and 1.5 W m⁻², twentyfold gravity, sixteen
cases of a 15-day rotator around a 3000 K star), each statement about the field names the works it rests on, and the
proposed SAMOSA test stands on ExoPlaSim's own arithmetic, which gives that rotation a model day of 15.65 days and a
cover bias of +0.34. No sentence claims a priority that the newly cited chains contradict: the paper rests what is
new on its classification of Earth values and its split between general repairs and per-world calibrations
(introduction.tex:91–105), and it sets TAM and TRAMS, PlanetWaves and the LMD's models beside its own links as
precedents. Reproducibility and physical validation stay distinct, and the lunar climate's conditional state is
stated once. The two MAJOR findings lie outside the round-16 text: the Introduction credits each porting team with
removing the Earth values that mattered for its target worlds, which the paper's own ExoPlaSim findings contradict,
and the electrification benchmark cites four runs for a flash-rate range that Terluna's record draws from four other,
uncited works. The fourteen MINOR findings concern the scope of two abstract sentences the author approved,
attribution details in the new citations, a few universal words, and gaps in the review history and the source
records. Nothing is BLOCKING.

Counts: BLOCKING 0, MAJOR 2, MINOR 14.

## Abstract

**1. abstract.tex:10–12, with worlds.tex:14–15. MINOR.** *What fails:* "which makes it a test of every Earth value
that depends on them" claims more than the runs examined. The lunar runs exercise the Earth values on the paths they
take, and the paper itself records Earth values that depend on the same ratios and stay untested on the Moon: gravity
at 9.81 "in schemes those paths leave unselected" (assumptions.tex:15–16), the inventory's row of unselected options,
"Unused in the lunar runs" (assumptions.tex:216), SWAN's ST6 drag, exact quadruplets and bottom friction and SWASH's
rotation, which "keep Earth's constants" (reach.tex:39–40), and "CM1's other schemes at 9.81" (reach.tex:102). The
Moon also departs in one direction along each ratio, so a value that errs only under stronger gravity, a shorter day
or a thinner column falls outside its test. *Evidence:* the passages quoted; W02 registers the ratios, and the
inventory is scoped "on their paths" (assumptions.tex:150). *Fix:* drop "every" in both places: "which makes it a test
of the Earth values that depend on them", keeping `\claim{W02}` in worlds.tex. The abstract's sentence is author-approved
text (`abstract_and_repository_2026-10-18.md`); the change is offered for the author's decision.

**2. abstract.tex:14–16. MINOR.** *What fails:* "three of them produce little or no error at Earth's values, yet by
ExoPlaSim's own arithmetic they bias its runs of slowly rotating and tidally locked planets" gives all three defects one
condition and drops the Introduction's "runs that meet their conditions". The Sun clock acts only in non-synchronous
runs on the default solar geometry, at any rotation other than one day, so it leaves tidally locked runs alone and
also shifts the Sun for rotations near one day (reach.tex:13–15; H23: "~1 deg for a rotation near Earth's set away
from one day"); the orbit default acts in any run that sets an obliquity or an eccentricity without fixing the orbit,
whatever its rotation (reach.tex:19–21; W06). The cover unit alone biases every slowly rotating and tidally locked run.
*Evidence:* H23, W06, reach.tex:12–21, introduction.tex:95–97. *Fix:* "...yet by ExoPlaSim's own arithmetic they bias
its runs that meet their conditions, runs of slowly rotating and tidally locked planets among them.\claim{H23}\claim{W06}",
the Introduction's wording. Author-approved text; for the author's decision.

## Introduction

**3. introduction.tex:49–50. MAJOR.** *What fails:* "Each team removed the Earth values that mattered for the worlds it
set out to model, but others could stay" credits each team with removing every Earth value that mattered for its
target worlds, and for ExoPlaSim the paper's own evidence says otherwise. ExoPlaSim was built for synchronously
rotating planets and planets of non-solar spectra, and its unit conversions were changed so that slow rotators could
run (Paradise et al. 2022, arXiv v2 p. 1 and Sect. 2.1, manifest locators). Its developers left the convective cover's
conversion per model day in place, which biases the cover by 0.125 ln(day/1 d) on slow rotators and in synchronous
mode, +0.23 for TRAPPIST-1e and +0.31 for Proxima Centauri b (assumptions.tex:114–117, H07; reach.tex:15–19, W06), and
the clause just before records that the near-infrared water absorptivity is still "tuned to a solar spectrum"
(introduction.tex:48–49; Paradise et al. Sect. 5, manifest locator). *Fix:* "Each team removed Earth values that mattered
for the worlds it set out to model, but others could stay:", which keeps the credit, drops the claim of completeness
and still leads into ROCKE-3D's and THOR's reports.

**4. introduction.tex:20. MINOR.** *What fails:* "Some have been joined to GCMs." follows the sentence naming SAM, CM1
and SWAN, so "Some" reads as some of those three, and none of them was joined to a GCM in the works cited. *Evidence:*
SAM's 4 km runs took sea surfaces from its own 40 km run (yang2023cloud, manifest locator, Methods p. 10); Banfield et
al. drove SWAN with "reasonable ranges of atmospheric pressure and wind" (archived original, abstract); Tan et al.'s
archived text mentions GCMs only in its background and discussion. The chains named next run other Earth-built models:
TRAMS, adapted from RAMS (literature.md:368), PlanetWaves and WRF's core. *Fix:* "Other models built for Earth have been
joined to GCMs."

**5. introduction.tex:21. MINOR.** *What fails:* in "tuned the GCM's convection scheme with its runs and observations",
"its" binds most readily to the GCM, which drops the link to the resolved runs that makes the Titan work a joined chain.
*Evidence:* Battalio et al., abstract: "Using results from the Titan Regional Atmospheric Modeling System (TRAMS) and
observations, we tune the parameters of the SBM parameterization". *Fix:* "tuned the GCM's convection scheme with the
cloud-resolving runs and observations", as next.tex:40–41 words it.

**6. introduction.tex:50–51. MINOR.** *What fails:* "report that the changes their first release made from the Earth
configuration went unstudied" states more than the source. *Evidence:* Tsigaridis et al. 2025, p. 5834, Sect. 3.3
(archived original): "the changes from the tight Earth configuration to the more general one were not studied
systematically". *Fix:* "went without systematic study".

## Repairs

**7. repairs.tex:98–99. MINOR.** *What fails:* "the diffuse light of a pseudo-spherical two-stream
\autocite{dahlback1991new,kylling1995reliable}" rests on two sources recorded at title depth (manifest: depth "not
read", support "title only"), so round 16's account that each new citation was checked against its abstract leaves
these two unchecked; the manifest notes that Dahlback and Stamnes's pseudo-spherical attribution "is unverified here",
and their title names "a new spherical model". The code's two-stream is Zdunkowski et al.'s practical improved flux
method with a direct beam through spherical shells, a source the bibliography excludes, so a reader can take Kylling
et al.'s algorithm for the code's. *Evidence:* `python/atmosphere/radiative_convective/METHODS.md`:111–119;
`python/climate/gcm/twilight.py`, `two_stream`; `paper/notes/literature.md`:70. *Fix:* read the two abstracts and
record locators, and attach the citation to the approximation the code shares with them: "with the diffuse light of a
two-stream given a pseudo-spherical direct beam \autocite{dahlback1991new,kylling1995reliable}, which the code runs only
with the Sun above the horizon".

**8. repairs.tex:134. MINOR.** *What fails:* "HITRAN's collision-induced absorption \autocite{karman2019update}" cites
the 2019 state of HITRAN's CIA section, while the reference reads files of 2021 (N2–N2), 2024 (O2–N2, O2–O2) and 2018
(N2–H2O), the same kind of version gap that round 16 closed for MT_CKD with "at version 4.3". *Evidence:*
`python/atmosphere/radiative_convective/spectroscopy.py`:396–397. *Fix:* "HITRAN's collision-induced absorption
\autocite{karman2019update}, in its files of 2018–2024,".

## Verification

**9. verification.tex:83–86. MAJOR.** *What fails:* "Set beside published runs of the same charging and lightning
schemes \autocite{macgorman2001lightning,kuhlman2006numerically,sun2023aerosol,salinas2021modeling}, ... its flash rates
and median charge per flash fall inside their ranges": "their" are the four cited runs, yet the benchmark's flash-rate
range comes from four other works, none cited in the paper or recorded in the manifest. *Evidence:* Terluna's benchmark
table, the source of V10 (`climate/crm/README.md`:1762–1765 at 186b294), gives the published flash rates as 34 a
minute (Mansell 2014), 75 (Brothers et al. 2018), 100–200 with peaks of 400–500 (Ziegler et al. 2014) and 300–600
(Calhoun et al. 2014); of the four cited, it takes first-flash times from MacGorman et al., Kuhlman et al. and Sun et
al., the charge per flash (2.7–39.6 C) from MacGorman et al., and the in-cloud share from Salinas et al.; the manifest
records Kuhlman et al., Sun et al. and Salinas et al. as "not read", carried from that table. *Fix:* give Mansell
(2014), Brothers et al. (2018), Ziegler et al. (2014) and Calhoun et al. (2014) bibliography and manifest records
(Terluna's `research/studies/atmospheric_electricity/sources.json`, S28, S29 and S32, holds their readings) and add
them to the citation; or confine the sentence to what the cited runs supply: "...where those runs flash first at
27–40 minutes and carry charges per flash that bracket its median, while ...", keeping `\claim{V10}`.

## Results on the test world

**10. results.tex:89. MINOR.** *What fails:* "on clear-sky columns of 250–360 K" gives the range to the columns, which
reads as columns at those temperatures throughout. *Evidence:* Yang et al. 2016, abstract: "with fixed moist adiabatic
profiles for surface temperatures from 250 to 360 K". *Fix:* "on clear-sky moist adiabats with surface temperatures of
250–360 K".

**11. results.tex:104–105. MINOR.** *What fails:* "the one change that moves the cooling by height" overstates: the
curved-air terms also take a tabulated infrared escape from every PlaSim layer, scaled with its temperature. *Evidence:*
repairs.tex:106–107; `twilight.json`, `longwave.gcm_layers`, the shells' widening at 0.02–2.9 W m⁻² by layer. What sets
the correction apart is that it was fitted to the cooling by height (repairs.tex:146–151). *Fix:* "the one change fitted
to the cooling by height".

## Reach to other worlds

**12. reach.tex:12–13. MINOR.** *What fails:* "The three ExoPlaSim defects that the general repairs remove" misclasses
the third. *Evidence:* the orbit default is avoided with ExoPlaSim's own `fixedorbit` switch (repairs.tex:42–44),
"Avoided" in the inventory (assumptions.tex:171), and an avoidance in W01; general repairs remove two of the three.
*Fix:* "The three ExoPlaSim defects, two removed by general repairs and the third avoided with the fixed-orbit switch,
remain in the released code".

## Next steps

**13. next.tex:43. MINOR.** *What fails:* "Every calibration was fitted to the line-by-line model" misses the longwave
correction, fitted against the correlated-k emulation. *Evidence:* assumptions.tex:76–78; Terluna
`climate/gcm/README.md`:775, "Against correlated-k on about 2,100 of those columns"; repairs.tex:131–132, "calibrated
against the reference model and its correlated-k emulation". *Fix:* "Every calibration was fitted to the line-by-line
model, the longwave correction through its correlated-k emulation, and that model's carbon dioxide, oxygen,
collision-induced absorption and sunlight have yet to be compared with an independent code on the lunar column."

## Availability, authorship and review

**14. availability.tex:8–9. MINOR.** *What fails:* "the paper's check script confirms that every marker resolves and
every listed source exists" claims more than the script does. *Evidence:* `paper/tools/check.py`:7–12 and 86–93 report
web sources unfetched and check drive files only when the drive is mounted; on this snapshot the script lists H23's and
N02's web source as "recorded, unchecked offline". *Fix:* "confirms that every marker resolves and that every listed
file exists, and lists the web records it leaves unchecked".

**15. availability.tex:76–81. MINOR.** *What fails:* the review history ends at the abstract's rewrite. It omits the
related-work scan by five Claude subagents, the reason for CM1's slices added at the author's direction, and round 16,
in which sixteen citations entered the body, the Introduction, the Conclusion and the abstract in seven steps, each
followed by a light reading by a fresh Claude Opus 5.5 subagent; this round follows. *Evidence:*
`paper/notes/related_work_scan_2026-10-18.md`; `paper/review/slice_reason_2026-10-18.md`;
`paper/review/editorial_round16_light.md`; AGENTS.md, "Final releases carry an accurate AI-assistance disclosure and
the actual review history". *Fix:* one or two sentences at the close of this round naming the scan, the slice reason,
the four body steps with the Introduction, Conclusion and abstract after them, the seven light readings and round 17.

## Source records

**16. paper/sources/manifest.json. MINOR.** *What fails:* (a) each round-16 source records one use, in the body section
it entered, while the Introduction and the Conclusion make further statements about it: sergeev2022thai, "a spread their
authors relate to the models' parameterization choices" (introduction.tex:56–58) and THAI's cases (conclusions.tex:66–67);
spiga2009new, "its parameters are shared by construction" (conclusions.tex:18–20); lefevre2021convection and
detelich2026modeling (introduction.tex:22–25); rafkin2022interaction and battalio2022interaction (introduction.tex:20–21,
conclusions.tex:47–49); haqqmisra2022samosa (conclusions.tex:66–67); hogan2022tool and hogan2020evaluating
(conclusions.tex:35–37). (b) Two statements rest on the PlanetWaves repository's README, Detelich et al.'s GCM winds and
PlanetWaves' descent from an Earth model (repairs.tex:200–202, introduction.tex:22); the README appears only inside
`paper_use` support text, with no record of its own (address, commit or retrieval date, quote). (c) mlawer2023inclusion's
notes still read "no abstract retrieved", while its depth is abstract and the archived original carries the abstract on
its first page. *Fix:* add the uses with their support, a web-record entry for the README, and correct the note.

## Checked and found sound

**The round-16 sources against their abstracts, records or originals.**
- Cazaubiel et al. 2019: a centrifuge, gravity up to 20 times Earth's, wave turbulence with container modes (abstract).
  The statement that wind seas keep Earth's gravity in the laboratory rests on Banfield et al. (p. 373, "This did not
  allow us to explore varying gravity") and the scan's search, and fits both.
- Price and Rind 1992, cloud-top height (abstract); Braam et al. 2022 set their flash rates from it (archived original,
  Sect. 2.4). McCaul et al. 2009, the upward flux of precipitating ice at −15 °C and the column's ice (abstract);
  Sergeev et al. 2025 apply it as F = 0.95F₁ + 0.05F₂, the upward graupel flux and the total ice water path, in their
  storm-resolving runs and Price and Rind in their coarse runs (archived original, Sect. 2.2), so "graupel" and the split
  between the two kinds of run match.
- Lacis and Oinas 1991, the correlated-k method (abstract). Karman et al. 2019: the four pairs the code reads are among
  the section's pairs (abstract; spectroscopy.py:396–397), with the version gap of finding 8. Mlawer et al. 2023: the
  archived original's abstract documents MT_CKD's inclusion in HITRAN; "at version 4.3" stays the code's own
  (`python/README.md`), as round 16 placed it.
- Rafkin et al. 2022, dozens of TAM's unstable profiles starting TRAMS; Battalio et al. 2022, two parameters of the
  simplified Betts–Miller scheme tuned with TRAMS results and observations (abstracts).
- Song et al. 2022: a 2 km two-dimensional cloud-resolving model, qualitatively consistent with a GCM in the Walker
  circulation and the substellar clouds, with large differences in cloud water path and cloud width (abstract).
- Schneck et al. 2026 and Detelich et al. 2026: an adapted physics-based wave model across gravity, atmospheres and
  liquids, and PlanetWaves on Titan's lakes (abstracts), with the GCM winds and the parent model from the README
  recorded in `paper_use` (finding 16).
- Spiga and Forget 2009: WRF's core with the LMD GCM's physics, driven at its boundaries by the GCM (abstract), and
  constants converted to Mars's values (p. 3 locator), which fits the Conclusion's "its parameters" and the abstract's
  opening on separately built models. Lefèvre et al. 2021: WRF with the LMD Generic radiative transfer and
  cloud/precipitation over Proxima b, a much weaker cloud feedback (abstract); Sect. 2.2's heading, "Coupling with
  complete LMD Generic GCM physical packages", supports the Introduction's broader "GCM physics".
- Turbet et al. 2022, 7 K and 6 K in the dry cases; Sergeev et al. 2022, 14 K and 24 K in the moist cases, all four GCMs
  temperate, parameterization choices as the authors' framing (abstracts).
- Haqq-Misra et al. 2022: a 15-day synchronous rotator around a 3000 K blackbody, 16 cases from an ExoPlaSim
  exploration, a preliminary ExoCAM comparison (abstract); W06's formula, recomputed, gives N = 24, a model day of
  15.65 d and a cover bias of +0.34 for that rotation.
- Yang et al. 2016: five band and two line-by-line codes, 60 W m⁻² in the shortwave, outgoing longwave differences
  growing with surface temperature to 10–20 W m⁻²; Yang et al. 2019: 20–30 K for the tidally locked M-star case, within
  8 K for the rapidly rotating G-star case, causes as named (abstracts).
- Hogan and Matricardi 2022 and 2020: a free tool dividing the spectrum into k-terms to a tolerance the user sets, and a
  protocol scoring schemes against benchmark line-by-line spectra for Earth's conditions and palaeo-to-future gas
  scenarios (abstracts).
- Prather and Hsu 2019: 2.5 and 1.5 W m⁻² as recorded in `paper_use` from the full abstract (the scratchpad copy is
  truncated). Li and Shibata's small Earth effect (literature.md:165–167) concerns the slant path, a different quantity.

**Precedent and novelty.** No sentence claims a first beyond the ensemble's own runs: reach.tex:3 and
conclusions.tex:68 speak of the repaired codes and the ensemble's cases. Banfield et al. forced SWAN with prescribed
winds (archived abstract), so Detelich et al. stand as the nearest GCM-to-wave precedent, and Repairs names them with
"likewise" (repairs.tex:200–202). The Titan tuning appears as a precedent in Next steps and the Conclusion, and the
LMD route as the alternative to repair and calibration in the Introduction, Next steps and the Conclusion. Results and
Next steps draw no general rule from Yang et al. 2023, Lefèvre et al. 2021 or Song et al. 2022; each statement stays
with its study.

**Numbers against their sources.**
- `regime_calc.json`: 7.245 (7.25), 52.4 km and 22.8 (52, 23), 7.22 and 34.45, 0.465 (about half), 1.0567 (5.7%),
  5.37, 9.21 and 15.26% (5.4, 9, 15.3), 1.053–1.059 (about 5%), 6.04, 2.94 and 2.27, 6.04 and 0.407, 5.43, 5.24×10⁻⁶ s⁻¹
  and 13.9 d, 0.424, 12.08 model days and 120 steps, 32.5° and 0.99°, 10.3°, 15.65° and 32.7°, 69.8 against 77.6 d and
  265 against 726 d, +0.228 and +0.305, 64.3 and 147.5 billion years (60 to 150), 0.0081 (a hundredth), 2.457, 7.38–7.50
  km, 17.46%.
- `worlds.json`: Chapman factors 22.2, 24.5 and 14.0; columns 10.5 and 100.4 times Earth's; Mars at 1 bar 4.96 times
  Earth's H/R, 2.60 times its column, 0.38 g; Titan's H/R 0.0080, 0.27 of the Moon's.
- `repairs.json`: −20.0, +2.30 (2.5 settled), +1.76 (1.6 settled), +0.59, −0.65, −2.23, +11.50, −3.21 (3.5), +1.71
  (2.2), −4.98 (5.9); the table of states' means match.
- `gap45n.json`: 5.87 to 3.70 K, 37% removed, as the caption says. `layers.json`: 4.21 W m⁻² above 85 km.
  `slant.json`: 7.14 and 13.54 at the horizon, fits within 0.30% and 0.08%. `sun_clock.json`: 0.917 and 1.174.
  `twilight.json`: +10.32 W m⁻² of sunlight, +16.15 of infrared, −5.83 net, −6.53 and +0.70, 1.40 of twilight.
- Terluna at 186b294: S14 (3⅓–4.7 minutes a model year on 4 ranks), S15 (142–198 K; 0.61–1.4 kg s⁻¹ without magnets;
  decisions lines 51, 125, 370), S16 (no budget for rented compute, CRM README 688–690), H03, H23, H24, R09, V07, G08,
  G10, G12, N04; Z01 recounted at 374 of 487 commits.

**Recurring numbers.** The abstract's at least 20 K, about 6 K and 1.6–2.5 K match Results; 14 and 24 K match between
the Introduction and Results; 3.7 K, 1.5 K, 4.5 W m⁻², 85% and 57–73%, 11.5 K and 307 K match between Results and
Next steps; 1.2 atm and 1,216 hPa, 7.25, 52 km, 29.53 days, 5.44% and 0.303% match wherever they recur.

**Universal words.** "Most fall into three classes" (introduction.tex:98) holds at 22 of the 40 rows of the table of
changes; the abstract's "mostly took repairs" holds at 14 of the 25 inventory rows of constant, time or geometry form
(12 of 22 without the defects); "most general circulation model (GCM) studies" is THOR's developers' statement
(Deitrick et al., archived original, Sect. 1).

**Reproducibility, validation and conditional results.** Verification separates code checks from calibrations and
benchmarks; Results bounds the near-ground bracket to "that one GCM state"; the Conclusion keeps the wave tests to "the
tested paths, with Earth's empirical coefficients retained"; the Introduction states the conditional state of every
lunar climate number once; the abstract attributes the escape result to the design's calculations.

**Author-approved choices.** The conditions the abstract's rewrite moved to the body, the radiation scheme's range and
the limit CM1's Earth-fitted microphysics sets on the cloud calibration, stand in next.tex:24–30 and 38–41 and
conclusions.tex:37–39 and 51–52, so the abstract's shorter "would replace those fits" follows the author's direction.

## Checks made and left undone

Made: `git diff 50c3e35 1278887 -- paper/sections`; `python3 paper/tools/check.py`; `pdftotext` on the archived
originals named above; `git show 186b294:<path>` on the Terluna lines named above; the Z01 recount; reads of
`paper/data/*.json`, `twilight.json`, `twilight.py`, `spectroscopy.py`, the reference model's `METHODS.md` and the
component notes. Left undone: no web fetch (the PlanetWaves README, the OSTI abstract of Prather and Hsu, the abstracts
of Kylling et al. and Dahlback and Stamnes); no drive file opened, `check.py` having confirmed their presence; no PDF
build; Terluna sources beyond the cited lines unread. The G6 status of the round-16 sources, BLOCKED or DEFERRED at
abstract depth, belongs to the release register and is left there.
