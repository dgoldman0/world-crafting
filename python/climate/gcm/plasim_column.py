"""A column of PlaSim's physics, compiled from the lab's patched ExoPlaSim and forced by the GCM's own dynamics.

    from climate.gcm import plasim_column as pc
    build = pc.build(patches, levels=15, archive=archive, configured=package, folder=store / 'builds')
    row, col = pc.site_point(gcm_folder, site, gravity_m_s2)              # the GCM's grid point at a site
    pc.prepare(work, gcm_folder, restart, row=row, steps=n, start=pc.start(gcm_folder, row),
               windows=pc.windows(gcm_folder, row), points=[col])        # forced by the GCM's windows
    pc.run(work, build / pc.EXECUTABLE)
    steps = pc.read_dump(work / 'column_output')                          # what the physics saw and made, by step

What it is. PlaSim's own Fortran, compiled from the pinned archive with the run's patch series, its makefile and the
compile flags ExoPlaSim's configure wrote for the machine, for one latitude a process (NPRO_ATM equal to NLAT_ATM):
NHOR is then one row of the GCM's grid, and the column is the process that holds the row a site stands in. Its
message-passing layer, plasim_column_mpi.f90, takes the place of PlaSim's single-process stub through the makefile's
MPIMOD, so that the process reads the GCM run's own namelists, surface files and restart and keeps the row's share
of each global field: the Gaussian latitude, the land, the orography, the slab sea's and the soil's state and every
other field a physics routine reads come from the GCM's files at the row's grid points, and each grid point keeps its
own longitude in the Sun's hour angle. PlaSim's plasim_main and prolog start the column. Four of PlaSim's routines are
weakened in their objects with objcopy so that the driver's take their place (REPLACED): master, the time loop;
mkdqtgp, which brings the dynamics' vapour tendency from spectral space for Kuo's scheme; makeareas, whose
single-process form reads latitudes a process of one row lacks; and oroini, which gathers the whole grid to route the
rivers. Everything else is PlaSim's code as the GCM compiles it.

The step. The column's master steps every grid point of the row through the physics in gridpointd's order: miscstep
(the humidity fixer), fluxstep, radstep, rainstep, surfstep, carbonstep and hurricanestep. The state the physics sees
comes from the GCM in one of two modes. In mode 1 the column starts from the GCM's state at its first step and steps
on under the dynamics' tendencies of each window of the GCM's forcing (patch 21, codes 241-245), which the GCM writes
as the storage of the state its physics sees less its physics' tendencies. With the scheme 'forward', the default,
that state steps forward by the step times the window's tendencies and the column's own physics' tendencies, so that
over each window the column's storage equals the GCM's wherever its physics equals the GCM's; with windows of one step
the column retraces the GCM's states. With 'leapfrog' it steps on PlaSim's leapfrog and Robert-Asselin filter, the
window's tendencies in place of the adiabatic step, a scheme that leaves the GCM's states within a step of windows
that short. Kuo's scheme reads the forcing's vapour tendency in the form mkdqtgp gives it. In mode 2 each step's state
is the GCM's own at that step, from the physics' inputs patch 21 writes to plasim_column, with the dynamics' vapour
tendency Kuo's scheme read there, so that the column's physics can be set beside the GCM's step for step. Each step
writes, at the grid points of the row a caller names, the state the physics saw and what the physics made of it, in
the layout of plasim_column.

What the column leaves out. Every physics routine runs on the row alone, so the work PlaSim does across processes
covers the row: the humidity fixer's last, global step, which acts only where a whole latitude lacks the vapour to
fill its negative humidity; the rivers, which keep the speeds the GCM's restart holds and exchange no water with
other rows, and which return nothing to the air; the carbon cycle's global means; and the check of sea ice in percent.
Stochastic large-scale rain (NSTORAIN), whose random numbers PlaSim draws for each process, the semi-Lagrangian
humidity, aerosols, the stratosphere's cooling, glaciers and the initial short steps stop the column (master and
oroini in plasim_column.f90).

Evidence. Tests in climate/tests/test_plasim_column.py and lab/tests/test_plasim_column.py; the replay check's rules
and results in lab/validation/column_replay.json and models/exoplasim/README.md, "The forcing of a column and the
column of PlaSim's physics". A forced column keeps the GCM's dynamics whatever its own physics does: in the test runs
it held the Open Moon's frozen first lunar day within the check's rules and left Earth's warm pool after 6-11 days.

The lab's own module and Fortran; the Fortran is distributed, as ExoPlaSim is, under the GNU GPL version 3.
"""
from __future__ import annotations

