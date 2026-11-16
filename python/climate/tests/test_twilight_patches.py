"""PlaSim's curved-air twilight through patches 07, 15 and 16 of models/exoplasim/patches, compiled alone: the routines
twilight_term and twilight_lw and the end of swr, taken from the series applied to the pinned ExoPlaSim archive, with
ExoPlaSim's flags against a stub of PlaSim's module, under a stand-in for radstep's passes. At their defaults patches 15
and 16 print every digit that patch 07's routines print, with the clear-sky diagnostic on and off and the twilight on
and off, and under -O3 -march=native, where the compiler fuses products and sums, they agree with them within a few
units of the last place. With the diagnostic on, the released passes count the twilight below the horizon twice:
exactly twice under clear sky, and T(2 - c) of the clear twilight T on the ground under cover c, where one pass gives
T(1 - c); with ntwlzero = 1 the two passes print every digit of one (defect log C21). With ntwlclear = 1 each layer's
twilight, sunlight and infrared escape alike, scales with the clear sky above it, as the arithmetic written out here
gives it, to 1e-12. The patches declare, read and broadcast each name once.

The lab's own file: Terluna's tests of the same two edits (climate/tests/test_exoplasim_run.py on domain/climate at
39c5ee04) compile a stand-in swr from its runner's edit lists."""
from __future__ import annotations

import math
import re
import subprocess

import numpy as np
import pytest

from climate.tests.test_rain_drops import NATIVE_FLAGS
from climate.tests.test_surface_gust import FORTRAN, GCM_FLAGS, num

CURVED_AIR, CLEAR_SHARE, ONCE = '07-curved-air.patch', '15-twilight-clear-share.patch', '16-twilight-counted-once.patch'
PI = 3.14159265359                  # PlaSim's own (plasimmod.f90), with which twilight_term turns the Sun's height
                                    # into degrees
SUN = 1361.0                        # gsol0 times gdist2, W/m2: a made-up sunlight at the top
SEED = 7

