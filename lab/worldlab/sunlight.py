"""The star's light at the top of a world's air: its spectrum, the filter a scenario sets in its path, the total that
reaches the air, and the near-infrared weights PlaSim's ice clouds take from it (lab/design/world_spec.md, the
derived quantities "Sunlight at the top" and "Ice-optics weights").

A star's spectrum is a pinned measured or model spectrum, or a blackbody at the star's temperature. Past a pinned
spectrum's ends the star's blackbody supplies the shape, at the level the spectrum's light gives it within 2% of
each end's wavelength, from where hc/(λkT) = 50 to 1 mm, wherever the spectrum leaves room. `star.spectrum_form` says
what the file holds:

- `irradiance`: the star's irradiance at 1 AU, as TSIS-1 measures the Sun's. The measured values stand, and the
  rest of the star's stated constant, the constant less the spectrum's own light, fills the tails.
- `shape`: a spectrum of the right shape in any units, as a model atmosphere gives it. The spectrum and its
  tails are scaled together to the constant.

A scenario's filter multiplies the spectrum by a transmission, read linearly between its points and held at its
end values beyond them, and the light is integrated on the union of the spectrum's points and the filter's. The
functions on arrays are pure; `sunlight` reads the world's and scenario's pins through the manifest.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .data import DataError, Manifest, parse_pin
from .spec import SpecError

C2_NM_K = 6.62607015e-34 * 299792458.0 / 1.380649e-23 * 1e9   # hc/k, the second radiation constant, nm K
TAIL_POINTS = 100_001                 # on a geometric grid, each tail's own
SHORT_X = 50.0                        # the short tail starts where hc/(λkT) = 50, e^-50 of the blackbody's scale
LONG_END_NM = 1.0e6                   # the long tail ends at 1 mm, past which a 5772 K star holds 8e-10 of its light
MATCH_SHARE = 0.02                    # the light within 2% of each end's wavelength sets that tail's level
NEGLIGIBLE = 1e-9                     # a remainder this small against the constant counts as none
ICE_BAND_EDGES_NM = (750.0, 1e7 / 7700.0, 1e7 / 5300.0, 1e7 / 4000.0)   # Ebert and Curry's four bands from PlaSim's
                                      # 0.75 µm; the fourth runs from 2.5 µm to the spectrum's end
FORMS = ('irradiance', 'shape')
TARGET_SCALE = 'to-reference-temperature'


@dataclass(frozen=True)
class Spectrum:
    """A spectral irradiance, W m⁻² nm⁻¹, on increasing wavelengths in nm."""
    wavelength_nm: np.ndarray
    irradiance: np.ndarray

    def total(self) -> float:
        return float(np.trapezoid(self.irradiance, self.wavelength_nm))

    def light(self, lo: float, hi: float) -> float:
        """The light between two of the spectrum's own wavelengths."""
        inside = (self.wavelength_nm >= lo) & (self.wavelength_nm <= hi)
        return float(np.trapezoid(self.irradiance[inside], self.wavelength_nm[inside]))


@dataclass(frozen=True)
class Filter:
    """A transmission between 0 and 1 on increasing wavelengths in nm."""
    wavelength_nm: np.ndarray
    transmission: np.ndarray


# The star.

def planck_shape(wavelength_nm, temperature_k: float) -> np.ndarray:
    """A blackbody's spectral radiance per unit wavelength at `temperature_k`, to a constant factor:
    λ⁻⁵ e^(−x)/(1 − e^(−x)) with x = hc/(λkT), a form that holds where e^x overflows."""
    w = np.asarray(wavelength_nm, dtype=float)
    x = C2_NM_K / (w * temperature_k)
    return w ** -5.0 * np.exp(-x) / -np.expm1(-x)


