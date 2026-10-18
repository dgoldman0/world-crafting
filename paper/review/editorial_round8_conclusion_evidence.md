# Editorial round 8: evidence review of the closing section, the abstract and the revised passages

## 1. Record

| | |
|---|---|
| Reviewer | A fresh Claude subagent (Claude Opus 5.5), acting as technical evidence reviewer. It read AGENTS.md, the snapshot and the evidence listed below, and no earlier review. |
| Date | 2026-10-18 |
| Snapshot | Commit 44d67d4 ("Revise from the seventh round's records: ..."). Every paper file was read with `git show 44d67d4:<path>`. |
| Scope | `paper/sections/conclusions.tex` and `paper/sections/abstract.tex` whole; the named passages of `results.tex`, `next.tex`, `reach.tex`, `repairs.tex`, `introduction.tex` and `assumptions.tex`; register entries G11, H22 and H04 |
| Method | Reading, `pdftotext -layout` on the archived originals, and small arithmetic in Python on the run records (charge totals, charge layers by output, flash counts by kind, yearly means). No model was run. |

**Files in scope, sha256 at 44d67d4.**

| File | sha256 |
|---|---|
| paper/sections/conclusions.tex | 1708e8f4b973ec9cb7e5c25524f434cdcec3ef1c5e379f8cde06c923807d3bfa (as the brief gives) |
| paper/sections/abstract.tex | b9c375c2a30787f5aa386a1489da713c5951ceecc3d31f555b2cf8785d27c45f (as the brief gives) |
| paper/sections/results.tex | 8b7858fa769f410f4a5a67d61d4d8ec249decbfc0eb397b17d7d4a9a0178ee59 |
| paper/sections/next.tex | 516b8926c1079571364f25904618bfed47d8368dcd6f21d50c4de8368ca66c22 |
| paper/sections/reach.tex | fff8183910168eeb9ee837c8e5766ac0bea7f64b6e95e0d63b8cf821e26f5b63 |
| paper/sections/repairs.tex | c846dbbf4dbaf39ae194d7bb93a26204aaa1b12f4b24e7aa1accdd948b281102 |
| paper/sections/introduction.tex | 9638d854622b6b7121279288a0c70542b1f61d5e25f92fd75bfb376a25556d54 |
| paper/sections/assumptions.tex | 1d0dfd93ba3f0f454cdbd7e8964e64fcb66b49f9275056fa6b5f76a083d4bb0e |
| paper/claims.json | e328443bc55424c69861e1f8766ce0d4a0acb4db43408857bf4770abe66b2129 |

**Evidence relied on, sha256.** Repository files at 44d67d4; Terluna files at 186b294; drive files as they stand on 2026-10-18.

