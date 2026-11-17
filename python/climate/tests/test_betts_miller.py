"""Simplified Betts-Miller convection in PlaSim through patches 18 to 20 of models/exoplasim/patches (`nprc` 2):
mksbm and mkshallow, taken from the series applied to the pinned ExoPlaSim archive and compiled with ExoPlaSim's flags
against a stub of PlaSim's module, give the numbers of the Python copy of Frierson's (2007) scheme written here to
1e-10, on Earth-like columns on PlaSim's ten levels and lunar columns on Terluna's fifteen and on forty: deep columns,
thin clouds, columns too dry to rain, columns held back by their inhibition and columns buoyant nowhere, with the
parcel undiluted and mixing within its layers. On them the scheme relaxes toward its references over tau_bm, rains the
vapour the column loses and keeps the column's moist enthalpy; the depth test turns a cloud from deep to shallow at the
share of the column's surface pressure it states, at Earth's 1 atm and in the Open Moon's air at 1.2 and 0.5 bar; and
the shallow cap hands mkshallow the highest level within that share of the cloud's base, where mkshallow keeps it in
place of PlaSim's 700 hPa. Called before patch 14's mkrain, mksbm's rain by level gives the evaporation of patch 14's
Python copy. Each patch at its defaults prints every digit the routine before it prints, under ExoPlaSim's flags and
under -O3 -march=native. Compiled into one program with the routines of Terluna's design build, read from its research
drive under a pinned hash, the lab's routines print every digit Terluna's print, the depth test's share set so that it
comes to exactly 20,000 Pa at the column's surface pressure. The patches hold no number of the Moon's, declare, read
and broadcast each name once, stop on settings out of range, and compile with PlaSim's modules.

The lab's own file: Terluna's tests of its edit lists (climate/tests/test_sbm.py and test_shallow_cap.py on
domain/climate at 39c5ee04) compiled the routine from its runner's strings against a copy of its own (climate/gcm/sbm.py).
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess

import numpy as np
import pytest

from atmosphere.radiative_convective.thermodynamics import DryAir, earthlike_air
from atmosphere.rain import breakup, drops, fall_law
from climate.gcm import rain_drops as rd
from climate.tests import test_rain_drops as rain
from climate.tests.test_rain_drops import NATIVE_FLAGS
from shared.constants import MOON_SURFACE_GRAVITY, STANDARD_GRAVITY
from climate.tests.test_surface_gust import FORTRAN, GCM_FLAGS, HALF15, num, plasim_half

SCHEME, DEPTH, CAP = ('18-betts-miller-convection.patch', '19-betts-miller-depth-test.patch',
                      '20-betts-miller-shallow-cap.patch')
POINT = {SCHEME: ('tau_bm', 'rh_bm', 'eps_bm', 'cin_bm'), DEPTH: ('dsigdeep_bm', 'nsub_bm'), CAP: ('nshcap_bm',)}
INTEGERS = ('nsub_bm', 'nshcap_bm', 'ndiagnight_bm')
# The settings at the patches' defaults, which the module declares
DEFAULTS = dict(tau_bm=7200.0, rh_bm=0.7, eps_bm=0.0, cin_bm=0.0, dsigdeep_bm=0.0, nsub_bm=1, nshcap_bm=0)
# The design scheme of Terluna's design run (A28R_301k_design_l15_snow_s934, model/rainmod_namelist), its depth as the
# lab's share of Earth's standard surface pressure
DESIGN = dict(DEFAULTS, dsigdeep_bm=200.0 / 1013.25, nshcap_bm=1)
# PlaSim's constants as a run of each world holds them: the Open Moon's air as Terluna's tests take it, and Earth's
PHYSICS = dict(ALV=2.5008e6, ALS=2.8345e6, ra1=610.78, ra2=17.2693882, ra4=35.86, TMELT=273.16, deltsec2=3600.0,
               akap=0.286)
LUNAR = dict(PHYSICS, ga=1.6242188765608128, gascon=288.3767, acpd=288.3767 / 0.286, ADV=0.8546,
             rdbrv=288.3767 / 461.51)
EARTH = dict(PHYSICS, ga=9.80665, gascon=287.05, acpd=1004.6, ADV=0.8608, rdbrv=287.05 / 461.51)
CONSTANTS = ('deltsec2', 'ga', 'gascon', 'akap', 'acpd', 'ADV', 'ALV', 'ALS', 'rdbrv', 'ra1', 'ra2', 'ra4', 'TMELT')
HALF40 = np.r_[np.linspace(0.025, 0.9, 30), np.linspace(0.92, 1.0, 10)]
# Terluna's design build: the rainmod.f90 its executable compiled (the run's record names rainmod b55e297f48e3a268), kept
# in the folder of a test build of the same run on Terluna's research drive
DESIGN_RUN = 'gcm-runs/A28R_301k_design_l15_snow_s934'
DESIGN_SOURCE = 'gcm-runs/A28R_301k_design_l15_snow_s934_weather_test/build/plasim/src/rainmod.f90'
DESIGN_SHA256 = 'b55e297f48e3a26843465607f21838dc21388777be052e85268693f23eafdb54'
DEEP_PA = 20000.0                                   # the design build's dpdeep_bm


# ------------------------------------------------------------------------------------------------------- Python copy

def saturation(t, p, c):
    """PlaSim's saturation specific humidity (kg/kg) at t (K) and p (Pa), as Kuo's parcel takes it."""
    q = min(c['rdbrv'] * c['ra1'] * math.exp(c['ra2'] * (t - c['TMELT']) / (t - c['ra4'])) / p, c['rdbrv'])
    return q / (1.0 - (1.0 / c['rdbrv'] - 1.0) * q)


def condense(t, q, p, c):
    """A supersaturated parcel condensed to saturation in two Newton steps, with the latent heat of sublimation below
    freezing."""
    for _ in range(2):
        qs = min(c['rdbrv'] * c['ra1'] * math.exp(c['ra2'] * (t - c['TMELT']) / (t - c['ra4'])) / p, c['rdbrv'])
        cor = 1.0 / (1.0 - (1.0 / c['rdbrv'] - 1.0) * qs)
        qs *= cor
        if qs >= q:
            break
        lcp = (c['ALS'] if t < c['TMELT'] else c['ALV']) / (c['acpd'] * (1.0 + c['ADV'] * q))
        rain = (q - qs) / (1.0 + lcp * c['ra2'] * (c['TMELT'] - c['ra4']) * qs * cor / (t - c['ra4']) ** 2)
        t, q = t + lcp * rain, q - rain
    return t, q


def parcel(t, q, sigma, ps, c, eps=0.0, steps=1):
    """The parcel from the lowest level, its temperature by level, top first: lifted dry adiabatically through each
    layer and condensed, mixing in the share 1 - exp(-eps ln(sigma_below/sigma)) of the layer's air; with steps > 1
    the mixing is taken in that many equal steps of log pressure, the air interpolated linearly in log pressure."""
    k = c['akap']
    tn, qn = condense(t[-1], q[-1], ps * sigma[-1], c)
    tp = np.empty(t.size)
    tp[-1] = tn
    for j in range(t.size - 2, -1, -1):
        if eps > 0.0 and steps > 1:
            sub = math.log(sigma[j + 1] / sigma[j]) / steps
            mix = 1.0 - math.exp(-eps * sub)
            s0 = sigma[j + 1]
            for i in range(1, steps + 1):
                s1 = s0 * math.exp(-sub) if i < steps else sigma[j]
                tn *= math.exp(-k * sub) if i < steps else (s1 / s0) ** k
                w = i / steps
                tn = (1.0 - mix) * tn + mix * ((1.0 - w) * t[j + 1] + w * t[j])
                qn = (1.0 - mix) * qn + mix * ((1.0 - w) * q[j + 1] + w * q[j])
                tn, qn = condense(tn, qn, ps * s1, c)
                s0 = s1
        else:
            tn *= (sigma[j] / sigma[j + 1]) ** k
            if eps > 0.0:
                mix = 1.0 - math.exp(-eps * math.log(sigma[j + 1] / sigma[j]))
                tn, qn = (1.0 - mix) * tn + mix * t[j], (1.0 - mix) * qn + mix * q[j]
            tn, qn = condense(tn, qn, ps * sigma[j], c)
        tp[j] = tn
    return tp


def base(t0, q0, p0, ptop, c):
    """The condensation level of air t0, q0 at p0 lifted dry adiabatically: p0 if saturated there, ptop if still
    unsaturated at ptop, and otherwise 24 halvings of the interval in log pressure."""
    lifted = lambda p: t0 * (p / p0) ** c['akap']
    if q0 >= saturation(t0, p0, c):
        return p0
    if q0 < saturation(lifted(ptop), ptop, c):
        return ptop
    lo, hi = math.log(ptop), math.log(p0)
    for _ in range(24):
        mid = 0.5 * (lo + hi)
        if q0 >= saturation(lifted(math.exp(mid)), math.exp(mid), c):
            lo = mid
        else:
            hi = mid
    return math.exp(0.5 * (lo + hi))


def column(t, q, sigma, dsigma, ps, c, s):
    """The scheme on one column (top first) at the settings s, from its state after the step's tendencies so far: its
    temperature and vapour tendencies, the rain formed at each level in mksbm's units (kg/kg/s times dsigma), its
    convective cloud layers (1, or 2 at a top above sigma 0.4), its decision, the parcel's top and the top it hands
    the shallow scheme, and the reference temperature."""
    n = t.size
    p, m = ps * sigma, ps * dsigma / c['ga']
    cp = c['acpd'] * (1.0 + c['ADV'] * q)
    out = dict(dtdt=np.zeros(n), dqdt=np.zeros(n), rain=np.zeros(n), clouds=np.zeros(n, int), decision='stable',
               top=None, shallow_top=None, base=None)
    tp = parcel(t, q, sigma, ps, c, s['eps_bm'], s['nsub_bm'])
    out['reference_t'] = tp
    buoyant = [j for j in range(n - 2, -1, -1) if tp[j] > t[j]]
    if not buoyant:
        return out
    lfc = top = buoyant[0]
    for j in range(lfc - 1, -1, -1):
        if tp[j] <= t[j]:
            break
        top = j
    cin = sum(c['gascon'] * max(0.0, t[j] - tp[j]) * dsigma[j] / sigma[j] for j in range(lfc + 1, n))
    out.update(top=top, cin=cin)
    deep = s['dsigdeep_bm'] * ps
    if s['dsigdeep_bm'] > 0.0:
        out['base'] = base(t[-1], q[-1], p[-1], p[top], c)
        if out['base'] - p[top] <= deep:
            out.update(decision='thin', shallow_top=top)
            return out
    tau = max(s['tau_bm'], c['deltsec2'])
    levels = range(top, n)
    dtr = {j: (tp[j] - t[j]) / tau for j in levels}
    dqr = {j: (s['rh_bm'] * saturation(tp[j], p[j], c) - q[j]) / tau for j in levels}
    pq = -sum(dqr[j] * m[j] for j in levels)
    if pq <= 0.0 or (s['cin_bm'] > 0.0 and cin > s['cin_bm']):
        out.update(decision='dry' if pq <= 0.0 else 'held', shallow_top=top)
        if s['nshcap_bm'] == 1 and s['dsigdeep_bm'] > 0.0:
            out['shallow_top'] = next((j for j in range(top, n) if p[j] >= out['base'] - deep), n - 1)
        return out
    corr = (c['ALV'] * pq - sum(cp[j] * dtr[j] * m[j] for j in levels)) / sum(cp[j] * m[j] for j in levels)
    cond = sum(max(0.0, -dqr[j]) * m[j] for j in levels)
    out['decision'] = 'deep'
    for j in levels:
        out['dtdt'][j], out['dqdt'][j] = dtr[j] + corr, dqr[j]
        if dqr[j] < 0.0:
            out['rain'][j] = -dqr[j] * pq / cond * dsigma[j]
            out['clouds'][j] = 2 if (sigma[j] < 0.4 and j == top) else 1
    return out


# ------------------------------------------------------------------------------------------------------- columns

def levels(half):
    half = np.asarray(half, float)
    lower = np.r_[0.0, half[:-1]]
    return 0.5 * (lower + half), half - lower, half


KINDS = {   # the lowest level's temperature (K) and humidity, and the humidity aloft; the air aloft either `below` the
            # lowest level's undiluted parcel by that many kelvin, or on a `lapse`, sigma's power of kappa times it;
            # and warm layers (K) above the lowest level and aloft
    'deep': dict(ts=300.0, rh0=0.95, rh=0.85, below=1.0),
    'dry': dict(ts=301.0, rh0=0.95, rh=0.1, below=1.0),
    'held': dict(ts=300.0, rh0=0.95, rh=0.85, below=1.0, low_warm=2.5),
    'thin': dict(ts=298.0, rh0=0.93, rh=0.7, below=1.0, cap_sigma=0.82, cap_warm=12.0),
    'middle': dict(ts=300.0, rh0=0.95, rh=0.85, below=2.0, cap_sigma=0.42, cap_warm=15.0),   # its top below sigma 0.42
    'stable': dict(ts=290.0, rh0=0.3, rh=0.3, lapse=0.4),
}


def columns(c, half, ps, kinds, seed):
    """Columns of the given kinds, top first, each with the state after the step's tendencies so far: its
    temperature, vapour and their tendencies, and the dynamics' vapour tendency (dqt); a stratosphere at 200 K and
    random departures of a few tenths of a kelvin and a few per cent of humidity."""
    sigma, dsigma, sigmah = levels(half)
    rng = np.random.default_rng(seed)
    out = []
    for kind in kinds:
        k = KINDS[kind]
        ts = k['ts'] + rng.uniform(-1.0, 1.0)
        if 'below' in k:
            start = np.full(sigma.size, ts), np.full(sigma.size, k['rh0'] * saturation(ts, ps * sigma[-1], c))
            t = np.maximum(parcel(*start, sigma, ps, c) - k['below'], 200.0)
            t[-1] = ts
        else:
            t = np.maximum(ts * (sigma / sigma[-1]) ** (c['akap'] * k['lapse']), 200.0)
        t += rng.normal(0.0, 0.2, t.size)
        if 'low_warm' in k:
            t[-3:-1] += k['low_warm']
        if 'cap_sigma' in k:
            t[sigma < k['cap_sigma']] += k['cap_warm']
        rh = np.where(sigma > 0.9, k['rh0'], k['rh']) * rng.uniform(0.97, 1.0, t.size)
        q = np.array([r * saturation(tj, ps * sj, c) for r, tj, sj in zip(rh, t, sigma)])
        out.append(dict(kind=kind, t=t, q=q, dtdt=rng.normal(0.0, 1e-5, t.size), dqdt=rng.normal(0.0, 1e-9, t.size),
                        dqt=rng.normal(0.0, 1e-8, t.size)))
    return dict(sigma=sigma, dsigma=dsigma, sigmah=sigmah, ps=ps, cols=out)


def after(col, c):
    """The state mksbm starts from: the column after the step's tendencies so far, over deltsec2."""
    return col['t'] + col['dtdt'] * c['deltsec2'], col['q'] + col['dqdt'] * c['deltsec2']


