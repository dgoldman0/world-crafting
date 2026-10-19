"""Topography above an equipotential surface, from a body's height grid and its gravity field.

A water surface at rest follows an equipotential, which a height above a sphere only approximates. The geoid
here is a spherical-harmonic gravity field (degrees 2 to n_max, fully normalized coefficients), plus the
body's centrifugal potential and, for a body that keeps one face to its host, the host's permanent tide scaled
by 1 + k2, for a field whose degree-2 terms leave the permanent tide out (as GRAIL's GL0420A does). The
permanent tide is the time mean of the host's degree-2 potential over its orbit, whose eccentricity and tilt to
the body's equator move the host about the mean sub-host point (the optical librations). Heights are the grid's
radii less the geoid's, relative to the grid's reference sphere; the geoid has zero mean over the sphere, so the
height datum is a constant offset that leaves areas and volumes unchanged.

The readers go by format, each through its PDS3 label: a global simple-cylindrical image (read_pds_image) and
a SHADR table of spherical-harmonic coefficients (read_shadr). On the Moon, LOLA's heights are in the
mean-Earth/polar-axis frame and GL0420A in DE421's principal-axis frame; their ~0.02 degree offset, 0.6 km at
the surface, is ignored, far below the 33 km shortest wavelength of a degree-330 geoid.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import re
from pathlib import Path
import numpy as np

# PDS3 sample types, as numpy's byte orders and kinds.
SAMPLE_TYPES = {'LSB_INTEGER': '<i', 'MSB_INTEGER': '>i', 'LSB_UNSIGNED_INTEGER': '<u',
                'MSB_UNSIGNED_INTEGER': '>u', 'PC_REAL': '<f', 'IEEE_REAL': '>f', 'MAC_REAL': '>f'}
DEGREES = dict(deg=1.0, degree=1.0, degrees=1.0)
PIXELS = dict(pix=1.0, pixel=1.0, pixels=1.0)
METRES = dict(m=1.0, meter=1.0, meters=1.0, metre=1.0, metres=1.0, km=1e3, kilometer=1e3, kilometers=1e3)
TIDE_SAMPLES = 512             # mean anomalies in the tide's average, and a quarter as many perigee angles
_TOKEN = re.compile(r'"[^"]*"|\'[^\']*\'|<[^>]*>|[=(){},]|[^\s=(){},<>"\']+')
_BASED = re.compile(r'([+-]?)(\d+)#([0-9A-Za-z]+)#')


class Bits(int):
    """A label's based integer, such as 16#8000#, whose digits give a sample's bit pattern."""


@dataclass(frozen=True)
class Grid:
    """Simple cylindrical grid with pixel-centred latitudes (north first) and east longitudes, on a sphere."""
    lat_deg: np.ndarray
    lon_deg: np.ndarray
    pixels_per_degree: int
    radius_m: float

    @classmethod
    def globe(cls, pixels_per_degree: int, radius_m: float) -> Grid:
        """The global grid at a resolution, its rows from the north pole and its columns east from 0."""
        lat = 90.0 - (np.arange(180 * pixels_per_degree) + 0.5) / pixels_per_degree
        lon = (np.arange(360 * pixels_per_degree) + 0.5) / pixels_per_degree
        return cls(lat, lon, pixels_per_degree, float(radius_m))

    @property
    def cell_area_m2(self):
        """Exact area of each cell on the reference sphere (lat x lon)."""
        half = 0.5 / self.pixels_per_degree
        top = np.radians(self.lat_deg + half)
        bottom = np.radians(self.lat_deg - half)
        band = self.radius_m**2 * np.radians(1.0 / self.pixels_per_degree) * (np.sin(top) - np.sin(bottom))
        return np.repeat(band[:, None], self.lon_deg.size, axis=1)


@dataclass(frozen=True)
class Field:
    """A gravity field's fully normalized coefficients C[n, m] and S[n, m], its GM and its reference radius."""
    c: np.ndarray
    s: np.ndarray
    gm_m3_s2: float
    reference_radius_m: float

    @property
    def degree(self) -> int:
        return self.c.shape[0] - 1


@dataclass(frozen=True)
class Tide:
    """The permanent tide a host raises on a body that keeps one face to it: the host's GM; the orbit's
    semi-major axis, eccentricity and inclination to the body's equator; the Love number k2 of the body; and the
    east longitude of the mean sub-host point, on the equator."""
    gm_m3_s2: float
    semi_major_axis_m: float
    eccentricity: float = 0.0
    inclination_deg: float = 0.0
    love_k2: float = 0.0
    sub_lon_deg: float = 0.0


