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

The in-house reference and calibration tools under `python/` were copied byte for byte from Terluna at
186b294, under their Terluna package paths; `python/provenance.json` lists all 98 files with their sha256.
One file differs: `python/climate/tests/test_plasim_ice_optics.py` takes the ice routines it compiles from
`models/exoplasim/patches/10-ice-optics.patch` in place of the runner's Python string (both hashes recorded).
