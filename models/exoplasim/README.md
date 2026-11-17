# ExoPlaSim 3.4.2 for a breathable Moon

Twenty patches to PlaSim's radiation, cloud, surface-transfer, rain, convection and output code inside ExoPlaSim
3.4.2, the settings that carry the Moon's orbit and calendar, the level set generated for a world, which takes no
patch, and the design case's namelists and input tables. The first
ten patches are Terluna's and the eleventh the world-crafting lab's; the lab wrote the twelfth to the twentieth
from Terluna's later code. Each patch adds a namelist switch, patch 14 a third value of PlaSim's own
`NEVAPPREC` and patch 18 a second value of its own `NPRC`, whose defaults reproduce ExoPlaSim as released, and each
of patches 11 to 20 at its default reproduces the build of the patches before it. Correctness, limits and room for improvement are in
[../../notes/exoplasim.md](../../notes/exoplasim.md).

## Upstream pin

| | |
|---|---|
| Source | ExoPlaSim 3.4.2, source distribution from PyPI (`pip download exoplasim==3.4.2 --no-binary :all:`) |
| sha256 of `exoplasim-3.4.2.tar.gz` | `fae502a92f5997ffd18b0bb85b9f0f0677857c62c5d1293f605c9799026f64c2` |
| Licence | GNU GPL version 3 (`LICENSE.TXT` in the distribution); these patches are distributed under the same licence |
| Patched files | `exoplasim/plasim/src/radmod.f90`, `rainmod.f90`, `fluxmod.f90`, `plasimmod.f90` and `outmod.f90` |

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
the copy deployed on 2026-10-17 byte for byte (`expected.sha256`); patches 11 to 20 follow them, and the
whole series gives `radmod.f90` `3a90be4f7e3a4132…`, as patch 16 leaves it, `rainmod.f90` `f8462e2938c40275…`, as
patch 20 leaves it, and `fluxmod.f90` `8534f22f7d10a423…`, `plasimmod.f90` `811f37ee4d72cbfd…` and `outmod.f90`
`14a440b6dcf11b38…`, as patch 17 leaves them (`expected-series.sha256`). The lab compiles each point of the series as
a build of its own (`lab/worldlab/builds.py`).

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
| 15 | `twilight-clear-share` | `NTWLCLEAR` (radmod) | 0 | 1: takes patch 07's sunlight in each layer in the share of the sky clear of cloud above it, and lets each layer's and the ground's extra infrared through the cloud above at each layer's longwave transmissivity | Repair of patch 07's method, whose terms are clear-sky values; written by the lab from Terluna's code |
| 16 | `twilight-counted-once` | `NTWLZERO` (radmod) | 0 | 1: starts each pass of `swr` from zero where the Sun is down, so that with the clear-sky diagnostic on the twilight below the horizon is counted once | Repair of a defect in patch 07 (defect log C21); written by the lab from Terluna's code |
| 17 | `wind-at-10-m` | `NWIND10` (fluxmod) | 0 | 1: brings the lowest level's wind down to 10 m on Geleyn's profile through the lowest layer, from the drag `surflx` computes, and writes its means since the last output as codes 165 and 166 (`uas`, `vas`) | Diagnostic: the model's state stays as it was; written by the lab from Terluna's code |
| 18 | `betts-miller-convection` | `NPRC` 2, a second value of PlaSim's switch; `TAU_BM`, `RH_BM`, `EPS_BM`, `CIN_BM` (rainmod) | 1, Kuo's; 7,200 s, 0.7, 0, 0 J/kg | 2: Frierson's simplified Betts–Miller scheme in place of Kuo's: where a parcel lifted from the lowest level is buoyant, temperature and vapour relax over `TAU_BM` toward the parcel's temperature and `RH_BM` of its saturation, the rain is the vapour the column loses and one heating through the layers keeps the moist enthalpy; a column too dry to rain or held back by `CIN_BM` takes PlaSim's shallow scheme | Capability: a second deep convection, whose relaxation time and humidity are Earth's values (defect log B39, B42); written by the lab from Terluna's code |
| 19 | `betts-miller-depth-test` | `DSIGDEEP_BM`, `NSUB_BM` (rainmod) | 0, 1 | The cloud-depth test: deep convection only where the parcel's cloud, from the condensation level to the top, spans more than the share `DSIGDEEP_BM` of the column's surface pressure; and the parcel's mixing taken in `NSUB_BM` steps within each layer | Capability, its depth a share of the surface pressure where Terluna's is 200 hPa; written by the lab from Terluna's code |
| 20 | `betts-miller-shallow-cap` | `NSHCAP_BM` (rainmod) | 0 | 1, with the depth test: a column the scheme hands to the shallow scheme takes a top within the depth test's share above its condensation level, which `mkshallow` keeps in place of PlaSim's 700 hPa | General repair of an Earth value (B34) for the Betts–Miller scheme; written by the lab from Terluna's code |

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

- **The patch applies.** `models/check_patches.sh` applied the series of fourteen to the pinned archive and
  found the sources that `expected-series.sha256` then recorded.
- **It compiles.** The lab's build of patches 01–14 compiles PlaSim at T21 on ten levels
  (`lab/tests/test_builds.py`), and the patched `rainmod.f90` compiles with PlaSim's module on fifteen levels
  (`python/climate/tests/test_rain_drops.py`).
- **Identity at the default.** On Earth's control over 96 steps on four ranks, the build of patches 01–14 gives
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

## The twilight's clear share and its single count (patches 15 and 16)

