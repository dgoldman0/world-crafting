# Editorial round 3: evidence review of "Discussion and conclusions" and five revised passages

## 1. Record

- **Reviewer.** A fresh Claude subagent (Claude Opus 5.5), acting as technical evidence reviewer. It saw no
  earlier review and left `paper/review/` (apart from this file) and `paper/notes/` unopened, as instructed.
- **Date.** 2026-10-17.
- **Snapshot.** Commit e89a394 (`e89a394dff2ce9ce2a570c016ee6357adfec3ec9`). The working tree was clean at that
  commit when the review began; during the review other work modified several files under `paper/` in the working
  tree. Every repository file named below was read at e89a394 with `git show`, so the findings refer to the
  snapshot; only the git-ignored source originals were read from disk, and their hashes match the manifest.
- **Machine load.** Load near 1.3 on 16 cores; heavier reads ran under `nice`.

**Files in scope (sha256 at e89a394)**

| File | sha256 | Passages reviewed |
|---|---|---|
| `paper/sections/conclusions.tex` | `0ceab5bc3331bb70f1e9cd9e863d259ac0c2aa15bb80576592e584686091cfc4` | whole section |
| `paper/sections/reach.tex` | `6c455cb802b9a13a11336f9d18e664a31f92f64a29f375ef239934f510f048c2` | L41–43 ("Of the natural worlds in Figure"); L45–58 ("Worlds near the existing fits.") |
| `paper/sections/next.tex` | `7075a036e4f497191070019df134a055d1c5c0bad25b5cb6217f1426198195a2` | L35–42 ("A test of the reach.") |
| `paper/sections/abstract.tex` | `299a4e7b1a849c7b9291469ae8152e50567f1dbd83cf7d78625cf064b27da11a` | L4–6 (constructed worlds); L15–16 (SWAN); L16–19 ("at least 20~K") |
| `paper/sections/results.tex` | `1764084dcd3a7ab1f902f0b161cbbc24f4e23c6987db94b142a3e871b35c12b7` | L48–52 (claim G17); L82–86 (Yang et al.'s comparison) |

The hashes of `conclusions.tex` and `reach.tex` match those the task gave.

**Evidence files relied on (sha256)**

| File | sha256 |
|---|---|
| `AGENTS.md` (e89a394) | `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32` |
| `paper/claims.json` | `8bb7e9e6cf2010e75be6f6890357c0238798bc27ab9c2b7412cb61ab8507e8e1` |
| `paper/references.bib` | `c0c9662b362141759bce9a27bb566e7ee6a00479ef773273f1dc109d7888747e` |
| `paper/sources/manifest.json` | `334f5973fe6339026237ca7953369c34e5f4a1cce89ef935bccd7ccfa76a66a4` |
| `paper/sections/introduction.tex` | `b8325d641b56d6da32cffbcaa143e26461495322235c2de3b0709402f1ef5b72` |
| `paper/sections/worlds.tex` | `453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112` |
| `paper/sections/assumptions.tex` | `01d5eea0744342fba7ef3eea7d274976cc88744f5d97e4a3ca16b2e1751fb50e` |
| `paper/sections/availability.tex` | `496434ae301b500a3f7dcec2750af08b8a4d1789c437844ab1318e3ff35f762d` |
| `paper/data/regime_calc.json` | `7a2935a8fbe6086c577097b838825c5415ba99f0adf040af62f5e4bcd370e7d1` |
| `paper/data/worlds.json` | `70dabbec07bf13ab1b31d1e60904d33eac44d0928f9ab50b965937eb3f7916f0` |
| `paper/data/repairs.json` | `3dada16f0e39dba9fe576587da12764ceceaa1ad4f421b33d8dffbe1826b4987` |
| `python/climate/results/gcm/sun_check_A28_dim5.json` | `5b922f8d7afede955e791a78c0b3204988a1515f84bca1e670c1880df9162966` |
| `notes/exoplasim.md` | `707d97ef683d2650db8044cfee18f3a3ac7c82675dc37f4222476a6a4c978bf2` |
| `notes/defect_log.md` | `c6e7aa541898ce52b68eae35907a9d501885a6330f062f04a6899ad144dd491d` |
| `notes/electrification.md` | `2cd81eb8edbd77348133a1e4aaca859b52ca4d0015bc5b26bf12e5d93308f59f` |
| `notes/cm1.md` | `75502ec7070a240006db6e4d491a6973cd2f013cc0c0945c3e61fb36b9fa5510` |
| Terluna 186b294 `climate/gcm/README.md` | `267413c2aa248c3b7581d796ef83de826fbe6764d6d03c9abd1677fee03150fb` |
| Terluna 186b294 `climate/crm/README.md` | `95776d41c55b3a3a372d3752ff367b66c45f3a98a1609b2cddfd953f49754acd` |
| Terluna 186b294 `climate/waves/runup.md` | `7104b129074b1a8b361177ee1717a07dc35faf06f47b7b68cbeaa28fe66cd357` |
| Terluna 186b294 `climate/waves/first_experiments.md` | `959868b935ca29c3b4f3f929c987036627f81c884064e4f5887e1a29ec60b2a5` |
| Terluna 186b294 `research/decisions.md` | `cfca4e5a14d98925bf2f2584566f5a3a1f76970d9f7494ac3cab6f51030816c2` |
| drive `gcm-runs/A28_dim5_sun_test/progress.json` | `0d8563dbbe8c815b92c88b29943c7a068e9d4b9fd743738a9da38ba08df7b816` |
| drive `gcm-runs/A28_dim5/progress.json` | `619f3de9adeafa38803e60fc4b311278f9c3bf9f681adcc1f69c05b9b16d8e61` |
| drive `gcm-runs/A28_dim5_moon/progress.json` | `d287252f152cb52f5b9f07f35f1e51fca87bddab6226fd960a1c35bdfc31be6d` |
| ExoPlaSim 3.4.2 as deployed in Terluna's GCM environment: `exoplasim/__init__.py`, `plasim/bld/plasim.f90`, `plasim/bld/rainmod.f90` | `07ea85554ef45172eee24d68c0e8be61b98db86ac276cc6f246ad5c161183903`, `04fd8941a51b9b70cf07791b54bcde33d40deebf7e19d0e60c5eb053748b9129`, `44c0668de3e8f7dbdbea2f35bfbd8fbff0834a62f32e526ca1dc56b818faeb23` (the rainmod hash prefix is the one `A28_dim5_sun_test` records) |

Yearly GCM output read on the drive (`/media/projectspace/terluna-research/gcm-runs/<run>/model/`):

```
a557bf32ab5a67b39fcb6a047274069eb20954a1b0bd6f5eae1cf0ac7e27fcac  A28_dim5_sun_test/MOST.00000.nc
f4ec03a97a1eb9ed50535c11459db5c9ce04d8d1bf0e2032481bd7927f510c34  A28_dim5_sun_test/MOST.00001.nc
8744b6d0e21c95de07d33e8eaf16c51ca0f4d3146dd1a1f4971b80742e04aafb  A28_dim5/MOST.00015.nc
d857751c1975442b3ef2eff78e47ef4fa6f72f918d98add37785dd830607eb3c  A28_dim5/MOST.00016.nc
047196ea52313a6ca65afea76073dc1ce9d6b4f7d7026d406dde0acb6db36bc4  A28_dim5/MOST.00017.nc
9e316fb3880d266ea4b73b04c67c94fecf363616911fc13475deaef023f78a33  A28_dim5/MOST.00018.nc
2eede29bf8e95f641a68a032e5b8b03fc049b3aa6b4e8a3425d5358e9601a803  A28_dim5/MOST.00019.nc
c1f0adc7254fc43a16ed0aacce27e8d16cf5d0b5ca20a23bf53feef35c4ee5c7  A28_dim5/MOST.00020.nc
d2fe9d4dc85d1f7293233135025fde21b85aa0155d42da6bc6779764e863f7e4  A28_dim5/MOST.00021.nc
bb68cedc3361115194c9e10b3b3d70b98732201a3034314e5c015708bb4f8566  A28_dim5/MOST.00022.nc
e194008811152fcc78df74c55d5349cd1cc7f2e6489f1e631fa5a569a86ce4ce  A28_dim5/MOST.00023.nc
85bfd9e48d1600bfdfdd880d3763bc381d4109077038fe756eae471293c9473f  A28_dim5/MOST.00024.nc
bbeed3420f4a58f77d39cfb23cf9da90fc55bded3d1117fd48f740136915a480  A28_dim5_moon/MOST.00020.nc
b6f830c4c54ae2a7bec27f7e42511ff54433840fab03f7d3f37d80da23470b6a  A28_dim5_moon/MOST.00021.nc
0ae90b2451546663f33121c96470d4a9ccdfcac9f6f9d7a3e545c35c43fc1404  A28_dim5_moon/MOST.00022.nc
bf5af81306d22099ed49bcab4e7f1b757b64f929478af1af25a478cd64431426  A28_dim5_moon/MOST.00023.nc
c1f46da8ff09eb0f52e0de1f53b221220d48abe5594345157802b12cc33dae77  A28_dim5_moon/MOST.00024.nc
f53383a1c75d092575cdaf224ec60d2e617745857a6a8f9ca292725dab46559f  A28_dim5_moon/MOST.00025.nc
03cbe4834edc0ee5e40187eab7e375834877af686ae8559714eb97723749d99b  A28_dim5_moon/MOST.00026.nc
492ce573560b816e751e14a69ce7f2bcb24b883c6c2b1a1a35c2da6809aed974  A28_dim5_moon/MOST.00027.nc
fec03a0274b828d20509aec761f365439090ef3d4a769e9f396e59ea530fba56  A28_dim5_moon/MOST.00028.nc
31040636f8423f55650b499b14b5187c7273aa9f0b3d8f58cb9fb52c5149bec1  A28_dim5_moon/MOST.00029.nc
```

**What was read.** `AGENTS.md` in full; the five scope files whole; `introduction.tex`, `worlds.tex` and
`assumptions.tex` whole and the register paragraph of `availability.tex`; every entry of `claims.json`; the manifest
entries of the cited works; the repository notes named in the table at the lines the register cites (and the
defect log's summary table and entries A1, A2, B11); the Terluna passages at the lines cited below; the drive's
yearly summaries and twenty-two yearly output files of three GCM runs; the ExoPlaSim source lines named in
section 3.

**Source originals opened** (text extracted with `pdftotext -layout`; every hash matches the manifest):

| Original | sha256 |
|---|---|
| `yang2023cloud.pdf` (arXiv:2306.12186v1) | `0637811e9ae240d47ab39da7d905421709afb685df2d0050f6f8ffdfa2d8bc41` |
| `yang2023cloud_si.pdf` (publisher SI) | `1cc0a5828d0dc0301b1b2aa712c48f58d8c312a6470e6c1d11df47a806ac5554` |
| `braam2022lightning.pdf` (arXiv:2209.12502v1) | `26486cfc19cb2185ca8f98a22bcbadf40a526afed1f8b3d460154915b58cf8c7` |
| `sergeev2025lightning.pdf` (arXiv:2504.19883v2) | `b2c3352f4ad065bd894341eb76741ff541b1bf4c4824612ae7e6404bd373c6df` |
| `vincendon2010spherical.pdf` (arXiv:1103.3215v1) | `afcdf418a60ce367c8b16c12d68c1bac36ea2fd8e0013498ea3553c0cbd8a7e9` |
| `way2018climates.pdf` (arXiv:1808.06480v2) | `476e3e967e5d7eeafea1f386fc801851106365653bd3d9132c5821edb7164820` |
| `yang2014strong.pdf` (arXiv:1404.4992v1) | `3b2852341d6ea46d600ed11e061f45092bb72b893c756f605505fdd1f0e38f5c` |
| `lunkeit2012plasim.pdf` (PlaSim manual v16) | `11d1465ed9a88b7b6e01a17b134fedcc634ca28ac21f5e3b5014473f52045bf5` |

**The reviewer's own calculations.** Two short read-only scripts (netCDF4 in Terluna's GCM environment) averaged
the yearly output of `A28_dim5` (years 15–24), `A28_dim5_sun_test` (years 0–1) and `A28_dim5_moon` (years 20–29):
zonal annual means of total cloud cover (`clt`), the clouds' effect in sunlight (`rst − rstcs`) and arriving
sunlight (`rst − rsut`, `rsut` being negative upward), with cos-latitude weights; and the area-weighted share of land
cells (`lsm`) whose annual-mean rain (`pr`) falls under 0.5 mm/day. These are calculations from model output, a
reviewer's check outside the claims register; their numbers appear in findings 3 and 8 and in section 3.

## 2. Findings

Severity: BLOCKING (a factual error, a wrong evidence state or an implied reach beyond the evidence); MAJOR (a
dropped condition or overstated scope); MINOR (precision). Locations are file:line at e89a394.

### 1. BLOCKING — conclusions.tex:74–76

> "For any new world, the geometry and the gas absorption can be computed from the world's own column, and cloud
> remains the part to be calibrated for that world, against cloud-resolving runs whose microphysics laboratories
> and similarity runs can test."

The paper's closing sentence extends the method to "any new world", in a state of present capability. The body
reaches less far on each count.

- Reach: `reach.tex`:74–77 places Titan, present Mars and Venus outside what PlaSim's and RRTMG's radiation and
  Morrison's water-only microphysics represent, "while their radiation, condensation and clouds would have to be
  built" (W05); `reach.tex`:77–82 bounds the adapted models by four limits (nitrogen–oxygen–argon–water air with
  modest CO₂; pressures within RRTMG's tables; scale heights up to a few hundredths of the radius; empirical laws
  near their Earth conditions).
