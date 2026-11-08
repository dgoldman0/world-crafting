# Editorial round 10: the Conclusion, evidence review

## 1. Record

- **Reviewer:** a fresh Claude subagent (Claude Opus 5.5), acting as technical reviewer. It saw the section, the
  body, the claims register, run records and archived sources. It opened nothing under `paper/review/` except this
  record, and nothing under `paper/notes/`.
- **Date:** 2026-10-18.
- **Snapshot:** world-crafting `04a6c27` (04a6c274651fc68401536fc5dbfe723e9e0ed2a0). Terluna at `186b294`.
- **Scope:** `paper/sections/conclusions.tex` at 04a6c27, the whole section, 99 lines, sha256
  `8e98a1918fec8ad21ab7c31b5e3dc7908690b513184ca1257ce48ae3b14e3196`.
- **Method:** each number, attribution, causal claim, physical inference, scope word and universal in the section
  was traced to a body line, a claim ID and the primary record behind it. A few arithmetic checks were made: the
  regime_calc entries, the means of two GCM progress files and the Sun-check global means. No model, build or lint
  was run. Nothing was changed except this record.

**Evidence relied on.** These are sha256 hashes, first 16 hex digits, of each file as read at its snapshot.

| File | sha256 (16) |
|---|---|
| paper/sections/abstract.tex | 1d22734b8e9c39bc |
| paper/sections/introduction.tex | a88f442f589e007d |
| paper/sections/worlds.tex | 453a1d6cd6e39bf3 |
| paper/sections/assumptions.tex | 77bc704fe58d964f |
| paper/sections/repairs.tex | c846dbbf4dbaf39a |
| paper/sections/verification.tex | 4ddeb46903522c72 |
| paper/sections/results.tex | 112e8074232fd043 |
| paper/sections/reach.tex | fff8183910168eeb |
| paper/sections/next.tex | 789a34bd471f58e0 |
| paper/sections/appendix.tex | 17abe050d20a8603 |
| paper/claims.json | e462d3ff93eea66b |
| paper/data/regime_calc.json | 7a2935a8fbe6086c |
| paper/sources/manifest.json | afe0042bfc11c660 |
| paper/references.bib | c0c9662b36214175 |
| notes/verification_record.md | 983329688203341c |
| notes/waves.md | 9f7a775ed1b8a297 |
| notes/reference_radiation.md | 348501fa28bbe855 |
| notes/electrification.md | 2cd81eb8edbd7734 |
| notes/cm1.md | 75502ec7070a2400 |
| models/swan/README.md | abb218a0608362f5 |
| models/exoplasim/runs.json | 59af02ab8d4b7ea5 |
| python/climate/results/gcm/sun_check_A28_dim5.json | 5b922f8d7afede95 |
| python/climate/results/gcm/sun_check_A28_dim5_sun_test.json | b690e29206ec2e73 |
| terluna:climate/crm/README.md | 95776d41c55b3a3a |
| terluna:climate/gcm/README.md | 267413c2aa248c3b |
| terluna:climate/waves/README.md | 87fe5f3621fee9cf |
| terluna:climate/waves/first_experiments.md | 959868b935ca29c3 |
| terluna:research/decisions.md | cfca4e5a14d98925 |
| drive:gcm-runs/A28_dim5_sun_test/progress.json | 0d8563dbbe8c815b |
| drive:gcm-runs/A28_dim5/progress.json | 619f3de9adeafa38 |

**Originals opened.** Each was read through its text layer (`pdftotext`), and each full sha256 equals the
manifest's.

- `yang2023cloud.pdf` (0637811e…bc41), arXiv v1. Read: p. 3, Results "Clouds" (cover 26.9 and 41.1% in SAM against
  94.8, 81.7, 90.4 and 97.4%; albedos 18 and 37% against 29, 22, 47 and 39%; rotation 6.1 days for TRAPPIST-1e); p. 4,
  "Overall, the simulated climates between CPM and GCM are broadly similar, although quantitative differences
  exist"; p. 39, the global-mean table.
