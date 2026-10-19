"""The steam columns' table over surface gravity and surface temperature, the radiation the paper computes once
before it solves the energy balance (Arnscheidt, Wordsworth and Ding 2019, section 3).

For each gravity and surface temperature of the grid the table holds the column's outgoing longwave, its emitting
surface's height and scaling factor, and for each star's temperature its absorbing surface's height and scaling
factor, with the shares of each mean whose depth reaches one within the top layer. Before the columns, every layer
state they will ask for, which depends on the surface temperature and, through the cap at the critical radius, on
gravity, is computed once into the optics' cache; the columns then read it. Each column runs in a worker of its own
and reports a line when it ends; a column that fails is recorded with its error, its values left NaN, and the table
is written with the rest.

The table's key covers its inputs and its producer: the grid, the stars, the levels, the bands, the optics' key
(lines, partition sums, continuum, method and version), the layers' gravity, the angles, the code of every module
that turns cross-sections into the table, shared/constants.json, and the versions of Python, numpy and scipy. Its
header states its evidence.

    python -m atmosphere.waterworlds.steam_table --store STORE \\
        --gravities 1.1:2.6:0.1 --temperatures 220:600:5 --stars 5772,3400 --processes 6

With --store the table lands at STORE/products/steam-table/<key>/table.json, the key being the first 16 hex digits of
the sha256 of its inputs and producer, and the optics' cache at STORE/caches/steam-optics/ (lab/design/architecture.md,
the store); --out and --cache place them elsewhere.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import datetime
import hashlib
import json
import math
import multiprocessing as mp
import os
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy

from atmosphere.radiative_convective import fetch_inputs
from atmosphere.waterworlds import radiating as rd, steam, steam_optics as so
from atmosphere.waterworlds.body import Waterworld

SCHEMA = 'world-crafting.waterworlds.steam-table/2'
PYTHON_ROOT = Path(__file__).resolve().parents[2]
PRODUCER_FILES = ('atmosphere/waterworlds/steam_table.py', 'atmosphere/waterworlds/steam.py',
                  'atmosphere/waterworlds/steam_optics.py', 'atmosphere/waterworlds/radiating.py',
                  'atmosphere/waterworlds/body.py', 'atmosphere/waterworlds/escape.py',
                  'atmosphere/radiative_convective/longwave.py', 'atmosphere/radiative_convective/thermodynamics.py',
                  'atmosphere/radiative_convective/spectroscopy.py', 'shared/constants.py', 'shared/constants.json')
N_ANGLES = 4
EVIDENCE = ('A calculation: clear-sky, plane-parallel radiative transfer through columns of saturated steam on '
            'HITRAN2020 lines and MT_CKD 4.3, with heights from hydrostatic balance under GM/r^2; numerically '
            'converged as notes/waterworlds.md records; compared with the paper in plan stage 9; physically '
            'unvalidated.')
ARRAYS = ('olr', 'z_lw', 'lw_factor', 'lw_top_share', 'z_sw', 'sw_factor', 'sw_top_share')


def span(text: str) -> list[float]:
    """The grid start:stop:step, its last value at or below stop."""
    start, stop, step = (float(v) for v in text.split(':'))
    if not step > 0 or stop < start:
        raise ValueError(f'{text}: a grid takes a positive step and a stop at or above its start')
    return [round(start + i * step, 10) for i in range(int(math.floor((stop - start) / step + 1e-9)) + 1)]


def producer() -> dict:
    """The code and environment that make the table."""
    return dict(module='atmosphere.waterworlds.steam_table',
                sources={name: hashlib.sha256((PYTHON_ROOT / name).read_bytes()).hexdigest() for name in PRODUCER_FILES},
                environment=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__))


_COLUMN_OPTICS: dict = {}


def _fill(job) -> None:
    band, p, t = job
    so._WORKER['optics'].cross_section(band, p, t)       # into the cache; nothing returns to the parent


def _column(job):
    g, t_s, stars, levels, bands, cache, optical_gravity = job
    world = Waterworld.from_gravity(g)
    col = steam.column(world, t_s, levels, optical_gravity=optical_gravity)
    return rd.surfaces(col, rd.column_spectra(col, _COLUMN_OPTICS[str(cache)], bands, n_angles=N_ANGLES), stars)


def compute(gravities, temperatures, stars, *, cache: Path, levels=steam.Levels(), bands=so.BANDS,
            optical_gravity: str = 'surface', processes: int = 1, report=print) -> dict:
    """The table, its arrays indexed [gravity, temperature] and [star, gravity, temperature]."""
    if fetch_inputs.restore()['status'] != 'PASS':
        raise ValueError('the spectroscopic inputs are missing or changed (fetch_inputs)')
    gravities, temperatures, stars = [float(g) for g in gravities], [float(t) for t in temperatures], \
        [float(s) for s in stars]
    if len(set(gravities)) != len(gravities) or len(set(temperatures)) != len(temperatures):
        raise ValueError('a grid repeats a value')
    optics = so.SteamOptics(cache=cache)
    states = set()
    for t_s in temperatures:
        for g in gravities:
            col = steam.column(Waterworld.from_gravity(g), t_s, levels)
            states.update(zip(col['layer_p_pa'].tolist(), col['layer_t_k'].tolist()))
    fill = [(band, p, t) for band in bands for p, t in sorted(states) if not optics.path(band, p, t).is_file()]
    start = time.time()
    if fill:
        so._WORKER['optics'] = optics
        if processes > 1:
            with mp.get_context('fork').Pool(processes) as pool:
                for _ in pool.imap_unordered(_fill, fill):
                    pass
        else:
            for job in fill:
                _fill(job)
        report(f'filled {len(fill)} cross-sections in {time.time() - start:.0f} s', flush=True)
    _COLUMN_OPTICS[str(cache)] = optics
    jobs = [(g, t, tuple(stars), levels, bands, cache, optical_gravity) for t in temperatures for g in gravities]
    shape = (len(gravities), len(temperatures))
    out = {name: np.full(((len(stars),) if name.endswith(('_sw', 'sw_factor', 'sw_top_share')) else ()) + shape,
                         np.nan) for name in ARRAYS}
    gi, ti = {g: i for i, g in enumerate(gravities)}, {t: j for j, t in enumerate(temperatures)}
    failed = []

    def record(job, result=None, error=None):
        g, t_s = job[0], job[1]
        i, j = gi[g], ti[t_s]
        if error is not None:
            failed.append(dict(g=g, t_s=t_s, error=f'{type(error).__name__}: {error}'))
        else:
            for name in ('olr', 'z_lw', 'lw_factor', 'lw_top_share'):
                out[name][i, j] = result[name]
            for k, t_star in enumerate(stars):
                out['z_sw'][k, i, j] = result['sw'][t_star]['z']
                out['sw_factor'][k, i, j] = result['sw'][t_star]['factor']
                out['sw_top_share'][k, i, j] = result['sw'][t_star]['top_share']
        done = len(failed) + int(np.count_nonzero(~np.isnan(out['olr'])))
        report(f'{done}/{len(jobs)} g={g} T={t_s} {"failed: " + failed[-1]["error"] if error else "ok"} '
               f'{time.time() - start:.0f} s', flush=True)

    columns_start = time.time()
    if processes > 1:
        with ProcessPoolExecutor(processes, mp_context=mp.get_context('fork')) as pool:
            futures = {pool.submit(_column, job): job for job in jobs}
            for future in as_completed(futures):
                try:
                    record(futures[future], future.result())
                except Exception as error:          # a broken pool fails every column still pending
                    record(futures[future], error=error)
    else:
        for job in jobs:
            try:
                record(job, _column(job))
            except Exception as error:
                record(job, error=error)
    inputs = {f['name']: f['sha256'] for f in fetch_inputs.manifest()['files']
              if f['name'].startswith(('hitran_h2o', 'hitran_q', 'mt_ckd'))}
    return dict(schema=SCHEMA, gravities=gravities, temperatures=temperatures, stars=stars,
                levels=dict(top_pa=levels.top_pa, per_decade=levels.per_decade, sliver=levels.sliver),
                optical_gravity=optical_gravity, n_angles=N_ANGLES,
                bands=[dict(start=b.start, stop=b.stop, step=b.step, coarse_factor=b.coarse_factor) for b in bands],
                optics=dict(key=optics.key, floor=1e-30, continuum='MT_CKD 4.3 self', broad_pa=so.BROAD_PA,
                            cutoff=so.CUTOFF, version=so.VERSION, lines='HITRAN2020 as served 2026-09-24',
                            inputs=inputs),
                producer=producer(), evidence=EVIDENCE, failed=failed,
                seconds=round(time.time() - columns_start, 1),
                made=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                **{k: v.tolist() for k, v in out.items()})


INPUT_FIELDS = ('schema', 'gravities', 'temperatures', 'stars', 'levels', 'optical_gravity', 'n_angles', 'bands',
                'optics', 'producer')


def key(table: dict) -> str:
    """The sha256 of the table's inputs and producer, canonical JSON of its INPUT_FIELDS."""
    return hashlib.sha256(json.dumps({k: table[k] for k in INPUT_FIELDS}, sort_keys=True).encode()).hexdigest()