Patches 15 and 16 add to `radmod.f90` two corrections of patch 07's twilight that Terluna made on `domain/climate`:
the terms in the clear share above each layer (`TWILIGHT_CLEAR_EDITS`, commit `b73fa088`, 19 October 2026) and
each pass of the shortwave started from zero where the Sun is down (`TWILIGHT_ZERO_EDITS`, `2762669e`, 8 November;
defect log C21), both in `climate/gcm/exoplasim_run.py` at `39c5ee04`. Terluna's runner applies them as edit lists
in its twilight copy of ExoPlaSim and switches both on in its runs, the clear share since 19 October and the zero
start since 8 November. The lab wrote them as two unified patches after patch 14, each behind its own switch and
under Terluna's name for it, so that patch 07 stays as Terluna deployed it on 2026-10-17 (`expected.sha256`). The
lab's writer sets them through `switches.twilight_clear_share` and `switches.twilight_counted_once`
(`lab/configs/exoplasim/defaults.toml`). The clear share is false by default, since each fix enters the lab opt-in,
and the single count true, since the double count lets a diagnostic change the run's state where the released
model's diagnostic leaves it alone (`PLAN.md`, "Decisions", 2026-11-16). It writes each switch where the run's
series holds its patch, resolves both off where the curved air's terms are off, a first run's among them, refuses
the clear share on a series without patch 15, and takes patch 07's passes on a series that stops before patch 16.

**What changes.** The ledger's terms are clear-sky values: the sunlight that the curved air adds to each layer and to
the ground, and the infrared that it lets out of each layer and the ground, computed on a cloudless column. Patch 07
adds each layer's sunlight in every column and the ground's in the share of the column clear of cloud, and lets out
the infrared in every column, cloudy or clear.

- With `NTWLCLEAR` 1, `twilight_term` takes each layer's sunlight in the share of the sky clear of cloud above that
  layer, the product of 1 − cover over the layers above it, by PlaSim's own random overlap (`zcs` in `swr`), as the
  ground already takes its own in the whole column's share. `lwr` records each layer's longwave transmissivity
  under its cloud, its own `ztaucc0` with patch 10's ice optics where `NICEOPT` 1, in `twltau`, and `twilight_lw`
  lets each layer's escape and the ground's through the cloud above at the product of those transmissivities.
- With `NTWLZERO` 1, `swr` sets `dfu`, `dfd` and `dswfl` to zero where the Sun is down before `twilight_term` adds
  to them. `radstep` sets the fluxes to zero once and, with the clear-sky diagnostic on (`NDIAGCF` 1), calls `swr`
  twice, first without cloud and then with it. `swr` writes the fluxes only where the Sun stands above the horizon
  (`losun`), and `twilight_term` adds the curved air's sunlight wherever the Sun's elevation lies in its table,
  down to 40° below the horizon. Below the horizon the all-sky pass therefore keeps the clear pass's twilight and
  adds its own: under cover c the ground takes T(2 − c) of the clear twilight T, where T(1 − c) is meant, and each
  layer its clear term beside its own. Where the Sun is up, `swr` writes every level in each pass, so those columns
  stay as they were; the diagnostic's own clear-sky fluxes, read after the clear pass, stay as they were too, and
  the longwave needs no such start, since `lwr` sets its fluxes to zero at each call.

Neither patch holds a value of the Moon's. The clear share reads the run's own cloud cover and longwave
transmissivity at each step, and the zero start reads where the Sun is up; the terms come from the world's own
ledger, as before (`lab/design/terluna_fixes.md`, row 10). The ledger itself is unchanged, and
`python/climate/gcm/twilight.py` keeps computing clear-sky terms, which the model now takes in the clear share.

**Verification.** The evidence states are those of the notes: none of them validates a climate.

- **The patches apply.** `models/check_patches.sh` applies the series to the pinned archive and finds the sources
  of `expected-series.sha256`.
- **They compile.** The lab's builds of patches 01–15 and of the whole series compile PlaSim at T21 on ten levels,
  and the whole series compiles on fifteen (`lab/tests/test_builds.py`).
- **Identity at the defaults.** On Earth's control over 96 steps on four ranks, with the released model's values
  stated as calibrations and the Open Moon's ledger for the curved air's terms, the folders written for the builds
  of patches 01–14, 01–15 and 01–16 differ in the two entries alone and give the same output and restart, each under
  its own build, with the curved air's terms on and off and with the clear-sky diagnostic on and off; the folder
  that names neither entry gives them under the build of patches 01–16 too (`lab/tests/test_builds.py`). In a harness
  of `twilight_term`, `twilight_lw` and the end of `swr`, taken from the series and compiled with ExoPlaSim's flags
  under a stand-in for `radstep`'s passes, the patched routines at their defaults print every digit that patch 07's
  print (`python/climate/tests/test_twilight_patches.py`). Compiled with `-O3 -march=native`, where the compiler
  fuses products and sums, they agree with patch 07's within a few units of the last place: there a factor of 1 can
  change which product a sum takes unrounded. The lab's builds compile with ExoPlaSim's flags.
- **The switches' effect, in the whole model.** On that control with the twilight on, `NTWLZERO` 1 changes nothing
  without the diagnostic, where `swr` runs once a step. With the diagnostic, patch 07's passes end the run in another
  state than the run without it, and with `NTWLZERO` 1 the run ends in that run's state byte for byte, with the
  clear share and without it. With the twilight off, the diagnostic leaves the run's state as it was. The clear share
  changes the output and the state (`lab/tests/test_builds.py`).
- **The switches' effect, against arithmetic.** In the harness, with the diagnostic on, patch 07's passes give each
  night column under clear sky exactly twice the twilight of one pass and, under cover c, T(2 − c) of the clear
  twilight on the ground where one pass gives T(1 − c); with `NTWLZERO` 1 the two passes print every digit of one.
  With `NTWLCLEAR` 1 each layer's sunlight and each layer's and the ground's escape follow the arithmetic written out
  in the test, the clear sky above by random overlap and the product of the transmissivities above, to 10⁻¹²; under
  an opaque layer the layers below it and the ground take no twilight sunlight.
- **Wrong code at eight places.** In a single scratch run on 16 November 2026, eight wrong statements put one at a
  time into the two patches each failed the harness's tests: the zero start on the sunlit columns, never taken, or
  leaving `dswfl`; the clear share counting the layer's own cover, kept with the switch at 0, or left off a layer's
  sunlight; and the longwave share counting the layer's own cloud or left off the ground's escape.
- **Agreement with Terluna's code.** The statements of `twilight_term`, `twilight_lw` and the end of `swr`, and the
  line in `lwr` that records the transmissivities, equal those of Terluna's deployed `radmod.f90` (`exoplasim-twilight`
  on its research drive, sha256 `14b6e9ac17849cfd…`, read on 16 November 2026), comments aside.
