# Round 21: the closing review, and verbs that name no operation, 19 October 2026

Kept by Claude Opus 5.5, the drafting assistant.

## The author's direction

Having read the paper whole after round 20, the author judged it good overall and named one remaining weakness: the
repeated use of "verbs that don't really work well", partly typical of academic writing, with two examples in
Assumptions, "Earth's day enters..." and "Earth's day in its Sun and its soil". Reviewers in every earlier round had
passed such verbs, though the rule against empty actions covers them. The author left the check to the closing review, which had been held since
round 19 until the author finished reading.

## The closing review (a50e0b1)

Two fresh Claude Opus 5.5 subagents each read the whole paper and then tested every verb in half of it against its
subject, dead metaphors included: the front half, from the title to Repairs (`editorial_round21_closing_front.md`:
71 verb findings, 2 of them for the author, nothing else), and the back half, from Verification to Availability
(`editorial_round21_closing_back.md`: 87 verb findings, 19 for the author, and 2 MINOR findings in Next steps).
Neither found anything BLOCKING or MAJOR. One fix also corrects a claim: Next steps said that hail "carried" most of
the charge, where claim N01 records that hail did 82–88% of the non-inductive charging.

Each finding names the operation its subject stands for and the record that shows it, so the fixes are local
wording. They were applied in one pass to the body and the Introduction (1662968), and one light reading covered
both. The fixes in the abstract and the Conclusion, whose wording the author approved, are held for the author.

## For the author's decision

| Finding | As it stands | The reader's proposal |
|---|---|---|
| Front V1 | `abstract.tex`:18, "the constants, units of time and geometry that the codes set for Earth mostly took repairs that hold on other worlds ..." | "... were mostly given repairs that hold on other worlds ..." |
| Front V2 | `abstract.tex`:20–21, "and in the lunar runs they moved the climate furthest, by amounts of the order of the spreads ..." | "and in the lunar runs their effects on the climate were the largest, of the order of the spreads ...", as the Introduction now says |
| Back V69 | `conclusions.tex`:19, "has to retain its intended physical time interval" | "has to count rain over its intended physical time interval" |
| Back V70 | `conclusions.tex`:19–20, "Where one physics package serves the global and the resolved calculations" | "Where the global and the resolved calculations use one physics package" |
| Back V71 | `conclusions.tex`:32–33, "Otherwise the comparison mixes the response of the convection schemes with a change in where the air gains and loses heat." | "Otherwise the response of the convection schemes is confounded in the comparison with a change in where the air gains and loses heat." |
| Back V72 | `conclusions.tex`:35–36, "would extend this work beyond successive adjustments of the inherited broadband fits" | "would replace the inherited broadband fits and their successive adjustments" |
| Back V73 | `conclusions.tex`:40–41, "A different stellar spectrum would then enter through the spectral calculation, with its effects followed ..." | "The spectral calculation would then take a different stellar spectrum as an input, with the spectrum's effects followed ..." |
| Back V74 | `conclusions.tex`:42–43, "That development would join the existing ability to explore climates quickly to a physical reference ..." | "With that development, a modeller could still explore climates quickly, with the radiation computed from a physical reference ..." |
| Back V75 | `conclusions.tex`:45, "Cloud requires a further exchange between the models." | "Calibrating cloud requires a further exchange between the models." |
| Back V76 | `conclusions.tex`:58–59, "The scaled wave tests offer a complementary case" | "The scaled wave tests are a complementary case" |
| Back V77 | `conclusions.tex`:60–61, "An ensemble that computes both can examine which properties ..." | "With an ensemble that computes both, a modeller can examine which properties ..." |
| Back V78 | `conclusions.tex`:64, "Constructed worlds permit these comparisons over combinations of parameters ..." | "On constructed worlds, these comparisons can be made over combinations of parameters ..." |
| Back V79 | `conclusions.tex`:65–66, "A massive atmosphere on a small body separates the consequences of low gravity from those of thin air, and varying its pressure ..." | "On a small body with a massive atmosphere, the consequences of low gravity can be separated from those of thin air, and varying the atmosphere's pressure ..." |
| Back V80 | `conclusions.tex`:75, "The choice of those cases can also sharpen the use of terrestrial experiments." | "A modeller can also choose those cases to direct terrestrial experiments." |
| Back V81 | `conclusions.tex`:79, "A storm's planetary scale can thus be combined with experiments ..." | "A storm simulated at planetary scale can thus be combined with experiments ..." |
| Back V82 | `conclusions.tex`:80–81, "Comparisons across worlds would help select the experiments as well as use their results." | "Comparing worlds, modellers could select the experiments as well as use their results." |
| Back V83 | `conclusions.tex`:83–85, "those developments would refine the climate ... For a constructed world, they could change the illumination ..., as the radiation corrections already changed the dimming in the lunar design." | "the models so developed would refine the climate ... For a constructed world, the illumination chosen to sustain a desired climate could change with them, as the dimming of the lunar design changed with the radiation corrections." |
| Back V84 | `conclusions.tex`:86–87, "so the storm and sea calculations have to follow the revised climate" | "so the storm and sea calculations have to be rerun from the revised climate" |
| Back V85 | `conclusions.tex`:87–88, "compared through the water they deliver to the land and the winds they drive over the seas" | "compared through the rain on their land and the winds over their seas" |
| Back V86 | `conclusions.tex`:89–90, "The same ensemble would serve the interpretation of a world found around another star and the design of an environment ..." | "The same ensemble could be used to interpret a world found around another star and to design an environment ..." |
| Back V87 | `conclusions.tex`:97–98, "Comparing changes in illumination or surface-water distribution through these connected calculations could turn a broad temperature requirement ..." | "By comparing changes in illumination or surface-water distribution through these connected calculations, a designer could turn a broad temperature requirement ..." |

