# Specifications: draft schema 0

Draft 3 of 2026-10-17. The seed files in [../worlds/](../worlds/) follow schema 0, and an uncommitted scratch
script computed their derived quantities on 2026-10-17 with Terluna's own formulas and constants. The code
that stage 1 of plan.md writes to read the seeds takes those derivations over.

## Four levels

| Level | Holds | Example | Where |
|---|---|---|---|
| World | The body: its size and mass, rotation, orbit, star, host planet and surface geometry. Its `kind` is `found` for an observed body and `illustrative` for a supposed one | `moon` | `lab/worlds/<world>/world.toml` |
| Scenario | The state of the world's air, water and land, the sunlight's filter and scale, and outside forcings, as observed, made or supposed. Its `kind` is `found`, `crafted` or `illustrative` | `moon/open-moon` | `lab/worlds/<world>/scenarios/<name>.toml` |
| Model defaults | One model's settings for any world: upstream pin, patches and switches, grid, physics, output and the calibration stages it reads. CM1's also define named variants and give lengths and the time step at a reference gravity | `cm1/defaults` | `lab/configs/<model>/defaults.toml` |
| Study | One scenario's whole chain: its GCM runs and the CM1 cases forced from them, each extending its model's defaults, with the study's compatibility settings | `open-moon` | `lab/studies/<study>.toml` |

World and scenario kinds combine freely. The Open Moon and its 1.0 atm extension (`moon/open-moon-1.0atm`)
are crafted scenarios of a found world, and an exoplanet study pairs a found world with an illustrative
scenario.

## Rules

1. **Units.** Each key's suffix names its unit, as Terluna names them (`radius_m`, `gm_m3_s2`, `co2_ppm`,
   `sidereal_period_days`, `timestep_min`, `taper_km`), and the adapters convert to each model's own units.
   `_days` counts days of 86,400 s; `_solar_days` counts the world's solar days; `model_` names the model's
   own calendar, as in `model_years` and `means_per_model_day`.
2. **Stated or derived.** Each derived quantity has one derivation.
   - A specification may state such a quantity together with its basis. The lab then compares the stated
     value with the derivation, within the derivation's tolerance, and records both.
   - The Moon's seed states its solar day as the synodic month, 29.53059 d, the value CM1's `var19` takes in
     Terluna's runner, against 29.5305882 d from 1/(1/P_rot − 1/P_year).
   - Earth's seed states the standard gravity of 9.80665 m/s². GM/R² comes to 9.8203 m/s², 0.14% higher
     through rotation and shape, which sets the tolerance a stated gravity needs.
3. **Sources.** Every value of a found world or scenario names its source, and every crafted or illustrative
   value its basis. A model choice in a scenario of any kind, such as a slab ocean and its depth, names its
   basis.
4. **External data by pin.** External data are named by pinned identifiers, such as `tsis1-hsrs-stride100`
   or `terluna:protection/shield_transmission#titania_stack`. A `terluna:` pin names a file in Terluna's
   repository and a `terluna-drive:` pin one on its research drive; `#` selects an entry in the file, and
   `@` appends the first 16 hex digits of the file's sha256.
   - **The lab's own stages** resolve a pin through the lab's manifest, which holds each one's hash, source,
     licence and credit and points to the lab's own copy.
   - **A study's compatibility settings** name Terluna's files by pin and hash, and the reproduction tests
     open them in place and check the hash.
5. **`"unchosen"` and `"model-default"`.** The lab refuses any stage that reads a field marked
   `"unchosen"`. A field marked `"model-default"` takes the model's own value, which the adapter records.
6. **Extended items.** `extends` names the parent, `[set]` lists the changed fields by dotted path, and
   `variants` names variants that the model's defaults define.
   - **The delta.** Every changed input enters through `[set]` or `variants`; descriptive fields such as
     `purpose` and `recorded_key` may be restated outside them.
   - **Replacement.** A set value replaces the parent's whole, an inline table included.
   - **Record.** The resolved form is hashed, and the delta, its set fields and variants together, is
     recorded with it.
