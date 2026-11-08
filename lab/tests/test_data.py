"""The data manifest: pins, the manifest's records and the store's copies."""
import datetime
import hashlib
import json
import stat
import tomllib

import pytest

from worldlab import data
from worldlab.data import DataError, Manifest, Pin, parse_pin
from worldlab.roots import root
from worldlab.spec import LAB, Library

LIB = Library()
MANIFEST = Manifest()
STORE, TERLUNA = root('store'), root('terluna')
needs_store = pytest.mark.skipif(STORE is None, reason='the store is unset (lab/local.example.toml)')
needs_repo = pytest.mark.skipif(TERLUNA is None, reason="Terluna's repository is unset (lab/local.example.toml)")
SEEDS = [p for p in LAB.glob('*/**/*.toml') if p.parts[len(LAB.parts)] in ('worlds', 'configs', 'studies', 'registry')]


class Raw(str):
    """A value written into a test's manifest as TOML source, unquoted."""


def _strings(tree, prefix=''):
    """Every string in a parsed TOML tree, with its dotted path."""
    if isinstance(tree, dict):
        for key, value in tree.items():
            yield from _strings(value, f'{prefix}{key}.')
    elif isinstance(tree, list):
        for value in tree:
            yield from _strings(value, prefix)
    elif isinstance(tree, str):
        yield prefix[:-1], tree


def _seed_pins():
    worlds = sorted(p.parent.name for p in (LAB / 'worlds').glob('*/world.toml'))
    scenarios = sorted(f'{p.parent.parent.name}/{p.stem}' for p in (LAB / 'worlds').glob('*/scenarios/*.toml'))
    pins = [p for w in worlds for p in data.spec_pins('world', LIB.world(w)).values()]
    return pins + [p for s in scenarios for p in data.spec_pins('scenario', LIB.scenario(s)).values()]


def _toml(value) -> str:
    return value if isinstance(value, Raw) else json.dumps(value)


def _manifest(tmp_path, files, *, top='schema = "worldlab.manifest/0"', name='x', **entry):
    """A manifest of one entry, written beside a test's store; an entry field given as None is left out, and each
    file takes the date 2026-10-18 unless it states its own."""
    fields = {k: v for k, v in {**dict(title='t', use='u', licence='l', credit='c', reviewed=Raw('2026-10-18')),
                                **entry}.items() if v is not None}
    lines = [top, f'[data.{json.dumps(name)}]', *(f'{k} = {_toml(v)}' for k, v in fields.items())]
    for f in files:
        f = {k: v for k, v in {'retrieved': Raw('2026-10-18'), **f}.items() if v is not None}
        lines += [f'[[data.{json.dumps(name)}.files]]', *(f'{k} = {_toml(v)}' for k, v in f.items())]
    path = tmp_path / 'manifest.toml'
    path.write_text('\n'.join(lines) + '\n')
    return path


def _record(name, content: bytes, **fields):
    return dict(name=name, bytes=len(content), sha256=hashlib.sha256(content).hexdigest(), **fields)


def _digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()[:16]


@pytest.fixture
def terluna(tmp_path, monkeypatch):
    """A Terluna repository of a test's own, and an empty store beside it."""
    (tmp_path / 'terluna').mkdir()
    (tmp_path / 'store').mkdir()
    monkeypatch.setenv('TERLUNA_REPO', str(tmp_path / 'terluna'))
    return tmp_path / 'terluna', tmp_path / 'store'


# Pins.

def test_a_pin_names_its_root_path_entry_and_digest():
    assert parse_pin('tsis1-hsrs-stride100') == Pin(None, 'tsis1-hsrs-stride100')
    pin = parse_pin('terluna:protection/spectra/shield_transmission.json#titania_stack')
    assert (pin.root, pin.path, pin.entry, pin.digest) == (
        'terluna', 'protection/spectra/shield_transmission.json', 'titania_stack', None)
    assert pin.name == 'terluna:protection/spectra/shield_transmission.json'
    pin = parse_pin('terluna-drive:gcm-runs/A28_corrected_9685/model/MOST_REST.00019@d65b88aa68443890')
    assert (pin.root, pin.path, pin.digest) == ('terluna-drive', 'gcm-runs/A28_corrected_9685/model/MOST_REST.00019',
                                                'd65b88aa68443890')
    assert parse_pin('x.json#a@0123456789abcdef') == Pin(None, 'x.json', 'a', '0123456789abcdef')


