# Editorial round 5: dispositions

**Round.** Two fresh reviewer agents, both Claude Opus 5.5 subagents, read snapshot 11026a8: the closing section
and the abstract whole, with the revised passages of Results, Reach, Next steps and the assumptions section. The
prose record (`editorial_round5_conclusion_prose.md`) raised 18 findings: 1 blocking, 3 major and 14 minor. The
evidence record (`editorial_round5_conclusion_evidence.md`) raised 19: 2 blocking, 4 major and 13 minor.

**Revision.** In commit 8bfd069 Claude Opus 5.5, the drafting assistant, rewrote the sentences that had
laboratories and runs at other gravities testing the cloud-resolving runs' laws of drops and charge: the drop-size
sentence now cites the laboratory experiments that Loftus and Wordsworth report, the paragraph on storms has
laboratories test the charging laws and resolved storms test other studies' flash-rate laws, and in the closing
sentence, recast as what a modeller of a new world would compute, fit and leave as Earth's, that world is bounded by
its composition, the pressure and temperature range of the reference's tables and the test world's ratio of scale
height to radius. The abstract, Results, Reach, Next steps and the SWAN sentence of the assumptions section were
brought to the same scope, repeated numbers were cut, the SWAN README lost an excluded phrase, claim R08 gained the
tables' ranges, and the source manifest gained the Loftus and Wordsworth passage.

**Reconstruction.** These dispositions were reconstructed after the round by a Claude subagent (Claude Opus 5.5)
comparing each finding with the revision commit; the drafting assistant acted on the findings at the time without
writing a dispositions record.

**Terms.** Accepted: the change was made as proposed or in an equivalent form, quoted where its wording differs.
Adapted: a different change met the finding, stated and quoted. In part: what was done and what remains. Open: the
fault stated in the finding remains in the passage at the revision commit, located there, with "no reason
recorded" where the commit message gives none. Moot: the passage went in a rewrite, with where its content went.
Locations in the tables are the records' own, at 11026a8; a remaining fault is located at 8bfd069. Quotations
render the LaTeX source as text.

## Prose record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| 1 | BLOCKING | `conclusions.tex:82–84`; `:46–47` | Accepted: lines 46–47 as proposed, "Some Earth-fitted laws of storms can be tested independently of the world modelled, in laboratories on Earth or against storms resolved at other gravities"; the landing's clause in the fuller form of prose 3. Same passages as prose 3 and evidence 2, 6 and 16 |
| 2 | MAJOR | `conclusions.tex:66–69` | Adapted: evidence 1's correction was taken for this rewrite: "experiments on the largest stable drops of other liquids at Earth's gravity agree with that capillary-length form within about 20%", cited to Loftus and Wordsworth, "and runs with Morrison's limits scaled by it are a step still to run". Same passage as evidence 1 |
| 3 | MAJOR | `conclusions.tex:79–84`, against `:34–36` and `:40–44` | Accepted: the landing recast as the modeller's three operations, with evidence 3's bound added, "at pressures and temperatures within the reference's tables and with a scale height at most three hundredths of its radius". Same sentence as prose 1 and evidence 2, 3 and 16 |
| 4 | MAJOR | `results.tex:151–154` | Accepted: "whose tops stand far below the lunar runs' 55–80 km", with evidence 12's air for Sergeev et al.'s runs. Same sentence as evidence 12 and prose 8 |
| 5 | MINOR | `conclusions.tex:20–26` | Accepted as proposed, with evidence 10's "which count cloud by a condensate threshold". Same passage as evidence 10 |
| 6 | MINOR | `conclusions.tex:37–40` | In part: the sentence was kept and its 80 km figure cut, "Titan's haze stands about as tall against its radius as the test world's air", with the "although" clause; the ratio rests on the source's 80 km, a figure absent from `claims.json` and the manifest, and the sentence keeps its place between the geometry and the gas scheme (:37–39), its relation to that sequence unwritten; no reason recorded |
| 7 | MINOR | `conclusions.tex:54–59` | Accepted as proposed. Evidence 6 concerns its second sentence |
| 8 | MINOR | `conclusions.tex:49–51` against `next.tex:79–81`; `conclusions.tex:51–54` against `results.tex:151–154` | In part: the measurement now stands "at the impact speeds, cloud water and temperatures of the lunar storms"; the sentence on the flash-rate laws keeps "and set the flash rate from the cloud-top height or, in Sergeev et al.'s storm-resolving runs, from the upward flux of graupel and the ice aloft" (:54–55), repeating `results.tex:154–155` apart from "set" for "setting"; no reason recorded. Same Results sentence as prose 4 and evidence 12 |
| 9 | MINOR | `conclusions.tex:73–75` | Accepted as proposed |
| 10 | MINOR | `conclusions.tex:75–79` | Accepted, with "at zero obliquity" from evidence 15. Same sentence as evidence 15 |
| 11 | MINOR | `conclusions.tex:63` and `:44` | Accepted as proposed |
| 12 | MINOR | `conclusions.tex:6`; `abstract.tex:13` | Accepted as proposed. Same phrases as evidence 17 |
| 13 | MINOR | `abstract.tex:8–12` | Accepted as proposed |
| 14 | MINOR | `abstract.tex:20–22` | Accepted in evidence 4's wording, "once that spectroscopy is checked against an independent code". Same sentence as evidence 4 |
| 15 | MINOR | `results.tex:90–94` | Accepted as proposed |
| 16 | MINOR | `reach.tex:38–41` (and `:34–35`) | Accepted: "all outside that configuration". "In the configuration used" still comes at `reach.tex:34` and `:38`, and the inventory's row of unselected options, left by the finding to the author, is unchanged. Same sentence as evidence 5 |
| 17 | MINOR | `next.tex:36–43` | Accepted as proposed: "would be run" and "would be reclassified". Same sentence as evidence 15 |
| 18 | MINOR | `assumptions.tex:21–26` | Accepted, with evidence 14's condition, "past the lower of the two knees, g/g_E Hz under weaker gravity and 1 Hz under stronger". The README sentence named outside scope now reads "avoided these options and left them unpatched". Same passage as evidence 14 |

