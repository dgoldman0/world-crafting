# Outline

Stage 3 of the build. The argument by section, each paragraph's governing relation (charter G1), the
figures and tables, and where each number comes from. Headings are unnumbered and few; run-in bold leads
carry the few divisions a section needs.

**Working title.** Earth inside the models: adapting ExoPlaSim 3.4.2, CM1 r22 and SWAN 41.51 to a
breathable Moon. (GMD asks for model names and versions in a model paper's title.)

**Through-line.** The models carry Earth in five forms; the Moon exposes them because it moves several
governing ratios at once; the repairs either remove a form of Earth for every world or calibrate it for
one column; checks of each kind establish different things; the adapted models have located the lunar
climate's remaining uncertainty and reach a definable set of other worlds; the next work follows from
where the uncertainty now sits.

## Abstract (≈250 words)

Question → regime → five forms → repairs in two classes → verification → what it gave (sensitivities,
uncertainty located, storms, seas) → reach → availability. Lands on the general/calibration distinction
as the portable result.

## Introduction

1. **The question** (need). Terluna's breathable Moon has to be known through models; every available
   model was built on Earth. Relation: need → the question underneath every lunar result.
2. **Why the Moon tests models hard**: it moves H/R, column mass, gravity and day length together (Table 1).
   Relation: comparison with Earth and with the exoplanet regimes ExoPlaSim was extended for.
3. **The models and why these** — a fast GCM for the global climate (ExoPlaSim), a cloud-resolving model
   that makes its own clouds (CM1) with an electrification scheme grafted in (WRF-ELEC), a spectral wave
   model and a phase-resolving shore model (SWAN, SWASH), and an in-house line-by-line reference.
   Relation: sequence of scales, each model answering what the previous cannot.
4. **Thesis**: five forms of hidden Earth; two classes of repair with different reach. Relation:
   consequence of 2–3; sets up the sections.
5. **Prior adaptations** (literature): Earth models taken to Mars, Titan and exoplanets (planetWRF,
   TitanWRF, ROCKE-3D, LMD Generic, ExoCAM, Isca, THOR, the UM), each changing constants, radiation and
   sometimes the dynamics; what is new here: a breathable atmosphere on a small, slow body, where Earth's
   air sits in a non-Earth geometry, so the hidden Earth is neither the composition nor the gravity alone.
   Relation: tension — earlier ports changed what differed visibly; the Moon's difficulty lies where
   Earth's values hid.

## A breathable Moon as a modelling regime

1. The scenario as the models take it (1.2 atm at the water level, O2 21.2 kPa, 400 ppm CO2, 28% water,
   shield-filtered TSIS-1 sunlight dimmed to 0.970, placeholder land, 50 m slab sea). Relation: conditions.
2. What the scenario does to the governing ratios (Table 1): H ≈ 52 km and H/R ≈ 0.03 (22× Earth);
   7.3× Earth's mass per area; g/g_E = 0.166; 29.53-day solar day, 27.32-day rotation; 1.54° tilt;
   horizon air mass 7.1 (air) and 13.5 (water) against Earth's 35; 0 °C level near 25 km and cloud tops
   55–80 km; 6 km lunar columns resolve convection as 1 km Earth columns do. Relation: mechanism — each
   ratio names the model parts it strains.
3. The questions the models must answer (comfort, rain, cloud, the flight band's winds, storms and
   lightning, seas and shores). Relation: consequence → which model owns which question.

## Where Earth hides in the models (the limitations and the defects)

One paragraph per form, each crossing the models, each separating defect from limitation:

1. **Constants written into code** — CM1's four g = 9.81 (and those left in unused schemes), SWAN's 1 Hz
   AGROW knee and 1.28 kg/m³, PlaSim's horizon factor 35, WRF-ELEC's 180 kV/m cap, −7 °C ground level,
   0.75 s sub-step, SWASH's Earth Ω. Relation: mechanism (dimensional constant → wrong scaling).
2. **Units of time** — Slingo's cover per model day (+0.42 cover); contrast: PlaSim's diffusion and
   friction already in 86,400 s units (ExoPlaSim generalised these). Relation: comparison.
3. **Geometry** — flat, sunlit-only columns; Earth's slant factor; constant g and a thin shell (5% air,
   heights 5–9% low aloft). Relation: mechanism and consequence (twilight, cone, escape).
