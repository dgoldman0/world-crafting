# Editorial round 6: evidence review of the closing section, the abstract and the revised passages

## 1. Record

- **Reviewer:** a fresh Claude subagent, Claude Opus 5.5 (`claude-opus-5-5`), with sight of the text, the rules and
  the evidence named in the brief, and of no earlier review. This file is the only file it wrote.
- **Date:** 2026-10-17.
- **Snapshot:** world-crafting commit `8bfd069` ("Revise the closing section from the fifth round's records: what
  laboratories and runs can test, and the bounds on a new world"). Every repository file was read with
  `git show 8bfd069:<path>`; Terluna files with `git -C ../terluna show 186b294:<path>`.
- **Rules read in full:** `AGENTS.md` (working tree, sha256 `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32`),
  with the author's direction that the closing section and the abstract carry each statement about other worlds in its
  own evidence state and imply no reach to untested kinds of world.

### Files in scope (sha256 at 8bfd069)

| File | sha256 | Scope |
|---|---|---|
| `paper/sections/conclusions.tex` | `81986ca02bb0dff1b95b263945ac3144f74e189dbdce7af97341e014c27e25c2` (as in the brief) | whole section |
| `paper/sections/abstract.tex` | `0cf59842b240289e4b318ed5b082c58df0340b44232585ff549a648459c9272d` (as in the brief) | whole abstract |
| `paper/sections/results.tex` | `10466525ecf68ba0c6b56fbb0d9a6f8a45c8979bf531635c7faabd3ce1813948` | lines 44–46, 81–86, 91–95, 151–155 |
| `paper/sections/reach.tex` | `99d26b100d9a9072f2660b0a7dc29fcf9a7cc398da32acf7154390d893209d02` | lines 38–42, 90–93, 114 |
| `paper/sections/next.tex` | `d0ee214445d0194d9dcf1fb310e2979d11705b4ac50046dd6ebf6fdb28d859ec` | lines 35–43 |
| `paper/sections/assumptions.tex` | `8f267b18c88d50e4083b9169adb7d38d6fcecd9fd0d11d14f58270989b798e68` | lines 21–27 |

### Evidence files relied on

At 8bfd069:

| File | sha256 |
|---|---|
| `paper/claims.json` | `6b4718a2be6128506d693a87cdcc2753194d0d8d39cce9c0a9038ed490f0cfb8` |
| `paper/sources/manifest.json` | `1bd81f61a4be8999481e6268021d588d082c6dc2f20256a1b368c5bf83d9ea29` |
| `paper/references.bib` | `c0c9662b362141759bce9a27bb566e7ee6a00479ef773273f1dc109d7888747e` |
| `paper/data/regime_calc.json` | `7a2935a8fbe6086c577097b838825c5415ba99f0adf040af62f5e4bcd370e7d1` |
| `paper/data/repairs.json` | `3dada16f0e39dba9fe576587da12764ceceaa1ad4f421b33d8dffbe1826b4987` |
| `notes/reference_radiation.md` | `348501fa28bbe855f6cc99a200d81004fb4163fe91dd0ccccaa13517bbae2730` |
| `models/swan/README.md` | `abb218a0608362f5d2d58cbb72b4d6defcaacb02f06d7123690d862dbc15109d` |
| `notes/waves.md` | `9f7a775ed1b8a297a4d4a8cf0cd416a8e732b8367cf9f241aaa15dc69cb28102` |
| `notes/exoplasim.md` | `707d97ef683d2650db8044cfee18f3a3ac7c82675dc37f4222476a6a4c978bf2` |
| `notes/electrification.md` | `2cd81eb8edbd77348133a1e4aaca859b52ca4d0015bc5b26bf12e5d93308f59f` |
| `paper/sections/introduction.tex` | `b8325d641b56d6da32cffbcaa143e26461495322235c2de3b0709402f1ef5b72` |
| `paper/sections/worlds.tex` | `453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112` |
| `paper/sections/repairs.tex` | `bb1d22c01616fdaf454280acded56316b7995af2a8fc3bb5a255af52c92e793c` |
| `paper/sections/verification.tex` | `4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00` |
| `paper/sections/appendix.tex` | `ebab8ca204f81ed41d9185d456353a43a9f59e5307290695277b4614b5bd6635` |
| `paper/sections/availability.tex` | `496434ae301b500a3f7dcec2750af08b8a4d1789c437844ab1318e3ff35f762d` |

Terluna at 186b294 (sha256 of the file content):

| File | sha256 |
|---|---|
| `climate/gcm/README.md` | `267413c2aa248c3b7581d796ef83de826fbe6764d6d03c9abd1677fee03150fb` |
| `climate/crm/README.md` | `95776d41c55b3a3a372d3752ff367b66c45f3a98a1609b2cddfd953f49754acd` |
| `atmosphere/radiative_convective/README.md` | `add6e0d821abd966bdb40b2b5e1180efc2b7039b00e7cd510f32c8dab64efaf6` |
| `atmosphere/radiative_convective/METHODS.md` | `14043b7693eab8b8cc16fc986f62c8e17ca04e6e64227fe1cdfc468ee2b9bfbc` |

### Source originals opened

Each was hashed before reading and matches its manifest record; text extracted with `pdftotext -layout`.

| Original | sha256 | Version |
|---|---|---|
| `yang2023cloud.pdf` | `0637811e9ae240d47ab39da7d905421709afb685df2d0050f6f8ffdfa2d8bc41` | arXiv 2306.12186v1 |
| `yang2023cloud_si.pdf` | `1cc0a5828d0dc0301b1b2aa712c48f58d8c312a6470e6c1d11df47a806ac5554` | publisher SI |
| `braam2022lightning.pdf` | `26486cfc19cb2185ca8f98a22bcbadf40a526afed1f8b3d460154915b58cf8c7` | arXiv 2209.12502v1 |
| `sergeev2025lightning.pdf` | `b2c3352f4ad065bd894341eb76741ff541b1bf4c4824612ae7e6404bd373c6df` | arXiv 2504.19883v2 |
| `vincendon2010spherical.pdf` | `afcdf418a60ce367c8b16c12d68c1bac36ea2fd8e0013498ea3553c0cbd8a7e9` | arXiv 1103.3215v1 |
| `way2018climates.pdf` | `476e3e967e5d7eeafea1f386fc801851106365653bd3d9132c5821edb7164820` | arXiv 1808.06480v2 |
| `loftus2021physics.pdf` | `d080f1289e115952977c4b09fa0f9e1b8d93f305315804c84a7878ed0a805d2c` | version of record |
| `deitrick2020thor.pdf` | `52da49f440c5f77cb35cd99b8ec66274d192e7461c33ea26695dcd8a823b7d7c` | read for the abstract's "Many" |
| `banfield2015winds.pdf` | `252db567cd32131d949261413bed1a948a4d2839161f6faeb206851eb9cda325` | read to see what the SWAN sentence attributes to it |

`loftus2021physics_arxiv.pdf` (`18fbf925…91af`) was hashed only; its text was left unread.

### What was read and computed

- The whole body at 8bfd069, all thirteen section files with their tables and captions; `claims.json` in full; the
  manifest records and bibliography entries of the six named works; the repository and Terluna files above at the lines
  cited in the findings; the `regime_calc.json` entries `exoplasim_synchronous_cover_bias`, `exoplasim_slow_rotators`,
  `sun_clock_skip`, `slingo_cover_bias`, `capillary_length_ratio`, `flash_density` and `scale_height`; the first row of
  `repairs.json`.
- Arithmetic by hand: ExoPlaSim's N, model day and cover bias for 6.1 and 11.2 days; the skip for N = 12 and N = 24;
  √(9.81/1.62); the flash-density ratio; Titan's aerosol scale height over its radius, 80/2,575; the albedo and
  temperature spreads of Yang et al.'s SI Table 3; the two knee cases of the SWAN sentence; the albedo fall times the
  mean sunlight in the two-year Sun-and-tilt test.
- Unperformed: model runs and builds; reads of the research drive; reads of Takahashi (1978) and Saunders and Peck (1998),
  so the charging-law statements were checked against the body, the notes and Terluna's record alone; any search of
  outside literature on laboratories at other gravities.

## 2. Findings

### 1. BLOCKING: the closing sentence sets the bounds of a new world wider than the evidence

- **Location:** `paper/sections/conclusions.tex:81–86`.
- **Text:** "A modeller of a new world of nitrogen--oxygen air with water and modest carbon dioxide, at pressures and
  temperatures within the reference's tables and with a scale height at most three hundredths of its radius, the test
  world's ratio, would compute its radiative geometry from its own column, its gas absorption from the reference's
  spectroscopy once a scheme is built and the spectroscopy checked, and fit its cloud scheme to cloud-resolving runs
  whose drop-size limits stay Earth's and whose lightning takes its sign from charging laws that Earth's laboratories can
  test."
- **Evidence.** The sentence defines a class of worlds by three bounds and attaches the work's procedure to the whole
  class.
  - (a) "Within the reference's tables" is the node box of the longwave correlated-k tables: 0.1 Pa to 3.2×10⁵ Pa,
    100–375 K and water fractions 0–0.5 (claims.json R08; `notes/reference_radiation.md:82–87, 238–242`; Terluna
    `atmosphere/radiative_convective/METHODS.md:143–148`). The interpolation clamps silently at the box's edges, and
    nodes far from Earth-like states are computed only on first use (`METHODS.md:156–158`). The checks of the reference
    reach less far: line sums against a direct Voigt sum from 3 Pa to 1 bar (`METHODS.md:92–94`); the correlated-k
    reduction at 288–290 K and on a saturated 330 K lunar column (Terluna
    `atmosphere/radiative_convective/README.md:130–131`), a test of the reduction alone
    (`notes/reference_radiation.md:210`); convergence on one 1.2 atm column at 288 K and a saturated 340 K column
    (`notes/reference_radiation.md:189–194`).
  - (b) The cloud-resolving runs of this work are CM1 with RRTMG, whose tables end at 1.05 bar, already exceeded over
    the lowest 7.5 km at 1.2 atm (`reach.tex:38, 80–81`; `assumptions.tex:79–82`). A 3 bar world inside the stated
    bounds lies past that radiation.
  - (c) Gravity, day length and starlight are left unbounded, while the body places the adapted models' limits along
    each: CM1 has run storms at the Moon's gravity and Earth's only, its gravity-scaled microphysics untested by
    similarity (`reach.tex:35–37`); its Sun and soil are built for days from a few Earth days to the Moon's
    (`reach.tex:37–38`); ExoPlaSim's model day drifts from the solar day beyond 20-day rotations
    (`reach.tex:57–60`); other stars' spectra lie beyond the calibrations (`reach.tex:62–64`, Table `tab:reach` row
    "Starlight").
  - (d) The sentence gives its three steps without their states: the curved-air table has been computed for one clear
    column of one world (`repairs.tex:87–88, 105–106`); the scheme is unbuilt; the cloud fit is still to be made on any
    world (`conclusions.tex:44`); the laboratory reach of the charging-law conditions is documented for the lunar storms
    alone (Terluna `climate/crm/README.md:2149–2150, 2168–2170`).

  Read together, the bounds present worlds up to 3.2 bar and 375 K, at any gravity, day and star, as the domain of a
  procedure that has run, in part, on one world, which the author's direction for this sentence excludes.
