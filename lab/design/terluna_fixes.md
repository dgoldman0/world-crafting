# Terluna's fixes in the lab: generality, world types and cost

An analysis of 8 November 2026, by reading and arithmetic, of the fixes `PLAN.md` lists for porting, from the lab's
design documents, `notes/cm1.md`, Terluna's modules at `bdda5a07` and PlaSim's `radmod.f90`; nothing was run.
`PLAN.md` ("Porting: confidence, form and cost") holds the decisions taken from it. R:n is the row at line n of
Terluna's `research/decisions.md` at `bdda5a07`.

Tags: [code] code or its documentation; [run] a Terluna run as recorded; [off] Terluna's offline calculation; [der]
arithmetic here; [int] interpretation; [prop] proposal. Worlds: E Earth control, M Open Moon, Ma Mars with Earth-like
air, W low-gravity waterworlds in Gaean air (g 1.21–2.49 m/s², all ocean), S steam worlds. For every row: the
registry refuses ExoPlaSim and CM1 on S; every "Tested" entry is M's, no E, Ma or W run having used these fixes (Ma
waits for pinned heights); on E each patch at its identity default is the released model byte for byte, and a fix
switched on must keep the Earth control within 2σ of the released run's yearly means.

## Cost against the released models

Per model step, every item except the level set costs nothing or an O(levels) column
calculation [code, int]. PlaSim's dynamical work grows with the level count N and its longwave scheme loops over pairs
of levels (`lwr`, lines 2306–2418) [code], so fifteen levels cost ×1.5–2.25 of ten [der]. Terluna's standard
configuration took 8.7 minutes a model year (R:804) against October's 218–278 s: **×1.9–2.5**, unattributed among the
changes [run].

Per study, one item costs nearly an order of magnitude more and two could. Weather-carrying boxes run 7–14 lunar days where earlier
boxes ran two, **×3.5–7 a box**, since Terluna judges them by paired daily differences against two standard errors
(R:657) [run]. Terluna sampled a higher dilution on a finer CM1 grid in one pair (R:703) [run], and columns of 3 or
2 km in place of 6 would cost ×8 or ×27 [der]. Complexity grows through calibration runs on other models, repeated
for each world type: CM1 boxes for rain's birth sizes, McSnow for snow's references [code].

## One component or several

All five are proposals [prop].

- **One component for every world:** its Earth limit is the released behaviour or physics Earth obeys, its remaining
  constants are dimensionless or derived, and the Earth control passes with it on.
- **Branches in one component:** shared physics branching on a specified field: surface type, rotation state, level
  set.
- **Settings by world type:** validity crossing a regime boundary: an absolute-pressure threshold, CM1 damping below
  the GCM's convection top.
- **Calibrations:** Moon-fitted values, separated by the envelope check.
- **Cost:** a component above ×2 gets a selector only where a cheaper form serves a class of worlds, as Earth's ten
  levels where H lies near Earth's. The level set's cost grows as ln(H/z₁), z₁ the lowest level's height; the weather
  protocol's as (daily spread/tolerance)² [der].

## Take now

