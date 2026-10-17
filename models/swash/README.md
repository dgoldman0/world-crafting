# SWASH 12.01 for a breathable Moon

SWASH (Simulating WAves till SHore, Delft University of Technology) is a non-hydrostatic wave–flow
model. Terluna uses it to follow individual waves, breaking and the moving waterline along
one-dimensional cross-shore profiles at the eastern Smythii headland. Its source is unchanged: lunar
gravity and the scenario's water density enter through the input file, and SWAN's coastal spectra
drive the offshore boundary through a one-way reduction done in Python. Correctness, limits and room
for improvement are in [../../notes/waves.md](../../notes/waves.md).

Terluna references are to its repository at commit 186b294. SWASH references (`SwashInit.ftn90:135`)
are to the files of the pinned archive.

## Upstream pin

| | |
|---|---|
| Release | SWASH 12.01 |
| Archive | https://swash.sourceforge.io/download/zip/swash-12.01.tar.gz |
| sha256 | `c8a2e149e4c1583f3f5a10fa6e9fa110e6db7d1eb41978420a4a387877ac397f` (897,775 bytes; 171 files) |
| Licence | GNU GPL version 3 or later, copyright Delft University of Technology (header of every source file, e.g. `SwashInit.ftn90:14–26`) |
| Source changes | None. Terluna's builder checks every source file against the archive and records `source_modifications: []` (`climate/waves/swash_build.py:36–46`, `66`). |
| Build | `make config`, then `make -j1 ser FLAGS_OPT=-O3` (`swash_build.py:55`), GNU Fortran 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1) |
| Executable | sha256 `2b5f94d2999121898dad72caa5e9f50c9c388085eff6ea7685d40b5cc063c124`, used by every Terluna run-up case and control (`climate/waves/results/runup.json`) |

Checked on 2026-10-17: the archive on the research drive matches the pin; all 171 archive files in
the deployed source tree are byte-identical except `macros.inc`, which `make config` writes; and the
executable matches its build record.

## Lunar settings

The western rock reference case (written by Terluna `climate/waves/runup.py:132–173`; output
requests omitted):

```
PROJECT 'Lunar runup' '001'
MODE DYN ONED
SET DEPMIN 0.005 SEED 12345678 GRAV 1.62421887656 RHOWAT 1025
CGRID 0 0 0 244 0 488 0
VERT 4
INPGRID BOTTOM 0 0 0 488 0 0.5 1
READINP BOTTOM 1 'depth.bot' 1 0 FREE
INIT ZERO
BOU SIDE W CCW BTYPE WEAK SMOO 120 SEC CON SPECFILE 'spectrum.dat'
BOU SIDE E CCW BTYPE RADIATION
FRIC CONSTANT 0
BREAK 0.6 0.3
NONHYDROSTATIC BOX PRECONDI ILU
DISCRET UPW MOM
TIMEI METH EXPL .1 .5
QUANT RUNUP DELRP 0.01
COMPUTE 000000.000 0.025 SEC 004000.000
```

