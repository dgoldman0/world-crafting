"""The PDS3 label, image and SHADR readers on small synthetic files, and the geoid's terms in closed form."""
from __future__ import annotations
import math
import numpy as np
import pytest

from geography import topography as tp

RADIUS = 1737400.0

LABEL = '''PDS_VERSION_ID            = "PDS3"
/* a comment, with = and "quotes" */
PRODUCT_ID                = "TEST_1"
TARGET_NAME               = MOON
DESCRIPTION               = "Two lines
   of text (with brackets)."
MISSION_PHASE_NAME        = {{"ONE","TWO
                            THREE"}}
OBJECT                    = UNCOMPRESSED_FILE
FILE_NAME                 = "TEST_1.IMG"
^IMAGE                    = "TEST_1.IMG"
  OBJECT                  = IMAGE
    LINES                 = {lines}
    LINE_SAMPLES          = {samples}
    SAMPLE_TYPE           = {sample_type}
    SAMPLE_BITS           = 16
    UNIT                  = {unit}
    SCALING_FACTOR        = 0.5
    OFFSET                = {offset}
{missing}  END_OBJECT              = IMAGE
END_OBJECT                = UNCOMPRESSED_FILE
OBJECT                    = IMAGE_MAP_PROJECTION
 MAP_PROJECTION_TYPE          = "{projection}"
 MAP_RESOLUTION               = {ppd} <pix/deg>
 A_AXIS_RADIUS                = 1737.4 <km>
 POSITIVE_LONGITUDE_DIRECTION = "{direction}"
 CENTER_LATITUDE              = 0 <deg>
 CENTER_LONGITUDE             = {centre} <deg>
 FIRST_STANDARD_PARALLEL      = 'N/A'
 MAXIMUM_LATITUDE             = 90 <deg>
 MINIMUM_LATITUDE             = {south} <deg>
 WESTERNMOST_LONGITUDE        = {west} <deg>
 EASTERNMOST_LONGITUDE        = {east} <deg>
 LINE_PROJECTION_OFFSET       = {line_offset} <pix>
 SAMPLE_PROJECTION_OFFSET     = {sample_offset} <pix>
 COORDINATE_SYSTEM_NAME       = "MEAN EARTH/POLAR AXIS OF DE421"
END_OBJECT                    = IMAGE_MAP_PROJECTION
END
'''


def write_image(folder, ppd=1, sample_type='LSB_INTEGER', unit='METER', offset='1737400.', south=-90, west=0,
                line_offset=None, projection='SIMPLE CYLINDRICAL', direction='EAST', missing=None, data=None,
                name='test_1.img'):
    lines, samples = int(180 * ppd), int(360 * ppd)
    label = folder / 'test_1.lbl'
    label.write_text(LABEL.format(
        lines=lines, samples=samples, sample_type=sample_type, unit=unit, offset=offset, ppd=ppd, south=south,
        west=west, east=west + 360, centre=west + 180, projection=projection, direction=direction,
        line_offset=90 * ppd - 0.5 if line_offset is None else line_offset, sample_offset=180 * ppd - 0.5,
        missing='' if missing is None else f'    MISSING_CONSTANT      = {missing}\n'))
    dn = np.arange(lines * samples, dtype=np.int64).reshape(lines, samples) % 2000 - 1000 if data is None else data
    dn.astype('<i2' if sample_type == 'LSB_INTEGER' else '>i2').tofile(folder / name)
    return label, folder / name, dn


