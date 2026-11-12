"""Shared by the tests of PlaSim's surface transfer (test_surface_gust.py, test_surface_similarity.py), of CM1's rain
(test_cm1_rain.py) and of CM1's world from the namelist (test_cm1_world.py): the lab's patch series applied to the
pinned ExoPlaSim and CM1 archives, once each in a session. The lab's own file: Terluna's tests took the Fortran from
its runner's edit lists."""
from __future__ import annotations

import hashlib
import io
import re
import shutil
import subprocess
import tarfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
ARCHIVE = REPO / 'upstream' / 'exoplasim-3.4.2.tar.gz'
PINS = REPO / 'models' / 'pins.sha256'
PATCHES = REPO / 'models' / 'exoplasim' / 'patches'
SOURCES = 'exoplasim-3.4.2/exoplasim/plasim/src/'
CM1_ARCHIVE = REPO / 'upstream' / 'cm1r22.0.tar.gz'
CM1 = REPO / 'models' / 'cm1'
CM1_SOURCES = 'cm1r22.0/src/'
# The files the tests of CM1 read at the points of the series: the rain's five, and those through which the world's
# gravity, air, soil and Sun reach the model.
CM1_KEPT = ('cm1.F', 'constants.F', 'input.F', 'morrison.F', 'param.F', 'getcape.F', 'init_physics.F', 'init_surface.F',
            'module_ra_etc.F', 'module_ra_rrtmg_lw.F', 'module_ra_rrtmg_sw.F', 'radiation_driver.F')
CM1_DATA = ('RRTMG_LW_DATA', 'RRTMG_SW_DATA')            # RRTMG's tables, which a column of it reads as it starts


class Series:
    """A model's sources at each point of a patch series, and each patch's own lines."""

    def __init__(self, names: list, texts: dict, folder: Path = PATCHES, encoding: str | None = None,
                 tree: dict | None = None, data: dict | None = None):
        self.names, self._texts, self.folder, self.encoding = names, texts, folder, encoding
        self.tree, self.data = tree or {}, data or {}     # every source file at the series' end; the run's data files

    def source(self, name: str, through: str | None) -> str:
        """A source file's text with the series applied through the patch `through`; None gives the archive's own."""
        return self._texts[through][name]

    def before(self, patch: str) -> str | None:
        """The patch before `patch` in the series; None before the first."""
        place = self.names.index(patch)
        return self.names[place - 1] if place else None

    def added(self, patch: str) -> list:
        """The lines `patch` adds to the sources."""
        return [line[1:] for line in (self.folder / patch).read_text(encoding=self.encoding).splitlines()
                if line.startswith('+') and not line.startswith('+++')]


def _pinned(archive: Path) -> bytes:
    """An archive's bytes, checked against its pin: the bytes checked are the bytes used."""
    data = archive.read_bytes()
    pins = dict(line.split()[::-1] for line in PINS.read_text().splitlines() if line.strip() and not line.startswith('#'))
    assert hashlib.sha256(data).hexdigest() == pins[archive.name], f'{archive} differs from its pin'
    return data


@pytest.fixture(scope='session')
def series_sources(tmp_path_factory) -> Series:
    """The lab's patch series on the pinned ExoPlaSim archive. The files the series patches, with plasimmod.f90, leave
    the archive once in a session, about 0.3 MB, and each point's text is kept in memory. A test that takes the
    fixture is skipped where the archive or patch is missing."""
    if not ARCHIVE.exists() or shutil.which('patch') is None:
        pytest.skip('the pinned ExoPlaSim archive (upstream/) or patch is missing')
    archive = _pinned(ARCHIVE)
    names = [line.strip() for line in (PATCHES / 'series').read_text().splitlines() if line.strip()]
    patched = {name for patch in names
               for name in re.findall(r'^\+\+\+ b/plasim/src/(\S+)', (PATCHES / patch).read_text(), flags=re.M)}
    root = tmp_path_factory.mktemp('plasim')
    src = root / 'plasim' / 'src'
    src.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
        for name in sorted(patched | {'plasimmod.f90'}):
            (src / name).write_bytes(tar.extractfile(SOURCES + name).read())
    texts = {None: {p.name: p.read_text(encoding='latin-1') for p in src.iterdir()}}
    for patch in names:
        subprocess.run(['patch', '-p1', '--quiet', '--no-backup-if-mismatch'], input=(PATCHES / patch).read_bytes(),
                       cwd=root, check=True, capture_output=True)
        texts[patch] = {p.name: p.read_text(encoding='latin-1') for p in src.iterdir()}
    return Series(names, texts)


@pytest.fixture(scope='session')
def cm1_series(tmp_path_factory) -> Series:
    """The core series and the lab's on the pinned CM1 archive: the texts of CM1_KEPT as released, after the core
    series and after each of the lab's patches, the patches named as the series files name them (patches/lab/03-...);
    every source file of the model at the series' end (`tree`); and RRTMG's two tables (`data`). The twenty-one files
    the two series patch leave the archive once in a session, about 4 MB, and the kept texts, the tree and the tables
    stay in memory, about 34 MB. A test that takes the fixture is skipped where the archive or patch is missing."""
    if not CM1_ARCHIVE.exists() or shutil.which('patch') is None:
        pytest.skip('the pinned cm1r22.0 archive (upstream/) or patch is missing')
    archive = _pinned(CM1_ARCHIVE)
    core, lab = ([line.strip() for line in (CM1 / series).read_text().splitlines() if line.strip()]
                 for series in ('series-core', 'series-lab'))
    names = core + lab
    patched = {name for patch in names
               for name in re.findall(r'^\+\+\+ b/src/(\S+)', (CM1 / patch).read_text(encoding='latin-1'), flags=re.M)}
    root = tmp_path_factory.mktemp('cm1')
    src = root / 'src'
    src.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
        for name in sorted(patched):
            (src / name).write_bytes(tar.extractfile(CM1_SOURCES + name).read())
        tree = {member.name[len(CM1_SOURCES):]: tar.extractfile(member).read().decode('latin-1') for member in tar
                if member.name.startswith(CM1_SOURCES) and member.name.endswith('.F')}
        data = {name: tar.extractfile(f'cm1r22.0/run/{name}').read() for name in CM1_DATA}
    kept = lambda: {name: (src / name).read_text(encoding='latin-1') for name in CM1_KEPT}
    texts = {None: kept()}
    for patch in names:
        subprocess.run(['patch', '-p1', '--quiet', '--no-backup-if-mismatch'], input=(CM1 / patch).read_bytes(),
                       cwd=root, check=True, capture_output=True)
        if patch == core[-1] or patch in lab:
            texts[patch] = kept()
    tree.update({name: (src / name).read_text(encoding='latin-1') for name in patched if name.endswith('.F')})
    return Series(names, texts, CM1, 'latin-1', tree, data)
