# Inventory: ExoPlaSim, CM1 and their surroundings

The state on 2026-10-17, covering:

- Terluna at f03b839, which is 186b294 plus one record file;
- world-crafting's `lab` branch, cut from main at 57c5ec5 and brought up to main's 6c8a68f the same day;
- the research drive as read that day.

Besides reading files, the surveys ran `models/check_patches.sh`, which passed on this branch (applied to its
pinned source, every series reproduces the deployed sources), and small scripts that computed the derived
values and file hashes quoted here.

Line numbers are Terluna's except where a path starts with `models/`, `python/`, `notes/` or `paper/`.

## Locations

| Piece | Terluna | world-crafting | Research drive |
|---|---|---|---|
| ExoPlaSim patches | String edits in `climate/gcm/exoplasim_run.py` (`PATCHES`, `TWILIGHT_PATCHES`, :443-448, :743-746) | `models/exoplasim/patches/`, which reproduce the deployed sources byte for byte | `exoplasim-twilight/`, the patched copy every run imports |
| CM1 patches | String edits in `climate/crm/cm1_run.py` and `cm1_elec.py` | `models/cm1/` series, `fortran/`, `builds.json` | `cm1/build/<label>/`: every label but `moon_omp_o2` built, each with its sources, `build.json` and executable |
| GCM runner | `exoplasim_run.py`, 1,396 lines | — | — |
| CM1 runner | `cm1_run.py`, 2,793 lines; `cm1_elec.py`, 491 lines | — | — |
| Planet and surfaces | `climate/gcm/boundary.py`, which writes the git-ignored `climate/gcm/products/` | — | — |
| Reference and calibration tools | `atmosphere/`, `illumination/`, `climate/gcm/{twilight,plasim_*,sun_check}.py` | Byte-identical copies under `python/`; five entry points still import Terluna modules (`python/README.md`) | Ledger and sky caches; `venvs/optics` (numba) and `venvs/mceq` |
| Analyses and tools around the runners | 16 scripts in `climate/gcm/` besides the runner, the calibration tools among them; 22 in `climate/crm/` besides the runner and `cm1_elec.py` | — | — |
| Runs | `climate/gcm/runs` and `climate/crm/runs`, symlinks to the drive | — | `gcm-runs/` 38 GB, `crm-runs/` 437 GB, `cm1/` 1.7 GB; 738 GB free of 1.8 TB |
| Chains | — | — | Shell scripts in `session-tools/`. The earlier chain scripts are gone from the drive, and their logs remain |
| Records | `progress.json`, `case.json`, `build.json` | `models/exoplasim/runs.json` and `models/cm1/builds.json`, matching each run and build to the patch-series state it compiled | — |
| Environment | `climate/gcm/.venv`: Python 3.13.7, ExoPlaSim 3.4.2, MPI | — | `venvs/optics`: Python 3.13, numpy 2.3.3, scipy 1.16.2, numba 0.68.0 |

## The GCM side

### What the runner does, in order

1. **The patched copy.** The runner puts the twilight copy of ExoPlaSim first on the import path
   (`exoplasim_run.py:758-770`). It applies each patch whose marker is missing, and deletes the compiled
   executables so that ExoPlaSim recompiles (`:773-794`).
2. **The configuration** (`:803-875`), from four sources:
   - the planet record, `climate/gcm/products/moon_gcm_configuration.json`;
   - one of four experiments (`EXPERIMENTS`: A, B, C and A28, `:85-94`);
   - the `MODEL` settings (`:98-145`) with `--set` overrides;
   - the ledger, gas-band and longwave products, whose values and hashes it records.
3. **The inputs** (`:999-1007`):
   - the T21 land mask and surface geopotential (`:934-951`);
   - the two spectrum files and the total flux (`:954-996`);
   - `twilight.dat` (`:885-902`).
4. **The run key** (`:905-911`), hashing the sorted configuration JSON with the bytes of the input files.
   The runner refuses to resume a run whose key has changed (`:1282`).
5. **ExoPlaSim's set-up.** The runner configures ExoPlaSim and edits its namelists (`:1010-1085`).
6. **The years**, run one at a time (`:1302-1326`):
   - **Guards:** at least 3 GB free, the sunlight's split at 0.75 µm between 0.3 and 0.7, and the expected
     number of outputs.
   - **Records:** a summary of each year (`:1203-1241`), written atomically to `progress.json`.
   - **Processes:** a lock, and a process group that takes the MPI ranks down with the runner.
   - **Resumption:** from the last restart, or as a branch from another run's restart.

