# Evidence review: "Discussion and conclusions" and reach's "Worlds that need the repairs as they stand"

Editorial round 2, technical evidence check of one revised section.

## 1. Record

- **Reviewer:** a fresh Claude subagent (Claude Opus 5.5). It saw no earlier review and opened nothing under
  `paper/review/` (apart from writing this file) or `paper/notes/`.
- **Date:** 2026-10-17.
- **Snapshot:** commit `bb5d0f0`, HEAD with a clean working tree when read; every repository file was read with
  `git show bb5d0f0:<path>`. Terluna files were read with `git -C ../terluna show 186b294:<path>`.
- **Scope:** `paper/sections/conclusions.tex`, the whole section, and `paper/sections/reach.tex` lines 47–56, the
  run-in heading "Worlds that need the repairs as they stand." with its paragraph.

### Hashes (sha256)

Files in scope, at `bb5d0f0`:

| File | sha256 |
|---|---|
| `paper/sections/conclusions.tex` | `a191f07ede146003ce1664863ad9c81dd824436e95610ec8531764e880f5a32d` |
| `paper/sections/reach.tex` | `483668bcbfa5c3800e198a211fe8bde23a049621a433b076707731f39277f6d2` |

Evidence relied on, this repository at `bb5d0f0`:

| File | sha256 |
|---|---|
| `AGENTS.md` | `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32` |
| `paper/sections/abstract.tex` | `77110b76b51fe6344a42ce39269f79f40f0ce13b84b45a34d379bc108d05fcb7` |
| `paper/sections/introduction.tex` | `b8325d641b56d6da32cffbcaa143e26461495322235c2de3b0709402f1ef5b72` |
| `paper/sections/worlds.tex` | `453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112` |
| `paper/sections/assumptions.tex` | `01d5eea0744342fba7ef3eea7d274976cc88744f5d97e4a3ca16b2e1751fb50e` |
| `paper/sections/repairs.tex` | `bb1d22c01616fdaf454280acded56316b7995af2a8fc3bb5a255af52c92e793c` |
| `paper/sections/verification.tex` | `4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00` |
| `paper/sections/results.tex` | `84222578242a78e05394215ed333b71fd81633a5d6e99eeeb6556e603039fa71` |
| `paper/sections/next.tex` | `c0efe8d232f6d8c592829d5b9d3a553555e6be460ba652f87447e0e04d15d3b7` |
| `paper/sections/appendix.tex` | `20cc69d4ef20554c2667c37f8654dcc3814b43a662ace234c709741581bc5004` |
| `paper/sections/availability.tex` | `496434ae301b500a3f7dcec2750af08b8a4d1789c437844ab1318e3ff35f762d` |
| `paper/claims.json` | `021ed1ee11dd98bf461cb39db030adb0d101d1cc39352f0acc8779d9700dbbd9` |
| `paper/references.bib` | `c0c9662b362141759bce9a27bb566e7ee6a00479ef773273f1dc109d7888747e` |
| `paper/sources/manifest.json` | `334f5973fe6339026237ca7953369c34e5f4a1cce89ef935bccd7ccfa76a66a4` |
| `paper/data/regime_calc.json` | `7a2935a8fbe6086c577097b838825c5415ba99f0adf040af62f5e4bcd370e7d1` |
| `paper/data/worlds.json` | `70dabbec07bf13ab1b31d1e60904d33eac44d0928f9ab50b965937eb3f7916f0` |
| `python/climate/results/gcm/sun_check_A28_dim5.json` | `5b922f8d7afede955e791a78c0b3204988a1515f84bca1e670c1880df9162966` |
| `python/climate/results/gcm/sun_check_A28_dim5_sun_test.json` | `b690e29206ec2e7393757969e9634ceffff42d051d220036581654ff08739186` |
| `python/climate/results/gcm/sun_check_A28_dim5_moon.json` | `4c2ae9ceee741c6afc25cb896051ee66d69c7f1adf7e036c8a7efa29cfe8f50a` |
| `notes/exoplasim.md` | `707d97ef683d2650db8044cfee18f3a3ac7c82675dc37f4222476a6a4c978bf2` |
| `models/exoplasim/README.md` | `7af8415bebd7733da42bb34c1f47bb9f5411408a243523cae5524be4b17c7149` |
| `models/cm1/README.md` | `8ad11dfabe6b2c74445e21fe1f9b0eab52101cc64d1f749bdebbe8e3d933bc5d` |
| `models/swan/README.md` | `3699e5e564fa484d36b1aa6c91434ab8119beeb3a50de8f72625db97476f8d3f` |
| `models/swash/README.md` | `99927157542500556d4e267bcb59ebfbd7b5572057ead6019284d4ea1af4532c` |

Terluna at `186b294` (sha256 of the `git show` output):

| File | sha256 |
|---|---|
| `climate/gcm/README.md` | `267413c2aa248c3b7581d796ef83de826fbe6764d6d03c9abd1677fee03150fb` |
| `climate/crm/README.md` | `95776d41c55b3a3a372d3752ff367b66c45f3a98a1609b2cddfd953f49754acd` |

Research drive, read-only (`/media/projectspace/terluna-research/`):

| File | sha256 |
|---|---|
| `gcm-runs/A28_dim5/progress.json` | `619f3de9adeafa38803e60fc4b311278f9c3bf9f681adcc1f69c05b9b16d8e61` |
| `gcm-runs/A28_dim5_sun_test/progress.json` | `0d8563dbbe8c815b92c88b29943c7a068e9d4b9fd743738a9da38ba08df7b816` |
| `gcm-runs/A28_dim5_moon/progress.json` | `d287252f152cb52f5b9f07f35f1e51fca87bddab6226fd960a1c35bdfc31be6d` |
| `gcm-runs/A28_corrected_9655/progress.json` | `bd602b5a6e723c7ebb34d51ef73945447f9351895391c99b30b2ca2c593f7e04` |
| `gcm-runs/A28_corrected_9685/progress.json` | `67e68988af133c3accc41a2c8b678b3af64c1c17a09d9630b4e3c0cea1f3f2fb` |

Source originals (`paper/sources/originals/`, git-ignored). Each hash matches its manifest record:

