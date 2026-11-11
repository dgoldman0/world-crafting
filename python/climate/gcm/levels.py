"""PlaSim's vertical levels for a world: the released model's own, a set generated from the world's scale height and
the heights it states for the half levels near its ground, the namelist entries of a run on a generated set, and the
conservative remap that carries a restart from one set onto another.

    from climate.gcm import levels
    moon = levels.TERLUNA_OPEN_MOON_LEVELS                      # the values Terluna's set states for the Open Moon
    half = levels.generate(moon['scale_height_m'], moon['interfaces_m'], moon['upper'])    # its fifteen half levels
    levels.summary(half, moon['scale_height_m'])                # full levels, the lowest level's height, the thinning
    levels.namelist_entries(half)                               # NEQSIG -1, SIGH and TFRC, for plasim_namelist
    levels.carry_restart(src, dst, levels.plasim_half(), half)  # a ten-level restart written onto the set

The levels. PlaSim counts its levels in sigma, the pressure over the surface's, from 0 at the top to 1 at the ground,
and puts each full level midway in sigma between the half levels that bound its layer (plasim.f90, initpm), so that
the half levels fix the set. The released model computes ten half levels from a formula (plasim_half; NEQSIG 0,
ExoPlaSim's vtype 0), fractions of the surface pressure chosen for Earth's air. A level stands near -H ln sigma, H the
scale height, so the same fractions stand higher where H is larger: the lowest full level, sigma 0.9833, stands near
0.14 km in Earth's air (H 8.4 km) and near 0.9 km in the Open Moon's (H 51-52 km), under a lowest layer 0.29 km and
1.7-1.8 km deep (defect log B31).

The rule (generate). A world's set keeps the released model's `upper` highest half levels, in the doubles the compiled
model computes, so that the layers above the join are the released model's own. Below them it takes one half level at
each height the world states, the highest first, at sigma = exp(-z/H) to four places, H the scale height the heights
are counted at, and it ends at the ground's 1. A stated height that falls on a released half level at four places
takes that half level's own double, so that a layer two sets share holds the same numbers in both. The count of levels
is `upper` plus the stated heights plus one. The rule refuses heights out of order, a height at or above the join, a
height within the rounding of its neighbour or of the ground, and a set that keeps fewer than the released model's
two highest half levels, whose layers take PlaSim's Rayleigh friction. Nothing of a world is built in: the scale
height, the heights and the count of released half levels kept are the world's, stated by the study that runs it.

What the heights are. They are the layer boundaries a world wants near its ground: the depth of its lowest layer,
which sets the height at which PlaSim takes its surface fluxes, the lowest full level standing midway in sigma, and
boundaries through its boundary layer and its low cloud. generate converts them at one scale height, and a run's own
temperatures set the heights its levels stand at. summary gives a set's full levels, the heights of its lowest level
and lowest layer at a scale height, and the least share of mass that a layer holds of the layer above it, the measure
by which Terluna kept its new layers thinning smoothly, each at least half of the one above.

Terluna's sets for the Open Moon (TERLUNA_OPEN_MOON_LEVELS). Terluna placed fourteen and then fifteen levels by hand
for its design air, counting heights at a scale height of 51 km (climate/gcm/levels.py at 39c5ee04, 'l14' and 'l15').
Its CM1 sea box holds a boundary layer 6 km deep and night cloud from 6.2 km to tops at 7-8 km, all inside the
released model's one layer from 6.4 to 13.7 km, and its lowest layer, the ground to 1.73 km, holds 1.4-2.3 kJ/kg less
moist static energy than CM1's air at 50 m. The fourteen keep the released model's six upper half levels and its
lowest one, and put six half levels at 15.5, 11.5, 9.0, 7.0, 5.0 and 3.1 km; the fifteen add one at 0.60 km, which
puts the lowest full level at 0.30 km under a lowest layer that holds 0.54 of the mass of the layer above. From
those values generate returns Terluna's half levels at the four places Terluna states them. In two of the fifteen,
0.3736 and 0.9666, the last bit differs from the doubles Terluna's module holds, since that module computes the
released formula with numpy's powers and the compiled model multiplies them out (plasim_half). The record is a value
a study of the Open Moon states, and the fourteen are the same values without the last height.

Earth. In Earth's air at 288 K, H 8.43 km, the released ten put the lowest full level at 142 m under a lowest layer
286 m deep, inside the 0.3 km that the Open Moon's fifteen reach, so a world whose scale height is near Earth's keeps
the released ten (PLAN.md). generate refuses the Open Moon's heights at Earth's scale height: its lowest layer,
0.60 km, is deeper than the released model's own there, and the heights above it stand above the join.

The run's entries (namelist_entries). A run on a generated set states NEQSIG -1 and its half levels in SIGH, which
PlaSim reads in place of its formula. PlaSim presets its Rayleigh friction, 20 and 100 days on its top two levels,
where it is compiled for ten levels alone (plasim.f90, readnl), so the entries state the same friction in TFRC, in
seconds, for a set that keeps those two layers. PlaSim's reference temperature for its semi-implicit scheme is 250 K
at every level on every set.

The restart (remap_matrix, remap, carry_restart). Sigma counts the air's mass, a layer holding ps dsigma / g, so a
restart goes onto another set through a conservative remap in sigma: each old layer's profile is reconstructed
linearly about its full level with the centred slope between its neighbours' values (one-sided at the top and at the
ground), and each new layer takes the reconstruction's mean over its sigma range, the parts in each old layer weighted
by their mass. A layer the two sets share keeps its values bit for bit, and a restart carried onto its own set comes
back byte for byte. The surface pressure, and with it every column's mass, stays as it is, and the remap keeps each
column's integrals over sigma of what it is applied to: the vapour, the temperature (the column's enthalpy at a
constant heat capacity), the vorticity and the divergence. Kinetic and potential energy are outside what it keeps.
It is one linear operator in the vertical, the same at every point, so it acts on the spectral coefficients of
vorticity, divergence, temperature and humidity (both time levels) directly, and on the gridpoint fields held by
level. The slopes are unlimited, so a new layer's value can pass its neighbours' where a profile bends sharply. The
cloud cover is clipped to 0-1 and the cloud water and saturation humidity to 0 and above, which changes those three
fields' column sums; the radiation of the run's first step reads the cloud cover and cloud water, and mkclouds then
computes them anew (plasim.f90, gridpointd; rainmod.f90, mkclouds). The field lists follow the pinned source's
restart, and a record sized like a field by level that the lists leave out stops the carry.

Evidence. A runnable calculation with its tests (climate/tests/test_levels.py; lab/tests/test_builds.py for the
compiled model). On this machine's gfortran the released ten of plasim_half, written through NEQSIG -1, SIGH and TFRC,
run the released model's output and restart byte for byte. Terluna ran its two sets on the Open Moon and records the
outcomes (climate/gcm/README.md at 39c5ee04, "Fourteen levels near the ground" and "Fifteen levels: a thin bottom
layer"): a fifteen-level year cost about 1.6 times a ten-level one; its two-year tests record how the rain by time of
day and the air near the ground changed on each set; and the longwave correction fitted on ten levels left
6.4-8.8 W/m2 by layer when carried onto the new levels, so each set takes its own fit. The lab has run no climate on
a generated set. The Earth control's test of a set other than the released ten, and a study's own choice of heights
for a world without Terluna's boxes, are ahead.

Brought from Terluna's climate/gcm/levels.py at 39c5ee04 (python/provenance.json). full_levels, shared_layers,
remap_matrix, remap, read_records, write_records and carry_restart are Terluna's; carry_restart reads the horizontal
sizes from the restart's own records, where Terluna's held T21's, and writes to a new path alone. generate, check,
summary and the record of Terluna's values are the lab's, in place of Terluna's three named sets; plasim_half
multiplies its powers out as the compiled model does; namelist_entries takes the half levels and returns values for
the lab's writer; and Terluna's command line, with its heights at 51 km, stays there.
"""
from __future__ import annotations

