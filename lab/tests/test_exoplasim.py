"""ExoPlaSim's own configure and PlaSim's own calendar, run in the lab's environment, against worldlab.derive."""
import json
import os
import subprocess

import pytest

from worldlab import derive
from worldlab.roots import root
from worldlab.spec import LAB, Library

LIB = Library()
MOON, EARTH = LIB.world('moon'), LIB.world('earth')
EXOPLASIM = LIB.defaults('exoplasim/defaults')
REGIME = json.loads((LAB.parent / 'paper' / 'data' / 'regime_calc.json').read_text())
ENV = root('env')
PYTHON = ENV / 'bin' / 'python' if ENV is not None else None
needs_env = pytest.mark.skipif(PYTHON is None or not PYTHON.exists(),
                               reason="the lab's environment is unset (lab/local.example.toml)")

# Runs in the lab's environment, each case in a model folder of its own: configure leaves ROTSPD as an earlier call
# set it when a later call passes a rotation period of 1. ExoPlaSim's first Model compiles PlaSim for the resolution,
# levels and ranks where its executable is missing, and the pinned install keeps it. A case marked `run` runs PlaSim
# for one step, whose diagnostics print the solar day, days per year, time step and steps per day it computed.
PROBE = r'''
import importlib.metadata, json, os, re, subprocess, sys, tempfile
import exoplasim
if importlib.metadata.version('exoplasim') != '3.4.2':
    sys.exit(f"the lab's environment holds ExoPlaSim {importlib.metadata.version('exoplasim')}, where 3.4.2 is pinned")
spec = json.loads(sys.argv[1])
def entry(path, key):
    match = re.search(rf'^\s*{key}\s*=\s*([^\s,]+)', open(path).read(), re.M)
    return match.group(1) if match else None
out = []
for case in spec['cases']:
    with tempfile.TemporaryDirectory(prefix='worldlab-configure-') as folder:
        os.chdir(folder)
        model = exoplasim.Model(workdir='run', modelname='run', resolution=spec['resolution'], layers=spec['levels'],
                                ncpus=spec['ranks'], precision=spec['precision'])
        if not os.path.exists(os.path.join(os.path.dirname(exoplasim.__file__), 'plasim', 'run', model.executable)):
            sys.exit(f'ExoPlaSim compiled no {model.executable}; its compile needs gfortran and mpif90')
        model.configure(timestep=spec['timestep_min'], rotationperiod=case['rotationperiod'], year=case['year'])
        found = dict(N_DAYS_PER_YEAR=entry('run/plasim_namelist', 'N_DAYS_PER_YEAR'),
                     ROTSPD=entry('run/planet_namelist', 'ROTSPD'))
        if case['run']:
            for key, value in (('N_RUN_YEARS', '0'), ('N_RUN_MONTHS', '0'), ('N_RUN_DAYS', '0'), ('N_RUN_STEPS', '1')):
                model._edit_namelist('plasim_namelist', key, value)
            done = subprocess.run(['mpirun', '-np', str(spec['ranks']), './' + model.executable], cwd='run',
                                  capture_output=True, text=True, timeout=300)
            if done.returncode:
                sys.exit(f'PlaSim stopped with {done.returncode}: {done.stderr[-2000:]}')
            diag = open('run/plasim_diag').read()
            for name, label in (('solar_day_s', 'Solar    day'), ('days_per_year', 'Days / Year'),
                                ('timestep_min', 'Timestep '), ('steps_per_day', 'Timesteps / day')):
                match = re.search(r'\* ' + re.escape(label) + r'[^:]*:\s*([-0-9.]+)', diag)
                found[name] = match.group(1) if match else None
        out.append(found)
        os.chdir('/')
print('worldlab-probe ' + json.dumps(out))
'''


def _world(sidereal_days: float) -> dict:
    """The Moon spun at another sidereal period, its solar day derived."""
    return {**MOON, 'rotation': {**MOON['rotation'], 'sidereal_period_days': sidereal_days, 'solar_day_days': None}}