- **Proposed correction:** bound the class by what the evidence reaches and give each step its state. For example:
  "A modeller of a new world whose air is nitrogen and oxygen with water and modest carbon dioxide, near the test
  world's pressures and temperatures and with a scale height up to its three hundredths of the radius, would compute the
  radiative geometry from the world's own column, as was done once, for the test world; take the gas absorption from the
  reference's spectroscopy once a scheme is built and the spectroscopy checked, its line sums so far tested to 1 bar; and
  fit the cloud scheme to cloud-resolving runs of that world, a fit still to be made on any world, in a model whose
  radiation in the adapted CM1 ends at 1.05 bar, whose drop-size limits stay Earth's and whose lightning takes its sign
  from charging laws that Earth's laboratories can test at the lunar storms' conditions; gravity, day and starlight bound
  the class further, as Table~\ref{tab:reach} lists." If the 3.2 bar and 375 K figures stay, attach them to the
  longwave tables alone, as their node range.

### 2. BLOCKING: storms resolved at other gravities are given the standing of a laboratory test

- **Location:** `paper/sections/conclusions.tex:47–48` and `58–60`.
- **Text:** "Some Earth-fitted laws of storms can be tested independently of the world modelled, in laboratories on Earth
  or against storms resolved at other gravities." and "Resolving electrified storms at other gravities, with the same
  laboratory charging laws, could test those flash-rate laws, along the route Sergeev et al. propose: explicit charging
  in cloud-resolving runs."
