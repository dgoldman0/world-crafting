"""CM1's adapter: a forced site box's case, written from a study, its world and scenario, CM1's defaults and a GCM run
that forces it (lab/design/architecture.md, "Model adapters"; plan.md, stage 3).

    from worldlab import cm1
    case = cm1.write_case(Library(), 'open-moon-couplings', 'sea_imposed', store=store)   # cases/cm1-<key>/

What a case holds. The case's folder in the store, cases/cm1-<the key's first 16 hex digits>/, holds every input CM1
reads but the build's own files: the namelist (namelist.template, which the job wrapper completes for each segment),
the sounding and the grid, the surface, the forcing's files from python/climate/crm/gcm_site.py (terluna_wls.txt,
terluna_lsadv.txt) with one solar day of its nudging windows (windows/, from which the wrapper writes each segment's
own), the rain's table where the case takes the world's fall law, and case.json: its header (key, producer, inputs,
read set, the registry's checks and any override) and its record, every value with its source. The folder is written
whole and made read-only, and `index/<study>/<case>` names it.

The values. The world's gravity, CO2 and O2 reach CM1 compiled into its build or through the namelist
(`world_constants`; patch 06 of the lab's CM1 series), the soil's top layer as `soil_dz1` (patch 07) and the Sun's
declination as `sun_decl` (patch 08), from `derive`. CM1's lengths, times and rates are the defaults' scaled by rule 9
(`derive.cm1_factors` and `cm1_values`): the columns' width, the vertical grid and its top, the time step, the
boundary layer's length and the damping rate. The box starts at sunrise at its site's latitude and the case's season,
and runs its solar days, cut to the last whole restart interval. The forcing comes from `gcm_site`: the GCM's column at
the site over the case's years, through `site_forcing` and `case_inputs`, with the coupling and its settings passed
through as the case states them, so that a case of coupling 'wtg' is written once gcm_site takes it. The rain's
limits, fall law and warm rain's factors follow the case's physics (patches 03 to 05), from the site's air at 2 m
(python/atmosphere/rain).

The thin path. A case is a box over the sea, on the core and lab series alone, with Morrison's rain, RRTMG, the MM5
surface layer and CM1's simple boundary layer; a ring, a box over land or terrain, and a variant are refused until
stage 3 widens. A case is forced by a GCM run named by a pin (`forcing_run`), read in place, with Terluna's layout of
a run's folder (model/ and inputs/*topography*.sra); a case forced by its study's own run (`forced_by`) waits for the
lab's runs of block 3. A coupled reference may be another case's own domain mean by local time (`from_case`), which
waits on that case's run (worldlab.cm1_read).

The registry. Every CM1 entry is evaluated on the case's world, scenario, resolved settings and quantities, among
them the build's compiled gravity against the world's (B1), the soil's layer against the day's depth, the box's
ground pressure against RRTMG's tables (B22) and the damping layer's clearance above the GCM's convection; an entry
that stops the case stops its writing unless an override states its justification, which the record keeps.
"""
from __future__ import annotations

import copy
import io
import math
import os
import re
import tarfile
import tempfile
from pathlib import Path

import numpy as np

from . import cm1_builds, derive, registry, stages
from .data import DataError, parse_pin
from .exoplasim import PINS, _verified
from .roots import root
from .spec import LAB, Library, SpecError

SCHEMA = 'worldlab.case.cm1/0'
DAY_S = derive.DAY_S
TEMPLATE = cm1_builds.TREE + 'run/config_files/cpm_RadConvEquil/namelist.input'   # CM1's radiative-convective case
KINDS = ('box',)
SURFACES = ('sea',)
# The physics of the thin path's cases: Morrison's rain (ptype 5), RRTMG (radopt 2), the MM5 surface layer over a
# sea held at the GCM's temperature (sfcmodel 2, oceanmodel 1) and CM1's simple boundary layer (ipbl 2).
THIN_PHYSICS = dict(microphysics='morrison', radiation='rrtmg', surface_layer='mm5', pbl='cm1-simple', twilight='none')
RAIN_LIMITS = ('capillary', 'earth', 'breakup-only')
FALL_LAWS = ('morrison', 'world')
WARM_RAIN = ('earth', 'gravity')
GUSTS = {'mm5': 0, 'beljaars': 1}
SUN_DECLINATIONS = ('from-season', 'equinox')
WIND_PULLS = ('gcm-lowest-level', 'ground')
INFLOWS = {'gcm-air': True, 'box-air': False}
BREAKUP_DIAMETER_M = 3.0e-4                  # Morrison's brkup_db, which patch 03 scales inside CM1
WINDOWS = 'windows'                          # the case's folder of one solar day's nudging windows
RAIN_TABLE = 'lab_rain_law.txt'              # the table patch 04 reads (python/atmosphere/rain/fall_law.TABLE_FILE)
SEA_LAND_USE = 16                            # CM1's water row of LANDUSE.TBL
# A box's output, as Terluna's site boxes wrote it (climate/crm/cm1_run.py at 39c5ee04, case_settings with
# RAIN_TEST_OUTPUT): the surface's parameters, the heat and vapour budgets and the radiative tendencies.
BOX_OUTPUT = dict(output_format=1, output_filetype=2, output_sfcparams=1, output_tke=0, output_km=0, output_kh=0,
                  output_uinterp=1, output_vinterp=1, output_v=0, output_winterp=1, output_u=0, output_w=0,
                  output_dbz=0, output_radten=1, output_thbudget=1, output_qvbudget=1, output_cape=1, output_cin=1,
                  output_lcl=1, output_lfc=1, output_pwat=1, output_lwp=1)