import datetime
import hashlib
import io
import json
import os
import re
import shutil
import stat
import struct
import subprocess
import tarfile
import tempfile
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DRIVER, MPI_LAYER = 'plasim_column.f90', 'plasim_column_mpi.f90'
EXECUTABLE = 'plasim_column.x'
SOURCES = 'exoplasim-3.4.2/exoplasim/plasim/src/'             # the archive's PlaSim sources
CONFIGURED = ('most_compiler', 'most_precision_optionsx')       # what ExoPlaSim's configure wrote for the machine
# The makefile's choices: the column's message-passing layer, PlaSim's single-process utilities, coupler and FFT, as
# compile.sh exports them for one process (compile.sh:255-285)
MAKE = dict(MPIMOD='plasim_column_mpi', UTILMOD='utilities_stub', OCEANCOUP='cpl_stub', FFTMOD='fftmod')
# The routines the driver takes over, by the object that holds PlaSim's own
REPLACED = {'plasim.o': 'master_', 'rainmod.o': 'mkdqtgp_', 'utilities_stub.o': 'makeareas_',
            'glaciermod.o': 'oroini_'}
PRECISION = 8                                                    # compile.sh's -p 8, double precision
TIMEOUT_S = 3600
INPUT_NAMES = re.compile(r'(_namelist|\.sra|\.dat)$|^lab_rain_law\.txt$')   # the GCM run's inputs the column reads
FORCING_CODES = {'t': 241, 'q': 242, 'u': 243, 'v': 244, 'lnps': 245}     # patch 21: the dynamics' tendencies
STATE_CODES = {'t': 246, 'q': 247, 'u': 248, 'v': 249, 'ps': 250}         # and the state the physics sees
# With the GCM's windows, the state the physics sees steps forward under them, or on PlaSim's leapfrog and filter
SCHEMES = {'forward': 1, 'leapfrog': 2}
PART_1 = (('t', 1), ('q', 1), ('u', 0), ('v', 0), ('ps', None))
PART_2 = (('dtdt', 0), ('dqdt', 0), ('dudt', 0), ('dvdt', 0), ('dqt', 0), ('gqdt', 0), ('t', 1), ('q', 1),
          ('convective_rain', None), ('large_scale_rain', None), ('snow', None), ('evaporation', None),
          ('sensible_heat', None), ('latent_heat', None), ('surface_solar', None), ('surface_thermal', None),
          ('cloud', 0))


# The build.

def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def toolchain() -> dict:
    """The tools the column compiles and links with, each with the first line of its version."""
    out = {}
    for name in ('gfortran', 'gcc', 'objcopy', 'make', 'patch'):
        path = shutil.which(name)
        if path is None:
            raise RuntimeError(f'the column takes {name}, which this machine lacks')
        done = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=60)
        out[name] = dict(path=path, version=((done.stdout or done.stderr).splitlines() or [''])[0].strip())
    return out


def build_inputs(patches, levels: int, *, archive, configured, latitudes: int = 32) -> tuple[dict, dict]:
    """The build's inputs as its key hashes them, and the bytes it is made from: the pinned archive, the patches in
    order, the compile files ExoPlaSim's configure wrote (in the package folder `configured`), the column's two Fortran
    files, the grid, the replaced routines and the toolchain."""
    if latitudes not in (32, 64) or not isinstance(levels, int) or levels < 2:
        raise ValueError(f'the column compiles for T21 or T42 (32 or 64 latitudes) and two levels or more, where '
                         f'{latitudes} latitudes and {levels!r} levels are given')
    archive = Path(archive)
    data = dict(archive=archive.read_bytes(),
                patches=[(Path(p).name, Path(p).read_bytes()) for p in patches],
                configured={name: (Path(configured) / name).read_bytes() for name in CONFIGURED},
                fortran={name: (HERE / name).read_bytes() for name in (DRIVER, MPI_LAYER)})
    made = dict(model='plasim-column', archive=dict(name=archive.name, sha256=_sha256(data['archive'])),
                patches=[dict(name=n, sha256=_sha256(b)) for n, b in data['patches']],
                configured={n: _sha256(b) for n, b in data['configured'].items()},
                fortran={n: _sha256(b) for n, b in data['fortran'].items()},
                grid=dict(latitudes=latitudes, levels=levels, processes=latitudes, precision=PRECISION),
                make=MAKE, replaced=REPLACED, toolchain=toolchain())
    return made, data


def key(made: dict) -> str:
    return _sha256(json.dumps(made, sort_keys=True, separators=(',', ':')).encode())


def build(patches, levels: int, *, archive, configured, folder, latitudes: int = 32) -> Path:
    """The column's build in `folder` (a store's builds/), compiled where the folder lacks it: plasim-column-<the key's
    first 16 hex digits>/, read-only, holding EXECUTABLE, compile.log and its record build.json, written last. A build
    found there is checked against its record."""
    made, data = build_inputs(patches, levels, archive=archive, configured=configured, latitudes=latitudes)
    k = key(made)
    target = Path(folder) / f'plasim-column-{k[:16]}'
    if (target / 'build.json').is_file():
        return _checked(target, k)
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = Path(tempfile.mkdtemp(prefix=f'.{target.name}.part-', dir=target.parent))
    try:
        record = _make(made, data, k, partial)
        (partial / 'build.json').write_text(json.dumps(record, indent=1, sort_keys=True) + '\n')
        for root, _, files in os.walk(partial):
            for name in files:
                p = Path(root) / name
                p.chmod((p.stat().st_mode | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH) & ~0o222)
        partial.chmod(0o555)
        try:
            os.replace(partial, target)
        except OSError:
            if not (target / 'build.json').is_file():      # a build of the same key that lands first stands
                raise
            _remove(partial)
            return _checked(target, k)
    except BaseException:
        _remove(partial)
        raise
    return target


