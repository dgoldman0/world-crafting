# Verification record: ExoPlaSim, CM1 with WRF-ELEC, SWAN and SWASH

This note lists every check performed on the adaptations from 2026-09-24 to 2026-10-17, grouped by kind. Each entry
says what the check establishes and what it does not, with its locator and date. The checks that are known to be
missing are listed in section 7.

The companion `defect_log.md` describes the defects these checks found or confirmed, and its conventions apply here.
Terluna references are file:line at commit 186b294, and run and build folders are on the research drive,
`/media/projectspace/terluna-research/`. Source marks:

- **R**: Terluna's documented record.
- **S**: the main session's finding.
- **V**: checked in this pass on 2026-10-17. This pass read run and build records and pristine source, hashed restart
  files and compared one pair of outputs variable by variable. No model was run.

## What each kind of check can establish

| Kind | Establishes | Does not establish |
|---|---|---|
| Identity and regression | A patch at its neutral setting leaves the model's arithmetic bitwise unchanged along the tested trajectory | That the active setting is right, or that paths not exercised are unchanged |
| Arithmetic and implementation | The code computes what its formula states | That the formula is right on the Moon |
| Calibration against the reference models | The calibrated form matches the in-house line-by-line or correlated-k model, within the stated residuals, on the columns it was fitted to | Physical truth. The reference is itself a clear-sky model resting on its spectroscopy, and a fit holds near the fitted state |
| Similarity | Gravity enters the implementation consistently: scaled runs reproduce dimensionless states | That the empirical laws hold at lunar gravity |
| Benchmark | The adapted or grafted code reproduces published behaviour of the same scheme on Earth | Correctness on the Moon |

Reproducibility and calibration are not physical validation. No check below validates a lunar climate, and no such
validation is possible without a lunar climate to observe.

## 1. Identity and regression

### ExoPlaSim

| Check | Compared | Result | Locator | Date | Src |
|---|---|---|---|---|---|
| Resume after `kill -9` | `A_kill`, killed a minute into year 2 and resumed, against the uninterrupted `A_ref` | Year-1 restart identical (V: sha256 `ab6437f143fc6289`). netCDF output identical in all 39 variables and the global attributes; the files differ in 12 bytes of HDF5 object-header metadata (V) | `climate/gcm/README.md:150-155`; `gcm-runs/A_kill`, `gcm-runs/A_ref` | 2026-09-25, d63ce22 | R, V |
| `RAYSCALE` 1 with `TH2OC` 0.024 (patch neutral) | `patch_regression` year 0, from that day's run A restart 9, against `A_uncalibrated` year 10 | Restart identical (V: `999c991bbbe1be13`) | `climate/gcm/README.md:236-239`; `gcm-runs/patch_regression` (run folder named only on the drive) | 2026-09-25, 0a33f3c | R, V |
| Cloud-water patch at `plasim`, clear-sky diagnostic on | `A_patch_check` year 0, from run A's restart 38, against run A's year 39 | Restart identical (V: `58cdae1193733fc4`). The clear-sky diagnostic changes no prognostic field | `climate/gcm/README.md:407-409`; `gcm-runs/A_patch_check` | 2026-09-25, 071f5ce | R, V |
| `CONVDAY` 0 | `regression_convday_off` year 0, from `A_earth_path_clouds` restart 13, against `A_earth_path_clouds` year 14 | Restart identical (V: `21a98f26b2e54808`) | `climate/gcm/README.md:462-465`; `gcm-runs/regression_convday_off` | 2026-09-25, 86bfb63 | R, V |
| `CONVDAY` 86400 against the staged code | `regression_convday_on` year 0 against `A_corrected_clouds` year 0, both from `A_earth_path_clouds` restart 14 | Restart identical (V: `1f028d2bb3bdb88d`). This shows the committed patch equals the staged code that ran `A_corrected_clouds`. It is not an identity with the unpatched model | same; `gcm-runs/regression_convday_on` | 2026-09-25, 86bfb63 | R, V |
| `TOP_INFRARED_EDITS` at zero | `A28_cal_control_patched` against `A28_cal_control`: same restart, different `radmod.f90` hashes | Restart identical (V: `abc63babda5f77bc`) | `climate/gcm/README.md:727-729`; `gcm-runs/A28_cal_control`, `gcm-runs/A28_cal_control_patched` | 2026-10-13, b7f24ea | R, V |
| `ICE_OPTICS_EDITS` with `NICEOPT` 0 | `A28_corrected_970_lwcheck_rebuilt` (twilight copy rebuilt with the ice patch) against `A28_corrected_970_lwcheck` | Restart identical (V: `2e0c1794322c8c46`) | `climate/gcm/README.md:858-861`; `gcm-runs/A28_corrected_970_lwcheck`, `gcm-runs/A28_corrected_970_lwcheck_rebuilt` | 2026-10-17, 9e30a1f | R, V |
| Run key | A run refuses to resume when its settings, rank count, ExoPlaSim version, patched sources or written inputs change | A design property, used throughout | `climate/gcm/exoplasim_run.py` (`run_key`); `climate/gcm/README.md:150-152` | since 2026-09-25 | R |