- Gas absorption: in the GCM it is fitted, a calibration to the reference model near the fitted columns
  (`introduction.tex`:79–80; `reach.tex`:9–14, W01); the scheme that would compute it from a column is a proposal
  (`next.tex`:13–16; this section's own L34–36, "would replace"). The reference itself covers HITRAN lines,
  MT_CKD 4.3, collision-induced absorption and Rayleigh scattering for the design air (R08), and its CO₂, O₂,
  collision-induced and solar calculation awaits an independent code on the lunar column (`next.tex`:27–33; V16).
- Geometry: the computed table is the radiative geometry, from one clear design column (R05; limits in
  `notes/exoplasim.md`:164–168); the dynamics keep a thin shell and constant gravity (`next.tex`:49–56;
  `reach.tex`:79–81).

**Proposed correction.** "For a world inside those four limits, the curved-air table is computed from that world's
own column and the gas fits are refitted to the reference model on it, until a scheme built from the reference's
spectroscopy takes their place; cloud remains the part to be calibrated for that world, against cloud-resolving
runs whose microphysics laboratories and similarity runs can test. Titan, present Mars and Venus lie outside those
limits, and their radiation, condensation and clouds would have to be built first."

The abstract's last clause, "with physics that holds across worlds" (`abstract.tex`:19–21, outside this review's
scope), makes the same reach and would follow the corrected landing.