import hashlib
import math
import struct
from pathlib import Path

import numpy as np

RELEASED = 10                   # the released model's count of levels, whose half levels a generated set keeps from
SIGMA_PLACES = 4                # a stated height's sigma is rounded to this many places, as Terluna's sets state theirs
# PlaSim's Rayleigh friction on its top two levels, which it presets where it is compiled for ten levels (days).
TOP_FRICTION_DAYS = (20.0, 100.0)
DAY_S = 86400.0

# Terluna's fifteen levels for the Open Moon ('l15', climate/gcm/levels.py at 39c5ee04), as the values a study of that
# world states: the 51 km that Terluna counts its heights at, the released model's six upper half levels kept, and
# eight half levels below them, six from 15.5 km down to 3.1 km, the released model's lowest at 1.73 km, and one at
# 0.60 km, which splits the lowest layer. Without the last height they give Terluna's fourteen ('l14').
TERLUNA_OPEN_MOON_LEVELS = dict(scale_height_m=51000.0, upper=6,
                                interfaces_m=(15500.0, 11500.0, 9000.0, 7000.0, 5000.0, 3100.0, 1730.0, 600.0))


def plasim_half(levels: int = RELEASED) -> np.ndarray:
    """The released model's own half levels (initpm's last branch, NEQSIG 0), the top layer's bottom first, ending at
    the ground's 1, in the doubles the compiled model computes. gfortran multiplies the formula's integer powers out,
    s**3 as (s s) s and s**4 as (s s)(s s), and so does this function; numpy's powers end one or two units of the last
    place away at three of the ten, 0.3736, 0.8816 and 0.9666. Checked against the compiled model for ten levels at
    double precision (lab/tests/test_builds.py)."""
    if isinstance(levels, bool) or not isinstance(levels, (int, np.integer)) or levels < 1:
        raise ValueError(f'The count of levels is a whole number from 1 up, where it is {levels!r}')
    s = np.arange(1, levels + 1) / levels
    return 0.75 * s + 1.75 * (s * s * s) - 1.5 * ((s * s) * (s * s))


