# Editorial review, round 1: the closing sections

**Reviewer.** A fresh Claude subagent (Claude Opus 5.5), started on 2026-10-17 for this review with the
text, the author's rules and the evidence files in view, and with no earlier review of the paper.

**Commit.** The review began at commit 4d03a81. During the review HEAD moved to a06a4ab, a commit that
changed `notes/cm1.md`, `notes/defect_log.md`, `notes/exoplasim.md` and files under `paper/notes/` and
`paper/review/`. Every section file kept the hash listed below, so the findings apply at both commits.

**Files in scope (sha256).**

| File | sha256 | Read |
|---|---|---|
| `paper/sections/reach.tex` | `817ee9ed88c4d9471d313708a4fc1b186d1e903e692c40c3d7e2d5bdf756a42f` | in full, with Table `tab:reach` |
| `paper/sections/next.tex` | `2c36f239634b8562ce7e5294e16ff4178e571163b50035ed303185f5973e24cb` | in full |
| `paper/sections/conclusions.tex` | `596dda2e4e628233793e76f972c37e7ba78ff3b7fe8681224c13373a0afca910` | in full |
| `paper/sections/availability.tex` | `44f67347836075fb4b6f99d1670ca52bf7ec30499170a87d6a2d19679ac95e3e` | in full |
| `paper/sections/appendix.tex` | `eaf27468e42bc1a28a57a6fdcafd8b7fa58365254e5ad965a794862237e196c6` | in full; findings confined to its opening paragraph and the three table captions |

**Rules, context and evidence (sha256).** The rules were read in full before the paper, and their general
requirements applied with their subject matter set aside. The context sections were read in full: the
abstract, introduction and results for what the closing sections must land on, and the other four sections
to trace the terms and facts the closing sections take from earlier pages. The evidence files were
consulted for facts only, to the extent stated.

| File | sha256 | Read |
|---|---|---|
| `AGENTS.md` | `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32` | in full, above all "The paper", "Writing" and "Review" |
| Terluna `ensemble/planning/Open_Moon_Editorial_Charter_control-01.md` | `aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0` | in full |
| Terluna `…/source_controls/STYLE_NOTES.md` | `659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46` | in full |
| Terluna `…/source_controls/Jewish_Papers_Updated_Style_Notes.md` | `18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab` | in full |
| Terluna `…/source_controls/Agent_Working_State_Editorial_Gates.md` | `553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464` | in full |
| `paper/sections/abstract.tex` | `b8b0f6fd8c184465454f7265f6870d2b5f8ac2c56386654d827c6f5595834921` | in full |
| `paper/sections/introduction.tex` | `5d1b9cf839ea398370c884d828d54fe45951ab79492e9f3c7a3fce6a70aff9e0` | in full |
| `paper/sections/results.tex` | `a864fc868d6f3cd0aaa23015813cb2b5b7fbe214573be229c4ec3c0b7ee7bdc6` | in full |
| `paper/sections/worlds.tex` | `46dc5b00bfd347693c0f57929ee690f4db4cd1a4ac97b996b82af07f010ff0b2` | in full |
| `paper/sections/assumptions.tex` | `4b0f209c6aebcbc4c907778548d27c5dca9512e3d44347ccf7cdff2f98b9cfd7` | in full |
| `paper/sections/repairs.tex` | `3bcef8a3a813e83b33cf4f954da68c05ce6bd78f8d31375808a955162dca81ef` | in full |
| `paper/sections/verification.tex` | `a3ca68dc2de6007d42e0081a2bbbb4e1308dfea16e406b8d577fdee65ad3cfa5` | in full |
| `paper/main.tex` | `87c1cddb6bc6a68d5a7666d4f310f250389600a5e640c3ffd8470d9ada41371c` | in full |
| `paper/claims.json` | `81d5ddce23c25b9accea366278fd7260c450799d6356aeaee46e6c210ac9202f` | the entries cited below |
| `paper/data/repairs.json` | `d4fc5bce0b5fa92d623abc4a073befc2faf167d33d32c5c8e83e6fc6008d19bc` | in full |
| `paper/data/worlds.json` | `70dabbec07bf13ab1b31d1e60904d33eac44d0928f9ab50b965937eb3f7916f0` | in full |
| `notes/exoplasim.md` | `707d97ef683d2650db8044cfee18f3a3ac7c82675dc37f4222476a6a4c978bf2` | in full |
| `notes/cm1.md` | `75502ec7070a240006db6e4d491a6973cd2f013cc0c0945c3e61fb36b9fa5510` | in full |
| `notes/defect_log.md` | `92b3443dbe3da76ee4c6f8a858a41acab0dc94d05d5cead61aa042b2a120d700` | entries A1, A2 and B11 |
| `notes/electrification.md` | `2cd81eb8edbd77348133a1e4aaca859b52ca4d0015bc5b26bf12e5d93308f59f` | its second half |
| `notes/waves.md` | `9f7a775ed1b8a297a4d4a8cf0cd416a8e732b8367cf9f241aaa15dc69cb28102` | swell, convergence and improvement sections |
| `notes/reference_radiation.md` | `348501fa28bbe855f6cc99a200d81004fb4163fe91dd0ccccaa13517bbae2730` | its summary and section 1.6 |
| `paper/sources/manifest.json` | `bcbe4f0643530f541fb03e37938a58e56970fb6d8f37e3a01d5ef95d1acd0503` | the entries for `yang2014strong` and `way2018climates`, with a text search of those two archived originals |
| `paper/tools/check.py` | `a72fc248a4bdf5f55b2ff8327f745f5cbb3f2f2dfd07e1b85c7be01c29d71f51` | its docstring and main routine |

