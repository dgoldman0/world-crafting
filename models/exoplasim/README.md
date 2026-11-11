# ExoPlaSim 3.4.2 for a breathable Moon

Fourteen patches to PlaSim's radiation, cloud, surface-transfer and rain code inside ExoPlaSim 3.4.2, the
settings that carry the Moon's orbit and calendar, the level set generated for a world, which takes no patch,
and the design case's namelists and input tables. The first
ten patches are Terluna's and the eleventh the world-crafting lab's; the lab wrote the twelfth, thirteenth and
fourteenth from Terluna's later code. Each patch adds a namelist switch, patch 14 a third value of PlaSim's own
`NEVAPPREC`, whose default reproduces ExoPlaSim as released, and each of patches 11 to 14 at its default
reproduces the build of the patches before it. Correctness, limits and room for improvement are in
[../../notes/exoplasim.md](../../notes/exoplasim.md).

## Upstream pin

| | |
|---|---|
| Source | ExoPlaSim 3.4.2, source distribution from PyPI (`pip download exoplasim==3.4.2 --no-binary :all:`) |
| sha256 of `exoplasim-3.4.2.tar.gz` | `fae502a92f5997ffd18b0bb85b9f0f0677857c62c5d1293f605c9799026f64c2` |
| Licence | GNU GPL version 3 (`LICENSE.TXT` in the distribution); these patches are distributed under the same licence |
| Patched files | `exoplasim/plasim/src/radmod.f90`, `exoplasim/plasim/src/rainmod.f90`, `exoplasim/plasim/src/fluxmod.f90` |

## Applying the series

The patches take paths relative to the installed `exoplasim` package folder (the one holding
`__init__.py`):

```sh
cd "$(python -c 'import exoplasim, os; print(os.path.dirname(exoplasim.__file__))')"
for p in $(cat /path/to/world-crafting/models/exoplasim/patches/series); do
    patch -p1 < /path/to/world-crafting/models/exoplasim/patches/$p
done
rm -f plasim/run/most_plasim_*.x      # ExoPlaSim recompiles PlaSim at the next run
```

Terluna applied patches 01–06 to its shared installation and 07–10 to a separate copy that every run
imports first since 2026-10-14, so earlier runs kept their source. Applied in order to a pristine
3.4.2, patches 01–10 give `radmod.f90` sha256 `a49791572fa8f5b2…` and `rainmod.f90` `44c0668de3e8f7db…`,
the copy deployed on 2026-10-17 byte for byte (`expected.sha256`); patches 11 to 14 follow them, and the
whole series gives `radmod.f90` `50e3df63c3d9872e…`, as patch 11 left it, `fluxmod.f90`
`6e6b0a1521d5cf97…`, as patch 13 left it, and `rainmod.f90` `7e83a5b6b2caef9f…` (`expected-series.sha256`). The
lab compiles each point of the series as a build of its own (`lab/worldlab/builds.py`).

## The patches