- **Terluna's runs**, made with its own edits (Terluna's `climate/gcm/README.md` at `39c5ee04`, "The terms in the
  clear share", "Each sunlight pass from zero where the Sun is down" and "The design years (20 October)"). On ten
  levels, a twin of the 301 K branch without the clear share (`A28R_301k_s0894_noclear`) settled near 301.9 K where
  the branch with it settled near 301.0 K, so the clear share cooled that climate by about 1 K; both runs had the
  clear-sky diagnostic on and carried the double count, so that at night the clear share acted on one of the two
  counts. Over the years 10–49 of the turned design run, on fifteen levels, the double count added 2.70 W/m² at the
  top of the air in the global mean, 1.5% of the 178.2 W/m² absorbed, rising from 1.7 W/m² at the equator to
  17.7 W/m² at 85.8°, all on the night side, and the search for the design temperature took it into the sunlight
  scale, 0.924 where about 0.938 holds without it. The lab has run none of these and has measured neither switch's
  effect on a climate.
- **Physical validation** remains to be done. The lab's runs with either switch are the tests' own, of two days,
  on Earth's control with the Open Moon's ledger.

**Limits.**

- The clear share takes the twilight that the cloud above a layer intercepts out of the budget: the cloud neither
  absorbs nor reflects it. A layer's own cloud leaves its own term whole, the cover overlaps at random, and the
  infrared passes the cloud at PlaSim's transmissivity for diffuse light, where the curved air's escape leaves
  along slant paths.
- The ledger's ground term is the sunlight absorbed over ground of albedo 0.1 (`SKY_ALBEDO` in `twilight.py`),
  whatever the run's ground: by Terluna's record that puts 11% too much of the term into land and 3% too little into
  the sea of its turned design run, and 1.5–4.5 times too much into snow or sea ice. A ledger solved at several
  ground albedos would correct it.
- At the writer's defaults a run with the twilight and the clear-sky diagnostic, as `exoplasim/defaults` has it,
  counts the night's twilight twice, as every Terluna run with the twilight before 8 November did.
- Untested anywhere: a run past the tests' 96 steps; a run restarted with either switch on, though the patches keep
  nothing between steps that the next step reads; a ledger on a level set other than the released ten, which the
  lab has yet to compute; ranks other than four; and PlaSim compiled in single precision.

**Choices made in the port,** where the lab's form differs from Terluna's or the design left it open:

- two patches, one for each switch, in the order Terluna made them, so that each point of the series adds one
  capability with its own identity test; Terluna's runner applies the clear share before its ice weights and cold
  cloud's factors and the zero start after them, where the lab's patch 11 precedes both;
- after patch 14, where the paper's defect log has the zero start ported into patch 07, which the lab keeps as
  Terluna deployed it;
- Terluna's statements, in which the clear share is a factor of exactly 1 with the switch at 0, which leaves every
  product as it was under ExoPlaSim's flags. A form that kept patch 07's statements on a branch of their own was
  tried in a scratch build and also moved the last bits under `-march=native`, so it gained nothing;
- the clear share off by default and the single count on, where Terluna's runner switches both on for every run
  with the twilight, and both resolved off with the twilight, where they would change nothing.

## The wind at 10 m (patch 17)

Patch 17 gives PlaSim the wind at 10 m that Terluna added on 19 October 2026 (`WIND10_PATCHES` in
`climate/gcm/exoplasim_run.py` on `domain/climate`, commit `4318bf67`, its statements unchanged at `39c5ee04`).
Terluna's runner applies it as three edit lists in its twilight copy of ExoPlaSim under `--wind10`. The lab wrote it
as one unified patch after patch 16, behind Terluna's switch `NWIND10` in fluxmod's namelist, 0 by default. The lab's
writer sets it through `switches.wind_10m` (`lab/configs/exoplasim/defaults.toml`), true by default, since a
diagnostic that changes no state leaves the Earth control's test nothing to gate (`PLAN.md`, "Decisions",
2026-11-16); it writes `NWIND10` where the run's series holds the patch, in a first run as in any other, and a run on
a series that stops before the patch writes no wind at 10 m.

