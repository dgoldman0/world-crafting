"""The registry's checks (worldlab.registry): each comparison on its own, a field a world leaves out, and the CM1 entries a
sea box on the Open Moon meets, evaluated as the case writer and the job wrapper evaluate them."""
import json

import pytest

from worldlab import registry
from worldlab.spec import LAB, Library, SpecError, get_path

LIB = Library()
ENTRIES = LIB.registry()


def test_each_comparison_holds_as_its_name_says():
    assert registry.holds({'q': 'g', 'eq': 9.81, 'rel_tolerance': 1e-3}, 9.80665)
    assert not registry.holds({'q': 'g', 'eq': 9.81}, 9.80665)
    assert registry.holds({'q': 'g', 'ne': 9.81, 'rel_tolerance': 1e-6}, 1.62)
    assert registry.holds({'q': 'x', 'lt': 1.62}, 1.6) and not registry.holds({'q': 'x', 'lt': 1.62}, 1.6242)
    assert registry.holds({'q': 'x', 'gt': 0.01}, 0.03)
    assert registry.holds({'q': 'x', 'outside': [0.9, 1.1]}, 5.0) and not registry.holds({'q': 'x', 'outside': [0.9, 1.1]}, 1.0)
    assert registry.holds({'config': 'cm1.physics', 'any_in': ['mynn']}, {'pbl': 'mynn', 'radiation': 'rrtmg'})
    assert not registry.holds({'config': 'cm1.physics', 'any_in': ['mynn']}, {'pbl': 'cm1-simple'})
    assert registry.holds({'config': 'cm1.x', 'ne': True}, False) and not registry.holds({'config': 'cm1.x', 'ne': True}, True)
    assert registry.holds({'config': 'cm1.x', 'ne': True}, 1)            # 1 is no logical: a bool is matched as a bool
    # A field the world leaves out holds no value: ne holds, every other comparison fails.
    assert registry.holds({'field': 'rotation.locked_to', 'ne': 'star'}, registry.MISSING)
    assert not registry.holds({'field': 'rotation.locked_to', 'eq': 'star'}, registry.MISSING)
    with pytest.raises(SpecError):
        registry.holds({'q': 'x', 'gt': 1.0, 'lt': 2.0}, 1.5)
    with pytest.raises(SpecError):
        registry.holds({'q': 'x', 'gt': 1.0}, 'text')


def _context(**changes) -> dict:
    """A sea box's context on the Open Moon: CM1's defaults with Beljaars's gust over water, as the coupling study's
    boxes take it, and the box's quantities."""
    settings = json.loads(json.dumps({k: v for k, v in LIB.defaults('cm1/defaults').items() if k not in ('schema', 'id')}))
    settings['physics']['gust_over_water'] = 'beljaars'
    q = dict(gravity_m_s2=1.6242107, scale_height_over_radius=0.0302, chapman_horizon=7.2, soil_layer_ratio=1.0,
             cm1_damping_clearance_m=20800.0, lowest_level_pressure_hpa=1214.6, cm1_build_gravity_departure=0.0)
    for path, value in changes.items():
        if path in q:
            q[path] = value
        else:
            node = settings
            parts = path.split('.')
            for part in parts[:-1]:
                node = node[part]
            node[parts[-1]] = value
    return dict(q=q, world=LIB.world('moon'), scenario=LIB.scenario('moon/open-moon'), settings=settings)


def test_a_sea_box_on_the_open_moon_draws_its_warnings_and_nothing_stops_it():
    """On the Open Moon the box draws B21 (H/R 0.03), B22 (its ground at 1,215 hPa beyond RRTMG's tables) and B38
    (Earth's warm rain); A9, B1, B28, B35, the soil, the Sun, the rain's range and the damping stay silent, the case
    taking each repair or lying within each bound. ExoPlaSim's entries are left to ExoPlaSim's runs."""
    checks = registry.evaluate(ENTRIES, 'cm1', _context())
    assert [w['id'] for w in checks['warnings']] == ['B21', 'B22', 'B38']
    assert checks['stops'] == [] and checks['unevaluated'] == [] and checks['unused_overrides'] == []
    assert {'A9', 'B1', 'B28', 'B35', 'B38', 'cm1-damping-below-convection', 'cm1-rain-limits-range', 'cm1-soil-day',
            'cm1-equinox-sun', 'cm1-earth-g-schemes'} <= set(checks['checked'])
    assert 'A1' not in checks['checked'] and 'B30' not in checks['checked']
    assert registry.require(checks, 'probe') is checks


