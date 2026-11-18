"""Patch 12 of the lab's CM1 series: the window of CM1's large-scale nudging held by the step's time, the fix of defect
log A12, behind nudge_window_by_time of &param3, whose default 0 leaves CM1 as released. CM1 moves its count of
windows on by one window a step, and lsnudge.F sets it to the first window whenever the run reads its windows, a
restart included, so a restarted run climbs from the first window one a step until it reaches its own. With the entry
at 1 the count moves on, at any step, until the window holds the step's time, bounded by the windows read; the
restart files are untouched, so a restart file of either build serves the other.

The patch's texts put the entry in place, and the count's block at the top of solve1.F compiles on its own, stepped
through a run's times. At the default the block keeps its bits and its printout under both of the builds' flag sets.
Without the fix a restarted run climbs one window a step; with it the restarted run holds, step by step, the window,
the ramp's factor and the printout of the run it continues, a fresh run keeps CM1's count where each window spans a
step or more, the count holds the window of the step's time where windows are shorter than a step, and it stops at
the last window read. param.F's checks stop a run on the settings it cannot take.

The lab's own file: Terluna's boxes ran with CM1's count (defect log A12). A compiled box of the whole model, run in
two segments, ran once from scratch scripts (models/cm1/README.md).
"""
import re

import numpy as np
import pytest

from climate.tests.test_cm1_nudging import FLAGS, build, needs_compiler, run, values

PATCH_11 = 'patches/lab/11-the-boxs-own-large-scale-vertical-wind-by-the-weak-temperature-gradient.patch'
PATCH_12 = 'patches/lab/12-the-nudging-window-held-by-the-steps-time.patch'
FILES = ['cm1.F', 'input.F', 'lsnudge.F', 'param.F', 'solve1.F']


# The patch's texts.

def test_the_window_patch_ends_the_labs_series(cm1_series):
    """The patch follows patch 11, removes no line of CM1's or the lab's, and its added lines fit CM1's sources, hold
    nothing cpp would read and no number of a world; CM1's own advance of the count stands whole in its ELSE branch."""
    assert cm1_series.names[-1] == PATCH_12 and cm1_series.before(PATCH_12) == PATCH_11
    text = (cm1_series.folder / PATCH_12).read_text(encoding='latin-1')
    assert re.findall(r'^\+\+\+ b/src/(\S+)', text, flags=re.M) == FILES
    assert not [line for line in text.splitlines() if line.startswith('-') and not line.startswith('---')]
    added = cm1_series.added(PATCH_12)
    for line in added:
        assert len(line) <= 120, line
        for mark in ('TERLUNA_', '//', '/*', '#'):
            assert mark not in line, line
        assert 'terluna' not in line.lower().split('!')[0], line
    numbers = {n for line in added for n in re.findall(r'(?<![\w.])\d+\.\d*(?:e-?\d+)?', line.split('!')[0])}
    assert not numbers, numbers
    block = count_block(cm1_series.source('solve1.F', PATCH_12))
    before = count_block(cm1_series.source('solve1.F', PATCH_11))
    start = before.index('          if( donudge .and. timenudge')
    cms = before[start:before.index('          endif\n', start) + len('          endif\n')]
    assert block.index('          IF( nudge_window_by_time.eq.1 )THEN\n') < block.index('          ELSE\n') < \
        block.index(cms) < block.index('          ENDIF   ! Lab: nudge_window_by_time\n')


