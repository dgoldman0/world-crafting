"""Patch 10 of the lab's CM1 series: the box's own large-scale vertical wind by the damped gravity wave, read from
&param3 with defaults under which CM1 keeps the wind it imposes. The patch's texts put the six entries in place, and
the part of solve1.F that the patch changes compiles on its own: CM1's large-scale nudging with patch 09's inflow,
the wave before it, core patch 17's table after it and the wave's record, stepped on a domain's means without
dynamics. At the defaults that part keeps its bits under both of the builds' flag sets. With the wave on, its wind
is that of the discrete boundary-value problem d2(omega)/dp2 = Rd Tv'/(tau c^2 p) solved apart in double precision,
and of the continuous problem to its discretisation's error; it is nil where the box's air is its reference; it
lifts a warm departure and sinks a cool one, relaxing the first mode at 1/tau; it falls linearly in pressure below
the base and is nil at the ground and from the lid up; with the inflow it keeps the column's heat, water and air;
and its record holds every interval of the domain diagnostics, the run's last included. The stops of param.F and the
wave's own stop on its lid end a run on the settings the model cannot take.

The lab's own file. The patch comes from Terluna's DGW_PATCHES (climate/crm/cm1_run.py at 29af5c16; c3898a7c), whose
tests read its edit lists and stay in Terluna (climate/tests/test_cm1_dgw.py); the first-mode test follows Terluna's,
on the compiled block. A compiled box of the whole model ran once from scratch scripts (models/cm1/README.md).
"""
import math
import re

import numpy as np
import pytest

from climate.tests.test_cm1_nudging import FLAGS, build, needs_compiler, run, single, values

PATCH_09 = 'patches/lab/09-the-winds-own-nudging-and-the-inflow-of-the-reference.patch'
PATCH_10 = 'patches/lab/10-the-boxs-own-large-scale-vertical-wind-by-the-damped-gravity-wave.patch'
ENTRIES = ('lsw_coupling', 'lsw_tau', 'lsw_mode_speed', 'lsw_top', 'lsw_base', 'lsw_table_heat')
KINDS = ('MPI_INTEGER', 'MPI_REAL', 'MPI_REAL', 'MPI_REAL', 'MPI_REAL', 'MPI_INTEGER')
RECORD = 'lab_lsw_means.txt'
RD, RV, CP = 287.04, 461.5, 1005.7            # CM1's constants (constants.F)
MOON_G = 1.6242188765608128


# The patch's texts.

def test_the_coupling_patch_ends_the_labs_series(cm1_series):
    assert cm1_series.names[-1] == PATCH_10 and cm1_series.before(PATCH_10) == PATCH_09
    text = (cm1_series.folder / PATCH_10).read_text(encoding='latin-1')
    assert re.findall(r'^\+\+\+ b/src/(\S+)', text, flags=re.M) == ['cm1.F', 'input.F', 'param.F', 'solve1.F']
    removed = [line[1:] for line in text.splitlines() if line.startswith('-') and not line.startswith('---')]
    assert removed == ['      real, intent(in),    dimension(kb:ke) :: wprof']          # solve1 now sets it
    added = cm1_series.added(PATCH_10)
    for line in added:
        assert len(line) <= 120, line
        if line in ('#ifdef MPI', '#endif'):                             # the rank's sum, as CM1 writes its own
            continue
        for mark in ('TERLUNA_', '//', '/*', '#'):                      # cpp would read these
            assert mark not in line, line
    # Nothing of a world is compiled in: the patch's lines name the lab, and no number in them is a world's.
    assert not any('terluna' in line.lower().split('!')[0] for line in added if 'terluna_th' not in line
                   and 'terluna_qv' not in line)
    numbers = {n for line in added for n in re.findall(r'(?<![\w.])\d+\.\d*(?:e-?\d+)?', line.split('!')[0])}
    assert numbers <= {'0.0', '0.5', '1.0', '1.5', '2.0', '0.0d0'}, numbers


def test_each_entry_is_declared_defaulted_read_broadcast_checked_and_printed(cm1_series):
    cm1, inputs, param = (cm1_series.source(name, PATCH_10) for name in ('cm1.F', 'input.F', 'param.F'))
    for default in ('      lsw_coupling = 0 ', '      lsw_tau = 0.0 ', '      lsw_mode_speed = 0.0 ',
                    '      lsw_top = 0.0 ', '      lsw_base = 0.0 ', '      lsw_table_heat = 0 '):
        assert cm1.count(default) == 1, default
    assert cm1.index('      lsw_table_heat = 0 ') < cm1.index("file='namelist.input'")   # the defaults, then reading
    for declared in ('      integer :: lsw_coupling ', '      real :: lsw_tau ', '      real :: lsw_mode_speed ',
                     '      real :: lsw_top,lsw_base ', '      integer :: lsw_table_heat ',
                     '      real :: lab_lsw_hpbl = 0.0 '):
        assert inputs.count(declared) == 1, declared
    assert ('                        wind_nudge_tau,wind_nudge_zmin,inflow_ref_air, &\n'
            '                        lsw_coupling,lsw_tau,lsw_mode_speed,lsw_top,lsw_base,lsw_table_heat, &\n'
            '                        csound,cstar,solconrce,zenanglrce\n') in inputs
    for name, kind in zip(ENTRIES, KINDS):
        assert param.count(f'      call MPI_BCAST({name},1,{kind},0,MPI_COMM_WORLD,ierr)') == 1, name
        assert param.count(f"      if(dowr) write(outfile,*) '{name} =',{name}  ! Lab\n") == 1, name
    stops = stop_block(param)
    assert param.index(stops) < param.index('      call set_constants( testcase , world_g )\n')
    assert stops.count('call stopcm1') == 7 and stops.count('Lab coupling:') == 7