PYTHON = LAB.parent / 'python'
PRODUCER = (Path(__file__), LAB / 'worldlab' / 'cm1_builds.py', LAB / 'worldlab' / 'derive.py',
            LAB / 'worldlab' / 'spec.py', LAB / 'worldlab' / 'stages.py', LAB / 'worldlab' / 'cm1_read.py',
            PYTHON / 'climate' / 'crm' / 'gcm_site.py', PYTHON / 'climate' / 'gcm' / 'year_files.py',
            PYTHON / 'atmosphere' / 'rain' / 'fall_law.py', PYTHON / 'atmosphere' / 'rain' / 'breakup.py',
            PYTHON / 'atmosphere' / 'rain' / 'drops.py', PYTHON / 'atmosphere' / 'rain' / 'morrison.py',
            PYTHON / 'atmosphere' / 'rain' / 'warm_rain.py',
            PYTHON / 'atmosphere' / 'radiative_convective' / 'thermodynamics.py',
            PYTHON / 'shared' / 'constants.py', PYTHON / 'shared' / 'constants.json')   # what the air and rain read
EVIDENCE = ('the inputs of a CM1 case, written from the lab\'s specifications and derivations and a GCM run\'s column at '
            'the site: a runnable set-up, checked by the tests of lab/tests/test_cm1.py; no physical validation')


# The namelist.

def template(archive: Path = cm1_builds.ARCHIVE) -> str:
    """CM1's radiative-convective namelist from the pinned archive, from which every case's starts."""
    data = _verified(str(archive), str(PINS))
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as tar:
        return tar.extractfile(TEMPLATE).read().decode()


def fortran(value) -> str:
    """A namelist value as CM1 reads it: a logical, an integer, a real as Python writes it, or a quoted string."""
    if isinstance(value, bool):
        return '.true.' if value else '.false.'
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)):
        if not math.isfinite(value):
            raise SpecError(f'a namelist value is finite, where it is {value!r}')
        return repr(float(value))
    if isinstance(value, str):
        return f"'{value}'"
    raise SpecError(f'a namelist value is a logical, integer, real or string, where it is {value!r}')


def set_entries(text: str, entries: dict) -> str:
    """The namelist `text` with `entries` ({section: {name: value}}) set: an entry the section holds takes the value
    in place, and one it lacks is added before the section's end. A section the text lacks is refused."""
    for section, values in entries.items():
        match = re.search(rf'^\s*&{re.escape(section)}\s*$', text, flags=re.M)
        if match is None:
            raise SpecError(f'the namelist holds no &{section}')
        end = re.compile(r'^\s*/\s*$', re.M).search(text, match.end())
        block = text[match.end():end.start()]
        for name, value in values.items():
            pattern = re.compile(rf'^(\s*{re.escape(name)}\s*=\s*)([^,\n]*)(,?)', re.M | re.I)
            if pattern.search(block):
                block = pattern.sub(lambda m: f'{m.group(1)}{fortran(value)}{m.group(3)}', block, count=1)
            else:
                block = block.rstrip('\n') + f'\n {name} = {fortran(value)},\n'
        text = text[:match.end()] + block + text[end.start():]
    return text


def entries_of(text: str) -> dict:
    """A namelist's entries as text, by section and lower-case name."""
    out, section = {}, None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith('&'):
            section = s[1:].strip().lower()
            out[section] = {}
        elif s == '/':
            section = None
        elif section and '=' in s:
            name, value = s.split('=', 1)
            out[section][name.strip().lower()] = value.strip().rstrip(',').strip()
    return out


# The grid.

def vertical_grid(dz0: float, z_fine: float, stretch: float, dz_max: float, ztop: float) -> list[float]:
    """Heights (m) of the w levels: dz0 up to z_fine, growing by `stretch` a level to dz_max, then even, to ztop,
    without a sliver under the top (Terluna's vertical_grid, climate/crm/cm1_run.py at 39c5ee04)."""
    if not (dz0 > 0 and z_fine >= 0 and stretch >= 1 and dz_max >= dz0 and ztop > dz0):
        raise SpecError(f'a vertical grid rises by dz0 > 0 to dz_max >= dz0 under ztop > dz0, where it is given '
                        f'{dz0}, {z_fine}, {stretch}, {dz_max}, {ztop}')
    levels, z, dz = [0.0], 0.0, dz0
    while z < ztop - 1e-6:
        if z >= z_fine:
            dz = min(dz * stretch, dz_max)
        z = min(z + dz, ztop)
        levels.append(z)
    if levels[-1] - levels[-2] < 0.5 * dz_max:
        levels.pop(-2)
    return levels


# The case's settings.

INTERVALS = ('segment_s', 'restart_s', 'output_s', 'diagnostics_s', 'stats_s')


def _divides(a: float, b: float) -> bool:
    """Whether a whole number of a, at least one, makes b."""
    n = b / a
    return round(n) >= 1 and abs(n - round(n)) < 1e-9


def check_intervals(run: dict, where: str) -> None:
    """A run's intervals as the wrapper's segments need them: each positive; each segment a whole number of restart
    intervals, so that it ends on the restart it resumes from; and the outputs, domain means and statistics each a
    divisor of the segment, since CM1 counts them from each restart's time (restart_reset_frqtim), so that a resumed run
    writes them at the times a run without the restart would."""
    for name in INTERVALS:
        value = run.get(name)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise SpecError(f'{where}: {name} is a positive number of seconds, where it is {value!r}')
    if not _divides(run['restart_s'], run['segment_s']):
        raise SpecError(f"{where}: a segment of {run['segment_s']} s holds no whole number of restart intervals of "
                        f"{run['restart_s']} s, so it would end between restarts")
    for name in ('output_s', 'diagnostics_s', 'stats_s'):
        if not _divides(run[name], run['segment_s']):
            raise SpecError(f"{where}: {name} of {run[name]} s divides no segment of {run['segment_s']} s, so the "
                            'outputs CM1 counts from each restart would fall off those of a run without it')


