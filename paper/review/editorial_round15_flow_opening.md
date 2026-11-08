# Editorial round 15: flow in the opening sections

## Record

| Field | Entry |
|---|---|
| Reviewer | A fresh Claude subagent (Claude Opus 5.5), with no sight of any earlier review of the paper |
| Date | 2026-10-18 |
| Snapshot | Commit 64d04e0, clean working tree; files read in place. 64d04e0 was later reworded as 2800b68, the same tree, under AGENTS.md's rule on quoting the author in commit messages |
| Check | Flow only, under the author's direction of 18 October 2026 (below) |
| Scope | The prose of the four files below; table bodies skipped |

Files in scope:

| File | Lines | sha256 |
|---|---|---|
| `paper/sections/abstract.tex` | 31 | `bf158f0f058e6d544bb486f1738d5795d58ae01da43b3514d470023d4bebb171` |
| `paper/sections/introduction.tex` | 92 | `7c9b41e4348619b7fb0002a44de746e5a3b822b3e13445c8caece3ce03826cfd` |
| `paper/sections/worlds.tex` | 103 | `97c0952df1a968079e8033e10320c1c7b1b383632ac11c310f13a2f502de8623` |
| `paper/sections/assumptions.tex` | 216 | `77bc704fe58d964ff2567a39ffbdf6e2af9b0cc422bfb88e04d25e949b877107` |

Read for the check:

- `AGENTS.md` (`d6edb79a6635865f77cd9dcbe043c526e42289f333a6acc688355e2697bfa909`), section "Writing" in full, above
  all "Sentences carry their dependencies" and "Inheritance and order".
- The four Terluna sources that section names, in full: `STYLE_NOTES.md`
  (`659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46`), `Jewish_Papers_Updated_Style_Notes.md`
  (`18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab`), `Agent_Working_State_Editorial_Gates.md`
  (`553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464`) and
  `Open_Moon_Editorial_Charter_control-01.md` (`aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0`).
- `paper/main.tex` (`09ddc294b8a441ff534e9533760d93660d4fac677470d16240b50d4ab2b7b04a`), for the order of sections.
- The opening of `paper/sections/repairs.tex` (`c846dbbf4dbaf39ae194d7bb93a26204aaa1b12f4b24e7aa1accdd948b281102`),
  for the transition out of the part.
- The opening of `paper/sections/next.tex` (`32054594479807c5764742cc1c82a26179960330bd750eb82e72eb340c4dec20`), to
  confirm the one relation that F03's sample rewrite writes in.
- The first 40 lines of `paper/review/README.md`, for the conventions of a record. They summarise earlier rounds by
  count only; no earlier round's record was opened.
- The author's standing notes on writing, kept for these sessions outside the repository.

Method: each file was read once through in the order of `main.tex`, then again paragraph by paragraph. The second
reading traced what each sentence inherits, at every sentence boundary and at the clause boundaries inside long
sentences, and applied the swap test. Both readings were silent; no read-aloud pass was made. A script compared each
sample rewrite with its original for numbers, citations, cross-references, inline mathematics and `\claim{}` markers.
All are kept, and F22 records the one change of order. No lint was run and nothing was built. This record is the only
file changed.

Direction applied, in the author's words (18 October 2026):

- "Remember I hate paratactic style in the academic papers I craft and I generally hate when paragraphs in them are
  just a bullet point set of information chained together pretending to be paragraphs."
- "A stock signpost is a stock signpost. "Moreover" and similar used appropriately to move from one thought to the
  next and keep flow is fine." The author also asked that writing flow and transition smoothly.
- On a drafted pair of sentences whose transitions had been cut, the author objected that the cuts left a bullet
  point list of sentences strung together. And: "The second issue does not directly stem from
  the first issue, does it? No. So we cannot just tack on that next sentence as if it does."

Kinds of failure: (1) paratactic run, equal-weight sentences with their relation unwritten; (2) a paragraph of
bullet points chained together; (3) an unmarked turn, a new point set as if it followed, or a contrast or concession
with no word to mark it; (4) a missing or abrupt transition between paragraphs or at a section opening; (5)
over-compression, connectives stripped or loosely related clauses chained by semicolons.

