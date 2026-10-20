"""HITEMP2010's water lines: their entry in the lab's data manifest, the reader of HITRAN's 160-character records in the
zips, the cut at 1000 K, the cache of the cut list, and, where the store holds the zips, their first records and the
cut list they give."""
import hashlib
import zipfile

import numpy as np
import pytest

from atmosphere.radiative_convective import fetch_inputs as column_inputs, spectroscopy as sp
from atmosphere.waterworlds import hitemp, steam_optics as so

worldlab = pytest.importorskip('worldlab.data')
needs_sums = pytest.mark.skipif(column_inputs.restore()['status'] != 'PASS',
                                reason='spectroscopic inputs not restored (radiative_convective.fetch_inputs --download)')


def _store_zips():
    """The store's zips, by name, where the store holds every one at its recorded size; else None."""
    from worldlab.roots import root
    store = root('store')
    if store is None:
        return None
    files = worldlab.Manifest().files(hitemp.ENTRY)
    paths = {f.name: f.in_store(store) for f in files}
    whole = all(p.is_file() and p.stat().st_size == f.bytes for p, f in zip(paths.values(), files))
    return (store, paths) if whole else None


needs_zips = pytest.mark.skipif(_store_zips() is None, reason="the store holds no whole copy of HITEMP2010's zips")


def _record(nu, strength, elower, *, iso='1', gamma_air=0.0613, gamma_self=0.333, n_air=0.53, molecule=' 1',
            end='\r\n'):
    """A line in HITRAN's 160-character layout: I2, A1, F12.6, E10.3, E10.3, F5.4, F5.3, F10.4, F4.2, F8.6, then the
    quantum numbers and references, here blank."""
    text = (f'{molecule}{iso}{nu:12.6f}{strength:10.3E}{1e-20:10.3E}' + f'{gamma_air:.4f}'[1:]
            + f'{gamma_self:5.3f}{elower:10.4f}{n_air:4.2f}{0.0:8.6f}')
    assert len(text) == 67
    return text.ljust(160) + end


def _zip(path, records, member='lines.par'):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(member, ''.join(records))
    return path


def test_the_manifest_records_34_zips_from_0_to_30000_cm_holding_hitemp2010s_lines():
    files = worldlab.Manifest().files(hitemp.ENTRY)
    ranges = [tuple(int(x) for x in f.name.split('_')[1].split('-')) for f in files]
    assert len(files) == 34 and ranges[0][0] == 0 and ranges[-1][1] == 30000
    assert all(a[1] == b[0] for a, b in zip(ranges, ranges[1:]))
    counts = [int(f.note.split(' lines')[0].replace(',', '')) for f in files]
    assert sum(counts) == 114241164                              # HITEMP2010's count of water lines
    assert all(f.url.endswith(f.name) for f in files)


@needs_sums
def test_records_read_field_by_field_and_the_cut_keeps_the_lines_whose_strength_at_1000_k_reaches_the_floor(tmp_path):
    sums = sp.PartitionSums(np.asarray([1, 2]))
    factor = hitemp.strengths(np.array([2000.0]), 1.0, np.array([3000.0]), np.array([1]), sums, hitemp.T_CUT)[0]
    above, below = 1.02 * hitemp.FLOOR / factor, 0.98 * hitemp.FLOOR / factor
    records = [_record(2000.0, below, 3000.0),                  # 2% short of the floor at 1000 K
               _record(1234.567891, 1.5e-20, 1234.5678, iso='2', gamma_air=0.0471, gamma_self=0.401, n_air=0.71),
               _record(2000.0, above, 3000.0),                  # 2% over it
               _record(0.0, 1e-20, 100.0),                      # a line at 0 cm^-1
               _record(3000.0, 1e-20, -1.0)]                    # a lower-state energy left unknown
    lines, read = hitemp.cut([_zip(tmp_path / 'a.zip', records)], sums)
    assert read == 5 and len(lines['nu']) == 2
    assert lines['nu'].tolist() == [1234.567891, 2000.0]        # sorted by wavenumber
    assert lines['strength'][0] == 1.5e-20 and lines['strength'][1] == pytest.approx(above, rel=1e-3)
    assert lines['gamma_air'][0] == 0.0471 and lines['gamma_self'][0] == 0.401 and lines['n_air'][0] == 0.71
    assert lines['elower'][0] == 1234.5678 and lines['delta_air'][0] == 0.0
    assert lines['gid'].tolist() == [2, 1] and lines['mass'][0] == sp.ISOTOPOLOGUES[(1, '2')][1]


