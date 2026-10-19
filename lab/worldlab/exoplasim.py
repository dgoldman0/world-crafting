"""ExoPlaSim's adapter: the input files of a GCM run, written from the lab's specifications, derivations and
calibrations (lab/design/architecture.md, "Model adapters"; plan.md, stage 2).

The lab writes every namelist PlaSim reads. Each starts from its template in the pinned ExoPlaSim 3.4.2 archive
and takes the entries ExoPlaSim's own `configure` writes for the same world (exoplasim/__init__.py:2469-2966, coded
here for the settings the lab uses), then the switches of the lab's patch series (models/exoplasim/README.md) and
the calibrations the run reads. `configure_arguments` gives the arguments under which `configure` writes the same
namelists, which the tests run in the lab's environment; the entries the lab writes otherwise are its
`departures`, each with its reason.

A run's calibrations come from the stages that fit them. `Calibrations.identity()` takes each at its identity
default, the released model's own value, with the curved air's terms and the gas bands off, as a world's first run
does (plan.md); otherwise every calibration the run's switches use must be given. `resolve` gives the switches as
the build and the calibrations make them (world_spec.md, rule 7), which the run's record carries and the registry
tests.
"""
from __future__ import annotations

import functools
import hashlib
import io
import math
import tarfile
from dataclasses import dataclass, fields
from pathlib import Path

from . import derive, sunlight
from .data import DataError
from .geography import REFERENCE_LEVELS
from .spec import LAB, SpecError

ARCHIVE = LAB.parent / 'upstream' / 'exoplasim-3.4.2.tar.gz'
PINS = LAB.parent / 'models' / 'pins.sha256'
TEMPLATES = 'exoplasim-3.4.2/exoplasim/plasim/run/'
NAMELISTS = ('plasim_namelist', 'planet_namelist', 'radmod_namelist', 'rainmod_namelist', 'landmod_namelist',
             'oceanmod_namelist', 'icemod_namelist', 'seamod_namelist', 'surfmod_namelist', 'vegmod_namelist',
             'carbonmod_namelist', 'glacier_namelist', 'hurricane_namelist', 'fluxmod_namelist', 'miscmod_namelist',
             'aero_namelist')
EARTH_RADIUS_M = 6371220.0           # ExoPlaSim's unit of radius (world_spec.md, rule 7)
# ExoPlaSim's own molar masses, g/mol, and gas constant, from which configure computes GASCON
# (exoplasim/__init__.py:25-34, 2575-2581); its CO2 takes 44.01 g/mol, the lab's derivations 44.0095.
MOLAR_MASS = {'N2': 28.0134, 'O2': 31.9988, 'Ar': 39.948, 'CO2': 44.01}
GAS_CONSTANT = 8314.46261815324
STAR_FILES = ('sun.dat', 'sun_hr.dat')   # in the run's own folder: the namelist holds a file name in 80 characters
PLASIM_TH2OC = 0.024                 # PlaSim's own water continuum coefficient (radmod.f90:38)
ICE_BELOW_K = 235.15                 # patch 10's TICEOPT: cloud colder than -38 °C takes ice optics
SUN_CLOCKS = {'plasim': 0, 'model-day': 1, 'synodic': 2}             # patch 04's NSUNCLOCK
CLOUD_WATER = ('plasim', 'earth_path', 'full_column')                 # patch 02
TWILIGHT = ('none', 'full')                                           # patch 07: off, or the ledger's full terms
ICE_WEIGHTS = ('from-spectrum', 'patch-10')    # the planned patch 11's weights from the spectrum, or patch 10's own
GAS_BANDS = ('CO2 near infrared', 'O2 near infrared', 'O2 visible')   # patch 08's ZGASQ columns, in order
OZONE = {'none': 0, 'model-default': 1}                               # NO3: PlaSim's synthetic ozone is its own default
SCALE_BASES = ('identity', 'calibration', 'scenario')