| Setting | What it does on the Moon |
|---|---|
| `GRAV 1.62421887656` | `GM/R²` from Terluna's shared constants, replacing the default 9.813 (`SwashInit.ftn90:135`; read at `SwashReadInput.ftn90:533`). Gravity reaches the breaking detector (`sqrt(grav*hs)`, `SwashBreakPoint.ftn90:115`, `174`), the boundary's evanescent-mode cut-off (`omegcf = 0.9·2·kmax·sqrt(grav/swd)`, `SwashBCshortwave.ftn90:106`) and the flow equations. Terluna's source audit names the routines it followed (`climate/waves/runup.md:136–143`). |
| `RHOWAT 1025` | The same seawater scenario as SWAN (`shared/scenarios/waves.json`). With uniform density, no wind and no air-pressure forcing, water density cancels from the flow: it appears divided by itself in the baroclinic and air-pressure terms (e.g. `SwashExpLay1DHflow.ftn90:757`, `784`, `807`) and in the kinematic viscosity (`SwashCheckPrep.ftn90:918`). The spectral boundary divides by ρg only when the file holds energy density (`SwashBCspecfile.ftn90:499–500`); Terluna's files hold variance density. Unset, SWASH would compute the density from Eckart's formula at 14 °C and 31 psu (`SwashCheckPrep.ftn90:894–899`; `SwashInit.ftn90:144–145`). |
| `DEPMIN 0.005`, `DELRP 0.01` | Wet–dry threshold (`epsdry`, `SwashReadInput.ftn90:528`) and the run-up depth threshold, both in metres. Numerical thresholds, not gravity-dependent. |
| `VERT 4` (6 in controls) | Keller-box layers. Up to four uniform layers SWASH builds incident velocities from its discrete first-order Stokes solution; above four it uses the continuum hyperbolic-cosine profile, so going from 4 to 6 layers also changes the wavemaker (Terluna `runup.md:160–167`). |
| `BOU SIDE W ... BTYPE WEAK SMOO 120 SEC CON SPECFILE` | Weakly reflective wavemaker driven by a 1-D variance spectrum with a 120 s ramp. The east side radiates; flat-flume controls add a sponge (`SPON E`). |
| `FRIC CONSTANT 0` | No bottom friction in the reference cases; a dimensionless 0.005 is a sensitivity case. |
| `BREAK 0.6 0.3` | Breaking starts where the surface rises faster than `α·sqrt(g·h)` and persists down to `β·sqrt(g·h)` (`SwashBreakPoint.ftn90:95–96`, `115`). These are SWASH's defaults: α 0.6, β 0.3 by default substitution (`SwashReadInput.ftn90:916–917`; `SwashCheckPrep.ftn90:1065–1083`). The command also switches on a mixing-length viscosity, `ν = NUFAC·h²·|∂u/∂x|` with `NUFAC` 1 (`SwashReadInput.ftn90:918–921`; `SwashHorzVisc.ftn90:139`); it contains no gravity term and is consistent with gravity scaling. |
| `NONHYDROSTATIC BOX PRECONDI ILU` | The default ILUD preconditioner failed in a four-layer spectral diagnostic; ILU completed it (Terluna `runup.md:177–179`). |
| `TIMEI METH EXPL .1 .5`, `COMPUTE ... 0.025 SEC` | Explicit time integration with the time step adapted to keep the Courant number within 0.1–0.5, starting from 0.025 s (0.05 s on the 1 m beach grids). |

Grids: 0.25–1 m spacing on profiles sampled every 2 m from the 118 m LOLA/GRAIL flooded-rock terrain,
plus smooth 1:20, 1:50 and 1:100 beach scenarios, each with a 100 m constant-depth reach before the
slope (Terluna `geography/shore_profiles.py`; `runup.md:69–89`). Water level is fixed at the atlas
level: no tide.

## Coupling from SWAN (Terluna `climate/waves/runup.py:52–129`)

1. **Source.** A SWAN `SPEC2D` spectrum E(f, θ) in m²/Hz/degree at a coastal station, from a completed
   shore or coastal-history case. The spectrum and its run record are hash-checked (`runup.py:56–64`).
2. **Consistency.** The SWAN case's `GRAV` and `RHO` must equal the SWASH settings to a relative
   1×10⁻¹⁰, or the transfer stops (`runup.py:65–70`).
3. **Reduction to normal incidence.** E₁ᴅ(f) = Σ_θ E(f, θ)·max(n·u_θ, 0)·Δθ, with n the shoreward normal
   of the station's profile (`runup.py:82–87`). This keeps the shoreward-travelling energy and drops
   seaward and alongshore components. At the source depth E₁ᴅ·c_g equals the shoreward energy flux of
   the 2-D spectrum.
4. **Band.** The upper frequency is capped at `0.9·K/π·sqrt(g/d)` for K layers and source depth d
   (`runup.py:91`), the cut-off SWASH applies at its boundary (`SwashBCshortwave.ftn90:106`), and at the
   SWAN band top. More than 1% of the incoming variance removed stops the transfer unless the bound is
   explicitly widened for a labelled sensitivity case (`runup.py:92–107`).
5. **Discretisation.** The piecewise-linear SWAN spectrum is integrated exactly onto a uniform
   1/3600 Hz grid, each bin receiving its integrated variance (`runup.py:40–49`, `97–103`). The boundary
   phases are random with a recorded seed and repeat after 3600 s.
6. **Record.** Incoming and represented Hs, removed variance, mean period, edge fractions of the source
   band and the error in shoreward variance flux (`runup.py:108–128`).

