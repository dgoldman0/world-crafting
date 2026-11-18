"""Patch 11 of the lab's CM1 series: the box's own large-scale vertical wind by the weak temperature gradient, as
lsw_coupling = 2 beside patch 10's damped gravity wave, with one entry of its own, lsw_stab_min, the least static
stability (K/m) by which it divides. The patch's texts put the entry and the branch in place, and the part of
solve1.F that patches 10 and 11 change compiles on its own in patch 10's driver, stepped on a domain's means without
dynamics. With the imposed wind or the wave that part keeps its bits under both of the builds' flag sets, and the
weak temperature gradient's wind is a Python copy's: w = thv'/(tau max(lsw_stab_min, dthv_r/dz)) on the w levels
between the base and the lid, the departure of the virtual potential temperature from the reference averaged from
the scalar levels on either side and the reference's own stability between them, omega linear in pressure below the
base, nil at the ground and from the lid up. The wind is nil where the box's air is its reference, rises where the
box is warm, relaxes a potential-temperature departure at 1/tau when CM1's large-scale advection carries it, and
divides by the floor where the reference's stability falls below it. param.F's stops and the block's stop on its lid
end a run on the settings the model cannot take.

The lab's own file: Terluna has no weak-temperature-gradient code. The form follows Edman and Romps (2015; eq. 3.4
of Edman's 2017 thesis, after Raymond and Zeng 2005) and Daleu et al. (2015, section 3), as models/cm1/README.md
records.
"""
import re

import numpy as np
import pytest

from climate.tests.test_cm1_coupling import (DRIVER, MOON_G, PATCH_10, RD, RECORD, RV, column_case, coupled_region,
                                             declarations, go, lid_level, pf_levels, read_record, steps, stop_block)
from climate.tests.test_cm1_nudging import FLAGS, build, needs_compiler, run, single, values

PATCH_11 = 'patches/lab/11-the-boxs-own-large-scale-vertical-wind-by-the-weak-temperature-gradient.patch'
EPS = RV / RD - 1.0
FLOOR = 1.0e-5 * MOON_G / 9.81       # Edman and Romps's 0.01 K/km at the Moon's gravity, as gcm_site writes it


# The patch's texts.

def test_the_wtg_patch_ends_the_labs_series(cm1_series):
    """The patch follows patch 10 and changes the same four files. The lines it removes are patch 10's own: comments
    that named one coupling, and the checks and messages that the second coupling joins; the wave's statements stay.
    Its added lines fit CM1's sources, hold nothing cpp would read, and no number of a world."""
    assert cm1_series.names[-1] == PATCH_11 and cm1_series.before(PATCH_11) == PATCH_10
    text = (cm1_series.folder / PATCH_11).read_text(encoding='latin-1')
    assert re.findall(r'^\+\+\+ b/src/(\S+)', text, flags=re.M) == ['cm1.F', 'input.F', 'param.F', 'solve1.F']
    removed = [line[1:] for line in text.splitlines() if line.startswith('-') and not line.startswith('---')]
    of_patch_10 = set(cm1_series.added(PATCH_10))
    assert removed and all(line in of_patch_10 for line in removed)
    assert not any('lab_lsw_om(k) =' in line or 'lab_lsw_d(k) =' in line or 'wprof(k) =' in line for line in removed)
    added = cm1_series.added(PATCH_11)
    for line in added:
        assert len(line) <= 120, line
        for mark in ('TERLUNA_', '//', '/*', '#'):
            assert mark not in line, line
        assert 'terluna' not in line.lower().split('!')[0], line
    numbers = {n for line in added for n in re.findall(r'(?<![\w.])\d+\.\d*(?:e-?\d+)?', line.split('!')[0])}
    assert numbers <= {'0.0', '0.5', '1.0', '1.5'}, numbers


