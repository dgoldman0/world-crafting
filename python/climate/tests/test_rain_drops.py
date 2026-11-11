"""PlaSim's rain evaporated from its drops (climate/gcm/rain_drops.py and patch 14 of models/exoplasim/patches): for the
Open Moon's air the settings are Terluna's and the Python copy gives the numbers of Terluna's module on its test
columns; Morrison's closures are read on their lines of the pinned CM1 source and in the patch, which contains none of
the Moon's numbers; on a power law's closed forms the copy's rates, its midpoint steps through a layer and its three
birth rules agree with arithmetic written out by hand, at the Moon's gravity and Earth's; the copy keeps each column's
water and evaporates rain in unsaturated air alone; in saturated air the drops grow toward the breakup size and stop
there; mkrain with the patch, taken from the series applied to the pinned source and compiled with ExoPlaSim's flags
against a stub of PlaSim's module, reads the table that fall_law.table_text writes and gives the copy's tendencies and
precipitation to 1e-10 under every birth rule, on lunar columns of fifteen levels and Earth-like columns of ten, also
with rain falling hard into dry air at extreme sizes; with nevapprec 1 or 0 it prints every digit the mkrain before it
prints, under ExoPlaSim's flags and under -O3 -march=native; it stops on a setting or a table it cannot take; the
patch declares, reads and broadcasts each name once; and the patched rainmod.f90 compiles with PlaSim's modules.

Brought from Terluna's climate/tests/test_rain_drops.py at 39c5ee04 (python/provenance.json): the Fortran comes from
the lab's patch series, where Terluna's came from its runner's edit lists, and the fall law from a table in the
harness's folder, where Terluna's patch compiled the Moon's in."""
import math
import re
import subprocess

import numpy as np
import pytest

from shared.constants import MOON_SURFACE_GRAVITY, STANDARD_GRAVITY
from atmosphere.radiative_convective.thermodynamics import DryAir, earthlike_air
from atmosphere.rain import breakup, drops, fall_law, morrison
from climate.gcm import rain_drops as rd
from climate.tests.test_surface_gust import FORTRAN, GCM_FLAGS, HALF15, num, plasim_half

RAIN_PATCH = '14-rain-from-drop-sizes.patch'    # in models/exoplasim/patches; series_sources applies the series
# gfortran with products fused into multiply-adds on a processor that has them, beside ExoPlaSim's own flags
NATIVE_FLAGS = ('-O3', '-march=native', '-cpp', '-fdefault-real-8')
# PlaSim's constants as a run of each world holds them: the Open Moon's air as Terluna's test takes it, and Earth's
PHYSICS = dict(ALV=2.5008e6, ALS=2.8345e6, ra1=610.78, ra2=17.2693882, ra4=35.86, TMELT=273.16, deltsec=1800.0,
               deltsec2=3600.0, gamma=0.01)
LUNAR = dict(PHYSICS, ga=1.6242188765608128, gascon=288.3767, acpd=288.3767 / 0.286, ADV=0.8546,
             rdbrv=288.3767 / 461.51)
EARTH = dict(PHYSICS, ga=9.80665, gascon=287.05, acpd=1004.6, ADV=0.8608, rdbrv=287.05 / 461.51)
# The Open Moon's air at 2 m as Terluna's rain products take it: the median over land of its resort climate at 301 K
# (atmosphere/rain/results/rain_drops.json at 39c5ee04), the air of atmosphere/tests/test_rain_fall_law.py.
RESORT_K, RESORT_HUMIDITY = 300.4274941880408, 0.6083150136678477
# Births made up for Earth's columns, where no calibration exists: the tests read the code's arithmetic from them.
EARTH_BIRTHS = dict(rule='share', new_rain_m=0.4e-3, melted_rain_m=0.8e-3)
ONE_SIZE_M = 0.465e-3                           # the one size of Terluna's first two birth rules, CM1's sea box's
# The three birth rules as Terluna's module names them, by the settings each changes
BIRTH_RULES = {'one_size': dict(nrdrop_join=0, rdrop_melt=ONE_SIZE_M, rdrop_warm=ONE_SIZE_M),
               'join': dict(nrdrop_join=1, rdrop_melt=ONE_SIZE_M, rdrop_warm=ONE_SIZE_M),
               'share': dict(nrdrop_join=2, rdrop_melt=2.95e-3, rdrop_warm=0.439e-3)}
GAMMA_48, GAMMA_18, GAMMA_29 = math.gamma(4.8), math.gamma(1.8), math.gamma(2.9)


class Base:
    """What `columns` builds a world's columns from: PlaSim's constants, the half levels, the mean surface pressure, the
    lapse of the temperature with height and the rate at which rain forms, against the Moon's."""

    def __init__(self, constants, half, pressure_pa, lapse_k_m=0.0, rate=1.0):
        self.c, self.half, self.pressure_pa, self.lapse_k_m, self.rate = constants, half, pressure_pa, lapse_k_m, rate


class World(Base):
    """A world's columns with what the scheme takes for its air: the settings, the namelist's six entries, and the
    fall law, as computed (`exact`) and as the model reads it from the table's text (`law`)."""

    def __init__(self, constants, half, pressure_pa, lapse_k_m, rate, column, births):
        super().__init__(constants, half, pressure_pa, lapse_k_m, rate)
        self.found = rd.settings(column, births)
        self.exact = rd.law_of(self.found['table'])
        self.law = rd.law_from_text(fall_law.table_text(self.found['table']))
        self.prm = {name: self.found['namelist'][name] for name in rd.NAMELIST_NAMES}


@pytest.fixture(scope='module')
def moon():
    air = drops.Column(gravity_m_s2=MOON_SURFACE_GRAVITY, surface_pressure_pa=1.2 * breakup.ATMOSPHERE_PA,
                       surface_temperature_k=RESORT_K, surface_relative_humidity=RESORT_HUMIDITY,
                       air=earthlike_air(1.2 * breakup.ATMOSPHERE_PA, 400.0))
    return World(LUNAR, HALF15, 121500.0, 1.15e-3, 1.0, air, rd.TERLUNA_OPEN_MOON_BIRTHS)


