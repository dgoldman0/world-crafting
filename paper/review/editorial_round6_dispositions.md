# Editorial round 6: dispositions

**Round.** Two fresh reviewer agents, both Claude Opus 5.5 subagents, read snapshot 8bfd069: the closing section
and the abstract whole, with the revised passages of Results, Reach, Next steps and the assumptions section. The
prose record (`editorial_round6_conclusion_prose.md`) raised 18 findings: 0 blocking, 2 major and 16 minor, and
judged that the section meets the author's direction once its two major findings are repaired. The evidence record
(`editorial_round6_conclusion_evidence.md`) raised 21: 2 blocking, 2 major and 17 minor, with two uncounted notes
outside its scope.

**Revision.** Claude Opus 5.5, the drafting assistant, made the revision in commit 654ebdf and wrote these
dispositions at the time. Both records found the same two faults: the planned gas scheme was given the range of the
reference's correlated-$k$ tables as its domain, wider than any check of the spectroscopy, and the closing sentence
bounded a class of new worlds and attached the procedure, with the lightning's sign, to the whole class. The closing
sentence was rebuilt to name the evidence each fit would take on another world, and the scheme was bounded by the
spectroscopy's check. The same commit acted on the out-of-scope observations of rounds 2 to 5 listed at the end.

**Terms.** Accepted: the change was made as proposed or in an equivalent form. Adapted: the finding was met by a
different change, stated. In part: what was done and what remains. Open: left, with the reason. Moot: the passage
went in the rewrite. Locations are the records' own, at 8bfd069.

## Prose record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| 1 | MAJOR | conclusions.tex:39–43, 81–84; abstract.tex:21–25 | Adapted, in the sense of the record's reading (b): the scheme would replace the gas fits "at the pressures and temperatures over which an independent code has checked that spectroscopy, a check so far planned on the design column alone"; the abstract has "over the pressures and temperatures where an independent code has checked that spectroscopy". The tables' range left the conclusion and the abstract, so the body needs no statement of it. Same passage as evidence 3 |
| 2 | MAJOR | conclusions.tex:81–86 | Adapted: the landing defines no class of new worlds and carries neither the lightning's sign nor the drop limits as part of a cloud fit. It reads: "The fits, which moved the test world's climate furthest, would be refitted or replaced on another world from evidence outside the adapted codes: the gas fits from line-by-line spectroscopy checked against an independent code, the cloud from cloud-resolving runs of that world, and the drop and charging laws inside those runs from laboratory tests." Same passage as evidence 1 |
| 3 | MINOR | conclusions.tex:3–7 | Accepted: the section opens on the relation of form to repair, and the defects follow in their own sentence |
| 4 | MINOR | conclusions.tex:21–26, 48–50, 65–67, 67–71 | Accepted at 48–50 ("so that") and 65–67 ("while"); adapted at 21–26, where "since global means can differ far less than cloud cover does" states the relation and Yang et al.'s evidence takes its own sentence; adapted at 67–71, where the drop sentences were rewritten with evidence 13 |
| 5 | MINOR | conclusions.tex:31–33 | Accepted: "moved the global mean by up to about 6~K as the runs settled". Same passage as evidence 6 |
| 6 | MINOR | conclusions.tex:35–36, 64 | Accepted: the 5.8~W\,m$^{-2}$ clause and the 1~Hz clause cut |
| 7 | MINOR | conclusions.tex:37–39 | Accepted: "On Titan, whose haze has a scale height of about 80~km, three hundredths of its radius as for the test world's air, ..."; the body now gives the haze and its scale height (repairs.tex), and the manifest holds Vincendon and Langevin's sentence as a locator, in place of a claim entry. Same passage as evidence 8 |
| 8 | MINOR | conclusions.tex:43–44; abstract.tex:24 | Accepted: "would be a calibration" in both |
| 9 | MINOR | conclusions.tex:47 | Adapted: the paragraph opens on the charging laws' fit to laboratory measurements, and resolved storms enter at its end as a comparison between models (evidence 2) |
| 10 | MINOR | conclusions.tex:51–52, 85–86; next.tex:80–81 | Accepted: "conditions laboratories reach" left the conclusion, and next.tex has "measured in a laboratory" in place of "conditions Earth's laboratories can reach". The landing's "laboratory tests" names the kind of evidence and states no reach of a laboratory |
| 11 | MINOR | conclusions.tex:58–60 | Accepted: "on grids fine enough to converge the flash count", with the discharge thresholds set for Earth's storms (evidence 2) |
| 12 | MINOR | conclusions.tex:76–78 | Accepted in substance: "The changes that remove or avoid the three defects contain no coefficient fitted to the test world, and away from Earth's values the repaired codes have run on the test world alone, so ..." |
| 13 | MINOR | abstract.tex:17–18 | Accepted |
| 14 | MINOR | results.tex:44–46, 27 | Accepted: "a year of whole model days" in the sentence and in the Sun-and-tilt row, and the classes in apposition: "a general repair, two avoidances, one of them output bookkeeping, and a calibration made in one step". Same passage as evidence 18 |
| 15 | MINOR | results.tex:81–86 | Accepted: the Yang et al. sentences now follow "Ranked by form" and precede "Given the reference's spectroscopy" |
| 16 | MINOR | results.tex:151–155 | Accepted, with evidence 9's "at $-15$\,\textdegree C and the column's ice water path" |
| 17 | MINOR | reach.tex:33–35, 38–42 | Accepted: "released SWAN, in the configuration used, loses ..."; "With SWAN's knee patched, SWAN and SWASH, in the configuration used, are built to run ..." |
| 18 | MINOR | reach.tex:114 | Accepted |

