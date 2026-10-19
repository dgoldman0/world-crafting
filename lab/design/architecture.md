# The lab: architecture

The lab's design on the `lab` branch, closed for coding on 2026-10-18 with the author's answers of
2026-10-17 and 18, to which the author added the flagship study on 2026-10-19 ([waterworlds.md](waterworlds.md)).
Each part described here stays a proposal until the code that builds it lands;
[inventory.md](inventory.md) describes what exists today, [regeneration.md](regeneration.md) what depends on
what.

## What the lab is for

A world is written down once, and ExoPlaSim and CM1, then SWAN, SWASH and other codes, are configured,
built, run, calibrated and analysed from that description. Three tasks that Terluna performs by hand
become the lab's routine work:

1. **Regeneration.** When a world, scenario or model parameter changes, the lab lists every derived input,
   calibration, build, run and analysis that depends on it, prices their rebuilding from past wall times
   and rebuilds them in order.
2. **Reach.** For any world the lab reports which of the models' Earth assumptions are repaired, which
   calibrations hold there, which need refitting and which schemes it refuses.
3. **Evidence.** Every product records its producer, its inputs and the parameter values it read, and the
   kind of evidence it is; a fit records the range of states it was fitted on as well.

The Open Moon, compared with Terluna's results, is the lab's test case, with Earth beside it as the Earth
control; both have Earth-like air, nitrogen and oxygen with water and modest carbon dioxide, the Moon's under
gravity, rotation, sunlight, column mass and scale height far from Earth's. The flagship study, a family of
low-gravity waterworlds after Arnscheidt, Wordsworth and Ding (2019), models each of its worlds under steam alone
and under such air ([waterworlds.md](waterworlds.md)). A scenario of steam alone, an air whose main gas condenses,
runs in a one-dimensional column of the lab's own, and the adapted three-dimensional models exclude it, as they
exclude scenarios whose air is dominated by CO2 or CH4, whose surface pressure reaches several bar, or whose
condensables are other than water; the registry refuses each of these for the three-dimensional models until one
that handles it is adapted.

The lab runs from the command line on one shared machine. Its stages are plain Python functions, which the
lab's runner, a small local service, calls in the order the stage graph sets; the command line is the
runner's first client, and a user interface can be a second.

## Principles

