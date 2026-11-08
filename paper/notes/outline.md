# Outline, second draft

Historical outline. The current terminology and ensemble framing follow the author's 18 October 2026
review, recorded in `../review/terracompatible_revision_2026-10-18.md`; the manuscript is the current text.

Stage 3 redone on 2026-10-17 after the author's reading of the first draft. The first draft's outline is in
the Git history (commit 6c8a68f). Headings are unnumbered and few; each paragraph below names its governing
relation (charter G1). The writing rules are in the repository's `AGENTS.md`.

**Title.** Modelling Earth-like worlds beyond Earth's range: ExoPlaSim, CM1, SWAN and SWASH adapted and
tested on a breathable Moon.

**Subject.** Earth-like worlds beyond Earth's range: exoplanets and constructed worlds whose air and water
are close to Earth's while their gravity, size, day or starlight differ. They are studied with models built
and tuned for Earth, in which Earth's values remain as constants, units of time, geometry, empirical fits
and latent defects. On such worlds those values run without failing, because the air and water stay inside
the regime the models were built for, so their errors go unseen.

**Through-line.** Each port of an Earth model to another world has repaired the Earth values its own world
exposed; locating them in general, and knowing which repairs hold from world to world, remains open. The
work so far was done on one world, a breathable Moon, which moves gravity, column mass, scale height over
radius and the solar day together while keeping Earth-like air, so adapting four models to it made each
Earth value's error large enough to find and measure. The repairs split into general repairs, which apply
on other worlds as they stand, and calibrations, which hold near one column. Checks of different kinds
establish different things. On the case, the Earth fits left in cloud and in the longwave cooling by height
move the climate most. The general repairs open a definable set of other worlds, bounded by composition,
surface pressure, scale height and the empirical laws.