### Records and cost

- **`progress.json`** holds four things:
  - `configuration`: all of the above, with the run key;
  - `inputs`: the paths, the flux and the land share;
  - `years`: 17 numbers a year;
  - `model_sunlight`: the band split and the Rayleigh coefficient ExoPlaSim derived.
- **Provenance.** Its input paths are absolute and run through whichever worktree started the run, such as
  `terluna-ecology`, and it omits the commit and the runner's hash.
- **Cost.**
  - Year 19 of the design case took 218 s on 4 ranks, and year 19 of the longwave and ice test 278 s.
  - Across Terluna's runs, a year took 2.5–4.7 min on 4–8 ranks.
- **Size.**
  - Output is 50.6 MB a year, or 85.8 MB with the heating diagnostics.
  - Restarts are 7.1 MB a year.
  - A 20-year run folder holds 1.3–2.0 GB.

### The Moon's values in the runner

| Value | Where | In the lab |
|---|---|---|
| 1,430 steps a model day, 10 means a day, 12 days a year, hence 120 means a year | `MODEL`, `:98`; the output check, `:1213` | Derived from the rotation by ExoPlaSim's rule (world_spec.md) |
| 121,590 and 101,325 Pa; 25, 28 and 35% water; the titania stack; a 50 m slab | `EXPERIMENTS`, `:85-94` | Scenario fields |
| O2 at 21,227 Pa, Ar/N2 of 0.00934/0.78084, CO2 at 400 ppm | `:78-80` | Scenario fields, in one recipe for every tool |
| Rayleigh 2.237 and near-infrared water 1.292, copied by hand from the fit product and rounded; the water continuum 0.004, from hand trials | `MODEL`, `:106`, `:112` | Calibration products with envelopes |
| Year 365.25636 d, eccentricity 0.016715 | `:841-842` | World fields |
| The radius divisor of 6,371,000 m, against ExoPlaSim's own 6,371,220 | `:77` | The adapter's convention, with a compatibility setting |
| The 1,361 W/m² total and the 5,772 K tail | `:958-959`, `:983` | Star fields |
| The yearly summary's equatorial and polar bands, \|latitude\| < 12° and > 70° | `:1222-1223` | Diagnostic settings |
| The product paths and the patched copy's folder | `:747-750` | Store keys |

## The CM1 side

### What the runner does

- **Fetch and build** (`cm1_run.py:837-853, 1038-1077`). The runner checks the pinned tarball and copies the
  pristine source.
  - It applies the string patches: the Makefile, the core list, the build's own list and the
    optimisation.
  - It compiles with the gravity, CO2 and O2 as preprocessor constants, and writes `build.json`.
  - A rebuild of any of the fourteen labels (`BUILDS`, `:969-1023`) overwrites its executable and its
    record.
- **Cases** (`CASES`, `:1093-1526`). About fifty cases, each a dict derived from another and given a purpose
  sentence. The kinds:
  - a ring on a circle of latitude or on a tilted great circle;
  - a box: flat, over terrain, or over terrain with sea;
  - the gravity pair;
  - CM1's own samples;
  - windows run again from another case's restart;
  - another case's inputs with a new build;
  - a finer box.
- **Extraction from the GCM** (`:1162-1956`).
  - Reference profiles by band and along a path, the mean vertical wind from the mass budget, the box
    sites, and the sideways forcing through `ring_heat_budget.gcm_sideways`.
  - A box takes its day–night forcing from another case's ring runs, through
    `ring_crossings.day_night_advection`.
- **Surfaces** (`:1607-1863`), from `boundary.lakes_product`, which combines the geography domain's atlas and
  drainage.
- **Settings** (`:1979-2035`):
  - the Rayleigh damping and the boundary layer's length, both scaled with gravity;
  - the Sun in `var16`–`var19`;
  - the nudging heights in `var14` and `var15`;
  - the Coriolis parameter from the rotation.
