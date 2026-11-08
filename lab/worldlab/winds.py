"""The largest winds of ExoPlaSim runs' output, the evidence for the guard on `timestep_min`, which compares them
with the advective limit of the step (lab/design/architecture.md, ExoPlaSim's guards). Reading the NetCDF output
needs netCDF4, which the lab's Python environment holds (lab/requirements.txt):

    PYTHONPATH=lab <env>/bin/python -m worldlab.winds <folder of run folders> <label>     # the record, on stdout

Each run folder holds its yearly output as model/MOST.<year>.nc and its namelists in model/.
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

from .derive import TRUNCATION_BY_LATITUDES

NOTE = ("The winds are the largest of each file's means over its levels and grid, 3-day means on the Moon, below the "
        "instantaneous winds of the run's steps. Every file holds finite winds, which the scan checks. The record "
        "shows the guard silent on these runs; holding no unstable run, it leaves the guard's warning ahead of "
        "instability untested.")


def largest_wind_m_s(path: Path) -> tuple[float, int]:
    """The largest wind speed, √(u² + v²), over one output file's means, levels and grid, and the file's latitude
    count. Only the variables' fill values are left out, as their attributes declare them or, undeclared, as
    netCDF's default; a file with a NaN or infinite wind is refused, since its run left its stable range."""
    import netCDF4
    import numpy as np
    with netCDF4.Dataset(path) as output:
        output.set_auto_mask(False)
        parts = []
        for name in ('ua', 'va'):
            variable = output[name]
            raw = np.asarray(variable[:])
            fills = [getattr(variable, key) for key in ('_FillValue', 'missing_value') if hasattr(variable, key)]
            fills = fills or [netCDF4.default_fillvals.get(raw.dtype.str[1:])]
            fill = np.zeros(raw.shape, dtype=bool)
            for value in fills:
                if value is not None:
                    fill |= raw == np.asarray(value, dtype=raw.dtype)
            parts.append((raw.astype(np.float64), fill))
        latitudes = output.dimensions['lat'].size
    (u, u_fill), (v, v_fill) = parts
    fill = u_fill | v_fill
    speed = np.sqrt(u ** 2 + v ** 2)
    unstable = int((~np.isfinite(speed) & ~fill).sum())
    if unstable:
        raise ValueError(f'{path}: {unstable} non-finite winds')
    if fill.all():
        raise ValueError(f'{path}: every wind is a fill value')
    return float(speed[~fill].max()), int(latitudes)


def _entry(path: Path, key: str) -> float:
    match = re.search(rf'^\s*{key}\s*=\s*([-+0-9.eE]+)', path.read_text(), re.M) if path.exists() else None
    if match is None:
        raise ValueError(f'{path}: no {key}')
    return float(match.group(1))


def scan(folder: Path) -> tuple[dict, int]:
    """Each run's largest wind over all its yearly output, with the model year and grid it occurred on, and the
    run's time step and radius as its namelists hold them; and the number of files read."""
    runs, files = {}, 0
    for path in sorted(Path(folder).glob('*/model/MOST.*.nc')):
        run, year = path.parts[-3], int(path.stem.split('.')[1])
        speed, latitudes = largest_wind_m_s(path)
        files += 1
        best = runs.get(run)
        if best is None or speed > best['m_s']:
            runs[run] = dict(m_s=speed, model_year=year, latitudes=latitudes)
    for run, best in runs.items():
        model = Path(folder) / run / 'model'
        if best['latitudes'] not in TRUNCATION_BY_LATITUDES:
            raise ValueError(f'{run}: {best["latitudes"]} latitudes, on no grid of ExoPlaSim\'s')
        best.update(truncation=TRUNCATION_BY_LATITUDES[best['latitudes']],
                    timestep_min=_entry(model / 'plasim_namelist', 'MPSTEP'),
                    radius_m=_entry(model / 'planet_namelist', 'PLARAD'))
    return runs, files


def record(folder: Path, label: str) -> dict:
    """The validation record of a folder of runs, `label` naming the folder as a pin would."""
    runs, files = scan(folder)
    return dict(schema='worldlab.validation/0',
                check="the time-step guard: each run's largest wind against the advective limit of its step",
                made=datetime.date.today().isoformat(),
                made_by=f'PYTHONPATH=lab <env>/bin/python -m worldlab.winds <folder> {label}',
                source=f'{label}/*/model/MOST.*.nc', files=files, note=NOTE, runs=runs)


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print('usage: python -m worldlab.winds <folder of run folders> <label>', file=sys.stderr)
        return 2
    print(json.dumps(record(Path(args[0]), args[1]), indent=1))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
