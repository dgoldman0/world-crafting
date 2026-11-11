"""PlaSim's levels for a world (climate/gcm/levels.py): the released model's half levels, the set generated from a scale
height and stated heights against hand arithmetic, Terluna's sets for the Open Moon, Earth's values, the entries of a
run on a generated set, and the conservative remap that carries a restart from one set onto another.

Brought from Terluna's climate/tests/test_levels.py at 39c5ee04 (python/provenance.json): its tests of the sets'
placement, of a run's entries, of the remap and of a carried restart are kept, on sets the lab's rule generates from
Terluna's values in place of Terluna's named sets; the tests of the rule, of the released half levels' doubles, of
Earth's values, of a restart carried onto its own set and of the refusals are the lab's; and the tests of Terluna's
runner and of its products on fourteen and fifteen levels stay in Terluna. The compiled model's tests are in
lab/tests/test_builds.py."""
import math
import struct

import numpy as np
import pytest

from climate.gcm import levels as lv

MOON = lv.TERLUNA_OPEN_MOON_LEVELS
# Terluna's fifteen half levels and full levels as it records them, to four and five places
# (climate/results/gcm/levels_l15_test.json at 39c5ee04), and the same half levels as its module holds them and its
# runs' plasim_namelist states them in SIGH (gcm-runs/A28R_301k_cold_sbm_rh07_deep200_l15cap on Terluna's drive).
TERLUNA_HALF = [0.0766, 0.1616, 0.2601, 0.3736, 0.5, 0.6336, 0.7379, 0.7981, 0.8382, 0.8717, 0.9066, 0.941, 0.9666,
                0.9883, 1.0]
TERLUNA_FULL = [0.0383, 0.1191, 0.21085, 0.31685, 0.4368, 0.5668, 0.68575, 0.768, 0.81815, 0.85495, 0.88915, 0.9238,
                0.9538, 0.97745, 0.99415]
TERLUNA_SIGH = ('0.07660000000000002,0.16160000000000002,0.2601,0.3736000000000001,0.5,0.6335999999999999,0.7379,'
                '0.7981,0.8382,0.8717,0.9066,0.941,0.9666000000000001,0.9883,1.0')
EARTH_SCALE_HEIGHT_M = 8429.74       # Earth's air at 288 K: 8314.46 x 288 / (28.966 x 9.80665)


def fifteen() -> np.ndarray:
    return lv.generate(MOON['scale_height_m'], MOON['interfaces_m'], MOON['upper'])


def fourteen() -> np.ndarray:
    return lv.generate(MOON['scale_height_m'], MOON['interfaces_m'][:-1], MOON['upper'])


# The released model's levels.

def test_the_released_half_levels_are_the_formulas_in_the_compiled_models_doubles():
    half = lv.plasim_half()
    s = np.arange(1, 11) / 10
    powers = 0.75 * s + 1.75 * s ** 3 - 1.5 * s ** 4
    assert [round(float(x), 4) for x in half] == [0.0766, 0.1616, 0.2601, 0.3736, 0.5, 0.6336, 0.7651, 0.8816, 0.9666,
                                                  1.0] and half[-1] == 1.0
    # The doubles of the multiplied powers, which the compiled model runs on (lab/tests/test_builds.py); numpy's
    # powers end one or two units of the last place away at three of them.
    assert [repr(float(x)) for x in half] == [
        '0.07660000000000002', '0.16160000000000002', '0.2601', '0.37360000000000004', '0.5', '0.6335999999999999',
        '0.7651', '0.8816000000000002', '0.9666', '1.0']
    assert [i for i in range(10) if powers[i] != half[i]] == [3, 7, 8]
    assert [round(float(abs(powers[i] - half[i]) / np.spacing(half[i]))) for i in (3, 7, 8)] == [1, 2, 1]
    assert np.allclose(lv.full_levels(half),
                       [0.0383, 0.1191, 0.21085, 0.31685, 0.4368, 0.5668, 0.69935, 0.82335, 0.9241, 0.9833])
    assert lv.plasim_half(5)[-1] == 1.0 and lv.plasim_half(5).size == 5
    for bad in (0, 2.5, True, '10'):
        with pytest.raises(ValueError, match='count of levels'):
            lv.plasim_half(bad)


# The rule.

