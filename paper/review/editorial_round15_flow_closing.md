# Editorial round 15: flow in the closing sections

Reviewer: a fresh Claude subagent (Claude Opus 5.5), reading for this check alone.
Date: 2026-10-18.
Snapshot: commit 64d04e0, with a clean working tree. During the reading HEAD moved to a29a5d4: 2800b68
rewords 64d04e0's message over the same tree, and a29a5d4 changes `AGENTS.md` and one review record. The five
files in scope hash the same at 64d04e0 and at a29a5d4, rechecked after the findings were written.
Check: flow alone, in five kinds: (1) paratactic runs, (2) paragraphs that read as chained bullet points,
(3) unmarked turns, (4) missing or abrupt transitions between paragraphs and at section openings, and
(5) over-compression, semicolon chains included. Word choice, negation, verbs, numbers, facts, citations,
tables, captions and genuine catalogues lie outside it.

## Files in scope

| File | sha256 |
|---|---|
| `paper/sections/reach.tex` | `b11ae5c3199f06e994b5265ee778034b427b2b43ad9b241638babbda1a81040d` |
| `paper/sections/next.tex` | `32054594479807c5764742cc1c82a26179960330bd750eb82e72eb340c4dec20` |
| `paper/sections/conclusions.tex` | `d82694c6efa13ad21753d7fd4b4b0a7a4f7b95cb8bb8264c9000a93e34485bee` |
| `paper/sections/availability.tex` | `efd5ef2247120603c1f5b40af15adc25192b57c8795bd57f01813614548666ed` |
| `paper/sections/appendix.tex` | `17abe050d20a86031b7f3b1e426afcca0050cb9928bdb6500d84850d73013bbc` |

In `appendix.tex` the prose paragraphs alone were judged (lines 3–14); the three tables were read for
context. Table bodies elsewhere were skipped.

## What I read

- `AGENTS.md` in full as at 64d04e0, with "Sentences carry their dependencies" and "Inheritance and order"
  read closely, and a29a5d4's later change to it.
- Terluna's style sources: `STYLE_NOTES.md` and `Jewish_Papers_Updated_Style_Notes.md` in full;
  `Agent_Working_State_Editorial_Gates.md` in part (its scope and gates G1–G3, lines 8–46, with a keyword
  search of the rest). The charter itself went unread.
- `paper/main.tex`, for the order of sections: Results, Reach, Next steps, Conclusion, Appendix, Availability.
- The five files in scope, in full.
- Neighbours, for the transitions and the terms: `results.tex`, `introduction.tex`, `abstract.tex`,
  `worlds.tex` and `repairs.tex` in full; the opening and closing paragraphs of `assumptions.tex` and
  `verification.tex`.
- For the form of this record: `paper/review/README.md` and the first 60 lines of
  `editorial_round14_whole_prose.md`. That record concerns terminology and framing; the findings below come
  from my own reading.
- `paper/tools/lint.py`, to see what it screens. It matches words and has no test of flow, so it was left
  unrun.
- Two of the session's memory notes: Terluna's locations, and the author's writing rules, which quote the
  same direction.

A short script in the session scratchpad listed each paragraph's sentences with the lines they start on, as
an aid to reading; it judges nothing. The reading was silent; no passage was read aloud. No build ran, and no
file other than this record changed.

## The author's direction for this check (18 October 2026)

> "Remember I hate paratactic style in the academic papers I craft and I generally hate when paragraphs in
> them are just a bullet point set of information chained together pretending to be paragraphs."

> "A stock signpost is a stock signpost. "Moreover" and similar used appropriately to move from one thought
> to the next and keep flow is fine."

The author also objected when a draft lost the author's transition words and became a list of sentences
strung together, pointed out that a second point independent of the first needs its own transition so that
it reads as an addition and never as a consequence, and asked that the writing flow and transition smoothly.
These two directions are given in my words, under the rule on quotation that a29a5d4 added to `AGENTS.md`.

## How the findings were judged

- Severity: MAJOR where a paragraph, or a run of three or more sentences, reads as a list; MINOR where one
  relation goes unmarked.
- A run-in bold heading counts as the transition into its paragraph. Within a paragraph, each move between
  thoughts needs its relation written: in the syntax, in a transition drawn from the subject, or in a
  transition word.
- Every sample rewrite keeps each claim, number, condition, citation and `\claim{}` marker of the passage,
  keeps the author's own transitions ("so", "since", "while", "such as", "besides"), and adds the relations
  in syntax or in plain transition words.
