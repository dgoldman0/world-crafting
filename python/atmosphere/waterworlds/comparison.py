"""Stage 9's comparison of the lab's steam worlds with the paper's Figures 2 to 5 (Arnscheidt, Wordsworth and Ding 2019).

The paper's curves come from figures.py's product; the lab's from the steam columns' table (steam_table), from
columns computed directly at Figure 2's 0.12 Earth masses, which lies beyond the table's gravities, and from the
energy balance and the wind. Each comparison sets the lab's value beside the paper's at the same abscissa, the paper's
interpolated linearly along its curve and NaN beyond it; the wind's sound speed takes the factors named, 1 for the
paper's equations as printed, 1.2722 for the paper's transition, 4/3 for Figure 3's lifetimes and 1.42, the upper
end of the factors the paper's figures need (notes/waterworlds.md). The paper's AD Leonis takes the flux its Figure 4
implies, from the distances of the two stars' 273 K contours, which carries the paper's own ratio of the two stars'
absorbing factors, and the temperature given; the Sun gives 1,361 W/m^2 at 1 AU (shared/constants.json), a value the
paper leaves unstated. `acceptance` applies stage 9's acceptance check to a comparison (lab/design/plan.md).

    python -m atmosphere.waterworlds.comparison --store STORE --table TABLE.json --figures FIGURES.json

writes the comparison to STORE/products/steam-comparison/<key>/comparison.json, NaN as null, the key covering the
table's and the figures' files, the optics' key, the Sun's flux, the red star's temperature and the producer: the
code of every module the comparison runs and the versions of Python, numpy and scipy. Its optics take the table's
lines and continuum, and a table whose optics' key differs from theirs is refused.
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

SCHEMA = 'world-crafting.waterworlds.steam-comparison/3'
BILLION_YEARS = 1e9 * es.YEAR_S
FACTORS = (1.0, 1.2722, 4 / 3, 1.42)
GANYMEDE_KG = 1.4819e23
# Stage 9's acceptance check: the tolerances, the uncertainties of reading the figures and of the lab's numerics
# (notes/waterworlds.md), the fitted factor, the factors at the ends of the escape's spread, and where the radiation
# sets the values, at 2.3 m/s^2 up to 450 K and in the contours from 1.6 m/s^2 up.
TOLERANCES = dict(instellation=0.03, distance=0.015, factor=0.015)
READING = 0.001
NUMERICAL = 0.001
FITTED = 4 / 3
ESCAPE_ENDS = (1.2722, 1.42)
RADIATION_TO_K = 450.0
RADIATION_FROM_G = 1.6


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


def _finite(v) -> bool:
    return v is not None and math.isfinite(float(v))


def _differences(points, tolerance: float) -> dict:
    """A row of (label, lab, paper) points held to a tolerance on lab/paper - 1. A point the paper leaves out is left
    out; a lab value missing where the paper has one is listed and fails the row."""
    found, missing = [], []
    for label, lab, paper in points:
        if not _finite(paper):
            continue
        if not _finite(lab):
            missing.append(label)
            continue
        found.append((abs(float(lab) / float(paper) - 1), label))
    worst, at = max(found) if found else (math.nan, None)
    return dict(worst=worst, at=at, tolerance=tolerance, reading=READING, numerical=NUMERICAL, points=len(found),
                missing=missing, passes=bool(found) and not missing and worst <= tolerance)


def _outside(paper, ends, widen: float = 0.0) -> float:
    """How far the paper's value lies outside the lab's values at the escape's two ends, as a share of the nearer end,
    the bracket widened by `widen` of each end: 0 within it."""
    lo, hi = sorted(float(e) for e in ends)
    lo, hi, paper = lo * (1 - widen), hi * (1 + widen), float(paper)
    return (lo - paper) / lo if paper < lo else (paper - hi) / hi if paper > hi else 0.0


def _bracket(points) -> dict:
    """A row of (label, paper, ends, widen) points, each paper value held between the lab's at the escape's two ends.
    The row passes on the bracket itself; the bracket widened by the radiation's tolerance, for the curves that carry
    the radiation as well, is reported beside it, with the point nearest an end."""
    found, missing = [], []
    for label, paper, ends, widen in points:
        if not _finite(paper):
            continue
        if not all(_finite(e) for e in ends):
            missing.append(label)
            continue
        lo, hi = sorted(float(e) for e in ends)
        margin = min(float(paper) - lo, hi - float(paper)) / (lo if float(paper) - lo < hi - float(paper) else hi)
        found.append(dict(label=label, outside=_outside(paper, ends), widened=_outside(paper, ends, widen),
                          margin=margin))
    nearest = min(found, key=lambda p: p['margin']) if found else None
    return dict(ends=list(ESCAPE_ENDS), points=len(found), missing=missing,
                outside=[p['label'] for p in found if p['outside'] > 0],
                worst=max((p['outside'] for p in found), default=math.nan),
                outside_widened=[p['label'] for p in found if p['widened'] > 0],
                nearest=None if nearest is None else dict(label=nearest['label'], margin=nearest['margin']),
                passes=bool(found) and not missing and all(p['outside'] == 0 for p in found))


def _widest(rows, factor: str, side: str):
    """The widest zone, freezing contour less 10^9-year contour, over a star's rows at one factor, the lab's or the
    paper's."""
    widths = [r[f'{side}_freezing'] - r[f'{side}_billion'] for r in rows if _name(r['factor']) == factor
              and _finite(r[f'{side}_freezing']) and _finite(r[f'{side}_billion'])]
    return max(widths) if widths else math.nan


