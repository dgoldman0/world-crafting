"""Stage 9's comparison of the lab's steam worlds with the paper's Figures 2 to 5 (Arnscheidt, Wordsworth and Ding 2019).

The paper's curves come from figures.py's product; the lab's from the steam columns' table (steam_table), from
columns computed directly at Figure 2's 0.12 Earth masses, which lies beyond the table's gravities, and from the
energy balance and the wind. Each comparison sets the lab's value beside the paper's at the same abscissa, the paper's
interpolated linearly along its curve and NaN beyond it; the wind's sound speed takes the factors named, 1 for the
paper's equations as printed, 1.2722 for the paper's transition and 4/3 for Figure 3's lifetimes
(notes/waterworlds.md). The paper's AD Leonis takes the flux its Figure 4 implies, from the distances of the two
stars' 273 K contours, which carries the paper's own ratio of the two stars' absorbing factors, and the
temperature given; the Sun gives 1,361 W/m^2 at 1 AU (shared/constants.json), a value the paper leaves unstated.

    python -m atmosphere.waterworlds.comparison --store STORE --table TABLE.json --figures FIGURES.json

writes the comparison to STORE/products/steam-comparison/<key>/comparison.json, NaN as null, the key covering the
table's and the figures' files, the optics' key, the Sun's flux, the red star's temperature and the producer: the
code of every module the comparison runs and the versions of Python, numpy and scipy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np

from shared.constants import SOLAR_CONSTANT
from atmosphere.waterworlds import (balance as bl, escape as es, figures as fg, maps, radiating as rd, steam,
                                    steam_optics as so, steam_table as tb)
from atmosphere.waterworlds.body import Waterworld

SCHEMA = 'world-crafting.waterworlds.steam-comparison/2'
BILLION_YEARS = 1e9 * es.YEAR_S
FACTORS = (1.0, 1.2722, 4 / 3)
GANYMEDE_KG = 1.4819e23


def _paper(curve: dict, x):
    """The paper's curve at x, linear between its points, NaN beyond them."""
    xs, ys = np.asarray(curve['x'], dtype=float), np.asarray(curve['y'], dtype=float)
    order = np.argsort(xs)
    xs, ys = xs[order], ys[order]
    x = np.asarray(x, dtype=float)
    return np.where((x >= xs[0]) & (x <= xs[-1]), np.interp(x, xs, ys), np.nan)


def _name(f: float) -> str:
    return f'{f:.4f}'


def figure_2(paper: dict, optics, temperatures=(250.0, 300.0, 350.0, 400.0, 450.0, 500.0, 550.0, 598.0),
             bands=so.BANDS) -> dict:
    """The scaling factors of a world of 0.12 Earth masses around the Sun, the layers' masses at the surface's
    gravity."""
    world = Waterworld(0.12)
    rows = []
    for t_s in temperatures:
        col = steam.column(world, t_s, optical_gravity='surface')
        r = rd.surfaces(col, rd.column_spectra(col, optics, bands), (5772.0,))
        rows.append(dict(t_s=t_s, lab_emitting=r['lw_factor'], lab_absorbing=r['sw'][5772.0]['factor'],
                         paper_emitting=float(_paper(paper['emitting'], t_s)),
                         paper_absorbing=float(_paper(paper['absorbing'], t_s))))
    return dict(earth_masses=0.12, rows=rows)


def _row(table: dict, gravity: float) -> int:
    g = np.asarray(table['gravities'], dtype=float)
    i = int(np.argmin(np.abs(g - gravity)))
    if abs(g[i] - gravity) > 1e-9:
        raise ValueError(f'the table holds no row at {gravity} m/s^2')
    return i


def figure_3(paper: dict, table: dict, sun: maps.Star, gravity: float = 2.3) -> dict:
    """The instellation holding each surface temperature at 2.3 m/s^2 around the Sun, with and without the expanding
    surfaces, for each factor on the wind's sound speed; and the temperatures of the paper's lifetimes."""
    i = _row(table, gravity)
    world = Waterworld.from_gravity(gravity)
    olr = np.asarray(table['olr'], dtype=float)[i]
    rows = []
    expanding = {f: maps.instellations(table, sun, factor=f)[i] for f in FACTORS}
    for j, t_s in enumerate(table['temperatures']):
        row = dict(t_s=float(t_s), paper_expanding=float(_paper(paper['expanding'], t_s)),
                   paper_no_expansion=float(_paper(paper['no_expansion'], t_s)))
        for f in FACTORS:
            row[f'lab_expanding_{_name(f)}'] = float(expanding[f][j])
            row[f'lab_no_expansion_{_name(f)}'] = bl.instellation(world, t_s, olr[j], 1.0, 1.0, factor=f)
        rows.append(row)
    lifetimes = {label: dict(paper=paper['lifetime_ticks_k'][label],
                             **{f'lab_{_name(f)}': float(maps.lifetime_temperatures([gravity], years * es.YEAR_S, f)[0])
                                for f in FACTORS})
                 for label, years in (('1e11', 1e11), ('1e9', 1e9), ('1e7', 1e7))}
    return dict(gravity=gravity, rows=rows, lifetimes_k=lifetimes, long_lived=paper['long_lived'])