Each of these identity runs covers one model year, from one restart, on one rank count.

**Patches with no runtime identity run** (V, from the record and a listing of `gcm-runs/`):
- `SUN_EDITS` at `NSUNCLOCK` 0 (74fed6c).
- `SHORTWAVE_EDITS` at `SWH2OSCALE` 1 (74fed6c). For this spectrum the added `max(0.001, …)` cannot bind at 1, so
  identity holds analytically (V). Lacis and Hansen's absorptivity stays below 2.9/5.925 = 0.49, and divided by the
  near-infrared fraction of 0.498 it stays below 0.983.
- `TWILIGHT_EDITS`, `GAS_EDITS` and `LW_CORRECTION_EDITS` with their switches off.
- The move of every run into the separate twilight copy of ExoPlaSim on 2026-10-14 (55e5020). The ice-optics check
  above repeated a year of that copy with all three switches on.

**Code-level tests** check the following (`climate/tests/test_exoplasim_run.py:43, 83, 89-145`):
- every patch applies in order with a distinct marker and changes only marked text;
- the twilight, gas, longwave and ice patches stay out of the shared installation.

### CM1 and the WRF-ELEC graft

| Check | Compared | Result | Locator | Date | Src |
|---|---|---|---|---|---|
| Tilted-ring patches: per-column Sun, Coriolis and vertical wind | Rebuilt CM1 against `ring_80n_lsw`'s first model day, and again with the vertical wind given as a uniform per-column table | Bit for bit, both | `climate/crm/README.md:557-560` | 2026-09-27, 3567c51 | R |
| Large-scale advection by local time (`var11`) | Rebuilt CM1 against `ring_80n_lsw`'s first day | Bit for bit | `climate/crm/README.md:837-838` | 2026-09-28, 13b8b9e | R |
| Supercell restart across thread counts | `supercell_elec` restarted at 30 min on 4 and on 2 threads against its first run | Output fields at 35 and 40 min, and the 41 flashes between, bit for bit | `climate/crm/README.md:1664-1667` | 2026-10-04, 6027230, 13c839e | R |
| Leader crossing on Earth | `supercell_elec_leader_1kv` against `supercell_elec_ground_rule` | Flash log identical to the byte: 7,406 flashes, 85 ground strikes, on 4 threads | `climate/crm/README.md:2326-2330` | 2026-10-05, f197ee3 | R |
| Gravity scaling at Earth's g | Code test that fall-speed scaling is skipped at 9.81 and where a particle is absent, and that no rain ventilation is left on Earth's coefficients | Passes | `climate/tests/test_cm1_elec.py:116` | 2026-10-04, 2026-10-06 | R |
| Inputs of paired cases | `ring_45n_corrected_sideways`, `ring_45n_corrected_gcm_land` and `box_highland_own_height` against their reference cases | Byte-identical except the intended files and switches | `climate/crm/README.md:1136-1137, 1213-1214, 1338-1339`; `climate/tests/test_cm1_run.py:567, 581` | 2026-10-02, 2026-10-16 | R |
| One thread | Repeated single-thread runs | Bit for bit | `climate/crm/README.md:80-81` | 2026-10-04 | R |
| Several threads | `moon_omp` and the electrified build from `box_0e`'s day-10.5 restart on 4 threads | Do not always repeat: an unlocated race (defect log A6) | `climate/crm/README.md:80-110` | 2026-10-04, 2026-10-06 | R |
| Compiler rebuilds | `-O3 -march=native` and a strict variant against `moon_omp` (`-O2`) and two last-bit nudges of it, one model day of `ring_equator` on one thread | Neither rebuild is bit for bit. Every field differs by 0.69–0.97 (strict variant 0.82–0.99) of the larger nudge's difference. 2-m air differs by 0.28–0.32 °C rms; domain means within 0.04 °C | `climate/crm/README.md:49-78`; `climate/results/crm/build_check_ring_equator.json`; `crm-runs/build_check/` | 2026-09-30, 27cde9a | R |