# ------------------------------------------------------------------------------------------------------- Fortran

STUB = """
      module rainmod
      integer, parameter :: NHOR={nhor}, NLEV={nlev}, NLEP={nlev}+1, NLEM={nlev}-1, NLON={nhor}, NLAT=1, NROOT=0
      real :: dt(NHOR,NLEP), dq(NHOR,NLEP), dtdt(NHOR,NLEP), dqdt(NHOR,NLEP), dqt(NHOR,NLEP), dp(NHOR)
      real :: du(NHOR,NLEP), dv(NHOR,NLEP), dudt(NHOR,NLEP), dvdt(NHOR,NLEP)
      real :: sigma(NLEV), dsigma(NLEV), sigmah(NLEV)
      real :: deltsec2, ga, gascon, akap, acpd, adv, alv, als, rdbrv, ra1, ra2, ra4, tmelt
      real :: pdeep = 999999., pdeepth = 70000., rkshallow = 10.
      real :: dprcl(NHOR,NLEV), dprscl(NHOR,NLEV), dgp3d(NHOR,NLEV,25)
      integer :: icclev(NHOR,NLEV), icctot(NHOR), iprobe(NHOR,4)
      integer :: ndiaggp = 1, nshallow = 1, nmoment = 0, ndheat = 0, nprint = 0, nprhor = 1, mypid = 0, nud = 6
      integer :: nprc = 2
{declarations}      end module rainmod

      subroutine mpgagp(pf,pp,klev)
      integer klev
      real pf(*), pp(*)
      end subroutine mpgagp
      subroutine sbmnight(pmuz)
      real pmuz(*)
      end subroutine sbmnight
"""
WRAPPER = """
      subroutine {name}(pt,pq,kshallow,klift,ktop,pdtdt,pdqdt)
      use rainmod
      integer kshallow(NHOR), klift(NHOR), ktop(NHOR)
      real pt(NHOR,NLEV), pq(NHOR,NLEV), pdtdt(NHOR,NLEV), pdqdt(NHOR,NLEV)
      iprobe(:,1)=kshallow(:)
      iprobe(:,2)=klift(:)
      iprobe(:,3)=ktop(:)
      call {name}_real(pt,pq,kshallow,klift,ktop,pdtdt,pdqdt)
      iprobe(:,4)=ktop(:)
      end subroutine {name}
"""
# A stand-in for mkshallow that mixes nothing, so that a column's tendencies are the deep scheme's alone
NO_MIXING = """
      subroutine mkshallow_real(pt,pq,kshallow,klift,ktop,pdtdt,pdqdt)
      use rainmod
      integer kshallow(NHOR), klift(NHOR), ktop(NHOR)
      real pt(NHOR,NLEV), pq(NHOR,NLEV), pdtdt(NHOR,NLEV), pdqdt(NHOR,NLEV)
      pdtdt(:,:)=0.
      pdqdt(:,:)=0.
      end subroutine mkshallow_real
"""
HARNESS = """
      program harness
      use rainmod
      implicit none
      integer :: jhor, jlev
      real :: zt0(NHOR,NLEP), zq0(NHOR,NLEP)
      read(*,*) {constants}
      read(*,*) nprc{settings}
      read(*,*) sigma, dsigma, sigmah
      do jhor=1,NHOR
       read(*,*) dp(jhor)
       read(*,*) (dt(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dq(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dtdt(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dqdt(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dqt(jhor,jlev), jlev=1,NLEV)
      enddo
      zt0(:,:)=dtdt(:,:)
      zq0(:,:)=dqdt(:,:)
{calls}
      contains
      subroutine report
      do jhor=1,NHOR
       write(*,'(*(es25.16e3))') (dtdt(jhor,jlev)-zt0(jhor,jlev), jlev=1,NLEV)
       write(*,'(*(es25.16e3))') (dqdt(jhor,jlev)-zq0(jhor,jlev), jlev=1,NLEV)
       write(*,'(*(es25.16e3))') (dprcl(jhor,jlev), jlev=1,NLEV)
       write(*,'(*(es25.16e3))') (dgp3d(jhor,jlev,8), jlev=1,NLEV), (dgp3d(jhor,jlev,16), jlev=1,NLEV), &
     &   (dgp3d(jhor,jlev,18), jlev=1,NLEV)
       write(*,'(*(i6))') (icclev(jhor,jlev), jlev=1,NLEV), icctot(jhor), iprobe(jhor,:)
      enddo
      end subroutine report
      end program harness
"""
CALL = """      dtdt(:,:)=zt0(:,:)
      dqdt(:,:)=zq0(:,:)
      dgp3d(:,:,:)=0.
      iprobe(:,:)=-9
      call {routine}
      call report
"""
# Terluna's settings in its design build that the lab's routine leaves out: the depth in Pa, the CAPE trigger and
# the night switch, the last two compiled in at their defaults, which hold them off
TERLUNA_ONLY = ('dpdeep_bm', 'cape_bm', 'epst_bm', 'ndiagnight_bm')


