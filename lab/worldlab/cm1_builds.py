"""CM1's builds: CM1 r22.0 compiled from the pinned archive with the lab's patch series, kept in the store under a key
of everything that makes it (lab/design/architecture.md, "Model adapters"; plan.md, stage 3).

A build extracts CM1's sources and run files from the pinned archive, applies the OpenMP makefile, the core series and
the lab's series (models/cm1/README.md), checks the patched sources against the hash models/check_patches.sh records
for that series (expected-series.sha256), applies the optimisation's makefile patch and compiles with CM1's own
Makefile in a fixed environment, at reduced priority. A build that takes its world from the namelist compiles no macro,
so that one build serves every world through the entries of the lab's patches 06 to 08 (`world_g`, `world_co2`,
`world_o2`, `soil_dz1`, `sun_decl`); a build that compiles its world in passes CM1 the macros `TERLUNA_G`,
`TERLUNA_CO2` and `TERLUNA_O2`, as Terluna's builds do, and those values enter its key. Each input is read once, so
the bytes the key hashes are the bytes the build uses: the archive, the makefile's and the optimisation's patches, the
series' patches in order, the macros, the flags and the toolchain, with the processor a build at -march=native
compiles for. The build lands in the store at builds/cm1-<the key's first 16 hex digits>/, read-only, holding the
executable and the run files CM1 reads beside it (RRTMG's two tables and the land-use table), its record build.json
written last, so that a folder holding its record is complete; a build found there is checked against its record
before the lab reuses it.

The thin path builds the core and lab series alone. The variants' series (terrain, sea, twilight, electrified) apply
after the core in Terluna's builds and have yet to be checked after the lab's series, so a case that names a variant
is refused here until stage 3 widens.
"""
from __future__ import annotations

import datetime
import hashlib
import io
import json
import os
import re
import shutil
import signal
import subprocess
import tarfile
import tempfile
import time
from pathlib import Path

from . import builds as common
from .data import DataError
from .exoplasim import PINS, _verified
from .spec import LAB, canonical

ARCHIVE = LAB.parent / 'upstream' / 'cm1r22.0.tar.gz'
MODELS = LAB.parent / 'models' / 'cm1'
TREE = 'cm1r22.0/'
SERIES = ('series-core', 'series-lab')       # every build of the thin path, in this order
MAKEFILES = {'omp': 'patches/makefile-gnu-omp.patch'}
# The optimisation flags a build takes, by the makefile patch that sets them: CM1's own -O2, or Terluna's OpenMP
# default, which the lab's CM1 defaults take.
OPTIMIZATIONS = {'-O2': (), '-O3 -march=native': ('patches/makefile-omp-O3-march-native.patch',)}
WORLD_CONSTANTS = ('build', 'namelist')
MACROS = ('TERLUNA_G', 'TERLUNA_CO2', 'TERLUNA_O2')
TOOLS = ('gfortran', 'cpp', 'make')
# The files a run reads beside the executable: RRTMG's longwave and shortwave tables and the land-use table.
RUN_FILES = ('RRTMG_LW_DATA', 'RRTMG_SW_DATA', 'LANDUSE.TBL')
EXECUTABLE = 'cm1.exe'
TIMEOUT_S = 3600                             # a compile's longest wait; a partial build older than this is abandoned
PREFIX = 'cm1'


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def toolchain(native: bool) -> dict:
    """The tools a build compiles with, each one's path and the first line of its version, and for a build at
    -march=native the processor it compiles for: gfortran's resolved -march and the CPU's model name."""
    env, out = common.environment(), {}
    for name in TOOLS:
        path = shutil.which(name, path=env['PATH'])
        if path is None:
            raise DataError(f'a CM1 build takes {name}, which this machine lacks')
        done = subprocess.run([path, '--version'], env=env, capture_output=True, text=True, timeout=60)
        out[name] = dict(path=path, version=((done.stdout or done.stderr).splitlines() or [''])[0].strip())
    if native:
        done = subprocess.run([out['gfortran']['path'], '-march=native', '-Q', '--help=target'], env=env,
                              capture_output=True, text=True, timeout=60)
        found = re.search(r'^\s*-march=\s+(\S+)', done.stdout, flags=re.M)
        model = next((line.split(':', 1)[1].strip() for line in Path('/proc/cpuinfo').read_text().splitlines()
                      if line.startswith('model name')), None) if Path('/proc/cpuinfo').exists() else None
        out['native'] = dict(march=found.group(1) if found else None, cpu=model)
    return out


def series_names(patches) -> list[str]:
    """The patches of the series files `patches` names, in order, each a path under models/cm1."""
    names = []
    for series in patches:
        path = MODELS / series
        if not path.is_file():
            raise DataError(f'{path}: the series file is missing')
        names += [line.strip() for line in path.read_text().splitlines() if line.strip()]
    return names