### 2. MAJOR — conclusions.tex:8–9

> "and by the code's own arithmetic they bias ExoPlaSim's runs of natural planets:"

The general clause drops the conditions on which each defect acts, and so covers runs the arithmetic leaves
unbiased (a one-day rotation with no configured tilt). `reach.tex`:16–17 states the scope: "they bias any run that
meets their conditions"; the Sun clock acts in non-synchronous runs on the default solar geometry whose rotation
differs from one day, the cover unit wherever the model day differs from one Earth day, the orbit default wherever a
tilt or eccentricity is set without the fixed orbit (`reach.tex`:17–24; H23, H07, W06; `notes/exoplasim.md`:51–65).

**Proposed correction.** "and by the code's own arithmetic they bias ExoPlaSim's runs of natural planets whose
rotation or model day differs from one Earth day, or that set a tilt or an eccentricity without fixing the orbit:"

### 3. MAJOR — conclusions.tex:18–20

> "The moved sunlight changed the clouds, and through them the global means: in a two-year test of the Sun and tilt
> alone, the clouds' effect in sunlight weakened by 2.4~W\,m$^{-2}$, the test world ran 0.9~K warmer while still
> gaining heat, and the share of land under half a millimetre of rain a day rose from 9 to 36\%."

The third item joins the dry-land share to the chain "through them [the clouds]". The record gives that change
another cause: "With only the Sun and tilt corrected (`A28_dim5_sun_test`, two years), the high latitudes already
dry out and 36% of the land gets under 0.5 mm/day: Earth's seasons had carried summer rain to 60°" (Terluna
`climate/gcm/README.md`:661–664; `defect_log.md` A2; G02). The numbers hold: from the output, land under 0.5 mm/day
covers 8.5% (`A28_dim5`, years 15–24), 36.2% (`A28_dim5_sun_test`) and 42.2% (`A28_dim5_moon`, years 20–29), area
weighted. The first two items hold as a cloud pathway (section 3).