- **Evidence.** A resolved electrified storm is a model result. Its flashes follow from WRF-ELEC's laboratory charging
  laws; from discharge thresholds kept at Earth's calibration, flash start at 0.9 of breakdown, 50 MV and 10 kV/m
  (`notes/electrification.md:85–87`; `assumptions.tex:203`, "Set for Earth's storms", Open); from Earth-fitted
  microphysics (`conclusions.tex:44–45, 67–69`); and from a grid that may set part of the rate (`results.tex:149–151`;
  `notes/electrification.md:97–99`, where how much of the lunar flash rate the grid sets "is open"). A flash-rate law
  set beside such a run is checked against the explicit model's own laws, at the world modelled, so the comparison
  depends on modelling that world. Sergeev et al. (2025, Sect. 4.2, arXiv v2 p. 9) call explicit charging in a
  cloud-resolving model "a possible route towards a more quantitative result" and, "in the absence of in-situ
  observations", "the best way of tuning" the parameterisations: in their account a source for tuning, standing in for
  observations. The last sentence names one of the conditions, the charging laws, and leaves the discharge thresholds and
  the grid unstated.
- **Proposed correction:** keep laboratories as the independent test and state the resolved-storm comparison in its own
  state. For example, open with "Some Earth-fitted laws of storms can be measured in laboratories on Earth." and close
  with "Electrified storms resolved at other gravities, the route Sergeev et al. propose for tuning such laws where
  observations are lacking, would set the flash-rate laws beside flashes computed from the same laboratory charging laws,
  WRF-ELEC's Earth-set discharge thresholds and a grid that may set part of the rate: a comparison of two models' laws at
  that gravity."