def acceptance(result: dict) -> dict:
    """Stage 9's acceptance check on a comparison (lab/design/plan.md, notes/waterworlds.md).

    Where the radiation sets the values, the lab at the fitted factor is held to the tolerances: Figure 3's
    instellation up to RADIATION_TO_K; the distances of the Sun's 273 K contour and of both stars' 10^9-year contours
    from RADIATION_FROM_G up, and of Figure 5's arrows; and each factor of Figure 2. AD Leonis's 273 K contour, to
    whose distances its flux is fitted, is reported apart. The values the escape sets are held to the spread of the
    factors the paper's figures need, each lying between the lab's at ESCAPE_ENDS: the lifetimes' temperatures, the
    transition, the temperature from which Figure 5's waters are short-lived, Figure 3's curves above RADIATION_TO_K,
    Figure 4's contours below RADIATION_FROM_G, the coldest snowball's thawed ocean, and the widest zones. Each value
    the escape sets is also compared by the printed equations, as the finding."""
    fit, ends = _name(FITTED), [_name(f) for f in ESCAPE_ENDS]
    f3, f4, f5 = result['figure3'], result['figure4'], result['figure5']
    kinds = ('expanding', 'no_expansion')
    instellation = [(f'Figure 3, {k}, {r["t_s"]:.0f} K', r[f'lab_{k}_{fit}'], r[f'paper_{k}']) for r in f3['rows']
                    if r['t_s'] <= RADIATION_TO_K for k in kinds]
    distance, calibrated = [], []
    for star in ('sun', 'ad_leonis'):
        for r in f4[star]['rows']:
            if _name(r['factor']) == fit and r['g'] >= RADIATION_FROM_G - 1e-9:
                (calibrated if star == 'ad_leonis' else distance).append(
                    (f'Figure 4, {star}, 273 K, {r["g"]:.1f} m/s2', r['lab_freezing'], r['paper_freezing']))
                distance.append((f'Figure 4, {star}, 10^9 years, {r["g"]:.1f} m/s2', r['lab_billion'],
                                 r['paper_billion']))
    distance += [(f'Figure 5, snowball {a}', s['lab_melt_au_paper_end'], s['paper_melt_au'])
                 for a, s in f5[fit]['snowballs'].items()]
    distance.append(('Figure 5, the ocean freezing', f5[fit]['ocean_freeze']['lab_au_paper_end'],
                     f5[fit]['ocean_freeze']['paper_au']))
    factors = [(f'Figure 2, {k}, {r["t_s"]:.0f} K', r[f'lab_{k}'], r[f'paper_{k}']) for r in result['figure2']['rows']
               for k in ('emitting', 'absorbing')]

    def escape(lab_ends):
        """The values the escape sets, (label, paper, the lab's at `lab_ends`, widening)."""
        points = [(f'Figure 3, 10^{label[2:]}-year lifetime', v['paper'], [v[f'lab_{e}'] for e in lab_ends], 0.0)
                  for label, v in f3['lifetimes_k'].items()]
        points.append(('Figure 4, the transition', f4['transition']['paper'],
                       [f4['transition'][f'lab_{e}'] for e in lab_ends], 0.0))
        short = f5['short_lived_from_k']
        points.append(('Figure 5, short-lived from', short['paper'], [short[f'lab_{e}'] for e in lab_ends], 0.0))
        points += [(f'Figure 3, {k}, {r["t_s"]:.0f} K', r[f'paper_{k}'], [r[f'lab_{k}_{e}'] for e in lab_ends],
                    TOLERANCES['instellation']) for r in f3['rows'] if r['t_s'] > RADIATION_TO_K for k in kinds]
        for star in ('sun', 'ad_leonis'):
            by_g = {}
            for r in f4[star]['rows']:
                if r['g'] < RADIATION_FROM_G - 1e-9:
                    by_g.setdefault(r['g'], {})[_name(r['factor'])] = r
            points += [(f'Figure 4, {star}, {name}, {g:.1f} m/s2', rows[lab_ends[0]][f'paper_{c}'],
                        [rows[e][f'lab_{c}'] for e in lab_ends], TOLERANCES['distance'])
                       for g, rows in sorted(by_g.items()) for c, name in (('freezing', '273 K'),
                                                                            ('billion', '10^9 years'))]
            points.append((f'Figure 4, {star}, widest zone', _widest(f4[star]['rows'], lab_ends[0], 'paper'),
                           [_widest(f4[star]['rows'], e, 'lab') for e in lab_ends], 0.0))
        cold = {e: f5[e]['snowballs']['0.4'] for e in lab_ends}
        points.append(('Figure 5, the coldest snowball thawed', cold[lab_ends[0]]['paper_to_k'],
                       [cold[e]['lab_to_k_paper_end'] for e in lab_ends], 0.0))
        return points

    rows = dict(instellation=_differences(instellation, TOLERANCES['instellation']),
                distance=_differences(distance, TOLERANCES['distance']),
                factor=_differences(factors, TOLERANCES['factor']),
                escape=_bracket(escape(ends)))
    printed = _bracket(escape([_name(1.0), _name(1.0)]))
    widest = {star: dict(paper=_widest(f4[star]['rows'], fit, 'paper'),
                         **{f'lab_{_name(f)}': _widest(f4[star]['rows'], _name(f), 'lab') for f in FACTORS})
              for star in ('sun', 'ad_leonis')}
    return dict(fitted=FITTED, rows=rows, calibrated=_differences(calibrated, TOLERANCES['distance']),
                printed=printed, widest=widest, passes=all(r['passes'] for r in rows.values()))

