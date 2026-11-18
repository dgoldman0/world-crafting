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

A build that applies the lab's series after the core (`series-lab`, below) reads the three values from the
namelist as well, as `world_g`, `world_co2` and `world_o2` of `&param3`, with the macros' values as their defaults.
One such build, compiled without the macros, serves every world, and a build compiled with them runs as before
where its namelist leaves the entries out ("The world from the namelist", below).

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
each switch's default, 0, the build keeps CM1's own path. A fifth patch, the lab's own, puts two factors on the
rates at which Morrison's cloud turns into rain; at their default, 1, the scheme keeps CM1's rates. Three more, the
lab's own, read the world from the namelist, so that one build serves every world: its gravity, CO2 and O2, which
Terluna's builds compile in, the slab soil's top layer and the Sun's declination. Each entry's default is the
present build's value. The ninth puts Terluna's three changes to the nudging of its site boxes behind entries of
`&param3`, which its build read from CM1's spare reals (the same file at `39c5ee04`); at their defaults the nudging
stands as CM1 has it. The tenth puts Terluna's damped gravity wave, by which a forced box makes its own large-scale
vertical wind, behind entries of `&param3` (the same file at `29af5c16`); at their defaults CM1 imposes the wind as
before. The eleventh, the lab's own, adds the weak temperature gradient as a second way for the box to make that wind,
with one entry of its own; at its defaults too CM1 imposes the wind.