def check(half) -> np.ndarray:
    """Half levels as PlaSim takes them: two or more finite numbers that rise from above 0 to the ground's 1."""
    half = np.array(half, float)
    if half.ndim != 1 or half.size < 2 or not np.all(np.isfinite(half)):
        raise ValueError('Half levels are two or more finite numbers, the top first')
    if half[-1] != 1.0 or np.any(np.diff(np.r_[0.0, half]) <= 0.0):
        raise ValueError("Half levels rise from above 0 to the ground's 1, where these are "
                         f'{[float(x) for x in half]}')
    return half


def full_levels(half) -> np.ndarray:
    """The full levels PlaSim puts midway in sigma between the half levels (0 above the first)."""
    half = np.asarray(half, float)
    return 0.5 * (np.r_[0.0, half[:-1]] + half)


def heights_m(sigma, scale_height_m: float) -> np.ndarray:
    """Heights of sigma levels at a constant scale height, m."""
    return -float(scale_height_m) * np.log(np.asarray(sigma, float))


def generate(scale_height_m: float, interfaces_m, upper: int) -> np.ndarray:
    """A world's half levels by the module's rule: the released model's `upper` highest half levels as the compiled
    model computes them, then one at each height of `interfaces_m` above the ground, the highest first, at
    sigma = exp(-z / scale_height_m) to four places, then the ground's 1. A height that falls on a released half
    level at four places takes that half level's own double."""
    if isinstance(scale_height_m, bool) or not isinstance(scale_height_m, (int, float)) \
            or not math.isfinite(scale_height_m) or not scale_height_m > 0:
        raise ValueError(f'The scale height is a positive number of metres, where it is {scale_height_m!r}')
    if isinstance(upper, bool) or not isinstance(upper, int) or not len(TOP_FRICTION_DAYS) <= upper < RELEASED:
        raise ValueError(f"A generated set keeps from {len(TOP_FRICTION_DAYS)} to {RELEASED - 1} of the released "
                         f"model's highest half levels, where `upper` is {upper!r}")
    try:
        given = list(interfaces_m)
        heights = [float(z) for z in given]
    except (TypeError, ValueError):
        raise ValueError(f'The stated heights are numbers of metres, where they are {interfaces_m!r}') from None
    if not heights or any(isinstance(z, (bool, str)) for z in given) \
            or not all(math.isfinite(z) and z > 0 for z in heights):
        raise ValueError(f'The stated heights are one or more positive numbers of metres, where they are {given!r}')
    if any(low >= high for high, low in zip(heights, heights[1:])):
        raise ValueError(f'The stated heights run from the highest down, where they are {heights}')
    released = plasim_half(RELEASED)
    own = {round(float(x), SIGMA_PLACES): float(x) for x in released}
    stated = [round(math.exp(-z / scale_height_m), SIGMA_PLACES) for z in heights]
    join = float(released[upper - 1])
    if not stated[0] > round(join, SIGMA_PLACES):
        raise ValueError(f'The highest stated height, {heights[0]:g} m, stands at sigma {stated[0]:.4f}, at or above '
                         f"the released model's half level {upper}, {join:.4f}, which the set keeps")
    if stated[-1] >= 1.0 or any(b <= a for a, b in zip(stated, stated[1:])):
        raise ValueError(f'The stated heights stand at sigma {stated} to {SIGMA_PLACES} places, where each lies below '
                         "the one before it and above the ground's 1")
    return check(np.r_[released[:upper], [own.get(s, s) for s in stated], 1.0])