def test_a_generated_set_is_the_released_upper_half_levels_and_the_stated_heights_by_hand():
    """At a 10 km scale height, heights of 2 km and 1 km stand at exp(-0.2) = 0.818730... and exp(-0.1) = 0.904837...,
    0.8187 and 0.9048 to four places, under the released model's seven upper half levels."""
    half = lv.generate(10000.0, [2000.0, 1000.0], 7)
    assert half.size == 10 and np.array_equal(half[:7], lv.plasim_half()[:7])
    assert list(half[7:]) == [0.8187, 0.9048, 1.0]
    assert math.exp(-0.2) == pytest.approx(0.8187307531, abs=1e-10) and math.exp(-0.1) == pytest.approx(0.9048374180,
                                                                                                        abs=1e-10)
    assert np.array_equal(lv.full_levels(half)[7:], [0.5 * (half[6] + 0.8187), 0.5 * (0.8187 + 0.9048), 0.5 * 1.9048])
    # The count is the kept half levels, the stated heights and the ground; integers serve as heights.
    assert lv.generate(10000, (2000, 1000, 500, 250), 7).size == 12
    # Half the scale height doubles each height's depth in sigma: exp(-0.4) and exp(-0.2).
    assert list(lv.generate(5000.0, [2000.0, 1000.0], 5)[5:]) == [0.6703, 0.8187, 1.0]


def test_a_height_on_a_released_half_level_takes_that_half_levels_own_double():
    """Stated at the released half levels' own heights, at any scale height, the rule returns the released ten, so
    that a layer two sets share holds the same numbers in both."""
    ten = lv.plasim_half()
    for scale_height in (EARTH_SCALE_HEIGHT_M, 22000.0, 43629.8, 51000.0):
        heights = [float(z) for z in lv.heights_m(ten[6:9], scale_height)]
        assert np.array_equal(lv.generate(scale_height, heights, 6), ten)
    assert round(math.exp(-1730.0 / 51000.0), 4) == 0.9666 and fifteen()[12] == ten[8]
    assert sorted(lv.shared_layers(ten, fourteen())) == [0, 1, 2, 3, 4, 5, 13]       # the lowest layer among them
    assert sorted(lv.shared_layers(ten, fifteen())) == [0, 1, 2, 3, 4, 5]
    assert sorted(lv.shared_layers(fourteen(), fifteen())) == list(range(13))


@pytest.mark.parametrize('scale_height, heights, upper, match', [
    (0.0, [600.0], 9, 'scale height'), (-51000.0, [600.0], 9, 'scale height'),
    (float('nan'), [600.0], 9, 'scale height'), ('scenario', [600.0], 9, 'scale height'),
    (True, [600.0], 9, 'scale height'),
    (51000.0, [600.0], 1, 'keeps from 2 to 9'), (51000.0, [600.0], 10, 'keeps from 2 to 9'),
    (51000.0, [600.0], 6.0, 'keeps from 2 to 9'), (51000.0, [600.0], True, 'keeps from 2 to 9'),
    (51000.0, [], 6, 'one or more positive'), (51000.0, [0.0], 9, 'one or more positive'),
    (51000.0, [600.0, -1.0], 9, 'one or more positive'), (51000.0, [float('inf')], 9, 'one or more positive'),
    (51000.0, ['600'], 9, 'one or more positive'), (51000.0, [True], 9, 'one or more positive'),
    (51000.0, 600.0, 9, 'numbers of metres'), (51000.0, [None], 9, 'numbers of metres'),
    (51000.0, [600.0, 3100.0], 6, 'from the highest down'), (51000.0, [600.0, 600.0], 6, 'from the highest down'),
    (51000.0, [23300.0, 600.0], 6, 'at or above'),        # 23.3 km stands on the sixth released half level, 0.6336
    (51000.0, [3100.0, 600.0], 9, 'at or above'),         # above the ninth, 0.9666
    (51000.0, [600.0, 2.0], 9, 'above the ground'),       # 2 m rounds to the ground's 1
    (51000.0, [600.0, 599.0], 9, 'lies below the one before'),   # both round to 0.9883
])
def test_the_rule_refuses_values_it_cannot_place(scale_height, heights, upper, match):
    with pytest.raises(ValueError, match=match):
        lv.generate(scale_height, heights, upper)


