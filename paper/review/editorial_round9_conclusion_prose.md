# Editorial review, round 9: Conclusion (prose and the author's direction)

## 1. Record

| Item | Entry |
|---|---|
| Reviewer | A fresh Claude subagent, Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), reading alone, with no earlier review of this section seen. Under `paper/review/` it opened `README.md` and the first 60 lines of `editorial_round8_conclusion_prose.md`, for the record's format; those lines hold round 8's first two findings on an earlier text. It wrote this file and changed nothing else. |
| Date | 2026-10-18 |
| Snapshot | Commit 0cb4f50 (`0cb4f50d8dd82afb60181644c79aad63054d92aa`), also the working tree's HEAD, with a clean tree. Paper files were read with `git show 0cb4f50:<path>`, through copies in `/tmp/claude-1000/r9prose_snap/`. |
| The rejected version | `git show 9e7c8b4:paper/sections/conclusions.tex` (sha256 `e5a5352b34883fd375e5d2d5f60f0675faa5e4e0a25462b6e39b487606f153a3`), read in full and compared with the snapshot item by item (table in finding 1). |
| The author's direction | As quoted in the brief (2026-10-17 and 2026-10-18), and as recorded in the session memory files `conclusion-as-discussion.md`, `writing-style-rules.md`, `paper-standalone-field-framing.md` and `editorial-review-by-reading.md`, read for the author's own words. The commit message of 0cb4f50 was seen with the commit. `paper/notes/` was left unopened. |
| Kind of reading | The section read whole twice: first as the author asked it to be read (would a scientist be excited and made to dream; is it a discussion or a summary), then as an editor, sentence by sentence and paragraph by paragraph under AGENTS.md "Writing" and the charter's ten passes, with the swap test at each paragraph boundary. A third reading checked the findings. All three readings were silent; the read-aloud pass that the charter requires for a conclusion remains pending. |
| Screening | A grep of the section for "not", "rather than", other negations, signposts, self-reference and universal words, and a script count of words and numbers (numerals plus number words) in three texts: 9e7c8b4, 6 paragraphs, about 1,570 words, about 76 numbers; 0cb4f50, 11 paragraphs, about 1,650 words, about 69 numbers; the rewrites of this record assembled, 10 paragraphs, about 1,615 words, about 58 numbers. Screening only. `paper/tools/lint.py` was left unrun. |
| Number check | Each number in the section checked against the body at 0cb4f50, and eleven records of `paper/claims.json` (G08, G09, G10, G12, G17, H04, H24, R04, S04, V04, W06) read where the section states more than the body. Cited sources were left unopened. The capillary-length agreement at l.53–56 appears in the conclusion alone. |

**File in scope** (sha256 at 0cb4f50)

| File | sha256 | Scope |
|---|---|---|
| `paper/sections/conclusions.tex` | `6dfec6728019a3e007c602159098dbf43b27a487d015cb03818fa385d1480049` | whole section, l.1–102 |

**Context read in full** (sha256 at 0cb4f50): `abstract.tex` `1d22734b8e9c39bc9b52f4eeff8c8436ee598b84e6bf5c14025f2b3fd17416b0`; `introduction.tex` `a88f442f589e007dbb57f081334fc53ef066dbc26734d9f6610e12194bbea3d2`; `worlds.tex` `453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112`; `assumptions.tex` `77bc704fe58d964ff2567a39ffbdf6e2af9b0cc422bfb88e04d25e949b877107`; `repairs.tex` `c846dbbf4dbaf39ae194d7bb93a26204aaa1b12f4b24e7aa1accdd948b281102`; `verification.tex` `4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00`; `results.tex` `112e8074232fd04300fccf280bb7bf5341e0b3d34a31a5c9a4561e46fcc4ca35`; `reach.tex` `fff8183910168eeb9ee837c8e5766ac0bea7f64b6e95e0d63b8cf821e26f5b63`; `next.tex` `789a34bd471f58e00c23ae3f422796c7c3333308337f80e49898017f862753ad`; the section order in `paper/main.tex` `b910d0edf1ca7b9b583208415d15588e64263c32769750937cd28d97675d57e4`; `paper/claims.json` `e462d3ff93eea66bb201aa51d42977bccff8b95f9099efc9559a01b487569745` (the eleven records above only). The appendix was left unread.

**Rule files read in full** (sha256)

| File | sha256 |
|---|---|
| `AGENTS.md` (identical at 0cb4f50 and in the working tree) | `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32` |
| Terluna `ensemble/planning/Open_Moon_Editorial_Charter_control-01.md` | `aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0` |
| Terluna `ensemble/planning/source_controls/STYLE_NOTES.md` | `659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46` |
| Terluna `ensemble/planning/source_controls/Jewish_Papers_Updated_Style_Notes.md` | `18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab` |
| Terluna `ensemble/planning/source_controls/Agent_Working_State_Editorial_Gates.md` | `553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464` |

The Terluna files were read from its working tree at HEAD f03b839. Order of reading: AGENTS.md, the section, the abstract, the introduction, the rejected version, results, reach, next steps, repairs, verification, worlds, assumptions, the memory files, the four Terluna files, then the section again against the findings.

## 2. Answers

### Question 1. Would a reader get excited? Would it make them dream?

In places. Four passages would catch a scientist who wants to be excited, and they are the section's best material:

- l.21–29, the one paragraph that lets the reader see the world: raindrops falling three times slower and mostly evaporating on the way down; storms stretched upward until their tops stand at 55–80 km, with Earth's arrangement of charge at five to six times its height; waves four to five times higher under the same wind; and air so tall that half of it is still in sunlight a full Earth day after sunset.
- l.52–53: a laboratory measurement on Earth "would decide which way up the model's storms hold their charge".
- l.79 and l.82–84: "For a constructed world the model is part of the design", and "the Earth values left in them are the design's own uncertainty: in the air where people and plants would live".
- l.101: "the storms, rain, seas and skies of a world still being designed before anyone lives under them".

Everywhere else the section falls back into the register the author rejected. Nearly every paragraph opens on an idea and then restates a body section with its numbers (the map is in finding 1): the chain's wiring (l.5–8); the ranking of 20 K, 6 K and 1.6–2.5 K, for the fifth time in the paper (l.13–16); the verification section (l.33–36); the abstract's sentence on the line-by-line scheme and the results' cloud-cover numbers (l.40–46); the classes of repair (l.58–64); the defects (l.67–77); the introduction's framing (l.87–91); and a replay of the section's own path (l.93–99).

