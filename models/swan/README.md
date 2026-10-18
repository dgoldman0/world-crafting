# SWAN 41.51 for a breathable Moon

SWAN (Simulating WAves Nearshore, Delft University of Technology) computes Terluna's lunar sea states:
the 100 km strips, the Smythii–Marginis and nearside seas through two lunar cycles, and nested coastal
grids down to 118 m. Two source patches change it. Every other lunar setting is an input command, and
the atmosphere enters through a stress-to-wind inversion done before SWAN runs. Correctness, limits
and room for improvement are in [../../notes/waves.md](../../notes/waves.md).

Terluna references are to its repository at commit 186b294. SWAN references (`swancom3.ftn:1800`) are
to the unpatched files of the pinned archive, relative to its `swan4151/` source root.

## Upstream pin

| | |
|---|---|
| Release | SWAN 41.51 |
| Archive | https://swanmodel.sourceforge.io/download/zip/swan4151.tar.gz |
| sha256 | `325c229f3dde0b812db4ec9ae6fa1cd4086d2109562c389576590ce8f94b26bb` (945,645 bytes; 93 files under `swan4151/`) |
| Licence | GNU GPL version 3 or later, copyright Delft University of Technology (header of every source file, e.g. `swancom3.ftn:56–61`). The patches and any executable built with them are distributed under the same licence and attribution. |
| Patched files, before | `swancom3.ftn` `b164c7b9ac8f94672b637e114dbacad503b624c8c1c8ae50339b80c0083558af`; `swanmain.ftn` `d89c664cddb06de60b84655e8523e04fb8b17dc342ff5add158579369bfb568a` |
| Patched files, after both patches | `swancom3.ftn` `809b4aa2fb020a9170a5a49bb0caa101889dc27939ecbeca4e07893346601acc`; `swanmain.ftn` `fd5b493749cd9264081b2094f61fcaff64b41a6e0f624bd68d89300bcd85fc43` |

Terluna pins the archive and the two original files in `climate/waves/build.py:25–30`. The archive
ships an empty `macros.inc`; `make config` writes it.

## The patches

| Patch | Location | Change | Run-time switch | Earth behaviour | Kind |
|---|---|---|---|---|---|
| `01-agrow-knee.patch` | `swancom3.ftn:1800`, routine `SWIND0` | The 1 Hz bend of AGROW's linear growth moves to `GRAV/9.80665` Hz | None; acts whenever `AGROW` is set | Bit-identical to stock at `SET GRAV 9.80665`; bend at 1.00034 Hz with SWAN's default `GRAV` 9.81 | General repair: a dimensional constant made to scale with gravity |
| `02-air-density.patch` | `swanmain.ftn:1740` | Compiled-in air density `PWIND(16)` 1.28 → 1.40390062332 kg/m³ | None; one value per build | Not applying the patch is stock | Value substitution, possible only by editing the source |

Both patches reproduce exactly the edits of Terluna's `climate/waves/build.py` (`patch_agrow`, lines
68–91; `patch_air_density`, lines 117–132; file sha256 `74afe80f…a378` at 186b294). They touch
different files and apply in either order. Each patch file starts with a short header (origin and
hashes) that `patch` and `git apply` skip.

### 01-agrow-knee.patch: AGROW's bend at fixed frequency/gravity

**Change.** `SWIND0` computes the linear growth term that starts waves on calm water (Cavaleri and
Malanotte-Rizzoli 1981, in the form SWAN uses) and multiplies it by `FREQ1**(-3)` wherever
`FREQ1 > 1` (`swancom3.ftn:1800–1806`). The patch replaces

    FREQ1 = SIGMA/PI2

with

    FREQ1 = (SIGMA/PI2) * (9.80665/GRAV)

and adds two comment lines. The bend moves from 1 Hz to `GRAV/9.80665` Hz: 1 Hz at standard gravity,
0.16562 Hz at the lunar `GM/R²` of 1.62421887656 m/s².

