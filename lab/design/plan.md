# How the lab is built

Each stage has a product and an acceptance check, and is marked done once its check has passed and been
recorded. A stage that builds on another waits for that record, so the work runs from the specifications,
through the lab's own inputs, builds and producers, to its runs. Until the lab has runs of its own, a check
that needs a GCM run's output or a reference column takes Terluna's, read in place as test input, and
compares the result with Terluna's product. A world's first GCM run takes each calibration at its identity
default, the released model's own value, with the twilight table and the longwave correction off; the
fixpoint of stage 8 then fits stage 5's calibrations on the lab's own runs and runs again until they settle.
The stages are built under AGENTS.md's software workflow: small changes committed on `lab`, each with its
tests, `make check` and one code review, and the design documents changed with the code they describe.

The Open Moon is the lab's test case, at the author's direction of 2026-10-19. Its stages compare the lab's
products with Terluna's within stated tolerances, so that each link of the chain, from the specifications to the
CM1 cases, is checked against earlier results before it serves other worlds. Where the lab's own choice for the
Moon differs from Terluna's, a check runs the code at Terluna's choice as well and records the difference's cause,
as the geoid's check at degree 200 did (`notes/geography.md`), and the lab refines the Moon's own data further only
for a study that needs it. The flagship study, a family of low-gravity
waterworlds in steam and in Gaean air, follows in stages 9 to 13 ([waterworlds.md](waterworlds.md)). It takes the
place the Moon at 1.0 atm held after the Open Moon, and the Moon at 1.0 atm, Mars at 1 bar and a slowly rotating
Earth-like planet wait as possible later additions.

