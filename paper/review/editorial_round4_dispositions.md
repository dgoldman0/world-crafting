# Editorial round 4: dispositions

**Round.** Two fresh reviewer agents, both Claude Opus 5.5 subagents, read snapshot 798f68b: the closing section
and the abstract whole, with revised passages of Results, Reach and Next steps. The prose record
(`editorial_round4_conclusion_prose.md`) raised 19 findings: 1 blocking (in Results), 4 major and 14 minor. The
evidence record (`editorial_round4_conclusion_evidence.md`) raised 20: 0 blocking, 7 major and 13 minor.

**Revision.** In commit 11026a8 Claude Opus 5.5, the drafting assistant, scoped the blocking sentence in Results to
Yang et al.'s comparison and tied it to PlaSim's diagnosed cover, and took the round's major findings into the
closing section: the released SWAN's knee as a property of its linear wind input; a new world bounded by
nitrogen–oxygen air with water and modest carbon dioxide, air at most as tall against its radius as the test
world's and spectroscopy checked against an independent code; the drop-size limits as Earth fits beyond what a
laboratory or a similarity run can test; the design's dimming, set with the calibrated model; and the slow-rotator
test as a pointer to Next steps. The abstract, Results, Reach, Next steps and the SWAN sentence of the assumptions section
were brought to the same scope.

**Reconstruction.** These dispositions were reconstructed after the round by a Claude subagent (Claude Opus 5.5)
comparing each finding with the revision commit; the drafting assistant acted on the findings at the time without
writing a dispositions record.

**Terms.** Accepted: the change was made as proposed or in an equivalent form, quoted where its wording differs.
Adapted: a different change met the finding, stated and quoted. In part: what was done and what remains. Open: the
fault stated in the finding remains in the passage at the revision commit, located there, with "no reason
recorded" where the commit message gives none. Moot: the passage went in a rewrite, with where its content went.
Locations in the tables are the records' own, at 798f68b; a remaining fault is located at 11026a8. Quotations
render the LaTeX source as text.

## Prose record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| 1 | BLOCKING | `results.tex:81–85` | Accepted as proposed, with the optional clause, "which counts cloud by a condensate threshold" (evidence F2, F8). The comparison is restated in the conclusion (prose 6) |
| 2 | MAJOR | `conclusions.tex:59–63` | Accepted, with gravity added: "keep coefficients fitted at Earth's gravity and ratio of air to water density" (evidence F3, F9). The assumptions sentence named in the finding keeps Mars "with that linear input switched on" and "wherever its frequency band reaches past the scaled knee", a condition that holds for weaker gravity alone (round 5, evidence 14) |
| 3 | MAJOR | `conclusions.tex:67–72` | Accepted: "Part of the test world's design was set with the model, and so with the Earth fits that remain in it"; the second sentence leaves out the 11.5 K and 6 K, which stand in the paragraph on fits, and the design's retention figures were cut from the conclusion; they remain in the introduction |
| 4 | MAJOR | `conclusions.tex:72–76` | Accepted as proposed. Same sentence as evidence F20 |
| 5 | MAJOR | `reach.tex:38–40` | Accepted, with the optional clause as "SWAN's ST6 drag, exact quadruplets and bottom friction, and SWASH's rotation, keep Earth's constants", and the Seas row given "Similarity at any gravity on the configuration's code paths". Same passage as evidence F7 |
| 6 | MINOR | `conclusions.tex:21–26` | In part: the comparison now names what agreed, "a comparison by global-mean temperature and albedo can pass large differences in cloud", "by their authors' account" (evidence F1). The agents of "passes" and "can pass" are still a check and a comparison (:20–22), and the clause still restates Results' comparison (prose 1). Same passage as evidence F1 and F8 |
| 7 | MINOR | `conclusions.tex:28` | Accepted as proposed. Evidence F17 concerns the same sentence |
| 8 | MINOR | `conclusions.tex:32–38` | Accepted as proposed: Titan in a sentence of its own, with "the plane-parallel codes that separate Titan's surface from its haze" |
| 9 | MINOR | `conclusions.tex:44–49` | Accepted as proposed, the sentence ending in evidence F11's wording. Same sentence as evidence F11 |
| 10 | MINOR | `conclusions.tex:52–56` | Accepted as proposed |
| 11 | MINOR | `conclusions.tex:3–9` | Accepted, with "would add" from evidence F10 (same sentence); the gapping also mended in the abstract (prose 19). The opening sentence keeps "four Earth-built codes adapted" (evidence F14) |
| 12 | MINOR | `conclusions.tex:76–80` | Accepted: "whose scale height is at most three hundredths of its radius, the test world's ratio" and "as it was from the test world's"; evidence F5's composition replaced the gases clause, and the closing clause was rewritten under evidence F4. Same sentence as evidence F4 and F5 |
| 13 | MINOR | The whole section | In part: the rewrites of findings 3, 4, 8 and 10 were made, and sentences of 70 words or more fell from eleven to seven (script count); the second paragraph's landing (:20–26, about 110 words), the fits sentence (:28–33, about 100) and the section's landing (:79–84, about 97) grew, and the audible reading remains pending |
| 14 | MINOR | `results.tex:51–53` | Accepted: "its clouds offsetting" |
| 15 | MINOR | `results.tex:90–93` | Adapted: the fits lead, then "while the geometry's curved-air terms, on the table's first channels, moved it by 0.65 K and the general repairs of units and constants measured singly by 1.6–2.5 K", an order out of rank (round 5, prose 15). Evidence F17 concerns the same sentence |
| 16 | MINOR | `reach.tex:89–90` | Accepted: "The third column". Same phrase as evidence F19 |
| 17 | MINOR | `next.tex:36–38` | Accepted as proposed. Same sentence as evidence F20 |
| 18 | MINOR | `abstract.tex:12–19` | Accepted, joined to the climate's evidence state (prose 19): "The test world's climate is unobserved, and it is the only world the repaired codes have run on away from Earth's values. There the two general repairs ...". Same sentences as evidence F6 and F17 |
| 19 | MINOR | `abstract.tex:10–17` | Accepted for "with little or no error", "took calibrations" and "up to 5.4%", the climate's state now a sentence of its own (prose 18); the clause on what the calibrations test was cut, and the checks sentence leads by a colon into the SWAN result. Same sentences as evidence F6 and F15 |

