# Reference radiation: the radiative–convective model, its correlated-k scheme and the curved-air ledger

These notes cover two in-house tools that the ExoPlaSim and CM1 adaptations rest on: the line-by-line
radiative–convective model with its correlated-k thermal scheme (`atmosphere/radiative_convective`), and the
curved-air ledger (`climate/gcm/twilight.py`) with the spherical sky solver it calls. Section 3 lists what a
runnable copy of the ledger needs. The solver itself is covered in [sky_solver.md](sky_solver.md).

Paths and line numbers are Terluna's at commit 186b294 (the files cited are unchanged at f03b839). In this
repository the same files sit under `python/` with the same package paths. **Documented** marks what Terluna's code,
records or READMEs state, with the file and line. **Finding** marks this review's own observation, with the evidence
or arithmetic behind it. Evidence states follow Terluna's AGENTS.md: reproduction of a reference output, agreement
with an independent code, analytic and limiting-case tests, numerical convergence and internal consistency are
different things. None of them is empirical validation of a lunar atmosphere, and no such validation exists.

This review read code, records, products, logs and cache metadata, and did small arithmetic. It ran no model and
no test.

Main points:

- The radiative–convective model is the target the GCM's shortwave and longwave were calibrated to and the
  reference CM1's radiation was checked against. Its only cross-code check (PyRADS) covers water-only longwave at
  constant gravity; nothing independent checks its CO2, O2, collision-induced or solar calculation on the lunar
  column.
- Two of its recorded checks, PyRADS and the Monte Carlo Rayleigh reference, are numbers in `validation.json` with
  no harness in the repository. The Monte Carlo stops at Rayleigh depth 1.5; the lunar column reaches about 4 at
  360 nm.
- Its longwave is plane-parallel and its global mean counts only the sunlit hemisphere on the solid disk. The
  ledger puts the missing geometry at −5.8 W/m² net for the design column; the 1-D balance tables do not carry it.
- The ledger's `orders_converged = false` comes from one of 282 channels, with an omitted tail of about 3×10⁻⁴ of
  that channel's diffuse field: negligible, but unrecorded.
- The ledger's daytime "curved light" term includes the two-stream's under-reflection relative to exact
  multiple scattering, not only geometry.
- The middle-atmosphere exobase check scales only the solar side. The ledger's own longwave terms offset about
  half of the added sunlight near the 0.3 Pa base and exceed it between 15 and 150 km.

## 1. The radiative–convective model and ck.py (`atmosphere/radiative_convective`)

### 1.1 What it computes

**Documented.** A one-dimensional, clear-sky, line-by-line energy budget of a prescribed column, the inverse
habitable-zone method (METHODS.md:1-10). For a surface temperature Ts, `climate.evaluate` (climate.py:147-179)
builds the column and returns, one row per spectral shield: outgoing longwave (OLR), surface longwave up and down,
absorbed sunlight (ASR), planetary albedo, sunlight absorbed by the ground and by the air, water and air columns,
and tropopause pressure and height. `run.py:37-63` defines the sweeps: the Earth control at 1 atm and the Moon at
1.0 and 1.2 atm, with Manabe–Wetherald humidity at 260–320 K or saturation at 250–370 K, CO2 at 150–1000 ppm, a
150 or 250 K stratosphere, and each shield. It writes `results/inverse_climate.csv` (schema
`terluna.atmosphere.inverse-climate/1`). `analysis.py` gives balance temperatures for an assumed cloud effect C and
the saturated runaway limit. `trace_gases.py` and `reduced_gases.py` add SF6, NF3, CF4, CH4 and N2O forcing on the
same columns.

- **Column** (thermodynamics.py):
  - A saturated, non-dilute pseudoadiabat (Ding & Pierrehumbert 2016) from Ts up to a prescribed isothermal
    stratosphere, 200 K by default (227-235).
  - Manabe–Wetherald relative humidity, RH = 0.77 (p/ps − 0.02)/0.98 (163-168), or saturation; stratospheric
    water held at the tropopause mixing ratio (281-283).
  - Longwave: 70 levels to 1% of ps and 20 more to a 1 Pa top. Sunlight: 40 + 8 levels (climate.py:57-58).
- **Spectroscopy** (spectroscopy.py, optics.py):
  - HITRAN2020 lines of H2O (7 isotopologues), CO2 (12) and O2 (3), fetched from hitran.org's API and checked by
    hash (inputs.json). Intensity floor 10⁻²⁸ cm/molecule for H2O and CO2; all O2 lines (optics.py:26).
  - Line shape: Voigt within 50 Gaussian widths and Lorentzian beyond, cut at 25 cm⁻¹. Each line is summed as a
    fine core, a coarse near wing and an FFT far wing (spectroscopy.py:174-187; METHODS.md:83-94).
  - MT_CKD 4.3 re-implemented in Python; water lines lose their 25 cm⁻¹ pedestal, as MT_CKD assumes
    (spectroscopy.py:288-326; METHODS.md:61-65).
  - HITRAN collision-induced absorption for N2–N2, O2–N2, O2–O2 and N2–H2O (spectroscopy.py:396-397). Rayleigh
    scattering after Bodhaine et al. (402-418).
  - CO2 and O2 are air-broadened only and served from a cached node table in ln p and T (optics.py:30, 46-50;
    METHODS.md:96-100).
- **Grids:** longwave 1–3000 cm⁻¹ at 0.01 cm⁻¹. Sunlight 2000–20,000 cm⁻¹ at 0.05 cm⁻¹, plus
  20,000–49,500 cm⁻¹ at 2 cm⁻¹ with only Rayleigh scattering and O2 collision bands (METHODS.md:78-81;
  climate.py:24).
- **Thermal transfer:** non-scattering, plane-parallel layers with a source linear in optical depth, four Gauss
  angles per hemisphere, black ground (longwave.py:1-79).
- **Solar transfer:**
  - Delta-scaled two-stream layers ("practical improved flux method") combined by adding over a Lambertian ground
    (shortwave.py:56-143), with a pseudo-spherical direct beam (91-127).
  - Planetary means over six Gauss nodes in μ0 on the sunlit hemisphere, normalised to S/4 on the solid disk
    (146-182).
  - The response is computed per unit spectral irradiance, so each shield applies as a product
    (climate.py:106-144).
  - Spectrum: TSIS-1 HSRS for 202–2730 nm with a 5772 K tail beyond, scaled to 1361 W/m². Light below 202 nm is
    omitted; light beyond 5 µm is counted as absorbed in the air (shortwave.py:21-53; climate.py:134-135).
