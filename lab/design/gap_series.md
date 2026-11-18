# The gap between ExoPlaSim and CM1: a series across three worlds

A study of 9 November 2026, by reading and arithmetic; no model ran. That day Terluna moved the work of closing the
gap between its GCM and CM1 to this project, carrying the gap as a range in its own studies meanwhile (Terluna's
`research/decisions.md` at `03da9585`, line 846). The study asks whether ExoPlaSim and CM1, run on the Moon, a
low-gravity waterworld and Earth, can separate the gap's causes without a third model, ROCKE-3D lying beyond the
machine's present resources, and whether MITgcm belongs in the lab. By the author's decision of 9 November 2026,
MITgcm stays out of the lab for now, and section 2 keeps the assessment behind that decision. The series is a
proposal: its runs wait on the stages and ports named below, and on the author's word (`PLAN.md`, "Decisions").

Tags: [read] a named source; [calc] arithmetic here; [lit] published work, "to verify" marking a figure unchecked
against its source; [int] interpretation; [prop] proposal. The paper is cited from its version 2 draft on
`paper/conclusion-development` at `b272157`. "The dilution report" is Terluna's
`session-tools/agents/gap_boxes/dilution_question/report.md`, on its research drive.

**Answers.** Comparing the two models on the Moon, a waterworld and Earth, the lab can separate four causes: the
GCM's convective closure, CM1's grid, the box's ascent and the microphysics [prop]. On Earth each model can be judged
against ERA5 and observed forcing, the evidence independent of the comparison that the paper's agreement test
requires [read: paper `results.tex`], and a waterworld can take nearly the Moon's gravity and its day with no land.
Where the cause lies outside gravity similarity, the Moon's true upper air stays unsettled. As the gap's third model
MITgcm adds little; as an ocean it would suit the lab later [prop].

## 1. The series

| | Moon | Twin: the flagship's anchor near the transition, all ocean | Earth control |
|---|---|---|---|
| g (m/s²); H (km) | 1.62; 53 [read] | 1.48; 58 at 301 K [read: `waterworlds.md`; calc] | 9.81; 8.4 [read] |
| Air per m² (t) | 74.9 [read] | 82 at 1.2 atm; the family at 1 bar, 40–83 [calc] | 10.3 [read] |
| Solar day; rotation | 29.5; 27.3 d [read] | 29.5; 27.3 d, the Moon's, set on 11 November 2026 with the Open Moon's air at 1.2 atm (`PLAN.md`, "Decisions") | 1; 1 d |
| T21 cell in scale heights | 3.2 [calc] | 4.5; the family 3.2–11.4 at 301 K [calc] | 74 [calc] |
| CM1 box of 32 × 32 columns, minutes per Earth day on 4 threads | 2.0 [read: Terluna `climate/crm/README.md`, 59 days in 2.0 h] | 1.9 [calc] | 12.3 [calc] |

Under rule 9, CM1's grid, top, hold and step follow H [read: `world_spec.md`], so under dry similarity a lunar box is
an Earth box stretched sixfold [read: paper `worlds.tex`]. The similarity breaks for radiation, since the lunar column
holds 7.25 times Earth's absorbing mass; for sedimentation, since rain falls at 0.34 of Earth's speed [read:
`worlds.tex`]; and for clocks set in seconds or days. Simplified Betts–Miller's Earth relaxation of 2 h scales to 12 h
on the Moon, inside the 11–27 h over which CM1 removes lunar instability, while the lunar runs keep 2 h [calc; read:
Terluna `research/decisions.md`, 2 November; `terluna_fixes.md`, row 12], and the lunar day scales to 4.9 Earth days
[calc]. An error within similarity shows on Earth as well, whereas an error outside it shows only off Earth and grows
with the departure from Earth's gravity, column mass or day [prop].

The table names one further cause. The Moon's T21 cell spans the equivalent of 27 km on Earth [calc], fine enough for
resolved ascent to take part of the convection scheme's place, as it does under the nearest closure tried, which
leaves 58–74% of the tropics' rain to large-scale condensation [read: `notes/exoplasim.md` on the paper's branch,
"The closures tried with simplified Betts–Miller convection"; prop]. A T21–T42 pair on the
Moon, about ×8 in cost, would test it [calc; prop].

