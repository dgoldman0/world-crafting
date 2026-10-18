# Editorial round 1: dispositions

**Round.** Five fresh reviewer agents read the second draft (sections at commit 4d03a81; the records give each
file's hash): four by part (`editorial_round1_opening.md`, `_inventory.md`, `_results.md`, `_closing.md`) and one
across the whole paper (`_whole.md`). They raised 172 findings, 20 of them blocking: opening 40 (3 blocking, 17
major, 20 minor), inventory 38 (4, 15, 19), results 35 (5, 18, 12), closing 33 (5, 19, 9), whole 26 (3, 16, 7).

**Revision.** While the round ran, the author read the second draft and directed a reframing: the paper is a field
paper on Earth-like natural and constructed worlds, with the Moon as the test world; constructed worlds and their
wider freedom of parameters are set up early; "Many exoplanet climate studies" opens the paper. Claude Opus 5.5,
the drafting assistant, wrote the third draft (commit c63df43) from the five records and that direction together.
The author then read the third draft and rejected its conclusions as a summary that implied reach to untested
worlds; the conclusions were rewritten as discussion and conclusions (commit bb5d0f0) and sent to a second round.
Rows below that concern the conclusions refer to the third draft's version unless they say otherwise.

**Terms.** Accepted: the change was made as proposed or in an equivalent form. Adapted: the finding was met by a
different change, stated. In part: what remains, and why. Open: left for a later round or for the author, with the
reason. Moot: the passage went in the rewrite. Locations are the third draft's.

## Opening (abstract, introduction, worlds)

| # | Sev. | Disposition |
|---|---|---|
| 1 | MINOR | Accepted: `\date{17 October 2026}` (main.tex) |
| 2 | BLOCKING | Accepted: "Many of the general circulation models used for exoplanets were developed for Earth or for solar-system planets", with the run that completes with a plausible result as the agent |
| 3 | MAJOR | Accepted: the Moon "departs from Earth at once in gravity, column mass, day and scale height in proportion to its radius" |
| 4 | MINOR | Adapted: the abstract names the fourth form as fits and simplifications beyond their range; the introduction states the forms after defining Earth value and defect |
| 5 | MAJOR | Adapted: the abstract states the three defects' consequence, a bias in ExoPlaSim's runs of slowly rotating and tidally locked planets by the code's own arithmetic; their operations are named in the assumptions section, which the abstract no longer anticipates with project names |
| 6 | MAJOR | Adapted: the abstract states the relation of form to class (constants and units of time, general repairs; geometry, a method; the radiation's fits, calibrations), with "built to hold" as the evidence state |
| 7 | MINOR | In part: "identity, reproduction, arithmetic and gravity-similarity checks and Earth benchmarks", with the calibrations against the line-by-line model; the labels stay, defined in Verification |
| 8 | MAJOR | Adapted: the abstract reports the sensitivities with their conditions (single general repairs 1.6–2.5 K; calibrating the radiation's fits more than 20 K; cloud settings varied in tests, up to about 6 K) and leaves the storm results to the body |
| 9 | MAJOR | Accepted: the landing names what each route changes, the radiation from line-by-line spectroscopy and cloud from cloud-resolving runs as a calibration for each world |
| 10 | MINOR | Accepted, with the author's "Many" |
| 11 | MAJOR | Accepted: McKay et al. asked how Mars could be made habitable; Terluna cited once as the source of the case |
| 12 | MAJOR | Accepted as proposed |
| 13 | MINOR | Accepted |
| 14 | MAJOR | Accepted: the step credited to PlanetWRF's developers, TitanWRF built on the result |
| 15 | MINOR | Accepted |
| 16 | BLOCKING | Accepted |
| 17 | MAJOR | Accepted |
| 18 | MINOR | Accepted: "Both questions are taken up here on a test world, the breathable Moon"; the project named in the constructed-worlds paragraph |
| 19 | MINOR | Accepted |
| 20 | MINOR | Adapted: "A run of a natural planet that departs from Earth along one of these ratios ... meets the Earth values that depend on that ratio alone; on the test world the values of all four err together" |
| 21 | MINOR | Accepted (a–c); (d) adapted: the appendix pointer moved into the paragraph's first sentence, which now ends on the radiation and its reference |
| 22 | MINOR | Accepted |
| 23 | BLOCKING | Accepted, then extended: the general class now names a parameterization fitted over a wider range and "no coefficient fitted to the test world", as in Repairs |
| 24 | MAJOR | Adapted: the introduction ends on the class following the form, the fits' effect on the test world and the evidence state; the inter-model test is reported in Results and the closing section |
| 25 | MAJOR | Accepted: the sentence deleted |
| 26 | MAJOR | Adapted: the grouping sentence as proposed, opening on "many" of the models' Earth values; the count of inventory rows by ratio is left out |
| 27 | MINOR | Accepted: natural and constructed worlds |
| 28 | MAJOR | Accepted |
| 29 | MINOR | Accepted: caption order, "Earth values", annotations "holds here" and "formulas hold", present Mars filled in the right panel |
| 30 | MINOR | Accepted |
| 31 | MINOR | Adapted: hPa in text and Table 1; the 1.02–1.22 atm range stated across the GCM's cells, its maximum's cause unstated |
| 32 | MINOR | Accepted |
| 33 | MINOR | Accepted; Table 1's CM1 rows removed |
| 34 | MAJOR | Accepted |
| 35 | MINOR | Accepted: 5.7% at 48.6 km in the column on which the curved geometry was computed (claim S09 corrected; regime_calc's shell ratio) |
| 36 | MINOR | Accepted |
| 37 | MAJOR | Accepted, with the dependence on gravity that Loftus and Wordsworth trace for raindrops |
| 38 | MAJOR | Accepted |
| 39 | MAJOR | Accepted: the definitions moved to the introduction; the paragraph lands on the orbit default, which the next section opens on |
| 40 | MINOR | Open: mckay1991making, trenberth2005trends and charnock1955wind remain BLOCKED (no legal original read); the manifest summary was regenerated and the release register carries them |

## Inventory (assumptions, repairs)

| # | Sev. | Disposition |
|---|---|---|
| 1 | MAJOR | Accepted: three defects "produce little or no error at Earth's values ... two through units of time and one through a constant"; the orbit default "puts an Earth constant in place of a configured value"; Table 2 gives form and kind apart |
| 2 | MAJOR | Accepted; the defect log's count note was corrected in 4fd640b |
| 3 | BLOCKING | Accepted: gravity as a number, a length and a frequency, then the other constants |
| 4 | MAJOR | Adapted: fitted laws classed as fits throughout; the fall-speed laws and the rain-size bounds both in the fits paragraph, the fall speeds with the scaling law that extends them; WRF-ELEC's thresholds stay constants |
| 5 | MINOR | In part: SWAN's knee placed with gravity and its air density scoped to CM1's equatorial seas; RRTMG's unfiltered Sun stays in Table 2 alone |
| 6 | MINOR | Accepted |
| 7 | MAJOR | Accepted (the second option): clear-air conduction is a simplification, in the fits paragraph, row "Fit, Capability" |
| 8 | MAJOR | Accepted |
| 9 | MINOR | Accepted; a CM1 dynamics row added |
| 10 | MINOR | Accepted: "in the design case" for the σ layers; "the curved-air table's design column" in Repairs and the layers figure |
| 11 | BLOCKING | Accepted: the fits in the order they erred (totals, split, heights) |
| 12 | MINOR | Accepted |
| 13 | MINOR | Accepted, with the race's time window |
| 14 | MINOR | Accepted |
| 15 | MINOR | Accepted |
| 16 | MAJOR | Accepted |
| 17 | MAJOR | Accepted, adapted: the classes are told apart by what was fitted to the test world |
| 18 | MAJOR | Accepted: the gas-band change described as part of each kind and classed a calibration in both tables; the daytime solver difference stated with the curved air |
| 19 | MAJOR | Accepted with the division proposed: the code change is the repair and the lunar value its setting; the fixed orbit, whole model days and SWAN's breaking are avoidances; CM1's and SWAN's forcing are couplings; "bypassed" and "open" are states in Table 2's caption |
| 20 | MAJOR | Accepted; the calendar sentence stays in this paragraph as an avoidance, corrected under finding 21 |
| 21 | BLOCKING | Accepted |
| 22 | MAJOR | Accepted |
| 23 | MAJOR | Accepted: "Switches and builds"; the rebuild moved to Verification |
| 24 | MINOR | Accepted after the check: `moon_omp`'s sources are byte-identical to `moon_omp_o3`'s (`models/cm1/builds.json`), so the series reproduce the 45° N rings' build as well |
| 25 | MINOR | Accepted |
| 26 | MAJOR | Accepted: similarity repairs and other general repairs in separate paragraphs |
| 27 | MINOR | Accepted: "the curved-air table" in prose, tables, claims and the appendix |
| 28 | MINOR | Accepted: the channels' construction moved to the appendix |
| 29 | MAJOR | Accepted |
| 30 | MINOR | Accepted; the ground term's clear-sky scaling confirmed in `notes/reference_radiation.md` |
| 31 | MINOR | Accepted |
| 32 | MINOR | Accepted |
| 33 | MINOR | Accepted |
| 34 | BLOCKING | Accepted: a parameterization fitted to crystals of 10 µm and larger, extrapolated in size below 190 K; class "General, above 190 K"; the reach table bounds the optics at 190 K |
| 35 | MAJOR | Accepted |
| 36 | MINOR | Accepted |
| 37 | MINOR | Accepted: "Curved air", "Calibration against the reference", "Forcing from the GCM" |
| 38 | MINOR | In part: the introduction keeps short class definitions while Repairs gives the criterion and the borderline cases; the horizon factors keep their numbers in the worlds section |

## Results (verification, results)

| # | Sev. | Disposition |
|---|---|---|
| 1 | MAJOR | Accepted, with a sentence on which checks concern properties of the code that hold on any world |
| 2 | MINOR | Accepted: three steps; arithmetic beside similarity in the section and the table |
| 3 | MINOR | Accepted |
| 4 | BLOCKING | Accepted: the chain closes for patches 01–03; patch names in prose |
| 5 | MINOR | Accepted for PyRADS (cited) and the record ("numbers alone"; the tilted-ring check "in Terluna's written record"); the Monte Carlo reference's source stays unnamed, the record holding its numbers alone |
| 6 | MAJOR | Accepted, with the wind-tunnel tests of SWAN for Mars as the reason a similarity test checks a wave model's gravity |
| 7 | MAJOR | Accepted |
| 8 | MAJOR | Adapted: the benchmark paragraph as proposed; the four arithmetic checks in the table, with one in the prose |
| 9 | MAJOR | Accepted: MacGorman et al., Kuhlman et al., Sun et al. and Salinas et al. cited; all four are BLOCKED in the manifest, their numbers from Terluna's record |
| 10 | MAJOR | Accepted, with Nicoll for the measured conductivity |
| 11 | MAJOR | Accepted: defects of the adaptation sorted by what remains in reported runs |
| 12 | BLOCKING | Accepted |
| 13 | MAJOR | Accepted: the open checks moved to Next steps and the table's "Leaves open" column |
| 14 | MINOR | Accepted |
| 15 | MINOR | Accepted |
| 16 | BLOCKING | Accepted |
| 17 | MINOR | Accepted |
| 18 | MINOR | Accepted |
| 19 | BLOCKING | Accepted; the figure marks the first channels |
| 20 | MAJOR | Accepted |
| 21 | BLOCKING | Accepted: the caption's baselines corrected; the figure redrawn by class, with the first calibration as an off-scale bar and the joined steps hatched |
| 22 | MAJOR | Accepted, with the cloud cover of Yang et al.'s cloud-permitting runs beside two GCMs' |
| 23 | MINOR | Accepted |
| 24 | MAJOR | Accepted; the 4 W m⁻² per kelvin stated as the ring's estimated sensitivity, its derivation unrecorded |
| 25 | MAJOR | Accepted |
| 26 | MAJOR | Accepted: "the Earth-orbit state" |
| 27 | MAJOR | Accepted |
| 28 | MINOR | Accepted |
| 29 | MINOR | Accepted |
| 30 | MAJOR | Accepted with a correction: the case files (`crm-runs/*/case.json`, `reference.run`) show the three boxes forced from the Earth-orbit state and the three rings from the Sun-and-tilt state; the text, Table 3 and claims G09 and G15 say so |
| 31 | MAJOR | Adapted: the arrangement first, then the flash density beside Earth's (Christian et al.); Earth's 5–30 C per ground strike dropped, its source unadmitted; the grid condition stated; the flash-rate laws used for tidally locked planets cited |
| 32 | MAJOR | Accepted |
| 33 | MAJOR | Accepted |
| 34 | MINOR | Accepted |
| 35 | MINOR | Accepted |

## Closing (reach, next, conclusions, availability, appendix)

| # | Sev. | Disposition |
|---|---|---|
| 1 | BLOCKING | Accepted: the joined steps named in Reach; the conclusions name them (rewritten again in bb5d0f0) |
| 2 | BLOCKING | Accepted: radiation from spectroscopy as the route to a general repair; cloud a calibration for each world; the reference check in Next steps |
| 3 | BLOCKING | Accepted |
| 4 | BLOCKING | Accepted |
| 5 | BLOCKING | In part: the declaration rewritten ("no competing interests ... brings the author no income", with the author's practice of making public what licences and sources allow); the repository "to be published with the paper's release commit"; an address and a route to the runs remain the author's to supply |
| 6 | MAJOR | Accepted |
| 7 | MAJOR | Accepted |
| 8 | MAJOR | Accepted; Table 4's header "Represented by the adapted models" |
| 9 | MAJOR | Accepted: three groups by what the modeller supplies; in bb5d0f0 the first group's heading became "Worlds that need the repairs as they stand" |
| 10 | MAJOR | Accepted |
| 11 | MAJOR | Accepted: a starlight row; the planets of M dwarfs need their shortwave refitted |
| 12 | MAJOR | Accepted |
| 13 | MAJOR | Moot after bb5d0f0, whose closing section opens on form and class and discusses the defects' errors by where they show |
| 14 | MAJOR | Accepted |
| 15 | MAJOR | Accepted, with the cloud-permitting comparison on tidally locked planets |
| 16 | MAJOR | Adapted in the third draft; reversed in bb5d0f0 at the author's direction: the closing section names no untested world as within reach |
| 17 | MAJOR | Accepted |
| 18 | MAJOR | Accepted |
| 19 | MAJOR | Accepted, with the direction of the RRTMG result corrected (whole, finding 13) |
| 20 | MAJOR | Accepted |
| 21 | MAJOR | Accepted: a list, issue #69 cited |
| 22 | MAJOR | Accepted; the clause on ChatGPT is written from Terluna's records and awaits the author's confirmation |
| 23 | MAJOR | Adapted: the author's stream-of-thought review recorded as the author counts it, the draft's cadence review; the assistant and the reviewer agents named |
| 24 | MAJOR | Accepted |
| 25 | MINOR | Accepted |
| 26 | MINOR | Accepted |
| 27 | MINOR | Accepted |
| 28 | MINOR | Accepted; the deciding measure is the design case's spread from year to year |
| 29 | MINOR | Accepted |
| 30 | MINOR | Accepted |
| 31 | MINOR | Accepted: LBLRTM and DISORT cited; TRAPPIST-1e's 6.1 days from Yang et al., Proxima Centauri b's 11.2 days from Boutle et al. |
| 32 | MINOR | Moot |
| 33 | MINOR | Accepted; a row for the flash-reach logging |

## Whole paper

| # | Sev. | Disposition |
|---|---|---|
| 1 | BLOCKING | Accepted: reach stated as built for, with evidence states; Table 4's caption says every run so far is of the test world, apart from the Earth benchmarks |
| 2 | BLOCKING | Accepted: the relation stated on the clean comparisons; the joined steps named; the repair figure coloured by class with the first calibration |
| 3 | BLOCKING | Accepted: "class" for the three, "kind" for the rest; configuration switches as avoidances; the beta plane's two rows told apart (Earth's β bypassed in Table 2; patch 16's Coriolis on departures a coupling in Table 6, active on the tilted rings, correcting "unused on the Moon") |
| 4 | MAJOR | Accepted in the third draft; in bb5d0f0 the closing section recalls the relation of form and class in its first paragraph |
| 5 | MAJOR | Accepted, then superseded by bb5d0f0 |
| 6 | MAJOR | Accepted: rows "Cloud thresholds" and "Convective cover, fit", with a sentence on the relative-humidity threshold |
| 7 | MAJOR | In part: Earth value and defect defined in the introduction; PlaSim related to ExoPlaSim there; the reference model named one way. Still ahead of their introduction: RRTMG in the worlds section, the synodic clock in Figure 2's caption, CM1's warm offset in Repairs, the eleven columns and the first calibration in the assumptions section |
| 8 | MAJOR | In part: Table 3's names used throughout and the next CM1 forcing named; the run with the extended spectrum and the uncalibrated first design run are still both called "first" |
| 9 | MAJOR | Accepted |
| 10 | MAJOR | Accepted: heading "The defects in other configurations"; "by the code's arithmetic"; issue #69 cited |
| 11 | MAJOR | Accepted in Results and the abstract; the closing section of bb5d0f0 is under review in round 2 |
| 12 | MAJOR | Accepted: the condition written into the assumptions and verification sentences |
| 13 | MAJOR | Accepted |
| 14 | MAJOR | Accepted, apart from the Monte Carlo reference's source |
| 15 | MAJOR | In part: the open checks merged into Next steps; the 295 K fit of the longwave correction still recurs in Results, Reach and Next steps |
| 16 | MAJOR | In part: the worlds section hands the orbit default to the assumptions section, and the assumptions section opens on what each form needs from a repair; the other section boundaries and Next steps' unordered items (still prose with run-in heads) are unchanged |
| 17 | MAJOR | In part: nicknames replaced, patch numbers moved to the tables, the adaptation's defects sorted by what remains in reported runs; the runners' mechanics stay in "Switches and builds", and the repository's address awaits the author |
| 18 | MAJOR | In part: the channels' construction moved to the appendix and Reach given its evidence states and world groups; the assumptions prose still walks through many of Table 2's rows |
| 19 | MAJOR | Accepted |
| 20 | MINOR | In part: the terms named defined or replaced; Table 7's "0.19 K of ground from water's lines" still appears in the table alone |
| 21 | MINOR | Accepted |
| 22 | MINOR | Accepted |
| 23 | MINOR | In part: most pairs reconciled; the 8.3% along the equatorial row and the 12% at 0° E stand without a stated link, and Results' "Two of the storm results" covers a second result on night fog and the air at 2 m |
| 24 | MINOR | Accepted |
| 25 | MINOR | Mars filled; the appendix pointer no longer cites a table ahead of order; the tables' placement goes to the G7 review |
| 26 | MINOR | In part: tense corrected; the repository's address awaits the author |

## Open after this round

The "In part" and "Open" rows above, the round-2 records on the rewritten closing section, and the AI-assistance
clause on ChatGPT, which awaits the author's confirmation.
