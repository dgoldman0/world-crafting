"""Patch 09 of the lab's CM1 series: the wind's own nudging time, its pull from a height up, and the inflow of the
nudging reference's air where the large-scale vertical wind converges, read from &param3 with defaults under which
CM1's nudging stands as before. The patch's texts put the three entries in place, and the parts of the patched model
that compile on their own, the large-scale nudging of solve1.F and the relaxation of the base-state and geostrophic
wind in solve3.F, stepped together on a domain's means without dynamics, keep their bits at the defaults under both
of the builds' flag sets, relax the wind on its own time from the given height up, and draw the reference's theta and
vapour in at the rate max(d(rho0 w)/dz, 0)/rho0, which Terluna's own check reckons independently within 2%, here on the
vertical wind that climate/crm/gcm_site.py writes. The stops of param.F, compiled alone, end a run on the settings the
model cannot take.

The lab's own file. The patch comes from three of Terluna's edit lists, WIND_TAU_PATCH, WIND_ALOFT_PATCH and
INFLOW_PATCH (climate/crm/cm1_run.py at 39c5ee04), whose tests read the lists' text and stay in Terluna; a compiled
box case of the whole model ran once from scratch scripts (models/cm1/README.md).
"""
import math
import os
import re
import shutil
import struct
import subprocess

import numpy as np
import pytest

from climate.crm import gcm_site as gs

PATCH_08 = 'patches/lab/08-the-suns-declination-from-the-namelist.patch'
PATCH_09 = 'patches/lab/09-the-winds-own-nudging-and-the-inflow-of-the-reference.patch'
CPP = ('cpp', '-C', '-P', '-traditional', '-Wno-invalid-pp-token', '-ffreestanding', '-DOPENMP')
# gfortran's flags in the two makefiles of the builds: CM1's own for OpenMP, and Terluna's optimisation of them, the
# lab's default, under which gfortran fuses products into multiply-adds on a processor that has them.
COMMON = ('-ffree-form', '-ffree-line-length-none', '-finline-functions', '--param=max-vartrack-size=0', '-fopenmp')
FLAGS = dict(cm1=('-O2', *COMMON), native=('-O3', '-march=native', *COMMON))
ENTRIES = ('wind_nudge_tau', 'wind_nudge_zmin', 'inflow_ref_air')
RATES = gs.INFLOW_RATES_FILE


def needs_compiler():
    if shutil.which('gfortran') is None or shutil.which('cpp') is None:
        pytest.skip('gfortran or cpp is missing')


def build(folder, driver, flags):
    """An executable from a driver that holds CM1's lines, preprocessed as the model's makefile preprocesses them."""
    (folder / 'driver.F').write_text(driver, encoding='latin-1')
    done = subprocess.run([*CPP, 'driver.F'], cwd=folder, check=True, capture_output=True, encoding='latin-1')
    (folder / 'driver.f90').write_text(done.stdout, encoding='latin-1')
    subprocess.run(['gfortran', *flags, 'driver.f90', '-o', 'run'], cwd=folder, check=True, capture_output=True)
    return folder / 'run'


def run(exe, text):
    """What an executable prints for an input: the lines before its mark, and each named row's words after it."""
    done = subprocess.run([str(exe)], input=text, capture_output=True, text=True, cwd=exe.parent,
                          env={**os.environ, 'OMP_NUM_THREADS': '1'})
    if done.returncode or 'VALUES\n' not in done.stdout:
        raise RuntimeError(done.stdout[-600:] + done.stderr[-600:])
    head, _, body = done.stdout.partition('VALUES\n')
    return head, {line.split()[0]: line.split()[1:] for line in body.splitlines()}


def values(words):
    return np.array([struct.unpack('>f', bytes.fromhex(word))[0] for word in words])


def single(x):
    """The single-precision numbers nearest x, which CM1 holds."""
    return np.asarray(x, float).astype(np.float32).astype(float)


# The patch's texts.

def test_the_nudging_patch_ends_the_labs_series(cm1_series):
    assert cm1_series.names[-1] == PATCH_09 and cm1_series.before(PATCH_09) == PATCH_08
    text = (cm1_series.folder / PATCH_09).read_text(encoding='latin-1')
    assert re.findall(r'^\+\+\+ b/src/(\S+)', text, flags=re.M) == ['cm1.F', 'input.F', 'param.F', 'solve1.F',
                                                                 'solve3.F']
    added = cm1_series.added(PATCH_09)
    for line in added:
        assert len(line) <= 120, line
        for mark in ('TERLUNA_', '//', '/*', '#'):                      # cpp would read these
            assert mark not in line, line
    # Nothing of a world is compiled in: the patch's lines name the lab, and no number in them is a world's.
    assert not any('terluna' in line.lower() for line in added)
    numbers = {n for line in added for n in re.findall(r'(?<![\w.])\d+\.\d*(?:e-?\d+)?', line.split('!')[0])}
    assert numbers <= {'0.0', '0.5', '1.5'}, numbers


