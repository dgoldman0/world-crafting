"""How PlaSim's year files hold their means, and the humidity's means to read from them (defect log A10).

A run writes one netCDF file a model year (MOST.<year>.nc). In low-I/O mode (NLOWIO 1) PlaSim adds each output field
to its mean at every step and writes the means at the end of each interval of NSTPW steps (outmod.f90: outaccu, outgp
and outsp). The temperature, the surface pressure, the winds, the cloud, the precipitable water and the fluxes are
true means, and the gridpoint diagnostics (codes 21-41) are single steps at each interval's end.

The specific humidity is a held value. With spectral humidity (NQSPEC 1) the field PlaSim adds for code 133, sqout,
is recomputed at output steps alone (plasim.f90, `if (mod(nstep,nafter)==0 .and. nqspec == 1)`), so each record of
hus holds the humidity at the end of the interval before it, carried through the interval. sqout is also absent from
the restart, so each year file's first record holds what the few steps before the first recompute added, about 2% of
the vapour in Terluna's runs. The rule here takes each interval's mean as the average of the humidity at its start
and at its end, the record and the next. A year file's first record, which holds that remnant, and its last, whose end
lies in the next file, have no such mean, so a reader takes records 1 to n-2 of every field, and a file of fewer than
three records gives none. A run that writes the humidity's true mean (hus_mean, code 233, Terluna's switch nhusmean,
the second half of ExoPlaSim's port 9 in PLAN.md) keeps every record.

Brought from Terluna's climate/gcm/year_files.py at 39c5ee04 (python/provenance.json): the rule and the functions
are Terluna's, and the refusal of a file of fewer than three records is the lab's.

Over the fifteen-level baseline's second year in Terluna, the rule brings the column's vapour within 5.7 kg/m2 of the
precipitable water's means (rms over cells and records) against 10.4 for the records themselves, with no bias, and
from 14.2 to 8.2 kg/m2 in the Kuo run (Terluna's climate/gcm/README.md at 39c5ee04, "The humidity in the year
files"). Those are Terluna's measurements on its runs; the lab's tests check the rule on files built to carry the
fault (climate/tests/test_year_files.py).
"""
from __future__ import annotations

import numpy as np

HUS_MEAN = 'hus_mean'         # code 233: the gridpoint humidity PlaSim accumulates every step (aadq), as a mean


def records(d) -> slice:
    """The records of a year file (an open netCDF4 dataset) whose humidity means are known: every record where the run
    writes hus_mean, otherwise the second to the second-last."""
    return slice(None) if HUS_MEAN in d.variables else slice(1, -1)


def interval_means(hus) -> np.ndarray:
    """Interval means of specific humidity from records that each hold the humidity at their interval's start (time
    first): the average of each record and the next, for records 1 to n-2. Three records or more give one mean or
    more; fewer are refused."""
    hus = np.asarray(hus, float)
    if hus.ndim < 1 or hus.shape[0] < 3:
        raise ValueError('the humidity held at each interval\'s start gives interval means from three records or more, '
                         f'where the file holds {hus.shape[0] if hus.ndim else 0}')
    return 0.5 * (hus[1:-1] + hus[2:])


def humidity(d) -> np.ndarray:
    """Means of specific humidity (kg/kg) over the records records(d) of a year file, (time, lev, lat, lon)."""
    if HUS_MEAN in d.variables:
        return np.asarray(d[HUS_MEAN][:], float)
    return interval_means(d['hus'][:])


def fields(d, names) -> dict:
    """The named fields of a year file over records(d), each a float array with time first; 'hus' is the humidity's
    means (humidity), and fields without a time axis come whole."""
    keep = records(d)
    timed = [name for name in names if d[name].dimensions and d[name].dimensions[0] == 'time']
    if keep != slice(None) and timed and d[timed[0]].shape[0] < 3:
        raise ValueError(f'a year file of {d[timed[0]].shape[0]} records holds no interval whose humidity mean is '
                         'known; the rule takes records 1 to n-2')
    out = {}
    for name in names:
        if name == 'hus':
            out[name] = humidity(d)
        elif d[name].dimensions and d[name].dimensions[0] == 'time':
            out[name] = np.asarray(d[name][:], float)[keep]
        else:
            out[name] = np.asarray(d[name][:], float)
    return out
