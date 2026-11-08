"""Builds: PlaSim compiled from ExoPlaSim at a point of the lab's patch series, kept in the store under a key of
everything that makes it (lab/design/architecture.md, "Model adapters").

A build extracts the ExoPlaSim 3.4.2 package from the pinned archive, takes from the lab's environment the compile
files ExoPlaSim's configure wrote there for this machine, applies the run's patch series and compiles PlaSim for the
run's resolution, levels, ranks and precision with ExoPlaSim's own compile script, as ExoPlaSim's Model calls it
(exoplasim/__init__.py:552-572), in a fixed environment. Each input is read once: the bytes the key hashes are the
bytes the build uses. The build lands in the store at builds/exoplasim-<the key's first 16 hex digits>/, read-only,
its record build.json written last, so that a folder holding its record is complete; a build found there is checked
against its record before the lab reuses it.
"""
from __future__ import annotations

import datetime
import hashlib
import io
import json
import os
import shutil
import signal
import stat
import subprocess
import tarfile
import tempfile
import time
from pathlib import Path

from . import derive, exoplasim as ex
from .data import DataError
from .spec import LAB, canonical

PATCHES = LAB.parent / 'models' / 'exoplasim' / 'patches'
# The files of configure.sh that compile.sh reads (compile.sh:255-267), and the marker ExoPlaSim's Model checks before
# it configures a package anew (exoplasim/__init__.py:392-393).
CONFIGURED = ('most_compiler', 'most_compiler_mpi', 'most_precision_optionsx', 'most_debug_options', 'firstrun')
TOOLS = ('mpif90', 'mpicc', 'gfortran', 'gcc', 'mpirun', 'make')
PRECISIONS = (4, 8)                  # compile.sh's -p: single or double precision (compile.sh:77-89)
TIMEOUT_S = 3600                     # a compile's longest wait; a partial build older than this is abandoned
# The folders compile.sh compiles in and writes to (compile.sh:213-214, 289-290), which it takes as present: it runs
# `rm -rf *` after `cd plasim/bld/`, in whatever folder it then stands in.
WORK_FOLDERS = ('plasim/bld', 'plasim/bin')


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def package(env: Path) -> Path:
    """The ExoPlaSim package the lab's environment holds."""
    found = sorted(Path(env).glob('lib/python*/site-packages/exoplasim/__init__.py'))
    if len(found) != 1:
        raise DataError(f'{env}: the environment holds {len(found)} ExoPlaSim packages, where a build takes one')
    return found[0].parent


def environment() -> dict:
    """The fixed environment a build compiles in: the caller's PATH, home and temporary folder, and the C locale. Every
    other variable stays out, make's among them, which compile.sh's `make -e` would let override the makefile
    (compile.sh:286)."""
    return {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': os.environ.get('HOME', '/tmp'),
            'TMPDIR': os.environ.get('TMPDIR', '/tmp'), 'LANG': 'C', 'LC_ALL': 'C'}


def toolchain() -> dict:
    """The tools a build compiles and links with: each one's path and the first line of its version, and the MPI
    wrapper's compile line, which names the MPI library."""
    env, out = environment(), {}
    for name in TOOLS:
        path = shutil.which(name, path=env['PATH'])
        if path is None:
            raise DataError(f'a build takes {name}, which this machine lacks')
        done = subprocess.run([path, '--version'], env=env, capture_output=True, text=True, timeout=60)
        out[name] = dict(path=path, version=((done.stdout or done.stderr).splitlines() or [''])[0].strip())
    for flag in ('--showme', '-show'):       # Open MPI's, then MPICH's
        done = subprocess.run([out['mpif90']['path'], flag], env=env, capture_output=True, text=True, timeout=60)
        if done.returncode == 0 and done.stdout.strip():
            out['mpif90_line'] = done.stdout.strip()
            return out
    raise DataError('the MPI wrapper gives its compile line to neither --showme nor -show')


