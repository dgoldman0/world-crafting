"""Patches 03 and 04 of the lab's CM1 series: rain's limits at the build's gravity, and its fall law and self-collection
for the world. The patches' texts keep CM1's statements for the defaults, and one column of the patched Morrison
scheme, compiled from the series on the pinned archive and stepped without dynamics, keeps its bits at the defaults
under both of the builds' flag sets, takes the limits the Python computes, settles at their breakup equilibrium, falls
and evaporates by the table, each of whose three moments it reads where it needs it, and collects itself at the
namelist's rate.

The lab's own file. Terluna's tests of its edit lists and of its runner's namelist writers stay in Terluna
(climate/tests/test_cm1_rain_limits.py and test_cm1_rain_law.py at 39c5ee04). The column is CM1's mp_graupel, called as
mp_driver.F calls it; a compiled case of the whole model is stage 3's test (lab/design/plan.md).
"""
import math
import os
import random
import re
import shutil
import struct
import subprocess

import numpy as np
import pytest

from shared.constants import MOON_SURFACE_GRAVITY
from atmosphere.radiative_convective.thermodynamics import earthlike_air
from atmosphere.rain import breakup, drops, fall_law, morrison

PATCH_02 = 'patches/lab/02-beljaars-gust-over-water.patch'
PATCH_03 = 'patches/lab/03-raindrop-limits-at-the-builds-gravity.patch'
PATCH_04 = 'patches/lab/04-rains-fall-law-and-self-collection-for-the-world.patch'
POINTS = (PATCH_02, PATCH_03, PATCH_04)
CPP = ('cpp', '-C', '-P', '-traditional', '-Wno-invalid-pp-token', '-ffreestanding', '-DOPENMP')
# gfortran's flags in the two makefiles of the builds: CM1's own for OpenMP (makefile-gnu-omp.patch), and Terluna's
# optimisation of them (makefile-omp-O3-march-native.patch), the lab's default, under which gfortran fuses products
# into multiply-adds on a processor that has them.
COMMON = ('-ffree-form', '-ffree-line-length-none', '-finline-functions', '--param=max-vartrack-size=0', '-fopenmp')
FLAGS = dict(cm1=('-O2', *COMMON), native=('-O3', '-march=native', *COMMON))
MOON_G, EARTH_G = MOON_SURFACE_GRAVITY, morrison.GRAVITY
RD, WATER = 287.04, 997.0                    # morrison.F's R and RHOW
# The settings of &param3: the limits' three and the law's two.
OFF = ((0, 1.0, 0.0), (0, 0.0))
LUNAR_LIMITS = ((1, 1.2, 0.687), (0, 0.0))
LUNAR = ((1, 1.2, 0.687), (1, 2.919))

