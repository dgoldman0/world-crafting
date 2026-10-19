"""A world's heights above its geoid, from the files its `surface.geometry` pins (lab/design/world_spec.md, the
surface fields). python/geography/topography.py reads the files and synthesises the geoid; this module takes from
the world's specification what that needs, finds each file by what its PDS3 label describes, and checks the
files against the world:

- **The files.** The pin's manifest entry holds a height image and a gravity table, each with its PDS3 label, and
  each label points at its own file by name. The heights are radii less a reference sphere, as LOLA's LDEM labels
  define them; the image reader refuses heights measured from a geoid already, as MOLA's MEGDR topography is.
- **The geoid** takes the field to `surface.geoid_degree`, the world's spin at its sidereal rotation, and, where
  the world states `surface.tide`, the permanent tide of a host fixed in its sky: the host's GM from the host's
  own world, and the time mean of its degree-2 potential over the orbit that `host.semi_major_axis_m`,
  `host.eccentricity` and `host.inclination_to_equator_deg` describe. A host stays fixed in the sky only for a
  rotation synchronous with the orbit, so the module checks the rotation against the orbit's two-body period.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from geography import topography as tp

from .data import Manifest, parse_pin
from .derive import DAY_S, rotation_rate
from .spec import Library, SpecError

GM_AGREEMENT = 1e-6            # the gravity field's GM against the world's body.gm_m3_s2, relative
RADIUS_AGREEMENT = 1e-2        # the heights' reference sphere against the world's mean radius, relative
SYNCHRONOUS = 1e-2             # the rotation against the two-body period about a host fixed in the sky, relative:
                               # the Sun's pull lengthens the Moon's month by 0.14% beyond the two-body period


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
