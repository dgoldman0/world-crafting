"""The paper's figures, each drawn from an extract in paper/data/ (paper/figures/extract.py writes them).

    python3 paper/figures/figures.py            # from the repository root; writes paper/figures/fig*.pdf and .png
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, NullFormatter

from style import (AQUA, AXIS, BLUE, CONTEXT, FULL, HALF, INK, INK2, MUTED, ORANGE, RED, load, save)


def label(ax, x, y, text, **kw):
    kw.setdefault('color', INK2)
    kw.setdefault('fontsize', 7.5)
    ax.annotate(text, (x, y), **kw)


def fig_regimes():
    """Where found and crafted worlds sit against the ratios the models' Earth assumptions depend on."""
    rows = load('worlds')['rows']
    fig, (a, b) = plt.subplots(1, 2, figsize=(FULL, 2.9), gridspec_kw=dict(wspace=0.32))
    offsets = {'Earth': (6, -9), 'Mars': (6, 2), 'Titan': (6, -3), 'Venus': (6, -3), 'Open Moon 1.2 atm': (7, -3),
               'Mars at 1 bar': (6, -3)}
    names_a = {'Open Moon 1.2 atm': 'Open Moon\n(1.2 and 1.0 atm)'}
    for r in rows:
        moon = r['name'].startswith('Open Moon')
        colour = BLUE if moon else CONTEXT
        size = 34 if moon else 26
        face = colour if (r['kind'] == 'found' or moon) else 'white'
        for ax, x, y in ((a, r['h_over_r'], r['column_mass_over_earth']), (b, r['solar_day_days'], r['g_m_s2'])):
            ax.scatter([x], [y], s=size, color=face, edgecolor=colour, linewidth=1.2, zorder=3)
        if r['name'] in offsets:
            dx, dy = offsets[r['name']]
            label(a, r['h_over_r'], r['column_mass_over_earth'], names_a.get(r['name'], r['name']), xytext=(dx, dy),
                  textcoords='offset points', ha='left', va='center' if moon else 'baseline', color=INK if moon else INK2)
        names_b = {'Open Moon 1.2 atm': 'Open Moon', 'Mars': 'Mars, present and at 1 bar'}
        if r['name'] in names_b or r['name'] in ('Earth', 'Titan', 'Venus'):
            label(b, r['solar_day_days'], r['g_m_s2'], names_b.get(r['name'], r['name']), xytext=(6, -3) if not moon else (-6, 5),
                  textcoords='offset points', ha='left' if not moon else 'right', color=INK if moon else INK2)
    earth = next(r for r in rows if r['name'] == 'Earth')
    a.axvline(earth['h_over_r'], color=AXIS, lw=0.8, zorder=1)
    a.axhline(1.0, color=AXIS, lw=0.8, zorder=1)
    label(a, earth['h_over_r'] * 1.08, 330, "PlaSim's horizon air mass, 35: exact here", ha='left', va='top', color=MUTED,
          fontsize=7)
    label(a, 0.19, 0.85, "Earth's absorber paths:\nthe broadband fits' range", ha='right', va='top', color=MUTED, fontsize=7)
    a.set(xscale='log', yscale='log', xlim=(8e-4, 0.25), ylim=(5e-3, 400),
          xlabel='Scale height over radius, H/R', ylabel="Mass per unit area, relative to Earth's")
    a.set_title('Geometry and column', pad=6)
    b.axvline(1.0, color=AXIS, lw=0.8, zorder=1)
    b.axhline(9.80665, color=AXIS, lw=0.8, zorder=1)
    for day in (16.0, 64.0, 243.0):          # slowly rotating Earth-like planets of the GCM literature
        b.scatter([day], [9.80665], s=22, color='white', edgecolor=CONTEXT, linewidth=1.1, zorder=3)
    label(b, 64.0, 9.80665, 'slowly rotating\nEarth-like planets', xytext=(0, -24), textcoords='offset points', ha='center',
          va='bottom', color=INK2)
    label(b, 1.08, 1.0, "PlaSim's per-day\nformulas exact", ha='left', va='bottom', color=MUTED, fontsize=7)
    b.set(xscale='log', yscale='log', xlim=(0.5, 400), ylim=(0.9, 14),
          xlabel='Solar day (Earth days)', ylabel='Surface gravity (m s$^{-2}$)')
    b.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:g}'))
    b.yaxis.set_minor_formatter(NullFormatter())
    b.set_yticks([1, 2, 5, 10])
    b.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:g}'))
    b.set_title('Day and gravity', pad=6)
    save(fig, 'fig_regimes')


