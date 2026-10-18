# Editorial round 7: prose review of "Discussion and conclusions", the abstract and the revised passages

## 1. Record

- Reviewer: a fresh Claude subagent, Claude Opus 5.5 (model id `claude-opus-5-5[1m]`), launched for this round. It
  saw no earlier review record. Its only contact with `paper/review/` was a filename listing to confirm that this
  record's path was free; it opened no file there and none under `paper/notes/`.
- Date: 2026-10-17; the record was completed at 00:01 EDT on 2026-10-18.
- Snapshot: commit 654ebdf (654ebdfd42989247f0639e0549c0a637c5927c37). Every file was read with
  `git show 654ebdf:<path>`. Nothing in the repository was changed apart from this record; scratch copies went to
  `/tmp/claude-1000/r7prose_work/`.
- Kind of reading: silent. Each paragraph was read whole, then sentence by sentence, under the ten passes of the
  charter's section 11 and the rules in AGENTS.md "Writing". No audible reading was made, so the read-aloud
  requirement for the conclusion and the major transitions stays pending.

Files in scope, sha256 at 654ebdf:

| File | sha256 | Scope |
|---|---|---|
| paper/sections/conclusions.tex | 30e4558960694cf815e0d9a4dc6ef4d5526651524553ef1aba5f36da26abbb0f | whole section |
| paper/sections/abstract.tex | 5a013c5fcebe028beceaf3a9421919f19503851b531363301c6f9033154acb36 | whole abstract |
| paper/sections/results.tex | ad92675e8c2d2a15beb6fa522da464dcd77ad8f260f883042658f4d2928b8e43 | lines 44–48, 90–96, 152–156, each read in its paragraph |
| paper/sections/reach.tex | de4c7f47235170d6f3a78db67d1d63ee3299b36a15f1682d818e450aff516551 | lines 38–42; Table tab:reach, Seas row (line 114) |
| paper/sections/next.tex | a68a6c3ab3a3a7d0374993c2d92e9cbb4a18a92cbe1a6f451d995ab32d5ba84d | lines 13–17, 36–44, 79–85 |
| paper/sections/repairs.tex | 2d5eb8d77bb2525244b3610a68d6554183ee7fe463310e7f6af37357f00240f0 | lines 106–109 |
| paper/sections/introduction.tex | 095321a4347073d02caf526e522cde34caf58d2c56ef30378114ae819484df60 | read in full; lines 71–75 in scope |

Also read in full, as context: worlds.tex (453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112),
assumptions.tex (4c2d7f99690986359955e327fe1ef9f1bc317c026da45221c032d59df8e81fd0), verification.tex
(4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00), and results, reach, next and repairs whole;
main.tex for the section order. To check numbers and attributions: paper/claims.json
(6b4718a2be6128506d693a87cdcc2753194d0d8d39cce9c0a9038ed490f0cfb8; entries H07, H23, H24, W03, W06, G01, G02,
G05, G09, G10, G11, G14, G17, V04, V06, V16, N01, R07) and paper/sources/manifest.json
(194f4261f8ef39960eb7140ba3a06c4cea9c2a44a12ad1031bc7750c6803988f; the entries for Vincendon and Langevin 2010,
Yang et al. 2023, Way et al. 2018, Braam et al. 2022, Sergeev et al. 2025 and Loftus and Wordsworth 2021).

Rule files, read in full before the paper:

| File | sha256 |
|---|---|
| AGENTS.md (world-crafting, at 654ebdf) | e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32 |
| terluna `ensemble/planning/Open_Moon_Editorial_Charter_control-01.md` | aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0 |
| terluna `ensemble/planning/source_controls/STYLE_NOTES.md` | 659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46 |
| terluna `ensemble/planning/source_controls/Jewish_Papers_Updated_Style_Notes.md` | 18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab |
| terluna `ensemble/planning/source_controls/Agent_Working_State_Editorial_Gates.md` | 553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464 |

Terluna's working tree stood at commit f03b839 when read; the charter's hash matches the one AGENTS.md gives
(aac4a4f2…0b0).

Screening: `paper/tools/lint.py`, taken from 654ebdf and run on copies of the two in-scope files, returned four
negative-contrast hits and ten universal-claim hits. Each was read. The negations ("no coefficient fitted",
"little or no error") are required by their propositions, and the universals ("any planet rotating more slowly",
"every zonal mean", "each world", "any gravity") hold by the code's arithmetic or state a design intent. Neither
file uses "not" or "rather than". The lint output is screening only; the findings come from reading.

Checks made:

- The conclusion's numbers were checked against Results, Assumptions, Verification and the claim register, and
  all agree: 0.23 for TRAPPIST-1e, 33° a model day above 20 days, 17% and 8% on the equator, 9 to 36%,
  2.4 W m⁻², 0.9 K, at least 20 K, 11.5 K, about 6 K, 1.6–2.5 K, 55–80 km, about a hundredth, 0.3% and 5.4%,
  2.46, 5.0 to 3.0%.
- Vincendon and Langevin's 65° for Titan, 80° for Mars and the 80 km haze scale height, and Loftus and Wordsworth's
  "within about 20%", have located quotes in the manifest.

Checks left undone:

- The manifest lists no locators for Braam et al. (2022) or Sergeev et al. (2025), both at admission DEFERRED, so
  the attributions at conclusions.tex:50–53 and 56–58 and results.tex:152–156, among them "the route Sergeev et al.
  propose", went unchecked against located passages. That check belongs to the evidence review.
- No source original was opened, no PDF was built and no page was inspected.

## 2. Findings

Every rewrite was checked against the rules (no "not" or "rather than", no empty action, the claim's numbers,
conditions, scope and evidence state kept) and against the sections cited in the finding. Line numbers are at
654ebdf.

### Finding 1. MAJOR. abstract.tex:21–25. The gas scheme's bound reads as a check already made

Text: "A radiation scheme built from the reference's line-by-line spectroscopy would replace the largest of these
fits for nitrogen--oxygen air with water and modest carbon dioxide over the pressures and temperatures where an
independent code has checked that spectroscopy, while cloud would be a calibration for each world, ..."

Rule: claims stay within their evidence; evidence states stay distinct, and future work is never marked complete
(File and evidence practice); G5.