No retained artefact of the two `ring_80n_lsw` checks was found in `crm-runs/` or `session-tools/cm1_smoke/` (V). No
run compares `moon_omp_twilight` with `var20` 0 against the build without the hook. The 45° N twilight pair also
differs in compiler flags (defect log C8).

### SWAN and SWASH

| Check | Compared | Result | Locator | Date | Src |
|---|---|---|---|---|---|
| AGROW patch at the reference gravity | Patched against stock SWAN at Earth's gravity | Earth outputs repeat exactly | `climate/waves/audit.md:54-58`; `climate/waves/results/waves.json` (`checks.earth_output_preserved`) | 2026-10-02, 8785f7e | R |
| Repeatability with breaking on | Identical inputs run twice | Identical, stock and patched | `climate/waves/audit.md:93-94`; `waves.json` (`checks.identical_input_repeatability`) | 2026-10-02, 8785f7e | R |
| SWASH source | Built source against the pinned archive, file by file | Byte-identical. SWASH is unmodified; gravity is an input | `climate/waves/swash_build.py:42-46` | 2026-10-03, 54545a4 | R |

## 2. Arithmetic and implementation checks

### Sun, orbit and ring geometry

| Check | Result | Locator | Date | Src |
|---|---|---|---|---|
| `sun_check` rebuilds `A28_dim5`'s sunlight by longitude from `solang`'s arithmetic alone | Correlation 1.0000. This pins defect A1 on `solang` | `climate/gcm/sun_check.py`; `climate/results/gcm/sun_check_A28_dim5.json`; `climate/gcm/README.md:189-191` | 2026-09-29, be50d8b | R |
| Patched Sun clock and fixed orbit in `A28_dim5_sun_test` (two years) | Equator 0.991–1.017 of its mean, as 12.1 lunar days a year predict. Rows within 0.1 W/m² rms of the Moon's orbit. The log reports 1.5424° and 0.016715 | `sun_check_A28_dim5_sun_test.json`; `climate/gcm/README.md:196-212`; `climate/tests/test_gcm_sun_check.py:24` | 2026-09-29, 74fed6c | R |
| Same, corrected design case | Equator even to 0.1%; rows within 0.1 W/m² rms | `sun_check_A28_dim5_moon.json`; `climate/gcm/README.md:632-634` | 2026-09-29, 28a5b9c | R |
| Tilted ring A, six hours | Sun's elevation within 8 × 10⁻⁷ of the formula; Coriolis parameter within 3 × 10⁻¹² s⁻¹ of 2Ω sin(latitude) | `climate/crm/README.md:561-562` | 2026-09-27, 3567c51 | R |

### CM1 forcing hooks

| Check | Result | Locator | Date | Src |
|---|---|---|---|---|
| Prescribed advection in the 3-D box, two three-hour runs | Heating and moistening arrive at 98% and 99.8% of the amounts expected; the nudging takes back the rest | `climate/crm/README.md:838-840` | 2026-09-28, 13b8b9e | R |
| Terrain forcing at each column's own height | The model prints where each forcing lands. On the first day the air is held from 8.0–8.6 km above sea level, and the valley floor is forced from the ring's lowest level | `climate/crm/README.md:1338-1350`; `climate/tests/test_cm1_run.py:658` | 2026-10-02, 80516a5 | R |
| Sideways-forcing ring, two model hours | Lowest 2 km 0.021 K cooler and 0.015 g/kg drier than the control, as the forcing gives | `climate/crm/README.md:1136-1139`; `session-tools/cm1_smoke/ring_45n_corrected_sideways` | 2026-10-16, 3a308ff | R |
| CM1 twilight hook, two model hours | Columns 2–10° past sunset gain 0.016–0.036 K a day, where RRTMG gives none | `climate/crm/README.md:346-348` | 2026-10-14, 2ac4359 | R |
| CM1 compiled air | Setup refuses a forcing run whose CO₂ and O₂ differ from the build's | `climate/crm/cm1_run.py:2444-2449` | 2026-10-14, 702bdb0 | R |