def test_the_mean_boundary_layer_is_taken_before_solve1_over_every_rank(cm1_series):
    """cm1.F sums the boundary layer's depth over the rank's columns, adds the ranks' sums and divides by the domain's
    columns, just before solve1, and only with a coupling: the depths a restart file holds give a restarted run the
    mean of the run it continues."""
    cm1 = cm1_series.source('cm1.F', PATCH_10)
    block = cm1[cm1.index('        IF( lsw_coupling.ge.1 )THEN\n          lab_lsw_hpbl = 0.0\n'):]
    block = block[:block.index('        ENDIF\n') + len('        ENDIF\n')]
    assert '            lab_lsw_hpbl = lab_lsw_hpbl + hpbl(i,j)\n' in block
    assert 'MPI_ALLREDUCE(mpi_in_place,lab_lsw_hpbl,1,MPI_REAL,MPI_SUM,MPI_COMM_WORLD,ierr)' in block
    assert block.endswith('          lab_lsw_hpbl = lab_lsw_hpbl/real(nx*ny)\n        ENDIF\n')
    assert cm1.index(block) < cm1.index('        call     solve1(nstep,num_soil_layers,')
    assert cm1.index('        call     solve1(nstep,num_soil_layers,') - cm1.index(block) < len(block) + 200
    assert "hpbl(ib,jb),'hpbl    '" in cm1_series.tree['restart_write.F']       # the depths go with each restart


def test_the_wave_stands_before_the_inflow_and_its_record_after_the_table(cm1_series):
    """In solve1.F the wave sits inside CM1's large-scale nudging, after the domain's means and the nudging of
    vapour and before patch 09's inflow, which reads the wind it sets; the inflow and the table add to the record's
    sums, the table's heating stops at the base with lsw_table_heat = 1, and the record is written after the table, at
    the step that ends an interval of the domain diagnostics or the run."""
    solve1 = cm1_series.source('solve1.F', PATCH_10)
    region = coupled_region(solve1)
    wave, inflow = region.index('      IF( lsw_coupling.ge.1 .and. dolsw )THEN\n'), region.index(
        '      IF( inflow_ref_air.eq.1 .and. dolsw )THEN\n')
    assert region.index('call     get_avg_uvtq') < region.index('qdiag(i,j,k,qd_nudge) = tem1') < wave < inflow
    assert region.index('lab_lsw_sth(k) = lab_lsw_sth(k) + tem1') > inflow
    table = region.index('    IF( var11.gt.0.5 )THEN\n')
    cut = ('        if( lsw_table_heat.eq.1 .and. zh(1,1,k).gt.max( lsw_base , min( lab_lsw_hpbl , lsw_top ) ) ) '
           'terluna_th = 0.0\n')
    assert table < region.index(cut) < region.index('          lab_lsw_stt(k) = lab_lsw_stt(k) + terluna_th\n') < \
        region.index('          thten1(i,j,k) = thten1(i,j,k) + terluna_th\n')
    written = region.index("            open(unit=94,file='lab_lsw_means.txt',status='replace',action='write')\n")
    assert written > region.index('          thten1(i,j,k) = thten1(i,j,k) + terluna_th\n')
    assert '( dotdwrite .or. (mtime+dbldt).ge.dble(timax) )' in region
    assert 'wprof(k) = -lab_lsw_om(k)/( rf0(1,1,k)*g )' in region
    assert ('      real, intent(inout), dimension(kb:ke) :: wprof   ! Lab: the coupled wind sets it (lsw_coupling, '
            'param3)\n') in solve1
    assert 'unit=94' not in ''.join(text for name, text in cm1_series.tree.items() if name != 'solve1.F')


# The coupled part of solve1.F, compiled and stepped on a domain's means.

def coupled_region(text):
    """From CM1's large-scale nudging, with patch 09's inflow and the wave, through core patch 17's table and the
    wave's record."""
    start = text.index('    IF( do_lsnudge .and. timenudge.gt.lsnudge_start )THEN\n')
    return text[start:text.index('!-------------------------------------------------------------------\n'
                                 '!    NOTE:  now ok to change dum7,dum8\n', start)]


def declarations(text):
    """solve1.F's declarations of the wave's arrays and sums."""
    if '! Lab: the coupled large-scale vertical wind (lsw_coupling, param3): its pressures' not in text:
        return ''
    start = text.index('      ! Lab: the coupled large-scale vertical wind (lsw_coupling, param3): its pressures')
    end = text.index('      real :: lab_lsw_zb,lab_lsw_k2e\n', start) + len('      real :: lab_lsw_zb,lab_lsw_k2e\n')
    return text[start:end]