def routine(text: str, name: str) -> str:
    """A routine's text, from its first line through its end."""
    start = min(s for s in (text.find(f'      subroutine {name}{end}') for end in ('\n', '(')) if s >= 0)
    end = text.index(f'      end subroutine {name}\n') + len(f'      end subroutine {name}\n')
    return text[start:end]


def module_part(text: str) -> list:
    return text[:text.index('      end module rainmod\n')].splitlines(keepends=True)


def additions(patched: str, before: str) -> str:
    """The lines a patched rainmod.f90 adds to the module's own part, its declarations, in order."""
    old = module_part(before)
    return ''.join(line for line in module_part(patched) if line not in old)


class Builds:
    """Harnesses compiled from the series' points, and with Terluna's design routine beside the lab's, each once."""

    def __init__(self, series_sources, root, design: str | None = None):
        self.series, self.root, self.design, self.built = series_sources, root, design, {}
        self.before = series_sources.source('rainmod.f90', series_sources.before(SCHEME))

    def names(self, point: str) -> tuple:
        out = ()
        for patch in (SCHEME, DEPTH, CAP):
            out += POINT[patch]
            if patch == point:
                return out
        raise ValueError(point)

    def harness(self, point: str, nhor: int, nlev: int, flags=GCM_FLAGS, terluna: bool = False,
                mixing: bool = True):
        """The harness of mksbm at the series' point `point`, with Terluna's design routine beside it where
        `terluna`, and with PlaSim's mkshallow, or with a stand-in that mixes nothing where `mixing` is false."""
        key = (point, nhor, nlev, flags, terluna, mixing)
        if key in self.built:
            return self.built[key]
        text = self.series.source('rainmod.f90', point)
        names = self.names(point)
        declarations = additions(text, self.before)
        shallow = routine(text, 'mkshallow').replace('subroutine mkshallow(', 'subroutine mkshallow_real(').replace(
            'end subroutine mkshallow\n', 'end subroutine mkshallow_real\n') if mixing else NO_MIXING
        code = routine(text, 'mksbm') + shallow + WRAPPER.format(name='mkshallow')
        calls = CALL.format(routine='mksbm')
        if terluna:
            design = self.design
            declarations += ''.join(line for line in module_part(design)
                                    if re.match(rf'\s+(real|integer) :: ({"|".join(TERLUNA_ONLY)})\b', line))
            names += TERLUNA_ONLY
            code += routine(design, 'mksbm').replace('subroutine mksbm\n', 'subroutine mksbm_t\n').replace(
                'call mkshallow(', 'call mkshallow_t(')
            code += routine(design, 'mkshallow').replace('subroutine mkshallow(', 'subroutine mkshallow_t_real(').replace(
                'end subroutine mkshallow\n', 'end subroutine mkshallow_t_real\n') + WRAPPER.format(name='mkshallow_t')
            calls += CALL.format(routine='mksbm_t')
        folder = self.root / f'build{len(self.built)}'
        folder.mkdir()
        files = {'stub.f90': STUB.format(nhor=nhor, nlev=nlev, declarations=declarations), 'scheme.f90': code,
                 'harness.f90': HARNESS.format(constants=', '.join(CONSTANTS), settings=''.join(f', {n}' for n in names),
                                               calls=calls)}
        for name, body in files.items():
            (folder / name).write_text(body)
        subprocess.run(['gfortran', *flags, '-o', 'harness', *files], cwd=folder, check=True, capture_output=True)
        self.built[key] = (folder / 'harness', names)
        return self.built[key]


def harness_input(c, cols, names, settings, nprc=2) -> str:
    value = lambda n: str(int(settings[n])) if n in INTEGERS else repr(float(settings[n]))
    lines = [num([c[k] for k in CONSTANTS]), ' '.join([str(nprc)] + [value(n) for n in names]),
             num(np.r_[cols['sigma'], cols['dsigma'], cols['sigmah']])]
    for col in cols['cols']:
        lines += [num(cols['ps'])] + [num(col[k]) for k in ('t', 'q', 'dtdt', 'dqdt', 'dqt')]
    return '\n'.join(lines) + '\n'


def run(exe, text) -> str:
    done = subprocess.run([str(exe)], input=text, capture_output=True, text=True)
    assert done.returncode == 0, done.stdout[-500:] + done.stderr[-2000:]
    return done.stdout


