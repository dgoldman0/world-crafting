# Editorial round 7: evidence review of the closing section, the abstract and revised passages

## 1. Record

- **Reviewer.** A fresh Claude subagent (Claude Opus 5.5), acting as technical reviewer for evidence. It saw no
  earlier review and opened nothing under `paper/review/` (apart from writing this file) or `paper/notes/`. One
  `git status` listing printed the name of an untracked round-7 prose record; that file stayed unopened.
- **Date.** 2026-10-18.
- **Snapshot.** Commit 654ebdf (654ebdfd42989247f0639e0549c0a637c5927c37). Every repository file was read with
  `git show 654ebdf:<path>`; Terluna was read at 186b294 with `git -C ../terluna show 186b294:<path>`; the research
  drive was read in place. No model or test was run. Scratch copies and text extracts are in
  `/tmp/claude-1000/r7evid_work/`.
- **Method.** Each number, condition, attribution, evidence state and physical inference in scope was traced to the
  body, to its entry in `paper/claims.json`, and from there to the run record, the pinned upstream source or the
  archived original; arithmetic was redone where the record gives its inputs.

### Files in scope (sha256 of `git show 654ebdf:<path>`)

| File | sha256 | Part in scope |
|---|---|---|
| `paper/sections/conclusions.tex` | `30e4558960694cf815e0d9a4dc6ef4d5526651524553ef1aba5f36da26abbb0f` | whole section |
| `paper/sections/abstract.tex` | `5a013c5fcebe028beceaf3a9421919f19503851b531363301c6f9033154acb36` | whole abstract |
| `paper/sections/results.tex` | `ad92675e8c2d2a15beb6fa522da464dcd77ad8f260f883042658f4d2928b8e43` | l. 44–48 and the Sun-and-tilt row (l. 27); Yang et al. (l. 90–96); flash-rate laws (l. 152–156) |
| `paper/sections/reach.tex` | `de4c7f47235170d6f3a78db67d1d63ee3299b36a15f1682d818e450aff516551` | l. 38–42; Seas row (l. 114) |
| `paper/sections/next.tex` | `a68a6c3ab3a3a7d0374993c2d92e9cbb4a18a92cbe1a6f451d995ab32d5ba84d` | l. 13–17; l. 36–44; l. 79–85 |
| `paper/sections/repairs.tex` | `2d5eb8d77bb2525244b3610a68d6554183ee7fe463310e7f6af37357f00240f0` | l. 106–109 |
| `paper/sections/introduction.tex` | `095321a4347073d02caf526e522cde34caf58d2c56ef30378114ae819484df60` | l. 71–75 |
| `paper/sections/assumptions.tex` | `4c2d7f99690986359955e327fe1ef9f1bc317c026da45221c032d59df8e81fd0` | l. 21–27 |

The scope hashes equal those in the brief.

### Evidence relied on (sha256)

Repository at 654ebdf:

| File | sha256 |
|---|---|
| `paper/claims.json` | `6b4718a2be6128506d693a87cdcc2753194d0d8d39cce9c0a9038ed490f0cfb8` |
| `paper/references.bib` | `c0c9662b362141759bce9a27bb566e7ee6a00479ef773273f1dc109d7888747e` |
| `paper/sources/manifest.json` | `194f4261f8ef39960eb7140ba3a06c4cea9c2a44a12ad1031bc7750c6803988f` |
| `paper/data/regime_calc.json` | `7a2935a8fbe6086c577097b838825c5415ba99f0adf040af62f5e4bcd370e7d1` |
| `paper/data/repairs.json` | `3dada16f0e39dba9fe576587da12764ceceaa1ad4f421b33d8dffbe1826b4987` |
| `paper/sections/worlds.tex` | `453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112` |
| `paper/sections/verification.tex` | `4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00` |
| `paper/sections/appendix.tex` | `ebab8ca204f81ed41d9185d456353a43a9f59e5307290695277b4614b5bd6635` |
| `paper/sections/availability.tex` | `496434ae301b500a3f7dcec2750af08b8a4d1789c437844ab1318e3ff35f762d` |
| `notes/reference_radiation.md` | `348501fa28bbe855f6cc99a200d81004fb4163fe91dd0ccccaa13517bbae2730` |
| `notes/electrification.md` | `2cd81eb8edbd77348133a1e4aaca859b52ca4d0015bc5b26bf12e5d93308f59f` |
| `notes/defect_log.md` | `c6e7aa541898ce52b68eae35907a9d501885a6330f062f04a6899ad144dd491d` |
| `notes/verification_record.md` | `983329688203341ce74e4253acfb72e490b9d8efd252893d1d7b76dc97413ddc` |
| `notes/waves.md` | `9f7a775ed1b8a297a4d4a8cf0cd416a8e732b8367cf9f241aaa15dc69cb28102` |
| `models/swan/README.md` | `abb218a0608362f5d2d58cbb72b4d6defcaacb02f06d7123690d862dbc15109d` |
| `models/cm1/fortran/terluna_branched.F` | `36ea5092380f4ac52b2284bea49c8f70c25286cc33baeee309730bfe5eee4288` |