- **An ensemble of its own.** The lab models found and crafted worlds for their own sake, and its design,
  numerics and code are chosen for that work alone (the author's direction of 2026-10-18). The Open Moon's
  case and some of its data come from Terluna, and the lab compares its values with Terluna's records
  within stated tolerances; it reproduces none of Terluna's runs, inputs, keys or quirks byte for byte.
- **Self-contained.** What the lab uses for its own work lives in world-crafting and the lab's store: its
  specifications, adapters and case writers, run bookkeeping, analyses, builds and runs, and the data it
  reads, copied with their provenance. Terluna's files serve the comparison tests alone, which skip where
  Terluna is absent (the author's decision of 2026-10-17).
- **One description, with every derived value computed.** Surface gravity comes from GM, R and the spin, the
  solar day from the rotation and the year, PlaSim's model day from ExoPlaSim's own rounding rule, and CM1's
  domain length from the radius and the latitude. The sunlight at the top comes from the star's spectrum, or
  its temperature alone, the orbit and the scenario's filter. CM1's grid follows the scale height, its
  raindrop limits the capillary length, its soil layers the solar day and its Sun the season. A scenario's
  sunlight scale may follow its reference temperature, which the target stage meets over GCM runs. A world may
  state such a value with its basis, as Earth's seed states the standard gravity of 9.80665 m/s², and the lab
  records it beside its derivation (world_spec.md, rule 2).
- **Internal forms, converted on import.** Where a form of the lab's own serves its computation better than the
  forms its sources use, each kind of quantity keeps that one form inside the lab: heights above the geoid on a
  global grid, a pressure at an equipotential, a spectrum as wavelength and irradiance, a climatology as fields on
  its grid. A reader converts outside data into that form as it imports them, from the Planetary Data System's
  images and tables, Terluna's products or a published model's output, and records the conversion with the
  product (the author's direction of 2026-10-19). A value stated another way is converted on import as well:
  Mars's seed states its pressure at the mean radius, which the lab will convert to a pressure at the areoid once
  Mars has heights, and refuses until then.
- **One register for the world and its scenario.** The Open Moon charter requires one versioned register of
  pressure and composition, water, gravity, rotation and the filtered spectrum (Terluna
  `ensemble/planning/Open_Moon_Editorial_Charter_control-01.md`, E3). In Terluna these values are typed into
  about twenty files (inventory.md), and the lab's world and scenario specifications become that register.
- **A header on every product.** It records:
  - the product's schema;
  - its producer, as a code identity;
  - its inputs: upstream products by hash and external data by pin;
  - its read set: every value it used from the world, the scenario and its run's settings, by name and
    value;
  - its evidence statement and state;
  - for a fit, the envelope of states it was fitted on.

  The header extends Terluna's data-product convention (`shared/README.md`, "Data products") and the
  recording of constants by name and value in `shared/provenance.py`.
- **Computed staleness.** A product is current while its key is unchanged; the key covers its producer, its
  upstream keys, its external pins, its read set and its environment class.
- **Refusal with a reason.** In any of five cases the lab stops the stage and names the cause:
  - an input is missing;
  - a hash differs;
  - the scenario and the run's settings lie outside a calibration's envelope, in the dimensions they fix;
  - a registry entry forbids the scheme;
  - a declared pair differs outside its delta (below).

  Outside an envelope or against a registry entry, the stage runs only on an explicit override, as the
  author decided on 2026-10-17. The override records its justification, which the lab copies into every
  downstream header, and the lab warns of it in the plan, at the start of the run and in every report built
  on its products. The other three causes stop the stage until the input, the hash or the pair is corrected.
- **Declared pairs.** A run or case derived from another names its change, as set fields or as a variant
  that its model's defaults define. The lab compares the two fully resolved input sets, build flags
  included, and refuses the pair when they differ elsewhere. A series point that the declared switches
  need counts within the delta. The check refuses, for instance, a twilight case whose control was compiled
  with other optimisation flags, the fault defect log C8 records in Terluna's 45° N pair.
- **Earth in two checks.**
  - **Identity, per patch.** With its switch at its identity default, the patched model reproduces the
    released model's own Earth configuration byte for byte.
  - **The Earth control, per pipeline.** Earth's specification runs through the same derivations and
    adapters as any other world.
    - The lab's model defaults switch several repairs on for every world, the synodic Sun clock among them,
      so the pipeline's Earth run follows other code paths than the released model's. Byte identity is
      therefore required of each patch alone.
    - The pipeline's Earth run is compared with a released run configured through ExoPlaSim's own
      interface with the same air and sunlight: its global means of surface temperature, top-of-atmosphere
      net flux, precipitation and cloud cover must fall within two standard deviations of the released run's
      yearly means, a criterion the author accepted on 2026-10-17. Plan stage 8 opens with the two runs.
- **A shared machine.** Every job states its threads, memory and disk. The lab checks the load and the
  free disk before it starts one, and runs it at reduced priority.

## Concepts

| Concept | What it is | Identity | In Terluna today |
|---|---|---|---|
| World | A body: its size and mass, rotation, orbit, star and any host planet | Name and content hash | `shared/constants.json`, through `climate/gcm/boundary.py`, into `moon_gcm_configuration.json`; the year and eccentricity typed into `exoplasim_run.py:841-842` |
| Scenario | A designed or supposed state of a world: air, water, shield and sunlight scale, surface properties, outside forcings | Name and content hash | `EXPERIMENTS` (`exoplasim_run.py:85-94`), parts of `MODEL`, command-line flags |
| Model defaults | One model's settings for any world: upstream pin, patch-series state and switches, grid, physics options, output, guards. CM1's also name variants and give lengths, times and rates at a reference state | Name and content hash | `MODEL` (`exoplasim_run.py:98-145`), `BUILDS`, `case_settings` (`cm1_run.py:1979-2035`) |
| Study | One scenario's whole chain: its GCM runs and the CM1 cases forced from them, each extending its model's defaults | Name and content hash | `EXPERIMENTS` and `CASES` together |
| Calibration | A fitted product, with the states it was fitted on and its residuals | Content hash | Scalars typed into `MODEL`; JSON products in `climate/results/gcm/` |
| Experiment | A GCM run in a study: its settings, calibrations, initial state and length | Its product key ("The stage graph and staleness"), which names its folder in the store | GCM run folders and their run key (`exoplasim_run.py:905-911`) |
| Case | A cloud-resolving slice in a study, forced from one of its experiments and, for a box, from a ring's day–night circulation: geometry, years, variants, CM1 settings | Its product key, as for an experiment | `CASES` (`cm1_run.py:1093-1526`), `case.json` |
| Build | An executable made from an upstream pin, a patch set, compile-time constants and flags | Hash of all four, with the compiler and its version | `cm1/build/<label>/build.json`; the patched ExoPlaSim copy on the drive |
| Delta | The declared difference between two experiments or cases: set fields, named variants | Part of the derived item | Prose ("so the pair differs in that alone") |
| Registry entry | One Earth assumption in one model: its location, what it assumes, when it matters, what repairs it | Stable id (A1, B1, …) | `notes/defect_log.md` |
| Record | What happened: segments, wall time, outputs, checks | Belongs to its run or case | `progress.json` |

A world file holds what the body is, and a scenario file what has been made of the body or is assumed for
it. The Moon's shield, its 28% seas and its air are scenario choices, so the Moon at 1.0 atm becomes a
second scenario of the same world. A run's settings are its model's defaults with the study's changes, and
the registry and the envelopes test those resolved settings.

## Components

```mermaid
flowchart TB
  subgraph specs [Specifications, in Git]
    W[worlds] --- S[scenarios] --- C[model defaults] --- E[studies: experiments and cases]
  end
  specs --> D[derive: quantities every model needs]
  D --> R[registry and reach report]
  D --> G[stage graph: keys, read sets, staleness, plan]
  R --> G
  G --> RN[runner: the job queue, within the machine budget]
  RN --> P[producers: surface, sunlight, air, reference columns, ledger, fits]
  RN --> B[builds: ExoPlaSim, CM1]
  RN --> J[jobs: GCM experiments, CM1 cases]
  P --> ST[(store: products, builds, runs)]
  B --> ST
  J --> ST
  ST --> X[coupling: GCM state and ring output to CRM slices]
  X --> J
  ST --> DG[diagnostics and reports]
```

| Component | Working module | Does | Built from |
|---|---|---|---|
| Specifications | `lab/worlds/`, `lab/configs/`, `lab/studies/` | Worlds, scenarios, model defaults and studies in TOML; `extends`, `set` and `variants` express a derived item and its delta | `EXPERIMENTS`, `MODEL`, `CASES` |
| Derive | `worldlab.derive`, `worldlab.sunlight` | Pure functions from a specification to the quantities the models need: g; Ω; the solar day; the scale height, H/R, the column mass and the Chapman horizon factor; ExoPlaSim's calendar (rotations per year, model day, steps per day, whole-day run steps); the gas mass fractions and gas constant; CM1's domain lengths and Coriolis parameters. `worldlab.sunlight` gives the sunlight at the top and the ice-optics weights from the star's spectrum and the filter | `paper/tools/regime_calc.py`, `boundary.planet()`, arithmetic spread through the runners |
| Registry and reach | `worldlab.registry`, `lab/registry/` | Earth-assumption entries and calibration envelopes, evaluated for a world, a scenario and a run's settings into a reach report | `notes/defect_log.md`, classes (a) and (b); the paper's table of reach |
| Stage graph and store | `worldlab.stages`, `worldlab.store` | Stage definitions, product keys and headers, read-set tracking, staleness, priced plans | Terluna's run key, `case.json`'s input hashes, `shared/provenance.py` |
| Model adapters | `worldlab.models.exoplasim`, `worldlab.models.cm1` | Builds, input files, namelists, runs and guards for each model | `exoplasim_run.py`, `cm1_run.py`, `cm1_elec.py` |
| Coupling | `worldlab.couple` | GCM state to CRM inputs: reference profiles, mean vertical wind, sideways forcing, surfaces along rings and in boxes; a ring's output to a box's day–night forcing | `cm1_run.py:1162-1956`, `ring_crossings.day_night_advection`, `ring_heat_budget.gcm_sideways` |
| Producers | `worldlab.produce.*`, calling `python/` | The surface grid and sunlight files, reference columns, the curved-air ledger, the gas-band, shortwave, water-continuum and longwave fits, the ice optics; the seas from the heights and the lakes from runoff; the infrared of a glow in space. Each runs on the scenario's own values, where Terluna's tools default to Earth's air and a ground albedo of 0.1 | `boundary.py`, `exoplasim_run.sunlight`, `python/climate/gcm/*`, `python/atmosphere/*`, `python/illumination/sky/*`; Terluna's `geography/atlas.py`, `geography/drainage.py` and `glow.py` |
| Runner | `worldlab.runner` | A local service that keeps the job queue in the store, orders the stale products by the stage graph, starts each job once its inputs exist and the machine budget allows, and takes start, stop, resume, cancel and reorder from its clients | The shell chains in `session-tools/` |
| Jobs | `worldlab.jobs` | Each model job's wrapper: locks, segments, resume and stop files, with its progress written to its record | The loops of Terluna's two run scripts |
| Diagnostics | `worldlab.diag` | One implementation of the diagnostics every world needs: global and zonal means, energy budgets, composites by local solar time, profiles by band, GCM–CRM comparisons | `summarise_year`, `climatology.py`, the generic parts of the ring and box analyses |

Analyses particular to Terluna (comfort, named sites, the ecology and resource couplings) remain in Terluna
and read the lab's products.

## Specifications

Specifications are TOML, written by hand or by the lab's own commands and kept in Git, while products and
records are JSON written by the lab. In TOML a comment beside each value can give its source, and Python's
standard library reads the format (`tomllib`). A specification's identity is the hash of its resolved form,
computed after its `extends` chain and variants are applied and its derived values filled in, which leaves
formatting and comments out of the identity. [world_spec.md](world_spec.md) sets out the draft schema with
the Open Moon worked through.

The lab keeps three kinds of specification:

- **World and scenario files** hold the physical values once, for every model.
- **Each model's defaults** hold the settings only that model has, stated for any world.
- **A study** sets up one scenario's chain: its GCM runs, then the CM1 cases forced from them, each extending
  its model's defaults with the changes particular to the study.

Terluna builds families of cases, such as rings at six latitudes, in loops over Python dicts
(`cm1_run.py:1124-1159`). The lab generates each family into explicit entries of a study, which can then be
read and compared one by one.

## The stage graph and staleness

A **stage** is a producer with declared kinds of input, and a **product** is one result of a stage. A
product's key is a hash of five things:

- the producer's identity: the hashes of its module and of the in-house modules it imports, with models
  identified by build hash and external tools by version;
- the upstream products' keys, whose content hashes the header records;
- the pins of the external data it reads, such as HITRAN lines, TSIS-1, MT_CKD and the RRTMG tables;
- the values in its read set;
- the environment's class: Python and the major and minor versions of numpy, scipy and numba; for builds,
  the Fortran compiler and its version, and for a build at `-march=native` the CPU type it compiles for.

The full versions are recorded beside the key.

**Read sets** are declared by each stage, by name, so that a product's key follows from the specifications
before the product exists. The producer receives a tracking view of the specifications, which records each
value it reads by name and value and refuses a read outside the declaration. A derived value enters as
its value, so a consumer that reads only g stays current when GM and R change together and leave g where
it was. Terluna's `shared/provenance.py` applies this rule to its constants; the lab extends it to every
input. A run's guards, such as `guards.wind_share_of_limit`, warn without changing what the run computes, so its
read set leaves them out and a new share leaves every run current.

**Plan.** `lab plan` computes the keys from the current specifications and compares them with the store.
It lists the stale products in the order it would rebuild them, each priced from the wall times in its
records. `lab make` then hands them to the runner's queue, which runs them within the machine budget.

**The runner** is a long-lived local process that keeps its queue and each job's state in the store, so
that a restart, or another client, finds the work where it stood. It builds only what lacks a complete
product under its key, so the key remains the one test of staleness. Clients reach it through a local
socket in the store; `lab serve` starts it, as does the first client that finds it down.

- **Progress.** A job's wrapper writes its progress, by model year or one-day segment, into the job's
  record, which the command line and a user interface read alike.
- **Failure.** A failed job keeps its folder and record, from which it resumes.
- **Loops.** The fixpoint and target stages run as jobs that add their own GCM runs to the queue, each pass
  recorded.
- **Clusters,** later, through an adapter that submits a job to a scheduler such as Slurm in place of
  starting it here.

**The test of the planner.** The dependency map in regeneration.md was worked out by hand from Terluna's
code. Before `lab make` acts on its plans, the planner's computed staleness must match the map in its
worked cases (plan.md, stage 4).

## Model adapters

Each model version has its own adapter, and a version that adds physics, such as reduced correlated-k
radiation or a deep-atmosphere core, also has its own patches and identity tests. An adapter states:

- what it needs from the derived quantities and the registry;
- how it makes a build;
- how it writes a run's input files;
- how it runs, resumes and stops;
- how its output is read into the diagnostics' variables.

**ExoPlaSim.**

- **Builds.** A build is an installed copy of ExoPlaSim 3.4.2 at a named point in the patch series. It is
  compiled for its resolution, levels and ranks, and kept in the store under its key. Terluna patched its
  shared installation with patches 01–06 and kept a second copy for 07–10 (inventory.md); in the lab each
  state of the series has a copy of its own.
- **The calendar** follows ExoPlaSim's own rule (`exoplasim/__init__.py:2609-2619`;
  `plasim.f90:1287-1302`):
  - `N_DAYS_PER_YEAR` is the year in whole days, 365 for Earth, when `rotationperiod` is 1, and otherwise
    12 · max(1, ⌊360/(12·P_rot) + 0.5⌋);
  - the model day is P_rot · N/(N − 1), and exactly one day when `rotationperiod` is 1 (`plasim.f90:1287`).

  The steps per model day, the whole-day run length, the steps per mean and the expected output count
  follow from it, replacing the values Terluna typed in for the Moon: 1,430 steps, 12 days a year and 120
  means (`exoplasim_run.py:98`). The steps per mean come from an interval in days: below a model day, the
  means a model day are the divisor of its steps whose mean lies nearest the interval, 10 means of 143
  steps for the Moon's 3 days; from a model day up, the interval takes whole model days.
- **Namelists and guards.** The namelist edits of `build_model` (`exoplasim_run.py:1010-1085`) become a
  function of the resolved inputs. The guards remain: the band split, the run's key against resuming a
  changed run, free disk and the output count. A new guard checks the time step, a stated model choice,
  against the advective limit at the world's radius and the truncation with the run's largest wind, each
  model year.
- **Worlds all ocean and worlds locked to their star.** For an all-ocean world the writer sets ExoPlaSim's
  aquaplanet switch, `NAQUA`, and leaves the land mask and heights unwritten (`exoplasim/__init__.py:2858-2860`).
  For a world locked to its star it sets the synchronous mode, `NFIXED`, with the substellar longitude in
  `FIXEDLON` (`:2628-2630`), and gives the orbit's period as the rotation period, from which `ROTSPD` follows
  (`:2616-2617`). The star's light files and, through patch 11, the ice-optics weights come from the star's own
  spectrum, which matters most around a red dwarf, whose light lies further into the near infrared than the Sun's.
- **Patch 10's solar weights.** Patch 10 writes the near-infrared weights of the TSIS-1 Sun into
  PlaSim as Fortran constants (regeneration.md, cross-dependency 13). A planned patch 11 reads them from
  the namelist, with patch 10's constants as its identity default, and the adapter computes them from the
  spectrum at the top of the air, the filter included. Until patch 11 passes its identity test (plan.md,
  stage 2), runs with ice optics on take patch 10's weights, from the unfiltered Sun, and registry entry
  `exoplasim-ice-weights` warns of them.

**CM1.**

- **Builds.** Gravity, CO2 and O2 are the three values Terluna's builds compile in: core patches 01–03, 06
  and 07 and the electrified series' fall speeds read them as macros (`models/cm1/README.md`), so each world
  or air has needed builds of its own. CM1's dynamics and the Morrison scheme already take gravity from
  `set_constants` as the model starts. A planned core patch reads all three from the namelist, giving RRTMG
  and the CAPE diagnostic the run's gravity and RRTMG its CO2 and O2, and a companion patch in the
  electrified series gives the NSSL fall speeds the same gravity, so that one build of each patch set serves
  every world, as the author preferred on 2026-10-17. MYNN's shared constants need gravity at compile time
  and keep 9.81; the lab already refuses MYNN off Earth. Until the patches pass their checks (plan.md,
  stage 3), the adapter compiles the values in, and a build's key covers them with its patch set, flags and
  compiler.
- **Points in the series.** A build names how far it applies each patch series, as ExoPlaSim's builds
  name their point in theirs. Each planned patch is appended after core 17 and electrified 9, as core 18
  onward and electrified 10, and at its identity default gives the output of the build without it: Earth's
  gravity and air for the namelist patches, Morrison's 2.8 mm cap, patch 08's 5–80 cm soil and patch 05's
  equinox Sun.
- **Case kinds,** as Terluna has them:
  - a ring on a circle of latitude, or on a tilted great circle;
  - a box: flat, over terrain, or over terrain with sea;
  - a window run again from a restart;
  - another case's inputs with a new build;
  - a finer box;
  - CM1's own samples.
- **Variants.** Twilight, terrain, sea and the electrified build are variants in CM1's defaults, each adding
  its patch series and the settings it needs (`lab/configs/cm1/defaults.toml`). A case names its variants,
  and those names form its declared delta.
- **Lengths, times and rates scaled with the scale height.**
  - The Rayleigh damping rate and the boundary layer's length already follow g (`cm1_run.py:2004-2005`).
  - The column width, the vertical grid, the model top, the nudging heights and the time step follow it in
    the lunar cases only through the values chosen for them. The defaults state these at the Open Moon's
    state, where Terluna's rings ran them. The adapter multiplies lengths by H/H_ref, with H = RT/(Mg) at
    the scenario's reference temperature, times by (H/c)/(H/c)_ref, with c = (RT/M)^½, and rates by the
    inverse. The defaults' reference state is the one Terluna's rings ran at, the Open Moon's air at 295 K
    under Terluna's gravity, GM/R² (`cm1/defaults`, `[reference]`); the spin term moves the lab's own lunar
    cases 5 parts per million from it. At Earth's 288 K and air, with CM1's 9.81 m/s², lengths take 0.161,
    giving columns of 965 m and a 24.1 km top.
  - **Unscaled:** with the world's Sun in a case, the run length is set in the world's solar days, and the
    output, restart and nudging intervals stay in seconds. Terluna's gravity pair, which ran without a Sun,
    scaled those too (`time_scale`, `cm1_run.py:1974-2029`).
- **Raindrops, soil and the Sun.** Each follows the world through a planned patch with an identity
  default (registry B28, `cm1-soil-day`, `cm1-equinox-sun`):
  - Morrison's breakup diameter and its cap on rain's mean diameter scale as (9.81/g)^½, the capillary
    length, through the namelist's `brkup_db` and a planned patch. NSSL's two-moment rain, which the
    electrified box runs, has its explicit breakup off (`irainbreak`), and stage 3 identifies any other size
    limit it holds.
  - The slab soil's layers scale as (solar day/1 d)^½, where patch 08 fixes the lunar 5–80 cm on every
    world.
  - The Sun takes the declination of the case's season, where patch 05's stands at the equinox. Each case
    starts at its own sunrise, at an hour angle of −acos(−tan φ tan δ), and the GCM reference it is forced
    from averages a window of solar longitude around its season, where Terluna's rings averaged whole
    model years.
  - For a world locked to its star, a further planned patch holds the star fixed in the sky over the case,
    with the moving Sun as its identity default (plan.md, stage 12).
- **Refused schemes.** At a gravity more than 0.5% from 9.81 m/s², the registry refuses the schemes that
  hard-code Earth's gravity (`notes/cm1.md`): MYNN, the GFS EDMF and GFDL layers, P3, WSM6, Jensen–Ishmael,
  LFO and Goddard radiation. The tolerance is proposed; it passes the Earth control's 9.80665 m/s².

## Calibrations, envelopes and loops

A calibration is a product whose header also records:

- the reference model and its version;
- the columns or states it was fitted on, as ranges of surface temperature, precipitable water, column
  mass, composition, spectrum and the GCM's levels, with the model switches in force, such as ice optics;
- the fit's residuals;
- the fit's form.

The lab checks the envelope twice:

- **Before a run,** the scenario and the run's settings must fall inside it in the dimensions they fix:
  column mass, composition, spectrum, the GCM's levels and the switches in force. Outside it, the run
  waits for an explicit override (Principles).
- **After a run,** the settled state must fall inside it in every dimension, surface temperature and
  precipitable water included. Outside it, the run's products are marked "used beyond its fit", and every
  report built on them carries the warning.

Terluna's longwave and ice test (`A28_corrected_970_lw_ice`), which settled near 307 K, shows what the second
check catches: its longwave correction was fitted at 295 K, and Terluna's plan records that the corrected
layers stray by 5–7 W/m² already at 302 K. The lab's own run of that pair, on such a correction, is marked
"used beyond its fit" wherever it settles outside the fit's range, and kept as a sensitivity until the
correction is refitted with ice optics on, as the author chose on 2026-10-17 (plan.md, stage 8).

Three calibrations are fitted on the GCM's own columns, as Terluna fitted its own:

- the shortwave multipliers, on 11 columns (Terluna's from `A28_dim5`);
- the water continuum (`TH2OC`), on cloud-free columns at 280 and 310 K, where Terluna chose 0.004 by hand
  trials (inventory.md);
- the longwave correction, on about 2,100 cloud-free columns (Terluna's from `A28_corrected_970_heating`).

Each refit changes the climate that supplies the next columns, so a **fixpoint stage** runs the loop that
`notes/exoplasim.md` puts first among its improvements: run, take the columns, refit, run again. A world's
first run takes each calibration at its identity default, the released model's own value, and the fixpoint
starts from it.

- **Stopping.** The stage stops once the parameters and the climate each move less than stated tolerances,
  or at a stated pass limit.
- **Record.** Every pass is recorded, and the product's evidence state becomes "calibration, consistent
  after n passes" or "calibration, unconverged after n passes".
- **First use.** The first such loop is the paper's first item of next work, the longwave at the settled
  state.

A **target stage** finds the sunlight scale of a scenario whose `sunlight.scale` is
`to-reference-temperature`: secant steps over GCM runs move
the scale until the global-mean surface temperature meets the scenario's reference temperature, and each
run is kept as the stage's record. Terluna took the same steps by hand (regeneration.md, "Loops").

- **Stopping.** The stage averages each run's last ten model years and stops within 0.1 K or after six
  runs, recording which.
- **Nesting.** Within the fixpoint it runs first in each pass, so that the calibrations are refitted on the
  climate at the target.
- **Order.** Stage 5 builds it and tests it by replaying Terluna's trial runs, and its own runs wait for
  stage 7's runner like any others.

**Lakes from runoff.** A run's surface takes the lakes routed from the runoff of a named earlier run of its
study (`lakes_from`), and the first run of a chain takes the lakes routed from the runoff of a pinned
climatology (`water.lakes_start`), so that each link is keyed, every link's lakes are routed over the lab's own
heights, and the chain holds no cycle. A fixpoint step repeats the chain on request, until the lake area moves
less than a stated tolerance or a pass limit stops it.

## The registry of Earth assumptions and the reach report

An entry records:

- **Location:** the model, the file and line in the pinned upstream, and the form (constant, unit of time,
  geometry, fit beyond its range, latent defect).
- **Assumption:** for example g = 9.81, a solar day of 86,400 s, H/R = 0.0013, or a surface pressure below
  1,053.63 hPa.
- **Condition:** a list of tests, all of which must hold, on derived quantities, specification fields and
  the run's settings. Examples: gravity more than 0.5% from 9.81 m/s² with the MYNN surface layer, or the lowest
  level's pressure above 1,053.63 hPa. The seed in `lab/registry/earth_assumptions.toml` encodes these as
  structured tests that the lab can check and print.
- **State:** repaired, with its patch, switch and identity default; calibrated, with its stage; bounded;
  or open.
- **Action** when the condition holds and the run's settings lack the repair:
  - require the switch;
  - require a build;
  - require a refit;
  - warn, the warning copied into every product;
  - refuse.
- **Evidence:** the defect-log and verification-record entries it cites.

For a world, a scenario and a run's settings, the lab evaluates every entry into a **reach report**, which
lists:

- what is repaired;
- what runs at its identity default;
- what needs a refit;
- what draws a warning;
- what is refused.

Its first test is to reproduce the paper's table of reach (`paper/sections/reach.tex`) for the ten worlds
of `paper/data/worlds.json` as of 2026-10-17. Three of those worlds are slow rotators, which test the
Sun-clock entry across ExoPlaSim's rounding.

## Storage and records

| Where | Holds |
|---|---|
| Git (this repository) | Specifications, the registry, the design, small products (calibrations, tables and reports of a few MB at most), the records index |
| The store, at `$WORLDLAB_STORE`: a folder of the lab's own, on the research drive on this machine | `data/<digest>/` for the manifest's files, `builds/<key>/`, `products/<stage>/<key>/`, `runs/<key>/`, `cases/<key>/`, `caches/`, an index of human names, and the runner's queue, job states and socket |

Each run and case is filed under its product key, as `runs/<key>/` and `cases/<key>/`, and the name its study
gives it, as `<study>:<name>`, becomes an alias of that key.

- **Links between records.** A case names its experiment by key.
- **Paths.** Paths enter keys relative to configurable roots, so the ledger takes from a root the run folder
  that Terluna's ledger hard-codes (`notes/reference_radiation.md`, section 3). Terluna's pins resolve
  through `$TERLUNA_REPO` and `$TERLUNA_DRIVE`, or `lab/local.toml` where those are unset, which the
  comparison tests read and skip without (`lab/worldlab/roots.py`); the lab's own pins resolve through the
  manifest at `lab/data/manifest.toml`. `$WORLDLAB_ENV`, or `lab/local.toml`, names the lab's Python
  environment, beside the system Python that runs `make check`: ExoPlaSim from its pinned archive, with netCDF4
  and the other packages of `lab/requirements.txt`.

**Comparisons with Terluna.** A comparison reads Terluna's records and output in place, under the Terluna
roots, and reports where the lab's values differ from them and why. It files nothing in the store, and the
lab's studies take their parents from runs the lab made.

## Native code

Work that needs the speed or the numerics of compiled code is written in Fortran, as the models are, and
scaffolding, data handling and orchestration stay in Python (the author's direction of 2026-10-18). That day
the tools were timed on one thread at nice 19, with the machine's load average at 2–7, on synthetic optics
except for the geoid and the line absorption, which read their real inputs; their logs were read beside.
Four kernels were picked out, each called from Python:

| Kernel | Today | In Fortran |
|---|---|---|
| The two-stream solver (`python/atmosphere/radiative_convective/shortwave.py`), inside every reference column | NumPy on one thread: 0.77 s for a slab of 47 layers and 40,000 points | 0.12 s, within 10⁻¹¹ of NumPy |
| The sky's scattering solver (`python/illumination/sky/solver.py`): 37 minutes of each ledger on 6 threads | numba | 1.3–1.5 times faster, equal to the last bit with `-ffp-contract=off` |
| The ledger's beam step (`python/climate/gcm/twilight.py`, `illumination/sky/solved_transport.py`): 412 of the step's 523 s | numba | 3–4 times faster with its loops reordered |
| PlaSim's radiation, as the shortwave and longwave fits call it (`python/climate/gcm/plasim_shortwave.py`, `plasim_longwave.py`) | Python copies of `radmod.f90` | PlaSim's own patched routines, compiled from `models/exoplasim/`'s series, so that the fits run the model's own code |

The row loop of the correlated-k overlap (`python/atmosphere/radiative_convective/ck.py`) becomes NumPy
array operations. The line absorption, already batched with FFTs, and the longwave, whose exponentials ran
only 1.3–1.6 times faster in Fortran, stay in Python, as do the GRAIL geoid (1 s), the seas and lakes (about 20 s) and
the lab's own code.

- **Where.** Each kernel's Fortran sits beside its Python tool, built by `make` with its flags in the build's
  key and called through C bindings. PlaSim's routines compile from the patched upstream source in
  `models/exoplasim/`, with their Python bindings beside the fits in `python/climate/gcm/`.
- **Acceptance.** A kernel replaces its Python once it agrees with it within its stated numerical tolerance,
  with the same spectral channels and scattering orders where those are chosen as it runs (plan.md, stage
  5). Its tests run under `make check` wherever gfortran is, the sky solver's among them, which pytest leaves
  uncollected where numba is missing.
- **Threads** follow the models' `OMP_NUM_THREADS`, within the machine budget.

## Jobs and the machine

Terluna's two run scripts already lock, run in segments, resume and stop on request, and the lab keeps each
of these.
It adds:

- **A machine budget,** set per machine: total threads (half the cores here), memory and disk, which the
  runner allots among its jobs; nice 10; and a minimum of free disk and a load-average ceiling, which the
  runner checks before it starts each job.
- **Thread variables set explicitly:** `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMBA_NUM_THREADS`.
- **Chains as queued targets,** replacing the shell scripts in `session-tools/`.
- **Disk planning before a case starts.** A 3-D box at Jura's size writes 54 GB over two lunar days.

## A session with the lab

Intended commands, to be built in plan stages 1–8:

```sh
lab reach moon/open-moon                         # what is repaired, what needs a refit, what is refused
lab new scenario moon/open-moon-0.960 --extends moon/open-moon --set sunlight.scale=0.960
lab new study open-moon-0.960 --extends open-moon --scenario moon/open-moon-0.960   # runs and cases, own keys
lab plan open-moon-0.960                         # stale products, their order and their cost
lab make open-moon-0.960                         # fits, builds, GCM runs and CM1 cases, within the budget
lab diff open-moon:design open-moon:design_lw_ice                     # resolved inputs that differ
lab status                                       # the runner's jobs: running, waiting, stopped, with progress
lab stop open-moon-0.960:design                  # the runner writes the job's stop file; it resumes later
```

## Decisions

**Taken by the author on 2026-10-17, 18 and 19:**

| Decision | Choice |
|---|---|
| Home | The `lab/` directory of world-crafting, beside the verified patches, tools and notes: the package in `lab/worldlab/` and its tests in `lab/tests/` |
| Self-contained | What the lab uses for its own work lives in world-crafting and its store; Terluna's files serve the comparison tests alone (Principles) |
| An ensemble of its own | The lab's design, numerics and code are chosen for its own work; it compares with Terluna's records within tolerances and reproduces none of Terluna's runs byte for byte, as the author directed on 2026-10-18 (Principles) |
| Patches | Builds apply the `models/` series alone, which `models/check_patches.sh` applies to the pinned upstream sources |
| Format | TOML specifications, with sources as comments beside values; JSON products and records, in the form of Terluna's products |
| Runs | The lab's own runs begin once stages 2–3 have checked its inputs and builds and stage 7's runner holds them to the machine budget, and they are filed in its store; Terluna's runs stay in Terluna's folders, where the comparisons read them |
| CM1 compiled once | Planned patches read gravity, CO2 and O2 from the namelist; once they pass plan stage 3, one build of each patch set serves every world (Model adapters) |
| The flagship | A family of low-gravity waterworlds after Arnscheidt, Wordsworth and Ding (2019): their steam worlds first, to evaluate the ensemble against the paper, then Gaean air over the same bodies, then protection where that air lasts too briefly ([waterworlds.md](waterworlds.md)); the Open Moon, compared with Terluna's results, is the lab's test case (2026-10-19) |
| Later additions | The Moon at 1.0 atm, the same body with every calibration refitted; Mars at 1 bar, a new column and ledger inside RRTMG's range; and a slowly rotating Earth-like planet, which needs the general repairs alone. The decision of 2026-10-17 placed them after the Open Moon, and since 2026-10-19 they wait as possible additions after the waterworlds |
| Internal forms | Where a form of the lab's own serves its computation better, each kind of quantity keeps that one form, and readers convert outside data into it on import, recording the conversion (2026-10-19; Principles) |
| Outside an envelope | The lab refuses the run unless explicitly overridden, warns clearly even then, and records the override (Principles) |
| The Earth control's test | Global means within two standard deviations of the released run's yearly means (Principles) |
| The longwave correction | Refitted with ice optics on, since it was fitted with them off (regeneration.md, example d) |
| Engine | A custom runner, a small local service with its job queue in the store; the command line is its first client, and a user interface can be a second ("The stage graph and staleness") |
| Workflow | The lab's code follows AGENTS.md's software workflow, in small tested changes each reviewed once; drafts and review rounds stay with the paper |
| Native code | Work that needs compiled speed or the models' own numerics is written in Fortran, and scaffolding stays in Python, as the author directed on 2026-10-18 ("Native code") |
| Time-step guard | A warning where a run's largest 3-day-mean wind passes 90% of the advective limit, `guards.wind_share_of_limit` in ExoPlaSim's defaults; the hottest of Terluna's 45 scanned runs, all stable, reached 83.5% (`lab/validation/timestep_guard.json`, which holds no unstable run) |

**Proposed values,** kept as data that later work may change without code:

| Decision | Choice | Reason |
|---|---|---|
| Registry thresholds | The schemes that hard-code Earth's gravity refused beyond 0.5% from 9.81 m/s²; a ledger of the world's own column required beyond 10% from Earth's horizon air mass of 35; the thin-shell warning above H/R = 0.01; the soil-layer warning beyond 10% of the day's depth; the equinox-Sun warning above an obliquity of 5° | 0.5% passes the Earth control's 9.80665 m/s², 0.01 is about 7.5 times Earth's H/R, and 10% admits Terluna's lunar layers (`lab/registry/earth_assumptions.toml`) |
| Target stage and seasons | The target stage averages each run's last ten model years and stops within 0.1 K or after six runs; a CM1 case's GCM reference averages ±15° of solar longitude around its season | Ten years, as Terluna's ring references average; Terluna's trials stopped at 295.02 K, within 0.1 K; ±15° spans a twelfth of the year |