**What PlaSim writes near the ground.** The released PlaSim writes no wind below its lowest full level. ExoPlaSim's
postprocessor names codes 165 and 166 `uas` and `vas`, the eastward and northward wind at 10 m (`pyburn.py`), and
`outmod.f90` writes neither code; the postprocessor marks a requested code that the raw output lacks for derivation,
holds no derivation for these two, and so leaves both names out of the file without an error (Terluna's
`climate/gcm/README.md` at `39c5ee04`, "The surface stress and the 10 m wind in the output"). The nearest wind in
the output is the lowest full level's, in the spectral vorticity and divergence (codes 138 and 155) from which the
postprocessor derives `ua` and `va`. Since the released levels are fixed in σ, that level's height in metres
follows the world's scale height: about 0.15 km on Earth's ten levels, 0.9 km in the Open Moon's air and 0.3 km on
Terluna's fifteen. Beside it the output holds the surface stress (codes 180 and 181, means over the interval), u*³
(159), the roughness (173) and the 2 m temperature (167), which is the lowest level's virtual potential temperature
at the ground's pressure. A near-surface wind read from the released output is therefore the wind at the lowest
level's height; Terluna's lake studies brought that wind down a neutral log profile from about 0.9 km, which takes
the lunar air near the ground as neutral (the same section of Terluna's record).

**What changes.** With `NWIND10` 1, `surflx`, once it has computed each column's transfer, takes the lowest level's
wind u_L at height z_L down Geleyn's (1988) profile through the lowest layer:

    u(z) = u_L [ln(1 + z/z0) − (z/z_L)(B_N − B_D)] / B_D,   B_N = ln(1 + z_L/z0),   B_D = κ/√C_D

C_D = C_N f_m is the drag coefficient of `dtransm` against the wind of the bulk formulas: C_N = (κ/ln(1 + z_L/z0_P))²
is PlaSim's neutral coefficient on its own roughness z0_P (`dz0`) and f_m its stability factor for momentum
(`zrifm`), so that B_D = ln(1 + z_L/z0_P)/√f_m. The profile reaches u_L at z_L, and near the ground it is the log law
of the friction velocity √C_D u_L; neutral air takes the log law throughout, stable air brings less of the wind down
and unstable air more, and the factor on u_L is held between 0 and 1. The drag is whichever the surface transfer
computed at that step: Louis's factors under PlaSim's wind with its least value of 1 m/s, the same factors under
Beljaars's gust (`NGUST` 1), and over ice-free water with `NSIMW` 1 the similarity's transfer velocity u*²/U, for
which B_D = κU/u*. The roughness z0 in the log and in B_N is that drag's: PlaSim's `dz0`, and under the similarity
over ice-free water the similarity's own, as `simwcol` finds it before carrying it to the next step. `outaccu` sums
the wind at each step, `outgp` divides the sums by the steps counted since the last output and writes them as codes
165 and 166 after the 2 m temperature on the mean output's unit, and `outreset` starts the sums again. The wind and
its sums sit in PlaSim's module beside its other accumulators and stay outside the restart, so the model's state,
and with it the restart, stays as it was.

**The world's values and Earth's.**

| Quantity | Its value in the patched code |
|---|---|
| The lowest level's height z_L | The model's own, computed by `surflx` from that level's temperature, `gascon` and `ga` |
| The drag's neutral coefficient and stability factor | Those `surflx` computes at the step: Louis's factors of the bulk Richardson number, which takes `ga`, with ECHAM's constants of 5 (`vdiff_b`, `vdiff_c`, `vdiff_d`), fitted on Earth; under patches 12 and 13, their transfer (above) |
| The roughness | PlaSim's own: over the sea Charnock's 0.018 u*²/g from the model's stress and gravity, at least 1.5 × 10⁻⁵ m (`seamod.f90`), 10⁻³ m over sea ice, and over land 2 m or the surface file's (`landmod.f90`), each constant Earth's (defect log B41); under the similarity, its own, with the Earth values listed for patch 13 |
| The height of 10 m | The convention of codes 165 and 166: the height of the surface stations' anemometers on Earth (WMO), at which bulk flux formulas and wave models, SWAN among them, take their wind |
| The profile | Geleyn's interpolation through a layer of constant flux, faithful where the lowest level stands in the surface layer ("Limits") |

**Verification.** The evidence states are those of the notes: none of them validates a climate.

- **The patch applies.** `models/check_patches.sh` applies the series of seventeen to the pinned archive, now with
  `plasimmod.f90` and `outmod.f90` among the files it takes out, and finds the sources of `expected-series.sha256`.
- **It compiles.** The lab's build of the whole series compiles PlaSim at T21 on ten levels and on fifteen
  (`lab/tests/test_builds.py`), and the patched `plasimmod.f90` and `fluxmod.f90` compile with PlaSim's module on
  fifteen levels (`python/climate/tests/test_wind_10m.py`).
- **Identity at the default, and a diagnostic with the switch on.** On Earth's control over 96 steps on four ranks,
  the folder written for the build of patches 01–16 gives the same output and restart under the build of patches
  01–17, and so does the folder written for that build with `NWIND10` 0. With `NWIND10` 1 the run ends in the same
  restart byte for byte, under PlaSim's own transfer and under the gust with the similarity over water, and its
  output holds every record of the run without the switch, byte for byte and in order, with codes 165 and 166 after
  each 2 m temperature at the same output time (`lab/tests/test_builds.py`). In a harness of `surflx` taken from the
  series and compiled against a stub of PlaSim's module, the transfer, the 2 m temperature and the similarity's
  carried state print the same digits as the series before patch 17 prints, with the switch at 0 and at 1, under
  ExoPlaSim's flags and under `-O3 -march=native`.
- **The wind against its formula.** In that harness `surflx` gives the wind of the Python copy written in the test
  to 10⁻¹⁰ on lunar columns on fifteen and forty levels and Earth-like columns on ten, under PlaSim's transfer, the
  gust, and the gust with the similarity from fresh and settled states, over sea, land and sea ice. The copy itself
  gives the log law in neutral air, the lowest level's wind at its height, the log law of √C_D u_L near the ground,
  and Terluna's recorded factors at 885 m over a roughness of 0.1 mm: 0.72 in neutral air, 0.51 and 0.88 at stability
  factors of 0.5 and 1.5. On one column in σ the lowest level stands 6.04 times higher at the Moon's gravity than at
  Earth's and the factor falls; with the similarity settled in neutral air, the wind follows the similarity's own log
  law.
- **Wrong code at fifteen places.** In a single scratch run on 16 November 2026, fifteen wrong statements put one at
  a time into the patch each failed the harness's tests: the stability factor without its square root, PlaSim's
  roughness where the similarity's belongs, at either of two places, the similarity's roughness taken over sea ice or
  left out, the sign of the linear term, the cap at 1 dropped, the two components exchanged at either place, the
  broadcast dropped, the zonal mean left undivided, the meridional sum fed with the zonal wind, the count left
  running past an output, the meridional mean written under code 165, and the switch on by default. The wrong
  meridional sum passed the first round of the tests, and the test of the output's lines, which now pins both sums,
  catches it.
- **Agreement with Terluna's code.** The patch's lines in `plasimmod.f90` and `outmod.f90` equal those of Terluna's
  deployed sources (`exoplasim-twilight` on its research drive, sha256 `4f73e21fe3980fe2…` and `1b105606c36ebf73…`,
  read on 16 November 2026), comments aside. In `surflx`, where the roughness is PlaSim's own, the lines compute what
  Terluna's deployed `fluxmod.f90` (`0eadda0bb213cf83…`) computes, operation for operation, in a loop of their own
  after the transfer's; under the similarity over ice-free water they take its roughness ("Choices made in the
  port"). In a single scratch run on 16 November 2026, the harness compiled with Terluna's three lines in place of
  the lab's printed every digit of the lab's wind on every column off the similarity's ice-free water, under
  ExoPlaSim's flags and under `-O3 -march=native`.
- **Terluna's runs**, made with its own edits (Terluna's `climate/gcm/README.md` at `39c5ee04`). A one-year smoke run
  on the 301 K design case's surface wrote both codes (commit `4318bf67`). Over a month from one restart, the
  fifteen-level run's wind at 10 m averaged 1.24 m/s against 1.17 m/s on fourteen levels, whose lowest level stands
  three times as high, and over two years 1.28 against 1.19 m/s. The lab has run neither comparison.
