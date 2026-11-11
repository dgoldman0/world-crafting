"""Beljaars's gust in PlaSim's surface transfer (climate/gcm/surface_gust.py and patch 12 of models/exoplasim/patches):
its depth follows the bulk Richardson rule, by hand arithmetic, and its convective velocity vanishes in stable air; on
one column in sigma the depth goes as 1/g and the velocity keeps its value from Earth's gravity to the Moon's; the
Python copy gives the numbers Terluna's module gives; PlaSim's surflx with the patch, taken from the series applied to
the pinned source and compiled with ExoPlaSim's flags against a stub of PlaSim's module, gives the Python copy's transfer
to 1e-10 on lunar and Earth-like columns over water and land, unstable, calm, windy, stable and neutral; with the switch
off it prints every digit the unpatched surflx prints; the patch declares, reads and broadcasts each name once; and the
patched fluxmod.f90 compiles with PlaSim's modules.

Brought from Terluna's climate/tests/test_surface_gust.py at 39c5ee04 (python/provenance.json): the Fortran comes from
the lab's patch series, where Terluna's came from its runner's edit lists."""
import re
import shutil
import subprocess

import numpy as np
import pytest

from climate.gcm import surface_gust as sg

GUST_PATCH = '12-surface-gust.patch'    # in models/exoplasim/patches; conftest.py's series_sources applies the series
# ExoPlaSim's own compile flags (most_compiler's MOST_F90_OPTS, with compile.sh's double precision)
GCM_FLAGS = ('-O3', '-cpp', '-fcheck=all', '-ffpe-trap=invalid,zero,overflow', '-ffpe-summary=none',
             '-finit-real=zero', '-fdefault-real-8')
FORTRAN = pytest.mark.skipif(shutil.which('gfortran') is None, reason='the test takes gfortran')
G_MOON = 1.6242188765608128
LUNAR = dict(ga=G_MOON, gascon=288.3767, acpd=288.3767 / 0.286, rdbrv=288.3767 / 461.51, ADV=0.8546)
EARTH = dict(ga=9.80665, gascon=287.05, acpd=1004.6, rdbrv=287.05 / 461.51, ADV=0.8608)
ALV = 2.5008e6
num = lambda xs: ' '.join(repr(float(x)) for x in np.atleast_1d(xs))


# ------------------------------------------------------------------------------------------------------- levels

def plasim_half(levels: int = 10) -> np.ndarray:
    """PlaSim's own half levels (initpm's last branch), the top layer's bottom first, ending at 1."""
    s = np.arange(1, levels + 1) / levels
    return 0.75 * s + 1.75 * s ** 3 - 1.5 * s ** 4


# Terluna's fifteen half levels for the Moon, its lowest full level near 0.3 km (climate/gcm/levels.py at 39c5ee04,
# 'l15'): PlaSim's own six upper ones, six from 15.5 km down to 3.1 km, PlaSim's ninth, and one at sigma 0.9883.
HALF15 = np.r_[plasim_half()[:6], 0.7379, 0.7981, 0.8382, 0.8717, 0.9066, 0.9410, plasim_half()[8], 0.9883, 1.0]


# ------------------------------------------------------------------------------------------------------- the source

def surflx(text, last='surflx'):
    start = text.index('      subroutine surflx\n')
    end = text.index(f'      end subroutine {last}\n') + len(f'      end subroutine {last}\n')
    return text[start:end]


def module_additions(patched: str, pristine: str) -> str:
    """The lines a patched fluxmod.f90 adds to the module's own part, its declarations, in order."""
    part = lambda text: text[:text.index('      end module fluxmod\n')].splitlines(keepends=True)
    old = part(pristine)
    return ''.join(line for line in part(patched) if line not in old)


# ------------------------------------------------------------------------------------------------------- columns

