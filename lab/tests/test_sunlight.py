"""The star's light at the top of the air: blackbody and pinned spectra, filters, the total and the ice-optics
weights."""
import hashlib
import json
import math
import warnings

import numpy as np
import pytest
from scipy.integrate import quad

from worldlab import sunlight
from worldlab.data import DataError, Manifest
from worldlab.roots import root
from worldlab.spec import Library, SpecError

LIB = Library()
MOON, EARTH, MARS = (LIB.world(w) for w in ('moon', 'earth', 'mars'))
OPEN_MOON, CONTROL, MARS_AIR = (LIB.scenario(s) for s in ('moon/open-moon', 'earth/control', 'mars/breathable-1bar'))
STORE, DRIVE = root('store'), root('terluna-drive')
needs_store = pytest.mark.skipif(STORE is None, reason='the store is unset (lab/local.example.toml)')
needs_drive = pytest.mark.skipif(DRIVE is None, reason="Terluna's research drive is unset (lab/local.example.toml)")
PATCH_10 = (0.6164, 0.2283, 0.0811, 0.0742)        # Terluna's ice-optics weights, to the four places patch 10 holds
EDGES = sunlight.ICE_BAND_EDGES_NM


def _planck_band(lo_nm, hi_nm, temperature_k):
    """The blackbody's light between two wavelengths, by quadrature on a logarithmic variable."""
    value, _ = quad(lambda u: math.exp(u) * float(sunlight.planck_shape(math.exp(u), temperature_k)), math.log(lo_nm),
                    math.log(hi_nm), limit=200, epsabs=0.0, epsrel=1e-11)
    return value


def _world(**star):
    return {**MOON, 'star': {**MOON['star'], **star}}


def _scenario(filter_value, scale='to-reference-temperature'):
    return {**OPEN_MOON, 'sunlight': {'filter': filter_value, 'scale': scale}}


def _pinned(tmp_path, name, content: bytes):
    """A manifest of one entry `x` serving `content` as the file `name`, and a store holding it."""
    source, store = tmp_path / name, tmp_path / 'store'
    source.write_bytes(content)
    store.mkdir(exist_ok=True)
    (tmp_path / 'manifest.toml').write_text(
        'schema = "worldlab.manifest/0"\n[data.x]\ntitle = "t"\nuse = "u"\nlicence = "l"\ncredit = "c"\n'
        'reviewed = 2026-10-18\n[[data.x.files]]\n'
        f'name = "{name}"\nurl = "{source.as_uri()}"\nretrieved = 2026-10-18\nbytes = {len(content)}\n'
        f'sha256 = "{hashlib.sha256(content).hexdigest()}"\n')
    manifest = Manifest(tmp_path / 'manifest.toml')
    manifest.fetch(store=store, download=True, lab=tmp_path)
    return manifest, store


def _csv(w, f) -> bytes:
    return ('wavelength (nm),irradiance (W/m^2/nm)\n' + ''.join(f'{a!r},{b!r}\n' for a, b in zip(w, f))).encode()


def _sampled(lo, hi, step, temperature_k, total):
    """A blackbody sampled between two wavelengths, scaled so that its samples hold `total`."""
    w = np.arange(lo, hi + step / 2, step)
    f = sunlight.planck_shape(w, temperature_k)
    return sunlight.Spectrum(w, f * total / np.trapezoid(f, w))


# The blackbody.

def test_the_planck_shape_integrates_to_its_closed_form_and_peaks_by_wiens_law():
    for temperature in (2500.0, 5772.0, 40000.0):
        star = sunlight.blackbody(temperature, 1.0)
        raw = sunlight.planck_shape(star.wavelength_nm, temperature)
        closed = (temperature / sunlight.C2_NM_K) ** 4 * math.pi ** 4 / 15.0      # ∫ λ⁻⁵/(e^x − 1) dλ
        assert np.trapezoid(raw, star.wavelength_nm) == pytest.approx(closed, rel=1e-6)
        fine = np.linspace(0.9, 1.1, 20001) * 2.897771955e6 / temperature
        peak = fine[np.argmax(sunlight.planck_shape(fine, temperature))]
        assert peak == pytest.approx(2.897771955e6 / temperature, rel=1e-4)
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        assert sunlight.planck_shape(0.1, 3000.0) == 0.0                     # hc/(λkT) near 48,000, past e^x's range


