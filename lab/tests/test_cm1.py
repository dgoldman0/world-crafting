"""CM1's case writer (worldlab.cm1): its grid, its namelist, its values from the lab's derivations, its refusals, and,
where Terluna's research drive holds the design run, the coupling study's cases written from that run read in place:
their files and entries against gcm_site's and derive's, the comparison with Terluna's recorded sea boxes, each
difference with its cause, and a tiny box run by the lab's own CM1 build where the store holds it."""
import json
import math
import shutil
import textwrap
from pathlib import Path

import numpy as np
import pytest

from worldlab import cm1, cm1_builds, derive, jobs, registry, stages
from worldlab.data import DataError
from worldlab.roots import root
from worldlab.spec import LAB, Library, SpecError

LIB = Library()
STORE = root('store')
STUDY = 'open-moon-couplings'
HEAD = 'schema = "worldlab.study/0"\nid = "probe"\nscenario = "moon/open-moon"\n'
RUN = 'A28R_301k_design_l15_snow_s938_turned_refit_precession'      # the coupling study's forcing run
BOX = f'''
[crm.box]
model = "cm1"
extends = "cm1/defaults"
forcing_run = "terluna-drive:gcm-runs/{RUN}"
reference_model_years = [10, 49]
kind = "box"
solar_longitude_deg = 0.0
site = {{ lat_deg = -9.24, lon_deg = -52.01, half_lat_deg = 5.6, half_lon_deg = 8.5, surface = "sea" }}
columns = {{ nx = 32, ny = 32 }}
'''
SEASON = '"coupling.reference_season" = "year"\n"coupling.reference_season_reason" = "a probe"\n'


def _probe(tmp_path, body, *, season=True) -> Library:
    """A study of one box, `box`, its whole years' mean stated with a reason unless `season` is false."""
    root_ = tmp_path / 'lab'
    for part in ('worlds', 'configs', 'studies', 'registry', 'data'):
        shutil.copytree(LAB / part, root_ / part)
    body = textwrap.dedent(body)
    if season:
        body = body.replace('[crm.box.set]\n', '[crm.box.set]\n' + SEASON) if '[crm.box.set]\n' in body \
            else body + '\n[crm.box.set]\n' + SEASON
    (root_ / 'studies' / 'probe.toml').write_text(HEAD + body)
    return Library(root_)


# The grid and the namelist.

def test_the_vertical_grid_is_terlunas_at_its_values():
    zw = cm1.vertical_grid(100.0, 1000.0, 1.08, 2000.0, 150000.0)
    assert len(zw) == 112 and zw[0] == 0.0 and zw[-1] == 150000.0 and zw[1] == 100.0 and zw[10] == 1000.0
    assert np.allclose(np.diff(zw)[-5:-1], 2000.0) and 0.5 * 2000.0 <= zw[-1] - zw[-2] <= 2000.0
    drive = root('terluna-drive')
    grid = None if drive is None else drive / 'crm-runs' / 'box_near_side_sea_design_years' / 'input_grid_z'
    if grid is not None and grid.exists():
        assert np.allclose(zw, np.loadtxt(grid), atol=1.0e-3)
    with pytest.raises(SpecError):
        cm1.vertical_grid(0.0, 1000.0, 1.08, 2000.0, 150000.0)


def test_entries_are_set_in_place_or_added_to_their_section():
    text = ' &param1\n dx = 1.0,\n dtl = 2.0,\n /\n &param3\n kdiv = 0.10,\n /\n'
    out = cm1.set_entries(text, dict(param1=dict(dx=6000.03, run_time=-999.9), param3=dict(world_g=1.6242107,
                                                                                            ipbl2_per_mass=1,
                                                                                            dodomaindiag=True)))
    found = cm1.entries_of(out)
    assert found['param1'] == dict(dx='6000.03', dtl='2.0', run_time='-999.9')
    assert found['param3'] == dict(kdiv='0.10', world_g='1.6242107', ipbl2_per_mass='1', dodomaindiag='.true.')
    with pytest.raises(SpecError, match='&param9'):
        cm1.set_entries(text, dict(param9=dict(x=1)))
    with pytest.raises(SpecError):
        cm1.fortran(float('nan'))


# The values.