def _make(made: dict, data: dict, k: str, partial: Path) -> dict:
    start = time.monotonic()
    work = partial / 'work'
    src = work / 'plasim' / 'src'
    src.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(data['archive']), mode='r:gz') as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.startswith(SOURCES) and '/' not in member.name[len(SOURCES):]:
                (src / member.name[len(SOURCES):]).write_bytes(tar.extractfile(member).read())
    log = open(partial / 'compile.log', 'wb')
    try:
        def step(command, cwd, **kw):
            log.write(('$ ' + ' '.join(command) + '\n').encode())
            log.flush()
            done = subprocess.run(command, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, timeout=TIMEOUT_S, **kw)
            if done.returncode:
                log.flush()
                tail = (partial / 'compile.log').read_text(errors='replace')[-3000:]
                raise RuntimeError(f'the column\'s build stopped at {command[0]}:\n{tail}')
        for name, patch in data['patches']:
            log.write(f'$ patch -p1 < {name}\n'.encode())
            done = subprocess.run(['patch', '-p1', '--quiet', '--no-backup-if-mismatch'], input=patch, cwd=work,
                                  capture_output=True, timeout=120)
            if done.returncode:
                raise RuntimeError(f'{name} fails to apply to the pinned sources: {(done.stdout + done.stderr).decode()}')
        sources = {p.name: _sha256(p.read_bytes()) for p in sorted(src.iterdir()) if p.suffix in ('.f90', '.c')}
        grid = made['grid']
        bld = partial / 'bld'
        shutil.copytree(src, bld)
        for name, text in data['fortran'].items():
            (bld / name).write_bytes(text)
        (bld / 'resmod.f90').write_text(f'      module resmod\n      parameter(NLAT_ATM = {grid["latitudes"]})\n'
                                        f'      parameter(NLEV_ATM = {grid["levels"]})\n'
                                        f'      parameter(NPRO_ATM = {grid["processes"]})\n      end module resmod\n')
        precision = data['configured']['most_precision_optionsx'].decode().splitlines()
        precision[0] += str(PRECISION)                         # compile.sh:270-276
        rules = ('\ncolumn-objects: $(OBJ)\n\ncolumn-object-list:\n\t@echo $(OBJ)\n')
        (bld / 'makefile').write_text(data['configured']['most_compiler'].decode() + '\n' + '\n'.join(precision) + '\n'
                                      + (bld / 'make_plasim').read_text() + rules)
        env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': os.environ.get('HOME', '/tmp'),
               'LANG': 'C', 'LC_ALL': 'C', **MAKE}
        step(['nice', '-n', '10', 'make', '-e', 'column-objects'], bld, env=env)
        listed = subprocess.run(['make', '-e', '-s', 'column-object-list'], cwd=bld, env=env, capture_output=True,
                                text=True, timeout=120)
        objects = listed.stdout.split()
        if listed.returncode or not set(REPLACED) <= set(objects):
            raise RuntimeError(f'PlaSim\'s makefile lists {objects}, which lacks a replaced object {sorted(REPLACED)}')
        compiler = dict(line.split('=', 1) for line in data['configured']['most_compiler'].decode().splitlines()
                        if '=' in line and not line.startswith('#'))
        f90, flags = compiler['MOST_F90'].strip(), compiler['MOST_F90_OPTS'].split()
        linked = []
        for name in objects:
            if name in REPLACED:
                weak = name[:-2] + '_weak.o'
                step(['objcopy', f'--weaken-symbol={REPLACED[name]}', name, weak], bld)
                linked.append(weak)
            else:
                linked.append(name)
        step([f90, '-c', *flags, f'-fdefault-real-{PRECISION}', DRIVER], bld)
        step([f90, '-o', EXECUTABLE, *flags, DRIVER[:-4] + '.o', *linked], bld)
        shutil.copy2(bld / EXECUTABLE, partial / EXECUTABLE)
    finally:
        log.close()
    shutil.rmtree(work)
    shutil.rmtree(bld)
    executable = (partial / EXECUTABLE).read_bytes()
    return dict(schema='world-crafting.plasim-column/0', key=k, inputs=made, sources=sources,
                executable=dict(name=EXECUTABLE, sha256=_sha256(executable)),
                compile_log_sha256=_sha256((partial / 'compile.log').read_bytes()),
                seconds=round(time.monotonic() - start, 1),
                made=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))


def _checked(target: Path, k: str) -> Path:
    record = json.loads((target / 'build.json').read_text())
    if record.get('key') != k:
        raise RuntimeError(f'{target}: its record names key {record.get("key")}, where its inputs give {k}')
    if _sha256((target / EXECUTABLE).read_bytes()) != record['executable']['sha256']:
        raise RuntimeError(f'{target}: its executable differs from its record')
    return target


def _remove(path: Path) -> None:
    if not path.exists():
        return
    for root, _, _ in os.walk(path):
        Path(root).chmod(0o700)
    shutil.rmtree(path)