EVIDENCE = ("A comparison of the lab's calculation (its steam table and direct columns, the energy balance and the "
            "wind) with values read from the paper's figures; the agreement it records is a reproduction of the "
            "paper's results by another code, and validates neither against observation.")
PRODUCER_FILES = ('atmosphere/waterworlds/comparison.py', 'atmosphere/waterworlds/balance.py',
                  'atmosphere/waterworlds/maps.py', 'atmosphere/waterworlds/escape.py', 'atmosphere/waterworlds/body.py',
                  'atmosphere/waterworlds/steam.py', 'atmosphere/waterworlds/radiating.py',
                  'atmosphere/waterworlds/steam_optics.py', 'atmosphere/waterworlds/hitemp.py',
                  'atmosphere/waterworlds/figures.py',
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
    result = dict(schema=SCHEMA, evidence=EVIDENCE,
                  stars=dict(sun=dict(temperature_k=5772.0, flux_1au_w_m2=sun_flux),
                             ad_leonis=dict(flux_ratio_from_figure_4=ratio, temperature_k=red_temperature,
                                            flux_1au_w_m2=ratio * sun_flux)),
                  figure2=figure_2(figures['figure2'], optics, bands=bands),
                  figure3=figure_3(figures['figure3'], table, sun),
                  figure4=figure_4(figures['figure4'], table, stars), figure5=figure_5(figures['figure5'], table, sun))
    return dict(result, acceptance=acceptance(result))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--store', type=Path, required=True)
    parser.add_argument('--table', type=Path, required=True)
    parser.add_argument('--figures', type=Path, required=True, help="the paper's curves (figures.py's product)")
    parser.add_argument('--red-temperature', type=float, default=3400.0)
    args = parser.parse_args(argv)
    table_bytes, table = args.table.read_bytes(), tb.read(args.table)
    record = table['optics']
    optics = so.SteamOptics(cache=args.store / 'caches' / 'steam-optics', lines=record.get('source', 'hitran'),
                            hold=record.get('hold', False), store=args.store)
    if optics.key != record['key']:
        raise SystemExit(f"the optics' key {optics.key} differs from the table's, {record['key']}")
    figures_bytes, figures = args.figures.read_bytes(), fg.read(args.figures)
    result = compare(table, figures, optics, red_temperature=args.red_temperature)
    inputs = dict(table_sha256=hashlib.sha256(table_bytes).hexdigest(),
                  figures_sha256=hashlib.sha256(figures_bytes).hexdigest(), optics_key=optics.key,
                  sun_flux_1au_w_m2=SOLAR_CONSTANT, red_temperature_k=args.red_temperature, producer=producer())
    result.update(inputs=inputs)
    k = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()
    out = args.store / 'products' / 'steam-comparison' / k[:16] / 'comparison.json'
    print(out, fg.write(out, result))
    print(json.dumps(result['acceptance'], indent=1, default=float))
    return 0


if __name__ == '__main__':
    sys.exit(main())