- **Set-up** (`:2425-2640`). The runner writes the case's input files:
  - `input_sounding`, `input_grid_z`, `lsnudge_0001.dat`;
  - `terluna_surface.txt` or `terluna_surface2d.txt`, `LANDUSE.TBL`;
  - `terluna_wls.txt` or `terluna_wls2d.txt`, `terluna_lsadv.txt`;
  - `perts.dat`, `terluna_twilight.txt`, `namelist.template` and the electrified files.

  It then links the executable and the RRTMG tables and writes `case.json`.
- **Runs** (`:2685-2735`). Segments start from the newest restart, under a lock, a `STOP` file and a
  wall-clock budget, and each one updates `progress.json` atomically.

### Records and cost

- **`case.json`** holds:
  - the configuration as written and the grid;
  - a full copy of `build.json`;
  - the GCM run, named by run name and years;
  - the reference profiles and forcing summaries;
  - the runner's hash and the hashes of the input files.

  The GCM run's key is left out.
- **Format.** The format has changed between versions, and the runner's hash is the only marker of which
  version wrote a record. `box_jura`'s record, written from another worktree, lacks the `sideways` key that
  `setup` writes today.
- **Cost.** Summed from the segments in each case's `progress.json`, over two lunar days, on 4–8 threads
  where recorded:
  - rings took 1.8–12.3 wall hours, in proportion to their length, from the 80° rings to the tilted and
    equatorial ones;
  - boxes took 2.3–27.2 hours, from the quarter-size land tests to the electrified box;
  - the 45° N twilight ring ran as 59 one-day segments of about 275 s each on 6 threads, 4.5 hours in all.
- **Size.** That ring wrote 8.5 GB, and the Jura box 54 GB: 37 GB of output and 17 GB of restarts.

### The Moon's values in the runner

| Value | Where |
|---|---|
| The default reference run `A28_dim5_moon` (years 20–29), from before the corrected radiation | `GCM_RUN`, `:1085`; `CORRECTED_GCM` = `A28_corrected_970` (10–19), `:1150` |
| A build's air, read from that run's `progress.json` at build time. The 45° N twilight ring's build holds `A28_dim5_moon`'s air and sunlight (1,173.49 W/m²). Its case runs on `A28_corrected_970` and takes that run's sunlight (1,198.19 W/m²), accepted because CO2 and O2 match | `design_air`, `:860-869`; `:2445-2449` |
| The planet, from the git-ignored planet record | `planet()`, `:856-857` |
| Columns of 6 km, a 150 km top, nudging from 8 to 16 km: lunar values of quantities that scale with gravity | `CASES['ring']`, `:1097-1101` |
| A placeholder land row, wetness classes, PlaSim's soil and land | `:1088-1091`, `:1270-1271`, `:1295` |
| Earth's dry-air R and cp (287.04, 1005.7) in the extraction | `:1197`, `:1551`, `:1682`, `:2411` |
| Two lunar days (59.06 d) starting at sunrise | `CASES['ring']` |
| The build folder on the drive | `CM1_HOME`, `:52` |

**The electrified build** (`cm1_elec.py`).

- **Sources:** three pinned WRF-ELEC files and the Terluna Fortran in `models/cm1/fortran/`.
- **Lunar defaults** (`LUNAR`, `:151`):
  - a 6.8 s sub-step;
  - WRF-ELEC's ground rule, with the leader's crossing at 1 kV/m;
  - the breakdown cap lifted;
  - leakage on.
- **Files it writes** (`:176-199`): `takahashi.txt`, and `terluna_conductivity.txt` from
  `atmosphere/electricity/results/conductivity_moon.json`.

## Calibration and reference products