- `yang2023cloud_si.pdf` (1cc0a582…5554). Read: Text 3, where SAM's cloud fraction is 100% above 0.01 g/kg of cloud
  water.
- `vincendon2010spherical.pdf` (afcdf418…a7e9), arXiv v1. Read: the abstract (Titan's aerosol scale height
  80 ± 10 km); p. 2, where plane-parallel codes are relevant "typically less than 80° for Mars and 65° for Titan,
  which has a larger relative scale height"; p. 11, where Titan's radius is set to 2575 km.
- `way2018climates.pdf` (476e3e96…4820), arXiv v2. Read: the abstract and Sect. 2. Obliquity and eccentricity are
  zero; the air is 1 bar, N2-dominated, with CO2 at 400 ppmv and CH4 at 1 ppmv; "O3 is set to zero"; the land is
  modern Earth's. Read also Table 2 and its notes: rotation in sidereal days; X016 and X064 run at S0X = 1.0.
- `loftus2021physics.pdf` (d080f128…5c2d). Read: p. 9, Sect. 3.4, on why the practical upper bound on raindrop size
  is "not set from individual raindrop breakup but rather from hydrometeor collisions". Read also p. 22, App. C1:
  "Such experiments consistently agree (within about 20%) with the predictions of Equation 21 … and the dynamic
  viscosity of the drop medium is much larger than the fall medium's".

## 2. Findings

Line numbers are those of `paper/sections/conclusions.tex` at 04a6c27 unless another file is named.

### 1. MAJOR: the rain's slow fall is credited to the wrong class of repair (conclusions.tex:13–14, 16–18)

**Text.** "where the repairs of units, constants and geometry, measured one at a time, moved it by 2.5~K or less"
and "Small as their share of the global mean was, repairs of those kinds put the world's own gravity and geometry
into the codes, and with them the codes computed the rain, storms and sky … Raindrops fall about three times
slower".

**Evidence.**
- The slow fall comes from the gravity scaling of Morrison's Earth-fitted fall-speed laws, V = aD^b
  (repairs.tex:54–62; claim R02; regime_calc.json `fall_speed_slowdown`, rain 2.94).
- The inventory gives that Earth value the form Fit, with a general repair: "Fall speeds & $V=aD^b$ fitted at
  Earth's $g$ … & Fit & L & General" (assumptions.tex:187). A general repair is one that "applies a scaling law"
  (introduction.tex:76–78).
- By L13–14, "repairs of those kinds" are repairs of units, constants and geometry. So the first of the paragraph's
  three features goes to a class that excludes its repair.
- The scaling's share of the global mean was never measured, since it acts in CM1 alone.
- The storms are credited correctly (CM1's gravity constant, assumptions.tex:186), and so is the sky (the
  curved-air method, geometry).

**Correction.** Name the class by kind at L13–14, with no added words: "where the general repairs and the curved-air
method, measured one at a time, moved it by 2.5~K or less".
- The figures stay true: 2.30 K and about 2.5 K settled, 1.76 K and about 1.6 K (G01); 0.65 K (G03); 0.9 K for the
  Sun and tilt together (G17).
- The ice optics, a general repair measured only together with the longwave correction (results.tex:82–86), stays
  outside "measured one at a time".
- L16's "repairs of those kinds" then includes the scaling law.
- If L13–14 is kept, L16 can read "repairs of those kinds, with the fall speeds' scaling law, put …" (+6 words).

### 2. MINOR: "drop sizes" for drop-size limits (conclusions.tex:18–19)

**Text.** "with drop sizes still set for Earth"

**Evidence.** Morrison's scheme computes the sizes. What stays Earth's are its limits: the 2.8 mm cap on rain's mean
diameter, and breakup from a mean of 0.3 mm (assumptions.tex:87–90 and :188; H21; notes/cm1.md:71–75). The section
itself later says "CM1's limits on raindrop size" (L53–54).

