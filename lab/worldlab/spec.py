"""Specifications: load the lab's TOML files, resolve `extends`, variants and `[set]`, and hash the result.

A world lives in worlds/<world>/world.toml, a scenario in worlds/<world>/scenarios/<name>.toml (id
"<world>/<name>"), a model's defaults in configs/<model>/defaults.toml (id "<model>/defaults") and a study
in studies/<study>.toml (id "<study>"), all under the lab's root. Inside a study, GCM runs sit under
[gcm.<name>] and CM1 cases under [crm.<name>], their names local to the study. lab/design/world_spec.md states
the rules this module codes, and its section "Settled in code" records the choices made here.
"""
from __future__ import annotations

import copy
import functools
import hashlib
import json
import tomllib
from dataclasses import dataclass
from pathlib import Path

LAB = Path(__file__).resolve().parent.parent

# Fields that describe an item without changing what a model computes. They stay out of the hash, a derived
# item restates them freely, and it inherits none of them, so that a parent's description stays with the parent.
DESCRIPTIVE = frozenset({'title', 'purpose'})
IDENTITY = frozenset({'schema', 'id'})
CONTROL = frozenset({'extends', 'set', 'variants'})
# Fields that only extends and variants change: what an item is, and what its variants make it.
STRUCTURAL = IDENTITY | CONTROL | {'model', 'world', 'kind', 'patches'}
TABLES = {'gcm': 'exoplasim', 'crm': 'cm1'}
MODELS = tuple(TABLES.values())
STUDY_KEYS = frozenset({'schema', 'id', 'title', 'scenario', 'extends', *TABLES})
REGISTRY_ACTIONS = frozenset({'require-switch', 'require-build', 'require-refit', 'warn', 'refuse'})
REGISTRY_STATES = frozenset({'repaired', 'calibrated', 'bounded', 'open'})


class SpecError(ValueError):
    """A specification the lab cannot resolve unambiguously."""


def canonical(obj) -> str:
    """The form a resolved item is hashed and compared in: JSON with sorted keys, no spaces, floats as Python writes them."""
    try:
        return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise SpecError(f'a value the lab cannot hash: {error}') from None


def spec_hash(resolved: dict) -> str:
    """sha256 of a resolved item's canonical form, its top-level descriptive fields left out."""
    kept = {k: v for k, v in resolved.items() if k not in DESCRIPTIVE}
    return hashlib.sha256(canonical(kept).encode()).hexdigest()


def same(a, b) -> bool:
    """Equal as the hash sees them, so that 0 and false, or 20 and 20.0, differ."""
    return canonical(a) == canonical(b)


def get_path(tree: dict, path: str):
    """The value at a dotted path; KeyError if any part of the path is missing."""
    node = tree
    for part in path.split('.'):
        if not isinstance(node, dict) or part not in node:
            raise KeyError(path)
        node = node[part]
    return node


def set_path(tree: dict, path: str, value, *, where: str) -> None:
    """Replace the value at an existing dotted path, whole.

    The path must exist, so that a misspelt field fails, and must leave structural fields alone. A table
    that replaces a table must keep every key of the one it replaces: an unquoted dotted key in [set]
    reaches here as such a table, and would otherwise drop its neighbours silently.
    """
    parts = path.split('.')
    if parts[0] in STRUCTURAL:
        raise SpecError(f'{where}: {path!r} is structural, changed only by extends and variants')
    node = tree
    for part in parts[:-1]:
        node = node.get(part) if isinstance(node, dict) else None
        if not isinstance(node, dict):
            raise SpecError(f'{where}: path {path!r} leaves the item at {part!r}')
    if parts[-1] not in node:
        raise SpecError(f'{where}: path {path!r} names no field of the item it changes')
    old = node[parts[-1]]
    if isinstance(old, dict) and isinstance(value, dict) and set(old) - set(value):
        raise SpecError(f'{where}: {path!r} would drop {sorted(set(old) - set(value))}; '
                        f'quote a dotted path to change one field, as "{path}.{sorted(old)[0]}"')
    node[parts[-1]] = copy.deepcopy(value)


def unchosen(tree, prefix: str = '') -> list[str]:
    """The dotted paths whose value is "unchosen", which every stage reading them refuses."""
    if isinstance(tree, dict):
        return [p for k, v in tree.items() for p in unchosen(v, f'{prefix}{k}.')]
    if isinstance(tree, list):
        return [p for i, v in enumerate(tree) for p in unchosen(v, f'{prefix}{i}.')]
    return [prefix[:-1]] if tree == 'unchosen' else []


