# Version 2: the added section rewritten as the paper's changes, 11 November 2026

Kept by Claude Fable 5.2, the drafting session.

## The author's direction

Seeing the section's title, the author wrote: "Refinement of the... MODELS? No... No. That's not the purpose of it.
[...] That's not supposed to be a log of the models. It's supposed to be the place where it summarizes what changed
from paper v1 to paper v2. Obviously that includes how v1 vs v2 understand what models, the model states, etc. It
should have always been a section about the paper's change so that the readers can quickly understand the new
version if they come from the old or before they read the old one how things are different." The drafting session
had read the earlier direction for the section as an account of how the models were refined, and had drafted and
titled it so since 8 November. The author approved a rewrite as "Changes from the first version", organised by what
a reader needs: what the paper now says differently, how the models and the design case differ between the versions,
what is new, and what was taken out.

## What changed

- `paper/sections/refinement.tex` becomes `paper/sections/changes.tex`, titled "Changes from the first version": an
  opening paragraph, Table `tab:changes` with ten rows that set the first version's statement beside this version's,
  a paragraph on what this version adds, and a paragraph on the first version's results that stand under a
  condition, the withdrawn figure and the run histories kept in the notes.
- The first version's statements rest on a new claim, C01, whose sources are `paper/notes/corrections_after_v1.md`
  and the root README's table; this version's statements carry the claims they carry elsewhere in the paper.
- Three framings of known work that the old section alone cited keep a place: the weak-temperature-gradient
  method's reason (Sobel and Bretherton) opens the boxes that make their own ascent in Results; the South
  Pole–Aitken basin's turn of the Moon (Keane and Matsuyama) joins Reach's paragraph on worlds turned by their
  water; and tuned parameters taking up a model's imbalance (Hourdin and others) joins Reach's recipe, with the two
  checks the old section stated: budgets closed against the surface and a second model, and a design climate checked
  after each retune for where its heat goes. The orientation's derivation was the recipe's first step already.
- The routes by which each fault was found, and the two sea boxes by the GCM that forced them, leave the paper; the
  defect log and `notes/cm1.md` hold them. Claim G25 leaves the register.
- `paper/notes/v2_realignment.md` names the section's new file.

## The second draft, the same day

The author read the first draft and found it too short: "It includes nothing on the change of understanding of the
lab ensemble and its components and what's planned. I wanted it from 'Changes from the first version' focused on
the changes in what the paper says. You did that. You also threw out ALL detail. You can avoid annoying specifics.
It should at least give the reader a general understanding."

The section now opens as before and keeps the table, and six paragraphs give the changes in general terms: the tie
between the cloud-resolving model and the GCM, from a hold above an Earth height read largely as a measure of the
GCM's fits to forcing through the whole column, an agreement test and a difference given as a range between two
couplings; the GCM's Earth values, found also in the physics of its lower air, with what the design case now runs
and what stays open; CM1 audited as the GCM is; the scenario, turned by its water and held at its design
temperature with the twilight counted once; the longer inventory and the checks it brings to a further world's
set-up; and the order of the work ahead, with the first version's results that stand under a condition. The first
draft's two closing paragraphs are folded into these.

## Checks

`make paper` builds with no warning, to 44 pages for the first draft and 45 for the second, the section on page 29;
`paper/tools/check.py` passes with 146 claims cited of 148 registered; the sections hold neither excluded word; the drafting session read the section in
the built PDF's text. The draft goes to the author, whose reading comes ahead of any reviewer's.
