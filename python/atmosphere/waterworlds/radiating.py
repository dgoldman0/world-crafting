"""The radiating surfaces of a steam column: the heights from which it emits and at which it absorbs.

Following Goldblatt (2015) as Arnscheidt, Wordsworth and Ding (2019, section 2.3) summarise him, the column emits
and absorbs at the height where the vertical optical depth from the top reaches one, wavenumber by wavenumber; the
emitting surface's height is the mean of those heights weighted by the outgoing spectrum, and the absorbing
surface's the mean weighted by the star's Planck curve, over all wavenumbers, those where the whole column's depth
stays below one counting at the surface. Within the layer where the depth reaches one the absorber grows with
pressure and the height with its logarithm. The outgoing spectrum is the column's plane-parallel flux at the top
(radiative_convective.longwave, four Gauss angles, a source linear in optical depth) over a black surface.
"""
from __future__ import annotations

import math

import numpy as np

from shared.constants import STEFAN_BOLTZMANN
from atmosphere.radiative_convective import longwave as lw

CHUNK = 40_000


def unit_depth_heights(tau: np.ndarray, p: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Heights, m, where the vertical optical depth from the top reaches one, and whether the top layer holds it.

    tau: layers x wavenumbers, the surface layer first; p and z: the level pressures and heights, the surface first.
    Where the whole column's depth stays below one the height is the surface's, 0.
    """
    above = np.cumsum(tau[::-1], axis=0)[::-1]                 # above[k]: the depth from the top down to level k,
    reached = above >= 1.0                                     # the bottom of layer k
    k = reached.sum(axis=0) - 1                                # the highest layer whose bottom lies at depth >= 1
    heights = np.zeros(tau.shape[1])
    hit = k >= 0
    kk = k[hit]
    cols = np.nonzero(hit)[0]
    depth_top = np.where(kk + 1 < tau.shape[0], above[np.minimum(kk + 1, tau.shape[0] - 1), cols], 0.0)
    share = (1.0 - depth_top) / tau[kk, cols]                  # of the layer's absorber, from its top
    p_bottom, p_top = p[kk], p[kk + 1]
    p_star = p_top + share * (p_bottom - p_top)
    heights[hit] = z[kk + 1] + (z[kk] - z[kk + 1]) * np.log(p_star / p_top) / np.log(p_bottom / p_top)
    return heights, k == tau.shape[0] - 1


def planck_mean_height(nu: np.ndarray, heights: np.ndarray, t_star: float) -> float:
    """The band's contribution to the mean height under a Planck curve at t_star, as a share of its whole integral."""
    weight = lw.planck(nu, t_star)
    return float(lw.integrate(nu, weight * heights)) / (STEFAN_BOLTZMANN * t_star ** 4 / math.pi)


def column_spectra(col: dict, optics, bands, *, n_angles: int = 4, chunk: int = CHUNK) -> list[dict]:
    """For each band: the wavenumbers, the outgoing spectral flux at the top (W m^-2 per cm^-1), the heights where
    the depth reaches one, and flags marking the wavenumbers whose depth reaches one within the top layer."""
    out = []
    for band in bands:
        nu, sigma = optics.layer_cross_sections(col, band)            # layers x wavenumbers, cm^2 per molecule
        n = col['layer_column_cm2'][:, None]
        olr = np.empty(nu.size)
        heights = np.empty(nu.size)
        at_top = np.empty(nu.size, dtype=bool)
        for a in range(0, nu.size, chunk):
            sl = slice(a, a + chunk)
            tau = sigma[:, sl] * n
            up, _ = lw.fluxes(nu[sl], tau, col['t_k'], col['surface_temperature_k'], n_angles=n_angles)
            olr[sl] = up[-1]
            heights[sl], at_top[sl] = unit_depth_heights(tau, col['p_pa'], col['z_m'])
        out.append(dict(nu=nu, olr=olr, heights=heights, at_top=at_top))
    return out


def surfaces(col: dict, spectra: list[dict], star_temperatures=()) -> dict:
    """The outgoing longwave (W/m^2), the emitting and absorbing surfaces' heights (m) and their scaling factors
    (r/r_s)^2, and for each the share of its weight whose depth reaches one within the top layer, where the absorber
    above the column's top would raise the height further. The share counts too few: the gas above the grid's top
    holds several times the top layer's mass, so wavenumbers whose top layer reaches a depth of a few tenths would
    move as well; the column's convergence with its top measures that better (notes/waterworlds.md)."""
    r_s = col['world'].radius_m
    olr = sum(float(lw.integrate(s['nu'], s['olr'])) for s in spectra)
    z_lw = sum(float(lw.integrate(s['nu'], s['olr'] * s['heights'])) for s in spectra) / olr
    top_share = sum(float(lw.integrate(s['nu'], s['olr'] * s['at_top'])) for s in spectra) / olr
    result = dict(olr=olr, z_lw=z_lw, lw_factor=((r_s + z_lw) / r_s) ** 2, lw_top_share=top_share, sw={})
    for t_star in star_temperatures:
        z_sw = sum(planck_mean_height(s['nu'], s['heights'], t_star) for s in spectra)
        top = sum(planck_mean_height(s['nu'], s['at_top'].astype(float), t_star) for s in spectra)
        result['sw'][t_star] = dict(z=z_sw, factor=((r_s + z_sw) / r_s) ** 2, top_share=top)
    return result
