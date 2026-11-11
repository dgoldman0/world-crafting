"""CM1's similarity over water in PlaSim's surface transfer (climate/gcm/surface_similarity.py;
models/exoplasim/patches/13-similarity-over-water.patch): its tables are Paulson's and its neutral limit the log law, at
Earth's gravity and the Moon's; its viscosity is the world's, the 1976 standard atmosphere's at Earth's sea level and
lower by the density's ratio in the Open Moon's air; at the viscosity CM1's code sets the Python copy gives the numbers
Terluna's module gives; carried from step to step it settles to a fixed point, and over the warm lunar sea in light
wind it transfers more heat and vapour than Louis's factors with the gust, while land and sea ice keep PlaSim's
transfer; PlaSim's surflx with the patch, taken from the series applied to the pinned source and compiled with
ExoPlaSim's flags against a stub of PlaSim's module, gives the Python copy's transfer and carried state to 1e-10 on
lunar and Earth-like columns from fresh and settled states; with the switch off it prints every digit the gust's surflx
prints; the patch declares, reads and broadcasts each name once; and the patched fluxmod.f90 compiles with PlaSim's
modules.

Brought from Terluna's climate/tests/test_surface_similarity.py at 39c5ee04 (python/provenance.json): the Fortran comes
from the lab's patch series, where Terluna's came from its runner's edit lists."""
import math
import re
import subprocess

import numpy as np
import pytest

from climate.gcm import surface_gust as sg
from climate.gcm import surface_similarity as ssf
from climate.tests.test_surface_gust import (EARTH, FORTRAN, GCM_FLAGS, GUST_PATCH, G_MOON, LUNAR, STUB, cases,
                                             compiles_with_plasims_modules, module_additions, num, surflx)

SIMW_PATCH = '13-similarity-over-water.patch'


def settle(x, sigma, half, c, steps=200):
    """The column's transfer after the similarity's state has been carried to its fixed point on fixed air."""
    state = dict(ssf.START)
    for _ in range(steps):
        out = ssf.surface_transfer(x, sigma, half, c, state=state)
        state = out['similarity']['state']
    return out, state


# ------------------------------------------------------------------------------------------------------- Python

def test_the_tables_are_paulsons_and_the_neutral_limit_is_the_log_law():
    assert ssf.PSIM_TABLE[0] == pytest.approx(0.0, abs=1e-15) and ssf.PSIH_TABLE[0] == pytest.approx(0.0, abs=1e-15)
    x = 17.0 ** 0.25                                                        # z/L = -1
    assert ssf.PSIM_TABLE[100] == pytest.approx(2 * math.log((1 + x) / 2) + math.log((1 + x * x) / 2)
                                                - 2 * math.atan(x) + math.pi / 2, rel=1e-12)
    assert ssf.PSIH_TABLE[100] == pytest.approx(2 * math.log((1 + math.sqrt(17.0)) / 2), rel=1e-12)
    for g, visc in ((G_MOON, 1.31e-5), (EARTH['ga'], 1.46e-5)):
        state = dict(ssf.START)
        for _ in range(200):                                                # neutral air: thv the same at both ends
            s = ssf.similarity_column(300.0, 295.0, 295.0, 296.0, 296.0, visc, 4.0, g, state)
            state = s['state']
        assert s['regime'] == 3
        assert state['ust'] == pytest.approx(ssf.KARMAN * 4.0 / math.log(300.0 / state['z0']), rel=1e-9)
        log_law = state['ust'] * ssf.KARMAN / math.log((300.0 + s['z0q']) / s['z0q'])
        assert s['transh'] == pytest.approx(log_law, rel=1e-9)
        # Charnock's roughness takes the world's gravity and the smooth-flow term its viscosity.
        assert state['z0'] == pytest.approx(0.0185 * state['ust'] ** 2 / g + 0.11 * visc / state['ust'], rel=1e-9)
        fairall = 5.5e-5 * (state['ust'] * state['z0'] / visc) ** -0.6      # on the roughness Reynolds number
        assert s['z0q'] == pytest.approx(min(max(fairall, 2.0e-9), 1.0e-4), rel=1e-9) and state['z0'] < ssf.Z0_MAX
        assert (fairall < 1.0e-4) == (g == G_MOON)      # within its range at the Moon's gravity, at its cap at Earth's