Terluna at 186b294:

| File | sha256 |
|---|---|
| `climate/gcm/README.md` | `267413c2aa248c3b7581d796ef83de826fbe6764d6d03c9abd1677fee03150fb` |
| `climate/crm/README.md` | `95776d41c55b3a3a372d3752ff367b66c45f3a98a1609b2cddfd953f49754acd` |
| `climate/results/crm/elec_charging_laws.json` | `8a275a971505530a9951288da7e65806e338e0465874c466ada339d9192339cb` |
| `climate/crm/elec_analysis.py` | `7eef6eaf777860d2ff36fa52f71b87f1a43d44c1043c10df360f5180b8d90b76` |
| `climate/waves/first_experiments.md` | `959868b935ca29c3b4f3f929c987036627f81c884064e4f5887e1a29ec60b2a5` |
| `climate/waves/audit.md` | `ec3eab1ebf6a82f9863128a760e15553ccedf92b4e03d06e9f96481d92087135` |
| `climate/waves/runup.md` | `7104b129074b1a8b361177ee1717a07dc35faf06f47b7b68cbeaa28fe66cd357` |
| `climate/waves/README.md` | `87fe5f3621fee9cfa5e402b2e5a5132aa93b81052ce6b6b2c1f5708eb51a4ab2` |
| `research/decisions.md` | `cfca4e5a14d98925bf2f2584566f5a3a1f76970d9f7494ac3cab6f51030816c2` |

Research drive (`/media/projectspace/terluna-research/`):

| File | sha256 |
|---|---|
| `gcm-runs/A28_dim5/progress.json` | `619f3de9adeafa38803e60fc4b311278f9c3bf9f681adcc1f69c05b9b16d8e61` |
| `gcm-runs/A28_dim5_sun_test/progress.json` | `0d8563dbbe8c815b92c88b29943c7a068e9d4b9fd743738a9da38ba08df7b816` |
| `gcm-runs/A28_dim5_moon/progress.json` | `d287252f152cb52f5b9f07f35f1e51fca87bddab6226fd960a1c35bdfc31be6d` |
| `crm-runs/box_0e_elec_takahashi/terluna_flashes.txt` | `ee9254a0fe719eb2ad8e5c9a803440ee58bc181bd01fb3d5584c8647fca95c3a` |

Pinned upstream sources (archives match `models/pins.sha256`):

