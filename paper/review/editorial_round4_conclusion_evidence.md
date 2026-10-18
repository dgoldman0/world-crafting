# Editorial round 4: evidence review of the closing section and its revised neighbours

## 1. Record

- **Reviewer.** A fresh Claude subagent (Claude Opus 5.5), given the brief, AGENTS.md and the evidence
  alone. `paper/review/` (apart from this file) and `paper/notes/` stayed unopened, and no earlier review
  was sought.
- **Date.** 2026-10-17.
- **Snapshot.** Commit 798f68b (`798f68bc77842d568764de714175528b9fd410e7`). Every repository file was read
  with `git show 798f68b:<path>`; this record is the only file written.
- **Scope, with sha256 at 798f68b** (the first two match the brief):

| File | Passages | sha256 |
|---|---|---|
| `paper/sections/conclusions.tex` | whole section | `d94c7cb2f7fa69c51c124d0c196a13a66e5cd87f9ab9aefa85e15f92149fbd3b` |
| `paper/sections/abstract.tex` | whole abstract | `67b5fcba63d5694ddd4eba67cacd70fdf7d1f6d03c19e7a5ec2a8a32e6a92c4c` |
| `paper/sections/results.tex` | L48–51 (G17), L51–53 (curved air), L81–85 (GCMs with diagnostic cloud schemes), L90–93 (Ranked by form) | `4c8204187de042831cdb17cf6335f56efd7cad1a4e568708a16769e5442810eb` |
| `paper/sections/reach.tex` | L38–40 (SWAN and SWASH), L42–43 (natural worlds), L45–58 (Worlds near the existing fits), L88–91 (caption of Table tab:reach) | `43a79acef7ec8ed0309f66b004c503490bd22b1530b237ff620de4a13a679c11` |
| `paper/sections/next.tex` | L35–42 (A test of the reach) | `074e611059513edd423b2e5754977d438b0ab1da6978a391bd70bfe0d200acea` |

- **Evidence files relied on, sha256.**
  - `AGENTS.md` `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32`
  - `paper/claims.json` `8bb7e9e6cf2010e75be6f6890357c0238798bc27ab9c2b7412cb61ab8507e8e1`
  - `paper/references.bib` `c0c9662b362141759bce9a27bb566e7ee6a00479ef773273f1dc109d7888747e`
  - `paper/sources/manifest.json` `334f5973fe6339026237ca7953369c34e5f4a1cce89ef935bccd7ccfa76a66a4`
  - Other sections: `introduction.tex` `b8325d641b56d6da32cffbcaa143e26461495322235c2de3b0709402f1ef5b72`;
    `worlds.tex` `453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112`; `assumptions.tex`
    `fef76870ffb4f1ddbaa79de5dec39ec1d141a845bdb247171100652e10b96a77`; `repairs.tex`
    `bb1d22c01616fdaf454280acded56316b7995af2a8fc3bb5a255af52c92e793c`; `verification.tex`
    `4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00`; `appendix.tex`
    `1fec348f0acd47080149c693fdb4f64be59a1d1c2214edcafe8851501dfbebac`; `availability.tex`
    `496434ae301b500a3f7dcec2750af08b8a4d1789c437844ab1318e3ff35f762d`
  - `paper/data/regime_calc.json` `7a2935a8fbe6086c577097b838825c5415ba99f0adf040af62f5e4bcd370e7d1`;
    `paper/data/repairs.json` `3dada16f0e39dba9fe576587da12764ceceaa1ad4f421b33d8dffbe1826b4987`;
    `paper/data/worlds.json` `70dabbec07bf13ab1b31d1e60904d33eac44d0928f9ab50b965937eb3f7916f0`
  - `notes/exoplasim.md` `707d97ef683d2650db8044cfee18f3a3ac7c82675dc37f4222476a6a4c978bf2`;
    `notes/defect_log.md` `c6e7aa541898ce52b68eae35907a9d501885a6330f062f04a6899ad144dd491d`;
    `notes/verification_record.md` `983329688203341ce74e4253acfb72e490b9d8efd252893d1d7b76dc97413ddc`;
    `notes/waves.md` `9f7a775ed1b8a297a4d4a8cf0cd416a8e732b8367cf9f241aaa15dc69cb28102`;
    `models/swan/README.md` `3699e5e564fa484d36b1aa6c91434ab8119beeb3a50de8f72625db97476f8d3f`
  - Terluna at 186b294: `climate/gcm/README.md` `267413c2aa248c3b7581d796ef83de826fbe6764d6d03c9abd1677fee03150fb`;
    `climate/crm/README.md` `95776d41c55b3a3a372d3752ff367b66c45f3a98a1609b2cddfd953f49754acd`;
    `research/decisions.md` `cfca4e5a14d98925bf2f2584566f5a3a1f76970d9f7494ac3cab6f51030816c2`
  - Research drive, `gcm-runs/<run>/progress.json`: `A28_dim5`
    `619f3de9adeafa38803e60fc4b311278f9c3bf9f681adcc1f69c05b9b16d8e61`; `A28_dim5_sun_test`
    `0d8563dbbe8c815b92c88b29943c7a068e9d4b9fd743738a9da38ba08df7b816`; `A28_dim5_moon`
    `d287252f152cb52f5b9f07f35f1e51fca87bddab6226fd960a1c35bdfc31be6d`; `A28_dim5_moon_geometry`
    `9db22a96a8041eeb5ec4e95d5b88785557eefe7476c11b81aec4e23cd53b7de1`; `A28_dim5_moon_geometry_gases`
    `03427b49b543ec88b8622e598df7d6f2cea4f01db6ff914a84f4d41c96cb013c`; `A_uncalibrated`
    `dcf6ab67fa0b01fe9e8b566c9277de9e108e11b9bd500a002dd18c5b73521b2f`; `A`
    `b832b428891da3ac70d21911897b95dad5d8796e79f44497bbd67c4ace814a25`
