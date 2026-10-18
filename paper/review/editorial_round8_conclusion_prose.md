# Editorial review, round 8: Discussion and conclusions, the abstract and revised passages (prose)

## 1. Record

| Item | Entry |
|---|---|
| Reviewer | A fresh Claude subagent, Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), reading alone. It had seen no earlier review of the paper. Under `paper/review/` it wrote this file and opened nothing else; it left `paper/notes/` unopened. |
| Date | 2026-10-18 |
| Snapshot | Commit 44d67d4 (`44d67d4007c8e4add08f5527605b4f82b5bdb5d3`). Every paper file was read with `git show 44d67d4:<path>`, through copies in `/tmp/claude-1000/r8prose_snap/`. The working tree's HEAD at the time of writing was 4d1032e, a later commit, left unread. |
| Kind of reading | Each paragraph read whole, then sentence by sentence, under the ten passes of the charter's section 11 and the rules of AGENTS.md "Writing", with the author's direction of 2026-10-17 for the closing section as the governing test. Cadence was read silently; the read-aloud pass that the charter's G3 requires for conclusions remains pending. |
| Screening | A grep for "not", "rather than", other negations, stock signposts and self-reference over the scope, reported as screening only. `paper/tools/lint.py` was left unrun. |
| Number check | Each number in the conclusion was checked against the body (results, assumptions, reach, verification, next steps, the appendix tables). Two literature statements appear only in the conclusion (l.72–74, the 20% agreement of the capillary-length form and the premise on collisions, cited to Loftus and Wordsworth) and were checked against the citation's presence alone. `paper/claims.json` and the cited sources lay outside this reading; source fidelity is judged against the paper's own statements of its sources. |

**Files in scope** (sha256 at 44d67d4):

| File | sha256 | Scope |
|---|---|---|
| `paper/sections/conclusions.tex` | `1708e8f4b973ec9cb7e5c25524f434cdcec3ef1c5e379f8cde06c923807d3bfa` | whole section |
| `paper/sections/abstract.tex` | `b9c375c2a30787f5aa386a1489da713c5951ceecc3d31f555b2cf8785d27c45f` | whole abstract |
| `paper/sections/results.tex` | `8b7858fa769f410f4a5a67d61d4d8ec249decbfc0eb397b17d7d4a9a0178ee59` | l.44–52, 91–97, 153–157, 159–165, each in its paragraph |
| `paper/sections/next.tex` | `516b8926c1079571364f25904618bfed47d8368dcd6f21d50c4de8368ca66c22` | l.9–17, 36–44, 79–89 |
| `paper/sections/reach.tex` | `fff8183910168eeb9ee837c8e5766ac0bea7f64b6e95e0d63b8cf821e26f5b63` | l.38–42 |
| `paper/sections/repairs.tex` | `c846dbbf4dbaf39ae194d7bb93a26204aaa1b12f4b24e7aa1accdd948b281102` | l.105–109 |
| `paper/sections/introduction.tex` | `9638d854622b6b7121279288a0c70542b1f61d5e25f92fd75bfb376a25556d54` | l.71–75 |
| `paper/sections/assumptions.tex` | `1d0dfd93ba3f0f454cdbd7e8964e64fcb66b49f9275056fa6b5f76a083d4bb0e` | l.90–95 |

**Rule files read in full** (sha256):

| File | sha256 |
|---|---|
| `AGENTS.md` (world-crafting, at 44d67d4, identical to the working tree) | `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32` |
| Terluna `ensemble/planning/Open_Moon_Editorial_Charter_control-01.md` | `aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0` (matches the aac4a4f2…0b0 that AGENTS.md records) |
| Terluna `ensemble/planning/source_controls/STYLE_NOTES.md` | `659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46` |
| Terluna `ensemble/planning/source_controls/Jewish_Papers_Updated_Style_Notes.md` | `18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab` |
| Terluna `ensemble/planning/source_controls/Agent_Working_State_Editorial_Gates.md` | `553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464` |

The Terluna files were read from the Terluna working tree at its HEAD, f03b839.

**Context read in full**, beyond the scope files above, all of which were read whole: `verification.tex` (`4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00`), `worlds.tex` (`453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112`), `appendix.tex` (`17abe050d20a86031b7f3b1e426afcca0050cb9928bdb6500d84850d73013bbc`), and the preamble and section order of `paper/main.tex` (`116d1a8ff0f25694a864c6d7d9d6922e5289e6e583f38c15eac07b81a06facd8`). Order of reading: the rule files, the abstract, the introduction, the conclusion, then the body.

