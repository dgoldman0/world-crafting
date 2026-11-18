"""Jobs: one CM1 case run in segments under the lab's own bookkeeping, the thin path of plan stage 7
(lab/design/architecture.md, "Jobs and the machine"; plan.md, stage 7).

    from worldlab import jobs
    record = jobs.run_case(case_folder, store=store, threads=4)      # runs/cm1-<the case's key>/run.json

The run of a case lives in runs/cm1-<the case's key's first 16 hex digits>/, beside the case's own folder: the case's
input files copied in, the build's executable and run files linked from the build's read-only folder, and run.json,
the run's record. Before it starts, the wrapper

- checks the build's executable and the case's files against their records, a hash that differs stopping the run;
- evaluates the registry anew on the case's context, with the case's overrides and the run's own, and refuses a run
  that an entry stops (registry.Refused);
- holds the run to its threads within the budget's;
- takes the run's lock, an exclusive flock on run.lock that the wrapper keeps open and hands CM1 with each segment, so
  that the kernel holds it until both have exited and a second wrapper refuses meanwhile; the file names the two
  processes for the reader alone.

Before each segment it holds the run back in place, with the reason recorded, while the load average from other work
and the run's threads together exceed the budget's ceiling, or the free disk less the run's estimated need falls
below the budget's minimum; a STOP file or the wall-clock budget ends the wait.

It then runs CM1 in segments of the case's segment_s, each from the restart the last finished segment wrote, at nice
10 with the thread variables set and an unlimited stack, until the case's length, a STOP file in the run's folder, the
wall-clock budget or the segments asked for ends it. Before each segment it writes the segment's nudging windows from
the case's solar day of windows, numbered from the window that holds the segment's start, so that CM1's count of its
windows, which a restart sets back to the first (defect log A12), holds the segment's own window from its first step;
and it writes namelist.input from the case's template with the restart, its number and the segment's length. A
segment is recorded, by its start, end, wall time, log, the executable's hash, the windows it read and the values CM1
printed as it read them, only once CM1 ends normally and its restart at the segment's end is complete; CM1 ends the
patches' stops with status 0, so the log's last lines decide. The segment's restart set and outputs, the statistics
and the wave's record are then written through to the disk (fsync), and the record keeps the restart set's sizes and
hashes, the outputs' sizes and the byte lengths of the statistics and the wave's record.

Resuming. A run interrupted mid-segment, its wrapper stopped by a signal or Ctrl-C (recorded as interrupted) or the
machine down, resumes from its last recorded segment whose restart set and outputs verify against the record, falling
back past any that fail, as a restart left empty by a power loss would: the files CM1 wrote past that time (outputs,
domain diagnostics and restart sets) are removed, and the statistics and the wave's record truncated to the lengths
recorded with that segment, so that the resumed run writes them as a run without the interruption would. A run whose
CM1 stops abnormally keeps its folder and record, the failed segment's log named in it.
"""
from __future__ import annotations

import ctypes
import fcntl
import json
import os
import re
import resource
import shutil
import signal
import subprocess
import threading
import time
import tomllib
from pathlib import Path

import numpy as np

from . import cm1, cm1_builds, cm1_read, registry, stages
from .data import DataError
from .spec import LAB, Library, SpecError