def test_a_blackbody_star_holds_its_constant_and_its_bands():
    star = sunlight.blackbody(5772.0, 1361.0)
    assert star.total() == pytest.approx(1361.0, rel=1e-12)
    bounds = EDGES + (1e6,)
    bands = [_planck_band(lo, hi, 5772.0) for lo, hi in zip(bounds[:-1], bounds[1:])]
    assert sunlight.band_shares(star, EDGES) == pytest.approx(tuple(b / sum(bands) for b in bands), rel=1e-6)


# Pinned spectra and their tails.

def test_a_shape_sampled_from_a_blackbody_extends_to_that_blackbody():
    extended = sunlight.extended(_sampled(300.0, 2000.0, 0.5, 5772.0, 7.0), 5772.0, 1361.0, 'shape')
    reference = sunlight.blackbody(5772.0, 1361.0)
    assert extended.total() == pytest.approx(1361.0, rel=1e-12)
    inside = (reference.wavelength_nm > 300.0) & (reference.wavelength_nm < 2000.0)
    assert np.interp(reference.wavelength_nm[inside], extended.wavelength_nm, extended.irradiance) == pytest.approx(
        reference.irradiance[inside], rel=1e-5)
    assert sunlight.band_shares(extended, EDGES) == pytest.approx(sunlight.band_shares(reference, EDGES), rel=1e-6)


def test_each_tail_takes_the_level_of_the_light_within_two_percent_of_its_end():
    w = np.arange(400.0, 1000.0 + 0.05, 0.1)
    flat = sunlight.Spectrum(w, np.full_like(w, 2.0))
    extended = sunlight.extended(flat, 5772.0, 1361.0, 'shape')
    scale = extended.light(w[0], w[-1]) / flat.total()
    window = (w >= w[-1] * (1.0 - sunlight.MATCH_SHARE)) & (w <= w[-1])
    model = np.trapezoid(sunlight.planck_shape(w[window], 5772.0), w[window])
    level = np.trapezoid(flat.irradiance[window], w[window]) / model
    first = np.searchsorted(extended.wavelength_nm, w[-1]) + 1
    assert extended.irradiance[first] == pytest.approx(
        scale * level * sunlight.planck_shape(extended.wavelength_nm[first], 5772.0), rel=1e-12)


def test_an_irradiance_keeps_its_measured_values_and_fills_the_rest_of_the_constant():
    measured = _sampled(300.0, 2000.0, 0.5, 5772.0, 1100.0)
    extended = sunlight.extended(measured, 5772.0, 1361.0, 'irradiance')
    inside = (extended.wavelength_nm >= 300.0) & (extended.wavelength_nm <= 2000.0)
    assert np.array_equal(extended.irradiance[inside], measured.irradiance)
    assert extended.total() == pytest.approx(1361.0, rel=1e-12)
    assert extended.light(extended.wavelength_nm[0], 300.0) + extended.light(2000.0, extended.wavelength_nm[-1]) == (
        pytest.approx(1361.0 - 1100.0, rel=1e-9))


def test_a_coarse_spectrum_gives_its_tails_light():
    coarse = _sampled(300.0, 2000.0, 50.0, 5772.0, 1100.0)          # one sample within 2% of each end
    extended = sunlight.extended(coarse, 5772.0, 1361.0, 'irradiance')
    assert extended.light(extended.wavelength_nm[0], 300.0) > 0.0
    assert extended.total() == pytest.approx(1361.0, rel=1e-12)


