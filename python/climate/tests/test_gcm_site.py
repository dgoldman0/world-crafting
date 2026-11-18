"""The forcing of a CM1 box from a GCM run at a site (climate/crm/gcm_site.py): the spherical harmonics it
differentiates with, the continuity that gives its vertical wind, the fits by local time, the cells it takes, the
remap onto CM1's levels, the convection's top, the held air and the proposed refusal; the whole extraction on
synthetic year files written as PlaSim writes them, at the Moon's constants and at Earth's; the case's files read back
as CM1 reads them; and, where Terluna's research drive is at hand, the forcing of Terluna's sea box on its design years,
from the same run read in place.

Brought from Terluna's climate/tests/test_gcm_site.py at 39c5ee04 (python/provenance.json): its tests of the
harmonics, the continuity, the fits, the cells, the remap, the column's pressure, the convection's top, the table on
CM1's levels and the wind's windows are kept, adapted to the lab's arguments; the others are the lab's, and Terluna's
tests on its branch run and of the GCM's weather at a site stay in Terluna."""
import io
import json
import math
import re
from pathlib import Path

import numpy as np
import pytest
from scipy.special import assoc_legendre_p_all

from climate.crm import gcm_site as gs

# netCDF4 sets the shape of the arrays it is given to write, which numpy 2.5 deprecates; the warning comes from its code.
pytestmark = pytest.mark.filterwarnings('ignore:Setting the shape on a NumPy array:DeprecationWarning')

NLAT, NLON, RADIUS = 32, 64, 1.7374e6


def grid(nlat=NLAT, nlon=NLON):
    nodes, _ = np.polynomial.legendre.leggauss(nlat)
    mu = np.sort(nodes)[::-1]                                               # rows north to south
    return np.degrees(np.arcsin(mu)), np.arange(nlon) * 360.0 / nlon, mu


# Terluna's tests, adapted.

def test_the_harmonics_give_back_a_harmonic_and_its_derivatives():
    sp = gs.Spectral(NLAT, NLON, 21)
    lat, lon, mu = grid()
    lam = np.radians(lon)
    p = np.asarray(assoc_legendre_p_all(21, 21, mu, norm=True, diff_n=1))
    for n, m in ((0, 0), (3, 1), (7, 4), (15, 2), (21, 21)):
        f = p[0, n, m][:, None] * np.cos(m * lam)[None, :]
        s = sp.analyse(f)
        scale = np.abs(p[1, n, m]).max() + 1.0
        assert np.allclose(sp.synthesise(s), f, atol=1e-10)
        assert np.allclose(sp.synthesise(s, 'lambda'), -m * p[0, n, m][:, None] * np.sin(m * lam)[None, :], atol=1e-9)
        assert np.allclose(sp.synthesise(s, 'mu'), p[1, n, m][:, None] * np.cos(m * lam)[None, :], atol=1e-10 * scale)
    # A harmonic beyond the truncation projects to nothing.
    beyond = p[0, 21, 3][:, None] * np.cos(3 * lam)[None, :]
    assert np.allclose(gs.Spectral(NLAT, NLON, 20).project(beyond), 0.0, atol=1e-10)
    with pytest.raises(ValueError, match='resolves no triangular truncation'):
        gs.Spectral(NLAT, NLON, 32)


def test_continuity_turns_a_rotating_flow_away_and_finds_a_spreading_one():
    sp, wind = gs.Spectral(NLAT, NLON, 21), gs.Spectral(NLAT, NLON, 22)
    lat, lon, mu = grid()
    phi = np.radians(lat)
    half = [0.2, 0.6, 0.8, 1.0]                                             # full levels 0.1, 0.4, 0.7, 0.9
    sigma = gs.full_levels(half)
    assert np.allclose(sigma, [0.1, 0.4, 0.7, 0.9])
    ps = np.full((1, NLAT, NLON), 1.2e5)
    shape = (1, sigma.size, NLAT, NLON)
    turning = np.broadcast_to((10.0 * np.cos(phi))[None, None, :, None], shape)
    assert np.abs(gs.omega(turning, np.zeros(shape), ps, half, RADIUS, sp, wind)).max() < 1e-9
    # v = cos(phi) sin(phi): div = (1/a) d(v cos)/d(mu) = (1 - 3 mu^2)/a at every level, so omega = -p div.
    spreading = np.broadcast_to((np.cos(phi) * np.sin(phi))[None, None, :, None], shape)
    expected = -(sigma[None, :, None, None] * ps[:, None]) * ((1.0 - 3.0 * mu**2) / RADIUS)[None, None, :, None]
    assert np.allclose(gs.omega(np.zeros(shape), spreading, ps, half, RADIUS, sp, wind), expected, rtol=1e-8,
                       atol=1e-14)
    # Across a surface pressure that rises northward, ln ps = ln P0 + a mu, a northward wind V_k cos(phi) differing by
    # level carries v.grad(ln ps) = V_k a (1 - mu^2) / R beside its divergence -2 V_k mu / R, and omega sums both from
    # the top: omega_k = ps (sigma_k g_k - sum over the layers above of (d + g) dsigma - (d_k + g_k)(sigma_k - e_k)).
    a, speeds = 0.01, np.array([3.0, -1.0, 2.0, 0.5])
    sloping = np.broadcast_to((1.2e5 * np.exp(a * mu))[None, :, None], (1, NLAT, NLON))
    flow = np.broadcast_to(speeds[None, :, None, None] * np.cos(phi)[None, None, :, None], shape)
    g = speeds[:, None] * a * (1.0 - mu**2)[None, :] / RADIUS                  # (lev, lat)
    d = -2.0 * speeds[:, None] * mu[None, :] / RADIUS
    e = gs.edges(half)
    above = np.cumsum((d + g) * np.diff(e)[:, None], axis=0) - (d + g) * np.diff(e)[:, None]
    by_hand = (1.2e5 * np.exp(a * mu))[None, :] * (sigma[:, None] * g - above - (d + g) * (sigma - e[:-1])[:, None])
    got = gs.omega(np.zeros(shape), flow, sloping, half, RADIUS, sp, wind)[0]
    assert np.allclose(got, np.broadcast_to(by_hand[:, :, None], got.shape), rtol=1e-8, atol=1e-12)


def test_the_fits_undo_a_mean_over_a_window_and_give_the_rate():
    for window in (36.0, 36.318272):
        centres = np.arange(10) * window - 162.0
        truth = lambda h: (2.0 + 0.5 * np.cos(np.radians(h)) - 0.3 * np.sin(np.radians(3 * h))
                           + 0.1 * np.cos(np.radians(4 * h)))
        damp = lambda n: np.sin(np.radians(window / 2.0 * n)) / np.radians(window / 2.0 * n)
        means = (2.0 + 0.5 * damp(1) * np.cos(np.radians(centres)) - 0.3 * damp(3) * np.sin(np.radians(3 * centres))
                 + 0.1 * damp(4) * np.cos(np.radians(4 * centres)))
        coef = gs.undamped(gs.harmonic_coefficients(centres, means), window)
        hours = np.linspace(-180.0, 180.0, 37)
        assert np.allclose(gs.evaluate(coef, hours), truth(hours), atol=1e-12)
        day = 2.55e6
        expected = (-0.5 * np.sin(np.radians(hours)) - 0.9 * np.cos(np.radians(3 * hours))
                    - 0.4 * np.sin(np.radians(4 * hours))) * 2.0 * np.pi / day
        assert np.allclose(gs.rate(coef, hours, day), expected, atol=1e-17)
    # Snapshots need no undoing: the plain fit gives them back.
    assert np.allclose(gs.evaluate(gs.harmonic_coefficients(centres, truth(centres)), hours), truth(hours), atol=1e-12)
    assert np.allclose(gs.bin_hours(36), np.arange(36) * 10.0 - 175.0)                # core patch 17's bin centres


def test_the_cells_are_the_sites_surface():
    lat, lon = np.array([10.0, 5.0, 0.0, -5.0, -10.0]), np.arange(0.0, 360.0, 5.0)
    lsm = np.zeros((5, 72), bool)
    lsm[:, :3] = True                                                        # land from 0 to 10 E
    height = np.zeros((5, 72))
    height[2, 71] = 300.0                                                    # a raised lake at 355 E
    site = dict(lat_deg=0.0, lon_deg=0.0, half_lat_deg=5.0, half_lon_deg=5.0)
    land = gs.site_cells(lat, lon, lsm, height, dict(site, surface='land'))
    sea = gs.site_cells(lat, lon, lsm, height, dict(site, surface='sea'))
    assert land.sum() == 6 and set(np.nonzero(land)[1]) == {0, 1}
    assert sea.sum() == 2 and set(np.nonzero(sea)[1]) == {71}                # the lake stands above the sea
    with pytest.raises(ValueError):
        gs.site_cells(lat, lon, lsm, height, dict(site, surface='ice'))
    with pytest.raises(ValueError):
        gs.site_cells(lat, lon, np.ones((5, 72), bool), height, dict(site, surface='sea'))
    for bad in (dict(site, surface='ice'), dict(site, surface='sea', radius_m=1.0), dict(site),
                dict(site, surface='sea', half_lat_deg=0.0)):
        with pytest.raises(ValueError):
            gs.check_site(bad)
    for name, recorded in gs.TERLUNA_OPEN_MOON_SITES.items():
        assert gs.check_site(recorded) == recorded, name


def box_forcing():
    """A three-level GCM column and its circulation by two hours of the day, the top level's moistening nil."""
    return dict(profile=dict(z_m=[60000.0, 20000.0, 4000.0], theta_k=[500.0, 340.0, 300.0],
                             specific_humidity_kg_kg=[1e-6, 2e-4, 0.015], u_m_s=[1.0, 2.0, 3.0],
                             v_m_s=[0.0, 0.0, -1.0]),
                vertical_wind_m_s=[0.001, 0.003, 0.002], half_levels=[0.4, 0.8, 1.0],
                surface=dict(pressure_pa=1.2e5),
                circulation=dict(hour_angle_deg=[-90.0, 90.0], theta_k_s=[[1e-6, 1e-5, 2e-5], [-1e-6, -1e-5, -2e-5]],
                                 specific_humidity_kg_kg_s=[[0.0, 1e-9, 1e-8], [0.0, -1e-9, -1e-8]]))


def test_on_the_boxs_levels_each_gcm_layer_keeps_its_total_and_the_mean_winds_advection_is_added_back():
    zw = np.linspace(0.0, 150000.0, 301)
    theta_at = lambda z: 280.0 + 0.004 * np.asarray(z)
    qv_at = lambda z: 0.012 * np.exp(-np.asarray(z) / 3000.0)
    forcing = box_forcing()
    out = gs.to_cm1(forcing, zw, dict(theta_at=theta_at, qv_at=qv_at), 1.62)
    zh = 0.5 * (zw[1:] + zw[:-1])
    w = 0.5 * (np.asarray(out['w_m_s'])[1:] + np.asarray(out['w_m_s'])[:-1])
    table = out['table']
    assert np.allclose(table['z_m'], zh)
    assert out['w_m_s'][0] == 0.0 and out['w_m_s'][-1] == 0.0
    assert np.interp(4000.0, zw, out['w_m_s']) == pytest.approx(0.002)
    p = out['pressure_pa']
    assert p[0] == pytest.approx(1.2e5) and np.all(np.diff(p) < 0.0)
    # Less CM1's own advection of its starting air by the mean wind, what is left is each GCM layer's by pressure.
    edges = gs.edges(forcing['half_levels']) * 1.2e5
    left_th = np.asarray(table['theta_k_s']) - (w * 0.004)[None, :]
    assert np.allclose(left_th, gs.remap(forcing['circulation']['theta_k_s'], edges, p), rtol=1e-9, atol=1e-15)
    assert np.allclose(out['circulation']['theta_k_s'], left_th, rtol=1e-9, atol=1e-15)
    # The vapour: the GCM's moistening in specific humidity, carried into CM1's mixing ratio by (1 + r).
    r0 = qv_at(zh)
    left_q = (np.asarray(table['qv_kg_kg_s']) - w[None, :] * np.gradient(r0, zh)[None, :]) / (1.0 + r0)[None, :]
    assert np.allclose(left_q, gs.remap(forcing['circulation']['specific_humidity_kg_kg_s'], edges, p), rtol=1e-9,
                       atol=1e-20)
    # The column's moistening is the GCM's: the dry mass of each of CM1's layers, its mass over (1 + r), gains in
    # mixing ratio what the GCM's layers gain in specific humidity; the top layer, in part above CM1's top,
    # moistens nothing.
    gcm = (np.asarray(forcing['circulation']['specific_humidity_kg_kg_s']) * np.diff(edges)).sum(axis=1)
    dry = -np.diff(p) / (1.0 + r0)
    cm1 = ((np.asarray(table['qv_kg_kg_s']) - w[None, :] * np.gradient(r0, zh)[None, :]) * dry[None, :]).sum(axis=1)
    assert np.allclose(cm1, gcm, rtol=1e-6)
    assert 0.0 < out['mass_above_top_share'] < 0.4 / 1.2


