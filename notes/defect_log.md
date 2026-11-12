# Defect log: ExoPlaSim, CM1 with WRF-ELEC, SWAN and SWASH

This log lists the defects found while carrying four Earth-built models to Terluna's breathable Moon, from
2026-09-24 on. The defects fall into three classes:

- **(a)** upstream defects that the adaptation exposed;
- **(b)** Earth constants, units, geometry and fitted forms written into upstream code;
- **(c)** defects in Terluna's own adaptation and analysis.

A fourth section, **(d)**, lists inconsistencies in Terluna's record that this pass found and that are not yet
corrected there. The companion note `verification_record.md` describes the checks cited below.

## Conventions

**References.**
- Repository paths are Terluna's at commit 186b294. `climate/gcm/exoplasim_run.py:212` means line 212 of that
  file at that commit. The checkout at `/home/kir/Documents/Projects/terluna` (f03b839) differs from 186b294 only in
  `research/integration/five-branches.md`, so its line numbers match. Entries and findings that Terluna recorded
  after 186b294 (A9, B29–B35, C19, C20 and the updates to B18, B22 and B28) cite the Terluna commit and branch that
  record them, and their paths are at that commit.
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
- **P**: found or checked in the pass of 2026-11-09 by reading the PlaSim source that Terluna's runs import
  (`exoplasim-twilight` on the research drive), the design runs' namelists and output and the pinned CM1 source, with
  arithmetic here. No model was run.

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
| A6 | CM1 r22.0 | Threaded runs part from one another; cause uncertain, most likely CM1's own threaded loops | 10-04, b85eb5c | None; one thread repeats | Paired multithread runs are separate realizations | Open | R |
| A7 | WRF-ELEC | No conduction by default; ion charge persists for weeks in month-long runs | 10-05, e09aa30 | `leakage` (lunar 1), 4499e35 | ~20 kV/m at the ground over the whole box; lightning unchanged | Fixed for lunar runs | R |
| A8 | WRF-ELEC `lightmsz` | Channel reach marked only above threshold `scth` | 10-05, a5205d2 | Flash log takes reach from charge handed to ions | 13 flashes logged no reach | Fixed (logging) | R |
| A9 | CM1 r22.0 | Simple boundary layer (`ipbl = 2`) hands the solver its tendencies multiplied by the air's density | 10-21, Terluna `domain/climate` 13e7123 | `ipbl2_per_mass` (0): the lab's series, patch 01, from Terluna's build `moon_omp_rain_law_pbl` | Boundary layer took 1.32–1.35× the surface's evaporation and 1.46–1.51× its sensible heat; 51 of Terluna's 59 CM1 runs, every reported ring and box among them | Fixed in the lab's series, before any lab run; fixed in Terluna's new builds | R |
| A10 | ExoPlaSim, low-I/O output | `hus` in the mean output is the humidity held from the last output step, where every other field is a mean; the held field is absent from the restart, so each year file's first record holds about 2% of the vapour | 10-27, Terluna `domain/climate` 984606a5 | None in the model; a reader's rule (Terluna's `climate/gcm/year_files.py`) | Read as means, the records misplace the humidity by half an interval, and two windows in every 120 meet air about half as humid | Open here; read by rule in Terluna | R, P |
| B1 | CM1 | `g = 9.81` in dynamics, RRTMG, CAPE and Morrison; Morrison fall speeds and caps at Earth's g | 09-27, 16319e1 | `TERLUNA_G` build constant, which the namelist's `world_g` replaces in the lab's series (patch 06, default the build's value); fall speeds × (g/9.81)^((B+1)/3) | Required for any lunar run | Fixed | R |
| B2 | WRF-ELEC NSSL | `gr = 9.8` twice; fall-speed laws at Earth's g | 10-02 a21a615; 10-04 6027230 | `TERLUNA_G`, still compiled in beside the lab's patch 06; same scaling | Required | Fixed | R |
| B3 | WRF-ELEC NSSL | Rain and cloud-ice ventilation tied to Earth fall-speed coefficients | 10-06, 1fa7f41 | Scaled at 11 places; no switch | Lunar rain evaporated 1.3–1.5× too fast | Fixed | R |
| B4 | WRF-ELEC | Breakdown field capped at 180 kV/m | 10-04, bf2fa5e | `lightning` 4 (lunar 4), 62b4c1e | Cap active below ~36 km in lunar air (44% at the ground) | Fixed for lunar runs | R |
| B5 | WRF-ELEC | Ground strike when a channel reaches air warmer than −7 °C; stopping field 0.15 of breakdown | 10-05, 54ea2b2 | Rule kept as upper bound; leader crossing `var1` (lunar 1 kV/m), ac55dc2 | Ground strikes from none to a fifth of flashes | Bounded | R |
| B6 | WRF-ELEC | 0.75-s sub-step tuned to Earth's 500-m layers and fall speeds | 10-04, 13c839e | `substep_s` (lunar 6.8 s) | One 8-s sub-step per step in the boxes | Fixed | R |
| B7 | WRF-ELEC | Other Earth calibrations: 50 MV, 10 kV/m, 0.9/0.8 of breakdown, 200 V/m, NOx yield, Earth conductivity table, laboratory charging laws | 10-04 to 10-05 | Retained; Takahashi law tested | Polarity depends on the charging law | Open | R |
| B8 | CM1 RRTMG | Earth's trace gases, CO₂ by calendar year, ozone profile | 09-27, 16319e1 | Design CO₂ and O₂ compiled in, which the namelist's `world_co2` and `world_o2` replace in the lab's series (patch 06, defaults the build's values); others zero | Required | Fixed | R |
| B9 | CM1 RRTMG | Uses the Sun's own spectrum, not the shield-filtered one | 09-29, 36e29c4 | None | 5 W/m² of clear-air absorption at 0° E | Open | R |
| B10 | CM1 | Earth-day soil, solar day, damping time and PBL length; Earth's Ω and radius in the beta plane | 09-27, 16319e1; beta plane V | Soil 5–80 cm, its top layer from `soil_dz1` in the lab's series (patch 07, default 0.05 m); `var16`–`var19` Sun, its declination from `sun_decl` there (patch 08, default 0); scaled `rdalpha`, `l_inf`; beta plane bypassed | Required; beta plane reaches no result | Fixed or bypassed | R, V |
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
| B21 | PlaSim, CM1 | Constant gravity and a thin shell in the dynamics | S | None | Not quantified; g is 5.4% lower at 48.6 km; the air over a square metre of ground exceeds p_s/g by about 12% | Open | S, V, P |
| B22 | CM1 RRTMG | Reference pressures stop at 1053.63 hPa; deeper layers extrapolated | S | None | Lowest ~7 km over the sea extrapolated; measured offline, 0.002–0.003 K a day in the lowest layers | Harmless for this air | S, V; R (6f7d7b0) |
| B23 | CM1 RRTMG | Ice optics end at 140 µm | 10-04, 0b9507d | Size passed to radiation capped at 140 µm and logged | Crash at day 6.45 avoided; capped ice 7% optically too thick in the main run | Mitigated | R |
| B24 | SWAN | AGROW knee fixed at 1 Hz | 10-02, 8785f7e | Patched knee at g/g_ref Hz | Similarity error 5.44% → 0.303% in Hs | Fixed | R |
| B25 | SWAN | Air density fixed at 1.28 kg/m³ | 10-02, 8785f7e | Patched to 1.40390 kg/m³ in the coupled build | Not quantified | Fixed in coupled build | R |
| B26 | SWAN | INIT 2-s period; ST6 and exact-XNL paths at Earth's g; Earth radius default | 10-02, 8785f7e | Bypassed or set by input | None in the selected configuration | Avoided | R |
| B27 | SWAN, SWASH | Earth-calibrated laws: Wu drag, Komen, AGROW coefficient, breaker index 0.73, SWASH breaking 0.6/0.3 | 10-02 to 10-03 | Retained | Not quantified | Open | R |
| B28 | CM1 Morrison | Rain's mean diameter capped at 2.8 mm and breakup begun at 0.3 mm, Earth's values | 10-17 | `brkup_gscale` (0), with `brkup_rhor` and `brkup_rhoexp`: the lab's series, patch 03, from Terluna's `RAIN_LIMITS_PATCHES` (dd89cef, 8b55847); patch 04 adds the solver's fall law and the world's self-collection rate (`rain_fall_law`, `rain_selfcoll`; 5a44e5e) | Lunar limits: rain at the ground 33 → 63 mm a lunar day, evaporated share 86% → 48%, air at 2 m +1.47 K | Scaled in the lab's series, off by default, before any lab run; scaled in Terluna's builds | S, V; R |
| B29 | PlaSim | Kuo-type deep convection rains a column's moisture supply wherever an undiluted surface parcel is buoyant | 10-21, Terluna `domain/climate` f07ad8d | In Terluna: simplified Betts–Miller (`nprc` 2) and mass-flux (`nprc` 3) schemes, Kuo kept at `nprc` 1 | Near-side Sea rains 2.9 mm/day after midnight against CM1's 0.14–0.17; upper air within 1.3 K of the undiluted adiabat, where CM1's mixing updrafts hold theirs 3.0–6.3 K below | Open; replacements under test in Terluna | R |
| B30 | PlaSim | Falling rain evaporates by one constant (`gamma` 0.01 in `rainmod.f90`), with no drop size or fall speed | 10-21, 05b1384 | `NEVAPPREC` 2 (PlaSim's own 1 the default), with the six `RDROP` entries and the table `lab_rain_law.txt`: the lab's series, patch 14, rain evaporated from its drops' sizes and fall speeds (Terluna's `rain_drops.py`, 8e805f60, f5f767fa). In Terluna also `--rain-evaporation`, which sets the constant | PlaSim evaporates 29% of its rain against 61% in CM1's boxes; matching takes 0.027 over the sea and about 0.046 over land. With the drops' sizes Terluna's column gives 0.96–1.05 of CM1's column evaporation on three boxes | Replaced in the lab's series, off by default until the Earth control's test; replaced in Terluna's design runs | R |
| B31 | PlaSim | Ten σ levels set for Earth: on the Moon the lowest layer spans 0–1.73 km and one layer 6.4–13.7 km | 10-26, 697ac36, a75fd47 | `levels` (10, the released model's own): a table of a scale height, the released half levels kept and the heights of those below generates a world's set, written as `NEQSIG` −1, `SIGH` and `TFRC`, with a conservative restart remap; no patch (`python/climate/gcm/levels.py`, from Terluna's `levels.py`). In Terluna: 14- and 15-level sets (`--levels`) | The lowest layer averages away 1.4–2.3 kJ/kg of surface-layer moist static energy; CM1's 6 km night boundary layer and 7–8 km cloud tops fall inside one layer | A set generated for the world in the lab, the released ten by default, before any lab run on one; fifteen levels in Terluna's design runs | R |
| B32 | PlaSim | Vertical diffusion's mixing lengths (160 m for momentum, 438 m for heat and vapour) and 1 m/s wind floor | 10-26, b182515; compared 10-27, 21d98fc | The lengths: none yet; a nonlocal scheme with the stretched length, tested in single columns, misses the sea night's stop rule (6d0c707). The floor in the surface transfer: `NGUST` (0), the lab's series, patch 12, Beljaars's gust with a least wind of 0.1 m/s | Over the sea after midnight CM1 mixes to 6.5 km and the GCM to 4.3 km; through the day CM1 carries 28–112 W/m² of vapour through 5.2 km where PlaSim's median diffusivity is 0.1–0.3 m²/s | The lengths open; the floor in the surface transfer replaced by the gust in the lab's series and in Terluna's design runs, and kept in the vertical diffusion's wind shear | R |
| B33 | PlaSim | Free-convection constant over water, 0.0016 m s⁻¹ K⁻¹ᐟ³, from a tank law that scales as (g/p_s)^⅓ | 10-26, b182515 | `NGUST`, `NSIMW` (0, 0): the lab's series, patches 12 and 13, Beljaars's gust with similarity over ice-free water, which drop the term (Terluna's `surface_gust.py`, `surface_similarity.py`). In Terluna also `cfree`, `--free-convection lunar` (0.00083), which has no patch here | Near-side Sea's evaporation 3.82 → 3.62 mm/day at the lunar constant (CM1 2.98), global evaporation and rain 3% lower; with the gust the site's transfer coefficient for vapour falls to 0.67 of the baseline's | Replaced in the lab's series, off by default until the Earth control's test; replaced in Terluna's design runs | R |
| B34 | PlaSim | Shallow convection's tops capped at 700 hPa | 10-25, 1d05c3d | In Terluna: `--sbm-shallow-cap`, tied to the depth test (ea1b62f) | Near 28 km in the Moon's air; binds in 1–1.4% of cells | Open here; switch in Terluna | R |
| B35 | CM1 r22.0 | The MM5 surface layer's gust over water, √Δθv m/s, has no gravity in it; over land the same scheme takes Beljaars's gust from the build's gravity | 10-28, Terluna `domain/climate` 238638f | `gust_over_water` (0): the lab's series, patch 02, from Terluna's `GUST_PATCH` | Raised the sea box's surface wind 1.6–1.8 times, where Beljaars's gust, computed from the box's own fluxes, raises it 1.1–1.2 times; every CM1 run over the seas behind the paper's first released draft | Fixed in the lab's series, before any lab run; fixed in Terluna's new builds | R |
| B36 | PlaSim | Horizontal diffusion's damping times at the truncation scale, 0.2–5.6 Earth days, Earth's for T21 | 11-09 | None | Unmeasured; the Moon's smallest wave is 3.7 times shorter than Earth's and damped as slowly | Open | P |
| B37 | PlaSim; CM1 set-up | A slab sea 50 m deep, Earth's seasonal mixed layer; CM1's sea boxes hold its mean temperature | 11-09 | `MLDEPTH` (50 m) | The sea site's surface swings 0.63 K through the lunar day; 2.5 to 5 times that in a layer of 10–20 m, by estimate; Terluna's calm column reaches 37.1 °C where the slab shows 30.9 °C | Open | P, R |
| B38 | CM1 Morrison | Cloud turns into rain at Earth's rates: Khairoutdinov and Kogan's autoconversion and accretion carry no gravity | Limit noted 10-17; sized 11-09 | `rain_autoconv_fac`, `rain_accr_fac` (1 each): the lab's series, patch 05, the lab's own | Unmeasured; by scaling, rain forms about 6 and 3 times too readily in each passage through a lunar cloud | A switch in the lab's series, off by default; its effect unmeasured | V, P |
| B39 | PlaSim, Terluna's `nprc` 2 | The simplified Betts–Miller scheme relaxes over 2 h, Frierson's value for Earth | 11-09, `lab/design/gap_series.md` | `tau_bm` (7,200 s) | Unmeasured; 12 h by similarity | Open | P |
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
| C19 | CM1 set-up | Nudging toward the GCM from 8 km (full at 16 km), with the day–night table stopping at 16 km | 10-21, Terluna `domain/climate` 13e7123 | Site forcing through the column, each layer's total kept, air held only above the GCM's convection top (`gcm_site.py`; 2cc5179, 5a44e5e) | Sea box: the nudging supplied 89 of the 107 W/m² its radiation removed, rain 0.06 against the GCM's 2.72 mm/day; the interpolation dried the column 0.55 mm/day | Fixed in Terluna's site boxes; every earlier ring and box ran it | R |
| C20 | CM1 analyses | Stored radiative tendencies (`lwten`, `swten`, at constant volume under `eqtset = 2`) read as rates at constant pressure | 10-20, Terluna `domain/atmosphere` fe49ad9 | Conventions in `climate/crm/cm1_output.py`: × cvm/cp against another code, × cv/cp in a θ budget | Radiation overstated by 38–40%: the extra RRTMG cooling of 4.5–10.2 W/m² and the 45° N ring's heat budget | Fixed | R |
| C22 | GCM and CM1 set-up | Sunlight taken at the Earth–Moon barycentre's distance: the Moon's monthly swing toward and away from the Sun left out | 11-09 | None | ±0.51% of the sunlight through each lunar day; the far side's noon 1.0% brighter than the near side's | An idealisation of the scenario, stated with it; an option in the lab | P |

## (a) Upstream defects exposed by the adaptation

The paper's first released draft (tag `paper-v1`) classes these items as follows. A3 (the 360-day calendar) is a
limitation in units of time, avoided by configuration; A7 (WRF-ELEC's missing clear-air conduction) a simplification
that holds for runs of hours; A8 (the flash log's reach threshold) a constant on the lunar path. Its four defects in
the released codes are A1, A2 and B11 (ExoPlaSim's convective-cover unit, classed here under (b)), which produce
little or no error at Earth's values, and A5, hidden by SWAN's usual configuration. A9, CM1's simple boundary layer,
makes a fifth on the lunar runs' path; the draft predates it, and its error, which grows with the air's density,
reaches Earth's runs as well. A6, the parting of CM1's threaded runs, most likely in CM1's own threaded loops, and
A4, PlaSim's cold lowest level, are faults of uncertain cause, since stock CM1 has yet to run with these cases'
options, which would place A6 in or out of the released code.

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
  the domain's total vertical momentum. The plain Morrison box parts too, so at least one source of the parting lies outside the
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

### A9. CM1 r22.0: the simple boundary layer's density-weighted tendencies (R)

- **Defect.** With `ipbl = 2`, `turb.F`'s block for the simple scheme calls `turbsz` for θ, qv, qc and qi and
  `turbuz` and `turbvz` for the wind. `turbsz` ends with `turbz(i,j,k) = rho(i,j,k)*(dumz(i,j,k)-s(i,j,k))*rdt`
  (`turbtend.F:686, 697`), and `turbuz` and `turbvz` with the mean of the neighbouring densities times the wind's
  change (`:1541, 2333`), while `solve1.F` adds the arrays as changes per second (`:1208, 1500`). YSU, MYNN and MYJ
  fill the same arrays with WRF's tendencies per second (`turb.F:2264, 2619, 2817`), so the fault is the simple
  scheme's alone.
- **Found** on 2026-10-21 by the closed heat and water budgets of Terluna's CM1 boxes (`domain/climate` 13e7123).
  The lines above were checked in pristine cm1r22.0 the same day; NCAR's main branch holds the same code.
- **Effect.** Under air near 1.4 kg/m³ at the ground, the boxes' boundary layer took 1.32–1.35 times the surface's
  evaporation and 1.46–1.51 times its sensible heat, with the drag inflated alike. Of Terluna's 59 CM1 runs, 51 used
  the scheme, every ring and box the paper reports among them. Boxes run with the fix and the corrected forcing
  (C19) stay 1.15 K over land and 0.23 K over the sea warmer than the GCM at 2 m, where the September rings ran
  2.4–4.7 °C warmer over land and 1.8–2.4 °C over the seas; the boxes also differ in site and forcing state, and
  Terluna reads most of the rings' warmth as this fault, which one corrected rerun of a reference ring or box, the
  step Terluna's plan recommends, would size. On
  Earth, where the boundary layer's air weighs 1.0–1.2 kg/m³, the code implies up to about 20%, untested on an
  Earth case.
- **Fix.** Divide the density out at the end of the `ipbl = 2` block, as Terluna's build `moon_omp_rain_law_pbl`
  does; its boundary layer passes on 0.995–1.000 of the evaporation. Patch 01 of the lab's `models/cm1/series-lab` makes the
  same fix, switched by `ipbl2_per_mass` (default 0, CM1's own scheme); its sources compile, and stage 3's CM1 builds
  will measure its effect in the lab's runs. `solve1.F` then averages `upten` and `vpten` as fields at scalar
  points, while this scheme fills them at u and v points, and the patch leaves that averaging as CM1 has it.
  `models/cm1/upstream-ipbl2-density.md` drafts the report to CM1's developer.

### A10. ExoPlaSim: the humidity in the mean output is a held value (R; code read P)

- **Defect.** In low-I/O mode (`nlowio`) ExoPlaSim adds each field to its output mean at every step. With spectral
  humidity (`nqspec = 1`) the field it adds for `hus` is recomputed only at output steps (`plasim.f90`, the test
  `mod(nstep,nafter)==0 .and. nqspec == 1` ahead of `sqout`), so each record holds the humidity at the end of the
  interval before it, where the temperature, pressure, winds and fluxes beside it are means (the gridpoint
  diagnostics are single steps by design). The held field is absent from the restart, so a call's first record lacks
  the steps before its first recompute: about 2% of the vapour remains in each year file's first record in Terluna's
  runs, whose calls start three steps before a write.
- **Found** in Terluna on 2026-10-27 (`domain/climate` 984606a5; `climate/gcm/README.md`, "The humidity in the year
  files"): the column's vapour from a record matches the average of that record's precipitable-water mean and the
  one before, within 7.6 kg/m² rms, better than its own, 10.4. The code was read here on 2026-11-11 in the copy
  Terluna's runs import (P).
- **Effect.** The model's state is untouched, and the fault lies in what a reader takes from the files. Read as
  means, the records misplace the humidity by half an interval, and two windows in every 120 meet air about half as
  humid. By the rule below, the layers' summed storage after midnight comes within 0.3 mm/day of the precipitable
  water's, against 0.5–1.0 with the records taken as means; Terluna's littoral forcing, corrected on 2026-11-10,
  moved its coldest hours by up to 0.36 K by cell (`research/decisions.md` line 871 at `59dcda1c`).
- **Rule and status.** Terluna's `climate/gcm/year_files.py` takes each interval's mean as the average of a record
  and the next and leaves out each year file's first and last records; `gcm_site`, the CM1 boxes' forcing, has read
  by it since 984606a5. The lab's readers of ExoPlaSim's output need the same rule, stage 3's extraction among
  them. Terluna's runner writes the humidity's true mean as a further field behind a switch (`nhusmean`,
  `domain/climate` b93a046e), the fix to port, and an open pull request upstream (ExoPlaSim #54, on #53) recomputes
  the field at every step in low-I/O mode. The paper counts the fault as the sixth defect in the released codes
  (the author's decision of 2026-11-11). Upstream already holds the report: pull requests #53 and #54, open since
  2026-08-19, state the fault and fix it, and the fix is unmerged, so the released model and `master` keep the
  fault. The lab's issue #71, posted on 2026-11-11, was closed by the maintainer the same day as redundant with
  them; `models/exoplasim/upstream-held-humidity.md` keeps its text.

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
- **In the lab's series** (patch 06 of `models/cm1/series-lab`, 2026-11-11). The gravity is the namelist's `world_g`,
  whose default is the build's `TERLUNA_G`, so that one build without the macro serves every world. `set_constants`
  gives CM1's `g` the entry, from which the dynamics and Morrison's scheme read it as before; RRTMG's two
  initialisations and the CAPE diagnostic take `g` as an argument, where each held a compile-time constant. In the
  suite the constants, the diagnostic, one column of RRTMG and one of Morrison's scheme, handed the Moon's gravity,
  return the bits of the same code with it compiled in, under both of the builds' flag sets
  (`python/climate/tests/test_cm1_world.py`). In single scratch runs of that day, three hours of Terluna's 45° N
  ring from a rainy restart agreed byte for byte, output and restart files alike, between a build with the Moon
  compiled in and one build told the Moon by its namelist, under both flag sets, and CM1's released supercell
  kept its output at the defaults. The MYNN and MYJ schemes keep the build's gravity and stop
  a run whose `world_g` differs from it, and the lab's adapter compiles the gravity in until the one-day segments
  and the timing of plan stage 3 pass (`models/cm1/README.md`, "The world from the namelist").

### B2. WRF-ELEC NSSL: gravity 9.8 and fall-speed laws (R)

- **Defect.** WRF-ELEC's NSSL module sets `gr = 9.8` as a parameter and again as an assignment
  (`module_mp_nssl_2mom_elec.F:942`, `:8431`). Its fitted fall-speed laws hold Earth's gravity.
- **Found** in the electricity plan (a21a615, 2026-10-02). **Fixed** in 6027230 (2026-10-04):
  - `gr` becomes the build's gravity;
  - each fitted law scales by (g/9.81)^((b+1)/3), only where the particle is present (`GRAVITY_TEXT` and
    `GRAVITY_PATCH`, `climate/crm/cm1_elec.py:437-487`).
- **Verified.** `test_cm1_elec.py:116`: the scaling acts only where the particle is present and not at Earth's
  gravity. The Earth supercell agrees with CM1's own NSSL twin (verification record).
- **In the lab's series.** Patch 03 of the electrified series still reads `TERLUNA_G`, so an electrified build
  compiles its gravity in while the lab's patch 06 reads the rest of the model's from the namelist (B1). A companion
  patch that hands NSSL's fall speeds and ventilation the namelist's gravity is still to write. CM1's own copy of
  the NSSL scheme, which the electrified build replaces, keeps `gr = 9.8` (`module_mp_nssl_2mom.F` 935, 6857), and
  the registry refuses it at another gravity since 2026-11-11 (`cm1-earth-g-schemes`).

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
- **In the lab's series** (patch 06, 2026-11-11). CO₂ and O₂ are the namelist's `world_co2` and `world_o2`, mole
  fractions whose defaults are the build's macros, and RRTMG's two drivers take them as arguments. In the suite one
  column of RRTMG, longwave and shortwave, handed the Open Moon's CO₂ and O₂ returns the bits of RRTMG with them
  compiled in, and twice the CO₂ lowers a clear column's outgoing longwave by 4.4 W/m². The gases set to zero stay
  so in every build: an Earth case of CM1 runs without Earth's ozone, methane and nitrous oxide
  (`models/cm1/README.md`, "The world from the namelist").

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
- **In the lab's series** (patches 07 and 08, 2026-11-11). The soil's top layer is the namelist's `soil_dz1`, 0.05 m
  by default, from which the four layers below double, so that a case states the depth its world's day reaches:
  CM1's 1 cm times the square root of the solar day in Earth days, where 5 cm on every world leaves an Earth case
  with layers five times too thick. The Sun's declination is the namelist's `sun_decl`, in degrees north and 0 by
  default, and the zenith cosine takes its spherical form, sin(lat) sin(δ) + cos(lat) cos(δ) cos(hour angle). In the
  suite the lines that lay out the soil and the block that sets the Sun keep their bits at the defaults, the layers
  double from the top layer they are handed, and the Sun follows the formula to 2 parts in 10⁶ and stands on the
  horizon at the lab's sunrise hour angle. The effect of either entry on a run is unmeasured
  (`models/cm1/README.md`, "The world from the namelist").
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
- **Checked near 301 K** (Terluna `domain/climate` 6fb0958). The 295 K fit leaves layers up to 5.9 W/m² off over
  land and 6.8 over the sea at 301.2 K, and 4.2–7.6 W/m² in the worst layers at 302.5 K; a refit on 301 K columns
  holds within 0.3 W/m² there.
- **Remains.** Each fit holds near its own state, level set and convection scheme. On Terluna's settled 301 K design
  years the refit holds within 1.9–2.65 W/m² by layer (8641746); on the Betts–Miller scheme's climate it leaves
  3.38 W/m² (5578b55); carried onto 14 or 15 levels it leaves 6.4–8.8 W/m², so runs on those sets take a refit on
  their own columns (6c78965, 805691b, 00da68d, 3fd43d5).

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
- **Arithmetic (P).** Integrated with g(r) and the shells' area through air at 250 K, whose mass-mean height is
  49 km, a straight column holds 5.5% more air than p_s/g_s, and the air over a square metre of ground 11.6%; at
  270–290 K the second figure is 12.7–13.8%. The paper already gave 11.5% for its 295 K column (claim S10). The
  models' p_s/g_s, 74.9 t/m², measures the pressure; the air the scenario needs, with the vapour and heat it holds
  over the ground, stands about 12% above it.
- **Status.** The radiative side of the shells' widening enters the GCM through the twilight `full` terms (B14). The
  dynamics are unchanged, and the effect is not quantified.

### B22. CM1 RRTMG: reference pressures stop at 1053.63 hPa (S; verified V)

- **Defect.** RRTMG's longwave and shortwave reference pressures begin at 1053.63 hPa (`module_ra_rrtmg_lw.F:3846`,
  `module_ra_rrtmg_sw.F:3026`). A layer at higher pressure gets index `jp` = 1 and a negative interpolation fraction
  `fp`, which extrapolates linearly in ln p (`module_ra_rrtmg_lw.F:3676-3683`, `module_ra_rrtmg_sw.F:2878-2885`).
- **Arithmetic (V).** At the water level the lunar air stands at 1,215.9 hPa. With a scale height near 51 km at
  290–295 K, the lowest ~7 km over the sea lie beyond the table; less over high ground.
- **Measured** offline (Terluna `domain/atmosphere` 6f7d7b0): the table's edge moves the lowest layers' cooling by
  0.002–0.003 K a day, and RRTMG's own optics come within 0.02 K a day of the correlated-k model, so the
  extrapolation is harmless for this air and needs no patch. The excess cooling on the 45° N ring (4.5 W/m² in the
  lowest 1.8 km, 8.5 W/m² at 1.8–6.5 km; 17fa76e) comes from reading CM1's stored tendencies at constant pressure
  (C20).

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

### B28. CM1 Morrison: rain's size limits and breakup (S, V; scaled in the lab's series, off by default)

- **Defect.** Morrison bounds each species' slope parameter (`morrison.F:486-503`, "SIZE LIMITS FOR LAMBDA"). For
  rain, `LAMMINR = 1/2800 µm` caps the mean diameter at 2.8 mm; snow and graupel are capped at 2 mm. Rain's
  self-collection turns to breakup above a mean diameter `D_b` (`morrison.F:2265-2276`), which defaults to 300 µm
  when the namelist's `brkup_db` is zero (`morrison.F:494-498`; `cm1.F:404`). Terluna's runner sets neither
  (V: no `brkup` in `climate/crm/` at 186b294), and the core patches scale fall speeds but leave these bounds.
- **Why it is Earth's.** The largest raindrop that survives its fall scales with the capillary length,
  (σ/(ρ_w g))^½, 2.46 times longer at lunar gravity (`paper/data/regime_calc.json`), and slower drops collide with
  less energy. Earth's caps keep lunar drops small, and small drops evaporate faster.
- **Found** on 2026-10-17 by this repository's main session, reading pristine cm1r22.0.
- **Effect** (Terluna `domain/atmosphere` dd89cef, 8b55847, read in 21529d2). Terluna's patch scales the limits
  from `&param3`, 0 giving stock CM1 bit for bit: breakup from 0.84 mm, a 6.88 mm cap on the mean diameter and a
  5.80 m/s cap on the mean fall speed at lunar gravity. Over the small box's second lunar day, against a spread of
  0.13 K between realizations, the lunar limits nearly doubled the rain at the ground (33 to 63 mm a lunar day), cut
  the share of falling water evaporated from 86% to 48% and the cloud cover from 47% to 36%, and warmed the air at
  2 m by 1.47 K.
- **Fix.** Patch 03 of the lab's `models/cm1/series-lab`, switched by `brkup_gscale` (default 0, CM1's own limits),
  scales the breakup's lengths and the two caps from the build's gravity and from the namelist's density ratio and
  exponent, which `python/atmosphere/rain` computes for a world; patch 04 gives rain the single-drop solver's fall
  law from a table and the world's self-collection rate (`rain_fall_law`, `rain_selfcoll`; defaults 0, CM1's own).
  In the suite, one column of the patched scheme keeps its bits at the defaults, takes the limits the Python
  computes and settles at their breakup balance (`python/climate/tests/test_cm1_rain.py`). The sources compile, and
  in a single scratch run on 11 November 2026 CM1's released supercell case kept its output byte for byte at the
  defaults. Stage 3's CM1 builds will repeat that identity on a lunar case and measure the effect in the lab's
  runs. The scaling is a similarity of the drops' collisions, which no measurement at another gravity tests, and
  the registry warns below 1.62 m/s² (`models/cm1/README.md`, "Rain's limits, fall law and self-collection").

### B29. PlaSim: Kuo-type deep convection (R; open)

- **Defect.** PlaSim's deep convection (`rainmod.f90`, `nprc` 1) is a Kuo scheme: wherever a parcel lifted
  undiluted from the surface is buoyant, it turns the column's moisture supply into rain, the surface's evaporation
  included. ExoPlaSim's namelist only switches the scheme on or off.
- **Found** on 2026-10-21 (Terluna `domain/climate` f07ad8d), when the corrected CM1 box over the Near-side Sea
  rained almost nothing after midnight while the GCM's circulation sank over the site.
- **Effect.** After midnight the sea there evaporates 3.4 mm/day and the scheme rains 2.9 of it, where CM1's box
  rains 0.14–0.17 mm/day. The scheme heats the upper air to within 1.3 K of the undiluted parcel's adiabat, where
  CM1's mixing updrafts hold theirs 3.0–6.3 K below (467a146).
- **Fixes under test in Terluna.** A simplified Betts–Miller scheme (Frierson 2007; `nprc` 2, 2542b57) with a
  cloud-depth test and mixing integrated within layers (91ab10d), and a bulk mass-flux scheme on Tiedtke's model
  with entrainment measured in CM1's clouds (`nprc` 3, 38c2371, 3fd43d5), each behind PlaSim's own switch with Kuo
  kept at 1. Settled, the Betts–Miller scheme runs 1.2–1.7 K warmer than Kuo's 298.4 K at the same sunlight
  (5578b55). In two-year tests each setting of either scheme so far misses CM1's rain by time of day at one site or
  both, and the mass-flux scheme's test parcel crosses PlaSim's stable layer below cloud base on too few columns,
  so convection's share of the rain falls from 86% to 42–45% (3fd43d5, b182515). In single columns on fifteen levels
  the mass-flux scheme goes deep on every step of the sea's night, its tops at 57–58 km where CM1's night cloud stops
  at 7–8 km, and the column loses CM1's night layer under that convection whichever boundary layer it has (6d0c707;
  B32).

### B30. PlaSim: one constant for the evaporation of falling rain (R; replaced in the lab's series, off by default)

- **Defect.** `mkrain` (`rainmod.f90`) evaporates falling rain by one Earth-set constant, `gamma` (0.01): a share of
  each layer's saturation deficit per step, with no drop size or fall speed (Terluna `domain/climate` 05b1384).
- **Effect.** PlaSim evaporates 29% of its falling rain on the Moon, an ordinary share on Earth, where CM1's
  corrected boxes with lunar drops evaporate 61% over the sea and over land. At one constant PlaSim evaporates far
  more over the sea than over land (75.8% against 58.2% at 0.04), so it matches the sea box at 0.027 and the land box
  near 0.046, by extrapolation (2cc5179, 30e7f83). More evaporation moistens the lower air and grows PlaSim's low
  cloud: two years at 0.04 cooled the Moon 1.8 K, still cooling (05b1384).
- **Fix.** Rain evaporated from its drops' sizes and fall speeds. Each column's rain takes its drops' number flux
  down beside its mass flux, Morrison's ventilated evaporation and his self-collection with breakup act through each
  layer, the fall law comes from the single-drop solver in the world's air, and new rain enters by a rule and two
  sizes fitted on cloud-resolving boxes. Terluna's design runs take the scheme (`climate/gcm/rain_drops.py` at
  `39c5ee04`, commits 8e805f60 and f5f767fa): offline on the mean air of its three CM1 boxes, its share rule gave
  0.96–1.05 of CM1's column evaporation with CM1's own melted size, where every new drop at one size gave 1.15–1.31
  and rain joining whatever falls 0.64–0.80, and in PlaSim over one lunar day it evaporated 45% of the rain formed
  against `gamma`'s 20%. Patch 14 of the lab's `models/exoplasim/patches/series` adds the scheme to `rainmod.f90`
  behind `NEVAPPREC` 2, PlaSim's own 1 staying the default. The lab's patch reads the fall law from a table in the
  run's folder, the one CM1's patch 04 reads, takes the world's self-collection rate and density exponent from the
  namelist with Earth's as defaults, and stops a run whose birth sizes are unstated, where Terluna's patch states the
  Moon's table, rate, exponent and births as its constants and defaults.
  `python/climate/gcm/rain_drops.py` computes the entries and the table for a world.
- **Evidence for the port.** On Earth's control over 96 steps the patch at its default gives the output and the
  restart of the build before it byte for byte; `mkrain` from the patched source gives the Python copy's numbers
  to 10⁻¹⁰ at the Moon's gravity and Earth's; and from the Open Moon's air the copy gives the numbers of Terluna's
  module (`models/exoplasim/README.md`). No lab run has measured the scheme's effect on a climate.
- **Status.** Replaced in the lab's series and off by default until the Earth control's test (`PLAN.md`). The
  births are Terluna's calibration for the Open Moon on fifteen levels, from boxes that ran Earth's warm-rain rates
  (B38) and Earth-sized ice; another world or level set takes its own. The snow's sublimation keeps `gamma`.
  Terluna's runner also sets the constant itself (`--rain-evaporation`, recorded only when given).

### B31. PlaSim: Earth's σ levels near the ground (R; a set generated for the world in the lab, the released ten by default)

- **Defect.** PlaSim's ten σ levels are fractions of the surface pressure chosen for Earth's air. At the design
  air's 51 km scale height they stand near 0.9, 4.0, 9.9, 18.2, 29, 42, 59, 79, 108 and 166 km, the lowest layer
  spanning the ground to 1.73 km and one layer 6.4–13.7 km (Terluna `domain/climate` 697ac36).
- **Effect.** The lowest layer averages away the 1.4–2.3 kJ/kg of moist static energy that CM1's afternoon and
  evening updraughts draw from the surface layer, and CM1's 6 km night boundary layer over the sea, with its clouds' 7–8 km
  tops, falls inside one layer (03e7c41, 697ac36).
- **Fix in Terluna.** Sets of 14 levels (new levels near 2.4, 6, 8 and 13.5 km) and 15 levels (the lowest near
  0.3 km), placed by hand at the 51 km scale height, at about 1.5 times the ten-level run's cost, with a
  mass-conserving remap for restarts (697ac36, a75fd47). Terluna's design runs take the fifteen. The longwave
  correction takes a refit on each set's own columns (B18).
- **Fix in the lab.** A level set generated for each world, with no patch, since PlaSim reads its half levels from
  the namelist under `NEQSIG` −1. A study states a table in place of the run's count of levels: the scale height
  its heights are counted at, the count of the released model's highest half levels kept, and the heights of the
  half levels below them. `python/climate/gcm/levels.py`, from Terluna's module at `39c5ee04`, generates the set,
  and the lab's writer states it in `SIGH` with PlaSim's friction on its top two levels in `TFRC`. From Terluna's
  values for the Open Moon the rule returns its fifteen levels at the four places Terluna states them; in two of
  them the last bit is the compiled model's, where Terluna's module computes the released formula with numpy's
  powers. A restart goes onto another set by the conservative remap, and the writer reads a calibration by layer
  on the half levels it states. Registry B31 warns where a run's lowest full level stands above a proposed 350 m
  at the scenario's scale height, and `exoplasim-longwave-fit` asks for a refit where the correction leaves its
  envelope.
- **Evidence for the port.** With the released count the writer's files are unchanged. On Earth's control over
  96 steps the released ten stated as a generated set give the output and the restart of PlaSim's own formula byte
  for byte; on Earth's surface under the Moon's gravity the fifteen-level build runs two days from a cold start and
  from a ten-level restart carried onto the set; and the remap keeps each column's integrals of vorticity,
  divergence, temperature and vapour (`models/exoplasim/README.md`, "Level sets"). No lab run has measured a set's
  effect on a climate.
- **Status.** The released ten are the lab's default, and a study opts in with its world's heights. In Earth's air
  the ten already put the lowest level at 142 m, so the Earth control keeps them (`PLAN.md`); the Earth control's
  test of a generated set is ahead. Each set takes its own longwave correction, ledger terms and rain births.

### B32. PlaSim: Earth's mixing lengths and wind floor in the vertical diffusion (R; the lengths open)

- **Defect.** PlaSim's vertical diffusion converts its coefficient from heights to σ with g³, as the physics
  requires, but its mixing lengths, 160 m for momentum and 438 m for heat and vapour, and its 1 m/s wind floor are
  Earth's (Terluna `domain/climate` 21d98fc).
- **Effect.** Near the ground PlaSim carries heat at about CM1's rate. Higher up, over the Near-side Sea after
  midnight, CM1's mixed layer reaches 6.5 km against the GCM's 4.3 km; at every hour CM1 keeps its vapour nearly
  uniform to 6.2 km where the GCM's falls 2.7–4.7 g/kg, and it carries 28–112 W/m² of vapour up through 5.2 km,
  80–92% by resolved motion, where PlaSim's median diffusivity is 0.1–0.3 m²/s at Richardson numbers of 3–8. Stretched by the gravity
  ratio, to 966 m and 2.65 km, the lengths raise PlaSim's diffusivity over the sea 1.5–3 times at 0.6–1.8 km and 5–9
  times at 5.2 km; CM1's set-up assumes the same scaling for its own length, a scaling untested by any experiment
  here.
- **Tested in single columns** (Terluna `domain/climate` 6d0c707). A nonlocal boundary layer, Holtslag and
  Boville's K-profile as CAM3 implements it with YSU's explicit entrainment, run on fifteen levels under the CM1
  boxes' forcing, brings the land's afternoon mixed layer down from PlaSim's 6.86 km to 3.54 km, toward CM1's
  2.75 km, closing 81% of the depth's gap and 55% of the vapour drop's. Over the sea at night, with the stretched length, it leaves the mixed layer 4.41 km deep against
  PlaSim's own 4.87 km and CM1's 6.48 km and closes 35% of the vapour drop's gap, short of the half that a stop rule
  set beforehand required, so no GCM run followed. In those columns the mass-flux convection goes deep on every night
  step and holds an inversion near 3.1 km; started from CM1's own midnight air, every boundary layer keeps CM1's deep
  night layer through the quarter, so the column loses that layer in the evening under deep convection, whichever
  boundary layer it has. CM1's cloud-topped night layer carries 10–12 W/m² of heat down through 6–7 km, mostly by its
  subgrid mixing, which Terluna reads as entrainment driven from the cloud's top, a term PlaSim's schemes lack.
- **The wind floor.** `zumin`, 1 m/s, floors the wind of `surflx`'s bulk formulas as well as the wind shear in
  `vdiff`. In the surface transfer, patch 12 of the lab's `models/exoplasim/patches/series` puts Beljaars's gust in
  its place with CM1's least wind of 0.1 m/s when a run sets `NGUST = 1` (default 0, PlaSim's floor), as Terluna's
  design runs have it; in the vertical diffusion the floor stays (B33; `notes/exoplasim.md`, "The gust and the
  similarity over water").

### B33. PlaSim: Earth's free-convection constant over water (R; replaced in the lab's series, off by default)

- **Defect.** `surflx` computes the transfer of heat and vapour over water with Miller, Beljaars and Palmer's
  (1992) free-convection constant, 0.0016 m s⁻¹ K⁻¹ᐟ³, the still-air limit of a tank law, 0.17 (g κ²/(θ_v ν))^⅓, that goes
  as (g/p_s)^⅓ once the diffusivities are written through the density (Terluna `domain/climate` b182515).
- **Effect.** The Moon's gravity and the design air's 1,215.9 hPa give 0.00083. Two years at that value lower the
  Near-side Sea's evaporation from 3.82 to 3.62 mm/day, a quarter of its excess over CM1's 2.98, dry the lowest
  0.6 km by 0.34 g/kg toward CM1's air, lower global evaporation and rain by 3% and move the imbalance at the top of
  the air 0.4 W/m² toward balance.
- **Evidence for the scaling, in Terluna (R).** A bounded study of 2026-11-10 examined whether the still-air laws
  carry to lunar gravity (`research/decisions.md` line 862 at `59dcda1c`; its report and sources on the research
  drive, `session-tools/agents/lunar_free_convection/`). Where the Rayleigh number or gravity itself was varied,
  the transfer followed the law: effective exponents of 0.28–0.333 in water (Funfschilling and others 2005), 0.27
  rising to a third and beyond in a centrifuge at 5–60 g (Jiang and others 2020), a heated plate at 0.05 g on
  parabolic flights matching the standard correlation in laminar flow (Lotto and others 2017), and large-eddy
  simulations at Mars's gravity reproducing measured boundary-layer depths (Spiga and others 2010). The study read
  Jiang and Spiga in full and the others at their abstracts, and it found no experiment on a turbulent horizontal or
  water surface at reduced gravity. Its bracket puts the lunar transfer by gravity alone at 0.41–0.61 of the Earth
  law against the cube root's 0.55, the low end from the gust law under a boundary layer no deeper than Earth's, in
  which gravity and the layer's depth enter as a product, and the high end from the lowest exponent. The bracket
  bears on the gust of B35 as well.
- **Fix.** Beljaars's gust with the similarity over ice-free water, which drop the term: over water as over land
  the transfer takes the wind √(|U|² + w*²), w* = (g/θ_v h B)^⅓ from the model's gravity, its boundary layer's depth
  and its buoyancy flux, and ice-free water then takes CM1's surface-layer similarity at the lowest level's height.
  Terluna's design runs take both (`climate/gcm/surface_gust.py`, `surface_similarity.py` at `39c5ee04`): in its
  four-year test the gust lowered the Near-side Sea site's transfer coefficient for vapour to 0.67 of the baseline's,
  against 0.78 at the lunar constant. Patches 12 and 13 of the lab's `models/exoplasim/patches/series` add both to
  `fluxmod.f90`, switched by `NGUST` and `NSIMW` (each 0 by default, PlaSim's own term), and derive the air's
  viscosity in each column, where Terluna's patch sets that of Earth's sea-level air.
- **Status.** At the series' defaults PlaSim keeps the Earth constant, and the lab's default keeps it until the Earth
  control's test decides whether the gust serves every world (`PLAN.md`). Each patch at its default gives the build
  before it byte for byte over two days of Earth's control, and the switches change that output
  (`lab/tests/test_builds.py`). Terluna's namelist variable for the constant (`fluxmod`'s `cfree`,
  `--free-convection lunar`) has no patch here.

### B34. PlaSim: shallow convection's tops at 700 hPa (R; open here)

- **Defect.** PlaSim's shallow convection caps its clouds' tops at 700 hPa, an Earth height in pressure, near
  28 km in the Moon's air (Terluna `domain/climate` 1d05c3d, ea1b62f).
- **Effect.** In Terluna's two-year tests of the Betts–Miller scheme's depth test the cap binds in 1–1.4% of cells
  (1d05c3d).
- **Status.** Terluna's `--sbm-shallow-cap`, off by default, ties the cap to the depth test's threshold above each
  column's condensation level (ea1b62f).

### B35. CM1 r22.0: the MM5 surface layer's gust over water (R)

- **Earth value.** CM1's MM5 surface layer (`sfclay.F`, `sfcmodel = 2`) adds a convective gust to the wind in its
  bulk formulas: over land Beljaars's form, vconvc (g/T_s h B)^⅓, from the build's gravity, and over water the old
  MM5 formula √Δθv m/s for Δθv in K, with no gravity in it. The comment on the branch reads "Use Beljaars over land,
  old MM5 (Wyngaard) formula over water".
- **Found** in Terluna's sea boxes and recorded on 2026-10-28 (`domain/climate` 238638f; `research/decisions.md`
  lines 560–561 at `bdda5a07`).
- **Effect.** Over the lunar sea, with the air 3–4 K below the sea in virtual temperature, the formula gave a gust
  of 1.6–2.1 m/s and raised the wind in the bulk formulas 1.6–1.8 times; Beljaars's form from the box's own fluxes
  raises it 1.1–1.2 times. Every CM1 run over the seas behind the paper's first released draft took the formula. At
  Earth's gravity the formula serves as fitted.
- **Fix.** Beljaars's form over water too, at the build's gravity: Terluna's build variants with `GUST_PATCH`, and
  patch 02 of the lab's `models/cm1/series-lab`, switched by `gust_over_water` (default 0, CM1's own formula). Its
  sources compile, and stage 3's CM1 builds will measure its effect in the lab's runs and on the Earth control.

### B36. PlaSim: Earth's damping times in the horizontal diffusion (P; open)

- **Earth value.** PlaSim's horizontal diffusion damps divergence, vorticity, temperature and humidity at the
  truncation wavenumber over 0.2, 1.1, 5.6 and 0.1 days at T21 (`plasimmod.f90`, `tdissd`, `tdissz`, `tdisst`,
  `tdissq`), on wavenumbers above 15 (`nhdiff`) with `ndel` 2. ExoPlaSim counts those days as 24 hours
  (`plasim.f90`, `day_24hr/(TWOPI*tdissd)` and alike), so the Moon's long model day leaves them as they are. The
  times suit Earth's T21, whose smallest wave spans 1,906 km.
- **On the Moon.** The same wavenumber spans 520 km, so a given wind crosses it 3.7 times faster while the damping
  keeps its time. The design run sets none of the four, and its log prints 5.6 days for temperature
  (`A28R_301k_design_l15_snow_s938_turned_refit_precession`, `MOST_DIAG`). Terluna's records hold no mention of the
  diffusion.
- **Evidence (P).** Zonal spectra of that run's last five years of output between 25° S and 25° N, from its
  71.5-hour means, fall smoothly to the truncation in the wind, the temperature and the surface pressure, while the
  vertical motion at σ 0.77 is flat from wavenumber 3 to 18. The Earth control's spectra, once the lab has them, are
  the comparison this reading lacks.
- **Status.** Open. Besides that comparison, one run with the four times multiplied by the radius ratio, 0.27, would
  size the effect.

### B37. PlaSim and the CM1 set-up: a slab sea 50 m deep (P; Terluna's column R; open)

- **Earth value.** The GCM's sea is a slab 50 m deep without heat transport (`MLDEPTH`, the default of
  `oceanmod.f90` and of ExoPlaSim's `configure`), a depth of Earth's seasonal mixed layer. `exoplasim.md` lists it
  among the placeholders, and Terluna's records hold no run at another depth.
- **On the Moon.** The sea's forcing turns with the 29.5-day lunar day. In the turned run at the target
  (`A28R_301k_design_l15_snow_s924_turned_refit`, years 30–49, the Near-side Sea site's six cells, binned by the
  Sun's hour angle), the slab's surface swings 0.63 K, from 304.19 K before dawn to 304.82 K in the afternoon, as a
  net heating near 100 W/m² through the day gives for 50 m, while its evaporation falls from 4.2 mm/day by day to 2.4
  at midnight with the wind (P).
- **Estimate (P).** Under a wind of 2 m/s and 200 W/m² of heating the sea's Monin–Obukhov depth is one to two
  metres, so a fortnight of sunlight would stay within the 10–20 m that visible light reaches, and the swing would be
  2.5 to 5 times the slab's, 2.1 K for 15 m. No ocean model ran, and the estimate leaves out the sea's own
  convection at night.
- **Terluna's column (R).** Terluna's lake model, run offline at five sites of the corrected design climate, puts
  the surface of calm water at 37.1 °C in its hottest hundredth of hours at the 8° sea cell, where the GCM's slab
  shows 30.9 °C, and its seas' oxygen study implies a day's mixed layer of 3–6 m (`research/decisions.md` lines 860
  and 863 at `59dcda1c`; `domain/ecology` 910f09c8, 85746366). The column meets the GCM's light winds and returns
  nothing to the air, so it marks the calm end, and it puts the swing well above this entry's estimate.
- **CM1.** The sea boxes hold the site's mean, 304.57 K (`oceanmodel = 1`; `sea_surface_k` in `case.json`), leaving
  out the slab's ±0.3 K, about ±6% of the evaporation by the humidity difference between sea and air.
- **Status.** Open. The sea's rain by time of day, the largest difference between the GCM and CM1, depends on the
  swing. One GCM run at 15 m would size it, and a box that follows the GCM's sea temperature by local time, as it
  follows the wind, would carry the swing into CM1.

### B38. CM1 Morrison: cloud turned into rain at Earth's rates (V; sized P; a switch in the lab's series, unmeasured)

- **Earth value.** Morrison's scheme forms rain from cloud by Khairoutdinov and Kogan's (2000) fits, the
  autoconversion `1350 q_c^2.47 (N_c ρ)^−1.79` and the accretion `67 (q_c q_r)^1.15` (`morrison.F` 2106–2107 and
  2241 in r22.0), fitted to drop spectra computed at Earth's gravity. The gravity patch and the lunar rain
  patches leave both as they are, a limit `cm1.md` has recorded since 2026-10-17 ("Fall speeds").
- **Scaling (P).** Cloud droplets fall in the Stokes regime, so the speed at which one overtakes another, and the
  collision kernel with it, goes as g: 0.166 at lunar gravity, before any loss of collision efficiency. Rain sweeps
  up cloud at its fall speed, which goes as g^0.6: 0.34. A lunar cloud is six times deeper at the same updraught
  speed, so the air spends six times as long in it, and at Earth's rates the scheme forms rain about six times too
  readily by autoconversion, and three times by accretion, in each passage.
- **Effect.** Unmeasured. Low cloud's water and its drizzle depend most on the autoconversion, and the GCM's fits
  drawn from CM1's boxes, the new rain's size of 0.439 mm and the evaporated share among them, inherit both rates.
  The boxes take 100 droplets per cm³ (`ndcnst`), a number without a lunar basis, and the autoconversion goes as
  its −1.79 power.
- **Fix.** Patch 05 of the lab's `models/cm1/series-lab`, the lab's own, reads two factors from `&param3`,
  `rain_autoconv_fac` and `rain_accr_fac`, each 1 by default. Each multiplies CM1's rate once CM1 has computed it,
  above freezing and below, and the number tendencies follow by CM1's own statements;
  `python/atmosphere/rain/warm_rain.py` gives g/9.81 and (g/9.81)^0.6 for a world, 0.166 and 0.340 on the Moon. In
  the suite one column of the patched scheme keeps its bits at the defaults and scales each rate by its factor,
  against hand arithmetic (`python/climate/tests/test_cm1_rain.py`). In a single scratch run on 11 November 2026,
  under CM1's flags, CM1's released supercell case kept its output byte for byte at the defaults and read the two
  entries from its namelist (`models/cm1/README.md`, "Factors on autoconversion and accretion").
- **Status.** A switch in the lab's series, off by default; its effect is unmeasured. A sea box of two lunar days
  with the factors at 0.166 and 0.340 would size it (`PLAN.md`, block 4, step 2). The scaling omits the collision
  efficiency's own dependence on the closing speed and the collisions that turbulence drives.

### B39. PlaSim, Terluna's simplified Betts–Miller scheme: a relaxation time of 2 h (P; open)

- **Earth value.** The scheme relaxes temperature and vapour toward its references over `tau_bm`, 7,200 s, the value
  Frierson (2007) took for Earth, in the design case and the 68 runs that share its closure (`rainmod.f90`, `mksbm`;
  the design run's `rainmod_namelist`). The closures Terluna tried relaxed over 18 h (three runs) or 12 h (five),
  each with reference profiles of its own.
- **Scaling.** By the similarity under which CM1's lengths and times follow the scale height
  (`lab/design/world_spec.md`, rule 9), 2 h becomes 12 h on the Moon, within the 11–27 h over which CM1's boxes
  remove lunar instability (`lab/design/gap_series.md`).
- **Effect.** Unmeasured for the time alone, since the closures changed their reference profiles with it.
- **Status.** Open. One GCM run of the design scheme at 43,200 s would size it; `lab/design/terluna_fixes.md`, row 12, holds the scheme
  for assessment before its port.

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

### C19. CM1 set-up: nudging from 8 km, and a forcing table that stops at 16 km (R)

- **Defect.** The rings and boxes held their air to the GCM's from 8 km, fully from 16 km (`nudge` in each case
  kind, `climate/crm/cm1_run.py:1100, 1112, 1116` at 186b294), and a box's day–night table reached 16 km (`top_m`,
  `:1285, 1334, 1354`), its layers interpolated in height. Lunar convection reaches 55–80 km, so the hold
  covers most of the convecting column.
- **Found** on 2026-10-21 by the water and heat budgets of Terluna's box over the Near-side Sea, set against the
  GCM's own budget at the site (`domain/climate` 13e7123).
- **Effect.** Over that box's second lunar day the nudging supplied 89 of the 107 W/m² its radiation removed,
  standing in for the deep convection that forms the GCM's rain at 18–72 km, and the box rained 0.06 mm/day against
  the GCM's 2.72. The table's stop left out the 35.5 W/m² the GCM's circulation takes from the air above 16 km, and
  its interpolation dried the column by 0.55 mm/day. How far the hold restrained the rings' convection is unmeasured.
- **Fix.** For Terluna's site boxes, `climate/crm/gcm_site.py` takes the GCM's own budget at the site, lays each GCM
  layer's tendency on CM1's levels with its total kept, applies it through the whole column, holds temperature and
  vapour to the GCM's only above the top of the GCM's convection, from its next level up at 93 km, and nudges the
  mean wind toward the GCM's by local time (2cc5179, 5a44e5e, 13e7123). The rings keep the earlier forcing until they are rerun.

### C20. CM1 analyses: radiative tendencies read at constant pressure (R)

- **Defect.** Under `eqtset = 2`, CM1 stores its radiative heating at constant volume (`lwten = hr*cp/cvm`, `swten`
  alike, cp/cvm 1.38–1.39 in the lunar air) and hands RRTMG the ground's temperature for the air at the ground.
  Terluna's readers (`ring_radiation.py`, `rrtmg_edge.py` and `ring_heat_budget.py` in `climate/crm`) took the
  stored tendencies as rates at constant pressure and extrapolated the air at the ground from the two lowest layers.
- **Found** on 2026-10-20, when RRTMG run offline on the ring's columns failed to reproduce CM1's written cooling
  (Terluna `domain/atmosphere` fe49ad9).
- **Effect.** Radiation overstated by 38–40%: the extra cooling of 4.5, 8.5 and 10.2 W/m² against the correlated-k
  model on the 45° N ring (the paper's claim V08, and B22's former attribution) and a heat budget of the ring that
  counted radiation 40% too large. Read correctly, CM1's longwave comes within 0.013 K a day of the correlated-k
  model in every layer (0.2–1.3 W/m²), and the GCM's longwave over-cooling is worth about 2.7 K of the 3.7 K gap near
  the ground at 45° N, where the paper's first released draft gives 1.5 K.
- **Fix.** One module of conventions, `climate/crm/cm1_output.py`: a stored tendency times cvm/cp against another
  radiation code, times cv/cp in a budget beside CM1's other θ tendencies (fe49ad9).

### C22. GCM and CM1 set-up: sunlight at the barycentre's distance (P; open)

C21, the night's twilight counted twice, is recorded on the paper's branch and joins this log at the next
integration.

- **Defect.** Terluna's set-up gives the GCM the orbit of the "Earth-Moon barycentre about the Sun: 1 AU,
  Earth-orbit eccentricity" (`climate/gcm/boundary.py` 197 on `domain/climate`), and CM1's cases take the GCM's
  sunlight (`var17`). The Moon's own orbit, which carries it 379,700 km sunward of the barycentre at new Moon and as
  far beyond it at full Moon, is left out.
- **Arithmetic (P).** The sunlight swings ±0.51% through the month, ±5.9 W/m² of the design case's 1,159 W/m², in
  step with the lunar day: the near side's noon falls at full Moon and the far side's at new Moon, so the far side's
  noon receives 1.0% more sunlight than the near side's in every lunar day.
- **Effect.** Unmeasured: a steady contrast of a hundredth in sunlight between the two faces.
- **Status.** A cosine of the subsolar longitude on the solar constant adds the swing to each model.
  Earthshine and Earth's infrared at full Earth, about 0.07 W/m² each, stay out.
- **Classed as an idealisation (2026-11-11).** Terluna's set-up states the choice, so the omission is a known
  simplification of the scenario: by the author's decision the paper states it with the scenario, outside its count
  of defects, and the lab offers the swing as an option that a study switches on or off (`PLAN.md`, "Decisions").

## (d) Record inconsistencies found in this pass, not yet corrected in Terluna (V)

- **Upstream report claim.** `climate/gcm/exoplasim_run.py:251` says the `solang` bug was "Reported upstream". The
  claim holds (ExoPlaSim issue #69, opened by the author on 2026-09-29, open and unanswered on 2026-10-17), but
  Terluna's record does not cite the issue. The history pass missed it; the literature pass found it.
- **Stale forcing description.** `climate/crm/README.md:37-39` gives CM1's sunlight as the 5% dimmer shield's
  1,173.5 W/m² from `A28_dim5`. The runner's default forcing run is `A28_dim5_moon` (`cm1_run.py:1085`), and the
  corrected rings use 1,198 W/m² from `A28_corrected_970`.
- **Build flags.** `climate/crm/README.md:76-78` (every OpenMP build at `-O3`) does not match the `moon_omp`
  executable (C8).

## Items listed by the main session and checked afterwards

`paper/notes/ideation.md` also lists Earth-fitted drop size limits among the fits used outside their range. The
history pass did not check them; the main session did, and they are entry B28.