- The author has accepted the Conclusion; its findings are marked "for the author".

## Findings

### Reach to other worlds (`reach.tex`)

**F1 · reach.tex:3–4 · kinds 4 and 3 · MINOR**
"Table~\ref{tab:reach} gives, property by property, the range" … "that the repaired codes have simulated."
Repair: the section opens on a table pointer straight after the lunar seas of Results, and the semicolon
sets the Moon beside the built-for ranges with their contrast unwritten. Open on the author's recast
sentence, which bridges from the lunar results, and mark the turn to other worlds: "The breathable Moon is
the first world besides Earth that the repaired codes have simulated; for other worlds,
Table~\ref{tab:reach} gives, property by property, the range each repair was built for." The wording of the
author's sentence stays as recast.

**F2 · reach.tex:7–9 · kind 5 · MINOR**
"and sets the scenario's values; leakage and the slice forcing read" … "between two of WRF-ELEC's rules."
Repair: contrast between the steps the modeller takes and the parts that take the new world's own fields;
replace the semicolon with "while": "…and sets the scenario's values, while leakage and the slice forcing
read that world's conductivity column and GCM fields, and the condition for ground strikes stays a bound…".

**F3 · reach.tex:12–20 · kinds 2 and 3 · MAJOR**
"The three ExoPlaSim defects that the general repairs remove" … "without fixing the orbit.\claim{W06}"
Failure: a lead sentence, then three parallel sentences, one per defect, each opening on the defect's name
("The Sun clock…" at 13, "The convective-cover unit…" at 15, "The orbit default…" at 19) in the same frame,
"in (or to) any run that…". The contrast between the Sun clock, confined to non-synchronous runs, and the
convective-cover unit, which biases synchronous runs too, is left to the reader, and the orbit default, an
independent third defect, follows the cover's arithmetic as if it came out of it.
Repair: write the contrast between the first two defects into the second sentence, and mark the third as
the last of the three announced.

```latex
\textbf{The defects in other configurations.} The three ExoPlaSim defects that the general repairs remove remain in
the released code, and by the code's arithmetic they bias any run that meets their conditions. The Sun clock skips
back in any non-synchronous run on the default solar geometry whose rotation differs from one day, by about
33\textdegree\ a model day for every rotation slower than 20 days. The convective-cover unit biases synchronous
runs as well, since ExoPlaSim's synchronous mode, even as it fixes the Sun in the sky, keeps the model day its
rotation period sets, and so it adds $0.125\ln(\text{day}/1\,\text{d})$ to the cover in any run whose model day
differs from one Earth day: about $+0.23$ for TRAPPIST-1e's rotation of 6.1 days \autocite{yang2023cloud} and
$+0.31$ for Proxima Centauri~b's 11.2 days \autocite{boutle2017exploring}. The third defect, the orbit default,
gives Earth's seasons to any run that sets an obliquity or an eccentricity without fixing the orbit.\claim{W06}
```