Both readers let "follow the consequences" stand in the abstract and the Conclusion's opening, as the paper's
governing image of the chained calculation; the back reader noted that the author may still prefer "compute".

## Dispositions

**Front (`editorial_round21_closing_front.md`).** V1 and V2 are for the author (above). V3–V71 were applied as
proposed, except:

| Finding | Applied as | Why |
|---|---|---|
| V6 | "while its code still contains a constant set for Earth's gravity" | "Retains" keeps the figure of the author's "keeps"; code contains a constant |
| V14 | "which PlaSim's broadband fits cover near Earth's" | Parallel to the next clause's "which RRTMG's tables cover", with the paths as the antecedent of "Earth's" |
| V29 | "as well as in schemes off those paths" | The proposal's "schemes the lunar cases leave unselected" kept a configuration as the agent; Assumptions already speaks of entries "off the lunar runs' paths" |
| V32 | "In their calendars, ExoPlaSim and CM1 count Earth days." | The codes count days; "count their calendars in Earth days" counted calendars |

The assistant added one fix of the same kind in Repairs: CM1's spare namelist reals "hold the settings of the lunar
Sun, the forcing and the electrification", where they held "the lunar Sun".

**Back (`editorial_round21_closing_back.md`).** V69–V87 are for the author (above). V1–V68, F1 and F2 were applied as
proposed, except:

