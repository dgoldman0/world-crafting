"""PlaSim's wind at 10 m through patch 17 of models/exoplasim/patches (`nwind10`), compiled alone: surflx, taken from
the series applied to the pinned ExoPlaSim archive, with ExoPlaSim's flags against a stub of PlaSim's module. Geleyn's
(1988) profile through the lowest layer gives the log law in neutral air, the lowest level's wind at that level's
height, the log law of the drag's friction velocity near the ground, less of the wind in stable air and more in
unstable air, and the factors Terluna recorded for its edit list; on one column in sigma the lowest level stands six
times higher at the Moon's gravity than at Earth's, and the factor falls with it. surflx gives the wind of the Python
copy written here to 1e-10 on lunar columns on fifteen and forty levels and Earth-like columns on ten, under PlaSim's
own transfer, Beljaars's gust and the gust with the similarity over water, from fresh and settled states and over sea
ice. With the similarity settled in neutral air over the sea, the wind takes the similarity's own log law. With the
switch off, and with it on, surflx prints every digit of the transfer that the series before the patch prints, under
ExoPlaSim's flags and under -O3 -march=native. The patch declares, reads and broadcasts its switch once, writes codes
165 and 166 as means since the last output, and compiles with PlaSim's modules.

The lab's own file: Terluna's test of its edit list (climate/tests/test_exoplasim_run.py on domain/climate at
39c5ee04, test_the_10_m_wind_follows_geleyns_profile) compiled the profile's lines alone on a stand-in."""
from __future__ import annotations

import math
import re
import subprocess

import numpy as np
import pytest

from climate.gcm import surface_gust as sg
from climate.gcm import surface_similarity as ssf
from climate.tests.test_rain_drops import NATIVE_FLAGS
from climate.tests.test_surface_gust import (EARTH, FORTRAN, GCM_FLAGS, G_MOON, LUNAR, STUB, cases,
                                             compiles_with_plasims_modules, module_additions, num, surflx)
from climate.tests.test_surface_similarity import settle

WIND_PATCH = '17-wind-at-10-m.patch'
SIMW_PATCH = '13-similarity-over-water.patch'
HEIGHT_M = 10.0                     # the height of codes 165 and 166, which ExoPlaSim's postprocessor names uas and vas
SWITCHES = ((0, 0), (1, 0), (1, 1))  # (ngust, nsimw): PlaSim's transfer, the gust, the gust with the similarity


# ------------------------------------------------------------------------------------------------------- Python copy

def factor(z_l: float, z0: float, rifm: float, z0_drag: float | None = None, z: float = HEIGHT_M) -> float:
    """Geleyn's factor on the lowest level's wind at height z: u(z) = u_L (ln(1 + z/z0) - (z/z_L)(B_N - B_D)) / B_D,
    B_N = ln(1 + z_L/z0) and B_D = kappa/sqrt(C_D) = ln(1 + z_L/z0_drag)/sqrt(rifm), C_D = C_N rifm the drag
    coefficient surflx uses, C_N its neutral coefficient at PlaSim's roughness z0_drag (dz0); z0 is the roughness of
    that drag, PlaSim's own unless the similarity sets the drag. Held between 0 and 1."""
    z0_drag = z0 if z0_drag is None else z0_drag
    b_d = math.log(z_l / z0_drag + 1.0) / math.sqrt(rifm)
    b_n = math.log(z_l / z0 + 1.0)
    return min(1.0, max(0.0, (math.log(1.0 + z / z0) - z / z_l * (b_n - b_d)) / b_d))


def transfer(x, half, c, ngust, nsimw, state):
    sigma = sg.full_sigma(half)
    if nsimw:
        return ssf.surface_transfer(x, sigma, half, c, state=state)
    return sg.surface_transfer(x, sigma, half, c, ngust=ngust)