def fig_sun_clock():
    runs = load('sun_clock')['runs']
    old, new = runs['A28_dim5'], runs['A28_dim5_sun_test']
    fig, ax = plt.subplots(figsize=(HALF + 0.4, 2.3))
    ax.axhline(1.0, color=AXIS, lw=0.8, zorder=1)
    ax.plot(old['lon_deg'], old['relative'], color=ORANGE, zorder=3)
    ax.scatter(old['lon_deg'][::2], old['solang_relative'][::2], s=7, color='white', edgecolor=INK2, linewidth=0.6, zorder=4)
    ax.plot(new['lon_deg'], new['relative'], color=BLUE, zorder=3)
    i = int(np.argmax(old['relative']))
    label(ax, old['lon_deg'][i], old['relative'][i], "PlaSim's clock", xytext=(-6, 2), textcoords='offset points', ha='right')
    label(ax, 300, 1.012, 'synodic clock', ha='center', va='bottom')
    label(ax, 356, 0.952, "circles: PlaSim's\narithmetic alone", ha='right', va='center', color=MUTED, fontsize=7)
    ax.set(xlim=(0, 360), xticks=range(0, 361, 90), xlabel='Longitude (° E)', ylabel='Sunlight over its row mean')
    ax.set_title('Sunlight along the equator', pad=6)
    save(fig, 'fig_sun_clock')


def fig_slant():
    d = load('slant')
    el = np.asarray(d['elevation_deg'])
    fig, ax = plt.subplots(figsize=(HALF + 0.4, 2.3))
    flat = np.asarray([f if f < 1e299 else np.nan for f in d['flat']])
    keep = el >= 2.0
    ax.plot(el[keep], flat[keep], color=CONTEXT, zorder=2, label='flat column, 1/μ')
    ax.plot(el, d['plasim'], color=ORANGE, zorder=3, label="PlaSim's formula (Earth's)")
    ax.plot(el, d['moon_water'], color=BLUE, zorder=3, label='Moon, water vapour')
    ax.plot(el, d['moon_air'], color=AQUA, zorder=3, label='Moon, well-mixed air')
    for series in (d['plasim'], d['moon_water'], d['moon_air']):
        ax.annotate(f'{series[0]:.1f}', (el[0], series[0]), xytext=(3, 0), textcoords='offset points', ha='left', va='center',
                    color=INK2, fontsize=7, bbox=dict(boxstyle='square,pad=0.1', fc='white', ec='none'), zorder=6)
    ax.legend(loc='upper right', handlelength=1.4)
    ax.set(yscale='log', xlim=(0, 30), ylim=(0.9, 80), xlabel='Solar elevation (°)', ylabel='Slant path over vertical path')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:g}'))
    ax.set_title('Low-Sun path stretch', pad=6)
    save(fig, 'fig_slant')


def fig_layers():
    rows = load('layers')['rows']
    rows = [r for r in rows if r['layer'] != 'Whole column']
    y = np.arange(len(rows))[::-1]
    fig, ax = plt.subplots(figsize=(HALF + 0.4, 2.6))
    for yi, r in zip(y, rows):
        lo, hi = min(r['line_by_line'], r['as_run'], r['with_bands']), max(r['line_by_line'], r['as_run'], r['with_bands'])
        ax.plot([lo, hi], [yi, yi], color=AXIS, lw=0.8, zorder=1)
    ax.scatter([r['as_run'] for r in rows], y, s=26, color=ORANGE, edgecolor='white', linewidth=1.0, zorder=3, label='PlaSim as run')
    ax.scatter([r['with_bands'] for r in rows], y, s=26, color=BLUE, edgecolor='white', linewidth=1.0, zorder=4,
               label='PlaSim with CO$_2$ and O$_2$')
    ax.scatter([r['line_by_line'] for r in rows], y, s=30, marker='D', color=INK, edgecolor='white', linewidth=1.0, zorder=5,
               label='line by line')
    ax.set_yticks(y, [r['layer'] for r in rows])
    ax.tick_params(axis='y', length=0)
    ax.set(xlabel='Absorbed sunlight (W m$^{-2}$)', xlim=(-0.5, 20))
    ax.grid(axis='y', visible=False)
    ax.legend(loc='upper right', handletextpad=0.2, borderaxespad=0.2)
    ax.set_title('Sunlight absorbed by GCM layer', pad=6)
    save(fig, 'fig_layers')


