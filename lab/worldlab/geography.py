"""A world's heights above its geoid, from the files its `surface.geometry` pins, and a scenario's seas and first
lakes on them (lab/design/world_spec.md, the surface and water fields). python/geography/ reads the files,
synthesises the geoid and routes the runoff; this module takes from the specifications what those need, finds
each file by what its PDS3 label describes, and checks the files against the world:

- **The files.** The pin's manifest entry holds a height image and a gravity table, each with its PDS3 label, and
  each label points at its own file by name. The heights are radii less a reference sphere, as LOLA's LDEM labels
  define them; the image reader refuses heights measured from a geoid already, as MOLA's MEGDR topography is.
- **The geoid** takes the field to `surface.geoid_degree`, the world's spin at its sidereal rotation, and, where
  the world states `surface.tide`, the permanent tide of a host fixed in its sky: the host's GM from the host's
  own world, and the time mean of its degree-2 potential over the orbit that `host.semi_major_axis_m`,
  `host.eccentricity` and `host.inclination_to_equator_deg` describe. A host stays fixed in the sky only for a
  rotation synchronous with the orbit, so the module checks the rotation against the orbit's two-body period.
- **The water.** A scenario's seas flood the heights to `water.seas_share` at one common level, every cell below it
  counting as sea; its first lakes are routed by python/geography/drainage.py from the runoff of the climatology
  `water.lakes_start` pins, over the heights with the seas as outlets, or there are none. The climatology is taken
  as the scenario's own runoff; the module checks its schema, fields and grid.
- **The model's grid.** The water and the land are averaged from the heights' cells onto a GCM's Gaussian grid,
  area for area: the land's share of each cell, the land's mean height above the water level, and the wet part's
  mean water surface above that level and its depth.
- **The lowest point.** The air's pressure at the lowest exposed surface follows from the scenario's pressure at
  its reference level, an equipotential, by isothermal hydrostatics at its reference temperature.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from geography import basins, drainage, topography as tp

from . import derive
from .data import Manifest, parse_pin
from .derive import DAY_S, rotation_rate
from .spec import Library, SpecError

GM_AGREEMENT = 1e-6            # the gravity field's GM against the world's body.gm_m3_s2, relative
RADIUS_AGREEMENT = 1e-2        # the heights' reference sphere against the world's mean radius, relative
SYNCHRONOUS = 1e-2             # the rotation against the two-body period about a host fixed in the sky, relative:
                               # the Sun's pull lengthens the Moon's month by 0.14% beyond the two-body period
CLIMATOLOGY_SCHEMAS = ('terluna.climate.gcm-climatology/1',)    # Terluna's, until the lab's diagnostics write their own
CLIMATOLOGY_FIELDS = ('lat', 'lon', 'lsm', 'pr_mm_day', 'evap_mm_day')
REFERENCE_LEVELS = ('water', 'sea')          # the seas' common level, and the geoid


@dataclass(frozen=True)
class Water:
    """A scenario's standing water on its world's heights: the seas' common level above the geoid (m), the cells
    below it, the lakes' cells above it as flat indices into the heights' grid, each with its surface above the
    geoid and whether its lake spills, and the record of the routing."""
    level_m: float
    sea: np.ndarray
    lake_cell: np.ndarray
    lake_level_m: np.ndarray
    lake_spills: np.ndarray
    record: dict


@dataclass(frozen=True)
class ModelSurface:
    """A scenario's surface on a GCM's Gaussian grid, laid out as PlaSim's is, its rows from the north and its columns
    centred on 0 E: each cell's land fraction, the land's mean height above the water level, the wet part's mean
    water surface above that level and its mean depth (m), and the cell's share of the surface."""
    lat_deg: np.ndarray
    lon_deg: np.ndarray
    land_fraction: np.ndarray
    land_elevation_m: np.ndarray
    water_surface_m: np.ndarray
    water_depth_m: np.ndarray
    cell_area_fraction: np.ndarray
    record: dict


@dataclass(frozen=True)
class Heights:
    """Topography above the geoid and the geoid above the reference sphere (m), on the heights' grid, with the
    record of the files read and the geoid's terms."""
    height_m: np.ndarray
    geoid_m: np.ndarray
    grid: tp.Grid
    record: dict