def wind_10m(x, half, c, ngust, nsimw, state) -> tuple[float, float, float, dict]:
    """The wind at 10 m that surflx with patch 17 gives a column: the factor, from the transfer of the Python copies
    of patches 12 and 13, on the lowest level's wind. The similarity's roughness is the one it finds, before it
    carries it to the next step."""
    out = transfer(x, half, c, ngust, nsimw, state)
    z0 = state['z0'] if nsimw and ssf.applies(x) else x['dz0']
    f = factor(out['znl'], z0, out['rifm'], z0_drag=x['dz0'])
    return f * x['du'][-1], f * x['dv'][-1], f, out


def with_crosswind(cols):
    """The cases' columns with a wind across the lowest level as well, half the wind along it, and a sea-ice twin of
    the first."""
    out = [dict(x, dv=np.r_[x['dv'][:-1], -0.5 * x['du'][-1]]) for x in cols]
    return out + [dict(out[0], dicec=0.4)]


# ------------------------------------------------------------------------------------------------------- by hand

def test_geleyns_profile_by_hand():
    z_l, z0 = 885.0, 1.0e-4
    # Neutral air takes the log law between the ground and the lowest level.
    assert factor(z_l, z0, 1.0) == pytest.approx(math.log(1.0 + HEIGHT_M / z0) / math.log(1.0 + z_l / z0), rel=1e-14)
    # Terluna's record of its edit list (climate/gcm/README.md at 39c5ee04), with the 0.1 mm roughness of its test:
    # over the sea at the lowest level's 885 m the neutral factor is 0.72, and stability factors of 0.5 and 1.5 give
    # 0.51 and 0.88.
    assert [round(factor(z_l, z0, fm), 2) for fm in (1.0, 0.5, 1.5)] == [0.72, 0.51, 0.88]
    for fm in (0.3, 0.7, 1.0, 1.4, 2.0):
        b_n = math.log(1.0 + z_l / z0)
        c_d = (0.4 / b_n) ** 2 * fm
        # The profile reaches the lowest level's wind at that level's height,
        assert factor(z_l, z0, fm, z=z_l) == pytest.approx(1.0, rel=1e-14)
        # and near the ground it is the log law of the drag's friction velocity, u* = sqrt(C_D) u_L, to first order in
        # z/z_L.
        z = 0.5
        log_law = math.sqrt(c_d) / 0.4 * math.log(1.0 + z / z0)
        assert factor(z_l, z0, fm, z=z) == pytest.approx(log_law, abs=2.0 * z / z_l * abs(1.0 - 1.0 / math.sqrt(fm)))
    # Stable air brings less of the wind down and unstable air more, held at 1 where the air mixes the layer.
    assert factor(z_l, z0, 0.5) < factor(z_l, z0, 1.0) < factor(z_l, z0, 1.5) < factor(z_l, z0, 1.8) < 1.0
    assert factor(z_l, z0, 3.0) == 1.0
    # The profile's roughness enters the log and B_N; the drag's, B_D alone. With one roughness the two forms agree.
    assert factor(z_l, 4.0e-5, 1.2, z0_drag=4.0e-5) == factor(z_l, 4.0e-5, 1.2)
    assert factor(z_l, 4.0e-5, 1.2, z0_drag=1.5e-5) != factor(z_l, 1.5e-5, 1.2)


def test_on_one_column_in_sigma_the_moons_lowest_level_stands_higher_and_brings_less_wind_down():
    """surflx takes the lowest level's height from its own temperature, gas constant and gravity: on one column in
    sigma it stands g_E/g_M times higher at the Moon's gravity than at Earth's, where the bulk Richardson number, which
    goes as g z_L, keeps its value. The neutral coefficient falls with the height, and so does the factor."""
    c, half, cols = cases()[2]                                   # Earth-like on PlaSim's ten levels
    moon = dict(c, ga=G_MOON)
    for x in cols:
        (_, _, f_e, out_e), (_, _, f_m, out_m) = (wind_10m(x, half, cc, 0, 0, None) for cc in (c, moon))
        assert out_m['znl'] * G_MOON == pytest.approx(out_e['znl'] * EARTH['ga'], rel=1e-12)
        assert out_m['ri'] == pytest.approx(out_e['ri'], rel=1e-9, abs=1e-15)
        assert f_m < f_e