STUB = """      module radmod
      implicit none
      integer, parameter :: NHOR = {nhor}, NLEV = {nlev}, NLEP = NLEV + 1
      real, parameter :: PI = 3.14159265359
      real :: gsol0 = 0.0, gdist2 = 1.0
      integer :: nclouds = 1
      real :: dcc(NHOR,NLEP) = 0.0, dt(NHOR,NLEP) = 0.0
      real :: dfu(NHOR,NLEP) = 0.0, dfd(NHOR,NLEP) = 0.0, dswfl(NHOR,NLEP) = 0.0
      real :: dftu(NHOR,NLEP) = 0.0, dlwfl(NHOR,NLEP) = 0.0
{declarations}      end module radmod

      module standin
      use radmod
      implicit none
      logical :: sunlit(NHOR) = .false.
      real :: sunfd(NHOR,NLEP) = 0.0, sunfu(NHOR,NLEP) = 0.0
      end module standin
"""
# A stand-in for swr: where the Sun is up it writes every level's fluxes from made-up sunlight thinned by the cover, as
# swr writes them there alone (losun); then the end of swr as the series has it at the point compiled.
SWR = """      subroutine swr
      use standin
      implicit none
      integer :: jlev
      logical :: losun(NHOR)
      real :: zcover(NHOR)
      losun(:) = sunlit(:)
      zcover(:) = sum(dcc(:,1:NLEV), dim=2) / NLEV
      do jlev=1,NLEP
       where(losun(:))
        dfu(:,jlev)=-sunfu(:,jlev)*(1.0+zcover(:))
        dfd(:,jlev)=sunfd(:,jlev)*(1.0-0.5*zcover(:))
        dswfl(:,jlev)=dfu(:,jlev)+dfd(:,jlev)
       endwhere
      enddo
{tail}      return
      end subroutine swr
"""
# radstep's order (radmod.f90, radstep): the shortwave fluxes set to zero once; with the clear-sky diagnostic, swr
# without cloud and then with it. lwr starts its fluxes from zero and records each layer's transmissivity before it
# calls twilight_lw, which the stand-in's last lines do for the all-sky pass.
HARNESS = """      program harness
      use standin
      implicit none
      integer :: ndiagcf, jhor, jlev, jtwl
      real :: zcc(NHOR,NLEP), ztau(NHOR,NLEV)
      read(*,*) ndiagcf, ntwilight, ntwilw, nclouds{switches}
      read(*,*) gsol0
      read(*,*) ntwl
      do jtwl = 1, ntwl
       read(*,*) twlel(jtwl), twlg(jtwl), (twlq(jlev,jtwl), jlev=1,NLEV)
      enddo
      read(*,*) (twlw(jlev), jlev=1,NLEP)
      read(*,*) (twlt(jlev), jlev=1,NLEP)
      do jhor = 1, NHOR
       read(*,*) gmuz(jhor), sunlit(jhor)
       read(*,*) (dcc(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dt(jhor,jlev), jlev=1,NLEP)
       read(*,*) (sunfd(jhor,jlev), jlev=1,NLEP)
       read(*,*) (sunfu(jhor,jlev), jlev=1,NLEP)
       read(*,*) (ztau(jhor,jlev), jlev=1,NLEV)
      enddo
      dfu(:,:) = 0.0
      dfd(:,:) = 0.0
      dswfl(:,:) = 0.0
      if (ndiagcf > 0) then
       zcc(:,:) = dcc(:,:)
       dcc(:,:) = 0.0
       call swr
       dcc(:,:) = zcc(:,:)
      endif
      call swr
      dftu(:,:) = 0.0
      dlwfl(:,:) = 0.0
{record}      if (ntwilw == 1) call twilight_lw
      do jhor = 1, NHOR
       write(*,'(*(es25.16e3))') (dswfl(jhor,jlev), jlev=1,NLEP)
       write(*,'(*(es25.16e3))') (dfd(jhor,jlev), jlev=1,NLEP)
       write(*,'(*(es25.16e3))') (dfu(jhor,jlev), jlev=1,NLEP)
       write(*,'(*(es25.16e3))') (dftu(jhor,jlev), jlev=1,NLEP)
       write(*,'(*(es25.16e3))') (dlwfl(jhor,jlev), jlev=1,NLEP)
      enddo
      end program harness
"""
RECORD = '      if (ntwlclear == 1) twltau(:,:) = ztau(:,:)\n'
OUTPUTS = ('dswfl', 'dfd', 'dfu', 'dftu', 'dlwfl')


def module_part(text: str) -> list:
    return text[:text.index('      end module radmod\n')].splitlines(keepends=True)


def module_additions(patched: str, before: str) -> str:
    """The lines a patched radmod.f90 adds to the module's own part, its declarations, in order."""
    old = set(module_part(before))
    return ''.join(line for line in module_part(patched) if line not in old)


def routine(text: str, name: str) -> str:
    start = text.index(f'      subroutine {name}\n')
    end = f'      end subroutine {name}\n'
    return text[start:text.index(end, start) + len(end)]


def swr_tail(text: str) -> str:
    """swr after its last loop, the fluxes at the layers' interfaces, up to its return: the patches' lines there and
    the call of twilight_term."""
    loop = '        dswfl(:,jlev)=dfu(:,jlev)+dfd(:,jlev)\n       endwhere\n      enddo\n'
    start = text.index(loop) + len(loop)
    return text[start:text.index('      return\n      end subroutine swr\n', start)]


class Sources:
    """radmod.f90 at the series' points 14 (before patch 15), 15 and 16, and harnesses compiled from them, each
    once."""

    def __init__(self, series_sources, root):
        self.series = series_sources
        before = series_sources.before(CLEAR_SHARE)
        self.points = {14: before, 15: CLEAR_SHARE, 16: ONCE}
        self.text = {n: series_sources.source('radmod.f90', patch) for n, patch in self.points.items()}
        self.curved = module_additions(series_sources.source('radmod.f90', CURVED_AIR),
                                       series_sources.source('radmod.f90', series_sources.before(CURVED_AIR)))
        self.root, self.built = root, {}

    def harness(self, point: int, nhor: int, nlev: int, flags=GCM_FLAGS):
        key = (point, nhor, nlev, flags)
        if key not in self.built:
            text = self.text[point]
            folder = self.root / f'build{len(self.built)}'
            folder.mkdir()
            declarations = self.curved + (module_additions(text, self.text[14]) if point > 14 else '')
            switches = {14: '', 15: ', ntwlclear', 16: ', ntwlclear, ntwlzero'}[point]
            files = {'stub.f90': STUB.format(nhor=nhor, nlev=nlev, declarations=declarations),
                     'swr.f90': SWR.format(tail=swr_tail(text)),
                     'twilight.f90': routine(text, 'twilight_term') + '\n' + routine(text, 'twilight_lw'),
                     'harness.f90': HARNESS.format(switches=switches, record=RECORD if point > 14 else '')}
            for name, body in files.items():
                (folder / name).write_text(body)
            subprocess.run(['gfortran', *flags, '-o', 'harness', *files], cwd=folder, check=True, capture_output=True)
            self.built[key] = folder / 'harness'
        return self.built[key]