**Proposed correction.** "The moved sunlight changed the clouds, and through them the global means: in a two-year
test of the Sun and tilt alone, the clouds' effect in sunlight weakened by 2.4~W\,m$^{-2}$ and the test world ran
0.9~K warmer while still gaining heat. The same test ended the summer rain that Earth's tilt had carried to
60\textdegree, and the share of land under half a millimetre of rain a day rose from 9 to 36\%."

### 4. MAJOR — conclusions.tex:27–29 and abstract.tex:17–18

> conclusions: "calibrating the radiation's Earth fits moved it by at least 20~K"
> abstract: "while calibrating the radiation's Earth fits moved it by at least 20~K"

The 20 K belongs to the first calibration alone, the Rayleigh multiplier and the weaker water continuum, on the
first design runs (25% seas, undimmed shield, PlaSim's Sun clock and Earth's orbit): `results.tex`:36–39 ("Fitting
the first calibration cooled the climate more than any later change"), G14, and `paper/data/repairs.json` row 1,
labelled "First calibration of the radiation", −19.999 K, "the uncalibrated run still warming in year 12, so the
change is at least this large". The later calibrations of the same fits moved the climate by other amounts and in
both directions: the gas bands −2.2 K (G03), the longwave correction with ice optics +11.5 K (G05). As written, both
sentences give 20 K to calibrating the radiation's fits as a class.

**Proposed correction.** Conclusions: "the first calibration of the radiation's Earth fits, its Rayleigh multiplier
and water continuum, moved the first design runs by at least 20~K". Abstract: "while the first calibration of the
radiation's Earth fits moved it by at least 20~K".

### 5. MAJOR — conclusions.tex:37–38

> "Cloud amount stays a calibration for each world, fitted to cloud-resolving runs of that world, and those runs
> compute with Earth-fitted microphysics of their own."

The sentence follows "as the curved-air table was for the test world" (L31) in the same paragraph and states the
cloud fit in the same present tense, so a reader takes the test world's cloud amount as fitted to CM1. The body
gives a proposed step: "PlaSim's cloud amount and cloud water move the test world by several kelvin and remain
uncalibrated for it" (`next.tex`:18–24); the inventory lists the cloud thresholds and Slingo's fit as open
(`assumptions.tex`:172–173). The evidence state, design intent and a step still to run, is left unmarked.

**Proposed correction.** "Cloud amount stays a calibration for each world, to be fitted to cloud-resolving runs of
that world; for the test world that fit is a step still to run, and its cloud keeps PlaSim's Earth-tuned settings
until then. Those runs compute with Earth-fitted microphysics of their own."

### 6. MAJOR — conclusions.tex:46–48

> "The flash-rate laws used for tidally locked planets were fitted to Earth's storms and set the flash rate from the
> cloud-top height or from the graupel and ice aloft \autocite{braam2022lightning,sergeev2025lightning}."

The definite plural characterises the field's practice from two studies. What the two did checks out: Braam et
al. used the oceanic cloud-top-height law LFR = 2.0×10⁻⁵ H^4.38, whose coefficients "have been tuned to match
observed" Earth flash rates (arXiv v1, Sect. 2.4 and 4.3); Sergeev et al. used McCaul et al.'s law from the upward
graupel flux at −15 °C and the total ice water path, with coefficients "determined empirically from observations"
of storms over the United States, beside Price and Rind's cloud-top law in coarse runs (arXiv v2, Sect. 2.2,
Table 1). `results.tex`:150–153 scopes the same statement better.