@pytest.mark.parametrize('text', ['', 42, 'TSIS', 'nasa:x', 'terluna:', 'terluna:/etc/x', 'terluna:a/../b',
                                  'terluna:a//b', 'terluna: a.json', 'terluna:a\x00b', 'terluna:a b/c', 'x@0123',
                                  'x@0123456789ABCDEF', 'x#', 'x#@0123456789abcdef'])
def test_ill_formed_pins_are_refused(text):
    with pytest.raises(DataError):
        parse_pin(text)


def test_a_pin_field_holding_a_table_is_refused():
    with pytest.raises(DataError, match='a pin or one of'):
        data.spec_pins('scenario', {'sunlight': {'filter': {'file': 'x'}}})
    assert data.spec_pins('scenario', {'sunlight': {'filter': 'none'}}) == {}


# The manifest's records.

def test_every_entry_records_its_licence_credit_and_one_source_for_each_file():
    for entry in MANIFEST.entries.values():
        assert entry['licence'] and entry['credit'] and isinstance(entry['reviewed'], datetime.date)
        for f in entry['files']:
            assert (f.url is None) != (f.source is None) and isinstance(f.retrieved, datetime.date)
            assert f.url is None or f.url.startswith('https://')


def test_the_manifest_holds_the_seeds_pins_and_the_data_a_stages_tool_names_alone():
    """Every entry is a pin the seeds name or the data a stage's tool names by its entry, stage 9's water lines."""
    from atmosphere.waterworlds import hitemp
    seeds = {p.name for p in _seed_pins()}
    assert seeds == {'tsis1-hsrs-stride100', 'lola-ldem16-grail-jggrx0420a',
                     'terluna:protection/spectra/shield_transmission.json',
                     'terluna:climate/gcm/products/climatology_A28_dim5_moon.npz'}
    assert set(MANIFEST.entries) == seeds | {hitemp.ENTRY}
    for pin in _seed_pins():
        assert MANIFEST.files(pin)


def test_terlunas_files_enter_the_seeds_only_through_pin_fields():
    assert SEEDS
    for path in SEEDS:
        kind = 'world' if path.name == 'world.toml' else 'scenario' if path.parent.name == 'scenarios' else None
        for field, value in _strings(tomllib.loads(path.read_text())):
            if value.startswith(('terluna:', 'terluna-drive:')):
                assert kind and field in data.PIN_FIELDS[kind], (path, field)


@needs_repo
def test_the_manifest_records_the_bytes_terlunas_input_records_name():
    """The outside data the lab fetched are those Terluna's own input records pin, by name, size and hash."""
    records = {}
    for path in (LAB.parent / 'python' / 'atmosphere' / 'radiative_convective' / 'inputs.json',
                 TERLUNA / 'geography' / 'inputs.json'):
        records.update({f['name']: (f['bytes'], f['sha256']) for f in json.loads(path.read_text())['files']})
    for name in ('tsis1-hsrs-stride100', 'lola-ldem16-grail-jggrx0420a'):
        for f in MANIFEST.entries[name]['files']:
            assert records[f.name] == (f.bytes, f.sha256), f.name


@pytest.mark.parametrize('entry, change, message', [
    (dict(licence=None), {}, 'an entry holds'),
    (dict(extra='x'), {}, 'an entry holds'),
    (dict(reviewed='2026-10-18'), {}, 'date of its licence review'),
    (dict(files_empty=True), {}, 'one file or more'),
    ({}, dict(sha256='0' * 63), 'sha256 is 64'),
    ({}, dict(bytes=True), 'bytes is a positive'),
    ({}, dict(retrieved='2026-10-18'), 'date the lab took'),
    ({}, dict(url='https://x/y'), 'one source'),
    ({}, dict(source=None), 'one source'),
    ({}, dict(source='terluna:a.json@0123456789abcdef'), 'without # or @'),
    ({}, dict(source=None, url='http://x/y'), 'a url starts with'),
    ({}, dict(name='a/b'), 'plain file name'),
    ({}, dict(commit='abc'), 'full Git commit'),
    ({}, dict(made=''), 'made is a non-empty'),
])
def test_a_malformed_manifest_is_refused(tmp_path, entry, change, message):
    record = {k: v for k, v in {**_record('a.json', b'{}', source='terluna:a.json'), **change}.items() if v is not None}
    empty = entry.pop('files_empty', False)
    path = _manifest(tmp_path, [] if empty else [record], **entry)
    if empty:
        path.write_text(path.read_text() + 'files = []\n')
    with pytest.raises(DataError, match=message):
        Manifest(path)


