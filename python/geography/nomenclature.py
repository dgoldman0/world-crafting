"""IAU feature names from the USGS Gazetteer of Planetary Nomenclature.

The gazetteer's centre-point archive for a body (a zipped shapefile, such as
MOON_nomenclature_center_pts.zip) carries a dBase table with each feature's name,
type code, diameter and centre. The table alone is read, with a small dBase III
reader, which leaves shapefile libraries out.

    features(archive)    # adopted names: name, code, diameter_km, lat, lon (east, -180..180)

Type codes used here: ME mare, OC oceanus, SI sinus, LC lacus, PA palus (water
names); MO mons or montes; AA crater; LF landing-site name; AL albedo feature.
"""
from __future__ import annotations
import struct
import zipfile

WATER_CODES = {'ME': 'Mare', 'OC': 'Oceanus', 'SI': 'Sinus', 'LC': 'Lacus', 'PA': 'Palus'}


def read_dbf(data: bytes, encoding: str = 'utf-8') -> list[dict]:
    """Records of a dBase III table as dicts; numeric fields become floats (None when blank)."""
    count, header_len, record_len = struct.unpack('<IHH', data[4:12])
    fields = []
    pos = 32
    while data[pos] != 0x0D:
        name = data[pos:pos + 11].split(b'\x00', 1)[0].decode('ascii')
        kind = chr(data[pos + 11])
        length = data[pos + 16]
        fields.append((name, kind, length))
        pos += 32
    rows = []
    for i in range(count):
        start = header_len + i * record_len
        record = data[start:start + record_len]
        if record[:1] == b'*':
            continue
        row, offset = {}, 1
        for name, kind, length in fields:
            raw = record[offset:offset + length].decode(encoding, errors='replace').strip()
            offset += length
            if kind in 'NF':
                row[name] = float(raw) if raw else None
            else:
                row[name] = raw
        rows.append(row)
    return rows


def features(path, adopted_only: bool = True) -> list[dict]:
    """A body's features from its gazetteer archive, with east longitudes in -180..180."""
    with zipfile.ZipFile(path) as archive:
        name = next(n for n in archive.namelist() if n.lower().endswith('.dbf'))
        cpg = next((n for n in archive.namelist() if n.lower().endswith('.cpg')), None)
        encoding = archive.read(cpg).decode('ascii').strip() if cpg else 'utf-8'
        rows = read_dbf(archive.read(name), encoding or 'utf-8')
    out = []
    for r in rows:
        if adopted_only and 'Adopted' not in (r.get('approval') or ''):
            continue
        lon = r['center_lon']
        out.append(dict(name=r['clean_name'] or r['name'], code=r['code'], type=r['type'],
                        diameter_km=r['diameter'] or 0.0, lat=r['center_lat'],
                        lon=lon - 360.0 if lon > 180.0 else lon))
    return out


def by_name(items: list[dict]) -> dict:
    return {f['name']: f for f in items}
