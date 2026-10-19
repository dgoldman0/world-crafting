# Specifications: draft schema 0

Draft 4 of 2026-10-18. The seed files in [../worlds/](../worlds/) follow schema 0, and uncommitted scratch
scripts computed their derived quantities on 2026-10-17 and 18, with Terluna's formulas and constants and the
lab's own derivations: the spin term, the scale-height, capillary and soil factors. The code that stage 1 of
plan.md writes to read the seeds takes those derivations over.

## Four levels

| Level | Holds | Example | Where |
|---|---|---|---|
| World | The body: its size and mass, rotation, orbit, star, host planet and surface geometry. Its `kind` is `found` for an observed body and `illustrative` for a supposed one | `moon` | `lab/worlds/<world>/world.toml` |
| Scenario | The state of the world's air, water and land, the sunlight's filter and scale, and outside forcings, as observed, made or supposed. Its `kind` is `found`, `crafted` or `illustrative` | `moon/open-moon` | `lab/worlds/<world>/scenarios/<name>.toml` |
| Model defaults | One model's settings for any world: upstream pin, patches and switches, grid, physics, output, guards and the calibration stages it reads. CM1's also define named variants and give lengths, times and rates at a reference state | `cm1/defaults` | `lab/configs/<model>/defaults.toml` |
| Study | One scenario's whole chain: its GCM runs and the CM1 cases forced from them, each extending its model's defaults | `open-moon` | `lab/studies/<study>.toml` |

World and scenario kinds combine freely. The Open Moon and its 1.0 atm extension (`moon/open-moon-1.0atm`)
are crafted scenarios of a found world, and an exoplanet study pairs a found world with an illustrative
scenario.

## Rules

1. **Units.** Each key's suffix names its unit, as Terluna names them (`radius_m`, `gm_m3_s2`, `co2_ppm`,
   `sidereal_period_days`, `timestep_min`, `taper_km`), and the adapters convert to each model's own units.
   `_days` counts days of 86,400 s; `_solar_days` counts the world's solar days; `model_` names the model's
   own calendar, as in `model_years` and `whole_model_days`.
2. **Stated or derived.** Each derived quantity has one derivation.
   - A specification may state such a quantity together with its basis. The lab then compares the stated
     value with the derivation, within the derivation's tolerance, and records both.
   - The Moon's seed states its solar day as the synodic month, 29.53059 d, the value CM1's `var19` takes in
     Terluna's runner, against 29.5305882 d from 1/(1/P_rot − 1/P_year).
   - Earth's seed states the standard gravity of 9.80665 m/s², PlaSim's own Earth value. The derivation, GM/R²
     less the spin term, gives the area mean of 9.7977 m/s², 0.09% lower.
   - **Tolerances.** A stated gravity lies within 0.2% of its derivation, and a stated solar day within one
     part in 10⁵; a breach refuses the world.
3. **Sources.** Every value of a found world or scenario names its source, and every crafted or illustrative
   value its basis. A model choice in a scenario of any kind, such as a slab ocean and its depth, names its
   basis.
4. **External data by pin.** External data are named by pinned identifiers, such as `tsis1-hsrs-stride100`
   or `terluna:protection/spectra/shield_transmission.json#titania_stack`. A plain name, such as the TSIS-1
   spectrum's, names data from outside Terluna that the manifest resolves to its source; a `terluna:` pin
   names a file in Terluna's repository and a `terluna-drive:` pin one on its research drive. `#` selects an
   entry in the file, and `@` appends the first 16 hex digits of the file's sha256.
   - **The lab's own stages** resolve a pin through the lab's manifest, which holds each one's hash, source,
     licence and credit and points to the lab's own copy.
   - **Comparison tests** read Terluna's records in place, under the Terluna roots, and skip without them.
5. **`"unchosen"` and `"model-default"`.** The lab refuses any stage that reads a field marked
   `"unchosen"`. A field marked `"model-default"` takes the model's own value, which the adapter records.