def surface_files(world: dict, *, manifest: Manifest | None = None, store: Path | None = None) -> dict:
    """The label and data paths of the world's height image ('heights') and gravity table ('gravity'), among the
    files of its surface.geometry pin, each found by the object its label points at."""
    where = f'{world.get("id", "the world")}: surface.geometry'
    value = world.get('surface', {}).get('geometry')
    if not isinstance(value, str) or value in ('unchosen', 'model-default', 'none'):
        raise SpecError(f'{where} is a pinned set of files, where the world states {value!r}')
    pin = parse_pin(value)
    if pin.entry is not None:
        raise SpecError(f'{where}: a set of files takes no # entry, where the world names {pin.entry!r}')
    paths = (manifest or Manifest()).paths(pin, store=store)
    by_name = {name.lower(): path for name, path in paths.items()}
    found = {}
    for name, path in sorted(paths.items()):
        if Path(name).suffix.lower() != '.lbl':
            continue
        label = tp.read_pds3_label(path)
        for kind, obj in (('heights', 'IMAGE'), ('gravity', 'SHADR_HEADER_TABLE')):
            target = tp.pointed_file(label, obj)
            if target is None:
                continue
            if kind in found:
                raise SpecError(f'{where}: two labels describe {kind}, {found[kind][0].name} and {name}')
            if target.lower() not in by_name:
                raise SpecError(f'{where}: {name} describes {target}, which the pin holds no file of')
            found[kind] = (path, by_name[target.lower()])
    missing = [kind for kind in ('heights', 'gravity') if kind not in found]
    if missing:
        raise SpecError(f'{where}: the pin\'s labels describe no {" or ".join(missing)}, where heights above a '
                        'sphere take a gravity field for their geoid')
    return found


def static_tide(world: dict, library: Library | None = None) -> tp.Tide | None:
    """The permanent tide of `surface.tide`, or None where the world states none."""
    tide = world.get('surface', {}).get('tide')
    if tide is None:
        return None
    where = f'{world.get("id", "the world")}: surface.tide'
    if not isinstance(tide, dict):
        raise SpecError(f'{where} is a table, where the world states {tide!r}')
    if tide.get('from') != 'host':
        raise SpecError(f'{where}.from: a tide comes from the world\'s host, where the world states {tide.get("from")!r}')
    host = world.get('host', {})
    if 'id' not in host:
        raise SpecError(f'{where}: the world names no host')
    gm = _number((library or Library()).world(host['id']).get('body', {}).get('gm_m3_s2'), f'{host["id"]}: body.gm_m3_s2')
    a = _number(host.get('semi_major_axis_m'), f'{where}: host.semi_major_axis_m')
    e = _number(host.get('eccentricity'), f'{where}: host.eccentricity', strict=False, below=1.0)
    inclination = _number(host.get('inclination_to_equator_deg'), f'{where}: host.inclination_to_equator_deg',
                          strict=False, below=90.0)
    k2 = _number(tide.get('love_k2'), f'{where}.love_k2', strict=False)
    lon0 = _number(tide.get('sub_longitude_deg'), f'{where}.sub_longitude_deg', low=None)
    gm_world = _number(world.get('body', {}).get('gm_m3_s2'), f'{world.get("id")}: body.gm_m3_s2')
    orbit_days = 2 * math.pi * math.sqrt(a**3 / (gm + gm_world)) / DAY_S
    spin_days = _number(derive.sidereal_period_days(world), f'{world.get("id")}: rotation.sidereal_period_days')
    if abs(spin_days / orbit_days - 1.0) > SYNCHRONOUS:
        raise SpecError(f'{where}: a host stays fixed in the sky only for a rotation synchronous with the orbit, where '
                        f'the world turns in {spin_days} d against a two-body period of {orbit_days:.4f} d')
    return tp.Tide(gm, a, e, inclination, k2, lon0)