def test_spectra_that_reach_past_the_tails_ends_take_no_tail_there():
    solar = _sampled(0.5, 3000.0, 0.5, 5772.0, 1300.0)        # from the X-ray side of the Sun, as SOLAR-ISS starts
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        extended = sunlight.extended(solar, 5772.0, 1361.0, 'irradiance')
        cool = sunlight.extended(_sampled(5.0, 3000.0, 0.5, 3000.0, 1.0), 3000.0, 1.0, 'shape')  # as PHOENIX
    assert extended.wavelength_nm[0] == 0.5 and extended.total() == pytest.approx(1361.0, rel=1e-12)
    assert np.all(np.isfinite(extended.irradiance)) and cool.total() == pytest.approx(1.0, rel=1e-12)
    wide = sunlight.Spectrum(np.geomspace(1.0, 2e6, 50001), np.ones(50001))
    assert sunlight.extended(wide, 5772.0, wide.total(), 'irradiance').wavelength_nm[-1] == 2e6
    with pytest.raises(DataError, match='spans every wavelength'):
        sunlight.extended(wide, 5772.0, 2.0 * wide.total(), 'irradiance')


@pytest.mark.parametrize('total, form, error, message', [
    (1400.0, 'irradiance', DataError, 'more than the star'),
    (1000.0, 'counts', SpecError, 'spectrum_form is one of'),
])
def test_ill_formed_extensions_are_refused(total, form, error, message):
    with pytest.raises(error, match=message):
        sunlight.extended(_sampled(300.0, 2000.0, 0.5, 5772.0, total), 5772.0, 1361.0, form)


@pytest.mark.parametrize('star, message', [
    (dict(temperature_k=None), 'temperature_k is a positive number'),
    (dict(temperature_k=0.0), 'temperature_k is a positive number'),
    (dict(constant_w_m2=-1.0), 'constant_w_m2 is a positive number'),
    (dict(constant_w_m2=True), 'constant_w_m2 is a positive number'),
    (dict(spectrum=None), 'a pinned spectrum or blackbody'),
    (dict(spectrum='unchosen'), 'a pinned spectrum or blackbody'),
    (dict(spectrum='tsis1-hsrs-stride100#visible'), 'takes no # entry'),
])
def test_ill_formed_stars_are_refused(star, message):
    with pytest.raises(SpecError, match=message):
        sunlight.star_spectrum(_world(**star))


@pytest.mark.parametrize('rows, message', [
    ('w,f\n500,1\n400,1\n', 'rise'),
    ('w,f\n400,1\n500,-1\n', 'positive or zero'),
    ('w,f\n400,1\n', 'two points'),
    ('w,f\n400,x\n500,1\n', 'could not convert'),
])
def test_ill_formed_spectrum_files_are_refused(tmp_path, rows, message):
    path = tmp_path / 's.csv'
    path.write_text(rows)
    with pytest.raises(DataError, match=message):
        sunlight.read_spectrum_csv(path)


def test_a_spectrum_file_with_no_light_is_refused():
    with pytest.raises(DataError, match='no light'):
        sunlight.extended(sunlight.Spectrum(np.array([400.0, 500.0]), np.zeros(2)), 5772.0, 1361.0)


# Filters.

