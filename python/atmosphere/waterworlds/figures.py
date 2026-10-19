"""Curves read from the images of Arnscheidt, Wordsworth and Ding's (2019) figures, for stage 9's comparison.

Each figure in the paper's arXiv source is a PDF holding one RGB image, its axes, lines and labels drawn in flat
colours. The reader decodes the image from the PDF's bytes and calibrates each axis from its tick marks: it finds the
middles of the tick labels in the band beside the axis, takes each tick as the run of dark pixels nearest its label
along the plot box's edge, translucent shading included and ticks drawn over by a curve left out, and fits the
labels' values, stated here figure by figure, through the ticks, refusing a fit that misses a tick by more than a
pixel. A curve's points are the middles of the runs of its colour in each pixel column (or row) inside the plot box,
outside the legend and the regions named for each figure; where a column holds several runs of the colour, the
longest serves, or the nearest to the last one taken where a label in the line's colour stands beside it, and a
column whose run touches another curve's colour, where that curve crosses it, is left out. Each axis records its
value per pixel, half of which is the resolution of its readings, and each curve's points their line's width.

    python -m atmosphere.waterworlds.figures --store STORE

writes the curves to STORE/products/paper-figures/<key>/figures.json, the key being the first 16 hex digits of the
sha256 of the source's sha256 and the reader's producer, its code and environment.
"""
from __future__ import annotations

from dataclasses import dataclass
import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import tarfile
import zlib

import numpy as np

AXIS_COLOUR = (38, 38, 38)


def images(source_tar: bytes) -> dict[str, np.ndarray]:
    """Each figure PDF's image in the arXiv source, by the PDF's name without its extension."""
    out = {}
    with tarfile.open(fileobj=io.BytesIO(source_tar), mode='r:gz') as tar:
        for member in tar.getmembers():
            if member.name.endswith('.pdf'):
                out[member.name[:-4]] = pdf_image(tar.extractfile(member).read())
    return out


def pdf_image(pdf: bytes) -> np.ndarray:
    """The one RGB image of an 8-bit, Flate-coded PDF image XObject, rows from the top."""
    found = [m for m in re.finditer(rb'<<(?:(?!>>).)*?/Subtype\s*/Image(?:(?!stream).)*?>>\s*stream\r?\n', pdf, re.S)]
    if len(found) != 1:
        raise ValueError(f'the PDF holds {len(found)} images, where the reader takes one')
    head = found[0].group(0)
    width = int(re.search(rb'/Width\s+(\d+)', head).group(1))
    height = int(re.search(rb'/Height\s+(\d+)', head).group(1))
    if b'/DeviceRGB' not in head or not re.search(rb'/BitsPerComponent\s+8', head) or b'/FlateDecode' not in head:
        raise ValueError('the reader takes 8-bit RGB images under Flate coding')
    if b'/DecodeParms' in head:
        raise ValueError('the reader takes images without a predictor')
    raw = zlib.decompressobj().decompress(pdf[found[0].end():])
    if len(raw) != width * height * 3:
        raise ValueError(f'the image stream holds {len(raw)} bytes, where {width} x {height} RGB takes '
                         f'{width * height * 3}')
    return np.frombuffer(raw, dtype=np.uint8).reshape(height, width, 3)


def runs(mask: np.ndarray) -> list[tuple[int, int]]:
    """The first and last indices of each run of True."""
    idx = np.nonzero(mask)[0]
    if idx.size == 0:
        return []
    groups = np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1)
    return [(int(g[0]), int(g[-1])) for g in groups]


def colour_mask(img: np.ndarray, colour, tolerance: int = 24) -> np.ndarray:
    return np.abs(img.astype(int) - np.asarray(colour)).sum(axis=2) <= tolerance