### 3. MAJOR: the domain of the proposed radiation scheme is the longwave tables' node box

- **Location:** `paper/sections/conclusions.tex:40–43`; `paper/sections/abstract.tex:21–25`.
- **Text (conclusion):** "A scheme built from the reference's line-by-line spectroscopy would replace the radiation's gas
  fits, the largest of the Earth fits, for air of nitrogen and oxygen with water and modest carbon dioxide at the
  pressures and temperatures its tables cover, up to 3.2~bar and 375~K, once that spectroscopy has been checked against
  an independent code, and the cloud optics would remain fits."
  **Text (abstract):** "… would replace the largest of these fits for nitrogen--oxygen air with water and modest carbon
  dioxide at the pressures and temperatures its tables cover, …"
- **Evidence.** The tables are those of ck.py, a longwave scheme of 16 bands over 1–3000 cm⁻¹ with k-tables for H₂O,
  CO₂ and O₃ (`notes/reference_radiation.md:82–90`; Terluna `METHODS.md:138–148`; R08 names them "its correlated-k
  tables"). The fits the scheme would replace include the shortwave ones, Lacis and Hansen's water absorptivity and the
  CO₂ and O₂ bands (`next.tex:14–16`; `repairs.tex:128–134`), for which the reference holds no table range: its solar
  calculation runs line by line, with CO₂ and O₂ cross-sections cached at nodes computed on demand
  (`METHODS.md:96–100`). Inside the box the checks reach 1 bar for the line sums (`METHODS.md:92–94`) and 330 K for the
  reduction (`radiative_convective/README.md:130–131`), and the planned independent check covers the design column
  (`next.tex:27–33`). After that check the stated domain would still exceed every check of the spectroscopy. The register
  records the range as table nodes (R08), a computational range; both sentences turn it into the scheme's domain. The
  water-fraction limit of 0.5 is a third bound of the same box, unstated.
- **Proposed correction:** separate the node range from the checked range. Conclusion, for example: "… for air of
  nitrogen and oxygen with water and modest carbon dioxide, once that spectroscopy has been checked against an
  independent code; its longwave correlated-k tables hold nodes up to 3.2 bar and 375 K, while its line sums have been
  tested to 1 bar and the tables' reduction on columns up to 330 K, and the cloud optics would remain fits." Abstract:
  "… for nitrogen--oxygen air with water and modest carbon dioxide over the pressures and temperatures where that
  spectroscopy is checked, while cloud would remain …".

### 4. MAJOR: the conclusion states Yang et al.'s judgement of the global means as fact and drops its conditions

- **Location:** `paper/sections/conclusions.tex:21–26`.
- **Text:** "… and a comparison by global-mean temperature and albedo can pass large differences in cloud: in the
  comparison of \textcite{yang2023cloud} on two tidally locked planets, three models came out broadly alike in
  global-mean surface temperature and albedo, while their cloud cover came to 27 and 41\% in the quasi-global
  cloud-permitting runs, which count cloud by a condensate threshold, and 82--97\% in two GCMs whose cover follows
  relative humidity, stability and large-scale ascent."
- **Evidence.** The cover values and the two ways of counting cover match Yang et al. (arXiv v1 p. 3; SI Text 3 and SI
  Table 3). The likeness of the global means is the authors' judgement: "broadly similar" (Discussion, p. 7) and
  "Overall, the simulated climates between CPM and GCM are broadly similar" (p. 4). Their numbers bound it. Planetary
  albedo was 18.1% in SAM against 22.1% (ExoCAM) and 29.1% (CAM3) on TRAPPIST-1e, and 37.4% against 39.0% and 47.0% on
  K2-72e (SI Table 3; p. 3: "smaller than those in the two GCMs"), and across the stellar-flux runs SAM's albedo was
  "~1/2 to 3/4" of the GCMs' (p. 4). Global-mean surface temperature came within 3.7 K on TRAPPIST-1e and spanned
  252.7–267.6 K on K2-72e. The 4 km cloud-permitting runs held their sea surface temperatures fixed at the last 30 days of
  a 40 km slab-ocean run of the same model (Methods, "Two steps for each experiment", p. 10), so the surface temperature
  in the comparison comes from the coarse run, and the clouds whose cover is cited acted on a fixed sea surface. The
  inference that a global-mean comparison "can pass large differences in cloud" thus rests on a judgement over albedos
  2–11 points apart and on surface temperatures held fixed in the runs that carry the cited cover. The results passage
  (`results.tex:81–86`) keeps "by the authors' account"; the conclusion drops it.
- **Proposed correction:** state the numbers and the condition, and land the inference on the size of the difference.
  For example: "… and global means can differ far less than cloud does: in the comparison of \textcite{yang2023cloud} on
  two tidally locked planets, cloud cover came to 27 and 41\% in quasi-global cloud-permitting runs over sea surfaces
  fixed from a coarser run of the same model, counted by a condensate threshold, against 82--97\% in two GCMs whose cover
  follows relative humidity, stability and large-scale ascent, while the planetary albedos lay 2--11 points apart and the
  authors judged the global-mean climates broadly similar."

### 5. MINOR: the calibrations' target omits the correlated-k emulation

- **Location:** `conclusions.tex:6–7`. **Text:** "the radiation's fits took calibrations to a line-by-line model".
- **Evidence:** the longwave correction was fitted against the reference's correlated-k emulation (claims H17, R11;
  `repairs.tex:120, 135–139`; `notes/reference_radiation.md:137`); the abstract names both (`abstract.tex:14–15`).