def checked_settings(item) -> dict:
    """A case's resolved settings, refused where the thin path cannot write them."""
    s = item.settings
    where = f'{item.study}:{item.name}'
    if s.get('kind') not in KINDS:
        raise SpecError(f'{where}: the thin path writes a box ({KINDS}), where the case is a {s.get("kind")!r}; rings '
                        'wait on stage 3\'s widening')
    if s.get('variants'):
        raise SpecError(f'{where}: variants {s["variants"]} wait on stage 3\'s widening, their series unchecked after '
                        "the lab's")
    for name, value in THIN_PHYSICS.items():
        if s['physics'].get(name) != value:
            raise SpecError(f'{where}: physics.{name} is {value!r} on the thin path, where the case states '
                            f'{s["physics"].get(name)!r}')
    checks = (('physics.rain_size_limits', s['physics']['rain_size_limits'], RAIN_LIMITS),
              ('physics.rain_fall_law', s['physics']['rain_fall_law'], FALL_LAWS),
              ('physics.warm_rain_rates', s['physics']['warm_rain_rates'], WARM_RAIN),
              ('physics.gust_over_water', s['physics']['gust_over_water'], tuple(GUSTS)),
              ('physics.sun_declination', s['physics']['sun_declination'], SUN_DECLINATIONS),
              ('world_constants', s['world_constants'], cm1_builds.WORLD_CONSTANTS),
              ('coupling.wind_pulled_from', s['coupling']['wind_pulled_from'], WIND_PULLS),
              ('coupling.inflow', s['coupling']['inflow'], tuple(INFLOWS)))
    for path, value, allowed in checks:
        if value not in allowed:
            raise SpecError(f'{where}: {path} is one of {allowed}, where the case states {value!r}')
    if not isinstance(s['physics'].get('pbl_per_mass'), bool):
        raise SpecError(f'{where}: physics.pbl_per_mass is true or false')
    if s['physics']['rain_fall_law'] == 'world' and s['physics']['rain_size_limits'] != 'capillary':
        raise SpecError(f"{where}: the world's fall law takes the capillary limits, at whose balance its rate is "
                        'computed (models/cm1/README.md, the limits of patches 03 and 04)')
    site = s.get('site', {})
    if site.get('surface') not in SURFACES:
        raise SpecError(f'{where}: the thin path writes a box over the sea, where the site states '
                        f'{site.get("surface")!r}; a box over land takes its land row and wetness, a later widening')
    columns = s.get('columns', {})
    if set(columns) != {'nx', 'ny'} or not all(isinstance(v, int) and not isinstance(v, bool) and v >= 4
                                                for v in columns.values()):
        raise SpecError(f'{where}: columns states whole nx and ny of 4 or more, where it states {columns!r}')
    if (s.get('forced_by') is None) == (s.get('forcing_run') is None):
        raise SpecError(f"{where}: a box is forced by one GCM run, its study's own (forced_by) or a pinned one "
                        '(forcing_run)')
    years = s.get('reference_model_years')
    if not (isinstance(years, list) and len(years) == 2 and all(isinstance(y, int) for y in years)
            and 0 <= years[0] <= years[1]):
        raise SpecError(f'{where}: reference_model_years names the first and last model years, where it is {years!r}')
    days = s['unscaled']['run_solar_days']
    if isinstance(days, bool) or not isinstance(days, (int, float)) or days <= 0:
        raise SpecError(f'{where}: unscaled.run_solar_days is a positive number of solar days, where it is {days!r}')
    read = s.get('read_solar_days')
    if read is not None and not (isinstance(read, list) and len(read) == 2 and 0 <= read[0] < read[1] <= days):
        raise SpecError(f'{where}: read_solar_days names the first and last solar day read, within the run\'s '
                        f'{days}, where it is {read!r}')
    check_intervals(s['unscaled'], where)
    for name in ('radiation_s', 'nudge_tau_s', 'wind_nudge_tau_s'):
        value = s['unscaled'][name]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise SpecError(f'{where}: unscaled.{name} is a positive number of seconds, where it is {value!r}')
    c = s['coupling']
    if c['reference_season'] == 'window':
        raise SpecError(f"{where}: coupling.reference_season 'window' averages the GCM's records within "
                        f"{c['season_window_deg']} degrees of solar longitude around the case's season, which waits for "
                        "a reading of each record's solar longitude: gcm_site.site_forcing averages every record of the "
                        "years. A case states 'year', the whole years' mean, with its reason in "
                        'coupling.reference_season_reason')
    if c['reference_season'] != 'year' or not str(c.get('reference_season_reason', '')).strip():
        raise SpecError(f"{where}: coupling.reference_season is 'year', with its reason in "
                        f"coupling.reference_season_reason, where the case states {c['reference_season']!r} and "
                        f"{c.get('reference_season_reason')!r}")
    return s


def gcm_site_of(site: dict) -> dict:
    """The site as gcm_site takes it."""
    return {k: site[k] for k in ('lat_deg', 'lon_deg', 'half_lat_deg', 'half_lon_deg', 'surface')}


def forcing_folder(settings: dict, where: str) -> dict:
    """The GCM run that forces the case: its folder, model folder and surface heights' file, and its pin."""
    if settings.get('forcing_run') is None:
        raise SpecError(f"{where}: forced by its study's own run {settings['forced_by']!r}, which the lab makes in block "
                        '3 of PLAN.md; until then a case names a pinned run as forcing_run')
    pin = parse_pin(settings['forcing_run'])
    if pin.root is None or pin.entry is not None:
        raise SpecError(f'{where}: forcing_run is a root and a folder, as terluna-drive:gcm-runs/<run>, where it is '
                        f"{settings['forcing_run']!r}")
    base = root(pin.root)
    if base is None:
        raise DataError(f"{where}: the root {pin.root!r} of the forcing run is absent on this machine")
    folder = base / pin.path
    model = folder / 'model'
    found = sorted((folder / 'inputs').glob('*topography*.sra'))
    if not model.is_dir() or len(found) != 1:
        raise DataError(f"{where}: {folder} holds no model/ folder and one inputs/*topography*.sra, Terluna's layout "
                        "of a run's folder")
    return dict(pin=settings['forcing_run'], folder=folder, model=model, topography=found[0], name=folder.name)


