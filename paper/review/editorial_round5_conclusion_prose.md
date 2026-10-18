# Editorial review, round 5: the closing section, the abstract and the revised passages (prose)

## 1. Record

| Item | Value |
|---|---|
| Reviewer | A fresh Claude subagent, Claude Opus 5.5 (`claude-opus-5-5[1m]`), reading the paper for the first time |
| Date | 2026-10-17 |
| Snapshot | commit `11026a8` (`11026a8860933914ab13c2b10dd9494d97555938`); every file read with `git show 11026a8:<path>` |
| Kind of review | Reading review of prose under AGENTS.md "Writing" and the charter's ten passes, with checks of technical meaning where a sentence's claim rests on the body |
| Cadence | Silent reading; no audible reading was made |

**Files in scope**

| File | Scope | sha256 at 11026a8 |
|---|---|---|
| paper/sections/conclusions.tex | whole section | 4d12601bc67f62add60c6e605d745c4e8d3c6db582ecfde8620112089113aee0 |
| paper/sections/abstract.tex | whole abstract | 8bbd11720dd47a835b8f7c512b601d554cf5c2aa81ba3c68cbc536dda811a075 |
| paper/sections/results.tex | :44–46 (the phrase at :45), :81–86, :90–94, :151–154, each read in its paragraph | 115b663dc4579b31fb47ec5d5b5f4fc50231f00e262e597bc7481de1908d86c7 |
| paper/sections/reach.tex | :38–41, :47–60, caption :90–93, Seas row :114 | af628ab20664ca3b40972ec320c7f75a04373f5fa3c4e4b22a3ab6e4af8e3c7d |
| paper/sections/next.tex | :35–43 | 650228e9ab643a80b519d9e14c42f86bedb76d00a9ad79b3eaa88ab326d6c5d0 |
| paper/sections/assumptions.tex | :21–26, read in its paragraph :13–34 | c57415f24ad79e207d0e87c773db69f7f1ace96640e4edd0a0738d648d534682 |

The hashes of conclusions.tex and abstract.tex match those in the brief.

**Rule files read in full**

| File | sha256 |
|---|---|
| AGENTS.md (world-crafting, at 11026a8; the working copy is identical) | e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32 |
| terluna: ensemble/planning/Open_Moon_Editorial_Charter_control-01.md | aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0 |
| terluna: ensemble/planning/source_controls/STYLE_NOTES.md | 659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46 |
| terluna: ensemble/planning/source_controls/Jewish_Papers_Updated_Style_Notes.md | 18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab |
| terluna: ensemble/planning/source_controls/Agent_Working_State_Editorial_Gates.md | 553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464 |

Terluna stood at commit f03b839 when read; the charter's hash matches the one AGENTS.md cites.

**Context read**