def implied_flux_ratio(paper: dict, gravities=(1.6, 1.8, 2.0, 2.2, 2.4)) -> float:
    """The flux of the paper's AD Leonis at 1 AU as a share of the Sun's: the square of the ratio of the distances of
    the two stars' 273 K contours, where the stars' absorbing factors differ least, averaged over `gravities`."""
    ratios = []
    for g in gravities:
        sun = float(_paper(dict(x=paper['sun']['freezing']['g'], y=paper['sun']['freezing']['d']), g))
        red = float(_paper(dict(x=paper['ad_leonis']['freezing']['g'], y=paper['ad_leonis']['freezing']['d']), g))
        ratios.append((red / sun) ** 2)
    return float(np.mean(ratios))


def figure_4(paper: dict, table: dict, stars: dict) -> dict:
    """For each star and gravity, the distances of the 273 K contour and of the 10^9-year contour, the lab's for each
    factor and the paper's; the transition's gravity; and the gravity of Ganymede's mass on the size relation."""
    g = np.asarray(table['gravities'], dtype=float)
    out = dict(transition=dict(paper=paper['transition_g'],
                               **{f'lab_{_name(f)}': es.lifetime_gravity(273.0, BILLION_YEARS, f) for f in FACTORS}),
               ganymede=dict(paper=paper['ganymede_g'],
                             lab=Waterworld(GANYMEDE_KG / Waterworld(1.0).mass_kg).gravity_m_s2))
    for name, star in stars.items():
        freezing_paper = _paper(dict(x=paper[name]['freezing']['g'], y=paper[name]['freezing']['d']), g)
        billion_paper = _paper(dict(x=paper[name]['billion_years']['g'], y=paper[name]['billion_years']['d']), g)
        rows = []
        for f in FACTORS:
            freezing = maps.contour_distance(table, star, np.full(g.size, 273.0), factor=f)
            t9 = maps.lifetime_temperatures(g, BILLION_YEARS, f)
            billion = maps.contour_distance(table, star, t9, factor=f)
            for i in range(g.size):
                rows.append(dict(factor=f, g=float(g[i]), lab_freezing=float(freezing[i]),
                                 paper_freezing=float(freezing_paper[i]), lab_billion=float(billion[i]),
                                 paper_billion=float(billion_paper[i]), lab_billion_k=float(t9[i])))
        out[name] = dict(flux_1au_w_m2=star.flux_1au_w_m2, temperature_k=star.temperature_k, rows=rows)
    return out


def figure_5(paper: dict, table: dict, sun: maps.Star, gravity: float = 2.3, ice_albedos=(0.25, 0.32, 0.4)) -> dict:
    """At 2.3 m/s^2 around the Sun: the ocean's steady temperature against distance at an albedo of 0.2; for each ice
    albedo the distance at which the snowball thaws and the ocean's temperature there, to which its deglaciation
    leads; and the distance at which the ocean freezes; for each factor. The lab thaws each snowball at 273 K, the
    paper's definition, and also at the temperature where the paper's curve ends beside its arrow, so that the two
    stand like for like; the paper's distances are its arrows'."""
    i = _row(table, gravity)
    t = np.asarray(table['temperatures'], dtype=float)
    out = dict(gravity=gravity, short_lived_from_k=dict(
        paper=paper['short_lived_from_k'],
        **{f'lab_{_name(f)}': float(maps.lifetime_temperatures([gravity], BILLION_YEARS, f)[0]) for f in FACTORS}))
    for f in FACTORS:
        water = maps.instellations(table, sun, albedo=bl.ALBEDO, factor=f)[i]
        ocean = []
        for d in np.round(np.arange(0.90, 1.0701, 0.01), 4):
            roots = bl.branch_temperatures(sun.flux_1au_w_m2 / d ** 2, t, water, water)['water']
            ocean.append(dict(d=float(d), lab=roots[0] if roots else math.nan,
                              paper=float(_paper(paper['ocean_0.2'], d))))
        snow = {}
        for a in ice_albedos:
            ice = maps.instellations(table, sun, albedo=a, factor=f)[i]
            drawn = paper[f'snowball_{a}']
            entry = dict(paper_melt_au=drawn['arrow_au'], paper_end_k=drawn['end_k'], paper_to_k=drawn['to_k'])
            for label, t_melt in (('273', bl.FREEZING_K), ('paper_end', drawn['end_k'])):
                melt = float(np.interp(t_melt, t, ice))              # the ice branch at the thawing temperature
                warm = bl.branch_temperatures(melt, t, water, ice)['water']
                entry[f'lab_melt_au_{label}'] = float(sun.distance_au(melt))
                entry[f'lab_to_k_{label}'] = warm[0] if warm else math.nan
            snow[str(a)] = entry
        freeze = paper['ocean_freeze']
        out[_name(f)] = dict(ocean=ocean, snowballs=snow, ocean_freeze=dict(
            paper_au=freeze['arrow_au'], paper_end_k=freeze['end_k'],
            lab_au_273=float(sun.distance_au(np.interp(bl.FREEZING_K, t, water))),
            lab_au_paper_end=float(sun.distance_au(np.interp(freeze['end_k'], t, water)))))
    return out


