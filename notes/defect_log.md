# Defect log: ExoPlaSim, CM1 with WRF-ELEC, SWAN and SWASH

This log lists the defects found while carrying four Earth-built models to Terluna's breathable Moon, from
2026-09-24 to 2026-10-17. The defects fall into three classes:

- **(a)** upstream defects that the adaptation exposed;
- **(b)** Earth constants, units, geometry and fitted forms written into upstream code;
- **(c)** defects in Terluna's own adaptation and analysis.

A fourth section, **(d)**, lists inconsistencies in Terluna's record that this pass found and that are not yet
corrected there. The companion note `verification_record.md` describes the checks cited below.

## Conventions

**References.**
- Repository paths are Terluna's at commit 186b294. `climate/gcm/exoplasim_run.py:212` means line 212 of that
  file at that commit. The checkout at `/home/kir/Documents/Projects/terluna` (f03b839) differs from 186b294 only in
  `research/integration/five-branches.md`, so its line numbers match.
- Upstream line numbers are those of the pinned sources:
  - CM1 r22.0: `cm1r22.0.tar.gz`, sha256 `05f990bb…6226`.
  - WRF-ELEC: MicroTed/wrf4-elec at `e43041b`.
  - SWAN 41.51: sha256 `325c229f…26bb`, as cited in `climate/waves/audit.md`.
  - SWASH 12.01: sha256 `c8a2e149…397f`.
- ExoPlaSim 3.4.2 is installed from PyPI and its PlaSim source is patched in place, so no pristine line numbers are
  available locally. Its routines are cited by name.
- Run and build folders are on the research drive, `/media/projectspace/terluna-research/`: `gcm-runs/`,
  `crm-runs/` and `cm1/build/`.

**Source marks.**
- **R**: Terluna's documented record. This means a commit message, a README, the decisions register, a data
  product, or a run or build record written by the runners.
- **S**: a finding of the main session's review of 186b294, recorded in this repository's `paper/notes/ideation.md`
  or in the brief for this note. It is not in Terluna's record.
- **V**: found or checked in this pass on 2026-10-17 by reading run records, build records and pristine upstream
  source. No model was run.

**Other terms.**
- "Default" is the runner's default at 186b294.
- An effect is the size the record gives. "Not quantified" means the record gives none.
- Climate numbers are conditional model results: they hold for Terluna's scenario and the models' remaining
  Earth-tuned parts.

## Summary

| ID | Model | Defect | Found | Fix: switch (default) | Effect on results | Status | Src |
|---|---|---|---|---|---|---|---|
| A1 | ExoPlaSim | `solang` Sun clock sweeps 392.5° and skips back 32.5° each model day | 09-29, be50d8b | `NSUNCLOCK` via `sun_clock` (`'synodic'`), 74fed6c | With A2, 328 of 373 W/m² reached 0° E; −8.3% to +17% along the equator | Fixed; reported upstream as ExoPlaSim issue #69 (open) | R |
| A2 | ExoPlaSim | `fixedorbit` default replaces the configured orbit with Earth's for 1 AD (23.695°) | 09-29, be50d8b | `fixed_orbit` (1), 74fed6c | 149 against 29 W/m² at 86°; Earth's seasons carried rain to 60° | Fixed | R |
| A3 | ExoPlaSim | 360-day year of 17,280 steps is not a whole number of 1,430-step model days | 09-29, be50d8b | `whole_lunar_days` (1), 74fed6c | Output means slipped 120 steps a year against the Sun | Fixed | R |
| A4 | PlaSim | Lowest model level reads up to ~20 K too cold in 0.8% of 3-day windows | 09-25, 86bfb63 | None; screen in analyses | Lowest-level analyses only; surface fields unaffected | Open | R |
| A5 | SWAN 41.51 | `KTETA` read uninitialised when depth breaking is off | 10-02, 8785f7e | Always `BREAKING CONSTANT 1.0 0.73` | Repeated Earth runs differed by ~2.5% in Hs; outputs excluded | Avoided, not patched | R |
| A6 | CM1 r22.0 | Thread race: runs on several threads do not always repeat | 10-04, b85eb5c | None; one thread repeats | Paired multithread runs are separate realizations | Open | R |
| A7 | WRF-ELEC | No conduction by default; ion charge persists for weeks in month-long runs | 10-05, e09aa30 | `leakage` (lunar 1), 4499e35 | ~20 kV/m at the ground over the whole box; lightning unchanged | Fixed for lunar runs | R |
| A8 | WRF-ELEC `lightmsz` | Channel reach marked only above threshold `scth` | 10-05, a5205d2 | Flash log takes reach from charge handed to ions | 13 flashes logged no reach | Fixed (logging) | R |
| B1 | CM1 | `g = 9.81` in dynamics, RRTMG, CAPE and Morrison; Morrison fall speeds and caps at Earth's g | 09-27, 16319e1 | `TERLUNA_G` build constant; fall speeds × (g/9.81)^((B+1)/3) | Required for any lunar run | Fixed | R |
| B2 | WRF-ELEC NSSL | `gr = 9.8` twice; fall-speed laws at Earth's g | 10-02 a21a615; 10-04 6027230 | `TERLUNA_G`; same scaling | Required | Fixed | R |
| B3 | WRF-ELEC NSSL | Rain and cloud-ice ventilation tied to Earth fall-speed coefficients | 10-06, 1fa7f41 | Scaled at 11 places; no switch | Lunar rain evaporated 1.3–1.5× too fast | Fixed | R |
| B4 | WRF-ELEC | Breakdown field capped at 180 kV/m | 10-04, bf2fa5e | `lightning` 4 (lunar 4), 62b4c1e | Cap active below ~36 km in lunar air (44% at the ground) | Fixed for lunar runs | R |
| B5 | WRF-ELEC | Ground strike when a channel reaches air warmer than −7 °C; stopping field 0.15 of breakdown | 10-05, 54ea2b2 | Rule kept as upper bound; leader crossing `var1` (lunar 1 kV/m), ac55dc2 | Ground strikes from none to a fifth of flashes | Bounded | R |
| B6 | WRF-ELEC | 0.75-s sub-step tuned to Earth's 500-m layers and fall speeds | 10-04, 13c839e | `substep_s` (lunar 6.8 s) | One 8-s sub-step per step in the boxes | Fixed | R |
| B7 | WRF-ELEC | Other Earth calibrations: 50 MV, 10 kV/m, 0.9/0.8 of breakdown, 200 V/m, NOx yield, Earth conductivity table, laboratory charging laws | 10-04 to 10-05 | Retained; Takahashi law tested | Polarity depends on the charging law | Open | R |
| B8 | CM1 RRTMG | Earth's trace gases, CO₂ by calendar year, ozone profile | 09-27, 16319e1 | Design CO₂ and O₂ compiled in; others zero | Required | Fixed | R |
| B9 | CM1 RRTMG | Uses the Sun's own spectrum, not the shield-filtered one | 09-29, 36e29c4 | None | 5 W/m² of clear-air absorption at 0° E | Open | R |
| B10 | CM1 | Earth-day soil, solar day, damping time and PBL length; Earth's Ω and radius in the beta plane | 09-27, 16319e1; beta plane V | Soil 5–80 cm; `var16`–`var19` Sun; scaled `rdalpha`, `l_inf`; beta plane bypassed | Required; beta plane reaches no result | Fixed or bypassed | R, V |
| B11 | PlaSim | Convective cover counts rain per model day (29.8 Earth days) | 09-25, 86bfb63 | `CONVDAY` via `convective_day_s` (86400) | +0.42 cover; Moon 1.6 K warmer when fixed | Fixed | R |
| B12 | PlaSim | CCM3 cloud water falls off with geometric height on an Earth scale | 09-25, 071f5ce | `CWGREF`, `CWSCALE` via `cloud_water` (`'earth_path'`) | High cloud waterless; Moon 2.5 K warmer when fixed | Fixed | R |
| B13 | PlaSim | Earth's horizon slant factor of 35 (Moon: 13.5 for water, 7.1 for air) | 10-14, 2ac4359 | `ZMLUNAR`, `ZMAIRLUNAR`, with `--twilight` (`full`) | Part of B14; not separated | Fixed | R |
| B14 | PlaSim | Flat, sunlit-only radiation columns | 10-14, 2ac4359 | `NTWILIGHT`, `NTWILW` (`--twilight full`), 55e5020 | −0.65 K over 20 years (first ledger) | Fixed | R |
| B15 | PlaSim | No CO₂ or O₂ in the shortwave bands | 10-14, 6a16d63 | `NGASBANDS` (`--gas-bands`, on), 55e5020 | With B14, 292.0 K (−2.9 K), 7.6% less rain | Fixed | R |
| B16 | PlaSim | Rayleigh coefficient normalised to a 5772 K blackbody; water continuum fitted on Earth | 09-25, 0a33f3c | `RAYSCALE` (2.237), `TH2OC` (0.004): calibration | Uncalibrated run passed 310 K | Calibrated | R |
| B17 | PlaSim | Lacis–Hansen water absorptivity fitted to Earth's water paths | 09-29, be50d8b | `SWH2OSCALE` (1.292): calibration | Air absorbed 8 points too little; fix cut rain 18% | Calibrated | R |
| B18 | PlaSim | Sasamori longwave cools the low air too much and the high air too little | 10-17, a822183 | `NLWCORR` (`--longwave-correction`, off): calibration | With B19, 306.5 K (+11.5 K) | Opt-in; open | R |
| B19 | PlaSim | Liquid-water optics for all cloud | 10-17, 9e30a1f | `NICEOPT` (`--ice-optics`, off) | High cloud's net warming 12.4 → 5.7 W/m² | Opt-in | R |
| B20 | PlaSim | Saturation over liquid at all temperatures; Earth's spacing of the top levels | 10-17, 9e30a1f | None | High cloud starts at 136–149% of ice saturation | Open | R |
| B21 | PlaSim, CM1 | Constant gravity and a thin shell in the dynamics | S | None | Not quantified; g is 5.4% lower at 48.6 km | Open | S, V |
| B22 | CM1 RRTMG | Reference pressures stop at 1053.63 hPa; deeper layers extrapolated | S | None | Lowest ~7 km over the sea extrapolated; not quantified | Open | S, V |
| B23 | CM1 RRTMG | Ice optics end at 140 µm | 10-04, 0b9507d | Size passed to radiation capped at 140 µm and logged | Crash at day 6.45 avoided; capped ice 7% optically too thick in the main run | Mitigated | R |
| B24 | SWAN | AGROW knee fixed at 1 Hz | 10-02, 8785f7e | Patched knee at g/g_ref Hz | Similarity error 5.44% → 0.303% in Hs | Fixed | R |
| B25 | SWAN | Air density fixed at 1.28 kg/m³ | 10-02, 8785f7e | Patched to 1.40390 kg/m³ in the coupled build | Not quantified | Fixed in coupled build | R |
| B26 | SWAN | INIT 2-s period; ST6 and exact-XNL paths at Earth's g; Earth radius default | 10-02, 8785f7e | Bypassed or set by input | None in the selected configuration | Avoided | R |
| B27 | SWAN, SWASH | Earth-calibrated laws: Wu drag, Komen, AGROW coefficient, breaker index 0.73, SWASH breaking 0.6/0.3 | 10-02 to 10-03 | Retained | Not quantified | Open | R |
| B28 | CM1 Morrison | Rain's mean diameter capped at 2.8 mm and breakup begun at 0.3 mm, Earth's values | 10-17 | None | Not quantified; lunar drops held small | Open | S, V |
| C1 | GCM runner | Solar spectrum beyond 2.73 µm held at its last value | 09-25, d73482c | Blackbody tail; band-split guard | 86% of sunlight in the near IR; >320 K | Fixed | R, V |
| C2 | CM1–GCM check | GCM's missing sunlight booked as reflection | 09-29, be50d8b retracts 36e29c4 | Each model's own arriving sunlight | A false "reflects too much" finding | Fixed | R |
| C3 | Twilight ledger | Sky model's channels overstate absorbed energy by 58%; ledger's first channels put near-IR sunlight too high | 10-14, 2ac4359 and 55e5020 | 10,697 channels keeping heights | First two 20-year GCM tests used the old terms | Fixed | R |
| C4 | CM1 set-up | Vapour held constant above the GCM's top level, 6–15× ice-saturated at 140–150 km | 10-17, 9e30a1f | `held_share_above` (new cases) | Persistent 1.1 g/m² of ice above 107 km | Fixed for new cases | R, V |
| C5 | CM1 terrain build | `box_highland` forcing placed by its corner column at 2.9 km | 10-02, 017a2cf | Rewritten in place, 80516a5 (`var13` 3) | Comfort below 1 km 134 → 82 hours | Fixed | R |
| C6 | CM1 box | First `box_0e` forcing lacked the day–night lifting and sinking | 09-28, 1679fd2 | Forcing includes it | Wrong diurnal rain; run stopped at day 47 | Fixed | R, V |
| C7 | CM1 land | Driest land class 0.05 is wetter than the GCM's ground | 09-30, 095e0c5 | Classes to 0.003 (new cases), 3527328 | Land evaporated 0.3–0.5 against 0.1–0.2 mm/day | Fixed for new cases | R |
| C8 | CM1 builds | `moon_omp` never rebuilt at `-O3`; 45° N twilight pair mixed builds | S | None | Twilight effect not separable from realization noise | Open | S, V |
| C9 | WRF-ELEC graft | First version discharged once per 6-s step | 10-04, 13c839e | Sub-steps (`var5`) | Field 3.2× breakdown; 150 C per discharge | Fixed | R, V |
| C10 | WRF-ELEC graft | Fall-speed scaling multiplied uninitialised memory | 10-04, 6027230 | Scaling only where a particle is present | Thread-count-dependent results | Fixed | R |
| C11 | WRF-ELEC graft | OpenMP directive made `infdo` private, so it was unset in threads | 10-04, 6027230 | `infdo` shared | Thread-count-dependent results | Fixed | R |
| C12 | WRF-ELEC graft | Lunar-gravity patch left ventilation at Earth speeds (B3) | 10-06, 1fa7f41 | See B3 | All NSSL runs before 10-06 affected | Fixed | R, V |
| C13 | WRF-ELEC graft | Lunar ground rule (channel within 5 km of the ground) could never strike | 10-05, 54ea2b2 | `ground_m` −1 (da3253f), then leader crossing | Zero ground strikes before 10-05 | Fixed | R |
| C14 | WRF-ELEC graft | Earth benchmarks passed ground height 0, switching ground strikes off | 10-05, 54ea2b2 | Default −1 | 0 against 1.1% negative ground strikes | Fixed | R |
| C15 | Conductivity column | Ion attachment lacked mobility scaling; continuum scaling applied at all heights | 10-05 f197ee3; 10-06 48b9af3 | Mobility scaling added; transition only bracketed | −12% at the ground, −22% at 34 km | Partly open | R |
| C16 | GCM runner | Yearly summary assumed 120 outputs per year | 10-17, 710df23 | `times_per_year` | None | Fixed | R |
| C17 | SWAN pilot | Exception-marked bottom nodes dropped adjacent water nodes | 10-02, f863b67 | Finite negative depths on dry ground; wet-node check | Smoke-run diagnostics rejected | Fixed | R |
| C18 | Records | Seven record errors corrected without code change | various | — | — | Corrected | R, V |