def tide_coefficients(eccentricity: float, inclination_deg: float, samples: int = TIDE_SAMPLES) -> tuple[float, float]:
    """The time means A0 = <(a/r)^3 P2(sin b)> and A22 = <3/4 (a/r)^3 cos^2 b cos 2l> of a host's distance r and
    direction (latitude b, longitude l) in the frame of a body turning at the orbit's mean motion, over the mean
    anomaly and over the perigee's angle from the node, which the orbit's precession turns through. The permanent
    tide is then (1 + k2) GM R^2/a^3 [A0 P2(sin lat) + A22 cos^2 lat cos 2(lon - lon0)]; a circular orbit in the
    equator gives A0 = -1/2 and A22 = 3/4, the tide of a host fixed over the sub-point."""
    e, inclination = float(eccentricity), math.radians(inclination_deg)
    if not 0.0 <= e < 1.0:
        raise ValueError(f'an orbit of eccentricity {e}')
    mean, perigee = np.meshgrid(2 * math.pi * np.arange(samples) / samples,
                                2 * math.pi * np.arange(samples // 4) / (samples // 4), indexing='ij')
    big_e = mean.copy()
    for _ in range(50):                                    # Kepler's equation, by Newton's method
        step = (big_e - e * np.sin(big_e) - mean) / (1.0 - e * np.cos(big_e))
        big_e -= step
        if np.abs(step).max() < 1e-15:
            break
    true = 2 * np.arctan2(math.sqrt(1 + e) * np.sin(big_e / 2), math.sqrt(1 - e) * np.cos(big_e / 2))
    inverse_cube = (1.0 - e * np.cos(big_e)) ** -3            # (a/r)^3
    u = perigee + true                                     # the argument of latitude, from the node
    x, y, z = np.cos(u), np.sin(u) * math.cos(inclination), np.sin(u) * math.sin(inclination)
    lon = np.arctan2(y, x) - (perigee + mean)              # against the body's turning, which keeps the mean anomaly
    a0 = float(np.mean(inverse_cube * (1.5 * z**2 - 0.5)))
    a22 = float(np.mean(0.75 * inverse_cube * (1.0 - z**2) * np.cos(2 * lon)))
    return a0, a22


def read_pds3_label(path) -> dict:
    """A PDS3 label as nested dicts: each OBJECT or GROUP a dict under its name (a list of dicts where the name
    repeats), each value a number, a string, a tuple, or a (value, unit) pair where the label states a unit."""
    text = re.sub(r'/\*.*?\*/', ' ', Path(path).read_text(encoding='ascii', errors='replace'), flags=re.S)
    tokens = _TOKEN.findall(text)
    root, stack, i = {}, [], 0
    node = root

    def value(i):
        token = tokens[i]
        if token in ('(', '{'):
            close, items, i = ')' if token == '(' else '}', [], i + 1
            while tokens[i] != close:
                if tokens[i] == ',':
                    i += 1
                    continue
                item, i = value(i)
                items.append(item)
            return tuple(items), i + 1
        atom, i = _atom(token), i + 1
        if i < len(tokens) and tokens[i].startswith('<'):
            return (atom, tokens[i][1:-1].strip()), i + 1
        return atom, i

    while i < len(tokens) and tokens[i] != 'END':
        key = tokens[i]
        has_value = i + 1 < len(tokens) and tokens[i + 1] == '='
        if key in ('END_OBJECT', 'END_GROUP'):
            if not stack:
                raise ValueError(f'{path}: {key} closes nothing')
            node = stack.pop()
            i += 3 if has_value else 1
            continue
        if not has_value:
            raise ValueError(f'{path}: expected "=" after {key!r}')
        if key in ('OBJECT', 'GROUP'):
            child = {}
            _put(node, tokens[i + 2], child)
            stack.append(node)
            node, i = child, i + 3
            continue
        item, i = value(i + 2)
        _put(node, key, item)
    if stack:
        raise ValueError(f'{path}: {len(stack)} OBJECT or GROUP left open')
    return root


def _atom(token: str):
    if token[0] in '"\'':
        return ' '.join(token[1:-1].split())
    based = _BASED.fullmatch(token)
    if based:
        sign, radix, digits = based.groups()
        return Bits(int(sign + digits, int(radix)))
    for kind in (int, float):
        try:
            return kind(token)
        except ValueError:
            pass
    return token


def _put(node: dict, key: str, item) -> None:
    if key not in node:
        node[key] = item
    elif isinstance(node[key], list):
        node[key].append(item)
    else:
        node[key] = [node[key], item]


def _owner(tree: dict, key: str) -> dict | None:
    """The first dict of a label, depth first, that holds `key`."""
    if key in tree:
        return tree
    for item in tree.values():
        for child in (item if isinstance(item, list) else [item]):
            if isinstance(child, dict):
                owner = _owner(child, key)
                if owner is not None:
                    return owner
    return None


def _object(label: dict, name: str, where) -> dict:
    owner = _owner(label, name)
    if owner is None or not isinstance(owner[name], dict):
        raise ValueError(f'{where}: the label describes no {name}')
    return owner[name]


def pointed_file(label: dict, name: str) -> str | None:
    """The file a label's ^name points at, or None where the label points at no object of that name."""
    owner = _owner(label, '^' + name)
    pointer = owner['^' + name] if owner is not None else None
    file = pointer[0] if isinstance(pointer, tuple) else pointer
    return file if isinstance(file, str) else None


def _pointed(label: dict, name: str, path, where) -> None:
    """Checks that the label's ^name points at the file given."""
    file = pointed_file(label, name)
    if file is None:
        raise ValueError(f'{where}: the label names no file for {name}')
    if file.lower() != Path(path).name.lower():
        raise ValueError(f'{where} describes {file}, where the file given is {Path(path).name}')


def _number(item, unit: str | None = None, scale: dict | None = None) -> float:
    """A label's number, converted by `scale` from the unit the label states, or from `unit` where it states none."""
    if isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], str):
        number, stated = item[0], item[1].lower()
    else:
        number, stated = item, unit
    if not isinstance(number, (int, float)) or isinstance(number, bool):
        raise ValueError(f'a number, where the label holds {item!r}')
    if scale is None:
        return float(number)
    if stated not in scale:
        raise ValueError(f'a unit {stated!r} outside {sorted(scale)}')
    return float(number) * scale[stated]