- **Physical validation** remains to be done: no wind at 10 m from a cloud-resolving box or an observation has been
  set beside the patch's.

**Limits.**

- Geleyn derived the profile for a layer of constant flux, so it is faithful where the lowest level stands in the
  surface layer, the lowest tenth of the boundary layer: the level near 0.15 km on Earth's ten levels needs a layer
  1.5 km deep, the level near 0.3 km on Terluna's lunar fifteen one of 3 km, and the level near 0.9 km on the Open
  Moon's released ten one of 9 km. Under shallower layers, stable nights among them, the profile interpolates between
  the drag at the ground and the wind at the lowest level; the registry's B31 warns where that level stands above
  345 m.
- The means are means of the components, so the speed of the mean wind understates the mean speed where the wind
  turns within an interval (Terluna's record).
- The sums stay outside the restart: a segment that starts between two outputs averages its first wind at 10 m over
  its own steps, while the other means also count the steps before the restart. The lab's output steps fill each
  model year with whole means (`derive.output_steps`), so a segment of whole years starts on an output.
- Over land, under PlaSim's preset roughness of 2 m, 10 m stands five roughness lengths above the ground, where
  profiles over tall vegetation take a displacement height that the profile lacks.
- The snapshot and high-cadence files (`NSNAPSHOT`, `NHCADENCE`) carry no wind at 10 m.
- Untested anywhere: a run past the tests' 96 steps; a run restarted with the switch on; the similarity with
  `NGUST` 0, which the writer never sets; ranks other than four; and PlaSim compiled in single precision.

**Choices made in the port,** where the lab's form differs from Terluna's or the design left it open:

- one patch after patch 16, under Terluna's switch name and with its state in PlaSim's module, as Terluna's lists
  have them; the comments are the lab's;
- the wind computed in a loop of its own after the transfer's, where Terluna's lines stand inside the transfer's
  loop, so that the transfer's loop compiles from the same statements whatever the switch;
- under the similarity over ice-free water, the profile on the roughness of the drag the similarity sets, where
  Terluna's lines take PlaSim's `dz0` on every surface. The drag's B_D comes from the similarity's friction velocity
  on its own roughness, and a profile on PlaSim's roughness then runs its log on another roughness than the drag's.
  In neutral air the lab's wind follows the similarity's log law exactly, while on PlaSim's Charnock roughness the
  wind at 10 m comes out 5.4% stronger at 2 m/s on the Moon's fifteen levels and 6.8% on Earth's ten
  (`python/climate/tests/test_wind_10m.py`), and 0.3% and 0.5% stronger at 10 m/s (a scratch calculation of
  16 November 2026 on the same columns). Terluna's runs whose commands its README lists with `--wind10` and
  `--surface-gust beljaars_similarity` took the wind on PlaSim's roughness;
- the setting on by default, since the patch changes no state; a run on a build before patch 17 writes none.

## Simplified Betts–Miller convection (patches 18 to 20)

Patches 18 to 20 add to `rainmod.f90` the simplified Betts–Miller scheme of Frierson (2007, J. Atmos. Sci. 64,
1959–1976) that Terluna wrote from 21 October 2026, in the form its design runs compiled and set: the scheme itself
(`SBM_EDITS`, `SBM_CODE`), its cloud-depth test with the mixing within layers (`SBM_DEPTH_EDITS`) and its shallow cap
(`SBM_CAP_EDITS`), all in `climate/gcm/exoplasim_run.py` on `domain/climate` at `39c5ee04`, unchanged since. Terluna's
runner applies them as edit lists to its twilight copy of ExoPlaSim; the lab wrote them as three unified patches, one
for each list, behind PlaSim's own switch `NPRC`, whose released default, 1, keeps Kuo's scheme. Terluna's design run
`A28R_301k_design_l15_snow_s934` sets `NPRC` 2, `TAU_BM` 7,200 s, `RH_BM` 0.7, `EPS_BM` and `CIN_BM` 0, `DPDEEP_BM`
20,000 Pa and `NSHCAP_BM` 1 in its `rainmod_namelist`, beside rain evaporated from its drops (`NEVAPPREC` 2). The lab's
writer sets the scheme through `switches.convection` (`lab/configs/exoplasim/defaults.toml`): `kuo`, the default under
the opt-in rule for each port (`PLAN.md`), and `betts_miller`, with the settings of `[betts_miller]`, whose defaults
are the design scheme's. It writes `NPRC` where the run's series holds patch 18 and each of the scheme's entries where
the series holds the patch that reads it, refuses the scheme on a series without patch 18, and refuses a setting away
from its patch's default on a series without that patch. Which scheme the Open Moon's runs take is block 3's decision
(`PLAN.md`).

**What Terluna's design build compiled.** The design run's record names its `rainmod.f90` by the hash
`b55e297f48e3a268`, the source of a test build of the same run that Terluna's research drive keeps
(`gcm-runs/A28R_301k_design_l15_snow_s934_weather_test/build/plasim/src/rainmod.f90`), and the design executable
carries that source's namelist entries. Beside the three edit lists, its `mksbm` holds the CAPE trigger (`cape_bm`,
`epst_bm`) and the night switch (`ndiagnight_bm`), both compiled in at their defaults of 0, which the design run leaves
unset and which keep them off; Terluna's `DIAGNOSTIC_PATCHES` line that completes PlaSim's diagnostic 16; and a call of
`mkdqtgp` for every `NPRC` from 1. The trigger, the night switch and the closures (closure (c), the two redesigns and
route L), none of which passed Terluna's agreement test, stay in Terluna; the design build compiled no closure. The
same source holds Terluna's mass-flux scheme (`NPRC` 3), which the design run leaves unused and which stays in
Terluna.