## (a) Upstream defects exposed by the adaptation

The paper (third draft, 2026-10-17) classes these items as follows. A3 (the 360-day calendar) is a limitation in
units of time, avoided by configuration; A7 (WRF-ELEC's missing clear-air conduction) a simplification that holds for
runs of hours; A8 (the flash log's reach threshold) a constant on the lunar path. Its five defects in the released
codes are A1, A2 and B11 (ExoPlaSim's convective-cover unit, classed here under (b)), which produce little or no error
at Earth's values; A5, hidden by SWAN's usual configuration; and A6, CM1's thread race, independent of the world. A4,
PlaSim's cold lowest level, is a fault of uncertain cause.

### A1. ExoPlaSim: `solang`'s Sun clock (R)

- **Defect.** PlaSim's `solang` (radmod.f90) turns the Sun at the planet's rotation rate and restarts its clock
  every model day. The rotation is one turn per 27.32 days and the model day is 29.8 days, so each model day the
  Sun sweeps 392.5° and then skips back 32.5°.
  - The skip is 1/(N − 1) of a turn for a planet whose rotations ExoPlaSim counts as N in a 360-day year: about 1°
    for N near 360 (Earth) and 33° for the Moon's 12.
  - Earth's parameters therefore hide it. It is in ExoPlaSim 3.4.2 and in its current source
    (`climate/gcm/README.md:182-200`).
- **Found** on 2026-09-29 (be50d8b), together with A2. The same commit reran the 0° E radiation check with the GCM's
  own arriving sunlight, 328 of the 373 W/m² due. `climate/gcm/sun_check.py` reproduces the run's longitude pattern
  from `solang`'s arithmetic alone, with correlation 1.0000 (`climate/results/gcm/sun_check_A28_dim5.json`).
- **Fix.** `SUN_EDITS` (`climate/gcm/exoplasim_run.py:248-267`) adds `NSUNCLOCK`:
  - 0, the patch's default, keeps PlaSim's clock;
  - 1 turns the Sun once per model day;
  - 2 is synodic and continuous in time.
  The runner's `sun_clock` defaults to `'synodic'` (`exoplasim_run.py:137`), from 74fed6c.
- **Verified.** In `A28_dim5_sun_test` (two years), sunlight along the equator varies only as 12.1 lunar days a
  year predict, 0.991–1.017 of the mean. Every latitude row gets the Moon's sunlight within 0.1 W/m² rms
  (`sun_check_A28_dim5_sun_test.json`). The arithmetic is unit-tested in `climate/tests/test_gcm_sun_check.py:24`.
  No run checked that `NSUNCLOCK` 0 repeats the unpatched model.
- **Effect.**
  - Along the equator, 270° E–57° E received 8.3% less sunlight and the far side near 164° E up to 17% more.
  - With A2, 0° E received 328 of the 373 W/m² due: about 30 W/m² lost to the sweep and 15 to the tilt
    (`climate/gcm/README.md:213-214`).
  - All runs before 2026-09-29 carry this, including the forcing of CM1 cases set up before that date
    (`research/status.json`, climate topic, unresolved list).
- **Remains.**
  - The runner's comment says "Reported upstream as a bug in solang (README)" (`exoplasim_run.py:251`). The README
    records no report, but one exists: the author opened ExoPlaSim issue #69 on 2026-09-29
    (github.com/alphaparrot/ExoPlaSim/issues/69), "solang: Sun skips back once per model day when rotationperiod ≠ 1",
    which states the condition as a non-synchronous run with `rotationperiod` ≠ 1 and `keplerian=False` and offers a
    fix. It was open with no reply on 2026-10-17 (checked by the main session; found by the literature pass).
  - The Sun's 29.53-day day runs 3.2° per day behind the 29.8-day model day, so day–night analyses sort by `czen`
    (`climate/gcm/README.md:179-181`).

### A2. ExoPlaSim: the `fixedorbit` default discards the configured orbit (R)

- **Defect.** ExoPlaSim uses the obliquity it is given only when `fixedorbit=True` (PlaSim `NFIXORB=1`). With the
  default, PlaSim replaces the namelist's orbit with Earth's orbit for its start year, 1 AD, from Berger's (1978)
  series: obliquity 23.695° and eccentricity 0.0175. It gives no warning, and on Earth the substitution is
  invisible (`climate/gcm/README.md:201-212`).
- **Found** on 2026-09-29 (be50d8b) in PlaSim's logs during the same investigation as A1. Every run's log,
  including the calibration runs', reported Earth's orbit.
- **Fix.** `fixed_orbit` = 1 (`exoplasim_run.py:141`, passed at `:1020`), from 74fed6c.
- **Verified.** The test run's log reports 1.5424° and 0.016715. Its latitude rows follow the Moon's orbit within
  0.1 W/m² rms (`climate/gcm/README.md:210-212`).
- **Effect.**
  - In `A28_dim5`, row-mean sunlight was 4% short at the equator, 6% over at 58° and 29% over at 69°, and
    149 W/m² at 86° against the Moon's 29.
  - Earth's seasons carried summer rain to 60°. With A1 and A2 corrected and the shortwave recalibrated (B17),
    `A28_dim5_moon` against `A28_dim5`:
    - surface 294.9 against 294.3 K;
    - rain 2.24 against 2.91 mm/day;
    - land under 0.5 mm/day 42% against 9%. The Sun and tilt alone, in two years, already gave 36%
      (`climate/gcm/README.md:626-680`).
  - The first radiation calibration (0a33f3c) was fitted on columns from runs with Earth's orbit.
- **Remains.** The CM1 cases set up before 2026-09-29 keep forcing from `A28_dim5` and were not rerun.

### A3. ExoPlaSim: a year that is not a whole number of model days (R)

- **Defect.** ExoPlaSim's year is 360 days, 17,280 half-hour steps. With a 1,430-step lunar model day, a year is not
  a whole number of model days, so the ten output means per model day slipped 120 steps against the Sun each year.
  The runner's first docstring also described the calendar wrongly, as a 357.5-day year (d63ce22; corrected in
  be50d8b).
- **Fix.** `whole_lunar_days` = 1 makes each year exactly 12 model days, 17,160 steps (`exoplasim_run.py:145`,
  `runsteps` at `:1023`), from 74fed6c.
- **Verified.** By the run calendar and the summary's check on output count (`exoplasim_run.py:1213`).
- **Effect.** Not quantified. Analyses that sort by the Sun's position (`czen`) are unaffected. Composites taken by
  output index would drift 2.5 days a year against the Sun (V: 120 half-hour steps).

### A4. PlaSim: a cold artefact at the lowest model level (R)

- **Defect.** In 0.8% of 3-day windows, the lowest model level in the output reads up to about 20 K colder than the
  air near the ground. It most likely comes from converting spectral temperatures to the grid over steep terrain
  (`climate/gcm/README.md:497-501`; 86bfb63, 2026-09-25).
- **Status.** Not fixed. Surface fields are unaffected, and analyses of the lowest level should screen it. It is not
  shown to be specific to the Moon.

### A5. SWAN 41.51: `KTETA` read uninitialised with breaking off (R)

- **Defect.** `SINTGRL` declares `KTETA` as an output (`swancom1.ftn:5706`) but assigns it, through `BRKPAR`, only
  when depth breaking is on (`5944–5949`). With breaking off it still calls `FRABRE` (`6001`), which divides by
  `sqrt(KTETA)` (`swancom2.ftn:1744`). The resulting breaking fraction controls the spectrum limiter
  (`swancom1.ftn:7990`) (`climate/waves/audit.md:68-83`).
- **Found** on 2026-10-02 (8785f7e). Initial runs with `OFF BREAKING` failed the repeatability check: identical
  executables and inputs gave different histories, and a repeated Earth control differed by about 2.5% in Hs at
  some locations. A debug build trapped the undefined read. A diagnostic with quadruplets off, which also disables
  the limiter, repeated exactly.
- **Not Moon-specific.** The Earth control showed it. SWAN's usual configuration keeps breaking on, which hides it.
- **Workaround.** Every run uses `BREAKING CONSTANT 1.0 0.73` (`climate/waves/model.py:103`). The diagnosed
  breaking fraction is checked to stay zero in deep water (`climate/waves/results/waves.json`, `checks`).
- **Verified.** Repeated Earth profiles then matched exactly, and stock and AGROW-patched Earth profiles matched
  (`audit.md:93-94`; `waves.json` `identical_input_repeatability`).
- **Effect.** The non-repeatable outputs were excluded. No reported result used them.
- **Remains.** SWAN itself is not patched for this; with breaking off it still reads the value uninitialised.

### A6. CM1 r22.0: results on several threads do not always repeat (R)

- **Defect.** On one thread a run repeats bit for bit. On four threads, `moon_omp` restarted from `box_0e`'s
  day-10.5 restart once matched and once parted about 85 steps in; the electrified build parted from itself about
  50 steps in (`climate/crm/README.md:80-95`; b85eb5c, 2026-10-04).
- **Search.** On 2026-10-06 (3e85df8, corrected in 0e9642f), runs parted at random 3,000–7,400 s in, always first in
  the domain's total vertical momentum. The plain Morrison box parts too, so at least one race lies outside the
  electrification. The search could not pin it to radiation or large-scale forcing: with about half the runs
  parting, three runs agree by chance about one time in eight (`README:96-110`).
- **Effect.** Paired runs that differ in one setting compare as realizations. For example, the uncapped rerun
  flashed first at day 10.842 against 10.919 (`README:1960-1963`).
- **Remains.** Not located. Single-thread checks and the supercell restart check (on 4 and 2 threads, which did
  repeat) stand.

### A7. WRF-ELEC: no conduction by default (R)

- **Defect.** WRF-ELEC carries no leakage of charge through the air's conductivity unless asked. In hours-long
  Earth storms this matters little. In month-long lunar runs, the charge that evaporating cloud hands to the small
  ions stayed for weeks: 1.9–3.1 kC positive and 2.0–3.7 kC negative through the first lunar night (66a4e3b), and
  11.4 kC net at day 40.5. This held the field at the ground near 20 kV/m over the whole box
  (`climate/crm/README.md:2216-2222`; e09aa30, 2026-10-05).
- **Fix.** `leakage` 1 through stage 1's conductivity column (`var9`), made the lunar default (`LUNAR`,
  `climate/crm/cm1_elec.py:151`; 4499e35).
- **Verified.** Window reruns differing only in leakage:
  - the leftover charge went within the hour;
  - the field at the ground away from storms fell to a median 0.2–1.6 kV/m;
  - the lightning was unchanged: 161 flashes against 144–157.
- **Remains.** The conductivity column is itself uncertain (C15).

### A8. WRF-ELEC `lightmsz`: no reach logged for weak flashes in thin air (R)

- **Defect.** `lightmsz` marks channel points only where a flash takes more than its threshold `scth`. Weak flashes
  high in thin air never reached it: 13 of `box_0e_elec`'s flashes, of 5–72 C starting at 50–68 km, logged no reach
  (`climate/crm/README.md:1689-1693`).
- **Fix.** On 2026-10-05 (a5205d2), the flash log takes a flash's area and levels from where it hands charge to the
  small ions. This changes logging only; the physics is unchanged.

## (b) Earth constants, units, geometry and fitted forms in upstream code

These were found mostly by reading source. Each fix is either a **general repair** (a parameter whose default
reproduces the original, a unit correction, or a scaling law) or a **calibration** (a multiplier or correction fitted
to a reference on the lunar design column), as `paper/notes/ideation.md` defines them.

### B1. CM1: gravity 9.81 in four places, and Morrison fall speeds (R)

- **Defect.** Pristine cm1r22.0 sets `g = 9.81` in four places:
  - `constants.F:113`, the default branch;
  - `module_ra_etc.F:412`, which RRTMG uses to convert pressure to layer mass;
  - `getcape.F:99`;
  - `morrison.F:460` (`G = 9.81`).
  Morrison's fall-speed laws V = A D^B and their caps (`UMR=MIN(UMR,9.1*dum)`, `morrison.F:2153` and four more
  sites; the 1.2 and 20 m/s caps likewise) hold Earth's gravity implicitly.
  - `constants.F` also sets 9.81 in the branches for test cases 4 and 5 (`:82`, `:93`), which Terluna's cases
    (`testcase` 0) do not use (V).
