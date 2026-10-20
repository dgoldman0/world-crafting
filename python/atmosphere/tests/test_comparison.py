"""Stage 9's comparison with the paper's figures, on synthetic tables and curves and, where the paper's source is
restored, on its own figures."""
import json
import math

import numpy as np
import pytest

from shared.constants import STEFAN_BOLTZMANN
from atmosphere.radiative_convective import fetch_inputs as column_inputs
from atmosphere.waterworlds import (balance as bl, comparison as cp, escape as es, fetch_inputs, figures as fg, maps,
                                    steam_optics as so)
from atmosphere.waterworlds.body import Waterworld

needs_source = pytest.mark.skipif(fetch_inputs.restore()['status'] != 'PASS',
                                  reason="the paper's source is unrestored (atmosphere.waterworlds.fetch_inputs --download)")
needs_lines = pytest.mark.skipif(column_inputs.restore()['status'] != 'PASS',
                                 reason='spectroscopic inputs not restored (radiative_convective.fetch_inputs --download)')
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


def _result(radiation=1.0, bracket=(0.98, 1.02), missing=False):
    """A comparison whose radiation runs `radiation` times the paper's and whose values bound by the escape stand, at
    the escape's two ends, the bracket's times the paper's and at the other factors at the paper's; one of Figure 2's
    points is missing from the paper, as NaN reads back, and with `missing` one of the lab's."""
    ends = {cp._name(cp.ESCAPE_ENDS[0]): bracket[0], cp._name(cp.ESCAPE_ENDS[1]): bracket[1]}

    def lab(paper, f, escape):
        return paper * (ends.get(cp._name(f), 1.0) if escape else radiation)
    figure2 = dict(rows=[dict(t_s=300.0, paper_emitting=1.1, lab_emitting=1.1 * radiation, paper_absorbing=1.05,
                              lab_absorbing=1.05 * radiation),
                         dict(t_s=250.0, paper_emitting=None, lab_emitting=1.0, paper_absorbing=None,
                              lab_absorbing=1.0)])
    rows3 = []
    for t in (300.0, 450.0, 480.0):                                      # 450 K belongs to the radiation
        row = dict(t_s=t, paper_expanding=1000.0, paper_no_expansion=900.0)
        for f in cp.FACTORS:
            for kind, paper in (('expanding', 1000.0), ('no_expansion', 900.0)):
                row[f'lab_{kind}_{cp._name(f)}'] = lab(paper, f, t > cp.RADIATION_TO_K)
        rows3.append(row)
    if missing:
        rows3[0][f'lab_expanding_{cp._name(cp.FITTED)}'] = None
    lifetimes = {'1e9': dict(paper=445.0, **{f'lab_{cp._name(f)}': lab(445.0, f, True) for f in cp.FACTORS})}

    def star():                                                          # 1.6 m/s^2 belongs to the radiation; the
        return dict(rows=[dict(factor=f, g=g, paper_freezing=1.0,          # widest zone lies at 1.4 m/s^2
                               lab_freezing=lab(1.0, f, g < cp.RADIATION_FROM_G),
                               paper_billion=0.90 if g < 1.5 else 0.95,
                               lab_billion=lab(0.90 if g < 1.5 else 0.95, f, g < cp.RADIATION_FROM_G))
                          for g in (1.4, 1.6, 2.0) for f in cp.FACTORS])

    def figure5(f):
        snow = {a: dict(paper_melt_au=1.0, lab_melt_au_paper_end=radiation, paper_to_k=495.0,
                        lab_to_k_paper_end=lab(495.0, f, True)) for a in ('0.25', '0.32', '0.4')}
        return dict(snowballs=snow, ocean_freeze=dict(paper_au=1.04, lab_au_paper_end=1.04 * radiation))
    figure5s = {cp._name(f): figure5(f) for f in cp.FACTORS}
    figure5s['short_lived_from_k'] = dict(paper=427.0, **{f'lab_{cp._name(f)}': lab(427.0, f, True)
                                                           for f in cp.FACTORS})
    return dict(figure2=figure2, figure3=dict(rows=rows3, lifetimes_k=lifetimes),
                figure4=dict(transition=dict(paper=1.48, **{f'lab_{cp._name(f)}': lab(1.48, f, True)
                                                            for f in cp.FACTORS}), sun=star(), ad_leonis=star()),
                figure5=figure5s)


def test_the_acceptance_check_holds_the_radiation_to_its_tolerances_and_the_escape_to_its_spread():
    within = cp.acceptance(_result(radiation=1.01))
    assert within['passes'] and all(r['passes'] for r in within['rows'].values())
    rows = within['rows']
    assert rows['instellation']['worst'] == pytest.approx(0.01) and rows['instellation']['points'] == 4
    assert rows['distance']['points'] == 2 + 4 + 3 + 1 and within['calibrated']['points'] == 2
    assert rows['factor']['points'] == 2                                 # the paper's missing point left out
    assert rows['escape']['points'] == 1 + 1 + 1 + 2 + 4 + 2 + 1 and rows['escape']['outside'] == []
    assert within['printed']['points'] == 12 and within['widest']['sun']['paper'] == pytest.approx(0.10)
    beyond = cp.acceptance(_result(radiation=1.02))                      # inside 3%, outside 1.5%
    assert beyond['rows']['instellation']['passes'] and not beyond['rows']['distance']['passes']
    assert not beyond['rows']['factor']['passes'] and not beyond['passes']
    gap = cp.acceptance(_result(radiation=1.01, missing=True))['rows']['instellation']
    assert gap['missing'] == ['Figure 3, expanding, 300 K'] and not gap['passes']
    # Both ends above the paper: every value falls outside the bracket, by (1.01 - 1)/1.01 of the nearer end, and the
    # curves, their bracket widened by the radiation's tolerance, inside the widened one.
    shifted = cp.acceptance(_result(bracket=(1.01, 1.05)))['rows']['escape']
    assert len(shifted['outside']) == 12 and shifted['worst'] == pytest.approx(0.01 / 1.01) and not shifted['passes']
    assert len(shifted['outside_widened']) == 1 + 1 + 1 + 2 + 1             # the values bound by the escape alone
    assert shifted['nearest']['margin'] == pytest.approx(-0.01 / 1.01)


@needs_lines
def test_the_comparison_refuses_a_table_whose_optics_key_differs_from_its_own(tmp_path):
    table = dict(schema=cp.tb.SCHEMA, optics=dict(key='0' * 16, source='hitran', hold=False),
                 **{name: [] for name in cp.tb.ARRAYS})
    (tmp_path / 't.json').write_text(json.dumps(table))
    with pytest.raises(SystemExit):
        cp.main(['--store', str(tmp_path), '--table', str(tmp_path / 't.json'), '--figures', str(tmp_path / 'f.json')])


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
    assert [f4['transition'][f'lab_{f:.4f}'] for f in cp.FACTORS] == pytest.approx([1.2916, 1.4800, 1.5198, 1.5749],
                                                                                   abs=2e-4)
    assert set(out['acceptance']['rows']) == {'instellation', 'distance', 'factor', 'escape'}
    assert f4['ganymede']['lab'] == pytest.approx(1.4357, abs=1e-4) and f4['ganymede']['paper'] == pytest.approx(
        1.4279, abs=1e-3)
    assert out['stars']['ad_leonis']['flux_ratio_from_figure_4'] == pytest.approx(0.02417, abs=1e-4)
    assert [r['lab_emitting'] for r in out['figure2']['rows']] == pytest.approx([1.0] * 8)    # a transparent column
