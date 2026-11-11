# CM1 r22 for a breathable Moon

Patches to CM1 release 22.0 that run it at lunar gravity under a 29.5-day Sun, forced from a GCM along
rings and in boxes, with optional terrain, the curved air's twilight and WRF-ELEC's electrified NSSL
microphysics; the Fortran written for the electrified build; and the build variants Terluna used.
Correctness, limits and room for improvement: [../../notes/cm1.md](../../notes/cm1.md) and
[../../notes/electrification.md](../../notes/electrification.md).

## Upstream pins

| Source | Pin | Licence |
|---|---|---|
| CM1 r22.0 (G. H. Bryan, NSF NCAR), `https://www2.mmm.ucar.edu/people/bryan/cm1/cm1r22.0.tar.gz` | sha256 `05f990bb79055873c49499c92d0ff447524a2795016a474447a7e87dd5a86226` | MIT-style, ©2026 UCAR (`README` in the archive) |
| WRF-ELEC, `github.com/MicroTed/wrf4-elec` at commit `e43041b000ebfd77c4a528f2ca3847746e839aa8`: `elec/module_mp_nssl_2mom_elec.F` | sha256 `9203693d…0ffc3`, 1,118,061 bytes | WRF public-domain notice |
| the same: `elec/module_discharge_msz.F` | sha256 `1cde4951…7c283`, 165,455 bytes | the same |
| the same: `elec/module_boxmgsetup.F` (source of `fortran/terluna_mlint2.F`) | sha256 `eca68827…1ac`, 264,072 bytes | the same |

## Building

From the `cm1r22.0` folder, apply the patches a build lists in [builds.json](builds.json), in order,
then compile with the gravity and the design air as preprocessor constants:

```sh
P=/path/to/world-crafting/models/cm1
patch -p1 < $P/patches/makefile-gnu-omp.patch                         # or makefile-gnu-mpi.patch
for p in $(cat $P/series-core); do patch -p1 < $P/$p; done
for p in $(cat $P/series-twilight); do patch -p1 < $P/$p; done        # build-specific series, if any
patch -p1 < $P/patches/makefile-omp-O3-march-native.patch            # optional; Terluna's OpenMP default
cd src && make TERLUNA="-DTERLUNA_G=1.6242188765608128 -DTERLUNA_CO2=4.000000e-04 -DTERLUNA_O2=0.174579"   # as Terluna's lunar builds
```

The electrified build first puts WRF-ELEC's files in place, `module_mp_nssl_2mom_elec.F` as
`src/module_mp_nssl_2mom.F` and `module_discharge_msz.F` as itself, copies `fortran/*.F` into `src/`, and
then applies `series-elec` after `series-core`. Without the macros the build defaults to g = 9.81,
400 ppm CO2 and Earth's O2.

## The patches

`var1`–`var20` are CM1's spare namelist reals (`&param8`); the patches give them meanings.

**Core** (`series-core`, every build)

| # | File | Switch | Change | Kind (the paper's classes) |
|---|---|---|---|---|
| 01 | constants.F | `TERLUNA_G` | Gravity of the dynamics | General repair |
| 02 | module_ra_etc.F | `TERLUNA_G` | Gravity in `module_model_constants`, from which RRTMG's own `grav` (absorber mass per layer, heating rates) and MYNN take theirs | General repair |
| 03 | getcape.F | `TERLUNA_G` | Gravity of the CAPE diagnostic | General repair |
| 04 | morrison.F | `TERLUNA_G` | Fall-speed coefficients and caps scaled by (g/9.81)^((b+1)/3); Stokes droplets with the host g | General repair (scaling law) |
| 05 | radiation_driver.F | `var19` > 1 | A solar day of `var19` s at `var17` W/m², hour angle from `var18`; on a domain `var16` m long the hour angle grows eastward along x; on a great circle tilted `var12`° each column takes its latitude and longitude | General repair; the lunar day, flux and hour angle are its settings |
| 06, 07 | module_ra_rrtmg_lw.F, _sw.F | `TERLUNA_CO2`, `TERLUNA_O2` | RRTMG's CO2 and O2 from the build; CH4, N2O, CFCs and O3 set to zero (unconditional) | General repair (CO2 and O2 as build parameters, set to the design air); setting (the other gases zeroed) |
| 08 | init_surface.F | `initsfc = 9` | Land and water segments along x from `terluna_surface.txt`; the slab soil's five layers 5–80 cm thick in place of 1–16 cm (unconditional) | Coupling (land and water from the GCM's surface); general repair (the soil, for long days) |
| 09 | solve1.F | `var14`, `var15` | Large-scale nudging weighted from zero at `var14` m to full at `var15` m | Coupling |
| 10–14 | param.F, base.F, input.F, adv_routines.F, adv.F | `var13` = 1, 2 | A large-scale vertical wind against height (1) or by column along x (2) through CM1's own large-scale vertical advection | Coupling |
| 15 | param.F | `var12` > 0 | On a tilted great-circle ring, the Coriolis parameter 2Ω sin(latitude) column by column, the beta plane kept on in two dimensions | Coupling |
| 16 | solve2.F | (beta plane on) | The beta plane's Coriolis acts on departures from the base-state wind, whose balancing pressure gradient is implied (unconditional for beta-plane runs) | Coupling (active on the tilted rings, where the beta plane stays on) |
| 17 | solve1.F | `var11` = 1 | Large-scale heating and moistening by local time and height from `terluna_lsadv.txt` (the day–night circulation a box lacks; the sideways transport a ring lacks) | Coupling |