- **ck.py** (the correlated-k scheme):
  - 16 bands over 1–3000 cm⁻¹ (29-31) × 16 g-points: 8 Gauss points on [0, 0.9] and 8 on [0.9, 1] (40-45).
  - k-tables for H2O (lines plus MT_CKD, by vapour fraction), CO2 and O3, built from this model's line-by-line
    spectra. Nodes: 27 pressures from 0.1 Pa to 3.2×10⁵ Pa, 12 temperatures from 100 to 375 K and five water
    fractions from 0 to 0.5 (32-34). Each spectrum is sampled at a quarter of a CO2 line's Voigt half-width,
    2×10⁻⁴–0.01 cm⁻¹ (53-58).
  - Collision-induced absorption enters as a temperature-only pseudo-gas (211-214, 286-292). Gases combine by
    random overlap with resorting and rebinning (216-237).
  - Transfer is the same plane-parallel, linear-in-τ scheme with band-integrated Planck functions (294-323).
  - `fluxes_nonlte` treats the CO2 15 µm bands (500–820 cm⁻¹) above 50 Pa as a two-level system,
    S = (J + εB)/(1 + ε), with López-Puertas & Taylor quenching rates (331-401).

### 1.2 Adaptations for a tall, low-gravity column

**Documented.**

- **Gravity falls as GM/r².** Heights come from the geopotential with the exact inversion z = Rφ/(g0R − φ), and each
  layer's mass is Δp/g(z) (thermodynamics.py:112-113, 292-328). The lunar column holds about 5% more air per unit
  area than ps/gs (METHODS.md:42-44). A constant-gravity path is kept for comparison with plane-parallel codes
  (thermodynamics.py:310-313). Test: `test_column_mass_and_gravity` (atmosphere/tests/test_radiative_convective.py:56-67).
- **The direct beam follows straight rays through spherical shells.** Each layer gets an effective cosine that
  reproduces that attenuation, so the adding method stays energy-conserving (shortwave.py:91-127;
  METHODS.md:117-119). For the 1.2-atm lunar column at 288 K this raises ASR by 1.8 W/m² over plane-parallel
  (validation.json:222-226).
- **The adiabat is non-dilute.** It holds from vapour-poor air to steam (thermodynamics.py:178-216; tests :41-54).
  Lunar gravity puts about six times more vapour over each pascal (README.md:66-72).
- **The correlated-k nodes reach 0.1 Pa**, about 575 km up on the Moon. They are sampled finely enough for Doppler
  cores, and half the g-points lie in the line cores that cool the thin upper layers (METHODS.md:139-154).
- **Moon values:** R and GM from `shared/constants.json`; 1.2 atm with Earth's O2 partial pressure of 21.2 kPa
  (17.5% O2) and Earth's Ar/N2 ratio (thermodynamics.py:148-160). The Earth control runs through the same code.

**Finding.** Layer masses are per unit *local* area: the column keeps a constant cross-section and ignores the
widening of its shells. The ledger records three masses for the design column (`twilight.json`,
`column.mass_kg_m2`):

| Column treatment | Mass per m² of ground |
|---|---|
| This model: flat, GM/r² | 80,278 kg/m² |
| Spherical shells | 84,876 kg/m² |
| PlaSim's constant-gravity ps/gs | 74,861 kg/m² |

This model therefore sits between the GCM's constant-gravity column and the true geometry. The ledger's column stands at a
moist surface pressure of 123,596 Pa against the GCM's dry 121,590 Pa; against its own ps/gs (76,096 kg/m²) the
flat column holds 5.5% more air and the spherical shells 11.5% more over each square metre of ground.

### 1.3 Where the GCM and CM1 work uses it

**Documented.**

- **ExoPlaSim calibration.** The GCM's radiation was calibrated against this model on the GCM's own clear columns:
  the Rayleigh multiplier, the water-vapour continuum and the near-infrared water absorption
  (climate/gcm/README.md:222, :261, :280). The current values are `rayleigh_scale=2.237`, `h2o_continuum=0.004` and
  `sw_water_absorption=1.292` (climate/gcm/exoplasim_run.py:100-112).
- **PlaSim's other radiation fits:**
  - Its CO2 and O2 bands are fitted to this model's direct-beam loss (climate/gcm/README.md:1065-1083).
  - Its longwave is refitted by height against ck.py (README.md:767-797; plasim_longwave.py:219).
  - Its ice optics use this model's two-stream (plasim_ice_optics.py:77, 99, 149).
- **CM1.** RRTMG is checked against this model at the crossing sites (climate/crm/README.md:911-935). The ring
  analyses use ck.py (ring_radiation.py:58; gcm_heating.py:52).
- **Other users:** the twilight ledger (Section 2) is built on its optics and two-stream, and so are the middle
  atmosphere, `climate/lunar_day.py`, `illumination/surface_light` and the spherical sky's optics.

### 1.4 Checks and their evidence state

| Check | Where | What it establishes | Evidence state |
|---|---|---|---|
| PyRADS | validation.json:85-169; METHODS.md:180-187 | Longwave line, continuum, angle and grid handling consistent with an independent code for water–N2 columns | Agreement with an independent code; recorded numbers, no harness in the repository |
| MT_CKD 4.3 port | test_radiative_convective.py:229-236; METHODS.md:61-65 | The port reproduces AER's example output | Reproduction of a reference output, at one spectral point in the committed test |
| Line kernel | test_radiative_convective.py:200-227; METHODS.md:92-94 | The fine/coarse/FFT line sum equals a direct Voigt sum | Test against direct summation |
| CO2 node table | test_radiative_convective.py:266-280; validation.json:240 | Interpolation in ln p and T adds negligible error | Error bound |
| Analytic transfer | test_radiative_convective.py:81-170 | Solvers reproduce analytic limits and conserve energy | Analytic and limiting-case tests |
| Monte Carlo Rayleigh | validation.json:7-84; METHODS.md:120-123 | Size of the two-stream's reflection error | Agreement with an independent method; scratch reference not in the repository |
| Convergence | validation.json:171-238 | Discretisation errors of the standard configuration | Numerical convergence for one lunar column |
| ck vs line-by-line | validate_ck.py; results/ck_validation.json; validation.json:241-285; test_middle_atmosphere.py:170-224 | The correlated-k reduction reproduces the line-by-line fluxes and heating | Internal consistency: same spectroscopy on both sides |

**PyRADS (Koll & Cronin 2018, commit of 2024-01-17).**

