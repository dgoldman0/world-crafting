"""The energy balance of steam waterworlds, the table of their columns over gravity and surface temperature, and
the contours that follow from it."""
import math

import numpy as np
import pytest

from shared.constants import STEFAN_BOLTZMANN
from atmosphere.radiative_convective import fetch_inputs
from atmosphere.radiative_convective.thermodynamics import latent_heat
from atmosphere.waterworlds import (balance as bl, escape as es, maps, radiating as rd, steam, steam_optics as so,
                                    steam_table as tb)
from atmosphere.waterworlds.body import Waterworld

needs_lines = pytest.mark.skipif(fetch_inputs.restore()['status'] != 'PASS',
                                 reason='spectroscopic inputs not restored (fetch_inputs --download)')
BILLION_YEARS = 1e9 * es.YEAR_S


def test_the_instellation_holds_the_balance_of_eq_2():
    world, t_s = Waterworld.from_gravity(2.3), 480.0
    olr, lw, sw = 249.0, 1.4, 1.2
    f = bl.instellation(world, t_s, olr, lw, sw, factor=4 / 3)
    power = (world.gravity_m_s2 * world.radius_m + bl.escape_heat(t_s)) * es.mass_flux(world, t_s, 4 / 3)
    assert bl.escape_power(world, t_s, 4 / 3) == pytest.approx(power, rel=1e-14)
    # eq. 2: (r_SW/r_s)^2 (1 - A) F / 4 - (g r + L) Phi = (r_LW/r_s)^2 F_out
    assert sw * (1 - bl.ALBEDO) * f / 4 - power == pytest.approx(lw * olr, rel=1e-12)
    cold = bl.instellation(world, 250.0, 200.0, 1.0, 1.0)      # a cold world's wind carries too little to count
    assert cold == pytest.approx(4 * 200.0 / 0.8, rel=1e-12)


@pytest.mark.parametrize('t, table_kj_kg', [(373.124, 2256.4), (500.0, 1827.4), (600.0, 1172.7)])
def test_the_heat_of_vaporisation_follows_the_steam_tables(t, table_kj_kg):
    """IAPWS-95's saturation tables give these heats of vaporisation; the ideal gas's Clausius-Clapeyron slope gives
    2,293, 2,143 and 2,158 kJ/kg."""
    assert bl.escape_heat(t) / 1e3 == pytest.approx(table_kj_kg, rel=1e-3)


def test_over_ice_the_heat_is_the_ice_curves_sublimation():
    assert bl.escape_heat(250.0) == pytest.approx(float(latent_heat(250.0)), rel=1e-14)
    assert bl.escape_heat(250.0) > bl.escape_heat(273.16) + 3e5


def test_steady_temperatures_are_every_crossing_of_the_curve_and_each_exact_meeting_once():
    t = np.array([250.0, 260.0, 270.0, 280.0, 290.0])
    f = np.array([1000.0, 1100.0, 1050.0, 1200.0, 1300.0])
    assert bl.steady_temperatures(1075.0, t, f) == pytest.approx([257.5, 265.0, 270.0 + 5 / 3])
    assert bl.steady_temperatures(1250.0, t, f) == pytest.approx([285.0])
    assert bl.steady_temperatures(900.0, t, f) == []
    assert bl.steady_temperatures(1100.0, t, f) == pytest.approx([260.0, 270.0 + 10 / 3])
    assert bl.steady_temperatures(1300.0, t, f) == pytest.approx([290.0])


def test_the_hysteresis_takes_each_branch_on_its_side_of_freezing():
    """At 2.3 m/s^2 with an ice albedo of 0.4 the curves jump from about 2,000 W/m^2 on ice to 1,600 on water; split
    into branches, the steady states lie on each side of 273 K, with no root on the jump between them."""
    t = np.arange(255.0, 300.0, 5.0)
    water = np.linspace(1500.0, 1700.0, t.size)
    ice = water * 0.8 / 0.6
    states = bl.branch_temperatures(2050.0, t, water, ice)
    assert states['water'] == [] and len(states['ice']) == 1 and states['ice'][0] < bl.FREEZING_K
    states = bl.branch_temperatures(1610.0, t, water, ice)
    assert len(states['water']) == 1 and states['water'][0] >= bl.FREEZING_K and states['ice'] == []


def _synthetic_table(gravities, temperatures, *, stars=(5772.0, 3400.0)):
    """A table of blackbody surfaces, the outgoing longwave sigma T^4, with factors that differ between the
    surfaces and the stars."""
    shape = (len(gravities), len(temperatures))
    olr = np.tile(STEFAN_BOLTZMANN * np.asarray(temperatures) ** 4, (len(gravities), 1))
    return dict(gravities=list(gravities), temperatures=list(temperatures), stars=list(stars), olr=olr,
                lw_factor=np.full(shape, 1.10), z_lw=np.zeros(shape), lw_top_share=np.zeros(shape),
                sw_factor=np.stack([np.full(shape, 1.02), np.full(shape, 1.05)]), z_sw=np.zeros((2,) + shape),
                sw_top_share=np.zeros((2,) + shape))