**Why.** The rest of `SWIND0` scales with gravity: the Pierson–Moskowitz frequency
`FPM = GRAV/(28·UFRIC)` (`swancom3.ftn:1774`), the coefficient `PWIND(31)/(GRAV²·2π)` (`:1775`) and the
onset gate `SIGMA ≥ 0.7·FPM` (`:1794`). The upstream comment calls the 1 Hz bend "mostly arbitrary,
intended to have zero effect on typical simulations (which stop at 1 Hz)" and names `fpm` as an
alternative bend (`swancom3.ftn:1722–1725`). A bend fixed in hertz makes a run at scaled gravity,
lengths and times differ from the Earth run it should reproduce in dimensionless form. Terluna's
source audit records the same diagnosis (`climate/waves/audit.md:45–60`).

**Switch and default.** There is no run-time switch. `SWIND0` runs only when `GEN3 ... AGROW` sets the
linear coefficient (`A = 0.0015` by default, `swanpre1.ftn:3063–3064`; the call is guarded at
`swancom1.ftn:7418`), so without `AGROW` the patch has no effect. The reference gravity 9.80665 m/s²
is written into the source.

**Earth behaviour.** With `SET GRAV 9.80665` the factor `9.80665/GRAV` is exactly 1.0 in single
precision, and the patched and stock executables wrote identical Earth strip profiles (Terluna
`climate/waves/run.py:117–120` requires exact equality; `results/waves.json`,
`earth_output_preserved: true`).
SWAN's default gravity is 9.81 (`swanmain.ftn:1267`); there the bend sits at 1.00034 Hz and output is
not bit-identical to stock.

**Effect at lunar gravity.** The lunar runs use 0.00497–0.497 Hz. The stock bend (1 Hz) lies above that
band and never acts; the patched bend damps the linear term over the top 11.5 of the band's 48 intervals,
by a factor of up to 27 at the band top. In Terluna's 100 km strip the 48-hour heights change by at most
0.11%, while one-hour heights at 100 km fall from 0.073 to 0.036 m (2.15 m/s wind), 0.179 to 0.132 m
(4.00 m/s) and 0.306 to 0.266 m (5.84 m/s) (`results/waves.json`, stock and patched rows). The patch
makes lunar SWAN behave as Earth SWAN does in dimensionless terms; it says nothing about how wind
starts waves on the Moon.

**Verification.**
- Gravity similarity (Terluna `run.py:83–109`): an Earth strip and a strip at one sixth of standard
  gravity with lengths, depth and duration ×6 and frequencies ÷6, compared at matching points.
  Largest differences in height and mean period: patched 0.303% and 0.326%; stock 5.44% and 3.91%.
- Earth identity, above.
- Patch arithmetic (Terluna `climate/tests/test_waves.py:229–251`): the patched `FREQ1` equals `f` at
  standard gravity and `f·9.80665/g` at lunar gravity.

**Limits.** The bend is still arbitrary. It scales with gravity at a fixed wind; a bend tied to
`FPM ∝ g/u*` would also preserve similarity across wind speeds. The coefficient 1.5×10⁻³ is
Earth-fitted and carries Earth's air–water density ratio implicitly (`swancom3.ftn:1775` has no density
in it). Early growth from calm water is not converged in time step (Terluna
`climate/waves/first_experiments.md:95–116`).

### 02-air-density.patch: the compiled-in air density

**Change.** `swanmain.ftn:1740` `PWIND(16) = 1.28` → `PWIND(16) = 1.40390062332`. After the input is
read SWAN resets `PWIND(9) = PWIND(16)/RHO` (`swanmain.ftn:6626`). `PWIND(9)` is the air–water density
ratio in Komen's wind input, `TEMP1 = 0.25·PWIND(9)` (`swancom3.ftn:2068`). `PWIND(16)` is also
Janssen's `RHOA` (`swancom3.ftn:2344`) and ST6's `d_air` (`m_constants.ftn90:45`).

**Why.** SWAN's third-generation physics has no input for air density. `SET RHO` sets the water density
(`swanpre1.ftn:2180`). The `RHOAW` keyword exists only in the undocumented `GROWTH G1|G2` commands
(`swanpre1.ftn:3239`, `3257`), and the reset at `swanmain.ftn:6626` overwrites it. 1.28 kg/m³ is an
Earth value.

