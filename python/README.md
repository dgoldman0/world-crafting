# In-house reference and calibration tools

The tools the ExoPlaSim and CM1 adaptations rest on, copied byte for byte from Terluna at 186b294 under
their Terluna package paths (`provenance.json` lists every file with its sha256; the geography package and one
test are modified, below). Import from this folder (`pytest` sets the path; elsewhere `PYTHONPATH=python`).

| Package | Holds | Notes |
|---|---|---|
| `atmosphere/radiative_convective/` | The line-by-line clear-sky radiative–convective column (HITRAN2020 lines, MT_CKD 4.3 continuum, collision-induced absorption, Rayleigh scattering; GM/r² hydrostatics; a pseudo-spherical solar beam) and the correlated-k thermal scheme built from the same spectroscopy. Every GCM and CM1 radiation calibration was fitted against it | [../notes/reference_radiation.md](../notes/reference_radiation.md) |
| `atmosphere/middle_atmosphere/` | `equilibrium.py`, `photolysis.py`, `chemistry.py`: the radiative–photochemical equilibrium column to 0.1 Pa that the surface-light model and the sky's optics build their columns from. Its escape and exobase modules stay in Terluna | Terluna's `METHODS.md`, copied here |
| `atmosphere/electricity/` (`conductivity.py`, `muons.py`, `charging.py`) | The lunar conductivity column the electrified CM1's leakage and screening read: ion production from the CRAC:CRII tables and MCEq muons, small ions' recombination, mobility and attachment to humidity-swollen aerosol; and the graupel-crystal charging laws integrated over size distributions (Saunders and Peck, Takahashi, with WRF-ELEC's critical rime accretion rates). Terluna's thunder, occurrence and tower scripts are analyses and stay there; the package README is Terluna's and still lists them | [../notes/electrification.md](../notes/electrification.md) |
| `atmosphere/waterworlds/` (`body.py`, `escape.py`, `steam.py`, `steam_optics.py`, `hitemp.py`, `radiating.py`, `balance.py`, `steam_table.py`, `maps.py`, `figures.py`, `comparison.py`, `column_check.py`, `fetch_inputs.py`) | The lab's own tools for low-gravity waterworlds after Arnscheidt, Wordsworth and Ding (2019), new on 2026-10-19 for plan stage 9: bodies of the size relation of Sotin et al. (2007), fixed by their surface gravity; the isothermal transonic wind of steam that carries their water away; columns of steam alone, saturated at every height, with their absorption line by line from the radiative–convective column's spectroscopy, summed directly where hot steam's lines grow broad; HITEMP2010's water lines, read in place from the zips that the lab's data manifest records in its store and cut at 1,000 K as the paper's model cut them, with MT_CKD's continuum held at 296 K in warmer layers as the lab reads that model; and the heights from which those columns emit and at which they absorb; the energy balance; the table of columns over gravity and surface temperature that the paper computes once; and the contours over gravity and distance at 273 K and at a lifetime; the curves of the paper's Figures 2 to 5, read from the images in its arXiv source, which `fetch_inputs.py` restores by hash into the git-ignored `inputs/`; and the comparison of the lab's steam worlds with them, with stage 9's acceptance check; and the check of HITEMP's lines on the radiative–convective column's own checked columns | [../notes/waterworlds.md](../notes/waterworlds.md) |
| `illumination/surface_light/`, `illumination/cloud_light/model.py` | Columns and sunlight for the sky solver and the curved-air ledger | |
| `illumination/sky/` | The spherical successive-orders sky solver and the solved-column sky | [../notes/sky_solver.md](../notes/sky_solver.md) |
| `climate/gcm/plasim_shortwave.py`, `plasim_longwave.py` | PlaSim's clear-sky shortwave and longwave arithmetic for one column, and the fitters for its corrections | [../notes/exoplasim.md](../notes/exoplasim.md) |
| `climate/gcm/plasim_ice_optics.py` | The ice optics of the `ice-optics` patch, in Python, with its PIFM two-stream | the same |
| `climate/gcm/twilight.py` | The curved-air ledger: what the Moon's tall, curved air does to sunlight and infrared against flat columns, and the terms the GCM and CM1 patches read | [../notes/reference_radiation.md](../notes/reference_radiation.md) |
| `climate/gcm/sun_check.py` | PlaSim's solar-position arithmetic, upstream and corrected, against a run's sunlight | [../notes/exoplasim.md](../notes/exoplasim.md) |
| `geography/` (`topography.py`, `basins.py`, `atlas.py`, `drainage.py`, `nomenclature.py`) | A body's heights above its geoid, from a PDS3 height image and a SHADR gravity field read through their labels, with the body's spin and the permanent tide of a host fixed in its sky; the common water level that floods a given share of the surface, and the connected seas below it; the atlas of seas, islands and flooded maria at that level; the steady routing of a GCM run's runoff into rivers and fill-and-spill lakes; and the IAU gazetteer's names. The lab's general versions of Terluna's lunar tools; Terluna's other geography tools (tides, groundwater, shores and coasts, the water inventory, the calendar) stay there | [../notes/geography.md](../notes/geography.md) |
| `climate/results/gcm/`, `atmosphere/*/results/`, `illumination/*/results/`, `protection/` | The committed products these tools wrote or read: the ledger (`twilight.json`), the gas-band fits, the longwave correction, the ice optics, the calibration and Sun checks, the middle-atmosphere cases the light models use, the shield's transmission | Data, with their producers' hashes inside |

## Running

```sh
python -m pytest python               # from the repository root: 225 tests
```

On 2026-10-17, after the electricity tools were added, all 111 passed in the research drive's `optics`
environment (Python 3.13.7, numpy 2.3.3, scipy 1.16.2, numba 0.68.0) with every input restored; the system Python, lacking numba, collects 77 and passes
them. Before that addition all 95 then present passed under Python 3.13 with numpy, scipy and numba 0.68, with the
spectroscopic inputs restored (176 MB for the radiative–convective model, fetched and hash-checked by
`python -m atmosphere.radiative_convective.fetch_inputs --download`; git-ignored). The 16 electricity tests
added the same day passed with their inputs restored (`python -m atmosphere.electricity.fetch_inputs
--download`: Takahashi's table, the CRAC:CRII tables and the PDG muon table, 0.7 MB, git-ignored; without
them three tests skip). `muons.py` needs MCEq, which Terluna keeps in a separate environment; its products
are committed. The geography package's 47 tests, on synthetic files, grids and fields, need no inputs; its
checks on the Moon's own heights and field, which the lab's data store holds, are in `lab/tests/test_geography.py`.
On 2026-10-18 the system Python (3.13.7, numpy 2.3.3, scipy 1.16.2), lacking numba, collected 124 tests and
passed 111: the sky solver's 34 stay uncollected, and without the inputs 13 skip. The waterworld tools' 67 tests,
added on 2026-10-19 and 2026-10-20, need no inputs but for these: sixteen read the spectroscopic inputs, two the
paper's source, and four HITEMP2010's zips in the lab's store, two of them with the spectroscopic inputs too. The ten
on HITEMP's lines also import the lab's data manifest (`lab/worldlab/data.py`), and one of the wind's tests takes the
mpmath package. The system Python then collected 191.

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
Python copy, to nine figures.

The geography package is the lab's general version of Terluna's, and `provenance.json` notes each file's changes.
Its tools take a body's grid, gravity field, rotation, tide and share as arguments, read PDS3 images and SHADR
tables through their labels, average the permanent tide over the host's eccentric orbit and its tilt to the
equator, and synthesise the geoid on the heights' own grid, which on LOLA's 16 pixels per degree removes the
0.17 m area-weighted rms, and 2.4 m at most, by which Terluna's interpolation from 4 pixels per degree erred.
The drainage summary lists lakes from label 1, where Terluna's reached label 0, the dry land, whenever fewer
than twelve lakes formed, and raised an OverflowError on its level of minus infinity. Terluna's input restorer, its manifest, the level table and the
water scenario gave way to the lab's data manifest and specifications. No other file differs from Terluna.
