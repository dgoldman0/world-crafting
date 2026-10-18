"""External data: the pins that name it, the manifest that records it, and the store that holds the lab's copies.

A pin (lab/design/world_spec.md, rule 4) is a plain name, such as `tsis1-hsrs-stride100`, for data from outside
Terluna, or `terluna:<path>` or `terluna-drive:<path>` for a file in Terluna's repository or on its research
drive. `#<entry>` selects an entry in the file, and `@<digest>` gives the first 16 hex digits of its sha256.

The lab's own stages read data through the manifest, lab/data/manifest.toml. Each entry there lists its files,
each with its size, sha256, one source (a URL to download, or a Terluna pin to copy) and the date the lab took
its bytes, beside the entry's licence and credit; the lab's copy of each file sits in the store as
data/<digest>/<name>, read-only. Nothing is substituted: a file missing, or of another size or hash than its
record, raises DataError, and a fetch keeps only bytes that match.

    PYTHONPATH=lab python -m worldlab.data                       # each file's state in the store
    PYTHONPATH=lab python -m worldlab.data --fetch               # copy what Terluna's roots hold
    PYTHONPATH=lab python -m worldlab.data --fetch --download    # and download the rest from their sources
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import http.client
import os
import re
import sys
import tempfile
import tomllib
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .roots import VARIABLES, root
from .spec import LAB, get_path

MANIFEST = LAB / 'data' / 'manifest.toml'
SCHEMA = 'worldlab.manifest/0'
ROOTS = ('terluna', 'terluna-drive')
# The fields of a world and of a scenario that hold a pin, or one of the words that name no pin.
PIN_FIELDS = {'world': ('star.spectrum', 'surface.geometry'), 'scenario': ('sunlight.filter', 'water.lakes_start')}
WORDS = frozenset({'none', 'model-default', 'unchosen'})
ENTRY_KEYS = frozenset({'title', 'use', 'licence', 'credit', 'reviewed', 'files', 'note'})
REQUIRED_ENTRY_KEYS = ENTRY_KEYS - {'note'}
FILE_KEYS = frozenset({'name', 'bytes', 'sha256', 'retrieved', 'url', 'source', 'commit', 'made', 'note'})
REQUIRED_FILE_KEYS = frozenset({'name', 'bytes', 'sha256', 'retrieved'})
URL_SCHEMES = ('https://', 'file://')         # file:// serves the tests
USER_AGENT = 'world-crafting-lab/0 (data manifest)'
_NAME = re.compile(r'[a-z0-9][a-z0-9._-]*')
_PART = re.compile(r'[A-Za-z0-9._+-]+')
_DIGEST = re.compile(r'[0-9a-f]{16}')
_SHA256 = re.compile(r'[0-9a-f]{64}')
_COMMIT = re.compile(r'[0-9a-f]{40}')
_CHUNK = 1 << 20


class DataError(ValueError):
    """Data the lab cannot use as recorded: a pin it cannot resolve, or a file missing or changed."""


# Pins.

@dataclass(frozen=True)
class Pin:
    root: str | None            # 'terluna' or 'terluna-drive'; None for a plain name
    path: str                   # the file's path under its root, or the plain name
    entry: str | None = None
    digest: str | None = None

    @property
    def name(self) -> str:
        """The pin without its entry and digest, as the manifest keys it."""
        return f'{self.root}:{self.path}' if self.root else self.path


def parse_pin(text) -> Pin:
    """A pin's parts; DataError for a pin that names no file unambiguously."""
    if isinstance(text, Pin):
        return text
    if not isinstance(text, str) or not text:
        raise DataError(f'{text!r}: a pin is a non-empty string')
    rest, digest, entry, base = text, None, None, None
    if '@' in rest:
        rest, digest = rest.rsplit('@', 1)
        if not _DIGEST.fullmatch(digest):
            raise DataError(f"{text!r}: @ takes the first 16 hex digits of the file's sha256")
    if '#' in rest:
        rest, entry = rest.split('#', 1)
        if not entry:
            raise DataError(f'{text!r}: # names an entry in the file')
    if ':' in rest:
        base, rest = rest.split(':', 1)
        if base not in ROOTS:
            raise DataError(f"{text!r}: a pin's root is one of {', '.join(ROOTS)}")
        if any(part in ('.', '..') or not _PART.fullmatch(part) for part in rest.split('/')):
            raise DataError(f'{text!r}: a path relative to its root, its parts of letters, digits, ".", "_", "+" '
                            'and "-", other than . and ..')
    elif not _NAME.fullmatch(rest):
        raise DataError(f'{text!r}: a plain name takes lowercase letters, digits, ".", "_" and "-"')
    return Pin(base, rest, entry, digest)