def test_half_levels_rise_from_above_zero_to_the_grounds_one():
    assert np.array_equal(lv.check((0.5, 1.0)), [0.5, 1.0])
    for bad in ([1.0], [0.5, 0.9], [0.0, 0.5, 1.0], [0.6, 0.5, 1.0], [0.5, 0.5, 1.0], [0.5, float('nan'), 1.0],
                [[0.5, 1.0]], [0.5, 1.0000001]):
        with pytest.raises(ValueError, match='[Hh]alf levels'):
            lv.check(bad)


# Terluna's sets for the Open Moon.

def test_the_open_moons_values_give_terlunas_fifteen_levels_to_the_digits_terluna_records():
    half = fifteen()
    assert half.size == 15 and MOON == dict(scale_height_m=51000.0, upper=6, interfaces_m=(
        15500.0, 11500.0, 9000.0, 7000.0, 5000.0, 3100.0, 1730.0, 600.0))
    assert [round(float(x), 4) for x in half] == TERLUNA_HALF
    assert np.allclose(lv.full_levels(half), TERLUNA_FULL, rtol=0, atol=1e-15)
    assert list(half[6:12]) == [0.7379, 0.7981, 0.8382, 0.8717, 0.9066, 0.941] and half[13] == 0.9883
    assert np.array_equal(half[:6], lv.plasim_half()[:6])           # the released model's six upper layers
    # Against the doubles of Terluna's module and of its runs' SIGH: thirteen the same, and the last bit of two,
    # 0.3736 and 0.9666, the compiled model's where Terluna's come from numpy's powers.
    theirs = [float(x) for x in TERLUNA_SIGH.split(',')]
    assert [i for i in range(15) if half[i] != theirs[i]] == [3, 12]
    assert [(repr(float(half[i])), repr(theirs[i])) for i in (3, 12)] == [
        ('0.37360000000000004', '0.3736000000000001'), ('0.9666', '0.9666000000000001')]
    assert all(abs(half[i] - theirs[i]) == np.spacing(half[i]) for i in (3, 12))
    # Terluna's heights for the set, at its 51 km: the lowest level at 0.30 km under a layer 0.60 km deep, the next at
    # 1.16 km, and the lowest layer holding 0.54 of the mass of the layer above.
    z = lv.heights_m(lv.full_levels(half), 51000.0)
    found = lv.summary(half, 51000.0)
    assert found['levels'] == 15 and found['half_levels'] == [float(x) for x in half]
    assert found['lowest_level_m'] == pytest.approx(300.0, abs=5.0) and found['lowest_level_m'] == z[14]
    assert found['lowest_layer_m'] == pytest.approx(600.0, abs=5.0) and z[13] == pytest.approx(1160.0, abs=10.0)
    assert found['least_share_of_layer_above'] == pytest.approx(0.54, abs=0.005)
    thick = np.diff(np.r_[0.0, half])
    assert found['least_share_of_layer_above'] == (thick[1:] / thick[:-1]).min() == thick[14] / thick[13]
    assert np.all(thick[1:] / thick[:-1] > 0.5) and np.all(thick[1:] / thick[:-1] < 1.35)   # Terluna's limits


def test_without_the_last_height_the_values_give_terlunas_fourteen():
    half, ten = fourteen(), lv.plasim_half()
    assert [round(float(x), 4) for x in half] == TERLUNA_HALF[:13] + [1.0]
    assert np.array_equal(half[:6], ten[:6]) and half[12] == ten[8]
    assert lv.full_levels(half)[13] == lv.full_levels(ten)[9]                         # the lowest layer and its level
    z = lv.heights_m(lv.full_levels(half), 51000.0) / 1000.0
    for target in (13.5, 8.0, 6.0, 2.4):                    # the levels Terluna asked the set to place, km
        assert np.min(np.abs(z - target)) < 0.05, target
    assert abs(z[6] - 19.24) < 0.01 and abs(z[8] - 10.24) < 0.01 and abs(z[11] - 4.04) < 0.01
    thick = np.diff(np.r_[0.0, half])
    assert np.all(thick[1:] / thick[:-1] > 0.5) and np.all(thick[1:] / thick[:-1] < 1.35)


