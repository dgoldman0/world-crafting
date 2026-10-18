# Editorial round 16: light readings of the revision from the related-work scan, 18 October 2026

Kept by Claude Opus 5.5, the drafting assistant.

The author asked for the related-work scan (`paper/notes/related_work_scan_2026-10-18.md`) to be used in four steps,
each in the body alone and each followed by "just a very light editorial review": (1) correct what is wrong and cite
what the body already describes; (2) place the ensemble beside its nearest neighbours; (3) give the lunar numbers
the field's measured context; (4) name existing tools for the next steps. The Introduction, the Conclusion and the
abstract then follow in that order, each with its own light review, and a full editorial review closes the
revision. The author's reason for the order, recorded in memory as a general pattern: the Introduction synthesizes
the whole and so follows the body, the Conclusion synthesizes and inspires from it, and the abstract encompasses
everything and comes last.

Each light reading is one fresh Claude Opus 5.5 subagent, given the commit's diff, the author's direction in the
author's words, the writing rules in `AGENTS.md` and the cited sources' records and abstracts (held outside the
repository, as third-party text). It reports only clear problems, located and marked MAJOR or MINOR, and edits
nothing.

## Step 1: corrections and missing citations (d8aa61c)

Verdict: needs the listed fixes, all MINOR; nothing blocking.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1 | `verification.tex`:43–44 | "Only" with the present perfect turned one abstract into a claim about every centrifuge experiment with waves | Applied: the experiment is named, "\textcite{cazaubiel2019wave}, who raised gravity up to twentyfold in a centrifuge, studied wave turbulence in a container" |
| 2 | `repairs.tex`:98–99 | The new citation of the pseudo-spherical method stood beside a consequence that comes from the in-house code: twilight without scattered light | Applied: "which the code runs only with the Sun above the horizon", checked at `python/climate/gcm/twilight.py`:408–410 and `notes/reference_radiation.md`:355 |
| 3 | `repairs.tex`:130 | The citation read as the source for MT_CKD 4.3; the archived Mlawer et al. paper documents versions up to 4.1.1 | Applied: "MT\_CKD \autocite{mlawer2023inclusion} at version 4.3"; checked in the archived original, whose manifest entry moves to abstract depth |
| 4 | `results.tex`:155–156 | "Exoplanet estimates of lightning use laws fitted to Earth's storms" characterised the field from the two studies the sentence names (wording from round 15, in a sentence the commit touched) | Applied: "Two exoplanet estimates of lightning ..." |

