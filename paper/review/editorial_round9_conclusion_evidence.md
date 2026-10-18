# Editorial round 9: the Conclusion, evidence and scope review

## 1. Record

- **Reviewer.** A fresh Claude subagent, Claude Opus 5.5, reviewing for evidence and scope. It had seen no earlier
  review of the paper and opened nothing under `paper/review/` (apart from writing this file) or `paper/notes/`.
- **Date.** 2026-10-18.
- **Snapshot.** Commit `0cb4f50`, read with `git show 0cb4f50:<path>`; the working tree was clean at that commit.
- **In scope.** `paper/sections/conclusions.tex`, sha256
  `6dfec6728019a3e007c602159098dbf43b27a487d015cb03818fa385d1480049`, lines 1–102, the whole section, checked as new
  text. Line numbers below are those of this file at `0cb4f50`.
- **Rules.** `AGENTS.md`, sha256 `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32`, read in full.

**Relied on, world-crafting at `0cb4f50`:**

| File | sha256 |
|---|---|
| `paper/sections/abstract.tex` | `1d22734b8e9c39bc9b52f4eeff8c8436ee598b84e6bf5c14025f2b3fd17416b0` |
| `paper/sections/introduction.tex` | `a88f442f589e007dbb57f081334fc53ef066dbc26734d9f6610e12194bbea3d2` |
| `paper/sections/worlds.tex` | `453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112` |
| `paper/sections/assumptions.tex` | `77bc704fe58d964ff2567a39ffbdf6e2af9b0cc422bfb88e04d25e949b877107` |
| `paper/sections/repairs.tex` | `c846dbbf4dbaf39ae194d7bb93a26204aaa1b12f4b24e7aa1accdd948b281102` |
| `paper/sections/verification.tex` | `4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00` |
| `paper/sections/results.tex` | `112e8074232fd04300fccf280bb7bf5341e0b3d34a31a5c9a4561e46fcc4ca35` |
| `paper/sections/reach.tex` | `fff8183910168eeb9ee837c8e5766ac0bea7f64b6e95e0d63b8cf821e26f5b63` |
| `paper/sections/next.tex` | `789a34bd471f58e00c23ae3f422796c7c3333308337f80e49898017f862753ad` |
| `paper/sections/appendix.tex` | `17abe050d20a86031b7f3b1e426afcca0050cb9928bdb6500d84850d73013bbc` |
| `paper/sections/availability.tex` | `e88d7cb8f9923427d7d7a2d9a727e289a0cade48e967c0a8daafc14f8568b193` |
| `paper/claims.json` | `e462d3ff93eea66bb201aa51d42977bccff8b95f9099efc9559a01b487569745` |
| `paper/sources/manifest.json` | `afe0042bfc11c660958ed4fd5ab7ed524fb9dc4a2324fd8ebeab89ad9965b1c3` |
| `paper/data/regime_calc.json` | `7a2935a8fbe6086c577097b838825c5415ba99f0adf040af62f5e4bcd370e7d1` |
| `notes/verification_record.md` | `983329688203341ce74e4253acfb72e490b9d8efd252893d1d7b76dc97413ddc` |
| `notes/electrification.md` | `2cd81eb8edbd77348133a1e4aaca859b52ca4d0015bc5b26bf12e5d93308f59f` |
| `notes/waves.md` | `9f7a775ed1b8a297a4d4a8cf0cd416a8e732b8367cf9f241aaa15dc69cb28102` |
| `notes/cm1.md` | `75502ec7070a240006db6e4d491a6973cd2f013cc0c0945c3e61fb36b9fa5510` |
| `notes/exoplasim.md` | `707d97ef683d2650db8044cfee18f3a3ac7c82675dc37f4222476a6a4c978bf2` |
| `notes/reference_radiation.md` | `348501fa28bbe855f6cc99a200d81004fb4163fe91dd0ccccaa13517bbae2730` |
| `models/swan/README.md` | `abb218a0608362f5d2d58cbb72b4d6defcaacb02f06d7123690d862dbc15109d` |

**Relied on, Terluna at `186b294`:**

| File | sha256 |
|---|---|
| `climate/waves/README.md` | `87fe5f3621fee9cfa5e402b2e5a5132aa93b81052ce6b6b2c1f5708eb51a4ab2` |
| `climate/waves/first_experiments.md` | `959868b935ca29c3b4f3f929c987036627f81c884064e4f5887e1a29ec60b2a5` |
| `climate/crm/README.md` | `95776d41c55b3a3a372d3752ff367b66c45f3a98a1609b2cddfd953f49754acd` |
| `climate/gcm/README.md` | `267413c2aa248c3b7581d796ef83de826fbe6764d6d03c9abd1677fee03150fb` |

