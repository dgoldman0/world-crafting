"""Patches 06, 07 and 08 of the lab's CM1 series: the world's gravity, CO2 and O2, the slab soil's top layer and the
Sun's declination, each read from the namelist with the build's value as its default, so that one build serves every
world. The patches' texts put a namelist entry at each place that read a build macro, and the parts of the patched
model that compile on their own keep their bits at the defaults and return, told another world's values, the bits of
a build compiled for that world: the constants, the CAPE diagnostic, one column of RRTMG's longwave and shortwave,
the block that sets the Sun, and the lines that lay out the soil.

The lab's own file, with no Terluna source: Terluna compiles one build for each world. The parts are compiled from the
series on the pinned archive under both of the builds' flag sets; a compiled case of the whole model, at the defaults
and at the Moon's values, ran once from scratch scripts (models/cm1/README.md).
"""
import math
import os
import re
import shutil
import struct
import subprocess
import tomllib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pytest

from worldlab import derive
from worldlab.spec import Library

REPO = Path(__file__).resolve().parents[3]
PATCH_05 = 'patches/lab/05-factors-on-autoconversion-and-accretion.patch'
PATCH_06 = 'patches/lab/06-gravity-co2-and-o2-from-the-namelist.patch'
PATCH_07 = 'patches/lab/07-the-soils-top-layer-from-the-namelist.patch'
PATCH_08 = 'patches/lab/08-the-suns-declination-from-the-namelist.patch'
CPP = ('cpp', '-C', '-P', '-traditional', '-Wno-invalid-pp-token', '-ffreestanding', '-DOPENMP')
# gfortran's flags in the two makefiles of the builds: CM1's own for OpenMP, and Terluna's optimisation of them, the
# lab's default, under which gfortran fuses products into multiply-adds and calls glibc's vector maths.
COMMON = ('-ffree-form', '-ffree-line-length-none', '-finline-functions', '--param=max-vartrack-size=0', '-fopenmp')
FLAGS = dict(cm1=('-O2', *COMMON), native=('-O3', '-march=native', *COMMON))
# A world as a build compiles it in and as the namelist states it: CM1's own gravity with the macros' default air, and
# the Open Moon as Terluna's builds have it (models/cm1/builds.json).
EARTH = dict(g=9.81, co2=400.0e-6, o2=0.209488)
MOON = dict(g=1.6242188765608128, co2=4.0e-4, o2=0.174579)
MOON_MACROS = ('-DTERLUNA_G=1.6242188765608128', '-DTERLUNA_CO2=4.000000e-04', '-DTERLUNA_O2=0.174579')
MACRO_DEFAULTS = ['#ifndef TERLUNA_G', '#define TERLUNA_G 9.81', '#endif', '#ifndef TERLUNA_CO2',
                  '#define TERLUNA_CO2 400.e-6', '#endif', '#ifndef TERLUNA_O2', '#define TERLUNA_O2 0.209488', '#endif']


def needs_compiler():
    if shutil.which('gfortran') is None or shutil.which('cpp') is None:
        pytest.skip('gfortran or cpp is missing')


def build(folder, sources, driver, flags, macros=()):
    """An executable from CM1 source files, preprocessed as the model's makefile preprocesses them, and a driver."""
    for name, text in sources:
        (folder / name).write_text(text, encoding='latin-1')
        done = subprocess.run([*CPP, *macros, name], cwd=folder, check=True, capture_output=True, encoding='latin-1')
        (folder / f'{name[:-2]}.f90').write_text(done.stdout, encoding='latin-1')
    (folder / 'driver.f90').write_text(driver)
    subprocess.run(['gfortran', *flags, *[f'{name[:-2]}.f90' for name, _ in sources], 'driver.f90', '-o', 'run'],
                   cwd=folder, check=True, capture_output=True)
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
    """The single-precision number nearest x, which CM1 holds."""
    return float(np.float32(x))


SHOW = """
  subroutine show(name, values)
    ! each value's bits, in hexadecimal
    character(len=*), intent(in) :: name
    real, intent(in) :: values(:)
    write(*,'(a,*(1x,z8.8))') name, values
  end subroutine show
"""


def imports(text, module):
    """The names each `use` of a module takes in a source file, None for the whole module."""
    found, lines = [], text.splitlines()
    for at, line in enumerate(lines):
        if re.match(rf' *use +{module}\b', line, flags=re.I):
            statement = line.split('!')[0].rstrip()
            while statement.endswith('&'):
                at += 1
                statement = statement[:-1] + lines[at].split('!')[0].strip().lstrip('&')
            only = re.search(r'only *:(.*)', statement, flags=re.I)
            found.append(only and [name.strip().lower() for name in only.group(1).split(',') if name.strip()])
    return found


# The patches' texts.

def test_the_world_patches_follow_the_labs_series(cm1_series):
    assert cm1_series.names[-3:] == [PATCH_06, PATCH_07, PATCH_08] and cm1_series.before(PATCH_06) == PATCH_05
    files = {PATCH_06: ['base.F', 'cm1.F', 'constants.F', 'domaindiag.F', 'getcape.F', 'init_physics.F', 'input.F',
                        'module_ra_etc.F', 'module_ra_rrtmg_lw.F', 'module_ra_rrtmg_sw.F', 'param.F',
                        'radiation_driver.F', 'writeout.F'],
             PATCH_07: ['cm1.F', 'init_surface.F', 'input.F', 'param.F'],
             PATCH_08: ['cm1.F', 'input.F', 'param.F', 'radiation_driver.F']}
    for patch, names in files.items():
        text = (cm1_series.folder / patch).read_text(encoding='latin-1')
        assert re.findall(r'^\+\+\+ b/src/(\S+)', text, flags=re.M) == names
        for line in cm1_series.added(patch):
            assert len(line) <= 120, line
            assert '//' not in line and '/*' not in line, line                  # cpp would read these
    # cpp reads nine added lines, the macros' defaults at the head of cm1.F; three more lines name a macro, the
    # entries' defaults in cm1.F, each ahead of its comment's apostrophes, and one keeps the constant of MYNN and MYJ.
    added = cm1_series.added(PATCH_06)
    assert [line for line in added if line.startswith('#')] == MACRO_DEFAULTS
    assert [line.split('!')[0].strip() for line in added if 'TERLUNA_' in line and not line.startswith('#')] == [
        'world_g = TERLUNA_G', 'world_co2 = TERLUNA_CO2', 'world_o2 = TERLUNA_O2', 'REAL    , PARAMETER :: g = TERLUNA_G']
    for patch in (PATCH_07, PATCH_08):
        assert not any('TERLUNA_' in line or '#' in line for line in cm1_series.added(patch))