@pytest.mark.parametrize('changes, stops, warns', [
    (dict(**{'physics.pbl_per_mass': False}), ['A9'], []),
    (dict(cm1_build_gravity_departure=(9.81 - 1.6242107) / 1.6242107), ['B1'], []),
    (dict(cm1_damping_clearance_m=-500.0), ['cm1-damping-below-convection'], []),
    (dict(**{'physics.gust_over_water': 'mm5'}), [], ['B35']),
    (dict(**{'physics.rain_size_limits': 'earth'}), [], ['B28']),
    (dict(soil_layer_ratio=0.2), [], ['cm1-soil-day']),
    (dict(gravity_m_s2=1.5), [], ['cm1-rain-limits-range']),
    (dict(**{'physics.pbl': 'mynn'}), ['cm1-earth-g-schemes'], []),
])
def test_each_cm1_entry_acts_where_its_condition_holds(changes, stops, warns):
    checks = registry.evaluate(ENTRIES, 'cm1', _context(**changes))
    assert [s['id'] for s in checks['stops']] == stops
    assert set(warns) <= {w['id'] for w in checks['warnings']}
    if stops:
        with pytest.raises(registry.Refused, match=stops[0]):
            registry.require(checks, 'probe')


def test_an_override_lets_a_run_past_an_entry_and_is_kept_with_its_justification():
    checks = registry.evaluate(ENTRIES, 'cm1', _context(**{'physics.pbl_per_mass': False}),
                               {'A9': 'a test', 'B28': 'an override that stops nothing'})
    assert checks['stops'] == [] and checks['overridden'][0]['id'] == 'A9'
    assert checks['overridden'][0]['justification'] == 'a test' and checks['unused_overrides'] == ['B28']


def test_an_entry_whose_quantity_the_run_lacks_is_reported_unevaluated():
    ctx = _context()
    del ctx['q']['soil_layer_ratio']
    checks = registry.evaluate(ENTRIES, 'cm1', ctx)
    assert checks['unevaluated'] == [dict(id='cm1-soil-day', lacks='quantity soil_layer_ratio')]


def test_a9_and_b35_stand_with_their_repairs_and_the_defaults_hold_their_settings():
    """A9 requires the boundary layer's fix wherever the simple boundary layer runs, so CM1's defaults take it on;
    B35 warns of the MM5 gust over water off Earth's gravity, the fix opt-in until the Earth control's test. B1 tests
    the build's compiled gravity against the world's, so a build that compiles the world's in passes, and a build told
    the world by its namelist stays refused until plan stage 3's checks make it require-switch."""
    entries = {e['id']: e for e in ENTRIES}
    a9, b35, b1 = entries['A9'], entries['B35'], entries['B1']
    patches = LAB.parent / 'models' / 'cm1' / 'patches'
    assert (a9['state'], a9['action']) == ('repaired', 'require-switch')
    assert (b35['state'], b35['action']) == ('repaired', 'warn')
    for entry, switch in ((a9, 'ipbl2_per_mass'), (b35, 'gust_over_water')):
        assert entry['repair']['switch'] == switch and (patches / (entry['repair']['patch'] + '.patch')).exists()
        assert (entry['repair']['value'], entry['repair']['default']) == (1, 0)
    defaults = LIB.defaults('cm1/defaults')
    assert get_path(defaults, 'physics.pbl_per_mass') is True and get_path(defaults, 'physics.gust_over_water') == 'mm5'
    assert b1['when'][1] == {'q': 'cm1_build_gravity_departure', 'gt': 1e-6} and b1['action'] == 'require-build'


def test_a_stopping_entry_the_context_cannot_evaluate_stops_the_run_unless_overridden():
    """A refusing or requiring entry whose quantity the context lacks, or holds as NaN, stops the run as one that holds
    would, since the lab can show neither that it holds nor that it fails; an override lets the run past it, and a
    test that fails decides the entry whatever another test lacks."""
    ctx = _context()
    del ctx['q']['cm1_damping_clearance_m']
    checks = registry.evaluate(ENTRIES, 'cm1', ctx)
    assert [(s['id'], s['lacks']) for s in checks['stops']] == [('cm1-damping-below-convection',
                                                                  'quantity cm1_damping_clearance_m')]
    with pytest.raises(registry.Refused, match='unevaluated, lacking quantity cm1_damping_clearance_m'):
        registry.require(checks, 'probe')
    assert registry.evaluate(ENTRIES, 'cm1', ctx, {'cm1-damping-below-convection': 'a test'})['stops'] == []
    nan = _context(cm1_build_gravity_departure=float('nan'))
    assert [s['id'] for s in registry.evaluate(ENTRIES, 'cm1', nan)['stops']] == ['B1']
    # B1's first test fails at Earth's gravity, so the entry holds nothing whatever its second lacks.
    earth = _context(gravity_m_s2=9.81, cm1_build_gravity_departure=float('nan'))
    assert registry.evaluate(ENTRIES, 'cm1', earth)['stops'] == []
