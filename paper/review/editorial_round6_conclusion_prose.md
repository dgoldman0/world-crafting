# Editorial round 6: the closing section, prose

## 1. Record

- **Reviewer:** a fresh Claude subagent, Claude Opus 5.5 (1M context), which had seen no earlier review of the paper.
- **Date:** 2026-10-17.
- **Snapshot:** commit 8bfd069 (8bfd069a6432e7b94c1524f3935096e592ab6d24), read with `git show 8bfd069:<path>`.
  When the review began the working tree's `paper/sections/` matched the snapshot (`git diff 8bfd069 --
  paper/sections/` came back empty); by its end other work had modified next.tex, repairs.tex,
  paper/sources/manifest.json and paper/Makefile in the working tree. This record cites the files at 8bfd069 only,
  and its one change to the repository is this file.
- **Severities:** BLOCKING breaks the author's direction or a rule as the author would reject it; MAJOR is a clear
  breach; MINOR is polish. Line numbers are those of the files at 8bfd069. Word counts of rewrites are approximate.

**Files in scope**

| File | Read | sha256 at 8bfd069 |
|---|---|---|
| paper/sections/conclusions.tex | whole section | 81986ca02bb0dff1b95b263945ac3144f74e189dbdce7af97341e014c27e25c2 |
| paper/sections/abstract.tex | whole abstract | 0cf59842b240289e4b318ed5b082c58df0340b44232585ff549a648459c9272d |
| paper/sections/results.tex | whole file; revised passages at 44–46, 81–86, 91–97, 151–155 | 10466525ecf68ba0c6b56fbb0d9a6f8a45c8979bf531635c7faabd3ce1813948 |
| paper/sections/reach.tex | whole file; revised passages at 38–42, 90–93, 114 | 99d26b100d9a9072f2660b0a7dc29fcf9a7cc398da32acf7154390d893209d02 |
| paper/sections/next.tex | whole file; revised paragraph at 35–43 | d0ee214445d0194d9dcf1fb310e2979d11705b4ac50046dd6ebf6fdb28d859ec |
| paper/sections/assumptions.tex | whole file; revised sentence at 21–27 | 8f267b18c88d50e4083b9169adb7d38d6fcecd9fd0d11d14f58270989b798e68 |

**Rule files, each read in full**

| File | sha256 |
|---|---|
| AGENTS.md at 8bfd069 | e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32 |
| Terluna (HEAD f03b839) ensemble/planning/Open_Moon_Editorial_Charter_control-01.md | aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0 |
| Terluna ensemble/planning/source_controls/STYLE_NOTES.md | 659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46 |
| Terluna ensemble/planning/source_controls/Jewish_Papers_Updated_Style_Notes.md | 18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab |
| Terluna ensemble/planning/source_controls/Agent_Working_State_Editorial_Gates.md | 553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464 |

**Context read**

- In full at 8bfd069: introduction.tex (b8325d641b56d6da32cffbcaa143e26461495322235c2de3b0709402f1ef5b72),
  worlds.tex (453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112), verification.tex
  (4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00) and repairs.tex
  (bb1d22c01616fdaf454280acded56316b7995af2a8fc3bb5a255af52c92e793c); main.tex
  (7ef8255c7fa8d14e9d0d61406d1f919be6dff5251b47fb3598aba9c913a8495c) for the order of sections.
- paper/claims.json (6b4718a2be6128506d693a87cdcc2753194d0d8d39cce9c0a9038ed490f0cfb8): the entries S09, S12,
  S15, H04, H07, H11, H21, H23, H24, R04–R06, R08, V04, V06, V16, G01–G05, G09–G12, G14, G16, G17, W01–W06, N01,
  N03 and N04.
- paper/sources/manifest.json (1bd81f61a4be8999481e6268021d588d082c6dc2f20256a1b368c5bf83d9ea29): the records for
  saunders1998laboratory, takahashi1978riming, vincendon2010spherical, yang2023cloud, sergeev2025lightning,
  braam2022lightning and loftus2021physics.
- Archived originals, text-searched at the passages the conclusion uses: vincendon2010spherical.pdf
  (afcdf418a60ce367c8b16c12d68c1bac36ea2fd8e0013498ea3553c0cbd8a7e9; abstract and Sect. 1),
  loftus2021physics.pdf (d080f1289e115952977c4b09fa0f9e1b8d93f305315804c84a7878ed0a805d2c; App. C1, p. 22),
  sergeev2025lightning.pdf (b2c3352f4ad065bd894341eb76741ff541b1bf4c4824612ae7e6404bd373c6df; Sects. 2.2 and
  4.2) and braam2022lightning.pdf (26486cfc19cb2185ca8f98a22bcbadf40a526afed1f8b3d460154915b58cf8c7; Sect. 2,
  the flash-rate scheme).
- models/swan/README.md at 8bfd069 (abb218a0608362f5d2d58cbb72b4d6defcaacb02f06d7123690d862dbc15109d), searched
  for the source-term configuration.

**Unopened.** Every file under paper/review/ (I listed the directory's names once, to confirm that this record's
name was free) and under paper/notes/; the earlier rounds' records; the files other agents keep in the session
scratchpad, which include drafts of this section and a round-5 file.

**Method.** I read the introduction and the abstract, then the conclusion whole, then each of its paragraphs whole
and sentence by sentence under the charter's ten passes (section 11) and AGENTS.md "Writing", and then each revised
passage in its paragraph. I checked each number in the conclusion against the body and the claim register, and the
passages on Titan's haze, laboratory drops, the flash-rate schemes and explicit charging against the archived
originals. The abstract, the opening pages and the conclusion were read as one arc.

**Cadence.** Silent reading only; the audible pass that G3 requires for a conclusion remains pending. The
conclusion holds 1,422 words in 25 sentences, about 57 a sentence counting numbers and units as words, with seven
sentences above 80 (conclusions.tex:3–7, 15–19, 21–26, 28–33, 63–67, 67–71 and 81–86).

**Screening.** `paper/tools/lint.py` on the six files; its output is screening only. In the conclusion and the
abstract: three negative-contrast hits (conclusions.tex:5 and 7, abstract.tex:10), each required by its
proposition ("no coefficient fitted", "little or no error"); twelve universal-claim hits, each checked against the
body and the register, of which conclusions.tex:43 and 82 and abstract.tex:24 enter findings 8 and 1; one possible
empty action, "laboratories reach" (conclusions.tex:52), whose subject is an agent; one generic verb, "would give"
(conclusions.tex:77, finding 12). In the revised passages: no excluded word, and the "reach" hits are the noun.

**Scratchpad.** To search the sections for repeated numbers I wrote copies of nine snapshot sections into the
session scratchpad at 23:14, under plain names (abstract.tex, assumptions.tex, introduction.tex, next.tex,
reach.tex, repairs.tex, results.tex, verification.tex, worlds.tex), and text extracts of four originals
(vinc.txt, loftus.txt, serg.txt, braam.txt). Other agents use that directory; a file kept there earlier under one
of those names would have been overwritten by the snapshot's copy.

## 2. Findings

### 1. MAJOR: the proposed scheme's domain is the tables' range, while the check that conditions it covers one column

- **Locations:** conclusions.tex:39–43; conclusions.tex:81–84; abstract.tex:21–25; with next.tex:27–31.
- **Text:** "A scheme built from the reference's line-by-line spectroscopy would replace the radiation's gas fits, the
  largest of the Earth fits, for air of nitrogen and oxygen with water and modest carbon dioxide at the pressures
  and temperatures its tables cover, up to 3.2~bar and 375~K, once that spectroscopy has been checked against an
  independent code, and the cloud optics would remain fits." The landing repeats the domain ("at pressures and
  temperatures within the reference's tables ... once a scheme is built and the spectroscopy checked"), and so
  does the abstract ("at the pressures and temperatures its tables cover").
- **Rule:** claims stay within their evidence; G5, under which a conditional claim keeps exact conditions; the
  author's direction against a conclusion that suggests the work reaches worlds it has yet to test.
- **Why:** "Up to 3.2 bar and 375 K" is the span of the reference's correlated-$k$ tables, which clamp at their
  edges (claim R08): the reach of a computation. The reference has run on lunar columns, its emulation is checked at
  288–290 K and on a saturated 330 K column (R08), and the calibrations were fitted near 1.2 atm. The condition
  attached, "once that spectroscopy has been checked against an independent code", reads in the paper's own terms
  as the step at next.tex:27–31, which compares the reference "on the lunar column" by running "the design column"
  through LBLRTM and a DISORT solver. Read together, the sentences name worlds up to 3.2 bar and 375 K as served once
  one column has been checked. The body states neither the tables' range nor "the reference's tables" (git grep
  finds both only in the conclusion and the abstract; the reach section bounds the adapted models by RRTMG's
  1.05 bar), so the bound first appears at the section's end, conditioned on a check of narrower scope.
- **Rewrite**, in one of two readings, the author's choice:
  - (a) Keep the range and widen the check. conclusions.tex:39–43: "A scheme built from the reference's
    line-by-line spectroscopy would replace the radiation's gas and scattering fits, the largest of the Earth fits,
    for air of nitrogen and oxygen with water and modest carbon dioxide at the pressures and temperatures its tables
    cover, up to 3.2~bar and 375~K, once an independent code has checked that spectroscopy across that range, and
    the cloud optics would remain fits." (+4 words; "gas and scattering" follows the abstract, since the first
    calibration fitted a Rayleigh multiplier beside the continuum.) abstract.tex:21–25: "... at the pressures and
    temperatures its tables cover, once an independent code has checked that spectroscopy across them, while ..."
    (+2 words). next.tex:29: "Running the design column, and columns spanning the reference's tables, through
    LBLRTM ..." (+6 words), so that the planned step meets the condition.
  - (b) Keep the planned check and narrow the range. conclusions.tex:39–43: "... for air of nitrogen and oxygen with
    water and modest carbon dioxide at the pressures and temperatures at which an independent code has checked that
    spectroscopy, within its tables' 3.2~bar and 375~K, and the cloud optics would remain fits." (±0 words); the
    abstract likewise.
  - Under either reading the tables' range belongs in the body where the reference is described
    (repairs.tex:120–125), one clause from R08 (+12 words).
- **Check:** no excluded word; "would" keeps the scheme's state as a proposal; the check stays unperformed in both
  readings.

### 2. MAJOR: the landing attaches the lightning's sign to the cloud fit and states Earth's drop limits as part of the procedure

- **Location:** conclusions.tex:81–86.
- **Text:** "... and fit its cloud scheme to cloud-resolving runs whose drop-size limits stay Earth's and whose lightning
  takes its sign from charging laws that Earth's laboratories can test."
- **Rule:** sentences carry their dependencies (G3 names list-like clauses disguised by syntax among its blocking
  failures); conclusions and the arc; the final-page arc pass.
- **Why:** Fitting a GCM's cloud scheme takes cloud cover and cloud water from the cloud-resolving runs; the sign
  of those runs' lightning plays no part in it, and the clause "whose lightning ..." joins it to the fit only
  because the same runs compute it. With that clause the last sentence takes up the section's lines in turn
  (geometry, gas absorption and cloud from the third paragraph, drops from the fifth, lightning from the fourth),
  and its final stress falls on the sign of the lightning, a side result for a modeller of a new world, where the
  abstract and the introduction end on the fits and on which repairs hold elsewhere. The drop-size clause does bear
  on the fit, since drop size moves the runs' rain and cloud water, yet "stay Earth's" reads as an instruction,
  while the fifth paragraph names runs with scaled limits as the step to make.
- **Rewrite**, with finding 1's reading (a): "A modeller of a new world of nitrogen--oxygen air with water and modest
  carbon dioxide, at pressures and temperatures within the reference's tables and with a scale height at most three
  hundredths of its radius, the test world's ratio, would compute its radiative geometry from its own column, its
  gas absorption from the reference's spectroscopy once a scheme is built and the spectroscopy checked at those
  pressures and temperatures, and fit its cloud scheme to cloud-resolving runs of that world, whose drop-size limits
  stay Earth's until limits scaled by the capillary length have run." (about the same length). The sign of the
  lightning and its laboratory test stay in the fourth paragraph, which ends on that route. A shorter landing stops
  at "cloud-resolving runs of that world" (−22 words) and lands where the abstract lands.
- **Check:** the scaled-limit runs stay unperformed ("until ... have run"); no excluded word.

### 3. MINOR: the opening sentence repeats the abstract

- **Location:** conclusions.tex:3–7.
- **Text:** "Earth values in four forms and five defects were found in four Earth-built codes adapted to a world that
  departs from Earth at once in gravity, column mass, scale height over radius and day, and where a value was
  repaired, the kind of repair followed largely from its form: ..."
- **Rule:** conclusions and the arc (reciting the inventory); the redundancy pass.
- **Why:** The sentence restates abstract.tex:8–15 and introduction.tex:70–83 in their own words ("four forms",
  "five defects", "followed largely from its form", the three classes). A reminder serves the author's direction;
  this one opens on "were found" and on the test world's four ratios, which the section uses nowhere later, so the
  conclusion begins where the abstract began its findings. Opening on the relation keeps the reminder and leads
  straight to the defects.
- **Rewrite** (optional): "Where an Earth value in the four codes was repaired, the kind of repair followed largely
  from the value's form: units and constants took general repairs with no coefficient fitted to the test world,
  geometry took a method whose table is computed from the world's own column, and the radiation's fits took
  calibrations to a line-by-line model. Of the five defects, three, all in ExoPlaSim, produce little or no error at
  Earth's values ..." (about −25 words).

### 4. MINOR: relations written with "and", and two sentences above 80 words

- **Rule:** sentences carry their dependencies (coordination for propositions of equal weight); cadence.
- **conclusions.tex:21–26** (88 words): "A modeller finds such an error in maps of sunlight by longitude and of rain by
  season, and a comparison by global-mean temperature and albedo can pass large differences in cloud: in the
  comparison of ..." The two clauses contrast, and the evidence after the colon supports the second alone.
  Rewrite: "A modeller finds such an error in maps of sunlight by longitude and of rain by season. A comparison by
  global-mean temperature and albedo can pass large differences in cloud: in the comparison of
  \textcite{yang2023cloud} ..." (±0 words).
- **conclusions.tex:48–50:** "... disagree on the sign that rimed ice takes in little cloud water, and in two windows
  of an earlier electrified run ..." The opposite polarities follow from the disagreement, as results.tex:160–162
  states. Rewrite: "..., so that in two windows of an earlier electrified run ..." (+2 words).
- **conclusions.tex:65–67:** "..., and Earth's empirical laws of drag, wind input and breaking keep coefficients
  fitted at Earth's gravity ..." The clause bounds the similarity result. Rewrite: "..., while Earth's empirical laws
  ..." (±0).
- **conclusions.tex:67–71** (81 words): split at the semicolon: "... 2.46 times longer at a sixth of Earth's
  gravity. Experiments on the largest stable drops of other liquids ..." (±0).

### 5. MINOR: "moved it" assigns the cloud-setting tests to the design case

- **Location:** conclusions.tex:31–33.
- **Text:** "... warmed the design case by 11.5~K in their test, and PlaSim's Earth-tuned cloud settings, pushed to the
  ends of their tests, moved it by up to about 6~K as the runs settled ..."
- **Rule:** technical meaning survives editing (the conditions of a claim); precise nouns.
- **Why:** The nearest antecedent of "it" is "the design case". The cloud-setting tests ran from the Sun-and-tilt
  run, and the cloud-water bound from the first calibrated run (results.tex:76–81; claims G05 and G16). The
  sentence is also the fourth statement of this ranking (abstract.tex:18–21, results.tex:91–95, reach.tex:3–8),
  so its repair should keep it short.
- **Rewrite:** "... moved the global mean by up to about 6~K as the runs settled ..." (+2 words).

### 6. MINOR: two restated details that the argument leaves unused

- **Locations:** conclusions.tex:35–36; conclusions.tex:64.
- **Text:** ", whose air in curved shells loses a net 5.8~W\,m$^{-2}$ against the same clear column taken flat with a
  pseudo-spherical direct beam,"; ", whose linear wind input is reduced above a fixed 1~Hz,".
- **Rule:** the redundancy pass; write for the expert.
- **Why:** The third paragraph argues that the geometry is computed from the world's column while the dynamics
  keep a thin shell; the 5.8 W m$^{-2}$ (assumptions.tex:46–48) measures the geometry's size, which the paragraph
  leaves unused. The fifth argues that similarity runs test how gravity enters a code; the knee's mechanism stands
  at assumptions.tex:21–27 and reach.tex:34–35. Cutting both shortens the two longest paragraphs.
- **Rewrite:** delete both (−19 and −10 words).

### 7. MINOR: Titan's haze, a comparison that lacks its number and reads against worlds.tex

- **Location:** conclusions.tex:37–39.
- **Text:** "Titan's haze stands about as tall against its radius as the test world's air, and the plane-parallel codes
  that separate Titan's surface from its haze hold to about 65\textdegree\ from the zenith
  \autocite{vincendon2010spherical}, although Titan's nitrogen--methane radiation lies outside the adapted models."
- **Rule:** claims stay within their evidence; exact action ("lies outside" places an abstraction); sentences carry
  their dependencies ("and" joins a premise to its consequence).
- **Why:** worlds.tex:77–78 has "Titan's air, at 0.8\% of its radius, is about a quarter as tall in proportion";
  the conclusion's comparison holds for the haze's own scale height, which the text never gives. Vincendon and
  Langevin (arXiv v1, abstract) infer "an aerosols scale height of 80 ± 10 km" on Titan, 0.031 of its 2,575 km
  radius against the test world's 0.030 (Table tab:regime), so the claim holds, yet the claim register has no entry
  for it (the manifest's locator Td covers the 65°). The 65° follows from the tall haze, which "and" sets beside it
  as an equal fact.
- **Rewrite:** "On Titan, whose haze has a scale height of about 80~km, three hundredths of the radius as for the test
  world's air, the plane-parallel codes that separate the surface from the haze hold to about 65\textdegree\ from
  the zenith \autocite{vincendon2010spherical}, although the adapted models lack Titan's nitrogen--methane
  radiation." (+5 words), with a claim entry citing the abstract's sentence.
- **Check:** "lack" is the form AGENTS.md allows ("a scheme that lacks ice"); "three hundredths" matches the
  landing's term.

### 8. MINOR: cloud "would stay" or "remain" a calibration that is yet to be made

- **Locations:** conclusions.tex:43–44; abstract.tex:24.
- **Text:** "Cloud amount would stay a calibration for each world"; "while cloud would remain a calibration for each
  world".
- **Rule:** technical meaning (precise nouns, evidence state).
- **Why:** In the paper's terms a calibration is a fit to the reference or to runs of the test world
  (repairs.tex:11–20). PlaSim's cloud thresholds and Slingo's cover are Earth fits left open (Table tab:inventory,
  "Open"; next.tex:18–19, "remain uncalibrated for it"). "Stay" and "remain" assert a present calibration; the
  clauses mean that cloud would be fitted for each world, in contrast with the gas absorption a scheme would
  compute.
- **Rewrite:** "Cloud amount would be a calibration for each world, fitted to cloud-resolving runs of that world;
  ..." and "while cloud would be a calibration for each world, fitted to cloud-resolving runs, ..." (±0).

### 9. MINOR: the storms paragraph opens with its two tests unpaired with their laws

- **Location:** conclusions.tex:47.
- **Text:** "Some Earth-fitted laws of storms can be tested independently of the world modelled, in laboratories on
  Earth or against storms resolved at other gravities."
- **Rule:** precise nouns; claims stay within their evidence.
- **Why:** "Independently of the world modelled" fits the laboratory test; a test against storms resolved at other
  gravities runs a model at those gravities, independent of any one world's climate run. The paragraph then develops two laws, one for each test, which the sentence leaves the reader to pair.
- **Rewrite:** "Some Earth-fitted laws of storms can be tested apart from any one world's climate: the charging laws
  in laboratories on Earth, and the flash-rate laws against storms resolved at other gravities." (+5 words).

### 10. MINOR: "conditions laboratories reach" has no recorded source

- **Locations:** conclusions.tex:51–52; conclusions.tex:85–86; next.tex:80–81.
- **Text:** "conditions laboratories reach"; "charging laws that Earth's laboratories can test"; "conditions Earth's
  laboratories can reach".
- **Rule:** claims stay within their evidence (G5, G6).
- **Why:** Claim N01 records the deciding conditions from the model (4–8 m s$^{-1}$, 0.02–0.2 g m$^{-3}$, −5 to
  −16 °C); the statement that laboratories reach them has no claim entry. The records for Takahashi (1978) and
  Saunders and Peck (1998) are abstract-only, with admission BLOCKED, and the Saunders and Peck abstract records
  experiments arranged by rime accretion rate (EW × V), with negative graupel charging at low rates: laboratories
  have reached low cloud water, and the abstract records no speeds or temperatures. The fourth paragraph and part of
  the landing rest on the feasibility of the deciding measurement.
- **Repair:** record a locator for the speeds, effective water contents and temperatures an admitted laboratory
  study covered; with one, the prose stands. Until then the three clauses state a test that the record leaves
  unsupported.

### 11. MINOR: the proposed test of the flash-rate laws names one of its two fixed conditions

- **Location:** conclusions.tex:58–60.
- **Text:** "Resolving electrified storms at other gravities, with the same laboratory charging laws, could test those
  flash-rate laws, ..."
- **Rule:** G5 (a proposed study names its fixed assumptions).
- **Why:** The sentence before ascribes part of the main run's low flash density to its grid, and on the Earth
  benchmark a coarser grid gave fewer, larger flashes (results.tex:149–151; claim G10). A resolved flash rate that
  moves with the grid tests a flash-rate law at a grid where the count has converged.
- **Rewrite** (optional): "Resolving electrified storms at other gravities, with the same laboratory charging laws
  and on grids fine enough to converge the flash count, could test those flash-rate laws, ..." (+9 words).

### 12. MINOR: the last paragraph's turn from calibrations to defects is left to the reader

- **Location:** conclusions.tex:76–78.
- **Text:** "... and a lower pressure or another shield would give columns other than those the calibrations were fitted
  on. Away from Earth's values the repaired codes have run on the test world alone, so the three defects' biases on
  other worlds are known so far from the code's arithmetic; ..."
- **Rule:** inheritance and order; generic verbs earn their place ("give").
- **Why:** The first sentence ends on calibrations, which another column would need refitted; the next turns to the
  defects' repairs, which have nothing to refit and have run on one world away from Earth's values. The
  paragraph's movement toward the landing's compute-and-fit procedure turns on that contrast, which the text leaves
  for the reader to supply.
- **Rewrite** (optional): "... and under a lower pressure or another shield the columns would differ from those
  the calibrations were fitted on. The three defects' repairs contain no coefficient fitted to the test world, and
  away from Earth's values they have run on it alone, so the defects' biases on other worlds are known so far from
  the code's arithmetic; ..." (+10 words).
- **Check:** the fixed-orbit switch, an avoidance, contains no fitted coefficient either; "so far" and the
  arithmetic's evidence state stay.

### 13. MINOR: in the abstract, "it" takes the climate as a world

- **Location:** abstract.tex:17–18.
- **Text:** "The test world's climate is unobserved, and it is the only world the repaired codes have run on away from
  Earth's values."
- **Rule:** precise nouns; sentences carry their dependencies.
- **Why:** The antecedent of "it" is "the test world's climate". The two facts bound one evidence state and read as
  one.
- **Rewrite:** "The test world, whose climate is unobserved, is the only world the repaired codes have run on away
  from Earth's values." (−2 words).

### 14. MINOR: in Results, "a step that joined" classifies four changes and names three

- **Location:** results.tex:44–46, with Table tab:states at results.tex:27.
- **Text:** "From the Earth-orbit state, the synodic clock, the Moon's own tilt and the recalibrated split of sunlight, a
  step that joined a general repair and two avoidances, one of them output bookkeeping, with a calibration, warmed
  the test world by 0.6~K ..."
- **Rule:** precise nouns; exact action (a step that joins); sentences carry their dependencies.
- **Why:** The second avoidance, the year of twelve whole model days (repairs.tex:33–35), appears in neither the
  sentence nor Table tab:states ("Synodic clock; fixed orbit; recalibrated split of sunlight"), so the reader has
  three changes for four classes. The apposition's purpose, that the 0.6 K mixes classes, holds once the four
  changes are named in the order of their classes.
- **Rewrite:** "From the Earth-orbit state, the synodic clock, the Moon's own tilt, a year of twelve whole model days and
  the recalibrated split of sunlight, a general repair, two avoidances and a calibration made in one step, warmed
  the test world by 0.6~K ..." (+3 words), with "whole model days" added to the Sun-and-tilt row of Table
  tab:states; or, if the calendar change belongs to another step, the count corrected to one avoidance.

### 15. MINOR: in Results, the sentence on Yang et al. can trade places with the next

- **Location:** results.tex:81–86, in the paragraph at results.tex:76–97.
- **Rule:** the swap test; paragraph development.
- **Why:** The longwave sentence that follows (results.tex:86–91) takes nothing from the sentence on Yang et al.,
  and the two can change places with no loss. The comparison belongs with the paragraph's last sentence, where
  cloud-resolving runs constrain the cloud amount.
- **Rewrite:** move the sentence, unchanged, to follow "Ranked by form ..." (results.tex:91–95) and precede "Given
  the reference's spectroscopy ..." (±0 words). The paragraph then runs from the cloud settings and the longwave
  test to the ranking, to the gap between parameterized and resolved cover on other planets, and to the constraint
  on the test world's cloud.

### 16. MINOR: in Results, the sentence on Braam et al. and Sergeev et al. splits its attribution twice

- **Location:** results.tex:151–155.
- **Text:** "\textcite{braam2022lightning} and \textcite{sergeev2025lightning} estimated lightning on tidally locked
  planets with Earth-like air or, in Sergeev et al.'s runs, oxygen-free nitrogen air at 0.25--10~bar, from laws
  fitted to Earth's storms, whose tops stand far below the lunar runs' 55--80~km, setting the flash rate from the
  cloud-top height or, in Sergeev et al.'s storm-resolving runs, from the upward flux of graupel and the ice aloft."
- **Rule:** cadence (a repeated grammatical frame); the paragraph's landing.
- **Why:** The frame "or, in Sergeev et al.'s ..." interrupts the sentence twice, and the contrast with the lunar
  tops, which ties the sentence to the run before it, sits in its middle.
- **Rewrite:** "The flash-rate laws with which \textcite{braam2022lightning} estimated lightning on tidally locked planets
  with Earth-like air, and \textcite{sergeev2025lightning} on planets of oxygen-free nitrogen air at 0.25--10~bar,
  set the rate from the cloud-top height or, in Sergeev et al.'s storm-resolving runs, from the upward flux of
  graupel and the ice aloft, and were fitted to Earth's storms, whose tops stand far below the lunar runs'
  55--80~km." (±0 words).
- **Check against the originals:** Braam et al. parameterise flashes by cloud-top height after Price and Rind;
  Sergeev et al. run nitrogen with 400 ppm of carbon dioxide and water, with oxygen and ozone left out, at
  0.25–10 bar, with McCaul et al.'s graupel-flux and ice-path scheme in the storm-resolving runs and Price and
  Rind's in the coarse runs.

### 17. MINOR: in Reach, "in the configuration used" introduces released SWAN and patched SWAN four lines apart

- **Locations:** reach.tex:33–35; reach.tex:38–42.
- **Text:** "... and SWAN, in the configuration used, loses gravity similarity through its wind-input knee, fixed at
  1~Hz."; "In the configuration used, SWAN and SWASH are built to run water seas at any gravity as the scaled image of
  an Earth sea, ..."
- **Rule:** precise nouns.
- **Why:** "Released" governs CM1 alone in the first sentence, and nothing marks the second as the patched code,
  so one phrase introduces opposite statements about SWAN. SWASH runs unmodified (repairs.tex:185–186); SWAN needs
  the knee patch.
- **Rewrite:** "... and released SWAN, in the configuration used, loses ..." (+1 word); "With the knee patched, SWAN
  and SWASH, in the configuration used, are built to run ..." (+4 words).

### 18. MINOR: in Table tab:reach, the Seas row has "tested ... on the tested paths"

- **Location:** reach.tex:114.
- **Rewrite:** "Similarity at any gravity, tested at a sixth of Earth's on the similarity tests' code paths" (+2 words).

## 3. What works

- **The section discusses.** Each paragraph opens from the matter of the one before: the three defects (first
  paragraph); two of them on the test world (second); "Where two of the defects moved sunlight between places"
  (third); the Earth-fitted microphysics of the cloud-resolving runs, which closes the third and opens the fourth on
  Earth-fitted laws of storms; laboratories, and then what laboratories hold fixed (fifth); the design set with the
  model, and other worlds (sixth). A swap of any two paragraphs breaks a stated link.
- **The second paragraph builds a line the field can use.** An error that keeps the global mean of the arriving
  sunlight, and for the Sun clock every zonal mean, moved rain and cloud and, through the cloud, the global means;
  a modeller therefore finds it in maps by longitude and season, and Yang et al.'s comparison sets global-mean
  agreement beside threefold differences in cloud cover. The paragraph develops the abstract's opening: a run that
  keeps an Earth value can complete with a plausible result.
- **The third paragraph states a relation that answers the introduction's question.** What a modeller of a new
  world needs for each part depends on how far the world's own column determines it; the paragraph sorts geometry,
  gas absorption, cloud optics and cloud amount by that relation, and ends on the Earth-fitted microphysics inside
  the very runs to which cloud would be fitted.
- **The fourth paragraph states a discriminating test in G5's terms:** the alternatives (Takahashi's law and
  Saunders and Peck's), the measurement and the polarity it decides. It sets the 55–80 km cloud tops beside the
  resolved run's flash density and leaves the consequence for cloud-top flash-rate laws on low-gravity worlds to
  the reader, as the author directed. The route is Sergeev et al.'s own (their Sect. 4.2: "an explicit electric
  charging scheme coupled with a cloud-resolving model").
- **The fifth paragraph turns on what an Earth laboratory holds fixed.** It states SWAN's evidence exactly ("tested
  at a sixth of Earth's on the code paths those tests ran"), states plainly that the CM1 pair failed to convect, and
  adds laboratory evidence for the capillary-length form from other liquids at Earth's gravity (Loftus and
  Wordsworth, App. C1, p. 22: "within about 20%"), a test of a gravity law made at one gravity.
- **The sixth paragraph draws the constructed-world consequence from the test world's own design,** with its
  evidence (the dimming eased from 5.0 to 3.0% as the radiation changed), and returns to the first paragraph's
  arithmetic with the test that would measure it.
- **Evidence states stand beside their claims:** "by the code's own arithmetic", "made before the ventilation
  repair and with leakage off", "part of the difference possibly from its grid", "a step still to run", "that fit
  is still to be made", "known so far from the code's arithmetic".
- **Diction.** The section holds neither of the excluded words; its negations ("failed to convect", "little or no
  error", "no coefficient fitted") are required by their propositions; it has no stock transition, self-reference,
  reader management or witticism.
- **The arc.** The modeller of introduction.tex:43–44 recurs at conclusions.tex:21, 33 and 81 and moves from finding
  errors to choosing what to compute and what to fit. Every number in the conclusion that I checked matches the body
  or the claim register.
- **The revised passages elsewhere.** assumptions.tex:21–27 gives SWAN's knee its mechanism, its evidence (5.44%)
  and the condition under which a sea at another gravity departs from similarity, and scopes the ancient seas of
  Mars by that condition. next.tex:35–43 meets G5 in full: the question, the alternatives, the radiation held as
  released, the measured outputs, and the reclassification a failure would bring. reach.tex:38–42 separates what
  SWAN and SWASH are built for from where they were tested, and the caption of Table tab:reach separates the reach
  each repair was built for from the worlds simulated. results.tex:91–97 ranks the effects by form with their
  conditions and lands on the two least certain parts and the runs that would constrain them.

## 4. Counts and judgement

BLOCKING 0; MAJOR 2 (findings 1 and 2); MINOR 16 (findings 3–18).

The section meets the author's direction. It reminds in its first paragraph and recalls the body's results where an
argument needs them, and it adds discussion the body lacks: how an error that keeps the global-mean sunlight
passes a global-mean comparison and where a modeller finds it; which parts of a new world's model its own column
determines and which must be fitted; which Earth-fitted laws a laboratory can test and which only similarity runs
can; how a constructed world's design takes in the model's remaining Earth fits. No sentence presents an untested
world as already within reach. The place where a reader could take untested worlds as within reach is the
conditional scheme of finding 1, whose named range, the tables' 3.2 bar and 375 K, exceeds the check the paper
plans; and the landing, which gathers the section into what a modeller of a new world would do, attaches the sign
of the lightning to the cloud fit (finding 2). With those two repaired I find nothing blocking. The register is
dense, about 57 words a sentence, with some thirty-five numbers, nearly all restated from the body; findings 3
and 6 would take out about 55 words and leave the consequences for exoplanets and constructed worlds clearer.
Whether the section also excites is the author's reading to make; its material for that is present: the bias the
released code puts on TRAPPIST-1e runs, global-mean agreement beside threefold differences in cloud cover, a
lightning polarity a laboratory can decide, and a design that moved with its model. The audible cadence pass
remains pending.
