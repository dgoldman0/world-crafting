# Editorial round 3: dispositions

**Round.** Two fresh reviewer agents, Claude subagents (Claude Opus 5.5), read commit e89a394: the closing section,
"Discussion and conclusions", whole, and five revised passages around it in reach (`reach.tex:41–58`), Next steps
("A test of the reach", `next.tex:35–42`), the abstract and Results. The working tree moved on during the reading,
and both reviewers read the frozen commit with `git show`, so their line numbers are those of e89a394. The prose
reviewer (`editorial_round3_conclusion_prose.md`) raised 21 findings, 2 blocking, 5 major and 14 minor; the
evidence reviewer (`editorial_round3_conclusion_evidence.md`) raised 17, 1 blocking, 6 major and 10 minor. Each
record adds three uncounted observations outside its scope.

**Revision.** Claude Opus 5.5, the drafting assistant, acted on both records in commit 798f68b: it bounded the
closing sentence to worlds whose gases, pressures and temperatures the line-by-line spectroscopy covers and whose
air stands within a few hundredths of the radius, with the spectroscopic scheme a step still to build, described
SWAN as built to keep its gravity scaling at any gravity and tested at a sixth of Earth's, stated the 20 K as the
first calibration's, the cloud fit as a step still to run, the retention as a loss rate with its time-scale and the
dry land as a seasonal effect, cut the repeats of Next steps, named the cited flash-rate studies, and carried the
same corrections into the abstract, Results, reach and Next steps. In the same commit the assistant fixed the
layout and build faults that the exact-build review of the PDF had found.

**Reconstruction.** These dispositions were reconstructed after the round by a Claude subagent (Claude Opus 5.5)
comparing each finding with the revision commit; the drafting assistant acted on the findings at the time without
writing a dispositions record.

**Terms.** Accepted: the change was made as proposed or in an equivalent form, its new wording quoted where it
differs. Adapted: a different change met the finding; the change is stated and its text quoted. In part: what was
done, and what remains. Open: the fault the finding names remains in the passage at the revision, located there,
with the reason given, or "no reason recorded" where none is recorded in the commit message. Moot: the passage went
in a rewrite, with where its content went, if anywhere. Locations are e89a394's, as the records give them; quoted
new text is 798f68b's, and line numbers marked "798f68b" are that commit's. P1 to P6 are the conclusion's six
paragraphs. Where two findings name the same passage, both rows say so.

## Prose record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| B1 | BLOCKING | `conclusions.tex:74–76` | Accepted, with a second bound, "and whose air stands within a few hundredths of its radius", and "the radiative geometry"; the abstract's "physics that holds across worlds" became "physics computed for each world's air, within the gases, pressures and temperatures the spectroscopy covers", where both records observed the same reach. Same passage as M4 and evidence 1 |
| B2 | BLOCKING | `conclusions.tex:54–58`; `reach.tex:39–40` | Accepted as proposed in both places. Same passage as evidence 13 |
| M1 | MAJOR | `conclusions.tex:41–46`, `58–63`, `71–74` | Accepted: (a) and (b) as proposed, the charge's magnitude, the evaporation fractions and the scaled-limit run left to Results and Next steps; (c) in M4's form. Same passages as M4 and evidence 14 (b), 15 (c) |
| M2 | MAJOR | `conclusions.tex:20–25` | Accepted as proposed, with evidence 8's "most of the difference on the night side and at high latitudes of the day side". Same passage as evidence 8 |
| M3 | MAJOR | `conclusions.tex:46–52` | Accepted, with evidence 6's "in Sergeev et al.'s storm-resolving runs" and evidence 12's "along the route Sergeev et al. propose of explicit charging in cloud-resolving runs". Same passage as evidence 6 and 12 |
| M4 | MAJOR | `conclusions.tex:65–74` | Accepted, with evidence 7's loss rates and evidence 15's "at Earth's insolation"; the rewrite's "with the released radiation" left out of the test sentence. Same passage as B1, M1 (c) and evidence 7, 15 |
| R1 | MAJOR | `results.tex:48–52` | Accepted as proposed, both changes: "The Sun and tilt changed the global means through the clouds", "with the Earth-orbit state's split of sunlight", and "From the Sun-and-tilt state, the curved air" |
| m1 | MINOR | `conclusions.tex:14–15` | Accepted as proposed |
| m2 | MINOR | `conclusions.tex:13–14` | Accepted as proposed |
| m3 | MINOR | `conclusions.tex:18–20` | Accepted as proposed. Same passage as evidence 3 |
| m4 | MINOR | `conclusions.tex:8–9` | Accepted as proposed. Same passage as evidence 2 |
| m5 | MINOR | `conclusions.tex:29–30` and `35` | Accepted as proposed |
| m6 | MINOR | `conclusions.tex:37` | Accepted, with evidence 5's "on the test world that fit is a step still to run". Same passage as evidence 5 |
| m7 | MINOR | `conclusions.tex:54` | Accepted as proposed |
| m8 | MINOR | `conclusions.tex:3–11` | Accepted as proposed, with m4's split. Same passage as m4 and evidence 2 |
| m9 | MINOR | `results.tex:82–86` | In part: "as well" removed and the cover's inputs given to CAM3 and ExoCAM; the new lead clause, "GCMs with diagnostic cloud schemes differ widely from cloud-permitting runs on tidally locked planets" (798f68b, 81–82), still sets models against runs, and round 4's reviewers read it as a claim about a class of models (prose 1, evidence F2). Same passage as evidence 9 |
| m10 | MINOR | `abstract.tex:4–6` | Accepted as proposed |
| m11 | MINOR | `abstract.tex:13–16` | Accepted as proposed |
| m12 | MINOR | `reach.tex:41–43` | Accepted as proposed; the caption of Table reach now reads "apart from the Earth benchmarks and numerical controls, the test world is the only world the adapted models have simulated". Same passage as evidence 16 |
| m13 | MINOR | `reach.tex:49–55` | Accepted as proposed |
| m14 | MINOR | `next.tex:37–38` | Accepted as proposed. Same passage as evidence 15 |