def summary(half, scale_height_m: float) -> dict:
    """What a set gives at a scale height: its count, its half and full levels, the heights of its lowest full level
    and of its lowest layer's top, m, and the least share of mass that a layer holds of the layer above it."""
    half = check(half)
    full, thick = full_levels(half), np.diff(np.r_[0.0, half])
    return dict(levels=int(half.size), half_levels=[float(x) for x in half], full_levels=[float(x) for x in full],
                lowest_level_m=float(heights_m(full[-1], scale_height_m)),
                lowest_layer_m=float(heights_m(half[-2], scale_height_m)),
                least_share_of_layer_above=float(np.min(thick[1:] / thick[:-1])))


def namelist_entries(half) -> dict:
    """The plasim_namelist entries of a run on a generated set: NEQSIG -1, with which PlaSim reads its half levels
    from SIGH, and in TFRC, in seconds, the friction PlaSim presets on its top two levels where it is compiled for
    ten. The friction belongs to the released model's two highest layers, so a set that changes them is refused."""
    half = check(half)
    top = len(TOP_FRICTION_DAYS)
    if half.size <= top or not np.array_equal(half[:top], plasim_half(RELEASED)[:top]):
        raise ValueError(f"PlaSim's friction belongs to the released model's {top} highest layers, where the set's "
                         f'begin with half levels {[float(x) for x in half[:top]]}')
    friction = [days * DAY_S for days in TOP_FRICTION_DAYS] + [0.0] * (half.size - top)
    return dict(NEQSIG=-1, SIGH=tuple(float(x) for x in half), TFRC=tuple(friction))


def shared_layers(half_from, half_to) -> dict:
    """The layers two grids share, new index to old: the same two half levels (0 above the first)."""
    a, b = np.r_[0.0, np.asarray(half_from, float)], np.r_[0.0, np.asarray(half_to, float)]
    out = {}
    for k in range(b.size - 1):
        for j in range(a.size - 1):
            if a[j] == b[k] and a[j + 1] == b[k + 1]:
                out[k] = j
    return out