def parse(stdout: str, n: int, nlev: int, passes: int = 1) -> list:
    """Each pass's fields by column: the tendencies, the rain by level, the diagnostics 8, 16 and 18, the convective
    cloud layers and their count, and what mksbm handed mkshallow (shallow, lift, top) with the top it kept."""
    rows = stdout.strip('\n').split('\n')
    assert len(rows) == 5 * n * passes
    out = []
    for i in range(passes):
        cols = []
        for j in range(n):
            r = rows[5 * (i * n + j):5 * (i * n + j + 1)]
            ints = np.array(r[4].split(), int)
            diag = np.array(r[3].split(), float)
            cols.append(dict(dtdt=np.array(r[0].split(), float), dqdt=np.array(r[1].split(), float),
                             rain=np.array(r[2].split(), float), diag8=diag[:nlev], diag16=diag[nlev:2 * nlev],
                             diag18=diag[2 * nlev:], clouds=ints[:nlev], count=ints[nlev], shallow=ints[nlev + 1],
                             lift=ints[nlev + 2], top_in=ints[nlev + 3], top_out=ints[nlev + 4]))
        out.append(cols)
    return out


@pytest.fixture(scope='module')
def builds(series_sources, tmp_path_factory):
    return Builds(series_sources, tmp_path_factory.mktemp('betts_miller'))


WORLDS = {   # constants, half levels and surface pressure: Earth's on PlaSim's ten, the Open Moon on Terluna's fifteen
             # and on forty, and the Moon's air at 0.5 bar
    'earth': (EARTH, plasim_half(), 101325.0),
    'moon15': (LUNAR, HALF15, 121590.0),
    'moon40': (LUNAR, HALF40, 121590.0),
    'moon_half_bar': (LUNAR, HALF15, 60795.0),
}
ALL_KINDS = ('deep', 'deep', 'dry', 'held', 'thin', 'stable', 'deep', 'dry', 'middle')


def world_columns(name, seed=3, kinds=ALL_KINDS):
    c, half, ps = WORLDS[name]
    return c, columns(c, half, ps, kinds, seed)


def agrees(got: list, cols: dict, c: dict, settings: dict, label) -> list:
    """The harness's fields against the Python copy's, to 1e-10 of each field's largest value, the decisions and the
    tops exactly; returns the copy's columns."""
    n = len(cols['sigma'])
    found = []
    for col, g in zip(cols['cols'], got):
        t, q = after(col, c)
        py = column(t, q, cols['sigma'], cols['dsigma'], cols['ps'], c, settings)
        found.append(py)
        for key in ('dtdt', 'dqdt', 'rain'):
            scale = max(np.abs(py[key]).max(), 1e-30)
            assert np.abs(g[key] - py[key]).max() <= 1e-10 * scale, (label, col['kind'], key)
        assert np.array_equal(g['clouds'], py['clouds']) and g['count'] == np.count_nonzero(py['clouds'])
        # Kuo's diagnostics: the heating (8) and the vapour in m/s of water (16) that the convection adds, here the deep
        # scheme's alone, and the dynamics' vapour (18)
        water = cols['ps'] * cols['dsigma'] / c['ga'] / 1000.0
        assert np.abs(g['diag8'] - g['dtdt']).max() <= 1e-12 * max(np.abs(g['dtdt']).max(), 1e-30)
        assert np.abs(g['diag16'] - g['dqdt'] * water).max() <= 1e-12 * max(np.abs(g['dqdt'] * water).max(), 1e-30)
        assert np.abs(g['diag18'] - col['dqt'] * water).max() <= 1e-12 * np.abs(col['dqt'] * water).max()
        shallow = py['shallow_top'] is not None
        assert g['shallow'] == int(shallow), (label, col['kind'], py['decision'])
        if shallow:   # Fortran counts levels from 1, the copy from 0
            assert (g['lift'], g['top_in']) == (n + 1, py['shallow_top'] + 1), (label, col['kind'], py['decision'])
    return found


# ------------------------------------------------------------------------------------------------------- the copy

@FORTRAN
@pytest.mark.parametrize('world', list(WORLDS))
def test_the_fortran_gives_the_copys_scheme_on_every_kind_of_column(tmp_path, builds, world):
    c, cols = world_columns(world)
    n, nlev = len(cols['cols']), len(cols['sigma'])
    settings_sets = {'design': DESIGN, 'no_depth': DEFAULTS, 'held': dict(DESIGN, cin_bm=5.0),
                     'mixing': dict(DESIGN, eps_bm=2.4, nsub_bm=16), 'mixing_once': dict(DESIGN, eps_bm=2.4),
                     'slow': dict(DESIGN, tau_bm=43200.0, rh_bm=0.6)}
    decisions = set()
    for label, settings in settings_sets.items():
        exe, names = builds.harness(CAP, n, nlev, mixing=False)
        got = parse(run(exe, harness_input(c, cols, names, settings)), n, nlev)[0]
        decisions |= {py['decision'] for py in agrees(got, cols, c, settings, (world, label))}
    assert decisions == {'deep', 'dry', 'held', 'thin', 'stable'}, decisions
    # A deep cloud topped below sigma 0.4 takes no anvil, and one topped above it does
    anvils = {}
    for col, g in zip(cols['cols'], parse(run(builds.harness(CAP, n, nlev, mixing=False)[0],
                                              harness_input(c, cols, builds.harness(CAP, n, nlev, mixing=False)[1],
                                                            DESIGN)), n, nlev)[0]):
        if g['rain'].sum() > 0.0:
            top = int(np.flatnonzero(g['clouds'])[0])
            anvils[cols['sigma'][top] < 0.4] = g['clouds'][top]
    assert anvils == {True: 2, False: 1}, (world, anvils)


@FORTRAN
def test_the_scheme_relaxes_over_tau_rains_the_vapour_lost_and_keeps_the_moist_enthalpy(builds):
    for world in WORLDS:
        c, cols = world_columns(world, seed=7, kinds=('deep',) * 6)
        n, nlev = len(cols['cols']), len(cols['sigma'])
        exe, names = builds.harness(CAP, n, nlev)
        sigma, dsigma, ps = cols['sigma'], cols['dsigma'], cols['ps']
        m = ps * dsigma / c['ga']
        fast, slow, held = (parse(run(exe, harness_input(c, cols, names, dict(DESIGN, tau_bm=tau))), n, nlev)[0]
                            for tau in (7200.0, 14400.0, 1800.0))
        deep = 0
        for col, f, s, h in zip(cols['cols'], fast, slow, held):
            t, q = after(col, c)
            py = column(t, q, sigma, dsigma, ps, c, DESIGN)
            if py['decision'] != 'deep':
                continue
            deep += 1
            top, tp = py['top'], py['reference_t']
            layers = slice(top, nlev)
            # The vapour relaxes toward rh_bm of saturation at the reference temperature over tau_bm
            want = (0.7 * np.array([saturation(tp[j], ps * sigma[j], c) for j in range(top, nlev)]) - q[layers]) / 7200.0
            assert np.abs(f['dqdt'][layers] - want).max() <= 1e-12 * np.abs(want).max(), world
            # and the temperature toward the reference, shifted at every convecting level by one heating
            shift = f['dtdt'][layers] - (tp[layers] - t[layers]) / 7200.0
            assert np.ptp(shift) <= 1e-12 * np.abs(f['dtdt'][layers]).max() and np.all(f['dtdt'][:top] == 0.0)
            # Twice the time halves every tendency and the rain; a time below deltsec2 takes deltsec2
            for key in ('dtdt', 'dqdt', 'rain'):
                scale = np.abs(f[key]).max()
                assert np.abs(s[key] - 0.5 * f[key]).max() <= 1e-12 * scale, (world, key)
                assert np.abs(h[key] - 2.0 * f[key]).max() <= 1e-12 * scale, (world, key)
            # The rain is the vapour the column loses: per square metre, its sum over the levels equals the column's
            # loss of vapour, and it forms where the vapour is removed
            rain = (f['rain'] * ps / c['ga']).sum()
            lost = -(f['dqdt'] * m).sum()
            assert rain > 0.0 and abs(rain - lost) <= 1e-12 * rain, world
            assert np.array_equal(f['rain'] > 0.0, f['dqdt'] < 0.0)
            # The column keeps its moist enthalpy: the heating releases the rain's latent heat
            cp = c['acpd'] * (1.0 + c['ADV'] * q)
            enthalpy = (cp * f['dtdt'] * m).sum() + c['ALV'] * (f['dqdt'] * m).sum()
            assert abs(enthalpy) <= 1e-12 * c['ALV'] * rain, world
        assert deep >= 4, (world, deep)