| # | Patch | Switch (namelist) | Default | Change | Kind |
|---|---|---|---|---|---|
| 01 | `rayleigh-scale` | `RAYSCALE` (radmod) | 1.0 | Multiplies the Rayleigh coefficient ExoPlaSim derives from the stellar spectrum | Calibration |
| 02 | `cloud-water-gravity` | `CWGREF`, `CWSCALE` (rainmod) | 0 (the planet's g), 1.0 | Counts the CCM3 cloud-water profile's heights and precipitable water at a reference gravity, and scales the diagnosed water | General repair |
| 03 | `convective-day` | `CONVDAY` (rainmod) | 0 (the model's solar day) | Counts convective rain per `CONVDAY` seconds in Slingo's cover formula | General repair |
| 04 | `sun-clock` | `NSUNCLOCK` (radmod) | 0 (PlaSim's clock) | 1: one turn per model day; 2: the synodic rate, continuous from step 0 | General repair (removes a defect) |
| 05 | `water-shortwave-absorptivity` | `SWH2OSCALE` (radmod) | 1.0 | Multiplies water vapour's near-infrared absorptivity, keeping the band's transmission above 0.001 | Calibration |
| 06 | `top-infrared` | `IRTOPDAY`, `IRTOPNIGHT` (radmod) | 0, 0 | Adds infrared from space to the downward longwave flux at the model top, by day and by night | Capability |
| 07 | `curved-air` | `NTWILIGHT`, `NTWILW`, `ZMLUNAR(3)` (radmod); `twilight.dat` | 0, 0, 0 (Earth's slant factor) | Adds the sunlight and the infrared escape the tall curved air adds to flat columns, by solar elevation (below the horizon too) and layer; replaces Earth's horizon slant factor | General repair (method); lunar table |
| 08 | `gas-bands` | `NGASBANDS`, `ZGASQ(5,3)`, `ZGASW(2)`, `ZMAIRLUNAR(3)` (radmod) | 0 | CO2 and O2 absorption in PlaSim's two solar bands, along a slant path for well-mixed air | Calibration (its structure general, its coefficients lunar fits) |
| 09 | `longwave-by-height` | `NLWCORR` (radmod); `lwcorr.dat` | 0 | Adds a fitted extra escape to space for each layer and the ground, over land and over sea, scaled with temperature to the fourth power | Calibration |
| 10 | `ice-optics` | `NICEOPT`, `TICEOPT` (radmod) | 0, 235.15 K | Gives cloud colder than `TICEOPT` Ebert and Curry's ice optics (CAM3's, as RRTMG carries them) through a delta-scaled PIFM two-stream, with the Kristjánsson–Mitchell effective radius | General repair, within the parameterization's range (crystals of 10 µm and more, which the radius table reaches above 190 K) |
| 11 | `ice-weights` | `ZICEW(4)` (radmod) | patch 10's 0.6164, 0.2283, 0.0811, 0.0742 | Reads the shares of Ebert and Curry's four near-infrared bands within PlaSim's band 2 from the namelist, where patch 10 held them as constants from the unfiltered TSIS-1 Sun; the lab writes the shares of the light at the top of the air | General repair (the world-crafting lab's) |
| 12 | `surface-gust` | `NGUST`; `GUST_BETA`, `GUST_UMIN`; `PBL_B`, `PBL_EPS`, `PBL_BETAM`, `PBL_RICRU`, `PBL_BU` (fluxmod) | 0; 1.0, 0.1 m/s; 8.5, 0.1, 15, 0, 100 | 1: adds Beljaars's convective gust β w* to the lowest level's wind in the surface transfer, at least `GUST_UMIN`, and gives unstable water Louis's factor as land has it, in place of the free-convection term with its Earth constant and the least wind of 1 m/s; w* takes the surface fluxes of the step before and a boundary-layer depth by the bulk Richardson rule | General repair of an Earth value (B33, and B32's wind floor in the surface transfer), for convective surface layers; written by the lab from Terluna's code |
| 13 | `similarity-over-water` | `NSIMW`; `SIMW_MUB`, `SIMW_MUS` (fluxmod) | 0; 1.458 × 10⁻⁶ kg m⁻¹ s⁻¹ K⁻½, 110.4 K | 1: over ice-free water, takes the transfer of heat, vapour and momentum from CM1's surface-layer similarity at the lowest level's height, under the gust's wind, with the air's kinematic viscosity derived in each column | General repair, where the lowest level stands inside the surface layer; written by the lab from Terluna's code |
| 14 | `rain-from-drop-sizes` | `NEVAPPREC` 2, a third value of PlaSim's switch; `NRDROP_JOIN`, `RDROP_WARM`, `RDROP_MELT`; `RDROP_KSC`, `RDROP_RHOEXP`, `RDROP_STEP` (rainmod); `lab_rain_law.txt` | 1, PlaSim's own; 2, 0 m, 0 m; 5.78 m³ kg⁻¹ s⁻¹, 0, 1,000 m | 2: evaporates falling rain from its drops' sizes and fall speeds, in place of the share `gamma` of each layer's saturation deficit. The rain's drops fall with it as a second flux, Morrison's ventilated evaporation and self-collection with breakup act through each layer, and the fall law of the world's rain comes from a table in the run's folder | General repair of an Earth value (B30), for air of Earth-like composition under Morrison's exponential drop spectrum; the rule and the sizes of the rain's births are a calibration that a study supplies; written by the lab from Terluna's code |

## The surface gust and the similarity over water (patches 12 and 13)

Patches 12 and 13 add to `fluxmod.f90` the surface transfer that Terluna wrote on 28 and 29 October 2026
(`climate/gcm/surface_gust.py` and `surface_similarity.py` on `domain/climate` at `39c5ee04`). Terluna's runner
applies that code as edit lists over its free-convection and nonlocal boundary-layer patches; the lab wrote it as
two unified patches, each behind its own switch. The lab's writer sets both through `switches.surface_gust`
(`lab/configs/exoplasim/defaults.toml`): `none`, the released model's transfer, which stays the default until the
Earth control's test (`PLAN.md`); `beljaars`, `NGUST` 1; and `beljaars_similarity`, `NGUST` 1 with `NSIMW` 1. It
writes each switch where the run's series holds its patch and refuses a gust whose patches the series lacks.

**What changes.** PlaSim's `surflx` gives each surface the transfer |U| C_N F: the lowest level's wind, at least
1 m/s, a neutral coefficient from that level's height and the roughness, and Louis's factors of the bulk Richardson
number. Over unstable water the factor for heat and vapour is instead Miller, Beljaars and Palmer's (1992)
interpolation toward free convection over a tank, whose constant, 0.0016 m s⁻¹ K⁻¹ᐟ³, is the still-air limit of a
tank law at Earth's gravity and sea-level air (defect log B33).

- With `NGUST` 1 the wind in the bulk formulas is max(√(|U|² + (β w*)²), u_min), where
  w* = (g/θ_v · h · (w′θ_v′)₀)^⅓ is the convective velocity of the boundary layer's eddies in unstable air and nil
  in stable or neutral air (Beljaars 1995, as CM1's surface layer takes it). The Richardson number takes that wind,
  and unstable water takes Louis's factor as land does. The buoyancy flux (w′θ_v′)₀ comes from the sensible heat and
  the evaporation of the step before, and the depth h from the rule of Terluna's nonlocal boundary layer: the bulk
  Richardson number, counted from the lowest level upward with 100 u*² in its shear, reaches zero at h for a parcel
  that carries the thermals' excess 8.5 (w′θ_v′)₀/w_m (Holtslag and Boville 1993 as CAM3 has it; Vogelezang and
  Holtslag 1996; Hong, Noh and Dudhia 2006). The series has no patch for the nonlocal scheme, so patch 12 declares
  the five constants that its depth rule reads, under Terluna's names. PlaSim's `zumin` keeps its second use, the
  least wind shear in the vertical diffusion.
- With `NSIMW` 1 as well, each ice-free water column takes its transfer velocities from CM1's surface layer over
  water (`sfclay.F`, `sfcmodel` 2 with `isftcflx` 0), evaluated at the lowest level's height under the gust's wind:
  κu*/ψ_q for heat and vapour and u*²/U for momentum. The bulk Richardson number selects the regime, Paulson's
  functions serve unstable air, the roughness is Charnock's with the smooth-flow term, the roughness for heat and
  vapour is Fairall's, and u*, the temperature scale and the roughness pass from each step to the next as CM1
  carries them. The velocities enter `surflx` as its stability factors against the neutral coefficient, in which
  PlaSim's own sea roughness then cancels, so the stress, the sensible heat and the evaporation's implicit step take
  them unchanged. Land, sea ice and partly frozen sea keep Louis's factors under the gust's wind.

**The world's values and Earth's.**

| Quantity | Its value in the patched code |
|---|---|
| Gravity, in w*, the levels' heights, both bulk Richardson numbers, z/L and Charnock's roughness 0.0185 u*²/g | The model's `ga` |
| The gas constant, κ, the heat capacity and the vapour's terms in the virtual temperature and the heat flux | The model's `gascon`, `akap`, `acpd`, `adv` and `rdbrv` |
| The air's density under the surface fluxes | The surface pressure over `gascon` and the surface temperature |
| The air's kinematic viscosity ν, in Fairall's roughness Reynolds number and in the smooth-flow roughness 0.11 ν/u* | Each column's own: Sutherland's dynamic viscosity at the lowest level's temperature, over the density that the surface pressure and `gascon` give. It comes to 1.46 × 10⁻⁵ m²/s at Earth's sea level and 288 K and to 1.31 × 10⁻⁵ m²/s in the Open Moon's air at 300 K. CM1's code, and Terluna's patch after it, sets the viscosity of Earth's sea-level air: (1.32 + 0.009 (T − 273.15)) × 10⁻⁵ m²/s in the Reynolds number and 1.5 × 10⁻⁵ m²/s in the smooth-flow term |
| Sutherland's constants, 1.458 × 10⁻⁶ kg m⁻¹ s⁻¹ K⁻½ and 110.4 K | Earth's dry air, from the 1976 US Standard Atmosphere; `SIMW_MUB` and `SIMW_MUS` set them for another air |
| The cap of 2.85 mm on the sea's roughness | Earth's: WRF's surface layer took it from its hurricane options (`sfclay.F`: "V3.9: Add limit as in isftcflx = 1,2") |
| Charnock's 0.0185; Fairall's roughness for heat and vapour, 5.5 × 10⁻⁵ m (u* z₀/ν)^−0.6 within 2 × 10⁻⁹ and 10⁻⁴ m; Paulson's functions and the regimes' limits | Earth's, from measurements over its seas and in its surface layer |
| β = 1, the least wind of 0.1 m/s, the start of the carried state (u* 0.1 m/s, a roughness of 0.1 mm) and the depth rule's five constants | CM1's and the cited boundary-layer studies', fitted on Earth; β and the depth rule's constants are dimensionless |

**Verification.** The evidence states are those of the notes: none of them validates a climate.

- **The patches apply.** `models/check_patches.sh` applies the whole series to the pinned archive and finds
  the sources of `expected-series.sha256`. On 11 November 2026 the routines of the patched `fluxmod.f90`, from
  `gustnl` through `simwcol`, differed from those of Terluna's deployed copy (`exoplasim-twilight` on its research
  drive) in comment lines and the two viscosity lines alone.
