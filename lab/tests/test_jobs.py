"""The job wrapper (worldlab.jobs) on a stand-in for CM1 (cm1_standin.py), which writes CM1's kinds of file under CM1's
names and counts them as CM1 does across a restart: a run in segments, its record and its resumption; a run stopped
mid-segment by SIGKILL, SIGTERM or Ctrl-C's SIGINT and resumed to the same bytes as a run without the interruption; a
restart left empty after its segment was recorded, from which the run falls back to the segment before; the lock
against a second wrapper, races included; the registry's refusal before a run; the budget's hold in place; the kept
restarts, a STOP file and the wall-clock budget; a CM1 that stops abnormally; the windows of each segment; and the
reader of a box's run (worldlab.cm1_read)."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pytest

from worldlab import cm1, cm1_read, jobs, registry, stages
from worldlab.data import DataError
from worldlab.spec import LAB, Library, SpecError

LIB = Library()
STANDIN = Path(__file__).with_name('cm1_standin.py')
SEGMENT, RESTART, OUTPUT, WINDOW, BINS = 3600.0, 1800.0, 900.0, 1000.0, 4
LENGTH = 3 * SEGMENT
TEMPLATE = """ &param1
 run_time = -999.9,
 tapfrq = 900.0,
 rstfrq = 1800.0,
 statfrq = 300.0,
 /
 &param2
 irst = 0,
 rstnum = 1,
 /
 &param3
 lsw_coupling = {lsw},
 /
 &param8
 var18 = -90.0,
 var19 = 4000.0,
 /
 &param14
 diagfrq = 900.0,
 /
"""
GENEROUS = 'jobs.budget = lambda lab=None: dict(jobs.BUDGET, load_ceiling=1.0e9, min_free_gb=1.0)\n'


def _window(i: int) -> str:
    return (' *  Header\n' + f'  {i * WINDOW:22.1f} {(i + 1) * WINDOW if i < BINS - 1 else 1e30:22.6e}\n'
            + ' * profile\n * columns\n' + f'  0.0 300.0 {10.0 + i} 1.0 0.0\n')


def context(**physics) -> dict:
    """A context the registry evaluates as it would a box of the coupling study on the Open Moon."""
    settings = json.loads(json.dumps(LIB.study('open-moon-couplings').crm['sea_imposed'].settings))
    settings['physics'].update(physics)
    q = dict(gravity_m_s2=1.6242107, scale_height_over_radius=0.0302, chapman_horizon=7.2, soil_layer_ratio=1.0,
             cm1_damping_clearance_m=20800.0, lowest_level_pressure_hpa=1214.6, cm1_build_gravity_departure=0.0)
    return dict(q=q, world=LIB.world('moon'), scenario=LIB.scenario('moon/open-moon'), settings=settings)


def make_case(folder: Path, *, lsw: int = 0, ctx: dict | None = None, overrides: dict | None = None,
              build_key: str = 'b' * 64, **run) -> Path:
    """A case's folder as cm1.write_case leaves it, for a small run of three segments."""
    texts = {'namelist.template': TEMPLATE.format(lsw=lsw), 'input_sounding': 'sounding\n'}
    texts.update({f'{cm1.WINDOWS}/lsnudge_{i + 1:04d}.dat': _window(i) for i in range(BINS)})
    ctx = ctx or context()
    header = dict(schema=cm1.SCHEMA, key=stages.key(dict(case=str(folder), lsw=lsw, ctx=ctx['settings']['physics'])),
                  registry_context=ctx, overrides=dict(overrides or {}))
    record = dict(study='probe', case=folder.name, build=dict(key=build_key), grid=dict(nx=4, ny=4, nz=2),
                  values=dict(scaled=dict(time_step_s=300.0)),
                  run=dict(dict(length_s=LENGTH, segment_s=SEGMENT, output_s=OUTPUT, diagnostics_s=OUTPUT,
                                restart_s=RESTART, stats_s=300.0, windows=dict(window_s=WINDOW, bins=BINS)), **run))
    cm1._write(folder, texts, header, record)
    return folder