DRIVER = """
program rain_column
  ! One column of CM1's Morrison scheme, stepped without dynamics; the column and the settings come from standard input.
  use input
  use constants, only : set_constants, g
  use module_mp_graupel, only : graupel_init, mp_graupel
  implicit none
  integer :: n, k, steps, inum_flag, levels, limits_switch, law_switch
  real :: gravity, step_s, density_ratio, exponent, collection_rate
  real, allocatable, dimension(:,:,:) :: t3d, pii, qv, qc, qr, qi, qs, qg, nni, ns, nr, ng, nc, p, rho, ddz, w, rmh, rr
  real, allocatable, dimension(:,:,:) :: vtc, vtr, vti, vts, vtg, effc, effi, effs, effr, effg, effis
  real, allocatable, dimension(:,:,:) :: rainnc
  real, allocatable, dimension(:,:) :: prate
  real, allocatable, dimension(:,:,:,:) :: tdiag, qdiag, out3d
  real, allocatable, dimension(:) :: ruh, rvh
  double precision :: tcond, tevac, tevar, train

  read(*,*) levels, steps, step_s, gravity
  read(*,*) limits_switch, density_ratio, exponent
  read(*,*) law_switch, collection_rate
  timestats = 0
  testcase = 0
  call set_constants(testcase)
  g = gravity
  dowr = .true.
  outfile = 6
  ib = 1; ie = 1; jb = 1; je = 1; kb = 1; ke = levels
  ni = 1; nj = 1; nk = levels
  ibr = 1; ier = 1; jbr = 1; jer = 1; kbr = 1; ker = 1
  ibdt = 1; iedt = 1; jbdt = 1; jedt = 1; kbdt = 1; kedt = 1; ntdiag = 1
  ibdq = 1; iedq = 1; jbdq = 1; jedq = 1; kbdq = 1; kedq = levels; nqdiag = 2
  ib3d = 1; ie3d = 1; jb3d = 1; je3d = 1; kb3d = 1; ke3d = 1; nout3d = 1
  dx = 1000.0; dy = 1000.0; dz = 100.0
  tsmall = 0.0001
  nrain = 1
  td_cond = 0; td_evac = 0; td_evar = 0; td_melt = 0; td_frz = 0; td_dep = 0; td_subl = 0
  qd_cond = 0; qd_evac = 0; qd_evar = 1; qd_dep = 0; qd_subl = 0; qd_dbz = 0
  qd_qcsed = 0; qd_qised = 0; qd_qssed = 0; qd_qrsed = 2; qd_qgsed = 0
  eqtset = 2
  axisymm = 0
  radopt = 0
  ihail = 0
  ndcnst = 100.0
  brkup_db = 0.0
!SETTINGS
  allocate(t3d(1,1,levels), pii(1,1,levels), qv(1,1,levels), qc(1,1,levels), qr(1,1,levels), qi(1,1,levels))
  allocate(qs(1,1,levels), qg(1,1,levels), nni(1,1,levels), ns(1,1,levels), nr(1,1,levels), ng(1,1,levels))
  allocate(nc(1,1,levels), p(1,1,levels), rho(1,1,levels), ddz(1,1,levels), w(1,1,levels+1), rmh(1,1,levels))
  allocate(rr(1,1,levels), vtc(1,1,levels), vtr(1,1,levels), vti(1,1,levels), vts(1,1,levels), vtg(1,1,levels))
  allocate(effc(1,1,1), effi(1,1,1), effs(1,1,1), effr(1,1,1), effg(1,1,1), effis(1,1,1))
  allocate(rainnc(1,1,1), prate(1,1), tdiag(1,1,1,1), qdiag(1,1,levels,2), out3d(1,1,1,1), ruh(1), rvh(1))
  do k = 1, levels
    read(*,*) t3d(1,1,k), p(1,1,k), rho(1,1,k), ddz(1,1,k), qv(1,1,k), qc(1,1,k), qr(1,1,k), qi(1,1,k), qs(1,1,k), &
              qg(1,1,k), nni(1,1,k), ns(1,1,k), nr(1,1,k), ng(1,1,k)
  enddo
  pii = (p*1.0e-5)**(287.04/1005.7)
  nc = 0.0; w = 0.0; rmh = 1.0; rr = rho; ruh = 1.0; rvh = 1.0
  vtc = 0.0; vtr = 0.0; vti = 0.0; vts = 0.0; vtg = 0.0
  rainnc = 0.0; prate = 0.0; tdiag = 0.0; qdiag = 0.0; out3d = 0.0
  tcond = 0.0d0; tevac = 0.0d0; tevar = 0.0d0; train = 0.0d0
  inum_flag = 1
  call graupel_init(cm1hail=ihail, cm1inum=inum_flag, cm1ndcnst=ndcnst, cm1db=brkup_db)
  write(*,'(a)') 'COLUMN'
  do n = 1, steps
    call mp_graupel(n, t3d, pii, qv, qc, qr, qi, qs, qg, nni, ns, nr, ng, nc, p, rho, step_s, ddz, w, rainnc, prate, &
                    effc, effi, effs, effr, effg, effis, tcond, tevac, tevar, train, ruh, rvh, rmh, rr, .false.,    &
                    vtc, vtr, vti, vts, vtg, .true., .true., .true., .false., .false., .true., tdiag, qdiag, out3d)
  enddo
  call show('t', t3d(1,1,:)); call show('qv', qv(1,1,:)); call show('qc', qc(1,1,:)); call show('qr', qr(1,1,:))
  call show('qi', qi(1,1,:)); call show('qs', qs(1,1,:)); call show('qg', qg(1,1,:)); call show('ni', nni(1,1,:))
  call show('ns', ns(1,1,:)); call show('nr', nr(1,1,:)); call show('ng', ng(1,1,:)); call show('vtr', vtr(1,1,:))
  call show('vts', vts(1,1,:)); call show('vtg', vtg(1,1,:)); call show('evap', qdiag(1,1,:,1))
  call show('qrsed', qdiag(1,1,:,2)); call show('rain', rainnc(1,1,:)); call show('prate', prate(1,:))
contains
  subroutine show(name, values)
    ! each value's bits, in hexadecimal
    character(len=*), intent(in) :: name
    real, intent(in) :: values(:)
    write(*,'(a,*(1x,z8.8))') name, values
  end subroutine show
end program rain_column

subroutine stopcm1
  ! CM1's stop, which the scheme's saturation adjustment calls on a failure
  stop 'stopcm1'
end subroutine stopcm1
"""
# What the driver hands the scheme of each point of the series: nothing before the two patches, then each patch's own.
TAKES = {PATCH_02: '', PATCH_03: '  brkup_gscale = limits_switch; brkup_rhor = density_ratio; brkup_rhoexp = exponent'}
TAKES[PATCH_04] = TAKES[PATCH_03] + '\n  rain_fall_law = law_switch; rain_selfcoll = collection_rate'


@pytest.fixture(scope='module')
def moon():
    """The Open Moon's settings from its air at 2 m, Terluna's resort climate (test_rain_fall_law.py)."""
    world = drops.Column(gravity_m_s2=MOON_G, surface_pressure_pa=121590.0, surface_temperature_k=300.4274941880408,
                         surface_relative_humidity=0.6083150136678477, air=earthlike_air(121590.0, 400.0))
    return fall_law.settings(world)