def test_the_entry_is_declared_defaulted_read_broadcast_checked_and_printed(cm1_series):
    cm1, inputs, param = (cm1_series.source(name, PATCH_11) for name in ('cm1.F', 'input.F', 'param.F'))
    assert cm1.count('      lsw_stab_min = 0.0 ') == 1
    assert cm1.index('      lsw_stab_min = 0.0 ') < cm1.index("file='namelist.input'")
    assert inputs.count('      real :: lsw_stab_min ') == 1
    assert ('                        lsw_coupling,lsw_tau,lsw_mode_speed,lsw_top,lsw_base,lsw_table_heat, &\n'
            '                        lsw_stab_min, &\n'
            '                        csound,cstar,solconrce,zenanglrce\n') in inputs
    assert param.count('      call MPI_BCAST(lsw_stab_min,1,MPI_REAL,0,MPI_COMM_WORLD,ierr)') == 1
    assert param.count("      if(dowr) write(outfile,*) 'lsw_stab_min =',lsw_stab_min  ! Lab\n") == 1
    stops = stop_block(param)
    assert stops.count('call stopcm1') == 10 and stops.count('Lab coupling:') == 10


def test_the_branch_follows_the_wave_and_sets_omega_before_the_wind_is_written(cm1_series):
    """In solve1.F the branch stands inside the coupled wind's block, after the departure and the wave's branch and
    before the wind is written into wprof, which patch 09's inflow then reads; it reads the reference's stability and
    the floor, and the record and the table's cut serve it unchanged."""
    region = coupled_region(cm1_series.source('solve1.F', PATCH_11))
    departure = region.index('          lab_lsw_tv(k) = 0.0\n')
    wave = region.index('        IF( lsw_coupling.eq.1 )THEN\n')
    branch = region.index('        IF( lsw_coupling.eq.2 )THEN\n')
    wind = region.index('          wprof(k) = -lab_lsw_om(k)/( rf0(1,1,k)*g )\n')
    inflow = region.index('      IF( inflow_ref_air.eq.1 .and. dolsw )THEN\n')
    assert departure < wave < branch < wind < inflow
    part = region[branch:wind]
    assert 'max( lsw_stab_min , lab_lsw_dr/(zh(1,1,k)-zh(1,1,k-1)) )' in part
    assert '( lab_lsw_pf(1)-lab_lsw_pf(k) )' in part and 'lsw_mode_speed' not in part
    assert "'  Lab: the weak temperature gradient; its lid (k, z) = '" in region


# The coupled part of solve1.F, compiled and stepped on a domain's means.

@pytest.fixture(scope='module')
def wtg_couplers(cm1_series, tmp_path_factory):
    """The coupled part of solve1.F from the series before patch 11 and after it, in patch 10's driver, under each
    flag set."""
    needs_compiler()
    out = {}
    for flags in FLAGS:
        for label, through in (('before', PATCH_10), ('after', PATCH_11)):
            text = cm1_series.source('solve1.F', through)
            driver = DRIVER.replace('!REGION', coupled_region(text)).replace('!DECLARE', declarations(text))
            out[label, flags] = build(tmp_path_factory.mktemp('wtg'), driver, flags=FLAGS[flags])
    return out


def test_with_the_imposed_wind_or_the_wave_the_coupled_part_keeps_its_bits(wtg_couplers):
    """With lsw_coupling 0 or 1 and every entry as before, the part after the patch returns every tendency, stepped
    mean and wind of the part before it, prints the same lines and writes the same record, byte for byte, under CM1's
    flags and under -O3 -march=native: the imposed wind with the inflow and the table on and off, one step and twenty,
    the wind's nudging off and the large-scale wind off; and the wave alone, with the inflow, the table's cut and the
    record over twenty steps, and with its base at the lid."""
    wave = dict(coupling=1, tau=10800.0, speed=40.0, top=20000.0, base=300.0, hpbl=1500.0)
    for flags in FLAGS:
        for seed in range(3):
            case = column_case(top=30000.0, dz0=300.0, seed=seed)
            case['thavg'] = case['th_ref'] + np.random.default_rng(seed).normal(0.0, 0.5, case['nk'])
            for options in (dict(), dict(nsteps=20, pattern=0), dict(inflow=1), dict(var11=1.0),
                            dict(nsteps=20, pattern=0, inflow=1, var11=1.0, writes=[1] * 20, timax=400.0),
                            dict(switches=(1, 0, 0, 1, 1, 1, 1), inflow=1), dict(switches=(1, 1, 1, 1, 1, 1, 0)),
                            wave, dict(wave, inflow=1),
                            dict(wave, inflow=1, var11=1.0, heat=1, nsteps=20, pattern=0, writes=[0, 0, 0, 1] * 5,
                                 timax=800.0),
                            dict(wave, hpbl=50000.0, inflow=1, var11=1.0)):
                exe_b, exe_a = wtg_couplers['before', flags], wtg_couplers['after', flags]
                for exe in (exe_b, exe_a):
                    (exe.parent / RECORD).unlink(missing_ok=True)
                head_b, before = go(exe_b, case, **options)
                head_a, after = go(exe_a, case, **options)
                assert after == before and head_a == head_b, (flags, seed, options)
                rec_b, rec_a = exe_b.parent / RECORD, exe_a.parent / RECORD
                assert rec_a.exists() == rec_b.exists() == ('writes' in options and 'coupling' in options)
                if rec_a.exists():
                    assert rec_a.read_bytes() == rec_b.read_bytes()