EVIDENCE = ("A comparison of the lab's calculation (its steam table and direct columns, the energy balance and the "
            "wind) with values read from the paper's figures; the agreement it records is a reproduction of the "
            "paper's results by another code, and validates neither against observation.")
PRODUCER_FILES = ('atmosphere/waterworlds/comparison.py', 'atmosphere/waterworlds/balance.py',
                  'atmosphere/waterworlds/maps.py', 'atmosphere/waterworlds/escape.py', 'atmosphere/waterworlds/body.py',
                  'atmosphere/waterworlds/steam.py', 'atmosphere/waterworlds/radiating.py',
                  'atmosphere/waterworlds/steam_optics.py', 'atmosphere/waterworlds/figures.py',
                  'atmosphere/radiative_convective/longwave.py', 'atmosphere/radiative_convective/thermodynamics.py',
                  'atmosphere/radiative_convective/spectroscopy.py', 'shared/constants.py', 'shared/constants.json')


def producer() -> dict:
    """The comparison's code and environment."""
    import platform
    import scipy
    root = Path(__file__).resolve().parents[2]
    return dict(module='atmosphere.waterworlds.comparison',
                sources={name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in PRODUCER_FILES},
                environment=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__))


def compare(table: dict, figures: dict, optics, *, red_temperature: float, sun_flux: float = SOLAR_CONSTANT,
            bands=so.BANDS) -> dict:
    """Every comparison."""
    ratio = implied_flux_ratio(figures['figure4'])
    sun = maps.Star('sun', 5772.0, sun_flux)
    stars = dict(sun=sun, ad_leonis=maps.Star('ad_leonis', red_temperature, ratio * sun_flux))
    return dict(schema=SCHEMA, evidence=EVIDENCE,
                stars=dict(sun=dict(temperature_k=5772.0, flux_1au_w_m2=sun_flux),
                           ad_leonis=dict(flux_ratio_from_figure_4=ratio, temperature_k=red_temperature,
                                          flux_1au_w_m2=ratio * sun_flux)),
                figure2=figure_2(figures['figure2'], optics, bands=bands),
                figure3=figure_3(figures['figure3'], table, sun),
                figure4=figure_4(figures['figure4'], table, stars), figure5=figure_5(figures['figure5'], table, sun))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--store', type=Path, required=True)
    parser.add_argument('--table', type=Path, required=True)
    parser.add_argument('--figures', type=Path, required=True, help="the paper's curves (figures.py's product)")
    parser.add_argument('--red-temperature', type=float, default=3400.0)
    args = parser.parse_args(argv)
    table_bytes, figures_bytes = args.table.read_bytes(), args.figures.read_bytes()
    table, figures = tb.read(args.table), fg.read(args.figures)
    optics = so.SteamOptics(cache=args.store / 'caches' / 'steam-optics')
    result = compare(table, figures, optics, red_temperature=args.red_temperature)
    inputs = dict(table_sha256=hashlib.sha256(table_bytes).hexdigest(),
                  figures_sha256=hashlib.sha256(figures_bytes).hexdigest(), optics_key=optics.key,
                  sun_flux_1au_w_m2=SOLAR_CONSTANT, red_temperature_k=args.red_temperature, producer=producer())
    result.update(inputs=inputs)
    k = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()
    out = args.store / 'products' / 'steam-comparison' / k[:16] / 'comparison.json'
    print(out, fg.write(out, result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
