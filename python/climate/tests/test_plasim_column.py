"""The column of PlaSim's physics (climate/gcm/plasim_column.py) and patch 21 of models/exoplasim/patches, without a
GCM run: the routines the column takes over are PlaSim's, each defined once where the column weakens it; its
message-passing layer defines every routine of PlaSim's single-process stub; patch 21 declares, reads and broadcasts
its two names once, at defaults that write nothing; the files the column reads and writes keep their layout; the
low air's and boundary layer's measures, the joined windows and the replay's verdict follow their definitions; and a
site takes the GCM's nearest grid point of its kind. The checks against a GCM's runs are in
lab/tests/test_plasim_column.py.

The lab's own file."""
import io
import re
import struct
import tarfile

import numpy as np
import pytest

from climate.gcm import plasim_column as pc
from climate.tests.conftest import ARCHIVE, SOURCES, _pinned

PATCH = '21-column-forcing.patch'


def routines(text: str) -> list:
    """The names of the subroutines and functions a Fortran text defines, in lower case."""
    return [m.lower() for m in re.findall(r'^\s*(?:(?:real|integer|logical)\s+)?(?:subroutine|function)\s+(\w+)',
                                          text, flags=re.M | re.I)]


@pytest.fixture(scope='module')
def archive_sources():
    if not ARCHIVE.exists():
        pytest.skip('the pinned ExoPlaSim archive (upstream/) is missing')
    with tarfile.open(fileobj=io.BytesIO(_pinned(ARCHIVE)), mode='r:gz') as tar:
        return {m.name[len(SOURCES):]: tar.extractfile(m).read().decode('latin-1') for m in tar.getmembers()
                if m.isfile() and m.name.startswith(SOURCES) and m.name.endswith('.f90')
                and '/' not in m.name[len(SOURCES):]}


# The build's parts.

def test_each_routine_the_column_takes_over_is_plasims_and_defined_once_in_the_object_it_weakens(archive_sources,
                                                                                                series_sources):
    """master (plasim.f90), mkdqtgp (rainmod.f90), makeareas (utilities_stub.f90) and oroini (glaciermod.f90): each
    defined once in the file whose object the column weakens, in no other file the single-process build links, and once
    in the column's driver, which defines nothing else at the top level but its module."""
    texts = dict(archive_sources)
    for name in ('plasim.f90', 'rainmod.f90'):
        texts[name] = series_sources.source(name, series_sources.names[-1])
    linked = {name: text for name, text in texts.items()
              if name not in ('mpimod.f90', 'mpimod_multi.f90', 'utilities.f90', 'plasim_dummy.f90', 'rainmod_bm.f90',
                              'rainmod_kuo_old.f90', 'rainmod_mca.f90', 'icemod_template.f90', 'guimod.f90',
                              'fft991mod.f90', 'cpl.f90')}
    for obj, symbol in pc.REPLACED.items():
        routine = symbol.rstrip('_')
        holders = [name for name, text in linked.items() if routine in routines(text)]
        assert holders == [obj[:-2] + '.f90'], (routine, holders)
        assert routines(linked[obj[:-2] + '.f90']).count(routine) == 1
    driver = (pc.HERE / pc.DRIVER).read_text()
    top = routines(re.sub(r'\n      contains\n.*?\n      end subroutine master\n', '\n', driver, flags=re.S))
    assert sorted(top) == sorted(s.rstrip('_') for s in pc.REPLACED.values())


def test_the_message_passing_layer_defines_every_routine_of_plasims_stub(archive_sources):
    stub = set(routines(archive_sources['mpimod_stub.f90']))
    layer = routines((pc.HERE / pc.MPI_LAYER).read_text())
    assert stub <= set(layer) and len(layer) == len(set(layer))
    assert set(layer) - stub == set()


def test_patch_21_declares_reads_and_broadcasts_each_name_once_and_writes_nothing_by_default(series_sources):
    assert all(len(line) <= 132 for line in series_sources.added(PATCH))
    module = series_sources.source('plasimmod.f90', PATCH)
    main = series_sources.source('plasim.f90', PATCH)
    namelist = main[main.index('      namelist /plasim_nl/'):main.index('!     preset namelist parameter')]
    for name in ('ncolforce', 'ncoldump'):
        assert re.findall(rf'integer :: {name}\s+= (\d+)', module) == ['0']
        assert len(re.findall(rf'call mpbci\({name} ?\)', main)) == 1
        assert len(re.findall(rf'\b{name}\b', namelist)) == 1
    # Each call into the patch's routines stands behind its switch, outside the initial short steps.
    calls = [line.strip() for line in main.splitlines() if re.search(r'call (colwindow|colsum|coldump)', line)]
    assert calls == ['if (ncolforce == 1 .and. nkits == 0) call colwindow',
                     'if (ncoldump > 0 .and. nkits == 0 .and. nhcstp <= ncoldump) call coldump(1)',
                     'if (ncolforce == 1 .and. nkits == 0) call colsum',
                     'if (ncoldump > 0 .and. nkits == 0 .and. nhcstp <= ncoldump) call coldump(2)']
    out = series_sources.source('outmod.f90', PATCH)
    writes = re.findall(r'call writegp\(40,\w+(?:\(1,jlev\))?,(\d+),', out[out.index('if (ncolforce == 1) then'):])
    assert writes == [str(c) for c in range(241, 251)]
    # The codes are PlaSim's own nowhere else.
    before = series_sources.source('outmod.f90', series_sources.before(PATCH))
    assert not set(re.findall(r'call writegp\(\d+,[^,]+,(\d+),', before)) & {str(c) for c in range(241, 251)}