Not represented: obliquity and alongshore variation (a 2-D wave-resolving model would be needed), bound
harmonics and infragravity waves at the boundary, and feedback from the shore to SWAN (Terluna
`runup.md:93–124`).

## Verification (Terluna's recorded controls)

| Control | Tests | Result | Evidence state |
|---|---|---|---|
| Linear waves (`runup.py:176–206`) | A 0.02 m regular wave in 5 m of water at lunar g (10 s), 4× lunar g (5 s) and standard g (4.07 s), three gauges against the analytic dispersion relation | amplitude within 1.76%, phase within 0.289% at all three gravities | implementation |
| Linear similarity (`runup.py:207–214`) | 4× gravity with the clock halved and lengths fixed | gauge records agree to 9.1×10⁻⁶ of the amplitude | similarity |
| Nonlinear similarity (`climate/waves/runup_controls.py:107–143`) | The western rock case with breaking and wetting at 4× gravity, half the clock, frequencies ×2 and spectral density ÷2 | 98th-percentile run-up within 1.20%, profile Hs within 0.189%; single waterline samples differ by up to 0.277 m | similarity |
| Still water (`runup_controls.py:92–106`) | Rest state on the rock profile at 0.5 and 0.25 m spacing | wet surface level within 10⁻⁵ m; the waterline diagnostic sits 4.07 and 0.892 cm above still water at rest | implementation |
| Wall reflection (`runup_controls.py:18–41`) | Incident and reflected waves at a closed wall | amplitude ratio 1.0102, fit residual 0.776% | implementation |
| Irregular input (`runup_controls.py:44–86`) | The transferred western spectrum (Hs 1.719 m, Tm 12.74 s) in a flat 22.38 m flume | Hs within 5.22%, Tm within 6.28%; fails its 5% bounds (6 layers 5.62%/6.74%; 0.25 m spacing 4.93%/5.73%) | implementation, open |
| Grid, layers, wavemaker position, initialisation, phases (`runup.md:41–56`, `169–175`, `234–260`) | Sensitivity of run-up statistics | 98th-percentile changes of 0.9–6.75%; the 1:50 beach grid (5.19%, 6.4%) and the eastern 4→6 layers (6.75%) exceed their 5% bounds | numerical convergence, partly open |

None of these validates lunar breaking or run-up: the similarity controls show that the configured
equations and the executable scale with gravity as they should, so the lunar runs are the
gravity-scaled images of Earth runs with Earth-calibrated breaking.

## Constants in SWASH that are Earth's (not active in Terluna's runs)

| Constant | Location | Settable | Status |
|---|---|---|---|
| Gravity 9.813 | `SwashInit.ftn90:135` | yes, `SET GRAV` (`SwashReadInput.ftn90:533`) | overridden |
| Earth's rotation `omega = pi2/(24.*3600.)` | `SwashCheckPrep.ftn90:3243` | no | Coriolis is off by default (`SwashInit.ftn90:307`) and disabled in 1-D (`SwashCheckPrep.ftn90:374–377`). A 2-D spherical lunar run with Coriolis needs a patch: the Moon's sidereal rate is 2.6617×10⁻⁶ s⁻¹, 27 times smaller than the coded 7.2722×10⁻⁵ s⁻¹ (2π per 86,400 s, Earth's solar day rather than its sidereal day). |
| Default latitude 52° for Coriolis | `SwashInit.ftn90:128` | yes | inactive |
| Radius 2×10⁷/π m | `SwashInit.ftn90:160` | yes, `COORDINATES SPHERICAL [rearth]` (`SwashReadInput.ftn90:584`) | inactive (Cartesian 1-D runs) |
| Air density 1.205 kg/m³ | `SwashInit.ftn90:137` | yes, `SET RHOAIR` (`SwashReadInput.ftn90:538`) | enters wind stress (`SwashWindStress.ftn90:135`); no wind in these runs |
| Seawater at 14 °C and 31 psu | `SwashInit.ftn90:144–145`, `SwashCheckPrep.ftn90:894–899` | yes, `RHOWAT` | overridden |
| Breaking α 0.6, β 0.3 | `SwashReadInput.ftn90:916–917`, `SwashCheckPrep.ftn90:1065–1083` | yes | dimensionless, Earth laboratory calibration, used as shipped |