Read-only git queries covered Terluna's history at 186b294 and this repository's remotes. During the
review, parallel sessions changed `paper/references.bib` and `paper/sources/manifest.json` in the working
tree, uncommitted (the manifest's hash is now `584c36a3156bab662399c16792656dbc27be95cd661273d952ea2f1c1e241c41`);
the manifest hash in the table is the version read here, and finding 31 notes the bibliography change. `paper/review/`
and `paper/notes/` stayed unread, as the brief directs; their file names appeared once, in git's change
summary for a06a4ab.

**Method.** Each paragraph was read whole and then sentence by sentence, through the ten passes of the
charter's section 11, and each number and condition was traced to the register, the data extracts and the
notes. The cadence pass was a silent reading on screen. No build, test or state-changing git command ran,
and this file is the only file written.

## Findings

### 1. BLOCKING. The general repairs credited with effects measured together with a calibration; the ice optics placed on both sides

- **Location:** `reach.tex:4–6`; `conclusions.tex:12–17`.
- **Text (reach.tex:4–6):**
  > The general repairs, which another world takes unchanged, moved the global mean by a few kelvin at
  > most and moved where sunlight and rain fall; the calibrations and the Earth-tuned cloud settings, which
  > another world must remake, moved it most.
- **Text (conclusions.tex:12–17):**
  > The general repairs, which another world takes unchanged, moved the Moon's global mean by a few kelvin
  > at most and moved where its sunlight and rain fall, cutting the rain by nearly a quarter and raising the
  > share of land under half a millimetre a day from a tenth to two fifths. The parts another world must
  > remake moved it most: the first calibration by at least 20~K, PlaSim's Earth-tuned cloud by up to about
  > 6~K, and its longwave cooling by height, corrected with ice optics, by about 11.5~K in a run outside the
  > correction's fitted state.
- **Rule:** Technical meaning survives editing (G5): each sentence keeps the claim's conditions and
  evidence state. Claims stay within their evidence.
- **Why:** The rain and dry-land changes come from one step that applied the Sun clock and the Moon's tilt
  together with the recalibrated split of sunlight (`results.tex:40–42`; `data/repairs.json`, row "The
  Sun's clock, the Moon's tilt and the sunlight split"; defect log A2, "With A1 and A2 corrected and the
  shortwave recalibrated (B17)"). The split's near-infrared water multiplier is a calibration (Table
  `tab:repairs`, patch 05), and in the conclusions the whole step is credited to the general class. The ice optics,
  classed general in Table `tab:repairs` and in `reach.tex:9`, ran only inside the longwave test, so their
  own effect on the global mean is unmeasured; `notes/exoplasim.md` records only a radiative change, the
  high cloud's net warming falling from 12.4 to 5.7 W m⁻² in one year. `reach.tex` bounds the general class
  at "a few kelvin" with that member unmeasured, and in the conclusions the joint 11.5 K is filed under the parts
  another world must remake. Both sentences state the relation that the conclusions develop, that the
  parts holding on other worlds moved the climate least, so the paper's final argument is built on the
  misattribution.
- **Rewrite (conclusions.tex:12–17):** "Measured one at a time, the general repairs moved the Moon's global
  mean by a few kelvin at most, 2.3~K over the years averaged for the cloud water counted by pressure, the
  largest. The Sun clock and the Moon's own tilt, applied with the split of sunlight recalibrated, cut the
  rain by nearly a quarter and raised the share of land under half a millimetre a day from a tenth to two
  fifths. The parts fitted to one world's columns moved the Moon furthest: the first calibration by at
  least 20~K, PlaSim's Earth-tuned cloud settings by up to about 6~K, and the longwave correction, run with
  the ice optics in a state outside its fit, by about 11.5~K, of which the ice optics' share is
  unmeasured." For `reach.tex:4–6`, see the paragraph rewrite under finding 7.

### 2. BLOCKING. The last claim of the conclusions contradicts the paper's own classes

- **Location:** `conclusions.tex:22–27`; the same claim at `abstract.tex:16–17`.
- **Text:**
  > The work that would narrow the Moon's remaining uncertainty is therefore the work that would extend the
  > models to other Earth-like worlds. A radiation scheme built from the reference's own spectroscopy in
  > place of fitted coefficients, cloud constrained by cloud-resolving runs in place of Earth's settings, and
  > a reference checked against an independent code would each turn a part that holds near one column into
  > one that holds wherever its physics does, …
- **Rule:** Claims stay within their evidence ("each" checked against what was examined); technical
  meaning (G5); the abstract, the opening and the conclusion land on the same, accurate contribution.
- **Why:** `repairs.tex:19–20` defines a calibration as the adjustment of an approximate scheme's free
  coefficients until its output matches a reference on chosen columns, holding near the states it was
  fitted on. `next.tex:18–19` describes the cloud step as fitting PlaSim's humidity thresholds and
  cloud-water profile to CM1's cloud cover and water: by that definition a calibration to a cloud-resolving
  reference, valid near the lunar columns and repeated for each other world (`notes/exoplasim.md` names
  the route "CRM-informed cover"). The check of the reference against LBLRTM and a DISORT-based solver tests
  the spectroscopy beneath every calibration and leaves every part in its class. Of the three items, the
  reduced correlated-k scheme alone turns a fitted part into one that holds wherever its spectroscopy does.
  The identity in the first sentence therefore holds for the radiation, and "each" holds for one item of
  three. The abstract's last sentence states the same identity for "the reference's physics and …
  cloud-resolving runs", so abstract and conclusions land together on the overstated form.
- **Rewrite:** "Replacing the fitted parts that moved the Moon most would narrow its uncertainty, and where
  the replacement is computed from physics it would extend the models as well. A reduced correlated-$k$
  scheme built from the reference's spectroscopy in place of Sasamori's and Lacis and Hansen's fits would
  hold on any column whose gases and pressures that spectroscopy covers; PlaSim's cloud fitted to
  cloud-resolving runs would remain a calibration, refitted for each other world with cloud-resolving runs
  of that world; and a check of the reference against LBLRTM and a DISORT-based solver would test the
  spectroscopy to which every calibration was fitted. Runs of the repaired ExoPlaSim on Earth-air slow
  rotators would show whether the parts classed as general hold off the Moon." The matching abstract
  sentence: "Rebuilding the radiation from the reference's spectroscopy would narrow the Moon's uncertainty
  and extend the models together; fitting PlaSim's cloud to cloud-resolving runs would narrow the Moon's
  alone."

### 3. BLOCKING. The cloud step proposes a forcing whose result already stands in the results

- **Location:** `next.tex:17–19`.
- **Text:**
  > Forcing CM1 from the design case, with the transport across each ring imposed, tests first whether the
  > near-ground gap closes, and then gives cloud cover and water by pressure to which PlaSim's humidity
  > thresholds and its cloud-water profile can be fitted.
- **Rule:** G5: a proposed study names the question it discriminates and the condition that makes its
  comparison new; technical meaning holds across sections.
- **Why:** The 45°N ring forced from the design case with the GCM's transport imposed has run, and its
  offset fell from 5.9 to 3.7 K (`results.tex:76–79`; `notes/cm1.md:117–122`). The open test is a forcing
  from the longwave-corrected GCM (`verification.tex:105–106`; `notes/cm1.md:126–127` and `160–161`). As
  written, the proposed test has its answer at 45°N in the results already, and the condition that would
  make it a test of the corrected physics is missing.
- **Rewrite:** "Forcing CM1 from the consistent state of the first step, with the transport across each ring
  imposed, tests whether the corrected longwave closes the 3.7~K by which CM1's lowest 1.8~km at
  45\textdegree\,N stays warmer than the GCM's, and the cloud cover and water by pressure of those runs
  become the target to which PlaSim's humidity thresholds and its cloud-water profile are fitted."

### 4. BLOCKING. The adapted CM1 credited with storms at any gravity

- **Location:** `reach.tex:38–41`; Table `tab:reach`, `reach.tex:89`, column "Reached by the adaptations".
- **Text:**
  > Taken model by model, the adapted CM1 runs storms in Earth-like air at any gravity on its Morrison and
  > NSSL paths, SWAN and SWASH run water seas at any gravity by similarity with Earth's empirical laws, and
  > ExoPlaSim, bounded by its radiation fits and its cloud, has the narrowest reach of the three.

  Table cell: "Any gravity on CM1's Morrison and NSSL paths".
- **Rule:** Claims stay within their evidence: each universal claim is checked against what was examined.
  G5 keeps evidence states apart.
- **Why:** The adapted CM1 ran at the Moon's gravity and, in the Earth benchmarks, at 9.81. The pair of runs
  designed to measure its gravity-scaled microphysics failed to convect (`verification.tex:38–40`);
  Morrison's limits on rain size, breakup and ice size stay Earth's, snow takes a smaller gravity exponent
  than its own laws give, and autoconversion and accretion remain Earth fits (`notes/cm1.md:64–77`;
  `next.tex:48–50`). The same table row lists "drop limits and breakup" as beyond the adaptations. "At any
  gravity" follows from a code property, gravity read as a parameter on those paths, and reads as a reach. The
  SWAN clause names its evidence state (similarity with Earth's laws); the CM1 clause omits its own. The
  sentence also states ExoPlaSim's reach only by comparison ("the narrowest of the three") and leaves CM1's
  range in day length and pressure unstated, though stating the per-model reach is the paragraph's task.
- **Rewrite:** "Model by model, the adapted CM1 reads gravity as a parameter on its Morrison and NSSL paths
  and has run storms at the Moon's gravity and at Earth's; its drop limits and breakup remain Earth's, and
  their effect at other gravities is unmeasured, since the similarity pair failed to convect. Its Sun and
  soil are built for days from a few Earth days to the Moon's, and RRTMG's tables end at 1.05~bar. SWAN and
  SWASH run water seas at any gravity as the scaled image of an Earth sea, tested at a sixth of Earth's
  gravity, with Earth's empirical laws. ExoPlaSim holds near the columns its radiation and cloud were
  fitted on: Earth-air columns near Earth's warmth with the released radiation, and the lunar design
  columns with the calibrations." Table cell: "Gravity read as a parameter on CM1's Morrison and NSSL
  paths, run at 1.62 and 9.81".

### 5. BLOCKING. Public availability stated as complete

- **Location:** `availability.tex:25–26`, with `availability.tex:3–10`.
- **Text:**
  > The author declares no competing interests: the work is an unfunded personal project that earns the
  > author nothing, and every part that may be made public is public.
- **Rule:** Claims stay within their evidence; report actual checks; a declaration states what it declares.
- **Why:** At 4d03a81 and at a06a4ab this repository's working copy has no git remote, and the code-and-data
  paragraph names "the world-crafting repository" with no address. The model runs are "held on the
  project's research drive", whose paths in the register (`/media/projectspace/terluna-research/…`) are a
  local mount, and no route of access is given. "Every part … is public" therefore claims a publication
  absent from the working copy's configuration, unless the repository was published by another route, in
  which case its address belongs in the code-and-data paragraph. The
  competing-interests declaration also contains an availability claim, and "the release
  register" (L7) names an internal record that an outside reader has no route to.
- **Rewrite:** Competing interests: "The author declares no competing interests; the work is unfunded and
  brings the author no income." Code and data, end of its first sentence: "… are held in the world-crafting
  repository, published at [address] with its release commit [hash]"; and for the runs: "the model runs
  themselves are held on the project's research drive, [available from the author on request / at
  address]". The bracketed facts are the author's to supply.

### 6. MAJOR. A pun and two empty actions open the reach section

- **Location:** `reach.tex:3–4`.
- **Text:**
  > The results sort the adapted models' parts by how far they moved the Moon, and the classes of repair
  > sort the same parts by how far they travel.
- **Rule:** No witticisms; exact action.
- **Why:** The sentence sets two senses of "how far" side by side, kelvin moved and worlds reached, and the
  paragraph's governing relation is stated through that play of words. Results and classes are given sorting, and
  code is given travel. The relation itself is plain and measured: the largest changes came from fitted
  parts.
- **Rewrite:** "The largest changes to the case's climate came from parts fitted to one world's columns, and
  the general repairs, whose values hold on other worlds, changed its global mean by a few kelvin at most."
  The paragraph rewrite under finding 7 takes this sentence in.

### 7. MAJOR. Reach, first paragraph: a class inventory in prose, motion verbs, and a landing that restates the opening

- **Location:** `reach.tex:6–16`.
- **Text:**
  > The general repairs are the synodic Sun clock, the fixed orbit and whole model days, convective cover per
  > Earth day, cloud water by pressure, gravity throughout CM1 with the fall-speed scaling, CM1's Sun for any
  > day and its deeper soil, the lifted breakdown cap and the scaled sub-step, SWAN's knee, and the ice
  > optics. Leakage and the methods that force a slice of a GCM travel with their inputs, a conductivity
  > column or a GCM's fields, and the leader's crossing travels as a bound set between two of WRF-ELEC's
  > rules; the curved-air terms travel as a method whose table is computed again for each column; and the
  > calibrations, …, hold near the case they were fitted on. Another world therefore takes the general
  > repairs unchanged and needs its calibrations, its ledger and its settings made again, with tools that
  > come with the repairs: the reference model, the ledger and offline copies of PlaSim's radiation.
- **Rule:** A genuine catalogue goes in a table or a list (G1); exact action; the delete-test for restated
  implications (G2).
- **Why:** The first two sentences list class membership, which Table `tab:repairs` lists change by change
  in its Class column, and within each list the items could be reordered without loss. "Travel" appears
  three times for repairs and methods. The landing repeats the clause "which another world takes
  unchanged" of L4; its new content is the list of tools. "Computed again for each column" reads as each
  GCM column, while the method uses one clear design column for every GCM column (Table `tab:reach`, "one
  clear column for all"); the table is computed for each world's column. "Its ledger" and "the ledger" in
  one sentence name a table and the code that computes it. "SWAN's knee" shortens "SWAN's wind-input
  knee", the name used where the term entered.
- **Rewrite of reach.tex:3–16, taking in findings 1, 6 and 7:** "The largest changes to the case's climate
  came from parts fitted to one world's columns: the first calibration moved the global mean by at least
  20~K, PlaSim's Earth-tuned cloud settings by up to about 6~K and the longwave correction, run with the
  ice optics, by 11.5~K. Measured one at a time, the general repairs, whose values hold on other worlds
  within the limits of Table~\ref{tab:reach}, moved it by a few kelvin at most, and the Sun clock and the
  Moon's tilt, applied with the split of sunlight recalibrated, moved where sunlight and rain fall; the ice
  optics' own share of the longwave run is unmeasured. Each change's class is in Table~\ref{tab:repairs}.
  For another world a modeller applies the general repairs unchanged, recomputes the curved-air table from
  that world's own column, refits the Rayleigh and water multipliers, the water continuum, the longwave
  correction and the gas-band fits against the reference model, and sets the scenario's values; leakage
  and the slice forcing read that world's conductivity column and GCM fields, and the leader's crossing
  stays a bound between two of WRF-ELEC's rules. The reference model, the ledger's code and the offline
  copies of PlaSim's radiation, all in the code repository, compute the new table and the refits."

### 8. MAJOR. Worlds and adaptations given actions: "another world takes", "the adaptations reach"

- **Rule:** Exact action. `AGENTS.md` lists "reaches" among the empty actions of abstractions. A world or an
  adaptation performs no taking, remaking or reaching; a modeller applies and refits, and a model
  represents or simulates.
- **Why:** The vocabulary appears throughout the section: the reader meets worlds that take repairs, parts that travel
  and adaptations that reach, while the operations behind them, a modeller applying a repair or refitting a
  calibration and a model computing a world's column, stay unnamed. The noun "reach" in the section title
  can stand as the section's term if defined once ("the reach of a model, the worlds on which its repaired
  code holds"); the verbs need the rewrite.
- **Locations, text and rewrites:**

| Location | Text | Rewrite |
|---|---|---|
| `reach.tex:41–42` | "Table~\ref{tab:reach} sets out, property by property, where the released models break, what the adaptations now reach and what lies beyond them." | "Table~\ref{tab:reach} lists, property by property, where the released models err, what the adapted models now represent and what lies beyond them." |
| `reach.tex:42–44` | "only Earth lies within that reach; the rest of it lies among constructed worlds and among exoplanets whose air is taken to be close to Earth's." | "Earth alone lies within it, and the other worlds within it are constructed worlds and exoplanets whose air is taken to be close to Earth's." |
| `reach.tex:46` | "The breathable Moon under other dimmings runs in all four models" | "The four models simulate the breathable Moon under other dimmings" |
| `reach.tex:62–63` | "though ground standing below that level takes RRTMG past its tables, as the lunar seas do" | "while the pressure on ground below that level lies past RRTMG's tables, as it does over the lunar seas" |
| `reach.tex:63–64` | "Earth-like air on a larger planet comes within reach the same way, with the cloud water's error running the other way" | "Earth-like air on a larger planet needs the same steps, a slant factor from its own column among them; there the released cloud water errs toward too much water, the reverse of the Moon's error, and the same general repair corrects it" |
| `reach.tex:70` | "their general repairs would hold" | "the general repairs of units, clocks and gravity would apply to them unchanged" (the density-scaled breakdown, a general repair, holds in nitrogen–oxygen air, and Table `tab:reach` lists breakdown in other gases as beyond) |
| `reach.tex:79–80`, `87` | caption "what the adaptations reach"; header "Reached by the adaptations" | "what the adapted models represent"; "Represented by the adapted models" |
| `reach.tex:29, 46, 59, 68` | run-in heads "Where Earth values break."; "Within reach as adapted."; "Within reach with a new column."; "Beyond reach." | "How the Earth values err."; the heads of finding 9's regrouping |
| `conclusions.tex:12, 15` | "which another world takes unchanged"; "The parts another world must remake" | as in findings 1 and 14 |

### 9. MAJOR. The groups of worlds mix what each world needs with how far the runs tested it

- **Location:** `reach.tex:46–66`.
- **Text:**
  > \textbf{Within reach as adapted.} The breathable Moon under other dimmings runs in all four models with
  > the repairs as they stand, … At 1.0~atm, a case yet to be run, or behind another shield that blocks the
  > ultraviolet, it needs its calibrations refitted against the reference and its cloud settings checked; …
  > Slowly rotating and synchronous planets … should need only ExoPlaSim's general repairs, though none has
  > been run …
- **Rule:** G1: the governing relation sets the order of paragraphs. G5: evidence states stay distinct.
- **Why:** The head promises worlds the models take as they stand. The paragraph then holds the Moon at
  1.0 atm and behind other shields, which need refitted calibrations, the condition that defines the next
  paragraph, and Earth-air slow rotators, which no run has tested. The three groups therefore mix two
  criteria, what a world needs from the modeller and how far the evidence goes. The section's own material
  sorts into four groups by what the modeller supplies: nothing (the Moon near its fitted columns, run);
  the general repairs alone (Earth-air slow rotators of a Sun-like star, expected and unrun); a column of
  the world's own with refitted calibrations (the Moon at 1.0 atm or behind another shield, Mars held at
  1 bar, Earth-like air on a larger planet, a breathable moon of a giant planet with the host's glow); and
  new radiation, condensation and cloud (Titan, present Mars, Venus).
- **Rewrite (heads and opening sentences):** "\textbf{Worlds the repaired models simulate as they stand.}
  With the repairs as they stand, the four models simulate the breathable Moon under other dimmings while
  its columns stay near the fitted ones: the split of sunlight falls 0.7 points short on a 303~K column
  with 338~kg\,m$^{-2}$ of vapour, and the longwave correction's accuracy near 307~K is unchecked. [The
  slow-rotator sentence of finding 11, then the sentence on rotations slower than 20 days, unchanged.]
  \textbf{Worlds that need a column of their own and refitted calibrations.} The breathable Moon at
  1.0~atm, a case yet to be run, or behind another shield that blocks the ultraviolet needs its
  calibrations refitted against the reference and its cloud settings checked; under a shield that passes
  the ultraviolet the air would form ozone, which every patched CM1 build sets to zero. A constructed world
  with breathable air on a small body, such as Mars held at 1~bar, … [as drafted, with the wording of
  finding 8]. \textbf{Worlds that need new physics.} Titan's nitrogen--methane air at 94~K, …"

### 10. MAJOR. The Sun clock's condition dropped, so "any" claims more than the examined runs

- **Location:** `reach.tex:18–20`; `conclusions.tex:7–8`.
- **Text (reach.tex:18–20):**
  > Three of ExoPlaSim's defects act well beyond the Moon. Its Sun clock, in any non-synchronous run whose
  > rotation differs from one day, skips back $1/(N-1)$ of a turn each model day, …
- **Text (conclusions.tex:7–8):** "the clock in any non-synchronous run whose rotation differs from a day"
- **Rule:** Claims stay within their evidence; technical meaning survives editing.
- **Why:** Upstream issue #69 and the defect log place the defect in non-synchronous runs with
  `rotationperiod` ≠ 1 and `keplerian=False`, ExoPlaSim's default solar geometry (`notes/defect_log.md`,
  A1; `notes/exoplasim.md`, "The Sun's clock"), and `assumptions.tex:102–103` keeps the condition ("on its
  default solar geometry"). The closing sections drop it, and "any" then extends the defect to runs on the
  Keplerian geometry, which no check examined. In "act well beyond the Moon", defects are given an action and a
  place; they bias other users' runs. The paragraph also opens with nothing inherited from the one before,
  and naming the general repairs that remove these defects supplies the link.
- **Rewrite (reach.tex:18–20):** "Three of the defects that the general repairs remove remain in the
  released ExoPlaSim and bias other users' runs. Its Sun clock, in any non-synchronous run on its default
  solar geometry whose rotation differs from one day, skips back $1/(N-1)$ of a turn each model day, …"
  Conclusions: "the clock in any non-synchronous run on ExoPlaSim's default solar geometry whose rotation
  differs from a day".

### 11. MAJOR. Starlight, one of the four properties the paper names, is absent from the reach

- **Location:** `reach.tex:51–54`; Table `tab:reach` (`reach.tex:86–98`).
- **Text:**
  > Slowly rotating and synchronous planets with Earth's gravity and air, common subjects of exoplanet GCMs
  > \autocite{yang2014strong,way2018climates}, should need only ExoPlaSim's general repairs, though none has
  > been run: the released radiation stays near the column it was fitted on as long as the climate stays
  > near Earth's warmth.
- **Rule:** G5: conditions and scope survive; the abstract, opening and conclusion develop the same
  contribution.
- **Why:** The abstract (`abstract.tex:2–3`) names "gravity, size, day or starlight" as the properties in
  which these worlds differ, and the introduction (`introduction.tex:22–24`) records that ExoPlaSim's
  near-infrared water absorptivity is tuned to a solar spectrum. The synchronous planets that the same
  section names, TRAPPIST-1e and Proxima Centauri b (`reach.tex:25–26`), orbit M dwarfs, whose light lies
  outside that tuning, and CM1's RRTMG takes the Sun's own spectrum (`notes/cm1.md:146–148`). The
  sentence's reason covers the column alone, and Table `tab:reach` has rows for gravity, day, tilt, tall
  air, heavy air, composition, cold cloud, electricity and seas, with starlight absent.
- **Rewrite:** "Slowly rotating planets with Earth's gravity and air around a Sun-like star should need only
  ExoPlaSim's general repairs, though none has been run, since the released radiation was fitted on columns
  and a spectrum like theirs; synchronous planets of M dwarfs, such as TRAPPIST-1e and Proxima
  Centauri~b, add a spectrum outside the near-infrared water fit, and their shortwave needs refitting
  against the reference with the star's spectrum." New row of Table `tab:reach`: "Starlight other than the
  Sun's & PlaSim's near-infrared water fit, tuned to a solar spectrum; RRTMG's solar spectrum & The
  shield-filtered Sun, through multipliers refitted to the reference & Other stars' spectra".

### 12. MAJOR. A field characterised from two studies

- **Location:** `reach.tex:51–52`.
- **Text:** "common subjects of exoplanet GCMs \autocite{yang2014strong,way2018climates}"
- **Rule:** Claims stay within their evidence: a statement about a field says what the cited works did,
  scoped to them. `AGENTS.md`'s table of rejected first-draft sentences holds the same case.
- **Why:** The two citations support what their authors did: Yang et al. (2014) varied rotation in CAM3,
  with a synchronously rotating case among their runs, and Way et al. (2018) ran slow rotators in ROCKE-3D
  at day lengths that include 16 and 64 days (both archived originals, text searched). "Common subjects"
  speaks for the field. The source manifest records the use in the same field-wide words.
- **Rewrite:** "Slowly rotating planets with Earth's gravity and air, such as those \textcite{yang2014strong}
  and \textcite{way2018climates} simulated with CAM3 and ROCKE-3D, …" (joined with the sentence of
  finding 11).