def test_the_instellation_takes_each_stars_absorbing_factor_and_refuses_a_star_the_table_lacks():
    table = _synthetic_table([1.5, 2.0], [250.0, 260.0])
    world = Waterworld.from_gravity(2.0)
    for star, sw in ((maps.Star('sun', 5772.0, 1361.0), 1.02), (maps.Star('red', 3400.0, 32.7), 1.05)):
        f = maps.instellations(table, star)
        expected = (1.10 * STEFAN_BOLTZMANN * 260.0 ** 4 + bl.escape_power(world, 260.0)) / (sw * 0.8 / 4)
        assert f[1, 1] == pytest.approx(expected, rel=1e-13)
    with pytest.raises(ValueError):
        maps.instellations(table, maps.Star('other', 3414.0, 30.9))


def test_the_273_k_contour_of_blackbody_worlds_meets_its_closed_form():
    table = _synthetic_table([1.5, 2.0], list(np.arange(250.0, 300.0, 1.0)))
    sun = maps.Star('sun', 5772.0, 1361.0)
    d = maps.contour_distance(table, sun, [273.0, 273.0])
    for i, g in enumerate(table['gravities']):
        world = Waterworld.from_gravity(g)
        f = (1.10 * STEFAN_BOLTZMANN * 273.0 ** 4 + bl.escape_power(world, 273.0)) / (1.02 * 0.8 / 4)
        assert d[i] == pytest.approx(math.sqrt(1361.0 / f), rel=1e-4)
    outside = maps.contour_distance(table, sun, [200.0, math.nan])
    assert np.isnan(outside).all()


def test_the_lifetime_temperatures_invert_the_wind_and_leave_nan_where_none_lies_in_the_bracket():
    temps = maps.lifetime_temperatures([1.5, 2.3], BILLION_YEARS)
    for g, t in zip((1.5, 2.3), temps):
        assert es.water_lifetime(Waterworld.from_gravity(g), t) == pytest.approx(BILLION_YEARS, rel=1e-6)
    printed = es.lifetime_gravity(273.0, BILLION_YEARS)                   # 1.29 m/s^2, the printed transition
    assert maps.lifetime_temperatures([printed], BILLION_YEARS)[0] == pytest.approx(273.0, abs=1e-6)
    # At 2.6 m/s^2 the water outlasts a billion years even at 640 K, by the printed equations.
    assert np.isnan(maps.lifetime_temperatures([2.6], BILLION_YEARS)[0])


def test_a_grid_stops_at_or_below_its_end_and_refuses_a_backward_step():
    assert tb.span('1.1:1.4:0.1') == [1.1, 1.2, 1.3, 1.4]
    assert tb.span('220:603:5')[-1] == 600.0 and tb.span('1.1:2.66:0.1')[-1] == 2.6
    for text in ('1:2:0', '2:1:0.1', '1:2:-0.1'):
        with pytest.raises(ValueError):
            tb.span(text)


def test_a_table_reads_back_as_written_and_its_key_follows_its_inputs(tmp_path):
    table = _synthetic_table([1.5], [250.0, 260.0])
    table.update(schema=tb.SCHEMA, levels={}, bands=[], optics={}, optical_gravity='surface', n_angles=4,
                 producer=tb.producer())
    digest = tb.write(tmp_path / 't.json', {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in table.items()})
    back = tb.read(tmp_path / 't.json')
    assert len(digest) == 64 and np.array_equal(back['olr'], table['olr'])
    assert tb.key(back) == tb.key(table) and tb.key(dict(table, gravities=[1.6])) != tb.key(table)
    assert tb.key(dict(table, producer=dict(table['producer'], environment={}))) != tb.key(table)
    (tmp_path / 'other.json').write_text('{"schema": "other"}')
    with pytest.raises(ValueError):
        tb.read(tmp_path / 'other.json')
    with pytest.raises(SystemExit):
        tb.main(['--out', str(tmp_path / 'x.json')])                        # the cache is missing


@needs_lines
def test_the_table_holds_each_columns_surfaces_in_and_out_of_process(tmp_path):
    band = so.Band(1000.0, 1010.0, 0.01, 10)
    levels = steam.Levels(top_pa=1e-2, per_decade=5)
    grid = dict(gravities=[1.15, 2.3], temperatures=[300.0, 500.0], stars=[5772.0], levels=levels, bands=(band,))
    lines = []
    table = tb.compute(**grid, cache=tmp_path, processes=1, report=lambda *a, **k: lines.append(a))
    cached = sorted(tmp_path.rglob('*.npy'))
    pooled = tb.compute(**grid, cache=tmp_path, processes=2, report=lambda *a, **k: None)
    assert sorted(tmp_path.rglob('*.npy')) == cached                      # the second table computed nothing anew
    assert table['failed'] == [] and len(lines) == 1 + 4                    # the fill, then one line a column
    for name in tb.ARRAYS:
        assert np.array_equal(np.asarray(table[name]), np.asarray(pooled[name]))
    assert steam.column(Waterworld.from_gravity(1.15), 500.0, levels)['capped']
    optics = so.SteamOptics(cache=tmp_path)
    for i, g in enumerate(grid['gravities']):
        for j, t_s in enumerate(grid['temperatures']):
            col = steam.column(Waterworld.from_gravity(g), t_s, levels, optical_gravity='surface')
            r = rd.surfaces(col, rd.column_spectra(col, optics, (band,)), (5772.0,))
            assert table['olr'][i][j] == pytest.approx(r['olr'], rel=1e-12)
            assert table['sw_factor'][0][i][j] == pytest.approx(r['sw'][5772.0]['factor'], rel=1e-12)