@FORTRAN
def test_the_depth_test_turns_deep_to_shallow_at_its_share_of_the_surface_pressure(builds):
    """Deep columns at Earth's surface pressure and at the Open Moon's air at 1.2 and 0.5 bar: each turns from deep to
    shallow, where the shallow scheme takes it, as the share passes its cloud's depth over its surface pressure."""
    for world in ('moon15', 'moon_half_bar', 'earth'):
        c, cols = world_columns(world, seed=11, kinds=('deep',) * 5)
        n, nlev = len(cols['cols']), len(cols['sigma'])
        exe, names = builds.harness(CAP, n, nlev)
        sigma, ps = cols['sigma'], cols['ps']
        shares = {}
        for j, col in enumerate(cols['cols']):
            t, q = after(col, c)
            py = column(t, q, sigma, cols['dsigma'], ps, c, DESIGN)
            if py['decision'] == 'deep':
                shares[j] = (py['base'] - ps * sigma[py['top']]) / ps
        assert len(shares) >= 3, (world, shares)
        for j, share in shares.items():
            for factor, deep in ((1.0 - 1e-9, True), (1.0 + 1e-9, False)):
                got = parse(run(exe, harness_input(c, cols, names, dict(DESIGN, dsigdeep_bm=share * factor))), n,
                            nlev)[0][j]
                assert bool(got['rain'].sum() > 0.0) is deep and got['shallow'] == int(not deep), (world, j, factor)


@FORTRAN
def test_the_inhibition_limit_holds_back_a_column_whose_inhibition_exceeds_it(builds):
    """Deep columns whose parcel crosses colder air below its level of free convection: each convects deep under a
    limit just above its inhibition, R sum(max(0, T - T_ref) dsigma/sigma) over the levels below that level as the copy
    counts it, and goes to the shallow scheme under a limit just below it."""
    for world in WORLDS:
        c, cols = world_columns(world, seed=29, kinds=('held',) * 4 + ('deep',) * 4)
        n, nlev = len(cols['cols']), len(cols['sigma'])
        exe, names = builds.harness(CAP, n, nlev, mixing=False)
        held = 0
        for j, col in enumerate(cols['cols']):
            py = column(*after(col, c), cols['sigma'], cols['dsigma'], cols['ps'], c, DESIGN)
            if py['decision'] != 'deep' or py['cin'] == 0.0:
                continue
            held += 1
            for factor, deep in ((1.0 + 1e-9, True), (1.0 - 1e-9, False)):
                got = parse(run(exe, harness_input(c, cols, names, dict(DESIGN, cin_bm=py['cin'] * factor))), n,
                            nlev)[0][j]
                assert bool(got['rain'].sum() > 0.0) is deep and got['shallow'] == int(not deep), (world, j, factor)
        assert held >= 3, (world, held)


@FORTRAN
def test_the_shallow_cap_hands_mkshallow_the_highest_level_within_the_share_of_the_base(builds):
    """Columns too dry to rain or held back, their clouds deeper than the share: without the cap mkshallow takes the
    parcel's top and lowers it to PlaSim's 700 hPa top where it lies above; with it the top is the highest level at or
    below the parcel's top whose pressure lies within the share of the cloud's base, which mkshallow keeps. Since the
    depth test hands a thinner cloud to the shallow scheme before the cap, the cap binds on every cloud it reaches, and
    a thin cloud keeps its parcel's top."""
    bound = thin = 0
    for world in WORLDS:
        c, cols = world_columns(world, seed=5, kinds=('dry', 'held', 'thin', 'dry', 'held', 'thin', 'dry'))
        n, nlev = len(cols['cols']), len(cols['sigma'])
        exe, names = builds.harness(CAP, n, nlev)
        sigma, ps = cols['sigma'], cols['ps']
        held = dict(DESIGN, cin_bm=5.0)
        for share in (DESIGN['dsigdeep_bm'], 0.6):
            capped, open_ = (parse(run(exe, harness_input(c, cols, names, dict(held, dsigdeep_bm=share,
                                                                                nshcap_bm=cap))), n, nlev)[0]
                             for cap in (1, 0))
            for col, g, o in zip(cols['cols'], capped, open_):
                t, q = after(col, c)
                py = column(t, q, sigma, cols['dsigma'], ps, c, dict(held, dsigdeep_bm=share))
                top, p = py['top'], ps * sigma
                if py['decision'] == 'thin':
                    assert (g['shallow'], g['top_in'], g['top_out']) == (1, top + 1, top + 1), (world, share)
                    thin += 1
                if py['decision'] not in ('dry', 'held'):
                    continue
                within = [j for j in range(top, nlev) if p[j] >= py['base'] - share * ps]
                cap_top = within[0] if within else nlev - 1
                assert (g['shallow'], g['top_in'], g['top_out']) == (1, cap_top + 1, cap_top + 1), (world, share)
                # Without the cap: the parcel's top, lowered to the lowest level above 700 hPa (PlaSim's pdeepth)
                plasim = max([j for j in range(1, nlev - 1) if p[j] < 70000.0], default=0) + 1
                assert (o['top_in'], o['top_out']) == (top + 1, max(top + 1, plasim)), (world, share)
                assert cap_top > top
                bound += 1
    assert bound >= 6 and thin >= 3, (bound, thin)


# ------------------------------------------------------------------------------------------------------- the rain

CHAIN_STUB = """
      module rainmod
      integer, parameter :: NHOR={nhor}, NLEV={nlev}, NLEP={nlev}+1, NLEM={nlev}-1, NLON={nhor}, NLAT=1, NROOT=0
      real :: dt(NHOR,NLEP), dq(NHOR,NLEP), dtdt(NHOR,NLEP), dqdt(NHOR,NLEP), dqt(NHOR,NLEP), dp(NHOR)
      real :: du(NHOR,NLEP), dv(NHOR,NLEP), dudt(NHOR,NLEP), dvdt(NHOR,NLEP)
      real :: sigma(NLEV), dsigma(NLEV), sigmah(NLEV)
      real :: deltsec, deltsec2, ga, gascon, akap, acpd, adv, alv, als, rdbrv, ra1, ra2, ra4, tmelt, gamma
      real :: pdeep = 999999., pdeepth = 70000., rkshallow = 10.
      real :: dprcl(NHOR,NLEV), dprscl(NHOR,NLEV), dprll(NHOR,NLEV), dprsll(NHOR,NLEV), dgp3d(NHOR,NLEV,25)
      real :: dprc(NHOR), dprl(NHOR), dprs(NHOR)
      real :: dentropy(NHOR,40), dentro(NHOR), dentrot(NHOR,NLEV), dentroq(NHOR,NLEV), dentrop(NHOR)
      real :: dentro3d(NHOR,NLEV,40), denergy(NHOR,40), dener3d(NHOR,NLEV,40)
      integer :: icclev(NHOR,NLEV), icctot(NHOR)
      integer :: ndiaggp = 1, nshallow = 1, nmoment = 0, ndheat = 0, nprint = 0, nprhor = 1, mypid = 0, nud = 6
      integer :: nprc = 2, nentropy = 0, nentro3d = 0, nenergy = 0, nener3d = 0, nevapprec = 1
{declarations}      end module rainmod

      subroutine mpgagp(pf,pp,klev)
      integer klev
      real pf(*), pp(*)
      end subroutine mpgagp
      subroutine mpbci(k)
      integer k
      end subroutine mpbci
      subroutine mpbcr(p)
      real p
      end subroutine mpbcr
      subroutine mpbcrn(p,n)
      integer n
      real p(n)
      end subroutine mpbcrn
      subroutine mpabort(ym)
      character(len=*) :: ym
      write(*,'(a)') 'ABORT '//trim(ym)
      stop 2
      end subroutine mpabort
"""
CHAIN = """
      program chain
      use rainmod
      implicit none
      integer :: jhor, jlev
      real :: zt1(NHOR,NLEP), zq1(NHOR,NLEP)
      read(*,*) {constants}
      read(*,*) nprc{settings}
      read(*,*) nevapprec{rain}
      read(*,*) sigma, dsigma, sigmah
      do jhor=1,NHOR
       read(*,*) dp(jhor)
       read(*,*) (dt(jhor,jlev), jlev=1,NLEP)
       read(*,*) (dq(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dtdt(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dqdt(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dqt(jhor,jlev), jlev=1,NLEV)
      enddo
      if(nevapprec == 2) call rdropini
      dprll(:,:)=0.
      dprsll(:,:)=0.
      call mksbm
      zt1(:,:)=dtdt(:,:)
      zq1(:,:)=dqdt(:,:)
      call mkrain
      do jhor=1,NHOR
       write(*,'(*(es25.16e3))') (dprcl(jhor,jlev), jlev=1,NLEV)
       write(*,'(*(es25.16e3))') (zt1(jhor,jlev), jlev=1,NLEV), (zq1(jhor,jlev), jlev=1,NLEV)
       write(*,'(*(es25.16e3))') (dtdt(jhor,jlev)-zt1(jhor,jlev), jlev=1,NLEV), (dqdt(jhor,jlev)-zq1(jhor,jlev), &
     &   jlev=1,NLEV)
       write(*,'(*(es25.16e3))') dprc(jhor), dprl(jhor), dprs(jhor)
      enddo
      end program chain
"""