def test_a_box_takes_the_lab_derivations_and_the_defaults_scaled_by_rule_9():
    v = cm1.values(LIB, STUDY, 'sea_imposed')
    moon, scenario = LIB.world('moon'), LIB.scenario('moon/open-moon')
    f = derive.cm1_factors(moon, scenario, LIB.defaults('cm1/defaults'))
    assert v['factors'] == f and f['length'] == pytest.approx(1.0 + 5.05e-6, abs=2e-8)
    assert v['scaled']['column_target_m'] == 6000.0 * f['length'] and v['scaled']['time_step_s'] == 40.0 * f['time']
    assert v['scaled']['rayleigh_rate_per_s'] == pytest.approx(0.0005518922448388763 * f['rate'], rel=1e-15)
    assert len(v['zw']) == 112 and v['zw'][-1] == pytest.approx(150000.0 * f['length'], rel=1e-12)
    # Four solar days of 29.53059 d, cut to the last of 236 whole restarts of 12 hours.
    assert v['solar_day_s'] == 29.53059 * 86400.0 and v['length_s'] == 236 * 43200.0
    assert (v['start_hour_deg'], v['declination_deg']) == (-90.0, 0.0)
    assert v['soil_dz1_m'] == pytest.approx(0.01 * math.sqrt(29.53059), rel=1e-12)
    assert v['coriolis'] == pytest.approx(2.0 * derive.rotation_rate(moon) * math.sin(math.radians(-9.24)), rel=1e-15)
    air = derive.mole_fractions(scenario)
    assert v['macros'] == cm1_builds.world_macros(derive.gravity(moon), air['CO2'], air['O2'])
    assert v['build_gravity_m_s2'] == derive.gravity(moon)


def test_a_case_told_its_world_by_the_namelist_compiles_none_and_meets_b1(tmp_path):
    lib = _probe(tmp_path, BOX + '[crm.box.set]\n"world_constants" = "namelist"\n')
    v = cm1.values(lib, 'probe', 'box')
    assert v['macros'] == {} and v['build_gravity_m_s2'] == 9.81


def test_a_value_the_study_sets_and_the_same_value_scaled_give_two_keys(tmp_path):
    """Rule 9 leaves a value the study sets unscaled, so a case that sets the defaults' 6000.0 m hands CM1 6000.0 m
    where its parent hands it 6000.03; their settings hash alike, and the read set, which holds the scaled values and
    the paths the study sets, tells them apart."""
    lib = _probe(tmp_path, BOX + """
        [crm.set_width]
        extends = "box"

        [crm.set_width.set]
        "scaled_length.column_target_m" = 6000.0
        """)
    plain, fixed = cm1.values(lib, 'probe', 'box'), cm1.values(lib, 'probe', 'set_width')
    assert plain['item'].settings_hash == fixed['item'].settings_hash
    assert fixed['scaled']['column_target_m'] == 6000.0 < plain['scaled']['column_target_m']
    assert plain['read_set'] != fixed['read_set'] and 'scaled_length.column_target_m' in fixed['read_set']['set_paths']
    if root('terluna-drive') is not None and STORE is not None:
        store = _seeded(tmp_path / 'store')
        assert cm1.case_key(lib, 'probe', 'box', store=store)['key'] != \
            cm1.case_key(lib, 'probe', 'set_width', store=store)['key']


def test_the_season_window_waits_and_the_years_mean_states_its_reason(tmp_path):
    with pytest.raises(SpecError, match="'window' .* waits for a reading of each record's solar longitude"):
        cm1.values(_probe(tmp_path / 'a', BOX, season=False), 'probe', 'box')
    lib = _probe(tmp_path / 'b', BOX + '[crm.box.set]\n"coupling.reference_season" = "year"\n', season=False)
    with pytest.raises(SpecError, match='reference_season_reason'):
        cm1.values(lib, 'probe', 'box')


def test_the_namelist_carries_the_world_where_the_build_compiles_none(tmp_path):
    """Told its world by the namelist, a case writes the world's gravity, CO2 and O2 into &param3 as the lab derives
    them; compiled in, it writes none."""
    inputs = dict(namelist=dict(param3={}, param8={}, param19={}))
    rain = dict(entries={})
    for world, expected in (('namelist', True), ('build', False)):
        lib = _probe(tmp_path / world, BOX + f'[crm.box.set]\n"world_constants" = "{world}"\n')
        v = cm1.values(lib, 'probe', 'box')
        entries = cm1.namelist_entries(v, inputs, rain, 300.0, 1158.665)['param3']
        if expected:
            air = derive.mole_fractions(lib.scenario('moon/open-moon'))
            assert (entries['world_g'], entries['world_co2'], entries['world_o2']) == \
                (derive.gravity(lib.world('moon')), air['CO2'], air['O2'])
            text = cm1.set_entries(cm1.template(), dict(param3=entries))
            assert cm1.entries_of(text)['param3']['world_g'] == repr(derive.gravity(lib.world('moon')))
        else:
            assert not {'world_g', 'world_co2', 'world_o2'} & set(entries)


