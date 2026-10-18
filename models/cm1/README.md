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
results; the details and the exceptions are in that file.