def test_a_box_whose_top_stands_below_the_gcms_top_level_takes_the_column_below_it():
    zw = np.linspace(0.0, 30000.0, 61)
    air = dict(theta_at=lambda z: 280.0 + 0.004 * np.asarray(z), qv_at=lambda z: np.zeros(np.shape(z)))
    forcing = box_forcing()
    # The middle layer, which the box's top cuts, holds a peak, so its slope is nil and the part within the box holds
    # its value times the pressure it spans there.
    forcing['circulation']['theta_k_s'] = [[1e-5, 3e-5, 2e-5], [-1e-5, -3e-5, -2e-5]]
    out = gs.to_cm1(forcing, zw, air, 1.62)
    assert out['w_m_s'][-1] == 0.0 and np.interp(20000.0, zw, out['w_m_s']) == pytest.approx(0.003)
    p = out['pressure_pa']
    assert out['mass_above_top_share'] == pytest.approx(p[-1] / 1.2e5) and 0.4 < p[-1] / 1.2e5 < 0.8
    edges = gs.edges([0.4, 0.8, 1.0]) * 1.2e5
    kept = (np.asarray(out['circulation']['theta_k_s']) * -np.diff(p)).sum(axis=1)
    thick = np.clip(edges[1:], p[-1], None) - np.clip(edges[:-1], p[-1], None)
    assert np.allclose(kept, (np.asarray(forcing['circulation']['theta_k_s']) * thick).sum(axis=1), rtol=1e-9)
    with pytest.raises(ValueError, match="w levels"):
        gs.to_cm1(box_forcing(), [10.0, 100.0, 200.0], air, 1.62)


def test_the_remap_keeps_each_layers_total_a_straight_line_and_no_new_extremes():
    edges = np.array([0.0, 2e4, 5e4, 8e4, 1e5, 1.2e5])
    targets = np.linspace(1.2e5, 0.0, 241)                                   # the ground up, 500 Pa layers
    width = -np.diff(targets)
    values = np.array([[3.0, -1.0, 2.0, 5.0, 4.0]])
    out = gs.remap(values, edges, targets)
    for k in range(5):
        inside = (targets[1:] >= edges[k]) & (targets[:-1] <= edges[k + 1])
        assert (out[0, inside] * width[inside]).sum() == pytest.approx(values[0, k] * (edges[k + 1] - edges[k]))
    assert out.min() >= values.min() - 1e-12 and out.max() <= values.max() + 1e-12
    # A field linear in pressure comes back as the line in the inner layers, flat in the top and bottom ones.
    mid = 0.5 * (edges[1:] + edges[:-1])
    line = gs.remap(2.0 + 1e-4 * mid, edges, targets)
    centres = 0.5 * (targets[1:] + targets[:-1])
    inner = (centres > edges[1]) & (centres < edges[-2])
    assert np.allclose(line[inner], 2.0 + 1e-4 * centres[inner])
    assert np.allclose(line[centres > edges[-2]], 2.0 + 1e-4 * mid[-1])
    # Where a layer's neighbours rise unevenly the slope is the centred one, within twice the smaller one-sided slope
    # (the monotonized-central limit): values 0, 1 and 3 on even layers give the middle layer the slope 1.5 a layer.
    even = np.linspace(0.0, 3e4, 4)
    fine = np.linspace(3e4, 0.0, 61)
    out = gs.remap(np.array([0.0, 1.0, 3.0]), even, fine)
    middle = (0.5 * (fine[1:] + fine[:-1]) > 1e4) & (0.5 * (fine[1:] + fine[:-1]) < 2e4)
    assert np.allclose(out[middle], 1.0 + 1.5 * (0.5 * (fine[1:] + fine[:-1])[middle] - 1.5e4) / 1e4)
    steep = gs.remap(np.array([0.0, 1.0, 9.0]), even, fine)                  # the centred slope, 4.5, limited to 2
    assert np.allclose(steep[middle], 1.0 + 2.0 * (0.5 * (fine[1:] + fine[:-1])[middle] - 1.5e4) / 1e4)


def test_the_columns_pressure_falls_as_cm1_integrates_its_sounding():
    zw = np.linspace(0.0, 30000.0, 31)
    flat = lambda value: (lambda z: np.full(np.shape(z), value))
    p = gs.column_pressures(zw, flat(300.0), flat(0.0), 1.2e5, 1.62)
    exner = (1.2e5 / 1e5)**gs.CM1_KAPPA - 1.62 * zw / (gs.CM1_CP * 300.0)
    assert np.allclose(p, 1e5 * exner**(1.0 / gs.CM1_KAPPA), rtol=1e-10)
    # With vapour the air is lighter by CM1's virtual temperature, theta (1 + r Rv/Rd) / (1 + r).
    p = gs.column_pressures(zw, flat(300.0), flat(0.02), 1.2e5, 1.62)
    thv = 300.0 * (1.0 + 0.02 * 461.5 / 287.04) / 1.02
    assert gs.virtual_theta(300.0, 0.02) == pytest.approx(thv, rel=1e-15)
    exner = (1.2e5 / 1e5)**gs.CM1_KAPPA - 1.62 * zw / (gs.CM1_CP * thv)
    assert np.allclose(p, 1e5 * exner**(1.0 / gs.CM1_KAPPA), rtol=1e-10)
    assert gs.mixing_ratio(0.02) == pytest.approx(0.02 / 0.98, rel=1e-15)


def test_the_convection_top_is_the_lowest_level_with_under_one_percent_above_it():
    z = [129e3, 93e3, 72e3, 55e3, 41e3]
    out = gs.convection_top([0.0, 0.012, 0.194, 0.69, 2.6], z)
    assert (out['level'], out['top_m'], out['held_from_m'], out['held_fully_from_m']) == (2, 72e3, 93e3, 129e3)
    out = gs.convection_top([0.0, 0.5, 0.3, 0.2, 0.0], z)
    assert (out['level'], out['held_from_m'], out['held_fully_from_m']) == (1, 129e3, None)
    out = gs.convection_top([0.5, 0.2, 0.3, 0.0, 0.0], z)                 # to the top level: nothing above to hold
    assert (out['level'], out['held_from_m'], out['held_fully_from_m']) == (0, None, None)
    with pytest.raises(ValueError):
        gs.convection_top([0.0] * 5, z)


def test_the_held_air_starts_above_the_convection_and_a_damping_layer_below_it_is_refused():
    convection = gs.convection_top([0.0, 0.012, 0.194, 0.69, 2.6], [129e3, 93e3, 72e3, 55e3, 41e3])
    assert gs.held_heights(convection, 150e3) == dict(var14=93e3, var15=129e3)
    # Terluna's boxes: the damping from 0.77 of a 150 km top, 115.5 km, 22.5 km above the GCM's next level.
    assert gs.check_damping(convection, 0.77 * 150e3) == pytest.approx(22.5e3)
    assert gs.check_damping(convection, 93e3) == 0.0                          # at the level itself: kept
    with pytest.raises(ValueError, match='refused \\(proposed rule'):
        gs.check_damping(convection, 92.9e3)
    upper = gs.convection_top([0.0, 0.5, 0.3, 0.2, 0.0], [129e3, 93e3, 72e3, 55e3, 41e3])
    assert gs.held_heights(upper, 150e3) == dict(var14=129e3, var15=150e3)    # fully from the box's top
    assert gs.held_heights(convection, 110e3) == dict(var14=93e3, var15=110e3)
    with pytest.raises(ValueError, match='stands below'):
        gs.held_heights(convection, 90e3)
    deep = gs.convection_top([0.5, 0.2, 0.3, 0.0, 0.0], [129e3, 93e3, 72e3, 55e3, 41e3])
    assert gs.damping_clearance_m(deep, 1e9) == -math.inf
    with pytest.raises(ValueError, match='reaches its top level'):
        gs.check_damping(deep, 1e9)
    with pytest.raises(ValueError, match='no air above it'):
        gs.held_heights(deep, 150e3)


def test_the_wind_windows_follow_the_day():
    hours = (np.arange(36) + 0.5) * 10.0 - 180.0
    wind = dict(hour_angle_deg=hours.tolist(), z_m=[20000.0, 800.0],
                u_m_s=[[0.0, float(np.cos(np.radians(h)))] for h in hours], v_m_s=[[0.0, 0.0] for _ in hours])
    day = 36.0 * 1000.0
    windows = gs.wind_windows(dict(wind_by_hour=wind), np.array([0.0, 800.0, 20000.0]), -90.0, day, 2.5 * day)
    assert len(windows) == 90 and windows[0]['time_s'] == (0.0, 1000.0)
    assert [w['hour_angle_deg'] for w in windows[:3]] == pytest.approx([-85.0, -75.0, -65.0])
    for w in windows[:40]:
        assert w['u_m_s'][0] == pytest.approx(np.cos(np.radians(w['hour_angle_deg'])))    # held down to the ground
        assert w['u_m_s'][1] == pytest.approx(np.cos(np.radians(w['hour_angle_deg'])))
    assert windows[36]['hour_angle_deg'] == pytest.approx(windows[0]['hour_angle_deg'])  # a day later, the same
    assert all(a['time_s'][1] == b['time_s'][0] for a, b in zip(windows, windows[1:]))     # contiguous
    assert len(gs.wind_windows(dict(wind_by_hour=wind), np.array([0.0]), -90.0, day, 2.0 * day)) == 72


# A GCM run written as PlaSim writes its year files, on a T5 grid of 8 x 16 cells and five levels, its records means
# over window_deg of hour angle. At every cell the air's temperature follows T_k + A_k cos(h) + S_k sin(h) through the
# day and its wind (U_k + U1 cos(h)) cos(latitude), a flow turning with the globe; the humidity follows
# Q_k + B_k cos(h), each record holding its value at its interval's start, the first record of each file the remnant a
# restart leaves; the precipitable water is the humidity's column, its records true means, with constant rain and
# evaporation; the physics heats each level by D_k cos(h) in its snapshots at the records' ends, with a wave of
# wavenumber 8 beside it that the run's T5 harmonics leave out, and moistens nothing; and convection heats the lowest
# three levels. h is the hour angle at the site, which grows by window_deg each record. So the circulation's heating,
# moistening and wind by local time are known by hand.

T5, NLAT5, NLON5 = 5, 8, 16
HALF5 = [0.15, 0.4, 0.7, 0.9, 1.0]
T_K = np.array([220.0, 250.0, 275.0, 290.0, 300.0])
A_K = np.array([0.5, 1.0, 1.5, 2.0, 3.0])
S_K = np.array([0.2, -0.4, 0.6, -0.8, 1.0])
D_K = np.array([1e-6, -2e-6, 3e-6, 4e-6, -5e-6])                 # K/s
Q_K = np.array([1e-6, 1e-4, 2e-3, 8e-3, 1.4e-2])
B_K = np.array([0.0, 2e-5, 3e-4, 6e-4, 9e-4])
U_K = np.array([20.0, 10.0, 5.0, 3.0, 2.0])
U1, RAIN, EVAP = 1.5, 3e-8, 4e-8                                  # m/s, m/s, m/s
CONV = np.array([0.0, 0.0, 1e-5, 2e-5, 3e-5])                  # K/s
P_HPA, RECORDS = 1000.0, 22
SEA5 = dict(lat_deg=-10.0, lon_deg=-45.0, half_lat_deg=25.0, half_lon_deg=25.0, surface='sea')
MOON = dict(gravity=1.6242, radius=1.7374e6, gas=288.38, day=29.53059 * 86400.0, nstpw=143, mpstep=30.0)
EARTH = dict(gravity=9.80665, radius=6.371e6, gas=287.05, day=86400.0, nstpw=4, mpstep=36.0)


def layer_mass(world):
    return P_HPA * 100.0 * np.diff(gs.edges(HALF5)) / world['gravity']