- Documented: PyRADS was run on its own saturated H2O–N2 profiles from 250 to 360 K at Earth and lunar gravity.
  This model was run on the same profiles with constant gravity, water lines and continuum only, and the same
  diffusivity (validation.json:86).
- Documented: with PyRADS's data choices (MT_CKD 3.2, main isotopologue), OLR agrees within 0.4%. That covers eight
  matched rows: two at Earth gravity (280 and 340 K) and six at lunar gravity.
- Documented: with this model's defaults the difference reaches +2.2%, mostly from the continuum version (+7 W/m² at
  340 K); isotopologues give −2 W/m² (validation.json:169).
- Finding: the record's own rows reach +2.4% (lunar gravity, 360 K: 242.35 against 236.63 W/m²), slightly above
  the stated 2.2%.
- Finding: the check does not exercise GM/r² hydrostatics, CO2, O2, collision-induced absorption, the solar code or
  the spherical beam. The PyRADS runs and comparison script are not in the repository, so the numbers are a record,
  not a rerunnable check.

**MT_CKD example output.**

- Documented: the port "reproduces AER's own example output to 5×10⁻⁷" (METHODS.md:64).
- Finding: the committed test checks the self and foreign coefficients at 497 cm⁻¹ only (300 K, 1013 mb), to 10⁻⁵.

**Monte Carlo Rayleigh.**

- Documented: the two-stream reflectance of a conservative Rayleigh slab over a black ground is low by 0.1–3%
  against a 400,000-photon Monte Carlo (τ = 0.1–1.5, μ0 = 0.25–1). That is "about 0.003 in planetary albedo
  (about 1 W/m²)" (validation.json:83).
- Finding: the Monte Carlo is a "scratch reference" (validation.json:8) and is not in the repository.
- Finding: it stops at τ = 1.5. The lunar column's Rayleigh depth is 0.75 at 550 nm (README.md:69), so roughly 1.7
  at 450 nm and 4 at 360 nm by the λ⁻⁴ law. The error at τ = 1.5, μ0 = 0.25 is already −2.7%, and larger depths are
  untested.
- Finding: the ledger confirms the direction independently. With the Sun overhead, the spherical solver's ground
  takes 1.3% less sunlight than the two-stream's (climate/gcm/README.md:1011-1013).

**Convergence** (one column: 1.2 atm, 288 K, and a saturated 340 K column for the line floor).

- Documented: spectral step, angles, line floor, μ0 nodes, solar levels and solar step each move the budget by less
  than 0.03 W/m².
- Documented: the longwave vertical grid converges at first order, and the standard 70 + 20 levels read OLR about
  0.6 W/m² low (Richardson estimate from 45 + 12, 70 + 20 and 140 + 40 levels; validation.json:238).

**ck against line-by-line.**

- Documented: the comparison columns are moist adiabats with a synthetic warm stratosphere and an ozone layer, up to
  0.1 Pa (validation.json:242).
  - OLR is within 0.4 W/m² at 288 K (Earth 273.99 against 273.98; Moon 230.26 against 230.60), and within 1.4 W/m²
    for a saturated 330 K lunar column.
  - Surface downward longwave is within 0.8–2.9 W/m².
  - The largest net-flux difference at any level is 3.2 W/m² (Earth) and 4.9–5.0 W/m² (Moon).
  - Ozone 9.6 µm heating is within 0.08 K/day.
  - CO2 15 µm heating is within about 5% up to 30 Pa (Earth) and 5 Pa (Moon), and 20–40% off above. The 0.1 Pa
    layer cools 5× (Earth) and 1.6× (Moon) too weakly (validation.json:284).
- Documented tests: OLR within 1 W/m² of the committed sweep at 270 and 300 K (test_middle_atmosphere.py:183-197).
  Overlap conserves the band-mean optical depth (:172-181). The non-LTE source reduces to LTE when collisions
  dominate and cools less where they are rare (:206-224).
- Finding: the k-tables come from the same spectroscopy, so this tests the reduction, not the spectroscopy.
- Finding: the record gives the 5 W/m² net-flux error without its level. ck.py is the target of PlaSim's longwave
  refit by height, whose per-layer corrections reach 12 W/m², most of them 3.6–12 W/m² (climate/gcm/README.md:777-779).
  ck's own per-level error is therefore not negligible against them, and it is not located.

The Earth control is not compared with published runaway limits or clear-sky observations in the record.

### 1.5 Limitations

1. **Plane-parallel longwave and a sunlit-only global mean.**
   - Documented: METHODS.md:104, 124, 207-209.
   - Documented: for the design column at its temperatures, the ledger finds the missing geometry takes in
     10.3 W/m² more sunlight and lets out 16.2 W/m² more infrared, −5.8 W/m² net (climate/gcm/README.md:1003-1016;
     research/decisions.md:369).
   - Finding: neither this model's balance tables (README.md:50-62, 105-114) nor the middle atmosphere's
     (atmosphere/middle_atmosphere/README.md:76-88) carry that net effect. At the columns' 1.6–1.7 W/m² per K it is
     worth about −3.5 K before any cloud response. The GCM's 20-year test with the first ledger's terms moved 0.65 K,
     because its clouds gave most of it back (climate/gcm/README.md:1042-1061).
2. **Composition.**
   - Documented: dry air may hold only N2, O2, Ar and CO2 (thermodynamics.py:126-132).
   - Documented: CO2 and O2 are broadened by air only (optics.py:30; METHODS.md:96-97). There is no CO2
     self-broadening and no CO2–CO2 or CO2–N2 collision-induced absorption; CO2 lines are Voigt to 25 cm⁻¹, with no
     line mixing and no sub-Lorentzian (χ-factor) far wings.
   - Documented: MT_CKD's foreign continuum assumes Earth air as the broadener; the Rayleigh cross-section is Earth
     air's with a small-CO2 correction (spectroscopy.py:402-418); heat capacities are fixed at their 300 K values
     (thermodynamics.py:25-28).
   - Finding: a ppm of CO2 on the Moon is about seven times Earth's column, so band-wing treatment matters more per
     ppm than on Earth. The model is not fit for CO2-rich or non-N2/O2 atmospheres without these additions.
3. **ck node ranges:** 0.1 Pa–3.2×10⁵ Pa, 100–375 K, water fraction 0–0.5 (ck.py:32-34). Findings:
   - Interpolation clamps silently at the node edges (ck.py:182-189), so states beyond them take edge values with no
     warning.
   - Nodes far from Earth-like states are computed on first use (ck.py:125-131, 255-271). That can stall a run for a
     line-by-line node calculation.
   - k-distributions are sampled uniformly in wavenumber within each band, without Planck weighting
     (ck.py:61-65). This is a common simplification; the flux checks absorb it, but it is largest in the widest
     bands (1–350 and 1480–1800 cm⁻¹).
   - CH4 and N2O are absent from ck (line-by-line only, `reduced_gases.py`).