Severity: MAJOR, a paragraph or a run of three or more sentences that reads as a list; MINOR, one unmarked relation.

Each sample rewrite keeps every claim, number, condition, citation and `\claim{}` marker of its passage and is
offered to the author as one way to write the relations in; the author's own wording decides.

## Findings

### abstract.tex

**F01. abstract.tex:4–8. Kind 3. MINOR.** "Their gravity, size, day or starlight can differ … too weak to hold it
naturally."
Repair: the concession (the worlds differ, yet a model that keeps an Earth value still completes plausibly) is left
to "while", and "depart further" in the next sentence then refers back past that clause; write "Even though their
gravity, size, day or starlight can differ substantially from Earth's, a model that keeps a value set for Earth can
complete with a plausible result" and open the next sentence "Moreover, a constructed world can depart further".

**F02. abstract.tex:13–16. Kind 3. MINOR.** "and by ExoPlaSim's own arithmetic three of them, with little or no
error at Earth's values, bias its runs …"
Repair: the concession (little or no error at Earth's values, yet a bias in runs of slow rotators) goes only to
"with"; mark it "three of them, though they produce little or no error at Earth's values, bias its runs that meet
their conditions".

**F03. abstract.tex:19–30. Kinds 1 and 3. MAJOR.** "Identity, reproduction, arithmetic … a fit still to be made on
the test world."

What fails: four sentences in a row each open on a new subject, and every joint between them is left for the reader
to supply. The step from the repairs of the sentence before to the checks of the code is a sequence; the turn from
checks against known answers to effects on the test world's climate is a contrast; the step from the sizes of those
effects to the two fits taken up next is a consequence, which Next steps states ("the two Earth fits whose tests
moved its climate most, are the first calibrations to revisit"); and the plan for cloud adds a second plan to the
first. The last two sentences can trade places without loss.

Sample rewrite:

```latex
With the repairs in place, identity, reproduction, arithmetic, gravity-similarity and Earth-benchmark checks test
the code: patched, SWAN reproduces a sixfold gravity scaling of an Earth sea to 0.3\% in wave height, where the
released code misses it by up to 5.4\%.\claim{V04} On the test world, however, whose climate is unobserved, the two
general repairs measured singly moved the global-mean surface temperature by 1.6--2.5~K, while the first
calibration of the radiation's Earth fits moved it by at least 20~K and the cloud's Earth-tuned settings, varied in
tests, by up to about 6~K.\claim{G01}\claim{G14}\claim{G05} Because the radiation's fits and the cloud's settings
moved it most, they are the first to revisit. A radiation scheme built from the in-house model's line-by-line
spectroscopy would replace the largest of these fits for nitrogen--oxygen air with water and modest carbon dioxide,
under the starlight it would be built for and over the pressures and temperatures where that spectroscopy agrees
with an independent code, a comparison planned on one column of the test world. Water cloud, in turn, would be
calibrated for each world against cloud-resolving runs whose own microphysics is fitted on Earth, a fit still to be
made on the test world.
```

The rewrite adds one hinge sentence, whose relation comes from Next steps. It keeps "whose climate is unobserved" as
written, because the check keeps every claim; the wording of that clause lies outside this check.

### introduction.tex

**F04. introduction.tex:13–17. Kind 3. MINOR.** "By the account of THOR's developers, most general circulation model
(GCM) studies … PlaSim"
Repair: an addition left unmarked, as the paragraph moves from what the studies varied to the codes such studies run;
tie the codes to the studies, e.g. "For such work, by the account of THOR's developers, most general circulation
model (GCM) studies of exoplanet atmospheres adapt codes …".

**F05. introduction.tex:21–22. Kind 3. MINOR.** "Constructed worlds reach further from Earth. The bodies of the Solar
System that keep atmospheres …"
Repair: the second sentence gives the ground for the first (natural worlds keep air only on one side of an escape
divide), and the relation is unwritten; join them with "for" ("Constructed worlds reach further from Earth, for the
bodies of the Solar System that keep atmospheres are those …").

**F06. introduction.tex:22–25. Kind 5. MINOR.** "and the known exoplanets crowd against the same divide extended:
the Moon held … on a body smaller than Mars."
Repair: the examples after the colon, the Moon and Titan, illustrate the Solar System clause, yet the exoplanet
clause comes between; set the examples straight after "the light they receive" and close on the exoplanets as an
extension ("…, and beyond the Solar System the known exoplanets crowd against the same divide extended").

**F07. introduction.tex:25–29. Kinds 1 and 3. MINOR.** "An engineered world can hold … \textcite{mckay1991making}
asked how Mars could be made habitable, and the breathable Moon … its upper air."
Repair: the example relation is unmarked, and "and" sets McKay's 1991 question level with the present design; mark
the design as an instance of the engineered world just named, e.g. "\textcite{mckay1991making} asked how Mars could
be made habitable; the breathable Moon designed in the Terluna project \autocite{goldman2026terluna}, one such world,
is to keep 1.2~atm …".

**F08. introduction.tex:31–34. Kind 4. MINOR.** "Such worlds combine nitrogen--oxygen air … / Developers who ported
Earth models to other planets found values fixed for Earth in the code."
Repair: the paragraph returns from constructed worlds to the ported codes of the second paragraph with no bridge;
mark the return, e.g. "Such worlds would be modelled with codes like those named above, and developers who ported
Earth models to other planets found values fixed for Earth in the code."

**F09. introduction.tex:42–52. Kinds 1, 3 and 5. MAJOR.** "Each team removed the Earth values … calibrations for
each world."

What fails: after the developers' evidence, three sentences in a row open on a frame ("On a terracompatible world",
"In an ensemble linking …", "Developing such an ensemble …") and set their points side by side. The contrast in the
first sentence ("removed the Earth values that mattered …, and others could stay") goes to "and"; the consequence
for terracompatible worlds is unwritten; a semicolon joins the retained value to the reason it escapes notice; the
step to the ensemble, an addition (the same values also enter the forcing exchanged between models), has no marker;
and the requirement that closes the paragraph reads as a fresh statement, though it follows from the two sentences
before it.

Sample rewrite:

```latex
Each team removed the Earth values that mattered for the worlds it set out to model, but others could stay:
ROCKE-3D's developers report that the changes their first release made from the Earth configuration went
unstudied \autocite{tsigaridis2025rocke3d}, and THOR's developers, who wrote their model for other planets from
the start, describe planet-specific tunings as often built into adapted codes and hard to find
\autocite{deitrick2020thor}. On a terracompatible world, then, a run can compute the familiar phases of water in
nitrogen--oxygen air while retaining a constant set for Earth's gravity, or a formula that counts rain per Earth
day, and because its output is plausible, the retained value can be hard to detect. In an ensemble linking global
climate to resolved storms and coastal waves, moreover, those values affect both the individual calculations and
the forcing exchanged between them, so developing such an ensemble for terracompatible exoplanets and constructed
worlds requires identifying which changes follow from general laws and which need calculations or calibrations
for each world.
```

**F10. introduction.tex:51–54. Kind 4. MINOR.** "… which need calculations or calibrations for each world. / The
adaptations and couplings described here began with the breathable Moon as their test world."
Repair: the present work enters as a first step toward the ensemble just required, with no bridge; mark it, e.g.
"Toward such an ensemble, the adaptations and couplings described here began with …" (the abstract makes this move
with "As a start toward that ensemble").

**F11. introduction.tex:57–60. Kind 5. MINOR.** "A run of a natural planet … that ratio alone; on the test world the
values of all four err together …"
Repair: the contrast between a natural planet's single departure and the test world's four goes to a semicolon; mark
it "whereas on the test world the values of all four err together".

**F12. introduction.tex:71–76. Kind 3. MINOR.** "The GCM's surface stress drives SWAN … / The radiation of both
atmospheric models was tested against an in-house … model"
Repair: the reference model takes no part in the forcing chain just traced, and the sentence that brings it in opens
with no marker of addition; e.g. "Alongside these couplings, the radiation of both atmospheric models was tested
against …".

**F13. introduction.tex:78–92. Kinds 2, 3 and 4. MAJOR.** "An Earth value is a value or form … the Earth values
that remain."

What fails: the paragraph opens on a definition with no bridge from the radiation reference before it, then sets
eight statements in a row, each on a new subject: two definitions, the four forms, the five defects, the three
classes, their definitions, the remaining changes, the link between class and form, and the evidence state. Inside
it, the concession about the three defects (little or no error at Earth's values, yet a bias on slow rotators) goes
to "and"; the turn from what was found to how it was repaired is unmarked; the fits' effect on the climate is joined
by "and" to the class–form link as if it followed from it, and the two clauses of that sentence can trade places
without loss; and the closing sentence on conditional results would read as well after the third sentence, so its
relation to what precedes it is unwritten.

Sample rewrite:

```latex
Adapting these codes to the test world meant finding two things in them: Earth values, each a value or form in a
model that agrees with Earth because it was set or fitted there, and defects, code that contradicts its own inputs,
units or intent. In the four codes the Earth values take four forms: dimensional constants written into the code,
units of time, geometry, and empirical fits and simplifications used beyond the range they were made for. On the
paths the lunar runs take, the released codes also contain five defects, three of which produce little or no error
at Earth's values yet, by ExoPlaSim's own arithmetic, bias its runs that meet their conditions, runs of slowly
rotating and tidally locked planets among them. Of the repairs made to these values and defects, most fall into
three classes, which differ in the worlds they hold for. A general repair, which corrects a unit, applies a scaling
law or a parameterization fitted over a wider range, or removes a defect, contains no coefficient fitted to the
test world and is built to hold on another world within the limits of its laws; a general method holds wherever
its table is computed from that world's own column, as for the curved geometry of a tall atmosphere; and a
calibration, fitted to the reference model on columns of the test world, holds near those columns and must be
refitted for another world. Settings, added capabilities, couplings, a bound, a mitigation and avoidances by
configuration make up the remaining changes. The class of a repair followed largely from the form of the Earth
value it removed. Of the four forms, moreover, the fits moved the test world's climate furthest. Even after these
repairs, every lunar climate number is a conditional model result, holding given the scenario and the Earth values
that remain.
```

The semicolon series of the three classes stays, as a catalogue announced by the sentence before it.

### worlds.tex

**F14. worlds.tex:8–10. Kind 3. MINOR.** "… and the solar day sets whatever a formula counts per day. Natural and
constructed worlds lie off Earth's values in different directions"
Repair: the step from what the four ratios set to where worlds lie along them is unmarked; take up the ratios, e.g.
"Along these four ratios, natural and constructed worlds lie off Earth's values in different directions".

**F15. worlds.tex:31–34. Kind 5. MINOR.** "… settles at the design value of 295~K; the sensitivity runs reported
below hold their sunlight fixed, and the scale was set once, for the design case."
Repair: a consequence given in reverse order behind a semicolon and "and"; write "… 295~K, and since the scale was
set once, for the design case, the sensitivity runs reported below hold their sunlight fixed".

**F16. worlds.tex:39–41. Kind 5. MINOR.** "… hold water; the seas are a 50~m slab with sea ice, and the land has a
placeholder albedo of 0.2."
Repair: the turn from the scenario's geography to the way the model represents seas and land goes to a semicolon;
give it its own sentence with a marker, e.g. "As modelled, the seas are a 50~m slab with sea ice, and the land has a
placeholder albedo of 0.2."

**F17. worlds.tex:70–71. Kind 4. MINOR.** "Every absorber path through the test world's air is longer … is curved."
Repair: after the scenario and the table, the paragraph returns to the first pair of ratios from the section's
opening with no bridge; mark the return, e.g. "With this scenario's column and scale height, every absorber path
through the test world's air is longer than its counterpart on Earth, and every layer the models treat as flat is
curved."

**F18. worlds.tex:73–84. Kinds 1, 3 and 5. MAJOR.** "In the column on which the curved geometry was computed …
than the models count."

What fails: after the topic sentence and its first example, three sentences in a row give three separate
consequences of the tall air (the geometry of one column, twilight, gravity falling with height), each opening on a
new subject with its relation to the sentence before left unwritten. Inside the first, the comparison with Titan
follows a semicolon after the horizon air masses, though it concerns the proportion given at the sentence's start.
The twilight and gravity sentences can trade places without loss.

Sample rewrite:

```latex
The curvature comes from the air's height: in the column on which the curved geometry was computed, the scale
height is about 52~km over a radius of 1,737~km, while Titan's air, at 0.8\% of its radius, is about a quarter as
tall in proportion. The air's mass lies on average 48.6~km above the ground, where a shell has 5.7\% more area than
the ground beneath it, and straight rays through that column give horizon air masses of 7.1 for well-mixed air and
13.5 for water vapour, against the 35 of PlaSim's formula, written for Earth.\claim{S09}\claim{W02} Because the air
is so tall, sunlight reaches far past each column's horizon: a full Earth day after sunset, about half the air above
a place still lies above the Moon's geometric shadow, before refraction adds more.\claim{S04} Across that height
gravity also falls, 9\% by the 86~km tropopause, so a column with gravity falling as $GM/r^2$ holds about 5\% more
air than the $p_s/g_s$ the codes assume, and spherical shells with that gravity raise the excess to 11.5\% per
square metre of ground: for the same surface pressure, the lunar air holds about a tenth more mass than the models
count.\claim{S10}
```

The rewrite splits the original's first sentence in two and keeps `\claim{S09}\claim{W02}` together at the end of
the pair, where the original set them at the end of its sentence.

**F19. worlds.tex:86–96. Kinds 1, 3 and 5. MAJOR.** "Gravity's surface value matters more. … justified by the dry
similarity alone."

What fails: after the hinge, the paragraph sets the effects of weak gravity side by side (heights, fall speeds, the
sea, the dry dynamics), each in a sentence or clause that restarts on a new subject. A semicolon joins the fall
speeds to the sea with no relation. The closing limit on convection contrasts with the dry similarity just stated
and has no word to mark the contrast, and its last clause joins a cause to its effect with "and". The fall-speed
and dry-dynamics sentences can trade places without loss.

Sample rewrite:

```latex
Gravity's surface value matters more. A sixth of Earth's gravity raises every pressure level sixfold in height, so
a code that sets a feature's height in metres puts it at a sixth of its lunar height. Fall speeds respond as well,
though unevenly, because they follow gravity to powers set by each particle's fall-speed law, slowing droplets
sixfold, rain about threefold and graupel 2.3-fold, the dependence on gravity that \textcite{loftus2021physics}
trace for raindrops across planetary atmospheres. At the sea the same weak gravity roughens the surface and slows
the waves: Charnock's roughness grows sixfold for the same friction velocity \autocite{charnock1955wind}, and a
deep-water wave of a given length travels at 0.41 of its speed on Earth.\claim{S11} The dry dynamics, for their
part, stretch about sixfold in size and duration at the same speeds, so a 6~km column of a cloud-resolving model
stands for about 1~km at Earth's scale, while the microphysics and the radiation keep their own scales. How far
lunar convection departs from Earth's, stretched sixfold, however, remains unmeasured: the pair of runs designed to
measure it failed to convect, so the 6~km grid is justified by the dry similarity alone.\claim{S12}
```

**F20. worlds.tex:98–103. Kinds 2, 4 and 5. MAJOR.** "The 29.53-day solar day deepens … Earth's tilt of
23.7\textdegree."

What fails: the paragraph is one sentence of three facts joined by semicolons (the day, the rotation, the tilt),
with no relation written among them. It opens with no bridge from the gravity paragraph, though the section's
first paragraph paired gravity and the solar day as the scales of height and time.

Sample rewrite:

```latex
The test world's day, rotation and tilt depart from Earth's as well. The 29.53-day solar day deepens the soil's
thermal wave to about 0.6~m, $\sqrt{29.53}\approx5.4$ times the depth of Earth's diurnal wave, and for the same
reason a formula written per Earth day but applied per lunar day takes nearly thirty times its intended input. The
rotation is nearly as slow: at 27.32 days it sets a Coriolis parameter of \SI{5.2e-6}{s^{-1}} at 80\textdegree, the
latitude of the polar CM1 rings, an inertial period of 14 Earth days.\claim{S13} The tilt, by contrast, is small: at
1.54\textdegree\ it keeps the Sun grazing at the poles all year, where ExoPlaSim's default orbit puts Earth's tilt
of 23.7\textdegree.\claim{H24}
```

`\claim{S13}` stays after the rotation, where the original placed it after the day and rotation clauses. The
paragraph still ends on the default orbit, which the next section takes up.

### assumptions.tex

**F21. assumptions.tex:3–11. Kinds 2, 3 and 4. MAJOR.** "ExoPlaSim's default orbit is one of the Earth values … the
adaptation's own defects."

What fails: the section's opening paragraph sets four statements side by side: the orbit default belongs to the
inventory, a repair's needs follow from form, each value errs along its ratio so the inventory doubles as a
checklist, and the defect log records more. The second and third can trade places without loss, though they concern
two different properties of each value (how it is repaired, where it errs), a contrast the text leaves unwritten.
The paragraph also ends on the defect log, so the next paragraph's "Gravity, the commonest constant" arrives with no
bridge.

Sample rewrite:

```latex
ExoPlaSim's default orbit is one of the Earth values and defects met on the paths the lunar runs take through the
four codes (Table~\ref{tab:inventory}). For each entry, the defect log in the code repository records its discovery
and evidence, with its repair and measured effect where these exist, and the log adds the entries found off the
lunar runs' paths and the adaptation's own defects. Each Earth value in the table is right at Earth's ratios and
errs as a world departs from them along the ratio it depends on, some steadily and some past a threshold, so the
inventory reads as well as a list of what to check on another world. What a repair of an Earth value needs,
however, follows from its form: a dimensional constant needs the world's own value or a law that gives it, a unit
of time the world's own unit, a geometry a method computed for the world's own air, and a fit or simplification a
refit or a scheme that holds over the world's range.
```

The rewrite moves the defect log up beside the table it describes and ends on the forms, so that "a dimensional
constant" hands on to "Gravity, the commonest constant".

**F22. assumptions.tex:27–35. Kinds 1 and 5. MAJOR.** "The other constants have the scale of Earth's air, storms,
composition and rotation. WRF-ELEC caps … Earth's rotation and radius."

What fails: after the announcing sentence, one sentence chains four constants with semicolons, out of the announced
order (storms first, then air, composition and rotation), and leaves each contrast between Earth and the Moon to
"and" ("binds on Earth only below about 4.5~km … and in lunar air below about 36~km"). The chain works as a run of
four sentences that reads as a list.

Sample rewrite:

```latex
The other constants have the scale of Earth's air, storms, composition and rotation. SWAN fixes the air's density
at 1.28~kg\,m$^{-3}$, against a mean of about 1.40 in CM1's air over the equatorial seas.\claim{H05} The air's
density enters the storms as well: WRF-ELEC caps a breakdown field scaled with the air's density
\autocite{dwyer2003fundamental} at 180~kV\,m$^{-1}$, a cap that binds on Earth only below about 4.5~km, beneath
where flashes start, but in lunar air below about 36~km, where it lowers the field by 44\% at the ground, and the
code also declares a ground strike when a channel reaches air warmer than $-7$\,\textdegree C, about 5~km above
Earth's ground but 27--34~km above the Moon's.\claim{H03} Composition and rotation, finally, stay Earth's in CM1:
RRTMG takes carbon dioxide from the calendar year, with Earth's trace gases and ozone, while CM1's beta plane
derives its gradient from Earth's rotation and radius.\claim{H06}
```

The rewrite follows the announced order, so `\claim{H05}` now precedes `\claim{H03}`; each marker stays with its own
claims.

**F23. assumptions.tex:38–42. Kind 3. MINOR.** "… against the released code's Sun. CM1's Sun follows Earth's 24-hour
day, …"
Repair: CM1's calendar arrives as a second instance with no marker of addition; e.g. "CM1's calendar is Earth's as
well: its Sun follows Earth's 24-hour day, …".

**F24. assumptions.tex:44–59. Kinds 1, 2 and 3. MAJOR.** "PlaSim and RRTMG treat each column … the boundary layer's
day--night shape."

What fails: the paragraph tours four geometric Earth values (flat, sunlit-only columns; the slant factor; the
dynamical cores; the $\sigma$ levels) in five sentences that each restart on a new subject. The second sentence
leaves out the relation that makes its numbers matter, namely that the test world's air is far taller than the
geometry suits. The slant factor arrives with no marker, though it is where PlaSim does allow for curvature, with
Earth's values. The cores' sentence leaves the step to lunar gravity's fall to a semicolon, and the $\sigma$ levels
arrive as a further item with no marker. The slant-factor and $\sigma$-level sentences can trade places without loss.

Sample rewrite:

```latex
PlaSim and RRTMG treat each column as a stack of flat layers lit only while the Sun stands above that column's
horizon, a geometry that suits air a tenth of a percent of the radius tall. The test world's air is far taller, so
against the same air in flat layers, with a pseudo-spherical direct beam for the sunlight, its air in curved shells
absorbs 10.3~W\,m$^{-2}$ more sunlight and sends 16.2~W\,m$^{-2}$ more infrared to space, a net loss of
5.8~W\,m$^{-2}$, the sum of a 6.5~W\,m$^{-2}$ loss through the widening of the shells and a 0.7~W\,m$^{-2}$ gain
from the curved light and escape, and its ground receives 1.4~W\,m$^{-2}$ of twilight while the Sun is below the
horizon.\claim{H11} Where PlaSim does allow for curvature, it uses Earth's: it stretches the low Sun's water path
by Earth's horizon magnification, $35/\sqrt{1+1224\mu^2}$ with $\mu$ the cosine of the solar zenith angle
\autocite{lacis1974parameterization,rodgers1967use}, where the Moon's factor is 13.5 for water vapour and 7.1 for
well-mixed air (Figure~\ref{fig:slant}).\claim{H12} The dynamical cores use the same flat or thin geometry,
PlaSim's a thin shell and CM1's a flat slab, both with gravity constant with height, while the reference models
compute with $g = GM/r^2$, by which lunar gravity is 5.4\% lower at the air's mass-mean height and 15.3\% lower at
CM1's 150~km top.\claim{H13} PlaSim's vertical grid is Earth's as well: its ten $\sigma$ levels are set at fractions
of the surface pressure chosen for Earth's air, and in the design case they put the top three layers above
107~km, at 81--107~km and at 63--81~km, each spanning about 25~K, with ice saturation changing 55-fold across the
second, and leave two layers for the lowest 6.5~km, too few to resolve the boundary layer's day--night shape.\claim{H33}
```

The rewrite adds one clause, "The test world's air is far taller", whose ground is the scale height over radius in
the worlds section's table (`tab:regime`: 0.030 against Earth's 0.0013).

**F25. assumptions.tex:75–76. Kind 3. MINOR.** "… and the air aloft up to 12~W\,m$^{-2}$ too little. PlaSim treats
all cloud as liquid, …"
Repair: the paragraph announced the gases' totals, split and heights, and the turn to cloud after them is unmarked;
mark it, e.g. "Beyond the gases, PlaSim treats all cloud as liquid, …".

**F26. assumptions.tex:77–79. Kind 5. MINOR.** "… forms only at 136--149\% of ice saturation; it forms cloud in each
layer above a relative-humidity threshold set for Earth, 0.983 in the lowest layer."
Repair: the clause after the semicolon gives the rule under which PlaSim forms cloud, a second Earth value that also
bears on the 136–149% figure before it, and the relation is unwritten; write it in with "because" if the threshold
explains the figure, or with "and, moreover," if it is a separate Earth value.

**F27. assumptions.tex:95–98. Kind 3. MINOR.** "One simplification holds for storms of a few hours: … and in a
month-long lunar run the charge … persisted for weeks …"
Repair: the contrast between storms of a few hours and the month-long lunar run goes to "and"; mark it "but in a
month-long lunar run".

**F28. assumptions.tex:102–110. Kind 3. MINOR.** "In a non-synchronous run on its default solar geometry, …" (102)
and "Slingo's convective cover, …" (109–110)
Repair: the paragraph announces three ExoPlaSim defects and names "The third" at line 115, while the first and second
open with no ordinal; mark the sequence, e.g. "The first is the Sun clock: in a non-synchronous run …" and "The
second is in Slingo's convective cover, …".

**F29. assumptions.tex:120–121. Kind 1. MINOR.** "The Moon's slow rotation and small tilt made all three large. The
errors of the other two are independent of the world."
Repair: two short declaratives in a row whose contrast (three defects whose errors grow with departure, two whose
errors are independent of the world) is unmarked; join them with "whereas", or open the second "The errors of the
other two, by contrast, …".

**F30. assumptions.tex:121–124. Kinds 3 and 5. MINOR.** "… so repeated Earth runs differed by about 2.5\% in wave
height; its usual configuration, with breaking on, assigns the parameter before the read."
Repair: a concession across a semicolon (the defect acts only with breaking off); mark it "…2.5\% in wave height,
although its usual configuration, with breaking on, assigns the parameter before the read".

## Summary

Thirty findings: 9 MAJOR and 21 MINOR.

| File | MAJOR | MINOR |
|---|---|---|
| `abstract.tex` | 1 | 2 |
| `introduction.tex` | 2 | 8 |
| `worlds.tex` | 3 | 4 |
| `assumptions.tex` | 3 | 7 |

The paragraphs that read most like lists:

1. `worlds.tex:98–103` (F20): one sentence holding the day, the rotation and the tilt as three facts joined by
   semicolons.
2. `introduction.tex:78–92` (F13): definitions, forms, defects, classes and an evidence-state landing set in a row of
   eight statements.
3. `worlds.tex:86–96` (F19): the effects of weak gravity side by side.
4. `assumptions.tex:44–59` (F24): a tour of four geometric Earth values.
5. `assumptions.tex:27–35` (F22): four constants in one semicolon chain, out of their announced order.

Close behind them is `assumptions.tex:3–11` (F21), the opening of its section.

Judged sound, or genuine catalogues, and left out: the mapping of forms to repairs at `abstract.tex:16–19`; the four
studies at `introduction.tex:9–13`, set out in the order of the sentence that announces them; the forcing chain at
`introduction.tex:63–72`; the three classes of repair at `introduction.tex:84–89`; the four ratios in two announced
pairs at `worlds.tex:4–9`, and the worlds placed on the figure at `worlds.tex:10–14`; the scenario at
`worlds.tex:30–39`, which descends from the shield to the ground (apart from F15 and F16); gravity as a number, a
length and a frequency at `assumptions.tex:13–27`; the radiation fits at `assumptions.tex:61–75`, ordered by the
totals, split and heights their second sentence announces; the Earth-fitted laws listed after the colon at
`assumptions.tex:91–95`; and the defects at `assumptions.tex:100–129` (apart from F28 to F30).

Transitions at the edges of the part are sound. The worlds section opens on "the models' Earth values", taken from
the introduction's close. The Earth-values section opens on ExoPlaSim's default orbit, the last item of the worlds
section. The Earth-values section ends with the inventory table, whose Repair column leads into the next section's
"Most repairs follow one rule".