def blackbody(temperature_k: float, constant_w_m2: float) -> Spectrum:
    """A blackbody star's spectrum, from where hc/(λkT) = 50 to 1 mm, scaled to `constant_w_m2`."""
    w = np.geomspace(C2_NM_K / (SHORT_X * temperature_k), LONG_END_NM, 2 * TAIL_POINTS - 1)
    shape = planck_shape(w, temperature_k)
    return Spectrum(w, shape * (constant_w_m2 / np.trapezoid(shape, w)))


def _level(w, f, temperature_k: float, lo: float, hi: float) -> float:
    """The blackbody's level that gives the spectrum's own light between `lo` and `hi`."""
    inside = (w >= lo) & (w <= hi)
    model = np.trapezoid(planck_shape(w[inside], temperature_k), w[inside])
    return float(np.trapezoid(f[inside], w[inside]) / model) if model > 0.0 else 0.0


def extended(measured: Spectrum, temperature_k: float, constant_w_m2: float, form: str = 'irradiance') -> Spectrum:
    """A pinned spectrum with the star's blackbody past each end where it leaves room, its light set by `form`
    (the module's docstring) so that the whole holds `constant_w_m2`."""
    if form not in FORMS:
        raise SpecError(f'star.spectrum_form is one of {FORMS}, where the world states {form!r}')
    w, f = measured.wavelength_nm, measured.irradiance
    own = float(np.trapezoid(f, w))
    if not own > 0.0:
        raise DataError('a spectrum file with no light in it')
    start = C2_NM_K / (SHORT_X * temperature_k)
    short = np.geomspace(start, w[0], TAIL_POINTS)[:-1] if w[0] > start else np.empty(0)
    long = np.geomspace(w[-1], LONG_END_NM, TAIL_POINTS)[1:] if w[-1] < LONG_END_NM else np.empty(0)
    # Each window spans at least the spectrum's outermost interval, so that a coarse spectrum gives its tails light.
    short_level = _level(w, f, temperature_k, w[0], max(w[0] * (1.0 + MATCH_SHARE), w[1]))
    long_level = _level(w, f, temperature_k, min(w[-1] * (1.0 - MATCH_SHARE), w[-2]), w[-1])
    short_f, long_f = short_level * planck_shape(short, temperature_k), long_level * planck_shape(long, temperature_k)
    # The whole holds own + edges + k * tails for tails at k times their matched level: the intervals between each
    # tail and the measured end share a part that follows k and a part that follows the measured end alone.
    tails, edges = 0.0, 0.0
    if len(short):
        tails += float(np.trapezoid(short_f, short)) + short_f[-1] * (w[0] - short[-1]) / 2.0
        edges += f[0] * (w[0] - short[-1]) / 2.0
    if len(long):
        tails += float(np.trapezoid(long_f, long)) + long_f[0] * (long[0] - w[-1]) / 2.0
        edges += f[-1] * (long[0] - w[-1]) / 2.0
    if form == 'shape':
        scale = constant_w_m2 / (own + edges + tails)
        return Spectrum(np.concatenate([short, w, long]), scale * np.concatenate([short_f, f, long_f]))
    rest = constant_w_m2 - own - edges
    if rest < -NEGLIGIBLE * constant_w_m2:
        raise DataError(f'the spectrum holds {own + edges:.6g} W/m², more than the star\'s stated constant of '
                        f'{constant_w_m2:.6g}; a spectrum in other units is a `shape`')
    if tails > 0.0:
        k = max(rest, 0.0) / tails
    elif rest > NEGLIGIBLE * constant_w_m2:
        raise DataError(f'the spectrum spans every wavelength and holds {own:.6g} W/m², short of the star\'s '
                        f'stated constant of {constant_w_m2:.6g}')
    else:
        k = 0.0
    return Spectrum(np.concatenate([short, w, long]), np.concatenate([k * short_f, f, k * long_f]))


