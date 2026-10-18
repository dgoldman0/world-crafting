# Check of the terracompatible revision, 18 October 2026

Checker: Claude Opus 5.5 (main session, model ID `claude-opus-5-5[1m]`), at the author's request of 18 October
2026: "give a pass over the work that codex gave back because it's done with its editorial work." Input: branch
`paper/conclusion-development` at `32df62e`, whose build inputs are those of `119b168`. Codex's commits `d25d587`
to `32df62e` were read with their diffs and records.

## Checks performed

| Check | Result |
|---|---|
| Clean build of `32df62e` in a separate worktree (`make -C paper pdf`) | PDF sha256 `45de8d3b2eaa2a6c1548e2cabcc8c0109cf0189ad81f15c895f981ace74970bd`, the hash recorded in `terracompatible_revision_2026-10-18.md`; 35 pages; zero overfull boxes; one underfull line, badness 2894 |
| `LC_ALL=en_US.UTF-8 make check`, in the main tree | Patch checks passed; 77 Python tests passed. In the worktree the patch checks stop at BLOCKED, since the pinned upstream folder lies outside Git |
| `make -C paper check` | Passed, with the existing warnings: offline web sources for H23 and N02; S01 and V14 uncited |
| `make -C paper figures`, in the worktree | The six figure PDFs equal the committed ones apart from their CreationDate stamps, and the PNGs are identical: the committed Figure 1 is the one its script makes |
| The author's words quoted in `terracompatible_revision_2026-10-18.md` and round 14's records | Identical to the author's message to Codex at 14:37 UTC (Codex session `rollout-2026-10-18T09-50-47-01a14f47-7e13-76f2-9f3e-b34844561299`) |
| Commit hashes replaced when Codex's commit messages were rewritten on 18 October | None cited in the repository |
| "Earth-like" in `main.tex` and the sections | None |
| Reading against the body and `claims.json` | Abstract, Introduction, Worlds with Figure 1's caption, Reach, Next steps, the changed line of Results, Conclusion and Availability. The Conclusion's statements agree with the body: fall speeds changing by powers of gravity set by each particle's law (Worlds l.86–90), the dimming eased from 5.0 to 3.0% when the corrected radiation ran (Results l.58–59), the arrangements of charge under the two charging laws (Results l.158–166), the transport imposed on CM1's rings (Repairs l.171–182), the similarity of the scaled seas (Verification l.38–49). The Conclusion stands as the author accepted it. |

## Corrections

| Location | Text read | Correction | Basis |
|---|---|---|---|
| Availability, Author and assistance | "followed by revisions from the drafting assistant" | "followed by Codex's revisions" | The paper names Claude Opus 5.5 as its drafting assistant; Codex made these revisions (`conclusion_rewrite_2026-10-18.md`) |
| Availability, Review history | Round 8, then "After further revisions, the author rejected the conclusion's summary structure", then rounds 11 and 12 | The author's readings of the conclusions of 94d337a and 04a6c27, with rounds 9 and 10 between them | The history omitted those two readings by the author and both rounds |
| Availability, Review history | "The agent cadence reviews were silent." | "Every agent read for cadence silently.", followed by one sentence on this check | Clarity; the history records each review |
| Results l.119 | "about 1.5~K of the bracket is the GCM's own over-cooling" | "... the GCM's over-cooling beyond CM1's" | Round 10, finding 12: by Results l.105–108 and G07 the GCM sheds about 6 W m⁻² more than CM1, worth about 1.5 K; Terluna's `climate/crm/README.md` l.1190–1193 puts PlaSim's own over-cooling near the ground at about 2.5 K's worth |
| `notes/cm1.md` l.121 | "over-cooling of its own lowest layers accounts for about 1.5 K" | "over-cooling of its lowest layers, beyond RRTMG's in CM1, accounts for about 1.5 K" | The same |
| Reach l.4–5 | "Beyond Earth's values and numerical controls, the breathable Moon remains the sole simulated case." | "Away from Earth's values, numerical controls apart, the breathable Moon remains the sole simulated case." | The wording of the abstract and Introduction; "beyond ... numerical controls" read as if the Moon lay past the controls |
| Next steps l.37–38 | "refitted before the reference is used for further worlds" | "refitted against a corrected reference before it serves further worlds" | A departure from LBLRTM or the DISORT solver faults the reference itself, and the fits follow its correction |
| `README.md` here | History to round 8, then round 11 | History, reviewers and files brought up to date; round 10's evidence record committed | Rounds 9 and 10 and the author's readings of 18 October |

## Open for the author

- The abstract runs to about 490 words; the author set its length aside on 18 October.
- The tested range, the Moon alone away from Earth's values, is stated in the abstract, the Introduction, Reach,
  Next steps and the Conclusion.
- The name of the class: terracompatible stands in the text while the author weighs it.

## Build after the corrections

