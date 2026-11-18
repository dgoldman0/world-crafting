"""Keys, headers and the store's small records: the thin path of plan stage 4 (lab/design/architecture.md, "The stage
graph and staleness" and "Storage and records").

A product's key is the sha256 of the canonical form of what makes it: its producer, the hashes of the modules that
compute it; its upstream products' keys; the digests of the outside files it reads; its read set, the values it
takes from the world, the scenario and its settings, by name; and the environment's class. Its header records those
with the key, the product's schema, its evidence statement and the checks it passed. The thin path declares each
stage's read set by hand, in the producer that writes it, where the full stage 4 tracks reads through a view of the
specifications; staleness across the stage graph waits for that stage.

The store keeps a cache of file digests, by path, size and modification time, so that a key over large inputs, such
as a GCM run's year files, is computed once; and an index of human names, `index/<study>/<item>`, a link to the
product's folder. Every write here lands whole: through a temporary file or link moved into place.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import platform
import sys
import tempfile
from pathlib import Path

from .spec import LAB, canonical

DIGESTS = 'caches/digests.json'
_CHUNK = 1 << 22


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')


def key(inputs: dict) -> str:
    """A product's key: the sha256 of its inputs' canonical form."""
    return hashlib.sha256(canonical(inputs).encode()).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(_CHUNK), b''):
            h.update(chunk)
    return h.hexdigest()


def digests(paths, store: Path | None) -> dict[str, str]:
    """Each file's sha256, by its path as given, from the store's cache where the file's size and modification time
    are those cached, and computed and cached otherwise."""
    paths = [Path(p) for p in paths]
    cache_path = Path(store) / DIGESTS if store is not None else None
    cache = {}
    if cache_path is not None and cache_path.is_file():
        try:
            cache = json.loads(cache_path.read_text())
        except (OSError, ValueError):
            cache = {}
    out, changed = {}, False
    for p in paths:
        st = p.stat()
        mark = [st.st_size, st.st_mtime_ns]
        found = cache.get(str(p.resolve()))
        if found and found[:2] == mark:
            out[str(p)] = found[2]
            continue
        digest = sha256_file(p)
        cache[str(p.resolve())] = mark + [digest]
        out[str(p)] = digest
        changed = True
    if changed and cache_path is not None:
        write_json(cache_path, cache, indent=None)
    return out


def producer(paths) -> dict[str, str]:
    """A producer's identity: the sha256 of each of its modules, by its path within the repository."""
    root = LAB.parent
    return {str(Path(p).resolve().relative_to(root)): sha256_file(Path(p)) for p in sorted(paths)}


def environment_class() -> dict:
    """The environment's class, which enters a key: Python's and numpy's and scipy's major and minor versions. The full
    versions are recorded beside it."""
    import numpy
    import scipy
    minor = lambda v: '.'.join(v.split('.')[:2])
    return dict(python=f'{sys.version_info.major}.{sys.version_info.minor}', numpy=minor(numpy.__version__),
                scipy=minor(scipy.__version__))


def environment_full() -> dict:
    import numpy
    import scipy
    return dict(python=platform.python_version(), numpy=numpy.__version__, scipy=scipy.__version__,
                machine=platform.node())


def header(schema: str, key_: str, *, producer_: dict, inputs: dict, read_set: dict, evidence: str, **extra) -> dict:
    """A product's header (architecture.md, Principles, "A header on every product")."""
    return dict(schema=schema, key=key_, producer=producer_, inputs=inputs, read_set=read_set, evidence=evidence,
                environment=environment_full(), made=now(), **extra)


def write_json(path: Path, obj, *, indent: int | None = 1) -> None:
    """A JSON file written whole: through a temporary file in its folder, moved into place."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f'.{path.name}.', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(json.dumps(obj, indent=indent, sort_keys=True, allow_nan=False) + '\n')
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def read_json(path: Path):
    return json.loads(Path(path).read_text())


def name_link(store: Path, study: str, item: str, target: Path) -> Path:
    """The index's link `index/<study>/<item>` to a product's folder, replaced whole where it names an earlier key."""
    link = Path(store) / 'index' / study / item
    link.parent.mkdir(parents=True, exist_ok=True)
    relative = os.path.relpath(target, link.parent)
    if link.is_symlink() and os.readlink(link) == relative:
        return link
    tmp = link.parent / f'.{item}.{os.getpid()}.link'
    tmp.unlink(missing_ok=True)
    os.symlink(relative, tmp)
    os.replace(tmp, link)
    return link


def named(store: Path, study: str, item: str) -> Path | None:
    """The folder the index names for a study's item, or None."""
    link = Path(store) / 'index' / study / item
    return link.resolve() if link.is_symlink() and link.resolve().is_dir() else None
