"""An atlas of a body's standing water at a given share of its surface.

One common water level above the geoid covers the share. For that level the atlas lists the separate seas and
lakes with their depths and the gazetteer's water names inside them, the islands with their summits, and how
much of each large named mare floods. The filling is hydrostatic, every closed depression below the level
counting as water; rainfall, runoff, evaporation, groundwater and crustal loading then move each shoreline.
"""
from __future__ import annotations
import numpy as np

from geography import basins as bs, nomenclature as nm

BODY_MIN_SHARE = 5e-4        # smallest sea or lake listed by name
ISLAND_MIN_KM2 = 400.0       # smallest island listed
ISLAND_NAME_RADIUS_KM = 60.0
MARE_CAP = 0.6               # inner share of each mare's radius used for its flooding fraction


def great_circle_km(lat0, lon0, lat, lon, radius_m):
    p0, l0, p, l = map(np.radians, (lat0, lon0, lat, lon))
    c = np.sin(p0) * np.sin(p) + np.cos(p0) * np.cos(p) * np.cos(l - l0)
    return radius_m / 1e3 * np.arccos(np.clip(c, -1.0, 1.0))


def cell_index(grid, lat, lon):
    i = np.clip(np.round((90.0 - np.asarray(lat)) * grid.pixels_per_degree - 0.5).astype(int), 0, grid.lat_deg.size - 1)
    j = np.round((np.asarray(lon) % 360.0) * grid.pixels_per_degree - 0.5).astype(int) % grid.lon_deg.size
    return i, j


def _centroids(labels, area, grid, n):
    la, lo = np.meshgrid(np.radians(grid.lat_deg), np.radians(grid.lon_deg), indexing='ij')
    lab, w = labels.ravel(), area.ravel()
    x = np.bincount(lab, w * (np.cos(la) * np.cos(lo)).ravel(), n)
    y = np.bincount(lab, w * (np.cos(la) * np.sin(lo)).ravel(), n)
    z = np.bincount(lab, w * np.sin(la).ravel(), n)
    return np.degrees(np.arctan2(z, np.hypot(x, y))), np.degrees(np.arctan2(y, x))


def bodies(height, area, level, grid, features=()):
    """Seas and lakes below a common level, largest first, with depth statistics and the gazetteer's water names."""
    _, lab = bs.seas(height, area, level, min_area_fraction=0.0)
    n = int(lab.max()) + 1
    surface = float(area.sum())
    depth = np.where(lab > 0, level - height, 0.0)
    a = np.bincount(lab.ravel(), area.ravel(), n)
    vol = np.bincount(lab.ravel(), (area * depth).ravel(), n)
    maxd = np.zeros(n)
    np.maximum.at(maxd, lab.ravel(), depth.ravel())
    clat, clon = _centroids(lab, area, grid, n)
    names = {}
    for f in features:
        if f['code'] in nm.WATER_CODES:
            i, j = cell_index(grid, f['lat'], f['lon'])
            if lab[i, j]:
                names.setdefault(int(lab[i, j]), []).append(f)
    out = []
    for c in np.argsort(-a):
        if c == 0 or a[c] < BODY_MIN_SHARE * surface:
            continue
        named = sorted(names.get(int(c), []), key=lambda f: -f['diameter_km'])
        out.append(dict(label=int(c), share=round(float(a[c] / surface), 5), area_km2=round(float(a[c] / 1e6)),
                        mean_depth_m=round(float(vol[c] / a[c])), max_depth_m=round(float(maxd[c])),
                        volume_km3=round(float(vol[c] / 1e9)), centroid=[round(float(clat[c]), 2), round(float(clon[c]), 2)],
                        water_names=[f['name'] for f in named]))
    wet_share = float(a[1:].sum() / surface)
    listed = sum(b['share'] for b in out)
    return out, lab, dict(water_share=round(wet_share, 4), small_lakes_share=round(wet_share - listed, 4))


def islands(height, area, level, grid, features=()):
    """Land regions above a common level: the main land mass and the islands, with their summits."""
    _, lab = bs.seas(-height, area, -level, min_area_fraction=0.0)
    n = int(lab.max()) + 1
    surface = float(area.sum())
    a = np.bincount(lab.ravel(), area.ravel(), n)
    a[0] = 0.0
    main = int(np.argmax(a))
    named = [f for f in features if f['code'] in ('MO', 'AA') and f['diameter_km'] >= 8.0]
    flat, flon = (np.array([f[k] for f in named]) for k in ('lat', 'lon'))
    out = []
    for c in np.argsort(-a):
        if c in (0, main) or a[c] < ISLAND_MIN_KM2 * 1e6:
            continue
        top = np.argmax(np.where(lab == c, height, -np.inf))
        i, j = np.unravel_index(top, height.shape)
        slat, slon = float(grid.lat_deg[i]), float(grid.lon_deg[j])
        slon = slon - 360.0 if slon > 180.0 else slon
        near = []
        if named:
            d = great_circle_km(slat, slon, flat, flon, grid.radius_m)
            fi, fj = cell_index(grid, flat, flon)
            on = (lab[fi, fj] == c) | (d < ISLAND_NAME_RADIUS_KM)
            near = [named[k]['name'] for k in sorted(np.flatnonzero(on), key=lambda k: -named[k]['diameter_km'])][:3]
        out.append(dict(label=int(c), area_km2=round(float(a[c] / 1e6)), summit_m=round(float(height[i, j] - level)),
                        summit=[round(slat, 2), round(slon, 2)], features=near))
    land_share = float(a.sum() / surface)
    return out, lab, dict(main_land_share=round(float(a[main] / surface), 4),
                          island_share=round(land_share - float(a[main] / surface), 4))


def mare_flooding(height, level, grid, features):
    """Share of each large mare's inner cap below the level, and its median height relative to the level."""
    la, lo = np.meshgrid(grid.lat_deg, grid.lon_deg, indexing='ij')
    w = np.cos(np.radians(la))
    rows = []
    for f in sorted((f for f in features if f['code'] in ('ME', 'OC') and f['diameter_km'] > 200.0),
                    key=lambda f: -f['diameter_km']):
        cap = great_circle_km(f['lat'], f['lon'], la, lo, grid.radius_m) <= MARE_CAP * f['diameter_km'] / 2
        rows.append(dict(name=f['name'], flooded=round(float((w * cap * (height < level)).sum() / (w * cap).sum()), 3),
                         median_height_m=round(float(np.median(height[cap]) - level))))
    return rows


def atlas(height, grid, share, features=()):
    """The atlas at a share of the surface: the common level, the global equivalent layer and the water's mass,
    the seas and lakes, the islands and the maria's flooding (names from `features`, the gazetteer's), and the
    arrays of heights and labels on the grid."""
    area = grid.cell_area_m2
    surface = float(area.sum())
    level = bs.level_for_area(height, area, share)
    water, wlab, wstats = bodies(height, area, level, grid, features)
    land, llab, lstats = islands(height, area, level, grid, features)
    _, vol = bs.level_curve(height, area, [level])
    result = dict(share=share, sea_level_m=level, global_layer_m=float(vol[0] / surface),
                  water_mass_kg=float(vol[0] * bs.WATER_DENSITY), **wstats, **lstats,
                  bodies=water, islands=land, mare_flooding=mare_flooding(height, level, grid, features),
                  grid=dict(pixels_per_degree=grid.pixels_per_degree))
    arrays = dict(height_m=height.astype(np.float32), water_label=wlab.astype(np.int32), land_label=llab.astype(np.int32),
                  lat_deg=grid.lat_deg, lon_deg=grid.lon_deg)
    return result, arrays