# Fortran's sequential records.

def records(path) -> list[bytes]:
    """A file of Fortran's sequential unformatted records with 4-byte little-endian markers, as bytes."""
    data, out, i = Path(path).read_bytes(), [], 0
    while i < len(data):
        if i + 4 > len(data):
            raise ValueError(f'{path}: a record at byte {i} breaks off in its marker')
        n = struct.unpack('<i', data[i:i + 4])[0]
        if n < 0 or i + 8 + n > len(data) or struct.unpack('<i', data[i + 4 + n:i + 8 + n])[0] != n:
            raise ValueError(f'{path}: the record at byte {i} closes with another length than it opens with')
        out.append(data[i + 4:i + 4 + n])
        i += n + 8
    return out


def iter_records(path):
    """The records of a file as `records` reads them, one at a time from the disk, so that a GCM's output of
    gigabytes passes through memory a record at a time."""
    with open(path, 'rb') as f:
        while True:
            head = f.read(4)
            if not head:
                return
            if len(head) < 4:
                raise ValueError(f'{path}: a record breaks off in its marker')
            n = struct.unpack('<i', head)[0]
            body, tail = f.read(n), f.read(4)
            if n < 0 or len(body) != n or len(tail) != 4 or struct.unpack('<i', tail)[0] != n:
                raise ValueError(f'{path}: a record closes with another length than it opens with')
            yield body


def record(*arrays) -> bytes:
    """One sequential record holding the arrays' bytes in order, Fortran's order for each."""
    body = b''.join(np.asarray(a).ravel(order='F').tobytes() for a in arrays)
    return struct.pack('<i', len(body)) + body + struct.pack('<i', len(body))


# The physics' inputs and outputs, from the GCM's plasim_column or the column's column_output.

def read_dump(path) -> list[dict]:
    """The steps a dump holds, each with its step number, its grid points' count, its row (0 in the GCM's file) and two
    parts: `inputs`, the state the physics saw (temperature and humidity with the surface's in their last level, the
    winds and the surface pressure, Pa) and psurf; and `outputs`, what the physics made of it (PART_2). Each field is
    (levels, points), top first, or (points,)."""
    raw = records(path)
    if len(raw) % 4:
        raise ValueError(f'{path}: a dump holds two parts of two records a step, where it holds {len(raw)} records')
    steps = []
    for k in range(0, len(raw), 4):
        parts = []
        for h, v in ((raw[k], raw[k + 1]), (raw[k + 2], raw[k + 3])):
            nstep, part, points, levels, count, row = struct.unpack('<6i', h)
            values = np.frombuffer(v, '<f8')
            if values.size != count:
                raise ValueError(f'{path}: step {nstep} part {part} holds {values.size} values, where its header '
                                 f'names {count}')
            parts.append((nstep, part, points, levels, row, values))
        (n1, p1, points, levels, row, v1), (n2, p2, _, _, _, v2) = parts
        if (p1, p2) != (1, 2) or n1 != n2:
            raise ValueError(f'{path}: step {n1} holds parts {p1} and {p2} of steps {n1} and {n2}')
        inputs = _unpack(v1, PART_1, points, levels)
        inputs['psurf'] = float(v1[-1])
        steps.append(dict(nstep=n1, points=points, levels=levels, row=row, inputs=inputs,
                          outputs=_unpack(v2, PART_2, points, levels)))
    return steps


def _unpack(values, layout, points, levels) -> dict:
    out, o = {}, 0
    for name, extra in layout:
        n = 1 if extra is None else levels + extra
        a = values[o:o + n * points].reshape(n, points)
        out[name] = a[0] if extra is None else a
        o += n * points
    if o not in (values.size, values.size - 1):
        raise ValueError(f'a part holds {values.size} values, where its layout takes {o}')
    return out


def row_of(field, row: int, nlon: int):
    """A global field's (..., points) values in the GCM's row `row`, 1 the northernmost."""
    return field[..., (row - 1) * nlon:row * nlon]


# PlaSim's raw output.

def read_output(path, codes) -> dict:
    """The records of PlaSim's raw output (outmod.f90) with the given codes: for each code its fields, (records,
    levels, points) for a field written by level, (records, points) for one written once, in single precision as
    written, with each record's steps since the run's start (the header's seventh integer)."""
    raw = iter_records(path)
    first = struct.unpack('<8i', next(raw))
    if first[0] != 333:
        raise ValueError(f'{path}: the first header names code {first[0]}, where PlaSim writes 333')
    next(raw)                                                    # the table of half levels
    found = {c: {} for c in codes}
    for h in raw:
        v = next(raw, None)
        if v is None or len(h) != 32:
            raise ValueError(f'{path}: PlaSim\'s output pairs a header of eight integers with each field')
        code, level, _, _, _, _, steps, _ = struct.unpack('<8i', h)
        if code in found:
            found[code].setdefault(steps, {})[level] = np.frombuffer(v, '<f4')
    out = {}
    for code, by_step in found.items():
        if not by_step:
            raise ValueError(f'{path} holds no records of code {code}')
        steps = sorted(by_step)
        levels = sorted(by_step[steps[0]])
        if any(sorted(by_step[s]) != levels for s in steps):
            raise ValueError(f'{path}: code {code} holds other levels in some records')
        field = np.array([[by_step[s][lv] for lv in levels] for s in steps], float)
        out[code] = dict(steps=np.array(steps), field=field[:, 0] if levels == [0] else field)
    return out