@pytest.mark.parametrize('limits, law, warm, expected', [
    ('earth', 'morrison', 'earth', dict(brkup_db=3.0e-4, brkup_gscale=0, rain_fall_law=0)),
    ('breakup-only', 'morrison', 'earth', dict(brkup_db=3.0e-4 * math.sqrt(9.81 / 1.6242107), brkup_gscale=0,
                                               rain_fall_law=0)),
    ('earth', 'morrison', 'gravity', dict(brkup_db=3.0e-4, brkup_gscale=0, rain_fall_law=0,
                                         rain_autoconv_fac=1.6242107 / 9.81, rain_accr_fac=(1.6242107 / 9.81) ** 0.6)),
])
def test_the_rain_entries_follow_the_cases_limits_law_and_warm_rain(tmp_path, limits, law, warm, expected):
    lib = _probe(tmp_path, BOX + f'[crm.box.set]\n"physics.rain_size_limits" = "{limits}"\n'
                                 f'"physics.rain_fall_law" = "{law}"\n"physics.warm_rain_rates" = "{warm}"\n')
    found = cm1.rain(cm1.values(lib, 'probe', 'box'), None)
    assert set(found['entries']) == set(expected) and found['table'] is None
    for key, value in expected.items():
        assert found['entries'][key] == pytest.approx(value, rel=2e-6), key


def test_the_producer_holds_every_module_and_constant_the_writer_computes_with():
    """In a fresh interpreter, the repository's modules under python/ that the writer's tools import, and the
    constants they read, are all in the case's producer, so that a change to any of them changes the case's key."""
    import subprocess
    import sys
    code = (f'import sys; sys.path[:0] = {[str(LAB), str(LAB.parent / "python")]!r}\n'
            'from climate.crm import gcm_site; from climate.gcm import year_files\n'
            'from atmosphere.rain import fall_law, warm_rain, drops, breakup, morrison\n'
            'print("\\n".join(m.__file__ for m in list(sys.modules.values()) if getattr(m, "__file__", None)))\n')
    files = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, check=True).stdout.split()
    python = (LAB.parent / 'python').resolve()
    ours = {Path(f).resolve() for f in files if Path(f).resolve().is_relative_to(python)}
    producer = {Path(f).resolve() for f in cm1.PRODUCER}
    missing = sorted(str(f.relative_to(python)) for f in ours - producer if f.name != '__init__.py')
    assert missing == [] and (python / 'shared' / 'constants.json') in producer


@pytest.mark.parametrize('body, match', [
    (BOX.replace('kind = "box"', 'kind = "ring"'), 'rings wait'),
    (BOX.replace('surface = "sea"', 'surface = "land"'), 'over the sea'),
    (BOX + 'variants = ["twilight"]\n', 'variants'),
    (BOX.replace(f'forcing_run = "terluna-drive:gcm-runs/{RUN}"', 'forced_by = "design"')
     + '\n[gcm.design]\nmodel = "exoplasim"\nextends = "exoplasim/defaults"\nmodel_years = 50\n', 'block 3'),
    (BOX + '[crm.box.set]\n"physics.rain_fall_law" = "world"\n"physics.rain_size_limits" = "earth"\n', 'capillary'),
    (BOX + '[crm.box.set]\n"physics.microphysics" = "nssl-2mom-elec"\n', 'morrison'),
    (BOX + '[crm.box.set]\n"unscaled.segment_s" = 2700.0\n', 'no whole number of restart intervals'),
    (BOX + '[crm.box.set]\n"unscaled.output_s" = 7000.0\n', 'divides no segment'),
    (BOX + '[crm.box.set]\n"unscaled.stats_s" = 0.0\n', 'positive'),
])
def test_what_the_thin_path_cannot_write_is_refused(tmp_path, body, match):
    lib = _probe(tmp_path, body)
    with pytest.raises((SpecError, DataError), match=match):
        if 'forced_by' in body:
            cm1.case_key(lib, 'probe', 'box', store=tmp_path / 'store')
        else:
            cm1.values(lib, 'probe', 'box')


# The cases written from Terluna's present design climate, read in place.

def _drive():
    drive = root('terluna-drive')
    if drive is None:
        pytest.skip("Terluna's research drive is absent")
    if not (drive / 'gcm-runs' / RUN / 'model' / 'MOST.00049.nc').exists():
        pytest.skip("Terluna's turned design run is absent from the drive")
    pytest.importorskip('netCDF4')
    return drive


def _seeded(store: Path) -> Path:
    """A store for a test, its caches of the forcing taken from the lab's store where it holds them."""
    for kind in ('gcm-site', 'gcm-mode'):
        source = None if STORE is None else STORE / 'caches' / kind
        if source is not None and source.is_dir():
            shutil.copytree(source, store / 'caches' / kind, dirs_exist_ok=True)
    if STORE is not None and (STORE / stages.DIGESTS).is_file():          # the year files' digests, by size and time
        (store / stages.DIGESTS).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(STORE / stages.DIGESTS, store / stages.DIGESTS)
    return store