**Proposed correction.** "The flash-rate laws that \textcite{braam2022lightning} and \textcite{sergeev2025lightning}
used for tidally locked planets were fitted to Earth's storms and set the flash rate from the cloud-top height or,
in Sergeev et al.'s storm-resolving runs, from the graupel and ice aloft."

### 7. MAJOR — conclusions.tex:65–66

> "By one design's own models, a shield in space that removes the ultraviolet heating the upper air would keep
> Earth-like air on the Moon for tens of billions of years,"

S15 records a time-scale: "the air loses 0.61–1.4 kg/s over a solar cycle without magnets; at those rates the
1.2 atm atmosphere (2.84e18 kg) would take 64–148 billion years to remove" (Terluna `research/decisions.md`:125;
`regime_calc.json` `retention`). The sentence turns the ratio of mass to a present solar cycle's loss rate into a
duration of tens of billions of years, past the Sun's remaining main-sequence life, and drops the condition "at
those rates". `introduction.tex`:23–25 keeps the condition ("losses that would take 60 to 150 billion years to
remove it").

**Proposed correction.** "By one design's own models, a shield in space that removes the ultraviolet heating the
upper air would hold the Moon's Earth-like air to losses of 0.6--1.4~kg\,s$^{-1}$ over a solar cycle, rates at
which removing it would take 60 to 150 billion years, on a body whose escape velocity let its natural atmosphere
go,"

### 8. MINOR — conclusions.tex:22–25

> "Models can agree in their global means and still disagree widely in where cloud lies: on two tidally locked
> planets, the quasi-global cloud-permitting runs of \textcite{yang2023cloud} covered 27 and 41\% of the sky with
> cloud and two GCMs ... covered 82--97\%, while the three models' global-mean surface temperatures and albedos came
> out broadly alike."

Three points of precision. (a) The evidence after the colon is cloud amount, itself a global mean that differs by a
factor of 2 to 3.5; Yang et al. place "the largest difference ... at the nightside and at the high latitudes of the
dayside" (arXiv v1, pp. 3–4), which carries the "where". (b) The agreement is broad: global-mean surface
temperatures 243, 240, 243 K and 263, 253, 268 K (SI, Text on Fig. S8), planetary albedos 18, 29, 22% and 37, 47,
39% (main text p. 3), which the authors call "broadly similar" (Discussion, p. 7). (c) The 4 km runs held their sea
surfaces at the temperatures of 40 km spin-ups (Methods, p. 10). The sentence's numbers (26.9, 41.1; 81.7–97.4%)
and the cover's dependence on "relative humidity, atmospheric stratification, and large-scale updrafts" (p. 4)
match the source.

**Proposed correction.** "Models can agree broadly in global-mean temperature and albedo and still differ widely in
how much cloud they form and where: on two tidally locked planets, the quasi-global cloud-permitting runs of
\textcite{yang2023cloud}, over sea surfaces held at the temperatures of coarser runs, covered 27 and 41\% of the sky
with cloud and two GCMs whose cover follows relative humidity, stability and large-scale ascent covered 82--97\%,
most of the difference on the night side and at high latitudes of the day side, while the three models' global-mean
surface temperatures and albedos came out broadly alike."

### 9. MINOR — results.tex:82–86

> "GCM cloud schemes of this kind, which set the cover from relative humidity, stability and large-scale ascent,
> differ widely from cloud-permitting runs on tidally locked planets as well:"

"Of this kind" takes in PlaSim's scheme, which the clause then describes with CAM3's inputs. PlaSim sets stratiform
cover from relative humidity, convective cover from convective rain and anvil cirrus from the convective cover, with
an optional vertical-velocity factor on low cloud that is off by default and no stability term (PlaSim manual v16,
Sect. 3.4.6, eqs. 3.96–3.98; `notes/exoplasim.md`:271). "As well" implies a wide cloud difference between PlaSim and
CM1 on the test world; the body reports none. Terluna's record holds one (the box at 0° E, 14% daytime cloud against
the corrected GCM's 39%; Terluna `climate/crm/README.md`:868–872), which the text could cite through a new register
entry. Point (c) of finding 8 applies here too.

**Proposed correction.** "Diagnostic GCM cloud schemes of this family, PlaSim's setting the cover from relative
humidity and convective rain and CAM3's and ExoCAM's from relative humidity, stability and large-scale ascent,
differ widely from cloud-permitting runs on tidally locked planets: ...", with "as well" kept only if the test
world's own comparison enters the body and the register.

### 10. MINOR — conclusions.tex:30–34

> "The geometry of tall air is computed from the world's own column, as the curved-air table was for the test world,
> ...; Titan's haze, with a scale height of about 80~km, stands a few hundredths of the radius tall, as the test
> world's air does, and plane-parallel aerosol codes for Titan's surface hold to about 65\textdegree\ from the
> zenith"

Under "what a modeller of a new world would need" (L29–30), the sentence gives the radiative geometry only; the
dynamics keep the thin shell and constant gravity (`next.tex`:49–56; `reach.tex`:79–81). Set beside the method, the
Titan example reads as a world the method serves, while Titan's radiation lies outside the adapted models
(`reach.tex`:74–77). The Titan numbers themselves check out (section 3).