def star_spectrum(world: dict, *, manifest: Manifest | None = None,
                  store: Path | None = None) -> tuple[Spectrum, tuple | None]:
    """The world's star's spectrum at 1 AU, and the range of its pinned spectrum, None for a blackbody."""
    star, where = world.get('star', {}), f'{world.get("id", "the world")}: star'
    temperature = _positive(star.get('temperature_k'), f'{where}.temperature_k')
    constant = _positive(star.get('constant_w_m2'), f'{where}.constant_w_m2')
    value = star.get('spectrum')
    if value == 'blackbody':
        return blackbody(temperature, constant), None
    if not isinstance(value, str) or value in ('unchosen', 'model-default', 'none'):
        raise SpecError(f'{where}.spectrum is a pinned spectrum or blackbody, where the world states {value!r}')
    pin = parse_pin(value)
    if pin.entry is not None:
        raise SpecError(f'{where}.spectrum: a spectrum file takes no # entry, where the world names {pin.entry!r}')
    measured = read_spectrum_csv((manifest or Manifest()).path(pin, store=store))
    whole = extended(measured, temperature, constant, star.get('spectrum_form'))
    return whole, (float(measured.wavelength_nm[0]), float(measured.wavelength_nm[-1]))


def read_spectrum_csv(path: Path) -> Spectrum:
    """A spectrum file of comma-separated rows, wavelength in nm and irradiance in W m⁻² nm⁻¹, below one header
    row; further columns are left aside."""
    try:
        rows = np.loadtxt(path, delimiter=',', skiprows=1, usecols=(0, 1), ndmin=2)
    except (OSError, ValueError) as error:
        raise DataError(f'{path}: {error}') from None
    w, f = rows[:, 0], rows[:, 1]
    if len(w) < 2 or not np.all(np.diff(w) > 0) or not w[0] > 0:
        raise DataError(f'{path}: wavelengths rise from above 0 nm, at two points or more')
    if not np.all(np.isfinite(f)) or np.any(f < 0):
        raise DataError(f'{path}: irradiance is finite and positive or zero')
    return Spectrum(w.astype(float), f.astype(float))


# The filter.

def read_transmission_json(path: Path, entry: str) -> Filter:
    """A transmission file of JSON, its `wavelength_nm` list and its `transmission` table of lists by entry, as
    Terluna's protection domain writes them."""
    try:
        product = json.loads(Path(path).read_text())
        w, table = np.asarray(product['wavelength_nm'], dtype=float), product['transmission']
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise DataError(f'{path}: {error!r}, where a transmission file holds wavelength_nm and transmission') from None
    if entry not in table:
        raise DataError(f'{path}: no entry {entry!r} among {sorted(table)}')
    t = np.asarray(table[entry], dtype=float)
    if t.shape != w.shape or len(w) < 2 or not np.all(np.diff(w) > 0):
        raise DataError(f'{path}#{entry}: one transmission for each of two or more rising wavelengths')
    if not np.all((t >= 0.0) & (t <= 1.0)):
        raise DataError(f'{path}#{entry}: transmissions lie between 0 and 1')
    return Filter(w, t)


def scenario_filter(scenario: dict, *, manifest: Manifest | None = None, store: Path | None = None) -> Filter | None:
    """The scenario's filter: None for `none`, otherwise its pinned transmission."""
    value, where = scenario.get('sunlight', {}).get('filter'), f'{scenario.get("id", "the scenario")}: sunlight.filter'
    if value == 'none':
        return None
    if not isinstance(value, str) or value in ('unchosen', 'model-default'):
        raise SpecError(f'{where} is a pinned transmission or none, where the scenario states {value!r}')
    pin = parse_pin(value)
    if pin.entry is None:
        raise SpecError(f"{where} names its file's entry with #, as {pin.name}#<entry>")
    return read_transmission_json((manifest or Manifest()).path(pin, store=store), pin.entry)


# What reaches the air.

