"""The forcing of a column (patch 21 of models/exoplasim/patches) and the column of PlaSim's physics that it forces
(python/climate/gcm/plasim_column.py), on runs the lab's adapter writes and builds the lab compiles.

Patch 21 at its defaults leaves the run of the build before it byte for byte; switched on, it leaves the restart byte
for byte and adds its records to the output, and its dynamics' tendencies are the storage of the state the physics
sees less the physics' tendencies over each window, as the dump of every step gives them. The column, compiled from
the same series, gives the GCM's physics bit for bit, step after step, on rows from pole to pole, from the GCM's own
restart and states, on Earth's control under Kuo's scheme and on the Open Moon with every switch of the series on.

The runs take two processes each and test the code's path; none of them is a climate."""
import json
import re
import shutil
import struct
import subprocess

import numpy as np
import pytest

from climate.gcm import plasim_column as pc
from worldlab import builds, derive, exoplasim as ex
from worldlab.roots import root
from worldlab.spec import LAB, Library

LIB = Library()
DEFAULTS = LIB.defaults('exoplasim/defaults')
EARTH, CONTROL = LIB.world('earth'), LIB.scenario('earth/control')
STORE, ENV = root('store'), root('env')
RANKS = 2                                   # the machine budget for these runs
SERIES_SOURCES = LAB.parent / 'models' / 'exoplasim' / 'expected-series.sha256'
needs_build = pytest.mark.skipif(STORE is None or ENV is None or not ex.ARCHIVE.exists() or shutil.which('mpif90') is None
                                 or shutil.which('objcopy') is None,
                                 reason="a build needs the lab's store and environment, the pinned archive, MPI and objcopy")


def _run(**switches) -> dict:
    run = {**DEFAULTS, 'ranks': RANKS}
    return {**run, 'switches': {**run['switches'], **switches}}


def _plasim(folder, executable, steps: int, restart=None) -> None:
    """PlaSim run for `steps` steps in a folder the adapter wrote, from `restart` where one is given; refused where
    PlaSim aborts, which mpirun reports with its own exit code of 0 (mpimod.f90:385)."""
    text = (folder / 'plasim_namelist').read_text()
    for name, value in (('N_RUN_YEARS', 0), ('N_RUN_MONTHS', 0), ('N_RUN_DAYS', 0), ('N_RUN_STEPS', steps)):
        text, count = re.subn(rf'^ {name} = .*$', f' {name} = {value}', text, flags=re.M)
        assert count == 1, name
    (folder / 'plasim_namelist').write_text(text)
    if restart is not None:
        shutil.copy2(restart, folder / 'plasim_restart')
    done = subprocess.run(['nice', '-n', '10', 'mpirun', '-np', str(RANKS), str(executable)], cwd=folder,
                          capture_output=True, text=True, timeout=1800)
    assert done.returncode == 0 and 'MPI_ABORT' not in done.stdout + done.stderr, done.stderr[-2000:]
    assert not (folder / 'Abort_Message').exists() and (folder / 'plasim_status').is_file()


def _executable(run):
    return builds.build(run, store=STORE, env=ENV) / 'exoplasim' / 'plasim' / 'run' / builds.executable_name(run)


def _records(path) -> list:
    """PlaSim's raw output as (header, field) pairs after its two opening records."""
    raw = pc.records(path)
    return list(zip(raw[2::2], raw[3::2]))