@functools.lru_cache(maxsize=256)
def _parse(data: bytes, path: str) -> dict:
    try:
        return tomllib.loads(data.decode())
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as error:
        raise SpecError(f'{path}: {error}') from None


def _read(path: Path) -> dict:
    """A parsed file, cached by its content, so that a file edited in a long-lived process reads anew."""
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        raise SpecError(f'{path}: no such specification') from None
    return copy.deepcopy(_parse(data, str(path)))


@dataclass(frozen=True)
class Item:
    """A resolved GCM run or CM1 case.

    `settings_hash` covers the item's own resolved settings alone; stage 4's product key adds the scenario
    and the upstream products' keys. `set_paths` are the paths that [set] changed along the item's chain:
    values a study states as they apply there, which CM1's scaling leaves as they are (world_spec.md, rule 9).
    """
    study: str
    name: str
    model: str
    parent: str
    settings: dict
    delta: dict
    settings_hash: str
    set_paths: frozenset = frozenset()


@dataclass(frozen=True)
class Study:
    """A resolved study: its scenario, and its GCM runs and CM1 cases by name."""
    id: str
    parent: str | None
    scenario: dict
    gcm: dict
    crm: dict


class Library:
    """The specifications under one lab root, resolved on request."""

    def __init__(self, root: Path = LAB):
        self.root = Path(root)

    # Worlds and scenarios.

    def world(self, world_id: str, _seen: tuple = ()) -> dict:
        """A world, its orbit taken from its host where it states `orbit.from_host`."""
        if world_id in _seen:
            raise SpecError(f'{world_id}: takes its orbit from itself through {" -> ".join(_seen)}')
        world = _read(self.root / 'worlds' / world_id / 'world.toml')
        _check_identity(world, 'worldlab.world/0', world_id)
        orbit = world.get('orbit', {})
        if 'from_host' in orbit:
            if set(orbit) != {'from_host'}:
                raise SpecError(f'{world_id}: states {sorted(set(orbit) - {"from_host"})} beside orbit.from_host')
            host_orbit = self.world(orbit['from_host'], _seen + (world_id,)).get('orbit', {})
            world['orbit'] = {**host_orbit, 'from_host': orbit['from_host']}
        return world

    def scenario(self, scenario_id: str) -> dict:
        """A scenario resolved through its `extends` chain."""
        return self._scenario(scenario_id, ())

    def _scenario(self, scenario_id: str, seen: tuple) -> dict:
        if scenario_id in seen:
            raise SpecError(f'{scenario_id}: extends itself through {" -> ".join(seen)}')
        world_id, sep, name = scenario_id.partition('/')
        if not sep or not name:
            raise SpecError(f'{scenario_id!r}: a scenario id is "<world>/<name>"')
        raw = _read(self.root / 'worlds' / world_id / 'scenarios' / f'{name}.toml')
        _check_identity(raw, 'worldlab.scenario/0', scenario_id)
        if 'variants' in raw:
            raise SpecError(f'{scenario_id}: a scenario changes through extends and [set]; variants belong to models')
        if 'extends' not in raw:
            if raw.get('world') != world_id:
                raise SpecError(f'{scenario_id}: world {raw.get("world")!r} differs from its folder {world_id!r}')
            return raw
        parent = self._scenario(raw['extends'], seen + (scenario_id,))
        if parent.get('world') != world_id:
            raise SpecError(f'{scenario_id}: extends a scenario of another world')
        return _derive(parent, raw, where=scenario_id, may_add=False)

    # Model defaults and studies.

    def defaults(self, defaults_id: str) -> dict:
        model, sep, rest = defaults_id.partition('/')
        if not sep or rest != 'defaults' or model not in MODELS:
            raise SpecError(f'{defaults_id!r}: a model defaults id is "<model>/defaults", for one of {MODELS}')
        raw = _read(self.root / 'configs' / model / 'defaults.toml')
        _check_identity(raw, f'worldlab.defaults.{model}/0', defaults_id)
        return raw

    def study(self, study_id: str) -> Study:
        """A study with every run and case resolved."""
        raw, parent_id = self._study_raw(study_id, ())
        if 'scenario' not in raw:
            raise SpecError(f'{study_id}: names no scenario')
        scenario = self.scenario(raw['scenario'])
        tables = {}
        for table, model in TABLES.items():
            memo = {}
            for name in raw.get(table, {}):
                self._item(study_id, raw[table], name, model, memo, ())
            tables[table] = memo
        _check_references(study_id, tables)
        return Study(study_id, parent_id, scenario, tables['gcm'], tables['crm'])

    def _study_raw(self, study_id: str, seen: tuple) -> tuple[dict, str | None]:
        """A study's own file with the runs and cases of the study it extends (world_spec.md, rule 8)."""
        if study_id in seen:
            raise SpecError(f'{study_id}: extends itself through {" -> ".join(seen)}')
        raw = _read(self.root / 'studies' / f'{study_id}.toml')
        _check_identity(raw, 'worldlab.study/0', study_id)
        unknown = set(raw) - STUDY_KEYS
        if unknown:
            raise SpecError(f'{study_id}: unknown top-level fields {sorted(unknown)}')
        parent_id = raw.get('extends')
        if parent_id is None:
            return raw, None
        parent, _ = self._study_raw(parent_id, seen + (study_id,))
        for table in TABLES:
            inherited = parent.get(table, {})
            clash = set(inherited) & set(raw.get(table, {}))
            if clash:
                raise SpecError(f'{study_id}: redefines {sorted(clash)} of {parent_id}; derive a new item instead')
            raw[table] = {**inherited, **raw.get(table, {})}
        raw.setdefault('scenario', parent['scenario'])
        return raw, parent_id

    def _item(self, study_id: str, items: dict, name: str, model: str, memo: dict, seen: tuple) -> Item:
        if name in memo:
            return memo[name]
        where = f'{study_id}:{name}'
        if name in seen:
            raise SpecError(f'{where}: extends itself through {" -> ".join(seen)}')
        raw = items[name]
        parent_id = raw.get('extends')
        if parent_id is None:
            raise SpecError(f'{where}: names no parent in `extends`')
        if raw.get('model', model) != model:
            raise SpecError(f'{where}: model {raw["model"]!r} in a table of {model} items')
        defaults = self.defaults(f'{model}/defaults')
        if '/' in parent_id:
            if parent_id != f'{model}/defaults':
                raise SpecError(f'{where}: a {model} item extends {parent_id!r}')
            parent = {k: v for k, v in defaults.items() if k not in IDENTITY | {'variants'}}
            parent.update(model=model, variants=[])
            inherited = frozenset()
        else:
            if parent_id not in items:
                raise SpecError(f'{where}: extends {parent_id!r}, which the study does not define')
            parent_item = self._item(study_id, items, parent_id, model, memo, seen + (name,))
            parent, inherited = parent_item.settings, parent_item.set_paths
        settings = _derive(parent, raw, where=where, may_add='/' in parent_id, defaults=defaults)
        added = [v for v in settings['variants'] if v not in parent['variants']]
        item = Item(study_id, name, model, parent_id, settings,
                    {'set': copy.deepcopy(raw.get('set', {})), 'variants': added}, spec_hash(settings),
                    inherited | frozenset(raw.get('set', {})))
        memo[name] = item
        return item

    # The registry of Earth assumptions.

    def registry(self) -> list[dict]:
        raw = _read(self.root / 'registry' / 'earth_assumptions.toml')
        if raw.get('schema') != 'worldlab.registry/0':
            raise SpecError(f'registry: schema {raw.get("schema")!r}')
        entries = raw.get('entry', [])
        ids = [e.get('id') for e in entries]
        if None in ids:
            raise SpecError('registry: an entry without an id')
        repeated = sorted({i for i in ids if ids.count(i) > 1})
        if repeated:
            raise SpecError(f'registry: ids repeated: {repeated}')
        for e in entries:
            if e.get('action') not in REGISTRY_ACTIONS or e.get('state') not in REGISTRY_STATES:
                raise SpecError(f'registry {e["id"]}: action {e.get("action")!r}, state {e.get("state")!r}')
            if not isinstance(e.get('when'), list):
                raise SpecError(f'registry {e["id"]}: `when` is a list of tests')
        return entries