- **Fix** (16319e1, 2026-09-27; `climate/crm/cm1_run.py:715-730`):
  - the four values become the build constant `TERLUNA_G` (GM/R² = 1.6242 m/s² for `moon` builds, 9.81 for
    `earth_g`);
  - Morrison's coefficients and caps scale by (g/9.81)^((B+1)/3), because a regime's Reynolds number grows as the
    Best number, which is proportional to g (`cm1_run.py:62-75`).
- **Verified.** By code tests only: `climate/tests/test_cm1_run.py:145` checks the scaling, and `earth_g` builds keep
  9.81. The gravity-similarity pair meant to test the scaled microphysics never convected (see the verification
  record).
- **Effect.** Required for every lunar run. Cloud droplets fall 6× slower, raindrops 2.9× and graupel 2.3×
  (`climate/crm/README.md:31-36`).

### B2. WRF-ELEC NSSL: gravity 9.8 and fall-speed laws (R)

- **Defect.** WRF-ELEC's NSSL module sets `gr = 9.8` as a parameter and again as an assignment
  (`module_mp_nssl_2mom_elec.F:942`, `:8431`). Its fitted fall-speed laws hold Earth's gravity.
- **Found** in the electricity plan (a21a615, 2026-10-02). **Fixed** in 6027230 (2026-10-04):
  - `gr` becomes the build's gravity;
  - each fitted law scales by (g/9.81)^((b+1)/3), only where the particle is present (`GRAVITY_TEXT` and
    `GRAVITY_PATCH`, `climate/crm/cm1_elec.py:437-487`).
