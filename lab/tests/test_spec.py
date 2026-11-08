"""The specification loader, on the lab's seed files and on small specifications written for a test."""
import re
import shutil
import textwrap

import pytest

from worldlab.spec import LAB, Library, SpecError, get_path, spec_hash, unchosen

LIB = Library()
STUDY_HEAD = '''\
schema = "worldlab.study/0"
id = "probe"
scenario = "moon/open-moon"
'''


def _copy_lab(tmp_path):
    root = tmp_path / 'lab'
    for part in ('worlds', 'configs', 'studies', 'registry'):
        shutil.copytree(LAB / part, root / part)
    return root


def _probe(tmp_path, body, *, head=STUDY_HEAD):
    root = _copy_lab(tmp_path)
    (root / 'studies' / 'probe.toml').write_text(head + textwrap.dedent(body))
    return Library(root).study('probe')


def _refused(match):
    return pytest.raises(SpecError, match=re.escape(match))


# The seeds.

def test_every_seed_loads():
    for world in ('moon', 'earth', 'mars'):
        LIB.world(world)
    for scenario in ('moon/open-moon', 'moon/open-moon-1.0atm', 'earth/control', 'mars/breathable-1bar'):
        LIB.scenario(scenario)
    study = LIB.study('open-moon')
    assert set(study.gcm) == {'design', 'design_lw_ice'}
    assert set(study.crm) == {'ring_45n', 'ring_45n_twilight', 'box_jura'}
    assert {'A1', 'B1', 'B28', 'cm1-soil-day', 'cm1-equinox-sun', 'exoplasim-ice-weights'} <= {
        e['id'] for e in LIB.registry()}


def test_a_moon_takes_its_hosts_orbit():
    moon, earth = LIB.world('moon'), LIB.world('earth')
    assert moon['orbit'] == {**earth['orbit'], 'from_host': 'earth'}


def test_the_1_atm_extension_changes_its_set_alone():
    base, extension = LIB.scenario('moon/open-moon'), LIB.scenario('moon/open-moon-1.0atm')
    assert extension['air'].pop('surface_pressure_pa') == 101325.0
    base['air'].pop('surface_pressure_pa')
    assert extension['air'] == base['air']
    assert extension['water'] == base['water'] and extension['sunlight'] == base['sunlight']
    assert extension['world'] == 'moon' and extension['kind'] == 'crafted'


def test_the_lw_ice_pair_differs_by_its_delta():
    study = LIB.study('open-moon')
    design, lw_ice = study.gcm['design'], study.gcm['design_lw_ice']
    assert design.settings['initial'] == 'model-default'
    assert lw_ice.settings['initial'] == {'from': 'design', 'model_year': 19}
    assert (design.settings['switches']['ice_optics'], lw_ice.settings['switches']['ice_optics']) == (False, True)
    assert set(lw_ice.delta['set']) == {'initial', 'switches.longwave_correction', 'switches.ice_optics',
                                        'heating_diagnostics'}
    assert lw_ice.parent == 'design' and design.parent == 'exoplasim/defaults'
    assert lw_ice.settings['purpose'] != design.settings['purpose']   # its own description, never its parent's
    assert design.settings_hash != lw_ice.settings_hash


def test_cm1_variants_add_their_series_in_the_builds_order():
    study = LIB.study('open-moon')
    ring, twilight, box = (study.crm[n] for n in ('ring_45n', 'ring_45n_twilight', 'box_jura'))
    assert ring.settings['physics']['twilight'] == 'none' and twilight.settings['physics']['twilight'] == 'full'
    assert twilight.settings['patches'] == ['series-core', 'series-twilight'] and twilight.delta['variants'] == ['twilight']
    # The box's series apply in the order of models/cm1/builds.json: core, terrain, sea, then twilight.
    assert box.settings['patches'] == ['series-core', 'series-terrain', 'series-sea', 'series-twilight']