@pytest.fixture(scope='module')
def earth():
    air = drops.Column(gravity_m_s2=STANDARD_GRAVITY, surface_pressure_pa=breakup.ATMOSPHERE_PA,
                       surface_temperature_k=RESORT_K, surface_relative_humidity=RESORT_HUMIDITY,
                       air=DryAir(breakup.ATMOSPHERE_PA))
    return World(EARTH, plasim_half(), 101325.0, 6.5e-3, 6.0, air, EARTH_BIRTHS)


def saturation(c, t, p):
    """PlaSim's saturation mixing ratio as mkrain forms it (before its correction factor)."""
    return c['rdbrv'] * c['ra1'] * np.exp(c['ra2'] * (t - c['TMELT']) / (t - c['ra4'])) / p


def columns(world, n=8, seed=5, ground_freezing=False):
    """Columns (top first) on the world's levels: a slow cooling from about 300 K, the freezing level near 24 km on the
    Moon's fifteen levels and near 4 km on Earth's ten, the air 55-100% humid and some layers a little supersaturated,
    snow forming above the freezing level and rain below it in most columns, none in some. With the Moon's values the
    columns are those of Terluna's test, draw for draw."""
    c = world.c
    rng = np.random.default_rng(seed)
    half = np.asarray(world.half, float)
    nlev = half.size
    edges = np.r_[0.0, half]
    sigma = 0.5 * (edges[1:] + edges[:-1])
    dsigma = np.diff(edges)
    ps = world.pressure_pa + rng.uniform(-3000.0, 1000.0, n) * (world.pressure_pa / 121500.0)
    z = -c['gascon'] * 285.0 / c['ga'] * np.log(sigma)
    t = (300.5 - world.lapse_k_m * z)[None, :] + rng.uniform(-1.0, 1.0, (n, nlev))
    t = np.maximum(t, 190.0)
    p = ps[:, None] * sigma[None, :]
    rh = np.where(rng.uniform(size=(n, nlev)) < 0.1, rng.uniform(1.0, 1.02, (n, nlev)),
                  rng.uniform(0.55, 0.97, (n, nlev)))
    q = rh * saturation(c, t, p)
    cold = t <= c['TMELT']
    raining = rng.uniform(size=n) < 0.75
    form = np.where(rng.uniform(size=(n, nlev)) < 0.6, rng.uniform(0.0, 4e-10, (n, nlev)) * world.rate, 0.0) \
        * raining[:, None]
    conv = form * rng.uniform(0.3, 1.0, (n, nlev))
    large = form - conv
    ground = np.where(ground_freezing & (rng.uniform(size=n) < 0.5), 270.0, t[:, -1] + 1.0)
    return dict(dt=np.c_[t, ground], dq=q, dp=ps, sigma=sigma, dsigma=dsigma,
                dtdt=rng.uniform(-2e-5, 1e-5, (n, nlev)), dqdt=rng.uniform(-2e-8, 2e-8, (n, nlev)),
                dprcl=conv, dprscl=np.where(cold, conv, 0.0), dprll=large, dprsll=np.where(cold, large, 0.0))


def copy(s):
    return {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in s.items()}


def warm_column(world, formed: dict, humidity=1.01, kelvin=290.0):
    """One column all above freezing, at one humidity against the saturation mkrain forms, that makes convective rain
    as rain in the layers `formed` names (level: sigma-weighted rate), with no tendencies before mkrain."""
    s = columns(world, n=1, seed=8)
    s['dt'][:] = kelvin
    raw = saturation(world.c, s['dt'][:, :-1], s['dp'][:, None] * s['sigma'][None, :])
    s['dq'] = humidity * raw / (1.0 - (1.0 / world.c['rdbrv'] - 1.0) * raw)
    for key in ('dprcl', 'dprscl', 'dprll', 'dprsll', 'dtdt', 'dqdt'):
        s[key][:] = 0.0
    for level, rate in formed.items():
        s['dprcl'][0, level] = rate
    return s


def power_law_table(gravity):
    """The fall-law table of Morrison's own power law at a gravity, V = AR (g/9.81)^0.6 D^0.8 in the reference air,
    by its closed forms: the law's coefficient and exponent, and the table as fall_law.table gives one."""
    a, b = morrison.FALL_COEFFICIENT * morrison.gravity_factor(gravity), morrison.FALL_EXPONENT
    first, last, points = fall_law.TABLE_LAMBDA
    found = np.log(fall_law.closed_forms(a, b, fall_law.table_lambda()))
    return a, b, dict(ln_lambda_first=math.log(first), ln_lambda_step=math.log(last / first) / (points - 1),
                      points=points, ln_mass_weighted=list(found[0]), ln_number_weighted=list(found[1]),
                      ln_ventilation=list(found[2]))


# ------------------------------------------------------------------------------------------------------ Python