4. **Upper-air cooling.**
   - Documented: ck's CO2 cooling errors above 5 Pa on the Moon. LTE fails above 1–10 Pa; the non-LTE option is a
     two-level approximation whose O quenching rate is uncertain by about a factor of two (ck.py:378-387).
   - Documented: the 0.01 cm⁻¹ line-by-line grid does not resolve the Doppler cores that upper-air cooling needs
     (validate_ck.py:11-14).
   - Finding: the step exceeds the full width of CO2 lines at 667 cm⁻¹ below roughly 10 kPa (Doppler half-width
     about 5×10⁻⁴ cm⁻¹ at 200 K; Lorentz half-width about 0.07 cm⁻¹ per atmosphere). The line-by-line model's own
     heating rates in the stratosphere and above are therefore not resolved, even though its OLR is converged (step
     test, validation.json). At its standard grid it should not be the reference for upper-air heating.
5. **Manabe–Wetherald humidity** (thermodynamics.py:163-168), an Earth fit, with stratospheric water at the
   tropopause mixing ratio. Documented as an assumption (METHODS.md:201-203).
   - Finding: PlaSim's calibration used the GCM's own columns, so this affects the inverse-climate sweeps and the ck
     validation columns, not the GCM calibration.
6. **Prescribed isothermal stratosphere** (200 K by default). Documented (METHODS.md:22-26): at 290 K, 150 K
   instead of 200 K lowers lunar OLR by 7 W/m² (README.md:85-88). The middle atmosphere solves for it instead.
7. **Simplified surface and sky:** clear sky; grey Lambertian ground (albedo 0.13); black ground in the longwave
   (longwave.py:43; ck.py:294-310); one global mean, no diurnal cycle (METHODS.md:196-200).
8. **Spectral edges.** Light below 202 nm is omitted (about 0.1 W/m²). TSIS-1 ends at 2730 nm, with a blackbody
   beyond. Light beyond 5 µm (about 1.9 W/m² global mean) is counted as absorbed in the air (METHODS.md:125-127).
   The inverse-climate sweeps carry no ozone (METHODS.md:204-206).
9. **Discretisation:** the two-stream error at large Rayleigh depth (1.4), and an OLR bias of about −0.6 W/m² from
   the standard vertical grid.

### 1.6 Room for improvement, ordered by value

1. **Cross-check the full design column against an independent code.** Compare shortwave and longwave with every
   absorber (CO2, O2, collision-induced, Rayleigh) on identical layers, for example LBLRTM or RRTMG for the
   longwave and a DISORT-based solver for the sunlight. The GCM and CM1 radiation were tuned to this model, and its
   only cross-code check is water-only longwave at constant gravity. The middle atmosphere's
   `radiation_benchmarks.json` format is a ready interface.
2. **Make the recorded checks rerunnable.**
   - Commit the PyRADS harness and the Monte Carlo Rayleigh reference.
   - Extend the Monte Carlo to τ ≈ 5 and to absorbing, spherical cases.
   - Assert the MT_CKD example at more than one wavenumber.
3. **Locate and bound ck's per-level net-flux error** (up to 5 W/m²) on the GCM's own columns, since ck is the
   target of PlaSim's longwave refit. Add Planck-weighted k-distributions or more g-points if the error sits where
   the refit acts.
4. **Carry the ledger's net geometry** into the 1-D balance tables, or give the longwave a spherical-shell option;
   the ledger's `outgoing_infrared` is a starting point.
5. **ck housekeeping:** report clamping when a column leaves the node box, and add CH4 and N2O to ck.
6. **Composition generality for other worlds:** CO2 self-broadening, CO2–CO2 collision-induced absorption,
   χ-factor wings, a general dry-air definition, and a foreign continuum for non-air backgrounds.
7. **Resolution:** a Doppler-resolving line-by-line option as an upper-air heating reference, and more levels or a
   Richardson correction for the 0.6 W/m² OLR bias.

## 2. The curved-air ledger (`climate/gcm/twilight.py`)

### 2.1 What it computes

**Documented.** For one clear design column, the ledger computes three things in five configurations
(twilight.py:1-28, 608-826):

- the sunlight from 360 nm to 5 µm absorbed by the ground;
- the sunlight absorbed in each of 100 layers;
- the infrared leaving the top.

The five configurations are:

| Name | What it is |
|---|---|
| `sphere` | Spherical shells |
| `sphere_shallow` | The sphere's light on the flat column's own layer volumes |
| `pseudo_spherical` | The radiative–convective model's two-stream with its pseudo-spherical beam |
| `flat` | The same two-stream, plane-parallel |
| `plasim` | A copy of PlaSim's clear-sky arithmetic on the design run's levels |

Each is given by solar elevation at the ground point, from −90° to 90°, and integrated over the sphere. The
product is `climate/results/gcm/twilight.json`, schema `terluna.climate.gcm-twilight/1`.

The design column is defined in `illumination/surface_light/model.py:103-111`:

- 1.2 atm of dry air over a 294.9 K surface;
- the middle atmosphere's titania-stack profiles, interpolated between its 288 and 298 K cases;
- Manabe–Wetherald humidity to the tropopause (205 kg/m² of water);
- 100 layers up to 0.1 Pa (575 km);
- sunlight through the titania stack × 0.95;
- ground albedo 0.1.

### 2.2 Method

1. **Optics** (twilight.py:84-141, 210-228).
   - 360–830 nm: the sky model's fine optics at 0.025 cm⁻¹ (`illumination/sky/solved_optics.fine_optics`). Below
     500 nm these are `photolysis.py`'s 1-nm absorbers; above, line-by-line H2O and O2 with continuum and
     collision-induced bands; plus the solved trace gases and Rayleigh scattering.
   - 830 nm–5 µm: the radiative–convective model's shortwave line optics at 0.05 cm⁻¹, through the design sunlight.
   - Longwave: line optics at 0.01 cm⁻¹ (H2O, CO2, continuum, collision-induced).