**PlaSim's own Betts–Miller scheme.** The pinned archive also ships `rainmod_bm.f90`, PlaSim's rainmod of 2002, with
the full Betts–Miller scheme in Betts's saturation-point form (`mkbm`): a deep threshold at 700 hPa, saturation-point
differences in Pa, and relaxation times of 2 h for deep and 4 h for shallow convection, Earth's values. ExoPlaSim
compiles `rainmod.f90` (`RAINMOD=rainmod` in `make_plasim`), and `rainmod_bm.f90` predates the parts of that file on
which ExoPlaSim and this series build, so the patches add Frierson's scheme to the rainmod that ExoPlaSim compiles.

**What changes.** With `NPRC` 2, `rainstep` calls `mksbm` in place of `kuo`, on each column's state after the step's
tendencies so far.

- **The reference.** A parcel from the lowest level, lifted dry adiabatically across each layer and condensed to
  PlaSim's saturation in two Newton steps, as Kuo's parcel is, with the latent heat of sublimation below freezing,
  gives the reference temperature T_ref from the lowest level up. With `EPS_BM` above 0 it mixes in the share
  1 − exp(−ε ln(p_below/p)) of each layer's air. The reference vapour q_ref is `RH_BM` of saturation at T_ref.
- **Where the column convects.** The parcel's level of free convection is the lowest level above its start at which
  it is warmer than the air, and its top the last level above that through which it stays warmer. Its inhibition is
  R Σ max(0, T − T_ref) Δσ/σ over the levels below its level of free convection.
- **The relaxation.** From the top to the lowest level, dT/dt = (T_ref − T)/τ + ΔT and dq/dt = (q_ref − q)/τ, with τ
  `TAU_BM` and at least `deltsec2`. The rain P is the vapour the column loses, −Σ (dq/dt) m, over the layers' masses
  m = p_s Δσ/g, and the one heating ΔT added at every convecting level releases its latent heat, Σ c_p (dT/dt) m = L P,
  so that the column keeps its moist enthalpy Σ (c_p T + L q) m. The rain forms at each level in proportion to the
  vapour removed there (`dprcl`), and the levels that lose vapour become the convective cloud layers (`icclev`,
  `icctot`), the top one an anvil's where it stands above σ 0.4, as under Kuo's scheme.
- **The shallow scheme.** A column whose relaxation would remove no vapour (P ≤ 0), whose parcel's inhibition exceeds
  `CIN_BM` J/kg where that limit is set, or whose top's pressure exceeds PlaSim's `pdeep` takes PlaSim's shallow
  scheme (`mkshallow`) from the lowest level to the parcel's top; it mixes temperature and vapour through those layers
  and forms no rain, as under Kuo's scheme.
- **The depth test** (patch 19, `DSIGDEEP_BM` above 0). A column convects deep only where the parcel's cloud, from the
  condensation level of the lowest level's air, found by 24 halvings of the interval in log pressure, to the top, spans
  more than the share `DSIGDEEP_BM` of the column's surface pressure; a thinner cloud takes the shallow scheme. The rule
  is the IFS's, which separates deep from shallow convection at 200 hPa on Earth (documentation Cy36r1, Part IV,
  section 6.4).
- **The mixing within layers** (patch 19, `NSUB_BM` above 1 with `EPS_BM` above 0). The parcel crosses each layer in
  `NSUB_BM` equal steps of log pressure, each lifting it dry adiabatically, mixing in its share of the air interpolated
  linearly in log pressure, and condensing the mixture.
- **The shallow cap** (patch 20, `NSHCAP_BM` 1, with the depth test). A column the scheme hands to the shallow scheme
  after the depth test, too dry to rain or held back, takes as its top the highest level at or below the parcel's top
  whose pressure is at least its condensation level's less the depth test's share of the surface pressure, and
  `mkshallow` keeps that top in place of its own, the lowest level above `pdeepth`, 700 hPa (defect log B34). A cloud the depth
  test hands over already lies within the share and keeps its parcel's top, so the cap lowers every top it sets.

**How the rain and the cloud reach the rest of PlaSim.** `mksbm` writes the rain by level and the convective cloud
layers into the variables Kuo's scheme writes, and `mkrain` and `mkclouds` take them unchanged. `mkrain` adds each
level's rain to the convective rain falling there and turns it to snow where the air is at or below freezing; with
patch 14 (`NEVAPPREC` 2) each level's rain enters the falling rain at that level as new drops by the run's birth rule
and evaporates from its drops below it, the configuration of Terluna's design run. `mkclouds`, the same routine in
the lab's series as in Terluna's design build, draws the convective cover from the convective rain at the ground over
the layers in `icclev`. The scheme also sets Kuo's diagnostics 8, 16 and 18, the heating and the vapour by layer that
the convection adds and the dynamics' vapour, read with `NDIAGGP` 1, and `rainstep` calls `mkdqtgp` for `NPRC` 2 as
for 1, so that diagnostic 18 holds the step's own tendency.

**The world's values and Earth's.**