def forcing_files(found: dict, years) -> list[Path]:
    """The forcing run's files a case reads: its namelists, its surface heights and its year files over the years."""
    names = [found['model'] / n for n in ('planet_namelist', 'plasim_namelist', 'landmod_namelist')]
    files = [p for p in names if p.exists()] + [found['topography']]
    for year in range(years[0], years[1] + 1):
        path = found['model'] / f'MOST.{year:05d}.nc'
        if not path.exists():
            raise DataError(f'{path}: a year file of the forcing run is missing')
        files.append(path)
    return files


def sunlight_w_m2(model: Path) -> float:
    """The sunlight at the top of the air with which the forcing run ran: GSOL0 of its planet namelist, so that the box
    takes the GCM's Sun."""
    m = re.search(r'^\s*GSOL0\s*=\s*([^,\s]+)', (model / 'planet_namelist').read_text(), flags=re.M | re.I)
    if m is None:
        raise DataError(f"{model}: the planet namelist states no GSOL0, the run's sunlight")
    return float(m.group(1))


# The case's values.

def values(library: Library, study_id: str, name: str) -> dict:
    """Everything a case's key and files follow from but the forcing's output: the resolved item, its world and
    scenario, its derived and scaled values, its grid, the build's settings and macros, and its read set."""
    study = library.study(study_id)
    if name not in study.crm:
        raise SpecError(f'{study_id}: holds no CM1 case {name!r}')
    item = study.crm[name]
    s = checked_settings(item)
    where = f'{study_id}:{name}'
    world = library.world(study.scenario['world'])
    scenario = study.scenario
    defaults = library.defaults('cm1/defaults')
    factors = derive.cm1_factors(world, scenario, defaults)
    scaled = derive.cm1_values(s, factors, set_paths=item.set_paths)
    g = derive.gravity(world)
    fractions = derive.mole_fractions(scenario)
    day_s = derive.solar_day_days(world) * DAY_S
    site = s['site']
    obliquity = world['rotation']['obliquity_deg']
    decl = derive.declination_deg(obliquity, s['solar_longitude_deg']) \
        if s['physics']['sun_declination'] == 'from-season' else 0.0
    if s['unscaled']['start'] != 'sunrise':
        raise SpecError(f"{where}: a box starts at sunrise, where the case states {s['unscaled']['start']!r}")
    start_hour = derive.sunrise_hour_angle_deg(site['lat_deg'], decl)
    u = s['unscaled']
    zw = vertical_grid(scaled['dz0_m'], scaled['z_fine_m'], u['z_stretch'], scaled['dz_max_m'], scaled['ztop_m'])
    restart_s = float(u['restart_s'])
    solar_days = float(u['run_solar_days'])
    length_s = math.floor(solar_days * day_s / restart_s + 1e-6) * restart_s
    if length_s < restart_s:
        raise SpecError(f'{where}: a run of {solar_days} solar days holds no whole restart interval of {restart_s} s')
    droplets = scenario['air'].get('cloud_droplets_per_cm3')
    if not isinstance(droplets, (int, float)) or isinstance(droplets, bool) or droplets <= 0:
        raise SpecError(f'{scenario["id"]}: air.cloud_droplets_per_cm3 is a positive number for Morrison\'s rain')
    build_gravity = g if s['world_constants'] == 'build' else derive.CM1_EARTH_G
    macros = (cm1_builds.world_macros(g, fractions['CO2'], fractions['O2']) if s['world_constants'] == 'build'
              else {})
    soil = scaled['soil_top_layer_m']
    read_set = dict(gravity_m_s2=g, rotation_rate_rad_s=derive.rotation_rate(world), solar_day_s=day_s,
                    radius_m=world['body']['radius_m'], obliquity_deg=obliquity, mole_fractions=fractions,
                    surface_pressure_pa=scenario['air']['surface_pressure_pa'],
                    reference_temperature_k=derive.reference_temperature_k(scenario),
                    cloud_droplets_per_cm3=float(droplets), factors=factors,
                    soil_factor=derive.soil_factor(day_s / DAY_S), scaled=scaled,
                    set_paths=sorted(item.set_paths))      # rule 9 leaves a value the study sets unscaled
    return dict(study=study, item=item, settings=s, where=where, world=world, scenario=scenario, defaults=defaults,
                factors=factors, scaled=scaled, gravity_m_s2=g, fractions=fractions, solar_day_s=day_s,
                declination_deg=decl, start_hour_deg=start_hour, zw=zw, length_s=length_s, solar_days=solar_days,
                restart_s=restart_s, macros=macros, build_gravity_m_s2=build_gravity, soil_dz1_m=soil,
                coriolis=derive.coriolis(derive.rotation_rate(world), site['lat_deg']), read_set=read_set)


def coupling_of(v: dict) -> dict:
    """The case's coupling as gcm_site.case_inputs takes it: the imposed wind takes none of a coupling's settings, a
    coupled box its length (the footprint, metres, or the world's radius), reference, vapour, start and table."""
    c = v['settings']['coupling']
    out = dict(coupling=c['vertical_wind'])
    if c['vertical_wind'] == 'imposed':
        return out
    length = c['coupling_length']
    if length == 'footprint':
        out['coupling_length_m'] = None
    elif length == 'radius':
        out['coupling_length_m'] = float(v['world']['body']['radius_m'])
    elif isinstance(length, (int, float)) and not isinstance(length, bool) and length > 0:
        out['coupling_length_m'] = float(length)
    else:
        raise SpecError(f"{v['where']}: coupling.coupling_length is 'footprint', 'radius' or metres, where it is "
                        f'{length!r}')
    out.update(reference=c['coupled_reference'], reference_vapour=c['coupled_vapour'], start=c['coupled_start'],
               table_heat=c['coupled_table_heat'])
    return out


