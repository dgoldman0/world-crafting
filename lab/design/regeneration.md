# Regeneration by parameter

When a parameter of the ExoPlaSim and CM1 work changes, the products downstream of it must be produced again,
each by a Terluna command at a stated cost, as traced by hand on 2026-10-17 from Terluna's code (f03b839) and
the surveys in [inventory.md](inventory.md). In Terluna each of those steps is started by hand or from a
session script, with the inventory's hand-copied values entered again every time. The lab's planner, which
takes the steps over, is tested against the same dependencies in stage 4 of plan.md, beginning with the four
worked examples.

## The graph

```mermaid
flowchart LR
  W[world: R, GM, rotation, orbit, star] --> PL[planet record and derived quantities]
  S[scenario: air, water, shield, scale, land, forcing] --> PL
  CG[GCM settings: defaults and study] --> PL
  W --> GEO[surface geometry: heights, seas, lakes]
  S --> GEO
  GEO -- lowest point --> PL
  GEO -- water fraction --> LED
  GEO --> SRF[T21 mask and geopotential]
  PL --> SRF
  CG --> SRF
  W --> SUN[spectrum files and flux]
  S --> SUN
  S --> COL[design column: middle atmosphere and reference column]
  PL --> COL
  SUN --> COL
  COL --> LED[curved-air ledger]
  CG --> LED
  S -- ground albedo --> LED
  COL --> GAS[gas-band fits]
  SUN --> GAS
  LED --> SWF[shortwave fits]
  GAS --> SWF
  CG --> SWF
  CG --> LWF
  PL --> LWF
  S --> LWF
  CG --> H2O[water-continuum fit]
  PL --> H2O
  S --> H2O
  SWF -. multipliers .-> LED
  CG --> EXB[ExoPlaSim build]
  EXB --> GCM[GCM experiment]
  PL --> GCM
  S --> GCM
  CG --> GCM
  SRF --> GCM
  SUN --> GCM
  LED --> GCM
  GAS --> GCM
  SWF --> GCM
  LWF[longwave correction] --> GCM
  H2O --> GCM
  GCM -. columns .-> SWF
  GCM -. columns .-> H2O
  GCM -. heating diagnostics .-> LWF
  GCM -. surface temperature, where the scale follows it .-> SUN
  S -- glow design --> IRS[infrared from space]
  IRS --> GCM
  GCM -. efficacy .-> IRS
  GCM -. runoff .-> GEO
  CC -- variants --> CMB[CM1 builds]
  PL -- while compiled in --> CMB
  S -- while compiled in --> CMB
  GCM --> EXT[extraction: profiles, vertical wind, sideways forcing]
  GCM --> BOX[ring and box surfaces]
  GEO --> BOX
  LED --> TWT[CM1 twilight table]
  EXT --> CASE[CM1 case inputs]
  BOX --> CASE
  TWT --> CASE
  CMB --> CASE
  PL --> CASE
  CC[CRM settings: defaults, variants and study] --> CASE
  CC --> PL
  CASE --> CRM[CM1 run]
  CRM -. day-night forcing .-> CASE
  GCM --> AN[analyses]
  CRM --> AN
  AN --> DS[downstream: biosphere, geography, studies]
```

- **Dashed edges:** a run's output, or the refitted multipliers, returning to a product upstream.
- **Planet record and scenario to CM1 builds:** gravity and the air, which the lab's builds take from the
  specification while they compile them in, where Terluna's read CO2 and O2 from a GCM run's record
  (inventory.md, hand step 9); once the namelist patches pass plan stage 3, those values reach the case
  inputs alone.

## Producers today