- **They compile.** The lab's builds at patches 01–12 and at patches 01–13 compile PlaSim at T21 on ten levels
  (`lab/tests/test_builds.py`), and the patched `fluxmod.f90` compiles with PlaSim's module on fifteen levels
  (`python/climate/tests/test_surface_gust.py`, `test_surface_similarity.py`).
- **Identity at the defaults.** On Earth's control over 96 steps on four ranks, the build of patches 01–12 gives
  PlaSim's output and restart byte for byte as the build of patches 01–11 from the same folder, and so does the
  build of patches 01–13 with `NGUST` 0 and `NSIMW` 0; with the gust on, that build with `NSIMW` at its default
  gives the output of the build of patches 01–12 (`lab/tests/test_builds.py`). In a harness of `surflx` alone, each patch
  with its switch off prints every digit the routine before it prints.
- **The switches' effect.** In those runs the gust changes the output and the similarity changes it again. On
  Earth's control with the Moon's gravity in place of its own, a made-up world that puts open sea under 1.62 m/s²,
  the whole series runs one day from a cold start with the gust and with the similarity beside it, under the
  floating-point traps ExoPlaSim compiles with, and the similarity changes the state in which the run ends.
- **Agreement with the Python copies.** `surflx` from the patched source, compiled with ExoPlaSim's flags against a
  stub of PlaSim's module, gives the transfer coefficients of `python/climate/gcm/surface_gust.py` and
  `surface_similarity.py`, and the similarity's carried state, to 10⁻¹⁰ on lunar columns on fifteen and forty
  levels and Earth-like columns on ten: sea unstable, calm, windy and stable, land by day, by night and in neutral
  air, and a sea-ice twin, from fresh and settled states.
- **Agreement with Terluna's code.** The gust's Python copy gave every number of Terluna's module at `39c5ee04` bit
  for bit on that module's own 24 test columns (11 November 2026), and the tests pin its numbers on one written-out
  column at each gravity. The similarity's copy, given the 1.5 × 10⁻⁵ m²/s that both of CM1's viscosity lines take
  at 20 °C, gives Terluna's numbers to 10⁻¹², pinned at each gravity.
- **Terluna's runs**, made with its own patches at CM1's viscosities, on fifteen levels under simplified
  Betts–Miller convection: over four years the gust lowered the transfer coefficient for vapour at the Near-side
  Sea site to 0.67 of the baseline's and left the globe 0.18–0.55 K warmer with 6% less rain, and over one lunar
  day the similarity then raised the sea's evaporation 17% and the globe's rain 5% (Terluna's
  `climate/gcm/README.md` at `39c5ee04`).
- **Physical validation** remains to be done. The lab's runs with either switch are the tests' own, of two days at
  most, and the Earth control's test against the released model, which decides whether the two serve every world as
  one component, comes with the lab's first runs (`lab/design/plan.md`, stage 8).

**Limits.**

- The similarity takes the flux as constant with height up to the lowest level. PlaSim's ten levels put that level
  near 0.15 km on Earth and 0.9 km in the Open Moon's air, and Terluna's fifteen-level set near 0.3 km; a warning
  where the level exceeds a tenth of the boundary layer's depth is proposed (`lab/design/terluna_fixes.md`, row 4)
  and unbuilt.
- The depth h comes from the model's own levels: it is at least the lowest level's height, and Terluna records it
  as untested against CM1's depths.
- β is CM1's 1, where COARE takes 1.25, and the buoyancy flux is the step before's.
- The fluxes of the step before and the similarity's carried state stay outside PlaSim's restart file, as in
  Terluna's patch. Each restarted segment therefore starts with one step that takes no gust and with the
  similarity at its start values, from which u* closes about half its distance to the settled value at each step.
- `NSIMW` 1 with `NGUST` 0 runs the similarity under PlaSim's own wind with its floor of 1 m/s; the lab's writer
  sets the similarity only with the gust.
- Four cases are untested anywhere: a run past the tests' 96 steps; a restart with either switch on; `NSIMW` 1
  with `NGUST` 0; and PlaSim compiled in single precision (`precision` 4), where every test builds at 8.