| Quantity | Its value in the patched code |
|---|---|
| Gravity, the levels, each column's surface pressure, the gas constant, κ, the heat capacities, the latent heats and the saturation curve | The model's own: `ga`, `sigma`, `dsigma`, `dp`, `gascon`, `akap`, `acpd`, `ADV`, `ALV`, `ALS`, `ra1`, `ra2`, `ra4`, `TMELT` and `rdbrv` |
| The relaxation time, `TAU_BM` | 7,200 s by default, Frierson's 2 h for Earth (defect log B39). The lab's writer keeps it, or with `relaxation_s = "similarity"` takes 7,200 s times (H/c)/(H/c)_ref at the scenario's reference temperature from Earth's gravity and the Earth control's air at 288 K (`[betts_miller.reference]`; `lab/design/world_spec.md`, rule 9): 12.25 h for the Open Moon at 295 K, 10.4 h for the waterworld seed and 2 h for the Earth control. Registry B39 warns where a run of the scheme keeps 7,200 s off Earth's gravity |
| The reference humidity, `RH_BM` | 0.7, Frierson's for Earth's tropics (defect log B42) |
| The depth test, `DSIGDEEP_BM` | A share of the column's surface pressure, 0 by default; the writer's default is the IFS's 200 hPa over Earth's 1013.25 hPa, 0.1974, 240 hPa at the Open Moon's 1,216 hPa, where Terluna's 200 hPa holds 16% of the column (defect log B42) |
| The shallow cap's depth | The depth test's share |
| PlaSim's `pdeep` | 999,999 Pa, an absolute pressure, idle at its default, as under Kuo's scheme |
| PlaSim's shallow scheme: its diffusivity `rkshallow`, 10 m²/s, and without the cap its top at `pdeepth`, 700 hPa | Earth's, as under Kuo's scheme; the top is defect log B34, which registry B34 warns of where a run of the scheme leaves the cap off away from Earth's surface pressure |
| The anvil's σ 0.4 | Kuo's, a share of the surface pressure |
| The condensation level's 24 halvings | Numerical: the base to 2⁻²⁴ of the interval in log pressure |

**Stops.** With `NPRC` 2 the run stops at its start, with PlaSim's abort message, on a `TAU_BM` of zero or less, an
`RH_BM` outside the range above 0 to 1, a negative `EPS_BM` or `CIN_BM`, a `DSIGDEEP_BM` outside 0 to below 1, an
`NSUB_BM` below 1, and `NSHCAP_BM` 1 without the depth test. Under `NPRC` 1 or 0 the scheme's settings are left
unread. The scheme stores nothing from one step to the next, so the restart file needs nothing from it.

**Verification.** The evidence states are those of the notes: none of them validates a climate.

- **The patches apply.** `models/check_patches.sh` applies the series of twenty to the pinned archive and finds the
  sources of `expected-series.sha256`.
- **They compile.** The lab's builds of patches 01–18, 01–19 and the whole series compile PlaSim at T21 on ten levels
  (`lab/tests/test_builds.py`), and the patched `rainmod.f90` compiles with PlaSim's module on fifteen levels
  (`python/climate/tests/test_betts_miller.py`).