def test_for_the_open_moons_air_the_settings_and_the_copys_numbers_are_terlunas(moon):
    """The entries Terluna's patch compiled in come back from the Open Moon's air, and on the eight columns of
    Terluna's test at seed 5 the copy gives the sums that Terluna's module at 39c5ee04 gave on 11 November 2026, run
    in place, under each of its three birth rules. That day the copy gave every field of that module bit for bit on
    72 columns, three seeds under each rule (PROVENANCE.md)."""
    assert moon.found['namelist'] == dict(nevapprec=2, nrdrop_join=2, rdrop_warm=0.439e-3, rdrop_melt=2.95e-3,
                                          rdrop_ksc=2.919, rdrop_rhoexp=0.687, rdrop_step=1000.0)
    assert moon.found['births'] == rd.TERLUNA_OPEN_MOON_BIRTHS
    limits = moon.found['limits']
    assert limits['mean_diameter_cap_m'] == pytest.approx(6.88e-3, rel=1e-3)                  # the lunar cap, 6.88 mm
    assert limits['fall_speed_cap_m_s'] == pytest.approx(5.804773506060524, rel=1e-12)        # 9.1 (g/9.81)^(1/4)
    assert limits['mean_diameter_floor_m'] == pytest.approx(20.0e-6, rel=1e-12)
    assert limits['breakup']['equilibrium_m'] * 1e3 == pytest.approx(1.6751368897938144, rel=1e-12)
    inv = rd.inverse(LUNAR['ga'], moon.exact)
    assert (inv['lnlam_min'], inv['lnlam_max']) == pytest.approx((4.978948229445036, 10.819778284410283), rel=1e-14)
    for d in (0.1e-3, 0.465e-3, 1.68e-3, 4e-3):                                              # the inverse reads back
        assert math.exp(-rd.slope_of(math.log(rd.number_per_flux(d, inv)), inv)) == pytest.approx(d, rel=1e-6)
    pins = {'one_size': (0.0002945641210863264, 0.00035341366079503486, 87.88016188921914),
            'join': (0.0005407324097038158, 0.00010724537217754544, 3.221403891386914),
            'share': (0.0003567742312863494, 0.00029120355059501183, 47.60457268727663)}
    for rule, (rain, evaporated, number) in pins.items():
        s = columns(moon, seed=5)
        out = rd.mkrain(s, LUNAR, dict(moon.prm, **BIRTH_RULES[rule]), moon.exact)
        mass = s['dp'] / LUNAR['ga']
        found = (((out['dprc'] + out['dprl'] - out['dprs']) * 1000.0).sum(),                 # kg/m2/s at the ground
                 ((out['rain_evaporation'] * s['dsigma'][None, :]).sum(axis=1) * mass).sum(), out['number'].sum())
        assert found == pytest.approx((rain, evaporated, number), rel=1e-12), rule
    # The model reads the table from a text of ten significant digits, which moves these sums by parts in 1e8.
    assert np.abs(moon.law['table'] - moon.exact['table']).max() < 1.0e-8
    assert (moon.law['x0'], moon.law['dx']) == pytest.approx((moon.exact['x0'], moon.exact['dx']), rel=1e-9)
    read = rd.mkrain(columns(moon, seed=5), LUNAR, moon.prm, moon.law)
    assert read['number'].sum() == pytest.approx(pins['share'][2], rel=1e-7)
    for text, match in (('', 'first line'), ('rain 4.6 0.02\n', 'first line'), ('1 4.6 0.02\n1 1 1\n', 'two rows'),
                        ('2 4.6 0.0\n1 1 1\n1 1 1\n', 'positive step'), ('2 4.6 0.02\n1 1 1\n', 'states 2 rows'),
                        ('2 4.6 0.02\n1 1 1\n1 1 1\n1 1 1\n', 'states 2 rows')):
        with pytest.raises(ValueError, match=match):
            rd.law_from_text(text)


def test_at_earths_gravity_and_pressure_the_limits_are_morrisons(earth):
    """In Earth's air under standard gravity the density exponent is nil and the rate Morrison's own, and at CM1's
    9.81 m/s2 the scheme's range and cap are Morrison's own."""
    assert earth.found['namelist'] == dict(nevapprec=2, nrdrop_join=2, rdrop_warm=0.4e-3, rdrop_melt=0.8e-3,
                                           rdrop_ksc=5.78, rdrop_rhoexp=0.0, rdrop_step=1000.0)
    assert rd.limits(morrison.GRAVITY) == dict(lnlam_min=math.log(1.0 / 2800.0e-6), lnlam_max=math.log(1.0 / 20.0e-6),
                                               vcap=9.1)
    assert math.exp(-rd.limits(STANDARD_GRAVITY)['lnlam_min']) == pytest.approx(2.8e-3, rel=2e-4)
    for births, match in ((dict(rule='largest', new_rain_m=1e-3, melted_rain_m=1e-3), 'birth rule'),):
        with pytest.raises(ValueError, match=match):
            rd.settings(None, births)
    for change, match in ((dict(rdrop_warm=0.0), 'positive'), (dict(rdrop_melt=-1e-3), 'positive'),
                          (dict(nrdrop_join=3), '0, 1 or 2'), (dict(rdrop_ksc=-1.0), 'zero or more'),
                          (dict(rdrop_step=0.0), 'positive')):
        with pytest.raises(ValueError, match=match):
            rd.mkrain(columns(earth), EARTH, dict(earth.prm, **change), earth.law)
    falling = dict(earth.found['table'], ln_number_weighted=[-6.0 * (math.log(100.0) + i * math.log(1000.0) / 300)
                                                               for i in range(301)])
    with pytest.raises(ValueError, match='fails to rise'):
        rd.inverse(EARTH['ga'], rd.law_of(falling))
    with pytest.raises(ValueError, match='two rows or more'):
        rd.law_of(dict(earth.found['table'], ln_lambda_step=0.0))


def test_the_closures_are_morrisons_on_the_pinned_source_and_in_the_patch(cm1_series, series_sources):
    """Morrison's evaporation closures on their lines of the pinned cm1r22.0, as released, and the same numbers as the
    patch declares them; the patch's defaults are Earth's self-collection and no density exponent, its two birth
    sizes are left for a run to state, and its text contains none of the Moon's numbers."""
    text = cm1_series.source('morrison.F', None)
    assert (morrison.WATER_DENSITY, morrison.VAPOUR_DIFFUSIVITY, morrison.VISCOSITY) == (997.0, (8.794e-5, 1.81),
                                                                                         (1.496e-6, 120.0))
    assert morrison.SELF_COLLECTION_FLOOR == 1.0e-8
    for line, count in (('         RHOW = 997.\n', 1), ('            MU(K) = 1.496E-6*T3D(K)**1.5/(T3D(K)+120.)\n', 1),
                        ('            DV(K) = 8.794E-5*T3D(K)**1.81/PRES(K)\n', 1),
                        ('\n         IF (QR3D(K).GE.1.E-8) THEN\n! v1.4\n! seifert and beheng\n', 2),
                        ('            AB(K) = 1.+DQSDT*XXLV(K)/CPM(K)\n', 1)):
        assert text.count(line) == count, line
    assert morrison.REFERENCE_DENSITY == 85000.0 / (287.04 * 273.15) == pytest.approx(1.0841148653626271, rel=1e-15)
    added = '\n'.join(series_sources.added(RAIN_PATCH))
    declared = '\n'.join(line for line in series_sources.added(RAIN_PATCH) if re.match(r' +(integer|real)\b', line))
    values = dict(re.findall(r'\b(n?rd\w+) = ([-0-9.e]+)(?=[,\s/]|$)', declared))
    assert len(values) == len(re.findall(r'\b(n?rd\w+) = ([-0-9.e]+)(?=[,\s/]|$)', declared))   # each stated once
    expected = dict(rdf1=morrison.VENTILATION[0], rdf2=morrison.VENTILATION[1], rdrhow=morrison.WATER_DENSITY,
                    rdexpd=morrison.DENSITY_EXPONENT, rddv0=morrison.VAPOUR_DIFFUSIVITY[0],
                    rddvx=morrison.VAPOUR_DIFFUSIVITY[1], rdmu0=morrison.VISCOSITY[0], rdmus=morrison.VISCOSITY[1],
                    rdbreak=morrison.BREAKUP_CUTOFF, rdkbreak=morrison.BREAKUP_RATE, rdcap0=morrison.MEAN_DIAMETER_CAP,
                    rdfloor0=morrison.MEAN_DIAMETER_FLOOR, rdvcap0=morrison.FALL_CAP, rdgref=morrison.GRAVITY,
                    rdpref=breakup.ATMOSPHERE_PA, rdcfloor=morrison.SELF_COLLECTION_FLOOR,
                    nrdinv=rd.INVERSE_POINTS, rdxlim=rd.EXPONENT_LIMIT, rdtiny=rd.TINY_FLUX,
                    nrdrop_join=2, rdrop_warm=0.0, rdrop_melt=0.0, rdrop_ksc=morrison.SELF_COLLECTION,
                    rdrop_rhoexp=0.0, rdrop_step=rd.STEP_M, nrdtab=0, rdx0=0.0, rddx=0.0)
    assert {name: float(values[name]) for name in expected} == expected
    assert 'rdrhosu = 85000.0/(287.04*273.15)' in added
    for lunar in ('2.919', '0.687', '0.000439', '0.439', '0.00295', '2.95', '1.62', 'nsnowsub'):
        assert lunar not in added, lunar