- In strongly stable air CM1's floor of −10 on ψ transfers more than Louis's factors, and CM1's subgrid wind is
  left out (Terluna's record).

**Choices made in the port,** where the design left them open:

- two patches, one for each switch, so that each point of the series adds one capability with its own identity test;
- the depth rule's constants in patch 12 under Terluna's names (`PBL_*`), which a later patch for the nonlocal
  scheme can share;
- PlaSim's free-convection constant left as the released source's literal 0.0016, since the gust drops the term:
  Terluna's namelist variable `cfree` and its lunar value have no patch here;
- the viscosity derived inside the model, column by column, with Sutherland's two constants in the namelist;
- one setting of three values in the lab, with β, the least wind and the depth rule's constants left at the
  patch's defaults;
- the carried state kept outside the restart, as Terluna has it.

## Rain from drop sizes (patch 14)

Patch 14 adds to `rainmod.f90` the evaporation of falling rain that Terluna wrote on 29 October 2026
(`climate/gcm/rain_drops.py` on `domain/climate` at `39c5ee04`, commits `8e805f60` and `f5f767fa`). Terluna's
runner applies that code as an edit list that writes the Moon's fall law into the source as Fortran constants;
the lab wrote it as one unified patch that reads the fall law from the run's folder and takes every other value
of the world from the model's own variables or the namelist. The lab's writer sets it through `switches.rain_evaporation`
(`lab/configs/exoplasim/defaults.toml`): `gamma`, the released model's evaporation, which stays the default
until the Earth control's test (`PLAN.md`), and `drop_sizes`, `NEVAPPREC` 2 with the six entries and the table.
The writer writes `NEVAPPREC` where the run's series holds the patch, refuses the drops' sizes on a series
without it and in a first run, which has no calibration of the births, and refuses a table on which the model
would stop.

**What changes.** PlaSim's `mkrain` takes each column's precipitation down through its layers, as snow where
the air is at or below freezing and as rain above, and evaporates in each unsaturated layer the share `gamma`,
0.01, of the layer's saturation deficit in each step, at most the precipitation there. The constant was set
for Earth, and the scheme takes no account of the drops' sizes or fall speeds (defect log B30). With `NEVAPPREC` 2 the rain
has, beside its mass flux F, the flux of its drops' number F_N, and its spectrum is Morrison's exponential
one, N₀ exp(−λD), whose slope follows from the two fluxes: F_N/F = λ³ V_n(λ)/(π ρ_w V_m(λ)).

- **Evaporation.** In each metre of its fall the rain loses the share
  k = 2ρ D_v λ⁴ W (q_s − q)/(ρ_w V_m AB) of its water, with W = F1R/λ² + F2R (ρ_f ρ/μ)^½ Sc^⅓ T₃, the
  ventilated diffusion of each drop integrated over the spectrum, as CM1's Morrison scheme evaporates its rain.
  AB is PlaSim's own latent-heat factor, and the drops go in proportion to the water.
- **Collisions.** The drops collect one another at the rate K (F/V_m)(F_N/V_n) and break up above a mean
  diameter D_b by the factor 2 − exp(K_B (1/λ − D_b)), which turns negative past the size at which the two
  balance, so that falling rain grows toward that size and stops there. The collisions leave rain thinner than
  10⁻⁸ kg/kg as it is.
- **The fall law.** The mass-weighted and number-weighted mean speeds V_m and V_n and the ventilation integral
  T₃ come from `lab_rain_law.txt`, linear in ln λ, times Morrison's density factor ρ_f = (ρ_ref/ρ)^0.54 and its
  square root. The mean speeds are capped at 9.1 (g/9.81)^¼ m/s times that factor, and the mean diameter lies
  between 20 µm and 2.8 mm (9.81/g)^½.
- **The births.** New rain enters each layer at its middle. Rain melted from snow there comes as drops of mean
  diameter `RDROP_MELT`. Rain formed as rain, W, comes as drops of `RDROP_WARM` with `NRDROP_JOIN` 0; with 1 it
  joins the rain already falling through the layer, and makes new drops where none falls; and with 2 the share
  W/(W + F) of it makes new drops and the rest joins, F being the rain that arrives at the layer's middle.
- **The steps and the bound.** Each half of a layer is taken in midpoint steps of at most `RDROP_STEP`, and a
  layer evaporates at most what would saturate it over the time step, the convective and the large-scale rain
  giving up that water in proportion to their fluxes.

The snow sublimates by `gamma` under either setting, and `mkrain`'s phase rule, which makes each layer's
precipitation all rain or all snow, stays as released. The scheme stores nothing from one step to the next, so
the restart file needs nothing from it.

**The world's values and Earth's.**

| Quantity | Its value in the patched code |
|---|---|
| Gravity, in the layers' depths, the column's mass, the cap on the mean diameter, the cap on the mean fall speeds and the breakup's two lengths | The model's `ga` |
| The gas constant, the vapour's term in the virtual temperature, the heat capacity, the latent heat and the saturation curve behind AB | The model's `gascon`, `rdbrv`, `acpd`, `ADV`, `ALV`, `ra2`, `ra4` and `TMELT` |
| V_m, V_n and T₃ at each slope | `lab_rain_law.txt`, the table that patch 04 of the lab's CM1 series reads: the single-drop solver's terminal speeds in the world's air at 2 m, integrated over the spectrum (`python/atmosphere/rain/fall_law.py`). Terluna's patch compiles the Moon's table in |
| The self-collection rate K | `RDROP_KSC`, by default Morrison's 5.78 m³ kg⁻¹ s⁻¹ for Earth; for a world, that rate over the ratio of Earth's collision kernel to the world's (`fall_law.self_collection`): 2.919 for the Open Moon's air, Terluna's default |
| The breakup's cutoff D_b and rate K_B | Morrison's 300 µm and 2,300 m⁻¹, the length times and the rate over (9.81/g)^½ (p_s/1013.25 hPa)^`RDROP_RHOEXP`, with each column's own surface pressure p_s. The exponent is 0 by default and in Earth's air, and 0.687 for the Open Moon's air, Terluna's default (`python/atmosphere/rain/breakup.py`) |
| The birth rule and the two birth sizes | `NRDROP_JOIN`, `RDROP_WARM` and `RDROP_MELT`, a calibration on cloud-resolving boxes of the world. The patch's defaults leave both sizes at 0, on which a run with `NEVAPPREC` 2 stops. Terluna's defaults are its calibration for the Open Moon: the share rule, 0.439 mm and 2.95 mm |
| Morrison's ventilation coefficients, 0.78 and 0.308; the vapour's diffusivity, 8.794 × 10⁻⁵ T^1.81/p m²/s; the air's viscosity, 1.496 × 10⁻⁶ T^1.5/(T + 120 K) kg m⁻¹ s⁻¹; water's density, 997 kg/m³ | Earth's, as CM1 r22.0's `morrison.F` states them: fits to measurements in Earth's air, which serve air of Earth-like composition at the model's own pressure and temperature |
| The density factor's reference, air at 850 hPa and 0 °C, and its exponent 0.54; the breakup law's form; the bounds of 20 µm and 2.8 mm and the cap of 9.1 m/s at 9.81 m/s²; the floor of 10⁻⁸ kg/kg under self-collection | Morrison's, for Earth's rain; the lengths and the cap scale with gravity as above |
| The step of 1 km and the 2,001 slopes of the inverse table | Numerical settings. Terluna records that 1 km steps stayed within 0.25% of 50 m steps on the fifteen-layer columns of its boxes |

**What a run supplies.** `python/climate/gcm/rain_drops.py` computes the entries and the table for a world from
its air at 2 m, a `drops.Column` of gravity, surface pressure, temperature, humidity and composition, and from a
calibration of the births (`settings`, about three seconds on one thread): `RDROP_KSC` and `RDROP_RHOEXP` as
`fall_law.settings` gives them for CM1's patches 03 and 04, the table as `fall_law.table_text` writes it, and
`NRDROP_JOIN`, `RDROP_WARM` and `RDROP_MELT` from the calibration. `TERLUNA_OPEN_MOON_BIRTHS` in that module
records Terluna's calibration for the Open Moon with its sources: the share rule, adopted on PlaSim's fifteen
levels; new rain of 0.439 mm, CM1's own size where its sea box forms rain as rain afresh; and melted rain of
2.95 mm, the size lunar snow melts into in Terluna's McSnow run at 1 mm/h. Another world, another level set or
another microphysics in the boxes takes a calibration of its own.

**Stops.** With `NEVAPPREC` 2 the run stops at its start, with PlaSim's abort message, on an `NRDROP_JOIN`
other than 0, 1 and 2, on a birth size or a step of zero or less, on a negative rate, on a missing table, on a
table of fewer than two rows, with a step of zero or less, with fewer or more rows than its first line states,
or with a first line it cannot read, and on a table whose F_N/F fails to rise with λ over the scheme's range,
from which no slope could be read back. With `NEVAPPREC` 1 or 0 the run opens no table and uses none of the
six settings.

**Verification.** The evidence states are those of the notes: none of them validates a climate.

- **The patch applies.** `models/check_patches.sh` applies the series of fourteen to the pinned archive and
  finds the sources of `expected-series.sha256`.
- **It compiles.** The lab's build of the whole series compiles PlaSim at T21 on ten levels
  (`lab/tests/test_builds.py`), and the patched `rainmod.f90` compiles with PlaSim's module on fifteen levels
  (`python/climate/tests/test_rain_drops.py`).
- **Identity at the default.** On Earth's control over 96 steps on four ranks, the whole series' build gives
  PlaSim's output and restart byte for byte as the build of patches 01–13, from the folder written for that
  build, whose namelist names none of the patch's entries, and from folders that state `NEVAPPREC` 1
  (`lab/tests/test_builds.py`). In a harness of `mkrain` alone, with `NEVAPPREC` 1 and with 0, the patched
  routine prints every digit that the routine before it prints, on lunar and Earth-like columns, under
  ExoPlaSim's flags and under `-O3 -march=native`.
- **The switch's effect.** In that control the rain evaporated from its drops' sizes, by the fall law of
  Earth's own air and births made up for the test, changes the output and the restart, and without its table the
  run stops with the abort message. On Earth's control under the Moon's gravity, the made-up world of the gust's
  test, the whole series runs two days from a cold start with the Open Moon's table, rate and exponent and
  Terluna's births, under the floating-point traps ExoPlaSim compiles with, and ends in another state than the
  run with `gamma`.
- **Agreement with the Python copy.** `mkrain` from the patched source, compiled with ExoPlaSim's flags against
  a stub of PlaSim's module, reads the table that `fall_law.table_text` writes and gives the tendencies and the
  precipitation of `rain_drops.mkrain` to 10⁻¹⁰ under each of the three birth rules, on lunar columns of fifteen
  levels and Earth-like columns of ten, also with rain falling hard into air 5–30% humid and births of 20 µm,
  0.465 mm and 6.5 mm.
- **Hand arithmetic.** On a table of the closed forms of Morrison's own power law, the copy's two loss rates at
  one slope, its midpoint steps through one layer under falling rain and its count of new drops under each birth
  rule agree to 10⁻⁹ with the same arithmetic written out from the closed forms, at the Moon's gravity and
  Earth's. The copy keeps each column's water to 10⁻¹², evaporates rain in unsaturated air alone, and in
  saturated air its drops grow to between half the breakup's equilibrium size and that size.
- **Agreement with Terluna's code.** From the Open Moon's air the Python gives the entries that Terluna's patch
  sets as defaults, 2.919 m³ kg⁻¹ s⁻¹ and 0.687, with the 6.88 mm cap on the mean diameter and the 5.80 m/s
  cap on the fall speeds, and the tests pin the sums of Terluna's module on its eight test columns at one seed
  under each birth rule. In a single scratch run on 11 November 2026 the copy gave every field of Terluna's
  module at `39c5ee04`, run in place, bit for bit on 72 columns, three seeds under each rule. The five routines
  from `rdroptab` through `rdropevap` equal those of Terluna's deployed `rainmod.f90` (`exoplasim-twilight` on
  its research drive, sha256 `4b154f40d48ab708…`, read that day) in every statement but two, listed under the
  choices below.