@dataclass(frozen=True)
class Axis:
    """Tick positions in pixels and their labels; `form` 'linear', or 'sqrt' where the axis is linear in the
    square root of its labels (Figure 2's scaling factors)."""
    pixels: tuple
    labels: tuple
    form: str = 'linear'

    def _coordinate(self, values):
        values = np.asarray(values, dtype=float)
        return np.sqrt(values) if self.form == 'sqrt' else values

    @property
    def fit(self):
        return np.polyfit(np.asarray(self.pixels, dtype=float), self._coordinate(self.labels), 1)

    def value(self, pixel):
        c = np.polyval(self.fit, np.asarray(pixel, dtype=float))
        return c ** 2 if self.form == 'sqrt' else c

    @property
    def residual_pixels(self) -> float:
        slope, intercept = self.fit
        return float(np.max(np.abs((self._coordinate(self.labels) - intercept) / slope - np.asarray(self.pixels))))


def tick_positions(img: np.ndarray, *, along: str, line: int, inward: int, span: tuple[int, int],
                   length: int = 10, colour=AXIS_COLOUR, tolerance: int = 160) -> list[float]:
    """The middles of the tick marks on one edge of a plot box: along 'x' (ticks on a horizontal edge at row
    `line`, reaching `inward` rows into the box) or 'y' (on a vertical edge at column `line`)."""
    grey = np.abs(img.astype(int) - np.asarray(colour)).sum(axis=2) <= tolerance
    grey &= (np.ptp(img.astype(int), axis=2) < 12)
    lo, hi = sorted((line + int(math.copysign(2, inward)), line + inward))
    if along == 'x':
        hits = grey[lo:hi + 1, span[0]:span[1]].sum(axis=0) >= length
    else:
        hits = grey[span[0]:span[1], lo:hi + 1].sum(axis=1) >= length
    return [span[0] + (a + b) / 2 for a, b in runs(hits)]


def curve(img: np.ndarray, colour, *, box: tuple[int, int, int, int], exclude=(), tolerance: int = 24,
          min_run: int = 3, scan: str = 'columns', track: bool = False,
          occluders=()) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """For each pixel column (or row) of the box (left, top, right, bottom), the middle and width of the longest
    run of the colour, outside the excluded boxes, or with `track` the run nearest the last one taken, so that a
    label written in the line's colour beside it is passed over; a run that touches one of the `occluders`' colours,
    a curve drawn over this one, is left out. Returns the positions scanned, the middles and the widths."""
    mask = colour_mask(img, colour, tolerance)
    hidden = np.zeros(mask.shape, dtype=bool)
    for other in occluders:
        hidden |= colour_mask(img, other, tolerance)
    for left, top, right, bottom in exclude:
        mask[top:bottom + 1, left:right + 1] = False
    left, top, right, bottom = box
    pos, mid, width = [], [], []
    for k in (range(left + 1, right) if scan == 'columns' else range(top + 1, bottom)):
        line = mask[top + 1:bottom, k] if scan == 'columns' else mask[k, left + 1:right]
        found = [(a, b) for a, b in runs(line) if b - a + 1 >= min_run]
        if found and occluders:
            under = hidden[top + 1:bottom, k] if scan == 'columns' else hidden[k, left + 1:right]
            found = [(a, b) for a, b in found if not under[max(a - 2, 0):b + 3].any()]
        if found:
            if track and mid:
                last = mid[-1] - (top + 1 if scan == 'columns' else left + 1)
                a, b = min(found, key=lambda r: abs((r[0] + r[1]) / 2 - last))
            else:
                a, b = max(found, key=lambda r: r[1] - r[0])
            pos.append(k)
            mid.append((top + 1 if scan == 'columns' else left + 1) + (a + b) / 2)
            width.append(b - a + 1)
    return np.array(pos, dtype=float), np.array(mid), np.array(width)