2. **Channels that keep energy and heights** (`faithful_channels`, 234-287).
   - Band edges (59-61): 10–40 nm wide up to 1250 nm, 50 cm⁻¹ wide beyond.
   - Within each band, wavenumbers are sorted by whole-column absorption and bisected by energy. Bisection continues
     until each group's energy-weighted mean optical depths absorb a direct beam within 1% of the group's sunlight of
     what its members absorb, on slant columns of 0.03–13 vertical columns (231, 262-263).
   - Above 1250 nm a group must also keep, within the same 1%, the beam's loss above the bottom of every layer
     (268-277, 293-297). Below 500 nm each band is one channel.
   - Result: 10,697 channels (climate/gcm/README.md:975-977).
3. **Spherical multiple scattering** for the 282 channels below 1250 nm whose whole-column absorption depth is
   under 3 (299; 58, 63).
   - Solver: `illumination/sky/solved_transport.solve` at 'standard' quality, ground albedo 0.1, in batches of 24
     (304-328).
   - It works by successive scattering orders through the spherical shells, with a scalar Rayleigh moment operator
     and a finite solar disk for attenuation. Orders continue until the newest adds less than 2×10⁻⁵, with a cap of
     100 (solved_transport.py:1-7, 154-204).
   - `field()` (346-372) takes the diffuse field as the retained series less its last order (357) and the beam from
     the solver's own table. It integrates each layer's absorption per unit ground area with the shells' widening
     (r/R)² for `sphere` and without it for `sphere_shallow`.
4. **Direct beam through 100 shells** for the other 10,415 channels (`direct_beams`, 375-394). The diffuse and
   reflected light come from the pseudo-spherical two-stream, i.e. the two-stream less its own direct beam
   (397-433, 656-665). Their twilight below the horizon therefore holds no scattered light (evidence string, 723-726).
5. **Comparators** (397-415, 466-493).
   - Flat and pseudo-spherical two-stream on the same layers; both cast nothing below the horizon.
   - PlaSim's copy with the design run's multipliers (2.215 and 1.356; 53-55) and Earth's magnification.
6. **Sphere integration** (537-571). A per-ground-area quantity x(a) integrates to 2∫x d(sin a), normalised to the
   power the solid disk intercepts, which is the GCM's footing. Results are also split by elevation class: below the
   horizon, 0–10°, above 10°.
7. **Cone vs curved split** (674-677, 761-765).
   - Cone = `sphere` − `sphere_shallow`: the shells widening above each square metre of ground.
   - Curved light = `sphere_shallow` − `pseudo_spherical`: the twilight, the low Sun's side light and the curved
     scattered light.
8. **Longwave escape, traced flat and as shells** (`outgoing_infrared`, 150-207).
   - Setup: isothermal layers at the design column's temperatures, over a black ground.
   - Flat: eight Gauss angles.
   - Shells: rays by impact parameter b, weighted (2π/R²) b db per square metre of ground. Panels close in on the
     ground's limb from inside (rays that reach the ground), with one panel per shell outside it (rays that cross
     the air twice).
   - Each layer's escape divided by (r/R)² gives its escape from the flat layer's volume (199-201). Cone and curved
     escape split as for the sunlight (711-712).
9. **Slant factors and their rational fits** (510-534).
   - Straight rays from the ground through constant-density shells give the slant column over the vertical column
     for a density profile.
   - The fit is (μ + a)/(μ² + bμ + c): exactly 1 overhead, with c = a/m(0) fixed by the horizon value, by least
     squares in the logarithm over 0–90°.

   | Absorber | Line | a | b | c | Horizon factor | Largest error |
   |---|---|---|---|---|---|---|
   | Water | 706 | 0.184013 | 0.170061 | 0.0135932 | 13.54 | 0.30% |
   | Well-mixed air | 707 | 0.491679 | 0.42366 | 0.068844 | 7.14 | 0.08% |

   PlaSim's Earth form is 35/√(1 + 1224μ²).
10. **Mapping onto the models.**
    - GCM: PlaSim's default ten sigma layers, by overlap in σ = p/ps of the design column (452-456, 496-507).
    - CM1: the 100 shells by height (778-784).
    - Terms are tabulated from −40° (73, 703-705) to 90° (167 elevations), per unit sunlight at the beam.

### 2.3 What it records

**Documented** (climate/gcm/README.md:1000-1028; global means at the design column's temperatures, W/m²):

| | Sunlight to the ground | Sunlight to the air | Infrared to space | Net |
|---|---|---|---|---|
| Cone | 0 | +4.0 | +10.5 more | −6.5 |
| Curved light and escape | +1.5 | +4.8 | +5.6 more | +0.7 |
| All | +1.5 | +8.8 | +16.2 more | −5.8 |

- The twilight gives 2.6 W/m² with the Sun below the horizon, 1.4 of it to the ground.
- PlaSim puts nothing above 85 km, where line-by-line puts 4.2 W/m².
- The horizon slant factors are 13.5 (water) and 7.1 (air), against PlaSim's 35.

**Finding.** The daytime curved light is partly a solver difference, not geometry.

- In daylight above 10°, the curved-light term gives the ground −1.10 W/m² and the air +1.88 W/m²
  (`twilight.json`, `curved_light_w_m2.by_sun`).
- With the Sun overhead, where the geometry is not curved, the spherical solver's ground still takes 1.3% less than
  the two-stream's (README.md:1011-1013).
- So part of what the GCM adds by day is the delta two-stream's under-reflection relative to successive-orders
  scattering. That corrects the column PlaSim was calibrated to; it is not a geometric effect. It is defensible, but
  should be named as such.

### 2.4 Correctness checks

**Committed tests** (climate/tests/test_twilight.py):

| Lines | What is checked |
|---|---|
| 28-41 | Channels keep the absorbed beam within 0.01 for slant columns of 0.1–10; one averaged channel absorbs more than its members |
| 44-58 | A channel mixing high and low absorbers fails the height test and is split |
| 61-65 | The sphere integral recovers the disk's power over a black ground |
| 68-76 | The sigma mapping conserves energy |
| 79-91 | The slant path matches direct quadrature along the ray to 10⁻³, and the horizon value √(πR/2H) of an exponential atmosphere to 1% |
| 94-98 | PlaSim's layers add up to its air absorption |
| 108-124 | With the product present: the global means integrate back from the per-elevation tables to 10⁻⁴; channels match the fine grid within 1% in total and, per GCM layer, within 1% of the band's absorption |
| 127-132 | Flat, pseudo-spherical and PlaSim columns cast no light below the horizon; the sphere does |
| 135-142 | Cone + curved = total; the GCM term's global mean reproduces the curved light within 2% |

**Channels vs fine grid by layer** (`reduction_check`, 584-605; numbers from `twilight.json`). Both are run
through the pseudo-spherical two-stream at μ0 = 1, 0.5, 0.2 and 0.05:

| Band | Air, channels vs fine grid | Ground | Largest per-GCM-layer difference |
|---|---|---|---|
| 360–830 nm | +0.4 to +0.8% | −0.06 to −0.13% | 0.1–0.45 W/m² |
| 830 nm–5 µm | +0.17 to +0.21% | −0.2 to −0.6% | 0.5–1.2 W/m² (0.9 with the Sun overhead, README.md:990-991) |

The sky model's own 114 production channels absorb 58% too much above 500 nm with the Sun overhead: 104.5 against
66.2 W/m² (README.md:987-990).

**Checks stated only in the README** (README.md:982-984), not committed as tests:

- The flat longwave side matches the radiative–convective solver within 0.7%.
- A thin shell at 46 km lets out 1.2250 times its flat escape, against the exact 1.2253.
- Finding: the "exact" value matches 1 + √(1 − (R/r)²), the escape of an optically thin, isotropically emitting
  shell relative to a flat layer of the same volume (1.2257 at 46 km, 1.2233 at 45 km).
- With the Sun overhead, `sphere_shallow` and `flat` agree within 0.1% in the air; the ground takes 1.3% less
  (README.md:1011-1013).

**The spherical solver's own record** (illumination/sky/SOLVED_COLUMN.md; illumination/sky/solved_checks.py:84-110;
`illumination/sky/results/solved_sky.json`, `additional_checks`).