@pytest.fixture(scope='module')
def rain_worlds():
    """The fall law and the births that patch 14 reads, as the rain's own test makes them: Earth's air with births
    made up for the test, and the Open Moon's air with Terluna's calibration; each with PlaSim's constants of
    test_rain_drops and the levels and surface pressure of the scheme's columns here."""
    earth_air = drops.Column(gravity_m_s2=STANDARD_GRAVITY, surface_pressure_pa=breakup.ATMOSPHERE_PA,
                             surface_temperature_k=rain.RESORT_K, surface_relative_humidity=rain.RESORT_HUMIDITY,
                             air=DryAir(breakup.ATMOSPHERE_PA))
    moon_air = drops.Column(gravity_m_s2=MOON_SURFACE_GRAVITY, surface_pressure_pa=1.2 * breakup.ATMOSPHERE_PA,
                            surface_temperature_k=rain.RESORT_K, surface_relative_humidity=rain.RESORT_HUMIDITY,
                            air=earthlike_air(1.2 * breakup.ATMOSPHERE_PA, 400.0))
    return {'earth': rain.World(dict(rain.EARTH, akap=0.286), plasim_half(), 101325.0, 6.5e-3, 6.0, earth_air,
                                rain.EARTH_BIRTHS),
            'moon15': rain.World(dict(rain.LUNAR, akap=0.286), HALF15, 121590.0, 1.15e-3, 1.0, moon_air,
                                 rd.TERLUNA_OPEN_MOON_BIRTHS)}


@FORTRAN
def test_the_schemes_rain_by_level_falls_through_the_drops_evaporation(series_sources, tmp_path, rain_worlds):
    """mksbm and the patched mkrain, both from patch 20's point of the series, compiled into one program and called as
    rainstep calls them: the rain the scheme forms at each level (dprcl, with no snow, dprscl, which mkrain sorts by
    temperature) enters the falling rain at that level, and with nevapprec 2 mkrain's tendencies and the precipitation
    at the ground are those of patch 14's Python copy given the scheme's rain, to 1e-10, on Earth's air and the Open
    Moon's. Rain formed aloft evaporates below its levels, the column keeps its water, and the drops evaporate another
    amount of the scheme's rain than gamma does."""
    text = series_sources.source('rainmod.f90', CAP)
    before = series_sources.source('rainmod.f90', series_sources.before(rain.RAIN_PATCH))
    names = POINT[SCHEME] + POINT[DEPTH] + POINT[CAP]
    constants = CONSTANTS + ('deltsec', 'gamma')
    for world, w in rain_worlds.items():
        c = w.c
        cols = columns(c, w.half, w.pressure_pa, ('deep',) * 6, seed=23)
        n, nlev = len(cols['cols']), len(cols['sigma'])
        folder = tmp_path / world
        folder.mkdir()
        code = (routine(text, 'mksbm') + routine(text, 'mkshallow') + rain.mkrain_code(text, 'rdropevap'))
        files = {'stub.f90': CHAIN_STUB.format(nhor=n, nlev=nlev, declarations=additions(text, before)),
                 'scheme.f90': code,
                 'chain.f90': CHAIN.format(constants=', '.join(constants), settings=''.join(f', {x}' for x in names),
                                           rain=''.join(f', {x}' for x in rd.NAMELIST_NAMES))}
        for name, body in files.items():
            (folder / name).write_text(body)
        subprocess.run(['gfortran', *GCM_FLAGS, '-o', 'chain', *files], cwd=folder, check=True, capture_output=True)
        (folder / fall_law.TABLE_FILE).write_text(fall_law.table_text(w.found['table']))
        value = lambda x: str(int(DESIGN[x])) if x in INTEGERS else repr(float(DESIGN[x]))

        def chain(nevapprec):
            lines = [num([c[k] for k in constants]), ' '.join(['2'] + [value(x) for x in names]),
                     f'{nevapprec} ' + ' '.join(repr(w.prm[k]) for k in rd.NAMELIST_NAMES),
                     num(np.r_[cols['sigma'], cols['dsigma'], cols['sigmah']])]
            for col in cols['cols']:
                lines += [num(cols['ps']), num(np.r_[col['t'], col['t'][-1] + 1.0])]
                lines += [num(col[k]) for k in ('q', 'dtdt', 'dqdt', 'dqt')]
            done = subprocess.run([str(folder / 'chain')], input='\n'.join(lines) + '\n', capture_output=True,
                                  text=True, cwd=folder)
            assert done.returncode == 0, done.stdout[-500:] + done.stderr[-2000:]
            rows = [np.array(r.split(), float) for r in done.stdout.strip('\n').split('\n')]
            assert len(rows) == 4 * n
            return [dict(births=rows[4 * j], dtdt=rows[4 * j + 1][:nlev], dqdt=rows[4 * j + 1][nlev:],
                         rain_dtdt=rows[4 * j + 2][:nlev], rain_dqdt=rows[4 * j + 2][nlev:], ground=rows[4 * j + 3])
                    for j in range(n)]

        drops_, gamma_ = chain(2), chain(1)
        s = dict(dt=np.array([np.r_[col['t'], col['t'][-1] + 1.0] for col in cols['cols']]),
                 dq=np.array([col['q'] for col in cols['cols']]), dp=np.full(n, cols['ps']), sigma=cols['sigma'],
                 dsigma=cols['dsigma'], dtdt=np.array([f['dtdt'] for f in drops_]),
                 dqdt=np.array([f['dqdt'] for f in drops_]), dprcl=np.array([f['births'] for f in drops_]),
                 dprscl=np.zeros((n, nlev)), dprll=np.zeros((n, nlev)), dprsll=np.zeros((n, nlev)))
        py = rain.copy(s)
        out = rd.mkrain(py, c, w.prm, w.law)
        got = lambda key: np.array([f[key] for f in drops_])
        for mine, want in ((got('rain_dtdt'), py['dtdt'] - s['dtdt']), (got('rain_dqdt'), py['dqdt'] - s['dqdt']),
                           (got('ground'), np.c_[out['dprc'], out['dprl'], out['dprs']])):
            assert np.abs(mine - want).max() <= 1e-10 * np.abs(want).max(), world
        raining = 0
        for f, g in zip(drops_, gamma_):
            births = (f['births'] * cols['ps'] / c['ga']).sum()             # kg/m2/s
            if births == 0.0:
                continue
            raining += 1
            top = np.flatnonzero(f['births'] > 0.0)[0]
            evaporated = (f['rain_dqdt'] * cols['ps'] * cols['dsigma'] / c['ga'])
            assert evaporated[top + 1:].sum() > 0.0 and np.all(evaporated[:top] == 0.0), world
            assert abs(births - evaporated.sum() - 1000.0 * f['ground'][0]) <= 1e-10 * births, world
            assert f['ground'][1] == 0.0 and not np.isclose(f['ground'][0], g['ground'][0], rtol=1e-6, atol=0.0)
        assert raining >= 4, (world, raining)


# ------------------------------------------------------------------------------------------------------- identity