### 13. MAJOR. The conclusions open by restating the defect inventory

- **Location:** `conclusions.tex:3–9`.
- **Text:** the paragraph, ending:
  > All three act in other users' runs as well, the clock in any non-synchronous run whose rotation differs
  > from a day, the rain unit in synchronous runs too, and the orbit default in any run that sets a tilt
  > without fixing the orbit.
- **Rule:** A conclusion gathers the developed lines into a new relation or consequence; reciting the
  inventory is excluded (charter section 11; `AGENTS.md`, "Conclusions and the arc").
- **Why:** The paragraph repeats `reach.tex:18–27` and the abstract's sentence on the three defects with the
  conditions reworded, and lands on their presence in other users' runs, the subject of a reach paragraph.
  The paper developed a relation that the paragraph leaves unstated: each defect produces little or no error at
  Earth's values and an error that grows as a world departs from Earth in one property, so the error stays
  small in tests at Earth's values and grows large on a world far along all four ratios (`introduction.tex:26–29`;
  `worlds.tex:3–4`; `assumptions.tex:119`). "A rain unit" renames the convective-cover unit, and "the rain
  unit in synchronous runs too" drops its main condition, a model day other than one Earth day.
- **Rewrite:** "Each of the three upstream defects found on the Moon produces little or no error at Earth's
  values and an error that grows as a world departs from Earth in one property: the Sun clock's skip with
  slower rotation, to 33\textdegree\ a model day beyond a 20-day rotation; the convective-cover unit's bias
  with the logarithm of the model day; and the orbit default's error with the distance of a world's tilt
  from Earth's. In the lunar runs, far along all four ratios at once, the three errors grew large enough to
  find, and the same arithmetic biases other users' runs: the Sun clock in non-synchronous runs on
  ExoPlaSim's default solar geometry, the convective-cover unit in any run whose model day differs from one
  Earth day, synchronous runs included, and the orbit default in any run that sets a tilt without fixing the
  orbit."

