"""Stage 9's check of HITEMP2010's lines on the radiative-convective column's own checked columns.

In the column's validation record (radiative_convective/validation.json, "pyrads"), PyRADS and the column computed
the outgoing longwave of saturated columns of water and nitrogen: 1 bar of nitrogen under a 200 K stratosphere, at
surface temperatures of 250 to 360 K, at 9.8 m/s^2 and at the Moon's gravity, held constant with height, with
water's lines and continuum alone and a diffusivity of 5/3. This check builds columns to that description with the
column's own moist adiabat (thermodynamics.build_column) and computes their outgoing longwave on the column's thermal
grid and water lines (optics.LONGWAVE: 1 to 3,000 cm^-1 at 0.01 cm^-1, HITRAN2020's lines above 1e-28 cm/molecule at
296 K), then again with HITEMP2010's lines as hitemp.py cuts them, each with MT_CKD 4.3's self and foreign continuum.
By stage 9's acceptance check the second lies within 3% of the first. Each row also gives the outgoing longwave the
validation records for the column on PyRADS's own 60-level profiles, and the first's difference from it, which
measures how far these columns lie from those. A layer's cross-sections depend on its pressure, temperature and
water alone, which the two gravities share, so each surface temperature's layers are computed once; the product is
written after each temperature.

    python -m atmosphere.waterworlds.column_check --store STORE [--processes N]

writes the check to STORE/products/hitemp-column-check/<key>/check.json, its key covering the line lists, the
columns, the grid and the producer.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import multiprocessing as mp
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy

from shared.constants import EARTH_RADIUS
from atmosphere.radiative_convective import fetch_inputs, longwave, optics as ro, spectroscopy as sp
from atmosphere.radiative_convective.thermodynamics import (MOON, ColumnSpec, DryAir, Planet, build_column,
                                                           column_from_levels, species_column, uniform_rh)
from atmosphere.waterworlds import figures as fg, hitemp

SCHEMA = 'world-crafting.waterworlds.hitemp-column-check/1'
TEMPERATURES = (250.0, 280.0, 300.0, 320.0, 340.0, 360.0)
PLANETS = (Planet('earth_9.8', EARTH_RADIUS, 9.8 * EARTH_RADIUS ** 2), MOON)
GRID = ro.LONGWAVE.grid                         # the column's own thermal grid, mesh and floor for water's lines
COARSE_FACTOR = ro.LONGWAVE.coarse_factor
HITRAN_FLOOR = ro.LONGWAVE.floor('H2O')
DIFFUSIVITY = 5 / 3
TOLERANCE = 0.03
AIR = DryAir(1e5, {'N2': 1.0})
VALIDATION = Path(__file__).resolve().parents[1] / 'radiative_convective' / 'validation.json'
RECORDED = {'earth_9.8': 'earth_gravity_9_8', 'moon': 'lunar_gravity'}   # the validation's rows for each planet
PRODUCER_FILES = ('atmosphere/waterworlds/column_check.py', 'atmosphere/waterworlds/hitemp.py',
                  'atmosphere/waterworlds/figures.py', 'atmosphere/radiative_convective/validation.json',
                  'atmosphere/radiative_convective/optics.py',
                  'atmosphere/radiative_convective/spectroscopy.py', 'atmosphere/radiative_convective/longwave.py',
                  'atmosphere/radiative_convective/thermodynamics.py', 'shared/constants.py', 'shared/constants.json')


def column(planet: Planet, t_s: float) -> dict:
    """A checked column: saturated water over 1 bar of nitrogen, a 200 K stratosphere, gravity constant with height."""
    col = build_column(ColumnSpec(planet, AIR, t_s, stratosphere_k=200.0, humidity=uniform_rh(1.0)))
    return column_from_levels(planet, AIR, col['p_pa'], col['t_k'], col['x_h2o'], constant_gravity=True)


_WORKER: dict = {}


def _layer(job) -> np.ndarray:
    """One layer's water cross-section (cm^2 per water molecule): its lines, self- and nitrogen-broadened, cut 25 cm^-1
    from centre less their value there, and the continuum, as the column's own layer optics take them."""
    p, t, x = job
    lines, sums, continuum, grid = (_WORKER[k] for k in ('lines', 'sums', 'continuum', 'grid'))
    sigma = sp.line_absorption(grid, lines, sums, t, p, x * p, pedestal=True, coarse_factor=COARSE_FACTOR)
    s_c, f_c = continuum.cross_sections(grid.nu, t, p, x)
    return sigma + s_c + f_c


def cross_sections(col: dict, lines: sp.LineList, *, grid: sp.Grid = GRID, processes: int = 1) -> np.ndarray:
    """The column's layers' water cross-sections, layers by wavenumbers."""
    _WORKER.update(lines=lines, sums=sp.PartitionSums(lines.gid), continuum=sp.WaterContinuum(), grid=grid)
    jobs = list(zip(col['layer_p_pa'].tolist(), col['layer_t_k'].tolist(), col['layer_x_h2o'].tolist()))
    if processes > 1:
        with mp.get_context('fork').Pool(min(processes, len(jobs))) as pool:
            rows = pool.map(_layer, jobs, chunksize=1)
    else:
        rows = [_layer(job) for job in jobs]
    return np.vstack(rows)