Against 9e7c8b4 the section has escaped in part. The gains are real: one line of argument that moves outward from the code to the laboratory and then to other worlds, an idea at the head of each paragraph, the images of l.21–29, the design paragraph, and an ending that looks forward. The content and weight are those of the rejected version: about the same length, about 69 numbers against 76, fourteen of the rejected version's fifteen content items in a new order, and in l.67–77 the rejected opening paragraphs themselves. A reader applying the author's test meets a summary in the first paragraph and again in the first sentence of the ending. My judgement, made as the author asked: a better-organised summary with a discussion inside it.

### Question 2. Is it rooted in the code work and the technology?

Yes, closely, and in three paragraphs too closely. The chain (l.3–8), the switches (l.8–10), the fits and their calibration to the in-house line-by-line model (l.12–17, 40–43), the fall-speed scaling and CM1's gravity (l.21–25), SWAN's knee (l.26), the curved-air terms (l.28–29, 59–63), the identity, rebuild and similarity checks (l.33–36), the graft's charging laws (l.49–53), the drop limits (l.53), the repair classes (l.58–64), the defects (l.67–76) and the shield's dimming (l.79–82) all appear. In l.33–36, l.58–64 and l.67–77 the code work serves as a store of results to restate, where a discussion would draw a consequence from it. One paragraph drifts from the code: l.87–91 return to the introduction's framing. Three parts of the technology appear stripped of their meaning:

- The chain appears as wiring alone (l.5–8). Its use is the means to calibrate a GCM's cloud against runs that resolve it, through a forcing built for a slice of any world's GCM (repairs l.187–188), and that use goes unwritten at l.43.
- The reference model enters as "a line-by-line model built in house".
- The graft appears through its charging laws alone.

### Question 3. Does it flow as one argument?

In outline, yes. The joints between paragraphs are written at five boundaries and missing at three.

| ¶ | Lines | What it develops | What it takes from the paragraph before | Swap test |
|---|---|---|---|---|
| 1 | 3–10 | The premise: four Earth codes, coupled and taken to a world that departs on four ratios, with switches to measure Earth's share | Opening | Fixed; its middle sentence, l.5–8, can go with no loss to the argument |
| 2 | 12–17 | Where Earth's share was largest: the fits | "Measured that way", from ¶1's switches | Fixed |
| 3 | 19–30 | The repairs with the smallest share put the world's own features into the codes | "Small as their share", from ¶2's units and constants | Tied to ¶2; ¶3 and ¶4 trade places with one pronoun changed |
| 4 | 32–38 | Checking a designed world's models with no observation of it | Nothing; a new premise, with no link to ¶3's features | Fits equally after ¶2; its landing returns to ¶2's ranking |
| 5 | 40–46 | Evidence for the fits from outside the code | The "open" fits, from ¶4; its first sentence repeats ¶2's last | Fixed after ¶4 |
| 6 | 48–56 | The resolved runs' own Earth laws, and the laboratories that would decide them | "The resolved runs", from ¶5 | Fixed; its two cases trade places inside it |
| 7 | 58–65 | What carries to another world, by how each part was made | Nothing from ¶6; a turn | Fits equally after ¶2 or ¶3; its last sentence hands on to ¶8 |
| 8 | 67–77 | The defects and exoplanets | "off that world", from ¶7's last sentence | Fixed after ¶7 |
| 9 | 79–85 | The model as part of a constructed world's design | A deliberate turn from natural planets to constructed worlds | Trades places with ¶10 with no loss |
| 10 | 87–91 | Designs combine Earth's air with any gravity, size and day | "Designs can also", from ¶9's "design" | Trades with ¶9; restates the introduction |
| 11 | 93–102 | The path and the prospect | A turn back to the field | Fixed as the ending; its first two sentences replay ¶2–¶7 and ¶3 |

¶1–¶6 move outward from the code: switch, fits, arithmetic, checks of the code, spectroscopy and resolved runs, laboratories. These are the same steps of distance from the code that the verification section uses, and that line is the section's best structural idea. ¶7–¶10 turn to other worlds in an order that is fixed from ¶7 to ¶8 and arbitrary at ¶9 and ¶10. The missing joints are ¶3→¶4, ¶6→¶7 and ¶9↔¶10, and the ending replays the outline where it should gather it.

### Question 4. Does the ending tie the section together and inspire?

Partly. Its last clause, "each with every Earth value left in its model named and measured" (l.102), returns to ¶1's measurement of Earth's share and closes the section's frame. "a world still being designed before anyone lives under them" (l.101) gives the ending its one image of people. The rest falls back into summary:

- l.93–96 replay the section's own path in its own order (arithmetic, column, calibration, resolved runs, laboratories), the recital the charter excludes.
- l.96–99 repeat ¶3's storms, rain and seas under "Already".
- The one forward sentence lands on bookkeeping.

The ending would be stronger as a gathering in one sentence, followed by a prospect accumulated in physical questions that a modeller or a designer could then answer, closing on the people who would live under the sky. Finding 3 gives a rewrite of that shape.

### Question 5. Reach to untested worlds, and breaches of the rules

**Reach.**

- l.59 "A general repair holds as it is" and l.59–60 "The curved-air method holds once its table is recomputed" state as fact that the repairs hold on worlds where they have yet to run. The introduction says "is built to hold" (l.78). Finding 11.
- l.73–74 give a property of the orbit default on the test world as a property of every configuration. Finding 12.
- l.26–30 credit the knee repair with waves that the released code computes within about 5%. Finding 7.
- l.102 "every Earth value" promises a completeness that the inventory, made on the lunar paths, supplies for those paths alone. Finding 3.
- l.4 and l.87–88 call the design's air "Earth's air". Findings 4 and 13.

The ending's "would let modellers compute the weather of an Earth-like exoplanet" (l.100) is conditional on the path being completed, and stays within the rules.

**Rules.**

- **Excluded words.** "not" and "rather than" are absent. The negations at l.33 ("no observation"), l.37 ("nothing") and l.87 ("no known natural world") state propositions that need them.
- **Empty actions.** l.50, the charging laws "held the lunar storms' charge"; l.93–94, "that origin was followed value by value and taken apart"; l.67, the defects "bear most directly on exoplanets"; l.29, features that "lay beyond the models". Milder: l.28, "Geometry ... sets the twilight"; l.40, "the code that holds it".
- **Aphorisms and quotable lines.** l.32, "exists only as a design has weather only in its models"; l.76–77, the antithesis "A modeller who checks global means passes such errors, and one who maps ... finds them"; l.16–17, the maxim "A fit holds near the data it was fitted to".
- **Explaining the obvious and generic lessons.** l.16–17, l.37, l.40.
- **Catalogues in prose.** l.5–8 (three couplings joined by semicolons); l.21–29 (four features, the last introduced by "Geometry, last"); l.59–64 (one class per sentence, with the subject–verb resets "A general repair holds", "The curved-air method holds", "A calibration has to be"); l.49–56 (two cases).
- **Self-reference.** l.33, "made here"; l.93, "here".
- **Promotional cue.** l.96, "Already".