def upstream_reference(v: dict, library: Library, store: Path) -> dict | None:
    """A coupled reference taken from another case's own run (`{from_case, solar_days}`): that case's key and the
    run's files it reads, for the key; None for a reference of the GCM's."""
    ref = v['settings']['coupling'].get('coupled_reference')
    if not isinstance(ref, dict):
        return None
    if set(ref) != {'from_case', 'solar_days'} or len(ref['solar_days']) != 2:
        raise SpecError(f"{v['where']}: a reference from a case states from_case and solar_days, where it is {ref!r}")
    from . import cm1_read
    other = case_key(library, v['study'].id, ref['from_case'], store=store)
    run = Path(store) / 'runs' / f'cm1-{other["key"][:16]}'
    first, last = (float(d) for d in ref['solar_days'])
    needed = min(last * v['solar_day_s'], other['values']['length_s'])     # the run's end, cut to whole restarts
    reached = cm1_read.reached_s(run)
    if reached is None or reached < needed - 1.0:
        raise DataError(f"{v['where']}: its reference is {ref['from_case']}'s domain mean over solar days {first}-{last}, "
                        f'which waits on that case\'s run to {needed:.0f} s (it stands at {reached or 0:.0f} s)')
    every = float(other['values']['settings']['unscaled']['diagnostics_s'])
    start, end = first * v['solar_day_s'], needed
    files = [p for p in cm1_read.diag_files(run)
             if start < (int(cm1_read.DIAG_NUMBER.match(p.name).group(1)) - 1) * every <= end + 1e-6]
    files += [run / cm1_read.DIAG_CTL, cm1_read.clock_file(run)]          # the variables' layout and the box's clock
    found = stages.digests(files, store)
    return dict(case=ref['from_case'], key=other['key'], run=run, solar_days=[first, last],
                files={p.name: found[str(p)] for p in files})


def case_key(library: Library, study_id: str, name: str, *, store: Path) -> dict:
    """The case's key and the inputs it hashes, before anything is written: its producer, its build's key, the forcing
    run's files by digest with the years and site it reads, an upstream case's run where its reference is that run's,
    its settings' hash, its read set and the environment's class."""
    v = values(library, study_id, name)
    build_inputs, _ = cm1_builds.gather(v['settings'], macros=v['macros'])
    found = forcing_folder(v['settings'], v['where'])
    years = v['settings']['reference_model_years']
    files = forcing_files(found, years)
    digests = stages.digests(files, store)
    upstream = upstream_reference(v, library, store)
    inputs = dict(producer=stages.producer(PRODUCER), build=cm1_builds.key(build_inputs),
                  forcing=dict(pin=found['pin'], years=years, site=gcm_site_of(v['settings']['site']),
                               files={str(p.relative_to(found['folder'])): digests[str(p)] for p in files}),
                  upstream=None if upstream is None else dict(case=upstream['case'], key=upstream['key'],
                                                               solar_days=upstream['solar_days'],
                                                               files=upstream['files']),
                  settings=v['item'].settings_hash, read_set=v['read_set'],
                  environment=stages.environment_class())
    return dict(key=stages.key(inputs), inputs=inputs, values=v, forcing=found, build_inputs=build_inputs,
                upstream=upstream)


# The forcing, cached.

def _cached(store: Path | None, kind: str, inputs: dict, compute):
    """A JSON product of `compute()`, kept in the store's caches under the key of `inputs`."""
    if store is None:
        return compute()
    path = Path(store) / 'caches' / kind / f'{stages.key(inputs)}.json'
    if path.is_file():
        return stages.read_json(path)
    result = compute()
    stages.write_json(path, result, indent=None)
    return result


def forcing(run: dict, years, site: dict, *, store: Path | None, files: dict) -> dict:
    """gcm_site.site_forcing of the run at the site, cached by the run's files, the years, the site and gcm_site's own
    hash."""
    from climate.crm import gcm_site as gs
    inputs = dict(producer=stages.producer([PYTHON / 'climate' / 'crm' / 'gcm_site.py',
                                            PYTHON / 'climate' / 'gcm' / 'year_files.py']),
                  run={k: v for k, v in run.items() if k not in ('folder', 'topography', 'surface_height_m')},
                  files=files, years=list(years), site=site)
    return _cached(store, 'gcm-site', inputs, lambda: gs.site_forcing(run, tuple(years), site))


def first_mode(run: dict, years, *, store: Path | None, files: dict) -> dict:
    """gcm_site.first_mode over the run's tropics, cached as `forcing` is."""
    from climate.crm import gcm_site as gs
    inputs = dict(producer=stages.producer([PYTHON / 'climate' / 'crm' / 'gcm_site.py',
                                            PYTHON / 'climate' / 'gcm' / 'year_files.py']),
                  run={k: v for k, v in run.items() if k not in ('folder', 'topography', 'surface_height_m')},
                  files=files, years=list(years))
    return _cached(store, 'gcm-mode', inputs, lambda: gs.first_mode(run, tuple(years)))


def site_column(v: dict, forcing_: dict) -> dict:
    """The site's air at 2 m for the rain's entries: the GCM's 2 m temperature and its lowest level's vapour at the
    surface pressure, as a relative humidity over liquid water, in the scenario's dry air at the world's gravity."""
    from atmosphere.radiative_convective.thermodynamics import DryAir
    from atmosphere.rain import drops
    surface, gcm = forcing_['surface'], forcing_['gcm']
    p, t = float(surface['pressure_pa']), float(surface['air_2m_k'])
    q = float(forcing_['profile']['specific_humidity_kg_kg'][-1])
    eps = gcm['gas_constant_j_kg_k'] / gcm['vapour_gas_constant_j_kg_k']
    e = q * p / (eps + (1.0 - eps) * q)
    rh = min(1.0, e / drops.liquid_saturation_pressure(t))
    column = drops.Column(gravity_m_s2=v['gravity_m_s2'], surface_pressure_pa=p, surface_temperature_k=t,
                          surface_relative_humidity=rh, air=DryAir(p, dict(v['fractions'])))
    return dict(column=column, record=dict(pressure_pa=p, temperature_k=t, relative_humidity=rh,
                                           source="the GCM's 2 m air temperature and its lowest level's vapour at the "
                                                  'surface pressure, at the site'))