Why: "where an independent code has checked that spectroscopy" presupposes a check of the named air's
spectroscopy. Verification (verification.tex:63–69) and claim V16 record two checks against other codes, PyRADS
for water-only longwave at constant gravity and a Monte Carlo Rayleigh calculation to optical depth 1.5, and
record that carbon dioxide, oxygen, collision-induced absorption and sunlight on the lunar column have yet to be
compared; next.tex:28–34 plans that comparison on the design column. The conclusion states the status ("a check
so far planned on the design column alone", conclusions.tex:41). Read alone, the abstract leaves the reader
taking the spectroscopy of nitrogen–oxygen air with carbon dioxide as independently checked. next.tex:15–17
states the same bound most clearly: "once that spectroscopy is checked".

Rewrite (adds 7 words, and also repairs Finding 13): "A radiation scheme built from the in-house model's
line-by-line spectroscopy would replace the largest of these fits for nitrogen--oxygen air with water and modest
carbon dioxide over the pressures and temperatures where that spectroscopy agrees with an independent code, a
comparison planned on one column of the test world, while cloud would be a calibration for each world, fitted to
cloud-resolving runs, a fit still to be made on the test world."

### Finding 2. MAJOR. conclusions.tex:83–86. The landing counts CM1's runs as evidence from outside the adapted codes

Text: "The fits, which moved the test world's climate furthest, would be refitted or replaced on another world from
evidence outside the adapted codes: the gas fits from line-by-line spectroscopy checked against an independent
code, the cloud from cloud-resolving runs of that world, and the drop and charging laws inside those runs from
laboratory tests."

Rule: technical meaning survives editing; claims stay within their evidence.

Why: CM1 is one of the four adapted codes, and the paper's plan fits PlaSim's cloud to CM1's runs
(next.tex:19–26). The same section calls tuning on resolved storms "a comparison between models at each gravity"
(lines 59–60) and says the cloud-resolving runs "compute with Earth-fitted microphysics of their own" (43–44);
the landing then classes those runs as outside evidence. The chain the sentence builds holds once each fit's
evidence lies beyond the code that contains the fit: the GCM's fits come from spectroscopy and from the
cloud-resolving model, and that model's own laws come from the laboratory. Stated so, the landing keeps its
force, since the chain ends in measurement.

Rewrite (adds 3 words): "The fits, which moved the test world's climate furthest, would each be refitted or
replaced on another world from evidence beyond its own code: the GCM's gas fits from line-by-line spectroscopy
checked against an independent code, its cloud from cloud-resolving runs of that world, and the drop and
charging laws inside those runs from laboratory tests."

### Finding 3. MAJOR. conclusions.tex:20–25. The "since" clause gives a reason unrelated to the maps it explains, and the paragraph lands on another subject

Text: "A modeller finds such an error in maps of sunlight by longitude and of rain by season, since global means
can differ far less than cloud cover does. In the comparison of \textcite{yang2023cloud} on two tidally locked
planets, cloud covered 82--97\% of the sky in two GCMs ..., while the planetary albedos lay 2 to 11 points apart."

Rule: sentences carry their dependencies (the connective names the real relation); inheritance and order; claims
stay within their evidence.

Why: the maps are of sunlight and rain, and the paragraph has already given their reason: the two defects keep
the global mean of the arriving sunlight, and the test world's mean temperature moved 0.9 K. The "since" clause
sets global means against cloud cover, yet Yang et al.'s cover figures are themselves global means, compared with
albedos, and they compare cloud schemes on planets free of these defects. With the comparison as its landing, the
paragraph ends on cloud parameterization, a subject apart from the defects it develops, and a reader of the next
paragraph's opening ("Where two of the defects moved sunlight between places") has to look back past it. Beside
the cloud calibration (lines 42–44) the same comparison is evidence for the claim next to it: how far two
parameterized covers stood from cloud-permitting runs on two tidally locked planets.

Rewrite (about length-neutral: the 11-word clause goes and the Yang sentence moves). End the second paragraph at
"A modeller finds such an error in maps of sunlight by longitude and of rain by season." Close the third
paragraph with: "Cloud amount would be a calibration for each world, fitted to cloud-resolving runs of that world.
On two tidally locked planets in the comparison of \textcite{yang2023cloud}, cloud covered 82--97\% of the sky in
two GCMs whose cover follows relative humidity, stability and large-scale ascent, and 27 and 41\% in quasi-global
cloud-permitting runs that count cloud by a condensate threshold, over sea surfaces fixed from a coarser run of
the same model, while the planetary albedos lay 2 to 11 points apart. On the test world the cloud fit is still to
be made, and CM1's runs compute with Earth-fitted microphysics of their own." The third paragraph grows by about
60 words and the second shrinks by about 70. The composed paragraphs follow Finding 24.

### Finding 4. MAJOR. conclusions.tex:56–60. Modelled storms given an action

Text: "Electrified storms resolved at other gravities, the route Sergeev et al. propose for tuning such laws where
observations are lacking, would set those laws beside flashes computed from the same laboratory charging laws and
from discharge thresholds set for Earth's storms, on grids fine enough to converge the flash count: a comparison
between models at each gravity."

Rule: exact action. Storms that "set laws beside flashes" act as "Three model families divide the work" acts in
the AGENTS.md examples.

Why: the storms are simulations. The operation is a modeller's tuning of the flash-rate laws to the simulated
flashes; naming it keeps the sentence's point, a comparison between models, and keeps Sergeev et al.'s route
attributed as before.

Rewrite (2 words shorter): "Tuning such laws on electrified storms resolved at other gravities, by the route
Sergeev et al. propose where observations are lacking, would fit them to flashes computed from the same
laboratory charging laws and from discharge thresholds set for Earth's storms, on grids fine enough to converge
the flash count: a comparison between models at each gravity."

### Finding 5. MAJOR. results.tex:44–48. Two lists stand before the verb

Text: "From the Earth-orbit state, the synodic clock, a year of whole model days, the Moon's own tilt and the
recalibrated split of sunlight, a general repair, two avoidances, one of them output bookkeeping, and a
calibration made in one step, warmed the test world by 0.6~K and cut its rain from 2.91 to 2.24~mm per day, and
the land receiving under 0.5~mm per day grew from 9 to 42\%, 36\% within two years of the Sun and tilt alone:
with Earth's 23.7\textdegree\ tilt, summer rain had reached 60\textdegree."

Rule: sentences carry their dependencies ("a long sentence holding the same inventory still fails"); a genuine
catalogue goes in a list.

Why: nine comma-separated phrases precede the verb, four changes and then their four classes, with "one of them
output bookkeeping" inside the second list and "made in one step" closing it. A reader counts to pair each change
with its class, and "From the Earth-orbit state," can be read as governing the first list. The pairing matters to
the ranking by form at lines 86–90.

Rewrite (adds 8 words): "From the Earth-orbit state, four changes were made in one step: the synodic clock, a
general repair; a year of whole model days, an avoidance in the output's bookkeeping; the Moon's own tilt, an
avoidance by configuration; and the recalibrated split of sunlight, a calibration. Together they warmed the test
world by 0.6~K and cut its rain from 2.91 to 2.24~mm per day, and the land receiving under 0.5~mm per day grew
from 9 to 42\%, 36\% within two years of the Sun and tilt alone: with Earth's 23.7\textdegree\ tilt, summer rain
had reached 60\textdegree." Checked against Table tab:inventory (Sun clock general, calendar avoided, orbit
default avoided, water absorptivity a calibration) and claim G02.