def heights(world: dict, library: Library | None = None, *, manifest: Manifest | None = None,
            store: Path | None = None) -> Heights:
    """The world's topography above its geoid, from its surface.geometry pin and its own values."""
    where = f'{world.get("id", "the world")}: surface'
    degree = world.get('surface', {}).get('geoid_degree')
    if isinstance(degree, bool) or not isinstance(degree, int) or degree < 2:
        raise SpecError(f'{where}.geoid_degree is a degree from 2, where the world states {degree!r}')
    files = surface_files(world, manifest=manifest, store=store)
    height, grid, info = tp.read_pds_image(*files['heights'])
    radius = _number(world.get('body', {}).get('radius_m'), f'{world.get("id")}: body.radius_m')
    if abs(grid.radius_m / radius - 1.0) > RADIUS_AGREEMENT:
        raise SpecError(f'{where}: heights above a {grid.radius_m} m sphere on a world of radius {radius} m')
    field = tp.read_shadr(*files['gravity'], degree)
    gm = _number(world.get('body', {}).get('gm_m3_s2'), f'{world.get("id")}: body.gm_m3_s2')
    if abs(field.gm_m3_s2 / gm - 1.0) > GM_AGREEMENT:
        raise SpecError(f'{where}: a gravity field of GM {field.gm_m3_s2} on a world of GM {gm}')
    tide = static_tide(world, library)
    omega = rotation_rate(world)
    topography, geoid = tp.height_above_geoid(height, grid, field, degree, omega, tide)
    record = dict(heights=files['heights'][1].name, gravity=files['gravity'][1].name, **info,
                  geoid_degree=degree, rotation_rate_rad_s=omega, field_gm_m3_s2=field.gm_m3_s2,
                  field_reference_radius_m=field.reference_radius_m,
                  tide=None if tide is None else dict(
                      gm_m3_s2=tide.gm_m3_s2, semi_major_axis_m=tide.semi_major_axis_m, eccentricity=tide.eccentricity,
                      inclination_deg=tide.inclination_deg, love_k2=tide.love_k2, sub_longitude_deg=tide.sub_lon_deg,
                      coefficients=list(tp.tide_coefficients(tide.eccentricity, tide.inclination_deg))))
    return Heights(topography, geoid, grid, record)


def climatology(pin, *, manifest: Manifest | None = None, store: Path | None = None) -> tuple[dict, dict, str]:
    """The fields of a pinned GCM climatology that a routing reads: its grid's latitudes and ascending east
    longitudes (degrees), its land-sea mask and its means of precipitation and evaporation (mm/day) on that grid,
    with its metadata and its sha256."""
    path = (manifest or Manifest()).path(pin, store=store)
    with np.load(path) as data:
        meta = json.loads(str(data['metadata'])) if 'metadata' in data.files else {}
        if meta.get('schema') not in CLIMATOLOGY_SCHEMAS:
            raise SpecError(f'{pin}: a climatology of schema {meta.get("schema")!r}, where the lab reads {CLIMATOLOGY_SCHEMAS}')
        missing = [name for name in CLIMATOLOGY_FIELDS if name not in data.files]
        if missing:
            raise SpecError(f'{pin}: a climatology without {missing}')
        fields = {name: np.asarray(data[name], dtype=float) for name in CLIMATOLOGY_FIELDS}
    lat, lon = fields['lat'], fields['lon']
    shape = (lat.size, lon.size)
    if lat.ndim != 1 or lon.ndim != 1 or any(fields[k].shape != shape for k in ('lsm', 'pr_mm_day', 'evap_mm_day')):
        raise SpecError(f'{pin}: fields of shapes {[fields[k].shape for k in CLIMATOLOGY_FIELDS]} on a {shape} grid')
    ordered = np.all(np.diff(lat) > 0) or np.all(np.diff(lat) < 0)
    if not (np.all(np.diff(lon) > 0) and lon[0] >= 0.0 and lon[-1] < 360.0) or not ordered:
        raise SpecError(f'{pin}: a grid of longitudes {lon[0]}..{lon[-1]}, where the routing takes them ascending from '
                        '0 E and the latitudes in order')
    return fields, meta, hashlib.sha256(Path(path).read_bytes()).hexdigest()