| Product | Command in Terluna, from its repository root | Cost |
|---|---|---|
| Planet record, T21 surfaces | `python -m climate.gcm.boundary` | Seconds |
| Spectrum files, flux | Written by `exoplasim_run` as each run starts | Seconds |
| Shield transmission | `python -m protection.spectra.transmission` | Seconds |
| Middle-atmosphere cases (the column's upper part, ozone) | `python -m atmosphere.middle_atmosphere.run [--only CASE]` | 7–15 min a case on 4 cores |
| Reference columns | `python -m atmosphere.radiative_convective.run [--only SWEEP]` | 1–2 min a column on 8 cores |
| Ledger | `python -m climate.gcm.twilight optics`, then `longwave`, `solve` and `ledger`, in `venvs/optics` | About 50 min on 6 threads |
| Gas-band fits | `python -m climate.gcm.plasim_shortwave gases` | Minutes |
| Radiation check on a GCM run's columns | `python -m climate.gcm.radiation_check RUN --years A B` | About 30 min on 8 cores |
| Shortwave fit | `python -m climate.gcm.plasim_shortwave fit RUN --years A B --lunar`, then copied by hand into `MODEL` | Minutes |
| Longwave correction | `python -m climate.gcm.plasim_longwave fit RUN --year 0`, on a run with heating diagnostics | About 2 min |
| Water continuum (`TH2OC`) | Hand trials in calibration runs (`gcm-runs/cal_*`), the chosen value typed into `MODEL` | A GCM run for each value tried |
| Seas and lakes | Terluna's `geography/atlas.py`, from the heights and the seas share, and `geography/drainage.py`, from a GCM run's runoff | Untimed in Terluna |
| Infrared from space | Terluna's `research/studies/solar_shield_array/glow.py`, copied into a study's runner | Untimed in Terluna |
| CM1 builds | `python -m climate.crm.cm1_run build LABEL…` | Minutes each |
| GCM experiment | `python -m climate.gcm.exoplasim_run A28 --folder NAME --years 20 --ncpus 4 [--set …] [--start-from …]` | 2.5–4.7 min a model year, on 4 to 8 ranks |
| CM1 case | `python -m climate.crm.cm1_run setup CASE`, then `run CASE --hours H --threads T` | 1.8–12.3 h a ring and 2.3–27.2 h a box, for two lunar days |
| Analyses | `python -m climate.gcm.climatology RUN:Y`, `python -m climate.crm.ring_analysis CASE`, and the others in the inventory | Minutes each |

## Parameter by parameter

Marks: ● produced again; ○ produced again through a loop, once the GCM experiment has run again and if the
loop is closed; b produced again while CM1's builds compile gravity and the air in, and unaffected once the
namelist patches pass plan stage 3 (cross-dependency 3); c kept, after a consistency or range check;
— unaffected.

Two rules add marks to every row:

- **The target stage.** Where a scenario's sunlight scale follows its reference temperature, each change
  that marks the GCM experiment ● also produces the spectrum files and flux again through the target
  stage, as ○.
- **The runoff chain.** A change of the heights or the water share produces the seas and lakes again, and
  each change that marks the GCM experiment ● reaches the lakes through the runoff chain, as ○.

The product groups that head the columns:

| Column | Product group |
|---|---|
| Plan | Planet record and derived quantities, ExoPlaSim's calendar among them |
| Srf | T21 surface files |
| Sun | Spectrum files and flux |
| Col | Design column |
| Led | Ledger |
| Gas | Gas-band fits |
| SW | Shortwave fits |
| LW | Longwave correction and water continuum, which share their marks |
| ExB | ExoPlaSim build |
| CMB | CM1 builds |
| GCM | GCM experiment |
| Case | CM1 case inputs |
| Down | CM1 runs, analyses and downstream consumers |

| Parameter | Plan | Srf | Sun | Col | Led | Gas | SW | LW | ExB | CMB | GCM | Case | Down |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Radius or GM | ● | ● | — | ● | ● | ● | ●○ | ●○ | — | b | ● | ● | ● |
| Rotation period | ● | ● | — | ● | ● | ● | ●○ | ●○ | — | b | ● | ● | ● |
| Solar day, where stated | ● | — | — | — | — | — | — | — | — | — | ● where the stated day becomes or ceases to be exactly one day, otherwise c | ● | ● |
| Tilt, year, eccentricity | ● | — | — | — | — | — | ○ | ○ | — | — | ● | ● | ● |
| Star spectrum (shape) | ● | — | ● | ● | ● | ● | ●○ | ○ | — | c | ● | ● | ● |
| Star total, or distance | ● | — | ● | ● | c | c | ○ | ○ | — | — | ● | ● | ● |
| Surface pressure | ● | — | — | ● | ● | ● | ●○ | ●○ | — | b | ● | ● | ● |
| O2 or CO2 | ● | — | — | ● | ● | ● | ●○ | ●○ | — | b | ● | ● | ● |
| Ar/N2 alone | ● | — | — | ● | ● | ● | ●○ | ●○ | — | — | ● | ● | ● |
| Reference temperature | ● | — | ● where the scale follows it | ● | ● | ● | ●○ | ○ | — | — | ● | ● | ● |
| Cloud droplets | — | — | — | — | — | — | — | — | — | — | — | ● | ● |
| Surface heights (world) | ● | ● | — | — | ● | — | ●○ | ○ | — | — | ● | ● | ● |
| Water share, seas, lakes | ● | ● | — | — | ● | — | ●○ | ○ | — | — | ● | ● | ● |
| Land albedo | — | — | — | — | ● | — | ●○ | ○ | — | — | ● | ● | ● |
| Shield (filter) | ● | — | ● | ● | ● | ● | ●○ | ○ | — | c | ● | ● | ● |
| Sunlight scale | ● | — | ● | ● | c | c | ○ | ○ | — | — | ● | ● | ● |
| Infrared from space | — | — | — | — | — | — | ○ | ○ | — | c | ● | ● | ● |
| GCM resolution | — | ● | — | — | — | — | ○ | ○ | ● | — | ● | ● | ● |
| GCM levels | — | — | — | — | ● | — | ●○ | ●○ | ● | — | ● | ● | ● |
| GCM time step | ● | — | — | — | — | — | ○ | ○ | — | — | ● | ● | ● |
| A patch switch | — | — | — | — | — | — | ○ | ○ | — | — | ● | ● | ● |
| A refitted calibration | — | — | — | — | — | — | — | — | — | — | ● | ● | ● |
| CM1 grid, physics, variants, case geometry | ● | — | — | — | — | — | — | — | — | ● where a variant adds patches | — | ● | ● |

## Cross-dependencies

1. **The ledger and PlaSim's shortwave depend on each other.** The ledger computes the sunlight the curved
   air absorbs and the infrared it lets escape beyond PlaSim's flat column of the same air, and computes
   that column with PlaSim's Rayleigh and water multipliers and band split (`twilight.py:53-55, 476, 491`).
   The shortwave fit then uses the ledger's slant factors.
2. **The Rayleigh multiplier scales a coefficient that ExoPlaSim derives from the spectrum,** so a
   multiplier fitted under one spectrum is refitted under another.
3. **CM1's builds compile gravity, CO2 and O2** until the namelist patches pass plan stage 3. O2 is held as a
   partial pressure, so a change of surface pressure moves its mole fraction and with it every build, even
   with the O2 partial pressure, the CO2 ppm and the Ar/N2 ratio unchanged. Once the patch passes, the same
   change reaches the case inputs alone.
4. **The tables depend on the sunlight's total through the column's state.**
   - The design column is computed under a stated sunlight, so a new scale or a new stellar total makes
     it stale.
   - Being per unit sunlight, the ledger's terms and the gas fits change under a spectrally flat scale
     only through the column's temperature and water. The lab checks those against the states each table
     was computed on.
   - Terluna's design column still holds the earlier scale of 0.95 and 294.9 K, while the design case runs
     at 0.970.
5. **The lakes come from GCM run A's runoff,** and the GCM's surfaces are built from those lakes.
6. **A box takes its day–night forcing from a ring's output.** A change upstream of the ring therefore
   arrives at the box twice: through its own GCM extraction, and through the ring.
7. **Albedos typed apart.**
   - CM1's placeholder land row in `LANDUSE.TBL` holds its own albedo of 20%, typed apart from the GCM's 0.2
     (`cm1_run.py:1088`). In the lab both read the scenario's land albedo, so a change alters the CM1 case
     inputs and leaves the builds as they are.
   - Terluna's ledger assumes its own ground albedo of 0.1 (`python/illumination/sky/atmospheres.py:24`). The
     lab's takes the scenario's land albedo and the model's own albedo for open water, weighted by the
     surface mask's water fraction, lakes included, so a change of the land albedo or of the water makes
     the ledger stale.
8. **RRTMG takes the Sun's spectrum unfiltered** (defect log B9), so CM1 receives a shield as the lowered
   total in `var17`.
9. **The design temperature enters as an input,** as the scenario's `air.reference_temperature_k`. The lab
   computes the reference column, the ledger, the gas fits, the surface light and the glow at it, where
   Terluna computed them at 294.9 K. A run that settles elsewhere, as the 307 K test does, leaves them
   describing another state.
10. **Only the GCM receives infrared from space,** through patch 06.
11. **PlaSim's levels enter four calibrations.** The ledger's GCM terms and the longwave correction are
    computed per PlaSim layer, and the offline shortwave copy and the water-continuum fit run on PlaSim's
    levels.
12. **The air has two Ar/N2 ratios.** The reference tools build the air with 0.0093/0.7808 by default
    (`python/atmosphere/radiative_convective/thermodynamics.py:124, 148`), and the GCM runner with
    0.00934/0.78084. Terluna's products hold both; the lab passes the scenario's air to every tool.
13. **Patch 10 compiles in a property of the sunlight.** It writes the weights of Ebert and Curry's four
    near-infrared bands inside PlaSim's band 2 as Fortran constants, `zew(4)` = 0.6164, 0.2283, 0.0811,
    0.0742 (`models/exoplasim/patches/10-ice-optics.patch:70`). Terluna computed them from the unshielded
    TSIS-1 spectrum, where the clouds see the light after the shield; the lab computes them from the
    spectrum at the top of the air.
    - With ice optics on, another star or shield needs new weights, which the planned patch 11 reads from
      the namelist as GCM inputs. Until it passes, runs take patch 10's weights from the unfiltered Sun,
      and registry entry `exoplasim-ice-weights` warns.

14. **Gravity carries the spin term.** The lab takes g as GM/R² less (2/3)Ω²R, so a change of rotation
    reaches every consumer of g, by 5 parts per million on the Moon and 0.3% on Mars; a stated gravity,
    such as Earth's, stays as stated.
15. **CM1's raindrops and soil follow the world.** Its breakup diameter and rain cap scale with the capillary
    length, and its soil layers with the square root of the solar day, so a change of gravity or of the day
    reaches the case inputs through them.

## Loops

| Loop | Closed by | State in Terluna | In the lab |
|---|---|---|---|
| Calibrations fitted on the GCM's own columns: the shortwave multipliers and the longwave correction | Running, taking the columns, refitting and running again until both move less than a tolerance | Fitted once. The longwave correction was fitted at 295 K and runs in a test that settles at 307 K | A fixpoint stage with stated tolerances, each pass recorded |
| The ledger and the shortwave fit | Recomputing the ledger with the refitted multipliers and refitting, until both move less than a tolerance | Open: the ledger holds the multipliers from before the refit | Part of the same fixpoint |
| The sunlight scale and the design temperature | Adjusting the scale until the global mean surface temperature meets the target | By hand. Trial runs at 0.9655, 0.9685 and 0.970 gave 295.02 K at 0.970. The target is open, and new runs are held until it is set (Terluna `research/decisions.md`, 2026-10-17) | A target stage of secant steps over runs, with the runs kept as its record |
| Climate, runoff, lakes, surface | Running the drainage again on the current design run's runoff | Deferred on 2026-10-16 | A chain of keyed links: each GCM run's lakes come from the runoff of a named earlier run (`lakes_from`), and a fixpoint step repeats the chain on request |
| The glow and the GCM's efficacy | Recomputing the glow's dimming with the efficacy the GCM returns | By hand: 0.71, then about 0.59 on the corrected radiation | A loop of two stages |
| Other gases as CO2 | Fitting the CO2 that warms as much as the other gases (755 ppm) against the reduced-gas forcing | By hand, from calibration runs | A calibration with its envelope |

## Worked examples

**(a) A stated sunlight scale from 0.970 to 0.960.**

- **Produced again:** the flux (`GSOL0`), the design column, the GCM experiment, the CM1 cases' `var17`, the
  CM1 runs and the analyses.
- **Checked against their envelopes and kept:** the ledger and the gas fits (cross-dependency 4). They are
  recomputed if the new column's state falls outside the states they were computed on.
- **Through the loop, when it is closed:** the shortwave and longwave fits, on the new run's columns.
- **Cost:** the column case, 7–15 min; a 20-year GCM run, 75–95 min on 4 ranks; then 1.8–12.3 h a ring.
- **In Terluna:** a new folder with `--set sunlight_scale=0.960`. A case reads the new run's flux once it
  names the run, and a build compiled for another run's air is accepted while CO2 and O2 match.

**(b) The surface pressure from 1.2 to 1.0 atm** (`moon/open-moon-1.0atm`).

- **Produced again:** the derived air and everything downstream of it:
  - ExoPlaSim's gases, `GASCON` and `ZGASW`, and an O2 mole fraction of 0.20949 against 0.17458;
  - the middle-atmosphere case, the design column, the ledger and the gas fits;
  - every CM1 build while builds compile the air in, then the GCM experiment, with the sunlight scale found
    again by the target stage, since the scenario's scale follows its reference temperature;
  - CM1's lengths, by 0.46%, through the air's molar mass;
  - through the loop, the radiation check, the shortwave and longwave fits and the GCM again;
  - the cases and the analyses.
- **Range check:** the 1,053.63 hPa limit of RRTMG's tables.
  - 1.0 atm (1,013.25 hPa) stays inside it.
  - The design's 1.2 atm (1,215.9 hPa) lies beyond it, and is extrapolated over the lowest 7.5 km (defect
    log B22).