def test_each_entry_is_declared_defaulted_read_broadcast_checked_and_printed(cm1_series):
    cm1, inputs, param = (cm1_series.source(name, PATCH_08) for name in ('cm1.F', 'input.F', 'param.F'))
    assert cm1.splitlines()[:9] == MACRO_DEFAULTS
    for default in ('      world_g = TERLUNA_G ', '      world_co2 = TERLUNA_CO2 ', '      world_o2 = TERLUNA_O2 ',
                    '      soil_dz1 = 0.05 ', '      sun_decl = 0.0 '):
        assert cm1.count(default) == 1, default
    for declared in ('      real :: world_g ', '      real :: world_co2,world_o2 ', '      real :: soil_dz1 ',
                     '      real :: sun_decl '):
        assert inputs.count(declared) == 1, declared
    assert ('                        rain_autoconv_fac,rain_accr_fac, &\n'
            '                        world_g,world_co2,world_o2,soil_dz1,sun_decl, &\n'
            '                        csound,cstar,solconrce,zenanglrce\n') in inputs
    for name in ('world_g', 'world_co2', 'world_o2', 'soil_dz1', 'sun_decl'):
        assert param.count(f'      call MPI_BCAST({name},1,MPI_REAL,0,MPI_COMM_WORLD,ierr)') == 1, name
        assert param.count(f"      if(dowr) write(outfile,*) '{name} =',{name}  ! Lab\n") == 1, name
    # The model stops on a value it cannot take before it sets its constants: a gravity of zero or less, another
    # gravity in the two test cases that set their own, a gas below zero or the two above one, a soil layer of zero or
    # less, a declination beyond a pole, and a declination without the Sun it acts on. Each test also fails a NaN.
    start = param.index("      ! Lab: the world's gravity and air come from the namelist")
    checks = param[start:param.index('      call set_constants( testcase , world_g )\n')]
    assert param.count('call set_constants(') == 1
    for test, message in (('IF( .not.(world_g.gt.0.0) )THEN', 'world_g must be positive'),
                          ('IF( (testcase.eq.4 .or. testcase.eq.5) .and. world_g.ne.9.81 )THEN', 'world_g must equal it'),
                          ('IF( .not.(world_co2.ge.0.0 .and. world_o2.ge.0.0 .and. (world_co2+world_o2).le.1.0) )THEN',
                           'world_co2 and world_o2 are mole fractions'),
                          ('IF( .not.(soil_dz1.gt.0.0) )THEN', 'soil_dz1 must be positive'),
                          ('IF( .not.(abs(sun_decl).le.90.0) )THEN', 'sun_decl must lie between -90 and 90 degrees'),
                          ('IF( sun_decl.ne.0.0 .and. .not.(radopt.eq.2 .and. var19.gt.1.0) )THEN',
                           'sun_decl is read with radopt = 2')):
        block = checks[checks.index(test):]
        assert message in block[:block.index('call stopcm1')], test
    assert checks.count('call stopcm1') == 6


def test_the_namelists_values_stand_where_the_builds_macros_were_read(cm1_series):
    """Before patch 06 five files read a build macro: constants.F, getcape.F and module_ra_etc.F the gravity, and
    RRTMG's two files the CO2 and the O2. After it the macros give the entries their defaults in cm1.F, and one read
    remains, the gravity that MYNN's and MYJ's schemes hold as a compile-time constant."""
    reads = lambda texts: {name: [line.split('!')[0].strip() for line in text.splitlines()
                                  if 'TERLUNA_' in line.split('!')[0] and not line.startswith('#')]
                           for name, text in texts.items() if 'TERLUNA_' in text}
    kept = ('cm1.F', 'constants.F', 'getcape.F', 'module_ra_etc.F', 'module_ra_rrtmg_lw.F', 'module_ra_rrtmg_sw.F')
    before = reads({name: cm1_series.source(name, PATCH_05) for name in kept})
    assert before == {'constants.F': ['g      = TERLUNA_G'], 'getcape.F': ['real, parameter :: g     = TERLUNA_G'],
                      'module_ra_etc.F': ['REAL    , PARAMETER :: g = TERLUNA_G'],
                      'module_ra_rrtmg_lw.F': ['data o2 / TERLUNA_O2 /', 'co2 = TERLUNA_CO2'],
                      'module_ra_rrtmg_sw.F': ['data o2 / TERLUNA_O2 /', 'co2 = TERLUNA_CO2']}
    assert reads(cm1_series.tree) == {'cm1.F': ['world_g = TERLUNA_G', 'world_co2 = TERLUNA_CO2', 'world_o2 = TERLUNA_O2'],
                                      'module_ra_etc.F': ['REAL    , PARAMETER :: g = TERLUNA_G']}
    tree = cm1_series.tree
    # The dynamics and every scheme that takes CM1's g: set_constants sets it from the entry.
    assert tree['constants.F'].count('        g      = world_g   ! Lab') == 1
    assert '      subroutine set_constants( testcase , world_g )\n' in tree['constants.F']
    assert tree['param.F'].count('      call set_constants( testcase , world_g )\n') == 1
    # RRTMG: its gravity comes with its initialisation's two calls, where the constant of module_model_constants stood,
    # and its CO2 and O2 with its two drivers' calls.
    for band, routine in (('lw', 'rrtmg_lw_ini'), ('sw', 'rrtmg_sw_ini')):
        text = tree[f'module_ra_rrtmg_{band}.F']
        assert text.count(f'   call {routine}(cp,grv)\n') == 1
        assert text.count('   REAL, INTENT(IN)               :: grv   ! Lab') == 1
        assert text.count('      co2 = lab_co2   ! Lab') == 1 and text.count('      o2 = lab_o2\n') == 1
        assert 'data o2' not in text and text.count('   real, intent(in)           :: lab_co2,lab_o2   ! Lab') == 1
    assert tree['init_physics.F'].count("                  grv=g )   ! Lab: RRTMG takes the run's gravity\n") == 2
    assert tree['radiation_driver.F'].count('lab_co2=world_co2,lab_o2=world_o2 )   ! Lab\n') == 2
    # The CAPE diagnostic: the gravity is an argument, which each of its three calls hands over.
    assert '                        zlcl, zlfc, zel , psource , tsource , qvsource , g )\n' in tree['getcape.F']
    assert sum(tree[name].count('qvsource , g )   ! Lab') for name in ('base.F', 'domaindiag.F', 'writeout.F')) == 3
    assert sum(text.count('call getcape(') for text in tree.values()) == 3
    # The constant that stays: the schemes that use module_model_constants' g hold the build's value, and a run that
    # selects one of them stops unless the namelist's gravity equals it.
    uses = {name: imports(text, 'module_model_constants') for name, text in tree.items()
            if imports(text, 'module_model_constants')}
    assert uses == {'module_bl_myjpbl.F': [None], 'module_sf_myjsfc.F': [None],               # the whole module
                    'module_bl_mynn_common.F': [['karman', 'g', 'p1000mb', 'cp', 'r_d', 'r_v', 'rcp', 'xlv', 'xlf', 'xls',
                                                 'svp1', 'svp2', 'svp3', 'p608', 'ep_2', 'rvovrd', 'cpv', 'cliq', 'cice',
                                                 'svpt0']],
                    'module_sf_mynn.F': [['p1000mb', 'ep_2']], 'init_physics.F': [['lab_build_g => g']],
                    'module_ra_rrtmg_lw.F': [['cp']], 'module_ra_rrtmg_sw.F': [['cp']]}
    guard = tree['init_physics.F']
    assert '      use module_model_constants , only : lab_build_g => g   ! Lab' in guard
    block = guard[guard.index('      IF( (ipbl.eq.4 .or. ipbl.eq.5 .or. ipbl.eq.6 .or. sfcmodel.eq.7) .and. world_g.ne.lab_build_g )THEN'):]
    assert 'world_g must equal it' in block[:block.index('call stopcm1')]


