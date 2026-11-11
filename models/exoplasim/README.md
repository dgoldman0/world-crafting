# ExoPlaSim 3.4.2 for a breathable Moon

Thirteen patches to PlaSim's radiation, cloud and surface-transfer code inside ExoPlaSim 3.4.2, the settings
that carry the Moon's orbit and calendar, and the design case's namelists and input tables. The first ten
patches are Terluna's and the eleventh the world-crafting lab's; the lab wrote the twelfth and thirteenth
from Terluna's later code. Each patch adds a namelist switch whose default reproduces ExoPlaSim as released,
and each of patches 11 to 13 at its default reproduces the build of the patches before it. Correctness, limits
and room for improvement are in [../../notes/exoplasim.md](../../notes/exoplasim.md).

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
the copy deployed on 2026-10-17 byte for byte (`expected.sha256`); patches 11 to 13 follow them, and the
whole series gives `radmod.f90` `50e3df63c3d9872e…`, as patch 11 left it, and `fluxmod.f90`
`6e6b0a1521d5cf97…` (`expected-series.sha256`). The lab compiles each point of the series as a build of its
own (`lab/worldlab/builds.py`).

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

- **The patches apply.** `models/check_patches.sh` applies the series of thirteen to the pinned archive and finds
  the sources of `expected-series.sha256`. On 11 November 2026 the routines of the patched `fluxmod.f90`, from
  `gustnl` through `simwcol`, differed from those of Terluna's deployed copy (`exoplasim-twilight` on its research
  drive) in comment lines and the two viscosity lines alone.
- **They compile.** The lab's builds at patches 01–12 and at the whole series compile PlaSim at T21 on ten levels
  (`lab/tests/test_builds.py`), and the patched `fluxmod.f90` compiles with PlaSim's module on fifteen levels
  (`python/climate/tests/test_surface_gust.py`, `test_surface_similarity.py`).
- **Identity at the defaults.** On Earth's control over 96 steps on four ranks, the build of patches 01–12 gives
  PlaSim's output and restart byte for byte as the build of patches 01–11 from the same folder, and so does the
  whole series with `NGUST` 0 and `NSIMW` 0; with the gust on, the whole series with `NSIMW` at its default gives
  the output of the build of patches 01–12 (`lab/tests/test_builds.py`). In a harness of `surflx` alone, each patch
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
| Surface | T21, 10 levels; 50 m slab ocean with sea ice; land albedo 0.2 (placeholder); `ozone=False` | |

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
