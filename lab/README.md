# The lab

An integrated environment for studying found and crafted worlds with the adapted Earth models: a world is
described once, and ExoPlaSim and CM1, then SWAN, SWASH and other codes, are configured, built, run,
calibrated and analysed from that description. The first worlds so described have Earth-like air and differ
from Earth in gravity, rotation, sunlight, column mass and scale height, starting with the Open Moon,
beside which Earth runs as the Earth control.

Every product records its producer, its inputs and the values it read, from which the lab works out what a
changed parameter makes stale. A fit also records the states it was fitted on, against which the lab checks
each run that uses it.

**State (2026-10-17): design.**

## Reading order

| Document | Holds |
|---|---|
| [design/inventory.md](design/inventory.md) | The ExoPlaSim and CM1 machinery as it stands: runners, builds, cases, calibration and reference tools, analyses, records, and the Moon's values within them |
| [design/regeneration.md](design/regeneration.md) | What each parameter's change requires producing again, by which command and at what cost; the loops; the steps Terluna performs by hand |
| [design/architecture.md](design/architecture.md) | The lab: principles, concepts, components, the stage graph, adapters, calibration envelopes, the registry of Earth assumptions, storage, jobs, decisions |
| [design/world_spec.md](design/world_spec.md) | The draft specification schema, with the Open Moon worked through value by value |
| [design/plan.md](design/plan.md) | The stages that build the lab, each with its acceptance check and its state |
| [worlds/](worlds/) | Seed worlds and scenarios: the Moon with the Open Moon at 1.2 and 1.0 atm, Earth as the control, and Mars with an illustrative 1 bar of Earth-like air |
| [configs/](configs/), [experiments/](experiments/) | ExoPlaSim and CM1 set up as Terluna runs them, with two of its GCM experiments and three of its CM1 cases written against them: the targets of plan stages 2 and 3 |
| [registry/](registry/) | A seed of the registry of Earth assumptions: eleven entries converted from the defect log, with the thresholds awaiting the author's decision marked "proposed" |

## What the lab is built from

| In this repository | Becomes |
|---|---|
| The `models/` patch series, pins and `check_patches.sh` | The single source of the builds' patches |
| The `python/` reference and calibration tools | The producers of reference columns, the curved-air ledger and the fits |
| `notes/defect_log.md` | The registry of Earth assumptions |
| `notes/verification_record.md` | The checks each stage runs and the evidence state each records |
| The notes' improvements in order of value | The order of model work once the lab can run it |
| `paper/tools/regime_calc.py`, `paper/data/worlds.json`, the paper's table of reach | The derived quantities and the reach report, with the paper's numbers as their first test |

Terluna's runners, case definitions and records remain where they are, and the lab only reads them. Under
the proposed decisions (design/architecture.md), runs continue in Terluna until the lab reproduces their
inputs byte for byte.