@pytest.fixture(scope='module')
def written(tmp_path_factory):
    """The coupling study's imposed and wave boxes written into a store of the test's, with gcm_site's own inputs for
    each from the same forcing."""
    from climate.crm import gcm_site as gs
    _drive()
    store = _seeded(tmp_path_factory.mktemp('store'))
    out = dict(store=store)
    for name in ('sea_imposed', 'sea_dgw', 'sea_dgw_planet'):
        folder = cm1.write_case(LIB, STUDY, name, store=store)
        case = cm1.checked(folder)
        a = cm1.assess(LIB, STUDY, name, store=store)
        v, f = a['keyed']['values'], a['forcing']
        air = gs.reference_air(f, v['gravity_m_s2'], v['zw'][-1])
        coupling = cm1.coupling_of(v)
        if coupling['coupling'] == 'dgw':
            coupling['mode'] = cm1.first_mode(a['run'], (10, 49), store=store, files=a['files'])
        own = gs.case_inputs(f, v['zw'], air, gravity_m_s2=v['gravity_m_s2'], start_hour_deg=v['start_hour_deg'],
                             solar_day_s=v['solar_day_s'], length_s=v['solar_day_s'],
                             damping_base_m=0.77 * v['zw'][-1], nudge_tau_s=259200.0, **coupling)
        out[name] = dict(folder=folder, case=case, values=v, forcing=f, gcm_site=own,
                         namelist=cm1.entries_of((folder / 'namelist.template').read_text()))
    return out


def _number(text: str):
    return float(text.replace('d', 'e'))


def test_the_cases_files_and_entries_are_gcm_sites(written):
    """The case carries gcm_site's forcing as gcm_site writes it: the vertical wind, the table, one solar day of
    windows, and its entries of &param3, &param8 and &param19."""
    for name in ('sea_imposed', 'sea_dgw'):
        w = written[name]
        folder, own, entries = w['folder'], w['gcm_site'], w['namelist']
        for file in (gs_file for gs_file in own['files'] if not gs_file.startswith('lsnudge')):
            assert (folder / file).read_text() == own['files'][file], file
        day = sorted((folder / cm1.WINDOWS).glob('lsnudge_*.dat'))
        assert len(day) == 36 and all(p.read_text() == own['files'][p.name] for p in day)
        for section in ('param3', 'param8', 'param19'):
            for key, value in own['namelist'][section].items():
                found = entries[section][key]
                if isinstance(value, bool):
                    assert found == ('.true.' if value else '.false.'), (name, key)
                else:
                    assert _number(found) == value, (name, section, key)
    dgw = written['sea_dgw']['namelist']['param3']
    assert int(dgw['lsw_coupling']) == 1 and int(dgw['lsw_table_heat']) == 1
    assert 'lsw_coupling' not in written['sea_imposed']['namelist']['param3']


def test_the_wave_stands_for_the_sites_footprint_or_the_planets_radius(written):
    """The wave's time is the length the box stands for over the first mode's speed: the site's footprint for the wave
    box, about 2.8 hours, and the Moon's radius for the box at the planet's scale, about 11.8 hours."""
    from climate.crm import gcm_site as gs
    mode = written['sea_dgw']['case']['record']['coupling']['mode']
    footprint = gs.footprint_m(gs.TERLUNA_OPEN_MOON_SITES['near_side_sea_turned'],
                               written['sea_dgw']['forcing']['gcm']['radius_m'])
    tau = lambda name: _number(written[name]['namelist']['param3']['lsw_tau'])
    assert tau('sea_dgw') == round(footprint / mode['c_m_s'], 1) and 2.6 < tau('sea_dgw') / 3600.0 < 3.0
    assert tau('sea_dgw_planet') == round(1737400.0 / mode['c_m_s'], 1) and 11.5 < tau('sea_dgw_planet') / 3600.0 < 12.0
    assert written['sea_dgw_planet']['case']['record']['coupling']['passed']['coupling_length_m'] == 1737400.0


