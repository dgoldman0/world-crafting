"""Geoid synthesis, level curves and the depression tree on synthetic topography."""
from __future__ import annotations
import math
import unittest
import numpy as np

from geography import topography as tp, basins as bs

RADIUS = 1737400.0
SURFACE = 4 * math.pi * RADIUS**2


def synthetic(ppd=2):
    grid = tp.Grid.globe(ppd, RADIUS)
    la, lo = np.meshgrid(np.radians(grid.lat_deg), np.radians(grid.lon_deg), indexing='ij')

    def distance(lat0, lon0):
        c = np.sin(la) * math.sin(math.radians(lat0)) + np.cos(la) * math.cos(math.radians(lat0)) * np.cos(lo - math.radians(lon0))
        return np.degrees(np.arccos(np.clip(c, -1, 1)))
    return grid, distance


class GeoidTests(unittest.TestCase):
    def test_legendre_orthonormal(self):
        x, w = np.polynomial.legendre.leggauss(300)
        u = np.sqrt(1 - x * x)
        for m in (0, 1, 13, 120):
            p = tp.legendre_column(m, 150, x, u)
            gram = (p * w) @ p.T * (0.5 if m == 0 else 0.25)
            self.assertLess(np.abs(gram - np.eye(gram.shape[0])).max(), 1e-10)

    def test_p20_closed_form(self):
        t = np.linspace(-1, 1, 11)
        p = tp.legendre_column(0, 2, t, np.sqrt(1 - t * t))
        self.assertTrue(np.allclose(p[2], math.sqrt(5) * (3 * t * t - 1) / 2))

    def test_cell_areas_cover_the_sphere(self):
        grid, _ = synthetic(3)
        self.assertAlmostEqual(grid.cell_area_m2.sum() / SURFACE, 1.0, delta=1e-12)
        self.assertAlmostEqual(tp.Grid.globe(3, 2 * RADIUS).cell_area_m2.sum() / SURFACE, 4.0, delta=1e-12)


class StorageTests(unittest.TestCase):
    def test_level_curve_of_a_flat_bowl(self):
        grid, distance = synthetic()
        area = grid.cell_area_m2
        bowl = distance(0.0, 180.0) < 30.0
        height = np.where(bowl, -1000.0, 0.0)
        frac, vol = bs.level_curve(height, area, [-500.0])
        cap = area[bowl].sum()
        self.assertAlmostEqual(frac[0], cap / SURFACE, delta=1e-12)
        self.assertAlmostEqual(vol[0] / (500.0 * cap), 1.0, delta=1e-12)
        level = bs.level_for_volume(height, area, 250.0 * cap)
        self.assertAlmostEqual(level, -750.0, delta=1e-3)

    def test_two_bowls_spill_at_the_saddle(self):
        grid, distance = synthetic()
        area = grid.cell_area_m2
        deep = distance(0.0, 100.0) < 20.0
        shallow = distance(0.0, 150.0) < 20.0
        saddle = (distance(0.0, 125.0) < 6.0)
        height = np.full(deep.shape, 1000.0)
        height[deep] = -2000.0
        height[shallow] = -800.0
        height[saddle & ~deep & ~shallow] = 300.0
        named = {'Deep': (0.0, 100.0), 'Shallow': (0.0, 150.0)}
        records = bs.depression_tree(height, area, grid.lat_deg, grid.lon_deg, named)
        joins = bs.major_merges(records, 1e-3)
        level, parts = joins[0]
        self.assertAlmostEqual(level, 300.0)
        vols = sorted(d.volume_m3 for d in parts)
        self.assertAlmostEqual(vols[0] / ((300.0 + 800.0) * area[shallow].sum()), 1.0, delta=1e-9)
        self.assertAlmostEqual(vols[1] / ((300.0 + 2000.0) * area[deep].sum()), 1.0, delta=1e-9)
        self.assertEqual(sorted(d.names for d in parts), [('Deep',), ('Shallow',)])
        self.assertAlmostEqual(parts[0].gel_m, parts[0].volume_m3 / SURFACE, delta=1e-9)
        self.assertEqual(bs.label(parts[0], named), 'Deep')
        sizes, _ = bs.seas(height, area, 0.0)
        self.assertEqual(len(sizes), 2)
        sizes, _ = bs.seas(height, area, 500.0)
        self.assertEqual(len(sizes), 1)


if __name__ == '__main__':
    unittest.main()