# A number that reads as a gravity in the model's code, outside its comments: 9.8 to 9.9 m/s2, or 980 to 982 cm/s2
# with a decimal, which leaves out RRTMG's band edges at 980 per cm; with an exponent of zero at most, which leaves
# out RRTMG's tables.
GRAVITY_LITERAL = re.compile(r'(?<![\w])(?<!\d\.)(?:9\.8\d{0,5}|980\.\d{1,3}|981\.\d{0,3})(?:[eEdD][+-]?0+)?(?:_\w+)?(?![\w.])')
# Each file that holds one, with its count of such lines. The first group the series accounts for: the macro's default
# (cm1.F, module_ra_etc.F), test cases 4 and 5 with the stop that guards them, in its test and in its message
# (constants.F, param.F), and Morrison's reference gravity, against which core patch 04 and the lab's patch 03 scale
# Earth's values (morrison.F, whose G takes CM1's g four lines on). The second group is Earth's gravity inside a
# scheme, which the registry refuses at another gravity (cm1-earth-g-schemes).
ACCOUNTED = {'cm1.F': 1, 'module_ra_etc.F': 1, 'constants.F': 2, 'param.F': 2, 'morrison.F': 11}
EARTHS = {'goddard.F': 1, 'lfoice.F': 1, 'module_gfs_physcons.F': 1, 'module_mp_jensen_ishmael.F': 1,
          'module_mp_nssl_2mom.F': 2, 'module_mp_p3.F': 1, 'module_sf_exchcoef.F': 5, 'module_sf_gfdl.F': 1,
          'module_sf_mynn.F': 5, 'mp_wsm6.F': 1, 'radtrns3d.F': 1}


def test_earths_gravity_stays_only_where_the_series_accounts_for_it_or_the_registry_refuses_it(cm1_series):
    found = {}
    for name, text in cm1_series.tree.items():
        count = sum(bool(GRAVITY_LITERAL.search(line.split('!')[0])) for line in text.splitlines())
        if count:
            found[name] = count
    assert len(cm1_series.tree) == 91 and found == {**ACCOUNTED, **EARTHS}
    morrison = cm1_series.tree['morrison.F']
    assert '         G = 9.81\n' in morrison and '         G = terluna_g_host\n' in morrison
    assert morrison.index('         G = 9.81\n') < morrison.index('         G = terluna_g_host\n')
    assert '      use constants, only : terluna_g_host => g\n' in morrison
    registry = tomllib.loads((REPO / 'lab' / 'registry' / 'earth_assumptions.toml').read_text())['entry']
    refused = next(entry for entry in registry if entry['id'] == 'cm1-earth-g-schemes')
    assert refused['action'] == 'refuse'
    for name in (*EARTHS, 'module_bl_mynn_common.F', 'module_bl_myjpbl.F', 'module_sf_myjsfc.F'):
        assert name in refused['where'], name


# The constants.

CONSTANTS_DRIVER = """
program constants_check
  use constants
  implicit none
  integer :: testcase
  real :: gravity
  read(*,*) testcase, gravity
  call set_constants(testcase, gravity)
  write(*,'(a)') 'VALUES'
  call show('g', (/ g /)); call show('govtwo', (/ govtwo /)); call show('given', (/ gravity /))
contains
""" + SHOW + """
end program constants_check
"""


def test_the_constants_take_the_namelists_gravity(cm1_series, tmp_path):
    needs_compiler()
    exe = build(tmp_path, [('constants.F', cm1_series.source('constants.F', PATCH_08))], CONSTANTS_DRIVER, FLAGS['cm1'])
    for gravity in (9.81, MOON['g'], 3.72076, 24.79):
        found = run(exe, f'0 {gravity!r}\n')[1]
        assert values(found['g'])[0] == single(gravity) and values(found['govtwo'])[0] == single(0.5 * single(gravity))
    # Test cases 4 and 5 keep the gravity of their own constants; param.F stops a run of either on another world_g.
    for testcase in (4, 5):
        assert values(run(exe, f'{testcase} 1.62\n')[1]['g'])[0] == single(9.81)


# The CAPE diagnostic.

CAPE_DRIVER = """
program cape_soundings
  ! CM1's CAPE diagnostic on soundings from standard input, for each of its three source parcels.
  use getcape_module, only : getcape
  implicit none
  integer :: count, nk, k, n, source
  real :: gravity, cape, cin, zlcl, zlfc, zel, psource, tsource, qvsource
  real, allocatable :: p(:), t(:), q(:)
  read(*,*) count, gravity
  write(*,'(a)') 'VALUES'
  do n = 1, count
    read(*,*) nk
    allocate(p(nk), t(nk), q(nk))
    do k = 1, nk
      read(*,*) p(k), t(k), q(k)
    enddo
    do source = 1, 3
      call getcape(source, nk, p, t, q, cape, cin, zlcl, zlfc, zel, psource, tsource, qvsource!GRAVITY)
      write(*,'(a,i0,a,i0,8(1x,z8.8))') 's', n, 'p', source, cape, cin, zlcl, zlfc, zel, psource, tsource, qvsource
    enddo
    deallocate(p, t, q)
  enddo
end program cape_soundings
"""


def sounding(surface_hpa, surface_c, humidity, levels=70):
    """Pressure (hPa), temperature (C) and vapour (kg/kg) from the ground up: air that cools as p^0.19 to a level
    of 210 K and stays there, moist in its lowest tenth of the pressure and drier above."""
    rows = []
    for k in range(levels):
        p = surface_hpa * (1.0 - 0.95 * k / (levels - 1))
        t = max((surface_c + 273.15) * (p / surface_hpa)**0.19, 210.0)
        rh = humidity if p > 0.9 * surface_hpa else 0.5 * humidity
        e = rh * 6.112 * math.exp(17.67 * (t - 273.15) / (t - 29.65))
        rows.append((p, t - 273.15, 0.622 * e / (p - e)))
    return rows


SOUNDINGS = [sounding(1000.0, 28.0, 0.85), sounding(1000.0, 18.0, 0.4), sounding(1215.9, 27.0, 0.75), sounding(700.0, 22.0, 0.9)]