# The weak temperature gradient's wind against a Python copy.

def theta_case(case, th):
    """The case with the domain's mean theta raised by th (K) over the reference's, its vapour the reference's."""
    return dict(case, thavg=single(case['th_ref']) + th)


def wtg_wind(case, *, tau, top, stab, base=0.0, hpbl=0.0):
    """The wind (m/s) on the w levels, in double precision from CM1's single-precision means and reference: on the w
    levels from the first above the base, max(base, min(hpbl, top)), to the last below the lid's w level, thv' averaged
    from the scalar levels on either side over tau times the reference's stability between them, floored at stab;
    below, omega falls linearly in the block's pressure to nil at the ground. Also the base's and the lid's levels."""
    zh, zf, rho, g = (single(case[k]) for k in ('zh', 'zf', 'rf0', 'g'))
    th, q, tr, qr = (single(case[k]) for k in ('thavg', 'qavg', 'th_ref', 'qv_ref'))
    pf, lid = pf_levels(case), lid_level(case, top)
    zb = max(np.float32(base), min(np.float32(hpbl), np.float32(top)))
    kb = next((k for k in range(1, lid) if zf[k] > zb), lid)
    dep = (th - tr) * (1.0 + EPS * q) + EPS * tr * (q - qr)
    omega = np.zeros(zf.size)
    for k in range(kb, lid):
        dr = (tr[k] - tr[k - 1]) * (1.0 + EPS * qr[k]) + EPS * tr[k - 1] * (qr[k] - qr[k - 1])
        omega[k] = -rho[k] * g * 0.5 * (dep[k - 1] + dep[k]) / (tau * max(stab, dr / (zh[k] - zh[k - 1])))
    for k in range(1, kb):
        omega[k] = omega[kb] * (pf[0] - pf[k]) / (pf[0] - pf[kb])
    return -omega / (rho * g), kb, lid


def test_the_wind_is_the_departure_over_tau_and_the_references_stability(wtg_couplers):
    """With a departure of theta and of vapour through the column, the block's wind is the Python copy's to 1 part in
    10^5 of its largest value under both flag sets, with the base at the boundary layer's 3 km and at its 400 m floor:
    nil at the ground and from the lid's w level up, bit for bit, and below the base omega linear in the block's
    pressure to 2 parts in 10^4, the rounding of single precision at the lowest levels. The model prints the
    coupling and its lid as the branch first runs."""
    case = column_case()
    zh = case['zh']
    th = 0.4 * np.sin(np.pi * np.clip(zh / 45000.0, 0.0, 1.0)) + 0.05 * np.cos(zh / 2000.0)
    warm = theta_case(case, th)
    warm['qavg'] = single(case['qv_ref']) * (1.0 + 0.1 * np.cos(zh / 3000.0))
    rho_g = single(case['rf0']) * single(case['g'])
    pf = pf_levels(case)
    for flags in FLAGS:
        for hpbl in (3000.0, 100.0):
            settings = dict(tau=10303.0, top=45000.0, stab=FLOOR, base=400.0, hpbl=hpbl)
            head, found = go(wtg_couplers['after', flags], warm, coupling=2, **settings)
            w = values(found['wprof'])
            expected, kb, lid = wtg_wind(warm, **settings)
            assert np.abs(w - expected).max() <= 1e-5 * np.abs(expected).max(), (flags, hpbl)
            assert w[0] == 0.0 and np.all(w[lid:] == 0.0) and np.all(w[kb:lid] != 0.0)
            omega = -w * rho_g
            slope = omega[1:kb + 1] / (pf[0] - pf[1:kb + 1])
            assert kb >= 3 and np.abs(slope / slope[-1] - 1.0).max() < 2e-4, slope
            assert 'Lab: the weak temperature gradient; its lid (k, z) =' in head
            assert 'damped gravity wave' not in head


