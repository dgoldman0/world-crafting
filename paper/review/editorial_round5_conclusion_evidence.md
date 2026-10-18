# Editorial round 5: evidence review of the closing section, the abstract and the revised passages

## 1. Record

- **Reviewer.** A fresh Claude subagent (Claude Opus 5.5). It saw no earlier review, and it read only the
  text, the rules and the evidence listed below.
- **Date.** 2026-10-17.
- **Snapshot.** Commit `11026a8` (`11026a8860933914ab13c2b10dd9494d97555938`). Every repository file was
  read with `git show 11026a8:<path>`. The reviewer changed nothing except this record.
- **Left unopened.** Everything under `paper/review/` except this file, and everything under `paper/notes/`.
- **Machine use.** Light reads only. Text extraction ran under `nice`.

### Files in scope (sha256 at 11026a8)

| File | sha256 |
|---|---|
| `paper/sections/conclusions.tex` (whole) | `4d12601bc67f62add60c6e605d745c4e8d3c6db582ecfde8620112089113aee0` (matches the brief) |
| `paper/sections/abstract.tex` (whole) | `8bbd11720dd47a835b8f7c512b601d554cf5c2aa81ba3c68cbc536dda811a075` (matches the brief) |
| `paper/sections/results.tex` (passages at lines 44–46, 81–86, 90–97, 151–154) | `115b663dc4579b31fb47ec5d5b5f4fc50231f00e262e597bc7481de1908d86c7` |
| `paper/sections/reach.tex` (lines 38–41, 47–60, 90–93, 114) | `af628ab20664ca3b40972ec320c7f75a04373f5fa3c4e4b22a3ab6e4af8e3c7d` |
| `paper/sections/next.tex` (lines 35–43) | `650228e9ab643a80b519d9e14c42f86bedb76d00a9ad79b3eaa88ab326d6c5d0` |
| `paper/sections/assumptions.tex` (lines 21–26) | `c57415f24ad79e207d0e87c773db69f7f1ace96640e4edd0a0738d648d534682` |

### Evidence relied on (sha256)

| File | sha256 |
|---|---|
| `AGENTS.md` | `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32` |
| `paper/main.tex` | `7ef8255c7fa8d14e9d0d61406d1f919be6dff5251b47fb3598aba9c913a8495c` |
| `paper/sections/introduction.tex` | `b8325d641b56d6da32cffbcaa143e26461495322235c2de3b0709402f1ef5b72` |
| `paper/sections/worlds.tex` | `453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112` |
| `paper/sections/repairs.tex` | `bb1d22c01616fdaf454280acded56316b7995af2a8fc3bb5a255af52c92e793c` |
| `paper/sections/verification.tex` | `4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00` |
| `paper/sections/appendix.tex` | `ebab8ca204f81ed41d9185d456353a43a9f59e5307290695277b4614b5bd6635` |
| `paper/sections/availability.tex` | `496434ae301b500a3f7dcec2750af08b8a4d1789c437844ab1318e3ff35f762d` |
| `paper/claims.json` | `8bb7e9e6cf2010e75be6f6890357c0238798bc27ab9c2b7412cb61ab8507e8e1` |
| `paper/references.bib` | `c0c9662b362141759bce9a27bb566e7ee6a00479ef773273f1dc109d7888747e` |
| `paper/sources/manifest.json` | `334f5973fe6339026237ca7953369c34e5f4a1cce89ef935bccd7ccfa76a66a4` |
| `paper/data/regime_calc.json` | `7a2935a8fbe6086c577097b838825c5415ba99f0adf040af62f5e4bcd370e7d1` |
| `models/swan/README.md` | `3699e5e564fa484d36b1aa6c91434ab8119beeb3a50de8f72625db97476f8d3f` |
| `notes/waves.md` | `9f7a775ed1b8a297a4d4a8cf0cd416a8e732b8367cf9f241aaa15dc69cb28102` |
| `notes/exoplasim.md` | `707d97ef683d2650db8044cfee18f3a3ac7c82675dc37f4222476a6a4c978bf2` |
| `notes/reference_radiation.md` | `348501fa28bbe855f6cc99a200d81004fb4163fe91dd0ccccaa13517bbae2730` |
| `python/climate/results/gcm/sun_check_A28_dim5.json` | `5b922f8d7afede955e791a78c0b3204988a1515f84bca1e670c1880df9162966` |
| `terluna:climate/gcm/README.md` at 186b294 | `267413c2aa248c3b7581d796ef83de826fbe6764d6d03c9abd1677fee03150fb` |
| `terluna:climate/crm/README.md` at 186b294 | `95776d41c55b3a3a372d3752ff367b66c45f3a98a1609b2cddfd953f49754acd` |
| `drive:gcm-runs/A28_dim5_sun_test/progress.json` | `0d8563dbbe8c815b92c88b29943c7a068e9d4b9fd743738a9da38ba08df7b816` |
| `drive:gcm-runs/A28_dim5/progress.json` | `619f3de9adeafa38803e60fc4b311278f9c3bf9f681adcc1f69c05b9b16d8e61` |
| `drive:gcm-runs/A28_dim5_moon/progress.json` | `d287252f152cb52f5b9f07f35f1e51fca87bddab6226fd960a1c35bdfc31be6d` |
| `drive:exoplasim-twilight/exoplasim/__init__.py` (the deployed wrapper, lines 2608–2635) | `07ea85554ef45172eee24d68c0e8be61b98db86ac276cc6f246ad5c161183903` |

