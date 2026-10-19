# ExoPlaSim 3.4.2 for a breathable Moon

Eleven patches to PlaSim's radiation and cloud code inside ExoPlaSim 3.4.2, the first ten Terluna's and
the eleventh the world-crafting lab's, the settings that carry the Moon's orbit and calendar, and the
design case's namelists and input tables. Each patch adds a namelist switch whose default reproduces
ExoPlaSim as released, and patch 11's reproduces the build of patches 01–10. Correctness, limits and room for
improvement are in [../../notes/exoplasim.md](../../notes/exoplasim.md).

## Upstream pin

| | |
|---|---|
| Source | ExoPlaSim 3.4.2, source distribution from PyPI (`pip download exoplasim==3.4.2 --no-binary :all:`) |
| sha256 of `exoplasim-3.4.2.tar.gz` | `fae502a92f5997ffd18b0bb85b9f0f0677857c62c5d1293f605c9799026f64c2` |
| Licence | GNU GPL version 3 (`LICENSE.TXT` in the distribution); these patches are distributed under the same licence |
| Patched files | `exoplasim/plasim/src/radmod.f90`, `exoplasim/plasim/src/rainmod.f90` |

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
the copy deployed on 2026-10-17 byte for byte (`expected.sha256`); patch 11 follows them, and the whole
series gives `radmod.f90` `50e3df63c3d9872e…` (`expected-series.sha256`). The lab compiles each point of
the series as a build of its own (`lab/worldlab/builds.py`).

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
