# Dispositions of the whole-manuscript challenge

The challenge (`whole_manuscript.md`) read the first draft at commit d090154. Its findings were acted on in
the second draft (commit e018be0, with the scoping rule of 4d03a81), written at the same time as the reframing
the author asked for. Locations below are those of the second draft's files. "Accepted" means the repair was
made as proposed or in an equivalent form; "in part" says what was left and why.

## Blocking

| Finding | Disposition | Where |
|---|---|---|
| B1 Framing; the eight rejected passages; Paper ID; "Open Moon"; empty actions; "hidden Earth" | Accepted. New title on the field's subject; Paper ID removed from the title page and the source; the breathable Moon named as the worked case and Terluna cited once as its source, again in the availability statement; every rejected passage rewritten; coined terms replaced by "Earth values"; the fresh-reader round started (`editorial_round1_*.md`) | `main.tex`; `introduction.tex`; `worlds.tex`; all sections |
| B2 Repair classes disagree | Accepted. One taxonomy: general repairs (a unit, a scaling or physical law, a defect removed), a general method with a per-world table (the curved air), calibrations (coefficients tuned to the reference), and the other kinds defined once; the criterion between table and fit stated. The Sun clock described as patch 04; the fixed orbit and whole model days as configuration with class general; the soil classed general for days from a few Earth days to the Moon's; leakage and the forcing methods moved out of the general list in Reach; the beta-plane rows named apart (Earth's β bypassed; patch 16's Coriolis on departures a capability unused on the Moon); one class list in every caption | `repairs.tex` paragraphs 1–2; `reach.tex` paragraph 1; Table 2 and the appendix switch table |
| B3 Defect against limitation | Accepted. Kind made an axis separate from four forms; the definition restated as code that contradicts its own inputs, units or intent, a defect even where Earth's values hide its error; Table 2 gains a Kind column. The convective-cover conversion decided as a defect, since ExoPlaSim's description says it replaced the solar day with 86,400 s in its unit conversions and left this one; its bias in synchronous runs computed (claim W06) and a report added to next work. The thread race (a defect with no Earth form) and the cold lowest level (cause uncertain) given their own sentences | `assumptions.tex` paragraphs 1 and 7; Table 2; `regime_calc.py`; `next.tex` last paragraph |
| B4 The reference's own checks | Accepted. Verification states the reference's two cross-code checks and their scope and names what no independent code has checked (claim V16); the full-column cross-check is the first of the checks still to make, a row of the appendix verification table and a next-work step with its deciding result; "given the reference's spectroscopy" attached to the ranking of uncertainties | `verification.tex` paragraphs 4 and 8; `next.tex` paragraph 4; `results.tex` paragraph 4 |
| B5 Next work short of its own claim | Accepted. Every step names its question, comparison and the result that would change the design or the reach; the independent GCM, RRTMG, microphysics, charging, leader model and seas steps gain their clauses; record work moved to a closing paragraph; the order claimed only for the first two steps, with the third testing the reference. Where the record gives no threshold, the deciding result is stated as an outcome (most of the 4.5 W m⁻² removed, or little); numerical thresholds for those steps remain the author's to set | `next.tex` |

## Major

