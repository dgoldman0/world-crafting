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
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from geography import basins, drainage, topography as tp

from .data import Manifest, parse_pin
from .derive import DAY_S, rotation_rate
from .spec import Library, SpecError

GM_AGREEMENT = 1e-6            # the gravity field's GM against the world's body.gm_m3_s2, relative
RADIUS_AGREEMENT = 1e-2        # the heights' reference sphere against the world's mean radius, relative
SYNCHRONOUS = 1e-2             # the rotation against the two-body period about a host fixed in the sky, relative:
                               # the Sun's pull lengthens the Moon's month by 0.14% beyond the two-body period
CLIMATOLOGY_SCHEMAS = ('terluna.climate.gcm-climatology/1',)    # Terluna's, until the lab's diagnostics write their own
CLIMATOLOGY_FIELDS = ('lat', 'lon', 'lsm', 'pr_mm_day', 'evap_mm_day')


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
    spin_days = _number(world.get('rotation', {}).get('sidereal_period_days'), f'{world.get("id")}: rotation.sidereal_period_days')
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