# What configure writes for the features the lab leaves at configure's defaults: the vertical grid, output, the
# physics filters, the carbon cycle, vegetation, glaciers, aerosols, the ocean's zenith rule, soil, high-cadence
# output and storms (exoplasim/__init__.py:2469, 2600-2635, 2684, 2699-2730, 2747-2751, 2773-2775, 2790, 2819,
# 2831-2832, 2839, 2896, 2921-2924, 2951).
CONFIGURE_DEFAULTS = {
    'plasim_namelist': {'NOUTPUT': 1, 'NEQSIG': 0, 'DTTL': 0.0, 'NVEG': 0, 'FILTERKAPPA': 8.0, 'NFILTEREXP': 8,
                        'LANDHOSKN0': 15.0, 'L_AERO': 0, 'NHCADENCE': 0, 'HCSTARTSTEP': 320, 'HCENDSTEP': 576,
                        'HCINTERVAL': 4},
    'planet_namelist': {'NGENKEPLERIAN': 0},
    'radmod_namelist': {'NPBROADEN': 1, 'DESYNC': 0.0, 'NSIMPLEALBEDO': 1, 'NECHAM': 1, 'NECHAM6': 0},
    'landmod_namelist': {'NWETSOIL': 0, 'DSOILZ': (0.4, 0.8, 1.6, 3.2, 6.4)},
    'carbonmod_namelist': {'NCARBON': 0, 'NCO2EVOLVE': 0, 'VOLCANCO2': 50.0},
    'vegmod_namelist': {'NCVEG': 1, 'FORGROW': 1.0, 'RINIDAGG': 0.5, 'RINIDSC': 1.0, 'RINIDMR': 2.0, 'RINISOIL': 0.0,
                        'RINIVEG': 0.0},
    'glacier_namelist': {'NGLACIER': 0, 'GLACELIM': 2.0, 'ICESHEETH': -1.0},
    'hurricane_namelist': {'NSTORMS': 4},
}
# The entries the lab writes otherwise than configure for every world, each with its reason.
DEPARTURES = {
    ('plasim_namelist', 'NSTPW'): "the lab's output steps, whole means in each model day and year "
                                  '(derive.output_steps), where configure takes 7200 // the time step',
    ('radmod_namelist', 'STARFILE'): "the star's file by its name in the run's folder, where configure writes its "
                                     'path, since the namelist holds a file name in 80 characters',
    ('radmod_namelist', 'STARFILEHR'): 'as STARFILE',
}
CO2_FREE = (('radmod_namelist', 'CO2'), 'for air without CO2 the lab writes 0, where configure leaves a zero pCO2 out '
                                        'and writes its default of 300 ppm (exoplasim/__init__.py:2539, 2593)')
# The entries the lab adds to configure's, by name before any index: the random seed, the clear-sky and heating
# diagnostics, PlaSim's water continuum, and the patch series' switches and calibrations.
ADDITIONS = {
    'plasim_namelist': ('SEED', 'NDIAGCF', 'NDIAGGP'),
    'radmod_namelist': ('TH2OC', 'RAYSCALE', 'NSUNCLOCK', 'SWH2OSCALE', 'IRTOPDAY', 'IRTOPNIGHT', 'NTWILIGHT',
                        'NTWILW', 'ZMLUNAR', 'NGASBANDS', 'ZGASQ', 'ZGASW', 'ZMAIRLUNAR', 'NLWCORR', 'NICEOPT',
                        'TICEOPT'),
    'rainmod_namelist': ('CWGREF', 'CWSCALE', 'CONVDAY', 'RCRIT'),
}


# Calibrations and the sunlight's scale.