### Finding 6. MINOR. conclusions.tex:3–8. The opening's two strands share no term

Text: "Where an Earth value in the four codes was repaired, the kind of repair followed largely from the value's
form: ... Of the five defects, three, all in ExoPlaSim, produce little or no error ..."

Rule: inheritance and order.

Why: the repair classes and the defects stand side by side as two reminders. The defects continue in the second
paragraph and the repair classes return only in the third, so the section opens like a list, the effect the
author rejected in an earlier version. Two of the general repairs named in the first sentence are the ones that
remove two of the defects, and naming them at the head of the second sentence links it to the first.

Rewrite (adds 2 words): "Two of the general repairs remove, and a switch avoids, three of the five defects, all
in ExoPlaSim, which produce little or no error at Earth's values and an error that grows as a world's rotation
slows or its day, tilt or eccentricity departs from Earth's." Checked against repairs.tex:29–33 and Table
tab:inventory.

### Finding 7. MINOR. conclusions.tex:8–11. Two tenses under one evidence state, and an interrupted phrase

Text: "By the code's own arithmetic, the convective-cover unit would add about 0.23, ..., and the Sun clock sets the
Sun back about 33\textdegree\ each model day in a non-synchronous run, on the default solar geometry, of any
planet rotating more slowly than once in 20 days."

Rule: sentences carry their dependencies; cadence.

Why: one clause is conditional and the other indicative under the same "By the code's own arithmetic", which reads
as two evidence states where the text has one; "on the default solar geometry" splits "run" from "of any planet".

Rewrite (length unchanged): "By the code's own arithmetic, the convective-cover unit adds about 0.23, up to the
cover's cap of 0.8, to the convective cover of a synchronous run of TRAPPIST-1e, and the Sun clock sets the Sun
back about 33\textdegree\ each model day in a non-synchronous run of any planet rotating more slowly than once in
20 days, on the default solar geometry."

### Finding 8. MINOR. conclusions.tex:16–18. The direction of the change is left to inference

Text: "... and in a two-year test of the Sun and tilt alone the share of land under half a millimetre of rain a day
rose from 9 to 36\%."

Why: the clause follows "the orbit default ... brought Earth's seasons and summer rain to 60\textdegree", so a
reader can credit the rise to the defect; it came with the repair.

Rewrite (adds 2 words): "and in a two-year test that repaired the Sun clock and tilt alone the share of land under
half a millimetre of rain a day rose from 9 to 36\%." The next sentence's "in the same test" keeps its antecedent.

### Finding 9. MINOR. conclusions.tex:33–38. Titan follows the dynamics clause it has no bearing on, and the dynamics clause states no consequence

Text: "The radiative geometry of tall air is computed from that column, as the curved-air table was for the test
world, while the GCM's dynamics keep a thin shell and CM1's a flat slab, both at constant gravity. On Titan, ..."

Rule: inheritance and order; a paragraph develops a mechanism or consequence.

Why: the dynamics clause stands between the geometry claim and the Titan sentence that illustrates it, and omits
what a modeller of a new world needs for the dynamics, the question the paragraph's hinge sentence (line 33)
asks. The answer the evidence supports is in next.tex:51–58: a test of the circulation's sensitivity.

Rewrite (adds about 10 words): "The radiative geometry of tall air is computed from that column, as the curved-air
table was for the test world; on Titan, whose haze has a scale height of about 80~km, three hundredths of its
radius as for the test world's air, the plane-parallel codes that separate the surface from the haze hold to
about 65\textdegree\ from the zenith \autocite{vincendon2010spherical}, although the adapted models lack Titan's
nitrogen--methane radiation. The dynamical cores keep a thin shell in the GCM and a flat slab in CM1, both at
constant gravity, an approximation whose effect on the test world's circulation is still to be measured."

### Finding 10. MINOR. conclusions.tex:38–42. The gas-scheme sentence clashes in tense and narrows the largest fit to gas

Text: "A scheme built from the reference's line-by-line spectroscopy would replace the radiation's gas fits, the
largest of the Earth fits, for air of nitrogen and oxygen with water and modest carbon dioxide at the pressures
and temperatures over which an independent code has checked that spectroscopy, a check so far planned on the
design column alone, and the cloud optics would remain fits."

Rule: technical meaning survives editing; exact action; sentences carry their dependencies.

Why: "has checked" reads as done until the appositive says "so far planned"; the agent of a check is the modeller
who compares two codes; the cloud-optics clause contrasts with the scheme and arrives by "and"; and "the largest
of the Earth fits" repeats the paragraph's first sentence while crediting to the gas fits an effect that the first
sentence credits to a Rayleigh multiplier and the water continuum together.

