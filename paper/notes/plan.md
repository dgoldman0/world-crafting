# How the paper is built

The paper is built the way a program is: small components with stated interfaces, each drafted,
checked and committed before the next depends on it.

| Stage | Product | State |
|---|---|---|
| 1. Ideate | `notes/ideation.md`: the question, thesis, contribution, evidence discipline, what to leave out | Done 2026-10-17 |
| 2. Root in the literature | `notes/literature.md`, `references.bib`, `sources/manifest.json` (bibliographic checks, open originals archived outside Git, claim locators for the claims that rest on a source) | Started |
| 3. Outline | `notes/outline.md`: the argument by section, the figure and table plan, the claims register `claims.json` (every number traced to a Terluna file at 186b294 or to a calculation here) | Pending |
| 4. Components | `sections/*.tex`, one at a time with its neighbours; figure scripts in `figures/` reading extracts in `data/` | Pending |
| 5. Build | `main.tex`, `Makefile`: LaTeX build, citation and claim checks | Pending |
| 6. Review | the ten prose passes per section and the whole-manuscript challenge, recorded in `review/`; exact-build PDF review by hash; release register | Pending |

Machinery brought from Terluna alongside the paper: patch series for ExoPlaSim, CM1 (with WRF-ELEC's
electrification) and SWAN; the Fortran written for CM1; the reference radiative–convective model,
PlaSim's offline radiation copies and ice optics, and the curved-air ledger with the spherical sky
solver. Notes on each component's correctness, limits and room for improvement go in `notes/`.