@dataclass(frozen=True)
class Ledger:
    """The curved air's terms for PlaSim (patch 07), from the ledger's stage. By solar elevation: the sunlight the
    curved air adds to the ground and to each layer, top first, per unit sunlight at the beam. The extra infrared
    each layer, top first, and the ground lose to space, W/m², and the temperatures it is given at. The coefficients
    (a, b, c) of the slant factor (μ + a)/(μ² + bμ + c) along the air's path (ZMLUNAR) and for well-mixed gases
    (ZMAIRLUNAR)."""
    elevation_deg: tuple
    ground: tuple
    layers: tuple
    escape_w_m2: tuple
    escape_temperature_k: tuple
    slant: tuple
    slant_air: tuple


@dataclass(frozen=True)
class Longwave:
    """The longwave correction by height (patch 09): the extra escape to space over land and over sea, W/m², for
    each layer, top first, and the ground, and the temperatures it is given at."""
    land: tuple
    sea: tuple
    temperature_k: tuple


@dataclass(frozen=True)
class Calibrations:
    """The fitted values a run reads (architecture.md, "Calibrations, envelopes and loops"). `sunlight_scale` is the
    target stage's, for a scenario whose scale follows its reference temperature; `gas_bands` holds patch 08's five
    coefficients for each of `GAS_BANDS`."""
    sunlight_scale: float | None = None
    rayleigh_scale: float | None = None        # RAYSCALE, patch 01
    water_absorption_scale: float | None = None   # SWH2OSCALE, patch 05
    water_continuum: float | None = None       # TH2OC
    ledger: Ledger | None = None
    gas_bands: tuple | None = None
    longwave: Longwave | None = None
    first_run: bool = False

    @classmethod
    def identity(cls) -> 'Calibrations':
        """A world's first run: every calibration at its identity default."""
        return cls(first_run=True)

    def __post_init__(self):
        given = [f.name for f in fields(self) if f.name != 'first_run' and getattr(self, f.name) is not None]
        if self.first_run and given:
            raise SpecError(f'a first run takes every calibration at its identity default, where {given} are given')
        for name in ('sunlight_scale', 'rayleigh_scale', 'water_absorption_scale', 'water_continuum'):
            value = getattr(self, name)
            if value is not None:
                _positive(value, f'calibration {name}')
        if self.gas_bands is not None and (len(self.gas_bands) != len(GAS_BANDS)
                                           or any(len(fit) != 5 for fit in self.gas_bands)):
            raise SpecError(f'gas_bands holds five coefficients for each of {GAS_BANDS}')
        if self.ledger is not None and (len(self.ledger.slant) != 3 or len(self.ledger.slant_air) != 3):
            raise SpecError("the ledger's slant factors each hold three coefficients, (a, b, c)")


@dataclass(frozen=True)
class TopOfAir:
    """The sunlight at the top of the air that GSOL0 takes, W/m², and its scale, with the scale's basis: `identity`
    in a first run, `calibration` from the target stage, or `scenario` as the scenario states it."""
    w_m2: float
    scale: float
    basis: str
    sunlight: dict | None = None


def top_of_air(world: dict, scenario: dict, calibrations: Calibrations, *, manifest=None, store=None) -> TopOfAir:
    """What the scenario's filter passes, times its scale. A scenario whose scale follows its reference temperature
    takes the target stage's, or 1 in a first run."""
    stated = scenario.get('sunlight', {}).get('scale')
    if stated == sunlight.TARGET_SCALE:
        if calibrations.first_run:
            scale, basis = 1.0, 'identity'
        elif calibrations.sunlight_scale is None:
            raise SpecError(f'{scenario.get("id")}: its sunlight scale follows its reference temperature, and the '
                            "target stage's scale is missing from the calibrations")
        else:
            scale, basis = calibrations.sunlight_scale, 'calibration'
    elif calibrations.sunlight_scale is not None:
        raise SpecError(f'{scenario.get("id")}: states its sunlight scale, {stated!r}, where the calibrations give '
                        "the target stage's")
    else:
        scale, basis = stated, 'scenario'
    light = sunlight.sunlight(world, scenario, manifest=manifest, store=store)
    return TopOfAir(light['filtered_w_m2'] * scale, scale, basis, light)


