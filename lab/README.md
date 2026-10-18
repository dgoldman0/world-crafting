# The lab

An integrated environment for studying found and crafted worlds with the adapted Earth models: a world is
described once, and ExoPlaSim and CM1, then SWAN, SWASH and other codes, are configured, built, run,
calibrated and analysed from that description. The first studies so described have Earth-like air under
gravity, rotation, sunlight, column mass and scale height far from Earth's, starting with the Open Moon,
beside which Earth runs as the Earth control.

Every product records its producer, its inputs and the values it read, from which the lab works out what a
changed parameter makes stale. A fit also records the states it was fitted on, against which the lab checks
each run that uses it.

**State (2026-10-18): coding plan stage 1. The loader, the derivations and the data manifest pass their checks.**

## Reading order

| Document | Holds |
|---|---|
| [design/inventory.md](design/inventory.md) | The ExoPlaSim and CM1 machinery as it stands: runners, builds, cases, calibration and reference tools, analyses, records, and the Moon's values within them |
| [design/regeneration.md](design/regeneration.md) | What each parameter's change requires producing again, by which command and at what cost; the loops; the steps Terluna performs by hand |
| [design/architecture.md](design/architecture.md) | The lab: principles, concepts, components, the stage graph, adapters, calibration envelopes, the registry of Earth assumptions, storage, jobs, decisions |
| [design/world_spec.md](design/world_spec.md) | The draft specification schema, with the Open Moon worked through value by value |
| [design/plan.md](design/plan.md) | The stages that build the lab, each with its acceptance check and its state |
| [worlds/](worlds/) | Seed worlds and scenarios: the Moon with the Open Moon at 1.2 and 1.0 atm, Earth as the control, and Mars with an illustrative 1 bar of Earth-like air |
| [configs/](configs/) | Each model's shared defaults, stated for any world: ExoPlaSim's, and CM1's with its variants and its lengths, times and rates given at a reference state |
| [studies/](studies/) | The Open Moon study: the design case's two GCM runs and three CM1 cases forced from the first, each extending its model's defaults; the subjects of plan stages 2 and 3 |
| [requirements.txt](requirements.txt) | The lab's Python environment, which holds ExoPlaSim and netCDF4, and how to build it; [local.example.toml](local.example.toml) names its folder and the other roots on a machine |
| [data/manifest.toml](data/manifest.toml) | The data the lab's stages read, each file with its source, size, hash, licence and credit; the lab's copies sit in the store |
| [registry/](registry/) | A seed of the registry of Earth assumptions: fourteen entries, eleven converted from the defect log and three from the models' patches, with the thresholds awaiting the author's decision marked "proposed" |

## What the lab is built from

| In this repository | Becomes |
|---|---|
| The `models/` patch series, pins and `check_patches.sh` | The single source of the builds' patches |
| The `python/` reference and calibration tools | The producers of reference columns, the curved-air ledger and the fits |
| `notes/defect_log.md` | The registry of Earth assumptions |
| `notes/verification_record.md` | The checks each stage runs and the evidence state each records |
| The notes' improvements in order of value | The order of model work once the lab can run it |
| `paper/tools/regime_calc.py`, `paper/data/worlds.json`, the paper's table of reach | The derived quantities and the reach report, with the paper's numbers as their first test |

The lab is self-contained: what it uses for its own work lives in this repository and the lab's store, the
Terluna data it needs among them, copied with their provenance. Terluna's run scripts, case definitions and
records stay where they are, and the lab's comparison tests read them there (design/architecture.md,
Principles).
