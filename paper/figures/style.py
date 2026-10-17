"""Print style for the paper's figures: the validated reference palette (light), thin marks, recessive axes.

Palette validated on 2026-10-17 with the dataviz skill's validate_palette.js against a white surface: the first three
categorical slots pass every gate (aqua sits at 2.82:1 contrast, so every series is direct-labelled and every figure's
numbers are in paper/data/); blue and red pass all-pairs as the diverging poles.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'paper' / 'data'
OUT = ROOT / 'paper' / 'figures'

INK, INK2, MUTED = '#0b0b0b', '#52514e', '#898781'
GRID, AXIS = '#e1e0d9', '#c3c2b7'
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'     # categorical slots 1-3, in this order
RED, NEUTRAL = '#e34948', '#f0efec'                     # diverging pole and midpoint
CONTEXT = '#b9b7ae'                                     # de-emphasised marks

FULL, HALF = 6.3, 3.05                                  # inches: text width, column of a two-panel figure

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.sans-serif': ['DejaVu Sans'], 'font.size': 8,
    'axes.edgecolor': AXIS, 'axes.linewidth': 0.6, 'axes.labelcolor': INK2, 'axes.titlesize': 8.5,
    'axes.titleweight': 'bold', 'axes.titlecolor': INK, 'axes.titlelocation': 'left',
    'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.color': GRID,
    'grid.linewidth': 0.5, 'grid.linestyle': '-', 'xtick.color': MUTED, 'ytick.color': MUTED,
    'xtick.labelcolor': INK2, 'ytick.labelcolor': INK2, 'xtick.major.width': 0.5, 'ytick.major.width': 0.5,
    'xtick.major.size': 2.5, 'ytick.major.size': 2.5, 'xtick.minor.size': 1.5, 'ytick.minor.size': 1.5,
    'lines.linewidth': 1.5, 'lines.solid_capstyle': 'round', 'lines.solid_joinstyle': 'round',
    'legend.frameon': False, 'legend.fontsize': 7.5, 'legend.labelcolor': INK2,
    'savefig.dpi': 300, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.03, 'pdf.fonttype': 42,
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
})


def load(name: str) -> dict:
    return json.loads((DATA / f'{name}.json').read_text())


def save(fig, name: str) -> None:
    for ext in ('pdf', 'png'):
        fig.savefig(OUT / f'{name}.{ext}')
    plt.close(fig)
    print('wrote', f'paper/figures/{name}.pdf')