def _sample(item, dtype: np.dtype, where):
    """A label's MISSING_CONSTANT as a sample's value: a based integer gives the sample's bits."""
    if isinstance(item, Bits):
        return np.array(int(item), dtype=f'u{dtype.itemsize}').view(f'{dtype.kind}{dtype.itemsize}')[()]
    if isinstance(item, (int, float)) and not isinstance(item, bool):
        return item
    raise ValueError(f'{where}: a MISSING_CONSTANT of {item!r}')


def read_pds_image(label_path, image_path):
    """A global simple-cylindrical PDS3 image, read through its label: each sample times SCALING_FACTOR, in the
    image's UNIT, is a height above the reference sphere of radius OFFSET, the convention of LOLA's LDEM labels.
    Returns the heights (m), their grid on that sphere, and the label's reference radius, target, frame and
    product.

    The label must describe a pixel-registered global map of east longitudes from 0 at a whole number of pixels
    per degree, in a file that holds the image alone, every sample present, with an OFFSET above zero; heights
    from another datum, such as an equipotential, are refused."""
    label = read_pds3_label(label_path)
    image, projection = _object(label, 'IMAGE', label_path), _object(label, 'IMAGE_MAP_PROJECTION', label_path)
    _pointed(label, 'IMAGE', image_path, label_path)
    kind = projection.get('MAP_PROJECTION_TYPE')
    if kind != 'SIMPLE CYLINDRICAL':
        raise ValueError(f'{label_path}: a {kind} map, where the reader takes SIMPLE CYLINDRICAL')
    if projection.get('POSITIVE_LONGITUDE_DIRECTION', 'EAST') != 'EAST':
        raise ValueError(f'{label_path}: west longitudes, where the reader takes east')
    resolution = _number(projection['MAP_RESOLUTION'])
    if resolution < 1 or resolution != int(resolution):
        raise ValueError(f'{label_path}: {resolution} pixels per degree, where the reader takes a whole number of them')
    ppd = int(resolution)
    north, south, west, east = (_number(projection[k], 'deg', DEGREES) for k in
                                ('MAXIMUM_LATITUDE', 'MINIMUM_LATITUDE', 'WESTERNMOST_LONGITUDE', 'EASTERNMOST_LONGITUDE'))
    lines, samples = int(image['LINES']), int(image['LINE_SAMPLES'])
    if (north, south, east - west) != (90.0, -90.0, 360.0) or (lines, samples) != (180 * ppd, 360 * ppd):
        raise ValueError(f'{label_path}: a {lines} x {samples} map from {north} to {south} N and {west} to {east} E at '
                         f'{ppd} pixels per degree, where the reader takes a pixel-registered global map')
    if west != 0.0:
        raise ValueError(f'{label_path}: columns from {west} E, where the reader takes columns east from 0')
    centre = _number(projection.get('CENTER_LONGITUDE', 180.0), 'deg', DEGREES)
    offsets = tuple(_number(projection[k], 'pix', PIXELS) for k in ('LINE_PROJECTION_OFFSET', 'SAMPLE_PROJECTION_OFFSET'))
    registered = (north * ppd - 0.5, (centre - west) * ppd - 0.5)
    if offsets != registered:
        raise ValueError(f'{label_path}: projection offsets {offsets}, where pixel registration puts {registered}')
    unit = str(image.get('UNIT', 'METER')).lower()
    if unit not in METRES:
        raise ValueError(f'{label_path}: samples in {image.get("UNIT")!r}, where the reader takes metres or kilometres')
    offset = _number(image.get('OFFSET', 0.0), unit, METRES)
    if not offset > 0:
        raise ValueError(f'{label_path}: an OFFSET of {image.get("OFFSET", 0.0)!r}, where the reader takes radii less '
                         'a reference sphere of radius OFFSET; heights from another datum take a reader of their own')
    sample_type, bits = image['SAMPLE_TYPE'], int(image['SAMPLE_BITS'])
    if sample_type not in SAMPLE_TYPES or bits % 8:
        raise ValueError(f'{label_path}: samples of {bits}-bit {sample_type}, outside {sorted(SAMPLE_TYPES)}')
    dtype = np.dtype(f'{SAMPLE_TYPES[sample_type]}{bits // 8}')
    size = Path(image_path).stat().st_size
    if size != lines * samples * dtype.itemsize:
        raise ValueError(f'{image_path}: {size} bytes, where the label describes {lines * samples * dtype.itemsize}')
    raw = np.fromfile(image_path, dtype=dtype).reshape(lines, samples)
    if 'MISSING_CONSTANT' in image:
        missing = np.sum(raw == _sample(image['MISSING_CONSTANT'], dtype, label_path))
        if missing:
            raise ValueError(f'{image_path}: {int(missing)} samples missing')
    height = raw.astype(float) * (_number(image.get('SCALING_FACTOR', 1.0)) * METRES[unit])
    return height, Grid.globe(ppd, offset), dict(reference_radius_m=offset, target=label.get('TARGET_NAME'),
                                                 frame=projection.get('COORDINATE_SYSTEM_NAME'),
                                                 product=label.get('PRODUCT_ID'))