def gather(run: dict, *, env: Path, archive: Path = ex.ARCHIVE) -> tuple[dict, dict]:
    """A build's inputs, as its key hashes them, and the bytes it is made from: the pinned archive, the compile files
    configure wrote for this machine, the patches of the run's series in order, the grid, ExoPlaSim's compile flags
    and the toolchain."""
    derive.truncation(run['resolution'])                 # refuses a grid ExoPlaSim lacks
    for name in ('levels', 'ranks'):
        if isinstance(run[name], bool) or not isinstance(run[name], int) or run[name] < 1:
            raise DataError(f'a build takes a whole number of {name}, where the run states {run[name]!r}')
    if isinstance(run['precision'], bool) or run['precision'] not in PRECISIONS:
        raise DataError(f'a build compiles at precision {PRECISIONS[0]} or {PRECISIONS[1]}, where the run states '
                        f'{run["precision"]!r}')
    pkg = package(env)
    missing = [name for name in CONFIGURED if not (pkg / name).is_file()]
    if missing:
        raise DataError(f'{pkg}: ExoPlaSim\'s first run has yet to configure it, lacking {missing}')
    archive_bytes = ex._verified(str(archive), str(ex.PINS))
    configured = {name: (pkg / name).read_bytes() for name in CONFIGURED}
    patches = []
    for name in ex.series(run):
        path = PATCHES / name
        if not path.is_file():
            raise DataError(f'{path}: a patch of the run\'s series is missing')
        patches.append((name, path.read_bytes()))
    made = dict(model='exoplasim', archive=dict(name=Path(archive).name, sha256=_sha256(archive_bytes)),
                configured={name: _sha256(data) for name, data in configured.items()},
                patches=[dict(name=name, sha256=_sha256(data)) for name, data in patches],
                grid={k: run[k] for k in ('resolution', 'levels', 'ranks', 'precision')},
                flags=dict(debug=False, optimization=None, mars=False), toolchain=toolchain())
    return made, dict(archive=archive_bytes, configured=configured, patches=patches)


def key(inputs: dict) -> str:
    """The build's key: the sha256 of its inputs' canonical form."""
    return _sha256(canonical(inputs).encode())


def executable_name(run: dict) -> str:
    """The executable compile.sh writes for the run's grid (compile.sh:208-209)."""
    return f'most_plasim_t{derive.truncation(run["resolution"])}_l{run["levels"]}_p{run["ranks"]}.x'


def folder(store: Path, key_: str) -> Path:
    return Path(store) / 'builds' / f'exoplasim-{key_[:16]}'


def build(run: dict, *, store: Path, env: Path, archive: Path = ex.ARCHIVE) -> Path:
    """The run's build in the store, compiled where the store lacks it. Returns its folder, whose `exoplasim/` is the
    patched package with the compiled executable in plasim/run/, beside its record, build.json."""
    made, payload = gather(run, env=env, archive=archive)
    k = key(made)
    target = folder(store, k)
    if (target / 'build.json').is_file():
        return _checked(target, k)
    target.parent.mkdir(parents=True, exist_ok=True)
    _abandoned(target.parent)
    partial = Path(tempfile.mkdtemp(prefix=f'.{target.name}.part-', dir=target.parent))
    try:
        record = _make(run, made, k, payload, partial)
        (partial / 'build.json').write_text(json.dumps(record, indent=1, sort_keys=True) + '\n')
        _read_only(partial)
        try:
            os.replace(partial, target)
        except OSError:
            if not (target / 'build.json').is_file():     # a build of the same key that lands first stands
                raise
            _remove(partial)
            return _checked(target, k)
    except BaseException:
        _remove(partial)
        raise
    return target