7. **Model conventions belong to the adapters.** Examples:
   - **The radius.** ExoPlaSim reads it in units of 6,371,220 m (`shared/constants.json`, `model_closures`).
     Terluna's runner divided by 6,371,000 m, which lengthens PlaSim's radius by 60 m
     (`notes/exoplasim.md`).
   - **The solar day.** ExoPlaSim keeps a 24-hour solar day only when `rotationperiod` is exactly 1. For a
     world whose stated solar day is exactly one day, as Earth's is, the adapter passes 1; PlaSim's model day
     is then exactly one day (`plasim.f90:1287`), and the year holds its whole days, 365 for Earth
     (`exoplasim/__init__.py:2609-2610`). For any other world it passes the sidereal period.
   - **CM1's namelist.** Its writer rounds the boundary-layer length to 0.1 m and the damping rate to
     10⁻⁸ s⁻¹, as Terluna's does (`cm1_run.py:2004-2005`).
   - **Molar masses.** ExoPlaSim computes the gas constant from its own molar masses: CO2 at 44.01 g/mol,
     against 44.0095 in Terluna's runner.
   - **CM1's Earth gravity** is 9.81 m/s².
8. **Compatibility settings.** For byte-for-byte reproduction of a Terluna run's inputs and its builds'
   sources, which the lab's tests check, the study holds each of Terluna's quirks as a named compatibility
   setting:
   - the radius divisor;
   - the eccentricity Terluna typed;
   - the calibration values copied by hand and rounded;
   - the CM1 run length typed as 59.06 days;
   - the build labels that Terluna's Makefile patch writes into a comment;
   - the point in each CM1 patch series before the namelist patches, where gravity and the air are
     compiled in;
   - the restart files Terluna's runs started from, and the products they read, named by their recorded
     hashes.

   The products carry Terluna's other states with them, such as the reference tools' Ar/N2 of 0.0093/0.7808
   and a design column at the sunlight scale of 0.95 and 294.9 K. The lab uses them as recorded in place of
   its own stages, and stage 5 reproduces each separately.
   - **Builds.** The lab compiles at its defaults' flags. A run that Terluna made on a stale build, such as
     the -O2 control of the 45° N twilight pair (defect log C8), is therefore reproduced in its inputs alone.
   - **Correction.** Correcting a quirk afterwards is a declared delta with a new key, and Terluna's record of
     the earlier run remains valid.
   - **Inheritance.** Compatibility settings and recorded keys stay with the study that holds them. A study
     extending it inherits its runs and cases, which then use the lab's own stages and earn keys of their
     own.
9. **Scaling with gravity.** Where a model's grid follows the scale height, as CM1's does, its defaults
   give their lengths and time step at a stated reference gravity, the one at which they were tested.
   - **Scaled:** the adapter multiplies those values by g_ref/g, and rates such as the Rayleigh damping by
     g/g_ref.
   - **Unscaled:** times tied to the day are given in the world's solar days, and the rest in seconds, the
     same on every world.
   - **ExoPlaSim:** its spectral grid spans the globe, so its defaults hold no scaled lengths.
   - **Studies:** a study, which belongs to one scenario, states its own values as they apply there,
     unscaled.

## World fields

| Field | Unit | Meaning |
|---|---|---|
| `kind` | – | `found` or `illustrative` |
| `body.radius_m` | m | Mean radius |
| `body.gm_m3_s2` | m³ s⁻² | GM; surface gravity is GM/R² unless `body.gravity_m_s2` is stated with its basis |
| `rotation.sidereal_period_days` | d | Rotation against the stars |
| `rotation.obliquity_deg` | ° | The equator's tilt to the orbit |
| `rotation.solar_day_days` | d | Optional, stated with its basis; otherwise 1/(1/P_rot − 1/P_year) |
| `orbit.star`, `semi_major_axis_au`, `sidereal_year_days`, `eccentricity` | –, AU, d, – | The orbit about the star |
| `orbit.from_host` | – | For a moon, the host planet whose orbit it follows, in place of the four fields above |
| `star.id`, `star.spectrum`, `star.constant_w_m2` | –, pinned name, W m⁻² | The spectrum, and its total at 1 AU |
| `host.id`, `host.neglected` | – | A moon's planet, and the forcings from it left out, with their size |
| `surface.geometry` | pinned name | Heights over the geoid from a pinned source, `model-default` or `unchosen` |

## Scenario fields

