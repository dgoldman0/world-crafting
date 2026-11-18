"""The registry's checks before a run: each entry of lab/registry/earth_assumptions.toml evaluated for one model run's
world, scenario, resolved settings and own quantities (lab/design/architecture.md, "The registry of Earth assumptions
and the reach report"; plan.md, stage 6).

An entry's `when` is a list of tests, all of which must hold for the entry to hold:

- `q`: a quantity of the context: the planet record's (`derive.planet`) and the run's own, such as a CM1 case's
  `soil_layer_ratio` or `cm1_damping_clearance_m`;
- `field`: a field of the world or the scenario by dotted path, looked up in the world first; a field they leave out
  holds no value, for which `ne` holds and every other test fails;
- `config`: `<model>.<path>` in the run's resolved settings, for an entry of that model;
- `calibration`: a calibration's envelope, which a run without calibrations leaves unevaluated.

Each test compares by `eq`, `ne`, `lt`, `gt`, `outside` (a closed range the value lies beyond) or `any_in` (a value, or
any value of a table, in a list), `eq` and `ne` within `rel_tolerance` where it is given. An entry whose test names a
quantity or calibration the context lacks, or reads a quantity of NaN, is reported unevaluated, with what it lacks.

Where an entry holds, its action decides: `warn` copies its warning into the run's record; `refuse`, `require-switch`,
`require-build` and `require-refit` stop the run, unless the run carries an override for the entry's id, whose
justification the record keeps (architecture.md, Principles, "Refusal with a reason"). An unevaluated entry of those
four actions stops the run too, as the lab can show neither that it holds nor that it fails, and an override lets the
run past it alike; an unevaluated warning is reported and stops nothing. The checks test what the run states: an entry
whose repair is a setting tests that setting in its `when`, as B28 tests `rain_size_limits`.
"""
from __future__ import annotations

import math

from .spec import SpecError, get_path

STOPS = ('refuse', 'require-switch', 'require-build', 'require-refit')
COMPARISONS = ('eq', 'ne', 'lt', 'gt', 'outside', 'any_in')
MISSING = object()


class Refused(SpecError):
    """A run the registry stops: its entries, each with its action and effect."""

    def __init__(self, entries: list[dict], where: str):
        self.entries = entries
        lines = '; '.join(f"{e['id']} ({e['action']}{', unevaluated, lacking ' + e['lacks'] if 'lacks' in e else ''}): "
                          f"{e['assumes']}" for e in entries)
        super().__init__(f'{where}: refused by the registry, {lines}. A run goes ahead past an entry only with an '
                         'override that states its justification')


def models(entry: dict) -> set[str]:
    return {m.strip() for m in str(entry.get('model', '')).split(',') if m.strip()}


def _lookup(test: dict, context: dict, model: str):
    """The value a test reads, MISSING where the context holds none, or a string naming what it lacks (unevaluated)."""
    if 'q' in test:
        quantities = context.get('q', {})
        return quantities[test['q']] if test['q'] in quantities else f"quantity {test['q']}"
    if 'field' in test:
        for tree in (context.get('world', {}), context.get('scenario', {})):
            try:
                return get_path(tree, test['field'])
            except KeyError:
                continue
        return MISSING
    if 'config' in test:
        owner, _, path = test['config'].partition('.')
        if owner != model:
            return f"another model's setting {test['config']}"
        try:
            return get_path(context.get('settings', {}), path)
        except KeyError:
            return MISSING
    if 'calibration' in test:
        return f"calibration {test['calibration']}"
    raise SpecError(f'registry: a test reads q, field, config or calibration, where it is {test}')


def _same(value, target, tolerance) -> bool:
    if tolerance is not None and isinstance(value, (int, float)) and isinstance(target, (int, float)) \
            and not isinstance(value, bool):
        return abs(value - target) <= tolerance * abs(target)
    return value == target and type(value) is type(target) if isinstance(target, bool) else value == target


def holds(test: dict, value) -> bool:
    """Whether a test holds for a value (MISSING for a field left out)."""
    found = [k for k in COMPARISONS if k in test]
    if len(found) != 1:
        raise SpecError(f'registry: a test compares by one of {COMPARISONS}, where it is {test}')
    how, target = found[0], test[found[0]]
    if value is MISSING:
        return how == 'ne'
    if how == 'eq':
        return _same(value, target, test.get('rel_tolerance'))
    if how == 'ne':
        return not _same(value, target, test.get('rel_tolerance'))
    if how == 'any_in':
        values = value.values() if isinstance(value, dict) else [value]
        return any(v in target for v in values if isinstance(v, (str, int, float)))
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SpecError(f'registry: {test} compares a number, where the value is {value!r}')
    if how == 'lt':
        return value < target
    if how == 'gt':
        return value > target
    low, high = target
    return value < low or value > high


def evaluate(entries: list[dict], model: str, context: dict, overrides: dict | None = None) -> dict:
    """Every entry of `model` evaluated on `context` (q, world, scenario, settings): the ids checked, the entries that
    hold with their actions, the warnings, the entries that stop the run, the overridden ones with their
    justification, the unevaluated ones with what each lacks, and the overrides that stop nothing."""
    overrides = dict(overrides or {})
    out = dict(model=model, checked=[], holding=[], warnings=[], stops=[], overridden=[], unevaluated=[])
    for entry in entries:
        if model not in models(entry):
            continue
        out['checked'].append(entry['id'])
        lacking, result = None, True
        for test in entry['when']:                    # a test that fails decides, whatever another test lacks
            value = _lookup(test, context, model)
            if isinstance(value, str) and value.startswith(('quantity ', 'calibration ', "another model's")):
                lacking = lacking or value
            elif isinstance(value, float) and math.isnan(value):
                lacking = lacking or f'a value for {test} (NaN)'
            elif not holds(test, value):
                result = False
                break
        if not result:
            continue
        found = dict(id=entry['id'], action=entry['action'], state=entry['state'], assumes=entry.get('assumes', ''),
                     effect=entry.get('effect', ''))
        if lacking is not None:
            out['unevaluated'].append(dict(id=entry['id'], lacks=lacking))
            if entry['action'] == 'warn':
                continue
            found['lacks'] = lacking                  # a stopping entry the lab cannot evaluate stops the run
        else:
            out['holding'].append(found)
        if entry['action'] == 'warn':
            out['warnings'].append(found)
        elif entry['id'] in overrides:
            out['overridden'].append(dict(found, justification=overrides[entry['id']]))
        else:
            out['stops'].append(found)
    out['unused_overrides'] = sorted(set(overrides) - {e['id'] for e in out['overridden']})
    return out


def require(checks: dict, where: str) -> dict:
    """The checks, once nothing stops the run; Refused otherwise."""
    if checks['stops']:
        raise Refused(checks['stops'], where)
    return checks