Rewrite (6 words shorter): "A scheme built from the reference's line-by-line spectroscopy would replace the
radiation's gas fits for air of nitrogen and oxygen with water and modest carbon dioxide, at the pressures and
temperatures where that spectroscopy agrees with an independent code, a comparison so far planned on the design
column alone, while the cloud optics would remain fits."

### Finding 11. MINOR. conclusions.tex:46. A plural for one model

Text: "The storm models' charging laws were fitted to laboratory measurements."

Why: one storm model is meant, CM1 with WRF-ELEC's electrification.

Rewrite (1 word shorter; it also inherits CM1 from the rewrite in Finding 3): "The charging laws grafted into CM1
were fitted to laboratory measurements."

### Finding 12. MINOR. conclusions.tex:62–64. The abstract's sentence repeated word for word

Text: "Patched, SWAN reproduces a sixfold gravity scaling of an Earth sea to 0.3\% in wave height, where the released
code misses it by up to 5.4\%; ..."

Why: the clause repeats abstract.tex:16–17 exactly and leaves its link to the paragraph's first sentence ("tested
by similarity runs") unwritten.

Rewrite (adds 3 words): "Patched, SWAN passes such a test, reproducing a sixfold gravity scaling of an Earth sea
to 0.3\% in wave height where the released code misses it by up to 5.4\%; ..." (verification.tex:41–44: 0.303%
against a 1% criterion).

### Finding 13. MINOR. abstract.tex:15 and 21. "The reference" lacks an antecedent in the abstract

Why: the abstract introduces the model as "an in-house line-by-line model" and later names it "the reference".

Rewrite: in Finding 1's rewrite, "the in-house model's line-by-line spectroscopy".

### Finding 14. MINOR. abstract.tex:10–12. "The code's" finds its referent late

Text: "the released codes also hold five defects, and by the code's own arithmetic three of them, with little or no
error at Earth's values, bias ExoPlaSim's runs that meet their conditions, ..."

Why: "the code's" follows "the released codes" and finds its referent only in "ExoPlaSim's" later in the clause.

Rewrite (length unchanged): "the released codes also hold five defects, and by ExoPlaSim's own arithmetic three of
them, with little or no error at Earth's values, bias its runs that meet their conditions, slowly rotating and
tidally locked planets among them."

### Finding 15. MINOR. conclusions.tex:68. An ambiguous pronoun

Text: "Its drop-size limits stay Earth's, ..."

Why: "Its" can take CM1 or "its convection" from the sentence before.

Rewrite: "Morrison's drop-size limits in CM1 stay Earth's, ..."

### Finding 16. MINOR. conclusions.tex:71–72. An unnamed sensitivity on an uncited premise

Text: "On Earth, collisions set the largest raindrops, so runs with Morrison's limits scaled by the capillary length
would bound a sensitivity, a step still to run."

Rule: precise nouns; claims stay within their evidence.

Why: "a sensitivity" names no quantity, so the paragraph lands on an unnamed step; and the premise "collisions set
the largest raindrops" appears nowhere else in the paper and has no citation, though the inference depends on it.
next.tex:73–74 names the quantity: how much of the evaporation the small drops cause.

Rewrite (adds 5 words): "On Earth, collisions set the largest raindrops [citation to a located passage of an
admitted source], so runs with Morrison's limits scaled by the capillary length would bound how much of the lunar
rain's evaporation its small drops cause, a step still to run." The citation is for the author or the evidence
review to supply; this review found no located passage for the premise in the manifest.

### Finding 17. MINOR. conclusions.tex:81–83. The code given the measuring

Text: "Released and repaired ExoPlaSim on ozone-free Earth-air planets ..., would measure their joint effect."

Why: in next.tex:37–40 the runs measure ("the pair would measure").

Rewrite (adds 2 words): "Runs of released and repaired ExoPlaSim on ozone-free Earth-air planets ... would
measure their joint effect." The conditions repeat next.tex:37–39 word for word; the claim depends on them, since
zero obliquity and eccentricity bring the orbit default into the released runs, so the repetition earns its place.

### Finding 18. MINOR, optional. abstract.tex:21–25 against conclusions.tex:74–86. The final-page arc stops one step short in the abstract

Why: the abstract lands on the gas scheme and on cloud fitted to cloud-resolving runs; the conclusion lands one step
further, on the drop and charging laws inside those runs and the laboratory tests they need, and its last paragraph
opens on the design set with the model. An abstract reader meets neither.