def column(c, half, ps_pa, theta, zi, lapse, q_bl, wind, dts, dls, dz0, shf, lhf, ust, seed):
    """One of PlaSim's columns as surflx finds it: a mixed layer zi deep at potential temperature theta, stable lapse
    K/m above, vapour q_bl in the mixed layer falling above, the wind at the lowest level wind m/s, the surface dts K
    warmer than the lowest level's air (in potential temperature), and the surface fluxes of the step before: sensible
    and latent heat shf and lhf (W/m2, upward) and u* ust."""
    rng = np.random.default_rng(seed)
    sigma = sg.full_sigma(half)
    akap = c['gascon'] / c['acpd']
    z = -c['gascon'] * 280.0 / c['ga'] * np.log(sigma)
    th = np.where(z < zi, theta, theta + lapse * (z - zi)) + rng.normal(0.0, 0.05, z.size)
    t = th * sigma ** akap
    q = np.where(z < zi, q_bl, q_bl * np.exp(-(z - zi) / 2500.0)) * (1.0 + rng.normal(0.0, 0.01, z.size))
    u = wind + 1.0e-3 * z + rng.normal(0.0, 0.3, z.size)
    u[-1] = wind
    v = rng.normal(0.0, 0.8, z.size)
    v[-1] = 0.0
    ts = th[-1] + dts                                   # theta is referred to the ground, where sigma is 1
    qs = 0.622 * 610.78 * np.exp(17.27 * (ts - 273.16) / (ts - 35.86)) / ps_pa
    rho = ps_pa / (c['gascon'] * ts)
    return dict(dt=np.r_[t, ts], dq=np.r_[q, qs if dls < 1.0 else 0.5 * qs], du=u, dv=v, dz0=dz0, dls=dls, dp=ps_pa,
                dshfl=-shf * max(1.0, 1.0 + c['ADV'] * q[-1]), devap=-lhf / (ALV * 1000.0), dust3=ust ** 3, rho=rho)


def cases():
    """(constants, half levels, columns): lunar on fifteen levels and on forty equal ones, and Earth-like on PlaSim's
    ten; over the sea unstable, calm, windy, stable and with last step's fluxes downward though the air is unstable;
    over land a convective day, a calm stable night with the wind below every floor, and neutral air."""
    half10 = plasim_half()
    equal40 = np.linspace(1.0, 40.0, 40) / 40.0
    sets = []
    for c, half, ps_pa, zi in ((LUNAR, HALF15, 121590.0, 4000.0), (LUNAR, equal40, 121590.0, 3000.0),
                               (EARTH, half10, 101325.0, 900.0)):
        rows = [  # theta, q, wind, dts, dls, dz0, shf, lhf, u*
            (299.0, 0.012, 3.0, 2.7, 0.0, 2.0e-4, 9.0, 110.0, 0.10),
            (299.0, 0.013, 0.2, 3.0, 0.0, 1.5e-5, 6.0, 60.0, 0.02),
            (299.0, 0.011, 9.0, 1.5, 0.0, 1.0e-3, 12.0, 220.0, 0.35),
            (301.0, 0.014, 1.5, -1.0, 0.0, 1.0e-4, -3.0, 5.0, 0.05),
            (299.0, 0.012, 0.6, 1.0, 0.0, 1.0e-4, -2.0, -1.0, 0.03),
            (300.0, 0.010, 2.0, 6.0, 1.0, 0.1, 40.0, 150.0, 0.25),
            (300.0, 0.006, 0.05, -5.0, 1.0, 0.1, -5.0, 2.0, 0.01),
            (300.0, 0.008, 4.0, 0.0, 1.0, 0.05, 0.0, 30.0, 0.2),
        ]
        cols = [column(c, half, ps_pa + 200.0 * j, th, zi * (0.7 + 0.1 * j), 1.0e-3, q, w, dts, dls, dz0, shf, lhf, ust,
                       seed=j) for j, (th, q, w, dts, dls, dz0, shf, lhf, ust) in enumerate(rows)]
        sets.append((c, half, cols))
    return sets


# One column written out, for the numbers pinned from Terluna's module and the arithmetic by hand.
PIN_HALF = np.array([0.2, 0.5, 0.75, 0.9, 0.97, 1.0])
PIN_THETA = np.array([330.0, 315.0, 304.0, 300.4, 300.0, 300.1])
PIN_Q = np.array([1.0e-5, 5.0e-4, 4.0e-3, 9.0e-3, 1.1e-2, 1.2e-2])
PIN_U = np.array([20.0, 12.0, 6.0, 4.5, 3.5, 3.0])
PIN_V = np.array([0.0, 1.0, -1.0, 0.5, 0.2, 0.0])


def pinned_column(c, ps_pa):
    """The written-out column over water: 9.5 W/m2 of sensible heat and 4.4e-8 m/s of evaporation the step before,
    u* 0.1 m/s, the sea at 302.5 K."""
    t = PIN_THETA * sg.full_sigma(PIN_HALF) ** (c['gascon'] / c['acpd'])
    return dict(dt=np.r_[t, 302.5], dq=np.r_[PIN_Q, 0.02], du=PIN_U, dv=PIN_V, dz0=2.0e-4, dls=0.0, dp=ps_pa,
                dshfl=-9.5, devap=-4.4e-8, dust3=1.0e-3)