## 3. Findings

Line numbers are those of `paper/sections/conclusions.tex` at 0cb4f50 unless another file is named. Rewrites are LaTeX, ready to paste, each checked against the body passages named under it, and each screened for the excluded words. Together the rewrites of findings 2–13 give a ten-paragraph section, in the order ¶1, ¶2, ¶3, ¶4, ¶5, ¶6, ¶7, ¶8, then ¶10 merged into ¶9, then ¶11.

### Finding 1. BLOCKING. The whole section, l.3–102

- **Text.** Each paragraph's first sentence states an idea; the sentences after it restate a body section with its numbers.
- **Rule.** The author's direction of 2026-10-18 ("you still wrote a bloody summary", "it's just a data dump about what we did"); AGENTS.md "Conclusions and the arc" (replaying the section order and reciting the inventory are excluded); charter §11 and gate G1.
- **Why.** The first table shows where each paragraph's material already stands in the paper. Ten of the eleven paragraphs restate it, eight with the same numbers. The second table shows that fourteen of the rejected version's fifteen content items reappear, in a new order. The section is as long as 9e7c8b4 and carries nearly as many numbers, so the reader receives the paper a second time, under better topic sentences. The ideas in those topic sentences are the discussion the author asked for; each is followed by data the reader has just met in the body.

Where each paragraph's material already stands:

| ¶ (lines) | Opening idea | What follows the idea | Where the paper already says it |
|---|---|---|---|
| 1 (3–10) | Switches measure Earth's share | The chain's wiring | intro l.55–68; repairs l.3–5 |
| 2 (12–17) | Fits read as physics | 20 K, 6 K, 1.6–2.5 K; a maxim | abstract l.20–23; intro l.82–83; results l.87–91; reach l.3–8 |
| 3 (19–30) | Repairs small in the mean put the world's features into the codes | 85 and 64%; 55–80 km; the charge; a hundredth; the waves; the twilight | results l.122–125, 141–149, 172–179; worlds l.78–80 |
| 4 (32–38) | A designed world is checked with no observation of it | Identity, rebuild, similarity | verification l.17–28, 39–44 |
| 5 (40–46) | Evidence for a fit comes from outside the code | The line-by-line scheme; 82–97 against 27 and 41% | abstract l.23–26; next l.15–19; results l.91–96 |
| 6 (48–56) | Resolved runs have laboratory laws | The charging windows; impact speeds; 2.46; 20% | results l.159–167; next l.73–91; assumptions l.87–90 |
| 7 (58–65) | What carries follows from how a part was made | The classes; Titan | intro l.75–81; reach l.8–14, 76–79; repairs l.105–109 |
| 8 (67–77) | The defects concern exoplanets | The run configuration; 33° and 0.23; 0.9 K and 9 to 36% | reach l.16–24; next l.38–45 |
| 9 (79–85) | The model is part of the design | 5.0 to 3.0%; 3.7 K | results l.58–60, 101–120 |
| 10 (87–91) | Designs combine Earth's air with any gravity | The design's column; every ratio at once | intro l.15–26, 46–51 |
| 11 (93–102) | (the ending) | The path; the features; the prospect | ¶2–¶7 and ¶3 of the section |

The rejected version's content, by this reviewer's division, and where it reappears:

| 9e7c8b4 | Content | At 0cb4f50 |
|---|---|---|
| l.3–6 | The repair's class follows the value's form | ¶7 l.58–64; ¶11 l.93–96 |
| l.6–11 | Three defects; +0.23 for TRAPPIST-1e; 33° for slow rotators | ¶8 l.71–73 |
| l.13–20 | Global mean kept; two-year test, 9 to 36%, 0.9 K; "A modeller finds such an error in maps of sunlight by longitude and of rain by season" | ¶8 l.73–77 |
| l.22–27 | The fits moved the mean most: 20 K, 6 K, against 1.6–2.5 K | ¶2 l.12–16 |
| l.28–32 | The curved-air table from the column; Titan at 80 km and 65° | ¶7 l.59–63 |
| l.33–34 | The dynamical cores' thin shell and flat slab | (dropped) |
| l.34–41 | A scheme from line-by-line spectroscopy; the comparison planned | ¶5 l.40–43 |
| l.41–46 | Cloud against resolved runs; 82–97 against 27 and 41% | ¶5 l.43–46 |
| l.48–53 | The charging laws; opposite arrangements; a laboratory at impact speeds | ¶6 l.49–53 |
| l.53–63 | Cloud tops 55–80 km; a hundredth of Earth's flash density | ¶3 l.23–25 |
| l.65–71 | SWAN at 0.3 against 5.4%; CM1's pair failed to convect | ¶4 l.35–36 |
| l.71–79 | 85 against 64%; the capillary length, 2.46; within about 20% | ¶3 l.21–23; ¶6 l.53–56 |
| l.81–85 | The dimming eased from 5.0 to 3.0%; refits could change it | ¶9 l.79–82 |
| l.86–90 | Biases known from arithmetic; the ROCKE-3D runs at 16 and 64 days | ¶8 l.67–71 |
| l.90–94 | The fits replaced from evidence beyond the GCM, down to the drop and ice laws | ¶5–¶6; ¶11 l.93–96 |