def _sha256(path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _column(levels: int):
    patches = [builds.PATCHES / name for name in ex.series(DEFAULTS)]
    return pc.build(patches, levels, archive=ex.ARCHIVE, configured=builds.package(ENV),
                    folder=STORE / 'builds') / pc.EXECUTABLE


# Patch 21 in the GCM.

@needs_build
def test_patch_21_at_its_default_runs_byte_for_byte_and_on_adds_its_records_alone(tmp_path):
    """Earth's control over two days on two processes. The folder the adapter writes for the build of patches 01-20,
    whose plasim_namelist names neither entry, gives the same output and restart under the build of the whole series,
    and so does the folder that states NCOLFORCE and NCOLDUMP 0. With NCOLFORCE 1 the restart stays byte for byte and
    the output holds every record of the run without it, in order, with codes 241-250 after the last record of each
    output, at its time; with NCOLDUMP 3 the restart stays byte for byte and plasim_column holds the run's first three
    steps."""
    patches = list(ex.series(DEFAULTS))
    assert patches[-1] == ex.PATCH_21 and len(patches) == 21
    twenty = {**_run(), 'patches': patches[:20]}
    whole = _run()
    executables = {20: _executable(twenty), 21: _executable(whole)}
    # The whole series' build compiled the sources that models/check_patches.sh pins.
    pinned = {name: digest for digest, name in (line.split() for line in SERIES_SOURCES.read_text().splitlines())}
    record = json.loads((builds.build(whole, store=STORE, env=ENV) / 'build.json').read_text())
    assert record['sources'] == pinned and 'plasim/src/plasim.f90' in pinned
    written = {'twenty': twenty, 'quiet': whole, 'forcing': _run(column_forcing=True),
               'dump': _run(column_dump_steps=3)}
    for name, run in written.items():
        record = ex.write_run(tmp_path / name, EARTH, CONTROL, run, calibrations=ex.Calibrations.identity(),
                              store=STORE)
        assert record['switches']['column_forcing'] is (name == 'forcing')
    lines = lambda name: [line for line in (tmp_path / name / 'plasim_namelist').read_text().splitlines()
                          if line.split()[0] in ('NCOLFORCE', 'NCOLDUMP')]
    assert [lines(name) for name in written] == [[], [' NCOLFORCE = 0', ' NCOLDUMP = 0'],
                                                 [' NCOLFORCE = 1', ' NCOLDUMP = 0'],
                                                 [' NCOLFORCE = 0', ' NCOLDUMP = 3']]
    out = {}
    for name, build in (('twenty', 20), ('twenty', 21), ('quiet', 21), ('forcing', 21), ('dump', 21)):
        folder = tmp_path / f'{name}-{build}'
        shutil.copytree(tmp_path / name, folder)
        _plasim(folder, executables[build], 96)
        out[name, build] = {p: _sha256(folder / p) for p in ('plasim_output', 'plasim_status')}
        out[name, build]['records'] = _records(folder / 'plasim_output')
        out[name, build]['dump'] = (folder / 'plasim_column').exists()
        if name == 'dump':
            out[name, build]['steps'] = [s['nstep'] for s in pc.read_dump(folder / 'plasim_column')]
        shutil.rmtree(folder)
    base = out['twenty', 20]
    assert out['twenty', 21]['plasim_output'] == base['plasim_output'] == out['quiet', 21]['plasim_output']
    assert out['twenty', 21]['plasim_status'] == base['plasim_status'] == out['quiet', 21]['plasim_status']
    for name in ('forcing', 'dump'):
        assert out[name, 21]['plasim_status'] == base['plasim_status'], name
    assert out['dump', 21]['plasim_output'] == base['plasim_output'] and not out['forcing', 21]['dump']
    first = out['dump', 21]['steps'][0]
    assert out['dump', 21]['steps'] == [first, first + 1, first + 2]
    plain, forced = base['records'], out['forcing', 21]['records']
    header = lambda r: struct.unpack('<8i', r[0])
    assert [r for r in forced if header(r)[0] not in range(241, 251)] == plain
    codes = [header(r)[0] for r in forced]
    nlev = derive.level_count(DEFAULTS)
    block = [c for c in range(241, 245) for _ in range(nlev)] + [245] + \
        [c for c in range(246, 250) for _ in range(nlev)] + [250]
    ends = [i for i, c in enumerate(codes) if c == 241 and (i == 0 or codes[i - 1] != 241)]
    assert len(ends) == codes.count(250) == 2                      # two outputs, one a day
    for i in ends:
        assert codes[i:i + len(block)] == block
        assert len({header(forced[j])[2:4] + header(forced[j])[6:7] for j in range(i - 1, i + len(block))}) == 1
        fields = np.array([np.frombuffer(forced[j][1], '<f4') for j in range(i, i + len(block))])
        assert np.isfinite(fields).all()


@needs_build
def test_the_forcing_is_the_storage_of_the_state_the_physics_sees_less_the_physics(tmp_path):
    """Earth's control over two days with outputs every 12 steps and every step's physics written to plasim_column:
    at each output the state written (codes 246-250) is the dump's at that step in single precision, and the dynamics'
    tendencies written (codes 241-245) are the dump's storage over the window, from the step of the output before (the
    run's first step for the first) to this one, less the mean of the physics' tendencies over the window's steps. The
    vapour's tendency is gqdt's, the humidity fixer's part with dqdt, brought back from the spectral step's units by
    PlaSim's own scale ww, 2 pi over the sidereal day its readnl sets, which the dump's columns untouched by the fixer
    give."""
    run = {**_run(column_forcing=True, column_dump_steps=96), 'mean_interval_days': 0.25}
    ex.write_run(tmp_path / 'run', EARTH, CONTROL, run, calibrations=ex.Calibrations.identity(), store=STORE)
    assert ' NSTPW = 12' in (tmp_path / 'run' / 'plasim_namelist').read_text()
    _plasim(tmp_path / 'run', _executable(run), 96)
    dump = pc.read_dump(tmp_path / 'run' / 'plasim_column')
    codes = pc.read_output(tmp_path / 'run' / 'plasim_output', list(range(241, 251)))
    lev, step_s = dump[0]['levels'], derive.calendar(EARTH, run)['step_s']
    first = dump[0]['nstep']
    assert len(dump) == 96 and list(codes[241]['steps']) == [11, 23, 35, 47, 59, 71, 83, 95]
    state = lambda s: dict(t=s['inputs']['t'][:lev], q=s['inputs']['q'][:lev], u=s['inputs']['u'],
                           v=s['inputs']['v'], lnps=np.log(s['inputs']['ps']))
    # PlaSim's scale ww from the columns the fixer left alone, where gqdt = dqdt dp / (ww psurf)
    o, i = dump[5]['outputs'], dump[5]['inputs']
    alone = np.all(o['q'][:lev] == i['q'][:lev], axis=0)[None, :] & (np.abs(o['dqdt']) > 1e-9)
    ww = np.median((o['dqdt'] * i['ps'] / (o['gqdt'] * i['psurf']))[alone])
    # readnl's sidereal day, the 24-hour day times 364/365 for 365 days a year (plasim.f90, readnl)
    assert alone.sum() > 20 and ww == pytest.approx(2 * np.pi / (86400.0 * 364 / 365), rel=1e-9)
    physics = lambda s: dict(t=s['outputs']['dtdt'], u=s['outputs']['dudt'], v=s['outputs']['dvdt'],
                             q=s['outputs']['gqdt'] * ww * s['inputs']['psurf'] / s['inputs']['ps'], lnps=0.0)
    begin = 0
    for k, end in enumerate(codes[241]['steps']):
        assert dump[end]['nstep'] == first + end
        written = {name: codes[c]['field'][k] for name, c in pc.STATE_CODES.items()}
        x = state(dump[end])
        for name in ('t', 'q', 'u', 'v'):
            assert np.array_equal(written[name], x[name].astype(np.float32).astype(float)), name
        assert np.array_equal(written['ps'], dump[end]['inputs']['ps'].astype(np.float32).astype(float))
        x0, n = state(dump[begin]), end - begin
        mean = {name: sum(physics(dump[j])[name] for j in range(begin, end)) / n for name in x}
        for name, c in pc.FORCING_CODES.items():
            expected = (x[name] - x0[name]) / (n * step_s) - mean[name]
            found = codes[c]['field'][k]
            scale = np.abs(expected).max() + np.abs(mean[name]).max()
            assert np.abs(found - expected).max() <= 2e-6 * scale + 1e-30, (k, name)
        begin = end


# The column against the GCM, step for step.

def _step_by_step(gcm, restart, executable, rows, steps, tmp_path) -> dict:
    """The column at each row, each step's state the GCM's, set beside the GCM's dump: for each row, the fields that
    differ in any bit."""
    dump = pc.read_dump(gcm / 'plasim_column')
    nlon = int(round(np.sqrt(2 * dump[0]['points'])))
    found = {}
    for row in rows:
        given = [pc.start(gcm, row, k) for k in range(steps)]
        work = pc.prepare(tmp_path / f'column-{row}', gcm, restart, row=row, steps=steps, start=given[0], given=given)
        pc.run(work, executable)
        col = pc.read_dump(work / 'column_output')
        assert [s['nstep'] for s in col] == [s['nstep'] for s in dump[:steps]] and col[0]['row'] == row
        bad = []
        for k in range(steps):
            for part in ('inputs', 'outputs'):
                for name, a in col[k][part].items():
                    g = dump[k][part][name]
                    if not np.array_equal(a, g if name == 'psurf' else pc.row_of(g, row, nlon)):
                        bad.append((k, part, name))
        found[row] = bad
        shutil.rmtree(work)
    return found


@needs_build
def test_the_column_gives_the_gcms_physics_bit_for_bit_on_earths_control(tmp_path):
    """Earth's control under Kuo's scheme on ten levels: a day from a cold start, then three steps from its restart
    with each step's physics written out. The column, compiled from the same series under ExoPlaSim's flags and started
    from the same restart, given each step's state and the dynamics' vapour tendency Kuo's scheme read, gives every
    field of the GCM's physics bit for bit at every grid point of rows from the north pole to the south: the
    tendencies of temperature, vapour and the winds, the humidity after the fixer, the surface's temperature and
    humidity as the land, sea and ice modules carry them from step to step, the rain, snow, evaporation and heat
    fluxes, the radiation at the ground and the cloud."""
    run = _run(column_dump_steps=3)
    executable = _executable(run)
    for name, steps, restart in (('spin', 48, None), ('steps', 3, tmp_path / 'spin' / 'plasim_status')):
        ex.write_run(tmp_path / name, EARTH, CONTROL, run, calibrations=ex.Calibrations.identity(), store=STORE)
        _plasim(tmp_path / name, executable, steps, restart)
    found = _step_by_step(tmp_path / 'steps', tmp_path / 'spin' / 'plasim_status', _column(10), (1, 9, 16, 17, 32), 3,
                          tmp_path)
    assert found == {row: [] for row in (1, 9, 16, 17, 32)}


@needs_build
def test_the_column_differs_where_its_input_differs(tmp_path):
    """The comparison above sees a change: with the dynamics' vapour tendency Kuo's scheme reads set to 0, the column's
    physics leaves the GCM's at a row of the tropics in its tendencies, rain and cloud."""
    run = _run(column_dump_steps=1)
    executable = _executable(run)
    for name, steps, restart in (('spin', 48, None), ('steps', 1, tmp_path / 'spin' / 'plasim_status')):
        ex.write_run(tmp_path / name, EARTH, CONTROL, run, calibrations=ex.Calibrations.identity(), store=STORE)
        _plasim(tmp_path / name, executable, steps, restart)
    gcm = tmp_path / 'steps'
    given = [dict(pc.start(gcm, 16, 0))]
    given[0]['dqt'] = np.zeros_like(given[0]['dqt'])
    work = pc.prepare(tmp_path / 'column', gcm, tmp_path / 'spin' / 'plasim_status', row=16, steps=1, start=given[0],
                      given=given)
    pc.run(work, _column(10))
    col, dump = pc.read_dump(work / 'column_output')[0], pc.read_dump(gcm / 'plasim_column')[0]
    differ = {name for name, a in col['outputs'].items() if not np.array_equal(a, pc.row_of(dump['outputs'][name], 16, 64))}
    assert {'dtdt', 'dqdt', 'dqt', 'convective_rain'} <= differ


@needs_build
def test_with_windows_of_one_step_the_column_retraces_the_gcms_states(tmp_path):
    """Earth's control under the simplified Betts-Miller scheme, a day from a cold start, then twelve steps from its
    restart with an output, and so a window of the forcing, at every step. Started from the GCM's state at the first
    step and stepped forward under the windows, the column retraces the GCM's states at every grid point of a row of
    the tropics within the rounding of the forcing's single precision: its temperature within 1e-5 K and its vapour
    within 1e-8 kg/kg at each of the steps, and its rain as the GCM's dump gives it. On PlaSim's leapfrog the same
    column leaves the GCM's states within the first windows."""
    run = {**_run(convection='betts_miller', column_forcing=True, column_dump_steps=12), 'mean_interval_days': 1 / 48}
    executable = _executable(run)
    for name, steps, restart in (('spin', 48, None), ('steps', 12, tmp_path / 'spin' / 'plasim_status')):
        ex.write_run(tmp_path / name, EARTH, CONTROL, run, calibrations=ex.Calibrations.identity(), store=STORE)
        _plasim(tmp_path / name, executable, steps, restart)
    assert ' NSTPW = 1' in (tmp_path / 'steps' / 'plasim_namelist').read_text()
    gcm, row = tmp_path / 'steps', 16
    windows = pc.windows(gcm, row)
    assert list(windows['steps']) == [0] + [1] * 11
    dump = pc.read_dump(gcm / 'plasim_column')
    found = {}
    for scheme in ('forward', 'leapfrog'):
        work = pc.prepare(tmp_path / scheme, gcm, tmp_path / 'spin' / 'plasim_status', row=row, steps=11,
                          start=pc.start(gcm, row), windows=windows, scheme=scheme)
        pc.run(work, _column(10))
        col = pc.read_dump(work / 'column_output')
        lev = col[0]['levels']
        found[scheme] = [(np.abs(c['inputs']['t'][:lev] - pc.row_of(g['inputs']['t'][:lev], row, 64)).max(),
                          np.abs(c['inputs']['q'][:lev] - pc.row_of(g['inputs']['q'][:lev], row, 64)).max(),
                          np.abs(c['outputs']['convective_rain'] - pc.row_of(g['outputs']['convective_rain'], row, 64)).max())
                         for c, g in zip(col, dump)]
    assert all(dt < 1e-5 and dq < 1e-8 and dr < 1e-12 for dt, dq, dr in found['forward'])
    assert max(dt for dt, _, _ in found['leapfrog']) > 0.1


def _stored(label) -> bool:
    from worldlab import data
    try:
        return data.locate(label, LIB, store=STORE) is not None
    except Exception:
        return False


@needs_build
def test_the_column_gives_the_gcms_physics_bit_for_bit_on_the_open_moon_with_every_switch_on(tmp_path):
    """The Open Moon on ten levels over its own surface with every switch of the series on: the curved air's twilight
    with its clear share and single count, the gas bands, the longwave correction, the ice optics with the spectrum's
    weights (Terluna's calibrations of its corrected design run, read in place), Beljaars's gust with the similarity
    over water, the rain from its drops (Terluna's births for the Open Moon), the simplified Betts-Miller scheme with
    its depth test and cap and the wind at 10 m. Two days from a cold start, then three steps from the restart; the
    column gives every field of the GCM's physics bit for bit at rows from pole to pole, the Near-side Sea's among
    them."""
    import importlib.util
    from worldlab import geography
    # Terluna's calibrations and the rain's drops as the writer's tests state them
    spec = importlib.util.spec_from_file_location('lab_writer_tests', LAB / 'tests' / 'test_exoplasim_files.py')
    files = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(files)
    moon, open_moon = LIB.world('moon'), LIB.scenario('moon/open-moon')
    if files.TERLUNA is None:
        pytest.skip("Terluna's repository is unset (lab/local.example.toml)")
    try:
        heights = geography.heights(moon, LIB, store=STORE)
        surface = geography.model_surface(geography.water(moon, open_moon, heights, LIB, store=STORE), heights, 32)
    except Exception as error:                       # the store lacks the Moon's heights or first runoff
        pytest.skip(f"the store lacks the Open Moon's surface: {error}")
    run = dict(LIB.study('open-moon').gcm['design'].settings, ranks=RANKS)
    run['switches'] = {**run['switches'], 'convection': 'betts_miller', 'surface_gust': 'beljaars_similarity',
                       'rain_evaporation': 'drop_sizes', 'longwave_correction': True, 'ice_optics': True,
                       'twilight_clear_share': True, 'column_dump_steps': 3}
    calibrations = files.terluna_calibrations()
    calibrations = ex.Calibrations(**{**calibrations.__dict__, 'rain_drops': files._rain()})
    executable = _executable(run)
    for name, steps, restart in (('spin', 96, None), ('steps', 3, tmp_path / 'spin' / 'plasim_status')):
        record = ex.write_run(tmp_path / name, moon, open_moon, run, calibrations=calibrations, surface=surface,
                              store=STORE)
        _plasim(tmp_path / name, executable, steps, restart)
    assert {k for k, v in record['switches'].items() if v is True} >= {
        'twilight_clear_share', 'twilight_counted_once', 'gas_bands', 'longwave_correction', 'ice_optics', 'wind_10m'}
    assert (record['switches']['twilight'], record['switches']['convection'], record['switches']['surface_gust'],
            record['switches']['rain_evaporation']) == ('full', 'betts_miller', 'beljaars_similarity', 'drop_sizes')
    sea = pc.site_point(tmp_path / 'steps', dict(lat_deg=-5.0, lon_deg=-45.0, half_lat_deg=5.6, half_lon_deg=8.5,
                                                 surface='sea'), derive.gravity(moon))
    rows = (1, sea[0], 24, 32)
    found = _step_by_step(tmp_path / 'steps', tmp_path / 'spin' / 'plasim_status', _column(10), rows, 3, tmp_path)
    assert found == {row: [] for row in rows}