### 14. MAJOR. The central relation of the conclusions stated through a figure

- **Location:** `conclusions.tex:11–12`.
- **Text:**
  > Removing the Earth values sorted the models' parts twice, by how far each moved the Moon and by how far
  > each travels, and the two orders run against each other.
- **Rule:** Exact action; no witticisms; technical meaning.
- **Why:** Removing values sorts nothing: the parts were ranked by measured effect and classed by where their
  values come from. "Travels" repeats the figure of `reach.tex:4`, and "the two orders run against each
  other" states a strict inversion, while the measured effects follow that order only at the extremes: the gas-band fit, a
  calibration, moved the global mean 2.2 K, beside the cloud-water repair's 2.3 K. PlaSim's cloud settings
  entered the ranking as tests of values left in place, so "removing the Earth values" also misdescribes
  how they entered.
- **Rewrite:** "The largest changes to the case's climate came from parts fitted to one world's columns,
  which are refitted for each other world, and the general repairs, which apply unchanged elsewhere,
  changed its global mean by a few kelvin at most."

### 15. MAJOR. Storm and sea results appended to the paragraph on fitted parts

- **Location:** `conclusions.tex:17–20`.
- **Text:**
  > Where CM1 forms its own cloud and rain at lunar gravity, the freezing level stands five to six times
  > higher than Earth's, most of the falling water evaporates before it reaches the ground, and the lightning
  > is rarer and larger than Earth's, with a sign set by a laboratory charging law; SWAN, by similarity,
  > raises waves four to five times higher than Earth's under the same wind.
- **Rule:** Reciting the inventory is excluded from conclusions; swap test (G1); landings complete the
  movement (G3).
- **Why:** The sentence lists results with no tie to the paragraph's subject, which parts moved the climate,
  and it could stand anywhere in the conclusions without loss. The results section holds the relation the
  paragraph needs: the two atmospheric models disagree where each runs on Earth fits of its own
  (`results.tex:88–96`). That relation is also the result of the test that the introduction names in its
  last sentence, agreement among independent models (`introduction.tex:65–67`), which the conclusions leave out.
  The freezing-level comparison drops "in Earth's tropics" (`results.tex:108–109`), and the lightning comes
  from one electrified box over two lunar days, forced from the pre-correction run.