def olr(col: dict, sigma: np.ndarray, grid: sp.Grid = GRID) -> float:
    """The column's outgoing longwave (W/m^2) on its layers' cross-sections, one stream at the diffusivity."""
    tau = sigma * species_column(col, 'H2O')[:, None]
    up, _ = longwave.fluxes(grid.nu, tau, col['t_k'], float(col['t_k'][0]), diffusivity=DIFFUSIVITY)
    return float(longwave.integrate(grid.nu, up[-1]))


def recorded() -> dict:
    """The column's own outgoing longwave on PyRADS's profiles, by planet and surface temperature, as its validation
    records it with its default data (W/m^2)."""
    pyrads = json.loads(VALIDATION.read_text())['pyrads']
    return {planet: {float(r['ts']): r['this_default'] for r in pyrads[rows]} for planet, rows in RECORDED.items()}


def producer() -> dict:
    root = Path(__file__).resolve().parents[2]
    return dict(module='atmosphere.waterworlds.column_check',
                sources={n: hashlib.sha256((root / n).read_bytes()).hexdigest() for n in PRODUCER_FILES},
                environment=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__))


def check(sources: dict, *, temperatures=TEMPERATURES, planets=PLANETS, grid: sp.Grid = GRID, processes: int = 1,
          report=print, written=None) -> dict:
    """The outgoing longwave of every checked column on each line list in `sources`, a name for each list, the first
    the reference; each other list's difference from it, and whether every one lies within TOLERANCE. `written`, when
    given, takes the result so far after each temperature."""
    names = list(sources)
    rows, record = [], recorded()
    for t_s in temperatures:
        cols = {p.name: column(p, t_s) for p in planets}
        first = cols[planets[0].name]
        for c in cols.values():                   # constant gravity: the same levels at every gravity
            if not (np.array_equal(c['p_pa'], first['p_pa']) and np.array_equal(c['t_k'], first['t_k'])):
                raise ValueError('the gravities give the column different levels')
        values = {}
        for name in names:
            start = time.time()
            sigma = cross_sections(first, sources[name], grid=grid, processes=processes)
            values[name] = {p: olr(c, sigma, grid) for p, c in cols.items()}
            report(f'{t_s:.0f} K {name}: {len(first["layer_p_pa"])} layers in {time.time() - start:.0f} s, '
                   + ', '.join(f'{p} {v:.2f} W/m2' for p, v in values[name].items()), flush=True)
        for p in cols:
            row = dict(t_s=t_s, planet=p, layers=int(len(first['layer_p_pa'])),
                       olr_recorded_on_pyrads_profiles=record.get(p, {}).get(t_s),
                       **{f'olr_{name}': values[name][p] for name in names})
            for name in names[1:]:
                row[f'difference_{name}'] = values[name][p] / values[names[0]][p] - 1
            recorded_olr = row['olr_recorded_on_pyrads_profiles']
            row[f'{names[0]}_against_recorded'] = (values[names[0]][p] / recorded_olr - 1 if recorded_olr
                                                   else math.nan)
            rows.append(row)
        result = _summary(names, rows, complete=t_s == temperatures[-1])
        if written is not None:
            written(result)
    return result


def _summary(names, rows, complete: bool) -> dict:
    worst = {name: max(abs(r[f'difference_{name}']) for r in rows) for name in names[1:]}
    gaps = [abs(r[f'{names[0]}_against_recorded']) for r in rows if math.isfinite(r[f'{names[0]}_against_recorded'])]
    return dict(schema=SCHEMA, reference=names[0], tolerance=TOLERANCE, rows=list(rows), worst=worst,
                worst_against_recorded=max(gaps) if gaps else math.nan, complete=complete,
                passes=complete and all(w <= TOLERANCE for w in worst.values()))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--store', type=Path, required=True, help="the lab's store, which holds HITEMP's lines")
    parser.add_argument('--processes', type=int, default=1)
    args = parser.parse_args(argv)
    if fetch_inputs.restore()['status'] != 'PASS':
        raise SystemExit('the spectroscopic inputs are missing or changed (radiative_convective.fetch_inputs)')
    hitran = sp.load_lines('H2O', HITRAN_FLOOR)
    cut, path = hitemp.from_store(args.store)
    inputs = dict(hitran={f['name']: f['sha256'] for f in fetch_inputs.manifest()['files']
                          if f['name'].startswith(('hitran_h2o_0', 'hitran_q', 'mt_ckd'))},
                  hitran_floor_296k=HITRAN_FLOOR, hitemp_cut=path.stem, temperatures=list(TEMPERATURES),
                  planets=[dict(name=p.name, gravity=p.surface_gravity) for p in PLANETS],
                  grid=dict(start=GRID.start, step=GRID.step, size=GRID.size), coarse_factor=COARSE_FACTOR,
                  diffusivity=DIFFUSIVITY, producer=producer())
    k = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()
    out = args.store / 'products' / 'hitemp-column-check' / k[:16] / 'check.json'

    def written(result):
        result = dict(result, inputs=inputs,
                      made=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))
        print(out, fg.write(out, result), flush=True)
    result = check(dict(hitran=hitran, hitemp=cut), processes=args.processes, written=written)
    print('passes' if result['passes'] else 'fails', json.dumps(result['worst']),
          'against the recorded', result['worst_against_recorded'], flush=True)
    return 0 if result['passes'] else 1


if __name__ == '__main__':
    sys.exit(main())