| File | sha256 |
|---|---|
| repo:notes/electrification.md | 2cd81eb8edbd77348133a1e4aaca859b52ca4d0015bc5b26bf12e5d93308f59f |
| repo:notes/exoplasim.md | 707d97ef683d2650db8044cfee18f3a3ac7c82675dc37f4222476a6a4c978bf2 |
| repo:notes/reference_radiation.md | 348501fa28bbe855f6cc99a200d81004fb4163fe91dd0ccccaa13517bbae2730 |
| repo:notes/waves.md | 9f7a775ed1b8a297a4d4a8cf0cd416a8e732b8367cf9f241aaa15dc69cb28102 |
| repo:notes/defect_log.md | c8b83621d548d4f678077b35d761a225fd4f27761b8e4192482e73381f435af8 |
| repo:models/swan/README.md | abb218a0608362f5d2d58cbb72b4d6defcaacb02f06d7123690d862dbc15109d |
| repo:models/swash/README.md | 99927157542500556d4e267bcb59ebfbd7b5572057ead6019284d4ea1af4532c |
| repo:models/exoplasim/README.md | 7af8415bebd7733da42bb34c1f47bb9f5411408a243523cae5524be4b17c7149 |
| repo:paper/data/regime_calc.json | 7a2935a8fbe6086c577097b838825c5415ba99f0adf040af62f5e4bcd370e7d1 |
| repo:python/climate/results/gcm/sun_check_A28_dim5.json | 5b922f8d7afede955e791a78c0b3204988a1515f84bca1e670c1880df9162966 |
| repo:paper/references.bib | c0c9662b362141759bce9a27bb566e7ee6a00479ef773273f1dc109d7888747e |
| repo:paper/sources/manifest.json | f7e84debe34be396642f406f189914a4d0ac9ffd8e3d443a78a9b8f4aeda7048 |
| terluna:climate/crm/README.md | 95776d41c55b3a3a372d3752ff367b66c45f3a98a1609b2cddfd953f49754acd |
| terluna:climate/gcm/README.md | 267413c2aa248c3b7581d796ef83de826fbe6764d6d03c9abd1677fee03150fb |
| terluna:climate/results/crm/elec_charging_laws.json | 8a275a971505530a9951288da7e65806e338e0465874c466ada339d9192339cb |
| terluna:climate/waves/first_experiments.md | 959868b935ca29c3b4f3f929c987036627f81c884064e4f5887e1a29ec60b2a5 |
| terluna:climate/waves/audit.md | ec3eab1ebf6a82f9863128a760e15553ccedf92b4e03d06e9f96481d92087135 |
| terluna:climate/waves/runup.md | 7104b129074b1a8b361177ee1717a07dc35faf06f47b7b68cbeaa28fe66cd357 |
| terluna:research/decisions.md | cfca4e5a14d98925bf2f2584566f5a3a1f76970d9f7494ac3cab6f51030816c2 |
| drive:gcm-runs/A28_dim5/progress.json | 619f3de9adeafa38803e60fc4b311278f9c3bf9f681adcc1f69c05b9b16d8e61 |
| drive:gcm-runs/A28_dim5_sun_test/progress.json | 0d8563dbbe8c815b92c88b29943c7a068e9d4b9fd743738a9da38ba08df7b816 |
| drive:gcm-runs/A28_dim5_moon/progress.json | d287252f152cb52f5b9f07f35f1e51fca87bddab6226fd960a1c35bdfc31be6d |
| drive:crm-runs/box_0e_elec_takahashi/case.json; terluna_flashes.txt | 6a45e92e3a24865c9a7852e3b1a80902387fba8b471a8be995054567907695a7; ee9254a0fe719eb2ad8e5c9a803440ee58bc181bd01fb3d5584c8647fca95c3a |
| drive:crm-runs/box_0e_elec_takahashi_first/case.json; terluna_flashes.txt | 613c645437c8ce4f82a75f1236091d807a3b47359df1d95791b3ff63f986fb62; 0f34b9ad391fd1898c4d40826f5420f7f3ca41066064ebd758695e74be21955f |
| drive:crm-runs/box_0e_elec_ground_rule/case.json; terluna_flashes.txt | 51807a90783ce105e47d699f22bd212e6c2ada61f0fdc8a17f2fec735cb01b1f; 4a146c2835fdf933a2cb3f39cc2b9a64cd110f27cec58ef46296c38fe6eb8735 |
| drive:crm-runs/box_0e_elec_uncapped/case.json; terluna_flashes.txt | becf7da1021092a7b4674df2a6e95cfe28d6b1382df142acba33530beeb7cada; 31a03f93271bc1ad115729f6bc21f9ce964ad9a5df53b150d59ed3f26fe078e7 |
| drive:crm-runs/box_0e_elec_corrected/case.json; terluna_flashes.txt | edbe9d46d382a78e7be827dc621e37e89621b93482ef122ad9a9e8439c6b5c12; 394037c69457ac9ac387c4c0d5dde892a12e44d4e029d733618c822e5a897590 |
| drive:crm-runs/box_0e, box_0e_small, box_0e_small_earth_fall, ring_equator, ring_70_45e, ring_70_135e (case.json) | 8a6ae22d…71e4b9; f9c93b6b…7e5831; ae4da9d2…72e0ba; 66979fb6…08b748; edd90a4a…05af792b; 5f8b8386…b26337 |
| upstream/exoplasim-3.4.2.tar.gz (the archive `models/exoplasim/README.md` pins) | fae502a92f5997ffd18b0bb85b9f0f0677857c62c5d1293f605c9799026f64c2 |

Drive paths are under `/media/projectspace/terluna-research/`.

