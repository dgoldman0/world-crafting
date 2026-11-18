"""The lab's commands for CM1's site boxes, the thin path of plan stages 3, 4, 6 and 7:

    PYTHONPATH=lab:python <env>/bin/python -m worldlab build <study> <case>       # the case's CM1 build, in the store
    PYTHONPATH=lab:python <env>/bin/python -m worldlab case <study> <case>        # its case's folder, from its forcing
    PYTHONPATH=lab:python <env>/bin/python -m worldlab plan <study>               # its boxes: keys, cost, checks
    PYTHONPATH=lab:python <env>/bin/python -m worldlab run <study> <case> --segments 1      # a model day; again resumes
    PYTHONPATH=lab:python <env>/bin/python -m worldlab status <study> <case>
    PYTHONPATH=lab:python <env>/bin/python -m worldlab stop <study> <case>        # after the segment under way
    PYTHONPATH=lab:python <env>/bin/python -m worldlab read <study> <case> 2 4    # rain and ascent over solar days 2-4

<env> is the lab's Python environment (lab/local.toml, [roots] env), which holds netCDF4 for the forcing. `case` and
`run` take `--override ID=justification` for a registry entry that stops the case, recorded with it.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import cm1, cm1_builds, cm1_read, jobs, registry
from .data import DataError
from .roots import root
from .spec import Library, SpecError


def _store() -> Path:
    store = root('store', allow_empty=True)
    if store is None:
        raise DataError("the lab's store is absent: lab/local.toml's [roots] store, or $WORLDLAB_STORE")
    return store


def _overrides(items) -> dict:
    out = {}
    for item in items or []:
        name, sep, why = item.partition('=')
        if not sep or not why.strip():
            raise SpecError(f'an override reads ID=justification, where it is {item!r}')
        out[name.strip()] = why.strip()
    return out


def _gb(n: float) -> str:
    return f'{n / 1e9:.1f} GB'


def build(args) -> int:
    v = cm1.values(Library(), args.study, args.case)
    path = cm1_builds.build(v['settings'], store=_store(), macros=v['macros'], jobs=args.jobs)
    record = cm1_builds.record(path)
    print(f"{path}: {record['inputs']['flags']}, macros {record['inputs']['macros'] or 'none'}, compiled in "
          f"{record['seconds']} s; sources {record['sources']['digest'][:16]}")
    return 0


def case(args) -> int:
    path = cm1.write_case(Library(), args.study, args.case, store=_store(), overrides=_overrides(args.override))
    found = cm1.checked(path)
    checks = found['header']['registry']
    print(f"{args.study}:{args.case}: {path}")
    print(f"  key {found['header']['key'][:16]}; warnings {[w['id'] for w in checks['warnings']] or 'none'}; "
          f"overridden {[o['id'] for o in checks['overridden']] or 'none'}")
    return 0


def plan(args) -> int:
    library, store = Library(), _store()
    study = library.study(args.study)
    total_h, total_disk = 0.0, 0.0
    for name in study.crm:
        line = [f'{args.study}:{name}']
        try:
            v = cm1.values(library, args.study, name)
        except (SpecError, DataError) as error:
            print(f'{line[0]}: refused: {error}')
            continue
        s = v['settings']
        g = s['columns']
        est = jobs.estimate_for(g['nx'], g['ny'], len(v['zw']) - 1, v['scaled']['time_step_s'], v['length_s'],
                                float(s['unscaled']['output_s']), v['restart_s'],
                                diagnostics_s=float(s['unscaled']['diagnostics_s']))
        total_h += est['four_thread_hours']
        total_disk += est['disk_bytes']
        line.append(f"{s['coupling']['vertical_wind']}, {v['solar_days']:g} solar days, "
                    f"{g['nx']} x {g['ny']} x {len(v['zw']) - 1}; about {est['four_thread_hours']:.1f} four-thread "
                    f"hours and {_gb(est['disk_bytes'])}")
        try:
            a = cm1.assess(library, args.study, name, store=store, overrides=_overrides(args.override))
        except (SpecError, DataError, ValueError) as error:
            line.append(f'waits: {error}')
            print('\n  '.join(line))
            continue
        k = a['keyed']['key']
        from climate.crm import gcm_site as gs
        if s['coupling']['vertical_wind'] not in gs.COUPLINGS:
            line.append(f"waits: gcm_site takes the couplings {gs.COUPLINGS}; '{s['coupling']['vertical_wind']}' joins "
                        'with its patch')
        written = (store / 'cases' / f'cm1-{k[:16]}' / 'case.json').is_file()
        built = (cm1_builds.folder(store, a['keyed']['inputs']['build']) / 'build.json').is_file()
        run = jobs.folder(store, k)
        state = jobs.status(run) if (run / jobs.RECORD).exists() else 'no run yet'
        c = a['checks']
        line.append(f"key {k[:16]}; build {a['keyed']['inputs']['build'][:16]} {'built' if built else 'to build'}; "
                    f"case {'written' if written else 'to write'}; {state}")
        line.append(f"registry: warns {[w['id'] for w in c['warnings']] or 'nothing'}; stops "
                    f"{[w['id'] for w in c['stops']] or 'nothing'}"
                    + (f"; overridden {[o['id'] for o in c['overridden']]}" if c['overridden'] else '')
                    + (f"; unevaluated {[u['id'] for u in c['unevaluated']]}" if c['unevaluated'] else ''))
        print('\n  '.join(line))
    print(f'{args.study}: about {total_h:.1f} four-thread hours and {_gb(total_disk)} for every box run whole')
    return 0


def run(args) -> int:
    library, store = Library(), _store()
    path = cm1.write_case(library, args.study, args.case, store=store, overrides=_overrides(args.override))
    found = cm1.checked(path)
    build = cm1_builds.folder(store, found['record']['build']['key'])
    if not (build / 'build.json').is_file():
        raise DataError(f'{build}: the case\'s build is absent; `python -m worldlab build {args.study} {args.case}` '
                        'makes it')
    record = jobs.run_case(path, store=store, threads=args.threads, segments=args.segments, hours=args.hours,
                           overrides=_overrides(args.override), keep_restarts=args.keep_restarts, library=library)
    print(jobs.status(jobs.folder(store, record['key'])))
    if record.get('held_back') and record['state'] == 'paused':
        print(f"  held back: {record['held_back'][-1]['reason']}")
    return 0


def _run_folder(args) -> Path:
    """The case's run in the store, found by the case's key as this worktree's specifications and code compute it, as
    `run` finds it; the store's shared index of names, which every worktree's `case` and `run` repoint, is left aside."""
    store = _store()
    key = cm1.case_key(Library(), args.study, args.case, store=store)['key']
    run = jobs.folder(store, key)
    if not (run / jobs.RECORD).is_file():
        raise DataError(f'{args.study}:{args.case} has no run in the store under its key {key[:16]} ({run})')
    return run


def status(args) -> int:
    print(jobs.status(_run_folder(args)))
    return 0


def stop(args) -> int:
    print(jobs.stop(_run_folder(args)))
    return 0


def read(args) -> int:
    print(json.dumps(cm1_read.summary(_run_folder(args), (args.first, args.last)), indent=1))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog='python -m worldlab', description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='command', required=True)
    for name, fn in (('build', build), ('case', case), ('run', run), ('status', status), ('stop', stop),
                     ('read', read)):
        p = sub.add_parser(name)
        p.add_argument('study')
        p.add_argument('case')
        p.set_defaults(fn=fn)
        if name == 'build':
            p.add_argument('--jobs', type=int, default=4)
        if name in ('case', 'run'):
            p.add_argument('--override', action='append', metavar='ID=JUSTIFICATION')
        if name == 'run':
            p.add_argument('--threads', type=int, default=4)
            p.add_argument('--segments', type=int)
            p.add_argument('--hours', type=float)
            p.add_argument('--keep-restarts', type=int, default=0, help='the newest restart sets kept; 0 keeps all')
        if name == 'read':
            p.add_argument('first', type=float)
            p.add_argument('last', type=float)
    p = sub.add_parser('plan')
    p.add_argument('study')
    p.add_argument('--override', action='append', metavar='ID=JUSTIFICATION')
    p.set_defaults(fn=plan)
    args = parser.parse_args(argv)
    try:
        return args.fn(args)
    except registry.Refused as error:
        print(f'refused: {error}', file=sys.stderr)
        return 3
    except jobs.Interrupted as error:
        print(f'interrupted: {error}; the run resumes from its last segment', file=sys.stderr)
        return 130
    except (SpecError, DataError, jobs.JobError, ValueError) as error:
        print(f'stopped: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