6. **Extended items.** `extends` names the parent, `[set]` lists the changed fields by dotted path, and
   `variants` names variants that the model's defaults define.
   - **The delta.** Every changed input enters through `[set]` or `variants`; descriptive fields such as
     `title` and `purpose` may be restated outside them.
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
   - **Molar masses.** ExoPlaSim computes the gas constant from its own molar masses: CO2 at 44.01 g/mol,
     against the 44.0095 g/mol of the lab's derivations.
   - **CM1's Earth gravity** is 9.81 m/s².
   - **Planned settings.** A setting whose planned patch the build lacks resolves to what the build does:
     `capillary` to `breakup-only`, the scaled `brkup_db` under Morrison's own 2.8 mm cap; `from-season` to
     the equinox; the day's soil depth to patch 08's 5 cm top layer; and `from-spectrum` to patch 10's
     weights. The registry tests the resolved settings, so their entries warn wherever their conditions hold
     until the patches land. On the Moon the soil and equinox entries stay silent, since patch 08's 5 cm lies
     within 10% of the day's 5.4 cm and the obliquity is 1.54°.
8. **Studies extending studies.** A study may extend another: it inherits that study's runs and cases, adds
   its own and redefines none. An inherited item keeps its settings and their hash, and its product key
   differs from the parent study's where the scenario or an upstream key differs. A study extending
   `open-moon` runs the same chain on a changed scenario, as `lab new study` writes it (architecture.md,
   "A session with the lab").
9. **Scaling with the scale height.** Where a model's grid follows the scale height, as CM1's does, its
   defaults give their lengths, times and rates at a stated reference state, the gravity, temperature and
   air at which they were tested, from which the lab derives the reference scale height and speed as it
   does a scenario's.
   - **Scaled:** lengths follow H = RT/(Mg) at the scenario's reference temperature, so the adapter
     multiplies them by H/H_ref; times follow H/c, with c = (RT/M)^½ setting the speeds; rates such as the
     Rayleigh damping follow c/H. With the reference's air and temperature, all three reduce to the ratio
     of gravities.
   - **Other physical scales:** raindrop limits follow the capillary length, (9.81/g)^½ from Morrison's Earth
     values, and soil layers the depth the day's heat reaches, (solar day/1 d)^½ from CM1's own.
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
| `body.gm_m3_s2` | m³ s⁻² | GM; surface gravity is GM/R² less the spin term, the area mean, unless `body.gravity_m_s2` is stated with its basis |
| `rotation.sidereal_period_days` | d | Rotation against the stars |
| `rotation.obliquity_deg` | ° | The equator's tilt to the orbit |
| `rotation.solar_day_days` | d | Optional, stated with its basis; otherwise 1/(1/P_rot − 1/P_year) |
| `orbit.star`, `semi_major_axis_au`, `sidereal_year_days`, `eccentricity` | –, AU, d, – | The orbit about the star |
| `orbit.from_host` | – | For a moon, the host planet whose orbit it follows, in place of the four fields above |
| `star.id`, `star.spectrum`, `star.spectrum_form`, `star.constant_w_m2`, `star.temperature_k` | –, pinned name or `blackbody`, –, W m⁻², K | The spectrum: a pinned measured or model spectrum, its tails the star's blackbody, or the blackbody alone; `irradiance` for a pinned irradiance at 1 AU, kept as measured with its tails holding the rest of the constant, or `shape` for one scaled whole to the constant; the total at 1 AU; and the effective temperature that sets the blackbody |
| `host.id`, `host.neglected` | – | A moon's planet, and the forcings from it left out, with their size |
| `host.semi_major_axis_m`, `host.eccentricity`, `host.inclination_to_equator_deg` | m, –, ° | The moon's orbit about its host, and its tilt to the moon's equator, over which a host's permanent tide is averaged |
| `surface.geometry` | pinned name | Heights over the geoid from a pinned source, `model-default` or `unchosen`: a height image and a gravity field, each with its PDS3 label |
| `surface.geoid_degree` | – | The gravity field's last degree in the geoid, stated with its basis |
| `surface.tide.from`, `surface.tide.love_k2`, `surface.tide.sub_longitude_deg` | –, –, ° | The permanent tide of a body fixed in the sky, for a field whose degree-2 terms leave it out: `host`, the k2 that scales it by 1 + k2, and the east longitude of the mean sub-host point, on the equator |

## Scenario fields