def test_a_reference_equal_to_the_boxs_mean_gives_no_wind(wtg_couplers):
    """The box's mean air at its reference leaves the wind nil at every level, bit for bit under both flag sets, from
    any imposed wind it held before: the departure (th - th_r)(1 + eps q) + eps th_r (q - q_r) is nil wherever the two
    airs agree, fused products or none. A departure of 0.1 K makes a wind of millimetres a second."""
    case = column_case()
    for flags in FLAGS:
        for hpbl in (0.0, 3000.0):
            found = go(wtg_couplers['after', flags], case, coupling=2, tau=10303.0, top=45000.0, stab=FLOOR,
                       hpbl=hpbl, inflow=1)[1]
            assert np.all(values(found['wprof']) == 0.0), flags
    found = go(wtg_couplers['after', 'native'], theta_case(case, 0.1 * (case['zh'] < 45000.0)), coupling=2,
               tau=10303.0, top=45000.0, stab=FLOOR)[1]
    assert np.abs(values(found['wprof'])).max() > 1e-3 and np.abs(case['wprof']).max() > 1e-3


def test_a_warm_departure_rises_and_a_cool_one_sinks(wtg_couplers):
    """Above the base a warm departure lifts the air at every w level up to the lid and a cool one sinks it, by
    opposite winds equal to the rounding of the box's theta; below the base the taper keeps the sign."""
    case = column_case()
    for flags in FLAGS:
        winds = {}
        for sign in (1.0, -1.0):
            found = go(wtg_couplers['after', flags], theta_case(case, sign * 0.2 * (case['zh'] < 45000.0)),
                       coupling=2, tau=10303.0, top=45000.0, stab=FLOOR, hpbl=2000.0)[1]
            winds[sign] = values(found['wprof'])
        lid = lid_level(case, 45000.0)
        assert np.all(winds[1.0][1:lid] > 0.0) and np.all(winds[-1.0][1:lid] < 0.0)
        assert winds[1.0] == pytest.approx(-winds[-1.0], rel=1e-3)


def advection(case, w, own):
    """CM1's large-scale vertical advection of a domain-mean scalar by the wind w on the w levels, in the form of
    patch 09's and 10's tests (the flux form less the scalar times the mass convergence, wsub): the tendency at the
    scalar levels."""
    rf0, rho = single(case['rf0']), 1.0 / single(case['rr0'])
    dz = 1.0 / (single(case['rdz']) * single(case['mh']))
    face = np.r_[0.0, 0.5 * (own[1:] + own[:-1]), 0.0]
    div = (rf0[1:] * w[1:] - rf0[:-1] * w[:-1]) / dz
    return (-(rf0 * w * face)[1:] + (rf0 * w * face)[:-1]) / dz / rho + own * div / rho


def test_a_departure_relaxes_at_one_over_tau_under_its_own_winds_advection(wtg_couplers):
    """A departure of theta, a half sine of 0.2 K between the base and the lid, stepped forward by CM1's large-scale
    advection of theta by the block's wind alone, the vapour held at the reference's, falls to e^-1 of itself in tau
    within 5% at its peak and through the column, on a lunar column (base 3 km, lid 60 km) and an Earth column (base
    1 km, lid 15 km), under both flag sets: the wind's advection of the reference's own stability returns the departure
    on tau. Fifty forward steps of tau/50; their own error, 1.3% for e^-1, lies within the bound."""
    for gravity, n_bv, top, lid_m, base in ((MOON_G, 0.002, 80000.0, 60000.0, 3000.0),
                                            (9.81, 0.011, 24000.0, 15000.0, 1000.0)):
        case = column_case(gravity=gravity, n_bv=n_bv, top=top)
        zh = case['zh']
        inside = (zh > base) & (zh < lid_m)
        start = np.where(inside, 0.2 * np.sin(np.pi * (zh - base) / (lid_m - base)), 0.0)
        peak = int(np.argmax(start))
        tau, n = 7200.0, 50
        for flags in FLAGS:
            box = theta_case(case, start)
            for _ in range(n):
                w = values(go(wtg_couplers['after', flags], box, coupling=2, tau=tau, top=lid_m, stab=FLOOR,
                              hpbl=base)[1]['wprof'])
                th = single(box['thavg'])
                box = dict(box, thavg=th + (tau / n) * advection(case, w, th))
            left = single(box['thavg']) - single(case['th_ref'])
            assert -np.log(left[peak] / start[peak]) == pytest.approx(1.0, rel=0.05), (gravity, flags)
            assert np.abs(left[inside]).max() / start.max() == pytest.approx(np.exp(-1.0), rel=0.05)


