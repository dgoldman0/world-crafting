# Editorial round 2: dispositions

**Round.** Two fresh reviewer agents, Claude subagents (Claude Opus 5.5), read commit bb5d0f0: the closing section,
"Discussion and conclusions" (`conclusions.tex`), whole, and the reach section's run-in heading "Worlds that need the
repairs as they stand." with its paragraph (`reach.tex:47–56`). The prose reviewer
(`editorial_round2_conclusion_prose.md`) raised 20 findings, 2 blocking, 8 major and 10 minor; the evidence reviewer
(`editorial_round2_conclusion_evidence.md`) raised 30, 4 blocking, 13 major and 13 minor. The prose record adds two
uncounted observations outside its scope, the evidence record four.

**Revision.** Claude Opus 5.5, the drafting assistant, acted on both records in commit e89a394, rebuilding the
closing section around what the findings mean: errors that keep the arriving sunlight's global mean and change the
climate through its clouds, beside models that agree in global means while disagreeing in cloud; what a modeller of
a new world can compute from its column and what stays a calibration; Earth laws that laboratories and runs at other
gravities can test; gravity similarity; and one design's retention, ending on the first test off the test world and
on cloud as the part each world must calibrate. The assistant also entered the two-year test of the Sun and tilt
alone as claim G17, with a sentence in Results, and corrected reach, Next steps, the abstract, Results and the
classes in the CM1 README where the reviewers found them overstated.

**Reconstruction.** These dispositions were reconstructed after the round by a Claude subagent (Claude Opus 5.5)
comparing each finding with the revision commit; the drafting assistant acted on the findings at the time without
writing a dispositions record.

**Terms.** Accepted: the change was made as proposed or in an equivalent form, its new wording quoted where it
differs. Adapted: a different change met the finding; the change is stated and its text quoted. In part: what was
done, and what remains. Open: the fault the finding names remains in the passage at the revision, located there,
with the reason given, or "no reason recorded" where none is recorded in the commit message. Moot: the passage went
in a rewrite, with where its content went, if anywhere. Locations are bb5d0f0's, as the records give them; quoted
new text is e89a394's, and line numbers marked "e89a394" are that commit's. P1 to P6 are the conclusion's six
paragraphs. Where two findings name the same passage, both rows say so.

