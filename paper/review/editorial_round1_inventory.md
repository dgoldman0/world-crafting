# Editorial review, round 1: assumptions.tex and repairs.tex

## Record

**Reviewer.** A fresh Claude subagent (Claude Opus 5.5), started for this review alone and given no earlier
review record. Date: 2026-10-17.

**Scope.** `paper/sections/assumptions.tex` (sha256
`4b0f209c6aebcbc4c907778548d27c5dca9512e3d44347ccf7cdff2f98b9cfd7`) and `paper/sections/repairs.tex`
(sha256 `3bcef8a3a813e83b33cf4f954da68c05ce6bd78f8d31375808a955162dca81ef`), with their figures, tables and
captions: Figure `fig:sunclock`, Table `tab:inventory`, Figures `fig:slant` and `fig:layers`. Table
`tab:repairs`, which repairs.tex cites for its departures and its classes, lies in appendix.tex and was read
as their companion.

**Repository state.** The review began at commit 4d03a81. During it, commit a06a4ab (notes and review
records) landed; both scope files kept the hashes above.

**Rules, read in full before the paper.**
- `AGENTS.md` on disk, sha256 `e1f25bc04fd72bafa5e1a41716f38bef56f5b22b5a6de0584c35623f54016d32`, with its
  sections "The paper", "Writing" and "Review".
- Terluna `ensemble/planning/Open_Moon_Editorial_Charter_control-01.md`, sha256
  `aac4a4f29402189ad9d3dd91e35bf860dabb26125aac94ba21cdf8054f4780b0`.
- `source_controls/STYLE_NOTES.md`, sha256
  `659627e564bba84d8ebed0ddebd33687705b31e1bf29decb6037e248eb4f5c46`.
- `source_controls/Jewish_Papers_Updated_Style_Notes.md`, sha256
  `18f3d0db8a83a48a55918dd66faec9b1473b5f1887c4ea7bffa0223deccb3eab`.
- `source_controls/Agent_Working_State_Editorial_Gates.md`, sha256
  `553e8957640ad194576a8aa403adc4e83dc71a177178fbe4bb4fa3873cd82464`.

**Read in full.** The five rule files above; for context, `introduction.tex` (sha256
`5d1b9cf839ea398370c884d828d54fe45951ab79492e9f3c7a3fce6a70aff9e0`) and `worlds.tex` (sha256
`46dc5b00bfd347693c0f57929ee690f4db4cd1a4ac97b996b82af07f010ff0b2`); both scope files; `appendix.tex` (sha256
`eaf27468e42bc1a28a57a6fdcafd8b7fa58365254e5ad965a794862237e196c6`, Tables `tab:config`, `tab:repairs`,
`tab:verification`); `reach.tex` (sha256 `817ee9ed88c4d9471d313708a4fc1b186d1e903e692c40c3d7e2d5bdf756a42f`);
`notes/defect_log.md`; `notes/exoplasim.md` at its state before a06a4ab.

**Read in part, for facts.** `results.tex` lines 1–60 (Table `tab:states`); `verification.tex` lines 1–30;
`paper/claims.json`, the entries for every claim marked in scope (H01–H33, R01–R15) and for S12, S13, W01,
W02, W06, V01–V03, V15, G04, G13, G14; `notes/cm1.md` lines 1–120; `notes/reference_radiation.md` lines
285–415; `models/exoplasim/README.md` lines 1–100; `models/cm1/builds.json`; `PROVENANCE.md` lines 1–30;
searches in `models/swash/README.md`, `models/swan/README.md` and `notes/waves.md`; Terluna
`climate/gcm/README.md` lines 165–215 and `climate/crm/README.md` lines 76–112 (checkout f03b839, which the
defect log equates with 186b294 for these files); the `references.bib` entries for Lacis and Hansen, Ebert and
Curry, Kristjánsson et al. and Mitchell; the PNG renders of the three figures in scope.

**Left unread by design.** `paper/notes/` and every file in `paper/review/`; the names of the review files
appeared once in a directory listing made while hashing, and none was opened.

**Method.** Each paragraph was read whole, then sentence by sentence, under the ten passes of the charter's
section 11 as they apply to two body sections, with the numbers checked against `claims.json` and the records
it cites. A lexical screen for "not" and "rather than" ran over both files; it is screening only.
`paper/tools/lint.py` was left unrun. The cadence check was a silent reading; no read-aloud pass was made.

**Counts.** 38 findings: 4 BLOCKING, 15 MAJOR, 19 MINOR.

## Findings

Line numbers refer to the files at the hashes above. A row of `tab:inventory` is cited by its line in
assumptions.tex, a row of `tab:repairs` by its line in appendix.tex. In each rewrite the paper's claim markers
stay with their numbers.

### 1. MAJOR · assumptions.tex:4–5, 9–10, 101–102, 114–115 · Earth value against defect

**Text.**
- 4–5: "Such a value is a limitation of the code, which does what it was written to do, for the world and
  range it was written for."
- 9–10: "Three of the five defects found in the released codes are tied to Earth's values through the same
  forms."
- 101–102: "Five defects sit in the released codes, and three of them are tied to Earth's values through a
  form."
- 114–115: "The third is an Earth constant."

**Rule.** The section's central distinction applied consistently (a definition its own example breaks);
Exact action ("sit").

**Why.** Lines 3–8 set two exclusive kinds: an Earth value, which is a limitation, and a defect, code that
contradicts its own inputs, units or intent. Line 114 calls the orbit default "an Earth constant", which by
line 4 makes it a limitation, while Table `tab:inventory` (row 159) gives it kind D and the paragraph counts it
among the defects. The prose and the table also follow two schemes: the prose writes four paragraphs by form
and a fifth for defects, so a defect reads as a fifth form, while the table gives form and kind as separate
columns and assigns a form to three defects. "Tied to Earth's values through a form" leaves the relation
unstated, and defects that "sit" in code are an empty action.

**Rewrite.**
- 9–10: "Three of the five defects found in the released codes produce little or no error at Earth's values
  and an error that grows as a world departs from them, two through units of time and one through a
  constant; Table~\ref{tab:inventory} therefore gives each entry a kind and, where one applies, a form."
- 101–102: "Of the five defects in the released codes, the three that produce little or no error at Earth's
  values are ExoPlaSim's. Two are errors of time."
- 114–115: "The third puts an Earth constant in place of a configured value."

### 2. MAJOR · assumptions.tex:10–13 · "each" in the pointer to the table and the log

**Text.** "Table~\ref{tab:inventory} lists the Earth values and defects on the paths the lunar runs use, each
with its form, its kind and its repair, and the defect log in the code repository adds those found off those
paths, with each one's discovery, evidence, repair and measured effect."

**Rule.** Claims stay within their evidence.

**Why.** Rows 172, 184 and 198 of the table give "---" for form, and row 172 gives "?" for kind. The defect
log records "Not quantified" as the effect of A3, B21, B22, B25, B27 and B28, and lists no repair for A4, A6,
B7, B9, B20, B21, B22, B27 and B28. Its classes (a) and (b) match the table's rows nearly one for one; what
it adds is a few off-path items and its class (c), the adaptation's own defects. The log's opening note on
the paper's classes (defect_log.md lines 104–107) still counts A4 and A6 as defects whose tie to Earth's
values is unknown and leaves B11 out, while the paper counts B11 and A6 among the five and A4 as a sixth
fault; a reader sent to the log meets a different count there, beside a later note under B11 that follows the
paper.

**Rewrite.** "Table~\ref{tab:inventory} lists the Earth values and defects on the paths the lunar runs use,
with the form, kind and repair of each where these are known; the defect log in the code repository records
each entry's discovery and evidence, with its repair and measured effect where these exist, and adds the
entries found off those paths and the defects of the adaptation itself." The log's note at lines 104–107
needs the paper's count (a file outside this review).

### 3. BLOCKING · assumptions.tex:15–38 · the constants paragraph is a tour by model

**Text.** The sentences open: "CM1 release 22 sets gravity to 9.81~m\,s$^{-2}$ in four places …" (16);
"WRF-ELEC's NSSL scheme sets 9.8 twice …" (20); "PlaSim diagnoses its clouds' water with CCM3's profile …"
(21); "WRF-ELEC's lightning holds two thresholds and a time step set for Earth's air and storms." (24–25);
"Its breakdown field, …" (25); "SWAN's constants come from Earth's seas." (30); "It reduces its linear wind
input …" (30); "Earth's composition and rotation enter the remaining constants: …" (34–35); "Options the lunar
runs leave unselected, …" (37).

**Rule.** G1 (swap test; feature tour); Sentences carry their dependencies (repeated subject resets);
Inheritance and order.