@FORTRAN
@pytest.mark.parametrize('flags', [GCM_FLAGS, NATIVE_FLAGS], ids=['exoplasim', 'native'])
def test_each_patch_at_its_defaults_prints_every_digit_of_the_routine_before_it(builds, flags):
    """Patch 19 with no depth test and one mixing step a layer prints what patch 18 prints, with the parcel undiluted
    and mixing; patch 20 without the cap prints what patch 19 prints, with the depth test and without it."""
    for world in WORLDS:
        c, cols = world_columns(world, seed=13)
        n, nlev = len(cols['cols']), len(cols['sigma'])
        for settings in (DEFAULTS, dict(DEFAULTS, eps_bm=2.4), dict(DEFAULTS, cin_bm=5.0, tau_bm=1800.0)):
            outs = [run(builds.harness(point, n, nlev, flags)[0],
                        harness_input(c, cols, builds.harness(point, n, nlev, flags)[1], settings))
                    for point in (SCHEME, DEPTH, CAP)]
            assert outs[0] == outs[1] == outs[2], (world, settings)
        for settings in (dict(DEFAULTS, dsigdeep_bm=0.2), dict(DEFAULTS, dsigdeep_bm=0.2, eps_bm=2.4, nsub_bm=8)):
            outs = [run(builds.harness(point, n, nlev, flags)[0],
                        harness_input(c, cols, builds.harness(point, n, nlev, flags)[1], settings))
                    for point in (DEPTH, CAP)]
            assert outs[0] == outs[1], (world, settings)
        # With the cap on, the output changes where a deep cloud goes to the shallow scheme
        exe, names = builds.harness(CAP, n, nlev, flags)
        assert run(exe, harness_input(c, cols, names, DESIGN)) != \
            run(exe, harness_input(c, cols, names, dict(DESIGN, nshcap_bm=0)))


SHALLOW = """
      program shallow
      use rainmod
      implicit none
      integer :: jhor, jlev, ks(NHOR), kl(NHOR), kt(NHOR)
      real :: zt(NHOR,NLEV), zq(NHOR,NLEV), zdt(NHOR,NLEV), zdq(NHOR,NLEV)
      read(*,*) {constants}
      read(*,*) nprc{settings}
      read(*,*) sigma, dsigma, sigmah
      read(*,*) ks, kl, kt
      do jhor=1,NHOR
       read(*,*) dp(jhor)
       read(*,*) (zt(jhor,jlev), jlev=1,NLEV)
       read(*,*) (zq(jhor,jlev), jlev=1,NLEV)
      enddo
      call mkshallow(zt,zq,ks,kl,kt,zdt,zdq)
      do jhor=1,NHOR
       write(*,'(*(es25.16e3))') (zdt(jhor,jlev), jlev=1,NLEV), (zdq(jhor,jlev), jlev=1,NLEV)
       write(*,'(i6)') kt(jhor)
      enddo
      end program shallow
"""


@FORTRAN
@pytest.mark.parametrize('flags', [GCM_FLAGS, NATIVE_FLAGS], ids=['exoplasim', 'native'])
def test_mkshallow_keeps_plasims_top_off_the_cap_and_the_caps_top_under_it(series_sources, tmp_path, flags):
    """mkshallow of the series before patch 18 and of patch 20, called on the same shallow columns: under Kuo's
    scheme, and under the Betts-Miller scheme without the cap or without the depth test, patch 20 prints every digit
    the released routine prints, which lowers each top to the lowest level above 700 hPa; with the cap and the depth
    test, it keeps the tops it is handed and mixes up to them."""
    before = series_sources.source('rainmod.f90', series_sources.before(SCHEME))
    after_ = series_sources.source('rainmod.f90', CAP)
    c, cols = world_columns('earth', seed=17, kinds=('deep', 'dry', 'held', 'thin', 'deep', 'dry'))
    n, nlev = len(cols['cols']), len(cols['sigma'])
    names = ('dsigdeep_bm', 'nshcap_bm')
    exes = {}
    for label, text in (('before', before), ('after', after_)):
        folder = tmp_path / label
        folder.mkdir()
        files = {'stub.f90': STUB.format(nhor=n, nlev=nlev, declarations=additions(after_, before)),
                 'shallow.f90': routine(text, 'mkshallow'),
                 'harness.f90': SHALLOW.format(constants=', '.join(CONSTANTS), settings=''.join(f', {x}' for x in names))}
        for name, body in files.items():
            (folder / name).write_text(body)
        subprocess.run(['gfortran', *flags, '-o', 'harness', *files], cwd=folder, check=True, capture_output=True)
        exes[label] = folder / 'harness'
    tops = [2, 3, 5, 6, 7, 8]                         # tops above and below 700 hPa on Earth's ten levels
    text = lambda nprc, share, cap: '\n'.join(
        [num([c[k] for k in CONSTANTS]), f'{nprc} {share!r} {cap}',
         num(np.r_[cols['sigma'], cols['dsigma'], cols['sigmah']]),
         ' '.join(['1'] * n), ' '.join([str(nlev + 1)] * n), ' '.join(map(str, tops))]
        + [line for col in cols['cols'] for line in (num(cols['ps']), num(after(col, c)[0]), num(after(col, c)[1]))]) + '\n'
    released = run(exes['before'], text(1, 0.0, 0))
    for case in ((1, 0.0, 0), (1, 0.2, 1), (2, 0.2, 0), (2, 0.0, 1)):
        assert run(exes['after'], text(*case)) == released, case
    capped = run(exes['after'], text(2, 0.2, 1))
    assert capped != released
    kept = [int(line) for line in capped.strip().split('\n')[1::2]]
    lowered = [int(line) for line in released.strip().split('\n')[1::2]]
    p = cols['ps'] * cols['sigma']
    plasim = max(j for j in range(1, nlev - 1) if p[j] < 70000.0) + 1
    assert kept == tops and lowered == [max(t, plasim) for t in tops] and lowered != tops


# ------------------------------------------------------------------------------------------------------- Terluna's

@pytest.fixture(scope='module')
def design_source():
    """The rainmod.f90 of Terluna's design build, read in place from its research drive, with the design run's record
    and namelist: the run's record names this source's hash and the design scheme, and its namelist sets it."""
    from worldlab import roots
    drive = roots.root('terluna-drive')
    if drive is None or not (drive / DESIGN_SOURCE).exists():
        pytest.skip("Terluna's research drive, which holds the design build's source, is absent")
    data = (drive / DESIGN_SOURCE).read_bytes()
    assert hashlib.sha256(data).hexdigest() == DESIGN_SHA256
    record = json.loads((drive / DESIGN_RUN / 'progress.json').read_text())['configuration']
    assert record['source']['rainmod'] == DESIGN_SHA256[:16]
    assert record['convection'] == dict(scheme='sbm', nprc=2, tau_s=7200.0, rh=0.7, eps=0.0, cin_j_kg=0.0,
                                        deep_hpa=200.0, shallow_cap=True)
    namelist = (drive / DESIGN_RUN / 'model' / 'rainmod_namelist').read_text()
    entries = dict(re.findall(r'^\s*(\w+)\s*=\s*(\S+)', namelist, flags=re.M))
    assert {k: float(entries[k]) for k in ('NPRC', 'TAU_BM', 'RH_BM', 'EPS_BM', 'CIN_BM', 'DPDEEP_BM', 'NSHCAP_BM')} == \
        dict(NPRC=2, TAU_BM=7200.0, RH_BM=0.7, EPS_BM=0.0, CIN_BM=0.0, DPDEEP_BM=DEEP_PA, NSHCAP_BM=1)
    assert not {'CAPE_BM', 'EPST_BM', 'NDIAGNIGHT_BM', 'NSUB_BM', 'NCLOS_BM'} & set(entries)
    return data.decode('latin-1')


def exact_share(ps: float) -> float:
    """The double s nearest 20,000/ps for which s*ps is 20,000 Pa exactly, as the lab's routine multiplies them."""
    s = DEEP_PA / ps
    for candidate in sorted((np.nextafter(s, s + k) if k else s for k in (-1.0, 0.0, 1.0)), key=lambda x: abs(x - s)):
        candidate = float(candidate)
        if candidate * ps == DEEP_PA:
            return candidate
    raise AssertionError(f'no double gives 20,000 Pa at {ps} Pa')