Checked clean by the reader: no excluded words in the edited sentences; the knee's sentence reads correctly without
the Mars example and keeps its number, condition and claim marker; the flash-rate citations match their abstracts
(Price and Rind for cloud-top height; McCaul et al. for the upward flux of precipitating ice at −15 °C and the
column's ice); Lacis and Oinas fits the correlated-$k$ emulation; HITRAN's collision-induced pairs in Karman et al.
include the four the code reads; the claim markers stand.

## Step 2: the ensemble beside its nearest neighbours (235e729)

Verdict: needs the listed fixes, one MAJOR.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1 | `next.tex`:4–6, MAJOR | "In the LMD's models of Mars that consistency is built in" claimed more than Spiga and Forget report: their shared physics reaches "a high level of downscaling consistency", yet gustiness matched only with convective adjustment off, and Lefèvre et al. found a resolved Bond albedo of 0.06 against the GCM's 0.32 (`paper/notes/literature.md`:333). What is built in is shared code | Applied: "In the LMD's models the global and resolved calculations share their physics: the Mars GCM's parameterizations run in a mesoscale model on WRF's core, which the GCM drives at its boundaries ..., and the generic model's radiation and cloud have run on the same core over Proxima b, where the resolved cloud feedback came out much weaker than the GCMs'. Codes built separately, as here, are brought toward that consistency by calibration." |
| 2 | `next.tex`:4 | The approved step named the Generic PCM's route; the sentence named only the Mars models | Applied with item 1: Lefèvre et al. 2021, the generic model's radiation and cloud on WRF's core, is now cited, its abstract read |
| 3 | `next.tex`:30–34 | The Titan sentence fell between the lunar fit and its consequence, and called the plan a loop the paragraph never named | Applied: the sentence closes the paragraph, "On Titan a GCM's convection has been tuned this way: ..." |
| 4 | `results.tex`:133–134 | Song et al. call the two models "qualitatively consistent" in the Walker circulation and the substellar clouds | Applied: "far from a GCM in cloud water path and cloud width, though qualitatively consistent with it in the Walker circulation and the substellar clouds" |
| 5 | `repairs.tex`:199–201 | The GCM forcing over Titan's lakes is Detelich et al.'s, yet carried Schneck et al.'s citation; the opening said the link twice | Applied: "Over Titan's polar lakes, a Titan GCM's winds likewise force a wave model, PlanetWaves \autocite{detelich2026modeling}, adapted from an Earth model ... \autocite{schneck2026modeling}" |
| 6 | `repairs.tex`:201–202 | The storm-wind clause now closed Repairs without saying what it means for forcing from the GCM | Applied: the clause is dropped, the PlanetWaves sentence moves before the closing sentence, and Repairs again ends on the methods "built for a slice of any world's GCM", now "the ensemble's methods" so the subject stays clear |

Checked clean by the reader: no excluded words, hedging or promotional wording in the added text; the lint flags
nothing on the added lines.

## Step 3: the field's measured context (12bb044)

Verdict: needs the listed fixes, chiefly the first, which is MAJOR. The reader checked every number against its
abstract and the SAMOSA cover claim against W06's arithmetic (a 15-day rotation gives a model day of 15.65 days and
a cover bias of +0.34), and found them sound.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1 | `results.tex`:87–88, MAJOR | "Amounts of the same order" had no anchor, the ranking before it running from 20 K down to 0.65 K, and "exoplanet GCMs differ" spoke for the field | Applied: "Intercomparisons have measured spreads among exoplanet models of the order of the fits' effects", the fits being the radiation and cloud fits the ranking names |
| 2 | `results.tex`:88–90 | THAI's ranges joined nitrogen- and carbon-dioxide-dominated cases | Applied: "by 7 and 6 K in dry air dominated by nitrogen and by carbon dioxide ..., and by 14 and 24 K with water and cloud" |
| 3 | `results.tex`:90–91 | Only the larger of Yang et al. 2019's results was quoted | Applied: "against 8 K or less on a rapidly rotating one under a G star" |
| 4 | `results.tex`:91–93 | Yang et al. 2016 compare seven 1-D codes, five band and two line-by-line, with longwave differences growing with surface temperature | Applied as proposed |
| 5 | `results.tex`:87–93 | One sentence chained four results as a list; "while" left the radiation codes unrelated to the radiation fits; the turn to cloud went unmarked | Applied: two sentences, the radiation codes first, then the GCMs' spread widening as water and cloud enter, ending on the causes Yang et al. 2019 name, which hands on to the sentence on parameterized and resolved cloud |
| 6 | `next.tex`:55–59 | "The SAMOSA intercomparison offers a second benchmark" gave an abstraction a generic verb and named no run; the source's "blackbody" was dropped | Applied: "Released and repaired ExoPlaSim run on the sixteen cases of the SAMOSA intercomparison, ... around a 3000 K blackbody star, ... would test the convective-cover repair in synchronous rotation, ..." |

## Step 4: existing tools and Earth's counterpart (bf56cac)

Verdict: needs four MINOR fixes; nothing blocking. The reader checked Prather and Hsu's 2.5 and 1.5 W m⁻² against
their full abstract (OSTI 1563031) and the two tools against their abstracts.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1 | `repairs.tex`:117–118 | Prather and Hsu's figures are global means of sunlight intercepted and absorbed; set after the Moon's net term of −6.5 W m⁻², which includes infrared escape, "heats the climate" invited a false comparison | Applied: "intercepts 2.5 W m⁻² more sunlight than flat layers in the global mean and absorbs 1.5 W m⁻² more of it" |
| 2 | `assumptions.tex`:47 | "A geometry that suits air a tenth of a percent of the radius tall" disagreed with a cited 1.5 W m⁻² error on Earth | Applied: "a geometry made for air a tenth of a percent of the radius tall" |
| 3 | `next.tex`:27 | "Both steps" had three candidates in the sentence before, and ecCKD performs neither check | Applied: "Free tools exist for the reduction and for its check" |
| 4 | `next.tex`:29 | "Built around Earth's air" contrasted the wrong thing, since the test world's air is also nitrogen and oxygen; what is Earth's is the columns | Applied: "both were built around Earth's columns" |

## The Introduction, after the body's four steps (943ad6f)