### Source originals opened

Each file's sha256 matched its manifest record before it was read with `pdftotext`.

| Key | File | sha256 | Read |
|---|---|---|---|
| yang2023cloud | `yang2023cloud.pdf` (arXiv v1, with SI) | `0637811e…8bc41` | main text pp. 1–7; SI Text 3 (p. 28); SI Table 3 (p. 39) |
| yang2023cloud (SI) | `yang2023cloud_si.pdf` | `1cc0a582…5ac5554` | Text 3; Table 3 (same values as the arXiv copy) |
| braam2022lightning | `braam2022lightning.pdf` | `26486cfc…cf8c7` | abstract; Sect. 2.4; Sect. 4 (pp. 13–14) |
| sergeev2025lightning | `sergeev2025lightning.pdf` | `b2c3352f…c6df` | abstract; Sects. 1–2.3; Sect. 4.2; Sect. 5 |
| vincendon2010spherical | `vincendon2010spherical.pdf` (arXiv v1) | `afcdf418…a7e9` | abstract; Sect. 1 |
| way2018climates | `way2018climates.pdf` (arXiv v2) | `476e3e96…4820` | abstract; Sect. 2.1; Table 2 with notes; Sect. 3.1 |
| yang2014strong | `yang2014strong.pdf` (arXiv v1) | `3b285234…f5c` | abstract; Sects. 1–3 |
| banfield2015winds | `banfield2015winds.pdf` | `252db567…b5cda325` | abstract; Sect. 3.2.2; Sect. 4.2 |
| deitrick2020thor | `deitrick2020thor.pdf` (arXiv v3) | `52da49f4…d7c` | Sect. 1 |
| loftus2021physics | `loftus2021physics.pdf` | `d080f128…805d2c` | Sect. 3.4 (p. 9); App. C1 (p. 22) |

### What was read

All of the paper's sections at 11026a8, `main.tex`, every entry of `claims.json`, the manifest records and
bibliography entries of the works above, the SWAN README in full, `notes/waves.md` in full, `notes/exoplasim.md`
lines 1–270 and `notes/reference_radiation.md` lines 1–290. Also read: the `regime_calc.json` entries for the
synchronous cover bias, the Sun-clock skip, slow rotators, the capillary length, the scale height, the shell and
the flash density; the Sun-clock check JSON; the Terluna GCM README at lines 222–234, 304–320, 620–690,
866–902 and 1205–1212; the Terluna CRM README at lines 1450–1458, 2097–2122, 2142–2172 and 2500–2530; the yearly
records and configurations of the three drive runs; and the deployed ExoPlaSim wrapper's rotation and
synchronous-mode lines. Arithmetic re-done by the reviewer is named where it is used.

## 2. Findings

### 1. BLOCKING — conclusions.tex:67–69

> "its drop-size limits stay Earth's while the largest raindrop that survives its fall scales with the
> capillary length, 2.46 times longer at a sixth of Earth's gravity, a dependence beyond what a laboratory on
> Earth or a similarity run can test."