**Correction.** "with drop-size limits still set for Earth" (+1 word).

### 3. MINOR: "in both models" (conclusions.tex:20)

**Text.** "The same gravity, in both models, stretched the storms upward"

**Evidence.**
- The heights come from six Morrison runs of CM1: three boxes, one of them at Earth's fall speeds, and three rings.
  In them 0 °C stands near 25 km, −40 °C near 60 km, and cloud tops reach 55–80 km (G09; results.tex:141–144; Terluna
  climate/crm/README.md:1454, "In every run").
- Elsewhere in the body, "both models" and "the two models" mean the GCM and CM1 (repairs.tex:87;
  results.tex:115–117; next.tex:45, 68).
- The body gives no storm heights for the GCM. The phrase therefore reads as a claim about the GCM that the evidence
  does not make.

**Correction.** "The same gravity, in every run, stretched the storms upward" (no added words).

### 4. MINOR: the scaled-sea statement lacks its code-path scope (conclusions.tex:26)

**Text.** "once SWAN's wind-input knee moves with gravity, the lunar sea is an Earth sea scaled."

**Evidence.**
- The similarity test ran on Cartesian strips started from rest, with Komen growth and whitecapping under a fixed
  wind, DIA, the knee and depth breaking.
- The lunar runs' spherical grids, nests and GCM forcing were checked separately or left unchecked
  (verification.tex:48–51; notes/waves.md:62–68; reach.tex:39–41).
- The lunar runs use air of 1.40 kg m⁻³, where both strips used 1.28 (models/swan/README.md:97–111; Terluna
  climate/waves/first_experiments.md, design table).
- "In its models" (L17) already keeps the statement a model statement. What is missing is the scope of the code
  paths.

**Correction.** "the lunar sea is, on the paths tested, an Earth sea scaled." (+4 words).

### 5. MAJOR: the failed CM1 pair is given a design it did not have (conclusions.tex:33–35)

**Text.** "A similarity run of that kind tests whether gravity enters a code consistently, a property of the code on
any world, and CM1's gravity-scaled microphysics, behind the slow rain, still lacks that test, since the pair of runs
designed for it failed to convect."

**Evidence.**
- The pair was designed to measure how far lunar convection departs from Earth's convection stretched sixfold. The
  record gives the reason: "The microphysics does not stretch: drops, snow and graupel fall at speeds that follow
  gravity to other powers" (Terluna climate/crm/README.md:2508–2516; S12, V06; worlds.tex:92–96).
- A run of that pair is expected to depart from similarity. It "would measure how far the scaled microphysics
  departs from similarity" (next.tex:75–77).
- It could not show, as SWAN's run did, that gravity enters the code consistently.
- The sentence gives the failed pair a design the record does not, and it turns a planned measurement of the
  physics into a missing check of the code.

**Correction.** "… still lacks such a run, since the pair of runs designed to measure its departure from similarity
failed to convect." (+5 words).

### 6. MINOR: "opposite arrangements" drops the record's "most" and "about half" (conclusions.tex:49)

**Text.** "the lunar storms held their charge in opposite arrangements under the two"

**Evidence.** Under Takahashi's law the arrangement was inverted. Under Saunders and Peck's law the normal arrangement
held "in most of the second window's outputs and about half of the first's" (G11; next.tex:84–87).

**Correction.** "in mostly opposite arrangements" (+1 word).

### 7. MINOR: what gravity enters through the capillary length, and the scope of the 20% (conclusions.tex:50–53)

**Text.** "Gravity enters the raindrop through the capillary length, so experiments at Earth's gravity can vary the
other terms: the largest stable drops of other liquids, falling through other fluids, follow the capillary scaling
within about 20\%"

**Evidence.**
- Gravity also enters a raindrop's fall speed and ventilation (L18; repairs.tex:54–62). The capillary length bounds
  the largest stable drop (assumptions.tex:89–90; H21).
