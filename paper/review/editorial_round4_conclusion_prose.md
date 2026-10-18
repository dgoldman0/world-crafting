# Editorial round 4: the closing section, read for prose and direction

## 1. Record

**Reviewer.** A fresh Claude subagent, Claude Opus 5.5 (model id `claude-opus-5-5[1m]`), given only the text,
the author's rules and the author's direction of 2026-10-17. Its reading stayed outside the earlier review
records and `paper/notes/`: in `paper/review/` it listed the file names once, to avoid overwriting one, and
wrote this record.

**Date.** 2026-10-17.

**Snapshot.** Commit `798f68b` (`798f68bc77842d568764de714175528b9fd410e7`), every file read with
`git show 798f68b:<path>`. Line numbers below are the snapshot's. Quotations drop the `\claim{}` markers and
join the source's line breaks; rewrites are LaTeX ready to paste.

**Files in scope (sha256 at 798f68b).**

| File | Scope | sha256 |
|---|---|---|
| `paper/sections/conclusions.tex` | whole section | `d94c7cb2f7fa69c51c124d0c196a13a66e5cd87f9ab9aefa85e15f92149fbd3b` |
| `paper/sections/abstract.tex` | whole abstract | `67b5fcba63d5694ddd4eba67cacd70fdf7d1f6d03c19e7a5ec2a8a32e6a92c4c` |
| `paper/sections/results.tex` | lines 48–53, 81–85, 90–93 | `4c8204187de042831cdb17cf6335f56efd7cad1a4e568708a16769e5442810eb` |
| `paper/sections/reach.tex` | lines 38–40, 42–43, 45–58, 88–91 | `43a79acef7ec8ed0309f66b004c503490bd22b1530b237ff620de4a13a679c11` |
| `paper/sections/next.tex` | lines 35–42 | `074e611059513edd423b2e5754977d438b0ab1da6978a391bd70bfe0d200acea` |

**Rule files, read in full before the paper.**

| File | sha256 |
|---|---|
| `AGENTS.md` (snapshot; identical to the working copy) | `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32` |
| Terluna `ensemble/planning/Open_Moon_Editorial_Charter_control-01.md` (Terluna at `f03b839`) | `aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0` |
| Terluna `ensemble/planning/source_controls/STYLE_NOTES.md` | `659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46` |
| Terluna `ensemble/planning/source_controls/Jewish_Papers_Updated_Style_Notes.md` | `18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab` |
| Terluna `ensemble/planning/source_controls/Agent_Working_State_Editorial_Gates.md` | `553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464` |

The charter's hash matches the one AGENTS.md names (`aac4a4f2…0b0`).

**Context read.**

| File at 798f68b | How read | sha256 |
|---|---|---|
| `paper/sections/introduction.tex` | in full, before the conclusion | `b8325d641b56d6da32cffbcaa143e26461495322235c2de3b0709402f1ef5b72` |
| `paper/sections/results.tex`, `reach.tex`, `next.tex` | in full | as above |
| `paper/sections/verification.tex` | in full | `4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00` |
| `paper/sections/worlds.tex` | in full, to check the conclusion's figures | `453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112` |
| `paper/sections/repairs.tex` | in full, to check the conclusion's figures | `bb1d22c01616fdaf454280acded56316b7995af2a8fc3bb5a255af52c92e793c` |
| `paper/sections/assumptions.tex` | lines 1–110 | `fef76870ffb4f1ddbaa79de5dec39ec1d141a845bdb247171100652e10b96a77` |
| `paper/main.tex` | section order | `7ef8255c7fa8d14e9d0d61406d1f919be6dff5251b47fb3598aba9c913a8495c` |
| `paper/sources/manifest.json` | entries for vincendon2010spherical, yang2023cloud, way2018climates, braam2022lightning, sergeev2025lightning, banfield2015winds | `334f5973fe6339026237ca7953369c34e5f4a1cce89ef935bccd7ccfa76a66a4` |
| `paper/claims.json` | entries H04, H23, V04, W03, W06 | `8bb7e9e6cf2010e75be6f6890357c0238798bc27ab9c2b7412cb61ab8507e8e1` |
| `models/swan/README.md` | the knee patch and the configuration table | `3699e5e564fa484d36b1aa6c91434ab8119beeb3a50de8f72625db97476f8d3f` |
| `git diff e89a394 798f68b` | results.tex and reach.tex, to see which scoped sentences changed | — |

**Sources checked against the conclusion's claims.** Text layers of the archived originals in
`paper/sources/originals/` (each sha256 matches its manifest entry), searched and read at the passages
named; full readings remain the work of the source records.

| Original | sha256 | Passages read |
|---|---|---|
| Vincendon and Langevin (2010), arXiv v1 | `afcdf418a60ce367c8b16c12d68c1bac36ea2fd8e0013498ea3553c0cbd8a7e9` | abstract; Sect. 1; Sect. 3.3 |
| Sergeev et al. (2025), arXiv v2 | `b2c3352f4ad065bd894341eb76741ff541b1bf4c4824612ae7e6404bd373c6df` | Sect. 2.2, Table 1; Sect. 4.2 |
| Braam et al. (2022), arXiv v1 | `26486cfc19cb2185ca8f98a22bcbadf40a526afed1f8b3d460154915b58cf8c7` | abstract; Sect. 2 on lightning |
| Banfield et al. (2015) | `252db567cd32131d949261413bed1a948a4d2839161f6faeb206851eb9cda325` | Sect. 3.2.2; the set-up of the Mars basin runs |
| Way et al. (2018), arXiv v2 | `476e3e967e5d7eeafea1f386fc801851106365653bd3d9132c5821edb7164820` | abstract; Sect. 2.1; Sect. 4 |