**Evidence.** The paper cites Loftus and Wordsworth (2021) for the gravity dependence of raindrops
(worlds.tex:88–90). In App. C1 (p. 22) they write: "numerous chemical engineering experiments have been done on
the maximum-sized drops of different media falling through various other media. Such experiments consistently
agree (within about 20%) with the predictions of Equation 21." Their Eq. 21 sets the largest stable size from
√(σ/(gΔρ)), the capillary length. Laboratories on Earth have therefore tested this scaling, at fixed g, by
changing the liquid and the medium. In Sect. 3.4 (p. 9) they add that on present-day Earth "the practical upper
bound on raindrop size is not set from individual raindrop breakup but rather from hydrometeor collisions".

The body makes no testability claim for the scaling. Assumptions.tex:86–89 states the scaling. Next.tex:72–73
proposes limits scaled with the capillary length as a test still to run. The similarity half of the clause holds:
a similarity run keeps Morrison's limits at their Earth values and tests the code's consistency
(verification.tex:11–13). The laboratory half contradicts the paper's own cited source.

**Proposed correction.** "…2.46 times longer at a sixth of Earth's gravity; experiments on the largest stable
drops of other liquids at Earth's gravity agree with that scaling within about 20% \autocite{loftus2021physics},
and runs with Morrison's limits scaled by it are a step still to run." Another option is to end the sentence at
"…at a sixth of Earth's gravity." and leave the test to Next steps.

### 2. BLOCKING — conclusions.tex:82–84 (the closing sentence's last clause)

> "cloud remains to be calibrated for each such world, against cloud-resolving runs whose laws of drops and
> charge remain Earth fits until laboratories and runs at other gravities test them."

**Evidence.** Verification.tex:11–13 says "a similarity test runs Earth's empirical laws at the scaled gravity
with their Earth coefficients, which it leaves untested there". `notes/waves.md`:19–22 says the similarity state
"does not test those coefficients", and lines 67–68 say the same. A run computes with its laws of drops and
charge, and the paper records no run that tests one of them.

The one run-based test this section describes (conclusions.tex:57–59) is narrower. It sets other studies'
flash-rate laws against resolved charge while holding the laboratory charging laws. Its outcome would be a
conditional model result. The body's route for the charging laws is the laboratory (next.tex:78–83).

As written, the clause also contradicts lines 68–69, which place the drop limit's dependence beyond both
laboratories and similarity runs. The paper's landing thus presents model runs as tests of empirical laws, which
is a wrong evidence state.

**Proposed correction.** "…against cloud-resolving runs whose laws of drops and charge remain Earth fits;
laboratories on Earth can test the charging laws in the conditions of that world's storms, and runs at other
gravities test whether gravity enters the code consistently."

### 3. MAJOR — conclusions.tex:79–82, and 40–42 (the closing sentence's bound)

> "For a new world of nitrogen--oxygen air with water and modest carbon dioxide, whose scale height is at most
> three hundredths of its radius, the test world's ratio, the radiative geometry can be computed from the world's
> own column as it was from the test world's, and, once a scheme is built from the reference's spectroscopy and
> checked against an independent code, the gas absorption as well"

**Evidence.** The bound names the composition and the scale height over the radius. It omits the pressure, or
column mass, which is the ratio that sets the radiation's absorber paths (worlds.tex:4–6).

The body bounds the proposed scheme to "any column whose gases and pressures that spectroscopy covers"
(next.tex:15–16). The reference's correlated-k tables, from which such a scheme would be built, span 0.1 Pa to
3.2×10⁵ Pa, 100–375 K and water fractions 0–0.5, and they "clamp silently at the node edges"
(`notes/reference_radiation.md`:238–239). Its CO2 and O2 are air-broadened only, and the notes say the model "is
not fit for CO2-rich or non-N2/O2 atmospheres without these additions" (:229–237). Table tab:reach lists
"multi-bar surfaces" beyond the adapted models (reach.tex:110).

As written, the sentence extends the gas-absorption step to nitrogen–oxygen worlds at any surface pressure whose
H/R is at most 0.03. Lines 40–42 ("for air of nitrogen and oxygen with water and modest carbon dioxide") have the
same omission.

**Proposed correction.** At 81–82: "…the gas absorption as well, at the pressures and temperatures that
spectroscopy's tables cover, up to 3.2 bar and 375 K;". At 41–42: "…for air of nitrogen and oxygen with water and
modest carbon dioxide at the pressures its tables cover…".

### 4. MAJOR — abstract.tex:20–22 (the last sentence)

> "A radiation scheme built from line-by-line spectroscopy would replace the largest fits with physics computed
> for each world's nitrogen--oxygen air, while cloud would remain a calibration for each world, fitted to
> cloud-resolving runs, a fit still to be made on the test world."