- Loftus and Wordsworth's 20% holds for experiments in which "the dynamic viscosity of the drop medium is much larger
  than the fall medium's (like raindrops and air)" (loftus2021physics, App. C1, p. 22 of 28).

**Correction.** "Gravity enters the largest stable raindrop through the capillary length … falling through less
viscous fluids" (+3 words).

### 8. MINOR: the cover's cap is dropped (conclusions.tex:70)

**Text.** "the convective-cover unit adds about 0.23 to the convective cover of a synchronous run of TRAPPIST-1e"

**Evidence.** At a 6.10-day rotation ExoPlaSim keeps a model day of 6.20 days, and 0.125 ln 6.20 = 0.228 (W06;
regime_calc.json `exoplasim_synchronous_cover_bias`). The cover is capped at 0.8 (assumptions.tex:114–115). The full
0.23 is added only where the cover lies below the cap by at least that much.

**Correction.** "adds up to about 0.23" (+2 words).

### 9. MINOR: "the repairs" for ExoPlaSim's repairs (conclusions.tex:75)

**Text.** "would be the first runs of the repairs off the test world"

**Evidence.**
- Every ExoPlaSim run on record is lunar (models/exoplasim/runs.json), so the statement holds for ExoPlaSim's
  repairs.
- The patched CM1 graft has run Earth's supercell, and patched SWAN has run Earth strips (verification.tex:34–35,
  39–44; appendix.tex:133–134; reach.tex:91–93).
- L63–64 already sets those runs apart as Earth's values and numerical controls.

**Correction.** "the first runs of its repairs off the test world" (no added words).

### 10. MINOR: "meets at once" and "one at a time" (conclusions.tex:78–80)

**Text.** "a model run on such a world meets at once the Earth values that a slow rotator meets one at a time and a
smaller world a few at a time."

**Evidence.**
- A constructed world with Earth-like air and Earth's day departs along fewer ratios. The test world departs along
  all four (introduction.tex:46–51; worlds.tex:3–14).
- A slow rotator departs along one ratio, the day, and meets several Earth values on it at once: the Sun clock, the
  cover's unit and the calendar (assumptions.tex:37–39, 100–115).
- Titan, a smaller world, departs along all four (worlds.tex:10–11). "A few at a time" therefore holds for smaller
  worlds with Earth-like air, which is the sentence's frame. No change is needed there.

**Correction.** "can meet at once the Earth values that a slow rotator meets one ratio at a time" (+2 words).

### 11. MINOR: the Earth values given as the whole of the design's uncertainty (conclusions.tex:84–86)

**Text.** "the Earth values left in them are the design's own uncertainty: in the air where people and plants would
live, … the storm model ran 3.7~K warmer than the GCM that forced it once the transport across the ring was imposed"

**Evidence.**
- The design's uncertainty also holds the scenario's placeholders, such as the land albedo of 0.2 (worlds.tex:41),
  and the adaptation's defects.
- The 3.7 K includes an unquantified term from the ice that the ring's starting sounding left above 107 km
  (results.tex:108–109; verification.tex:99–102; H31).
- The 3.7 K is a ring mean over the second lunar day: 23.5 against 19.8 °C (G06; Terluna climate/crm/README.md,
  the table of the confirming test).

**Correction.** "are part of the design's own uncertainty" (+2 words). Optionally, "ran 3.7~K warmer over its second
lunar day".

### 12. MAJOR: the 1.5 K is the GCM's over-cooling beyond CM1's, not its own (conclusions.tex:87)

**Text.** "and about 1.5~K of that gap is the GCM's own over-cooling through its Earth-fitted longwave."

**Evidence.**
- Against the correlated-k model, PlaSim over-cools its lowest layer by 10.6 W m⁻², and RRTMG over-cools CM1's lowest
  1.8 km by 4.5 W m⁻².
- The GCM therefore sheds about 6 W m⁻² more than CM1, worth about 1.5 K at the ring's estimated 4 W m⁻² per kelvin
  (G07; results.tex:105–108).