@pytest.fixture(scope='module')
def columns(cm1_series, moon, tmp_path_factory):
    """The column's executable from the series through the lab's patch 02, 03 and 04, under each flag set: six builds
    of input.F, constants.F and morrison.F with the driver, about 0.7 MB each, with the Open Moon's table beside the
    builds that read one."""
    if shutil.which('gfortran') is None or shutil.which('cpp') is None:
        pytest.skip('gfortran or cpp is missing')
    built = {}
    for through in POINTS:
        for name, flags in FLAGS.items():
            folder = tmp_path_factory.mktemp('column')
            for source in ('input', 'constants', 'morrison'):
                (folder / f'{source}.F').write_text(cm1_series.source(f'{source}.F', through), encoding='latin-1')
                text = subprocess.run([*CPP, f'{source}.F'], cwd=folder, check=True, capture_output=True,
                                      encoding='latin-1').stdout
                (folder / f'{source}.f90').write_text(text, encoding='latin-1')
            (folder / 'driver.f90').write_text(DRIVER.replace('!SETTINGS', TAKES[through]))
            subprocess.run(['gfortran', *flags, 'input.f90', 'constants.f90', 'morrison.f90', 'driver.f90', '-o',
                            'column'], cwd=folder, check=True, capture_output=True)
            if through == PATCH_04:
                (folder / fall_law.TABLE_FILE).write_text(fall_law.table_text(moon['table']))
            built[through, name] = folder / 'column'
    return built


def run(exe, rows, steps, step_s, gravity, settings=OFF, cwd=None):
    """The column after its steps: what the scheme printed as it began, and each field's bits by level. settings are
    the limits' three entries of &param3 and the law's two, which a scheme from before a patch leaves unread."""
    text = (f'{len(rows)} {steps} {step_s!r} {gravity!r}\n' + ''.join(' '.join(map(str, s)) + '\n' for s in settings)
            + ''.join(' '.join(repr(float(x)) for x in row) + '\n' for row in rows))
    done = subprocess.run([str(exe)], input=text, capture_output=True, text=True, cwd=cwd or exe.parent,
                          env={**os.environ, 'OMP_NUM_THREADS': '1'})
    if done.returncode or 'COLUMN\n' not in done.stdout:               # gfortran's STOP with a message returns 0
        raise RuntimeError(done.stdout[-600:] + done.stderr[-600:])
    head, _, body = done.stdout.partition('COLUMN\n')
    return head, {line.split()[0]: line.split()[1:] for line in body.splitlines()}


def values(words):
    return np.array([struct.unpack('>f', bytes.fromhex(word))[0] for word in words])


def saturation(t):
    return 611.2 * math.exp(17.67 * (t - 273.15) / (t - 29.65))


def number(q, mean_diameter_m):
    """Drops per kg of air in an exponential spectrum of a mean diameter 1/lambda with q kg/kg of water."""
    return q / (math.pi * WATER * mean_diameter_m**3)


def level(t, p, humidity, dz=250.0, qc=0.0, qr=0.0, qi=0.0, qs=0.0, qg=0.0, ni=0.0, ns=0.0, ng=0.0, rain_mean_m=None):
    """One level of a column as the driver reads it: its air, with vapour at a relative humidity, and its water."""
    e = humidity * saturation(t)
    qv = 0.622 * e / (p - e)
    rho = p / (RD * t * (1 + 0.608 * qv))
    return (t, p, rho, dz, qv, qc, qr, qi, qs, qg, ni, ns, number(qr, rain_mean_m) if qr else 0.0, ng)


def storm():
    """Forty levels of 250 m with rain from the ground to 7 km, cloud water from 2 to 6 km, snow and graupel from 3 to
    9 km and cloud ice above 6 km, in air that cools 6.5 K/km from 300 K: rain meets snow and graupel above and below
    the melting level, breaks up on both sides of it and evaporates below the cloud and in the dry layer aloft. On
    this column each statement the two patches add or change in the column routine runs in the setting that selects
    it, the defaults or the switches on (checked once with gcov, models/cm1/README.md)."""
    rows = []
    for k in range(40):
        z = (k + 0.5) * 250.0
        t = 300.0 - 6.5e-3 * z
        rows.append(level(t, 101325.0 * math.exp(-z / 8000.0), 0.7 if z < 2000 else 1.0 if z < 5000 else 0.9 if z < 8000 else 0.6,
                          qc=0.5e-3 if 2000 <= z < 6000 else 0.0, qr=1.0e-3 if z < 7000 else 0.0,
                          qi=0.1e-3 if z >= 6000 else 0.0, qs=0.5e-3 if 3000 <= z < 9000 else 0.0,
                          qg=0.5e-3 if 3000 <= z < 9000 else 0.0, ni=1.0e5 if z >= 6000 else 0.0,
                          ns=1.0e4 if 3000 <= z < 9000 else 0.0, ng=1.0e3 if 3000 <= z < 9000 else 0.0,
                          rain_mean_m=0.5e-3 if t >= 273.15 else 1.0e-3))
    return rows


def random_column(rng):
    """Thirty levels of air and water drawn at random: each kind of water present in seven levels of ten."""
    surface_k, lapse = rng.uniform(275.0, 310.0), rng.uniform(2.0e-3, 9.0e-3)
    surface_pa, scale, dz = rng.uniform(6.0e4, 1.6e5), rng.uniform(6.0e3, 6.0e4), rng.uniform(100.0, 800.0)
    rows = []
    for k in range(30):
        z = (k + 0.5) * dz
        some = lambda top: 10.0**rng.uniform(-7, top) if rng.random() < 0.7 else 0.0
        qc, qr, qi, qs, qg = some(-2.7), some(-2.3), some(-3.5), some(-2.7), some(-2.5)
        rows.append(level(max(surface_k - lapse * z, 215.0), surface_pa * math.exp(-z / scale), rng.uniform(0.3, 1.05), dz,
                          qc, qr, qi, qs, qg, 10.0**rng.uniform(3, 6) if qi else 0.0,
                          10.0**rng.uniform(2, 5) if qs else 0.0, 10.0**rng.uniform(1, 4) if qg else 0.0,
                          rain_mean_m=10.0**rng.uniform(-4.7, -1.9)))
    return rows