| Field | Unit | Meaning |
|---|---|---|
| `kind` | – | `found`, `crafted` or `illustrative` |
| `air.reference_level` | – | The level at which the stated pressure holds: `water`, `sea` or `mean-radius` |
| `air.surface_pressure_pa` | Pa | Total pressure at that level |
| `air.o2_partial_pressure_pa`, `co2_ppm`, `ar_per_n2`, `balance` | Pa, ppm of the total, –, gas | The air, built as Terluna builds it (`exoplasim_run.py:820-821, 843-844`) |
| `air.reference_temperature_k` | K | The surface temperature the scenario is stated at, observed for a found scenario and designed or supposed otherwise, with its basis: the design column, the ledger and the gas fits are computed at it, and the scale height and horizon factor take it as their reference |
| `air.ozone`, `air.water_vapour` | – | `none`, `model-default` or a pinned profile; `prognostic` |
| `water.seas_share`, `water.seas`, `water.lakes` | –, pinned names | The standing water and its geometry |
| `water.ocean` | – | `kind` (`slab`), `mixed_layer_m`, `sea_ice` |
| `land.albedo` | – | One value marked as a placeholder until a surface map exists |
| `sunlight.filter`, `sunlight.scale` | pinned name, – | A transmission spectrum or `none`, and a multiplier the same at every wavelength |
| `forcing.top_infrared_w_m2` | W m⁻² | Infrared from space at the top of the air, by day and by night (patch 06) |

## The first derived quantities

| Quantity | Derivation | The Moon (Open Moon design) | Used by |
|---|---|---|---|
| Surface gravity | GM/R² | 1.6242188765608128 m/s² | ExoPlaSim `gravity`; CM1's gravity, compiled in as `TERLUNA_G` until the namelist patches (architecture.md, "Model adapters"); the surface geopotential; every hydrostatic height in the GCM-to-CRM extraction |
| Rotation rate | 2π/P_rot | 2.6616995 × 10⁻⁶ s⁻¹ | CM1's Coriolis parameter (`cm1_run.py:2038-2040`) |
| Solar day | 1/(1/P_rot − 1/P_year), or stated | 29.53059 d stated; 29.5305882 d derived | CM1 `var19` (`cm1_run.py:2016`; 2,551,443.0 s). PlaSim's synodic clock derives its own from the rotation and the year (patch 04), 0.2 s a lunar day shorter than CM1's |
| Partial pressures | p_CO2 = x·p; p_N2 + p_Ar = p − p_O2 − p_CO2, split by Ar/N2 | N2 0.99128639, O2 0.21227, Ar 0.01185725, CO2 0.00048636 bar | ExoPlaSim `configure` |
| Mole fractions | p_i/p | CO2 4.0 × 10⁻⁴, O2 0.17457850 | CM1's CO2 and O2, compiled in as `TERLUNA_CO2` and `TERLUNA_O2` (written as 0.174579) until the namelist patches |
| Mass fractions | x_i M_i / Σ x_j M_j | CO2 6.1057 × 10⁻⁴, O2 0.19375 | PlaSim `ZGASW` (patch 08) |
| Molar mass and gas constant | Σ x_i M_i; 8314.46/M | 28.8319 g/mol; 288.38 J kg⁻¹ K⁻¹ | ExoPlaSim `GASCON`, computed inside ExoPlaSim |
| ExoPlaSim's rotation period | 1 for a stated one-day solar day, otherwise P_rot (rule 7) | 27.321661 d | `rotationperiod` |
| ExoPlaSim's days per year | The year in whole days when `rotationperiod` is 1 (`exoplasim/__init__.py:2609-2610`); otherwise N = 12 · max(1, ⌊360/(12 P_rot) + 0.5⌋) (`:2618-2619`) | 12 | `N_DAYS_PER_YEAR` |
| PlaSim's model day | P_rot · N/(N − 1) (`plasim.f90:1292-1300`); exactly one day when `rotationperiod` is 1 (`:1287`) | 29.8054 d | The calendar every output follows |
| Steps per model day | nint(model day) ÷ nint(time step), as an integer division (`plasim.f90:1348`) | 1,430 at 30 min | `NSTPW` 143 for 10 means a day; `N_RUN_STEPS` 17,160 for 12 whole days; 120 means a year |
| Sunlight at the top | ∫ S_λ T_λ dλ over the measured spectrum, plus the rest of the total at the longest measured wavelength's transmission (`exoplasim_run.py:976-984`); times (1 AU/a)² and the scale | 1,235.25 W/m² through the shield; 1,198.19 W/m² at 0.970 | ExoPlaSim `flux` (`GSOL0`); CM1 `var17` |
| Scale height, H/R, column mass, horizon factor | RT/(Mg), H/R, p/g and √(πR/2H), at `air.reference_temperature_k` | At the paper's 295 K: 52.4 km, 0.03015, 74,861 kg/m², 7.2 (`paper/data/worlds.json`); the seed's 294.9 K changes none of these digits | The reach report; deciding whether a column needs a ledger of its own |
| Ring length and columns | 2πR cos(latitude); the column count a multiple of the ranks | At 45° N: 7,719 km, 1,288 columns of 5,993 m | CM1 `nx`, `dx`, `var16` (`cm1_run.py:2051-2056`) |
| CM1 lengths and time step | The defaults' values × g_ref/g (rule 9) | A factor of 1, with the reference at lunar gravity: 6 km columns, a 150 km top, nudging from 8 to 16 km, a 40 s step | CM1's grid, top, nudging heights and `dtl` (`cm1_run.py:1979-2035`) |