def cape_input(gravity):
    return f'{len(SOUNDINGS)} {gravity!r}\n' + ''.join(
        f'{len(rows)}\n' + ''.join(' '.join(repr(x) for x in row) + '\n' for row in rows) for rows in SOUNDINGS)


@pytest.fixture(scope='module')
def capes(cm1_series, tmp_path_factory):
    """The CAPE diagnostic from the series before patch 06, with CM1's gravity and with the Moon's compiled in, and
    from the series' end, which takes the gravity as an argument, under each flag set: six builds of getcape.F."""
    needs_compiler()
    built = {}
    for flags in FLAGS:
        for label, through, macros, takes in (('earth', PATCH_05, (), ''), ('moon', PATCH_05, MOON_MACROS[:1], ''),
                                              ('namelist', PATCH_08, (), ', gravity')):
            built[label, flags] = build(tmp_path_factory.mktemp('cape'), [('getcape.F', cm1_series.source('getcape.F', through))],
                                        CAPE_DRIVER.replace('!GRAVITY', takes), FLAGS[flags], macros)
    return built


def test_the_cape_diagnostic_takes_the_gravity_it_is_given_as_the_build_took_its_own(capes):
    """On four soundings and CM1's three source parcels, the diagnostic that takes its gravity as an argument returns
    the bits of the diagnostic with that gravity compiled in, at CM1's 9.81 m/s2 and at the Moon's, under CM1's flags
    and under -O3 -march=native."""
    for flags in FLAGS:
        for label, world in (('earth', EARTH), ('moon', MOON)):
            compiled = run(capes[label, flags], cape_input(world['g']))[1]
            assert len(compiled) == 12 and all(len(words) == 8 for words in compiled.values())
            assert run(capes['namelist', flags], cape_input(world['g']))[1] == compiled, (flags, label)
    # For the surface parcel and the most unstable one, the diagnostic's energies are the sounding's and its heights go
    # as 1/g: on the Moon the same sounding holds the same CAPE and inhibition, with its condensation level, level of
    # free convection and equilibrium level 6.04 times as high.
    earth, moon = (run(capes['namelist', 'cm1'], cape_input(world['g']))[1] for world in (EARTH, MOON))
    ratio = EARTH['g'] / MOON['g']
    unstable = 0
    for key in earth:
        if key.endswith('p3'):
            continue
        (cape_e, cin_e, *heights_e), (cape_m, cin_m, *heights_m) = (values(found[key])[:5] for found in (earth, moon))
        assert cape_m == pytest.approx(cape_e, rel=2e-4, abs=0.05) and cin_m == pytest.approx(cin_e, rel=2e-4, abs=0.05)
        for height_e, height_m in zip(heights_e, heights_m):            # -1 where the sounding has no such level
            assert height_m == (pytest.approx(ratio * height_e, rel=2e-4) if height_e > 0.0 else -1.0)
        unstable += cape_e > 500.0
    assert ratio == pytest.approx(6.04, abs=0.005) and unstable >= 4
    # The mixed-layer parcel, which CM1's output takes, averages the sounding's lowest 500 m, a depth the diagnostic
    # holds at every gravity (ml_depth). On these soundings the second level stands above 500 m at the Moon's gravity,
    # and the diagnostic then takes the lowest level alone, where at 9.81 m/s2 it averages several.
    for n in range(1, len(SOUNDINGS) + 1):
        assert moon[f's{n}p3'] == moon[f's{n}p1'] and earth[f's{n}p3'] != earth[f's{n}p1']


# One column of RRTMG.