### Ports and copies of PlaSim's physics

| Check | Result | Locator | Date | Src |
|---|---|---|---|---|
| Ice-optics patch | Its Fortran, compiled as PlaSim compiles, matches the Python copy to nine figures | `climate/gcm/README.md:860`; `climate/tests/test_plasim_ice_optics.py:81` | 2026-10-17, 9e30a1f | R |
| Longwave correction in the GCM (`A28_corrected_970_lwcheck`) | PlaSim's own longwave heating within 0.02 K a day of the Python copy's on cloud-free columns | `climate/gcm/README.md:793-795` | 2026-10-17, b6171de | R |
| Python copy of PlaSim's longwave | Reproduces PlaSim's own heating within 0.01 K a day on average | `climate/gcm/README.md:773-775` (`plasim_longwave.py validate`) | 2026-10-17, b6171de | R |
| Python copy of PlaSim's shortwave | Reproduces the GCM's clear-sky split within 0.4 points on 11 columns, and within 0.5 in the corrected run's first year | `climate/gcm/README.md:283-286`; `shortwave_validate_A28_dim5_sun_test.json`, `shortwave_validate_A28_dim5_moon.json` | 2026-09-29, 74fed6c | R |
| PlaSim heating by process | The processes sum to the diabatic total within 0.02 K a day | `climate/crm/README.md:1186-1187` | 2026-10-17, a822183 | R |
| Twilight ledger | Channels keep absorbed energy within 1%. The flat side is within 0.7% of the radiative-convective solver. A thin shell at 46 km escapes 1.2250× its flat value against the exact 1.2253. The corrected channels are within 0.9 W/m² of the fine grid in every layer. Not every batch's scattering orders converged (V: `twilight.json`, `channels.orders_converged: false`) | `climate/gcm/README.md:975-991`; `climate/tests/test_twilight.py`; `climate/results/gcm/twilight.json` | 2026-10-14, 2ac4359, 55e5020 | R, V |
| ExoPlaSim sea roughness against Charnock's law at lunar gravity, 203,389 open-sea samples | Ratio 1.000000 (0.999999–1.000001, 5th–95th percentile). At Earth's gravity the law would give 6.04× less | `climate/waves/review.md:21-28` | 2026-10-03, bf20d96 | R |

### Electrification

| Check | Result | Locator | Date | Src |
|---|---|---|---|---|
| Field solver and lightning | The potential matches a direct solve on stretched levels to 1 part in 10⁵, and a charged layer between grounded plates to 1 in 10³. Separate tests cover cylinders, branched flashes, ground strikes, the leader crossing and screening | `climate/crm/README.md:1710-1729`; `climate/tests/test_cm1_elec_field.py`, `test_cm1_elec_branched.py`, `test_cm1_elec_screen.py` | 2026-10-04 to 2026-10-05 | R |
| Tower re-solve | A numpy re-solve of the saved charge fields matches the direct solve of the same difference equations | e219b82 | 2026-10-08 | R |

### Waves

| Check | Result | Locator | Date | Src |
|---|---|---|---|---|
| SWAN lunar radius | The same small grid in Cartesian metres and in lunar degrees agrees within 1% in height and period | `climate/waves/audit.md:158-164` | 2026-10-02 | R |
| SWAN energy flux | Small-amplitude narrow-band `Hs² Cg` is conserved to 2% before breaking | `climate/waves/audit.md:171-173` | 2026-10-02 | R |
| SWASH still water and reflection | Still water stays level at 0.5 and 0.25 m, with rest offsets of 4.07 and 0.892 cm. Closed-wall reflection ratio 1.0102 with a 0.776% fit residual | `climate/waves/runup.md:206-209, 214-215`; `climate/waves/results/runup.json` (`controls`) | 2026-10-03, 54545a4 | R |

### Test suite

`make check` on main on 2026-10-17 at 13:55 (the log names no commit; main was then at 186b294, merged at 13:47):
2,430 tests passed and 19 were skipped, and the layer check found 0 violations in 1,039 files. The adaptation tests
all pass (`test_exoplasim_run`, `test_cm1_run`, `test_cm1_elec*`, `test_plasim_*`, `test_twilight`,
`test_gcm_sun_check`, `test_build_check`); `test_waves` skips one. These are code-level checks.
Log: `session-tools/make_check_main_after_integration3.log`.