| Finding | Applied as | Why |
|---|---|---|
| V3 | "The first three were compared in sequence, starting from the released model, each against a build ..." | The checks compared runs with builds; "were run in sequence from the released model" described the runs' order alone |
| V11 | Table 3: "absorbed near-infrared sunlight too high in the air" | In the table, without the text's heights, "too high" could be read as too much |
| V26 | "from the ice that formed above 107~km out of the vapour of the ring's starting sounding" | Ice formed from the sounding's vapour |
| V36 | "Under the third defect, the orbit default, PlaSim replaces a configured obliquity or eccentricity with Earth's" | The proposal left the defect as the agent; PlaSim replaces, as Assumptions now says |
| V39 | "ExoPlaSim would be run with its general repairs, ..." | The passive keeps the paragraph on the code and its configuration |
| V42 | The headings "Worlds that need refitted calibrations" and "Worlds that need new physics" stand | The reader marked them optional; the five sentences beneath them name the modelling that requires each step |
| V45 | Table 4: "Earth's orbit in place of the configured one, by ExoPlaSim's default" | As Table 2 words the same entry, with no setting as agent |
| V47 | "In the first experiments, the two Earth fits with the largest effects on the test world's climate in the tests are refitted" | The proposal's fits that "moved the test world's climate" kept the figure that V2 and V13 remove |
| V50 | "change the test world's temperature by several kelvin"; "could change the test world's temperature as much as the cloud settings do" | "Moves the temperature" kept a figure of motion |
| V61 | "The sign of the ground strikes under Takahashi's law is also undetermined in the windows" | The proposal made the windows the agent of leaving it undetermined |

## Light reading (1662968)

One fresh Claude Opus 5.5 subagent read every sentence the fixes changed, in its paragraph, against the claims
register, the defect log (A2, A3, A7, A8, B3, B10, C1, C3, C4), the verification record, CM1's README and the
graft's Fortran. It found every claim's numbers, conditions and scope intact, no "not" or "rather than" added, and
the assistant's departures from the proposals sound, the addition in Repairs among them: by CM1's README, `var1`–`var10`
hold the electrification, `var11`–`var15` the forcing and `var16`–`var19` the Sun. Verdict: 11 MINOR findings, all
applied in be4a1d5.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1 | `introduction.tex`:96 | With "by amounts" gone, "of the order of the spreads" followed "climate" and read as describing it | Applied: "effects of the order of the spreads" |
| 2 | `assumptions.tex`:35 | The new opening dropped "unit of time", the form the paragraph treats, and its "their" came before the names it stood for | Applied: "Earth's day is the unit of time in the calendars of ExoPlaSim and CM1." |
| 3 | `verification.tex`:22 | With the checks as subject, "once they are" tied the elided "run that way" to the checks | Applied: "only once those patches are" |
| 4 | `verification.tex`:44 | "from which it was scaled by 5.44\%" read as a scaling by 5.44% | Applied: "differs by 5.44\% in significant wave height and 3.91\% in mean period from the Earth run from which it was scaled" |
| 5 | `verification.tex`:94 | "absorbed near-infrared sunlight too high" read as an amount | Applied: "too high in the air", as in Table 3 |
| 6 | `results.tex`:118 | "above 107~km out of the vapour" first read as a distance | Applied: "from the ice above 107~km, formed out of the vapour of the ring's starting sounding" |
| 7 | `next.tex`:8 | "in the tests" sat beside "are refitted", so the restriction to the sensitivity tests, which leaves out the first calibration's 20 K, read unclearly | Applied: "two Earth fits are refitted, those whose changes in the sensitivity tests had the largest effects on the test world's climate" |
| 8 | `next.tex`:25 | The sentence made the cloud the cause of the temperature, where G05 and G16 record the changes in temperature when the settings were varied | Applied: "Varied in the tests, PlaSim's cloud amount and cloud water changed the test world's temperature by several kelvin, and both remain uncalibrated for that world." |
| 9 | `next.tex`:77 | After F2's "the two candidates still open", "if they remove little" read as the candidates | Applied: "if the extended tables remove little" |
| 10 | `appendix.tex`:99 | Table 6 kept "the charge each flash hands to the ions" | Applied: "adds" |
| 11 | `reach.tex`:52, 60 | The two headings kept "Worlds that need", the figure removed from the sentences beneath them | Applied: "Worlds beyond the existing calibrations." and "Worlds beyond the codes' physics.", after "Worlds near the existing fits." |