**Terrain** (`series-terrain`): nudging over terrain, each column held toward the reference at its own
height; the Rayleigh layer damping toward the initial state over terrain; every column's ground from
`terluna_surface2d.txt`; the day–night forcing and the vertical wind (`var13` = 3) at each column's own
height, staggered once to u and v points. **Sea** (`series-sea`): water columns of the two-dimensional
surface become sea. **Twilight** (`series-twilight`, `var20` = 1): after RRTMG, each shell's share of the
curved air's sunlight by the column's solar elevation, below the horizon too, heats the levels it
overlaps, the ground takes its share in the column's clear share, and each shell's and the ground's
extra infrared escape cools them, scaled with temperature to the fourth power (`terluna_twilight.txt`).
**Earth fall** (`series-earth-fall`): a control in which hydrometeors fall at Earth's speeds and
everything else keeps the host gravity.

**Electrification** (`series-elec`, with the WRF-ELEC files and `fortran/`)

| # | File | Change |
|---|---|---|
| 01 | module_discharge_msz.F | The branched lightning's reports go to its own log unit |
| 02 | module_mp_nssl_2mom.F (WRF-ELEC's) | Settings CM1 reads made public; CM1's equation set, charging switch and law passed in; OpenMP over slabs as in CM1's copy; cloud-ice radius handed on whole for `terluna_elec.F` to cap at RRTMG's 140 µm |
| 03 | module_mp_nssl_2mom.F | Fall speeds of rain, snow, cloud ice, graupel and hail scaled by (g/9.81)^((b+1)/3) where each is present; drag-law particles and Stokes droplets with the host g; rain and cloud-ice ventilation at the scaled speeds |
| 04 | module_discharge_msz.F | Branched lightning on one process; breakdown-field bounds from the build; the leader's crossing to the ground (`var1`) |
| 05 | mp_driver.F | CM1's calls go to `terluna_nssl_elec` with the charge tracers; rain accounting as WRF reports it |
| 06–08 | cm1.F, param.F, init3d.F | Charge tracers and time passed to the microphysics; the vertical field kept with each restart; charging switch (`var6`) and law (`var7`); tracers start at zero |
| 09 | Makefile | The added files and their dependencies |

`fortran/terluna_elec.F` reorders CM1's (i, j, k) arrays to WRF's (i, k, j), keeps the charges in CM1's
passive tracers, sub-steps sedimentation with a field solve and lightning after each sub-step, and
applies leakage and point discharge; `terluna_lightning.F` solves Poisson's equation by FFT across the
periodic domain with a tridiagonal solve on stretched levels and carries the cylindrical discharge;
`terluna_branched.F` runs one branched flash on a domain that wraps round; `terluna_screen.F` ports
WRF-ELEC's screening layers and adds point discharge from the ground; `terluna_mlint2.F` is WRF-ELEC's
trilinear interpolation taken out of `module_boxmgsetup.F`. Namelist: `var1` leader internal field (V/m
at 1.225 kg/m³), `var2` point-discharge onset, `var3` screening, `var4` ground-strike rule, `var5`
sub-step, `var6` charging, `var7` charging law, `var8` lightning (4: branched without the 180 kV/m cap),
`var9` leakage, `var10` cylinder radius. The lunar defaults: sub-step 6.8 s, WRF-ELEC's −7 °C ground rule
with the leader's crossing at 1 kV/m, the cap lifted, leakage on.

**The lab's** (`series-lab`, after `series-core`). The lab's own patches put four of Terluna's changes behind
entries of `&param3`, so that one build serves every case: two that Terluna compiled as build variants
(`climate/crm/cm1_run.py` at `bdda5a07`) and its two patches of Morrison's rain (the same file at `39c5ee04`). At
each switch's default, 0, the build keeps CM1's own path.

| # | Files | Switch | Change | Kind |
|---|---|---|---|---|
| 01 | turb.F; input.F, cm1.F, param.F | `ipbl2_per_mass` = 1 | The simple boundary layer's (`ipbl = 2`) tendencies of θ, the mixing ratios and the wind divided by the density, at u and v points for the wind, so that `solve1.F` adds changes per second, as it does for the other schemes (Terluna's `PBL_DENSITY_PATCH`). `solve1.F` then averages `upten` and `vpten` as fields at scalar points, while this scheme fills them at u and v points; the patch leaves that averaging as CM1 has it | General repair of a defect (A9) |
| 02 | sfclay.F, init_physics.F; input.F, cm1.F, param.F | `gust_over_water` = 1 | The MM5 surface layer (`sfcmodel = 2`) takes Beljaars's convective gust over water as over land, at the build's gravity, in place of the old MM5 formula √Δθv m/s, which has no gravity in it (Terluna's `GUST_PATCH`) | General repair of an Earth value (B35), for convective surface layers; a stable surface layer takes no gust |
| 03 | morrison.F; input.F, cm1.F, param.F | `brkup_gscale` = 1, with `brkup_rhor` and `brkup_rhoexp` | Morrison's limits on rain at the build's gravity. With s = (9.81/g)^½, the ratio of the capillary lengths, the breakup law's two lengths, its cutoff (300 µm, `brkup_db`) and its e-folding length 1/2300 m, are multiplied by s · `brkup_rhor`^`brkup_rhoexp`; the 2.8 mm cap on rain's mean diameter is multiplied by s; and the cap on its mean fall speeds becomes 9.1 (g/9.81)^¼ m/s, where core patch 04 sets 9.1 (g/9.81)^0.6. `brkup_rhor` is the surface air's density over that of Earth's sea-level air at the same temperature, in CM1 the surface pressure over 1013.25 hPa, and `brkup_rhoexp` its exponent (defaults 1.0 and 0.0) (Terluna's `RAIN_LIMITS_PATCHES`) | General repair of Earth values (B28), by a scaling law |
| 04 | morrison.F; input.F, cm1.F, param.F | `rain_fall_law` = 1; `rain_selfcoll` > 0 | Rain's fall law from a table, and its self-collection at a given rate. Morrison reads the fall law through three moments of rain's exponential spectrum: the mass-weighted and number-weighted mean fall speeds, in the sedimentation and in rain's collection of snow and graupel, and the ventilation integral of its evaporation. With `rain_fall_law` = 1 the three come from `lab_rain_law.txt` in the run's folder. A positive `rain_selfcoll` replaces the 5.78 m³/kg/s of rain's self-collection (Terluna's `RAIN_LAW_PATCHES`) | General repair of an Earth fit and an Earth rate; the table and the rate are inputs computed for the world |

Applied to pristine CM1 r22.0 on the OpenMP makefile after the core series, the four patches give the sources
`expected-series.sha256` records (`models/check_patches.sh`). The sources of the first two compiled with gfortran and
OpenMP on 8 November 2026, and those of all four on 11 November, under CM1's flags and under `-O3 -march=native`
(gfortran 13.3.0, at CM1's own gravity and air). Stage 3's CM1 builds will test the identity at the defaults of a
compiled case on the lab's own builds and measure each fix's effect in the lab's own runs. Terluna ran the code of the
first two as build variants: with the density divided out, its boxes' boundary layer passed on 0.995–1.000 of the
evaporation in its trials, and Beljaars's gust, computed from the sea box's own fluxes, raises its wind 1.1–1.2
times, where the MM5 formula raised it 1.6–1.8 times.

### Rain's limits, fall law and self-collection (patches 03 and 04)

**The entries and the table.** `python/atmosphere/rain/` computes a world's entries from its air at 2 m, given as a
gravity, a pressure, a temperature, a humidity and a dry composition (`fall_law.settings`): `brkup_rhor`; the exponent
`brkup_rhoexp`, from the Weber numbers of the drops' collisions on that world and on Earth (`breakup.py`);
`rain_selfcoll`, Earth's rate over the ratio of the two worlds' collision kernels; and the table's text
(`fall_law.table_text`). The table gives, for 301 slopes λ of the spectrum on a uniform grid in ln λ from 100 to
100,000 per metre, the natural logs of the two mean fall speeds (m/s) and of the integral of D^1.5 V^0.5 e^(−λD) dD
(m³ s^−½), each in Morrison's reference air; its first line states the count of rows, the first ln λ and the step.
The speeds are a single-drop solver's (`drops.py`, after Loftus and Wordsworth 2021), integrated over the spectrum.
CM1 reads the table linearly in ln λ and takes its end rows beyond it, multiplies the speeds by the scheme's density
factor (ρ₀/ρ)^0.54 and the integral by that factor's square root, and keeps its cap on the mean speeds. With
`brkup_gscale` = 1 the namelist's `brkup_db` stays Morrison's 300 µm, since the patch scales it. CM1's own line
`D_b =`, among the scheme's settings in the log, prints that namelist value, the unscaled cutoff; the line
`Lab rain limits:`, above it, prints the cutoff, the rate and the two caps in force.

For the Open Moon's air, the design air at 1.2 atm with the 300.4 K and 61% humidity of Terluna's resort climate, the
entries are `brkup_rhor` = 1.2, `brkup_rhoexp` = 0.687 and `rain_selfcoll` = 2.919 m³/kg/s. They give breakup from
0.84 mm at 826 per metre, a balance of self-collection and breakup at a mean diameter of 1.68 mm, where CM1's own
lies at 0.60 mm, a 6.88 mm cap, a 5.80 m/s cap on the mean fall speeds in the reference air, and self-collection 1.98
times slower than Earth's. These are the numbers of Terluna's products (`atmosphere/rain/results/rain_breakup.json`
and `rain_fall_law.json` at `39c5ee04`), and the lab's modules return them to the last digit from the same air. At
CM1's 9.81 m/s² in Earth's air the scaled limits are CM1's own, and `fall_law.settings` returns a rate of
5.7808 m³/kg/s, 0.01% above CM1's 5.78, since it measures the world against an Earth at the standard 9.80665 m/s²;
at that gravity it returns 5.78. The table there is the solver's, which Morrison's Earth fit follows in part: over
mean diameters of 0.2 to 3 mm the fit's mass-weighted speed under its 9.1 m/s cap is 0.87 to 1.12 of the solver's,
its number-weighted speed 0.93 to 1.23 and its ventilation integral 0.95 to 1.31, so an Earth case that reads the
table changes its rain.

**Where the lab's patches differ from Terluna's.** The identifiers, the comments and the table's name are the lab's
(`LAB_RAIN`; `lab_rain_law.txt` for Terluna's `terluna_rain_law.txt`), and the entries of `&param3` keep Terluna's
names. The code differs in two places. The lab's scheme stops at its start on a `brkup_gscale` other than 0 and 1 and
on a table of fewer than two rows or with a step of zero or less, which Terluna's patches leave unchecked. And where
Terluna's patch branches on the table at each of the four statements at which rain's collection of snow and graupel
computes rain's two mean fall speeds, the lab's sets the two speeds once in each level, where rain's slope is set, by
CM1's own expressions at the default; the four statements read them, so that the collection's blocks contain no
branch.

**The default path's last bits.** The branch was moved out of the collection because of a difference that Terluna
recorded on 21 October (`climate/crm/README.md` at `39c5ee04`, "The build and the smoke test"). At
`-O3 -march=native` Terluna's build with the law patch at its default parted from its rain-limits build in the last
digits, the rain at the ground of its small box differing in the sixth digit after two hours, while two builds made
with `-ffp-contract=off -nostdinc`, without fused multiply-adds and without glibc's vector maths, matched bit for bit
in every output, statistic and restart file. Terluna's record attributes the parting to vectorisation: the patch's
branches change which of Morrison's loops gfortran vectorises, and so where it calls glibc's vector exp and log. That
strict build removes the fused products and the vector maths together. The lab's runs of 11 November 2026 removed
them one at a time, on single columns of the scheme and on a compiled case, each run made once (the one-off checks
below).

On the columns, the storm column and twenty random ones at the Moon's gravity with the switches at their defaults,
three forms of `morrison.F` were compared with the scheme before the two patches under eight sets of gfortran's
flags: the lab's patch 04; the lab's sources with Terluna's branch at each of the four statements; and the
`morrison.F` of Terluna's build `moon_omp_rain_law_pbl_wind_gust_aloft_inflow` (sha256 `79170284…`). Each set adds
its flags to `-ffree-form -ffree-line-length-none -finline-functions --param=max-vartrack-size=0 -fopenmp`, and the
two counts of instructions and functions are those of the lab's `morrison.o`.

| Flags | Fused multiply-adds in `morrison.o` | Vector-maths functions it calls | Columns of 21 that differ: the lab's patch 04 | Terluna's branches | Terluna's file |
|---|---|---|---|---|---|
| `-O2`, CM1's own | 0 | 0 | 0 | 0 | 0 |
| `-O3` | 0 | 2 | 0 | 0 | 0 |
| `-O3 -march=native -ffp-contract=off` | 0 | 5 | 0 | 0 | 0 |
| `-O3 -march=native -ffp-contract=off -nostdinc`, the flags of Terluna's strict build | 0 | 0 | 0 | 0 | 0 |
| `-O3 -march=native`, Terluna's OpenMP default and the lab's (`lab/configs/cm1/defaults.toml`) | 550 | 5 | 0 | 13 | 13 |
| `-O3 -march=native -nostdinc` | 553 | 0 | 0 | 13 | 13 |
| `-O3 -march=native -fno-tree-vectorize` | 485 | 0 | 0 | 13 | 13 |
| `-O2 -mfma` | 374 | 0 | 0 | 13 | 13 |

With Terluna's branches the default path lost its last bits in 13 of the 21 columns, by up to 1 part in 10⁵ of a
field's largest value, under each of the four sets with which gfortran fused products, and kept them in all 21 under
each of the four with which it fused none. The object calls vector maths under one of the four sets that fused
products and under two of the four that fused none, and one set that lost the bits has gfortran's vectoriser off.
Under `-O3 -march=native` the calls of vector maths lie in `graupel_init`, where the reflectivity's size bins are
set, and in the reflectivity routine `calc_refl10cm`; the column routine `M2005MICRO_GRAUPEL`, with 376 of the 550
fused multiply-adds, calls none.

On the compiled case, CM1's released supercell on builds of the whole model, Terluna's branches changed 39 of the
2.4 million values of the fields after 1,500 s under `-O3 -march=native`, by up to 4 parts in 10⁷, and 53 of them in
a build with `-nostdinc` added, whose objects call no vector maths; with `-ffp-contract=off` added in its place, the
nine output files equal those of the series before the patches byte for byte.

Across these runs Terluna's branches changed the default path's bits under every flag set with which gfortran fused
products into multiply-adds and under none of the others, with vector maths called or absent. The lab's sources with
those branches differ from the lab's patch only in where the collection's two speeds are computed. In the lab's runs
the cause is therefore the fusing: with a branch at the four statements gfortran fuses a different set of products,
and which products those are was left unexamined. For Terluna's small box the same cause is inferred, since the lab
ran neither that box nor a build of Terluna's series.

**Checks in the suite** (`make check`). The column is CM1's `mp_graupel`, compiled with `input.F` and `constants.F`
from the series before the two patches, after 03 and after 04, and called as `mp_driver.F` calls it
(`python/climate/tests/test_cm1_rain.py`).

| Check | Result | Evidence state |
|---|---|---|
| The series on the pinned archive | The sources of `expected-series.sha256`, with every Terluna build still reproduced (`models/check_patches.sh`) | The patches apply |
| The patches' text | In `morrison.F` after each patch the default's branch is CM1's own statement: the limits' block sets the rate to CM1's 2300 per metre outside its test of `brkup_gscale`, the evaporation and the sedimentation keep CM1's expressions beside the table's, and the collection's two speeds are CM1's expressions, written where rain's slope is set; the collection's blocks contain no branch of the patch; autoconversion and accretion are unchanged | The default path's statements are CM1's, by their text |
| One column at the defaults | A storm column of 40 levels over 100 steps and twelve random columns over 20 steps, at the Moon's gravity and at 9.81 m/s², under CM1's OpenMP flags and under `-O3 -march=native`, return every field bit for bit after each patch | Identity at the default, of the scheme's routine |
| The limits in the compiled scheme | The cutoff, the rate and the two caps CM1 prints equal `breakup.limits` to 2 parts in 10⁶ at the Moon's gravity, at 3.7 m/s² and at 9.81 m/s²; at 9.81 m/s² with `brkup_rhor` = 1 the scaled scheme returns the storm column bit for bit as the default | The Fortran agrees with the Python |
| Breakup's balance | Sixty uniform levels of rain settle at a mean diameter of 0.601 mm under CM1's limits and of 1.675 mm under the Open Moon's, from 0.4 mm and from 2.5 mm, within 0.1% of `breakup.limits` | Effect, in one column |
| Fall speeds and caps | For mean diameters from 30 µm to 9 mm the mass-weighted speed CM1 returns is the power law's, or the table's, times the density factor, under the cap in force, to 5 parts in 10⁶, and a wider spectrum returns at the cap on the mean diameter, 2.8 or 6.88 mm | Effect, in one column |
| Sedimentation of water and of drops | From rain of eight mean diameters between 50 µm and 3 mm, each in one level of saturated air, the level below receives in one step the water that the mass-weighted mean speed delivers and the drops that the number-weighted delivers, by hand from the power law's closed forms or from the table's first two moments, to 2 parts in 10⁵; the two speeds differ by a factor of two or more at each diameter | Effect, in one column, against hand arithmetic |
| The table's three moments, each where the scheme reads it | With a table of the power law's own three moments in closed form, the storm column returns the default's fields to 2 parts in 10⁵ of each field's largest value after 1, 5 and 100 steps. Eight places read the table: rain's two speeds where its slope is set, above freezing and below; the two speeds of the sedimentation; and the evaporation's integral, above freezing and below | The Fortran reads each moment where the scheme needs it |
| Evaporation | Rain's evaporation with the table, over that with the power law, equals the ratio of the two ventilated sums by hand to 2 parts in 10⁵, above freezing and below: 0.84 to 1.07 for mean diameters of 60 µm to 5 mm | Effect, in one column |
| Self-collection | Between 5.78 and 2.919 m³/kg/s the drops lost in a step differ by the rates' difference times ρ q N Δt, to 1 part in 10⁴ | Effect, in one column |
| Stops and the printed moments | A density ratio of zero, a `brkup_gscale` of 2, a `rain_fall_law` of 2, a folder without the table, a table of one row and a table with a step of zero each end the run at the scheme's start. With the Open Moon's table the scheme prints the three moments it reads at a slope of 1,000 per metre, 3.763 m/s, 1.184 m/s and 6.661 × 10⁻⁸ m³ s^−½, the Python's to 1 part in 10⁶ | The scheme stops on settings it cannot take; the Fortran agrees with the Python |
| The Python | Terluna's numbers for the Open Moon; hand arithmetic at the Moon's gravity, at Earth's and at 3.7 m/s²; Morrison's constants read from the pinned source; the solver against 34 of Gunn and Kinzer's fall speeds on Earth, within 0.20 m/s rms (`python/atmosphere/tests/test_rain_*.py`) | Reproduction of Terluna's calculation; hand arithmetic; for the solver on Earth, empirical validation |
| The registry | B28 names patch 03's switch as its repair and warns where Morrison's rain keeps Earth's limits off Earth's gravity, and `cm1-rain-limits-range` warns below 1.62 m/s² with the limits scaled (`lab/tests/test_spec.py`) | The registry's entries are as recorded |

**Checks run once**, on 11 November 2026, with gfortran 13.3.0 on an Intel i9-11980HK, one thread to a run. Each is
a single run from scratch scripts and builds on the project drive, which stay outside the repository and the suite
(`world-crafting-research/tmp/port-rain/tools/`: `checks.py`, `case_builds.sh` and `case_runs.py`, with their logs in
`tmp/port-rain/checks/`). They ran on the series' sources as they stood before one comment of patch 04 was reworded;
`morrison.o` compiles to the same bytes from both texts under CM1's flags and under `-O3 -march=native`.

| Check | Result | Evidence state |
|---|---|---|
| The whole model | Nine builds at CM1's own gravity and air compiled and linked: the series before the two patches under CM1's OpenMP flags, under `-O3 -march=native`, and under the latter with `-ffp-contract=off` and with `-nostdinc`; the series itself under the first two; and the lab's sources with Terluna's branches under the last three | The sources compile |
| The default path's bits on one column, flag set by flag set | The table above: the lab's patch 04 kept every field of the 21 columns under the eight sets, and Terluna's branches lost the last bits of 13 columns under the four sets that fuse products | Identity at the default, of the scheme's routine, under eight flag sets; the cause of the difference in Terluna's form |
| A compiled case at the defaults | CM1's released case (`run/namelist.input` in the archive, a supercell under Morrison's scheme on 60 × 60 × 40 points) with four settings changed so that rain and ice form within about a hundred steps: `dtl` 12 s for 7.5, `timax` 1,500 s for 7,200, `tapfrq` 1,500 s for 900 and `statfrq` 300 s for 60. Over its 125 steps at CM1's own gravity the nine output files, the fields at the start and after 1,500 s and the statistics, agree byte for byte between the series before the two patches and after them, under CM1's OpenMP flags and under `-O3 -march=native`. By 1,500 s the storm contains rain, hail, snow and cloud ice | Identity at the default, of a compiled case of CM1's own |
| Terluna's branches in that case | Against the series before the patches, 39 of the 2,368,800 values of the fields after 1,500 s differ under `-O3 -march=native`, by up to 4 parts in 10⁷, with 2 of the 852 statistics; 53 values and 2 statistics differ with `-nostdinc` added; the nine files agree byte for byte with `-ffp-contract=off` added | The cause of the difference in Terluna's form, in a compiled case |
| The entries in a compiled case | In that case the model reads the five entries from `&param3` and prints them. `brkup_gscale` = 1 with a density ratio of 1 returns the default's output byte for byte; a ratio of 1.2 with the exponent 0.71 sets the cutoff at 0.3415 mm and the rate at 2,020.7 per metre, the values of `breakup.limits`, and changes the output, as do a `rain_selfcoll` of 2.919 and Earth's own table; `brkup_gscale` = 2 stops the model at the scheme's start with the patch's message | The namelist's entries act in a compiled case |
| Terluna's scheme | On the 21 columns the `morrison.F` of Terluna's build and the lab's returned the same fields to the bit under CM1's flags, at the defaults, with the Open Moon's limits, and with its table and rate. Under `-O3 -march=native` they differed in 13, 14 and 13 of the columns, by up to 3 parts in 10⁵ of a field's largest value | Agreement with Terluna's code where products stay unfused |
| Each statement runs | On the storm column gcov counted 26 statements of the column routine that the patches add or change: the 12 common to both paths and the 6 of CM1's own path ran at the defaults, and the 12 and the 8 of the table's path ran with the switches on | The storm column exercises the patched statements |
| Bounds, uninitialised reals and traps | Compiled with `-O0 -fcheck=all -finit-real=snan -ffpe-trap=invalid,zero,overflow`, the scheme ran the storm column and twelve random ones clean at the defaults and with the switches on | No fault of these three kinds in those columns |
| A wrong moment at each place | With another moment of the table at any one of the eight places that read it, the suite's test of the three moments fails: a field departs from the default's by 6 parts in 10³ or more after one step, where the patch as written departs by 2 parts in 10⁶ | The suite detects a wrong moment at each of the eight places |

Two checks wait for stage 3: the identity at the defaults of a lunar case on the lab's own builds, and the effect in
a run at the world's gravity. In Terluna's small box the lunar limits nearly doubled the rain at the ground over its
second lunar day, from 33 to 63 mm a lunar day (`notes/cm1.md`, "Fall speeds").

**Limits.**

- The scaling is a similarity. Colliding drops are taken to coalesce or break by their Weber number alone, the law of
  Straub et al. (2010), which `python/atmosphere/rain/sources.json` records as taken from that paper's abstract; the
  collisions' energies come from the solver's terminal speeds; and no measurement at another gravity tests the
  result. Terluna computed the scale for gravities from the Moon's to Earth's. The lab's registry warns below
  1.62 m/s² (`cm1-rain-limits-range`) and is silent above Earth's gravity, the other side of that range. B28 keeps a
  warning for a case that leaves the limits unscaled off Earth's gravity, since each fix enters the lab opt-in
  (`PLAN.md`), where row 5 of `lab/design/terluna_fixes.md` proposed that the registry require the scaling.
- `fall_law.settings` gives CM1 the surface pressure over 1013.25 hPa as `brkup_rhor`, with an exponent fitted on the
  ratio of the two airs' densities. The two ratios agree for dry air of Earth's molar mass, CM1's air having Earth's
  gas constant. The breakup scale the patch then sets is 0.2% above the collisions' own in the Open Moon's air, of
  17.5% oxygen; with 10% and 35% oxygen it is 0.9% above and 1.3% below at the Moon's gravity and 1.2 atm, and 1.2%
  above and 1.5% below at CM1's gravity and 1 atm (`python/atmosphere/tests/test_rain_fall_law.py`).
- The table and the rate are computed in the world's air at 2 m, at one temperature and humidity, for air of N2, O2,
  Ar and CO2 with a ground between 273.15 and 313.15 K; at each level above, the scheme multiplies the speeds by its
  density factor (ρ₀/ρ)^0.54 alone. The table spans mean diameters from 10 µm to 10 mm, which the scaled cap exceeds
  below 0.77 m/s², and the solver stops below about 0.48 m/s², where the largest stable drop exceeds its 30 mm.
- The rate is computed at the scaled limits' balance, so a case that takes the table and the rate takes
  `brkup_gscale` = 1 with them; Terluna's runner refuses its lunar law without its lunar limits, and the lab's case
  writer applies that rule from stage 3.
- Rain's collection of cloud ice keeps the power law at the build's gravity, as in Terluna's patch. Autoconversion
  and accretion keep Earth's rates (defect log B38), and NSSL's rain, which the electrified build runs, keeps its own
  limits and law.
- Gravity is the build's (core patch 01). Each rank of an MPI build reads the table itself; the series was compiled
  with OpenMP alone.
- A setting CM1 cannot take stops the run at the scheme's start: with `brkup_gscale` = 1 a density ratio of zero or
  less; a `brkup_gscale` or a `rain_fall_law` other than 0 and 1; a table of fewer than two rows or with a step of
  zero or less; and a missing table, on which gfortran's own error ends the run. gfortran's `STOP` with a message
  returns status 0, so a runner finds the patch's stops by their text.
- The identity at the defaults was run with gfortran 13.3.0 on one processor that has fused multiply-adds. The
  suite's column test repeats it under CM1's flags and under `-O3 -march=native` wherever the suite runs, and for
  each later patch to the scheme.

## Settings of the lunar cases

The Rayleigh damping rate `rdalpha` = (g/9.81)/300 s⁻¹ and the boundary-layer scheme's asymptotic
length `l_inf` = 75 m × 9.81/g stretch with gravity as the dynamics do; 6 km columns at lunar gravity
resolve convection as about 1 km columns do on Earth. The rings use the Morrison scheme with 100
droplets per cm³, RRTMG every 30 minutes, the MM5 surface layer with fixed sea temperatures,
`cm1setup` 2 with CM1's simple boundary-layer scheme, 111 stretched levels to 150 km (100 m apart near
the ground, 2 km above 27 km), damping above 115 km, and nudging toward the GCM over 3 days from 8 km,
fully from 16 km. Case set-up stays in Terluna (`climate/crm/cm1_run.py`).

## Builds and their check

[builds.json](builds.json) lists the 14 build variants, the patches each applies, its gravity and
flags, and the cases recorded on its deployed executable. On 2026-10-17 the series applied with GNU
patch to pristine CM1 r22.0 reproduced every Fortran source of the deployed builds behind the current
results; the details and the exceptions are in that file. The lab's series follows the core on the OpenMP
makefile, and `expected-series.sha256` records the sources it gives.