def test_the_entry_is_declared_defaulted_read_broadcast_checked_and_printed(cm1_series):
    cm1, inputs, param, solve1 = (cm1_series.source(name, PATCH_12)
                                  for name in ('cm1.F', 'input.F', 'param.F', 'solve1.F'))
    lsnudge = cm1_series.tree['lsnudge.F']                               # the series' end, patch 12 its last
    assert cm1.count('      nudge_window_by_time = 0 ') == 1
    assert cm1.index('      nudge_window_by_time = 0 ') < cm1.index("file='namelist.input'")
    assert inputs.count('      integer :: nudge_window_by_time ') == 1
    assert ('                        wind_nudge_tau,wind_nudge_zmin,inflow_ref_air, &\n'
            '                        nudge_window_by_time, &\n') in inputs
    assert param.count('      call MPI_BCAST(nudge_window_by_time,1,MPI_INTEGER,0,MPI_COMM_WORLD,ierr)') == 1
    assert param.count("      if(dowr) write(outfile,*) 'nudge_window_by_time =',nudge_window_by_time  ! Lab\n") == 1
    stops = stop_block(param)
    assert stops.count('call stopcm1') == 2 and stops.count('Lab nudging:') == 2
    assert param.index(stops) < param.index('      ! Lab: the coupled large-scale vertical wind of param3.')
    assert '  public :: lsnudge_maxcount ' in lsnudge and '      lsnudge_maxcount = lsnudge_count\n' in lsnudge
    assert '      use lsnudge_module, only : lsnudge_maxcount ' in solve1
    # The restart files keep what they kept: no file that writes or reads them changes.
    assert not {'restart_write.F', 'restart_read.F'} & set(FILES)


# The count's block at the top of solve1.F, compiled and stepped through a run's times.

def count_block(text):
    """From the step's time through the ramp of the nudging's factor."""
    start = text.index('      timenudge = mtime+dt\n')
    return text[start:text.index('      if(timestats.ge.1) time_misc=time_misc+mytime()\n', start)]


DRIVER = """
program windows
  ! The count of lsnudge's windows at the top of solve1.F, stepped on its own through a run's times; the settings and
  ! the windows' times come from standard input, and each step's count, factor and printed lines are written out.
  implicit none
  integer, parameter :: lsnudge_nmax = 100
  integer :: nsteps, step, n, myid, timestats, lsnudge_count, lsnudge_maxcount, nudge_window_by_time
  logical :: do_lsnudge, donudge
  real :: dt, timenudge, lsnudgefac, lsnudge_start, lsnudge_end, lsnudge_ramp_time, smeps, time_misc
  real :: lsnudge_time1(lsnudge_nmax), lsnudge_time2(lsnudge_nmax)
  double precision :: mtime, mtime0
  read(*,*) nsteps, n, lsnudge_count, nudge_window_by_time
  read(*,*) dt, mtime0, lsnudge_start, lsnudge_end, lsnudge_ramp_time
  lsnudge_time1 = 0.0
  lsnudge_time2 = 0.0
  read(*,*) lsnudge_time1(1:n)
  read(*,*) lsnudge_time2(1:n)
  lsnudge_maxcount = n
  do_lsnudge = .true.; myid = 0; timestats = 0; time_misc = 0.0; smeps = 1.0e-30
  do step = 1, nsteps
    mtime = mtime0 + dble(step-1)*dble(dt)
    write(*,'(a,i5)') 'STEP', step
!BLOCK
    write(*,'(a,i5,1x,z8.8,1x,l1)') 'COUNT', lsnudge_count, lsnudgefac, donudge
  enddo
  write(*,'(a)') 'VALUES'
contains
  real function mytime()
    mytime = 0.0
  end function mytime
end program windows
"""


@pytest.fixture(scope='module')
def counters(cm1_series, tmp_path_factory):
    """The count's block from the series before patch 12 and after it, under each flag set."""
    needs_compiler()
    out = {}
    for flags in FLAGS:
        for label, through in (('before', PATCH_11), ('after', PATCH_12)):
            driver = DRIVER.replace('!BLOCK', count_block(cm1_series.source('solve1.F', through)))
            out[label, flags] = build(tmp_path_factory.mktemp('windows'), driver, flags=FLAGS[flags])
    return out


def windows(n=12, length=600.0, last=1.0e30):
    """n windows of `length` seconds from the run's start, the last held to `last`, as gcm_site writes them."""
    t1 = np.arange(n) * length
    t2 = t1 + length
    t2[-1] = last
    return t1, t2


