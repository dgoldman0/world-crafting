"""HITEMP2010's water lines (Rothman et al. 2010) from the 34 zips HITRANonline serves, cut as Schaefer et al. (2016) cut
them for their line-by-line model, which Arnscheidt, Wordsworth and Ding (2019) used: a line stays where its strength
at 1000 K reaches 1e-30 cm/molecule.

The zips hold HITEMP2010's 114,241,164 water lines from 0 to 30,000 cm^-1 in HITRAN's 160-character records, each closed
by CR LF. They are the lab's data, recorded with their sizes, sha256 and rights review in lab/data/manifest.toml (entry
`hitemp2010-h2o`) and kept in the store at data/<digest>/<name>, and the reader takes their records in place, block by
block. A line's strength scales with temperature as in the radiative-convective column's spectroscopy, through HITRAN's
partition sums. Two kinds of line are dropped: a line at 0 cm^-1, whose strength vanishes and of which HITEMP2010 holds
none, and a line whose lower-state energy HITEMP leaves unknown (-1), whose strength has no temperature scaling, 19 of
H2(17)O and H2(18)O between 11,800 and 14,420 cm^-1. The lines the cut keeps form one of that spectroscopy's
LineLists, cached in the store at caches/hitemp-lines/ under a key of the zips' and the partition sums' hashes, the
isotopologues' ids and masses, the scaling's constants, the cut and the reader's version.

    python -m atmosphere.waterworlds.hitemp [--store STORE] [--processes N]   # cut the zips and count the lines

The zips' sizes and hashes are checked when the cache lacks the cut list and the reader cuts them anew.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid
import zipfile

import numpy as np

from atmosphere.radiative_convective import fetch_inputs as column_inputs, spectroscopy as sp

ENTRY = 'hitemp2010-h2o'   # in the lab's data manifest
FLOOR = 1e-30              # cm/molecule, at T_CUT
T_CUT = 1000.0             # K
WIDTH = 162                # a record's 160 characters and its CR LF
BLOCK = 1 << 19            # records read at a time
VERSION = 2                # of the reader and the cut: raised when either changes, it rebuilds the cached lists
FIELDS = {'nu': (3, 15), 'strength': (15, 25), 'gamma_air': (35, 40), 'gamma_self': (40, 45), 'elower': (45, 55),
          'n_air': (55, 59), 'delta_air': (59, 67)}
ORDER = ('nu', 'strength', 'gamma_air', 'gamma_self', 'elower', 'n_air', 'delta_air', 'gid', 'mass')


def _isotopologues() -> tuple[np.ndarray, np.ndarray]:
    """Water's global isotopologue ids and molar masses by the byte of a record's isotopologue column, -1 and NaN
    elsewhere."""
    gid, mass = np.full(256, -1, dtype=np.int64), np.full(256, np.nan)
    for (molecule, code), (g, m) in sp.ISOTOPOLOGUES.items():
        if molecule == 1:
            gid[ord(code)], mass[ord(code)] = g, m
    return gid, mass


GID, MASS = _isotopologues()
WATER = np.unique(GID[GID >= 0])
SUM_FILES = tuple(f'hitran_q{g}.txt' for g in WATER)


def blocks(path: Path, size: int = BLOCK):
    """The records of a zip's one member as uint8 rows of WIDTH bytes, `size` records at a time. A member of another
    layout, or a record of another length or molecule, raises ValueError."""
    with zipfile.ZipFile(path) as archive:
        members = archive.infolist()
        if len(members) != 1 or members[0].file_size % WIDTH:
            raise ValueError(f'{path}: one member of whole {WIDTH}-byte records expected')
        with archive.open(members[0]) as handle:
            while data := handle.read(size * WIDTH):
                if len(data) % WIDTH:
                    raise ValueError(f'{path}: a record cut short')
                block = np.frombuffer(data, dtype=np.uint8).reshape(-1, WIDTH)
                if (block[:, 160] != 13).any() or (block[:, 161] != 10).any():
                    raise ValueError(f'{path}: a record of another length')
                if (block[:, 0] != ord(' ')).any() or (block[:, 1] != ord('1')).any():
                    raise ValueError(f'{path}: a record of another molecule')
                yield block


def _field(block: np.ndarray, start: int, stop: int) -> np.ndarray:
    """One fixed-width field of every record, as floats."""
    return np.ascontiguousarray(block[:, start:stop]).view(f'S{stop - start}').ravel().astype(float)


def strengths(nu, strength, elower, gid, sums: sp.PartitionSums, t: float) -> np.ndarray:
    """Each line's strength at t (cm/molecule) from its value at 296 K, scaled as the column's spectroscopy scales it."""
    return (strength * sums.ratio(gid, t) * np.exp(-sp.C2 * elower * (1 / t - 1 / sp.T_REF))
            * (-np.expm1(-sp.C2 * nu / t)) / (-np.expm1(-sp.C2 * nu / sp.T_REF)))


def cut(paths, sums: sp.PartitionSums, *, floor: float = FLOOR, t_cut: float = T_CUT) -> tuple[dict, int]:
    """The lines of the zips whose strength at t_cut reaches floor, field by field in the order of ORDER and sorted by
    wavenumber, with the count of lines read."""
    parts, read = [], 0
    for path in paths:
        for block in blocks(path):
            read += len(block)
            gid = GID[block[:, 2]]
            if (gid < 0).any():
                raise ValueError(f"{path}: an isotopologue code outside HITRAN's water")
            nu, strength, elower = _field(block, 3, 15), _field(block, 15, 25), _field(block, 45, 55)
            known = (nu > 0) & (elower >= 0)
            keep = known & (strengths(np.where(known, nu, 1.0), strength, np.where(known, elower, 0.0), gid, sums,
                                      t_cut) >= floor)
            kept = block[keep]
            part = {name: _field(kept, a, b) for name, (a, b) in FIELDS.items()
                    if name not in ('nu', 'strength', 'elower')}
            part.update(nu=nu[keep], strength=strength[keep], elower=elower[keep], gid=gid[keep],
                        mass=MASS[kept[:, 2]])
            parts.append(part)
    if parts:
        lines = {k: np.concatenate([p[k] for p in parts]) for k in ORDER}
    else:
        lines = {k: np.zeros(0, dtype=np.int64 if k == 'gid' else float) for k in ORDER}
    order = np.argsort(lines['nu'], kind='stable')
    return {k: v[order] for k, v in lines.items()}, read


def key(zips, *, floor: float = FLOOR, t_cut: float = T_CUT) -> str:
    """The cut list's key, from each zip's name and sha256 as their record gives them, the partition sums' hashes, the
    cut and the reader's version."""
    sums = {f['name']: f['sha256'] for f in column_inputs.manifest()['files'] if f['name'] in SUM_FILES}
    isotopologues = sorted([code, g, m] for (molecule, code), (g, m) in sp.ISOTOPOLOGUES.items() if molecule == 1)
    text = json.dumps(dict(zips=sorted([str(n), str(s)] for n, s in zips), sums=sums, isotopologues=isotopologues,
                           c2=sp.C2, t_ref=sp.T_REF, floor=floor, t_cut=t_cut, width=WIDTH, version=VERSION),
                      sort_keys=True)
    return hashlib.sha256(text.encode()).hexdigest()[:16]