- **Identity at the defaults.** On Earth's control over 96 steps on four ranks, the folder written for the build of
  patches 01–17, whose namelist names no `NPRC`, gives the same output and restart under the whole series' build, and
  so does the folder written for the whole series, which states `NPRC` 1. Under the scheme without its depth test and
  cap, the folder written for the build of patches 01–18 gives the same output and restart under the builds of
  patches 01–19 and 01–20, and with the depth test the folder written for the build of patches 01–19 gives the same
  under the whole series (`lab/tests/test_builds.py`). In a harness of `mksbm` and `mkshallow` alone, each patch at
  its defaults prints every digit the routine before it prints, under ExoPlaSim's flags and under `-O3
  -march=native`, and patch 20's `mkshallow` prints the released routine's digits under Kuo's scheme, under the
  scheme without the cap and with the cap but no depth test.
- **The scheme's effect, in the whole model.** In that control the scheme changes the output and the restart against
  Kuo's, and the depth test changes them again. At the writer's settings, the design scheme with its depth test and
  cap, the whole series runs two days from a cold start under the floating-point traps ExoPlaSim compiles with, with
  PlaSim's `gamma` and with the rain's drops: in both runs the convective rain at the ground (code 143) is finite and
  positive in every output mean, the drops change it and the state, and the cap changes the state.
- **Agreement with the Python copy.** `mksbm` from the patched source, compiled with ExoPlaSim's flags against a stub
  of PlaSim's module, gives the tendencies, the rain by level, the cloud layers and the tops handed to the shallow
  scheme of a Python copy of Frierson's scheme written in the test, to 10⁻¹⁰, on Earth-like columns on PlaSim's ten
  levels and lunar columns on Terluna's fifteen and on forty, at 1.2 and 0.5 bar: deep, thin, too dry to rain, held
  back and buoyant nowhere, with the parcel undiluted and mixing, at 2 h and at 12 h. Its diagnostics 8, 16 and 18
  hold the scheme's heating, its vapour in m/s of water and the dynamics' vapour, and a deep cloud topped above σ 0.4
  takes an anvil where one topped between σ 0.4 and 0.5 takes none.
- **Against arithmetic.** On deep columns at both gravities the vapour relaxes toward `RH_BM` of saturation at the
  copy's reference temperature over τ to 10⁻¹², the temperature toward the reference shifted by one heating at every
  convecting level, twice the time halves every tendency and the rain, and a time below `deltsec2` takes `deltsec2`.
  The rain equals the vapour the column loses to 10⁻¹², forms where the vapour is removed, and the column's moist
  enthalpy changes by under 10⁻¹² of the rain's latent heat. Each deep cloud turns shallow as the share passes its
  depth over its surface pressure, at 1.2 and 0.5 bar and at Earth's 1 atm, and a column whose parcel crosses colder
  air turns shallow as the inhibition limit falls below its inhibition, counted as the copy counts it. On clouds too dry to rain or held back the
  cap hands `mkshallow` the highest level within the share of the base, which `mkshallow` keeps, where without the cap
  it takes the parcel's top lowered to the lowest level above 700 hPa; a thin cloud keeps its parcel's top.
- **The scheme's rain through the drops.** `mksbm` and patch 14's `mkrain`, compiled into one program and called as
  `rainstep` calls them, on Earth's air and the Open Moon's: with `NEVAPPREC` 2 mkrain's tendencies and the
  precipitation at the ground are those of patch 14's Python copy given the scheme's rain by level, to 10⁻¹⁰; rain
  formed aloft evaporates below its levels, the column keeps its water to 10⁻¹⁰, and the drops evaporate another
  amount of the scheme's rain than `gamma` does.
- **Agreement with Terluna's code.** The statements of `mksbm` and `mkshallow` equal those of the design build's
  source, comments aside, but for the CAPE trigger and the night switch, which the lab leaves out, the depth's share,
  and the condition in `mkshallow` (choices below). Compiled into one program with the design build's two routines,
  read from Terluna's research drive under their pinned hash, the lab's routines print every digit Terluna's print in
  every tendency, rain, diagnostic, cloud layer and shallow top, at Earth's gravity and the Moon's and at four surface
  pressures, on deep, thin, dry, held-back and stable columns, under the design scheme, with the inhibition limit, with
  the mixing within layers, without the cap and without the depth test, the lab's share set so that it comes to
  20,000 Pa exactly at the column's surface pressure (`python/climate/tests/test_betts_miller.py`, which skips where the
  drive is absent).
- **Wrong code at fifteen places.** In single scratch runs on 17 November 2026, fourteen wrong statements put one at
  a time into the patches each failed the tests of `python/climate/tests/test_betts_miller.py`: the reference
  humidity left out, the closure's heating of the wrong sign, the rain without its Δσ, the depth taken on Earth's
  surface pressure in place of the column's, the condensation level taken from the level above the lowest, the cap at
  half the share, PlaSim's top dropped without the depth test, the mixing within layers weighted a step behind, the
  anvil below σ 0.5, diagnostic 16 left at minus the tendency, the inhibition without its weight, the relaxation time
  let below `deltsec2`, the depth taken to the level below the top, and the stop on the cap without the depth test
  dropped. The anvil's and the diagnostic's were caught at first by the comparison with Terluna's build alone; the
  tests added for them catch both with the research drive absent. A fifteenth, the inhibition counted from the level
  of free convection, changes nothing, since the parcel is warmer than the air there.
- **Terluna's runs**, made with its own edits on its runs' configurations (Terluna's `climate/gcm/README.md` at
  `39c5ee04`). On ten levels at the design climate's sunlight, the scheme at Frierson's settings settled at 299.6 K
  against Kuo's 298.4 K and rained 2.32 mm/day against 2.19; at the Near-side Sea it rained 1.45 mm/day from midnight
  to sunrise against Kuo's 2.93 and CM1's box's 0.17. Over two years the depth test at 200 hPa cut the sea's rain after
  midnight by a quarter, to 1.55 mm/day, and on fourteen levels the cap moved the global ground by under 0.05 K. On
  fifteen levels, with the gust, the similarity over water and the rain's drops, the scheme is the design climate's,
  301.0 K over years 10–49 of the turned design case (`PLAN.md`). No setting of the scheme matched CM1's rain by time
  of day at both of Terluna's sites. The lab has run none of these.
- **Physical validation** remains to be done. The lab's runs with the scheme are the tests' own, of two days on
  Earth's control.

**Limits.**

- The scheme relaxes the whole column, from the lowest level to the top, toward an undiluted parcel's temperature at
  the design settings; CM1's mixing updrafts hold the Moon's upper air 3.0–6.3 K below that adiabat (defect log B29),
  and Terluna's closures, which change the reference, passed none of its tests.
- One relaxation time, one reference humidity and one depth serve every column, each Earth's value at the defaults
  (defect log B39, B42); the similarity that scales the time is untested on the scheme.
- The parcel starts at the lowest level, whose height follows the level set, and the condensation level and the cap's
  top fall on the model's levels.
- The rain forms where the relaxation removes vapour and the heating spreads by one amount through the convecting
  levels, so the scheme has no plumes, downdrafts, cold pools or organization, and its rain follows the instability
  after a fixed delay (Terluna's record).
- Untested anywhere: a run past the tests' 96 steps; a restart with the scheme on, though it keeps nothing between
  steps; the mixing within layers and the inhibition limit in the whole model; a generated level set with the scheme in
  the whole model; ranks other than four; T42; and PlaSim compiled in single precision.

**Choices made in the port,** where the lab's form differs from Terluna's or the design left it open:

- three patches, one for each of Terluna's edit lists, so that each point of the series adds one capability with its
  own identity test;
- the depth test as a share of each column's surface pressure, the new entry `DSIGDEEP_BM`, in place of Terluna's
  `DPDEEP_BM` in Pa, as `PLAN.md` sets: 200 hPa is 16% of the Open Moon's 1,216 hPa and 40% at 0.5 bar
  (`lab/design/terluna_fixes.md`, row 12); the shallow cap holds to the same share. Where the share times the
  surface pressure equals Terluna's depth, the arithmetic is Terluna's;
- PlaSim's 700 hPa top kept wherever the scheme's cap has no depth to hold to, where Terluna's `mkshallow` drops it
  whenever `NPRC` is 2 and `NSHCAP_BM` 1, which with no depth test would leave the shallow tops at the parcel's top,
  unbounded; Terluna's runner refuses that combination, and the lab's patch stops on it as well;
- stops on settings out of range, where Terluna's patch checks none and its runner refuses them;
- `mkdqtgp` called for `NPRC` 1 and 2, where Terluna's patch calls it for any value from 1;
- diagnostic 16 completed as the design build completes it, by Terluna's `DIAGNOSTIC_PATCHES` line, so that it holds
  the vapour the convection adds, where Terluna's scheme patch alone leaves it at minus the tendency before the scheme;
- the CAPE trigger, the night switch and the closures left in Terluna;
- in the lab's writer, one setting of two values and a table of the seven settings at the design scheme's values,
  the relaxation time Frierson's 7,200 s by default, with the world's value by similarity as a stated option.

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
Earth's. Registry entry B31 warns where a run's lowest full level stands above 345 m at the scenario's
scale height (`exoplasim_lowest_level_m`): the Open Moon on the ten draws the warning, and on the fifteen, at
307 m, it falls silent. The threshold is provisional and of low confidence: it marks the tested range, 10% over
the highest such height run so far, the Open Moon's fifteen levels in Terluna's design runs, and it is to be
revisited when the automatic rule for the heights is designed (`PLAN.md`, "Decisions").

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
the `twilight.dat` and `lwcorr.dat` tables those runs read. Both ran the clear-sky diagnostic with the curved air's
terms, before Terluna's clear share and zero start, so the night's twilight counted twice in them (defect log C21),
as the lab's writer reproduces with patches 15 and 16 at their defaults.

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
