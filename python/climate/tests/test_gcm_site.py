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


def write_run(folder, world, years=2, *, still=False, drop=None, lev=None, true_mean=()):
    """A synthetic run's model folder: its namelists, its surface geopotential and its year files; the years in
    true_mean also write the humidity's true mean, hus_mean."""
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
            field('va', 0.0)
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
    # The refusals: the damping below the held air (proposed), and more windows than CM1 reads.
    common = dict(gravity_m_s2=run['gravity_m_s2'], start_hour_deg=-90.0, solar_day_s=run['solar_day_s'],
                  nudge_tau_s=259200.0)
    with pytest.raises(ValueError, match='refused \\(proposed rule'):
        gs.case_inputs(f, zw, air, length_s=1e6, damping_base_m=held_from - 1.0, **common)
    with pytest.raises(ValueError, match='CM1 reads at most 100'):
        gs.case_inputs(f, zw, air, length_s=2.8 * run['solar_day_s'], damping_base_m=0.77 * zw[-1], **common)


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