DRIVER = """
program coupling
  ! The large-scale nudging of solve1.F with the inflow and the wave, the day-night table and the wave's record,
  ! stepped on a domain's means without dynamics; the settings and the profiles come from standard input.
  implicit none
  integer :: ni, nj, nk, nsteps, pattern, showing, step, i, j, k, ib, ie, jb, je
  integer :: nqv, imoist, myid, timestats, lsnudge_count, ud_nudge, vd_nudge, td_nudge, qd_nudge, inflow_ref_air
  integer :: lsw_coupling, lsw_table_heat, irst
  integer :: switches(7)
  integer, save :: terluna_nb = 0, terluna_nl = 0
  integer :: terluna_b0, terluna_b1, terluna_l, terluna_m
  logical :: do_lsnudge, do_lsnudge_u, do_lsnudge_v, do_lsnudge_th, do_lsnudge_qv, donudge, dolsw, dotdwrite
  logical :: lab_inflow_out
  real :: timenudge, lsnudge_start, lsnudgefac, lsnudge_tau, umove, vmove, rdt, dt, tem, tem1, tem2, terluna_w
  real :: var11, var14, var15, var18, var19, time_misc, rdz, wind_nudge_tau, wind_nudge_zmin, lab_tau_uv
  real :: lsw_tau, lsw_mode_speed, lsw_top, lsw_base, lab_lsw_hpbl, timax, g, rd, rv
  real :: terluna_h, terluna_f, terluna_th, terluna_qv
  double precision :: mtime, dbldt, mtime0
  real, dimension(:), allocatable, save :: terluna_az
  real, dimension(:,:), allocatable, save :: terluna_ath, terluna_aqv
!DECLARE
  integer, allocatable :: writes(:)
  real, allocatable :: uavg(:), vavg(:), thavg(:), qavg(:,:), wprof(:)
  double precision, allocatable :: cavg(:,:)
  real, allocatable :: th0(:,:,:), ua(:,:,:), va(:,:,:), tha(:,:,:), qa(:,:,:,:), ruh(:), ruf(:), rvh(:), rvf(:)
  real, allocatable :: uten1(:,:,:), vten1(:,:,:), thten1(:,:,:), qten(:,:,:,:)
  real, allocatable :: udiag(:,:,:,:), vdiag(:,:,:,:), tdiag(:,:,:,:), qdiag(:,:,:,:)
  real, allocatable :: zh(:,:,:), zf(:,:,:), rf0(:,:,:), rr0(:,:,:), mh(:,:,:), prs0(:,:,:), pi0(:,:,:)
  real, allocatable :: lsnudge_u(:,:), lsnudge_v(:,:), lsnudge_th(:,:), lsnudge_qv(:,:)
  real, allocatable :: column(:)
  character(len=8) :: tag

  read(*,*) ni, nj, nk, nsteps, pattern, showing
  read(*,*) switches
  read(*,*) dt, lsnudge_tau, lsnudgefac, umove, vmove, var14, var15, rdz, g
  read(*,*) wind_nudge_tau, wind_nudge_zmin, inflow_ref_air
  read(*,*) lsw_coupling, lsw_tau, lsw_mode_speed, lsw_top, lsw_base, lsw_table_heat, lab_lsw_hpbl
  read(*,*) var11, var18, var19, mtime0, timax, irst
  allocate(writes(nsteps))
  read(*,*) writes
  do_lsnudge = switches(1).eq.1; do_lsnudge_u = switches(2).eq.1; do_lsnudge_v = switches(3).eq.1
  do_lsnudge_th = switches(4).eq.1; do_lsnudge_qv = switches(5).eq.1; donudge = switches(6).eq.1
  dolsw = switches(7).eq.1
  rd = 287.04; rv = 461.5
  ib = 0; ie = ni + 1; jb = 0; je = nj + 1
  nqv = 1; imoist = 1; myid = 0; timestats = 0; lsnudge_count = 1
  ud_nudge = 0; vd_nudge = 0; td_nudge = 0; qd_nudge = 0
  lsnudge_start = 1.0; time_misc = 0.0; lab_inflow_out = .true.
  allocate(uavg(0:nk+1), vavg(0:nk+1), thavg(0:nk+1), qavg(0:nk+1,1), wprof(0:nk+2), cavg(0:nk+1,4), column(nk+1))
  allocate(th0(ib:ie,jb:je,0:nk+1), ua(ib:ie,jb:je,0:nk+1), va(ib:ie,jb:je,0:nk+1), tha(ib:ie,jb:je,0:nk+1))
  allocate(qa(ib:ie,jb:je,0:nk+1,1), ruh(ib:ie), ruf(ib:ie), rvh(jb:je), rvf(jb:je))
  allocate(uten1(ib:ie+1,jb:je+1,0:nk+1), vten1(ib:ie+1,jb:je+1,0:nk+1), thten1(ib:ie+1,jb:je+1,0:nk+1))
  allocate(qten(ib:ie+1,jb:je+1,0:nk+1,1))
  allocate(udiag(1,1,1,1), vdiag(1,1,1,1), tdiag(1,1,1,1), qdiag(1,1,1,1))
  allocate(zh(ib:ie,jb:je,0:nk+1), zf(ib:ie,jb:je,0:nk+2), rf0(ib:ie,jb:je,0:nk+2), rr0(ib:ie,jb:je,0:nk+1))
  allocate(mh(ib:ie,jb:je,0:nk+1), prs0(ib:ie,jb:je,0:nk+1), pi0(ib:ie,jb:je,0:nk+1))
  allocate(lsnudge_u(nk,1), lsnudge_v(nk,1), lsnudge_th(nk,1), lsnudge_qv(nk,1))
  uavg = 0.0; vavg = 0.0; thavg = 0.0; qavg = 0.0; wprof = 0.0
  rf0 = 1.0; rr0 = 1.0; mh = 1.0; prs0 = 1.0; pi0 = 1.0; zf = 0.0
  read(*,*) column(1:nk); call spread3(zh, column, nk)
  read(*,*) column(1:nk+1); call spread3(zf, column, nk+1)
  read(*,*) uavg(1:nk)
  read(*,*) vavg(1:nk)
  read(*,*) thavg(1:nk)
  read(*,*) qavg(1:nk,1)
  read(*,*) lsnudge_u(1:nk,1)
  read(*,*) lsnudge_v(1:nk,1)
  read(*,*) lsnudge_th(1:nk,1)
  read(*,*) lsnudge_qv(1:nk,1)
  read(*,*) wprof(1:nk+1)
  read(*,*) column(1:nk+1); call spread3(rf0, column, nk+1)
  read(*,*) column(1:nk); call spread3(rr0, column, nk)
  read(*,*) column(1:nk); call spread3(mh, column, nk)
  read(*,*) column(1:nk); call spread3(prs0, column, nk)
  read(*,*) column(1:nk); call spread3(pi0, column, nk)

  do step = 1, nsteps
    mtime = mtime0 + dble(step-1)*dble(dt)
    dbldt = dble(dt)
    timenudge = real(mtime) + dt
    dotdwrite = writes(step).eq.1
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
!REGION
    if( showing.eq.1 )then
      write(tag,'(a,i3.3)') 'W', step
      call shown(tag, wprof(1:nk+1))
      write(tag,'(a,i3.3)') 'T', step
      call shown(tag, thten1(1,1,1:nk))
      write(tag,'(a,i3.3)') 'Q', step
      call shown(tag, qten(1,1,1:nk,1))
    endif
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
  call show('wprof', wprof(1:nk+1))
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

  subroutine stopcm1()
    write(*,'(a)') 'VALUES'
    write(*,'(a)') 'stopped 1'
    stop
  end subroutine stopcm1

  subroutine show(name, values)
    ! each value's bits, in hexadecimal
    character(len=*), intent(in) :: name
    real, intent(in) :: values(:)
    write(*,'(a,*(1x,z8.8))') name, values
  end subroutine show

  subroutine shown(name, values)
    ! a step's values, before the mark
    character(len=*), intent(in) :: name
    real, intent(in) :: values(:)
    write(*,'(a,*(1x,z8.8))') trim(name), values
  end subroutine shown
end program coupling
"""