def write(path: Path, table: dict) -> str:
    """Writes the table atomically and returns the file's sha256."""
    data = (json.dumps(table, indent=1) + '\n').encode()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    part = path.with_suffix(path.suffix + f'.part{os.getpid()}')
    part.write_bytes(data)
    part.replace(path)
    return hashlib.sha256(data).hexdigest()


def read(path: Path) -> dict:
    table = json.loads(Path(path).read_text())
    if table.get('schema') != SCHEMA:
        raise ValueError(f'{path}: schema {table.get("schema")!r}, where the reader takes {SCHEMA}')
    for name in ARRAYS:
        table[name] = np.asarray(table[name], dtype=float)
    return table


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--store', type=Path, help="the lab's store, which places the table and the cache")
    parser.add_argument('--out', type=Path, help='the table file, in place of the store')
    parser.add_argument('--cache', type=Path, help="the optics' cache folder, in place of the store's")
    parser.add_argument('--optical-gravity', default='surface', choices=steam.OPTICAL_GRAVITIES)
    parser.add_argument('--gravities', default='1.1:2.6:0.1')
    parser.add_argument('--temperatures', default='220:600:5')
    parser.add_argument('--stars', default='5772,3400')
    parser.add_argument('--processes', type=int, default=1)
    args = parser.parse_args(argv)
    if args.store is None and (args.out is None or args.cache is None):
        parser.error('give --store, or --out and --cache')
    cache = args.cache or args.store / 'caches' / 'steam-optics'
    table = compute(span(args.gravities), span(args.temperatures), [float(v) for v in args.stars.split(',')],
                    cache=cache, optical_gravity=args.optical_gravity, processes=args.processes)
    out = args.out or args.store / 'products' / 'steam-table' / key(table)[:16] / 'table.json'
    print(out, write(out, table), f'{len(table["failed"])} failed', flush=True)
    return 1 if table['failed'] else 0


if __name__ == '__main__':
    sys.exit(main())
