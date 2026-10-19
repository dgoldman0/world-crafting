"""Curves read from the images of the paper's figures: the PDF image reader, the axes' calibration, the curves, the
product, and the readings of Arnscheidt, Wordsworth and Ding's Figures 2 to 5 where the paper's source is restored."""
import json
import math
import zlib

import numpy as np
import pytest

from atmosphere.waterworlds import fetch_inputs, figures as fg

needs_source = pytest.mark.skipif(fetch_inputs.restore()['status'] != 'PASS',
                                  reason="the paper's source is unrestored (atmosphere.waterworlds.fetch_inputs --download)")


def _pdf(img: np.ndarray, extra: bytes = b'', parms: bytes = b'', stream: bytes = None) -> bytes:
    h, w, _ = img.shape
    head = (f'9 0 obj\n<< /Length 10 0 R\n   /Filter /FlateDecode\n   /Type /XObject\n   /Subtype /Image\n'
            f'   /Width {w}\n   /Height {h}\n   /ColorSpace /DeviceRGB\n   /BitsPerComponent 8\n').encode()
    body = zlib.compress(img.tobytes() if stream is None else stream)
    return b'%PDF-1.5\n' + extra + head + parms + b'>>\nstream\n' + body + b'\nendstream\nendobj\n'


def test_the_image_of_a_pdf_reads_back_byte_for_byte_and_odd_streams_are_refused():
    img = np.arange(2 * 3 * 3, dtype=np.uint8).reshape(2, 3, 3)
    assert np.array_equal(fg.pdf_image(_pdf(img)), img)
    for bad in (_pdf(img, extra=_pdf(img)),                                   # two images
                _pdf(img).replace(b'/DeviceRGB', b'/DeviceGray'),
                _pdf(img, parms=b'   /DecodeParms << /Predictor 15 /Columns 3 >>\n'),
                _pdf(img, stream=img.tobytes()[:-1]),                         # a stream a byte short
                _pdf(img, stream=img.tobytes() + b'\0' * 2)):                 # or two bytes long
        with pytest.raises(ValueError):
            fg.pdf_image(bad)


def test_an_axis_fits_its_ticks_linearly_or_in_the_square_root_of_its_labels():
    linear = fg.Axis((100.0, 200.0, 300.0), (0.0, 1.0, 2.0))
    assert linear.value(250.0) == pytest.approx(1.5) and linear.residual_pixels < 1e-9
    square = fg.Axis(tuple(1000 - 1000 * np.sqrt([1.0, 1.21, 1.44])), (1.0, 1.21, 1.44), form='sqrt')
    assert square.value(1000 - 1000 * 1.05) == pytest.approx(1.05 ** 2) and square.residual_pixels < 1e-9
    with pytest.raises(ValueError):
        fg.axis_from_ticks([10.0, None, 30.0], (1.0, 2.0, 3.0))   # two ticks left
    with pytest.raises(ValueError):
        fg.axis_from_ticks([10.0, 20.0, 36.0], (1.0, 2.0, 3.0))   # a tick strays two pixels from the fit


def _axis_image():
    """A plot box's bottom edge at row 80 with ticks every 50 columns from 50 and labels below them; the tick at 150
    lies under a light curve."""
    img = np.full((120, 300, 3), 255, dtype=np.uint8)
    img[80, 20:280] = 38
    for x in (50, 100, 150, 200, 250):
        img[66:80, x - 1:x + 1] = 38
        img[90:100, x - 6:x + 7] = 38                              # the label
    img[60:82, 145:156] = 179                                     # a light curve over the third tick
    return img


def test_ticks_are_found_beside_their_labels_and_one_drawn_over_is_left_out():
    img = _axis_image()
    labels = fg.label_centres(img, rows=(85, 105), columns=(0, 300), gap=10)
    assert labels == pytest.approx([50.0, 100.0, 150.0, 200.0, 250.0], abs=0.6)
    ticks = fg.refine_ticks(img, labels, along='x', line=80, inward=-15)
    assert ticks[2] is None and ticks[0] == pytest.approx(49.5) and ticks[4] == pytest.approx(249.5)
    axis = fg.axis_from_ticks(ticks, (0.0, 1.0, 2.0, 3.0, 4.0))
    assert axis.value(174.5) == pytest.approx(2.5)
    # Ticks of the axes' own colour on the edge, the third hidden under the light curve.
    assert fg.tick_positions(img, along='x', line=80, inward=-15, span=(30, 270)) == [49.5, 99.5, 199.5, 249.5]


def test_a_curve_takes_its_longest_run_tracks_past_a_label_and_leaves_out_runs_another_curve_crosses():
    img = np.full((60, 40, 3), 255, dtype=np.uint8)
    img[20:24, 2:38] = (0, 0, 179)                                # a horizontal line, rows 20-23
    img[30:44, 10:14] = (0, 0, 179)                               # a label beside it, 14 rows tall
    x, mid, width = fg.curve(img, (0, 0, 179), box=(0, 0, 39, 59))
    assert mid[x == 11][0] == pytest.approx(36.5) and width[x == 11][0] == 14
    x, mid, width = fg.curve(img, (0, 0, 179), box=(0, 0, 39, 59), track=True)
    assert np.all(mid == 21.5)
    img[16:20, 25:28] = (254, 0, 0)                               # a red curve drawn over the blue line's edge
    x, mid, width = fg.curve(img, (0, 0, 179), box=(0, 0, 39, 59), track=True, occluders=((254, 0, 0),))
    assert not set(x.tolist()) & {25.0, 26.0, 27.0} and np.all(mid == 21.5)