# The files.

def test_records_round_trip_and_a_dump_unpacks_into_its_fields(tmp_path):
    points, levels = 3, 2
    rng = np.random.default_rng(1)
    count1 = 2 * points * (levels + 1) + 2 * points * levels + points + 1
    count2 = 7 * points * levels + 2 * points * (levels + 1) + 8 * points
    parts = [rng.normal(size=count1), rng.normal(size=count2)]
    data = b''.join(pc.record(np.array([5, k + 1, points, levels, part.size, 7], '<i4')) + pc.record(part)
                    for k, part in enumerate(parts))
    (tmp_path / 'dump').write_bytes(data)
    assert [len(r) for r in pc.records(tmp_path / 'dump')] == [24, 8 * count1, 24, 8 * count2]
    (step,) = pc.read_dump(tmp_path / 'dump')
    assert (step['nstep'], step['row'], step['points'], step['levels']) == (5, 7, 3, 2)
    assert np.array_equal(step['inputs']['t'], parts[0][:9].reshape(3, 3)) and step['inputs']['psurf'] == parts[0][-1]
    assert np.array_equal(step['inputs']['ps'], parts[0][-4:-1])
    assert np.array_equal(step['outputs']['dtdt'], parts[1][:6].reshape(2, 3))
    assert np.array_equal(step['outputs']['cloud'], parts[1][-6:].reshape(2, 3))
    assert np.array_equal(step['outputs']['convective_rain'], parts[1][6 * 6 + 2 * 9:6 * 6 + 2 * 9 + 3])
    (tmp_path / 'broken').write_bytes(data[:-3])
    with pytest.raises(ValueError):
        pc.records(tmp_path / 'broken')


def test_plasims_raw_output_is_read_by_code_level_and_steps(tmp_path):
    nugp = 8
    head = lambda code, level, steps: pc.record(np.array([code, level, 0, 0, 4, 2, steps, 12], '<i4'))
    field = lambda value: pc.record(np.full(nugp, value, '<f4'))
    body = pc.record(np.array([333, 0, 0, 0, 4, 2, 2, 1], '<i4')) + pc.record(np.zeros(nugp, '<f4'))
    for steps in (4, 9):
        body += head(142, 0, steps) + field(steps) + head(241, 1, steps) + field(10 + steps) \
            + head(241, 2, steps) + field(20 + steps)
    (tmp_path / 'plasim_output').write_bytes(body)
    found = pc.read_output(tmp_path / 'plasim_output', [142, 241])
    assert list(found[142]['steps']) == [4, 9] and found[142]['field'].shape == (2, nugp)
    assert found[241]['field'].shape == (2, 2, nugp) and found[241]['field'][1, 0, 0] == 19.0
    with pytest.raises(ValueError, match='no records of code 143'):
        pc.read_output(tmp_path / 'plasim_output', [143])