def label_centres(img: np.ndarray, *, rows: tuple[int, int], columns: tuple[int, int], gap: int,
                  scan: str = 'columns', colour=AXIS_COLOUR, tolerance: int = 60) -> list[float]:
    """The middles of the labels in a band of the image: runs of the labels' colour along the band, joined across
    gaps narrower than `gap` (the space between one label's characters)."""
    dark = np.abs(img.astype(int) - np.asarray(colour)).sum(axis=2) <= tolerance
    region = dark[rows[0]:rows[1], columns[0]:columns[1]]
    profile = region.sum(axis=0) if scan == 'columns' else region.sum(axis=1)
    joined = []
    for a, b in runs(profile > 0):
        if joined and a - joined[-1][1] < gap:
            joined[-1] = (joined[-1][0], b)
        else:
            joined.append((a, b))
    start = columns[0] if scan == 'columns' else rows[0]
    return [start + (a + b) / 2 for a, b in joined]


def refine_ticks(img: np.ndarray, guesses, *, along: str, line: int, inward: int, length: int = 10,
                 window: int = 8, darkness: int = 150) -> list[float]:
    """Each tick's middle, found within `window` pixels of its guess as a run of dark pixels at least `length`
    long reaching `inward` from the box's edge at `line`; dark is a luminance below `darkness`, so that ticks under
    a translucent fill count."""
    lum = img.astype(int).mean(axis=2)
    lo, hi = sorted((line + int(math.copysign(2, inward)), line + inward))
    out = []
    for guess in guesses:
        g0 = int(round(guess))
        span = range(g0 - window, g0 + window + 1)
        if along == 'x':
            hits = np.array([(lum[lo:hi + 1, k] < darkness).sum() >= length for k in span])
        else:
            hits = np.array([(lum[k, lo:hi + 1] < darkness).sum() >= length for k in span])
        found = runs(hits)
        if found:
            a, b = min(found, key=lambda r: abs((r[0] + r[1]) / 2 - window))
            out.append(g0 - window + (a + b) / 2)
        else:
            out.append(None)                     # a tick drawn over by a curve
    return out


def axis_from_ticks(ticks, labels, form: str = 'linear', max_residual: float = 1.0) -> Axis:
    """The axis through the ticks found, those drawn over left out, refused where its fit misses a tick by more
    than `max_residual` pixels or fewer than three ticks remain."""
    pairs = [(t, v) for t, v in zip(ticks, labels) if t is not None]
    if len(pairs) < 3:
        raise ValueError(f'{len(pairs)} ticks found, where an axis takes three')
    axis = Axis(tuple(t for t, _ in pairs), tuple(v for _, v in pairs), form)
    if axis.residual_pixels > max_residual:
        raise ValueError(f'the ticks stray {axis.residual_pixels:.2f} pixels from their fit')
    return axis


def _axis(img, *, labels_rows, labels_columns, gap, scan, along, line, inward, values, form='linear', window=10):
    guesses = label_centres(img, rows=labels_rows, columns=labels_columns, gap=gap, scan=scan)
    if len(guesses) != len(values):
        raise ValueError(f'{len(guesses)} labels found where the axis has {len(values)}')
    return axis_from_ticks(refine_ticks(img, guesses, along=along, line=line, inward=inward, window=window),
                           values, form)


def _axes(ax=None, ay=None) -> dict:
    """Each axis's fit, its form, and its coordinate per pixel (the value, or for a 'sqrt' axis its square root),
    half of which is its readings' resolution."""
    out = {}
    for name, axis in (('x', ax), ('y', ay)):
        if axis is not None:
            out[name] = dict(fit=axis.fit.tolist(), form=axis.form, coordinate_per_px=abs(float(axis.fit[0])))
    return out


def _points(axis_x, axis_y, scanned):
    x, y, width = scanned
    return dict(x=axis_x.value(x).tolist(), y=axis_y.value(y).tolist(), width_px=width.tolist())