**Proposed correction.** "The radiative geometry of tall air is computed from the world's own column, as the
curved-air table was for the test world, ...; the dynamics keep a thin shell and constant gravity, which the
adapted models hold to scale heights of a few hundredths of the radius. Titan's haze, with a scale height of about
80~km, stands a few hundredths of the radius tall, as the test world's air does, and plane-parallel aerosol codes
for Titan's surface hold to about 65\textdegree\ from the zenith \autocite{vincendon2010spherical}; Titan's
radiation itself lies outside what the adapted models represent."

### 11. MINOR — conclusions.tex:31–32

> "whose air in curved shells loses a net 5.8~W\,m$^{-2}$ against the same clear column taken flat"

The comparison column is flat with a pseudo-spherical direct beam for the sunlight (H11; `assumptions.tex`:43–46,
"with a pseudo-spherical direct beam for the sunlight"). The condition drops here.

**Proposed correction.** "loses a net 5.8~W\,m$^{-2}$ against the same clear column taken flat with a
pseudo-spherical direct beam"

### 12. MINOR — conclusions.tex:51–52

> "electrified storms resolved at other gravities, computed with the same laboratory charging laws, could test those
> flash-rate laws, a route \textcite{sergeev2025lightning} also propose."

Sergeev et al. write: "A possible route towards a more quantitative result is to use an explicit electric charging
scheme coupled with a cloud-resolving model ... this may be the best way of tuning convection- or
microphysics-based parameterisations in climate models for different planetary atmospheres" (arXiv v2, Sect. 4.2).
The gravity and the shared laboratory laws are this paper's specification of that route.

**Proposed correction.** "... could test those flash-rate laws, as \textcite{sergeev2025lightning} propose explicit
charging in cloud-resolving runs for tuning such laws to other planetary atmospheres."

### 13. MINOR — conclusions.tex:55–58

> "so in a sea under another gravity, the ancient seas of Mars among them, SWAN's gravity follows that scaling, as
> tested at a sixth of Earth's gravity on the code paths those tests ran,"

The present tense states a property at Mars's 0.38 g, where no run was made; the evidence is one sixfold test (V04:
0.303% against 5.44%) and the patch's construction, a knee at f g_E/g (R04). The clause "as tested at a sixth"
names the test; the inference to other gravities needs its own state.

**Proposed correction.** "so the patched code, whose knee scales with gravity, would carry that scaling to a sea
under another gravity, the ancient seas of Mars among them, on the code paths those tests ran; the scaling has been
tested at a sixth of Earth's gravity alone, and what stays uncertain is ..."

### 14. MINOR — conclusions.tex:61–62

> "85\% of the water falling from the clouds of a box forced from the Earth-orbit state evaporated before it reached
> the ground, against 57--73\% in the rings"

The box's forcing is named and the rings' is absent. N03's source gives "the rings lose 57–73%" without naming them
(Terluna `climate/crm/README.md`:939–940), and `next.tex`:70 repeats it bare. The rings run in two dimensions and,
where they are the flat rings set up from the corrected run (`README.md`:957–958), under other forcing, so "against"
sets cases of different geometry, and perhaps of different forcing, side by side.

**Proposed correction.** Name the rings and their forcing in N03 and in the sentence ("against 57--73\% in the
rings forced from the [state]"), or keep the box's 85\% alone.

### 15. MINOR — conclusions.tex:71–73 and next.tex:35–38

> conclusions: "Released and repaired ExoPlaSim on Earth-air planets rotating once in 16 and 64 days, two of the
> sidereal periods at which \textcite{way2018climates} ran ROCKE-3D, with the released radiation, would measure ..."

The proposed test leaves the insolation open. Way et al. completed the 16-day rotation from 1.0 to 1.4 times
Earth's insolation and the 64-day rotation from 1.0 to 2.9 times (arXiv v2, Tables 2–3), and the paper places the
warmer runs "beyond the radiation's fits" (`reach.tex`:53–55); the released radiation holds near Earth's warmth
(`reach.tex`:40–41).

**Proposed correction.** "Released and repaired ExoPlaSim on Earth-air planets at Earth's insolation, rotating once
in 16 and 64 days, ..." (and in `next.tex`:36, "at Earth's insolation, where the released radiation holds, rotating
once in 16 and 64 days").

### 16. MINOR — reach.tex:42–43

> "and every run of those models away from Earth's values is of the test world."

SWASH's linear-wave control ran "at lunar, fourfold lunar and Earth gravity" (Terluna `climate/waves/runup.md`:200–204;
V05), a gravity of neither Earth nor the test world. It is a numerical control on unmodified SWASH; the universal
reads past it. The table caption at `reach.tex`:86–87 carries the same wording.

**Proposed correction.** "and every run of a world by those models away from Earth's values is of the test world."

### 17. MINOR — abstract.tex:16–17

> "On the test world single general repairs moved the global-mean surface temperature by 1.6--2.5~K,"