- The primary record adds: "Against the line-by-line model both over-cool their lower air, PlaSim by about 2.5 K's
  worth near the ground and RRTMG by about 1 K's" (Terluna climate/crm/README.md:1190–1193).
- So the 1.5 K is the GCM's over-cooling net of CM1's own. The GCM's own over-cooling is worth about 2.5 K.
- The reading matters for the next steps (next.tex:21–24, 63–69). By the record's own figures, correcting the GCM's
  longwave alone would move the gap by about 2.5 K's worth, which is more than 1.5 K. This is the reviewer's
  arithmetic; no run has made the correction.
- results.tex:119 and notes/cm1.md:120–121 use the same shorthand. Both lie outside this scope and are noted for
  the author.

**Correction.** "and about 1.5~K of that gap is the GCM's over-cooling beyond CM1's, through its Earth-fitted
longwave." (+1 word).

### 13. MINOR: the laboratory charge measurement is listed among the fits that carry the climate's Earth share (conclusions.tex:89–93)

**Text.** "in four of them, measured one switch at a time on the test world, Earth's share of the climate came mostly
from fits whose replacements would come from evidence outside the codes: … and, inside those runs, laboratory
measurements of the charge rimed ice takes at the storms' impact speeds and of the largest stable drops of other
liquids."

**Evidence.**
- The ranking of Earth's share by form was measured on the GCM's global-mean surface temperature
  (results.tex:87–91; G01, G03, G05, G14). SWASH runs unmodified (repairs.tex:186–187).
- The charging law's measured effect is on the arrangement of charge (results.tex:159–167; G11).
- The drop limits' effect is unmeasured (reach.tex:36–37).
- Neither the charging law nor the drop limits is part of the measured share of the climate. "Inside those runs"
  places the laboratory evidence with the resolved runs' own laws, but the colon presents it as replacing fits that
  carry Earth's share of the climate.

**Correction.** "and, for the weather inside those runs, laboratory measurements …" (+3 words). "The climate" then
reads as the GCM's, which is what the paper calls the climate elsewhere (L95, "from its climate to its shore").

### 14. MAJOR: the prospect's condition falls short of its promise (conclusions.tex:93–95)

**Text.** "Built and checked, those replacements would let a modeller set the gravity, day, column and starlight of a
world whose air and water resemble Earth's and follow its weather down the chain from its climate to its shore, with
Earth's share of the results measured:"

**Evidence.**
- The replacements named in L91–93 cover the radiation's gas fits, the cloud's cover and water, the charging laws
  and the drop limits.
- Earth values outside them stay on the chain, with no replacement in view, so their share would stay unmeasured.
- The first group is the sea's laws: wind input, whitecapping and breaking, and SWASH's breaking thresholds
  (assumptions.tex:91–93 and :214, "Empirical laws … Open"; reach.tex:114, Seas, "Beyond them: Earth's drag, growth
  and breaking laws"; next.tex:98–101). AGROW's coefficient carries Earth's ratio of air to water density
  (models/swan/README.md:89–93).
- The second is the thin-shell, constant-gravity dynamics and Earth's σ levels (assumptions.tex:171, 174, 195;
  next.tex:54–61). The σ levels bear on the gap's unexplained "degree or two" (results.tex:115–117).
- The adapted models also hold only for "scale heights up to a few hundredths of the radius, the test world's"
  (reach.tex:81–82). That limit bounds the gravity and column a modeller could set.
- The section states none of these. The prospect stays conditional ("would"), but its condition falls short of
  its promise for the shore and for the share measured.

**Correction.** "with Earth's share in those fits measured:" (no added words). This makes the promised measurement
exact. It leaves the sea's laws and the dynamics as Earth's, inside the model. If the author wants the height limit
stated, "…of a world whose air and water resemble Earth's, its air no taller against its radius than the test
world's," adds it (+10 words).

## 3. Checked and sound