@pytest.fixture(scope='module')
def couplers(cm1_series, tmp_path_factory):
    """The coupled part of solve1.F from the series before patch 10 and after it, in one program, under each flag
    set."""
    needs_compiler()
    out = {}
    for flags in FLAGS:
        for label, through in (('before', PATCH_09), ('after', PATCH_10)):
            text = cm1_series.source('solve1.F', through)
            driver = DRIVER.replace('!REGION', coupled_region(text)).replace('!DECLARE', declarations(text))
            out[label, flags] = build(tmp_path_factory.mktemp('coupling'), driver, flags=FLAGS[flags])
    return out


TABLE_BINS = 4


def table_text(nk, zh, seed=3):
    """A day-night table of four bins on the case's levels, as core patch 17 reads it."""
    rng = np.random.default_rng(seed)
    th = rng.normal(0.0, 2e-5, (TABLE_BINS, nk))
    qv = rng.normal(0.0, 3e-9, (TABLE_BINS, nk))
    return (f'{TABLE_BINS} {nk}\n' + ' '.join(f'{z:.3f}' for z in zh) + '\n'
            + ''.join(' '.join(f'{v:.6e}' for v in a) + '\n' + ' '.join(f'{v:.6e}' for v in b) + '\n'
                      for a, b in zip(th, qv))), th, qv


def levels(top, fine=1000.0, dz0=100.0, stretch=1.08, dz_max=2000.0):
    """w levels as the lab's boxes take them: dz0 up to `fine`, then stretched to dz_max, the last at `top`."""
    zw, dz = [0.0], dz0
    while zw[-1] < top:
        zw.append(zw[-1] + dz)
        if zw[-1] >= fine:
            dz = min(dz * stretch, dz_max)
    zw[-1] = top
    return np.array(zw)


def column_case(top=60000.0, n_bv=0.002, gravity=MOON_G, theta0=300.0, ps=1.2e5, seed=0, dz0=100.0):
    """A domain of 3 x 2 columns on stretched levels to `top`, its base state of uniform buoyancy frequency in
    hydrostatic balance at the gravity (CM1's pressure, Exner function and densities), its means at the reference,
    a moist column, and a large-scale wind that rises below a third of the top."""
    rng = np.random.default_rng(seed)
    zw = levels(top, dz0=dz0)
    nk = zw.size - 1
    zh = 0.5 * (zw[1:] + zw[:-1])
    theta = lambda z: theta0 * np.exp(n_bv ** 2 * z / gravity)
    fine = np.linspace(0.0, zw[-1], 200001)
    exner = (ps / 1e5) ** (RD / CP) - np.r_[0.0, np.cumsum(gravity / (CP * theta(fine[1:])) * np.diff(fine))]
    pi_at = lambda z: np.interp(z, fine, exner)
    rho_at = lambda z: 1e5 * pi_at(z) ** (CP / RD) / (RD * theta(z) * pi_at(z))
    qv = 0.012 * np.exp(-zh / 3000.0)
    w = 0.003 * np.sin(np.pi * np.minimum(zw / (top / 3.0), 1.0))
    w[0] = w[-1] = 0.0
    return dict(ni=3, nj=2, nk=nk, dt=40.0, lsnudge_tau=259200.0, lsnudgefac=1.0, umove=0.0, vmove=0.0,
                var14=2.0 * top, var15=3.0 * top, rdz=1.0 / 500.0, g=gravity, zh=zh, zf=zw,
                uavg=rng.normal(3.0, 2.0, nk), vavg=rng.normal(-1.0, 2.0, nk), thavg=theta(zh), qavg=qv,
                u_ref=np.full(nk, 3.0), v_ref=np.zeros(nk), th_ref=theta(zh), qv_ref=qv, wprof=w, rf0=rho_at(zw),
                rr0=1.0 / rho_at(zh), mh=500.0 / np.diff(zw), prs0=1e5 * pi_at(zh) ** (CP / RD), pi0=pi_at(zh),
                rho0=rho_at(zh))


ON = (1, 1, 1, 1, 1, 1, 1)           # do_lsnudge, its u, v, theta and vapour, donudge, dolsw


def coupling_input(case, *, nsteps=1, pattern=1, show=0, switches=ON, inflow=0, coupling=0, tau=0.0, speed=0.0,
                   top=0.0, base=0.0, heat=0, hpbl=0.0, var11=0.0, mtime0=0.0, timax=1.0e9, irst=0, writes=None,
                   tau_wind=0.0, zmin=0.0):
    """The driver's input for a case of profiles."""
    rows = [f"{case['ni']} {case['nj']} {case['nk']} {nsteps} {pattern} {show}", ' '.join(str(s) for s in switches),
            ' '.join(repr(float(case[k])) for k in ('dt', 'lsnudge_tau', 'lsnudgefac', 'umove', 'vmove', 'var14',
                                                    'var15', 'rdz', 'g')),
            f'{float(tau_wind)!r} {float(zmin)!r} {int(inflow)}',
            f'{int(coupling)} {float(tau)!r} {float(speed)!r} {float(top)!r} {float(base)!r} {int(heat)} '
            f'{float(hpbl)!r}',
            f'{float(var11)!r} -180.0 {float(4 * case["dt"] * nsteps + 1.0)!r} {float(mtime0)!r} {float(timax)!r} '
            f'{int(irst)}',
            ' '.join(str(int(x)) for x in (writes if writes is not None else [0] * nsteps))]
    for key in ('zh', 'zf', 'uavg', 'vavg', 'thavg', 'qavg', 'u_ref', 'v_ref', 'th_ref', 'qv_ref', 'wprof', 'rf0',
                'rr0', 'mh', 'prs0', 'pi0'):
        rows.append(' '.join(repr(float(v)) for v in case[key]))
    return '\n'.join(rows) + '\n'


def steps(head, letter, nsteps):
    """The values the driver shows at each step, by step, from its lines before the mark."""
    found = {line.split()[0]: line.split()[1:] for line in head.splitlines() if re.match(rf'^{letter}\d{{3}} ', line)}
    return np.array([values(found[f'{letter}{s:03d}']) for s in range(1, nsteps + 1)])


def go(exe, case, **options):
    """A run of the driver in a folder that holds the case's table."""
    (exe.parent / 'terluna_lsadv.txt').write_text(table_text(case['nk'], case['zh'])[0])
    return run(exe, coupling_input(case, **options))