def test_in_earths_air_the_released_ten_already_stand_where_the_open_moons_fifteen_reach():
    """At Earth's 8.43 km the released ten put the lowest full level at 142 m under a layer 286 m deep, against 859 m
    and 1,732 m at the Open Moon's 51 km, so the rule has nothing to add near Earth's ground: it refuses the Open
    Moon's 600 m layer there, which is deeper than the released model's own, and the Open Moon's heights, which
    stand above the join. The Open Moon's sigma on Earth would put the lowest level near 49 m."""
    ten = lv.plasim_half()
    earth, moon = lv.summary(ten, EARTH_SCALE_HEIGHT_M), lv.summary(ten, 51000.0)
    assert earth['lowest_level_m'] == pytest.approx(142.0, abs=0.5)
    assert earth['lowest_layer_m'] == pytest.approx(286.4, abs=0.5)
    assert moon['lowest_level_m'] == pytest.approx(859.0, abs=0.5)
    assert moon['lowest_layer_m'] == pytest.approx(1732.5, abs=0.5)
    assert earth['least_share_of_layer_above'] == pytest.approx(0.393, abs=5e-4) == moon['least_share_of_layer_above']
    with pytest.raises(ValueError, match='600 m, stands at sigma 0.9313, at or above'):
        lv.generate(EARTH_SCALE_HEIGHT_M, [600.0], 9)
    with pytest.raises(ValueError, match='15500 m, stands at sigma 0.1590, at or above'):
        lv.generate(EARTH_SCALE_HEIGHT_M, MOON['interfaces_m'], MOON['upper'])
    assert lv.summary(fifteen(), EARTH_SCALE_HEIGHT_M)['lowest_level_m'] == pytest.approx(49.5, abs=0.5)
    assert lv.generate(51000.0, [600.0], 9).size == 11          # in the Moon's air the same layer splits the lowest


# The run's entries.

@pytest.mark.parametrize('half', [fifteen(), fourteen()])
def test_a_run_on_a_generated_set_states_its_half_levels_and_plasims_top_friction(half):
    entries = lv.namelist_entries(half)
    assert list(entries) == ['NEQSIG', 'SIGH', 'TFRC'] and entries['NEQSIG'] == -1
    assert entries['SIGH'] == tuple(float(x) for x in half) and all(type(x) is float for x in entries['SIGH'])
    assert [float(repr(x)) for x in entries['SIGH']] == list(half)          # the digits Python writes read back exactly
    assert entries['TFRC'] == (20.0 * 86400.0, 100.0 * 86400.0) + (0.0,) * (half.size - 2)


def test_the_top_friction_belongs_to_the_released_models_two_highest_layers():
    for bad in ([0.5, 1.0], [0.1, 0.2, 0.5, 1.0], np.r_[0.0766, lv.plasim_half()[1:]]):
        with pytest.raises(ValueError, match='friction belongs'):
            lv.namelist_entries(bad)
    with pytest.raises(ValueError, match='alf levels'):
        lv.namelist_entries([0.5, 0.4, 1.0])


# The remap.

def test_the_remap_keeps_column_integrals_reproduces_linear_profiles_and_copies_shared_layers():
    a, b = lv.plasim_half(), fourteen()
    da, db = np.diff(np.r_[0.0, a]), np.diff(np.r_[0.0, b])
    rng = np.random.default_rng(3)
    x = rng.normal(size=(10, 7)) * 50.0 + 250.0
    y = lv.remap(x, a, b)
    assert y.shape == (14, 7)
    assert np.allclose(db @ y, da @ x, rtol=0, atol=1e-11)
    for k, j in lv.shared_layers(a, b).items():
        assert np.array_equal(y[k], x[j])
    fa, fb = lv.full_levels(a), lv.full_levels(b)
    assert np.allclose(lv.remap(2.0 - 3.0 * fa, a, b), 2.0 - 3.0 * fb, atol=1e-13)
    # Each new layer's weights sum to 1, so that a constant, PlaSim's 250 K reference among them, stays a constant.
    assert np.allclose(lv.remap_matrix(a, b).sum(axis=1), 1.0, rtol=0, atol=1e-13)
    # Onto its own set a field comes back as it was, and so along another axis.
    assert np.array_equal(lv.remap(x, a, a), x) and np.array_equal(lv.remap_matrix(b, b), np.eye(14))
    assert np.array_equal(lv.remap(x.T, a, a, axis=1), x.T) and np.allclose(lv.remap(x.T, a, b, axis=1), y.T)
    with pytest.raises(ValueError, match='hold 7 levels'):
        lv.remap(x.T, a, b)
    with pytest.raises(ValueError, match='alf levels'):
        lv.remap_matrix(a, b[:-1])


