# The lab

An integrated environment for studying found and crafted worlds with the adapted Earth models: a world is
described once, and ExoPlaSim and CM1, then SWAN, SWASH and other codes, are configured, built, run,
calibrated and analysed from that description. The lab's test case is the Open Moon, Earth-like air under
gravity, rotation, sunlight, column mass and scale height far from Earth's, compared with Terluna's results, with
Earth beside it as the Earth control. Its flagship study is a family of low-gravity waterworlds, in steam and in
Gaean air ([design/waterworlds.md](design/waterworlds.md)).

Every product records its producer, its inputs and the values it read, from which the lab works out what a
changed parameter makes stale. A fit also records the states it was fitted on, against which the lab checks
each run that uses it.

**State (2026-10-19): plan stages 1 and 2 passed; the waterworld study planned as stages 9 to 13, with stage 9
under way. Since 2026-11-18 the thin path of stages 3, 4, 6 and 7 builds CM1, writes a forced site box's case, checks
it against the registry and runs it in segments under the lab's own bookkeeping ([design/plan.md](design/plan.md)).**

The commands, from the repository's root, with the lab's Python environment (`lab/local.toml`, `[roots] env`):

```sh
PYTHONPATH=lab:python <env>/bin/python -m worldlab plan open-moon-couplings              # boxes, keys, cost, checks
PYTHONPATH=lab:python <env>/bin/python -m worldlab build open-moon-couplings sea_imposed  # its CM1 build
PYTHONPATH=lab:python <env>/bin/python -m worldlab case open-moon-couplings sea_imposed   # its case
PYTHONPATH=lab:python <env>/bin/python -m worldlab run open-moon-couplings sea_imposed --segments 1   # a model day
PYTHONPATH=lab:python <env>/bin/python -m worldlab status open-moon-couplings sea_imposed
```

`run` resumes from the run's last recorded segment and takes `--override ID=justification` for a registry entry that
stops it; `stop` ends a run after the segment under way, and `read` gives a box's rain and ascent over solar days.

Following Terluna's comparison of CM1 boxes with the GCM, stage 3 forces CM1 through the whole column, holding the
air to the GCM's only above the GCM's convection, and the ExoPlaSim runs of stages 8 and 12 gain level sets and a
convection setting ([design/plan.md](design/plan.md), stage 3 and "The GCM's convection, boundary layer and
levels"). The repository's root README lists the findings beside the paper's passages they change ("Where current
understanding differs from the paper").

## Reading order

| Document | Holds |
|---|---|
| [design/inventory.md](design/inventory.md) | The ExoPlaSim and CM1 machinery as it stands: runners, builds, cases, calibration and reference tools, analyses, records, and the Moon's values within them |
| [design/regeneration.md](design/regeneration.md) | What each parameter's change requires producing again, by which command and at what cost; the loops; the steps Terluna performs by hand |
| [design/architecture.md](design/architecture.md) | The lab: principles, concepts, components, the stage graph, adapters, calibration envelopes, the registry of Earth assumptions, storage, jobs, decisions |
| [design/world_spec.md](design/world_spec.md) | The draft specification schema, with the Open Moon worked through value by value |
| [design/plan.md](design/plan.md) | The stages that build the lab, each with its acceptance check and its state |
| [design/waterworlds.md](design/waterworlds.md) | The flagship study: low-gravity waterworlds after Arnscheidt, Wordsworth and Ding (2019), in steam, in Gaean air and with protection where needed |
| [design/terluna_fixes.md](design/terluna_fixes.md) | Terluna's fixes of October and November weighed for the lab: each one's general form, the worlds where it holds and where it is untested, one component or several, and its cost |
| [design/gap_series.md](design/gap_series.md) | The gap between ExoPlaSim and CM1, whose closing moved here from Terluna on 9 November 2026: a proposed series on Earth, an all-ocean twin of the Moon and the Moon that separates its causes, Earth first, and MITgcm, weighed and left out for now |
| [worlds/](worlds/) | Seed worlds and scenarios: the Moon with the Open Moon at 1.2 and 1.0 atm, Earth as the control, and Mars with an illustrative 1 bar of Earth-like air; the 1.0 atm scenario and Mars wait as later additions |
| [configs/](configs/) | Each model's shared defaults, stated for any world: ExoPlaSim's, and CM1's with its variants and its lengths, times and rates given at a reference state |
| [studies/](studies/) | The Open Moon study: the design case's two GCM runs and three CM1 cases forced from the first, each extending its model's defaults; the subjects of plan stages 2 and 3. The coupling test's study: four sea boxes over the Near-side Sea that test the couplings of a CM1 box to the GCM, and a fifth that waits on the weak temperature gradient's patch |
| [requirements.txt](requirements.txt) | The lab's Python environment, which holds ExoPlaSim and netCDF4, and how to build it; [local.example.toml](local.example.toml) names its folder and the other roots on a machine |
| [data/manifest.toml](data/manifest.toml) | The data the lab's stages read, each file with its source, size, hash, licence and credit; the lab's copies sit in the store |
| [registry/](registry/) | A seed of the registry of Earth assumptions: twenty-five entries, seventeen under the defect log's ids and eight named by model, with the thresholds awaiting the author's decision marked "proposed"; `worldlab.registry` evaluates a CM1 case's entries before it is written and before each run |

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