def test_on_a_power_law_the_rates_and_a_layers_steps_agree_with_arithmetic_by_hand():
    """Morrison's own power law at each gravity, as a table of its closed forms: the copy's loss rates at one slope,
    and its midpoint steps through one layer of unsaturated air under falling rain, against the same arithmetic
    written out from the closed forms, with no table and no inverse."""
    for c, pressure_pa, lam0 in ((LUNAR, 121590.0, 1000.0), (EARTH, 101325.0, 2500.0)):
        g = c['ga']
        a, b, table = power_law_table(g)
        law = rd.law_of(table)
        inv = rd.inverse(g, law)
        prm = dict(nrdrop_join=2, rdrop_warm=0.4e-3, rdrop_melt=1.0e-3, rdrop_ksc=3.5, rdrop_rhoexp=0.687,
                   rdrop_step=400.0)
        # One layer: sigma 0.90 to 0.95 of a column at 290 K and 60% humidity, with rain arriving and none formed.
        s = warm_column(Base(c, np.array([0.5, 0.9, 0.95, 1.0]), pressure_pa), {}, humidity=0.6)
        level, sigma, dsigma, ps = 2, 0.925, s['dsigma'][2], s['dp'][0]
        assert (s['sigma'][level], dsigma) == pytest.approx((sigma, 0.05), rel=1e-12)
        capillary = math.sqrt(9.81 / g) * (ps / 101325.0) ** 0.687
        cutoff, rate = 300.0e-6 * capillary, 2300.0 / capillary
        vcap = 9.1 * (g / 9.81) ** 0.25

        def by_hand(f, n, air):
            """The shares of water and of drops lost per metre, from the closed forms: the slope from F_N/F =
            lambda^3 6 Gamma(1.8) / (Gamma(4.8) pi rho_w), the two speeds under their cap."""
            lam = (n / f * math.pi * 997.0 * GAMMA_48 / (6.0 * GAMMA_18)) ** (1.0 / 3.0)
            dens = (85000.0 / (287.04 * 273.15) / air['rho']) ** 0.54
            vm, vn = dens * a * GAMMA_48 / 6.0 * lam ** -b, dens * a * GAMMA_18 * lam ** -b
            assert a * GAMMA_48 / 6.0 * lam ** -b < vcap                    # the test's rain falls below the cap
            vent = math.sqrt(a) * GAMMA_29 * lam ** -2.9
            w = 0.78 / lam ** 2 + 0.308 * math.sqrt(dens * air['rho'] / air['mu']) * air['sc'] ** (1.0 / 3.0) * vent
            k = 2.0 * air['rho'] * air['dv'] * lam ** 4 * w * max(air['qs'] - air['q'], 0.0) / (997.0 * vm * air['ab'])
            d = 1.0 / lam
            dum = 1.0 if d < cutoff else 2.0 - math.exp(rate * (d - cutoff))
            collect = 3.5 * dum * (f / vm) / vn if f / vm / air['rho'] >= 1.0e-8 else 0.0
            return k, k * vm / vn + collect, lam

        t, q = 290.0, s['dq'][0, level]
        p = ps * sigma
        qs0 = c['rdbrv'] * 610.78 * math.exp(17.2693882 * (t - 273.16) / (t - 35.86)) / p
        cor = 1.0 / (1.0 - (1.0 / c['rdbrv'] - 1.0) * qs0)
        qs = qs0 * cor
        tv = t * (1.0 + (1.0 / c['rdbrv'] - 1.0) * q)
        rho = p / (c['gascon'] * tv)
        lcpe = 2.5008e6 / (c['acpd'] * (1.0 + c['ADV'] * q))
        mu = 1.496e-6 * t ** 1.5 / (t + 120.0)
        dv = 8.794e-5 * t ** 1.81 / p
        air = dict(q=q, qs=qs, rho=rho, mu=mu, dv=dv, sc=mu / (rho * dv),
                   ab=1.0 + lcpe * 17.2693882 * (273.16 - 35.86) * qs * cor / (t - 35.86) ** 2,
                   db=cutoff, kb=rate)
        mass = ps / g
        arriving = 2.0e-5                                                   # kg/m2/s, 1.7 mm a day
        drops_in = arriving * lam0 ** 3 * 6.0 * GAMMA_18 / (GAMMA_48 * math.pi * 997.0)
        k, loss, lam = by_hand(arriving, drops_in, air)
        assert lam == pytest.approx(lam0, rel=1e-12)
        assert rd.rates(arriving, drops_in, air, inv, prm) == pytest.approx((k, loss), rel=1e-9)
        assert k > 0.0 and loss != k * GAMMA_48 / (6.0 * GAMMA_18)          # the drops collide as well
        # The layer's depth, its midpoint steps of at most 400 m in each half, and what they leave.
        depth = c['gascon'] * tv / g * dsigma / sigma
        steps = math.ceil(0.5 * depth / 400.0)
        ds = 0.5 * depth / steps
        f, n = arriving, drops_in
        for _ in range(2 * steps):
            k1, l1, _ = by_hand(f, n, air)
            k2, l2, _ = by_hand(f * math.exp(-0.5 * k1 * ds), n * math.exp(-0.5 * l1 * ds), air)
            f, n = f * math.exp(-k2 * ds), n * math.exp(-l2 * ds)
        assert steps == (4 if g < 2.0 else 1) and 0.0 < arriving - f < 0.5 * arriving
        zprc, zprl, zprn = np.array([0.7 * arriving / mass]), np.array([0.3 * arriving / mass]), np.array([drops_in])
        dqdt, dtdt = np.zeros(1), np.zeros(1)
        rd.rdropevap(level, np.array([q]), np.array([t]), np.array([qs]), np.array([cor]), zprc + zprl, np.zeros(1),
                     zprc, zprl, zprn, dqdt, dtdt, s, c, prm, inv)
        evaporated = (arriving - f) / mass
        assert evaporated < (qs - q) * dsigma / c['deltsec2'] / air['ab']    # below what would saturate the layer
        assert dqdt[0] == pytest.approx(evaporated / dsigma, rel=1e-9)
        assert dtdt[0] == pytest.approx(-evaporated / dsigma * lcpe, rel=1e-9)
        assert zprn[0] == pytest.approx(n, rel=1e-9)
        assert (zprc[0], zprl[0]) == pytest.approx((0.7 * f / mass, 0.3 * f / mass), rel=1e-9)   # by their shares