- **What was read.** The five scoped files whole; the seven other sections whole; all 108 register entries
  with their sources and states; the regime, repairs and worlds extracts; the ExoPlaSim, waves, defect-log
  and verification notes at the lines the register cites and the lines named below; the SWAN patch README
  whole; Terluna's GCM README at L280–303, L626–680 and L1036–1070, its CRM README at L1454–1456,
  L2365–2397 and L2504–2528, and `research/decisions.md` L51, L125 and L370; the seven drive summaries
  above, from which the G17, G03 and G14 means were recomputed.
- **Source originals opened** (`paper/sources/originals/`, text taken with `pdftotext -layout`; each sha256
  matches `manifest.json`):
  - `yang2023cloud.pdf` `0637811e…bc41`: main text, Methods, Supplementary Texts 1–9 and Tables 1–4 as the
    arXiv file carries them; `yang2023cloud_si.pdf` `1cc0a582…5554`: Text 3, Text 7 and Table 3, which give
    the same values.
  - `braam2022lightning.pdf` `26486cfc…f8c7`: Sects 1, 2.1–2.4, 3.1–3.2, 4.3 and 5.
  - `sergeev2025lightning.pdf` `b2c3352f…c6df`: whole text.
  - `vincendon2010spherical.pdf` `afcdf418…a7e9`: abstract, Sect. 1, Sect. 2 set-up for Titan, Sect. 3.1.
  - `way2018climates.pdf` `476e3e96…4820`: abstract, Sects 1–2.1, Sect. 3.1 opening, Table 2.
  - `yang2014strong.pdf` `3b285234…5c6f`: abstract, Sects 1–3.
  - `boutle2017exploring.pdf` `88e68668…3b15`: Table 1, orbital period.
  - `banfield2015winds.pdf` `252db567…c325`: Sect. 3.2.2 and the SWAN passages of Sect. 4.
  - `swan4151user.pdf` `bb35675b…1af1`: the GEN3 command (AGROW) and INIT entries.
  - `deitrick2020thor.pdf` `52da49f4…7d7c`: Sect. 1.

## 2. Findings

Line numbers are those of `git show 798f68b:<file>`. Each finding gives its severity, location, text,
evidence and a proposed correction.

### F1. MAJOR. `conclusions.tex:21–26`. What the global means of Yang et al. show

**Text.** "A modeller finds such an error in maps of sunlight by longitude and of rain by season, and a
comparison of models by their global means can pass it: on two tidally locked planets, the quasi-global
cloud-permitting runs of \textcite{yang2023cloud} covered 27 and 41\% of the sky with cloud and two GCMs
whose cover follows relative humidity, stability and large-scale ascent covered 82--97\%, most of the
difference on the night side and at high latitudes of the day side, while the three models' global-mean
surface temperatures and albedos came out broadly alike."