def uniform(mean_diameter_m, humidity, levels, dz=250.0, t=290.0, rain=1.0e-3):
    """Levels of the same air at 1.2 atm, each with the same rain."""
    return [level(t, 121590.0, humidity, dz, qr=rain, rain_mean_m=mean_diameter_m) for _ in range(levels)]


def mean_diameter(fields):
    return (values(fields['qr']) / (math.pi * WATER * values(fields['nr'])))**(1.0 / 3.0)


# The patches' texts.

def test_the_two_patches_follow_the_labs_series(cm1_series):
    assert cm1_series.names[-4:] == ['patches/lab/01-the-simple-boundary-layers-tendencies-per-unit-mass.patch', PATCH_02,
                                     PATCH_03, PATCH_04]
    for patch in (PATCH_03, PATCH_04):
        text = (cm1_series.folder / patch).read_text()
        assert re.findall(r'^\+\+\+ b/src/(\S+)', text, flags=re.M) == ['cm1.F', 'input.F', 'morrison.F', 'param.F']
        for line in cm1_series.added(patch):                       # every added line marked, or inside a marked block
            assert len(line) <= 120, line
        for macro in ('TERLUNA_G', 'TERLUNA_CO2', 'TERLUNA_O2', '//', '/*', '#'):     # cpp would read these
            assert not any(macro in line for line in cm1_series.added(patch)), macro
    cm1, inputs, param = (cm1_series.source(name, PATCH_04) for name in ('cm1.F', 'input.F', 'param.F'))
    for default in ('      brkup_gscale = 0 ', '      brkup_rhor = 1.0 ', '      brkup_rhoexp = 0.0 ', '      rain_fall_law = 0 ',
                    '      rain_selfcoll = 0.0 '):
        assert cm1.count(default) == 1, default
    assert '                        brkup_gscale,brkup_rhor,brkup_rhoexp,rain_fall_law,rain_selfcoll, &\n' in inputs
    assert inputs.count('      integer :: brkup_gscale ') == 1 and inputs.count('      integer :: rain_fall_law ') == 1
    assert inputs.count('      real :: brkup_rhor,brkup_rhoexp ') == 1 and inputs.count('      real :: rain_selfcoll ') == 1
    assert param.count('MPI_BCAST(brkup_') == 4 and param.count('MPI_BCAST(rain_') == 2      # brkup_db is CM1's own
    for name in ('brkup_gscale', 'brkup_rhor', 'brkup_rhoexp', 'rain_fall_law', 'rain_selfcoll'):
        assert param.count(f"      if(dowr) write(outfile,*) '{name} =',{name}  ! Lab\n") == 1, name


def test_the_limits_patch_keeps_cm1s_statements(cm1_series):
    before, after = (cm1_series.source('morrison.F', patch) for patch in (PATCH_02, PATCH_03))
    # CM1's own lines, with core patch 04's cap, stay as they were.
    for line in ('         LAMMAXR = 1./20.E-6\n', '         LAMMINR = 1./2800.E-6\n',
                 '         cm1db = 300.e-6  ! default cutoff diameter for breakup\n',
                 '         D_b = cm1db  ! cutoff diameter for breakup\n',
                 '         VCAPR = 9.1*(G/9.81)**((BR+1.)/3.)\n'):
        assert before.count(line) == 1 and after.count(line) == 1, line
    # Outside the IF on brkup_gscale = 1 the added block sets the rate alone, to CM1's 2300; inside, the four limits.
    start = after.index("         ! Lab: rain's limits at the build's gravity")
    block = after[start:after.index('\n\n', start)]
    outside = re.sub(r'IF \(brkup_gscale\.EQ\.1\) THEN.*?END IF', '', block, flags=re.S)
    assert [line.strip() for line in outside.splitlines() if re.match(r'^\s+[A-Za-z_]\w* =', line)] == ['KB_r = 2300.']
    inside = block[block.index('IF (brkup_gscale.EQ.1) THEN'):block.index('END IF')]
    for expression in ('lab_scap = SQRT(9.81/G)', 'lab_scol = lab_scap*brkup_rhor**brkup_rhoexp', 'D_b = D_b*lab_scol',
                       'KB_r = KB_r/lab_scol', 'LAMMINR = LAMMINR/lab_scap', 'VCAPR = 9.1*(G/9.81)**0.25'):
        assert expression in inside, expression
    assert "STOP 'Lab rain limits: brkup_rhor must be positive'" in inside
    assert "STOP 'Lab rain limits: brkup_gscale must be 0 or 1'" in block[block.index('ELSE IF (brkup_gscale.NE.0) THEN'):]
    # The breakup law reads the rate in CM1's own expression, in the warm branch and the cold.
    assert before.count('            dum=2.-exp(2300.*(1./lamr(k)-dum1))\n') == 2 and 'exp(2300.' not in after
    assert after.count('            dum=2.-exp(KB_r*(1./lamr(k)-dum1))   ! Lab') == 2
    # Every other line of the scheme is the one before the patch.
    kept = set(after.splitlines())
    assert {line for line in before.splitlines() if line not in kept} == {'            dum=2.-exp(2300.*(1./lamr(k)-dum1))'}