def windows(gcm_folder, row: int, nlon: int = 64) -> dict:
    """The forcing of the column at row `row` from a GCM run that wrote patch 21's codes: for each window, its steps
    and the dynamics' tendencies of temperature (K/s), vapour (kg/kg/s), the winds (m/s2), each (windows, points,
    levels), and of the surface pressure's log (1/s), (windows, points); and the state the physics saw at each window's
    end. The first window runs from the run's first step to the step before its first output, each later window from
    one output step to the step before the next."""
    codes = read_output(Path(gcm_folder) / 'plasim_output', list(FORCING_CODES.values()) + list(STATE_CODES.values()))
    steps = codes[FORCING_CODES['t']]['steps']
    if any(not np.array_equal(codes[c]['steps'], steps) for c in codes):
        raise ValueError(f'{gcm_folder}: the forcing\'s codes fall at different steps')
    lengths = np.diff(np.r_[0, steps])
    get = lambda c: np.moveaxis(row_of(codes[c]['field'], row, nlon), -1, 1) if codes[c]['field'].ndim == 3 \
        else row_of(codes[c]['field'], row, nlon)
    dyn = {name: get(code) for name, code in FORCING_CODES.items()}
    state = {name: get(code) for name, code in STATE_CODES.items()}
    return dict(steps=lengths, ends=steps, dynamics=dyn, state=state, row=row)


def start(gcm_folder, row: int, step: int = 0) -> dict:
    """The state the GCM's physics saw at its run's first step (or the dump's step `step`), at row `row`, from
    plasim_column: temperature, vapour and winds (points, levels), the surface pressure (Pa) and psurf, with the
    dynamics' vapour tendency Kuo's scheme read there."""
    dump = read_dump(Path(gcm_folder) / 'plasim_column')[step]
    nlon = int(round(np.sqrt(2 * dump['points'])))
    i, o = dump['inputs'], dump['outputs']
    lev = dump['levels']
    pick = lambda a: row_of(a[:lev], row, nlon).T
    return dict(nstep=dump['nstep'], t=pick(i['t']), q=pick(i['q']), u=pick(i['u']), v=pick(i['v']),
                ps=row_of(i['ps'], row, nlon), psurf=i['psurf'], dqt=pick(o['dqt']))


# The column's folder and run.

def prepare(folder, gcm_folder, restart, *, row: int, steps: int, points=None, start: dict, windows: dict | None = None,
            given: list | None = None, scheme: str = 'forward', changes: dict | None = None) -> Path:
    """A new folder for the column: the GCM run's inputs (its namelists, surface files and tables, INPUT_NAMES), its
    restart as plasim_restart, column_namelist and column_input. With `windows` (mode 1) the column starts from `start`
    and steps on under the windows' dynamics' tendencies, its state forward or on PlaSim's leapfrog (`scheme`); with
    `given` (mode 2), a list of states as `start` gives them, one a step, each step's state is the GCM's. `points`
    lists the row's grid points (1 to NLON) written to column_output, all of them by default. `changes` sets entries
    of the GCM's namelists in the column's copies, by file and name, such as a test of the vertical diffusion's
    mixing length: {'fluxmod_namelist': {'VDIFF_LAMM': 966.4}}."""
    folder, gcm_folder = Path(folder), Path(gcm_folder)
    if (windows is None) == (given is None):
        raise ValueError('the column takes the GCM\'s windows (mode 1) or its states step by step (mode 2)')
    nlon = start['t'].shape[0]
    points = list(range(1, nlon + 1)) if points is None else [int(p) for p in points]
    if not points or min(points) < 1 or max(points) > nlon:
        raise ValueError(f'the output takes grid points 1 to {nlon} of the row, where {points} are given')
    folder.mkdir(parents=True, exist_ok=False)
    for p in sorted(gcm_folder.iterdir()):
        if p.is_file() and INPUT_NAMES.search(p.name):
            shutil.copy2(p, folder / p.name)
    shutil.copy2(restart, folder / 'plasim_restart')
    for name, entries in (changes or {}).items():
        path = folder / name
        if not name.endswith('_namelist') or not path.is_file():
            raise ValueError(f'{name}: the column changes entries of the GCM\'s namelists, which its folder holds')
        path.write_text(namelist_with(path.read_text(), entries))
    mode = 1 if windows is not None else 2
    if scheme not in SCHEMES:
        raise ValueError(f'the column steps by one of {tuple(SCHEMES)}, where {scheme!r} is given')
    (folder / 'column_namelist').write_text(f' &column_nl\n nrow = {row}\n nsteps = {steps}\n nmode = {mode}\n'
                                            f' nscheme = {SCHEMES[scheme]}\n /\n')
    stack = lambda s: np.stack([s['t'], s['q'], s['u'], s['v']], axis=-1)
    out = [record(np.array([len(windows['steps']) if mode == 1 else len(given), len(points)], '<i4')),
           record(np.array(points, '<i4')), record(np.array([start['psurf']], '<f8'))]
    if mode == 1:
        if int(np.sum(windows['steps'])) < steps:
            raise ValueError(f'the windows cover {int(np.sum(windows["steps"]))} steps, where the column runs {steps}')
        out.append(record(stack(start).astype('<f8'), np.asarray(start['ps'], '<f8')))
        d = windows['dynamics']
        for k, n in enumerate(windows['steps']):
            out.append(record(np.array([n], '<i4')))
            out.append(record(np.stack([d['t'][k], d['q'][k], d['u'][k], d['v'][k]], axis=-1).astype('<f8'),
                              np.asarray(d['lnps'][k], '<f8')))
    else:
        if len(given) < steps:
            raise ValueError(f'{len(given)} states are given, where the column runs {steps} steps')
        for s in given:
            out.append(record(stack(s).astype('<f8'), np.asarray(s['ps'], '<f8'), np.asarray(s['dqt'], '<f8')))
    (folder / 'column_input').write_bytes(b''.join(out))
    return folder