| File | sha256 |
|---|---|
| `yang2023cloud.pdf` (arXiv 2306.12186v1; carries the Supplementary Information text) | `0637811e9ae240d47ab39da7d905421709afb685df2d0050f6f8ffdfa2d8bc41` |
| `yang2023cloud_si.pdf` (hashed and extracted; its text was left unread, since the arXiv file carries it) | `1cc0a5828d0dc0301b1b2aa712c48f58d8c312a6470e6c1d11df47a806ac5554` |
| `braam2022lightning.pdf` (arXiv 2209.12502v1) | `26486cfc19cb2185ca8f98a22bcbadf40a526afed1f8b3d460154915b58cf8c7` |
| `sergeev2025lightning.pdf` (arXiv 2504.19883v2) | `b2c3352f4ad065bd894341eb76741ff541b1bf4c4824612ae7e6404bd373c6df` |
| `vincendon2010spherical.pdf` (arXiv 1103.3215v1) | `afcdf418a60ce367c8b16c12d68c1bac36ea2fd8e0013498ea3553c0cbd8a7e9` |
| `way2018climates.pdf` (arXiv 1808.06480v2) | `476e3e967e5d7eeafea1f386fc801851106365653bd3d9132c5821edb7164820` |
| `yang2014strong.pdf` (arXiv 1404.4992v1) | `3b2852341d6ea46d600ed11e061f45092bb72b893c756f605505fdd1f0e38f5c` |

### What was read

- **In full:** `AGENTS.md`; every section of the paper at `bb5d0f0` (abstract, introduction, worlds, assumptions,
  repairs, verification, results, reach, next, conclusions, appendix, availability), with all tables and captions;
  all 107 entries of `paper/claims.json`.
- **In part:** the six bibliography entries and six manifest records of the cited works; eight entries of
  `paper/data/regime_calc.json` (`sun_clock_skip`, `exoplasim_slow_rotators`, `exoplasim_synchronous_cover_bias`,
  `slingo_cover_bias`, `capillary_length_ratio`, `flash_density`, `retention`, `one_day_after_sunset`); every
  row of `paper/data/worlds.json`; the `along_row` and `by_latitude` blocks of the three sun-check files;
  `notes/exoplasim.md` lines 1–140 and 175–270; the patch tables of the four model READMEs; Terluna's
  `climate/gcm/README.md` lines 134–146, 160–322 and 600–690; Terluna's `climate/crm/README.md` lines 930–1000,
  1140–1200, 1436–1470, 1895–1940, 2090–2175 and 2360–2420, with a search for cloud tops; the yearly summaries in
  the drive's `progress.json` for `A28_dim5`, `A28_dim5_sun_test`, `A28_dim5_moon`, `A28_corrected_970`,
  `A28_corrected_9655`, `A28_corrected_9685`, `A28_dim3` and `A28_dim8`, and the configurations of the two
  `A28_corrected_96xx` runs.
- **Source originals opened** (text extracted with `pdftotext`): Yang et al. 2023 (abstract, introduction,
  results to p. 7, discussion, methods on the domain, Supplementary Text 3 on cloud fraction); Braam et al. 2022
  (abstract, Sects. 1, 2.1, 2.4 and 3.2); Sergeev et al. 2025 (abstract, Sects. 1–3.1 and 4); Vincendon and
  Langevin 2010 (abstract, Sect. 1, and every passage on scale heights and zenith angles); Way et al. 2018
  (abstract, Sects. 1, 2.1 and 3.1, Tables 2 and 3); Yang et al. 2014 (abstract, Sects. 1–3, Figs. 1–3 captions).
- **Unperformed:** no build, lint, test or model run; `paper/review/` and `paper/notes/` unopened.

## 2. Findings

Locations are `file:line` at `bb5d0f0`. Corrections are written in the paper's voice and keep its claim
markers out of the conclusion, as `availability.tex:28–29` describes.

### Finding 1 — BLOCKING — `conclusions.tex:11–20`

**Text.** "Several of these errors leave the global means nearly intact and change where sunlight and rain
fall. [...] while the step in which both were corrected, with a refit of the split of sunlight, moved the global
mean by 0.6~K. A check of the global energy balance passes with such errors in place; they show in a map of
sunlight by longitude or of rain by season."

**Evidence.**
- The body's only global-mean figure for the Sun clock and the orbit default is the joint step from the
  Earth-orbit state: +0.6 K, with the global rain cut from 2.91 to 2.24 mm a day, a 23% fall
  (`results.tex:44–48`; G02, sensitivity). That step joined two general repairs with a calibration, and the body
  gives no global mean for the Sun and tilt alone.
- Terluna records a two-year test of the Sun and tilt alone with the old split, `A28_dim5_sun_test`
  (terluna `climate/gcm/README.md#L662–671`, `#L1207`). Its yearly summaries on the drive give a global-mean
  surface of 294.95 and 295.44 K, a two-year mean of 295.20 K, against 294.31 K over years 15–24 of `A28_dim5`
  and 294.14 K in its branch year 24. That is +0.9 K over the two years and +1.3 K by the second, with the top of
  the air still gaining 1.93 and 1.79 W/m². In the same test the planetary albedo fell from 0.293 to 0.285, about
  2.3 W/m² more sunlight absorbed. The clouds' effect in sunlight weakened from −15.7 to −13.3 W/m², and the rain
  fell 6%, from 2.91 to 2.74 mm a day.
- The 0.6 K is therefore the net of a warming from the Sun and tilt, still growing when the test stopped, and a
  cooling from the refit of the split. The settled step (`A28_dim5_moon`, years 20–29, 294.90 K) confirms the net
  +0.59 K.
- What the two errors leave intact is the global mean of the arriving sunlight: the three sun-check files give
  293.55, 293.29 and 293.41 W/m², within 0.1%.
- "Several" counts two of the three defects. The third, the convective-cover unit, moved the global mean 1.8 K
  (G01).

**Correction.** "Two of these errors leave the global mean of the sunlight arriving at the top of the air
unchanged and move that sunlight between longitudes and latitudes. ExoPlaSim's Sun clock keeps every zonal and
global mean of the arriving sunlight exact, since at any instant the sunlight a latitude circle receives depends
on the Sun's declination and distance alone, and moves it between longitudes: [as now, to 'about 33° each model
day']. Earth's tilt, put in place of the configured one by the orbit default, brought Earth's seasons and summer
rain to 60°. With the Sun and the tilt set right, the climate's own global means moved too. Within two years 36%
of the land received under half a millimetre of rain a day, against 9% before, and the global-mean surface stood
0.9 K warmer, its top still gaining 1.9 W m⁻². The refit of the split of sunlight, made in the same step, then
brought the settled change to +0.6 K. A check of the global mean of the arriving sunlight passes with both errors
in place; they show in a map of sunlight by longitude or of rain by season." The two-year test needs a register
entry (`drive:…/gcm-runs/A28_dim5_sun_test/progress.json`) and a sentence in `results.tex` beside G02 before the
conclusion cites it.

### Finding 2 — BLOCKING — `conclusions.tex:46–49`