| Cause | Comparison that separates it | Implicated if | Left unseparated |
|---|---|---|---|
| The GCM's closure: undiluted reference, humidity 0.7, 2 h, trigger | The Earth control against ERA5, by Palmer and Singh's zero-buoyancy diagnostic | ExoPlaSim's raining Earth tropics read near-zero effective entrainment, as the lunar design years do (−0.24 to 0.08 per e-folding of pressure), against ERA5's 0.15–0.4 per km [read: the dilution report, after Palmer and Singh 2025] | Which element errs, all of them tuned together |
| CM1's dilution and grid | CM1 on Earth at 1 km, the scaled twin of the lunar 6 km, and at 200 m | The 1 km run dilutes beyond ERA5's range and the 200 m run moves toward it; CM1's lunar band rates scale to 0.6–1.0 per km on Earth [calc] | The width of lunar plumes, whose cores fill one or two 6 km cells [read: the dilution report] |
| The box's ascent | Earth boxes, imposed and by the damped gravity wave (DGW); DGW against its own world's radiative–convective equilibrium, the test of Daleu et al. (2015) [lit] | Earth's imposed boxes rain within 10% of the forcing's rain, as 13 CRM runs did over TWP-ICE's active period [lit: Fridlind et al. 2012, to verify], where lunar ones rain 0.75–0.84 of it [read: paper `results.tex`]; or the lunar DGW leaves its reference while Earth's holds | Which method is right on the Moon |
| Microphysics at low gravity | The gravity pair under prescribed, scaled cooling [read: Terluna `climate/crm/README.md`, "The gravity pair"]; the family's gravities | The pair departs from similarity in dilution or in the rain evaporated (CM1 0.69, GCM 0.51 at sea [read: paper]), more as g falls | Morrison's Earth-calibrated ice at low gravity |
| Radiation | The pair, which removes it; the Moon at 1.0 against 1.2 atm, 17% less column [read: `lab/worlds/moon`; calc] | An excess survives the pair and grows with column mass | Errors in the reference spectroscopy that both models share |
| Surface exchange | One law over water in both already [read: paper `repairs.tex`]; the box's wind 0.72–0.81 of its target after midnight [read: Terluna `climate/crm/README.md`, branch `domain/climate`] | The twin repeats the shortfall | Little from the series; a lunar box nudged faster tests it [prop] |

**The steps, Earth first** [prop]. A GCM year costs 8.7 minutes on four threads [read: `terluna_fixes.md`], and the
boxes cost as in the first table.

| Step | Runs | 4-thread hours [calc] | Decision |
|---|---|---|---|
| 1. CM1's RCEMIP output at 300 K, at 1 km and 200 m [lit: Wing et al. 2020; the 200 m runs to verify], through the dilution report's zero-buoyancy inversion | None; a rights review first | <1 | Whether the Earth twin of the lunar grid dilutes as ERA5 does |
| 2. The Earth control with the Moon's GCM refinements, on the Moon's fifteen σ levels (lowest near 50 m [read: `terluna_fixes.md`, row 9]), beside Kuo | 2 × 10 y | 3 | Whether simplified Betts–Miller's warm band exists on Earth; if so, a closure refitted to ERA5 and scaled by H is admissible |
| 3. CM1 at 965 m under observed TWP-ICE forcing (period to verify) | 1 × 16 d | 3 | Whether the box machinery and the scaled grid reproduce observed rain and upper air |
| 4. Boxes forced by step 2 at a warm-pool sea and at tropical land, imposed and DGW | 4 × 12 d; 2 GCM y | 10 | Whether the pair passes the agreement test on Earth |
| 5. The gravity pair, each member then under DGW against its own radiative–convective equilibrium | Earth 60 d; Moon 360 d | 24 | The microphysics against similarity; the DGW's yardstick at lunar parameters |
| 6. The twin: ExoPlaSim, then sea boxes imposed and DGW | 1 × 10–20 y; 2 × 5 lunar days | 11–12 | Whether the sea's night-rain gap (GCM 50%, CM1 8.5–9.5% [read: paper `results.tex`]) needs land |
| 7. If step 5 departs: anchors at g 1.2 and 2.5 | 2 GCM; 4 boxes | 29 | Whether the departure grows as g falls |