def namelist_with(text: str, entries: dict) -> str:
    """A namelist's text with each entry set: an entry the text states takes the new value in its line, and one it
    lacks joins before the closing line."""
    lines = text.splitlines()
    end = next((k for k, line in enumerate(lines) if line.strip().startswith('/')), None)
    if end is None or not lines or not lines[0].strip().startswith('&'):
        raise ValueError('a namelist opens with &name and closes with /')
    for name, value in entries.items():
        value = repr(float(value)) if isinstance(value, float) else str(int(value))
        found = [k for k, line in enumerate(lines) if re.match(rf'\s*{re.escape(name)}\s*=', line, flags=re.I)]
        if found:
            lines[found[0]] = f' {name} = {value}'
        else:
            lines.insert(end, f' {name} = {value}')
            end += 1
    return '\n'.join(lines) + '\n'


def run(folder, executable, *, timeout: float = 3600.0) -> subprocess.CompletedProcess:
    """The column run in its folder, under nice; refused where it stops early or PlaSim aborts."""
    done = subprocess.run(['nice', '-n', '10', str(executable)], cwd=folder, capture_output=True, text=True,
                          timeout=timeout)
    abort = Path(folder) / 'Abort_Message'
    if done.returncode or abort.exists():
        why = abort.read_text() if abort.exists() else ''
        raise RuntimeError(f'the column stopped ({done.returncode}): {why}{done.stdout[-1500:]}{done.stderr[-1500:]}')
    return done


# The GCM's grid and a site.

def gaussian_latitudes(nlat: int = 32) -> np.ndarray:
    """The Gaussian latitudes, degrees, from the north as PlaSim's rows run."""
    nodes = np.polynomial.legendre.leggauss(nlat)[0]
    return np.degrees(np.arcsin(np.sort(nodes)[::-1]))


def site_point(gcm_folder, site: dict, gravity_m_s2: float, nlat: int = 32) -> tuple[int, int]:
    """The GCM's grid point at a site, as its row (1 the northernmost) and its place in the row (1 at 0 E): of the
    site's cells (climate/crm/gcm_site.py, site_cells), from the run's land mask and surface geopotential (codes 172
    and 129, none for a world all ocean), the one nearest the site's centre."""
    from climate.crm import gcm_site as gs
    site = gs.check_site(site)
    folder = Path(gcm_folder)
    lat, lon = gaussian_latitudes(nlat), np.arange(2 * nlat) * 360.0 / (2 * nlat)
    read = lambda code, empty: gs.read_sra(folder / f'N{nlat:03d}_surf_{code:04d}.sra') \
        if (folder / f'N{nlat:03d}_surf_{code:04d}.sra').exists() else np.full((nlat, 2 * nlat), empty)
    cells = gs.site_cells(lat, lon, read(172, 0.0) > 0.5, read(129, 0.0) / gravity_m_s2, site)
    jj, ii = np.nonzero(cells)
    a, b = np.radians(lat[jj]), np.radians(site['lat_deg'])
    c = np.cos(a) * np.cos(b) * np.cos(np.radians(lon[ii] - site['lon_deg'])) + np.sin(a) * np.sin(b)
    k = int(np.argmax(c))
    return int(jj[k]) + 1, int(ii[k]) + 1


# The replay check: the column under the GCM's forcing set beside the GCM's own records at the same grid point.

# The check's tolerances, fixed on 2026-11-18 at 11:56 EST before the column's first lunar day ran
# (models/exoplasim/README.md, "A column of PlaSim's physics"): rain by quarter of the lunar day, mm/day, within the
# larger of a share of the GCM's and a floor; the lowest level's temperature (K), vapour (g/kg) and theta-e (K); the
# boundary layer's theta-e over sigma 1.0-0.85 (K), the lowest level's excess over it (K), and the vapour's fall from
# the lowest level to the level nearest sigma 0.85 (g/kg).
TOLERANCES = dict(rain_share=0.25, rain_floor_mm_day=0.5, t_low_k=1.0, q_low_g_kg=1.0, theta_e_low_k=2.0,
                  theta_e_b_k=1.5, excess_k=1.0, vapour_fall_g_kg=1.0)