**Text.** "In the one electrified box, cloud tops reached 55--80~km, with the freezing levels five to six times
their heights in Earth's tropics, and the flashes came at about a hundredth of Earth's average density".

**Evidence.**
- The 55–80 km cloud tops and the 0 °C and −40 °C levels near 25 and 60 km come from six Morrison runs: three
  boxes forced from the Earth-orbit state and three rings forced from the Sun-and-tilt state (`results.tex:134–137`;
  G09). Terluna lists them as `box_0e`, `box_0e_small`, `box_0e_small_earth_fall` and three rings (terluna
  `climate/crm/README.md#L1437–1455`). None of the six carries electrification.
- The body itself describes at least two lunar electrified runs: the main run and "an earlier electrified run"
  (`results.tex:138–141`, `151–154`). Terluna's record has more: the original `box_0e_elec`, a fine 2 km box
  (`#L1895–1939`), and the main `box_0e_elec_corrected` with its first attempt before the ventilation fix
  (`#L2360–2387`). "The one electrified box" counts these as one and gives it the Morrison runs' cloud tops.
- For the main electrified run the body gives the charge at five to six times Earth's height: flashes start a
  median 35.8 km up, and the main negative charge lies at 40–42 km. It also gives the run's forcing from the
  Earth-orbit state and a caveat on the grid: the 6 km columns stand for about 1 km at Earth's scale, and on the
  Earth benchmark a coarser grid gave fewer, larger flashes (`results.tex:138–146`; G10). The sentence drops both.

**Correction.** "In the Morrison runs, cloud tops reached 55–80 km and the 0 °C and −40 °C levels stood five to
six times their heights in Earth's tropics. In the main electrified run, forced from the Earth-orbit state, the
charge took Earth's arrangement at five to six times its height, and the flashes came at about a hundredth of
Earth's average density, part of that difference perhaps from the 6 km grid. A law fitted at Earth's gravity
would be applied there far from the storms it was fitted on."

### Finding 3 — BLOCKING — `conclusions.tex:41–44`

**Text.** "with 85\% of the water falling from the clouds of a box forced from the GCM evaporating before it
reached the ground, those limits help set how much rain a low-gravity world receives."

**Evidence.**
- The body gives the limits' effect as unmeasured: "its drop limits and breakup remain Earth's, and their effect
  at other gravities is unmeasured, since the similarity pair failed to convect" (`reach.tex:37–38`). The
  measuring test is still to run: "limits scaled with the capillary length would show how much of the evaporation
  the small drops cause" (`next.tex:71–72`), and both outcomes are left open (`next.tex:73–75`).
- The 85% against 64% contrast comes from changing the fall speeds, with the drop-size limits held at Earth's
  (`results.tex:115–118`; G08). Terluna: "the pair differs in the fall alone" (`climate/crm/README.md#L963–966`).
  No run varied the limits.
- The box was forced from the Earth-orbit state (finding 7), and the rings lost 57–73% (`next.tex:69–70`).
- The sentence turns an untested mechanism into an outcome, a change of evidence state, and carries it from one
  lunar box to "a low-gravity world".

**Correction.** "...with 85% of the water falling from the clouds of a box forced from the Earth-orbit state
evaporating before it reached the ground, against 57–73% in the rings, those limits may set part of the test
world's surface rain; limits scaled with the capillary length would measure how much."

### Finding 4 — BLOCKING — `conclusions.tex:60–62`

**Text.** "Behind engineered protection, Earth-like air can persist on a body whose escape velocity would let a
natural atmosphere go, so that gravity, column, day and the air's height against the radius depart from Earth's
together, and the Earth values that depend on them err together."

**Evidence.**
- A low escape velocity goes with low gravity and a small radius. For a surface pressure near Earth's, these
  raise the column mass p/g and the scale height over the radius. The solar day follows from rotation and orbit.
- The paper's own constructed example contradicts the step. Mars held at 1 bar, plotted in Figure 1
  (`worlds.tex:24`), has a solar day of 1.0275 Earth days, beside g = 3.721 m/s², H/R = 0.00655 and 2.6 times
  Earth's column (`paper/data/worlds.json`; W04).
- The test world's 29.53-day day comes from the Moon's tidal lock (`worlds.tex:61–62`, Table regime; S01).

**Correction.** "...on a body whose escape velocity would let a natural atmosphere go, so that gravity, column
and the air's height against the radius depart from Earth's together, and the Earth values that depend on them
err together; on the test world, whose tidal lock sets a 29.53-day day, the day departs with them." Finding 12
adds the design's evidence state to the first clause.

### Finding 5 — MAJOR — `conclusions.tex:28–30`

**Text.** "Models of natural planets differ widely in cloud as well: on two tidally locked planets a global
cloud-permitting model covered 27 and 41\% of the sky with cloud, where two GCMs whose cover follows relative
humidity, stability and large-scale ascent covered 82--97\% \autocite{yang2023cloud}."

**Evidence.**
- The numbers and the GCMs' basis match Yang et al. (2023), arXiv v1 p. 3: "In global mean, the simulated cloud
  coverages in SAM are 26.9% and 41.1% for TRAPPIST-1e and K2-72e, respectively. In contrast, the corresponding
  values are 94.8% and 81.7% in CAM3 and 90.4% and 97.4% in ExoCAM". On pp. 3–4: "cloud coverages are
  empirically parameterized based on relative humidity, atmospheric stratification, and large-scale updrafts".
- The opening clause characterises models of natural planets as a class from one study: three models on two
  planets (AGENTS.md, "Claims stay within their evidence").
- The same authors conclude: "For time- and global-mean, the simulated surface temperature and planetary albedo
  in the CPM are broadly similar to those found in GCM experiments, but GCM simulations may have overestimated the
  cloud liquid water amount and cloud coverage especially on the nightside" (arXiv v1 p. 7).
- Their Supplementary Text 3 (in the arXiv file) counts a SAM column cloudy when its condensate path exceeds
  0.02 kg/m². The GCMs diagnose partial cloudiness with overlap rules, so part of the spread comes from the
  definitions.

**Correction.** "In one comparison on natural planets the models differed as widely in cloud cover. On
TRAPPIST-1e and K2-72e, both tidally locked, Yang et al.'s quasi-global cloud-permitting runs covered 27 and 41%
of the sky with cloud, where two GCMs whose cover follows relative humidity, stability and large-scale ascent
covered 82–97%, while the three models' global-mean surface temperatures and albedos came out broadly alike
\autocite{yang2023cloud}."

### Finding 6 — MAJOR — `conclusions.tex:30–32`