- **Proposed correction:** "calibrations to a line-by-line model and its correlated-k emulation".

### 6. MINOR: "moved it" reads as the design case; the 11.5 K loses its conditions

- **Location:** `conclusions.tex:30–33`. **Text:** "the longwave correction and the ice optics, switched on together,
  warmed the design case by 11.5~K in their test, and PlaSim's Earth-tuned cloud settings, pushed to the ends of their
  tests, moved it by up to about 6~K as the runs settled".
- **Evidence:** the nearest antecedent of "it" is the design case, while the cloud-setting tests ran from the Sun-and-tilt
  run (`results.tex:76–81`; Table `tab:states` row "Sun and tilt", `results.tex:27`; claim G16) and the full-column
  cloud-water test from the first calibrated run. The 11.5 K is a mean over years 10–19 of a run still warming toward
  306.8–307.1 K, with a correction fitted at 295 K (`results.tex:87–89`; G05, G13).
- **Proposed correction:** "… moved the Sun-and-tilt run by up to about 6~K as the runs settled"; and "warmed the design
  case by 11.5~K over years 10--19, with a correction fitted at 295~K".

### 7. MINOR: both dynamical cores are given a thin shell

- **Location:** `conclusions.tex:36–37`. **Text:** "while the dynamics keep a thin shell and constant gravity".
- **Evidence:** PlaSim's core is a thin shell and CM1's a flat slab, both at constant gravity (`assumptions.tex:53–55`;
  `next.tex:50–51`; Table `tab:inventory` rows "Dynamics").
- **Proposed correction:** "while the GCM's dynamics keep a thin shell and CM1's a flat slab, both at constant gravity".

### 8. MINOR: Titan's haze height enters only in the conclusion

- **Location:** `conclusions.tex:37–39`. **Text:** "Titan's haze stands about as tall against its radius as the test
  world's air".