**Why.** The opening sentence sets a relation, gravity as the commonest constant, and the next three
sentences follow it; the paragraph then turns to the models one by one, and SWAN's knee, a gravity constant,
comes after WRF-ELEC's lightning. The sentences on PlaSim's cloud water, WRF-ELEC's lightning and SWAN trade
places with no loss, and seven of the ten sentences open on a model's name or a pronoun for one. Table
`tab:inventory` holds the same items in rows. Ordered by its own opening relation, the paragraph would state
first the routes by which gravity enters the codes, then the constants of Earth's air, storms, composition and
rotation.

**Rewrite.**

> \textbf{Constants written into the code.} A dimensional constant has the scale of the world it was set
> for, and gravity, the commonest, enters the codes by three routes. As a number, it is 9.81~m\,s$^{-2}$ in
> four places on the lunar cases' paths in CM1 release 22, its dynamics, the conversion of pressure to layer
> mass in its RRTMG radiation \autocite{iacono2008radiative}, its CAPE diagnostic and the Morrison
> microphysics, as well as in schemes those cases leave unselected, and 9.8, set twice, in WRF-ELEC's NSSL
> scheme; the coefficients of both schemes' fall-speed laws $V = aD^b$ and their caps were fitted at Earth's
> gravity, and NSSL ties the ventilation of evaporating rain and depositing ice to those coefficients. As a
> length, it enters CCM3's profile of cloud water \autocite{kiehl1996description}, from which PlaSim
> diagnoses its clouds' water and which decays with geometric height on a scale of
> $700\ln(1+\mathrm{PW})$~m written for Earth's gravity; with every pressure level six times higher, clouds
> above about 20~km, most of the lunar cover, were left nearly dry. As a frequency, it enters SWAN, which
> reduces its linear wind input above a knee fixed at 1~Hz, a value its source comments call largely
> arbitrary; because the knee stays fixed while gravity changes, stock SWAN misses a sixfold
> gravity-similarity test by 5.44\% in significant wave height. Other constants are set for Earth's air,
> storms, composition and rotation: SWAN's air density of 1.28~kg\,m$^{-3}$, against a mean of about 1.40 in
> CM1's air over the equatorial seas; WRF-ELEC's cap of 180~kV\,m$^{-1}$ on a breakdown field scaled with
> the air's density \autocite{dwyer2003fundamental}, which binds on Earth only below about 4.5~km, beneath
> where flashes start, and in lunar air below about 36~km, lowering the field by 44\% at the ground; its
> ground-strike temperature of $-7$\,\textdegree C, about 5~km above Earth's ground and 27--34~km above the
> Moon's; its 0.75~s sub-step, sized for 500~m layers and Earth's fall speeds; RRTMG's carbon dioxide by
> calendar year, with Earth's methane, nitrous oxide, halocarbons and ozone; and CM1's beta plane, derived
> from Earth's rotation and a 6,370~km radius. Options the lunar runs leave unselected, SWAN's ST6 source
> terms and exact nonlinear transfer and SWASH's rotation for spherical runs, are set to Earth's gravity or
> rotation as well.

The author can reduce the closing list to a pointer to the table and keep its numbers there.

### 4. MAJOR · assumptions.tex:19–20, 89–93; rows 175–176, 189, 193 · constant against fit

**Text.**
- 19–20: "and the coefficients of Morrison's fall-speed laws $V = aD^b$ and their caps were fitted at Earth's
  gravity."
- 89: "The laws of drops, seas and charge were fitted to Earth's data in the same way."
- 90–92: "Morrison's scheme as implemented in CM1 \autocite{morrison2005new} bounds the mean diameter of rain
  at 2.8~mm and begins breakup in rain's self-collection above a mean of 0.3~mm, …"
- Rows: 175 "Gravity & 9.81 in four routines on the lunar paths; fall speeds & … & Constant"; 176 "Rain size &
  … & Fit"; 189 "Ground strike & $-7$\,\textdegree C level; stopping field 0.15 & … & Constant"; 193 "Charging,
  thresholds & Laboratory laws; 50~MV, 10~kV\,m$^{-1}$ & … & Fit".

**Rule.** The forms applied consistently; the same thing classed two ways.

**Why.** Morrison's fall-speed coefficients and its rain-size bounds are dimensional values of one scheme,
both set for Earth's gravity: the first are constants (line 19, row 175), the second fits (lines 89–93, row
176), and line 89 calls the laws of drops fits after line 19 placed the fall-speed laws of drops among the
constants. WRF-ELEC's ground-strike conditions split the same way: the −7 °C level and the 0.15 stopping field
are constants (row 189), the 50 MV and 10 kV m−1 conditions fits (row 193), while the defect log (B5, B7)
describes all four as Earth calibrations of the one rule.

**Rewrite.** State one criterion where the forms are named (lines 8–9), for example "a constant is a
dimensional value with the scale of the world it was set for; a fit is a law fitted to Earth's data and valid
over the range of those data", and apply it to every row. Under that criterion the rain-size bounds join the
fall-speed laws in the constants paragraph: "Morrison's scheme also bounds the mean diameter of rain at
2.8~mm and begins breakup in rain's self-collection above a mean of 0.3~mm, values set for Earth's rain, while
the largest drop that survives its own fall scales with the capillary length $\sqrt{\sigma/\rho_w g}$, 2.46
times longer at lunar gravity"; line 89 opens "The laws of seas and charge were fitted to Earth's data in the
same way."; and the 50 MV and 10 kV m−1 conditions move from row 193 to the ground-strike row as constants.
The opposite choice, the fall-speed laws as fits, is equally consistent if applied to all four.

### 5. MINOR · assumptions.tex:30–35 · SWAN's constants and "the remaining constants"

**Text.**
- 30–31: "SWAN's constants come from Earth's seas. It reduces its linear wind input above a knee fixed at
  1~Hz, a value its source comments call largely arbitrary,"
- 33–34: "it also fixes the air's density at 1.28~kg\,m$^{-3}$, where the air over the lunar seas holds about
  1.40."
- 34–35: "Earth's composition and rotation enter the remaining constants:"

**Rule.** Claims stay within their evidence; Technical meaning survives editing (scope and evidence state).

**Why.** The first example of constants that "come from Earth's seas" is a value its own source calls largely
arbitrary. The 1.40 kg m−3 is the mean moist surface density of CM1's equatorial water columns near
Smythii–Marginis (claim H05; defect log B25), a CM1 result; "the air over the lunar seas" widens it to every
sea and states it as a property of the Moon, and air "holds" a density only loosely. "The remaining constants"
are two, while the table lists three more that the prose names nowhere: RRTMG's unfiltered Sun (row 180),
CM1's damping time and mixing length (row 182) and WRF-ELEC's flash-reach threshold (row 191).

**Rewrite.** The rewrite in Finding 3 covers all three: SWAN's knee enters as a route of gravity; "SWAN's air
density of 1.28~kg\,m$^{-3}$, against a mean of about 1.40 in CM1's air over the equatorial seas"; and "Other
constants are set for Earth's air, storms, composition and rotation:". Rows 180, 182 and 191 then need a
clause in the prose or a pointer to the table.

### 6. MINOR · assumptions.tex:143, 199 · the table's scope

**Text.** Caption, 143: "Earth values and defects on the paths the lunar runs use." Row 199: "Unselected
options & 2~s initial period; $g$ in ST6 and exact transfer; SWASH's rotation & Unused in the lunar runs &
Constant & L & Avoided".

**Rule.** Technical meaning survives editing: a caption and its rows agree.

**Why.** The caption limits the table to the lunar paths; row 199 lists options off them, and lines 11–13 send
off-path items to the defect log.

**Rewrite.** Caption: "Earth values and defects in the codes the lunar runs use, on their paths, with the
options they leave unselected gathered in one row."

### 7. MAJOR · assumptions.tex:40, 45–48; row 192 · units of time

**Text.** 40: "Earth's day enters as a unit of time in the calendars and in processes that a run of a few hours
can neglect." 45–47: "WRF-ELEC conducts no charge through clear air, its screening option acting only at cloud
edges, an omission of little weight in a storm of a few hours;" Row 192: "Conduction & None in clear air &
Charge persists for weeks & Time & L & Capability".

**Rule.** A definition its own example breaks.

**Why.** The form names Earth's day; the conduction example turns on the hours an Earth storm lasts, and
WRF-ELEC leaves clear-air conduction out at any day length. The omission matches the fourth form, a
simplification used beyond its range: it holds for runs of hours and breaks down in runs of a month. Row
192's class, Time, depends on that broken definition.

**Rewrite.** Either widen the form at line 40: "Earth's day, and the few hours an Earth storm lasts, enter as
units of time: in the calendars, in the soil and in processes that a run of a few hours can neglect." Or move
the conduction sentence to the paragraph on fits and simplifications and class row 192 as Fit.