**Conditions stated once in the section.** These are not asked for again:
- L47–50 gives the charge arrangement's dependence on the law for L20–21.
- "In its models" (L17) keeps L18–26 as model statements.
- "By the code's own arithmetic" (L67) gives L68–70 the state of a calculation.
- L38–41 gives the radiation scheme's conditions: the independent check, the comparison layer by layer, the gases,
  pressures and temperatures of the checks, and the starlight it is built for. These cover "column and starlight" in
  L94 as far as the radiation goes.
- "Within the limits of its law" (L58) bounds the general repairs on another world.
- L63–64 bounds where the repaired codes have run.

**Paragraph 1.**
- L3–6, "most repairs … switches whose default is written to reproduce the released code": repairs.tex:3–6 and
  tab:repairs (appendix.tex:63–109). Counted over repairs of Earth values and defects, about 17 take a switch or
  input whose default reproduces the release. About 6 are unconditional or depart from it: CM1's air and soil,
  WRF-ELEC's 9.81 for 9.8, flash reach, ice size, and SWAN's air density. "Written to" keeps the design-intent state;
  identity has been run for five ExoPlaSim patches (V01).
- L6–8: introduction.tex:46–51 and worlds.tex:3–14.

**Paragraph 2.**
- L10–14, "at least 20 K": G14. Terluna climate/gcm/README.md:222–233 shows that the first calibration was fitted
  against the line-by-line model on global-mean columns, so "against the line-by-line model" is exact.
- "Up to about 6 K": G05 and G16, −4.98 K over the window and about −5.9 K settled. The sentence names these as
  tests, so their sensitivity state is visible.
- "2.5 K or less": G01, G03 and G17. The geometry's 0.65 K ran on the table's first channels (results.tex:53–54),
  and the bound holds as stated.

**Paragraph 3.**
- L18, "about three times slower": R02, 2.94.
- L19–20, 85 against 64%: G08. Terluna climate/crm/README.md:936–975 gives 197/(197+34) and 108/(108+60), in the
  Morrison box on the Earth-orbit forcing, with every hydrometeor at Earth's speeds in the control. The ventilation
  defect of H29 affected NSSL only.
- L20–21, the charge "at five to six times its height": G10 puts the main negative charge at 40–42 km, at −13 to
  −14 °C, just above −7 °C as on Earth. G09 puts the temperature levels five to six times Earth's heights. The normal
  arrangement held in both lunar days (Terluna climate/crm/README.md:2392–2394).
- L21–24: S04 gives the Sun 12.2° down, the shadow 40.1 km up, and 0.465 (isothermal) or 0.45 (design profile) of
  the mass above the shadow, refraction ignored. Flat columns are lit only above their own horizon
  (assumptions.tex:44–45). The terms apply below the horizon (repairs.tex:96–99).
- L24–26: 4.2–4.8 times the height, about five times the period, Wu's drag at both gravities (Terluna
  climate/waves/first_experiments.md:26–27). The knee patch changes the lunar 48-hour heights by at most 0.11%
  (models/swan/README.md:75–77), so "needed only the gravity" holds. "Earth's steepness": Terluna
  climate/waves/README.md:42.

**Paragraph 4.**
- L28–29, "the checks of a code need nothing from the world it models": no observation of the world enters any
  check. The calibrations use the designed columns (verification.tex:3–15).
- L29–31: V01 and notes/verification_record.md:36–44. Five one-year identity runs repeat the restart of the build
  before each patch. The identity holds along the trajectory tested, which "a model year's restart" names.
- L31–33, 0.3% and "up to 5.4%": V04 and models/swan/README.md:82–84. Both figures are largest differences.
- L33–34, "a property of the code on any world": verification.tex:11–12 and notes/verification_record.md:23. That
  the Earth coefficients go untested (verification.tex:12–13) is carried by L35, "The fits need evidence from outside
  the codes."

**Paragraph 5.**
- L37–41: next.tex:15–19 and 30–34; notes/reference_radiation.md:20–26 and 272–275. The planned independent check
  includes Rayleigh scattering with every absorber, so "gas and scattering fits" lies within the planned evidence.
  The state is design intent.