def test_a_column_folder_holds_the_gcms_inputs_its_restart_and_its_own_files(tmp_path):
    gcm = tmp_path / 'gcm'
    gcm.mkdir()
    for name in ('plasim_namelist', 'N032_surf_0172.sra', 'sun.dat', 'lab_rain_law.txt', 'plasim_output',
                 'plasim_diag', 'plasim_status', 'annualweather'):
        (gcm / name).write_text(name)
    nlon, levels = 4, 3
    state = dict(t=np.ones((nlon, levels)), q=np.zeros((nlon, levels)), u=np.zeros((nlon, levels)),
                 v=np.zeros((nlon, levels)), ps=np.full(nlon, 1e5), psurf=1e5, dqt=np.zeros((nlon, levels)))
    windows = dict(steps=np.array([2, 3]), dynamics={k: np.zeros((2, nlon, levels)) for k in 'tquv'} |
                   {'lnps': np.zeros((2, nlon))})
    folder = pc.prepare(tmp_path / 'col', gcm, gcm / 'plasim_status', row=5, steps=5, start=state, windows=windows,
                        points=[2])
    assert sorted(p.name for p in folder.iterdir()) == ['N032_surf_0172.sra', 'column_input', 'column_namelist',
                                                       'lab_rain_law.txt', 'plasim_namelist', 'plasim_restart',
                                                       'sun.dat']
    assert 'nrow = 5' in (folder / 'column_namelist').read_text() and 'nmode = 1' in (folder / 'column_namelist').read_text()
    raw = pc.records(folder / 'column_input')
    assert [len(r) for r in raw] == [8, 4, 8, 8 * (4 * nlon * levels + nlon)] + [4, 8 * (4 * nlon * levels + nlon)] * 2
    with pytest.raises(ValueError, match='cover 5 steps'):
        pc.prepare(tmp_path / 'long', gcm, gcm / 'plasim_status', row=5, steps=6, start=state, windows=windows)
    with pytest.raises(ValueError, match='grid points 1 to 4'):
        pc.prepare(tmp_path / 'wide', gcm, gcm / 'plasim_status', row=5, steps=5, start=state, windows=windows,
                   points=[5])
    with pytest.raises(ValueError, match='mode 1'):
        pc.prepare(tmp_path / 'both', gcm, gcm / 'plasim_status', row=5, steps=1, start=state)
    with pytest.raises(ValueError, match='steps by one of'):
        pc.prepare(tmp_path / 'euler', gcm, gcm / 'plasim_status', row=5, steps=5, start=state, windows=windows,
                   scheme='euler')
    (gcm / 'fluxmod_namelist').write_text(' &fluxmod_nl\n NGUST = 1\n /END\n')
    changed = pc.prepare(tmp_path / 'longer', gcm, gcm / 'plasim_status', row=5, steps=5, start=state,
                         windows=windows, scheme='leapfrog', changes={'fluxmod_namelist': {'VDIFF_LAMM': 966.4}})
    assert (changed / 'fluxmod_namelist').read_text() == ' &fluxmod_nl\n NGUST = 1\n VDIFF_LAMM = 966.4\n /END\n'
    assert 'nscheme = 2' in (changed / 'column_namelist').read_text()
    with pytest.raises(ValueError, match='namelists'):
        pc.prepare(tmp_path / 'other', gcm, gcm / 'plasim_status', row=5, steps=5, start=state, windows=windows,
                   changes={'sun.dat': {'X': 1}})


def test_a_namelists_entries_are_set_in_their_line_or_join_before_its_close():
    text = ' &fluxmod_nl\n NGUST = 1\n NSIMW = 1\n /END\n'
    assert pc.namelist_with(text, {'NGUST': 0, 'VDIFF_LAMM': 966.4}) == \
        ' &fluxmod_nl\n NGUST = 0\n NSIMW = 1\n VDIFF_LAMM = 966.4\n /END\n'
    assert pc.namelist_with(' &x_nl\n zumin = 1.\n /\n', {'ZUMIN': 0.1}) == ' &x_nl\n ZUMIN = 0.1\n /\n'
    with pytest.raises(ValueError):
        pc.namelist_with('NGUST = 1\n', {'NGUST': 0})


# The measures and the verdict.

def test_the_measures_follow_their_definitions():
    half = np.array([0.2, 0.5, 0.8, 0.9, 0.97, 1.0])
    sigma = 0.5 * (np.r_[0.0, half[:-1]] + half)
    ps = 1.2e5
    t = 300.0 * sigma ** 0.2
    q = np.array([1e-5, 2e-3, 8e-3, 1.2e-2, 1.4e-2, 1.6e-2])
    m = pc.measures(t, q, ps, half)
    p = sigma * ps
    the = pc.theta_e(t, p, q)
    w = np.array([0.0, 0.0, 0.0, 0.05, 0.07, 0.03])               # each layer's sigma within 0.85-1.0
    assert pc.overlap(half, 0.85, 1.0) == pytest.approx(w)
    assert m['theta_e_b_k'] == pytest.approx((the * w).sum() / 0.15)
    assert m['excess_k'] == pytest.approx(the[-1] - m['theta_e_b_k'])
    assert m['vapour_fall_g_kg'] == pytest.approx(1e3 * (q[-1] - q[3]))   # sigma 0.85 the nearest level to 0.85
    assert (m['t_low_k'], m['q_low_g_kg']) == (pytest.approx(t[-1]), pytest.approx(16.0))
    # Bolton's theta-e with T_L from his eq. 21, by the vapour pressure, in place of eq. 22, by relative humidity:
    # the two forms agree within 0.1 K; and dry air takes the potential temperature.
    r = q[-1] / (1 - q[-1])
    e_hpa = r * p[-1] / (287.04 / 461.5 + r) / 100.0
    tl = 2840.0 / (3.5 * np.log(t[-1]) - np.log(e_hpa) - 4.805) + 55.0
    rg = 1000.0 * r
    eq21 = t[-1] * (1e5 / p[-1]) ** (0.2854 * (1 - 0.28e-3 * rg)) * np.exp((3.376 / tl - 0.00254) * rg * (1 + 0.81e-3 * rg))
    assert abs(the[-1] - eq21) < 0.1
    assert pc.theta_e(280.0, 8e4, 0.0) == pytest.approx(280.0 * 1.25 ** 0.2854, rel=1e-6)
    # A column of one potential temperature and one vapour holds one theta-e to a few hundredths of a kelvin, and the
    # lowest level stands out of it by nothing.
    flat = pc.measures(290.0 * sigma ** 0.2854, np.full(6, 1e-3), 1e5, half)
    assert abs(flat['excess_k']) < 0.05 and flat['vapour_fall_g_kg'] == 0.0