def test_the_floor_divides_where_the_references_stability_falls_below_it(wtg_couplers):
    """A reference with a layer of uniform theta, its vapour falling through it so that its virtual stability is
    negative there: the block divides by lsw_stab_min in that layer and by the reference's stability elsewhere, as
    the Python copy does, to 1 part in 10^5; a floor ten times higher multiplies the wind in that layer by a tenth and
    leaves every other level's bit for bit; and a floor above every level's stability makes the wind the departure
    over tau times the floor throughout."""
    case = column_case()
    zh = case['zh']
    neutral = (zh > 12000.0) & (zh < 16000.0)
    th_ref = np.array(case['th_ref'], float)
    th_ref[neutral] = th_ref[np.argmax(neutral) - 1]
    warm = theta_case(dict(case, th_ref=th_ref), 0.2 * (zh < 45000.0))
    lid = lid_level(case, 45000.0)
    thv_ref = single(th_ref) * (1.0 + EPS * single(case['qv_ref']))
    stability = np.r_[np.nan, np.diff(thv_ref) / np.diff(single(zh)), np.nan]          # on the w levels
    floored = np.zeros(stability.size, bool)
    floored[1:lid] = stability[1:lid] < 1e-6
    assert floored.sum() >= 3 and np.all(stability[1:lid][~floored[1:lid]] > 1e-5)
    for flags in FLAGS:
        winds = {}
        for stab in (1e-6, 1e-5, 1.0):
            settings = dict(tau=10303.0, top=45000.0, stab=stab, hpbl=2000.0)
            w = values(go(wtg_couplers['after', flags], warm, coupling=2, **settings)[1]['wprof'])
            expected, kb, _ = wtg_wind(warm, **settings)
            assert np.abs(w - expected).max() <= 1e-5 * np.abs(expected).max(), (flags, stab)
            winds[stab] = w
        assert np.array_equal(winds[1e-6][~floored], winds[1e-5][~floored])
        assert winds[1e-6][floored] / winds[1e-5][floored] == pytest.approx(10.0, rel=1e-5)
        k = np.arange(kb, lid)
        dep = (single(warm['thavg']) - single(th_ref)) * (1.0 + EPS * single(case['qv_ref']))
        assert winds[1.0][k] == pytest.approx(0.5 * (dep[k - 1] + dep[k]) / 10303.0, rel=1e-5)


def test_with_the_inflow_the_record_holds_every_interval_and_the_column_keeps_its_air(wtg_couplers):
    """Under the weak temperature gradient patch 10's record holds its three intervals of 3, 4 and 3 steps, each the
    mean of the wind over its steps, and patch 09's inflow reads the branch's wind: nil at the ground and the lid, it
    draws in as much air as it sends out, the inflow nil where the wind diverges."""
    case = column_case(top=30000.0, dz0=300.0)
    zh = case['zh']
    warm = theta_case(case, 0.3 * np.sin(np.pi * np.clip(zh / 20000.0, 0.0, 1.0)) * (zh < 20000.0))
    warm['qavg'] = single(case['qv_ref']) * 0.95
    exe = wtg_couplers['after', 'cm1']
    (exe.parent / RECORD).unlink(missing_ok=True)
    head, found = go(exe, warm, coupling=2, tau=10303.0, top=20000.0, stab=FLOOR, base=300.0, hpbl=2000.0,
                     inflow=1, nsteps=10, pattern=0, show=1, mtime0=3600.0, timax=4000.0,
                     writes=[0, 0, 1, 0, 0, 0, 1, 0, 0, 0])
    rows = read_record(exe.parent / RECORD)
    assert [(r['start'], r['end'], r['steps']) for r in rows] == [(3600.0, 3720.0, 3.0), (3720.0, 3880.0, 4.0),
                                                                 (3880.0, 4000.0, 3.0)]
    w = steps(head, 'W', 10)
    for row, part in zip(rows, (slice(0, 3), slice(3, 7), slice(7, 10))):
        assert row['table'][:, 2] == pytest.approx(w[part, :-1].mean(axis=0), rel=1e-5, abs=1e-12)
        assert row['base'] == pytest.approx(2000.0)
    last = values(found['wprof'])
    rf0 = single(case['rf0'])
    dz = 1.0 / (single(case['rdz']) * single(case['mh']))
    div = (rf0[1:] * last[1:] - rf0[:-1] * last[:-1]) / dz
    assert last[0] == 0.0 and last[-1] == 0.0 and np.abs(div).max() > 0.0
    assert abs((div * dz).sum()) < 1e-6 * np.abs(div * dz).sum()
    inflow = values(found['qten']).reshape(case['nk'], case['nj'] + 1, case['ni'] + 1)[:, 0, 0]
    assert np.all(inflow[div < -1e-4 * np.abs(div).max()] == 0.0)


