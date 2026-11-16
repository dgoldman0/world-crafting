"""ExoPlaSim's builds: their keys, a build of the series' deployed point against Terluna's deployed sources, and PlaSim
compiled by the lab running on run folders the lab's adapter writes."""
import hashlib
import json
import re
import shutil
import struct
import subprocess

import numpy as np
import pytest

from atmosphere.radiative_convective.thermodynamics import DryAir, earthlike_air
from atmosphere.rain import drops
from climate.gcm import levels, rain_drops
from worldlab import builds, derive, exoplasim as ex
from worldlab.data import DataError
from worldlab.roots import root
from worldlab.spec import LAB, Library, SpecError

LIB = Library()
DEFAULTS = LIB.defaults('exoplasim/defaults')
EARTH, CONTROL = LIB.world('earth'), LIB.scenario('earth/control')
STORE, ENV = root('store'), root('env')
DEPLOYED = LAB.parent / 'models' / 'exoplasim' / 'expected.sha256'
SERIES_SOURCES = LAB.parent / 'models' / 'exoplasim' / 'expected-series.sha256'
needs_build = pytest.mark.skipif(STORE is None or ENV is None or not ex.ARCHIVE.exists() or shutil.which('mpif90') is None,
                                 reason="a build needs the lab's store and environment, the pinned archive and MPI")