def test_the_viscosity_is_the_worlds():
    """Sutherland's dynamic viscosity over the ideal gas's density: the 1976 standard atmosphere's 1.4607e-5 m2/s at
    Earth's sea level, within 1% of CM1's line from 0 to 30 degrees C, and 1.31e-5 m2/s in the Open Moon's air at
    300 K, lower than Earth's sea-level air at that temperature by the ratio of the densities."""
    earth = ssf.kinematic_viscosity(288.15, 101325.0, 287.05)
    mu = 1.458e-6 * 288.15 ** 1.5 / (288.15 + 110.4)
    assert mu == pytest.approx(1.7894e-5, rel=1e-4)
    assert earth == pytest.approx(mu / (101325.0 / (287.05 * 288.15)), rel=1e-12)
    assert earth == pytest.approx(1.4607e-5, rel=1e-4)
    for t in (273.15, 283.15, 293.15, 303.15):
        assert ssf.kinematic_viscosity(t, 101325.0, 287.05) == pytest.approx(ssf.cm1_viscosity(t), rel=0.01)
    assert ssf.cm1_viscosity(293.15) == pytest.approx(1.5e-5, rel=1e-12)       # its smooth-flow term's value
    moon = ssf.kinematic_viscosity(300.0, 121590.0, LUNAR['gascon'])
    assert moon == pytest.approx(1.31e-5, rel=5e-3)
    assert moon / ssf.kinematic_viscosity(300.0, 101325.0, 287.05) == pytest.approx(
        (LUNAR['gascon'] / 287.05) * (101325.0 / 121590.0), rel=1e-12)
    # A column's transfer takes it from its own surface pressure, gas constant and lowest level's temperature.
    c, half, cols = cases()[0]
    out = ssf.surface_transfer(cols[0], sg.full_sigma(half), half, c)
    assert out['viscosity'] == ssf.kinematic_viscosity(cols[0]['dt'][half.size - 1], cols[0]['dp'], c['gascon'])


def test_at_cm1s_viscosity_the_python_copy_gives_terlunas_numbers():
    """Terluna's surface_similarity.py at 39c5ee04 holds CM1's viscosities of Earth's sea-level air, which agree at
    1.5e-5 m2/s at 293.15 K. Run there on 2026-11-11 for four steps from the start, at 313 m with the air at 299 K and
    301.2 K (virtual) over a surface at 301.7 K and 306.4 K under 3 m/s, its similarity_column gave these."""
    pins = {G_MOON: (0.003210508490397601, 0.003017947970828825, 0.09515168896286852, -0.09110056814079447,
                     0.00012046483421455002),
            9.80665: (0.003205963710048553, 0.0026429108054431345, 0.08904342994477135, -0.09721213594871572,
                      3.348763892985748e-05)}
    for g, (transh, transm, ust, mol, z0) in pins.items():
        state = dict(ssf.START)
        for _ in range(4):
            s = ssf.similarity_column(313.0, 299.0, 301.7, 301.2, 306.4, ssf.cm1_viscosity(293.15), 3.0, g, state)
            state = s['state']
        assert s['regime'] == 4
        assert (s['transh'], s['transm'], state['ust'], state['mol'], state['z0']) == \
            pytest.approx((transh, transm, ust, mol, z0), rel=1e-12)