## 3. Calibration against the reference models

**The reference.** The atmosphere domain's line-by-line model and its correlated-k emulation
(`atmosphere/radiative_convective/README.md:129-135`; 2026-09-24, 4d9280a). Correlated-k reproduces:
- line-by-line OLR within 0.4 W/m² at 288–290 K, and within 1.4 W/m² for a saturated 330 K lunar column;
- surface downward longwave within 0.8–2.9 W/m²;
- CO₂ 15-µm heating within about 5% up to 5 Pa in the lunar column.

Every calibration below is clear-sky. PlaSim's clouds are not calibrated against anything.

| Calibrated or checked | Fitted on | Residual | Beyond the fit | Locator | Date |
|---|---|---|---|---|---|
| `RAYSCALE` 1.8 and `TH2OC` 0.004 | Global-mean columns at 280 and 310 K, from runs that had Earth's orbit (defect log A2) | Albedo within about 0.007; OLR within about ±2 W/m², from +3.4 and −11.8 | — | `climate/gcm/README.md:222-252`; `gcm-runs/cal_*`, `gcm-runs/calibration/` | 2026-09-25, 0a33f3c |
| `SWH2OSCALE` 1.356 and `RAYSCALE` 2.215 | Clear-sky split of arriving sunlight on 11 columns of `A28_dim5` | Air 0.3 points and reflection 0.7 points rms; the air had been 8.1 points short | A 303 K column with 338 kg/m² of vapour: 0.7 points short, from 9.7. A cooler column: 0.2. On 11 new columns of the corrected run, within 0.6 points rms; at 0° E the air takes 31.4%, as line-by-line's does (corrected 2026-10-17 by the technical referee; the product gives 0.3137 against 0.3136) | `climate/gcm/README.md:280-302`; `shortwave_fit_A28_dim5.json`; `radiation_check_A28_dim5_moon.json` | 2026-09-29, 74fed6c, 28a5b9c |
| CO₂ and O₂ bands, with `SWH2OSCALE` 1.292 and `RAYSCALE` 2.237 | The line-by-line pseudo-spherical design column, layer by layer | Layers within 0.97 W/m² rms, from 1.71 as run. 0.19 K of ground is left, from water lines under the tropopause | — | `climate/gcm/README.md:1098-1112`; `shortwave_gases.json`; `shortwave_fit_A28_dim5_lunar.json`; `shortwave_water_A28_dim5.json` | 2026-10-14, 6a16d63, 55e5020 |
| Longwave by height (`NLWCORR`) | About 2,100 cloud-free 3-day means of `A28_corrected_970_heating` (about 295 K), against correlated-k | Each layer's mean error removed over land and over sea. 1–5 W/m² remain column to column, within 2.5 W/m² in every latitude band | Not checked at the settled state near 307 K (section 7) | `climate/gcm/README.md:767-790`; `longwave_A28_corrected_970_heating.json` | 2026-10-17, b6171de |
| CM1 RRTMG (checked, not calibrated) | Clear columns at the 0° E crossing | Within 2.5 points of line-by-line in the reflected, air and ground shares; within 8 W/m² over the lunar day | On 990 cloud-free columns of the 45° N ring, RRTMG cools more than correlated-k: by 4.5 W/m² at 0–1.8 km, 8.5 at 1.8–6.5 km and 10.2 at 6.5–13.7 km | `climate/crm/README.md:911-919, 1173-1180`; `radiation_check_box_0e_small.json`; `radiation_ring_45n_corrected_sideways.json` | 2026-09-29, 36e29c4; 2026-10-17, 17fa76e |
| PlaSim longwave before correction (checked) | 151 cloud-free 3-day means at 47° N | Cools the lowest layer 10.6 W/m² and the next 11.4 W/m² more than correlated-k | — | `climate/crm/README.md:1181-1190`; `gcm_heating_A28_corrected_970_heating.json` | 2026-10-17, a822183 |

**What these calibrations do not establish:**
- the reference's own accuracy (clear sky, its spectroscopy and continuum);
- the cloud radiative effects;
- validity away from the fitted state. The longwave fit made at 295 K was carried to a run that settled near 307 K
  without a refit.

## 4. Similarity tests