def test_with_the_similarity_settled_in_neutral_air_the_wind_takes_the_similaritys_log_law():
    """Over the sea at 2 m/s, in neutral air and with no fluxes the step before, so that the gust is nil, the
    similarity settles to u* = kappa U / ln(z_L/z0) on its own roughness z0, Charnock's with the smooth-flow term, and
    the wind at 10 m is the log law on that roughness, ln(10/z0)/ln(z_L/z0) of the lowest level's wind, on the Moon's
    fifteen levels and on Earth's ten. PlaSim's own roughness over the sea, which seamod takes from the stress by
    Charnock's 0.018 with a floor of 0.015 mm, stands at half the similarity's or less in this light wind; on it, the
    form of Terluna's edit list, the profile's log runs on another roughness than the drag's, and the wind at 10 m
    comes out 5.4% stronger on the Moon and 6.8% on Earth."""
    for k, ratio in ((0, 1.0543), (2, 1.0684)):                   # lunar on fifteen levels, Earth-like on ten
        c, half, cols = cases()[k]
        x, n = cols[0], half.size
        sigma = sg.full_sigma(half)
        tha = x['dt'][n - 1] * sigma[n - 1] ** (-sg.plasim_constants(c)['akap'])
        neutral = dict(x, du=np.r_[x['du'][:-1], 2.0], dv=np.r_[x['dv'][:-1], 0.0], dshfl=0.0, devap=0.0,
                       dt=np.r_[x['dt'][:n], tha], dq=np.r_[x['dq'][:n], x['dq'][n - 1]])
        out, state = settle(neutral, sigma, half, c, steps=400)
        assert out['wstar'] == 0.0 and out['similarity']['regime'] == 3
        z_l, z0 = out['znl'], state['z0']
        assert state['ust'] == pytest.approx(0.4 * 2.0 / math.log(z_l / z0), rel=1e-12)
        plasim_z0 = max(0.018 * state['ust'] ** 2 / c['ga'], 1.5e-5)          # seamod's, from that stress
        assert 1.5 * plasim_z0 < z0 < 3.0 * plasim_z0
        neutral['dz0'] = plasim_z0
        _, _, f, out = wind_10m(neutral, half, c, 1, 1, state)
        assert f == pytest.approx(math.log(HEIGHT_M / z0) / math.log(z_l / z0), rel=1e-6)
        assert factor(z_l, plasim_z0, out['rifm']) / f == pytest.approx(ratio, abs=1e-4)


# ------------------------------------------------------------------------------------------------------- Fortran

WIND_STUB = STUB.replace('{declarations}', '      real :: dicec(NHOR) = 0.\n'
                                           '      integer :: nwind10 = 0\n'
                                           '      real :: du10(NHOR) = 0., dv10(NHOR) = 0.\n{declarations}')
HARNESS = """
      program harness
      use fluxmod
      implicit none
      integer :: jhor, jlev
      read(*,*) ga, gascon, akap, rdbrv, acpd, adv
      read(*,*) sigma, sigmah
      read(*,*) zumin, ngust, gust_beta, gust_umin, nsimw, nwind10
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
       write(*,'(*(es25.16e3))') dtransh(jhor), dtransm(jhor), dtsa(jhor), dsimust(jhor), dsimmol(jhor), &
     &                           dsimz0(jhor), du10(jhor), dv10(jhor)
      enddo
      end program harness
"""


def compile_wind(folder, code, nhor, nlev, declarations: str, flags=GCM_FLAGS):
    """A harness of surflx against the stub of PlaSim's module, with the declarations the patches add to fluxmod and,
    in the stub, the three that patch 17 adds to PlaSim's own module."""
    folder.mkdir(parents=True, exist_ok=True)
    files = {'stub.f90': WIND_STUB.format(nhor=nhor, nlev=nlev, declarations=declarations), 'surflx.f90': code,
             'harness.f90': HARNESS}
    for name, text in files.items():
        (folder / name).write_text(text)
    subprocess.run(['gfortran', *flags, '-o', 'harness', *files], cwd=folder, check=True, capture_output=True)
    return folder / 'harness'