| Finding | Disposition | Where |
|---|---|---|
| M1 The dimming as a tuning target | Accepted: stated where the scenario is set | `worlds.tex` paragraph 2 |
| M2 Configurations; the GCM's σ grid | Accepted: configuration table in the appendix; the σ grid added to the inventory (claim H33) and cited where the gap is attributed | The appendix configuration table; `assumptions.tex` geometry paragraph; `results.tex` gap paragraph |
| M3 GCM states and run conditions | Accepted: a table of states with one name each; the Sun-and-tilt baseline corrected to the pre-correction run; each CM1 result's forcing named, with the pre-correction run's 12% shortfall at 0° E; the rings' starting-sounding ice noted as an unquantified term at the gap | Table 3; `results.tex` |
| M4 Model outputs among the scenario's ratios | Accepted: CM1 results marked in Table 1; the vapour columns attributed to the design case's GCM | `worlds.tex` |
| M5 "Farther than any repair" | Accepted: the first calibration's effect reported (claim G14); the comparison restricted to the general repairs; carried into the conclusions | `results.tex`; `conclusions.tex` |
| M6 The arc | Accepted: the introduction promises the measurement on the case and the reach; the abstract and conclusions carry the change in rain and dry land and the storms and seas; the conclusions land on the relation between what travels and what moved the Moon most, and name the correlated-k scheme as the step that loosens the tie to one column | `introduction.tex` last paragraph; `abstract.tex`; `conclusions.tex` |
| M7 The chain after Results | Accepted: the worlds figure moved to the second section; Reach opens from the results; a test of reach added to next work with its criterion for reclassifying a repair | `worlds.tex`; `reach.tex`; `next.tex` |
| M8 Reach under-developed | Accepted: the split between found and constructed worlds stated; synchronous rotators; the three defects' reach into other users' runs; moons of giant planets; reach model by model; the bound on other dimmings | `reach.tex` |
| M9 How the defects were repaired | Accepted: a paragraph on defects removed or avoided | `repairs.tex` paragraph 3 |
| M10 Internal names | Accepted: run names moved to the states table; the sky solver's grid glossed; the ledger defined before its first use; the twilight pair defined, with its result; installation, patch names and PlaSim's solar-position routine named; the equatorial crossing and the 45° rings defined; rings and boxes glossed at first use; "found and constructed worlds"; Earth's top levels replaced by the σ-grid row; the unselected SWAN and SWASH options explained; the switch table moved to the appendix | throughout |
| M11 Duplication and balance | In part. Done: the switch table and the verification record moved to the appendix; Verification's prose trimmed; the adaptation's defects moved into Verification and the slice's limits into the forcing paragraph; conditionality stated once in the introduction and attached to each claim. Kept: the worlds section stands as its own section, since the field framing makes it the paper's map of worlds; Table 2 and the appendix switch table stay separate, the inventory now carrying the repair class and the switch table serving as the reproducibility record | `appendix.tex`; `verification.tex`; `repairs.tex` |

## Minor

| Finding | Disposition |
|---|---|
| 1 Figure against text | Accepted: window and settled values both in the text |
| 2 One term for the transport | Accepted: "transport across the circle", also in Figure 6's legend |
| 3 The forms' names | Accepted: four forms named once and used throughout |
| 4 Cloud water's form | Accepted: moved to the constants paragraph |
| 5 The high cloud's temperatures | Accepted: each range named by what it describes |
| 6 The 11.5% column | Accepted: one baseline, $p_s/g_s$ |
| 7 The gravity pair's purpose | Accepted: one purpose, the departure from Earth's convection stretched sixfold |
| 8 The count of kinds of check | Accepted: six, with arithmetic |
| 9 An estimate stated as an attribution | Accepted: "estimated at about 1.5 K", with its basis |
| 10 One box against Earth's mean | Accepted: the box's flash density |
| 11 Rain and the slice's direction | Accepted: claim G15 |
| 12 Identity by construction | Accepted: the patches without a runtime identity run named |
| 13 One hedge on reach | Pending: the second draft's abstract states the general repairs serve other worlds unchanged; to be hedged with the round-1 revisions |
| 14 The 11.5 K in the abstract | Accepted: stated as a run outside the correction's fitted state |
| 15 Claims for table numbers | In part: the availability statement restricted to numbers in the prose |
| 16 The cold lowest level's next step | Accepted: a test against smoothed terrain |
| 17 The GCM's top | Accepted: "the GCM's top level, near 130 km" |
| 18 "Exact" for approximations | Accepted: "right" in Reach and in Figure 1 |
| 19 Table-only items | Accepted: explained in the constants paragraph |
| 20 SWASH in the title | Kept: the title the author approved says "adapted and tested"; SWASH is configured for lunar gravity and tested for similarity |
| 21 Abstract length | In part: about 315 words cut to about 263 |
