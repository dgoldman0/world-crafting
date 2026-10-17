# How the paper is built

The paper is built the way a program is: small components with stated interfaces, each drafted,
checked and committed before the next depends on it.

| Stage | Product | State |
|---|---|---|
| 1. Ideate | `notes/ideation.md`: the question, thesis, contribution, evidence discipline, what to leave out | Done 2026-10-17 |
| 2. Root in the literature | `notes/literature.md`, `references.bib` (142 entries, each checked against Crossref, DataCite or a release record), `sources/manifest.json` (originals archived outside Git, claim locators) | Done as far as access allows: 85 sources held locally (DEFERRED: none read in full), 57 BLOCKED, 23 of them cited |
| 3. Outline | `notes/outline.md`: the argument by section, the figure and table plan, the claims register `claims.json` | Done 2026-10-17 |
| 4. Components | `sections/*.tex`, one at a time with its neighbours; figure scripts in `figures/` reading extracts in `data/`; `tools/regime_calc.py` for every calculated number | All sections drafted 2026-10-17; 98 claims registered and checked for sources |
| 5. Build | `main.tex`, `Makefile`: LaTeX build, citation and claim checks | `make pdf` builds with no overfull boxes; `make check` and `make lint` run clean of errors |
| 6. Review | the ten prose passes per section (`review/passes_*.md`), two technical referees and their dispositions (`review/referee_*.md`), the whole-manuscript challenge (`review/whole_manuscript.md`), exact-build PDF review by hash (G7), release register | Passes done (self-review, silent); 94 referee findings acted on; the challenge is running; G7 and the register follow the final build |

Machinery brought from Terluna alongside the paper: patch series for ExoPlaSim, CM1 (with WRF-ELEC's
electrification) and SWAN; the Fortran written for CM1; the reference radiative–convective model,
PlaSim's offline radiation copies and ice optics, the curved-air ledger with the spherical sky solver, and
the lunar conductivity column with its muon ionization and the charging laws. Notes on each component's
correctness, limits and room for improvement are in `notes/`, with the defect log and the verification
record.