The Introduction took in the body's new sources: Earth-built models joined to GCMs off Earth, the spread among four
GCMs on the same moist TRAPPIST-1e cases, and the fits' effects set against such spreads. It also names the
calculations of atmospheric escape made for the design, the clarification the author asked for in the abstract,
since the same unclear phrase stood here. Verdict: needs the listed fixes, the first MAJOR. The reader found the
sources matched, apart from the items below, and the claim of what is new resting on the classification and the
split into classes, as the related-work scan advises.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1 | `introduction.tex`:54–56, MAJOR | "Across models, such choices add up to measured spreads" said retained Earth values sum to the THAI spread; Sergeev et al. relate it to parameterization choices in general, and "such choices" renamed the undetected values as choices | Applied: "Plausible results can still disagree: four GCMs given the same moist cases of TRAPPIST-1e all keep it temperate, yet differ in global-mean surface temperature by 14 K with nitrogen-dominated air and 24 K with carbon dioxide, a spread their authors relate to the models' parameterization choices" |
| 2 | `introduction.tex`:55 | "14 and 24 K" left each case unnamed, and the 24 K case lies outside the Gaean class | Applied with item 1 |
| 3 | `introduction.tex`:57 | "So those values affect both ..." lost its antecedent | Applied: "so the retained Earth values affect both ..." |
| 4 | `introduction.tex`:20–21 | "Runs ... tuned the GCM's convection" gave the runs an action; Battalio et al. tuned the convection scheme with runs and observations | Applied: "\textcite{rafkin2022interaction} started a cloud-resolving model from a GCM's unstable profiles and \textcite{battalio2022interaction} tuned the GCM's convection scheme with its runs and observations" |
| 5 | `introduction.tex`:22–23 | The body's contrast, shared physics against separately built codes, was missing | Applied: "so that the global and resolved calculations share their physics", which the paragraph on separately built codes then answers |
| 6 | `introduction.tex`:33–34 | "Its exobase" bound to "the design" | Applied: "the Moon's exobase" |

## The Conclusion, after the body and the Introduction (18f4da6)

Four sentences entered existing paragraphs: the LMD's shared physics, the free tools for a reduced radiation scheme,
the Titan precedent, and the intercomparisons as further cases. Verdict: needs the listed fixes, two MAJOR. The
reader found the synthesis free of recap, the line of argument intact and the ending, unchanged, still the climax.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1 | `conclusions.tex`:35–37, MAJOR | "So what remains is to supply them with the spectra of other worlds" made supplying spectra the only step left, ahead of the checks the next sentence requires, and could be read as stellar spectra | Applied: "so the reference model would supply them with absorption spectra computed on other worlds' columns" |
| 2 | `conclusions.tex`:69–74, MAJOR | The intercomparison sentence split "additional physics" from the sentence that develops it, named nothing to measure, and SAMOSA's ExoCAM–ExoPlaSim differences lie in steam and runaway states outside the Gaean class | Applied: the sentence is removed, and the intercomparisons' planets join the planets of other rotations and spectra, "like those the THAI and SAMOSA intercomparisons define"; the SAMOSA test stays in Next steps |
| 3 | `conclusions.tex`:46–50 | The Titan sentence fell between the lunar cloud target and its consequence | Applied: it closes the target sentence, "much as \textcite{battalio2022interaction} tuned a Titan GCM's convection with resolved storms \autocite{rafkin2022interaction} and observations" |
| 4 | `conclusions.tex`:15–20 | The LMD sentence came before the gravity example, and construction shares only the physics package's own parameters, since WRF's core was adapted to Mars | Applied: the sentence follows the gravity and day sentence, "its parameters are shared by construction; in codes built separately, as here, they are made consistent by repair", and leads into "The repairs make ..." |
| 5 | `conclusions.tex`:69–71 | "Intercomparisons" unqualified generalised from two works, and SAMOSA reports one survey and a preliminary comparison | Applied with item 2: the two are named |
| 6 | `conclusions.tex`:35, 48, 69 | Three added "already"s joined three earlier ones and the ending's | Applied: "exist", "tuned", "define" |

## The abstract, last (dde4212)

Two clauses changed, keeping the text the author approved: the fits' effect is set beside the spreads measured
among exoplanet GCMs, and the radiation scheme would be reduced with existing tools. Verdict: two MINOR fixes,
nothing blocking. The reader found both clauses supported by Results, Next steps and the Conclusion, consistent
with the Introduction's wording, free of inventory, and the repository kept out.

| # | Location | Finding | Disposition |
|---|---|---|---|
| 1 | `abstract.tex`:18–22 | The comparison lengthened the abstract's longest sentence to about 71 words, and its colon let the 20 K and 6 K read for a moment as the GCMs' spreads | Applied: the sentence ends at "... the spreads measured among exoplanet GCMs.", and "Calibrating the radiation's fits ..." opens the next, with the three claim markers |
| 2 | `abstract.tex`:22–23 | "With existing tools" could attach to "spectroscopy" | Applied: "A radiation scheme reduced with existing tools from line-by-line spectroscopy, ..." |