QUARTERS = ('morning', 'afternoon', 'evening', 'after_midnight')   # hour angle -90 to 0, 0-90, 90-180, -180 to -90
BOUNDARY_LAYER, LOWER_TROPOSPHERE = (0.85, 1.0), (0.50, 0.85)      # sigma, as the gap readings take them
WATER_DENSITY = 1000.0                                               # PlaSim's precipitation, m/s of water


def theta_e(t, p, q):
    """Equivalent potential temperature (K) by Bolton (1980) eq. 43, T_L from eq. 22 by relative humidity, with
    Bolton's own saturation pressure; t (K), p (Pa), q specific humidity (kg/kg). The gap readings' definition
    (research drive, agents/gap_readings/scripts/gr_common.py, 17 November 2026)."""
    t, p, q = (np.asarray(x, float) for x in (t, p, q))
    q = np.maximum(q, 1e-10)
    r = q / (1.0 - q)
    eps = 287.04 / 461.5
    e = r * p / (eps + r)
    es = 611.2 * np.exp(17.67 * (t - 273.15) / (t - 29.65))
    tl = 1.0 / (1.0 / (t - 55.0) - np.log(np.clip(e / es, 1e-6, None)) / 2840.0) + 55.0
    rg = r * 1000.0
    return t * (1.0e5 / p) ** (0.2854 * (1.0 - 0.28e-3 * rg)) * np.exp((3.376 / tl - 0.00254) * rg * (1.0 + 0.81e-3 * rg))


def theta_e_sat(t, p):
    """Saturation theta-e (K): Bolton's eq. 43 at the saturation mixing ratio over liquid, T_L = T."""
    t, p = np.asarray(t, float), np.asarray(p, float)
    es = 611.2 * np.exp(17.67 * (t - 273.15) / (t - 29.65))
    rs = (287.04 / 461.5) * es / np.maximum(p - es, 1.0)
    rg = rs * 1000.0
    return t * (1.0e5 / p) ** (0.2854 * (1.0 - 0.28e-3 * rg)) * np.exp((3.376 / t - 0.00254) * rg * (1.0 + 0.81e-3 * rg))


def overlap(half_levels, lo: float, hi: float) -> np.ndarray:
    """Each layer's thickness in sigma inside [lo, hi], top first."""
    edges = np.r_[0.0, np.asarray(half_levels, float)]
    return np.clip(np.minimum(edges[1:], hi) - np.maximum(edges[:-1], lo), 0.0, None)


def measures(t, q, ps, half_levels) -> dict:
    """The low air and boundary layer of columns (..., levels, top first): the lowest level's temperature (K), vapour
    (g/kg) and theta-e (K); theta_eB over sigma 1.0-0.85 and theta*_eL over 0.85-0.50 (K), each a mean weighted by the
    layers' overlap in sigma; the excess of the lowest level's theta-e over theta_eB; the vapour's fall from the lowest
    level to the level nearest sigma 0.85 (g/kg); and B_L (K), the deep-inflow buoyancy of Ahmed and Neelin (2018) with
    the gap readings' two layers."""
    half = np.asarray(half_levels, float)
    sigma = 0.5 * (np.r_[0.0, half[:-1]] + half)
    t, q = np.asarray(t, float), np.asarray(q, float)
    p = sigma * np.asarray(ps, float)[..., None]
    the, thes = theta_e(t, p, q), theta_e_sat(t, p)
    wb, wl = overlap(half, *BOUNDARY_LAYER), overlap(half, *LOWER_TROPOSPHERE)
    the_b = (the * wb).sum(-1) / wb.sum()
    the_l, thes_l = (the * wl).sum(-1) / wl.sum(), (thes * wl).sum(-1) / wl.sum()
    db, dl = BOUNDARY_LAYER[1] - BOUNDARY_LAYER[0], LOWER_TROPOSPHERE[1] - LOWER_TROPOSPHERE[0]
    w_b = db / dl * np.log(1.0 + dl / db)
    top = int(np.argmin(np.abs(sigma - BOUNDARY_LAYER[0])))
    return dict(t_low_k=t[..., -1], q_low_g_kg=1e3 * q[..., -1], theta_e_low_k=the[..., -1], theta_e_b_k=the_b,
                excess_k=the[..., -1] - the_b, vapour_fall_g_kg=1e3 * (q[..., -1] - q[..., top]),
                theta_e_sat_l_k=thes_l, b_l_k=w_b * (the_b - thes_l) - (1.0 - w_b) * (thes_l - the_l))


def half_levels(gcm_folder) -> np.ndarray:
    """The half levels the GCM ran on, from the table its output opens with (outmod.f90, outini)."""
    raw = iter_records(Path(gcm_folder) / 'plasim_output')
    first, table = next(raw), next(raw)
    return np.frombuffer(table, '<f4')[:struct.unpack('<8i', first)[6]].astype(float)


