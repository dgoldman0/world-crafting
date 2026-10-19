"""Water's absorption in a steam column: its lines and its continuum, layer by layer, on two wavenumber bands.

The lines are HITRAN's, read by the radiative-convective column's spectroscopy with its intensity scaling and Voigt
profiles cut 25 cm^-1 from centre, the profile's value there subtracted, as MT_CKD's continuum assumes; the continuum
is MT_CKD 4.3's self continuum, the whole air being water. Up to `BROAD_PA`, 2 bar, the column's multi-mesh line sum
serves: there its points stay within 0.4% of a direct sum on the thermal band's grid and within 0.9% on the stellar
band's, and its band integrals within 0.1%. Above it, where steam's Lorentz widths pass about 0.5 cm^-1 and the
multi-mesh sum's far wings, expanded in (gamma/d)^2, err further (0.7% at 5 bar; at 26 bar the sum keeps 27 to 85% of
the lines' absorption, by window), each line's profile is summed directly on the band's grid out to the cut.
Absorption alone sets the optical depths: scattering is folded into the albedo, as in the paper.

Cross-sections depend on a layer's pressure and temperature alone, so a cache folder, when given, keeps each layer's
as float32 under a key of the lines, the partition sums and continuum files, the band, the method and its version,
and the state.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.special import voigt_profile

from shared.constants import AVOGADRO, BOLTZMANN, SPEED_OF_LIGHT
from atmosphere.radiative_convective import fetch_inputs, spectroscopy as sp

BROAD_PA = 2e5
CUTOFF = 25.0
VERSION = 1          # of broad_line_absorption and cross_section: raised when either changes, it rebuilds the cache


@dataclass(frozen=True)
class Band:
    start: float
    stop: float
    step: float
    coarse_factor: int

    @property
    def grid(self) -> sp.Grid:
        return sp.Grid.span(self.start, self.stop, self.step)


THERMAL = Band(1.0, 3500.0, 0.01, 10)
STELLAR = Band(3500.0, 25000.0, 0.05, 4)            # the trapezoid joins the bands at 3500 cm^-1
BANDS = (THERMAL, STELLAR)


def broad_line_absorption(grid: sp.Grid, lines: sp.LineList, sums: sp.PartitionSums, t: float, p_pa: float,
                          cutoff: float = CUTOFF, batch: int = 512) -> np.ndarray:
    """Cross-section (cm^2 per molecule) of pure steam's lines at (t, p_pa), every line's Voigt profile cut at
    `cutoff`, less its value there, summed directly on the grid."""
    lines = lines.select(grid.start - cutoff, grid.stop + cutoff)
    out = np.zeros(grid.size)
    if len(lines) == 0:
        return out
    p_atm = p_pa / 101325.0
    strength = (lines.strength * sums.ratio(lines.gid, t) * np.exp(-sp.C2 * lines.elower * (1 / t - 1 / sp.T_REF))
                * (-np.expm1(-sp.C2 * lines.nu / t)) / (-np.expm1(-sp.C2 * lines.nu / sp.T_REF)))
    lorentz = (sp.T_REF / t) ** lines.n_air * lines.gamma_self * p_atm
    gauss = lines.nu * math.sqrt(BOLTZMANN * t * AVOGADRO * 1e3) / SPEED_OF_LIGHT / np.sqrt(lines.mass)
    base = lorentz / (math.pi * (cutoff ** 2 + lorentz ** 2))
    k = int(math.ceil(cutoff / grid.step))
    offsets = np.arange(-k, k + 1)
    for a in range(0, len(lines), batch):
        sl = slice(a, a + batch)
        # HITRAN's 160-character records give the shift by air alone, which applies to no foreign gas here, and no
        # self shift, so the lines stay at their centres, as line_absorption keeps them for pure steam.
        centre = lines.nu[sl]
        i0 = np.rint((centre - grid.start) / grid.step).astype(np.int64)
        idx = i0[:, None] + offsets[None, :]
        d = grid.start + idx * grid.step - centre[:, None]
        l_, g_ = lorentz[sl, None], gauss[sl, None]
        shape = l_ / (math.pi * (d * d + l_ * l_))
        core = np.abs(d) < sp.VOIGT_CORE * g_
        if core.any():
            shape[core] = voigt_profile(d[core], np.broadcast_to(g_, d.shape)[core],
                                        np.broadcast_to(l_, d.shape)[core])
        vals = strength[sl, None] * (shape - base[sl, None])
        ok = (np.abs(d) <= cutoff) & (idx >= 0) & (idx < grid.size)
        out += np.bincount(np.where(ok, idx, 0).ravel(), weights=np.where(ok, vals, 0.0).ravel(),
                           minlength=grid.size)
    return np.maximum(out, 0.0)


class SteamOptics:
    """Water's lines above an intensity floor at 296 K, with MT_CKD's self continuum, for layers of pure steam."""

    def __init__(self, *, floor: float = 1e-30, continuum: bool = True, broad_pa: float = BROAD_PA,
                 cache: Path | None = None, processes: int = 1):
        self.lines = sp.load_lines('H2O', floor)
        self.sums = sp.PartitionSums(self.lines.gid)
        self.continuum = sp.WaterContinuum() if continuum else None
        self.broad_pa, self.cache, self.processes = broad_pa, (Path(cache) if cache else None), processes
        digest = hashlib.sha256()
        for name in ('nu', 'strength', 'gamma_self', 'elower', 'n_air', 'gid'):
            digest.update(np.ascontiguousarray(getattr(self.lines, name)).tobytes())
        inputs = {f['name']: f['sha256'] for f in fetch_inputs.manifest()['files']
                  if f['name'].startswith('hitran_q') or f['name'].startswith('mt_ckd')}
        digest.update(json.dumps(dict(floor=floor, continuum=continuum, broad_pa=broad_pa, cutoff=CUTOFF,
                                      kernel=sp.KERNEL_VERSION, voigt_core=sp.VOIGT_CORE, version=VERSION,
                                      inputs=inputs), sort_keys=True).encode())
        self.key = digest.hexdigest()[:16]

    def path(self, band: Band, p: float, t: float) -> Path | None:
        """The cache file of a layer state's cross-sections on the band, or None without a cache."""
        if self.cache is None:
            return None
        state = hashlib.sha256(repr((band, float(p).hex(), float(t).hex())).encode()).hexdigest()[:24]
        return self.cache / f'steam-{self.key}' / f'{state}.npy'

    def cross_section(self, band: Band, p: float, t: float) -> np.ndarray:
        """cm^2 per molecule of pure steam at (p Pa, t K) on the band's grid."""
        path = self.path(band, p, t)
        if path is not None and path.is_file():
            return np.load(path)
        grid = band.grid
        if p <= self.broad_pa:
            sigma = sp.line_absorption(grid, self.lines, self.sums, t, p, p, pedestal=True, cutoff=CUTOFF,
                                       coarse_factor=band.coarse_factor)
        else:
            sigma = broad_line_absorption(grid, self.lines, self.sums, t, p)
        if self.continuum is not None:
            sigma = sigma + self.continuum.cross_sections(grid.nu, t, p, 1.0)[0]
        sigma = sigma.astype(np.float32)
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            part = path.with_suffix(f'.part{np.random.randint(1 << 30)}.npy')
            np.save(part, sigma)
            part.replace(path)
        return sigma

    def layer_cross_sections(self, col: dict, band: Band) -> tuple[np.ndarray, np.ndarray]:
        states = list(zip(col['layer_p_pa'].tolist(), col['layer_t_k'].tolist()))
        if self.processes > 1:
            import multiprocessing as mp
            _WORKER['optics'] = self              # the forked workers inherit it, so each task sends its state alone
            with mp.get_context('fork').Pool(min(self.processes, len(states))) as pool:
                rows = pool.starmap(_cross_section, [(band, p, t) for p, t in states], chunksize=1)
        else:
            rows = [self.cross_section(band, p, t) for p, t in states]
        return band.grid.nu, np.vstack(rows)


_WORKER: dict = {}


def _cross_section(band: Band, p: float, t: float) -> np.ndarray:
    return _WORKER['optics'].cross_section(band, p, t)