**Value.** 1.40390062332 kg/m³ is the mean 2 m moist-air density over the 72 water columns of CM1's
corrected equatorial ring between 75° E and 103° E, across 237 snapshots on model days 29.5–59 (range
1.38029–1.41668), from CM1's ideal-gas closure (Terluna `climate/crm/wave_forcing.py:27–31, 95–98, 115`;
`climate/waves/results/forcing.json`, sha256 `c5bac5fd…d74b`). `build.py:128` writes it with 12
significant figures.

**Switch and default.** There is no run-time switch; the value holds for the whole run and every grid
point. Without the patch SWAN uses 1.28. For another atmosphere, change the `+` line of the patch; the
context lines stay valid.

**Effect.** At a given friction velocity, Komen's input coefficient rises by 1.40390/1.28 = 1.0968.

**Verification.** The patch is anchored to the pinned file hash and to one exact line
(`build.py:121–127`), and Terluna's build manifests record the before and after hashes. No run
isolates its effect on the waves.

**Limits.** One density for all grid points, while Terluna's GCM air over open sea ranges 1.22–1.45
kg/m³ (see the notes). The linear AGROW term has no density. ST6's ECMWF drag routine has its own
`RHOA = 1.28` (`SdsBabanin.ftn90:2471`) and does not read `PWIND(16)`.

## Verification of these patch files

Done on 2026-10-17 from the pinned archive, without compiling or running SWAN:

| Check | Result |
|---|---|
| Archive sha256 | `325c229f…26bb`, as pinned |
| Fresh extraction against Terluna's pristine source tree | identical |
| `patch -p1 --dry-run`, each patch on a pristine tree | applies at lines 1797 and 1737 with no offset or fuzz; `git apply --check` also passes |
| Both patches applied | `swancom3.ftn` `809b4aa2…6acc`, `swanmain.ftn` `fd5b4937…fc43` |
| Terluna's own `patch_agrow` and `patch_air_density`, run on a pristine copy | the same two hashes |
| Deployed patched sources (`patched_agrow`, `coupled_air`, `optimized_serial/coupled_air`, `optimized_openmp/coupled_air`) | the same hashes; of the 93 archive files only `macros.inc` differs, written by `make config` |
| Diffs recorded in the build manifests | identical to the patch bodies |
| Reverse application to the deployed OpenMP sources | returns the pristine hashes |

For the repository's patch check, the series is `01-agrow-knee.patch` then `02-air-density.patch`,
and the expected results, as `sha256sum -c` lines relative to the source root, are:

    809b4aa2fb020a9170a5a49bb0caa101889dc27939ecbeca4e07893346601acc  swancom3.ftn
    fd5b493749cd9264081b2094f61fcaff64b41a6e0f624bd68d89300bcd85fc43  swanmain.ftn

Terluna's builds are under `/media/projectspace/terluna-research/wave-runs/swan_builds/lunar-seas-swan/`
on the author's machine. All were compiled with GNU Fortran 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1),
and every executable still matches its manifest:

| Build | Patches | `make` target, optimisation | Executable sha256 | Used by |
|---|---|---|---|---|
| `stock` | none | `ser`, `-O` | `683cc283…7d1f` | none of the recorded products (the strip used an earlier build, below) |
| `patched_agrow` | 01 | `ser`, `-O` | `a7d809de…e673` | early growth |
| `coupled_air` | 01, 02 | `ser`, `-O` | `b0cac8ff…d3c1` | basin pilot, coastal resolution, weather week |
| `optimized_serial/coupled_air` | 01, 02 | `ser`, `-O3 -march=native` | `ed8baf28…6f56` | build comparison only |
| `optimized_openmp/coupled_air` | 01, 02 | `omp`, `-O3 -march=native` | `8883fc9e…4875` | lunar cycle, shore exposure, coastal history, nearside sea |

