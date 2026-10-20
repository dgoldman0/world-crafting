"""Steam columns over waterworlds: the vapour curve, the shared levels, the lines of hot steam, and the heights at
which the column emits and absorbs."""
import math

import numpy as np
import pytest

from shared.constants import AVOGADRO, STEFAN_BOLTZMANN
from atmosphere.radiative_convective import spectroscopy as sp
from atmosphere.radiative_convective import fetch_inputs
from atmosphere.radiative_convective.thermodynamics import MOLAR_MASS, column_from_levels, saturation_pressure
from atmosphere.waterworlds import escape as es, radiating as rd, steam, steam_optics as so
from atmosphere.waterworlds.body import Waterworld

needs_lines = pytest.mark.skipif(fetch_inputs.restore()['status'] != 'PASS',
                                 reason='spectroscopic inputs not restored (fetch_inputs --download)')


def test_the_saturation_temperature_inverts_the_vapour_curve_over_ice_and_liquid():
    t = np.concatenate([np.linspace(100.0, 273.15, 200), np.linspace(273.17, 646.9, 200)])
    assert np.allclose(steam.saturation_temperature(saturation_pressure(t)), t, rtol=1e-12, atol=0)
    # At the triple point the liquid curve stands 7e-5 Pa above the ice curve; either side inverts to its own branch.
    assert steam.saturation_temperature(saturation_pressure(273.16)) == pytest.approx(273.16, abs=1e-9)
    assert steam.saturation_temperature(saturation_pressure(273.16 - 1e-9)) == pytest.approx(273.16 - 1e-9, abs=1e-11)
    with pytest.raises(ValueError):
        steam.saturation_temperature(1e-20)            # below the ice curve at 100 K, 1.1e-14 Pa


def test_columns_share_their_levels_above_their_lowest_layer():
    levels = steam.Levels()
    cold, hot = levels.pressures(float(saturation_pressure(300.0))), levels.pressures(float(saturation_pressure(450.0)))
    assert cold[0] == saturation_pressure(300.0) and np.all(np.diff(cold) < 0) and np.all(np.diff(hot) < 0)
    assert set(cold[1:].tolist()) <= set(hot.tolist())
    assert cold[-1] == pytest.approx(levels.top_pa, rel=1e-12)
    # No layer thinner than the sliver at the bottom, and none thicker than a grid step but the bottom one, up to one
    # and a half.
    for p in (cold, hot):
        steps = np.log10(p[:-1] / p[1:]) * levels.per_decade
        assert steps.min() >= levels.sliver * levels.per_decade - 1e-9
        assert steps.max() < 1 + levels.sliver * levels.per_decade + 1e-9
    with pytest.raises(ValueError):
        levels.pressures(levels.top_pa)


def test_a_steam_column_follows_the_vapour_curve_and_stands_taller_as_gravity_falls_with_height():
    world = Waterworld.from_gravity(1.8)
    col = steam.column(world, 350.0)
    flat_heights = column_from_levels(world.planet, steam.STEAM_AIR, col['p_pa'], col['t_k'], col['x_h2o'],
                                      constant_gravity=True)['z_m']
    assert np.all(col['z_m'][1:] > flat_heights[1:])
    assert col['t_k'][0] == 350.0 and col['p_pa'][0] == pytest.approx(saturation_pressure(350.0), rel=1e-15)
    assert np.allclose(saturation_pressure(col['t_k'][1:]), col['p_pa'][1:], rtol=1e-10)
    assert np.all(col['x_h2o'] == 1.0) and np.all(np.diff(col['z_m']) > 0)
    # Each layer's mass is its pressure difference over gravity at its middle height.
    g_mid = world.gm_m3_s2 / (world.radius_m + col['layer_z_m']) ** 2
    assert np.allclose(col['layer_mass_kg_m2'], -np.diff(col['p_pa']) / g_mid, rtol=1e-12)
    assert col['layer_column_cm2'] == pytest.approx(col['layer_mass_kg_m2'] / MOLAR_MASS['H2O'] * AVOGADRO * 1e-4)
    # At the surface's gravity the layers hold less mass, their heights unchanged.
    flat = steam.column(world, 350.0, optical_gravity='surface')
    assert np.array_equal(flat['z_m'], col['z_m'])
    assert np.allclose(flat['layer_mass_kg_m2'], -np.diff(col['p_pa']) / world.gravity_m_s2, rtol=1e-12)
    assert np.all(flat['layer_column_cm2'] < col['layer_column_cm2'])
    with pytest.raises(ValueError):
        steam.column(world, 350.0, optical_gravity='flat')