@FORTRAN
def test_the_labs_routine_prints_every_digit_of_terlunas_design_build(builds, design_source):
    """The design build's mksbm, with its CAPE trigger and night switch compiled in at their defaults, and its
    mkshallow, renamed and compiled into one program with the lab's: at Earth's gravity and the Moon's, at four surface
    pressures, on deep, thin, dry, held-back and stable columns, under the design scheme, with the inhibition limit,
    with the mixing within layers, without the cap and without the depth test, the lab's share set so that it comes to
    20,000 Pa exactly at the column's surface pressure. The two routines print the same digits in every tendency, rain,
    diagnostic, cloud layer and shallow top."""
    seen = set()
    for world in WORLDS:
        c, cols = world_columns(world, seed=19)
        n, nlev = len(cols['cols']), len(cols['sigma'])
        share = exact_share(cols['ps'])
        builds.design = design_source
        exe, names = builds.harness(CAP, n, nlev, terluna=True)
        lab_only = dict(cape_bm=0.0, epst_bm=0.0, ndiagnight_bm=0)
        for label, settings in (('design', dict(DESIGN, dsigdeep_bm=share, dpdeep_bm=DEEP_PA)),
                                ('held', dict(DESIGN, dsigdeep_bm=share, dpdeep_bm=DEEP_PA, cin_bm=5.0)),
                                ('mixing', dict(DESIGN, dsigdeep_bm=share, dpdeep_bm=DEEP_PA, eps_bm=2.4, nsub_bm=16)),
                                ('no_cap', dict(DESIGN, dsigdeep_bm=share, dpdeep_bm=DEEP_PA, nshcap_bm=0)),
                                ('no_depth', dict(DEFAULTS, dpdeep_bm=0.0))):
            out = run(exe, harness_input(c, cols, names, {**lab_only, **settings}))
            rows = out.strip('\n').split('\n')
            assert len(rows) == 10 * n
            assert rows[:5 * n] == rows[5 * n:], (world, label)
            seen |= {column(*after(col, c), cols['sigma'], cols['dsigma'], cols['ps'], c,
                            {**DEFAULTS, **{k: v for k, v in settings.items() if k in DEFAULTS}})['decision']
                     for col in cols['cols']}
    assert seen == {'deep', 'dry', 'held', 'thin', 'stable'}


# ------------------------------------------------------------------------------------------------------- the patches

def _added(series_sources, patch) -> list:
    return series_sources.added(patch)


def test_the_patches_hold_no_number_of_the_moons_and_declare_read_and_broadcast_each_name_once(series_sources):
    """The patches' statements hold no gravity, pressure or height: the scheme takes the run's gravity, levels and
    surface pressure. Their literals are Frierson's 2 h and 70%, Kuo's sigma 0.4 for an anvil's top and his diagnostic
    units (1000 kg/m3 of water), the bisection's 24 halvings and midpoint, and the switches' values."""
    statements = [re.sub(r"'[^']*'", '', line.split('!')[0]) for patch in (SCHEME, DEPTH, CAP)
                  for line in _added(series_sources, patch) if not line.lstrip().startswith('!')]
    literals = {float(x) for line in statements for x in re.findall(r'(?<![\w.])(\d+\.?\d*(?:e[-+]?\d+)?)', line)}
    assert literals <= {0.0, 1.0, 2.0, 0.4, 0.5, 0.7, 24.0, 1000.0, 7200.0, 8.0, 16.0, 18.0}, literals
    text = series_sources.source('rainmod.f90', CAP)
    namelist = text[text.index('      namelist/rainmod_nl/'):text.index('!     reset defaults')]
    for name in ('tau_bm', 'rh_bm', 'eps_bm', 'cin_bm', 'dsigdeep_bm', 'nsub_bm', 'nshcap_bm'):
        assert len(re.findall(rf'(real|integer) :: {name} *= ', text)) == 1, name
        assert len(re.findall(rf'call mpbc[ri]\({name}\)', text)) == 1, name
        assert len(re.findall(rf'\b{name}\b', namelist)) == 1, name
    assert text.count('      if(nprc == 2) call mksbm') == 1 and text.count('      if(nprc == 1) call kuo') == 1
    assert all(len(line) <= 132 for patch in (SCHEME, DEPTH, CAP) for line in _added(series_sources, patch))
    # Kuo's lines stay: of the released rainmod.f90 the patches take two lines, the test before mkdqtgp and PlaSim's
    # shallow top, and patch 19 rewrites lines of patch 18's mksbm alone
    removed = {patch: [line[1:] for line in (series_sources.folder / patch).read_text().splitlines()
                       if line.startswith('-') and not line.startswith('---')] for patch in (SCHEME, DEPTH, CAP)}
    assert removed[SCHEME] + removed[CAP] == ['      if(nprc == 1) call mkdqtgp', '      ktop(:)=MAX(ktop(:),kktop(:))']
    scheme = routine(series_sources.source('rainmod.f90', SCHEME), 'mksbm').splitlines()
    assert removed[DEPTH] and all(line in scheme for line in removed[DEPTH])
    before = series_sources.source('rainmod.f90', series_sources.before(SCHEME))
    assert routine(before, 'kuo') == routine(text, 'kuo')


STOPS = """
      program stops
      use rainmod
      implicit none
      read(*,*) nprc{settings}
{checks}      write(*,'(a)') 'ran'
      end program stops

      subroutine mpabort(ym)
      character(len=*) :: ym
      write(*,'(a)') 'ABORT '//trim(ym)
      stop 2
      end subroutine mpabort
"""


@FORTRAN
def test_the_scheme_stops_on_settings_out_of_range(series_sources, tmp_path):
    """rainini's checks of patches 18 to 20, run on their own: with nprc 2 each setting out of range stops the run
    with PlaSim's abort message, and with nprc 1 none of them is read."""
    text = series_sources.source('rainmod.f90', CAP)
    start = text.index('      if(nprc == 2) then\n       if(tau_bm')
    checks = text[start:text.index('      endif\n', start) + len('      endif\n')]
    names = POINT[SCHEME] + POINT[DEPTH] + POINT[CAP]
    files = {'stub.f90': STUB.format(nhor=1, nlev=2, declarations=additions(text, series_sources.source(
        'rainmod.f90', series_sources.before(SCHEME)))),
             'stops.f90': STOPS.format(settings=''.join(f', {n}' for n in names), checks=checks)}
    for name, body in files.items():
        (tmp_path / name).write_text(body)
    subprocess.run(['gfortran', *GCM_FLAGS, '-o', 'stops', *files], cwd=tmp_path, check=True, capture_output=True)
    go = lambda nprc, **changes: subprocess.run(
        [str(tmp_path / 'stops')], capture_output=True, text=True,
        input=' '.join([str(nprc)] + [str(int(v)) if k in INTEGERS else repr(float(v))
                                      for k, v in {**DESIGN, **changes}.items() if k in names]) + '\n')
    assert go(2).stdout.strip() == 'ran'
    for changes, message in ((dict(tau_bm=0.0), 'tau_bm is positive'), (dict(rh_bm=0.0), 'rh_bm lies above 0'),
                             (dict(rh_bm=1.2), 'rh_bm lies above 0'), (dict(eps_bm=-1.0), 'eps_bm and cin_bm'),
                             (dict(cin_bm=-1.0), 'eps_bm and cin_bm'), (dict(dsigdeep_bm=1.0), 'dsigdeep_bm lies in'),
                             (dict(dsigdeep_bm=-0.1), 'dsigdeep_bm lies in'), (dict(nsub_bm=0), 'nsub_bm is 1'),
                             (dict(dsigdeep_bm=0.0), 'nshcap_bm 1 takes dsigdeep_bm')):
        done = go(2, **changes)
        assert done.returncode == 2 and done.stdout.startswith('ABORT nprc 2: ') and message in done.stdout, changes
        assert len(done.stdout.strip().removeprefix('ABORT ')) <= 59
        assert go(1, **changes).stdout.strip() == 'ran'


@FORTRAN
def test_the_patched_rainmod_compiles_with_plasims_modules(tmp_path, series_sources):
    (tmp_path / 'resmod.f90').write_text('      module resmod\n      parameter(NLAT_ATM = 32)\n'
                                         '      parameter(NLEV_ATM = 15)\n      parameter(NPRO_ATM = 1)\n'
                                         '      end module resmod\n')
    for name in ('plasimmod.f90', 'rainmod.f90'):
        (tmp_path / name).write_text(series_sources.source(name, CAP), encoding='latin-1')
    for name in ('resmod.f90', 'plasimmod.f90', 'rainmod.f90'):
        subprocess.run(['gfortran', *GCM_FLAGS, '-c', name], cwd=tmp_path, check=True, capture_output=True)