### 8. MAJOR · assumptions.tex:52–56 · the curved geometry as an agent

**Text.** "Against the same air in flat layers, with a pseudo-spherical direct beam for the sunlight, the
curved geometry takes in 10.3~W\,m$^{-2}$ more sunlight and lets out 16.2~W\,m$^{-2}$ more infrared, a net loss
of 5.8~W\,m$^{-2}$, of which the widening of the shells accounts for 6.5 and the curved light and escape return
0.7; its twilight puts 1.4~W\,m$^{-2}$ on the ground while the Sun is below the horizon."

**Rule.** Exact action; Technical meaning survives editing.

**Why.** A geometry absorbs and emits nothing; the air in curved shells does. "Return" is a "gives back", one
of the verbs this review was asked to check. "Of which … 6.5" names a part larger than the whole: the net loss is the sum of −6.5 and
+0.7.

**Rewrite.** "Against the same air in flat layers, with a pseudo-spherical direct beam for the sunlight, the
air in curved shells absorbs 10.3~W\,m$^{-2}$ more sunlight and sends 16.2~W\,m$^{-2}$ more infrared to space, a
net loss of 5.8~W\,m$^{-2}$, the sum of a 6.5~W\,m$^{-2}$ loss through the widening of the shells and a
0.7~W\,m$^{-2}$ gain from the curved light and escape. The ground receives 1.4~W\,m$^{-2}$ of twilight while the
Sun is below the horizon."

### 9. MINOR · assumptions.tex:59–66; rows 162, 165 · dynamics and levels

**Text.** 59–60: "The dynamics hold the same flat or thin geometry:"; 61–62: "while the in-house reference
models take $g = GM/r^2$, and lunar gravity falls 5.4\% by the air's mass-mean height and 15.3\% by CM1's
150~km top."; 62–63: "PlaSim's ten $\sigma$ levels sit at fractions of the surface pressure chosen for Earth's
air."

**Rule.** Exact action; precise nouns; the forms applied consistently.

**Why.** "Hold", "take" and "sit" name no operation, and "falls 5.4% by the height" reads both as an amount and
as a place. The paragraph opens on geometry as flat layers lit only with the Sun up (lines 50–51); the σ
levels are a vertical spacing, which that definition leaves out, while row 162 classes them as Geometry. The table gives a Dynamics row for PlaSim (row 165) and none for CM1, whose flat slab and 15.3% the
prose names.

**Rewrite.** "The dynamical cores use the same flat or thin geometry: PlaSim's treats the air as a thin shell
and CM1's as a flat slab, both with gravity constant with height, while the in-house reference models compute
with $g = GM/r^2$; lunar gravity is 5.4\% lower at the air's mass-mean height and 15.3\% lower at CM1's 150~km
top. PlaSim's ten $\sigma$ levels are set at fractions of the surface pressure chosen for Earth's air." At
lines 50–51, name the spacing within the form: "PlaSim and RRTMG treat each column as a stack of flat layers,
lit only while the Sun stands above that column's horizon, and PlaSim spaces its layers for Earth's air." Add a
CM1 row for the dynamics.

### 10. MINOR · assumptions.tex:63–64; repairs.tex:113–114, 129–130 · two sets of layer heights

**Text.** assumptions.tex:63–64: "On the Moon they put the top three layers above 107~km, at 81--107~km and at
63--81~km"; repairs.tex:113–114: "PlaSim put almost nothing above 85~km"; the `fig:layers` panel labels
(112–575, 85–112 and 66–85 km) and caption (repairs.tex:129–130): "35--66~km in place of 66--85~km".

**Rule.** Technical meaning survives editing.

**Why.** The same three PlaSim layers have two sets of boundaries four to five kilometres apart. Each set
belongs to a column (claim H33 cites `notes/exoplasim.md`; claim R10 the layer data of the curved-air design
column), and neither text names its column, so a reader who compares "the second layer from the top" at 81–107
km (assumptions.tex:82–83 with H19) with the figure's 85–112 km finds two heights for one layer.

**Rewrite.** Name the column at each use, for example "In the GCM's design case they put the top three layers
above 107~km, at 81--107~km and at 63--81~km" (the column to be confirmed against the source of H33) and "in
the curved-air design column PlaSim put almost nothing above 85~km", with the column stated in the
`fig:layers` caption; or give one column's heights throughout.

### 11. BLOCKING · assumptions.tex:68–87 · the fits paragraph is a tour

**Text.** After the opening, the sentences open: "PlaSim's near-infrared water absorptivity, …" (69–70);
"ExoPlaSim normalises its Rayleigh coefficient …" (72); "PlaSim's two shortwave bands omit carbon dioxide and
oxygen, …" (76); "PlaSim's longwave, Sasamori's broadband absorptivities …" (78–79); "It gives every cloud the
optics of liquid water …" (82); "In CM1, RRTMG's reference pressures begin at 1,053.63~hPa, …" (84). Line 80:
"against the correlated-$k$ reference".

**Rule.** G1 (swap test); Sentences carry their dependencies (subject resets); Write for the expert (a term
used before its introduction).

**Why.** The five PlaSim fits at lines 69–83 trade places with no loss, and five consecutive sentences open on
PlaSim, ExoPlaSim, PlaSim, PlaSim and It. Their order follows neither the order in which the errors were found
(Rayleigh and continuum on 25 September, the water absorptivity on 29 September, the gas bands on 14 October,
the longwave and cloud on 17 October) nor the order of the calibrations at repairs.tex:107–121 (totals, split,
heights), and the paragraph can follow either. "The correlated-k reference" appears here before
repairs.tex:102–103 introduces the correlated-k emulation.

**Rewrite.**

> \textbf{Fits and simplifications beyond their range.} The radiation schemes were fitted to Earth's columns
> and Earth's Sun, and the lunar columns lie far outside both; PlaSim's fits were found to err first in the
> column's totals, then in its split of sunlight, then in the heights at which it absorbs and cools. In the
> totals, ExoPlaSim normalises its Rayleigh coefficient to the ultraviolet of a 5772~K blackbody, which for
> the shield-filtered Sun gives a coefficient too low, and PlaSim's water continuum over-absorbs at lunar
> paths; uncalibrated, the first design run, with 25\% seas under the undimmed shield, passed 310~K and was
> still warming at 315.5~K in model year 12. In the split, Lacis and Hansen's near-infrared water
> absorptivity, fitted to Earth's water paths \autocite{lacis1974parameterization}, levels off toward half the
> sunlight, and over the Moon's longer paths it left the air absorbing 7.7--8.2 points too little of the
> arriving sunlight on eleven columns. By height, PlaSim's two shortwave bands omit carbon dioxide and
> oxygen, whose lines absorb sunlight high in a column 7.25 times Earth's, so once a water multiplier was
> calibrated on the column's total, the water absorbed their share lower down; and PlaSim's longwave,
> Sasamori's broadband absorptivities \autocite{sasamori1968radiative} with a water continuum that the first
> calibration fitted to the outgoing flux, cools the lowest two layers 9.7--11.9~W\,m$^{-2}$ too much against
> the correlated-$k$ emulation of the reference model and the air aloft up to 12~W\,m$^{-2}$ too little.
> PlaSim's cloud scheme treats all cloud as liquid, giving it liquid water's optics and reckoning saturation
> over liquid at every temperature, so the high cloud in its second layer from the top, at 180--204~K, forms
> only at 136--149\% of ice saturation. In CM1, RRTMG's reference pressures begin at 1,053.63~hPa, and the
> lowest 7.5~km of air over the lunar sea, at up to 1,216~hPa, lie beyond them and are extrapolated in
> $\ln p$; its ice optics end at 140~\textmu m, a size that slowly falling lunar ice outgrows, and the
> electrified box stopped at day 6.45 when its microphysics passed 157~\textmu m to the radiation.

### 12. MINOR · assumptions.tex:110–115 · agents of the cover and the orbit

**Text.** 110–111: "a conversion that ExoPlaSim's replacement of the solar day by 86,400~s in its unit
conversions \autocite{paradise2022exoplasim} left in place"; 113: "so the formula takes lunar rain as about 30
times heavier than it is"; 115: "replaces the configured obliquity, without a warning, with that of Earth's
orbit".

**Rule.** Exact action (people visible where they did the work); negative contrast judged by meaning.

**Why.** A replacement leaves nothing in place; ExoPlaSim's developers made the replacement and left this
conversion. A formula "takes" rain as heavier only as a figure; the code reads it so. "Without a warning" has
an affirmative form.