**Evidence.** The cover figures are themselves global means: "In global mean, the simulated cloud coverages
in SAM are 26.9% and 41.1% … the corresponding values are 94.8% and 81.7% in CAM3 and 90.4% and 97.4% in
ExoCAM" (Yang et al., arXiv p. 3; Supplementary Table 3, "Global-mean values", total cloud fraction 27, 95,
90 and 41, 82, 97). A comparison by global means therefore sees cover two to three and a half times the
cloud-permitting model's. The quantities that agreed are the global-mean surface temperature, 243.4, 239.7
and 242.6 K on TRAPPIST-1e and 262.5, 252.7 and 267.6 K on K2-72e, and the planetary albedo, 18.1, 29.1 and
22.1% and 37.4, 47.0 and 39.0% (Supplementary Table 3), which the authors call "broadly similar"
(Discussion, p. 7) and differences that are "relatively small" (Supplementary Text 7). The example is also a
difference between two kinds of model whose truth the authors leave open (GCMs "may have overestimated the
cloud liquid water amount and cloud coverage"), while "such an error" in the sentence is a code defect that
moves sunlight.

**Correction.** "…, and a comparison of models by global-mean surface temperature and albedo can pass it:
on two tidally locked planets, the quasi-global cloud-permitting runs of Yang et al. covered 27 and 41% of
the sky with cloud and two GCMs whose cover follows relative humidity, stability and large-scale ascent
82–97%, most of the difference on the night side and at high latitudes of the day side, while the three
models' global-mean surface temperatures, within 4 K on TRAPPIST-1e and 15 K on K2-72e, and albedos,
18–29% and 37–47%, came out broadly similar by the authors' account."

### F2. MAJOR. `results.tex:81–85`. One study stated as a property of a class of models

**Text.** "GCMs with diagnostic cloud schemes differ widely from cloud-permitting runs on tidally locked
planets: on TRAPPIST-1e and K2-72e, CAM3 and ExoCAM, … covered 94.8 and 81.7\% and 90.4 and 97.4\% of the
sky, against 26.9 and 41.1\% in a quasi-global cloud-permitting model, while the three models' global-mean
surface temperatures and albedos came out broadly alike \autocite{yang2023cloud}."

**Evidence.** The opening clause states a property of GCMs with diagnostic cloud schemes in general. Its
support is one study, with two GCMs of one lineage ("ExoCAM is similar to CAM3, except that its radiative
transfer module is more accurate", Yang et al., Methods, p. 14) against one cloud-permitting model on two
planets. AGENTS.md, "Claims stay within their evidence": "characterising a whole field takes evidence about
the whole field." The numbers match the source (arXiv p. 3). "Broadly alike" repeats the authors' judgement
over spreads of 4 and 15 K in surface temperature and up to 11 points in albedo (F1).

**Correction.** "In the one comparison of this kind cited, two GCMs whose cover follows relative humidity,
stability and large-scale ascent differed widely from a cloud-permitting model on tidally locked planets: on
TRAPPIST-1e and K2-72e, CAM3 and ExoCAM covered 94.8 and 81.7% and 90.4 and 97.4% of the sky, against 26.9
and 41.1% in a quasi-global cloud-permitting model, while the three models' global-mean surface
temperatures and albedos came out broadly similar by the authors' account (Yang et al. 2023)."

### F3. MAJOR. `conclusions.tex:59–61`. The released SWAN departs through its knee only with its linear wind input on

**Text.** "Patched, SWAN reproduces a sixfold gravity scaling of an Earth sea to 0.3\% in wave height, where
the released code missed it by 5.4\% and departs from it on any sea under another gravity, the ancient seas
of Mars among them;"

**Evidence.** The 1 Hz knee sits in `SWIND0`, which "runs only when `GEN3 ... AGROW` sets the linear
coefficient …, so without `AGROW` the patch has no effect" (`models/swan/README.md:61–63`). The SWAN 41.51
manual, GEN3 command: "if this keyword is NOT used, the wave growth term of Cavaleri and Malanotte (1981) is
NOT activated". The reach section scopes the loss itself: "SWAN, in the configuration used, loses gravity
similarity through its wind-input knee, fixed at 1~Hz" (`reach.tex:34–35`). Banfield et al. (2015,
Sect. 3.2.2) describe their SWAN wind input as Miles's mechanism "later improved by Janssen (1989)", with
Komen whitecapping, Madsen bottom friction and Battjes–Janssen breaking, and name no linear growth term, so
whether their Mars runs met the knee is unreported. The released code's other latent Earth constants act
only where their options are chosen (ST6 drag, exact quadruplets, JONSWAP friction, INIT DEFAULT;
`notes/waves.md:265–276`). The same unscoped wording stands in `assumptions.tex:22–26`, outside this scope.

**Correction.** "…, where the released code missed it by 5.4%, and in any run that switches on its linear
wind input (AGROW) under another gravity, the ancient seas of Mars among them, the released code departs
from that scaling through its 1 Hz knee;"

### F4. MAJOR. `conclusions.tex:79–80`, with `conclusions.tex:58–59`. What laboratories and similarity runs can test in the microphysics

**Text.** "… while cloud remains to be calibrated for that world against cloud-resolving runs whose
microphysics can be tested in laboratories and by similarity runs." And L58–59: "Gravity stays fixed in a
wave tank or a cloud laboratory on Earth, so a model's dependence on it is tested by similarity runs."

**Evidence.** A similarity check tests "whether gravity enters the code consistently", and "runs Earth's
empirical laws at the scaled gravity with their Earth coefficients, which it leaves untested there"
(`verification.tex:7–13`). CM1's microphysics departs from similarity by construction: "The microphysics does
not stretch: drops, snow and graupel fall at speeds that follow gravity to other powers, and rain forms at
rates that do not depend on it" (Terluna `climate/crm/README.md`, "The gravity pair", L2510–2514). A
similarity pair therefore "would measure how far the scaled microphysics departs from similarity"
(`next.tex:70–72`), a size of effect under CM1's own laws, and the pair designed for it failed to convect
(V06). The gravity-dependent laws, the drop-size limits and breakup, stay Earth's (H21) and stand in the
"Beyond them" column (`reach.tex:103`), and a laboratory on Earth holds gravity at Earth's
(`conclusions.tex:58`). Laboratories reach the laws whose conditions Earth can supply, such as the sign of
riming charge (N01). The two tests named in the closing clause thus leave the gravity-dependent microphysics,
the part that changes with the world, without a test; the clause reads as closing the last Earth dependence
of the new world's cloud calibration.

**Correction.** L79–80: "…, while cloud remains to be calibrated for that world against cloud-resolving
runs whose microphysics keeps Earth's fits apart from its scaled fall speeds: laboratories can settle the
laws whose conditions Earth reaches, such as the sign of riming charge, a similarity pair can measure how
far the scaled microphysics departs from similarity, and the drop-size limits and breakup remain Earth fits
at other gravities." L58–59: "… so whether a model carries gravity consistently is tested by similarity
runs."

### F5. MAJOR. `conclusions.tex:76–78`; also `conclusions.tex:38–40` and `abstract.tex:20–21`. The closing bound left undefined

**Text.** "For a new world whose gases, pressures and temperatures the line-by-line spectroscopy covers, and
whose air stands within a few hundredths of its radius, the radiative geometry can be computed from the
world's own column and, once a scheme is built from that spectroscopy, the gas absorption as well, …"; L38–40,
"on any column whose gases, pressures and temperatures that spectroscopy covers"; abstract L20–21, "within the
gases, pressures and temperatures the spectroscopy covers".

**Evidence.** The paper defines the reference's spectroscopy as "HITRAN lines of water, carbon dioxide and
oxygen, a re-implementation of MT\_CKD~4.3, collision-induced absorption and Rayleigh scattering"
(`repairs.tex:121–123`) and gives it no range of pressure or temperature. Its emulation was checked at
288–290 K and on a saturated 330 K lunar column (R08); its checks against other codes cover water-only
longwave at constant gravity and Rayleigh scattering to an optical depth of 1.5, while "Its carbon dioxide,
oxygen, collision-induced absorption and sunlight on the lunar column have yet to be compared with an
independent code" (`verification.tex:63–69`; V16). The reach section names the examined composition,
"nitrogen, oxygen, argon, water and modest carbon dioxide" (`reach.tex:77–78`), and puts "CO$_2$- or
CH$_4$-dominated air" beyond the adapted models (`reach.tex:109`); the bound as written lets a reader count
any atmosphere whose gases have HITRAN lines. "Within a few hundredths of its radius" also reaches past the
one value run, the test world's 0.030 (`worlds.json`, `h_over_r` 0.03015), which `reach.tex:79–80` gives as
the limit itself: "scale heights up to a few hundredths of the radius, the test world's".

**Correction.** "For a new world of nitrogen–oxygen air with water and modest carbon dioxide, at pressures
and temperatures near those the reference has been checked at, and with air no taller against its radius
than the test world's three hundredths, the radiative geometry can be computed from the world's own column
and, once a scheme is built from the reference's spectroscopy and that spectroscopy has been checked against
an independent code, the gas absorption as well, …", with the same bound at L38–40 and in the abstract.

### F6. MAJOR. `abstract.tex:12–14`. The form-to-repair mapping without its conditions

**Text.** "Constants and units of time took general repairs built to hold on other worlds, geometry a method
computed for each world's column, and the radiation's fits calibrations to an in-house line-by-line model
that hold near the columns they were fitted on."

**Evidence.** In Table tab:inventory (`assumptions.tex:163–212`) three of the five geometry rows stay "Open"
(the vertical grid, PlaSim's thin shell, CM1's flat slab) beside two "Method, lunar table" rows; the
constants include "Avoided" (the orbit default; SWAN's unselected options), "Bypassed" (the beta plane),
"Bound" (the ground-strike rule), "Setting" (SWAN's air density) and "Open" (RRTMG's Sun; WRF-ELEC's other
thresholds); the calendar, a unit of time, is "Avoided". The introduction ("The class of a repair followed
largely from the form of the Earth value it removed", `introduction.tex:82`) and the conclusion ("where a
value was repaired, the kind of repair followed largely from its form", `conclusions.tex:4–5`) carry both
conditions, which the abstract drops.

**Correction.** "Where a value was repaired, constants and units of time took, for the most part, general
repairs built to hold on other worlds, the radiative geometry a method computed for each world's column, and
the radiation's fits calibrations to an in-house line-by-line model that hold near the columns they were
fitted on; the dynamics keep their thin shell and constant gravity."

### F7. MAJOR. `reach.tex:38–40`. SWAN and SWASH at any gravity, without the configuration and code paths

**Text.** "SWAN and SWASH are built to run water seas at any gravity as the scaled image of an Earth sea, and
have been tested at a sixth of Earth's gravity, with Earth's empirical laws."

**Evidence.** The similarity checks "show that nothing on the code paths they exercise still assumes Earth's
gravity (for SWAN, only after patch 01): for SWAN, Komen input and whitecapping with Wu drag at a fixed wind,
AGROW, DIA and depth breaking, on Cartesian strips started from rest; for SWASH, the non-hydrostatic solver,
the spectral wavemaker, breaking and wetting. Spherical geometry, nesting and stationary iteration were
checked separately or not at all" (`notes/waves.md:62–67`; `verification.tex:47–51`). SWAN's ST6 drag routines
(`G` 9.8 and 9.81, `RHOW`, `RHOA`), exact quadruplets (`g` 9.81), JONSWAP bottom friction (0.038 m²/s³) and
INIT DEFAULT's 2 s keep Earth's constants, and SWASH hard-codes Earth's rotation (`notes/waves.md:265–276`;
`models/swan/README.md:211, 266–270`; `assumptions.tex:211`); SWAN's air density is one compiled value per
build (`models/swan/README.md:113–115`). The conclusion keeps the condition: "has been tested at a sixth of
Earth's on the code paths those tests ran" (`conclusions.tex:61–62`). The Seas row of Table tab:reach,
"Similarity at any gravity" (`reach.tex:112`), outside this scope, needs the same bound.

**Correction.** "On the code paths of the lunar configuration (for SWAN, Komen input and whitecapping with
Wu drag, AGROW, DIA and depth breaking; for SWASH, its solver, wavemaker, breaking and wetting), SWAN and
SWASH are built to run water seas at any gravity as the scaled image of an Earth sea, and on those paths
have been tested at a sixth of Earth's gravity, SWASH also at four times that, with Earth's empirical laws;
SWAN's ST6, exact quadruplets and bottom friction, and SWASH's rotation, keep Earth's constants."

### F8. MINOR. `conclusions.tex:22–24`; `results.tex:83–84`. The two cover figures follow two definitions

**Evidence.** SAM's cover is diagnosed from condensate thresholds, 0.01 g kg⁻¹ at a level and 0.02 kg m⁻² in a
column, so each cell is 0 or 100% at each step, while the GCMs' parameterised cover takes partial values and
an overlap rule (Yang et al., Supplementary Text 3). Part of the 27–41 against 82–97% difference is
definitional.

**Correction.** Add once, in Results: "the cloud-permitting model's cover counted by a condensate threshold".

### F9. MINOR. `conclusions.tex:61–63`. The drag law's lunar uncertainty lies chiefly in its gravity

**Text.** "… and Earth's empirical laws of drag, wind input and breaking remain uncertain at each such sea's
ratio of air to water density."

**Evidence.** "With Charnock's roughness at each gravity the lunar drag would be larger and the ratio higher,
by about a tenth to a half" (`results.tex:167–168`; G12, 11–51%). Charnock's roughness, 0.018 u*²/g, carries
gravity (`worlds.tex:90–91`; `models/swan/README.md:244–246`). The air–water density ratio enters Komen's
wind input (`PWIND(9)`, `models/swan/README.md:97–100`); whitecapping and depth breaking act through steepness
and depth.

**Correction.** "… remain uncertain under each such sea's gravity and ratio of air to water density: on the
Moon, Charnock's roughness in place of Wu's drag raises the wave heights by a tenth to a half."

### F10. MINOR. `conclusions.tex:9–10`. A calculated bias stated as an outcome

**Text.** "The convective-cover unit adds about 0.23 to the convective cover of a synchronous run of
TRAPPIST-1e"

**Evidence.** W06 is a calculation from ExoPlaSim's source (`regime_calc.json`: model day 6.20 d, bias
0.228); no such run was made, and Slingo's cover is capped at 0.8 (`notes/exoplasim.md:95–98`;
`assumptions.tex:112–113`).