Two general repairs were measured singly, cloud water by pressure and the cover per Earth day (G01); the Sun clock
ran with the fixed orbit and the ice optics with the longwave correction. The conclusion's L29 has the exact form:
"the two general repairs measured alone".

**Proposed correction.** "On the test world the two general repairs measured singly moved the global-mean surface
temperature by 1.6--2.5~K,"

## 3. Checked and sound

- **Forms, defects and repair classes** (conclusions:3–6): four forms and five defects in four codes; "largely"
  covers the bound, settings, avoidances, the ice optics (general) and RRTMG's ice (mitigation) in the inventory
  (`assumptions.tex`:141–209; `introduction.tex`:70–84).
- **Three defects small at Earth's values** (conclusions:7–8): skip 1/(N−1) of a turn, none at a one-day rotation,
  about 1° near Earth's, 10° at 10 days, 16° at 12–20 days, 33° beyond; cover bias 0.125 ln(day); the orbit default
  moves Earth's tilt by a fraction of a degree (`assumptions.tex`:98–118; H23, H07, H24).
- **+0.23 for TRAPPIST-1e** (conclusions:9–10): W06; `regime_calc.json` gives N 60, model day 6.203 d, bias 0.228.
  The deployed ExoPlaSim 3.4.2 confirms the code path: `__init__.py`:2616–2619 sets `ROTSPD` and
  `N_DAYS_PER_YEAR = max(int(360/P/12+0.5),1)*12` for any rotation, `:2628–2630` sets only `NFIXED` and `FIXEDLON`
  for a synchronous run, `plasim.f90`:1292–1300 sets `solar_day = sidereal_day*N/(N-1)`, and `rainmod.f90`:1899
  converts rain with `zrfac = solar_day * 1000`. Yang et al. give TRAPPIST-1e's rotation as 6.1 days (p. 3).
- **About 33° for rotations slower than 20 days** (conclusions:10–11): `regime_calc.json`
  `exoplasim_slow_rotators` (20 d: N 24, 15.65°; 21 d: N 12, 32.73°).
- **The zonal-mean inference** (conclusions:14–16): for insolation S(a/r)² max(0, cos z) summed around a latitude
  circle at one instant, the hour angle runs over every value, so the sum depends on the latitude, the declination
  and the distance alone. `solang` errs in the hour angle only (`notes/exoplasim.md`:25–31; Terluna
  `climate/gcm/README.md`:182–187, "Each row of latitude still gets its right mean"). In `sun_check_A28_dim5.json`
  the rows follow the orbit the log reports within 1.83 W/m² rms, and the equator row runs 0.9171–1.1737 of its
  mean (8.3% short, 17.4% over).
- **Global mean kept** (conclusions:13): the arriving sunlight's global mean is 293.55 W/m² in the Earth-orbit state
  (years 15–24, both faults; `sun_check_A28_dim5.json`) and 293.29 W/m² in the two-year test (both repaired; the
  reviewer's calculation), within 0.1%. The orbit default also replaced the eccentricity (0.016715 by 0.0175;
  `notes/exoplasim.md`:57), which moves the annual mean by about a part in 10⁵.
- **Claim G17** (results:48–52; conclusions:18–19): the drive's yearly summaries give, for `A28_dim5_sun_test`
  years 0–1, surface 295.195 K, top of the air +1.86 W/m², albedo 0.2851, clouds' effect in sunlight −13.32 W/m²,
  rain 2.739 mm/day, and for `A28_dim5` years 15–24, 294.311 K, −0.485 W/m², 0.2931, −15.698 W/m², 2.913 mm/day.
  The albedo's fall of 0.0080 over 293.4 W/m² of mean sunlight is 2.35 W/m², equal to the cloud term's 2.38 and to
  the change at the top of the air, +2.35 W/m², so the clear sky's share stayed near zero and the extra sunlight
  entered through the clouds. The baseline was still cooling (294.61 K in year 15, 294.14 K in year 24, the branch
  year), so the +0.9 K against the window mean is the smaller of the two measures (+1.06 K against year 24).
- **"Changed the clouds"** (conclusions:18): the reviewer's zonal means show the global cover nearly unchanged
  (0.2492 to 0.2476) and redistributed: within 30° of the equator, cover 0.317 to 0.349 and the clouds' effect in
  sunlight −21.97 to −23.46 W/m²; at 50–70°, cover 0.151 to 0.106 and the effect −7.23 to −0.68 W/m² under sunlight
  falling only from 207 to 188 W/m². The test's sunlight with the baseline's cloud reflectivity row by row gives
  −15.96 W/m², and the baseline's sunlight with the test's gives −12.87, so the clouds' own change carries the
  2.4 W/m², and the sunlight's move with unchanged clouds would have strengthened the effect slightly.
- **Seasons and rain at 60°** (conclusions:17): H24; G02; Terluna `climate/gcm/README.md`:201–212, 661–664.
- **Yang et al.'s numbers and scheme description** (conclusions:22–25; results:84–86): 26.9 and 41.1%; 94.8 and
  81.7% (CAM3); 90.4 and 97.4% (ExoCAM); "relative humidity, atmospheric stratification, and large-scale updrafts";
  "broadly similar" (arXiv v1, pp. 3–4, 7).
