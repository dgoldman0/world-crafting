# Editorial round 17: dispositions

Kept by Claude Opus 5.5, the drafting assistant, on 18 October 2026. Round 17 closed the revision from the
related-work scan: two fresh Claude Opus 5.5 subagents read the whole paper at commit 1278887, one for prose and the
author's direction (`editorial_round17_prose.md`: 0 BLOCKING, 3 MAJOR, 40 MINOR) and one for evidence and scope
(`editorial_round17_evidence.md`: 0 BLOCKING, 2 MAJOR, 14 MINOR). Every finding was acted on except those on wording
the author had approved, the abstract's text after its opening and the accepted Conclusion, which go to the author
as in round 15. A finding marked applied took the reader's fix or sample rewrite; where the text differs, the reason
is given.

## For the author's decision

| Finding | Wording | The reader's proposal |
|---|---|---|
| Evidence 1 (abstract part) | `abstract.tex`:11–12, "which makes it a test of every Earth value that depends on them" | Drop "every": "a test of the Earth values that depend on them", since the lunar runs exercise the values on their own paths, and the Moon departs one way along each ratio. The same change was applied in Worlds, which said the same |
| Evidence 2 | `abstract.tex`:14–16, "they bias its runs of slowly rotating and tidally locked planets" | The three defects act under different conditions (the Sun clock leaves tidally locked runs alone; the orbit default acts at any rotation); restore the Introduction's wording, "they bias its runs that meet their conditions, runs of slowly rotating and tidally locked planets among them" |
| Prose F40 | `conclusions.tex`:12–13, "Such a comparison could follow a change ..." | No comparison precedes it: "Run together, the global and resolved calculations could follow a change in a planet's climate down to the water arriving in a basin and the waves arriving at its coast, through the circulation that determines both." |
| Prose F41 | `conclusions.tex`:26, "make that distinction useful when specifying another world" | A generic verb where the next sentences name the operations: "With the ensemble's reference and calibration tools, that distinction becomes a procedure for specifying another world: ..." |
| Prose F42 | `conclusions.tex`:76–77, "Their disagreement identifies collision speeds, ..." | An abstraction given the act of identifying: "Comparing runs under each law locates the collision speeds, water contents and temperatures at which further measurements would discriminate between the laws." |

## Prose (`editorial_round17_prose.md`)