**Evidence.** The sentence's tense is right for a proposal, but its scope exceeds the body's.

- **The check condition is dropped.** The conclusion keeps "once that spectroscopy has been checked against an
  independent code" (conclusions.tex:42, 81–82). The reference's carbon dioxide, oxygen, collision-induced
  absorption and sunlight on the lunar column "have yet to be compared with an independent code"
  (verification.tex:68–69; claim V16).
- **"each world's nitrogen--oxygen air" covers every such world.** The body bounds the scheme to the gases and
  pressures the spectroscopy covers (next.tex:15–16). The reference holds dry air of N2, O2, Ar and CO2 only,
  with air-broadened CO2 and O2 and tables to 3.2 bar and 375 K (`notes/reference_radiation.md`:229–239). The
  conclusion adds "with water and modest carbon dioxide" (conclusions.tex:41–42).
- **"physics computed" goes too far.** The scheme would carry the MT_CKD continuum, whose "foreign continuum
  assumes Earth air as the broadener" (`notes/reference_radiation.md`:233). Part of the scheme stays an
  empirical fit.

**Proposed correction.** "A radiation scheme built from the reference's line-by-line spectroscopy, once that
spectroscopy is checked against an independent code, would replace the largest of these fits for
nitrogen--oxygen air with water and modest carbon dioxide at the pressures and temperatures its tables cover,
while cloud would remain a calibration for each world, fitted to cloud-resolving runs, a fit still to be made on
the test world."

### 5. MAJOR — reach.tex:38–41

> "In the configuration used, SWAN and SWASH are built to run water seas at any gravity as the scaled image of an
> Earth sea, and on that configuration's code paths have been tested at a sixth of Earth's gravity, with Earth's
> empirical laws;"

**Evidence.** The SWAN similarity test ran "Komen growth and whitecapping under a fixed wind, DIA, the
wind-input knee and depth breaking on Cartesian strips started from rest". The same passage says "the lunar
runs' spherical grids, nests and GCM forcing were checked separately or left unchecked" (verification.tex:48–51).
`notes/waves.md`:62–67 says: "Spherical geometry, nesting and stationary iteration were checked separately or not
at all."

The configuration used includes spherical coordinates at the lunar radius, nests, hotstarts and the Wu-equivalent
forcing (`models/swan/README.md`:188–199). "That configuration's code paths" covers all of these, so the sentence
widens the tested scope. The conclusion's wording, "on the code paths those tests ran" (conclusions.tex:64–65),
matches the body.

**Proposed correction.** "…and on the code paths the similarity tests ran have been tested at a sixth of Earth's
gravity, with Earth's empirical laws; …".

### 6. MAJOR — conclusions.tex:46–47 (with 57–59)

> "Some of those Earth-fitted laws can be tested independently of the world modelled, in laboratories on Earth or
> in runs at other gravities."

**Evidence.** "Those Earth-fitted laws" refers back to the cloud-resolving runs' "Earth-fitted microphysics of
their own" (line 44). The paragraph's laboratory test, the charging sign at lines 47–51, fits that referent. Its
run-based test (lines 57–59) falls outside it: that test concerns the flash-rate laws Braam et al. and Sergeev
et al. used, and CM1 has no such law, since it computes flashes from resolved charge (line 56). The test also holds the
laboratory charging laws and CM1's Earth-fitted microphysics fixed (verification.tex:11–13).

The sentence therefore says runs can test the cloud-resolving runs' own laws. Finding 2 carries the same
conflation into the closing sentence.

**Proposed correction.** "Laboratories on Earth can test some of those Earth-fitted laws in another world's
conditions, and runs that resolve charge at other gravities can set the flash-rate laws other studies used
against explicit charging."

### 7. MINOR — conclusions.tex:30–31

> "the longwave correction, switched on with the ice optics, warmed the design case by 11.5~K in its test"

**Evidence.** The 11.5 K is a joint effect "in which the ice optics' share is unmeasured" (reach.tex:5–6;
claim G05; `notes/exoplasim.md`:229). As written, the correction alone does the warming.

**Proposed correction.** "the longwave correction and the ice optics, switched on together, warmed the design
case by 11.5~K in their test".

### 8. MINOR — conclusions.tex:31–33

> "PlaSim's Earth-tuned cloud settings, pushed to the ends of their tests, moved the climate by up to about 6~K"