def test_the_study_runs_on_the_labs_own_values():
    study = LIB.study('open-moon')
    assert study.scenario['sunlight']['scale'] == 'to-reference-temperature'
    ring = study.crm['ring_45n'].settings
    assert ring['physics']['rain_size_limits'] == 'capillary' and ring['diurnal']['soil_top_layer_m'] == 0.01
    assert ring['forced_by'] == 'design' and study.crm['box_jura'].settings['site']['ring'] == 'ring_45n'


def test_the_mars_illustration_lists_its_unchosen_fields():
    assert set(unchosen(LIB.scenario('mars/breathable-1bar'))) == {
        'air.cloud_droplets_per_cm3', 'air.ozone', 'water.seas_share', 'land.albedo'}
    assert unchosen(LIB.world('mars')) == ['surface.geometry']
    assert unchosen({'a': [{'b': 'unchosen'}, 1]}) == ['a.0.b']


def test_the_registrys_field_paths_name_fields_a_seed_states():
    seeds = [LIB.world(p.parent.name) for p in (LAB / 'worlds').glob('*/world.toml')]
    seeds += [LIB.scenario(f'{p.parent.parent.name}/{p.stem}') for p in (LAB / 'worlds').glob('*/scenarios/*.toml')]
    for entry in LIB.registry():
        for test in entry['when']:
            if 'field' in test:
                assert any(_has(seed, test['field']) for seed in seeds), (entry['id'], test['field'])


def _has(tree: dict, path: str) -> bool:
    try:
        get_path(tree, path)
        return True
    except KeyError:
        return False


def test_the_registrys_config_paths_name_fields_of_the_defaults():
    for entry in LIB.registry():
        for test in entry['when']:
            if 'config' in test:
                model, _, path = test['config'].partition('.')
                get_path(LIB.defaults(f'{model}/defaults'), path)


# The hash.

def test_the_canonical_form_is_pinned():
    assert spec_hash({'b': [1.5, 'x'], 'a': 1, 'purpose': 'left out'}) == (
        '253252306831c7a53e616d2fac19ec1f21555d2c739d3366d5fa6399d3cce7be')


def test_the_hash_ignores_layout_comments_and_descriptions(tmp_path):
    root = _copy_lab(tmp_path)
    path = root / 'studies' / 'open-moon.toml'
    lines = [line.split('  #')[0].rstrip() for line in path.read_text().splitlines() if not line.startswith('#')]
    text = '\n'.join(lines).replace('purpose = "the 45 N ring on the design case"', 'purpose = "another"')
    path.write_text(text)
    before, after = LIB.study('open-moon').crm['ring_45n'], Library(root).study('open-moon').crm['ring_45n']
    assert after.settings['purpose'] == 'another' and after.settings_hash == before.settings_hash
    assert spec_hash({**before.settings, 'latitude_deg': 44.0}) != before.settings_hash


def test_variants_added_along_a_chain_resolve_as_variants_added_at_once(tmp_path):
    study = _probe(tmp_path, '''
        [crm.at_once]
        model = "cm1"
        extends = "cm1/defaults"
        variants = ["terrain", "sea", "twilight"]
        latitude_deg = 45.0

        [crm.first]
        model = "cm1"
        extends = "cm1/defaults"
        variants = ["twilight"]
        latitude_deg = 45.0

        [crm.then]
        extends = "first"
        variants = ["sea", "terrain"]
        ''')
    at_once, then = study.crm['at_once'], study.crm['then']
    assert then.settings['patches'] == at_once.settings['patches'] == [
        'series-core', 'series-terrain', 'series-sea', 'series-twilight']
    assert then.settings_hash == at_once.settings_hash and then.delta['variants'] == ['terrain', 'sea']