The registry's tests (`q`) name these quantities in snake case with their units: `gravity_m_s2`,
`exoplasim_rotationperiod_days`, `model_day_days`, `scale_height_over_radius`, `chapman_horizon`, and
`lowest_level_pressure_hpa`, the air's pressure at the lowest point of the surface.

## The Moon worked through

Where Terluna holds each value of the seed files today (commit 186b294), and where the value enters the
models:

| Specification value | In Terluna | Enters |
|---|---|---|
| `body.radius_m`, `body.gm_m3_s2` | `shared/constants.json`, through `boundary.planet()` (`boundary.py:162-172`) into `climate/gcm/products/moon_gcm_configuration.json` | ExoPlaSim's radius and gravity (`exoplasim_run.py:814, 840`); CM1's build gravity (`cm1_run.py:969-971`), ring lengths (`:2051-2056`) and box columns (`:1828`); about 15 analysis scripts through `cm1_run.planet()` |
| `rotation.sidereal_period_days`, `obliquity_deg` | The same chain | ExoPlaSim's `rotationperiod` and `obliquity` (`exoplasim_run.py:841-842`); CM1's Coriolis parameter (`cm1_run.py:2040`) |
| `rotation.solar_day_days` | The same chain, as `solar_day_days` | CM1's `var19` (`cm1_run.py:2065-2066`); the CRM analyses through `solar_day_s()` |
| `orbit.from_host`, which takes Earth's year (365.25636 d) and eccentricity (0.0167) | Typed into `exoplasim_run.py:841-842` as 365.25636 d and 0.016715, the second now a compatibility setting of the study | ExoPlaSim's `year` and `eccentricity`, with `fixedorbit` |
| `star.spectrum`, `constant_w_m2` | The `atmosphere/radiative_convective` inputs (TSIS-1); 1361 typed into `exoplasim_run.py:983` | `sun_<shield>.dat` and `_hr.dat`, copied into the model folder as `sun.dat` and `sun_hr.dat`, and the total flux (`exoplasim_run.py:954-996, 1028-1029`) |
| `air.*` | `EXPERIMENTS['A28']` with `O2_PA`, `AR_PER_N2` and `CO2_PPM` (`exoplasim_run.py:78-92`) | ExoPlaSim's gases; CM1's build macros, read back from the GCM run's `progress.json` (`cm1_run.py:860-869`) |
| `water.*` | `EXPERIMENTS['A28']`; `boundary.py`, from the geography products | The T21 land mask and topography (`exoplasim_run.py:934-951`); CM1's surfaces along rings and in boxes, through `boundary.lakes_product` (`cm1_run.py:1607-1632, 1767-1821`) |
| `land.albedo` | `MODEL['land_albedo']` (`exoplasim_run.py:98`) | ExoPlaSim's `soilalbedo`; CM1's placeholder land row holds a separate value (`cm1_run.py:1088`) |
| `sunlight.filter`, `scale` | `EXPERIMENTS['A28']['shield']`; `--set sunlight_scale=0.970` in the session script | The spectrum files and `GSOL0`; CM1's `var17`, from the GCM run's recorded flux (`cm1_run.py:869, 2013`) |

**Two sources on the CM1 side.** CM1 reads the world from `moon_gcm_configuration.json` and again from the
GCM run's `progress.json`.

- A build records the air of the GCM run it was compiled against.
- A case may run against another GCM run whose CO2 and O2 match the build's, and then uses that run's
  sunlight (`cm1_run.py:2445-2449`).

The lab replaces both sources with one specification, which the case's namelist reads, and the build too
while builds compile the air in.

## Fields still to add

- Rotation locked to the star: ExoPlaSim's synchronous mode and substellar longitude, and CM1 with a fixed
  Sun.
- Stellar spectra besides the Sun's, as a blackbody or a pinned model spectrum, and systems of more than one
  star.
- Surface geometry beyond Terluna's atlas: aquaplanets, idealized continents, other bodies' heights.
- Vertical grids chosen for the world, where today PlaSim's σ levels are Earth's and the ledger's GCM terms
  are computed on them.
- Scenarios that change in time, such as a shield dimming over years.