SCHEMA = 'worldlab.run.cm1/0'
RECORD, LOCK, STOP = 'run.json', 'run.lock', 'STOP'
NORMAL_END = 'Program terminated normally'      # CM1's last line, which Terluna's run loop tests for too
RESTART_PARTS = ('i', 's', 'u', 'v', 'w', 'x')     # restart_filetype 2: one file of each part for each restart
OUTPUT = re.compile(r'^cm1out_t(\d{6})_\w+\.dat$')
DIAG = re.compile(r'^cm1out_diag_(\d{6})_\w+\.dat$')
RESTART = re.compile(r'^cm1rst_t(\d{6})_\w+\.dat$')
STATS, STATS_CTL = 'cm1out_stats.dat', 'cm1out_stats.ctl'
# What CM1 prints of the values it read: its echo of every namelist entry, one `name = value` a line, and the lines
# of the lab's patches and RRTMG that state the values in force (`Lab ...`; `cp,grv =`), which the first segment's
# record keeps, and a failed segment's the last of.
ENTRY_LINE = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\S+)\s*$', re.M)
LAB_LINES = re.compile(r'^\s*(Lab\b.*|.*\bcp,grv\s*=.*)$', re.M)
# The machine's budget where lab/local.toml's [budget] leaves a value out: half the cores' threads, nice 10, 20 GB of
# free disk kept, a load average with the run's own threads at most the core count, and a minute between looks at the
# load while a run is held back (architecture.md, "Jobs and the machine").
BUDGET = dict(threads=max(1, (os.cpu_count() or 2) // 2), nice=10, min_free_gb=20.0, load_ceiling=float(os.cpu_count() or 1),
              poll_s=60.0)
# The wall time and disk a box takes, from Terluna's sea box (32 x 32 columns, 111 levels, a 40 s step, 4 threads):
# 59 lunar-day-equivalent days in 2.0 hours (lab/design/gap_series.md, its table; Terluna's climate/crm/README.md),
# 20.76 MB of output every 3 hours, 16.4 MB a restart set and 92 kB of domain means at each output
# (crm-runs/box_near_side_sea_dgw on Terluna's research drive).
REFERENCE = dict(cells=32 * 32 * 111, step_s=40.0, model_s=59.0 * 86400.0, wall_s=2.0 * 3600.0, threads=4,
                 output_bytes_per_cell=20758528 / (32 * 32 * 111), restart_bytes_per_cell=16360528 / (32 * 32 * 111),
                 diag_bytes_per_level=92316 / 111)


class JobError(RuntimeError):
    """A run the wrapper stops: a budget exceeded, a lock held, a CM1 that ended abnormally."""


class Interrupted(JobError):
    """A run stopped by a signal to its wrapper, SIGTERM or Ctrl-C's SIGINT, which kills CM1 and records the run as
    interrupted."""


def budget(lab: Path = LAB) -> dict:
    """The machine's budget: lab/local.toml's [budget] over BUDGET."""
    out = dict(BUDGET)
    local = lab / 'local.toml'
    if local.exists():
        try:
            out.update(tomllib.loads(local.read_text()).get('budget', {}))
        except tomllib.TOMLDecodeError as error:
            raise SpecError(f'{local}: {error}') from None
    return out


def estimate(case: dict, *, keep_restarts: int = 0) -> dict:
    """A written case's wall time and disk (`estimate_for`)."""
    rec = case['record']
    g, r = rec['grid'], rec['run']
    return estimate_for(g['nx'], g['ny'], g['nz'], rec['values']['scaled']['time_step_s'], r['length_s'],
                        r['output_s'], r['restart_s'], diagnostics_s=r['diagnostics_s'], keep_restarts=keep_restarts)


def estimate_for(nx: int, ny: int, nz: int, step_s: float, length_s: float, output_s: float, restart_s: float, *,
                 diagnostics_s: float | None = None, keep_restarts: int = 0) -> dict:
    """A box's wall time (s, on the reference's 4 threads) and disk (bytes), from Terluna's sea box scaled by its
    columns, levels, steps, length, outputs and the restarts kept (0: every one)."""
    cells = nx * ny * nz
    wall = REFERENCE['wall_s'] * (cells / REFERENCE['cells']) * (length_s / REFERENCE['model_s']) \
        * (REFERENCE['step_s'] / step_s)
    outputs = int(length_s // output_s) + 1
    restarts = int(length_s // restart_s)
    kept = restarts if keep_restarts <= 0 else min(restarts, keep_restarts)
    disk = cells * (outputs * REFERENCE['output_bytes_per_cell'] + kept * REFERENCE['restart_bytes_per_cell']) \
        + (int(length_s // (diagnostics_s or output_s)) + 1) * nz * REFERENCE['diag_bytes_per_level']
    return dict(wall_s_on_4_threads=wall, four_thread_hours=wall / 3600.0, disk_bytes=disk, outputs=outputs,
                restarts=restarts, restarts_kept=kept,
                basis="Terluna's sea box: 59 lunar-day-equivalent days of 32 x 32 x 111 columns in 2.0 h on 4 threads, "
                      'scaled by columns, levels, steps and length; its output, restarts and domain means by size')


def folder(store: Path, case_key: str) -> Path:
    return Path(store) / 'runs' / f'cm1-{case_key[:16]}'


def _alive(pid) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _lock(run: Path) -> tuple[int, dict]:
    """The run's lock: an exclusive flock on run.lock, taken without waiting, its descriptor returned open. The kernel
    releases it when every process holding the descriptor has exited, the wrapper and the CM1 it hands it to, so that
    neither an empty lock file nor a dead wrapper's leaves a gap for a second wrapper. The file's text names the
    processes for a reader and decides nothing."""
    fd = os.open(Path(run) / LOCK, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        held = _lock_info(run)
        os.close(fd)
        raise JobError(f'{run}: its run is held by another wrapper ({held or "its lock file names none yet"})') from None
    info = dict(wrapper=os.getpid(), cm1=None, taken=stages.now())
    _write_lock_info(fd, info)
    return fd, info


def _write_lock_info(fd: int, info: dict) -> None:
    os.ftruncate(fd, 0)
    os.pwrite(fd, json.dumps(info).encode(), 0)


def _lock_info(run: Path) -> dict:
    try:
        return json.loads((Path(run) / LOCK).read_text() or '{}')
    except (OSError, ValueError):
        return {}


def held(run: Path) -> bool:
    """Whether a wrapper or its CM1 named in the run's lock file lives: the status's reading, which the lock itself
    leaves to the kernel."""
    info = _lock_info(run)
    return _alive(info.get('wrapper')) or _alive(info.get('cm1'))


def _child_setup(parent: int):
    """What CM1's process does before it runs: an unlimited stack, as CM1's arrays on the stack need, and death with the
    wrapper (PR_SET_PDEATHSIG), so that an interrupted wrapper leaves no CM1 writing into the run; and, since the
    wrapper may die between the fork and the prctl, an exit where its parent is already another process."""
    def setup():
        resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
        try:
            ctypes.CDLL('libc.so.6', use_errno=True).prctl(1, signal.SIGKILL)
        except OSError:
            pass
        if os.getppid() != parent:
            os._exit(70)
    return setup


def _on_signal(signum, frame):
    raise Interrupted(f'the wrapper took signal {signal.Signals(signum).name}')


def segment_windows(case_folder: Path, run: Path, start_s: float, end_s: float, window_s: float) -> dict:
    """The nudging windows of one segment, written into the run's folder from the case's solar day of windows: those
    from the window holding start_s to the last starting before end_s, numbered from 1 as CM1 reads them, each with
    its own times and the profile of the case's window at the same phase of the day, the last open-ended (Terluna's
    restart_windows, climate/crm/cm1_run.py at 39c5ee04)."""
    day = sorted((Path(case_folder) / cm1.WINDOWS).glob('lsnudge_*.dat'))
    if not day:
        raise DataError(f'{case_folder}: the case holds no windows')
    rows = [p.read_text().splitlines() for p in day]
    bins = len(rows)
    for old in run.glob('lsnudge_*.dat'):
        old.unlink()
    first = int(np.floor(start_s / window_s + 1e-9))
    last = max(first, int(np.ceil(end_s / window_s - 1e-9)) - 1)
    if last - first + 1 > 100:
        raise DataError(f'{last - first + 1} nudging windows in one segment; CM1 reads at most 100')
    for k, i in enumerate(range(first, last + 1), 1):
        t1, t2 = i * window_s, (1.0e30 if i == last else (i + 1) * window_s)
        r = rows[i % bins]
        (run / f'lsnudge_{k:04d}.dat').write_text('\n'.join(r[:1] + [f'  {t1:22.1f} {t2:22.6e}'] + r[2:]) + '\n')
    return dict(count=last - first + 1, first_window=first + 1, phase_of_first=first % bins + 1)


def restart_sets(run: Path) -> dict[int, list[Path]]:
    found = {}
    for p in run.iterdir():
        m = RESTART.match(p.name)
        if m:
            found.setdefault(int(m.group(1)), []).append(p)
    return found


def complete_restart(run: Path, n: int) -> bool:
    names = {p.name for p in restart_sets(run).get(n, [])}
    return all(f'cm1rst_t{n:06d}_{part}.dat' in names for part in RESTART_PARTS)


def restart_files(n: int) -> list[str]:
    return [f'cm1rst_t{n:06d}_{part}.dat' for part in RESTART_PARTS]


def _fsync(paths, folder: Path) -> None:
    """The files and their folder written through to the disk."""
    for path in paths:
        fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    fd = os.open(folder, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def written(run: Path, start_s: float, end_s: float, u: dict) -> dict:
    """What a segment from start_s to end_s wrote that its record keeps: the restart set at end_s, by size and sha256;
    the outputs and domain means past start_s, by size; and the byte lengths of the statistics and the wave's record."""
    n = int(round(end_s / u['restart_s']))
    restart = {name: dict(bytes=(run / name).stat().st_size, sha256=stages.sha256_file(run / name))
               for name in restart_files(n)}
    outputs = {}
    for p in sorted(run.iterdir()):
        for pattern, every in ((OUTPUT, u['output_s']), (DIAG, u['diagnostics_s'])):
            m = pattern.match(p.name)
            if m and start_s < (int(m.group(1)) - 1) * every <= end_s + 1e-6:
                outputs[p.name] = p.stat().st_size
    size = lambda name: (run / name).stat().st_size if (run / name).exists() else 0
    return dict(restart=restart, outputs=outputs, stats_bytes=size(STATS), lsw_bytes=size(cm1_read.LSW_RECORD))


def verify(run: Path, segment: dict, restart_s: float) -> str | None:
    """Why a recorded segment's files fail their record, or None: its restart set's sizes and hashes, its outputs'
    sizes, and statistics and a wave's record at least as long as it left them."""
    kept = segment.get('kept')
    if kept is None:                                       # a segment recorded before the record kept its files
        n = int(round(segment['end_s'] / restart_s))
        return None if complete_restart(run, n) else f'its restart set {n} is incomplete'
    for name, want in kept['restart'].items():
        path = run / name
        if not path.is_file() or path.stat().st_size != want['bytes'] or stages.sha256_file(path) != want['sha256']:
            return f'its restart file {name} differs from its record'
    for name, size in kept['outputs'].items():
        if not (run / name).is_file() or (run / name).stat().st_size != size:
            return f'its output {name} differs from its record'
    for name, size in ((STATS, kept['stats_bytes']), (cm1_read.LSW_RECORD, kept['lsw_bytes'])):
        if size and (not (run / name).is_file() or (run / name).stat().st_size < size):
            return f'its {name} is shorter than its record'
    return None


def cut_back(run: Path, done_s: float, *, output_s: float, diagnostics_s: float, restart_s: float,
             stats_bytes: int | None = None, lsw_bytes: int | None = None) -> list[str]:
    """The files CM1 wrote past `done_s` removed or cut back, before a run resumes from its restart at done_s: outputs
    and domain diagnostics after it and restart sets after it removed, and the statistics and the wave's record
    truncated in place (os.truncate) to the lengths recorded with the segment that ends at done_s, or, for a record
    without them, to the prefix of records and intervals that end by done_s. Returns what changed."""
    changed = []
    last_output = int(np.floor(done_s / output_s + 1e-9)) + 1         # output k holds time (k - 1) output_s
    last_diag = int(np.floor(done_s / diagnostics_s + 1e-9)) + 1     # and domain means k (k - 1) diagnostics_s
    last_restart = int(round(done_s / restart_s))                    # restart n holds time n restart_s
    for p in sorted(run.iterdir()):
        for pattern, last in ((OUTPUT, last_output), (DIAG, last_diag), (RESTART, last_restart)):
            m = pattern.match(p.name)
            if m and int(m.group(1)) > last:
                p.unlink()
                changed.append(p.name)
    stats, ctl = run / STATS, run / STATS_CTL
    if stats.exists():
        if stats_bytes is None:
            stats_bytes = 0
            if ctl.exists():
                count = int(re.search(r'^vars\s+(\d+)', ctl.read_text(), flags=re.M).group(1))
                times = np.fromfile(stats, dtype='<f4')
                times = times[:times.size // count * count].reshape(-1, count)[:, 0]
                beyond = np.flatnonzero(times > done_s + 1e-3)
                stats_bytes = 4 * count * int(beyond[0] if beyond.size else times.size)
        if stats.stat().st_size > stats_bytes:
            changed.append(f'{STATS}: {stats.stat().st_size} bytes to {stats_bytes}')
            os.truncate(stats, stats_bytes)
    lsw = run / cm1_read.LSW_RECORD
    if lsw.exists():
        if lsw_bytes is None:
            lsw_bytes = cm1_read.lsw_cut(lsw.read_bytes().decode('ascii'), done_s)
        if lsw.stat().st_size > lsw_bytes:
            changed.append(f'{cm1_read.LSW_RECORD}: {lsw.stat().st_size} bytes to {lsw_bytes}')
            os.truncate(lsw, lsw_bytes)
    return changed


def prune(run: Path, keep: int, done_s: float, restart_s: float) -> list[int]:
    """Restart sets beyond the newest `keep` removed (0 keeps every one), the set at done_s always kept."""
    if keep <= 0:
        return []
    numbers = sorted(n for n in restart_sets(run) if complete_restart(run, n))
    newest = set(numbers[-keep:]) | {int(round(done_s / restart_s))}
    removed = [n for n in numbers if n not in newest]
    for n in removed:
        for p in restart_sets(run)[n]:
            p.unlink()
    return removed


def _prepare(case_folder: Path, run: Path, build: Path) -> dict:
    """A run's folder made from its case and build: the case's files copied, the build's executable and run files
    linked."""
    run.mkdir(parents=True, exist_ok=True)
    copied = {}
    for p in sorted(Path(case_folder).iterdir()):
        if p.is_file() and p.name != 'case.json':
            target = run / p.name
            shutil.copyfile(p, target)
            target.chmod(0o644)
            copied[p.name] = stages.sha256_file(target)
    for name in (cm1_builds.EXECUTABLE, *cm1_builds.RUN_FILES):
        link = run / name
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(Path(build) / name)
    return copied


def namelist_for(template: str, *, start_s: float, run_s: float, restart_s: float) -> str:
    """The namelist of one segment: from the restart at start_s, if any, for run_s seconds."""
    n = int(round(start_s / restart_s))
    if start_s > 0 and abs(n * restart_s - start_s) > 1e-6:
        raise DataError(f'a segment starts at {start_s} s, which no restart of every {restart_s} s holds')
    return cm1.set_entries(template, dict(param2=dict(irst=1 if start_s > 0 else 0, rstnum=max(n, 1)),
                                          param1=dict(run_time=float(run_s))))


def _check_budget(plan: dict, threads: int, own_load: float, store: Path, need_bytes: float) -> tuple[str | None, dict]:
    """Why the budget holds the run back now, or None, with what was read: the load average less the run's own
    threads where its last segment has just run, plus the threads it asks, against the ceiling; and the free disk
    less the run's remaining need against the minimum kept."""
    load = os.getloadavg()[0]
    others = max(0.0, load - own_load)
    free = shutil.disk_usage(store).free
    seen = dict(load=load, others=others, threads=threads, free_bytes=free, need_bytes=need_bytes)
    if others + threads > plan['load_ceiling']:
        return (f"the load average from other work, {others:.1f}, with the run's {threads} threads exceeds the budget's "
                f"ceiling of {plan['load_ceiling']}"), seen
    if free - need_bytes < plan['min_free_gb'] * 1e9:
        return (f"the store's disk holds {free / 1e9:.1f} GB free; the run needs about {need_bytes / 1e9:.1f} GB more "
                f"and the budget keeps {plan['min_free_gb']} GB"), seen
    return None, seen


def run_case(case_folder: Path, *, store: Path, threads: int = 4, segments: int | None = None,
             hours: float | None = None, overrides: dict | None = None, keep_restarts: int = 0,
             build_folder: Path | None = None, library: Library | None = None, lab: Path = LAB,
             nice: int | None = None) -> dict:
    """Run the case in its folder of the store, in segments, from where its record stands; returns the run's record.
    `segments` and `hours` bound this call; `overrides` ({entry: justification}) let the run past registry entries
    that stop it; `keep_restarts` keeps the newest restart sets (0: all)."""
    library = library or Library()
    case_folder = Path(case_folder)
    case = cm1.checked(case_folder)
    k = case['header']['key']
    rec = case['record']
    u = rec['run']
    where = f"{rec['study']}:{rec['case']}"
    cm1.check_intervals(u, where)
    build = Path(build_folder) if build_folder is not None else cm1_builds.folder(store, rec['build']['key'])
    build_record = cm1_builds.record(cm1_builds.checked(build))
    if build_record['key'] != rec['build']['key']:
        raise DataError(f"{build}: holds build {build_record['key']}, where the case takes {rec['build']['key']}")
    checks = registry.require(cm1.recheck(case, entries=library.registry(), overrides=overrides), where)
    plan = budget(lab)
    if not (isinstance(threads, int) and 1 <= threads <= plan['threads']):
        raise JobError(f"a run takes from 1 to the budget's {plan['threads']} threads, where it asks {threads!r}")
    run = folder(store, k)
    run.mkdir(parents=True, exist_ok=True)
    fd, lock = _lock(run)
    main = threading.current_thread() is threading.main_thread()
    previous = signal.signal(signal.SIGTERM, _on_signal) if main else None
    record = None
    path = run / RECORD
    try:
        record = stages.read_json(path) if path.exists() else None
        if record is None:
            leftover = sorted(p.name for p in run.iterdir() if OUTPUT.match(p.name) or DIAG.match(p.name)
                              or RESTART.match(p.name) or p.name in (STATS, cm1_read.LSW_RECORD))
            if leftover:
                raise DataError(f'{run}: holds CM1\'s files without a record ({leftover[:3]} and {len(leftover) - 3} '
                                'more); a new run starts in an empty folder, so remove them, or the folder')
            copied = _prepare(case_folder, run, build)
            record = stages.header(SCHEMA, k, producer_=dict(build=build_record['key'],
                                                             executable=build_record['executable']['sha256'],
                                                             wrapper=stages.producer([Path(__file__)])),
                                   inputs=dict(case=k, files=copied), read_set=dict(threads=threads),
                                   evidence='a run of a CM1 case under the lab\'s wrapper; its output is the model\'s, '
                                            'read as evidence only by the analyses that state their rules',
                                   study=rec['study'], case=rec['case'], case_folder=str(case_folder),
                                   build_folder=str(build), length_s=u['length_s'], segments=[], starts=[],
                                   state='ready')
        elif record['key'] != k:
            raise DataError(f"{run}: its record names case {record['key']}, where the case's key is {k}")
        else:
            for name, digest in record['inputs']['files'].items():
                if stages.sha256_file(run / name) != digest:
                    raise DataError(f'{run}: its {name} differs from the case\'s, as recorded')
            _prepare_links(run, build)
        start_entry = dict(at=stages.now(), threads=threads, registry=checks, overrides=dict(overrides or {}),
                           budget=plan, after=record['state'])
        if (run / STOP).exists():                          # no wrapper holds the run, so a STOP file is stale
            (run / STOP).unlink()
            start_entry['cleared_stop'] = True
        dropped = []
        while record['segments']:
            failed = verify(run, record['segments'][-1], u['restart_s'])
            if failed is None:
                break
            dropped.append(dict(segment=record['segments'][-1]['segment'], reason=failed))
            record['segments'].pop()
        if dropped and not record['segments'] and record.get('pruned'):
            raise JobError(f'{run}: no recorded segment\'s restart verifies ({dropped}), and earlier restarts were '
                           'pruned; the run starts again only from an empty folder')
        last = record['segments'][-1] if record['segments'] else None
        done = float(last['end_s']) if last else 0.0
        kept = (last or {}).get('kept') or {}
        cut = cut_back(run, done, output_s=u['output_s'], diagnostics_s=u['diagnostics_s'], restart_s=u['restart_s'],
                       stats_bytes=kept.get('stats_bytes', 0 if last is None else None),
                       lsw_bytes=kept.get('lsw_bytes', 0 if last is None else None)) \
            if record['state'] != 'ready' or dropped else []
        start_entry.update(from_s=done, cut_back=cut, dropped=dropped)
        record['starts'].append(start_entry)
        record['state'] = 'running'
        stages.write_json(path, record)
        env = dict(os.environ, OMP_NUM_THREADS=str(threads), OPENBLAS_NUM_THREADS='1', NUMBA_NUM_THREADS=str(threads),
                   OMP_STACKSIZE='512M')
        template = (run / 'namelist.template').read_text()
        deadline = None if hours is None else time.time() + hours * 3600.0
        need = estimate(case, keep_restarts=keep_restarts)
        ran = 0
        while True:
            done = float(record['segments'][-1]['end_s']) if record['segments'] else 0.0
            if done >= u['length_s'] - 1e-6:
                record['state'] = 'complete'
                break
            if segments is not None and ran >= segments:
                record['state'] = 'paused'
                break
            last_wall = record['segments'][-1]['wall_s'] if record['segments'] else 0.0
            reason, seen = None, None
            while True:                                    # the budget holds the run back in place
                if (run / STOP).exists():
                    break
                if deadline is not None and time.time() + last_wall > deadline:
                    break
                remaining = need['disk_bytes'] * max(0.0, 1.0 - done / u['length_s'])
                reason, seen = _check_budget(plan, threads, threads if ran else 0.0, store, remaining)
                if reason is None:
                    break
                held_back = record.setdefault('held_back', [])
                if not held_back or held_back[-1].get('until') is not None:
                    held_back.append(dict(since=stages.now(), at_s=done, reason=reason, seen=seen, until=None))
                    record['state'] = 'held back'
                    stages.write_json(path, record)
                time.sleep(plan['poll_s'])
            if record.get('held_back') and record['held_back'][-1].get('until') is None:
                record['held_back'][-1]['until'] = stages.now()
                record['state'] = 'running'
            if (run / STOP).exists():
                (run / STOP).unlink()
                record['state'] = 'stopped'
                break
            if deadline is not None and time.time() + last_wall > deadline:
                record['state'] = 'paused'
                break
            run_s = min(u['segment_s'], u['length_s'] - done)
            end = done + run_s
            if done > 0 and not complete_restart(run, int(round(done / u['restart_s']))):
                raise DataError(f'{run}: the restart at {done} s, from which the run resumes, is incomplete')
            windows = segment_windows(case_folder, run, done, end, u['windows']['window_s'])
            (run / 'namelist.input').write_text(namelist_for(template, start_s=done, run_s=run_s,
                                                             restart_s=u['restart_s']))
            log = run / f'cm1_segment_{len(record["segments"]) + 1:03d}.log'
            start = time.time()
            with open(log, 'w') as out:
                process = subprocess.Popen(['nice', '-n', str(plan['nice'] if nice is None else nice),
                                            f'./{cm1_builds.EXECUTABLE}'], cwd=run, env=env, stdout=out,
                                           stderr=subprocess.STDOUT, preexec_fn=_child_setup(os.getpid()),
                                           start_new_session=True, pass_fds=(fd,))
                lock['cm1'] = process.pid
                _write_lock_info(fd, lock)
                try:
                    returncode = process.wait()
                except BaseException:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                    record['state'] = 'interrupted'
                    raise
                finally:
                    lock['cm1'] = None
                    _write_lock_info(fd, lock)
            text = log.read_text(errors='replace')
            if returncode != 0 or NORMAL_END not in text[-4000:]:
                record['state'] = 'failed'
                record['failed'] = dict(segment=len(record['segments']) + 1, log=log.name, returncode=returncode,
                                        lab_lines=[m.group(1).strip() for m in LAB_LINES.finditer(text)][-20:])
                raise JobError(f'CM1 stopped abnormally in {run}; see {log.name}')
            n = int(round(end / u['restart_s']))
            if abs(n * u['restart_s'] - end) > 1e-6 or not complete_restart(run, n):
                record['state'] = 'failed'
                raise JobError(f'{run}: CM1 wrote no complete restart at {end} s')
            kept = written(run, done, end, u)
            _fsync([run / name for name in (*kept['restart'], *kept['outputs'], STATS, cm1_read.LSW_RECORD)
                    if (run / name).exists()], run)
            record['segments'].append(dict(
                segment=len(record['segments']) + 1, start_s=done, end_s=end, wall_s=round(time.time() - start, 1),
                log=log.name, finished=stages.now(), threads=threads,
                executable=stages.sha256_file(run / cm1_builds.EXECUTABLE), windows=windows, kept=kept,
                read=read_values(text) if not record['segments'] else None))
            record['pruned'] = record.get('pruned', []) + prune(run, keep_restarts, end, u['restart_s'])
            stages.write_json(path, record)
            ran += 1
    except BaseException:
        if record is not None and record.get('state') in ('running', 'held back'):
            record['state'] = 'interrupted'
        raise
    finally:
        if record is not None:
            stages.write_json(path, record)
        if main:
            signal.signal(signal.SIGTERM, previous)
        os.ftruncate(fd, 0)                                # the file names no process once the lock is let go
        os.close(fd)
    return record


def read_values(text: str) -> dict:
    """What a segment's log says CM1 read: its echo of the namelist's entries, by name, and the lab's and RRTMG's
    lines of the values in force."""
    values = {}
    for m in ENTRY_LINE.finditer(text):
        values.setdefault(m.group(1), m.group(2))
    return dict(values=values, lines=[m.group(1).strip() for m in LAB_LINES.finditer(text)])


def _prepare_links(run: Path, build: Path) -> None:
    for name in (cm1_builds.EXECUTABLE, *cm1_builds.RUN_FILES):
        link = run / name
        if not (link.is_symlink() and os.readlink(link) == str(Path(build) / name)):
            if link.is_symlink() or link.exists():
                link.unlink()
            link.symlink_to(Path(build) / name)


def status(run: Path) -> str:
    """One line on a run: its model time, its share of the case, its wall time and state."""
    path = Path(run) / RECORD
    if not path.exists():
        return f'{run}: no run yet'
    record = stages.read_json(path)
    done = float(record['segments'][-1]['end_s']) if record['segments'] else 0.0
    wall = sum(s['wall_s'] for s in record['segments'])
    running = held(run)
    state = record['state'] if running else ('interrupted; it resumes from its last segment'
                                             if record['state'] in ('running', 'held back', 'interrupted')
                                             else record['state'])
    return (f"{record['study']}:{record['case']}: {done / 86400.0:.2f} of {record['length_s'] / 86400.0:.2f} days "
            f"({100.0 * done / record['length_s']:.0f}%), {len(record['segments'])} segments, {wall / 3600.0:.2f} wall "
            f"hours; {state}")


def stop(run: Path) -> Path:
    """A STOP file in the run's folder: the wrapper stops after the segment under way."""
    path = Path(run) / STOP
    path.write_text('stop after the segment under way\n')
    return path