The strip experiment (`results/waves.json`) ran on an earlier build in
`/tmp/terluna-swan-wrapper-build/` from the same archive, patch (same after-hash and diff) and commands.
Its executables hash differently (stock `b22dc0e6…`, patched `0a32101d…`). The patched sources are
identical across builds; the executables are not, for a reason not recorded. Against the original
serial build over the weather week, the optimised OpenMP build changes Hs by at most 0.512% and mean
period by 1.62%. Its serial and two-thread outputs agree exactly, and so do its two- and four-thread
outputs (Terluna `climate/waves/cycle.md:138–145`).

## Applying the patches

```sh
sha256sum swan4151.tar.gz      # 325c229f3dde0b812db4ec9ae6fa1cd4086d2109562c389576590ce8f94b26bb
tar -xzf swan4151.tar.gz
cd swan4151
patch -p1 < /path/to/world-crafting/models/swan/patches/01-agrow-knee.patch
patch -p1 < /path/to/world-crafting/models/swan/patches/02-air-density.patch   # omit for 1.28 kg/m³
make config
make -j1 omp FLAGS_OPT='-O3 -march=native'   # Terluna's production build; 'make -j1 ser' for serial
```

Patch 01 alone gives Terluna's `patched_agrow` build; no patch gives `stock`. `-march=native` ties the
executable to the build machine's processor.

## Run settings of the lunar studies

The GCM-forced basin runs use these commands (from the nearside sea's first segment; grid, input and
output lines shortened; `$` starts a SWAN comment):

```
MODE NONSTAT TWODIMENSIONAL
COORDINATES SPHERICAL 1737400 CCM
SET GRAV 1.62421887656 RHO 1025
CGRID REG ... CIRCLE 36 0.00496872696556 0.496872696556 48
INPGRID WIND ... NONSTAT 20000101.000000 15 MIN ...
GEN3 KOMEN DRAG WU AGROW
BREAKING CONSTANT 1.0 0.73
PROP BSBT
INIT ZERO                    $ INIT HOTSTART ... for the later 48-hour segments
COMPUTE NONSTAT ... 300 SEC  $ 150 SEC for Smythii–Marginis
```

The text is written by Terluna `climate/waves/nearside.py:188–223`; the Smythii runs use
`climate/waves/pilot.py:137–173` and `weather.py:165–187`, and the strip `climate/waves/model.py:87–117`.