- **Verified.** `test_cm1_elec.py:116`: the scaling acts only where the particle is present and not at Earth's
  gravity. The Earth supercell agrees with CM1's own NSSL twin (verification record).

### B3. WRF-ELEC NSSL: ventilation tied to Earth fall speeds (R)

- **Defect.** Rain's ventilation takes the fixed coefficients `ar` and `ax(lr)` instead of the scaled speeds: in
  `NUCOND`, where rain evaporates, and in the gather-scatter routine (pristine `Sqrt((ar*rhovt(mgs)))` at
  `module_mp_nssl_2mom_elec.F:15500`, `:15539`, `:24210` and more). Cloud ice's ventilation takes a Reynolds number
  fitted on Earth.
- **Found** on 2026-10-06 (1fa7f41) by a code review of the electrified build. The project's first gravity patch had
  missed it (C12).
- **Fix.** Both scale as the fall speeds do, at all 11 sites (`cm1_elec.py:482-487`). There is no switch, and
  nothing changes at Earth's gravity.
- **Verified.** `test_cm1_elec.py:116` asserts that no rain ventilation is left on Earth's coefficients.
- **Effect.** In every NSSL run before `box_0e_elec_corrected`'s restart from day 0:
  - lunar rain evaporated 1.3–1.5× too fast for its drop sizes;
  - the larger ice crystals deposited up to 15% too fast (`climate/crm/README.md:1607-1617`).
  Snow, graupel and hail, and the Morrison scheme, were right.

### B4. WRF-ELEC: the 180 kV/m cap on the breakdown field (R)

- **Defect.** The breakdown field is 284 kV/m × (ρ/1.225 kg/m³), held within 50–180 kV/m
  (`module_discharge_msz.F:674`; `climate/crm/fortran/terluna_lightning.F:28`).
  - On Earth the cap acts below about 4.5 km, beneath where flashes start.
  - In lunar air it acts below about 36 km. It lowers the field by 4% at 34 km, 10% at 30 km, 23% at 20 km and 44%
    at the ground (`climate/crm/README.md:1640-1651`).
- **Found** on 2026-10-04 (bf2fa5e). In `box_0e_elec`'s first lunar day, 84 of 162 flashes started at 32–34 km.
- **Fix.** `lightning` 4 (branched lightning without the cap) is the lunar default (`cm1_elec.py:151`; 62b4c1e). The
  50 kV/m floor stays; it applies above about 100 km.
- **Effect.** In the uncapped rerun, a third of flashes started below 34.8 km against half, with 123 flashes against
  162. The runs are separate realizations (A6).

### B5. WRF-ELEC: the −7 °C ground-strike level and the stopping field (R)

- **Defect.** A downward channel counts as a ground strike when it reaches air warmer than −7 °C in charge of the
  matching sign (`module_discharge_msz.F:2039`). This is about 5 km above Earth's ground but 27–34 km above the
  Moon's. WRF-ELEC's Earth-calibrated stopping field for ground flashes (`elgtfestopcg = 0.15` of breakdown,
  `module_discharge_msz.F:313`) halted every lunar downward channel 15–25 km up (`climate/crm/README.md:2016-2030`).