**Rewrite.** "…converts the rain with the model's solar day, a conversion that ExoPlaSim's developers left in
place when they replaced the solar day by 86,400~s in its unit conversions \autocite{paradise2022exoplasim}."
"…so the formula reads lunar rain as about 30 times heavier than it is…" "ExoPlaSim's default orbit setting
silently replaces the configured obliquity with that of Earth's orbit…"

### 13. MINOR · assumptions.tex:120, 123–126 · the two defects independent of the world

**Text.** 120: "The other two lie outside the Earth values." 123–126: "CM1 on several threads departs from
itself after a few thousand seconds, … and the race, placed in CM1's own loops by ruling out the patches,
remains unlocated."

**Rule.** Exact action; No witticisms (a code departing from itself).

**Why.** Defects "lie outside" values only as a figure; the relation is independence from the world. Runs part
from one another; the code is the same in all of them. "Placed" and "unlocated" in one clause read as a
contradiction until the reader works out that a check of the patches confined the race to CM1's loops and
the search that followed left it unlocated there. Terluna's record (climate/crm/README.md lines 87–91) states
the check.

**Rewrite.** "The errors of the other two are independent of the world." … "Runs of CM1 on several threads
part from one another after a few thousand seconds, first in the domain's total vertical momentum, in the plain
Morrison build as in the electrified one; since every patch in a threaded region writes only its own points
and WRF-ELEC's threaded loops only their own slabs, the race lies in CM1's own threaded loops, where it remains
unlocated."

### 14. MINOR · assumptions.tex:135–138 · the Sun-clock caption

**Text.** "the circles rebuild that pattern from PlaSim's solar-position arithmetic alone." and "the row varies
only by the 0.991--1.017 that 12.1 lunar days in a model year give."

**Rule.** Exact action.

**Why.** Plot markers rebuild nothing; they display a pattern a calculation rebuilt. "Give" is the generic
verb where a spread is expected.

**Rewrite.** "the circles are that pattern rebuilt from PlaSim's solar-position arithmetic alone. Under the
synodic clock, in a test from the same state, the row varies only between 0.991 and 1.017, the spread expected
from 12.1 lunar days in a model year."

### 15. MINOR · assumptions.tex:143–200 · rows and legend of the inventory table

**Rule.** Technical meaning survives editing; Write for the expert.

**Text and why.**
- Legend, 143–145: the Form and Kind legends list four forms and L or D; rows 172, 184 and 198 use "---" and
  row 172 "?". The Repair legend includes "bypassed" (row 183), a kind defined nowhere in repairs.tex
  (Finding 19).
- Row 170, "High cloud at 165--217~K reflects as liquid", against "at 180--204~K" in the prose (82–83): the
  table's range is the high cloud's in the longwave test (`notes/exoplasim.md`, patch 10), the prose's that of
  the design case's second layer.
- Row 180, "5~W\,m$^{-2}$ of clear-air absorption": the record gives 5 W m−2 of the difference in clear-air
  absorbed sunlight between CM1 and the GCM at 0° E (defect log B9); the row drops both conditions, and the
  prose names this item nowhere.
- Row 182, "Damping, mixing length & 300~s; 75~m & Earth's scales": the lunar column repeats the Earth column;
  on the Moon each is a sixth of its stretched equivalent.
- Row 187, "Rain evaporates 1.3--1.5 times too fast if scaled alone": this describes the adaptation's own
  first patch, which scaled the fall speeds and left the ventilation at Earth's (defect log C12); the released
  code's lunar error is the unscaled fall speed.
- Row 191, "Flash reach & Logged above a charge threshold & Weak high flashes logged none": the prose of both
  sections names this item nowhere, and "logged none" leaves the reader to supply "reach".

**Rewrite.** Legend: "Form: a constant, a unit of time, geometry, or a fit or simplification used beyond its
range (Fit); --- for none. Kind: a limitation (L), a defect (D), or of uncertain cause (?)." Row 170: "High
cloud at 180--204~K (design case) reflects as liquid". Row 180: "5~W\,m$^{-2}$ of the CM1--GCM gap in clear-air
absorption at 0\textdegree~E". Row 182: "Each a sixth of its lunar equivalent". Row 187: "Fall speeds 2.3--6
times too fast; ventilation tied to them". Row 191: "Weak flashes high in thin air logged no reach".

### 16. MAJOR · repairs.tex:4–12 · the departures recited after the table marks them

**Text.** "Some changes depart from the rule, and Table~\ref{tab:repairs} marks them. CM1's deeper soil and
its zeroed trace gases and ozone act in every patched build; its 400~ppm default for carbon dioxide replaces
the calendar formula, and the electrified build's gravity defaults to 9.81 where the released NSSL scheme has
9.8; the beta plane's Coriolis force acts on departures from the base-state wind in beta-plane runs; the
electrified build caps the ice sizes its radiation reads; and SWAN's air density is compiled in. SWAN's
wind-input patch reproduces stock output only at standard gravity, 9.80665~m\,s$^{-2}$, set by input, and the
guard added to the water scaling is the identity only for spectra like the design case's. Each change is
recorded as a patch against a pinned upstream source, with its switch, its default and the checks made on it."

**Rule.** G1 and Inheritance and order (a genuine catalogue goes in a table); G4 (a caveat list after the
claim); Claims stay within their evidence ("Each change … with its switch"); Write for the expert.

**Why.** The paragraph says the table marks the departures and then lists eight of them in semicolon clauses
whose order follows no relation; the list repeats `tab:repairs`. The closing sentence gives every change a
switch, which the unconditional changes just listed lack, and calls every change a patch, while the fixed
orbit, the 17,160-step year, breaking and the initial state are settings of the released codes. "The guard
added to the water scaling" is first explained in the appendix, at `tab:repairs` row 51.

**Rewrite.** "Most repairs follow one rule: an Earth value or a defect becomes a parameter whose default
reproduces the released code, so that the repair can be switched off and its effect compared with the
original. The changes that depart from it act in every build that includes them or reproduce the released code
only under a stated condition, and Table~\ref{tab:repairs} marks each with its condition. The source changes
are recorded as patches against pinned upstream archives, each with its switch or its condition, its default
and the checks made on it, and the settings of the released codes that the runs depend on are listed with
them."

### 17. MAJOR · repairs.tex:16, 18, 19–20 · classes given actions

**Text.** 16: "and another world takes it unchanged within the limits of Table~\ref{tab:reach}."; 18: "so the
method serves another world once its table is computed there."; 19–20: "A calibration adjusts the free
coefficients of an approximate scheme until its output matches the reference model on chosen columns, and
holds near the states it was fitted on."

**Rule.** Exact action ("takes" is among the verbs this review was asked to check; a method serving; a
calibration adjusting).

**Why.** A world takes nothing; a modeller applies the repair in another world's runs, or the repair holds
there. A calibration is the operation in which someone adjusts coefficients. The phrase "another world takes
… unchanged" recurs at introduction.tex:60 and reach.tex:4 and 13, outside this scope.

**Rewrite.** "…its value follows from physics or from the code's own intent, and it holds unchanged on another
world within the limits of Table~\ref{tab:reach}. A general method with a per-world table computes a quantity
of a world's own column, a path ratio or an energy difference, and tabulates it, so the method holds on
another world once the table is computed for that world's column. In a calibration, the free coefficients of
an approximate scheme are adjusted until its output matches the reference model on chosen columns, and the
fit holds near the states it was made on."

### 18. MAJOR · repairs.tex:20–22 · the line between method and calibration

**Text.** "The line between the last two lies in the tuning: the curved-air terms follow from the column's
geometry and its computed radiation, while the coefficients of the gas bands were fitted until PlaSim matched
the line-by-line model's absorption."

**Rule.** The classes crisp and applied consistently; Technical meaning survives editing; Exact action (a
line that "lies").

**Why.** The example on the calibration side misdescribes its fit. The gas bands' coefficients were fitted
offline to the line-by-line beam's loss above every level of the design column (repairs.tex:114–115;
`notes/exoplasim.md`, patch 08), a quantity the reference computes for the column, the same kind of input as
the curved-air terms; the step that adjusted coefficients until PlaSim's own output matched was the refit of
the Rayleigh and water multipliers. The repository gives the change two classes: `tab:repairs` (appendix.tex
row 48) "Calibration (structure general)", and `models/exoplasim/README.md` "General repair (structure); lunar
fits". On the method side, the curved-air terms contain by day a solver difference, through which PlaSim is
shifted from the two-stream reference it was calibrated against (repairs.tex:88–90), a calibration's work.
Under the stated criterion, two of the section's own items, the gas bands and the curved-air terms, belong to
both classes.