@pytest.mark.parametrize('source', [lv.plasim_half(), fourteen()])
def test_the_remap_onto_fifteen_levels_keeps_column_integrals_and_splits_only_what_it_must(source):
    a, b = source, fifteen()
    da, db = np.diff(np.r_[0.0, a]), np.diff(np.r_[0.0, b])
    rng = np.random.default_rng(11)
    x = rng.normal(size=(a.size, 9)) * 40.0 + 260.0
    y = lv.remap(x, a, b)
    assert y.shape == (15, 9)
    assert np.allclose(db @ y, da @ x, rtol=0, atol=1e-11)
    for k, j in lv.shared_layers(a, b).items():
        assert np.array_equal(y[k], x[j])
    # Both grids' lowest layer starts at sigma 0.9666, and its two parts on fifteen levels hold its mass-weighted mean.
    assert a[-2] == b[-3]
    assert np.allclose((db[13] * y[13] + db[14] * y[14]) / (db[13] + db[14]), x[-1], atol=1e-11)
    fa, fb = lv.full_levels(a), lv.full_levels(b)
    assert np.allclose(lv.remap(2.0 - 3.0 * fa, a, b), 2.0 - 3.0 * fb, atol=1e-13)


def test_the_remap_takes_a_layers_mean_by_hand():
    """Two equal layers onto four: the old slopes are one-sided, (x2 - x1) / 0.5 in both layers, so the new layers
    hold x1 - d/4, x1 + d/4, x2 - d/4 and x2 + d/4 with d = x2 - x1, and each old layer's mean is kept. Four layers
    onto two take each pair's mean."""
    two, four = np.array([0.5, 1.0]), np.array([0.25, 0.5, 0.75, 1.0])
    x = np.array([10.0, 18.0])
    assert np.allclose(lv.remap(x, two, four), [8.0, 12.0, 16.0, 20.0], rtol=0, atol=1e-13)
    y = np.array([1.0, 2.0, 4.0, 8.0])
    assert np.allclose(lv.remap(y, four, two), [1.5, 6.0], rtol=0, atol=1e-13)


# The restart.

def _restart(path, nlev, records, *, sizes=(506, 32, 64)):
    rows = [('nstep', struct.pack('<i', 12345)), ('nlat', struct.pack('<i', sizes[1])),
            ('nlon', struct.pack('<i', sizes[2])), ('nlev', struct.pack('<i', nlev)),
            ('nrsp', struct.pack('<i', sizes[0]))]
    rows += [(name, np.ascontiguousarray(v, '<f8').tobytes()) for name, v in records]
    lv.write_records(path, rows)


def test_a_restart_is_carried_onto_the_set_with_its_other_records_untouched(tmp_path):
    a, b = lv.plasim_half(), fourteen()
    rng = np.random.default_rng(5)
    st = rng.normal(size=(10, 506))
    aadt = rng.normal(size=(11, 2048))
    dcc = rng.uniform(0.0, 1.0, size=(10, 2048))
    soil = rng.normal(size=(5, 2048))
    months = rng.normal(size=(14, 2048))                # a climatology's 14 months, the size of fourteen levels
    src, dst = tmp_path / 'rest10', tmp_path / 'rest14'
    _restart(src, 10, [('st', st), ('aadt', aadt), ('dcc', dcc), ('dsoilt', soil), ('dtcl', months)])
    report = lv.carry_restart(src, dst, a, b)
    got = {name.strip(): data for name, data in lv.read_records(dst)}
    assert struct.unpack('<i', got['nlev'])[0] == 14 and struct.unpack('<i', got['nstep'])[0] == 12345
    st14 = np.frombuffer(got['st'], '<f8').reshape(14, 506)
    assert np.allclose(np.diff(np.r_[0.0, b]) @ st14, np.diff(np.r_[0.0, a]) @ st, atol=1e-12)
    assert np.array_equal(st14[:6], st[:6]) and np.array_equal(st14[13], st[9])
    aadt14 = np.frombuffer(got['aadt'], '<f8').reshape(15, 2048)
    assert np.array_equal(aadt14[14], aadt[10])                        # the ground's value kept
    dcc14 = np.frombuffer(got['dcc'], '<f8').reshape(14, 2048)
    assert dcc14.min() >= 0.0 and dcc14.max() <= 1.0
    assert got['dsoilt'] == np.ascontiguousarray(soil, '<f8').tobytes()
    assert got['dtcl'] == np.ascontiguousarray(months, '<f8').tobytes()
    assert set(report['fields']) == {'st', 'aadt', 'dcc'} and report['levels'] == [10, 14]
    assert report['fields']['st']['column_integral_change'] < 1e-12 and report['fields']['st']['points'] == 506
    assert len(report['source_sha256']) == len(report['written_sha256']) == 64
    assert not (tmp_path / 'rest14.part').exists()
    # Carried on to fifteen levels, the fourteen months keep their record although fifteen is one level and the ground
    # more: the list of the surface's climatologies names them.
    report = lv.carry_restart(dst, tmp_path / 'rest15', b, fifteen())
    assert report['levels'] == [14, 15] and set(report['fields']) == {'st', 'aadt', 'dcc'}