def _check_top(top: TopOfAir, scenario: dict, calibrations: Calibrations) -> float:
    """GSOL0, once the sunlight's scale agrees with the scenario and the calibrations."""
    stated = scenario.get('sunlight', {}).get('scale')
    if stated == sunlight.TARGET_SCALE:
        expected = ('identity', 1.0) if calibrations.first_run else ('calibration', calibrations.sunlight_scale)
    else:
        expected = ('scenario', stated)
    if (top.basis, top.scale) != expected:
        raise SpecError(f'{scenario.get("id")}: the sunlight at the top takes scale {top.scale!r} ({top.basis}), '
                        f'where the scenario and the calibrations give {expected[1]!r} ({expected[0]})')
    return _positive(top.w_m2, 'the sunlight at the top')


# Templates and the namelist format.

def templates(archive: Path = ARCHIVE, pins: Path = PINS) -> dict[str, str]:
    """The template namelists of the pinned ExoPlaSim archive, by file name, read from the bytes whose sha256
    matches the archive's pin in models/pins.sha256."""
    archive = Path(archive)
    try:
        stat = archive.stat()
    except FileNotFoundError:
        raise DataError(f'{archive}: the pinned ExoPlaSim archive is missing (models/pins.sha256)') from None
    return dict(_templates(str(archive), stat.st_size, stat.st_mtime_ns, str(pins)))


@functools.lru_cache(maxsize=4)
def _templates(path: str, size: int, mtime_ns: int, pins_path: str) -> tuple:
    pins = {}
    for line in Path(pins_path).read_text().splitlines():
        if line.strip() and not line.lstrip().startswith('#'):
            digest, _, name = line.strip().partition(' ')
            pins[name.strip()] = digest
    data = Path(path).read_bytes()
    digest, name = hashlib.sha256(data).hexdigest(), Path(path).name
    if pins.get(name) != digest:
        raise DataError(f'{path}: sha256 {digest} differs from its pin, {pins.get(name)}')
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
        return tuple((name, archive.extractfile(TEMPLATES + name).read().decode()) for name in NAMELISTS)


def parse(text: str) -> tuple[str, list[tuple[str, str]]]:
    """A namelist file's group and its entries in order, as ExoPlaSim writes them: one `NAME = value` a line between
    the `&group` line and `/END`, `&END` or `/`."""
    group, entries = None, []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.upper() in ('/END', '/', '&END'):
            break
        if stripped.startswith('&'):
            if group is not None:
                raise DataError(f'a second group, {stripped!r}, in the namelist of {group!r}')
            group = stripped[1:].strip()
            continue
        key, sep, value = stripped.partition('=')
        if group is None or not sep:
            raise DataError(f'a namelist line outside its group or without "=": {line!r}')
        if value.rstrip().endswith('/'):
            raise DataError(f"an entry and its group's end on one line: {line!r}")
        entries.append((key.strip(), value.strip()))
    if group is None:
        raise DataError('a namelist without its &group line')
    return group, entries


def text(value) -> str:
    """A value as the namelist holds it: integers and floats as Python writes them, as configure writes its own; a
    string in quotes; a tuple as its values joined by commas."""
    if isinstance(value, bool):
        raise SpecError(f'a switch is written as an integer, where the value is the bool {value!r}')
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise SpecError(f'a namelist value is finite, where it is {value!r}')
        return repr(float(value))
    if isinstance(value, str):
        return f"'{value}'"
    if isinstance(value, tuple):
        return ','.join(text(v) for v in value)
    raise SpecError(f'a namelist value is a number, a string or a tuple, where it is {value!r}')


