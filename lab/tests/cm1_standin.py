#!/usr/bin/env python3
"""A stand-in for CM1 in the job wrapper's tests (lab/tests/test_jobs.py): it reads namelist.input as CM1 does for the
settings the wrapper changes, starts afresh or from a restart, steps a state in time by a deterministic rule, and
writes CM1's kinds of file under CM1's names: the outputs (cm1out_tNNNNNN_s.dat), the domain means
(cm1out_diag_NNNNNN_s.dat with cm1out_diag_s.ctl), the statistics (cm1out_stats.dat with its control file), the
restart sets (cm1rst_tNNNNNN_{i,s,u,v,w,x}.dat) and, with lsw_coupling 1, the wave's record (lab_lsw_means.txt), then
prints CM1's normal end. As CM1 does under restart_reset_frqtim, it counts its outputs and domain means from the time it
starts at, numbering them on from the counts its restart holds, and it writes each statistics record at its record
number, also taken from the restart, so that a record past the restart's is written over. A run interrupted and
resumed thus writes the same bytes as a run without the interruption.

It checks that nudging window 1 holds its start, as the wrapper writes the windows, and stops without the normal end
where window 1 misses it. Environment: STANDIN_SLEEP (s a step), STANDIN_SIGNAL_PARENT (`<model time>:<signal>`, at
which it signals the process that started it, as a machine going down or a user stops the wrapper), STANDIN_STOP_FILE_AT
(a model time at which it writes a STOP file beside itself) and STANDIN_STOP (a stop message, printed with status 0,
as the lab's patches stop CM1).
"""
import math
import os
import re
import signal
import struct
import sys
import time
from pathlib import Path

DT = 300.0
LEVELS = 2


def value(text, name, default=None):
    m = re.search(rf'^\s*{name}\s*=\s*([^,\s]+)', text, flags=re.M | re.I)
    if m is None:
        return default
    word = m.group(1).strip("'")
    return {'.true.': 1.0, '.false.': 0.0}.get(word.lower(), None) if word.startswith('.') else float(word)


def write_ctl():
    Path('cm1out_diag_s.ctl').write_text(
        'dset ^cm1out_diag_00%y4_s.dat\noptions template\nundef -999999.9\nxdef 1 linear 0 1\nydef 1 linear 0 1\n'
        f'zdef {LEVELS} levels\n 0.05\n 0.15\ntdef 1 linear 00:00Z01JAN0001 1YR\nvars 8\n'
        'mtime 0 99 time\nprate 0 99 rain\nth 2 99 theta\nqv 2 99 vapour\nu 2 99 u\nv 2 99 v\nhpbl 0 99 pbl\n'
        'pwat 0 99 water\nendvars\n')
    Path('cm1out_stats.ctl').write_text('dset ^cm1out_stats.dat\nvars 3\nmtime 1 99 time\ndt 1 99 step\nx 1 99 state\n'
                                        'endvars\n')


def main():
    text = Path('namelist.input').read_text()
    irst, rstnum = int(value(text, 'irst')), int(value(text, 'rstnum'))
    run_time, tapfrq = value(text, 'run_time'), value(text, 'tapfrq')
    rstfrq, statfrq, diagfrq = value(text, 'rstfrq'), value(text, 'statfrq'), value(text, 'diagfrq')
    lsw = int(value(text, 'lsw_coupling', 0.0))
    at, _, name = os.environ.get('STANDIN_SIGNAL_PARENT', 'inf:SIGKILL').partition(':')
    signal_at, signum = float(at), getattr(signal, name)
    stop_at = float(os.environ.get('STANDIN_STOP_FILE_AT', 'inf'))
    pause = float(os.environ.get('STANDIN_SLEEP', '0'))
    if irst:
        t, x, nwrite, ndiag, nrec = struct.unpack('<dd3q', Path(f'cm1rst_t{rstnum:06d}_s.dat').read_bytes())
    else:
        t, x, nwrite, ndiag, nrec = 0.0, 1.0, 0, 0, 0
    window = Path('lsnudge_0001.dat').read_text().splitlines()[1].split()
    if not float(window[0]) <= t < float(window[1]):
        print(f'stand-in: window 1 spans {window}, which misses the start at {t}')
        return 0
    print(f'stand-in: starting at {t} s from window 1 of {len(list(Path(".").glob("lsnudge_*.dat")))}')
    write_ctl()
    t0 = t
    if not irst:
        for old in ('cm1out_stats.dat', 'lab_lsw_means.txt'):
            Path(old).unlink(missing_ok=True)
    counts = dict(nwrite=nwrite, ndiag=ndiag, nrec=nrec)
    if not irst:
        emit(t, t0, x, tapfrq, diagfrq, statfrq, counts)
    end = t + run_time
    while t < end - 1e-6:
        if pause:
            time.sleep(pause)
        before = t
        t += DT
        x = x + DT * 1.0e-6 * math.sin(x + t * 1.0e-5)
        emit(t, t0, x, tapfrq, diagfrq, statfrq, counts)
        if lsw and on(t - t0, diagfrq):
            with open('lab_lsw_means.txt', 'a') as f:
                f.write(f' {t - diagfrq!r} {t!r} {int(diagfrq / DT)} {1000.0 + x!r} {LEVELS}\n')
                for k in range(LEVELS):
                    f.write(' ' + ' '.join(repr(v) for v in (50.0 + 100 * k, 100.0 * (k + 1), 0.001 * x * (k + 1),
                                                                0.0, 0.0, 1e-6, 1e-9)) + '\n')
        if on(t, rstfrq):
            n = int(round(t / rstfrq))
            for part in 'isuvwx':
                data = (struct.pack('<dd3q', t, x, counts['nwrite'], counts['ndiag'], counts['nrec']) if part == 's'
                        else f'{part}{n}'.encode())
                Path(f'cm1rst_t{n:06d}_{part}.dat').write_bytes(data)
        if before < stop_at <= t:
            Path('STOP').write_text('stop\n')
        if before < signal_at <= t:
            os.kill(os.getppid(), signum)
            time.sleep(5.0)
    if os.environ.get('STANDIN_STOP'):
        print(f"Lab coupling: {os.environ['STANDIN_STOP']}")
        return 0
    print(' Program terminated normally')
    return 0


def on(t, every):
    return abs(t / every - round(t / every)) < 1e-9


def emit(t, t0, x, tapfrq, diagfrq, statfrq, counts):
    """The outputs, domain means and statistics due at t, counted from the start t0, each numbered on from its count."""
    if on(t - t0, tapfrq):
        counts['nwrite'] += 1
        Path(f'cm1out_t{counts["nwrite"]:06d}_s.dat').write_bytes(struct.pack('<dd', t, x))
    if on(t - t0, diagfrq):
        counts['ndiag'] += 1
        th = [300.0 + x + k for k in range(LEVELS)]
        qv = [0.01 * x / (k + 1) for k in range(LEVELS)]
        values = [t, 1e-5 * x] + th + qv + [1.0] * LEVELS + [0.5] * LEVELS + [800.0, 0.05]
        Path(f'cm1out_diag_{counts["ndiag"]:06d}_s.dat').write_bytes(struct.pack(f'<{len(values)}f', *values))
    if on(t - t0, statfrq):
        path = Path('cm1out_stats.dat')
        with open(path, 'r+b' if path.exists() else 'w+b') as f:      # by record number, as CM1 writes them
            f.seek(12 * counts['nrec'])
            f.write(struct.pack('<3f', t, DT, x))
        counts['nrec'] += 1


if __name__ == '__main__':
    sys.exit(main())
