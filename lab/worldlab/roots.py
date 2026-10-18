"""The folders outside Git that the lab reads: Terluna's repository and research drive, which the reproduction
tests compare with and the `terluna:` and `terluna-drive:` pins name, and the lab's own store.

Each root comes from its environment variable, or from lab/local.toml ([roots], kept out of Git; see
lab/local.example.toml), a relative path there taken from lab/. A root counts only as a folder that holds
something, so that an unmounted drive's empty mount point reads as absent. A test that needs a root it lacks
reports itself skipped.
"""
from __future__ import annotations

import os
import tomllib
import warnings
from pathlib import Path

from .spec import LAB

VARIABLES = {'terluna': 'TERLUNA_REPO', 'terluna-drive': 'TERLUNA_DRIVE', 'store': 'WORLDLAB_STORE'}


def root(name: str, lab: Path = LAB) -> Path | None:
    """The root's folder, or None where neither its variable nor lab/local.toml names one that holds anything."""
    value = os.environ.get(VARIABLES[name]) or _local(lab).get(name)
    if not value:
        return None
    path = Path(value) if Path(value).is_absolute() else lab / value
    return path if path.is_dir() and any(path.iterdir()) else None


def _local(lab: Path) -> dict:
    local = lab / 'local.toml'
    if not local.exists():
        return {}
    try:
        return tomllib.loads(local.read_text()).get('roots', {})
    except tomllib.TOMLDecodeError as error:
        warnings.warn(f'{local}: {error}; its roots are ignored')
        return {}