| Stage | Product | Acceptance check | State |
|---|---|---|---|
| 0. Design | `lab/design/`; seed specifications in `lab/worlds/`, `lab/configs/` and `lab/studies/`; the registry seed | The author has answered the design's open questions and closed it for coding (architecture.md, "Decisions") | Passed on 2026-10-18. The thresholds, the target stage's tolerances and the season window stay proposed values in the data, which later work may change without code; the time-step guard's share became the author's choice in stage 1 |
| 1. Specifications, data and derivations | The package in `lab/worldlab/` and its tests in `lab/tests/`, which `pyproject.toml`'s `testpaths` and `pythonpath` gain so that `make check` runs them; `worldlab.spec` (load, `extends` and `set`, resolve, hash), `worldlab.derive` with every quantity of world_spec.md's table (gravity with the spin term, CM1's scale-height, capillary and soil factors, the Sun's declination, ExoPlaSim's output steps and time-step limit), `worldlab.sunlight` with the sunlight at the top and the ice-optics weights, and the data manifest, with the data the seeds pin copied into the store with their provenance | As listed under "Stage 1: checks" | Passed on 2026-10-18: the loader, the derivations, the data manifest, the sunlight and the guard's evidence (`lab/worldlab/spec.py`, `derive.py`, `data.py`, `sunlight.py`, `winds.py`, `lab/data/manifest.toml` and `lab/validation/timestep_guard.json`) pass their checks against world_spec.md, the paper, ExoPlaSim's own `configure` and PlaSim's own calendar, their comparisons with Terluna's records hold within their tolerances, and the store holds the manifest's files. The pressure at the surface's lowest point moved to stage 2, as the author agreed on 2026-10-18, with the geography producer that computes the heights and seas it needs; the loader's field tables, reference levels and source comments moved to the stages that first read them (world_spec.md, "Settled in code") |
| 2. ExoPlaSim inputs | The ExoPlaSim adapter's input writer, for worlds with land and for worlds all ocean, turning freely or locked to their star; the geography producer, with Terluna's `atlas.py` and `drainage.py` brought into `python/geography/`, for the seas from the heights, the lakes and the T21 surfaces, and the air's pressure at the surface's lowest point from them; ExoPlaSim's builds, keyed by their patch series; the planned patch 11, which reads the ice-optics weights from the namelist | From the `open-moon` study and `exoplasim/defaults`, the lab writes the files of the first design run ("Stage 2: files") from its derivations, the manifest's data and the geography producer's surface, with each calibration at its identity default. Given calibration products, the writer writes their values, and given a ledger, the twilight table; for the run with the longwave correction and ice optics it adds `lwcorr.dat` and the namelist entries its switches need. Each namelist entry that ExoPlaSim's own `configure` also sets equals what `configure` writes, but for the output steps and the star files' names, which the lab sets by its own rules (`exoplasim.DEPARTURES`). From a seed waterworld, all ocean and locked to a red dwarf whose values stay provisional until the author's choice for AD Leonis (waterworlds.md), the writer writes ExoPlaSim's aquaplanet and synchronous settings and the star's light files, and there too each entry that `configure` also sets equals what `configure` writes. The geography producer's seas and lakes are compared with Terluna's `atlas_28pct_4ppd` and `drainage_28pct_16ppd`, and the run's inputs with those of Terluna's design run, `A28_corrected_970`, each difference listed with its cause. At its identity default, patch 10's constants, patch 11 leaves the output byte for byte as the build without it | Under way: the geography tools brought from Terluna (82b4b59) and generalised for any world, with the Moon's heights above its geoid read through the manifest, and the Open Moon's seas and first lakes, routed over those heights from the pinned runoff of Terluna's run A28_dim5_moon, their surface on ExoPlaSim's Gaussian grid and the air's pressure at the lowest point (`lab/worldlab/geography.py`, `notes/geography.md`); the writer's namelists and input files (`lab/worldlab/exoplasim.py`), checked against Terluna's design run, file by file with each difference's cause, and against ExoPlaSim's own configure; the waterworld, the builds and patch 11 next |
| 3. CM1 builds and cases | Build keys from patch sets and compile constants; the case writers and the GCM-to-CRM extraction; the core patch that reads gravity, CO2 and O2 from the namelist; the planned patches for rain's mean-diameter cap, the soil layers and the Sun's declination, each reading its value from the namelist, appended after core 17 and electrified 9 (architecture.md, "Points in the series") | Over a one-day ring segment each, the namelist builds, core and electrified, match builds of the lab's own compiled with the same values and flags, at the Moon's values and at 9.81 m/s². Their output is identical, or differs from the compiled build's by no more than a last-bit nudge of that build does, the test by which Terluna accepted its `-O3` rebuild (`notes/verification_record.md`, "Compiler rebuilds"). At its identity default each planned patch leaves the output byte for byte as the build without it. NSSL's two-moment rain is searched for size limits besides its breakup switch. Timed best of three on a quiet machine, they run within 2% of the compiled builds' wall time. The lab then builds CM1 once per patch set and flags. Run on the output of Terluna's design run and of its 45° N twilight ring as test input, the case writers and the extraction write the files of the study's three cases, and a comparison with Terluna's cases lists each difference with its cause; the lab's own cases follow from its own design run in stage 8 | To start |
| 4. Stage graph and planner | Keys, headers, declared read sets, staleness, `plan` | Keys computed from a study extending `open-moon`, which runs on the lab's own stages, before and after each of regeneration.md's worked changes differ for exactly the products the example lists; with nothing changed, no key changes. A declared pair whose resolved inputs or build flags differ outside its delta is refused, as a twilight case would be whose control was compiled with other optimisation flags (defect log C8) | To start |
| 5. Producers and calibrations | Stages for the ledger, the gas bands, the shortwave and longwave fits, the water continuum and the ice optics, with their envelopes; the glow producer; the target stage for the sunlight scale; the Fortran kernels of the two-stream solver, the sky's scattering solver and the ledger's beam step, and PlaSim's own radiation routines for the fits (architecture.md, "Native code") | Each passes the checks of its own physics that it states, and its products, compared with Terluna's from the same inputs, differ by no more than its stated tolerance or by a stated cause. The water-continuum stage, which replaces Terluna's hand trials, is compared with their `TH2OC` of 0.004 from the same cloud-free columns at 280 and 310 K. A test fails wherever a tool falls back on its own Earth defaults for the air or the ground albedo. Each Fortran kernel agrees with the Python it replaces within its stated numerical tolerance, with the same spectral channels and scattering orders where those are chosen as it runs, and its tests run under `make check`. The target stage, replayed on Terluna's trial runs at 0.9655, 0.9685 and 0.970 with their recorded global means, takes its secant steps and records where its tolerance stops it | To start |
| 6. Registry and reach | `lab/registry/`, completed from the defect log's classes (a) and (b); the reach report | The report reproduces the paper's table of reach for the worlds of `paper/data/worlds.json`, ten on 2026-10-17 | Fourteen-entry seed drafted |
| 7. Jobs | The runner, a local service with its job queue in the store, and the job wrappers it starts within the machine budget | In tests, the runner holds a job back while the load exceeds its ceiling or free disk falls below its minimum; a restart mid-queue finds every job where it stood; and a client stops, resumes, cancels and reorders jobs | To start |
| 8. The first runs: the Earth control and the Open Moon's fixpoint and cases | The Earth control's study, `studies/earth-control.toml`, and its two runs, the first the lab makes itself. Its calibrations are the released model's own values for the shortwave multipliers and the water continuum (`model-default`, world_spec.md rule 5), and the ledger and gas-band fits of Earth's own column from stage 5's tools; the Open Moon's first design run, at identity calibrations, and the fixpoint stage on it, in the `open-moon` study, the target stage finding the sunlight scale in each pass (architecture.md, "Calibrations, envelopes and loops"); the study's CM1 cases, forced from the settled design run; the raindrop sensitivity, the 45° N ring with Morrison's own limits and with the capillary scaling | The pipeline's Earth run passes the Earth control's test against the released run. The fixpoint starts from the lab's first design run, and its passes fit stage 5's calibrations on the lab's own runs, the longwave correction with ice optics on. Each pass is recorded, and the stage stops within its tolerances or at its pass limit, recording which. Each run passes its registry and envelope checks before it starts, and its post-run envelope check is recorded with it. The target stage meets the reference temperature within its stated tolerance or records where it stopped. The raindrop sensitivity records the rain reaching the ground and the share of falling water that evaporates under each | To start |
| 9. The steam column and the reproduction | A one-dimensional model of a waterworld under steam alone, in `python/`, built on the radiative–convective column: hot water's lines, the radiating surfaces under gravity falling with height, the energy balance, the isothermal wind and the water's lifetime, mapped over gravity and surface temperature and then over gravity and distance from each star; the size from the paper's relation and the stars as blackbodies; the water lines in the manifest after their rights review (waterworlds.md, "The reference study") | Over the paper's ranges, the lab's maps give its transition at g ≈ 1.48 m/s² and 0.0268 Earth masses for both stars, its habitable zones about 0.08 and 0.008 AU wide at their widest, and the curves of its Figures 3 to 5, digitised, within the tolerances the author sets when the stage is built; each difference is listed with its cause, the lab's choices for the inputs the paper leaves unstated among them. On the radiative–convective tool's own checked columns, 250 to 360 K, the column with hot water's lines gives that tool's outgoing longwave within a stated tolerance | To start. It needs stage 1 alone and can proceed beside stages 3–8 |
| 10. Escape and the upper air for any world | Terluna's thermal column (`atmosphere/thermal_column.py`), its exobase and escape model (`atmosphere/middle_atmosphere/escape.py`), its tracing of the heat that filtered light leaves along slant paths (`atmosphere/middle_atmosphere/limb_heat.py`, with `fetch_limb_inputs.py` and `limb_inputs.json`) and its loss response (`atmosphere/loss_response/`), with the modules they import that `python/` lacks, such as `protection/spectra/annulus_film.py`, brought into `python/` byte for byte under their Terluna paths and generalised for any body and star, as stage 2 generalised the geography tools; a star's X-ray and extreme-ultraviolet spectrum and its history, by pin; for steam, stage 9's wind heated by that light and cooling as it rises | On the Open Moon the generalised tools give Terluna's recorded exobase temperatures and losses within stated tolerances, each difference with its cause; on a steam world at the paper's settings, the escape equals stage 9's isothermal wind | To start. It needs stage 1, and stage 9 for steam |
| 11. The waterworld survey | Maps in one dimension for each star: the steam worlds under the lab's physics, each change from the paper's simplifications measured alone; Gaean air over the same bodies, with its cold trap, its water's loss and the losses of its nitrogen and oxygen; the four diagnostics mapped apart; and the anchors chosen from the maps (waterworlds.md, "The work, in order") | Each map records the inputs and evidence state of its points, and each boundary its diagnostic and horizon; at the paper's settings the steam maps give stage 9's; the anchors are recorded with the reasons for their choice | To start, after stages 9 and 10 |
| 12. The anchors in three dimensions | Each anchor's world and scenario files and its study; ExoPlaSim's runs in Gaean air, all ocean, locked to AD Leonis or turning around the Sun, each with its fixpoint; CM1 cases over the open ocean at one or two anchors, under a star fixed in the sky where the world is locked, through a planned CM1 patch with an identity default; SWAN's adapter, for the patched build in `models/swan/`, and its runs over the global ocean at one or two anchors, forced by their winds | Each run passes its registry and envelope checks before it starts, and its post-run check is recorded with it; each anchor's global means and profiles are compared with the survey's column at the same point, each difference with its cause. Before the anchors' wave runs, SWAN's adapter writes the inputs of a lunar sea of Terluna's and its run gives Terluna's recorded sea states within stated tolerances, each difference with its cause | To start, after stages 8 and 11 |
| 13. Protection where it is needed | For each anchor whose Gaean air lasts less than the horizon, the least attenuation of the star's ultraviolet and the least shelter from its wind that keep the air, from stage 10's tools; then the shield's design for a planet alone with its star, near the star–planet L1 point | The protected air lasts the horizon in stage 10's tools, and the shield's design is checked for its station against the star's gravity and light, its size and its optics | Follows stages 11 and 12, where their findings call for it |

## Stage 1: checks

- **Compared with Terluna's records.** The Moon's derived values agree with those Terluna recorded within
  each comparison's stated tolerance, or differ by a stated cause, such as the spin term in the gravity:
  - gravity and the partial pressures in `progress.json` of `A28_corrected_970`;
  - the build macros in `build.json`;
  - `var16` and `var19` in each ring case's `namelist.input`, and `grid.nx` and the ring length in its
    `case.json`;
  - the CM1 lengths, time step, boundary-layer length and damping rate scaled from `cm1/defaults`, against
    Terluna's ring settings.
- **Against ExoPlaSim.** `N_DAYS_PER_YEAR` and `ROTSPD` from `worldlab.derive` must equal what ExoPlaSim's
  own `configure` writes, and the model day and steps per model day what `plasim.f90:1287-1348` computes
  from them:
  - for the Moon;
  - for Earth, at `rotationperiod` 1, where the year sets the days (365);
  - for the periods in `exoplasim_slow_rotators` of `paper/data/regime_calc.json`;
  - on either side of the rounding's steps, where N falls from 36 to 24 just above 12 days and from 24
    to 12 just above 20 days.

  Both run in the lab's environment (`lab/requirements.txt`), whose pinned ExoPlaSim 3.4.2 compiles PlaSim the
  first time a run asks for it; PlaSim runs one step for the Moon, Earth, the 243-day rotator and either side of
  the step at 12 days, and its diagnostics give the model day and steps it computed (`lab/tests/test_exoplasim.py`).
- **The time-step guard.** At 90% of the advective limit, the author's choice of 2026-10-18, it stays silent on
  the largest 3-day-mean winds of Terluna's 45 lunar runs, all stable at 30 minutes in 526 model years; the
  hottest, `A28_corrected_970_lw_ice`, reached 38.4 m/s in its year 9, 83.5% of the 46.0 m/s limit, where the 80%
  first proposed would have warned (`lab/validation/timestep_guard.json`, made by `lab/worldlab/winds.py`). The
  record holds no unstable run, so it shows the guard silent on stable runs and leaves its warning ahead of
  instability to a run that goes unstable.
- **Against the paper.** The quantities world_spec.md derives agree with `regime_calc.json` to one part in
  10¹² and with `worlds.json` to its stated digits, each from the basis its row states, as `regime_calc.json`
  takes g = GM/R² and `worlds.json` states each world's g and temperature:
  - in `paper/data/regime_calc.json`: the gravity, column mass, scale height, horizon air mass, capillary
    length ratio, rotation, soil wave depth ratio, PlaSim calendar, Sun-clock skip and slow rotators;
  - in `paper/data/worlds.json`: each row's scale height, H/R, column mass and horizon factor.

  The paper's other entries, such as retention, flash density and the seas, stay the paper's.
- **The sunlight and the ice-optics weights.** A blackbody star's total equals its constant to 10⁻¹², and its
  band shares equal the blackbody's own by quadrature to 10⁻⁶; a blackbody sampled as a `shape` extends to that
  blackbody to 10⁻⁵, and an `irradiance` keeps its values while its tails fill the rest of the constant.
  Terluna's rule on the same TSIS-1 file gives patch 10's four constants to their four places, and on the same
  files the shield flux its record holds to 10⁻¹²; the lab's figure differs from that by its tails' passage at
  the shield's own transmission, stated to 10⁻¹².
- **The data manifest.** Every pin the lab's own stages read resolves within world-crafting and the store,
  with its hash, source, licence and credit recorded. Data from outside Terluna, such as LOLA, GRAIL and
  TSIS-1, pass the review of redistribution rights that AGENTS.md requires before they are copied. Terluna's
  other files are read in place, by the comparison tests alone.
- **Without Terluna.** With Terluna's paths absent, the stage's tests pass and the comparisons with Terluna's
  records report themselves skipped.

## Stage 2: files

For the design run, the lab writes:

- the namelists;
- `sun.dat` and `sun_hr.dat`, the sunlight through the filter;
- `twilight.dat`, from the ledger;
- the land mask and the surface heights, as `.sra` files, from the seas, the lakes and the heights.

Each follows from the lab's derivations and products. The comparison with Terluna's `A28_corrected_970`
lists, file by file, the entries that differ and why.

## Order and cost

- **Stages 1, 2, 4 and 6** cost seconds to minutes of one core.
  - Stage 1 copied 3.3 MB of Terluna's data, the shield's transmission and the lakes file whose 86 kB runoff
    climatology took its place in stage 2, and downloaded 45 MB from LASP and the PDS, in 5 s on 2026-10-18.
  - Stage 6, mostly data entry from the defect log, can proceed beside stages 2–5.
- **Stage 3 runs CM1 for its checks:** one-day ring segments of about 5 minutes each on 6 threads, three
  for each build timed.
- **Stage 5** runs the reference tools and so waits for a quiet machine.
  - The ledger takes about 40 minutes of solving on 6 threads, and the ledger step itself about 9 minutes.
    Its optics caches take 0.1–0.4 GB each (`notes/reference_radiation.md`, section 3).
  - The shortwave and longwave fits take minutes, reading the output of the runs they are fitted on;
    Terluna fitted its own on `A28_dim5` and `A28_corrected_970_heating`.
- **Stage 8 runs the models.**
  - The Earth control's two 20-year runs take about 75 minutes each: an Earth year at a 30-minute step has
    17,520 steps, against the Moon's 17,160.
  - The target stage takes three or four GCM runs of about 75 minutes, as Terluna's trials for the Open Moon
    took three, and the raindrop sensitivity two two-lunar-day rings of about 4.5 hours each.
  - A GCM year took 218 s on 4 ranks in `A28_corrected_970`, and 278 s in `A28_corrected_970_lw_ice` with
    its heating diagnostics, so 20 years take about 73–93 minutes.
  - Each one-day segment of the 45° N twilight ring took about 275 s on 6 threads, so its 59 days took 4.5
    hours. That ring wrote 8.5 GB, and the Jura box 54 GB over the same two lunar days.
- **Stages 9 to 11 run one-dimensional columns.** The authors' method computes the radiation once over a grid of
  gravity and surface temperature, and the maps then solve the energy balance on that grid, so the cost lies in
  the line-by-line columns, timed when stage 9 is built. Stage 9 needs stage 1 alone, and stage 10 needs stage 1
  and, for steam, stage 9; both can proceed beside stages 3–8.
- **Stage 12 runs the anchors.** At the Open Moon's 73–93 minutes for about 20 years of model time, six anchors'
  first runs take seven to nine hours of the machine together, and each fixpoint pass about as much again; CM1
  runs at one or two of them.

## What the lab takes from Terluna

- **Copied once into the store, with their provenance:** the two Terluna files the seeds pin for the lab's own
  stages, the shields' transmission `protection/spectra/shield_transmission.json` (0.6 MB, stage 1) and the
  climatology of run A28_dim5_moon, `climate/gcm/products/climatology_A28_dim5_moon.npz` (86 kB), whose runoff the
  lab routes into the Open Moon's first lakes (stage 2, in place of Terluna's lakes from the same runoff,
  `geography/products/drainage_28pct_16ppd.npz`, routed over Terluna's heights and copied in stage 1, which the
  comparisons now read in place, while the store keeps the stage-1 copy outside the manifest at the author's word
  of 2026-10-19; Terluna's Git ignores its products folder, so the copy there may be overwritten);
  `shared/constants.json` is in the repository
  already, as `python/shared/constants.json`, byte for byte as at 186b294. The TSIS-1 spectrum comes from LASP,
  and LOLA's heights and the GRAIL geoid from NASA's Planetary Data System, by the hashes Terluna recorded
  (`atmosphere/radiative_convective/inputs.json`, `geography/inputs.json`). `lab/data/manifest.toml` records
  each file's source, hash, licence and credit.
- **Brought into `python/` under their Terluna paths, with provenance:** in stage 2, `geography/atlas.py` and
  `geography/drainage.py`, which flood the heights to a seas share and route runoff into lakes, with the modules
  the atlas imports, `topography.py` (the heights above the geoid), `basins.py` (the levels and the connected
  seas), `nomenclature.py` (the gazetteer's names) and the input restorer `fetch_inputs.py`, and their tests,
  brought byte for byte from 186b294 on 2026-10-18 (82b4b59) and generalised the same day for any world, the lab's
  data manifest and specifications taking over from Terluna's input restorer and water scenario; in stage 5,
  `research/studies/solar_shield_array/glow.py`, which computes the infrared of a glow in space; in stage 10, the
  thermal column, the exobase and escape model, the limb tracing and the loss response (`atmosphere/thermal_column.py`,
  `atmosphere/middle_atmosphere/escape.py`, `limb_heat.py` and its inputs, `atmosphere/loss_response/`), with the
  modules they import, such as `protection/spectra/annulus_film.py`, and their tests.
- **Read in place by the comparison tests alone, where Terluna is at hand:**
  - `climate/gcm/exoplasim_run.py`, `climate/crm/cm1_run.py` and `climate/crm/cm1_elec.py`, Terluna's set-up
    of its runs, which the comparisons cite;
  - `climate/gcm/products/`: the planet record and the T21 surfaces;
  - `geography/products/` and `geography/results/`: the atlas, the drainage and its summary, and the level
    table, with which stage 2 compares the geography producer's seas and lakes;
  - `climate/results/gcm/`: the ledger, gas-band, shortwave and longwave products;
  - `gcm-runs/<run>/`: `progress.json`, `inputs/`, `model/*_namelist` and the yearly output
    `model/MOST.<year>.nc`, for the comparisons, the time-step guard's check and test input to the case
    writers and the producers;
  - `gcm-runs/cal_*`: the hand trials behind `TH2OC`;
  - `crm-runs/<case>/`: `case.json` and the input files, and the rings' output (`cm1out_t*_s.dat`), for the
    comparisons and the box's day–night forcing in stage 3's test;
  - `cm1/build/<label>/build.json`, whose macros stage 1 compares;
  - `atmosphere/middle_atmosphere/results/` and `atmosphere/loss_response/results/`, with which stage 10 compares
    the generalised escape tools;
  - `climate/waves/`, Terluna's set-up of its SWAN runs and their records, with which stage 12 checks SWAN's
    adapter.