**Evidence.** The quantity is the global-mean surface temperature. "About 6 K" is the settled estimate. The
lower threshold gave 289.9 K over years 5–14 and was settling near 289.0 K, against 294.9 K (Terluna
`climate/gcm/README.md`:1210; claim G05: −4.98 K over the years averaged, about −5.9 K settled).

**Proposed correction.** "…moved the global-mean surface temperature by up to about 6~K as the runs settled".

### 9. MINOR — conclusions.tex:9–10

> "the convective-cover unit would add about 0.23 to the convective cover of a synchronous run of TRAPPIST-1e"

**Evidence.** The body gives the lunar bias with its cap: "adds 0.125 ln 29.8 = 0.42 to the cover, up to its cap
of 0.8" (assumptions.tex:113–114; `notes/exoplasim.md`:98). Where Slingo's cover nears 0.8, under heavy
substellar rain, the addition is smaller. The value 0.23 itself checks: the reviewer computed N = 60 and a model
day of 6.203 d, giving 0.228 (`regime_calc.json`, `exoplasim_synchronous_cover_bias`).

**Proposed correction.** "…would add about 0.23, up to the cover's cap of 0.8, to the convective cover of a
synchronous run of TRAPPIST-1e".

### 10. MINOR — conclusions.tex:21–26

> "on two tidally locked planets, three models came out broadly alike in global-mean surface temperature and
> albedo by their authors' account, while the quasi-global cloud-permitting runs of \textcite{yang2023cloud}
> covered 27 and 41\% of the sky with cloud and two GCMs … covered 82--97\%"

**Evidence.** Each number and the attribution check against Yang et al. Two conditions are missing.

- **The cover definitions differ.** In SAM a column counts as cloudy when its vertically integrated cloud water
  exceeds 0.02 kg m⁻², while the GCMs give partial cover with overlap (SI Text 3, arXiv p. 28). Results keeps
  that condition ("which counts cloud by a condensate threshold", results.tex:85). The conclusion drops it.
- **"Broadly alike" covers a wide spread.** The attribution is right: their Discussion (p. 7) reads "For time-
  and global-mean, the simulated surface temperature and planetary albedo in the CPM are broadly similar to
  those found in GCM experiments". Their SI Table 3 (p. 39), however, spans 239.7–243.4 K and 252.7–267.6 K in
  surface temperature, and 18.1–29.1% and 37.4–47.0% in albedo.

**Proposed correction.** Keep Results' condensate-threshold clause in the conclusion. Optionally, give the spread
the authors called similar: "within 4 and 15 K, and 11 and 10 points of albedo".

### 11. MINOR — results.tex:81–86

> "two GCMs that diagnose their cover, as PlaSim does, covered far more of the sky than a quasi-global
> cloud-permitting model … against 26.9 and 41.1\% in the cloud-permitting model, which counts cloud by a
> condensate threshold, while the three models' global-mean surface temperatures and albedos came out broadly
> alike."

**Evidence.**

- **(a) Both kinds of model diagnose cover.** Yang et al. call cloud fraction "a diagnostic variable" in SAM as
  well (SI Text 3, p. 28). What sets the GCMs apart is that their "cloud coverages are empirically parameterized
  based on relative humidity, atmospheric stratification, and large-scale updrafts" (main text, p. 4).
- **(b) "Broadly alike" is stated in the paper's own voice.** The conclusion attributes it to the authors. Given
  the 15 K and 11-point spreads in their Table 3, Results should attribute it as well.

**Proposed correction.** "two GCMs that parameterize their cover, as PlaSim does, …" and "…came out broadly
alike by the authors' account."

### 12. MINOR — results.tex:151–154

> "\textcite{braam2022lightning} and \textcite{sergeev2025lightning} estimated lightning on tidally locked planets
> with Earth-like air from laws fitted to Earth's storms"

**Evidence.** Braam et al. simulate Proxima Centauri b with an Earth-like atmosphere and its ozone chemistry
(abstract, p. 1). Sergeev et al. set "N2 as the dominant background gas and 400 ppm of CO2 … Oxygen and ozone are
not included", at 0.25–10 bar on TRAPPIST-1e (Sect. 2.3, p. 4).

**Proposed correction.** "…on tidally locked planets with Earth-like air or, in Sergeev et al.'s runs,
oxygen-free nitrogen air at 0.25--10 bar, from laws fitted to Earth's storms…".

### 13. MINOR — results.tex:44–46

> "a step that joined a general repair and an avoidance with a calibration"

