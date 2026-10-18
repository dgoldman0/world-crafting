"""The wind scan behind the time-step guard's record, with its file reader replaced (the reader itself is tested in
the lab's environment, lab/tests/test_exoplasim.py)."""
import pytest

from worldlab import winds


def _runs(tmp_path, winds_by_run, namelists=True):
    for run, years in winds_by_run.items():
        model = tmp_path / run / 'model'
        model.mkdir(parents=True)
        if namelists:
            (model / 'plasim_namelist').write_text(' MPSTEP  =  30.0\n NSTPW  =  143\n')
            (model / 'planet_namelist').write_text(' PLARAD = 1737459.9949772405\n')
        for year in years:
            (model / f'MOST.{year:05d}.nc').write_bytes(b'')


def _reader(winds_by_run, latitudes=32):
    return lambda path: (winds_by_run[path.parts[-3]][int(path.stem.split('.')[1])], latitudes)


def test_the_scan_keeps_each_runs_largest_year_and_its_settings(tmp_path, monkeypatch):
    found = {'a': {0: 10.0, 1: 30.0, 2: 20.0}, 'b': {0: 25.0, 3: 20.0}}
    _runs(tmp_path, found)
    monkeypatch.setattr(winds, 'largest_wind_m_s', _reader(found))
    record = winds.record(tmp_path, 'test:runs')
    assert record['files'] == 5 and record['source'] == 'test:runs/*/model/MOST.*.nc'
    assert record['runs']['a'] == dict(m_s=30.0, model_year=1, latitudes=32, truncation=21, timestep_min=30.0,
                                       radius_m=1737459.9949772405)
    assert record['runs']['b']['model_year'] == 0


def test_the_scan_refuses_runs_it_cannot_place(tmp_path, monkeypatch):
    found = {'a': {0: 10.0}}
    _runs(tmp_path / 'bare', found, namelists=False)
    monkeypatch.setattr(winds, 'largest_wind_m_s', _reader(found))
    with pytest.raises(ValueError, match='no MPSTEP'):
        winds.scan(tmp_path / 'bare')
    _runs(tmp_path / 'odd', found)
    monkeypatch.setattr(winds, 'largest_wind_m_s', _reader(found, latitudes=40))
    with pytest.raises(ValueError, match="no grid of ExoPlaSim's"):
        winds.scan(tmp_path / 'odd')