def test_the_law_patch_keeps_cm1s_statements(cm1_series):
    before, after = (cm1_series.source('morrison.F', patch) for patch in (PATCH_03, PATCH_04))
    epsr = ('        EPSR = 2.*PI*N0RR(K)*RHO(K)*DV(K)*                           &\n'
            '                   (F1R/(LAMR(K)*LAMR(K))+                       &\n'
            '                    F2R*(ARN(K)*RHO(K)/MU(K))**0.5*                      &\n'
            '                    SC(K)**(1./3.)*CONS9/                   &\n'
            '                (LAMR(K)**CONS34))\n')
    sediment = '      UNR = ARN(K)*CONS6/DLAMR**BR\n      UMR = ARN(K)*CONS4/(DLAMR**BR)\n'
    # CM1's expressions for the evaporation and the sedimentation are the branch the default takes.
    for expression, count in ((epsr, 2), (sediment, 1)):
        assert before.count(expression) == count and after.count(expression) == count, expression
    assert after.count('IF (LAB_RLAW) THEN') == 5                  # the slope twice, the evaporation twice, the fall
    # The speeds of the collection by snow and graupel: CM1's two expressions, each written four times before, are
    # written twice after, where rain's slope is set above freezing and below, and the four places read what was set.
    for old, new, kept in (('ARN(K)*CONS4/(LAMR(K)**BR)', 'UMR = LAB_UMR(K)', '      LAB_UMR(K) = ARN(K)*CONS4/(LAMR(K)**BR)\n'),
                           ('ARN(K)*CONS6/LAMR(K)**BR', 'UNR = LAB_UNR(K)', '      LAB_UNR(K) = ARN(K)*CONS6/LAMR(K)**BR\n')):
        assert before.count(old) == 4 and after.count(old) == 2 and after.count(kept) == 2, old
        assert after.count(f'            {new}   ! Lab: set with rain\'s slope\n') == 4, new
    # The collection's blocks contain no branch of the patch, from their speeds to the next block's test.
    for start in ('            UMR = LAB_UMR(K)',):
        for block in after.split(start)[1:]:
            assert 'LAB_RLAW' not in block[:block.index('         IF (QR3D(K).GE.1.E-8')]
    # The self-collection rate is CM1's unless the namelist gives one, and the table is read only when asked for.
    start = after.index("         ! Lab: rain's fall law and self-collection for the world")
    block = after[start:after.index('\n\n', start)]
    assert block.index('KSC_r = 5.78') < block.index('IF (rain_selfcoll.GT.0.) KSC_r = rain_selfcoll')
    assert 'LAB_RLAW = .TRUE.' in block[block.index('IF (rain_fall_law.EQ.1'):block.index('ELSE IF')]
    assert '     LOGICAL, PRIVATE ::   LAB_RLAW = .FALSE.' in after
    assert before.count('            nragg(k) = -5.78*dum*qr3d(k)*nr3d(k)*rho(k)\n') == 2 and '-5.78*dum' not in after
    assert after.count('            nragg(k) = -KSC_r*dum*qr3d(k)*nr3d(k)*rho(k)   ! Lab') == 2
    # Autoconversion and accretion are unchanged, Khairoutdinov and Kogan's and Seifert and Beheng's.
    for line in ('           PRA(K) = 67.*(DUM)**1.15\n', '           pra(k) = 5.78e3*rho(k)/1000.*qc3d(k)*qr3d(k)*dum1\n'):
        assert before.count(line) == after.count(line) == 2, line


# One column of the patched scheme.

def test_a_column_keeps_its_bits_at_the_defaults(columns):
    """The storm column over 100 steps of 6 s and twelve random columns over 20 steps of 10 s, at the Moon's gravity
    and CM1's own: with the switches at their defaults the scheme after each patch returns every field bit for bit as
    the scheme before the two, under CM1's flags and under -O3 -march=native."""
    rng = random.Random(20261111)
    cases = [(storm(), 100, 6.0)] + [(random_column(rng), 20, 10.0) for _ in range(12)]
    for flags in FLAGS:
        for gravity in (MOON_G, EARTH_G):
            for rows, steps, step_s in cases:
                before = run(columns[PATCH_02, flags], rows, steps, step_s, gravity)[1]
                assert len(before) == 18 and all(len(words) in (1, len(rows)) for words in before.values())
                for patch in (PATCH_03, PATCH_04):
                    assert run(columns[patch, flags], rows, steps, step_s, gravity)[1] == before, (flags, gravity, patch)
    # The storm rains, and the switches move it: the identity above is of a column in which the patched lines act.
    off, on = (run(columns[PATCH_04, 'cm1'], storm(), 100, 6.0, MOON_G, settings)[1] for settings in (OFF, LUNAR))
    assert values(off['rain'])[0] > 0.1 and values(on['rain'])[0] > 1.2 * values(off['rain'])[0]
    assert all(on[name] != off[name] for name in ('qr', 'nr', 'vtr', 'evap', 'qs', 'qg', 't'))