| Field | Unit | Meaning |
|---|---|---|
| `kind` | – | `found`, `crafted` or `illustrative` |
| `air.reference_level` | – | The level at which the stated pressure holds: `water`, `sea` or `mean-radius` |
| `air.surface_pressure_pa` | Pa | Total pressure at that level |
| `air.o2_partial_pressure_pa` or `o2_mole_fraction`, `co2_ppm`, `ar_per_n2` or `ar_mole_fraction`, `balance` | Pa or –, ppm of the total, –, gas | The air: O2 by partial pressure or mole fraction, CO2 in ppm of the total, Ar by its ratio to N2 or its mole fraction, and N2 the balance; the lab derives the mole fractions, and from them the partial pressures |
| `air.reference_temperature_k` | K | The surface temperature the scenario is stated at, observed for a found scenario and designed or supposed otherwise, with its basis, or `settled`, the GCM's settled global mean, which the fixpoint finds: the design column, the ledger and the gas fits are computed at it, and the scale height and horizon factor take it as their reference |
| `air.cloud_droplets_per_cm3` | cm⁻³ | The cloud droplets the air's aerosol supports, which CM1's two-moment schemes take |
| `air.ozone`, `air.water_vapour` | – | `none`, `model-default` or a pinned profile; `prognostic` |
| `water.seas_share`, `water.seas`, `water.lakes` | –, pinned names | The standing water: the seas `from-heights`, the world's heights flooded to the share, and the lakes `from-runoff`, a GCM run's runoff routed over the heights; either may be pinned instead. `water.lakes_start` pins the first link of the runoff chain, and a study's GCM run names `lakes_from`, an earlier run whose runoff fills its lakes; a run derived from another keeps its parent's lakes unless its delta sets `lakes_from` |
| `water.ocean` | – | `kind` (`slab`), `mixed_layer_m`, `sea_ice` |
| `land.albedo` | – | One value marked as a placeholder until a surface map exists |
| `sunlight.filter`, `sunlight.scale` | pinned name, – | A transmission spectrum or `none`; a multiplier the same at every wavelength, stated or `to-reference-temperature`, which the target stage finds from the GCM's global-mean surface temperature |
| `forcing.top_infrared_w_m2` | W m⁻² | Infrared from space at the top of the air, by day and by night (patch 06), stated or `from-glow`, computed from a pinned design of lit structures in space |

## The first derived quantities