def stepped(exe, times, *, nsteps, dt=40.0, mtime0=0.0, count=1, by_time=0, start=1.0, end=1.0e12, ramp=0.0):
    """Each step's count, the factor's bits, whether it nudged and the lines it printed."""
    t1, t2 = times
    text = (f'{nsteps} {len(t1)} {count} {by_time}\n{dt!r} {mtime0!r} {start!r} {end!r} {ramp!r}\n'
            + ' '.join(repr(float(x)) for x in t1) + '\n' + ' '.join(repr(float(x)) for x in t2) + '\n')
    head = run(exe, text)[0]
    out, printed = [], []
    for line in head.splitlines():
        if line.startswith('STEP'):
            printed = []
        elif line.startswith('COUNT'):
            _, k, bits, flag = line.split()
            out.append(dict(count=int(k), factor=bits, nudged=flag == 'T', printed=printed))
        else:
            printed.append(line.strip())
    assert len(out) == nsteps
    return out


def counts(steps):
    return [s['count'] for s in steps]


RESTART = 3640.0       # a restart's time, on the steps of 40 s: an hour and 40 s, inside the seventh window of 600 s


def test_at_the_default_the_count_keeps_its_bits(counters):
    """With nudge_window_by_time at 0 the block after the patch gives the count, the factor and the printout of the
    block before it, step for step, under CM1's flags and under -O3 -march=native: a fresh run, a restarted one, windows
    shorter than a step, a ramp of the factor, and nudging that starts after the first window."""
    for flags in FLAGS:
        for times, options in ((windows(), dict(nsteps=200)),
                               (windows(), dict(nsteps=60, mtime0=RESTART)),
                               (windows(n=40, length=30.0), dict(nsteps=20, mtime0=RESTART / 4.0)),
                               (windows(), dict(nsteps=60, mtime0=RESTART, ramp=900.0)),
                               (windows(), dict(nsteps=60, start=1500.0))):
            before = stepped(counters['before', flags], times, **options)
            assert stepped(counters['after', flags], times, **options) == before, (flags, options)


def test_without_the_fix_a_restarted_run_climbs_from_the_first_window(counters):
    """A run restarted at 3,640 s, inside the seventh window, starts at the first window as CM1 reads its windows and
    climbs one window a step, printing each, until the seventh, six steps of 40 s in which the run it continues held
    the seventh; the first steps' nudging pulls toward windows the run has passed."""
    for flags in FLAGS:
        whole = stepped(counters['after', flags], windows(), nsteps=150)
        restarted = stepped(counters['after', flags], windows(), nsteps=14, mtime0=RESTART)
        same = whole[int(RESTART / 40.0):int(RESTART / 40.0) + 14]
        assert counts(same) == [7] * 14
        assert counts(restarted) == [2, 3, 4, 5, 6, 7] + [7] * 8
        assert all(len(s['printed']) == 1 and s['printed'][0].startswith('lsnudge times:') for s in restarted[:6])


def test_with_the_fix_a_restarted_run_holds_the_window_of_the_run_it_continues(counters):
    """With nudge_window_by_time at 1 the run restarted at 3,640 s moves its count from the first window to the
    seventh at its first step, printing the six windows it passes, and from there holds, step by step, the count, the
    ramp's factor and the printout of the run done whole, through the next windows; under both flag sets, with the
    factor at 1 and ramped over 900 s."""
    for flags in FLAGS:
        for ramp in (0.0, 900.0):
            exe = counters['after', flags]
            whole = stepped(exe, windows(), nsteps=210, by_time=1, ramp=ramp)
            restarted = stepped(exe, windows(), nsteps=110, mtime0=RESTART, by_time=1, ramp=ramp)
            first = int(RESTART / 40.0)
            assert counts(restarted)[0] == 7 and len(restarted[0]['printed']) == 6 + (ramp > 0.0)
            assert restarted[1:] == whole[first + 1:first + 110], (flags, ramp)
            assert [s['count'] for s in restarted] == counts(whole[first:first + 110])
            assert [s['factor'] for s in restarted] == [s['factor'] for s in whole[first:first + 110]]
            assert counts(restarted)[-1] == 12