The reader also noted two passages older than this revision. In Repairs, `var20` holds the curved-air switch,
outside the groups the sentence named; the namelist sentence now ends "the electrification and the curved-air
terms". In Results, the list after "two realisations:" holds the three explanations tested, so it can first be read
as the realisations; it stands for a later reading.

## Build (be4a1d5)

Two clean builds from `be4a1d5153ad1804fb1eeb2028538321f8ba22d0` gave the same PDF, 37 pages, SHA256
`3b1514a37391e0637db0f8856222a48fa31b944d0bdd612a4cbc0948953742c9`, with zero overfull boxes and every font embedded.
The reflow removed the stranded line that closed page 24; a screen of every page break by `pdftotext` found only
table cells wrapping across pages 8–9 and 30–31. `paper/tools/check.py` passes with its standing warnings (96 cited
keys of 167; 107 of 109 claims cited; S01 and V14 uncited; the web source of H23 and N02 unchecked offline). The 21
fixes on approved wording are held for the author's decision.

## The Conclusion and the abstract (1df6379, 2fbc500)

The author accepted all 21 fixes on approved wording, and they were applied as listed above (1df6379). For "follow
the consequences", the author kept the verb and moved the action to a user of the ensemble: the abstract and the
Conclusion's first sentence now have a modeller follow the consequences, and the Conclusion's second paragraph, whose
first sentence already has a modeller, has the change in a planet's climate followed, in the passive.

One fresh Claude Opus 5.5 subagent read the two sections as revised. It found the numbers and conditions intact (V69
against H07, V83 against G04), every pronoun pointing where it should, and no new figure; its six findings, one
MAJOR, touched approved wording and went to the author, who approved all six (2fbc500).

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1, MAJOR | `conclusions.tex`:11, 35, 51 | Sentences opening on "With" went from three to seven, and three paragraphs now ended "With ..., a modeller could ...", each after a sentence closing on a ", with ..." clause | Applied: "Because the global and resolved calculations are chained through their forcing, ..."; "A modeller using the reduced scheme could still explore climates quickly, ..."; "Since the ensemble computes both, a modeller can examine ..." |
| 2 | `conclusions.tex`:54–55 | Two sentences in a row had the frame "On X, Y can be ...", so the example read as a second item | Applied: "These comparisons can be made on constructed worlds over combinations of parameters ..." |
| 3 | `conclusions.tex`:74, 77 | "could be used to" twice in a row | Applied: "Developed in this way, the ensemble could be run to explore ..." |
| 4 | `conclusions.tex`:29 | "confounded in the comparison with a change" first attached "with a change" to the comparison | Applied: "Otherwise, in the comparison, the response of the convection schemes is confounded with a change ..." |
| 5 | `conclusions.tex`:68 | "A storm simulated at planetary scale" read as a planet-wide storm-resolving run, where the electrified storms ran in 385 km boxes | Applied: "A storm simulated in its planetary setting" |
| 6 | `abstract.tex`:24–26 | The abstract's last two sentences both opened "With ..." | Applied: "A modeller running the ensemble could then follow the consequences ..." |

## Generic planetary models (a1dce83, 79db976, 88e2efe)

The author asked whether the paper makes plain why the ensemble builds on ExoPlaSim when generic planetary GCMs
exist, and whether the ensemble is of use to groups with more computing than one laptop. The assistant's reading: the
paper gave the pieces (most exoplanet GCMs are adapted Earth codes; the THAI models differ by 14 and 24 K; the works
it cites join two links of the chain at most) without the reason for the choice, and the sharpest form of the question
went unanswered, since ROCKE-3D with SOCRATES and the LMD generic model already compute their radiation from each
atmosphere's gases, the step Next steps proposes for PlaSim. The author described the ensemble as geared, for now, to
limited resources, and asked for the answer in plain statements, free of defensive phrasing. The assistant's first
summary called the calibrations "a stopgap that measured the problem", which the author rejected as itself a verb of
the kind round 21 removed; the calibration framing was dropped, since the paper already states what the calibrations
did.