## Prose record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| F1 | BLOCKING | `conclusions.tex:3–69` | In part: rebuilt in six paragraphs on the lines of the record's Appendix A, with the TRAPPIST-1e bias, the join of laboratory and similarity tests and the designer's refits brought in; passages restating Results and Next steps remain (e89a394, 41–46, 58–63, 71–74; round 3, prose M1), the turn from P2's global means to P3's ranking stays unwritten, and the wind-tunnel link is left out |
| F2 | BLOCKING | `conclusions.tex:41–44` | Adapted, in evidence 3's form: the claim about low-gravity worlds removed, the sentence ending on "a run with limits scaled to the capillary length would measure how much of that evaporation the small drops cause". Same passage as evidence 3 and 7 |
| F3 | MAJOR | `conclusions.tex:11` and `19–20` | In part: the first sentence as proposed ("Two of the three keep the global mean of the sunlight arriving at the top of the air and move that sunlight between places"), with the moved global means now reported; the last sentence was kept and revised ("An error of this kind leaves a check of the arriving sunlight's global mean unchanged, ..."), and its first clause restates P2's opening (e89a394, 20–22; round 3, prose M2); met at 798f68b. Same passage as F11 and evidence 1, 20 |
| F4 | MAJOR | `conclusions.tex:22–34` | Adapted: the CM1–GCM gap left the section and Yang et al.'s comparison moved to P2, so P3 runs from the ranking through the curved air, moved in as Appendix A proposed, and the gas fits to cloud as a calibration. Same paragraph as F14–F18 and evidence 5–7, 21–23 |
| F5 | MAJOR | `conclusions.tex:36–49` | Accepted: "Some of those Earth-fitted laws can be tested apart from any one world, in laboratories on Earth or in runs at other gravities"; the drop limits moved to P5. Same paragraph as F2, F6, F13 and evidence 2, 3, 8, 9 |
| F6 | MAJOR | `conclusions.tex:46–49` | Accepted: the freezing levels given to "six Morrison runs" and the flash density to "the main electrified run, forced from the Earth-orbit state", with "part of the difference possibly from its grid"; the cloud tops left out. Same passage as evidence 2 and 9 |
| F7 | MAJOR | `conclusions.tex:51–57` | Accepted: the maxim removed, P5 opened on "Gravity stays fixed in a laboratory on Earth, and a model's dependence on it is tested by similarity runs" and given the drop limits, the curved air moved to P3; the rewrite's wind-tunnel link left out. Same paragraph as F19 and evidence 10, 11, 24–26 |
| F8 | MAJOR | `conclusions.tex:59–69` | In part: the restated introduction and the record sentence removed, "By one design's own models" restored, the day tied to the tidal lock, and a last sentence added on cloud as each world's calibration, as in the abstract; the slow-rotator sentence still restates `next.tex:35–42` (e89a394, 71–74; round 3, prose M1 c), and the new last sentence states the method for "any new world" (round 3, prose B1). Same paragraph as F20 and evidence 4, 12–14, 27–29 |
| F9 | MAJOR | `reach.tex:47` | Accepted: "Worlds near the existing fits." Same passage as evidence 30 |
| F10 | MAJOR | `reach.tex:50–53` | Accepted, with evidence 16 and 17's insolation range and fixed orbit: "ExoPlaSim needs its general repairs, its fixed-orbit setting and its released radiation, ... while its cloud keeps Slingo's fit to Earth's convection and PlaSim's Earth-tuned thresholds". Same passage as evidence 16 and 17 |
| F11 | MINOR | `conclusions.tex:11` | Accepted: "Two of the three". Same passage as F3 and evidence 1 |
| F12 | MINOR | `conclusions.tex:11–13` | In part: the premise corrected, "At any instant the sunlight a latitude circle receives depends on the Sun's declination and distance alone", and checked by round 3's evidence reviewer; the deduction still stands in the conclusion alone (e89a394, 14–16), with `assumptions.tex` unchanged, and the author's confirmation is unrecorded. Same passage as evidence 19 |
| F13 | MINOR | `conclusions.tex:36–37` | Accepted, with evidence 8's leakage: "In two windows of an earlier electrified run, made before the ventilation repair and with leakage off". Same passage as evidence 8 |
| F14 | MINOR | `conclusions.tex:28` | Adapted: the comparison moved to P2, opening "Models can agree in their global means and still disagree widely in where cloud lies", and "as well" went. Same passage as evidence 5 and 23 |
| F15 | MINOR | `conclusions.tex:26` | Moot: the CM1–GCM comparison left the section; the 3.7 K and its attribution stay in Results. Same passage as evidence 7 and 22 |
| F16 | MINOR | `conclusions.tex:30–32` | In part: "outright" removed and temperatures added in the conclusion ("on any column whose gases, pressures and temperatures that spectroscopy covers"); `next.tex:16` keeps "gases and pressures", and the author's confirmation of the temperature bound is unrecorded. Same passage as evidence 6 |
| F17 | MINOR | `conclusions.tex:22` | Accepted: "By the global-mean temperature, changes to the parts fitted to Earth's atmosphere moved the test world furthest". Same passage as evidence 21 |
| F18 | MINOR | `conclusions.tex:33` | Accepted: "Cloud amount stays a calibration for each world, fitted to cloud-resolving runs of that world" |
| F19 | MINOR | `conclusions.tex:51–54` | In part: the verb and its object corrected, "reproduces a sixfold gravity scaling of an Earth sea to 0.3% in wave height, where the released code missed it by 5.4%"; "what stays uncertain is Earth's empirical laws" still closes the list (e89a394, 54–58); met at 798f68b. Same passage as evidence 10, 24 and 25 |
| F20 | MINOR | `conclusions.tex:66–67` | Accepted, in evidence 29's form, with "two of the sidereal periods" and "with the released radiation"; `next.tex:37` changed with it. Same passage as evidence 14 and 29 |

