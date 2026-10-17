# World-crafting

Earth-built models carried to other worlds: the patches, new Fortran and in-house tools that let
ExoPlaSim (a general circulation model), CM1 (a cloud-resolving model, here with WRF-ELEC's storm
electrification) and SWAN (a spectral wave model) simulate a breathable Moon, the reference models
they were calibrated against, and the paper that describes the work.

The first world is Terluna's Open Moon (github.com/dgoldman0/Terluna): 1.2 atm of nitrogen and oxygen
at the water level, seas over 28% of the surface, sunlight filtered by a shield, lunar gravity and the
29.53-day solar day. The machinery came from Terluna at commit 186b294 (2026-10-17).

## Layout

| Folder | Holds |
|---|---|
| `models/exoplasim/` | Patches to ExoPlaSim 3.4.2's PlaSim source |
| `models/cm1/` | Patches to CM1 r22, the Fortran written for its electrified build, and the build variants |
| `models/swan/`, `models/swash/` | Patches to SWAN 41.51; SWASH 12.01's lunar settings |
| `python/` | In-house reference and calibration tools, under their Terluna package paths |
| `notes/` | Each component's correctness, limits and room for improvement |
| `paper/` | The paper: notes, sections, figures, data extracts, source records, review records |

`PROVENANCE.md` records every brought file's Terluna path and hash and every upstream pin. Work is in
progress; `paper/notes/plan.md` holds the build stages and their state.