| Product | Producer | Reads | World parameters | Consumer | Cost |
|---|---|---|---|---|---|
| The planet record and the T21 surfaces | `python -m climate.gcm.boundary` | `shared/constants.json`; the geography products. The surfaces' lakes come from GCM run A's runoff, through a drainage file Terluna replaced on 2026-09-29 with one from run A28_dim5_moon's runoff | R, GM, rotation, solar day, tilt, S0, water share, heights | `exoplasim_run.py:814, 934-951`; `cm1_run.planet()` | Seconds |
| `shield_transmission.json` | `protection.spectra.transmission` | The thin-film model | Spectral only | The spectrum files, the reference columns, the sky | Seconds |
| `sun_<shield>.dat`, `_hr.dat` and the flux | `exoplasim_run.sunlight` (`:966-996`) | TSIS-1 HSRS, the shield, ExoPlaSim's wavelength grid | Star, shield, and the scale through `GSOL0` | PlaSim | Seconds |
| `radiation_check_<run>.json` | `climate.gcm.radiation_check <run>` | A GCM run's output (years 15–24), the topography, line-by-line columns | g, air, shield, the run's climate | The shortwave fits | About 30 min on 8 cores |
| `shortwave_gases.json` (`ZGASQ`) | `plasim_shortwave gases` | The design column at 294.9 K under the titania stack × 0.95; CO2 and O2 lines; `A28_dim5_moon`'s band split | Air, pressure, g, the column's state, the spectrum | `exoplasim_run.py:867-874` | Minutes |
| `twilight.json`: GCM and CM1 terms, the escape, the slant factors | `twilight optics`, `longwave`, `solve`, `ledger` (numba) | The design column; the sky's fine optics; line caches on the drive; `A28_dim5_moon`'s multipliers (2.215, 1.356) and band split (`twilight.py:53-55`) | R, g, air, pressure, the column's state, the shield, a ground albedo of 0.1, PlaSim's σ levels | `twilight.dat`, `ZMLUNAR`, `ZMAIRLUNAR`, `terluna_twilight.txt`, the shortwave fit | About 50 min on 6 threads, with optics caches of 0.1–0.4 GB |
| `shortwave_fit_A28_dim5_lunar.json` | `plasim_shortwave fit A28_dim5 --lunar` | `radiation_check_A28_dim5.json`, that run's output, `twilight.json`, `shortwave_gases.json` | g, air, shield, the fit run's climate, the slant factors | Copied by hand, rounded, into `MODEL` (2.237, 1.292); a test checks the copy | Minutes |
| `TH2OC` = 0.004 | Hand trials in the calibration runs | Uncalibrated runs | The climate state | `MODEL` | — |
| `longwave_A28_corrected_970_heating.json` | `plasim_longwave fit A28_corrected_970_heating --year 0 --every 20` | That run's heating diagnostics; correlated-k with constant g | g, pressure, air, a 295 K state | `exoplasim_run.py:849-853`, into `lwcorr.dat` | About 2 min |
| Ice optics | Literals in `plasim_ice_optics.py:33-61`, the near-infrared weights copied by hand from the unshielded TSIS spectrum | TSIS-1 | The star | The patch's Fortran (`exoplasim_run.py:598-663`) | — |
| Infrared from space (10.1718 and 0.5165 W/m²) | `glow.py` | The ring layout, the film optics, the outgoing longwave, an efficacy of 0.7106 taken from the GCM | R, orbit, star | Copied into a study's runner, then passed as `--top-infrared` | — |
| CM1 build constants | `cm1_run.build` (`:1045`) | g from the planet record; CO2 and O2 from `A28_dim5_moon`'s record | g, air | Every CM1 build | Minutes to compile |
| `terluna_twilight.txt` | `write_twilight` (`:2381-2402`) | `twilight.json` | As the ledger | The twilight builds | Seconds |
| `conductivity_moon.json` | `atmosphere.electricity.conductivity`, with MCEq muons | Cosmic-ray tables, an old CM1 box profile, the middle-atmosphere column | g, R, the column, humidity, an assumed aerosol | The electrified cases' leakage | 4–16 min for MCEq |
| Middle-atmosphere cases (the upper column, ozone) | `atmosphere/middle_atmosphere` | Cross-sections, the shield, the column | Pressure, air, g, the shield | The design column of the ledger, the gas fits and the sky | 7–15 min on 4 cores |
| Correlated-k tables | `atmosphere/radiative_convective/ck.py` | HITRAN lines, MT_CKD | Keyed by pressure, temperature and water fraction up to 3.2 × 10⁵ Pa, independent of the world | The longwave fit, the ring analyses | Hours, once |

Since the reference model refuses any input whose bytes differ from the hashes pinned in `inputs.json`
(251 MB) and `inputs_added.json` (93 MB more), the lab can reuse its 4.1 GB of caches for any world with the
same gases below 3.2 bar.

## Analyses

The survey covered 38 scripts, every one in `climate/gcm/` and `climate/crm/` besides the runners and
`cm1_elec.py`, and classed them by whether they would run on another world's output:

