# World-crafting

The models, patches and in-house tools for studying found and crafted worlds with Earth-built
atmosphere, storm and wave models, and the paper that describes them. The first world is Terluna's
breathable Moon (github.com/dgoldman0/Terluna); the machinery here was brought from Terluna at commit
186b294 (2026-10-17) and its provenance is recorded file by file in `PROVENANCE.md`.

## Commits

Use informative commit messages. Multiple phrases for a commit message.

## System usage limits

Be mindful of system resource availability, especially when other sessions run tests or models on the
same machine. The GCM, CM1 and SWAN runs themselves stay in Terluna; work here runs patches, offline
tools and tests.

## Where work goes

| Work | Home |
|---|---|
| A patch to an upstream model, or Fortran written for one | `models/<model>/` with its README: what each patch changes, its switch and default, its verification and its limits |
| An in-house reference or calibration tool | `python/`, under the package path it had in Terluna so its imports and history stay traceable |
| Notes on correctness, limitations and room for improvement | `notes/`, one file per component |
| The paper | `paper/`: notes, sections, figures, data extracts, source records, review records |

Case set-up, run bookkeeping and analysis scripts stay in Terluna. Upstream source code is never
committed whole: patches are applied to the pinned upstream archives named in each model's README.

## File and evidence practice

These follow Terluna's AGENTS.md (sha256 7fac1ca0…be6 at 186b294):

- A runnable calculation, numerical convergence, an input hash, a proposed design and empirical
  validation are different evidence states. State assumptions and boundaries near outputs.
- Never fill an empty topic with invented results or mark future work complete. Never silently
  substitute data after a failed download or hash mismatch.
- Review redistribution rights before adding outside datasets, source code or full papers, and
  record their source, hash and credit. Full papers archived for reading stay outside Git
  (`paper/sources/originals/` is ignored); their records are committed.
- Report actual checks and unperformed work.

## The paper

The paper holds to the general writing and evidence requirements of Terluna's editorial charter
(`ensemble/planning/Open_Moon_Editorial_Charter_control-01.md`, sha256 aac4a4f2…0b0): the gates G1–G7,
release integrity E4 and the ten separate prose passes. Headings stay unnumbered and few. Each
section is drafted and reviewed with its neighbours, its passes are recorded in `paper/review/`, and
the release register uses PASS, BLOCKED and DEFERRED with exact artifact hashes; nothing is prefilled.
Author metadata: Daniel S. Goldman, ORCID 0000-0003-2835-3521, no affiliation label. Final releases
carry an accurate AI-assistance disclosure and the actual review history.

## Checks

`make check` runs the Python tests and the patch checks (each patch series applies cleanly to its
pinned upstream source). The paper builds with `make paper`.