def test_each_entry_is_declared_defaulted_read_broadcast_checked_and_printed(cm1_series):
    cm1, inputs, param = (cm1_series.source(name, PATCH_09) for name in ('cm1.F', 'input.F', 'param.F'))
    for default in ('      wind_nudge_tau = 0.0 ', '      wind_nudge_zmin = 0.0 ', '      inflow_ref_air = 0 '):
        assert cm1.count(default) == 1, default
    assert cm1.index('      inflow_ref_air = 0 ') < cm1.index("file='namelist.input'")   # the defaults, then reading
    for declared in ('      real :: wind_nudge_tau ', '      real :: wind_nudge_zmin ',
                     '      integer :: inflow_ref_air '):
        assert inputs.count(declared) == 1, declared
    assert ('                        world_g,world_co2,world_o2,soil_dz1,sun_decl, &\n'
            '                        wind_nudge_tau,wind_nudge_zmin,inflow_ref_air, &\n'
            '                        csound,cstar,solconrce,zenanglrce\n') in inputs
    for name, kind in zip(ENTRIES, ('MPI_REAL', 'MPI_REAL', 'MPI_INTEGER')):
        assert param.count(f'      call MPI_BCAST({name},1,{kind},0,MPI_COMM_WORLD,ierr)') == 1, name
        assert param.count(f"      if(dowr) write(outfile,*) '{name} =',{name}  ! Lab\n") == 1, name
    # The stops stand with the lab's others, ahead of the constants.
    stops = stop_block(param)
    assert param.index(stops) < param.index('      call set_constants( testcase , world_g )\n')
    assert stops.count('call stopcm1') == 5 and stops.count('Lab nudging:') == 5


def test_the_wind_keeps_its_statements_but_its_time_and_height_and_the_inflow_follows_the_vapours_nudging(cm1_series):
    """In solve1.F the wind's two tendencies take lab_tau_uv where they took lsnudge_tau and are set to nil below
    wind_nudge_zmin; theta and vapour keep lsnudge_tau; the inflow stands inside the large-scale nudging, after the
    vapour's, and adds the rate times the reference less the domain's mean to each column. In solve3.F the base-state
    and geostrophic wind relax on lab_tau_uv, at every level. The patch replaces the four lines that divided the wind's
    relaxation by lsnudge_tau and adds the rest, so every other line of the five files stays as it was."""
    text = (cm1_series.folder / PATCH_09).read_text(encoding='latin-1')
    removed = [line[1:] for line in text.splitlines() if line.startswith('-') and not line.startswith('---')]
    assert removed == ['          tem1 = -lsnudgefac*( (umove+uavg(k))-lsnudge_u(k,lsnudge_count) )/(lsnudge_tau)',
                       '          tem2 = -lsnudgefac*( (vmove+vavg(k))-lsnudge_v(k,lsnudge_count) )/(lsnudge_tau)',
                       '        tem = lsnudgefac*dt/lsnudge_tau', '        tem = lsnudgefac*dt/lsnudge_tau']
    solve1 = cm1_series.source('solve1.F', PATCH_09)
    block = nudge_block(solve1)
    assert block.count('/(lab_tau_uv)') == 2 and block.count('/(lsnudge_tau)') == 2          # wind; theta and vapour
    assert block.count('if( zh(1,1,k).lt.wind_nudge_zmin ) tem1 = 0.0') == 1
    assert block.count('if( zh(1,1,k).lt.wind_nudge_zmin ) tem2 = 0.0') == 1
    assert block.index('lab_tau_uv = lsnudge_tau') < block.index('if( donudge .and. do_lsnudge_u )then')
    inflow = block[block.index('      IF( inflow_ref_air.eq.1 .and. dolsw )THEN'):]
    assert block.index('qdiag(i,j,k,qd_nudge) = tem1') < block.index(inflow)
    assert 'tem = max( 0.0 , (rf0(1,1,k+1)*wprof(k+1)-rf0(1,1,k)*wprof(k))*rdz*mh(1,1,k) )*rr0(1,1,k)' in inflow
    # wsub's own convergence, the same expression adv_routines.F forms
    assert 'div = (rf0(1,1,k+1)*wprof(k+1)-rf0(1,1,k)*wprof(k))*rdz*mh(1,1,k)' in cm1_series.tree['adv_routines.F']
    assert 'tem1 = tem*( lsnudge_th(k,lsnudge_count)-thavg(k) )' in inflow
    assert 'tem2 = tem*( lsnudge_qv(k,lsnudge_count)-qavg(k,nqv) )' in inflow
    assert f"file='{RATES}'" in inflow
    solve3 = cm1_series.source('solve3.F', PATCH_09)
    assert solve3.count('tem = lsnudgefac*dt/lab_tau_uv') == 2 and 'lsnudgefac*dt/lsnudge_tau' not in solve3
    assert 'wind_nudge_zmin' not in solve3


# The nudging of solve1.F and the relaxation of solve3.F, compiled together and stepped on a domain's means.

def nudge_block(text):
    """The large-scale nudging of solve1.F: the domain's means, the nudging of the wind, theta and vapour, and the
    patch's inflow."""
    start = text.index('    IF( do_lsnudge .and. timenudge.gt.lsnudge_start )THEN\n')
    return text[start:text.index('\n    ENDIF\n', start) + len('\n    ENDIF\n')]


def base_block(text):
    """The relaxation of the base-state and geostrophic wind in solve3.F."""
    start = text.index('      if( do_lsnudge .and. donudge .and. do_lsnudge_u )then\n')
    return text[start:text.index('#ifdef MPI\n      call comm_3u_end', start)]