Rewrite of the abstract's last clause (adds about 11 words): "while cloud would be a calibration for each world,
still to be made on the test world, fitted to cloud-resolving runs whose own drop and charging laws come from
Earth's rain and the laboratory." Checked against assumptions.tex:84–94. The abstract's last sentence then runs to
about 75 words; the author may judge the gain worth less than the length.

### Finding 19. MINOR. results.tex:91–92. "On" twice

Text: "on two tidally locked planets: on TRAPPIST-1e and K2-72e, CAM3 covered ..."

Rewrite (1 word shorter): "on two tidally locked planets, TRAPPIST-1e and K2-72e: CAM3 covered ..."

### Finding 20. MINOR. reach.tex:38–39. SWAN named twice in five words

Text: "With SWAN's knee patched, SWAN and SWASH, in the configuration used, are built ..."

Rewrite: "With SWAN's knee patched, the two wave models, in the configuration used, are built to run water seas at any
gravity ..."

### Finding 21. MINOR. next.tex:42–43. The separation credited to one comparison

Text: "and setting the repaired climate beside ROCKE-3D's would separate the defects' effects from the two models' own
physics and configurations."

Why: the released–repaired pair measures the defects, and the comparison with ROCKE-3D measures what remains once
they are removed; the sentence credits the separation to the comparison alone.

Rewrite (adds 2 words): "and the repaired climate, set beside ROCKE-3D's, would measure what the two models' own
physics and configurations change once the defects are removed."

### Finding 22. MINOR. next.tex:79–83. A cause joined by "and", and two openings on "The sign"

Text: "The sign of the lunar lightning changes with the laboratory charging law chosen, and the laws disagree in the
lunar storms' little cloud water. The sign of the charge rimed ice takes ..."

Rule: sentences carry their dependencies; vary openings.

Rewrite (about length-neutral): "The sign of the lunar lightning changes with the laboratory charging law chosen,
since the laws disagree on the charge rimed ice takes in the lunar storms' little cloud water. Measured in a
laboratory at 4--8~m\,s$^{-1}$ in 0.02--0.2~g\,m$^{-3}$ of cloud water at $-5$ to $-16$\,\textdegree C, the sign
of that charge would decide whether ..."

### Finding 23. MINOR. next.tex:83–85. A coined label for the strike's path

Text: "A leader model of the long crossing would replace the bound on ground strikes, ..."

Rule: no coined terms; precise nouns.

Why: "the long crossing" leaves its path unnamed.

Rewrite (adds 7 words): "A leader model of the descent from the $-7$\,\textdegree C level, 27--34~km up, to the
ground would replace the bound on ground strikes, ..." (assumptions.tex:31; repairs.tex:160–164).

### Finding 24. MINOR. introduction.tex:71–75. The list runs into the next clause, and the evidence basis is absent

Text: "In the four codes the Earth values take four forms, dimensional constants written into the code, units of
time, geometry, and empirical fits and simplifications used beyond the range they were made for, and the released
codes hold five defects, three of which produce little or no error at Earth's values and bias ExoPlaSim's runs
that meet their conditions, ..."

Why: the comma list runs into ", and the released codes hold", so the defects can read as a fifth form; and the
basis that the abstract and conclusion state ("by the code's own arithmetic") is absent here.

Rewrite (adds 6 words): "In the four codes the Earth values take four forms: dimensional constants written into
the code, units of time, geometry, and empirical fits and simplifications used beyond the range they were made
for. The released codes also hold five defects, three of which produce little or no error at Earth's values and,
by ExoPlaSim's own arithmetic, bias its runs that meet their conditions, slowly rotating and tidally locked
planets among them."

### The first three paragraphs with Findings 3 and 6–10 composed

Shown so the author can read the rewrites together; every number and condition is the snapshot's.