- **Rewrite:** "The two atmospheric models disagree most where each runs on Earth fits of its own: with the
  GCM's transport imposed, CM1's lowest 1.8~km at 45\textdegree\,N stays 3.7~K warmer than the GCM's, and a
  box forced from the GCM brings a quarter of the forcing GCM's rain to the ground, the GCM's rain set by
  its convection scheme and CM1's by Earth's drop limits; in the one electrified box, the sign of the
  lightning changes with the laboratory charging law chosen."

### 16. MAJOR. The conclusions name no world

- **Location:** `conclusions.tex`, whole; the promise at `introduction.tex:63–65`.
- **Text (introduction.tex:64–65):** "the three classes set which other worlds the adapted models can reach."
- **Rule:** The abstract, the opening pages and the conclusion promise, develop and land on the same
  contribution.
- **Why:** The introduction promises the worlds open to the adapted models and the reach section sorts them,
  while the conclusions name none; their one statement at the scale of worlds is the closing test on slow
  rotators.
- **Rewrite (a sentence to open the third paragraph):** "The worlds open to the adapted models are ordered by
  how far their columns lie from a fitted one: the Moon near its fitted columns as the models stand;
  Earth-air planets of a Sun-like star that differ from Earth in rotation alone, with the general repairs,
  though none has been run; a breathable world on a small body, with a column of its own and refitted
  calibrations; and Titan, present Mars and Venus, with radiation, condensation and cloud built anew."

### 17. MAJOR. The next-work opening describes its own paragraphs and orders them by the Moon alone

- **Location:** `next.tex:3–6`, with the position of `next.tex:57–61`.
- **Text:**
  > The first two steps below address the two sensitivities that moved the case's climate most, in order of
  > their size, and the third tests the reference both rest on; the rest are unordered, since their effects
  > on the climate remain unmeasured. Each names the question it settles, the comparison that settles it and
  > the result that would change the lunar design or the reach.
- **Rule:** Self-reference and reader management (G2); universal claims checked; generic verbs earn their
  place; the arc.
- **Why:** The second sentence tells the reader what each paragraph contains, and it fails as a universal:
  "Reports and the record" (L74–81) names no question or result, the sea items of L69–72 name needs, and the
  reach test names a comparison that leaves its question open (finding 18). "The reference both rest on"
  fits the longwave correction, fitted to the correlated-k reference, while the cloud step's target is CM1.
  "Address" stands where the steps name operations (refit, force, fit). The stated order of the first three
  steps holds by its own criterion, the size of the lunar sensitivities. The paper's contribution, though,
  is the reach of its repairs to other worlds, and the one step that tests that reach takes hours of
  ExoPlaSim (`introduction.tex:43–44`) and changes Table `tab:reach` directly; it stands seventh among steps
  declared unordered, while the conclusions end on it.
- **Rewrite:** "The longwave correction and PlaSim's cloud, the two Earth fits whose tests moved the case's
  climate most, come first, the larger first; a check of the reference to which the longwave correction and
  every calibration were fitted comes third; and a test of the general repairs off the Moon, a few hours of
  computing on which Table~\ref{tab:reach} depends, comes fourth. The later steps are unordered, since their
  effects on the climate are unmeasured." The paragraph "A test of the reach" then moves to fourth place.

### 18. MAJOR. The reach test names a comparison that leaves its question open

- **Location:** `next.tex:57–61`.
- **Text:**
  > The repairs have run on the Moon alone. Released and repaired ExoPlaSim on the Earth-air slow rotators of
  > Figure~\ref{fig:regimes}, with solar days of 16 and 64 days and the released radiation, which suits their
  > Earth-sized columns, would test whether the general repairs carry without refitting. A general repair
  > that needs retuning off the Moon would move to the calibrations, and the reach of Table~\ref{tab:reach}
  > would narrow with it.
- **Rule:** G5: each proposed study identifies the question it discriminates, the alternatives, the
  measured outputs and the result that would alter the design. Exact action.
- **Why:** The general repairs have no free coefficients, so "needs retuning" names no observable. Released
  against repaired ExoPlaSim measures the size of the three defects on those worlds, a useful result in its
  own right, and leaves the repairs' validity there untested. A discriminating form names its measures: the
  repaired runs' sunlight by longitude and convective cover against rain, set against the arithmetic each
  repair encodes, and the repaired climate set beside an independent model's runs at the same rotations.
  Way et al. (2018) ran ROCKE-3D at rotation periods of 16 and 64 days, counted as sidereal days, while the
  draft specifies solar days of 16 and 64, so the comparison calls for one definition. "The repairs have run"
  and "carry" give motion to repairs; the repaired models ran.
- **Rewrite:** "Away from Earth's values, the repaired models have run on the Moon alone. Released and
  repaired ExoPlaSim on Earth-air planets rotating once in 16 and 64 days, the periods of the ROCKE-3D runs
  of \textcite{way2018climates}, with the released radiation, which suits their Earth-sized columns, would
  measure the three defects' effect on worlds that other users study; the repaired runs' sunlight by
  longitude and convective cover against rain would test each general repair's arithmetic off the Moon; and
  setting the repaired climate beside ROCKE-3D's would separate the defects' effects from the two models'
  own physics. A general repair whose arithmetic fails off the Moon would be reclassed, and the reach of
  Table~\ref{tab:reach} would narrow with it."

### 19. MAJOR. The CM1 radiation test changes two inputs at once and offers the remedy as the test

- **Location:** `next.tex:42–46`.
- **Text:**
  > Extending its tables past 1,053.63~hPa, or replacing it with the in-house correlated-$k$ scheme, and
  > giving it the shield's spectrum would separate the table's edge from the other causes. If extended tables
  > remove most of the 4.5~W\,m$^{-2}$, the extrapolation was the cause and the near-ground range between the
  > models narrows with it; if they remove little, the cause lies in RRTMG's other approximations, and
  > replacing RRTMG becomes the step.
- **Rule:** G5: a discriminating study names its held-constant assumptions and the alternatives it
  separates.
- **Why:** Extending the tables and changing the spectrum in one run mixes their effects. Replacing RRTMG,
  offered in the first sentence as a route to the separation, removes every cause at once, and the second
  sentence then makes replacement the consequence of the test. The 4.5 W m⁻² excess cooling of the lowest
  1.8 km (claim V08) and the spectrum's difference of about 5 W m⁻² in the air's absorbed sunlight (Table
  `tab:inventory`, row "RRTMG Sun") are separate quantities with separate tests.
- **Rewrite:** "Extending RRTMG's tables past 1,053.63~hPa, with every other input held, would separate the
  table's edge from the other causes: if the extended tables remove most of the 4.5~W\,m$^{-2}$, the
  extrapolation was the cause and the near-ground range between the models narrows with it; if they remove
  little, the cause lies in RRTMG's other approximations, and replacing RRTMG with the in-house
  correlated-$k$ scheme becomes the step. Giving RRTMG the shield's spectrum, in a run of its own, would
  correct the difference of about 5~W\,m$^{-2}$ in the air's absorbed sunlight that the Sun's unfiltered
  spectrum brings."

### 20. MAJOR. "Electricity and seas" joins two subjects and lists the sea work as needs

- **Location:** `next.tex:63–72`.
- **Text:**
  > A leader model would replace the bound on ground strikes, now between none and a fifth of flashes, with
  > a rate. The seas need the air's density field in place of one value, swell decay over the long fetches
  > where swell carries a third to two thirds of the wave energy, a test of convergence in frequency for the
  > small seas that fail it, and wind input and breaking checked against theory at the lunar ratio of air to
  > water density; the last decides whether the similarity image of an Earth sea holds on the Moon at all.
- **Rule:** G1: one governing question per paragraph, and disconnected items in a list; the section's own
  standard of question, comparison and result (G5).
- **Why:** The sign of the lightning and the physics of the waves share a heading and nothing else. The
  sign step is complete: question, laboratory measurement, consequence for protection. The leader model has
  a result, a rate, with no consequence named. Three of the four sea items name needs with no question or
  result. "A test of convergence in frequency for the small seas that fail it" names a test the small
  seas already fail, the band-edge test, where the notes' remedy is a wider frequency band
  (`notes/waves.md`, improvement 6). "At all" intensifies.
