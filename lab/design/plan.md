# How the lab is built

Each stage has a product and an acceptance check, and is marked done once its check has passed and been
recorded. A stage that builds on another waits for that record, so the work runs from the specifications,
through the reproduction of what Terluna already has, to new work.

| Stage | Product | Acceptance check | State |
|---|---|---|---|
| 0. Design | `lab/design/`; seed specifications in `lab/worlds/`, `lab/configs/` and `lab/studies/`; the registry seed | The author has read the design, answered its open questions and confirmed its proposed decisions (architecture.md, "Decisions") | Draft 3 of 2026-10-17: the open questions answered that day; the engine and three registry thresholds await the author |
| 1. Specifications, data and derivations | `worldlab.spec` (load, `extends` and `set`, resolve, hash), `worldlab.derive` with every quantity of world_spec.md's table (gravity with the spin term, CM1's scale-height, capillary and soil factors, the Sun's declination, the ice-optics weights, ExoPlaSim's output steps and time-step limit), and the data manifest, with the data the seeds pin copied into the store with their provenance | As listed under "Stage 1: checks" | To start |
| 2. ExoPlaSim inputs | The ExoPlaSim adapter's input writer, reading the study's compatibility settings | From the `open-moon` study, with `exoplasim/defaults` and the study's compatibility settings (among them the calibration values Terluna typed in and the restart files its runs started from), the lab writes the files and run key of `A28_corrected_970` byte for byte ("Stage 2: files"), then those of `A28_corrected_970_lw_ice`, which adds `lwcorr.dat` and four namelist entries | To start |
| 3. CM1 builds and cases | Build keys from patch sets and compile constants; the case writers and the GCM-to-CRM extraction; the core patch that reads gravity, CO2 and O2 from the namelist; the planned patches for rain's mean-diameter cap, the soil layers (patch 08) and the Sun's declination (patch 05), each reading its value from the namelist with an identity default | The builds the study's cases resolve to match deployed Terluna builds source for source: `moon_omp_o3` for `ring_45n_corrected`, `moon_omp_twilight` and `moon_omp_terrain_sea_twilight`, Terluna's label entering as a compatibility setting where the Makefile's comment carries it. The input files of the study's three CM1 cases reproduced byte for byte from `A28_corrected_970` and, for the box, from the twilight ring's output. Over a one-day ring segment each, the namelist builds, core and electrified, match builds compiled with the same values and flags: Terluna's `moon_omp_o3` and `moon_omp_elec` at the Moon's values, and builds of the lab's own at 9.81 m/s². Their output is identical, or differs from the compiled build's by no more than a last-bit nudge of that build does, the test by which Terluna accepted its `-O3` rebuild (`notes/verification_record.md`, "Compiler rebuilds"). At its identity default each planned patch leaves the output byte for byte as the build without it. Timed best of three on a quiet machine, they run within 2% of the compiled builds' wall time. The lab then builds CM1 once per patch set and flags | To start |
| 4. Stage graph and planner | Keys, headers, declared read sets, staleness, `plan`, and the rules that run the stages, in Snakemake as proposed (architecture.md, "Decisions") | Keys computed from the `open-moon` study before and after each of regeneration.md's worked changes differ for exactly the products the example lists; with nothing changed, no key changes | To start |
| 5. Producers and calibrations | Stages for the ledger, the gas bands, the shortwave and longwave fits, the water continuum and the ice optics, with their envelopes; the geography producer, with Terluna's `atlas.py` and `drainage.py` brought into `python/geography/`; the glow producer; the target stage for the sunlight scale | Each reproduces its Terluna product from the same inputs within the tolerance it states. The water-continuum stage, which replaces Terluna's hand trials, arrives at `TH2OC` = 0.004 from the same cloud-free columns at 280 and 310 K. The geography producer reproduces `atlas_28pct_4ppd` and `drainage_28pct_16ppd` from the same inputs, and a test fails wherever a tool falls back on its own Earth defaults for the air or the ground albedo | To start |
| 6. Registry and reach | `lab/registry/`, completed from the defect log's classes (a) and (b); the reach report | The report reproduces the paper's table of reach for the worlds of `paper/data/worlds.json`, ten on 2026-10-17 | Thirteen-entry seed drafted |
| 7. Jobs and the Terluna import | The job wrappers, which Snakemake runs within the machine budget under the proposed engine; the read-only importer | Terluna's runs, cases and builds registered with their recorded hashes, each GCM run's key, recomputed from its imported record, matching the recorded one. The inputs of the 32 runs that `models/exoplasim/runs.json` matches rewritten byte for byte from their imported specifications, and the other deployed builds reproduced source for source. The imported 45° N twilight pair flagged for its mixed builds (defect log C8), and the imported `A28_corrected_970_lw_ice` marked used beyond its fit by the envelope check. In a test, a job's wrapper holds the job back while the load exceeds its ceiling or free disk falls below its minimum | To start |
| 8. The Earth control, the fixpoint and the Moon at 1.0 atm | The Earth control's study, `studies/earth-control.toml`, and its two runs, the first the lab makes itself. Its calibrations are the released model's own values for the shortwave multipliers and the water continuum (`model-default`, world_spec.md rule 5), and the ledger and gas-band fits of Earth's own column from stage 5's tools; the fixpoint stage on the 1.2 atm Open Moon, in a study extending `open-moon` (world_spec.md, rule 8); then the study of the Moon at 1.0 atm (architecture.md, "Decisions"), its sunlight scale found by the target stage; the raindrop sensitivity, the 45° N ring with Morrison's own limits and with the capillary scaling | The pipeline's Earth run passes the Earth control's test against the released run. The fixpoint starts from the lab's own run of the design case, stage 5 having reproduced Terluna's correction from Terluna's columns, and its passes refit the correction with ice optics on. Each pass is recorded, and the stage stops within its tolerances or at its pass limit, recording which. The 1.0 atm study's runs pass their registry and envelope checks before they start, and each run's post-run envelope check is recorded with it. The target stage meets the reference temperature within its stated tolerance or records where it stopped. The raindrop sensitivity records the rain reaching the ground and the share of falling water that evaporates under each | To start |

