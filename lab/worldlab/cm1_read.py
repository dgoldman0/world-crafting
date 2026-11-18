"""A reader of a CM1 box's run, enough to read the coupling test: its domain means through the run, by local time, and
the record the damped gravity wave writes (patch 10 of the lab's CM1 series, lab_lsw_means.txt).

CM1's domain diagnostics (dodomaindiag) write, every diagfrq seconds, one file cm1out_diag_NNNNNN_s.dat of domain means
at the scalar levels, described by the GrADS control file cm1out_diag_s.ctl: each variable a float in the machine's
order for a single value, or one for each of its levels, the variables one after another in the control file's order,
`mtime` (s) first. The local hour angle of a time t is var18 + 360 t / var19 (core patch 05), the box's start hour
and solar day. The job wrapper's record (run.json in the run's folder) gives the model time a run has reached.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np

DIAG_CTL = 'cm1out_diag_s.ctl'
DIAG_FILES = 'cm1out_diag_[0-9][0-9][0-9][0-9][0-9][0-9]_s.dat'
DIAG_NUMBER = re.compile(r'^cm1out_diag_(\d{6})_s\.dat$')         # file k holds time (k - 1) diagfrq
LSW_RECORD = 'lab_lsw_means.txt'
RUN_RECORD = 'run.json'
QUARTERS = (('morning', -90.0, 0.0), ('afternoon', 0.0, 90.0), ('evening', 90.0, 180.0), ('night', -180.0, -90.0))


def reached_s(run: Path) -> float | None:
    """The model time (s) a run has reached by its record, or None for a run without one."""
    path = Path(run) / RUN_RECORD
    if not path.is_file():
        return None
    segments = json.loads(path.read_text()).get('segments', [])
    return float(segments[-1]['end_s']) if segments else 0.0


def diag_files(run: Path) -> list[Path]:
    return sorted(Path(run).glob(DIAG_FILES))


def control(path: Path) -> dict:
    """A GrADS control file's levels (zdef, km) and variables, each with its count of levels (0 for one value)."""
    text = Path(path).read_text()
    zdef = re.search(r'^zdef\s+(\d+)\s+levels\s*(.*?)^(?:tdef|vars)', text, flags=re.M | re.S | re.I)
    levels = [float(x) for x in zdef.group(2).split()] if zdef else []
    body = re.search(r'^vars\s+(\d+)\s*$(.*?)^endvars', text, flags=re.M | re.S | re.I)
    if body is None:
        raise ValueError(f'{path}: no vars ... endvars block')
    names = []
    for line in body.group(2).strip().splitlines():
        parts = line.split()
        names.append((parts[0], int(parts[1])))
    if len(names) != int(body.group(1)):
        raise ValueError(f'{path}: {body.group(1)} variables stated, {len(names)} found')
    return dict(z_km=levels, variables=names)


def domain_means(run: Path, names=('mtime', 'prate', 'th', 'qv', 'u', 'v', 'hpbl', 'pwat')) -> dict:
    """The run's domain means by output time: each named variable, a series (times) or (times, levels), with the
    scalar levels' heights (m)."""
    run = Path(run)
    ctl = control(run / DIAG_CTL)
    sizes = [(name, max(n, 1)) for name, n in ctl['variables']]
    offsets, at = {}, 0
    for name, n in sizes:
        offsets[name] = (at, n)
        at += n
    missing = [n for n in names if n not in offsets]
    if missing:
        raise ValueError(f'{run / DIAG_CTL} holds no {missing}')
    out = {n: [] for n in names}
    for path in diag_files(run):
        data = np.fromfile(path, dtype='<f4')
        if data.size != at:
            raise ValueError(f'{path} holds {data.size} values, where its control file states {at}')
        for n in names:
            start, count = offsets[n]
            out[n].append(data[start] if count == 1 else data[start:start + count])
    result = {n: np.asarray(v, float) for n, v in out.items()}
    result['z_m'] = np.asarray(ctl['z_km'], float) * 1000.0
    return result


CLOCK_FILES = ('namelist.template', 'namelist.input')   # the case's namelist, which every segment's takes its clock from


def clock_file(run: Path) -> Path:
    """The namelist a run's clock is read from: the case's template, which stays as the case wrote it, or the namelist
    CM1 read where a run holds no template."""
    for name in CLOCK_FILES:
        if (Path(run) / name).is_file():
            return Path(run) / name
    raise ValueError(f'{run} holds no namelist')


def run_clock(run: Path) -> dict:
    """The box's start hour (var18, degrees) and solar day (var19, s), from its namelist (`clock_file`)."""
    text = clock_file(run).read_text()
    get = lambda name: float(re.search(rf'^\s*{name}\s*=\s*([^,\s]+)', text, flags=re.M).group(1))
    return dict(start_hour_deg=get('var18'), solar_day_s=get('var19'))


def hour_angle(t_s, clock: dict):
    """The local hour angle (degrees, from -180) at model times t_s."""
    return (clock['start_hour_deg'] + 360.0 * np.asarray(t_s, float) / clock['solar_day_s'] + 180.0) % 360.0 - 180.0