**Rewrite.** "The second and third classes differ in what is fitted to what: the curved-air terms are
differences between spherical and flat solutions of the design column, traced offline and tabulated as
computed, with a slant factor fitted to straight rays through the same shells, while in a calibration PlaSim's
own coefficients are adjusted until its output matches the reference. The gas-band change has a part of each
kind: its coefficients were fitted to the line-by-line beam's loss above every level of the design column, and
the Rayleigh and water multipliers were then refitted with them until PlaSim's layers matched the reference."
The prose, `tab:repairs` and the model README then give the gas bands one class, and the daytime solver
difference is named where the method's class is stated.

### 19. MAJOR · repairs.tex:22–25 · the other kinds of change

**Text.** "Beside the three classes stand settings, which give the scenario's values; capabilities, which add a
process or a forcing the released codes lack; a bound, where the physics is unsettled; a mitigation;
avoidances by configuration; and a coupling method."

**Rule.** Exact action ("stand"); the kinds defined and applied consistently.

**Why.** "A mitigation" and "avoidances" appear as names alone, and `tab:inventory` uses a further kind,
"Bypassed" (row 183), that this sentence omits. Members break the definitions or split across kinds:
- CM1's carbon dioxide and oxygen, build constants set to the scenario's values, are a setting (appendix.tex
  row 59); CM1's gravity and Sun, also set to lunar values, are general (rows 57, 60).
- SWAN's air density, a setting (row 84), is a CM1 result.
- Released switches that keep a run clear of a defect fall in two kinds: the fixed orbit and the 17,160-step
  year are general (rows 43–44; `tab:inventory` rows 159–160), keeping depth-induced breaking on is an
  avoidance (row 85; `tab:inventory` row 198).
- The rows that force CM1 from the GCM's fields are capabilities (rows 64–68, 70); the row that forces SWAN
  from the GCM's stress is a coupling (row 86).
- "A bound" names the leader's crossing (row 77), a value chosen between two bounds, WRF-ELEC's stopping
  field and its −7 °C rule (repairs.tex:143–145).

**Rewrite.** "Six other kinds of change appear in the tables: a setting, a value the scenario fixes, entered
in the code; a capability, a process the released codes lack; a coupling, one model's fields used to force
another; an avoidance, a released configuration chosen to keep the runs clear of a defect or an Earth default;
a bound, a value chosen between two rules that bracket an unsettled process; and a mitigation, a cap on what
one scheme passes to another." The members then follow the definitions. One consistent division: the code
change that turns an Earth value into a parameter is the repair, and the lunar value entered in it is a
setting; under it CM1's gravity, Sun and air fall together, the fixed orbit, whole model days and breaking
fall together, and CM1's and SWAN's forcing fall together as couplings. The author either defines "Bypassed"
or classes the beta plane among the avoidances.

### 20. MAJOR · repairs.tex:27–35 · limitations under "Defects removed or avoided"

**Text.** "Patch 04 turns ExoPlaSim's Sun at the synodic rate continuously from the first step, a mode that
assumes a steady, non-synchronous rotation and counts the Sun's phase from step 0. Patch 03 converts
convective rain per 86,400~s. ExoPlaSim's own \code{fixedorbit} switch, whose documentation describes only the
freezing of Milankovitch variations, holds the configured orbit, and a year of 17,160 half-hour steps, …";
"SWAN's breaker parameter is avoided by keeping depth-induced breaking on in every run, and SWAN's default
initial state, whose 2~s peak period has Earth's dimensions, by starting from rest or from hotstart files."

**Rule.** The kinds applied consistently; Write for the expert (repository labels in prose); economy; Exact
action.

**Why.** Under a heading for defects, the paragraph places two limitations: the calendar (`tab:inventory` row
160, kind L) and SWAN's initial state (row 199, kind L). "Patch 04" and "Patch 03" are the repository's
labels, defined only in `tab:repairs`. "From the first step" and "from step 0" state one fact twice. A switch
"holds" an orbit only as a figure, and the read of the breaker parameter, an uninitialised read, is what the
configuration avoids. The items follow an order, from removal in the code through a released switch and a
configuration to a workaround, and the syntax can state it.

**Rewrite.**

> \textbf{Defects and Earth defaults removed or avoided.} Two defects are removed in the code: the patched
> PlaSim turns the Sun at the synodic rate continuously from step 0, a mode that assumes a steady,
> non-synchronous rotation, and converts convective rain per 86,400~s. The third is removed by ExoPlaSim's own
> \code{fixedorbit} switch, whose documentation describes only the freezing of Milankovitch variations; set,
> it makes PlaSim use the configured orbit. SWAN's uninitialised read of its breaker parameter is avoided by
> keeping depth-induced breaking on in every run, and its default initial state, whose 2~s peak period has
> Earth's dimensions, by starting from rest or from hotstart files. The thread race and PlaSim's cold lowest
> level stay open: CM1 runs that must repeat use one thread, and analyses of the lowest level screen the cold
> windows.

The calendar moves to the paragraph of Finding 26, with the sentence of Finding 21.

### 21. BLOCKING · repairs.tex:30–31 · output and the Sun

**Text.** "and a year of 17,160 half-hour steps, twelve whole lunar model days, keeps output aligned with the
Sun."

**Rule.** Technical meaning survives editing; Claims stay within their evidence.

**Why.** The synodic clock turns the Sun continuously from step 0 at one turn per 29.53 days (repairs.tex:
27–28), while the model day is 29.8 days of 1,430 steps; the Sun therefore shifts about 3.2° against the model
day each model day, about 38° a model year, and a 17,160-step year holds 12.1 lunar days. Three records say so:
the `fig:sunclock` caption (assumptions.tex:137–138, "12.1 lunar days in a model year"); reach.tex:54–57
("output kept in whole model days drifts against the Sun; analyses that sort output by the Sun's position avoid
the drift"); and Terluna's GCM README at 186b294 (climate/gcm/README.md lines 174–181: "The Sun keeps its own
day of 29.53 …, 3.2° of its path behind the model day each day, so day–night analyses sort by the Sun's
position"). Whole model days keep the ten output means at fixed places in each model day and year; their
alignment with the Sun held under PlaSim's own clock, which the same runs replaced. The same claim appears in
`models/exoplasim/README.md` ("so output means stay aligned with the Sun"), and `tab:inventory` row 160
classes the calendar's repair as general on its strength.

**Rewrite.** "A year of 17,160 half-hour steps, twelve whole lunar model days, keeps the ten output means of
each model day at the same places in every year; the synodic Sun shifts 3.2\textdegree\ a model day against
those means, so analyses sort the output by the Sun's position." At assumptions.tex:42, "against the Sun"
holds for the released clock and can say so: "so output kept by model time slips 120 steps a year against the
model day, and with it against the released code's Sun."

### 22. MAJOR · repairs.tex:37–38 · each switch and its default

**Text.** "The ExoPlaSim repairs are ten patches to PlaSim's radiation, cloud and Sun code, each adding a
namelist switch whose default is the released behaviour."

**Rule.** Claims stay within their evidence; evidence states kept distinct (a design against a run).

**Why.** Line 11 of the same section says the guard on the water scaling reproduces the released code only for
spectra like the design case's. Verification.tex:26–28 records that patches 04, 05 and 07–09 were written to
reproduce the released code at their off settings and have yet to be run that way, so for five of the ten the
identity is a design. The ExoPlaSim repairs in the tables include the fixed orbit and the 17,160-step year as
well, and both are settings.

**Rewrite.** "Ten patches change PlaSim's radiation, cloud and Sun code, each adding a namelist switch written
to reproduce the released code at its default; runs confirm that identity for five of them
(Table~\ref{tab:verification}), and the guard added with the water scaling keeps it only for spectra like the
design case's."

### 23. MAJOR · repairs.tex:37–47, with 9–10 and 64–66 · "Constants to parameters"

**Text.** Heading "\textbf{Constants to parameters.}"; 41: "SWAN's wind-input knee moves with gravity and stays
at 1~Hz under standard gravity."; 9–10: "SWAN's wind-input patch reproduces stock output only at standard
gravity, 9.80665~m\,s$^{-2}$, set by input"; 64–66: "SWAN's knee becomes a function of $f\,g_\mathrm{E}/g$,
which reproduces stock SWAN at standard gravity and restores the model's gravity similarity."; 43–47: "The code
repository holds the changes as patch series against pinned upstream archives, and a script rebuilds from those
archives, byte for byte, the deployed ExoPlaSim installation and the Fortran of the eight lunar CM1 builds used
for the results reported here, …"

**Rule.** Headings say what they name (No witticisms); G1 (an order by model); G2 (redundancy).

**Why.** The heading names the rule of line 3, while the paragraph describes how all the changes were built
and recorded, calibrations and capabilities with them. Its first three sentences treat ExoPlaSim, CM1 and SWAN
in turn and trade places freely. SWAN's knee and its identity at standard gravity appear three times in the
section. The rebuild sentence repeats verification.tex:23–26 nearly word for word.

**Rewrite.**

> \textbf{Switches and builds.} The lunar runs were made with runners, the scripts that configure, compile and
> run each model, which insert each change into the installed source at a marked anchor: in PlaSim, ten
> namelist switches; in CM1, preprocessor constants for gravity and the air's carbon dioxide and oxygen,
> defaulting to 9.81~m\,s$^{-2}$, 400~ppm and Earth's oxygen, and CM1's twenty spare namelist reals for the
> lunar Sun, the forcing and the electrification's settings. The patch series in the code repository were
> generated from the runners' edit lists, and their byte-for-byte rebuild of the deployed sources is recorded
> in Table~\ref{tab:verification}.

SWAN's knee then appears once, in the paragraph of Finding 26.

### 24. MINOR · repairs.tex:44–47 · the eight builds

**Text.** "the Fortran of the eight lunar CM1 builds used for the results reported here, while older CM1
builds, the Earth-gravity benchmark builds among them, were compiled from earlier states of the series."

**Rule.** Claims stay within their evidence.

**Why.** `models/cm1/builds.json`, the record of the check, lists the eight rebuilt builds. `moon_omp`, which
ran `ring_45n_corrected` and `ring_45n_corrected_sideways`, the 45° N comparison behind claim H32 at
repairs.tex:155–156, lies outside them, and three of the eight (`moon_omp_o3`, `moon_omp_o3_strict`,
`moon_omp_terrain_sea`) list no recorded case. `notes/cm1.md` (lines 10–13) says the series reproduce the build
of the corrected 45° rings, so the two records disagree. The series were generated on 2026-10-17 from the
runners' edit lists (`PROVENANCE.md`), so the older builds were compiled from earlier states of those lists.

**Rewrite.** Once the records agree: "…and the Fortran of eight lunar CM1 builds, among them those of the
twilight rings, the terrain boxes, the Earth-fall box and the electrified box, while older CM1 builds, among
them the build of the 45\textdegree\,N control and sideways rings and the Earth-gravity benchmark builds, were
compiled from earlier states of the runners' edit lists." If the check confirms `moon_omp`'s Fortran, the
first list includes that build. With Finding 23's rewrite the sentence moves to the verification section.

### 25. MINOR · repairs.tex:49 · a universal opening

**Text.** "Where gravity enters a fitted law, a similarity argument gives the repair."

**Rule.** Claims stay within their evidence.

**Why.** Gravity enters other fitted laws that the paper repairs another way or leaves open: CCM3's
cloud-water profile (a unit repair, repairs.tex:66–69), Morrison's rain-size bounds (open, `tab:inventory` row
176), Wu's drag and Komen's growth (open, row 200).