## Stage 1: checks

- **Against Terluna's records.** The Moon's derived values must equal those Terluna recorded:
  - gravity, the partial pressures and the flux in `progress.json` of `A28_corrected_970`;
  - the build macros in `build.json`;
  - `var16`, `var19` and `nx` in each ring case's `case.json`;
  - the CM1 lengths, time step, boundary-layer length and damping rate scaled from `cm1/defaults` at the
    Moon's gravity. Written with the rounding of Terluna's namelist writer (`cm1_run.py:1979-2035`), they must
    equal Terluna's ring settings exactly.
- **Against ExoPlaSim.** The calendar from `worldlab.derive` must equal what ExoPlaSim's own `configure`
  writes:
  - for the Moon;
  - for Earth, at `rotationperiod` 1, where the year sets the days (365);
  - for the time-step guard, against the largest winds of Terluna's runs, which ran stable at 30 minutes;
  - for the periods in `exoplasim_slow_rotators` of `paper/data/regime_calc.json`;
  - on either side of the rounding's steps, where N falls from 36 to 24 just above 12 days and from 24
    to 12 just above 20 days.
- **Against the paper.** `paper/data/regime_calc.json` and `paper/data/worlds.json` must come out of the
  derivations unchanged, each world at the temperature that file states.
- **The data manifest.** Every pin the lab's own stages read resolves within world-crafting and the store,
  with its hash, source, licence and credit recorded. Data from outside Terluna, such as LOLA, GRAIL and
  TSIS-1, pass the review of redistribution rights that AGENTS.md requires before they are copied. The
  compatibility settings' pins name Terluna's files, which the reproduction tests alone open.