def through(spectrum: Spectrum, filt: Filter | None, extra_nm=()) -> Spectrum:
    """The light the filter passes, on the union of the spectrum's points, the filter's points within its range and
    `extra_nm`: the spectrum read linearly between its points, the filter between its own and held beyond them."""
    w = spectrum.wavelength_nm
    pieces = [w, np.asarray(extra_nm, dtype=float)]
    if filt is not None:
        pieces.append(filt.wavelength_nm)
    points = np.concatenate(pieces)
    grid = np.unique(points[(points >= w[0]) & (points <= w[-1])])
    light = np.interp(grid, w, spectrum.irradiance)
    if filt is not None:
        light = light * np.interp(grid, filt.wavelength_nm, filt.transmission)
    return Spectrum(grid, light)


def band_shares(spectrum: Spectrum, edges_nm, filt: Filter | None = None) -> tuple[float, ...]:
    """Each band's share of the passed light from the first edge on, the last band running to the spectrum's end."""
    edges = [float(e) for e in edges_nm]
    light = through(spectrum, filt, edges)
    bounds = edges + [float(light.wavelength_nm[-1])]
    parts = [light.light(lo, hi) for lo, hi in zip(bounds[:-1], bounds[1:])]
    whole = sum(parts)
    if not whole > 0.0:
        raise SpecError(f'no light passes from {edges[0]} nm on')
    return tuple(p / whole for p in parts)


def sunlight(world: dict, scenario: dict, *, manifest: Manifest | None = None, store: Path | None = None) -> dict:
    """The sunlight at the top of the air at the orbit's semi-major axis, W m⁻²: the star's total there, with the
    light its pinned spectrum measures and its tails hold; what the filter passes, and the part of it beyond the
    filter's own range, where its end values hold; the filter's share; and the filtered light times the scenario's
    scale where the scale is a number. Beside them, the ice-optics weights of the filtered light and of the
    unfiltered star."""
    where = world.get('id', 'the world')
    distance = _positive(world.get('orbit', {}).get('semi_major_axis_au'), f'{where}: orbit.semi_major_axis_au')
    spectrum, measured_range = star_spectrum(world, manifest=manifest, store=store)
    filt = scenario_filter(scenario, manifest=manifest, store=store)
    dilution = 1.0 / distance ** 2
    passed = through(spectrum, filt)
    record = dict(star_w_m2=spectrum.total() * dilution, filtered_w_m2=passed.total() * dilution)
    if measured_range is not None:
        lo, hi = measured_range
        first, last = spectrum.wavelength_nm[0], spectrum.wavelength_nm[-1]
        record.update(measured_w_m2=spectrum.light(lo, hi) * dilution,
                      short_tail_w_m2=spectrum.light(first, lo) * dilution,
                      long_tail_w_m2=spectrum.light(hi, last) * dilution)
    if filt is not None:
        first, last = passed.wavelength_nm[0], passed.wavelength_nm[-1]
        f_lo, f_hi = float(filt.wavelength_nm[0]), float(filt.wavelength_nm[-1])
        held = (passed.light(first, f_lo) if f_lo > first else 0.0) + (passed.light(f_hi, last) if f_hi < last else 0.0)
        record['held_w_m2'] = held * dilution
    record['filter_share'] = record['filtered_w_m2'] / record['star_w_m2']
    scale = scenario.get('sunlight', {}).get('scale')
    record['scale'] = scale
    if scale != TARGET_SCALE:
        if isinstance(scale, bool) or not isinstance(scale, (int, float)) or not math.isfinite(scale) or not scale > 0:
            raise SpecError(f'{scenario.get("id")}: sunlight.scale is a positive number or {TARGET_SCALE!r}, where '
                            f'the scenario states {scale!r}')
        record['top_w_m2'] = record['filtered_w_m2'] * scale
    record['ice_weights'] = band_shares(spectrum, ICE_BAND_EDGES_NM, filt)
    record['ice_weights_unfiltered'] = band_shares(spectrum, ICE_BAND_EDGES_NM)
    return record


def _positive(value, where: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not value > 0:
        raise SpecError(f'{where} is a positive number, where the specification states {value!r}')
    return float(value)