def harness_input(c, half, cols, states, ngust, nsimw, nwind10):
    sigma = sg.full_sigma(half)
    akap = c['gascon'] / c['acpd']
    lines = [num([c['ga'], c['gascon'], akap, c['rdbrv'], c['acpd'], c['ADV']]), num(np.r_[sigma, half]),
             f'{sg.EXOPLASIM_ZUMIN!r} {ngust} {sg.GUST_BETA!r} {sg.GUST_UMIN!r} {nsimw} {nwind10}']
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


def sources(series_sources):
    """fluxmod.f90 before patch 12, before patch 17 and with it."""
    before = series_sources.before(WIND_PATCH)
    return tuple(series_sources.source('fluxmod.f90', name)
                 for name in (series_sources.before('12-surface-gust.patch'), before, WIND_PATCH))


def columns_and_states(c, half, cols):
    sigma = sg.full_sigma(half)
    cols = with_crosswind(cols)
    fresh = [dict(ssf.START) for _ in cols]
    settled = [settle(x, sigma, half, c, steps=40)[1] if ssf.applies(x) else dict(ssf.START) for x in cols]
    return cols, (fresh, settled)


@FORTRAN
def test_the_fortran_wind_gives_the_python_copys(tmp_path, series_sources):
    pristine, _, patched = sources(series_sources)
    code, declarations = surflx(patched, last='simwcol'), module_additions(patched, pristine)
    for i, (c, half, cols) in enumerate(cases()):
        cols, state_sets = columns_and_states(c, half, cols)
        exe = compile_wind(tmp_path / f'case{i}', code, len(cols), half.size, declarations)
        for ngust, nsimw in SWITCHES:
            for states in state_sets[:1 + nsimw]:
                rows = run(exe, harness_input(c, half, cols, states, ngust, nsimw, 1), len(cols))
                for x, s, row in zip(cols, states, rows):
                    values = [float(v) for v in row.split()]
                    u10, v10, f, out = wind_10m(x, half, c, ngust, nsimw, s)
                    assert values[1] == pytest.approx(out['dtransm'], rel=1e-10)
                    assert values[6] == pytest.approx(u10, rel=1e-10) and values[7] == pytest.approx(v10, rel=1e-10)
                    assert 0.0 < f <= 1.0


@FORTRAN
@pytest.mark.parametrize('flags', [GCM_FLAGS, NATIVE_FLAGS], ids=['exoplasim', 'native'])
def test_off_and_on_surflx_prints_every_digit_of_the_transfer_it_printed_before(tmp_path, series_sources, flags):
    """surflx before patch 17 and with it, at nwind10 0 and 1: the transfer, the 2 m temperature and the similarity's
    carried state print the same digits, and the wind at 10 m stays at the stub's zero with the switch off."""
    pristine, before, patched = sources(series_sources)
    old, new = surflx(before, last='simwcol'), surflx(patched, last='simwcol')
    assert old != new
    declarations = module_additions(patched, pristine)
    assert declarations == module_additions(before, pristine)       # the patch adds nothing to fluxmod's module
    for i, (c, half, cols) in enumerate(cases()):
        cols, (fresh, settled) = columns_and_states(c, half, cols)
        exe_old = compile_wind(tmp_path / f'old{i}', old, len(cols), half.size, declarations, flags)
        exe_new = compile_wind(tmp_path / f'new{i}', new, len(cols), half.size, declarations, flags)
        for ngust, nsimw in SWITCHES:
            for states in (fresh, settled)[:1 + nsimw]:
                a = run(exe_old, harness_input(c, half, cols, states, ngust, nsimw, 0), len(cols))
                b = run(exe_new, harness_input(c, half, cols, states, ngust, nsimw, 0), len(cols))
                on = run(exe_new, harness_input(c, half, cols, states, ngust, nsimw, 1), len(cols))
                assert a == b
                assert [row.split()[:6] for row in on] == [row.split()[:6] for row in a]
                assert all(float(v) == 0.0 for row in b for v in row.split()[6:])
                assert any(float(v) != 0.0 for row in on for v in row.split()[6:])