def test_a_filter_reads_linearly_holds_its_ends_and_counts_the_light_it_holds(tmp_path):
    product = {'wavelength_nm': [400.0, 600.0, 800.0], 'transmission': {'half': [0.2, 0.6, 1.0]}}
    manifest, store = _pinned(tmp_path, 'shield.json', json.dumps(product).encode())
    filt = sunlight.scenario_filter(_scenario('x#half'), manifest=manifest, store=store)
    flat = sunlight.Spectrum(np.array([300.0, 500.0, 700.0, 900.0]), np.ones(4))
    passed = sunlight.through(flat, filt)
    assert list(passed.wavelength_nm) == [300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    assert list(passed.irradiance) == pytest.approx([0.2, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0])
    assert sunlight.scenario_filter(_scenario('none')) is None
    with pytest.raises(SpecError, match='entry with #'):
        sunlight.scenario_filter(_scenario('x'), manifest=manifest, store=store)
    with pytest.raises(DataError, match='no entry'):
        sunlight.scenario_filter(_scenario('x#full'), manifest=manifest, store=store)
    for value in (None, 'unchosen'):
        with pytest.raises(SpecError, match='a pinned transmission or none'):
            sunlight.scenario_filter(_scenario(value))


def test_a_coarse_spectrum_sees_a_fine_filter_between_its_points():
    flat = sunlight.Spectrum(np.arange(400.0, 800.0 + 1.0, 20.0), np.ones(21))
    notch = sunlight.Filter(np.array([400.0, 509.0, 510.0, 520.0, 521.0, 800.0]),
                            np.array([1.0, 1.0, 0.0, 0.0, 1.0, 1.0]))
    assert sunlight.through(flat, notch).total() == pytest.approx(400.0 - 11.0, rel=1e-12)   # the notch, 11 nm wide


def test_the_band_shares_weigh_the_light_the_filter_passes():
    star = sunlight.blackbody(5772.0, 1361.0)
    blocks_first = sunlight.Filter(np.array([100.0, 1298.0, 1299.0, 1e7]), np.array([0.0, 0.0, 1.0, 1.0]))
    shares = sunlight.band_shares(star, EDGES, blocks_first)
    assert shares[0] < 1e-3 and sum(shares[1:]) == pytest.approx(1.0, abs=1e-3)


@pytest.mark.parametrize('product, message', [
    ({'wavelength_nm': [400.0, 600.0], 'transmission': {'a': [0.2, 1.2]}}, 'between 0 and 1'),
    ({'wavelength_nm': [600.0, 400.0], 'transmission': {'a': [0.2, 0.4]}}, 'rising wavelengths'),
    ({'wavelength_nm': [400.0, 600.0], 'transmission': {'a': [0.2]}}, 'rising wavelengths'),
    ({'transmission': {'a': [0.2]}}, 'holds wavelength_nm'),
])
def test_ill_formed_filters_are_refused(tmp_path, product, message):
    path = tmp_path / 'f.json'
    path.write_text(json.dumps(product))
    with pytest.raises(DataError, match=message):
        sunlight.read_transmission_json(path, 'a')


# The record.

def test_a_blackbody_world_reaches_its_air_at_its_distance_through_its_filter(tmp_path):
    product = {'wavelength_nm': [10.0, 1e7], 'transmission': {'grey': [0.5, 0.5]}}     # past both ends of the star
    manifest, store = _pinned(tmp_path, 'grey.json', json.dumps(product).encode())
    far = {**_world(spectrum='blackbody', temperature_k=4000.0), 'orbit': {**MOON['orbit'], 'semi_major_axis_au': 2.0}}
    record = sunlight.sunlight(far, _scenario('x#grey', scale=0.8), manifest=manifest, store=store)
    assert record['star_w_m2'] == pytest.approx(1361.0 / 4.0, rel=1e-12) and 'measured_w_m2' not in record
    assert record['filter_share'] == pytest.approx(0.5, rel=1e-12) and record['held_w_m2'] == 0.0
    assert record['top_w_m2'] == pytest.approx(1361.0 / 4.0 * 0.5 * 0.8, rel=1e-12)
    assert record['ice_weights'] == pytest.approx(record['ice_weights_unfiltered'], rel=1e-12)
    for scale in (0.0, -1.0, True, '1.0', 'unchosen'):
        with pytest.raises(SpecError, match='sunlight.scale is a positive number'):
            sunlight.sunlight(far, _scenario('x#grey', scale=scale), manifest=manifest, store=store)
    for orbit in ({'semi_major_axis_au': -1.0}, {'semi_major_axis_au': None}):
        with pytest.raises(SpecError, match='semi_major_axis_au'):
            sunlight.sunlight({**far, 'orbit': {**far['orbit'], **orbit}}, _scenario('none'))


# The seeds' worlds, from the store. Values marked as pins are this code's output on 2026-10-18, held to catch change.

@needs_store
def test_the_moon_earth_and_mars_take_the_suns_light():
    moon = sunlight.sunlight(MOON, OPEN_MOON)
    measured = sunlight.read_spectrum_csv(Manifest().path('tsis1-hsrs-stride100')).total()
    assert moon['star_w_m2'] == pytest.approx(1361.0, rel=1e-12) and 'top_w_m2' not in moon   # its scale is a stage's
    assert moon['measured_w_m2'] == pytest.approx(measured, rel=1e-12)
    assert moon['short_tail_w_m2'] + moon['long_tail_w_m2'] == pytest.approx(1361.0 - measured, rel=1e-9)
    assert moon['filtered_w_m2'] == pytest.approx(1236.12, abs=0.005)                          # a pin
    assert moon['held_w_m2'] == pytest.approx(6.21, abs=0.005)                                 # a pin
    assert moon['ice_weights'] == pytest.approx((0.6295, 0.2276, 0.0752, 0.0677), abs=1e-4)    # a pin
    assert sunlight.sunlight(EARTH, CONTROL)['top_w_m2'] == pytest.approx(1361.0, rel=1e-12)
    assert sunlight.sunlight(MARS, MARS_AIR)['top_w_m2'] == pytest.approx(1361.0 / 1.52366231 ** 2, rel=1e-12)


@needs_store
def test_terlunas_rule_on_the_same_spectrum_gives_patch_10s_weights():
    """Terluna's weights came from the whole TSIS-1 spectrum with the 5772 K blackbody matched at its last value
    past its end, nothing short of its start, and the whole scaled to the constant (python/atmosphere/
    radiative_convective/shortwave.py, solar_spectrum). That rule, on the lab's reading of the same file, gives patch
    10's constants to their four places; the lab's own rule, whose tails hold the rest of the constant, gives
    0.0685 for the fourth band, where Terluna's tail held 11% more light than the rest."""
    measured = sunlight.read_spectrum_csv(Manifest().path('tsis1-hsrs-stride100'))
    w, f = measured.wavelength_nm, measured.irradiance
    long = np.geomspace(w[-1], 1e6, sunlight.TAIL_POINTS)[1:]
    tail = f[-1] * sunlight.planck_shape(long, 5772.0) / sunlight.planck_shape(w[-1], 5772.0)
    terluna = sunlight.Spectrum(np.concatenate([w, long]), np.concatenate([f, tail]))
    assert sunlight.band_shares(terluna, EDGES) == pytest.approx(PATCH_10, abs=5e-5)
    fourth = sunlight.sunlight(MOON, OPEN_MOON)['ice_weights_unfiltered'][3]
    assert fourth == pytest.approx(0.0685, abs=1e-4)                                           # a pin


@needs_store
@needs_drive
def test_the_light_through_the_shield_agrees_with_terlunas_record_by_its_stated_cause():
    """Terluna's runner passed the measured light at the shield's transmission and the rest of the constant at the
    transmission of the spectrum's last wavelength, 2,730 nm (exoplasim_run.py:976-984). With that rule on the lab's
    reading of the same files the record comes back to 10⁻¹². The lab's figure differs by the rest of the constant
    passing at the shield's own transmission along each tail."""
    record = json.loads((DRIVE / 'gcm-runs' / 'A28_corrected_970' / 'progress.json').read_text())['inputs']
    spectrum, (lo, hi) = sunlight.star_spectrum(MOON)
    filt = sunlight.scenario_filter(OPEN_MOON)
    passed = sunlight.through(spectrum, filt)
    rest = 1361.0 - spectrum.light(lo, hi)
    at_end = float(np.interp(hi, filt.wavelength_nm, filt.transmission))
    terluna = passed.light(lo, hi) + rest * at_end
    assert terluna == pytest.approx(record['shield_flux_w_m2'], rel=1e-12)
    tails = passed.light(passed.wavelength_nm[0], lo) + passed.light(hi, passed.wavelength_nm[-1])
    lab = sunlight.sunlight(MOON, OPEN_MOON)['filtered_w_m2']
    assert lab == pytest.approx(terluna - rest * at_end + tails, rel=1e-12)