RRTMG_DRIVER = """
program rrtmg_column
  ! One column of CM1's RRTMG, longwave and shortwave, called as radiation_driver.F calls them. The column, its
  ! surface and its Sun come from standard input, with the world's gravity, CO2 and O2.
  use module_ra_rrtmg_lw, only : rrtmg_lwinit, rrtmg_lwrad
  use module_ra_rrtmg_sw, only : rrtmg_swinit, rrtmg_swrad
  implicit none
  integer, parameter :: cldovrlp = 2, calc_clean_atm_diag = 0
  real, parameter :: rd = 287.04, cp = 1005.7, degrad = 3.1415926535897932384626433/180.0
  integer :: nk, k, yr, julday, icloud, mp_physics, o3input, aer_opt, no_src_types, sf_surface_physics
  integer :: has_reqc, has_reqi, has_reqs
  logical :: warm_rain, is_cammgmp_used
  real :: gravity, co2, o2, skin_k, emissivity, albedo, cosz, sunlight, p_top, co2out, julian, xtime, gmt
  real :: radt_min, declin
  real, allocatable, dimension(:,:,:) :: p3d, p8w, t3d, t8w, pi3d, dz8w, rho3d, qv, qc, qr, qi, qs, qg, cldfra
  real, allocatable, dimension(:,:,:) :: lwten, lwtenc, swten, swtenc, effc, effi, effs, o3
  real, dimension(1,1) :: glw, olr, lwcf, emiss, tsk, xland, xice, snow, lwupt, lwuptc, lwdnt, lwdntc, lwupb
  real, dimension(1,1) :: lwupbc, lwdnb, lwdnbc, swupt, swuptc, swdnt, swdntc, swupb, swupbc, swdnb, swdnbc, swcf
  real, dimension(1,1) :: gsw, xlat, xlong, albd, coszr, coszen, swddir, swddni, swddif, swdownc, swddnic, swddirc
  real, dimension(:,:,:,:), pointer :: tauaer_sw => null(), ssaaer_sw => null(), asyaer_sw => null()

  read(*,*) nk, gravity, co2, o2
  read(*,*) skin_k, emissivity, albedo, cosz, sunlight
  allocate(p3d(1,1,nk+1), p8w(1,1,nk+1), t3d(1,1,nk+1), t8w(1,1,nk+1), pi3d(1,1,nk+1), dz8w(1,1,nk+1))
  allocate(rho3d(1,1,nk+1), qv(1,1,nk+1), qc(1,1,nk+1), qr(1,1,nk+1), qi(1,1,nk+1), qs(1,1,nk+1), qg(1,1,nk+1))
  allocate(cldfra(1,1,nk+1), lwten(1,1,nk+1), lwtenc(1,1,nk+1), swten(1,1,nk+1), swtenc(1,1,nk+1))
  allocate(effc(1,1,nk+1), effi(1,1,nk+1), effs(1,1,nk+1), o3(1,1,nk+1))
  p3d = 0.0; t3d = 0.0; dz8w = 0.0; qv = 0.0; qc = 0.0; qr = 0.0; qi = 0.0; qs = 0.0; qg = 0.0; cldfra = 0.0
  do k = 1, nk
    read(*,*) p3d(1,1,k), t3d(1,1,k), dz8w(1,1,k), qv(1,1,k), qc(1,1,k), qi(1,1,k), qs(1,1,k), cldfra(1,1,k)
  enddo
  do k = 1, nk+1
    read(*,*) p8w(1,1,k), t8w(1,1,k)
  enddo
  p3d(1,1,nk+1) = p8w(1,1,nk+1); t3d(1,1,nk+1) = t8w(1,1,nk+1)
  pi3d = (p3d*1.0e-5)**(rd/cp)
  rho3d = p3d/(rd*t3d*(1.0+0.608*qv))
  effc = 10.0e-6; effi = 40.0e-6; effs = 120.0e-6; o3 = 1.0e-12
  lwten = 0.0; lwtenc = 0.0; swten = 0.0; swtenc = 0.0
  glw = 0.0; olr = 0.0; lwcf = 0.0; gsw = 0.0; swcf = 0.0
  emiss = emissivity; tsk = skin_k; albd = albedo; coszen = cosz; coszr = cosz
  xland = 1.0; xice = 0.0; snow = 0.0; xlat = 0.0; xlong = 0.0
  p_top = p8w(1,1,nk+1)
  icloud = 1; warm_rain = .false.; is_cammgmp_used = .false.; mp_physics = 10; o3input = 0
  has_reqc = 1; has_reqi = 1; has_reqs = 1
  yr = 2014; julian = 181.0; julday = 182; xtime = 0.0; gmt = 0.0; radt_min = 30.0; declin = 0.0
  aer_opt = 0; no_src_types = 6; sf_surface_physics = 1

  call rrtmg_lwinit(p_top=p_top, allowed_to_read=.true., myid=0,                 &
                    ids=1, ide=2, jds=1, jde=2, kds=1, kde=nk+1,                 &
                    ims=1, ime=1, jms=1, jme=1, kms=1, kme=nk+1,                 &
                    its=1, ite=1, jts=1, jte=1, kts=1, kte=nk!INIT
                    )
  call rrtmg_swinit(allowed_to_read=.true., myid=0,                              &
                    ids=1, ide=2, jds=1, jde=2, kds=1, kde=nk+1,                 &
                    ims=1, ime=1, jms=1, jme=1, kms=1, kme=nk+1,                 &
                    its=1, ite=1, jts=1, jte=1, kts=1, kte=nk!INIT
                    )
  call rrtmg_lwrad(rthratenlw=lwten, lwtenc=lwtenc,                              &
                   lwupt=lwupt, lwuptc=lwuptc, lwdnt=lwdnt, lwdntc=lwdntc,       &
                   lwupb=lwupb, lwupbc=lwupbc, lwdnb=lwdnb, lwdnbc=lwdnbc,       &
                   glw=glw, olr=olr, lwcf=lwcf, emiss=emiss,                     &
                   p8w=p8w, p3d=p3d, pi3d=pi3d, dz8w=dz8w, tsk=tsk, t3d=t3d,     &
                   t8w=t8w, rho3d=rho3d, r=rd, g=gravity,                        &
                   icloud=icloud, warm_rain=warm_rain, cldfra3d=cldfra,          &
                   cldovrlp=cldovrlp, is_cammgmp_used=is_cammgmp_used,           &
                   xland=xland, xice=xice, snow=snow,                            &
                   qv3d=qv, qc3d=qc, qr3d=qr, qi3d=qi, qs3d=qs, qg3d=qg,         &
                   o3input=o3input, o33d=o3,                                     &
                   f_qv=.true., f_qc=.true., f_qr=.true., f_qi=.true., f_qs=.true., f_qg=.true., &
                   re_cloud=effc, re_ice=effi, re_snow=effs,                     &
                   has_reqc=has_reqc, has_reqi=has_reqi, has_reqs=has_reqs,      &
                   yr=yr, julian=julian, calc_clean_atm_diag=calc_clean_atm_diag, &
                   ids=1, ide=2, jds=1, jde=2, kds=1, kde=nk+1,                  &
                   ims=1, ime=1, jms=1, jme=1, kms=1, kme=nk+1,                  &
                   its=1, ite=1, jts=1, jte=1, kts=1, kte=nk,                    &
                   mp_physics=mp_physics, co2out=co2out!AIR
                   )
  lwcf(1,1) = co2out
  call rrtmg_swrad(rthratensw=swten, swtenc=swtenc,                              &
                   swupt=swupt, swuptc=swuptc, swdnt=swdnt, swdntc=swdntc,       &
                   swupb=swupb, swupbc=swupbc, swdnb=swdnb, swdnbc=swdnbc,       &
                   swcf=swcf, gsw=gsw,                                           &
                   xtime=xtime, gmt=gmt, xlat=xlat, xlong=xlong,                 &
                   radt=radt_min, degrad=degrad, declin=declin,                  &
                   coszr=coszr, julday=julday, solcon=sunlight,                  &
                   albedo=albd, t3d=t3d, t8w=t8w, tsk=tsk,                       &
                   p3d=p3d, p8w=p8w, pi3d=pi3d, rho3d=rho3d, dz8w=dz8w,          &
                   cldfra3d=cldfra, is_cammgmp_used=is_cammgmp_used,             &
                   r=rd, g=gravity, icloud=icloud, warm_rain=warm_rain,          &
                   cldovrlp=cldovrlp, xland=xland, xice=xice, snow=snow,         &
                   qv3d=qv, qc3d=qc, qr3d=qr, qi3d=qi, qs3d=qs, qg3d=qg,         &
                   o3input=o3input, o33d=o3, aer_opt=aer_opt, no_src=no_src_types, &
                   sf_surface_physics=sf_surface_physics,                        &
                   f_qv=.true., f_qc=.true., f_qr=.true., f_qi=.true., f_qs=.true., f_qg=.true., &
                   re_cloud=effc, re_ice=effi, re_snow=effs,                     &
                   has_reqc=has_reqc, has_reqi=has_reqi, has_reqs=has_reqs,      &
                   calc_clean_atm_diag=calc_clean_atm_diag,                      &
                   ids=1, ide=2, jds=1, jde=2, kds=1, kde=nk+1,                  &
                   ims=1, ime=1, jms=1, jme=1, kms=1, kme=nk+1,                  &
                   its=1, ite=1, jts=1, jte=1, kts=1, kte=nk,                    &
                   tauaer3d_sw=tauaer_sw, ssaaer3d_sw=ssaaer_sw, asyaer3d_sw=asyaer_sw, &
                   swddir=swddir, swddni=swddni, swddif=swddif,                  &
                   swdownc=swdownc, swddnic=swddnic, swddirc=swddirc,            &
                   xcoszen=coszen, yr=yr, julian=julian, mp_physics=mp_physics, co2out=co2out!AIR
                   )
  write(*,'(a)') 'VALUES'
  call show('co2', (/ lwcf(1,1), co2out /))
  call show('lwten', lwten(1,1,1:nk)); call show('lwtenc', lwtenc(1,1,1:nk))
  call show('swten', swten(1,1,1:nk)); call show('swtenc', swtenc(1,1,1:nk))
  call show('olr', olr(1,:)); call show('glw', glw(1,:)); call show('lwupt', lwupt(1,:))
  call show('lwuptc', lwuptc(1,:)); call show('lwdnb', lwdnb(1,:)); call show('lwdnbc', lwdnbc(1,:))
  call show('lwupb', lwupb(1,:)); call show('gsw', gsw(1,:)); call show('swcf', swcf(1,:))
  call show('swdnt', swdnt(1,:)); call show('swupt', swupt(1,:)); call show('swuptc', swuptc(1,:))
  call show('swdnb', swdnb(1,:)); call show('swdnbc', swdnbc(1,:)); call show('swupb', swupb(1,:))
contains
""" + SHOW + """
end program rrtmg_column
"""


