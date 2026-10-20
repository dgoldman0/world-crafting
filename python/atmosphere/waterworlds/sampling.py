"""Stage 9's test of spectral sampling on Figure 2's world: its emitting factor on the grid Schaefer et al. (2016)
describe for the line-by-line model the paper used, 5,000 points from 1 cm^-1 to five times the Wien peak of the
surface's Planck curve, beside the factor on the lab's own bands and the paper's. Each coarse point takes the lab's
cross-section at the nearest point of the band that holds it, as a line-by-line code on a coarse grid samples its
lines; the column, its optics and its levels are the comparison's for Figure 2.

    python -m atmosphere.waterworlds.sampling --store STORE --table TABLE.json --figures FIGURES.json

writes the test to STORE/products/steam-sampling/<key>/sampling.json, its key covering the table's optics, the
figures' file and the producer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

from atmosphere.radiative_convective import spectroscopy as sp
from atmosphere.waterworlds import comparison as cp, figures as fg, radiating as rd, steam, steam_optics as so
from atmosphere.waterworlds.body import Waterworld

SCHEMA = 'world-crafting.waterworlds.steam-sampling/1'
POINTS = 5000
WIEN = 2.821439372 / sp.C2       # the Planck curve's peak in wavenumber, cm^-1 per K
PRODUCER_FILES = ('atmosphere/waterworlds/sampling.py', 'atmosphere/waterworlds/comparison.py',
                  'atmosphere/waterworlds/radiating.py', 'atmosphere/waterworlds/steam.py',
                  'atmosphere/waterworlds/steam_optics.py', 'atmosphere/waterworlds/hitemp.py',
                  'atmosphere/radiative_convective/longwave.py', 'atmosphere/radiative_convective/spectroscopy.py')


def coarse_grid(t_s: float, points: int = POINTS) -> np.ndarray:
    """Schaefer and colleagues' grid: `points` wavenumbers from 1 cm^-1 to five times the Wien peak at t_s."""
    return np.linspace(1.0, 5 * WIEN * t_s, points)


class Sampled:
    """The optics' cross-sections at a coarse grid's points, each from the nearest point of the band that holds it,
    the thermal band first where the bands meet."""

    def __init__(self, optics, nu: np.ndarray, bands=so.BANDS):
        self.optics, self.nu, self.bands = optics, np.asarray(nu, dtype=float), bands

    def layer_cross_sections(self, col: dict, band=None) -> tuple[np.ndarray, np.ndarray]:
        out = np.full((len(col['layer_p_pa']), self.nu.size), np.nan)
        free = np.ones(self.nu.size, dtype=bool)
        for b in self.bands:
            grid = b.grid
            inside = free & (self.nu >= grid.start) & (self.nu <= grid.stop)
            if inside.any():
                _, sigma = self.optics.layer_cross_sections(col, b)
                out[:, inside] = sigma[:, np.rint((self.nu[inside] - grid.start) / grid.step).astype(np.int64)]
                free &= ~inside
        if free.any():
            raise ValueError("the coarse grid reaches beyond the optics' bands")
        return self.nu, out


def emitting_factors(optics, temperatures, *, earth_masses: float = 0.12, points: int = POINTS) -> list[dict]:
    """Figure 2's world at each surface temperature: the emitting factor on the coarse grid and on the lab's bands."""
    world = Waterworld(earth_masses)
    rows = []
    for t_s in temperatures:
        col = steam.column(world, t_s, optical_gravity='surface')
        full = rd.surfaces(col, rd.column_spectra(col, optics, so.BANDS))
        coarse = rd.surfaces(col, rd.column_spectra(col, Sampled(optics, coarse_grid(t_s, points)), (None,)))
        rows.append(dict(t_s=float(t_s), lab=full['lw_factor'], coarse=coarse['lw_factor'], olr=full['olr'],
                         olr_coarse=coarse['olr']))
    return rows


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--store', type=Path, required=True)
    parser.add_argument('--table', type=Path, required=True)
    parser.add_argument('--figures', type=Path, required=True)
    args = parser.parse_args(argv)
    record = cp.tb.read(args.table)['optics']
    optics = so.SteamOptics(cache=args.store / 'caches' / 'steam-optics', lines=record.get('source', 'hitran'),
                            hold=record.get('hold', False), store=args.store)
    if optics.key != record['key']:
        raise SystemExit(f"the optics' key {optics.key} differs from the table's, {record['key']}")
    figures_bytes = args.figures.read_bytes()
    paper = fg.read(args.figures)['figure2']['emitting']
    temperatures = (250.0, 300.0, 350.0, 400.0, 450.0, 500.0, 550.0, 598.0)
    rows = emitting_factors(optics, temperatures)
    for r in rows:
        r['paper'] = float(cp._paper(paper, r['t_s']))
    root = Path(__file__).resolve().parents[2]
    inputs = dict(optics_key=optics.key, figures_sha256=hashlib.sha256(figures_bytes).hexdigest(), points=POINTS,
                  producer={n: hashlib.sha256((root / n).read_bytes()).hexdigest() for n in PRODUCER_FILES})
    k = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()
    out = args.store / 'products' / 'steam-sampling' / k[:16] / 'sampling.json'
    print(out, fg.write(out, dict(schema=SCHEMA, inputs=inputs, rows=rows)))
    for r in rows:
        print(f"{r['t_s']:.0f} K: lab {r['lab']:.4f}, coarse {r['coarse']:.4f}, paper {r['paper']:.4f}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