- **Rewrite (two run-in heads):** "\textbf{The sign of the lunar lightning.} [L63–68 as drafted, with the
  verb of finding 27.] A leader model of the long crossing would replace the bound on ground strikes, now
  between none and a fifth of flashes, with a rate, and with it the number of strikes, each lowering a
  median 149~C, that the ground receives." "\textbf{The seas' Earth laws.} Wind input and breaking checked
  against theory at the lunar ratio of air to water density, and the spread between source-term packages,
  Komen's against Janssen's and ST6, would decide whether the similarity image of an Earth sea holds on the
  Moon; a wide spread would make the lunar wave heights a range. The air's density as a field and a wider
  frequency band for the small seas that fail the band-edge test are numerical needs, and swell decay over
  the long fetches, where swell carries a third to two thirds of the wave energy, a physical one that ST6
  includes."

### 21. MAJOR. "Reports and the record" written as prose: a status list on one verb

- **Location:** `next.tex:74–81`.
- **Text:**
  > The Sun clock is reported to ExoPlaSim's maintainers and awaits a reply. The convective-cover unit, with
  > its bias in synchronous runs, the orbit default and SWAN's uninitialised breaker parameter await reports
  > that would serve every user of those codes; CM1's thread race, placed by elimination in its own loops,
  > awaits locating and a report; and PlaSim's cold lowest level awaits a test against smoothed terrain that
  > would confirm or clear the spectral transform. CM1 would gain from one gravity parameter honoured by
  > every scheme. The record itself needs …
- **Rule:** A genuine catalogue goes in a list (G1); repeated subject–verb frames (G3); exact action;
  generic importance claims (G4).
- **Why:** Four items share one frame ("awaits"), and the defects are the ones that await, while the agents
  are the author and the upstream maintainers. "Would serve every user of those codes" claims an effect on
  all users, where each defect biases runs under its stated conditions. The paragraph names no question or
  result, against the standard the section's opening sets. "The CM1 cases set up before the Sun and the
  starting soundings were corrected" leaves the reader to work out which Sun, the GCM's Sun clock reaching
  CM1 through the forcing.
- **Rewrite:** "The author reported the Sun clock to ExoPlaSim's maintainers as issue~\#69 on 29 September
  2026; it had no reply on 17 October. Still to be done:" followed by a list:
  - reports to ExoPlaSim's maintainers of the convective-cover unit, with its bias in synchronous runs, and
    of the orbit default, and to SWAN's of the uninitialised breaker parameter;
  - locating CM1's thread race, placed by elimination in CM1's own loops, and reporting it, with a proposal
    for one gravity parameter read by every scheme;
  - a test of PlaSim's cold lowest level against smoothed terrain, which would confirm or clear the spectral
    transform;
  - for the record: the twilight pair's control rerun on one build; runtime identity runs for the Sun
    clock, the water scaling and patches 07–09 at their off settings; and new forcing for the CM1 cases set
    up before the GCM's Sun clock and CM1's starting soundings were corrected.

### 22. MAJOR. The AI-assistance disclosure names one assistant where Terluna's commit messages name more

- **Location:** `availability.tex:15–21`.
- **Text:**
  > The adaptations, analyses and this manuscript were developed with AI assistance. Claude Opus~5.5
  > (Anthropic), working under the author's direction, wrote and ran most of the code, patches and analyses
  > in Terluna, where 374 of the 487 commits to 186b294 name it as co-author, …
- **Rule:** `AGENTS.md`, "The paper": Terluna enters "as provenance only", and the history of AI
  assistance is part of that provenance; final releases carry an accurate AI-assistance disclosure (charter
  section 3).
- **Why:** The count reproduces: 374 of the 487 commits to 186b294 contain a Claude Opus 5.5 co-author line
  (329 with "(1M context)", 45 without), and no other co-author line appears. Terluna's commit messages
  record a second assistant. Commit 05810ce (8 October 2026) keeps "Codex's review of the five research
  states and its plan for joining them", which covered the solar-shield and atmospheric-electricity
  branches, from which this paper takes the shield's spectrum and the electrified runs, with an audit script
  and a merge order the author accepted; b198bd1 rewrites "Codex-written" notes, 6745ee6 moves "Codex's
  calendar", and eeaecbc rewrites "Codex's uncommitted draft". Commit 5d64033 names the July 2026 bundle's
  archives by hash "in place of ChatGPT Library identifiers", fdd173c imports the shield lineage as
  "conversation-recovered reconstructions", and the charter's controls, which the paper's writing rules
  consolidate, cite Library file identifiers of the same form. The disclosure states Claude's part
  accurately and leaves the others unstated.
- **Rewrite (after the subagents sentence):** "In Terluna, OpenAI's Codex reviewed the solar-shield,
  atmospheric-electricity and three other research branches on 8 October 2026 and planned their merge, an
  order the author accepted, and wrote notes and a calendar outside this paper's subject; [the July and
  September 2026 packages from which the shield's lineage was reconstructed, and the editorial controls
  behind the paper's writing rules, came from conversations with ChatGPT]." The bracketed clause states what
  Terluna's records indicate; the author confirms it.

### 23. MAJOR. In the review history the author's reading is recast, the agent of the rewrite goes unnamed, and rounds under way are recorded as complete

- **Location:** `availability.tex:31–36`.
- **Text:**
  > The author then read the draft and rejected its framing and much of its prose, and that reading served
  > as the cadence review of the first draft. This second draft answers both: it reframes the paper, rewrites
  > its prose to the rules recorded in the repository's instructions, and acts on the challenge. Its
  > editorial rounds by fresh reviewer agents, the referees' reports, the challenge and every disposition are
  > recorded in the repository's review folder.
- **Rule:** `AGENTS.md`: the actual review history, "in which each of the author's own readings is recorded
  as the author's review". Charter G3: a silent review is recorded as silent, and an absent audible review
  stays pending. E4: nothing prefilled. Exact action.
- **Why:** Crediting the reading as "the cadence review" files it under the pass that the charter ties to
  reading aloud and leaves open whether the author read aloud; under the rule it is recorded as the author's review.
  A draft performs none of the four actions given to it (answers, reframes, rewrites, acts), and the agent,
  Claude Opus 5.5 under the author's direction, goes unnamed in the one paragraph that says who did what. The
  second draft's editorial rounds are under way, this record belonging to the first, so "every disposition
  [is] recorded" states a record still being made as complete. The counts in L29–31 (94 statements; 5, 11
  and 21 findings) come from review records outside this review's reading and from no register entry, so
  this review leaves them unverified.
- **Rewrite:** "The author then read the draft, [silently or aloud], as the author's review, and rejected its
  framing and much of its prose. Claude Opus~5.5, under the author's direction, wrote the second draft in
  answer to that review and to the challenge: it reframed the paper, rewrote its prose to the rules in the
  repository's instructions and acted on the challenge's findings. Fresh reviewer agents read the second
  draft in editorial rounds, and each round's findings and dispositions, with the referees' reports and the
  challenge, are recorded in the repository's review folder as the round closes. Review by people other than
  the author, or by a journal, is still to come."

### 24. MAJOR. "Every number in the prose carries a claim"

- **Location:** `availability.tex:21–23`.
- **Text:**
  > Every number in the prose carries a claim in the register, traced to a file in one of the two
  > repositories, a run on the research drive, a web record or a stated calculation.
- **Rule:** Universal claims checked against what was examined; report actual checks.
- **Why:** `conclusions.tex` contains no claim marker; `next.tex:3–46` and `57–61` contain none; the review
  counts of `availability.tex:29–31` appear in no register entry. `paper/tools/check.py` confirms that every
  marker resolves and every listed source exists, and its docstring calls these completeness checks; it
  examines no unmarked number. Most unmarked numbers repeat registered values (G02, G05, G14, H20, R10,
  V07, V08), so the practice comes close, and the sentence states more than the check covers. In "carries", a
  number is also given an action.
- **Rewrite:** "Each claim marker in the source names a register entry that traces the claim to a file in
  one of the two repositories, a run on the research drive, a web record or a stated calculation, and the
  paper's check script confirms that every marker resolves and every listed source exists. Numbers repeated
  in the conclusions and next work refer to the same entries without markers, and the review counts below
  come from the review records."

### 25. MINOR. Reach, third paragraph: a figurative topic sentence and generic verbs

- **Location:** `reach.tex:29–38`.
- **Text:**
  > Against the ratios of Figure~\ref{fig:regimes}, each Earth value fails along its own direction.
  > … while PlaSim's broadband fits, made near Earth's column, meet columns ten times Earth's on Titan, …
  > … Released CM1 fails at any gravity but Earth's, under any day but Earth's 24 hours, and in any air whose
  > carbon dioxide differs from Earth's value for the calendar year; SWAN, in the configuration used, loses
  > gravity similarity through one constant.
- **Rule:** Exact action; universal "each"; generic verbs; technical meaning.
- **Why:** The topic sentence states its point through a figure, "fails along its own direction", and "each"
  claims more than the paragraph supports: Slingo's fit, two sentences later, lies along no ratio of the figure. Fits "meet" columns.
  "Released CM1 fails" names an outcome where the operation is known, a code that computes with 9.81,
  Earth's 24-hour day and the calendar's gases, and the prose omits the trace gases and ozone that Table
  `tab:reach` lists. "One constant" leaves unnamed the wind-input knee fixed at 1 Hz.