## Evidence record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| F1 | MAJOR | `conclusions.tex:21–26` | Adapted: "where a check of the arriving sunlight's global mean passes it, and a comparison by global-mean temperature and albedo can pass large differences in cloud", the three models "broadly alike ... by their authors' account"; the spreads of temperature and albedo left out. Same passage as prose 6 and evidence F8 |
| F2 | MAJOR | `results.tex:81–85` | In part: scoped in prose 1's wording, "two GCMs that diagnose their cover, as PlaSim does"; "came out broadly alike" stays in the paper's own voice in Results (:85–86), the conclusion alone adding "by their authors' account". Same passage as prose 1 and evidence F8 |
| F3 | MAJOR | `conclusions.tex:59–61` | Adapted: prose 2's rewrite cut the Mars clause and tied the knee to the input, "whose linear wind input bends at a fixed 1 Hz"; the assumptions sentence named in the finding keeps Mars "with that linear input switched on". Same sentence as prose 2 and evidence F9 |
| F4 | MAJOR | `conclusions.tex:79–80`, with `58–59` | In part: lines 58–59 became "so whether gravity enters a model consistently is tested by similarity runs", and the drop-size sentence ends "a dependence beyond what a laboratory on Earth or a similarity run can test" (:66–69); the closing clause still reads "whose laws of drops and charge remain Earth fits until laboratories and runs at other gravities test them" (:82–84). Same sentence as prose 12 |
| F5 | MAJOR | `conclusions.tex:76–78`; also `38–40` and `abstract.tex:20–21` | In part: the composition entered all three places, the independent-code check both places in the conclusion, and the landing's height bound became the test world's three hundredths; the pressures and temperatures were cut from the bound (`conclusions.tex:40–43`, `79–82`; `abstract.tex:20–22`), and the abstract gives "nitrogen–oxygen air" and leaves out water, carbon dioxide and the check. Same sentences as prose 12 and evidence F16 |
| F6 | MAJOR | `abstract.tex:12–14` | In part: "Where a value was repaired", "mostly" and "the radiative geometry" added; the dynamics clause left out, and the calibrations lost their bound, "that hold near the columns they were fitted on", which the correction kept (`abstract.tex:12–14`). Same sentence as prose 18 and 19 |
| F7 | MAJOR | `reach.tex:38–40` | In part: bounded by "In the configuration used", with the options that keep Earth's constants named, and the Seas row by "the configuration's code paths"; the tested paths went unlisted, so "on that configuration's code paths have been tested" (:38–41) takes in spherical grids and nests, which lie outside the similarity tests. Same passage as prose 5 |
| F8 | MINOR | `conclusions.tex:22–24`; `results.tex:83–84` | Accepted: Results adds "which counts cloud by a condensate threshold" (prose 1's optional clause). Same passages as prose 1 and 6 and evidence F1 and F2 |
| F9 | MINOR | `conclusions.tex:61–63` | Accepted in prose 2's wording with gravity added, "keep coefficients fitted at Earth's gravity and ratio of air to water density"; the Charnock comparison, a tenth to a half, left out. Same sentence as prose 2 and evidence F3 |
| F10 | MINOR | `conclusions.tex:9–10` | In part: "would add about 0.23"; the cover's cap of 0.8 left out (:9–10). Same sentence as prose 11 |
| F11 | MINOR | `conclusions.tex:47–49` | Accepted as proposed. Same sentence as prose 9 |
| F12 | MINOR | `conclusions.tex:51–52` | Accepted, with the −15 °C level left out: "from the upward flux of graupel and the ice aloft", in the conclusion and in Results, which now also gives the cloud-top law to both studies |
| F13 | MINOR | `abstract.tex:4–6` | Accepted: "would keep Earth-like air"; the loss rate left out. The commit message says the abstract names the design's loss rate; the abstract at 11026a8 omits it |
| F14 | MINOR | `abstract.tex:6–8`; `conclusions.tex:3` | Open: the abstract still reads "were adapted to such a world" (`abstract.tex:6–8`) and the conclusion "four Earth-built codes adapted" (`conclusions.tex:3`), SWASH's adaptation by configuration alone unstated; no reason recorded. Same opening sentence as prose 11 |
| F15 | MINOR | `abstract.tex:10–11` | In part: "that meet their conditions" added; the conditions stay unnamed, and the runs are still those "of slowly rotating and tidally locked planets" (`abstract.tex:10–12`), while the orbit default acts at any rotation. Same sentence as prose 19 |
| F16 | MINOR | `abstract.tex:20–22` | Accepted: "fitted to cloud-resolving runs, a fit still to be made on the test world". Same sentence as evidence F5 |
| F17 | MINOR | `abstract.tex:17–19`; `conclusions.tex:28–31`; `results.tex:90–93` | In part: the conclusion adds "the longwave correction, switched on with the ice optics, warmed the design case by 11.5 K in its test", and Results adds the geometry (prose 15); the abstract's ranking still gives the first calibration and the cloud settings alone (`abstract.tex:18–20`). Same sentences as prose 7, 15 and 18 |
| F18 | MINOR | `reach.tex:49–55` | Accepted: "ExoPlaSim would need" |
| F19 | MINOR | `reach.tex:89` | Accepted in prose 16's wording, "The third column" |
| F20 | MINOR | `next.tex:36–41`; `conclusions.tex:73–76` | In part: Next steps adds "at Earth's insolation and zero obliquity and eccentricity" (prose 17); Way et al.'s land and oceans stay unnamed there (`next.tex:36–39`), and the conclusion's sentence, cut to a pointer under prose 4, leaves the orbit unnamed (`conclusions.tex:77–79`). Same sentences as prose 4 and 17 |

Of the passages the evidence record lists outside its scope, `results.tex:44–45` now reads "a step that joined a
general repair and an avoidance with a calibration"; the other three appear under F3, F7 and F12.

## Open after this round

- Prose 6: a check and a comparison as the agents of "passes" and "can pass", and the clause restating Results'
  comparison (`conclusions.tex:20–26`). Round 5 cut the check clause (prose 5); the comparison clause and the
  restated figures remain at 8bfd069.
- Prose 13: seven sentences of 70 words or more, three of them longer than before, and the audible reading,
  still pending at 8bfd069.
- Evidence F2: "broadly alike" in the paper's own voice in Results; met in 8bfd069 (round 5, evidence 11).
- Evidence F4: the closing clause naming laboratories and runs at other gravities as tests of the laws of drops
  and charge; met in 8bfd069 (round 5, prose 1 and 3, evidence 2 and 6), which also rewrote the drop-size
  sentence's claim on laboratories (evidence 1).
- Evidence F5: the pressure and temperature bound on a new world, cut from three places; met in 8bfd069 (round 5,
  evidence 3 and 4, prose 14).
- Evidence F6: the calibrations' bound, "that hold near the columns they were fitted on", cut from the abstract;
  still absent at 8bfd069.
- Evidence F7: the tested scope of SWAN and SWASH in Reach; met in 8bfd069 (round 5, evidence 5 and 19).
- Evidence F10: the convective cover's cap of 0.8; met in 8bfd069 (round 5, evidence 9).
- Evidence F14 (Open): SWASH adapted by configuration alone, in the abstract and the conclusion; unchanged at
  8bfd069.
- Evidence F15: the three defects' conditions in the abstract; unchanged at 8bfd069.
- Evidence F17: the longwave test's 11.5 K, absent from the abstract's ranking; unchanged at 8bfd069.
- Evidence F20: Way et al.'s land and oceans in Next steps, unchanged at 8bfd069; the conclusion's orbit taken up
  in round 5 (evidence 15).