Three sentences were added in the order of synthesis, as the author approved them, with two precisions: ROCKE-3D
computes radiation from the air's own gases in its SOCRATES configuration, one of its two radiation schemes, and the
paper's existing name, "the LMD generic model", is kept.

| Commit | Section | Addition |
|---|---|---|
| a1dce83 | Next steps | After the reduced scheme: "PlaSim would then compute its radiation as ROCKE-3D with SOCRATES and the LMD generic model do, from k-distributions of the air's own gases, at its own speed." |
| 79db976 | Introduction | Where ExoPlaSim enters: "..., the speed for which it was chosen, ..., computes its radiation with broadband fits to Earth's columns and ..." |
| 88e2efe | Conclusion | After the reduced scheme's prospect: "CM1 and the wave models take only the GCM's fields, so a GCM that computes its radiation from each atmosphere's gases, such as ROCKE-3D with SOCRATES or the LMD generic model, could force them as well." |

The sources were read for the purpose in their archived originals: Tsigaridis et al. (2025), p. 5825, "Two different
radiation schemes are supported, the GISS radiation, valid only for atmospheres similar to that of modern Earth, and
SOCRATES, which is more generalized but more computationally expensive", and p. 5831, on the spectral file that holds
"gas absorption coefficients for major and minor species"; Wordsworth et al. (2011), p. 2, on the correlated-k
coefficients. The manifest records the locators and both sources' new uses. Claim S14 now records the reason for the
choice: Terluna's table of candidate GCMs at 186b294 (`climate/gcm/README.md`, lines 70–85), which takes ExoPlaSim as
the fast first look and plans ROCKE-3D or the LMD model for the cases that matter, and the author's account above.
The abstract needs no change for this direction.

One fresh Claude Opus 5.5 subagent read the four commits from 2fbc500 to 88e2efe. It found the statements about
ROCKE-3D and the LMD generic model within their sources, with all three locators correct, the Introduction's clause
supported by S14 and by the body's own account of PlaSim's radiation, no statement answering an objection or hedging,
and the six approved fixes clean in their paragraphs. Verdict: one MAJOR and four MINOR findings, applied in 67b4786.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1, MAJOR | `next.tex`:18 | "at its own speed" claimed a speed that no run has timed, and the ROCKE-3D paper it cites calls SOCRATES the costlier of its two schemes | Applied: the phrase is dropped. The reader also asked the author about the Conclusion's approved "could still explore climates quickly", which rests on the same untimed premise; it stands, as a prospect for a reduced scheme made with a tool built for "fast $k$-distribution gas-optics models", in the title of Hogan and Matricardi (2022) |
| 2 | `next.tex`:18 | "k-distributions" set the k in text, where the paper sets it as math | Applied: "$k$-distributions" |
| 3 | `next.tex`:18–20 | The new sentence parted "that spectroscopy" and "such a scheme" from the phrases they point back to | Applied: the sentence moves, unchanged otherwise, to the end of its paragraph, after the reduction and its check |
| 4 | `conclusions.tex`:35 | "take only the GCM's fields" left out the slice's geometry and SWAN's spectra, which Repairs names | Applied: "take from the GCM only its fields" |
| 5 | `claims.json`, S14 | The record S14 cites was missing the author's account when read | Applied: the section above records it |

## Build

Two clean builds from `67b4786d8b18d5b5e1acdae4a496842668705345` gave the same PDF, 37 pages, SHA256
`76a0c0c90915f11bfd7f171d885bc36683a92ec63b53df05a4945f88cfb70b67`, with zero overfull boxes and every font embedded.
`paper/tools/check.py` passes with its standing warnings, and a screen of the page breaks found only table cells
wrapping across pages.