def test_set_paths_gather_along_a_chain_and_descriptions_stay_with_their_item(tmp_path):
    study = _probe(tmp_path, '''
        [crm.c]
        model = "cm1"
        extends = "cm1/defaults"
        latitude_deg = 45.0
        purpose = "the parent"
        set = { "diurnal.soil_top_layer_m" = 0.05 }

        [crm.d]
        extends = "c"
        set = { "unscaled.damping_base_fraction" = 0.8 }
        ''')
    c, d = study.crm['c'], study.crm['d']
    assert c.set_paths == {'diurnal.soil_top_layer_m'}
    assert d.set_paths == {'diurnal.soil_top_layer_m', 'unscaled.damping_base_fraction'}
    assert c.settings['purpose'] == 'the parent' and 'purpose' not in d.settings


# Studies that extend studies.

def test_a_study_extending_open_moon_takes_its_runs_and_cases(tmp_path):
    study = _probe(tmp_path, '', head=STUDY_HEAD.replace('scenario = "moon/open-moon"\n', 'extends = "open-moon"\n'))
    own = LIB.study('open-moon')
    assert study.parent == 'open-moon' and study.scenario == own.scenario
    for table in ('gcm', 'crm'):
        mine, theirs = getattr(study, table), getattr(own, table)
        assert set(mine) == set(theirs)
        for name in mine:
            assert mine[name].settings_hash == theirs[name].settings_hash


# Refusals.

@pytest.mark.parametrize('body, message', [
    ('[crm.c]\nmodel = "cm1"\nextends = "cm1/defaults"\nvariants = ["sea"]\n', 'requires'),
    ('[crm.c]\nmodel = "cm1"\nextends = "cm1/defaults"\nvariants = ["glacier"]\n', 'not defined'),
    ('[crm.c]\nmodel = "cm1"\nextends = "cm1/defaults"\nset = { "physics.twilight_typo" = "full" }\n', 'names no field'),
    ('[crm.c]\nmodel = "cm1"\nextends = "cm1/defaults"\nthreads = 8\n', 'outside [set]'),
    ('[crm.c]\nmodel = "cm1"\nextends = "cm1/defaults"\n[crm.d]\nextends = "c"\nsurface_output = true\n', 'adds'),
    ('[crm.c]\nmodel = "cm1"\nextends = "cm1/defaults"\nset = { "variants" = ["electrified"] }\n', 'structural'),
    ('[crm.c]\nmodel = "cm1"\nextends = "cm1/defaults"\nset = { "model" = "exoplasim" }\n', 'structural'),
    ('[crm.c]\nmodel = "cm1"\nextends = "cm1/defaults"\n[crm.c.set]\nphysics.twilight = "full"\n', 'would drop'),
    ('[gcm.g]\nmodel = "exoplasim"\nextends = "exoplasim/defaults"\nmodel_years = 20\n'
     '[gcm.h]\nextends = "g"\nmodel_years = 20.0\n', 'changes its parent'),
    ('[crm.c]\nmodel = "cm1"\nextends = "c"\n', 'extends itself'),
    ('[crm.c]\nmodel = "cm1"\nextends = "exoplasim/defaults"\n', 'a cm1 item extends'),
    ('[gcm.g]\nmodel = "exoplasim"\nextends = "exoplasim/defaults"\nmodel_years = 20\n'
     '[gcm.h]\nextends = "g"\nset = { "initial" = { from = "nowhere", model_year = 1 } }\n', 'starts from'),
    ('[gcm.g]\nmodel = "exoplasim"\nextends = "exoplasim/defaults"\nmodel_years = 20\n'
     '[gcm.h]\nextends = "g"\nset = { "initial" = { from = "g", model_year = 20 } }\n', 'model year 20'),
    ('[gcm.g]\nmodel = "exoplasim"\nextends = "exoplasim/defaults"\nmodel_years = 20\n'
     '[gcm.h]\nextends = "g"\nset = { "initial" = { from = "i", model_year = 1 } }\n'
     '[gcm.i]\nextends = "g"\nset = { "initial" = { from = "h", model_year = 1 } }\n', 'in a loop'),
    ('[gcm.g]\nmodel = "exoplasim"\nextends = "exoplasim/defaults"\nmodel_years = 20\n'
     '[crm.c]\nmodel = "cm1"\nextends = "cm1/defaults"\nforced_by = "g"\nreference_model_years = [10, 20]\n', 'outside the 20'),
    ('[crm.c]\nmodel = "cm1"\nextends = "cm1/defaults"\nforced_by = "missing"\n', 'forced_by'),
    ('[crm.c]\nmodel = "cm1"\nextends = "cm1/defaults"\nkind = "box"\nsite = { ring = "c" }\n', 'not another ring'),
    ('[cases]\n', 'unknown top-level'),
    ('[compatibility]\ngravity = "gm-over-r2"\n', 'unknown top-level'),
])
def test_ill_formed_studies_are_refused(tmp_path, body, message):
    with _refused(message):
        _probe(tmp_path, body)