def test_switched_on_in_earths_air_at_cm1s_gravity_the_limits_are_cm1s(columns):
    """At 9.81 m/s2 with the density ratio 1 the scaled limits are CM1's own to the bit, whatever the exponent."""
    exe = columns[PATCH_04, 'cm1']
    head, own = run(exe, storm(), 100, 6.0, EARTH_G)
    scaled_head, scaled = run(exe, storm(), 100, 6.0, EARTH_G, ((1, 1.0, 0.71), (0, 0.0)))
    assert scaled == own
    assert 'brkup_gscale           1' in scaled_head and 'brkup_gscale           0' in head


def printed(head, label):
    """The numbers CM1 prints on a line of the scheme's start."""
    line = next(line for line in head.splitlines() if label in line)
    return [float(x) for x in re.findall(r'-?\d+\.\d*(?:E[+-]\d+)?', line.split(label)[1])]


def test_the_limits_cm1_sets_are_the_pythons(columns):
    exe = columns[PATCH_04, 'cm1']
    for gravity, settings, scaled in ((MOON_G, OFF, False), (MOON_G, LUNAR_LIMITS, True), (EARTH_G, OFF, False),
                                      (3.7, ((1, 1.5, 0.6), (0, 0.0)), True)):
        head = run(exe, storm()[:2], 1, 1.0, gravity, settings)[0]
        ratio, exponent = settings[0][1:]
        want = breakup.limits(gravity, ratio, exponent, scaled=scaled)
        found = printed(head, 'D_b')
        assert found == pytest.approx([want['breakup_cutoff_m'], want['breakup_rate_per_m'], want['mean_diameter_cap_m'],
                                       want['fall_speed_cap_m_s']], rel=2e-6), (gravity, settings)
    # The Open Moon's, as Terluna's numbers have them: breakup from 0.84 mm, a 6.88 mm cap, a 5.80 m/s fall-speed cap.
    found = printed(run(exe, storm()[:2], 1, 1.0, MOON_G, LUNAR_LIMITS)[0], 'D_b')
    assert [round(found[0] * 1e3, 2), round(found[2] * 1e3, 2), round(found[3], 2)] == [0.84, 6.88, 5.80]


def test_rain_settles_at_the_breakup_equilibrium(columns):
    """Sixty uniform levels of 500 m of rain in nearly saturated air, over 300 steps of 10 s: in the lowest ten levels,
    which the thinning from the top has yet to reach, self-collection and breakup bring the mean diameter to the
    equilibrium of the limits in force, from below it and from above."""
    exe = columns[PATCH_04, 'cm1']
    for settings, scaled in ((OFF, False), (LUNAR_LIMITS, True), (LUNAR, True)):
        want = breakup.limits(MOON_G, 1.2, 0.687, scaled=scaled)['equilibrium_m']
        for start_m in (0.4e-3, 2.5e-3):
            found = mean_diameter(run(exe, uniform(start_m, 0.95, 60, 500.0), 300, 10.0, MOON_G, settings)[1])[:10]
            assert found == pytest.approx(want, rel=1e-3), (settings, start_m)
    assert breakup.limits(MOON_G, scaled=False)['equilibrium_m'] == pytest.approx(0.6014e-3, abs=5e-8)
    assert breakup.limits(MOON_G, 1.2, 0.687)['equilibrium_m'] == pytest.approx(1.6751e-3, abs=5e-8)


def test_rain_falls_by_the_table_under_the_caps(columns, moon):
    """A ladder of mean diameters from 30 um to 9 mm, one step of 0.1 ms: the mass-weighted fall speed CM1 returns at
    each level is the power law's, or the table's with rain_fall_law = 1, times the density factor, under the cap in
    force; and a spectrum wider than the cap on the mean diameter comes back at the cap."""
    exe = columns[PATCH_04, 'cm1']
    means = np.geomspace(30.0e-6, 9.0e-3, 24)
    rows = [level(290.0, 121590.0, 0.8, qr=1.0e-3, rain_mean_m=m) for m in means]
    factor = morrison.density_factor(np.array([row[2] for row in rows]))
    power = morrison.FALL_COEFFICIENT * morrison.gravity_factor(MOON_G)
    for settings, scaled, table in ((OFF, False, False), (LUNAR_LIMITS, True, False), (LUNAR, True, True)):
        limits = breakup.limits(MOON_G, 1.2, 0.687, scaled=scaled)
        fields = run(exe, rows, 1, 1.0e-4, MOON_G, settings)[1]
        lam = 1.0 / np.clip(means, morrison.MEAN_DIAMETER_FLOOR, limits['mean_diameter_cap_m'])
        speed = (fall_law.interpolate(moon['table'], lam)[0] if table
                 else fall_law.closed_forms(power, morrison.FALL_EXPONENT, lam)[0])
        assert values(fields['vtr']) == pytest.approx(factor * np.minimum(speed, limits['fall_speed_cap_m_s']), rel=5e-6)
        assert np.any(speed > limits['fall_speed_cap_m_s']) and np.any(speed < limits['fall_speed_cap_m_s'])
        wide = means > limits['mean_diameter_cap_m']
        assert wide.sum() >= 2 and mean_diameter(fields)[wide] == pytest.approx(limits['mean_diameter_cap_m'], rel=2e-4)
        assert mean_diameter(fields)[~wide] == pytest.approx(means[~wide], rel=2e-4)
    # The table's water falls slower than the power law's in drizzle, faster at mean diameters near 0.5 mm, and slower
    # again in wide spectra, whose large drops the power law speeds without limit: 0.61, 1.20 and 0.69 of it at mean
    # diameters of 0.05, 0.5 and 3 mm.
    lam = 1.0 / np.array([0.05e-3, 0.5e-3, 3.0e-3])
    ratio = fall_law.interpolate(moon['table'], lam)[0] / fall_law.closed_forms(power, morrison.FALL_EXPONENT, lam)[0]
    assert ratio == pytest.approx([0.613, 1.197, 0.695], abs=2e-3)