def spec_pins(kind: str, tree: dict) -> dict[str, Pin]:
    """The pins a resolved world or scenario holds (`kind` 'world' or 'scenario'), by field, leaving out the fields
    it lacks and the words that name no pin."""
    found = {}
    for field in PIN_FIELDS[kind]:
        try:
            value = get_path(tree, field)
        except KeyError:
            continue
        if not isinstance(value, str):
            raise DataError(f'{field}: a pin or one of {sorted(WORDS)}, where the {kind} holds {value!r}')
        if value not in WORDS:
            found[field] = parse_pin(value)
    return found


# The manifest.

@dataclass(frozen=True)
class File:
    entry: str
    name: str
    bytes: int
    sha256: str
    retrieved: datetime.date
    url: str | None = None
    source: Pin | None = None
    commit: str | None = None
    made: str | None = None
    note: str | None = None

    @property
    def digest(self) -> str:
        return self.sha256[:16]

    def in_store(self, store: Path) -> Path:
        return Path(store) / 'data' / self.digest / self.name


class Manifest:
    """The manifest's entries by name: each a dict of its fields, with `files` a tuple of File records."""

    def __init__(self, path: Path = MANIFEST):
        self.toml = Path(path)
        self.entries = _load(self.toml)

    def entry(self, pin) -> dict:
        pin = parse_pin(pin)
        if pin.name not in self.entries:
            raise DataError(f'{pin.name!r} has no entry in {self.toml}')
        return self.entries[pin.name]

    def files(self, pin) -> tuple[File, ...]:
        """The pin's files: every file of its entry, or the one whose digest the pin gives."""
        pin = parse_pin(pin)
        files = self.entry(pin)['files']
        if pin.digest is None:
            return files
        chosen = tuple(f for f in files if f.digest == pin.digest)
        if not chosen:
            raise DataError(f'{pin.name!r} holds no file of digest {pin.digest}')
        return chosen

    def paths(self, pin, *, store: Path | None = None, lab: Path = LAB) -> dict[str, Path]:
        """Each of the pin's files in the store, by name, after its size and sha256 are checked."""
        store = _store(store, lab)
        return {f.name: checked(f.in_store(store), f) for f in self.files(pin)}

    def path(self, pin, *, store: Path | None = None, lab: Path = LAB) -> Path:
        """The pin's one file in the store, checked; a pin of several files names one by its digest."""
        paths = self.paths(pin, store=store, lab=lab)
        if len(paths) != 1:
            raise DataError(f'{parse_pin(pin).name!r} holds {len(paths)} files: {", ".join(paths)}')
        return next(iter(paths.values()))

    def status(self, names=None, *, store: Path | None = None, lab: Path = LAB) -> dict[str, list[str]]:
        """Each file's state in the store: present (and matching its record), missing or changed."""
        store = _store(store, lab, allow_empty=True)
        report = {'present': [], 'missing': [], 'changed': []}
        for f in self._chosen(names):
            report[_state(f.in_store(store), f)].append(f.name)
        return report

    def fetch(self, names=None, *, store: Path | None = None, download: bool = False, lab: Path = LAB) -> dict:
        """Put the files of the named entries or pins, or of every entry, into the store. A file already there is
        checked, and a changed one is reported and left for review; a missing one is copied from its source pin's
        root or, with `download`, fetched from its URL, and kept only where its size and sha256 match the record."""
        store = _store(store, lab, allow_empty=True)
        report = {'present': [], 'copied': [], 'downloaded': [], 'missing': [], 'changed': []}
        for f in self._chosen(names):
            target = f.in_store(store)
            state = _state(target, f)
            if state != 'missing':
                report[state].append(f.name)
            elif f.source is not None:
                base = root(f.source.root, lab)
                origin = base / f.source.path if base is not None else None
                if origin is None or not origin.is_file():
                    report['missing'].append(f.name)
                    continue
                _store_checked(_file_chunks(origin), target, f, str(origin))
                report['copied'].append(f.name)
            elif download:
                _store_checked(_url_chunks(f.url), target, f, f.url)
                report['downloaded'].append(f.name)
            else:
                report['missing'].append(f.name)
        return report

    def _chosen(self, names) -> list[File]:
        return [f for name in (names or self.entries) for f in self.files(name)]