| Quantity | Derivation | The Moon (Open Moon design) | Used by |
|---|---|---|---|
| Surface gravity | GM/R² − (2/3)Ω²R, the area mean with the spin term | 1.6242107 m/s², against Terluna's GM/R² of 1.6242188765608128 m/s² | ExoPlaSim `gravity`; CM1's gravity, compiled in as `TERLUNA_G` until the namelist patches (architecture.md, "Model adapters"); the surface geopotential; every hydrostatic height in the GCM-to-CRM extraction |
| Rotation rate | 2π/P_rot | 2.6616995 × 10⁻⁶ s⁻¹ | CM1's Coriolis parameter (`cm1_run.py:2038-2040`) |
| Solar day | 1/(1/P_rot − 1/P_year), or stated | 29.53059 d stated; 29.5305882 d derived | CM1 `var19` (`cm1_run.py:2016`; 2,551,443.0 s). PlaSim's synodic clock derives its own from the rotation and the year (patch 04), 0.2 s a lunar day shorter than CM1's |
| Partial pressures | x_i·p, from the mole fractions | N2 0.99128639, O2 0.21227, Ar 0.01185725, CO2 0.00048636 bar | ExoPlaSim `configure` |
| Mole fractions | CO2 as ppm of the total; O2 as p_O2/p or as given; the rest N2 and Ar, split by Ar/N2 or with Ar as given | CO2 4.0 × 10⁻⁴, O2 0.17457850 | CM1's CO2 and O2, compiled in as `TERLUNA_CO2` and `TERLUNA_O2` (written as 0.174579) until the namelist patches |
| Mass fractions | x_i M_i / Σ x_j M_j, from the mole fractions | CO2 6.1057 × 10⁻⁴, O2 0.19375 | PlaSim `ZGASW` (patch 08) |
| Molar mass and gas constant | Σ x_i M_i; 8314.46/M | 28.8319 g/mol; 288.38 J kg⁻¹ K⁻¹ | ExoPlaSim `GASCON`, computed inside ExoPlaSim |
| ExoPlaSim's rotation period | 1 for a stated one-day solar day, otherwise P_rot (rule 7) | 27.321661 d | `rotationperiod` |
| ExoPlaSim's days per year | The year in whole days when `rotationperiod` is 1 (`exoplasim/__init__.py:2609-2610`); otherwise N = 12 · max(1, ⌊360/(12 P_rot) + 0.5⌋) (`:2618-2619`) | 12 | `N_DAYS_PER_YEAR` |
| PlaSim's model day | P_rot · N/(N − 1) (`plasim.f90:1292-1300`); exactly one day when `rotationperiod` is 1 (`:1287`) | 29.8054 d | PlaSim's `solar_day`, which registry entry B11 tests |
| Steps per model day | PlaSim first rounds the steps of a 24-hour day to an even count and divides the day by them, then counts nint(model day) ÷ nint(that step) as an integer division (`plasim.f90:1343-1348`) | 1,430 at 30 min | `NSTPW` 143 for the 3-day means, 10 a model day; `N_RUN_STEPS` 17,160 for 12 whole days; 120 means a year |
| The stepped model day | The steps per model day times PlaSim's step | 1,430 × 1,800 s, 29.7917 d | The calendar the outputs follow, the paper's `model_day_days` |
| Sunlight at the top | ∫ S_λ T_λ dλ × (1 AU/a)² × the scale, on the union of the spectrum's points and the filter's: S_λ the star's spectrum, holding its stated constant, and T_λ the filter's transmission, held at its end values beyond its range | 1,236.12 W/m² through the shield. TSIS-1 stands as measured, 1,326.23 W/m², and its tails hold the rest: 0.16 W/m² below 202 nm, where the Sun has about 0.1, and 34.61 W/m² past 2,730 nm. Terluna's 1,235.25 passed all 34.77 W/m² at the shield's 0.904 at 2,730 nm, and the lab's tails pass at the shield's own transmission along them, 0.070% more. Of the total, 6.21 W/m² passes beyond the shield file's 5 µm end at its held 0.934, where the file's model leaves out silica's absorption | ExoPlaSim `flux` (`GSOL0`) and its spectrum files; CM1 `var17` |
| Scale height, H/R, column mass, horizon factor | RT/(Mg), H/R, p/g and √(πR/2H), at `air.reference_temperature_k` | At 295 K: 52.4 km, 0.03015, 74,861 kg/m², 7.2 (`paper/data/worlds.json`) | The reach report; deciding whether a column needs a ledger of its own |
| Ring length and columns | 2πR cos(latitude); the column count a multiple of the ranks | At 45° N: 7,719 km, 1,288 columns of 5,993 m | CM1 `nx`, `dx`, `var16` (`cm1_run.py:2051-2056`) |
| CM1 lengths, times and rates | Lengths × H/H_ref, times × (H/c)/(H/c)_ref, rates × (c/H)/(c/H)_ref (rule 9) | A factor of 1 at the reference state, and 1 + 5.05 × 10⁻⁶ on the Moon with the spin term: 6 km columns, a 150 km top, nudging from 8 to 16 km, a 40 s step | CM1's grid, top, nudging heights, `dtl`, `l_inf` and `rdalpha` (`cm1_run.py:1979-2035`) |
| CM1's raindrop limits | Morrison's 0.3 mm breakup and 2.8 mm cap on rain's mean diameter × (9.81/g)^½ | × 2.4576: 0.737 mm and 6.88 mm | `brkup_db`; the cap through a planned patch (registry B28) |
| CM1's soil layers | CM1's 1 cm top layer × (solar day/1 d)^½, the four below doubling | × 5.4342: a 5.4 cm top layer, 5.4 to 86.9 cm | `slab_dzs`, through a planned patch after core 17 (registry `cm1-soil-day`) |
| CM1's Sun | Declination asin(sin ε · sin L_s), from the obliquity ε and the case's solar longitude L_s | 0 at the equinox the study's cases take | A planned patch after core 17 (registry `cm1-equinox-sun`); the case's sunrise, −acos(−tan φ tan δ) |
| Ice-optics weights | The shares of Ebert and Curry's four near-infrared bands within PlaSim's band 2, from the spectrum at the top of the air, the filter included | 0.6295, 0.2276, 0.0752 and 0.0677 through the shield, the fourth 0.0581 were the shield opaque past 5 µm. From the unfiltered TSIS-1, 0.6202, 0.2297, 0.0816 and 0.0685; patch 10's 0.6164, 0.2283, 0.0811 and 0.0742 came from a tail 11% brighter than the rest of the constant, with the whole spectrum scaled to it | The planned ExoPlaSim patch 11; patch 10's constants until it passes, when registry entry `exoplasim-ice-weights` warns |
| ExoPlaSim's output steps | `mean_interval_days`: below a model day, the divisor of the steps per model day whose mean lies nearest it; from a model day up, the divisor of the year's model days nearest it, the shorter at a tie, so that whole means fill each year | 10 means of 143 steps, 2.98 d; on Earth, 3 days give daily means | `NSTPW` |
| ExoPlaSim's time-step limit | The advective limit set by the radius a, the truncation N and the run's largest wind u: u·Δt·N/a below 1 | Checked in stage 1 against the largest winds of Terluna's runs, which ran stable at 30 minutes | The guard on `timestep_min` |