def test_the_patch_declares_reads_and_broadcasts_its_switch_and_writes_the_means(series_sources):
    added = series_sources.added(WIND_PATCH)
    assert all(len(line) <= 132 for line in added)
    text = (series_sources.folder / WIND_PATCH).read_text()
    assert re.findall(r'^\+\+\+ b/plasim/src/(\S+)', text, flags=re.M) == ['plasimmod.f90', 'fluxmod.f90', 'outmod.f90']
    module = series_sources.source('plasimmod.f90', WIND_PATCH)
    flux = series_sources.source('fluxmod.f90', WIND_PATCH)
    out = series_sources.source('outmod.f90', WIND_PATCH)
    # The switch, off by default, its state beside PlaSim's other accumulators, read in fluxmod's namelist and sent to
    # every rank.
    assert len(re.findall(r'integer :: nwind10 = 0 ', module)) == 1 and 'nwind10' not in flux[:flux.index('end module')]
    for name in ('nu10acc', 'du10', 'dv10', 'au10', 'av10'):
        assert len(re.findall(rf'(?:real|integer) :: {name}\b', module)) == 1
    namelist = flux[flux.index('      namelist/fluxmod_nl/'):flux.index('      if(mypid==NROOT) then')]
    assert len(re.findall(r'\bnwind10\b', namelist)) == 1 and flux.count('      call mpbci(nwind10)\n') == 1
    # surflx sets the wind at 10 m after its transfer, in a loop of its own, and writes nothing else.
    body = surflx(flux, last='surflx')
    assert body.index('       dtransm(jhor)=ztrans*zrifm(jhor)\n      enddo\n') < body.index('        du10(jhor)=')
    assigned = set(re.findall(r'^\s+(\w+)(?:\([^)]*\))?\s*=', body, flags=re.M))
    assert assigned - set(re.findall(r'^\s+(\w+)(?:\([^)]*\))?\s*=', surflx(series_sources.source(
        'fluxmod.f90', series_sources.before(WIND_PATCH)), last='surflx'), flags=re.M)) == \
        {'zz0w', 'zbd', 'zbn', 'zf10', 'du10', 'dv10'}
    # The output: codes 165 and 166 on the mean output's unit, with the switch on, as means over the steps counted
    # since the last output; the sums and the count start again at each output.
    block = out[out.index('      if (nwind10 == 1) then\n       au10(:)=au10(:)/'):]
    block = block[:block.index('      endif\n')]
    assert 'call writegp(40,au10,165,0)' in block and 'call writegp(40,av10,166,0)' in block
    assert block.count('/real(max(nu10acc,1))') == 2
    assert out.count('       nu10acc=nu10acc+1\n') == 1 and out.count('      nu10acc=0\n') == 1
    accu = out[out.index('      subroutine outaccu'):]
    reset = out[out.index('      subroutine outreset'):]
    accu, reset = (part[:part.index('\n      return\n      end\n')] for part in (accu, reset))
    assert '       au10(:)=au10(:)+du10(:)\n       av10(:)=av10(:)+dv10(:)\n       nu10acc=nu10acc+1\n' in accu
    assert '      au10(:)=0.\n      av10(:)=0.\n      nu10acc=0\n' in reset
    assert len(re.findall(r'writegp\(\w+,\w+,16[56],', out)) == 2


@FORTRAN
def test_the_patched_sources_compile_with_plasims_modules(tmp_path, series_sources):
    compiles_with_plasims_modules(tmp_path, series_sources, WIND_PATCH)