## Evidence record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| 1 | BLOCKING | `conclusions.tex:11–20` | Accepted: claim G17 and a Results sentence entered for the two-year test; the arriving sunlight's global mean is now stated as kept, and the test reported, "the test world ran 0.9 K warmer while still gaining heat"; the settled +0.6 K stays in Results. Same passage as prose F3, F11, F12 and evidence 19, 20 |
| 2 | BLOCKING | `conclusions.tex:46–49` | Accepted: the six Morrison runs and the main electrified run told apart, with the run's forcing and grid; the cloud tops and the charge's arrangement left out. Same passage as prose F6 and evidence 9 |
| 3 | BLOCKING | `conclusions.tex:41–44` | Accepted: "a box forced from the Earth-orbit state", "against 57–73% in the rings", and a run with scaled limits that "would measure how much of that evaporation the small drops cause". Same passage as prose F2 and evidence 7 |
| 4 | BLOCKING | `conclusions.tex:60–62` | Accepted: "so that gravity, column and the air's height against the radius depart from Earth's together, and the Moon's tidal lock adds a 29.53-day day". Same passage as prose F8 and evidence 12 |
| 5 | MAJOR | `conclusions.tex:28–30` | Adapted: moved to P2, opening "Models can agree in their global means and still disagree widely in where cloud lies", the runs named as Yang et al.'s and the alike global-mean temperatures and albedos added; "where cloud lies" was raised again in round 3 (evidence 8). Same passage as prose F14 and evidence 23 |
| 6 | MAJOR | `conclusions.tex:30–32` | Accepted as proposed: "would replace the radiation's gas fits, the largest of them, ... and the cloud optics would remain fits". Same passage as prose F16 |
| 7 | MAJOR | `conclusions.tex:27–28` and `42–43` | Accepted at 42–43, "a box forced from the Earth-orbit state"; the quarter-of-the-rain clause at 27–28 went with the CM1–GCM comparison. Same passages as prose F2, F15 and evidence 3, 22 |
| 8 | MAJOR | `conclusions.tex:36–38` | Accepted as proposed, with "within the spread of the Saunders and Peck runs". Same passage as prose F13 |
| 9 | MAJOR | `conclusions.tex:48–49` | Accepted: "electrified storms resolved at other gravities, computed with the same laboratory charging laws, could test those flash-rate laws", with Sergeev et al.'s route cited. Same passage as prose F6 and evidence 2 |
| 10 | MAJOR | `conclusions.tex:51–54` | In part: the test's scope added, "as tested at a sixth of Earth's gravity on the code paths those tests ran"; "what stays uncertain is Earth's empirical laws" still presents the laws as all that remains (e89a394, 54–58); met at 798f68b. Same passage as prose F7, F19 and evidence 24, 25 |
| 11 | MAJOR | `conclusions.tex:55–57` | Accepted, now in P3: "Titan's haze, with a scale height of about 80 km, stands a few hundredths of the radius tall, as the test world's air does, and plane-parallel aerosol codes for Titan's surface hold to about 65° from the zenith". Same paragraph as prose F7 |
| 12 | MAJOR | `conclusions.tex:60–61` | Accepted: "By one design's own models, a shield in space that removes the ultraviolet heating the upper air would keep Earth-like air on the Moon for tens of billions of years"; "by one design's own models" also entered the abstract, where the record's observation found the same form. Same passage as prose F8 and evidence 4 |
| 13 | MAJOR | `conclusions.tex:62–63` | Moot: the sentence went; P1 now reads "Three of the defects, all in ExoPlaSim". Same passage as prose F8 |
| 14 | MAJOR | `conclusions.tex:66–69` | Accepted: "would test its Sun-clock and convective-cover repairs there"; Next steps changed with it (e89a394, `next.tex:38–40`). Same passage as prose F8, F20 and evidence 29 |
| 15 | MAJOR | `reach.tex:48–49` | Accepted as proposed. Same sentence as evidence 30 |
| 16 | MAJOR | `reach.tex:50–53` | Accepted, with prose F10's cloud clause: "near Earth's insolation, such as the cooler runs", and "their warmer runs, at up to 2.9 times Earth's insolation, lie beyond the radiation's fits". Same passage as prose F10 and evidence 17 |
| 17 | MAJOR | `reach.tex:52` | Accepted: "its fixed-orbit setting". Same passage as prose F10 and evidence 16 |
| 18 | MINOR | `conclusions.tex:7–8` | Accepted as proposed |
| 19 | MINOR | `conclusions.tex:11–13` | Accepted: "At any instant the sunlight a latitude circle receives depends on the Sun's declination and distance alone, so the Sun clock ... keeps every zonal mean of the arriving sunlight". Same passage as prose F12 and evidence 1 |
| 20 | MINOR | `conclusions.tex:19–20` | Accepted, the record's alternative: "An error of this kind leaves a check of the arriving sunlight's global mean unchanged". Same passage as prose F3 and evidence 1 |
| 21 | MINOR | `conclusions.tex:22–24` | Accepted: "at least 20 K", in the abstract as well; Results' ranking (e89a394, `results.tex:93`) kept "more than 20 K" until 798f68b. Same passage as prose F17 |
| 22 | MINOR | `conclusions.tex:25–27` | Moot: the CM1–GCM comparison left the section; Results keeps it. Same passage as prose F15 and evidence 7 |
| 23 | MINOR | `conclusions.tex:29` | Accepted: "quasi-global", in the conclusion and at `results.tex:80`. Same passage as prose F14 and evidence 5 |
| 24 | MINOR | `conclusions.tex:51` | Moot: the maxim went (prose F7); its closed list returned in the SWAN sentence (finding 10). Same passage as prose F7 and evidence 10 |
| 25 | MINOR | `conclusions.tex:51–52` | Accepted: "to 0.3%", in the abstract as well. Same passage as prose F19 and evidence 10 |
| 26 | MINOR | `conclusions.tex:54–55` | Accepted: "whose air in curved shells loses a net 5.8 W m⁻² against the same clear column taken flat". Same paragraph as prose F7 |
| 27 | MINOR | `conclusions.tex:63–65` | Accepted: the CM1 README's classes now match Table repairs (patch 05 a general repair; 06–07 a general repair and a setting; 08 a coupling and a general repair); the conclusion's sentence on the record went. Same paragraph as prose F8 |
| 28 | MINOR | `conclusions.tex:65–66` | Accepted: "Away from Earth's values every change made for the test world has run on it alone." Same paragraph as prose F8 |
| 29 | MINOR | `conclusions.tex:66–67` | Accepted as proposed; `next.tex:37` changed with it. Same passage as prose F20 and evidence 14 |
| 30 | MINOR | `reach.tex:47–48` | Accepted: "the four models are built to simulate". Same passage as prose F9 and evidence 15 |

## Open after this round

- Prose F1: passages restating Results and Next steps (e89a394, `conclusions.tex:41–46`, `58–63`, `71–74`), the
  unwritten turn from P2's global means to P3's ranking, and the wind-tunnel link.
- Prose F3: the check sentence restates P2's opening (e89a394, `conclusions.tex:20–22`); met at 798f68b.
- Prose F8: the slow-rotator sentence restates Next steps (e89a394, `conclusions.tex:71–74`).
- Prose F12: the zonal-mean deduction stands in the conclusion alone (e89a394, `conclusions.tex:14–16`), and the
  author's confirmation is unrecorded.
- Prose F16: `next.tex:16` bounds the spectroscopy by "gases and pressures", and the author's confirmation of the
  temperature bound is unrecorded.
- Prose F19 and evidence 10: "what stays uncertain is" closes SWAN's list of uncertainties (e89a394,
  `conclusions.tex:54–58`); met at 798f68b.

Of the six uncounted observations, five were acted on in e89a394 (the reach sentence at `reach.tex:43–45`,
`next.tex:37`, `results.tex:80`, and the abstract's 0.3%, 20 K and design state); the Figure 1 caption's "solar days
of 16, 64 and 243 days" (`worlds.tex:24`) stands as it was.