_WORKER: dict = {}


def _cut_one(path: Path, floor: float, t_cut: float) -> tuple[dict, int]:
    return cut([path], _WORKER['sums'], floor=floor, t_cut=t_cut)


def load(zips, cache: Path, *, paths, floor: float = FLOOR, t_cut: float = T_CUT, processes: int = 1,
         report=print) -> sp.LineList:
    """The zips' lines that pass the cut, from the cache folder, or cut and cached there. `zips` gives each zip's name
    and sha256 as their record has them; `paths`, called only when the cache lacks the cut list, returns the zips' files
    in the same order, once their sizes and hashes match that record."""
    zips = [(str(n), str(s)) for n, s in zips]
    if not zips:
        raise ValueError('no zips given')
    path = Path(cache) / f'{key(zips, floor=floor, t_cut=t_cut)}.npz'
    if path.is_file():
        with np.load(path) as data:
            return sp.LineList('H2O', *(data[k] for k in ORDER))
    files = [Path(p) for p in paths()]
    if [p.name for p in files] != [n for n, _ in zips]:
        raise ValueError('the zips given differ from their record')
    sums = sp.PartitionSums(WATER)
    if processes > 1:
        import multiprocessing as mp
        _WORKER['sums'] = sums                    # the forked workers inherit it
        with mp.get_context('fork').Pool(min(processes, len(files))) as pool:
            results = pool.starmap(_cut_one, [(p, floor, t_cut) for p in files], chunksize=1)
    else:
        results = [cut([p], sums, floor=floor, t_cut=t_cut) for p in files]
    for p, (part, read) in zip(files, results):
        report(f'{p.name}: {len(part["nu"])} of {read} lines kept')
    read = sum(r[1] for r in results)
    lines = {}
    for k in ORDER:                               # one field at a time, each zip's copy freed once joined
        lines[k] = np.concatenate([r[0].pop(k) for r in results])
    del results
    order = np.argsort(lines['nu'], kind='stable')
    for k in ORDER:
        lines[k] = lines[k][order]
    path.parent.mkdir(parents=True, exist_ok=True)
    part = path.with_name(f'.part{os.getpid()}-{uuid.uuid4().hex}.npz')
    try:
        with open(part, 'wb') as handle:
            np.savez(handle, read=np.int64(read), **lines)
            handle.flush()
            os.fsync(handle.fileno())
        part.replace(path)
    except BaseException:
        part.unlink(missing_ok=True)
        raise
    return sp.LineList('H2O', *(lines[k] for k in ORDER))