> Where an Earth value in the four codes was repaired, the kind of repair followed largely from the value's form:
> units and constants took general repairs with no coefficient fitted to the test world, geometry took a method
> whose table is computed from the world's own column, and the radiation's fits took calibrations to a
> line-by-line model and its correlated-$k$ emulation. Two of the general repairs remove, and a switch avoids,
> three of the five defects, all in ExoPlaSim, which produce little or no error at Earth's values and an error
> that grows as a world's rotation slows or its day, tilt or eccentricity departs from Earth's. By the code's own
> arithmetic, the convective-cover unit adds about 0.23, up to the cover's cap of 0.8, to the convective cover of
> a synchronous run of TRAPPIST-1e, and the Sun clock sets the Sun back about 33\textdegree\ each model day in a
> non-synchronous run of any planet rotating more slowly than once in 20 days, on the default solar geometry.
>
> On the test world two of the three kept the global mean of the sunlight arriving at the top of the air and
> moved that sunlight between places. The Sun clock, which errs in the Sun's longitude alone, keeps every zonal
> mean of the arriving sunlight, while the test world's equator received up to 17\% more than its mean in one
> sector and 8\% less in another; the orbit default, which put Earth's tilt in place of the configured one,
> brought Earth's seasons and summer rain to 60\textdegree, and in a two-year test that repaired the Sun clock and
> tilt alone the share of land under half a millimetre of rain a day rose from 9 to 36\%. The moved sunlight
> changed the clouds, and through them the global means: in the same test the clouds' effect in sunlight weakened
> by 2.4~W\,m$^{-2}$, and the test world ran 0.9~K warmer while still gaining heat. A modeller finds such an error
> in maps of sunlight by longitude and of rain by season.
>
> Where two of the defects moved sunlight between places, changes to the parts fitted to Earth's atmosphere moved
> the test world's global-mean surface temperature furthest: the first calibration of the radiation's Earth fits,
> a Rayleigh multiplier and a weaker water continuum, moved the first design runs by at least 20~K; the longwave
> correction and the ice optics, switched on together, warmed the design case by 11.5~K over years 10--19, with a
> correction fitted at 295~K; and PlaSim's Earth-tuned cloud settings, pushed to the ends of their tests, moved
> the global mean by up to about 6~K as the runs settled, against 1.6--2.5~K for the two general repairs measured
> alone. What a modeller of a new world needs for each part depends on how far the world's own column determines
> it. The radiative geometry of tall air is computed from that column, as the curved-air table was for the test
> world; on Titan, whose haze has a scale height of about 80~km, three hundredths of its radius as for the test
> world's air, the plane-parallel codes that separate the surface from the haze hold to about 65\textdegree\ from
> the zenith \autocite{vincendon2010spherical}, although the adapted models lack Titan's nitrogen--methane
> radiation. The dynamical cores keep a thin shell in the GCM and a flat slab in CM1, both at constant gravity, an
> approximation whose effect on the test world's circulation is still to be measured. A scheme built from the
> reference's line-by-line spectroscopy would replace the radiation's gas fits for air of nitrogen and oxygen
> with water and modest carbon dioxide, at the pressures and temperatures where that spectroscopy agrees with an
> independent code, a comparison so far planned on the design column alone, while the cloud optics would remain
> fits. Cloud amount would be a calibration for each world, fitted to cloud-resolving runs of that world. On two
> tidally locked planets in the comparison of \textcite{yang2023cloud}, cloud covered 82--97\% of the sky in two
> GCMs whose cover follows relative humidity, stability and large-scale ascent, and 27 and 41\% in quasi-global
> cloud-permitting runs that count cloud by a condensate threshold, over sea surfaces fixed from a coarser run of
> the same model, while the planetary albedos lay 2 to 11 points apart. On the test world the cloud fit is still
> to be made, and CM1's runs compute with Earth-fitted microphysics of their own.

## 3. What works