**Method.** Each paragraph was read whole, then sentence by sentence, under the charter's ten passes
(section 11) and the rules of AGENTS.md, "Writing"; the abstract, the introduction and the conclusion were
then read as one arc (pass 10). The cadence reading was silent; the charter keeps an audible reading of the
conclusion as a requirement, and that reading remains pending. `paper/tools/lint.py` (sha256
`27f9b47a1f4837583b75eb750e302531f3e07a44e452983dd9ddce2b35657367`) was run on snapshot copies in the session scratchpad, as screening only: in the conclusion
and the abstract it found the excluded words "not" and "rather than" absent, two negations for reading ("no coefficient fitted",
"little or no error", both required by their propositions), one possible empty action ("conditions
laboratories reach", accepted) and sixteen universal words, each checked below; in the scoped passages of
Results, Reach and Next steps its hits are the noun "reach". Sentence lengths were counted by script.
The only file written in the repository is this record.

## 2. Findings

Severity: BLOCKING breaks the author's direction or a rule as the author would reject it; MAJOR is a clear
breach; MINOR is polish. Each rewrite was checked against the paper's own figures and, where named, the
archived source, and against the writing rules.

### 1. BLOCKING — a class of GCMs characterised from one comparison

- **Location.** `results.tex:81–85`.
- **Text.**
  ```text
  GCMs with diagnostic cloud schemes differ widely from cloud-permitting runs on tidally locked planets: on
  TRAPPIST-1e and K2-72e, CAM3 and ExoCAM, whose cover follows relative humidity, stability and large-scale
  ascent, covered 94.8 and 81.7\% and 90.4 and 97.4\% of the sky, against 26.9 and 41.1\% in a quasi-global
  cloud-permitting model, while the three models' global-mean surface temperatures and albedos came out
  broadly alike \autocite{yang2023cloud}.
  ```
- **Rule.** Claims stay within their evidence: a statement about a field says what the cited works did,
  scoped to them; AGENTS.md lists the same failure among the author's rejected examples ("A whole field
  characterised from four studies"). Also inheritance and the swap test (G1, G3).
- **Why.** The opening clause characterises a class of models from two GCMs in one study. The project's
  own source records hold a study with the opposite direction of effect (the manifest's note on
  sergeev2024impact: explicit convection raises low cloud and albedo), so the class claim is wider than
  even the project's own literature supports. The revision in 798f68b replaced "GCM cloud schemes of this kind ... as
  well", which tied the comparison to PlaSim's cloud, with the class claim; the sentence now stands between
  two sensitivity results with its relation to them unwritten, and it could move after the longwave sentence
  without loss. The figures "94.8 and 81.7\% and 90.4 and 97.4\%" leave the reader to work out that each pair
  runs by planet within one model. From "whose cover follows" to "came out broadly alike" the clause recurs
  almost word for word at `conclusions.tex:23–26`.
- **Rewrite** (about 8 words longer):
  ```text
  In the comparison of \textcite{yang2023cloud}, two GCMs that diagnose their cover, as PlaSim does, covered
  far more of the sky than a quasi-global cloud-permitting model on two tidally locked planets: on TRAPPIST-1e
  and K2-72e, CAM3 covered 94.8 and 81.7\% and ExoCAM 90.4 and 97.4\%, their cover following relative
  humidity, stability and large-scale ascent, against 26.9 and 41.1\% in the cloud-permitting model, while the
  three models' global-mean surface temperatures and albedos came out broadly alike.
  ```
- **Check.** Figures and their pairing follow the manifest's locator for yang2023cloud (arXiv v1 p. 3:
  "26.9% and 41.1% for TRAPPIST-1e and K2-72e"; "94.8% and 81.7% in CAM3 and 90.4% and 97.4% in ExoCAM").
  PlaSim diagnoses its clouds (`introduction.tex:57–58`); the rewrite claims only that PlaSim, like the two
  GCMs, diagnoses its cover, and leaves their predictors to the clause that names CAM3's and ExoCAM's. Optional, about 12 words: the manifest notes that the cloud-permitting model counts cloud
  by a condensate threshold, unlike the GCMs, and a clause saying so would bound the comparison (G5).

### 2. MAJOR — the released SWAN's error extended to every sea under another gravity

- **Location.** `conclusions.tex:59–63`.
- **Text.**
  ```text
  Patched, SWAN reproduces a sixfold gravity scaling of an Earth sea to 0.3\% in wave height, where the
  released code missed it by 5.4\% and departs from it on any sea under another gravity, the ancient seas of
  Mars among them; the patch, built to keep the scaling at any gravity, has been tested at a sixth of Earth's
  on the code paths those tests ran, and Earth's empirical laws of drag, wind input and breaking remain
  uncertain at each such sea's ratio of air to water density.
  ```
- **Rule.** Technical meaning survives editing (G5); claims stay within their evidence; the author's
  direction, which rejects results asserted on worlds the work has left untested.