## 2. Findings

Line numbers are those of the files at 44d67d4. Rewrites are in LaTeX, ready to paste; each was checked against the body passages named under it.

### Finding 1. MAJOR. `conclusions.tex:53–55`

- **Text.** "The flash-rate laws with which \textcite{braam2022lightning} and \textcite{sergeev2025lightning} estimated lightning on tidally locked planets were fitted to Earth's storms and set the rate from the upward flux of graupel and the column's ice water path or from the cloud-top height."
- **Rule.** Technical meaning survives editing; claims stay within their evidence (a statement about the literature says what the cited works did).
- **Why.** The sentence names the two studies, then the two laws in the same order, and a reader pairs them: Braam et al. with the graupel flux and ice water path, Sergeev et al. with the cloud-top height. Results gives the reverse (`results.tex:153–157`): the rate from the cloud-top height or, in Sergeev et al.'s storm-resolving runs, from the upward flux of graupel at −15 °C and the column's ice water path. Read in order, the next sentence's "the cloud-top law" then becomes Sergeev et al.'s.
- **Rewrite.** "The flash-rate laws with which \textcite{braam2022lightning} and \textcite{sergeev2025lightning} estimated lightning on tidally locked planets were fitted to Earth's storms and set the rate from the cloud-top height or, in Sergeev et al.'s storm-resolving runs, from the upward flux of graupel and the column's ice water path."
- **Check and length.** Against `results.tex:153–157`. Adds five words. The next sentence's "cloud tops" still finds "the cloud-top height" inside this sentence.

### Finding 2. MAJOR. `conclusions.tex:81–86`

- **Text.** "The changes that remove or avoid the three defects contain no coefficient fitted to the test world, and away from Earth's values the repaired codes have run on the test world alone, so the defects' biases on other worlds are known so far from the code's arithmetic. Runs of released and repaired ExoPlaSim on ozone-free Earth-air planets at Earth's insolation and zero obliquity and eccentricity, rotating once in 16 and 64 days, two of the sidereal periods of the ROCKE-3D runs of \textcite{way2018climates}, would measure their joint effect."
- **Rule.** Coordination joins only propositions of equal weight ("Sentences carry their dependencies"); a conclusion excludes reciting the inventory ("Conclusions and the arc"); the charter's pass 8 (redundancy).
- **Why.** The two clauses joined by "and" stand in a concessive relation: the changes are general by construction, and yet they have run on one world. This is the final paragraph's turn, from the calibrations, fitted on columns that a lower pressure or another shield would change (l.79–81), to repairs that contain no coefficient fitted to one world and whose effect elsewhere is known through arithmetic alone; with an "and", the reader has to make the turn. The second sentence then copies the reach test's configuration from `next.tex:37–39` nearly word for word, so in the paragraph that lands the paper the reader meets the next-steps list again, between the turn and the landing.
- **Rewrite.** "Although the changes that remove or avoid the three defects contain no coefficient fitted to the test world, away from Earth's values the repaired codes have run on the test world alone, so the defects' biases on other worlds are known from the code's arithmetic; runs of released and repaired ExoPlaSim on Earth-air planets rotating once in 16 and 64 days, two of the sidereal periods of the ROCKE-3D runs of \textcite{way2018climates}, would measure their joint effect."
- **Check and length.** Against `next.tex:36–44` (the runs, their periods, what the pair measures) and `reach.tex:16–24`. "Away from Earth's values" stays fronted, which keeps "run away" from reading as a phrasal verb. The full configuration stays in Next steps. Shortens the paragraph by about ten words.

### Finding 3. MINOR. `conclusions.tex:6–11`