| # | Files | Switch | Change | Kind |
|---|---|---|---|---|
| 01 | turb.F; input.F, cm1.F, param.F | `ipbl2_per_mass` = 1 | The simple boundary layer's (`ipbl = 2`) tendencies of θ, the mixing ratios and the wind divided by the density, at u and v points for the wind, so that `solve1.F` adds changes per second, as it does for the other schemes (Terluna's `PBL_DENSITY_PATCH`). `solve1.F` then averages `upten` and `vpten` as fields at scalar points, while this scheme fills them at u and v points; the patch leaves that averaging as CM1 has it | General repair of a defect (A9) |
| 02 | sfclay.F, init_physics.F; input.F, cm1.F, param.F | `gust_over_water` = 1 | The MM5 surface layer (`sfcmodel = 2`) takes Beljaars's convective gust over water as over land, at the build's gravity, in place of the old MM5 formula √Δθv m/s, which has no gravity in it (Terluna's `GUST_PATCH`) | General repair of an Earth value (B35), for convective surface layers; a stable surface layer takes no gust |
| 03 | morrison.F; input.F, cm1.F, param.F | `brkup_gscale` = 1, with `brkup_rhor` and `brkup_rhoexp` | Morrison's limits on rain at the build's gravity. With s = (9.81/g)^½, the ratio of the capillary lengths, the breakup law's two lengths, its cutoff (300 µm, `brkup_db`) and its e-folding length 1/2300 m, are multiplied by s · `brkup_rhor`^`brkup_rhoexp`; the 2.8 mm cap on rain's mean diameter is multiplied by s; and the cap on its mean fall speeds becomes 9.1 (g/9.81)^¼ m/s, where core patch 04 sets 9.1 (g/9.81)^0.6. `brkup_rhor` is the surface air's density over that of Earth's sea-level air at the same temperature, in CM1 the surface pressure over 1013.25 hPa, and `brkup_rhoexp` its exponent (defaults 1.0 and 0.0) (Terluna's `RAIN_LIMITS_PATCHES`) | General repair of Earth values (B28), by a scaling law |
| 04 | morrison.F; input.F, cm1.F, param.F | `rain_fall_law` = 1; `rain_selfcoll` > 0 | Rain's fall law from a table, and its self-collection at a given rate. Morrison reads the fall law through three moments of rain's exponential spectrum: the mass-weighted and number-weighted mean fall speeds, in the sedimentation and in rain's collection of snow and graupel, and the ventilation integral of its evaporation. With `rain_fall_law` = 1 the three come from `lab_rain_law.txt` in the run's folder. A positive `rain_selfcoll` replaces the 5.78 m³/kg/s of rain's self-collection (Terluna's `RAIN_LAW_PATCHES`) | General repair of an Earth fit and an Earth rate; the table and the rate are inputs computed for the world |
| 05 | morrison.F; input.F, cm1.F, param.F | `rain_autoconv_fac`, `rain_accr_fac` (each 1 by default) | Two factors on Morrison's warm rain: `rain_autoconv_fac` multiplies the autoconversion of cloud water to rain and `rain_accr_fac` the accretion of cloud water by rain, each in Khairoutdinov and Kogan's (2000) fit, above freezing and below, and the number tendencies follow from the scaled rates by CM1's own statements. Gravity appears in neither fit; for a world the factors are g/9.81 and (g/9.81)^0.6 (the lab's own patch, with no Terluna source) | General repair of two Earth fits (B38), by a scaling law; its effect in a run is unmeasured |
| 06 | constants.F, getcape.F, base.F, domaindiag.F, writeout.F, init_physics.F, module_ra_etc.F, module_ra_rrtmg_lw.F, module_ra_rrtmg_sw.F, radiation_driver.F; input.F, cm1.F, param.F | `world_g`, `world_co2`, `world_o2` (the build's `TERLUNA_G`, `TERLUNA_CO2` and `TERLUNA_O2` by default: 9.81 m/s², 400 ppm and 0.209488 in a build without the macros) | Gravity, CO2 and O2 from the namelist. `world_g` becomes CM1's `g` as the model starts, which the dynamics, Morrison's scheme and the schemes that take `g` by argument read; RRTMG takes it as an argument of its two initialisations, where it read a compile-time constant, and the CAPE diagnostic as an argument of its three calls. `world_co2` and `world_o2` reach RRTMG's two drivers as arguments. The MYNN and MYJ schemes keep the build's gravity, and a run of them stops unless `world_g` equals it (the lab's own patch, with no Terluna source) | General repair: the values core patches 01–03, 06 and 07 compile in become inputs of one build (B1, B8) |
| 07 | init_surface.F; input.F, cm1.F, param.F | `soil_dz1` (0.05 m by default, core patch 08's) | The slab soil's top layer from the namelist; each of the four layers below is twice the one above, as in CM1. A world's layer is CM1's 1 cm times the square root of its solar day in Earth days (the lab's own patch) | General repair of a unit of time (`cm1-soil-day`, B10) |
| 08 | radiation_driver.F; input.F, cm1.F, param.F | `sun_decl` (0° by default, the equinox of core patch 05) | The Sun's declination, in degrees north, under core patch 05's solar day: the zenith cosine sin(lat) sin(δ) + cos(lat) cos(δ) cos(hour angle) at each column's latitude, set by a loop that follows the equinox's where `sun_decl` differs from 0 (the lab's own patch) | General repair of a geometry (`cm1-equinox-sun`, B10) |
| 09 | solve1.F, solve3.F; input.F, cm1.F, param.F | `wind_nudge_tau` > 0; `wind_nudge_zmin` > 0; `inflow_ref_air` = 1 | CM1's large-scale nudging (`lsnudge`) relaxes the wind on its own time, `wind_nudge_tau` seconds, where θ and vapour keep `lsnudge_tau`: the domain-mean wind in `solve1.F` and the base-state and geostrophic wind in `solve3.F`; it pulls the domain-mean wind only at the levels from `wind_nudge_zmin` m up; and with `inflow_ref_air` = 1 the large-scale vertical wind's convergence draws the nudging reference's θ and vapour in, at max(d(ρ₀w)/dz, 0)/ρ₀ (Terluna's `WIND_TAU_PATCH`, `WIND_ALOFT_PATCH` and `INFLOW_PATCH`; the base-state and geostrophic wind's time the lab's) | Coupling: the forcing of a site box ("The wind's own nudging and the inflow", below) |
| 10 | solve1.F, cm1.F; input.F, param.F | `lsw_coupling` = 1, with `lsw_tau`, `lsw_mode_speed`, `lsw_top`, `lsw_base`; `lsw_table_heat` = 1 | The box's large-scale vertical wind its own, by the damped gravity wave: each step `solve1.F` solves d²ω/dp² = R_d T_v′/(τ c² p) for the domain-mean ω, nil at the ground and from the lid `lsw_top` up, T_v′ the domain-mean virtual temperature less the nudging window's between the coupled layer's base, the domain-mean boundary layer's depth no lower than `lsw_base`, and the lid, and sets `wprof` = −ω/(ρ₀g); with `lsw_table_heat` = 1 the table heats below the base alone; the means over each interval of the domain diagnostics go to `lab_lsw_means.txt`, the run's last interval included (Terluna's `DGW_PATCHES`; the record's timing, the base's mean, its own entries and the stops the lab's) | Coupling: a site box's own ascent ("The box's own large-scale vertical wind", below) |
| 11 | solve1.F, cm1.F, input.F, param.F | `lsw_coupling` = 2, with `lsw_tau`, `lsw_top`, `lsw_base`, `lsw_stab_min`; `lsw_table_heat` = 1 | The box's large-scale vertical wind its own, by the weak temperature gradient: in patch 10's block `solve1.F` sets w = θ_v′/(τ max(γ, ∂θ_v,r/∂z)) at the w levels from the first above the base to the last below the lid, θ_v′ the domain-mean virtual potential temperature less the nudging window's and ∂θ_v,r/∂z the window's own stability, γ = `lsw_stab_min`, with ω linear in pressure below the base, and sets `wprof` = −ω/(ρ₀g); the record, the table's cut and the base are patch 10's (Edman and Romps 2015, after Raymond and Zeng 2005; the lab's own patch) | Coupling: a site box's own ascent ("The box's own large-scale vertical wind by the weak temperature gradient", below) |

Applied to pristine CM1 r22.0 on the OpenMP makefile after the core series, the eleven patches give the sources
`expected-series.sha256` records (`models/check_patches.sh`). The sources of the first two compiled with gfortran and
OpenMP on 8 November 2026, those of the first four on 11 November under CM1's flags and under `-O3 -march=native`,
those of the first five the same day under CM1's flags (gfortran 13.3.0, at CM1's own gravity and air), those
of the first eight the same day under both flag sets, at CM1's own gravity and air and with the Moon's compiled in,
those of the first nine on 16 November under both flag sets, at CM1's own gravity and air, those of the first ten on
17 November and those of all eleven on 18 November, each under both flag sets, at CM1's own gravity and air. Where
the rows of patches 02 to 04, their names and their comments say the build's gravity, they mean CM1's `g`, which
since patch 06 is the run's. Stage 3's CM1
builds will test the identity at the defaults of a compiled case on the lab's own builds and measure each fix's
effect in the lab's own runs. Terluna ran the code of the first two as build variants: with the density divided out,
its boxes' boundary layer passed on 0.995–1.000 of the evaporation in its trials, and Beljaars's gust, computed from
the sea box's own fluxes, raises its wind 1.1–1.2 times, where the MM5 formula raised it 1.6–1.8 times.

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
  and accretion keep Earth's rates unless a case sets the factors of patch 05 (below; defect log B38), and NSSL's
  rain, which the electrified build runs, keeps its own limits and law.
- Gravity is CM1's `g`, which the build compiles in (core patch 01) or the namelist states (patch 06, below). Each
  rank of an MPI build reads the table itself; the series was compiled
  with OpenMP alone.
- A setting CM1 cannot take stops the run at the scheme's start: with `brkup_gscale` = 1 a density ratio of zero or
  less; a `brkup_gscale` or a `rain_fall_law` other than 0 and 1; a table of fewer than two rows or with a step of
  zero or less; and a missing table, on which gfortran's own error ends the run. gfortran's `STOP` with a message
  returns status 0, so a runner finds the patch's stops by their text.
- The identity at the defaults was run with gfortran 13.3.0 on one processor that has fused multiply-adds. The
  suite's column test repeats it under CM1's flags and under `-O3 -march=native` wherever the suite runs, and for
  each later patch to the scheme.

### Factors on autoconversion and accretion (patch 05)

**The entries.** `rain_autoconv_fac` and `rain_accr_fac`, each 1 by default, multiply the two rates at which
Morrison's scheme turns cloud water into rain: the autoconversion, 1350 q_c^2.47 N_c^−1.79, and the accretion of
cloud water by rain, 67 (q_c q_r)^1.15, both in kg/kg/s with N_c the cloud droplets per cm³, the fits of
Khairoutdinov and Kogan (2000). Each factor multiplies CM1's rate in the statement after the one that computes it,
so CM1's expression and its order of operations stay as they were, and the number tendencies follow from the scaled
rate by CM1's own statements: the new rain's drops (`NPRC1`, the rate over the mass of a drop of 25 µm radius) and
the cloud droplets that the two processes remove (`NPRC`, `NPRA`). The scheme prints the two factors at its start
(`Lab warm rain:`) and stops there on a factor of zero or less.

**The formulas the factors multiply.**

| Formula in `morrison.F` | When r22.0 takes it | Multiplied by patch 05 |
|---|---|---|
| Khairoutdinov and Kogan's autoconversion and accretion, above freezing and below (`IRAIN = 0`) | In every run of the scheme: `GRAUPEL_INIT` sets `IRAIN = 0`, and no namelist entry sets it | Yes: both rates in both branches, at four statements |
| Seifert and Beheng's autoconversion and accretion (`IRAIN = 1`) | In no run | No |
| Rain's self-collection and its breakup | In every run of the scheme | No; their entries are those of patches 03 and 04 |
| The collection of cloud water by snow and graupel, and the freezing of cloud water and of rain | Below freezing | No |

CM1's copy of the scheme holds the cloud's droplet number constant (`INUM = 1`, set in the same routine, at the
namelist's `ndcnst`), so the scheme resets the number that `NPRC` and `NPRA` reduce, and of the three number
tendencies the new rain's drops alone change a run.

**For a world.** `python/atmosphere/rain/warm_rain.py` (`factors`) gives the two entries from the world's gravity.
By the fall-speed scaling of core patch 04, a particle of the regime V = A D^B falls as g^((B+1)/3) at a fixed size.
Cloud droplets fall in the Stokes regime (B = 2), so one droplet overtakes another at a speed that goes as g, and
the autoconversion's factor is g/9.81; rain sweeps up cloud at its own fall speed (B = 0.8), and the accretion's
factor is (g/9.81)^0.6. Both are 1 at CM1's 9.81 m/s², and 0.166 and 0.340 at the Moon's 1.6242 m/s². The lab's
default keeps Earth's rates (`physics.warm_rain_rates = "earth"` in `lab/configs/cm1/defaults.toml`), and the
registry's B38 warns of them at another gravity.

**Checks in the suite** (`make check`), on the column of patches 03 and 04 (`python/climate/tests/test_cm1_rain.py`).

| Check | Result | Evidence state |
|---|---|---|
| The series on the pinned archive | The sources of `expected-series.sha256` (`models/check_patches.sh`) | The patch applies |
| The patch's text | CM1's two rates stay as CM1 writes them, each followed by its factor and then by CM1's statements for the number tendencies; Seifert and Beheng's formulas are unchanged, and `IRAIN` is set to 0 and read from no namelist; the patch adds 19 lines to `morrison.F` and changes none | The default path's statements are CM1's, by their text |
| One column at the defaults | The storm column over 100 steps and twelve random columns over 20 steps, at the Moon's gravity and at 9.81 m/s², under CM1's OpenMP flags and under `-O3 -march=native`, return every field bit for bit as before the patch | Identity at the default, of the scheme's routine |
| Autoconversion | Twelve uniform levels of cloud water in saturated air without rain, one step, at 290 K and at 270 K, where the branch below freezing runs and no ice forms. The rain a level gains is the fit's rate times the step, by hand to 2 parts in 10⁶, and its drops are that water over the mass of a drop of 25 µm radius. With the Moon's factor, 0.16557, the rain's water and its drops are the factor's share to 5 parts in 10⁷, and the cloud keeps the rest to 1 part in 10⁴. The accretion's factor leaves this column bit for bit as it was | Effect, in one column, against hand arithmetic |
| Accretion | Twelve uniform levels of cloud water and rain in saturated air, one step of 10 s, at 290 K and at 270 K. The rain's gain is the two fits' by hand to 5 parts in 10⁶. With the Moon's factor, 0.33993, the rain gains less and the cloud keeps more by the same water, the accretion less its factor's share, to 1 part in 10⁵, while the temperature, the vapour and, in the lowest eight levels, rain's number stay bit for bit | Effect, in one column, against hand arithmetic |
| Stops and the printed factors | A factor of 0 on the autoconversion and one of −0.5 on the accretion each end the run at the scheme's start; the scheme prints the Moon's two factors and, at the defaults, 1 and 1. In the storm column the Moon's factors leave the cloud 5% or more of extra water, summed over its levels, after 100 steps | The scheme stops on a factor it cannot take, and reads the two entries |
| The Python | The factors by hand at the Moon's gravity, at 9.81 m/s², at Mars's 3.72 m/s² and at twice CM1's gravity; the two fits, the 25 µm drops, the two fall-speed exponents and `IRAIN` on their lines of the pinned source (`python/atmosphere/tests/test_rain_warm.py`) | Hand arithmetic; the constants are the pinned source's |
| The registry | B38 names the patch and its two entries, stays open and warns where a Morrison case keeps Earth's rates off Earth's gravity (`lab/tests/test_spec.py`) | The registry's entry is as recorded |

**Checks run once**, on 11 November 2026, with gfortran 13.3.0 under CM1's OpenMP flags (`-O2`), one thread to a
run. Each is a single run from scratch scripts on the project drive, outside the repository and the suite
(`world-crafting-research/tmp/port-warm/tools/`: `case.sh` and `case_runs.py`, with their logs beside them), on the
sources of `expected-series.sha256`.

| Check | Result | Evidence state |
|---|---|---|
| The whole model | Two builds at CM1's own gravity and air compiled and linked: the series before patch 05 and after it | The sources compile, under CM1's flags |
| A compiled case at the defaults | CM1's released supercell with the four settings changed as for patches 03 and 04 (125 steps of 12 s): the nine output files agree byte for byte between the two builds | Identity at the default, of a compiled case of CM1's own, under CM1's flags |
| The entries in a compiled case | The model reads the two entries from `&param3` and prints them. With 0.166 and 0.340 the output changes: after 1,500 s the storm's largest rain mixing ratio is 0.009 g/kg against 3.7 g/kg at the defaults, and its largest cloud water 6.8 g/kg against 5.3 g/kg. A `rain_accr_fac` of 0 stops the model at the scheme's start with the patch's message. The case is Earth's, where the lunar factors have no place; the run reads the entries and sizes nothing | The namelist's entries act in a compiled case |

**Limits.**

- The factors are a scaling law, and their effect in a run is unmeasured until a sea box runs with them (`PLAN.md`,
  block 4, step 2). The scaling omits the collision efficiency's own dependence on the closing speed and the
  collisions that turbulence drives, which are independent of gravity. Both fits were made on drop spectra of
  Earth's clouds, and a factor multiplies each fit whole, with its exponents on the cloud's water and on the droplet
  number as they are; the lunar cases' 100 droplets per cm³, to whose −1.79 power the autoconversion goes, have no
  lunar basis either (defect log B38).
- The identity of a compiled case ran under CM1's flags alone. Under `-O3 -march=native`, the lab's default, the
  identity at the defaults is the column's, and a lunar case on the lab's own builds waits for stage 3.
- A build that predicted the droplet number would take `NPRC` and `NPRA` scaled, a path CM1's copy never runs and
  the suite leaves untested, as it does Seifert and Beheng's formulas.
- NSSL's rain, which the electrified build runs, keeps its own rates, and the lab's case writer, which is to set
  the entries from `physics.warm_rain_rates`, belongs to stage 3.
- gfortran's `STOP` with a message returns status 0, so a runner finds the patch's stops by their text. Each rank
  of an MPI build takes the entries by broadcast, lines the OpenMP builds leave uncompiled.

### The world from the namelist (patches 06 to 08)

**The entries.** Five entries of `&param3` state the world of a run. Each takes the present build's value as its
default, so that a namelist without them runs as the build ran before the three patches, and one build without the
macros serves every world. The lab's derivations give a world's values (`lab/worldlab/derive.py`), which the case
writer of stage 3 hands to CM1.

| Entry | Unit | Default | What a world supplies | The Open Moon |
|---|---|---|---|---|
| `world_g` | m/s² | The build's `TERLUNA_G`: 9.81 without the macro | Its surface gravity, GM/R² − (2/3)Ω²R (`derive.gravity`) | 1.6242107; Terluna's builds compile GM/R², 1.6242188765608128 |
| `world_co2` | Mole fraction of the air | The build's `TERLUNA_CO2`: 400 × 10⁻⁶ without the macro | CO2's share (`derive.mole_fractions`) | 4.0 × 10⁻⁴ |
| `world_o2` | Mole fraction of the air | The build's `TERLUNA_O2`: 0.209488 without the macro | O2's share | 0.1745785; Terluna's builds compile 0.174579 |
| `soil_dz1` | m | 0.05, the top layer of core patch 08 | CM1's 1 cm × (solar day/1 d)^½, the depth the day's heat reaches against Earth's (`derive.cm1_values`, `soil_top_layer_m`) | 0.0543 |
| `sun_decl` | Degrees north | 0, the equinox of core patch 05 | asin(sin ε sin L_s), from the obliquity ε and the case's solar longitude L_s (`derive.declination_deg`); the case starts at the hour angle −acos(−tan φ tan δ), which it states as `var18` (`derive.sunrise_hour_angle_deg`) | 0 at an equinox, 1.54 at the northern solstice |

The model prints the five with the rest of `&param3`. RRTMG prints the gravity it took as it starts (`cp,grv =`) and
its CO2 at its first call (`co2 =`), and `init_surface.F` prints the soil's layers (`Lab soil: the layers (m)`).

**Where each value was read, and what reads it now.** Before patch 06 five files read a build macro; after it the
macros give the entries their defaults at the head of `cm1.F`, and one read of `TERLUNA_G` remains, the constant
that MYNN and MYJ hold (below).

| Value | Read in the series before patch 06 | In the series' end |
|---|---|---|
| Gravity of the dynamics and of the physics that takes CM1's `g` | `constants.F`, `set_constants`: `g = TERLUNA_G`. From this `g` come `govtwo`, the base state, the solver's buoyancy, the turbulence and the surface exchange, Morrison's `G` with its scaled fall speeds and caps (core patch 04) and the lab's rain limits (patch 03), the gust over water (patch 02), and by argument the MM5 and revised surface layers, YSU, the ocean mixed layer, Tiedtke's convection and RRTMG's cloud water paths | `g = world_g`, which `param.F` hands to `set_constants` once the namelist is read and checked; the readers of `g` are unchanged |
| Gravity of RRTMG's gas columns and heating rates | `module_ra_etc.F`: `g`, a compile-time constant of `module_model_constants`, which `rrtmg_lwinit` and `rrtmg_swinit` pass to `rrtmg_lw_ini` and `rrtmg_sw_ini` (`grav`, `heatfac`) | An argument of the two initialisations, to which `init_physics.F` gives CM1's `g` |
| Gravity of the CAPE diagnostic | `getcape.F`: `g`, a compile-time constant, with `cpdg = cp/g` derived from it as it compiles | An argument of `getcape`, which its three calls give CM1's `g` (`base.F`, `domaindiag.F`, `writeout.F`); `cpdg` is computed at each call |
| Gravity of the MYNN boundary layer and of MYJ's boundary layer and surface layer | The same constant of `module_model_constants`, with `gtr`, `g_inv`, `BTG` and their like derived from it as the schemes compile | Unchanged: the schemes hold the build's value, and `init_physics.F` stops a run that selects one of them (`ipbl` 4, 5 or 6, `sfcmodel` 7) unless `world_g` equals it |
| RRTMG's CO2 | `module_ra_rrtmg_lw.F` and `_sw.F`: `co2 = TERLUNA_CO2` in each driver | `co2 = lab_co2`, an argument to which `radiation_driver.F` gives `world_co2` |
| RRTMG's O2 | The same files: `data o2 / TERLUNA_O2 /` | `o2 = lab_o2`, an argument to which `radiation_driver.F` gives `world_o2` |
| The slab soil's top layer | `init_surface.F`: `slab_dzs(1)=.05` (core patch 08) | `slab_dzs(1)=soil_dz1` |
| The Sun's declination | `radiation_driver.F`: zenith cosine cos(lat) cos(hour angle) under a solar day of `var19` s (core patch 05) | The same loop, followed where `sun_decl` differs from 0 by a loop that sets sin(lat) sin(δ) + cos(lat) cos(δ) cos(hour angle) at each column's latitude, on a circle of latitude or a tilted great circle, and passes δ on as the declination CM1 writes among its diagnostics |

Methane, nitrous oxide, the halocarbons and ozone stay at zero in every build, as core patches 06 and 07 set them.

**Earth's gravity as a number.** A scan of the 91 source files at the series' end for a gravity written as a number,
in code outside comments, finds it in sixteen. Five the series accounts for: the macro's default (`cm1.F`,
`module_ra_etc.F`), test cases 4 and 5 with the stop that guards them (`constants.F`, `param.F`), and Morrison's
reference gravity, against which core patch 04 and the lab's patch 03 scale Earth's values (`morrison.F`). Eleven
are schemes that hold Earth's gravity in any build, which the registry refuses at another gravity
(`cm1-earth-g-schemes`): `goddard.F`, `lfoice.F`, `module_gfs_physcons.F`, `module_mp_jensen_ishmael.F`,
`module_mp_nssl_2mom.F`, `module_mp_p3.F`, `module_sf_exchcoef.F`, `module_sf_gfdl.F`, `module_sf_mynn.F`,
`mp_wsm6.F` and `radtrns3d.F`. Two of them were absent from the notes and the registry until this scan: the
NASA-GSFC LFO microphysics (`goddard.F`, 981 cm/s²) and CM1's own copy of the NSSL scheme
(`module_mp_nssl_2mom.F`, `gr = 9.8`).

**Stops.** The model stops as it starts, before it sets its constants, on a `world_g` of zero or less; on a
`world_g` other than 9.81 in test cases 4 and 5, which set their own constants; on a `world_co2` or `world_o2` below
zero, or the two above one together; on a `soil_dz1` of zero or less; on a `sun_decl` beyond ±90°; and on a
`sun_decl` other than 0 without the Sun it acts on, RRTMG under a solar day of `var19` seconds. `init_physics.F`
stops a run of MYNN or MYJ whose `world_g` differs from the build's gravity. Each stop prints a line that begins
`Lab world:`, `Lab soil:` or `Lab Sun:` and ends the run through CM1's `stopcm1`, with status 0, so a runner finds
the stops by their text.

**Checks in the suite** (`make check`). The parts of the model that compile on their own are built from the series
on the pinned archive, before the patch that changes them and after it, under CM1's OpenMP flags and under
`-O3 -march=native` (`python/climate/tests/test_cm1_world.py`).

| Check | Result | Evidence state |
|---|---|---|
| The series on the pinned archive | The sources of `expected-series.sha256`, with every Terluna build still reproduced (`models/check_patches.sh`) | The patches apply |
| The patches' texts | Each of the five entries is declared, given its default, listed in `&param3`, broadcast, checked and printed. The series before patch 06 reads a macro in five files; its end reads them in `cm1.F`, for the defaults, and in `module_ra_etc.F`, for the constant of MYNN and MYJ. `set_constants`, RRTMG's two initialisations and two drivers and the CAPE diagnostic's three calls take the namelist's values, and RRTMG's modules import `cp` alone from `module_model_constants` | Each read of a compiled value is found and replaced, by the sources' text |
| Earth's gravity as a number | The scan above: sixteen of the 91 files, the five the series accounts for and the eleven the registry refuses, each named in `cm1-earth-g-schemes` | Each gravity written as a number in the patched source is accounted for |
| The constants | `set_constants` gives `g` the bits of the gravity it is handed and `govtwo` half of it, at 9.81, the Moon's 1.6242, 3.72 and 24.79 m/s²; test cases 4 and 5 keep 9.81 | The entry reaches CM1's `g` |
| The CAPE diagnostic | On four soundings and the three source parcels, the diagnostic handed its gravity returns the bits of the diagnostic with that gravity compiled in, at 9.81 m/s² and at the Moon's, under both flag sets. For the surface parcel and the most unstable one, the Moon's CAPE and CIN equal Earth's to 2 parts in 10⁴ and each height stands 6.04 times as high | One build for every world, of the diagnostic; effect |
| One column of RRTMG | A cloudy sunlit column of each world, through the longwave and the shortwave as `radiation_driver.F` calls them: RRTMG handed the gravity, CO2 and O2 returns the bits of RRTMG with them compiled in, in the heating rates of every level and the fluxes at the top and at the ground, with cloud and clear, at CM1's gravity in the macros' default air (40 levels) and at the Moon's gravity in the Open Moon's air (60 levels), under both flag sets; the build for Earth returns other bits on the Moon's column. In a clear column of Earth's air, twice the CO2 lowers the longwave leaving the top by 4.4 W/m², air without O2 lets 5.4 W/m² more sunlight reach the ground, beside 599 W/m², and the Moon's gravity on the same pressures lowers the outgoing longwave by 56 W/m² and the sunlight at the ground by 198 W/m² | Identity at the default and one build for every world, of RRTMG's two schemes; effect |
| One column of Morrison's scheme | The column of patches 03 to 05, built at the series' end, where its gravity comes through `world_g` and `set_constants`: the storm column and twelve random ones return every field bit for bit as before the lab's rain patches, at the Moon's gravity and at 9.81 m/s², under both flag sets (`python/climate/tests/test_cm1_rain.py`) | The entry reaches Morrison's scheme; identity at the default |
| The Sun | The block of `radiation_driver.F` that sets the Sun, compiled from the series before patch 08 and from its end in a program that declares what it reads. At the default the zenith cosine, the hour angle and the sunlight keep their bits in a box, on a ring of latitude and on a tilted ring, under both flag sets, and the equinox's loop keeps its text. With a declination the zenith cosine follows sin(lat) sin(δ) + cos(lat) cos(δ) cos(hour angle) to 2 parts in 10⁶ of one, for five declinations from −25.19° to 60°, north and south of the equator; at the lab's sunrise hour angle the Sun stands on the horizon; and round a circle at 80° N it stays up through a summer's day and down through a winter's | Identity at the default; effect, against the spherical formula and the lab's own sunrise |
| The soil | The lines of `init_surface.F` that lay out the layers, compiled from the series before patch 07 and after it: at the default they return core patch 08's layers bit for bit under both flag sets, and handed a top layer they return five layers doubling from it, 1 to 16 cm from CM1's own 0.01 m and 5.4 to 86.9 cm for the Open Moon's day | Identity at the default; effect |
| The registry | B1 names patch 06 and `world_g` beside the build constant and stays `require-build`; `cm1-soil-day` and `cm1-equinox-sun` name patches 07 and 08 with their entries and defaults; the refused schemes include MYJ, CM1's own NSSL and the GSFC LFO scheme (`lab/tests/test_spec.py`) | The registry's entries are as recorded |

**Checks run once**, on 11 November 2026, with gfortran 13.3.0 on an Intel i9-11980HK, one thread to a run. Each is
a single run from scratch scripts and builds on the project drive, which stay outside the repository and the suite
(`world-crafting-research/tmp/port-namelist-world/tools/`: `make_patches.py`, `builds.sh` and `case_runs.py`, with
their logs in `tmp/port-namelist-world/logs/`), on the sources of `expected-series.sha256`.

| Check | Result | Evidence state |
|---|---|---|
| The whole model | Twelve builds compiled and linked, each under CM1's OpenMP flags and under `-O3 -march=native`: the series before the three patches and after each of them, at CM1's own gravity and air; and the series before them and at its end with the Moon's gravity and the Open Moon's CO2 and O2 compiled in as Terluna's builds have them (`-DTERLUNA_G=1.6242188765608128 -DTERLUNA_CO2=4.000000e-04 -DTERLUNA_O2=0.174579`) | The sources compile |
| CM1's released case at the defaults | The supercell of patches 03 to 05 (125 steps of 12 s). Its ten output files, the fields at the start and after 1,500 s, the statistics and the metadata, agree byte for byte between the series before the three patches and the series after each of them, under both flag sets | Identity at each patch's default, of a compiled case of CM1's own |
| A case in which each changed place runs, at the defaults | That supercell with RRTMG every 300 s, the MM5 surface layer over land with the slab soil, core patch 05's Sun (a solar day of 86,400 s at 1,361 W/m², from an hour angle of −60° at 36.68° N) and CAPE, CIN, LCL and LFC in its output. By 1,500 s the storm holds rain, graupel and cloud ice, the ground has warmed from 299.3 K to between 300.3 and 302.1 K, and the CAPE field reads 1,329 to 2,017 J/kg. Between the series before the three patches and the series after each of them, under both flag sets, every field of the ten output files agrees bit for bit but `z0t` and `z0q`, two diagnostics that CM1's surface layer leaves unset over land (Limits) | Identity at each patch's default, of a compiled case that runs RRTMG, the soil, the Sun and the CAPE diagnostic |
| The entries in that case | The model reads the five entries from `&param3` and prints them. The defaults, stated in the namelist, return the default's output bit for bit. A `world_g` of 9.80665 m/s², twice the CO2, air without O2, a `soil_dz1` of 0.01 m and declinations of 20° and −20° each change the output: RRTMG prints the gravity and the CO2 it took, the soil's layers print as 1 to 16 cm, and the zenith cosine that the model prints at its first radiation call and writes at 1,500 s equals the formula by hand to 1 part in 10⁷, at both declinations | The namelist's entries act in a compiled case |
| The stops in that case | A `world_g` of zero, a negative `world_co2`, gases above one together, a `soil_dz1` of zero, a `sun_decl` of 100°, a `sun_decl` without the solar day, test case 4 at 9.80665 m/s², and MYNN and MYJ at 9.80665 m/s² in a build that holds 9.81 each end the run as it starts with the patch's message; MYNN at the build's gravity runs | The model stops on the values it cannot take |
| One build for every world, on a lunar ring | Three hours of Terluna's 45° N ring (`ring_45n_corrected`: 1,288 columns and 111 levels in two dimensions, RRTMG, the MM5 surface layer over land and sea, the simple boundary layer, nudging and the large-scale vertical wind), from its restart 38, nineteen days into the run, with its own inputs as test input; rain reaches 2.5 g/kg within the three hours, and the ring spans night and day. The build of the whole series without macros, told the Moon by its namelist (`world_g = 1.6242188765608128`, `world_co2 = 4.000000e-04`, `world_o2 = 0.174579`), returns the 23 files of the build of the series before the three patches with the Moon compiled in, byte for byte: the fields, the domain's diagnostics and the statistics at each hour, 59 MB with the six restart files written at the end. So does the build of the whole series with the Moon compiled in and the namelist silent. Both hold under CM1's flags and under `-O3 -march=native`. The build without macros, its namelist silent, stops at its first step on a Courant number of NaN, the lunar state under 9.81 m/s² | One build for every world, and identity at the default of a build with the Moon compiled in, of a compiled lunar case; every bit of the output and of the restart agrees |

The ring took 92.4 s of wall time with the Moon compiled in and 92.7 s with the Moon in the namelist under CM1's
flags, and 91.0 and 90.3 s under `-O3 -march=native`, each a single run beside two others on a busy machine. The two builds' times lie within
1% of each other in these readings, which stage 3's best of three is to test.

**Limits.**

- The lab's adapter still compiles the world in (`world_constants = "build"` in `lab/configs/cm1/defaults.toml`,
  registry B1). Plan stage 3 asks of the namelist build one-day ring segments at the Moon's values and at
  9.81 m/s², and a wall time within 2% of the compiled build's, timed best of three on a quiet machine; the runs
  above cover three model hours of a ring and 25 minutes of a supercell, each made once, and their wall times are
  single readings.
- The electrified series' NSSL keeps the build's gravity: its patch 03 reads `TERLUNA_G` in the scheme's fall speeds
  and ventilation, where the lab's patch 06 leaves it. An electrified build therefore compiles its gravity in until
  a companion patch hands NSSL the namelist's, and the lab's series was checked on the core series alone.
- MYNN's boundary layer and MYJ's boundary layer and surface layer hold the build's gravity, and the schemes that
  write Earth's gravity as a number hold Earth's; the model stops on the first group where `world_g` differs from
  the build's value, and the registry refuses both groups at another gravity. The scan finds numbers: the
  fall-speed fits of the microphysics other than Morrison's hold Earth's gravity without one.
- A macro and an entry can both state a value, and the entry then takes the run. A value in the namelist becomes the
  single-precision number nearest its decimal, as a macro's does when it compiles, so nine significant digits fix
  it.
- The trace gases other than CO2 and O2, and ozone, stay at zero in every build (core patches 06 and 07), so an
  Earth case runs without them until a later patch reads them from the namelist too.
- The soil's layers are laid out at each start and stay out of the restart files, so a case keeps one `soil_dz1`
  over its segments. The effect of the layers on a run is unmeasured.
- The declination holds through a run, so a case that spans a season restates it with each segment; the hour angle
  takes no equation of time, as before. At the default the declination CM1 writes among its diagnostics
  (`rad_declin`) stays the one CM1 computes for the calendar date, as core patch 05 leaves it, and with a
  `sun_decl` it is the namelist's. The effect of a declination on a run is unmeasured.
- The CAPE diagnostic averages its mixed-layer parcel over the lowest 500 m at every gravity (`notes/cm1.md`, "The
  CAPE diagnostic's mixed layer"), and CM1's MM5 surface layer leaves its `z0t` and `z0q` diagnostics unset over
  land (`notes/cm1.md`, "The MM5 surface layer's roughness diagnostics over land"); the patches change neither.
- Each rank of an MPI build takes the five entries by broadcast, lines that the OpenMP builds leave uncompiled.
- The identity and the agreement of the two builds were run with gfortran 13.3.0 on one processor that has fused
  multiply-adds, one thread to a run; the suite's parts repeat them under both flag sets wherever the suite runs.

### The wind's own nudging and the inflow (patch 09)

**Why.** CM1's large-scale nudging (`lsnudge`, `&param19`) relaxes the domain-mean wind, potential temperature and
vapour toward a series of profiles on one time, `lsnudge_tau`, and pulls the wind at every level. A box forced
through the whole column (`python/climate/crm/gcm_site.py`) holds its air to the GCM's above the GCM's convection on
three days, while its wind's target changes with each window of local time, every 0.82 days on the Moon; on the
three days Terluna's sea box kept its mean wind at 44–67% of its target's speed. On 28 October 2026 Terluna gave its
site boxes three changes, compiled into its build `moon_omp_rain_law_pbl_wind_gust_aloft_inflow` and read through
CM1's spare reals: the wind's own time (`WIND_TAU_PATCH`, `var10`), its pull from a height up (`WIND_ALOFT_PATCH`,
`var8`) and the inflow of the reference's air where the mean wind converges (`INFLOW_PATCH`, `var7`), each recorded in
Terluna's `climate/crm/README.md` at `39c5ee04` with its trials (238638f, 3dd0c96, 191d967). Patch 09 reads the three
as named entries of `&param3`, whose defaults keep CM1's nudging.

**The entries.**

| Entry | Unit | Default | With a value | A forced box (`gcm_site.case_inputs`) |
|---|---|---|---|---|
| `wind_nudge_tau` | s | 0: the wind relaxes on `lsnudge_tau` | The domain-mean wind's nudging in `solve1.F`, and the base-state and geostrophic wind in `solve3.F`, relax on this time; θ and vapour keep `lsnudge_tau` | 7,200 s, Terluna's 2 hours, the time on which cloud-resolving runs forced by observations relax their mean wind (Khairoutdinov, Randall and DeMott 2005), a tenth of the Moon's window of local time |
| `wind_nudge_zmin` | m | 0: every level | The domain-mean wind's tendency is nil at the levels below this height, which the box's surface layer and turbulence shape; `solve3.F`'s relaxation acts at every level | The GCM's lowest level, to 0.1 m, below which the windows repeat that level's wind: 317.6 m over the Near-side Sea on the design run's own constants, 316.1 m on Terluna's |
| `inflow_ref_air` | 0 or 1 | 0 | Each level's domain-mean θ and vapour gain max(d(ρ₀w)/dz, 0)/ρ₀ × (reference − domain mean) | 1 |

**What the patch does.** In `solve1.F` the time on which the wind relaxes, `lsnudge_tau` or a positive
`wind_nudge_tau`, divides the domain-mean wind's departure from its target, and the wind's tendency is set to nil at
the levels whose height, `zh` of the first column as CM1's nudging reads its levels, lies below `wind_nudge_zmin`;
θ and vapour, held from `var14` to `var15` by core patch 09, keep `lsnudge_tau`. With `inflow_ref_air` = 1 a block
after the nudging of vapour, inside the large-scale nudging, adds to each level's θ and vapour the rate
max(d(ρ₀w)/dz, 0)/ρ₀, the convergence `wsub` forms in `adv_routines.F` from `wprof` and CM1's base-state density, times
the nudging reference less the domain's mean. CM1's large-scale vertical advection (`wsub`) is the flux form less the
scalar times that convergence, so the air the convergence draws in carries the domain's own mean; the added term gives
it the reference's, the upwind value of coupled columns (Daleu, Woolnough and Plant 2012, their equation 9), and the
air that leaves keeps the domain's own. The term vanishes while the domain's air is the reference, so the day–night
table's added-back advection still cancels at the start. The block writes its rates to `lab_inflow_rate.txt` as each
run starts, the level count and then each level's height (m) and rate (s⁻¹), and prints a line that begins
`Lab: the mean wind draws in`.

**The lab's form.** The code the patch adds to `solve1.F` is Terluna's under the lab's names, and the patch departs
from Terluna's edit lists in three places.

- In `solve3.F` CM1's nudging of the wind also relaxes the base-state wind `u0` and `v0`, from which the large-scale
  pressure gradient follows under `lspgrad = 1` (Terluna's boxes), and the geostrophic `ug` and `vg`
  (`lspgrad = 2`), toward the same target on `lsnudge_tau`. Terluna's `WIND_TAU_PATCH` leaves them there, so its boxes
  pull the mean wind on 2 hours while the pressure gradient's wind follows on 3 days, and the Coriolis force acts on
  the difference. The patch relaxes them on the wind's own time, at every level, the pull's height aside, since the
  large-scale pressure gradient below the GCM's lowest level is that level's. On the sea box's windows the 3-day lag
  averages 1.46 m/s, which at the site's f of −4.6 × 10⁻⁷ s⁻¹ turns the mean wind 0.005 m/s off its target, and at
  Earth's 45° would hold it 0.87 m/s off, by estimate (defect log C25).
- The model stops as it starts on settings it cannot take, where Terluna's lists read the slots unchecked and its
  inflow stood still unless its conditions held: a `wind_nudge_tau` other than 0 below the step `dtl`, or below zero;
  a `wind_nudge_zmin` below zero; either set where `lsnudge` nudges no wind; an `inflow_ref_air` other than 0 and 1;
  and an inflow without `lsnudge`'s θ and vapour and `imoist` = 1, or without one profile of large-scale vertical
  wind, `var13` = 1 or one of CM1's test cases 3 to 7 (the wind by column of core patches 10–14, `var13` = 2, is
  refused). Each stop prints a line that begins `Lab nudging:` and ends the run through `stopcm1`. The inflow keeps a
  guard on `dolsw`, which test case 10's nudging turns off as it runs.
- The identifiers, the comments and the rates' file name are the lab's; no number of a world is compiled in.

**Checks in the suite** (`make check`; `python/climate/tests/test_cm1_nudging.py`, with the forcing's entries in
`python/climate/tests/test_gcm_site.py`). The large-scale nudging of `solve1.F` and the relaxation of `solve3.F`,
taken from the series before patch 09 and after it, compile together in one program that steps them on a domain's
means without dynamics, under CM1's OpenMP flags and under `-O3 -march=native`.

| Check | Result | Evidence state |
|---|---|---|
| The series on the pinned archive | The sources of `expected-series.sha256`, with every Terluna build still reproduced (`models/check_patches.sh`) | The patches apply |
| The patch's texts | The three entries are declared, given their defaults ahead of the namelist's reading, listed in `&param3`, broadcast, checked and printed. The patch removes four lines, the wind's two divisions by `lsnudge_tau` in `solve1.F` and the relaxation's two in `solve3.F`, and adds the rest; the inflow stands after the nudging of vapour and forms `wsub`'s own convergence; no added line holds a world's number or a Terluna name | Each line the patch changes is found |
| The nudging at the defaults | Every tendency, every mean stepped by them and the relaxed base-state and geostrophic wind keep their bits after the patch, on four random domains, one step on tendencies already set and twenty from nil, with the wind's nudging off and with the large-scale vertical wind off, under both flag sets | Identity at the default |
| The wind's own time | With `wind_nudge_tau` 7,200 s the wind's tendency is its departure from its target over 7,200 s to 1 part in 10⁵, θ's and vapour's keep their bits; stepped 36 times on 200 s the means, `ug`, `vg`, `u0` and `v0` approach their targets by (1 − dt/τ)ⁿ, 0.36 in two hours, where the defaults' three days leave 0.97, and θ keeps its three days under core patch 09's weight | Effect, against hand arithmetic |
| The pull's height | At the levels below `wind_nudge_zmin` the wind's tendencies are nil and the stepped means stand; at that level and above they are the pull from the ground's, bit for bit; θ and vapour and `solve3.F`'s relaxation are the same at every level, under both flag sets | Effect |
| The inflow | On the mean vertical wind `gcm_site` writes for a moist column under the Moon's gravity and CM1's base-state density from its air: the rates written once match the convergence by hand on the block's inputs to 1 part in 10⁵ of the largest and, by Terluna's own check, the rates reckoned from the file's wind and the air's density at the w levels within 2% at every level where they exceed 1% of the largest (Terluna's trial: within 3%, found 0.983–1.020), and stand at zero where the flow diverges; θ and vapour gain the rate times the reference less the mean in every column; nothing while the domain's air is the reference or the large-scale vertical wind is off; stepped 90 times the low air comes toward the reference by (1 − rate dt)ⁿ | Effect, against hand arithmetic and an independent reckoning |
| The stops | `param.F`'s five checks, compiled alone: sixteen settings the model cannot take stop it with their message, and six it can take run, a box as `gcm_site` writes it, the defaults and test case 5's inflow among them | The model stops on the values it cannot take |
| The forcing's entries | `case_inputs` writes `&param3` with 7,200 s, the GCM's lowest level to 0.1 m and the inflow on by default, a case's stated values in their place, the record of each, the time's share of a window and the refusals of a time of zero or less and of a height outside the box; on Terluna's design run read in place, the values Terluna's set-up gave the sea box's `var10`, `var8` and `var7` | The forcing writes the entries |

**Checks run once,** on 16 November 2026, with gfortran 13.3.0 on an Intel i9-11980HK, one thread to a run. Each is
a single run from scratch scripts and builds on the project drive, which stay outside the repository and the suite
(`world-crafting-research/tmp/port09/tools/`: `builds.sh`, `case_runs.py`, `terluna_block.py` and `mutations.py`,
with their logs in `tmp/port09/logs/`), on the sources of `expected-series.sha256`.

| Check | Result | Evidence state |
|---|---|---|
| The whole model | Four builds compiled and linked without macros, the series before patch 09 and after it, each under CM1's OpenMP flags and under `-O3 -march=native` | The sources compile |
| CM1's released cases at the defaults | CM1's released supercell (125 steps of 12 s) and the world case of patches 06 to 08, that supercell with RRTMG every 300 s, the MM5 surface layer over land with the slab soil, core patch 05's Sun and CAPE in its output, between the series before patch 09 and after it: the supercell's 10 files agree byte for byte under both flag sets, and the world case's 10 byte for byte under `-O3 -march=native` and bit for bit under CM1's flags in every field but `z0t`, which CM1's surface layer leaves unset over land; the model prints the three entries at their defaults | Identity at the default, of compiled cases of CM1's own |
| A lunar box at the defaults | Three hours of a box of 8 × 8 columns of 6 km on the 111 levels of Terluna's `box_near_side_sea_design_years`, told the Moon by its namelist, forced through `gcm_site` from Terluna's design run `A28R_301k_design_l15_snow_s934`, years 10–19, read in place, at the Near-side Sea on the run's own constants: the table, the mean vertical wind, the held air from 94.7 km and CM1's large-scale nudging toward the window's wind and air, with RRTMG, the MM5 surface layer over the sea and Morrison's rain. Its 28 output and restart files agree byte for byte between the series before patch 09 and after it, with the entries silent and with their defaults stated, under both flag sets | Identity at the default, of a compiled forced box |
| The entries in that box | The model prints the three. With the entries as `gcm_site` writes them, 7,200 s, 317.6 m and the inflow on: the rates CM1 writes match those reckoned, by Terluna's check, from `terluna_wls.txt` and the first output's domain-mean density to 0.9978–1.0021 at the 48 levels where they exceed 1% of the largest, and stand at zero where the flow diverges; the largest is 7.4 × 10⁻⁷ s⁻¹ at 9.3 km, and the low inflow reaches 1.2 km. Over the three hours the domain-mean wind's distance from its target falls to 0.22 of its start at 4.8 km and 0.30 at 950 m, against 0.95 and 0.96 on the defaults' three days; with the pull from the ground it falls to 0.31–0.33 at 50–250 m, and with the pull from 317.6 m to 0.53–0.67 there, the levels the box's own surface layer and turbulence shape. Both flag sets give these to the digits shown | Effect in a compiled forced box; three model hours, read as a test of the code |
| The stops in the compiled model | In that box under CM1's flags, seven settings each end the run as it starts with its `Lab nudging:` line: a wind's time of 20 s under the 40 s step, a pull's height of −1 m, an inflow of 2, the wind's entries with the wind's nudging off, and the inflow without the vapour nudged, without the large-scale vertical wind (`var13` = 0) and with the wind by column (`var13` = 2); the box as `gcm_site` writes it runs | The model stops on the values it cannot take |
| Terluna's deployed block | The large-scale nudging of `solve1.F` from Terluna's build `moon_omp_rain_law_pbl_wind_gust_aloft_inflow` (research drive, `cm1/build/`, `solve1.F` sha256 `75b558a8a40749f1…`), its `var10`, `var8` and `var7` given the lab's three values, and the lab's, each in the suite's program with CM1's own `solve3.F`: every tendency, stepped mean and written rate agree bit for bit in 120 runs under each flag set, on six random domains and the inflow's column, at the defaults, the wind's time, its time and height, all three and the inflow alone. With the lab's `solve3.F` the base-state and geostrophic wind alone differ, wherever the wind's time is set | The lab's code is Terluna's where the forms agree |
| Wrong statements | 33, put one at a time into a copy of the patch (28, each a line replaced so that the patch still applies) and of `gcm_site.py` (5): each fails the suite's tests, and each fails them again with the tests of the patch's text left out, 20 by the compiled nudging, 8 by the compiled stops and 5 by the forcing's case | The suite's tests find each fault put in |

**Limits.**

- The checks test the code. The box ran three model hours on 64 columns, and no lab run has read a forced box as a
  study; that waits for the case writer of `PLAN.md`'s block 2 and the author's word. Terluna's measured effects are
  Terluna's runs: relaxed on 2 hours its sea box's mean wind at 0.3 km rose from 1.44 to 2.49 m/s within three hours
  against a target of 3.24; pulled from the GCM's lowest level up, its 50 m wind fell to 0.92–0.93 of the 0.3 km wind
  where the pull to the ground held 1.00–1.02; and with the GCM's air drawn in, its column dried 0.30 mm/day over a
  lunar day where it had dried 0.67.
- The inflow draws in the windows' air, the GCM's mean air at the site, at rates from CM1's base-state density; the
  domain's density departs from the base state as the box's air does, by 0.2% in the box above and by up to 2% in
  Terluna's trial.
- The rates are written once a run, as the large-scale vertical wind stands through it. A box budget reckons the inflow
  from them against the nudging window CM1 holds at each output (Terluna's `box_budget`, `4f63c439`); that reckoning
  waits for the lab's box budget, and every window `gcm_site` writes holds one air.
- 2 hours is a tenth of the Moon's window of local time. A world whose solar day is short has short windows, 40 minutes
  for 36 windows of Earth's day, which the wind follows less closely on 2 hours; `gcm_site` records the time's share
  of a window, and a world's own time is a setting its study states.
- The pull's height compares the first column's heights, as CM1's nudging reads its levels; CM1 refuses the
  large-scale vertical wind over terrain, so the inflow runs on flat ground alone.
- Each rank of an MPI build takes the three entries by broadcast, lines the OpenMP builds leave uncompiled, and the
  domain's means the inflow reads are CM1's own across the ranks.

### The box's own large-scale vertical wind (patch 10)

**Why.** A box forced through the whole column (`python/climate/crm/gcm_site.py`) takes the GCM's mean vertical wind
as given, so much of its free troposphere's temperature comes from motion the GCM supplied, and the moisture its
storms draw in follows the GCM's ascent. On 5 November 2026 Terluna let its site boxes make their own large-scale vertical
wind by the damped gravity wave (Kuang 2008; Blossey, Bretherton and Wyant 2009), in its build
`moon_omp_rain_law_pbl_wind_gust_aloft_inflow_dgw`, which read the wave's settings from CM1's spare reals
(`DGW_PATCHES`, `var9` and `var4` to `var8`; `climate/crm/cm1_run.py` at `29af5c16`, from c3898a7c). Making its own
ascent, Terluna's sea box rained 1.6–1.7 mm/day after midnight where under the imposed ascent it rained about 0.2,
against the GCM's 1.21, so the night gap on which Terluna's redesigns of the convection rested depends on the coupling; the next test of
the yardstick runs three sea boxes, the wave against another box's own domain mean by local time (the test of
self-consistency of Edman and Romps 2015), a weak-temperature-gradient coupling, and the wave at the planet's scale
(`PLAN.md`, "Decisions", 17 November 2026). Patch 10 reads the wave's settings from named entries of `&param3`, whose
defaults keep the wind CM1 imposes.

**The entries.**

| Entry | Unit | Default | With a value | A coupled box (`gcm_site.case_inputs`, coupling `'dgw'`) |
|---|---|---|---|---|
| `lsw_coupling` | 0 or 1 | 0: CM1's own `wprof`, from `terluna_wls.txt` (`var13` = 1) or a test case | 1: the damped gravity wave sets `wprof` each step | 1 |
| `lsw_tau` | s | 0 | τ, the first baroclinic mode's adjustment time, the length the box stands for over the mode's speed, so that k²/ε = 1/(τc²); `dtl` or more | The site's footprint over the mode's speed, to 0.1 s: 10,303.0 s at the Near-side Sea on Terluna's design years with Terluna's constants (418 km at 40.53 m/s), 10,243.5 s on the run's own |
| `lsw_mode_speed` | m/s | 0 | c, the first baroclinic mode's speed | `first_mode`'s over the run's tropics, to 1 mm/s: 40.534 m/s, 40.771 on the run's own constants |
| `lsw_top` | m | 0 | The lid: ω is nil from the first w level at or above it | The GCM's convection top at the site, to 0.1 m: 73,084.5 m, 73,422.4 on the run's own constants |
| `lsw_base` | m | 0 | The lowest height of the coupled layer's base, which is the domain-mean boundary layer's depth held between it and the lid | The GCM's lowest level, to 0.1 m: 316.1 m, 317.6 on the run's own constants |
| `lsw_table_heat` | 0 or 1 | 0: the table (`var11`) heats every level | 1: the table heats below the base alone, and moistens every level | 1 |

**What the patch does.** Just before `solve1`, `cm1.F` averages CM1's boundary-layer depth `hpbl` over the domain's
columns, summing every rank's under MPI, and `solve1.F` takes the mean, held between `lsw_base` and `lsw_top`, as the
coupled layer's base. Inside CM1's large-scale nudging, after the domain's means and the nudging of vapour and before
patch 09's inflow, a block forms T_v′ = π₀ (θ̄ (1 + 0.608 q̄) − θ_r (1 + 0.608 q_r)) at the scalar levels between the
base and the lid's w level, the reference r being the nudging window CM1 holds, and solves d²ω/dp² = R_d T_v′/(τ c² p)
on the w levels between the ground and the lid by a tridiagonal sweep, on the base state's pressures (at w levels the
geometric means of the scalar levels', at the ground and the top extrapolated in log pressure), T_v′ averaged onto the
w levels; at the w levels below the base the source is nil and ω falls linearly in pressure to the ground. `wprof` =
−ω/(ρ₀ g), which `solve1.F` now takes as `intent(inout)`, carries the wave's wind through CM1's large-scale vertical
advection and patch 09's inflow. With `lsw_table_heat` = 1 core patch 17's table heats below the base alone. The model
prints `Lab: the damped gravity wave; its lid (k, z) =` as the wave first runs, and writes `lab_lsw_means.txt`: for
each interval of CM1's domain diagnostics, at the step that ends it, and for the interval that the run's last step
ends, a line of the interval's start and end (s), its steps, the base's mean height (m) and the level count, then at
each level zh and zf (m), the wind at zf (m/s), the inflow's θ (K/s) and vapour (kg/kg/s) tendencies and the table's
heating (K/s) and moistening (kg/kg/s) as applied, each the mean over the interval's steps. A run that starts afresh
replaces the file, and a restarted run adds to it.

**With patch 09.** The wave sets `wprof` before patch 09's inflow reads it, so the inflow's rate,
max(d(ρ₀w)/dz, 0)/ρ₀, follows the box's own convergence step by step and draws the window's air in where the wave
gathers air; with the wave's ω nil at the ground and the lid, the air drawn in equals the air sent out. CM1's
large-scale vertical advection carries the box's mean wind as it carries θ and vapour, so the wave's ascent and
descent move the wind between levels, and the wind's own nudging, on 2 hours from the GCM's lowest level up in a box
as `gcm_site` writes it, pulls it back toward the window's wind. The held air above the GCM's convection, nudged on 3
days from the GCM's first level above that top, lies above the wave's lid, which `gcm_site` sets at the convection's top.

**The lab's form.** The wave's arithmetic is Terluna's statement for statement, and in the suite's driver the lab's
block returns every tendency, stepped mean and wind of Terluna's deployed block bit for bit where the settings coincide
(below). The form departs from Terluna's in five places.

- The record writes each interval at the step that ends it, and the run's last at its last step. Terluna's build wrote
  an interval at the first step past its end, so each run segment lost its last interval (1 in 8 with one-day segments
  and 3-hour intervals, which Terluna's `box_budget` estimated from their neighbours, 3d42c797), its intervals ended one
  step after the domain diagnostics', and the table's heating of the step that wrote an interval fell into the next.
  The lab's record also states each interval's start, so a segment's partial intervals show, and holds the table's
  moistening as applied.
- The base reads the boundary layer's depth from the array CM1 keeps in its restart files, just before `solve1`.
  Terluna's build averaged it in `turb.F` as the surface layer ran, which a restarted run skips at its first step, so
  the first step of each segment took the base at its floor, 316 m where the sea box's boundary layer stood 1.3–4.5 km
  deep, and a restarted run parted from the run it continued. With the lab's form a wave box restarted after an hour
  writes the outputs, restart files and record of the box run whole, byte for byte (below). Under MPI the lab's mean
  sums every rank's columns, where Terluna's took one process's.
- The wave runs with the inflow on or off. Terluna's ran only with its inflow (`var7` = 1), lsnudge's θ and vapour and
  moisture, and otherwise left the imposed wind in place unannounced; the lab's model stops as it starts on settings it
  cannot take: a coupling other than 0 and 1; the wave's entries set with the coupling at 0; a time below `dtl`, a
  speed of zero or less, or a lowest base below the ground or at or above the lid; an `lsw_table_heat` other than 0
  and 1, or 1 without the table; and a wave without lsnudge's θ and vapour, without `imoist` = 1 or without one
  profile of large-scale vertical wind (`var13` = 1 or one of CM1's test cases 3 to 7). The block itself stops on a lid
  at or below the first w level above the ground. Each stop prints a line that begins `Lab coupling:`.
- The entries are the wave's own. Terluna's `var8` served both the wind's pull from the GCM's lowest level and the
  wave's floor; the lab's `wind_nudge_zmin` and `lsw_base` are two entries, which `gcm_site` sets alike by default.
  The table's cut is an entry too, so a case can apply the table's heating at every level, as a test of self-consistency
  may need.
- The identifiers, the comments and the record's name are the lab's, and no number of a world is compiled in.

**How the weak temperature gradient joins.** The entries name the coupling, its time, its lid and its base, and the
base's depth, the record, the table's cut, the reference and the stops serve any coupling of a box's wind to its
departure from the reference. Patch 11 adds the weak temperature gradient as `lsw_coupling` = 2 in a branch beside the
wave's, with one entry of its own, and `gcm_site.case_inputs` writes it for coupling `'wtg'` ("The box's own
large-scale vertical wind by the weak temperature gradient", below).

**Checks in the suite** (`make check`; `python/climate/tests/test_cm1_coupling.py`, with the forcing in
`python/climate/tests/test_gcm_site.py`). The part of `solve1.F` from CM1's large-scale nudging through core patch 17's
table and the wave's record, taken from the series before patch 10 and after it, compiles in one program that steps it
on a domain's means without dynamics, under CM1's OpenMP flags and under `-O3 -march=native`.

| Check | Result | Evidence state |
|---|---|---|
| The series on the pinned archive | The sources of `expected-series.sha256`, with every Terluna build still reproduced (`models/check_patches.sh`) | The patches apply |
| The patch's texts | The six entries are declared, given their defaults ahead of the namelist's reading, listed in `&param3`, broadcast, checked and printed; `cm1.F` averages the depth over every rank just before `solve1`; the wave stands after the nudging of vapour and before the inflow, the table's cut and sums before its heating is added, and the record after the table; the patch removes one line, `wprof`'s `intent(in)`; no added line holds a world's number or a Terluna name | Each line the patch changes is found |
| The coupled part at the defaults | Every tendency, every mean stepped by them and the wind keep their bits after the patch, on three domains, one step on tendencies already set and twenty from nil, with the inflow and the table on and off, the wind's nudging off and the large-scale wind off, under both flag sets; no record is written | Identity at the default |
| The boundary-value problem | With the base at the ground the wave's wind is −ω/(ρ₀g) of the discrete problem solved apart by numpy in double precision, to 1 part in 10⁴ of its largest value, under both flag sets; for ω = A sin(π(p_s − p)/(p_s − p_lid)), whose T_v′ the case sets, it returns that sine within 1% of A on 66 stretched levels | The Fortran solves the problem; the discretisation's error |
| No departure, no wind | The box's mean air at its reference leaves the wind nil bit for bit under CM1's flags; under `-O3 -march=native` gfortran fuses one of the two products θ(1 + 0.608 q) of the departure and rounds the other, and the wind stays below 10⁻⁶ m/s (2.9 × 10⁻⁷ on the test's column, where 0.1 K makes 8.5 × 10⁻³) | Effect; the fused products' residual |
| The first mode's rate | A departure of the operator's first mode, 0.5 K at its peak, rises where warm and sinks where cool, and the wind relaxes it at 1/τ within 5% when `lsw_mode_speed` is that mode's speed, on a lunar column and an Earth column, under both flag sets (Terluna's test, on the compiled block) | Effect, against the eigenproblem |
| Below the base, the ground and the lid | ω is nil at the ground and from the lid's w level up, bit for bit, and linear in pressure at the w levels below the base to 2 parts in 10⁴, with the base at the boundary layer's 2 km and at the floor where the boundary layer lies lower | Effect |
| With the inflow | The column gains the reference's θ and vapour where the wave's wind converges and loses its own where it diverges, under CM1's advection by that wind, to 1 part in 10⁵, and the air drawn in equals the air sent out; the inflow is nil where the wind diverges | The inflow reads the wave's wind; heat, water and air kept |
| The record | Ten steps from 3,600 s with the domain diagnostics at the ends of steps 3 and 7 and the run's end at step 10 give three intervals, 3,600–3,720, 3,720–3,880 and 3,880–4,000 s, of 3, 4 and 3 steps, each the mean over its steps of the wind, the inflow's and the table's tendencies to 1 part in 10⁵, the heating cut above the base; a run ending on an interval's end writes it once, a segment that stops short of an interval's end writes nothing past its last, a fresh run replaces the file and a restart adds to it | The record holds every interval, the run's last included |
| The stops | `param.F`'s seven checks, compiled alone: twenty-one settings stop the model with their message and five run, a box as `gcm_site` writes it and the defaults among them; the block stops on a lid at the first w level and takes the top for a lid above it | The model stops on the values it cannot take |
| The forcing | `site_forcing`'s air, vertical wind and horizontal part by local time, `first_mode` and `footprint_m` by hand on synthetic runs; `case_inputs`' entries, files, start and record for the wave, a case's stated length, time, lid, base, table, reference (a box's domain mean among them) and start, and its refusals; and, where Terluna's research drive is at hand, Terluna's three damped-gravity-wave boxes (below) | The forcing writes the entries |

**On Terluna's design run,** read in place (the tests skip without the drive): with Terluna's constants `first_mode` gives
the speed of Terluna's three boxes, 40.53382926508821 m/s, and `footprint_m` their lengths, 417,621, 418,418 and
353,976 m, to the last bit; the sea box's case takes the values Terluna's set-up gave its slots `var4`, `var5`, `var6`
and `var8` (73,084.5 m, 10,303.0 s, 40.534 m/s and 316.1 m); its 72 windows and its sounding hold Terluna's air to their
printed digits, the vapour once carried into a mixing ratio; and its record holds Terluna's split of the GCM's column
moistening, −2.188 mm/day, −0.220 of it horizontal and −1.968 by the GCM's own vertical wind. Laid on the GCM's mean
air, as Terluna laid it, the table is Terluna's to 1 part in 10⁴ of its largest value; the lab lays it on the box's
starting air, the base state CM1 runs on, which moves it by up to 1.0% of the heating's largest value and 1.5% of the
moistening's, near 650 m. Terluna's rule for the vapour by local time gives its three choices: the sea's lowest level
swings by 4.3% of its mean through the day, under the rule's tenth, and the two land sites' by more. On the run's own
constants the speed comes to 40.77 m/s, 0.58% faster, with the heights 0.47% higher and the potential temperature in the
run's own ratio of gas constant to heat capacity.

**Checks run once,** on 17 November 2026, with gfortran 13.3.0 on an Intel i9-11980HK, one thread to a run. Each is a
single run from scratch scripts and builds on the project drive, removed after the runs, on the sources of
`expected-series.sha256`.

| Check | Result | Evidence state |
|---|---|---|
| The whole model | Four builds compiled and linked without macros, the series before patch 10 and after it, each under CM1's OpenMP flags and under `-O3 -march=native` | The sources compile |
| CM1's released cases at the defaults | CM1's released supercell (125 steps of 12 s) and the world case of patches 06 to 08, between the series before patch 10 and after it: the supercell's 10 files agree byte for byte under both flag sets, and the world case's 10 byte for byte under `-O3 -march=native` and bit for bit under CM1's flags in every field but `z0t`, which CM1's surface layer leaves unset over land; the model prints the six entries at their defaults | Identity at the default, of compiled cases of CM1's own |
| A lunar box at the defaults | Patch 09's box, three hours of 8 × 8 columns of 6 km forced through `gcm_site` from Terluna's design run `A28R_301k_design_l15_snow_s934`, years 10–19, read in place, on the run's own constants, with patch 09's entries as `gcm_site` writes them: its 28 output and restart files agree byte for byte between the series before patch 10 and after it, the new entries silent and stated at their defaults, under both flag sets | Identity at the default, of a compiled forced box |
| The wave in that box | The case as `gcm_site` writes it with the wave, on the run's own constants, starting from the first window's air: the record holds three intervals, 0–1, 1–2 and 2–3 h, of 50, 48 and 48 steps, the last at the run's end, with the base at 2.8–3.2 km; the box's band of 20–60 km falls 0.014 to 0.024 K below its reference and the box sinks, at up to 5.2 mm/s in the interval's mean at 47–49 km by the third hour; at each output the wind CM1 wrote matches the problem solved apart on the box's own mean air, the base state taken from the first output, within 1.0%, 0.5% and 0.3% of its largest value. Both flag sets give these to the digits shown | Effect in a compiled box; three model hours, read as a test of the code |
| A restart | Two hours of the wave box run whole, and one hour run and then restarted for the second: the three outputs, the three domain diagnostics, the two restart files and the record agree byte for byte, under both flag sets; the statistics differ in two words, CM1's step and largest Courant number at the restart's time, alike with the wave off | The wave keeps a restarted run on the path of the run it continues |
| The stops in the compiled model | Under CM1's flags, seven settings each end the run as it starts with its `Lab coupling:` line: a coupling of 2, a time below the step, the entries with the coupling at 0, the table's cut without the table, the wave without the vapour nudged, the wave without the large-scale wind (`var13` = 0) and a lid of 50 m; the box as `gcm_site` writes it runs | The model stops on the values it cannot take |
| Terluna's deployed block | The part of `solve1.F` from the large-scale nudging through the table, from Terluna's build `moon_omp_rain_law_pbl_wind_gust_aloft_inflow_dgw` (research drive, `cm1/build/`, `solve1.F` sha256 `c723f391d1107582…`), its slots given the lab's values and its record left unwritten, and the lab's, each in the suite's driver: every tendency, stepped mean and wind agree bit for bit in 72 runs, 36 under each flag set, on six domains with the inflow and the table on and off, one step and twenty, and the base at the boundary layer's depth and at its floor | The lab's code is Terluna's where the forms agree |
| Wrong statements | 43, put one at a time into a copy of the patch (30, each a line replaced so that the patch still applies) and of `gcm_site.py` (13): each fails the suite's tests, 41 of them with the tests of the patch's text left out; the other two, a wrong divisor and a wrong condition of `cm1.F`'s mean depth, which the compiled tests take as an input, fail the test of the text | The suite's tests find each fault put in |

**Limits.**

- The checks test the code. The wave box ran three model hours on 64 columns, and no lab run has read a coupled box as
  a study; that waits for the case writer of `PLAN.md`'s block 2 and the author's word. Terluna's measured effects are
  Terluna's runs, read on its lunar days 3 and 4: its sea box rained 2.85 mm/day against the GCM's 1.42, 69% of it in
  the afternoon; its land box's own large-scale motion brought it +17.1 mm/day of vapour in the afternoon, against the
  +11.25 that the GCM's vertical advection brought in the design years; and its dry box dried to 2% of the GCM's rain
  under steady descent
  (`session-tools/agents/gap_boxes/yardstick/reading_wtg.md` on Terluna's research drive).
- The mode's speed is the WKB estimate. On Terluna's column the operator's own discrete first mode runs at 43.3 m/s,
  so with the WKB speed the first mode relaxes in 0.875 τ (Terluna's `report_wtg.md`, its calculation, which waits to be
  repeated on a lab box's base state).
- The base takes CM1's boundary-layer depth, which the simple boundary layer finds by the bulk Richardson number
  against a critical 0.125 (defect log B43); on Terluna's land box it swung from 0.06 to 8.4 km over the lunar day.
  Where the base reaches the lid, the scalar levels between `lsw_top` and the lid's w level still feel the departure,
  as in Terluna's block.
- The departure takes the base state's Exner function and pressures and no condensate's weight (Terluna's form, after
  Kuang 2008). Under `-O3 -march=native` the fused products leave a box at its reference a wind below 10⁻⁶ m/s.
- The reference is the window CM1 holds. After a restart CM1 counts its windows again from the first, one a step
  (defect log A12), so a restarted wave box measures itself against earlier windows for as many steps as windows have
  passed: 35 steps, 47 minutes of model time, at the start of Terluna's sea box's thirtieth one-day segment. The fix
  belongs to CM1's nudging and waits for a patch of its own.
- Under the wave, patch 09's `lab_inflow_rate.txt` holds the rates of the run's first step, nil at a start from rest,
  and the record holds the inflow's means. A run that CM1 stops on its Courant number leaves its last interval
  unrecorded. CM1 refuses the large-scale vertical wind over terrain, so the wave runs on flat ground alone.
- Each rank of an MPI build takes the six entries by broadcast and the depth's sum over the ranks, lines that the
  OpenMP builds leave uncompiled.

### The box's own large-scale vertical wind by the weak temperature gradient (patch 11)

**Why.** Under the damped gravity wave Terluna's sea box rained eight times as much after midnight as under the imposed
ascent, and a review of the gap found the two couplings further apart than the two models (`lab/design/gap_series.md`,
section 3). The next test of that yardstick runs sea boxes coupled three ways: the wave against another box's own
domain mean, a weak-temperature-gradient coupling, and the wave at the planet's scale (`PLAN.md`, "Decisions", 17 and
18 November 2026). Edman and Romps (2015) tested both families against a cloud-resolving model's own benchmark. In
radiative–convective equilibrium the weak temperature gradient held the domain's mean motion under 1 mm/s, against a
clear-sky descent near 4 mm/s, at each time they tried, 0.725, 7.25 and 72.5 h, where their damped-wave schemes sank
about 2 mm/s at a length of 1,280 km; under the forcing of ARM's Southern Great Plains it followed the benchmark's rain
more closely than either damped-wave scheme, which over-predicted almost every event, while over TWP-ICE their new
damped-wave scheme followed it best (R² 0.78 against 0.59). Patch 11 adds the weak temperature gradient as
`lsw_coupling` = 2 beside the wave, on the same reference, time, lid, base, table's cut, record and stops. It is the
lab's own: Terluna has no code for it.

**The entries.** One entry is new; the others keep their meaning under the second coupling.

| Entry | Unit | Default | Under the weak temperature gradient | A coupled box (`gcm_site.case_inputs`, coupling `'wtg'`) |
|---|---|---|---|---|
| `lsw_coupling` | 0, 1 or 2 | 0: CM1's own `wprof` | 2: the weak temperature gradient sets `wprof` each step | 2 |
| `lsw_tau` | s | 0 | τ, the time on which the wind relaxes the departure; `dtl` or more | The wave's: the site's footprint over the first mode's speed, 10,243.5 s at the Near-side Sea on the run's own constants, or a time or length the case states |
| `lsw_mode_speed` | m/s | 0 | Unread; any other value stops the run | Left out |
| `lsw_top`, `lsw_base`, `lsw_table_heat` | m, m, 0 or 1 | 0 | As for the wave: the lid, the lowest base, and the table's heating below the base alone | As for the wave: 73,422.4 m, 317.6 m and 1 |
| `lsw_stab_min` | K/m | 0 | γ, the least static stability by which the departure is divided; more than 0. With coupling 0 or 1 any other value stops the run | Edman and Romps's 0.01 K/km times the world's gravity over 9.81 m/s², to three figures: 1.66 × 10⁻⁶ K/m on the Moon, or a value the case states |

**What the patch does.** Inside patch 10's block, after the departure and the wave's branch, the branch for
`lsw_coupling` = 2 finds the first w level above the base, the domain-mean boundary layer's depth held between
`lsw_base` and the lid, and at each w level from there to the last below the lid's w level sets

w = θ_v′ / (τ max(γ, ∂θ_v,r/∂z)),

θ_v′ the domain-mean virtual potential temperature less the nudging window's, the mean of its values at the scalar
levels on either side, and ∂θ_v,r/∂z the window's own virtual stability between those levels. Each θ_v′ is
(θ̄ − θ_r)(1 + ε q̄) + ε θ_r (q̄ − q_r), with ε = R_v/R_d − 1: the wave's departure θ̄(1 + ε q̄) − θ_r(1 + ε q_r) over
π₀, written so that it is nil wherever the box's air equals its reference, fused products or none, where the wave's
form keeps a residual below 10⁻⁶ m/s under `-O3 -march=native`. The stability is formed the same way. There
ω = −ρ₀ g w; below the first level ω falls linearly in the base state's pressure, on the wave's pressures, to nil at
the ground; from the lid's w level up it is nil. `wprof` = −ω/(ρ₀ g) as for the wave, so CM1's large-scale vertical
advection and patch 09's inflow read it, and the record and the table's cut serve it unchanged. The model prints
`Lab: the weak temperature gradient; its lid (k, z) =` as the branch first runs. `param.F` accepts 2 and stops as the
run starts on settings it cannot take: a coupling other than 0, 1 and 2; `lsw_stab_min` set with the imposed wind or
the wave; under the gradient a time below `dtl`, a floor of nil or less, a lowest base below the ground or at or above
the lid, any of them NaN, or a mode speed stated; and, as for the wave, a table's rule other than 0 and 1 or without
the table, and a coupling without lsnudge's θ and vapour, moisture or one profile of large-scale vertical wind. The
block's stop on a lid at the first w level serves both couplings. Each stop prints a line that begins
`Lab coupling:`.

**The form and its sources.** Edman and Romps (2015) give the form they found self-consistent, the
relaxed weak temperature gradient after Raymond and Zeng (2005), read here as eq. 3.4 of chapter 3 of Edman's thesis
(2017), which reprints the paper (sections 3.1–3.4, the text extracted from the thesis's PDF); Daleu et al. (2015) give
the protocol of an intercomparison of single-column and cloud-resolving models (section 3, read in the published
version). Raymond and Zeng (2005) is cited as those two papers report it, unread here.

| Choice | The lab's | Edman and Romps (2015) | Daleu et al. (2015) |
|---|---|---|---|
| Variable | θ_v, the domain mean less the window's, as in the wave's departure | θ_v | θ_v |
| Stability | The reference's ∂θ_v/∂z | The reference's ∂θ_v/∂z | The reference's ∂θ_v/∂p |
| Floor | `lsw_stab_min`; by default 0.01 K/km times g/9.81 | 0.01 K/km | 1 K/km |
| Time | `lsw_tau`: L/c, or stated | L/c with c ≈ 50 m/s: 0.725, 7.25, 72.5 h | 3 h, uniform in height |
| Base | The domain-mean boundary layer's depth, no lower than `lsw_base` (patch 10's) | 1 km | 850 hPa |
| Below the base | ω linear in pressure to nil at the ground | w linear in height to nil at the surface | ω linear in pressure to nil at the surface |
| Top | Nil from the lid's w level, `lsw_top`, by default the GCM's convection top | None stated, in a domain to 32 km | 100 hPa |
| Heat and vapour | CM1's large-scale vertical advection by the wind; with patch 09 the window's θ and vapour drawn in where the wind converges | A mass source with the column's and the reference's θ and vapour averaged into the flow, converging or diverging | Vertical advection; the reference's vapour drawn in where the wind converges |

Besides the transport of heat and vapour (below), the lab's form differs from Edman and Romps's in four places. The
base follows the box's boundary layer, as the wave's does, where both papers fixed an Earth height: a fixed 1 km would
lie inside the lunar sea box's boundary layer of 1.3–4.5 km, and the land box's swung from 0.06 to 8.4 km (defect log
B43). The taper below the base runs linearly in pressure, as for the wave and in Daleu et al.; with the base at 3 km
and a scale height near 50 km it parts from a taper linear in height by 1.5% midway. The floor stretches with gravity
(defect log B44): at a given temperature heights stretch as 1/g and a stability as g, so the floor keeps the share of
the world's stability that 0.01 K/km is of Earth's. And above the lid the wind is nil, so the GCM's held air above its
convection stays under the nudging alone.

**With patch 09.** As under the wave, the wind is set before patch 09's inflow reads it, and with ω nil at the ground
and the lid the air drawn in equals the air sent out. Edman and Romps let both the column's and the reference's air
enter the flow, half of each, whether it converges or diverges; Daleu et al. draw in the reference's vapour alone,
where the wind converges, and patch 09 draws in the reference's θ and vapour there.

**Checks in the suite** (`make check`; `python/climate/tests/test_cm1_wtg.py`, with the forcing in
`python/climate/tests/test_gcm_site.py`). The part of `solve1.F` from CM1's large-scale nudging through the table and
the record, taken from the series before patch 11 and after it, compiles in patch 10's driver under CM1's OpenMP
flags and under `-O3 -march=native`.

| Check | Result | Evidence state |
|---|---|---|
| The series on the pinned archive | The sources of `expected-series.sha256`, with every Terluna build still reproduced (`models/check_patches.sh`) | The patches apply |
| The patch's texts | It follows patch 10 in the same four files and removes only lines of patch 10's: comments that named one coupling, and the checks and messages the second joins, the wave's statements kept; `lsw_stab_min` is declared, given its default ahead of the namelist's reading, listed in `&param3`, broadcast and printed; ten stops; the branch stands after the wave's and before `wprof` is written; no added line holds a world's number, a Terluna name or anything cpp reads | Each line the patch changes is found |
| Identity with the imposed wind and the wave | Every tendency, stepped mean and wind, every printed line and the record keep their bits after the patch, on three domains: the imposed wind one step and twenty, with the inflow and the table on and off, the wind's nudging off and the large-scale wind off; the wave one step and twenty, with the inflow, the table's cut, the record and a base at the lid; under both flag sets | Identity at coupling 0 and 1 |
| The wind against a Python copy | With a departure of θ and of vapour, the base at the boundary layer's 3 km and at its 400 m floor, the wind is the Python copy's to 1 part in 10⁵ of its largest value; nil at the ground and from the lid's w level up, bit for bit; ω linear in pressure below the base to 2 parts in 10⁴; under both flag sets | The Fortran computes the form |
| No departure, no wind | The box's mean air at its reference leaves the wind nil at every level, bit for bit, under both flag sets, from any wind held before | Effect |
| The sign | A warm departure lifts the air at every w level up to the lid and a cool one sinks it, by opposite winds | Effect |
| The rate | A half sine of 0.2 K in θ between the base and the lid, stepped fifty times over τ by CM1's large-scale advection of θ by the branch's wind alone, the vapour at the reference's, falls to e⁻¹ of itself in τ within 5% at its peak and through the column, on a lunar column (base 3 km, lid 60 km) and an Earth column (base 1 km, lid 15 km), under both flag sets | Effect: the wind's advection of the reference's own stability returns the departure on τ |
| The floor | In a reference with a neutral layer, the branch divides by `lsw_stab_min` there and by the reference's stability elsewhere, as the copy does; a floor ten times higher divides the layer's wind by ten and leaves every other level's bits; a floor above every level's stability gives the departure over τ γ throughout | The floor acts as stated |
| The record and the inflow | Patch 10's record holds three intervals of 3, 4 and 3 steps, each the mean wind over its steps; the column draws in as much air as it sends out, the inflow nil where the wind diverges | The record and the inflow serve the gradient |
| The stops | `param.F`'s checks, compiled alone: twenty-nine settings stop the model with their message and six run, the boxes as `gcm_site` writes them under either coupling among them; the block stops on a lid at the first w level, takes the top for a lid above it, gives the gradient the last level alone with the base just under it, and leaves the wind nil with the base at the lid | The model stops on the values it cannot take |
| The forcing | `case_inputs` with coupling `'wtg'`: patch 11's entries, the wave's files, windows, start and other entries, the floor and its source, the first window's least stability by hand from the window's printed air and its count of floored levels, none at the default and all under a floor above every level's stability, a time stated without a mode, a stated floor and Earth's gravity's floor; and its refusals | The forcing writes the entries |

**Checks run once,** on 18 November 2026, with gfortran 13.3.0 on an Intel i9-11980HK, one thread to a run. Each is a
single run from scratch scripts and builds on the project drive, removed after the runs, on the sources of
`expected-series.sha256`.

| Check | Result | Evidence state |
|---|---|---|
| The whole model | Four builds compiled and linked without macros, the series before patch 11 and after it, each under CM1's OpenMP flags and under `-O3 -march=native` | The sources compile |
| CM1's released cases at the defaults | CM1's released supercell and the world case of patches 06 to 08, between the series before patch 11 and after it: the supercell's 10 files agree byte for byte under both flag sets, and the world case's 10 byte for byte under `-O3 -march=native` and bit for bit under CM1's flags in every field but `z0t`, which CM1's surface layer leaves unset over land; the model prints `lsw_stab_min` at its default | Identity at the default, of compiled cases of CM1's own |
| Patch 10's lunar box, imposed and under the wave | The box of patches 09 and 10, three hours of 8 × 8 columns of 6 km forced through `gcm_site` from Terluna's design run `A28R_301k_design_l15_snow_s934`, years 10–19, read in place, on the run's own constants: with the imposed wind, the new entry silent and stated at its default, and under the wave as `gcm_site` writes it, its 28 output and restart files agree byte for byte between the series before patch 11 and after it, the wave's record and the inflow's rates too, under both flag sets | Identity at coupling 0 and 1, of a compiled forced box |
| The gradient in that box | The case as `gcm_site` writes it for coupling `'wtg'` (τ 10,243.5 s, γ 1.66 × 10⁻⁶ K/m, lid 73,422.4 m, lowest base 317.6 m), starting from the first window's air: the record holds three intervals, 0–1, 1–2 and 2–3 h, of 50, 48 and 48 steps, the base at 2.8–3.2 km; at each output the wind CM1 wrote, nil at the ground and from the lid, matches the form applied apart to that output's own mean air and the window's from 3.3–3.9 km to the lid within 1.0%, 0.6% and 0.3% of its largest value, the difference of one step; the box sinks most at 59 km, 12.6 mm/s at the first output and 18.4 at the third, where the window's stability falls to 0.28 K/km, and by the third hour its band of 20–60 km stands 0.009–0.061 K below its reference; under the wave it sank at most 5.2 mm/s, at 47–49 km. Both flag sets give these to the digits shown | Effect in a compiled box; three model hours, read as a test of the code |
| A restart | Two hours of the gradient's box run whole, and one hour run and then restarted for the second: the three outputs, the domain diagnostics, the first restart file and the record agree byte for byte, under both flag sets; the statistics differ in CM1's step and largest Courant number at the restart's time, and the second restart file in one double of CM1's output schedule, 10⁹ + 3,600 against 10⁶⁰, alike with the imposed wind | The gradient keeps a restarted run on the path of the run it continues |
| The stops in the compiled model | Under CM1's flags, six settings each end the run as it starts with its `Lab coupling:` line: a coupling of 3, a floor of nil, a mode speed with the gradient, a floor with the wave, a floor with the imposed wind and a time below the step | The model stops on the values it cannot take |
| Wrong statements | 31, put one at a time into a copy of the patch (23, each a line replaced so that the patch still applies) and of `gcm_site.py` (8): each fails the suite's tests, 30 of them with the tests of the patch's text left out; the other, `lsw_stab_min`'s default in `cm1.F`, which the compiled tests take as an input, fails the test of the text. Two, a search for the base that starts a level low and a count of floored levels held at nil, passed the first tests and are caught by cases added for them | The suite's tests find each fault put in |

**Limits.**

- The checks test the code. No lab run has read a box under the weak temperature gradient as a study; the test of the
  couplings' consistency, the gradient's included, waits for stage 3's case writer and the author's word.
- Edman and Romps's tests ran a cloud-resolving model of Earth's tropics with prescribed radiative cooling, on domains
  of 64 and 128 km at 2 km spacing; the lunar boxes run interactive radiation on 192 km at 6 km. Daleu et al. found
  the weak temperature gradient's equilibria in some models dry or raining by their start, more often over warmer
  seas (their abstract), and their introduction reports its profiles of ascent more top-heavy than the wave's (after
  Raymond and Zeng 2005, Daleu et al. 2012 and Romps 2012); the lunar box above sank most at 59 km.
- Where the box's boundary layer stands below the reference's near-neutral air, the gradient divides by it. On the
  Near-side Sea's first window the GCM's air holds 0.013–0.072 K/km from 0.4 to 2.35 km, where a departure of 0.1 K
  makes 0.14–0.72 m/s; above 2.56 km it holds 0.28–0.91 K/km (defect log B44). Under the wave the sea box's base held
  2.8–3.2 km. CM1's explicit advection carries the gradient's wind into the column, so where the floor binds under
  air more stable than the floor the departure relaxes faster than 1/τ, by the box's stability over the floor; whether
  the step stays stable there is untested.
- The gradient's wind runs up to the last w level below the lid and is nil from the lid's level up, with no taper
  between. A base at or above that last level leaves the gradient no level, and the wind is nil throughout.
- The reference is the window CM1 holds, so after a restart the gradient, as the wave, measures the box against
  earlier windows for as many steps as windows have passed (defect log A12).
- Each rank of an MPI build takes `lsw_stab_min` by broadcast, a line the OpenMP builds leave uncompiled.

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