def _sha256(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inputs(**changes) -> dict:
    """A build's inputs as `builds.gather` gives them, made up, and `changes` on top."""
    made = dict(model='exoplasim', archive=dict(name='exoplasim-3.4.2.tar.gz', sha256='a' * 64),
                configured={name: 'b' * 64 for name in builds.CONFIGURED},
                patches=[dict(name='01-rayleigh-scale.patch', sha256='c' * 64),
                         dict(name='02-cloud-water-gravity.patch', sha256='d' * 64)],
                grid=dict(resolution='T21', levels=10, ranks=4, precision=8),
                flags=dict(debug=False, optimization=None, mars=False),
                toolchain=dict(mpirun=dict(path='/usr/bin/mpirun', version='mpirun (Open MPI) 4.1.6'),
                               mpif90_line='gfortran -lmpi_mpifh -lmpi'))
    return {**made, **changes}


def test_a_builds_key_follows_everything_that_makes_it():
    base = builds.key(_inputs())
    assert builds.key(_inputs()) == base and len(base) == 64
    for change in (dict(patches=_inputs()['patches'][::-1]), dict(patches=_inputs()['patches'][:1]),
                   dict(grid=dict(resolution='T42', levels=10, ranks=4, precision=8)),
                   dict(flags=dict(debug=True, optimization=None, mars=False)),
                   dict(toolchain=dict(mpirun=dict(path='/usr/bin/mpirun', version='mpirun (Open MPI) 5.0.3'),
                                       mpif90_line='gfortran -lmpi_mpifh -lmpi')),
                   dict(configured={name: 'e' * 64 for name in builds.CONFIGURED})):
        assert builds.key(_inputs(**change)) != base, change
    assert builds.executable_name(DEFAULTS) == 'most_plasim_t21_l10_p4.x'
    assert builds.folder(STORE or LAB, base).name == f'exoplasim-{base[:16]}'


def test_a_build_compiles_in_a_fixed_environment(monkeypatch):
    monkeypatch.setenv('MOST_F90_OPTS', '-O0')
    monkeypatch.setenv('MAKEFLAGS', 'MOST_F90_OPTS=-O0')
    assert set(builds.environment()) == {'PATH', 'HOME', 'TMPDIR', 'LANG', 'LC_ALL'}


@needs_build
def test_the_inputs_name_the_series_patches_the_compile_files_and_the_mpi_library():
    made, payload = builds.gather(DEFAULTS, env=ENV)
    assert [(p['name'], p['sha256']) for p in made['patches']] == \
        [(name, _sha256(builds.PATCHES / name)) for name in ex.series(DEFAULTS)]
    assert [name for name, _ in payload['patches']] == list(ex.series(DEFAULTS))
    assert made['archive']['sha256'] == hashlib.sha256(payload['archive']).hexdigest()
    assert set(made['configured']) == set(builds.CONFIGURED)
    toolchain = made['toolchain']
    assert set(builds.TOOLS) <= set(toolchain) and 'mpi' in toolchain['mpif90_line']
    for bad in ({'precision': 16}, {'precision': '8'}, {'levels': '10'}, {'ranks': 0}, {'resolution': 'T31'}):
        with pytest.raises((DataError, SpecError)):
            builds.gather({**DEFAULTS, **bad}, env=ENV)


@pytest.fixture(scope='module')
def deployed_point():
    """The build at the series' first ten patches, the point Terluna deployed."""
    run = {**DEFAULTS, 'patches': list(ex.series(DEFAULTS))[:10]}
    return run, builds.build(run, store=STORE, env=ENV)


@pytest.fixture(scope='module')
def eleven_point():
    """The build at the series' first eleven patches: Terluna's ten and the lab's patch 11, before the surface gust."""
    run = {**DEFAULTS, 'patches': list(ex.series(DEFAULTS))[:11]}
    return run, builds.build(run, store=STORE, env=ENV)


@pytest.fixture(scope='module')
def thirteen_point():
    """The build at the series' first thirteen patches, through the surface gust and the similarity over water, before
    the rain from its drops."""
    run = {**DEFAULTS, 'patches': list(ex.series(DEFAULTS))[:13]}
    return run, builds.build(run, store=STORE, env=ENV)


@pytest.fixture(scope='module')
def fourteen_point():
    """The build at the series' first fourteen patches, through the rain from its drops, before the twilight's clear
    share."""
    run = {**DEFAULTS, 'patches': list(ex.series(DEFAULTS))[:14]}
    return run, builds.build(run, store=STORE, env=ENV)


@pytest.fixture(scope='module')
def fifteen_point():
    """The build at the series' first fifteen patches, through the twilight's clear share, before its single count."""
    run = {**DEFAULTS, 'patches': list(ex.series(DEFAULTS))[:15]}
    return run, builds.build(run, store=STORE, env=ENV)


@pytest.fixture(scope='module')
def sixteen_point():
    """The build at the series' first sixteen patches, through the twilight's single count, before the wind at 10 m."""
    run = {**DEFAULTS, 'patches': list(ex.series(DEFAULTS))[:16]}
    return run, builds.build(run, store=STORE, env=ENV)


@pytest.fixture(scope='module')
def whole_point():
    """The build of the whole series, as the defaults name it."""
    return DEFAULTS, builds.build(DEFAULTS, store=STORE, env=ENV)


@needs_build
def test_the_deployed_points_build_compiles_terlunas_deployed_sources(deployed_point):
    run, folder = deployed_point
    record = json.loads((folder / 'build.json').read_text())
    deployed = {name: digest for digest, name in (line.split() for line in DEPLOYED.read_text().splitlines())}
    package = folder / 'exoplasim'
    assert {name: _sha256(package / name) for name in deployed} == deployed == record['sources']
    executable = package / 'plasim' / 'run' / record['executable']['name']
    assert _sha256(executable) == record['executable']['sha256']
    made, _ = builds.gather(run, env=ENV)
    assert record['key'] == builds.key(made) and folder == builds.folder(STORE, record['key'])
    assert not any(p.stat().st_mode & 0o222 for p in (folder, folder / 'build.json', executable))   # read-only
    assert builds.build(run, store=STORE, env=ENV) == folder  # a build in the store stands


def _run_plasim(folder, executable, steps: int, *, output: bool = True) -> subprocess.CompletedProcess:
    """PlaSim run for `steps` steps in a folder the adapter wrote, with the build's executable, run from the build's
    own folder; with `output` False PlaSim's output files stay unwritten (NOUTPUT 0) and its restart alone records the
    run. Refused where PlaSim aborts, which mpirun reports with its own exit code of 0 (mpimod.f90:385)."""
    text = (folder / 'plasim_namelist').read_text()
    entries = [('N_RUN_YEARS', 0), ('N_RUN_MONTHS', 0), ('N_RUN_DAYS', 0), ('N_RUN_STEPS', steps)]
    for name, value in entries + ([] if output else [('NOUTPUT', 0)]):
        text, count = re.subn(rf'^ {name} = .*$', f' {name} = {value}', text, flags=re.M)
        assert count == 1, name
    (folder / 'plasim_namelist').write_text(text)
    done = subprocess.run(['nice', '-n', '10', 'mpirun', '-np', str(DEFAULTS['ranks']), str(executable)],
                          cwd=folder, capture_output=True, text=True, timeout=900)
    assert done.returncode == 0 and 'MPI_ABORT' not in done.stdout + done.stderr, done.stderr[-2000:]
    assert not (folder / 'Abort_Message').exists() and (folder / 'plasim_status').is_file()
    return done


def _hashes(folder, executable, steps: int, *, output: bool = True) -> dict:
    """PlaSim run in a folder the adapter wrote, and the sha256 of the output and the restart it writes there. Every
    file the run wrote is then removed, the restart's 7 MB among them, so that the folder is as the adapter wrote
    it, but for the run's length in plasim_namelist, and takes another run."""
    written = {p.name for p in folder.iterdir()}
    _run_plasim(folder, executable, steps, output=output)
    made = [p for p in folder.iterdir() if p.name not in written]
    out = {p.name: _sha256(p) for p in made if p.name in ('plasim_output', 'plasim_status')}
    for p in made:
        p.unlink()
    return out


def _diagnostic(folder, label: str) -> str | None:
    match = re.search(r'\* ' + re.escape(label) + r'[^:]*:\s*([-0-9.]+)', (folder / 'plasim_diag').read_text())
    return match.group(1) if match else None


@needs_build
@pytest.mark.parametrize('world, scenario', [('earth', 'earth/control'), ('waterworld-seed', 'waterworld-seed/gaean-1bar')])
def test_plasim_compiled_by_the_lab_runs_on_the_files_the_lab_writes(deployed_point, tmp_path, world, scenario):
    run, folder = deployed_point
    executable = folder / 'exoplasim' / 'plasim' / 'run' / builds.executable_name(run)
    calendar = derive.calendar(LIB.world(world), run)
    ex.write_run(tmp_path / 'run', LIB.world(world), LIB.scenario(scenario), run,
                 calibrations=ex.Calibrations.identity(), store=STORE)
    _run_plasim(tmp_path / 'run', executable, 4)
    assert (tmp_path / 'run' / 'plasim_output').stat().st_size > 0
    assert float(_diagnostic(tmp_path / 'run', 'Solar    day')) == pytest.approx(calendar['model_day_s'], abs=0.0501)
    assert int(_diagnostic(tmp_path / 'run', 'Timesteps / day')) == calendar['steps_per_model_day']
    assert int(_diagnostic(tmp_path / 'run', 'Days / Year')) == calendar['n_days_per_year']
    (tmp_path / 'run' / 'plasim_status').unlink()       # the restart, 7 MB, which the test reads nothing from


def _executable(build, run):
    return build / 'exoplasim' / 'plasim' / 'run' / builds.executable_name(run)


def _differing(a, b) -> set:
    """The names of the files that differ between two run folders the adapter wrote."""
    return {p.name for p in a.iterdir() if p.read_bytes() != (b / p.name).read_bytes()}


@needs_build
def test_patch_11_at_its_default_runs_byte_for_byte_as_the_build_without_it(deployed_point, eleven_point, tmp_path):
    """Earth's control with ice optics on, two days: the folder the adapter writes for the build of patches 01-10,
    without ZICEW, gives the same output under the build of patches 01-11, where patch 11 holds patch 10's constants;
    the weights the adapter writes for that build, from the Sun's spectrum, change it."""
    (ten, ten_build), (eleven, eleven_build) = deployed_point, eleven_point
    ice = lambda run: {**run, 'switches': {**run['switches'], 'ice_optics': True}}
    executables = {'ten': _executable(ten_build, ten), 'eleven': _executable(eleven_build, eleven)}
    ex.write_run(tmp_path / 'ten', EARTH, CONTROL, ice(ten), calibrations=ex.Calibrations.identity(), store=STORE)
    ex.write_run(tmp_path / 'spectrum', EARTH, CONTROL, ice(eleven), calibrations=ex.Calibrations.identity(), store=STORE)
    assert 'ZICEW' not in (tmp_path / 'ten' / 'radmod_namelist').read_text()
    # The two folders differ in the four ZICEW lines alone, so that a change of output comes from the ice optics.
    assert _differing(tmp_path / 'ten', tmp_path / 'spectrum') == {'radmod_namelist'}
    lines = lambda name: (tmp_path / name / 'radmod_namelist').read_text().splitlines()
    assert [l for l in lines('spectrum') if 'ZICEW' not in l] == lines('ten')
    assert len([l for l in lines('spectrum') if 'ZICEW' in l]) == 4
    # The folder without ZICEW under each build, then the folder with the Sun's weights under the build of 01-11.
    runs = (('ten', 'ten', 'ten'), ('default', 'ten', 'eleven'), ('spectrum', 'spectrum', 'eleven'))
    out = {name: _hashes(tmp_path / folder, executables[build], 96) for name, folder, build in runs}
    assert set(out['ten']) == {'plasim_output', 'plasim_status'} and out['default'] == out['ten']
    assert out['spectrum']['plasim_output'] != out['default']['plasim_output']


def _with_gust(run: dict, choice: str) -> dict:
    return {**run, 'switches': {**run['switches'], 'surface_gust': choice}}


@needs_build
def test_patches_12_and_13_at_their_defaults_run_byte_for_byte_as_the_builds_without_them(eleven_point,
                                                                                         thirteen_point, tmp_path):
    """Earth's control over two days. The folder the adapter writes for the build of patches 01-11, whose fluxmod
    namelist names neither switch, gives the same output and restart under the build of patches 01-12, where NGUST
    takes its default, and so does the folder written for patches 01-13 with the released model's transfer, NGUST
    and NSIMW 0. With Beljaars's gust on, the folder written for patches 01-12 gives the same output and restart under
    the build of patches 01-13, where NSIMW takes its default. The gust changes the output, and the similarity over
    water changes it again. Each run's files are removed once their hashes are taken."""
    (eleven, eleven_build), (thirteen, thirteen_build) = eleven_point, thirteen_point
    patches = list(thirteen['patches'])
    assert patches[11:] == [ex.PATCH_12, ex.PATCH_13] and eleven['patches'] == patches[:11]
    twelve = {**thirteen, 'patches': patches[:12]}
    executables = {'eleven': _executable(eleven_build, eleven),
                   'twelve': _executable(builds.build(twelve, store=STORE, env=ENV), twelve),
                   'thirteen': _executable(thirteen_build, thirteen)}
    written = {'eleven': eleven, 'none': thirteen, 'gust12': _with_gust(twelve, 'beljaars'),
               'similarity': _with_gust(thirteen, 'beljaars_similarity')}
    for name, run in written.items():
        ex.write_run(tmp_path / name, EARTH, CONTROL, run, calibrations=ex.Calibrations.identity(), store=STORE)
    # The folders differ in fluxmod's namelist alone, so that a change of output comes from the surface transfer.
    flux = lambda name: (tmp_path / name / 'fluxmod_namelist').read_text().splitlines()[1:-1]
    assert [flux(name) for name in written] == \
        [[], [' NGUST = 0', ' NSIMW = 0'], [' NGUST = 1'], [' NGUST = 1', ' NSIMW = 1']]
    for name in ('none', 'gust12', 'similarity'):
        assert _differing(tmp_path / 'eleven', tmp_path / name) == {'fluxmod_namelist'}
    out = {(name, build): _hashes(tmp_path / name, executables[build], 96)
           for name, build in (('eleven', 'eleven'), ('eleven', 'twelve'), ('none', 'thirteen'),
                               ('gust12', 'twelve'), ('gust12', 'thirteen'), ('similarity', 'thirteen'))}
    assert set(out['eleven', 'eleven']) == {'plasim_output', 'plasim_status'}
    assert out['eleven', 'twelve'] == out['eleven', 'eleven'] and out['none', 'thirteen'] == out['eleven', 'eleven']
    assert out['gust12', 'thirteen'] == out['gust12', 'twelve']
    changed = (('eleven', 'eleven'), ('gust12', 'twelve'), ('similarity', 'thirteen'))
    assert len({out[key]['plasim_output'] for key in changed}) == 3


@needs_build
def test_under_the_moons_gravity_the_gust_and_the_similarity_run_over_open_sea(whole_point, tmp_path):
    """Earth's control with the Moon's gravity in place of its own, a made-up world that puts ice-free sea under a
    sixth of Earth's gravity: from a cold start the whole series runs one day with Beljaars's gust, alone and with
    the similarity over water beside it, under the floating-point traps ExoPlaSim compiles with, and the similarity
    changes the state the run ends in. The run tests the code's path at that gravity and no climate; it writes no
    output, and its restart is removed once its hash is taken."""
    whole, whole_build = whole_point
    g_moon, body = derive.gravity(LIB.world('moon')), EARTH['body']
    spin = (2.0 / 3.0) * derive.rotation_rate(EARTH) ** 2 * body['radius_m']
    light = {**EARTH, 'id': 'earth-under-lunar-gravity',
             'body': {'radius_m': body['radius_m'], 'gm_m3_s2': (g_moon + spin) * body['radius_m'] ** 2}}
    assert derive.gravity(light) == pytest.approx(g_moon, rel=1e-12) and g_moon == pytest.approx(1.6242, abs=1e-4)
    day, restarts = derive.calendar(light, whole)['steps_per_model_day'], {}
    for choice in ('beljaars', 'beljaars_similarity'):
        ex.write_run(tmp_path / choice, light, CONTROL, _with_gust(whole, choice),
                     calibrations=ex.Calibrations.identity(), store=STORE)
        assert f' GA = {derive.gravity(light)!r}\n' in (tmp_path / choice / 'planet_namelist').read_text()
        restarts[choice] = _hashes(tmp_path / choice, _executable(whole_build, whole), day, output=False)
    assert day == 48 and all(set(found) == {'plasim_status'} for found in restarts.values())
    assert restarts['beljaars'] != restarts['beljaars_similarity']


# Earth's control's air at 2 m for the rain's fall law, and births made up for it, since no calibration of Earth's
# exists: the runs below read the code's path from them and no climate.
EARTH_RAIN = dict(surface_temperature_k=288.15, surface_relative_humidity=0.7)
MADE_UP_BIRTHS = dict(rule='share', new_rain_m=0.4e-3, melted_rain_m=0.8e-3)
# The released model's values for the calibrations a later run states, with the curved air's terms and the gas bands
# switched off: the namelists a first run writes, in a run that may also state the rain's drops.
RELEASED = dict(rayleigh_scale=1.0, water_absorption_scale=1.0, water_continuum=ex.PLASIM_TH2OC)


def _plain(run: dict, rain: str) -> dict:
    return {**run, 'switches': {**run['switches'], 'twilight': 'none', 'gas_bands': False, 'rain_evaporation': rain}}


@needs_build
def test_patch_14_at_its_default_runs_byte_for_byte_as_the_build_without_it(thirteen_point, fourteen_point, tmp_path):
    """Earth's control over two days. The folder the adapter writes for the build of patches 01-13, whose rainmod
    namelist names none of patch 14's entries, gives the same output and restart under the build of patches 01-14,
    where NEVAPPREC keeps PlaSim's own 1, and so do the folders written for that build with PlaSim's constant, as a
    first run and with the released model's values stated as calibrations. With the rain evaporated from its drops'
    sizes, by the fall law of Earth's own air and births made up for the test, the folder differs in rainmod's
    namelist and the table alone, and the output changes. Without its table that run stops with PlaSim's abort
    message. Each run's files are removed once their hashes are taken."""
    (thirteen, thirteen_build), (fourteen, fourteen_build) = thirteen_point, fourteen_point
    patches = list(fourteen['patches'])
    assert patches[13:] == [ex.PATCH_14] and thirteen['patches'] == patches[:13]
    air = drops.Column(gravity_m_s2=derive.gravity(EARTH), surface_pressure_pa=CONTROL['air']['surface_pressure_pa'],
                       air=DryAir(CONTROL['air']['surface_pressure_pa']), **EARTH_RAIN)
    rain = ex.RainDrops.from_settings(rain_drops.settings(air, MADE_UP_BIRTHS))
    assert (rain.self_collection_m3_kg_s, rain.density_exponent) == (5.78, 0.0)        # Morrison's own, in Earth's air
    executables = {'thirteen': _executable(thirteen_build, thirteen), 'fourteen': _executable(fourteen_build, fourteen)}
    first, later = ex.Calibrations.identity(), ex.Calibrations(**RELEASED)
    written = {'thirteen': (thirteen, first), 'default': (fourteen, first),
               'gamma': (_plain(fourteen, 'gamma'), later),
               'sized': (_plain(fourteen, 'drop_sizes'), ex.Calibrations(**RELEASED, rain_drops=rain))}
    for name, (run, calibrations) in written.items():
        ex.write_run(tmp_path / name, EARTH, CONTROL, run, calibrations=calibrations, store=STORE)
    # The folders differ in rainmod's namelist alone, and the drops' folder holds the table besides, so that a change
    # of output comes from the rain's evaporation.
    entries = lambda name: [line for line in (tmp_path / name / 'rainmod_namelist').read_text().splitlines()
                            if line.split()[0] == 'NEVAPPREC' or 'RDROP' in line]
    assert entries('thirteen') == [] and entries('default') == entries('gamma') == [' NEVAPPREC = 1']
    assert entries('sized') == [' NEVAPPREC = 2', ' NRDROP_JOIN = 2', ' RDROP_WARM = 0.0004', ' RDROP_MELT = 0.0008',
                                ' RDROP_KSC = 5.78', ' RDROP_RHOEXP = 0.0', ' RDROP_STEP = 1000.0']
    for name in ('default', 'gamma', 'sized'):
        assert _differing(tmp_path / 'thirteen', tmp_path / name) == {'rainmod_namelist'}
    names = lambda name: {p.name for p in (tmp_path / name).iterdir()}
    assert names('sized') - names('thirteen') == {ex.RAIN_TABLE} and names('gamma') == names('thirteen')
    out = {(name, build): _hashes(tmp_path / name, executables[build], 96)
           for name, build in (('thirteen', 'thirteen'), ('thirteen', 'fourteen'), ('default', 'fourteen'),
                               ('gamma', 'fourteen'), ('sized', 'fourteen'))}
    assert set(out['thirteen', 'thirteen']) == {'plasim_output', 'plasim_status'}
    for key in (('thirteen', 'fourteen'), ('default', 'fourteen'), ('gamma', 'fourteen')):
        assert out[key] == out['thirteen', 'thirteen'], key
    assert out['sized', 'fourteen']['plasim_output'] != out['gamma', 'fourteen']['plasim_output']
    assert out['sized', 'fourteen']['plasim_status'] != out['gamma', 'fourteen']['plasim_status']
    # Without the table the run stops at its start, on every rank, and leaves PlaSim's abort message.
    (tmp_path / 'sized' / ex.RAIN_TABLE).unlink()
    before = names('sized')
    done = subprocess.run(['nice', '-n', '10', 'mpirun', '-np', str(DEFAULTS['ranks']), str(executables['fourteen'])],
                          cwd=tmp_path / 'sized', capture_output=True, text=True, timeout=300)
    assert 'nevapprec 2 reads lab_rain_law.txt, which is missing' in (tmp_path / 'sized' / 'Abort_Message').read_text()
    assert not (tmp_path / 'sized' / 'plasim_status').exists() and 'MPI_ABORT' in done.stdout + done.stderr
    for name in names('sized') - before:
        (tmp_path / 'sized' / name).unlink()


@needs_build
def test_under_the_moons_gravity_the_rain_evaporates_from_its_drops(whole_point, tmp_path):
    """Earth's control with the Moon's gravity in place of its own, as the gust's test makes it, with the fall law of
    the Open Moon's air, its self-collection rate and density exponent, and Terluna's births for the Open Moon: from
    a cold start the whole series runs two days with the rain evaporated from its drops' sizes, under the
    floating-point traps ExoPlaSim compiles with, and ends in another state than the run with PlaSim's constant. The
    run tests the code's path at that gravity and no climate; it writes no output, and its restart is removed once
    its hash is taken."""
    whole, whole_build = whole_point
    g_moon, body = derive.gravity(LIB.world('moon')), EARTH['body']
    spin = (2.0 / 3.0) * derive.rotation_rate(EARTH) ** 2 * body['radius_m']
    light = {**EARTH, 'id': 'earth-under-lunar-gravity',
             'body': {'radius_m': body['radius_m'], 'gm_m3_s2': (g_moon + spin) * body['radius_m'] ** 2}}
    moon_air = LIB.scenario('moon/open-moon')['air']['surface_pressure_pa']
    air = drops.Column(gravity_m_s2=g_moon, surface_pressure_pa=moon_air, surface_temperature_k=300.4,
                       surface_relative_humidity=0.61, air=earthlike_air(moon_air, 400.0))
    rain = ex.RainDrops.from_settings(rain_drops.settings(air, rain_drops.TERLUNA_OPEN_MOON_BIRTHS))
    # Terluna's 2.919 m3/kg/s and 0.687, to the rounding of the air's temperature and humidity here.
    assert rain.self_collection_m3_kg_s == pytest.approx(2.919, abs=5e-4) and rain.birth_rule == 'share'
    assert rain.density_exponent == pytest.approx(0.687, abs=1e-3)
    steps, restarts = 2 * derive.calendar(light, whole)['steps_per_model_day'], {}
    for choice, calibrations in (('gamma', ex.Calibrations(**RELEASED)),
                                 ('drop_sizes', ex.Calibrations(**RELEASED, rain_drops=rain))):
        ex.write_run(tmp_path / choice, light, CONTROL, _plain(whole, choice), calibrations=calibrations, store=STORE)
        assert f' GA = {derive.gravity(light)!r}\n' in (tmp_path / choice / 'planet_namelist').read_text()
        restarts[choice] = _hashes(tmp_path / choice, _executable(whole_build, whole), steps, output=False)
    assert steps == 96 and all(set(found) == {'plasim_status'} for found in restarts.values())
    assert restarts['gamma'] != restarts['drop_sizes']


# The curved air's twilight.

# The Open Moon's ledger as the lab keeps it, on the released ten levels: on Earth's control, terms made up for the
# tests below, which run the code's path and no climate.
LEDGER = LAB.parent / 'python' / 'climate' / 'results' / 'gcm' / 'twilight.json'


def _ledger() -> ex.Ledger:
    """The ledger's full terms, the curved light with the shells' widening, as Terluna's runner summed them for its
    "full" mode (exoplasim_run.py:885-902 at 186b294), with the Moon's slant factors."""
    product = json.loads(LEDGER.read_text())
    term, cone, longwave = product['gcm_term'], product['gcm_term_cone'], product['longwave']
    return ex.Ledger(
        elevation_deg=tuple(term['elevation_deg']), ground=tuple(term['ground']),
        layers=tuple(tuple(q + c for q, c in zip(lq, lc)) for lq, lc in zip(term['layers'], cone['layers'])),
        escape_w_m2=tuple(a + b for a, b in zip(longwave['gcm_layers']['curved'], longwave['gcm_layers']['cone']))
        + (longwave['ground_curved_w_m2'],),
        escape_temperature_k=tuple(longwave['gcm_layers']['temperature_k']) + (longwave['ground_temperature_k'],),
        slant=tuple(product['magnification'][k] for k in 'abc'),
        slant_air=tuple(product['magnification_air'][k] for k in 'abc'))


def _twilit(run: dict, twilight: str, clear_sky: bool, **switches) -> dict:
    """Earth's control with the curved air's terms on or off, the clear-sky diagnostic on or off, and `switches`."""
    return {**run, 'clear_sky': clear_sky, 'switches': {**run['switches'], 'twilight': twilight, 'gas_bands': False,
                                                         'rain_evaporation': 'gamma', **switches}}


@needs_build
def test_patches_15_and_16_at_their_defaults_run_byte_for_byte_as_the_build_without_them(fourteen_point, fifteen_point,
                                                                                         sixteen_point, tmp_path):
    """Earth's control over two days, with the released model's values stated as calibrations and the Open Moon's
    ledger for the curved air's terms. With those terms on and off, and the clear-sky diagnostic on and off, the
    folders written for the build of patches 01-14, for that of 01-15 with NTWLCLEAR 0 and for that of 01-16 with
    NTWLZERO 0 as well differ in those entries alone and give the same output and restart, each under its own build;
    the folder that names neither entry gives them under the build of patches 01-16 too. The twilight changes the
    run, and with it off the diagnostic leaves the run's state as it was. Each run's files are removed once their
    hashes are taken."""
    (fourteen, b14), (fifteen, b15), (sixteen, b16) = fourteen_point, fifteen_point, sixteen_point
    patches = list(ex.series(sixteen))
    assert patches[14:] == [ex.PATCH_15, ex.PATCH_16]
    assert fourteen['patches'] == patches[:14] and fifteen['patches'] == patches[:15]
    points = {'14': (fourteen, _executable(b14, fourteen)), '15': (fifteen, _executable(b15, fifteen)),
              '16': (sixteen, _executable(b16, sixteen))}
    ledger, out = _ledger(), {}
    for twilight in ('full', 'none'):
        calibrations = ex.Calibrations(**RELEASED, ledger=ledger if twilight == 'full' else None)
        for clear_sky in (True, False):
            folder = lambda point: tmp_path / f'{twilight}-{int(clear_sky)}-{point}'
            for point, (run, _) in points.items():
                ex.write_run(folder(point), EARTH, CONTROL, _twilit(run, twilight, clear_sky),
                             calibrations=calibrations, store=STORE)
            assert _differing(folder('14'), folder('15')) == _differing(folder('14'), folder('16')) == \
                {'radmod_namelist'}
            entries = lambda point: [line for line in (folder(point) / 'radmod_namelist').read_text().splitlines()
                                     if line.split()[0] in ('NTWLCLEAR', 'NTWLZERO')]
            assert (entries('14'), entries('15'), entries('16')) == \
                ([], [' NTWLCLEAR = 0'], [' NTWLCLEAR = 0', ' NTWLZERO = 0'])
            lines = lambda point: (folder(point) / 'radmod_namelist').read_text().splitlines()
            assert [line for line in lines('16') if line not in entries('16')] == lines('14')
            found = {point: _hashes(folder(point), executable, 96) for point, (_, executable) in points.items()}
            assert set(found['14']) == {'plasim_output', 'plasim_status'}
            assert found['15'] == found['14'] and found['16'] == found['14'], (twilight, clear_sky)
            out[twilight, clear_sky] = found['14']
    assert 'twilight.dat' in {p.name for p in (tmp_path / 'full-1-14').iterdir()}
    assert 'twilight.dat' not in {p.name for p in (tmp_path / 'none-1-14').iterdir()}
    assert _hashes(tmp_path / 'full-1-14', points['16'][1], 96) == out['full', True]
    assert out['full', True]['plasim_status'] != out['none', True]['plasim_status']
    assert out['none', True]['plasim_status'] == out['none', False]['plasim_status']


@needs_build
def test_the_clear_share_changes_the_run_and_the_single_count_leaves_the_diagnostic_out_of_it(whole_point, tmp_path):
    """Earth's control over two days with the Open Moon's ledger, on the whole series. Without the clear-sky
    diagnostic, swr runs once a step and NTWLZERO 1 changes nothing. With it, patch 07's passes add the diagnostic's
    clear twilight below the horizon to the run's, which ends in another state than the run without the diagnostic
    (defect log C21); with NTWLZERO 1 it ends in that run's state, byte for byte, with the clear share and without
    it. The clear share changes the output and the state. Each run's files are removed once their hashes are taken."""
    whole, build = whole_point
    executable, calibrations = _executable(build, whole), ex.Calibrations(**RELEASED, ledger=_ledger())
    out = {}
    for clear_share in (False, True):
        for clear_sky in (False, True):
            for once in (False, True):
                name = f'share{int(clear_share)}-sky{int(clear_sky)}-once{int(once)}'
                run = _twilit(whole, 'full', clear_sky, twilight_clear_share=clear_share, twilight_counted_once=once)
                record = ex.write_run(tmp_path / name, EARTH, CONTROL, run, calibrations=calibrations, store=STORE)
                assert (record['switches']['twilight_clear_share'], record['switches']['twilight_counted_once']) == \
                    (clear_share, once)
                out[clear_share, clear_sky, once] = _hashes(tmp_path / name, executable, 96)
    for share in (False, True):
        state = lambda sky, once: out[share, sky, once]['plasim_status']
        assert out[share, False, True] == out[share, False, False], share
        assert state(True, True) == state(False, False) and state(True, False) != state(False, False), share
        assert out[share, True, True]['plasim_output'] != out[share, True, False]['plasim_output'], share
    for sky in (False, True):
        for kind in ('plasim_output', 'plasim_status'):
            assert out[True, sky, True][kind] != out[False, sky, True][kind], (sky, kind)


# The wind at 10 m.

def _records(path) -> list:
    """PlaSim's raw output as (header, field) pairs, after the two records that open the file: each header eight
    integers, the field's code first and the steps run seventh, and each field in single precision (outmod.f90, outini,
    writegp and writesp)."""
    data, records, i = path.read_bytes(), [], 0
    while i < len(data):
        size = struct.unpack('<i', data[i:i + 4])[0]
        assert struct.unpack('<i', data[i + 4 + size:i + 8 + size])[0] == size
        records.append(data[i + 4:i + 4 + size])
        i += size + 8
    assert len(records) % 2 == 0
    return list(zip(records[2::2], records[3::2]))


def _header(record) -> tuple:
    return struct.unpack('<8i', record[0])


def _run_records(folder, executable, steps: int) -> tuple[dict, list]:
    """PlaSim run as `_hashes` runs it, with the records of its output read before its files are removed."""
    written = {p.name for p in folder.iterdir()}
    _run_plasim(folder, executable, steps)
    records = _records(folder / 'plasim_output')
    made = [p for p in folder.iterdir() if p.name not in written]
    out = {p.name: _sha256(p) for p in made if p.name in ('plasim_output', 'plasim_status')}
    for p in made:
        p.unlink()
    return out, records


def _switched(run: dict, **switches) -> dict:
    return {**run, 'switches': {**run['switches'], **switches}}


@needs_build
def test_patch_17_at_its_default_runs_byte_for_byte_and_on_adds_the_wind_at_10_m_alone(sixteen_point, whole_point,
                                                                                     tmp_path):
    """Earth's control over two days. The folder the adapter writes for the build of patches 01-16, whose fluxmod
    namelist names no NWIND10, gives the same output and restart under the whole series' build, where NWIND10 takes
    its default, and so does the folder written for the whole series with NWIND10 0. With the wind at 10 m on, the run
    ends in the same state byte for byte, under PlaSim's own surface transfer and under Beljaars's gust with the
    similarity over water; its output holds every record of the run without it, byte for byte and in order, and after
    each 2 m temperature (167) the two components of the wind at 10 m (165 and 166) at the same output time, finite,
    below 30 m/s and somewhere nonzero. The gust with the similarity changes the run, and with it the wind at 10 m.
    Each run's files are removed once their hashes and records are taken."""
    (sixteen, b16), (whole, b17) = sixteen_point, whole_point
    patches = list(ex.series(whole))
    assert patches[16:] == [ex.PATCH_17] and sixteen['patches'] == patches[:16]
    # The whole series' build compiled the sources that models/check_patches.sh pins.
    pinned = {name: digest for digest, name in (line.split() for line in SERIES_SOURCES.read_text().splitlines())}
    assert json.loads((b17 / 'build.json').read_text())['sources'] == pinned
    executables = {'16': _executable(b16, sixteen), '17': _executable(b17, whole)}
    similarity = 'beljaars_similarity'
    written = {'sixteen': sixteen, 'default': whole, 'wind': _switched(whole, wind_10m=True),
               'gust': _switched(whole, surface_gust=similarity),
               'gust_wind': _switched(whole, surface_gust=similarity, wind_10m=True)}
    for name, run in written.items():
        record = ex.write_run(tmp_path / name, EARTH, CONTROL, run, calibrations=ex.Calibrations.identity(),
                              store=STORE)
        assert record['switches']['wind_10m'] is (name in ('wind', 'gust_wind'))
    # The folders differ in fluxmod's namelist alone.
    flux = lambda name: (tmp_path / name / 'fluxmod_namelist').read_text().splitlines()[1:-1]
    assert [flux(name) for name in written] == [
        [' NGUST = 0', ' NSIMW = 0'], [' NGUST = 0', ' NSIMW = 0', ' NWIND10 = 0'],
        [' NGUST = 0', ' NSIMW = 0', ' NWIND10 = 1'], [' NGUST = 1', ' NSIMW = 1', ' NWIND10 = 0'],
        [' NGUST = 1', ' NSIMW = 1', ' NWIND10 = 1']]
    for name in ('default', 'wind', 'gust', 'gust_wind'):
        assert _differing(tmp_path / 'sixteen', tmp_path / name) == {'fluxmod_namelist'}
    out = {(name, build): _run_records(tmp_path / name, executables[build], 96)
           for name, build in (('sixteen', '16'), ('sixteen', '17'), ('default', '17'), ('wind', '17'),
                               ('gust', '17'), ('gust_wind', '17'))}
    hashes = {key: found for key, (found, _) in out.items()}
    assert set(hashes['sixteen', '16']) == {'plasim_output', 'plasim_status'}
    assert hashes['sixteen', '17'] == hashes['sixteen', '16'] == hashes['default', '17']
    assert hashes['gust', '17']['plasim_status'] != hashes['default', '17']['plasim_status']
    winds = {}
    for off, on in (('default', 'wind'), ('gust', 'gust_wind')):
        assert hashes[on, '17']['plasim_status'] == hashes[off, '17']['plasim_status'], on
        plain, windy = out[off, '17'][1], out[on, '17'][1]
        assert [r for r in windy if _header(r)[0] not in (165, 166)] == plain
        codes = [_header(r)[0] for r in windy]
        at = [i for i, code in enumerate(codes) if code == 167]
        assert at and codes.count(165) == codes.count(166) == len(at)
        for i in at:
            assert codes[i + 1:i + 3] == [165, 166]
            assert {_header(windy[j])[2:4] + _header(windy[j])[6:7] for j in (i, i + 1, i + 2)} == \
                {_header(windy[i])[2:4] + _header(windy[i])[6:7]}
        fields = np.array([np.frombuffer(windy[i + k][1], '<f4') for i in at for k in (1, 2)])
        assert np.isfinite(fields).all() and np.abs(fields).max() < 30.0 and np.abs(fields).max() > 0.0
        winds[on] = fields
    assert not np.array_equal(winds['wind'], winds['gust_wind'])


# The level set.

# Terluna's values for the Open Moon's fifteen levels, as a study's table states them.
MOON_LEVELS = {**levels.TERLUNA_OPEN_MOON_LEVELS,
               'interfaces_m': list(levels.TERLUNA_OPEN_MOON_LEVELS['interfaces_m'])}


def _output_levels(folder) -> tuple[int, np.ndarray]:
    """The count of levels and the half levels PlaSim ran on, from the first two records of its output: the header's
    seventh integer, and the vertical coordinate table it hands its postprocessor, in single precision
    (outmod.f90, outini)."""
    data = (folder / 'plasim_output').read_bytes()
    size = struct.unpack('<i', data[:4])[0]
    count = struct.unpack('<8i', data[4:4 + size])[6]
    return count, np.frombuffer(data, '<f4', count=count, offset=4 + size + 4 + 4)


def _step(restart) -> int:
    return struct.unpack('<i', dict((name.strip(), data) for name, data in levels.read_records(restart))['nstep'])[0]


def test_a_generated_sets_build_compiles_for_its_count():
    run = {**DEFAULTS, 'levels': MOON_LEVELS}
    assert builds.executable_name(run) == 'most_plasim_t21_l15_p4.x' and derive.level_count(run) == 15
    for bad in ({'levels': {'upper': 6}}, {'levels': 10.0}, {'levels': True}):
        with pytest.raises(SpecError, match='level'):
            builds.executable_name({**DEFAULTS, **bad})


@needs_build
def test_the_released_ten_stated_as_a_generated_set_run_byte_for_byte_as_the_released_grid(whole_point, tmp_path):
    """Earth's control over two days. Stated at the heights of the released model's own seventh to ninth half levels,
    a generated set is the released ten, in the compiled model's doubles, and the run reads them from SIGH under
    NEQSIG -1 with its top friction from TFRC. Its build is the released grid's, its folder differs in those three
    entries alone, and it gives the output and the restart of the run that leaves the levels to PlaSim's formula.
    Each run's files are removed once their hashes are taken."""
    whole, whole_build = whole_point
    ten = levels.plasim_half()
    heights = [float(z) for z in levels.heights_m(ten[6:9], derive.planet(EARTH, CONTROL)['scale_height_m'])]
    stated = {**whole, 'levels': dict(scale_height_m='scenario', upper=6, interfaces_m=heights)}
    found = derive.levels(stated, EARTH, CONTROL)
    assert found['basis'] == 'generated' and found['half_levels'] == derive.levels(whole)['half_levels'] == tuple(ten)
    assert builds.gather(stated, env=ENV)[0] == builds.gather(whole, env=ENV)[0]          # one key, one build
    for name, run in (('formula', whole), ('stated', stated)):
        ex.write_run(tmp_path / name, EARTH, CONTROL, run, calibrations=ex.Calibrations.identity(), store=STORE)
    assert _differing(tmp_path / 'formula', tmp_path / 'stated') == {'plasim_namelist'}
    lines = lambda name: (tmp_path / name / 'plasim_namelist').read_text().splitlines()
    assert [line for line in lines('formula') if line not in lines('stated')] == [' NEQSIG = 0']
    assert [line.split(' = ')[0] for line in lines('stated') if line not in lines('formula')] == \
        [' NEQSIG', ' SIGH', ' TFRC']
    out = {name: _hashes(tmp_path / name, _executable(whole_build, whole), 96) for name in ('formula', 'stated')}
    assert set(out['formula']) == {'plasim_output', 'plasim_status'} and out['stated'] == out['formula']


@needs_build
def test_plasim_runs_on_a_generated_set_and_starts_there_from_a_restart_carried_onto_it(whole_point, tmp_path):
    """Earth's control with the Moon's gravity in place of its own, as the gust's test makes it, on Terluna's values
    for the Open Moon's fifteen levels. From a cold start the build compiled for fifteen levels runs two days under
    the floating-point traps ExoPlaSim compiles with, and its output states the fifteen levels and the set's half
    levels. A ten-level run's restart, carried onto the set by the conservative remap, starts a fifteen-level run,
    which counts its steps on from the restart's and ends in another state than the cold start. The carry keeps each
    spectral field's column integrals, and the same restart carried onto its own ten levels comes back byte for byte.
    The runs test the code's path and no climate; each run's files are removed once read."""
    whole, whole_build = whole_point
    g_moon, body = derive.gravity(LIB.world('moon')), EARTH['body']
    spin = (2.0 / 3.0) * derive.rotation_rate(EARTH) ** 2 * body['radius_m']
    light = {**EARTH, 'id': 'earth-under-lunar-gravity',
             'body': {'radius_m': body['radius_m'], 'gm_m3_s2': (g_moon + spin) * body['radius_m'] ** 2}}
    fifteen = {**whole, 'levels': MOON_LEVELS}
    half = np.array(derive.levels(fifteen)['half_levels'])
    build = builds.build(fifteen, store=STORE, env=ENV)
    record = json.loads((build / 'build.json').read_text())
    assert record['inputs']['grid'] == dict(resolution='T21', levels=15, ranks=4, precision=8)
    assert record['inputs']['patches'] == json.loads((whole_build / 'build.json').read_text())['inputs']['patches']
    executable = _executable(build, fifteen)
    assert executable.name == 'most_plasim_t21_l15_p4.x' and executable != _executable(whole_build, whole)

    def run(name, settings, exe, restart=None):
        """Two days in a folder the adapter writes; returns the folder, which keeps the run's files."""
        folder = tmp_path / name
        ex.write_run(folder, light, CONTROL, settings, calibrations=ex.Calibrations.identity(), store=STORE)
        if restart is not None:
            shutil.copyfile(restart, folder / 'plasim_restart')
        _run_plasim(folder, exe, 96)
        return folder

    cold = run('cold', fifteen, executable)
    count, table = _output_levels(cold)
    assert count == 15 and np.array_equal(table, half.astype('<f4'))
    printed = re.findall(r'^ \* +\d+ \* +([0-9.]+) +[0-9.]+ +[0-9.]+ \*$', (cold / 'plasim_diag').read_text(),
                         flags=re.M)                    # the table of levels: sigma, the reference temperature, km
    assert [float(x) for x in printed] == [round(float(x), 8) for x in levels.full_levels(half)]
    cold_step, cold_end = _step(cold / 'plasim_status'), _sha256(cold / 'plasim_status')
    shutil.rmtree(cold)

    ten = run('ten', whole, _executable(whole_build, whole))
    assert _output_levels(ten)[0] == 10 and _step(ten / 'plasim_status') == cold_step
    carried = tmp_path / 'carried'
    report = levels.carry_restart(ten / 'plasim_status', carried, levels.plasim_half(), half)
    assert report['levels'] == [10, 15] and set(report['fields']) == set(
        levels.SPECTRAL_BY_LEVEL + levels.GRID_BY_LEVEL + levels.GRID_BY_LEVEL_AND_GROUND)
    for name in levels.SPECTRAL_BY_LEVEL:                   # vorticity, divergence, temperature and humidity
        field = report['fields'][name]
        assert field['column_integral_scale'] > 0.0
        assert field['column_integral_change'] <= 1e-10 * field['column_integral_scale'], name
    same = tmp_path / 'same'
    levels.carry_restart(ten / 'plasim_status', same, levels.plasim_half(), levels.plasim_half())
    assert same.read_bytes() == (ten / 'plasim_status').read_bytes()
    shutil.rmtree(ten)
    same.unlink()

    warm = run('warm', fifteen, executable, restart=carried)
    assert 'variables in file <plasim_restart>' in (warm / 'plasim_diag').read_text()
    assert _output_levels(warm)[0] == 15 and _step(warm / 'plasim_status') == cold_step + 96
    assert _sha256(warm / 'plasim_status') != cold_end
    shutil.rmtree(warm)
    carried.unlink()