- **8 generic,** among them `compare`, `sun_check`, `build_check`, `elec_analysis` and `storm_lives`.
- **20 parameterizable,** working once given the world's parameters; the core reader `ring_analysis` and
  `ring_crossings` are among them.
- **10 wired to the Moon's sites, runs or geometry,** among them `twilight`, `plasim_shortwave`,
  `ring_comfort`, `jura_analysis` and the dusk-cloud and wave exporters.

The scripts read the world from four places:

- the reference model's `thermodynamics.MOON`;
- `cm1_run.planet()`;
- the shared constants;
- the run's own record, which only five scripts read.

Beyond what those sources supply, many of the scripts build the lunar day into their bins, windows and
keys, and write in the design air, Earth's R and cp, and heights in km.

**Consumers outside `climate/`.** Biosphere, geography, resources, visualization and about fifteen research
studies read products of `A28_dim5_moon`, the design run before 2026-10-14 (its climatology, winds,
convection and radiation check, and the ring summaries), and `atmosphere/lower_air.py`, `reduced_gases.py`
and two provisioning files hold GCM numbers copied in by hand. The lab can mark both kinds stale once its
importer records them.

## Hand steps and open dependencies in Terluna

1. **Calibrations copied into code.** `RAYSCALE` and `SWH2OSCALE` are copied by hand, rounded, from their fit
   product, and `TH2OC` came from hand trials.
2. **The sunlight scale in three places:**
   - 1.0 by default;
   - 0.970 on the design case's command line;
   - 0.95 in the design column on which the ledger, the gas fits, the surface light, the reduced gases and
     the glow dimming were computed (`illumination/surface_light/model.py:111`; `plasim_shortwave.py:43`,
     1,173.49 W/m²; consequences for the tables: regeneration.md, cross-dependency 4).
3. **The air typed into about twenty files, with two Ar/N2 ratios.**
   - The reference model's `earthlike_air` uses 0.0093/0.7808, and the GCM runner 0.00934/0.78084.
   - The gas-band fit therefore holds an O2 mass fraction of 0.19375839, where the run computes 0.19375391.
4. **The shield and the design temperature in code.** The shield is named in code and on command lines, and
   the design temperature appears as 294.9 K in some files and 295 K in others.
5. **An open loop.** The ledger used `A28_dim5_moon`'s multipliers (2.215, 1.356) and band split, and the
   shortwave refit (2.237, 1.292) then used the ledger; each was computed once.
6. **Calibration columns from an uncorrected run.** The shortwave fit took its columns from `A28_dim5`, the
   run before the 2026-09-29 corrections of the Sun and the tilt, whose corrected successor is
   `A28_dim5_moon`.
7. **A correction beyond its fit.** The longwave correction, fitted at 295 K, runs in a test that settles at
   307 K.
8. **A surface downstream of a GCM run.** The design run's lakes come from GCM run A's runoff. Since 2026-09-29
   Terluna's drainage file, under the same name, has held lakes from run A28_dim5_moon's runoff, and running the
   drainage again on the design run's runoff was deferred on 2026-10-16.
9. **CM1's air from a named run.** CM1 reads its CO2 and O2 from `A28_dim5_moon`'s record at build time.
10. **Earth's physics in CM1.** RRTMG takes the Sun's spectrum unfiltered, and the extraction keeps Earth's R
   and cp.
11. **Numbers carried by hand between tools:**
    - the near-infrared weights;
    - the glow and its efficacy, with the glow and the GCM each depending on the other;
    - the 755 ppm CO2 equivalent;
    - the sunlight scale of 0.970, found by trial runs at 0.9655, 0.9685 and 0.970.
12. **Paths in code and records.** The code hard-codes run folders, the patched copy and the caches to the
    drive, and records hold absolute paths through other worktrees. Both models read the planet from one
    git-ignored file.
13. **Staleness checked in a few tests only.** `inverse_climate.json` records hashes of `spectroscopy.py`
    (05496883…) and `inputs.json` (23b4fadb…). On 2026-10-17 those files hashed to 42df5059… and
    65f81b5a…, and no check flagged the difference. Whether the changes move its numbers is unknown.
14. **Chains as shell scripts** in `session-tools/`. Decisions made during runs are recorded in the earlier
    chains' logs alone.