def figure_2(img: np.ndarray) -> dict:
    """The right panel: the emitting and absorbing surfaces' (r/r_s)^2 against surface temperature, for 0.12 Earth
    masses around the Sun. Its axis is linear in r/r_s, its ticks labelled with the squares."""
    box = (1620, 37, 2792, 692)
    ax = _axis(img, labels_rows=(700, 790), labels_columns=(1560, 3051), gap=25, scan='columns', along='x',
               line=692, inward=-15, values=(200, 300, 400, 500, 600))
    ay = _axis(img, labels_rows=(30, 720), labels_columns=(2800, 2930), gap=12, scan='rows', along='y', line=2792,
               inward=-15, values=(1.4, 1.3, 1.2, 1.1, 1.0), form='sqrt', window=12)
    legend = (1640, 55, 2420, 250)
    # The dotted lines that carry each surface at 400 K across to the left panel end on their curve near 396 K; the
    # blue one crosses the red curve near 300 K.
    red_dots, blue_dots = (1620, 370, 2200, 395), (1620, 570, 2200, 595)
    red, blue = (254, 0, 0), (0, 0, 254)
    return dict(x='surface temperature, K', y='(r/r_s)^2', axes=_axes(ax, ay),
                emitting=_points(ax, ay, curve(img, red, box=box, exclude=(legend, red_dots), min_run=8,
                                                occluders=(blue,))),
                absorbing=_points(ax, ay, curve(img, blue, box=box, exclude=(legend, blue_dots), min_run=8,
                                                 occluders=(red,))))


def figure_3(img: np.ndarray) -> dict:
    """The instellation holding each surface temperature at 2.3 m/s^2 around the Sun, with expanding surfaces, with
    none, and with the surface's sigma T^4 up to the runaway limit; the shading of long-lived liquid water; and the
    lifetimes on the top axis."""
    box = (351, 256, 2043, 1384)
    ax = _axis(img, labels_rows=(1395, 1470), labels_columns=(330, 2073), gap=25, scan='columns', along='x',
               line=1384, inward=-20, values=(250, 300, 350, 400, 450, 500))
    ay = _axis(img, labels_rows=(230, 1410), labels_columns=(180, 340), gap=15, scan='rows', along='y', line=351,
               inward=20, values=(1700, 1600, 1500, 1400, 1300, 1200, 1100))
    legend, text = (402, 295, 1725, 620), (880, 950, 1850, 1075)
    shade = colour_mask(img, (204, 204, 255), 6)
    edges = [runs(shade[r, box[0]:box[2]]) for r in range(700, 1380)]
    left = float(ax.value(box[0] + np.median([e[0][0] for e in edges if e]) - 0.5))
    right = float(ax.value(box[0] + np.median([e[-1][1] for e in edges if e]) + 0.5))
    ticks = [t for t in tick_positions(img, along='x', line=256, inward=20, span=(353, 2000))]
    if len(ticks) != 3:
        raise ValueError(f'{len(ticks)} lifetime ticks found where Figure 3 has three')
    return dict(x='surface temperature, K', y='instellation, W/m^2', axes=_axes(ax, ay),
                expanding=_points(ax, ay, curve(img, (0, 0, 0), box=box, exclude=(legend, text), min_run=8)),
                no_expansion=_points(ax, ay, curve(img, (51, 51, 51), box=box, exclude=(legend, text), tolerance=10,
                                                   min_run=6)),
                blackbody=_points(ax, ay, curve(img, (179, 179, 179), box=box, exclude=(legend, text), tolerance=10,
                                                min_run=6)),
                long_lived=dict(from_k=left, to_k=right),
                lifetime_ticks_k={'1e11': float(ax.value(ticks[0])), '1e9': float(ax.value(ticks[1])),
                                  '1e7': float(ax.value(ticks[2]))})