def _check_identity(raw: dict, schema: str, item_id: str) -> None:
    if raw.get('schema') != schema:
        raise SpecError(f'{item_id}: schema {raw.get("schema")!r}, where {schema!r} is expected')
    if raw.get('id') != item_id:
        raise SpecError(f'{item_id}: its file states id {raw.get("id")!r}')


def _derive(parent: dict, raw: dict, *, where: str, may_add: bool, defaults: dict | None = None) -> dict:
    """A derived item: its parent, then its own fields, then its added variants, then its [set].

    Only an item that extends model defaults may add fields of its own, since its whole content is its
    delta; any other may restate a field only with its parent's value, unless the field is descriptive or
    names the file. Variants apply as `_apply_variants` says, and [set] comes last.
    """
    resolved = {k: copy.deepcopy(v) for k, v in parent.items() if k not in DESCRIPTIVE}
    for key, value in raw.items():
        if key in CONTROL or key in DESCRIPTIVE | IDENTITY:
            if key not in CONTROL:
                resolved[key] = copy.deepcopy(value)
            continue
        if key in resolved:
            if not same(resolved[key], value):
                raise SpecError(f'{where}: {key!r} changes its parent outside [set]')
        elif not may_add:
            raise SpecError(f'{where}: adds {key!r}, where an item derived from another changes only through [set]')
        resolved[key] = copy.deepcopy(value)
    if defaults is not None:
        _apply_variants(resolved, raw.get('variants', []), defaults, where=where)
    for path, value in raw.get('set', {}).items():
        set_path(resolved, path, value, where=where)
    return resolved


