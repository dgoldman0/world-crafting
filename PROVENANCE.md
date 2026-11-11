# Provenance

Everything here came from Terluna (github.com/dgoldman0/Terluna, commit 186b294, 2026-10-17, the same
state as the author's local checkout that day) or from its research drive, or was generated from them.
This file records each origin and hash; the upstream archives are pinned in `models/pins.sha256`.

## Generated patch series

The patch files were generated on 2026-10-17 by applying, one group at a time, the edit lists in
Terluna's runners to pristine upstream sources and recording each group's unified diff:

| Series | Generated from (Terluna 186b294) | sha256 (first 16) of that file |
|---|---|---|
| `models/exoplasim/patches/` | `climate/gcm/exoplasim_run.py`: `PATCHES`, `TWILIGHT_PATCHES` (with constants from `climate/gcm/plasim_ice_optics.py`) | 20457ad6dbf94453 (with c21af4d40819633b) |
| `models/cm1/patches/` (core, terrain, sea, twilight, earth-fall, Makefiles) | `climate/crm/cm1_run.py`: `MAKEFILE`, `PATCHES`, `TERRAIN_PATCHES`, `SEA_COLUMNS_PATCH`, `TWILIGHT_PATCH`, `EARTH_FALL_PATCH`, `optimization_patch` | c779ac6e6ac20f50 |
| `models/cm1/patches/elec/` | `climate/crm/cm1_elec.py`: `quiet_msz`, `PATCHES` | 2619025f7b0a647e |
| `models/swan/patches/` | `climate/waves/build.py` | 74afe80f1161372e |
| `models/cm1/patches/lab/` (written 2026-11-08, from Terluna `bdda5a07`) | `climate/crm/cm1_run.py`: `PBL_DENSITY_PATCH`, `GUST_PATCH`, moved behind namelist switches | c0337fc8be2635ac |
| `models/exoplasim/patches/12-surface-gust.patch`, `13-similarity-over-water.patch` (written 2026-11-11, from Terluna `39c5ee04`, branch `domain/climate`) | `climate/gcm/surface_gust.py`: `GUST_EDITS`; `climate/gcm/surface_similarity.py`: `SIMW_EDITS`; `climate/gcm/pbl_fortran.py`: the declarations of the five constants the depth rule reads | fb163850a4aa62d0, b676096169aa7f25, 66a8edb841195d7e |
| `models/cm1/patches/lab/03-raindrop-limits-at-the-builds-gravity.patch`, `04-rains-fall-law-and-self-collection-for-the-world.patch` (written 2026-11-11, from Terluna `39c5ee04`, branch `domain/climate`) | `climate/crm/cm1_run.py`: `RAIN_LIMITS_PATCHES`, `RAIN_LAW_PATCHES` | ba507fc66d1ea4fd |

The last three rows differ. Patches 01 and 02 of `models/cm1/patches/lab/` were written by hand on 2026-11-08 from
Terluna's edits at `bdda5a07`, with namelist switches added. ExoPlaSim's patches 12 and 13 were written on
2026-11-11 from Terluna's edit lists at `39c5ee04`, applied to the pinned `fluxmod.f90` without Terluna's
free-convection and nonlocal boundary-layer patches, which they follow there, and with the air's viscosity derived
in each column. Their routines, from `gustnl` through `simwcol`, equal those of Terluna's deployed `fluxmod.f90`
(research drive, `exoplasim-twilight/exoplasim/plasim/src/`, sha256 `0eadda0bb213cf83…`, read on 2026-11-11) but for
comment lines and the two viscosity lines. CM1's patches 03 and 04 were written on 2026-11-11 from Terluna's two edit
lists at `39c5ee04`, applied after the lab's patches 01 and 02, with the entries of `&param3` under Terluna's names.
The identifiers, the comments and the table's file name are the lab's, and the headers Terluna's lists set at the
top of `morrison.F` are left out. The code differs from the lists in two ways: the two mean fall speeds that rain's
collection of snow and graupel reads are set once in a level, where Terluna's list branches at each of four
statements, and the scheme stops on a `brkup_gscale` other than 0 and 1 and on a table of fewer than two rows or
with a step of zero or less, which the lists leave unchecked (`models/cm1/README.md`). In a single scratch run on
2026-11-11, one column of the patched scheme returned the fields of the `morrison.F` of Terluna's build
`moon_omp_rain_law_pbl_wind_gust_aloft_inflow` (research drive, `cm1/build/`, sha256 `79170284b1487597…`) to the bit
on 21 test columns under CM1's flags, at the defaults and with the Open Moon's settings.

The runners themselves, which insert this code at build time, stay in Terluna. Applying the series to
the pinned sources reproduces the deployed sources (see each model's README and `models/check_patches.sh`).

## Files brought

| Here | From | sha256 (first 16) here | sha256 there |
|---|---|---|---|
| models/cm1/fortran/terluna_elec.F | Terluna climate/crm/fortran/terluna_elec.F | 698d87b20f1a8e20 | 698d87b20f1a8e20 |
| models/cm1/fortran/terluna_lightning.F | Terluna climate/crm/fortran/terluna_lightning.F | 332666577105b5cc | 332666577105b5cc |
| models/cm1/fortran/terluna_branched.F | Terluna climate/crm/fortran/terluna_branched.F | 36ea5092380f4ac5 | 36ea5092380f4ac5 |
| models/cm1/fortran/terluna_screen.F | Terluna climate/crm/fortran/terluna_screen.F | 60e47591506b4d16 | 60e47591506b4d16 |
| models/cm1/fortran/terluna_mlint2.F | Extracted from WRF-ELEC elec/module_boxmgsetup.F (e43041b) by Terluna cm1_elec.mlint2 | 204da89fd8684a7a | source file eca6882798713e9b |
| models/exoplasim/design_case/A28_corrected_970/radmod_namelist | research drive gcm-runs/A28_corrected_970/model/radmod_namelist | ef6f406ba20a1d2f | ef6f406ba20a1d2f |
| models/exoplasim/design_case/A28_corrected_970/rainmod_namelist | research drive gcm-runs/A28_corrected_970/model/rainmod_namelist | fa9b41795525ce17 | fa9b41795525ce17 |
| models/exoplasim/design_case/A28_corrected_970/plasim_namelist | research drive gcm-runs/A28_corrected_970/model/plasim_namelist | ebe3cc08315417f1 | ebe3cc08315417f1 |
| models/exoplasim/design_case/A28_corrected_970/planet_namelist | research drive gcm-runs/A28_corrected_970/model/planet_namelist | 6305555c03892c9e | 6305555c03892c9e |
| models/exoplasim/design_case/A28_corrected_970/landmod_namelist | research drive gcm-runs/A28_corrected_970/model/landmod_namelist | 2351e42beaa53ae3 | 2351e42beaa53ae3 |
| models/exoplasim/design_case/A28_corrected_970/oceanmod_namelist | research drive gcm-runs/A28_corrected_970/model/oceanmod_namelist | 1e3a55b418fb4a3a | 1e3a55b418fb4a3a |
| models/exoplasim/design_case/A28_corrected_970/icemod_namelist | research drive gcm-runs/A28_corrected_970/model/icemod_namelist | 38d0dacf99632342 | 38d0dacf99632342 |
| models/exoplasim/design_case/A28_corrected_970/twilight.dat | research drive gcm-runs/A28_corrected_970/model/twilight.dat | 33f11867ade29a40 | 33f11867ade29a40 |
| models/exoplasim/design_case/A28_corrected_970_lw_ice/radmod_namelist | research drive gcm-runs/A28_corrected_970_lw_ice/model/radmod_namelist | 3d832991a123576e | 3d832991a123576e |
| models/exoplasim/design_case/A28_corrected_970_lw_ice/lwcorr.dat | research drive gcm-runs/A28_corrected_970_lw_ice/model/lwcorr.dat | e8c187b3668d6137 | e8c187b3668d6137 |

## Not brought

Case set-up, run bookkeeping and analysis scripts (`climate/gcm/exoplasim_run.py`, `climate/crm/cm1_run.py`
and the CRM analysis modules, `climate/waves/*` runners) stay in Terluna. Model output stays on the research
drive. Upstream source code is never committed whole.

## Python tools

The in-house reference and calibration tools under `python/` were copied byte for byte from Terluna, at
186b294 unless their entry names another commit, under their Terluna package paths; `python/provenance.json` lists the 135 files they hold with their
sha256 (98 brought first; the electricity package's conductivity column, muon ionization and charging laws, with
their three tests and committed products, added on 2026-10-17; and on 2026-10-18 the geography package's
heights above the geoid, storage levels, atlas, drainage and gazetteer reader, with their three tests and the
package's `.gitignore`; on 2026-11-08 CM1's output conventions and their test, from `bdda5a07`; and on 2026-11-11
the Python copies of PlaSim's gust and similarity over water with their two tests, from `39c5ee04`; and that day
the rain package's solver, breakup scale and fall law with their three tests, its record of sources and two files of
its vendored rainprops, from the same commit).
`python/climate/tests/test_plasim_ice_optics.py` takes the ice routines it compiles from
`models/exoplasim/patches/10-ice-optics.patch` in place of the runner's Python string (both hashes recorded).
The geography package came over byte for byte (82b4b59), with its input restorer and manifest, the level table
one test read and Terluna's water scenario, and was then generalised for any world: its five tools and three
tests hold both hashes and a note of each change, `tests/test_topography.py` is the lab's own, and the lab's
data manifest and specifications took over from the four files the generalisation removed.
On 2026-11-08 `climate/crm/cm1_output.py` came over byte for byte from Terluna at `bdda5a07`, with its test, whose
last check reads the pinned CM1 archive in place of Terluna's lunar build; both entries record that commit.
On 2026-11-11 `climate/gcm/surface_gust.py` and `climate/gcm/surface_similarity.py` came over from Terluna at
`39c5ee04` (branch `domain/climate`) with their tests, each changed as its entry records, with both hashes. The
Fortran edit lists are left out, since the patches are kept in `models/exoplasim/patches/`; `surface_gust.py`
includes the parts of Terluna's `pbl_scheme.py` and `pbl_fortran.py` that the depth rule shares; the similarity
takes the air's viscosity as an argument, derived for the world; and the tests compile the Fortran from the lab's
series applied to the pinned archive, through a fixture of the lab's own in `climate/tests/conftest.py`. That day
the gust's copy gave every number of Terluna's module bit for bit on that
module's 24 test columns, and the similarity's column agreed with Terluna's to 3 × 10⁻¹⁶ at the viscosity that
CM1's two lines share at 20 °C.
The same day `atmosphere/rain/` came over from Terluna at `39c5ee04`. `drops.py`, the single-drop solver, and
`sources.json`, Terluna's record of each source and of how far it was read, are Terluna's byte for byte. The solver
adapts the equations of K. Loftus's rainprops (github.com/kaitlyn-loftus/rainprops, commit `e2df9c2`, MIT licence),
which Terluna vendors whole; the lab keeps two of its files byte for byte under `atmosphere/rain/vendor/rainprops/`,
the licence and the transcription of Gunn and Kinzer's (1949) fall speeds that the solver's test on Earth reads,
with a record of their hashes and URLs. Where `drops.py` and `sources.json`, kept as Terluna wrote them, say that
rainprops' code is kept or vendored in `vendor/rainprops`, they describe Terluna's tree: the lab holds those two
files of it and none of its code. `breakup.py` and `fall_law.py` keep Terluna's functions and take any world's
air where Terluna's product builders took its target climates; `morrison.py`, the scheme's constants, is the lab's
own, with a test that reads each from the pinned CM1 archive. From the Open Moon's air the lab's modules returned
the numbers of Terluna's `rain_breakup.json` and `rain_fall_law.json` that were compared, the breakup scale with its
exponent, the five limits, the kernel ratio and the table's 903 entries, with no difference in any digit.