def _grey_column(n=60, p_s=1e5, t=300.0, g=2.0):
    """An isothermal column at constant gravity, levels evenly spaced in log pressure."""
    p = np.exp(np.linspace(math.log(p_s), math.log(1e-2), n + 1))
    h = 8.314462618 * t / (MOLAR_MASS['H2O'] * g)
    z = h * np.log(p_s / p)
    column = -np.diff(p) / g / MOLAR_MASS['H2O'] * AVOGADRO * 1e-4      # molecules per cm^2
    return p, z, column, h


def test_the_unit_depth_height_of_a_grey_column_is_where_its_absorber_above_reaches_one_over_sigma():
    p, z, column, h = _grey_column()
    for sigma in (1e-30, 1e-27, 3e-24, 1e-20):
        tau = (sigma * column)[:, None] * np.ones((1, 3))
        heights, at_top = rd.unit_depth_heights(tau, p, z)
        # The pressure holding 1/sigma molecules per cm^2 above it, the column's top lying at p[-1].
        above = 1.0 / sigma * MOLAR_MASS['H2O'] / AVOGADRO * 1e4 * 2.0 + p[-1]
        expected = h * math.log(p[0] / above) if above < p[0] else 0.0
        assert heights == pytest.approx(np.full(3, expected), rel=1e-9, abs=1e-6)
    tau = np.zeros((len(column), 2))
    tau[-1] = [5.0, 0.5]                                                       # the top layer alone reaches one
    heights, at_top = rd.unit_depth_heights(tau, p, z)
    assert at_top.tolist() == [True, False] and heights[1] == 0.0 and z[-2] < heights[0] < z[-1]


def test_the_planck_mean_of_a_uniform_height_is_that_height_where_the_bands_hold_the_curve():
    nu = sp.Grid.span(1.0, 30000.0, 0.5).nu
    assert rd.planck_mean_height(nu, np.full(nu.size, 1234.0), 300.0) == pytest.approx(1234.0, rel=1e-4)
    # A star at 5772 K puts 12.2% of its light beyond 25,000 cm^-1, where the steam column has no lines.
    nu = sp.Grid.span(1.0, 25000.0, 0.5).nu
    assert rd.planck_mean_height(nu, np.ones(nu.size), 5772.0) == pytest.approx(0.8782, abs=2e-4)
    # Heights of h below 10,000 cm^-1 and 0 above weigh h by the curve's share below 10,000 cm^-1.
    x = sp.C2 * 1e4 / 3400.0
    below = 1 - 15 / math.pi ** 4 * sum(math.exp(-n * x) * (x ** 3 / n + 3 * x ** 2 / n ** 2 + 6 * x / n ** 3
                                                             + 6 / n ** 4) for n in range(1, 60))
    assert rd.planck_mean_height(nu, np.where(nu < 1e4, 500.0, 0.0), 3400.0) == pytest.approx(500.0 * below, rel=1e-4)


class _Clear:
    """Optics of a transparent column."""
    def layer_cross_sections(self, col, band):
        nu = band.grid.nu
        return nu, np.zeros((len(col['layer_p_pa']), nu.size))


def test_a_transparent_column_emits_its_surfaces_blackbody_from_the_surface():
    world = Waterworld.from_gravity(2.0)
    col = steam.column(world, 300.0)
    spectra = rd.column_spectra(col, _Clear(), (so.Band(1.0, 6000.0, 0.5, 4),))
    result = rd.surfaces(col, spectra, (5772.0,))
    assert result['olr'] == pytest.approx(STEFAN_BOLTZMANN * 300.0 ** 4, rel=2e-4)
    assert result['z_lw'] == 0.0 and result['lw_factor'] == 1.0 and result['sw'][5772.0]['factor'] == 1.0


@needs_lines
@pytest.mark.parametrize('t_s', [300.0, 393.0])
def test_the_direct_line_sum_matches_the_multi_mesh_sum_where_both_hold(t_s):
    lines = sp.load_lines('H2O', 1e-30)
    sums = sp.PartitionSums(lines.gid)
    grid = sp.Grid.span(1200.0, 1260.0, 0.01)
    p = float(saturation_pressure(t_s))
    multi = sp.line_absorption(grid, lines, sums, t_s, p, p, pedestal=True)
    direct = so.broad_line_absorption(grid, lines, sums, t_s, p)
    assert np.max(np.abs(direct - multi) / np.maximum(direct, 1e-3 * direct.max())) < 5e-3