def test_with_the_fix_a_fresh_run_keeps_cms_count_where_each_window_spans_a_step(counters):
    """From the run's start, with windows of 600 s and steps of 40 s, the fix moves the count on at the same steps as
    CM1, one window at a time, and the block returns CM1's count, factor and printout bit for bit."""
    for flags in FLAGS:
        for ramp in (0.0, 900.0):
            off = stepped(counters['after', flags], windows(), nsteps=200, ramp=ramp)
            on = stepped(counters['after', flags], windows(), nsteps=200, by_time=1, ramp=ramp)
            assert on == off and counts(on)[-1] == 12


def test_with_the_fix_the_count_holds_the_window_of_the_steps_time_and_stops_at_the_last(counters):
    """Where windows are 30 s long and steps 40 s, the fix holds at each step the window whose interval holds the
    step's time, where CM1's count falls a window behind for each step; and past the last window read, the fix holds
    the last, where CM1's count moves on to windows the run never read."""
    exe = counters['after', 'cm1']
    t1, t2 = windows(n=40, length=30.0)
    on = stepped(exe, (t1, t2), nsteps=20, mtime0=0.0, by_time=1)
    off = stepped(exe, (t1, t2), nsteps=20, mtime0=0.0)
    for step, s in enumerate(on, 1):
        time = np.float32(40.0 * step)
        assert t1[s['count'] - 1] < time <= t2[s['count'] - 1]
    assert counts(off) == list(range(2, 22))
    finite = windows(n=5, last=3000.0)
    on = stepped(exe, finite, nsteps=10, mtime0=2960.0, by_time=1)
    off = stepped(exe, finite, nsteps=10, mtime0=2960.0, count=5)
    assert counts(on) == [5] * 10 and counts(off)[-1] > 5


# The stops.

def stop_block(text):
    start = text.index('      ! Lab: nudge_window_by_time of param3')
    return text[start:text.index('      ! Lab: the coupled large-scale vertical wind of param3.', start)]


STOP_DRIVER = """
program stops
  ! The checks of param.F on nudge_window_by_time, with stopcm1 reporting the stop.
  implicit none
  integer :: myid, nudge_window_by_time, lsnudge
  logical :: do_lsnudge
  read(*,*) nudge_window_by_time, lsnudge
  do_lsnudge = lsnudge.eq.1
  myid = 0
!BLOCK
  write(*,'(a)') 'VALUES'
  write(*,'(a)') 'ran 1'
contains
  subroutine stopcm1()
    write(*,'(a)') 'VALUES'
    write(*,'(a)') 'stopped 1'
    stop
  end subroutine stopcm1
end program stops
"""


def test_the_model_stops_on_settings_it_cannot_take(cm1_series, tmp_path):
    """The model stops as it starts on an entry other than 0 and 1 and on the fix without lsnudge's windows; the
    default runs with lsnudge or without it, and the fix runs with lsnudge, as gcm_site writes every forced case."""
    needs_compiler()
    exe = build(tmp_path, STOP_DRIVER.replace('!BLOCK', stop_block(cm1_series.source('param.F', PATCH_12))),
                FLAGS['cm1'])
    for (entry, lsnudge), message in (((0, 1), None), ((0, 0), None), ((1, 1), None),
                                      ((2, 1), 'nudge_window_by_time must be 0 or 1'),
                                      ((-1, 1), 'nudge_window_by_time must be 0 or 1'),
                                      ((1, 0), 'acts on the windows of lsnudge')):
        head, found = run(exe, f'{entry} {lsnudge}\n')
        if message is None:
            assert 'ran' in found and 'Lab nudging' not in head, (entry, lsnudge)
        else:
            assert 'stopped' in found and message in head, (entry, lsnudge, head)
