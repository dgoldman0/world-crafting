# How the paper is built

The paper is built the way a program is: small components with stated interfaces, each drafted, checked and
committed before the next depends on it. The writing rules are in the repository's `AGENTS.md`.

| Stage | Product | State |
|---|---|---|
| 1. Ideate | `notes/ideation.md`: the question, thesis, contribution, evidence discipline, what to leave out | Done 2026-10-17 for the first draft; the second draft's framing is in `notes/outline.md` |
| 2. Root in the literature | `notes/literature.md`, `references.bib` (143 entries, each checked against Crossref, DataCite or a release record), `sources/manifest.json` | Done as far as access allows: 85 sources held locally (DEFERRED: none read in full), 58 BLOCKED |
| 3. Outline | `notes/outline.md` | Redone 2026-10-17 for the second draft; the third draft's framing (field paper, Moon as the test world, constructed worlds set up early) follows the author's reading recorded in `review/editorial_round1_dispositions.md` |
| 4. Components | `sections/*.tex`; figure scripts in `figures/` reading extracts in `data/`; `tools/regime_calc.py` for every calculated number; `claims.json` | Third draft written 2026-10-17 (c63df43); closing section rewritten as discussion and conclusions (bb5d0f0) |
| 5. Build | `main.tex`, `Makefile` (`make paper` from the root) | `make pdf` builds 31 pages with no overfull boxes; `make check` passes with three warnings (two web sources unchecked offline, two registered claims uncited) |
| 6. Review | Editorial rounds by fresh reviewer agents (`review/editorial_round<n>_*.md`) until a round finds nothing blocking; the author's readings; G7 on the final PDF; the release register | Round 1 (172 findings) acted on in the third draft; the author read the third draft and directed the closing section's rewrite; round 2 reads that section |

Machinery brought from Terluna alongside the paper: patch series for ExoPlaSim, CM1 (with WRF-ELEC's
electrification) and SWAN; the Fortran written for CM1; the reference radiative–convective model, PlaSim's
offline radiation copies and ice optics, the curved-air ledger with the spherical sky solver, and the lunar
conductivity column with its muon ionization and the charging laws. Notes on each component's correctness,
limits and room for improvement are in `notes/`, with the defect log and the verification record.