NUDGE_DRIVER = """
program nudging
  ! The large-scale nudging of solve1.F and the relaxation of the base-state and geostrophic wind of solve3.F, stepped
  ! on a domain's means without dynamics; the settings and the profiles come from standard input.
  implicit none
  integer :: ni, nj, nk, nsteps, pattern, step, i, j, k, ib, ie, jb, je
  integer :: nqv, imoist, myid, timestats, lsnudge_count, ud_nudge, vd_nudge, td_nudge, qd_nudge, inflow_ref_air
  integer :: switches(7)
  logical :: do_lsnudge, do_lsnudge_u, do_lsnudge_v, do_lsnudge_th, do_lsnudge_qv, donudge, dolsw, dotdwrite
  logical :: lab_inflow_out
  real :: timenudge, lsnudge_start, lsnudgefac, lsnudge_tau, umove, vmove, rdt, dt, tem, tem1, tem2, terluna_w
  real :: var14, var15, time_misc, rdz, wind_nudge_tau, wind_nudge_zmin, lab_tau_uv
  real, allocatable :: uavg(:), vavg(:), thavg(:), qavg(:,:), wprof(:), ug(:), vg(:), dumk5(:)
  double precision, allocatable :: cavg(:,:)
  real, allocatable :: th0(:,:,:), ua(:,:,:), va(:,:,:), tha(:,:,:), qa(:,:,:,:), ruh(:), ruf(:), rvh(:), rvf(:)
  real, allocatable :: uten1(:,:,:), vten1(:,:,:), thten1(:,:,:), qten(:,:,:,:)
  real, allocatable :: udiag(:,:,:,:), vdiag(:,:,:,:), tdiag(:,:,:,:), qdiag(:,:,:,:)
  real, allocatable :: zh(:,:,:), rf0(:,:,:), rr0(:,:,:), mh(:,:,:), u0(:,:,:), v0(:,:,:)
  real, allocatable :: lsnudge_u(:,:), lsnudge_v(:,:), lsnudge_th(:,:), lsnudge_qv(:,:)
  real, allocatable :: column(:)

  read(*,*) ni, nj, nk, nsteps, pattern
  read(*,*) switches
  read(*,*) dt, lsnudge_tau, lsnudgefac, umove, vmove, var14, var15, rdz
  read(*,*) wind_nudge_tau, wind_nudge_zmin, inflow_ref_air
  do_lsnudge = switches(1).eq.1; do_lsnudge_u = switches(2).eq.1; do_lsnudge_v = switches(3).eq.1
  do_lsnudge_th = switches(4).eq.1; do_lsnudge_qv = switches(5).eq.1; donudge = switches(6).eq.1
  dolsw = switches(7).eq.1
  ib = 0; ie = ni + 1; jb = 0; je = nj + 1
  nqv = 1; imoist = 1; myid = 0; timestats = 0; lsnudge_count = 1; dotdwrite = .false.
  ud_nudge = 0; vd_nudge = 0; td_nudge = 0; qd_nudge = 0
  timenudge = 1000.0; lsnudge_start = 1.0; time_misc = 0.0; lab_inflow_out = .true.
  allocate(uavg(0:nk+1), vavg(0:nk+1), thavg(0:nk+1), qavg(0:nk+1,1), wprof(0:nk+2), ug(0:nk+1), vg(0:nk+1))
  allocate(dumk5(0:nk+1), cavg(0:nk+1,4), column(nk+1))
  allocate(th0(ib:ie,jb:je,0:nk+1), ua(ib:ie,jb:je,0:nk+1), va(ib:ie,jb:je,0:nk+1), tha(ib:ie,jb:je,0:nk+1))
  allocate(qa(ib:ie,jb:je,0:nk+1,1), ruh(ib:ie), ruf(ib:ie), rvh(jb:je), rvf(jb:je))
  allocate(uten1(ib:ie+1,jb:je+1,0:nk+1), vten1(ib:ie+1,jb:je+1,0:nk+1), thten1(ib:ie+1,jb:je+1,0:nk+1))
  allocate(qten(ib:ie+1,jb:je+1,0:nk+1,1))
  allocate(udiag(1,1,1,1), vdiag(1,1,1,1), tdiag(1,1,1,1), qdiag(1,1,1,1))
  allocate(zh(ib:ie,jb:je,0:nk+1), rf0(ib:ie,jb:je,0:nk+2), rr0(ib:ie,jb:je,0:nk+1), mh(ib:ie,jb:je,0:nk+1))
  allocate(u0(ib:ie+1,jb:je+1,0:nk+1), v0(ib:ie+1,jb:je+1,0:nk+1))
  allocate(lsnudge_u(nk,1), lsnudge_v(nk,1), lsnudge_th(nk,1), lsnudge_qv(nk,1))
  uavg = 0.0; vavg = 0.0; thavg = 0.0; qavg = 0.0; wprof = 0.0; ug = 0.0; vg = 0.0; dumk5 = 0.0
  rf0 = 1.0; rr0 = 1.0; mh = 1.0
  read(*,*) column(1:nk); call spread3(zh, column, nk)
  read(*,*) uavg(1:nk)
  read(*,*) vavg(1:nk)
  read(*,*) thavg(1:nk)
  read(*,*) qavg(1:nk,1)
  read(*,*) lsnudge_u(1:nk,1)
  read(*,*) lsnudge_v(1:nk,1)
  read(*,*) lsnudge_th(1:nk,1)
  read(*,*) lsnudge_qv(1:nk,1)
  read(*,*) ug(1:nk)
  read(*,*) vg(1:nk)
  read(*,*) column(1:nk); call spread3(u0, column, nk)
  read(*,*) column(1:nk); call spread3(v0, column, nk)
  read(*,*) wprof(1:nk+1)
  read(*,*) column(1:nk+1); call spread3(rf0, column, nk+1)
  read(*,*) column(1:nk); call spread3(rr0, column, nk)
  read(*,*) column(1:nk); call spread3(mh, column, nk)

  do step = 1, nsteps
    if( pattern.eq.1 )then
      do k = 0, nk+1
      do j = jb, je+1
      do i = ib, ie+1
        uten1(i,j,k) = 1.0e-4*sin(real(i+3*j+7*k))
        vten1(i,j,k) = 1.0e-4*cos(real(2*i+j+5*k))
        thten1(i,j,k) = 1.0e-5*sin(real(3*i+2*j+k))
        qten(i,j,k,1) = 1.0e-8*cos(real(i+5*j+3*k))
      enddo
      enddo
      enddo
    else
      uten1 = 0.0; vten1 = 0.0; thten1 = 0.0; qten = 0.0
    endif
!SOLVE1
!SOLVE3
    if( pattern.eq.0 )then
      do k = 1, nk
        uavg(k) = uavg(k) + dt*uten1(1,1,k)
        vavg(k) = vavg(k) + dt*vten1(1,1,k)
        thavg(k) = thavg(k) + dt*thten1(1,1,k)
        qavg(k,1) = qavg(k,1) + dt*qten(1,1,k,1)
      enddo
    endif
  enddo

  write(*,'(a)') 'VALUES'
  call show('uten1', pack(uten1(1:ni+1,1:nj+1,1:nk), .true.))
  call show('vten1', pack(vten1(1:ni+1,1:nj+1,1:nk), .true.))
  call show('thten1', pack(thten1(1:ni+1,1:nj+1,1:nk), .true.))
  call show('qten', pack(qten(1:ni+1,1:nj+1,1:nk,1), .true.))
  call show('uavg', uavg(1:nk)); call show('vavg', vavg(1:nk))
  call show('thavg', thavg(1:nk)); call show('qavg', qavg(1:nk,1))
  call show('ug', ug(1:nk)); call show('vg', vg(1:nk))
  call show('u0', pack(u0(ib:ie+1,jb:je+1,1:nk), .true.)); call show('v0', pack(v0(ib:ie+1,jb:je+1,1:nk), .true.))
contains

  subroutine spread3(a, profile, n)
    ! a profile laid on every column
    real, intent(inout) :: a(:,:,0:)
    real, intent(in) :: profile(:)
    integer, intent(in) :: n
    integer :: kk
    do kk = 1, n
      a(:,:,kk) = profile(kk)
    enddo
  end subroutine spread3

  subroutine get_avg_uvtq(uavg, vavg, thavg, qavg, cavg, th0, ua, va, tha, qa, ruh, ruf, rvh, rvf, n)
    ! the domain's means come from standard input and the driver's steps
    real :: uavg(:), vavg(:), thavg(:), qavg(:,:), th0(:,:,:), ua(:,:,:), va(:,:,:), tha(:,:,:), qa(:,:,:,:)
    real :: ruh(:), ruf(:), rvh(:), rvf(:)
    double precision :: cavg(:,:)
    integer :: n
  end subroutine get_avg_uvtq

  subroutine get_avg_uvt(uavg, vavg, thavg, cavg, th0, ua, va, tha, ruh, ruf, rvh, rvf)
    real :: uavg(:), vavg(:), thavg(:), th0(:,:,:), ua(:,:,:), va(:,:,:), tha(:,:,:)
    real :: ruh(:), ruf(:), rvh(:), rvf(:)
    double precision :: cavg(:,:)
  end subroutine get_avg_uvt

  real function mytime()
    mytime = 0.0
  end function mytime
""" + """
  subroutine show(name, values)
    ! each value's bits, in hexadecimal
    character(len=*), intent(in) :: name
    real, intent(in) :: values(:)
    write(*,'(a,*(1x,z8.8))') name, values
  end subroutine show
end program nudging
"""

