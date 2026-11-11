"""Shared by the tests of PlaSim's surface transfer (test_surface_gust.py, test_surface_similarity.py): the lab's patch
series applied to the pinned ExoPlaSim archive, once in a session. The lab's own file: Terluna's tests took the Fortran
from its runner's edit lists."""
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


class Series:
    """PlaSim's sources at each point of the lab's patch series, and each patch's own lines."""

    def __init__(self, names: list, texts: dict):
        self.names, self._texts = names, texts

    def source(self, name: str, through: str | None) -> str:
        """A source file's text with the series applied through the patch `through`; None gives the archive's own."""
        return self._texts[through][name]

    def before(self, patch: str) -> str | None:
        """The patch before `patch` in the series; None before the first."""
        place = self.names.index(patch)
        return self.names[place - 1] if place else None

    def added(self, patch: str) -> list:
        """The lines `patch` adds to the sources."""
        return [line[1:] for line in (PATCHES / patch).read_text().splitlines()
                if line.startswith('+') and not line.startswith('+++')]


@pytest.fixture(scope='session')
def series_sources(tmp_path_factory) -> Series:
    """The lab's patch series on the pinned ExoPlaSim archive. The files the series patches, with plasimmod.f90, leave
    the archive once in a session, about 0.3 MB, and each point's text is kept in memory. A test that takes the
    fixture is skipped where the archive or patch is missing."""
    if not ARCHIVE.exists() or shutil.which('patch') is None:
        pytest.skip('the pinned ExoPlaSim archive (upstream/) or patch is missing')
    archive = ARCHIVE.read_bytes()                     # read once: the bytes checked against the pin are the bytes used
    pins = dict(line.split()[::-1] for line in PINS.read_text().splitlines() if line.strip() and not line.startswith('#'))
    assert hashlib.sha256(archive).hexdigest() == pins[ARCHIVE.name], f'{ARCHIVE} differs from its pin'
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