def test_the_cases_values_are_derives(written):
    """The grid, step, damping, boundary layer, soil, Sun and Coriolis parameter the namelist holds are the lab's
    derivations; the world's gravity and air are compiled into the build (world_constants "build"), so the namelist
    states none; the box takes the forcing run's sunlight."""
    w = written['sea_imposed']
    v, e = w['values'], w['namelist']
    assert _number(e['param1']['dx']) == v['scaled']['column_target_m'] == _number(e['param1']['dy'])
    assert _number(e['param1']['dtl']) == v['scaled']['time_step_s'] and _number(e['param1']['timax']) == v['length_s']
    assert _number(e['param3']['rdalpha']) == v['scaled']['rayleigh_rate_per_s']
    assert _number(e['param3']['l_inf']) == v['scaled']['pbl_length_m']
    assert _number(e['param3']['zd']) == 0.77 * v['zw'][-1] and _number(e['param6']['ztop']) == v['zw'][-1]
    assert _number(e['param3']['soil_dz1']) == v['soil_dz1_m'] and _number(e['param3']['sun_decl']) == 0.0
    assert _number(e['param3']['fcor']) == pytest.approx(v['coriolis'], rel=1e-6)
    assert int(e['param3']['ipbl2_per_mass']) == 1 and int(e['param3']['gust_over_water']) == 1
    assert int(e['param0']['nz']) == 111 and np.allclose(np.loadtxt(w['folder'] / 'input_grid_z'), v['zw'], atol=6e-4)
    assert not {'world_g', 'world_co2', 'world_o2'} & set(e['param3'])
    assert _number(e['param8']['var17']) == 1158.665 and _number(e['param8']['var18']) == -90.0
    assert _number(e['param12']['tsk0']) == round(w['forcing']['surface']['ground_k'], 3)
    record = w['case']['record']
    assert record['build']['macros'] == v['macros'] and record['values']['sunlight_w_m2'] == 1158.6652768232743


def test_the_rain_follows_the_sites_air_at_2_m(written):
    """The capillary limits and the world's fall law take the entries fall_law.settings computes from the site's air at
    2 m, and the table it writes."""
    from atmosphere.rain import fall_law
    w = written['sea_imposed']
    found = fall_law.settings(cm1.site_column(w['values'], w['forcing'])['column'])
    e = w['namelist']['param3']
    for key in ('brkup_rhor', 'brkup_rhoexp', 'rain_selfcoll'):
        assert _number(e[key]) == found['namelist'][key], key
    assert int(e['brkup_gscale']) == 1 and int(e['rain_fall_law']) == 1 and _number(e['brkup_db']) == 3.0e-4
    assert (w['folder'] / cm1.RAIN_TABLE).read_text() == fall_law.table_text(found['table'])


def test_the_case_records_its_key_inputs_and_the_registrys_checks(written):
    case = written['sea_imposed']['case']
    h = case['header']
    assert h['schema'] == cm1.SCHEMA and written['sea_imposed']['folder'].name == f"cm1-{h['key'][:16]}"
    assert [w['id'] for w in h['registry']['warnings']] == ['B21', 'B22', 'B38'] and h['registry']['stops'] == []
    assert h['registry_context']['q']['cm1_damping_clearance_m'] > 0.0
    files = h['inputs']['forcing']['files']
    assert len([n for n in files if n.startswith('model/MOST.')]) == 40 and 'model/MOST.00049.nc' in files
    assert h['inputs']['build'] == case['record']['build']['key'] and h['inputs']['forcing']['years'] == [10, 49]
    # The forcing averages every record of the forty years, 118 of each year file's 120 by the rule of defect A10, and
    # the case states why it takes the whole years' mean.
    season = case['record']['forcing']['season']
    assert season['reference'] == 'year' and season['records'] == 40 * 118 and 'declination' in season['reason']
    assert set(h['files']) >= {'namelist.template', 'input_sounding', 'input_grid_z', 'terluna_surface.txt',
                               'terluna_wls.txt', 'terluna_lsadv.txt', cm1.RAIN_TABLE, 'windows/lsnudge_0036.dat'}
    assert stages.named(written['store'], STUDY, 'sea_imposed') == written['sea_imposed']['folder']
    # Written again, the case is the one in the store.
    assert cm1.write_case(LIB, STUDY, 'sea_imposed', store=written['store']) == written['sea_imposed']['folder']