def gust_of(x, half, c):
    n = half.size
    sigma = sg.full_sigma(half)
    s = sg.surface_from_plasim(x['dshfl'], x['devap'], x['dust3'], x['dt'][n], x['dp'], x['dq'][n - 1], c)
    return sg.gust_column(x['dt'][:n], x['dq'][:n], x['du'], x['dv'], sigma, half, s['wth0'], s['wq0'], s['ustar'], c), s


STUB = """
      module fluxmod
      integer, parameter :: NHOR={nhor}, NLEV={nlev}, NLEP={nlev}+1, NLEM={nlev}-1, NLON={nhor}, NLAT=1, NROOT=0
      real, parameter :: vonkarman=0.4
      real :: dt(NHOR,NLEP), dq(NHOR,NLEP), du(NHOR,NLEP), dv(NHOR,NLEP)
      real :: dtsa(NHOR), dz0(NHOR), dls(NHOR), dp(NHOR), dshfl(NHOR), devap(NHOR), dust3(NHOR)
      real :: dtransh(NHOR), dtransm(NHOR)
      real :: sigma(NLEV), sigmah(NLEV)
      real :: ga, gascon, akap, rdbrv, acpd, adv
      integer :: ntsa=2, nstress=0, nshfl=0, nevap=0, ntime=0, nprint=0, nprhor=1, nud=6, mypid=0
      real :: time4tr=0., time4st=0., time4sh=0., time4ev=0.
      real :: zumin=1., vdiff_lamm=160., vdiff_b=5., vdiff_c=5., vdiff_d=5.
{declarations}      end module fluxmod

      subroutine mksecond(a,b)
      real a,b
      end subroutine mksecond
      subroutine mpgagp(a,b,n)
      real a(*),b(*)
      integer n
      end subroutine mpgagp
      subroutine mkstress
      end subroutine mkstress
      subroutine mkshfl
      end subroutine mkshfl
      subroutine mkevap
      end subroutine mkevap
"""
HARNESS = """
      program harness
      use fluxmod
      implicit none
      integer :: jhor, jlev
      read(*,*) ga, gascon, akap, rdbrv, acpd, adv
      read(*,*) sigma, sigmah
      read(*,*) zumin{switch}
      do jhor=1,NHOR
       read(*,*) dp(jhor), dshfl(jhor), devap(jhor), dust3(jhor), dz0(jhor), dls(jhor)
       read(*,*) (dt(jhor,jlev), jlev=1,NLEP)
       read(*,*) (dq(jhor,jlev), jlev=1,NLEP)
       read(*,*) (du(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dv(jhor,jlev), jlev=1,NLEV)
      enddo
      call surflx
      do jhor=1,NHOR
       write(*,'(*(es25.16e3))') dtransh(jhor), dtransm(jhor), dtsa(jhor)
      enddo
      end program harness
"""


def compile_surflx(folder, code, nhor, nlev, declarations: str):
    """A harness of surflx against the stub of PlaSim's module, with the patch's own declarations where it has them."""
    folder.mkdir(parents=True, exist_ok=True)
    files = {'stub.f90': STUB.format(nhor=nhor, nlev=nlev, declarations=declarations), 'surflx.f90': code,
             'harness.f90': HARNESS.replace('{switch}', ', ngust, gust_beta, gust_umin' if declarations else '')}
    for name, text in files.items():
        (folder / name).write_text(text)
    subprocess.run(['gfortran', *GCM_FLAGS, '-o', 'harness', *files], cwd=folder, check=True, capture_output=True)
    return folder / 'harness'


def harness_input(c, half, cols, ngust=None):
    sigma = sg.full_sigma(half)
    akap = c['gascon'] / c['acpd']
    switch = '' if ngust is None else f' {int(ngust)} {sg.GUST_BETA!r} {sg.GUST_UMIN!r}'
    lines = [num([c['ga'], c['gascon'], akap, c['rdbrv'], c['acpd'], c['ADV']]), num(np.r_[sigma, half]),
             f'{sg.EXOPLASIM_ZUMIN!r}' + switch]
    for x in cols:
        lines.append(num([x['dp'], x['dshfl'], x['devap'], x['dust3'], x['dz0'], x['dls']]))
        lines += [num(x[k]) for k in ('dt', 'dq', 'du', 'dv')]
    return '\n'.join(lines) + '\n'