def column(world, surface_pa, top_m, levels, lapse_k_m, sunlight, cosz=0.6, cloud=True, laid_out_at=None):
    """The driver's input for a world: levels of equal depth to `top_m` in hydrostatic air at the world's gravity, or
    at the gravity `laid_out_at`, cooling from 300 K at `lapse_k_m` to 200 K, moist below a third of the depth, with a
    layer of cloud water low down, snow in the middle and cloud ice above it where `cloud` is set; a ground at 301 K
    of emissivity 0.98 and albedo 0.15."""
    scale = 287.04 * 255.0 / (laid_out_at or world['g'])
    dz = top_m / levels
    temperature = lambda z: max(300.0 - lapse_k_m * z, 200.0)
    pressure = lambda z: surface_pa * math.exp(-z / scale)
    lines = [f'{levels} {world["g"]!r} {world["co2"]!r} {world["o2"]!r}', f'301.0 0.98 0.15 {cosz!r} {sunlight!r}']
    for k in range(levels):
        z, share = (k + 0.5) * dz, (k + 0.5) / levels
        t, p = temperature(z), pressure(z)
        e = (0.7 if share < 0.33 else 0.3 if share < 0.6 else 0.01) * 611.2 * math.exp(17.67 * (t - 273.15) / (t - 29.65))
        qc = 2.0e-5 if cloud and 0.06 < share < 0.1 else 0.0
        qs = 2.0e-5 if cloud and 0.3 < share < 0.4 else 0.0
        qi = 1.0e-5 if cloud and 0.4 < share < 0.5 else 0.0
        lines.append(' '.join(repr(x) for x in (p, t, dz, 0.622 * e / (p - e), qc, qi, qs, 1.0 if qc or qs or qi else 0.0)))
    lines += [f'{pressure(k * dz)!r} {301.0 if k == 0 else temperature(k * dz)!r}' for k in range(levels + 1)]
    return '\n'.join(lines) + '\n'


EARTH_COLUMN = dict(surface_pa=101325.0, top_m=30000.0, levels=40, lapse_k_m=6.5e-3, sunlight=1361.0)
MOON_COLUMN = dict(surface_pa=121590.0, top_m=150000.0, levels=60, lapse_k_m=1.1e-3, sunlight=1198.193)


@pytest.fixture(scope='module')
def rrtmg(cm1_series, tmp_path_factory):
    """One column of RRTMG from the series before patch 06, with CM1's gravity and Earth's air and with the Moon's
    compiled in, and from the series' end, which takes the three from its caller, under each flag set: six builds of
    module_ra_etc.F and RRTMG's two files, about 1.7 MB each beside the two tables, three compiling at a time."""
    needs_compiler()
    names = ('module_ra_etc.F', 'module_ra_rrtmg_lw.F', 'module_ra_rrtmg_sw.F')

    def one(job):
        label, flags, through, macros, init, air, folder = job
        driver = RRTMG_DRIVER.replace('!INIT', init + ' &').replace('!AIR', air + ' &')     # each ends a call's line
        exe = build(folder, [(name, cm1_series.source(name, through)) for name in names], driver, FLAGS[flags], macros)
        for name, content in cm1_series.data.items():
            (folder / name).write_bytes(content)
        return (label, flags), exe

    jobs = [(label, flags, through, macros, init, air, tmp_path_factory.mktemp('rrtmg'))
            for flags in FLAGS
            for label, through, macros, init, air in (
                ('earth', PATCH_05, (), '', ''), ('moon', PATCH_05, MOON_MACROS, '', ''),
                ('namelist', PATCH_08, (), ', grv=gravity', ', lab_co2=co2, lab_o2=o2'))]
    with ThreadPoolExecutor(3) as pool:
        return dict(pool.map(one, jobs))


def test_rrtmg_takes_the_gravity_and_air_it_is_given_as_the_build_took_its_own(rrtmg):
    """A cloudy column of each world, sunlit: RRTMG told the gravity, CO2 and O2 returns the bits of RRTMG with them
    compiled in, the heating rates of every level and the fluxes at the top and at the ground, longwave and shortwave,
    with cloud and clear: at CM1's gravity in the macros' default air, and at the Moon's gravity in the Open Moon's
    air, under CM1's flags and under -O3 -march=native."""
    for flags in FLAGS:
        for label, world, shape in (('earth', EARTH, EARTH_COLUMN), ('moon', MOON, MOON_COLUMN)):
            text = column(world, **shape)
            head, compiled = run(rrtmg[label, flags], text)
            assert len(compiled) == 20 and len(compiled['lwten']) == len(compiled['swten']) == shape['levels']
            assert run(rrtmg['namelist', flags], text) == (head, compiled), (flags, label)
            # The column is one in which the radiation acts: cloud changes both bands at the top, and the Sun heats.
            assert abs(values(compiled['olr'])[0] - values(compiled['lwuptc'])[0]) > 5.0
            assert abs(values(compiled['swupt'])[0] - values(compiled['swuptc'])[0]) > 5.0
            assert values(compiled['swten']).max() > 0.0 and values(compiled['lwten']).min() < 0.0
    # The build for Earth, given the Moon's column, returns other bits: the comparison above tells the worlds apart.
    assert run(rrtmg['earth', 'cm1'], column(MOON, **MOON_COLUMN))[1] != run(rrtmg['moon', 'cm1'], column(MOON, **MOON_COLUMN))[1]