@needs_sums
def test_the_cuts_strength_is_the_one_the_columns_line_sum_integrates():
    """One line at 1000 K and 1 Pa, a Doppler core on a grid of a thousandth of a wavenumber: the column's line sum
    integrates to the strength the cut takes."""
    sums = sp.PartitionSums(np.asarray([1]))
    line = sp.LineList('H2O', *(np.array([v]) for v in (2000.0, 1e-20, 0.07, 0.3, 1500.0, 0.6, 0.0)),
                       np.array([1]), np.array([sp.ISOTOPOLOGUES[(1, '1')][1]]))
    grid = sp.Grid.span(1960.0, 2040.0, 0.001)
    sigma = sp.line_absorption(grid, line, sums, 1000.0, 1.0, 1.0, cutoff=so.CUTOFF)
    strength = hitemp.strengths(line.nu, line.strength, line.elower, line.gid, sums, 1000.0)[0]
    assert sigma.sum() * grid.step == pytest.approx(strength, rel=1e-5)


@needs_sums
def test_zips_and_records_of_another_layout_are_refused(tmp_path):
    sums = sp.PartitionSums(np.asarray([1]))
    good = _record(1000.0, 1e-20, 100.0)
    cases = {'lf.zip': [_record(1000.0, 1e-20, 100.0, end='\n')] * 162,       # 161-byte records, 162 of them
             'short.zip': [good, good[:-5]],
             'molecule.zip': [good, _record(1000.0, 1e-20, 100.0, molecule=' 2')],
             'isotopologue.zip': [_record(1000.0, 1e-20, 100.0, iso='Z')]}
    for name, records in cases.items():
        with pytest.raises(ValueError):
            hitemp.cut([_zip(tmp_path / name, records)], sums)
    with zipfile.ZipFile(tmp_path / 'two.zip', 'w') as archive:
        archive.writestr('a.par', good)
        archive.writestr('b.par', good)
    with pytest.raises(ValueError):
        hitemp.cut([tmp_path / 'two.zip'], sums)


@needs_sums
def test_the_cut_list_is_cached_under_its_key_and_read_back_without_the_zips(tmp_path):
    zips = [_zip(tmp_path / 'a.zip', [_record(1500.0, 1e-20, 100.0), _record(1400.0, 1e-35, 100.0)]),
            _zip(tmp_path / 'b.zip', [_record(900.0, 2e-21, 400.0)])]
    record = [(z.name, hashlib.sha256(z.read_bytes()).hexdigest()) for z in zips]
    cache = tmp_path / 'cache'
    lines = hitemp.load(record, cache, paths=lambda: zips, report=lambda *_: None)
    assert isinstance(lines, sp.LineList) and lines.nu.tolist() == [900.0, 1500.0]
    assert (cache / f'{hitemp.key(record)}.npz').is_file()

    def gone():
        raise FileNotFoundError('the zips are gone')
    assert hitemp.load(record, cache, paths=gone).nu.tolist() == [900.0, 1500.0]     # from the cache alone
    assert len({hitemp.key(record), hitemp.key(record, floor=1e-31), hitemp.key(record, t_cut=900.0),
                hitemp.key([(record[0][0], 'f' * 64), record[1]])}) == 4
    with pytest.raises(FileNotFoundError):                    # another cut needs the zips again
        hitemp.load(record, cache, paths=gone, floor=1e-31)
    with pytest.raises(ValueError):                           # and they must be the zips of the record
        hitemp.load(record, cache, paths=lambda: zips[::-1], floor=1e-31)
    with pytest.raises(ValueError):
        hitemp.load([], cache, paths=lambda: [])