def run_harness(exe, text, ncols):
    rows = subprocess.run([str(exe)], input=text, capture_output=True, text=True, check=True).stdout.strip('\n')
    rows = rows.split('\n')
    assert len(rows) == ncols
    return rows


# ------------------------------------------------------------------------------------------------------- tests

def test_the_depth_follows_the_bulk_richardson_rule_and_the_gust_vanishes_in_stable_air():
    for c, ps_pa in ((LUNAR, 121590.0), (EARTH, 101325.0)):
        x = pinned_column(c, ps_pa)
        g, s = gust_of(x, PIN_HALF, c)
        # By hand, from the column as written: the heights, the fluxes, the two passes of the rule and w*.
        n, eps = PIN_HALF.size, 1.0 / c['rdbrv'] - 1.0
        sigma = sg.full_sigma(PIN_HALF)
        tv = x['dt'][:n] * (1.0 + eps * PIN_Q)
        thick = c['gascon'] * tv / c['ga'] * np.log(PIN_HALF / np.r_[1.0, PIN_HALF[:-1]])   # each layer's, the top's aside
        below = np.r_[np.cumsum(thick[:0:-1])[::-1], 0.0]                       # the layers' lower boundaries
        z = below + c['gascon'] * tv / c['ga'] * np.log(PIN_HALF / sigma)       # the full levels' heights
        thv = PIN_THETA * (1.0 + eps * PIN_Q)
        rho = ps_pa / (c['gascon'] * 302.5)
        wth = 9.5 / (rho * c['acpd'] * (1.0 + c['ADV'] * PIN_Q[-1]))
        wq = 1000.0 * 4.4e-8 / rho
        wthv = wth * (1.0 + eps * PIN_Q[-1]) + eps * PIN_THETA[-1] * wq
        assert (s['wth0'], s['wq0'], s['ustar']) == pytest.approx((wth, wq, 0.1), rel=1e-12)
        buoy = c['ga'] / thv[-1] * wthv

        def number(k, thref):
            shear = (PIN_U[k] - PIN_U[-1]) ** 2 + (PIN_V[k] - PIN_V[-1]) ** 2 + 100.0 * 0.1 ** 2
            return c['ga'] * (thv[k] - thref) * (z[k] - z[-1]) / (thv[-1] * shear)

        # The two levels above the lowest hold a lower thv than it and the third a higher one (levels 4, 3 and 2,
        # counted from 0 at the top), with or without the thermals' excess, so each pass finds its depth between
        # levels 3 and 2, where the number crosses zero.
        def crossing(thref):
            assert number(4, thref) < 0.0 and number(3, thref) < 0.0 <= number(2, thref)
            return z[3] + (0.0 - number(3, thref)) / (number(2, thref) - number(3, thref)) * (z[2] - z[3])

        h_first = crossing(thv[-1])
        wm = (0.1 ** 3 + 15.0 * 0.1 * 0.4 * buoy * h_first) ** (1.0 / 3.0)
        excess = 8.5 * wthv / wm
        h = crossing(thv[-1] + excess)
        assert g['unstable'] and g['h_first'] == pytest.approx(h_first, rel=1e-12)
        assert g['excess'] == pytest.approx(excess, rel=1e-12) and g['h'] == pytest.approx(h, rel=1e-12)
        assert g['wstar'] == pytest.approx((buoy * h) ** (1.0 / 3.0), rel=1e-12) and z[3] < h_first < h < z[2]
        # Stable or neutral air takes none: the surface's fluxes downward, or nil.
        for shfl, evap in ((+20.0, 0.0), (0.0, 0.0)):
            calm, _ = gust_of(dict(x, dshfl=shfl, devap=evap), PIN_HALF, c)
            assert not calm['unstable'] and calm['h'] == 0.0 and calm['wstar'] == 0.0