def test_rains_water_and_drops_reach_the_level_below_at_their_two_speeds(columns, moon):
    """Rain of eight mean diameters from 50 um to 3 mm, each in one level of saturated air with an empty level below it
    and above, one step of 1 ms under the Open Moon's limits: the level below takes the water at the mass-weighted mean
    speed and the drops at the number-weighted, by hand A Gamma(4 + B) / 6 lambda^-B and A Gamma(1 + B) lambda^-B for
    the power law, or the table's first two moments with rain_fall_law = 1, each times the density factor under the
    cap. The two speeds differ by a factor of two or more at every diameter."""
    exe = columns[PATCH_04, 'cm1']
    step_s, dz = 1.0e-3, 250.0
    air = level(290.0, 121590.0, 1.0, dz)
    rows = [row for m in np.geomspace(50.0e-6, 3.0e-3, 8)
            for row in (air, level(290.0, 121590.0, 1.0, dz, qr=1.0e-3, rain_mean_m=m), air)]
    below, rainy, above = (slice(first, None, 3) for first in (0, 1, 2))
    factor = morrison.density_factor(air[2])
    power = morrison.FALL_COEFFICIENT * morrison.gravity_factor(MOON_G)
    cap = breakup.limits(MOON_G, 1.2, 0.687)['fall_speed_cap_m_s']
    for settings, table in ((LUNAR_LIMITS, False), (LUNAR, True)):
        fields = run(exe, rows, 1, step_s, MOON_G, settings)[1]
        water, number_ = values(fields['qr']), values(fields['nr'])
        lam = (math.pi * WATER * number_[rainy] / water[rainy])**(1.0 / 3.0)
        moments = (fall_law.interpolate(moon['table'], lam) if table
                   else fall_law.closed_forms(power, morrison.FALL_EXPONENT, lam))
        by_mass, by_number = (factor * np.minimum(moments[m], cap) * step_s / dz for m in (0, 1))
        # The rainy level kept 1 - share of what it had, so the level below took share / (1 - share) of what it kept.
        assert water[below] == pytest.approx(by_mass / (1.0 - by_mass) * water[rainy], rel=2e-5)
        assert number_[below] == pytest.approx(by_number / (1.0 - by_number) * number_[rainy], rel=2e-5)
        assert np.all(by_number < 0.5 * by_mass) and np.all(water[above] == 0.0)


def test_each_place_reads_its_own_moment_of_the_table(columns, tmp_path):
    """A table of the power law's own three moments, in closed form, in place of the solver's: over 1, 5 and 100 steps
    of the storm column the scheme returns the default's fields to 2 parts in 10^5 of each field's largest value. The
    slopes above freezing and below it, the sedimentation and the evaporation therefore each read the moment they
    need. With another moment at any one of those eight places a field departs by 6 parts in 10^3 or more, in a
    check run once (models/cm1/README.md)."""
    exe = columns[PATCH_04, 'cm1']
    lam = fall_law.table_lambda()
    closed = fall_law.closed_forms(morrison.FALL_COEFFICIENT * morrison.gravity_factor(MOON_G), morrison.FALL_EXPONENT, lam)
    first, last, points = fall_law.TABLE_LAMBDA
    table = dict(points=points, ln_lambda_first=math.log(first), ln_lambda_step=math.log(last / first) / (points - 1),
                 ln_mass_weighted=np.log(closed[0]), ln_number_weighted=np.log(closed[1]), ln_ventilation=np.log(closed[2]))
    (tmp_path / fall_law.TABLE_FILE).write_text(fall_law.table_text(table))
    for steps in (1, 5, 100):
        own = run(exe, storm(), steps, 6.0, MOON_G)[1]
        read = run(exe, storm(), steps, 6.0, MOON_G, ((0, 1.0, 0.0), (1, 0.0)), cwd=tmp_path)[1]
        for name in own:
            largest = np.abs(values(own[name])).max()
            assert np.abs(values(read[name]) - values(own[name])).max() <= 2e-5 * largest, (steps, name)
        assert values(own['rain'])[0] > 0 or steps < 100