@needs_sums
def test_the_cut_in_two_processes_is_the_cut_in_one(tmp_path):
    zips = [_zip(tmp_path / f'{i}.zip', [_record(1000.0 + 10 * i + j, 1e-20 * (j + 1), 100.0 * j) for j in range(3)])
            for i in range(3)]
    record = [(z.name, hashlib.sha256(z.read_bytes()).hexdigest()) for z in zips]
    one = hitemp.load(record, tmp_path / 'one', paths=lambda: zips, report=lambda *_: None)
    two = hitemp.load(record, tmp_path / 'two', paths=lambda: zips, processes=2, report=lambda *_: None)
    assert len(one) == 9
    for k in hitemp.ORDER:
        assert np.array_equal(getattr(one, k), getattr(two, k))


@needs_zips
def test_the_first_records_of_the_stores_zips_read_as_hitemp2010s():
    _, paths = _store_zips()
    block = next(hitemp.blocks(paths['01_00000-00050_HITEMP2010.zip'], size=2))
    first = {name: hitemp._field(block, a, b) for name, (a, b) in hitemp.FIELDS.items()}
    assert first['nu'].tolist() == [0.0001, 0.0001] and first['strength'].tolist() == [3.998e-79, 6.731e-84]
    assert first['elower'][0] == 22841.1953 and first['gamma_self'][0] == 0.333 and first['n_air'][0] == 0.53


@needs_sums
@needs_zips
def test_the_stores_smallest_zip_gives_its_recorded_cut():
    """The zip from 11,000 to 30,000 cm^-1, which holds every line of unknown lower-state energy, cut anew."""
    _, paths = _store_zips()
    path = paths['01_11000-30000_HITEMP2010.zip']
    unknown = sum(int((hitemp._field(block, 45, 55) < 0).sum()) for block in hitemp.blocks(path))
    lines, read = hitemp.cut([path], sp.PartitionSums(hitemp.WATER))
    assert (read, len(lines['nu']), unknown) == (1461436, 622109, 19)


@needs_sums
@needs_zips
def test_the_steam_optics_take_the_stores_cut_list():
    store, _ = _store_zips()
    record = [(f.name, f.sha256) for f in worldlab.Manifest().files(hitemp.ENTRY)]
    if not (store / 'caches' / 'hitemp-lines' / f'{hitemp.key(record)}.npz').is_file():
        pytest.skip("the store's cache lacks the cut list of the current key (python -m atmosphere.waterworlds.hitemp)")
    optics = so.SteamOptics(lines='hitemp', store=store)
    assert len(optics.lines) == 6617956 and optics.cut == hitemp.key(record)
    assert optics.key != so.SteamOptics().key and optics.describe()['source'] == 'hitemp'
    sigma = optics.cross_section(so.Band(1500.0, 1505.0, 0.01, 10), 1e3, 250.0)
    assert np.all(np.isfinite(sigma)) and np.all(sigma >= 0) and sigma.max() > 0


@needs_zips
def test_the_stores_cut_list_holds_the_recorded_count():
    store, _ = _store_zips()
    record = [(f.name, f.sha256) for f in worldlab.Manifest().files(hitemp.ENTRY)]
    cached = store / 'caches' / 'hitemp-lines' / f'{hitemp.key(record)}.npz'
    if not cached.is_file():
        pytest.skip("the store's cache lacks the cut list of the current key (python -m atmosphere.waterworlds.hitemp)")
    with np.load(cached) as data:
        assert int(data['read']) == 114241164 and data['nu'].shape == (6617956,)