def rain(v: dict, forcing_: dict) -> dict:
    """The rain's entries of &param3, its table where it takes the world's fall law, and their record: the limits by
    physics.rain_size_limits (patch 03, or the scaled brkup_db alone for 'breakup-only', or Morrison's own), the fall
    law and self-collection by physics.rain_fall_law (patch 04), the warm rain's factors by physics.warm_rain_rates
    (patch 05)."""
    from atmosphere.rain import fall_law, warm_rain
    p = v['settings']['physics']
    limits, law = p['rain_size_limits'], p['rain_fall_law']
    entries, record, table = {}, dict(limits=limits, fall_law=law, warm_rain=p['warm_rain_rates']), None
    if limits == 'capillary' or law == 'world':
        air = site_column(v, forcing_)
        found = fall_law.settings(air['column'])
        record.update(air=air['record'], computed=dict(limits=found['limits'], breakup=found['breakup'],
                                                       self_collection=found['self_collection']))
    if limits == 'capillary':
        n = found['namelist']
        entries.update(brkup_db=n['brkup_db'], brkup_gscale=1, brkup_rhor=n['brkup_rhor'], brkup_rhoexp=n['brkup_rhoexp'])
    elif limits == 'breakup-only':
        entries.update(brkup_db=v['scaled']['breakup_diameter_m'], brkup_gscale=0)
    else:
        entries.update(brkup_db=BREAKUP_DIAMETER_M, brkup_gscale=0)
    if law == 'world':
        entries.update(rain_fall_law=1, rain_selfcoll=found['namelist']['rain_selfcoll'])
        table = fall_law.table_text(found['table'])
    else:
        entries.update(rain_fall_law=0)
    if p['warm_rain_rates'] == 'gravity':
        entries.update(warm_rain.factors(v['gravity_m_s2']))
    record['entries'] = dict(entries)
    return dict(entries=entries, table=table, record=record)


def sounding(start: dict, zw, surface: dict) -> str:
    """input_sounding (isnd = 7): the surface's pressure (hPa), potential temperature (K) and vapour (g/kg), then at
    each scalar level and the top the height (m), potential temperature, vapour and wind (m/s) of the air the box starts
    from, in the form Terluna's setup writes (climate/crm/cm1_run.py at 39c5ee04). The surface's potential temperature
    is the GCM's 2 m air's, in CM1's own constants."""
    from climate.crm import gcm_site as gs
    zw = np.asarray(zw, float)
    zh = 0.5 * (zw[1:] + zw[:-1])
    ps = float(surface['pressure_pa'])
    theta_sfc = float(surface['air_2m_k']) * (gs.P00 / ps) ** gs.CM1_KAPPA
    heights = [*zh, zw[-1]]
    rows = [f'{ps / 100.0:12.4f} {theta_sfc:12.4f} {float(start["qv_at"](0.0)) * 1000.0:12.5f}']
    rows += [f'{z:12.3f} {float(start["theta_at"](z)):12.4f} {float(start["qv_at"](z)) * 1000.0:12.5f} '
             f'{float(start["u_at"](z)):8.3f} {float(start["v_at"](z)):8.3f}' for z in heights]
    return '\n'.join(rows) + '\n'


def grid_text(zw) -> str:
    return ''.join(f'{z:.3f}\n' for z in zw)


def surface_text(sea_k: float) -> str:
    """terluna_surface.txt (core patch 08, initsfc = 9): one segment over the whole box, water at the GCM's temperature,
    as Terluna's setup writes a sea box's."""
    return f'1\n{-1e9:.1f} {1e9:.1f} {2.0:.1f} {SEA_LAND_USE:d} {sea_k:.3f} {sea_k:.3f}\n'


def namelist_entries(v: dict, case: dict, rain_: dict, sea_k: float, sunlight: float) -> dict:
    """The case's entries by section, on CM1's radiative-convective template: the grid and times, the physics, the
    world, the surface, the output, and the forcing's own (case_inputs). The entries a box forced from a GCM site takes
    follow Terluna's case_settings (climate/crm/cm1_run.py at 39c5ee04), with the lab's scaled values."""
    s, scaled, u = v['settings'], v['scaled'], v['settings']['unscaled']
    zw = v['zw']
    nz = len(zw) - 1
    p = s['physics']
    param3 = dict(fcor=float(f"{v['coriolis']:.6e}"), rdalpha=scaled['rayleigh_rate_per_s'],
                  zd=u['damping_base_fraction'] * zw[-1], l_inf=scaled['pbl_length_m'],
                  ndcnst=v['read_set']['cloud_droplets_per_cm3'], ipbl2_per_mass=int(p['pbl_per_mass']),
                  gust_over_water=GUSTS[p['gust_over_water']], **rain_['entries'], soil_dz1=v['soil_dz1_m'],
                  sun_decl=v['declination_deg'])
    if s['world_constants'] == 'namelist':
        param3.update(world_g=v['gravity_m_s2'], world_co2=v['fractions']['CO2'], world_o2=v['fractions']['O2'])
    param3.update(case['namelist']['param3'])
    param8 = dict(var12=0.0, var16=0.0, var17=round(sunlight, 3), var20=0.0)
    param8.update(case['namelist']['param8'])
    return dict(
        param0=dict(nx=s['columns']['nx'], ny=s['columns']['ny'], nz=nz, timeformat=3, timestats=1,
                    terrain_flag=False),
        param1=dict(dx=scaled['column_target_m'], dy=scaled['column_target_m'], dz=round(zw[-1] / nz, 1),
                    dtl=scaled['time_step_s'], cfl_limit=1.0, timax=v['length_s'], run_time=-999.9,
                    tapfrq=float(u['output_s']), rstfrq=float(u['restart_s']), statfrq=float(u['stats_s']),
                    prclfrq=1.0e9),
        param2=dict(cm1setup=2, testcase=0, adapt_dt=1, irst=0, rstnum=1, ipbl=2, sgsmodel=0, tconfig=2,
                    horizturb=0, irdamp=2, psolver=3, ptype=5, ihail=0, icor=int(v['coriolis'] != 0.0), betaplane=0,
                    lspgrad=int(v['coriolis'] != 0.0), eqtset=2, idiss=1, wbc=1, ebc=1, sbc=1, nbc=1, bbc=3, tbc=1,
                    isnd=7, iwnd=0, itern=0, iinit=0, irandp=1, iorigin=1, apmasscon=1),
        param3=param3,
        param6=dict(stretch_z=4, ztop=zw[-1]),
        param8=param8,
        param9=dict(BOX_OUTPUT),
        param11=dict(radopt=2, dtrad=float(u['radiation_s']), ctrlat=float(s['site']['lat_deg']), ctrlon=0.0),
        param12=dict(isfcflx=1, sfcmodel=2, oceanmodel=1, initsfc=9, season=1, tsk0=round(sea_k, 3),
                     tmn0=round(sea_k, 3), xland0=2.0, lu0=SEA_LAND_USE),
        param14=dict(dodomaindiag=True, diagfrq=float(u['diagnostics_s'])),
        param16=dict(restart_format=1, restart_filetype=2, restart_reset_frqtim=True),
        param19=dict(case['namelist']['param19']))