**Text.** "The radiation's fits can be replaced outright, since a scheme built from line-by-line spectroscopy would
hold on any column whose gases and pressures that spectroscopy covers, on a natural world as on a constructed
one."

**Evidence.**
- The scheme is a proposed design: "a reduced correlated-$k$ scheme built from the reference model's own
  spectroscopy in place of Sasamori's and Lacis and Hansen's fits would replace it, and would hold on any column
  whose gases and pressures that spectroscopy covers" (`next.tex:14–16`). The abstract keeps the conditional and
  the scope: "would replace the largest of those fits" (`abstract.tex:19–21`). "Can be replaced outright" states
  a present capability for the whole class.
- The radiation's fits include cloud optics, which gas spectroscopy leaves in place: liquid water's optics for all
  cloud, and Ebert and Curry's ice optics fitted to crystals of 10 µm and more (Table inventory rows "Cloud phase"
  and "RRTMG ice"; `repairs.tex:81–85`).
- The reference's continuum, MT_CKD (`introduction.tex:66–67`; `repairs.tex:121–122`), is itself fitted to
  measurements, and a correlated-k table spans temperature as well as pressure.
- The reference's checks against independent codes reach water-only longwave and Rayleigh scattering. Its CO₂,
  O₂, collision-induced absorption and sunlight on the lunar column still await one (`verification.tex:63–69`).

**Correction.** "A scheme built from line-by-line spectroscopy would replace the radiation's gas fits, the
largest of them, and would hold on any column whose gases, pressures and temperatures that spectroscopy covers,
on a natural world as on a constructed one; the cloud optics remain fits."

### Finding 7 — MAJOR — `conclusions.tex:27–28` and `42–43`

**Text.** "a box forced from the GCM brings a quarter of the GCM's rain to the ground" and "with 85\% of the
water falling from the clouds of a box forced from the GCM".

**Evidence.**
- The box was forced from the Earth-orbit state, which carried the Sun clock and Earth's tilt and brought 12% too
  little sunlight to the site: "A small box forced from the Earth-orbit state brought 34 mm to the ground per
  lunar day, where the GCM that forced it rained 129 mm and the Sun-and-tilt run 180 mm" (`results.tex:103–104`,
  `115–117`). G08 records "pre-correction forcing".
- The quarter holds against the forcing state (34/129 = 0.26). Against the corrected run's 180 mm the same box
  brought a fifth. Terluna records that a box forced from the corrected GCM brought 38 mm against 180 (terluna
  `climate/crm/README.md#L953–956`).
- The main electrified run of finding 2 had the same forcing (`results.tex:138–139`).

**Correction.** "...and a box forced from the GCM's Earth-orbit state, which still carried the Sun clock and
Earth's tilt, brings a quarter of that state's rain to the ground." Later in the section: "...from the clouds of
that box...".

### Finding 8 — MAJOR — `conclusions.tex:36–38`

**Text.** "In two windows of the test world's electrified run, the storms separated as much charge under
Takahashi's charging law as under Saunders and Peck's, with the opposite sign".

**Evidence.**
- The body: "In two windows of an earlier electrified run, days 10.5--12 and 40.5--42, made before the
  ventilation repair and with leakage off, the storms under Takahashi's charging law separate as much charge as
  under Saunders and Peck's, within the spread of the Saunders and Peck runs of the same days"
  (`results.tex:151–155`; G11). Terluna names that run `box_0e_elec` (`climate/crm/README.md#L2142–2143`).
- The missing ventilation made lunar rain evaporate 1.3–1.5 times too fast for its size (`verification.tex:102–105`).
- "The test world's electrified run" reads as the main run (`results.tex:138`), a different run with leakage on
  and the ventilation repaired.

**Correction.** "In two windows of an earlier electrified run, made before the ventilation repair and with leakage
off, the storms separated as much charge under Takahashi's charging law as under Saunders and Peck's, within the
spread of the Saunders and Peck runs, with the opposite sign, ..."

### Finding 9 — MAJOR — `conclusions.tex:48–49`

**Text.** "and resolved storms at other gravities can test it."

**Evidence.**
- The adapted CM1 reads gravity as a parameter "and has run storms at the Moon's gravity and at Earth's"
  (`reach.tex:36–37`; Table reach, "run at 1.62 and 9.81"). Storms at other gravities are a test still to run,
  and "can test it" states a present capability.
- Resolved electrified storms compute with laboratory charging laws whose choice turns the lunar polarity over,
  and with thresholds set for Earth's storms (Table inventory rows "Charging laws" and "Other thresholds", both
  Open; `results.tex:151–156`). The test they offer is therefore conditional on those laws.
- Sergeev et al. (2025), Sect. 4.2 (arXiv v2 p. 9), propose this route as an open one: "A possible route towards
  a more quantitative result is to use an explicit electric charging scheme coupled with a cloud-resolving model
  (e.g., Fierro et al. 2013)."

**Correction.** "...and electrified storms resolved at other gravities, computed with the same laboratory charging
laws, could test it."

### Finding 10 — MAJOR — `conclusions.tex:51–54`

**Text.** "Patched, SWAN scales an Earth sea sixfold in gravity within 0.3\% in wave height, where the released
code missed by 5.4\%, so for a sea under another gravity, the ancient seas of Mars among them, the open questions
are Earth's empirical laws for drag, wind input and breaking at that sea's ratio of air to water density."

**Evidence.**
- The similarity holds "On the code paths these tests ran, Komen growth and whitecapping under a fixed wind, DIA,
  the wind-input knee and depth breaking on Cartesian strips started from rest", while "the lunar runs' spherical
  grids, nests and GCM forcing were checked separately or left unchecked" (`verification.tex:47–51`). The body's
  reach statement keeps "tested at a sixth of Earth's gravity" (`reach.tex:39–41`).
- Other items remain open on the same model:
  - SWAN's early growth depends on the time step, and small seas fail their 5% criterion
    (`verification.tex:109–112`).
  - The air's density as a field, a wider frequency band for small seas, and swell decay (`next.tex:89–91`).
- "The open questions are" presents the laws as everything that remains for Mars's ancient seas, a world the
  patched code has yet to run.

**Correction.** "...so for a sea under another gravity, the ancient seas of Mars among them, the gravity scaling,
tested at a sixth of Earth's gravity on the code paths those tests ran, leaves open Earth's empirical laws for
drag, wind input and breaking at that sea's ratio of air to water density."

### Finding 11 — MAJOR — `conclusions.tex:55–57`

**Text.** "and on Titan, whose air is a quarter as tall in proportion, a flat treatment already fails beyond about
65\textdegree\ from the zenith \autocite{vincendon2010spherical}."