def read_shadr(label_path, table_path, max_degree: int) -> Field:
    """A PDS SHADR table's coefficients to max_degree, read through its label: the header row's reference
    radius (km) and GM (km^3/s^2), fully normalized coefficients, and each row's degree, order, C and S, every
    degree and order from 2 to max_degree present."""
    label = read_pds3_label(label_path)
    _pointed(label, 'SHADR_HEADER_TABLE', table_path, label_path)
    columns = _object(label, 'SHADR_HEADER_TABLE', label_path).get('COLUMN', [])
    units = {c.get('NAME'): c.get('UNIT') for c in (columns if isinstance(columns, list) else [columns])}
    unit = units.get('REFERENCE RADIUS')
    if unit != 'KILOMETER':
        raise ValueError(f'{label_path}: ' + ('the label lists no REFERENCE RADIUS column, which the reader takes from '
                                              'the label itself' if unit is None else
                                              f'a reference radius in {unit!r}, where SHADR takes km'))
    rows = Path(table_path).read_text().splitlines()
    head = [v.strip() for v in rows[0].split(',')]
    ref_radius, gm, degree = float(head[0]) * 1e3, float(head[1]) * 1e9, int(head[3])
    if int(head[5]) != 1:
        raise ValueError('Expected fully normalized coefficients')
    if max_degree > degree:
        raise ValueError(f'{table_path}: a field to degree {degree}, below the {max_degree} asked for')
    c = np.zeros((max_degree + 1, max_degree + 1))
    s = np.zeros_like(c)
    found = np.zeros(c.shape, dtype=bool)
    for row in rows[1:]:
        v = row.split(',')
        if len(v) < 4:
            if row.strip():
                raise ValueError(f'{table_path}: a row of {len(v)} fields, {row.strip()[:40]!r}')
            continue
        n, m = int(v[0]), int(v[1])
        if n <= max_degree:
            c[n, m], s[n, m], found[n, m] = float(v[2]), float(v[3]), True
    wanted = np.tril(np.ones(c.shape, dtype=bool))
    wanted[:2] = False
    if (wanted & ~found).any():
        raise ValueError(f'{table_path}: {int((wanted & ~found).sum())} coefficients of degrees 2 to {max_degree} missing')
    return Field(c, s, gm, ref_radius)