def water(world: dict, scenario: dict, topography: Heights | None = None, library: Library | None = None, *,
          manifest: Manifest | None = None, store: Path | None = None) -> Water:
    """The scenario's seas, from the world's heights flooded to `water.seas_share`, and its first lakes, routed from
    the runoff of the climatology `water.lakes_start` pins over the heights with the seas as outlets, or none where
    `water.lakes` is "none". This function floods the heights and routes runoff; the other forms world_spec.md
    allows the seas and lakes, pinned files among them, take functions of their own."""
    where = f'{scenario.get("id", "the scenario")}: water'
    if scenario.get('world') != world.get('id'):
        raise SpecError(f'{where}: a scenario of the world {scenario.get("world")!r} on the world {world.get("id")!r}')
    spec = scenario.get('water', {})
    share = _number(spec.get('seas_share'), f'{where}.seas_share', below=1.0)
    if spec.get('seas') != 'from-heights':
        raise SpecError(f'{where}.seas: this function floods the heights ("from-heights"), where the scenario states '
                        f'{spec.get("seas")!r}')
    lakes = spec.get('lakes')
    if lakes not in ('from-runoff', 'none'):
        raise SpecError(f'{where}.lakes: this function routes runoff ("from-runoff") or makes none ("none"), where the '
                        f'scenario states {lakes!r}')
    if lakes == 'from-runoff':
        start = spec.get('lakes_start')
        if not isinstance(start, str) or start in ('unchosen', 'model-default', 'none'):
            raise SpecError(f'{where}.lakes_start is a pinned climatology, where the scenario states {start!r}')
        pin = parse_pin(start)
        if pin.entry is not None:
            raise SpecError(f'{where}.lakes_start: a climatology takes no # entry, where the scenario names {pin.entry!r}')
    found = topography or heights(world, library, manifest=manifest, store=store)
    area = found.grid.cell_area_m2
    flat = area.ravel()
    level = basins.level_for_area(found.height_m, area, share)
    if lakes == 'none':
        sea = found.height_m.astype(np.float32) < level         # the drainage's outlets, as it compares them
        record = dict(seas=dict(stated_share=share, level_m=level, share=float(flat[sea.ravel()].sum() / flat.sum())),
                      lakes=None)
        return Water(level, sea, np.zeros(0, np.int32), np.zeros(0, np.float32), np.zeros(0, bool), record)
    fields, meta, sha256 = climatology(pin, manifest=manifest, store=store)
    _, routing = drainage.compute(found.height_m, found.grid, level, fields)
    sea = routing['outlet'].reshape(found.height_m.shape)
    arrays = drainage.lake_arrays(routing)
    summary = drainage.summarise(level, found.height_m, found.grid, routing)
    record = dict(
        seas=dict(stated_share=share, level_m=level, share=float(flat[sea.ravel()].sum() / flat.sum())),
        lakes=dict(share=float(flat[arrays['lake_cell']].sum() / flat.sum()), cells=int(arrays['lake_cell'].size),
                   **{k: summary['lakes'][k] for k in ('bodies', 'closed_bodies', 'volume_km3', 'median_depth_m')}),
        rivers={k: v for k, v in summary['rivers'].items() if k != 'largest'}, depressions=summary['depressions'],
        runoff=dict(pin=start, sha256=sha256, run=meta.get('run'), years=meta.get('years')))
    return Water(level, sea, arrays['lake_cell'], arrays['lake_level_m'], arrays['lake_spills'], record)


def gaussian_latitudes(rows: int) -> tuple[np.ndarray, np.ndarray]:
    """A Gaussian grid's latitudes (degrees, north first) and its rows' edges in sin(latitude), the running sums of the
    Gauss-Legendre weights from the north, so that each row covers its weight's half of the sphere. Terluna's
    climate/gcm/boundary.py (186b294) builds its Gaussian grids the same way."""
    x, w = np.polynomial.legendre.leggauss(rows)
    order = np.argsort(-x)
    edges = np.clip(1.0 - np.concatenate([[0.0], np.cumsum(w[order])]), -1.0, 1.0)
    return np.degrees(np.arcsin(x[order])), edges


def _overlap(source, target):
    """The lengths shared by each target interval (rows) and each source interval (columns); edges in either order.
    Terluna's boundary.py (186b294) has the same."""
    s0, s1 = np.minimum(source[:-1], source[1:]), np.maximum(source[:-1], source[1:])
    t0, t1 = np.minimum(target[:-1], target[1:]), np.maximum(target[:-1], target[1:])
    return np.clip(np.minimum(t1[:, None], s1[None, :]) - np.maximum(t0[:, None], s0[None, :]), 0.0, None)