- **Wrong code at twelve places.** In a single scratch run on 11 November 2026, twelve wrong statements put one
  at a time into the patch each failed the suite's Fortran tests: a table row read for another, the ventilation
  without the density factor, the share rule's share, the breakup without gravity, the uncapped mass speed, the
  layer's saturation bound, the split between convective and large-scale rain, the drops' loss, the count of
  midpoint steps, the melted rain's size, the default path's evaporation and the rain counted as arriving.
- **The table on every rank.** In a single scratch run that day, `rdropini` from the patch, with its broadcasts
  made through MPI itself, left each of four ranks with the same table, inverse table and cap. That run, the
  twelve wrong statements and the single-precision compile named under the limits used the source as it was
  before one comment of `rdroprates` was reworded; `rainmod.f90` compiles to the same object file, byte for
  byte, from both texts under ExoPlaSim's flags.
- **Terluna's runs**, made with its own patch on fifteen levels under simplified Betts–Miller convection
  (Terluna's `climate/gcm/README.md` at `39c5ee04`, "PlaSim's rain from its drops"). Offline, on the mean air
  of its three CM1 boxes, the share rule with melted rain at CM1's own 0.865 mm gave 0.96–1.05 of CM1's column
  evaporation, and with the lunar 2.95 mm 0.91–0.98; every new drop at one size gave 1.15–1.31 and rain joining
  whatever falls 0.64–0.80. In PlaSim over one lunar day the share rule evaporated 45% of the rain formed,
  against 20% with `gamma`, and brought 1.71 mm/day to the ground against 2.00; Terluna's first build, under the
  one-size rule, ran that day in about 1% more time than `gamma`'s. The lab has run none of these.
- **Physical validation** remains to be done. The lab's runs with the switch are the tests' own, of two days,
  and the Earth control's test against the released model, which decides whether the scheme serves every world
  as one component, comes with the lab's first runs (`lab/design/plan.md`, stage 8).

**Limits.**

- The births are a calibration. Terluna fitted its rule and sizes on three CM1 boxes of the Open Moon, on its
  fifteen levels, and the share W/(W + F) depends on the layers' thickness: on CM1's own levels Terluna's rule
  made 42–47% of the rain formed as rain into new drops, against 65–69% on PlaSim's layers. One melted size
  serves every snowfall. The lab has no calibration for Earth or for any other world, and its writer refuses
  the drops' sizes without one.
- The CM1 boxes behind that calibration ran Khairoutdinov and Kogan's Earth rates of autoconversion and
  accretion (defect log B38) and ice sized by Earth's limits, so the size of new rain, 0.439 mm, inherits both.
- The collisions follow Morrison's self-collection and breakup, taken to another gravity by the drops' Weber
  number, a similarity that no measurement at another gravity tests (`python/atmosphere/rain/breakup.py`). The
  exponent is fitted on the two airs' densities, and the scheme raises the pressure ratio to it, as CM1's patch
  03 does: for the Open Moon's air the breakup's scale is then 0.2% larger than the collisions' own.
- The diffusivity and the viscosity are Morrison's fits for Earth's air, and the fall law is the solver's in
  the world's air at 2 m, at one temperature and humidity, taken to each level by the density factor alone.
- The collisions take the grid cell's mean rain content. On the rain-covered shares of Terluna's boxes, 25–78%
  by level, the content inside the rain moved the column's evaporation by at most 0.03 of CM1's.
- New rain enters at each layer's middle. In the thick layer about the Moon's freezing level, Terluna's column
  therefore took its new rain in near 29 km, where CM1 formed that layer's rain at 24.5–25.9 km on average.
- The table's text states ten significant digits, so the model's moments lie within 10⁻⁸ of the solver's.
- Untested anywhere: a run past the tests' 96 steps; a run restarted with the switch on; a level set other
  than PlaSim's ten in the whole model; ranks other than four; and a run of PlaSim compiled in single precision
  (`precision` 4), where every test builds at 8 and the patched `rainmod.f90` was compiled once at 4, in a
  scratch folder, without a warning in the patch's lines.

**Choices made in the port,** where the lab's form differs from Terluna's or the design left it open:

- the fall law in a table in the run's folder, in the format and under the name of CM1's, so that one writer
  serves both models, where Terluna's patch declares the Moon's 301 rows as Fortran parameters;
- the defaults of an Earth run or none: Morrison's 5.78 m³ kg⁻¹ s⁻¹, an exponent of 0 and birth sizes of 0 that
  stop the run, where Terluna's patch defaults to the Moon's rate, exponent and births;
- the set-up in `rdropini`, called once from `rainini` on every rank, with the stops above, where Terluna's
  `rdropevap` builds the inverse table at its first call and checks nothing;
- one condition of `mkrain` widened and one branch around its two statements for rain, so that the saturation
  and the snow's sublimation by `gamma` are written once, where Terluna's patch repeats them, about thirty
  lines, in a block of its own; the identity tests above were run on this form;
- the slope read from `LOG(pn/pf)`, where Terluna's statement guards `pn` with a constant of 10⁻³⁰⁰ that the
  routine's first test already makes idle and that underflows in a single-precision build;
- the snow's sublimation by its flakes, which Terluna's `mkrain` calls behind `nsnowsub`, left out until its
  assessment (`PLAN.md`), with the output diagnostics that serve it;
- one setting of two values in the lab, `switches.rain_evaporation`, with the rain's entries and table in one
  record of the run's calibrations (`RainDrops` in `lab/worldlab/exoplasim.py`).

## Level sets (no source change)

PlaSim reads its half levels from the namelist under `NEQSIG` −1 (`SIGH`; `plasim.f90`, `initpm`), so a level
set for a world takes no patch: the lab's writer states the set in `plasim_namelist`, and the run's build
compiles PlaSim for the set's count. Terluna's fourteen and fifteen levels have the same form
(`climate/gcm/levels.py` at `39c5ee04`: three named sets, a run's entries and a restart's remap). The module
came over as `python/climate/gcm/levels.py`, with a rule that generates a world's set from its scale height in
place of the named sets (defect log B31).

**The setting.** A run's `levels` (`lab/configs/exoplasim/defaults.toml`) takes one of two forms:

| Value | The run's levels | Entries in `plasim_namelist` |
|---|---|---|
| A count, 10 by default | The released model's own, from PlaSim's formula | `NEQSIG` 0, as configure writes it |
| A table of `scale_height_m`, `upper` and `interfaces_m` | A set generated for the world | `NEQSIG` −1; the half levels in `SIGH`; in `TFRC`, in seconds, the Rayleigh friction of 20 and 100 days that PlaSim presets on its top two levels where it is compiled for ten |

A study supplies the table's three values for its world: the scale height at which the heights are counted, a
number of metres or `"scenario"` for the scenario's own at its reference temperature; `upper`, from 2 to 9, the
count of the released model's highest half levels that the set keeps; and `interfaces_m`, the heights above
the ground of the half levels below them, the highest first. The set's count is `upper` plus the heights plus
one. With the default the writer's files are those it wrote before the setting took a table.

**The rule** (`levels.generate`). The set keeps the released model's `upper` highest half levels in the doubles
the compiled model computes, puts one half level at each stated height, at σ = exp(−z/H) to four places, and
ends at the ground's 1. A height that falls on a released half level at four places takes that half level's own
double, so that a layer two sets share holds the same numbers in both. The heights are a world's layer
boundaries near its ground: the depth of its lowest layer, whose middle in σ is the level at which PlaSim takes
its surface fluxes, and boundaries through its boundary layer and its low cloud. The rule converts them at one
scale height, and a run's own temperatures set the heights its levels stand at. It refuses heights out of
order, a height at or above the lowest released half level kept, a height within the rounding of its neighbour
or of the ground, and a set that keeps fewer than the released model's two highest half levels, whose layers
take the friction.

**Terluna's fifteen levels for the Open Moon** are what the rule returns from Terluna's values
(`levels.TERLUNA_OPEN_MOON_LEVELS`): heights counted at 51 km, the released model's six upper half levels, and
half levels at 15.5, 11.5, 9.0, 7.0, 5.0, 3.1, 1.73 and 0.60 km, the seventh of them the released model's own
lowest. Terluna placed them by hand from its CM1 sea box, whose 6 km boundary layer and night cloud from 6.2 km
to tops at 7–8 km fall inside the released model's one layer from 6.4 to 13.7 km, and whose air at 50 m holds
1.4–2.3 kJ/kg more moist static energy than the released lowest layer, the ground to 1.73 km.

| | The released ten | The Open Moon's fifteen |
|---|---|---|
| Half levels, σ | 0.0766, 0.1616, 0.2601, 0.3736, 0.5, 0.6336, 0.7651, 0.8816, 0.9666, 1 | 0.0766, 0.1616, 0.2601, 0.3736, 0.5, 0.6336, 0.7379, 0.7981, 0.8382, 0.8717, 0.9066, 0.9410, 0.9666, 0.9883, 1 |
| Full levels, km at 51 km | 166, 108, 79, 59, 42, 29, 18.2, 9.9, 4.0, 0.86 | 166, 108, 79, 59, 42, 29, 19.2, 13.5, 10.2, 8.0, 6.0, 4.0, 2.4, 1.16, 0.30 |
| Least share of mass a layer holds of the layer above | 0.39, the lowest layer's | 0.54, the lowest layer's |

The fifteen equal Terluna's at the four places it states them (`climate/results/gcm/levels_l15_test.json`), and
without the last height the same values give its fourteen. Two of the fifteen doubles, 0.3736 and 0.9666,
differ in the last bit from those that Terluna's runs state in `SIGH`: Terluna's module computes the released
formula with numpy's powers, and the lab keeps the doubles of the compiled model, which multiplies the powers
out, so that the layers a generated set keeps are the released model's own to the bit. The values are a record
that a study of the Open Moon states; counted at the scenario's own 52.4 km, the same heights give other half
levels, 0.9886 for the lowest.

**Earth.** In Earth's air at 288 K, H 8.43 km, the released ten put the lowest full level at 142 m under a
lowest layer 286 m deep, where the Open Moon's stand at 882 m and 1,779 m. The rule has nothing to add near
Earth's ground: it refuses the Open Moon's 600 m layer there, which is deeper than the released model's own,
and the Earth control keeps `levels = 10`, as `PLAN.md` decides for a world whose scale height is near
Earth's. Registry entry B31 warns where a run's lowest full level stands above a proposed 350 m at the
scenario's scale height (`exoplasim_lowest_level_m`): the Open Moon on the ten draws the warning, and on the
fifteen, at 307 m, it falls silent.

**What follows the count in PlaSim.** The friction's preset holds for ten levels alone (`readnl`), which the
`TFRC` entry replaces. `rainmod` presets `gamma` 0.007 for ten levels at T42 and switches the shallow
convection off for five at T21 (`rainini`), so the writer refuses a generated set of another count at T42 and
one of five levels at T21. `radmod`'s presets by level count are idle in every run, since `radini` tests the
daily cycle's module default, on, before it reads the namelist. The reference temperature of the semi-implicit
scheme is 250 K at every level of every set, and the lowest layer's cloud threshold `RCRIT` takes the set's
count as its index.

**Calibrations by layer.** `twilight.dat` and `lwcorr.dat` hold one value for each layer, so the ledger and the
longwave correction state the half levels their rows are laid on (`Ledger.half_levels`,
`Longwave.half_levels`). The writer reads them on those half levels alone, each within 10⁻⁹ of the run's, and
on a generated set it refuses a calibration that states none. A calibration fitted on one set and read on
another lies outside its envelope (registry `exoplasim-longwave-fit`, `exoplasim-rain-births`).

**The restart** (`levels.carry_restart`). PlaSim reads a restart by its records' names and takes each field at
the size of its own level count, so a restart from one set starts a run on another once it is carried there.
σ counts the air's mass, and the carry is a conservative remap in σ: each old layer's profile is reconstructed
linearly about its full level with the centred slope of its neighbours, and each new layer takes the mean over
its σ range. The surface pressure, and with it each column's mass, stays as it is, and each column keeps its
integrals over σ of vorticity, divergence, temperature and vapour, so its water and its enthalpy at a constant
heat capacity; kinetic and potential energy lie outside what it keeps. Shared layers are copied bit for bit,
and a restart carried onto its own set comes back byte for byte. The remap is one linear operator in the
vertical, so it acts on the spectral coefficients directly. Its slopes are unlimited, so a new layer's value
can pass its neighbours' where a profile bends sharply; the cloud cover is then clipped to 0–1 and the cloud
water to 0 and above, two fields that the radiation of the run's first step reads and `mkclouds` then computes
anew. A record sized like a field by level that the carrier's lists leave out stops the carry.

**Verification** (2026-11-11), by what each check shows:

- **The default writes what it wrote.** For an integer `levels` the writer states `NEQSIG` 0 and neither
  `SIGH` nor `TFRC` (`lab/tests/test_exoplasim_files.py`). In a single scratch run the working tree and the
  tree at `10bf621` wrote the same 114 files, byte for byte, for five runs on the released ten: Earth's
  control, the Open Moon's first design run, its longwave-and-ice run, one with the surface cloud's threshold
  and the gust, and the waterworld seed. The store's five ten-level builds were found under their keys.
- **The namelist's route is the released model's.** On Earth's control over two days (96 steps), the whole
  series' build gives the same output and restart, byte for byte, from the folder that leaves the levels to
  PlaSim's formula and from one that states the released ten as a generated set, through `NEQSIG` −1, `SIGH`
  and `TFRC`; the two folders differ in those three entries alone (`lab/tests/test_builds.py`). The test also
  pins the released half levels' doubles: in a single scratch run the same ten written with numpy's powers,
  which end one or two units of the last place away at 0.3736, 0.8816 and 0.9666, changed the output and the
  restart.
- **PlaSim on a generated set.** On Earth's surface under the Moon's gravity, the build compiled for fifteen
  levels runs two days from a cold start on the Open Moon's fifteen, under the floating-point traps ExoPlaSim
  compiles with; its output's header states fifteen levels and the set's half levels, and its diagnostic
  prints the set's full levels to eight places. A ten-level run's restart, carried onto the set, starts a
  fifteen-level run that counts its steps on from the restart's and ends in another state than the cold start.
  The runs test the code's path and no climate. In a single scratch run Earth's control at Earth's own
  gravity, where the fifteen's lowest level stands near 50 m, also ran two days from a cold start and from a
  carried restart.
- **The carry.** On that restart each spectral field keeps its column integrals within 10⁻¹⁰ of their size,
  the test's bound, and the restart carried onto its own ten levels comes back byte for byte. In Python the
  remap keeps column integrals to 10⁻¹¹ on random fields, reproduces linear profiles to 10⁻¹³, copies shared
  layers exactly, agrees with hand arithmetic on two layers split into four, and refuses a restart of another
  level count, an unknown field by level, a truncated file and an existing target
  (`python/climate/tests/test_levels.py`).
- **The rule.** `generate` agrees with hand arithmetic at a 10 km scale height, returns the released ten from
  their own heights at four scale heights, gives Terluna's fifteen and fourteen at the four places Terluna
  states, with the two last bits pinned, and refuses twenty-three malformed inputs (the same file).
- **Against Terluna's module**, in single scratch runs. On five pairs of Terluna's grids the lab's remap
  matrix, shared layers and a remapped field equal those of Terluna's module, run from a copy. With Terluna's
  doubles the lab's carrier turns Terluna's year-19 restart of `A28R_301k_cold` (sha256 `5a0f31f96382169a…`)
  into its carried fifteen-level restart byte for byte (`29343e47f9b681b9…`), each spectral field's column
  integrals within 3 × 10⁻¹⁴ of their size; with the lab's doubles the fields differ from Terluna's by at
  most 2 × 10⁻¹². There the clip moved the cloud cover's column sum by up to 0.010, against a typical 0.034,
  and the cloud water's by 2.0 × 10⁻⁷ against 4.3 × 10⁻⁷.
- **Terluna's runs** on its two sets are Terluna's (`climate/gcm/README.md` at `39c5ee04`, "Fourteen levels
  near the ground" and "Fifteen levels: a thin bottom layer"): its month trials cost 1.6 times a ten-level
  run's on fifteen levels; over two years each set moved the rain by time of day and the air near the ground;
  and its longwave correction fitted on ten levels left 6.4–8.8 W/m² by layer on the new sets. The lab has
  run none of them and has measured no set's effect on a climate.

**Limits.**

- The heights are the study's. Terluna's come from its CM1 boxes of the Open Moon; the lab has none for any
  other world, and no rule here chooses heights from a scale height alone.
- A set counted at `"scenario"` needs a stated reference temperature; a scenario whose temperature the
  fixpoint is to find states its scale height in metres.
- One scale height converts every height, so a run's levels stand off the stated heights by its own
  temperatures: on Terluna's sea box the fifteen's lowest level stands at 313 m, against 299 m at 51 km.
- The released half levels' doubles are those of gfortran's arithmetic at double precision on this machine,
  for ten levels. A build at single precision, or a compiler that fuses the formula's products and sums,
  computes other last bits, and the byte-for-byte test would show it.
- Each set takes its own calibrations: the longwave correction, the ledger's terms on its layers and the
  rain's births. The lab has fitted none on a generated set.
- Untested: a run past the tests' 96 steps on a generated set; a generated set with the gust, the similarity
  or the rain's drops switched on, and with the curved air's or the longwave's tables in the model; a set at
  T42 or above; ranks other than four; single precision; and a restart carried between two generated sets in
  the model, which the Python tests alone cover. The Earth control's test of a generated set is ahead and
  waits for the author's word.

**Choices made in the port,** where the lab's form differs from Terluna's:

- a rule and a study's values in place of Terluna's three named sets, with Terluna's values for the Open Moon
  kept as a record;
- the released half levels in the compiled model's doubles, where Terluna's module computes them with numpy's
  powers and its sets differ from the model's own by a last bit at 0.3736 and 0.9666;
- the refusals at T42 and at five levels, where Terluna ran T21 alone;
- the calibrations by layer keyed to stated half levels and refused elsewhere, where Terluna's runner also
  carried a ten-level correction and ledger onto a new set (`levels_product`); the lab lays or fits each on
  the run's own set;
- the carrier's horizontal sizes read from the restart's own `nrsp`, `nlat` and `nlon`, where Terluna's holds
  T21's 506 and 2,048, and a carried restart written to a new path alone;
- Terluna's command line, with its heights at 51 km, left there: the lab's runner will call the carrier.

## Settings that carry the Moon (no source change)

These go through ExoPlaSim's `configure` and namelists. Two of them avoid, by configuration, behaviour
that holds only on Earth; the defect or limitation stays in the released code for runs that leave them unset.

| Setting | Design value | Why |
|---|---|---|
| `fixedorbit=True` (`NFIXORB=1`) | | With the default, PlaSim replaces the configured obliquity and eccentricity with Berger's orbit of the Earth for its start year (1 AD: 23.695°, 0.0175). Avoidance by configuration |
| `runsteps` | 17,160 (12 model days of 1,430 half-hour steps) | Whole model days per year, so the ten output means of each model day fall at the same places every year. Under the synodic clock the Sun shifts 3.2° a model day against those means (12.1 lunar days in a model year), so day–night analyses sort the output by the Sun's position (corrected 2026-10-17; the earlier text said the means stay aligned with the Sun, which held under PlaSim's own clock). Avoidance by configuration |
| `CONVDAY`, `NSUNCLOCK` | 86,400 s, 2 | Patches 03 and 04 |
| `rotationperiod`, `synchronous` | 27.32166 d, False | The Moon turns once a sidereal month against the stars; the Sun's day follows from the year |
| `year`, `eccentricity`, `obliquity` | 365.25636 d, 0.016715, 1.5424° | The Earth–Moon system's orbit of the Sun; the lunar equator's tilt to the ecliptic |
| `radius`, `gravity` | 1,737.4 km, GM/R² = 1.62422 m/s² | ExoPlaSim takes the radius in Earth radii and multiplies by 6,371,220 m for the model and its postprocessor; Terluna's runner divided by 6,371,000 m, so PlaSim's `PLARAD` is 1,737,460 m, 60 m (0.0035%) long |
| Air | 121,590 Pa at the water level; O2 21,227 Pa, Ar/N2 as Earth's, CO2 400 ppm (`GASCON` 288.38) | Terluna's design air |
| Sunlight | TSIS-1 HSRS times the shield's transmission, a 5,772 K tail past the measured spectrum, times the sunlight scale (0.970 for the design case: `GSOL0` 1,198.2 W/m²) | Sets the total and the split between PlaSim's two solar bands |
| Surface | T21, 10 levels; 50 m slab ocean with sea ice; land albedo 0.2 (placeholder); `ozone=False` | The design case ran on the released ten levels; Terluna's later design runs take its fifteen ("Level sets", above) |

## The design case

[design_case/](design_case/) holds the namelists of `A28_corrected_970` (the design case since
2026-10-14: patches 01–08, the curved air and the gas bands on, 295.0 K over years 10–19) and of
`A28_corrected_970_lw_ice` (the same with patches 09 and 10 switched on, settling near 307 K), with
the `twilight.dat` and `lwcorr.dat` tables those runs read.

`twilight.dat` holds, in order: the number of solar elevations; for each elevation (degrees) the
sunlight added to the ground and to each layer, top first, per unit sunlight at the beam; the extra
infrared each layer and the ground lose to space (W/m²); the temperatures that infrared is given at.
`lwcorr.dat` holds three rows of 11 values, the extra escape over land and over sea (W/m², top layer
first, ground last) and the temperatures they are given at. Both were written by Terluna's runner from
`climate/results/gcm/twilight.json` and `longwave_A28_corrected_970_heating.json` at 186b294.

## Provenance of runs

[runs.json](runs.json) matches each Terluna GCM run to the state of this series it compiled, from the
source hashes the runner recorded: 32 runs reproduce a prefix of the series exactly (patches 01–02 for
the cloud-water bracket, 01–03 for the 28% seas and the dimming runs, 01–05 for the first corrected
design case, 01–08 for the current design case, 01–10 for the 307 K test). Two do not: `A_corrected_clouds`
compiled an uncommitted draft of patch 03 on 2026-09-25, whose committed form reproduces its first year
byte for byte (`regression_convday_on`), and `A28_dim5_moon_twilight` used a separate sunlight-only copy
of an early patch 07, stopped after four years. Eleven runs from before source hashing carry no record.