def world_macros(gravity_m_s2: float, co2: float, o2: float) -> dict:
    """The macros of a build that compiles its world in: the gravity (m/s2) and the CO2 and O2 mole fractions, each
    written as Python writes the float, so that the macro holds every digit the lab derived."""
    return dict(TERLUNA_G=repr(float(gravity_m_s2)), TERLUNA_CO2=repr(float(co2)), TERLUNA_O2=repr(float(o2)))


def gather(settings: dict, *, macros: dict, archive: Path = ARCHIVE) -> tuple[dict, dict]:
    """A build's inputs, as its key hashes them, and the bytes it is made from, for a case's resolved settings: its
    `parallel`, `optimization` and `patches`, and the macros of its world where it compiles its world in (an empty
    dict where the namelist states it)."""
    if settings.get('parallel') not in MAKEFILES:
        raise DataError(f"a CM1 build of the thin path runs with OpenMP ({tuple(MAKEFILES)}), where the case states "
                        f"{settings.get('parallel')!r}")
    if settings.get('optimization') not in OPTIMIZATIONS:
        raise DataError(f'a CM1 build compiles with one of {tuple(OPTIMIZATIONS)}, where the case states '
                        f"{settings.get('optimization')!r}")
    if list(settings.get('patches', [])) != list(SERIES):
        raise DataError(f"the thin path builds the series {list(SERIES)}, where the case's are {settings.get('patches')}: "
                        "the variants' series wait on stage 3's widening")
    if set(macros) - set(MACROS) or (macros and set(macros) != set(MACROS)):
        raise DataError(f'a build compiles all of {MACROS} or none, where it is given {sorted(macros)}')
    archive_bytes = _verified(str(archive), str(PINS))
    makefile = MAKEFILES[settings['parallel']]
    optimization = OPTIMIZATIONS[settings['optimization']]
    patches = []
    for name in (makefile, *series_names(settings['patches']), *optimization):
        path = MODELS / name
        if not path.is_file():
            raise DataError(f'{path}: a patch of the build is missing')
        patches.append((name, path.read_bytes()))
    made = dict(model='cm1', archive=dict(name=Path(archive).name, sha256=_sha256(archive_bytes)),
                makefile=makefile, series=list(settings['patches']), optimization_patches=list(optimization),
                patches=[dict(name=name, sha256=_sha256(data)) for name, data in patches],
                flags=dict(parallel=settings['parallel'], optimization=settings['optimization']),
                macros=dict(sorted(macros.items())),
                toolchain=toolchain('-march=native' in settings['optimization']))
    return made, dict(archive=archive_bytes, patches=patches, makefile=makefile, optimization=optimization)


def key(inputs: dict) -> str:
    """The build's key: the sha256 of its inputs' canonical form."""
    return _sha256(canonical(inputs).encode())


def folder(store: Path, key_: str) -> Path:
    return Path(store) / 'builds' / f'{PREFIX}-{key_[:16]}'


# The locale whose collation orders the files in the digests expected-series.sha256 records: models/check_patches.sh's
# `sort -k2` ran under en_US.UTF-8 when they were made, and the C locale's byte order gives other digests (23c57fbe...
# under C for 6dd4b11c... recorded). The lead moves the script and the digest files to the C locale in a change of its
# own; until then the build pins the locale they were made under, whatever the caller's.
DIGEST_LOCALE = 'en_US.UTF-8'


def sources_digest(src: Path) -> str:
    """The patched sources' digest as models/check_patches.sh computes it: sha256 over the lines that
    `sha256sum *.F Makefile | sort -k2` prints in src, sorted under DIGEST_LOCALE."""
    env = {k: v for k, v in common.environment().items() if not (k == 'LANG' or k.startswith('LC_'))}
    env.update(LANG=DIGEST_LOCALE, LC_ALL=DIGEST_LOCALE)
    done = subprocess.run(['bash', '-c', 'sha256sum *.F Makefile | sort -k2 | sha256sum'], cwd=src, env=env,
                          capture_output=True, text=True, timeout=120, check=True)
    return done.stdout.split()[0]


def expected_sources() -> dict:
    """The digests expected-series.sha256 records for the lab's series after the core, by label."""
    out = {}
    for line in (MODELS / 'expected-series.sha256').read_text().splitlines():
        if line.strip():
            digest, label = line.split()
            out[label] = digest
    return out