def test_the_namelists_gravity_co2_and_o2_reach_rrtmg(rrtmg):
    """In a clear column of Earth's air at CM1's gravity, under a Sun of 1361 W/m2 at a zenith cosine of 0.6: RRTMG
    reports the CO2 it was given in both bands; twice the CO2 lowers the longwave leaving the top by 3 to 6 W/m2; and
    air without O2 lets 3 to 8 W/m2 more sunlight reach the ground. Told the Moon's gravity on the same pressures,
    where each pascal holds 6.04 times the air, RRTMG lets less longwave leave the top and less sunlight reach the
    ground, and prints the gravity it took as it starts."""
    exe = rrtmg['namelist', 'cm1']
    clear = lambda world: run(exe, column(world, cloud=False, laid_out_at=EARTH['g'], **EARTH_COLUMN))
    head, base = clear(EARTH)
    top, ground = values(base['lwuptc'])[0], values(base['swdnbc'])[0]
    assert list(values(base['co2'])) == [single(EARTH['co2'])] * 2 and 250.0 < top < 300.0 and 500.0 < ground < 700.0
    assert base['olr'] == base['lwuptc'] and values(base['gsw'])[0] == pytest.approx(0.85 * ground, rel=1e-4)
    doubled = clear({**EARTH, 'co2': 2 * EARTH['co2']})[1]
    assert list(values(doubled['co2'])) == [single(2 * EARTH['co2'])] * 2
    assert 3.0 < top - values(doubled['lwuptc'])[0] < 6.0
    anoxic = clear({**EARTH, 'o2': 0.0})[1]
    assert 3.0 < values(anoxic['swdnbc'])[0] - ground < 8.0
    assert anoxic['co2'] == base['co2'] and anoxic['swdnt'] == base['swdnt']
    lunar_head, lunar = clear({**EARTH, 'g': MOON['g']})
    assert values(lunar['lwuptc'])[0] < top - 10.0 and values(lunar['swdnbc'])[0] < ground - 10.0
    printed = lambda text: [float(line.split()[-1]) for line in text.splitlines() if 'cp,grv =' in line]
    assert printed(head) == pytest.approx([9.81, 9.81], rel=1e-6)
    assert printed(lunar_head) == pytest.approx([MOON['g']] * 2, rel=1e-6)


# The Sun.

SUN_DRIVER = """
program sun_block
  ! The block of radiation_driver.F that sets the Sun under a solar day of var19 seconds, on columns along x.
  implicit none
  real, parameter :: pi = 3.1415926535897932384626433
  integer :: ni, nj, i, j
  real :: var12, var16, var17, var18, var19, ctrlat, dtrad, solcon, declin, terluna_lat, terluna_s, sun_decl
  double precision :: mtime
  real, allocatable :: xh(:), hrang(:,:), coszen(:,:)
  read(*,*) ni, var12, var16, var17, var18, var19, ctrlat, dtrad, mtime, sun_decl
  nj = 1
  allocate(xh(ni), hrang(ni,nj), coszen(ni,nj))
  read(*,*) xh
  declin = 0.25; solcon = 0.0; hrang = 0.0; coszen = 0.0
!BLOCK
  write(*,'(a)') 'VALUES'
  call show('coszen', coszen(:,1)); call show('hrang', hrang(:,1)); call show('declin', (/ declin /))
  call show('solcon', (/ solcon /))
contains
""" + SHOW + """
end program sun_block
"""


def sun_block(text):
    start = text.index('        IF( var19.gt.1.0 )THEN\n')
    return text[start:text.index('\n        ENDIF\n', start) + len('\n        ENDIF\n')]


@pytest.fixture(scope='module')
def suns(cm1_series, tmp_path_factory):
    """The Sun's block of radiation_driver.F from the series before patch 08 and from its end, in a program that
    declares what the block reads, under each flag set."""
    needs_compiler()
    return {(label, flags): build(tmp_path_factory.mktemp('sun'), [],
                                  SUN_DRIVER.replace('!BLOCK', sun_block(cm1_series.source('radiation_driver.F', through))),
                                  FLAGS[flags])
            for flags in FLAGS for label, through in (('equinox', PATCH_07), ('declined', PATCH_08))}


# The Sun's cases: a box at one latitude, a ring round a circle of latitude, and a ring on a great circle tilted
# 45 degrees, each of 48 columns, 26.3 Earth days into a lunar day that began at sunrise.
RING_M, COLUMNS, LUNAR_DAY_S = 7719064.817, 48, 2551443.0
SUN_CASES = dict(box=(0.0, 0.0, 44.3), south_box=(0.0, 0.0, -30.0), ring=(0.0, RING_M, 45.0), tilted=(45.0, RING_M, 0.0),
                 polar_ring=(0.0, RING_M, 80.0))


def sun_input(case, declination, hour_deg=-90.0, time_s=2272320.0, radiation_s=1800.0):
    tilt, length, latitude = SUN_CASES[case]
    x = [(i + 0.5) * RING_M / COLUMNS for i in range(COLUMNS)]
    return (f'{COLUMNS} {tilt!r} {length!r} 1198.193 {hour_deg!r} {LUNAR_DAY_S!r} {latitude!r} {radiation_s!r} {time_s!r} '
            f'{declination!r}\n' + ' '.join(repr(v) for v in x) + '\n')


def sun_geometry(case, hour_deg=-90.0, time_s=2272320.0, radiation_s=1800.0):
    """Each column's latitude and hour angle (radians), by core patch 05's rule."""
    tilt, length, latitude = SUN_CASES[case]
    hour = np.full(COLUMNS, math.radians(hour_deg + 360.0 * (time_s + 0.5 * radiation_s) / LUNAR_DAY_S))
    lat = np.full(COLUMNS, math.radians(latitude))
    if length > 1.0:
        s = 2.0 * math.pi * (np.arange(COLUMNS) + 0.5) / COLUMNS
        if tilt > 0.0:
            lat = np.arcsin(math.sin(math.radians(tilt)) * np.sin(s))
            hour = hour + np.arctan2(math.cos(math.radians(tilt)) * np.sin(s), np.cos(s))
        else:
            hour = hour + s
    return lat, hour


def test_the_equinox_sun_keeps_its_bits(cm1_series, suns):
    """At the default declination the block returns the zenith cosine, the hour angle and the sunlight of the block
    before the patch bit for bit, in a box, on a ring of latitude and on a tilted ring, under CM1's flags and under
    -O3 -march=native, and leaves the declination CM1 passes on as it found it. The patch adds its loop after the
    equinox's, whose statements stay as they were."""
    for flags in FLAGS:
        for case in SUN_CASES:
            before = run(suns['equinox', flags], sun_input(case, 0.0))[1]
            assert run(suns['declined', flags], sun_input(case, 0.0))[1] == before, (flags, case)
            assert values(before['declin'])[0] == 0.25 and values(before['solcon'])[0] == single(1198.193)
    before, after = (sun_block(cm1_series.source('radiation_driver.F', patch)) for patch in (PATCH_07, PATCH_08))
    assert after.startswith(before[:before.rindex('        ENDIF\n')]) and after.count('IF( sun_decl.ne.0.0 )THEN') == 1