| Setting | Value | Reason and source path |
|---|---|---|
| Gravity | `SET GRAV 1.62421887656`, `GM/R²` from Terluna's shared constants (GM 4.9028001180×10¹² m³/s², R 1737.4 km) | The default is 9.81 (`swanmain.ftn:1267`). Gravity reaches the dispersion relation (`KSCIP1`, `swanser.ftn:694–717`), Komen's input through `k/σ` and `28·u*` (`swancom3.ftn:2068–2084`), Komen whitecapping through `k` and the mean steepness (`swancom2.ftn:2485–2491`, `2611–2615`), the DIA's `1/GRAV**4` (`swancom4.ftn:243`) and AGROW (above). The default action limiter, `0.0081/(2σk³c_g)` (`swancom1.ftn:7980`), is dimensionally consistent. |
| Water density | `RHO 1025`, Terluna's seawater scenario (`shared/scenarios/waves.json`) | In this configuration it enters only the air–water ratio (and output in energy units, not used). The default is also 1025 (`swanmain.ftn:1277`). The author has since directed fresh seas (see the notes). |
| Spherical radius | `COORDINATES SPHERICAL 1737400 CCM` | `REARTH` is read as the number after `SPHERICAL` (`swanpre1.ftn:827–828`, not in the manual); the default is 2×10⁷/π m ≈ 6366 km (`swanmain.ftn:1449`). It sets the degree length (`swancom5.ftn:204–205`) and the great-circle turning (`:1918`); the source has no other radius constant. |
| Frequencies and directions | 0.03–3 Hz scaled by g/9.80665: 0.0049687–0.49687 Hz, 48 logarithmic intervals (10.1% spacing), 36 directions | Keeps the dimensionless resolution of an Earth run (Terluna `model.py:82–85`). The band top corresponds to a 1.05 m deep-water wave, where surface tension changes the dispersion by 0.16%. |
| Source terms | `GEN3 KOMEN DRAG WU AGROW`; DIA quadruplets by default (`IQUAD 2`, `swanmain.ftn:1373`); no bottom friction or triads (defaults `IBOT 0`, `ITRIAD 0`, `swanmain.ftn:1376–1377`) | These paths take gravity from `GRAV`. Komen whitecapping keeps its defaults (`Cds` 2.36×10⁻⁵, `s̃²_PM` 3.02×10⁻³; `swanmain.ftn:1602–1607`); DIA keeps λ 0.25 and C 3×10⁷ (`:1715–1716`). |
| Avoided options | ST6 with FAN or ECMWF drag; exact quadruplets (XNL) | They carry Earth constants: `SURF_ROUGH_FAN` sets `G=9.8` (`SdsBabanin.ftn90:2305`); `SURF_ROUGH_ECMWF` sets `G=9.81`, `RHOW=1025.0` and `RHOA=1.28` (`:2466`, `:2470`, `:2471`); the finite-depth coefficient `xc_hh` sets `g=9.81` twice (`mod_xnl4v5.ftn90:8540`, `8563`). Terluna avoided these options and left them unpatched (`audit.md:135–138`). |
| Depth breaking | `BREAKING CONSTANT 1.0 0.73`, which is SWAN's default (`ISURF 1`, `PSURF(2) 0.73`; `swanmain.ftn:1375`, `1664–1665`) | Kept on because of a latent defect. With `OFF BREAKING`, `SINTGRL` leaves `KTETA` unset (declared `INTENT(OUT)` at `swancom1.ftn:5706`, assigned through `BRKPAR` only when `ISURF > 0`, `:5944–5949`). `FRABRE` is still called (`:6001`) and divides by `SQRT(KTETA)` (`swancom2.ftn:1744`), and the resulting breaking fraction gates the limiter (`swancom1.ftn:7990`). Repeated identical Earth runs differed by about 2.5% in Hs (`audit.md:68–100`). In deep water the breaking fraction stays zero: every strip run checks it (`run.py:146`). The index 0.73 is dimensionless and Earth-calibrated. |
| Initial state | `INIT ZERO` (hotstart files between nearside segments) | `INIT DEFAULT` builds a fetch-limited first guess but forces a 2 s peak period when Hs < 0.05 m, and uses Hs 0.02 m and 2 s without wind (`swanmain.ftn:9410`, `9417`; again at `9469`, `9475`), which are Earth dimensions. A zero start needs AGROW to seed growth (Terluna `model.py:75–76`). |
| Propagation and time step | `PROP BSBT`; 300 s (strip, nearside sea), 150 s (Smythii–Marginis), 900 s with 450 s checks (coastal history), stationary for the shore nests | Steps and their checks are in the notes. |
| Output | `TRANSP` with SWAN's default `INRHOG 0` (`swanmain.ftn:1400`) | Variance transport in m³/s; Terluna multiplies by ρ·g with the lunar g to get W/m (`climate/waves/shore.py:204–205`). |

## The forcing: stress to Wu-equivalent wind

SWAN takes a wind at 10 m and turns it into a friction velocity through a drag law. Terluna instead
gives SWAN a wind chosen so that SWAN's own drag law returns the GCM's surface stress (Terluna
`climate/waves/weather.py:20–42`, coefficients in `shared/constants.json:59–66`):

    ρ_SWAN · Cd_Wu(|U|) · |U| · U = τ_GCM,
    Cd_Wu = 1.2875×10⁻³ for |U| ≤ 7.5 m/s, (0.8 + 0.065 |U|)×10⁻³ above   (swancom3.ftn:1014–1024)

- `stress_equivalent_wind` solves for |U| by 55 bisections between 0 and `sqrt(|τ|/(ρ·1.2875×10⁻³))`,
  an upper bound because Cd grows with speed, and keeps the stress direction; zero stress gives zero
  wind. ρ_SWAN is the compiled `PWIND(16)`, read from the build manifest, so SWAN's friction velocity is
  `sqrt(|τ|/ρ_SWAN)`.