@needs_env
def test_configure_and_plasim_keep_the_calendar_that_derive_predicts():
    version = subprocess.run([PYTHON, '-c', 'import importlib.metadata as m; print(m.version("exoplasim"))'],
                             capture_output=True, text=True, timeout=120)
    assert version.returncode == 0, f"the lab's environment fails to import ExoPlaSim: {version.stderr[-2000:]}"
    slow = [float(label[:-1]) for label in REGIME['exoplasim_slow_rotators'] if label not in ('formula', '27.3217d')]
    assert len(slow) == 7
    long_year = {**EARTH, 'orbit': {**EARTH['orbit'], 'sidereal_year_days': 365.6}}   # int, where round would give 366
    worlds = [MOON, EARTH, long_year] + [_world(p) for p in slow + [12.0, 12.0001, 20.0, 20.0001]]
    runs = {0, 1, 3 + slow.index(243.0), len(worlds) - 4, len(worlds) - 3}               # PlaSim runs these five
    calendars = [derive.calendar(w, EXOPLASIM) for w in worlds]
    cases = [dict(rotationperiod=c['rotationperiod'], year=w['orbit']['sidereal_year_days'], run=i in runs)
             for i, (w, c) in enumerate(zip(worlds, calendars))]
    spec = {k: EXOPLASIM[k] for k in ('resolution', 'levels', 'ranks', 'precision', 'timestep_min')}
    done = subprocess.run([PYTHON, '-c', PROBE, json.dumps(dict(spec, cases=cases))], capture_output=True, text=True,
                          timeout=900)
    assert done.returncode == 0, done.stderr[-3000:]
    line = next(l for l in reversed(done.stdout.splitlines()) if l.startswith('worldlab-probe '))
    written = json.loads(line.removeprefix('worldlab-probe '))
    for i, (world, cal, found) in enumerate(zip(worlds, calendars, written, strict=True)):
        where = (world['rotation']['sidereal_period_days'], world['orbit']['sidereal_year_days'])
        assert int(found['N_DAYS_PER_YEAR']) == cal['n_days_per_year'], where
        rotspd = 1.0 if found['ROTSPD'] is None else float(found['ROTSPD'])          # absent: PlaSim's own 1
        assert rotspd == 1.0 / cal['rotationperiod'], where
        if i in runs:
            assert float(found['solar_day_s']) == pytest.approx(cal["model_day_s"], abs=0.0501), where  # to 0.1 s
            assert int(found['days_per_year']) == cal['n_days_per_year'], where
            assert float(found['timestep_min']) == pytest.approx(cal['step_s'] / 60.0, abs=5e-4), where
            assert int(found['steps_per_day']) == cal['steps_per_model_day'], where
    assert [c['n_days_per_year'] for c in calendars[1:3]] == [365, 365]
    assert [c['n_days_per_year'] for c in calendars[-4:]] == [36, 24, 24, 12]


@needs_env
@pytest.mark.skipif(root('terluna-drive') is None, reason="Terluna's research drive is unset (lab/local.example.toml)")
def test_the_guard_record_holds_the_hottest_runs_largest_wind():
    record = json.loads((LAB / 'validation' / 'timestep_guard.json').read_text())
    hottest = max(record['runs'], key=lambda run: record['runs'][run]['m_s'])
    best = record['runs'][hottest]
    path = root('terluna-drive') / 'gcm-runs' / hottest / 'model' / f"MOST.{best['model_year']:05d}.nc"
    read = ('import json, sys; from worldlab.winds import largest_wind_m_s; '
            'print(json.dumps(largest_wind_m_s(sys.argv[1])))')
    done = subprocess.run([PYTHON, '-c', read, str(path)], capture_output=True, text=True, timeout=120,
                          env={**os.environ, 'PYTHONPATH': str(LAB)})
    assert done.returncode == 0, done.stderr[-2000:]
    speed, latitudes = json.loads(done.stdout)
    assert speed == pytest.approx(best['m_s'], rel=1e-12) and latitudes == best['latitudes']


READER_PROBE = r'''
import json, sys
from pathlib import Path
import netCDF4, numpy as np
from worldlab.winds import largest_wind_m_s
folder = Path(sys.argv[1])
def write(name, u):
    with netCDF4.Dataset(folder / name, 'w') as output:
        for dim, size in (('time', 2), ('lev', 2), ('lat', 32), ('lon', 4)):
            output.createDimension(dim, size)
        for name_, values in (('ua', u), ('va', np.zeros(u.shape, dtype='f4'))):
            output.createVariable(name_, 'f4', ('time', 'lev', 'lat', 'lon'), fill_value=9.96921e36)[:] = values
u = np.full((2, 2, 32, 4), 3.0, dtype='f4')
u[0, 0, 0, 0] = 4.0
masked = np.ma.masked_array(u.copy(), mask=np.zeros(u.shape, dtype=bool))
masked[1, 1, 1, 1] = np.ma.masked                                  # written as the fill value, 9.97e36
write('masked.nc', masked)
unstable = u.copy()
unstable[1, 0, 0, 0] = np.nan
write('unstable.nc', unstable)
out = dict(masked=largest_wind_m_s(folder / 'masked.nc'))
try:
    largest_wind_m_s(folder / 'unstable.nc')
except ValueError as error:
    out['unstable'] = str(error)
print(json.dumps(out))
'''


@needs_env
def test_the_wind_reader_leaves_out_fill_values_and_refuses_non_finite_winds(tmp_path):
    done = subprocess.run([PYTHON, '-c', READER_PROBE, str(tmp_path)], capture_output=True, text=True, timeout=120,
                          env={**os.environ, 'PYTHONPATH': str(LAB)})
    assert done.returncode == 0, done.stderr[-2000:]
    out = json.loads(done.stdout)
    assert out['masked'] == [4.0, 32] and 'non-finite' in out.get('unstable', '')