**Source originals opened** (text layers by `pdftotext -layout`; each sha256 equals the manifest's).

| Original | sha256 | Parts read |
|---|---|---|
| yang2023cloud.pdf (arXiv:2306.12186v1) | 0637811e9ae240d47ab39da7d905421709afb685df2d0050f6f8ffdfa2d8bc41 | Results "Clouds" pp. 3–4; Methods pp. 9–10; Text 3 p. 28 |
| yang2023cloud_si.pdf (publisher SI) | 1cc0a5828d0dc0301b1b2aa712c48f58d8c312a6470e6c1d11df47a806ac5554 | Supplementary Table 3 (printed p. 13); Text 5 |
| braam2022lightning.pdf (arXiv:2209.12502v1) | 26486cfc19cb2185ca8f98a22bcbadf40a526afed1f8b3d460154915b58cf8c7 | Sect. 2.4 p. 4; Sect. 4.3 p. 14 |
| sergeev2025lightning.pdf (arXiv:2504.19883v2) | b2c3352f4ad065bd894341eb76741ff541b1bf4c4824612ae7e6404bd373c6df | Abstract; Sect. 2.2 pp. 3–4; Table 2 p. 4; Sect. 3.1 p. 4; Sect. 4.2 p. 9; Sect. 5 |
| vincendon2010spherical.pdf (arXiv:1103.3215v1) | afcdf418a60ce367c8b16c12d68c1bac36ea2fd8e0013498ea3553c0cbd8a7e9 | Abstract; Sect. 1 pp. 1–2; Sect. 3.2 p. 11 |
| way2018climates.pdf (arXiv:1808.06480v2) | 476e3e967e5d7eeafea1f386fc801851106365653bd3d9132c5821edb7164820 | Abstract; Sect. 2 pp. 2–3; Tables 2 and 3 pp. 5–6 |
| loftus2021physics.pdf (JGR Planets, author copy) | d080f1289e115952977c4b09fa0f9e1b8d93f305315804c84a7878ed0a805d2c | Sect. 3.4 p. 9; Sect. 4.3 pp. 14–15; Appendix C1 p. 22 |
| loftus2021physics_arxiv.pdf | 18fbf925ba0d68443cf445281ce6727b1a8ba0a1270e9c30e81742b5d53491af | Text extracted; the JGR copy served for every locator |
| mansell2026wrfelec-README.electricity.txt | d44c1594248a9f3b7492fa6ad581c821044a5a0d04addce5fac0d57aed516710 | `nssl_isaund` options, lines 119–154 |

**Read in full or in the parts cited.** The eight section files in scope at 44d67d4 whole (the scoped passages checked line by line, the rest read for the body's statements); `paper/claims.json` whole (108 entries); `notes/electrification.md`, `notes/exoplasim.md` lines 1–270, `notes/reference_radiation.md` lines 1–290, `notes/waves.md` lines 14–70 and 255–280, `notes/defect_log.md` lines 1–100, 313–352 and 602–616, `models/swan/README.md` lines 1–150, `models/swash/README.md` (gravity and controls); Terluna's `climate/crm/README.md` lines 1440–1462, 1486–1505, 1596–1680, 2030–2260 and 2340–2440, `climate/gcm/README.md` lines 620–690 and 1143–1163, `climate/waves/first_experiments.md` 25–45, `audit.md` 40–85, `runup.md` 145–160, `research/decisions.md` 364–374; ExoPlaSim 3.4.2 `exoplasim/__init__.py` 2608–2632, `plasim/src/plasim.f90` 1290–1302 and `plasim/src/rainmod.f90` 1886–1892, extracted from the pinned archive.

**Left unread.** Nothing under `paper/review/` was opened; its file names were listed once, to confirm this record's name was free. Nothing under `paper/notes/` was opened. Scratch directories of other sessions under `/tmp/claude-1000/` were left unread; this review's own copies are in `/tmp/claude-1000/r8evid_work/`.

**Sources outside the archive.** The manifest marks saunders1998laboratory and takahashi1978riming BLOCKED, read at abstract level, and christian2003global BLOCKED and unread. Statements on the two charging laws were checked against WRF-ELEC's archived README and the run records. Earth's 44 flashes a second was checked against Sergeev et al. (2025, p. 4), who give "the global average LFR of 44 ± 5 s−1 observed on Earth (Christian et al. 2003)".

## 2. Findings

Locations are `file:line` at 44d67d4. Severity follows the brief: BLOCKING for a factual error, a wrong evidence state or an implied reach or test beyond the evidence; MAJOR for a dropped condition or overstated scope; MINOR for precision.

### 1. MAJOR: the closing sentence ties the charging laws to the cloud evidence and asks for drop-law tests the body routes elsewhere

- **Location.** `conclusions.tex:86–90`.
- **Text.** "The radiation and cloud fits, which moved the test world's climate furthest, would be refitted or replaced on another world from evidence beyond the GCM: the gas and scattering fits from line-by-line spectroscopy checked against an independent code, and the cloud from cloud-resolving runs of that world, a second model whose own drop and charging laws would in turn need laboratory tests at the conditions of its storms."
- **Evidence.**
  - The charge in the graft is a passive tracer: WRF-ELEC's driver "keeps the charges in CM1's passive tracers (C/kg), which CM1 advects and mixes like any tracer" (terluna `climate/crm/README.md:1494–1497`; `notes/electrification.md:15–18`). The two laws changed the storms' arrangement of charge while flashes and separated charge stayed alike, "So the charging law sets the lunar storms' polarity more than their rate" (README:2097–2106, 2140). The record names no path by which the charging law changes cloud. What moved the box's cloud was the microphysics scheme: NSSL against Morrison, night fog at the ground 29 against 56% (README:2409–2418; `results.tex:165–168`). The cloud fit would therefore draw on the CRM's microphysics, and its charging laws enter the lightning alone.
  - For the drop laws, "the conditions of its storms" include the world's gravity. The route the conclusion gives two paragraphs earlier is the capillary-length scaling, the experiments on other media that Loftus and Wordsworth cite (Appendix C1, p. 22), and runs with Morrison's limits scaled (`conclusions.tex:70–75`; `next.tex:70–74`). The record places the charging measurement within reach of Earth's laboratories ("conditions Earth's laboratories can reach", `notes/electrification.md:130–132`; README:2167–2170); it names no laboratory test of drop sizes at another gravity.
  - The sentence's "on another world" carries none of the bounds the same paragraph set on the spectroscopic scheme (composition, starlight, pressures and temperatures, `conclusions.tex:35–38`).
- **Correction.** Keep the landing on evidence beyond the GCM and name the laws the cloud depends on, for example: "... and the cloud from cloud-resolving runs of that world, a second model whose own Earth-fitted drop and ice laws would in turn need testing at that world's gravity, by the capillary-length scaling and by experiments on other media of the kind Loftus and Wordsworth cite." If the closing sentence should also carry the lightning, give the charging laws their own clause: "...; its charging laws, which set its storms' charge and leave their cloud unchanged, would need laboratory measurements at its storms' impact speeds and cloud water." Bound "another world" once, for example "another world of nitrogen–oxygen air".

### 2. MAJOR: a measurement at hail's impact speeds decides the law for hail; graupel carried most of the charge under Takahashi's law

- **Location.** `conclusions.tex:51–53`; `next.tex:83–85`; register N01 (`claims.json:974`), cited there.
- **Text.** "a measurement of that sign at hail's impact speeds of 4--8 m s−1, in 0.02--0.2 g m−3 of cloud water at −5 to −16 °C, would decide which arrangement the model's lunar storms take" (conclusions); "the sign of that charge would decide which arrangement the model's lunar storms take" (next).
- **Evidence.**
  - Under Takahashi's law hail did 37% (days 10.5–12) and 43% (days 40.5–42) of the non-inductive charging (README:2088, 2091). From `elec_charging_laws.json` (`charge.by_collisions`), graupel separated 15.5 of 24.7 kC and 63.3 of 110.5 kC, 57–63% in the two windows.
  - Graupel strikes ice and snow at 0.95–3.6 m s−1 (README:2150–2151), outside the 4–8 m s−1 of the proposed measurement. Under Saunders and Peck's law the same graupel rimes below the 0.1 g m−2 s−1 below which the law separates no charge (README:2069–2072, 2101–2103), while under Takahashi's law it separates four to six times more (README:2104–2106). The two laws therefore differ for graupel in magnitude as well as sign.
  - The record frames the measurement as one "that would decide between the laws" (README:2167–2170). It also cites slow-impact laboratory results at graupel's speeds pointing Takahashi's way (Ávila et al. 2013 at 1.8 m s−1; Pradeep Kumar et al. 2024 at 1.2 m s−1; README:2120–2126). The paper omits them, and neither is in `references.bib`.
  - If the hail measurement gave Saunders and Peck's sign while graupel charged as those slow-impact studies found, the storms would follow a law the windows never ran, and their arrangement would remain to be computed.
  - N01's "hail does 82-88% of the charging" holds under Saunders and Peck's law only (README:2101–2102).
- **Correction.** Bound the decision to what the measurement covers, for example: "a measurement of that sign at hail's impact speeds of 4–8 m s−1, ..., would decide between the two laws for hail, which carries most of the charge under Saunders and Peck's law; under Takahashi's law graupel, striking at 1–4 m s−1, separated most of it, so the model's arrangement follows once graupel's sign at its own speeds is set as well." In N01, add "under Saunders and Peck's law" after "82-88% of the charging" and give Takahashi's 37–43%.

### 3. MAJOR: the largest sensitivity is credited to the correction alone

- **Location.** `next.tex:9–10`.
- **Text.** "The largest single sensitivity comes from a correction fitted at 295 K and used near 307 K with twice the water vapour."
- **Evidence.** The 11.5 K came from "a calibration and a general repair switched on together" (`results.tex:82–86`), "a joint effect in which the ice optics' share is unmeasured" (`reach.tex:5–6`; G05; `notes/exoplasim.md:229–237`). "Single" and "comes from a correction" drop the ice optics. By the paper's own definition the sensitivities include the changes "as Earth values were removed one repair at a time" (`results.tex:3–4`). Under that definition the first calibration's "at least 20 K" (`results.tex:36–39`; G14, state "sensitivity") is the larger, and it too joined two changes.
- **Correction.** "The largest of the sensitivity tests, 11.5 K, came from the longwave correction switched on with the ice optics, a joint effect in which the ice optics' share is unmeasured; the correction was fitted at 295 K and is used near 307 K with twice the water vapour."

### 4. MINOR: "within the spread of the Saunders and Peck runs" holds as a range in one window

- **Location.** `results.tex:161–162`; G11 (`claims.json:899`).
- **Text.** "the storms under Takahashi's charging law separate as much charge as under Saunders and Peck's, within the spread of the Saunders and Peck runs of the same days".
- **Evidence.** From README:2083–2091 and `elec_charging_laws.json` (non-inductive plus inductive):

  | Window | Takahashi | Saunders and Peck runs |
  |---|---|---|
  | Days 10.5–12 | 29.9 kC | 16.0, 20.8 and 25.7 kC |
  | Days 40.5–42 | 140.0 kC | 138.0 and 144.5 kC |

  Read as a range, the first window's 29.9 kC lies 16% above the largest Saunders and Peck run. Read as a difference, both windows agree: Takahashi's run differs from its paired run (25.7 and 138.0 kC) by 4.2 and 2.0 kC, less than the Saunders and Peck runs' own range (9.7 and 6.5 kC). The record's wording is "within the spread of the realizations" (README:2097–2098).
- **Correction.** "... separate about as much charge as under Saunders and Peck's, 29.9 against 16.0–25.7 kC in the first window and 140.0 against 138.0–144.5 kC in the second, differing from the paired run by less than the Saunders and Peck runs differ among themselves". Give G11 the same numbers.

### 5. MINOR: the first window held no ground strikes under either law

- **Location.** `next.tex:85–87`; G11 (`claims.json:899`).
- **Text.** "The windows leave the sign of the ground strikes under Takahashi's law undecided, since their strikes under both laws, all negative, carried charge left over from a run without leakage." G11: "the windows' ground strikes, all negative under both laws".
- **Evidence.** Days 10.5–12 ran under the 5-km rule (`ground_m` 5000 in both `case.json` files), under which "no lunar flash could strike the ground" (README:1628–1635; defect log C13). Their flash logs hold 14 and 123 flashes, every one of kind 1, in cloud; the second log runs on past the window to day 13.5, and the window's own count is 13 (README:2086). Days 40.5–42 held 21 negative strikes under Saunders and Peck's law and 10 under Takahashi's, none positive (flash logs; README:2090–2091, 2133–2138). The leftover-charge reading is the record's (README:2242–2244).
- **Correction.** "The second window's strikes, 21 under Saunders and Peck's law and 10 under Takahashi's, all negative, carried charge left over from a run without leakage, and the first window ran under a rule that let no lunar channel reach the ground; the windows therefore leave the sign ... undecided." Give G11 the same counts, and cite README:2242–2244.

### 6. MINOR: the normal arrangement under Saunders and Peck's law is clear in the second window and partial in the first

- **Location.** `next.tex:82–83` ("and the normal arrangement under Saunders and Peck's"); `conclusions.tex:50–51` ("held their charge in opposite arrangements under the two").
- **Evidence.** The record documents the normal arrangement for "18 of the second window's 23 outputs" (README:2117–2120). In the first window, the outputs holding over 300 C of negative charge are those the record's rule counts (README:2093–2095). Of these, the paired Saunders and Peck run (`box_0e_elec_uncapped`) shows an upper positive layer above the main negative in 3 of 5 (hours 12, 24 and 27; none at hours 9 and 21), and the capped run in 1 of 2 (`elec_charging_laws.json`, `snapshots`). Under Takahashi's law none of the first window's 8 such outputs holds an upper positive layer, and the main negative sits at 48–64 km (−23 to −44 °C), against 34–44 km (−7 to −17 °C) in the paired run. The contrast therefore holds in both windows, sharpest in the second.
- **Correction.** Either scope the normal arrangement to "in most of the second window's outputs and about half of the first's", or state the contrast the first window supports: "the main negative charge at −7 to −17 °C with positive charge above it in about half the outputs, against −23 to −44 °C with none above under Takahashi's".

### 7. MINOR: the turnover is stated with its conditions dropped, and H22 records a sensitivity as documented

- **Location.** `assumptions.tex:93–95`; `assumptions.tex:207` (the "Charging laws" row); H22 (`claims.json:356`).
- **Text.** "... and WRF-ELEC's laboratory charging laws, between which the lunar storms' arrangement of charge turns over."; the row reads "Charge arrangement turns with the law"; H22 reads "the charging laws (Takahashi's inverts the lunar storms' arrangement of charge)", with state "documented".
- **Evidence.** The turnover is G11's sensitivity result from two windows of an earlier run, made before the ventilation repair and with leakage off (`results.tex:159–165`; README:2072–2080; README:1607–1615 for the repair of 2026-10-06; the windows ran on 2026-10-05, README:2073). The main run, with the repair and leakage, ran under Saunders and Peck's law alone (`box_0e_elec_corrected/case.json`: `isaund` 12, `leakage` 1). The conclusion and next steps carry the conditions (`conclusions.tex:49–51`; `next.tex:81–82`).
- **Correction.** "... between which the lunar storms' arrangement of charge turned over in two windows of an earlier run"; in the row, "Arrangement turned with the law in two windows". In H22, point the parenthesis to G11 with its conditions, or move it to G11 and keep H22's state for the inventory.

### 8. MINOR: one of the reference's two outside checks is an in-house Monte Carlo

- **Location.** `conclusions.tex:38–40`.
- **Text.** "The reference has been compared with independent codes for water-only longwave at constant gravity and for Rayleigh scattering to an optical depth of 1.5".
- **Evidence.** `notes/reference_radiation.md:21–26` calls PyRADS the reference's "only cross-code check". Its table of checks gives the Rayleigh comparison the state "Agreement with an independent method; scratch reference not in the repository" (line 153). What it compared was the two-stream's reflectance of a conservative Rayleigh slab over a black ground against a 400,000-photon Monte Carlo (lines 177–185). V16 says "a Monte Carlo Rayleigh reference".
- **Correction.** "The reference has been compared with an independent code, PyRADS, for water-only longwave at constant gravity, and with a Monte Carlo kept outside the repository for its two-stream's Rayleigh reflection to an optical depth of 1.5, ..."

### 9. MINOR: the count of five defects is the paper's count on the lunar paths

- **Location.** `abstract.tex:10–11`; `introduction.tex:73`.
- **Text.** "the released codes also hold five defects" / "The released codes also hold five defects".
- **Evidence.** The inventory covers "the paths the lunar runs take through the four codes" (`assumptions.tex:3–4`, caption at 147–148). The count follows the paper's definition of a defect (`introduction.tex:70–71`; `assumptions.tex:100`). The defect log's section (a), "upstream defects that the adaptation exposed", lists eight entries, A1–A8 (`notes/defect_log.md:47–54`). The paper classes three of them as Earth values: A3, the calendar (`assumptions.tex:169`); A7, conduction (`:206`); A8, flash reach (`:205`). It adds B11, the cover unit, as a defect (`assumptions.tex:110–115`). The universal "hold" outruns what was examined.
- **Correction.** "on the paths the lunar runs take, the released codes also hold five defects" in both places, or "the adaptation found five defects in the released codes".

### 10. MINOR: Way et al.'s planets carry nitrogen-dominated air with methane, described as "Earth-air"

- **Location.** `conclusions.tex:84–86`; `next.tex:37–39`.
- **Text.** "Runs of released and repaired ExoPlaSim on ozone-free Earth-air planets at Earth's insolation and zero obliquity and eccentricity, rotating once in 16 and 64 days, two of the sidereal periods of the ROCKE-3D runs of Way et al."
- **Evidence.** Way et al. (arXiv v2, abstract p. 1): "The atmosphere is 1 bar N2-dominated with CO2=400 ppmv and CH4=1 ppmv". Sect. 2 (p. 3): "984 millibars, with N2 the major constituent ... CO2 = 400 ppmv and CH4 = 1 ppmv ... O3 is set to zero", with H2O "the only other radiatively active constituent besides CO2 and CH4". Their land and sea follow modern Earth's mask (pp. 2–3). The rotation periods (X016, X064, sidereal), S0X = 1.0 (1,360.67 W m−2) and zero obliquity and eccentricity all match (Table 2, p. 5; p. 2). PlaSim's released shortwave omits oxygen (`assumptions.tex:70–71`), so the oxygen that "Earth-air" names leaves the defect arithmetic and nearly all of the radiation unchanged. The description still sets the configuration that the comparison with ROCKE-3D in `next.tex:42–43` would match.
- **Correction.** "on ozone-free planets of 1 bar nitrogen-dominated air with 400 ppm carbon dioxide, at Earth's insolation and zero obliquity and eccentricity, rotating once in 16 and 64 days, the configuration of two of the ROCKE-3D runs of Way et al."

### 11. MINOR: "Saunders and Peck's law" is WRF-ELEC's default form, whose sign above −15 °C follows Brooks et al.'s critical rate

- **Location.** `conclusions.tex:48–49`; `results.tex:161–162`; `next.tex:82–83`.
- **Evidence.** The runs' `isaund` 12 (`case.json` of `box_0e_elec_ground_rule`, `_uncapped` and `_corrected`) is "Brooks et al. RARcrit for T > -15 using saund6 (otherwise same as isaund=9) (DEFAULT)" (`mansell2026wrfelec-README.electricity.txt:127`). The hail that charges sits at −5 to −16 °C and turns sign at "the critical rate, which above −15 °C is Brooks et al.'s" (README:2159–2163; `notes/electrification.md:11–12`). `references.bib:737` holds brooks1997effect, uncited, BLOCKED in the manifest.
- **Correction.** Name the law once as "Saunders and Peck's law in WRF-ELEC's default form, with Brooks et al.'s critical rime accretion rate above −15 °C", cited to the archived WRF-ELEC README (mansell2026wrfelec) until brooks1997effect clears admission.

### 12. MINOR: "would therefore bound" leaves the bound's direction and premise unstated

- **Location.** `conclusions.tex:74–75`.
- **Text.** "Runs with Morrison's limits scaled by the capillary length would therefore bound how much of the lunar rain's evaporation its small drops cause, a step still to run."
- **Evidence.** The premises in the sentence before are (a) the largest stable drop scales with the capillary length and (b) on present-day Earth collisions set the largest raindrops (Loftus and Wordsworth, Sect. 3.4 p. 9, Appendix C1 p. 22). They leave open how Morrison's Earth limits, which encode collision-limited sizes, scale at lunar gravity, so the direction of any bound stays open. The defect log supplies the premise that would set one: "slower drops collide with less energy" (`notes/defect_log.md:609–611`). Under it, lunar drops would grow at least to the scaled limits, and the run would give a lower bound on the small drops' share. The body describes the same run as one that "would show how much of the evaporation the small drops cause" (`next.tex:73–74`).
- **Correction.** Either "would show, if collision-limited sizes scale as the largest stable drop does, how much ...", matching next steps, or state the direction with its premise: "since slower drops also collide with less energy, would give a lower bound on how much ...".

### 13. MINOR: a reduced correlated-k scheme holds within the reduction's own error as well as the spectroscopy's

- **Location.** `next.tex:14–17`.
- **Text.** "a reduced correlated-k scheme built from the reference model's own spectroscopy ... would replace it, and, once that spectroscopy is checked, would hold on columns within the gases, pressures and temperatures of the check".
- **Evidence.** The in-house correlated-k reduction, built from the same spectroscopy, reproduces the outgoing longwave within 0.4–1.4 W m−2, yet "The largest net-flux difference at any level is ... 4.9–5.0 W/m² (Moon)", unlocated. Against it, the longwave corrections reach "3.6–12 W/m²". The notes add "the k-tables come from the same spectroscopy, so this tests the reduction, not the spectroscopy" (`notes/reference_radiation.md:196–213`). The planned LBLRTM and DISORT comparison tests the spectroscopy (`next.tex:28–32`).
- **Correction.** "... and, once that spectroscopy is checked and the reduction is checked against it layer by layer, would hold on columns within ...".

### 14. MINOR: "for each world" for the cloud calibration

- **Location.** `abstract.tex:25–26`; `conclusions.tex:41–42`.
- **Text.** "Cloud would be a calibration for each world, fitted to cloud-resolving runs" / "Cloud amount would be a calibration for each world, fitted to cloud-resolving runs of that world."
- **Evidence.** The cloud-resolving model represents water cloud through Earth-fitted microphysics (`conclusions.tex:46`; `reach.tex:76–84` on worlds needing new condensation and clouds). The conclusion states that limit beside the sentence; the abstract leaves it out.
- **Correction.** In the abstract, "for each world of water cloud, fitted to cloud-resolving runs whose own microphysics is fitted on Earth"; or scope both sentences to "each such world".

### 15. MINOR: "the only world" leaves out the numerical controls the reach table names

- **Location.** `abstract.tex:18–19`.
- **Text.** "The test world, whose climate is unobserved, is the only world the repaired codes have run on away from Earth's values."
- **Evidence.** The patched SWAN ran the similarity strip at one sixth of standard gravity (`models/swan/README.md:82–84`), and CM1 ran its gravity pair at lunar gravity (V06). The reach table's caption makes the exception explicit: "apart from the Earth benchmarks and numerical controls" (`reach.tex:91–93`).
- **Correction.** "... is the only world the repaired codes have simulated away from Earth's values, numerical controls apart."

## 3. Checked and sound

- **Conclusion, first paragraph.** The forms and their repairs match the inventory, with "largely" covering the bound, settings and avoidances. The convective-cover bias of about 0.23 for a synchronous TRAPPIST-1e checks against `regime_calc.json` (0.228 at a model day of 6.20 d) and ExoPlaSim 3.4.2's own code: `__init__.py` sets only `NFIXED` and `FIXEDLON` for synchronous runs while the rotation period sets `ROTSPD` and N, `plasim.f90` takes `solar_day = sidereal_day*N/(N-1)`, and `rainmod.f90:1890` sets `zrfac = solar_day*1000`. TRAPPIST-1e's 6.1 d is Yang et al.'s (p. 3). The 33° skip for rotations slower than 20 days (N = 12, 1/11 of a turn) checks against `exoplasim_slow_rotators`.
- **Conclusion, second paragraph.** The 17% and 8% match `sun_check_A28_dim5.json` (0.917–1.174 of the row mean). The zonal means sit within 1.8 W m−2 rms of the orbit used. "9 to 36%" matches terluna `climate/gcm/README.md:662–664`. The two-year test's 2.4 W m−2, 0.9 K and continued gain check against the progress files: −13.3 W m−2, 295.20 K and +1.86 W m−2 against years 15–24 of A28_dim5 (−15.70 W m−2, 294.31 K). That test also ran whole model days, which move only the output bookkeeping (`notes/exoplasim.md:255–258`).
- **Conclusion, third paragraph.**
  - The radiation, cloud and repair effects check against the register: at least 20 K, G14; 11.5 K over years 10–19 with a correction fitted at 295 K, G05 and G13; about 6 K settled, G05; 1.6–2.5 K settled, G01.
  - Titan's haze scale height of 80 ± 10 km on a 2,575 km radius, 3.1%, is Vincendon and Langevin's (abstract; Sect. 3.2 p. 11); the test world's ratio is 52/1,737 = 3.0%. Their "typically less than 80° for Mars and 65° for Titan" stands in their Sect. 1, for the plane-parallel codes used in surface–atmosphere separation.
  - The reference's checks (V16) and the planned comparison (`next.tex:28–34`) are stated in their evidence states.
  - Yang et al.: the cover figures are on p. 3, the cover's basis on relative humidity, stratification and updrafts on p. 4, the fixed SSTs from the 40-km run in the Methods (p. 10), the condensate threshold in Text 3 (p. 28) and the albedos in Supplementary Table 3 (18.1/29.1/22.1 and 37.4/47.0/39.0%, so 1.6 to 11.0 points). "Broadly similar" is on p. 4.
- **Conclusion, fourth paragraph.**
  - The windows' set-up checks against `case.json`: restarts of `box_0e_elec` at days 10.5 and 40.5, `leakage` 0, `isaund` 1 and 12, run before the ventilation repair. The impact speeds, cloud water and temperatures match README:2142–2170.
  - Braam et al. set the oceanic cloud-top law with coefficients "tuned to match observed" Earth flash rates (p. 4, Eq. 1; p. 14). Sergeev et al. used McCaul et al.'s graupel flux at −15 °C and total ice water path in storm-resolving runs and Price and Rind's cloud-top law in coarse ones, "originally derived from observations of severe thunderstorms over the United States" (p. 3), with N2 air, 400 ppm CO2, no O2 or O3, at 0.25–10 bar. Their Sect. 4.2 (p. 9) proposes explicit charging in a cloud-resolving model "In the absence of in-situ observations".
  - The 55–80 km cloud tops come from six Morrison runs (README:1454–1455), with the forcing states confirmed in `case.json`.
  - The main run logs 530 flashes, 106 negative to ground and none positive, median 148.9 C. Its 0.022 km−2 yr−1 is 0.008 of 2.72 (`flash_density`).
- **Conclusion, fifth paragraph.** SWAN's 0.303% and 5.44% come from the test at one sixth of standard gravity (`models/swan/README.md:82–84`), and the CM1 pair failed to convect (V06). The capillary ratio is 2.457. Loftus and Wordsworth give "within about 20%" for drop media much more viscous than the fall medium, as water is in air (p. 22), and collisions on present-day Earth (p. 9).
- **Conclusion, sixth paragraph.** The 295 K design temperature and the dimming eased from 5.0 to 3.0% check against terluna `climate/gcm/README.md:1143–1163` and G04. Way et al.'s sidereal periods, insolation, zero tilt and eccentricity and zero ozone match the cited work (see finding 10 for the air). The defects' biases elsewhere are rightly given as code arithmetic.
- **Abstract.** Every number matches its register entry (G01, G14, G05, V04, H23, W06). The radiation scheme's bounds and the planned single-column comparison stand in the right states, and no sentence claims a run on another world.
- **Results.**
  - The Sun-and-tilt row checks against `A28_dim5_moon`'s configuration: synodic clock, fixed orbit, whole model days, `rayleigh_scale` 2.215 and `sw_water_absorption` 1.356 at 1,173.49 W m−2, with years 20–29 at 294.90 K and 2.24 mm a day. Rings forced from it are confirmed in `case.json`; SWAN and the cloud tests in G12 and G16.
  - The four changes, +0.59 K, 2.91 to 2.24 mm and 9 to 42% check against terluna `climate/gcm/README.md:639–651`.
  - The Yang et al. and flash-rate sentences match the originals as above.
- **Reach.** The sentence beginning "With SWAN's knee patched" matches `notes/waves.md:30–68` and 265–276 and `models/swash/README.md:99–116`. SWASH's similarity controls ran at lunar gravity and four times it, so "tested at a sixth of Earth's gravity" holds for both models.
- **Repairs.** The Mars and Titan sentence matches Vincendon and Langevin's Sect. 1 and their 80 km on 2,575 km.
- **Introduction.** The four forms match the inventory's Form column.
- **Register.** H04 matches its sources: the upstream comment "mostly arbitrary" (`models/swan/README.md:55–57`) and the largest Hs difference of 5.44%, which the text gives as "up to". G11's comparison of NSSL with Morrison matches README:2409–2418. The Takahashi citation is defensible: WRF-ELEC's README files `isaund` 1 under "Takahashi (1978, 1984) charge separation" (lines 129–130).

## 4. Counts

| Severity | Count | Findings |
|---|---|---|
| BLOCKING | 0 | |
| MAJOR | 3 | 1, 2, 3 |
| MINOR | 12 | 4–15 |