def window(means: dict, clock: dict, solar_days) -> np.ndarray:
    """The output times within solar days (first, last] of the run."""
    t = means['mtime']
    first, last = (float(d) * clock['solar_day_s'] for d in solar_days)
    keep = (t > first + 1e-6) & (t <= last + 1e-6)
    if not keep.any():
        raise ValueError(f'the run holds no output within solar days {list(solar_days)}')
    return keep


def domain_mean_by_hour(run: Path, solar_days, *, bins: int = 36, source: str | None = None) -> dict:
    """The run's domain-mean potential temperature (K) and vapour mixing ratio (kg/kg) by local time over solar days
    (first, last], each output taken into the bin of local time nearest its hour: the column series gcm_site's
    reference_column takes for a box measured against another box's own mean (the test of self-consistency of Edman and
    Romps 2015). Every bin holds outputs, or the series is refused."""
    means = domain_means(run)
    clock = run_clock(run)
    keep = window(means, clock, solar_days)
    centres = (np.arange(bins) + 0.5) * 360.0 / bins - 180.0
    hours = hour_angle(means['mtime'][keep], clock)
    nearest = np.argmin(np.abs((hours[:, None] - centres[None, :] + 180.0) % 360.0 - 180.0), axis=1)
    counts = np.bincount(nearest, minlength=bins)
    if (counts == 0).any():
        raise ValueError(f'{int((counts == 0).sum())} of {bins} bins of local time hold no output over solar days '
                         f'{list(solar_days)}')
    th, qv = means['th'][keep], means['qv'][keep]
    theta = np.array([th[nearest == b].mean(axis=0) for b in range(bins)])
    vapour = np.array([qv[nearest == b].mean(axis=0) for b in range(bins)])
    return dict(hour_angle_deg=centres.tolist(), z_m=means['z_m'].tolist(), theta_k=theta.tolist(),
                qv_kg_kg=vapour.tolist(), outputs_per_bin=counts.tolist(),
                source=source or f"{Path(run).name}'s domain mean by local time over solar days {list(solar_days)}")


def lsw_record(run: Path) -> list[dict]:
    """The damped gravity wave's record: for each interval, its start and end (s), its steps, the coupled layer's mean
    base (m) and, at each level, zh and zf (m), the wind at zf (m/s), the inflow's theta (K/s) and vapour (kg/kg/s)
    tendencies and the table's heating (K/s) and moistening (kg/kg/s) as applied, each the interval's mean."""
    path = Path(run) / LSW_RECORD
    if not path.is_file():
        return []
    words = path.read_text().split()
    out, i = [], 0
    names = ('zh_m', 'zf_m', 'w_m_s', 'inflow_theta_k_s', 'inflow_qv_kg_kg_s', 'table_theta_k_s', 'table_qv_kg_kg_s')
    while i < len(words):
        t0, t1, n, base, nk = float(words[i]), float(words[i + 1]), int(float(words[i + 2])), float(words[i + 3]), \
            int(float(words[i + 4]))
        i += 5
        rows = np.asarray(words[i:i + 7 * nk], float).reshape(nk, 7)
        i += 7 * nk
        out.append(dict(start_s=t0, end_s=t1, steps=n, base_m=base, **{k: rows[:, j] for j, k in enumerate(names)}))
    return out


def lsw_cut(text: str, end_s: float) -> int:
    """Where the wave's record is cut so that it holds the intervals ending by end_s alone: the start of the line on
    which the first later interval begins, or the text's length. The record's bytes before it stay as CM1 wrote them."""
    words = list(re.finditer(r'\S+', text))
    i = 0
    while i + 5 <= len(words):
        if float(words[i + 1].group()) > end_s + 1e-3:
            return text.rfind('\n', 0, words[i].start()) + 1
        i += 5 + 7 * int(float(words[i + 4].group()))
    return len(text)


def summary(run: Path, solar_days) -> dict:
    """What the coupling test reads of one box over solar days (first, last]: its domain-mean rain (mm/day) over the
    days and by quarter of local time from sunrise, and, under the damped gravity wave, the mean of its own
    large-scale vertical wind by level over the intervals within the days, with the coupled layer's mean base."""
    means = domain_means(run)
    clock = run_clock(run)
    keep = window(means, clock, solar_days)
    rain = means['prate'][keep] * 86400.0
    hours = hour_angle(means['mtime'][keep], clock)
    quarters = {name: float(rain[(hours >= lo) & (hours < hi)].mean()) if ((hours >= lo) & (hours < hi)).any() else None
                for name, lo, hi in QUARTERS}
    out = dict(run=Path(run).name, solar_days=list(solar_days), outputs=int(keep.sum()),
               rain_mm_day=float(rain.mean()), rain_by_quarter_mm_day=quarters)
    first, last = (float(d) * clock['solar_day_s'] for d in solar_days)
    intervals = [r for r in lsw_record(run) if r['start_s'] >= first - 1e-6 and r['end_s'] <= last + 1e-6]
    if intervals:
        weights = np.array([r['end_s'] - r['start_s'] for r in intervals])
        w = np.average(np.array([r['w_m_s'] for r in intervals]), axis=0, weights=weights)
        out['lsw'] = dict(intervals=len(intervals), zf_m=intervals[0]['zf_m'].tolist(), w_m_s=w.tolist(),
                          base_m=float(np.average([r['base_m'] for r in intervals], weights=weights)))
    return out