def merged(template: str, entries: dict) -> str:
    """A namelist file: the template's entries in order, each that `entries` names taking its value, then the rest
    of `entries` in their order. Names match without regard to case, as Fortran reads them."""
    group, lines = parse(template)
    wanted = {name.upper(): name for name in entries}
    if len(wanted) != len(entries):
        raise SpecError(f'{group}: entries repeat a name in another case: {sorted(entries)}')
    written, out = set(), []
    for key, value in lines:
        name = wanted.get(key.upper())
        if name is None:
            out.append((key, value))
        elif name not in written:
            out.append((key, text(entries[name])))
            written.add(name)
    out += [(name, text(value)) for name, value in entries.items() if name not in written]
    return f' &{group}\n' + ''.join(f' {key} = {value}\n' for key, value in out) + ' /END\n'


# The switches as the build and the calibrations make them.

def series(run: dict) -> tuple[str, ...]:
    """The patches of the run's build, in order: the series file its `patches` names, or the list it gives."""
    patches = run['patches']
    if isinstance(patches, str):
        return tuple(line.strip() for line in (LAB.parent / patches).read_text().splitlines() if line.strip())
    return tuple(patches)


def resolve(run: dict, calibrations: Calibrations) -> dict:
    """The run's switches as its build and calibrations make them (world_spec.md, rule 7): `from-spectrum` ice
    weights take patch 10's constant weights while the series stops before patch 11, and a first run holds the
    curved air's terms and the gas bands off."""
    switches = dict(run['switches'])
    if switches.get('ice_weights') not in ICE_WEIGHTS:
        raise SpecError(f'switches.ice_weights is one of {ICE_WEIGHTS}, where the run states '
                        f'{switches.get("ice_weights")!r}')
    if switches['ice_weights'] == 'from-spectrum' and not any(p.startswith('11-') for p in series(run)):
        switches['ice_weights'] = 'patch-10'
    if calibrations.first_run:
        switches.update(twilight='none', gas_bands=False)
    return switches


# The entries.