The registry's tests (`q`) name these quantities in snake case with their units: `gravity_m_s2`,
`exoplasim_rotationperiod_days`, `model_day_days`, `scale_height_over_radius`, `chapman_horizon`,
`lowest_level_pressure_hpa`, the air's pressure at the lowest point of the surface, and `soil_layer_ratio`,
a case's top soil layer against 1 cm × (solar day/1 d)^½.

## Settled in code

`lab/worldlab/derive.py` computes the table's quantities, and its `planet()` gathers them into the planet
record under the registry's names, each stated value beside its derivation. The sunlight at the top and the
ice-optics weights come from `lab/worldlab/sunlight.py`, and the pressure at the surface's lowest point comes
with stage 2's geography producer, from the world's heights and seas. Each derivation takes its plainest form,
and the calendar follows the rounding of ExoPlaSim's configure and `plasim.f90`, which the model applies. The
derivations agree with `paper/data/regime_calc.json` to one part in 10¹² and with `worlds.json` to its stated
digits, and with Terluna's records within each comparison's stated tolerance.
`lab/worldlab/spec.py` codes these rules:

- **Ids.** A world takes its folder's name, a scenario `<world>/<name>`, a model's defaults `<model>/defaults`
  and a study its file's name. Inside a study, `extends` names model defaults where it holds a `/` and a
  sibling in the same table otherwise.
- **References.** `forced_by` and `initial.from` name another GCM run, and `site.ring` and
  `day_night.from_case` another CM1 case of kind `ring`. A run's start lies within its source's
  `model_years`, a case's `reference_model_years` within its forcing run's, and no chain of starts closes
  on itself.
- **Order.** A derived item takes its parent, then its own fields, then its added variants, then its
  `[set]`.
- **Variants** add to the parent's and apply in the order the model's defaults define them, which is the
  order in which `models/cm1/builds.json` applies their series. An item's series are rebuilt from the defaults' and its
  variants', so that they never depend on the chain that reached them. `requires` checks; two variants that
  set one path differently are an error, as is a variant that changes a value its parent's chain set.
- **Changes.** Only an item that extends model defaults adds fields of its own; any other changes through
  `[set]` and variants, and restates a field only with its parent's value, compared as the hash sees it.
  Descriptive fields (`title`, `purpose`) are restated freely and never inherited. A
  `[set]` path names an existing field and leaves structural ones alone (`schema`, `id`, `extends`, `set`,
  `variants`, `model`, `world`, `kind`, `patches`). A table that replaces a table keeps all its keys, which
  refuses the unquoted dotted keys TOML reads as nested tables.
- **Studies** may extend a study, taking its runs and cases; a parent's item is never redefined, only
  derived from.