def model_surface(water_: Water, topography: Heights, rows: int) -> ModelSurface:
    """The scenario's water and land averaged, area for area, from the heights' cells onto the Gaussian grid of
    `rows` latitudes and twice as many longitudes, as Terluna's boundary.regrid (186b294) averages its own products.
    A cell without land holds a land height of 0, and a cell without water a water surface and depth of 0."""
    grid, level, h = topography.grid, water_.level_m, topography.height_m
    if rows not in derive.TRUNCATION_BY_LATITUDES:
        raise SpecError(f'a Gaussian grid of {rows} rows, where ExoPlaSim\'s grids hold {sorted(derive.TRUNCATION_BY_LATITUDES)}')
    ppd = grid.pixels_per_degree
    half = 0.5 / ppd
    if (h.shape != (180 * ppd, 360 * ppd) or grid.lat_deg[0] != 90.0 - half or grid.lon_deg[0] != half
            or water_.sea.shape != h.shape):
        raise SpecError(f'heights of shape {h.shape} from {grid.lat_deg[0]} N and {grid.lon_deg[0]} E, where the model\'s '
                        'grid takes a global grid, north first, from 0 E, with its seas on it')
    lat, row_edges = gaussian_latitudes(rows)
    columns = 2 * rows
    column_edges = np.linspace(0.0, 360.0, columns + 1) - 180.0 / columns
    by_row = _overlap(np.sin(np.radians(np.concatenate([[90.0], grid.lat_deg - half]))), row_edges)
    by_column = sum(_overlap(np.concatenate([[0.0], grid.lon_deg + half]) + shift, column_edges)
                    for shift in (-360.0, 0.0, 360.0))
    wet = water_.sea.copy()
    wet.ravel()[water_.lake_cell] = True
    surface = np.zeros(h.shape)
    surface.ravel()[water_.lake_cell] = water_.lake_level_m - level
    dry = (~wet).astype(float)

    def mean(field, weight):
        total, weights = by_row @ (field * weight) @ by_column.T, by_row @ weight @ by_column.T
        return np.where(weights > 0, total / np.maximum(weights, 1e-300), 0.0)

    area = by_row @ np.ones(h.shape) @ by_column.T
    land = (by_row @ dry @ by_column.T) / area
    cells = area / area.sum()
    elevation = mean(h - level, dry)
    water_surface = mean(surface, 1.0 - dry)
    # A lake's surface is stored in single precision, so the cell its surface was set from can stand a fraction of a
    # millimetre above it.
    depth = mean(np.maximum(level + surface - h, 0.0), 1.0 - dry)
    record = dict(rows=rows, columns=columns, land_share=float((land * cells).sum()),
                  land_elevation_max_m=float(elevation.max()), water_surface_max_m=float(water_surface.max()))
    return ModelSurface(lat, column_edges[:-1] + 180.0 / columns, land, elevation, water_surface, depth, cells, record)


def lowest_level_pressure(world: dict, scenario: dict, water_: Water, topography: Heights) -> dict:
    """The air's pressure at the lowest exposed surface, the sea's or a lake's water or the dry ground, from the
    scenario's surface pressure at its reference level, the seas' common level ("water") or the geoid ("sea"), by
    isothermal hydrostatics at its reference temperature with the world's surface gravity. Returns
    `lowest_level_pressure_hpa`, in the registry's name, with `reference_level`, `reference_level_m` and
    `lowest_surface_m` (m above the geoid), and, where the two heights differ, the gravity, the dry air's gas constant
    and the temperature taken."""
    air = scenario.get('air', {})
    where = f'{scenario.get("id", "the scenario")}: air.reference_level'
    reference = air.get('reference_level')
    if reference == 'mean-radius':
        raise SpecError(f'{where}: "mean-radius" names a sphere, which crosses the equipotentials of a flattened world; '
                        'the lab reads the pressure at the seas\' level ("water") or at the geoid ("sea")')
    if reference not in REFERENCE_LEVELS:
        raise SpecError(f'{where} is "water", the seas\' level, or "sea", the geoid, where the scenario states {reference!r}')
    reference_m = water_.level_m if reference == 'water' else 0.0
    if water_.sea.any():
        # Every cell below the seas' level is sea, so the seas' surface is the lowest exposed, whatever the single
        # precision of the flooding and the lakes leaves of the cells beside it.
        lowest_m = water_.level_m
    else:
        lake = np.zeros(water_.sea.shape, bool)
        lake.ravel()[water_.lake_cell] = True
        lowest_m = min(float(topography.height_m[~lake].min(initial=np.inf)),
                       float(water_.lake_level_m.min(initial=np.inf)))
    pressure = _number(air.get('surface_pressure_pa'), f'{scenario.get("id")}: air.surface_pressure_pa')
    record = dict(reference_level=reference, reference_level_m=reference_m, lowest_surface_m=lowest_m)
    if lowest_m != reference_m:
        gravity = derive.gravity(world)
        gas = derive.specific_gas_constant(derive.molar_mass_g_mol(derive.mole_fractions(scenario)))
        temperature = derive.reference_temperature_k(scenario)
        pressure *= math.exp(gravity * (reference_m - lowest_m) / (gas * temperature))
        record.update(gravity_m_s2=gravity, gas_constant_j_kg_k=gas, temperature_k=temperature)
    return dict(lowest_level_pressure_hpa=pressure / 100.0, **record)


def _number(value, where: str, *, low: float | None = 0.0, strict: bool = True, below: float | None = None) -> float:
    """A finite number above `low` (from it, where `strict` is false) and below `below`; `low` None takes either sign."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise SpecError(f'{where} is a number, where the specification states {value!r}')
    if low is not None and (value <= low if strict else value < low):
        raise SpecError(f'{where} is a number {"above" if strict else "of at least"} {low}, where the specification '
                        f'states {value!r}')
    if below is not None and not value < below:
        raise SpecError(f'{where} is a number below {below}, where the specification states {value!r}')
    return float(value)
