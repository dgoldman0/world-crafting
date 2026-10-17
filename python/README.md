# In-house reference and calibration tools

The tools the ExoPlaSim and CM1 adaptations rest on, copied byte for byte from Terluna at 186b294 under
their Terluna package paths (`provenance.json` lists every file with its sha256; one test is modified,
below). Import from this folder (`pytest` sets the path; elsewhere `PYTHONPATH=python`).

| Package | Holds | Notes |
|---|---|---|
| `atmosphere/radiative_convective/` | The line-by-line clear-sky radiative–convective column (HITRAN2020 lines, MT_CKD 4.3 continuum, collision-induced absorption, Rayleigh scattering; GM/r² hydrostatics; a pseudo-spherical solar beam) and the correlated-k thermal scheme built from the same spectroscopy. Every GCM and CM1 radiation calibration was fitted against it | [../notes/reference_radiation.md](../notes/reference_radiation.md) |
| `atmosphere/middle_atmosphere/` | `equilibrium.py`, `photolysis.py`, `chemistry.py`: the radiative–photochemical equilibrium column to 0.1 Pa that the surface-light model and the sky's optics build their columns from. Its escape and exobase modules stay in Terluna | Terluna's `METHODS.md`, copied here |
| `illumination/surface_light/`, `illumination/cloud_light/model.py` | Columns and sunlight for the sky solver and the curved-air ledger | |
| `illumination/sky/` | The spherical successive-orders sky solver and the solved-column sky | [../notes/sky_solver.md](../notes/sky_solver.md) |
| `climate/gcm/plasim_shortwave.py`, `plasim_longwave.py` | PlaSim's clear-sky shortwave and longwave arithmetic for one column, and the fitters for its corrections | [../notes/exoplasim.md](../notes/exoplasim.md) |
| `climate/gcm/plasim_ice_optics.py` | The ice optics of the `ice-optics` patch, in Python, with its PIFM two-stream | the same |
| `climate/gcm/twilight.py` | The curved-air ledger: what the Moon's tall, curved air does to sunlight and infrared against flat columns, and the terms the GCM and CM1 patches read | [../notes/reference_radiation.md](../notes/reference_radiation.md) |
| `climate/gcm/sun_check.py` | PlaSim's solar-position arithmetic, upstream and corrected, against a run's sunlight | [../notes/exoplasim.md](../notes/exoplasim.md) |
| `climate/results/gcm/`, `atmosphere/*/results/`, `illumination/*/results/`, `protection/` | The committed products these tools wrote or read: the ledger (`twilight.json`), the gas-band fits, the longwave correction, the ice optics, the calibration and Sun checks, the middle-atmosphere cases the light models use, the shield's transmission | Data, with their producers' hashes inside |

## Running

```sh
python -m pytest                      # from the repository root: 95 tests
```

On 2026-10-17 all 95 passed under Python 3.13 with numpy, scipy and numba 0.68, with the spectroscopic
inputs restored (176 MB for the radiative–convective model, fetched and hash-checked by
`python -m atmosphere.radiative_convective.fetch_inputs --download`; git-ignored). Without numba the sky
solver's 29 tests are not collected; without the inputs 10 tests skip.

## What still needs Terluna

The column arithmetic, the reference models and their tests run here. Five entry points read Terluna's GCM
output or case modules and run only inside a Terluna checkout; they are kept unmodified so that their
provenance stays exact:

- `plasim_shortwave.py`: `validate`, `fit`, `water` (they read GCM output through Terluna's
  `climate/gcm/radiation_check.py` and the planet through `climate/crm/cm1_run.py`);
- `plasim_longwave.py`: `validate`, `fit` (Terluna's `cm1_run.planet`, `crm/gcm_heating.py`,
  `crm/ring_radiation.py`, and the run's netCDF output);
- `sun_check.py`: `check` (a run folder, and `crm/ring_crossings.rounded` for output rounding);
- `twilight.py`: `ledger` and `plasim_column` (Terluna's `exoplasim_run` for the design run's configuration,
  and optics and scattering caches on the research drive; a full regeneration takes about 40 minutes of
  scattering on six threads).

A port to another world replaces those imports with a small configuration module.

## Changed from Terluna

`climate/tests/test_plasim_ice_optics.py::test_the_fortran_patch_matches_its_python_copy` compiles the ice
routines taken from the committed patch `models/exoplasim/patches/10-ice-optics.patch` where Terluna's test
took them from the runner's Python string; it checks the patch this repository distributes against the
Python copy, to nine figures. No other file differs from Terluna.