# The stops.

STOP_DRIVER = """
program stops
  ! The checks of param.F on patch 10's six entries and patch 11's, with stopcm1 reporting the stop.
  implicit none
  integer :: myid, lsw_coupling, lsw_table_heat, imoist, testcase, switches(4)
  logical :: do_lsnudge, do_lsnudge_th, do_lsnudge_qv
  real :: lsw_tau, lsw_mode_speed, lsw_top, lsw_base, lsw_stab_min, dtl, var11, var13
  read(*,*) lsw_coupling, lsw_tau, lsw_mode_speed, lsw_top, lsw_base, lsw_table_heat, lsw_stab_min
  read(*,*) dtl, var11, var13, testcase, imoist
  read(*,*) switches
  do_lsnudge = switches(1).eq.1; do_lsnudge_th = switches(2).eq.1; do_lsnudge_qv = switches(3).eq.1
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
    """The model stops as it starts on a coupling other than 0, 1 and 2; on lsw_stab_min set with the imposed wind or
    the wave; on a weak temperature gradient whose time falls below the step, whose floor is nil or less, whose base
    lies below the ground or at the lid, or any of them NaN, or with a mode speed stated; and, as for the wave, on a
    table's rule other than 0 and 1 or without the table, and without lsnudge's theta and vapour, moisture or one
    profile of large-scale vertical wind. The boxes as gcm_site writes them run under either coupling, as do the
    defaults, a gradient without the table's cut and a gradient in test case 5; the wave's own stops stand."""
    needs_compiler()
    block = stop_block(cm1_series.source('param.F', PATCH_11))
    exe = build(tmp_path, STOP_DRIVER.replace('!BLOCK', block[block.index('      IF( lsw_coupling.ne.0'):]),
                FLAGS['cm1'])
    nan = float('nan')
    box = dict(c=2, tau=10303.0, speed=0.0, top=73084.5, base=316.1, heat=1, stab=1.65e-6, dtl=40.0, var11=1.0,
               var13=1.0, testcase=0, imoist=1, on=(1, 1, 1, 1))
    wave = dict(c=1, speed=40.534, stab=0.0)
    zero = dict(c=0, tau=0.0, speed=0.0, top=0.0, base=0.0, heat=0, stab=0.0)
    cases = [(dict(), None), (wave, None), (zero, None), (dict(heat=0), None),
             (dict(var13=0.0, testcase=5, var11=0.0, heat=0), None), (dict(tau=40.0, base=0.0), None),
             (dict(c=3), 'must be 0 (imposed), 1 (the wave) or 2 (the WTG)'), (dict(c=-1), 'lsw_coupling must be 0'),
             (dict(zero, stab=1e-6), 'act with lsw_coupling 1 or 2'), (dict(zero, stab=nan), 'act with lsw_coupling 1'),
             (dict(zero, tau=10303.0), 'act with lsw_coupling 1 or 2'),
             (dict(wave, stab=1e-6), 'lsw_stab_min acts with lsw_coupling 2'),
             (dict(wave, stab=nan), 'lsw_stab_min acts with lsw_coupling 2'),
             (dict(wave, tau=20.0), 'lsw_mode_speed > 0'), (dict(wave, speed=0.0), 'lsw_mode_speed > 0'),
             (dict(tau=20.0), 'lsw_stab_min > 0'), (dict(tau=nan), 'lsw_stab_min > 0'),
             (dict(stab=0.0), 'lsw_stab_min > 0'), (dict(stab=-1e-6), 'lsw_stab_min > 0'),
             (dict(stab=nan), 'lsw_stab_min > 0'), (dict(base=-1.0), 'lsw_stab_min > 0'),
             (dict(base=73084.5), 'lsw_stab_min > 0'), (dict(top=nan), 'lsw_stab_min > 0'),
             (dict(speed=40.534), 'lsw_mode_speed acts with lsw_coupling 1'),
             (dict(speed=nan), 'lsw_mode_speed acts with lsw_coupling 1'),
             (dict(heat=2), 'lsw_table_heat must be 0 or 1'), (dict(var11=0.0), 'acts on the table of var11 = 1'),
             (dict(on=(0, 1, 1, 1)), 'the coupling reads the theta and vapour'),
             (dict(on=(1, 0, 1, 1)), 'theta and vapour'), (dict(on=(1, 1, 0, 1)), 'theta and vapour'),
             (dict(imoist=0), 'theta and vapour'), (dict(wave, on=(1, 1, 0, 1)), 'theta and vapour'),
             (dict(var13=0.0), 'the coupling sets one profile of large-scale vertical wind'),
             (dict(var13=2.0), 'one profile of large-scale vertical wind'),
             (dict(wave, var13=0.0), 'one profile of large-scale vertical wind')]
    for change, message in cases:
        s = dict(box, **change)
        text = (f"{s['c']} {s['tau']!r} {s['speed']!r} {s['top']!r} {s['base']!r} {s['heat']} {s['stab']!r}\n"
                f"{s['dtl']!r} {s['var11']!r} {s['var13']!r} {s['testcase']} {s['imoist']}\n"
                + ' '.join(str(x) for x in s['on']) + '\n')
        head, found = run(exe, text.replace('nan', 'NaN'))
        if message is None:
            assert 'ran' in found and 'Lab coupling' not in head, change
        else:
            assert 'stopped' in found and message in head, (change, head)


def test_the_gradient_stops_on_a_lid_below_its_first_level_and_takes_the_top_for_a_lid_above_it(wtg_couplers):
    """As for the wave, a lid at or below the first w level above the ground stops the block as it first runs, and a
    lid above the box's top takes the top. A base between the last two w levels below the lid leaves the gradient the
    last alone, tapered below; a base at or above the lid leaves no w level between them, and the wind is nil."""
    case = column_case()
    head, found = go(wtg_couplers['after', 'cm1'], case, coupling=2, tau=10303.0, top=float(case['zf'][1]),
                     stab=FLOOR)
    assert 'stopped' in found and 'lsw_top lies at or below the first w level' in head
    warm = theta_case(case, 0.3 * np.ones(case['nk']))
    head, found = go(wtg_couplers['after', 'cm1'], warm, coupling=2, tau=10303.0, top=1e7, stab=FLOOR)
    assert re.search(r'weak temperature gradient; its lid \(k, z\) =\s+%d\s' % (case['nk'] + 1), head)
    w = values(found['wprof'])
    assert w[-1] == 0.0 and np.all(w[1:-1] > 0.0)
    lid, zf = lid_level(case, 45000.0), single(case['zf'])
    settings = dict(tau=10303.0, top=45000.0, stab=FLOOR, base=0.5 * (zf[lid - 2] + zf[lid - 1]))
    w = values(go(wtg_couplers['after', 'cm1'], warm, coupling=2, **settings)[1]['wprof'])
    expected, kb, _ = wtg_wind(warm, **settings)
    assert kb == lid - 1 and w[lid - 1] > 0.0 and np.abs(w - expected).max() <= 1e-5 * np.abs(expected).max()
    found = go(wtg_couplers['after', 'cm1'], warm, coupling=2, tau=10303.0, top=45000.0, stab=FLOOR, hpbl=50000.0)[1]
    assert np.all(values(found['wprof']) == 0.0)