def _arrow(img: np.ndarray, colour, rows: tuple[int, int], columns: tuple[int, int]) -> float:
    """The middle column of a dotted vertical arrow of the colour within the rows: the run of columns holding at
    least half the most pixels of the colour that any column holds there."""
    counts = colour_mask(img, colour, 12)[rows[0]:rows[1], columns[0]:columns[1]].sum(axis=0)
    if counts.max() == 0:
        raise ValueError(f'no arrow of colour {colour} in rows {rows}')
    a, b = max(runs(counts >= 0.5 * counts.max()), key=lambda r: counts[r[0]:r[1] + 1].sum())
    return columns[0] + (a + b) / 2


def figure_5(img: np.ndarray) -> dict:
    """Steady surface temperatures against distance from the Sun at 2.3 m/s^2: the ocean's at an albedo of 0.2 and
    the snowballs' at 0.25, 0.32 and 0.4; the dotted arrows at which each snowball thaws into the ocean and the ocean
    freezes, read from the image, with each snowball curve's last state, extrapolated to its arrow, and the ocean's
    temperature there; the shading of short-lived water; and the lifetimes on the right axis."""
    box = (250, 40, 1639, 1032)
    ax = _axis(img, labels_rows=(1040, 1110), labels_columns=(200, 1700), gap=25, scan='columns', along='x',
               line=1032, inward=-15, values=(0.9, 0.95, 1.0, 1.05), window=12)
    ay = _axis(img, labels_rows=(20, 1060), labels_columns=(110, 245), gap=12, scan='rows', along='y', line=250,
               inward=15, values=(500, 450, 400, 350, 300, 250), window=12)
    legend = (1000, 70, 1639, 455)
    row = lambda t: int(round((t - ay.fit[1]) / ay.fit[0]))
    colours = {'0.25': (153, 153, 153), '0.32': (102, 102, 102), '0.4': (0, 0, 0)}
    ocean_colour, freeze_colour = (0, 113, 189), (0, 0, 254)
    # Each snowball's arrow rises from its curve's end into the ocean, above 276 K; the ocean's own arrow falls from
    # its curve's end below 272 K to 238 K, a stem long enough to outweigh its head's wide arms.
    arrows = {a: _arrow(img, c, (row(292.0 if a == '0.25' else 410.0), row(276.0)), (box[0] + 1, box[2]))
              for a, c in colours.items()}
    freeze = _arrow(img, freeze_colour, (row(272.0), row(238.0)), (box[0] + 1, box[2]))
    strips = tuple((int(round(c)) - 6, box[1] + 1, int(round(c)) + 6, box[3] - 1) for c in (*arrows.values(), freeze))
    shade = colour_mask(img, (255, 103, 102), 8)
    bottom = [runs(shade[box[1] + 1:box[3], c]) for c in range(box[0] + 5, legend[0] - 10)]   # left of the legend
    short_lived_from = float(ay.value(box[1] + 1 + np.median([b[-1][1] for b in bottom if b]) + 0.5))
    ticks = tick_positions(img, along='y', line=1639, inward=-15, span=(45, 600))
    if len(ticks) != 3:
        raise ValueError(f'{len(ticks)} lifetime ticks found where Figure 5 has three')
    ocean_px = curve(img, ocean_colour, box=box, exclude=(legend,) + strips, tolerance=10, min_run=5)
    ocean = _points(ax, ay, ocean_px)
    ox, oy = np.asarray(ocean['x']), np.asarray(ocean['y'])
    order = np.argsort(ox)
    out = dict(x='distance from the Sun, AU', y='surface temperature, K', axes=_axes(ax, ay),
               short_lived_from_k=short_lived_from,
               lifetime_ticks_k={'1e7': float(ay.value(ticks[0])), '1e9': float(ay.value(ticks[1])),
                                 '1e11': float(ay.value(ticks[2]))},
               **{'ocean_0.2': ocean})
    ocean_end = np.polyfit(ox[order][-15:], oy[order][-15:], 1)
    out['ocean_freeze'] = dict(arrow_au=float(ax.value(freeze)), end_k=float(np.polyval(ocean_end, ax.value(freeze))))
    # The snowballs stand below 273 K; their search stops there, below the labels and the shading.
    snow_box = (box[0], row(273.5), box[2], box[3])
    for a, colour in colours.items():
        points = _points(ax, ay, curve(img, colour, box=snow_box, exclude=(legend,) + strips, tolerance=10, min_run=5))
        x, y = np.asarray(points['x']), np.asarray(points['y'])
        near = np.argsort(np.abs(x - ax.value(arrows[a])))[:15]                 # the curve's end beside its arrow
        end = np.polyfit(x[near], y[near], 1)
        arrow_au = float(ax.value(arrows[a]))
        out[f'snowball_{a}'] = dict(points, arrow_au=arrow_au, end_k=float(np.polyval(end, arrow_au)),
                                    to_k=float(np.interp(arrow_au, ox[order], oy[order])))
    return out