4. **Fits outside their range** — Lacis–Hansen water, Rayleigh normalisation, Sasamori longwave
   (cooling by height), CCM3 cloud water in metres, liquid-only optics, RRTMG tables to 1,054 hPa,
   Morrison size limits, Wu drag and Komen growth, Saunders–Peck's rime threshold vs slow graupel.
   Relation: the range each was fitted on against the lunar range.
5. **Latent defects** — ExoPlaSim's Sun clock (Figure 2), its orbit default, SWAN's uninitialised KTETA;
   and the project's own defects found on the way (spectrum tail, discharge cadence, uninitialised memory
   in a scaling, ventilation, ledger channel heights, sounding above the GCM top). Relation: tension —
   Earth's own values hid these; the Moon's exposed them.
6. **What the GCM leaves to a slice, and what a slice lacks** — a ring has no sideways transport; a box
   has no day–night circulation; stock CM1 has no lunar Sun, no forcing aloft and no terrain nudging.
   Relation: structural limits of forcing one model from another.

Table 2: the inventory of hidden Earth (model; location; Earth value; lunar consequence; form; defect or
limitation; repaired or open).

## Repairs

1. **Principle: constant to parameter, default as identity** — every ExoPlaSim switch and the CM1 build
   constants; identity tests. Relation: method.
2. **Scaling laws** — fall speeds ∝ g^((b+1)/3) (exact for spheres, approximate for snow), damping and
   PBL length ∝ 1/g, sub-step ∝ layer depth / fall speed, breakdown field ∝ density, AGROW knee ∝ g.
   Relation: derivation from similarity.
3. **Geometry restored** — the curved-air ledger: spherical multiple scattering vs flat columns, cone vs
   curved light, by elevation and layer, with longwave escape (Figure 3: slant factors). Relation:
   mechanism → terms → patches.
4. **Calibration by height against a reference** — the in-house line-by-line model on the GCM's own
   columns; why totals are not enough (the longwave continuum fitted to OLR left cooling by height free);
   gas bands; Figure 4 (absorbed sunlight by layer). Relation: sequence of refinements, each forced by
   the previous one's residual.
5. **Processes added** — ice optics, CO2/O2 in the sunlight, infrared from space, electrical leakage,
   point discharge, the leader's crossing. Relation: what each fills.
6. **Forcing a slice of the GCM** — rings along latitudes and great circles with their own Sun and
   Coriolis, nudging aloft, imposed vertical wind, local-time advection, sideways transport, terrain at
   each column's height; waves forced by the GCM's stress through a Wu-equivalent wind. Relation: method.

Table 3: the repairs (model; change; switch and default; class: general or calibration; state).

## Verification

1. **What each kind of check establishes** (G5): identity, reproduction and provenance, similarity,
   calibration, benchmark; none validates a lunar climate. Relation: distinction.
2. **Identity and provenance** — switches at default byte-identical; the series rebuilds the deployed
   sources and the source of 32 GCM runs. Relation: evidence.
3. **Similarity** — SWAN's sixfold gravity similarity (0.30% vs 5.44% stock), SWASH at 4× gravity;
   CM1's gravity stretch. Relation: test design.
4. **Calibration residuals** — clear air within 0.6 points rms; gas fits ≤0.13% of band; layers
   0.97 W/m² rms; the longwave correction's residual 1–5 W/m² and its drift at 302 K. Relation: what
   holds where.
5. **Benchmarks** — the electrified supercell against CM1's own NSSL and published runs; arithmetic
   checks (Sun elevation 8×10⁻⁷, Coriolis 3×10⁻¹²). Relation: evidence.
6. **Checks still missing** — CM1 forced from the corrected GCM; the longwave refit at the settled
   state; the twilight pair's mixed builds; unconverged scattering orders. Relation: boundary.

Table 4: verification record.

## What the adapted models have given