**Rewrite.** "In the fall-speed laws gravity enters through the balance of weight and drag, and the repair
follows from a similarity argument."

### 26. MAJOR · repairs.tex:59–70 · one argument announced, four kinds of repair

**Text.** 59: "The same argument sets other lengths and times."; 63–64: "The breakdown field already scales
with the air's density, and lifting its 180~kV\,m$^{-1}$ cap lets that scaling act wherever lunar flashes
start."; 64–65: "SWAN's knee becomes a function of $f\,g_\mathrm{E}/g$,"; 66–70: "The repairs of units and
heights restore the quantity each formula was written for. CCM3's cloud water counts heights and precipitable
water at Earth's gravity and scales its mixing ratio by $g/g_\mathrm{E}$, which gives each cloud the water path
it would hold at the same pressures on Earth, and CM1's five soil layers thicken to 5--80~cm, …"

**Rule.** G1 (a governing relation announced and then broken); Sentences carry their dependencies
(coordination of unrelated propositions); Exact action; Technical meaning survives editing.

**Why.** The similarity argument governs the damping rate, the mixing length, the sub-step and SWAN's knee; the
breakdown cap is a constant removed, the cloud water a unit changed and the soil a grid deepened for a longer
wave, and the last sentence joins the cloud water and the soil with "and". An argument sets nothing, repairs
"restore" only as a figure, and a cloud's water counts nothing; the patched code counts. A knee is a
frequency: the patch passes f g_E/g to the reduction above it, which moves the knee to g/g_E Hz.

**Rewrite.**

> CM1's Rayleigh damping rate and its boundary-layer length are scaled by $g/g_\mathrm{E}$ and
> $g_\mathrm{E}/g$, as the dry dynamics stretch, and WRF-ELEC's sub-step lengthens from 0.75 to 6.8~s, which
> keeps graupel settling through about 1\% of a layer per sub-step in the 2~km layers of the lunar charging
> zone, at 0.44 of Earth's fall speed; the boxes, rounding to whole sub-steps, run one 8~s sub-step per model
> step. In SWAN the reduction above the knee takes $f\,g_\mathrm{E}/g$ in place of $f$, which moves the knee
> to $g/g_\mathrm{E}$~Hz, reproduces stock SWAN at standard gravity and restores the model's gravity
> similarity.
>
> Other general repairs remove an Earth value directly. Lifting WRF-ELEC's 180~kV\,m$^{-1}$ cap lets the
> breakdown field's scaling with the air's density act wherever lunar flashes start. Counted at Earth's
> gravity, CCM3's formula computes the quantity it was written for: the patched code counts heights and
> precipitable water at $g_\mathrm{E}$ and scales the mixing ratio by $g/g_\mathrm{E}$, which gives each cloud
> the water path it would hold at the same pressures on Earth. For the long day, CM1's five soil layers are
> thickened to 5--80~cm, 1.55~m in all, so that they extend below the thermal wave of any solar day from a few
> Earth days to the Moon's, and ExoPlaSim's year is shortened to 17,160 half-hour steps, twelve whole lunar
> model days, which keeps the ten output means of each model day at the same places in every year; the
> synodic Sun shifts 3.2\textdegree\ a model day against those means, so analyses sort the output by the
> Sun's position.

### 27. MINOR · repairs.tex:72 · "ledger"

**Text.** "The curved geometry enters both models through an energy ledger of the design column:"

**Rule.** No witticisms (coined terms say what they name); Exact action.

**Why.** "Ledger" names a book of accounts; the object is a table of differences between spherical and flat
solutions, by solar elevation and layer. The term recurs in results.tex, reach.tex, verification.tex and
appendix.tex, so a plain name serves the whole paper. A geometry enters a model only as a figure; the codes
read a table.

**Rewrite.** "Both models read the curved geometry from a table of curved-air terms for the design column: the
radiation of the same air traced once, offline, through spherical shells and through flat layers, and the
differences tabulated." Later uses: "the curved-air table".

### 28. MINOR · repairs.tex:75–77 · the channels

**Text.** "Each channel absorbs a direct beam within 1\% of its sunlight as its members do and, beyond
1,250~nm, keeps the beam's loss above every layer; below 500~nm each band is one channel."

**Rule.** Write for the expert (a reader outside the project).

**Why.** "Its members", "keeps the beam's loss" and "each band" depend on a construction stated nowhere in the
text; `notes/reference_radiation.md` (section 2.2) states it in one step.

**Rewrite.** "The channels group wavenumbers by their absorption within bands 10--40~nm wide below 1,250~nm
and 50~cm$^{-1}$ wide beyond; each group was bisected until its mean optical depths absorb a direct beam within
1\% of the group's sunlight of what its members absorb and, beyond 1,250~nm, match within the same 1\% the
beam's loss above every layer. Below 500~nm each band is one channel."

### 29. MAJOR · repairs.tex:81–83 · "divide"

**Text.** "The ledger's terms divide the curved geometry into the widening of the shells above each square
metre of ground, worth $-6.5$~W\,m$^{-2}$ net, and the curved light and escape, the twilight and the low Sun's
side light, worth $+0.7$~W\,m$^{-2}$."

**Rule.** Exact action: AGENTS.md names "divides" among the empty actions.

**Rewrite.** "The differences are summed in two terms: the widening of the shells above each square metre of
ground, $-6.5$~W\,m$^{-2}$ net, and the curved light and escape, the twilight and the low Sun's side light,
$+0.7$~W\,m$^{-2}$."

### 30. MINOR · repairs.tex:83–86 · how the terms enter the codes

**Text.** "the terms add sunlight to each PlaSim layer or CM1 shell and the ground's share in the column's
clear share, below the horizon as well as above, and remove each layer's extra infrared escape, scaled with
temperature to the fourth power."

**Rule.** Technical meaning survives editing; Write for the expert; Exact action.