# Files and their checks.

def checked(path: Path, f: File) -> Path:
    """`path`, once its size and sha256 match the record `f`."""
    try:
        size = path.stat().st_size
    except FileNotFoundError:
        raise DataError(f'{f.name} ({f.entry}) is missing from the store, at {path}; fetch it with '
                        '`python -m worldlab.data --fetch`') from None
    if size != f.bytes or _digest_of(path) != f.sha256:
        raise DataError(f"{path}: its bytes differ from the manifest's record of {f.name} ({f.entry}); after review, "
                        'remove it for a fresh fetch')
    return path


def _state(path: Path, f: File) -> str:
    if not path.is_file():
        return 'missing'
    return 'present' if path.stat().st_size == f.bytes and _digest_of(path) == f.sha256 else 'changed'


def _digest_of(path: Path) -> str:
    """A file's sha256, read afresh each time: a file rewritten within one tick of the clock keeps its time stamp."""
    digest = hashlib.sha256()
    for chunk in _file_chunks(path):
        digest.update(chunk)
    return digest.hexdigest()


def _file_chunks(path: Path):
    with open(path, 'rb') as handle:
        while chunk := handle.read(_CHUNK):
            yield chunk


def _url_chunks(url: str):
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(request, timeout=300) as response:
        try:
            while chunk := response.read(_CHUNK):
                yield chunk
        except http.client.IncompleteRead as error:
            # Some servers close abruptly after the last byte; the size and hash checks then show whether the
            # transfer is whole.
            yield error.partial


def _store_checked(chunks, target: Path, f: File, origin: str) -> None:
    """Write `chunks` to `target` through a temporary file beside it, kept only where its size and sha256 match `f`,
    and synced to disk before it takes the target's name."""
    made = not target.parent.exists()
    target.parent.mkdir(parents=True, exist_ok=True)
    digest, size = hashlib.sha256(), 0
    handle = tempfile.NamedTemporaryFile(dir=target.parent, prefix='.partial-', delete=False)
    try:
        with handle:
            for chunk in chunks:
                size += len(chunk)
                if size > f.bytes:
                    break
                digest.update(chunk)
                handle.write(chunk)
            handle.flush()
            os.fsync(handle.fileno())
        if size != f.bytes or digest.hexdigest() != f.sha256:
            got = f'more than {f.bytes} bytes' if size > f.bytes else f'{size} bytes of sha256 {digest.hexdigest()[:16]}'
            raise DataError(f'{origin}: {got}, where the manifest records {f.bytes} bytes of {f.digest} for {f.name}. '
                            'A short transfer or a changed source gives this; new bytes need review before use')
        os.chmod(handle.name, 0o444)
        os.replace(handle.name, target)
    except BaseException:
        Path(handle.name).unlink(missing_ok=True)
        if made:
            try:
                target.parent.rmdir()
            except OSError:
                pass
        raise


def _store(store: Path | None, lab: Path = LAB, *, allow_empty: bool = False) -> Path:
    if store is not None:
        return Path(store)
    found = root('store', lab, allow_empty=allow_empty)
    if found is None:
        raise DataError(f"the store is unset, or holds nothing: set ${VARIABLES['store']} or lab/local.toml's "
                        '[roots] store (lab/local.example.toml)')
    return found


