# Release register

Kept by Claude Opus 5.5, the drafting assistant, on 18 October 2026, under the editorial charter's E4: PASS, BLOCKED or
DEFERRED for each gate, with the exact artifact and its evidence. A status records work performed; nothing here is
prefilled, and any change to a build input reopens the gates it touches.

The artifact and gate judgments below describe the historical build from 94d337a. The fresh conclusion of
18 October 2026 has its initial draft, review and build record in `conclusion_rewrite_2026-10-18.md`.
The author read and rejected that draft's lunar framing. Its replacement, centred on the model ensemble,
has its record in `conclusion_ensemble_rewrite_2026-10-18.md`. The author accepted that Conclusion and
requested the terracompatible terminology, one prospective sentence and a whole-manuscript framing check,
recorded in `terracompatible_revision_2026-10-18.md`.
G1–G5 and G7 release judgments for the new artifact remain DEFERRED, with G6 and E4 still BLOCKED by the
source-admission and release work listed below.

## The artifact

| Item | Value |
|---|---|
| Source commit | 94d337a (`94d337a68f248528f54b09421d403ab942216003`), clean for every build input |
| PDF | `paper/build/main.pdf`, sha256 `c0c63cf1eff7c476a6913f0b06830f9d9a03ec8c48de50e099688d67aa17ff55`, 34 pages |
| Build | `make paper`; `SOURCE_DATE_EPOCH=1792299769` (the last commit that changed a build input), `FORCE_SOURCE_DATE=1`; pdfTeX 1.40.25 (TeX Live 2023/Debian), latexmk 4.83, biber 2.19; two clean builds byte-identical |
| Input hashes | Listed in `g7_visual_review.md` for `main.tex`, `references.bib`, `Makefile`, the thirteen section files and the six figure PDFs |
| Claims register | `paper/claims.json`, sha256 `e462d3ff93eea66bb201aa51d42977bccff8b95f9099efc9559a01b487569745`, 108 claims |
| Source manifest | `paper/sources/manifest.json`, sha256 `afe0042bfc11c660958ed4fd5ab7ed524fb9dc4a2324fd8ebeab89ad9965b1c3`, 152 records |

## Checks run on this state

These establish record completeness and code integrity; they clear no editorial gate.

| Check | Result, 18 October 2026 |
|---|---|
| `paper/tools/check.py` | Exit 0: 13 TeX files, 73 cited keys of 152, 106 of 108 claims cited. Warnings: S01 and V14 registered and uncited; the web source of H23 and N02, ExoPlaSim issue #69, recorded and unchecked offline |
| `make check-patches` | Exit 0, 18 checks: the pinned archives of ExoPlaSim 3.4.2, CM1 r22.0, SWAN 41.51 and SWASH 12.01 and three WRF-ELEC source files match their pins; the ten ExoPlaSim patches reproduce the deployed `radmod.f90` and `rainmod.f90`; nine CM1 r22.0 build variants reproduce their deployed sources; the SWAN patches apply |
| Python tests | 111 passed, in the research drive's `optics` environment (numba 0.68.0, pytest 9.0.2); the code under `python/` and the patch series are unchanged since the run recorded at 6c8a68f |
| `paper/tools/lint.py` | Run as screening during the rounds; its candidate places were read, and it clears nothing |

## Gates

| Gate | Status | Evidence | What remains |
|---|---|---|---|
| G1 Argument and reorderability; G2 Audience and economy; G4 Affirmative stance and exact action, for the closing section and the abstract | DEFERRED | Seven rounds of two fresh reviewers each (rounds 2–8, `editorial_round<n>_conclusion_{prose,evidence}.md`), with dispositions; the eighth round's prose and evidence records found nothing blocking; its major and minor findings were acted on in 94d337a, unread by a further round | The author's reading, decisive under the repository's rules |
| G1, G2, G4 for the rest of the body | DEFERRED | Round 1 read the second draft (172 findings, dispositions in `editorial_round1_dispositions.md`); the third draft acted on them; the author judged the rest of the paper to stand for now; passages revised beside the closing section were read in rounds 2–8 | The author's reading of the third draft's body as revised; a fresh round on the whole body if the author wants one |
| G3 Inheritance, syntax, transitions and cadence | DEFERRED | Silent cadence readings in every round, recorded as silent; the author counted the stream-of-thought reading of the first draft as that draft's cadence review | The read-aloud pass of the conclusion, the major transitions and the dense passages, which the charter requires, by the author |
| G5 Technical meaning, evidence status and discriminating tests | DEFERRED | The claims register resolves every marker; two technical referees checked the first draft's claims and table rows; evidence rounds 2–8 checked the closing section and the revised passages against the register, the run records and the archived sources; round 7 found and the revision corrected a factual error on the sign of the ground strikes | An evidence check of the third draft's body as a whole, last made by the first draft's referees; the author's reading |
| G6 Full-document source admission | BLOCKED | Of the 73 cited sources, 30 have no legal local original (admission BLOCKED); 43 have an archived original (DEFERRED), 33 of them read at claim locators, 7 at the abstract, 2 unread and 1, the author's own issue report, in full; none is admitted | Originals for the 30, and full readings, with appendices and bibliographies, of every cited source; or a substantive revision of each dependent use |
| G7 Exact-build visual and production review | PASS | `g7_visual_review.md`: every page of the PDF above read in the poppler render, the six figure pages again in MuPDF's; fonts embedded, metadata set, links present; no blocking finding | The author's own inspection; three notes for the author in that record (the title page's date, one loosely set reference line, Table 4's last row alone on page 22) |
| Whole-manuscript challenge (E4) | DEFERRED | The first draft was challenged (`whole_manuscript.md`, dispositions in `whole_manuscript_dispositions.md`) | A challenge of the third draft as revised |
| E4 Release integrity | BLOCKED | This register | G6; the publication of the world-crafting repository with the paper's release commit, which the availability statement promises; the author's confirmation of the AI-assistance disclosure's wording on Codex and ChatGPT; the author's final reading; the deferred gates above |

Terluna's ensemble audit belongs to its five-paper ensemble, which this paper stands apart from by the repository's
`AGENTS.md`, so it has no row here.

## Reviewers

Every reviewer named in these records except the author is Claude Opus 5.5, the model that drafted the paper, as main
session or subagent; `README.md` in this folder lists them with their records. No review by a person other than the
author, or by a journal, has been made.