**Correction.** "By that arithmetic the convective-cover unit would add about 0.23 to the convective cover of
a synchronous run of TRAPPIST-1e, up to the formula's cap of 0.8, …"

### F11. MINOR. `conclusions.tex:47–49`. The polarity decided within the model

**Text.** "… would decide the polarity of the lightning."

**Evidence.** G11 is a sensitivity and N01 a conditional model result; `next.tex:80–81` frames the decision
within the runs: "would decide whether the lunar ground strikes are negative, as under Saunders and Peck's
law, or positive, as under Takahashi's".

**Correction.** "… would decide which polarity the model's lunar lightning takes."

### F12. MINOR. `conclusions.tex:51–52`. Sergeev et al.'s microphysical law

**Text.** "… or, in Sergeev et al.'s storm-resolving runs, from the graupel and ice aloft."

**Evidence.** McCaul et al.'s scheme as Sergeev et al. run it takes 95% of the flash rate from the upward flux
of graupel at the −15 °C isotherm, w·q_g, and 5% from the column's total ice water path (Sergeev et al. 2025,
Sect. 2.2.1, Eqs 1–3). Outside this scope, `results.tex:150–152` gives the cloud-top law to Braam et al. alone,
while Sergeev et al. also ran it on their N96 runs (Sect. 2.2.2, Table 1).

