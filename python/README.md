# In-house reference and calibration tools

The tools the ExoPlaSim and CM1 adaptations rest on, copied byte for byte from Terluna at 186b294 under
their Terluna package paths (`provenance.json` lists every file with its sha256 and, where another commit is its
source, that commit; the geography package, the surface transfer's two modules, the rain package's two, PlaSim's rain
from its drops, PlaSim's levels and twelve tests are modified, below).
Import from this folder (`pytest` sets the path; elsewhere `PYTHONPATH=python`).

| Package | Holds | Notes |
|---|---|---|
| `atmosphere/radiative_convective/` | The line-by-line clear-sky radiative–convective column (HITRAN2020 lines, MT_CKD 4.3 continuum, collision-induced absorption, Rayleigh scattering; GM/r² hydrostatics; a pseudo-spherical solar beam) and the correlated-k thermal scheme built from the same spectroscopy. Every GCM and CM1 radiation calibration was fitted against it | [../notes/reference_radiation.md](../notes/reference_radiation.md) |
| `atmosphere/middle_atmosphere/` | `equilibrium.py`, `photolysis.py`, `chemistry.py`: the radiative–photochemical equilibrium column to 0.1 Pa that the surface-light model and the sky's optics build their columns from. Its escape and exobase modules stay in Terluna | Terluna's `METHODS.md`, copied here |
| `atmosphere/electricity/` (`conductivity.py`, `muons.py`, `charging.py`) | The lunar conductivity column the electrified CM1's leakage and screening read: ion production from the CRAC:CRII tables and MCEq muons, small ions' recombination, mobility and attachment to humidity-swollen aerosol; and the graupel-crystal charging laws integrated over size distributions (Saunders and Peck, Takahashi, with WRF-ELEC's critical rime accretion rates). Terluna's thunder, occurrence and tower scripts are analyses and stay there; the package README is Terluna's and still lists them | [../notes/electrification.md](../notes/electrification.md) |
| `atmosphere/waterworlds/` (`body.py`, `escape.py`, `steam.py`, `steam_optics.py`, `hitemp.py`, `radiating.py`, `balance.py`, `steam_table.py`, `maps.py`, `figures.py`, `comparison.py`, `column_check.py`, `sampling.py`, `fetch_inputs.py`) | The lab's own tools for low-gravity waterworlds after Arnscheidt, Wordsworth and Ding (2019), new on 2026-10-19 for plan stage 9: bodies of the size relation of Sotin et al. (2007), fixed by their surface gravity; the isothermal transonic wind of steam that carries their water away; columns of steam alone, saturated at every height, with their absorption line by line from the radiative–convective column's spectroscopy, summed directly where hot steam's lines grow broad; HITEMP2010's water lines, read in place from the zips that the lab's data manifest records in its store and cut at 1,000 K as the paper's model cut them, with MT_CKD's continuum held at 296 K in warmer layers as the lab reads that model; and the heights from which those columns emit and at which they absorb; the energy balance; the table of columns over gravity and surface temperature that the paper computes once; and the contours over gravity and distance at 273 K and at a lifetime; the curves of the paper's Figures 2 to 5, read from the images in its arXiv source, which `fetch_inputs.py` restores by hash into the git-ignored `inputs/`; and the comparison of the lab's steam worlds with them, with stage 9's acceptance check; the check of HITEMP's lines on the radiative–convective column's own checked columns, rebuilt or PyRADS's own; and the test of the paper's spectral sampling | [../notes/waterworlds.md](../notes/waterworlds.md) |
| `atmosphere/rain/` (`drops.py`, `breakup.py`, `fall_law.py`, `morrison.py`, `warm_rain.py`) | Rain for CM1's Morrison scheme on any world, and the fall law for PlaSim's patch 14. Terluna's single-drop solver, after Loftus and Wordsworth (2021), gives terminal speeds in a world's air at 2 m; from them come the size scale of raindrop breakup against Earth's with its exponent on the air's density, the scheme's limits as patch 03 of the lab's CM1 series sets them, the table of the fall law's three moments that patch 04 reads, and the rate of rain's self-collection. `warm_rain.py` gives the two factors that patch 05 puts on the scheme's autoconversion and accretion at a world's gravity. `morrison.py` states the scheme's constants as the pinned CM1 source has them. `sources.json` is Terluna's record of each source and of how far it was read, and `vendor/rainprops/` keeps the MIT licence of Loftus's rainprops, whose equations the solver adapts, with its transcription of Gunn and Kinzer's fall speeds. Terluna's products for its three target climates, its survival and arrival tools and its recovered solver stay there | [../notes/cm1.md](../notes/cm1.md), "Fall speeds"; [../models/cm1/README.md](../models/cm1/README.md) |
| `illumination/surface_light/`, `illumination/cloud_light/model.py` | Columns and sunlight for the sky solver and the curved-air ledger | |
| `illumination/sky/` | The spherical successive-orders sky solver and the solved-column sky | [../notes/sky_solver.md](../notes/sky_solver.md) |
| `climate/gcm/plasim_shortwave.py`, `plasim_longwave.py` | PlaSim's clear-sky shortwave and longwave arithmetic for one column, and the fitters for its corrections | [../notes/exoplasim.md](../notes/exoplasim.md) |
| `climate/gcm/plasim_ice_optics.py` | The ice optics of the `ice-optics` patch, in Python, with its PIFM two-stream | the same |
| `climate/gcm/surface_gust.py`, `surface_similarity.py` | PlaSim's surface transfer on one column, in Python: as released, with Beljaars's gust in the bulk formulas' wind, and with CM1's surface-layer similarity over ice-free water at the world's viscosity; the copies that the Fortran of patches 12 and 13 is tested against | the same |
| `climate/gcm/rain_drops.py` | PlaSim's falling rain evaporated from its drops' sizes and fall speeds, on columns of any world, in Python: the copy that the Fortran of patch 14 is tested against. For a world's air at 2 m and a calibration of the rain's births it gives the entries of rainmod's namelist and, through `atmosphere/rain/fall_law.py`, the table of the fall law that the run's folder holds. It records Terluna's calibration of the births for the Open Moon | the same; [../models/exoplasim/README.md](../models/exoplasim/README.md), "Rain from drop sizes" |
| `climate/gcm/levels.py` | PlaSim's vertical levels for a world: the released model's half levels in the compiled model's doubles; the set generated from a scale height and the heights a study states for the half levels near the ground, under a stated count of the released model's highest half levels; the entries of a run on a generated set, `NEQSIG` −1, `SIGH` and `TFRC`; and the conservative remap in σ that carries a restart from one set onto another. It records Terluna's values for the Open Moon's fifteen levels | the same; [../models/exoplasim/README.md](../models/exoplasim/README.md), "Level sets" |
| `climate/gcm/twilight.py` | The curved-air ledger: what the Moon's tall, curved air does to sunlight and infrared against flat columns, and the terms the GCM and CM1 patches read | [../notes/reference_radiation.md](../notes/reference_radiation.md) |
| `climate/gcm/sun_check.py` | PlaSim's solar-position arithmetic, upstream and corrected, against a run's sunlight | [../notes/exoplasim.md](../notes/exoplasim.md) |
| `geography/` (`topography.py`, `basins.py`, `atlas.py`, `drainage.py`, `nomenclature.py`) | A body's heights above its geoid, from a PDS3 height image and a SHADR gravity field read through their labels, with the body's spin and the permanent tide of a host fixed in its sky; the common water level that floods a given share of the surface, and the connected seas below it; the atlas of seas, islands and flooded maria at that level; the steady routing of a GCM run's runoff into rivers and fill-and-spill lakes; and the IAU gazetteer's names. The lab's general versions of Terluna's lunar tools; Terluna's other geography tools (tides, groundwater, shores and coasts, the water inventory, the calendar) stay there | [../notes/geography.md](../notes/geography.md) |
| `climate/results/gcm/`, `atmosphere/*/results/`, `illumination/*/results/`, `protection/` | The committed products these tools wrote or read: the ledger (`twilight.json`), the gas-band fits, the longwave correction, the ice optics, the calibration and Sun checks, the middle-atmosphere cases the light models use, the shield's transmission | Data, with their producers' hashes inside |

## Running

```sh
python -m pytest python               # from the repository root: 360 tests, the sky solver's 34 among them
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
passed 111: the sky solver's 34 stay uncollected, and without the inputs 13 skip. The waterworld tools' 70 tests,
added on 2026-10-19 and 2026-10-20, need no inputs but for these: sixteen read the spectroscopic inputs, two the
paper's source, four HITEMP2010's zips in the lab's store, two of them with the spectroscopic inputs too, and one a
PyRADS checkout beside the store. The ten on HITEMP's lines and the one on PyRADS's columns also import the lab's
`worldlab` package, and one of the wind's tests takes the mpmath package. The system Python then collected 194.
CM1's output conventions brought six tests on 2026-11-08, and the gust and the similarity over water sixteen on
2026-11-11, of which eight apply the lab's patch series to the pinned ExoPlaSim archive in `upstream/` with `patch`
and six of those compile its `surflx` with gfortran; without the archive or the tools they skip. The system Python,
lacking numba, then collected 216 and passed them, and the lab's environment, which lacks mpmath as well, passed
215 and skipped the one test that takes it. CM1's rain brought 49 on 2026-11-11: 36 of the single-drop solver, the
breakup scale and the fall law, which need no inputs but for one that reads the pinned CM1 archive, and 13 of the
lab's patches 03 and 04, which apply the CM1 series to that archive with `patch`; ten of those compile one column
of the Morrison scheme with gfortran and cpp, and without the archive or the tools they skip. The warm rain's factors
brought six more the same day: two of the factors and the scheme's constants, one of which reads the pinned archive,
and four of the lab's patch 05, three of which compile the column. PlaSim's rain from its drops brought fifteen that
day: seven in Python alone, one that reads Morrison's closures from the pinned CM1 archive and the patch's from the
ExoPlaSim series, and seven of the lab's patch 14, which apply that series to the pinned ExoPlaSim archive; six of
those compile `mkrain` with gfortran, and without the archives or the tools they skip. The lab's environment then
collected 286 and passed 285. PlaSim's levels brought forty that day, in Python alone and with no inputs, with which
the lab's environment collected 326.

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
Python copy, to nine figures. `climate/tests/test_cm1_output.py`, from Terluna at `bdda5a07`, reads CM1's
conventions from the pinned CM1 archive in its last check, where Terluna's read its lunar build.

`climate/gcm/surface_gust.py` and `surface_similarity.py`, with their tests, came from Terluna at `39c5ee04`. Their
Fortran is in `models/exoplasim/patches/12-surface-gust.patch` and `13-similarity-over-water.patch`, where
Terluna's modules keep it as edit lists for its runner, and the tests compile `surflx` from the series applied to
the pinned archive, which a fixture of the lab's own supplies once in a session (`climate/tests/conftest.py`).
`surface_gust.py` includes the parts of Terluna's `pbl_scheme.py` and `pbl_fortran.py` that the
gust's depth rule shares with the nonlocal boundary layer, a scheme the series has no patch for.
`similarity_column` takes the air's kinematic viscosity as an argument, which `surface_transfer` derives from the
column's surface pressure, gas constant and lowest level's temperature with Sutherland's law, where Terluna's module
held CM1's two values for Earth's sea-level air (`cm1_viscosity` keeps CM1's line). The tests of Terluna's runner
and of its nonlocal scheme's depth stay in Terluna; in their place the tests here check the depth by hand
arithmetic at Earth's gravity and the Moon's and pin numbers that Terluna's modules gave.

`atmosphere/rain/` came from Terluna at `39c5ee04` (branch `domain/climate`) on 2026-11-11. `drops.py`,
`sources.json` and the two files of the vendored rainprops are Terluna's byte for byte; where the first two say that
rainprops' code is kept or vendored in `vendor/rainprops`, they describe Terluna's tree, of which the lab holds the
licence and the Gunn–Kinzer fall speeds alone. `breakup.py` and `fall_law.py` keep Terluna's functions and leave out
its product builders, which read its three target climates and write the Moon's values; in their place
`density_exponent`, `limits`, `table`, `self_collection` and `settings` take any world's air at 2 m, and
`fall_law.table_text` writes the table as Terluna's runner does. The lab's `morrison.py` states the scheme's
constants, which Terluna keeps in a later `shared/constants.json` than the copy pinned here, and `warm_rain.py`,
with its test, is the lab's own. The three tests run the
same calculation on the Open Moon's air and pin the numbers of Terluna's products, beside hand arithmetic at the
Moon's gravity and Earth's; the two tests of the recovered solver's vapour diffusivity stay in Terluna with
`recovered.py`. `climate/tests/test_cm1_rain.py` is the lab's own: it compiles one column of the Morrison scheme from
the lab's series on the pinned CM1 archive (`climate/tests/conftest.py`, `cm1_series`), where Terluna's tests of its
rain patches read its runner's edit lists.

`climate/gcm/rain_drops.py` and its test came from Terluna at `39c5ee04` on 2026-11-11. The Fortran is in
`models/exoplasim/patches/14-rain-from-drop-sizes.patch`, where Terluna's module keeps it as an edit list with the
Moon's fall law written into it. Terluna's module reads its lunar products when it is imported, the fall law, the
self-collection rate and the density exponent; here `mkrain` and the functions under it take the fall law and the
six settings as arguments, `settings` computes them for any world's air through `atmosphere/rain/fall_law.py`, and
`law_from_text` reads the table's text as the model reads it. Morrison's constants come from the lab's
`atmosphere/rain/morrison.py`, which gains his evaporation closures. The snow's sublimation by its flakes, which
Terluna's `mkrain` also calls, stays in Terluna until its assessment (`PLAN.md`). The test takes the Fortran from the
lab's series, adds Earth-like columns on ten levels beside Terluna's lunar ones on fifteen, checks the copy against
hand arithmetic on a power law's closed forms, the stops and the identity under two sets of flags, and pins the
numbers that Terluna's module gave on its own test columns; the tests of Terluna's runner and of its edit lists
stay in Terluna.

`climate/gcm/levels.py` and its test came from Terluna at `39c5ee04` on 2026-11-11. Terluna's module holds three
named sets, PlaSim's ten and the fourteen and fifteen levels it placed by hand for the Open Moon at a 51 km scale
height, with the entries of a run on a set and the remap of a restart. Here `generate` returns a world's set from a
scale height, a count of the released model's highest half levels and the heights a study states below them, and
`TERLUNA_OPEN_MOON_LEVELS` records the values from which it returns Terluna's fifteen, and without the last height
its fourteen, at the four places Terluna states them. `plasim_half` multiplies the released formula's powers out, as
the compiled model does, where Terluna's takes numpy's powers, so that two of the fifteen doubles differ from
Terluna's in the last bit. The remap's arithmetic is Terluna's, with the two grids checked first, and on Terluna's
grids its matrices equalled that module's in a single scratch run; `carry_restart` reads the horizontal sizes from
the restart's own records, where Terluna's holds T21's, and writes to a new path alone;
`namelist_entries` returns values for the lab's writer; and Terluna's command line stays there. The test keeps
Terluna's checks of the sets' placement, of a run's entries, of the remap and of a carried restart, on sets the rule
generates, and adds the rule against hand arithmetic, the released half levels' doubles, Earth's values, a restart
carried onto its own set and the refusals; the tests of Terluna's runner and of its products on the two sets stay in
Terluna, and the compiled model's tests are in `lab/tests/test_builds.py`.

The geography package is the lab's general version of Terluna's, and `provenance.json` notes each file's changes.
Its tools take a body's grid, gravity field, rotation, tide and share as arguments, read PDS3 images and SHADR
tables through their labels, average the permanent tide over the host's eccentric orbit and its tilt to the
equator, and synthesise the geoid on the heights' own grid, which on LOLA's 16 pixels per degree removes the
0.17 m area-weighted rms, and 2.4 m at most, by which Terluna's interpolation from 4 pixels per degree erred.
The drainage summary lists lakes from label 1, where Terluna's reached label 0, the dry land, whenever fewer
than twelve lakes formed, and raised an OverflowError on its level of minus infinity. Terluna's input restorer, its manifest, the level table and the
water scenario gave way to the lab's data manifest and specifications. No other file differs from Terluna.
