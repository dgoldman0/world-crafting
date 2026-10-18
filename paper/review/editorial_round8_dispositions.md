# Editorial round 8: dispositions

**Round.** Two fresh reviewer agents, both Claude Opus 5.5 subagents, read snapshot 44d67d4: the closing section and
the abstract whole, with the revised passages of Results, Next steps, Reach, Repairs, the introduction and the
assumptions section, and the register entries G11, H22 and H04. The prose record
(`editorial_round8_conclusion_prose.md`) raised 17 findings: 0 blocking, 2 major and 15 minor, and judged that the
section meets the author's direction. The evidence record (`editorial_round8_conclusion_evidence.md`) raised 15: 0
blocking, 3 major and 12 minor. The round found nothing blocking, which closes the rounds on the closing section under
the repository's rules.

**Revision.** Claude Opus 5.5, the drafting assistant, acted on the round's findings in commit 94d337a and wrote these
dispositions at the time. No further round read that revision; the author's reading is the next review. Before
revising, the drafting assistant checked the evidence record's graupel finding against Terluna's
`climate/crm/README.md:2064–2100` (hail's share of the non-inductive charging, 37% and 43% under Takahashi's law) and
its ground-strike counts against the same record and the WRF-ELEC README's list of charging options.

**Terms.** Accepted: the change was made as proposed or in an equivalent form. Adapted: the finding was met by a
different change, stated. In part: what was done and what remains. Open: left, with the reason. Locations are the
records' own, at 44d67d4.

## Prose record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| 1 | MAJOR | conclusions.tex:53–55 | Accepted: the cloud-top law first, then "in Sergeev et al.'s storm-resolving runs" the graupel flux and the column's ice water path |
| 2 | MAJOR | conclusions.tex:81–86 | In part: the turn is concessive ("Although the changes that remove or avoid the three defects contain no coefficient fitted to the test world, away from Earth's values the repaired codes have run on the test world alone"); the reach test keeps its configuration, compressed and named as Way et al.'s, since round 7's prose record and round 6's evidence record asked for the conditions that bring the orbit default into the released runs |
| 3 | MINOR | conclusions.tex:6–11 | Accepted |
| 4 | MINOR | conclusions.tex:14–20 | Accepted, with the optional "and so keeps every zonal mean" |
| 5 | MINOR | conclusions.tex:23 | Accepted: "Whereas" |
| 6 | MINOR | conclusions.tex:30–33 | Accepted: "typically" and "the same three hundredths of the radius as the test world's air" |
| 7 | MINOR | conclusions.tex:33–35 | Accepted |
| 8 | MINOR | conclusions.tex:41–45; abstract.tex:25–26 | Accepted in the conclusion; adapted in the abstract with evidence 14: "Water cloud would be calibrated for each world against cloud-resolving runs whose own microphysics is fitted on Earth" |
| 9 | MINOR | conclusion, abstract, next steps | Accepted: "would be built for" at all three |
| 10 | MINOR | conclusions.tex:68–75 | Accepted: "For CM1 the test is still to be made" and "a step still to run" cut |
| 11 | MINOR, optional | conclusions.tex:70–75, 86–90 | Accepted in part (a): the box's 85% evaporation against 64% at Earth's fall speeds, and the quarter of the GCM's rain, enter the drop-size discussion; (b) adapted with evidence 1: the landing asks of the second model's Earth-fitted drop and ice laws a test at that world's gravity |
| 12 | MINOR | abstract.tex:10–12; introduction.tex:73–75 | Accepted, with evidence 9's scope: "on the paths the lunar runs take, the released codes also contain five defects", "runs of slowly rotating and tidally locked planets among them" |
| 13 | MINOR | results.tex:47–48 | Accepted |
| 14 | MINOR | results.tex:91–99 | Accepted, with the optional landing ("Given the reference's spectroscopy and these tests") |
| 15 | MINOR | results.tex:159 | Accepted |
| 16 | MINOR | next.tex:14–15 | Accepted: "would replace both the correction and Sasamori's and Lacis and Hansen's fits" |
| 17 | MINOR | next.tex:85–89 | Accepted, with evidence 5's counts |

## Evidence record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| 1 | MAJOR | conclusions.tex:86–90 | Adapted: the landing names the cloud-resolving model's "own drop and ice laws, fitted on Earth", which "would in turn need testing at that world's gravity", leaves the charging laws to the lightning paragraph, and bounds the other world to nitrogen–oxygen air |
| 2 | MAJOR | conclusions.tex:51–53; next.tex:83–85; N01 | Accepted: the conclusion gives the impact speeds of hail and graupel, 4–8 and about 1–4 m\,s$^{-1}$, "since hail carried most of the charge under Saunders and Peck's law and graupel under Takahashi's"; Next steps has the hail measurement decide between the laws for hail and graupel's sign at its own speeds complete the decision; N01 gives hail's shares under both laws |
| 3 | MAJOR | next.tex:9–10 | Accepted: "The longwave correction, switched on with the ice optics, warmed the design case by 11.5~K, a joint effect in which the ice optics' share is unmeasured" |
| 4 | MINOR | results.tex:161–162; G11 | Accepted: "30 against 16--26~kC in the first window and 140 against 138--145~kC in the second, differing from the paired run by less than the Saunders and Peck runs differ among themselves", in Results and in G11 |
| 5 | MINOR | next.tex:85–87; G11 | Accepted: the first window's rule let no lunar channel reach the ground; the second window's strikes were 21 and 10, all negative |
| 6 | MINOR | next.tex:82–83 | Accepted: "in most of the second window's outputs and about half of the first's", in Next steps and G11 |
| 7 | MINOR | assumptions.tex:93–95, 207; H22 | Accepted: "turned over in two windows of an earlier run" in the sentence and the row; H22 points to G11 |
| 8 | MINOR | conclusions.tex:38–40 | Accepted: "with an independent code, PyRADS, ... and with an independent method, a Monte Carlo calculation" |
| 9 | MINOR | abstract.tex:10–11; introduction.tex:73 | Accepted, as prose 12 |
| 10 | MINOR | conclusions.tex:84–86; next.tex:37–39 | Accepted: "ozone-free planets of nitrogen-dominated air" in the conclusion, "1~bar nitrogen-dominated air with 400~ppm of carbon dioxide" in Next steps |
| 11 | MINOR | results.tex | Accepted once, in Results: "in WRF-ELEC's default form with Brooks et al.'s critical rime accretion rate above $-15$\,\textdegree C", cited to the archived WRF-ELEC README with a manifest locator (option `isaund` 12), since brooks1997effect awaits admission |
| 12 | MINOR | conclusions.tex:74–75 | Accepted in its first form: "would show, if the sizes that collisions allow scale as the largest stable drop does, how much ..." |
| 13 | MINOR | next.tex:14–17 | Accepted: "once that spectroscopy is checked and the reduction is checked against it layer by layer" |
| 14 | MINOR | abstract; conclusion | Adapted in the abstract (prose 8); the conclusion's sentence stands beside "CM1's runs compute with Earth-fitted microphysics of their own" |
| 15 | MINOR | abstract.tex:18–19 | Accepted: "is the only world the repaired codes have simulated away from Earth's values, numerical controls apart" |

## Also in 94d337a

The availability section's review history was brought through this round and the page inspection by hash, from the
records in this folder.

## Open after this round

- Prose 2, in part: the reach test's configuration stays in the conclusion, for the reason given.
- Round 7's prose 18 and round 6's open items, with their reasons.
- The read-aloud cadence pass, for the author.