- The GCM stress vectors are interpolated linearly in time to 15-minute knots, then inverted
  (`weather.py:120–131`; `nearside.py:168–185`). SWAN interpolates the winds linearly between knots. The
  implied stress at the midpoints departs from the intended stress by at most 1.1×10⁻⁴ Pa over the
  Smythii cycle (99th percentile 0.21% of the stress; `results/cycle.json`, forcing record).
- In space, bilinear weights use only GCM cells that stay ice-free open water for the whole record. A
  node with no such corner takes the nearest open-water cell (`weather.py:45–81`). The nearside grid
  extends the GCM's longitudes periodically across 0° (`nearside.py:128–135`).
- Every run checks SWAN's printed wind against the supplied vectors, and SWAN's printed friction
  velocity against `sqrt(Cd)·|U|` (`weather.py:207–216`). A unit test checks the inversion in both drag
  regimes (`climate/tests/test_wave_weather.py:11`).

Why this carries the GCM's momentum flux: with `GEN3 KOMEN AGROW` every wind-dependent source term
uses the friction velocity `UFRIC` (`swancom3.ftn:1113`, `1774`, `2073`); whitecapping and quadruplets
do not use the wind; and the 10 m wind enters only through `Cd_Wu(U)`. The Wu law is an Earth fit with no gravity in it. After the inversion it only converts units,
so the friction velocity carries the GCM's lunar surface layer. In that layer ExoPlaSim's open-sea
roughness is `max(0.018 u*²/g, 1.5×10⁻⁵ m)` with the lunar g (Terluna `climate/waves/review.md:22–30`;
`shared/constants.json:50–58`). The GCM's stress-closure density is `p_s/(R T_s)` with its gas constant,
288.38 J/(kg K) (`climate/gcm/wave_snapshots.py:194–199`).

What the inversion is not:
- U is not a 10 m wind. Over the equatorial seas the GCM's 99th-percentile Wu-equivalent speed is
  6.57 m/s against a Charnock-neutral 5.77 m/s (Terluna `results/review_checks.json`).
- It holds only for `DRAG WU`. Janssen's input (`SWIND4`) solves the stress from the 10 m wind with its
  own Charnock constant 0.01 (`swancom3.ftn:2347`, `2561–2569`; `swanmain.ftn:1735`), so a Janssen run
  needs its own inversion or a physical 10 m wind.
- The density is the compiled constant, not the GCM's local air (see the notes).

The prescribed-wind experiments (strip, early growth, basin pilot, coastal resolution) pass CM1's
10 m winds through Wu's law directly. Their friction velocities carry Wu's Earth calibration.

## SWAN constants left as they are

| Constant | Location | In Terluna's lunar runs |
|---|---|---|
| Default gravity 9.81 | `swanmain.ftn:1267` | overridden by `SET GRAV` |
| Default radius 2×10⁷/π m | `swanmain.ftn:1449` | overridden by `COORDINATES SPHERICAL 1737400` |
| `INIT DEFAULT`'s 2 s period, 0.05 m and 0.02 m | `swanmain.ftn:9410`, `9417` (`9469`, `9475`) | bypassed by `INIT ZERO` and hotstarts |
| Wu drag | `swancom3.ftn:1014–1024` | inverted in GCM-forced runs; used directly in prescribed-wind runs |
| ST6 FAN and ECMWF drag: `G`, `RHOW`, `RHOA` | `SdsBabanin.ftn90:2305`, `2466`, `2470`, `2471` | option not used |
| XNL finite-depth coefficient `g=9.81` | `mod_xnl4v5.ftn90:8540`, `8563` | option not used |
| JONSWAP bottom friction 0.038 m²/s³ | `swanmain.ftn:1658` | bottom friction off (`IBOT 0`, `:1376`); dimensional, so it would need scaling with g if used |
| AGROW coefficient 0.0015, Komen 0.25 and 28, whitecapping coefficients, DIA coefficients, breaking index 0.73 | `swanpre1.ftn:3064`; `swancom3.ftn:2068`, `2073`; `swanmain.ftn:1602–1607`, `1715–1716`, `1665` | dimensionless Earth fits, used as shipped |