def test_on_one_column_in_sigma_the_depth_goes_as_one_over_gravity_and_the_velocity_keeps_its_value():
    """Heights go as 1/g on a column given in sigma, and the buoyancy as g, so the bulk number, the thermals' excess
    and the depth's place among the levels stay, and w*^3 = (g/thv) (w'thv')0 h holds its value."""
    for c, half, cols in cases():
        other = dict(c, ga=EARTH['ga'] if c['ga'] == G_MOON else G_MOON)
        for x in cols:
            (here, _), (there, _) = gust_of(x, half, c), gust_of(x, half, other)
            assert here['unstable'] == there['unstable']
            if here['unstable']:
                assert there['h'] * other['ga'] == pytest.approx(here['h'] * c['ga'], rel=1e-12)
                assert there['wstar'] == pytest.approx(here['wstar'], rel=1e-12)
                assert there['excess'] == pytest.approx(here['excess'], rel=1e-12)
                thv = x['dt'][half.size - 1] / sg.full_sigma(half)[-1] ** (c['gascon'] / c['acpd']) \
                    * (1.0 + (1.0 / c['rdbrv'] - 1.0) * x['dq'][half.size - 1])
                wstar = (c['ga'] / thv * here['wthv0'] * here['h']) ** (1.0 / 3.0)
                assert here['wstar'] == pytest.approx(wstar, rel=1e-12)


def test_the_python_copy_gives_terlunas_numbers():
    """Terluna's surface_gust.py at 39c5ee04, run on the written-out column on 2026-11-11, gave these; over its own
    tests' 24 columns the copy here gave its every number bit for bit that day (PROVENANCE.md)."""
    pins = {'moon': (LUNAR, 121590.0, 12276.086716646378, 0.9358915861743418, 0.00399770184059855, 0.002344902664921407,
                     0.002578402792725083, 0.0024434342432979104),
            'earth': (EARTH, 101325.0, 2049.5292530597685, 0.9981571638554125, 0.0045154296374020466,
                      0.003331125867261733, 0.003804748167200532, 0.0034745791174285545)}
    for c, ps_pa, h, wstar, plain_h, plain_m, gusty_h, gusty_m in pins.values():
        x = pinned_column(c, ps_pa)
        g, _ = gust_of(x, PIN_HALF, c)
        plain, gusty = (sg.surface_transfer(x, sg.full_sigma(PIN_HALF), PIN_HALF, c, ngust=k) for k in (0, 1))
        assert (g['h'], g['wstar']) == pytest.approx((h, wstar), rel=1e-12)
        assert (plain['dtransh'], plain['dtransm']) == pytest.approx((plain_h, plain_m), rel=1e-12)
        assert (gusty['dtransh'], gusty['dtransm']) == pytest.approx((gusty_h, gusty_m), rel=1e-12)


def test_over_the_lunar_sea_the_gust_is_small_and_the_tank_term_goes():
    c, half, cols = cases()[0]
    sea = cols[0]                                                     # 3 m/s, 2.7 K, 9 and 110 W/m2 the step before
    earth, moon = (sg.surface_transfer(sea, sg.full_sigma(half), half, c, cfree=k) for k in (0.0016, 0.00083))
    gust = sg.surface_transfer(sea, sg.full_sigma(half), half, c, ngust=1)
    assert 0.3 < gust['wstar'] < 1.0 and 1000.0 < gust['h'] < 8000.0
    assert gust['absu2'] == pytest.approx(9.0 + gust['wstar'] ** 2)
    neutral = np.sqrt(9.0) * (sg.KARMAN / np.log(earth['znl'] / sea['dz0'] + 1.0)) ** 2
    # the transfer of heat against the neutral: the tank term's at Earth's and the Moon's constants, the gust's
    assert earth['dtransh'] / neutral > moon['dtransh'] / neutral > 1.25 > gust['dtransh'] / neutral > 1.0
    # over land the transfer was Louis's already; with the gust it takes the gust's wind alone
    land = cols[5]
    plain, gusty = (sg.surface_transfer(land, sg.full_sigma(half), half, c, ngust=k) for k in (0, 1))
    assert gusty['dtransh'] > plain['dtransh'] and gusty['wstar'] > 0.0
    # a calm stable night: 1 m/s without the gust, 0.1 m/s with it
    night = cols[6]
    assert sg.surface_transfer(night, sg.full_sigma(half), half, c)['absu2'] == 1.0
    assert sg.surface_transfer(night, sg.full_sigma(half), half, c, ngust=1)['absu2'] == pytest.approx(0.01)