def test_the_three_birth_rules_count_the_new_drops_as_written():
    """Saturated air and no collisions, so that the drops at the ground are the births alone, by hand from the power
    law's F_N/F: every new drop at its size; rain formed under falling rain joining it; and the share W/(W + F) of it
    as new drops, F the rain arriving at the layer's middle. Rain melted from snow comes at its own size under each."""
    for c, pressure_pa in ((LUNAR, 121500.0), (EARTH, 101325.0)):
        a, b, table = power_law_table(c['ga'])
        law = rd.law_of(table)
        per_flux = lambda d: d ** -3 * 6.0 * GAMMA_18 / (GAMMA_48 * math.pi * 997.0)       # drops per kg at a mean size
        warm, melt = 0.4e-3, 0.8e-3                # mean sizes whose speeds lie below the cap at either gravity
        s = warm_column(Base(c, HALF15, pressure_pa), {6: 3.0e-9, 9: 2.0e-9})
        mass = s['dp'][0] / c['ga']
        upper, lower = 3.0e-9 * mass, 2.0e-9 * mass
        expected = {0: (upper + lower) * per_flux(warm), 1: upper * per_flux(warm),
                    2: (upper + lower * lower / (lower + upper)) * per_flux(warm)}
        for join, number in expected.items():
            prm = dict(nrdrop_join=join, rdrop_warm=warm, rdrop_melt=melt, rdrop_ksc=0.0, rdrop_rhoexp=0.0,
                       rdrop_step=1000.0)
            out = rd.mkrain(copy(s), c, prm, law)
            assert out['number'][0] == pytest.approx(number, rel=1e-9), join
            assert out['dprc'][0] * 1000.0 == pytest.approx(upper + lower, rel=1e-12) and out['dprs'][0] == 0.0
            # Snow formed at level 3 in freezing air melts at level 4, the first above freezing, into drops of the
            # melted size, and the rain formed lower down then follows the rule under it.
            snowy = copy(s)
            snowy['dt'][0, :4] = 260.0
            snowy['dprcl'][0, 3] = snowy['dprscl'][0, 3] = 1.0e-9
            out = rd.mkrain(snowy, c, prm, law)
            melted = 1.0e-9 * mass
            below = {0: (upper + lower) * per_flux(warm), 1: 0.0,
                     2: (upper * upper / (upper + melted) + lower * lower / (lower + upper + melted)) * per_flux(warm)}
            assert out['number'][0] == pytest.approx(melted * per_flux(melt) + below[join], rel=1e-9), join


def test_the_python_copy_keeps_the_columns_water_and_evaporates_only_unsaturated_air(moon, earth):
    for world in (moon, earth):
        c = world.c
        for seed in (5, 6):
            s = columns(world, seed=seed)
            before = copy(s)
            out = rd.mkrain(s, c, world.prm, world.law)
            mass = s['dp'] / c['ga']
            formed = (s['dprcl'] + s['dprll']).sum(axis=1)                             # sigma-weighted, per second
            ground = (out['dprc'] + out['dprl']) * 1000.0 / mass
            gone = ((out['rain_evaporation'] + out['snow_sublimation']) * s['dsigma'][None, :]).sum(axis=1)
            assert np.allclose(formed, ground + gone, rtol=1e-12, atol=1e-24)
            zq = before['dq'] + before['dqdt'] * c['deltsec2']
            zt = before['dt'][:, :-1] + before['dtdt'] * c['deltsec2']
            qs = saturation(c, zt, s['dp'][:, None] * s['sigma'][None, :])
            qs = np.minimum(qs, c['rdbrv'])
            qs = qs / (1.0 - (1.0 / c['rdbrv'] - 1.0) * qs)
            assert (out['rain_evaporation'][zq >= qs] == 0.0).all()
            assert (out['rain_evaporation'] >= 0.0).all() and (out['rain_evaporation'] > 0.0).any()
            rained = out['dprc'] + out['dprl'] - out['dprs'] > 0.0
            assert rained.any() and (out['number'][rained] > 0.0).all()


def test_in_saturated_air_the_drops_grow_toward_the_breakup_size_and_stop_there(moon, earth):
    for world, level in ((moon, 6), (earth, 4)):                              # rain born high, well above the ground
        c = world.c
        s = warm_column(world, {level: 3.0e-9 * world.rate})
        inv = rd.inverse(c['ga'], world.law)
        out = rd.mkrain(copy(s), c, world.prm, world.law)
        flux = out['dprc'][0] * 1000.0
        size = math.exp(-rd.slope_of(math.log(out['number'][0] / flux), inv))
        scol = math.sqrt(9.81 / c['ga']) * (s['dp'][0] / 101325.0) ** world.prm['rdrop_rhoexp']
        equilibrium = (morrison.BREAKUP_CUTOFF + math.log(2.0) / morrison.BREAKUP_RATE) * scol
        assert world.prm['rdrop_warm'] < size <= equilibrium * 1.001
        assert size > 0.5 * equilibrium


