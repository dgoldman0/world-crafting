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

## Committed artifact and exact-build inspection

| Item | Value |
|---|---|
| Source commit | `119b168d0f4053f92a52a28266807718369c2832` |
| PDF | `paper/build/main.pdf`, 35 A4 pages |
| PDF SHA256 | `45de8d3b2eaa2a6c1548e2cabcc8c0109cf0189ad81f15c895f981ace74970bd` |
| Build date input | `SOURCE_DATE_EPOCH=1792334837`, `FORCE_SOURCE_DATE=1` |
| Final build | `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`, from `paper/`, after the source commit |
| Tools | pdfTeX 1.40.25, latexmk 4.83, biber 2.19; Poppler 24.02.0 and MuPDF 1.23.10 |
| Metadata | Title matches the printed title; author Daniel S. Goldman; date 18 October 2026 |
| Fonts and links | `pdffonts`: all 26 listed font entries embedded; `mutool show ... grep`: 211 link annotations, with the author's ORCID URI present |
| Build warnings | Zero overfull boxes; one underfull line, badness 2894 |

The final source matches the input hashes in the round 14 reports, including the prose review's bounded
disposition verification. That verification reversed only the article, layout, disclosure and AGENTS.md
clarification edits in memory and recovered the reviewed hashes.

The final PDF was rendered with `pdftoppm -scale-to 1600 -png`. The visual records identify the actual
pages inspected and their observations:

- `terracompatible_visual_pages01-18.md`, by `/root/round14_whole_prose`.
- `terracompatible_visual_pages19-35.md`, by `/root/round14_whole_scope`.

Together the reviewers inspected all 35 rendered pages and found zero blocking layout issues. The first
record notes one minor widow line at the top of page 14, completing the preceding Verification paragraph;
the sentence is complete and readable. This observation is retained for a later production pass.

The drafting assistant also inspected page 4, containing the changed Figure 1, in MuPDF's independent
120 dpi render. Its label, points, axes and caption remain readable and clear of collisions. Preliminary
Poppler inspections covered the title and Conclusion; the final render preserves both closing paragraphs
together on page 26. These visual operations assess the specified artifact; the outstanding release
work in the register retains its evidence states.

### Other build-input hashes

The round 14 reports identify `main.tex` and every section by hash. The remaining build inputs are:

| File | SHA256 |
|---|---|
| `paper/Makefile` | `a79bebc7bc3abc1f5e14e31aceddabfa2bbdffee6bf9587a4b9ebf5e9949ad7d` |
| `paper/references.bib` | `c0c9662b362141759bce9a27bb566e7ee6a00479ef773273f1dc109d7888747e` |
| `paper/figures/fig_regimes.pdf` | `5f5e1b1fb96989db519b921eba1d19fe1588f07e0b9a1f706def8677b34eb6cf` |
| `paper/figures/fig_sun_clock.pdf` | `1a70fb8a8c7b6ee2f4593098c88b8f1337a91fe1f852010b15e33df1ae6affe6` |
| `paper/figures/fig_slant.pdf` | `5af5b9ead93a4b611b79c58479afeac4a3704f0390cb3b20260739f954811ee4` |
| `paper/figures/fig_layers.pdf` | `119955426500005e90653008a80bf9a37b4c570875c20ff3576d85dae8bb701a` |
| `paper/figures/fig_repairs.pdf` | `2fcb37ca7a6538c8187332ede7682c57d0111ecc087c89e454835865d31c59c9` |
| `paper/figures/fig_gap.pdf` | `943022583a689edf2a10a0cd68503b9131280d9695f51ec0568f30e5373bd422` |