**Originals opened** (`paper/sources/originals/`, text taken with `pdftotext -layout`; each hash equals the
manifest's):

| File | sha256 | Passages read |
|---|---|---|
| `yang2023cloud.pdf` (arXiv:2306.12186v1) | `0637811e9ae240d47ab39da7d905421709afb685df2d0050f6f8ffdfa2d8bc41` | pp. 3–4 (cloud fractions, "broadly similar"), Methods (fixed SSTs), Discussions p. 7, Supplementary Text 3 |
| `yang2023cloud_si.pdf` (publisher SI) | `1cc0a5828d0dc0301b1b2aa712c48f58d8c312a6470e6c1d11df47a806ac5554` | Text 3; Table 3 |
| `vincendon2010spherical.pdf` (arXiv:1103.3215v1) | `afcdf418a60ce367c8b16c12d68c1bac36ea2fd8e0013498ea3553c0cbd8a7e9` | Abstract; Sect. 1; the Titan fit (80 ± 10 km) |
| `way2018climates.pdf` (arXiv:1808.06480v2) | `476e3e967e5d7eeafea1f386fc801851106365653bd3d9132c5821edb7164820` | Abstract; Sect. 2 (configuration); Table 2 notes |
| `loftus2021physics.pdf` (JGR version of record) | `d080f1289e115952977c4b09fa0f9e1b8d93f305315804c84a7878ed0a805d2c` | Sect. 3.4; Sect. 4.3; Appendix C1 |
| `mansell2026wrfelec-README.electricity.txt` | `d44c1594248a9f3b7492fa6ad581c821044a5a0d04addce5fac0d57aed516710` | the `nssl_isaund` options, lines 119–131 |

**Method.** Each number and statement in the section was matched to the body and its tables, to the claims-register
entry that carries it (the section has no markers, by design: `availability.tex`:28–29), and to the notes or
Terluna records that entry cites; the four cited works were read at the passages the section draws on. A few
ratios were computed by hand and are marked as such. No model, test or build was run.

## 2. Findings

### 1. BLOCKING — the ranking of Earth's share by form leaves out geometry, which moved the climate least

- **Location.** `conclusions.tex`:12.
- **Text.** "Measured that way on the test world, Earth's share was smallest in the units and constants and largest
  in the fits".
- **Evidence.** The body ranks the four forms (`introduction.tex`:71–73) at `results.tex`:87–91: the fits moved the
  global mean by at least 20 K and up to about 6 K, "while the two general repairs of units and constants measured
  singly moved it by 1.6–2.5 K and the geometry's curved-air terms, on the table's first channels, by 0.65 K"
  (G03: −0.65 K). Geometry's share is the smallest measured. The section's own next paragraph (L19–20) counts the
  geometry among the small shares.
- **Correction.** "Measured that way on the test world, Earth's share was smallest in the units, constants and
  geometry and largest in the fits, ..."; if a number is wanted, "and the curved-air terms, on the table's first
  channels, by 0.65 K".

### 2. BLOCKING — the sea's wave heights are credited to the knee repair; released SWAN computes them within 0.11%

- **Location.** `conclusions.tex`:25–28 and 29–30; echoed at 97–99.
- **Text.** "On the sea, once the bend in SWAN's wind growth moved with gravity, a lunar sea became the scaled image
  of an Earth sea, and the same wind, fetch and duration as on Earth raised waves four to five times higher, with
  periods five times longer and Earth's steepness." ... "Each of these features lay beyond the models while the
  code held the Earth value it depends on."
- **Evidence.** Released SWAN takes gravity as an input (`SET GRAV`; `notes/waves.md`:36). The knee patch "changes
  the lunar heights at the three main endpoints by at most 0.11%" (Terluna `climate/waves/first_experiments.md`:37–38);
  "In Terluna's 100 km strip the 48-hour heights change by at most 0.11% ... The patch makes lunar SWAN behave as
  Earth SWAN does in dimensionless terms" (`models/swan/README.md`:73–79). At lunar gravity the released bend, in the
  README's words, "lies above that band and never acts" (`models/swan/README.md`:73–74; `notes/waves.md`:166–167).
  The 4.2–4.8-fold heights and fivefold periods at
  100 km after 48 hours (`first_experiments.md`:18–27) therefore come out of released SWAN at lunar gravity to within
  0.11%. What the patch changed is the similarity error, 5.44% to 0.303% (V04), and the early growth, one-hour
  heights 13–51% lower (`notes/waves.md`:168–169). The paragraph's opening, "with them the models computed the
  features" (L19–20), and the closing claim at L29–30 attribute the sea's features to a repaired Earth value; for
  the sea the attribution is wrong.
- **Correction.** L25–28: "On the sea, SWAN at lunar gravity, with Wu's drag at both gravities, raised waves four to
  five times higher than the same wind, fetch and duration raise on Earth, with periods five times longer and
  Earth's steepness, and once the bend in its wind growth moved with gravity, that sea matched the scaled image of
  an Earth sea to 0.3%, while its 48-hour heights moved by at most 0.11%." L29–30: "The storms, the rain's fall and
  the twilight lay beyond the models while the code held the Earth value each depends on." L97–99 can stand once
  L25–30 is corrected.

### 3. BLOCKING — the reach of a general repair and of the curved-air method is stated as a result

- **Location.** `conclusions.tex`:58–60.
- **Text.** "A general repair holds as it is, within the limits of its law. The curved-air method holds once its
  table is recomputed from the new world's own column".
- **Evidence.** The body states design intent: a general repair "is built to hold on another world within the limits
  of its laws" (`introduction.tex`:76–79); W01 "built to apply unchanged"; W03 "untested; no run made"; the reach
  table gives "the reach each repair was built for" (`reach.tex`:91–93); and `next.tex`:45–47 provides for failure:
  "A general repair whose arithmetic fails off the test world would be reclassified, and the reach of
  Table~\ref{tab:reach} would narrow with it." The curved-air table exists for one design column
  (`repairs.tex`:87–96). The paragraph's last sentence (L64–65) gives the evidence state after the claims, while
  L59–60 state the reach as fact.
- **Correction.** "A general repair is built to hold as it is, within the limits of its law, and the curved-air
  method to hold once its table is recomputed from the new world's own column, which matters wherever ...". Keep
  L64–65.

### 4. BLOCKING — the 3.7 K disagreement of two models in one state is presented as the design's uncertainty

- **Location.** `conclusions.tex`:82–85.
- **Text.** "the Earth values left in them are the design's own uncertainty: in the air where people and plants
  would live, the lowest 1.8~km at 45\textdegree\,N, the GCM and the storm model it forces still bracket the warmth
  within 3.7~K once the transport across the ring is imposed."
- **Evidence.** `results.tex`:116–120: "Under the design-case forcing, with the longwave correction off, the two
  models bracket ... within 3.7 K once the transport is imposed; about 1.5 K of the bracket is the GCM's own
  over-cooling, so the bracket measures the models' disagreement in that one GCM state." CM1 is nudged toward the
  GCM above 8–16 km and takes the GCM's vertical wind and forcing (`repairs.tex`:176–183), so an Earth fit in the GCM
  moves both models together: the longwave correction, switched on with the ice optics, warmed the design case by
  11.5 K (`results.tex`:82–86; G05), the cloud settings moved it by up to about 6 K (G05), and no CM1 case has run
  from a longwave-corrected GCM (`notes/verification_record.md`:215–219). The colon makes the 3.7 K the size of the
  design's uncertainty in the habitable layer; the evidence makes it the two models' disagreement in one state, with
  the largest tested fit switched off.
- **Correction.** "... are the design's own uncertainty: switched on with the ice optics in a test, the longwave
  correction warmed the design case by 11.5 K, and in the air where people and plants would live, the lowest 1.8 km
  at 45°N, the GCM and the storm model it forces, with that correction off, still differ by 3.7 K once the transport
  across the ring is imposed, about 1.5 K of it the GCM's own over-cooling."

### 5. MAJOR — "whose default reproduces the released code" states as verified what is written to hold

- **Location.** `conclusions.tex`:8–10.
- **Text.** "Most repairs of an Earth value or a defect were built as switches whose default reproduces the released
  code".
- **Evidence.** `repairs.tex`:3–4: "a parameter whose default is written to reproduce the released code";
  `repairs.tex`:45–48: "runs confirm that identity for five of them ..., and the near-infrared water scaling
  reproduces the released code at its default only for spectra like the design case's." The Sun-clock,
  water-scaling, curved-air, gas-band and longwave patches have no runtime identity run
  (`verification.tex`:20–26; `notes/verification_record.md`:46–53). Some defaults differ from the release by design:
  CM1's carbon dioxide defaults to 400 ppm "in place of the calendar formula", and the graft's gravity to 9.81 where
  WRF-ELEC has 9.8 (`appendix.tex`:81, 96). Runtime identity is confirmed for five ExoPlaSim patches, SWAN's knee at
  standard gravity and two CM1 forcing changes (`appendix.tex`:130–134).
- **Correction.** "Most repairs of an Earth value or a defect were built as switches whose default is written to
  reproduce the released code, an identity that runs have confirmed for five of ExoPlaSim's patches, so that ...".

### 6. MAJOR — the geometry is credited to "repairs made by arithmetic"

- **Location.** `conclusions.tex`:19–20 (with 28–29).
- **Text.** "the repairs made by arithmetic put the world's own gravity and geometry into the models".
- **Evidence.** The body separates a general repair, whose values follow from a unit, a scaling law or a fitted
  parameterization, from a general method, which "computes a quantity of the world's own column offline and enters
  it as computed" (`repairs.tex`:11–16). The curved-air terms come from line-by-line radiation traced through 100
  spherical shells in 10,697 channels, 282 of them by successive orders of scattering (`repairs.tex`:87–96; R05),
  and the inventory classes them "Method, lunar table" (`assumptions.tex`:172–173). The section's own L94–95
  separates "constants and clocks by arithmetic" from "the geometry of tall air from the world's own column".
- **Correction.** "the repairs made by arithmetic put the world's own gravity into the models, and the curved-air
  table computed from its own column put in its geometry, and with them ...".

### 7. MAJOR — "such a world" carries one world's conditional results to a kind of world

- **Location.** `conclusions.tex`:20.
- **Text.** "and with them the models computed the features by which such a world departs from Earth."
- **Evidence.** Each feature at L21–29 is a conditional model result for the test world alone: "Every lunar climate
  number is a conditional model result ... and every repair has so far run on the Moon alone"
  (`introduction.tex`:83–85); "the test world is the only world those models have simulated away from Earth's
  values" (`reach.tex`:44–45). The author's direction excludes wording that extends the work to untested kinds of
  world.
- **Correction.** "and with them the models computed the features by which the test world, in its models, departs
  from Earth."

### 8. MAJOR — the electrified run's flash density and charge heights lose their grid and forcing conditions

- **Location.** `conclusions.tex`:24–25; the condition list at 99.
- **Text.** "and in the electrified run their charge took Earth's arrangement at five to six times its height,
  flashing at about a hundredth of Earth's average density." ... "each a conditional result that the remaining fits
  can still move."
- **Evidence.** The electrified run is one box at 0°E forced from the Earth-orbit state (`results.tex`:144–146), a GCM
  state that kept PlaSim's Sun clock and Earth's orbit (`results.tex`:11–13) and "brought 12% too little sunlight
  there" (`results.tex`:110–111); the verification record lists its forcing among the older GCM states whose CM1
  cases still await new forcing (`notes/verification_record.md`:227–228; `next.tex`:114–117). On the flash density, `results.tex`:151–153: "Part of the difference
  from Earth may come from the grid, since the box's 6 km columns correspond to about 1 km at Earth's scale and on
  the Earth benchmark a coarser grid gave fewer, larger flashes"; `notes/electrification.md`:97–99: "how much of the
  lunar flash delay and rate the grid sets is open". The sentence ties the density to gravity's stretch (L23–25),
  and L99 names the remaining fits as the only thing that can move these results, while the forcing state, the grid
  and the single realisation on several threads (`verification.tex`:35–36) bound them as well.
- **Correction.** L24–25: "and in the electrified run, one box forced from the GCM before its Sun and tilt were
  corrected, their charge took Earth's arrangement at five to six times its height, flashing at about a hundredth
  of Earth's average density, a rate the 6 km grid may set in part." L99: "each a conditional result that the
  remaining fits, and the forcing and grid of the runs, can still move."

### 9. MAJOR — the fourfold-to-fivefold wave heights lose the drag law they rest on

- **Location.** `conclusions.tex`:26–28.
- **Text.** "the same wind, fetch and duration as on Earth raised waves four to five times higher, with periods five
  times longer and Earth's steepness".
- **Evidence.** `results.tex`:172–176: "Under Earth's laws for wind input, whitecapping and breaking, scaled to lunar
  gravity by similarity, and with Wu's drag law at both gravities ... with Charnock's roughness at each gravity the
  lunar drag would be larger and the ratio higher, by about a tenth to a half"; G12 (11–51%);
  `notes/waves.md`:191–196. `next.tex`:98–101 leaves open whether the similarity image holds on the test world: "a
  wide spread would make the lunar wave heights a range."
- **Correction.** Within the rewrite of finding 2: "with Wu's drag at both gravities, raised waves four to five times
  higher, a tenth to a half higher still with Charnock's roughness at each gravity, ...".

### 10. MAJOR — the prospect of a line-by-line scheme drops the range its checks would cover

- **Location.** `conclusions.tex`:40–43.
- **Text.** "A scheme built from line-by-line spectroscopy would replace the radiation's gas and scattering fits for
  air of nitrogen and oxygen with water and modest carbon dioxide, under the starlight it would be built for, once an
  independent code has checked that spectroscopy, a comparison planned on the design column."
- **Evidence.** The abstract bounds the same scheme "over the pressures and temperatures where that spectroscopy
  agrees with an independent code" (`abstract.tex`:23–26); `next.tex`:14–19: "once that spectroscopy is checked and
  the reduction is checked against it layer by layer, would hold on columns within the gases, pressures and
  temperatures of the checks". A comparison on the one design column (`next.tex`:30–36) covers that column's
  pressures and temperatures. With both conditions dropped, the sentence extends the scheme to all nitrogen–oxygen
  air.
- **Correction.** "... under the starlight it would be built for and over the pressures and temperatures of its
  checks, once an independent code has checked that spectroscopy, a comparison planned on the design column, and
  the scheme has been checked against it layer by layer."

### 11. MAJOR — Yang et al. found the models far apart in cloud cover and judged their climates broadly similar

- **Location.** `conclusions.tex`:43–46.
- **Text.** "\textcite{yang2023cloud} found the two kinds of model far apart on two tidally locked planets: two GCMs
  covered 82--97\% of the sky, and cloud-permitting runs over sea surfaces fixed from a coarser run, counting cloud by
  a condensate threshold, 27 and 41\%."
- **Evidence.** The numbers hold: SAM 26.9 and 41.1%, CAM3 94.8 and 81.7%, ExoCAM 90.4 and 97.4% (arXiv v1 p. 3;
  SI Table 3: 27, 95, 90; 41, 82, 97); the threshold is SI Text 3's 0.01 g/kg by level and 0.02 kg/m² by column; the
  4 km runs used SSTs fixed from the 40 km run (Methods). The same authors write, p. 4: "Overall, the simulated
  climates between CPM and GCM are broadly similar ... The similarity in the results between the two types of models
  also increases our confidence of using GCMs", and, Discussions p. 7, that surface temperature and planetary albedo
  in the CPM "are broadly similar to those found in GCM experiments" while the GCMs "may have overestimated the cloud
  liquid water amount and cloud coverage especially on the nightside". The albedos lay at 18.1 and 37.4% against
  22.1–29.1 and 39.0–47.0% (SI Table 3). `results.tex`:95–96 reports the albedos and the authors' judgement; the
  section keeps only the cover and attributes "far apart" to the authors without its variable.
- **Correction.** "\textcite{yang2023cloud} found the two kinds of model far apart in cloud cover on two tidally
  locked planets, while judging their climates broadly similar: ...".

### 12. MAJOR — "many climate studies" characterises the field from two cited studies

- **Location.** `conclusions.tex`:70–71.
- **Text.** "on slowly rotating planets of the kind many climate studies model."
- **Evidence.** The paper's evidence for this kind of planet is two studies, \textcite{yang2014strong} and
  \textcite{way2018climates} (`introduction.tex`:3–5; `reach.tex`:51–53); the body's own wording for the same test is
  "worlds that other studies model" (`next.tex`:42). `AGENTS.md`, "Claims stay within their evidence", scopes such
  statements to the cited works.
- **Correction.** "on slowly rotating planets of the kind \textcite{yang2014strong} and \textcite{way2018climates}
  modelled."

### 13. MINOR — "Earth's air" for air close to Earth's; "seven times" for 7.25

- **Location.** `conclusions.tex`:4, 87, 88–89.
- **Text.** "a world whose air is Earth's"; "combine Earth's air"; "hold Earth's air ..., seven times Earth's mass of
  air over each square metre".
- **Evidence.** The air holds 1,216 hPa at the water level, oxygen at 17.5% and no ozone (`worlds.tex`:35–39); the
  body calls it "close to Earth's in composition and surface pressure" (`introduction.tex`:46–47) and "Earth-like air"
  (`introduction.tex`:25). S02: 7.25.
- **Correction.** "a world whose air is close to Earth's"; "Earth-like air" at L87 and L88; "7.25 times Earth's mass
  of air".

### 14. MINOR — the ground strikes rest on a bound

- **Location.** `conclusions.tex`:6.
- **Text.** "separate charge and strike the ground".
- **Evidence.** Under WRF-ELEC's stopping field "every lunar channel stops 15–25 km up", and the condition used
  places the strikes between that rule and the −7 °C rule (`repairs.tex`:160–165); "the bound on ground strikes, now
  between none and a fifth of flashes" (`next.tex`:94–96).
- **Correction.** "separate charge and flash, striking the ground under a bounded condition".

### 15. MINOR — the second paragraph's numbers lose their run and the word "first"

- **Location.** `conclusions.tex`:13–15.
- **Text.** "Correcting the convective cover's unit, or the height scale of the cloud water, moved the global-mean
  surface temperature by 1.6--2.5~K; calibrating the radiation's fits against the line-by-line model moved it by at
  least 20~K".
- **Evidence.** Both general repairs were measured on the first calibrated run, with 25% seas, the undimmed shield
  and Earth's seasons (`results.tex`:41–44; G01). The 20 K belongs to the first calibration, from a run still warming
  at 315.5 K (`results.tex`:36–39; G14); later calibrations moved the climate by other amounts (gas bands −2.2 K, G03).
- **Correction.** "On the first calibrated run, still in Earth's seasons, correcting the convective cover's unit, or
  the height scale of the cloud water, moved the global-mean surface temperature by 1.6–2.5 K; the first
  calibration of the radiation's fits against the line-by-line model moved it by at least 20 K".

### 16. MINOR — the rain pair's forcing

- **Location.** `conclusions.tex`:21–23.
- **Text.** "in a storm-resolving box, with drop sizes still set for Earth, 85\% of the water leaving the clouds
  evaporated on the way down, against 64\% when the same drops fell at Earth's speeds."
- **Evidence.** G08, "The small box on pre-correction forcing"; Terluna `climate/crm/README.md`:965–966: "the pair
  differs in the fall alone, and both keep the forcing of the GCM before its correction"; each box run on several
  threads is one realisation (`verification.tex`:35–36). Both members share the forcing, so the comparison stands;
  the 85% carries the forcing as a condition.
- **Correction.** "in a storm-resolving box forced from the GCM before its Sun and tilt were corrected, ...".

### 17. MINOR — the storms' stretch is credited to the microphysics as well as the dynamics

- **Location.** `conclusions.tex`:23–24.
- **Text.** "Read by CM1's dynamics and microphysics, the same gravity stretched the storms upward".
- **Evidence.** The 0 °C and −40 °C levels near 25 and 60 km and the 55–80 km tops hold "in every run", the box whose
  particles all fall at Earth's speeds included (Terluna `climate/crm/README.md`:1445–1455). CM1 is nudged toward the
  GCM's profile above 8–16 km (`repairs.tex`:179–180), and that profile carries lunar gravity's heights.
- **Correction.** "Read by CM1's dynamics, and set in the GCM profile toward which CM1 is nudged aloft, the same
  gravity stretched the storms upward".

### 18. MINOR — "half" for 0.45–0.47

- **Location.** `conclusions.tex`:28–29.
- **Text.** "air so tall that half of it still lies above the Moon's shadow a full Earth day after sunset."
- **Evidence.** S04: 0.465 of an isothermal column's mass and 0.453 of the design profile's above the shadow, with
  the Sun 12.2° down and refraction ignored (`regime_calc.json`, `one_day_after_sunset`); the body says "about half
  ... before refraction adds more" (`worlds.tex`:78–80).
- **Correction.** "air so tall that about half of it still lies above the Moon's shadow ...".

### 19. MINOR — the identity checks belong to ExoPlaSim and compare restarts; "that kind" covers every check

- **Location.** `conclusions.tex`:33–34.
- **Text.** "Most of the checks made here are of that kind: five patches at their neutral settings repeat the runs
  of the builds before them byte for byte".
- **Evidence.** Five ExoPlaSim runs, "each a model year from one restart, repeat byte for byte the restart of the same
  build before the patch" (`verification.tex`:17–20; `notes/verification_record.md`:44). SWAN's knee and two CM1
  forcing changes have identity checks of their own (`appendix.tex`:130–134). The kind defined at L32–33, checks
  "that need no observation of it", includes every check made here, the calibrations and Earth benchmarks among
  them; "most" fits the narrower kind of L37–38, checks that "need nothing from the world it models".
- **Correction.** "Most of the checks made here need nothing from the world at all: five of ExoPlaSim's patches at
  their neutral settings repeat a model year's restart of the builds before them byte for byte; ...".

### 20. MINOR — WRF-ELEC carries more charging laws than the two compared

- **Location.** `conclusions.tex`:49.
- **Text.** "The two charging laws grafted into CM1".
- **Evidence.** The graft replaces CM1's NSSL module with WRF-ELEC's (`notes/electrification.md`:15–18), whose
  `nssl_isaund` offers Saunders (1991) variants, Saunders and Peck variants, Brooks et al.'s critical-rate variants
  and Takahashi's (`mansell2026wrfelec-README.electricity.txt`:119–131); the windows compared two of them (G11).
- **Correction.** "Two of the charging laws grafted into CM1".

### 21. MINOR — "opposite arrangements" held in part of the first window

- **Location.** `conclusions.tex`:50–51.
- **Text.** "they held the lunar storms' charge in opposite arrangements".
- **Evidence.** G11 and `next.tex`:85–87: the normal arrangement under Saunders and Peck's law held "in most of the
  second window's outputs and about half of the first's".
- **Correction.** "they held the lunar storms' charge in opposite arrangements, the normal one under Saunders and
  Peck's law in most of the second window's outputs and about half of the first's".

### 22. MINOR — the deciding measurement loses its cloud water and temperature

- **Location.** `conclusions.tex`:51–53.
- **Text.** "measurements of that sign at the impact speeds of the storms' hail and graupel, 4--8 and about
  1--4~m\,s$^{-1}$".
- **Evidence.** N01; `next.tex`:88–91; `notes/electrification.md`:130–132: the sign "in 0.02–0.2 g/m³ of cloud water
  at −5 to −16 °C". The speeds match N01 (4.4–7.6 and 0.95–3.6 m/s).
- **Correction.** "measurements of that sign at the impact speeds of the storms' hail and graupel, 4–8 and about
  1–4 m s⁻¹, in 0.02–0.2 g m⁻³ of cloud water at −5 to −16 °C".

### 23. MINOR — the numerical controls drop out of the statement of reach

- **Location.** `conclusions.tex`:64–65.
- **Text.** "Away from Earth's values, the repaired codes have run on the test world alone."
- **Evidence.** The abstract keeps "numerical controls apart" (`abstract.tex`:19–20) and the reach table "apart from
  the Earth benchmarks and numerical controls" (`reach.tex`:92–93); patched SWAN ran Cartesian strips at a sixth of
  Earth's gravity (V04) and CM1 its gravity pair (V06), both off the test world.
- **Correction.** "Away from Earth's values, numerical controls apart, the repaired codes have run on the test world
  alone."

### 24. MINOR — "the configuration" of the ROCKE-3D runs covers more than the planned runs match

- **Location.** `conclusions.tex`:68–70.
- **Text.** "run in the configuration of two of the ROCKE-3D runs of \textcite{way2018climates}".
- **Evidence.** The listed settings match Way et al. (arXiv v2, abstract and Sect. 2): ozone-free, nitrogen-dominated
  air with 400 ppm of carbon dioxide, S0X = 1.0, zero obliquity and eccentricity, sidereal periods 16 and 64 days.
  Their runs also fixed modern Earth's land and topography, a land albedo of 0.2, 984 hPa, 1 ppmv of methane and a
  100 m Q-flux = 0 or a dynamic ocean; the planned runs match "two of the sidereal periods" with the air, orbit and
  insolation (`next.tex`:38–42).
- **Correction.** "run with the air, orbit, insolation and rotation of two of the ROCKE-3D runs of
  \textcite{way2018climates}".

### 25. MINOR — the orbit default keeps the annual global mean on near-circular orbits

- **Location.** `conclusions.tex`:73–75.
- **Text.** "The Sun clock and the orbit default keep the global mean of the sunlight arriving at the top of the air,
  and the Sun clock every zonal mean as well".
- **Evidence.** The Sun clock: "Each row of latitude still gets its right mean" (Terluna `climate/gcm/README.md`:
  186–187). The orbit default discards the configured eccentricity with the obliquity and puts Earth's 0.0175 (W06;
  `notes/exoplasim.md`:53–58). The annual global mean scales as (1 − e²)^(−1/2): by hand, it changes by 0.015% for a
  configured eccentricity of 0 and by 2.0% for one of 0.2.