def test_the_sun_stands_at_the_namelists_declination(suns):
    """With a declination the zenith cosine is sin(lat) sin(decl) + cos(lat) cos(decl) cos(hour angle) at each column's
    latitude and hour angle, to 2 parts in 10^6 of one, north and south of the equator and in each kind of case; the
    hour angle and the sunlight stay the equinox's; and the declination CM1 passes on is the namelist's."""
    exe = suns['declined', 'cm1']
    for case in SUN_CASES:
        lat, hour = sun_geometry(case)
        equinox = run(exe, sun_input(case, 0.0))[1]
        assert values(equinox['coszen']) == pytest.approx(np.cos(lat) * np.cos(hour), abs=2e-6)
        for declination in (1.54, -1.54, 23.44, -25.19, 60.0):
            found = run(exe, sun_input(case, declination))[1]
            d = math.radians(declination)
            want = np.sin(lat) * math.sin(d) + np.cos(lat) * math.cos(d) * np.cos(hour)
            assert values(found['coszen']) == pytest.approx(want, abs=2e-6), (case, declination)
            assert found['hrang'] == equinox['hrang'] and found['solcon'] == equinox['solcon']
            assert values(found['declin'])[0] == pytest.approx(d, rel=1e-6)
            assert np.abs(values(found['coszen']) - values(equinox['coszen'])).max() > 0.01
    # A northern summer raises the noon Sun in the north and lowers it in the south.
    noon = dict(hour_deg=0.0, time_s=0.0, radiation_s=0.0)
    for case, sign in (('box', 1.0), ('south_box', -1.0)):
        latitude = SUN_CASES[case][2]
        for declination in (0.0, 20.0):
            found = values(run(exe, sun_input(case, declination, **noon))[1]['coszen'])
            assert found == pytest.approx(math.cos(math.radians(latitude - declination)), abs=2e-6)
        assert sign * (math.cos(math.radians(latitude - 20.0)) - math.cos(math.radians(latitude))) > 0.05


def test_a_case_that_starts_at_the_labs_sunrise_meets_the_sun_on_the_horizon(suns):
    """The lab starts a case at the hour angle -acos(-tan(lat) tan(decl)) (worldlab.derive). At that hour angle the
    patched block puts the Sun on the horizon, to 2 parts in 10^6 of one: for Mars's solstices at 44.3 N, for the
    Moon's 1.54 degrees at 30 S, and for Earth's 23.44 degrees on a ring at 45 N, at the ring's first column. Round a
    circle at 80 N the Sun stays up through a summer's day and down through a winter's."""
    exe = suns['declined', 'cm1']
    start = dict(time_s=0.0, radiation_s=0.0)
    for case, declination in (('box', 25.19), ('box', -25.19), ('south_box', 1.54), ('ring', 23.44)):
        tilt, length, latitude = SUN_CASES[case]
        sunrise = derive.sunrise_hour_angle_deg(latitude, declination)
        first = 360.0 * 0.5 / COLUMNS if length > 1.0 else 0.0       # a ring's first column stands half a column east
        found = values(run(exe, sun_input(case, declination, hour_deg=sunrise - first, **start))[1]['coszen'])
        assert (found[:1] if length > 1.0 else found) == pytest.approx(0.0, abs=2e-6), (case, declination)
        assert (sunrise < -90.0) == (latitude * declination > 0.0)          # summer's Sun rises earlier
    # Round a circle of latitude at 80 N the Sun stays up through a summer's day and down through a winter's, and
    # crosses the horizon at the equinox.
    summer, winter, equinox = (values(run(exe, sun_input('polar_ring', d, **start))[1]['coszen']) for d in (20.0, -20.0, 0.0))
    assert summer.min() > 0.0 and winter.max() < 0.0 and equinox.min() < 0.0 < equinox.max()


# The soil.

SOIL_DRIVER = """
program soil_layers
  ! The lines of init_surface.F that lay out the slab soil's layers.
  implicit none
  integer, parameter :: num_soil_layers = 5, outfile = 6
  logical, parameter :: dowr = .true.
  integer :: l
  real :: soil_dz1
  real, dimension(num_soil_layers) :: slab_zs, slab_dzs
  read(*,*) soil_dz1
  slab_zs = 0.0; slab_dzs = 0.0
!BLOCK
      ENDIF
  write(*,'(a)') 'VALUES'
  call show('dzs', slab_dzs); call show('zs', slab_zs)
contains
""" + SHOW + """
end program soil_layers
"""


def soil_block(text):
    start = text.index('      IF (num_soil_layers.NE.1)THEN\n')
    return text[start:text.index('      DO l=1,num_soil_layers\n', start)]


@pytest.fixture(scope='module')
def soils(cm1_series, tmp_path_factory):
    """The soil's lines of init_surface.F from the series before patch 07 and after it, under each flag set."""
    needs_compiler()
    return {(label, flags): build(tmp_path_factory.mktemp('soil'), [],
                                  SOIL_DRIVER.replace('!BLOCK', soil_block(cm1_series.source('init_surface.F', through))),
                                  FLAGS[flags])
            for flags in FLAGS for label, through in (('core', PATCH_06), ('namelist', PATCH_07))}


def test_the_soils_layers_double_from_the_namelists_top_layer(cm1_series, soils):
    """At the default, 0.05 m, the lines return the layers of core patch 08 bit for bit under both flag sets, 5 to
    80 cm thick. Told a top layer, they return five layers that double from it, each centred under the ones above:
    CM1's own 1 to 16 cm from 0.01 m, and for the Open Moon's solar day 5.4 to 86.9 cm."""
    doubling = np.array([1.0, 2.0, 4.0, 8.0, 16.0])
    centres = np.array([0.5, 2.0, 5.0, 11.0, 23.0])
    for flags in FLAGS:
        core = run(soils['core', flags], '99.0\n')[1]
        assert run(soils['namelist', flags], '0.05\n')[1] == core, flags
        assert values(core['dzs']) == pytest.approx(0.05 * doubling, rel=1e-6)
    seeds = Library()
    lunar = 0.01 * derive.soil_factor(derive.planet(seeds.world('moon'), seeds.scenario('moon/open-moon'))['solar_day_days'])
    assert lunar == pytest.approx(0.054342, abs=5e-7)
    for top in (0.01, 0.05, lunar, 0.2):
        head, found = run(soils['namelist', 'cm1'], f'{top!r}\n')
        assert values(found['dzs']) == pytest.approx(top * doubling, rel=1e-6)
        assert values(found['zs']) == pytest.approx(top * centres, rel=1e-6)
        printed = [float(x) for x in head[head.index('Lab soil: the layers (m)'):].split()[5:]]
        assert printed == pytest.approx(top * doubling, rel=1e-6)
    assert values(run(soils['namelist', 'cm1'], f'{lunar!r}\n')[1]['dzs'])[[0, -1]] == pytest.approx([0.0543, 0.8695], abs=5e-5)
    text = cm1_series.source('init_surface.F', PATCH_08)
    assert text.count('      slab_dzs(1)=soil_dz1\n') == 1 and '.05' not in soil_block(text).split('slab_dzs(1)=soil_dz1')[1]