def test_joined_windows_keep_each_windows_weight_by_its_steps():
    steps = np.array([4, 5, 5, 5, 5])
    d = np.arange(5.0)[:, None, None] * np.ones((5, 2, 3))
    joined = pc.joined(dict(steps=steps, dynamics={'t': d}), 2)
    assert list(joined['steps']) == [9, 10, 5]
    assert joined['dynamics']['t'][0, 0, 0] == pytest.approx((4 * 0 + 5 * 1) / 9)
    assert joined['dynamics']['t'][2, 1, 2] == 4.0


def test_the_verdict_holds_where_each_quantity_lies_within_its_tolerance_in_every_quarter():
    hour = np.array([-60.0, 30.0, 120.0, -150.0] * 2)
    gcm = dict(rain_mm_day=np.array([1.0, 4.0, 2.0, 0.2] * 2), t_low_k=np.full(8, 300.0), q_low_g_kg=np.full(8, 15.0),
               theta_e_low_k=np.full(8, 340.0), theta_e_b_k=np.full(8, 335.0), excess_k=np.full(8, 5.0),
               vapour_fall_g_kg=np.full(8, 3.0), b_l_k=np.full(8, -7.0))
    near = {k: v + (0.4 if k != 'rain_mm_day' else 0.2) for k, v in gcm.items()}
    found = pc.replay_verdict(dict(hour_deg=hour, gcm=gcm, column=near))
    assert found['verdict'] == 'PASS' and found['quarters']['b_l_k']['evening']['holds'] is None
    assert found['quarters']['rain_mm_day']['afternoon']['limit'] == 1.0
    far = dict(near, excess_k=near['excess_k'] + np.array([0, 0, 2.0, 0] * 2),
               rain_mm_day=gcm['rain_mm_day'] * np.array([1, 1.5, 1, 1] * 2))
    found = pc.replay_verdict(dict(hour_deg=hour, gcm=gcm, column=far))
    assert found['verdict'] == 'FAIL' and found['breaks'] == ['rain_mm_day afternoon', 'excess_k evening']
    assert list(pc.quarter_of([-90.0, -0.1, 0.0, 89.9, 90.0, 180.0, -180.0, -90.1])) == [0, 0, 1, 1, 2, 3, 3, 3]


# The site.

def test_a_site_takes_the_nearest_grid_point_of_its_kind(tmp_path):
    from climate.crm import gcm_site as gs
    nlat, nlon, g = 32, 64, 1.62
    lat = pc.gaussian_latitudes(nlat)
    assert lat[0] > 0 > lat[-1] and np.allclose(lat, -lat[::-1]) and abs(lat[16] + 2.7689) < 1e-3
    land = np.ones((nlat, nlon))
    land[14:20, 50:60] = 0.0                                    # a sea west of 0 E
    geopotential = np.where(land > 0, 500.0 * g, 0.0)

    def sra(code, field):
        head = f'{code:10d}{0:10d}{20090101:10d}{0:10d}{nlon:10d}{nlat:10d}{0:10d}{0:10d}\n'
        (tmp_path / f'N032_surf_{code:04d}.sra').write_text(head + ''.join(f' {x:9.3f}' for x in field.ravel()) + '\n')
    sra(172, land)
    sra(129, geopotential)
    assert np.array_equal(gs.read_sra(tmp_path / 'N032_surf_0172.sra'), land)
    site = dict(lat_deg=-5.0, lon_deg=-45.0, half_lat_deg=5.6, half_lon_deg=8.5, surface='sea')
    row, point = pc.site_point(tmp_path, site, g)
    assert (row, point) == (17, 57) and land[row - 1, point - 1] == 0.0
    assert pc.site_point(tmp_path, dict(site, lon_deg=-60.0), g) == (17, 54)
    with pytest.raises(ValueError, match='no land cells'):
        pc.site_point(tmp_path, dict(site, surface='land', half_lat_deg=1.0, half_lon_deg=1.0), g)