def test_the_share_rule_makes_the_drops_of_rain_formed_afresh_and_part_of_them_below(moon):
    """Rain formed as rain where none arrives makes all its own drops under the share rule, as under the rule that makes
    every new drop; formed lower down, where rain already falls, part of it joins that rain, so the ground gets more
    drops than when all of it joins and fewer than when none does. The air is saturated, so the births and the
    collisions alone set the drops' number."""
    s = warm_column(moon, {6: 3.0e-9})
    sizes = dict(rdrop_melt=0.439e-3, rdrop_warm=0.439e-3)

    def number(case, join):
        return rd.mkrain(copy(case), LUNAR, dict(moon.prm, nrdrop_join=join, **sizes), moon.law)['number'][0]

    assert number(s, 2) == pytest.approx(number(s, 0), rel=1e-12)
    s['dprcl'][0, 9] = 2.0e-9                                                       # more rain formed lower down
    joined, shared, new = (number(s, join) for join in (1, 2, 0))
    assert joined < shared < new


# ------------------------------------------------------------------------------------------------------ Fortran

STUB = """
      module rainmod
      integer, parameter :: NHOR={nhor}, NLEV={nlev}, NLEP={nlev}+1, NLEM={nlev}-1, NLON=1, NLAT=1, NROOT=0
      real :: dt(NHOR,NLEP), dq(NHOR,NLEP), dtdt(NHOR,NLEP), dqdt(NHOR,NLEP), dp(NHOR)
      real :: sigma(NLEV), dsigma(NLEV)
      real :: deltsec, deltsec2, ga, gascon, acpd, adv, alv, als, rdbrv, ra1, ra2, ra4, tmelt, gamma
      real :: dprll(NHOR,NLEV), dprsll(NHOR,NLEV), dprcl(NHOR,NLEV), dprscl(NHOR,NLEV)
      real :: dprc(NHOR), dprl(NHOR), dprs(NHOR)
      real :: dgp3d(NHOR,NLEV,25)
      real :: dentropy(NHOR,40), dentro(NHOR), dentrot(NHOR,NLEV), dentroq(NHOR,NLEV), dentrop(NHOR)
      real :: dentro3d(NHOR,NLEV,40), denergy(NHOR,40), dener3d(NHOR,NLEV,40)
      integer :: ndiaggp=1, nentropy=0, nentro3d=0, nenergy=0, nener3d=0, nprc=2, mypid=0
      integer :: nevapprec= 1
{declarations}      end module rainmod

      subroutine mpbci(k)
      integer k
      end subroutine mpbci
      subroutine mpbcr(p)
      real p
      end subroutine mpbcr
      subroutine mpbcrn(p,n)
      integer n
      real p(n)
      end subroutine mpbcrn
      subroutine mpabort(ym)
      character(len=*) :: ym
      write(*,'(a)') 'ABORT '//trim(ym)
      stop 2
      end subroutine mpabort
"""
HARNESS = """
      program harness
      use rainmod
      implicit none
      integer :: jhor, jlev
      real :: zt0(NHOR,NLEP), zq0(NHOR,NLEP)
      read(*,*) deltsec, deltsec2, ga, gascon, acpd, adv, alv, als, rdbrv, ra1, ra2, ra4, tmelt, gamma
      read(*,*) nevapprec{switch}
      read(*,*) sigma, dsigma
      do jhor=1,NHOR
       read(*,*) dp(jhor)
       read(*,*) (dt(jhor,jlev), jlev=1,NLEP)
       read(*,*) (dq(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dtdt(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dqdt(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dprcl(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dprscl(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dprll(jhor,jlev), jlev=1,NLEV)
       read(*,*) (dprsll(jhor,jlev), jlev=1,NLEV)
      enddo
      zt0(:,:)=dtdt(:,:)
      zq0(:,:)=dqdt(:,:)
{setup}      call mkrain
      do jhor=1,NHOR
       write(*,'(*(es25.16e3))') (dtdt(jhor,jlev)-zt0(jhor,jlev), jlev=1,NLEV)
       write(*,'(*(es25.16e3))') (dqdt(jhor,jlev)-zq0(jhor,jlev), jlev=1,NLEV)
       write(*,'(*(es25.16e3))') dprc(jhor), dprl(jhor), dprs(jhor)
      enddo
      end program harness
"""
SETTINGS = ', ' + ', '.join(rd.NAMELIST_NAMES)
SETUP = '      if(nevapprec == 2) call rdropini   ! as rainini calls it\n'
CONSTANTS = ('deltsec', 'deltsec2', 'ga', 'gascon', 'acpd', 'ADV', 'ALV', 'ALS', 'rdbrv', 'ra1', 'ra2', 'ra4', 'TMELT',
             'gamma')


def mkrain_code(text, last='mkrain'):
    """mkrain and the routines that follow it in rainmod.f90, through `last`."""
    start = text.index('      subroutine mkrain\n')
    return text[start:text.index(f'      end subroutine {last}\n') + len(f'      end subroutine {last}\n')]


def module_additions(patched: str, before: str) -> str:
    """The lines a patched rainmod.f90 adds to the module's own part, its declarations, in order."""
    part = lambda text: text[:text.index('      end module rainmod\n')].splitlines(keepends=True)
    old = part(before)
    return ''.join(line for line in part(patched) if line not in old)


class Sources:
    """mkrain before patch 14 and with it, and the harnesses compiled from them, each compiled once."""

    def __init__(self, series_sources, root):
        self.before = series_sources.source('rainmod.f90', series_sources.before(RAIN_PATCH))
        self.patched = series_sources.source('rainmod.f90', RAIN_PATCH)
        self.root, self.built = root, {}

    def harness(self, patched: bool, nhor: int, nlev: int, flags=GCM_FLAGS):
        key = (patched, nhor, nlev, flags)
        if key not in self.built:
            folder = self.root / f'build{len(self.built)}'
            folder.mkdir()
            code = mkrain_code(self.patched, 'rdropevap') if patched else mkrain_code(self.before)
            declarations = module_additions(self.patched, self.before) if patched else ''
            files = {'stub.f90': STUB.format(nhor=nhor, nlev=nlev, declarations=declarations), 'rain.f90': code,
                     'harness.f90': HARNESS.format(switch=SETTINGS if patched else '', setup=SETUP if patched else '')}
            for name, body in files.items():
                (folder / name).write_text(body)
            subprocess.run(['gfortran', *flags, '-o', 'harness', *files], cwd=folder, check=True, capture_output=True)
            self.built[key] = folder / 'harness'
        return self.built[key]