@pytest.mark.parametrize('kwargs, message', [
    (dict(top='schema = "worldlab.manifest/1"'), 'schema'),
    (dict(top='schema = "worldlab.manifest/0"\nother = 1'), 'unknown keys'),
    (dict(name='x#a'), 'without # or @'),
    (dict(name='x@0123456789abcdef'), 'without # or @'),
    (dict(name='Not A Pin'), 'plain name'),
])
def test_a_manifest_of_another_schema_or_ill_named_entries_is_refused(tmp_path, kwargs, message):
    with pytest.raises(DataError, match=message):
        Manifest(_manifest(tmp_path, [_record('a.json', b'{}', source='terluna:a.json')], **kwargs))


def test_two_files_of_one_digest_or_one_name_are_refused(tmp_path):
    with pytest.raises(DataError, match='shares its digest'):
        Manifest(_manifest(tmp_path, [_record('a.json', b'{}', source='terluna:a.json'),
                                      _record('b.json', b'{}', source='terluna:b.json')]))
    with pytest.raises(DataError, match='two files named lakes.npz'):
        Manifest(_manifest(tmp_path, [_record('lakes.npz', b'old', source='terluna:old/lakes.npz'),
                                      _record('lakes.npz', b'new', source='terluna:lakes.npz')]))


# The store.

def test_a_fetch_copies_from_terlunas_root_and_keeps_only_matching_bytes(terluna, tmp_path):
    repo, store = terluna
    (repo / 'p').mkdir()
    (repo / 'p' / 'a.json').write_bytes(b'{"a": 1}')
    manifest = Manifest(_manifest(tmp_path, [_record('a.json', b'{"a": 1}', source='terluna:p/a.json')]))
    assert manifest.status(store=store, lab=tmp_path) == {'present': [], 'missing': ['a.json'], 'changed': []}
    assert manifest.fetch(store=store, lab=tmp_path)['copied'] == ['a.json']
    copy = manifest.path('x', store=store, lab=tmp_path)
    assert copy == store / 'data' / _digest(b'{"a": 1}') / 'a.json'
    assert copy.read_bytes() == b'{"a": 1}' and not copy.stat().st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
    assert manifest.fetch(store=store, lab=tmp_path)['present'] == ['a.json']
    assert sorted(p.name for p in copy.parent.iterdir()) == ['a.json']        # no partial file left beside it


def test_a_changed_store_copy_is_reported_and_left_for_review(terluna, tmp_path):
    repo, store = terluna
    (repo / 'a.json').write_bytes(b'{"a": 1}')
    (repo / 'b.json').write_bytes(b'{"b": 1}')
    manifest = Manifest(_manifest(tmp_path, [_record('a.json', b'{"a": 1}', source='terluna:a.json'),
                                             _record('b.json', b'{"b": 1}', source='terluna:b.json')]))
    copy = store / 'data' / _digest(b'{"a": 1}') / 'a.json'
    copy.parent.mkdir(parents=True)
    copy.write_bytes(b'{"a": 2}')
    report = manifest.fetch(store=store, lab=tmp_path)
    assert report['changed'] == ['a.json'] and report['copied'] == ['b.json'] and copy.read_bytes() == b'{"a": 2}'
    assert manifest.status(store=store, lab=tmp_path)['changed'] == ['a.json']
    with pytest.raises(DataError, match='differ'):
        manifest.path('x@' + _digest(b'{"a": 1}'), store=store, lab=tmp_path)
    assert data.main(['--fetch'], manifest=manifest, store=store, lab=tmp_path) == 1


def test_a_fetch_refuses_a_changed_source_and_writes_nothing(terluna, tmp_path):
    repo, store = terluna
    (repo / 'a.json').write_bytes(b'{"a": 2}')
    manifest = Manifest(_manifest(tmp_path, [_record('a.json', b'{"a": 1}', source='terluna:a.json')]))
    with pytest.raises(DataError, match='need review'):
        manifest.fetch(store=store, lab=tmp_path)
    assert list(store.iterdir()) == [store / 'data'] and not any((store / 'data').iterdir())


