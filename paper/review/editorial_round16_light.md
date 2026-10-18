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