def context(v: dict, quantities: dict) -> dict:
    """What the registry tests for the case: the planet's quantities and the case's own, the world, the scenario and
    the case's resolved settings."""
    planet = derive.planet(v['world'], v['scenario'])
    q = {k: planet[k] for k in ('gravity_m_s2', 'scale_height_over_radius', 'chapman_horizon', 'column_mass_kg_m2',
                                'capillary_factor', 'soil_factor') if planet.get(k) is not None}
    q.update(quantities)
    return dict(q=q, world=copy.deepcopy(v['world']), scenario=copy.deepcopy(v['scenario']),
                settings=copy.deepcopy(v['settings']))


def assess(library: Library, study_id: str, name: str, *, store: Path, overrides: dict | None = None,
           registry_entries: list | None = None) -> dict:
    """A case's key, its forcing at the site (computed once and cached in the store) and the registry's checks on its
    context, before anything is written; the checks stop nothing here."""
    from climate.crm import gcm_site as gs
    keyed = case_key(library, study_id, name, store=Path(store))
    v, found = keyed['values'], keyed['forcing']
    s = v['settings']
    years = s['reference_model_years']
    run = gs.run_record(found['model'], found['topography'], solar_day_s=v['solar_day_s'], name=found['name'])
    files = keyed['inputs']['forcing']['files']
    f = forcing(run, years, gcm_site_of(s['site']), store=Path(store), files=files)
    zw = v['zw']
    damping_base = s['unscaled']['damping_base_fraction'] * zw[-1]
    quantities = dict(soil_layer_ratio=v['soil_dz1_m'] / (0.01 * v['read_set']['soil_factor']),
                      cm1_damping_clearance_m=gs.damping_clearance_m(f['convection'], damping_base),
                      lowest_level_pressure_hpa=f['surface']['pressure_pa'] / 100.0,
                      cm1_build_gravity_departure=abs(v['build_gravity_m_s2'] - v['gravity_m_s2']) / v['gravity_m_s2'])
    ctx = context(v, quantities)
    entries = registry_entries if registry_entries is not None else library.registry()
    checks = registry.evaluate(entries, 'cm1', ctx, overrides)
    return dict(keyed=keyed, run=run, files=files, forcing=f, damping_base_m=damping_base, context=ctx, checks=checks)


