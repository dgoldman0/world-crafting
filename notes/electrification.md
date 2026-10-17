# Electrified CM1: correctness, limits and room for improvement

Notes on the electrified build: WRF-ELEC's NSSL two-moment microphysics with charge (MicroTed/wrf4-elec
at e43041b), grafted into CM1 r22.0, the five Fortran files in [../models/cm1/fortran/](../models/cm1/fortran/)
and `series-elec`. References to Terluna are at commit 186b294 (`climate/crm/README.md` "Electrified
storms" and its subsections; `climate/crm/cm1_elec.py`).

## What the graft does

WRF-ELEC carries charge on cloud droplets, rain, cloud ice, snow, graupel and hail through every
microphysical process, separates it by non-inductive charging (Saunders and Peck's law with Brooks et
al.'s critical rime accretion rate by default) and inductive charging, and hands the small ions' net
charge to particles. CM1 has no electricity of its own. The graft:

- replaces CM1's copy of the NSSL module with WRF-ELEC's (the same scheme, maintained by the same author,
  with the electrification kept), routes CM1's microphysics calls to `terluna_nssl_elec`
  (`terluna_elec.F`), which reorders CM1's (i, j, k) arrays to WRF's (i, k, j) and keeps the charges in
  CM1's passive tracers without their positivity limiter;
- runs the step as WRF-ELEC's driver does: microphysics without sedimentation, then sedimentation in
  sub-steps, each followed by a field solve and lightning, then leakage once a step;
- solves Poisson's equation for the potential by FFT across the periodic domain with a tridiagonal solve
  on CM1's stretched levels, potential zero at the ground and the model top (`terluna_lightning.F`);
- carries WRF-ELEC's cylindrical discharge (`light1d`) and its branched lightning (`lightmsz`, MacGorman
  et al. 2001), the latter run one flash at a time on one process on a domain that wraps round
  (`terluna_branched.F`, with WRF-ELEC's `mlint2` taken out as `terluna_mlint2.F`);
- ports WRF-ELEC's screening layers at cloud edges and adds point discharge from the ground, which
  WRF-ELEC lacks (`terluna_screen.F`);
- keeps the vertical field for the next step's inductive charging across restarts.

## Correctness

**Unit tests** (Terluna `climate/tests/test_cm1_elec_field.py`, `_branched.py`, `_screen.py`): the
potential matches a direct solve of the same difference equations on stretched levels to one part in
10⁵ and the exact potential of a charged layer between grounded plates to one part in 10³; a cylinder
call removes the charge WRF-ELEC's rule sets, only inside the cylinders, and counts regions across the
domain's edges; a branched flash between two charge regions neutralises equal positive and negative
charge; a flash at the domain's edge reaches both sides; a channel through a strong lower positive region
strikes the ground with negative charge and the mirror storm with positive; screening charge gathers on
cloud tops and bases as the formula gives, never inside clouds or past its cap.

**Benchmark against CM1's own NSSL** (the Weisman–Klemp supercell at Earth's gravity, two hours): largest
updrafts within 6% at every half hour, reflectivity within 3.4 dBZ, condensate within 9%, graupel within
12% from 30 minutes, cloud-ice number within a factor of 1.5, hail within a factor of two (the two copies
are different versions of the scheme). Reproduction: restarted at 30 minutes on 4 threads and on 2, the
storm repeats its first run's fields and its 41 flashes bit for bit.

**Against published runs of the same schemes** (no published run puts them in CM1): first flash at 28.5
min against 27–40 min; peak flash rate 153 per minute against 34–600 in the literature; median 9.4 C per
flash against 2.7–39.6 C; net charge densities up to ±4.8 nC/m³ against about 1–4; non-inductive
charging several times stronger and charge per particle type tens of times larger, traced to cloud ice
at up to 2×10⁸ crystals per kg where droplets freeze homogeneously in 50 m/s updrafts.

**Faults found and fixed during the work** (Terluna's record): the first version discharged once per
6 s step, after all its sedimentation, and the field stood a median 3.2 times above breakdown at a
step's first discharge (fixed by WRF-ELEC's sub-steps); the gravity scaling multiplied uninitialised
memory where the scheme had set no graupel exponent, and the OpenMP directive privatised fall-speed
moments set before the loop (both found as thread-dependent results, located with signalling-NaN
builds); rain and cloud-ice ventilation stayed at Earth's speeds, so lunar rain evaporated 1.3–1.5 times
too fast for its drop sizes until 2026-10-06.

## Lunar adaptations

| Change | Why | Kind |
|---|---|---|
| Fall speeds, collection coefficients and ventilation scaled by (g/9.81)^((b+1)/3) where each particle is present; drag-law particles and Stokes droplets with the host g | The scheme's fitted laws are Earth's | General repair |
| Sub-step 6.8 s in place of 0.75 s | Keeps graupel settling about 1% of a layer per sub-step in the lunar charging zone's 2 km layers at 0.44 of Earth's fall speed | Setting from a scaling argument |
| The 180 kV/m cap on the breakdown field lifted (`lightning` 4) | The breakdown field is density-scaled; the cap binds below about 4.5 km on Earth, beneath where flashes start, but below about 36 km in the lunar air, where they start | General repair for denser or taller air |
| WRF-ELEC's ground-strike rule (a downward channel reaching −7 °C in charge of the matching sign) with a leader's crossing at 1 kV/m internal field scaled by density | −7 °C stands about 34 km up on the Moon against 3–5 km on Earth; the rule alone counts a channel there as reaching the ground, WRF-ELEC's 0.15-of-breakdown stopping field halts every lunar channel 15–25 km up | Bounded repair |
| Leakage through the lunar conductivity column | Without it the charge evaporating cloud leaves on the ions stays for weeks and holds the field at the ground near 20 kV/m over the whole box | Capability |
| Point discharge from the ground (off by default) | Holds the field at the ground near its onset under storms | Capability |

## What the lunar storms give (main run `box_0e_elec_corrected`, two lunar days)

530 flashes, 106 of them negative to ground (20%), none positive; 0.022 flashes per km² per year over
the box, about a hundredth of Earth's average; flashes start a median 35.8 km up; in-cloud flashes
neutralise a median 108 C and ground strikes lower 149 C (Earth's lower 5–30 C); hail does 87% of the
non-inductive charging; the main negative charge sits at 40–42 km (−13 to −14 °C), as on Earth just
above the −7 °C level. Storms take about an hour from core to first flash and flash 190–1,500 times less
often at their busiest than the Earth benchmark. With the NSSL scheme in place of Morrison's the same box
runs 1.0 °C warmer at 2 m and its night fog halves, so the lunar night fog depends on the microphysics
scheme by about a factor of two.

## Limits

- **Earth calibration kept**: flashes start at 0.9 and run while the field exceeds 0.8 of breakdown; the
  branched channel's internal field is 200 V/m; a ground strike needs a starting potential beyond 50 MV
  and a field above 10 kV/m; nitrogen oxides at Wang et al.'s yield times 0.1. The leader's crossing uses
  the column below the channel's start (the drawn path is vertical) and leaves out whether a downward end
  forms, whether the cloud end holds the channel's potential through the 0.2–0.4 s crossing, and current
  cutoff in a long branched channel.
- **Charging laws** come from laboratory collisions at Earth's impact speeds. Lunar graupel strikes ice at
  1.3–1.5 m/s and snow at 0.8–1.0 m/s; Saunders and Peck's law nearly stops for graupel riming below its
  threshold, and hail, which rimes faster, does most of the charging. Under Takahashi's law the storms
  separate as much charge but carry an inverted dipole.
- **Resolution**: 6 km columns (about 1 km at Earth scale). On the benchmark a coarser grid gives fewer,
  larger flashes; the 2 km lunar box charged a storm to 73% of breakdown without a flash and its deep
  convection collapsed, so how much of the lunar flash delay and rate the grid sets is open.
- **Physics left out**: terrain under the field solver; the small ions' drift in the field; three-moment
  arrays; CM1's own water budget from the NSSL scheme. Runs on several threads are realizations.

## The conductivity column and the charging laws (`python/atmosphere/electricity/`)

Two in-house tools stand behind the lunar settings. `conductivity.py` builds the column that leakage
(`var9`) and the screening layers read: ion production from the CRAC:CRII v2 tables above Earth's sea-level
depth and from MCEq muons and their decay electrons below it (`muons.py`, run in its own environment),
then the small ions' recombination, mobility, and attachment to aerosol swollen by the air's humidity
(κ-Köhler, κ 0.3 with 0.1 and 1.0 as a bracket, 100 particles per cm³) and to cloud droplets.
`charging.py` integrates graupel's rebounding collisions with crystals and snow over both size
distributions under four laboratory laws, Saunders and Peck with WRF-ELEC's critical rime accretion rate and
Takahashi's table among them, at lunar impact speeds.

**Correctness.** The ion chain reproduces Earth's measured fair-weather positive conductivity within 2–8% from
5 to 30 km at a 3 GV cutoff; MCEq gives Earth's sea-level vertical muon intensity within 6–13% of the
Bogdanova et al. fit above 10 GeV/c (51 against 76 m⁻² s⁻¹ sr⁻¹ above 1 GeV/c, where three-dimensional effects
matter); the charging integrals reproduce WRF-ELEC's critical rime accretion rates and Takahashi's tabulated
charges (Terluna `atmosphere/electricity/README.md` 18–36). The 16 tests brought here passed on 2026-10-17;
three need the fetched inputs.

**Limits.**
- The aerosol is one assumed state (100 cm⁻³, κ 0.3). Terluna's aerosol study puts the ground's conductivity
  at 2.2–2.7 × 10⁻¹⁵ S/m across regions (0.6–4.7 across its cases), against this column's 3.7 × 10⁻¹⁵ S/m.
- Ion attachment scales with mobility as in the continuum regime at every height (defect log C15); with Fuchs
  and Sutugin's transition factor the clear air would conduct 5–12% more at 34 km, 12–25% more at 50 km and
  23–45% more at 70 km. The column's values aloft are the low end, kept by the author's decision until the
  regional aerosol rebuilds the column.
- Mobility and recombination carry no humidity term; ionization below Earth's sea-level depth comes from
  muons alone, and the lunar cutoff rigidity and modulation are one choice.
- The charging laws are Earth's laboratory laws; at the lunar impact speeds (graupel on ice 1.3–1.5 m/s) they
  are extrapolated, and the deciding measurement, for fast rimed ice in little cloud water at −5 to −16 °C, is
  unavailable.

**Improvement.** Rebuild the column with the regional aerosol and the transition-regime attachment; carry the
column's uncertainty into leakage as a bracket; laboratory or theoretical charging at lunar impact speeds.

## Improvements in order of value

1. Laboratory or theoretical charging rates at lunar impact speeds and riming rates.
2. A finer box over a stormy window with a sound initial state, to separate the grid from the physics.
3. A leader model for the long crossing, with the drawn path's geometry.
4. Ion drift, so point discharge and screening act in calm air as measured.
5. An independent electrification model on the same storms.