@FORTRAN
def test_the_fortran_surflx_gives_the_python_copys_transfer(tmp_path, series_sources):
    pristine = series_sources.source('fluxmod.f90', series_sources.before(GUST_PATCH))
    patched = series_sources.source('fluxmod.f90', GUST_PATCH)
    code, declarations = surflx(patched, last='gustcol'), module_additions(patched, pristine)
    for i, (c, half, cols) in enumerate(cases()):
        exe = compile_surflx(tmp_path / f'case{i}', code, len(cols), half.size, declarations)
        for ngust in (0, 1):
            rows = run_harness(exe, harness_input(c, half, cols, ngust), len(cols))
            for x, row in zip(cols, rows):
                h, m, tsa = (float(v) for v in row.split())
                py = sg.surface_transfer(x, sg.full_sigma(half), half, c, ngust=ngust)
                assert h == pytest.approx(py['dtransh'], rel=1e-10) and m == pytest.approx(py['dtransm'], rel=1e-10)
                assert tsa == pytest.approx(py['dtsa'], rel=1e-12)


@FORTRAN
def test_with_the_switch_off_the_patched_surflx_prints_every_digit_the_old_one_prints(tmp_path, series_sources):
    pristine = series_sources.source('fluxmod.f90', series_sources.before(GUST_PATCH))
    patched = series_sources.source('fluxmod.f90', GUST_PATCH)
    old, new = surflx(pristine), surflx(patched, last='gustcol')
    assert old != new
    for i, (c, half, cols) in enumerate(cases()):
        exe_old = compile_surflx(tmp_path / f'old{i}', old, len(cols), half.size, '')
        exe_new = compile_surflx(tmp_path / f'new{i}', new, len(cols), half.size, module_additions(patched, pristine))
        a = run_harness(exe_old, harness_input(c, half, cols), len(cols))
        b = run_harness(exe_new, harness_input(c, half, cols, 0), len(cols))
        assert a == b


def test_the_patch_declares_reads_and_broadcasts_each_name_once(series_sources):
    assert all(len(line) <= 132 for line in series_sources.added(GUST_PATCH))
    pristine = series_sources.source('fluxmod.f90', series_sources.before(GUST_PATCH))
    text = series_sources.source('fluxmod.f90', GUST_PATCH)
    assert text.count('       call gustnl(zgust2)') == 1 and text.count('      subroutine gustcol(') == 1
    assert text.count('if(dls(jhor) < 1. .and. ngust /= 1) then') == 1
    names = ('ngust', 'gust_beta', 'gust_umin', 'pbl_b', 'pbl_eps', 'pbl_betam', 'pbl_ricru', 'pbl_bu')
    namelist = text[text.index('      namelist/fluxmod_nl/'):text.index('      if(mypid==NROOT) then')]
    for name in names:
        assert len(re.findall(rf'(real|integer) :: {name} = ', text)) == 1
        assert len(re.findall(rf'call mpbc[ri]\({name}\)', text)) == 1
        assert len(re.findall(rf'\b{name}\b', namelist)) == 1
    # The defaults are the Python copy's: the switch off, CM1's factor and least wind, the depth rule's five constants.
    values = dict(re.findall(r'(?:real|integer) :: (\w+) = ([-0-9.e]+)', module_additions(text, pristine)))
    assert {name: float(values[name]) for name in names} == dict(
        ngust=0.0, gust_beta=sg.GUST_BETA, gust_umin=sg.GUST_UMIN, pbl_b=sg.PARAMETERS['b_excess'],
        pbl_eps=sg.PARAMETERS['eps_surface'], pbl_betam=sg.PARAMETERS['beta_m'],
        pbl_ricru=sg.PARAMETERS['ricr_unstable'], pbl_bu=sg.PARAMETERS['b_ustar'])


def compiles_with_plasims_modules(folder, series_sources, through: str) -> None:
    """fluxmod.f90 at a point of the series, compiled with PlaSim's own module on fifteen levels."""
    (folder / 'resmod.f90').write_text('      module resmod\n      parameter(NLAT_ATM = 32)\n'
                                       '      parameter(NLEV_ATM = 15)\n      parameter(NPRO_ATM = 1)\n'
                                       '      end module resmod\n')
    for name in ('plasimmod.f90', 'fluxmod.f90'):
        (folder / name).write_text(series_sources.source(name, through), encoding='latin-1')
    for name in ('resmod.f90', 'plasimmod.f90', 'fluxmod.f90'):
        subprocess.run(['gfortran', *GCM_FLAGS, '-c', name], cwd=folder, check=True, capture_output=True)


@FORTRAN
def test_the_patched_fluxmod_compiles_with_plasims_modules(tmp_path, series_sources):
    compiles_with_plasims_modules(tmp_path, series_sources, GUST_PATCH)
