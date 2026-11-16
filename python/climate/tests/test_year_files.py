"""The humidity's means read from PlaSim's year files by the rule of defect A10: on stand-ins of an open year file, as
Terluna's tests have them, and on a netCDF file written to carry the fault, whose humidity each record holds at its
interval's start and whose first record holds the remnant a restart leaves.

Brought from Terluna's climate/tests/test_year_files.py at 39c5ee04 (python/provenance.json): its three tests are
kept, and the tests of a short file and of the written files are the lab's."""
import math

import numpy as np
import pytest

from climate.gcm import year_files as yf

# netCDF4 sets the shape of the arrays it is given to write, which numpy 2.5 deprecates; the warning comes from its code.
pytestmark = pytest.mark.filterwarnings('ignore:Setting the shape on a NumPy array:DeprecationWarning')


class Var:
    def __init__(self, data, dimensions):
        self.data, self.dimensions = np.asarray(data, float), dimensions
        self.shape = self.data.shape

    def __getitem__(self, index):
        return self.data[index]


class YearFile:
    """A stand-in for an open year file: its variables by name, each with its dimensions."""

    def __init__(self, **variables):
        self.variables = variables

    def __getitem__(self, name):
        return self.variables[name]


def year_file(with_mean=False, n=6):
    start = np.arange(n, dtype=float)[:, None] * 1e-3 + 1e-2      # the humidity at each interval's start, (time, lev)
    start[0] = 2e-4                                                # the restart's empty first record
    variables = dict(hus=Var(start, ('time', 'lev')), ta=Var(np.arange(n)[:, None] + 270.0, ('time', 'lev')),
                     lev=Var([0.5], ('lev',)))
    if with_mean:
        variables[yf.HUS_MEAN] = Var(start + 5e-4, ('time', 'lev'))
    return YearFile(**variables), start


def test_humidity_means_average_each_record_with_the_next():
    d, start = year_file()
    assert yf.records(d) == slice(1, -1)
    got = yf.humidity(d)
    assert got.shape == (4, 1)
    assert np.allclose(got[:, 0], 0.5 * (start[1:-1, 0] + start[2:, 0]))
    assert np.allclose(yf.interval_means(start), got)


def test_fields_take_the_same_records():
    d, start = year_file()
    f = yf.fields(d, ('hus', 'ta', 'lev'))
    assert f['ta'].shape == f['hus'].shape == (4, 1)
    assert np.allclose(f['ta'][:, 0], np.arange(1, 5) + 270.0)     # records 1 to n-2
    assert np.allclose(f['lev'], [0.5])                             # no time axis: whole


def test_a_run_that_writes_the_mean_keeps_every_record():
    d, start = year_file(with_mean=True)
    assert yf.records(d) == slice(None)
    f = yf.fields(d, ('hus', 'ta'))
    assert f['hus'].shape == f['ta'].shape == (6, 1)
    assert np.allclose(f['hus'], start + 5e-4)


def test_a_file_of_fewer_than_three_records_gives_no_mean():
    d, _ = year_file(n=2)
    with pytest.raises(ValueError, match='three records'):
        yf.interval_means(d['hus'].data)
    with pytest.raises(ValueError, match='records 1 to n-2'):
        yf.fields(d, ('ta', 'hus'))
    d, _ = year_file(with_mean=True, n=2)                           # the true mean keeps both records
    assert yf.fields(d, ('ta', 'hus'))['hus'].shape == (2, 1)


# A year file written to carry the fault. A level's humidity follows q(t) = q0 + b cos(2 pi t / P) through a day of
# period P, and the file's records are means over intervals of P/10, the temperature a true mean and the humidity the
# value at each interval's start, as PlaSim writes them in low-I/O mode with spectral humidity; the first record holds
# 2% of the vapour, the remnant a call's first steps leave. The true interval mean of the cosine is the cosine at the
# interval's centre times sin(x)/x, x = pi/10; the rule's average of the starts at the interval's two ends is the
# cosine at the centre times cos(x).