**Departures from the first draft.** The paper stands alone; the project that designed the case is cited
once as its source and again in the availability statement, and the ensemble Paper ID is gone. The
introduction opens on the field's need and its literature. The world-regime figure moves from the reach
section to the second section, which places found and constructed worlds before introducing the case. The
"one rule" of the repairs becomes the main rule, with the other kinds beside it. Coined terms ("hidden
Earth", "Earth inside the models") give way to "Earth values" and "Earth assumptions". The results section
loses its closing summary of conditions, which now sit with each claim. The technical content, the claims
register and the figures carry over, with the referees' corrections.

## Abstract (about 250 words)

Promise the subject and its difficulty; develop the case, the five forms with the defects named, the two
classes of repair, the checks and what they establish, the measured effects on the case; land on the reach
and its limits, the portable result.

## Introduction

1. **The need.** Exoplanet and constructed-world studies ask about Earth-like worlds beyond Earth's range
   (slow rotators, other gravities and sizes, other stars; terraformed planets and moons). Their GCMs,
   cloud-resolving and wave models descend from Earth models. Relation: question → the tools that answer it.
2. **The problem.** Ports to other worlds have each found values fixed for Earth in the code (PlanetWRF,
   TitanWRF, ROCKE-3D 1.0 and 2.0, THOR 2.0, ExoPlaSim's own description) and repaired what their world
   required. On an Earth-like world a remaining Earth value runs without failing and returns a plausible
   number. Relation: tension → the open question: locating Earth values, and which repairs hold elsewhere.
3. **The case.** A breathable Moon from an open design project: Earth-like air under a sixth of Earth's
   gravity, a 29.5-day solar day, 7.25 times Earth's air per square metre, a scale height 23 times Earth's
   in proportion to the radius. Relation: mechanism — four ratios move together, so each Earth value's error
   grows large enough to measure.
4. **The models.** ExoPlaSim for the global climate, CM1 with WRF-ELEC's electrification on GCM-forced
   slices, SWAN and SWASH for seas and shores, an in-house line-by-line reference for the radiation.
   Relation: sequence of scales joined by forcing.
5. **What the adaptation found and built.** Five forms of Earth value, with defects separated from
   limitations; two classes of repair with different reach; records of patches against pinned sources; the
   evidence state of the lunar results, stated once. Relation: consequence.

## Worlds beyond Earth's range

1. **The ratios.** Scale height over radius, column mass, gravity, solar day and rotation, composition and
   starlight, each with the model parts whose Earth values depend on it. Figure 1 places found and
   constructed worlds against them. Relation: mechanism, then comparison.
2. **The case's scenario** as the models take it: pressure and composition, seas and lakes, filtered
   sunlight, placeholder land, slab sea. Relation: the conditions every lunar number holds under.
3. **Geometry and column on the case** (Table 1): column 7.25 times Earth's, water vapour paths, mass-mean
   height, shell area, straight-ray horizon air masses against PlaSim's 35, the fall of gravity with height.
   Relation: mechanism.
4. **Gravity and calendar on the case**: pressure heights, fall speeds, sea roughness, wave speed, the
   dry-dynamics stretch and its limits, soil wave, per-day formulas, Coriolis, tilt. Relation: mechanism →
   the parts each model must change.

## Earth assumptions in the released models

0. **Two kinds.** A limitation is correct on its own terms for Earth; a defect is wrong on any world.
   Table 2 lists both on the paths the lunar runs use. Relation: classification.
1. **Constants written into the code** (CM1, NSSL, WRF-ELEC's thresholds and sub-step, SWAN's knee and air
   density, RRTMG's gases, CM1's beta plane). Relation: a dimensional constant fixes its world's scale.
2. **Units of time** (Slingo's cover per model day; ExoPlaSim's calendar; CM1's Sun and soil; WRF-ELEC's
   missing clear-air conduction). Relation: a formula counted per day takes its world's day.
3. **Geometry** (flat sunlit-only columns and the curved air's energy terms; PlaSim's horizon factor; thin
   shell and constant gravity). Relation: mechanism and size.
4. **Fits and simplifications beyond their range** (PlaSim's shortwave and longwave fits, cloud water,
   cloud phase and saturation; RRTMG's tables and ice optics; Morrison's drop limits; the laws of sea and
   charge). Relation: each fit's range against the lunar range.
5. **Defects in the released codes** (Sun clock, orbit default, SWAN's breaker parameter; CM1's thread race
   and PlaSim's lowest level, with their tie to Earth unknown). Relation: tension — exact or invisible at
   Earth's parameters.
6. **Defects of the adaptation**, found by its own checks. Relation: sequence of discovery.
7. **What a slice of the GCM lacks.** Relation: structural limit → the forcing methods.

## Repairs

0. **The main rule and the other kinds**: switchable parameters defaulting to the released code, the
   exceptions, and the class set by where a lunar value comes from. Relation: method → classification.
1. Constants to parameters. 2. Scaling laws. 3. Geometry restored. 4. Calibration by height, each step forced
   by the last one's residual. 5. Processes added. 6. Forcing a slice of the GCM. Relation: method by method,
   in the order the inventory raised them. Table 3.

## Verification

0. What each kind of check establishes: code, consistency of gravity, agreement with the reference,
   published behaviour on Earth; the lunar climate itself is unobserved. 1. Identity and reproduction.
2. Similarity. 3. Calibration. 4. Benchmarks and arithmetic. 5. Checks that fell short. 6. Checks still
   missing. Table 4.

## Results for the breathable Moon

1. Each repair's effect on the global-mean temperature (Figure 5) and the sensitivity tests: the climate
   moves most where cloud and the longwave by height keep Earth's fits. 2. The near-ground gap between CM1
   and the GCM, taken apart (Figure 6), and the rain gap. 3. Storms and lightning; the two choices that a
   measurement or theory could settle. 4. Seas. Conditions attach to each claim.

## Reach to other worlds

1. The two classes reach differently; what another world needs and the tools that come with the repairs.
2. Where each Earth assumption breaks, world by world (Figure 1 again; Table 5). 3. Within reach as adapted;
   with a new column; beyond reach; the four limits.

## Next work

Ordered by how far each step moves the case's climate: the longwave at the settled state; cloud from the
cloud-resolving model; the tall air's dynamics; radiation in CM1; microphysics at lunar gravity; electricity
and seas; upstream reports and the record. Each step names the question, the comparison and the result that
would change the design (G5).

## Conclusions

Gather the lines into one relation: on Earth-like worlds Earth values fail without a trace; a world that
moves several ratios at once made them measurable; the general repairs and the inventory carry to other
worlds, the calibrations and the ledger are remade with the reference tools; the case's climate depends
most on the Earth fits that remain in cloud and longwave cooling.

## Back matter

Code and data availability (world-crafting repository; Terluna at 186b294 as the source of the case and
the runs; upstream pins and licences); author and assistance; competing interests (none: an unfunded
personal project, public where licences allow); review history (first draft, two referees, the author's
reading, the editorial rounds); acknowledgements.

## Figures and tables

| Item | Content | Data | Script |
|---|---|---|---|
| Figure 1 | Found and constructed worlds: H/R against column mass; solar day against gravity | `data/worlds.json` | `figures/figures.py` |
| Table 1 | The ratios, Earth against the case, and the model parts each strains | `data/regime_calc.json` | LaTeX |
| Figure 2 | The Sun clock: equatorial sunlight by longitude, upstream and synodic | `data/sun_clock.json` | `figures/figures.py` |
| Table 2 | Earth assumptions on the lunar paths | notes, defect log | LaTeX |
| Figure 3 | Slant path against solar elevation | `data/slant.json` | `figures/figures.py` |
| Figure 4 | Absorbed sunlight by GCM layer | `data/layers.json` | `figures/figures.py` |
| Table 3 | The repairs, switches, settings and classes | `models/` READMEs | LaTeX |
| Table 4 | The verification record | `notes/verification_record.md` | LaTeX |
| Figure 5 | Each repair's effect on the global-mean surface temperature | `data/repairs.json` | `figures/figures.py` |
| Figure 6 | CM1 and the GCM at 45° N by layer | `data/gap45n.json` | `figures/figures.py` |
| Table 5 | Reach by world property | notes | LaTeX |