def test_a_restart_carried_onto_its_own_set_comes_back_byte_for_byte(tmp_path):
    a = fifteen()
    rng = np.random.default_rng(7)
    records = [('sz', rng.normal(size=(15, 506))), ('sqm', rng.normal(size=(15, 506))),
               ('dql', rng.uniform(0.0, 1e-4, size=(15, 2048))), ('aadcc', rng.uniform(0.0, 1.0, size=(16, 2048))),
               ('dls', rng.uniform(0.0, 1.0, size=2048))]
    _restart(tmp_path / 'rest', 15, records)
    report = lv.carry_restart(tmp_path / 'rest', tmp_path / 'same', a, a)
    assert (tmp_path / 'same').read_bytes() == (tmp_path / 'rest').read_bytes()
    assert report['source_sha256'] == report['written_sha256']
    assert all(field['column_integral_change'] == 0.0 for field in report['fields'].values())


def test_a_restart_the_carrier_would_misread_is_refused(tmp_path):
    a, b = lv.plasim_half(), fourteen()
    rng = np.random.default_rng(9)
    good = [('st', rng.normal(size=(10, 506)))]
    _restart(tmp_path / 'good', 10, good)
    # A field sized like one by level that the lists leave out, at the grid's size and at the spectral one, on the
    # restart's own counts: a T42 restart's are 1,892 coefficients and 64 by 128 points.
    for name, values, sizes in (('zzz', rng.normal(size=(10, 2048)), (506, 32, 64)),
                                ('zzz', rng.normal(size=(11, 2048)), (506, 32, 64)),
                                ('zzz', rng.normal(size=(10, 506)), (506, 32, 64)),
                                ('zzz', rng.normal(size=(10, 8192)), (1892, 64, 128))):
        path = tmp_path / f'odd{values.size}'
        _restart(path, 10, [(name, values)], sizes=sizes)
        with pytest.raises(ValueError, match='sized like a field by level'):
            lv.carry_restart(path, tmp_path / 'odd14', a, b)
    _restart(tmp_path / 't42', 10, [('zzz', rng.normal(size=(10, 2048)))], sizes=(1892, 64, 128))
    assert lv.carry_restart(tmp_path / 't42', tmp_path / 't42-14', a, b)['fields'] == {}    # no field of that grid
    with pytest.raises(ValueError, match='holds 10 levels, where the grid it is carried from holds 14'):
        lv.carry_restart(tmp_path / 'good', tmp_path / 'again', b, fifteen())
    lv.carry_restart(tmp_path / 'good', tmp_path / 'there', a, b)
    with pytest.raises(ValueError, match='new path'):
        lv.carry_restart(tmp_path / 'good', tmp_path / 'there', a, b)
    _restart(tmp_path / 'short', 10, [('st', rng.normal(size=(9, 506)))])
    with pytest.raises(ValueError, match='st holds another size'):
        lv.carry_restart(tmp_path / 'short', tmp_path / 'short14', a, b)
    lv.write_records(tmp_path / 'bare', [('nstep', struct.pack('<i', 1)), ('st', b'\0' * 8 * 5060)])
    with pytest.raises(ValueError, match='states nlev once'):
        lv.carry_restart(tmp_path / 'bare', tmp_path / 'bare14', a, b)
    whole = (tmp_path / 'good').read_bytes()
    for cut, match in ((whole[:-3], 'runs past the end'), (whole[:-4] + b'\1\0\0\0', 'closes with another length'),
                       (whole + b'\0\0', 'breaks off'), (whole[:24], 'a name without its data')):
        (tmp_path / 'cut').write_bytes(cut)
        with pytest.raises(ValueError, match=match):
            lv.read_records(tmp_path / 'cut')