| Item | Value |
|---|---|
| Source commit | `12678a9e2367c7435a47c3a4be196f3c36f59ce4` |
| PDF | `paper/build/main.pdf`, 35 A4 pages, from `make -C paper clean` and `make -C paper pdf` |
| PDF SHA256 | `fd4bf48ba1fcb5a79a2d6042621cc06abebd6dac95bb9cfe58a51d32dc747992` |
| Build date input | `SOURCE_DATE_EPOCH=1792336037`, the source commit's time, with `FORCE_SOURCE_DATE=1`; printed date 18 October 2026 |
| Warnings | Zero overfull boxes; the one underfull line, badness 2894 |
| Fonts and links | `pdffonts`: every font embedded; `mutool show ... grep`: 211 link annotations |

Rendered with Poppler at 50 dpi, the build of the corrected sources made before the commit differed from the
inspected build `45de8d3b…70bd` on pages 18–20, 23 and 30–35 alone. Pages 18–20, 23, 30, 31 and 35 were rendered
at 1,600 pixels high and read: the gap between the models and the storms in Results (18), Figure 6, the seas and
the opening of Reach (19), Reach (20), Next steps from the reference check to the charge (23), Availability with
the start of the references (30–31) and the last references (35). Each is legible, with no collision, overflow or
stranded line. Pages 32–34 hold references alone and were checked by their text layer: each begins and ends on a
whole entry. The final build from `12678a9` renders identically to that earlier build on all 35 pages.

## After the author's reading of this check

The author read this check's report on 18 October and, of the statement it listed as repeated, wrote: "Not only
is it said over and over again, it's phrased an a very stupid way. "Simulated away from Earth's values" is an
example of a thing verbing something it doesn't verb." Then: "It's not just a matter of reducing it and rewording
it. You have to be careful beacuse it was from the start defensive posturing. Make sure when you reword it and use
it sparingly in the reworded sense that it's simply informing rather than defensive posturing." The author judged
the abstract's length fine for now; the name of the class stays under the author's consideration.

The statement stood in seven places, and a related clause in an eighth. It now informs once, at the opening of
Reach, where a modeller reads what the repairs were built for and where they have run:

> Table~\ref{tab:reach} gives, property by property, the range each repair was built for; the breathable Moon is
> the first world besides Earth that the repaired codes have simulated.

| Location | Before | After |
|---|---|---|
| Abstract | "The test world, whose climate is unobserved, is the only world the repaired codes have simulated away from Earth's values, numerical controls apart. There the two general repairs measured singly moved ..." | "On the test world, whose climate is unobserved, the two general repairs measured singly moved ..." |
| Introduction, last sentence | "...; away from Earth's values, numerical controls apart, the repaired codes have so far run on the Moon alone." | The clause removed |
| Reach, opening | "Extending the ensemble to another world requires distinguishing the range each repair was built for from the conditions in which it has been tested. Away from Earth's values, numerical controls apart, the breathable Moon remains the sole simulated case." | The sentence quoted above, followed by "To extend the ensemble to another world, a modeller applies the general repairs unchanged within those ranges, ..." |
| Reach, how the Earth values err | "..., and the test world is the only world those models have simulated away from Earth's values." | The clause removed |
| Reach, worlds near the existing fits | "..., and ExoPlaSim's runs of these planets have yet to be made." | The clause removed; the paragraph's "would need" already marks those runs as prospective |
| Table 4, caption | "...; apart from the Earth benchmarks and numerical controls, the test world is the only world the adapted models have simulated." | The clause removed |
| Next steps, a test of the reach | "Away from Earth's values, the repaired models have run on the test world alone." | The sentence removed |
| Conclusion | "The breathable Moon remains the sole case run away from Earth's values, numerical controls apart. Further cases would measure ..." | "The breathable Moon is the first of them, and further cases would measure ..." |
| Availability, review history | | One sentence recording the author's judgement and the recast |

Checks: `make -C paper check` passed with its existing warnings; the lint's screening of the changed sections
found no excluded word; `git diff --check` passed; the PDF built at 35 pages with zero overfull boxes. Against the
build `fd4bf48b…7992`, pages 1–7, 19–25 and 31–35 changed. Pages 1, 3, 19–21, 23, 25 and 31, which hold the
changed text, were read at 1,600 pixels high; pages 2, 4–7, 22, 24 and 32–35, which only moved, were inspected
for layout at 1,100 pixels. Each is legible, with no collision, overflow or stranded line. Page 25 now ends about
four lines short, since the Conclusion's last two paragraphs stay together on page 26, as they did before.

The clean build from `17c54b1d1de431fe487b9909d8dff4a30cc76204` (`SOURCE_DATE_EPOCH=1792337154`,
`FORCE_SOURCE_DATE=1`) is 35 pages with SHA256 `7423314cfb7cb12f302e86005a782d93ea9c5419d33ee1235029b8731a797bcc`:
zero overfull boxes, every font embedded, 211 link annotations, and all 35 pages render identically to the build
read before the commit.