## Evidence record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| 1 | BLOCKING | `conclusions.tex:67–69` | Accepted, with "that capillary-length form" for "that scaling"; the source manifest records the passage (App. C1, p. 22). Same passage as prose 2 |
| 2 | BLOCKING | `conclusions.tex:82–84` | Adapted: the landing in the wording of prose 1 and 3, "fit its cloud scheme to cloud-resolving runs whose drop-size limits stay Earth's and whose lightning takes its sign from charging laws that Earth's laboratories can test"; the similarity runs' test of consistency stays at :62–63. Same sentence as prose 1 and 3 |
| 3 | MAJOR | `conclusions.tex:79–82`, and `40–42` | Accepted: "at the pressures and temperatures its tables cover, up to 3.2 bar and 375 K" in the third paragraph and "at pressures and temperatures within the reference's tables" in the landing; claim R08 records the tables' ranges. Same sentence as prose 3 |
| 4 | MAJOR | `abstract.tex:20–22` | Accepted as proposed. Same sentence as prose 14 |
| 5 | MAJOR | `reach.tex:38–41` | Accepted as proposed. Same sentence as prose 16 |
| 6 | MAJOR | `conclusions.tex:46–47` (with `57–59`) | Adapted: prose 1's wording, "Some Earth-fitted laws of storms can be tested independently of the world modelled, in laboratories on Earth or against storms resolved at other gravities", which detaches the laws from the runs' own microphysics. Same sentences as prose 1 and 7 |
| 7 | MINOR | `conclusions.tex:30–31` | Accepted as proposed |
| 8 | MINOR | `conclusions.tex:31–33` | Accepted: "moved it by up to about 6 K as the runs settled", "it" being the global-mean surface temperature named at the head of the sentence |
| 9 | MINOR | `conclusions.tex:9–10` | Accepted as proposed |
| 10 | MINOR | `conclusions.tex:21–26` | Accepted: "which count cloud by a condensate threshold"; the optional spreads left out. Same passage as prose 5 |
| 11 | MINOR | `results.tex:81–86` | Accepted as proposed |
| 12 | MINOR | `results.tex:151–154` | Accepted as proposed. Same sentence as prose 4 and prose 8 |
| 13 | MINOR | `results.tex:44–46` | Accepted as proposed |
| 14 | MINOR | `assumptions.tex:21–26` | Accepted; the optional rewording of the Mars clause left out. Same passage as prose 18 |
| 15 | MINOR | `conclusions.tex:76–79`, and `next.tex:36–39` | In part: the conclusion adds "at zero obliquity"; Earth's insolation and zero eccentricity stay out of it, and "Earth-air", for Way et al.'s ozone-free air, stays in both places (`conclusions.tex:79–80`; `next.tex:36`). Same sentences as prose 10 and 17 |
| 16 | MINOR | `conclusions.tex:79–84` | Open: the recast landing reads "would compute its radiative geometry from its own column" (:81–83) and leaves the single clear design column, the vertical grid and Table tab:reach unnamed; no reason recorded. Same sentence as prose 1 and 3 |
| 17 | MINOR | `abstract.tex:12–14`, and `conclusions.tex:5–7` | In part: the abstract takes "within the limits of their laws", "gas and scattering fits" and "its correlated-k emulation", with prose 12's "a method whose table is computed for each world's column"; the conclusion still gives "calibrations to a line-by-line model" alone (`conclusions.tex:6–7`). Same phrases as prose 12 |
| 18 | MINOR | `reach.tex:90–93` | Accepted as proposed |
| 19 | MINOR | `reach.tex:114` | Accepted as proposed |

## Open after this round

- Prose 6: the Titan sentence, its ratio, which lacks a claim record or locator, and its place between the
  geometry and the gas scheme (`conclusions.tex:37–39`).
- Prose 8: the conclusion's description of the flash-rate laws, in the words of Results (`conclusions.tex:52–55`).
- Evidence 15: Earth's insolation and zero eccentricity in the conclusion's test, and "Earth-air" for Way et al.'s
  ozone-free air (`conclusions.tex:79–80`; `next.tex:36`).
- Evidence 16 (Open): the landing's single clear design column, vertical grid and pointer to Table tab:reach
  (`conclusions.tex:81–86`).
- Evidence 17: the conclusion's calibrations, named to the line-by-line model alone (`conclusions.tex:6–7`).
- From round 4, unchanged at 8bfd069: prose 6's comparison as the agent of "can pass", with the comparison's figures
  restated from Results; prose 13's audible reading; evidence F6's bound on the calibrations in the abstract;
  evidence F14, SWASH adapted by configuration alone; evidence F15, the three defects' conditions in the abstract;
  evidence F17, the 11.5 K absent from the abstract's ranking; and evidence F20, Way et al.'s land and oceans in
  Next steps.