- **Text.** "... an error that grows as a world's rotation slows or its day, tilt or eccentricity departs from Earth's." and "... and the Sun clock sets the Sun back about 33\textdegree\ each model day in a non-synchronous run of any planet rotating more slowly than once in 20 days, on the default solar geometry."
- **Rule.** Nouns and verbs are precise; cadence (a paragraph's stress falls on its last words).
- **Why.** "As a world's rotation slows" describes a rotation slowing in time, where the claim compares worlds that rotate at different rates. The paragraph then ends on the condition "on the default solar geometry", which takes the terminal stress from the consequence the paragraph builds toward, the slow rotators.
- **Rewrite.** "... an error that grows the more slowly a world rotates or the further its day, tilt or eccentricity departs from Earth's." and "... and, on the default solar geometry, the Sun clock sets the Sun back about 33\textdegree\ each model day in a non-synchronous run of any planet rotating more slowly than once in 20 days."
- **Check and length.** Against `assumptions.tex:102–107` and `reach.tex:17–19`. Adds two words.

### Finding 4. MINOR. `conclusions.tex:14–20`

- **Text.** "... the orbit default, which put Earth's tilt in place of the configured one, brought Earth's seasons and summer rain to 60\textdegree, and in a two-year test of the corrected Sun clock and tilt alone the share of land under half a millimetre of rain a day rose from 9 to 36\%. The moved sunlight changed the clouds, and through them the global means: in the same test the clouds' effect in sunlight weakened by 2.4~W\,m$^{-2}$, and the test world ran 0.9~K warmer while still gaining heat."
- **Rule.** Coordination joins only propositions of equal weight; inheritance.
- **Why.** The two-year test corrected both defects, and its result is coordinated into the orbit default's clause, so the dry land reads as the tilt's effect alone, and the next sentence has to recover the test with "in the same test". A sentence of its own for the test joins its two results, the dry land and the change in cloud, and the sentence on the clouds inherits the test directly.
- **Rewrite.** "... the orbit default, which put Earth's tilt in place of the configured one, brought Earth's seasons and summer rain to 60\textdegree. In a two-year test of the corrected Sun clock and tilt alone, the share of land under half a millimetre of rain a day rose from 9 to 36\%, and the moved sunlight changed the clouds and through them the global means: the clouds' effect in sunlight weakened by 2.4~W\,m$^{-2}$, and the test world ran 0.9~K warmer while still gaining heat."
- **Check and length.** Against `results.tex:46–52`. Shortens by three words. Optional, at l.14: "which errs in the Sun's longitude alone and so keeps every zonal mean of the arriving sunlight" writes the relation between the two predicates (one word more).

### Finding 5. MINOR. `conclusions.tex:23`

- **Text.** "Where two of the defects moved sunlight between places, changes to the parts fitted to Earth's atmosphere moved the test world's global-mean surface temperature furthest:"
- **Rule.** The relation goes into the syntax; cadence (openings).
- **Why.** "Where" means "whereas" here, and beside "between places" it first reads as a place: in the places where the defects moved sunlight. The section's first paragraph opens on "Where" in its conditional sense (l.3), so two paragraph openings use the word in two senses.
- **Rewrite.** "Whereas two of the defects moved sunlight between places, changes to the parts fitted to Earth's atmosphere moved the test world's global-mean surface temperature furthest:"
- **Check and length.** Two letters more.

### Finding 6. MINOR. `conclusions.tex:30–33`

- **Text.** "on Titan, whose haze has a scale height of about 80~km, three hundredths of its radius as for the test world's air, the plane-parallel codes that separate the surface from the haze hold to about 65\textdegree\ from the zenith \autocite{vincendon2010spherical}"
- **Rule.** Technical meaning survives editing; claims stay within their evidence, scoped to the cited work. The charter's G4 lists a technical qualification that vanishes in editing among its blocking failures.
- **Why.** `repairs.tex:106–109` gives Vincendon and Langevin's limits as typical values for remote-sensing codes ("hold typically to about 80\textdegree ... and to about 65\textdegree\ on Titan"). The conclusion states the Titan limit as a fixed property of the codes, so the two sections state the cited result with different scope. "As for the test world's air" also reads awkwardly.
- **Rewrite.** "on Titan, whose haze has a scale height of about 80~km, the same three hundredths of the radius as the test world's air, the plane-parallel codes that separate the surface from the haze hold typically to about 65\textdegree\ from the zenith \autocite{vincendon2010spherical}"
- **Check and length.** Against `repairs.tex:105–109` and the regime table (`worlds.tex:59`, scale height over radius 0.030). Adds three words. The evidence review can confirm "typically" against the source.

### Finding 7. MINOR. `conclusions.tex:33–35`

- **Text.** "The dynamical cores keep a thin shell in the GCM and a flat slab in CM1, both at constant gravity, an approximation whose effect on the test world's circulation is still to be measured."
- **Rule.** Inheritance and order (swap test); "Sentences carry their dependencies".
- **Why.** The author orders the paragraph's parts by how far a world's own column fixes them: the radiative geometry computed from the column, the gases and scattering from spectroscopy, the cloud by calibration. The sentence on the dynamics could go at several points in the paragraph, since its relation to the sentence before, the same geometry approximated in the dynamics where the radiation now computes it, stays unwritten.
- **Rewrite.** "The dynamical cores approximate the same geometry by a thin shell in the GCM and a flat slab in CM1, both at constant gravity, with an effect on the test world's circulation still to be measured."
- **Check and length.** Against `assumptions.tex:53–56` and `next.tex:51–58`. Adds two words.

### Finding 8. MINOR. `conclusions.tex:41–45`; `abstract.tex:25–26`

- **Text.** "Cloud amount would be a calibration for each world, fitted to cloud-resolving runs of that world. On two tidally locked planets in the comparison of \textcite{yang2023cloud}, cloud covered 82--97\% of the sky ..." and, in the abstract, "Cloud would be a calibration for each world, fitted to cloud-resolving runs, a fit still to be made on the test world."
- **Rule.** Nouns are precise; "Sentences carry their dependencies" (the evidentiary relation).
- **Why.** A cloud amount is a quantity and a calibration a procedure, so "cloud amount would be a calibration" names the wrong thing; what the plan states (`next.tex:21–26`) is that PlaSim's cloud settings would be calibrated. The sentence on Yang et al. then follows as a separate declarative, and its role, the evidence that two GCMs' parameterized cover exceeded the cloud-permitting runs' by a factor of two or more on two tidally locked planets, is left for the reader to supply; it could change places with the claim it supports, the swap test's sign of an unwritten relation.
- **Rewrite (conclusion).** "Cloud amount would be calibrated for each world against cloud-resolving runs of that world: on two tidally locked planets in the comparison of \textcite{yang2023cloud}, cloud covered 82--97\% of the sky in two GCMs whose cover follows relative humidity, stability and large-scale ascent, and 27 and 41\% in quasi-global cloud-permitting runs that count cloud by a condensate threshold, over sea surfaces fixed from a coarser run of the same model, while the planetary albedos lay 2 to 11 points apart."
- **Rewrite (abstract).** "Cloud would be calibrated for each world against cloud-resolving runs, a fit still to be made on the test world."
- **Check and length.** Against `results.tex:91–97` and `next.tex:19–26`. Each shortens by two words.

### Finding 9. MINOR. `conclusions.tex:35–38`; `abstract.tex:22–25`; `next.tex:14–17`

- **Text.** Conclusion: "A scheme built from the reference's line-by-line spectroscopy would replace ... under the starlight the scheme is built for". Abstract: "A radiation scheme built from the in-house model's line-by-line spectroscopy would replace ... under the starlight it is built for". Next steps: "... would hold on columns within the gases, pressures and temperatures of the check, under the starlight its shortwave is built for".
- **Rule.** A proposed design and a runnable calculation are different evidence states (File and evidence practice); technical meaning.
- **Why.** "Would replace" marks the scheme as proposed, and "is built for" describes it as existing, so the evidence state shifts inside one sentence, in three places. Next steps (`next.tex:14`) presents the scheme as a step to come.
- **Rewrite.** "under the starlight it would be built for" (abstract); "under the starlight the scheme would be built for" (conclusion); "under the starlight its shortwave would be built for" (next steps). If the scheme is instead the existing correlated-$k$ emulation, naming it settles the state.
- **Check and length.** Against `next.tex:13–17` and `repairs.tex:121–126`. One word more in each place. The author knows which state holds.

### Finding 10. MINOR. `conclusions.tex:68–70`, `74–75` (with l.35, 41, 46, 84)

- **Text.** "For CM1 the test is still to be made: the pair of runs designed to measure how far its convection, with gravity-scaled microphysics, departs from Earth's convection stretched sixfold failed to convect." and "Runs with Morrison's limits scaled by the capillary length would therefore bound how much of the lunar rain's evaporation its small drops cause, a step still to run."
- **Rule.** Cadence (repeated frames); a qualification attaches once to the claim it bounds; redundancy.
- **Why.** Statements of pending work recur through the section: "is still to be measured" (l.35), "is planned" (l.41), "is still to be made" (l.46), "is still to be made" (l.68), "a step still to run" (l.75), "so far" (l.84). Each is accurate; read together they form a refrain, and the reader meets the next-steps list again inside the discussion, in the section the author wants to excite the reader. Two go with no loss of evidence state: at l.75 the conditional "would therefore bound" already marks the runs as unmade, and at l.68 the sentence on the failed pair already says that CM1's test is outstanding. Finding 2 removes "so far" at l.84.
- **Rewrite.** "For CM1 the pair of runs designed to measure how far its convection, with gravity-scaled microphysics, departs from Earth's convection stretched sixfold failed to convect." and "Runs with Morrison's limits scaled by the capillary length would therefore bound how much of the lunar rain's evaporation its small drops cause."
- **Check and length.** Against `verification.tex:51–52` and `next.tex:72–74`. Shortens by eleven words.

### Finding 11. MINOR, optional, adds length. `conclusions.tex:70–75` and `86–90`

- **Text.** "Morrison's drop-size limits in CM1 stay Earth's, while the largest raindrop that survives its fall scales with the capillary length, ..." and the landing, "... a second model whose own drop and charging laws would in turn need laboratory tests at the conditions of its storms."
- **Rule.** Write for the expert (a sentence stays where it supplies a premise the reader lacks); a conclusion gathers the developed lines.
- **Why.** The fifth paragraph ends on a bound to "how much of the lunar rain's evaporation its small drops cause" and omits the result the bound concerns: in a box forced from the GCM, 85% of the water falling from the clouds evaporated on the way down, and the ground received about a quarter of the GCM's rain (`results.tex:122–125`). That result, the rain half of the gap between the two models, is absent from the section, and it is the paper's own evidence that the second model's laws matter, the premise of the final sentence. The landing then states a need for laboratory tests of the drop laws, where the fifth paragraph offers runs that bound their effect; the step between, that the collisions which set the largest drops on Earth are what a laboratory would test at lunar fall speeds, stays unwritten.
- **Rewrite (a), the premise, about thirty words more.** "Morrison's drop-size limits in CM1 stay Earth's: under them, 85\% of the water falling from the clouds of a box forced from the GCM evaporated on the way down, and the ground received about a quarter of the GCM's rain. The largest raindrop that survives its fall scales with the capillary length, 2.46 times longer at a sixth of Earth's gravity: ..."
- **Rewrite (b), the landing, one of two.** Either the fifth paragraph ends on the laboratory step, if the author holds it: "... would therefore bound how much of the lunar rain's evaporation its small drops cause, and the collisions that set the largest drops would remain for a laboratory to measure at lunar fall speeds." Or the landing keeps to what the body states: "... a second model whose drop limits were set for Earth's rain and whose charging laws would in turn need laboratory tests at the conditions of its storms."
- **Check and length.** (a) against `results.tex:122–125` (34 mm against 129 mm; 85% evaporated) and `next.tex:70–77`; (b) against `assumptions.tex:87–90` and `next.tex:79–85`. The first option of (b) adds a proposal the body lacks and needs the author's judgement.

### Finding 12. MINOR. `abstract.tex:10–12`; `introduction.tex:73–75`

- **Text.** Abstract: "the released codes also hold five defects, and by ExoPlaSim's own arithmetic three of them, with little or no error at Earth's values, bias its runs that meet their conditions, slowly rotating and tidally locked planets among them." Introduction: "The released codes also hold five defects, three of which produce little or no error at Earth's values and, by ExoPlaSim's own arithmetic, bias its runs that meet their conditions, slowly rotating and tidally locked planets among them."
- **Rule.** Nouns are precise; exact action.
- **Why.** "Planets among them" makes planets members of a set of runs. "Hold" gives the codes a verb of possession where "contain" names the relation.
- **Rewrite.** "... the released codes also contain five defects, ... bias its runs that meet their conditions, runs of slowly rotating and tidally locked planets among them." The same two changes in the introduction.
- **Check and length.** Against `reach.tex:16–24`. Two words more in each.

### Finding 13. MINOR. `results.tex:47–48`

- **Text.** "... and the land receiving under 0.5~mm per day grew from 9 to 42\%, 36\% within two years of the Sun and tilt alone:"
- **Rule.** "Sentences carry their dependencies"; technical meaning (which run gave which number).
- **Why.** "36\% within two years of the Sun and tilt alone" compresses a separate test into an appositive whose head is unclear; it can read as the four-change run itself, two years after the Sun and tilt changed. The next sentence names the test ("in a two-year test of the two alone"), and this clause can name it the same way.
- **Rewrite.** "... and the land receiving under 0.5~mm per day grew from 9 to 42\%, and to 36\% in a two-year test of the Sun and tilt alone:"
- **Check and length.** Against `results.tex:49–52` and `conclusions.tex:17–18`. Four words more.

### Finding 14. MINOR. `results.tex:91–99`

- **Text.** "In the comparison of \textcite{yang2023cloud}, two GCMs that parameterize their cover, as PlaSim does, covered far more of the sky than a quasi-global cloud-permitting model on two tidally locked planets, TRAPPIST-1e and K2-72e: ... The planetary albedos lay closer, ... and the authors judged the three models' climates broadly similar. Given the reference's spectroscopy, the test world's climate is least certain in its cloud amount ..."
- **Rule.** Inheritance (each sentence receives something from the one before); swap test; competing findings are integrated where their premises enter (charter G4).
- **Why.** The comparison follows the ranking of effects by form with "as PlaSim does" as its only link, and it could follow the paragraph's last sentence with little loss. Its concession, the albedos closer and the climates judged broadly similar, comes next to the landing's claim that the test world's climate is least certain in its cloud amount, with the relation between them unstated: the landing's basis is the test world's own cloud tests (up to about 6 K), and the comparison measures how far parameterized cover departs from resolved cover on two other worlds.
- **Rewrite.** Opening: "\textcite{yang2023cloud} compared the cover of two GCMs that parameterize it, as PlaSim does, with resolved cloud on two tidally locked planets, TRAPPIST-1e and K2-72e: CAM3 covered 94.8 and 81.7\% of the sky and ExoCAM 90.4 and 97.4\%, their cover following relative humidity, stability and large-scale ascent, against 26.9 and 41.1\% in a quasi-global cloud-permitting model, which counts cloud by a condensate threshold and ran over sea surfaces fixed from a coarser run of the same model." Landing, optional: "Given the reference's spectroscopy and these tests, the test world's climate is least certain in its cloud amount ..."
- **Check and length.** Against the numbers in `results.tex:91–97`. The opening names the authors and their operation and shortens by about five words; the optional landing adds three.

### Finding 15. MINOR. `results.tex:159`

- **Text.** "Two of the storm results depend on choices that a measurement or a theory could settle."
- **Rule.** A paragraph's opening promise is kept by the paragraph; claims stay within their evidence.
- **Why.** The paragraph closes the first result on laboratory laws that disagree, which implies the measurement, and the second on a factor of two between microphysics schemes, for which it names neither a measurement nor a theory. The opening promises routes to settling both; Next steps names the first, and the second stays unnamed.
- **Rewrite.** "Two of the storm results depend on the choice of a law or a scheme." If the author holds a route for the fog, naming it keeps the original opening.
- **Check and length.** Against `results.tex:159–168` and `next.tex:79–85`. Shortens by two words.

### Finding 16. MINOR. `next.tex:14–15`

- **Text.** "a reduced correlated-$k$ scheme built from the reference model's own spectroscopy in place of Sasamori's and Lacis and Hansen's fits would replace it"
- **Rule.** Say what is (negative contrasts judged by meaning); redundancy.
- **Why.** "In place of" and "would replace" state the replacement twice, once as a contrast; the positive form names everything replaced once.
- **Rewrite.** "a reduced correlated-$k$ scheme built from the reference model's own spectroscopy would replace it together with Sasamori's and Lacis and Hansen's fits"
- **Check and length.** Same length.

### Finding 17. MINOR. `next.tex:85–89`

- **Text.** "The windows leave the sign of the ground strikes under Takahashi's law undecided, since their strikes under both laws, all negative, carried charge left over from a run without leakage. A leader model of the descent from the $-7$\,\textdegree C level, 27--34~km up, to the ground would replace the bound on ground strikes, now between none and a fifth of flashes, with a rate, and with it the number of strikes, each lowering a median 149~C, that the ground receives."
- **Rule.** Exact action (an abstraction that "leaves" a sign undecided); negation stays only where the proposition requires it; "Sentences carry their dependencies".
- **Why.** The windows, spans of a run, take an agent's verb. "Without leakage" has a positive form the paragraph already uses (l.81, "with leakage off"). In the last sentence, "and with it the number of strikes ... that the ground receives" has no verb of its own and reads as a second object of "replace".
- **Rewrite.** "In the windows the sign of the ground strikes under Takahashi's law stays open: their strikes under both laws, all negative, carried charge left over from a run with leakage off. A leader model of the descent from the $-7$\,\textdegree C level, 27--34~km up, to the ground would replace the bound on ground strikes, now between none and a fifth of flashes, with a rate, and from the rate would follow the number of strikes the ground receives, each lowering a median 149~C."
- **Check and length.** Against `next.tex:79–84` and `results.tex:150–151`. Three words more.

## 3. What works

**The author's direction.**

- Every sentence of the conclusion that concerns another world keeps to its evidence. Titan enters through Vincendon and Langevin's limit and the adapted models' lack of its radiation (l.30–33); the gas scheme is bounded by its composition, its starlight and the range where its spectroscopy agrees with an independent code (l.35–38), and the next sentence gives the checks made and the one planned (l.38–41); the wave patch is "built to keep the scaling at any gravity" and "tested at a sixth of Earth's on the code paths those tests ran" (l.66–67); the defects' biases elsewhere come "by the code's own arithmetic" (l.8); the storms are "the model's lunar storms" (l.52–53). The abstract states the bound once, early: "the only world the repaired codes have run on away from Earth's values".
- Each paragraph after the first develops a consequence the body leaves implicit: defects that keep the global mean of the arriving sunlight and still move the climate through cloud, found in maps by longitude and by season (l.13–21); the dependence of what a modeller of another world needs on how far that world's own column fixes each part, which orders the third paragraph from computed geometry through spectroscopy to calibrated cloud (l.29–46); lightning laws traced back to a laboratory measurement at stated impact speeds, cloud water and temperatures, and forward to a comparison between models at each gravity (l.48–62); gravity consistency as a property of code, set against empirical laws fitted on Earth (l.64–75); and a constructed world whose design was set with the model, and so with the Earth fits left in it (l.77–81). These meet the author's test, "real substance of discussion".
- The landing (l.86–90) gathers the third, fourth and fifth paragraphs into one chain of evidence for another world, from the GCM's fits through line-by-line spectroscopy and cloud-resolving runs to laboratory tests of the second model's own laws. The relation is stated only in the conclusion, and it ends on the field's next consequential work, as the charter's section 11 requires of a companion paper's ending.
- Exoplanet and natural-world consequences enter as findings, with no "this means that": TRAPPIST-1e's convective cover, the Sun of slow rotators, Titan's haze, Yang et al.'s tidally locked planets, Braam et al.'s and Sergeev et al.'s lightning, Way et al.'s rotation periods.
- The opening paragraph and the third give the paper's answers to the introduction's two questions (`introduction.tex:44`), where a model's Earth values lie and which repairs made for one world hold on another, so the reader receives the reminder the author asks for in the form of answers.

**The rules, by pass** (the charter's section 11):

| Pass | Result |
|---|---|
| 1. Equal-weight declaratives | Sentences subordinate their dependencies; two coordinations of unequal propositions (Findings 2, 4). |
| 2. Inheritance | Paragraph boundaries inherit from the subject: the defects that moved sunlight (P2 to P3), CM1's Earth-fitted microphysics and its laboratory charging laws (P3 to P4), "a comparison between models at each gravity" and gravity consistency as a property of the code (P4 to P5). Two sentences enter with their link unwritten (Findings 7, 14). |
| 3. Swap test | Findings 7, 8, 14. The fourth and fifth paragraphs could trade places with small loss; the fourth's landing prepares the fifth's opening, which gives the present order its reason. |
| 4. Exact action | Agents act: the code adds and sets back, the runs flashed, the cloud tops rose, the modeller finds. One agent's verb on an abstraction and one imprecise noun (Findings 17, 8). |
| 5. Living presence | The modeller (l.20, 29), the cited authors by name, and the storms, rain and drops stay visible. |
| 6. Transitions | Subject-generated throughout; no stock signpost. One opening reads two ways (Finding 5). |
| 7. Defensive structure | No objection catalogue, disclaimer or pre-emptive hedge; qualifications attach once ("with a correction fitted at 295~K", "pushed to the ends of their tests", "made before the ventilation repair and with leakage off", "part of the difference possibly from its grid"). The pending-work refrain (Finding 10). |
| 8. Redundancy | Findings 2, 10, 16; the second paragraph and the ranking at l.23–28 restate results number for number (judgement below). |
| 9. Cadence, silent | Openings vary; hinges at l.20, 29, 48 and 64. The first and last paragraphs run on long sentences alone. Findings 3, 5, 10. Audible pass pending. |
| 10. Final-page arc | Holds: see below. |

**Screening.** The grep found neither "not" nor "rather than" in the conclusion, the abstract or the revised passages, and reading confirmed it. The negations that remain state propositions that need them: "no coefficient fitted", "lack Titan's nitrogen–methane radiation", "failed to convect", "where observations are lacking", "in place of the breakup of single drops", and in Next steps "none" as a lower bound (Finding 17 takes up one "without"). No witticism, rhetorical question, stock signpost or self-reference appears in the scope; headings name their subjects.

**Numbers.** Every number in the conclusion matches the body, apart from the two literature statements at l.72–74 noted in the record: 0.23, 33° and 20 days (`reach.tex`); the cap of 0.8, 17% and 8%, 2.46 (`assumptions.tex`); 60°, 9 to 36%, 2.4 W m⁻², 0.9 K, at least 20 K, 11.5 K, about 6 K, 1.6–2.5 K, six runs, 55–80 km and a hundredth (`results.tex`); 82–97%, 27 and 41% and 2 to 11 points, each derived from the values in `results.tex:93–96`; 80 km and 65° (`repairs.tex`); optical depth 1.5, 0.3% and 5.4% (`verification.tex`); 4–8 m s⁻¹, 0.02–0.2 g m⁻³, −5 to −16 °C, 16 and 64 days (`next.tex`); 295 K and 5.0 to 3.0% (`results.tex`, `worlds.tex`).

**Arc.** The introduction's two questions are where a model's Earth values lie and which repairs made for one world hold on another; the conclusion's opening paragraph states the answer to the first, and its third and last paragraphs the answer to the second; the abstract's last two sentences, the bounded scheme and cloud calibrated for each world, promise the first two links of the landing. The landing's third link, the second model's own laws, and the design set with the model have no counterpart in the abstract. A clause on each would cost about twenty words and is the author's choice; the abstract would then land where the conclusion lands, on what a modeller of another world needs beyond the GCM.

**Revised passages, each read in its paragraph.**

- `results.tex:44–49` names the four changes of one step with the class of each in a single sentence and explains the dry land by Earth's tilt after a colon; the classes agree with Table `tab:repairs` (Finding 13 for one appositive).
- `results.tex:153–157` attributes the flash-rate laws correctly and ends its paragraph on the lunar tops beyond the laws' fitted range, which prepares the conclusion's fourth paragraph.
- `results.tex:159–165` states the windows' conditions (days, before the ventilation repair, leakage off) and draws the dependence on the laboratory laws with "therefore" (Finding 15 for the opening).
- `next.tex:9–13` names both outcomes of the refit and the design consequence of each, as the charter's G5 requires of a proposed study (Findings 9, 16 for the last sentence).
- `next.tex:36–44` maps each run to what it measures and states the reclassification that would follow a failed repair, a full question-to-test mapping.
- `next.tex:79–85` gives the measurement's impact speeds, cloud water and temperatures and the reason the ground strikes' sign stays open; its heading names the arrangement of charge (Finding 17 for the wording).
- `reach.tex:38–42` separates what the wave models are built to do from what has been tested, on which code paths and with which laws.
- `repairs.tex:105–109` scopes Vincendon and Langevin's limits as typical values and ends its paragraph on the evidence from natural worlds.
- `introduction.tex:71–75` gives the forms and the defects sentences of their own (Finding 12 for two words).
- `assumptions.tex:90–95` names the charging laws as laboratory laws and ties the turn of the storms' arrangement of charge to them, in agreement with `results.tex` and `next.tex`.

## 4. Counts and judgement

**Counts.** BLOCKING 0. MAJOR 2 (Findings 1, 2). MINOR 15 (Findings 3–17).

**Length.** Findings 2, 4, 8, 10, 14 (opening) and 15 shorten the text; Findings 1, 3, 6, 7, 9, 12, 13 and 17 add one to five words each; Findings 5 and 16 keep the length; Finding 11 adds about thirty words if its first part is taken.

**Judgement.** The section meets the author's direction. It reminds the reader of the paper's answers to the introduction's two questions and develops real discussion: defects that keep the global mean of the sunlight yet change the climate through cloud, a dependence of each part's needs on how far a world's own column fixes it, lightning laws traced to a laboratory measurement and to a comparison between models, code consistency set against Earth's empirical laws, a constructed world whose design was set with the model, and a closing chain of evidence that ends in laboratory tests. Every sentence about another world keeps to its evidence, so the section suggests no reach to untested kinds of world. The two MAJOR findings are local and quick to repair: in the flash-rate sentence a reader pairs a law with the wrong study (Finding 1), and in the final paragraph the concession is written as an "and" and the next step's configuration is copied in (Finding 2). The section excites least in three places, where the text restates results number for number or repeats its pending work: the second paragraph, the ranking that opens the third, and the six tags of work still to be done (Findings 4, 10). With those repaired and the two unwritten links written (Findings 7, 8), the reader would meet the discussion lines, already present, at the centre of their paragraphs.