def test_at_the_defaults_the_coupled_part_keeps_its_bits(couplers):
    """With the six entries at their defaults the part after the patch returns every tendency, every stepped mean and
    the large-scale vertical wind of the part before it, bit for bit, under CM1's flags and under -O3 -march=native:
    one step on tendencies already set and twenty from nil, with the inflow and the table on and off, with the
    wind's nudging off and with the large-scale vertical wind off; and it writes no record."""
    for flags in FLAGS:
        for seed in range(3):
            case = column_case(top=30000.0, dz0=300.0, seed=seed)
            case['thavg'] = case['th_ref'] + np.random.default_rng(seed).normal(0.0, 0.5, case['nk'])
            for options in (dict(), dict(nsteps=20, pattern=0), dict(inflow=1), dict(var11=1.0),
                            dict(nsteps=20, pattern=0, inflow=1, var11=1.0, writes=[1] * 20, timax=400.0),
                            dict(switches=(1, 0, 0, 1, 1, 1, 1), inflow=1), dict(switches=(1, 1, 1, 1, 1, 1, 0))):
                exe_b, exe_a = couplers['before', flags], couplers['after', flags]
                before = go(exe_b, case, **options)[1]
                (exe_a.parent / RECORD).unlink(missing_ok=True)
                assert go(exe_a, case, **options)[1] == before, (flags, seed, options)
                assert not (exe_a.parent / RECORD).exists()


# The wave's wind against the boundary-value problem.

def pf_levels(case):
    """The pressures of the w levels as the block takes them, in double precision from CM1's single-precision base
    state: log-linear to the ground and the top, geometric means between scalar levels."""
    p, zh, zf = single(case['prs0']), single(case['zh']), single(case['zf'])
    nk = zh.size
    pf = np.empty(nk + 1)
    pf[0] = p[0] * (p[0] / p[1]) ** ((zh[0] - zf[0]) / (zh[1] - zh[0]))
    pf[1:nk] = np.sqrt(p[:-1] * p[1:])
    pf[nk] = p[-1] * (p[-1] / p[-2]) ** ((zf[nk] - zh[-1]) / (zh[-1] - zh[-2]))
    return pf


def lid_level(case, top):
    zf = single(case['zf'])
    return next((k for k in range(1, zf.size) if zf[k] >= np.float32(top)), zf.size - 1)


def solve_bvp(case, tv, tau, speed, top):
    """omega (Pa/s) on the w levels from d2(omega)/dp2 = Rd Tv'/(tau c^2 p), nil at the ground and from the lid up,
    the second difference on the block's pressures and Tv' averaged onto the w levels, solved by numpy in double
    precision."""
    pf, lid = pf_levels(case), lid_level(case, top)
    inner = np.arange(1, lid)
    h1, h2 = pf[inner] - pf[inner - 1], pf[inner + 1] - pf[inner]
    a, c = 2.0 / (h1 * (h1 + h2)), 2.0 / (h2 * (h1 + h2))
    matrix = np.diag(-(a + c)) + np.diag(c[:-1], 1) + np.diag(a[1:], -1)
    rhs = RD * 0.5 * (tv[inner - 1] + tv[inner]) / (tau * speed ** 2 * pf[inner])
    omega = np.zeros(pf.size)
    omega[inner] = np.linalg.solve(matrix, rhs)
    return omega


def departure_case(case, tv):
    """The case with the domain's mean theta raised by Tv'/pi0 over the reference's, its vapour the reference's."""
    return dict(case, thavg=single(case['th_ref']) + tv / single(case['pi0']))


def tv_of(case):
    """The virtual-temperature departure the block forms, in double precision from the single-precision means."""
    eps = RV / RD - 1.0
    th, q, tr, qr, pi0 = (single(case[k]) for k in ('thavg', 'qavg', 'th_ref', 'qv_ref', 'pi0'))
    return pi0 * (th * (1.0 + eps * q) - tr * (1.0 + eps * qr))


def test_the_wave_solves_the_boundary_value_problem(couplers):
    """With the base at the ground the block's wind is -omega/(rho0 g) of the discrete problem solved apart in double
    precision, the departure taking the box's vapour and the reference's, to 1 part in 10^4 of its largest value, under
    both flag sets; and for omega = A sin(pi (p_s - p)/
    (p_s - p_lid)), whose Tv' = p omega''/(k2/eps Rd) the case sets at the scalar levels, the block returns that sine
    within 1% of its amplitude, the discretisation's error on sixty-six stretched levels."""
    case = column_case()
    tau, speed, top = 10800.0, 40.0, 45000.0
    zh = case['zh']
    tv = 0.4 * np.sin(np.pi * np.clip(zh / top, 0.0, 1.0)) * (zh < top) + 0.05 * np.cos(zh / 2000.0) * (zh < top)
    warm = departure_case(case, tv)
    warm['qavg'] = single(case['qv_ref']) * (1.0 + 0.1 * np.cos(zh / 3000.0))      # a vapour departure besides
    rho_g = single(case['rf0']) * single(case['g'])
    for flags in FLAGS:
        exe = couplers['after', flags]
        head, found = go(exe, warm, coupling=1, tau=tau, speed=speed, top=top)
        w = values(found['wprof'])
        omega = solve_bvp(case, tv_of(warm), tau, speed, top)
        assert np.abs(-w * rho_g - omega).max() <= 1e-4 * np.abs(omega).max(), flags
        assert 'Lab: the damped gravity wave; its lid (k, z) =' in head
    # The continuous problem: a sine in pressure between the ground and the lid.
    pf, lid = pf_levels(case), lid_level(case, top)
    ps, plid, amp = pf[0], pf[lid], 0.02
    k2e = 1.0 / (tau * speed ** 2)
    p_h = single(case['prs0'])
    shape = np.where(zh < case['zf'][lid], np.sin(np.pi * (ps - p_h) / (ps - plid)), 0.0)
    tv = -p_h * amp * (np.pi / (ps - plid)) ** 2 * shape / (k2e * RD)
    found = go(couplers['after', 'cm1'], departure_case(case, tv), coupling=1, tau=tau, speed=speed, top=top)[1]
    omega = -values(found['wprof']) * rho_g
    exact = np.where(np.arange(pf.size) < lid, amp * np.sin(np.pi * (ps - pf) / (ps - plid)), 0.0)
    assert np.abs(omega - exact).max() <= 0.01 * amp and np.abs(exact).max() > 0.99 * amp