## Evidence record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| 1 | BLOCKING | conclusions.tex:81–86 | Adapted: the closing sentence names no class of worlds, so the bounds of pressure, temperature, gravity, day and starlight it lacked have nothing to bound; it states the evidence each fit would take on another world. The scheme's domain elsewhere is the coverage of the spectroscopy's check (prose 1, evidence 3). Same passage as prose 2 |
| 2 | BLOCKING | conclusions.tex:47–48, 58–60 | Accepted in substance: the paragraph opens "The storm models' charging laws were fitted to laboratory measurements"; resolved storms at other gravities are "the route Sergeev et al. propose for tuning such laws where observations are lacking" and "would set those laws beside flashes computed from the same laboratory charging laws and from discharge thresholds set for Earth's storms, on grids fine enough to converge the flash count: a comparison between models at each gravity" |
| 3 | MAJOR | conclusions.tex:40–43; abstract.tex:21–25 | Adapted as prose 1; with the tables' range gone, their water-fraction limit needs no statement |
| 4 | MAJOR | conclusions.tex:21–26 | Adapted: "since global means can differ far less than cloud cover does", then the cover values, the condensate threshold, the sea surfaces fixed from a coarser run of the same model, and "the planetary albedos lay 2 to 11 points apart" (SI Table 3). The authors' judgement of broad similarity left the conclusion and stays in Results, attributed |
| 5 | MINOR | conclusions.tex:6–7 | Accepted |
| 6 | MINOR | conclusions.tex:30–33 | Accepted for the 11.5~K ("over years 10--19, with a correction fitted at 295~K"); adapted for the cloud settings, "moved the global mean" (prose 5), since the cloud-water test ran from the first calibrated run and the others from the Sun-and-tilt run |
| 7 | MINOR | conclusions.tex:36–37 | Accepted |
| 8 | MINOR | conclusions.tex:37–39 | Accepted as prose 7; manifest locator for the 80 km and the 2,575 km radius added |
| 9 | MINOR | conclusions.tex:55; results.tex:155 | Accepted: "the column's ice water path" in both, and "at $-15$\,\textdegree C" in Results |
| 10 | MINOR | conclusions.tex:55–58 | Accepted: "six runs with Morrison's microphysics" and "the main electrified run, with the NSSL microphysics" |
| 11 | MINOR | conclusions.tex:62–63 | Accepted: "Whether gravity enters a model consistently is a property of the code, tested by similarity runs." The clause on the wind-tunnel tests for SWAN's Mars runs was left out, since the paragraph no longer sets laboratories against similarity runs |
| 12 | MINOR | conclusions.tex:67–68 | Accepted in a reworded form: "For CM1 the test is still to be made: the pair of runs designed to measure how far its convection, with gravity-scaled microphysics, departs from Earth's convection stretched sixfold failed to convect." |
| 13 | MINOR | conclusions.tex:68–71 | Accepted: "other media falling through other fluids"; "On Earth, collisions set the largest raindrops, so runs with Morrison's limits scaled by the capillary length would bound a sensitivity, a step still to run." |
| 14 | MINOR | conclusions.tex:79–81 | Accepted, with "ozone-free" from evidence 21 |
| 15 | MINOR | abstract.tex:10–12 | Accepted: "bias ExoPlaSim's runs that meet their conditions, slowly rotating and tidally locked planets among them"; the same in introduction.tex (the record's uncounted note) |
| 16 | MINOR | abstract.tex:13–14 | Accepted |
| 17 | MINOR | results.tex:81–86 | Accepted: the cloud-permitting model "ran over sea surfaces fixed from a coarser run of the same model", and "The planetary albedos lay closer, 22.1--29.1 and 39.0--47.0\% in the GCMs against 18.1 and 37.4\%, and the authors judged the three models' climates broadly similar." Manifest locators added for the cover drivers, the cover definitions, the judgement, the fixed sea surfaces and the albedos |
| 18 | MINOR | results.tex:44–46 | Accepted as prose 14; Terluna's `climate/gcm/README.md:173–178` dates the whole model days to 2026-09-29, with the Sun clock's repair |
| 19 | MINOR | results.tex:93–94 | Accepted |
| 20 | MINOR | assumptions.tex:22–24 | Accepted: "mostly arbitrary"; "by up to 5.44\%" |
| 21 | MINOR | next.tex:38–42 | Accepted: "ozone-free Earth-air planets" and "the two models' own physics and configurations" |
| note | — | next.tex:14–16 | Accepted: the scheme, "once that spectroscopy is checked, would hold on columns within the gases, pressures and temperatures of the check" |
| note | — | introduction.tex:73–75 | Accepted, as evidence 15 |

## Out-of-scope observations of rounds 2 to 5, acted on in the same commit

| Round, record | Observation | Disposition |
|---|---|---|
| 3, prose | repairs.tex:106–108 gave Titan's 65\textdegree\ to its air | Accepted: "about 65\textdegree\ on Titan, whose haze has a scale height of about 80~km, 3\% of its radius" |
| 2, prose 16 | next.tex:16 bounded the scheme by gases and pressures alone | Adapted: bounded by the check's gases, pressures and temperatures |
| 2 and 3, evidence | Figure 1's caption places the slow rotators at solar days of 16, 64 and 243 days, where the test of the reach uses sidereal periods | Open: the caption states the plotted points exactly, as illustrative positions; the test of the reach names its periods as sidereal |
| 4, evidence 6 | The abstract lost the calibrations' bound | Accepted: "each holding near the columns it was fitted on" |
| 4, evidence 14 | SWASH adapted by configuration alone, unstated in the abstract and conclusion | Open: the abstract's "adapted" covers a configuration, and the body states that SWASH runs unmodified |
| 4, evidence 17 | The abstract's ranking leaves out the 11.5~K | Open: the abstract ranks the single repairs, the first calibration and the cloud settings; the joint test of the longwave correction and ice optics stays in Results and the conclusion, for the abstract's length |
| 4, evidence 20; 5, evidence 15 | Way et al.'s configuration and orbit in the test of the reach | Accepted: Earth's insolation, zero obliquity and eccentricity, ozone-free air, and "physics and configurations" |
| 5, prose 6 | The Titan ratio had no record | Accepted: the 80~km in repairs.tex and in the manifest |
| 5, prose 8 | The conclusion's flash-rate laws repeated Results | In part: the conclusion states the laws in one clause, Results in full |
| 5, evidence 16 | The landing left the single design column and the reach table unnamed | Moot: the landing bounds no class of worlds |
| 5, evidence 17 | The calibrations named the line-by-line model alone | Accepted |

## Open after this round

- Figure 1's caption, round 4's evidence 14 and 17, as above, with their reasons.
- Round 5's prose 8, in part.
- The audible cadence pass of the conclusion, recorded as silent by both reviewers, remains for the author.
- Round 7 reads the revision (654ebdf).