| File | sha256 |
|---|---|
| `swan4151/swancom3.ftn` from `upstream/swan4151.tar.gz` (`325c229f…26bb`) | `b164c7b9ac8f94672b637e114dbacad503b624c8c1c8ae50339b80c0083558af` (the README's "before" hash) |
| `exoplasim/__init__.py` from `upstream/exoplasim-3.4.2.tar.gz` (`fae502a9…64c2`) | `07ea85554ef45172eee24d68c0e8be61b98db86ac276cc6f246ad5c161183903` |
| `exoplasim/plasim/src/rainmod.f90` (same archive) | `8feb589634236577cf7c94dbac05bf2fa01c9e67f2c1da5b0b770ede82bee295` |
| `exoplasim/plasim/src/plasim.f90` (same archive) | `04fd8941a51b9b70cf07791b54bcde33d40deebf7e19d0e60c5eb053748b9129` |
| `upstream/wrf4-elec/module_discharge_msz.F` | `1cde4951dfc5e01f72bccb3437be6e6c03dd0e239b49b8f6b6485d9217a7c283` (equals its pin) |

### Source originals opened (text extracted with `pdftotext`; each hash equals the manifest's)

| Original | sha256 | Read |
|---|---|---|
| `yang2023cloud.pdf` (arXiv v1, author version) | `0637811e9ae240d47ab39da7d905421709afb685df2d0050f6f8ffdfa2d8bc41` | abstract; Results "Clouds" (pp. 3–4); Methods "Cloud-permitting simulations" and "Two steps" (pp. 9–10) |
| `yang2023cloud_si.pdf` (publisher SI) | `1cc0a5828d0dc0301b1b2aa712c48f58d8c312a6470e6c1d11df47a806ac5554` | Text 3; Table 3 |
| `braam2022lightning.pdf` | `26486cfc19cb2185ca8f98a22bcbadf40a526afed1f8b3d460154915b58cf8c7` | abstract; Sect. 2.3–2.4; Sect. 4.3 |
| `sergeev2025lightning.pdf` | `b2c3352f4ad065bd894341eb76741ff541b1bf4c4824612ae7e6404bd373c6df` | abstract; Sect. 1–2 with Tables 1–2; Sect. 3.1; Sect. 4.2 |
| `vincendon2010spherical.pdf` | `afcdf418a60ce367c8b16c12d68c1bac36ea2fd8e0013498ea3553c0cbd8a7e9` | abstract; Sect. 1 |
| `way2018climates.pdf` | `476e3e967e5d7eeafea1f386fc801851106365653bd3d9132c5821edb7164820` | abstract; Sect. 2 (configuration); Table 2 |
| `loftus2021physics.pdf` (version of record) | `d080f1289e115952977c4b09fa0f9e1b8d93f305315804c84a7878ed0a805d2c` | Sect. 3.4; Sect. 5.3; App. C1 |
| `loftus2021physics_arxiv.pdf` | `18fbf925ba0d68443cf445281ce6727b1a8ba0a1270e9c30e81742b5d53491af` | extracted and hashed only |
| `deitrick2020thor.pdf` | `52da49f440c5f77cb35cd99b8ec66274d192e7461c33ea26695dcd8a823b7d7c` | Introduction (for the abstract's first sentence) |

Yang et al.'s main-text numbers were checked against the arXiv author version, which the manifest archives in place
of the paywalled version of record; the SI is the publisher's.

### What was read

- Every section of the paper at 654ebdf, in full; `paper/main.tex` header.
- All 108 entries of `paper/claims.json`; the manifest entries of the six named sources; their `references.bib`
  entries.
- `notes/reference_radiation.md` l. 1–130 and 200–290; `notes/electrification.md` whole; `notes/defect_log.md` A1–A3,
  B7, B24–B28; `notes/verification_record.md` l. 160–255; `notes/waves.md` (the constants and similarity passages);
  `models/swan/README.md` l. 1–120; `paper/data/repairs.json` and the relevant keys of `regime_calc.json`.
- Terluna: `climate/gcm/README.md` l. 160–260 and 600–700; `climate/crm/README.md` l. 1448–1460, 2060–2175,
  2236–2250, 2365–2420; `climate/results/crm/elec_charging_laws.json`; `climate/crm/elec_analysis.py` l. 30–60 and
  265–330; `climate/waves/first_experiments.md` l. 20–60; `audit.md` l. 40–62; `runup.md` l. 196–214;
  `climate/waves/README.md` l. 1–40; `research/decisions.md` (the electricity entry).
- Drive: the three GCM `progress.json` files above (means recomputed); the Takahashi run's flash log (kinds counted).
- Upstream: `swancom3.ftn` l. 1705–1810; ExoPlaSim `__init__.py` l. 2605–2635, `rainmod.f90` l. 1869–1895,
  `plasim.f90` l. 1290–1302; WRF-ELEC `module_discharge_msz.F` l. 2700–2775; `terluna_branched.F` header.

## 2. Findings

### 1. BLOCKING: the abstract states the spectroscopy's independent check as made

- **Location.** `paper/sections/abstract.tex:21–24`.
- **Text.** "A radiation scheme built from the reference's line-by-line spectroscopy would replace the largest of these
  fits for nitrogen--oxygen air with water and modest carbon dioxide over the pressures and temperatures where an
  independent code has checked that spectroscopy"
- **Evidence.** `verification.tex:63–69`: "Its carbon dioxide, oxygen, collision-induced absorption and sunlight on
  the lunar column have yet to be compared with an independent code." `next.tex:28–32` makes the LBLRTM and DISORT runs
  of the design column a step still to run. Claim V16: "no independent code checks its CO2, O2, collision-induced or
  solar calculation on the lunar column". `notes/reference_radiation.md:20–23`: the only cross-code check, PyRADS,
  covers water-only longwave at constant gravity. The conclusion keeps the state ("a check so far planned on the
  design column alone", `conclusions.tex:41`); the abstract drops it, so its reader meets the check in the perfect
  tense with no state, and the sentence bounds a class of air by a check that has yet to run. The abstract of the
  parent commit (8bfd069) carried the condition: "once that spectroscopy is checked against an independent code".
- **Correction.** "... would replace the largest of these fits for nitrogen–oxygen air with water and modest carbon
  dioxide, over the pressures and temperatures of a check of that spectroscopy against an independent code, a check
  still to be made, while cloud would be ..."

### 2. BLOCKING: the next steps give Takahashi's law positive ground strikes; the run made negative ones

- **Location.** `paper/sections/next.tex:79–83`.
- **Text.** "The sign of the lunar lightning changes with the laboratory charging law chosen, ... would decide whether
  the lunar ground strikes are negative, as under Saunders and Peck's law, or positive, as under Takahashi's, and so
  the polarity that protection on the ground and in the air must meet.\claim{N01}"
- **Evidence.** The one run under Takahashi's law with ground strikes allowed, `box_0e_elec_takahashi` (days
  40.5–42, WRF-ELEC's −7 °C rule, leakage off, before the ventilation repair), logged 10 ground strikes, all of kind 2
  and none of kind 3: drive `crm-runs/box_0e_elec_takahashi/terluna_flashes.txt` (10 rows of kind 2, 0 of kind 3);
  Terluna `climate/results/crm/elec_charging_laws.json`, `second_lunar_day`, `box_0e_elec_takahashi`:
  `negative_to_ground` count 10, positive charge 0 C in each, negative charge median 204.2 C, with no
  `positive_to_ground` entry. Kind 2 is negative charge to ground and kind 3 positive (`terluna_branched.F:24–25`;
  WRF-ELEC `module_discharge_msz.F:2745–2770`, "DISCHARGE IS POSITIVE" for 3 and "DISCHARGE IS NEGATIVE" for 2).
  Terluna `climate/crm/README.md:2242–2244`: "The Takahashi windows ran without leakage as well; their arrangement of
  charge follows from the law's sign, while their ground strikes carry the same leftover charge as
  `box_0e_elec_ground_rule`'s." The first Takahashi window (days 10.5–12, 5-km rule) made no ground strike. What
  inverted under Takahashi's law is the storms' arrangement of charge (README:2108–2120; defect log B7; claims G11,
  H22). N01, the marker on the sentence, holds the impact speeds and cloud water only. The opening sentence also drops
  G11's conditions (two windows of an earlier run, before the ventilation repair, leakage off), which
  `results.tex:158–160` and `conclusions.tex:47–48` keep.
- **Correction.** "In two windows of an earlier electrified run, made before the ventilation repair and with leakage
  off, Takahashi's law inverted the storms' arrangement of charge, while the second window's ten ground strikes, which
  carried charge left by a run without leakage, stayed negative as under Saunders and Peck's. The sign of the charge
  rimed ice takes at 4–8 m s⁻¹ in 0.02–0.2 g m⁻³ of cloud water at −5 to −16 °C, measured in a laboratory, would
  decide which arrangement the lunar storms take; the sign of their ground strikes under each law awaits a run with
  leakage on." The same reading appears at `results.tex:162` ("the sign of the lightning therefore depends on
  laboratory laws"), outside this round's scope.

### 3. BLOCKING: the closing sentence places cloud-resolving runs outside the adapted codes

- **Location.** `paper/sections/conclusions.tex:83–86`.
- **Text.** "The fits, which moved the test world's climate furthest, would be refitted or replaced on another world
  from evidence outside the adapted codes: the gas fits from line-by-line spectroscopy checked against an independent
  code, the cloud from cloud-resolving runs of that world, and the drop and charging laws inside those runs from
  laboratory tests."
- **Evidence.** The cloud-resolving model of this work is CM1, one of the four adapted codes
  (`introduction.tex:58–62`). The paper's plan fits PlaSim's cloud to CM1 runs (`next.tex:19–26`: "Forcing CM1 ... the
  cloud cover and water by pressure of those runs become the target to which PlaSim's humidity thresholds and its
  cloud-water profile are fitted"); `conclusions.tex:42–44` adds that "those runs compute with Earth-fitted
  microphysics of their own"; and the storms paragraph calls resolved storms "a comparison between models"
  (`conclusions.tex:59–60`). A cloud fitted to cloud-resolving runs is a calibration of one model to another; the
  closing sentence gives it the state of evidence from outside the adapted codes.
- **Correction.** "... would be refitted or replaced on another world from evidence outside the GCM: the gas fits from
  line-by-line spectroscopy checked against an independent code, the cloud from cloud-resolving runs of that world, a
  comparison between models whose microphysics is fitted to Earth, and the drop and charging laws inside those runs
  from laboratory tests." (Finding 11 concerns the same sentence's relative clause.)

### 4. MAJOR: "which polarity the model's lunar lightning takes" reaches past the record

- **Location.** `paper/sections/conclusions.tex:46–50`.
- **Text.** "... the test world's storms took opposite polarities under the two; a measurement of that sign at the
  impact speeds, cloud water and temperatures of the lunar storms would decide which polarity the model's lunar
  lightning takes."
- **Evidence.** As in finding 2: the storms' arrangement of charge inverted (Terluna `climate/crm/README.md:2108–2120`),
  while the Takahashi window's 10 ground strikes were negative, as the Saunders and Peck window's 21 were
  (`elec_charging_laws.json`; the run's flash log). Read as ground-flash polarity, the clause states a change the run
  lacks. The record's deciding conditions are hail's: 4–8 m s⁻¹ in 0.02–0.2 g m⁻³ at −5 to −16 °C (claim N01;
  `notes/electrification.md:91–96, 130–132`; README:2142–2170), where graupel strikes at 0.95–3.6 m s⁻¹.
- **Correction.** "... a measurement of that sign at hail's impact speeds of 4–8 m s⁻¹, in 0.02–0.2 g m⁻³ of cloud
  water at −5 to −16 °C, would decide which way up the model's lunar storms hold their charge."

### 5. MAJOR: the planned scheme's reach to another world leaves the starlight free

- **Location.** `paper/sections/next.tex:14–17`; `paper/sections/conclusions.tex:38–42`;
  `paper/sections/abstract.tex:21–24`.
- **Text.** next.tex: "... and, once that spectroscopy is checked, would hold on columns within the gases, pressures
  and temperatures of the check, on another world as on the test world." conclusions.tex: "for air of nitrogen and
  oxygen with water and modest carbon dioxide at the pressures and temperatures over which ..." abstract.tex: "for
  nitrogen--oxygen air with water and modest carbon dioxide over the pressures and temperatures where ..."
- **Evidence.** The reduced scheme replaces Lacis and Hansen's shortwave fit as well as Sasamori's longwave
  (`next.tex:14–15`). A correlated-k shortwave carries the incident spectrum in its band and g-point weights, and the
  planned check uses the design column under the shield-filtered TSIS-1 Sun. Table `tab:reach` (`reach.tex:108`) puts
  "Other stars' spectra" beyond the adapted models, and `reach.tex:62–64` requires the shortwave of M-dwarf planets to
  be refitted "against the reference with the star's spectrum". Each sentence bounds the scheme by gases, pressures and
  temperatures alone, so "on another world as on the test world" carries a planned scheme, to be checked on one
  column, to worlds of any star.
- **Correction.** Add the condition at each use: next.tex "... would hold on columns within the gases, pressures and
  temperatures of the check, under the starlight its shortwave is built for, on another world as on the test world";
  conclusions.tex and abstract.tex "... and under the starlight it is built for".

### 6. MINOR: the check's tense, and the checks already made

- **Location.** `paper/sections/conclusions.tex:40–41`.
- **Text.** "over which an independent code has checked that spectroscopy, a check so far planned on the design column
  alone"
- **Evidence.** The clause puts "has checked" and "planned" on the same check. The line-by-line model already has two
  recorded checks, PyRADS for water-only longwave at constant gravity and a Monte Carlo Rayleigh reference to optical
  depth 1.5 (`verification.tex:63–68`; V16; `notes/reference_radiation.md:20–25`); the planned check is the full
  design column with every absorber (`next.tex:28–32`).
- **Correction.** "over which an independent code checks that spectroscopy, a check planned on the design column;
  PyRADS has so far checked its water-only longwave at constant gravity".

### 7. MINOR: "the radiation's gas fits, the largest of the Earth fits"

- **Location.** `paper/sections/conclusions.tex:38–40`.
- **Evidence.** The effect of at least 20 K came from calibrating a Rayleigh multiplier and the water continuum
  (`conclusions.tex:28–29`; `results.tex:36–39`; G14), a scattering fit and a gas fit; the abstract names "the
  radiation's gas and scattering fits" (`abstract.tex:14`), and the reference carries Rayleigh scattering
  (`repairs.tex:122–124`), so the scheme would replace both.
- **Correction.** "the radiation's gas and scattering fits, the largest of the Earth fits".

### 8. MINOR: the reason given for where the error shows

- **Location.** `paper/sections/conclusions.tex:20–21`.
- **Text.** "A modeller finds such an error in maps of sunlight by longitude and of rain by season, since global means
  can differ far less than cloud cover does."
- **Evidence.** In the two-year Sun-and-tilt test the global cloud cover moved 0.2 points (24.9% over `A28_dim5`'s
  years 15–24; 24.7 and 24.8% in the test's two years; drive `progress.json` files), while the clouds' effect in
  sunlight moved 2.4 W m⁻² and the surface 0.9 K. The premise of the "since" clause comes from Yang et al.'s
  comparison of parameterized with resolved cloud under different definitions of cover, a difference in model
  structure. The direct reason is in the sentences before: the clock keeps every zonal mean, and both errors keep the
  global-mean arriving sunlight.
- **Correction.** "A modeller finds such an error in maps of sunlight by longitude and of rain by season, since the
  global-mean sunlight stays right and the global means moved by under a kelvin." Yang et al.'s comparison can then
  stand as its own point, for example "Global means can also agree where cloud cover differs widely: in the comparison
  of ..."

### 9. MINOR: Sergeev et al.'s proposal and "at other gravities"

- **Location.** `paper/sections/conclusions.tex:56–58`.
- **Text.** "Electrified storms resolved at other gravities, the route Sergeev et al. propose for tuning such laws
  where observations are lacking"
- **Evidence.** sergeev2025lightning, Sect. 4.2: "A possible route towards a more quantitative result is to use an
  explicit electric charging scheme coupled with a cloud-resolving model (e.g., Fierro et al. 2013). In the absence of
  in-situ observations, this may be the best way of tuning convection- or microphysics-based parameterisations in
  climate models for different planetary atmospheres." Gravity enters with this paper's application of the route.
- **Correction.** "Electrified storms resolved at other gravities, an application of the route Sergeev et al. propose
  for different planetary atmospheres where observations are lacking, would set ..."

### 10. MINOR: Loftus and Wordsworth's statement on Earth's largest raindrops stands without its citation

- **Location.** `paper/sections/conclusions.tex:71`.
- **Text.** "On Earth, collisions set the largest raindrops"
- **Evidence.** loftus2021physics, Sect. 3.4: the physics is complicated "in many situations (such as on present-day
  Earth) by the fact that the practical upper bound on raindrop size is not set from individual raindrop breakup but
  rather from hydrometeor collisions (e.g., Barros et al., 2010)". The citation sits on the sentence before.
- **Correction.** Add `\autocite{loftus2021physics}` to this sentence.

### 11. MINOR: the closing sentence's relative clause covers fits with no measured climate effect

- **Location.** `paper/sections/conclusions.tex:83–86`.
- **Text.** "The fits, which moved the test world's climate furthest, ... and the drop and charging laws inside those
  runs from laboratory tests."
- **Evidence.** Morrison's drop limits have no run (defect log B28: "No run tested it"; `reach.tex:36–37`, "their
  effect at other gravities is unmeasured"); the charging laws set the storms' arrangement of charge (G11) and carry no
  climate measure. The ranking by form (`results.tex:86–90`) rests on the radiation fits and the cloud settings.
- **Correction.** "The radiation and cloud fits, which moved the test world's climate furthest, would be refitted or
  replaced ..., and the drop and charging laws inside those runs from laboratory tests."

### 12. MINOR: Braam et al. simulated one planet

- **Location.** `paper/sections/results.tex:152–153`.
- **Text.** "The flash-rate laws with which \textcite{braam2022lightning} estimated lightning on tidally locked planets
  with Earth-like air"
- **Evidence.** braam2022lightning, abstract: "We simulate the atmosphere of Proxima Centauri b orbiting in the
  Habitable Zone of its M-dwarf star, but the results apply to similar M-dwarf orbiting planets." Their law is the
  oceanic Price and Rind fit, Eq. (1) of Sect. 2.4, whose coefficients "have been tuned to match observed LFRs on
  Earth" (Sect. 4.3). The rest of the sentence checks: Sergeev et al. simulated one planet, TRAPPIST-1e, in N₂ air with
  400 ppm CO₂ and no O₂ or O₃ at 0.25–10 bar (Sect. 2.3, Table 2), with Price and Rind's cloud-top law in coarse runs
  and McCaul et al.'s graupel flux at −15 °C and total ice water path in storm-resolving runs, "originally derived from
  observations of severe thunderstorms over the United States" (Sect. 2.2, Table 1).
- **Correction.** "The flash-rate laws with which \textcite{braam2022lightning} estimated lightning on Proxima
  Centauri b with Earth-like air, and \textcite{sergeev2025lightning} on TRAPPIST-1e with oxygen-free nitrogen air at
  0.25--10~bar, ..."

### 13. MINOR: Vincendon and Langevin's limits concern remote-sensing codes and are typical values

- **Location.** `paper/sections/repairs.tex:106–109`.
- **Text.** "How close to the horizon a flat treatment holds depends on the height of the scattering layer against the
  radius: to solar zenith angles of about 80° on Mars, and about 65° on Titan, whose haze has a scale height of about
  80 km, 3% of its radius"
- **Evidence.** vincendon2010spherical, Sect. 1: "The radiative transfer codes widely used in surface–atmosphere
  separation problems assume a plane-parallel geometry ... This approach is relevant when the solar zenith angle is
  small enough to neglect the curvature of the planet (typically less than 80° for Mars and 65° for Titan, which has a
  larger relative scale height)." The limits are typical values stated in the introduction for codes that separate
  surface and aerosol in remote sensing; the 80 ± 10 km haze scale height is the paper's own inference from VIMS data
  (abstract), and Titan's radius of 2575 km makes it 3.1%. The conclusion's wording, "the plane-parallel codes that
  separate the surface from the haze" (`conclusions.tex:36–37`), matches the source.
- **Correction.** "How close to the horizon a flat treatment holds depends on the height of the scattering layer
  against the radius: the plane-parallel codes that separate surface and aerosol in remote sensing hold typically to
  about 80° from the zenith on Mars, and to about 65° on Titan, whose haze has a scale height of about 80 km, 3% of its
  radius"

### 14. MINOR: the introduction drops the evidence state of the defects' biases

- **Location.** `paper/sections/introduction.tex:73–75`.
- **Text.** "three of which produce little or no error at Earth's values and bias ExoPlaSim's runs that meet their
  conditions, slowly rotating and tidally locked planets among them"
- **Evidence.** Away from the test world the biases follow from the code's arithmetic (`conclusions.tex:79–81`; H23;
  W06); the abstract keeps "by the code's own arithmetic" (`abstract.tex:10`).
- **Correction.** "... and, by the code's own arithmetic, bias ExoPlaSim's runs that meet their conditions, ..."

### 15. MINOR: "Four Earth-built codes"

- **Location.** `paper/sections/abstract.tex:6`.
- **Evidence.** ExoPlaSim is "PlaSim ... extended for other worlds" (`introduction.tex:55–56`; paradise2022exoplasim);
  CM1, SWAN and SWASH were built for Earth.
- **Correction.** "Four codes built on Earth models, ExoPlaSim~3.4.2, ..."

### 16. MINOR (record): register entry H04 misquotes SWAN's comment

- **Location.** `paper/claims.json`, H04 (also `notes/defect_log.md` B24 and Terluna `climate/waves/audit.md:49–50`).
- **Evidence.** `swancom3.ftn:1722` in the pinned archive: "Source for the 1 Hz application/bending point: mostly
  arbitrary, intended to have zero effect on typical simulations (which stop at 1 Hz)". The paper
  (`assumptions.tex:23`) and `models/swan/README.md:55–56` quote "mostly arbitrary"; H04 and B24 read "largely
  arbitrary".
- **Correction.** H04: "called mostly arbitrary in its comments"; B24 likewise.

### 17. MINOR (record): the manifest lacks locators for three attributions

- **Location.** `paper/sources/manifest.json`: braam2022lightning and sergeev2025lightning (`"locators": []`);
  way2018climates (locators for claim L12 alone).
- **Evidence.** The paper attributes specific content to each (`results.tex:152–156`; `conclusions.tex:50–52, 56–58,
  81–83`; `next.tex:37–39`). Locators found in this review: Braam et al., abstract ("We simulate the atmosphere of
  Proxima Centauri b ..."), Sect. 2.4 Eq. (1), Sect. 4.3 ("tuned to match observed LFRs on Earth"); Sergeev et al.,
  Table 1, Sect. 2.2.1 (graupel flux at −15 °C, total ice water path, the thunderstorms over the United States),
  Sect. 2.2.2 (Price and Rind), Sect. 2.3 (the air and the six pressures), Sect. 4.2 (the route quoted in finding 9);
  Way et al., abstract (zero obliquity and eccentricity; N₂ air with 400 ppmv CO₂ and 1 ppmv CH₄), Sect. 2 ("O3 is set
  to zero"), Table 2 (X016 and X064 at S0X = 1.0, 1360.67 W m⁻²).
- **Correction.** Add these locators.

## 3. Checked and sound

**Conclusions.**
- l. 3–6: the repair classes by form agree with Table `tab:inventory`, under the sentence's "largely".
- l. 6–11: the three defects and their conditions (H23, W06, W02). Recomputed: TRAPPIST-1e's synchronous model day
  6.2030 d gives 0.125 ln 6.203 = 0.228 (`regime_calc.json`); ExoPlaSim's synchronous mode sets only `NFIXED` and
  `FIXEDLON` (`__init__.py:2628–2630`), N = max(int(360/P/12 + 0.5), 1)·12 (`:2616–2619`), model day P·N/(N−1)
  (`plasim.f90:1296–1300`), `zrfac = solar_day*1000` and the 0.8 cap (`rainmod.f90:1869–1893`); any rotation slower
  than 20 days gives N = 12 and a skip of 32.7°.
- l. 13–18: Terluna `climate/gcm/README.md:187–193` ("Each row of latitude still gets its right mean") supports every
  zonal mean kept; the orbit default's global annual mean changes by the factor (1 − e²)^−½, about 1×10⁻⁵ between
  e = 0.0175 and 0.016715; 17% over and 8.3% short (A1); summer rain to 60° and land under 0.5 mm per day 9 → 36% in
  the two-year test (A2; README:662–668).
- l. 18–20: recomputed from the drive: clouds' effect in sunlight −15.70 → −13.32 W m⁻², surface 294.31 → 295.20 K,
  top-of-air net +1.86 W m⁻² (G17); the albedo drop of 0.008 matches the cloud term to within 0.03 W m⁻².
- l. 21–25: Yang et al.: cover 94.8/81.7% (CAM3), 90.4/97.4% (ExoCAM), 26.9/41.1% (SAM); cover parameterized "based
  on relative humidity, atmospheric stratification, and large-scale updrafts"; SAM's cover by the 0.01 g kg⁻¹ threshold
  (SI Text 3); SSTs fixed from SAM's own 40-km run (Methods); albedo gaps 1.6–11.0 points (SI Table 3).
- l. 27–32: 315.51 → 295.51 K with the uncalibrated run still warming; +11.50 K over years 10–19 with a correction fitted
  at 295 K; settled cloud-setting effects of about +2.2 and −5.9 K; settled general repairs of about 2.5 and 1.6 K
  (`repairs.json`; G01, G05, G14).
- l. 33–38: thin shell and flat slab at constant gravity (`assumptions.tex:53–55`); Titan's haze 80 ± 10 km and the
  65° limit (Vincendon and Langevin, abstract and Sect. 1); 80/2575 = 0.031 against the test world's 0.030; Titan's
  radiation outside the adapted models (W05).
- l. 42–44: the cloud fit still to be made and the Earth-fitted microphysics of the runs (`next.tex:19–26`;
  `results.tex:124–125`).
- l. 46–48: laboratory charging laws; the inversion in two windows of an earlier run before the ventilation repair,
  leakage off (G11; Terluna README:2068–2127, 2242–2244).
- l. 50–56: the flash-rate laws as described (finding 12's evidence); cloud tops 55–80 km in six Morrison runs (G09;
  README:1454–1456); 0.022 against 2.72 flashes km⁻² yr⁻¹, ratio 0.0081 (G10); the grid caveat (G10).
- l. 56–60: discharge thresholds set for Earth's storms (Table `tab:inventory`, 50 MV and 10 kV m⁻¹); the comparison
  stated as one between models.
- l. 62–68: SWAN's largest differences 0.303% patched and 5.44% stock (first_experiments.md:33–37; SWAN README:81–84),
  hence "up to"; the empirical coefficients carry Earth's air–water density ratio (SWAN README:89–93); the CM1 pair
  failed to convect (V06).
- l. 68–72: capillary-length ratio 2.457 (`regime_calc.json`); Loftus and Wordsworth, App. C1, "within about 20%",
  under a condition raindrops in air meet (drop viscosity far above the fall medium's); the bounding inference
  follows from collision-set sizes on Earth.
- l. 74–83: dimming scale 0.970 and the easing from 5.0 to 3.0% (G04, S07); the three repairs carry no lunar
  coefficient; Way et al.'s runs at S0X = 1.0 with zero obliquity and eccentricity, ozone set to zero, and sidereal
  periods including 16 and 64 days. At those periods all three defects act: skips of 15.7° and 32.7°, model days of
  16.70 and 69.82 d, cover biases of +0.35 and +0.53, and Earth's 23.7° tilt replacing zero.

**Abstract.** Deitrick et al.'s "Most studies of exoplanet atmospheres using GCMs have adapted codes developed for
Earth or solar system planets" supports "Many" (l. 2–4); S15 for the shield (l. 4–6); H23 and W06 (l. 8–12); "each
holding near the columns it was fitted on" agrees with V07 (l. 12–15); V04 (l. 15–17); G01, G14 and G05 (l. 17–21).

**Results.** l. 44–48 and the Sun-and-tilt row (l. 27): +0.586 K, rain 2.913 → 2.239 mm per day, land 9 → 42% and
36% (G02; `repairs.json`; drive means); `A28_dim5_moon` runs the synodic clock, `fixed_orbit`, `whole_lunar_days`,
Rayleigh 2.215 and water 1.356 at 1,173.49 W m⁻², 294.90 K over years 20–29; SWAN forced from it (Terluna
`climate/waves/README.md:10`); the rings forced from it (G09). l. 90–96: Yang et al.'s numbers, definitions, fixed SSTs
and "broadly similar" (Results, p. 4).

**Reach.** l. 38–42 and the Seas row (l. 114): the knee at g/g_E Hz (SWAN README:50–51); ST6's drag, exact XNL,
JONSWAP bottom friction (0.038 m² s⁻³) and SWASH's hard-coded rotation carry Earth's constants (`notes/waves.md`,
"Constants that are inactive"); tested at a sixth of Earth's gravity on the similarity tests' code paths
(`verification.tex:48–50`). SWASH was also tested at four times lunar gravity, so the sentence states less than the
record allows.

**Next steps.** l. 36–44: as for conclusions l. 81–83; "configurations" covers Way et al.'s topography, ocean and air.
l. 79–85 apart from finding 2: 4–8 m s⁻¹, 0.02–0.2 g m⁻³ and −5 to −16 °C (N01; README:2142–2170); ground strikes
between none and a fifth, a median 149 C (G10; `repairs.tex:160–165`).

**Assumptions.** l. 21–27: "mostly arbitrary" at `swancom3.ftn:1722`; "up to 5.44%" as a largest difference; the
departure above the lower of 1 Hz and g/g_E Hz follows from the scaling (frequencies scale by g/g_E, the stock knee
stays at 1 Hz).

## 4. Counts

| Severity | Count | Findings |
|---|---|---|
| BLOCKING | 3 | 1, 2, 3 |
| MAJOR | 2 | 4, 5 |
| MINOR | 12 | 6–17 (16 and 17 concern the record) |
| Total | 17 | |