def figure_4(img: np.ndarray) -> dict:
    """Steady surface temperatures and water lifetimes over distance and gravity, around the Sun (left) and AD Leonis
    (right): for each panel the 273 K contour, where the shading of temperate states meets the white of the
    snowballs, and the 10^9-year contour, read row by row; the dashed transition and the dotted line of Ganymede's
    mass, read as gravities."""
    top, bottom = 44, 1147
    ay = _axis(img, labels_rows=(40, 1160), labels_columns=(460, 530), gap=12, scan='rows', along='y', line=535,
               inward=15, values=(2.4, 2.2, 2.0, 1.8, 1.6, 1.4, 1.2), window=12)
    panels = dict(sun=dict(box=(535, top, 1748, bottom), labels=(480, 1800), values=(0.9, 0.95, 1.0, 1.05, 1.1)),
                  ad_leonis=dict(box=(1833, top, 3046, bottom), labels=(1800, 3100), values=(0.15, 0.16, 0.17)))
    lum = img.astype(int).mean(axis=2)
    out = dict(x='distance from the star, AU', y='surface gravity, m/s^2')
    for name, panel in panels.items():
        box = panel['box']
        ax = _axis(img, labels_rows=(1155, 1235), labels_columns=panel['labels'], gap=25, scan='columns',
                   along='x', line=bottom, inward=-15, values=panel['values'])
        # The 10^9-year contour, tracked down from the top so that its inline label is passed over.
        rows, xs, widths = curve(img, (0, 0, 179), box=box, scan='rows', track=True, min_run=4, tolerance=12)
        billion = dict(g=ay.value(rows).tolist(), d=ax.value(xs).tolist(), width_px=widths.tolist())
        # The 273 K contour: in each row the rightmost pixel of the temperate shading, which ends at a thin line.
        r, g, b = (img[:, :, c].astype(int) for c in range(3))
        pink = (r > 240) & (g < 245) & (np.abs(g - b) < 8) & (r - g >= 8)      # neutral greys stay out
        g273, d273 = [], []
        for r in range(top + 2, bottom - 1):
            cols = np.nonzero(pink[r, box[0] + 2:box[2] - 1])[0]
            if cols.size:
                g273.append(float(ay.value(r)))
                d273.append(float(ax.value(box[0] + 2 + cols[-1] + 0.5)))
        out[name] = dict(axes=dict(x=_axes(ax)['x']), billion_years=billion, freezing=dict(g=g273, d=d273))
    # The horizontal lines across both panels, as rows of dark pixels in the left panel: the dashed transition, dark
    # over half the row, and Ganymede's mass, dotted, in over sixty short runs.
    left = panels['sun']['box']
    dashed = [r for r in range(top + 2, bottom - 1) if (lum[r, left[0] + 1:left[2]] < 120).sum() > 400]
    grey = colour_mask(img, (51, 51, 51), 30)[:, left[0] + 1:left[2]]
    dotted = [r for r in range(top + 2, bottom - 1) if 100 < grey[r].sum() < 400 and len(runs(grey[r])) > 60]
    if not dashed or not dotted:
        raise ValueError('Figure 4 lacks its dashed transition or its dotted line of Ganymede')
    out['axes'] = dict(y=_axes(ay=ay)['y'])
    out['transition_g'] = float(ay.value(np.mean(dashed)))
    out['ganymede_g'] = float(ay.value(np.mean(dotted)))
    return out