- **Rewrite:** "The Earth values that depend on a ratio of Figure~\ref{fig:regimes} err as a world departs
  from Earth along it. … and PlaSim's broadband fits, made near Earth's column, would be applied to columns
  ten times Earth's on Titan, a hundred times on Venus and seven times on the Moon. … Released CM1 computes
  with Earth's gravity of 9.81, Earth's 24-hour day and the calendar year's carbon dioxide, trace gases and
  ozone; SWAN, in the configuration used, loses gravity similarity through its wind-input knee, fixed at
  1~Hz."

### 26. MINOR. Reach, last paragraph: an unmeasured "most" and a landing on a table pointer

- **Location:** `reach.tex:71–76`.
- **Text:** "Four limits bound most of the reach of the adapted models: … Table~\ref{tab:reach} adds the
  narrower ones."
- **Rule:** Quantity words checked against what was examined; landings complete the paragraph's movement
  (G3); exact action.
- **Why:** "Most" quantifies nothing measured, and "limits bound the reach" restates itself. The section's
  last prose sentence points to the table, so the section lands on reader management after the four limits,
  the sentence that completes its movement.
- **Rewrite:** "The adapted models hold within four limits: compositions of nitrogen, oxygen, argon, water and
  modest carbon dioxide; surface pressures within RRTMG's tables, already exceeded over the lowest 7.5~km at
  1.2~atm; scale heights up to a few hundredths of the radius, the Moon's, where thin-shell,
  constant-gravity dynamics already omit the 5--15\% fall of gravity across the air; and empirical laws of
  cloud, sea and charge used near the Earth conditions they were fitted on (narrower limits in
  Table~\ref{tab:reach})."

### 27. MINOR. Verbs of rest and carriage where the operation is known