**Correction.** "… from the upward flux of graupel at the −15 °C level and the column's ice."

### F13. MINOR. `abstract.tex:4–6`. The design's retention in the indicative

**Text.** "by one design's own models, a shield in space that removes the ultraviolet heating the upper air
keeps Earth-like air under a gravity too weak to hold it naturally."

**Evidence.** S15, a conditional model result: losses of 0.61–1.4 kg/s over a solar cycle, 64–148 billion
years to remove the air (`regime_calc.json`, `retention`; Terluna `research/decisions.md` L125). The
conclusion gives the same result as "would hold … to losses of 0.6--1.4~kg\,s$^{-1}$"
(`conclusions.tex:67–70`).

**Correction.** "… would keep Earth-like air, losing 0.6–1.4 kg/s, under a gravity too weak to hold it
naturally."

### F14. MINOR. `abstract.tex:6–8`; `conclusions.tex:3`. SWASH configured and unmodified

**Text.** "Four Earth-built codes, … SWAN~41.51 and SWASH~12.01, were adapted to such a world"; "four
Earth-built codes adapted".

**Evidence.** "SWASH runs unmodified, with lunar gravity as an input and SWAN's spectra at its boundary"
(`repairs.tex:185–186`; R15).

**Correction.** "…, were adapted to such a world, SWASH by configuration alone".