def test_the_imposed_box_differs_from_terlunas_turned_sea_box_by_its_causes(written):
    """Against Terluna's box_near_side_sea_turned, read in place, each entry of &param0 to &param3, &param8, &param12 and
    &param19 that both state either agrees or differs by a stated cause. Terluna's box was forced by the turned run of
    an earlier sunlight (A28R_301k_design_l15_snow_s924_turned_refit, years 10-49), the lab's by the present design
    climate (s938_turned_refit_precession, the same years and site), so the forcing's own values differ besides the
    lab's choices."""
    drive = _drive()
    folder = drive / 'crm-runs' / 'box_near_side_sea_turned'
    if not (folder / 'namelist.template').exists():
        pytest.skip("Terluna's box_near_side_sea_turned is absent from the drive")
    causes = {
        ('param1', 'dx'): "Terluna's width is an equatorial ring's of 8 ranks, 6,011.237 m; the lab's the defaults' "
                          '6 km scaled by rule 9',
        ('param1', 'dy'): 'as dx',
        ('param1', 'dtl'): "the lab's step is 40 s scaled by rule 9, the spin term's 5 parts per million",
        ('param1', 'timax'): 'four solar days cut to whole restarts, where Terluna ran 59.06 days',
        ('param1', 'dz'): 'the top scaled by rule 9',
        ('param3', 'rdalpha'): "Terluna's rounded to 8 places; the lab's scaled by rule 9",
        ('param3', 'l_inf'): "Terluna's rounded to 0.1 m; the lab's scaled by rule 9",
        ('param3', 'zd'): 'the top scaled by rule 9',
        ('param3', 'brkup_rhor'): "the forcing run's surface pressure at the site, over 1013.25 hPa",
        ('param3', 'brkup_rhoexp'): "the site's air at 2 m from the forcing run, where Terluna took its resort climate "
                                    'at 300.4 K and 61%',
        ('param3', 'rain_selfcoll'): 'as brkup_rhoexp',
        ('param3', 'brkup_db'): 'the same 300 um, written as 3e-4',
        ('param6', 'ztop'): 'the top scaled by rule 9',
        ('param8', 'var14'): "the forcing run's convection top, in the run's own gas constant, 0.47% above CM1's",
        ('param8', 'var15'): 'as var14',
        ('param8', 'var17'): "the forcing run's sunlight: s938's 1,158.665 W/m2 against s924's 1,141.372",
        ('param8', 'var20'): "the thin path's build holds no twilight series",
        ('param8', 'var7'): "Terluna's slot of the inflow, now inflow_ref_air (patch 09)",
        ('param8', 'var8'): "Terluna's slot of the pull's height, now wind_nudge_zmin (patch 09)",
        ('param8', 'var10'): "Terluna's slot of the wind's time, now wind_nudge_tau (patch 09)",
        ('param12', 'tsk0'): "the forcing run's sea at the site",
        ('param12', 'tmn0'): 'as tsk0',
        ('param0', 'ppnode'): "an MPI setting, which the OpenMP build leaves unread; the lab keeps the template's",
    }
    theirs = cm1.entries_of((folder / 'namelist.template').read_text())
    mine = written['sea_imposed']['namelist']
    seen, same_keys = set(), set()
    for section in ('param0', 'param1', 'param2', 'param3', 'param8', 'param12', 'param19'):
        for key in set(theirs[section]) & set(mine[section]):
            a, b = mine[section][key], theirs[section][key]
            try:
                same = math.isclose(_number(a), _number(b), rel_tol=1e-9, abs_tol=1e-12)
            except ValueError:
                same = a.lower() == b.lower()
            if same:
                same_keys.add((section, key))
            else:
                assert (section, key) in causes, (section, key, a, b)
                seen.add((section, key))
    assert {('param1', 'dx'), ('param8', 'var14'), ('param8', 'var17'), ('param12', 'tsk0')} <= seen
    # The site, the start at sunrise, the Coriolis parameter, the solar day and the grid's levels are Terluna's.
    assert {('param3', 'fcor'), ('param8', 'var18'), ('param8', 'var19'), ('param0', 'nz'), ('param0', 'nx')} <= same_keys
    assert written['sea_imposed']['forcing']['cells'] == json.loads((folder / 'case.json').read_text())['gcm_site']['cells']
    # The sounding starts at the forcing run's own surface pressure.
    first = [float(x) for x in (written['sea_imposed']['folder'] / 'input_sounding').read_text().split()[:3]]
    assert first[0] == round(written['sea_imposed']['forcing']['surface']['pressure_pa'] / 100.0, 4)