**Evidence.**
- Vincendon and Langevin (2010), arXiv v1 Sect. 1, write that plane-parallel codes for separating surface and
  aerosol signals are relevant "when the solar zenith angle is small enough to neglect the curvature of the
  planet (typically less than 80° for Mars and 65° for Titan, which has a larger relative scale height)".
- The same introduction gives atmospheric scale heights "typically around 10 km for Mars and 60 km for Titan",
  and their retrieval gives Titan's aerosols a scale height of 80 ± 10 km (abstract).
- Over Titan's 2,575 km radius those heights come to 0.023–0.031 of the radius, close to the test world's 0.030
  (`paper/data/worlds.json`). The paper's "quarter" uses the gas scale height at Titan's 94 K surface, 0.008 of
  the radius (`worlds.tex:77–78`).
- "Already" therefore infers from a shorter air to the 65° limit, while the source ties the limit to Titan's tall
  haze. The source also gives 65° as a typical value for aerosol scattering in surface retrievals.

**Correction.** "...and on Titan, whose haze has a scale height of about 80 km, a few hundredths of its radius as
on the test world, plane-parallel aerosol codes for its surface hold to about 65° from the zenith
\autocite{vincendon2010spherical}."

### Finding 12 — MAJOR — `conclusions.tex:60–61`

**Text.** "Behind engineered protection, Earth-like air can persist on a body whose escape velocity would let a
natural atmosphere go".

**Evidence.** The persistence rests on the Terluna design's own models: "By the design's own models its exobase
stays below 200~K and the air loses 0.6--1.4~kg\,s$^{-1}$ over a solar cycle, losses that would take 60 to 150
billion years to remove it" (`introduction.tex:22–25`). The register holds this as S15, state conditional model,
from terluna `research/decisions.md` L51, L125 and L370. One design, assessed by its own models, supports the
sentence. The conclusion states it for constructed worlds in general and drops that condition; the abstract
carries the same form (`abstract.tex:4–5`).

**Correction.** "By the Terluna design's own models, a shield that removes the ultraviolet heating the upper air
would keep Earth-like air on the Moon for tens of billions of years, on a body whose escape velocity let its
natural atmosphere go, so that ...", with finding 4's change to the rest of the sentence.

### Finding 13 — MAJOR — `conclusions.tex:62–63`

**Text.** "Modelling such a world also tests the tools used for natural ones: the defects found here bias runs
of slowly rotating and tidally locked planets".

**Evidence.**
- Of the five defects found, only the three in ExoPlaSim have errors that depend on the world. "The errors of the
  other two are independent of the world" (`assumptions.tex:98–100`, `119–125`).
- The Sun clock acts in non-synchronous runs alone (`assumptions.tex:100–101`; `reach.tex:17–19`).
- The section's first paragraph scopes the same statement correctly: "Three of the defects ... bias ExoPlaSim's
  runs" (`conclusions.tex:7–9`).

**Correction.** "...the three ExoPlaSim defects found here bias that model's runs of slowly rotating and tidally
locked planets, ..."

### Finding 14 — MAJOR — `conclusions.tex:66–69`

**Text.** "Released and repaired ExoPlaSim on Earth-air planets [...] would measure how far the three defects
move the simulated climate of worlds that other studies model, and would test the general repairs on a world
beyond the one they were made on."

**Evidence.**
- These runs exercise ExoPlaSim alone, so CM1's and SWAN's general repairs lie outside them.
- At Earth's gravity the cloud-water repair reproduces the released formula: CWGREF 9.80665 with CWSCALE
  g/9.80665 = 1 (Table repairs row "Cloud water"; `notes/exoplasim.md` L75–78). The test leaves it untested.
- The body names what the test reads: "the repaired runs' sunlight by longitude and convective cover against rain
  would test each general repair's arithmetic off the test world" (`next.tex:38–39`). Those are the Sun clock and
  the convective-cover unit.

**Correction.** "...and would test ExoPlaSim's Sun-clock and convective-cover repairs on a world beyond the one
they were made on."

### Finding 15 — MAJOR — `reach.tex:48–49`

**Text.** "the split of sunlight falls 0.7 points short on a 303~K column with 338~kg\,m$^{-2}$ of vapour".

**Evidence.**
- The 0.7 points belong to "the version fitted before the gas bands" (`verification.tex:57–60`; V07). For the
  current version, "The refit with the gas bands and the longwave correction are known through their fit
  residuals" (`verification.tex:60–61`).
- Terluna ties the test to the water multiplier 1.356 with Rayleigh 2.215 (`climate/gcm/README.md#L287–298`).
  The repairs as they stand use 1.292 and 2.237 (`notes/exoplasim.md` L204; Table repairs).
- The sentence itself opens "With the repairs as they stand".

**Correction.** "...while its columns stay near the fitted ones: the split of sunlight, in the version fitted
before the gas bands, fell 0.7 points short on a 303 K column with 338 kg m⁻² of vapour; the refit with the gas
bands is known through its fit residuals, and the longwave correction's accuracy near 307 K is unchecked."

### Finding 16 — MAJOR — `reach.tex:50–53`

**Text.** "For slowly rotating planets with Earth's gravity and air around a Sun-like star, such as those that
\textcite{yang2014strong} and \textcite{way2018climates} simulated with CAM3 and ROCKE-3D, ExoPlaSim's general
repairs alone should suffice, since the released radiation was fitted on columns and a spectrum like theirs".

**Evidence.**
- Way et al. (2018), arXiv v2 Table 2 (p. 5), list completed runs from 1.0 to 2.9 times Earth's insolation, up to
  3,959 W/m² at a 64-day rotation. Their simulations "were generally conducted for surface temperatures that
  remain lower than 400 K" (p. 4).
- Yang et al. (2014), arXiv v1 Sect. 2: "We increase the stellar flux until the model crashes, which occurs when
  the global mean surface temperature reaches ≈310 K". Their Fig. 2 shows a 128-day rotator at 3,000 W/m².
- The released radiation fits Earth's columns: Lacis and Hansen's absorptivity covers a range that ends at 10 cm
  of precipitable water (`assumptions.tex:64–66`). The body bounds it to "Earth-air columns near Earth's warmth
  with the released radiation" (`reach.tex:41–43`). The warm runs of both studies lie beyond those fits.
- The expectation and its evidence state ("should suffice", "the runs have yet to be made") match W03.

**Correction.** "For slowly rotating planets with Earth's gravity and air around a Sun-like star near Earth's
insolation, such as the cooler runs that \textcite{yang2014strong} and \textcite{way2018climates} made with CAM3
and ROCKE-3D, ExoPlaSim's general repairs, with its fixed-orbit setting, should suffice, since the released
radiation was fitted on columns and a spectrum like theirs; their warmer runs, at up to 2.9 times Earth's
insolation, lie beyond those fits. The runs have yet to be made."