@pytest.fixture(scope='module')
def sources(series_sources, tmp_path_factory):
    return Sources(series_sources, tmp_path_factory.mktemp('rain_drops'))


def harness_input(c, s, nevapprec, prm=None) -> str:
    n = s['dq'].shape[0]
    lines = [num([c[k] for k in CONSTANTS]),
             f'{nevapprec} ' + ('' if prm is None else ' '.join(repr(prm[k]) for k in rd.NAMELIST_NAMES)),
             num(np.r_[s['sigma'], s['dsigma']])]
    for j in range(n):
        lines += [num(s['dp'][j])] + [num(s[k][j]) for k in ('dt', 'dq', 'dtdt', 'dqdt', 'dprcl', 'dprscl', 'dprll',
                                                               'dprsll')]
    return '\n'.join(lines) + '\n'


def run_harness(exe, folder, text, table: dict | str | None = None) -> subprocess.CompletedProcess:
    """The harness run in a folder of its own, which holds the fall law's table where one is given: a table as
    fall_law.table gives it, written by fall_law.table_text, or a text to write as it stands."""
    folder.mkdir()
    if table is not None:
        (folder / fall_law.TABLE_FILE).write_text(table if isinstance(table, str) else fall_law.table_text(table))
    return subprocess.run([str(exe)], input=text, capture_output=True, text=True, cwd=folder)


def fields(done: subprocess.CompletedProcess, n: int) -> dict:
    assert done.returncode == 0, done.stdout[-500:] + done.stderr[-2000:]
    rows = [np.array(r.split(), float) for r in done.stdout.strip('\n').split('\n')]
    assert len(rows) == 3 * n
    return dict(dtdt=np.array([rows[3 * j] for j in range(n)]), dqdt=np.array([rows[3 * j + 1] for j in range(n)]),
                ground=np.array([rows[3 * j + 2] for j in range(n)]))


def agrees(got: dict, s: dict, world, prm: dict, label) -> None:
    """The harness's tendencies and precipitation against the Python copy's, to 1e-10 of each field's largest value."""
    py = copy(s)
    out = rd.mkrain(py, world.c, prm, world.law)
    scale = lambda a: max(np.abs(a).max(), 1e-30)
    for key, want in (('dtdt', py['dtdt'] - s['dtdt']), ('dqdt', py['dqdt'] - s['dqdt']),
                      ('ground', np.c_[out['dprc'], out['dprl'], out['dprs']])):
        assert np.isfinite(got[key]).all() and np.isfinite(want).all(), (label, key)
        assert np.abs(got[key] - want).max() <= 1e-10 * scale(want), (label, key)
    assert out['rain_evaporation'].max() > 0.0, label


@FORTRAN
def test_the_fortran_gives_the_python_copys_rain_under_every_birth_rule(tmp_path, sources, moon, earth):
    for world, name, seeds in ((moon, 'moon', ((5, False), (6, True))), (earth, 'earth', ((5, False), (7, True)))):
        for rule, births in BIRTH_RULES.items():
            prm = dict(world.prm, **births)
            for seed, freezing in seeds:
                s = columns(world, seed=seed, ground_freezing=freezing)
                n, nlev = s['dq'].shape
                done = run_harness(sources.harness(True, n, nlev), tmp_path / f'{name}{rule}{seed}',
                                   harness_input(world.c, s, 2, prm), world.found['table'])
                agrees(fields(done, n), s, world, prm, (name, rule, seed))


@FORTRAN
def test_in_dry_air_heavy_rain_and_extreme_sizes_the_fortran_stays_finite_and_follows_the_copy(tmp_path, sources,
                                                                                              moon, earth):
    """Rain falling heavily into air 5-30% humid, born at the floor's 20 um, at 0.465 mm or at 6.5 mm: the drops
    evaporate within a step's half, break up hard or saturate their layer, and the compiled routine, with ExoPlaSim's
    traps on invalid arithmetic, division by zero and overflow, still gives the copy's numbers."""
    for world, name in ((moon, 'moon'), (earth, 'earth')):
        for size in (2e-5, ONE_SIZE_M, 6.5e-3):
            for join in (0, 1, 2):
                prm = dict(world.prm, rdrop_melt=size, rdrop_warm=size, nrdrop_join=join)
                s = columns(world, seed=12, ground_freezing=True)
                rng = np.random.default_rng(13)
                s['dq'] = s['dq'] * np.where(rng.uniform(size=s['dq'].shape) < 0.5,
                                             rng.uniform(0.05, 0.3, s['dq'].shape), 1.0)
                for key in ('dprcl', 'dprscl', 'dprll', 'dprsll'):
                    s[key] = s[key] * 40.0
                n, nlev = s['dq'].shape
                done = run_harness(sources.harness(True, n, nlev), tmp_path / f'{name}{size}_{join}',
                                   harness_input(world.c, s, 2, prm), world.found['table'])
                agrees(fields(done, n), s, world, prm, (name, size, join))


@FORTRAN
@pytest.mark.parametrize('flags', [GCM_FLAGS, NATIVE_FLAGS], ids=['exoplasim', 'native'])
def test_with_nevapprec_1_or_0_the_patched_mkrain_prints_every_digit_the_old_one_prints(tmp_path, sources, moon,
                                                                                       earth, flags):
    """PlaSim's own two settings, gamma's evaporation and none, on the mkrain before the patch and with it: the same
    digits in every tendency and at the ground, with the patch's settings at their defaults and no table in the
    folder, which the default path leaves unread."""
    assert mkrain_code(sources.before) != mkrain_code(sources.patched)
    defaults = dict(nrdrop_join=2, rdrop_warm=0.0, rdrop_melt=0.0, rdrop_ksc=5.78, rdrop_rhoexp=0.0, rdrop_step=1000.0)
    for world, name in ((moon, 'moon'), (earth, 'earth')):
        for seed in (9, 10):
            s = columns(world, seed=seed, ground_freezing=seed == 10)
            n, nlev = s['dq'].shape
            for nevapprec in (1, 0):
                old = run_harness(sources.harness(False, n, nlev, flags), tmp_path / f'old{name}{seed}{nevapprec}',
                                  harness_input(world.c, s, nevapprec))
                new = run_harness(sources.harness(True, n, nlev, flags), tmp_path / f'new{name}{seed}{nevapprec}',
                                  harness_input(world.c, s, nevapprec, defaults))
                assert old.returncode == 0 and new.returncode == 0, old.stderr[-1000:] + new.stderr[-1000:]
                assert old.stdout == new.stdout and len(old.stdout.splitlines()) == 3 * n, (name, seed, nevapprec)
            evaporating, dry = (fields(run_harness(sources.harness(True, n, nlev, flags),
                                                   tmp_path / f'read{name}{seed}{k}',
                                                   harness_input(world.c, s, k, defaults)), n) for k in (1, 0))
            assert np.abs(evaporating['dqdt']).max() > 0.0 and not np.array_equal(evaporating['dqdt'], dry['dqdt'])