def write_case(library: Library, study_id: str, name: str, *, store: Path, overrides: dict | None = None,
               registry_entries: list | None = None) -> Path:
    """The case's folder in the store, written where the store lacks it, and named in the index. Refused where the
    registry stops it without an override (registry.Refused), and wherever gcm_site refuses its forcing."""
    from climate.crm import gcm_site as gs
    store = Path(store)
    keyed = case_key(library, study_id, name, store=store)
    k = keyed['key']
    target = store / 'cases' / f'cm1-{k[:16]}'
    if (target / 'case.json').is_file():
        checked(target, k)
        stages.name_link(store, study_id, name, target)
        return target
    a = assess(library, study_id, name, store=store, overrides=overrides, registry_entries=registry_entries)
    keyed, v, found, f, run, ctx = a['keyed'], a['keyed']['values'], a['keyed']['forcing'], a['forcing'], a['run'], \
        a['context']
    s, zw, damping_base, years, files = v['settings'], v['zw'], a['damping_base_m'], v['settings'][
        'reference_model_years'], a['files']
    checks = registry.require(a['checks'], v['where'])
    coupling = coupling_of(v)
    if coupling['coupling'] != 'imposed':
        coupling['mode'] = first_mode(run, years, store=store, files=files)
    upstream = keyed['upstream']
    if upstream is not None:
        from . import cm1_read
        coupling['reference'] = cm1_read.domain_mean_by_hour(upstream['run'], upstream['solar_days'],
                                                            bins=gs.BINS, source=f"{upstream['case']}'s own domain "
                                                            f"mean by local time, solar days {upstream['solar_days']}")
    air = gs.reference_air(f, v['gravity_m_s2'], zw[-1])
    u, c = s['unscaled'], s['coupling']
    try:
        inputs = gs.case_inputs(
            f, zw, air, gravity_m_s2=v['gravity_m_s2'], start_hour_deg=v['start_hour_deg'],
            solar_day_s=v['solar_day_s'], length_s=v['solar_day_s'], damping_base_m=damping_base,
            nudge_tau_s=float(u['nudge_tau_s']), wind_nudge_tau_s=float(u['wind_nudge_tau_s']),
            wind_from_m=0.0 if c['wind_pulled_from'] == 'ground' else None, inflow=INFLOWS[c['inflow']], **coupling)
    except ValueError as error:                       # gcm_site's refusals, the coupling 'wtg' among them for now
        raise SpecError(f"{v['where']}: gcm_site refuses its forcing: {error}") from None
    rain_ = rain(v, f)
    sea_k = float(f['surface']['ground_k'])
    sun = sunlight_w_m2(found['model'])
    entries_ = namelist_entries(v, inputs, rain_, sea_k, sun)
    texts = {'namelist.template': set_entries(template(), entries_), 'input_sounding': sounding(inputs['start'], zw,
                                                                                                 f['surface']),
             'input_grid_z': grid_text(zw), 'terluna_surface.txt': surface_text(sea_k)}
    texts.update({n: t for n, t in inputs['files'].items() if not n.startswith('lsnudge_')})
    texts.update({f'{WINDOWS}/{n}': t for n, t in inputs['files'].items() if n.startswith('lsnudge_')})
    if rain_['table'] is not None:
        texts[RAIN_TABLE] = rain_['table']
    window_s = inputs['record']['wind']['window_s']
    record = dict(
        study=study_id, case=name, settings=s, settings_hash=v['item'].settings_hash, delta=v['item'].delta,
        world=v['world']['id'], scenario=v['scenario']['id'],
        build=dict(key=keyed['inputs']['build'], world_constants=s['world_constants'], macros=v['macros'],
                   compiled_gravity_m_s2=v['build_gravity_m_s2']),
        values=dict(factors=v['factors'], scaled=v['scaled'], gravity_m_s2=v['gravity_m_s2'],
                    mole_fractions=v['fractions'], solar_day_s=v['solar_day_s'], declination_deg=v['declination_deg'],
                    start_hour_deg=v['start_hour_deg'], coriolis_1_s=v['coriolis'], soil_dz1_m=v['soil_dz1_m'],
                    sunlight_w_m2=sun, sunlight_source="the forcing run's GSOL0 (planet_namelist)", sea_k=sea_k,
                    sea_source="the GCM's mean ground temperature over the site's sea cells"),
        grid=dict(nx=s['columns']['nx'], ny=s['columns']['ny'], nz=len(zw) - 1, dx_m=v['scaled']['column_target_m'],
                  ztop_m=zw[-1], zw_m=zw),
        run=dict(length_s=v['length_s'], solar_days=v['solar_days'], restart_s=v['restart_s'],
                 segment_s=float(u['segment_s']), output_s=float(u['output_s']),
                 diagnostics_s=float(u['diagnostics_s']), stats_s=float(u['stats_s']),
                 read_solar_days=s.get('read_solar_days'),
                 windows=dict(folder=WINDOWS, bins=len([n for n in inputs['files'] if n.startswith('lsnudge_')]),
                              window_s=window_s, start_hour_deg=v['start_hour_deg'],
                              rule="the job wrapper writes each segment's windows, numbered from the one that holds "
                                   "the segment's start, from this solar day's windows at the same phase")),
        forcing=dict(pin=found['pin'], run=found['name'], years=years, gcm_site=inputs['record'],
                     season=dict(reference=s['coupling']['reference_season'],
                                 reason=s['coupling']['reference_season_reason'],
                                 records=inputs['record']['records'],
                                 rule="every record of the years, which gcm_site.site_forcing averages")),
        coupling=dict(settings=s['coupling'], passed={k: (val if k != 'reference' or not isinstance(val, dict)
                                                          else val.get('source')) for k, val in coupling.items()
                                                      if k != 'mode'},
                      mode={k: val for k, val in coupling.get('mode', {}).items() if k not in ('z_m', 'theta_k')}
                      if 'mode' in coupling else None),
        rain=rain_['record'], namelist=entries_)
    header = stages.header(SCHEMA, k, producer_=keyed['inputs']['producer'],
                           inputs=dict(build=keyed['inputs']['build'], forcing=keyed['inputs']['forcing'],
                                       upstream=keyed['inputs']['upstream'], settings=keyed['inputs']['settings'],
                                       environment=keyed['inputs']['environment']),
                           read_set=v['read_set'], evidence=EVIDENCE,
                           registry=checks, overrides=dict(overrides or {}), registry_context=ctx)
    _write(target, texts, header, record)
    stages.name_link(store, study_id, name, target)
    return target


def _write(target: Path, texts: dict, header: dict, record: dict) -> None:
    """The case's files and case.json written into a temporary folder beside `target`, made read-only and moved into
    place whole; a case of the same key that lands first stands."""
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = Path(tempfile.mkdtemp(prefix=f'.{target.name}.part-', dir=target.parent))
    try:
        files = {}
        for name, text in texts.items():
            path = partial / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            files[name] = stages.sha256_file(path)
        header['files'] = files
        stages.write_json(partial / 'case.json', dict(header=header, record=record))
        cm1_builds.common._read_only(partial)
        try:
            os.replace(partial, target)
        except OSError:
            if not (target / 'case.json').is_file():
                raise
            cm1_builds.common._remove(partial)
    except BaseException:
        cm1_builds.common._remove(partial)
        raise


def checked(target: Path, k: str | None = None) -> dict:
    """A case found in the store, once its header names the key and each file its recorded bytes; its case.json."""
    found = stages.read_json(Path(target) / 'case.json')
    if k is not None and found['header']['key'] != k:
        raise DataError(f"{target}: its header names key {found['header']['key']}, where its inputs give {k}")
    for name, digest in found['header']['files'].items():
        path = Path(target) / name
        if not path.is_file() or stages.sha256_file(path) != digest:
            raise DataError(f'{target}: its {name} differs from its header')
    return found


def recheck(case: dict, *, entries: list, overrides: dict | None = None) -> dict:
    """The registry evaluated anew on a written case's context, its quantities, world, scenario and settings as the
    case was written, as the job wrapper evaluates it before each run: with the case's own overrides and the run's
    together."""
    return registry.evaluate(entries, 'cm1', case['header']['registry_context'],
                             {**case['header'].get('overrides', {}), **(overrides or {})})