def namelists(world: dict, scenario: dict, run: dict, *, top: TopOfAir,
              calibrations: Calibrations) -> dict[str, dict]:
    """The entries the lab sets in each namelist for one GCM run, by file and name: configure's for the same world,
    then the patch series' switches and the calibrations. `run` holds the run's resolved settings, its model's
    defaults with the study's changes, and `top` the sunlight at the top of the air (`top_of_air`)."""
    where = scenario.get('id', 'the scenario')
    air, water = scenario['air'], scenario['water']
    if 'locked_to' in world['rotation'] or world.get('surface', {}).get('geometry') == 'ocean':
        raise SpecError(f'{world["id"]}: rotation locked to the star and a surface all ocean are fields still to add '
                        '(world_spec.md), which the adapter writes once they are coded')
    if air.get('reference_level') not in REFERENCE_LEVELS:
        raise SpecError(f'{where}: PlaSim takes its surface pressure at the level its heights start from, '
                        f'{" or ".join(REFERENCE_LEVELS)}, where the scenario states {air.get("reference_level")!r}')
    if air.get('water_vapour') != 'prognostic':
        raise SpecError(f'{where}: PlaSim carries water vapour as a prognostic field, where the scenario states '
                        f'{air.get("water_vapour")!r}')
    if air.get('ozone') not in OZONE:
        raise SpecError(f'{where}: the ozone is one of {tuple(OZONE)}, where the scenario states {air.get("ozone")!r}')
    ocean = water.get('ocean', {})
    if ocean.get('kind') != 'slab':
        raise SpecError(f'{where}: ExoPlaSim runs a slab ocean, where the scenario states {ocean.get("kind")!r}')
    switches = resolve(run, calibrations)
    g = derive.gravity(world)
    cal = derive.calendar(world, run)
    orbit, rotation = world['orbit'], world['rotation']
    entries = {name: dict(CONFIGURE_DEFAULTS.get(name, {})) for name in NAMELISTS}

    plasim = entries['plasim_namelist']
    plasim.update(PSURF=_positive(air['surface_pressure_pa'], f'{where}: air.surface_pressure_pa'),
                  MPSTEP=float(run['timestep_min']), NSTPW=cal['steps_per_mean'],
                  N_DAYS_PER_YEAR=cal['n_days_per_year'], N_RUN_STEPS=cal['run_steps_per_year'],
                  SEED=_integer(run['seed'], 'seed'), NDIAGCF=_switch(run['clear_sky'], 'clear_sky'),
                  NDIAGGP=_switch(run['heating_diagnostics'], 'heating_diagnostics'))

    planet = entries['planet_namelist']
    planet.update(GSOL0=_check_top(top, scenario, calibrations), GASCON=gas_constant(scenario), GA=g,
                  PLARAD=float(world['body']['radius_m']), SIDEREAL_YEAR=orbit['sidereal_year_days'] * derive.DAY_S,
                  ECCEN=float(orbit['eccentricity']), OBLIQ=float(rotation['obliquity_deg']),
                  NFIXORB=_switch(run['fixed_orbit'], 'fixed_orbit'))
    perihelion = perihelion_longitude(world)
    if perihelion is not None:
        planet['MVELP'] = perihelion
    if cal['rotationperiod'] != 1.0:
        planet['ROTSPD'] = 1.0 / cal['rotationperiod']

    radmod = entries['radmod_namelist']
    radmod.update(CO2=_nonnegative(air['co2_ppm'], f'{where}: air.co2_ppm'),
                  NRADICE=_switch(ocean['sea_ice'], 'water.ocean.sea_ice'), NO3=OZONE[air['ozone']], NSTARFILE=1,
                  STARFILE=STAR_FILES[0], STARFILEHR=STAR_FILES[1])
    radmod.update(_radiation_switches(scenario, switches, calibrations, where))

    rainmod = entries['rainmod_namelist']
    reference, scale = cloud_water(switches['cloud_water'], g)
    day = switches['convective_day_s']
    if isinstance(day, bool) or not isinstance(day, (int, float)) or not day >= 0:
        raise SpecError(f'{where}: switches.convective_day_s is 0 (the model day) or a number of seconds, where the '
                        f'run states {day!r}')
    rainmod.update(CWGREF=reference, CWSCALE=scale, CONVDAY=float(day))
    rcrit = switches['surface_cloud_rcrit']
    if isinstance(rcrit, bool) or not isinstance(rcrit, (int, float)) or not 0.0 <= rcrit < 1.0:
        raise SpecError(f"{where}: switches.surface_cloud_rcrit is 0 (PlaSim's own) or lies below 1, where the run "
                        f'states {rcrit!r}')
    if rcrit > 0.0:                                   # the lowest layer is the last of RCRIT
        rainmod[f'RCRIT({_integer(run["levels"], "levels")})'] = float(rcrit)

    albedo = scenario['land']['albedo']
    if albedo != 'model-default':
        albedo = _positive(albedo, f'{where}: land.albedo')
        entries['landmod_namelist'].update(ALBLAND=albedo, DGROUNDALB=(albedo, albedo))
    entries['oceanmod_namelist']['MLDEPTH'] = _positive(ocean['mixed_layer_m'], f'{where}: water.ocean.mixed_layer_m')
    return {name: values for name, values in entries.items() if values}