- **Rewrite.** Keep each opening idea and develop it by consequence: what it means for a modeller of a world beyond Earth's range, or for a designer, and what it opens. Keep a number where it makes the point, for example the 20 K against 2.5 K of ¶2, the 85 against 64% of ¶3 and the fourfold dry land of ¶8. Leave the rest to the body, which the reader has just read. Findings 2–13 give paragraph rewrites in that direction. Assembled, they keep the section's length (about 1,600 words, which the author's call for more paragraphs allows) and cut its numbers from about 69 to about 58. Most of their change is in register: each paragraph's idea governs and its data serves as evidence, the missing joints are written, and the reminder shrinks to ¶1. The drafter can cut further. ¶7 could shrink to its first sentence and its scope sentence, and the identity clause of ¶4 could go.

### Finding 2. BLOCKING. ¶8, l.67–77

- **Text.** "The first runs off that world would measure the defects, which bear most directly on exoplanets. Released and repaired ExoPlaSim, run in the configuration of two of the ROCKE-3D runs of \textcite{way2018climates}, ozone-free planets of nitrogen-dominated air at Earth's insolation and zero obliquity and eccentricity rotating once in 16 and 64 days, would measure ... By the code's own arithmetic, ... about 33\textdegree\ ... 20 days, ... about 0.23 ... TRAPPIST-1e. The Sun clock and the orbit default keep the global mean ... 0.9~K ... from 9 to 36\%. A modeller who checks global means passes such errors, and one who maps sunlight by longitude and rain by season finds them."
- **Rule.** The author's direction (write the conclusion fresh; the brief asks whether the new section escaped the rejected one); AGENTS.md "Conclusions and the arc"; "No witticisms" (quotable closing lines).
- **Why.** This paragraph is the rejected version's first two paragraphs (9e7c8b4 l.6–20) and its run configuration (9e7c8b4 l.88–90), with the same numbers in nearly the same order. Its landing is the rejected landing (9e7c8b4 l.20) turned into an antithesis. The configuration in l.68–70 is copied from Next steps (next l.38–42). The point the field most needs from the defects goes unstated: the test world's month-long day and small tilt made these defects large, and by the code's own arithmetic the same defects bias runs of natural planets that many studies make. Errors in a code used for natural planets were found on a constructed world. With that point stated, the numbers become its evidence; left unstated, they read as the rejected list.
- **Rewrite.** Findings 12, 18 and 19 are repaired in it.

```latex
The three ExoPlaSim defects that grow as a world departs from Earth's values were found on the test world, whose
month-long day and small tilt made them large, and by the code's own arithmetic they bias the runs of natural
planets that meet their conditions as well: the Sun clock sets the Sun back about 33\textdegree\ each model day,
as it did on the test world, in any non-synchronous run on the default solar geometry of a planet turning more
slowly than once in 20 days, and the convective-cover unit adds about 0.23 to the convective cover of a
synchronous run of TRAPPIST-1e. On the test world the Sun clock and the orbit default kept the global mean of the
arriving sunlight and moved it between places, and correcting them warmed the global mean by 0.9~K over two
years while the share of land under half a millimetre of rain a day rose fourfold, a change a modeller finds in
maps of sunlight by longitude and of rain by season. Released and repaired ExoPlaSim, run on two of the slowly
rotating planets of \textcite{way2018climates}, would be the first runs of the repairs off the test world and
would measure the three defects' joint effect on worlds that other studies have modelled.
```

- **Check.** assumptions l.100–109 and l.120 (the three defects grow with departure; the Moon's slow rotation and small tilt made all three large; 32.5° on the Moon); reach l.16–24 (33° for rotations slower than 20 days; +0.23 for TRAPPIST-1e); results l.47–52 and claim G17 (0.9 K over two years; 9 to 36%); next l.38–45. The configuration's details stay in Next steps.

### Finding 3. BLOCKING. ¶11, the ending, l.93–102

- **Text.** "Many models used for other worlds began as models of Earth, and in the four codes here that origin was followed value by value and taken apart in steps: constants and clocks by arithmetic, ... measured in Earth's laboratories. Already, for a world that exists only as a design, the repaired codes compute storms ..., rain ..., and seas ..., each a conditional result that the remaining fits can still move. Followed to its end, that path would let modellers compute the weather of an Earth-like exoplanet from its own gravity, day and starlight, and the storms, rain, seas and skies of a world still being designed before anyone lives under them, each with every Earth value left in its model named and measured."
- **Rule.** The author's direction of 2026-10-18 (the end ties the section together and is "pure inspiration"); AGENTS.md "Conclusions and the arc" (a conclusion gathers its lines into a new relation; replaying the section order is excluded); "Exact action"; "Claims stay within their evidence" (each "every" checked).
- **Why.** Each sentence has its own fault:
  - The first sentence replays the section's own path in its own order, a recital where the ending should gather. Its subject, "that origin was followed ... and taken apart", is an empty action on an abstraction, and "here" is self-reference.
  - The second sentence repeats ¶3's storms, rain and seas, under "Already", a cue of achievement.
  - Only the third sentence looks forward, and it lands on bookkeeping. Its "every Earth value left in its model named and measured" promises a completeness that the inventory supplies on the paths the lunar runs took (assumptions l.3–4).

  The inspiration the author asked for appears in one phrase, "before anyone lives under them".
- **Rewrite.** Gather in one sentence (the switches, the fits, the evidence from outside the code down to the laboratory), then accumulate a conditional prospect in physical questions that close on people:

```latex
Many models used for other worlds began as models of Earth, and in four of them, measured one switch at a time
on the test world, Earth's share of the climate came mostly from fits whose replacements can be built from
evidence outside the code: line-by-line spectroscopy for the radiation's gases, runs that resolve the cloud for
its cover and water, and, inside those runs, laboratory measurements of the charge rimed ice takes at the
storms' impact speeds and of the largest stable drops of other liquids. Built and checked, those replacements
would let a modeller set the gravity, day, column and starlight of a world whose air and water resemble Earth's
and follow its weather down the chain from its climate to its shore, with Earth's share of the results
measured: for a slowly turning exoplanet, where its sunlight falls and how its cloud and rain follow its long
day; for a world still being designed, how high its storms build and which way up they hold their charge, how
much of its rain reaches the ground, how its swell runs up a shore and how long its upper air stays sunlit
after sunset, all before anyone lives under its sky.
```

- **Check.** Each clause of the prospect returns to a line the section developed: the Sun clock (¶8); cloud under slow rotation (intro l.4–5, Way et al.); the storm heights and the charge (¶3, ¶6); the rain (¶3, ¶6); the run-up that SWASH computed from SWAN's spectra (results l.179–181); and the sunlit upper air of the curved-air terms (¶3). Each clause is conditional on the replacements, and scoped to worlds whose air and water resemble Earth's.

### Finding 4. MAJOR. ¶1, l.3–10

- **Text.** "Four codes that began as models of Earth were joined into a chain ..., and the chain was taken to a world whose air is Earth's while its gravity, day, column of air and scale height all differ from Earth's. ExoPlaSim's climate forces CM1, ...; the GCM's surface stress drives SWAN over the seas, and SWAN's spectra drive SWASH up the shore; and the radiation of both atmospheric models was calibrated or checked against a line-by-line model built in house. Most repairs ... were built as switches whose default reproduces the released code, ..."
- **Rule.** The author's direction (remind briefly; the memory records "the contribution in a sentence or two at most"); AGENTS.md "Write for the expert" (delete test); "Technical meaning survives editing".
- **Why.** The opening is the first thing the author reads, and it reads as what was done.
  - l.5–8 restate the introduction's wiring of the chain (intro l.59–68) as a three-part list that the argument leaves unused.
  - "whose air is Earth's" (l.4) overstates the design's air, 1.2 atm with 17.5% oxygen, which the introduction calls "close to Earth's" (l.46–47).
  - "whose default reproduces the released code" (l.9) drops the repairs section's "is written to reproduce" (repairs l.3–5). Runs confirm the identity for five of ten PlaSim patches, and the water scaling reproduces the released code only for spectra like the design case's (repairs l.46–48).
- **Rewrite.** This opens on the modeller's situation, keeps the chain as one clause, and states the idea the section develops:

```latex
A modeller who takes an Earth-built code to another world inherits the values set in it for Earth, and in four
such codes, coupled so that a planet's climate forces both its electrified storms and the waves that run up its
shore, most repairs of those values, and of the defects found beside them, were built as switches whose default
is written to reproduce the released code. On a world whose air resembles Earth's while its gravity, day, column
of air and scale height all depart from Earth's, a modeller can then remove the Earth values one at a time and
measure Earth's share of a result.
```

- **Check.** intro l.28–44 (developers who ported Earth models found Earth values), l.46–49 (the four ratios), l.55–68 (the chain); repairs l.3–5. The reference model moves to ¶5 and ¶11, where its use is discussed.

### Finding 5. MAJOR. ¶2, l.12–17

- **Text.** "Measured that way on the test world, Earth's share was smallest in the units and constants and largest in the fits, ... Correcting the convective cover's unit, or the height scale of the cloud water, moved the global-mean surface temperature by 1.6--2.5~K; calibrating the radiation's fits ... by at least 20~K, and PlaSim's Earth-tuned cloud settings, ... by up to about 6~K. A fit holds near the data it was fitted to, and on a world beyond Earth's range only new evidence can replace it."
- **Rule.** "Technical meaning survives editing"; "Write for the expert" (familiar principles offered as findings; restated implications); charter G3 (compulsory concluding lessons).
- **Why.**
  - "smallest in the units and constants" contradicts the paper's own ranking. The geometry's curved-air terms moved the global mean by 0.65 K, less than either repair of a unit or a constant (results l.87–91).
  - The ranking's three numbers appear here for the fifth time (abstract l.20–23, intro l.82–83, results l.87–91, reach l.3–8).
  - The landing states a principle every modeller holds, and the section states it twice more: "They leave the fits open" (l.38) and "The evidence for a fit has to come from outside the code that holds it" (l.40).
- **Rewrite.** One sentence, landing on the comparison that ¶3 then turns:

```latex
Measured that way on the test world, Earth's share was largest in the fits, the formulas that read as physics
while their coefficients come from Earth's columns, clouds and storms: calibrating the radiation's fits against
the line-by-line model moved the global-mean surface temperature by at least 20~K, and PlaSim's Earth-tuned
cloud settings, pushed to the ends of their tests, moved it by up to about 6~K, where the repairs of units,
constants and geometry, measured one at a time, moved it by 2.5~K or less.
```

- **Check.** results l.36–44, 53–54, 77–91.

### Finding 6. MAJOR. ¶3, opening sentence, l.19–20

- **Text.** "Small as their share of the global mean was, the repairs made by arithmetic put the world's own gravity and geometry into the models, and with them the models computed the features by which such a world departs from Earth."
- **Rule.** "Technical meaning survives editing"; the classes of repair as the paper defines them (repairs l.11–20).
- **Why.**
  - The repairs that ¶3 goes on to name (the fall-speed scaling, CM1's gravity and SWAN's knee) sit in CM1 and SWAN and have no share of the GCM's global mean. The concession fits the GCM repairs of ¶2 alone.
  - "the repairs made by arithmetic" then take in the curved-air terms of l.28–29, a general method whose table is computed from the world's column. The ending separates that method from arithmetic ("constants and clocks by arithmetic, the geometry of tall air from the world's own column", l.94–95).
  - "such a world" extends the test world's features to a class of worlds the runs leave unexamined.
- **Rewrite.**

```latex
Repairs of those kinds, the ones that moved the GCM's global mean least, put the world's own gravity and
geometry into the codes, and with them the codes computed the rain, storms, seas and sky by which the test world
departs from Earth.
```

- **Check.** repairs l.11–20 (general repair, general method), l.54–69 (scaling laws), l.71–73 (CM1's gravity), l.87–105 (curved air). The four nouns announce the paragraph's order, from the drop to the sky.

### Finding 7. MAJOR. ¶3, l.21–30

- **Text.** "On the sea, once the bend in SWAN's wind growth moved with gravity, a lunar sea became the scaled image of an Earth sea, and the same wind, fetch and duration as on Earth raised waves four to five times higher, with periods five times longer and Earth's steepness. Geometry, last, sets the twilight: ... Each of these features lay beyond the models while the code held the Earth value it depends on."
- **Rule.** "Technical meaning survives editing"; "Claims stay within their evidence"; AGENTS.md's rejected example of a "landing that restates the paragraph"; "A genuine catalogue goes in a table or a list".
- **Why.**
  - The sentence makes the knee repair the cause of waves four to five times higher. Released SWAN reads gravity as an input, and it misses the sixfold similarity test by 5.44% in wave height and 3.91% in period (verification l.42–44; claims H04, V04). So the released code computes waves of nearly the same height and period at lunar gravity; the repair brought the scaled image to 0.3%.
  - The landing, "Each of these features lay beyond the models while the code held the Earth value", fails for the seas for that reason. It also restates the opening sentence in reverse, and gives "features" an empty spatial action ("lay beyond").
  - "Geometry, last," marks the paragraph as a four-item list.

  Its images are the section's best (question 1). Ordered from the drop to the sky and ending on the sunlit upper air, the paragraph completes its own movement and needs no restating landing.
- **Rewrite.** The whole paragraph, with findings 6, 14, 15 and 16 repaired in it:

```latex
Repairs of those kinds, the ones that moved the GCM's global mean least, put the world's own gravity and
geometry into the codes, and with them the codes computed the rain, storms, seas and sky by which the test world
departs from Earth. Raindrops fall about three times slower, and in a storm-resolving box, with drop sizes still
set for Earth, 85\% of the water leaving the clouds evaporated on the way down, against 64\% when the same drops
fell at Earth's speeds. Read by CM1's dynamics and microphysics, the same gravity stretched the storms upward
until their tops stood at 55--80~km, and in the electrified run their charge took Earth's arrangement at five to
six times its height. Under the same wind, fetch and duration as on Earth the seas build waves four to five
times higher, with periods five times longer and Earth's steepness, and with SWAN's wind-input knee moved with
gravity the lunar sea is the Earth sea scaled. Overhead, the air stands so tall that a full Earth day after
sunset about half of it still lies above the Moon's geometric shadow, in sunlight that the curved-air terms add
to each layer and that PlaSim's flat columns, lit only while the Sun stands above their own horizon, leave out.
```

- **Check.** repairs l.54–58 (2.94 times slower); results l.122–125 (85 and 64%), l.141–147 (55–80 km; five to six times), l.172–179 (the waves; Earth's steepness); worlds l.78–80 and claim S04 (0.45–0.465 of the column's mass above the shadow, refraction ignored); assumptions l.44–45 (columns lit only while the Sun stands above the horizon). The flash density leaves the paragraph and stays in Results.

### Finding 8. MAJOR. ¶4, l.32–38

- **Text.** "A world that exists only as a design has weather only in its models, and its models have to be checked by means that need no observation of it. Most of the checks made here are of that kind: ... Such checks test whether a code computes what it is written to compute, and they need nothing from the world it models. They leave the fits open, and the fits moved the test world's climate most."
- **Rule.** G1 and the swap test; "Write for the expert" (delete test); "Inheritance and order"; self-reference.
- **Why.**
  - Every check made on the test world needs no observation of it, since none exists, so "Most of the checks made here are of that kind" splits a class that every check belongs to. The paragraph means the checks of the code against itself (verification l.11–12), and l.37 then says so, restating l.32.
  - The middle is the verification section in miniature (verification l.17–28, 39–44), and the landing restates ¶2's ranking a third time.
  - ¶4 opens on a new premise with nothing taken from ¶3's features, so ¶3 and ¶4 trade places. Its real link to ¶3 goes unwritten. The identity runs make each switch's change its own, which is what makes ¶1's measurement of Earth's share clean. A similarity run checks a code's gravity on a world with no observations. CM1's gravity-scaled microphysics, behind ¶3's rain and storms, lacks that check, since its pair failed to convect (verification l.51–52).
- **Rewrite.**

```latex
Computed for a world that exists only as a design, these features can be checked against other models and
against the code itself, and the checks of the code need nothing from the world: five patches at their neutral
settings repeat the runs of the builds before them byte for byte, so that the change each makes when switched on
is its own, and run at a sixth of Earth's gravity with its lengths and times stretched sixfold, the patched SWAN
matches the Earth sea it scales to 0.3\% in wave height, where the released code misses by up to 5.4\%. A
similarity run of that kind tests whether gravity enters a code consistently, a property of the code that holds
on any world, and CM1's gravity-scaled microphysics, behind the slow rain and the tall storms, remains untested
this way, since the pair of runs designed to test it failed to convect. The fits need evidence from outside the
code.
```

- **Check.** verification l.9–15, 17–21, 39–44, 51–52.

### Finding 9. MAJOR. ¶5, l.40–46

- **Text.** "The evidence for a fit has to come from outside the code that holds it. A scheme built from line-by-line spectroscopy would replace ... a comparison planned on the design column. Cloud would be calibrated against runs that resolve it, and \textcite{yang2023cloud} found the two kinds of model far apart on two tidally locked planets: two GCMs covered 82--97\% of the sky, and cloud-permitting runs over sea surfaces fixed from a coarser run, counting cloud by a condensate threshold, 27 and 41\%."
- **Rule.** "Write for the expert" (redundancy); "Sentences carry their dependencies" (coordination for equal weight alone); "Claims stay within their evidence".
- **Why.**
  - The first sentence repeats l.17 and l.38, and "the code that holds it" gives the code an empty action.
  - The second sentence is the abstract's (abstract l.23–26) nearly word for word, and it omits the consequence the paper states for it: a checked scheme would hold on another world within the gases, pressures and temperatures of its checks (next l.15–19).
  - In the third sentence, "and" joins a plan to the evidence that motivates it. The relation is evidentiary, and belongs in the syntax.
  - The section gives the cover numbers and omits the albedos, which lay closer, 2 to 11 points apart, and with which the authors judged the climates broadly similar (results l.95–96). A reader of the conclusion alone takes a threefold gap in cover for a threefold gap in climate.
  - The gapped construction ("..., counting cloud by a condensate threshold, 27 and 41%") makes the reader rebuild the verb.
  - The paragraph leaves out the code's own part: CM1, forced from the GCM's fields by a method built for a slice of any world's GCM (repairs l.187–188), is the means to that calibration. This is the clearest place for the chain to earn its mention.
- **Rewrite.**

```latex
For the radiation's gas and scattering fits, which moved the test world's climate most, that evidence is
spectroscopy: a scheme built from the reference model's line-by-line spectroscopy would replace them, once an
independent code has checked that spectroscopy, a comparison planned on the design column, and would then hold on
another world's columns within the gases, pressures and temperatures of the checks, under the starlight it is
built for. For cloud the evidence is runs that resolve it, which on two tidally locked planets
\textcite{yang2023cloud} found far from two GCMs in cover and closer in albedo: the GCMs covered 82--97\% of the
sky and the cloud-permitting runs, counting cloud by a condensate threshold, 27 and 41\%, while the planetary
albedos lay 2 to 11 points apart. CM1, forced from the GCM's own fields by a method built for a slice of any
world's GCM, computes such runs for the test world.
```

- **Check.** next l.15–19, l.30–36; results l.91–96; repairs l.170–188.

### Finding 10. MAJOR. ¶6, l.48–56

- **Text.** "The resolved runs compute with Earth-fitted laws of their own, and some of those laws come from Earth's laboratories. The two charging laws grafted into CM1 ... they held the lunar storms' charge in opposite arrangements, and measurements of that sign ... would decide which way up the model's storms hold their charge. CM1's raindrops keep Earth's size limits, while the largest drop that survives its fall scales with the capillary length, 2.46 times longer at a sixth of Earth's gravity, a scaling that experiments on the largest stable drops of other liquids, falling through other fluids at Earth's gravity, follow within about 20\% \autocite{loftus2021physics}."
- **Rule.** G1 and the swap test; "Exact action"; "Inheritance and order" (the last sentence completes the movement); "Claims stay within their evidence".
- **Why.**
  - The two cases are parallel and trade places with no loss, so the paragraph is a two-item list.
  - "they held the lunar storms' charge" makes the laws the agents; the storms held the charge, under each law.
  - The paragraph lands on a datum, "within about 20%". It stops the drop case short of the consequence that ¶3 prepared: whether larger drops would let more of the rain reach the ground, and with it whether the design's rain-fed lakes keep their source (next l.78–80).
  - The capillary agreement appears in the conclusion alone, and it supports the largest stable drop. Morrison's limits are a mean-diameter bound and a breakup threshold set for Earth's rain (assumptions l.87–90), so scaling them by the capillary length is a premise of the proposed runs. 9e7c8b4 stated that premise (l.75–78), and this version dropped it.

  Ordered from the law a laboratory can test at the storms' own speeds to the law where the laboratory has to stand in for gravity, the two cases stop trading places.
- **Rewrite.**

```latex
Those runs compute with Earth-fitted laws of their own, and laboratories on Earth can test two of them. The two
charging laws grafted into CM1 disagree on the sign of the charge rimed ice takes in little cloud water, and in
two windows of an earlier run, made before the ventilation repair and with leakage off, the lunar storms held
their charge in opposite arrangements under the two; measured at the speeds at which the storms' hail and
graupel strike, that sign would decide which way up the model's storms hold their charge. Gravity, which a
laboratory on Earth holds fixed, enters the raindrop through the capillary length, and the largest stable drops
of other liquids, falling through other fluids, follow the capillary scaling within about 20\%
\autocite{loftus2021physics}; if the sizes that collisions allow scale as the largest stable drop does, CM1's
limits on raindrop size, scaled the same way, would show how much of the lunar rain's evaporation its small
drops cause, and whether the design's rain-fed lakes keep their source.
```

- **Check.** results l.159–167; next l.73–91; assumptions l.87–90; 9e7c8b4 l.73–79, for the premise on collisions.

### Finding 11. MAJOR. ¶7, l.58–65

- **Text.** "What it takes to use a part of a code on another world follows from how the part was made. A general repair holds as it is, within the limits of its law. The curved-air method holds once its table is recomputed from the new world's own column, ... A calibration has to be refitted on the new world's columns, and for an air or a condensate other than Earth's the radiation, condensation and clouds have to be built anew. Away from Earth's values, the repaired codes have run on the test world alone."
- **Rule.** The author's direction of 2026-10-17 (implied reach to untested worlds is "almost as bad" as the summary); "Claims stay within their evidence"; G1 (one class per sentence, with subject–verb resets).
- **Why.**
  - "A general repair holds as it is" states as fact that a repair holds on worlds where it has yet to run. The introduction says a general repair "is built to hold on another world within the limits of its laws" (intro l.78). Next steps plans the test that would reclassify a repair whose arithmetic fails off the test world (next l.45–47).
  - The paragraph's own last sentence states that the codes have run on the test world alone, so the paragraph claims and withdraws in four lines.
  - The classes come one to a sentence in the paper's order, restating intro l.75–81 and reach l.8–14 and 76–79. The Titan example restates repairs l.105–109.
  - ¶7 takes nothing from ¶6. The turn to other worlds is deliberate, and it can stay as a turn once the paragraph is shorter.
- **Rewrite.**

```latex
What a modeller must do to carry a part of these codes to another world follows from how the part was made: a
general repair is built to hold there unchanged within the limits of its law, the curved-air method once its
table is recomputed from that world's column, and a calibration once it is refitted on that world's columns,
while a world whose air or condensate differs from Earth's needs its radiation, condensation and clouds built
anew. The curved-air method matters wherever the scattering layer stands tall against the radius, as Titan's
haze does at the test world's three hundredths, where the plane-parallel codes that separate surface from haze
hold typically to about 65\textdegree\ from the zenith \autocite{vincendon2010spherical}. Away from Earth's
values, the repaired codes have run on the test world alone.
```

- **Check.** intro l.75–81; reach l.8–14, 76–79; repairs l.105–109.

### Finding 12. MAJOR. ¶8, l.73–74

- **Text.** "The Sun clock and the orbit default keep the global mean of the sunlight arriving at the top of the air, and the Sun clock every zonal mean as well:"
- **Rule.** "Claims stay within their evidence"; "Technical meaning survives editing".
- **Why.**
  - Stated in the present tense, in a paragraph about exoplanets, the clause reads as a property of every configuration.
  - The orbit default discards a configured eccentricity as well as a configured obliquity (reach l.23–24; claim W06). The annual global mean of the arriving sunlight varies with eccentricity, so on an eccentric planet the default moves the global mean.
  - The test world's heliocentric orbit is Earth's, and there the clause holds. 9e7c8b4 scoped it to the test world ("On the test world two of the three kept the global mean", l.13), and this version dropped the scope.
  - The zonal-mean clause appears in the conclusion alone. Its reason, that the Sun clock errs in the Sun's longitude alone, belongs with it.
- **Rewrite.** Incorporated in finding 2.

```latex
On the test world the Sun clock and the orbit default kept the global mean of the sunlight arriving at the top
of the air, and the Sun clock, which errs in the Sun's longitude alone, kept every zonal mean as well:
```

### Finding 13. MAJOR. ¶9 and ¶10, l.79–91

- **Text.** ¶9: "For a constructed world the model is part of the design. ... Until such a world is built its models are the only evidence of its climate, and the Earth values left in them are the design's own uncertainty: ... bracket the warmth within 3.7~K once the transport across the ring is imposed." ¶10: "Designs can also combine Earth's air with a gravity, a size and a day that no known natural world combines with it. By the design's own models, a shield in space would hold Earth's air under a sixth of Earth's gravity, seven times Earth's mass of air over each square metre, with a scale height three hundredths of the radius. A world built that way departs from Earth along every ratio at once, ..."
- **Rule.** The swap test; "Inheritance and order"; "Technical meaning survives editing".
- **Why.**
  - ¶10 restates the introduction nearly word for word (intro l.25–26 and l.49–51), and its link to ¶9 is "also", so the two paragraphs trade places with no loss.
  - Placed before ¶9 and cut to one sentence, the design's freedom becomes the premise of "For such a world the model is part of the design". The reader then comes to the ending from the design, where the ending's prospect begins.
  - "Earth's air" (l.87, 88) overstates the design's air, and "seven times Earth's mass of air" in the same sentence contradicts it. The introduction says "Earth-like air" (l.19, 25).
  - In ¶9 the colon equates the two models' disagreement with the Earth values' effect, and the bracket loses its conditions (results l.117–120: the longwave correction off; about 1.5 K of the bracket the GCM's own over-cooling). Naming the 1.5 K and its Earth-fitted source makes the colon's claim exact.
- **Rewrite.** One paragraph in place of ¶9 and ¶10:

```latex
A constructed world can combine Earth-like air with a gravity, a size and a day that no known natural world
combines with it, and a model run on such a world meets at once the Earth values that a run of a slow rotator or
a smaller world meets one at a time. For such a world the model is part of the design. The test world's shield
was dimmed until the calibrated GCM settled at the design's 295~K, and as the curved-air terms and the carbon
dioxide and oxygen bands entered the radiation, holding that temperature took easing the dimming from 5.0 to
3.0\%; a refitted longwave correction, or cloud calibrated against resolved runs, could move it again. Until
such a world is built its models are the only evidence of its climate, and the Earth values left in them are the
design's own uncertainty: in the air where people and plants would live, the lowest 1.8~km at
45\textdegree\,N, the storm model ran 3.7~K warmer than the GCM that forced it once the transport across the ring
was imposed, and about 1.5~K of that gap is the GCM's own over-cooling through its Earth-fitted longwave.
```

- **Check.** intro l.15–26, l.49–51; worlds l.30–34; results l.58–60, l.101–120; assumptions l.73–75 (PlaSim's longwave, Sasamori's absorptivities, over-cools the lowest layers).

### Finding 14. MINOR. l.24–25

- **Text.** "... and in the electrified run their charge took Earth's arrangement at five to six times its height, flashing at about a hundredth of Earth's average density."
- **Why.** "flashing" attaches to "their charge"; the storms flashed. "Earth's average density" reads as the planet's density, where the measure is flash density (results l.148–149; 9e7c8b4 l.59 said "flash density").
- **Rewrite.** "... and in the electrified run their charge took Earth's arrangement at five to six times its height, while the storms flashed at about a hundredth of Earth's average flash density." (Finding 7's paragraph moves the flash density to Results.)

### Finding 15. MINOR. l.26

- **Text.** "once the bend in SWAN's wind growth moved with gravity"
- **Why.** The body's term is the wind-input knee (assumptions l.22–27, repairs l.67–69, reach l.35, Table 3 of the paper), and the reduction above it acts on the linear wind input alone. Meeting a new name in the conclusion, a reader looks for a second feature.
- **Rewrite.** "once SWAN's wind-input knee moved with gravity"

### Finding 16. MINOR. l.28–29

- **Text.** "air so tall that half of it still lies above the Moon's shadow a full Earth day after sunset"
- **Why.** The body gives "about half" and "the Moon's geometric shadow, before refraction adds more" (worlds l.78–80). The claim record gives 0.45–0.465 of the column's mass (S04).
- **Rewrite.** "air so tall that about half of it still lies above the Moon's geometric shadow a full Earth day after sunset"

### Finding 17. MINOR. l.32, with l.82–83 and l.97

- **Text.** "A world that exists only as a design has weather only in its models"
- **Why.** The sentence states a real premise in the form of an aphorism, with "only" twice. The premise returns at l.82–83 ("Until such a world is built its models are the only evidence of its climate") and at l.97 ("for a world that exists only as a design"), each time in nearly the same words. Stated once as the premise of the checks (finding 8) and once as the design's evidence (finding 13), it deepens in its second use.
- **Rewrite.** "For a world that exists only as a design, every check of its models is made by means that need no observation of it:" (or finding 8's rewrite).

### Finding 18. MINOR. l.71–72

- **Text.** "the Sun clock sets the Sun back about 33\textdegree\ each model day on any non-synchronous planet rotating more slowly than once in 20 days"
- **Why.** The skip is a property of the run, and the body places it there: "in any non-synchronous run on the default solar geometry" (reach l.17–19). 9e7c8b4 said "in a non-synchronous run of any planet" (l.11).
- **Rewrite.** "the Sun clock sets the Sun back about 33\textdegree\ each model day in any non-synchronous run of a planet rotating more slowly than once in 20 days" (incorporated in finding 2).

### Finding 19. MINOR. l.76–77

- **Text.** "A modeller who checks global means passes such errors, and one who maps sunlight by longitude and rain by season finds them."
- **Why.** A balanced antithesis at a paragraph's end is a quotable closing line, and its first half tells readers what to conclude about their own practice. The point needs its second half alone.
- **Rewrite.** "..., a change a modeller finds in maps of sunlight by longitude and of rain by season." (incorporated in finding 2)

### Finding 20. MINOR. l.83–85

- **Text.** "the GCM and the storm model it forces still bracket the warmth within 3.7~K once the transport across the ring is imposed."
- **Why.** The body states the bracket's bounds. It holds under the design-case forcing with the longwave correction off, about 1.5 K of it is the GCM's own over-cooling, and it measures the models' disagreement in that one GCM state (results l.117–120). The conclusion gives the number and omits the bounds.
- **Rewrite.** As in finding 13; or, keeping the sentence, add "..., about 1.5~K of it the GCM's own over-cooling."

## 4. What works

- The excluded words are absent, and the three negations state propositions that need them.
- Every paragraph opens on an idea, and several of these ideas would carry a discussion:
  - "the formulas that read as physics while their coefficients come from Earth's columns, clouds and storms" (l.12–13);
  - the repairs with the smallest share putting the world's own features into the codes (l.19–20);
  - a designed world checked with no observation of it (l.32);
  - a laboratory deciding "which way up the model's storms hold their charge" (l.52–53);
  - "For a constructed world the model is part of the design" (l.79);
  - "the Earth values left in them are the design's own uncertainty" (l.83).
- ¶3's images (l.21–29) are the section's strongest material, and the closest it comes to letting the reader see the world.
- People enter where they belong: "in the air where people and plants would live" (l.84), "before anyone lives under them" (l.101).
- ¶1–¶6 follow one line outward from the code to the laboratory. The joints at ¶1→¶2, ¶2→¶3, ¶4→¶5, ¶5→¶6 and ¶7→¶8 come from the subject matter.
- Qualifications attach once, to the claim they bound: "with drop sizes still set for Earth" (l.22), "made before the ventilation repair and with leakage off" (l.50–51), "each a conditional result that the remaining fits can still move" (l.99).
- "Away from Earth's values, the repaired codes have run on the test world alone" (l.64–65) states the scope plainly, and the ending's prospect is conditional.
- The ending's last clause returns to ¶1's measurement, the tie the author asked for; the rewrite in finding 3 keeps it.
- Every number checked agrees with the body, apart from the ranking in finding 5 and the scope points in findings 7, 12 and 20.

## 5. Counts and verdict

| Severity | Count | Findings |
|---|---|---|
| BLOCKING | 3 | 1, 2, 3 |
| MAJOR | 10 | 4–13 |
| MINOR | 7 | 14–20 |
| Total | 20 | |

Findings 12, 14–16 and 18–20 are sentence-level repairs that the paragraph rewrites of findings 2, 7 and 13 already carry. They stand separately in case a paragraph keeps its sentences.

**Verdict.** The rewrite has moved from the rejected version's inventory toward a discussion. Its paragraphs follow one line outward from the code to the laboratory and then to other worlds, each opens on an idea, and several of those ideas would excite the author: formulas that read as physics; a laboratory deciding which way up another world's storms hold their charge; the model as part of a constructed world's design; the sky of a world computed before anyone lives under it. It has escaped the rejected version only in part. It is as long, it carries nearly as many numbers, and fourteen of the rejected version's fifteen content items reappear in it; its eighth paragraph is the rejected opening rearranged. After each opening idea the paragraphs return to the body's results, and the ending opens by replaying the section's own path. Read as the author would read it, the section is a better-organised summary with a discussion inside it, and I expect the author to reject it again. Acting on findings 1–3 with the paragraph rewrites of findings 4–13 does four things. It turns each paragraph's idea into the thing developed, with the data as its evidence. It writes the joints that the swap test exposes. It corrects four technical points: the ranking of forms, the cause of the larger waves, the orbit default on other worlds, and the reach of a general repair. And it gives the ending its inspiration through physical questions a modeller or a designer could answer, closing on the people who would live under the sky. After that revision a fresh round should read the section again, and the read-aloud pass remains pending.