- **The hash** is the sha256 of the resolved settings as JSON with sorted keys, no spaces and floats as
  Python writes them, its descriptive fields left out. It covers an item's own settings; stage 4's product
  keys add the scenario and the upstream keys.
- **Unchosen fields** are listed by path, for the stages that read them to refuse.

`lab/worldlab/sunlight.py` gives the sunlight at the top and the ice-optics weights, reading the star's
spectrum and the scenario's filter through the manifest:

- **The star's spectrum** is a pinned file of wavelengths in nm and irradiance in W m⁻² nm⁻¹ below one header
  row, or `blackbody`, the blackbody at `star.temperature_k` from where hc/(λkT) = 50 to 1 mm. A pinned
  spectrum takes that blackbody past each end where it leaves room, at the level of its own light within 2%
  of the end's wavelength. As an `irradiance` its values stand and its tails hold the rest of
  `star.constant_w_m2`; a spectrum holding more than the constant is refused. As a `shape` the spectrum and its
  tails are scaled together to the constant. The one spectrum gives the total and the band weights alike.
- **The filter** is `none` or a pinned JSON file of `wavelength_nm` and a `transmission` table, whose entry
  the pin names with `#`. Its transmissions lie between 0 and 1, read linearly between its points and held
  at its end values beyond them, and the filtered light is integrated on the union of the spectrum's points
  and the filter's.
- **The record** gives the star's total at the orbit's semi-major axis; for a pinned spectrum, the light it
  measures and the light each tail holds; what the filter passes, and the part of that beyond the filter's
  own range; the filter's share; and the filtered light times the scale where the scale is a number. It ends
  with the ice-optics weights of the filtered light and of the unfiltered star, each band's edges set into the
  grid.

`lab/worldlab/data.py` codes rule 4, and `lab/data/manifest.toml` holds its records:

- **Pins.** A pin reads `[root:]path[#entry][@digest]`, its root `terluna` or `terluna-drive` and its digest 16
  lowercase hex digits. A plain name takes lowercase letters, digits, `.`, `_` and `-`; a root's path is
  relative, without empty, `.` or `..` parts. A world's `star.spectrum` and `surface.geometry`, and a
  scenario's `sunlight.filter` and `water.lakes_start`, hold a pin or one of `none`, `model-default` and
  `unchosen`; these fields alone name Terluna's files in the seeds.
- **The manifest** keys each entry by its pin without `#` or `@`. An entry holds a title, a use, the licence
  its review found, a credit, the review's date and its files; each file its name, size, sha256 and one
  source, a URL or a Terluna pin, with the date the lab took its bytes. A pin with a digest names one file of
  its entry.
- **The store** keeps each file at `data/<digest>/<name>`, read-only. A fetch copies from Terluna's roots and
  downloads only when asked, writing through a temporary file and keeping only bytes of the recorded size
  and hash; each read checks both again.
- **Comparisons** read Terluna's records in place, under the Terluna roots, and skip without them; their
  files enter neither the manifest nor the store.

`lab/worldlab/geography.py` gives a world's heights above its geoid, reading the files of `surface.geometry`
through the manifest with the readers of `python/geography/topography.py` (`notes/geography.md`):

- **The files.** Among the pin's files, each PDS3 label names the file it describes: one a global
  simple-cylindrical height image, whose samples times its scaling factor, in its unit, are radii less its
  reference sphere, of radius OFFSET, and one a SHADR gravity table. The sphere's radius lies within 1% of
  `body.radius_m`, and the field's GM within one part in 10⁶ of `body.gm_m3_s2`.