def test_a_reference_from_another_cases_run_is_keyed_by_the_days_it_reads(tmp_path):
    """A wave measured against another box's own domain mean takes into its key that box's key and the domain means
    within the reference's days, with the files that lay them out and set the box's clock; a domain mean outside the
    days leaves the key as it was."""
    _drive()
    lib = _probe(tmp_path, BOX + """
        [crm.wave]
        extends = "box"

        [crm.wave.set]
        "coupling.vertical_wind" = "dgw"
        "coupling.coupled_reference" = { from_case = "box", solar_days = [0.0, 0.01] }
        """)
    store = _seeded(tmp_path / 'store')
    other = cm1.case_key(lib, 'probe', 'box', store=store)['key']
    run = jobs.folder(store, other)
    run.mkdir(parents=True)
    stages.write_json(run / jobs.RECORD, dict(segments=[dict(end_s=30000.0)]))
    (run / 'namelist.template').write_text(' &param8\n var18 = -90.0,\n var19 = 2551443.0,\n /\n')
    (run / 'cm1out_diag_s.ctl').write_text('vars 1\nmtime 0 99 time\nendvars\n')
    for k in range(1, 7):
        (run / f'cm1out_diag_{k:06d}_s.dat').write_bytes(bytes([k]))
    found = cm1.upstream_reference(cm1.values(lib, 'probe', 'wave'), lib, store)
    # Solar days 0 to 0.01 reach 25,514 s, so the domain means at 10,800 and 21,600 s, files 2 and 3, are read.
    assert set(found['files']) == {'cm1out_diag_000002_s.dat', 'cm1out_diag_000003_s.dat', 'cm1out_diag_s.ctl',
                                   'namelist.template'} and found['key'] == other
    key = cm1.case_key(lib, 'probe', 'wave', store=store)['key']
    (run / 'cm1out_diag_000005_s.dat').write_bytes(b'changed')
    assert cm1.case_key(lib, 'probe', 'wave', store=store)['key'] == key
    (run / 'cm1out_diag_000002_s.dat').write_bytes(b'changed')
    assert cm1.case_key(lib, 'probe', 'wave', store=store)['key'] != key


def test_the_weak_temperature_gradient_writes_and_the_self_test_waits_on_its_upstream_run(written):
    """With patch 11 in CM1's series the gradient's box writes lsw_coupling 2 with the least stability scaled by the
    Moon's gravity and no mode speed, every forced box holds the nudging's window by the step's time (patch 12), a floor
    stated for another coupling is refused, and the wave against the imposed box's own mean waits on that box's run."""
    import copy
    folder = cm1.write_case(LIB, STUDY, 'sea_wtg', store=written['store'])
    p3 = cm1.entries_of((folder / 'namelist.template').read_text())['param3']
    assert int(p3['lsw_coupling']) == 2 and _number(p3.get('lsw_mode_speed', '0.0')) == 0.0
    assert _number(p3['lsw_stab_min']) == pytest.approx(1.0e-5 * 1.6242 / 9.81, rel=1e-2)
    assert int(p3['nudge_window_by_time']) == 1
    assert all(int(written[name]['namelist']['param3']['nudge_window_by_time']) == 1
               for name in ('sea_imposed', 'sea_dgw', 'sea_dgw_planet'))
    v = copy.deepcopy(written['sea_dgw']['values'])
    v['settings']['coupling']['coupled_stability_floor'] = 2.0e-6
    with pytest.raises(SpecError, match='coupled_stability_floor acts with the weak temperature gradient'):
        cm1.coupling_of(v)
    v['settings']['coupling']['vertical_wind'] = 'wtg'
    assert cm1.coupling_of(v)['coupling_stability_min_k_m'] == 2.0e-6
    v['settings']['coupling']['nudge_window'] = 'sometimes'
    with pytest.raises(SpecError, match='coupling.nudge_window is one of'):
        cm1.nudge_window(v)
    with pytest.raises(DataError, match="sea_imposed's domain mean over solar days 2.0-4.0"):
        cm1.write_case(LIB, STUDY, 'sea_dgw_self', store=written['store'])


def test_a_case_the_registry_stops_is_written_only_with_an_override(tmp_path):
    _drive()
    lib = _probe(tmp_path, BOX + '[crm.box.set]\n"physics.pbl_per_mass" = false\n')
    store = _seeded(tmp_path / 'store')
    with pytest.raises(registry.Refused, match='A9'):
        cm1.write_case(lib, 'probe', 'box', store=store)
    assert not (store / 'cases').exists()
    folder = cm1.write_case(lib, 'probe', 'box', store=store, overrides={'A9': 'a test of the override'})
    header = cm1.checked(folder)['header']
    assert header['overrides'] == {'A9': 'a test of the override'}
    assert [o['id'] for o in header['registry']['overridden']] == ['A9']


# The lab's own CM1 build on a tiny box: the case's files as CM1 reads them.

TINY = BOX.replace('columns = { nx = 32, ny = 32 }', 'columns = { nx = 4, ny = 4 }') + '''
[crm.box.set]
"unscaled.restart_s" = 1800.0
"unscaled.segment_s" = 1800.0
"unscaled.output_s" = 1800.0
"unscaled.diagnostics_s" = 1800.0
"unscaled.stats_s" = 1800.0
"coupling.vertical_wind" = "dgw"
'''