**Evidence.** The step also set whole model days. Both `A28_dim5_moon` and `A28_dim5_sun_test` carry
`whole_lunar_days: 1` in their configurations (drive `progress.json`), and Table tab:repairs classes "Whole
model days" as an avoidance. This second avoidance changes output bookkeeping alone (`notes/exoplasim.md`:255).
The phrase is otherwise exact: the synodic clock is a general repair, the fixed orbit an avoidance, and the
refitted Rayleigh and near-infrared water multipliers (1.8→2.215; 1.356) a calibration.

**Proposed correction.** "a step that joined a general repair and two avoidances, one of them output
bookkeeping, with a calibration". Another option is to keep the phrase and add "whole model days" to the
Sun-and-tilt row of Table tab:states.

### 14. MINOR — assumptions.tex:21–26

> "with that linear input switched on, a sea at any gravity other than Earth's, the ancient seas of Mars among
> them, departs through that constant from the scaled image of an Earth sea wherever its frequency band reaches
> past the scaled knee."

**Evidence.**

- **The condition holds for weaker gravity only.** Stock SWAN multiplies the linear term by f⁻³ above 1 Hz
  (`models/swan/README.md`:40–42), and the scaled image bends at g/g_E Hz. Under weaker gravity the stock code
  departs from the image above g/g_E Hz, as written. Under stronger gravity it damps from 1 Hz, below the scaled
  knee, so such a sea departs wherever its band passes 1 Hz.
- **The Mars clause could be misread.** Banfield et al. describe SWAN's wind input "by the classical approach by
  Miles (1957, 1959, 1960), later improved by Janssen (1989)", with Komen whitecapping, Madsen bottom friction and
  Battjes–Janssen breaking, and they mention no linear term (Sect. 3.2.2, pp. 371–372). The sentence's condition
  covers this, but a reader may take the clause as a statement about their runs.
- **The rest checks.** "Largely arbitrary" paraphrases the source comment "mostly arbitrary"
  (`models/swan/README.md`:55), and 5.44% is the largest stock difference (:84).

**Proposed correction.** "…wherever its frequency band reaches past the lower of the two knees, g/g_E~Hz under
weaker gravity and 1~Hz under stronger". Optionally: "an ancient Martian sea, run with that input, among them".

### 15. MINOR — conclusions.tex:76–79, and next.tex:36–39

> "released and repaired ExoPlaSim on Earth-air planets rotating once in 16 and 64 days, as in two of the
> ROCKE-3D runs of \textcite{way2018climates}, would measure them on worlds that other studies model."

**Evidence.**

- **The conclusion drops two of next.tex's conditions:** "at Earth's insolation and zero obliquity and
  eccentricity" and "with the released radiation". The orbit default shows only where the configured orbit
  differs from Earth's. Way et al. set "Planetary obliquity and eccentricity are zero" (Sect. 2.1, p. 3), so that
  condition carries the third defect's test.
- **"Earth-air" is loose in both places.** Way et al.'s air is 984 hPa of N2 with 400 ppm CO2 and 1 ppm CH4, with
  "O3 … set to zero", on modern Earth's land (p. 3). A run made as in theirs therefore sets ozone to zero.

**Proposed correction.** For the conclusion: "released and repaired ExoPlaSim at Earth's insolation and zero
obliquity and eccentricity, rotating once in 16 and 64 days as in two of the ROCKE-3D runs of
\textcite{way2018climates}, …". In next.tex, "ozone-free" could be added after "Earth-air".

### 16. MINOR — conclusions.tex:79–84

> "…the radiative geometry can be computed from the world's own column as it was from the test world's, …"

**Evidence.** The closing sentence names three parts: the radiative geometry, the gas absorption and the cloud.
For air tall against the radius, Table tab:reach also lists "Thin-shell, constant-gravity dynamics; one clear
column for all; the vertical grid" beyond the adapted models (reach.tex:109). Lines 36–37 name the dynamics; the
single clear column and the vertical grid stay unnamed at the landing.

The capability clause matches the body's design statement (repairs.tex:105–106; reach.tex:9–14). Its evidence
state, that the table has been computed for one clear design column (repairs.tex:87–89), is left implicit.

**Proposed correction.** "…as it was from the test world's single clear design column, within the vertical grid
and thin-shell dynamics that Table~\ref{tab:reach} bounds, …". Another option is a pointer to Table tab:reach at
the end of the sentence.