- **Fix.** 2026-10-05:
  - the −7 °C rule became the lunar default as an upper bound (da3253f);
  - a leader-crossing condition (`var1`, the channel's internal field at sea-level density) requires the leader to
    keep its streamer zone's potential down to the ground. 1 kV/m is the lunar default (f197ee3, ac55dc2).
- **Effect.**
  - Under the stopping field, no ground strikes (lower bound).
  - Under the −7 °C rule on days 40.5–42, 21 of 144 flashes (upper bound).
  - The leader crossing passes 82–100% of those at 1–3 kV/m and half at about 10 kV/m.
  - The main run had a fifth of its 530 flashes as negative ground strikes (94082be).
- **Remains.** The 1 kV/m value is the literature's central value for a thermalised leader, not a lunar measurement.

### B6. WRF-ELEC: the 0.75-s sub-step (R)

- **Defect.** The 0.75-s sub-step lets graupel settle through about 1% of WRF-ELEC's 500-m layers. In the boxes'
  charging zone (25–35 km) the layers are 2 km deep and graupel falls at 0.44 of Earth's speed.
- **Fix.** `substep_s` 6.8 s for lunar runs (`cm1_elec.py:151`; `terluna_elec.F:62` keeps WRF-ELEC's 0.75 s as the
  default), from 13c839e on 2026-10-04. The driver rounds to whole sub-steps, so the boxes run one 8-s sub-step per
  model step (`climate/crm/README.md:1623-1630`).

### B7. WRF-ELEC: Earth calibrations retained (R)

- **Retained as calibrated for Earth.**
  - The 50 MV and 10 kV/m conditions for a ground strike.
  - The 0.9 and 0.8 fractions of breakdown for starting and propagating a channel.
  - The 200 V/m internal field.
  - The NOx yield per metre times 0.1 (`climate/crm/README.md:1630-1633`).
  - The Earth conductivity table for screening option 1.
  - The laboratory charging laws.
- **Tested.** Takahashi's law (`isaund` 1) against Saunders and Peck (`isaund` 12, the default) on 2026-10-05
  (b5a797a). Flash rates and separated charge were alike, but Takahashi's law inverts the storms' polarity, with the
  main negative charge at 48–58 km.
- **Remains.** The deciding measurement, for fast rimed ice in little cloud water at −5 to −16 °C, is not available
  (0e9642f).

### B8. CM1 RRTMG: Earth's atmospheric composition (R)

- **Defect.** RRTMG sets CO₂ from the calendar year, `co2 = (280 + 90 exp(0.02 (yr − 2000))) × 10⁻⁶`. It also carries
  Earth's CH₄, N₂O and halocarbons, and an ozone profile.
- **Fix** (16319e1). CO₂ and O₂ are compiled in from the forcing GCM run (`TERLUNA_CO2`, `TERLUNA_O2`), and the other
  gases and ozone are set to zero (`cm1_run.py:746-763`). The setup checks the build's compiled air against the
  forcing run and refuses a mismatch (`cm1_run.py:2444-2449`).

### B9. CM1 RRTMG: the unfiltered solar spectrum (R; open)

RRTMG takes the Sun's own spectrum, not the shield-filtered one. At 0° E this accounts for 5 W/m² of the
difference in clear-air absorbed sunlight between CM1 and the GCM (`climate/crm/README.md:927-931`; 36e29c4,
2026-09-29). It has not been fixed.

### B10. CM1: Earth-day settings, and Earth's rotation and radius in the beta plane (R; beta plane V)

- **Fixed in 16319e1:**
  - soil layers of 1–16 cm, sized for Earth's diurnal wave, become 5–80 cm (`cm1_run.py:768`);
  - the solar geometry becomes a lunar day of `var19` seconds at `var17` W/m², starting at hour angle `var18`, with
    the hour angle growing along a ring that wraps the Moon (`var16`) (`SUN_BLOCK`, `cm1_run.py:77-104`). CM1's
    Sun keeps a declination of zero, "equinox sunlight", which ignores the 1.54° tilt;
  - the Rayleigh damping time (300 s) and the PBL asymptotic length (75 m) scale by the gravity ratio
    (`cm1_run.py:2004-2005`).
- **Bypassed, not changed (V).** CM1's beta plane derives its latitude and gradient from Earth's rotation,
  `omega = 2π/86400` (`constants.F:25`), and Earth's radius, 6,370 km (`constants.F:119`). It does so as
  `phi = asin(fcor/2Ω)` and `beta0 = 2Ω cos(phi)/earth_radius` (`param.F:9715-9718`).
  - Terluna's tilted rings overwrite `f2d` after that block (`CORIOLIS_BLOCK`, `cm1_run.py:259-270`).
  - The boxes and latitude rings run on an f-plane (`betaplane` is 1 only for tilted rotating rings,
    `cm1_run.py:1997`).
  - So no Terluna result depends on it. A lunar run that enabled CM1's own beta plane would get Earth's beta.

### B11. PlaSim: convective cover counted per model day (R)

- **Defect.** Slingo's convective cover, 0.245 + 0.125 ln P with P in mm/day and capped at 0.8, divides rain by
  PlaSim's own solar day (`zrfac = solar_day * 1000.0`, rainmod.f90). On the Moon that day is 29.8 Earth days, so
  the formula reads rain about 30× too heavy and adds 0.42 to the cover, up to the cap
  (`climate/gcm/README.md:454-461`).
- **Found** on 2026-09-25 (86bfb63).
- **Fix.** `CONVDAY` (`CONVECTIVE_EDITS`, `exoplasim_run.py:238-247`). `convective_day_s` defaults to 86400; 0 keeps
  PlaSim's behaviour (`:121`).
- **Verified.** `regression_convday_off` and `regression_convday_on` (verification record).
- **Effect.** The Moon settled 1.6 K warmer, 298.0 → 299.6 K, with cover 22% → 20% and cloud effect −7.8 → −5.8 W/m²
  (`climate/gcm/README.md:467-490`).
- **Remains.** Slingo's fit itself remains Earth's. A test with the cover near its floor (`convective_day_s` 2400)
  warmed the Moon by 1.7 K and was not adopted (20ff260).
- **Class (V, 2026-10-17).** The paper's second draft classes B11 with the upstream defects of (a): ExoPlaSim's
  description says it replaced the solar day with 86,400 s in its unit conversions, and this one was left in
  place. Synchronous runs carry it too, since the rotation period still sets the model day there: +0.23 to the
  cover for TRAPPIST-1e's 6.1-day rotation, +0.31 for Proxima Centauri b's 11.2 days
  (`paper/tools/regime_calc.py`). Not yet reported upstream.

### B12. PlaSim: CCM3 cloud water with geometric height (R)

- **Defect.** PlaSim diagnoses the cloud water its radiation sees with CCM3's profile: 0.21 g/m³ at the ground,
  falling off with geometric height on a scale of 700 ln(1 + PW) m. Its heights are computed with the planet's
  gravity (rainmod.f90, `mkclouds`). At a sixth of Earth's gravity, pressure levels stand six times higher, so
  clouds above about 20 km, most of the cover, held almost no water (`climate/gcm/README.md:367-399`).
- **Found** on 2026-09-25 (071f5ce) from the layer-by-layer water paths of run A's final year
  (`climate/gcm/cloud_water.py`).
- **Fix.** `CWGREF` and `CWSCALE` (`RAINMOD_EDITS`, `exoplasim_run.py:221-235`) through `cloud_water`
  (`exoplasim_run.py:115`):
  - `'plasim'` is unmodified;
  - `'earth_path'`, the default, counts heights at Earth's gravity;
  - `'full_column'` is the upper bound.
- **Verified.** `A_patch_check` (verification record).
- **Effect.** The Moon settled about 2.5 K warmer, 295.5 → ~298 K. The cloud effect went from −10.7 to −7.8 W/m². The
  full-column bound settled near 292 K (`climate/gcm/README.md:414-452`).

### B13. PlaSim: Earth's horizon slant factor (R)

- **Defect.** PlaSim stretches the low Sun's water path by Earth's horizon magnification, 35/√(1 + 1224 μ²)
  (radmod.f90, `swr`). The Moon's factor is 13.5 for water and 7.1 for well-mixed air
  (`climate/gcm/README.md:1025-1027`).
- **Found** on 2026-10-14 (2ac4359).
- **Fix.** `ZMLUNAR` (`exoplasim_run.py:365-369`) is set whenever `--twilight` is not `none` (default `full`).
  For CO₂ and O₂, `ZMAIRLUNAR` (`GAS_EDITS`) is set with `--gas-bands` (on by default).
- **Effect.** Included in B14's numbers. The runner's `path` mode, which isolates it, was not run.

### B14. PlaSim: flat, sunlit-only radiation columns (R)

- **Defect.** PlaSim, like RRTMG in CM1, lights a column only while its Sun is above the horizon and treats each
  column as flat layers. In the Moon's tall air (mass-mean height 48.6 km), the curved geometry takes in 10.3 W/m²
  more sunlight and lets out 16.2 W/m² more infrared, 5.8 W/m² net. Twilight puts 1.4 W/m² on the ground with the
  Sun below the horizon (`research/decisions.md:369`).
- **Fix.** `twilight_term`, `twilight_lw` (`TWILIGHT_EDITS`, `exoplasim_run.py:316-441`) and, in CM1, the
  `moon_omp_twilight` hook (`var20`, `cm1_run.py:882-966`). This has been the GCM's default (`--twilight full`)
  since 55e5020. The patch lives only in a separate ExoPlaSim copy outside the repository
  (`exoplasim_run.py:747`).
- **Effect.**
  - 20 years with the first ledger's terms: 0.65 K cooler. The clouds gave back most of the geometry's loss.
  - A sunlight-only branch warmed 3.7 K in four years and was stopped (`climate/gcm/README.md:1042-1063`).
  - In CM1 the local effect is below detection (C8).

### B15. PlaSim: no CO₂ or O₂ in sunlight (R)

- **Defect.** PlaSim's two shortwave bands carry no CO₂ or O₂, so the sunlight their lines take high in the Moon's
  deep column went where the water is.
- **Found** on 2026-10-14 (6a16d63).
- **Fix.** `NGASBANDS` (`GAS_EDITS`, `exoplasim_run.py:471-513`), with fits in
  `climate/results/gcm/shortwave_gases.json`. On by default since 55e5020.
- **Effect.**
  - With B14, 20 years settled near 292.0 K, 2.9 K under the design case, with 7.6% less rain.
  - Holding the design temperature then needed a sunlight scale of 0.970 (3.0% dimming) instead of 0.95
    (`research/decisions.md:370-372`).
  - The layers' misplacement fell from 1.71 to 0.97 W/m² rms (`climate/gcm/README.md:1102`).

### B16. PlaSim: Rayleigh coefficient and water continuum (R; calibration)

- **Defect.** ExoPlaSim derives a Rayleigh coefficient from the spectrum, normalised to a 5772 K blackbody's
  ultraviolet. For the titania-filtered Sun this gives 0.214, too low (V: `MOST_DIAG.00000` of `A_uncalibrated`).
  PlaSim's water continuum `TH2OC` = 0.024 over-absorbs at lunar water paths.
- **Found** on 2026-09-25 (0a33f3c) against the line-by-line model on the GCM's own columns. When warm and moist, the
  clear-sky albedo was 0.203 against 0.248 and the longwave 12 W/m² too low (`climate/gcm/README.md:222-252`).
- **Fix.** Calibration, not a general repair:
  - `RAYSCALE` (`RADMOD_EDITS`, `exoplasim_run.py:206-217`): 1.8, then 2.215 (74fed6c), then 2.237 (55e5020);
  - `TH2OC` 0.004.
- **Effect.** The uncalibrated design case passed 310 K and was still warming (315.5 K at year 12 in
  `gcm-runs/A_uncalibrated/progress.json`, V). The calibrated run A settled at 295.5 K.

### B17. PlaSim: Lacis–Hansen water absorptivity (R; calibration)

- **Defect.** PlaSim's near-infrared band absorbs through Lacis and Hansen's formula fitted to Earth's water paths.
  It levels off toward half the sunlight, so over the Moon's longer paths the air absorbed 7.7–8.2 points of the
  arriving sunlight too little on 11 columns (be50d8b, 2026-09-29).
- **Fix.** Calibration: `SWH2OSCALE` (`SHORTWAVE_EDITS`, `exoplasim_run.py:272-286`), 1.356 (74fed6c), then 1.292
  with the CO₂ and O₂ bands (55e5020).
- **Effect.** The corrected Sun plus this recalibration cut rain by a further 18% (`climate/gcm/README.md:659-666`).
- **Remains.** About 0.19 K of ground in the column's misplaced sunlight remains: water's lines just under the
  tropopause. A pressure exponent on the water path fitted worse at every value below 1 and was rejected
  (`climate/gcm/README.md:1103-1112`).

### B18. PlaSim: Sasamori longwave by height (R; calibration, opt-in)

- **Defect.** Against the correlated-k model on about 2,100 cloud-free 3-day means, PlaSim's broadband longwave is
  9.7–11.9 W/m² too cooling in the lowest two layers and up to 12 W/m² too little cooling aloft. Its own continuum
  and path exponents cannot move this (`climate/gcm/README.md:767-790`).
- **Found** on 2026-10-17 from the heating-by-process diagnostics (a822183).
- **Fix.** `NLWCORR`: an extra escape to space per layer, fitted over land and over sea and scaled with T⁴
  (`LW_CORRECTION_EDITS`, `exoplasim_run.py:518-571`). It is opt-in via `--longwave-correction` (`:1364`), from
  b6171de.
- **Verified.** In-model against its Python copy (verification record).
- **Effect.**
  - One year: the ground warmed 3.0 K and was still warming; the top two levels cooled 7–11 K; high cloud rose from
    20% to 46% of the sky.
  - Twenty years with B19 (`A28_corrected_970_lw_ice`): 306.5 K over years 10–19, 11.5 K above the design case
    (e790666).
- **Remains.** The fit was made on the 295 K design state. Its accuracy at the settled state is unchecked
  (verification record, missing checks).

### B19. PlaSim: liquid-water optics for all cloud (R; opt-in)

- **Defect.** PlaSim gives every cloud liquid water's optics.
- **Fix.** For cloud colder than −38 °C, Ebert and Curry's ice optics through a PIFM two-stream, at Kristjánsson and
  Mitchell's radius for the layer's temperature (`ICE_OPTICS_EDITS`, `exoplasim_run.py:715-739`;
  `climate/gcm/plasim_ice_optics.py`). It is opt-in via `--ice-optics`, from 9e30a1f.
- **Effect.** In one year from the design case, ice halves the new high cloud's net warming, 12.4 → 5.7 W/m²
  (`climate/gcm/README.md:856-875`).
- **Remains.** Below 180 K the radius follows the table's trend, and below 190 K the optics run past the 10 µm that
  Ebert and Curry fitted. The high cloud's range, from its water and crystal size, has not been worked out.

### B20. PlaSim: saturation over liquid, and Earth's top levels (R; open)

- **Defect.** PlaSim reckons saturation over liquid at every temperature, so high cloud starts at 136–149% of ice
  saturation. Its top three σ levels are Earth's pressures. On the Moon the 81–107 km layer spans about 180–204 K, a
  55-fold change in ice saturation (`climate/gcm/README.md:811-822`; 9e30a1f).
- **Status.** Not changed.

### B21. PlaSim and CM1: constant gravity and a thin shell (S; arithmetic V)

- **Defect.** Both models' dynamics use one gravity and a thin shell. The in-house reference models use g(z) = GM/r²
  (`atmosphere/radiative_convective/METHODS.md:43`).
- **Arithmetic (V).** With R = 1,737.4 km, g is 5.4% lower at the air's mass-mean height of 48.6 km
  (`climate/gcm/README.md:963`), 10.6% lower at 100 km, and 15.3% lower at CM1's 150 km top.
- **Status.** The radiative side of the shells' widening enters the GCM through the twilight `full` terms (B14). The
  dynamics are unchanged, and the effect is not quantified.

### B22. CM1 RRTMG: reference pressures stop at 1053.63 hPa (S; verified V)

- **Defect.** RRTMG's longwave and shortwave reference pressures begin at 1053.63 hPa (`module_ra_rrtmg_lw.F:3846`,
  `module_ra_rrtmg_sw.F:3026`). A layer at higher pressure gets index `jp` = 1 and a negative interpolation fraction
  `fp`, which extrapolates linearly in ln p (`module_ra_rrtmg_lw.F:3676-3683`, `module_ra_rrtmg_sw.F:2878-2885`).