**Why.** "Remove each layer's extra infrared escape" reads as cancelling the escape, where the codes take the
extra escape out of each layer as a cooling. With "the ground's share in the column's clear share" the
reader reconstructs the operation unaided; according to `notes/exoplasim.md` (patch 07), clouds enter the term
only through the ground's clear share, which reads as the ground's term scaled by the column's clear-sky
fraction (for the author to confirm). CM1 receives the terms on its levels, by height.

**Rewrite.** "Tabulated at 167 solar elevations from $-40$ to 90\textdegree, the terms are applied in the
patched codes below the horizon as well as above: each PlaSim layer and each CM1 level gains its tabulated
sunlight, the ground gains its share scaled by the column's clear-sky fraction, and each layer loses to space
its extra infrared escape, scaled with temperature to the fourth power."

### 31. MINOR · repairs.tex:88–90 · the solver difference

**Text.** "with the Sun overhead, where the geometry is flat, the spherical solver's ground still takes 1.3\%
less than the two-stream's, so the daytime term also corrects the reference column PlaSim was calibrated
against."

**Rule.** Technical meaning survives editing; Exact action.

**Why.** With the Sun overhead the shells still curve; what vanishes is curvature's effect on the beam's path.
The reference column stays as it was; by day PlaSim is shifted from the two-stream reference toward the
successive-orders solver (`notes/reference_radiation.md`, section 2.3).

**Rewrite.** "with the Sun overhead, where curvature leaves the beam's path unchanged, the spherical solver's
ground still receives 1.3\% less sunlight than the two-stream's, so by day PlaSim is also shifted from the
two-stream reference it was calibrated against toward the successive-orders solver."

### 32. MINOR · repairs.tex:108–110 · two totals

**Text.** "The first fitted two totals, a Rayleigh multiplier and a weaker water continuum on global-mean
columns, which brought the clear-sky albedo within 0.007 and the outgoing longwave within about
2~W\,m$^{-2}$."

**Rule.** Technical meaning survives editing.

**Why.** The apposition makes the multiplier and the continuum the two totals; the totals were the clear-sky
albedo and the outgoing longwave.

**Rewrite.** "The first fitted a Rayleigh multiplier and a weaker water continuum to two totals on global-mean
columns, bringing the clear-sky albedo within 0.007 and the outgoing longwave within about 2~W\,m$^{-2}$."

### 33. MINOR · repairs.tex:117–121 · the longwave step and its conditions

**Text.** "In the longwave, a fit to totals proved insufficient:" and "removes each layer's mean error and
leaves 1--5~W\,m$^{-2}$ from column to column."

**Rule.** Say what is (a step framed by its lack); Technical meaning survives editing (conditions near the
output).

**Why.** The clause after the colon states the fact that the frame withholds. The correction's conditions
appear only in the tables and in reach.tex: it is off in the design case (`tab:inventory` row 169;
appendix.tex row 52), it was fitted on the 295 K design state, and its accuracy near the 307 K state is
unchecked (reach.tex:48–49); the sentence states its result without them.

**Rewrite.** "In the longwave, the first calibration had fitted PlaSim's water continuum to the outgoing flux,
which a scheme can match while misplacing its cooling by 10~W\,m$^{-2}$ in a layer. An extra escape to space for
each layer and for the ground, fitted over land and over sea on about 2,100 cloud-free three-day means of the
design state and scaled with temperature to the fourth power, removes each layer's mean error on that state
and leaves 1--5~W\,m$^{-2}$ from column to column; it runs only in the longwave test."

### 34. BLOCKING · repairs.tex:134–137 · ice optics called a physical law

**Text.** "Cloud colder than $-38$\,\textdegree C takes Ebert and Curry's ice optics
\autocite{ebert1992parameterization} through a delta-scaled two-stream, with an effective radius from
Kristjánsson and Mitchell's table \autocite{kristjansson2000impact}, in place of liquid water's, a physical law
in place of a simplification."

**Rule.** Technical meaning survives editing; Claims stay within their evidence; the general class's own
definition (repairs.tex:14–15, "applies a scaling law or a physical law").

**Why.** Ebert and Curry's work is, by its title, "A parameterization of ice cloud optical properties for
climate models" (references.bib lines 425–427), fitted to crystals with effective radii of 10 µm and more.
Kristjánsson and Mitchell's table gives radii of 10 µm and more only above 190 K and continues by its own trend below 180 K
(`notes/exoplasim.md`, patch 10; defect log B19), and the lunar high cloud lies at 180–204 K in the design case
and 165–217 K in the longwave test. The change replaces one simplification with a fit used partly beyond its
range. "A physical law" places it in the general class on a premise the cited work contradicts. The reach
table (reach.tex:95) bounds the optics at 180 K, the end of the radius table, while the fitted sizes end at
190 K.

**Rewrite.** "Cloud colder than $-38$\,\textdegree C is given Ebert and Curry's parameterized ice optics
\autocite{ebert1992parameterization} through a delta-scaled two-stream, with an effective radius from
Kristjánsson and Mitchell's table \autocite{kristjansson2000impact}, in place of liquid water's; the
parameterization was fitted to crystals of 10~\textmu m and larger, sizes the table gives only above 190~K, so
in the coldest lunar cloud the optics are extrapolated in size." The tables then give the change its class
with that bound.

### 35. MAJOR · repairs.tex:134–148 · "Processes and capabilities added"

**Text.** Heading "\textbf{Processes and capabilities added.}"; 142: "The lunar runs add leakage of charge
through a computed lunar conductivity column,"; 146–148: "PlaSim gains a downward infrared flux at the model
top, by day and by night, for any source above the air, a host planet's glow for a moon among them, and CM1's
radiation reads ice sizes capped at RRTMG's 140~\textmu m, with the excess logged."

**Rule.** G1 (mixed kinds, reorderable sentences); Sentences carry their dependencies (coordination of
unrelated propositions); Exact action; Claims stay within their evidence ("any source").

**Why.** The heading names capabilities; the paragraph also contains a general repair (the ice optics,
`tab:repairs` "General"), a bound (the leader's crossing) and a mitigation (the ice-size cap). The ice-optics
sentence and the last sentence trade places with no loss, and the last sentence joins PlaSim's infrared from
space and CM1's ice cap with "and". Runs add nothing; the author added the processes. The infrared flux enters
as a broadband flux whose spectrum is ignored (`notes/exoplasim.md`, patch 06), so "any source" holds for the
flux's total alone.

**Rewrite.** With the ice optics moved to the general repairs (Finding 34):

> \textbf{Processes and capabilities added.} WRF-ELEC's charge separation, discharge and screening, which CM1
> lacks, were grafted into it: the NSSL scheme with charge on every hydrometeor; a Poisson solver by Fourier
> transform across the periodic domain and a tridiagonal solve on CM1's stretched levels; WRF-ELEC's
> cylindrical discharge \autocite{ziegler1994observed} and its three-dimensional discharge adapted from
> \textcite{macgorman2001lightning}, on a domain that wraps round; and its screening layers, available and off
> in the lunar runs. For month-long lunar storms the graft was given leakage of charge through a computed lunar
> conductivity column, and a leader's crossing to the ground at an internal field of 1~kV\,m$^{-1}$ at
> sea-level density, scaled with the air's density, which places the ground strikes between the bounds set by
> WRF-ELEC's stopping field and its $-7$\,\textdegree C rule; point discharge from the ground, added as an
> option, ran in one test window and stays off. Where the graft's ice outgrows RRTMG's optics, CM1's radiation
> reads sizes capped at 140~\textmu m and logs the excess. PlaSim gains a broadband downward infrared flux at
> the model top, by day and by night, for a source above the air such as a host planet's glow on a moon.

### 36. MINOR · repairs.tex:150–151, 156–157 · the slice and what CM1 receives

**Text.** 150–151: "Running CM1 inside the GCM's climate adds a structural limit to the inherited ones:";
156–157: "The forcing methods supply what the slice lacks from the GCM's fields, and with them the GCM's
remaining Earth values."; 157: "(a box takes one)".

**Rule.** Exact action; Technical meaning survives editing; Inheritance and order.

**Why.** One "structural limit" introduces three items, and the third, stock CM1's missing lunar Sun, forcing
aloft and terrain nudging, is a gap in the code's capabilities. "The inherited ones" leaves the reader to
supply "Earth values". The sentence on the forcing gives methods an action and states the paragraph's main
consequence, that CM1 receives the GCM's own Earth values, as an elliptical tail.

**Rewrite.** "Running CM1 inside the GCM's climate adds structural limits to the Earth values the code holds:
a ring of columns along a latitude circle lacks the transport across the circle, and a box lacks any day--night
circulation larger than itself; stock CM1 also has no lunar Sun, no forcing above its boundary layer and no
nudging that follows terrain." … "CM1 receives what the slice lacks from the GCM's fields, and with those
fields the Earth values that remain in the GCM. Each ring column has its own Sun, a box one Sun for all its
columns, and on tilted rings each column has its own Coriolis parameter; …"

### 37. MINOR · repairs.tex:72, 102, 150 · run-in headings

**Text.** "\textbf{Geometry restored.}"; "\textbf{Calibration by height.}"; "\textbf{Forcing a slice of the
GCM.}"