@needs_lines
def test_hot_steam_needs_the_direct_sum():
    """At 500 K and 26 bar the multi-mesh far wings' expansion in (gamma/d)^2 loses a third of the lines' absorption
    over 1,200 to 1,260 cm^-1, which the direct sum keeps; below the switch the optics take the multi-mesh sum."""
    lines = sp.load_lines('H2O', 1e-30)
    sums = sp.PartitionSums(lines.gid)
    grid = sp.Grid.span(1200.0, 1260.0, 0.01)
    p = float(saturation_pressure(500.0))
    multi = sp.line_absorption(grid, lines, sums, 500.0, p, p, pedestal=True)
    direct = so.broad_line_absorption(grid, lines, sums, 500.0, p)
    assert multi.sum() / direct.sum() == pytest.approx(0.673, abs=0.01)
    optics = so.SteamOptics(processes=1)
    band = so.Band(1200.0, 1260.0, 0.01, 10)
    with_continuum = optics.cross_section(band, p, 500.0)
    continuum = sp.WaterContinuum().cross_sections(band.grid.nu, 500.0, p, 1.0)[0]
    assert np.allclose(with_continuum, (direct + continuum).astype(np.float32), rtol=1e-6)
    low = float(saturation_pressure(350.0))
    expected = (sp.line_absorption(grid, lines, sums, 350.0, low, low, pedestal=True, cutoff=so.CUTOFF)
                + sp.WaterContinuum().cross_sections(grid.nu, 350.0, low, 1.0)[0])
    assert np.allclose(optics.cross_section(band, low, 350.0), expected.astype(np.float32), rtol=1e-6)


@needs_lines
def test_a_cached_cross_section_is_the_one_computed(tmp_path):
    band = so.Band(1500.0, 1510.0, 0.01, 10)
    cached = so.SteamOptics(cache=tmp_path)
    first = cached.cross_section(band, 1e3, 250.0)
    assert len(list(tmp_path.rglob('*.npy'))) == 1
    assert np.array_equal(cached.cross_section(band, 1e3, 250.0), first)
    assert np.array_equal(so.SteamOptics().cross_section(band, 1e3, 250.0), first)
    # The key follows the continuum switch, and so the lines alone sit apart.
    assert so.SteamOptics(cache=tmp_path, continuum=False).path(band, 1e3, 250.0) != cached.path(band, 1e3, 250.0)


@needs_lines
def test_the_held_continuum_is_mt_ckds_own_up_to_296_k_and_keeps_its_296_k_coefficients_above():
    """At the continuum's 10 cm^-1 nodes, where its interpolation returns the node's value, the held continuum at 450 K
    is the 296 K coefficients times the layer's own density and radiation term."""
    band = so.Band(1100.0, 1110.0, 0.01, 10)
    plain, held = so.SteamOptics(), so.SteamOptics(hold=True)
    assert held.key != plain.key and held.describe()['hold'] and not plain.describe()['hold']
    assert np.array_equal(held.cross_section(band, 1e3, 250.0), plain.cross_section(band, 1e3, 250.0))
    assert np.array_equal(held.cross_section(band, 1e3, 296.0), plain.cross_section(band, 1e3, 296.0))
    nodes, p, t = np.array([1100.0, 1110.0, 1120.0]), 1e4, 450.0
    at_296 = plain.continuum.cross_sections(nodes, 296.0, p, 1.0)[0]
    rad = sp.WaterContinuum.radiation_term
    expected = at_296 * (296.0 / t) * rad(nodes, t) / rad(nodes, 296.0)
    assert held.held.cross_sections(nodes, t, p, 1.0)[0] == pytest.approx(expected, rel=1e-12)
    assert np.all(plain.continuum.cross_sections(nodes, t, p, 1.0)[0] < 0.5 * expected)   # MT_CKD 4.3 weakens
    grid = band.grid
    expected = (sp.line_absorption(grid, held.lines, held.sums, t, p, p, pedestal=True, cutoff=so.CUTOFF,
                                   coarse_factor=band.coarse_factor)
                + held.held.cross_sections(grid.nu, t, p, 1.0)[0])
    assert np.allclose(held.cross_section(band, p, t), expected.astype(np.float32), rtol=1e-6)
    with pytest.raises(ValueError):
        so.SteamOptics(hold=True, continuum=False)
    with pytest.raises(ValueError):
        so.SteamOptics(lines='hitran2016')


def test_two_transparent_bands_join_at_3500_cm1_without_counting_it_twice():
    col = steam.column(Waterworld.from_gravity(2.0), 300.0, steam.Levels(top_pa=1.0, per_decade=4))
    result = rd.surfaces(col, rd.column_spectra(col, _Clear(), so.BANDS), (5772.0,))
    assert result['olr'] == pytest.approx(STEFAN_BOLTZMANN * 300.0 ** 4, rel=1e-8)


def test_a_column_ends_below_the_critical_radius_where_the_grids_top_lies_beyond_it():
    low, high = Waterworld.from_gravity(1.15), Waterworld.from_gravity(2.3)
    capped = steam.column(low, 500.0)
    assert capped['capped'] and low.radius_m + capped['z_m'][-1] < es.critical_radius(low, 500.0)
    assert capped['top_pa'] > steam.Levels().top_pa
    full = steam.column(high, 300.0)
    assert not full['capped'] and full['top_pa'] == pytest.approx(steam.Levels().top_pa, rel=1e-12)