def remap_matrix(half_from, half_to) -> np.ndarray:
    """The conservative remap from one grid's layer values to another's (new by old, the top first): a linear
    reconstruction in each old layer about its full level with the centred slope of its neighbours, averaged over each
    new layer by mass (sigma). Layers the grids share are copied; every column's integral over sigma is kept."""
    a = np.r_[0.0, check(half_from)]
    b = np.r_[0.0, check(half_to)]
    n, m = a.size - 1, b.size - 1
    centre = 0.5 * (a[:-1] + a[1:])
    slope = np.zeros((n, n))                      # slope[j] @ x: the old layer j's slope in sigma
    for j in range(n):
        lo, hi = max(j - 1, 0), min(j + 1, n - 1)
        slope[j, hi] += 1.0 / (centre[hi] - centre[lo])
        slope[j, lo] -= 1.0 / (centre[hi] - centre[lo])
    w = np.zeros((m, n))
    shared = shared_layers(half_from, half_to)
    for k in range(m):
        if k in shared:
            w[k, shared[k]] = 1.0
            continue
        for j in range(n):
            lo, hi = max(a[j], b[k]), min(a[j + 1], b[k + 1])
            if hi <= lo:
                continue
            part = (hi - lo) / (b[k + 1] - b[k])
            w[k, j] += part
            w[k] += part * slope[j] * (0.5 * (lo + hi) - centre[j])
    return w


def remap(values, half_from, half_to, axis: int = 0) -> np.ndarray:
    """Layer values (any shape, the levels along axis) carried from one grid to another by remap_matrix; layers the
    grids share are copied exactly."""
    w = remap_matrix(half_from, half_to)
    x = np.moveaxis(np.asarray(values, float), axis, 0)
    if x.shape[0] != w.shape[1]:
        raise ValueError(f'The values hold {x.shape[0]} levels, where the grid they are carried from holds '
                         f'{w.shape[1]}')
    out = np.tensordot(w, x, axes=(1, 0))
    for k, j in shared_layers(half_from, half_to).items():
        out[k] = x[j]
    return np.moveaxis(out, 0, axis)


# The restart's fields held by level (plasim.f90, the restart's write and read): spectral at each level (both time
# levels), gridpoint at each level, and gridpoint at each level and the ground (NLEP), whose ground value is kept.
SPECTRAL_BY_LEVEL = ('sz', 'sd', 'st', 'sq', 'sr', 'szm', 'sdm', 'stm', 'sqm')
GRID_BY_LEVEL = ('dcc', 'dql', 'dqsat', 'aast', 'aasqout', 'aasd', 'aasz', 'aadqo3')
GRID_BY_LEVEL_AND_GROUND = ('aadq', 'aammr', 'aanrho', 'aadt', 'aadql', 'aadcc')
CLIPPED = {'dcc': (0.0, 1.0), 'dql': (0.0, None), 'dqsat': (0.0, None)}
# Records held by something other than the air's levels: the 14 months of the surface's climatologies and the soil's
# layers.
NOT_BY_LEVEL = ('dtcl', 'dwcl', 'dalbcl', 'dalbcl1', 'dalbcl2', 'xclicec', 'xcliced', 'xclsst', 'yclsst', 'dsoilt')
# The restart's own counts, from which the carrier knows a field's horizontal size: spectral coefficients, and the
# grid's latitudes and longitudes.
SIZES = ('nrsp', 'nlat', 'nlon')


def read_records(path) -> list:
    """A PlaSim restart's records (Fortran sequential, unformatted, little-endian 4-byte markers): pairs of a
    16-character name and its data, as (name, bytes)."""
    data = Path(path).read_bytes()
    raw, i = [], 0
    while i < len(data):
        if i + 4 > len(data):
            raise ValueError(f'{path}: a record at byte {i} breaks off in its opening marker')
        size = struct.unpack('<i', data[i:i + 4])[0]
        if size < 0 or i + 8 + size > len(data):
            raise ValueError(f'{path}: a record at byte {i} runs past the end of the file')
        raw.append(data[i + 4:i + 4 + size])
        if struct.unpack('<i', data[i + 4 + size:i + 8 + size])[0] != size:
            raise ValueError(f'{path}: a record at byte {i} closes with another length than it opens with')
        i += size + 8
    if len(raw) % 2:
        raise ValueError(f'{path}: a name without its data')
    return [(raw[k].decode('ascii'), raw[k + 1]) for k in range(0, len(raw), 2)]