def _make(run: dict, made: dict, k: str, payload: dict, partial: Path) -> dict:
    start = time.monotonic()
    copy = partial / 'exoplasim'
    with tarfile.open(fileobj=io.BytesIO(payload['archive']), mode='r:gz') as tar:
        members = []
        for member in tar.getmembers():
            if member.name.startswith(ex.PACKAGE) and len(member.name) > len(ex.PACKAGE):
                member.name = member.name[len(ex.PACKAGE):]
                members.append(member)
        tar.extractall(copy, members=members, filter='data')
    for name in WORK_FOLDERS:                    # the archive holds them empty, so it leaves them out
        (copy / name).mkdir(exist_ok=True)
    pristine = {str(p.relative_to(copy)): _sha256(p.read_bytes()) for p in (copy / 'plasim' / 'src').iterdir()
                if p.is_file()}
    for name, data in payload['configured'].items():
        (copy / name).write_bytes(data)
    for name, data in payload['patches']:
        done = subprocess.run(['patch', '-p1', '--quiet', '--no-backup-if-mismatch'], input=data, cwd=copy,
                              env=environment(), capture_output=True, timeout=120)
        if done.returncode:
            raise DataError(f'{name} fails to apply to the pinned sources: {(done.stdout + done.stderr).decode()}')
    if not all((copy / name).is_dir() for name in WORK_FOLDERS):
        raise DataError(f'{copy}: compile.sh empties plasim/bld after entering it, which the copy lacks')
    grid = made['grid']
    command = ['nice', '-n', '10', './compile.sh', '-n', str(grid['ranks']), '-p', str(grid['precision']),
               '-r', grid['resolution'], '-v', str(grid['levels'])]
    with open(partial / 'compile.log', 'wb') as log:
        process = subprocess.Popen(command, cwd=copy, env=environment(), stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        try:
            returncode = process.wait(timeout=TIMEOUT_S)
        except BaseException:
            os.killpg(process.pid, signal.SIGKILL)       # make and the compilers with it
            process.wait()
            raise
    executable = copy / 'plasim' / 'run' / executable_name(run)
    if returncode or not executable.is_file():
        tail = (partial / 'compile.log').read_text(errors='replace')[-3000:]
        raise DataError(f'compile.sh stopped with {returncode} and wrote no {executable.name}:\n{tail}')
    sources = {}
    for name, digest in pristine.items():
        now = _sha256((copy / name).read_bytes())
        if now != digest:
            sources[name] = now
    return dict(schema='worldlab.build.exoplasim/0', key=k, inputs=made, sources=sources,
                executable=dict(name=executable.name, sha256=_sha256(executable.read_bytes())),
                compile_log_sha256=_sha256((partial / 'compile.log').read_bytes()), command=command[3:],
                seconds=round(time.monotonic() - start, 1),
                made=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))


def _checked(target: Path, k: str) -> Path:
    """A build found in the store, once its record names the key and its executable the record's bytes."""
    record = json.loads((target / 'build.json').read_text())
    executable = target / 'exoplasim' / 'plasim' / 'run' / record.get('executable', {}).get('name', '')
    if record.get('key') != k:
        raise DataError(f'{target}: its record names key {record.get("key")}, where its inputs give {k}')
    if not executable.is_file() or _sha256(executable.read_bytes()) != record['executable']['sha256']:
        raise DataError(f'{target}: its executable differs from its record')
    return target


def _read_only(path: Path) -> None:
    """Every file and folder readable by all and writable by none, the executables kept executable."""
    for root, dirs, files in os.walk(path):
        for name in files:
            p = Path(root) / name
            if not p.is_symlink():
                p.chmod((p.stat().st_mode | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH) & ~0o222)
        Path(root).chmod(0o555)


def _remove(path: Path) -> None:
    """A folder removed whole, read-only parts included."""
    if not path.exists():
        return
    for root, _, _ in os.walk(path):
        Path(root).chmod(0o700)
    shutil.rmtree(path)


def _abandoned(builds: Path) -> None:
    """Partial builds older than the longest compile, left by a process stopped mid-build, removed."""
    for partial in builds.glob('.exoplasim-*.part-*'):
        if time.time() - partial.stat().st_mtime > TIMEOUT_S:
            _remove(partial)