- For the Moon's solved column, a spectral Monte Carlo of the photopic diffuse flux at the ground agrees with the
  solver within 1.3% at Sun 90°, 10°, 1°, −6° and −12°. The solver runs low by 0.4–1.3%, 2–4 standard errors.
- Standard and refined grids differ by up to 1.6% in radiance, at −18°.
- The energy audit of a three-channel test grid at 'standard' quality closes to 2.2% (0.8% at 'refined').
- Finding: these describe the solver in the sky product's configuration: visible light, ground flux, Sun no lower
  than −18°. They were not repeated for the ledger's channels, its absorbed energy by layer, its near-infrared
  channels, or Sun elevations down to −40°.

**Evidence state overall.** A runnable calculation with internal-consistency and analytic checks, "without
empirical check" (evidence string, 717-728). No independent spherical radiative-transfer code has been run on the
ledger's terms.

### 2.5 Limitations

1. **`orders_converged = false` and its residual** (`twilight.json`; twilight.py:745). Findings:
   - The batch metadata on the drive (`sky_a6acd69c82efba01_00.npz` … `_11.npz`, `meta`) show the cause. One
     channel of 282, the bluest of batch 1 (366–513 nm), reached the 100-order cap with its last ground increment
     at 2.75×10⁻⁵ of the field, against a 2×10⁻⁵ tolerance. The other 281 converged at orders 8–92.
   - The increments fall by about 0.914 per order. The omitted tail is therefore about 3×10⁻⁴ of that channel's
     ground diffuse field, plus about 3×10⁻⁵ from the dropped last order (twilight.py:357). The effect on the
     ledger's watts is negligible.
   - The README does not record it. The sky product's own pipeline would refuse such a solution
     (illumination/sky/solved_sky.py:87-88) until `solved_checks.py --finish` completes it (solved_checks.py:112-153).
2. **One clear design column at albedo 0.1, applied everywhere.**
   - The shortwave terms are per unit sunlight for one column: 205 kg/m² of water, 294.9 K at the surface, no cloud
     or aerosol. Both models apply them to every column and hour, whatever its humidity, temperature, surface
     pressure or albedo.
   - Only the ground term is scaled by the clear-sky share; the layer terms are added under cloud as well
     (exoplasim_run.py:399-410; cm1_run.py:939-960).
   - Finding: the GCM's global-mean vapour column runs from 138 to 176 kg/m² across the October runs
     (climate/gcm/README.md:1127, 1155), against the design column's 205 kg/m².
3. **No refraction** (README.md:984-985).
   - Finding: by the same Chapman scaling as the air mass, horizontal refraction is about (n0 − 1)√(πR/2H). On the
     Moon that is 3.3×10⁻⁴ × 7.5 ≈ 2.5 mrad, about 0.14°. The formula gives 0.56° for Earth, against the observed
     0.57°.
   - This is small against the terms' −40° to 90° range: it moves the terminator by about 17 minutes at the equator.
4. **T⁴ scaling of the longwave terms.** Each layer's extra escape was computed at the design column's temperatures
   and humidity, and is scaled by the model's own (T/T_design)⁴ (exoplasim_run.py:415-440; cm1_run.py:947, 952-960).
   Findings:
   - This holds the escaping spectrum and the absorber amounts fixed.
   - The Planck function's sensitivity is x/(1 − e⁻ˣ), with x = hcν/kT. It is about 2.1 in water's rotation band
     (300 cm⁻¹, 250 K), 4.8 in the CO2 band (667 cm⁻¹, 200 K) and 5.0 in the window (1000 cm⁻¹, 290 K).
   - The curved escape also depends on humidity, which varies far more between columns than temperature does.
5. **Longwave optics from the 0.01 cm⁻¹ grid** (twilight.py:120-141), with isothermal layers, LTE and a black ground.
   Finding: validate_ck.py:11-14 documents that this grid does not resolve Doppler cores for upper-air cooling, so
   the highest shells' terms inherit that error. The top shell at 0.1 Pa is anomalous: its curved escape is 1.15×
   its curved sunlight, against about 0.5 just below.
6. **Coverage:** 360 nm–5 µm only (light below 360 nm matters only for shields that pass it); top at 0.1 Pa; scalar
   Rayleigh scattering, no polarisation; Lambertian ground.
7. **Scale of the terms.** Finding:
   - The terms are fractions of the ledger's 360 nm–5 µm sunlight: 1,166.67 W/m² at the beam out of 1,174.55 W/m²
     for the design spectrum.
   - PlaSim multiplies them by its full solar flux, gsol0·gdist2 (exoplasim_run.py:384), and CM1 by `solcon`
     (cm1_run.py:939, 944). They are therefore about 0.7% high.
   - CM1's RRTMG also takes the Sun's own spectrum rather than the shielded one (climate/crm/README.md:456).
   - Negligible, but definitional.
8. **Mapping onto the models.** Finding:
   - The GCM receives the terms on the design column's sigma layers (surface 123,596 Pa including vapour), at the
     same sigma in every column, high ground included.
   - CM1 receives them on the design column's fixed heights, so a column with a different temperature profile puts
     them at different pressures.