### Finding 17 — MAJOR — `reach.tex:52`

**Text.** "ExoPlaSim's general repairs alone should suffice".

**Evidence.**
- Both cited studies set obliquity and eccentricity to zero. Way et al. (2018), arXiv v2 Sect. 2.1: "Planetary
  obliquity and eccentricity are zero". Yang et al. (2014), arXiv v1 Sect. 2: "We set geothermal heat flux,
  aerosols, obliquity, and eccentricity to zero".
- Under ExoPlaSim's default, a configured obliquity gives way to Earth's 23.7° (`assumptions.tex:113–118`;
  `reach.tex:24–25`).
- The cure is the `fixedorbit` switch, classed as an avoidance, a class apart from the general repairs
  (`repairs.tex:31–33`; Table repairs; W01). The general repairs alone would leave Earth's seasons in such runs.

**Correction.** "ExoPlaSim's general repairs, with its fixed-orbit setting, should suffice", as in finding 16's
text.

### Finding 18 — MINOR — `conclusions.tex:7–8`

**Text.** "an error that grows as a world departs from Earth's rotation, day or tilt".

**Evidence.** The Sun clock's skip is 1/(N−1) of a turn, where N is the number of rotations ExoPlaSim counts in a
360-day year (`notes/exoplasim.md` L25–32; `regime_calc.json`, `exoplasim_slow_rotators`). The skip is about 1°
near a one-day rotation and smaller for faster rotation, where N exceeds 360. The Sun clock's error therefore
grows as rotation slows. The cover unit's error grows with any departure of the day, and the orbit default's with
any departure of the configured tilt.

**Correction.** "...an error that grows as a world's rotation slows or its day or tilt departs from Earth's".

### Finding 19 — MINOR — `conclusions.tex:11–13`

**Text.** "ExoPlaSim's Sun clock keeps every zonal and global mean of sunlight exact, since the share of a latitude
circle in sunlight depends on the Sun's declination alone".

**Evidence.**
- The statement holds for the sunlight arriving at the top of the air. At any instant the zenith angles around a
  latitude circle, and so its mean sunlight, depend on the declination and the Sun's distance alone; the hour
  angle only turns the pattern in longitude. The sunlit share is one factor of that mean.
- Terluna: "Each row of latitude still gets its right mean" (`climate/gcm/README.md#L186–187`).
- In `sun_check_A28_dim5.json` the rows depart from the orbit used by up to 3.3 W/m², in a north–south
  antisymmetric pattern. I read that pattern as seasonal sampling under Earth's tilt with a 360-day output year,
  and it falls to 0.09 W/m² with the synodic clock and fixed orbit (`sun_check_A28_dim5_sun_test.json`).
- The means of the absorbed sunlight changed (finding 1).

**Correction.** "...keeps every zonal and global mean of the sunlight arriving at the top of the air exact, since
at any instant the sunlight a latitude circle receives depends on the Sun's declination and distance alone".
Finding 1's text includes this.

### Finding 20 — MINOR — `conclusions.tex:19–20`

**Text.** "A check of the global energy balance passes with such errors in place".

**Evidence.**
- The body and the register lack this statement.
- Terluna logs the top-of-atmosphere balance every year (`climate/gcm/README.md#L139–141`). Run A, with the Sun
  clock and Earth's orbit, balanced at +0.2 W/m² over years 30–39 (`#L309–314`), and `A28_dim5`'s years 15–24
  average −0.49 W/m² (drive `progress.json`).
- Any settled run passes such a check whatever its errors, the cover unit's included.

**Correction.** Enter the record in the body and register. Alternatively, state the property the errors have, as
finding 1's text does: "A check of the global mean of the arriving sunlight passes with both errors in place".

### Finding 21 — MINOR — `conclusions.tex:22–24`

**Text.** "moved its global-mean surface temperature by more than 20~K".

**Evidence.** The uncalibrated run was 315.5 K in model year 12 and still warming, against 295.5 K over years
30–39, "at least 20 K cooler" (`results.tex:38–39`; G14). The abstract (`abstract.tex:17–18`) and
`results.tex:89` carry "more than".

**Correction.** "by at least 20 K".

### Finding 22 — MINOR — `conclusions.tex:25–27`

**Text.** "The two atmospheric models disagree where each computes with Earth fits of its own: with the GCM's
transport imposed, CM1's lowest 1.8~km at 45\textdegree\,N stays 3.7~K warmer than the GCM's".

**Evidence.** In the body (`results.tex:94–113`), the ring was forced from the design case, the gap is measured
over the second lunar day, and the longwave correction was off. Of the 3.7 K:
- About 1.5 K is the GCM's own longwave over-cooling.
- "The remainder, a degree or two, is attributed by elimination to the two models' upward transport of the
  ground's heat". There the GCM has two layers in its lowest 6.5 km, Earth's σ levels, which Table inventory
  classes as geometry.
- The ice the starting sounding left above 107 km adds an unquantified term (`results.tex:101–102`;
  `verification.tex:99–102`).

**Correction.** "The two atmospheric models disagree in quantities each computes with Earth fits and grids of its
own: on the 45° N ring forced from the design case, with the GCM's transport imposed, CM1's lowest 1.8 km stays
3.7 K warmer than the GCM's over the second lunar day, about 1.5 K of it the GCM's longwave over-cooling, ..."

### Finding 23 — MINOR — `conclusions.tex:29`

**Text.** "a global cloud-permitting model".

**Evidence.** Yang et al. (2023), arXiv v1 Methods p. 9, run SAM in Cartesian geometry from 90° S to 90° N:
"So, we call the experiments as 'quasi-global cloud-permitting', rather than 'global cloud-resolving' over a
sphere". `results.tex:80` carries the same word.

**Correction.** "a quasi-global cloud-permitting model".

### Finding 24 — MINOR — `conclusions.tex:51`

**Text.** "Once a model scales correctly with gravity, its Earth-fitted laws are what remains uncertain."

**Evidence.** For the same model, numerical and forcing items also remain open (`verification.tex:109–114`;
`next.tex:89–91`; finding 10).

**Correction.** "Once a model scales correctly with gravity, what the change of gravity leaves uncertain lies in
its Earth-fitted laws."

### Finding 25 — MINOR — `conclusions.tex:51–52`

**Text.** "within 0.3\% in wave height".

**Evidence.** The value is 0.303% (`verification.tex:44`; V04). The abstract rounds the same way
(`abstract.tex:15–16`).

**Correction.** "within 0.31%" or "by 0.3%".