def test_the_labs_build_runs_a_tiny_wave_box_from_the_writers_files(tmp_path):
    """Two segments of 30 minutes of a box of 4 x 4 columns making its own ascent, on the store's build: CM1 reads
    every entry the writer gives it and prints the values, restarts from the first segment's restart, and the wave's
    record holds an interval for each."""
    _drive()
    lib = _probe(tmp_path, TINY)
    store = _seeded(tmp_path / 'store')
    v = cm1.values(lib, 'probe', 'box')
    build = None if STORE is None else cm1_builds.folder(STORE, cm1_builds.key(cm1_builds.gather(v['settings'],
                                                                                                 macros=v['macros'])[0]))
    if build is None or not (build / 'build.json').exists():
        pytest.skip("the lab's store holds no build for the case; `python -m worldlab build` makes it")
    folder = cm1.write_case(lib, 'probe', 'box', store=store)
    record = jobs.run_case(folder, store=store, threads=1, segments=2, build_folder=build, library=lib)
    assert [(s['start_s'], s['end_s']) for s in record['segments']] == [(0.0, 1800.0), (1800.0, 3600.0)]
    read = record['segments'][0]['read']
    assert read['values']['lsw_coupling'] == '1' and read['values']['ipbl2_per_mass'] == '1'
    assert float(read['values']['dtl']) == pytest.approx(v['scaled']['time_step_s'], rel=1e-6)
    assert any(line.startswith('Lab: the damped gravity wave; its lid') for line in read['lines'])
    assert any(line.startswith('Lab soil: the layers') for line in read['lines'])
    assert any('cp,grv =' in line for line in read['lines'])
    from worldlab import cm1_read
    run = jobs.folder(store, record['key'])
    intervals = cm1_read.lsw_record(run)
    assert [(r['start_s'], r['end_s']) for r in intervals] == [(0.0, 1800.0), (1800.0, 3600.0)]
    means = cm1_read.domain_means(run)
    assert means['mtime'].tolist() == [0.0, 1800.0, 3600.0] and np.all(np.isfinite(means['th']))


def test_the_reader_takes_terlunas_wave_box_as_cm1_wrote_it():
    """Terluna's damped-gravity-wave sea box, read in place: its 473 domain means every three hours through 59 days on
    111 levels, every bin of local time filled over its second solar day, and rain by quarter of local time from
    sunrise, most of it in the afternoon, as Terluna's readings of its later days have it (2.79-2.91 mm/day over days
    3 and 4)."""
    from worldlab import cm1_read
    drive = _drive()
    run = drive / 'crm-runs' / 'box_near_side_sea_dgw'
    if not (run / cm1_read.DIAG_CTL).exists():
        pytest.skip("Terluna's box_near_side_sea_dgw is absent from the drive")
    means = cm1_read.domain_means(run)
    assert means['th'].shape == (473, 111) and np.allclose(np.diff(means['mtime']), 10800.0)
    assert cm1_read.run_clock(run) == dict(start_hour_deg=-90.0, solar_day_s=2551443.0)
    series = cm1_read.domain_mean_by_hour(run, (1.0, 2.0))
    assert len(series['hour_angle_deg']) == 36 and min(series['outputs_per_bin']) >= 6
    summary = cm1_read.summary(run, (1.0, 2.0))
    quarters = summary['rain_by_quarter_mm_day']
    assert 2.0 < summary['rain_mm_day'] < 3.5 and quarters['afternoon'] == max(quarters.values())


def test_the_commands_reach_a_run_by_the_cases_key_and_leave_the_shared_index_aside(tmp_path, monkeypatch, capsys):
    """status, stop and read find a run by the case's key as this worktree computes it; a link of the store's index
    that another worktree pointed elsewhere changes nothing, and a case without a run is named as such."""
    from worldlab import __main__ as commands
    _drive()
    store = _seeded(tmp_path / 'store')
    monkeypatch.setenv('WORLDLAB_STORE', str(store))
    elsewhere = store / 'runs' / 'cm1-elsewhere'
    elsewhere.mkdir(parents=True)
    stages.name_link(store, STUDY, 'sea_imposed', elsewhere)
    assert commands.main(['status', STUDY, 'sea_imposed']) == 2
    key = cm1.case_key(LIB, STUDY, 'sea_imposed', store=store)['key']
    assert f'has no run in the store under its key {key[:16]}' in capsys.readouterr().err
    run = jobs.folder(store, key)
    run.mkdir(parents=True)
    stages.write_json(run / jobs.RECORD, dict(study=STUDY, case='sea_imposed', segments=[], length_s=86400.0,
                                              state='paused'))
    assert commands.main(['status', STUDY, 'sea_imposed']) == 0
    assert capsys.readouterr().out.startswith(f'{STUDY}:sea_imposed: 0.00 of 1.00 days')
    assert commands.main(['stop', STUDY, 'sea_imposed']) == 0 and (run / jobs.STOP).exists()
