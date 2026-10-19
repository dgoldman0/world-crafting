# Final reader review after the declarations cleanup, 19 October 2026

## Direction and snapshot

The author rejected the earlier final skim for overlooking the internal revision history embedded in the
manuscript. After Claude removed that history and revised the declarations and associated passages, the
author requested another final review. The acceptance threshold remains substantial errors, missed central
points, inappropriate material and novelty overclaims; minor polishing stays below that threshold.

- Source reviewed: `6a35a24317fe6b325f64a4974739def3fb92ec14`.
- Latest manuscript change: `1da5034c5cd9342d052222fa665deb4f6af293af`.
- Existing PDF: 37 pages, SHA256 `9f6744e43bb561358aaf0b276b8665e78120efdbe9d51d859877ed8cb864be16`.
- Manuscript files remain as reviewed. This record and its index entry are the changes from this review.

## Reviewers and scope

Two fresh Codex agents, `final_reader_facing_review` and `final_reader_coherence_review`, each read
`main.tex` and all thirteen included sections, including tables, captions, the appendix and declarations,
against the author's direction and AGENTS.md. The reader-facing reviewer also read the four governing
editorial sources. The coherence reviewer checked claim H26 and the cited CM1 provenance records.

The primary Codex reviewer inspected the changes since the previous skim, checked the three findings below
against their surrounding text, read the original CM1 investigation record, checked the OpenMP specification,
and inspected rendered PDF page 31, which contains the complete declarations. That page is legible and the
declarations fit the paper. The visual inspection covers this page only; the existing whole-build review
remains a separate record.

## Findings and disposition

**Decision: BLOCKED at the requested substantial-error threshold by the three inference claims below.**
The manuscript's removal of internal editorial history resolves the author's immediate objection. The
ensemble remains the subject, with the Open Moon as the worked case and broader applications prospective.
Both fresh reviewers found the current declarations appropriate; the reader-facing reviewer found no
substantial instance of familiar work presented as newly invented.

1. **An upstream CM1 race is asserted beyond the recorded diagnosis.** At `assumptions.tex:130–134`,
   H26 treats threaded divergence as an established defect in released CM1. That diagnosis contributes to
   the five-defect count in the abstract and Introduction and to the inventory table's classification.
   The cited Terluna `climate/crm/README.md:80–110` records intermittent divergence in patched lunar builds,
   including plain Morrison builds, and an inconclusive search with selected processes disabled. Its
   inference that intermittent divergence excludes summation order is unsound: the
   [OpenMP 5.2 specification, section 5.5.6](https://www.openmp.org/spec-html/5.2/openmpsu50.html)
   leaves reduction combination order unspecified and permits differing results between repeated parallel
   executions at the same thread count. The evidence establishes threaded nonrepeatability; a race and
   its attribution to released CM1 remain hypotheses. This review leaves the actual cause unresolved.
   **Disposition:** refer to the author for qualification of H26 and its dependent claims, or stronger
   diagnostic evidence. Found by the coherence reviewer and checked by the primary reviewer.

2. **The remaining temperature offset receives a stronger causal attribution than the tests justify.**
   At `results.tex:130–132`, the remaining degree or two is attributed to upward heat transport
   "by elimination", although the immediately preceding text leaves the high-altitude ice's radiative
   effect unquantified and the dry-ground test at 45 degrees north unperformed. The differing mixing
   depths make boundary-layer transport a plausible explanation while these alternatives remain open.
   **Disposition:** refer to the author to state the transport explanation as a hypothesis. Both fresh
   reviewers raised this finding independently; the primary reviewer confirmed the contradiction in scope.

3. **Agreement with a third GCM is promised as a decisive diagnosis.** At `next.tex:67–70`, the proposed
   independent GCM comparison would identify which current model errs and place the error in named
   schemes. Temperature agreement can guide controlled comparisons and priorities; shared biases and
   compensating errors leave the causal diagnosis open. **Disposition:** refer to the author to narrow
   the promised inference to prioritising further tests. Both fresh reviewers raised the finding. The
   previous skim acknowledged this wording and judged it below threshold; this pass treats it as material
   alongside the related causal attribution in Results.

The reader-facing reviewer also suggested trimming the future-project intention in `availability.tex:4`.
That suggestion is optional polish and carries no blocking disposition. Findings on approved wording go
to the author; this review makes no manuscript revisions.

## Checks actually performed

- `make -C paper check`: passed; 14 TeX files, 96 cited bibliography keys of 167, and 107 cited claims of 109.
  Existing warnings concern offline checks of H23 and N02 and uncited S01 and V14. This checks record
  structure and references, with scientific and editorial judgment supplied by reading.
- GitHub repository metadata confirmed that both `dgoldman0/world-crafting` and `dgoldman0/Terluna` are
  public. The availability statement distinguishes their code and derived products from raw output
  available by request.
- The current PDF's hash matches the last build recorded in round 19. Rendered page 31 was inspected.
- Model integrations, the software test suite, a new PDF build and a new full-document visual pass remain
  outside this review. The review leaves the physical cause of CM1's threaded divergence unresolved.

The earlier PASS remains in its historical record. This review supplies the current decision and the
findings returned to the author; the release register retains its own artifact-specific evidence.
