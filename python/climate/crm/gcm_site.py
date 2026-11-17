"""The forcing of a CM1 box from a GCM run at one site, through the whole column, and the files and namelist entries
through which CM1 reads it.

    from climate.crm import gcm_site as gs
    run = gs.run_record(model_folder, topography, solar_day_s=29.53059 * 86400.0)   # a PlaSim run, from its namelists
    forcing = gs.site_forcing(run, (10, 19), site)                       # the GCM's column at the site
    air = gs.reference_air(forcing, run['gravity_m_s2'], zw[-1])         # its mean air as CM1 holds air
    case = gs.case_inputs(forcing, zw, air, gravity_m_s2=run['gravity_m_s2'], start_hour_deg=-90.0,
                          solar_day_s=run['solar_day_s'], length_s=59.0 * 86400.0, damping_base_m=0.77 * zw[-1],
                          nudge_tau_s=259200.0)
    case['files'], case['namelist'], case['start'], case['record']       # for the case writer to place
    mode = gs.first_mode(run, (10, 19))                                  # a box that makes its own vertical wind
    case = gs.case_inputs(forcing, zw, air, ..., coupling='dgw', mode=mode)

What a box takes. A box at a site no ring passes takes the GCM's column there: the cells within half_lat_deg and
half_lon_deg of the site whose surface is the site's, sea at sea level or land, averaged with weights cos(latitude)
(site_cells). From them site_forcing gives the GCM's mean air and surface; its mean vertical wind, which CM1 applies to
its own air through its own large-scale vertical advection (core patches 10-14, var13 = 1, terluna_wls.txt); the
heating and moistening the GCM's circulation brings by local time (core patch 17, var11 = 1, terluna_lsadv.txt); its
wind by local time, toward which CM1 nudges the box's mean wind window by window (CM1's own lsnudge files) on the
wind's own time from the GCM's lowest level up (patch 09 of the lab's series); and the top of its convection, above
which alone the box holds its temperature and vapour to the GCM's (core patch 09, var14 and var15). The table and the
mean wind act through the whole column, the box's top included, and where the mean wind converges it draws in the
GCM's mean air (patch 09 of the lab's series). A box may instead make its own large-scale vertical wind by the damped
gravity wave (patch 10 of the lab's series; "The box's own large-scale vertical wind", below).

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
share of the window. Under the imposed wind every window holds the GCM's mean air by default, so the inflow draws
toward one reference through the run.

The box's own large-scale vertical wind. A box forced by the GCM's mean vertical wind takes much of its free
troposphere's temperature from motion the GCM supplied. With coupling 'dgw' case_inputs writes patch 10's entries of
&param3, under which CM1 solves the damped gravity wave (Kuang 2008; Blossey, Bretherton and Wyant 2009) each step for
the box's own wind from its virtual-temperature departure from the windows' air, between the base of the coupled layer,
the domain-mean boundary layer's depth no lower than the GCM's lowest level, and a lid at the GCM's convection top at
the site. For the first baroclinic mode k2/eps = 1/(L c), so the wave takes one time, lsw_tau = L/c: c the mode's speed
over the run's tropics, the WKB integral of the buoyancy frequency to the top of their convection over pi (first_mode,
40.5-40.8 m/s on Terluna's design years), and L the length the box stands for, by default its site's footprint
(footprint_m, 418 km at the Near-side Sea), so about 2.85 h there; a case states another length, such as the planet's
radius (1,737 km on the Moon, 11.9 h), or the time. terluna_wls.txt then holds nil, and the table holds the
circulation's horizontal part alone, its tendencies less the advection by the GCM's own vertical wind by local time
(the fits of omega from continuity, as of the air), heating by default below the coupled layer's base alone, as
Terluna's boxes took it: above the base the wave's motion stands for the large-scale heating, horizontal gradients of
temperature being weak there. The windows hold the GCM's air by local time (reference_column), the vapour by the hour
where the lowest level swings by more than a tenth of its mean through the day (Terluna's rule, which gives the land
and dry sites theirs by the hour and the sea its mean), and the box starts from its first window's air, so that the
wave starts from rest. A case states its own reference, such as another box's domain mean by local time for the
self-consistency test of Edman and Romps (2015), its start and each of the wave's settings, and the record holds each
with its source. The table is laid on the pressures of the box's own starting air, its base state.

What a world and a run supply. Nothing of a world is built in. The run's record (run_record) holds its gravity,
radius, gas constant and heat capacity as the GCM ran with them, its half levels, its truncation, its output interval
and its surface heights, and the world's solar day; CM1's constants (CM1_RD, CM1_CP, CM1_RV, constants.F) set the
potential temperature, Exner function and virtual temperature in which the box's air is written. The site, the
harmonics, the bins of local time and the convection's share are settings, Terluna's values by default.
TERLUNA_OPEN_MOON_SITES records the sites Terluna's boxes took, as values a study of the Open Moon states.

Evidence. A runnable calculation with its tests (climate/tests/test_gcm_site.py; the wave's Fortran in
climate/tests/test_cm1_coupling.py). On Terluna's design run read in
place, with Terluna's constants and choices stated as values, the extraction gives the forcing that Terluna's box over
the Near-side Sea records, bit for bit at the GCM's levels and to the printed digits in its files; on the run's own
constants it departs from it by the causes that test states, each within its tolerance. Terluna's measured effects
of the forcing, the boxes' rain against the GCM's among them, are Terluna's runs: with the hold from 8 km the sea box
rained 0.06 mm/day against the GCM's 2.72, the nudging putting back 83.5 W/m2 above 16 km in place of the deep
convection; forced through the whole column it rained 31% of the GCM's rain over its second lunar day and 49% over its
third (notes/cm1.md, "The nudging and the convection"). Relaxed on 2 hours, the sea box's mean wind at 0.3 km rose
from 1.44 to 2.49 m/s within three hours against a target of 3.24, and with the GCM's air drawn in, its column dried
0.30 mm/day over a lunar day where it had dried 0.67 (Terluna's climate/crm/README.md at 39c5ee04). No lab run has
taken this forcing; a forced CM1 box waits for the lab's case writer (PLAN.md, block 2). With Terluna's choices the
wave's inputs give those of Terluna's damped-gravity-wave boxes: first_mode's 40.53382926508821 m/s and the three
footprints to the last bit, the entries Terluna's slots held, its windows and sounding to their printed digits and its
column of the GCM's vertical advection; laid on the GCM's mean air as Terluna laid it, the table is Terluna's to 1 part
in 10^4. Terluna's measured effects of the wave are Terluna's runs: its sea box rained 2.85 mm/day against the GCM's
1.42, 69% of it in the afternoon, and its dry box dried to 2% of the GCM's rain under steady descent (Terluna's
session-tools/agents/gap_boxes/yardstick/reading_wtg.md).

Brought from Terluna's climate/crm/gcm_site.py at 39c5ee04 (python/provenance.json), with the pieces of its
climate/crm/cm1_run.py that the forcing needs. Spectral, omega, remap, convection_top, the fits and wind_windows keep
Terluna's arithmetic; run_record, the run's constants and window, the humidity's own filter, the vapour in CM1's mixing
ratio, the refusals and case_inputs are the lab's. The entries of patch 09 take the values of Terluna's
corrected_wind and corrected_inflow (cm1_run.py at 39c5ee04) under the lab's names. The wave's inputs come from
Terluna's dgw_forcing, first_mode, footprint_m, dgw_settings and dgw_inputs (gcm_site.py and cm1_run.py at 29af5c16,
c3898a7c): first_mode and footprint_m keep Terluna's arithmetic, with the run's own constants; dgw_forcing's air,
vertical wind and horizontal part by local time are site_forcing's own outputs; the reference by local time, its
vapour rule and the choice of start are reference_column and case_inputs, which also take a case's own column series;
and the table is laid on the box's starting air, where Terluna's took the GCM's mean air.

Left for later changes: the reckoning of the inflow against the nudging window CM1 holds at each output, which a box
budget needs once the windows carry the GCM's weather (Terluna's box_budget, 4f63c439), with the lab's box budget and
its reading of the wave's record (lab_lsw_means.txt); the GCM's own weather at a site (Terluna's site_sequence and its
readers, af42e928); and the weak temperature gradient, which joins the wave as coupling 'wtg' with a later patch.
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
COUPLING = 'imposed'                       # a box's large-scale vertical wind: the GCM's mean, imposed through CM1's
                                           # own wprof; 'dgw' makes it the box's own by the damped gravity wave
                                           # (lsw_coupling = 1, patch 10 of the lab's CM1 series)
COUPLINGS = ('imposed', 'dgw')
REFERENCES = ('gcm-mean', 'gcm-by-hour')   # the air of a box's windows, beside a column series a case supplies
VAPOURS = ('auto', 'by-hour', 'mean')      # the GCM's vapour in a reference by local time
VAPOUR_SWING = 0.10                        # 'auto' takes the vapour by local time where the GCM's lowest level swings
                                           # by more than this share of its mean through the day, and its mean
                                           # otherwise: Terluna's rule F3 for its damped-gravity-wave boxes
STARTS = ('mean', 'reference')             # a box starts from the GCM's mean air or from its first window's
TABLE_HEATS = ('every-level', 'below-base')   # where the table heats a coupled box (lsw_table_heat 0 or 1)
MODE_LAT_LIMIT_DEG = 30.0                  # first_mode's tropics, Terluna's
LSW_RECORD_FILE = 'lab_lsw_means.txt'      # where patch 10 writes the coupled wind's means by interval
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
    # By local time, for a box that makes its own large-scale vertical wind: the GCM's air, its vertical wind from its
    # continuity, and the circulation's horizontal part, the circulation less the advection by that wind.
    th_h = on(theta_c)
    w_h = -on(undamped(harmonic_coefficients(centre, s['omega'], harmonics), window_deg, harmonics)) / (
        rho[None, :] * gravity)
    dz = lambda a: np.gradient(a, z, axis=-1)
    horizontal_th, horizontal_q = heating + w_h * dz(th_h), moistening + w_h * dz(q_h)
    lowest = evaluate(q_c, np.arange(360) + 0.5 - 180.0, harmonics)[:, -1]
    per_day = 86400.0
    lists = lambda a: np.asarray(a, float).tolist()
    by_hour = lambda a: [round(float(x), 4) for x in a]
    columns = {k: (a @ mass) * per_day for k, a in (('circulation', moistening), ('horizontal', horizontal_q),
                                                     ('vertical_advection', moistening - horizontal_q))}
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
        air_by_hour=dict(hour_angle_deg=lists(hours), z_m=lists(z), theta_k=lists(th_h),
                         specific_humidity_kg_kg=lists(q_h),
                         lowest_level_vapour_swing=float((lowest.max() - lowest.min()) / q_c[0][-1])),
        vertical_wind_by_hour=dict(hour_angle_deg=lists(hours), z_m=lists(z), w_m_s=lists(w_h)),
        horizontal=dict(hour_angle_deg=lists(hours), z_m=lists(z), theta_k_s=lists(horizontal_th),
                        specific_humidity_kg_kg_s=lists(horizontal_q),
                        column_vapour_mm_day={k: dict(mean=float(v.mean()), by_hour=by_hour(v))
                                              for k, v in columns.items()}),
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


# The coupled box's length and speed.

def first_mode(run: dict, years, *, lat_limit_deg: float = MODE_LAT_LIMIT_DEG, share: float = CONVECTION_SHARE) -> dict:
    """The first baroclinic gravity wave's speed over a run's tropics (m/s): the WKB estimate c = (1/pi) * integral of
    N dz on the mean over the years (first, last) of the GCM's mean potential temperature over the cells within
    lat_limit_deg of the equator, weighted by cos(latitude), from the ground to the top of their convection
    (convection_top's rule on the convective rain they form by level), and to the model's top level beside it. The
    potential temperature, the heights and the formed rain take the run's own gas constant, heat capacity and
    latent heat; the humidity is read by the rule of A10 (climate/gcm/year_files.py)."""
    import netCDF4
    from climate.gcm import year_files as yf
    first, last = (int(y) for y in years)
    if last < first:
        raise ValueError(f'years run from the first to the last, where they are {years}')
    if not 0.0 < lat_limit_deg <= 90.0:
        raise ValueError(f'the tropics reach a latitude between 0 and 90 degrees, where it is {lat_limit_deg}')
    gravity, gas, cp = run['gravity_m_s2'], run['gas_constant_j_kg_k'], run['heat_capacity_j_kg_k']
    rv, lv = run['vapour_gas_constant_j_kg_k'], run['latent_heat_j_kg']
    half = np.asarray(run['half_levels'], float)
    e = edges(half)
    sigma, thick = 0.5 * (e[1:] + e[:-1]), np.diff(e)
    folder = Path(run['folder'])
    sums, count = {}, 0
    for year in range(first, last + 1):
        path = folder / f'MOST.{year:05d}.nc'
        with netCDF4.Dataset(path) as d:
            f = yf.fields(d, ('ta', 'hus', 'ps', 'dt_conv'))
            lat = np.asarray(d['lat'][:], float)
            lev = np.asarray(d['lev'][:], float)
        if lev.shape != sigma.shape or np.abs(lev - sigma).max() > 1e-6:
            raise ValueError(f"{path}'s levels {lev.tolist()} lie off the full levels of the run's half levels")
        ps = f['ps'] * 100.0
        w = np.where(np.abs(lat) <= lat_limit_deg, np.cos(np.radians(lat)), 0.0)[:, None] * np.ones(ps.shape[-1])
        w /= w.sum()
        tm = lambda a: np.tensordot(a, w, axes=([-2, -1], [0, 1])).sum(axis=0)          # summed over records
        for key, value in (('theta', f['ta'] / (sigma[None, :, None, None] * ps[:, None] / P00) ** (gas / cp)),
                           ('ta', f['ta']), ('q', f['hus']),
                           ('conv', f['dt_conv'] * cp * ps[:, None] * thick[None, :, None, None] / (gravity * lv))):
            sums[key] = sums.get(key, 0.0) + tm(value)
        count += ps.shape[0]
    mean = {k: v / count for k, v in sums.items()}
    z = level_heights(mean['ta'], mean['q'], half, gravity, gas, rv)                  # top first
    top = convection_top(mean['conv'], z, share)
    zb, thb = z[::-1], mean['theta'][::-1]                                              # the ground up
    n = np.sqrt(np.maximum(gravity * np.diff(np.log(thb)) / np.diff(zb), 0.0))
    cum = np.r_[n[0] * zb[0], n[0] * zb[0] + np.cumsum(n * np.diff(zb))]              # from the ground to each level
    kt = int(np.argmin(np.abs(zb - top['top_m'])))
    return dict(run=run.get('name'), years=[first, last], lat_limit_deg=float(lat_limit_deg), records=count,
                convection_top_m=top['top_m'], c_m_s=float(cum[kt] / math.pi),
                c_to_model_top_m_s=float(cum[-1] / math.pi), z_m=zb.tolist(), theta_k=thb.tolist())


def footprint_m(site: dict, radius_m: float) -> float:
    """The length (m) a box at the site stands for: the square root of the area within half_lat_deg of latitude and
    half_lon_deg of longitude of its centre, on a sphere of radius_m."""
    site = check_site(site)
    a = float(radius_m)
    return math.sqrt((2.0 * math.radians(site['half_lat_deg']) * a)
                     * (2.0 * math.radians(site['half_lon_deg']) * a * math.cos(math.radians(site['lat_deg']))))


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


def _nearest(hours, hour: float) -> int:
    """The index of the hour angle in `hours` nearest `hour` round the day."""
    return int(np.argmin(np.abs((np.asarray(hours, float) - hour + 180.0) % 360.0 - 180.0)))


def reference_column(forcing: dict, air: dict, reference=None, *, vapour: str = 'auto') -> dict:
    """The air of a box's nudging windows by local time, which CM1 holds the box to above the GCM's convection, draws
    in where the large-scale wind converges (inflow_ref_air) and, under a coupled wind, measures the box against:
    potential temperature (theta, K) and vapour mixing ratio (qv, kg/kg) as functions of height (m) and local hour
    angle (degrees), with the record of their source.

    'gcm-mean' (and None) is the GCM's mean air at the site, the air `air` (reference_air), at every hour.
    'gcm-by-hour' is that air with the GCM's own swing by local time at the site added, Terluna's reference for its
    damped-gravity-wave boxes: at each hour the fits' potential temperature less their mean over the day, and the
    vapour times the ratio of the fits' mixing ratio to its mean over the day, each at the bin of `bins` nearest the
    hour, interpolated in height and held beyond the GCM's levels. Its vapour follows the hour ('by-hour'), keeps the
    mean ('mean'), or follows the hour where the GCM's lowest level swings by more than VAPOUR_SWING of its mean
    through the day ('auto', Terluna's rule). A dict is a column series a case supplies, such as a box's own domain
    mean by local time: hour_angle_deg (n), z_m (m, rising), theta_k (n, levels) and qv_kg_kg (n, levels, CM1's
    mixing ratio), with an optional source; each hour takes the series' nearest hour, interpolated in height and
    held beyond its levels."""
    if vapour not in VAPOURS:
        raise ValueError(f"the reference's vapour is one of {VAPOURS}, where it is {vapour!r}")
    if reference is None or reference == 'gcm-mean':
        return dict(theta=lambda z, hour: np.asarray(air['theta_at'](z), float),
                    qv=lambda z, hour: np.asarray(air['qv_at'](z), float),
                    record=dict(source='gcm-mean', air="the GCM's mean air at the site at every hour"))
    if reference == 'gcm-by-hour':
        by = forcing['air_by_hour']
        zg = np.asarray(by['z_m'], float)[::-1]                              # the ground up
        hours = np.asarray(by['hour_angle_deg'], float)
        th = np.asarray(by['theta_k'], float)[:, ::-1]
        r = mixing_ratio(np.asarray(by['specific_humidity_kg_kg'], float)[:, ::-1])
        swing = float(by['lowest_level_vapour_swing'])
        follows = vapour == 'by-hour' or (vapour == 'auto' and swing > VAPOUR_SWING)
        th_dev, r_ratio = th - th.mean(axis=0), r / r.mean(axis=0)
        theta = lambda z, hour: np.asarray(air['theta_at'](z), float) + np.interp(z, zg, th_dev[_nearest(hours, hour)])
        if follows:
            qv = lambda z, hour: np.asarray(air['qv_at'](z), float) * np.interp(z, zg, r_ratio[_nearest(hours, hour)])
        else:
            qv = lambda z, hour: np.asarray(air['qv_at'](z), float)
        return dict(theta=theta, qv=qv, record=dict(
            source='gcm-by-hour', air="the GCM's mean air at the site with its swing by local time",
            vapour='by-hour' if follows else 'mean', vapour_rule=vapour, lowest_level_vapour_swing=swing,
            swing_threshold=VAPOUR_SWING, bins=int(hours.size)))
    if isinstance(reference, dict):
        hours = np.atleast_1d(np.asarray(reference['hour_angle_deg'], float))
        z = np.asarray(reference['z_m'], float)
        th, qv_ = (np.asarray(reference[k], float) for k in ('theta_k', 'qv_kg_kg'))
        if (hours.ndim != 1 or z.ndim != 1 or z.size < 2 or np.any(np.diff(z) <= 0.0)
                or th.shape != (hours.size, z.size)
                or qv_.shape != th.shape or not np.all(np.isfinite(np.r_[hours, z, th.ravel(), qv_.ravel()]))
                or np.any(th <= 0.0) or np.any(qv_ < 0.0) or np.any(np.abs(hours) > 180.0)):
            raise ValueError('a column series states hour_angle_deg (n, within 180 degrees of noon), z_m (rising), '
                             'and theta_k and qv_kg_kg (n, levels), finite, with a positive temperature and a vapour '
                             'of nil or more')
        return dict(theta=lambda zz, hour: np.interp(zz, z, th[_nearest(hours, hour)]),
                    qv=lambda zz, hour: np.interp(zz, z, qv_[_nearest(hours, hour)]),
                    record=dict(source=str(reference.get('source', 'a column series the case supplies')),
                                hours=int(hours.size), z_m=[float(z[0]), float(z[-1])], vapour='by-hour'))
    raise ValueError(f"a reference is one of {REFERENCES} or a column series, where it is {reference!r}")


def coupling_entries(forcing: dict, zw, *, mode: dict | None, length_m: float | None, time_s: float | None,
                     top_m: float | None, base_m: float | None, table_heat: str) -> tuple:
    """The &param3 entries of patch 10 of the lab's CM1 series for a box that makes its own large-scale vertical wind
    by the damped gravity wave, and their record. The wave's time is the length L the box stands for over the first
    baroclinic mode's speed c (mode['c_m_s'], first_mode's), lsw_tau = L/c to 0.1 s, with lsw_mode_speed = c to 1 mm/s;
    L is the site's footprint (footprint_m) unless the case states it, or the case states the time and L follows as
    time times c. The lid lsw_top is the GCM's convection top at the site and the lowest base lsw_base its lowest
    level, each to 0.1 m, unless the case states them; lsw_table_heat is 1 where the table heats below the base alone
    ('below-base'). Refused: a mode without a positive speed, a length and a time both stated, a length or time of
    zero or less, and a lid and base outside 0 <= base < lid <= the box's top."""
    if mode is None or not float(mode.get('c_m_s', float('nan'))) > 0.0:
        raise ValueError("the damped gravity wave takes the first baroclinic mode's speed: "
                         'mode=first_mode(run, years), or a dict with a positive c_m_s')
    c = float(mode['c_m_s'])
    if length_m is not None and time_s is not None:
        raise ValueError("a case states the coupling's length or its time, where it states both")
    if time_s is not None:
        if not float(time_s) > 0.0:
            raise ValueError(f"the coupling's time is positive, where it is {time_s}")
        tau, length, length_from = float(time_s), float(time_s) * c, 'the stated time times the speed'
    else:
        stated = length_m is not None
        length = float(length_m) if stated else footprint_m(forcing['site'], forcing['gcm']['radius_m'])
        if not length > 0.0:
            raise ValueError(f"the coupling's length is positive, where it is {length}")
        tau, length_from = length / c, 'stated' if stated else "the footprint of the GCM's site"
    lowest_m = float(np.asarray(forcing['profile']['z_m'], float)[-1])
    top = round(float(forcing['convection']['top_m']), 1) if top_m is None else float(top_m)
    base = round(lowest_m, 1) if base_m is None else float(base_m)
    if not 0.0 <= base < top <= float(np.asarray(zw, float)[-1]):
        raise ValueError(f"the coupled layer's base and lid lie at 0 <= base < lid <= the box's top, where they are "
                         f'{base} and {top} m')
    entries = dict(lsw_coupling=1, lsw_tau=round(tau, 1), lsw_mode_speed=round(c, 3), lsw_top=top, lsw_base=base,
                   lsw_table_heat=1 if table_heat == 'below-base' else 0)
    record = dict(
        kind='dgw', method='the damped gravity wave (Kuang 2008; Blossey, Bretherton and Wyant 2009), k2/eps = 1/(L c)',
        entries=dict(entries), length_m=length, length_from=length_from, time_s=tau, time_h=tau / 3600.0,
        mode={k: v for k, v in mode.items() if k not in ('z_m', 'theta_k')},
        top_m=top, top_from="the GCM's convection top at the site" if top_m is None else 'stated',
        base_m=base, base_from="the GCM's lowest level" if base_m is None else 'stated', table_heat=table_heat,
        record_file=LSW_RECORD_FILE)
    return entries, record


def case_inputs(forcing: dict, zw, air: dict, *, gravity_m_s2: float, start_hour_deg: float, solar_day_s: float,
                length_s: float, damping_base_m: float, nudge_tau_s: float, wind_nudge_tau_s: float = WIND_NUDGE_TAU_S,
                wind_from_m: float | None = None, inflow: bool = INFLOW, coupling: str = COUPLING, reference=None,
                reference_vapour: str = 'auto', start: str | None = None, mode: dict | None = None,
                coupling_length_m: float | None = None, coupling_time_s: float | None = None,
                coupling_top_m: float | None = None, coupling_base_m: float | None = None,
                table_heat: str | None = None) -> dict:
    """What a CM1 case takes from the forcing: its files (terluna_wls.txt, terluna_lsadv.txt and the nudging windows
    lsnudge_0001.dat on, as text), its namelist entries by section, the air it starts from and the record its case
    keeps. The box starts at the local hour angle start_hour_deg and runs length_s seconds of a solar day of
    solar_day_s, and its Rayleigh layer begins at damping_base_m. The case is refused where that layer begins below the
    GCM's convection's top plus one layer (proposed), where the box's top stands below the held air's first level, and
    where its windows outnumber the hundred files CM1 reads. Each window's wind is the GCM's at the window's middle
    hour, and its air the reference's at that hour (reference_column). &param8 sets the table (var11), the large-scale
    vertical wind (var13), the held air's heights (var14, var15) and the hour angle and solar day that core patch 17
    reads the table by (var18, var19), which the case's Sun shares; &param19 nudges the wind, temperature and vapour
    toward the windows on nudge_tau_s, from the first step and with no ramp, since CM1 restarts a ramp at each
    window's start. &param3 holds the three entries of patch 09 of the lab's CM1 series: the wind's own nudging time
    (wind_nudge_tau, wind_nudge_tau_s, 2 hours by default), the height from which CM1 pulls the wind (wind_nudge_zmin,
    wind_from_m, by default the GCM's lowest level to 0.1 m, and 0 for every level) and the inflow of the windows' air
    where the large-scale wind converges (inflow_ref_air, inflow, on by default). The case is refused on a wind's time
    of zero or less and on a height outside the box.

    The coupling sets the box's large-scale vertical wind. 'imposed', the default, imposes the GCM's mean vertical
    wind through terluna_wls.txt, lays the circulation's heating and moistening by local time in the table with the
    mean wind's advection of the starting air added back (to_cm1), fills the windows with the GCM's mean air and
    starts the box from it. 'dgw' lets the box make its own wind by the damped gravity wave (patch 10 of the lab's
    CM1 series, &param3's lsw_ entries from coupling_entries): terluna_wls.txt holds nil, which keeps CM1's
    large-scale vertical advection on (var13) to carry the wave's wind; the table holds the circulation's horizontal
    part alone, the circulation less the advection by the GCM's own vertical wind by local time, heating by default
    below the coupled layer's base alone (table_heat 'below-base', lsw_table_heat 1); the windows hold the GCM's air
    by local time ('gcm-by-hour'); and the box starts from its first window's air, so that the wave starts from rest.
    A case states its own reference (reference_column: 'gcm-mean', 'gcm-by-hour' or a column series such as a box's
    domain mean by local time) and its vapour rule, its start ('mean' or 'reference'), and for the wave the first
    baroclinic mode (mode, first_mode's result), the length it stands for or the time, its lid and its lowest base
    (coupling_entries); the record holds each with its source. A coupling's settings with the imposed wind are
    refused, as is a coupling other than 'imposed' and 'dgw': the weak temperature gradient joins with a later
    patch."""
    zw = _w_levels(zw)
    if not (length_s > 0.0 and solar_day_s > 0.0 and nudge_tau_s > 0.0):
        raise ValueError('a case runs a positive length under a positive solar day and nudging time')
    if not wind_nudge_tau_s > 0.0:
        raise ValueError("the wind's own nudging time is positive; nudge_tau_s states the held air's")
    if coupling not in COUPLINGS:
        later = ' (the weak temperature gradient joins with a later patch)' if coupling == 'wtg' else ''
        raise ValueError(f'the coupling is one of {COUPLINGS}, where it is {coupling!r}{later}')
    coupled = coupling != 'imposed'
    table_heat = table_heat or ('below-base' if coupled else 'every-level')
    start = start or ('reference' if coupled else 'mean')
    if table_heat not in TABLE_HEATS or start not in STARTS:
        raise ValueError(f'the table heats {TABLE_HEATS} and a box starts from {STARTS}, where they are '
                         f'{table_heat!r} and {start!r}')
    stated = dict(mode=mode, coupling_length_m=coupling_length_m, coupling_time_s=coupling_time_s,
                  coupling_top_m=coupling_top_m, coupling_base_m=coupling_base_m)
    if not coupled and (table_heat != 'every-level' or any(v is not None for v in stated.values())):
        raise ValueError(f"the imposed wind takes none of a coupling's settings, where the case states "
                         f"{sorted(k for k, v in stated.items() if v is not None) or ['table_heat']}")
    lowest_m = float(np.asarray(forcing['profile']['z_m'], float)[-1])     # the GCM's lowest level (top first)
    pulled_from_m = round(lowest_m, 1) if wind_from_m is None else float(wind_from_m)
    if not 0.0 <= pulled_from_m < zw[-1]:
        raise ValueError(f"the wind's pull starts at a height from the ground up to below the box's top, here "
                         f"{pulled_from_m} m")
    convection = forcing['convection']
    clearance = check_damping(convection, damping_base_m)
    held = held_heights(convection, zw[-1])
    lsw, coupled_record = {}, dict(kind='imposed', vertical_wind="the GCM's mean, imposed (terluna_wls.txt)")
    if coupled:
        lsw, coupled_record = coupling_entries(forcing, zw, mode=mode, length_m=coupling_length_m,
                                               time_s=coupling_time_s, top_m=coupling_top_m, base_m=coupling_base_m,
                                               table_heat=table_heat)
    ref = reference_column(forcing, air, reference if reference is not None else
                           ('gcm-by-hour' if coupled else 'gcm-mean'), vapour=reference_vapour)
    zh = 0.5 * (zw[1:] + zw[:-1])
    heights = np.r_[0.0, zh, zw[-1]]
    windows = wind_windows(forcing, heights, start_hour_deg, solar_day_s, length_s)
    if len(windows) > CM1_NUDGE_FILES:
        raise ValueError(f'{len(windows)} nudging windows; CM1 reads at most {CM1_NUDGE_FILES}')
    first_hour = windows[0]['hour_angle_deg']
    start_air = air if start == 'mean' else dict(air, theta_at=lambda z: ref['theta'](z, first_hour),
                                                 qv_at=lambda z: ref['qv'](z, first_hour))
    laid = forcing
    if coupled:                     # the table holds the circulation's horizontal part, and the GCM's wind is nil
        laid = dict(forcing, circulation=forcing['horizontal'],
                    vertical_wind_m_s=[0.0] * len(forcing['vertical_wind_m_s']))
    cm1 = to_cm1(laid, zw, start_air, gravity_m_s2)
    files = {WLS_FILE: wls_text(zw, cm1['w_m_s']), LSADV_FILE: lsadv_text(cm1['table'])}
    for i, window in enumerate(windows, 1):
        t1, t2 = window['time_s']
        hour = window['hour_angle_deg']
        files[f'lsnudge_{i:04d}.dat'] = nudging_text(t1, 1.0e30 if i == len(windows) else t2, heights,
                                                      ref['theta'](heights, hour), ref['qv'](heights, hour),
                                                      window['u_m_s'], window['v_m_s'])
    namelist = dict(
        param3=dict(wind_nudge_tau=float(wind_nudge_tau_s), wind_nudge_zmin=pulled_from_m,
                    inflow_ref_air=1 if inflow else 0, **lsw),
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
    if coupled:
        coupled_record.update(
            vertical_wind="the box's own; terluna_wls.txt holds nil",
            table="the circulation's horizontal part: its tendencies less the advection by the GCM's own vertical wind "
                  "by local time", gcm_column_vapour_mm_day=forcing['horizontal']['column_vapour_mm_day'])
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
        inflow=dict(on=bool(inflow), reference="the windows' air, the reference's at each window's hour",
                    rate="max(d(rho0 w)/dz, 0)/rho0, the large-scale vertical wind's convergence over CM1's "
                         "base-state density",
                    rates_file=INFLOW_RATES_FILE),
        coupling=coupled_record, reference=ref['record'],
        start=dict(source=start, hour_angle_deg=float(first_hour) if start == 'reference' else None,
                   air="the reference's air in the first window" if start == 'reference' else
                       "the GCM's mean air at the site"),
        vapour="CM1's mixing ratio, from the GCM's specific humidity: r = q / (1 - q), the moistening times (1 + r)")
    return dict(files=files, namelist=namelist, record=record, cm1=cm1, windows=windows, start=start_air)
