"""Stage 9's comparison with the paper's figures, on synthetic tables and curves and, where the paper's source is
restored, on its own figures."""
import math

import numpy as np
import pytest

from shared.constants import STEFAN_BOLTZMANN
from atmosphere.waterworlds import (balance as bl, comparison as cp, escape as es, fetch_inputs, figures as fg, maps,
                                    steam_optics as so)
from atmosphere.waterworlds.body import Waterworld

needs_source = pytest.mark.skipif(fetch_inputs.restore()['status'] != 'PASS',
                                  reason="the paper's source is unrestored (atmosphere.waterworlds.fetch_inputs --download)")
SUN = maps.Star('sun', 5772.0, 1361.0)


def _table(olr=248.0, lw=1.1, sw=1.02):
    g = [round(1.1 + 0.1 * i, 10) for i in range(16)]
    t = [220.0 + 5 * j for j in range(77)]
    shape = (len(g), len(t))
    olr = np.full(shape, olr) if np.isscalar(olr) else np.tile(np.asarray(olr, dtype=float), (len(g), 1))
    return dict(gravities=g, temperatures=t, stars=[5772.0, 3400.0], olr=olr,
                lw_factor=np.full(shape, lw), sw_factor=np.full((2,) + shape, sw))


def test_the_paper_curve_is_read_between_its_points_and_nan_beyond_them():
    curve = dict(x=[3.0, 1.0, 2.0], y=[30.0, 10.0, 20.0])
    assert cp._paper(curve, 1.5) == pytest.approx(15.0)
    assert np.isnan(cp._paper(curve, 3.5)) and np.isnan(cp._paper(curve, 0.5))


def test_the_red_stars_flux_is_the_square_of_the_ratio_of_its_contours_distance_to_the_suns():
    paper = dict(sun=dict(freezing=dict(g=[1.5, 2.5], d=[1.0, 1.0])),
                 ad_leonis=dict(freezing=dict(g=[1.5, 2.5], d=[0.155, 0.155])))
    assert cp.implied_flux_ratio(paper) == pytest.approx(0.155 ** 2, rel=1e-12)


def test_figure_3s_rows_hold_the_balance_with_and_without_the_factors():
    table = _table()
    curve = dict(x=[250.0, 450.0], y=[1100.0, 1500.0])
    paper = dict(expanding=curve, no_expansion=curve, lifetime_ticks_k={'1e11': 1.0, '1e9': 2.0, '1e7': 3.0},
                 long_lived={})
    out = cp.figure_3(paper, table, SUN)
    world = Waterworld.from_gravity(2.3)
    row = [r for r in out['rows'] if r['t_s'] == 300.0][0]
    assert row['paper_expanding'] == pytest.approx(1200.0)
    for f in cp.FACTORS:
        assert row[f'lab_no_expansion_{f:.4f}'] == pytest.approx((248.0 + bl.escape_power(world, 300.0, f)) / 0.2)
        assert row[f'lab_expanding_{f:.4f}'] == pytest.approx((1.1 * 248.0 + bl.escape_power(world, 300.0, f))
                                                              / (1.02 * 0.2))
    assert math.isnan([r for r in out['rows'] if r['t_s'] == 500.0][0]['paper_expanding'])
    with pytest.raises(ValueError):
        cp.figure_3(paper, table, SUN, gravity=2.35)


def test_figure_5s_snowballs_thaw_into_the_ocean_state_their_flux_holds():
    """On blackbody worlds whose flux rises with temperature, a snowball thaws where its branch reaches the thawing
    temperature, and lands on the water branch's state at the same instellation, found here by bisection."""
    table = _table(olr=STEFAN_BOLTZMANN * np.asarray([220.0 + 5 * j for j in range(77)]) ** 4, lw=1.0, sw=1.0)
    drawn = dict(x=[1.0, 1.1], y=[260.0, 250.0], arrow_au=0.95, end_k=271.0, to_k=330.0)
    paper = dict(short_lived_from_k=427.0, ocean_freeze=dict(arrow_au=1.04, end_k=275.0),
                 **{f'snowball_{a}': drawn for a in (0.25, 0.32, 0.4)}, **{'ocean_0.2': dict(x=[0.9, 1.05],
                                                                                       y=[400.0, 280.0])})
    out = cp.figure_5(paper, table, SUN)
    world, t = Waterworld.from_gravity(2.3), np.asarray(table['temperatures'])
    for label, t_melt in (('273', 273.0), ('paper_end', 271.0)):
        entry = out['1.0000']['snowballs']['0.4']
        f_ice = np.interp(t_melt, t, [bl.instellation(world, x, STEFAN_BOLTZMANN * x ** 4, 1.0, 1.0, albedo=0.4)
                                      for x in t])
        assert entry[f'lab_melt_au_{label}'] == pytest.approx(math.sqrt(1361.0 / f_ice), rel=1e-12)
        f_water = [bl.instellation(world, x, STEFAN_BOLTZMANN * x ** 4, 1.0, 1.0) for x in t]
        lo, hi = 273.0, 600.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if np.interp(mid, t, f_water) < f_ice else (lo, mid)
        assert entry[f'lab_to_k_{label}'] == pytest.approx(lo, abs=1e-6)
    assert out['1.0000']['snowballs']['0.4']['paper_melt_au'] == 0.95
    assert out['1.0000']['ocean_freeze']['paper_au'] == 1.04


class _Clear:
    def layer_cross_sections(self, col, band):
        nu = band.grid.nu
        return nu, np.zeros((len(col['layer_p_pa']), nu.size))


@needs_source
def test_the_whole_comparison_runs_and_the_transition_and_ganymede_stand_as_recorded():
    """The paper's lines at 1.481 and 1.428 m/s^2 against the lab's transitions at the three factors and Ganymede's
    mass on the size relation (notes/waterworlds.md); Figure 2's columns on a narrow transparent band."""
    figures = fg.read_all(fg.source_bytes())
    out = cp.compare(_table(), figures, _Clear(), red_temperature=3400.0, bands=(so.Band(1000.0, 1001.0, 0.5, 2),))
    f4 = out['figure4']
    assert f4['transition']['paper'] == pytest.approx(1.4812, abs=1e-3)
    assert f4['transition']['lab_1.0000'] == pytest.approx(es.lifetime_gravity(273.0, cp.BILLION_YEARS), rel=1e-12)
    assert [f4['transition'][f'lab_{f:.4f}'] for f in cp.FACTORS] == pytest.approx([1.2916, 1.4800, 1.5198], abs=2e-4)
    assert f4['ganymede']['lab'] == pytest.approx(1.4357, abs=1e-4) and f4['ganymede']['paper'] == pytest.approx(
        1.4279, abs=1e-3)
    assert out['stars']['ad_leonis']['flux_ratio_from_figure_4'] == pytest.approx(0.02417, abs=1e-4)
    assert [r['lab_emitting'] for r in out['figure2']['rows']] == pytest.approx([1.0] * 8)    # a transparent column