1. **Each repair's effect on the lunar climate** (Figure 5): cloud water +2.5 K, convective day +1.6 K,
   Sun and tilt +0.6 K, curved air −0.65 K, gas bands −2.2 K, longwave by height with ice +11.5 K; and
   the cloud scheme's settings 289–297 K. Relation: comparison → the climate is most sensitive where the
   models stay Earth's (clouds; longwave by height).
2. **The gap between CM1 and the GCM, decomposed** (Figure 6): sideways transport a third; PlaSim's
   longwave about 1.5 K; the rest in how heat leaves the ground. Relation: sequence of eliminations.
3. **Lunar storms and their lightning**: 85% of falling water evaporates; flashes a hundredth of Earth's
   density, ten times the charge per strike, 20% to ground. Relation: consequence of gravity's scaling.
4. **Lunar seas**: wave climate and run-up, forced by the GCM's stress (from the wave notes). Relation:
   consequence.
5. **What stays conditional**: the 307 K state; comfort as a range between models. Relation: boundary.

## Worlds within reach

1. **Two classes, two reaches**: general repairs transfer; calibrations refit. Relation: distinction.
2. **The regime map** (Figure 1, computed): worlds by H/R and column mass, and by solar day and gravity;
   found worlds (Earth, Mars, Titan, Venus, the ancient Moon's transient atmosphere, slowly rotating
   exoplanets) and crafted ones (the Open Moon at 1.0–1.2 atm and other dimmings, a breathable Mars);
   lines where each Earth assumption breaks. Relation: calculation of conditions.
3. **Table 5**: by world property, stock against adapted, for each model. Relation: catalogue (intended).
4. **Limits of reach**: compositions PlaSim and RRTMG cannot carry; multi-bar surfaces beyond RRTMG's
   tables; H/R beyond a few per cent (deep atmosphere); empirical source terms at ε far from Earth's.
   Relation: boundary.

## Next work

Ordered by how much of the remaining uncertainty each removes: the longwave at the settled state; cloud
amount and water constrained by CRM runs; deep-atmosphere dynamics; RRTMG's range and spectrum; drop
size limits with gravity; two-way GCM–CRM coupling; an independent GCM; electrification at lunar impact
speeds; waves with the air's density field and swell decay; upstream reports. Each item: the question it
discriminates, alternatives, measured outputs, the result that would change the design (G5).

## Conclusions

Gather into one relation: the Moon could only be modelled once Earth was found inside the models; the
repairs that removed it are general; the calibrations tie the lunar climate to one column and one
cloud scheme; the next work is where that tie is weakest. No section replay.

## Back matter

Code and data availability (world-crafting repository; Terluna at 186b294; upstream pins; research-drive
outputs as available); author contributions; competing interests; AI-assistance disclosure (charter);
review history; acknowledgements; references.

## Figures and tables

| Item | Content | Data | Script |
|---|---|---|---|
| Table 1 | Governing ratios, Earth and the Open Moon | `shared/constants.json`; computed | `figures/regime.py` |
| Figure 1 | Regime map: H/R vs column mass; solar day vs gravity; worlds; assumption lines | computed from stated parameters | `figures/regime.py` |
| Figure 2 | The Sun clock: equatorial sunlight by longitude, upstream vs synodic | `python/climate/results/gcm/sun_check_*.json` | `figures/sun_clock.py` |
| Figure 3 | Slant-path factor vs solar elevation: flat, PlaSim's Earth formula, Moon water and air | `twilight.json` `column.slant` | `figures/slant.py` |
| Figure 4 | Absorbed sunlight by GCM layer: line-by-line, PlaSim as run, with the bands | Terluna `climate/gcm/README.md` 1088–1100 | `figures/layers.py` |
| Figure 5 | Each repair's effect on the global-mean surface temperature | run pairs' `progress.json` and the README tables | `figures/repairs.py` |
| Figure 6 | CM1 vs GCM at 45° N by layer: control, sideways, GCM | `heat_budget_ring_45n_corrected*.json` | `figures/gap.py` |
| Table 2–5 | Inventory, repairs, verification, reach | notes/, models/ | LaTeX |

## Claims register

`paper/claims.json` holds each number in the text with its source (Terluna file and line at 186b294, a
results file, a run's `progress.json`, or a calculation here) and its evidence state. The build checks that
every claim the sections cite exists in the register and that its source path exists.