def test_a_reference_equal_to_the_boxs_mean_gives_no_wind(couplers):
    """The box's mean air at its reference leaves the wind nil at every level under CM1's flags, bit for bit, from any
    imposed wind it held before, with the base low or high. Under -O3 -march=native gfortran fuses one of the two
    products theta (1 + eps q) of the departure into a multiply-add and rounds the other, so the departure of equal
    air keeps that rounding, about an ulp of 300 K, and the wind stays below 1e-6 m/s (2.9e-7 m/s on this column),
    where a departure of 0.1 K makes 8.5e-3 m/s; Terluna's block forms the departure the same way."""
    case = column_case()
    for flags, most in (('cm1', 0.0), ('native', 1e-6)):
        for hpbl in (0.0, 3000.0):
            found = go(couplers['after', flags], case, coupling=1, tau=10800.0, speed=40.0, top=45000.0, hpbl=hpbl,
                       inflow=1)[1]
            assert np.abs(values(found['wprof'])).max() <= most, flags
    tv = 0.1 * (case['zh'] < 45000.0)
    found = go(couplers['after', 'native'], departure_case(case, tv), coupling=1, tau=10800.0, speed=40.0,
               top=45000.0)[1]
    assert np.abs(values(found['wprof'])).max() > 1e-3 and np.abs(case['wprof']).max() > 1e-3


def first_mode(case, lid):
    """The discrete first baroclinic mode of the block's operator on the case's base state (Terluna's test, on the
    block's pressures): omega's shape on the w levels between the ground and the lid, its speed (m/s), and the
    static stability S_p = -(T/theta) dtheta/dp there, from M v = -mu D v with D = Rd S_p / p."""
    pf = pf_levels(case)
    th, p, pi0 = single(case['th_ref']), single(case['prs0']), single(case['pi0'])
    i = np.arange(1, lid)
    h1, h2 = pf[i] - pf[i - 1], pf[i + 1] - pf[i]
    a, c = 2.0 / (h1 * (h1 + h2)), 2.0 / (h2 * (h1 + h2))
    m = np.diag(-(a + c)) + np.diag(c[:-1], 1) + np.diag(a[1:], -1)
    sp = -0.5 * (pi0[i - 1] + pi0[i]) * (th[i] - th[i - 1]) / (p[i] - p[i - 1])
    mu, vec = np.linalg.eig(np.linalg.solve(np.diag(RD * sp / pf[i]), -m))
    k = int(np.argmin(mu.real))
    return dict(i=i, v=vec[:, k].real, c=1.0 / math.sqrt(mu[k].real), sp=sp)


def test_warm_departures_rise_and_cool_ones_sink_at_the_first_modes_rate(couplers):
    """A departure of the first mode's shape, 0.5 K at its peak, rises where warm and sinks where cool, and the wave's
    wind relaxes it, dT'/dt = omega S_p, at 1/tau within 5% when lsw_mode_speed is that mode's speed: a lunar column's
    first mode and an Earth column's, under both flag sets."""
    for gravity, n_bv, top, lid_m in ((MOON_G, 0.002, 80000.0, 60000.0), (9.81, 0.011, 24000.0, 15000.0)):
        case = column_case(gravity=gravity, n_bv=n_bv, top=top)
        lid = lid_level(case, lid_m)
        mode = first_mode(case, lid)
        i, sp = mode['i'], mode['sp']
        t_w = sp * mode['v']
        t_w *= 0.5 / t_w[np.argmax(np.abs(t_w))]
        peak = int(np.argmax(np.abs(t_w)))
        t_scalar = np.interp(case['zh'], case['zf'][i], t_w, left=0.0, right=0.0)
        tau = 7200.0
        for flags in FLAGS:
            for sign in (1.0, -1.0):
                found = go(couplers['after', flags], departure_case(case, sign * t_scalar), coupling=1, tau=tau,
                           speed=mode['c'], top=lid_m)[1]
                w = values(found['wprof'])
                assert np.sign(w[i[peak]]) == sign
                tendency = -single(case['rf0'])[i] * gravity * w[i] * sp
                rate = -tendency[peak] / (sign * t_w[peak])
                assert rate == pytest.approx(1.0 / tau, rel=0.05), (gravity, flags, rate * tau)
        assert 10.0 < mode['c'] < 150.0


def test_below_the_base_the_wind_falls_linearly_in_pressure_and_it_is_nil_at_the_ground_and_from_the_lid(couplers):
    """With a warm departure through the column, omega is nil at the ground and from the lid's w level up, bit for
    bit, and linear in the block's pressure at the w levels below the base, the boundary layer's mean depth held
    between lsw_base and the lid: at 2 km between a floor of 400 m and a 45 km lid, and at the floor where the
    boundary layer lies lower. A boundary layer that reaches the lid leaves the wind nil where the lid lies on a w
    level; otherwise the departure between the lid's height and its w level still acts, as in Terluna's block."""
    case = column_case()
    tv = 0.3 * np.ones(case['nk'])
    warm = departure_case(case, tv)
    pf = pf_levels(case)
    zh, zf = single(case['zh']), single(case['zf'])
    rho_g = single(case['rf0']) * single(case['g'])
    lid = lid_level(case, 45000.0)
    for hpbl, base in ((2000.0, 2000.0), (100.0, 400.0)):
        found = go(couplers['after', 'cm1'], warm, coupling=1, tau=10800.0, speed=40.0, top=45000.0, base=400.0,
                   hpbl=hpbl)[1]
        omega = -values(found['wprof']) * rho_g
        assert omega[0] == 0.0 and np.all(omega[lid:] == 0.0) and np.all(omega[1:lid] < 0.0)
        below = [k for k in range(1, zh.size) if zh[k] <= base]        # w levels whose two scalar levels lie below
        assert len(below) >= 3
        slope = omega[below] / (pf[0] - pf[below])
        assert np.abs(slope / slope[0] - 1.0).max() < 2e-4, slope
        above = int(np.argmin(np.abs(zh - 10000.0)))
        assert abs(omega[above] / (pf[0] - pf[above]) / slope[0] - 1.0) > 1e-2      # the source acts above the base
    on_level = float(zf[lid])                    # a lid on a w level leaves no scalar level between it and the top
    found = go(couplers['after', 'cm1'], warm, coupling=1, tau=10800.0, speed=40.0, top=on_level, base=400.0,
               hpbl=50000.0)[1]
    assert np.all(values(found['wprof']) == 0.0)