def write_records(path, records):
    out = bytearray()
    for name, data in records:
        for rec in (name.ljust(16)[:16].encode('ascii'), data):
            out += struct.pack('<i', len(rec)) + rec + struct.pack('<i', len(rec))
    tmp = Path(str(path) + '.part')
    tmp.write_bytes(bytes(out))
    tmp.replace(path)


def carry_restart(src, dst, half_from, half_to) -> dict:
    """Write src's restart onto another grid at dst, a new path (remap_matrix), every other record as it was; returns
    what moved, with each field's column integrals before and after and the two files' sha256."""
    half_from, half_to = check(half_from), check(half_to)
    n, m = half_from.size, half_to.size
    if Path(dst).exists():
        raise ValueError(f'{dst}: a carried restart is written to a new path')
    records = read_records(src)
    names = [name.strip() for name, _ in records]
    counts = {}
    for key in ('nlev',) + SIZES:
        if names.count(key) != 1 or len(records[names.index(key)][1]) != 4:
            raise ValueError(f'{src}: a PlaSim restart states {key} once, as one integer')
        counts[key] = struct.unpack('<i', records[names.index(key)][1])[0]
    if counts['nlev'] != n:
        raise ValueError(f"{src} holds {counts['nlev']} levels, where the grid it is carried from holds {n}")
    widths = (counts['nrsp'], counts['nlat'] * counts['nlon'])
    dsig_from, dsig_to = np.diff(np.r_[0.0, half_from]), np.diff(np.r_[0.0, half_to])
    out, moved = [], {}
    for name, data in records:
        key = name.strip()
        values = np.frombuffer(data, '<f8') if len(data) % 8 == 0 else None
        if key == 'nlev':
            out.append((name, struct.pack('<i', m)))
            continue
        if key in SPECTRAL_BY_LEVEL or key in GRID_BY_LEVEL or key in GRID_BY_LEVEL_AND_GROUND:
            levels = n + (key in GRID_BY_LEVEL_AND_GROUND)
            if values is None or values.size == 0 or values.size % levels:
                raise ValueError(f'{src}: {key} holds another size than {levels} levels of one field')
            x = values.reshape(levels, -1)               # Fortran's (point, level) order: one level after another
            new = remap(x[:n], half_from, half_to)
            if key in GRID_BY_LEVEL_AND_GROUND:
                new = np.concatenate([new, x[n:]])
            if key in CLIPPED:
                lo, hi = CLIPPED[key]
                new = np.clip(new, lo, hi)
            before = float(np.abs(dsig_from @ x[:n]).sum())
            after = float(np.abs(dsig_to @ new[:m]).sum())
            moved[key] = dict(points=int(x.shape[1]), levels=[levels, int(new.shape[0])],
                              column_integral_change=float(np.abs(dsig_to @ new[:m] - dsig_from @ x[:n]).max()),
                              column_integral_scale=max(before, after) / x.shape[1])
            out.append((name, np.ascontiguousarray(new, '<f8').tobytes()))
            continue
        if values is not None and values.size and key not in NOT_BY_LEVEL \
                and any(values.size == k * p for k in (n, n + 1) for p in widths):
            raise ValueError(f'{src}: {key} is sized like a field by level, one the carrier has no rule for')
        out.append((name, data))
    write_records(dst, out)
    return dict(source=str(src), source_sha256=hashlib.sha256(Path(src).read_bytes()).hexdigest(),
                written=str(dst), written_sha256=hashlib.sha256(Path(dst).read_bytes()).hexdigest(),
                levels=[n, m], fields=moved)