**Rule.** Headings say what they name.

**Why.** The released codes had flat columns throughout, so "restored" misnames a geometry added for the first
time; the calibration paragraph covers the totals and the split of sunlight before the heights; the forcing
paragraph ends on SWAN and SWASH, which force no slice. ("Constants to parameters" is Finding 23.)

**Rewrite.** "\textbf{Curved air.}"; "\textbf{Calibration against the reference.}"; "\textbf{Forcing from the
GCM.}"

### 38. MINOR · statements repeated from neighbouring sections

**Text and locations.**
- repairs.tex:14–22 restates introduction.tex:58–63: the three classes, with the same members and the same
  "another world takes it unchanged".
- repairs.tex:102–107 re-describes the reference model of introduction.tex:50–53.
- assumptions.tex:51–52 and 57–59 restate worlds.tex:75–80: the widening shells, the sunlight beyond the
  horizon, the horizon factors of 13.5 and 7.1 against 35.
- assumptions.tex:44–45 restates worlds.tex:92–93: the 0.6 m thermal wave.
- repairs.tex:117–119 restates assumptions.tex:79–81: the continuum fitted to the outgoing flux.

**Rule.** G2 and the redundancy pass (repeated definitions; delete test).

**Why.** Under the delete test, each repeated sentence returns a fact the reader met a page or two earlier,
and its paragraph keeps its inference without the repetition, except where the paragraph computes with the
number.

**Rewrite.** Keep each statement in the section whose argument computes with it and refer back by figure or
table: the class definitions in repairs.tex, with the introduction reduced to the classes' names and reach (a
change outside this scope); the horizon factors and the thermal wave in assumptions.tex, with worlds.tex
keeping the ratios; at repairs.tex:117–119 the consequence alone, as in Finding 33.

## Paragraphs examined and found sound

**Sound in full.**
- repairs.tex:3–4, the rule sentence: "Most repairs follow one rule: …". The quantifier holds: by this
  review's count, about 28 of the 39 rows of `tab:repairs` follow the rule.
- repairs.tex:50–57, the fall-speed derivation after its opening sentence: the Reynolds–Best argument, the
  exponents and their numbers, the condition for exactness, and the passage of the scaled speeds into
  collection and ventilation follow one another as steps of one inference.
- repairs.tex:92–100, Figure `fig:slant` and its caption; the render agrees with the caption.
- repairs.tex:123–132, Figure `fig:layers` and its caption; the render agrees with the caption, apart from the
  layer heights of Finding 10.
- assumptions.tex:3–8, the definitions of an Earth value and of a defect, as sentences; the paragraph's later
  sentences are the subjects of Findings 1 and 2.
- The inventory itself as a form: the section's catalogue is in a table, `tab:inventory`, where AGENTS.md
  places catalogues; its row-level and class-level findings are 1, 4, 6, 7, 9 and 15.

**Sound in movement, with local findings only.**
- assumptions.tex:40–48, units of time: the calendars, then the soil, then a process a short run neglects,
  landing on the measured lunar field. Finding 7 concerns the opening definition.
- assumptions.tex:50–66, geometry: the radiation's column, the measured cost of curvature, the slant path, the
  dynamics, the grid. Findings 8–10.
- assumptions.tex:89–99, the laws of drops, seas and charge: two sentences, the second landing on the polarity
  reversal. Finding 4 concerns its first clause.
- assumptions.tex:101–128, defects: from defects whose errors vanish at Earth's values, through the two
  independent of the world, to the fault of uncertain cause, with an earned hinge at 119–120 ("The Moon's slow
  rotation and small tilt made all three large."). Findings 1, 12 and 13.
- repairs.tex:72–90, curved air: a method statement in the order of construction, ending on a qualification
  attached to the claim it bounds. Findings 27–31.
- repairs.tex:102–121, calibration: "Each calibration was made to remove the residual of the one before"
  orders the paragraph, and its opening inherits the calibration reference from the end of the paragraph
  before. Findings 32 and 33.
- repairs.tex:150–166, forcing: the limits, the runs that exposed two of them, then the remedies. Findings 36
  and 37.
- Figure `fig:sunclock` (assumptions.tex:130–140): the render agrees with the caption. Finding 14.

## Gates G1–G4 for this scope

**G1, argument and reorderability.** The constants paragraph (assumptions.tex:15–38) and the fits paragraph
(68–87) fail the swap test across their middles (Findings 3, 11). In repairs.tex, the opening paragraph
(4–12), "Constants to parameters" (37–47), the paragraph at 59–70 and "Processes and capabilities added"
(134–148) hold items in an arbitrary order, or under an announced relation that covers part of them
(Findings 16, 23, 26, 35); "Defects removed or avoided" (27–35) has an order from removal to workaround that
its syntax leaves unwritten (Finding 20). The paragraphs listed above as sound in movement each follow a
stated relation. The catalogues are in `tab:inventory` and `tab:repairs`, and the classification columns of
both tables hold the inconsistencies of Findings 1, 4, 7, 15, 18 and 19.

**G2, audience, specificity and economy.** The outside reader needs project knowledge for these repository
labels and project terms: "Patch 04" and "Patch 03" (repairs.tex:27, 29), "the guard added to the water
scaling" (11), the channel construction (75–77), "the ground's share in the column's clear share" (84), the
coined "ledger" (72) and "the correlated-k reference" ahead of its introduction (assumptions.tex:80)
(Findings 11, 16, 20, 27, 28, 30). Repeated statements: SWAN's knee three times in repairs.tex, the rebuild
claim in repairs.tex and verification.tex (Finding 23), the class definitions in the introduction and
repairs.tex, and the worlds section's geometry and thermal wave in assumptions.tex (Finding 38). Explanatory
sentences kept under the delete test: the Best-number derivation (repairs.tex:49–55), the definition of a
dimensional constant (assumptions.tex:15), and the mechanism of curved columns (assumptions.tex:51–52, with the
repetition of Finding 38).

**G3, inheritance, syntax, transitions and cadence.** Consecutive sentences open on a model's name at
assumptions.tex:15–38 and 68–87 and at repairs.tex:27–35 and 37–47 (Findings 3, 11, 20, 23). Coordination
joins unrelated propositions at repairs.tex:66–70 (cloud water and soil) and 146–148 (infrared from space and
the ice cap) (Findings 26, 35). The run-in heads mark the paragraph boundaries; at repairs.tex:88–103 one
paragraph ends on the reference PlaSim was calibrated against and the next opens on it. Landings examined:
assumptions.tex:48, 66, 87, 99 and 128 and repairs.tex:90, 121 and 166 each end on a measured consequence or
a stated status; repairs.tex:47, 70 and 148 end on an appended item (Findings 23, 26, 35). The cadence check
was a silent reading.

**G4, affirmative stance, exact action and economy.** The lexical screen found no "not" and no "rather than"
in either file (screening only). Negative contrasts judged by meaning: "without a warning"
(assumptions.tex:115) and "proved insufficient" (repairs.tex:117) have affirmative forms (Findings 12, 33);
the absences at repairs.tex:80, 151–153 and 161–162 are required by their propositions. Empty actions: "sit"
(assumptions.tex:62, 101), "takes in … lets out … return" (53–55), "takes" (repairs.tex:16), "serves" (18),
"adjusts" (19), "lies" (20), "stand" (23), "the same argument sets" (59), "restore" and "counts" (66–67),
"divide" (81) and "supply" (156) (Findings 1, 8, 9, 17, 18, 19, 26, 29, 36). Claims beyond their evidence:
"each" at assumptions.tex:11–13 and repairs.tex:11–12 and 37–38, "the remaining constants"
(assumptions.tex:34), "the air over the lunar seas" (33), "a physical law" (repairs.tex:137), "keeps output
aligned with the Sun" (31), "the eight lunar CM1 builds used for the results" (45) and "where gravity enters a
fitted law" (49) (Findings 2, 5, 16, 21, 22, 24, 25, 34). The first paragraph of repairs.tex lists its
exceptions after the claim they qualify, a caveat list in the place of the table that already marks them
(Finding 16). People: ExoPlaSim's developers made the replacement that assumptions.tex:110–111 credits to
"ExoPlaSim's replacement" (Finding 12), and the author's additions appear as actions of "the lunar runs"
(repairs.tex:142, Finding 35).