def joined(windows: dict, count: int) -> dict:
    """The windows joined `count` at a time, each joined window's tendencies the mean of its windows' weighted by
    their steps."""
    n = windows['steps']
    groups = [slice(k, min(k + count, n.size)) for k in range(0, n.size, count)]
    weight = lambda a, g: np.tensordot(n[g], a[g], axes=(0, 0)) / n[g].sum()
    return dict(windows, steps=np.array([n[g].sum() for g in groups]),
                dynamics={k: np.array([weight(a, g) for g in groups]) for k, a in windows['dynamics'].items()})


def replay_series(gcm_folder, column_output, *, row: int, point: int) -> dict:
    """The GCM's records at one grid point of the row (`point`, 1 at 0 E) and the column's at the same steps: for each
    of the GCM's outputs, its hour angle at the point (degrees, from the subsolar longitude of the output's mean solar
    height, climate/crm/gcm_site.py), the rain over its steps (mm/day) and `measures` of the state the physics saw at
    its step."""
    from climate.crm import gcm_site as gs
    folder = Path(gcm_folder)
    codes = read_output(folder / 'plasim_output', [142, 143, 318] + list(STATE_CODES.values()))
    steps = codes[318]['steps']
    first = read_dump(folder / 'plasim_column')[0]['nstep']
    nlon = int(round(np.sqrt(2 * codes[318]['field'].shape[-1])))
    nlat = nlon // 2
    lat, lon = gaussian_latitudes(nlat), np.arange(nlon) * 360.0 / nlon
    czen = codes[318]['field'].reshape(-1, nlat, nlon)
    hour = (lon[point - 1] - gs.subsolar_longitude(czen, lat, lon) + 180.0) % 360.0 - 180.0
    at = lambda code: row_of(codes[code]['field'], row, nlon)[..., point - 1]
    half = half_levels(folder)
    gcm_rain = (at(142) + at(143)) * WATER_DENSITY * 86400.0
    gcm = measures(at(STATE_CODES['t']), at(STATE_CODES['q']), at(STATE_CODES['ps']), half)
    col = read_dump(column_output)
    by_step = {s['nstep']: s for s in col}
    rain_steps = np.array([s['nstep'] for s in col])
    if col[0]['points'] != nlon:
        raise ValueError('the replay reads a column that wrote every grid point of its row')
    rain = np.array([(s['outputs']['convective_rain'][point - 1] + s['outputs']['large_scale_rain'][point - 1])
                     for s in col]) * WATER_DENSITY * 86400.0
    ends = first + steps                      # each output's step
    starts = np.r_[first - 1, ends[:-1]]      # its rain's steps run after the step before
    col_rain = np.array([rain[(rain_steps > a) & (rain_steps <= b)].mean() if ((rain_steps > a) & (rain_steps <= b)).any()
                         else np.nan for a, b in zip(starts, ends)])
    keep = np.array([e in by_step for e in ends])
    pick = lambda e, name: by_step[e]['inputs'][name][..., point - 1]
    lev = col[0]['levels']
    state = {name: np.array([pick(e, name)[:lev] if name in ('t', 'q') else pick(e, name) for e in ends[keep]])
             for name in ('t', 'q', 'ps')}
    column = measures(state['t'], state['q'], state['ps'], half)
    return dict(hour_deg=hour[keep], steps=ends[keep], gcm=dict(rain_mm_day=gcm_rain[keep], **{k: v[keep] for k, v in gcm.items()}),
                column=dict(rain_mm_day=col_rain[keep], **column), half_levels=half)


def quarter_of(hour) -> np.ndarray:
    h = (np.asarray(hour, float) + 180.0) % 360.0 - 180.0
    return np.where(h >= 90.0, 2, np.where(h >= 0.0, 1, np.where(h >= -90.0, 0, 3)))


def replay_verdict(series: dict, tolerances: dict = TOLERANCES) -> dict:
    """Quarter means of the GCM's and the column's quantities, their differences, and the verdict by the tolerances:
    PASS where every quantity holds in every quarter, FAIL naming each quarter and quantity that breaks."""
    q = quarter_of(series['hour_deg'])
    out, breaks = {}, []
    for name in series['gcm']:
        g, c = np.asarray(series['gcm'][name], float), np.asarray(series['column'][name], float)
        rows = {}
        for k, quarter in enumerate(QUARTERS):
            m = (q == k) & np.isfinite(g) & np.isfinite(c)
            if not m.any():
                continue
            gm, cm = float(g[m].mean()), float(c[m].mean())
            if name == 'rain_mm_day':
                limit = max(tolerances['rain_share'] * abs(gm), tolerances['rain_floor_mm_day'])
            else:
                limit = tolerances.get(name)
            ok = None if limit is None else abs(cm - gm) <= limit
            rows[quarter] = dict(gcm=gm, column=cm, difference=cm - gm, limit=limit, holds=ok, records=int(m.sum()))
            if ok is False:
                breaks.append(f'{name} {quarter}')
        out[name] = rows
    return dict(quarters=out, verdict='PASS' if not breaks else 'FAIL', breaks=breaks)