## Evidence record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| 1 | BLOCKING | `conclusions.tex:74–76` | In part: the landing bounded, the scheme made a step to build ("once a scheme is built from that spectroscopy, the gas absorption as well") and the geometry named as radiative; the bound is the spectroscopy's coverage and the scale height (798f68b, 76–80), wider in composition and pressure than the reach section's four limits, the bound of the proposed correction, and the proposed sentence on Titan, present Mars and Venus is absent, with Titan's radiation placed outside the adapted models in P3. Raised again in round 4 (evidence F5). Same passage as prose B1 |
| 2 | MAJOR | `conclusions.tex:8–9` | Adapted: prose m4's "that meet their conditions"; the conditions themselves stay in `reach.tex:16–24`. Same passage as prose m4 and m8 |
| 3 | MAJOR | `conclusions.tex:18–20` | Accepted in prose m3's arrangement: the dry-land share placed with the orbit default and its summer rain at 60°. Same passage as prose m3 |
| 4 | MAJOR | `conclusions.tex:27–29`; `abstract.tex:17–18` | Accepted in both: "the first calibration of the radiation's Earth fits, a Rayleigh multiplier and a weaker water continuum, moved the first design runs by at least 20 K", and in the abstract "the first calibration of the radiation's Earth fits"; Results' ranking (`results.tex:90–93` at 798f68b) changed with them. Same abstract sentence as evidence 17 |
| 5 | MAJOR | `conclusions.tex:37–38` | Accepted, with prose m6's "would stay": "on the test world that fit is a step still to run"; the clause on PlaSim's Earth-tuned settings until then left out. Same passage as prose m6 |
| 6 | MAJOR | `conclusions.tex:46–48` | Accepted in prose M3's opening, with "in Sergeev et al.'s storm-resolving runs". Same passage as prose M3 |
| 7 | MAJOR | `conclusions.tex:65–66` | Accepted as proposed. Same passage as prose M4 |
| 8 | MINOR | `conclusions.tex:22–25` | In part: the sentence rebuilt in prose M2's form, with the "where" added ("most of the difference on the night side and at high latitudes of the day side"); "a comparison of models by their global means" still takes in the cover, itself a global mean that differs 2 to 3.5 times, where the proposed correction has "global-mean temperature and albedo", and (c), the sea surfaces held at the coarser runs' temperatures, is absent (798f68b, 21–26). Same passage as prose M2 |
| 9 | MINOR | `results.tex:82–86` | In part: "of this kind" and "as well" removed, the cover's inputs given to CAM3 and ExoCAM; finding 8's point (c), the held sea surfaces, is absent here too (798f68b, 81–85). Same passage as prose m9 |
| 10 | MINOR | `conclusions.tex:30–34` | Accepted: "The radiative geometry of tall air", "while the dynamics keep a thin shell and constant gravity", and "although Titan's nitrogen–methane radiation lies outside the adapted models"; the scale-height bound went to the landing. Same paragraph as evidence 11 |
| 11 | MINOR | `conclusions.tex:31–32` | Accepted as proposed. Same passage as evidence 10 |
| 12 | MINOR | `conclusions.tex:51–52` | Accepted: "along the route Sergeev et al. propose of explicit charging in cloud-resolving runs". Same passage as prose M3 |
| 13 | MINOR | `conclusions.tex:55–58` | Accepted in prose B2's form: "the patch, built to keep the scaling at any gravity, has been tested at a sixth of Earth's on the code paths those tests ran". Same passage as prose B2 |
| 14 | MINOR | `conclusions.tex:61–62` | Moot: the evaporation figures left the conclusion with prose M1 (b); `next.tex:70` and claim N03 keep the rings' 57–73% with their forcing unnamed. Same passage as prose M1 (b) |
| 15 | MINOR | `conclusions.tex:71–73`; `next.tex:35–38` | Accepted in both: "on Earth-air planets at Earth's insolation". Same passages as prose M1 (c), M4 and m14 |
| 16 | MINOR | `reach.tex:42–43` | Accepted in prose m12's wording, the table caption with it. Same passage as prose m12 |
| 17 | MINOR | `abstract.tex:16–17` | Accepted as proposed. Same sentence as evidence 4's abstract part |

## Open after this round

- Prose m9 and evidence 9: the lead clause at `results.tex:81–82` (798f68b) sets GCMs against cloud-permitting runs,
  and the cloud-permitting runs' held sea surfaces stay unstated.
- Evidence 1: the landing's bound (798f68b, `conclusions.tex:76–80`) is the spectroscopy's coverage and the scale
  height, wider than the reach section's four limits, and the proposed sentence on Titan, present Mars and Venus is
  absent.
- Evidence 8: "a comparison of models by their global means" (798f68b, `conclusions.tex:21–26`) takes in the cover,
  where the proposed correction has "global-mean temperature and albedo", and the held sea surfaces stay unstated.

The six uncounted observations name four passages. Two, each observed in both records, were corrected in 798f68b:
`results.tex:93`'s "more than 20 K" and the abstract's "physics that holds across worlds". Two stand as they were:
`repairs.tex:106–108`, which ties Titan's 65° to its air, "taller in proportion", and the Figure 1 caption's solar
days (`worlds.tex:24`).