The CM1 steps wait on stage 3, Terluna's DGW ported as patch 10 of the lab's CM1 series (17 November 2026;
`terluna_fixes.md`, row 13), with the weak temperature gradient beside it as patch 11 (18 November 2026), and steps 2, 4
and 6 on the GCM ports of `PLAN.md` step 2. Steps 1–6 take about 52 four-thread hours, three or four nights at the
eight-thread budget [calc].

**Checks ahead of the series** [prop]. A pass over the models on 9 November 2026 logged five entries that bear on
what the series would compare (`notes/defect_log.md`, B36–B39 and C22): the horizontal diffusion's Earth times, the
slab sea's 50 m, Morrison's warm rain at Earth's rates, the relaxation time of 2 h, and the Moon's monthly swing in
sunlight. One GCM run or one sea box of two lunar days sizes each of the first four: the mixed layer at 15 m, the
warm-rain factors at 0.166 and 0.34, the design scheme's relaxation time at 10 h, inside the grid's bound of about
11 h at T21 (section 3) and near the 12 h that gravity's similarity gives, a time Terluna ran only beside closures
with reference profiles of their own, and the diffusion times multiplied by 0.27. The
sea's rain by time of day depends most directly on the mixed layer and the warm rain, so those two come first.
Terluna's records of 10 November add two facts about the sea's exchange [read: Terluna `research/decisions.md` at `59dcda1c`, lines
860–871]: its lake model puts a calm sea's surface at 37.1 °C in the hottest hours where the slab shows 30.9 °C, and
a year written every 6.5 hours shows the GCM's flow holding 1.13 times the speed of its 3-day mean vectors over
water, speed that a box nudged to the mean vector lacks in its surface exchange (`notes/cm1.md`, "The wind inside
the GCM's means").

**The series' limits.** If Earth passes and steps 5 and 6 implicate lunar physics, the lab learns which physics
matters, and with no observation of lunar convection it has no measure of which model represents it. Finer lunar grids
then remain, ×8 at 3 km and ×27 at 2 km [read: `terluna_fixes.md`]; GATE's cores, mostly under 2 km, translate to
under 12 km on the Moon [read: the dilution report], so several cells across a lunar core take about 1 km, ×216
[calc; prop]. Two limits hold whatever the outcome: errors common to both models stay invisible to their comparison,
and Earth's idealised benchmarks are wide, RCEMIP's models differing by up to 10 K at a height [lit: Wing et al. 2020,
to verify], so ERA5 and observed forcing give the sharp targets. Within the family, moreover, radius follows mass by
Sotin's relation, so g, H/R and the cell in scale heights change together [read: `waterworlds.md`; calc].

## 2. MITgcm, left out for now

| Package | Physics | Earth values compiled in checkpoint69s [read: Terluna's checkout, `ocean/src/MITgcm` on the research drive] | Convection independent of simplified Betts–Miller |
|---|---|---|---|
| atm_phys | Frierson's simplified Betts–Miller (2 h, humidity 0.8); gray radiation | GRAV 9.80, RADIUS, OMEGA (`constants_mod.F90`) | No: the family of Terluna's scheme [read] |
| aim_v23 | SPEEDY's mass flux, 6 h toward humidity 0.8; four bands; its level count from the grid (`NLEV = Nr`, `AIM_SIZE.h`), five in each of MITgcm's own set-ups (`verification/aim.5l_*`) | SOLC 342 W/m², hour constants; gravity from the core | In form; the Moon's 0.3 km layer needs more levels than those set-ups' five, and a retuning with them [read; int] |
| fizhi | Relaxed Arakawa–Schubert, Chou–Suarez radiation, Mellor–Yamada 2.5, Koster–Suarez land [read: MITgcm's documentation] | GRAV 9.81, S0 1,365, SDAY, YRLEN, CO2 355 ppm, SRFPRS 984.7 hPa (`getcon.F`) | Yes |

MITgcm's core reads gravity, radius, rotation, R and cp from namelists, and Terluna ran checkpoint69s unchanged on
the Moon's seas [read: Terluna `climate/ocean/README.md`]. No package resolves moist convection, so CM1 keeps its
place [read: `pkg/`]. The deep-atmosphere option runs in pressure coordinates, where a gravity profile is refused
("Variable gravity not yet implemented for P-coordinate", `model/src/config_check.F`) [read], so MITgcm could test the
shells' geometry in the paper's question of tall air, with gravity held constant [prop].

For the gap, atm_phys would relax its air toward the undiluted parcel as PlaSim's scheme does, aim_v23 would need more
levels and a retuning, and fizhi alone brings a full independent scheme, with the most Earth values to replace, a
port of weeks [prop]. Any third GCM sets its upper air by its own Earth-tuned convection, which the lab would audit as
it audited PlaSim's [prop], while PlaSim as Terluna patched it already switches among Kuo, simplified Betts–Miller
and a mass-flux scheme (`nprc`) [read: `plan.md`].

Terluna's tide run took 1.6 µs of core time per cell-step (3.6 h on four processes, 64,195 steps, 516,076 cells)
[read; calc]. At three to six times that, a 6 × 16 × 16 cubed sphere on 20 levels at 30-minute steps would take 10–20
minutes a model year on four cores, ExoPlaSim's order, as would aquaplanet and radiative–convective set-ups [calc;
untimed].

MITgcm's strengths for the lab lie in the ocean, where the ensemble has a 50 m slab [read]: sea ice; coupled
aquaplanets run for millennia and into multiple equilibria (Marshall et al. 2007; Ferreira, Marshall and Rose 2011)
[lit]; a non-hydrostatic ocean for the seas' night convection, on Terluna's list of next work [read]; tracer and
carbon packages [read]; and the cubed sphere. These would serve the ocean that carries heat sideways beneath a locked
world's day side, a possible later addition in `waterworlds.md` [read], once the forcing package's bulk formulas pass
the audit of Earth terms that Terluna names [read].

**When to weigh it again** [prop]. As the lab's ocean, when stage 12 or the seas need heat carried by water, with the
shells' geometry as a second use. For the gap, if steps 2–6 clear both convection schemes and leave PlaSim's core or
cell under suspicion, atm_phys on the cubed sphere, with simplified Betts–Miller held, becomes a test worth days of
porting. An independent scheme in a full GCM would set fizhi against Isca's relaxed Arakawa–Schubert with RRTM or
SOCRATES radiation [lit: Vallis et al. 2018], already in Terluna's table of candidates [read: Terluna
`climate/gcm/README.md`]. ROCKE-3D, whose SOCRATES radiation is validated for nitrogen–oxygen–water air at other
pressures [read: same], would come ahead of both once the machine's resources allow it.

## 3. The yardstick read again, 17 November 2026

Two studies on the lab's research drive read Terluna's existing output again, with no model run: a review of the
routes to closure (`agents/gap_alternatives/`, with the lead's corrections beside it) and four readings, each under
rules fixed before it was computed (`agents/gap_readings/`) [read]. They move the first step from the GCM's
convection to the coupling through which a CM1 box meets the GCM.

**The coupling sets the state CM1 works from.** By night the couplings hand the sea box air far apart, the GCM's
night beside them [calc: `gap_readings`, path 1]:

| Night means at the sea site | θe*_L (σ 0.85–0.50), K | θe_B (σ 1.0–0.85), K | B_L, K | Rain, mm/day |
|---|---|---|---|---|
| CM1 under the GCM's imposed ascent | 314.7 | 322.1 | +2.5 | 0.25 |
| CM1 carrying the GCM's weather | 316.6 | 322.6 | +1.1 | 0.55 |
| CM1 making its own ascent (DGW) | 327.8 | 328.1 | −3.4 | 1.68 |
| The GCM, written every 5.5 hours | 328.2 | 321.6 | −7.9 | 1.48 |

Under imposed ascent the box's free troposphere cools as the box spins up, by night 13.5 K below the GCM's in
saturation θe, and the box rains little under the imposed descent. Making its own ascent, the box keeps the GCM's free
troposphere, its boundary layer rises to that air's saturation θe, and it rains more after midnight than the GCM
[calc]. The night's dry box, the evening's dry air near the sea and the dilution study's target, a band about 3.5 K
below the fine undiluted parcel, all come from boxes under imposed ascent; under the DGW, CM1's raining band stands
0.15 K above its own parcel [calc; read: the dilution report]. The couplings' own consistency is therefore tested
before either model's convection changes again, as the review proposed in its path 2: the DGW measured against the
imposed box's own mean by local time, a weak-temperature-gradient coupling, and the DGW at the planet's scale [prop].
The second is patch 11 of the lab's CM1 series (18 November 2026), in the form Edman and Romps (2015) found
self-consistent, on the DGW's reference, time, lid and base [code; lit: Edman and Romps 2015, sections 3.1–3.4 read in
Edman's 2017 thesis].

**The GCM's convection starts at a buoyancy where neither CM1 nor Earth's tropics rain.** By B_L, the lower
troposphere's plume buoyancy of Ahmed and Neelin (2018) with its layers taken as shares of the surface pressure, the
GCM's rain picks up at −7.5 to −8.6 K at every site and in every run read, against CM1's −2.5 to +1.4 K and Earth's
pickup near nil [calc; lit: Ahmed and Neelin 2018, read in full]. Under the DGW, in the GCM's own free troposphere,
CM1's 72 outputs between −6.5 and −5.5 K rain 0.00–0.01 mm/day [calc]. The GCM's lowest level holds a θe 4.2 K above
its boundary layer's mean, where CM1's under the DGW stands within 0.5 K of its layer's, and the scheme lifts the
lowest level's air alone, so it fires on a moist surface layer beneath drier air; PlaSim's vertical mixing leaves the
vapour falling off through layers CM1 keeps uniform (defect log B32) [calc; int]. The GCM's candidates are a trigger
on the lower troposphere's buoyancy, with Earth's onset statistics as its evidence apart from the comparison, and the
boundary layer's mixing [prop].

**Ruled out or bounded** [calc]:
- **A downdraught** for the GCM's evening sub-cloud layer: its convection already removes 1.9–2.3 mm/day there, 25–55
  times CM1's resolved export, and the layer's state differs between the couplings.
- **Grid-point storms** behind the redesigns' large-scale condensation: the isolated cells ascend no faster than their
  neighbours.
- **The relaxation time:** the grid bounds it near 11 h at T21 (10.7 h from the year written every 6.5 hours), so the
  12 h that gravity's similarity gives lies just past the bound, and B39's run takes 10 h (`PLAN.md`, block 4,
  step 3).
- **The domain:** the radiative conditions under which small domains turn episodic (Seeley and Wordsworth 2021; Song,
  Abbot and Yang 2024, read in abstract) hold in the sea boxes, so a box of 192 km may be small for the night's rain,
  and a larger sea box comes before any verdict on the night [lit; prop].

Two of the review's claims fell to checks against the records (`agents/gap_alternatives/corrections.md`), and one of
Terluna's records counts the boundary layer's vapour twice in one row (`followups/report_subcloud.md`, its turbulence
row) [read; calc].

## First steps, at the author's word [prop]

1. After a rights review, read CM1's RCEMIP output at 300 K, at 1 km and, if CM1 ran it, at 200 m, through the
   dilution report's zero-buoyancy inversion: no runs, and it settles whether CM1 at the lunar grid's scaled spacing
   dilutes as ERA5 does.
2. With the GCM ports of `PLAN.md` step 2 in place (simplified Betts–Miller, the fifteen-level set, the gust and the
   evaporation from drop sizes), run the Earth control beside Kuo (about 3 hours) and read Palmer and Singh's
   diagnostic on its raining tropics.
3. With stage 3 built and the DGW ported (patch 10 of the lab's CM1 series), run the gravity pair under prescribed
   cooling, each member then under DGW against its own radiative–convective equilibrium (about 24 hours).