| File | How | sha256 at 11026a8 |
|---|---|---|
| paper/sections/introduction.tex | in full, with the abstract, before the conclusion | b8325d641b56d6da32cffbcaa143e26461495322235c2de3b0709402f1ef5b72 |
| paper/sections/results.tex, reach.tex, next.tex, assumptions.tex | in full | above |
| paper/sections/verification.tex | in full | 4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00 |
| paper/sections/worlds.tex | in full | 453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112 |
| paper/sections/repairs.tex | in full | bb1d22c01616fdaf454280acded56316b7995af2a8fc3bb5a255af52c92e793c |
| paper/sections/appendix.tex | the configuration and change tables | ebab8ca204f81ed41d9185d456353a43a9f59e5307290695277b4614b5bd6635 |
| paper/main.tex | section order | 7ef8255c7fa8d14e9d0d61406d1f919be6dff5251b47fb3598aba9c913a8495c |
| paper/claims.json | records H04, H07, H11, H21, H23, H24, R04, R05, V04, V06, V16, G01, G02, G04, G05, G09, G10, G14, G16, G17, W03–W06, N01, N03, S07, S15 | 8bb7e9e6cf2010e75be6f6890357c0238798bc27ab9c2b7412cb61ab8507e8e1 |
| paper/sources/manifest.json | locators for vincendon2010spherical, yang2023cloud, way2018climates, yang2014strong, braam2022lightning, sergeev2025lightning | 334f5973fe6339026237ca7953369c34e5f4a1cce89ef935bccd7ccfa76a66a4 |
| models/swan/README.md | the rows on source terms and avoided options (:210–211), for finding 16 | 3699e5e564fa484d36b1aa6c91434ab8119beeb3a50de8f72625db97476f8d3f |
| terluna: climate/waves/first_experiments.md | lines 25–45, to check "up to 5.4%" in the abstract and conclusion (the stock code's 5.44% is a maximum, so "up to" holds) | 959868b935ca29c3b4f3f929c987036627f81c884064e4f5887e1a29ec60b2a5 |

paper/review/ (apart from this record) and paper/notes/ stayed closed.

**Screening.** `paper/tools/lint.py` (sha256 27f9b47a1f4837583b75eb750e302531f3e07a44e452983dd9ddce2b35657367), run on copies of the snapshot files in a scratch directory outside the repository, found no "not" and no "rather than" in the conclusion or the abstract; it listed three negative contrasts, one possible empty action and 13 universal words in the conclusion, and each was read below. These counts are screening only.

**Order of the paper** (main.tex): abstract, introduction, worlds, Earth values and defects, repairs, verification, results, reach, next steps, discussion and conclusions, appendix. The conclusion follows Next steps, so the reader meets a step repeated in the conclusion a page or two after its full statement.

**Method.** Each paragraph was read whole, then sentence by sentence, under the ten passes of the charter's section 11 and the rules of AGENTS.md "Writing", and against the author's direction for the closing section: remind and excite; real discussion; no untested world presented as within reach; findings for exoplanets and constructed worlds drawn out without explaining the obvious; natural-world implications stated implicitly. Each rewrite below was checked against the body sentence its claim rests on, and the finding names that check.

## 2. Findings

### 1. BLOCKING — the landing claims test routes that the section's own paragraphs rule out

- **Location.** conclusions.tex:82–84; the confusion starts at :46–47.
- **Text.** "cloud remains to be calibrated for each such world, against cloud-resolving runs whose laws of drops and charge remain Earth fits until laboratories and runs at other gravities test them." At :46–47: "Some of those Earth-fitted laws can be tested independently of the world modelled, in laboratories on Earth or in runs at other gravities."
- **Rule.** Technical meaning survives editing; claims stay within their evidence; a conclusion gathers the developed lines into a new relation (charter G5 and section 11).
- **Why.** The section's last clause promises that laboratories and runs at other gravities will test the cloud-resolving runs' laws of drops and charge. Three passages of the paper say otherwise. (a) The paragraph just before ends (:66–69) on the drop-size dependence as "beyond what a laboratory on Earth or a similarity run can test". (b) At :57–59 the runs at other gravities are computed "with the same laboratory charging laws" and test another set of laws, the flash-rate laws of the GCM studies; a run that computes with a law leaves that law untested. (c) verification.tex:11–13: "a similarity test runs Earth's empirical laws at the scaled gravity with their Earth coefficients, which it leaves untested there." Of the routes the clause names, only laboratory tests of the charging laws survive these passages (:47–51). The clause also ties "charge" to the cloud calibration, whose target is cloud cover and cloud water by pressure (next.tex:21–22), while the charging laws set the sign of the lightning (results.tex:156–161). The last sentence therefore gathers P4 and P5 into a relation that both contradict, and an expert reader meets the contradiction on the last line before the appendix. The root lies at :46–47, where "those Earth-fitted laws" points to the cloud-resolving runs' own microphysics (:44) and the runs at other gravities of :57–59 test laws outside those runs.
- **Rewrite** (about the same length; finding 3 gives a fuller rewrite of the whole sentence that includes this one): "cloud remains to be calibrated for each such world, against cloud-resolving runs whose drop-size limits stay Earth's and whose lightning takes its sign from charging laws that Earth's laboratories can test." Checked against :47–51 (a laboratory measurement decides the polarity), :66–67 (the drop-size limits stay Earth's), results.tex:156–161 and next.tex:21–22.
  At :46–47 (same length): "Some Earth-fitted laws of storms can be tested independently of the world modelled, in laboratories on Earth or against storms resolved at other gravities." Checked against :47–51 (charging laws, laboratories) and :57–59 (flash-rate laws, resolved storms).

### 2. MAJOR — a claim about what any laboratory can test

- **Location.** conclusions.tex:66–69.
- **Text.** "its drop-size limits stay Earth's while the largest raindrop that survives its fall scales with the capillary length, 2.46 times longer at a sixth of Earth's gravity, a dependence beyond what a laboratory on Earth or a similarity run can test."
- **Rule.** Claims stay within their evidence: each universal claim is checked against what was examined (AGENTS.md "Writing"; charter G5).
- **Why.** The appositive rules out every laboratory test. The paper examined no laboratory method, and a cloud physicist can name candidates: the capillary length $\sqrt{\sigma/\rho_w g}$ varies with surface tension and density as well as with gravity, so liquids of other $\sigma/\rho$ probe the same dependence at Earth's gravity, and drop towers and partial-gravity flights vary $g$ itself. The similarity half of the claim agrees with verification.tex:11–13. The appositive also takes the paragraph's terminal stress, and finding 1's contradiction starts there.
- **Rewrite** (two words shorter): "…2.46 times longer at a sixth of Earth's gravity, a dependence that a similarity run, holding the limits at their Earth values, leaves untested." Checked against verification.tex:11–13 and next.tex:71–73, where limits scaled with the capillary length enter as a sensitivity run.

### 3. MAJOR — the landing restates the third paragraph

- **Location.** conclusions.tex:79–84, against :34–36 and :40–44.
- **Text.** Landing: "the radiative geometry can be computed from the world's own column as it was from the test world's, and, once a scheme is built from the reference's spectroscopy and checked against an independent code, the gas absorption as well; cloud remains to be calibrated for each such world, against cloud-resolving runs …". P3: "The radiative geometry of tall air is computed from that column, as the curved-air table was for the test world"; "A scheme built from the reference's line-by-line spectroscopy would replace the radiation's gas fits, … for air of nitrogen and oxygen with water and modest carbon dioxide, once that spectroscopy has been checked against an independent code"; "Cloud amount would stay a calibration for each world, to be fitted to cloud-resolving runs of that world; … those runs compute with Earth-fitted microphysics of their own."
- **Rule.** Conclusions and the arc: a conclusion gathers the developed lines into a new relation, and restating them is excluded; redundancy pass (charter section 11, pass 8).
- **Why.** Clause for clause the landing repeats P3: the composition, the geometry computed from the column as for the test world, the scheme from the reference's spectroscopy under the same check, and cloud calibrated for each world against cloud-resolving runs with Earth-fitted laws. It adds two things, the bound on scale height over radius and the clause on testability (finding 1). The author rejected an earlier conclusion as a summary; the section now ends on a summary of its own third paragraph, three paragraphs on.
- **Rewrite** (about ten words shorter; includes finding 1). The landing returns to the modeller whom P3 introduced at :33 ("What a modeller of a new world needs") and turns P3's gradient into that modeller's three operations, ending on the Earth that remains: "A modeller of a new world of nitrogen--oxygen air with water and modest carbon dioxide, whose scale height is at most three hundredths of its radius, the test world's ratio, would compute its radiative geometry from its own column, its gas absorption from the reference's spectroscopy once a scheme is built and the spectroscopy checked, and fit its cloud scheme to cloud-resolving runs whose drop-size limits stay Earth's and whose lightning takes its sign from charging laws that Earth's laboratories can test." Checked: "would" keeps the evidence state (one curved-air table computed, the scheme unbuilt, the cloud fit unmade); the two conditions on the gas absorption are those of :40–42; the cloud optics stay with P3 (:42–43); the last clause is finding 1's. P3 stays as written, since its last clause gives P4 its antecedent.

### 4. MAJOR — Results: a landing whose relation to its paragraph is unwritten

- **Location.** results.tex:151–154, the last sentence of "Storms and lightning".
- **Text.** "\textcite{braam2022lightning} and \textcite{sergeev2025lightning} estimated lightning on tidally locked planets with Earth-like air from laws fitted to Earth's storms, which set the flash rate from the cloud-top height or, in Sergeev et al.'s storm-resolving runs, from the upward flux of graupel and the ice aloft."
- **Rule.** Inheritance and order: a paragraph's last sentence completes its movement or sets up the next paragraph; sentences carry their dependencies (charter G1 and G3).
- **Why.** The paragraph moves from the lunar storms' heights (tops at 55–80 km) through the charge to the flash rate and the grid. The last sentence turns to two other studies and stops at what they did, and the next paragraph turns to the charging laws. The relation between the lunar storms and those laws, which the conclusion draws at :54–55 ("far above the storms the cloud-top law was fitted on"), is missing where Results reports the evidence for it.
- **Rewrite** (about nine words longer): "\textcite{braam2022lightning} and \textcite{sergeev2025lightning} estimated lightning on tidally locked planets with Earth-like air from laws fitted to Earth's storms, whose tops stand far below the lunar runs' 55--80~km, setting the flash rate from the cloud-top height or, in Sergeev et al.'s storm-resolving runs, from the upward flux of graupel and the ice aloft." Checked against results.tex:141–142 (claim G09). With this in Results, conclusions.tex:51–54 can shorten (finding 8).

### 5. MINOR — P2's last sentence: a restated implication, a late attribution and a new detail at the landing

- **Location.** conclusions.tex:20–26.
- **Text.** "A modeller finds such an error in maps of sunlight by longitude and of rain by season, where a check of the arriving sunlight's global mean passes it, and a comparison by global-mean temperature and albedo can pass large differences in cloud: on two tidally locked planets, three models came out broadly alike in global-mean surface temperature and albedo by their authors' account, while the quasi-global cloud-permitting runs of \textcite{yang2023cloud} covered 27 and 41\% … covered 82--97\%, the largest differences on the night side and at high latitudes of the day side."
- **Rule.** Write for the expert (delete test; an implication the evidence already makes plain); claims within their evidence; paragraph landings.
- **Why.** (a) :13–14 says that two of the defects "kept the global mean of the sunlight arriving at the top of the air", so "where a check of the arriving sunlight's global mean passes it" restates it. (b) "by their authors' account" comes before the reader learns who the authors are. (c) The detail on the night side and high latitudes appears nowhere in results.tex:81–86, and the source manifest gives no locator for it; it also takes the paragraph's terminal stress from its point, that models can agree in global means while their cloud differs widely.
- **Rewrite** (about 25 words shorter): "A modeller finds such an error in maps of sunlight by longitude and of rain by season, and a comparison by global-mean temperature and albedo can pass large differences in cloud: in the comparison of \textcite{yang2023cloud} on two tidally locked planets, three models came out broadly alike in global-mean surface temperature and albedo, while their cloud cover came to 27 and 41\% in the quasi-global cloud-permitting runs and 82--97\% in two GCMs whose cover follows relative humidity, stability and large-scale ascent." Checked against results.tex:81–86 and the manifest's locators for yang2023cloud (26.9 and 41.1%; 94.8, 81.7, 90.4 and 97.4%).

### 6. MINOR — the Titan sentence brings in a world outside the models, then excludes it

- **Location.** conclusions.tex:37–40.
- **Text.** "Titan's haze, with a scale height of about 80~km, stands a few hundredths of its radius tall, as the test world's air does, and the plane-parallel codes that separate Titan's surface from its haze hold to about 65\textdegree\ from the zenith \autocite{vincendon2010spherical}, although Titan's nitrogen--methane radiation lies outside the adapted models."
- **Rule.** Inheritance and order (swap test); claims within their evidence.
- **Why.** P3 runs a gradient from the parts the column fixes to the parts it leaves open: geometry (:34–37), gas absorption (:40–43), cloud (:43–44). The Titan sentence stands between the first two steps and can trade places with the gas sentence without loss, so its relation to the gradient is unwritten. Its "although" clause is needed only because the sentence names a world outside the adapted models. The 80 km haze scale height is new to the paper and has no record in claims.json; the manifest's locator for Vincendon and Langevin covers the 65° and Titan's "larger relative scale height". repairs.tex:106–108 already gives the 65° figure.
- **Rewrite** (about 50 words shorter): delete the sentence, so that P3 passes from the curved-air table to the gas scheme. If the author keeps it for its natural-world link, the 80 km figure needs a claim record and the "although" clause stays.

### 7. MINOR — P4: an unwritten contrast, and storms that test

- **Location.** conclusions.tex:54–59.
- **Text.** "…rose to 55--80~km, far above the storms the cloud-top law was fitted on, and the main electrified run, …, flashed at about a hundredth of Earth's average flash density, …. Electrified storms resolved at other gravities, computed with the same laboratory charging laws, could test those flash-rate laws, along the route Sergeev et al. propose of explicit charging in cloud-resolving runs."
- **Rule.** Sentences carry their dependencies; exact action.
- **Why.** "and" joins a fitted law's predictor far out of its range with a resolved flash rate far below Earth's; the relation is a contrast, and "while" writes it without claiming what the cloud-top law would predict. In the next sentence the testing is done by modellers who resolve storms, and "the route … of explicit charging" separates "route" from its complement.
- **Rewrite** (same length): "…far above the storms the cloud-top law was fitted on, while the main electrified run, forced from the Earth-orbit state and computing its flashes from resolved charge, flashed at about a hundredth of Earth's average flash density, part of the difference possibly from its grid. Resolving electrified storms at other gravities, with the same laboratory charging laws, could test those flash-rate laws, along the route Sergeev et al. propose: explicit charging in cloud-resolving runs."

### 8. MINOR — P4 repeats Next steps and Results word for word

- **Location.** conclusions.tex:49–51 against next.tex:79–81; conclusions.tex:51–54 against results.tex:151–154.
- **Rule.** Redundancy pass; a conclusion gathers the lines.
- **Why.** The measurement conditions ("4--8~m\,s$^{-1}$ in 0.02--0.2~g\,m$^{-3}$ of cloud water between $-5$ and $-16$\,\textdegree C") and the description of Braam et al.'s and Sergeev et al.'s laws appear in the same words a page or two earlier. The conclusion's claim needs the fact that laboratories reach the conditions; the numbers belong to Next steps.
- **Rewrite** (about 5 and about 25 words shorter): "a measurement of that sign at the impact speeds, cloud water and temperatures of the lunar storms, conditions laboratories reach, would decide which polarity the model's lunar lightning takes." With finding 4 taken: "The flash-rate laws with which \textcite{braam2022lightning} and \textcite{sergeev2025lightning} estimated lightning on tidally locked planets were fitted to Earth's storms." The next sentence names the cloud-top law. Checked against claim N01 (impact speeds of 4.4–7.6 m/s).

### 9. MINOR — P6: a correction that moves a dimming

- **Location.** conclusions.tex:73–75.
- **Text.** "A longwave correction refitted at the settled state, or cloud fitted to cloud-resolving runs, could move the dimming again, and a lower pressure or another shield would move the columns off those the calibrations were fitted on."
- **Rule.** Exact action.
- **Why.** The designers choose the dimming; a refitted correction changes the model's temperature at a given dimming, and with it the dimming that holds 295 K, as next.tex:11–13 states. The second "move" repeats the figure on the columns.
- **Rewrite** (same length): "With a longwave correction refitted at the settled state, or cloud fitted to cloud-resolving runs, the dimming that holds 295~K could change again, and a lower pressure or another shield would give columns other than those the calibrations were fitted on." Checked against next.tex:11–13 and :21–23.

### 10. MINOR — P6: the natural-planet sentence

- **Location.** conclusions.tex:75–79.
- **Text.** "On natural planets the three defects' biases are known so far from the code's arithmetic, since away from Earth's values every change made for the test world has run on it alone; released and repaired ExoPlaSim … would measure them on worlds that other studies model."
- **Rule.** The author's direction (natural-world implications stated implicitly); exact action; redundancy.
- **Why.** "On natural planets" names the implication outright, while the ROCKE-3D runs already place the test among natural planets. Models run, and changes run inside them; the abstract (:17) has the exact form, "the repaired codes have run". "on worlds that other studies model" repeats next.tex:38–39.
- **Rewrite** (about eight words shorter): "Away from Earth's values the repaired codes have run on the test world alone, so the three defects' biases on other worlds are known so far from the code's arithmetic; released and repaired ExoPlaSim on Earth-air planets rotating once in 16 and 64 days, as in two of the ROCKE-3D runs of \textcite{way2018climates}, would measure them." The new opening also inherits from :74–75, the columns off those fitted.

### 11. MINOR — two words in the conclusion

- **Location.** conclusions.tex:63 and :44.
- **Text.** "whose linear wind input bends at a fixed 1~Hz"; "on the test world that fit is a step still to run".
- **Rule.** Exact action; precise nouns.
- **Why.** "bends" names no operation: above the knee the code reduces the linear input (assumptions.tex:22). Runs are run and fits are made; the abstract (:22) has "a fit still to be made".
- **Rewrite.** "whose linear wind input is reduced above a fixed 1~Hz" (one word longer); "on the test world that fit is still to be made" (two words shorter).

### 12. MINOR — "a method computed"

- **Location.** conclusions.tex:6; abstract.tex:13.
- **Text.** "geometry took a method computed from the world's own column"; "the radiative geometry took a method computed for each world's column".
- **Rule.** Precise nouns; exact action.
- **Why.** The method stays the same from world to world; its table is computed from each world's column (repairs.tex:14–16).
- **Rewrite** (three words longer in each): "geometry took a method whose table is computed from the world's own column"; "the radiative geometry took a method whose table is computed for each world's column".

### 13. MINOR — abstract: the inventory sentence

- **Location.** abstract.tex:8–12.
- **Text.** "Their Earth values take four forms, constants, units of time, geometry, and fits and simplifications used beyond their range, beside five defects in the released codes; three of the defects, with little or no error at Earth's values, bias by the code's own arithmetic ExoPlaSim's runs of slowly rotating and tidally locked planets that meet their conditions."
- **Rule.** Sentences carry their dependencies; cadence.
- **Why.** The list stands in apposition with commas inside it, "beside" sets the defects next to the four forms as if they were a fifth, and "bias by the code's own arithmetic ExoPlaSim's runs" puts a long adverbial between the verb and its object.
- **Rewrite** (three words longer): "Their Earth values take four forms: constants, units of time, geometry, and fits and simplifications used beyond their range; the released codes also hold five defects, and by the code's own arithmetic three of them, with little or no error at Earth's values, bias ExoPlaSim's runs of slowly rotating and tidally locked planets that meet their conditions." Checked against introduction.tex:70–75, which uses the same order.

### 14. MINOR — abstract: the last sentence drops a condition the conclusion keeps

- **Location.** abstract.tex:20–22.
- **Text.** "A radiation scheme built from line-by-line spectroscopy would replace the largest fits with physics computed for each world's nitrogen--oxygen air, while cloud would remain a calibration …"
- **Rule.** Technical meaning survives editing; the abstract and the conclusion land on the same claim (pass 10).
- **Why.** The conclusion conditions the scheme on a check of the reference's spectroscopy against an independent code (:42, :81–82), and verification.tex:68–69 records that the reference's carbon dioxide, oxygen, collision-induced absorption and sunlight await that comparison. The abstract states the claim without the condition, so the two ends of the arc land on claims of different strength.
- **Rewrite** (five words longer): "A radiation scheme built from line-by-line spectroscopy checked against an independent code would replace the largest fits with physics computed for each world's nitrogen--oxygen air, …"

### 15. MINOR — Results: "Ranked by form" lists out of rank

- **Location.** results.tex:90–94.
- **Text.** "…while the geometry's curved-air terms, on the table's first channels, moved it by 0.65~K and the general repairs of units and constants measured singly by 1.6--2.5~K."
- **Rule.** Inheritance and order: a sentence that announces a ranking follows it.
- **Why.** After the fits (at least 20 K; up to about 6 K) the sentence gives the geometry's 0.65 K before the general repairs' 1.6–2.5 K.
- **Rewrite** (same length): "…by up to about 6~K, while the general repairs of units and constants, measured singly, moved it by 1.6--2.5~K and the geometry's curved-air terms, on the table's first channels, by 0.65~K."

### 16. MINOR — reach: options outside the configuration read as part of it

- **Location.** reach.tex:38–41 (and :34–35).
- **Text.** "In the configuration used, SWAN and SWASH are built to run water seas at any gravity …; SWAN's ST6 drag, exact quadruplets and bottom friction, and SWASH's rotation, keep Earth's constants."
- **Rule.** Technical meaning; sentences carry their dependencies.
- **Why.** The semicolon clause leaves its relation to "the configuration used" open, so a reader may count those parts among it. models/swan/README.md:210–211 places them outside it (ST6 and exact quadruplets avoided; bottom friction off by default). The row of unselected options in Table tab:inventory (assumptions.tex:212) lists ST6, exact transfer and SWASH's rotation and has no entry for bottom friction. "In the configuration used" also comes twice in five lines (:34, :38).
- **Rewrite** (three words longer): "…with Earth's empirical laws; SWAN's ST6 drag, exact quadruplets and bottom friction, and SWASH's rotation, all outside that configuration, keep Earth's constants." The author may add bottom friction to the inventory's row of unselected options.

### 17. MINOR — Next steps: forty-odd words of subject before the verb

- **Location.** next.tex:36–43.
- **Text.** "Released and repaired ExoPlaSim on Earth-air planets at Earth's insolation and zero obliquity and eccentricity, rotating once in 16 and 64 days, two of the sidereal periods of the ROCKE-3D runs of \textcite{way2018climates}, with the released radiation, fitted on columns like theirs, would measure …"; "would be reclassed".
- **Rule.** Cadence (charter G3); precise words.
- **Why.** The reader carries the planets, the periods, the source and the radiation through about 45 words before reaching "would measure". "reclassified" is the standard form.
- **Rewrite** (about four words longer): "Released and repaired ExoPlaSim would be run on Earth-air planets at Earth's insolation and zero obliquity and eccentricity, rotating once in 16 and 64 days, two of the sidereal periods of the ROCKE-3D runs of \textcite{way2018climates}, with the released radiation, fitted on columns like theirs: the pair would measure the three defects' effect on worlds that other studies model; …", and "would be reclassified".

### 18. MINOR — assumptions: gravity that fixes a knee

- **Location.** assumptions.tex:21–26.
- **Text.** "As a frequency it fixes at 1~Hz the knee above which SWAN reduces its linear wind input, … because the knee stays put while gravity changes, …; with that linear input switched on, a sea at any gravity other than Earth's, the ancient seas of Mars among them, departs through that constant from the scaled image of an Earth sea …"
- **Rule.** Exact action; precise nouns.
- **Why.** SWAN's authors fixed the knee, and Earth's gravity enters through its value; "it fixes" gives the act to gravity. "stays put" falls outside the paper's register. The sea that departs through a code's constant is SWAN's sea.
- **Rewrite** (about four words longer): "As a frequency it is written into SWAN as the 1~Hz knee above which the code reduces its linear wind input, a value its source comments call largely arbitrary, and because the knee stays at 1~Hz while gravity changes, stock SWAN misses a sixfold gravity-similarity test by 5.44\% in significant wave height; with that linear input switched on, SWAN's sea at any gravity other than Earth's, the ancient seas of Mars among them, departs through that constant from the scaled image of an Earth sea wherever its frequency band reaches past the scaled knee."

**Outside scope.** models/swan/README.md:211 reads "Terluna avoided these options rather than patching them"; AGENTS.md's writing rules govern READMEs, and the sentence uses an excluded phrase.

## 3. What works

- **The plan.** Each paragraph turns on a claim for the field, and the transitions come from the subject: P3 opens on "Where two of the defects moved sunlight between places", P4 on "Some of those Earth-fitted laws", P5 on gravity that stays fixed in a laboratory, after P4's laboratories. Several of Next steps' items return as consequences, in an order the argument sets, and the paragraphs pass the swap test apart from P3's Titan sentence (finding 6) and P6's third sentence (finding 10).
- **Remind.** P1 gathers the four forms, the five defects and the rule that repairs followed form in 172 words, and ends on two numbers for real targets, TRAPPIST-1e and any non-synchronous planet slower than 20 days, given "by the code's own arithmetic".
- **Discussion of substance.** P2 builds a causal chain from the test world (sunlight moved with its global mean kept, the clouds changed, the global mean followed) to a point for comparisons of exoplanet models, scoped to Yang et al.'s study. P3's hinge, "What a modeller of a new world needs for each part depends on how far the world's own column determines it", is the section's governing claim, and the mood of its verbs records the evidence: "is computed" for the geometry method that exists, "would replace" and "would stay" for the scheme and the calibration still to come. P4 turns from the Earth-fitted microphysics to a laboratory measurement that "would decide which polarity the model's lunar lightning takes", scoped to the model. P6:71–75 draws the constructed-world consequence, a design set with the model's fits, and leaves its implication to the reader.
- **Excite.** The forward pull comes from P4, a measurement on Earth and resolved storms at other gravities as tests of laws that exoplanet studies use, and from P6's design point. Findings 1–3 concern the landing that should gather them.
- **Reach.** No sentence in scope presents an untested world as within reach. The nearest candidates hold: the defect numbers for TRAPPIST-1e and slow rotators are code arithmetic; "can be computed" in the landing names the capability of a method that exists; the gas scheme is conditional and conditioned; the Titan sentence excludes Titan (finding 6 proposes cutting it); reach.tex:51–57 says what ExoPlaSim "would need" for slow rotators, keeps cloud as Earth fits "of a process through which those studies found the climate to change with rotation", and records that the runs "have yet to be made".
- **Rules checked by reading.** In scope there is no "not" or "rather than", no self-reference, stock signpost, rhetorical question, witticism or promotional word; the negations stand where their propositions need them ("failed to convect", "remains untested", "little or no error").
- **Abstract.** It runs from the hazard (a run that keeps an Earth value completes with a plausible result) through constructed worlds' further reach ("by one design's own models"), the inventory and the repair classes, to the evidence state ("the only world the repaired codes have run on away from Earth's values") and lands on the radiation scheme and the cloud fit "still to be made". The abstract, the introduction's last paragraph and the conclusion land on the same contribution.
- **Revised passages.** results.tex:81–86 scopes the cloud comparison to Yang et al.'s study and ties it to PlaSim's diagnosed cover. results.tex:45, "a step that joined a general repair and an avoidance with a calibration", marks the 0.6 K as a joint effect of three classes, which the figure and the ranking need. reach.tex:38–41 keeps "built to" apart from "have been tested". In reach.tex:47–60 the first sentence bounds the test world under other dimmings by the residuals and checks of each fit, and the slow-rotator sentence lists needs, keeps cloud as the open Earth fit and records the runs as unmade. The caption of Table tab:reach states that the third column gives "the reach each repair was built for" and that the test world is "the only world the adapted models have simulated", and the Seas row agrees with it. next.tex:35–43 names what the test measures, what each output discriminates and the result that would narrow the table (charter G5). assumptions.tex:21–26 ties the knee to the linear input and makes the Mars clause conditional on that input.

## 4. Counts and judgement

| Severity | Count | Findings |
|---|---:|---|
| BLOCKING | 1 | 1 |
| MAJOR | 3 | 2, 3, 4 |
| MINOR | 14 | 5–18 |

Of the 18 findings, 1–3 and 5–12 concern the conclusion, 12–14 the abstract, 4 and 15 Results, 16 reach, 17 Next steps and 18 the assumptions section. The rewrites in findings 4, 11 (first part), 12, 13, 14, 16, 17 and 18 add a few words each; the rest keep or cut length, and taken together the conclusion's rewrites shorten it by about 125 words if finding 6's deletion is taken.

The section meets the author's direction in its plan and in most of its substance. It reminds the reader of the four forms, the five defects and the rule that repairs followed form, then develops consequences that a modeller of exoplanets or constructed worlds can use: errors that pass a check of global means, a gradient from geometry computed from the column through gas absorption computable from checked spectroscopy to cloud that stays a calibration, Earth-fitted laws that laboratories and resolved storms can test, and a constructed world's design set with the model's own fits. Natural-world implications enter mostly through named cases, and no sentence presents an untested world as within reach. The section falls short in its landing: its last clause promises laboratory and other-gravity tests of the cloud-resolving runs' laws of drops and charge that P4, P5 and the verification section rule out (finding 1), after a claim about laboratories that exceeds what the paper examined (finding 2), and most of the last sentence restates P3 (finding 3). With those three repaired, the conclusion would end on the Earth that remains in a new world's cloud and on the laboratory measurements that can test part of it, a landing that gathers P3 to P5; findings 5–10 would lighten the re-quoted numbers that still give parts of P2 and P4 the feel of a summary.