@pytest.fixture
def build(tmp_path) -> Path:
    """A build's folder holding the stand-in as its executable, with its record."""
    folder = tmp_path / 'build'
    folder.mkdir()
    (folder / 'cm1.exe').write_text(f'#!{sys.executable}\n' + STANDIN.read_text().split('\n', 1)[1])
    (folder / 'cm1.exe').chmod(0o755)
    for name in ('RRTMG_LW_DATA', 'RRTMG_SW_DATA', 'LANDUSE.TBL'):
        (folder / name).write_text(name)
    stages.write_json(folder / 'build.json', dict(key='b' * 64, executable=dict(sha256=stages.sha256_file(folder / 'cm1.exe')),
                                                  run_files={n: stages.sha256_file(folder / n)
                                                             for n in ('RRTMG_LW_DATA', 'RRTMG_SW_DATA', 'LANDUSE.TBL')}))
    return folder


@pytest.fixture(autouse=True)
def generous_budget(monkeypatch):
    """A budget whose load ceiling stands above any load, so that the tests run on a busy machine; the budget's own
    test sets its limits."""
    monkeypatch.setattr(jobs, 'budget', lambda lab=LAB: dict(jobs.BUDGET, load_ceiling=1.0e9, min_free_gb=1.0))


def _run(case, store, build, **kw):
    return jobs.run_case(case, store=store, threads=1, build_folder=build, nice=0, **kw)