- **Why.** The fixed 1 Hz bend lies in AGROW, SWAN's linear growth term, which runs only when AGROW is set
  (`models/swan/README.md`, 01-agrow-knee.patch, "Switch and default"). A run under another gravity departs
  from the scaled image only where its band extends into the frequencies between the stock bend at 1 Hz and
  the scaled bend at g/g_E Hz, as the lunar band of 0.005–0.497 Hz extends past 0.166 Hz. The 5.44% is the
  largest difference in the similarity comparison (README, "Verification"), and at lunar gravity the stock
  and patched 48-hour heights on the 100 km strip differ by at most 0.11% (README, "Effect at lunar
  gravity"), so the heights of developed seas differ far less than the headline figure. The body names the mechanism, "its
  linear wind input" (`assumptions.tex:22`), and the configuration, "in the configuration used"
  (`reach.tex:34`); the conclusion drops both, and "any sea under another gravity, the ancient seas of Mars
  among them" then asserts a result on seas outside every run the work has made. Banfield et al.'s archived
  text describes SWAN with Janssen's wind input, run from flat calm to equilibrium, and its account of the
  source terms leaves AGROW and any linear term unnamed, so whether their runs used the bent term at all
  stays open in the record. "Remain uncertain" leaves the property unnamed, and "missed" (past) stands beside
  "reproduces" (present) for the same test.
- **Rewrite** (preferred, about 15 words shorter):
  ```text
  Patched, SWAN reproduces a sixfold gravity scaling of an Earth sea to 0.3\% in wave height, where the
  released code, whose linear wind input bends at a fixed 1~Hz, misses it by up to 5.4\%; the patch, built
  to keep the scaling at any gravity, has been tested at a sixth of Earth's on the code paths those tests
  ran, and Earth's empirical laws of drag, wind input and breaking keep coefficients fitted at Earth's ratio
  of air to water density.
  ```
  If the author keeps the natural-world clause, it needs both conditions, and Banfield et al.'s configuration
  needs checking first: "..., misses it by up to 5.4\%, and under another gravity departs from it in any run
  of that input whose band extends between the fixed and the scaled bend; ...".
- **Check.** "Linear wind input" is the body's term (`assumptions.tex:22`); "up to" follows the README's
  "Largest differences" and claims.json V04; the README records that AGROW's coefficient "carries Earth's
  air–water density ratio implicitly" and lists Komen's 0.25 and 28 among the Earth fits used as shipped. The same
  generalisation stands at `assumptions.tex:22–26`, outside this round's scope, and needs the same repair.

### 3. MAJOR — the constructed-world passage restates the premise and an implication already plain

- **Location.** `conclusions.tex:67–72`.
- **Text.**
  ```text
  By one design's own models, a shield in space that removes the ultraviolet heating the upper air would hold
  the Moon's Earth-like air to losses of 0.6--1.4~kg\,s$^{-1}$ over a solar cycle, rates at which removing it
  would take 60 to 150 billion years, on a body whose escape velocity let its natural atmosphere go, so that
  gravity, column and the air's height against the radius depart from Earth's together, and the Moon's tidal
  lock adds a 29.53-day day. A designer who lowers the pressure or changes the shield moves the columns off
  those the calibrations were fitted on, and would need the calibrations refitted.
  ```
- **Rule.** The author's direction: findings drawn out for constructed worlds "without explaining the
  obvious", "real substance of discussion", a conclusion that reminds and excites. Write for the expert
  (restating an implication the evidence already makes plain). Conclusions gather the developed lines into a
  new relation. Exact action ("whose escape velocity let its natural atmosphere go"; "the Moon's tidal lock
  adds a 29.53-day day", where the doubled "day" also jars).
- **Why.** These two sentences are the section's only passage on constructed worlds. The first gives the
  design's premise in the numbers of the introduction (lines 21–25) and the words of the abstract (lines
  4–6), and the four departures it ends on are the ones the conclusion's own first sentence lists. The second
  states the consequence that the definition of a calibration already contains (`introduction.tex:79–80`;
  `reach.tex:62–64`; `conclusions.tex:40–41`). The paper holds a stronger relation for constructed worlds:
  the shield's dimming was set with the calibrated GCM, so the Earth fits that remain in the model enter the
  design itself (`worlds.tex:31–34`; `results.tex:56–59`; `next.tex:9–13`, 23). Stated for the test world,
  it leaves the implication for other constructed worlds implicit, as the author asked.
- **Rewrite** (about the same length):
  ```text
  Part of the test world's design was set with the model, and so with the Earth fits that remain in it: the
  shield's dimming was chosen so that the calibrated GCM settles at the design's 295~K, and holding that
  temperature on the corrected curved-air terms and the gas bands took easing it from 5.0 to 3.0\%. A
  longwave correction refitted at the settled state, which with the ice optics warmed the design case by
  11.5~K in its test, or cloud fitted to cloud-resolving runs, whose Earth-tuned settings moved the climate by
  up to about 6~K, could move the dimming again, and a lower pressure or another shield would move the
  columns off those the calibrations were fitted on.
  ```
- **Check.** Each figure keeps its condition: the dimming and 295 K (`worlds.tex:31–34`), the easing from
  5.0 to 3.0% on the corrected terms and the bands (`results.tex:56–59`), the 11.5 K as a joint effect with
  the ice optics (`results.tex:85–88`), the cloud settings' "up to about 6 K" (abstract, `results.tex:93`),
  and "could" from `next.tex:12–13` and 23. The design's retention figures stay in the introduction. If the
  author wants the design recalled here, one clause recalls it and leaves the numbers to the introduction: "Part of the test
  world's design, a shield in space holding Earth-like air under a sixth of Earth's gravity, was set with
  the model, ...".

### 4. MAJOR — the natural-planet sentence repeats Next steps

- **Location.** `conclusions.tex:72–76`.
- **Text.**
  ```text
  On natural planets the three defects' biases are known so far from the code's arithmetic, since away from
  Earth's values every change made for the test world has run on it alone; released and repaired ExoPlaSim on
  Earth-air planets at Earth's insolation, rotating once in 16 and 64 days, two of the sidereal periods at
  which \textcite{way2018climates} ran ROCKE-3D, would measure those biases in the climate of worlds that other
  studies model and test the Sun-clock and convective-cover repairs there.
  ```
- **Rule.** Conclusions (reciting excluded); the redundancy pass; the swap test.
- **Why.** From "released and repaired ExoPlaSim" to "repairs there" the sentence restates `next.tex:36–40`
  almost word for word: the same planets, insolation, rotations, ROCKE-3D periods and outcomes. The charter
  has a companion's conclusion land on the next consequential work, so naming the test belongs here, while
  its design belongs to Next steps. Its place in the paragraph is also loose: it could follow
  `conclusions.tex:26`, where the defects' effects end, without loss. Its opening, "On natural planets",
  sets it against the constructed world before it, and that contrast works once the constructed-world
  sentences state a consequence (finding 3).
- **Rewrite** (about 25 words shorter):
  ```text
  On natural planets the three defects' biases are known so far from the code's arithmetic, since away from
  Earth's values every change made for the test world has run on it alone; released and repaired ExoPlaSim on
  Earth-air planets rotating once in 16 and 64 days, as in two of the ROCKE-3D runs of
  \textcite{way2018climates}, would measure them on worlds that other studies model.
  ```

### 5. MAJOR — the adapted SWAN's reach stated as if for every configuration

- **Location.** `reach.tex:38–40`.
- **Text.**
  ```text
  SWAN and SWASH are built to run water seas at any gravity as the scaled image of an Earth sea, and have been
  tested at a sixth of Earth's gravity, with Earth's empirical laws.
  ```
- **Rule.** Claims stay within their evidence; technical meaning (G5).
- **Why.** Three sentences earlier the paragraph bounds the released code to "the configuration used"
  (lines 34–35), and this sentence, on the adapted code, drops the bound. The SWAN record lists options that
  hold Earth's gravity as a number, ST6 with its FAN or ECMWF drag routines and the exact quadruplets, and
  records that the runs avoided them (`models/swan/README.md`, configuration table, "Avoided options"); as
  written, the sentence extends the scaled image to those options as well. Verification bounds the
  similarity to "the code paths these tests ran" (`verification.tex:48–51`).
- **Rewrite** (4 words longer):
  ```text
  In the configuration used, SWAN and SWASH are built to run water seas at any gravity as the scaled image of
  an Earth sea, and have been tested at a sixth of Earth's gravity, with Earth's empirical laws.
  ```
  Optional, about 14 words more, naming the avoided options: "...; SWAN's ST6 drag routines and exact
  quadruplets, which hold Earth's gravity as a number, stayed unused." The "Seas" row of Table tab:reach
  ("Similarity at any gravity") makes the same claim under the caption's "the reach each repair was built
  for"; the table body lies outside this round's scope.

### 6. MINOR — "a comparison ... can pass it", and the evidence behind the colon

- **Location.** `conclusions.tex:21–26`.
- **Text.**
  ```text
  A modeller finds such an error in maps of sunlight by longitude and of rain by season, and a comparison of
  models by their global means can pass it: on two tidally locked planets, the quasi-global cloud-permitting
  runs of \textcite{yang2023cloud} covered 27 and 41\% of the sky with cloud and two GCMs whose cover follows
  relative humidity, stability and large-scale ascent covered 82--97\%, most of the difference on the night
  side and at high latitudes of the day side, while the three models' global-mean surface temperatures and
  albedos came out broadly alike.
  ```
- **Rule.** Exact action; claims stay within their evidence; redundancy.
- **Why.** "A comparison ... can pass it" gives the act to an abstraction, where the modeller who compares
  is the agent. After the colon, Yang et al.'s comparison stands as the instance of a comparison passing
  "such an error"; it shows global means agreeing across models that place cloud differently, a parallel case, while
  the direct evidence, the test world's 0.9 K, stands in the sentence before. The last clause repeats
  `results.tex:83–85`.
- **Rewrite** (about the same length):
  ```text
  A modeller finds such an error in maps of sunlight by longitude and of rain by season and can miss it in
  global means: on the test world the global-mean surface temperature moved 0.9~K, and on two tidally locked
  planets three models whose cloud cover differed widely came out broadly alike in global-mean surface
  temperature and albedo, the quasi-global cloud-permitting runs of \textcite{yang2023cloud} covering 27 and
  41\% of the sky and two GCMs whose cover follows relative humidity, stability and large-scale ascent
  82--97\%, most of the difference on the night side and at high latitudes of the day side.
  ```
- **Check.** The location of the difference (night side, high latitudes of the day side) rests on the
  manifest's note for yang2023cloud, whose locators quote the cover figures alone; a locator for the
  location would admit it under G6.

### 7. MINOR — the turn from defects to fits is unwritten

- **Location.** `conclusions.tex:28`.
- **Text.** "Changes to the parts fitted to Earth's atmosphere moved the test world's global-mean surface
  temperature furthest:"
- **Rule.** Transitions come from the subject matter; inheritance.
- **Why.** The paragraph turns from defects that moved sunlight between places to fits that moved the global
  mean, and that comparison is the turn's content; written into the opening, it lets the paragraph receive
  the one before.
- **Rewrite** (7 words longer): "Where two of the defects moved sunlight between places, changes to the parts
  fitted to Earth's atmosphere moved the test world's global-mean surface temperature furthest:"
- **Check.** "Two of the defects" leaves the third, the convective-cover unit, among the general repairs
  measured at 1.6–2.5 K (`results.tex:42–44`).

### 8. MINOR — a 100-word sentence holding four items, with the Titan case at its end

- **Location.** `conclusions.tex:32–38`.
- **Text.**
  ```text
  The radiative geometry of tall air is computed from that column, as the curved-air table was for the test
  world, whose air in curved shells loses a net 5.8~W\,m$^{-2}$ against the same clear column taken flat with
  a pseudo-spherical direct beam, while the dynamics keep a thin shell and constant gravity; Titan's haze, with
  a scale height of about 80~km, stands a few hundredths of its radius tall, as the test world's air does,
  and plane-parallel aerosol codes for Titan's surface hold to about 65\textdegree\ from the zenith
  \autocite{vincendon2010spherical}, although Titan's nitrogen--methane radiation lies outside the adapted
  models.
  ```
- **Rule.** Sentences carry their dependencies (a long sentence holding an inventory still fails); exact
  nouns.
- **Why.** The sentence contains the general method, the test world's instance with its basis of
  comparison, the dynamics' limit, and Titan with its bound; the Titan case, the paragraph's implicit
  natural-world instance, comes after a semicolon in the sentence's last third. "Plane-parallel aerosol
  codes for Titan's surface" compresses Vincendon and Langevin's "radiative transfer codes widely used in
  surface–atmosphere separation problems" (arXiv v1, Sect. 1) into a phrase that reads as codes of the
  surface.
- **Rewrite** (one full stop added; same length):
  ```text
  The radiative geometry of tall air is computed from that column, as the curved-air table was for the test
  world, whose air in curved shells loses a net 5.8~W\,m$^{-2}$ against the same clear column taken flat with
  a pseudo-spherical direct beam, while the dynamics keep a thin shell and constant gravity. Titan's haze,
  with a scale height of about 80~km, stands a few hundredths of its radius tall, as the test world's air
  does, and the plane-parallel codes that separate Titan's surface from its haze hold to about 65\textdegree\
  from the zenith \autocite{vincendon2010spherical}, although Titan's nitrogen--methane radiation lies
  outside the adapted models.
  ```
- **Check.** The archived original gives the haze's scale height as 80 ± 10 km (abstract) and the
  plane-parallel limit as "typically less than 80° for Mars and 65° for Titan" (Sect. 1).

### 9. MINOR — "apart from any one world", and the charging-law sentence's order

- **Location.** `conclusions.tex:44–49`.
- **Text.** "Some of those Earth-fitted laws can be tested apart from any one world, in laboratories on Earth
  or in runs at other gravities." and "In two windows of an earlier electrified run, made before the
  ventilation repair and with leakage off, the test world's storms took opposite polarities under Takahashi's
  charging law and Saunders and Peck's, which disagree on the sign that rimed ice takes in little cloud water;
  ..."
- **Rule.** Exact nouns; inheritance and order.
- **Why.** "Apart from any one world" leaves the reader to supply its sense, independence from the world
  modelled, and the laboratories the sentence names stand on Earth. The second sentence opens on the run's
  windows and names the laws it inherits from the first only in its second half; opening on the laws puts
  law, consequence in the test world's storms and deciding measurement in their order.
- **Rewrite** (same lengths):
  ```text
  Some of those Earth-fitted laws can be tested independently of the world modelled, in laboratories on Earth
  or in runs at other gravities. Takahashi's charging law and Saunders and Peck's disagree on the sign that
  rimed ice takes in little cloud water, and in two windows of an earlier electrified run, made before the
  ventilation repair and with leakage off, the test world's storms took opposite polarities under the two; a
  measurement of that sign at 4--8~m\,s$^{-1}$ in 0.02--0.2~g\,m$^{-3}$ of cloud water between $-5$ and
  $-16$\,\textdegree C, conditions laboratories reach, would decide the polarity of the lightning.
  ```

### 10. MINOR — the flash density set beside the cloud tops, their relation unwritten

- **Location.** `conclusions.tex:52–56`.
- **Text.**
  ```text
  At a sixth of Earth's gravity the cloud tops of six Morrison runs rose to 55--80~km, far above the storms
  the cloud-top law was fitted on, while the main electrified run, forced from the Earth-orbit state, flashed
  at about a hundredth of Earth's average density, part of the difference possibly from its grid; electrified
  storms resolved at other gravities, computed with the same laboratory charging laws, could test those
  flash-rate laws, along the route Sergeev et al. propose of explicit charging in cloud-resolving runs.
  ```
- **Rule.** Sentences carry their dependencies; exact nouns.
- **Why.** "While" sets the run's flash density beside the cloud-top heights and leaves out what joins
  them: the cited laws set the flash rate from cloud-top height or graupel, and the run computes its flashes
  from resolved charge, which is why runs of its kind could test the laws. "Earth's average density" reads
  first as the air's density. At 85 words the sentence holds the observation, the result with its grid
  caveat, and the proposal.
- **Rewrite** (two sentences, about 5 words longer):
  ```text
  At a sixth of Earth's gravity the cloud tops of six Morrison runs rose to 55--80~km, far above the storms
  the cloud-top law was fitted on, and the main electrified run, forced from the Earth-orbit state and
  computing its flashes from resolved charge, flashed at about a hundredth of Earth's average flash density,
  part of the difference possibly from its grid. Electrified storms resolved at other gravities, computed
  with the same laboratory charging laws, could test those flash-rate laws, along the route Sergeev et al.
  propose of explicit charging in cloud-resolving runs.
  ```
- **Check.** Sergeev et al. (2025), Sect. 4.2: "A possible route towards a more quantitative result is to
  use an explicit electric charging scheme coupled with a cloud-resolving model (e.g., Fierro et al. 2013)";
  their storm-resolving runs use McCaul et al.'s graupel-flux scheme and their coarse runs Price and Rind's
  cloud-top law (Table 1), and Braam et al. (2022) set flashes from cloud-top height (abstract), as the
  preceding sentence says. The flash density is that of `results.tex:144–146`.

### 11. MINOR — the opening paragraph's gapping, coordination and explicit natural-planet clause

- **Location.** `conclusions.tex:3–9`.
- **Text.** "... and the radiation's fits calibrations to a line-by-line model. Three of the defects, all in
  ExoPlaSim, produce little or no error at Earth's values and an error that grows as a world's rotation slows
  or its day or tilt departs from Earth's, and by the code's own arithmetic they bias ExoPlaSim's runs of
  natural planets that meet their conditions."
- **Rule.** Coordination joins only propositions of equal weight; the direction (natural-world implications
  stated implicitly); claims stay within their evidence.
- **Why.** The gapped "the radiation's fits calibrations" puts two nouns side by side and is hard to parse
  (also `abstract.tex:13`). In the second sentence "and ... and" coordinates the defects' profile with its
  consequence. The final clause states outright what the third sentence's TRAPPIST-1e and slow-rotator
  figures show; moving "by the code's own arithmetic" into the third sentence keeps the evidence state and
  leaves the implication to the figures. The orbit default discards a configured eccentricity as well as a
  tilt (claims.json W06).
- **Rewrite** (about 10 words shorter):
  ```text
  ... geometry took a method computed from the world's own column, and the radiation's fits took calibrations
  to a line-by-line model. Three of the defects, all in ExoPlaSim, produce little or no error at Earth's
  values and an error that grows as a world's rotation slows or its day, tilt or eccentricity departs from
  Earth's. By the code's own arithmetic, the convective-cover unit adds about 0.23 to the convective cover of
  a synchronous run of TRAPPIST-1e, and the Sun clock sets the Sun back about 33\textdegree\ each model day in
  a non-synchronous run, on the default solar geometry, of any planet rotating more slowly than once in 20
  days.
  ```

### 12. MINOR — the landing's two bounds can name the world they come from

- **Location.** `conclusions.tex:76–80`.
- **Text.** "For a new world whose gases, pressures and temperatures the line-by-line spectroscopy covers, and
  whose air stands within a few hundredths of its radius, the radiative geometry can be computed from the
  world's own column and, once a scheme is built from that spectroscopy, the gas absorption as well, ..."
- **Rule.** Claims stay within their evidence; the arc (pass 10).
- **Why.** The landing works (see section 3). Two phrases can state their evidence more exactly: "can be
  computed from the world's own column" names a capability exercised once, on the test world's column, and
  "within a few hundredths of its radius" admits taller air than the 0.030 that Reach names as the bound
  (`reach.tex:79–80`, "up to a few hundredths of the radius, the test world's").
- **Rewrite** (about 11 words longer):
  ```text
  For a new world whose gases, pressures and temperatures the line-by-line spectroscopy covers, and whose
  scale height is at most three hundredths of its radius, the test world's ratio, the radiative geometry can
  be computed from the world's own column as it was from the test world's and, once a scheme is built from
  that spectroscopy, the gas absorption as well, while cloud remains to be calibrated for that world against
  cloud-resolving runs whose microphysics can be tested in laboratories and by similarity runs.
  ```
- **Check.** Scale height over radius 0.030 (`worlds.tex:59`). The landing repeats two phrases of
  `conclusions.tex:38–41` ("whose gases, pressures and temperatures that spectroscopy covers"; cloud fitted
  to cloud-resolving runs of that world); a gathering may repeat its terms, and trimming either place is
  optional.

### 13. MINOR — cadence, read silently

- **Location.** The whole section.
- **Rule.** G3 cadence: vary lengths, openings and stress; short sentences as hinges and landings.
- **Why.** The section has 1,333 words in 23 sentences, a mean of 58. Eleven sentences run to 70 words or
  more, among them the landings of the second (92), fourth (85) and sixth (72) paragraphs; the five
  sentences of 28 words or fewer open or hinge the second to sixth paragraphs. In the silent reading the
  stress falls late in most sentences, after three to five dependent clauses, and the reader reaches each
  landing holding several open dependencies. The rewrites of findings 3, 4, 8 and 10 shorten four of the
  eleven.
- **Rewrite.** Those of findings 3, 4, 8 and 10. The audible reading the charter requires for conclusions
  remains pending.

### 14. MINOR — "its clouds returning"

- **Location.** `results.tex:51–53`.
- **Text.** "... cooled it by 0.65~K, its clouds returning in the first year 3.5 of the clear sky's
  5.4~W\,m$^{-2}$ loss under those terms."
- **Rule.** Exact action.
- **Why.** "Returning" gives the clouds a figurative act; the operation is a compensation in the cloud's
  radiative effect.
- **Rewrite** (same length): "... cooled it by 0.65~K, its clouds offsetting in the first year 3.5 of the
  clear sky's 5.4~W\,m$^{-2}$ loss under those terms."

### 15. MINOR — "Ranked by form" ranks three of the four forms

- **Location.** `results.tex:90–93`.
- **Text.** "Ranked by form, the effects on the test world grow from the units and constants, whose single
  general repairs moved the global mean by 1.6--2.5~K, to the fits: ..."
- **Rule.** Claims stay within their evidence; exact wording.
- **Why.** Geometry, one of the four forms, drops out of the ranking: the curved-air terms on the table's
  first channels moved the global mean by 0.65 K (`results.tex:51–53`), below the units and constants, so a
  sentence that reads as a complete ranking covers three forms. "Single general repairs" can read as one
  repair each.
- **Rewrite** (about 17 words longer):
  ```text
  Ranked by form, the effects on the test world grow from the geometry, whose curved-air terms on the table's
  first channels moved the global mean by 0.65~K, and the units and constants, whose general repairs measured
  singly moved it by 1.6--2.5~K, to the fits: ...
  ```
  If the author keeps geometry out because its single measurement ran on the defective first channels, a
  clause saying so serves the same end.

### 16. MINOR — "the middle column" of a four-column table

- **Location.** `reach.tex:89–90`, caption of Table tab:reach.
- **Text.** "The middle column gives the reach each repair was built for;"
- **Rule.** Exact nouns.
- **Why.** Of four columns, two stand in the middle; the column meant is the third, "Represented by the
  adapted models".
- **Rewrite.** "The third column gives the reach each repair was built for;"

### 17. MINOR — the proposed ExoPlaSim test can name its orbit

- **Location.** `next.tex:36–38`.
- **Text.** "Released and repaired ExoPlaSim on Earth-air planets at Earth's insolation, rotating once in 16
  and 64 days, two of the sidereal periods of the ROCKE-3D runs of \textcite{way2018climates}, with the
  released radiation, fitted on columns like theirs, would measure the three defects' effect ..."
- **Rule.** G5: a proposed study names the fixed assumptions its discrimination depends on.
- **Why.** The orbit default acts only where the configured orbit differs from Earth's. Way et al. ran at
  zero obliquity and eccentricity (arXiv v2, Sect. 2.1: "Planetary obliquity and eccentricity are zero"), so
  runs that copy their set-up measure all three defects, while runs at Earth's orbit measure two; naming the
  setting makes the third measurable by design.
- **Rewrite** (5 words longer): "Released and repaired ExoPlaSim on Earth-air planets at Earth's insolation
  and zero obliquity and eccentricity, rotating once in 16 and 64 days, ..."

### 18. MINOR — the abstract gives design reach three times and the tested reach nowhere

- **Location.** `abstract.tex:12–19`.
- **Text.** "Constants and units of time took general repairs built to hold on other worlds, geometry a method
  computed for each world's column, ..." and "On the test world the two general repairs measured singly moved
  ..."
- **Rule.** The arc (pass 10); the author's direction against suggesting that the work extends to untested
  worlds; evidence states kept distinct.
- **Why.** The abstract names the repairs' reach to other worlds three times, each by design ("built to hold
  on other worlds", "computed for each world's column", "physics computed for each world's air"), and nowhere
  gives the evidence state that the introduction (line 84) and the conclusion (line 73) give: away from
  Earth's values, every repair has run on the test world alone. Each phrase is accurate, and a reader who
  meets the three together in the paper's most-read paragraph can take design reach for tested reach.
- **Rewrite** (12 words longer): "On the test world, the only world the repaired codes have run on away from
  Earth's values, the two general repairs measured singly moved ..."

### 19. MINOR — four phrases in the abstract

- **Location.** `abstract.tex:10–17`.
- **Text.** "three of the defects, exact or nearly so at Earth's values," / "and the radiation's fits calibrations
  to an in-house line-by-line model" / "and the calibrations test it against the line-by-line model." /
  "where the released code misses it by 5.4\%; the lunar climate is unobserved."
- **Rule.** Exact nouns and action; coordination; technical meaning.
- **Why.** "Exact" describes a result, while a defect is code; the introduction and the conclusion say
  "little or no error". The gapped "fits calibrations" puts two nouns side by side. A calibration fits the
  code to the reference, and its residuals on the columns fitted and a few beyond test it
  (`verification.tex:9–11`). The 5.4% is the comparison's largest difference. The semicolon joins the
  similarity result to the climate's evidence state, which bounds every check before it and every climate
  number after it, and which works better as a short sentence of its own.
- **Rewrite** (about 13 words longer in all):
  ```text
  three of the defects, with little or no error at Earth's values, ...
  ... and the radiation's fits took calibrations to an in-house line-by-line model ...
  ... and the calibrations' residuals, on the columns fitted and a few beyond, test it against the
  line-by-line model.
  ... where the released code misses it by up to 5.4\%. The lunar climate itself is unobserved.
  ```
  With finding 18, the short sentence leads into "On the test world, the only world ...".

## 3. What works

- **The section's governing relation.** "What a modeller of a new world needs for each part depends on how
  far the world's own column determines it" (`conclusions.tex:31–32`) turns the finding that the kind of
  repair followed the form of the Earth value into a criterion a modeller of any Earth-like world can apply.
  The paragraph develops it in order, geometry computed from the column, gas absorption computable once a
  scheme exists, cloud calibrated against cloud-resolving runs, their microphysics fitted to Earth, and its
  last term is the one the next paragraph takes up.
- **Transitions from the subject.** "Earth-fitted microphysics of their own" leads to "Some of those
  Earth-fitted laws can be tested ... in laboratories on Earth or in runs at other gravities", and that to
  "Gravity stays fixed in a wave tank or a cloud laboratory on Earth, so a model's dependence on it is tested
  by similarity runs". Swapped, the third, fourth and fifth paragraphs lose these links, the swap test's
  mark of a written relation.
- **A consequence for the field, drawn from the test world's numbers.** The second paragraph shows that two
  defects kept the global mean of the arriving sunlight and moved it between places, that the moved sunlight
  changed the clouds and the global means only modestly, and that the error shows in maps by longitude and
  season; it receives "two of the three" from the first paragraph. The results sentence it draws on, "The Sun
  and tilt changed the global means through the clouds" (`results.tex:48–51`), states its mechanism and
  inherits the two-year test from the sentence before.
- **Natural-world implications stated through named cases.** TRAPPIST-1e's convective cover, the slow
  rotators' Sun clock, Titan's haze and the flash-rate laws of the tidally locked planets state the
  implications for natural worlds through specific cases, each bounded once ("although Titan's nitrogen--methane radiation lies
  outside the adapted models"; "computed with the same laboratory charging laws"). The haze's scale height,
  the 65° limit and Sergeev et al.'s proposed route match the archived originals.
- **Evidence states attached once to their claims.** "Made before the ventilation repair and with leakage
  off"; "on the test world that fit is a step still to run"; "has been tested at a sixth of Earth's on the
  code paths those tests ran"; "known so far from the code's arithmetic, since away from Earth's values every
  change made for the test world has run on it alone". Each qualification bounds one claim and stands
  beside it.
- **The landing.** The final sentence gathers the third to fifth paragraphs into one relation for a new
  world: what the world's column determines is computed, what remains is calibrated, and the calibration's
  microphysics is open to laboratory and similarity tests. It bounds the computed parts by the spectroscopy's
  coverage and the air's height, marks the spectroscopic scheme as still to build and cloud as a calibration
  still to make, and presents no untested world as within reach. It lands on the contribution the abstract
  lands on, and it gives the answer to the introduction's two questions, where a model's Earth values lie
  and which repairs hold on another world.
- **Diction.** The screen found the excluded words absent from the conclusion and the abstract, and the
  remaining negations are required by their propositions; the reading found the prose clear of witticisms,
  stock transitions, self-reference, promotional words and rhetorical questions; the agents who act are named ("A modeller", "A designer",
  laboratories).
- **Reach and Next steps.** "Of the natural worlds in Figure~\ref{fig:regimes}, Earth alone lies near the
  fits in the adapted models, and the test world is the only world those models have simulated away from
  Earth's values" (`reach.tex:42–43`) states the bound positively. "Worlds near the existing fits" names the
  cloud fits as the open part for slow rotators, "Earth fits of a process through which those studies found
  the climate to change with rotation", which matches Way et al.'s "a shield of high, optically thick clouds
  that limit warming there", and keeps its evidence states plain ("fell 0.7 points short", "known through its
  fit residuals", "unchecked", "have yet to be made"); its second sentence is dense, and its clauses state real
  dependencies, so the record leaves it as it stands. "A test of the reach" names the question, the runs, the outputs, the
  separation from the models' own physics and the outcome that would reclass a repair, as G5 asks. The
  caption of Table tab:reach states design reach and evidence state together.

## 4. Counts and judgement

**Counts.** 19 findings: 1 BLOCKING (`results.tex:81–85`), 4 MAJOR (`conclusions.tex:59–63`, `67–72`,
`72–76`; `reach.tex:38–40`), 14 MINOR. Within the closing section itself: 3 MAJOR and 8 MINOR.

**Judgement.** The section meets the author's direction in its body and its landing, and falls short in its
last paragraph. From the second paragraph to the fifth it is a discussion: it draws from the test world a
diagnostic for errors that move sunlight between places, a criterion for which parts of a new world's model
come from the world's own column, and routes by which the remaining Earth laws can be tested, and it brings
the natural-world cases in through TRAPPIST-1e, Titan and the lightning laws of tidally locked planets,
leaving their lesson implicit. The landing gathers these lines into one bounded relation and places no
untested world within reach. The last paragraph reads in part as the earlier "laundry list" did: its passage on
constructed worlds recalls the design and states an implication the definition of a calibration already
holds, and its natural-planet sentence copies Next steps, while the paper holds a stronger constructed-world
relation, the shield's dimming set with the calibrated model, that would give the paragraph the substance and
the interest the author asked for. One clause in the fifth paragraph extends the released SWAN's error to
"any sea under another gravity, the ancient seas of Mars among them", beyond the configuration and the band
on which that error depends, and it is the one place where the section asserts a result on a world the work
has left untested. The single BLOCKING finding lies in Results, where a revised sentence characterises a
class of GCMs from one study. With findings 1 to 5 repaired, the section would meet the direction; the
audible reading of the conclusion remains pending.