### F15. MINOR. `abstract.tex:10–11`. The three defects' conditions

**Text.** "three of the defects, exact or nearly so at Earth's values, bias ExoPlaSim's runs of slowly
rotating and tidally locked planets by the code's own arithmetic."

**Evidence.** The Sun clock acts in non-synchronous runs on the default solar geometry (H23); the
convective-cover unit in any run whose model day differs from one Earth day, synchronous runs included
(W06); the orbit default in any run that configures an obliquity or eccentricity without fixing the orbit,
at any rotation (W06; `reach.tex:23–24`). The conclusion states the conditions: "runs of natural planets that
meet their conditions" (`conclusions.tex:9`).

**Correction.** "… bias, by the code's own arithmetic, ExoPlaSim's runs that meet their conditions: slow
non-synchronous rotation, a model day other than one Earth day, or a configured orbit."

### F16. MINOR. `abstract.tex:20–22`. The cloud fit's state

**Text.** "… while cloud fitted to cloud-resolving runs remains a calibration for each world."

**Evidence.** On the test world "that fit is a step still to run, and those runs compute with Earth-fitted
microphysics of their own" (`conclusions.tex:41–42`; `next.tex:18–25`).

**Correction.** "… while cloud would remain a calibration for each world, fitted to cloud-resolving runs of
that world, a fit still to be made on the test world."

### F17. MINOR. `abstract.tex:17–19`; `conclusions.tex:28–31`; `results.tex:90–93`. The ranking leaves out the longwave test and the geometry

**Evidence.** The longwave correction with the ice optics warmed the design case 11.5 K over years 10–19,
toward 306.8–307.1 K (G05, G13; `results.tex:85–88`), "The largest single sensitivity" (`next.tex:9`); the
abstract and conclusion rank the fits by the first calibration and the cloud settings alone. In
`results.tex:90–93`, "Ranked by form, the effects on the test world grow from the units and constants, … to
the fits" leaves out the geometry, whose curved air moved the global mean 0.65 K on the first channels (G03),
and the gas-band calibration's 2.2 K (G03) lies inside the general repairs' 1.6–2.5 K.

**Correction.** In the abstract and conclusion, add "and the longwave correction, switched on with the ice
optics, by 11.5 K". In Results: "Ranked by form, the effects grow from the geometry, whose curved air moved
the global mean by 0.65 K, and the units and constants, whose single general repairs moved it by 1.6–2.5 K,
to the largest of the fits: …".