### 17. MINOR — abstract.tex:12–14, and conclusions.tex:5–7

> abstract: "constants and units of time mostly took general repairs built to hold on other worlds, the radiative
> geometry took a method computed for each world's column, and the radiation's fits took calibrations to an
> in-house line-by-line model."

**Evidence.**

- **(a) A condition is dropped.** "Built to hold on other worlds" omits "within the limits of its laws"
  (introduction.tex:76–78; repairs.tex:13–14).
- **(b) The method computes a table.** The table has so far been computed for one clear design column
  (repairs.tex:87–89), so "computed for each world's column" overstates what has been done.
- **(c) Two of the radiation's fits took other repairs.** The liquid cloud optics took a general repair (ice
  optics), and RRTMG's ice optics took a mitigation (assumptions.tex:178, 190). The conclusion covers this with
  "largely"; in the abstract, "mostly" reaches only the constants and units of time.
- **(d) Both places name the line-by-line model alone.** The longwave correction was fitted to the reference's
  correlated-k emulation (assumptions.tex:73–74; repairs.tex:120–121, 135–139).

**Proposed correction.** "…mostly took general repairs built to hold on other worlds within the limits of their
laws, the radiative geometry took a method that computes a table from each world's own column, and the
radiation's gas and scattering fits took calibrations to an in-house line-by-line model and its correlated-$k$
emulation."

### 18. MINOR — reach.tex:90–93 (caption of Table tab:reach)

> "where the released ExoPlaSim, CM1, SWAN and SWASH err"

**Evidence.** The second column includes WRF-ELEC's 180 kV m⁻¹ cap, its −7 °C ground rule, its 0.75 s sub-step
and its want of clear-air conduction (reach.tex:106, 113).

**Proposed correction.** "where the released ExoPlaSim, CM1 with WRF-ELEC, SWAN and SWASH err".

### 19. MINOR — reach.tex:114 (the Seas row)

> "Similarity at any gravity on the configuration's code paths; air density per build; breaking kept on |
> Earth's drag, growth and breaking laws"

**Evidence.**

- **The third column has finding 5's widening.** The caption makes the column the reach each repair was built
  for, so the design state is stated. What was tested goes unstated: a sixth of Earth's gravity, on the paths the
  tests ran.
- **The fourth column omits Earth constants.** The text (reach.tex:40–41) names the avoided options that keep
  Earth's constants: ST6 drag, exact quadruplets, JONSWAP bottom friction and SWASH's rotation
  (`models/swan/README.md`:211, 268–270; `notes/waves.md`:265–276). The single air density per build also
  belongs there (`models/swan/README.md`:123–125).

**Proposed correction.** Third column: "Similarity at any gravity, tested at a sixth of Earth's on the tested
paths; …". Fourth column: "Earth's drag, growth and breaking laws; ST6, exact quadruplets, bottom friction and
SWASH's rotation at Earth's constants; air density as a field".

## 3. Checked and sound

- **Conclusion numbers against the register.**
  - W06 (+0.23; N = 60, model day 6.203 d, bias 0.228). The wrapper's lines 2615–2630 confirm
    N = max(int(360/P/12 + 0.5), 1) × 12 and that synchronous mode sets only NFIXED and FIXEDLON.
  - H23/W02: about 33° for every rotation slower than 20 days (N = 12, skip 32.7°).
  - H23: up to 17% over and 8% short. The equatorial row runs 0.9171–1.1737 of its mean.
  - H24/G02: summer rain to 60°, and 9 to 36% of land under 0.5 mm a day in `A28_dim5_sun_test` (Terluna GCM
    README:662).
  - G17: −15.7 → −13.3 W m⁻², 294.31 → 295.20 K, and +1.86 W m⁻² at the top of the air, from the drive's yearly
    records.
  - G14 (at least 20 K), G05 (11.5 K, Terluna GCM README:889), G01 (1.6–2.5 K as settled values) and H11
    (5.8 W m⁻²).
  - N01 (Terluna CRM README:2167), G09 (55–80 km, :1454), G10 (0.0081 of 2.72 km⁻² yr⁻¹) and G11.
  - V04: 0.303% and 5.44% are largest differences, so "to 0.3%" and "up to 5.4%" hold.
  - H21 (2.457), G04/S07 (295 K; 5.0 → 3.0%) and S03 (H/R 0.0301, three hundredths).