| Test | Result | Establishes / does not | Locator | Date | Src |
|---|---|---|---|---|---|
| SWAN sixfold: gravity ÷6; length, depth and duration ×6; frequencies ÷6; compare g Hs/U² and g T/U | Patched SWAN agrees within 0.303% in Hs and 0.326% in mean period, against a 1% criterion. Stock SWAN: 5.44% and 3.91%. The largest peak-period difference is one spectral bin | Gravity is carried consistently through dispersion, Komen input and whitecapping, and DIA, once the AGROW knee is scaled. It does not establish the lunar wind-input physics. Frequency-bin convergence was not tested | `climate/waves/first_experiments.md:33-37`; `climate/waves/audit.md:93-100`; `waves.json` (`checks.gravity_similarity`, `criteria`) | 2026-10-02, 8785f7e | R |
| SWASH linear waves at lunar, 4 × lunar and Earth gravity | Largest amplitude error 1.76% and phase error 0.289% against the dispersion relation | Dispersion and the boundary carry gravity | `climate/waves/runup.md:200-202`; `runup.json` (`controls`) | 2026-10-03, 54545a4 | R |
| SWASH gravity ×4 with the clock ×½ | Linear waveform preserved to 0.000908% of the amplitude | Exact linear similarity | `climate/waves/runup.md:202-204` | 2026-10-03, 54545a4 | R |
| SWASH nonlinear gravity control, with breaking and shoreline motion | 98th-percentile run-up changes by 1.20% and the largest profile height by 0.189%. Single waterline samples differ by up to 0.277 m | Approximate similarity with breaking. It does not establish the breaking coefficients' lunar validity | `climate/waves/runup.md:209-212`; `runup.json` (`shore_controls`) | 2026-10-03, 54545a4 | R |
| CM1 gravity pair (`pair_moon`, `pair_earth`) | Neither design convected; there is no result | CM1's gravity-scaled microphysics has no similarity test (section 7) | `climate/crm/README.md:2508-2528` | 2026-09-27, 16319e1 | R |

## 5. Benchmarks

| Benchmark | Result | Establishes / does not | Locator | Date | Src |
|---|---|---|---|---|---|
| Electrified supercell against CM1's own NSSL twin (`supercell_nssl`) | Largest updraft within 6%, reflectivity within 3.4 dBZ, condensate within 9% (19% by level), graupel within 12%, cloud-ice numbers within a factor of 1.5, final rain within a third. Hail differs by up to a factor of 2, since the two copies are different versions of the scheme | The array reordering and sub-stepped sedimentation leave the storm as CM1's own scheme makes it | `climate/crm/README.md:1742-1754` | 2026-10-04, 6027230 | R |
| The same storm against published runs of the charging and lightning schemes | First flash at 28.5 min (published 27–40). Flash rates and charge per flash within the published range. Net charge densities ±4.7 nC/m³ (published about 1, up to 4). Charging is several times stronger and charge per particle type tens of times larger, traced to cloud-ice numbers | The graft behaves like the published scheme on Earth. No published run puts this scheme in CM1 | `climate/crm/README.md:1755-1778` | 2026-10-04, 13c839e | R |
| Ground strikes under WRF-ELEC's rule | 1.1% of flashes were negative ground strikes, the first at 36.8 min. Published: 99.67% in cloud; a first ground flash at 34 min | — | `climate/crm/README.md:1764`; 54ea2b2 | 2026-10-05 | R |
| 2-km supercell, and WRF-ELEC's own test settings | At 2 km, onset and flash rates hold, with larger overshoot past breakdown at the 90th percentile. In the test settings the storm flashes about twice as often | No output of WRF-ELEC's own run of its test case was at hand to compare | `climate/crm/README.md:1819-1838` | 2026-10-04, 0b9507d | R |
| Conductivity column against Earth's measured fair-weather conductivity | Within 2–8% from 5 to 30 km | The ion chain on Earth. It does not establish the lunar column's aerosol | `atmosphere/electricity/README.md:18` | 2026-10-03, ce6e3d7 | R |
| SWAN | `waves.json` records `empirical_validation: "Not established"`. The Earth strips serve only as controls | — | `climate/waves/results/waves.json` | 2026-10-02 | R |
| ExoPlaSim | No Earth benchmark run is recorded | — | — | — | R |

## 6. Checks that failed or fell short

All of these are in Terluna's record except the last two, which are this pass's findings.

- **SWAN with breaking off** failed repeatability by about 2.5% in Hs. The cause was the uninitialised `KTETA`
  (defect log A5; `climate/waves/audit.md:70-83`).