def test_a_fetch_without_terlunas_root_reports_the_copy_missing(tmp_path, monkeypatch):
    monkeypatch.delenv('TERLUNA_REPO', raising=False)
    (tmp_path / 'store').mkdir()
    manifest = Manifest(_manifest(tmp_path, [_record('a.json', b'{}', source='terluna:a.json')]))
    assert manifest.fetch(store=tmp_path / 'store', lab=tmp_path)['missing'] == ['a.json']
    assert data.main([], manifest=manifest, store=tmp_path / 'store', lab=tmp_path) == 1


def test_a_fetch_downloads_only_when_asked_and_stops_past_the_recorded_size(tmp_path):
    store = tmp_path / 'store'
    store.mkdir()
    served = tmp_path / 'served.csv'
    served.write_bytes(b'1,2\n')
    manifest = Manifest(_manifest(tmp_path, [_record('s.csv', b'1,2\n', url=served.as_uri())]))
    assert manifest.fetch(store=store, lab=tmp_path)['missing'] == ['s.csv']
    assert manifest.fetch(store=store, download=True, lab=tmp_path)['downloaded'] == ['s.csv']
    assert manifest.path('x', store=store, lab=tmp_path).read_bytes() == b'1,2\n'

    large = tmp_path / 'large.bin'
    large.write_bytes(b'\0' * (3 << 20))                                   # three chunks, where one is recorded
    longer = Manifest(_manifest(tmp_path, [_record('l.bin', b'\0' * (1 << 20), url=large.as_uri())]))
    with pytest.raises(DataError, match=f'more than {1 << 20} bytes'):
        longer.fetch(store=store, download=True, lab=tmp_path)
    assert not (store / 'data' / _digest(b'\0' * (1 << 20))).exists()


def test_an_entry_of_several_files_names_one_by_its_digest(tmp_path):
    store = tmp_path / 'store'
    store.mkdir()
    sources = {name: tmp_path / name for name in ('a.img', 'a.lbl')}
    for name, path in sources.items():
        path.write_bytes(name.encode())
    manifest = Manifest(_manifest(tmp_path, [_record(n, n.encode(), url=p.as_uri()) for n, p in sources.items()]))
    label = f"x@{_digest(b'a.lbl')}"
    assert manifest.fetch([label], store=store, download=True, lab=tmp_path)['downloaded'] == ['a.lbl']
    assert manifest.path(label, store=store, lab=tmp_path).name == 'a.lbl'
    manifest.fetch(store=store, download=True, lab=tmp_path)
    assert set(manifest.paths('x', store=store, lab=tmp_path)) == {'a.img', 'a.lbl'}
    with pytest.raises(DataError, match='holds 2 files'):
        manifest.path('x', store=store, lab=tmp_path)
    with pytest.raises(DataError, match='no file of digest'):
        manifest.files('x@0123456789abcdef')


def test_the_command_line_reports_refusals_and_takes_download_with_fetch(tmp_path, capsys, monkeypatch):
    monkeypatch.delenv('WORLDLAB_STORE', raising=False)
    manifest = Manifest(_manifest(tmp_path, [_record('a.json', b'{}', source='terluna:a.json')]))
    assert data.main([], manifest=manifest, lab=tmp_path) == 1                 # no store at this lab
    assert 'refused: the store is unset' in capsys.readouterr().err
    with pytest.raises(SystemExit):
        data.main(['--download'], manifest=manifest, lab=tmp_path)


# This machine's store, and Terluna's files.

@needs_store
def test_the_store_holds_every_file_of_the_manifest():
    assert MANIFEST.status() == {'present': [f.name for e in MANIFEST.entries.values() for f in e['files']],
                                 'missing': [], 'changed': []}
    assert data.main([]) == 0


@needs_store
def test_the_open_moons_filter_names_an_entry_of_its_file():
    pin = parse_pin(LIB.scenario('moon/open-moon')['sunlight']['filter'])
    product = json.loads(MANIFEST.path(pin).read_text())
    assert len(product['transmission'][pin.entry]) == len(product['wavelength_nm'])