- **Physical inferences in paragraph 2.**
  - The Sun clock errs in hour angle alone, so every zonal mean of the arriving sunlight is kept, and the global
    mean with it. The check JSON gives a global mean of 293.5 W m⁻².
  - The orbit default keeps the annual global mean. Earth's 1 AD eccentricity of 0.0175, against 0.016715,
    changes it by about 1×10⁻⁵.
  - The albedo fell by 0.008; 0.008 × 293 W m⁻² ≈ 2.4 W m⁻², which equals the clouds' change in sunlight. The
    global means did move through the clouds.
- **Yang et al. 2023.**
  - The cover values are right: 26.9/41.1%, 94.8/81.7% and 90.4/97.4%.
  - The quasi-global domain and the location of the largest differences, on the night side and at high
    latitudes of the day side, are right (pp. 3–4).
  - The GCMs' cover does follow relative humidity, stratification and large-scale updrafts (p. 4).
  - TRAPPIST-1e's 6.1-day rotation (p. 3) is right. "Broadly similar" is the authors' own phrase
    (Discussion, p. 7).
- **Braam et al. 2022.** They use a cloud-top-height law (Price and Rind's oceanic form), whose coefficients
  "have been tuned to match observed LFRs on Earth" (pp. 4, 13–14).
- **Sergeev et al. 2025.**
  - The storm-resolving N1280 runs use McCaul et al.'s scheme, 95% from the upward graupel flux at −15 °C and 5%
    from the total ice water path. It was "originally derived from observations of severe thunderstorms over the
    United States" (p. 3).
  - The N96 runs use Price and Rind's law.
  - "Along the route Sergeev et al. propose" matches their "explicit electric charging scheme coupled with a
    cloud-resolving model" (Sect. 4.2, p. 9).
- **Vincendon and Langevin 2010.**
  - Titan's aerosol scale height is "80 ± 10 km" (abstract).
  - Plane-parallel surface–aerosol separation holds "typically less than 80° for Mars and 65° for Titan"
    (Sect. 1, pp. 1–2).
  - 80/2575 = 0.031, against the test world's 0.030. "Although" bounds Titan's radiation outside the models.
- **Way et al. 2018 and Yang et al. 2014.** These support reach.tex:47–60 and next.tex:35–43.
  - Way et al. ran sidereal periods X001–X256, including 16 and 64 days at S0X 1.0, with zero obliquity and
    eccentricity, and completed runs up to S0X 2.9.
  - Yang et al. used CAM3 with Earth's radius and gravity, zero obliquity and eccentricity and a Sun-like star,
    with cloud albedo as the main reason for the change with rotation.
  - The 77.6-day solar day for a 64-day rotation is the paper's own calculation for a 365.25-day prograde year
    (`regime_calc.json`; 1/(1/64 − 1/365.25) = 77.6). Way et al.'s Table 2 note lists 76.6 days for X064, but the
    paper attributes its value to its own calculation, so it stands.
- **Next.tex, "A test of the reach."** The conditions match Way et al. Each clause is in the state of a test
  still to run.
- **Results.** The "Ranked by form" figures (at least 20 K, about 6 K, 0.65 K, 1.6–2.5 K) match G14, G05, G03
  and G01, and "Given the reference's spectroscopy" keeps the reference's condition.
- **Conclusion.**
  - Lines 13–20, 37–40, 47–59 and 61–66 hold as written.
  - Lines 71–75 match G04 and Next steps.
  - Lines 75–77 ("known so far from the code's arithmetic") keep the calculation state.
- **Abstract.**
  - "Many" is weaker than Deitrick et al.'s "Most studies of exoplanet atmospheres using GCMs have adapted codes
    developed for Earth or solar system planets" (Sect. 1).
  - The constructed-world sentence keeps the design's own evidence state (S15).
  - The defect sentence keeps the calculation state (H23, W06).
  - "The only world the repaired codes have run on away from Earth's values" matches reach.tex:43–45.
  - The sensitivity figures match G01, G14 and G05.
- **The author's direction.** The abstract and the closing section claim no run of the adapted models on another
  world. The Titan sentence and the Way test keep their evidence states. Findings 2, 3 and 4 mark where a
  statement about other worlds reaches past its evidence or into the wrong state.

## 4. Counts

| Severity | Count | Findings |
|---|---|---|
| BLOCKING | 2 | 1, 2 |
| MAJOR | 4 | 3, 4, 5, 6 |
| MINOR | 13 | 7–19 |
| Total | 19 | |