def fig_repairs():
    rows = load('repairs')['rows']
    order = [r for r in rows if r['kind'] == 'repair'] + [r for r in rows if r['kind'] != 'repair']
    y = np.arange(len(order))[::-1].astype(float)
    y[len([r for r in rows if r['kind'] == 'repair']):] -= 0.6          # a gap before the sensitivity tests
    fig, ax = plt.subplots(figsize=(FULL, 2.7))
    for yi, r in zip(y, order):
        v = r['change_k']
        repair = r['kind'] == 'repair'
        colour = (RED if v > 0 else BLUE) if repair else CONTEXT
        ax.barh(yi, v, height=0.56, color=colour, zorder=3)
        text = f'{v:+.2f} K'.replace('-', '−')
        ax.annotate(text, (v, yi), xytext=(4 if v >= 0 else -4, 0), textcoords='offset points', ha='left' if v >= 0 else 'right',
                    va='center', color=INK2, fontsize=7)
    ax.axvline(0, color=INK2, lw=0.8, zorder=4)
    names = [r['label'].replace('CO2 and O2', 'CO₂ and O₂') for r in order]
    ax.set_yticks(y, names)
    ax.tick_params(axis='y', length=0)
    ax.grid(axis='y', visible=False)
    nrep = len([r for r in rows if r['kind'] == 'repair'])
    ax.text(-7.5, y[0] + 0.62, 'Repairs', color=INK, fontsize=7.5, fontweight='bold', va='bottom')
    ax.text(-7.5, y[nrep] + 0.62, "The cloud-water bound and two of PlaSim's Earth-tuned cloud settings", color=INK,
            fontsize=7.5, fontweight='bold', va='bottom')
    ax.set(xlim=(-7.5, 13.5), ylim=(y[-1] - 0.6, y[0] + 1.3), xlabel='Change in the global-mean surface temperature (K)')
    save(fig, 'fig_repairs')


def fig_gap():
    cases = load('gap45n')['cases']
    ctl, side = cases['ring_45n_corrected'], cases['ring_45n_corrected_sideways']
    names = [f"{L['km'][0]:.1f}–{L['km'][1]:.1f} km" for L in ctl]
    y = np.arange(len(ctl))
    fig, ax = plt.subplots(figsize=(HALF + 0.4, 2.3))
    for yi, c, s in zip(y, ctl, side):
        ax.plot([c['gcm_c'], c['ring_c']], [yi, yi], color=AXIS, lw=0.8, zorder=1)
    ax.scatter([c['gcm_c'] for c in ctl], y, s=30, marker='D', color=INK, edgecolor='white', linewidth=1.0, zorder=5, label='GCM')
    ax.scatter([c['ring_c'] for c in ctl], y, s=28, color=ORANGE, edgecolor='white', linewidth=1.0, zorder=3,
               label='CM1 ring')
    ax.scatter([s['ring_c'] for s in side], y, s=28, color=BLUE, edgecolor='white', linewidth=1.0, zorder=4,
               label="CM1 ring with the GCM's\nsideways transport")
    ax.set_yticks(y, names)
    ax.tick_params(axis='y', length=0)
    ax.grid(axis='y', visible=False)
    ax.set(xlabel='Layer-mean air temperature (°C)', xlim=(3, 28))
    ax.legend(loc='lower left', handletextpad=0.2)
    ax.set_title('CM1 and the GCM at 45° N', pad=6)
    save(fig, 'fig_gap')


if __name__ == '__main__':
    fig_regimes(); fig_sun_clock(); fig_slant(); fig_layers(); fig_repairs(); fig_gap()
