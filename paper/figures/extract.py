"""Extract the numbers the paper's figures and tables use into paper/data/, each file naming its sources and their hashes.

    python3 paper/figures/extract.py                 # from the repository root

Sources: the committed products under python/ (copied from Terluna at 186b294), Terluna's own checkout at the same
commit for the CRM heat budgets, and the GCM runs' progress records on Terluna's research drive. A missing source stops
the extraction with its name; nothing is substituted.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'paper' / 'data'
PY = ROOT / 'python'
TERLUNA = Path('/home/kir/Documents/Projects/terluna')
RUNS = Path('/media/projectspace/terluna-research/gcm-runs')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name: str, about: str, sources: list[Path], body: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    rec = dict(about=about, sources=[dict(path=str(p), sha256=sha(p)) for p in sources], **body)
    (DATA / f'{name}.json').write_text(json.dumps(rec, indent=1) + '\n')
    print('wrote', (DATA / f'{name}.json').relative_to(ROOT))


def sun_clock() -> None:
    paths = [PY / 'climate/results/gcm' / f'sun_check_{r}.json' for r in ('A28_dim5', 'A28_dim5_sun_test')]
    runs = {}
    for p in paths:
        d = json.loads(p.read_text())
        row = d['along_row']
        runs[d['run']] = dict(years=d['years'], clock=d['model_day']['sun_clock'], lat_deg=row['lat_deg'],
                              lon_deg=row['lon_deg'], relative=row['relative'], solang_relative=row['solang_relative'],
                              relative_range=row['relative_range'], correlation_with_solang=row['correlation_with_solang'],
                              sweep_deg=d['model_day']['sun_sweep_deg'], skip_back_deg=d['model_day']['skip_back_deg'],
                              orbit_used=d['orbit']['used'])
    write('sun_clock', "Equatorial sunlight at the top of the air by longitude over its row's mean: PlaSim's own Sun clock "
          '(A28_dim5, years 15-24) and the synodic clock (A28_dim5_sun_test, years 0-1); solang_relative is the same from '
          "PlaSim's solar-position arithmetic alone (sun_check.py)", paths, dict(runs=runs))


def slant() -> None:
    p = PY / 'climate/results/gcm/twilight.json'
    d = json.loads(p.read_text())
    s = d['column']['slant']
    write('slant', 'Slant-path factor (absorber path over the vertical path) against solar elevation for the design column: '
          "the Moon's well-mixed air and its water from the curved-air ledger, PlaSim's Earth formula 35/sqrt(1+1224 mu^2), and "
          'the flat 1/mu; the rational fits the GCM patches carry', [p],
          dict(elevation_deg=s['elevation_deg'], moon_air=s['air'], moon_water=s['water'], plasim=s['plasim'], flat=s['flat'],
               fit_water=d['magnification'], fit_air=d['magnification_air'],
               mass_mean_height_km=d['column']['mass_mean_height_km'], column_mass_kg_m2=d['column']['mass_kg_m2']))


def layers() -> None:
    p = TERLUNA / 'climate/gcm/README.md'
    lines = p.read_text().splitlines()
    head = next(i for i, l in enumerate(lines) if l.startswith('| GCM layer | Line-by-line | PlaSim as run | PlaSim with the bands |'))
    rows = []
    for l in lines[head + 2:]:
        if not l.startswith('|'):
            break
        cells = [c.strip() for c in l.strip('|').split('|')]
        rows.append(dict(layer=cells[0], line_by_line=float(cells[1]), as_run=float(cells[2]), with_bands=float(cells[3])))
    write('layers', "The design column's absorbed sunlight by GCM layer, global means in W/m2: the line-by-line pseudo-spherical "
          "column against PlaSim's arithmetic on the same column as run and with the CO2 and O2 bands (Terluna "
          f'climate/gcm/README.md lines {head + 1}-{head + 2 + len(rows)} at 186b294)', [p], dict(rows=rows))


def run_mean(run: str, years: range) -> tuple[float, int]:
    p = RUNS / run / 'progress.json'
    entries = {e['year']: e for e in json.loads(p.read_text())['years']}
    vals = [entries[y]['surface_k'] for y in years]
    return sum(vals) / len(vals), len(vals)


REPAIRS = [  # (label, kind, baseline run, its years, test run, its years, note)
    ('Cloud water counted in pressure terms', 'repair', 'A', range(30, 40), 'A_earth_path_clouds', range(10, 15),
     'settles near 298.0 K'),
    ('Convective cover per Earth day', 'repair', 'A_earth_path_clouds', range(10, 15), 'A_corrected_clouds', range(10, 15),
     'settles near 299.6 K'),
    ("The Sun's clock, the Moon's tilt and the sunlight split", 'repair', 'A28_dim5', range(15, 25), 'A28_dim5_moon', range(20, 30), ''),
    ('Curved air: twilight, cone and slant path', 'repair', 'A28_dim5_moon', range(20, 30), 'A28_dim5_moon_geometry', range(10, 20), ''),
    ('CO2 and O2 in the sunlight', 'repair', 'A28_dim5_moon_geometry', range(10, 20), 'A28_dim5_moon_geometry_gases', range(10, 20),
     'still cooling 0.3 K a decade'),
    ('Longwave by height with ice optics', 'test', 'A28_corrected_970', range(10, 20), 'A28_corrected_970_lw_ice', range(10, 20),
     'extrapolates to balance at 306.8-307.1 K; a sensitivity test, off in the design case'),
    ('Cloud water at the full-column bound', 'bracket', 'A', range(30, 40), 'A_full_column_clouds', range(10, 15), 'settles near 292.0 K'),
    ('Thinner convective cloud', 'cloud setting', 'A28_dim5_moon', range(20, 30), 'A28_dim5_moon_thin_convective', range(5, 15),
     'settles near 297.1 K'),
    ('More low cloud', 'cloud setting', 'A28_dim5_moon', range(20, 30), 'A28_dim5_moon_low_cloud', range(5, 15), 'settles near 289.0 K'),
]


def repairs() -> None:
    rows, paths = [], set()
    for label, kind, base, by, test, ty, note in REPAIRS:
        b, nb = run_mean(base, by)
        t, nt = run_mean(test, ty)
        paths |= {RUNS / base / 'progress.json', RUNS / test / 'progress.json'}
        rows.append(dict(label=label, kind=kind, baseline=dict(run=base, years=[by[0], by[-1]], surface_k=round(b, 3), n=nb),
                         test=dict(run=test, years=[ty[0], ty[-1]], surface_k=round(t, 3), n=nt),
                         change_k=round(t - b, 3), note=note))
    write('repairs', "Global-mean surface temperature of each test run against its baseline over the README's stated years, "
          "from the runs' yearly summaries (progress.json); repairs in the design case, and sensitivity tests: the "
          "longwave correction with ice optics, the cloud-water bracket's upper bound, and two of PlaSim's Earth-tuned cloud "
          "settings", sorted(paths), dict(rows=rows))


def gap45n() -> None:
    paths = [TERLUNA / 'climate/results/crm' / f'heat_budget_ring_45n_corrected{s}.json' for s in ('', '_sideways')]
    out = {}
    for p in paths:
        d = json.loads(p.read_text())
        out[d['case']] = [dict(km=L['km'], ring_c=L['ring_temperature_c'], gcm_c=L['gcm_temperature_c']) for L in d['layers']]
    write('gap45n', "Layer-mean air temperature over the 45 N ring's second lunar day in CM1, without and with the GCM's sideways "
          "heat and vapour imposed, against the GCM design case's row (A28_corrected_970, years 10-19)", paths, dict(cases=out))


# Worlds for the regime map: the basis is stated per world; each value is a calculation from it.
R_GAS = 8.314462618
WORLDS = [  # name, kind, g (m/s2), radius (km), surface pressure (bar), temperature (K), molar mass (g/mol), solar day (Earth days), basis
    ('Earth', 'found', 9.80665, 6371.0, 1.01325, 288.0, 28.97, 1.0, 'global means'),
    ('Mars', 'found', 3.721, 3389.5, 0.0061, 210.0, 43.34, 1.0275, 'present atmosphere, global means'),
    ('Titan', 'found', 1.352, 2574.7, 1.467, 93.7, 28.0, 15.945, 'surface values (Huygens)'),
    ('Venus', 'found', 8.87, 6051.8, 92.0, 737.0, 43.45, 116.75, 'surface values'),
    ('Open Moon 1.2 atm', 'crafted', 1.6242, 1737.4, 1.2159, 295.0, 28.83, 29.53, "Terluna's design case at the water level"),
    ('Open Moon 1.0 atm', 'crafted', 1.6242, 1737.4, 1.01325, 295.0, 28.83, 29.53, "Terluna's pressure variant"),
    ('Mars at 1 bar', 'crafted', 3.721, 3389.5, 1.0, 288.0, 28.97, 1.0275, 'an illustrative breathable Mars, Earth-like air'),
    ('Slow rotator, 16 d', 'illustrative', 9.80665, 6371.0, 1.01325, 288.0, 28.97, 16.0, 'Earth with a 16-day solar day'),
    ('Slow rotator, 64 d', 'illustrative', 9.80665, 6371.0, 1.01325, 288.0, 28.97, 64.0, 'Earth with a 64-day solar day'),
    ('Slow rotator, 243 d', 'illustrative', 9.80665, 6371.0, 1.01325, 288.0, 28.97, 243.0, 'Earth with a 243-day solar day'),
]


def worlds() -> None:
    rows = []
    for name, kind, g, r_km, p_bar, t, m, day, basis in WORLDS:
        h_km = R_GAS * t / (m * 1e-3 * g) / 1000.0
        rows.append(dict(name=name, kind=kind, g_m_s2=g, radius_km=r_km, surface_pressure_bar=p_bar, temperature_k=t,
                         molar_mass_g_mol=m, solar_day_days=day, basis=basis, scale_height_km=round(h_km, 2),
                         h_over_r=round(h_km / r_km, 5), column_mass_t_m2=round(p_bar * 1e5 / g / 1000.0, 3),
                         column_mass_over_earth=round((p_bar * 1e5 / g) / (101325.0 / 9.80665), 3),
                         chapman_horizon=round(math.sqrt(math.pi * r_km / (2.0 * h_km)), 1),
                         convective_cover_bias=round(0.125 * math.log(max(day, 1.0)), 3)))
    write('worlds', 'Governing ratios of found and crafted worlds, calculated from the stated basis: scale height RT/(Mg) at the '
          'surface temperature, H/R, column mass p/g, the Chapman horizon air mass sqrt(pi R / 2H) for an isothermal '
          "atmosphere, and the bias PlaSim's convective cover formula takes when it counts rain per solar day, "
          '0.125 ln(day / 1 d)', [], dict(rows=rows))


if __name__ == '__main__':
    for missing in [p for p in (TERLUNA, RUNS) if not p.exists()]:
        raise SystemExit(f'missing source: {missing}')
    sun_clock(); slant(); layers(); repairs(); gap45n(); worlds()