def _radiation_switches(scenario: dict, switches: dict, cal: Calibrations, where: str) -> dict:
    """The radiation's patch switches and calibrations: patches 01 and 04 to 10, and PlaSim's water continuum."""
    out = {}
    if switches['sun_clock'] not in SUN_CLOCKS:
        raise SpecError(f'{where}: switches.sun_clock is one of {tuple(SUN_CLOCKS)}, where the run states '
                        f'{switches["sun_clock"]!r}')
    out['NSUNCLOCK'] = SUN_CLOCKS[switches['sun_clock']]
    if switches['twilight'] not in TWILIGHT:
        raise SpecError(f'{where}: switches.twilight is one of {TWILIGHT}, where the run states '
                        f'{switches["twilight"]!r}')
    if switches['top_infrared'] != 'from-scenario':
        raise SpecError(f"{where}: switches.top_infrared takes the scenario's stated infrared, where the run asks "
                        f"{switches['top_infrared']!r}; the glow producer comes with plan stage 5")
    infrared = scenario['forcing']['top_infrared_w_m2']
    out.update(IRTOPDAY=_nonnegative(infrared['day'], f'{where}: forcing.top_infrared_w_m2.day'),
               IRTOPNIGHT=_nonnegative(infrared['night'], f'{where}: forcing.top_infrared_w_m2.night'))
    twilight = switches['twilight'] == 'full'
    gas_bands = _switch(switches['gas_bands'], 'switches.gas_bands') == 1
    longwave = _switch(switches['longwave_correction'], 'switches.longwave_correction') == 1
    if cal.first_run:
        if longwave:
            raise SpecError(f'{where}: a first run takes the longwave correction off, where the run switches it on')
        out.update(RAYSCALE=1.0, SWH2OSCALE=1.0, TH2OC=PLASIM_TH2OC, NTWILIGHT=0, NTWILW=0, NGASBANDS=0, NLWCORR=0)
    else:
        needed = {'rayleigh_scale': True, 'water_absorption_scale': True, 'water_continuum': True,
                  'ledger': twilight or gas_bands, 'gas_bands': gas_bands, 'longwave': longwave}
        missing = [name for name, wanted in needed.items() if wanted and getattr(cal, name) is None]
        if missing:
            raise SpecError(f'{where}: the run reads calibrations {missing}, which are missing')
        out.update(RAYSCALE=float(cal.rayleigh_scale), SWH2OSCALE=float(cal.water_absorption_scale),
                   TH2OC=float(cal.water_continuum), NTWILIGHT=int(twilight), NTWILW=int(twilight),
                   NGASBANDS=int(gas_bands), NLWCORR=int(longwave))
        if twilight:
            out.update({f'ZMLUNAR({i})': float(x) for i, x in enumerate(cal.ledger.slant, 1)})
        if gas_bands:
            for j, fit in enumerate(cal.gas_bands, 1):
                out.update({f'ZGASQ({i},{j})': float(x) for i, x in enumerate(fit, 1)})
            mass = derive.zgasw(derive.mole_fractions(scenario))
            out.update({'ZGASW(1)': mass['CO2'], 'ZGASW(2)': mass['O2']})
            out.update({f'ZMAIRLUNAR({i})': float(x) for i, x in enumerate(cal.ledger.slant_air, 1)})
    ice = _switch(switches['ice_optics'], 'switches.ice_optics')
    out['NICEOPT'] = ice
    if ice:
        out['TICEOPT'] = ICE_BELOW_K
    return out


def perihelion_longitude(world: dict) -> float | None:
    """PlaSim's MVELP: the orbit's longitude of perihelion from the vernal equinox, which an eccentric orbit states;
    a circular orbit may leave it out, and the template's value then stands."""
    orbit, where = world['orbit'], world.get('id', 'the world')
    value = orbit.get('perihelion_longitude_deg')
    if value is None:
        if orbit['eccentricity'] > 0.0:
            raise SpecError(f"{where}: an eccentric orbit states its longitude of perihelion, "
                            "orbit.perihelion_longitude_deg, where PlaSim's template holds Earth's")
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0.0 <= value < 360.0:
        raise SpecError(f'{where}: orbit.perihelion_longitude_deg lies from 0 to 360°, where the world states {value!r}')
    return float(value)


def gas_constant(scenario: dict) -> float:
    """GASCON as configure computes it: ExoPlaSim's gas constant over the mean of its own molar masses, weighted by
    the air's mole fractions (world_spec.md, rule 7)."""
    fractions = derive.mole_fractions(scenario)
    return GAS_CONSTANT / sum(x * MOLAR_MASS[gas] for gas, x in fractions.items())