### Finding 26 — MINOR — `conclusions.tex:54–55`

**Text.** "against flat columns, the test world's curved air loses a net 5.8~W\,m$^{-2}$".

**Evidence.** The 5.8 W/m² is for the curved-air table's clear design column, set against the same air in flat
layers with a pseudo-spherical direct beam (`assumptions.tex:43–47`; H11). In the GCM, on the first channels, the
clear sky lost 5.4 W/m² and its clouds returned 3.5 of it in the first year (`results.tex:49–50`).

**Correction.** "against the same clear design column taken flat, the test world's curved air loses a net
5.8 W m⁻²".

### Finding 27 — MINOR — `conclusions.tex:63–65`

**Text.** "each change made for the test world is recorded with its switch or condition and its class".

**Evidence.** The two records give different classes for three CM1 changes:

| Change | `models/cm1/README.md` (patch table, lines 43–56) | Table repairs (`appendix.tex:69–71`) |
|---|---|---|
| The Sun (patch 05) | Capability | General |
| Soil, 5–80 cm (patch 08) | Capability; repair for long days | General |
| RRTMG's CO₂ and O₂ (patches 06–07) | Setting | General; setting |

`repairs.tex:21–23` also calls CM1's Sun, carbon dioxide and oxygen general repairs.

**Correction.** Reconcile the classes in `models/cm1/README.md` with Table repairs. The sentence stands once the
two agree.

### Finding 28 — MINOR — `conclusions.tex:65–66`

**Text.** "The general repairs were built to hold off the test world and have run on it alone."

**Evidence.**
- The Earth benchmarks ran general repairs at Earth's values: the electrified supercell on the gravity build at
  9.81 (`verification.tex:34–35`, `75–84`), and SWAN's knee patch at standard gravity (Table verification).
- The body's own wording elsewhere: "apart from the Earth benchmarks, every run so far is of the test world"
  (`reach.tex:84–85`), and "Away from Earth's values, the repaired models have run on the test world alone"
  (`next.tex:35`).

**Correction.** "...and, away from Earth's values, have run on it alone."

### Finding 29 — MINOR — `conclusions.tex:66–67`

**Text.** "rotating once in 16 and 64 days, the periods at which ROCKE-3D has simulated such planets
\autocite{way2018climates}".

**Evidence.**
- Way et al. (2018), arXiv v2 Tables 2–3, ran sidereal periods of 1, 2, 4, 8, 16, 32, 64, 128 and 256 days, so 16
  and 64 are two of nine. ROCKE-3D also has runs of such planets in other studies.
- `next.tex:36–37` adds "with the released radiation, which suits their Earth-sized columns", a condition the
  conclusion drops.

**Correction.** "...rotating once in 16 and 64 days, two of the sidereal periods at which
\textcite{way2018climates} ran ROCKE-3D, with the released radiation, would ..."

### Finding 30 — MINOR — `reach.tex:47–48`

**Text.** "With the repairs as they stand, the four models simulate the breathable Moon under other dimmings while
its columns stay near the fitted ones".

**Evidence.**
- The body reports runs of the repairs as they stand at the design dimming alone: "The corrected terms have run
  only together with the bands and the eased dimming, in the design case" (`results.tex:53–54`), and "the scale
  was set once, for the design case" (`worlds.tex:33–34`).
- The drive holds two 20-year runs of the current repairs, with the curved-air table and the gas bands in their
  configurations, at 0.9655 and 0.9685 of the sunlight (`gcm-runs/A28_corrected_9655` and
  `gcm-runs/A28_corrected_9685`). The body omits them.

**Correction.** "...the four models are built to simulate the breathable Moon under other dimmings while its
columns stay near the fitted ones". Alternatively, report the two runs and keep "simulate".

## 3. Checked and sound