9. **Cached optics on the drive.**
   - `RUNS` is an absolute path (twilight.py:46).
   - The near-infrared and longwave caches are keyed on column heights and grid settings only (84-89, 127-129), not
     on the spectroscopic inputs or the line code.
   - The sky batches are keyed on `solved_transport.py` but not on `solver.py`, whose transport kernel they use
     (310-312).
   - Finding: a change of HITRAN files or of `spectroscopy.py` would not invalidate cached optics. The product
     records the fine optics by an absolute path in another worktree (`twilight.json` `inputs`:
     `/home/kir/Documents/Projects/terluna-ecology/...`).
10. **The PlaSim comparator is pinned to the design run before the bands:** Rayleigh multiplier 2.215, water
    multiplier 1.356, Earth's magnification (twilight.py:53-55, 466-493). `pseudo_spherical_minus_plasim` describes
    that version, not the current standard (2.237, 1.292, lunar slant factors, CO2/O2 bands).
11. **The exobase check applies only the solar side.**
    - Documented: `atmosphere/middle_atmosphere/curved_light.py` scales the middle atmosphere's 500 nm–5 µm
      heating by `sphere_shallow`/`pseudo_spherical`, by log pressure (curved_light.py:70-76, 103-127). The ratio is
      1.04–1.27, and 1.19 at the 0.3 Pa base. It finds the base 3.6–5.6 K warmer
      (atmosphere/middle_atmosphere/README.md:395-419).
    - Finding: the ledger's own longwave curved escape (`twilight.json` `shells_w_m2` and `longwave.shells.curved`)
      against the curved sunlight gained:

      | Shells | Longwave escape / sunlight gained |
      |---|---|
      | Between 0.15 and 0.35 Pa (511–553 km) | 0.49–0.52 |
      | 149–575 km | 0.79 |
      | 49–149 km | 1.66 |
      | 15–49 km | 1.05 |
      | 0–15 km | 0.83 |

    - Finding: the base warming is therefore an upper estimate. It is roughly halved in LTE, and the non-LTE
      treatments weaken the longwave side. Between 15 and 149 km, where the longwave term exceeds the sunlight term,
      the one-sided scaling gets the sign of the net effect wrong.
    - Finding: the thermal-column runs in that check use `escape.py`'s older configuration: no infrared cooling and
      the 'middle' heating shape (curved_light.py:179-210). The curved bases are not passed on to the limb tracing or
      the loss response.

### 2.6 What the GCM and CM1 take from it, and how

**GCM** (ExoPlaSim 3.4.2, a patched copy on the drive; exoplasim_run.py:743-760).

- **Modes** (752-755):
  - `curved`: the curved light and curved escape;
  - `full`: also the cones on both sides;
  - `path`: the lunar slant factor alone.

  `--twilight full` with `--gas-bands` has been the runner's default since 2026-10-14 (exoplasim_run.py:52-55, 803;
  research/decisions.md:371).
- **Input file** `twilight.dat`, written by `twilight_table` (885-903), in this order:
  - the number of elevations;
  - per elevation: the elevation, the ground term and ten layer terms, per unit sunlight at the beam;
  - the layers' and ground's extra infrared escape (W/m²);
  - the temperatures the escape was computed at.
- **Shortwave**, at the end of `swr` (`twilight_term`, 371-413):
  - The elevation comes from `gmuz`; the `solang` edit keeps the cosine below the horizon (356-364). The terms are
    interpolated linearly in elevation and scaled by zsun = gsol0·gdist2.
  - The ground term, times the clear share Π(1 − dcc·nclouds), and each layer's term are accumulated into the net
    downward flux from the ground up. The energy therefore enters at the top of the column.
- **Longwave**, at the end of `lwr` (`twilight_lw`, 415-440): each layer's and the ground's escape × (T/T_design)⁴,
  accumulated as upward flux to the top.
- **Slant factors:** `ZMLUNAR` (a, b, c) replaces Earth's 35/√(1 + 1224μ²) for the water path (365-369).
  `GAS_EDITS` adds CO2 and O2 bands with `ZMAIRLUNAR` (471; README.md:1065-1083).
- **Results in the GCM:**
  - In the first year, the clear sky lost 5.4 W/m² at the top of the air "as the ledger has it" (README.md:1054).
  - With the first ledger's terms the GCM settled 0.65 K cooler; with the bands as well, 2.9 K cooler.
  - The design case was then reset at a sunlight scale of 0.970, `A28_corrected_970` (README.md:1042-1170;
    research/decisions.md:369-372).

**CM1** (r22 with RRTMG; cm1_run.py:872-960, 1000-1001, 2381-2402).

- **Build and input:** build `moon_omp_twilight` with `var20 = 1`. `terluna_twilight.txt` is written from
  `cm1_term`, plus `cm1_term_cone` in `full` mode. It holds the shells' height edges, the ground and 100 shell terms
  for each elevation, and the shells' and ground's infrared escape and temperatures.
- **After RRTMG, at each column's own solar elevation (below the horizon too):**
  - Each shell's sunlight × `solcon` is shared over the model levels by height overlap, as heating.
  - The ground term × the clear share Π(1 − cldfra) is added to the surface net shortwave.
- **In every column, every hour:**
  - Each shell's escape × (T_level/T_shell)⁴ is applied as cooling.
  - The ground's escape is taken from the downward longwave at the surface, `glw` (cm1_run.py:947).
- **Geometry limits:** shells above the 150 km top are dropped (climate/crm/README.md:335-348). Terrain builds place
  shells by each column's own face heights (README.md:426-431).
- **Results:** in a two-hour test, columns 2–10° past sunset gain 0.016–0.036 K/day of solar heating
  (README.md:347-348). On the 45° N ring the local effect is hundredths of a kelvin; the large-scale effect arrives
  through the GCM state the rings are held to (README.md:389-393).

### 2.7 Room for improvement, ordered by value

1. **Use the infrared side wherever the solar side is used**, starting with the middle-atmosphere exobase check.
   Then pass the corrected 0.3 Pa base to the limb tracing and loss response, or record why not.
2. **Check the below-horizon and low-Sun terms independently.** Run a backward Monte Carlo through the same 100
   shells for a few channels (one blue, one red, one near-infrared beam channel) at −30°, −15°, −5° and 1°,
   comparing absorbed energy by layer and at the ground. These terms are the ledger's new physics and rest on one
   solver.
3. **Make the terms depend on the column state.** Tabulate a few columns spanning the GCM's humidity (about
   140–200 kg/m²), surface temperature and albedo, and interpolate per column. Replace T⁴ with a band-resolved
   Planck scaling and a humidity dependence for the longwave terms.