- **Cost:**

  | Step | Cost |
  |---|---|
  | The column cases | 15–30 min |
  | The ledger | About 50 min |
  | The target stage's GCM runs, three or four | About 75 min each |
  | Two GCM runs | About 3 h |
  | The radiation check and fits | About 40 min |
  | The rings | 1.8–12.3 h each |

- **In Terluna:** this change was run as experiment C, with the 25% seas, before the radiation was
  calibrated. Repeating it now means editing the twenty or so files into which 1.2 atm is typed.

**(c) A new body: Mars held at 1 bar** (`mars/breathable-1bar`).

- **Produced again:** everything.
- **The registry entries the reach report must raise,** two of them beyond the fourteen-entry seed (A3 and
  the column-mass envelope), which stage 6 adds:
  - a gravity of 3.72 m/s² against CM1's 9.81: the core patches are required, the schemes that hard-code
    Earth's gravity are refused, and rain's limits scale 1.62 times by the capillary length;
  - a solar day of 1.0275 d, 0.15% longer than the rotation: PlaSim's own clock would skip back about 1° a
    model day, which the synodic clock repairs, and each model year must still hold whole model days
    (defect log A3);
  - H/R of 0.0066 and a horizon factor of 15.5 against PlaSim's 35: a ledger of its own column;
  - a model day of 1.0289 d: Slingo's cloud cover needs patch 03's convective day (B11);
  - CCM3's cloud water at 3.72 m/s²: patch 02's gravity switch (B12);
  - a column 2.6 times Earth's: every calibration refitted;
  - a tilt of 25.19°: the equinox-Sun entry warns until the planned declination patch gives each case its
    season's.
- **Before any of this:** the lab refuses every stage that reads an unchosen field (the world's surface
  heights, the scenario's seas, land, ozone and cloud droplets) until it is chosen.

**(d) Ice optics switched on.**

- **Produced again:** the GCM experiment and what is forced from it, and the longwave correction, which was
  fitted with ice optics off. The fixpoint refits it with them on, as the author chose on 2026-10-17, and
  the GCM takes the ice-optics weights of its own sunlight through patch 11.