def legendre_column(m: int, max_degree: int, t, u):
    """Fully normalized (4-pi, no Condon-Shortley phase) P_nm(t) for n = m..max_degree.

    t = sin(latitude), u = cos(latitude). Standard stable column recursion.
    """
    p = np.zeros((max_degree - m + 1, t.size))
    pmm = np.ones_like(t)
    for k in range(1, m + 1):
        pmm = pmm * u * math.sqrt((2 * k + 1) / (2 * k)) if k > 1 else pmm * u * math.sqrt(3.0)
    p[0] = pmm
    if max_degree > m:
        p[1] = math.sqrt(2 * m + 3) * t * pmm
    for n in range(m + 2, max_degree + 1):
        a = math.sqrt((2 * n - 1) * (2 * n + 1) / ((n - m) * (n + m)))
        b = math.sqrt((2 * n + 1) * (n + m - 1) * (n - m - 1) / ((n - m) * (n + m) * (2 * n - 3)))
        p[n - m] = a * t * p[n - m - 1] - b * p[n - m - 2]
    return p


def geoid(grid: Grid, field: Field, max_degree: int, rotation_rate_rad_s: float, tide: Tide | None = None):
    """Geoid height (m) above the grid's reference sphere.

    Degree 0 and 1 are excluded (mean radius and centre of mass), so the gravity part has zero mean; the
    centrifugal and tidal terms are written as zero-mean degree-2 functions.
    """
    if max_degree > field.degree:
        raise ValueError(f'a geoid to degree {max_degree} from a field read to degree {field.degree}')
    c, s, gm, ref, radius = field.c, field.s, field.gm_m3_s2, field.reference_radius_m, grid.radius_m
    lat, lon = np.radians(grid.lat_deg), np.radians(grid.lon_deg)
    t, u = np.sin(lat), np.cos(lat)
    scale = (ref / radius) ** np.arange(max_degree + 1)
    a = np.zeros((lat.size, max_degree + 1))
    b = np.zeros_like(a)
    for m in range(max_degree + 1):
        p = legendre_column(m, max_degree, t, u)
        n = np.arange(m, max_degree + 1)
        keep = n >= 2
        a[:, m] = (scale[n][keep] * c[n[keep], m]) @ p[keep]
        b[:, m] = (scale[n][keep] * s[n[keep], m]) @ p[keep]
    mm = np.arange(max_degree + 1)
    height = radius * (a @ np.cos(np.outer(mm, lon)) + b @ np.sin(np.outer(mm, lon)))
    gamma = gm / radius**2
    potential = np.repeat((0.5 * rotation_rate_rad_s**2 * radius**2 * (u**2 - 2.0 / 3.0))[:, None], lon.size, 1)
    if tide is not None:
        a0, a22 = tide_coefficients(tide.eccentricity, tide.inclination_deg)
        lon0 = math.radians(tide.sub_lon_deg)
        potential = potential + ((1 + tide.love_k2) * tide.gm_m3_s2 * radius**2 / tide.semi_major_axis_m**3
                                 * (a0 * (1.5 * t**2 - 0.5)[:, None] + a22 * np.outer(u**2, np.cos(2 * (lon - lon0)))))
    return height + potential / gamma


def height_above_geoid(height, grid: Grid, field: Field, max_degree: int, rotation_rate_rad_s: float,
                       tide: Tide | None = None):
    """Topography relative to the geoid (m), and the geoid itself, on a grid of heights above the grid's
    reference sphere. The geoid is synthesised on the heights' own grid, where Terluna's interpolation from 4
    pixels per degree to LOLA's 16 erred by 0.17 m area-weighted rms and 2.4 m at most at degree 200."""
    n_full = geoid(grid, field, max_degree, rotation_rate_rad_s, tide)
    return height - n_full, n_full