- **6 K and 1.6–2.5 K** (conclusions:28–29): G05 (−4.98 K, about −5.9 K settled); G01 (2.30 and about 2.5 K;
  1.76 and about 1.6 K); `repairs.json`.
- **Titan** (conclusions:32–34): Vincendon and Langevin infer an aerosol scale height of 80 ± 10 km (abstract;
  Sect. 3, Titan) on a model radius of 2,575 km (Sect. 3.2), 0.031 of the radius against the test world's 52.4 over
  1,737.4 km, 0.030 (`regime_calc.json` `scale_height`); plane-parallel codes for surface–atmosphere separation are
  "relevant when the solar zenith angle is small enough ... (typically less than 80° for Mars and 65° for Titan,
  which has a larger relative scale height)" (Sect. 1). `worlds.tex`:77–78 keeps Titan's gas at 0.8% of its radius,
  consistent with the haze's larger scale height.
- **Line-by-line scheme** (conclusions:34–37): a conditional design ("would replace"), scoped to the gases,
  pressures and temperatures the spectroscopy covers; `next.tex`:13–16; R08 (correlated-k within 0.4–1.4 W/m²).
- **Electrification** (conclusions:41–46): G11 and N01 against Terluna `climate/crm/README.md`:2097–2120 (as much
  charge within the realizations' spread; at 0.03–0.17 g/m³ Takahashi's table gives rimed ice positive charge at
  every temperature) and 2142–2170 (the deciding measurement in those words; hail strikes at 4.4–7.6 m/s, "within
  the 1.2–11 m/s Earth's laboratories have measured").
- **Freezing levels and flash density** (conclusions:48–51): G09 (Terluna `climate/crm/README.md`:1454–1455);
  G10 (`regime_calc.json` `flash_density`, 0.022 against 2.72 per km² per year, ratio 0.0081;
  `notes/electrification.md`:74–76, 97–99).
- **SWAN and the CM1 pair** (conclusions:55–59; abstract:15–16): V04 (Terluna
  `climate/waves/first_experiments.md`:33–37: 0.303% and 0.326% against 5.44% and 3.91%); V06 (Terluna
  `climate/crm/README.md`:2508–2528).
- **Drop size and evaporation** (conclusions:60–62): H21 (`regime_calc.json` 2.457); G08 (Terluna
  `climate/crm/README.md`:936–940, 969–975: 85% lunar, 64% at Earth's fall speeds).
- **The design's losses and the Moon's day** (conclusions:65–68): S15 (Terluna `research/decisions.md`:125;
  `regime_calc.json` `retention`, 64–148 billion years); S01 (29.53 days).
- **Calibrations for the designers; runs on the test world alone** (conclusions:69–71; next.tex:35): `reach.tex`:62–64;
  `introduction.tex`:83–84; the SWASH control of finding 16 is a numerical control on an unmodified code.
- **Way et al.** (conclusions:71–72; next.tex:36–37; reach.tex:49–55): sidereal periods X001 to X256, X016 and X064
  among them, "in multiples of Earth length sidereal days" (Tables 2–3); zero obliquity and eccentricity; 1 bar
  N₂-dominated with 400 ppmv CO₂ and 1 ppmv CH₄ (abstract); highest completed insolation S0X 2.9 at X064 (Tables
  2–3); cloud among the climate's routes with rotation (abstract).
- **Yang et al. 2014** (reach.tex:50–54): CAM3 at Earth's radius and gravity, 1 bar mainly N₂ with 400 ppmv CO₂,
  the Sun's spectrum among others, flux raised until the model crashed near 310 K, and cloud albedo the main reason
  slow rotators run cooler (Sect. 2–3).
- **Natural worlds in Figure regimes** (reach.tex:41–42): `worlds.json` holds four found worlds, Earth, present
  Mars, Titan and Venus, with columns 1, 0.016, 10.5 and 100 times Earth's; Earth alone lies near both fitted lines.
- **The split and the calendar** (reach.tex:46–48, 55–58): V07 (Terluna `climate/gcm/README.md`:293–298, 0.7 points
  short on the 303 K, 338 kg/m² column with the 1.356 multiplier fitted before the gas bands); W03
  (`regime_calc.json`: 64 d, 69.82 against 77.60 d; 243 d, 265.1 against 726.0 d).
- **Constructed worlds in the abstract** (abstract:4–6): S15 in the conditional state "by one design's own models";
  `introduction.tex`:15–26.

**Outside this review's scope, uncounted.** `abstract.tex`:19–21 ("with physics that holds across worlds") makes
finding 1's reach. `results.tex`:93 has "more than 20~K" where the abstract and conclusion have "at least 20~K" for
the same −19.999 K extract. `worlds.tex`:24 labels the illustrative slow rotators by solar days of 16, 64 and 243
days, while the proposed test and W03 use sidereal rotations of those lengths (solar days 16.7, 77.6 and 726 days).

## 4. Counts

| Severity | Count | Findings |
|---|---|---|
| BLOCKING | 1 | 1 |
| MAJOR | 6 | 2, 3, 4, 5, 6, 7 |
| MINOR | 10 | 8–17 |
| Total | 17 | |