def from_store(store: Path | None = None, *, floor: float = FLOOR, t_cut: float = T_CUT, processes: int = 1,
               report=print) -> tuple[sp.LineList, Path]:
    """HITEMP2010's water lines that pass the cut, through the lab's data manifest and its store, with the cut list's
    file; the store defaults to the lab's own (lab/local.toml or $WORLDLAB_STORE)."""
    from worldlab.data import Manifest           # the lab's manifest records the zips
    from worldlab.roots import root
    store = Path(store) if store is not None else root('store')
    if store is None:
        raise FileNotFoundError("the lab's store is unset (lab/local.toml's [roots] store, or $WORLDLAB_STORE)")
    manifest = Manifest()
    zips = [(f.name, f.sha256) for f in manifest.files(ENTRY)]
    cache = store / 'caches' / 'hitemp-lines'
    lines = load(zips, cache, paths=lambda: list(manifest.paths(ENTRY, store=store).values()), floor=floor,
                 t_cut=t_cut, processes=processes, report=report)
    return lines, cache / f'{key(zips, floor=floor, t_cut=t_cut)}.npz'


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--store', type=Path, help="the lab's store, which holds the zips and the cache")
    parser.add_argument('--processes', type=int, default=1)
    args = parser.parse_args(argv)
    lines, path = from_store(args.store, processes=args.processes)
    with np.load(path) as data:
        read = int(data['read'])
    gids, counts = np.unique(lines.gid, return_counts=True)
    print(json.dumps(dict(file=str(path), read=read, kept=len(lines), floor=FLOOR, t_cut_k=T_CUT,
                          nu_cm=[float(lines.nu.min()), float(lines.nu.max())],
                          by_isotopologue={int(g): int(c) for g, c in zip(gids, counts)},
                          gamma_self_nonpositive=int((lines.gamma_self <= 0).sum())), indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