@FORTRAN
def test_the_scheme_stops_on_a_setting_or_a_table_it_cannot_take(tmp_path, sources, moon):
    s = columns(moon, seed=5)
    n, nlev = s['dq'].shape
    exe, table = sources.harness(True, n, nlev), moon.found['table']
    good = fall_law.table_text(table)
    rows = good.splitlines(keepends=True)
    first, step = table['ln_lambda_first'], table['ln_lambda_step']
    # A table whose number-weighted speed falls so fast with lambda that the drops per unit of rain fall with it.
    falling = dict(table, ln_number_weighted=[-6.0 * (first + i * step) for i in range(table['points'])])
    cases = [('missing', moon.prm, None, 'which is missing'),
             ('one_row', moon.prm, f'1 {first!r} {step!r}\n' + rows[1], 'two rows or more and a positive step'),
             ('no_step', moon.prm, f'{table["points"]} {first!r} 0.0\n' + ''.join(rows[1:]), 'a positive step'),
             ('short', moon.prm, ''.join(rows[:-3]), 'a row is missing or unreadable'),
             ('long', moon.prm, good + rows[-1], 'more rows than its first line states'),
             ('header', moon.prm, 'rain\n' + ''.join(rows[1:]), 'its first line is unreadable'),
             ('falling', moon.prm, falling, 'F_N/F fails to rise with lambda'),
             ('rule', dict(moon.prm, nrdrop_join=3), table, 'nrdrop_join is 0, 1 or 2'),
             ('warm', dict(moon.prm, rdrop_warm=0.0), table, 'rdrop_warm and rdrop_melt are positive'),
             ('melt', dict(moon.prm, rdrop_melt=-1.0e-3), table, 'rdrop_warm and rdrop_melt are positive'),
             ('rate', dict(moon.prm, rdrop_ksc=-1.0), table, 'rdrop_ksc is zero or more'),
             ('step', dict(moon.prm, rdrop_step=0.0), table, 'rdrop_step is positive')]
    for name, prm, given, message in cases:
        done = run_harness(exe, tmp_path / name, harness_input(LUNAR, s, 2, prm), given)
        assert done.returncode == 2 and done.stdout.startswith('ABORT ') and message in done.stdout, (name, done.stdout)
        assert len(done.stdout.strip().removeprefix('ABORT ')) <= 59          # mpabort centres up to 59 characters
    # The same folder and settings with the table as written run through, and a rate of zero is taken.
    for name, prm in (('good', moon.prm), ('still', dict(moon.prm, rdrop_ksc=0.0))):
        fields(run_harness(exe, tmp_path / name, harness_input(LUNAR, s, 2, prm), table), n)


def test_the_patch_declares_reads_and_broadcasts_each_name_once(series_sources):
    assert all(len(line) <= 132 for line in series_sources.added(RAIN_PATCH))
    before = series_sources.source('rainmod.f90', series_sources.before(RAIN_PATCH))
    text = series_sources.source('rainmod.f90', RAIN_PATCH)
    namelist = text[text.index('      namelist/rainmod_nl/'):text.index('!     reset defaults')]
    for name in rd.NAMELIST_NAMES:
        assert len(re.findall(rf'(real|integer) :: {name} = ', text)) == 1
        assert len(re.findall(rf'call mpbc[ri]\({name}\)', text)) == 1
        assert len(re.findall(rf'\b{name}\b', namelist)) == 1
    assert text.count('      if(nevapprec == 2) call rdropini') == 1 and text.count("file='lab_rain_law.txt'") == 1
    assert fall_law.TABLE_FILE == 'lab_rain_law.txt'
    for name in ('nrdtab', 'rdx0', 'rddx'):
        assert len(re.findall(rf'call mpbc[ri]\({name}\)', text)) == 1
    assert text.count('      call mpbcrn(rdtab,3*nrdtab)') == 1
    for routine in ('subroutine rdropini', 'subroutine rdroptab(', 'real function rdropslope(',
                    'real function rdropnper(', 'subroutine rdroprates(', 'subroutine rdropevap('):
        assert text.count(f'      {routine}') == 1, routine
    # mkrain's own statements stay: the patch takes one line from it, the test of nevapprec, and widens it.
    removed = [line[1:] for line in (series_sources.folder / RAIN_PATCH).read_text().splitlines()
               if line.startswith('-') and not line.startswith('---')]
    assert removed == ['       if(nevapprec.eq.1) then']
    assert text.count('       if(nevapprec.eq.1 .or. nevapprec.eq.2) then') == 1
    assert before.count('where((zq(:).lt.zqsat(:))') == text.count('where((zq(:).lt.zqsat(:))') == 4


@FORTRAN
def test_the_patched_rainmod_compiles_with_plasims_modules(tmp_path, series_sources):
    (tmp_path / 'resmod.f90').write_text('      module resmod\n      parameter(NLAT_ATM = 32)\n'
                                         '      parameter(NLEV_ATM = 15)\n      parameter(NPRO_ATM = 1)\n'
                                         '      end module resmod\n')
    for name in ('plasimmod.f90', 'rainmod.f90'):
        (tmp_path / name).write_text(series_sources.source(name, RAIN_PATCH), encoding='latin-1')
    for name in ('resmod.f90', 'plasimmod.f90', 'rainmod.f90'):
        subprocess.run(['gfortran', *GCM_FLAGS, '-c', name], cwd=tmp_path, check=True, capture_output=True)
