"""ExoPlaSim's builds: their keys, a build of the series' deployed point against Terluna's deployed sources, and PlaSim
compiled by the lab running on run folders the lab's adapter writes."""
import hashlib
import json
import re
import shutil
import subprocess

import pytest

from atmosphere.radiative_convective.thermodynamics import DryAir, earthlike_air
from atmosphere.rain import drops
from climate.gcm import rain_drops
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
def test_patch_14_at_its_default_runs_byte_for_byte_as_the_build_without_it(thirteen_point, whole_point, tmp_path):
    """Earth's control over two days. The folder the adapter writes for the build of patches 01-13, whose rainmod
    namelist names none of patch 14's entries, gives the same output and restart under the whole series' build, where
    NEVAPPREC keeps PlaSim's own 1, and so do the folders written for the whole series with PlaSim's constant, as a
    first run and with the released model's values stated as calibrations. With the rain evaporated from its drops'
    sizes, by the fall law of Earth's own air and births made up for the test, the folder differs in rainmod's
    namelist and the table alone, and the output changes. Without its table that run stops with PlaSim's abort
    message. Each run's files are removed once their hashes are taken."""
    (thirteen, thirteen_build), (whole, whole_build) = thirteen_point, whole_point
    patches = list(ex.series(whole))
    assert patches[13:] == [ex.PATCH_14] and thirteen['patches'] == patches[:13]
    # The whole series' build compiled the sources that models/check_patches.sh pins.
    pinned = {name: digest for digest, name in (line.split() for line in SERIES_SOURCES.read_text().splitlines())}
    assert json.loads((whole_build / 'build.json').read_text())['sources'] == pinned
    air = drops.Column(gravity_m_s2=derive.gravity(EARTH), surface_pressure_pa=CONTROL['air']['surface_pressure_pa'],
                       air=DryAir(CONTROL['air']['surface_pressure_pa']), **EARTH_RAIN)
    rain = ex.RainDrops.from_settings(rain_drops.settings(air, MADE_UP_BIRTHS))
    assert (rain.self_collection_m3_kg_s, rain.density_exponent) == (5.78, 0.0)        # Morrison's own, in Earth's air
    executables = {'thirteen': _executable(thirteen_build, thirteen), 'whole': _executable(whole_build, whole)}
    first, later = ex.Calibrations.identity(), ex.Calibrations(**RELEASED)
    written = {'thirteen': (thirteen, first), 'default': (whole, first), 'gamma': (_plain(whole, 'gamma'), later),
               'sized': (_plain(whole, 'drop_sizes'), ex.Calibrations(**RELEASED, rain_drops=rain))}
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
           for name, build in (('thirteen', 'thirteen'), ('thirteen', 'whole'), ('default', 'whole'),
                               ('gamma', 'whole'), ('sized', 'whole'))}
    assert set(out['thirteen', 'thirteen']) == {'plasim_output', 'plasim_status'}
    for key in (('thirteen', 'whole'), ('default', 'whole'), ('gamma', 'whole')):
        assert out[key] == out['thirteen', 'thirteen'], key
    assert out['sized', 'whole']['plasim_output'] != out['gamma', 'whole']['plasim_output']
    assert out['sized', 'whole']['plasim_status'] != out['gamma', 'whole']['plasim_status']
    # Without the table the run stops at its start, on every rank, and leaves PlaSim's abort message.
    (tmp_path / 'sized' / ex.RAIN_TABLE).unlink()
    before = names('sized')
    done = subprocess.run(['nice', '-n', '10', 'mpirun', '-np', str(DEFAULTS['ranks']), str(executables['whole'])],
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