ON = (1, 1, 1, 1, 1, 1, 1)           # do_lsnudge, its u, v, theta and vapour, donudge, dolsw


@pytest.fixture(scope='module')
def nudgers(cm1_series, tmp_path_factory):
    """The nudging of solve1.F and the relaxation of solve3.F from the series before patch 09 and after it, in one
    program, under each flag set."""
    needs_compiler()
    out = {}
    for flags in FLAGS:
        for label, through in (('before', PATCH_08), ('after', PATCH_09)):
            driver = NUDGE_DRIVER.replace('!SOLVE1', nudge_block(cm1_series.source('solve1.F', through)))
            driver = driver.replace('!SOLVE3', base_block(cm1_series.source('solve3.F', through)))
            out[label, flags] = build(tmp_path_factory.mktemp('nudging'), driver, flags=FLAGS[flags])
    return out


def nudge_input(case, *, nsteps=1, pattern=1, switches=ON, tau=0.0, zmin=0.0, inflow=0):
    """The driver's input for a case of profiles (a dict of arrays on the case's nk levels, rf0 and wprof on nk + 1)."""
    rows = [f"{case['ni']} {case['nj']} {case['nk']} {nsteps} {pattern}", ' '.join(str(s) for s in switches),
            ' '.join(repr(float(case[k])) for k in ('dt', 'lsnudge_tau', 'lsnudgefac', 'umove', 'vmove', 'var14',
                                                    'var15', 'rdz')),
            f'{float(tau)!r} {float(zmin)!r} {int(inflow)}']
    for key in ('zh', 'uavg', 'vavg', 'thavg', 'qavg', 'u_ref', 'v_ref', 'th_ref', 'qv_ref', 'ug', 'vg', 'u0', 'v0',
                'wprof', 'rf0', 'rr0', 'mh'):
        rows.append(' '.join(repr(float(v)) for v in case[key]))
    return '\n'.join(rows) + '\n'