1. The section has a governing relation: what the codes can test on themselves, the defects by their arithmetic
   and paired runs and gravity by similarity runs, set against what needs evidence from beyond them, the fits.
   Lines 62–66 state it most sharply ("Whether gravity enters a model consistently is a property of the code,
   tested by similarity runs ... while Earth's empirical laws ... keep coefficients fitted at Earth's gravity"),
   and the last sentence gathers it. The relation appears in neither the abstract nor the introduction in this
   form, which meets the charter's requirement that a conclusion gather its lines into a new consequence.
2. The hinge at line 33, "What a modeller of a new world needs for each part depends on how far the world's own
   column determines it", orders the third paragraph from the part the column fixes, the radiative geometry, to
   the parts it leaves to other evidence, and puts the repair classes in the terms a modeller of another world
   needs, with no "this means that".
3. The storms paragraph (46–60) develops a question for exoplanet lightning: Braam et al.'s and Sergeev et al.'s
   laws were fitted to Earth's storms, the lunar tops rose far beyond them, and tuning on resolved storms compares
   models. The polarity sentence names the measurement and its conditions and scopes the result to the model.
4. The design paragraph (74–78) states the constructed-world consequence through the case's own numbers: the
   dimming chosen with the calibrated GCM, eased from 5.0 to 3.0% when the curved-air terms and gas bands came in,
   and open to change with each refit or under a lower pressure or another shield. The point for designers of
   other constructed worlds stays implicit, as the author asked.
5. No sentence places an untested world within reach. TRAPPIST-1e and the slow rotators enter through the released
   code's arithmetic; Titan through Vincendon and Langevin, with the adapted models' lack of its radiation in the
   same sentence; other worlds through the evidence each fit would need. The reach test (79–83) is a proposal with
   its measured quantity.
6. Qualifications attach once, to the claim they bound, and positively: "By the code's own arithmetic", "made
   before the ventilation repair and with leakage off", "on the code paths those tests ran", "part of the
   difference possibly from its grid", "known so far from the code's arithmetic".
7. Transitions come from the subject matter: "two of the three" (line 13), "Where two of the defects moved sunlight
   between places" (27), "Earth-fitted microphysics of their own" leading into the charging laws (43–46), and "a
   comparison between models at each gravity" leading into "a property of the code" (59–62). No stock signpost
   appears.
8. The abstract opens on the field's need, names the test world only as "such a world, a breathable Moon", and lands on
   the same next consequences as the conclusion: a scheme built from the spectroscopy, and cloud calibrated for
   each world to cloud-resolving runs.
9. Among the revised passages, next.tex:13–17 states the scheme's bound in its clearest form ("once that
   spectroscopy is checked, would hold on columns within the gases, pressures and temperatures of the check"), the
   model for Findings 1 and 10. results.tex:152–156 attributes each flash-rate law to its study and lands on the
   cloud-top gap. reach.tex:38–42 and the Seas row distinguish released from patched SWAN and state the tested
   scope exactly.
   repairs.tex:106–109 states the dependence on the scattering layer's height against the radius with both worlds'
   angles and its source. next.tex:36–44 names three distinct measurements and what a failed one would change in
   Table tab:reach. next.tex:79–85 ties the polarity question to the people it concerns ("the polarity that
   protection on the ground and in the air must meet").

Pass notes, for the ten passes of the charter's section 11:

- Bead strings: none in the conclusion; the long list sentences (27–32, 46–50) are comparisons with their
  relations written. Finding 5 is the case in Results.
- Inheritance and reorderability: Findings 3, 6 and 9. The storms and gravity paragraphs could trade places at
  some cost; in the present order "a comparison between models" leads into "a property of the code", which earns
  the order its place.
- Verbs and exact action: Findings 4, 10 and 17.
- Living presence: modellers and the cited authors act ("A modeller finds", "Sergeev et al. propose", "Yang et
  al."); the author's own work passes in the passive with its agent known, which the rules allow.
- Defensive structure: no objection catalogue or disclaimer. Finding 10 is the one place where qualifications
  crowd a claim.
- Redundancy and audience: Findings 3 (the "since" clause), 10 (the repeated superlative) and 12 (the abstract's
  sentence repeated).
- Cadence, silent: openings vary within each paragraph; the first and third paragraphs both open on a "Where"
  clause, as does the abstract's repair sentence. Sentences run from 10 to about 85 words, with short hinges at
  lines 33, 46 and 62. Paragraph landings: the 33° skip; with Finding 3, the modeller's diagnostic; the
  cloud-resolving runs' own Earth fits; "a comparison between models at each gravity"; "a step still to run",
  the flattest (Finding 16); and "laboratory tests". Read-aloud pending.
- Final-page arc: Finding 18; otherwise the abstract, the introduction's last paragraph and the conclusion promise
  and land on the same contribution.

## 4. Counts and judgement

BLOCKING 0. MAJOR 5 (Findings 1–5). MINOR 19 (Findings 6–24, of which Finding 18 is optional).

The section meets the author's direction. It discusses where the rejected version listed: each paragraph develops
one question (how defects that keep the global means are found, what a new world needs part by part, what decides
the lunar storms' laws, what a similarity test can check, how a design set with a model moves with its fits), and
the last sentence gathers them into a chain of evidence that ends in spectroscopy and laboratory measurement. It
reminds through its first paragraph and its numbers, and in its strongest lines the reader meets open questions
with stakes: a laboratory measurement that would decide the model's lightning polarity, a design temperature that each
refit can move, and cloud covers two to three times apart on tidally locked planets. No sentence presents an
untested world as within reach. Five repairs come before the next round: the abstract's bound on the gas scheme
reads as an independent check already made (Finding 1); the landing counts CM1's runs as evidence from outside
the adapted codes (Finding 2); the defects paragraph closes on a reason and a comparison that belong beside the
cloud calibration (Finding 3); modelled storms set laws beside flashes (Finding 4); and one revised Results
sentence holds two lists before its verb (Finding 5). Of the minor findings, the opening's seam (Finding 6) does
most to remove the remaining summary feel. The cadence reading was silent, and the read-aloud pass stays pending.