Q0, B, PERIOD, INTERVALS = 0.012, 0.004, 10, 23


def _written(path, with_mean=False):
    netCDF4 = pytest.importorskip('netCDF4')
    x = math.pi / PERIOD
    centre = 2.0 * x * (np.arange(INTERVALS) + 0.5)                  # phase at each interval's centre
    start = Q0 + B * np.cos(centre - x)                             # the humidity at each interval's start
    start[0] = 0.02 * Q0
    mean = Q0 + B * np.cos(centre) * math.sin(x) / x                # the true interval means
    with netCDF4.Dataset(path, 'w') as d:
        d.createDimension('time', None)
        d.createDimension('lev', 1)
        d.createVariable('lev', 'f4', ('lev',))[:] = [0.9]
        d.createVariable('time', 'f8', ('time',))[:] = np.arange(INTERVALS) + 1.0
        d.createVariable('hus', 'f8', ('time', 'lev'))[:, 0] = start
        d.createVariable('ta', 'f8', ('time', 'lev'))[:, 0] = 280.0 + 3.0 * np.cos(centre)
        if with_mean:
            d.createVariable(yf.HUS_MEAN, 'f8', ('time', 'lev'))[:, 0] = mean
    return centre, start, mean


def test_on_a_written_file_the_rule_centres_the_humidity_where_the_records_lag_half_an_interval(tmp_path):
    import netCDF4
    path = tmp_path / 'MOST.00000.nc'
    centre, start, mean = _written(path)
    with netCDF4.Dataset(path) as d:
        f = yf.fields(d, ('hus', 'ta'))
    x = math.pi / PERIOD
    kept = centre[1:-1]
    assert f['hus'].shape == f['ta'].shape == (INTERVALS - 2, 1)
    assert np.allclose(f['ta'][:, 0], 280.0 + 3.0 * np.cos(kept))           # the true means, aligned with hus
    # The rule: the cosine at each interval's centre, damped by cos(x) where the true mean is damped by sin(x)/x.
    assert np.allclose(f['hus'][:, 0], Q0 + B * np.cos(kept) * math.cos(x), rtol=0, atol=1e-15)
    assert np.abs(f['hus'][:, 0] - mean[1:-1]).max() < B * (math.sin(x) / x - math.cos(x)) + 1e-15
    # The fault: the records read as means lag the centres by half an interval, 18 degrees of the day, so that their
    # error reaches about b sin(x), beside the rule's b (sin(x)/x - cos(x)): 0.31 b against 0.033 b.
    held = start[1:-1]
    assert np.allclose(held, Q0 + B * np.cos(kept - x), rtol=0, atol=1e-15)
    error_held, error_rule = np.abs(held - mean[1:-1]).max(), np.abs(f['hus'][:, 0] - mean[1:-1]).max()
    assert error_held > 0.3 * B and error_rule < 0.033 * B and error_held > 9.0 * error_rule
    fit = lambda q: np.linalg.lstsq(np.column_stack([np.ones_like(kept), np.cos(kept), np.sin(kept)]), q, rcond=None)[0]
    assert math.degrees(math.atan2(fit(held)[2], fit(held)[1])) == pytest.approx(18.0, abs=1e-9)
    assert abs(fit(f['hus'][:, 0])[2]) < 1e-14                              # the rule's phase is the centres'
    # The first record's remnant, 2% of the vapour, is left out with the last record.
    assert f['hus'].min() > Q0 - B


def test_on_a_written_file_the_true_mean_keeps_every_record(tmp_path):
    import netCDF4
    path = tmp_path / 'MOST.00000.nc'
    centre, start, mean = _written(path, with_mean=True)
    with netCDF4.Dataset(path) as d:
        f = yf.fields(d, ('hus', 'ta'))
    assert f['hus'].shape == (INTERVALS, 1) and np.array_equal(f['hus'][:, 0], mean)