- **Correction.** "The Sun clock and the orbit default keep the global annual mean of the sunlight arriving at the top
  of the air, the orbit default on near-circular orbits, and the Sun clock every zonal mean as well".

### 26. MINOR — the 0.9 K comes from a run still out of balance

- **Location.** `conclusions.tex`:75–76.
- **Text.** "in a two-year test on the test world, correcting the Sun and tilt moved the global-mean surface
  temperature by 0.9~K".
- **Evidence.** G17: a two-year mean against the Earth-orbit state's years 15–24, the "top of the air still gaining
  1.9 W/m2" (`results.tex`:49–52); the settled step with the refitted split gave +0.59 K (G02).
- **Correction.** "moved the global-mean surface temperature by 0.9 K over two years while its air still gained
  1.9 W m⁻²".

### 27. MINOR — "every ratio" and a smaller world met "one at a time"

- **Location.** `conclusions.tex`:90–91.
- **Text.** "departs from Earth along every ratio at once, ... the same values a run of a slow rotator or a smaller
  world meets one at a time."
- **Evidence.** The paper names four ratios (`introduction.tex`:46–51; `worlds.tex`:3–14). A smaller world with
  Earth-like air departs along several of them together: Mars held at 1 bar has 0.38 of Earth's gravity, 2.6 times
  Earth's air over each square metre and five times its scale height over radius (`reach.tex`:67–69; W04).