def test_it_settles_and_parts_from_louiss_factors_with_the_wind():
    """Calm and unstable over the warm lunar sea, the similarity carries more heat and vapour than Louis's factors with
    the gust; at 9 m/s it carries less, its roughness for heat and vapour (Fairall's) far below the momentum's."""
    c, half, cols = cases()[0]                                   # lunar, fifteen levels
    sigma = sg.full_sigma(half)
    for j in range(5):                                            # the sea's five columns
        x = cols[j]
        out, state = settle(x, sigma, half, c)
        again = ssf.surface_transfer(x, sigma, half, c, state=state)
        assert again['dtransh'] == pytest.approx(out['dtransh'], rel=1e-9)
        assert again['similarity']['state']['ust'] == pytest.approx(state['ust'], rel=1e-9)
        assert out['absu2'] == sg.surface_transfer(x, sigma, half, c, ngust=1)['absu2']   # the same wind, the gust's
    calm, windy = (settle(cols[j], sigma, half, c)[0] for j in (1, 2))
    louis_calm, louis_windy = (sg.surface_transfer(cols[j], sigma, half, c, ngust=1) for j in (1, 2))
    assert calm['similarity']['regime'] == 4 and calm['dtransh'] > 1.3 * louis_calm['dtransh']
    assert windy['dtransh'] < 0.85 * louis_windy['dtransh']
    assert windy['similarity']['z0q'] < 0.1 * windy['similarity']['state']['z0']
    for j in (5, 6, 7):                                           # land keeps PlaSim's transfer
        x = cols[j]
        out = ssf.surface_transfer(x, sigma, half, c)
        louis = sg.surface_transfer(x, sigma, half, c, ngust=1)
        assert 'similarity' not in out and out['dtransh'] == louis['dtransh'] and out['dtransm'] == louis['dtransm']
    ice = dict(cols[0], dicec=0.3)                                # so does sea ice
    assert 'similarity' not in ssf.surface_transfer(ice, sigma, half, c)
    off = ssf.surface_transfer(cols[0], sigma, half, c, nsimw=0)
    assert off['dtransh'] == sg.surface_transfer(cols[0], sigma, half, c, ngust=1)['dtransh']


# ------------------------------------------------------------------------------------------------------- Fortran

SIM_STUB = STUB.replace('{declarations}', '      real :: dicec(NHOR) = 0.\n{declarations}')
HARNESS = """
      program harness
      use fluxmod
      implicit none
      integer :: jhor, jlev
      read(*,*) ga, gascon, akap, rdbrv, acpd, adv
      read(*,*) sigma, sigmah
      read(*,*) zumin, ngust, gust_beta, gust_umin, nsimw
      do jhor=1,NHOR
       read(*,*) dp(jhor), dshfl(jhor), devap(jhor), dust3(jhor), dz0(jhor), dls(jhor), dicec(jhor)
       read(*,*) dsimust(jhor), dsimmol(jhor), dsimz0(jhor)
       read(*,*) (dt(jhor,jlev), jlev=1,NLEP)
       read(*,*) (dq(jhor,jlev), jlev=1,NLEP)
       read(*,*) (du(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dv(jhor,jlev), jlev=1,NLEV)
      enddo
      call surflx
      do jhor=1,NHOR
       write(*,'(*(es25.16e3))') dtransh(jhor), dtransm(jhor), dtsa(jhor), dsimust(jhor), dsimmol(jhor), dsimz0(jhor)
      enddo
      end program harness
"""


def compile_similarity(folder, code, nhor, nlev, declarations: str):
    """A harness of surflx against the stub of PlaSim's module with the two patches' own declarations."""
    folder.mkdir(parents=True, exist_ok=True)
    files = {'stub.f90': SIM_STUB.format(nhor=nhor, nlev=nlev, declarations=declarations), 'surflx.f90': code,
             'harness.f90': HARNESS}
    for name, text in files.items():
        (folder / name).write_text(text)
    subprocess.run(['gfortran', *GCM_FLAGS, '-o', 'harness', *files], cwd=folder, check=True, capture_output=True)
    return folder / 'harness'


def harness_input(c, half, cols, states, nsimw):
    sigma = sg.full_sigma(half)
    akap = c['gascon'] / c['acpd']
    lines = [num([c['ga'], c['gascon'], akap, c['rdbrv'], c['acpd'], c['ADV']]), num(np.r_[sigma, half]),
             f'{sg.EXOPLASIM_ZUMIN!r} 1 {sg.GUST_BETA!r} {sg.GUST_UMIN!r} {int(nsimw)}']
    for x, s in zip(cols, states):
        lines.append(num([x['dp'], x['dshfl'], x['devap'], x['dust3'], x['dz0'], x['dls'], x.get('dicec', 0.0)]))
        lines.append(num([s['ust'], s['mol'], s['z0']]))
        lines += [num(x[k]) for k in ('dt', 'dq', 'du', 'dv')]
    return '\n'.join(lines) + '\n'


def run(exe, text, ncols):
    rows = subprocess.run([str(exe)], input=text, capture_output=True, text=True, check=True).stdout.strip('\n')
    rows = rows.split('\n')
    assert len(rows) == ncols
    return rows