def test_rain_evaporates_by_the_tables_ventilation(columns, moon):
    """Rain of twelve mean diameters in air at 60% humidity, above freezing and below, one step of 10 ms: the
    evaporation with the table over the evaporation with the power law is the ratio of the two ventilated sums,
    F1R / lambda^2 + F2R (factor rho / mu)^(1/2) Sc^(1/3) I, with I the table's integral or the power law's
    A^(1/2) Gamma(5/2 + B/2) / lambda^(5/2 + B/2), by hand with Morrison's viscosity and diffusivity."""
    exe = columns[PATCH_04, 'cm1']
    means = np.geomspace(60.0e-6, 5.0e-3, 12)
    f1, f2 = morrison.VENTILATION
    power, b = morrison.FALL_COEFFICIENT * morrison.gravity_factor(MOON_G), morrison.FALL_EXPONENT
    for t in (290.0, 265.0):
        rows = [level(t, 121590.0, 0.6, qr=1.0e-3, rain_mean_m=m) for m in means]
        law, table = (values(run(exe, rows, 1, 0.01, MOON_G, settings)[1]['evap'])
                      for settings in (LUNAR_LIMITS, ((1, 1.2, 0.687), (1, 0.0))))
        rho = np.array([row[2] for row in rows])
        lam = (math.pi * WATER * np.array([row[12] for row in rows]) / 1.0e-3)**(1.0 / 3.0)
        mu = 1.496e-6 * t**1.5 / (t + 120.0)                           # morrison.F's MU, DV and SC
        schmidt = mu / (rho * 8.794e-5 * t**1.81 / 121590.0)
        factor = morrison.density_factor(rho)
        own = f1 / lam**2 + (f2 * np.sqrt(factor * power * rho / mu) * schmidt**(1.0 / 3.0)
                             * math.gamma(2.5 + b / 2) / lam**(2.5 + b / 2))
        new = f1 / lam**2 + (f2 * np.sqrt(factor * rho / mu) * schmidt**(1.0 / 3.0)
                             * fall_law.interpolate(moon['table'], lam)[2])
        assert np.all(law > 0) and table / law == pytest.approx(new / own, rel=2e-5)
        assert (table / law).min() < 0.9 and (table / law).max() > 1.05


def test_rain_collects_itself_at_the_namelists_rate(columns):
    """Twelve uniform levels of rain below the breakup cutoff, one step of 1 s: between CM1's 5.78 m3/kg/s and the
    Open Moon's 2.919 the drops lost differ by the step times the rates' difference times rho q N, by hand."""
    exe = columns[PATCH_04, 'cm1']
    rows = uniform(0.2e-3, 0.9, 12)
    own, lunar = (values(run(exe, rows, 1, 1.0, MOON_G, ((0, 1.0, 0.0), (0, rate)))[1]['nr']) for rate in (0.0, 2.919))
    hand = 1.0 * (5.78 - 2.919) * rows[0][2] * 1.0e-3 * rows[0][12]              # 0.42% of the 39,908 drops per kg
    assert (lunar - own)[:10] == pytest.approx(hand, rel=1e-4) and hand / rows[0][12] == pytest.approx(4.16e-3, rel=5e-3)
    head = run(exe, rows, 1, 1.0, MOON_G, ((0, 1.0, 0.0), (0, 2.919)))[0]
    assert printed(head, 'self-collection') == pytest.approx([2.919], rel=1e-6)


def test_settings_cm1_cannot_take_stop_the_run(columns, moon, tmp_path):
    exe = columns[PATCH_04, 'cm1']
    rows = uniform(0.5e-3, 0.9, 2)
    with pytest.raises(RuntimeError, match='brkup_rhor must be positive'):
        run(exe, rows, 1, 1.0, MOON_G, ((1, 0.0, 0.687), (0, 0.0)))
    with pytest.raises(RuntimeError, match='brkup_gscale must be 0 or 1'):
        run(exe, rows, 1, 1.0, MOON_G, ((2, 1.2, 0.687), (0, 0.0)))
    with pytest.raises(RuntimeError, match='rain_fall_law must be 0 or 1'):
        run(exe, rows, 1, 1.0, MOON_G, ((0, 1.0, 0.0), (2, 0.0)))
    with pytest.raises(RuntimeError, match='lab_rain_law.txt'):             # a folder without the table
        run(exe, rows, 1, 1.0, MOON_G, LUNAR, cwd=tmp_path)
    # A table of one row, and one whose step in ln lambda is zero, each with its first row's three logs.
    for header in ('1 4.605170186e+00 2.302585093e-02', '3 4.605170186e+00 0.000000000e+00'):
        (tmp_path / fall_law.TABLE_FILE).write_text(header + '\n' + int(header.split()[0]) * '1.8 1.5 -10.3\n')
        with pytest.raises(RuntimeError, match='two rows or more and a positive step'):
            run(exe, rows, 1, 1.0, MOON_G, LUNAR, cwd=tmp_path)
    # With the Open Moon's table the scheme prints the three moments it reads at a slope of 1000/m: 3.763 and
    # 1.184 m/s in the reference air, and 6.661e-8 m3 s^-1/2.
    head = run(exe, rows, 1, 1.0, MOON_G, LUNAR)[0]
    assert 'table rows         301' in head
    assert printed(head, 'at lambda 1000/m: UMR') == pytest.approx(
        fall_law.interpolate(moon['table'], np.array([1000.0]))[:, 0], rel=1e-6)
    assert printed(head, 'at lambda 1000/m: UMR') == pytest.approx([3.7632478, 1.1841879, 6.6606509e-08], rel=1e-6)