def test_the_label_reader_keeps_objects_strings_sets_and_units(tmp_path):
    label, _, _ = write_image(tmp_path)
    tree = tp.read_pds3_label(label)
    assert tree['TARGET_NAME'] == 'MOON' and tree['PRODUCT_ID'] == 'TEST_1'
    assert tree['DESCRIPTION'] == 'Two lines of text (with brackets).'
    assert tree['MISSION_PHASE_NAME'] == ('ONE', 'TWO THREE')
    image = tree['UNCOMPRESSED_FILE']['IMAGE']
    assert (image['LINES'], image['SAMPLE_TYPE'], image['OFFSET']) == (180, 'LSB_INTEGER', 1737400.0)
    projection = tree['IMAGE_MAP_PROJECTION']
    assert projection['MAP_RESOLUTION'] == (1, 'pix/deg') and projection['A_AXIS_RADIUS'] == (1737.4, 'km')
    assert projection['FIRST_STANDARD_PARALLEL'] == 'N/A'


def test_the_label_reader_lists_repeated_objects_reads_based_integers_and_refuses_open_ones(tmp_path):
    path = tmp_path / 'table.lbl'
    path.write_text('^T = ("X.TAB",3)\nMISSING = 16#FC18#\nOBJECT = T\n OBJECT = COLUMN\n  NAME = "A"\n END_OBJECT = COLUMN\n'
                    ' OBJECT = COLUMN\n  NAME = "B"\n END_OBJECT\nEND_OBJECT = T\nEND\n')
    tree = tp.read_pds3_label(path)
    assert tree['^T'] == ('X.TAB', 3) and [c['NAME'] for c in tree['T']['COLUMN']] == ['A', 'B']
    assert tree['MISSING'] == 0xFC18 and isinstance(tree['MISSING'], tp.Bits)
    path.write_text('OBJECT = T\n NAME = "A"\nEND\n')
    with pytest.raises(ValueError, match='left open'):
        tp.read_pds3_label(path)


@pytest.mark.parametrize('sample_type', ['LSB_INTEGER', 'MSB_INTEGER'])
def test_an_image_reads_as_heights_above_its_sphere_on_its_grid(tmp_path, sample_type):
    label, image, dn = write_image(tmp_path, ppd=2, sample_type=sample_type)
    height, grid, info = tp.read_pds_image(label, image)
    assert np.array_equal(height, dn * 0.5)
    assert grid.radius_m == RADIUS and grid.pixels_per_degree == 2
    assert grid.lat_deg[0] == 89.75 and grid.lat_deg[-1] == -89.75 and grid.lon_deg[0] == 0.25 and grid.lon_deg[-1] == 359.75
    assert info == dict(reference_radius_m=RADIUS, target='MOON', frame='MEAN EARTH/POLAR AXIS OF DE421', product='TEST_1')


def test_an_image_in_kilometres_reads_in_metres(tmp_path):
    label, image, dn = write_image(tmp_path, unit='KILOMETER', offset='1737.4')
    height, grid, _ = tp.read_pds_image(label, image)
    assert np.array_equal(height, dn * 500.0) and grid.radius_m == pytest.approx(RADIUS, rel=1e-15)


@pytest.mark.parametrize('change, message', [
    (dict(name='other.img'), 'describes TEST_1.IMG'),
    (dict(south=-80), 'pixel-registered global map'),
    (dict(ppd=0.5), '0.5 pixels per degree, where the reader takes a whole number'),
    (dict(line_offset=90), 'pixel registration'),
    (dict(data=np.zeros((180, 359), np.int64)), 'bytes, where the label describes'),
    (dict(offset='0'), 'an OFFSET of 0'),
    (dict(unit='FOOT'), "samples in 'FOOT'"),
    (dict(projection='POLAR STEREOGRAPHIC'), 'where the reader takes SIMPLE CYLINDRICAL'),
    (dict(direction='WEST'), 'west longitudes'),
    (dict(west=-180), r'columns from -180\.0 E'),
    (dict(sample_type='VAX_REAL'), 'samples of 16-bit VAX_REAL'),
    (dict(missing='-1000'), '33 samples missing'),
    (dict(missing='16#FC18#'), '33 samples missing'),           # -1000 as 16 bits
])
def test_the_image_reader_refuses_what_its_label_misdescribes(tmp_path, change, message):
    label, image, _ = write_image(tmp_path, **change)
    with pytest.raises(ValueError, match=message):
        tp.read_pds_image(label, image)