**F4 · reach.tex:22–41 · kinds 2, 1, 3 and 5 · MAJOR**
"The Earth values that depend on a ratio of Figure~\ref{fig:regimes}" … "Earth alone lies near the fits in
the adapted models."
Failure: nine sentences move among PlaSim's radiation, PlaSim's cloud, released CM1 and SWAN, adapted CM1,
the wave models and ExoPlaSim, mostly by "and" or by a semicolon. Three sentences join unrelated facts with
"and": Slingo's cover and the cloud water (26–29), CM1 and SWAN (29–31), and CM1's Sun and soil with RRTMG's
tables (33–34). The turn from released to adapted CM1 (31) goes unmarked, as do the concessions behind the
semicolons at 32 ("its drop limits and breakup remain Earth's") and 37 ("SWAN's ST6 drag … keep Earth's
constants"). At 38 the paragraph returns to ExoPlaSim with no transition, and the landing at 40 follows from
everything before it with nothing to say so. This is the paragraph in my part that reads most like a list.
Repair: take the transitions from the ratios that the first sentence names (along the column, along gravity,
along the day), mark the move from the released codes to the adapted ones, and write the two concessions.
A break before "Once adapted" would also give the released codes and the adapted ones a paragraph each.

```latex
\textbf{How the Earth values err.} The Earth values that depend on a ratio of Figure~\ref{fig:regimes} err as a
world departs from Earth along it. PlaSim's horizon factor of 35 is right only at Earth's scale height over radius:
an isothermal Chapman factor gives 22 for present Mars, 24.5 for Venus, 14 for Titan and 7.2 for the Moon, so the
slant path errs for each and most for the tallest air. Along the column, PlaSim's broadband fits, made near Earth's
column, would be applied to columns ten times Earth's on Titan, a hundred times on Venus and seven times on the
Moon, and along gravity its cloud water, written in metres, errs at any gravity other than Earth's, too dry aloft
under weaker gravity and too wet under stronger; beside these ratios, Slingo's cover, even with its unit repaired,
remains a fit made on Earth's convection.\claim{W02} The other released codes contain Earth values of their own:
CM1 computes with Earth's gravity of 9.81~m\,s$^{-2}$, Earth's 24-hour day and the calendar year's carbon dioxide,
trace gases and ozone, and SWAN, in the configuration used, loses gravity similarity through its wind-input knee,
fixed at 1~Hz. Once adapted, CM1 reads gravity as a parameter on its Morrison and NSSL paths and has run storms at
the Moon's gravity and at Earth's; its drop limits and breakup, however, remain Earth's, and their effect at other
gravities is unmeasured, since the similarity pair failed to convect. Along the day, its Sun and soil are built for
days from a few Earth days to the Moon's, while along the column RRTMG's tables end at 1.05~bar. At sea, with
SWAN's knee patched, the two wave models, in the configuration used, are built to run water seas at any gravity as
the scaled image of an Earth sea, and on the code paths the similarity tests ran they have been tested at a sixth
of Earth's gravity, with Earth's empirical laws, whereas SWAN's ST6 drag, exact quadruplets and bottom friction,
and SWASH's rotation, all outside that configuration, keep Earth's constants. ExoPlaSim, for its part, holds near
the columns its radiation and cloud were fitted on: Earth-air columns near Earth's warmth with the released
radiation, and the test world's design columns with the calibrations. Of the natural worlds in
Figure~\ref{fig:regimes}, then, Earth alone lies near the fits in the adapted models.
```

**F5 · reach.tex:44–47 · kind 5 · MINOR**
"the split of sunlight, in the version fitted before the gas bands," … "the longwave correction's accuracy
near 307~K is unchecked."
Repair: contrast between the earlier fit, tested on a warm column, and the current refit and correction,
which lack that test; replace the semicolon with "whereas": "…fell 0.7 points short on a 303~K column with
338~kg\,m$^{-2}$ of vapour, whereas the refit with the gas bands is known through its fit residuals and the
longwave correction's accuracy near 307~K is unchecked."

**F6 · reach.tex:52 · kind 3 · MINOR**
"rotation; their warmer runs, at up to 2.9 times Earth's insolation, lie beyond the radiation's fits."
Repair: contrast with the cooler runs named at 48; replace the semicolon with "whereas their warmer runs…".

**F7 · reach.tex:53–56 · kind 3 · MINOR**
"At rotations slower than 20 days, ExoPlaSim's model day departs" … "avoid the drift.\claim{W03}"
Repair: an independent point about slow rotators, set straight after the warmer runs as if it followed from
them; mark it as an addition with "moreover" ("At rotations slower than 20 days, moreover, ExoPlaSim's model
day departs…"), and mark the closing remedy as a concession: "…drifts against the Sun, though analyses that
sort output by the Sun's position avoid the drift."

**F8 · reach.tex:58–70 · kind 2 · MAJOR**
"Synchronous planets of M dwarfs, such as TRAPPIST-1e and" … "for the host's glow.\claim{W04}"
Failure: five sentences, five worlds, each opening on a new subject ("Synchronous planets…", "The
breathable Moon…", "A constructed world…", "Nitrogen--oxygen air…", "A breathable moon…"), so the paragraph
reads as five bullets. Inside them, "and" joins a cause to its consequence (59: the spectrum lies outside the
fit, so the shortwave needs refitting), and a semicolon sets the ozone case beside the shielded Moon (61)
with their contrast unwritten. Only "the same steps" (67) and "besides its column" (69) link one world to
another.
Repair: introduce each world by how it differs from the one before (a new star, the Moon's own pressure and
shield, a smaller body, a larger one, a host planet), and write the consequence and the contrasts.

```latex
\textbf{Worlds that need refitted calibrations.} Synchronous planets of M dwarfs, such as TRAPPIST-1e and
Proxima Centauri~b, add a spectrum outside the near-infrared water fit, so their shortwave needs refitting against
the reference with the star's spectrum. Even the breathable Moon needs its calibrations refitted and its cloud
settings checked at 1.0~atm, a case yet to be run, or behind another shield that blocks the ultraviolet, while under
a shield that passes the ultraviolet its air would form ozone, which every patched CM1 build sets to zero. Beyond
the Moon, a constructed world with breathable air on a small body, such as Mars held at 1~bar, has a scale height
over radius five times Earth's, 2.6 times Earth's air over each square metre and 0.38 of Earth's gravity, and so
needs the general repairs, a curved-air table of its own column and calibrations refitted to it. For CM1's
radiation, its 1~bar level stays inside RRTMG's pressure range, while the pressure on ground below that level lies
past RRTMG's tables, as it does over the lunar seas. On a larger planet, nitrogen--oxygen air needs the same steps,
a slant factor from its own column among them, though there the released cloud water errs toward too much water,
the reverse of the test world's error, and the same general repair corrects it. Around a giant planet, a breathable
moon needs, besides its column, the downward infrared that PlaSim now takes at its top for the host's
glow.\claim{W04}
```

**F9 · reach.tex:72–75 · kind 5 · MINOR**
"Titan's nitrogen--methane air at 94~K, present Mars's thin carbon dioxide" … "would have to be
built.\claim{W05}"
Repair: the semicolon leaves a concession unwritten (these worlds lie outside the schemes, yet the general
repairs apply to them); mark it: "…represent, so that, although the general repairs of units, clocks and
gravity would apply to them unchanged, their radiation, condensation and clouds would have to be built."

### Next steps (`next.tex`)

**F10 · next.tex:11–13 · kind 5 · MINOR**
"The longwave correction, switched on with the ice optics, warmed" … "near 307~K with twice the water vapour."
Repair: the semicolon hides the concession that sets up the refit in the next sentence; mark it with "yet":
"…a joint effect in which the ice optics' share is unmeasured, yet the correction was fitted at 295~K and is
used near 307~K with twice the water vapour."

**F11 · next.tex:16–21 · kinds 3 and 5 · MINOR**
"A correction with humidity among its predictors would extend the fit;" … "on another world as on the test
world."
Repair: two options of rising scope, a step beyond the refit, are set side by side across a semicolon; mark
the step and the gradation: "Beyond the refit, a correction with humidity among its predictors would extend the
fit, and a reduced correlated-$k$ scheme built from the reference model's own spectroscopy would go further
and replace both the correction and Sasamori's and Lacis and Hansen's fits…".

**F12 · next.tex:23–27 · kind 3 · MINOR**
"PlaSim's cloud amount and cloud water move the test world" … "and its cloud-water profile are fitted."
Repair: the first sentence names uncalibrated cloud, and the second opens on the longwave test before it
reaches the cloud target; lead with the target and attach the longwave test as a second use of the same
runs: "The cloud cover and water by pressure of CM1 runs forced from the consistent state of the first step,
with the transport across each ring imposed, become the target to which PlaSim's humidity thresholds and its
cloud-water profile are fitted, and the same runs test whether the corrected longwave closes the 3.7~K…".

**F13 · next.tex:59–62 · kind 5 · MINOR**
"The consistent deep-atmosphere equations" … "whether the full equations are needed."
Repair: the semicolon leaves the staged approach unwritten (a first step short of the full equations);
mark it with "before adopting them": "…include both effects, and before adopting them a first step corrects
the GCM's column mass and heights, while a test of the circulation's sensitivity shows whether the full
equations are needed."

**F14 · next.tex:72–74 · kind 3 · MINOR**
"Giving RRTMG the shield's spectrum, in a run of its own," … "that the Sun's unfiltered spectrum brings."
Repair: a separate remedy, for the unfiltered spectrum named at 66–67, follows the two-branch test of the
tables as if it were one of its outcomes; mark it as separate: "Separately, giving RRTMG the shield's
spectrum, in a run of its own, would correct…".

**F15 · next.tex:76–78 · kind 5 · MINOR**
"Morrison's limits on the size of rain, its breakup and the size of ice" … "in the rings 57--73\%."
Repair: a semicolon chain of three loosely related clauses, two retained approximations and a measured
evaporation, which reads as a three-item list; join the approximations and attach the evaporation to them as
the condition it was measured under: "Morrison's limits on the size of rain, its breakup and the size of ice
crystals stay Earth's, and snow falls with the drops' gravity exponent where its own mass and area laws give
a larger one; with these limits, 85\% of the falling water evaporates in the boxes and 57--73\% in the
rings." This is the most list-like sentence in Next steps.

**F16 · next.tex:95–98 · kind 3 · MINOR**
"In the windows the sign of the ground strikes under Takahashi's law" … "left over from a run with leakage
off."
Repair: a second open question, the strikes' sign, follows the laboratory test as if it came out of it;
mark it as an addition with "also": "The sign of the ground strikes under Takahashi's law also stays open in
the windows: …".

**F17 · next.tex:98–100 · kind 3 · MINOR**
"A leader model of the descent from the $-7$\,\textdegree C level" … "each lowering a median 149~C."
Repair: the leader model concerns the number of strikes, and it follows the sentence on their sign as if it
answered it; mark the shift from sign to number: "For their number, a leader model of the descent … would
replace the bound on ground strikes…".

**F18 · next.tex:105–107 · kind 3 · MINOR**
"The air's density as a field and a wider frequency band" … "a physical one that ST6
includes.\claim{N04}"
Repair: needs beyond the source-term checks, added after the spread's consequence with no marker; open with
the relation: "Beyond the source terms, the air's density as a field and a wider frequency band for the
small seas that fail the band-edge test are numerical needs…".

### Conclusion (`conclusions.tex`), for the author

The Conclusion moves by written relations through most of its length ("For those calculations to describe the
same world", "instead", "Otherwise", "then", "Once", "Those limits also", "thus"). Three light places follow.

**F19 · conclusions.tex:9–12 · kind 1 · MINOR · for the author**
"Connecting that global calculation to CM1 and the wave models" … "where cloud, rain or surface conditions
change."
Repair: the third sentence describes the use that the connection makes possible, set beside it as a parallel
statement; mark the consequence with "then": "The GCM can then be used to explore a range of illumination or
rotation…".

**F20 · conclusions.tex:58–60 · kind 5 · MINOR · for the author**
"A massive atmosphere on a small body separates the consequences" … "while leaving gravity fixed."
Repair: the clause after the semicolon adds a second separation that the same world allows; write the
addition: "…from those of thin air, and varying its pressure then changes the column mass while leaving
gravity fixed."

**F21 · conclusions.tex:67–69 · kind 3 · MINOR · for the author**
"The choice of those cases can also sharpen the use of terrestrial experiments." … "can predict different
charge arrangements."
Repair: the second sentence gives the example of the first, yet it opens on a new subject, the graft, and
names the laboratory only in its last words; mark the example: "In the simulated storms, for instance, the
electrification graft computes charge separation in ice-particle collisions, where alternative laboratory
fits can predict different charge arrangements."

### Appendix (`appendix.tex`, prose)

**F22 · appendix.tex:11–12 · kind 5 · MINOR**
"beyond 1,250~nm a group must also keep, within the same 1\%," … "below 500~nm each band is one channel."
Repair: the last clause is an exception to the bisection, joined by "and" as if it were one more rule; mark
the contrast with "while": "…the beam's loss above the bottom of every layer, while below 500~nm each band is
one channel."

### Availability, authorship and review (`availability.tex`)

**F23 · availability.tex:10–13 · kind 3 · MINOR**
"The upstream sources are pinned by checksum:" … "the WRF public-domain notice for WRF-ELEC."
Repair: after the Terluna sentence the paragraph turns back to the patches on a new subject, and the licences
follow from the patches' relation to those sources, which stays unwritten; tie both to the patch series:
"The patches apply to upstream sources pinned by checksum: …, and as patches to them they inherit their
licences: …".

**F24 · availability.tex:33–36 · kinds 3 and 4 · MINOR**
"Each claim marker in the source names a register entry" … "refer to the same entries without markers."
Repair: the claims register enters at the end of the assistance narrative with no link to it; move the
sentence to "Code and data", after its first sentence (3–7), which names the claims register, or link
it to the drafting just described ("For text drafted this way, each claim marker…").

**F25 · availability.tex:49–51 · kind 5 · MINOR**
"The author, reading the second draft during that round, found it still centred" … "acts on the round's
findings."
Repair: consequence behind a semicolon; mark it with "so": "…found it still centred on the test world, so the
third draft, written by the same assistant, reframes the paper on the field and acts on the round's findings."

**F26 · availability.tex:57–59 · kind 3 · MINOR**
"Each round's findings and dispositions, with the referees' reports" … "identified by its hash."
Repair: a note on where the records are kept breaks into the chronology, and the next sentence's "the
resulting conclusion" refers back past it to the revision at 56; move the note to the end of the paragraph,
before the sentence on outside review, where it covers every round.

**F27 · availability.tex:59–68 · kinds 1 and 2 · MAJOR**
"The author read the resulting conclusion on 18 October 2026" … "Both findings were acted on."
Failure: seven sentences alternate the author's readings and the assistants' rewrites, each opening on a new
actor ("The author read…" at 59, "Claude Opus~5.5 rewrote it…" at 60, "The author read…" at 61, "The Codex
rewrite received…" at 62, "The author read…" at 64, "The replacement develops…" at 65). The causes that link
them, a rejection followed by a rewrite, are left to juxtaposition, and "The replacement" (65) arrives with
the rewrite that produced it unstated in this paragraph; the paper states it at 27–28.
Repair: write each rejection as the cause of the rewrite that follows, keeping the dates, rounds and
findings.

```latex
When the author read the resulting conclusion on 18 October 2026 and rejected it as a summary of the work,
Claude Opus~5.5 rewrote it, and two fresh reviewer agents read the rewrite in a ninth round before a tenth checked
the evidence of its revision. Reading the revision, the author judged it still a summary and so asked Codex to
write the conclusion afresh. The Codex rewrite received prose and evidence reviews in rounds 11 and 12; both
evidence reviews found no blocking issue, while the prose reviews prompted a structural revision followed by local
revisions to the opening, paragraph endings and final prospect. Because the author, reading that revision, judged
it still centred on the Moon, its replacement develops the broader model ensemble. In round 13, the prose review
found the conclusion ready for the author's reading and required alignment of the introduction, while the
evidence review required a local qualification of the cloud-calibration claim. Both findings were acted on.
```

**F28 · availability.tex:72 · kind 3 · MINOR**
"Every agent read for cadence silently."
Repair: a statement about every round, placed between round 14 and the check that followed it, where it
reads as a remark on round 14 alone; move it beside the records note of F26 at the paragraph's end, or mark
its scope: "In every round, the agents read for cadence silently."

## Summary

Counts: 28 findings, 4 MAJOR and 24 MINOR.

| File | MAJOR | MINOR |
|---|---|---|
| `reach.tex` | 3 (F3, F4, F8) | 6 |
| `next.tex` | 0 | 9 |
| `conclusions.tex`, for the author | 0 | 3 |
| `appendix.tex`, prose | 0 | 1 |
| `availability.tex` | 1 (F27) | 5 |

The paragraphs that read most like lists:

1. reach.tex:22–41, "How the Earth values err": nine sentences across five codes, joined by "and" and
   semicolons, with the turn from released to adapted codes unmarked (F4).
2. reach.tex:58–70, "Worlds that need refitted calibrations": five worlds, each opening a fresh sentence on a
   fresh subject (F8).
3. reach.tex:12–20, "The defects in other configurations": a lead sentence and three parallel sentences, one
   per defect (F3).
4. availability.tex:59–68, the review history from 18 October: seven sentences that alternate the author's
   readings and the rewrites, with each cause left to juxtaposition (F27).
5. availability.tex:3–13, "Code and data": four sentences on four subjects; a catalogue by its function, with
   the link from pinned sources to inherited licences unwritten (F23).

Two patterns account for most of the minor findings. Eleven (F1, F2, F5, F6, F9, F10, F11, F13, F15, F20,
F25) are semicolons between independent clauses whose contrast, concession, consequence or addition goes
unwritten, so a reviser can search the closing sections for that semicolon. Seven (F7, F14, F16, F17, F18,
F26, F28) set an independent point after a sentence as if it followed from it; "moreover", "also",
"separately" or a phrase drawn from the subject marks each one as an addition.

Of the section openings, Reach's alone lacks a bridge (F1). Next steps opens by turning Reach's limits into
the requirements for developing the ensemble; the Conclusion, the Appendix and Availability open on their own
subjects under their headings. Next steps' opening paragraph, its paragraphs on the reference, the test of
the reach and an independent GCM, and the Conclusion at conclusions.tex:15–55 and 75–100 move by written
relations throughout.