- **Evidence:** the comparison holds against the source: Vincendon and Langevin infer "an aerosols scale height of
  80 ± 10 km" on Titan (abstract, p. 1), 3.1% of Titan's 2,575 km radius against the test world's 3.0%
  (`regime_calc.json` `scale_height`). The figure appears nowhere in the body or the register, and the manifest's
  locator for this source holds only the 65° quote. Beside `worlds.tex:77–78` ("Titan's air, at 0.8\% of its radius, is
  about a quarter as tall in proportion"), the reader meets two comparisons of Titan's height that differ fourfold, with
  the haze–gas distinction left to inference.
- **Proposed correction:** name the quantity and its source ("Titan's haze, with an aerosol scale height near 80~km,
  stands about as tall …"), and add the figure to the body or the register, with a manifest locator.

### 9. MINOR: "the ice aloft" for a column ice water path

- **Location:** `conclusions.tex:55`; `results.tex:155`. **Text:** "from the upward flux of graupel and the ice aloft".
- **Evidence:** in Sergeev et al.'s storm-resolving runs McCaul et al.'s scheme weights the upward graupel flux at
  −15 °C by 0.95 and the total ice water path, cloud ice, snow and graupel integrated from the ground to the model top, by
  0.05 (Sect. 2.2.1, Eqs. 1–3, arXiv v2 p. 3).
- **Proposed correction:** "from the upward flux of graupel at $-15$\,\textdegree C and the column's ice water path".

### 10. MINOR: cloud tops from one scheme are set beside flashes from another

- **Location:** `conclusions.tex:55–58`. **Text:** "At a sixth of Earth's gravity the cloud tops of six Morrison runs rose
  to 55--80~km, far above the storms the cloud-top law was fitted on, while the main electrified run … flashed at about a
  hundredth of Earth's average flash density".
- **Evidence:** the six runs use Morrison's scheme (G09); the main electrified run uses the NSSL scheme
  (`results.tex:142–149`; Table `tab:config`), and the body gives no cloud-top height for it. The pairing reads as tall
  tops and few flashes in the same storms.
- **Proposed correction:** give the electrified run's cloud-top heights, or say that the tops come from the Morrison runs
  and the flashes from the NSSL run.

### 11. MINOR: an unsourced universal joined to a consequence by "so"

- **Location:** `conclusions.tex:62–63`. **Text:** "Gravity stays fixed in a wave tank or a cloud laboratory on Earth, so
  whether gravity enters a model consistently is tested by similarity runs."
- **Evidence:** `verification.tex:39–41` supports the clause for the wind-tunnel tests made for SWAN's Mars runs, which
  varied the air's density and the wind; the universal for every wave tank and cloud laboratory carries no source here.
  The "so" joins two independent propositions: a similarity run tests the code's consistency, a property laboratories
  leave unmeasured at any gravity. Seven lines later the paragraph cites laboratory tests, at Earth's gravity, of a
  gravity-dependent law through σ/Δρ (`conclusions.tex:69–71`).
- **Proposed correction:** "Whether gravity enters a model consistently is a property of the code, tested by similarity
  runs; the laboratory tests made for SWAN's Mars runs varied the air's density and the wind at Earth's gravity."

### 12. MINOR: the CM1 pair was designed to measure a departure from similarity

- **Location:** `conclusions.tex:67–68`. **Text:** "CM1's gravity-scaled microphysics remains untested this way, since
  the pair of runs designed for it failed to convect".
- **Evidence:** Terluna designed the pair to compare lunar convection with Earth's stretched sixfold, with radiation off,
  recording that "the microphysics does not stretch" (`climate/crm/README.md:2510–2518`); the pair would measure how far
  the scaled microphysics departs from similarity (`next.tex:71–73`), an evidence state apart from SWAN's consistency
  test, which "this way" names.
- **Proposed correction:** "CM1 has no such test yet: the pair of runs designed to measure how far its convection, with
  gravity-scaled microphysics, departs from Earth's stretched sixfold failed to convect".

### 13. MINOR: the drop experiments' conditions and the collisional bound are dropped

- **Location:** `conclusions.tex:68–71`. **Text:** "experiments on the largest stable drops of other liquids at Earth's
  gravity agree with that capillary-length form within about 20\% \autocite{loftus2021physics}, and runs with Morrison's
  limits scaled by it are a step still to run."
- **Evidence:** Loftus and Wordsworth give the agreement within about 20% for "the maximum-sized drops of different media
  falling through various other media", where the drop's viscosity far exceeds the fall medium's (App. C1, p. 22). They
  also state that on present-day Earth hydrometeor collisions, in place of single-drop breakup, set the practical upper
  bound on raindrop size (Sect. 3.4, p. 9), the process Morrison's breakup in self-collection represents
  (`assumptions.tex:87–90`).
- **Proposed correction:** "… experiments on the largest stable drops of other media falling through other fluids agree
  with that capillary-length form within about 20\%, while on Earth collisions set the largest raindrops, so runs with
  Morrison's limits scaled by it would bound a sensitivity, a step still to run."

### 14. MINOR: the proposed ROCKE-3D pair loses two conditions and names its measure loosely

- **Location:** `conclusions.tex:79–81`. **Text:** "released and repaired ExoPlaSim on Earth-air planets at zero
  obliquity, rotating once in 16 and 64 days as in two of the ROCKE-3D runs of \textcite{way2018climates}, would measure
  them."
- **Evidence:** `next.tex:36–37` sets Earth's insolation and zero eccentricity as well. Way et al. ran each sidereal period
  at many insolations and with two oceans (Tables 2–3, arXiv v2 pp. 5–6), so "two of the ROCKE-3D runs" leaves the pair
  open. A released–repaired pair at each rotation measures the three defects' joint effect (`next.tex:38–39`, "the three
  defects' effect").
- **Proposed correction:** "… on Earth-air planets at Earth's insolation and zero obliquity and eccentricity, rotating
  once in 16 and 64 days, two of the sidereal periods of the ROCKE-3D runs of \textcite{way2018climates}, would measure
  their joint effect."

### 15. MINOR: the orbit default's bias is confined to slow and synchronous rotators

- **Location:** `abstract.tex:10–12`. **Text:** "bias ExoPlaSim's runs of slowly rotating and tidally locked planets that
  meet their conditions".
- **Evidence:** the orbit default's condition, an obliquity or eccentricity set without `fixedorbit`, holds at any
  rotation (`reach.tex:23–24`; W06; `notes/exoplasim.md:64–65`).
- **Proposed correction:** "bias ExoPlaSim's runs that meet their conditions, slowly rotating and tidally locked planets
  among them".

### 16. MINOR: "computed for each world's column" for a table computed once

- **Location:** `abstract.tex:13–14`. **Text:** "a method whose table is computed for each world's column".
- **Evidence:** the table has been computed for one clear design column of the test world (`repairs.tex:87–88,
  105–106`).
- **Proposed correction:** "a method whose table is computed from the world's own column", the conclusion's wording
  (`conclusions.tex:6`).

### 17. MINOR: the results' Yang passage omits the fixed sea surface

- **Location:** `results.tex:81–86`. **Text:** "… against 26.9 and 41.1\% in the cloud-permitting model, which counts
  cloud by a condensate threshold, while the three models' global-mean surface temperatures and albedos came out broadly
  alike by the authors' account."
- **Evidence:** as in Finding 4: the attribution stands, while the fixed sea surface of the 4 km runs (Methods, p. 10) and
  the albedo spread (SI Table 3) go unstated.
- **Proposed correction:** add "over sea surfaces fixed from a coarser run of the same model" after "cloud-permitting
  model", and the albedos, 18 and 37\% against 22--29 and 39--47\%.

### 18. MINOR: the step's second avoidance goes unnamed

- **Location:** `results.tex:44–46`. **Text:** "the synodic clock, the Moon's own tilt and the recalibrated split of
  sunlight, a step that joined a general repair and two avoidances, one of them output bookkeeping, with a calibration".
- **Evidence:** the apposition counts four changes and the list names three. The second avoidance is the year of whole
  model days, 17,160 steps in place of 17,280 (Table `tab:repairs`, `appendix.tex:60`), adopted on 2026-09-29 with the Sun
  and tilt repairs (Terluna `climate/gcm/README.md:173–178`); the "Sun and tilt" row of Table `tab:states`
  (`results.tex:27`) omits it as well.
- **Proposed correction:** "the synodic clock, a year of whole model days, the Moon's own tilt and the recalibrated split
  of sunlight", and the same addition in the table row.

### 19. MINOR: "the general repairs … measured singly" for two of them

- **Location:** `results.tex:93–94`. **Text:** "while the general repairs of units and constants, measured singly, moved
  it by 1.6--2.5~K".
- **Evidence:** two general repairs were measured singly (G01; `abstract.tex:18–19`; `conclusions.tex:33`).
- **Proposed correction:** "while the two general repairs of units and constants measured singly moved it by
  1.6--2.5~K".

### 20. MINOR: the source comment's word and the test's maximum

- **Location:** `assumptions.tex:22–24`. **Text:** "a value its source comments call largely arbitrary, … stock SWAN
  misses a sixfold gravity-similarity test by 5.44\% in significant wave height".
- **Evidence:** the upstream comment calls the bend "mostly arbitrary, intended to have zero effect on typical simulations
  (which stop at 1 Hz)" (`models/swan/README.md:55–56`); 5.44% is the largest difference at matching points
  (`models/swan/README.md:84`; `notes/waves.md:51`), which the abstract and conclusion give as "up to 5.4%".
- **Proposed correction:** "mostly arbitrary"; "by up to 5.44\%".

### 21. MINOR: the ROCKE-3D comparison carries configuration with physics

- **Location:** `next.tex:38–42`. **Text:** "with the released radiation, fitted on columns like theirs … and setting the
  repaired climate beside ROCKE-3D's would separate the defects' effects from the two models' own physics."
- **Evidence:** Way et al.'s runs used modern Earth topography with some shallow seas replaced by land, a 100 m Q-flux=0
  ocean or a dynamic ocean limited to 1,360 m, 984 hPa of N₂-dominated air with 400 ppmv CO₂ and 1 ppmv CH₄, and ozone
  set to zero (Sect. 2, arXiv v2 pp. 3–4). The comparison carries these differences with the physics, and "columns like
  theirs" holds with ExoPlaSim's ozone removed.
- **Proposed correction:** "… would separate the defects' effects from the two models' physics and configurations, with
  ExoPlaSim's ozone removed as in Way et al.'s runs."

### Outside the scope, noted for the author (uncounted)

- `next.tex:14–16`: "would hold on any column whose gases and pressures that spectroscopy covers, on another world as on
  the test world" carries the domain issue of Finding 3.
- `introduction.tex:73–75` carries the phrase of Finding 15.

## 3. Checked and sound

- **Numbers in the conclusion and abstract against the register and data:** four forms and five defects
  (`assumptions.tex:100–129`); +0.23 to the cover, cap 0.8 (W06, H07; `regime_calc.json`: N = 60, model day 6.203 d,
  0.228); 33° beyond 20-day rotations (H23, W02; N = 12, 32.7°); 17% over and 8% short (H23, 8.3%); Earth's tilt and
  summer rain to 60° (H24, G02); land under 0.5 mm a day from 9 to 36% in the two-year test (G02; Terluna
  `climate/gcm/README.md:659–664`); 2.4 W/m² and 0.9 K while gaining heat (G17; the albedo fall of 0.008 times about
  293 W/m² of mean sunlight gives 2.3 W/m², consistent); 27 and 41% and 82–97% (Yang p. 3; SI Table 3); at least 20 K
  (G14; `repairs.json` −19.999 K against an uncalibrated run still warming); 11.5 K (G05); about 6 K (G05, −5.9 K
  settled); 1.6–2.5 K (G01, settled values); 5.8 W/m² (H11); 65° (Vincendon and Langevin, Sect. 1); 3.2 bar and 375 K as
  node values (R08); 55–80 km (G09); a hundredth (G10; ratio 0.0081); 0.3% and up to 5.4% (V04); the knee reducing the
  linear input above 1 Hz (`models/swan/README.md:40–42`); 2.46 (H21; 2.457); 295 K and 5.0 to 3.0% (G04, S07); 16 and
  64 days sidereal at zero obliquity (Way et al., Sect. 2 and Tables 2–3); three hundredths (`scale_height` 0.0301).
- **Physical inferences:** the Sun clock keeps every zonal mean (Terluna `climate/gcm/README.md:186–187`) and the orbit
  default the global mean of the arriving sunlight; with `FREQ1 = f·g_E/g` the scaled knee sits at g/g_E Hz, so stock
  SWAN departs from the scaled image above g/g_E Hz under weaker gravity and above 1 Hz under stronger, as
  `assumptions.tex:24–27` states; the similarity statements of `conclusions.tex:63–67` and `reach.tex:38–42` keep to
  consistency on the paths run (`notes/waves.md:62–68`).
- **Attributions:** Braam et al. set flash rates from cloud-top height with coefficients tuned to Earth's observed flash
  rates, for Earth-like air on Proxima Centauri b (Sect. 2.4, Sect. 4); Sergeev et al. used N₂ air with 400 ppm CO₂ and
  water, without O₂ or O₃, at 0.25–10 bar (Sect. 2.3), the graupel-flux law in their N1280 storm-resolving runs and the
  cloud-top law in their N96 runs (Sect. 2.2), with coefficients from observations of Earth's storms; Yang et al.'s cover
  values, cover definitions, quasi-global domain, the GCMs' cover drivers and TRAPPIST-1e's 6.1-day rotation; Vincendon
  and Langevin's 65° for Titan's surface–haze separation codes; Way et al.'s periods, orbit and insolation; Loftus and
  Wordsworth's r_max ∝ √(σ/gΔρ) (Eq. 26) and the 20% agreement (App. C1); Deitrick et al.'s "Most studies of exoplanet
  atmospheres using GCMs … have adapted codes developed for Earth or solar system planets" (Sect. 1), which supports the
  abstract's "Many". The `assumptions.tex` sentence attributes no configuration to Banfield et al.
- **Evidence states:** the abstract's defect sentence ("by the code's own arithmetic"), its "built to hold", and "the only
  world the repaired codes have run on away from Earth's values"; the conclusion's "a step still to run", "would
  measure" and "once … checked"; the laboratory reach of the charging-law conditions (Terluna
  `climate/crm/README.md:2149–2150, 2168–2170`; N01); the caption of Table `tab:reach` and its Seas row ("built for",
  "tested at a sixth of Earth's on the tested paths", the unused options at Earth's constants;
  `models/swan/README.md:204–271`; `notes/waves.md:265–276`); the `next.tex` paragraph's sidereal periods, insolation of
  1,360.67 W/m², zero obliquity and eccentricity, arithmetic tests named as such, and the reclassification rule.
- **Bibliography:** the six entries match their manifest records and the archived originals.

## 4. Counts

| Severity | Count |
|---|---|
| BLOCKING | 2 (Findings 1, 2) |
| MAJOR | 2 (Findings 3, 4) |
| MINOR | 17 (Findings 5–21) |
| Total | 21 |

Two further notes outside the scope are listed uncounted.