def test_a_variant_may_not_change_what_its_parent_set(tmp_path):
    with _refused('would change'):
        _probe(tmp_path, '''
            [crm.c]
            model = "cm1"
            extends = "cm1/defaults"
            set = { "physics.twilight" = "half" }

            [crm.d]
            extends = "c"
            variants = ["twilight"]
            ''')


def test_variants_that_disagree_or_reach_past_the_defaults_are_refused(tmp_path):
    root = _copy_lab(tmp_path)
    defaults = root / 'configs' / 'cm1' / 'defaults.toml'
    defaults.write_text(defaults.read_text() + textwrap.dedent('''
        [variants.dark]
        set = { "physics.twilight" = "none-at-all" }

        [variants.stray]
        set = { "physics.glow" = "on" }
        '''))
    for variants, message in ((['twilight', 'dark'], 'differently'), (['stray'], 'the defaults lack')):
        (root / 'studies' / 'probe.toml').write_text(STUDY_HEAD + textwrap.dedent(f'''
            [crm.c]
            model = "cm1"
            extends = "cm1/defaults"
            variants = {variants}
            '''.replace("'", '"')))
        with _refused(message):
            Library(root).study('probe')


@pytest.mark.parametrize('edit, call, message', [
    (('studies/open-moon.toml', 'id = "open-moon"', 'id = "open-sea"'), ('study', 'open-moon'), 'states id'),
    (('worlds/earth/world.toml', 'worldlab.world/0', 'worldlab.planet/0'), ('world', 'earth'), 'schema'),
    (('worlds/moon/scenarios/open-moon-1.0atm.toml', 'extends = "moon/open-moon"', 'extends = "moon/open-moon-1.0atm"'),
     ('scenario', 'moon/open-moon-1.0atm'), 'extends itself'),
    (('worlds/moon/world.toml', 'from_host = "earth"', 'from_host = "moon"'), ('world', 'moon'), 'from itself'),
    (('worlds/moon/world.toml', 'from_host = "earth"', 'from_host = "earth"\neccentricity = 0.05'),
     ('world', 'moon'), 'beside orbit.from_host'),
    (('registry/earth_assumptions.toml', 'id = "B1"', 'id = "A1"'), ('registry',), 'repeated'),
    (('registry/earth_assumptions.toml', 'action = "require-build"', 'action = "require-a-miracle"'), ('registry',), 'action'),
    (('worlds/earth/world.toml', 'radius_m = 6371000.0', 'radius_m = '), ('world', 'earth'), 'world.toml'),
])
def test_ill_formed_files_are_refused(tmp_path, edit, call, message):
    root = _copy_lab(tmp_path)
    path, old, new = edit
    target = root / path
    text = target.read_text()
    assert old in text
    target.write_text(text.replace(old, new, 1))
    with _refused(message):
        getattr(Library(root), call[0])(*call[1:])


def test_an_unquoted_dotted_key_in_a_scenarios_set_is_refused(tmp_path):
    root = _copy_lab(tmp_path)
    path = root / 'worlds' / 'moon' / 'scenarios' / 'open-moon-1.0atm.toml'
    path.write_text(path.read_text().replace('"air.surface_pressure_pa" = 101325.0', 'air.surface_pressure_pa = 101325.0'))
    with _refused('would drop'):
        Library(root).scenario('moon/open-moon-1.0atm')