def _in_process(case, store, build, *, env=None, before='', timeout=120):
    """The wrapper run in a process of its own, as the command line runs it."""
    code = (f'import sys; sys.path[:0] = {[str(LAB), str(LAB.parent / "python")]!r}\n'
            'from pathlib import Path\nfrom worldlab import jobs\n' + GENEROUS + before +
            f'jobs.run_case(Path({str(case)!r}), store=Path({str(store)!r}), threads=1, '
            f'build_folder=Path({str(build)!r}), nice=0)\n')
    return subprocess.Popen([sys.executable, '-c', code], env=dict(os.environ, **(env or {})),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def _gone(run: Path) -> None:
    """Waits until the CM1 the lock file names has died."""
    info = jobs._lock_info(run)
    for _ in range(100):
        if not jobs._alive(info.get('cm1')):
            return
        time.sleep(0.1)
    raise AssertionError(f'CM1 {info.get("cm1")} outlived its wrapper')


def _outputs(run: Path) -> dict:
    """Every file the stand-in wrote, by name and bytes."""
    return {p.name: p.read_bytes() for p in sorted(run.iterdir())
            if p.name.startswith(('cm1out', 'cm1rst', 'lab_lsw')) and p.is_file()}


def test_a_case_runs_in_segments_from_its_restarts_and_resumes_where_its_record_stands(tmp_path, build):
    store = tmp_path / 'store'
    case = make_case(store / 'cases' / 'cm1-probe')
    first = _run(case, store, build, segments=1)
    run = jobs.folder(store, first['key'])
    assert first['state'] == 'paused' and [(s['start_s'], s['end_s']) for s in first['segments']] == [(0.0, SEGMENT)]
    assert (run / jobs.LOCK).exists() and not jobs.held(run) and (run / 'cm1.exe').is_symlink()
    assert first['starts'][0]['registry']['warnings'] and not first['starts'][0]['registry']['stops']
    assert first['segments'][0]['executable'] == stages.sha256_file(build / 'cm1.exe')
    # The record keeps the segment's restart set by size and hash, its outputs by size, and the statistics' length.
    kept = first['segments'][0]['kept']
    assert sorted(kept['restart']) == jobs.restart_files(2) and kept['stats_bytes'] == 13 * 12
    assert sorted(kept['outputs']) == [f'cm1out_diag_{k:06d}_s.dat' for k in range(2, 6)] + \
        [f'cm1out_t{k:06d}_s.dat' for k in range(2, 6)]
    done = _run(case, store, build)
    assert done['state'] == 'complete' and [s['end_s'] for s in done['segments']] == [SEGMENT, 2 * SEGMENT, LENGTH]
    assert cm1_read.reached_s(run) == LENGTH and jobs.status(run).endswith('complete')
    namelist = (run / 'namelist.input').read_text()
    assert 'irst = 1' in namelist and 'rstnum = 4' in namelist and 'run_time = 3600.0' in namelist
    assert sorted(n for n in jobs.restart_sets(run)) == [1, 2, 3, 4, 5, 6]
    assert _run(case, store, build)['state'] == 'complete'                  # nothing left to run


def test_each_segments_windows_start_from_the_window_that_holds_its_start(tmp_path, build):
    store = tmp_path / 'store'
    case = make_case(store / 'cases' / 'cm1-probe')
    record = _run(case, store, build)
    # Windows of 1000 s in a solar day of four: the segment from 3600 s starts in window 4 (3000-4000 s), the phase
    # of the day's fourth, and the one from 7200 s in window 8, the day's fourth again.
    assert [s['windows'] for s in record['segments']] == [
        dict(count=4, first_window=1, phase_of_first=1), dict(count=5, first_window=4, phase_of_first=4),
        dict(count=4, first_window=8, phase_of_first=4)]
    run = jobs.folder(store, record['key'])
    lines = [p.read_text().splitlines() for p in sorted(run.glob('lsnudge_*.dat'))]
    assert [float(x[1].split()[0]) for x in lines] == [7000.0, 8000.0, 9000.0, 10000.0]
    assert float(lines[-1][1].split()[1]) == 1e30 and lines[0][4] == _window(3).splitlines()[4]


@pytest.mark.parametrize('name', ['SIGKILL', 'SIGTERM', 'SIGINT'])
def test_a_run_stopped_mid_segment_resumes_to_the_bytes_of_a_run_without_the_interruption(tmp_path, build, name):
    """Killed outright, the wrapper leaves its record at the last segment and CM1 dies with it; stopped by SIGTERM or
    Ctrl-C's SIGINT, it kills CM1 and records the run as interrupted. Either way the resumed run cuts back what CM1
    wrote past its last segment, the statistics and the wave's record truncated to their recorded lengths, and ends
    with the bytes of a run without the interruption."""
    whole_store, cut_store = tmp_path / 'whole', tmp_path / 'cut'
    whole = make_case(whole_store / 'cases' / 'cm1-probe', lsw=1)
    cut = make_case(cut_store / 'cases' / 'cm1-probe', lsw=1)
    reference = _run(whole, whole_store, build)
    process = _in_process(cut, cut_store, build, env=dict(STANDIN_SIGNAL_PARENT=f'{SEGMENT + 2400.0}:{name}'))
    _, err = process.communicate(timeout=120)
    assert process.returncode == dict(SIGKILL=-9, SIGTERM=1, SIGINT=-2)[name], err
    run = jobs.folder(cut_store, cm1.checked(cut)['header']['key'])
    _gone(run)
    record = stages.read_json(run / jobs.RECORD)
    assert record['state'] == ('running' if name == 'SIGKILL' else 'interrupted')
    assert [s['end_s'] for s in record['segments']] == [SEGMENT] and not jobs.held(run)
    assert jobs.status(run).endswith('interrupted; it resumes from its last segment')
    if name != 'SIGKILL':
        assert 'Interrupted' in err and f'signal {name}' in err or 'KeyboardInterrupt' in err
    assert 3 in jobs.restart_sets(run) and (run / 'cm1out_t000007_s.dat').exists()   # written past the record
    stats = run / jobs.STATS
    inode = stats.stat().st_ino
    resumed = _run(cut, cut_store, build)
    assert resumed['state'] == 'complete' and resumed['starts'][-1]['after'] == record['state']
    cut_back = resumed['starts'][-1]['cut_back']
    assert any('cm1rst_t000003' in c for c in cut_back) and any(c.startswith(jobs.STATS) for c in cut_back)
    assert any(c.startswith(cm1_read.LSW_RECORD) for c in cut_back)
    assert stats.stat().st_ino == inode                                    # truncated in place, never rewritten
    assert _outputs(run) == _outputs(jobs.folder(whole_store, reference['key']))


def test_a_restart_left_empty_after_its_segment_was_recorded_sends_the_run_back_to_the_segment_before(tmp_path, build):
    """As after a power loss that left a recorded restart empty, the resumed run finds the last segment's restart
    differing from its record, drops that segment, cuts back to the one before and runs on to the same bytes."""
    whole_store, cut_store = tmp_path / 'whole', tmp_path / 'cut'
    reference = _run(make_case(whole_store / 'cases' / 'cm1-probe', lsw=1), whole_store, build)
    cut = make_case(cut_store / 'cases' / 'cm1-probe', lsw=1)
    record = _run(cut, cut_store, build, segments=2)
    run = jobs.folder(cut_store, record['key'])
    os.truncate(run / 'cm1rst_t000004_s.dat', 0)
    resumed = _run(cut, cut_store, build)
    start = resumed['starts'][-1]
    assert start['dropped'] == [dict(segment=2, reason='its restart file cm1rst_t000004_s.dat differs from its record')]
    assert start['from_s'] == SEGMENT and resumed['state'] == 'complete'
    assert [s['end_s'] for s in resumed['segments']] == [SEGMENT, 2 * SEGMENT, LENGTH]
    assert _outputs(run) == _outputs(jobs.folder(whole_store, reference['key']))


def test_the_cut_back_truncates_the_statistics_and_the_waves_record_to_their_recorded_lengths(tmp_path):
    run = tmp_path / 'run'
    run.mkdir()
    (run / jobs.STATS).write_bytes(bytes(range(60)))
    (run / cm1_read.LSW_RECORD).write_text('0.0 900.0 3 1000.0 1\n 50.0 100.0 0.1 0 0 0 0\n'
                                            '900.0 1800.0 3 1000.0 1\n 50.0 100.0 0.2 0 0 0 0\n')
    first = len('0.0 900.0 3 1000.0 1\n 50.0 100.0 0.1 0 0 0 0\n')
    changed = jobs.cut_back(run, 900.0, output_s=900.0, diagnostics_s=900.0, restart_s=900.0, stats_bytes=24,
                            lsw_bytes=first)
    assert (run / jobs.STATS).read_bytes() == bytes(range(24)) and len(changed) == 2
    assert (run / cm1_read.LSW_RECORD).read_text().count('\n') == 2
    # Without recorded lengths the wave's record is cut where the first interval ending past the time begins.
    (run / cm1_read.LSW_RECORD).write_text('0.0 900.0 3 1000.0 1\n 50.0 100.0 0.1 0 0 0 0\n'
                                            '900.0 1800.0 3 1000.0 1\n 50.0 100.0 0.2 0 0 0 0\n')
    jobs.cut_back(run, 900.0, output_s=900.0, diagnostics_s=900.0, restart_s=900.0, stats_bytes=24)
    assert (run / cm1_read.LSW_RECORD).stat().st_size == first


def test_a_second_wrapper_is_refused_while_the_lock_is_held_and_takes_a_dead_wrappers(tmp_path, build):
    store = tmp_path / 'store'
    case = make_case(store / 'cases' / 'cm1-probe')
    run = jobs.folder(store, cm1.checked(case)['header']['key'])
    run.mkdir(parents=True)
    fd, _ = jobs._lock(run)                                 # held by this process
    try:
        with pytest.raises(jobs.JobError, match='held by another wrapper'):
            _run(case, store, build)
    finally:
        os.close(fd)
    # A dead wrapper's lock file names it, and its lock went with it.
    (run / jobs.LOCK).write_text(json.dumps(dict(wrapper=2 ** 22 + 12345, cm1=2 ** 22 + 12346)))
    assert _run(case, store, build, segments=1)['state'] == 'paused'


def test_two_wrappers_started_together_cannot_both_hold_the_lock(tmp_path, build):
    """The first wrapper pauses for a second between taking its flock and writing the lock file's text, as a slow
    disk might, the window in which the reviewer's probe found two wrappers holding one run; the second, started in
    that window, finds the file empty and is refused all the same."""
    store = tmp_path / 'store'
    case = make_case(store / 'cases' / 'cm1-probe')
    slow = ('_write = jobs._write_lock_info\n'
            'def _slow(fd, info):\n    import time; time.sleep(1.5) if info.get("cm1") is None else None; _write(fd, info)\n'
            'jobs._write_lock_info = _slow\n')
    first = _in_process(case, store, build, before=slow, env=dict(STANDIN_SLEEP='0.02'))
    run = jobs.folder(store, cm1.checked(case)['header']['key'])
    for _ in range(100):
        if (run / jobs.LOCK).exists():
            break
        time.sleep(0.02)
    assert (run / jobs.LOCK).read_text() == ''              # taken, its text still to write
    second = _in_process(case, store, build)
    out2, err2 = second.communicate(timeout=60)
    out1, err1 = first.communicate(timeout=120)
    assert first.returncode == 0, err1
    assert second.returncode == 1 and 'held by another wrapper' in err2
    assert stages.read_json(run / jobs.RECORD)['state'] == 'complete'


def test_a_run_the_registry_stops_is_refused_unless_an_override_states_why(tmp_path, build):
    store = tmp_path / 'store'
    case = make_case(store / 'cases' / 'cm1-probe', ctx=context(pbl_per_mass=False))
    with pytest.raises(registry.Refused, match='A9 .require-switch.'):
        _run(case, store, build)
    assert not jobs.folder(store, cm1.checked(case)['header']['key']).exists()      # refused before anything ran
    record = _run(case, store, build, segments=1, overrides={'A9': 'a test of the refusal'})
    assert [o['id'] for o in record['starts'][0]['registry']['overridden']] == ['A9']
    assert record['starts'][0]['overrides'] == {'A9': 'a test of the refusal'}
    # The case's own override, recorded as it was written, lets its runs past the entry too.
    other = make_case(tmp_path / 'other' / 'cases' / 'cm1-probe', ctx=context(pbl_per_mass=False),
                      overrides={'A9': 'recorded with the case'})
    assert _run(other, tmp_path / 'other', build, segments=1)['state'] == 'paused'


def test_a_registry_changed_since_the_case_was_written_stops_its_run(tmp_path, build):
    store = tmp_path / 'store'
    case = make_case(store / 'cases' / 'cm1-probe')
    probe = dict(id='probe-entry', model='cm1', where='a test', form='constant', assumes='a probe', state='open',
                 action='refuse')

    class Probe(Library):
        def __init__(self, when):
            super().__init__()
            self.when = when

        def registry(self):
            return LIB.registry() + [dict(probe, when=self.when)]
    with pytest.raises(registry.Refused, match='probe-entry'):
        _run(case, store, build, library=Probe([{'q': 'gravity_m_s2', 'lt': 2.0}]))
    # An entry that stops runs, testing a quantity the case's context lacks, stops the run as well.
    with pytest.raises(registry.Refused, match='probe-entry .refuse, unevaluated, lacking quantity a_new_quantity'):
        _run(case, store, build, library=Probe([{'q': 'a_new_quantity', 'gt': 0.0}]))


def test_the_budget_holds_a_run_back_in_place_and_records_why(tmp_path, build, monkeypatch):
    store = tmp_path / 'store'
    case = make_case(store / 'cases' / 'cm1-probe')
    with pytest.raises(jobs.JobError, match='threads'):
        jobs.run_case(case, store=store, threads=jobs.budget()['threads'] + 1, build_folder=build)
    for limits, reason in ((dict(load_ceiling=0.5), 'the load average from other work'),
                           (dict(min_free_gb=1e9), 'GB free')):
        plan = dict(dict(jobs.BUDGET, load_ceiling=1.0e9, min_free_gb=1.0, poll_s=0.05), **limits)
        monkeypatch.setattr(jobs, 'budget', lambda lab=LAB, plan=plan: plan)
        record = _run(case, store, build, hours=0.3 / 3600.0)
        assert record['state'] == 'paused' and reason in record['held_back'][-1]['reason']
        assert record['held_back'][-1]['until'] is not None
    # The load from other work counts with the run's threads against the ceiling; between its own segments the run's
    # threads are taken out of the load average, which still holds them.
    monkeypatch.setattr(jobs.os, 'getloadavg', lambda: (10.0, 10.0, 10.0))
    plan = dict(jobs.BUDGET, load_ceiling=12.0, min_free_gb=1.0)
    assert jobs._check_budget(plan, 2, 0.0, store, 0.0)[0] is None
    assert 'exceeds' in jobs._check_budget(plan, 3, 0.0, store, 0.0)[0]
    assert jobs._check_budget(plan, 3, 3.0, store, 0.0)[0] is None


def test_kept_restarts_a_stop_file_and_the_wall_clock_bound_each_end_or_trim_a_run(tmp_path, build, monkeypatch):
    store = tmp_path / 'store'
    case = make_case(store / 'cases' / 'cm1-probe')
    record = _run(case, store, build, keep_restarts=2)
    run = jobs.folder(store, record['key'])
    assert record['state'] == 'complete' and sorted(jobs.restart_sets(run)) == [5, 6] and record['pruned'] == [1, 2, 3, 4]
    # A STOP file written during the first segment ends the run after it; one left from before a start is cleared.
    other = make_case(tmp_path / 'b' / 'cases' / 'cm1-probe')
    monkeypatch.setenv('STANDIN_STOP_FILE_AT', '1800')
    stopped = _run(other, tmp_path / 'b', build)
    run_b = jobs.folder(tmp_path / 'b', stopped['key'])
    assert stopped['state'] == 'stopped' and len(stopped['segments']) == 1 and not (run_b / jobs.STOP).exists()
    monkeypatch.delenv('STANDIN_STOP_FILE_AT')
    jobs.stop(run_b)
    again = _run(other, tmp_path / 'b', build, segments=1)
    assert again['starts'][-1]['cleared_stop'] and len(again['segments']) == 2
    # The wall-clock bound lets a segment start only where the last one's wall time still fits.
    third = make_case(tmp_path / 'c' / 'cases' / 'cm1-probe')
    monkeypatch.setenv('STANDIN_SLEEP', '0.03')
    bounded = _run(third, tmp_path / 'c', build, hours=0.6 / 3600.0)
    assert bounded['state'] == 'paused' and len(bounded['segments']) == 1


def test_a_held_input_a_wrong_build_cm1s_files_without_a_record_and_bad_intervals_each_stop_the_run(tmp_path, build,
                                                                                                     monkeypatch):
    store = tmp_path / 'store'
    case = make_case(store / 'cases' / 'cm1-probe')
    record = _run(case, store, build, segments=1)
    run = jobs.folder(store, record['key'])
    monkeypatch.setenv('STANDIN_STOP', 'a stop of the patches')
    with pytest.raises(jobs.JobError, match='stopped abnormally'):
        _run(case, store, build)
    failed = stages.read_json(run / jobs.RECORD)
    assert failed['state'] == 'failed' and failed['failed']['lab_lines'] == ['Lab coupling: a stop of the patches']
    monkeypatch.delenv('STANDIN_STOP')
    assert _run(case, store, build)['state'] == 'complete'
    (run / 'input_sounding').write_text('changed\n')
    with pytest.raises(DataError, match='differs'):
        _run(case, store, build)
    other = make_case(tmp_path / 'o' / 'cases' / 'cm1-probe', build_key='c' * 64)
    with pytest.raises(DataError, match='where the case takes c'):
        _run(other, tmp_path / 'o', build)
    leftover = make_case(tmp_path / 'l' / 'cases' / 'cm1-probe')
    folder = jobs.folder(tmp_path / 'l', cm1.checked(leftover)['header']['key'])
    folder.mkdir(parents=True)
    (folder / 'cm1out_t000001_s.dat').write_bytes(b'x')
    with pytest.raises(DataError, match="CM1's files without a record"):
        _run(leftover, tmp_path / 'l', build)
    for bad, match in ((dict(segment_s=2700.0), 'no whole number of restart'), (dict(output_s=1000.0), 'divides no'),
                       (dict(stats_s=0.0), 'positive')):
        odd = make_case(tmp_path / f'x{len(match)}' / 'cases' / 'cm1-probe', **bad)
        with pytest.raises(SpecError, match=match):
            _run(odd, tmp_path / f'x{len(match)}', build)


def test_the_reader_takes_a_runs_domain_means_by_local_time_and_the_waves_record(tmp_path, build):
    store = tmp_path / 'store'
    case = make_case(store / 'cases' / 'cm1-probe', lsw=1)
    run = jobs.folder(store, _run(case, store, build)['key'])
    means = cm1_read.domain_means(run)
    assert means['mtime'].tolist() == [900.0 * k for k in range(13)] and means['th'].shape == (13, 2)
    assert means['z_m'].tolist() == [50.0, 150.0]
    series = cm1_read.domain_mean_by_hour(run, (1.0, 2.0), bins=4)
    # Solar day 2, 4000-8000 s: outputs at 4500, 5400, 6300 and 7200 s, one in each bin of 90 degrees.
    assert len(series['hour_angle_deg']) == 4 and min(series['outputs_per_bin']) >= 1
    assert np.shape(series['theta_k']) == (4, 2) and series['z_m'] == [50.0, 150.0]
    with pytest.raises(ValueError, match='hold no output'):
        cm1_read.domain_mean_by_hour(run, (1.0, 2.0), bins=40)
    record = cm1_read.lsw_record(run)
    assert [r['end_s'] for r in record] == [900.0 * k for k in range(1, 13)] and record[0]['w_m_s'].shape == (2,)
    summary = cm1_read.summary(run, (1.0, 2.0))
    assert summary['lsw']['intervals'] == 3 and set(summary['rain_by_quarter_mm_day']) == {
        'morning', 'afternoon', 'evening', 'night'}