def _apply_variants(resolved: dict, added: list, defaults: dict, *, where: str) -> None:
    """Add variants to those the parent applied, in the order the model's defaults define them.

    The series are rebuilt from the defaults' patches and every applied variant, so that an item's patches
    depend on its variants alone and never on the chain that reached them. A variant may change only a
    value its parent's chain left at the defaults'; two variants that set one path differently are an error.
    """
    definitions = defaults.get('variants', {})
    unknown = [v for v in added if v not in definitions]
    if unknown:
        raise SpecError(f'{where}: variants {unknown} are not defined by the model defaults')
    before = list(resolved.get('variants', []))
    applied = set(before) | set(added)
    for name in applied:
        missing = [r for r in definitions[name].get('requires', []) if r not in applied]
        if missing:
            raise SpecError(f'{where}: variant {name!r} requires {missing}')
    setters = {}
    for name, variant in definitions.items():
        if name not in applied:
            continue
        for path, value in variant.get('set', {}).items():
            if path in setters and not same(setters[path][1], value):
                raise SpecError(f'{where}: variants {setters[path][0]!r} and {name!r} set {path!r} differently')
            setters[path] = (name, value)
            if name in before:
                continue
            try:
                current, original = get_path(resolved, path), get_path(defaults, path)
            except KeyError:
                raise SpecError(f'{where}: variant {name!r} sets {path!r}, which the defaults lack') from None
            if not same(current, original) and not same(current, value):
                raise SpecError(f'{where}: variant {name!r} would change {path!r}, which its parent already set')
            set_path(resolved, path, value, where=f'{where} variant {name}')
    series = [p for name in definitions if name in applied for p in definitions[name].get('patches', [])]
    base = defaults.get('patches')
    if series and not isinstance(base, list):
        raise SpecError(f'{where}: variants add series to defaults whose patches are {base!r}, a single series')
    if isinstance(base, list):
        resolved['patches'] = list(dict.fromkeys(base + series))
    resolved['variants'] = [v for v in definitions if v in applied]


def _check_references(study_id: str, tables: dict) -> None:
    """Each reference names an item of the right table and kind, and none closes a loop."""
    gcm, crm = tables['gcm'], tables['crm']
    starts = {}
    for name, item in gcm.items():
        source = item.settings.get('initial')
        if not isinstance(source, dict):
            continue
        origin = source.get('from')
        if origin not in gcm or origin == name:
            raise SpecError(f'{study_id}:{name}: starts from {origin!r}, which is not another run of the study')
        year, years = source.get('model_year'), gcm[origin].settings.get('model_years')
        if isinstance(years, int) and not (isinstance(year, int) and 0 <= year < years):
            raise SpecError(f'{study_id}:{name}: starts from model year {year!r} of a {years}-year run')
        starts[name] = origin
    for name in starts:
        seen, at = {name}, starts.get(name)
        while at in starts:
            if at in seen:
                raise SpecError(f'{study_id}:{name}: its starting states run in a loop')
            seen.add(at)
            at = starts[at]
    for name, item in crm.items():
        s = item.settings
        forced = s.get('forced_by')
        if forced is not None:
            if forced not in gcm:
                raise SpecError(f'{study_id}:{name}: forced_by names {forced!r}, which the study does not run')
            years, span = gcm[forced].settings.get('model_years'), s.get('reference_model_years')
            if span is not None and not (isinstance(years, int) and len(span) == 2 and 0 <= span[0] <= span[1] < years):
                raise SpecError(f'{study_id}:{name}: reference_model_years {span} outside the {years} years of {forced}')
        for label, ref in (('site.ring', s.get('site', {}).get('ring')),
                           ('day_night.from_case', s.get('day_night', {}).get('from_case'))):
            if ref is None:
                continue
            if ref not in crm or ref == name or crm[ref].settings.get('kind') != 'ring':
                raise SpecError(f'{study_id}:{name}: {label} names {ref!r}, which is not another ring of the study')