@pytest.fixture(scope='module')
def sources(series_sources, tmp_path_factory):
    return Sources(series_sources, tmp_path_factory.mktemp('twilight'))


def table(nlev: int, rng) -> dict:
    """A made-up twilight table on irregular elevations from 40 degrees below the horizon to the zenith, as the
    ledger's span, with terms of the ledger's order: per unit sunlight at the beam, the ground's and each layer's; and
    each layer's and the ground's extra infrared escape, W/m2, at its temperature."""
    elevation = np.r_[-40.0, -31.0, -22.5, -15.0, -9.0, -5.0, -2.5, -1.0, 0.0, 1.5, 4.0, 10.0, 25.0, 50.0, 90.0]
    return dict(elevation=elevation, ground=rng.uniform(1e-4, 4e-3, elevation.size),
                layers=rng.uniform(1e-5, 2e-3, (nlev, elevation.size)), escape=rng.uniform(0.05, 2.0, nlev + 1),
                temperature=rng.uniform(190.0, 300.0, nlev + 1))


def columns(nlev: int, rng) -> dict:
    """Columns at Suns from below the table to high noon, sunlit where the Sun stands above the horizon: cloudless,
    under random cover, under one opaque layer, and one at a table's own elevation."""
    degrees = np.array([-55.0, -35.2, -20.0, -9.0, -6.3, -3.1, -0.4, -12.7, -27.0, 0.6, 7.0, 33.0, -1.0, 60.0])
    n = degrees.size
    cover = rng.uniform(0.0, 0.8, (n, nlev)) * (rng.uniform(size=(n, nlev)) < 0.6)
    cover[[0, 3, 10]] = 0.0                                   # cloudless columns, by night and by day
    cover[7] = 0.0
    cover[7, nlev // 2] = 1.0                                 # one opaque layer at night
    cover[12, :2] = 0.3                                       # a Sun on one of the table's elevations, under high cloud
    return dict(mu=np.sin(np.radians(degrees)), sunlit=degrees > 0.0, cover=cover,
                t=rng.uniform(200.0, 300.0, (n, nlev + 1)), fd=rng.uniform(10.0, 600.0, (n, nlev + 1)),
                fu=rng.uniform(1.0, 80.0, (n, nlev + 1)), tau=1.0 - cover * rng.uniform(0.2, 1.0, (n, nlev)))


def harness_input(tab: dict, col: dict, ndiagcf: int, twilight: int = 1, switches: tuple = ()) -> str:
    lines = [f'{ndiagcf} {twilight} {twilight} 1' + ''.join(f' {s}' for s in switches), num(SUN),
             str(tab['elevation'].size)]
    lines += [num(np.r_[tab['elevation'][i], tab['ground'][i], tab['layers'][:, i]])
              for i in range(tab['elevation'].size)]
    lines += [num(tab['escape']), num(tab['temperature'])]
    for j in range(col['mu'].size):
        lines += [f"{float(col['mu'][j])!r} {'T' if col['sunlit'][j] else 'F'}", num(col['cover'][j]),
                  num(col['t'][j]), num(col['fd'][j]), num(col['fu'][j]), num(col['tau'][j])]
    return '\n'.join(lines) + '\n'


def run(exe, text: str) -> str:
    done = subprocess.run([str(exe)], input=text, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr[-2000:]
    return done.stdout


def fields(stdout: str, n: int) -> dict:
    rows = [np.array(r.split(), float) for r in stdout.strip('\n').split('\n')]
    assert len(rows) == len(OUTPUTS) * n
    return {name: np.array([rows[len(OUTPUTS) * j + k] for j in range(n)]) for k, name in enumerate(OUTPUTS)}


def interpolated(tab: dict, mu: float):
    """twilight_term's reading of the table at a Sun of cosine-of-zenith mu, written out: the elevation in degrees by
    PlaSim's pi, the bracketing rows by bisection and the linear weight; None outside the table."""
    el = math.asin(max(-1.0, min(1.0, mu))) * 180.0 / PI
    els = tab['elevation']
    if el < els[0] or el > els[-1]:
        return None
    lo, hi = 0, els.size - 1
    while hi - lo > 1:
        mid = (lo + hi + 2) // 2 - 1                         # Fortran's (jlo + jhi) / 2 on indices from 1
        if els[mid] > el:
            hi = mid
        else:
            lo = mid
    u = (el - els[lo]) / (els[hi] - els[lo])
    ground = (1.0 - u) * tab['ground'][lo] + u * tab['ground'][hi]
    return ground, (1.0 - u) * tab['layers'][:, lo] + u * tab['layers'][:, hi]


def added(tab: dict, mu: float, cover, clear_share: bool) -> np.ndarray:
    """The sunlight one pass of twilight_term adds to dswfl at each level, top first, by hand: the ground's term in the
    column's clear share, each layer's in the clear sky above it with the clear share and in full without, carried
    down from the top as net downward flux."""
    terms = interpolated(tab, mu)
    if terms is None:
        return np.zeros(cover.size + 1)
    ground, layers = terms
    clear = np.cumprod(np.r_[1.0, 1.0 - cover])               # the clear sky above each layer, then the column's
    absorbed = SUN * layers * (clear[:-1] if clear_share else 1.0)
    return SUN * ground * clear[-1] + np.r_[np.cumsum(absorbed[::-1])[::-1], 0.0]


def escaped(tab: dict, t, tau, clear_share: bool) -> np.ndarray:
    """dftu as twilight_lw leaves it after lwr's own zero, by hand: each layer's and the ground's extra escape at its
    temperature to the fourth power, through the cloud above at each layer's transmissivity with the clear share,
    carried up to the top as upward flux."""
    through = np.cumprod(np.r_[1.0, tau]) if clear_share else np.ones(tau.size + 1)
    escape = tab['escape'] * (t / tab['temperature']) ** 4 * through
    return -np.r_[np.cumsum(escape[:-1][::-1])[::-1] + escape[-1], escape[-1]]


def close(got, want, label, rel=1e-12):
    scale = max(np.abs(want).max(), 1e-300)
    assert np.abs(got - want).max() <= rel * scale, (label, np.abs(got - want).max() / scale)


@pytest.fixture(scope='module')
def case():
    rng = np.random.default_rng(SEED)
    nlev = 10
    return nlev, table(nlev, rng), columns(nlev, rng)


@FORTRAN
def test_at_their_defaults_patches_15_and_16_print_every_digit_patch_07s_routines_print(sources, case):
    """Under ExoPlaSim's flags, the point before patch 15, with neither switch, against points 15 and 16 at their
    defaults, 0: with the clear-sky diagnostic off and on, the curved air's terms on and off, the same digits in every
    flux of every column. With 0 the clear share is a factor of exactly 1, which leaves every product as it was."""
    nlev, tab, col = case
    n = col['mu'].size
    for twilight in (1, 0):
        for ndiagcf in (0, 1):
            before = run(sources.harness(14, n, nlev), harness_input(tab, col, ndiagcf, twilight))
            assert len(before.splitlines()) == len(OUTPUTS) * n
            assert run(sources.harness(15, n, nlev), harness_input(tab, col, ndiagcf, twilight, (0,))) == before
            assert run(sources.harness(16, n, nlev), harness_input(tab, col, ndiagcf, twilight, (0, 0))) == before, \
                (twilight, ndiagcf)
    lit = fields(before, n)                                   # the last: the twilight off, the diagnostic on
    assert np.all(lit['dswfl'][~col['sunlit']] == 0.0) and np.all(lit['dftu'] == 0.0)


@FORTRAN
def test_compiled_to_fuse_products_and_sums_the_defaults_keep_patch_07s_numbers_to_the_last_bits(sources, case):
    """Under -O3 -march=native, on a processor whose multiply-adds the compiler fuses, a factor of 1 can change which
    product a sum takes unrounded: at their defaults points 15 and 16 then agree with the point before them within a
    few units of the last place, 1e-15 of each flux's largest value. The lab's builds compile with ExoPlaSim's flags
    (lab/worldlab/builds.py), under which the digits agree."""
    nlev, tab, col = case
    n = col['mu'].size
    for ndiagcf in (0, 1):
        before = fields(run(sources.harness(14, n, nlev, NATIVE_FLAGS), harness_input(tab, col, ndiagcf)), n)
        for point, switches in ((15, (0,)), (16, (0, 0))):
            got = fields(run(sources.harness(point, n, nlev, NATIVE_FLAGS), harness_input(tab, col, ndiagcf, 1,
                                                                                         switches)), n)
            for name in OUTPUTS:
                close(got[name], before[name], (point, ndiagcf, name), rel=1e-15)


@FORTRAN
@pytest.mark.parametrize('clear_share', [0, 1])
def test_the_released_passes_count_the_night_twilight_twice_and_ntwlzero_counts_it_once(sources, case, clear_share):
    """Defect log C21 at point 16. With the clear-sky diagnostic on and ntwlzero 0 the twilight below the horizon is
    the clear pass's beside the all-sky pass's: exactly twice one pass's under clear sky, and on the ground T(2 - c)
    of the clear twilight T under cover c, where one pass gives T(1 - c). With ntwlzero 1 the two passes print every
    digit of one, with the diagnostic off, in every column; and where the Sun is up the two settings agree."""
    nlev, tab, col = case
    n, exe = col['mu'].size, sources.harness(16, col['mu'].size, nlev)
    out = {(ndiagcf, zero): run(exe, harness_input(tab, col, ndiagcf, 1, (clear_share, zero)))
           for ndiagcf in (0, 1) for zero in (0, 1)}
    assert out[1, 1] == out[0, 0] == out[0, 1]
    once, twice = fields(out[0, 0], n), fields(out[1, 0], n)
    night = ~col['sunlit']
    lit = col['sunlit']
    for name in OUTPUTS:
        assert np.array_equal(twice[name][lit], once[name][lit]), name
    assert np.array_equal(twice['dftu'], once['dftu']) and np.array_equal(twice['dfu'], once['dfu'])
    within = np.array([interpolated(tab, mu) is not None for mu in col['mu']])
    assert not within[0] and np.all(twice['dswfl'][night & ~within] == 0.0)
    for j in np.flatnonzero(night & within):
        cover = col['cover'][j]
        clear = added(tab, col['mu'][j], np.zeros(nlev), bool(clear_share))   # the clear pass's, T at the ground
        own = added(tab, col['mu'][j], cover, bool(clear_share))
        close(once['dswfl'][j], own, ('once', j))
        close(twice['dswfl'][j], clear + own, ('twice', j))
        c = 1.0 - np.prod(1.0 - cover)
        close(twice['dswfl'][j, -1:], clear[-1:] * (2.0 - c), ('T(2-c)', j))
        close(once['dswfl'][j, -1:], clear[-1:] * (1.0 - c), ('T(1-c)', j))
        assert np.array_equal(twice['dfd'][j], twice['dswfl'][j])        # the twilight is downward flux alone
        if not cover.any():
            assert np.array_equal(twice['dswfl'][j], 2.0 * once['dswfl'][j]) and once['dswfl'][j, 0] > 0.0


@FORTRAN
def test_with_the_clear_share_each_layers_twilight_scales_with_the_clear_sky_above_it(sources, case):
    """Point 15 with ntwlclear 1 and one pass: each layer's sunlight from the curved air in the share of the sky clear
    of cloud above it, by random overlap, the ground's in the whole column's; each layer's and the ground's infrared
    escape through the cloud above at each layer's transmissivity. Against the arithmetic written out, to 1e-12, and
    under an opaque layer the layers below it and the ground take no twilight and lose no escape through it. With
    ntwlclear 0 the same arithmetic without the clear sky gives patch 07's numbers."""
    nlev, tab, col = case
    n = col['mu'].size
    for share in (1, 0):
        got = fields(run(sources.harness(15, n, nlev), harness_input(tab, col, 0, 1, (share,))), n)
        for j in range(n):
            want = added(tab, col['mu'][j], col['cover'][j], bool(share))
            if col['sunlit'][j]:                              # the stand-in's own sunlight beneath the twilight
                cover = col['cover'][j].sum() / nlev
                want = want - col['fu'][j] * (1.0 + cover) + col['fd'][j] * (1.0 - 0.5 * cover)
            close(got['dswfl'][j], want, ('sunlight', share, j))
            close(got['dftu'][j], escaped(tab, col['t'][j], col['tau'][j], bool(share)), ('infrared', share, j))
            assert np.array_equal(got['dlwfl'][j], got['dftu'][j])
        if share:
            shared = got
    # Under the opaque layer of column 7 the layers below it and the ground take nothing: dswfl stays at its value
    # below the cloud's layer, and each layer above takes its term in full, the sky above it being clear.
    k, j = nlev // 2, 7
    assert col['cover'][j, k] == 1.0 and not col['cover'][j, :k].any() and not col['sunlit'][j]
    assert np.all(shared['dswfl'][j, k + 1:] == 0.0) and shared['dswfl'][j, k] > 0.0
    plain = fields(run(sources.harness(15, n, nlev), harness_input(tab, col, 0, 1, (0,))), n)
    layer = lambda f: f['dswfl'][j, :-1] - f['dswfl'][j, 1:]
    assert np.allclose(layer(shared)[:k + 1], layer(plain)[:k + 1], rtol=1e-12, atol=0.0)
    # The infrared: a cloudless column's escape is patch 07's to the last digit.
    for j in np.flatnonzero(~col['cover'].any(axis=1)):
        assert np.array_equal(shared['dftu'][j], plain['dftu'][j])


def test_the_patches_declare_read_and_broadcast_each_name_once(series_sources):
    for patch in (CLEAR_SHARE, ONCE):
        assert all(len(line) <= 132 for line in series_sources.added(patch)), patch
    text = series_sources.source('radmod.f90', ONCE)
    namelist = text[text.index('      namelist/radmod_nl/'):text.index('     namelist/aero_nl/')]
    for name, kind in (('ntwlclear', 'integer'), ('ntwlzero', 'integer')):
        assert len(re.findall(rf'{kind} :: {name} = 0 ', text)) == 1, name
        assert len(re.findall(rf'call mpbci\({name}\)', text)) == 1, name
        assert len(re.findall(rf'\b{name}\b', namelist)) == 1, name
    assert text.count('      real :: twltau(NHOR,NLEV) = 1.0 ') == 1 and text.count('twltau(') == 3
    # lwr records each layer's transmissivity in its first loop, after the ice optics have set it, and calls
    # twilight_lw after its fluxes are complete.
    lwr = routine(text, 'lwr')
    ice = '       if (niceopt == 1 .and. clgray <= 0.) call ice_cloud_lw(jlev,ztaucc0(:,jlev)) ! Terluna: ice\n'
    record = '       if (ntwlclear == 1) twltau(:,jlev) = ztaucc0(:,jlev) ! Lab: for the twilight\'s clear share\n'
    assert lwr.count(ice + record + '      enddo\n') == 1
    assert lwr.index(record) < lwr.index('      if (ntwilw == 1) call twilight_lw')
    # The zero start comes last in swr, before the call that adds the twilight, and touches no column the Sun lights.
    tail = swr_tail(text)
    assert tail.index('      if (ntwlzero == 1) then\n') < tail.index('call twilight_term')
    assert tail.count('where(.not. losun(:))') == 1 and tail.count('=0.0\n') == 3
    # Patch 15 removes six lines and patch 16 one, each put back with its addition.
    for patch, count in ((CLEAR_SHARE, 6), (ONCE, 1)):
        removed = [line for line in (series_sources.folder / patch).read_text().splitlines()
                   if line.startswith('-') and not line.startswith('---')]
        assert len(removed) == count, (patch, removed)
