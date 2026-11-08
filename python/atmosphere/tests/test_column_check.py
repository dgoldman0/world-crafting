"""Stage 9's check of HITEMP2010's lines on the radiative-convective column's own checked columns: the columns, their
layer optics against the column's own, and the check's reference."""
import numpy as np
import pytest

from atmosphere.radiative_convective import fetch_inputs, optics as ro, spectroscopy as sp
from atmosphere.radiative_convective.thermodynamics import saturation_pressure, species_column
from atmosphere.waterworlds import column_check as cc

needs_lines = pytest.mark.skipif(fetch_inputs.restore()['status'] != 'PASS',
                                 reason='spectroscopic inputs not restored (fetch_inputs --download)')


def test_a_checked_column_is_saturated_over_a_bar_of_nitrogen_at_constant_gravity():
    col = cc.column(cc.PLANETS[0], 300.0)
    assert col['p_pa'][0] == pytest.approx(1e5 + float(saturation_pressure(300.0)), rel=1e-12)
    troposphere = col['t_k'] > 200.0 + 1e-9
    assert np.allclose(col['x_h2o'][troposphere],
                       saturation_pressure(col['t_k'][troposphere]) / col['p_pa'][troposphere], rtol=1e-9)
    assert np.allclose(col['t_k'][~troposphere], 200.0)
    p_trop = col['p_pa'][~troposphere][0]                                 # the stratosphere keeps the tropopause's water
    assert np.allclose(col['x_h2o'][~troposphere], float(saturation_pressure(200.0)) / p_trop, rtol=1e-9)
    assert np.allclose(col['layer_mass_kg_m2'], -np.diff(col['p_pa']) / 9.8, rtol=1e-12)
    moon = cc.column(cc.PLANETS[1], 300.0)
    assert np.array_equal(moon['p_pa'], col['p_pa']) and np.array_equal(moon['t_k'], col['t_k'])


@needs_lines
def test_the_checks_layer_optics_are_the_columns_own_for_water_alone():
    cfg = ro.OpticsConfig(nu_min=1500.0, nu_max=1510.0, molecules=('H2O',), s_min=(('H2O', cc.HITRAN_FLOOR),),
                          cia=False, tabulated=(), processes=1)
    col = cc.column(cc.PLANETS[0], 320.0)
    ro._load(cfg)
    lines = ro._STATE['lines']['H2O']
    sigma = cc.cross_sections(col, lines, grid=cfg.grid)
    water = species_column(col, 'H2O')
    for k in (0, 30, len(water) - 1):
        tau = ro._layer((cfg.grid, cfg, ro.layer_inputs(col)[k]))
        assert np.allclose(sigma[k] * water[k], tau, rtol=1e-12, atol=0)


@needs_lines
def test_the_check_holds_each_line_list_to_the_first():
    lines = sp.load_lines('H2O', cc.HITRAN_FLOOR)
    grid = sp.Grid.span(1500.0, 1505.0, 0.01)
    written = []
    same = cc.check(dict(a=lines, b=lines), temperatures=(250.0,), grid=grid, report=lambda *a, **k: None,
                    written=written.append)
    assert same['passes'] and same['complete'] and same['worst'] == {'b': 0.0} and len(same['rows']) == 2
    assert written == [same]
    assert [r['olr_recorded_on_pyrads_profiles'] for r in same['rows']] == [194.83, 179.63]
    assert same['rows'][0]['a_against_recorded'] == pytest.approx(same['rows'][0]['olr_a'] / 194.83 - 1)
    weaker = sp.LineList('H2O', *(lines.strength * 0.5 if f == 'strength' else getattr(lines, f)
                                  for f in ('nu', 'strength', 'gamma_air', 'gamma_self', 'elower', 'n_air',
                                            'delta_air', 'gid', 'mass')))
    out = cc.check(dict(a=lines, b=weaker), temperatures=(250.0,), grid=grid, report=lambda *a, **k: None)
    assert all(r['difference_b'] > 0 for r in out['rows'])              # weaker lines let more out


def _pyrads():
    """A PyRADS checkout beside the lab's store, where the lab keeps its outside code."""
    from worldlab.roots import root
    store = root('store')
    path = None if store is None else store.parent / 'external' / 'PyRADS'
    return path if path is not None and (path / 'pyrads' / 'SetupGrids.py').is_file() else None


@pytest.mark.skipif(_pyrads() is None, reason='no PyRADS checkout beside the store')
def test_pyrads_columns_take_pyrads_own_levels_and_saturation():
    """PyRADS's 60 levels, up to 1e-4 of the surface's pressure, saturated over liquid water at every temperature, so
    that at 250 K its air holds more water than the column's own, saturated over ice."""
    p, t, x = cc.pyrads_levels(300.0, _pyrads())
    assert len(p) == 60 and np.all(np.diff(p) < 0) and p[-1] == pytest.approx(1e-4 * p[0], rel=1e-9)
    assert t[0] == pytest.approx(300.0, abs=1e-9) and np.allclose(t[t <= 200.0 + 1e-9], 200.0)
    strat = t <= 200.0 + 1e-9
    assert np.allclose(x[strat], x[strat][0], rtol=1e-12)
    cold = cc.column(cc.PLANETS[0], 250.0, _pyrads())
    assert cold['p_pa'][0] - 1e5 > 1.2 * float(saturation_pressure(250.0))
    assert np.allclose(cold['layer_mass_kg_m2'], -np.diff(cold['p_pa']) / 9.8, rtol=1e-12)