- **Rule:** Exact action: positional verbs given to abstractions (`AGENTS.md` names "sits" and "stands
  behind") are empty actions; where the evidence names an operation (fitted to, changes with, used), the
  prose names it.

| Location | Text | Rewrite |
|---|---|---|
| `next.tex:8` | "The largest single sensitivity rests on a correction fitted at 295~K" | "The largest single sensitivity comes from a correction fitted at 295~K" |
| `next.tex:11–12` | "a correction carrying humidity as well as temperature, and then a reduced correlated-$k$ scheme … would remove the fit altogether" | "a correction with humidity among its predictors would extend the fit, and a reduced correlated-$k$ scheme built from the reference model's own spectroscopy in place of Sasamori's would replace it" (the draft also groups the humidity correction, still a fit, with the scheme that removes the fit) |
| `next.tex:26` | "Every calibration rests on the line-by-line model" | "Every calibration was fitted to the line-by-line model" |
| `next.tex:63` | "The sign of the lunar lightning rests on laboratory charging laws that disagree in the lunar storms' little cloud water." | "The sign of the lunar lightning changes with the laboratory charging law chosen, and the laws disagree in the lunar storms' little cloud water." |
| `availability.tex:38` | "The work rests on models and data that their developers make freely available" | "The work used models and data that their developers make freely available" |

### 28. MINOR. The tall air's dynamics: CM1's geometry and an undefined threshold

- **Location:** `next.tex:33–39`.
- **Text:**
  > Both dynamical cores hold gravity constant in a thin shell, where the lunar air loses 5\% of its gravity
  > by its mass-mean height … A change in the heat carried poleward larger than the spread between the present
  > models would make a deep core a requirement for the design case.
- **Rule:** Technical meaning; G5: the result that would change the design is measurable.
- **Why:** CM1 runs a flat slab and PlaSim a thin shell (`assumptions.tex:59–61`). Air "loses" gravity,
  where gravity falls with height. Of the present models the GCM alone computes a global poleward transport,
  so "the spread between the present models" names a quantity the runs lack, and the deciding result stays
  undefined.
- **Rewrite:** "Both dynamical cores hold gravity constant, PlaSim's in a thin shell and CM1's in a flat
  slab, while lunar gravity falls 5\% by the air's mass-mean height and the air in spherical shells holds
  11.5\% more over each square metre of ground than $p_s/g_s$. … A change in the GCM's poleward heat
  transport larger than [a stated measure, such as the design case's spread from year to year] would make a
  deep core a requirement for the design case."

### 29. MINOR. "A fifth" compares the box with a GCM state other than its forcing

- **Location:** `next.tex:54–55`.
- **Text:** "if CM1's rain stays near a fifth of the GCM's"
- **Rule:** Technical meaning survives editing.
- **Why:** The box was forced from the pre-correction run, whose GCM rained 129 mm per lunar day against the
  box's 34, about a quarter; a fifth sets the box beside the Sun-and-tilt run's 180 mm
  (`results.tex:91–93`).
- **Rewrite:** "if CM1's rain stays near a quarter of the forcing GCM's".

### 30. MINOR. The independent GCM is placed inside the cloud step

- **Location:** `next.tex:20–24`.
- **Text:**
  > An independent GCM on the same scenario, ROCKE-3D or the LMD generic model …, would show which of the two
  > present models departs near the ground: air as warm as CM1's would make PlaSim's boundary layer and
  > longwave the next repairs, and air as cool as PlaSim's would point to the slices' forcing and CM1's
  > microphysics.
- **Rule:** G1: one question per paragraph; swap test.
- **Why:** The independent GCM settles the near-ground gap, a question apart from fitting PlaSim's cloud;
  inside the cloud paragraph it reads as an added item and passes the swap test. It is also the test the
  introduction names last, agreement among independent models, and in the rewrite it becomes a step of
  its own.
- **Rewrite:** a run-in head after the reference check: "\textbf{An independent GCM.} ROCKE-3D or the LMD
  generic model on the same scenario \autocite{way2017resolving,wordsworth2011gliese} would show which of
  the two present models departs near the ground: an independent GCM's air as warm as CM1's would make
  PlaSim's boundary layer and longwave the next repairs, and air as cool as PlaSim's would place the error
  in the slices' forcing and CM1's microphysics."

### 31. MINOR. Named codes and planetary periods without citations

- **Location:** `next.tex:28` (LBLRTM; "a DISORT-based solver"); `reach.tex:25–26` (TRAPPIST-1e's 6.1-day
  rotation; Proxima Centauri b's 11.2 days).
- **Rule:** Claims stay within their evidence; names that a reader outside the project can follow.
- **Why:** At 4d03a81 and a06a4ab `references.bib` held no entry for LBLRTM, DISORT or TRAPPIST-1e. During
  this review a parallel session added `clough2005atmospheric` and `stamnes1988numerically` to the working
  tree's bibliography, uncommitted, and `next.tex` cites neither; TRAPPIST-1e still has no entry, and
  Proxima b has candidate sources in the bibliography (`boutle2017exploring`, `delgenio2019habitable`). A reader traces a
  named code or a planet's period through a citation, and under G6 each is admitted as a source.
- **Rewrite:** "Running the design column through LBLRTM \autocite{clough2005atmospheric} for the longwave
  and a solver built on DISORT \autocite{stamnes1988numerically} for the sunlight, …", once those entries
  are committed and admitted, and an orbital solution cited for each planet.

### 32. MINOR. Naming and evidence state in the conclusions

- **Location:** `conclusions.tex:6`, `18`, `19`.
- **Text:** "a rain unit exact at a one-day model day"; "the freezing level stands five to six times higher
  than Earth's"; "the lightning is rarer and larger than Earth's".
- **Rule:** Names a reader can follow; technical meaning and evidence state.
- **Why:** The unit is "the convective-cover unit" everywhere else; the freezing level's comparison in the
  results is with Earth's tropics; the lightning comes from one box. With findings 13 and 15 taken, these
  sentences leave the conclusions; if they stay, the qualifiers return.
- **Rewrite:** "a convective-cover unit exact at a one-day model day"; "five to six times higher than in
  Earth's tropics"; "in the one electrified box, the lightning is rarer and larger than Earth's".

### 33. MINOR. The appendix's opening paragraph and the caption of the changes table

- **Location:** `appendix.tex:3–5`; `appendix.tex:27–32`.
- **Text:**
  > Table~\ref{tab:config} gives each model's configuration in the lunar runs, Table~\ref{tab:repairs}
  > every change with its switch and lunar setting, and Table~\ref{tab:verification} the verification record
  > by kind of check, condensed from the code repository's record.

  Caption: "… rows marked unconditional act in every build that has them. Class: general; … a coupling
  method."
- **Rule:** G2 (reader management; generic verbs); universal claims checked; exact action.
- **Why:** The opening is a roadmap of three tables. "Every change" claims more than the table holds: the flash-reach
  logging change, classed "General (logging)" in Table `tab:inventory` (`assumptions.tex:191`), has no row
  in Table `tab:repairs`. In the caption, rows act where the changes act. The gas-band row's class,
  "Calibration (structure general)", has no gloss in the caption's list of classes.
- **Rewrite:** "The lunar runs' configurations, the changes with their switches and lunar settings, and the
  verification record by kind of check, condensed from the code repository's record, are in
  Tables~\ref{tab:config}, \ref{tab:repairs} and \ref{tab:verification}." Caption: "… changes marked
  unconditional act in every build that has them. Class: general; a general method with a lunar table; a
  calibration to the lunar design case, or a calibration of general structure whose coefficients are lunar
  fits; …". Either a row for the flash-reach logging or "the changes" in the opening.

## Combined rewrite of the conclusions

Findings 1, 2, 10 and 13–16 touch every sentence of `conclusions.tex`. Assembled, in the paper's voice:

> Each of the three upstream defects found on the Moon produces little or no error at Earth's values and an
> error that grows as a world departs from Earth in one property: the Sun clock's skip with slower rotation,
> to 33\textdegree\ a model day beyond a 20-day rotation; the convective-cover unit's bias with the
> logarithm of the model day; and the orbit default's error with the distance of a world's tilt from
> Earth's. In the lunar runs, far along all four ratios at once, the three errors grew large enough to find,
> and the same arithmetic biases other users' runs: the Sun clock in non-synchronous runs on ExoPlaSim's
> default solar geometry, the convective-cover unit in any run whose model day differs from one Earth day,
> synchronous runs included, and the orbit default in any run that sets a tilt without fixing the orbit.
>
> The largest changes to the case's climate came from parts fitted to one world's columns, which are
> refitted for each other world: the first calibration moved the global mean by at least 20~K, PlaSim's
> Earth-tuned cloud settings by up to about 6~K, and the longwave correction, run with the ice optics in a
> state outside its fit, by about 11.5~K, of which the ice optics' share is unmeasured. Measured one at a
> time, the general repairs, which apply unchanged elsewhere, moved it by a few kelvin at most, while the
> Sun clock and the Moon's own tilt, applied with the split of sunlight recalibrated, cut the rain by nearly
> a quarter and raised the share of land under half a millimetre a day from a tenth to two fifths. The two
> atmospheric models disagree most where each runs on Earth fits of its own: with the GCM's transport
> imposed, CM1's lowest 1.8~km at 45\textdegree\,N stays 3.7~K warmer than the GCM's, and a box forced from
> the GCM brings a quarter of the forcing GCM's rain to the ground, the GCM's rain set by its convection
> scheme and CM1's by Earth's drop limits; in the one electrified box, the sign of the lightning changes with
> the laboratory charging law chosen.
>
> The worlds open to the adapted models are ordered by how far their columns lie from a fitted one: the
> Moon near its fitted columns as the models stand; Earth-air planets of a Sun-like star that differ from
> Earth in rotation alone, with the general repairs, though none has been run; a breathable world on a small
> body, with a column of its own and refitted calibrations; and Titan, present Mars and Venus, with
> radiation, condensation and cloud built anew. Replacing the fitted parts that moved the Moon most would
> narrow its uncertainty, and where the replacement is computed from physics it would extend the models as
> well. A reduced correlated-$k$ scheme built from the reference's spectroscopy in place of Sasamori's and
> Lacis and Hansen's fits would hold on any column whose gases and pressures that spectroscopy covers;
> PlaSim's cloud fitted to cloud-resolving runs would remain a calibration, refitted for each other world
> with cloud-resolving runs of that world; and a check of the reference against LBLRTM and a DISORT-based
> solver would test the spectroscopy to which every calibration was fitted. Runs of the repaired ExoPlaSim
> on Earth-air slow rotators would show whether the parts classed as general hold off the Moon.

## Paragraphs examined and found sound

Sound throughout:

- `appendix.tex:8`, caption of Table `tab:config`.
- `appendix.tex:92`, caption of Table `tab:verification`; "what each leaves open" names the untested
  remainder of each check plainly.
- `reach.tex:90–97`, the rows of Table `tab:reach` for the solar day, tilt and orbit, tall air, heavy air,
  composition, cold cloud, storm electricity and seas: each cell matches the notes and Table `tab:inventory`.

Sound in argument and evidence, with the local note named:

- `reach.tex:18–27`, the defects in other users' runs: the arithmetic matches claims W02 and W06 and the
  notes (the skip of 1/(N−1) of a turn; 1°, 2°, 10° and 33°; N rounded to a multiple of 12 and floored at
  12; +0.23 and +0.31 for TRAPPIST-1e and Proxima b; the orbit default). Its one defect is the dropped
  condition of finding 10.
- `reach.tex:59–62`, Mars held at 1 bar: the ratios match `data/worlds.json` (H/R 0.00655, five times
  Earth's; column 2.6 times; gravity 0.38). The wording of `reach.tex:62–66` is in finding 8.
- `reach.tex:68–70`, Titan, present Mars and Venus: composition, temperature and pressure match
  `data/worlds.json`; one clause is in finding 8.
- `next.tex:8–14`, the longwave at the settled state: question, procedure and the result that changes the
  dimming, in order; verbs in finding 27.
- `next.tex:26–31`, the reference against an independent code: the section's model step, with its question,
  a comparison on identical layers and a threshold set at the calibration residuals; one verb in finding 27.
- `next.tex:48–53`, microphysics at lunar gravity: the facts match claim N03 and `notes/cm1.md`; L54–55 are
  in finding 29.
- `next.tex:63–68`, the sign of the lightning: question, laboratory conditions (claim N01) and the
  consequence for protection; one verb in finding 27.
- `availability.tex:3–13`, code and data: the pins and licences match the model READMEs (GPL version 3 for
  ExoPlaSim; version 3 or later for SWAN and SWASH; CM1's MIT-style licence; the WRF public-domain notice
  for WRF-ELEC); the missing address is in finding 5.
- `availability.tex:15–21`, as far as it goes: the commit count reproduces; the omission is finding 22.
- `availability.tex:38–40`, acknowledgements; one verb in finding 27.

## Gate notes for this scope

These notes state findings only, with no verdict.

- **G1, argument and reorderability.** Inventories stand in prose: the class list of `reach.tex:6–13`
  (finding 7), the sea items and the status list of `next.tex:69–81` (findings 20, 21), and the defect
  recital and the storm-and-sea sentence of the conclusions (findings 13, 15). The groups of worlds in
  `reach.tex:46–76` mix what a world needs with how far the runs tested it (finding 9). The next-work order
  follows the Moon's sensitivities and leaves the reach test seventh (finding 17), and the independent GCM
  passes the swap test inside the cloud step (finding 30).
- **G2, audience and explanatory economy.** Reader management: `next.tex:5–6` describes its own paragraphs
  (finding 17); `reach.tex:41–42`, `reach.tex:75–76` and `appendix.tex:3–5` point to tables where a landing
  belongs (findings 8, 26, 33). The landing of `reach.tex:13–16` restates its paragraph's second sentence
  (finding 7). Names an outside reader stumbles on: "SWAN's knee" and "its ledger" beside "the ledger"
  (finding 7), "the release register" (finding 5), "a rain unit" (finding 32); LBLRTM and DISORT appear
  without citations (finding 31).
- **G3, inheritance, syntax and cadence.** The reach section opens on a play of words (finding 6), and its
  second paragraph opens with nothing inherited (finding 10); `next.tex:74–81` repeats one subject–verb frame
  four times (finding 21); `reach.tex:29–38` runs a chain of model-by-model declaratives (finding 25); the
  section's last prose sentence lands on a table pointer (finding 26). The cadence pass behind this record
  was a silent reading on screen; a read-aloud of the closing sections remains pending.
- **G4, affirmative stance and exact action.** "Not" and "rather than" are absent from the scope; the
  remaining negations ("little or no error", "without fixing the orbit", "none has been run", "no
  independent code has checked", "no competing interests") are required by the propositions' meaning. Empty
  actions: results and classes that sort, parts that travel, worlds that take and remake repairs,
  adaptations that reach (findings 6, 7, 8, 14); defects that act and await (findings 10, 21); a draft that
  answers, reframes and rewrites (finding 23); numbers that carry claims (finding 24); verbs of rest
  (finding 27). Generic importance: "every user of those codes" (finding 21).
- **G5, technical meaning and discriminating tests.** The effects of a calibration and of a general repair
  are credited to the wrong class (finding 1); the last claim of the conclusions contradicts the paper's
  class definitions (finding 2); a proposed forcing has already run (finding 3); a per-model reach goes past
  its runs (finding 4); a defect's condition and the starlight property drop out (findings 10, 11); a field
  is characterised from two studies (finding 12); proposed tests change two inputs at once, name no
  observable, or leave their deciding threshold undefined (findings 18, 19, 28); a ratio is taken against a
  state other than the forcing (finding 29); availability and the claim register are stated beyond the
  record (findings 5, 24).

## Counts

BLOCKING 5 (findings 1–5); MAJOR 19 (findings 6–24); MINOR 9 (findings 25–33).