| Fix | General form | Holds: physics; tested | One or several; selector | Cost | Recommendation |
|---|---|---|---|---|---|
| 1. CM1 radiation at constant volume | cv/cp, with vapour cvm/cp: composition only [code] | Every `eqtset = 2` run. Tested: within 0.013 K/day of correlated-k (V08) [run] | One reader rule keyed on `eqtset` | ×1 | General |
| 2. `ipbl = 2` density | Coding defect: tendencies multiplied by the air's density, +20% on E, +40% on M, −40% at 0.5 bar [code, der] | Every `ipbl = 2` run. Tested: box budgets [run] | One patch, on by default; A9 requires it | ×1 | General |
| 3. CM1 gust over water | w* = (g h B/θv)^⅓, β 1, least wind 0.1 m/s: g, boundary-layer depth h, buoyancy flux B [code] | Physics: convective surface layers; stable nights take none. Tested: sea-box wind ×1.1–1.2, MM5's ×1.6–1.8 [run]; E's output moves [int] | One; gravity from the build until the namelist patch | ×1 | General with limits |
| 4. PlaSim gust; similarity over ice-free water | g in w*, Ri_b and Charnock's 0.0185 u*²/g; the nonlocal scheme's depth rule; Earth air's ν = 1.5×10⁻⁵ m²/s and a 2.85 mm roughness cap [code]; M's ν ≈ 1.3×10⁻⁵ [der] | Physics: similarity needs z₁ in the surface layer (0.3 km on l15; row 9) [der]. Tested: +17% sea evaporation, +5% rain in a lunar day [run] | One; surface type selects; ν derived; warn where z₁ exceeds 0.1 h [prop]; ports with the nonlocal scheme's depth code [code] | ×1 plus O(N) a column | General with limits |
| 5. Raindrop limits | (9.81/g)^½ on breakup and the D_m cap (capillary length); (g/9.81)^¼ on the fall cap; (ρ/ρ_E)^α, α 0.69–0.71, computed for g from M's to E's [code] | Physics: Weber similarity of water drops in N2–O2 air; Low and List's fit read beyond its 0.4–4.6 mm [code]. W's 1.21–1.62 m/s² lies just below the computed range [der] | One; B28 requires it off 9.81; warn below 1.62 m/s² [prop] | ×1 | General with limits |
| 6. Whole-column forcing | GCM heating and moistening (codes 21, 40); convection top, the lowest level above which under 1% of convective rain forms; CM1's damping from 0.77 of its top [code] | Physics: convection top below CM1's damping. Tested: 73 km against 115 km [run, code]. E's damping under rule 9 starts at 18.6 km [der], close above a 16–17 km tropical tropopause [int] | One; refuse a case whose damping starts below the convection top plus one GCM layer [prop] | CM1 ×1; forcing runs ≤×1.3 for the diagnostics [run]; a top raised from 2.9 to 4 H, ×1.3 [der] | General with limits |
| 7. Reorientation | Base moments (measured or hydrostatic); loads' degree-2 form with self-gravity and elastic response; frame rule (C along the spin; if locked, A toward the host, planet or star); Cassini obliquity; a viscoelastic interior (long-term); the code holds the Moon's constants [code] | Physics: loads small beside the figure. Tested: 8.05° [off]. E must show no turn [prop]; W's loads lie nearly even; an illustrative world's assumed figure decides its turn [int] | One tool, branched by rotation state, moment source and response; warn past 0.6°, refuse past 2.8° on T21 (PLAN, proposed) | Offline minutes; M's turn cost about three 20-year runs and a refit [run]: ×1.3–2 on a land world's GCM stage, ×1 all ocean [int] | General with limits (elastic); assess the viscoelastic branch first |
| 8. Rain from drop sizes | Per world: fall-law table at g, ρ, μ; self-collection rate (M's 2.919 m³/kg/s); breakup by (9.81/g)^½ (p_s/1013 hPa)^0.687. Moon calibrations: new rain 0.439 mm (CM1), melted rain 2.95 mm (McSnow), a W/(W+F) share set by layer thickness [code] | Tested: 0.96–1.05 of CM1's column evaporation on three boxes [run] | One scheme; tables per world; birth sizes a calibration whose envelope holds g, p_s and level set, γ outside it [prop] | GCM: midpoint steps of ≤1 km [code]; calibration: CM1 boxes of 2.3–27.2 h each [run] | General; birth sizes the Moon's calibration |
| 9. Fifteen σ levels | σ set for M's 51 km scale height, z₁ 0.30 km [code]; generally, a set from H and boundary-layer depth (plan.md) | On E the same σ put z₁ near 50 m [der]; W (H 33–68 km) lies near M, Ma (22 km) between | One generator, a set per world, calibrations keyed by set; warn where z₁ exceeds ~0.3 km: ten levels give 0.15 km on E, 0.39 on Ma, 0.6–1.2 on W, 0.9 on M [der, prop] | **×1.5–2.25** [code, der] | World-type switches: sets per world |
| 10. Clear-share twilight | Ledger geometry (H/R, horizon factor); cloud cover above each layer [code] | Physics: needed where the horizon factor leaves 31.5–38.5 (B13): M 7.2, W 7.3–13.8, Ma ~15.5 [der]; locked terminators untested. Tested: ~1 K cooler (R:505) [run] | One; a ledger per world and reference temperature | GCM ×1; ledger about 50 min on 6 threads [run] | General with limits |
| 11. 10 m wind | Geleyn's profile from PlaSim's drag; faithful with z₁ in the surface layer [int] | Every world; a diagnostic | One | ×1 | General |

## Waiting

| Fix | General form | Holds | One or several | Cost | Recommendation |
|---|---|---|---|---|---|
| 12. Simplified Betts–Miller | Reference humidity 0.7 [int]; 2 h relaxation (`tau_bm` 7,200 s) [code]; a depth test in absolute pressure (`dpdeep_bm`): 200 hPa is 16% of M's 1,216 hPa, 20% of E's, 40% at 0.5 bar [der] | Tested: design runs; no closure has passed [run] | Setting `nprc`, Kuo the default; depth as Δσ ≈ 0.2 [prop] | ×1 [int] | Assess first |
| 13. Inflow, weather, damped gravity wave | Mean-wind convergence; 5.5-hour GCM means; the first baroclinic mode's speed (40.5 m/s on M) and footprint, lid at the convection top [run, code] | A locked W lacks the lunar-day cycle they follow [int] | Case variants | Per step ×1. **Weather ×3.5–7 a box:** a transition and six read lunar days, six more if unresolved; the sea box ran 14 [run]. Damped wave ×2 [run] | Assess first |
| 14. Cold-cloud factors; longwave `l15_turned` | Fitted on M's turned design states, level set and orientation [run] | Within their envelope | The Moon's; stage 5's fitting tools general | A refit, one 20-year pass, about 3 h [der] | Keep as the Moon's calibration |
| 15. Snow from capped flakes | Lunar McSnow references by height above the freezing level, a 14 cm cap, CM1's graupel shares, a fraction pooled from two boxes [code] | Tested: design boxes; box-mean air overstates sublimation 1.19 times [code] | The Moon's if adopted; γ elsewhere | GCM: five quadrature rates a snowing column, shadows when on [code]; McSnow per world, unmeasured | Assess first |

## Cross-cutting

1. **The Earth control as the gate.** Items 3, 4, 8 and 9 change Earth's released physics. If one moves E beyond the
   2σ test, it becomes a switch off Earth or the control changes what it measures; that choice decides "one component
   for every world" [int].
2. **Levels against scale height.** Keeping z₁ in the surface layer adds a few levels across the Gaean range, while
   cost grows as N to N²: 20 levels ×2–4 and 30 levels ×3–9 against ten [der]. Each set refits the longwave
   (6.4–8.8 W/m² by layer left on other levels), the cold cloud and the rain share [code].
3. **CM1's domain against gravity.** Rule 9 scales lengths with H, so a deeper low-gravity column adds no points and
   the step lengthens as 1/g. At equal temperature, per simulated second, a box costs ∝ g (W 0.75–1.5, Ma 2.3, E 6
   times M's) and a ring ∝ R g² (W 0.7–5.4, Ma 10, E 130) [der]; the solar day multiplies both. This rule-9 growth
   exceeds any fix's. Domain height follows the convection top: 1.05–1.53 H on M, near 1.9 H on E [run, int].
4. **Orientation in the lakes fixpoint.** A pass whose lakes move re-derives the orientation, which the longwave
   envelope includes, so a settled turn costs a refit and a target pass: one or two extra passes on land worlds, none
   on all-ocean anchors [int].
5. **Storage for weather.** 5.5-hour means hold 13 times the 3-day means' records; Terluna split the year's
   conversion after it held 11.6 GB [run]. A box of the Jura box's size, 54 GB per two lunar days, would write about
   380 GB over 14 [der].