def test_a_missing_constant_absent_from_the_image_leaves_it_whole(tmp_path):
    label, image, dn = write_image(tmp_path, missing='16#8000#')    # -32768 as 16 bits
    assert np.array_equal(tp.read_pds_image(label, image)[0], dn * 0.5)


SHADR_LABEL = '''PDS_VERSION_ID = PDS3
^SHADR_HEADER_TABLE = ("TEST_SHA.TAB",1)
^SHADR_COEFFICIENTS_TABLE = ("TEST_SHA.TAB",3)
OBJECT = SHADR_HEADER_TABLE
  OBJECT = COLUMN
    NAME = "REFERENCE RADIUS"
    UNIT = "{unit}"
  END_OBJECT = COLUMN
  OBJECT = COLUMN
    NAME = "CONSTANT"
    UNIT = "N/A"
  END_OBJECT = COLUMN
END_OBJECT = SHADR_HEADER_TABLE
END
'''


def write_shadr(folder, unit='KILOMETER', normalized=1, degree=3, by_order=False, drop=()):
    (folder / 'test_sha.lbl').write_text(SHADR_LABEL.format(unit=unit))
    pairs = [(n, m) for n in range(1, degree + 1) for m in range(n + 1) if (n, m) not in drop]
    rows = [f' 0.1738000000000000E+04, 0.4902800126160000E+04, 0.1E-04, {degree:4d}, {degree:4d}, {normalized:4d}, 0.0, 0.0']
    for n, m in sorted(pairs, key=lambda p: (p[1], p[0])) if by_order else pairs:
        rows.append(f'{n:5d},{m:5d}, {n + m / 10:.16E}, {-(n + m / 10) if m else 0.0:.16E}, 0.0, 0.0')
    (folder / 'test_sha.tab').write_text('\n'.join(rows) + '\n')
    return folder / 'test_sha.lbl', folder / 'test_sha.tab'


@pytest.mark.parametrize('by_order', [False, True])
def test_a_shadr_table_reads_to_the_degree_asked_in_any_row_order(tmp_path, by_order):
    field = tp.read_shadr(*write_shadr(tmp_path, by_order=by_order), 2)
    assert field.degree == 2 and field.reference_radius_m == 1738000.0
    assert field.gm_m3_s2 == pytest.approx(4902.80012616e9, rel=1e-15)
    assert field.c[2, 1] == 2.1 and field.s[2, 1] == -2.1 and field.c[1, 0] == 1.0 and field.s[2, 0] == 0.0


@pytest.mark.parametrize('change, degree, message', [
    (dict(unit='METER'), 2, 'where SHADR takes km'),
    (dict(normalized=0), 2, 'fully normalized'),
    (dict(), 4, 'below the 4 asked for'),
    (dict(drop={(3, 2)}), 3, '1 coefficients of degrees 2 to 3 missing'),
])
def test_the_shadr_reader_refuses_other_units_states_degrees_and_gaps(tmp_path, change, degree, message):
    with pytest.raises(ValueError, match=message):
        tp.read_shadr(*write_shadr(tmp_path, **change), degree)


def zonal_field(c20: float, degree: int = 4, gm: float = 4.9028e12, ref: float = 1738000.0) -> tp.Field:
    c = np.zeros((degree + 1, degree + 1))
    c[2, 0] = c20
    return tp.Field(c, np.zeros_like(c), gm, ref)