def write_run(folder, world, years=2, *, still=False, drop=None, lev=None, true_mean=(), spread=None):
    """A synthetic run's model folder: its namelists, its surface geopotential and its year files; the years in
    true_mean also write the humidity's true mean, hus_mean. With spread, a meridional wind spread (level) sin(2
    latitude) (1 + cos(h)) away from the equator's low levels, written as means over the windows, gives the run a
    vertical wind that swings through the day."""
    netCDF4 = pytest.importorskip('netCDF4')
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'planet_namelist').write_text(
        f" &planet_nl\n GA = {world['gravity']!r} \n PLARAD = {world['radius']!r} \n GASCON = {world['gas']!r} \n"
        " /END\n")
    (folder / 'plasim_namelist').write_text(
        f" &plasim_nl\n NEQSIG  =  -1 \n SIGH = {','.join(repr(x) for x in HALF5)} \n NSTPW  =  {world['nstpw']} \n"
        f" MPSTEP  =  {world['mpstep']!r} \n /END\n")
    lat, lon, _ = grid(NLAT5, NLON5)
    lsm = np.zeros((NLAT5, NLON5))
    lsm[:, :4] = 1.0                                                          # land from 0 to 67.5 E
    height = np.where(lsm > 0, 500.0, 0.0)
    height[4, 13] = 30.0                                                      # a raised lake within the site's box
    values = ' '.join(f'{v:.3f}' for v in (height * world['gravity']).ravel())
    (folder / 'topography.sra').write_text(f'       129         0  20090101         0        {NLON5}         {NLAT5}'
                                           f'         0         0\n{values}\n')
    window = 360.0 * world['nstpw'] * world['mpstep'] * 60.0 / world['day']
    d1 = math.sin(math.radians(window / 2.0)) / math.radians(window / 2.0)
    full, mass = gs.full_levels(HALF5), layer_mass(world)
    for year in range(years):
        index = year * RECORDS + np.arange(RECORDS)
        hour = -170.0 + (0.0 if still else window) * (index + 0.5)           # the site's hour angle at each centre
        subsolar = SEA5['lon_deg'] - hour
        with netCDF4.Dataset(folder / f'MOST.{year:05d}.nc', 'w') as d:
            for name, size in (('time', None), ('lev', 5), ('lat', NLAT5), ('lon', NLON5), ('modes', 21)):
                d.createDimension(name, size)
            d.createVariable('lat', 'f8', ('lat',))[:] = lat
            d.createVariable('lon', 'f8', ('lon',))[:] = lon
            d.createVariable('lev', 'f4', ('lev',))[:] = full if lev is None else lev
            d.createVariable('time', 'f8', ('time',))[:] = index + 1.0
            def field(name, value, levels=True):
                if name == drop:
                    return
                dims = ('time', 'lev', 'lat', 'lon') if levels else ('time', 'lat', 'lon')
                shape = (RECORDS, 5, NLAT5, NLON5) if levels else (RECORDS, NLAT5, NLON5)
                d.createVariable(name, 'f8', dims)[:] = np.broadcast_to(value, shape)
            cos_lat = np.cos(np.radians(lat))[None, None, :, None]
            mean_cos = (d1 * np.cos(np.radians(hour)))[:, None, None, None]   # a cosine's mean over each window
            start_cos = np.cos(np.radians(hour - window / 2.0))[:, None, None, None]
            mean_sin = (d1 * np.sin(np.radians(hour)))[:, None, None, None]
            end_cos = np.cos(np.radians(hour + window / 2.0))[:, None, None, None]
            field('ta', T_K[None, :, None, None] + A_K[None, :, None, None] * mean_cos
                  + S_K[None, :, None, None] * mean_sin)
            held = Q_K[None, :, None, None] + B_K[None, :, None, None] * start_cos
            held[0] *= 0.02                                                   # the restart's remnant
            field('hus', held)
            if year in true_mean:
                field('hus_mean', Q_K[None, :, None, None] + B_K[None, :, None, None] * mean_cos)
            field('ua', (U_K[None, :, None, None] + U1 * mean_cos) * cos_lat)
            field('va', 0.0 if spread is None else np.asarray(spread)[None, :, None, None]
                  * np.sin(2.0 * np.radians(lat))[None, None, :, None] * (1.0 + mean_cos))
            field('dt_diab', D_K[None, :, None, None] * end_cos
                  + 1e-5 * np.cos(np.radians(8.0 * lon))[None, None, None, :])
            field('dq_dyn', 0.0)
            field('dt_conv', CONV[None, :, None, None])
            field('dt_lsp', 0.0)
            field('ps', P_HPA, False)
            field('ts', 301.0, False)
            field('tas', 299.5, False)
            czen = np.maximum(0.0, np.cos(np.radians(lat))[None, :, None]
                              * np.cos(np.radians(lon[None, None, :] - subsolar[:, None, None])))
            field('czen', czen, False)
            field('pr', RAIN, False)
            field('evap', -EVAP, False)
            field('prw', Q_K @ mass + (B_K @ mass) * mean_cos[:, 0], False)
            field('mrso', 0.1, False)
            field('lsm', lsm[None], False)
    return gs.run_record(folder, folder / 'topography.sra', solar_day_s=world['day'])


def kept_centres(window, years=2):
    """The hour angles at the centres of the records the rule keeps, 1 to n-2 of each file."""
    index = np.concatenate([year * RECORDS + np.arange(1, RECORDS - 1) for year in range(years)])
    return -170.0 + window * (index + 0.5)


def moistening_by_hand(world, b_k):
    """The circulation's moistening by local time (kg/kg/s): the humidity's own change, its daily harmonic b_k, the
    physics being nil, and the column's difference from the exact means, here the rain less the evaporation, spread
    over the levels by the vapour each holds."""
    hours = np.radians(gs.bin_hours(36))
    q_h = Q_K[None, :] + b_k[None, :] * np.cos(hours)[:, None]
    rest = 1000.0 * (RAIN - EVAP) - ((B_K - b_k) @ layer_mass(world)) * np.sin(hours) * 2.0 * math.pi / world['day']
    return -b_k[None, :] * np.sin(hours)[:, None] * 2.0 * math.pi / world['day'] + rest[:, None] * q_h / (
        q_h @ layer_mass(world))[:, None]


@pytest.mark.parametrize('world', [MOON, EARTH], ids=['moon', 'earth'])
def test_the_extraction_gives_a_written_runs_circulation_by_hand(tmp_path, world):
    run = write_run(tmp_path / 'model', world)
    assert run['gravity_m_s2'] == world['gravity'] and run['radius_m'] == world['radius']
    assert run['gas_constant_j_kg_k'] == world['gas'] and run['half_levels'] == HALF5
    assert run['heat_capacity_j_kg_k'] == pytest.approx(world['gas'] / 0.286)
    window = run['window_deg']
    assert window == pytest.approx(360.0 * world['nstpw'] * world['mpstep'] * 60.0 / world['day'])
    f = gs.site_forcing(run, (0, 1), SEA5)
    assert f['truncation'] == T5 and f['records'] == 2 * (RECORDS - 2) and f['phases'] == 10
    assert f['humidity_filter'] == 'ends'
    # The site's cells: sea at sea level within the box, the raised lake and the land left out.
    lat, lon, _ = grid(NLAT5, NLON5)
    assert len(f['cells']) == 8 and [float(lat[4]), float(lon[13])] not in f['cells']
    assert {lo for _, lo in f['cells']} == {292.5, 315.0, 337.5} and f['cell_heights_m'] == [0.0] * 8
    hours = gs.bin_hours(36)
    sigma = gs.full_levels(HALF5)
    exner = (sigma * P_HPA * 100.0 / 1e5)**gs.CM1_KAPPA
    day, mass = world['day'], layer_mass(world)
    # The circulation's heating is the air's own change less the physics' at its snapshots' hours, the wave beyond the
    # harmonics left out: ((S cos(h) - A sin(h)) 2 pi / day - D cos(h)) / exner.
    h = np.radians(hours)[:, None]
    heat = (((S_K * np.cos(h) - A_K * np.sin(h)) * 2.0 * math.pi / day - D_K * np.cos(h)) / exner)
    assert np.allclose(f['circulation']['theta_k_s'], heat, rtol=1e-9, atol=1e-12 * np.abs(heat).max())
    # The column's vapour is held to the exact means, and the rule's means, undone by their own filter, give the
    # humidity's daily harmonic whole.
    exact = -(B_K @ mass) * np.sin(np.radians(hours)) * 2.0 * math.pi / day + 1000.0 * (RAIN - EVAP)
    column = f['budget']['column_vapour_mm_day']
    assert np.allclose(column['exact_by_hour'], exact * 86400.0, rtol=1e-9)
    assert np.allclose(column['held_by_hour'], column['exact_by_hour'], rtol=1e-12)
    moist = moistening_by_hand(world, B_K)
    assert np.allclose(f['circulation']['specific_humidity_kg_kg_s'], moist, rtol=1e-9,
                       atol=1e-12 * np.abs(moist).max())
    # The humidity's mean: the rule's means, the first record's remnant left out.
    centres = kept_centres(window)
    half_window = math.radians(window / 2.0)
    assert np.allclose(f['profile']['specific_humidity_kg_kg'],
                       Q_K + B_K * math.cos(half_window) * np.cos(np.radians(centres)).mean(), rtol=1e-12)
    # The wind turns with the globe, so continuity finds no vertical wind; its diurnal part comes back undamped.
    weights = np.cos(np.radians([c[0] for c in f['cells']]))
    mean_cos = (weights * weights).sum() / weights.sum()
    assert np.abs(f['vertical_wind_m_s']).max() < 1e-12
    assert np.allclose(f['wind_by_hour']['u_m_s'], (U_K[None, :] + U1 * np.cos(np.radians(hours))[:, None]) * mean_cos,
                       rtol=1e-9)
    # Heights by the hypsometric rule in the run's gas constant, from each record's virtual temperatures.
    d1 = math.sin(half_window) / half_window
    c = np.cos(np.radians(centres))[:, None]
    sn = np.sin(np.radians(centres))[:, None]
    tv = (T_K + A_K * d1 * c + S_K * d1 * sn) * (1.0 + (461.51 / world['gas'] - 1.0) * (Q_K + B_K * math.cos(
        half_window) * c))
    z = np.empty(tv.shape)
    z[:, -1] = world['gas'] * tv[:, -1] / world['gravity'] * math.log(1.0 / sigma[-1])
    for k in range(3, -1, -1):
        z[:, k] = z[:, k + 1] + world['gas'] * 0.5 * (tv[:, k] + tv[:, k + 1]) / world['gravity'] * math.log(
            sigma[k + 1] / sigma[k])
    assert np.allclose(f['profile']['z_m'], z.mean(axis=0), rtol=1e-12)
    # Convection forms its rain in the lowest three levels: its top the third level, the air held from the second.
    formed = CONV * world['gas'] / 0.286 * P_HPA * 100.0 * np.diff(gs.edges(HALF5)) / (world['gravity'] * 2.5008e6)
    assert np.allclose(f['convection']['convective_rain_formed_mm_day'], formed * 86400.0, rtol=1e-12)
    assert (f['convection']['level'], f['convection']['held_from_m']) == (2, pytest.approx(z.mean(0)[1], rel=1e-12))
    assert f['surface'] == pytest.approx(dict(pressure_pa=P_HPA * 100.0, ground_k=301.0, air_2m_k=299.5, wetness=0.5,
                                              height_m=0.0), rel=1e-12)