- **Correction.** "departs from Earth along all four ratios at once, so a model run on it meets at once every Earth
  value that depends on them, values a slow rotator meets one at a time and a smaller world a few at a time."

### 28. MINOR — the laboratory plan covers some of the laws inside the resolved runs

- **Location.** `conclusions.tex`:96.
- **Text.** "and the laws inside those runs to be measured in Earth's laboratories."
- **Evidence.** The next steps plan a laboratory measurement for the charging sign (`next.tex`:88–91); the drop
  limits are to be tested by runs with limits scaled by the capillary length (`next.tex`:76–77), and the seas' laws
  against theory and the spread of source-term packages (`next.tex`:98–101). The section's own L48–49 says "some of
  those laws come from Earth's laboratories".
- **Correction.** "and some of the laws inside those runs to be measured in Earth's laboratories."

## 3. Checked and sound

- **The chain** (L3–8): the codes, couplings and the reference's role match `introduction.tex`:55–68 and
  `repairs.tex`:184–187. "Most repairs" (L8) matches `repairs.tex`:3.
- **Numbers in the second paragraph** (L13–16): 1.6–2.5 K (G01, settled 1.6 and 2.5; window means 1.8 and 2.3), at
  least 20 K (G14), up to about 6 K (G05: −4.98 K, about −5.9 K settled); conditions in finding 15.