def test_with_the_inflow_the_wave_keeps_the_columns_heat_water_and_air(couplers):
    """The wave's wind and the inflow's tendencies from the compiled block, with CM1's large-scale advection in its
    flux form less the scalar times the convergence (wsub): the air the wave draws in equals the air it sends out, and
    the column gains the reference's theta and vapour where the wind converges and loses its own where it diverges,
    to 1 part in 10^5; air at the reference gains nothing. The inflow reads the wave's wind."""
    case = column_case()
    rng = np.random.default_rng(5)
    zh = case['zh']
    tv = (0.3 * np.sin(np.pi * np.clip(zh / 45000.0, 0.0, 1.0)) + 0.05 * rng.standard_normal(zh.size)) * (zh < 45000.0)
    warm = departure_case(case, tv)
    warm['qavg'] = single(case['qv_ref']) * 0.9
    found = go(couplers['after', 'cm1'], warm, coupling=1, tau=10800.0, speed=40.0, top=45000.0, base=300.0,
               hpbl=2000.0, inflow=1, pattern=0)[1]
    w = values(found['wprof'])
    rf0, rho = single(case['rf0']), 1.0 / single(case['rr0'])
    dz = 1.0 / (single(case['rdz']) * single(case['mh']))
    div = (rf0[1:] * w[1:] - rf0[:-1] * w[:-1]) / dz
    assert w[0] == 0.0 and w[-1] == 0.0 and np.abs(div).max() > 0.0
    assert abs((div * dz).sum()) < 1e-6 * np.abs(div * dz).sum()                   # the air drawn in is sent out
    for name, own, ref in (('thten1', single(warm['thavg']), single(case['th_ref'])),
                           ('qten', single(warm['qavg']), single(case['qv_ref']))):
        inflow = values(found[name]).reshape(case['nk'], case['nj'] + 1, case['ni'] + 1)[:, 0, 0]
        face = np.r_[0.0, 0.5 * (own[1:] + own[:-1]), 0.0]
        advect = (-(rf0 * w * face)[1:] + (rf0 * w * face)[:-1]) / dz / rho + own * div / rho
        gained = ((advect + inflow) * rho * dz).sum()
        expected = (dz * np.where(div > 0.0, div * ref, div * own)).sum()
        assert gained == pytest.approx(expected, rel=1e-5, abs=1e-5 * np.abs(div * dz * own).sum()), name
        small = 1e-4 * np.abs(div).max()
        assert np.all(inflow[div < -small] == 0.0) and np.all(inflow[div > small] != 0.0)


# The record.

def read_record(path):
    """lab_lsw_means.txt: for each interval its start, end, steps, mean base and level count, then seven columns a
    level."""
    words = path.read_text().split()
    rows, at = [], 0
    while at < len(words):
        t0, t1, n, zb, nk = (float(x) for x in words[at:at + 5])
        block = np.array([float(x) for x in words[at + 5:at + 5 + 7 * int(nk)]]).reshape(int(nk), 7)
        rows.append(dict(start=t0, end=t1, steps=n, base=zb, table=block))
        at += 5 + 7 * int(nk)
    return rows


def test_the_record_holds_every_interval_the_runs_last_included(couplers):
    """Over ten steps of 40 s from 3,600 s, with the domain diagnostics written at the ends of steps 3 and 7 and the
    run ending at step 10, the record holds three intervals, 3,600-3,720 s, 3,720-3,880 s and 3,880-4,000 s, of 3, 4
    and 3 steps; each holds, at each level, the mean over its steps of the wind and of the tendencies the inflow and
    the table add, to 1 part in 10^5, the table's heating cut above the base. A run that ends on an interval's end
    writes it once, a segment that stops short of its end writes nothing past its last interval, a fresh run replaces
    the file and a restarted run adds to it; and a boundary layer deeper than the lid sets the base at the lid."""
    case = column_case(top=30000.0, dz0=300.0)
    zh = case['zh']
    tv = 0.3 * np.sin(np.pi * np.clip(zh / 45000.0, 0.0, 1.0)) * (zh < 45000.0)
    warm = departure_case(case, tv)
    warm['qavg'] = single(case['qv_ref']) * 0.95
    exe = couplers['after', 'cm1']
    common = dict(coupling=1, tau=10800.0, speed=40.0, top=45000.0, base=300.0, hpbl=2000.0, nsteps=10, pattern=0,
                  show=1, mtime0=3600.0, timax=4000.0, writes=[0, 0, 1, 0, 0, 0, 1, 0, 0, 0])
    for inflow, var11, heat in ((1, 0.0, 0), (0, 1.0, 1), (1, 1.0, 1)):
        (exe.parent / RECORD).write_text('stale\n')
        head, found = go(exe, warm, inflow=inflow, var11=var11, heat=heat, **common)
        rows = read_record(exe.parent / RECORD)
        assert [(r['start'], r['end'], r['steps']) for r in rows] == [(3600.0, 3720.0, 3.0), (3720.0, 3880.0, 4.0),
                                                                     (3880.0, 4000.0, 3.0)]
        w, t, q = (steps(head, letter, 10) for letter in 'WTQ')
        for row, part in zip(rows, (slice(0, 3), slice(3, 7), slice(7, 10))):
            assert np.allclose(row['table'][:, 0], zh, atol=0.01) and np.allclose(row['table'][:, 1], case['zf'][:-1],
                                                                                    atol=0.01)
            assert row['base'] == pytest.approx(2000.0)
            assert row['table'][:, 2] == pytest.approx(w[part, :-1].mean(axis=0), rel=1e-5, abs=1e-12)
            got_t, got_q = row['table'][:, 3] + row['table'][:, 5], row['table'][:, 4] + row['table'][:, 6]
            assert got_t == pytest.approx(t[part].mean(axis=0), rel=1e-5, abs=1e-14)
            assert got_q == pytest.approx(q[part].mean(axis=0), rel=1e-5, abs=1e-18)
            if not inflow:
                assert np.all(row['table'][:, 3:5] == 0.0)
            if not var11:
                assert np.all(row['table'][:, 5:7] == 0.0)
            else:
                assert np.all(row['table'][zh > 2000.0, 5] == 0.0) and np.any(row['table'][zh < 2000.0, 5] != 0.0)
                assert np.any(row['table'][zh > 2000.0, 6] != 0.0)          # the moistening at every level
        assert np.abs(w).max() > 1e-4
    # A run that ends on an interval's end writes it once; a segment that stops short writes nothing past the last.
    go(exe, warm, **dict(common, writes=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1]))
    assert [(r['start'], r['end']) for r in read_record(exe.parent / RECORD)] == [(3600.0, 4000.0)]
    go(exe, warm, **dict(common, timax=9000.0))
    assert [(r['start'], r['end']) for r in read_record(exe.parent / RECORD)] == [(3600.0, 3720.0), (3720.0, 3880.0)]
    go(exe, warm, **dict(common, irst=1))                                 # a restart adds its intervals
    assert len(read_record(exe.parent / RECORD)) == 5
    # A boundary layer deeper than the lid sets the base at the lid.
    go(exe, warm, **dict(common, hpbl=50000.0))
    assert {r['base'] for r in read_record(exe.parent / RECORD)} == {45000.0}