def test_the_humiditys_fit_undoes_the_filter_its_records_carry(tmp_path):
    """Read by the rule, the humidity's records are averages of their intervals' two ends, which damp its daily
    harmonic by cos(x) where a true mean damps it by sin(x)/x; undone as true means, as Terluna's module undoes them,
    the harmonic comes back short by the ratio, 0.967 for a mean over 36.3 degrees. A run that writes the true mean
    gives the harmonic whole by the mean's own filter, and years that mix the two are refused."""
    rule = gs.site_forcing(write_run(tmp_path / 'rule', MOON), (0, 1), SEA5)
    as_means = gs.site_forcing(write_run(tmp_path / 'rule', MOON), (0, 1), SEA5, humidity_filter='mean')
    x = math.radians(rule['window_deg'] / 2.0)
    short = math.cos(x) / (math.sin(x) / x)
    assert short == pytest.approx(0.967, abs=1e-3) and as_means['humidity_filter'] == 'mean'
    assert np.allclose(as_means['circulation']['specific_humidity_kg_kg_s'], moistening_by_hand(MOON, B_K * short),
                       rtol=1e-9, atol=1e-20)
    assert np.allclose(as_means['circulation']['theta_k_s'], rule['circulation']['theta_k_s'], rtol=0, atol=0)
    true = gs.site_forcing(write_run(tmp_path / 'true', MOON, true_mean=(0, 1)), (0, 1), SEA5)
    assert true['humidity_filter'] == 'mean' and true['records'] == 2 * RECORDS
    assert np.allclose(true['circulation']['specific_humidity_kg_kg_s'], moistening_by_hand(MOON, B_K), rtol=1e-9,
                       atol=1e-20)
    with pytest.raises(ValueError, match='mix files'):
        gs.site_forcing(write_run(tmp_path / 'mixed', MOON, true_mean=(1,)), (0, 1), SEA5)
    with pytest.raises(ValueError, match="humidity's filter"):
        gs.site_forcing(write_run(tmp_path / 'rule', MOON), (0, 1), SEA5, humidity_filter='snapshot')
    coef = np.array([1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    assert gs.undamped(coef, 36.0, kind='ends')[1] == pytest.approx(0.5 / math.cos(math.radians(18.0)), rel=1e-15)
    with pytest.raises(ValueError, match='two ends'):
        gs.undamped(coef, 36.0, kind='snapshot')


def test_the_extraction_refuses_what_it_cannot_fit_or_read(tmp_path):
    with pytest.raises(ValueError, match="too few"):
        gs.site_forcing(write_run(tmp_path / 'still', MOON, still=True), (0, 1), SEA5)       # a Sun that stands still
    with pytest.raises(ValueError, match="lacks \\['dq_dyn'\\]"):
        gs.site_forcing(write_run(tmp_path / 'dry', MOON, years=1, drop='dq_dyn'), (0, 0), SEA5)
    with pytest.raises(ValueError, match='lie off the full levels'):
        gs.site_forcing(write_run(tmp_path / 'lev', MOON, years=1, lev=gs.full_levels(HALF5) * 1.01), (0, 0), SEA5)
    run = write_run(tmp_path / 'model', MOON, years=1)
    with pytest.raises(ValueError, match='shorter than a 9th of the day'):
        gs.site_forcing(dict(run, window_deg=45.0), (0, 0), SEA5)
    with pytest.raises(ValueError, match="surface's heights"):
        gs.site_forcing(dict(run, surface_height_m=[[0.0]]), (0, 0), SEA5)
    with pytest.raises(ValueError, match='truncated at T5'):
        gs.site_forcing(run, (0, 0), SEA5, truncation=4)
    with pytest.raises(ValueError, match='carry no fit'):
        gs.site_forcing(run, (0, 0), SEA5, harmonics=4, bins=8)
    with pytest.raises(ValueError, match='no land cells|no sea cells'):
        gs.site_forcing(run, (0, 0), dict(SEA5, lat_deg=80.0, half_lat_deg=1.0))
    (tmp_path / 'model' / 'plasim_namelist').write_text(' &plasim_nl\n NSTPW = 143 \n MPSTEP = 30.0 \n /END\n')
    with pytest.raises(ValueError, match="state the run's half levels"):
        gs.run_record(tmp_path / 'model', tmp_path / 'model' / 'topography.sra', solar_day_s=MOON['day'])
    assert gs.run_record(tmp_path / 'model', tmp_path / 'model' / 'topography.sra', solar_day_s=MOON['day'],
                         half_levels=HALF5)['half_levels'] == HALF5
    (tmp_path / 'model' / 'planet_namelist').write_text(' &planet_nl\n GA = 1.62 \n /END\n')
    with pytest.raises(ValueError, match='PLARAD, GASCON'):
        gs.run_record(tmp_path / 'model', tmp_path / 'model' / 'topography.sra', solar_day_s=MOON['day'])


# The box's air and the case's files.

def test_the_reference_air_is_the_gcms_in_cm1s_variables():
    f = box_forcing()
    air = gs.reference_air(f, 1.62, 150000.0)
    z = np.array([0.0, 4000.0, 12000.0, 20000.0, 60000.0, 80000.0])
    assert np.allclose(air['theta_at'](z), [300.0, 300.0, 320.0, 340.0, 500.0, 580.0])     # along the top slope above
    r = gs.mixing_ratio(f['profile']['specific_humidity_kg_kg'])[::-1]
    assert np.allclose(air['qv_at'](np.array([0.0, 4000.0, 20000.0, 60000.0])), [r[0], r[0], r[1], r[2]], rtol=1e-12)
    assert air['qv_at'](12000.0) == pytest.approx(math.sqrt(r[0] * r[1]), rel=1e-12)       # linear in the logarithm
    assert np.allclose(air['u_at'](z[:3]), [3.0, 3.0, 2.5])
    # Above the GCM's top level the vapour keeps that level's share of saturation, here 1e-6 kg/kg at 60 km.
    from atmosphere.radiative_convective.thermodynamics import saturation_pressure
    zz = np.linspace(0.0, 150000.0 * 1.01, 4001)
    inv = 1.0 / gs.virtual_theta(air['theta_at'](zz), air['qv_at'](zz))
    exner = (1.2e5 / 1e5)**gs.CM1_KAPPA - 1.62 / gs.CM1_CP * np.r_[0.0, np.cumsum(0.5 * (inv[1:] + inv[:-1])
                                                                                    * np.diff(zz))]
    p, t = 1e5 * exner**(1.0 / gs.CM1_KAPPA), air['theta_at'](zz) * exner
    share = lambda q: q * p / (gs.CM1_RD / gs.CM1_RV + q) / saturation_pressure(t)
    above = zz > 60000.0
    assert np.allclose(share(air['qv_at'](zz))[above], np.interp(60000.0, zz, share(air['qv_at'](zz))), rtol=1e-6)


def read_lsadv(text):
    """terluna_lsadv.txt as core patch 17 reads it: the counts, the heights, then a theta line and a vapour line a
    bin."""
    lines = text.splitlines()
    nb, nl = (int(x) for x in lines[0].split())
    assert len(lines) == 2 + 2 * nb
    th = np.array([lines[2 + 2 * b].split() for b in range(nb)], float)
    qv = np.array([lines[3 + 2 * b].split() for b in range(nb)], float)
    return np.array(lines[1].split(), float), th, qv


def read_nudging(text):
    """An lsnudge_NNNN.dat as lsnudge.F reads it: a line, the two times, two lines, then five columns a level."""
    lines = text.splitlines()
    t1, t2 = (float(x) for x in lines[1].split())
    return t1, t2, np.array([[float(x) for x in line.split()] for line in lines[4:]])


def test_the_case_takes_its_files_and_entries_as_cm1_reads_them(tmp_path):
    run = write_run(tmp_path / 'model', MOON)
    f = gs.site_forcing(run, (0, 1), SEA5)
    zw = np.r_[0.0, np.cumsum(np.full(60, 2500.0))]                         # a 150 km box of 60 layers
    air = gs.reference_air(f, run['gravity_m_s2'], zw[-1])
    held_from = f['convection']['held_from_m']
    case = gs.case_inputs(f, zw, air, gravity_m_s2=run['gravity_m_s2'], start_hour_deg=-90.0,
                          solar_day_s=run['solar_day_s'], length_s=2.0 * run['solar_day_s'],
                          damping_base_m=held_from + 1.0, nudge_tau_s=259200.0)
    names = sorted(case['files'])
    assert names == ['lsnudge_%04d.dat' % i for i in range(1, 73)] + ['terluna_lsadv.txt', 'terluna_wls.txt']
    wls = np.loadtxt(io.StringIO(case['files']['terluna_wls.txt']), skiprows=1)
    assert case['files']['terluna_wls.txt'].startswith('61\n') and np.allclose(wls[:, 0], zw)
    assert np.allclose(wls[:, 1], case['cm1']['w_m_s'], rtol=1e-6, atol=1e-12) and wls[0, 1] == wls[-1, 1] == 0.0
    z, th, qv = read_lsadv(case['files']['terluna_lsadv.txt'])
    assert th.shape == qv.shape == (36, 60) and np.allclose(z, 0.5 * (zw[1:] + zw[:-1]))
    assert np.allclose(th, case['cm1']['table']['theta_k_s'], rtol=1e-6, atol=1e-30)
    assert np.allclose(qv, case['cm1']['table']['qv_kg_kg_s'], rtol=1e-6, atol=1e-30)
    heights = np.r_[0.0, z, zw[-1]]
    times = []
    for i, window in enumerate(case['windows'], 1):
        t1, t2, rows = read_nudging(case['files'][f'lsnudge_{i:04d}.dat'])
        times.append((t1, t2))
        assert np.allclose(rows[:, 0], heights) and rows.shape == (62, 5)
        assert np.allclose(rows[:, 1], air['theta_at'](heights), atol=1e-4)                # every window: the mean air
        assert np.allclose(rows[:, 2], air['qv_at'](heights) * 1000.0, atol=1e-6)          # g/kg of mixing ratio
        assert np.allclose(rows[:, 3], window['u_m_s'], atol=1e-4) and np.allclose(rows[:, 4], 0.0, atol=1e-4)
    assert times[0][0] == 0.0 and times[-1][1] == 1.0e30
    # Each window ends where the next begins, to the seven figures CM1's file gives the end (Terluna's format).
    assert all(abs(a[1] - b[0]) <= 5e-7 * a[1] for a, b in zip(times, times[1:]))
    # The entries: the table, the mean wind and the held air's heights in &param8, and the nudging in &param19.
    p8, p19 = case['namelist']['param8'], case['namelist']['param19']
    assert p8 == dict(var11=1.0, var13=1.0, var14=held_from, var15=f['convection']['held_fully_from_m'], var18=-90.0,
                      var19=round(run['solar_day_s'], 1))
    assert p19 == dict(do_lsnudge=True, do_lsnudge_u=True, do_lsnudge_v=True, do_lsnudge_th=True, do_lsnudge_qv=True,
                       lsnudge_tau=259200.0, lsnudge_start=1.0, lsnudge_end=1.0e12, lsnudge_ramp_time=0.0)
    record = case['record']
    assert record['held']['damping_clearance_m'] == pytest.approx(1.0) and record['wind']['windows'] == 72
    json.dumps(record)                                                         # the record a case keeps is JSON
    # The entries of patch 09 of the lab's CM1 series in &param3, by default: the wind relaxed on its own 2 hours and
    # pulled from the GCM's lowest level, to 0.1 m, and the windows' air drawn in where the mean wind converges; and
    # patch 12's, the window held by the step's time.
    lowest = f['profile']['z_m'][-1]
    assert 0.0 < lowest < zw[-1] and lowest != round(lowest, 1)
    assert case['namelist']['param3'] == dict(wind_nudge_tau=7200.0, wind_nudge_zmin=round(lowest, 1), inflow_ref_air=1,
                                              nudge_window_by_time=1)
    assert record['windows']['by_time'] is True
    wind, inflow = record['wind'], record['inflow']
    assert (wind['nudge_tau_s'], wind['pulled_from_m'], wind['pulled_from']) == (7200.0, round(lowest, 1),
                                                                                "the GCM's lowest level")
    assert wind['window_s'] == pytest.approx(run['solar_day_s'] / 36.0, rel=1e-12)
    assert wind['nudge_tau_share_of_window'] == pytest.approx(7200.0 / wind['window_s'], rel=1e-12)
    assert 0.1 < wind['nudge_tau_share_of_window'] < 0.11                     # a tenth of the Moon's window
    assert inflow['on'] is True and inflow['rates_file'] == 'lab_inflow_rate.txt'
    # A case states its own: another time, the pull from the ground, the inflow off; the files stay as they were.
    common = dict(gravity_m_s2=run['gravity_m_s2'], start_hour_deg=-90.0, solar_day_s=run['solar_day_s'],
                  nudge_tau_s=259200.0)
    same = dict(length_s=2.0 * run['solar_day_s'], damping_base_m=held_from + 1.0, **common)
    stated = gs.case_inputs(f, zw, air, wind_nudge_tau_s=3600.0, wind_from_m=0.0, inflow=False, **same)
    assert stated['namelist']['param3'] == dict(wind_nudge_tau=3600.0, wind_nudge_zmin=0.0, inflow_ref_air=0,
                                                nudge_window_by_time=1)
    assert stated['record']['wind']['pulled_from'] == 'stated' and stated['record']['inflow']['on'] is False
    assert stated['files'] == case['files'] and stated['namelist']['param8'] == p8
    assert gs.case_inputs(f, zw, air, wind_from_m=312.7, **same)['namelist']['param3']['wind_nudge_zmin'] == 312.7
    # The refusals: the damping below the held air (proposed), more windows than CM1 reads, a wind's time of zero or
    # less, and a pull from below the ground or from the box's top up.
    with pytest.raises(ValueError, match='refused \\(proposed rule'):
        gs.case_inputs(f, zw, air, length_s=1e6, damping_base_m=held_from - 1.0, **common)
    with pytest.raises(ValueError, match='CM1 reads at most 100'):
        gs.case_inputs(f, zw, air, length_s=2.8 * run['solar_day_s'], damping_base_m=0.77 * zw[-1], **common)
    for tau in (0.0, -7200.0, float('nan')):
        with pytest.raises(ValueError, match="wind's own nudging time is positive"):
            gs.case_inputs(f, zw, air, wind_nudge_tau_s=tau, **same)
    for z in (-1.0, zw[-1], float('nan')):
        with pytest.raises(ValueError, match="wind's pull starts at a height"):
            gs.case_inputs(f, zw, air, wind_from_m=z, **same)


# The box that makes its own large-scale vertical wind (patch 10 of the lab's CM1 series).

V_K = np.array([0.0, -0.3, -0.1, 0.2, 0.4])                    # m/s: out from the equator low, in high


@pytest.mark.parametrize('world', [MOON, EARTH], ids=['moon', 'earth'])
def test_the_extraction_gives_the_air_and_the_horizontal_part_by_local_time(tmp_path, world):
    """By local time the extraction gives the GCM's air, its fits undamped: theta (T_k + A_k cos(h) + S_k sin(h)) /
    exner and the humidity Q_k + B_k cos(h), whose lowest level swings by 2 B/Q through the day; the vertical wind
    from continuity on the fits of omega, which a spreading flow written as means over the windows makes W_k (1 +
    cos(h)) at each level, whose mean over the records is the mean vertical wind; and the circulation's horizontal
    part, the circulation less the advection by that wind,
    -w d/dz of the air by local time. Where the flow only turns with the globe, the horizontal part is the
    circulation."""
    f = gs.site_forcing(write_run(tmp_path / 'still', world), (0, 1), SEA5)
    hours = gs.bin_hours(36)
    h = np.radians(hours)[:, None]
    exner = (gs.full_levels(HALF5) * P_HPA * 100.0 / 1e5)**gs.CM1_KAPPA
    by = f['air_by_hour']
    assert by['hour_angle_deg'] == hours.tolist() and by['z_m'] == f['profile']['z_m']
    assert np.allclose(by['theta_k'], (T_K + A_K * np.cos(h) + S_K * np.sin(h)) / exner, rtol=1e-12)
    assert np.allclose(by['specific_humidity_kg_kg'], Q_K + B_K * np.cos(h), rtol=1e-9)
    assert by['lowest_level_vapour_swing'] == pytest.approx(2.0 * B_K[-1] * math.cos(math.radians(0.5)) / Q_K[-1],
                                                            rel=1e-9)
    assert np.abs(f['vertical_wind_by_hour']['w_m_s']).max() < 1e-12
    for key in ('theta_k_s', 'specific_humidity_kg_kg_s'):
        circ = np.asarray(f['circulation'][key])
        assert np.allclose(f['horizontal'][key], circ, rtol=0, atol=1e-9 * np.abs(circ).max())
    # A flow that spreads from the equator low and gathers high: the GCM's vertical wind by local time.
    f = gs.site_forcing(write_run(tmp_path / 'spread', world, spread=V_K), (0, 1), SEA5)
    w_h = np.asarray(f['vertical_wind_by_hour']['w_m_s'])
    shape = 1.0 + np.cos(h)
    at_noon = w_h[np.argmin(np.abs(hours)), :] / shape[np.argmin(np.abs(hours))]
    assert np.abs(at_noon).max() > 1e-6
    assert np.allclose(w_h, at_noon[None, :] * shape, rtol=1e-6, atol=1e-6 * np.abs(at_noon).max())
    # Its mean over the records, the mean vertical wind, by the means' damping of the cosine over the kept records.
    half = math.radians(f['window_deg'] / 2.0)
    swing = math.sin(half) / half * np.cos(np.radians(kept_centres(f['window_deg']))).mean()
    assert np.allclose(f['vertical_wind_m_s'], at_noon * (1.0 + swing), rtol=1e-6, atol=1e-6 * np.abs(at_noon).max())
    z = np.asarray(f['profile']['z_m'])
    for key, air in (('theta_k_s', 'theta_k'), ('specific_humidity_kg_kg_s', 'specific_humidity_kg_kg')):
        circ, horizontal = np.asarray(f['circulation'][key]), np.asarray(f['horizontal'][key])
        advection = w_h * np.gradient(np.asarray(f['air_by_hour'][air]), z, axis=-1)
        assert np.allclose(horizontal, circ + advection, rtol=1e-12, atol=1e-12 * np.abs(circ).max())
        assert np.abs(horizontal - circ).max() > 1e-3 * np.abs(circ).max()
    mass = layer_mass(world)
    column = f['horizontal']['column_vapour_mm_day']
    moist = np.asarray(f['circulation']['specific_humidity_kg_kg_s'])
    horizontal = np.asarray(f['horizontal']['specific_humidity_kg_kg_s'])
    assert column['circulation']['by_hour'] == [round(float(x), 4) for x in moist @ mass * 86400.0]
    assert column['horizontal']['mean'] == pytest.approx(float((horizontal @ mass).mean() * 86400.0), rel=1e-12)
    assert column['vertical_advection']['mean'] == pytest.approx(
        column['circulation']['mean'] - column['horizontal']['mean'], rel=1e-9, abs=1e-12)


def write_tropics(folder, *, t0, t1, years=2, records=5, gravity=1.6242, lat_limit=30.0):
    """Year files of an atmosphere at rest, isothermal at t0 within lat_limit of the equator and at t1 beyond, dry,
    under a uniform surface pressure, its convection heating the lowest three levels; with the record a run's
    first_mode reads."""
    netCDF4 = pytest.importorskip('netCDF4')
    folder.mkdir(parents=True, exist_ok=True)
    lat, lon, _ = grid(NLAT5, NLON5)
    ta = np.where(np.abs(lat) <= lat_limit, t0, t1)[None, None, :, None] * np.ones((records, 5, NLAT5, NLON5))
    for year in range(years):
        with netCDF4.Dataset(folder / f'MOST.{year:05d}.nc', 'w') as d:
            for name, size in (('time', None), ('lev', 5), ('lat', NLAT5), ('lon', NLON5)):
                d.createDimension(name, size)
            d.createVariable('lat', 'f8', ('lat',))[:] = lat
            d.createVariable('lon', 'f8', ('lon',))[:] = lon
            d.createVariable('lev', 'f4', ('lev',))[:] = gs.full_levels(HALF5)
            d.createVariable('time', 'f8', ('time',))[:] = np.arange(records) + 1.0
            d.createVariable('ta', 'f8', ('time', 'lev', 'lat', 'lon'))[:] = ta
            d.createVariable('hus', 'f8', ('time', 'lev', 'lat', 'lon'))[:] = np.zeros(ta.shape)
            d.createVariable('dt_conv', 'f8', ('time', 'lev', 'lat', 'lon'))[:] = np.broadcast_to(
                CONV[None, :, None, None], ta.shape)
            d.createVariable('ps', 'f8', ('time', 'lat', 'lon'))[:] = np.full((records, NLAT5, NLON5), P_HPA)
    return dict(name='tropics', folder=str(folder), gravity_m_s2=gravity, gas_constant_j_kg_k=288.38,
                heat_capacity_j_kg_k=288.38 / 0.286, vapour_gas_constant_j_kg_k=461.51, latent_heat_j_kg=2.5008e6,
                half_levels=HALF5)


def test_the_first_mode_of_an_isothermal_tropics_is_its_buoyancy_frequency_times_its_depth_over_pi(tmp_path):
    """Over an isothermal tropics at T the buoyancy frequency is g / (cp T)^(1/2) at every height, in the run's own
    heat capacity, so the first mode's speed is that frequency times the height of the convection's top over pi, and
    times the top level's height beside it; the extratropics, at another temperature, stay out, and the records are
    those the rule of A10 keeps."""
    run = write_tropics(tmp_path / 'model', t0=280.0, t1=230.0)
    mode = gs.first_mode(run, (0, 1))
    g, gas, cp = run['gravity_m_s2'], run['gas_constant_j_kg_k'], run['heat_capacity_j_kg_k']
    n = g / math.sqrt(cp * 280.0)
    z = gas * 280.0 / g * np.log(1.0 / gs.full_levels(HALF5))                   # top first
    assert mode['records'] == 2 * (5 - 2) and mode['lat_limit_deg'] == 30.0
    assert mode['convection_top_m'] == pytest.approx(z[2], rel=1e-12)
    assert mode['c_m_s'] == pytest.approx(n * z[2] / math.pi, rel=1e-9)
    assert mode['c_to_model_top_m_s'] == pytest.approx(n * z[0] / math.pi, rel=1e-9)
    assert mode['z_m'] == pytest.approx(z[::-1].tolist(), rel=1e-12)
    wide = gs.first_mode(run, (0, 1), lat_limit_deg=89.0)                      # the extratropics' cold air enters
    assert abs(wide['c_m_s'] / mode['c_m_s'] - 1.0) > 0.01
    with pytest.raises(ValueError, match='from the first to the last'):
        gs.first_mode(run, (1, 0))
    with pytest.raises(ValueError, match='between 0 and 90'):
        gs.first_mode(run, (0, 1), lat_limit_deg=0.0)
    with pytest.raises(ValueError, match='lie off the full levels'):
        gs.first_mode(dict(run, half_levels=[0.1, 0.4, 0.7, 0.9, 1.0]), (0, 1))


def test_the_footprint_is_the_square_root_of_the_sites_area():
    radius = 1.7374e6
    side = lambda half, lat=0.0: 2.0 * math.radians(half) * radius
    assert gs.footprint_m(SEA5, radius) == pytest.approx(
        math.sqrt(side(25.0) * side(25.0) * math.cos(math.radians(-10.0))), rel=1e-14)
    north = dict(SEA5, lat_deg=60.0)
    assert gs.footprint_m(north, radius) / gs.footprint_m(dict(SEA5, lat_deg=0.0), radius) == pytest.approx(
        math.sqrt(0.5), rel=1e-12)
    sea = gs.TERLUNA_OPEN_MOON_SITES['near_side_sea']
    assert 417e3 < gs.footprint_m(sea, 1737400.0) < 418e3                    # 5.6 by 8.5 degrees on the Moon


def coupled(f, run, zw, air, **settings):
    held_from = f['convection']['held_from_m']
    return gs.case_inputs(f, zw, air, gravity_m_s2=run['gravity_m_s2'], start_hour_deg=-90.0,
                          solar_day_s=run['solar_day_s'], length_s=2.0 * run['solar_day_s'],
                          damping_base_m=held_from + 1.0, nudge_tau_s=259200.0, **settings)


def test_a_coupled_case_makes_its_own_wind_against_the_gcms_air_by_local_time(tmp_path):
    """With the damped gravity wave, the case states patch 10's entries: the time the site's footprint over the
    mode's speed, to 0.1 s, the speed to 1 mm/s, the lid at the GCM's convection top and the lowest base at its lowest
    level, each to 0.1 m, and the table's heating below the base; terluna_wls.txt holds nil; the table holds the
    circulation's horizontal part with nothing added back; each window holds the GCM's air at its hour, the vapour by
    the hour where the lowest level swings by more than a tenth; and the box starts from the first window's air. The
    imposed case keeps its files and entries, and records its coupling."""
    run = write_run(tmp_path / 'model', MOON)
    f = gs.site_forcing(run, (0, 1), SEA5)
    zw = np.r_[0.0, np.cumsum(np.full(60, 2500.0))]
    air = gs.reference_air(f, run['gravity_m_s2'], zw[-1])
    imposed = coupled(f, run, zw, air)
    case = coupled(f, run, zw, air, coupling='dgw', mode=dict(c_m_s=40.0, source='stated'))
    lowest, top = f['profile']['z_m'][-1], f['convection']['top_m']
    footprint = gs.footprint_m(SEA5, run['radius_m'])
    assert case['namelist']['param3'] == dict(
        wind_nudge_tau=7200.0, wind_nudge_zmin=round(lowest, 1), inflow_ref_air=1, nudge_window_by_time=1,
        lsw_coupling=1,
        lsw_tau=round(footprint / 40.0, 1), lsw_mode_speed=40.0, lsw_top=round(top, 1), lsw_base=round(lowest, 1),
        lsw_table_heat=1)
    assert case['namelist']['param8'] == imposed['namelist']['param8']
    assert case['namelist']['param19'] == imposed['namelist']['param19']
    wls = np.loadtxt(io.StringIO(case['files']['terluna_wls.txt']), skiprows=1)
    assert np.allclose(wls[:, 0], zw) and np.all(wls[:, 1] == 0.0)
    # The table: the horizontal part laid on the box's levels, nothing added back (the flow here turns with the globe,
    # so the horizontal part is the circulation); laid on the mean air's pressures, it is the imposed case's table.
    table, laid = case['cm1']['table'], case['cm1']['circulation']
    assert np.array_equal(table['theta_k_s'], laid['theta_k_s'])
    zh = 0.5 * (zw[1:] + zw[:-1])
    r0 = np.asarray(case['start']['qv_at'](zh))
    assert np.allclose(table['qv_kg_kg_s'], laid['specific_humidity_kg_kg_s'] * (1.0 + r0)[None, :], rtol=1e-12)
    on_mean = coupled(f, run, zw, air, coupling='dgw', mode=dict(c_m_s=40.0), start='mean')
    for key in ('theta_k_s', 'qv_kg_kg_s'):
        mine, theirs = on_mean['cm1']['table'][key], imposed['cm1']['table'][key]
        assert np.allclose(mine, theirs, rtol=1e-9, atol=1e-9 * np.abs(theirs).max())
    # The windows: the GCM's air with its swing by local time, by hand, the vapour by the hour.
    heights = np.r_[0.0, zh, zw[-1]]
    zg = np.asarray(f['profile']['z_m'])[::-1]
    exner = (gs.full_levels(HALF5) * P_HPA * 100.0 / 1e5)**gs.CM1_KAPPA
    hours = gs.bin_hours(36)
    r_h = gs.mixing_ratio(Q_K[None, :] + B_K[None, :] * np.cos(np.radians(hours))[:, None])
    for i in (1, 18, 72):
        window = case['windows'][i - 1]
        b = int(np.argmin(np.abs((hours - window['hour_angle_deg'] + 180.0) % 360.0 - 180.0)))
        a = math.radians(hours[b])
        dev = ((A_K * math.cos(a) + S_K * math.sin(a)) / exner)[::-1]
        ratio = (r_h[b] / r_h.mean(axis=0))[::-1]
        rows = read_nudging(case['files'][f'lsnudge_{i:04d}.dat'])[2]
        assert np.allclose(rows[:, 1], air['theta_at'](heights) + np.interp(heights, zg, dev), atol=1e-4)
        assert np.allclose(rows[:, 2], air['qv_at'](heights) * np.interp(heights, zg, ratio) * 1000.0, rtol=1e-5,
                           atol=1e-6)
    first = read_nudging(case['files']['lsnudge_0001.dat'])[2]
    assert np.allclose(case['start']['theta_at'](heights), first[:, 1], atol=1e-4)
    assert np.allclose(case['start']['qv_at'](heights) * 1000.0, first[:, 2], atol=1e-6)
    record = case['record']
    assert record['coupling']['kind'] == 'dgw' and record['coupling']['entries'] == {
        k: v for k, v in case['namelist']['param3'].items() if k.startswith('lsw_')}
    assert record['coupling']['length_m'] == footprint and record['coupling']['time_s'] == footprint / 40.0
    assert record['coupling']['mode'] == dict(c_m_s=40.0, source='stated')
    assert record['coupling']['length_from'] == "the footprint of the GCM's site"
    assert record['reference']['vapour'] == 'by-hour' and record['reference']['lowest_level_vapour_swing'] > 0.1
    assert record['start'] == dict(source='reference', hour_angle_deg=-85.0,
                                   air="the reference's air in the first window")
    json.dumps(record)
    # The imposed case: no entry of patch 10, the GCM's mean air in every window and at the start.
    assert set(imposed['namelist']['param3']) == {'wind_nudge_tau', 'wind_nudge_zmin', 'inflow_ref_air',
                                                  'nudge_window_by_time'}
    assert imposed['record']['coupling']['kind'] == 'imposed' and imposed['record']['start']['source'] == 'mean'
    assert imposed['record']['reference']['source'] == 'gcm-mean' and imposed['start'] is air
    # Where the GCM's flow spreads and gathers, the table holds its horizontal part, apart from the circulation.
    f = gs.site_forcing(write_run(tmp_path / 'spread', MOON, spread=V_K), (0, 1), SEA5)
    air = gs.reference_air(f, run['gravity_m_s2'], zw[-1])
    case = coupled(f, run, zw, air, coupling='dgw', mode=dict(c_m_s=40.0))
    nil = [0.0] * len(f['vertical_wind_m_s'])
    laid = lambda part: gs.to_cm1(dict(f, circulation=f[part], vertical_wind_m_s=nil), zw, case['start'],
                                  run['gravity_m_s2'])['circulation']['theta_k_s']
    assert np.array_equal(case['cm1']['circulation']['theta_k_s'], laid('horizontal'))
    assert np.abs(laid('horizontal') - laid('circulation')).max() > 1e-3 * np.abs(laid('circulation')).max()


def test_a_coupled_case_states_its_length_or_time_lid_base_reference_and_start(tmp_path):
    """A case states the length its box stands for or the wave's time, its lid and its lowest base, the table's
    heating at every level, its reference (the GCM's mean air, its air by local time with its mean vapour, or a
    column series such as a box's own domain mean by local time) and its start; the record says which it stated."""
    run = write_run(tmp_path / 'model', MOON)
    f = gs.site_forcing(run, (0, 1), SEA5)
    zw = np.r_[0.0, np.cumsum(np.full(60, 2500.0))]
    air = gs.reference_air(f, run['gravity_m_s2'], zw[-1])
    zh = 0.5 * (zw[1:] + zw[:-1])
    heights = np.r_[0.0, zh, zw[-1]]
    mode = dict(c_m_s=40.5)
    planet = coupled(f, run, zw, air, coupling='dgw', mode=mode, coupling_length_m=1.7374e6)
    assert planet['namelist']['param3']['lsw_tau'] == round(1.7374e6 / 40.5, 1)
    assert planet['record']['coupling']['length_from'] == 'stated'
    timed = coupled(f, run, zw, air, coupling='dgw', mode=mode, coupling_time_s=42840.0, coupling_top_m=60000.0,
                    coupling_base_m=500.0, table_heat='every-level', reference='gcm-mean', start='mean')
    p3 = timed['namelist']['param3']
    assert (p3['lsw_tau'], p3['lsw_top'], p3['lsw_base'], p3['lsw_table_heat']) == (42840.0, 60000.0, 500.0, 0)
    assert timed['record']['coupling']['length_m'] == 42840.0 * 40.5
    assert timed['record']['coupling']['top_from'] == 'stated' == timed['record']['coupling']['base_from']
    for i in (1, 40):
        rows = read_nudging(timed['files'][f'lsnudge_{i:04d}.dat'])[2]
        assert np.allclose(rows[:, 1], air['theta_at'](heights), atol=1e-4)
    mean_vapour = coupled(f, run, zw, air, coupling='dgw', mode=mode, reference_vapour='mean')
    assert mean_vapour['record']['reference']['vapour'] == 'mean'
    rows = read_nudging(mean_vapour['files']['lsnudge_0010.dat'])[2]
    assert np.allclose(rows[:, 2], air['qv_at'](heights) * 1000.0, atol=1e-6)
    # A column series: a box's own domain mean at two hours of the day, each window taking the nearer.
    series = dict(hour_angle_deg=[-85.0, 95.0], z_m=zh.tolist(), source="a box's domain mean by local time",
                  theta_k=np.vstack([air['theta_at'](zh) - 1.0, air['theta_at'](zh) + 2.0]).tolist(),
                  qv_kg_kg=np.vstack([air['qv_at'](zh) * 0.9, air['qv_at'](zh) * 1.1]).tolist())
    boxed = coupled(f, run, zw, air, coupling='dgw', mode=mode, reference=series)
    assert boxed['record']['reference']['source'] == "a box's domain mean by local time"
    for i, row, offset in ((1, 0, -1.0), (19, 1, 2.0), (37, 0, -1.0)):
        window = boxed['windows'][i - 1]
        assert abs((window['hour_angle_deg'] - series['hour_angle_deg'][row] + 180.0) % 360.0 - 180.0) <= 90.0
        rows = read_nudging(boxed['files'][f'lsnudge_{i:04d}.dat'])[2]
        assert np.allclose(rows[1:-1, 1], air['theta_at'](zh) + offset, atol=1e-4)
        assert rows[0, 1] == pytest.approx(rows[1, 1], abs=1e-4) and rows[-1, 1] == pytest.approx(rows[-2, 1], abs=1e-4)
    assert np.allclose(boxed['start']['theta_at'](zh), air['theta_at'](zh) - 1.0, atol=1e-9)
    # The imposed wind can take a reference by local time too.
    by_hour = coupled(f, run, zw, air, reference='gcm-by-hour')
    assert by_hour['record']['coupling']['kind'] == 'imposed' and by_hour['record']['start']['source'] == 'mean'
    assert by_hour['files']['lsnudge_0001.dat'] != coupled(f, run, zw, air)['files']['lsnudge_0001.dat']


def test_a_coupled_case_refuses_what_it_cannot_state(tmp_path):
    run = write_run(tmp_path / 'model', MOON)
    f = gs.site_forcing(run, (0, 1), SEA5)
    zw = np.r_[0.0, np.cumsum(np.full(60, 2500.0))]
    air = gs.reference_air(f, run['gravity_m_s2'], zw[-1])
    mode = dict(c_m_s=40.0)
    zh = 0.5 * (zw[1:] + zw[:-1])
    good = dict(hour_angle_deg=[0.0], z_m=zh.tolist(), theta_k=[air['theta_at'](zh).tolist()],
                qv_kg_kg=[air['qv_at'](zh).tolist()])
    refused = [(dict(coupling='relaxed'), "one of \\('imposed', 'dgw', 'wtg'\\)"),
               (dict(coupling='dgw'), "first baroclinic mode's speed"),
               (dict(coupling='dgw', mode=dict(c_m_s=0.0)), "first baroclinic mode's speed"),
               (dict(coupling='dgw', mode=mode, coupling_length_m=4e5, coupling_time_s=1e4), 'where it states both'),
               (dict(coupling='dgw', mode=mode, coupling_time_s=0.0), "coupling's time is positive"),
               (dict(coupling='dgw', mode=mode, coupling_length_m=-1.0), "coupling's length is positive"),
               (dict(coupling='dgw', mode=mode, coupling_top_m=300.0, coupling_base_m=300.0), 'base < lid'),
               (dict(coupling='dgw', mode=mode, coupling_top_m=2e5), 'base < lid'),
               (dict(coupling='dgw', mode=mode, coupling_base_m=-1.0), 'base < lid'),
               (dict(coupling='dgw', mode=mode, table_heat='aloft'), 'the table heats'),
               (dict(coupling='dgw', mode=mode, start='noon'), 'a box starts from'),
               (dict(coupling='dgw', mode=mode, reference='tropics'), 'a reference is one of'),
               (dict(coupling='dgw', mode=mode, reference_vapour='hourly'), "reference's vapour is one of"),
               (dict(coupling='dgw', mode=mode, reference=dict(good, z_m=zh[::-1].tolist())), 'column series'),
               (dict(coupling='dgw', mode=mode, reference=dict(good, theta_k=[[300.0] * 3])), 'column series'),
               (dict(coupling='dgw', mode=mode, reference=dict(good, qv_kg_kg=[[-1e-3] * zh.size])), 'column series'),
               (dict(coupling='dgw', mode=mode, reference=dict(good, hour_angle_deg=[270.0])), 'column series'),
               (dict(mode=mode), "imposed wind takes none of a coupling's settings"),
               (dict(coupling_time_s=1e4), "imposed wind takes none"),
               (dict(table_heat='below-base'), "imposed wind takes none"),
               (dict(coupling_stability_min_k_m=1e-6), "imposed wind takes none"),
               (dict(coupling='dgw', mode=mode, coupling_stability_min_k_m=1e-6), 'reads no least stability'),
               (dict(coupling='wtg'), 'weak temperature gradient takes its time'),
               (dict(coupling='wtg', mode=dict(c_m_s=0.0)), 'weak temperature gradient takes its time'),
               (dict(coupling='wtg', mode=dict(c_m_s=0.0), coupling_time_s=1e4), 'takes its time'),
               (dict(coupling='wtg', mode=mode, coupling_stability_min_k_m=0.0), 'least stability is positive'),
               (dict(coupling='wtg', mode=mode, coupling_stability_min_k_m=-1e-6), 'least stability is positive'),
               (dict(coupling='wtg', mode=mode, coupling_stability_min_k_m=float('nan')), 'least stability'),
               (dict(coupling='wtg', mode=mode, coupling_length_m=4e5, coupling_time_s=1e4), 'where it states both'),
               (dict(coupling='wtg', coupling_time_s=-1.0), "coupling's time is positive"),
               (dict(coupling='wtg', mode=mode, coupling_top_m=300.0, coupling_base_m=300.0), 'base < lid'),
               (dict(coupling='wtg', mode=mode, table_heat='aloft'), 'the table heats')]
    for settings, message in refused:
        with pytest.raises(ValueError, match=message):
            coupled(f, run, zw, air, **settings)
    assert coupled(f, run, zw, air, coupling='dgw', mode=mode, reference=good)['record']['reference']['hours'] == 1
    with pytest.raises(ValueError, match="'dgw' or 'wtg'"):
        gs.coupling_entries(f, zw, mode=mode, length_m=None, time_s=None, top_m=None, base_m=None,
                            table_heat='below-base', kind='imposed')


def test_a_wtg_case_writes_patch_11s_entries_beside_the_waves_files(tmp_path):
    """With the weak temperature gradient the case states patch 11's entries: lsw_coupling 2, the wave's time, the
    site's footprint over the mode's speed, its lid, lowest base and table's cut, no mode speed, and the floor, Edman
    and Romps's 0.01 K/km times the world's gravity over Earth's 9.81 m/s2 to three figures, 1.66e-6 K/m at the Moon's.
    Its files, windows, start and the rest of its namelist are the wave's. The record holds the floor with its source
    and the least stability of the first window's air between the lowest base and the lid, which the window's printed
    air gives by hand, with the count of levels at which the floor binds: none here, and all under a floor twice the
    greatest stability. A case states its time without a mode, and its floor; at Earth's gravity the floor is Edman
    and Romps's own."""
    run = write_run(tmp_path / 'model', MOON)
    f = gs.site_forcing(run, (0, 1), SEA5)
    zw = np.r_[0.0, np.cumsum(np.full(60, 2500.0))]
    air = gs.reference_air(f, run['gravity_m_s2'], zw[-1])
    mode = dict(c_m_s=40.0, source='stated')
    wave = coupled(f, run, zw, air, coupling='dgw', mode=mode)
    case = coupled(f, run, zw, air, coupling='wtg', mode=mode)
    floor = 1.66e-6
    assert floor == float(f"{1e-5 * run['gravity_m_s2'] / 9.81:.3g}")
    p3 = {k: v for k, v in wave['namelist']['param3'].items() if k != 'lsw_mode_speed'}
    assert case['namelist']['param3'] == dict(p3, lsw_coupling=2, lsw_stab_min=floor)
    assert case['files'] == wave['files']
    assert all(case['namelist'][k] == wave['namelist'][k] for k in ('param8', 'param19'))
    zh = 0.5 * (zw[1:] + zw[:-1])
    for key in ('theta_at', 'qv_at'):
        assert np.array_equal(case['start'][key](zh), wave['start'][key](zh))
    record = case['record']['coupling']
    assert record['kind'] == 'wtg' and record['entries'] == {
        k: v for k, v in case['namelist']['param3'].items() if k.startswith('lsw_')}
    assert record['stability_min_k_m'] == floor
    assert record['stability_min_from'].startswith("Edman and Romps's 0.01 K/km")
    assert record['time_s'] == wave['record']['coupling']['time_s'] and record['mode'] == mode
    assert 'Edman and Romps (2015' in record['method'] and 'Daleu' in record['below_base']
    # The first window's stability, from its printed air at the box's scalar levels.
    rows = read_nudging(case['files']['lsnudge_0001.dat'])[2][1:-1]
    thv = rows[:, 1] * (1.0 + (gs.CM1_RV / gs.CM1_RD - 1.0) * rows[:, 2] / 1000.0)
    between = (zw[1:-1] > p3['lsw_base']) & (zw[1:-1] < p3['lsw_top'])
    s = (np.diff(thv) / np.diff(zh))[between]
    found = record['first_window_stability']
    assert found['levels'] == between.sum() > 10 and found['floored_levels'] == (s < floor).sum()
    assert found['least_k_m'] == pytest.approx(s.min(), rel=1e-3, abs=1e-7)
    json.dumps(case['record'])
    above = coupled(f, run, zw, air, coupling='wtg', mode=mode, coupling_stability_min_k_m=2.0 * float(s.max()))
    assert above['record']['coupling']['first_window_stability']['floored_levels'] == between.sum()
    # A time without a mode, a floor stated, and Earth's gravity.
    timed = coupled(f, run, zw, air, coupling='wtg', coupling_time_s=42840.0, coupling_stability_min_k_m=5e-6)
    assert (timed['namelist']['param3']['lsw_tau'], timed['namelist']['param3']['lsw_stab_min']) == (42840.0, 5e-6)
    assert timed['record']['coupling']['mode'] is None and timed['record']['coupling']['length_m'] is None
    assert timed['record']['coupling']['stability_min_from'] == 'stated'
    entries = gs.coupling_entries(f, zw, mode=mode, length_m=None, time_s=None, top_m=None, base_m=None,
                                  table_heat='every-level', kind='wtg', gravity_m_s2=9.81)[0]
    assert entries['lsw_stab_min'] == 1e-5 and entries['lsw_table_heat'] == 0


def test_every_forced_case_holds_the_nudging_window_by_the_steps_time(tmp_path):
    """Patch 12's entry is on in every forced case, imposed, under the wave and under the weak temperature gradient, so
    that a box run in segments nudges toward the windows of the box run whole (defect log A12); a case turns it off,
    which leaves CM1's count, and the record says which. The files are the same either way."""
    run = write_run(tmp_path / 'model', MOON)
    f = gs.site_forcing(run, (0, 1), SEA5)
    zw = np.r_[0.0, np.cumsum(np.full(60, 2500.0))]
    air = gs.reference_air(f, run['gravity_m_s2'], zw[-1])
    mode = dict(c_m_s=40.0)
    for settings in (dict(), dict(coupling='dgw', mode=mode), dict(coupling='wtg', mode=mode)):
        on, off = (coupled(f, run, zw, air, window_by_time=by_time, **settings) for by_time in (True, False))
        assert coupled(f, run, zw, air, **settings)['namelist'] == on['namelist']
        assert on['namelist']['param3']['nudge_window_by_time'] == 1 and on['record']['windows']['by_time'] is True
        assert off['namelist']['param3'] == dict(on['namelist']['param3'], nudge_window_by_time=0)
        assert off['record']['windows']['by_time'] is False and 'A12' in off['record']['windows']['count']
        assert off['files'] == on['files']


# Terluna's sea box on its design years, from the same GCM run read in place (research drive).

def _drive():
    from worldlab import roots
    drive = roots.root('terluna-drive')
    if drive is None:
        pytest.skip("Terluna's research drive is absent")
    run = drive / 'gcm-runs' / 'A28R_301k_design_l15_snow_s934'
    case = drive / 'crm-runs' / 'box_near_side_sea_design_years'
    if not (run / 'model' / 'MOST.00019.nc').exists() or not (case / 'case.json').exists():
        pytest.skip("Terluna's design run or its sea box is absent from the drive")
    pytest.importorskip('netCDF4')
    return run, case


def terluna_choices(run_folder: Path) -> dict:
    """The values Terluna's gcm_site takes where the lab reads the run's own (Terluna's climate/crm/gcm_site.py at
    39c5ee04): CM1's gas constant, 287.04, and its 0.608 for the vapour in place of the run's GASCON and PlaSim's RV;
    CM1's heat capacity and latent heat, 1005.7 and 2.501e6, in place of PlaSim's; the planet record's radius,
    1,737,400 m, in place of PLARAD; a window of 36 degrees, where the records span 143 steps of 30 minutes of a solar
    day of 29.53059 days, 36.318 degrees; and the half levels rebuilt from the output's single-precision full levels.
    Beside them Terluna's module undoes the humidity's means as true means (site_forcing's humidity_filter 'mean')."""
    import netCDF4
    with netCDF4.Dataset(run_folder / 'model' / 'MOST.00010.nc') as d:
        lev = np.asarray(d['lev'][:], float)
    e = [0.0]
    for s in lev:
        e.append(2.0 * s - e[-1])
    return dict(window_deg=36.0, gas_constant_j_kg_k=287.04, vapour_gas_constant_j_kg_k=1.608 * 287.04,
                heat_capacity_j_kg_k=1005.7, latent_heat_j_kg=2.501e6, radius_m=1737400.0, half_levels=e[1:])


@pytest.fixture(scope='module')
def terluna_box():
    """The lab's forcing of Terluna's sea box over the design years 10-19, with Terluna's choices and with the run's
    own constants, on the box's own w levels, beside Terluna's recorded case."""
    run_folder, case = _drive()
    own = gs.run_record(run_folder / 'model', run_folder / 'inputs' / 'moon_topography.sra',
                        solar_day_s=29.53059 * 86400.0)
    zw = np.loadtxt(case / 'input_grid_z')
    out = dict(record=json.loads((case / 'case.json').read_text()), case=case, zw=zw)
    for name, run, humidity in (('terluna', dict(own, **terluna_choices(run_folder)), 'mean'), ('own', own, None)):
        f = gs.site_forcing(run, (10, 19), gs.TERLUNA_OPEN_MOON_SITES['near_side_sea'], humidity_filter=humidity)
        air = gs.reference_air(f, run['gravity_m_s2'], zw[-1])
        out[name] = dict(forcing=f, air=air, case=gs.case_inputs(
            f, zw, air, gravity_m_s2=run['gravity_m_s2'], start_hour_deg=-90.0, solar_day_s=run['solar_day_s'],
            length_s=118 * 43200.0, damping_base_m=0.77 * zw[-1], nudge_tau_s=259200.0))
    return out


def _rel(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float(np.abs(a - b).max() / np.abs(b).max())


def test_with_terlunas_choices_the_extraction_gives_terlunas_recorded_sea_box(terluna_box):
    """Run with the values Terluna's module takes, the lab's extraction gives Terluna's recorded forcing of
    box_near_side_sea_design_years: the GCM's column and budget to the last bit, and the files to the digits they
    print, the vapour carried into CM1's mixing ratio."""
    g, f = terluna_box['record']['gcm_site'], terluna_box['terluna']['forcing']
    case, record = terluna_box['terluna']['case'], terluna_box['record']
    assert f['cells'] == g['cells'] and (f['records'], f['phases']) == (g['outputs'], g['phases']) == (1180, 10)
    assert {k: f['convection'][k] for k in ('level', 'top_m', 'held_from_m', 'held_fully_from_m')} == \
        {k: g['convection'][k] for k in ('level', 'top_m', 'held_from_m', 'held_fully_from_m')}
    for key in ('convective_rain_formed_mm_day', 'large_scale_rain_formed_mm_day'):
        assert f['convection'][key] == g['convection'][key]
    for key in ('circulation_heating_theta_k_day', 'circulation_moistening_g_kg_day', 'physics_heating_theta_k_day',
                'physics_moistening_g_kg_day', 'rain_mm_day', 'evaporation_mm_day', 'column_heating_w_m2'):
        assert f['budget'][key] == g['budget'][key], key
    for key in ('exact', 'from_snapshots', 'exact_by_hour', 'from_snapshots_by_hour', 'held_by_hour'):
        assert f['budget']['column_vapour_mm_day'][key] == g['budget']['column_vapour_mm_day'][key], key
    assert f['surface'] == g['surface']
    profile = record['reference']['profile']
    for mine, theirs in (('z_m', 'z_m'), ('theta_k', 'theta_k'), ('specific_humidity_kg_kg', 'qv_kg_kg'),
                         ('u_m_s', 'u_m_s'), ('v_m_s', 'v_m_s')):
        assert f['profile'][mine] == profile[theirs], mine
    assert case['namelist']['param8']['var14'] == record['configuration']['nudge']['z_start_m']
    assert case['namelist']['param8']['var15'] == record['configuration']['nudge']['z_full_m']
    # The entries of the lab's patch 09, at their defaults, take the values Terluna's set-up gave the box in the
    # generic slots its build read them from: the wind's time (var10), its pull's height (var8) and the inflow (var7).
    text = (terluna_box['case'] / 'namelist.input').read_text()
    slot = lambda name: float(re.search(rf'^\s*{name}\s*=\s*([^,\n]+),', text, flags=re.M).group(1))
    p3 = {k: v for k, v in case['namelist']['param3'].items() if k != 'nudge_window_by_time'}   # patch 12's, the lab's
    assert p3 == dict(wind_nudge_tau=slot('var10'), wind_nudge_zmin=slot('var8'), inflow_ref_air=int(slot('var7'))) == \
        dict(wind_nudge_tau=7200.0, wind_nudge_zmin=316.1, inflow_ref_air=1)
    assert case['namelist']['param3']['nudge_window_by_time'] == 1
    assert record['corrected_wind'] == dict(var10=7200.0, var8=316.1)
    # The files, read back: the vertical wind to its printed 1e-9 m/s, the windows' wind and air to their printed
    # digits, their heights to the millimetre to which the box's input_grid_z gives the levels it is read from, and the
    # vapour once Terluna's specific humidity is carried into a mixing ratio, to 1 part in 10^3.
    folder = terluna_box['case']
    wls_t = np.loadtxt(folder / 'terluna_wls.txt', skiprows=1)
    wls_l = np.loadtxt(io.StringIO(case['files']['terluna_wls.txt']), skiprows=1)
    assert np.array_equal(wls_t[:, 0], wls_l[:, 0]) and np.abs(wls_t[:, 1] - wls_l[:, 1]).max() <= 1.0001e-9
    assert len([n for n in case['files'] if n.startswith('lsnudge')]) == len(list(folder.glob('lsnudge_0*.dat'))) == 72
    for i in range(1, 73):
        t1, t2, theirs = read_nudging((folder / f'lsnudge_{i:04d}.dat').read_text())
        s1, s2, mine = read_nudging(case['files'][f'lsnudge_{i:04d}.dat'])
        assert (t1, t2) == (s1, s2)
        assert np.abs(mine[:, 0] - theirs[:, 0]).max() <= 1e-3
        assert np.abs(mine[:, [1, 3, 4]] - theirs[:, [1, 3, 4]]).max() <= 1.0001e-4
        q = theirs[:, 2] / 1000.0
        assert np.allclose(mine[:, 2], q / (1.0 - q) * 1000.0, rtol=1e-3, atol=2e-6)
    # The table: Terluna's less its own addition of the mean wind's advection of its starting air is each GCM layer's
    # circulation laid on CM1's levels, which the lab's gives to 1 part in 10^4 of its largest value.
    _, th, qv = read_lsadv((folder / 'terluna_lsadv.txt').read_text())
    start = read_nudging((folder / 'lsnudge_0001.dat').read_text())[2][1:-1]
    zh = start[:, 0]
    w = 0.5 * (wls_t[1:, 1] + wls_t[:-1, 1])
    laid_th = th - (w * np.gradient(start[:, 1], zh))[None, :]
    laid_q = qv - (w * np.gradient(start[:, 2] / 1000.0, zh))[None, :]
    assert _rel(case['cm1']['circulation']['theta_k_s'], laid_th) < 1e-4
    assert _rel(case['cm1']['circulation']['specific_humidity_kg_kg_s'], laid_q) < 1e-4


def test_on_the_runs_own_constants_the_extraction_departs_from_terlunas_by_their_causes(terluna_box):
    """On the run's own constants the forcing moves from Terluna's by stated causes, each within its tolerance: the
    GCM's heights by the ratio of its gas constant to CM1's, 288.377 over 287.04, 0.47%, and the vertical wind with
    them and with the density; the fits by local time by the window, 36.318 degrees in place of 36; the humidity's
    fit by its records' own filter, which moves the moistening by local time up to 8% of its largest value; the
    formed rain by PlaSim's heat capacity and latent heat. The column's budget, the surface and the air's vapour and
    wind at the GCM's levels stay Terluna's."""
    g, f = terluna_box['record']['gcm_site'], terluna_box['own']['forcing']
    t = terluna_box['terluna']['forcing']
    ratio = f['gcm']['gas_constant_j_kg_k'] / 287.04
    assert ratio == pytest.approx(1.00466, abs=1e-5) and f['window_deg'] == pytest.approx(36.3183, abs=1e-4)
    assert f['cells'] == g['cells'] and f['records'] == 1180 and f['surface'] == g['surface']
    assert f['convection']['level'] == g['convection']['level'] == 2
    for key in ('top_m', 'held_from_m', 'held_fully_from_m'):
        assert f['convection'][key] / g['convection'][key] == pytest.approx(ratio, abs=2e-4)
    assert np.allclose(np.asarray(f['profile']['z_m']) / np.asarray(t['profile']['z_m']), ratio, atol=2e-4)
    assert f['budget']['column_vapour_mm_day']['exact'] == pytest.approx(g['budget']['column_vapour_mm_day']['exact'],
                                                                        rel=1e-12)
    assert f['profile']['specific_humidity_kg_kg'] == t['profile']['specific_humidity_kg_kg']
    assert f['profile']['u_m_s'] == t['profile']['u_m_s']
    assert _rel(f['profile']['theta_k'], t['profile']['theta_k']) < 1e-5            # the exact levels' sigma
    assert _rel(f['budget']['circulation_heating_theta_k_day'], g['budget']['circulation_heating_theta_k_day']) < 1e-4
    assert _rel(f['budget']['circulation_moistening_g_kg_day'], g['budget']['circulation_moistening_g_kg_day']) < 1e-3
    assert (f['humidity_filter'], t['humidity_filter']) == ('ends', 'mean')
    moistening = _rel(f['circulation']['specific_humidity_kg_kg_s'], t['circulation']['specific_humidity_kg_kg_s'])
    assert 0.05 < moistening < 0.1
    assert _rel(f['convection']['convective_rain_formed_mm_day'], g['convection']['convective_rain_formed_mm_day']) \
        == pytest.approx((f['gcm']['heat_capacity_j_kg_k'] / 2.5008e6) / (1005.7 / 2.501e6) - 1.0, abs=1e-4)
    assert _rel(f['circulation']['theta_k_s'], t['circulation']['theta_k_s']) < 0.01
    assert _rel(f['wind_by_hour']['u_m_s'], t['wind_by_hour']['u_m_s']) < 0.001
    assert _rel(f['vertical_wind_m_s'], t['vertical_wind_m_s']) < 0.01
    own, theirs = terluna_box['own']['case'], terluna_box['terluna']['case']
    assert _rel(own['cm1']['w_m_s'], theirs['cm1']['w_m_s']) < 0.015
    assert _rel(own['cm1']['table']['theta_k_s'], theirs['cm1']['table']['theta_k_s']) < 0.05
    assert _rel(own['cm1']['table']['qv_kg_kg_s'], theirs['cm1']['table']['qv_kg_kg_s']) < 0.1
    u = lambda c: np.array([w['u_m_s'] for w in c['windows']])
    assert _rel(u(own), u(theirs)) < 0.01
    assert own['record']['held']['damping_clearance_m'] == pytest.approx(115500.0 - f['convection']['held_from_m'])
    assert 0.015 < own['record']['mass_above_top_share'] < 0.025                      # about 2% above 150 km
    # The vapour in CM1's variable: near the sea about 14 g/kg of specific humidity, 0.2 g/kg more as a mixing ratio.
    q0, r0 = f['profile']['specific_humidity_kg_kg'][-1], float(terluna_box['own']['air']['qv_at'](0.0))
    assert 0.0135 < q0 < 0.0145 and r0 - q0 == pytest.approx(q0 * q0 / (1.0 - q0), rel=1e-12)


# Terluna's damped-gravity-wave boxes on its design years (research drive): box_near_side_sea_dgw, box_0e_dgw and
# box_se_dry_dgw, set up on 5 November 2026 by Terluna's dgw_inputs (climate/crm/cm1_run.py at 29af5c16).

DGW_BOXES = (('box_near_side_sea_dgw', 'near_side_sea', False), ('box_0e_dgw', '0e', True),
             ('box_se_dry_dgw', 'se_dry', True))


@pytest.fixture(scope='module')
def terluna_wave(terluna_box):
    """The first mode over the design years with Terluna's choices and on the run's own constants, the sea box's case
    with the wave from each, and Terluna's three recorded boxes."""
    run_folder, _ = _drive()
    drive = run_folder.parents[1]
    own = gs.run_record(run_folder / 'model', run_folder / 'inputs' / 'moon_topography.sra',
                        solar_day_s=29.53059 * 86400.0)
    runs = dict(terluna=dict(own, **terluna_choices(run_folder)), own=own)
    out = dict(runs=runs, boxes={})
    for name, site, _ in DGW_BOXES:
        folder = drive / 'crm-runs' / name
        if not (folder / 'case.json').exists():
            pytest.skip(f"Terluna's {name} is absent from the drive")
        out['boxes'][name] = dict(folder=folder, record=json.loads((folder / 'case.json').read_text()))
    zw = terluna_box['zw']
    for label in ('terluna', 'own'):
        mode = gs.first_mode(runs[label], (10, 19))
        f, air = terluna_box[label]['forcing'], terluna_box[label]['air']
        run = runs[label]
        case = lambda **settings: gs.case_inputs(
            f, zw, air, gravity_m_s2=run['gravity_m_s2'], start_hour_deg=-90.0, solar_day_s=run['solar_day_s'],
            length_s=118 * 43200.0, damping_base_m=0.77 * zw[-1], nudge_tau_s=259200.0, coupling='dgw', mode=mode,
            **settings)
        out[label] = dict(mode=mode, case=case(), on_mean=case(start='mean'))
    return out


def test_the_first_mode_and_the_footprints_are_terlunas(terluna_wave):
    """With Terluna's choices first_mode gives the first mode's speed of Terluna's three boxes to the last bit,
    40.53382926508821 m/s over the design years' tropics (and 82.447 m/s to the model's top), and footprint_m their
    lengths, 418 km at the sea and the land and 354 km at the dry box, so the times 10,303, 10,323 and 8,733 s. On the
    run's own constants the heights stand 0.47% higher, and the potential temperature takes the run's own ratio of gas
    constant to heat capacity, so the speed comes to 40.77 m/s, 0.58% faster."""
    mode, own = terluna_wave['terluna']['mode'], terluna_wave['own']['mode']
    for name, site, _ in DGW_BOXES:
        dgw = terluna_wave['boxes'][name]['record']['dgw']
        assert mode['c_m_s'] == dgw['c_m_s'] == 40.53382926508821
        assert mode['c_to_model_top_m_s'] == dgw['c_to_model_top_m_s']
        assert mode['convection_top_m'] == dgw['tropical_convection_top_m']
        footprint = gs.footprint_m(gs.TERLUNA_OPEN_MOON_SITES[site], terluna_wave['runs']['terluna']['radius_m'])
        assert footprint == dgw['scale_m'] and footprint / mode['c_m_s'] == dgw['tau_s']
    assert mode['records'] == 1180
    assert own['c_m_s'] / mode['c_m_s'] == pytest.approx(1.0058, abs=2e-4)
    assert own['convection_top_m'] / mode['convection_top_m'] == pytest.approx(288.377 / 287.04, abs=3e-4)


def test_with_terlunas_choices_the_wave_case_gives_terlunas_sea_box(terluna_wave):
    """With Terluna's choices the sea box's case with the wave takes the values Terluna's set-up gave its generic
    slots, the lid var4, the time var5, the speed var6 and the floor var8; its windows hold Terluna's air by local time
    to their printed digits, the vapour its mean at sea once carried into a mixing ratio; terluna_wls.txt holds nil; the
    box starts from the first window's air, Terluna's sounding; and the record's column of the circulation, its
    horizontal part and its vertical advection is Terluna's. The table, laid on the GCM's mean air as Terluna laid it,
    is Terluna's to 1 part in 10^4 of its largest value; the lab lays it on the box's own starting air, the base state
    CM1 runs on, which moves it by up to 1.0% of the heating's largest value and 1.5% of the moistening's, near
    650 m."""
    name = 'box_near_side_sea_dgw'
    folder, record = terluna_wave['boxes'][name]['folder'], terluna_wave['boxes'][name]['record']
    case, on_mean = terluna_wave['terluna']['case'], terluna_wave['terluna']['on_mean']
    text = (folder / 'namelist.input').read_text()
    slot = lambda key: float(re.search(rf'^\s*{key}\s*=\s*([^,\n]+),', text, flags=re.M).group(1))
    p3 = case['namelist']['param3']
    assert (p3['lsw_top'], p3['lsw_tau'], p3['lsw_mode_speed'], p3['lsw_base']) == \
        (slot('var4'), slot('var5'), slot('var6'), slot('var8')) == (73084.5, 10303.0, 40.534, 316.1)
    assert p3['lsw_coupling'] == int(slot('var9')) == 1 and p3['inflow_ref_air'] == int(slot('var7'))
    assert case['record']['reference']['vapour'] == 'mean' and not record['dgw']['qv_by_hour']
    wls = np.loadtxt(io.StringIO(case['files']['terluna_wls.txt']), skiprows=1)
    assert np.all(wls[:, 1] == 0.0) and np.all(np.loadtxt(folder / 'terluna_wls.txt', skiprows=1)[:, 1] == 0.0)
    assert len(list(folder.glob('lsnudge_0*.dat'))) == 72
    for i in range(1, 73):
        t1, t2, theirs = read_nudging((folder / f'lsnudge_{i:04d}.dat').read_text())
        s1, s2, mine = read_nudging(case['files'][f'lsnudge_{i:04d}.dat'])
        assert (t1, t2) == (s1, s2)
        assert np.abs(mine[:, [1, 3, 4]] - theirs[:, [1, 3, 4]]).max() <= 1.0001e-4
        q = theirs[:, 2] / 1000.0
        assert np.allclose(mine[:, 2], q / (1.0 - q) * 1000.0, rtol=1e-3, atol=2e-6)
    sounding = np.loadtxt(folder / 'input_sounding', skiprows=1)
    zh, q = sounding[:, 0], sounding[:, 2] / 1000.0
    assert np.abs(case['start']['theta_at'](zh) - sounding[:, 1]).max() <= 1e-4
    assert np.allclose(case['start']['qv_at'](zh), q / (1.0 - q), rtol=1e-3, atol=1.0001e-8)   # 5 decimals of g/kg
    assert record['initial']['hour_deg'] == case['record']['start']['hour_angle_deg'] == -85.0
    mine = case['record']['coupling']['gcm_column_vapour_mm_day']
    for key in ('circulation', 'horizontal', 'vertical_advection'):
        assert mine[key]['mean'] == pytest.approx(record['dgw']['gcm_column_vapour_mm_day'][key]['mean'], rel=1e-9)
        assert mine[key]['by_hour'] == record['dgw']['gcm_column_vapour_mm_day'][key]['by_hour']
    _, th, qv = read_lsadv((folder / 'terluna_lsadv.txt').read_text())
    assert _rel(on_mean['cm1']['circulation']['theta_k_s'], th) < 1e-4
    assert _rel(on_mean['cm1']['circulation']['specific_humidity_kg_kg_s'], qv) < 1e-4
    theta, moist = (_rel(case['cm1']['circulation'][k], v) for k, v in (('theta_k_s', th),
                                                                        ('specific_humidity_kg_kg_s', qv)))
    assert 0.005 < theta < 0.012 and 0.01 < moist < 0.02


def test_terlunas_rule_for_the_vapour_by_local_time_gives_its_three_choices(terluna_wave, terluna_box):
    """By Terluna's rule the reference takes the GCM's vapour by local time where its lowest level swings by more than
    a tenth of its mean through the day: at the sea its lowest level swings by 4.3%, and Terluna's sea box took the
    mean, while its land and dry boxes took the vapour by the hour, where the lowest level swings by more."""
    swing = terluna_box['terluna']['forcing']['air_by_hour']['lowest_level_vapour_swing']
    assert swing == pytest.approx(0.0433, abs=5e-4)
    run = terluna_wave['runs']['terluna']
    for name, site, by_hour in DGW_BOXES[1:]:
        f = gs.site_forcing(run, (10, 19), gs.TERLUNA_OPEN_MOON_SITES[site], humidity_filter='mean')
        assert f['air_by_hour']['lowest_level_vapour_swing'] > gs.VAPOUR_SWING
        assert terluna_wave['boxes'][name]['record']['dgw']['qv_by_hour'] is by_hour is True


def test_on_the_runs_own_constants_the_wave_case_departs_from_terlunas_by_its_causes(terluna_wave):
    """On the run's own constants the wave's entries move by the stated causes: the speed 0.58% faster, the lid and
    the floor 0.47% higher with the GCM's heights, and the time 0.58% shorter, the footprint's length unchanged but
    for the run's radius."""
    own, terluna = (terluna_wave[k]['case']['namelist']['param3'] for k in ('own', 'terluna'))
    assert own['lsw_mode_speed'] / terluna['lsw_mode_speed'] == pytest.approx(1.0058, abs=2e-4)
    assert own['lsw_top'] / terluna['lsw_top'] == pytest.approx(288.377 / 287.04, abs=3e-4)
    assert own['lsw_base'] == 317.6 and terluna['lsw_base'] == 316.1
    assert own['lsw_tau'] / terluna['lsw_tau'] == pytest.approx(terluna['lsw_mode_speed'] / own['lsw_mode_speed']
                                                                * 1.7374e6 / 1737400.0, rel=2e-4)