- L41–43, Yang et al.: cover and albedo as read above, and "broadly similar" (p. 4).
- L43–44, "a method built for a slice of any world's GCM": repairs.tex:187–188. The calibration is planned
  (next.tex:21–28). The sentence claims nothing about the target's accuracy. The body records that the cloud at a
  place depends on the slice's direction (results.tex:126–129; G15).

**Paragraph 6.**
- L46–50: G11, N01 and notes/electrification.md:91–96. The windows' conditions (made before the ventilation repair,
  with leakage off) are kept.
- L50–53: Loftus and Wordsworth, App. C1.
- L53–55: next.tex:73–80. The added condition, "if the sizes that collisions allow scale as the largest stable drop
  does", matches Loftus and Wordsworth p. 9, where collisions set the practical bound on Earth.

**Paragraph 7.**
- L57–60: introduction.tex:76–81, reach.tex:76–79, W01 and W05. "Is built to hold" keeps the design-intent state.
- L60–63: Vincendon and Langevin, p. 2 and Sect. 3.2. The 80 km haze is 3.1% of 2575 km, against the test world's
  0.030 (regime_calc.json `scale_height`). "Matters" infers from their published result, and Titan's radiation is
  scoped as built anew at L60.
- L63–64: abstract.tex:19–20, reach.tex:44–45 and the tab:reach caption.

**Paragraph 8.**
- L66–68: assumptions.tex:100–120 and H07, H23, H24.
- L68–69, "about 33°" for rotations slower than 20 days: regime_calc.json `exoplasim_slow_rotators` gives N = 24
  and 15.7° at 20 days, and N = 12 and 32.7° at 21 days and slower. The Moon's skip is 32.5° (H23).
- L70: 0.228 (W06). TRAPPIST-1e's rotation of 6.1 days is from Yang et al., p. 3.
- L70–71, "kept the global mean of the sunlight": the global means at the top of the air are 293.55 W m⁻² in
  A28_dim5, years 15–24, and 293.29 in the two-year test (`sun_check` files). Each row keeps its mean under the old
  Sun clock (Terluna climate/gcm/README.md:187).
- L72–73, 0.9 K, still gaining: the drive's progress files give 294.31 K over years 15–24 against 295.20 K over the
  test's two years, with the top of the air gaining 1.93 and 1.79 W m⁻² (G17).
- L73, "fourfold": 9 to 36% (G02).
- L74–76: Way et al.'s set-up as read above matches next.tex:38–45. X016 and X064 run at Earth's insolation. All
  three defects bite: the Sun clock at 15.7° and 32.7°, the cover's unit, and the default orbit replacing a configured
  zero tilt.

**Paragraph 9.**
- L78: introduction.tex:25–26.
- L80–83: worlds.tex:31–34 and G04. Terluna research/decisions.md, the rows of 2026-10-14, gives the cooling
  "answered with less dimming" to a scale near 0.970. The conditional "could move it again" matches next.tex:12–14
  and 26.
- L85–86, 3.7 K at 45°N with the longwave correction off, once the transport is imposed: G06 and results.tex:101–105.

**Paragraph 10.**
- L89, "many models … began as models of Earth": introduction.tex:3–13. This is scoped to the cited developers and
  codes.
- L95–99: each feature listed has a body counterpart. Storm heights: G09. Charge: G10 and G11. Rain at the ground:
  G08. Run-up: G12. Sunlit air: S04. The prospect stays conditional ("would"); Finding 14 covers the condition.

## 4. Counts

| Severity | Count | Findings |
|---|---|---|
| BLOCKING | 0 | — |
| MAJOR | 4 | 1, 5, 12, 14 |
| MINOR | 10 | 2, 3, 4, 6, 7, 8, 9, 10, 11, 13 |

The corrections, if all are taken, add about 25 words to the section. Each keeps its sentence's structure.