def _load(path: Path) -> dict:
    """The manifest's entries, each checked for its fields, its files' records and one source for each file."""
    try:
        raw = tomllib.loads(path.read_text(encoding='utf-8'))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise DataError(f'{path}: {error}') from None
    if raw.get('schema') != SCHEMA:
        raise DataError(f"{path}: schema {raw.get('schema')!r}, where the lab reads {SCHEMA!r}")
    if set(raw) - {'schema', 'data'}:
        raise DataError(f"{path}: unknown keys {sorted(set(raw) - {'schema', 'data'})}")
    entries, digests = {}, {}
    for name, entry in raw.get('data', {}).items():
        where = f'{path.name}, {name!r}'
        pin = parse_pin(name)
        if pin.entry is not None or pin.digest is not None:
            raise DataError(f'{where}: an entry is named by a pin without # or @')
        if not isinstance(entry, dict) or set(entry) - ENTRY_KEYS or REQUIRED_ENTRY_KEYS - set(entry):
            raise DataError(f'{where}: an entry holds {sorted(REQUIRED_ENTRY_KEYS)}, and may hold a note')
        for key in REQUIRED_ENTRY_KEYS - {'files', 'reviewed'}:
            if not isinstance(entry[key], str) or not entry[key].strip():
                raise DataError(f'{where}: {key} is a non-empty string')
        if type(entry['reviewed']) is not datetime.date:
            raise DataError(f'{where}: reviewed is the date of its licence review')
        if not isinstance(entry['files'], list) or not entry['files']:
            raise DataError(f'{where}: files lists one file or more')
        files = []
        for item in entry['files']:
            record = _file(item, name, where)
            if record.digest in digests:
                raise DataError(f'{where}: {record.name} shares its digest with {digests[record.digest]}')
            if any(f.name == record.name for f in files):
                raise DataError(f'{where}: two files named {record.name}; a new version takes an entry of its own')
            digests[record.digest] = record.name
            files.append(record)
        entries[name] = {**entry, 'files': tuple(files)}
    return entries


def _file(item, entry: str, where: str) -> File:
    if not isinstance(item, dict) or set(item) - FILE_KEYS or REQUIRED_FILE_KEYS - set(item):
        raise DataError(f'{where}: a file holds {sorted(REQUIRED_FILE_KEYS)} and a url or source, and may hold '
                        f'{sorted(FILE_KEYS - REQUIRED_FILE_KEYS - {"url", "source"})}')
    name, size, sha = item['name'], item['bytes'], item['sha256']
    if not isinstance(name, str) or name in ('.', '..') or not _PART.fullmatch(name):
        raise DataError(f'{where}: {name!r} is a plain file name')
    if type(size) is not int or size <= 0:
        raise DataError(f'{where}, {name}: bytes is a positive integer')
    if not isinstance(sha, str) or not _SHA256.fullmatch(sha):
        raise DataError(f'{where}, {name}: sha256 is 64 lowercase hex digits')
    if type(item['retrieved']) is not datetime.date:
        raise DataError(f'{where}, {name}: retrieved is the date the lab took the bytes')
    if ('url' in item) == ('source' in item):
        raise DataError(f'{where}, {name}: a file has one source, a url or a Terluna pin')
    if 'url' in item and not (isinstance(item['url'], str) and item['url'].startswith(URL_SCHEMES)):
        raise DataError(f'{where}, {name}: a url starts with one of {URL_SCHEMES}')
    source = parse_pin(item['source']) if 'source' in item else None
    if source is not None and (source.root is None or source.entry is not None or source.digest is not None):
        raise DataError(f"{where}, {name}: a source pin names a file under one of Terluna's roots, without # or @")
    if 'commit' in item and not (isinstance(item['commit'], str) and _COMMIT.fullmatch(item['commit'])):
        raise DataError(f'{where}, {name}: commit is a full Git commit hash')
    for key in ('made', 'note'):
        if key in item and not (isinstance(item[key], str) and item[key].strip()):
            raise DataError(f'{where}, {name}: {key} is a non-empty string')
    return File(entry, name, size, sha, item['retrieved'], item.get('url'), source, item.get('commit'),
                item.get('made'), item.get('note'))


def main(argv=None, *, manifest: Manifest | None = None, store: Path | None = None, lab: Path = LAB) -> int:
    parser = argparse.ArgumentParser(description="The data the lab's stages read: each file's state in the store.")
    parser.add_argument('names', nargs='*', help='entries or pins of the manifest (all by default)')
    parser.add_argument('--fetch', action='store_true', help="copy missing files from Terluna's roots into the store")
    parser.add_argument('--download', action='store_true', help='with --fetch, download missing files from their URLs')
    args = parser.parse_args(argv)
    if args.download and not args.fetch:
        parser.error('--download goes with --fetch')
    try:
        manifest = manifest or Manifest()
        report = (manifest.fetch(args.names, store=store, download=args.download, lab=lab) if args.fetch
                  else manifest.status(args.names, store=store, lab=lab))
    except (DataError, OSError) as error:
        print(f'refused: {error}', file=sys.stderr)
        return 1
    for state, names in report.items():
        for name in names:
            print(f'{state}: {name}')
    return 0 if not report['missing'] and not report['changed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