- **The geoid** takes the field to `surface.geoid_degree` and the centrifugal potential of the sidereal
  rotation, synthesised on the heights' own grid. Where the world states `surface.tide`, it adds the host's
  permanent tide, (1 + k2) GM r²/a³ [A₀ P₂(sin φ) + A₂₂ cos²φ cos 2(λ − λ₀)] over the field's GM/r², with the
  host's GM from its own world: A₀ and A₂₂ are the time means of (a/d)³ P₂(sin β) and ¾ (a/d)³ cos²β cos 2λ' for the
  host at distance d and direction (β, λ') in the world's frame, over the mean anomaly and the perigee's angle from
  the node, and a circular orbit in the equator gives −½ and ¾, the host held over the sub-point. A host stays
  fixed in the sky only for a rotation synchronous with its orbit, so the world's rotation lies within 1% of the
  orbit's two-body period, which the Sun's pull lengthens by 0.14% on the Moon.
- **The record** gives the files read, the label's target, frame and product, the degree, the rotation rate,
  the field's GM and reference radius, and the tide's terms.

Still to settle, each with the stage whose code first reads it, where stage 1 left them on 2026-10-18: the field
tables of the defaults, studies, runs and cases, with optional fields and their defaults, as stage 2's and 3's
adapters read them; the `water` and `sea` reference levels, with the pressure at the surface's lowest point, in
stage 2; and whether sources stay as comments, with stage 4's product headers.

## The Moon worked through

Where Terluna holds each value of the seed files today (commit 186b294), and where the value enters the
models:

| Specification value | In Terluna | Enters |
|---|---|---|
| `body.radius_m`, `body.gm_m3_s2` | `shared/constants.json`, through `boundary.planet()` (`boundary.py:162-172`) into `climate/gcm/products/moon_gcm_configuration.json` | ExoPlaSim's radius and gravity (`exoplasim_run.py:814, 840`); CM1's build gravity (`cm1_run.py:969-971`), ring lengths (`:2051-2056`) and box columns (`:1828`); about 15 analysis scripts through `cm1_run.planet()` |
| `rotation.sidereal_period_days`, `obliquity_deg` | The same chain | ExoPlaSim's `rotationperiod` and `obliquity` (`exoplasim_run.py:841-842`); CM1's Coriolis parameter (`cm1_run.py:2040`) |
| `rotation.solar_day_days` | The same chain, as `solar_day_days` | CM1's `var19` (`cm1_run.py:2065-2066`); the CRM analyses through `solar_day_s()` |
| `orbit.from_host`, which takes Earth's year (365.25636 d) and eccentricity (0.0167) | Typed into `exoplasim_run.py:841-842` as 365.25636 d and 0.016715, the second a typed value beside the 0.0167 of Earth's file | ExoPlaSim's `year` and `eccentricity`, with `fixedorbit` |
| `star.spectrum`, `constant_w_m2` | The `atmosphere/radiative_convective` inputs (TSIS-1); 1361 typed into `exoplasim_run.py:983` | `sun_<shield>.dat` and `_hr.dat`, copied into the model folder as `sun.dat` and `sun_hr.dat`, and the total flux (`exoplasim_run.py:954-996, 1028-1029`) |
| `air.*` | `EXPERIMENTS['A28']` with `O2_PA`, `AR_PER_N2` and `CO2_PPM` (`exoplasim_run.py:78-92`) | ExoPlaSim's gases; CM1's build macros, read back from the GCM run's `progress.json` (`cm1_run.py:860-869`) |
| `water.*` | `EXPERIMENTS['A28']`; `boundary.py`, from the geography products, which the seed derives from the heights and the runoff | The T21 land mask and topography (`exoplasim_run.py:934-951`); CM1's surfaces along rings and in boxes, through `boundary.lakes_product` (`cm1_run.py:1607-1632, 1767-1821`) |
| `land.albedo` | `MODEL['land_albedo']` (`exoplasim_run.py:98`) | ExoPlaSim's `soilalbedo`; CM1's placeholder land row holds a separate value (`cm1_run.py:1088`) |
| `sunlight.filter`, `scale` | `EXPERIMENTS['A28']['shield']`; `--set sunlight_scale=0.970` in the session script, where the seed's scale follows its reference temperature | The spectrum files and `GSOL0`; CM1's `var17`, from the GCM run's recorded flux (`cm1_run.py:869, 2013`) |

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
- Stellar spectra in formats beyond the comma-separated wavelength and irradiance the lab reads, such as
  model-atmosphere grids, and systems of more than one star.
- Surface geometry beyond a height image over a gravity field: heights measured from an equipotential already,
  as MOLA's MEGDR topography is, aquaplanets, idealized continents and designed height fields.
- Vertical grids chosen for the world, where today PlaSim's σ levels are Earth's and the ledger's GCM terms
  are computed on them.
- Scenarios that change in time, such as a shield dimming over years.