### F18. MINOR. `reach.tex:49–55`. A requirement read from the code

**Text.** "ExoPlaSim needs its general repairs, its fixed-orbit setting and its released radiation, …"

**Evidence.** W03 records that such planets "should need only ExoPlaSim's general repairs (untested; no run
made)", and `next.tex:40–42` leaves the general repairs' arithmetic untested off the test world. The sentence
closes on "ExoPlaSim's runs of these planets have yet to be made", which carries the state at its end.

**Correction.** "ExoPlaSim would need …".

### F19. MINOR. `reach.tex:89`. "The middle column" in a table of four

**Text.** "The middle column gives the reach each repair was built for;"

**Evidence.** Table tab:reach has four columns (`reach.tex:93`), two of them in the middle.

**Correction.** "The column of what the adapted models represent gives the reach each repair was built for;".

### F20. MINOR. `next.tex:36–41`; `conclusions.tex:73–76`. The test's configuration

**Evidence.** The orbit default acts only when an obliquity or eccentricity other than Earth's is configured
(W06). Way et al. set "Planetary obliquity and eccentricity are zero", modern Earth's land and topography, a
land albedo of 0.2 and two oceans, one of them a 100 m thermodynamic ocean without heat transport (Way et al.
2018, Sect. 2.1 and Sect. 3.1). Released against repaired runs measure the orbit default's bias at that zero
obliquity, and the comparison with ROCKE-3D's climate separates the defects from the two models' physics once
land, ocean and orbit match.

**Correction.** "Released and repaired ExoPlaSim on Earth-air planets at Earth's insolation, rotating once in
16 and 64 days, two of the sidereal periods of the ROCKE-3D runs of Way et al., with their zero obliquity and
eccentricity and their land, …"

## 3. Checked and sound

- **Numbers in the conclusion.** 0.23 (W06; `regime_calc.json` 0.228 at a 6.10-day rotation); about 33° for
  rotations slower than 20 days (`regime_calc.json` 32.7° at N = 12 from 21 days, 15.7° at 16–20 days); 17%
  and 8% (H23: up to 17% over near 164° E, 8.3% short at 270–57° E); 60° and 9 to 36% (H24, G02; Terluna GCM
  README L650 and L661–664); 2.4 W m⁻², 0.9 K and the heat still gained (G17; drive summaries: `A28_dim5`
  years 15–24 294.311 K, −15.698 W m⁻², albedo 0.29307, top of the air −0.49 W m⁻²; `A28_dim5_sun_test`
  years 0–1 295.195 K, −13.32 W m⁻², 0.2851, +1.86 W m⁻²); 27 and 41% and 82–97% (Yang et al.,
  Supplementary Table 3); "most of the difference on the night side" (the reviewer's calculation from
  Supplementary Table 3, with each day-side mean taken as twice the global mean less the night-side mean:
  the night side alone carries 55–65% of each GCM's difference from SAM in global-mean cover); at least 20 K (G14:
  `A_uncalibrated` year 12 at 315.51 K and still gaining 15.5 W m⁻², `A` years 30–39 at 295.51 K); up to about
  6 K (`repairs.json`: more low cloud settles near 289.0 K against 294.9 K); 1.6–2.5 K (G01; `repairs.json`
  2.30 and 1.76 K, settled 2.5 and 1.6 K); 5.8 W m⁻² (H11); about 80 km and about 65° (Vincendon and
  Langevin, abstract and Sect. 1; 80 km over 2,575 km is 0.031); 4–8 m s⁻¹, 0.02–0.2 g m⁻³, −5 to −16 °C
  (N01); 55–80 km (G09; CRM README L1454–1456); about a hundredth (G10; `regime_calc.json` 0.0081; CRM
  README L2369–2370); 0.3% and 5.4% (V04); 2.46 (H21; `regime_calc.json` 2.457); 0.6–1.4 kg s⁻¹ and 60 to
  150 billion years (S15; `regime_calc.json` 64–148 billion years); 16 and 64 days among Way et al.'s
  sidereal periods of 1–256 days (Table 2).
