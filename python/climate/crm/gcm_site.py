"""The forcing of a CM1 box from a GCM run at one site, through the whole column, and the files and namelist entries
through which CM1 reads it.

    from climate.crm import gcm_site as gs
    run = gs.run_record(model_folder, topography, solar_day_s=29.53059 * 86400.0)   # a PlaSim run, from its namelists
    forcing = gs.site_forcing(run, (10, 19), site)                       # the GCM's column at the site
    air = gs.reference_air(forcing, run['gravity_m_s2'], zw[-1])         # its mean air as CM1 holds air
    case = gs.case_inputs(forcing, zw, air, gravity_m_s2=run['gravity_m_s2'], start_hour_deg=-90.0,
                          solar_day_s=run['solar_day_s'], length_s=59.0 * 86400.0, damping_base_m=0.77 * zw[-1],
                          nudge_tau_s=259200.0)
    case['files'], case['namelist'], case['record']                      # for the case writer to place

What a box takes. A box at a site no ring passes takes the GCM's column there: the cells within half_lat_deg and
half_lon_deg of the site whose surface is the site's, sea at sea level or land, averaged with weights cos(latitude)
(site_cells). From them site_forcing gives the GCM's mean air and surface; its mean vertical wind, which CM1 applies to
its own air through its own large-scale vertical advection (core patches 10-14, var13 = 1, terluna_wls.txt); the
heating and moistening the GCM's circulation brings by local time (core patch 17, var11 = 1, terluna_lsadv.txt); its
wind by local time, toward which CM1 nudges the box's mean wind window by window (CM1's own lsnudge files) on the
wind's own time from the GCM's lowest level up (patch 09 of the lab's series); and the top of its convection, above
which alone the box holds its temperature and vapour to the GCM's (core patch 09, var14 and var15). The table and the
mean wind act through the whole column, the box's top included, and where the mean wind converges it draws in the
GCM's mean air (patch 09 of the lab's series).

The budget. The heating and moistening come from the GCM's own budget at each of its levels, the storage less the
physics. In Terluna's design climate the Moon's column holds about 220 kg/m2 of vapour, so its circulation moves water
through a column about a hundred times as fast as the column keeps it, and the net at a site, about a millimetre a
day, is a residual that differences of the GCM's winds and humidity across its cells leave unresolved: at the
Near-side Sea centred and spectral differences of the 3-day means brought the column +0.1 to +2.5 mm/day, where the
GCM's own budget takes away 0.7 (Terluna's climate/crm/README.md at 39c5ee04). PlaSim writes its physics' heating and
moistening of each layer as it applies them: the heating at each grid point (code 21, dt_diab), projected here onto
the run's harmonics as its spectral step takes it, and the moistening as that step applies it (code 40, under the
name dq_dyn that Terluna's runner gives it). These diagnostics are single steps at the end of each mean, so the
vapour over the column is held to the GCM's exact means, the precipitable water's change less the evaporation plus
the rain, the difference spread over the levels in proportion to the vapour each holds.

The vertical wind. PlaSim's postprocessor writes omega (wap) about a hundred times too weak at the equator against
the meridional mass flux of the same winds (Terluna's finding), so the wind here is the GCM's continuity on its own
spectral fields: the divergence and the surface pressure's gradient from the written winds and pressure projected
onto the harmonics, summed down each column over its layers as PlaSim sums them (omega).

Local time. Each record is a mean over the run's output interval, window_deg of hour angle (360 times the interval
over the solar day), centred on the site's hour angle from the subsolar longitude of the record's mean solar height;
the physics' snapshots fall at each record's end, half a window later. The humidity's records are read by the rule of
defect A10 (climate/gcm/year_files.py): each interval's mean the average of a record and the next, each year file's
first and last records left out. Each level's series is fitted by least squares with the day's mean and its first
`harmonics` harmonics, those of the means divided by the damping that their filter gives them: sin(x)/x for a true
mean over window_deg, x = n window_deg / 2, and for the humidity read by the rule cos(x), the damping of an average
of the window's two ends. Terluna's module divides the humidity's by sin(x)/x too, which on its design years at the
Near-side Sea left the humidity's third daily harmonic at the ground two thirds of its size and its fourth under
half, and the storage by local time up to 0.2 g/kg/day short where it swings 0.5-0.8; undone by cos(x), the fit
agrees with one of the held records as snapshots at their intervals' starts within 0.02 g/kg/day. The fit needs
records in at least 2 harmonics + 1 of the day's windows, so a run whose means span a solar day or more, or whose
Sun stands still, is refused.

The table on CM1's levels (to_cm1). CM1 applies the mean vertical wind to its own air, so the table holds the
circulation's heating and moistening with the mean wind's advection of the box's starting air added back, so that at
the start the two cancel to the accuracy of the two differences (centred here, CM1's third-order upstream). The GCM
holds its tendencies as layer values between half levels, so each layer's is laid on CM1's levels by pressure,
linear within the layer about its value, its slope the monotonized-central limit of its neighbours' (flat in the top
and bottom layers), which keeps every layer's total (remap); what lies above the box's top is left out, and the
record states its share of the column's mass, about 2% for Terluna's 150 km boxes.

The held air and the damping (convection_top, held_heights, damping_clearance_m). The top of the GCM's convection is
its lowest level above which its convection forms less than `share` of its convective rain. The box holds its air to
the GCM's from the GCM's next level up, fully from the level above that or from the box's top. A case whose Rayleigh
layer begins below that next level would damp air the GCM's convection reaches, and case_inputs refuses it: the
threshold is proposed (PLAN.md, "Porting: confidence, form and cost"; registry entry cm1-damping-below-convection).

The vapour in CM1's variable. CM1 holds vapour as a mixing ratio, kg per kg of dry air, and reads its sounding and its
nudging files in it; PlaSim writes specific humidity, kg per kg of moist air. The GCM's side here keeps specific
humidity (specific_humidity_kg_kg), and reference_air and to_cm1 convert at CM1's side: the air's vapour to
r = q / (1 - q), and the circulation's moistening, laid on CM1's levels by pressure, to (1 + r) times itself, so that
CM1's dry mass, (1 - q) of each layer's mass, gains the vapour the GCM's layer gains. Terluna's runner handed CM1 the
specific humidity as its mixing ratio, which at the ground over the Near-side Sea in its design years, at 14.1 g/kg,
left the box's air 0.2 g/kg drier and its moistening 1.4% weaker.

The wind's own nudging and the inflow. CM1 relaxes the box's mean wind and its held air toward the windows on one
time, lsnudge_tau, and on the held air's three days Terluna's sea box kept its mean wind at 44-67% of its target's
speed through most of the lunar day, its targets changing every 0.82 days. Patch 09 of the lab's CM1 series reads
three entries of &param3, which case_inputs sets as a case states them: wind_nudge_tau, the wind's own time, by
default Terluna's 2 hours (WIND_NUDGE_TAU_S), a tenth of the Moon's window of local time; wind_nudge_zmin, the height
from which CM1 pulls the wind, by default the GCM's lowest level to 0.1 m, below which the windows repeat that level's
wind down to the ground and the box's own surface layer and turbulence shape it; and inflow_ref_air, on by default
(INFLOW), with which the mean wind's convergence draws in the windows' air, the GCM's mean air, at the rate
max(d(rho0 w)/dz, 0)/rho0, where CM1's own advection draws in the box's (Daleu, Woolnough and Plant 2012). Where a
world's window of local time is shorter, the wind follows it less closely on 2 hours, and the record states the time's
share of the window. Every window here holds the GCM's mean air, so the inflow draws toward one reference through the
run.

What a world and a run supply. Nothing of a world is built in. The run's record (run_record) holds its gravity,
radius, gas constant and heat capacity as the GCM ran with them, its half levels, its truncation, its output interval
and its surface heights, and the world's solar day; CM1's constants (CM1_RD, CM1_CP, CM1_RV, constants.F) set the
potential temperature, Exner function and virtual temperature in which the box's air is written. The site, the
harmonics, the bins of local time and the convection's share are settings, Terluna's values by default.
TERLUNA_OPEN_MOON_SITES records the sites Terluna's boxes took, as values a study of the Open Moon states.

Evidence. A runnable calculation with its tests (climate/tests/test_gcm_site.py). On Terluna's design run read in
place, with Terluna's constants and choices stated as values, the extraction gives the forcing that Terluna's box over
the Near-side Sea records, bit for bit at the GCM's levels and to the printed digits in its files; on the run's own
constants it departs from it by the causes that test states, each within its tolerance. Terluna's measured effects
of the forcing, the boxes' rain against the GCM's among them, are Terluna's runs: with the hold from 8 km the sea box
rained 0.06 mm/day against the GCM's 2.72, the nudging putting back 83.5 W/m2 above 16 km in place of the deep
convection; forced through the whole column it rained 31% of the GCM's rain over its second lunar day and 49% over its
third (notes/cm1.md, "The nudging and the convection"). Relaxed on 2 hours, the sea box's mean wind at 0.3 km rose
from 1.44 to 2.49 m/s within three hours against a target of 3.24, and with the GCM's air drawn in, its column dried
0.30 mm/day over a lunar day where it had dried 0.67 (Terluna's climate/crm/README.md at 39c5ee04). No lab run has
taken this forcing; a forced CM1 box waits for the lab's case writer (PLAN.md, block 2).

Brought from Terluna's climate/crm/gcm_site.py at 39c5ee04 (python/provenance.json), with the pieces of its
climate/crm/cm1_run.py that the forcing needs. Spectral, omega, remap, convection_top, the fits and wind_windows keep
Terluna's arithmetic; run_record, the run's constants and window, the humidity's own filter, the vapour in CM1's mixing
ratio, the refusals and case_inputs are the lab's. The entries of patch 09 take the values of Terluna's
corrected_wind and corrected_inflow (cm1_run.py at 39c5ee04) under the lab's names.

Left for later changes: the reckoning of the inflow against the nudging window CM1 holds at each output, which a box
budget needs once the windows carry the GCM's weather (Terluna's box_budget, 4f63c439), with the lab's box budget; the
GCM's own weather at a site (Terluna's site_sequence and its readers, af42e928); and the damped gravity wave's inputs
(Terluna's dgw_forcing and first_mode, c3898a7c, CM1 port 5).
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np

# CM1's constants (constants.F of cm1r22.0, its defaults): the potential temperature, Exner function and virtual
# temperature in which the box's sounding, nudging and table are written.
CM1_RD, CM1_CP, CM1_RV = 287.04, 1005.7, 461.5
CM1_KAPPA = CM1_RD / CM1_CP
P00 = 1.0e5
# PlaSim's constants (plasimmod.f90, p_exo.f90 and landmod.f90 of ExoPlaSim 3.4.2): the vapour's gas constant, the
# latent heat of its rain, the default Poisson constant, from which with a run's GASCON its heat capacity follows, and
# the soil bucket's capacity (m) and the share of it from which the ground evaporates freely.
PLASIM_RV, PLASIM_ALV, PLASIM_AKAP = 461.51, 2.5008e6, 0.286
PLASIM_SOIL = dict(wsmax=0.5, drhsfull=0.4)
WATER_DENSITY = 1000.0                     # PlaSim's, in its water fluxes (m/s of water)
SEA_LEVEL_M = 1.0                          # a sea cell stands below this height; a raised lake above it
HARMONICS = 4                              # the fits by local time: the day's mean and its first four harmonics
BINS = 36                                  # the table and the wind's windows: bins of local time from -180 degrees
CONVECTION_SHARE = 0.01                    # the levels above the GCM's convection top form less than this of its rain
CM1_NUDGE_FILES = 100                      # lsnudge_nmax (lsnudge.F): the most nudging files CM1 reads
WIND_NUDGE_TAU_S = 7200.0                  # the wind's own nudging time: Terluna's 2 hours, the time on which
                                           # cloud-resolving runs forced by observations relax their mean wind
                                           # (Khairoutdinov, Randall and DeMott 2005; cm1_run.py WIND_TAU_S at 39c5ee04)
INFLOW = True                              # the windows' air drawn in where the mean wind converges, as Terluna's
                                           # site boxes take it from 28 October 2026 (corrected_inflow at 39c5ee04)
INFLOW_RATES_FILE = 'lab_inflow_rate.txt'  # where patch 09 of the lab's CM1 series writes the inflow's rates
MEANS = ('ta', 'hus', 'ua', 'va', 'ps', 'ts', 'tas', 'czen', 'pr', 'evap', 'prw', 'mrso', 'lsm')
SNAPSHOTS = ('dt_diab', 'dq_dyn')          # codes 21 and 40: the physics' heating, and its moistening as applied
SCHEMES = ('dt_conv', 'dt_lsp')            # codes 28 and 27: the convective and large-scale heating, where rain forms
SURFACES = ('sea', 'land')
WLS_FILE, LSADV_FILE = 'terluna_wls.txt', 'terluna_lsadv.txt'      # the names core patches 10 and 17 read

# The sites of Terluna's boxes forced by the GCM's column, as values a study of the Open Moon states (climate/crm/
# cm1_run.py at 39c5ee04: SITE_BOX and the design-years and turned cases). Each takes the cells within 5.6 degrees of
# latitude and 8.5 of longitude: on the design years six sea cells at the Near-side Sea, four land cells at 0 E and
# six in the south-east. Terluna
# forced the first three from its design runs, A28R_301k_cold_moist over its years 0-5 and A28R_301k_design_l15_snow_
# s934 over its years 10-19, and the turned three from A28R_301k_design_l15_snow_s924_turned_refit over its years
# 10-49, the sites carried with the ground when the Moon turned.
TERLUNA_OPEN_MOON_SITES = {
    'near_side_sea': dict(lat_deg=-5.0, lon_deg=-45.0, half_lat_deg=5.6, half_lon_deg=8.5, surface='sea'),
    '0e': dict(lat_deg=0.0, lon_deg=0.0, half_lat_deg=5.6, half_lon_deg=8.5, surface='land'),
    'se_dry': dict(lat_deg=-44.3, lon_deg=56.25, half_lat_deg=5.6, half_lon_deg=8.5, surface='land'),
    'near_side_sea_turned': dict(lat_deg=-9.24, lon_deg=-52.01, half_lat_deg=5.6, half_lon_deg=8.5, surface='sea'),
    '0e_turned': dict(lat_deg=-7.85, lon_deg=-6.28, half_lat_deg=5.6, half_lon_deg=8.5, surface='land'),
    'se_dry_turned': dict(lat_deg=-49.85, lon_deg=56.39, half_lat_deg=5.6, half_lon_deg=8.5, surface='land'),
}


# The run.

def _namelist(path: Path) -> dict:
    """The entries of a Fortran namelist file as text, by upper-case name."""
    text = path.read_text() if path.exists() else ''
    return {m.group(1).upper(): m.group(2).strip().rstrip(',').strip()
            for m in re.finditer(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$', text, flags=re.M)}


def read_sra(path) -> np.ndarray:
    """A PlaSim surface file's field (lat, lon), from the north and from 0 E: its header of eight integers names the
    longitudes and latitudes (fifth and sixth), and the values follow."""
    numbers = Path(path).read_text().split()
    nlon, nlat = int(numbers[4]), int(numbers[5])
    values = np.array(numbers[8:8 + nlat * nlon], float)
    if values.size != nlat * nlon:
        raise ValueError(f'{path} holds {values.size} values, where its header names {nlat} x {nlon}')
    return values.reshape(nlat, nlon)


def run_record(model_folder, topography, *, solar_day_s: float, half_levels=None, name: str | None = None) -> dict:
    """A PlaSim run's record as site_forcing reads it, from the namelists in its model folder: its gravity (GA), radius
    (PLARAD), gas constant (GASCON) and heat capacity (GASCON / AKAP, PlaSim's 0.286 where AKAP is unstated), with
    PlaSim's own gas constant of vapour and latent heat of condensation (RV and ALV of plasimmod.f90), its half
    levels (SIGH under NEQSIG -1; half_levels, where the caller gives them from the lab's derive.levels, take their
    place, and a run on PlaSim's own levels, NEQSIG 0, needs them), its output interval (NSTPW steps of MPSTEP
    minutes), its soil (WSMAX and DRHSFULL of landmod_namelist, PlaSim's defaults where unstated) and the surface's
    heights, m, from the surface geopotential's file `topography` (code 129) over the run's gravity. The solar day, s,
    is the world's: the period of the Sun's hour angle at a site, which PlaSim's model day may round."""
    folder = Path(model_folder)
    planet, plasim = _namelist(folder / 'planet_namelist'), _namelist(folder / 'plasim_namelist')
    land = _namelist(folder / 'landmod_namelist')
    missing = [k for k in ('GA', 'PLARAD', 'GASCON') if k not in planet] + \
              [k for k in ('NSTPW', 'MPSTEP') if k not in plasim]
    if missing:
        raise ValueError(f'{folder} states no {", ".join(missing)} in its planet and plasim namelists')
    gravity, gas = float(planet['GA']), float(planet['GASCON'])
    if half_levels is None:
        if plasim.get('NEQSIG', '0').strip() != '-1' or 'SIGH' not in plasim:
            raise ValueError(f"{folder} keeps PlaSim's own levels (NEQSIG 0); state the run's half levels")
        half_levels = [float(x) for x in plasim['SIGH'].replace(',', ' ').split()]
    record_s = float(plasim['NSTPW']) * float(plasim['MPSTEP']) * 60.0
    return dict(name=name or folder.parent.name, folder=str(folder), gravity_m_s2=gravity,
                radius_m=float(planet['PLARAD']), gas_constant_j_kg_k=gas, vapour_gas_constant_j_kg_k=PLASIM_RV,
                heat_capacity_j_kg_k=gas / float(planet.get('AKAP', PLASIM_AKAP)), latent_heat_j_kg=PLASIM_ALV,
                half_levels=[float(x) for x in half_levels], record_s=record_s, solar_day_s=float(solar_day_s),
                window_deg=360.0 * record_s / float(solar_day_s),
                soil=dict(wsmax=float(land.get('WSMAX', PLASIM_SOIL['wsmax'])),
                          drhsfull=float(land.get('DRHSFULL', PLASIM_SOIL['drhsfull']))),
                surface_height_m=(read_sra(topography) / gravity).tolist(), topography=str(topography))


# Spherical harmonics and the GCM's continuity.

class Spectral:
    """Triangular spherical harmonics on a Gaussian grid (rows north to south): analysis of grid fields, and synthesis
    of a field, its derivative in mu = sin(latitude) or in longitude."""

    def __init__(self, nlat: int, nlon: int, truncation: int):
        from scipy.special import assoc_legendre_p_all
        if truncation < 1 or nlat < truncation + 1 or nlon <= 2 * truncation:
            raise ValueError(f'a grid of {nlat} x {nlon} resolves no triangular truncation T{truncation}')
        nodes, weights = np.polynomial.legendre.leggauss(nlat)
        order = np.argsort(-nodes)
        self.mu, self.w = nodes[order], weights[order]
        p = np.asarray(assoc_legendre_p_all(truncation, truncation, self.mu, norm=True, diff_n=1))
        self.p, self.dp = p[0, :, :truncation + 1, :], p[1, :, :truncation + 1, :]       # (n, m, lat)
        self.t, self.nlon = truncation, nlon
        self.m = np.arange(truncation + 1)
        self.cos = np.sqrt(1.0 - self.mu**2)

    def analyse(self, f):
        """Coefficients (..., n, m) of a grid field (..., lat, lon)."""
        fourier = np.fft.rfft(np.asarray(f, float), axis=-1)[..., :self.t + 1] / self.nlon
        return np.einsum('...jm,nmj,j->...nm', fourier, self.p, self.w)

    def synthesise(self, s, along=None):
        """The field (..., lat, lon), or its derivative along 'mu' or 'lambda' (radians), from coefficients."""
        f = np.einsum('...nm,nmj->...jm', s, self.dp if along == 'mu' else self.p)
        if along == 'lambda':
            f = f * 1j * self.m
        full = np.zeros(f.shape[:-1] + (self.nlon // 2 + 1,), complex)
        full[..., :self.t + 1] = f * self.nlon
        return np.fft.irfft(full, n=self.nlon, axis=-1)

    def project(self, f):
        return self.synthesise(self.analyse(f))


def edges(half_levels) -> np.ndarray:
    """PlaSim's layer interfaces in sigma, the top's 0 first, then the half levels to the ground's 1."""
    half = np.asarray(half_levels, float)
    if half.ndim != 1 or half.size < 2 or half[-1] != 1.0 or np.any(np.diff(np.r_[0.0, half]) <= 0.0):
        raise ValueError(f"half levels rise from above 0 to the ground's 1, where these are {half.tolist()}")
    return np.r_[0.0, half]


def full_levels(half_levels) -> np.ndarray:
    """The full levels PlaSim puts midway in sigma between the interfaces around them."""
    e = edges(half_levels)
    return 0.5 * (e[1:] + e[:-1])


def omega(u, v, ps, half_levels, radius, sp: Spectral, wind: Spectral):
    """PlaSim's continuity on its spectral fields: omega (Pa/s) at the full levels (time, lev, lat, lon) from the
    winds and surface pressure (Pa), omega = sigma ps v.grad(ln ps) less ps times the sum from the top of
    (div v + v.grad(ln ps)) over the layers above and the part of its own layer above the level, each layer's value
    its full level's, as PlaSim's vertical sums take them; the divergence from (u cos, v cos) on harmonics one degree
    higher (wind), as a flow of the run's truncation carries them, and the gradient of ln ps from its projection
    (sp)."""
    e = edges(half_levels)
    sigma = 0.5 * (e[1:] + e[:-1])
    cos = wind.cos[:, None]
    div = (wind.synthesise(wind.analyse(u * cos), 'lambda') / (radius * cos**2)
           + wind.synthesise(wind.analyse(v * cos), 'mu') / radius)
    lnps = sp.analyse(np.log(ps))
    gx = sp.synthesise(lnps, 'lambda') / (radius * cos)
    gy = sp.synthesise(lnps, 'mu') * cos / radius
    vgrad = u * gx[:, None] + v * gy[:, None]
    thick = np.diff(e)[None, :, None, None]
    total = div + vgrad
    above = np.cumsum(total * thick, axis=1) - total * thick + total * (sigma - e[:-1])[None, :, None, None]
    return ps[:, None] * (sigma[None, :, None, None] * vgrad - above)


# The site's cells and the Sun.

def check_site(site: dict) -> dict:
    """A site as site_forcing takes it: its centre, the half widths of its cells' box and its surface."""
    keys = ('lat_deg', 'lon_deg', 'half_lat_deg', 'half_lon_deg', 'surface')
    if set(site) != set(keys):
        raise ValueError(f'a site states {", ".join(keys)}, where it states {sorted(site)}')
    if site['surface'] not in SURFACES:
        raise ValueError(f"a site's surface is sea or land, where it is {site['surface']!r}")
    if not (-90.0 <= site['lat_deg'] <= 90.0 and site['half_lat_deg'] > 0.0 and 0.0 < site['half_lon_deg'] <= 180.0):
        raise ValueError(f'a site stands within the globe and its box has a positive size, where it is {site}')
    return dict(site)


def site_cells(lat, lon, lsm, height, site):
    """The GCM cells of the site: within half_lat_deg and half_lon_deg of it, sea at sea level or land."""
    rows = np.abs(lat - site['lat_deg']) <= site['half_lat_deg']
    cols = np.abs((lon - site['lon_deg'] + 180.0) % 360.0 - 180.0) <= site['half_lon_deg']
    cells = rows[:, None] & cols[None, :]
    if site['surface'] == 'sea':
        cells &= ~lsm & (height < SEA_LEVEL_M)
    elif site['surface'] == 'land':
        cells &= lsm
    else:
        raise ValueError(f"surface is sea or land, where it is {site['surface']!r}")
    if not cells.any():
        raise ValueError(f'no {site["surface"]} cells at the site {site}')
    return cells


def subsolar_longitude(czen, lat, lon):
    """The longitude (degrees) each record's mean solar height centres on, near the equator: the circular mean of
    longitude weighted by the mean cosine of the solar zenith over the rows within 20 degrees of the equator, which a
    mean over a window of the day keeps symmetric about the window's centre."""
    rows = np.abs(lat) < 20.0
    weight = czen[:, rows, :].mean(axis=1)                                  # (time, lon)
    a = np.radians(lon)
    return np.degrees(np.arctan2((weight * np.sin(a)).sum(axis=1), (weight * np.cos(a)).sum(axis=1))) % 360.0


def level_heights(ta, hus, half_levels, gravity, gas_constant, vapour_gas_constant=PLASIM_RV):
    """Heights (m) of the full levels above the ground (..., lev), top first, from the virtual temperatures in the
    GCM's own gas constants: the lowest level ln(1/sigma) of its virtual temperature's scale height up, each level above
    the trapezoid of the two levels' virtual temperatures over the step in ln sigma."""
    sigma = full_levels(half_levels)
    tv = ta * (1.0 + (vapour_gas_constant / gas_constant - 1.0) * hus)
    z = np.zeros_like(tv)
    z[..., -1] = gas_constant * tv[..., -1] / gravity * np.log(1.0 / sigma[-1])
    for k in range(sigma.size - 2, -1, -1):
        z[..., k] = z[..., k + 1] + gas_constant * 0.5 * (tv[..., k] + tv[..., k + 1]) / gravity * np.log(
            sigma[k + 1] / sigma[k])
    return z


# The fits by local time.

def basis(hour_deg, harmonics=HARMONICS):
    a = np.radians(np.asarray(hour_deg, float))
    return np.column_stack([np.ones_like(a)] + [f(n * a) for n in range(1, harmonics + 1) for f in (np.cos, np.sin)])


def harmonic_coefficients(hour_deg, values, harmonics=HARMONICS):
    """Least-squares coefficients of a series values (time, ...) against the hour angle: the mean, then the cosine and
    sine of each harmonic."""
    b = basis(hour_deg, harmonics)
    values = np.asarray(values, float)
    coef, *_ = np.linalg.lstsq(b, values.reshape(len(b), -1), rcond=None)
    return coef.reshape((b.shape[1],) + values.shape[1:])


def undamped(coef, window_deg, harmonics=HARMONICS, kind='mean'):
    """The coefficients with each harmonic divided by the damping that the records' filter over window_deg of hour
    angle gives it: a true mean over the window ('mean') damps the n-th harmonic by sin(x)/x, and the average of the
    values at the window's two ends ('ends'), the rule by which the year files' humidity is read (defect log A10), by
    cos(x), x = n window_deg / 2 in radians."""
    if kind not in ('mean', 'ends'):
        raise ValueError(f"a record's filter is a true mean or the average of its two ends, where it is {kind!r}")
    out = np.array(coef, float)
    for n in range(1, harmonics + 1):
        x = math.radians(n * window_deg / 2.0)
        out[2 * n - 1:2 * n + 1] /= math.sin(x) / x if kind == 'mean' else math.cos(x)
    return out


def evaluate(coef, hour_deg, harmonics=HARMONICS):
    return np.tensordot(basis(hour_deg, harmonics), coef, axes=(1, 0))


def rate(coef, hour_deg, day_s, harmonics=HARMONICS):
    """The time derivative (per second) of a fitted series at the hour angles, which grow 360 degrees a solar day."""
    a = np.radians(np.asarray(hour_deg, float))
    d = np.column_stack([np.zeros_like(a)] + [g for n in range(1, harmonics + 1)
                                              for g in (-n * np.sin(n * a), n * np.cos(n * a))])
    return np.tensordot(d, coef, axes=(1, 0)) * 2.0 * math.pi / day_s


def bin_hours(bins=BINS) -> np.ndarray:
    """The centres of the bins of local time (degrees), from -180 degrees, as core patch 17 reads its table."""
    return (np.arange(bins) + 0.5) * 360.0 / bins - 180.0


# The column's layers on CM1's levels.

def remap(values, edges_pa, targets_pa):
    """A field the GCM holds as layer values (..., layer) between the pressures edges_pa (top first, increasing) as
    means over the target layers between targets_pa (in either order): linear in pressure within each source layer
    about its value, its slope the monotonized-central limit of the neighbouring layers' (flat in the top and bottom
    layers), integrated over the part of each target layer the source layer covers. Each source layer's integral in
    pressure is kept wherever the targets cover it."""
    v = np.asarray(values, float)
    e = np.asarray(edges_pa, float)
    mid = 0.5 * (e[1:] + e[:-1])
    slope = np.zeros_like(v)
    if mid.size > 2:
        up = (v[..., 1:-1] - v[..., :-2]) / (mid[1:-1] - mid[:-2])
        down = (v[..., 2:] - v[..., 1:-1]) / (mid[2:] - mid[1:-1])
        centre = (v[..., 2:] - v[..., :-2]) / (mid[2:] - mid[:-2])
        limit = 2.0 * np.minimum(np.abs(up), np.abs(down))
        slope[..., 1:-1] = np.where(up * down > 0.0, np.sign(centre) * np.minimum(np.abs(centre), limit), 0.0)
    t = np.asarray(targets_pa, float)
    lo, hi = np.minimum(t[1:], t[:-1]), np.maximum(t[1:], t[:-1])
    out = np.zeros(v.shape[:-1] + lo.shape)
    for k in range(mid.size):
        a, b = np.clip(lo, e[k], e[k + 1]), np.clip(hi, e[k], e[k + 1])
        out += v[..., k, None] * (b - a) + slope[..., k, None] * 0.5 * ((b - mid[k])**2 - (a - mid[k])**2)
    return out / (hi - lo)


def virtual_theta(theta, qv):
    """CM1's virtual potential temperature (base.F): theta (1 + qv Rv/Rd) / (1 + qv), qv the mixing ratio."""
    qv = np.asarray(qv, float)
    return np.asarray(theta, float) * (1.0 + qv * CM1_RV / CM1_RD) / (1.0 + qv)


def column_pressures(zw, theta_at, qv_at, surface_pa, gravity, steps=20):
    """Pressure (Pa) at the heights zw (the ground up) in hydrostatic balance with air of potential temperature
    theta_at(z) and vapour mixing ratio qv_at(z), from the surface pressure, as CM1 integrates its sounding: the Exner
    function falls by g / (cp theta_v) per metre, by the trapezoid rule on `steps` sub-layers of each layer."""
    zw = np.asarray(zw, float)
    z = np.concatenate([np.linspace(a, b, steps, endpoint=False) for a, b in zip(zw[:-1], zw[1:])] + [zw[-1:]])
    inv = 1.0 / virtual_theta(theta_at(z), qv_at(z))
    exner = (surface_pa / P00)**CM1_KAPPA - gravity / CM1_CP * np.r_[0.0, np.cumsum(0.5 * (inv[1:] + inv[:-1])
                                                                                     * np.diff(z))]
    return P00 * exner[::steps]**(1.0 / CM1_KAPPA)


def mixing_ratio(specific_humidity):
    """CM1's vapour, kg per kg of dry air, from the GCM's, kg per kg of moist air: q / (1 - q)."""
    q = np.asarray(specific_humidity, float)
    return q / (1.0 - q)


# The GCM's convection and the box's held air.

def convection_top(formed, z, share=CONVECTION_SHARE):
    """The top of the GCM's convection from the rain it forms in each layer (top first) at heights z (m): the lowest
    level above which less than share of it forms; and the heights from which a box holds its air to the GCM's, the
    next level up and, fully, the one above that (None past the GCM's top)."""
    formed = np.maximum(np.asarray(formed, float), 0.0)
    if formed.sum() <= 0.0:
        raise ValueError('the GCM forms no convective rain here')
    above = np.r_[0.0, np.cumsum(formed)[:-1]] / formed.sum()            # formed above each level
    k = int(np.flatnonzero(above < share).max())
    level = lambda i: float(z[i]) if i >= 0 else None
    return dict(level=k, top_m=float(z[k]), share=share, held_from_m=level(k - 1), held_fully_from_m=level(k - 2))


def held_heights(convection: dict, ztop_m: float) -> dict:
    """The heights (m) between which core patch 09 weights the box's held air from 0 to 1: the GCM's first level above
    its convection's top (var14), and the next above it or the box's top (var15)."""
    if convection['held_from_m'] is None:
        raise ValueError("the GCM's convection reaches its top level; there is no air above it to hold")
    start = convection['held_from_m']
    full = convection['held_fully_from_m'] if convection['held_fully_from_m'] is not None else ztop_m
    if not start < ztop_m:
        raise ValueError(f"the box's top at {ztop_m:.0f} m stands below the GCM's first level above its convection, "
                         f'{start:.0f} m, from which the box holds its air')
    return dict(var14=float(start), var15=float(min(full, ztop_m)))


def damping_clearance_m(convection: dict, damping_base_m: float) -> float:
    """How far (m) the case's Rayleigh layer begins above the GCM's first level over its convection's top (the
    convection's top plus one layer): -inf where the convection reaches the GCM's top level."""
    if convection['held_from_m'] is None:
        return -math.inf
    return float(damping_base_m) - float(convection['held_from_m'])


def check_damping(convection: dict, damping_base_m: float) -> float:
    """The proposed refusal (PLAN.md; registry cm1-damping-below-convection): a case whose Rayleigh layer begins below
    the GCM's convection's top plus one layer is refused. Returns the clearance (m) of a case that passes."""
    clearance = damping_clearance_m(convection, damping_base_m)
    if clearance < 0.0:
        where = ('reaches its top level' if convection['held_from_m'] is None else
                 f"tops at {convection['top_m']:.0f} m, its next level at {convection['held_from_m']:.0f} m")
        raise ValueError(f"refused (proposed rule, registry cm1-damping-below-convection): the case's Rayleigh layer "
                         f"begins at {damping_base_m:.0f} m, where the GCM's convection {where}")
    return clearance


# The GCM's column at the site.

def _truncation(d) -> int | None:
    """The triangular truncation of a year file's spectral modes, (T + 1)(T + 2) / 2 of them; None without them."""
    if 'modes' not in d.dimensions:
        return None
    count = len(d.dimensions['modes'])
    t = int(round((math.sqrt(8 * count + 1) - 3) / 2))
    if (t + 1) * (t + 2) // 2 != count:
        raise ValueError(f'{count} spectral modes make no triangular truncation')
    return t


def site_forcing(run: dict, years, site: dict, *, harmonics: int = HARMONICS, bins: int = BINS,
                 share: float = CONVECTION_SHARE, truncation: int | None = None,
                 humidity_filter: str | None = None) -> dict:
    """The GCM's column at a site over the years (first, last), from a run's record (run_record): its mean air and
    surface, its mean vertical wind, the circulation's heating and moistening by local time with the budget behind
    them, its wind by local time and the top of its convection. Arrays by level run top first, as PlaSim writes them;
    the vapour is the GCM's specific humidity. The run's year files need the means MEANS, the snapshots SNAPSHOTS and
    the schemes' heating SCHEMES, which a run writes with PlaSim's gridpoint diagnostics (NDIAGGP 1) and its codes 27,
    28 and 40 named (Terluna's --heating-diagnostics and --moisture-diagnostics). The humidity's fit by local time
    undoes the filter its records carry, the average of each interval's two ends where the run's files are read by the
    rule of A10, a true mean where they hold hus_mean; humidity_filter 'mean' undoes a true mean's whatever the files
    hold, as Terluna's module does, kept for comparison with Terluna's products."""
    import netCDF4
    from climate.gcm import year_files as yf
    site = check_site(site)
    first, last = (int(y) for y in years)
    if last < first:
        raise ValueError(f'years run from the first to the last, where they are {years}')
    if harmonics < 1 or bins < 2 * harmonics + 1:
        raise ValueError(f'{bins} bins of local time carry no fit of {harmonics} harmonics')
    gravity, radius = run['gravity_m_s2'], run['radius_m']
    gas, cp = run['gas_constant_j_kg_k'], run['heat_capacity_j_kg_k']
    rv, lv = run['vapour_gas_constant_j_kg_k'], run['latent_heat_j_kg']
    half = np.asarray(run['half_levels'], float)
    e = edges(half)
    sigma, thick = 0.5 * (e[1:] + e[:-1]), np.diff(e)
    window_deg, day_s = float(run['window_deg']), float(run['solar_day_s'])
    if not 0.0 < window_deg < 360.0 / (2 * harmonics + 1):
        raise ValueError(f'means over {window_deg:.1f} degrees of hour angle leave too few windows of the day for '
                         f'{harmonics} harmonics: the fit takes means shorter than a {2 * harmonics + 1}th of the day')
    folder, soil = Path(run['folder']), run.get('soil', PLASIM_SOIL)
    if humidity_filter not in (None, 'mean', 'ends'):
        raise ValueError(f"the humidity's filter is the files' own, 'mean' or 'ends', where it is {humidity_filter!r}")
    filters = set()
    keep = {k: [] for k in ('hour', 'theta', 'q', 'u', 'v', 'z', 'rho', 'omega', 'heat', 'moist', 'ps', 'ts', 'tas',
                            'rain', 'evaporation', 'water', 'wetness', 'conv', 'lsp')}
    for year in range(first, last + 1):
        path = folder / f'MOST.{year:05d}.nc'
        with netCDF4.Dataset(path) as d:
            missing = [k for k in MEANS + SNAPSHOTS + SCHEMES if k not in d.variables]
            if missing:
                raise ValueError(f"{path} lacks {missing}: the run writes PlaSim's gridpoint diagnostics with codes "
                                 "27, 28 and 40 named, as Terluna's --heating-diagnostics --moisture-diagnostics do")
            f = yf.fields(d, MEANS + SNAPSHOTS + SCHEMES)            # the humidity's means: gcm/year_files.py
            filters.add('mean' if yf.HUS_MEAN in d.variables else 'ends')
            lat, lon = np.asarray(d['lat'][:], float), np.asarray(d['lon'][:], float)
            lev = np.asarray(d['lev'][:], float)
            found = _truncation(d)
        if year == first:
            if lev.shape != sigma.shape or np.abs(lev - sigma).max() > 1e-6:
                raise ValueError(f"{path}'s levels {lev.tolist()} lie off the full levels of the run's half levels "
                                 f'{sigma.tolist()}')
            t = truncation if truncation is not None else found
            if t is None or (found is not None and t != found):
                raise ValueError(f'the run is truncated at T{found}, where T{truncation} is stated')
            height = np.asarray(run['surface_height_m'], float)
            if height.shape != (lat.size, lon.size):
                raise ValueError(f"the surface's heights span {height.shape}, the run's grid {(lat.size, lon.size)}")
            lsm = f['lsm'][0] > 0.5
            cells = site_cells(lat, lon, lsm, height, site)
            jj, ii = np.nonzero(cells)
            weight = np.cos(np.radians(lat[jj]))
            weight = weight / weight.sum()
            sp, wind = Spectral(lat.size, lon.size, t), Spectral(lat.size, lon.size, t + 1)
            grid = (lat, lon)
        elif not (np.array_equal(lat, grid[0]) and np.array_equal(lon, grid[1])):
            raise ValueError(f"{path}'s grid differs from year {first}'s")
        at = lambda a: a[..., jj, ii]                                        # (..., cells)
        mean = lambda a: np.tensordot(a, weight, axes=(-1, 0))               # the cells' mean
        grid_ps = f['ps'] * 100.0                                            # hPa in the output
        ps = at(grid_ps)                                                     # (time, cells)
        ta, hus = at(f['ta']), at(f['hus'])                                  # (time, lev, cells)
        exner = (sigma[None, :, None] * ps[:, None, :] / P00)**CM1_KAPPA     # CM1's, for its theta
        rho = sigma[None, :, None] * ps[:, None, :] / (gas * ta * (1.0 + (rv / gas - 1.0) * hus))
        water = WATER_DENSITY * gravity / (ps[:, None, :] * thick[None, :, None])     # water flux to kg/kg/s
        keep['theta'].append(mean(ta / exner))
        keep['q'].append(mean(hus))
        keep['u'].append(mean(at(f['ua'])))
        keep['v'].append(mean(at(f['va'])))
        keep['rho'].append(mean(rho))
        keep['z'].append(mean(np.moveaxis(level_heights(np.moveaxis(ta, 1, -1), np.moveaxis(hus, 1, -1), half,
                                                        gravity, gas, rv), -1, 1)))
        keep['omega'].append(mean(at(omega(f['ua'], f['va'], grid_ps, half, radius, sp, wind))))
        keep['heat'].append(mean(at(sp.project(f['dt_diab'])) / exner))     # the physics' heating, as theta
        keep['moist'].append(mean(at(f['dq_dyn']) * water))                 # the physics' moistening as applied
        formed = cp * ps[:, None, :] * thick[None, :, None] / (gravity * lv)   # K/s of latent heat to kg/m2/s
        keep['conv'].append(mean(at(f['dt_conv']) * formed))
        keep['lsp'].append(mean(at(f['dt_lsp']) * formed))
        keep['ps'].append(mean(ps))
        keep['ts'].append(mean(at(f['ts'])))
        keep['tas'].append(mean(at(f['tas'])))
        keep['rain'].append(mean(at(f['pr'])) * WATER_DENSITY)               # kg/m2/s
        keep['evaporation'].append(-mean(at(f['evap'])) * WATER_DENSITY)    # upward positive
        keep['water'].append(mean(at(f['prw'])))                             # kg/m2
        keep['wetness'].append(mean(at(np.minimum(1.0, f['mrso'] / (soil['drhsfull'] * soil['wsmax'])))))
        keep['hour'].append((site['lon_deg'] - subsolar_longitude(f['czen'], lat, lon) + 180.0) % 360.0 - 180.0)
    s = {k: np.concatenate(v) for k, v in keep.items()}
    tm = lambda k: s[k].mean(axis=0)
    centre = s['hour']
    end = (centre + window_deg / 2.0 + 180.0) % 360.0 - 180.0
    windows = int(round(360.0 / window_deg))
    phases = int(np.unique(np.round(((centre + 180.0) % 360.0) / window_deg - 0.5).astype(int) % windows).size)
    if phases < 2 * harmonics + 1:
        raise ValueError(f"the records fall in {phases} of the day's {windows} windows, where a fit of {harmonics} "
                         f'harmonics takes {2 * harmonics + 1}: a Sun that stands still, or too few records')
    if len(filters) > 1:
        raise ValueError(f"years {first}-{last} mix files that hold the humidity's true mean with files read by the "
                         'rule')
    humidity = humidity_filter or filters.pop()
    fit_mean = lambda k, kind='mean': undamped(harmonic_coefficients(centre, s[k], harmonics), window_deg, harmonics,
                                               kind)
    fit_snap = lambda k: harmonic_coefficients(end, s[k], harmonics)
    theta_c, water_c, rain_c, evap_c = (fit_mean(k) for k in ('theta', 'water', 'rain', 'evaporation'))
    q_c = fit_mean('q', humidity)
    u_c, v_c = fit_mean('u'), fit_mean('v')
    heat_c, moist_c = fit_snap('heat'), fit_snap('moist')
    z, rho = tm('z'), tm('rho')
    w = -tm('omega') / (rho * gravity)
    mass = tm('ps') * thick / gravity                                        # kg/m2 in each layer
    hours = bin_hours(bins)
    on = lambda c: evaluate(c, hours, harmonics)
    heating = rate(theta_c, hours, day_s, harmonics) - on(heat_c)           # the circulation's, by local time
    moistening = rate(q_c, hours, day_s, harmonics) - on(moist_c)
    # The column's vapour held to the exact means: the precipitable water's change less the evaporation, plus the rain.
    exact = rate(water_c, hours, day_s, harmonics) - on(evap_c) + on(rain_c)                      # kg/m2/s
    snapped = moistening @ mass
    q_h = on(q_c)
    shares = q_h * mass[None, :] / (q_h @ mass)[:, None]                     # each level's share of the vapour
    moistening = moistening + (exact - snapped)[:, None] * shares / mass[None, :]
    per_day = 86400.0
    lists = lambda a: np.asarray(a, float).tolist()
    return dict(
        run=run.get('name'), years=[first, last], site=site, window_deg=window_deg, harmonics=harmonics, bins=bins,
        humidity_filter=humidity,
        truncation=t, records=int(centre.size), phases=phases,
        sigma=lists(sigma), half_levels=lists(half),
        gcm=dict(gravity_m_s2=gravity, radius_m=radius, gas_constant_j_kg_k=gas, vapour_gas_constant_j_kg_k=rv,
                 heat_capacity_j_kg_k=cp, latent_heat_j_kg=lv, solar_day_s=day_s, record_s=run.get('record_s')),
        cells=[[float(lat[j]), float(lon[i])] for j, i in zip(jj, ii)],
        cell_heights_m=[float(height[j, i]) for j, i in zip(jj, ii)],
        profile=dict(z_m=lists(z), theta_k=lists(tm('theta')), specific_humidity_kg_kg=lists(tm('q')),
                     u_m_s=lists(tm('u')), v_m_s=lists(tm('v')), density_kg_m3=lists(rho)),
        surface=dict(pressure_pa=float(tm('ps')), ground_k=float(tm('ts')), air_2m_k=float(tm('tas')),
                     wetness=float(tm('wetness')), height_m=float(np.mean([height[j, i] for j, i in zip(jj, ii)]))),
        vertical_wind_m_s=lists(w),
        circulation=dict(hour_angle_deg=lists(hours), z_m=lists(z), theta_k_s=lists(heating),
                         specific_humidity_kg_kg_s=lists(moistening)),
        wind_by_hour=dict(hour_angle_deg=lists(hours), z_m=lists(z), u_m_s=lists(on(u_c)), v_m_s=lists(on(v_c))),
        convection=dict(convective_rain_formed_mm_day=lists(tm('conv') * per_day),
                        large_scale_rain_formed_mm_day=lists(tm('lsp') * per_day),
                        **convection_top(tm('conv'), z, share)),
        budget=dict(
            circulation_heating_theta_k_day=lists(heating.mean(axis=0) * per_day),
            circulation_moistening_g_kg_day=lists(moistening.mean(axis=0) * per_day * 1e3),
            physics_heating_theta_k_day=lists(heat_c[0] * per_day),            # the fits' means over the day
            physics_moistening_g_kg_day=lists(moist_c[0] * per_day * 1e3),
            column_vapour_mm_day=dict(exact=float(exact.mean() * per_day),
                                      from_snapshots=float(snapped.mean() * per_day),
                                      exact_by_hour=lists(exact * per_day),
                                      from_snapshots_by_hour=lists(snapped * per_day),
                                      held_by_hour=lists((moistening @ mass) * per_day)),
            column_heating_w_m2=dict(physics=float(cp * (heat_c[0] * mass * (tm('ps') * sigma / P00)**CM1_KAPPA).sum()),
                                     rain_latent=float(lv * tm('rain'))),
            rain_mm_day=float(tm('rain') * per_day), evaporation_mm_day=float(tm('evaporation') * per_day)))


# The box's air and its forcing on CM1's levels.

def held_share_above(zg, theta_at, qv_below, surface_pa, gravity, ztop):
    """Vapour (mixing ratio, kg/kg) at any height: the GCM's own up to its top level zg[-1], and above it whatever keeps
    that level's share of saturation (over ice below freezing) as the temperature falls. The pressure comes from the
    potential temperature profile hydrostatically, at the world's gravity over the case's heights, as CM1 takes it from
    the sounding."""
    from atmosphere.radiative_convective.thermodynamics import saturation_pressure
    eps = CM1_RD / CM1_RV
    z = np.linspace(0.0, max(ztop, zg[-1]) * 1.01, 4001)
    r = qv_below(z)
    inv = 1.0 / virtual_theta(theta_at(z), r)
    exner = (surface_pa / P00) ** CM1_KAPPA - gravity / CM1_CP * np.concatenate(
        [[0.0], np.cumsum(0.5 * (inv[1:] + inv[:-1]) * np.diff(z))])
    p, t = P00 * exner ** (1.0 / CM1_KAPPA), theta_at(z) * exner
    e = r * p / (eps + r)
    share = float(np.interp(zg[-1], z, e / saturation_pressure(t)))
    e_held = share * saturation_pressure(t)
    log_held = np.log(eps * e_held / (p - e_held))
    return lambda zz: np.where(np.asarray(zz) <= zg[-1], qv_below(zz), np.exp(np.interp(zz, z, log_held)))


def reference_air(forcing: dict, gravity_m_s2: float, ztop_m: float) -> dict:
    """The GCM's mean air at the site as CM1 holds air, functions of height above the ground (m): potential temperature
    (theta_at, K) linear between the GCM's levels and along the top two levels' slope above them; vapour as a mixing
    ratio (qv_at, kg/kg), linear in its logarithm between the levels and above the top level at that level's share of
    saturation (held_share_above); and the mean wind (u_at, v_at, m/s). Below the lowest level each holds that level's
    value, as Terluna's set-up held them. This is the air the box starts from and holds to above the GCM's
    convection."""
    prof = forcing['profile']
    zg = np.asarray(prof['z_m'], float)[::-1]                               # the ground up
    th = np.asarray(prof['theta_k'], float)[::-1]
    r = mixing_ratio(prof['specific_humidity_kg_kg'])[::-1]
    uu, vv = (np.asarray(prof[k], float)[::-1] for k in ('u_m_s', 'v_m_s'))
    top_slope = (th[-1] - th[-2]) / (zg[-1] - zg[-2])
    theta_at = lambda z: np.where(np.asarray(z) <= zg[-1], np.interp(z, zg, th),
                                  th[-1] + top_slope * (np.asarray(z) - zg[-1]))
    r_below = lambda z: np.exp(np.interp(z, zg, np.log(np.maximum(r, 1e-9))))
    ps = forcing['surface']['pressure_pa']
    qv_at = held_share_above(zg, theta_at, r_below, ps, gravity_m_s2, ztop_m)
    return dict(theta_at=theta_at, qv_at=qv_at, u_at=lambda z: np.interp(z, zg, uu),
                v_at=lambda z: np.interp(z, zg, vv), surface_pa=ps, gravity_m_s2=float(gravity_m_s2),
                ztop_m=float(ztop_m))


def _w_levels(zw) -> np.ndarray:
    zw = np.asarray(zw, float)
    if zw.ndim != 1 or zw.size < 3 or zw[0] != 0.0 or np.any(np.diff(zw) <= 0.0):
        raise ValueError("a box's w levels rise from the ground's 0 to its top")
    return zw


def to_cm1(forcing: dict, zw, air: dict, gravity_m_s2: float) -> dict:
    """The forcing as CM1's box reads it, on its w levels zw (m, the ground's 0 to the top): the mean vertical wind
    (zero at the ground and at the box's top, linear between the GCM's levels); and the table of the circulation's
    heating (potential temperature, K/s) and moistening (mixing ratio, kg/kg/s) by local time on CM1's scalar levels,
    each GCM layer laid on them by pressure (remap), the levels' pressures those of the starting air `air`
    (reference_air) in balance from the GCM's surface pressure, the moistening carried into CM1's mixing ratio, and the
    mean wind's advection of the starting air added back, so that at the start CM1's own advection by the mean wind
    takes it away again. The circulation as laid on CM1's levels, before the conversion and the addition, is returned
    beside the table."""
    zw = _w_levels(zw)
    z = np.asarray(forcing['profile']['z_m'], float)[::-1]                # the ground up
    w = np.asarray(forcing['vertical_wind_m_s'], float)[::-1]
    inside = z < zw[-1]
    w_zw = np.interp(zw, np.r_[0.0, z[inside], zw[-1]], np.r_[0.0, w[inside], 0.0])
    zh = 0.5 * (zw[1:] + zw[:-1])
    w_zh = 0.5 * (w_zw[1:] + w_zw[:-1])
    ps = forcing['surface']['pressure_pa']
    e = edges(forcing['half_levels']) * ps                                  # the GCM's interfaces, top first
    p_w = column_pressures(zw, air['theta_at'], air['qv_at'], ps, gravity_m_s2)
    circ = forcing['circulation']
    on_box = lambda a: remap(a, e, p_w)                                    # (bins, CM1's levels from the ground)
    heat, moist = on_box(circ['theta_k_s']), on_box(circ['specific_humidity_kg_kg_s'])
    th0, r0 = np.asarray(air['theta_at'](zh), float), np.asarray(air['qv_at'](zh), float)
    theta_table = heat + (w_zh * np.gradient(th0, zh))[None, :]
    qv_table = moist * (1.0 + r0)[None, :] + (w_zh * np.gradient(r0, zh))[None, :]
    return dict(w_m_s=w_zw, pressure_pa=p_w, mass_above_top_share=float(p_w[-1] / ps),
                table=dict(z_m=zh, hour_angle_deg=np.asarray(circ['hour_angle_deg'], float), theta_k_s=theta_table,
                           qv_kg_kg_s=qv_table),
                circulation=dict(theta_k_s=heat, specific_humidity_kg_kg_s=moist))


def wind_windows(forcing: dict, heights, start_hour_deg: float, day_s: float, length_s: float) -> list:
    """The GCM's wind by local time as a series of windows for CM1's nudging: each window a bin of the day, from the
    box's start (local hour angle start_hour_deg) through its length, with the wind (m/s) at the heights at the bin's
    middle hour angle, held at the GCM's lowest level down to the ground and at its top level above."""
    wind = forcing['wind_by_hour']
    z = np.asarray(wind['z_m'], float)[::-1]
    hours = np.asarray(wind['hour_angle_deg'], float)
    u, v = (np.asarray(wind[k], float)[:, ::-1] for k in ('u_m_s', 'v_m_s'))
    step = day_s / hours.size
    count = int(math.ceil(length_s / step - 1e-9))
    out = []
    for i in range(count):
        t = i * step
        middle = (start_hour_deg + 360.0 * (t + 0.5 * step) / day_s + 180.0) % 360.0 - 180.0
        b = int(np.argmin(np.abs((hours - middle + 180.0) % 360.0 - 180.0)))
        out.append(dict(time_s=(t, t + step), hour_angle_deg=float(middle),
                        u_m_s=np.interp(heights, z, u[b]), v_m_s=np.interp(heights, z, v[b])))
    return out


# The case's files and entries.

def wls_text(zw, w_m_s) -> str:
    """terluna_wls.txt (core patch 10): the level count, then height (m) and vertical wind (m/s) from the ground up."""
    return f'{len(zw)}\n' + ''.join(f'{a:.3f} {b:.6e}\n' for a, b in zip(zw, w_m_s))


def lsadv_text(table: dict) -> str:
    """terluna_lsadv.txt (core patch 17): the bin and level counts, the level heights (m), then for each bin of local
    time, evenly spaced from -180 degrees, a line of theta tendencies (K/s) and a line of vapour tendencies
    (kg/kg/s)."""
    z, th, qv = (np.asarray(table[k], float) for k in ('z_m', 'theta_k_s', 'qv_kg_kg_s'))
    return (f'{th.shape[0]} {z.size}\n' + ' '.join(f'{v:.3f}' for v in z) + '\n'
            + ''.join(' '.join(f'{v:.6e}' for v in a) + '\n' + ' '.join(f'{v:.6e}' for v in b) + '\n'
                      for a, b in zip(th, qv)))


def nudging_text(t1: float, t2: float, heights, theta, qv, u, v) -> str:
    """One lsnudge_NNNN.dat as CM1 reads it (lsnudge.F): a header, the window's times (s), two lines of comment, then
    height (m), potential temperature (K), vapour mixing ratio (g/kg) and the two wind components (m/s)."""
    rows = [' *  Header:   lsnudge_time1 (s)   lsnudge_time2 (s)', f'  {t1:22.1f} {t2:22.6e}',
            ' *  Profile.   Note: values will be ignored if nudging for that variable is off.',
            ' *    z (m)   theta (K)    qv (g/kg)  u (m/s, grnd-reltv) v (m/s, grnd-reltv)']
    rows += [f'  {z:12.4f} {th:12.4f} {q * 1000.0:12.6f} {uu:10.4f} {vv:10.4f}'
             for z, th, q, uu, vv in zip(heights, theta, qv, u, v)]
    return '\n'.join(rows) + '\n'


def case_inputs(forcing: dict, zw, air: dict, *, gravity_m_s2: float, start_hour_deg: float, solar_day_s: float,
                length_s: float, damping_base_m: float, nudge_tau_s: float, wind_nudge_tau_s: float = WIND_NUDGE_TAU_S,
                wind_from_m: float | None = None, inflow: bool = INFLOW) -> dict:
    """What a CM1 case takes from the forcing: its files (terluna_wls.txt, terluna_lsadv.txt and the nudging windows
    lsnudge_0001.dat on, as text), its namelist entries by section and the record its case keeps. The box starts at the
    local hour angle start_hour_deg and runs length_s seconds of a solar day of solar_day_s, and its Rayleigh layer
    begins at damping_base_m. The case is refused where that layer begins below the GCM's convection's top plus one
    layer (proposed), where the box's top stands below the held air's first level, and where its windows outnumber the
    hundred files CM1 reads. Every window holds the GCM's mean air; its wind is the GCM's at the window's middle hour.
    &param8 sets the table (var11), the mean vertical wind (var13), the held air's heights (var14, var15) and the
    hour angle and solar day that core patch 17 reads the table by (var18, var19), which the case's Sun shares;
    &param19 nudges the wind, temperature and vapour toward the windows on nudge_tau_s, from the first step and with
    no ramp, since CM1 restarts a ramp at each window's start. &param3 holds the three entries of patch 09 of the
    lab's CM1 series: the wind's own nudging time (wind_nudge_tau, wind_nudge_tau_s, 2 hours by default), the height
    from which CM1 pulls the wind (wind_nudge_zmin, wind_from_m, by default the GCM's lowest level to 0.1 m, and 0 for
    every level) and the inflow of the windows' air where the mean wind converges (inflow_ref_air, inflow, on by
    default). The case is refused on a wind's time of zero or less and on a height outside the box."""
    zw = _w_levels(zw)
    if not (length_s > 0.0 and solar_day_s > 0.0 and nudge_tau_s > 0.0):
        raise ValueError('a case runs a positive length under a positive solar day and nudging time')
    if not wind_nudge_tau_s > 0.0:
        raise ValueError("the wind's own nudging time is positive; nudge_tau_s states the held air's")
    lowest_m = float(np.asarray(forcing['profile']['z_m'], float)[-1])     # the GCM's lowest level (top first)
    pulled_from_m = round(lowest_m, 1) if wind_from_m is None else float(wind_from_m)
    if not 0.0 <= pulled_from_m < zw[-1]:
        raise ValueError(f"the wind's pull starts at a height from the ground up to below the box's top, here "
                         f"{pulled_from_m} m")
    convection = forcing['convection']
    clearance = check_damping(convection, damping_base_m)
    held = held_heights(convection, zw[-1])
    cm1 = to_cm1(forcing, zw, air, gravity_m_s2)
    zh = 0.5 * (zw[1:] + zw[:-1])
    heights = np.r_[0.0, zh, zw[-1]]
    windows = wind_windows(forcing, heights, start_hour_deg, solar_day_s, length_s)
    if len(windows) > CM1_NUDGE_FILES:
        raise ValueError(f'{len(windows)} nudging windows; CM1 reads at most {CM1_NUDGE_FILES}')
    theta, qv = air['theta_at'](heights), air['qv_at'](heights)
    files = {WLS_FILE: wls_text(zw, cm1['w_m_s']), LSADV_FILE: lsadv_text(cm1['table'])}
    for i, window in enumerate(windows, 1):
        t1, t2 = window['time_s']
        files[f'lsnudge_{i:04d}.dat'] = nudging_text(t1, 1.0e30 if i == len(windows) else t2, heights, theta, qv,
                                                      window['u_m_s'], window['v_m_s'])
    namelist = dict(
        param3=dict(wind_nudge_tau=float(wind_nudge_tau_s), wind_nudge_zmin=pulled_from_m,
                    inflow_ref_air=1 if inflow else 0),
        param8=dict(var11=1.0, var13=1.0, var14=held['var14'], var15=held['var15'], var18=float(start_hour_deg),
                    var19=round(float(solar_day_s), 1)),
        param19=dict(do_lsnudge=True, do_lsnudge_u=True, do_lsnudge_v=True, do_lsnudge_th=True, do_lsnudge_qv=True,
                     lsnudge_tau=float(nudge_tau_s), lsnudge_start=1.0, lsnudge_end=1.0e12, lsnudge_ramp_time=0.0))
    low = cm1['table']['z_m'] < 3000.0
    spread = lambda a, scale: dict(mean=float(a[:, low].mean() * scale),
                                   min=float(a[:, low].mean(axis=1).min() * scale),
                                   max=float(a[:, low].mean(axis=1).max() * scale))
    speeds = [float(np.hypot(w['u_m_s'][1], w['v_m_s'][1])) for w in windows]
    window_s = windows[0]['time_s'][1] - windows[0]['time_s'][0]
    record = dict(
        {k: forcing[k] for k in ('run', 'years', 'site', 'cells', 'cell_heights_m', 'records', 'phases', 'harmonics',
                                 'bins', 'window_deg', 'humidity_filter', 'truncation', 'gcm', 'surface', 'budget',
                                 'convection')},
        held=dict(held, damping_base_m=float(damping_base_m), damping_clearance_m=clearance,
                  rule='the damping begins at or above the GCM\'s first level over its convection\'s top (proposed)'),
        mass_above_top_share=cm1['mass_above_top_share'],
        table=dict(lowest_3_km=dict(theta_k_day=spread(cm1['table']['theta_k_s'], 86400.0),
                                    qv_g_kg_day=spread(cm1['table']['qv_kg_kg_s'], 8.64e7))),
        wind=dict(windows=len(windows), window_s=window_s, start_hour_deg=float(start_hour_deg),
                  lowest_level_speed_m_s=dict(min=min(speeds), max=max(speeds)),
                  nudge_tau_s=float(wind_nudge_tau_s), nudge_tau_share_of_window=float(wind_nudge_tau_s / window_s),
                  pulled_from_m=pulled_from_m,
                  pulled_from="the GCM's lowest level" if wind_from_m is None else 'stated'),
        inflow=dict(on=bool(inflow), reference="the windows' air, the GCM's mean air at the site",
                    rate="max(d(rho0 w)/dz, 0)/rho0, the mean vertical wind's convergence over CM1's base-state "
                         "density",
                    rates_file=INFLOW_RATES_FILE),
        vapour="CM1's mixing ratio, from the GCM's specific humidity: r = q / (1 - q), the moistening times (1 + r)")
    return dict(files=files, namelist=namelist, record=record, cm1=cm1, windows=windows)