def columns_and_states(c, half, cols):
    """Each case's columns with a sea-ice twin of the first, from the fresh state and from a settled one."""
    sigma = sg.full_sigma(half)
    cols = cols + [dict(cols[0], dicec=0.4)]
    fresh = [dict(ssf.START) for _ in cols]
    settled = [settle(x, sigma, half, c, steps=40)[1] if ssf.applies(x) else dict(ssf.START) for x in cols]
    return cols, (fresh, settled)


def sources(series_sources):
    """fluxmod.f90 before the gust's patch, with it, and with the similarity's over it."""
    points = (series_sources.before(GUST_PATCH), GUST_PATCH, SIMW_PATCH)
    return tuple(series_sources.source('fluxmod.f90', name) for name in points)


@FORTRAN
def test_the_fortran_surflx_gives_the_python_copys_transfer_and_state(tmp_path, series_sources):
    pristine, _, patched = sources(series_sources)
    code, declarations = surflx(patched, last='simwcol'), module_additions(patched, pristine)
    for i, (c, half, cols) in enumerate(cases()):
        cols, state_sets = columns_and_states(c, half, cols)
        exe = compile_similarity(tmp_path / f'case{i}', code, len(cols), half.size, declarations)
        for states in state_sets:
            rows = run(exe, harness_input(c, half, cols, states, 1), len(cols))
            for x, s, row in zip(cols, states, rows):
                h, m, tsa, ust, mol, z0 = (float(v) for v in row.split())
                py = ssf.surface_transfer(x, sg.full_sigma(half), half, c, state=s)
                assert h == pytest.approx(py['dtransh'], rel=1e-10) and m == pytest.approx(py['dtransm'], rel=1e-10)
                assert tsa == pytest.approx(py['dtsa'], rel=1e-12)
                new = py['similarity']['state'] if 'similarity' in py else s
                assert ust == pytest.approx(new['ust'], rel=1e-10) and z0 == pytest.approx(new['z0'], rel=1e-10)
                assert mol == pytest.approx(new['mol'], rel=1e-10, abs=1e-14)


@FORTRAN
def test_with_the_switch_off_it_prints_every_digit_the_gusts_surflx_prints(tmp_path, series_sources):
    pristine, gust, patched = sources(series_sources)
    old, new = surflx(gust, last='gustcol'), surflx(patched, last='simwcol')
    assert old != new
    declarations = module_additions(patched, pristine)
    for i, (c, half, cols) in enumerate(cases()):
        cols, (fresh, _) = columns_and_states(c, half, cols)
        exe_old = compile_similarity(tmp_path / f'old{i}', old, len(cols), half.size, declarations)
        exe_new = compile_similarity(tmp_path / f'new{i}', new, len(cols), half.size, declarations)
        a = run(exe_old, harness_input(c, half, cols, fresh, 0), len(cols))
        b = run(exe_new, harness_input(c, half, cols, fresh, 0), len(cols))
        assert a == b


def test_the_patch_declares_reads_and_broadcasts_each_name_once(series_sources):
    assert all(len(line) <= 132 for line in series_sources.added(SIMW_PATCH))
    _, gust, text = sources(series_sources)
    assert text.count('        call simwcol(jhor,') == 1 and text.count('      subroutine simwcol(') == 1
    namelist = text[text.index('      namelist/fluxmod_nl/'):text.index('      if(mypid==NROOT) then')]
    for name in ('nsimw', 'simw_mub', 'simw_mus'):
        assert len(re.findall(rf'(real|integer) :: {name} = ', text)) == 1
        assert len(re.findall(rf'call mpbc[ri]\({name}\)', text)) == 1
        assert len(re.findall(rf'\b{name}\b', namelist)) == 1
    # The defaults are the Python copy's: the switch off, Sutherland's constants and the state before a first step.
    values = dict(re.findall(r'(?:real|integer) :: (\w+)(?:\(NHOR\))? = ([-0-9.e]+)', module_additions(text, gust)))
    assert {name: float(value) for name, value in values.items()} == dict(
        nsimw=0.0, simw_mub=ssf.SUTHERLAND_B, simw_mus=ssf.SUTHERLAND_S, dsimust=ssf.START['ust'],
        dsimmol=ssf.START['mol'], dsimz0=ssf.START['z0'], nsimwinit=0.0)


@FORTRAN
def test_the_patched_fluxmod_compiles_with_plasims_modules(tmp_path, series_sources):
    compiles_with_plasims_modules(tmp_path, series_sources, SIMW_PATCH)
