# How the lab is built

Each stage has a product and an acceptance check, and is marked done once its check has passed and been
recorded. A stage that builds on another waits for that record, so the work runs from the specifications,
through the reproduction of what Terluna already has, to new work.

| Stage | Product | Acceptance check | State |
|---|---|---|---|
| 0. Design | `lab/design/`; seed specifications in `lab/worlds/`, `lab/configs/` and `lab/experiments/`; the registry seed | The author has read the design and answered its open questions (architecture.md, "Decisions") | Drafted 2026-10-17 |
| 1. Specifications and derivations | `worldlab.spec` (load, `extends` and `set`, resolve, hash) and `worldlab.derive` | As listed under "Stage 1: checks" | To start |
| 2. ExoPlaSim inputs | The ExoPlaSim adapter's input writer, with its Terluna compatibility settings | From `moon/open-moon` and `exoplasim/terluna-corrected`, the lab writes the files and run key of `A28_corrected_970` byte for byte ("Stage 2: files"), then those of `A28_corrected_970_lw_ice`, which adds `lwcorr.dat` and four namelist entries, and then the inputs of the 32 runs that `models/exoplasim/runs.json` matches | To start |
| 3. CM1 builds and cases | Build keys from patch sets and compile constants; the case writers and the GCM-to-CRM extraction | The fields of each deployed build's `build.json` reproduced (`check_patches.sh` already reproduces their sources). The input files of the three seed cases (`ring_45n_corrected`, `ring_45n_corrected_twilight`, `box_jura`) reproduced byte for byte from `A28_corrected_970` | To start |
| 4. Stage graph and planner | Keys, headers, read sets, staleness, `plan` | With nothing changed, the plan is empty; the computed stale sets equal the worked examples in regeneration.md | To start |
| 5. Producers and calibrations | Stages for the ledger, the gas bands, the shortwave and longwave fits and the ice optics, with their envelopes | Each reproduces its Terluna product from the same inputs within the tolerance it states. The envelope check marks `A28_corrected_970_lw_ice` as used beyond its fit | To start |
| 6. Registry and reach | `lab/registry/`, completed from the defect log's classes (a) and (b); the reach report | The report reproduces the paper's table of reach for the worlds of `paper/data/worlds.json`, ten on 2026-10-17 | Eleven-entry seed drafted |
| 7. Jobs and the Terluna import | The job runner with its machine budget and queue; the read-only importer | Terluna's runs, cases and builds registered with their recorded hashes, each GCM run's key, recomputed from its imported record, matching the recorded one. The imported 45° N twilight pair flagged for its mixed builds (defect log C8). In a test, the runner holds back a job while the load exceeds its ceiling or free disk falls below its minimum | To start |
| 8. The fixpoint and the first new run | The fixpoint stage; the first experiment the lab runs itself (architecture.md, open question 3) | The fixpoint's first pass reproduces the existing longwave correction from the same columns. Each further pass is recorded, and the stage stops within its tolerances or at its pass limit, recording which. The new experiment passes its registry and envelope checks before it runs, and its post-run envelope check is recorded with it | To start |

## Stage 1: checks

- **Against Terluna's records.** The Moon's derived values must equal those Terluna recorded:
  - gravity, the partial pressures and the flux in `progress.json` of `A28_corrected_970`;
  - the build macros in `build.json`;
  - `var16`, `var19` and `nx` in each ring case's `case.json`.
- **Against ExoPlaSim.** The calendar from `worldlab.derive` must equal what ExoPlaSim's own `configure`
  writes:
  - for the Moon;
  - for the periods in `exoplasim_slow_rotators` of `paper/data/regime_calc.json`;
  - on either side of the rounding's steps, where N falls from 36 to 24 just above 12 days and from 24
    to 12 just above 20 days.
- **Against the paper.** `paper/data/regime_calc.json` and `paper/data/worlds.json` must come out of the
  derivations unchanged.

## Stage 2: files

For `A28_corrected_970`, the files the lab must write byte for byte are:

- the namelists;
- `sun.dat` and `sun_hr.dat`;
- `twilight.dat`;
- `moon_landmask.sra` and `moon_topography.sra`.

The run key must match as well.

## Order and cost

- **Stages 1–4 and 6** cost seconds to minutes of one core. Stage 6, mostly data entry from the defect log,
  can proceed beside stages 2–5.
- **Stage 5** runs the reference tools and so waits for a quiet machine.
  - The ledger takes about 40 minutes of solving on 6 threads, and the ledger step itself about 9 minutes.
    Its optics caches take 0.1–0.4 GB each (`notes/reference_radiation.md`, section 3).
  - The shortwave and longwave fits take minutes, reading the output of the runs they were fitted on:
    `A28_dim5` and `A28_corrected_970_heating`.
- **Stage 8 runs the models.**
  - A GCM year took 218 s on 4 ranks in `A28_corrected_970`, and 278 s in `A28_corrected_970_lw_ice` with
    its heating diagnostics, so 20 years take about 73–93 minutes.
  - Each one-day segment of the 45° N twilight ring took about 270 s on 6 threads, so its 59 days took 4.5
    hours. That ring wrote 8.5 GB, and the Jura box 54 GB over the same two lunar days.

## What the stages read from Terluna

The stages open these Terluna and research-drive paths read-only:

- `climate/gcm/exoplasim_run.py`, `climate/crm/cm1_run.py` and `climate/crm/cm1_elec.py`, as the reference
  for what the adapters reproduce;
- `climate/gcm/products/`: the planet record and the T21 surfaces;
- `climate/results/gcm/`: the ledger, gas-band, shortwave and longwave products;
- `protection/spectra/shield_transmission.json`;
- the geography products under `geography/products/`;
- `gcm-runs/<run>/`: `progress.json`, `inputs/`, `model/*_namelist` and the yearly output
  `model/MOST.<year>.nc`, for the GCM-to-CRM extraction and the fits;
- `crm-runs/<case>/`: `case.json` and the input files, and the rings' output (`cm1out_t*_s.dat`) from which
  a box's day–night forcing is computed;
- `cm1/build/<label>/build.json`.