READERS = dict(figure2=figure_2, figure3=figure_3, figure4=figure_4, figure5=figure_5)
SCHEMA = 'world-crafting.waterworlds.paper-figures/2'
EVIDENCE = ("Values read from the images of the paper's Figures 2 to 5 in its arXiv source: each axis fitted through "
            "its ticks to within a pixel, each curve's points the middles of its colour's runs; a reading of the "
            "published figures, credited to their authors, whose resolution is half a pixel of each axis.")


def producer() -> dict:
    """The reader's code and environment."""
    import platform
    return dict(module='atmosphere.waterworlds.figures',
                sources={'atmosphere/waterworlds/figures.py': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                environment=dict(python=platform.python_version(), numpy=np.__version__))


def read_all(source_tar: bytes) -> dict:
    """The curves of Figures 2 to 5, with the source's sha256, the reader's producer and the evidence."""
    found = images(source_tar)
    out = dict(schema=SCHEMA, source_sha256=hashlib.sha256(source_tar).hexdigest(), producer=producer(),
               evidence=EVIDENCE,
               credit='Arnscheidt, C. W., Wordsworth, R. D. & Ding, F. (2019), ApJ 881, 60, Figures 2 to 5, read '
                      'from the images in the arXiv source of version 2')
    for name, reader in READERS.items():
        out[name] = reader(found[name])
    return out


def key(figures: dict) -> str:
    """The sha256 of the source's sha256 and the reader's producer."""
    return hashlib.sha256(json.dumps(dict(source=figures['source_sha256'], producer=figures['producer']),
                                     sort_keys=True).encode()).hexdigest()


def without_nan(value):
    """The value with every NaN as None, so that the JSON written is standard."""
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, dict):
        return {k: without_nan(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [without_nan(v) for v in value]
    return value


def write(path: Path, product: dict) -> str:
    """Writes a product atomically, NaN as null, and returns the file's sha256."""
    data = (json.dumps(without_nan(product), indent=1, allow_nan=False) + '\n').encode()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    part = path.with_suffix(path.suffix + f'.part{os.getpid()}')
    part.write_bytes(data)
    part.replace(path)
    return hashlib.sha256(data).hexdigest()


def read(path: Path) -> dict:
    figures = json.loads(Path(path).read_text())
    if figures.get('schema') != SCHEMA:
        raise ValueError(f'{path}: schema {figures.get("schema")!r}, where the reader takes {SCHEMA}')
    return figures


def source_bytes() -> bytes:
    """The paper's arXiv source, refused unless the restorer finds it whole by its size and sha256."""
    from atmosphere.waterworlds import fetch_inputs
    if fetch_inputs.restore()['status'] != 'PASS':
        raise ValueError("the paper's source is missing or changed (atmosphere.waterworlds.fetch_inputs)")
    return fetch_inputs.path(SOURCE).read_bytes()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--store', type=Path, help="the lab's store, which places the curves")
    parser.add_argument('--out', type=Path, help="the curves' file, in place of the store")
    args = parser.parse_args(argv)
    if (args.store is None) == (args.out is None):
        parser.error('give --store or --out')
    figures = read_all(source_bytes())
    out = args.out or args.store / 'products' / 'paper-figures' / key(figures)[:16] / 'figures.json'
    print(out, write(out, figures))
    return 0


SOURCE = 'arnscheidt2019_arxiv_1906.10561v2.tar.gz'

if __name__ == '__main__':
    raise SystemExit(main())