- **Rain** (L21–23): raindrops 2.94 times slower (R02); 85% against 64% (G08; Terluna `climate/crm/README.md`:969–975).
- **Storms** (L24–25): tops 55–80 km (G09); main negative charge at 40–42 km, five to six times Earth's height (G10);
  0.022 against Earth's 2.72 flashes per km² per year, 0.0081 (`regime_calc.json`, `flash_density`).
- **Waves** (L27): periods 5.2, 5.0 and 4.7 times Earth's at 100 km after 48 h (`first_experiments.md`:22–24). By hand,
  with deep-water wavelengths from the mean periods, the lunar strip waves are 9–15% steeper than Earth's, which
  "Earth's steepness" carries at the paper's precision.
- **Twilight** (L28–29): the terms are tabulated from −40 to 90° and applied below the horizon (R06), and the Sun
  stands 12.2° down a day after sunset (S04).
- **Reproduction and similarity** (L34–36): the series rebuild the deployed ExoPlaSim sources and the lunar CM1 builds
  (V03; `notes/cm1.md`:10–13) and SWAN's patched sources (`notes/waves.md`:48) byte for byte; 0.303% against 5.44%
  (V04; `notes/verification_record.md`:170).
- **The independent check** (L43): planned on the design column (`next.tex`:30–36).
- **Yang et al.** (L44–46): every number, the condensate threshold and the fixed SSTs (finding 11 covers the
  attribution).