- **Attributions.** Braam et al. set flash rates by Price and Rind's oceanic law, 2.0×10⁻⁵ H^4.38, and
  "acknowledge that the coefficients used in Equation 1 have been tuned to match observed LFRs on Earth"
  (Sects 2.4 and 4.3), on Proxima Centauri b. Sergeev et al. ran McCaul et al.'s scheme in storm-resolving
  N1280 runs and Price and Rind's on N96 runs of TRAPPIST-1e, the first "originally derived from
  observations of severe thunderstorms over the United States" and the second "developed for Earth"
  (Sects 2.2.1–2.2.2), and name as "A possible route towards a more quantitative result … an explicit
  electric charging scheme coupled with a cloud-resolving model" (Sect. 4.2). Yang et al.'s runs are
  quasi-global and cloud-permitting on synchronously rotating TRAPPIST-1e and K2-72e, and the GCMs' cover is
  "empirically parameterized based on relative humidity, atmospheric stratification, and large-scale
  updrafts" (pp. 3–4). Vincendon and Langevin give plane-parallel surface–aerosol codes "typically less than
  80° for Mars and 65° for Titan, which has a larger relative scale height", and infer "an aerosols scale
  height of 80 ± 10 km" (abstract, Sect. 1). Way et al. completed runs up to 2.9 times Earth's insolation
  (X064 at S0X 2.9, Table 2); Yang et al. (2014) used CAM3 with rotation periods from 12 hours to 365 days and
  found the cloud albedo "much higher on slowly rotating planets" (Sects 2–3); Boutle et al. give Proxima
  Centauri b an 11.186-day period (Table 1).
- **Evidence states in the conclusion.** The design's retention "By one design's own models"; the defects'
  biases "by the code's own arithmetic" and "known so far from the code's arithmetic"; the SWAN patch's design
  ("built to keep the scaling at any gravity") apart from its test ("tested at a sixth of Earth's on the code
  paths those tests ran"); the spectroscopic scheme "once a scheme is built"; the cloud fit "a step still to
  run"; Titan's radiation "outside the adapted models"; the proposed ExoPlaSim runs "would measure". "Away
  from Earth's values every change made for the test world has run on it alone" agrees with
  `introduction.tex:83–84` and the caption of Table tab:reach.
- **Universal and quantity words.** "every zonal mean" (the Sun clock errs in hour angle; the instantaneous
  zonal mean of arriving sunlight depends on declination and distance alone); "any planet rotating more
  slowly than once in 20 days" (ExoPlaSim's wrapper floors N at 12 from 21 days on); "all in ExoPlaSim" (the D
  rows of Table tab:inventory); "Some of those Earth-fitted laws"; "two of the three".
- **Physical inferences.** The orbit default keeps the annual global mean of arriving sunlight (Earth's
  eccentricity of 0.0175 for the Moon's 0.016715 changes (1−e²)^−½ by under 2×10⁻⁵); G17's warming runs
  through the clouds (the albedo fall of 0.0080 over 293.4 W m⁻² of mean sunlight is 2.35 W m⁻², equal to the
  cloud shortwave change of 2.38 W m⁻² and to the change at the top of the air, −0.49 to +1.86 W m⁻²); the
  largest stable raindrop scales with √(σ/ρ_w g); cloud tops of 55–80 km lie far above the Earth storms of
  Price and Rind's fit (Braam et al., Sect. 3.2: Earth's oceanic tropical clouds reach 17 km).
- **`results.tex:48–51` and `51–53`.** Every number matches the drive summaries and Terluna's GCM README
  L1042–1056 ("In the first year the clear sky lost 5.4 W/m² … and the clouds returned 3.5 W/m²";
  `A28_dim5_moon_geometry` years 10–19 at 294.243 K against `A28_dim5_moon` years 20–29 at 294.897 K). The
  numbers of `results.tex:90–93` match G01, G14 and G05.
- **`reach.tex:42–43`.** The natural worlds of Figure fig:regimes are Earth, Mars, Titan and Venus
  (`worlds.json`, kind "found"). **`reach.tex:45–58`.** 0.7 points on the 303 K, 338 kg m⁻² column (V07; GCM
  README L280–302); 2.9 times Earth's insolation (Way et al., Table 2); 69.8 against 77.6 days and 265 against
  726 days (`regime_calc.json`, `exoplasim_slow_rotators`).
- **`next.tex:35–42`**, apart from F20: the periods, the released radiation's columns, and the logic by which
  released against repaired runs give the defects and repaired runs against ROCKE-3D the models' differences.
- **`abstract.tex`.** "Many of the general circulation models used for exoplanets were developed for Earth or
  for solar-system planets" lies within Deitrick et al.'s "Most studies of exoplanet atmospheres using GCMs …
  have adapted codes developed for Earth or solar system planets" (Sect. 1); the abstract's numbers match
  G01, G14, G05 and V04.

## 4. Counts

- BLOCKING: 0.
- MAJOR: 7 (F1–F7).
- MINOR: 13 (F8–F20).
- Total: 20.

Passages outside this scope that carry the same faults: `assumptions.tex:22–26` (F3's unscoped SWAN
statement); `reach.tex:112` (F7's "Similarity at any gravity"); `results.tex:150–152` (F12); and
`results.tex:44–45`, which calls the Sun-and-tilt step one "that joined two general repairs with a
calibration", where Table tab:repairs classes the fixed orbit as an avoidance (`appendix.tex:59`).