def random_case(seed, nk=14):
    """A domain of 3 x 2 columns whose means, references and base state are drawn at random about a moist column,
    with a large-scale wind that rises below 2.5 km and sinks above."""
    rng = np.random.default_rng(seed)
    zh = np.cumsum(rng.uniform(80.0, 900.0, nk))
    zw = np.r_[0.0, 0.5 * (zh[1:] + zh[:-1]), zh[-1] + 0.5 * (zh[-1] - zh[-2])]
    rho0 = 1.2 * np.exp(-zh / 8000.0)
    c2 = (zw[1:-1] - zh[:-1]) / (zh[1:] - zh[:-1])
    rf0 = np.r_[rho0[0], (1.0 - c2) * rho0[:-1] + c2 * rho0[1:], rho0[-1]]
    w = 0.004 * np.sin(np.pi * np.minimum(zw / 5000.0, 1.0)) - 0.001 * (zw > 5000.0)
    w[0] = w[-1] = 0.0
    th = 300.0 + 0.004 * zh
    qv = 0.015 * np.exp(-zh / 2500.0)
    return dict(ni=3, nj=2, nk=nk, dt=float(rng.uniform(5.0, 60.0)), lsnudge_tau=259200.0, lsnudgefac=1.0,
                umove=float(rng.uniform(-2.0, 2.0)), vmove=float(rng.uniform(-2.0, 2.0)),
                var14=float(zh[nk // 2]), var15=float(zh[3 * nk // 4]), rdz=1.0 / 500.0, zh=zh,
                uavg=rng.normal(3.0, 2.0, nk), vavg=rng.normal(-1.0, 2.0, nk), thavg=th + rng.normal(0.0, 1.0, nk),
                qavg=qv * rng.uniform(0.7, 1.1, nk), u_ref=rng.normal(3.0, 2.0, nk), v_ref=rng.normal(-1.0, 2.0, nk),
                th_ref=th, qv_ref=qv, ug=rng.normal(3.0, 2.0, nk), vg=rng.normal(-1.0, 2.0, nk),
                u0=rng.normal(3.0, 2.0, nk), v0=rng.normal(-1.0, 2.0, nk), wprof=w, rf0=rf0, rr0=1.0 / rho0,
                mh=500.0 / np.diff(zw))


def columns(found, case, name):
    """A tendency the driver writes for every point, as (k, j, i)."""
    return values(found[name]).reshape(case['nk'], case['nj'] + 1, case['ni'] + 1)


# The points each tendency's loops in solve1.F reach, as (k, j, i): u at i = 1..ni+1 and j = 1..nj, v at i = 1..ni and
# j = 1..nj+1, theta and vapour at i = 1..ni and j = 1..nj. The driver writes one point further in each direction.
REACH = dict(uten1=np.s_[:, :-1, :], vten1=np.s_[:, :, :-1], thten1=np.s_[:, :-1, :-1], qten=np.s_[:, :-1, :-1])


def outside(case, name):
    """The points the driver writes beyond a tendency's reach."""
    mask = np.ones((case['nk'], case['nj'] + 1, case['ni'] + 1), bool)
    mask[REACH[name]] = False
    return mask


def test_at_the_defaults_the_nudging_keeps_its_bits(nudgers):
    """With the three entries at their defaults the nudging after the patch returns every tendency, every stepped mean
    and the relaxed base-state and geostrophic wind of the nudging before it, bit for bit, under CM1's flags and under
    -O3 -march=native: one step on tendencies already set, twenty steps from nil, with the wind's nudging off, and
    with the large-scale vertical wind off."""
    for flags in FLAGS:
        for seed in range(4):
            case = random_case(seed)
            for options in (dict(), dict(nsteps=20, pattern=0), dict(switches=(1, 0, 0, 1, 1, 1, 1)),
                            dict(switches=(1, 1, 1, 1, 1, 1, 0))):
                before = run(nudgers['before', flags], nudge_input(case, **options))[1]
                assert run(nudgers['after', flags], nudge_input(case, **options))[1] == before, (flags, seed, options)


def test_the_wind_relaxes_on_its_own_time(nudgers):
    """With wind_nudge_tau = 7200 s the wind's tendency is the departure of the domain's mean wind from its target
    over 7,200 s where theta and vapour keep lsnudge_tau's three days, whose tendencies stay those of the default bit
    for bit. Stepped on the means, the wind's departure from its target falls as (1 - dt/tau)^n on the wind's time,
    to about 1/e in two hours, and the base-state and geostrophic wind of solve3.F follow on the same time, where the
    defaults relax all of them on the three days; theta keeps its three days, weighted as core patch 09 holds it."""
    case = random_case(7)
    exe = nudgers['after', 'cm1']
    default = run(exe, nudge_input(case))[1]
    found = run(exe, nudge_input(case, tau=7200.0))[1]
    target_u, target_v = single(case['u_ref']) - single(case['umove']), single(case['v_ref']) - single(case['vmove'])
    for name, mean, target in (('uten1', single(case['uavg']), target_u), ('vten1', single(case['vavg']), target_v)):
        got, before = columns(found, case, name), columns(default, case, name)
        added = (got - before)[REACH[name]] + (-(mean - target) / 259200.0)[:, None, None]
        assert added == pytest.approx(np.broadcast_to((-(mean - target) / 7200.0)[:, None, None], added.shape),
                                      rel=1e-5, abs=1e-9)
        assert np.array_equal(got[outside(case, name)], before[outside(case, name)])
    assert found['thten1'] == default['thten1'] and found['qten'] == default['qten']
    # Stepped: 36 steps of 200 s, two hours.
    stepped = dict(case, dt=200.0)
    zh = single(case['zh'])
    weight = np.clip((zh - single(case['var14'])) / (single(case['var15']) - single(case['var14'])), 0.0, 1.0)
    for tau in (7200.0, 0.0):
        ratio = (1.0 - 200.0 / (tau or 259200.0))**36
        means = run(exe, nudge_input(stepped, nsteps=36, pattern=0, tau=tau))[1]
        after = lambda start, target, factor=ratio: target + (single(start) - target) * factor
        assert values(means['uavg']) == pytest.approx(after(case['uavg'], target_u), abs=5e-5)
        assert values(means['vavg']) == pytest.approx(after(case['vavg'], target_v), abs=5e-5)
        assert values(means['ug']) == pytest.approx(after(case['ug'], target_u), abs=5e-5)
        assert values(means['vg']) == pytest.approx(after(case['vg'], target_v), abs=5e-5)
        # solve3.F relaxes u0 at i = ib..ie+1 and j = jb..je, and v0 at i = ib..ie and j = jb..je+1: every column alike
        u0 = values(means['u0']).reshape(case['nk'], case['nj'] + 3, case['ni'] + 3)[:, :-1, :].reshape(case['nk'], -1)
        v0 = values(means['v0']).reshape(case['nk'], case['nj'] + 3, case['ni'] + 3)[:, :, :-1].reshape(case['nk'], -1)
        assert np.all(u0 == u0[:, :1]) and np.all(v0 == v0[:, :1])
        assert u0[:, 0] == pytest.approx(after(case['u0'], target_u), abs=5e-5)
        assert v0[:, 0] == pytest.approx(after(case['v0'], target_v), abs=5e-5)
        assert values(means['thavg']) == pytest.approx(
            after(case['thavg'], single(case['th_ref']), (1.0 - weight * 200.0 / 259200.0)**36), abs=2e-3)
    assert (1.0 - 200.0 / 7200.0)**36 == pytest.approx(math.exp(-1.0), rel=0.02)
    assert np.abs(single(case['uavg']) - target_u).max() > 1.0                  # departures the steps resolve


def test_the_wind_is_pulled_from_its_height_up(nudgers):
    """With wind_nudge_zmin at a level's height the wind's tendencies are nil at the levels below it and those of the
    pull from the ground at that level and above, bit for bit; theta and vapour keep theirs; and the base-state and
    geostrophic wind relax at every level, the pull's height aside. So for Terluna's form, under both flag sets."""
    case = random_case(11)
    zh = single(case['zh'])
    assert zh[0] < 312.7 < zh[-1]
    for flags in FLAGS:
        exe = nudgers['after', flags]
        nil = run(exe, nudge_input(case, switches=(1, 0, 0, 1, 1, 1, 1)))[1]       # the wind's nudging off
        for tau in (0.0, 7200.0):
            ground = run(exe, nudge_input(case, tau=tau))[1]
            full = run(exe, nudge_input(case, nsteps=5, pattern=0, tau=tau))[1]
            for zmin in (float(zh[4]), float(zh[4]) + 1.0, 312.7):
                below = zh < np.float32(zmin)
                assert 0 < below.sum() < case['nk']
                found = run(exe, nudge_input(case, tau=tau, zmin=zmin))[1]
                for name in ('uten1', 'vten1'):
                    got, pulled, free = (columns(r, case, name) for r in (found, ground, nil))
                    assert np.array_equal(got[~below], pulled[~below]) and np.array_equal(got[below], free[below])
                assert found['thten1'] == ground['thten1'] and found['qten'] == ground['qten']
                stepped = run(exe, nudge_input(case, nsteps=5, pattern=0, tau=tau, zmin=zmin))[1]
                for name in ('ug', 'vg', 'u0', 'v0'):                       # every level, the height aside
                    assert stepped[name] == full[name], (flags, tau, zmin, name)
                for name in ('uavg', 'vavg'):                               # the means below stand where they were
                    got, pulled = values(stepped[name]), values(full[name])
                    assert np.array_equal(got[below], single(case[name])[below])
                    assert np.array_equal(got[~below], pulled[~below])


# The inflow, on the vertical wind gcm_site writes.

def gcm_column():
    """A GCM column over a moist site, top first: its mean wind rises through the lowest 5 km, fastest near 2.2 km,
    and sinks from 6 to 14 km, as the GCM's over Terluna's sea site."""
    z = [60000.0, 30000.0, 14000.0, 9000.0, 6000.0, 4000.0, 2200.0, 1200.0, 316.0]
    return dict(profile=dict(z_m=z, theta_k=[520.0, 400.0, 345.0, 325.0, 315.0, 308.0, 303.0, 300.0, 299.0],
                             specific_humidity_kg_kg=[1e-6, 2e-5, 2e-4, 1.5e-3, 4e-3, 7e-3, 1.0e-2, 1.25e-2, 1.4e-2],
                             u_m_s=[0.0] * 9, v_m_s=[0.0] * 9),
                vertical_wind_m_s=[0.0, -0.0004, -0.0008, -0.0012, 0.0002, 0.0025, 0.0039, 0.0025, 0.0008],
                half_levels=[0.002, 0.03, 0.15, 0.3, 0.45, 0.6, 0.75, 0.88, 1.0], surface=dict(pressure_pa=1.2159e5),
                circulation=dict(hour_angle_deg=[-90.0, 90.0], theta_k_s=np.zeros((2, 9)),
                                 specific_humidity_kg_kg_s=np.zeros((2, 9))))


def inflow_case():
    """A box of 3 x 2 columns on stretched levels to 150 km, CM1's base-state density from the GCM's air in balance
    under the Moon's gravity, the mean vertical wind read back from the terluna_wls.txt gcm_site writes, and a domain
    whose air stands 0.4-1 K and 1-2 g/kg off the GCM's, the reference."""
    gravity = 1.6242
    dz = [100.0]
    while sum(dz) < 150000.0:
        dz.append(min(dz[-1] * 1.08, 2000.0))
    zw = np.r_[0.0, np.cumsum(dz)]
    zw[-1] = 150000.0
    zh = 0.5 * (zw[1:] + zw[:-1])
    forcing = gcm_column()
    air = gs.reference_air(forcing, gravity, zw[-1])
    w_file = np.loadtxt(gs.wls_text(zw, gs.to_cm1(forcing, zw, air, gravity)['w_m_s']).splitlines()[1:])
    assert np.allclose(w_file[:, 0], zw, atol=5e-4)
    density = lambda z, p: p / (gs.CM1_RD * gs.virtual_theta(air['theta_at'](z), air['qv_at'](z))
                                * (p / gs.P00)**gs.CM1_KAPPA)
    p_w = gs.column_pressures(zw, air['theta_at'], air['qv_at'], 1.2159e5, gravity)
    p_h = np.exp(0.5 * (np.log(p_w[1:]) + np.log(p_w[:-1])))
    rho0 = density(zh, p_h)
    c2 = (zw[1:-1] - zh[:-1]) / (zh[1:] - zh[:-1])
    rf0 = np.r_[rho0[0], (1.0 - c2) * rho0[:-1] + c2 * rho0[1:], rho0[-1]]          # CM1's: linear between levels
    nk = zh.size
    th, qv = air['theta_at'](zh), air['qv_at'](zh)
    shift = np.linspace(0.0, 1.0, nk)
    case = dict(ni=3, nj=2, nk=nk, dt=40.0, lsnudge_tau=259200.0, lsnudgefac=1.0, umove=0.0, vmove=0.0, var14=93000.0,
                var15=113000.0, rdz=1.0 / 500.0, zh=zh, uavg=np.full(nk, 2.0), vavg=np.full(nk, -1.0),
                thavg=th - 0.4 - 0.6 * shift, qavg=qv * (0.9 - 0.05 * shift), u_ref=np.full(nk, 3.0),
                v_ref=np.zeros(nk), th_ref=th, qv_ref=qv, ug=np.full(nk, 3.0), vg=np.zeros(nk), u0=np.full(nk, 3.0),
                v0=np.zeros(nk), wprof=w_file[:, 1], rf0=rf0, rr0=1.0 / rho0, mh=500.0 / np.diff(zw))
    return case, dict(zw=zw, zh=zh, w=w_file, rho_w=density(zw, p_w), rho0=rho0)


def written_rates(exe, nk):
    words = (exe.parent / RATES).read_text().split()
    assert int(words[0]) == nk and len(words) == 1 + 2 * nk
    return np.array([float(v) for v in words[1:]]).reshape(nk, 2)


def test_the_inflow_draws_in_the_references_air_where_the_mean_wind_converges(nudgers):
    """With inflow_ref_air = 1 each level's theta and vapour gain the rate max(d(rho0 w)/dz, 0)/rho0 times the
    reference less the domain's mean, the same in every column, beside the tendencies they had: nil where the mean
    wind diverges, and nil while the domain's mean air is the reference. The rates the block writes, once, match the
    convergence by hand on the block's own inputs to 1 part in 10^5 of their largest, and, by Terluna's own check, the
    rates reckoned independently from the gcm_site file's vertical wind and the air's density at the w levels, within
    2% wherever the reckoned rate exceeds 1% of its largest. The low inflow reaches the mean wind's fastest level,
    2.2 km, and above 14 km, where the sinking slows with height, the air the slowing draws in is the reference's too.
    Stepped 90 times on 40 s, the domain's low air comes toward the reference."""
    case, grid = inflow_case()
    nk = case['nk']
    for flags in FLAGS:
        exe = nudgers['after', flags]
        default = run(exe, nudge_input(case))[1]
        (exe.parent / RATES).unlink(missing_ok=True)
        head, found = run(exe, nudge_input(case, inflow=1))
        rates = written_rates(exe, nk)
        assert head.count('Lab: the mean wind draws in the reference air') == 1
        assert np.allclose(rates[:, 0], grid['zh'], atol=0.01)
        # by hand, on the block's own inputs in single precision
        rf0, w, rr0 = single(case['rf0']), single(case['wprof']), single(case['rr0'])
        div = (rf0[1:] * w[1:] - rf0[:-1] * w[:-1]) * single(case['rdz']) * single(case['mh'])
        by_hand = np.maximum(div, 0.0) * rr0
        assert np.abs(rates[:, 1] - by_hand).max() <= 1e-5 * by_hand.max()
        assert np.all(rates[div < 0.0, 1] == 0.0) and (div < 0.0).sum() > 10 and (div > 0.0).sum() > 10
        # Terluna's check: the rates reckoned from the file's wind and the density at the w levels
        conv = np.diff(grid['rho_w'] * grid['w'][:, 1]) / np.diff(grid['zw'])
        reckoned = np.maximum(conv, 0.0) / grid['rho0']
        big = reckoned > 0.01 * reckoned.max()
        ratio = rates[big, 1] / reckoned[big]
        assert big.sum() >= 10 and np.abs(ratio - 1.0).max() <= 0.02, (ratio.min(), ratio.max())
        assert np.all(rates[conv < 0.0, 1] == 0.0)
        drawn = rates[:, 1] > 0.0
        first_out = int(np.argmin(drawn))                                    # the first level the wind leaves
        assert drawn[:first_out].all() and 2000.0 < grid['zh'][first_out] < 2600.0
        assert drawn[(grid['zh'] > 15000.0) & (grid['zh'] < 29000.0)].all()
        # the tendencies
        for name, ref, mean in (('thten1', 'th_ref', 'thavg'), ('qten', 'qv_ref', 'qavg')):
            added = columns(found, case, name) - columns(default, case, name)
            want = (rates[:, 1] * (single(case[ref]) - single(case[mean])))[:, None, None]
            assert np.abs(added[REACH[name]] - want).max() <= 1e-4 * np.abs(want).max(), name
            assert np.all(added[rates[:, 1] == 0.0] == 0.0) and np.all(added[outside(case, name)] == 0.0)
        assert found['uten1'] == default['uten1'] and found['vten1'] == default['vten1']
        # nil while the domain's air is the reference
        same = dict(case, thavg=case['th_ref'], qavg=case['qv_ref'])
        assert run(exe, nudge_input(same, inflow=1))[1] == run(exe, nudge_input(same))[1]
        # without the large-scale vertical wind the inflow stands still
        off = (1, 1, 1, 1, 1, 1, 0)
        assert run(exe, nudge_input(case, inflow=1, switches=off))[1] == run(exe, nudge_input(case, switches=off))[1]
    # Stepped 90 times on 400 s, the rates go to their file once and the low air comes toward the reference by the
    # rate's factor, (1 - rate dt)^n, to the rounding of 90 single-precision sums, where the steps move theta by more
    # than its single precision resolves.
    exe = nudgers['after', 'cm1']
    head, found = run(exe, nudge_input(dict(case, dt=400.0), nsteps=90, pattern=0, inflow=1))
    assert head.count('Lab: the mean wind draws in the reference air') == 1
    rates = written_rates(exe, nk)[:, 1]
    low = (rates > 0.1 * rates.max()) & (grid['zh'] < 2600.0)
    still = (rates == 0.0) & (grid['zh'] < case['var14'])                    # neither drawn in nor held
    for name, ref in (('thavg', 'th_ref'), ('qavg', 'qv_ref')):
        start, target = single(case[name]), single(case[ref])
        want = target + (start - target) * (1.0 - rates * 400.0)**90
        rounding = 90 * 0.5 * float(np.spacing(np.float32(start.max())))
        assert values(found[name])[low] == pytest.approx(want[low], rel=1e-6, abs=rounding)
        assert np.all(np.abs(values(found[name]) - target)[low] < np.abs(start - target)[low]), name
        assert np.array_equal(values(found[name])[still], start[still]), name
    assert low.sum() >= 10 and ((1.0 - rates * 400.0)**90)[low].min() < 0.95


# The stops.

def stop_block(text):
    start = text.index("      ! Lab: the wind's own nudging, wind_nudge_tau (s)")
    return text[start:text.index('      call set_constants( testcase , world_g )\n', start)]


STOP_DRIVER = """
program stops
  ! The checks of param.F on the patch's three entries, with stopcm1 reporting the stop.
  implicit none
  integer :: myid, inflow_ref_air, imoist, testcase, switches(5)
  logical :: do_lsnudge, do_lsnudge_u, do_lsnudge_v, do_lsnudge_th, do_lsnudge_qv
  real :: wind_nudge_tau, wind_nudge_zmin, dtl, var13
  read(*,*) wind_nudge_tau, wind_nudge_zmin, inflow_ref_air, dtl, var13, testcase, imoist
  read(*,*) switches
  do_lsnudge = switches(1).eq.1; do_lsnudge_u = switches(2).eq.1; do_lsnudge_v = switches(3).eq.1
  do_lsnudge_th = switches(4).eq.1; do_lsnudge_qv = switches(5).eq.1
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
    """The model stops as it starts on a wind's time below zero or shorter than its step, on a pull's height below the
    ground or a NaN, on either set where lsnudge nudges no wind, on an inflow other than 0 and 1, and on an inflow
    without lsnudge's theta and vapour or without one profile of large-scale vertical wind; a box as gcm_site writes it
    runs, as do the defaults with no nudging."""
    needs_compiler()
    exe = build(tmp_path, STOP_DRIVER.replace('!BLOCK', stop_block(cm1_series.source('param.F', PATCH_09))),
                FLAGS['cm1'])
    nan = float('nan')
    box = dict(tau=7200.0, zmin=316.1, inflow=1, dtl=40.0, var13=1.0, testcase=0, imoist=1, on=(1, 1, 1, 1, 1))
    cases = [(dict(), None),
             (dict(tau=0.0, zmin=0.0, inflow=0, on=(0, 0, 0, 0, 0)), None),
             (dict(inflow=0), None), (dict(on=(1, 0, 1, 1, 1)), None), (dict(tau=40.0), None),
             (dict(var13=0.0, testcase=5), None),
             (dict(tau=-1.0), 'wind_nudge_tau must be 0 or at least dtl'),
             (dict(tau=20.0), 'wind_nudge_tau must be 0 or at least dtl'),
             (dict(tau=nan), 'wind_nudge_tau must be 0 or at least dtl'),
             (dict(zmin=-5.0), 'wind_nudge_zmin 0 or more'), (dict(zmin=nan), 'wind_nudge_zmin 0 or more'),
             (dict(inflow=0, on=(0, 1, 1, 1, 1)), 'act on the wind that lsnudge nudges'),
             (dict(tau=0.0, inflow=0, on=(1, 0, 0, 1, 1)), 'act on the wind that lsnudge nudges'),
             (dict(inflow=2), 'inflow_ref_air must be 0 or 1'), (dict(inflow=-1), 'inflow_ref_air must be 0 or 1'),
             (dict(on=(1, 1, 1, 1, 0)), 'draws in the theta and vapour'),
             (dict(on=(1, 1, 1, 0, 1)), 'draws in the theta and vapour'),
             (dict(imoist=0), 'draws in the theta and vapour'),
             (dict(tau=0.0, zmin=0.0, on=(0, 0, 0, 1, 1)), 'draws in the theta and vapour'),
             (dict(var13=0.0), 'one profile of large-scale vertical wind'),
             (dict(var13=2.0), 'one profile of large-scale vertical wind'),
             (dict(var13=2.0, testcase=5), 'one profile of large-scale vertical wind')]
    for change, message in cases:
        s = dict(box, **change)
        text = (f"{s['tau']!r} {s['zmin']!r} {s['inflow']} {s['dtl']!r} {s['var13']!r} {s['testcase']} {s['imoist']}\n"
                + ' '.join(str(x) for x in s['on']) + '\n')
        head, found = run(exe, text.replace('nan', 'NaN'))
        if message is None:
            assert 'ran' in found and 'Lab nudging' not in head, change
        else:
            assert 'stopped' in found and message in head, (change, head)