def test_a_product_reads_back_with_nan_as_null_and_its_key_follows_its_source_and_producer(tmp_path):
    product = dict(schema=fg.SCHEMA, source_sha256='a' * 64, producer=fg.producer(), value=math.nan, values=[1.0, math.nan])
    fg.write(tmp_path / 'f.json', product)
    text = (tmp_path / 'f.json').read_text()
    assert 'NaN' not in text and json.loads(text)['values'] == [1.0, None]
    back = fg.read(tmp_path / 'f.json')
    assert fg.key(back) == fg.key(product) and fg.key(dict(product, source_sha256='b' * 64)) != fg.key(product)
    (tmp_path / 'other.json').write_text('{"schema": "other"}')
    with pytest.raises(ValueError):
        fg.read(tmp_path / 'other.json')


@needs_source
def test_the_papers_figures_read_as_recorded():
    """Pinned against the readings recorded on 2026-10-19 (notes/waterworlds.md); the change's reviewer repeated
    Figure 2 at 400 K, Figure 3 at 300 and 400 K, the lifetime ticks, Figure 4's contours, lines and arrows of Figure 5
    by fits of their own."""
    f = fg.read_all(fg.source_bytes())
    assert f['source_sha256'].startswith('8d416543')
    f3 = f['figure3']
    assert [f3['lifetime_ticks_k'][k] for k in ('1e11', '1e9', '1e7')] == pytest.approx([403.11, 445.22, 498.25],
                                                                                         abs=0.05)
    assert (f3['long_lived']['from_k'], f3['long_lived']['to_k']) == pytest.approx((272.97, 445.06), abs=0.05)
    for name, values in (('expanding', [1326.2, 1445.3]), ('no_expansion', [1239.3, 1239.3])):
        x, y = np.asarray(f3[name]['x']), np.asarray(f3[name]['y'])
        assert np.interp([300.0, 400.0], x[np.argsort(x)], y[np.argsort(x)]) == pytest.approx(values, abs=0.3)
        assert x.min() > 254.0                                    # the legend's sample lines stay out
    f5 = f['figure5']
    assert f5['short_lived_from_k'] == pytest.approx(427.05, abs=0.1)
    assert [f5['lifetime_ticks_k'][k] for k in ('1e7', '1e9', '1e11')] == pytest.approx([476.0, 426.91, 387.98],
                                                                                         abs=0.05)
    arrows = [f5[f'snowball_{a}']['arrow_au'] for a in ('0.25', '0.32', '0.4')]
    assert arrows == pytest.approx([1.0160, 0.9650, 0.9090], abs=2e-4)
    assert [f5[f'snowball_{a}']['end_k'] for a in ('0.25', '0.32', '0.4')] == pytest.approx([270.7, 272.1, 270.6],
                                                                                              abs=0.3)
    assert [f5[f'snowball_{a}']['to_k'] for a in ('0.25', '0.32', '0.4')] == pytest.approx([295.9, 424.2, 494.6],
                                                                                             abs=0.5)
    assert f5['ocean_freeze']['arrow_au'] == pytest.approx(1.0410, abs=2e-4)
    f4 = f['figure4']
    assert f4['transition_g'] == pytest.approx(1.4812, abs=1e-3) and f4['ganymede_g'] == pytest.approx(1.4279, abs=1e-3)
    for star, g, d in (('sun', 1.3, 1.0123), ('sun', 2.0, 1.0460), ('ad_leonis', 2.0, 0.1626)):
        gs, ds = np.asarray(f4[star]['freezing']['g']), np.asarray(f4[star]['freezing']['d'])
        assert np.interp(g, gs[np.argsort(gs)], ds[np.argsort(gs)]) == pytest.approx(d, abs=5e-4)
    # The 273 K contour leaves the panel through 0.9 AU near 1.216 m/s^2; no row reads a label's grey edge.
    assert min(f4['sun']['freezing']['g']) == pytest.approx(1.216, abs=0.005)
    gs, ds = np.asarray(f4['sun']['billion_years']['g']), np.asarray(f4['sun']['billion_years']['d'])
    assert np.interp(2.4, gs[np.argsort(gs)], ds[np.argsort(gs)]) == pytest.approx(0.9606, abs=5e-4)
    f2 = f['figure2']
    x, y = np.asarray(f2['emitting']['x']), np.asarray(f2['emitting']['y'])
    assert np.interp([300.0, 400.0], x[np.argsort(x)], y[np.argsort(x)]) == pytest.approx([1.0592, 1.1968], abs=5e-4)