4. **Separate the solver difference from the geometry** in the daytime curved light, for example by running the
   spherical solver on a very-large-radius column. The GCM could then add the geometry alone.
5. **Finish and record convergence.** Complete the unconverged channel (`solved_checks.py --finish`). Record
   convergence and the reduction residuals in the product and README. Commit the thin-shell and flat-side longwave
   checks as tests.
6. **Fix the caches:** keys that include the spectroscopic inputs and every solver file, configurable cache paths,
   and fine optics recorded by key rather than by an absolute path.
7. **Extend coverage** below 360 nm and above 0.1 Pa if a UV-passing shield or a higher model top is studied. Add
   refraction last (about 0.14°).

## 3. Dependency chain for a runnable ledger

**Steps and cost.** From climate/gcm/README.md:967-973 and the logs on the drive:

| Step | What it does | Cost | numba |
|---|---|---|---|
| `twilight optics` | Near-infrared line optics | About 40 s | Not needed |
| `twilight longwave` | Longwave line optics | About 52 s | Not needed |
| `twilight solve` | 12 sky batches of multiple scattering | About 37 min on 6 threads | Needed |
| `twilight ledger` | Builds `twilight.json` | 523 s for the corrected ledger (`ledger_heights.log`) | Needed |

The README's "2.5 minutes" for `ledger` dates from the first ledger, which had 1,504 channels.

**Modules** (Terluna package paths, to go under `python/`):

| Package | Files | Role |
|---|---|---|
| `climate/gcm` | `twilight.py` | The ledger |
| | `exoplasim_run.py` | Imported for `PRODUCTS` and `EXPERIMENTS`; it imports `plasim_ice_optics.py` at module level |
| | `plasim_shortwave.py` | `half_levels`, `net_flux`, `RCOEFF_PER_RAYSCALE` |
| | `plasim_ice_optics.py` | Imported by `exoplasim_run.py` |
| `illumination/sky` | `solved_optics.py` | `fine_optics` |
| | `solved_transport.py` | `solve`, `solar_table`; numba |
| | `solver.py` | `bracket`, `interpolate`, `ray_path`, `transport`; numba |
| | `atmospheres.py`, `colour_matching.py` | Imported along the chain |
| `illumination/cloud_light` | `model.py` | `MolecularColumn`, imported by `solved_optics.py` |
| `illumination/surface_light` | `model.py` | `COLUMNS`, `build`, `sunlight`, `column_facts` |
| `atmosphere/radiative_convective` | `climate.py`, `thermodynamics.py`, `spectroscopy.py`, `optics.py`, `shortwave.py`, `longwave.py`, `ck.py`, `fetch_inputs.py`, `inputs.json` | `ck.py` is imported through the middle atmosphere's `equilibrium.py` |
| `atmosphere/middle_atmosphere` | `equilibrium.py`, `photolysis.py`, `chemistry.py`, `fetch_inputs.py`, `inputs.json` | Column build and photolysis optics |
| `shared` | `constants.py`, `constants.json`, `provenance.py`, `external_inputs.py` | Constants, provenance, fetching |
| `climate/tests` | `test_twilight.py`, `test_plasim_shortwave.py` | The second supplies `SIGMA` and `moist_column` |

**Data products read** (committed in Terluna unless stated):

- `atmosphere/middle_atmosphere/results/`:
  - `middle_atmosphere.json`;
  - `profiles/moon_1.2atm_titania_stack.csv` and `_ts298.csv`;
  - `cases/moon_1.2atm_titania_stack.json` and `_ts298.json`.
- `protection/spectra/shield_transmission.json` (climate.py:25-45).
- `protection/transmission/results/uv_transmission.json`. It is hashed into the fine-optics key
  (solved_optics.py:35-66).
- `climate/gcm/products/moon_gcm_configuration.json`, which supplies gravity (twilight.py:473). It is ignored in
  Terluna and written by `python -m climate.gcm.boundary`, which reads geography products; bring the file itself.
- `research/runs/optical_comfort/spherical/moon_1.2atm_standard.npz` (155 MB, ignored in Terluna). It is the sky
  product's standard solution. It serves as the fine-optics directory, supplies the reduction check's
  production-channel row, and enters the input digest (twilight.py:71, 221, 587-589, 821).

**External inputs** (checked by hash, not committed):

- `atmosphere/radiative_convective/inputs` (about 176 MB): HITRAN H2O/CO2/O2 lines and partition sums, HITRAN
  collision-induced absorption, MT_CKD 4.3, TSIS-1 HSRS. Fetch with
  `python -m atmosphere.radiative_convective.fetch_inputs --download`.
- `atmosphere/middle_atmosphere/inputs`: JPL-2010 cross-sections and quantum yields from MPI-Mainz, and WHI 2008.
  Fetch with `python -m atmosphere.middle_atmosphere.fetch_inputs --download`.
- `atmosphere/radiative_convective/cache`: the CO2/O2 node table, rebuilt on demand.

**Caches** (expensive to rebuild):

| Cache | Size | Note |
|---|---|---|
| `research/runs/optical_comfort/spherical/moon_1.2atm_fine_cf785973b6545596.npz` | 435 MB | The 0.025 cm⁻¹ visible optics. Its key hashes about 25 files at their package paths, the restored input files, and the Python, numpy and scipy versions (solved_optics.py:35-79). A different environment, an edited file (comments included) or a missing file makes the ledger recompute it. |
| `/media/projectspace/terluna-research/gcm-runs/twilight/moon_1.2atm_near_infrared_fe0b783a97b5429e.npz` | 142 MB | Near-infrared optics |
| `.../twilight/moon_1.2atm_longwave_5b5751fd8861bc01.npz` | 108 MB | Longwave optics |
| `.../twilight/sky/sky_a6acd69c82efba01_00.npz` … `_11.npz` | 358 MB in all | The sky batches; `RUNS` is hard-coded (twilight.py:46) |

**Environment.** numba is needed for `solve` and `ledger`. Terluna's environment is
`/media/projectspace/terluna-research/venvs/optics`: Python 3.13, numpy 2.3.3, scipy 1.16.2, numba 0.68.0,
llvmlite 0.50.0. `illumination/sky/requirements.txt` asks for numpy ≥ 2.0 and numba ≥ 0.61.

**Notes for the port.**

- Each module computes `ROOT` relative to itself (twilight.py:43; solved_optics.py:27; surface_light/model.py:55),
  and it resolves to `python/` here. The products and runs above must sit at the same relative paths under it.
- Make `RUNS` configurable before running on any machine other than this one.