def build(settings: dict, *, store: Path, macros: dict, jobs: int = 4, archive: Path = ARCHIVE) -> Path:
    """The case's build in the store, compiled where the store lacks it, `jobs` compiles at a time at nice 10.
    Returns its folder, which holds cm1.exe, RUN_FILES and its record, build.json."""
    if not (isinstance(jobs, int) and jobs >= 1):
        raise DataError(f'a build compiles on a whole number of jobs from 1, where it is given {jobs!r}')
    made, payload = gather(settings, macros=macros, archive=archive)
    k = key(made)
    target = folder(store, k)
    if (target / 'build.json').is_file():
        return checked(target, k)
    target.parent.mkdir(parents=True, exist_ok=True)
    common._abandoned(target.parent, PREFIX)
    partial = Path(tempfile.mkdtemp(prefix=f'.{target.name}.part-', dir=target.parent))
    try:
        record = _make(made, k, payload, partial, jobs)
        (partial / 'build.json').write_text(json.dumps(record, indent=1, sort_keys=True) + '\n')
        common._read_only(partial)
        try:
            os.replace(partial, target)
        except OSError:
            if not (target / 'build.json').is_file():     # a build of the same key that lands first stands
                raise
            common._remove(partial)
            return checked(target, k)
    except BaseException:
        common._remove(partial)
        raise
    return target


def _make(made: dict, k: str, payload: dict, partial: Path, jobs: int) -> dict:
    start = time.monotonic()
    tree = partial / 'cm1r22.0'
    with tarfile.open(fileobj=io.BytesIO(payload['archive']), mode='r:gz') as tar:
        members = [m for m in tar.getmembers() if m.name.startswith(TREE + 'src/')
                   or m.name in {TREE + 'run/' + name for name in RUN_FILES}]
        tar.extractall(partial, members=members, filter='data')
    (tree / 'run').mkdir(exist_ok=True)
    src = tree / 'src'
    pristine = {p.name: _sha256(p.read_bytes()) for p in src.iterdir() if p.is_file()}
    sources = None
    for name, data in payload['patches']:
        if name in payload['optimization'] and sources is None:
            sources = sources_digest(src)
        done = subprocess.run(['patch', '-p1', '--quiet', '--no-backup-if-mismatch'], input=data, cwd=tree,
                              env=common.environment(), capture_output=True, timeout=120)
        if done.returncode:
            raise DataError(f'{name} fails to apply to the pinned sources: {(done.stdout + done.stderr).decode()}')
    if sources is None:
        sources = sources_digest(src)
    expected = expected_sources().get('lab_omp') if made['series'] == list(SERIES) else None
    if expected is not None and sources != expected:
        raise DataError(f'the patched sources give {sources}, where models/cm1/expected-series.sha256 records '
                        f'{expected} for the lab series after the core')
    command = ['nice', '-n', '10', 'make', f'-j{jobs}']
    if made['macros']:
        command.append('TERLUNA=' + ' '.join(f'-D{name}={value}' for name, value in made['macros'].items()))
    with open(partial / 'compile.log', 'wb') as log:
        process = subprocess.Popen(command, cwd=src, env=common.environment(), stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        try:
            returncode = process.wait(timeout=TIMEOUT_S)
        except BaseException:
            os.killpg(process.pid, signal.SIGKILL)               # make and the compilers with it
            process.wait()
            raise
    executable = tree / 'run' / EXECUTABLE
    if returncode or not executable.is_file():
        tail = (partial / 'compile.log').read_text(errors='replace')[-3000:]
        raise DataError(f'make stopped with {returncode} and wrote no {EXECUTABLE}:\n{tail}')
    changed = {name: _sha256((src / name).read_bytes()) for name, digest in pristine.items()
               if _sha256((src / name).read_bytes()) != digest}
    for name in (EXECUTABLE, *RUN_FILES):
        os.replace(tree / 'run' / name, partial / name)
    shutil.rmtree(tree)
    return dict(schema='worldlab.build.cm1/0', key=k, inputs=made, sources=dict(digest=sources, expected=expected,
                changed=changed), executable=dict(name=EXECUTABLE, sha256=_sha256((partial / EXECUTABLE).read_bytes())),
                run_files={name: _sha256((partial / name).read_bytes()) for name in RUN_FILES},
                compile_log_sha256=_sha256((partial / 'compile.log').read_bytes()), command=command[3:],
                seconds=round(time.monotonic() - start, 1),
                made=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))


def checked(target: Path, k: str | None = None) -> Path:
    """A build found in the store, once its record names the key and its executable and run files the record's bytes."""
    path = Path(target) / 'build.json'
    if not path.is_file():
        raise DataError(f'{target}: no build record')
    record = json.loads(path.read_text())
    if k is not None and record.get('key') != k:
        raise DataError(f'{target}: its record names key {record.get("key")}, where its inputs give {k}')
    files = {EXECUTABLE: record.get('executable', {}).get('sha256'), **record.get('run_files', {})}
    for name, digest in files.items():
        p = Path(target) / name
        if not p.is_file() or _sha256(p.read_bytes()) != digest:
            raise DataError(f'{target}: its {name} differs from its record')
    return Path(target)


def record(target: Path) -> dict:
    return json.loads((Path(target) / 'build.json').read_text())