| Finding | Disposition |
|---|---|
| F1, MAJOR | Applied in four places: Worlds now says only that lunar convection's departure remains unmeasured, so the 6 km grid rests on the dry similarity; Verification's overview names the third step's standards as ranges, and its third shortfall says builds compare as realisations, "as the threaded box runs do"; Reach keeps the drop limits' effect "unmeasured" without retelling the failed pair. Verification keeps the full account with V06 |
| F2, MAJOR | Applied, condensed: the Introduction now ends on the path ahead, "Replacing those fits comes first in the ensemble's further development, with a radiation scheme reduced with existing tools from the reference model's spectroscopy and cloud calibrated against cloud-resolving runs of each world; runs on planets that other studies model, among them slowly rotating planets of Way et al. and the cases of the SAMOSA intercomparison, would then test how far the general repairs hold." |
| F3 | Applied with evidence 4 and 5: "Other models built for Earth have been joined to GCMs", the Titan acts in the past, and the LMD's shared physics in a sentence of its own, "for its part" in place of the reader's "has gone further", which ranked the work |
| F4 | Applied: "can depart further from Earth", "for about 70 million years" (Needham and Kring's estimate, already cited), and "cluster near the same divide, extended to them" |
| F5, F6 | Applied |
| F7 | Applied: "determine", "govern", "fixes", "measures" and "fixes" where "set" repeated; "set" stays for the scales of height and time |
| F8–F12 | Applied; for F10 the ground-strike rule has its own sentence, "Its rule for ground strikes was drawn from Earth's storms", and H03 marks both |
| F13, F14 | Applied; RRTMG opens a paragraph of its own, "CM1's RRTMG meets the same columns at the edges of its tables" |
| F15 | Applied to four of the five frames: "In the storms, WRF-ELEC caps ...", "CM1 keeps Earth's day in its Sun and its soil", "PlaSim's vertical grid was laid out for Earth", "The wave and storm laws come from Earth's calibrations"; "PlaSim's longwave errs by height as well" stays |
| F16 | Applied: the cover sentence breaks after the developers' clause, and the orbit default's sunlight falls "at 86° latitude" |
| F17 | Applied with evidence 7: "the 282 weakly absorbing channels by spherical successive orders of scattering ..., and the rest by the pseudo-spherical approximation, a direct beam through the shells with the diffuse light of a two-stream" |
| F18, F19 | Applied: "Between them, the bound counts ..."; "Since the methods that force CM1 impose only ..." |
| F20 | Applied in part: "and although Cazaubiel et al. raised gravity up to twentyfold in a centrifuge, they studied wave turbulence in a container, so a wave model's response to gravity under wind is checked numerically". The reader's "forced mechanically" rests on the scan's landing-page reading; the abstract says a container, and the paper's text was refused to scripted reading, so the sentence says no more than the abstract |
| F21 | Applied |
| F22, MAJOR | Applied as proposed with evidence 10 and 11: the lunar paragraph keeps its line, the ranking followed by the longwave test ("the one change fitted to the cooling by height") and the uncertainty; the field's spreads open a paragraph of their own, "The fits' effects are of the order of the spreads measured in intercomparisons of exoplanet models", ending on Yang et al. 2023 and handing on to the gap between the models |
| F23, F24 | Applied; F23 reads "the calibrated configuration settled at 295.5 K, at least 20 K below the uncalibrated run, which was still warming at 315.5 K in model year 12" |
| F25 | Applied: "44 flashes a second or about 2.7 per square kilometre per year", the 2.72 already in G10's calculation |
| F26–F30 | Applied; F27 with evidence 12. For F28, Reach drops its sentence listing the other codes' Earth values, which Table 4 carries, opens CM1's adapted state with "Among the other codes", and drops the restated Sun-clock skip and cover formula while keeping the synchronous mode and the two planets' biases |
| F31–F36 | Applied; F35 opens on the relation, "A second set of runs would test the convective-cover repair in synchronous rotation, ...: released and repaired ExoPlaSim on the sixteen cases of the SAMOSA intercomparison, ..." |
| F37 | Applied: (a) "in the two windows that Results describes", with both arrangements; (b) the reader's note on N01 taken up: "under Takahashi's, hail carried 37–43% and graupel, striking at about 1–4 m s⁻¹, most of the rest", as N01 records, in place of "graupel carried most of the charge"; (c), (d) as proposed |
| F38, F39 | Applied |
| F40–F42 | For the author (above) |
| F43 | Applied with evidence 15: the review history in Availability and `README.md` now record the scan, round 16 and this round |

## Evidence (`editorial_round17_evidence.md`)

| Finding | Disposition |
|---|---|
| 1 | Applied in Worlds: "a test of the Earth values that depend on them". The abstract's identical wording is for the author (above) |
| 2 | For the author (above) |
| 3, MAJOR | Applied: "Each team removed Earth values that mattered for the worlds it set out to model, but others could stay" |
| 4, 5 | Applied with prose F3 |
| 6 | Applied: "went without systematic study", the source's own qualifier |
| 7 | Applied with prose F17: the citation now attaches to the pseudo-spherical approximation the code shares with Dahlback and Stamnes and Kylling et al.; the code's own two-stream goes unnamed. Neither abstract could be retrieved (Elsevier and Springer refuse scripted reading, and Semantic Scholar holds none), so both stay at title depth in the manifest |
| 8 | Applied: "HITRAN's collision-induced absorption, in its files of 2018–2024", checked at `spectroscopy.py`:396–397 |
| 9, MAJOR | Applied by narrowing: the storm's first flash is set beside the cited runs' 27–40 minutes and its median charge per flash inside MacGorman et al.'s range; the flash-rate comparison, which Terluna's benchmark draws from four works the paper does not cite (Mansell 2014; Brothers et al. 2018; Ziegler et al. 2014; Calhoun et al. 2014), leaves the sentence. Citing those four, whose readings Terluna's sources hold, would restore it |
| 10, 11, 12 | Applied with prose F22 and F27 |
| 13 | Applied: "Every calibration was fitted to the line-by-line model, the longwave correction through its correlated-$k$ emulation, and that model's carbon dioxide, ..." |
| 14 | Applied: the check script "confirms that every marker resolves and that every listed file exists, and lists the web records it leaves unchecked" |
| 15 | Applied with prose F43 |
| 16 | Applied: the manifest records the further uses in the Introduction and the Conclusion of the round-16 sources and of Way et al. 2018; the PlanetWaves README is recorded as a supporting web record (address, commit `9a5da8ab`, retrieval date, quote) on Detelich et al.'s and Schneck et al.'s entries; Mlawer et al.'s note now records the abstract read on the archived original |

## Checks

`paper/tools/check.py` passes with its standing warnings (96 cited keys of 167; 107 claims cited of 109; S01 and
V14 uncited; the web source of H23 and N02 unchecked offline). The lint's negative-contrast candidates in the changed
text are negations the claims require, "went without systematic study" among them, the source's own qualifier.
`git diff --check` is clean. The PDF builds at 38 pages with zero overfull boxes; the exact-build record follows in
the release register.