def test_a_zonal_field_spun_gives_its_closed_form_geoid():
    grid = tp.Grid.globe(2, RADIUS)
    field, omega = zonal_field(-9.09e-5), 2.6617e-6
    gamma = field.gm_m3_s2 / RADIUS**2
    t = np.sin(np.radians(grid.lat_deg))
    expected = (RADIUS * (field.reference_radius_m / RADIUS)**2 * -9.09e-5 * math.sqrt(5) * (3 * t**2 - 1) / 2
                + 0.5 * omega**2 * RADIUS**2 * (1 - t**2 - 2.0 / 3.0) / gamma)
    geoid = tp.geoid(grid, field, 4, omega)
    assert np.allclose(geoid, expected[:, None], rtol=0, atol=1e-9)
    area = grid.cell_area_m2                     # the cell-centre sum of a degree-2 term errs by ~1e-5 of it
    assert abs((geoid * area).sum() / area.sum()) < 3e-5 * np.abs(geoid).max()


def test_the_tides_mean_takes_its_closed_forms():
    assert tp.tide_coefficients(0.0, 0.0) == (-0.5, 0.75)
    for e in (0.0549, 0.3):
        a0, _ = tp.tide_coefficients(e, 0.0)            # the mean of (a/r)^3, in the plane of the equator
        assert a0 == pytest.approx(-0.5 * (1 - e * e) ** -1.5, rel=1e-12)
    for inclination in (6.6874, 30.0):
        a0, a22 = tp.tide_coefficients(0.0, inclination)
        c = math.cos(math.radians(inclination))
        assert a0 == pytest.approx(0.75 * (1 - c * c) - 0.5, rel=1e-12)
        assert a22 == pytest.approx(0.75 * (c + (1 - c) ** 2 / 4), rel=1e-12)


def test_the_moons_librations_lower_its_tide_by_two_percent():
    e, inclination = 0.0549, 6.6874
    a0, a22 = tp.tide_coefficients(e, inclination)
    fixed = (1 - e * e) ** -1.5                          # Earth held over the sub-point at the orbit's mean 1/r^3
    assert 1 - a0 / (-0.5 * fixed) == pytest.approx(0.0203, abs=5e-4)
    assert 1 - a22 / (0.75 * fixed) == pytest.approx(0.0187, abs=5e-4)


def test_a_host_fixed_in_the_sky_raises_its_tide_about_its_sub_longitude():
    grid = tp.Grid.globe(2, RADIUS)
    field = zonal_field(0.0)
    gamma = field.gm_m3_s2 / RADIUS**2
    height = tp.geoid(grid, field, 2, 0.0, tp.Tide(3.986004418e14, 3.8382e8, love_k2=0.0248, sub_lon_deg=90.25))
    peak = (1 + 0.0248) * 3.986004418e14 * RADIUS**2 / 3.8382e8**3 / gamma
    i, j = np.unravel_index(np.argmax(height), height.shape)
    assert height.max() == pytest.approx(peak, rel=1e-4)            # at 0.25 degrees from the sub-point
    assert abs(grid.lat_deg[i]) == 0.25 and grid.lon_deg[j] in (90.25, 270.25)
    area = grid.cell_area_m2
    assert abs((height * area).sum() / area.sum()) < 3e-5 * peak
    # About the sub-point (0 N, 0 E), the tide is the one Terluna wrote, (3 cos^2(lat) cos^2(lon) - 1) / 2.
    centred = tp.geoid(grid, field, 2, 0.0, tp.Tide(3.986004418e14, 3.8382e8, love_k2=0.0248))
    cos_psi = np.outer(np.cos(np.radians(grid.lat_deg)), np.cos(np.radians(grid.lon_deg)))
    assert np.allclose(centred, peak * 0.5 * (3 * cos_psi**2 - 1), rtol=0, atol=1e-12 * peak)


def test_the_geoid_refuses_degrees_beyond_its_field_and_subtracts_from_the_heights():
    grid = tp.Grid.globe(1, RADIUS)
    with pytest.raises(ValueError, match='read to degree 4'):
        tp.geoid(grid, zonal_field(1e-5), 5, 0.0)
    height = np.full((180, 360), 100.0)
    topo, geoid = tp.height_above_geoid(height, grid, zonal_field(1e-5), 4, 0.0)
    assert np.array_equal(topo, height - geoid)