def cloud_water(choice: str, gravity_m_s2: float) -> tuple[float, float]:
    """Patch 02's CWGREF and CWSCALE: the gravity at which the cloud-water formula counts heights and precipitable
    water (0, the planet's own) and a multiplier on the water. `earth_path` gives each cloud the water path it holds
    at the same pressures on Earth; `full_column` keeps the mixing ratio over the whole column."""
    if choice == 'plasim':
        return 0.0, 1.0
    if choice == 'earth_path':
        return derive.STANDARD_G, gravity_m_s2 / derive.STANDARD_G
    if choice == 'full_column':
        return derive.STANDARD_G, 1.0
    raise SpecError(f'switches.cloud_water is one of {CLOUD_WATER}, where the run states {choice!r}')


def departures(scenario: dict) -> dict:
    """The entries the lab writes otherwise than configure for this scenario, with their reasons: `DEPARTURES`, and
    the CO2 of air without it."""
    out = dict(DEPARTURES)
    if scenario['air']['co2_ppm'] == 0:
        out[CO2_FREE[0]] = CO2_FREE[1]
    return out


def configure_arguments(world: dict, scenario: dict, run: dict, *, top: TopOfAir, starspec: str,
                        landmap: str | None = None, topomap: str | None = None) -> dict:
    """The arguments under which ExoPlaSim's own configure writes the namelists `namelists` gives, the scenario's
    `departures` and the patch series' switches aside: what Terluna's runner passed (exoplasim_run.py:1018-1024),
    from the lab's derivations."""
    cal = derive.calendar(world, run)
    pressures = derive.partial_pressures_bar(scenario)
    ocean, albedo = scenario['water']['ocean'], scenario['land']['albedo']
    return dict(flux=top.w_m2, starspec=starspec, **pressures, gravity=derive.gravity(world),
                radius=world['body']['radius_m'] / EARTH_RADIUS_M, rotationperiod=cal['rotationperiod'],
                synchronous=False, year=world['orbit']['sidereal_year_days'],
                eccentricity=world['orbit']['eccentricity'], obliquity=world['rotation']['obliquity_deg'],
                lonvernaleq=perihelion_longitude(world), fixedorbit=bool(run['fixed_orbit']), landmap=landmap,
                topomap=topomap, mldepth=ocean['mixed_layer_m'], seaice=bool(ocean['sea_ice']),
                ozone=bool(OZONE[scenario['air']['ozone']]), soilalbedo=None if albedo == 'model-default' else albedo,
                timestep=run['timestep_min'], snapshots=None, runsteps=cal['run_steps_per_year'])


# Writing.

def write_namelists(folder: Path, entries: dict[str, dict], *, archive: Path = ARCHIVE) -> dict[str, str]:
    """Write every namelist PlaSim reads into `folder`, each its template with the lab's entries, and return each
    file's sha256."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    unknown = sorted(set(entries) - set(NAMELISTS))
    if unknown:
        raise SpecError(f"entries for files outside ExoPlaSim's namelists: {unknown}")
    written = {}
    for name, template in templates(archive).items():
        content = merged(template, entries.get(name, {}))
        (folder / name).write_text(content)
        written[name] = hashlib.sha256(content.encode()).hexdigest()
    return written


def _switch(value, name: str) -> int:
    if not isinstance(value, bool):
        raise SpecError(f'{name} is true or false, where the run states {value!r}')
    return int(value)


def _integer(value, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise SpecError(f'{name} is an integer, where the run states {value!r}')
    return value


def _positive(value, where: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not value > 0:
        raise SpecError(f'{where} is a positive number, where it is {value!r}')
    return float(value)


def _nonnegative(value, where: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise SpecError(f'{where} is a number from 0 up, where it is {value!r}')
    return float(value)