# The stops.

def stop_block(text):
    start = text.index('      ! Lab: the coupled large-scale vertical wind of param3.')
    return text[start:text.index('      call set_constants( testcase , world_g )\n', start)]


STOP_DRIVER = """
program stops
  ! The checks of param.F on the patch's six entries, with stopcm1 reporting the stop.
  implicit none
  integer :: myid, lsw_coupling, lsw_table_heat, imoist, testcase, switches(4)
  logical :: do_lsnudge, do_lsnudge_th, do_lsnudge_qv
  real :: lsw_tau, lsw_mode_speed, lsw_top, lsw_base, dtl, var11, var13
  read(*,*) lsw_coupling, lsw_tau, lsw_mode_speed, lsw_top, lsw_base, lsw_table_heat
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
    """The model stops as it starts on a coupling other than 0 and 1; on the wave's entries set without the wave; on a
    wave whose time falls below the step, whose speed is nil, whose base lies below the ground or at the lid, or any
    of them NaN; on a table's heating rule other than 0 and 1 or without the table; and on a wave without lsnudge's
    theta and vapour, without moisture or without one profile of large-scale vertical wind. A box as gcm_site writes
    it runs, as do the defaults, a wave without the table's cut and a wave in test case 5."""
    needs_compiler()
    param = cm1_series.source('param.F', PATCH_10)
    block = stop_block(param)
    exe = build(tmp_path, STOP_DRIVER.replace('!BLOCK', block[block.index('      IF( lsw_coupling.ne.0'):]),
                FLAGS['cm1'])
    nan = float('nan')
    box = dict(c=1, tau=10303.0, speed=40.534, top=73084.5, base=316.1, heat=1, dtl=40.0, var11=1.0, var13=1.0,
               testcase=0, imoist=1, on=(1, 1, 1, 1))
    zero = dict(c=0, tau=0.0, speed=0.0, top=0.0, base=0.0, heat=0)
    cases = [(dict(), None), (zero, None), (dict(heat=0), None), (dict(var13=0.0, testcase=5, var11=0.0, heat=0), None),
             (dict(tau=40.0, base=0.0), None),
             (dict(c=2), 'lsw_coupling must be 0'), (dict(c=-1), 'lsw_coupling must be 0'),
             (dict(zero, tau=10303.0), 'act with lsw_coupling 1'), (dict(zero, top=73084.5), 'act with lsw_coupling 1'),
             (dict(zero, heat=1), 'act with lsw_coupling 1'), (dict(zero, base=nan), 'act with lsw_coupling 1'),
             (dict(tau=20.0), 'lsw_tau >= dtl'), (dict(tau=nan), 'lsw_tau >= dtl'), (dict(speed=0.0), 'lsw_tau >= dtl'),
             (dict(speed=nan), 'lsw_tau >= dtl'), (dict(base=-1.0), 'lsw_tau >= dtl'),
             (dict(base=73084.5), 'lsw_tau >= dtl'), (dict(top=nan), 'lsw_tau >= dtl'),
             (dict(heat=2), 'lsw_table_heat must be 0 or 1'), (dict(var11=0.0), 'acts on the table of var11 = 1'),
             (dict(on=(0, 1, 1, 1)), 'theta and vapour that lsnudge'), (dict(on=(1, 0, 1, 1)), 'theta and vapour'),
             (dict(on=(1, 1, 0, 1)), 'theta and vapour'), (dict(imoist=0), 'theta and vapour'),
             (dict(var13=0.0), 'one profile of large-scale vertical wind'),
             (dict(var13=2.0), 'one profile of large-scale vertical wind')]
    for change, message in cases:
        s = dict(box, **change)
        text = (f"{s['c']} {s['tau']!r} {s['speed']!r} {s['top']!r} {s['base']!r} {s['heat']}\n"
                f"{s['dtl']!r} {s['var11']!r} {s['var13']!r} {s['testcase']} {s['imoist']}\n"
                + ' '.join(str(x) for x in s['on']) + '\n')
        head, found = run(exe, text.replace('nan', 'NaN'))
        if message is None:
            assert 'ran' in found and 'Lab coupling' not in head, change
        else:
            assert 'stopped' in found and message in head, (change, head)


def test_the_wave_stops_on_a_lid_below_its_first_level(couplers):
    """A lid at or below the first w level above the ground leaves the wave no level to solve, and the block stops as
    it first runs; a lid above the box's top takes the top."""
    case = column_case()
    head, found = go(couplers['after', 'cm1'], case, coupling=1, tau=10800.0, speed=40.0, top=float(case['zf'][1]))
    assert 'stopped' in found and 'lsw_top lies at or below the first w level' in head
    tv = 0.3 * np.ones(case['nk'])
    head, found = go(couplers['after', 'cm1'], departure_case(case, tv), coupling=1, tau=10800.0, speed=40.0, top=1e7)
    assert re.search(r'its lid \(k, z\) =\s+%d\s' % (case['nk'] + 1), head) and values(found['wprof'])[-1] == 0.0