- **Arithmetic (V).** At the water level the lunar air stands at 1,215.9 hPa. With a scale height near 51 km at
  290–295 K, the lowest ~7 km over the sea lie beyond the table; less over high ground.
- **Status.** Not changed and not tested separately. RRTMG's excess cooling against correlated-k on the 45° N ring
  (4.5 W/m² in the lowest 1.8 km, 8.5 W/m² at 1.8–6.5 km; 17fa76e) includes this extrapolation along with other
  causes.

### B23. CM1 RRTMG: ice optics end at 140 µm (R)

- **Defect.** RRTMG's ice optics table ends at 140 µm. The NSSL sedimentation driver passed 157 µm and the
  electrified box stopped at day 6.45. Lunar ice falls slowly and grows larger (`climate/crm/README.md:1859-1867`;
  0b9507d, 2026-10-04).
- **Fix.** The size the radiation reads is capped at 140 µm, as CM1's Morrison scheme already caps it.
  `terluna_ice_optics.txt` logs the ice above the cap every ten steps (`fortran/terluna_elec.F`; test
  `test_cm1_elec.py:78`).
- **Effect.** The capped ice reaches the radiation optically thicker than its size gives. In the main electrified run
  the radiation's ice was cut at 140 µm in a third of its mass, at a mean radius of 150 µm above the cap, so the
  radiation saw that ice 7% optically thicker than its size gives (`climate/crm/README.md:2403-2406`; R, found in this
  repository's review after the history pass).

### B24. SWAN: the AGROW knee at 1 Hz (R)

- **Defect.** `SWIND0` reduces AGROW's linear wind source above 1 Hz by a factor in f³ (`swancom3.ftn:1800–1807`).
  The source comments call the knee "mostly arbitrary" (`1714–1723`). A fixed knee breaks gravity similarity when
  frequency bands are rescaled (`climate/waves/audit.md:45-60`).
- **Fix** (8785f7e, 2026-10-02). The frequency entering the reduction becomes f · g_ref/g, so the knee sits at
  g/g_ref Hz (`climate/waves/build.py:68-90`). At the reference gravity the stock behaviour is reproduced.
- **Verified.** The sixfold similarity pair and Earth outputs repeating exactly (verification record).
- **Effect.**
  - The similarity error fell from 5.44% to 0.303% in Hs and from 3.91% to 0.326% in mean period.
  - Lunar heights at the main endpoints changed by at most 0.11%; early growth changed more
    (`climate/waves/first_experiments.md:33-37, 54`).

### B25. SWAN: air density fixed at 1.28 kg/m³ (R)

- **Defect.** SWAN fixes air density at 1.28 kg/m³ (`swanmain.ftn:1740–1743`) and resets the air/water ratio from
  it after parsing (`6624–6627`). `SET RHO` sets only water density.
- **Fix.** In the coupled build, `PWIND(16)` = 1.40390 kg/m³: the mean moist surface density over CM1's equatorial
  water columns near Smythii–Marginis, range 1.38029–1.41668 (`climate/waves/build.py:117-131`;
  `first_experiments.md:84-90`). The strip experiments kept 1.28.
- **Effect.** Not quantified separately.
- **Remains.** The density comes from CM1's near-surface air, which runs warm against the GCM (C8 and the open
  problem in `verification_record.md`).

### B26. SWAN: other dimensional defaults (R)

- **INIT default.** The usual initial spectrum forces a 2-s period when the initial Hs is below 0.05 m
  (`swanmain.ftn:9411–9418`). Bypassed with `INIT ZERO`.
- **ST6 and exact-XNL paths.** The FAN and ECMWF drag paths (`SdsBabanin.ftn90:2305, 2466–2471`) and the finite-depth
  exact-XNL coupling (`mod_xnl4v5.ftn90:8540, 8563`) set Earth's gravity directly. The selected configuration
  bypasses them; they are not patched.
- **Earth radius default.** Spherical geometry defaults to Earth's size. The radius is supplied through
  `COORDINATES SPHERICAL` (`swanpre1.ftn:827–828`).
- **Record.** `climate/waves/audit.md:62-66, 135-140, 158-164`.

### B27. SWAN and SWASH: Earth-calibrated empirical laws (R; open)

- **Retained:**
  - Wu drag (`WINDP1`, `swancom3.ftn:1014–1024`);
  - Komen growth and whitecapping;
  - the AGROW coefficient;
  - the breaker index 0.73 (`swancom2.ftn:3120–3122`);
  - SWASH's breaking onset 0.6 and persistence 0.3 (`climate/waves/runup.md:147-158`).
- **Wu drag.** The GCM-forced runs invert the GCM's stress through Wu's law, so SWAN's friction velocity is the GCM's
  Charnock value at lunar gravity. Wu's Earth calibration therefore enters only the first strip experiment
  (`climate/waves/review.md:21-30`).
- **Remains.** Lunar calibration of these laws is open. `waves.json` records `empirical_validation: "Not
  established"`.

### B28. CM1 Morrison: rain's size limits and breakup (S, V; open)

- **Defect.** Morrison bounds each species' slope parameter (`morrison.F:486-503`, "SIZE LIMITS FOR LAMBDA"). For
  rain, `LAMMINR = 1/2800 µm` caps the mean diameter at 2.8 mm; snow and graupel are capped at 2 mm. Rain's
  self-collection turns to breakup above a mean diameter `D_b` (`morrison.F:2265-2276`), which defaults to 300 µm
  when the namelist's `brkup_db` is zero (`morrison.F:494-498`; `cm1.F:404`). Terluna's runner sets neither
  (V: no `brkup` in `climate/crm/` at 186b294), and the core patches scale fall speeds but leave these bounds.
