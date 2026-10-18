# Terracompatible terminology and whole-manuscript framing, 18 October 2026

## Author's review and requested revision

The author read and accepted the ensemble-centred Conclusion from source commit
`1b5b03d6c0e0724b209997a1cd00b280f37f68b3`, whose exact-build inspection was recorded at
`f3d15117aef13d0cf0703b61fd686a5f49450bfa`. The accepted Conclusion's SHA256 is
`b1a0cb6ab18c6febfcf35cd7a9f2d01cdb0dd849e5a32a7176b194462761ff8a`.
The author wrote:

> Terracompatible is a good one. The conclusion is quite good except it should use terracompatible instead of Earth-like and just maybe one sentence best place just so it's clear that the ensemble could also eventually be useful for modeling other worlds beyond just terracompatible ones and the ensemble work gets us closer to that too. Other than that the conclusion is good.
>
> Let's see.. we should coin terracompatible early so probably the introduction. We should also make sure it's used properly throughout and since we're doing a check throughout anyway we should double check that the paper aligns with our central frame.

This is the author's review of that Conclusion. The requested terminology revision and whole-manuscript
check are the next work; the author's acceptance preserves the Conclusion's argument and ending.

## Definition and scope

The author selected the word after the terminology discussion; the introduction stipulates its physical
meaning: nitrogen–oxygen atmospheres, water as the principal condensable, and surface pressures and
temperatures broadly comparable to Earth's, permitting liquid surface water and an active water cycle.
Gravity, size, rotation and starlight may differ substantially. The abstract gives a compact definition.
The code's tested and calibrated ranges remain stated separately.

The nitrogen–oxygen requirement preserves the narrow resemblance intended in the author's earlier
description. Oxygen-free nitrogen cases remain literature comparisons and proposed tests of the general
repairs; Titan, present Mars and Venus remain comparisons requiring further physics. An exploratory
scope audit proposed a nitrogen-dominated definition with freely varying oxygen; that broader definition
was set aside because the comparison cases can be discussed outside the named class.

The new sentence follows the Conclusion's paragraph on testing planetary parameters and additional
physics:

> With radiation and cloud microphysics developed for other gases and condensables, the couplings and general repairs could also form the basis for extending the ensemble beyond terracompatible worlds.

The sentence is prospective and conditional on further physical development. The rest of the approved
Conclusion receives the requested term substitution and, where needed, page-break adjustments.

## Whole-manuscript reading and changes

Codex, the drafting assistant, read the twelve section files and `main.tex`, with two independent
read-only audits before revision. `/root/terracompatible_framing_audit` examined the whole manuscript's
governing purpose; `/root/terracompatible_scope_audit` examined terminology and physical scope in the
seven sections using or defining the class. These audits informed drafting; the fresh editorial round
below reviews the revised text.

| Location | Finding and disposition |
|---|---|
| Title, abstract and Introduction | Name ensemble development for climate, storms and seas at the outset; define terracompatible in the independently readable abstract and Introduction. The Moon remains the starting case. |
| Introduction, retained Earth values | Remove the claim that familiar air and water keep inputs inside a model's fitted range: the lunar column already exceeds some radiation ranges. Describe plausible output from familiar constituents while an Earth constant remains. |
| Introduction, final sentence | State the lunar-only application away from Earth's values with numerical controls excepted, preserving the Earth benchmarks described later. |
| Atmosphere descriptions | Use nitrogen–oxygen or nitrogen-dominated air where composition is the claim. The class adjective applies to worlds. |
| Worlds and Figure 1 | The illustrative slow rotators hold Earth's gravity, radius and atmospheric state fixed. Name those conditions in text and caption, and label the plotted points “Earth parameters, longer days.” Regenerate only that figure. |
| Reach | Open with intended versus tested applicability and the operations needed for another world; remove the repeated lunar sensitivity summary. State current implementation restrictions within the terracompatible class. |
| Next steps | Organise the opening around consistent heating and cloud, the shared radiation reference and tests across worlds; retain the lunar experiments and numerical thresholds. Relate the reference and drop-size experiments to their use across worlds. |
| Conclusion | Substitute the term and add the single prospective sentence above. Preserve all twelve paragraphs and the approved ending. |
| Availability | Record the author's acceptance and requested revision as the author's review. |
| Repository guidance | Align AGENTS.md and README.md with the term and ensemble purpose. Mark the second-draft outline and third-draft build-stage table as historical, with a pointer to current records. |
| Historical evidence | Preserve earlier drafts, review quotations, source titles and extracted source descriptions in their recorded wording. |

## Fresh editorial round 14

The revised manuscript was frozen for two fresh agents, each given the current text, the writing rules
and the author's latest direction. Their separate records identify input hashes and the actual scope:

- `editorial_round14_whole_prose.md`: whole-manuscript framing, terminology and prose, plus the
  figure-label diff.
- `editorial_round14_whole_scope.md`: whole-manuscript evidence states and physical scope, with source
  checks of the changed composition descriptions.

Both reviews found the revised terminology and ensemble framing ready for the author's reading within
the requested scope, with a single copy correction: Introduction lines 12–13 had “an nitrogen–oxygen
atmosphere” after the composition replacement. R14-P1 and S14-07 were resolved by changing the article
to “a”. The scope reviewer checked the changed gas descriptions against passages from five archived
originals; those selected readings retain their source-admission limits. The prose reviewer also reviewed
the two-line figure-script diff and found its plotting operations unchanged.

The drafting assistant then recorded the completed round in Availability and replaced the Conclusion's
old page enlargement with a three-baseline space requirement before its penultimate paragraph, keeping
that paragraph's opening with the following lines. These changes preserve the approved prose outside
the requested term and single sentence. The AGENTS.md purpose statement also replaces an ambiguous
“Its” with “The paper's”.

## Checks performed

- `make -C paper check`: exit 0; 13 TeX files, 73 cited keys of 152, 106 cited claims of 108.
  Existing warnings concern the offline web records for H23 and N02 and uncited entries S01 and V14.
- `LC_ALL=en_US.UTF-8 make check`: exit 0; pinned-source and patch checks passed, 77 Python tests passed.
  The only Python source edit changes a figure label and its explanatory comment.
- `python3 paper/tools/lint.py`: screening completed across all sections. It found zero excluded
  “not” or “rather than” candidates; the other matches remain reading prompts. An initial `--help`
  invocation was rejected because the script accepts file paths; the subsequent full invocation completed.
- `make paper`: the first revised build completed at 35 pages with zero overfull boxes. The drafting
  assistant inspected Figure 1 and the title and Conclusion pages; a paragraph-opening orphan in the
  Conclusion was corrected with the space requirement described above. A second build and inspection of
  pages 25–26 confirmed that both closing paragraphs remain whole. Final exact-build review follows the
  completed source revision.
- An exact source comparison against the accepted Conclusion, after removing the two layout commands,
  confirms that the requested term and single sentence are its entire prose change.
- `git diff --check`: passed. The final paper check after the copy correction passed with the same
  pre-existing warnings.

The checks establish the operations reported. Physical validation, full-document source admission and
publication release retain the outstanding work recorded in `release_register.md`.