- **SWAN early growth** is not converged in time step. Halving the step changes Hs by up to 33.2% and mean period by
  17.0% in the first hours. The 48-hour endpoints change by under 0.3% (`climate/waves/first_experiments.md:41-52`).
- **SWASH flume control** with the western spectrum: 5.22% in height and 6.28% in period, against 5% bounds. With six
  layers, 5.62% and 6.74%. With the spacing halved, 4.93% and 5.73%. The irregular-input control stays open
  (`climate/waves/runup.md:219-232`).
- **SWASH eastern case**, four layers against six: 6.75% and 10.66%, against 5% and 10% bounds
  (`climate/waves/runup.md:169-175`).
- **Other wave bounds** the record lists as failed: the local coastal grid and earliest growth; the full-field
  weather time step in small waves; weak-wave spectral edges; later eastern transport; irregular SWASH input height
  and period (`research/status.json`, seas topic, condition list).
- **CM1 reproducibility.** The `-O3` rebuilds are not bit-identical, though they stay within the nudge spread
  (section 1), and CM1 on several threads is not bit-reproducible.
- **Twilight ledger (V).** Its scattering orders did not converge in every batch: `twilight.json` has
  `channels.orders_converged: false`.
- **Kill-and-resume record (V).** The record says the resumed year's output was "byte-identical". That holds for the
  data, not for the file bytes (section 1).

## 7. Checks known to be missing

### The CM1–GCM comparison

- **CM1 against the longwave-corrected GCM.** No CM1 case has been forced from `A28_corrected_970_lw_ice`, or from
  any run with the longwave correction.
  - At 45° N, with the sideways transport imposed, CM1's lowest 1.8 km run 3.7 K above the GCM. About 1.5 K of that
    is attributed to PlaSim's longwave over-cooling (`climate/crm/README.md:1147-1196`).
  - Whether the corrected GCM physics closes that gap is untested.
- **The longwave refit at the settled state.** The correction was fitted at about 295 K and applied in a run that
  settled near 307 K. `research/plan.md:301-302` says its layers stray 5–7 W/m² at 302 K, but no product holding that
  comparison was located (V).
- **The high cloud's range,** from its water and its crystal size, has not been worked out
  (`research/decisions.md:419`). The ice optics below 180 K and for crystals below 10 µm rest on extrapolation.
- **The CM1 twilight pair** has no same-executable control and no estimate of the realization noise in
  second-lunar-day composites (defect log C8; S, V).
- **CM1 forcing from older GCM states,** neither set rerun:
  - cases set up before 2026-09-29 keep `A28_dim5` forcing, with Earth's tilt and the uneven Sun;
  - every case set up before 2026-10-17 keeps the constant-vapour sounding above the GCM's top (defect log C4).
- **The CM1 dry-ground land test** (`ring_45n_corrected_gcm_land`) is set up and smoke-tested but not run.
- **A CM1 ring that makes its own upper vapour** has not been built (`research/decisions.md:419`).
- **An independent GCM** (ROCKE-3D), planned as the check that would settle the CM1–GCM disagreement, has not been run
  (`research/decisions.md:142`).

### Model-level gaps

- **ExoPlaSim runtime identity** of `SUN_EDITS`, `SHORTWAVE_EDITS`, and the twilight copy with its patches off
  (section 1).
- **CM1 MPI builds** remain at `-O2` and are untested against the OpenMP builds (`climate/crm/README.md:76-78`).
- **The CM1 thread race** is not located (`climate/crm/README.md:96-110`).
- **CM1 microphysics similarity.** The gravity pair never convected, and its next design, a prescribed radiative
  cooling, was not built.
- **RRTMG below 1053.63 hPa.** Its extrapolation over the lowest ~7 km over the sea is not tested on its own (defect
  log B22; S, V).
- **RRTMG with the shield-filtered solar spectrum** (defect log B9).
- **WRF-ELEC:** no output of its own test case to compare; the 2-km grid's effect on flash initiation is unchecked;
  no 2-km box wide enough for several storms has been run.
- **SWAN and SWASH:**
  - frequency-bin convergence was not tested (`waves.json`, `criteria.frequency_bin_convergence_tested: false`);
  - Wu drag, the AGROW coefficient, the breaker index and SWASH's breaking coefficients have no lunar calibration.

### Physical validation

Physical validation of any lunar result is impossible: there is no lunar climate to observe.