| Statement | Location | Source and check |
|---|---|---|
| A world departing from Earth along four ratios at once | `conclusions.tex:3` | `introduction.tex:46–51`; `worlds.tex:3–14` |
| Four Earth-built codes; Earth values in four forms and five defects | `conclusions.tex:3–4` | `abstract.tex:5–9`; `introduction.tex:71–75`; `assumptions.tex:98` |
| Repair kind followed "largely" from form | `conclusions.tex:4–7` | `introduction.tex:82`; Table inventory. Constants and units took general repairs; geometry took the method where repaired; the radiation's gas fits took calibrations. The exceptions (ground-strike bound, SWAN's air density as a setting, ice optics as general) fall within "largely" |
| Three defects, little or no error at Earth's values | `conclusions.tex:7` | `assumptions.tex:98–118`; H23, H07, H24 |
| They bias ExoPlaSim's slow and tidally locked runs, by the code's arithmetic | `conclusions.tex:8–9` | `reach.tex:16–25`; W06 and W02 (calculation). `regime_calc.json`: cover bias +0.23 for TRAPPIST-1e, +0.31 for Proxima b |
| 8.3% below the mean from 270° to 57° E, up to 17% above near 164° E | `conclusions.tex:13–14` | `assumptions.tex:105–107`; H23. `sun_check_A28_dim5.json` relative range 0.9171–1.1737; terluna GCM README L186–189 |
| About 33° set back each model day for any rotation slower than 20 days, non-synchronous, default geometry | `conclusions.tex:15–16` | `regime_calc.json`: N = 12 and 32.7° for 21, 27.32, 64 and 243 days; `notes/exoplasim.md` L25–32; W02. Evidence state is the code's arithmetic, as paragraph 1 states |
| Earth's tilt brought Earth's seasons and summer rain to 60° | `conclusions.tex:16–17` | `assumptions.tex:113–118`; H24; G02 |
| 36% of land under 0.5 mm a day within two years, against 9% | `conclusions.tex:17–18` | `results.tex:46–48`; G02. Terluna GCM README L651, L662–665 (`A28_dim5_sun_test`, two years) |
| Joint step moved the global mean 0.6 K | `conclusions.tex:18–19` | `results.tex:44–46`; G02 (+0.59 K). Drive: 294.311 → 294.897 K. Its use is finding 1 |
| Changes to Earth-fitted parts moved the test world furthest | `conclusions.tex:22` | `results.tex:86–89`; G14, G05, G01 |
| Cloud settings up to about 6 K | `conclusions.tex:24` | `results.tex:73–78`; G05 (−4.98 K, about −5.9 K settled) |
| "The two general repairs measured singly", 1.6–2.5 K | `conclusions.tex:25` | `results.tex:42–44`, `86–88`; G01 (2.3 and 2.5 K; 1.8 and 1.6 K). Cloud water by pressure (a constant) and cover per Earth day (a unit) are the only general repairs measured alone in the GCM |
| 3.7 K at 45° N with transport imposed | `conclusions.tex:26–27` | `results.tex:94–98`; G06. Terluna CRM README L1151–1153: 23.5 against 19.8 °C |
| A quarter of the rain | `conclusions.tex:27–28` | 34/129 = 0.26; G08 (condition in finding 7) |
| 27 and 41%; 82–97%; cover from relative humidity, stability and ascent | `conclusions.tex:29–30` | Yang et al. (2023) arXiv v1 pp. 3–4: 26.9, 41.1; 94.8, 81.7; 90.4, 97.4. Two tidally locked planets: "both are assumed to be in synchronously rotating orbits" (p. 3) |
| Cloud-resolving runs compute with Earth-fitted microphysics | `conclusions.tex:32–34` | `next.tex:18–25`; Table inventory, CM1 rows |
| Some Earth laws testable in laboratories | `conclusions.tex:36` | `next.tex:77–82`; N01 |
| As much charge with the opposite sign; the laws disagree on rimed ice's sign in little cloud water | `conclusions.tex:37–39` | `results.tex:151–156`; G11; Terluna CRM README L2097–2117 (condition in finding 8) |
| The deciding measurement: 4–8 m/s, 0.02–0.2 g/m³, −5 to −16 °C, reachable in laboratories | `conclusions.tex:39–40` | N01; `next.tex:78–82`; Terluna CRM README L2167–2170 |
| Largest stable drop scales with the capillary length, 2.46 times longer at a sixth of Earth's gravity | `conclusions.tex:41–42` | `assumptions.tex:87–88`; H21. `regime_calc.json` 2.457; √(9.81/1.6242) = 2.458 |
| Morrison keeps Earth's drop-size and breakup limits | `conclusions.tex:42` | `assumptions.tex:85–88`; H21 |
| 85% of falling water evaporated | `conclusions.tex:42–43` | `results.tex:116–118`; G08; Terluna CRM README L936–940 (use in findings 3 and 7) |
| Flash rates on tidally locked planets estimated with Earth-fitted laws, from cloud-top height or graupel and ice | `conclusions.tex:44–46` | Braam et al. (2022) Sect. 2.4: "the lightning flash rates (LFR) can be described in terms of the cloud-top height H (Williams 1985; Price & Rind 1992; Boccippio 2002; Luhar et al. 2021)"; oceanic LFR = 2.0×10⁻⁵ H^4.38; "the range of data used to develop the parameterisation (Price & Rind 1994)"; Proxima Centauri b, tidally locked, 10.9 m/s². Sergeev et al. (2025) Sect. 2.2: M09 from the upward graupel flux at −15 °C and the total ice water path, "The coefficients k1 and k2 are determined empirically from observations", "originally derived from observations of severe thunderstorms over the United States"; PR92 "developed for Earth"; TRAPPIST-1e in 1:1 rotation |
| About a hundredth of Earth's average flash density | `conclusions.tex:47–48` | G10; `regime_calc.json` `flash_density`, ratio 0.0081 (attribution in finding 2) |
| Released SWAN missed by 5.4% | `conclusions.tex:52` | `verification.tex:42–44`; V04 (5.44%) |
| Tall air's geometry computed from the world's own column | `conclusions.tex:54–55` | `repairs.tex:87–108`; a general method, design intent |
| Titan's gas a quarter as tall in proportion | `conclusions.tex:56` | `worlds.json`: 0.00799/0.03015 = 0.27. The quote of the 65° limit matches Vincendon and Langevin Sect. 1 (its use is finding 11) |
| Constructed worlds pair Earth-like air with gravities, sizes and days no known natural world has | `conclusions.tex:59` | `introduction.tex:25–26` |
| Changes recorded with switch or condition | `conclusions.tex:63–64` | `repairs.tex:7–9`; Table repairs; model README patch tables (class in finding 27) |
| A modeller can see which changes apply unchanged and which need refitting | `conclusions.tex:64–65` | W01; Table repairs classes |
| Released and repaired ExoPlaSim on Earth-air planets would measure the three defects' effect | `conclusions.tex:66–68` | `next.tex:35–41`, a test still to run. Way et al. (2018): 1 bar N₂-dominated air with 400 ppmv CO₂ and 1 ppmv CH₄, zero obliquity and eccentricity, Earth-like topography. All three defects would act in such runs |
| The longwave correction's accuracy near 307 K is unchecked | `reach.tex:49–50` | `next.tex:9–13`; `notes/exoplasim.md` L229–237 |
| Yang et al. (2014) and Way et al. (2018): slow rotators with Earth's gravity and air around a Sun-like star, with CAM3 and ROCKE-3D | `reach.tex:50–52` | Yang et al. (2014) Sect. 2: CAM3 (CAM4 and CCSM3 in some cases), Earth's radius and gravity, 1 bar mainly N₂, 400 ppmv CO₂, 1 ppmv CH₄, the Sun's spectrum among others, rotation from 12 h to 365 d. Way et al. (2018) Sect. 2.1: ROCKE-3D. Scope in finding 16 |
| "The runs have yet to be made" | `reach.tex:53` | W03: "untested; no run made" |
| 69.8 against 77.6 days (64-day rotation); 265 against 726 days (243-day); "unless the year holds about twelve rotations" | `reach.tex:53–55` | `regime_calc.json` `exoplasim_slow_rotators`: model day P·12/11; solar day 1/(1/P − 1/365.25). The two match when the year holds 12 rotations. Way et al.'s Table 2 note gives 76.6 days for a 64-day sidereal period; the paper's 77.6 follows its own stated formula |
| Output in whole model days drifts against the Sun; sorting by the Sun's position avoids it | `reach.tex:55–56` | `repairs.tex:33–35` |

**Observations outside the scope**, for the sections that carry them:

- The Figure 1 caption (`worlds.tex:24–25`) and `worlds.json` place the illustrative slow rotators at "solar days
  of 16, 64 and 243 days". The conclusion and `next.tex:36–37` take 16 and 64 days as Way et al.'s sidereal
  periods, whose solar days are 16.7 and 77.6 days.
- `results.tex:80` ("a global cloud-permitting model") carries finding 23.
- `abstract.tex:15–18` ("within 0.3%", "more than 20 K") carries findings 25 and 21.
- `abstract.tex:4–5` ("an engineered shield can hold Earth-like air under a gravity too weak to keep it
  naturally") carries finding 12's evidence state.

## 4. Counts

| Severity | Count | Findings |
|---|---|---|
| BLOCKING | 4 | 1–4 |
| MAJOR | 13 | 5–17 |
| MINOR | 13 | 18–30 |
| Total | 30 | |