- **Why it is Earth's.** The largest raindrop that survives its fall scales with the capillary length,
  (σ/(ρ_w g))^½, 2.46 times longer at lunar gravity (`paper/data/regime_calc.json`), and slower drops collide with
  less energy. Earth's caps keep lunar drops small, and small drops evaporate faster.
- **Found** on 2026-10-17 by this repository's main session, reading pristine cm1r22.0. No run tested it.
- **Effect.** Not quantified. It bears on the 85% of falling water that evaporates in the lunar boxes and on the
  rain gap with the GCM.

## (c) Defects in Terluna's own work

### C1. GCM runner: the solar spectrum's tail (R; evidence V)

- **Defect.** The TSIS-1 spectrum ends at 2.73 µm. The runner extended it to 100 µm at its last value, which invented
  an infrared tail.
- **Found** on 2026-09-25, within the first ten model years of run A, which warmed past 320 K with planetary albedo
  0.14 (d73482c).
  - V: `gcm-runs/A_invalid_ir_tail/model/MOST_DIAG.00000` reports 0.1398 of the sunlight below 0.75 µm, against
    0.5021 after the fix.
  - V: that run reached 322.5 K at year 9.
- **Fix.** The spectrum continues as the Sun's 5772 K blackbody (`filtered_spectrum`, `exoplasim_run.py:954`). The
  runner stops if the model's band split falls outside 0.3–0.7 (`:1318`). Tested in `test_exoplasim_run.py:172`.
- **Effect.** The ten invalid years were set aside (`A_invalid_ir_tail`) and run A restarted. No reported result uses
  them.

### C2. CM1–GCM radiation check: missing sunlight booked as reflection (R)

- **Defect.** On 2026-09-29 (36e29c4), the crossing check computed the GCM's reflected sunlight from CM1's arriving
  sunlight (373.5 W/m² over the lunar day). The GCM's own arriving sunlight was about 12% smaller because of A1 and
  A2. The check recorded that the GCM reflects 131 W/m² against line-by-line's 96.
- **Found** the same day (be50d8b) by rerunning with the GCM's own arriving sunlight.
- **Fix.** `arriving = (rst − rsut)` (`climate/crm/radiation_check.py:158`).
- **Corrected result.** The GCM reflects the right share. Its air took 23% against 31% (26 W/m² too little) and its
  ground 51% against 43%. That led to B17.

### C3. Twilight ledger: channel errors (R)

- **First defect.** The sky model's 114 production channels average optical depth over windows and opaque lines.
  With the Sun overhead they absorbed 104.5 W/m² above 500 nm against the fine grid's 66.2, 58% too much. This had
  made PlaSim look 8.7 W/m² short of its calibration (2ac4359; `climate/gcm/README.md:987-991`).
- **Second defect.** The ledger's first channels were bisected on the whole column only. They mixed line cores that
  go dark high up with wings that absorb low down. Above 1,250 nm, with the Sun overhead, they put 19.0 W/m² at
  66–85 km against the fine grid's 10.7, and 27.7 against 35.1 at 35–49 km (`README:993-998`).
- **Found** on 2026-10-14. The first defect was found by the ledger itself (2ac4359), the second by a test of the
  beam's loss above every layer (55e5020).
- **Fix.** 10,697 channels that keep the absorbed energy within 1% and the beam's loss above every layer. The rebuilt
  product agrees with the fine grid within 0.9 W/m² per layer.
- **Effect.**
  - The two 20-year GCM tests (`A28_dim5_moon_geometry`, `A28_dim5_moon_geometry_gases`) ran with the first terms
    and were not rerun. The design case `A28_corrected_970` and later runs use the corrected ledger.
  - The 45° twilight rings on the first terms (`ring_45{n,s}_lsw_twilight`) were paused at day 9 and superseded
    (`climate/crm/README.md:356-360`).
- **Remains (V).** `climate/results/gcm/twilight.json` records `channels.orders_converged: false`: the solve's
  scattering orders did not converge in every batch. The README does not mention it, and its effect is not
  quantified.

### C4. CM1 set-up: the sounding above the GCM's top (R; scope V)

- **Defect.** Above the GCM's top level (130 km), the starting sounding and the nudging reference kept the top's vapour
  while the temperature kept falling. The ring's 140–150 km began 6–15 times saturated over ice. Ice formed within
  three days and stayed at 1.1 g/m² above 107 km in every column through both lunar days
  (`climate/crm/README.md:1197-1209`).
- **Found** on 2026-10-17 (9e30a1f) while selecting cloud-free columns for the radiation check.
- **Fix.** `held_share_above` (`climate/crm/cm1_run.py:2405-2422`, used at `:2487`) keeps the top level's share of ice
  saturation above it. It applies to cases set up from 2026-10-17 and has no switch. Tested in
  `test_cm1_run.py:791`.
- **Effect.** The radiation check took only columns cloud-free below 25 km. The ice's radiative effect on the rings
  is not quantified.
- **Remains (V).** The constant-vapour construction dates from the first CM1 commit (`qv_at` in `cm1_run.py` at
  16319e1, line 532). Every case set up before 2026-10-17 used it. The record documents the supersaturation only for
  the 45° N rings; other cases were not checked.

### C5. CM1 terrain build: `box_highland`'s corner-column forcing (R)

- **Defect.** The first terrain build placed the held upper air, the day–night forcing and the vertical wind by the
  levels of the box's first column, a corner at 2.9 km. So the air was held from 5.3 km above every column's ground,
  and the ring's forcing in its lowest 2.9 km went unused (`climate/crm/README.md:1248-1258`).
- **Found** on 2026-10-02 while writing up the run (017a2cf).
- **Fix.** The terrain build was rewritten in place (80516a5): `TERRAIN_NUDGE`, `ADVECTION_COLUMNS` and `W3_BLOCK`
  (`cm1_run.py:384, 495, 559`), with `var13` 3. There is no switch, so the first run cannot be rebuilt from 186b294.
- **Verified.** The rerun's inputs are byte-identical to the first run's, and the model prints where each forcing
  lands (`README:1338-1350`).
- **Effect** (`README:1360-1380`):
  - air at 2 m within 0.4 °C of the first run's;
  - low ground more humid;
  - comfortable hours below 1 km 134 → 82;
  - the box's total 192 → 183 per lunar day.

### C6. CM1 box: the first day–night forcing (R; run folder V)

- **Defect.** `box_0e`'s first prescribed forcing carried only the advection along the rings. That run rained in the
  mornings, stayed clear and hot in the afternoons, and was stopped at day 47 (`climate/crm/README.md:830-832`).
- **Fix.** The forcing also carries the lifting and sinking of the rings' longest waves (1679fd2, 2026-09-28). The
  stopped run is `crm-runs/box_0e_sideways_only`, 47 segments (V).

### C7. CM1 land: the 0.05 wetness floor (R)

- **Defect.** Each land column takes the nearest of the land-use wetness classes, and the driest class was 0.05. The
  corrected GCM's ground poleward of 45° is drier almost everywhere (median 0.005–0.013), so there the rings' land
  evaporated 0.3–0.5 mm/day against the GCM's 0.1–0.2 (`climate/crm/README.md:742-756`).
- **Found** on 2026-09-30 (095e0c5).
- **Fix.** Classes 0.003, 0.01 and 0.02 in land-use rows 31–33 (3527328; `WETNESS_CLASSES`, `cm1_run.py:1270`). This
  applies to new cases. The three flat rings ran with the floor and were not rerun.

### C8. CM1 builds: `moon_omp` never rebuilt at `-O3`; mixed-build twilight pair (S; verified V)

- **Defect.** On 2026-09-30 (27cde9a) every OpenMP build was moved to `-O3 -march=native` (`OMP_DEFAULT`,
  `cm1_run.py:981`). The record says "every OpenMP build now compiles at `-O3 -march=native`"
  (`climate/crm/README.md:76-78`).
- **Evidence (V).**
  - `moon_omp` was not rebuilt. Its build record has no `optimization` key, its Makefile has `-O2`
    (`cm1/build/moon_omp/src/Makefile:81`), and its executable `e7b9a4a0706891b7` dates from 2026-09-28 09:38.
  - `climate/results/crm/build_check_ring_equator.json` lists `moon_omp` as `-O2`, `e7b9a4a0706891b7`.
  - The 45° N control `ring_45n_corrected` ran all 59 segments on `e7b9a4a0706891b7` (`-O2`), from 2026-10-15 04:39
    to 11:19.
  - Its twilight twin `ring_45n_corrected_twilight` ran on `moon_omp_twilight`, `f51a3ffac2ca09bc`
    (`-O3 -march=native`, built 2026-10-14 12:53), from 2026-10-14 22:37 to 2026-10-15 04:04.
  - The two builds' patched sources differ only in `radiation_driver.F` (the twilight hook) and the Makefile
    (`cm1/build/*/build.json`, `patched`).
  - The record describes the control as "the same rings on the build without the twilight hook" (`README:374`).