- **Without Terluna.** With Terluna's paths absent, the stage's tests pass and the checks against Terluna's
  records report themselves skipped.

## Stage 2: files

For `A28_corrected_970`, the files the lab must write byte for byte are:

- the namelists;
- `sun.dat` and `sun_hr.dat`;
- `twilight.dat`;
- `moon_landmask.sra` and `moon_topography.sra`.

The run key must match as well.

## Order and cost

- **Stages 1, 2, 4 and 6** cost seconds to minutes of one core.
  - Stage 1 copies about 50 MB of Terluna's data and fetches LOLA's heights and the GRAIL geoid.
  - Stage 6, mostly data entry from the defect log, can proceed beside stages 2–5.
- **Stage 3 runs CM1 for its checks:** one-day ring segments of about 5 minutes each on 6 threads, three
  for each build timed.
- **Stage 5** runs the reference tools and so waits for a quiet machine.
  - The ledger takes about 40 minutes of solving on 6 threads, and the ledger step itself about 9 minutes.
    Its optics caches take 0.1–0.4 GB each (`notes/reference_radiation.md`, section 3).
  - The shortwave and longwave fits take minutes, reading the output of the runs they were fitted on:
    `A28_dim5` and `A28_corrected_970_heating`.
- **Stage 8 runs the models.**
  - The Earth control's two 20-year runs take about 75 minutes each: an Earth year at a 30-minute step has
    17,520 steps, against the Moon's 17,160.
  - The target stage for the 1.0 atm study takes three or four GCM runs of about 75 minutes, and the
    raindrop sensitivity two two-lunar-day rings of about 4.5 hours each.
  - A GCM year took 218 s on 4 ranks in `A28_corrected_970`, and 278 s in `A28_corrected_970_lw_ice` with
    its heating diagnostics, so 20 years take about 73–93 minutes.
  - Each one-day segment of the 45° N twilight ring took about 275 s on 6 threads, so its 59 days took 4.5
    hours. That ring wrote 8.5 GB, and the Jura box 54 GB over the same two lunar days.

## What the lab takes from Terluna

- **Copied once into the store, with their provenance (stage 1):** the data the seeds pin. These are the
  geography products under `geography/products/` (49 MB, the atlas and the drainage among them),
  `protection/spectra/shield_transmission.json`, the TSIS-1 spectrum file
  (`atmosphere/radiative_convective/inputs/TSIS1_HSRS_stride100.csv`); `shared/constants.json` is in the
  repository already, as `python/shared/constants.json`, byte for byte as at 186b294. LOLA's
  heights and the GRAIL geoid come from NASA's Planetary Data System by pinned hash, as Terluna's geography
  fetches them (`geography/fetch_inputs.py`).
- **Brought into `python/` under their Terluna paths, with provenance (stage 5):** `geography/atlas.py` and
  `geography/drainage.py`, which flood the heights to a seas share and route runoff into lakes, and
  `research/studies/solar_shield_array/glow.py`, which computes the infrared of a glow in space.
- **Opened read-only by the reproduction tests and the importer alone:**
  - `climate/gcm/exoplasim_run.py`, `climate/crm/cm1_run.py` and `climate/crm/cm1_elec.py`, as the
    reference for what the adapters reproduce;
  - `climate/gcm/products/`: the planet record and the T21 surfaces;
  - `climate/results/gcm/`: the ledger, gas-band, shortwave and longwave products;
  - `gcm-runs/<run>/`: `progress.json`, `inputs/`, `model/*_namelist`, the restart files and the yearly
    output `model/MOST.<year>.nc`, for the GCM-to-CRM extraction and the fits;
  - `gcm-runs/cal_*`: the hand trials behind `TH2OC`;
  - `crm-runs/<case>/`: `case.json` and the input files, and the rings' output (`cm1out_t*_s.dat`) from
    which a box's day–night forcing is computed;
  - `cm1/build/<label>/`: `build.json` and the deployed sources.
