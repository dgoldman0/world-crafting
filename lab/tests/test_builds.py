"""ExoPlaSim's builds: their keys, a build of the series' deployed point against Terluna's deployed sources, and PlaSim
compiled by the lab running on run folders the lab's adapter writes."""
import hashlib
import json
import re
import shutil
import subprocess

import pytest

from worldlab import builds, derive, exoplasim as ex
from worldlab.data import DataError
from worldlab.roots import root
from worldlab.spec import LAB, Library, SpecError

LIB = Library()
DEFAULTS = LIB.defaults('exoplasim/defaults')
EARTH, CONTROL = LIB.world('earth'), LIB.scenario('earth/control')
STORE, ENV = root('store'), root('env')
DEPLOYED = LAB.parent / 'models' / 'exoplasim' / 'expected.sha256'
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


def _run_plasim(folder, executable, steps: int) -> subprocess.CompletedProcess:
    """PlaSim run for `steps` steps in a folder the adapter wrote, with the build's executable; refused where PlaSim
    aborts, which mpirun reports with its own exit code of 0 (mpimod.f90:385)."""
    shutil.copy2(executable, folder / executable.name)
    text = (folder / 'plasim_namelist').read_text()
    for name, value in (('N_RUN_YEARS', 0), ('N_RUN_MONTHS', 0), ('N_RUN_DAYS', 0), ('N_RUN_STEPS', steps)):
        text, count = re.subn(rf'^ {name} = .*$', f' {name} = {value}', text, flags=re.M)
        assert count == 1, name
    (folder / 'plasim_namelist').write_text(text)
    done = subprocess.run(['nice', '-n', '10', 'mpirun', '-np', str(DEFAULTS['ranks']), './' + executable.name],
                          cwd=folder, capture_output=True, text=True, timeout=900)
    assert done.returncode == 0 and 'MPI_ABORT' not in done.stdout + done.stderr, done.stderr[-2000:]
    assert not (folder / 'Abort_Message').exists() and (folder / 'plasim_status').is_file()
    return done


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


@needs_build
def test_patch_11_at_its_default_runs_byte_for_byte_as_the_build_without_it(deployed_point, tmp_path):
    """Earth's control with ice optics on, two days: the folder the adapter writes for the build of patches 01-10,
    without ZICEW, gives the same output under the build of the whole series, where patch 11 holds patch 10's
    constants; the weights the adapter writes for the whole series, from the Sun's spectrum, change it."""
    ten, ten_build = deployed_point
    ice = {**DEFAULTS, 'switches': {**DEFAULTS['switches'], 'ice_optics': True}}
    whole_build = builds.build(ice, store=STORE, env=ENV)
    executables = {name: build / 'exoplasim' / 'plasim' / 'run' / builds.executable_name(ice)
                   for name, build in (('ten', ten_build), ('whole', whole_build))}
    ex.write_run(tmp_path / 'ten', EARTH, CONTROL, {**ice, 'patches': ten['patches']},
                 calibrations=ex.Calibrations.identity(), store=STORE)
    shutil.copytree(tmp_path / 'ten', tmp_path / 'default')
    ex.write_run(tmp_path / 'spectrum', EARTH, CONTROL, ice, calibrations=ex.Calibrations.identity(), store=STORE)
    assert 'ZICEW' not in (tmp_path / 'ten' / 'radmod_namelist').read_text()
    # The two folders differ in the four ZICEW lines alone, so that a change of output comes from the ice optics.
    differ = {p.name for p in (tmp_path / 'ten').iterdir() if p.read_bytes() != (tmp_path / 'spectrum' / p.name).read_bytes()}
    assert differ == {'radmod_namelist'}
    lines = lambda name: (tmp_path / name / 'radmod_namelist').read_text().splitlines()
    assert [l for l in lines('spectrum') if 'ZICEW' not in l] == lines('ten')
    assert len([l for l in lines('spectrum') if 'ZICEW' in l]) == 4
    out = {}
    for name, executable in (('ten', executables['ten']), ('default', executables['whole']),
                             ('spectrum', executables['whole'])):
        _run_plasim(tmp_path / name, executable, 96)
        out[name] = {f: _sha256(tmp_path / name / f) for f in ('plasim_output', 'plasim_status')}
    assert out['default'] == out['ten']
    assert out['spectrum']['plasim_output'] != out['default']['plasim_output']