- **Effect.**
  - The build check found that the flag change behaves like a last-bit nudge: 0.28–0.32 °C rms in 2-m air after one
    model day, domain means within 0.04 °C (`README:66-70`). On several threads even one executable does not always repeat (A6).
  - The pair's reported twilight effect is 0.013–0.021 K in land 2-m air composites (`README:389-392`). That cannot
    be separated from realization noise, which was not measured. `paper/notes/ideation.md` already carries the
    twilight's local effect as "below detection, with no figure claimed".
  - `ring_45n_corrected_sideways` ran on the same `e7b9a4a0706891b7` as its control, so that comparison is not
    mixed.
- **Remains.** Rerun the control on `moon_omp_twilight` with `var20` 0 (the hook is skipped below 0.5), or measure
  the composite noise floor with nudged twins. Rebuild `moon_omp` or record its flags.

### C9. WRF-ELEC graft: discharge once per step (R; run folders V)

- **Defect.** The first electrified build discharged once per 6-s step, after the step's charging and all its
  sedimentation. WRF-ELEC instead sub-steps the sedimentation and discharges after each sub-step
  (`climate/crm/README.md:1653-1657`).
- **Evidence.** At a step's first discharge the field stood a median 3.2× breakdown, and each discharge removed a
  median 150 C. The first-version runs are `crm-runs/supercell_elec_before_substeps` (`f42c6a76528ab154`) and
  `crm-runs/box_0e_elec_before_substeps` (`ffa3ae3afb406503`, 4 segments) (V).
- **Fix.** Sub-steps (`var5`; WRF-ELEC's 0.75 s by default, 6.8 s lunar), 13c839e, 2026-10-04.
- **Verified.** At a sub-step's first flash the field stands a median 1.20× breakdown with branched lightning. With
  cylinders it stands 1.15×, and a call removes a median 32 C (`README:1798-1812`).

### C10. WRF-ELEC graft: scaling uninitialised memory (R)

- **Defect.** The fall-speed scaling ran wherever graupel might be, including where the scheme had set no graupel
  exponent, so it multiplied by whatever value was left in memory (`climate/crm/README.md:1658-1660`).
- **Found** before the first commit of the build (6027230, 2026-10-04): results changed with the number of threads. A
  build that fills unset reals with signalling NaNs and stops at the first invalid operation located it (`:1663-1665`).
- **Fix.** The scaling acts only where the particle is present (`cm1_elec.py:437-473`; `test_cm1_elec.py:116`).
- **Effect.** No committed result used the faulty build.

### C11. WRF-ELEC graft: the OpenMP directive privatised `infdo` (R)

- **Defect.** The directive made private the fall-speed moments that the driver sets before the loop (`infdo`), so
  each thread's copy was unset (`climate/crm/README.md:1660-1662`).
- **Found** with C10 (6027230).
- **Fix.** `infdo` stays shared (`cm1_elec.py:285-287`). `test_cm1_elec.py:78` keeps every private variable of both
  directives from being set before its loop.
- **Verified.** Restarted at 30 minutes on 4 threads and on 2, the supercell repeats its output fields at 35 and 40
  minutes and its 41 flashes bit for bit (`README:1664-1667`).

### C12. WRF-ELEC graft: ventilation left at Earth speeds (R; run folder V)

- **Defect.** This is the project's side of B3: the lunar-gravity patch of 6027230 scaled the NSSL fall speeds but not
  the ventilation tied to them.
- **Found** on 2026-10-06 (1fa7f41) by a review of 6027230, 13c839e, 0b9507d and 62b4c1e.
- **Effect.** Every NSSL run before that date is affected: `box_0e_elec`, the fine box, and the cap, corona, ground,
  Takahashi, leakage and leader windows. The main run `box_0e_elec_corrected` was restarted from day 0. Its first
  attempt's days 0–7 are kept as `crm-runs/box_0e_elec_corrected_before_ventilation_fix`
  (`906d23664302f2f7`, 7 segments) (V).

### C13. WRF-ELEC graft: a lunar ground rule that could not strike (R)

- **Defect.** The lunar boxes first counted a channel within 5 km of the ground as a strike (`ground_m` 5000;
  13c839e). They kept WRF-ELEC's demand that the channel end in charge of the matching sign, which the lunar storms
  do not hold 5 km up. No lunar flash struck the ground in any run before 2026-10-05 (`climate/crm/README.md:1628-1638,
  2016-2030`).
- **Fix.** `ground_m` −1 (da3253f), then the leader crossing (B5).

### C14. WRF-ELEC graft: Earth benchmarks with ground strikes off (R)

- **Defect.** `lightmsz` applies WRF-ELEC's ground rule only for a ground height below zero. The Earth settings
  passed 0, which leaves only a channel reaching the two lowest levels (`climate/crm/README.md:1528-1531`).
- **Fix.** Default `ground_m` −1 (`cm1_elec.py:131`; 54ea2b2, 2026-10-05). Earth benchmark cases that ran before
  the change keep `ground_m` 0 pinned (ac55dc2).
- **Effect.** The supercell's 7,134 flashes were all in cloud. With the rule there were 7,321 in cloud and 85 negative
  ground strikes (1.1%), the first at 36.8 min.

### C15. Conductivity column: ion attachment (R)

This column is the input to leakage and to the screening layers (`atmosphere/electricity/`).

- **First defect.** The aerosol attachment coefficient lacked mobility scaling at every height. f197ee3 (2026-10-05)
  added it with humidity growth of the aerosol, giving 12% less conductivity at the ground and 22% less at 34 km.
- **Second defect.** That scaling is the continuum regime's, valid only for particles much larger than the ions'
  mean free path, but it was applied at all heights.
- **Status.** 48b9af3 (2026-10-06) records the transition correction only as a bracket: +5–12% at 34 km, +12–25% at
  50 km, +23–45% at 70 km and −1–3% at the ground. The continuum values are kept until stage 3, by the author's
  decision (`research/decisions.md:69`).

### C16. GCM runner: the yearly summary's output count (R)

The yearly summary refused years with other than 120 outputs, which would have failed the 6.5-hourly eddy run. It now
takes the run's own count (`exoplasim_run.py:1203-1213`; 710df23, 2026-10-17). No result was affected.

### C17. SWAN pilot: exception-marked bottom nodes (R)

A geographic smoke run exposed roundoff in interpolating exception-marked bottom nodes, which excluded some adjacent
water nodes. Those diagnostics were rejected. The accepted inputs use finite negative depths on dry ground, and the
reader checks every wet node's depth against the atlas (`climate/waves/audit.md:186-192`; f863b67, 2026-10-02).

### C18. Record errors corrected without code change (R; one V)

| Record | Error | Correction |
|---|---|---|
| d63ce22 runner docstring | Calendar described as a 357.5-day year | be50d8b: 360-day year (A3) |
| c3fa72c | Run A's cloud effect inferred as −4 W/m² | 071f5ce: −10.7 W/m², measured with the clear-sky diagnostic (`climate/gcm/README.md:340-342`) |
| Early GCM README | Column mass | 86bfb63: 7.3× Earth's at 1.2 atm |
| GCM heat tables | `maxt`/`mint` listed as air temperature; they are ground temperature | a394eca (`climate/gcm/README.md:503-508`) |
| 41db634 | Whole warm offset at 45° N credited to the missing sideways transport | a04224f: about a third |
| a5205d2, b5a797a, e09aa30 | Hail charging account, Takahashi share, leftover-charge figures, thunder levels | 0e9642f, 66a4e3b |
| `climate/gcm/README.md:152-155` | Resumed year's "restart and output were byte-identical" | V: restart identical; netCDF output identical in every variable but differs in 12 bytes of HDF5 object-header metadata (verification record) |

## (d) Record inconsistencies found in this pass, not yet corrected in Terluna (V)

- **Upstream report claim.** `climate/gcm/exoplasim_run.py:251` says the `solang` bug was "Reported upstream". The
  claim holds (ExoPlaSim issue #69, opened by the author on 2026-09-29, open and unanswered on 2026-10-17), but
  Terluna's record does not cite the issue. The history pass missed it; the literature pass found it.
- **Twilight convergence flag.** `climate/results/gcm/twilight.json` has `channels.orders_converged: false`. The
  ledger's README section (`climate/gcm/README.md:958-1000`) does not mention it.
- **Unbacked longwave caveat.** `research/plan.md:301-302` says the longwave refit's "layers stray 5–7 W/m² at
  302 K". No product or script holding that comparison was found in the repository or in the research drive's
  `session-tools/`, `climate-targets-runs/` or `gcm-runs/twilight/`.
- **Stale forcing description.** `climate/crm/README.md:37-39` gives CM1's sunlight as the 5% dimmer shield's
  1,173.5 W/m² from `A28_dim5`. The runner's default forcing run is `A28_dim5_moon` (`cm1_run.py:1085`), and the
  corrected rings use 1,198 W/m² from `A28_corrected_970`.
- **Build flags.** `climate/crm/README.md:76-78` (every OpenMP build at `-O3`) does not match the `moon_omp`
  executable (C8).

## Items listed by the main session and checked afterwards

`paper/notes/ideation.md` also lists Earth-fitted drop size limits among the fits used outside their range. The
history pass did not check them; the main session did, and they are entry B28.