- **Charging speeds** (L52–53): 4–8 and about 1–4 m/s (N01).
- **Loftus and Wordsworth** (L53–56): 2.46 (H21; `regime_calc.json` 2.457); Appendix C1, "Such experiments
  consistently agree (within about 20%) with the predictions of Equation 21", for drops much more viscous than the
  fluid they fall through, a condition raindrops in air meet; the experiments were run at Earth's gravity, as the
  sentence says.
- **Vincendon and Langevin** (L60–63): plane-parallel codes "typically less than 80° for Mars and 65° for Titan,
  which has a larger relative scale height" (Sect. 1); Titan's aerosol scale height 80 ± 10 km (abstract; Sect. 4);
  by hand 80/2,575 = 0.031 against the test world's 52.4/1,737 = 0.030.
- **Other worlds' needs** (L63–64): refitted calibrations and new radiation, condensation and clouds for other air
  match `reach.tex`:62–79 and W05.
- **The defects off the test world** (L71–73): about 33° for any rotation slower than 20 days (W02, H23: N = 12,
  32.7°); 0.23 for TRAPPIST-1e (W06: model day 6.20 d, 0.228); both stated as the code's arithmetic. The Sun clock's
  zonal means (L74–75) hold by Terluna's record. 9 to 36% (G02; Terluna `climate/gcm/README.md`:662–664).
- **The design** (L79–81, 84–85, 88–89): 295 K, 5.0 to 3.0% (G04); 1.8 km and 3.7 K (G06; conditions in finding 4);
  the shield's retention as the design's own models (S15); three hundredths (S03, 0.0301).
- **The field** (L93): "Many models used for other worlds began as models of Earth" rests on the body's account
  (`introduction.tex`:7–13: THOR's developers; ROCKE-3D, ExoCAM, ExoPlaSim, PlanetWRF).
- **The closing results** (L97–98): charge heights (G10), rain that mostly evaporates (85% in the boxes, 57–73% in
  the rings, N03).
- **The ending** (L99–102): "Followed to its end" and "would" keep it a prospect; its inputs, gravity, day and
  starlight, and the per-world steps of L94–96 match the body's plan, and "every Earth value ... named and measured"
  reads as the method's aim.

## 4. Counts

| Severity | Count | Findings |
|---|---|---|
| BLOCKING | 4 | 1, 2, 3, 4 |
| MAJOR | 8 | 5–12 |
| MINOR | 16 | 13–28 |
| Total | 28 | |
