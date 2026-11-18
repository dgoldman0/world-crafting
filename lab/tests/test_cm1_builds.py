"""CM1's builds (worldlab.cm1_builds): their keys, their refusals, the patched sources against the digest
models/check_patches.sh records, and the builds in the store, where it holds them."""
import io
import json
import shutil
import subprocess
import tarfile

import pytest

from worldlab import cm1_builds, derive
from worldlab.data import DataError
from worldlab.roots import root
from worldlab.spec import LAB, Library

LIB = Library()
STORE = root('store')
SETTINGS = dict(parallel='omp', optimization='-O3 -march=native', patches=['series-core', 'series-lab'])


def _inputs(**changes) -> dict:
    """A build's inputs as `cm1_builds.gather` gives them, made up, and `changes` on top."""
    made = dict(model='cm1', archive=dict(name='cm1r22.0.tar.gz', sha256='a' * 64), makefile='patches/makefile-gnu-omp.patch',
                series=['series-core', 'series-lab'], optimization_patches=[],
                patches=[dict(name='patches/core/01.patch', sha256='c' * 64), dict(name='patches/lab/01.patch',
                                                                                   sha256='d' * 64)],
                flags=dict(parallel='omp', optimization='-O2'), macros={},
                toolchain=dict(gfortran=dict(path='/usr/bin/gfortran', version='GNU Fortran 13.3.0')))
    return {**made, **changes}


def test_a_builds_key_follows_everything_that_makes_it():
    base = cm1_builds.key(_inputs())
    assert cm1_builds.key(_inputs()) == base and len(base) == 64
    for change in (dict(patches=_inputs()['patches'][::-1]), dict(patches=_inputs()['patches'][:1]),
                   dict(flags=dict(parallel='omp', optimization='-O3 -march=native')),
                   dict(macros=cm1_builds.world_macros(1.6242107, 4e-4, 0.1745785)),
                   dict(toolchain=dict(gfortran=dict(path='/usr/bin/gfortran', version='GNU Fortran 14.1.0'))),
                   dict(archive=dict(name='cm1r22.0.tar.gz', sha256='e' * 64))):
        assert cm1_builds.key(_inputs(**change)) != base, change
    assert cm1_builds.folder(LAB, base).name == f'cm1-{base[:16]}'


def test_a_build_takes_the_lab_series_with_openmp_and_compiles_all_three_world_macros_or_none():
    assert cm1_builds.world_macros(1.6242107, 4e-4, 0.1745785) == dict(
        TERLUNA_G='1.6242107', TERLUNA_CO2='0.0004', TERLUNA_O2='0.1745785')
    for bad in (dict(parallel='mpi'), dict(optimization='-Ofast'), dict(patches=['series-core']),
                dict(patches=['series-core', 'series-lab', 'series-twilight'])):
        with pytest.raises(DataError):
            cm1_builds.gather({**SETTINGS, **bad}, macros={})
    with pytest.raises(DataError, match='all of'):
        cm1_builds.gather(SETTINGS, macros=dict(TERLUNA_G='1.62'))


@pytest.mark.skipif(not cm1_builds.ARCHIVE.exists() or shutil.which('patch') is None,
                    reason='the pinned CM1 archive (upstream/) or patch is missing')
def test_the_inputs_name_the_series_patches_and_the_toolchain(tmp_path, monkeypatch):
    made, payload = cm1_builds.gather(SETTINGS, macros={})
    names = [p['name'] for p in made['patches']]
    assert names[0] == 'patches/makefile-gnu-omp.patch' and names[-1] == 'patches/makefile-omp-O3-march-native.patch'
    assert names[1:-1] == cm1_builds.series_names(SETTINGS['patches'])
    assert len(names) == 2 + len(cm1_builds.series_names(SETTINGS['patches']))
    assert set(cm1_builds.TOOLS) <= set(made['toolchain']) and made['toolchain']['native']['march']
    # The patched sources give the digest models/check_patches.sh records for the lab's series after the core.
    with tarfile.open(fileobj=io.BytesIO(payload['archive']), mode='r:gz') as tar:
        tar.extractall(tmp_path, members=[m for m in tar.getmembers() if m.name.startswith('cm1r22.0/src/')],
                       filter='data')
    for name, data in payload['patches'][:-1]:
        subprocess.run(['patch', '-p1', '--quiet'], input=data, cwd=tmp_path / 'cm1r22.0', check=True)
    assert cm1_builds.sources_digest(tmp_path / 'cm1r22.0' / 'src') == cm1_builds.expected_sources()['lab_omp']
    # The digest takes the locale the recorded digests were made under, whatever the caller's.
    monkeypatch.setenv('LC_ALL', 'C')
    monkeypatch.setenv('LANG', 'C')
    assert cm1_builds.sources_digest(tmp_path / 'cm1r22.0' / 'src') == cm1_builds.expected_sources()['lab_omp']


def _builds():
    if STORE is None or not (STORE / 'builds').is_dir():
        return []
    return sorted(p for p in (STORE / 'builds').glob('cm1-*') if (p / 'build.json').is_file())


@pytest.mark.skipif(not _builds(), reason="the lab's store holds no CM1 build")
def test_the_stores_builds_match_their_records_and_compile_the_recorded_sources():
    """Each CM1 build in the store holds the executable and run files its record names, compiled from the sources
    expected-series.sha256 records; a build of the Open Moon compiles the lab's derived gravity, CO2 and O2."""
    moon, air = LIB.world('moon'), derive.mole_fractions(LIB.scenario('moon/open-moon'))
    expected = cm1_builds.world_macros(derive.gravity(moon), air['CO2'], air['O2'])
    current = cm1_builds.gather(SETTINGS, macros={})[0]['patches']    # the series as it stands
    for folder in _builds():
        record = cm1_builds.record(cm1_builds.checked(folder))
        assert folder.name == f"cm1-{record['key'][:16]}" and record['key'] == cm1_builds.key(record['inputs'])
        assert record['sources']['digest'] == record['sources']['expected']            # as its record holds them
        if record['inputs']['patches'] == current:     # a build of an earlier series keeps that series' digest
            assert record['sources']['expected'] == cm1_builds.expected_sources()['lab_omp']
        assert record['inputs']['macros'] in ({}, expected)
        assert not any(p.stat().st_mode & 0o222 for p in folder.iterdir())                 # read-only
