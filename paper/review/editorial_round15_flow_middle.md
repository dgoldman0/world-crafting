# Editorial round 15: flow check of Repairs, Verification and Results

## Record

- **Reviewer:** a fresh Claude subagent (Claude Opus 5.5). Earlier review records of the paper stayed unread,
  apart from the review folder's README for its conventions.
- **Date:** 2026-10-18.
- **Snapshot:** commit 64d04e0 (64d04e0da70643d3ecc29ab919468c5c5ad56150), working tree clean; 64d04e0 was later
  reworded as 2800b68, the same tree, under AGENTS.md's rule on quoting the author in commit messages. No file
  outside this record was changed, and no build was run.
- **Files in scope** (`sha256sum` at the snapshot):

  | File | sha256 |
  |---|---|
  | `paper/sections/repairs.tex` | `c846dbbf4dbaf39ae194d7bb93a26204aaa1b12f4b24e7aa1accdd948b281102` |
  | `paper/sections/verification.tex` | `4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00` |
  | `paper/sections/results.tex` | `4e3092cca7678c663a334798b95942ec93d04f193c5799e57b91fafe60c8daba` |

- **The check:** flow alone, judged first against the author's direction of 18 October 2026 and then against
  AGENTS.md. The direction, in the author's words: "Remember I hate paratactic style in the academic papers I
  craft and I generally hate when paragraphs in them are just a bullet point set of information chained together
  pretending to be paragraphs." "A stock signpost is a stock signpost. "Moreover" and similar used appropriately
  to move from one thought to the next and keep flow is fine." And, on a drafted pair of sentences: "The second
  issue does not directly stem from the first issue, does it? No. So we cannot just tack on that next sentence as
  if it does." The prose was read; table bodies were skipped; word choice, negation, verbs, numbers, facts,
  citations and captions were left aside.
- **What I read:**
  - `AGENTS.md`, section "Writing" as of 64d04e0, with that commit's diff to it ("Sentences carry
    their dependencies", "Inheritance and order").
  - The four sources AGENTS.md names, in full: Terluna's charter
    (`ensemble/planning/Open_Moon_Editorial_Charter_control-01.md`) and its three style notes
    (`STYLE_NOTES.md`, `Jewish_Papers_Updated_Style_Notes.md`, `Agent_Working_State_Editorial_Gates.md`).
  - `paper/main.tex`, for the order of sections.
  - The three sections in scope, whole, then paragraph by paragraph.
  - The neighbours, whole: `assumptions.tex` (before Repairs) and `reach.tex` (after Results), for the
    transitions in and out; `introduction.tex`, where the classes of repair that Repairs refers back to are
    first set out.
  - `appendix.tex`, Tables `tab:repairs` and `tab:verification`, which the prose in scope cites.
  - `paper/claims.json`, the entries for the `\claim{}` markers in scope, so that each marker in a sample rewrite
    stays with the sentence that holds its content.
- **Method:** each section was read whole, then each paragraph with an inheritance trace and the swap test. The
  reading was silent. Two scratch scripts served as screens: one printed the opening words of every sentence by
  paragraph, to confirm subject restarts; the other compared the numbers, citations, references, `\code{}`,
  inline mathematics and `\claim{}` markers of each original passage with its sample rewrite. Every token
  survives in every rewrite; the only added token is a further mention of CM1. `paper/tools/lint.py` was left
  unrun: it has no screen for parataxis, and its "stock transition" pattern still lists "Moreover", "In
  addition" and "However", which AGENTS.md at 64d04e0 admits where they move the reader on, so its hits on those
  words are screening at most.

## How to read the findings

- **Kinds:** 1, a paratactic run; 2, a paragraph of facts chained like bullet points; 3, an unmarked turn (a new
  point set as though it followed, or a contrast or concession with no word to mark it); 4, a missing or abrupt
  transition between paragraphs or at a section's opening; 5, over-compression, including semicolon chains of
  loosely related clauses.
- **Severity:** MAJOR, a paragraph or a run of three or more sentences that reads as a list; MINOR, one unmarked
  relation.
- **Sample rewrites** keep every claim, number, condition, citation and `\claim{}` marker of their passage (checked
  by script, as above). They are samples: the author may word each transition differently. Where a rewrite moves
  a sentence or a marker, the finding says so, and where it writes a relation that the evidence could read two
  ways, the finding flags it for the author.
- **Run-in headings.** In Repairs and Verification the bold headings mark most transitions between paragraphs.
  A heading-only transition is reported where the prose also lacks an antecedent or the paragraph is placed apart
  from the one it elaborates; the others pass.

## Findings

### Repairs (`paper/sections/repairs.tex`)

**1. repairs.tex:7–9 · MINOR · kind 3.** "The source changes are recorded as patch series … are listed with them."
The sentence turns from the rule and its exceptions to the record of every change, an addition that reads as a
further clause of the rule; mark it as covering both kinds ("Both kinds of change are recorded as patch series
…"), or move it into the Switches-and-builds paragraph, which takes up the same record (finding 4).

**2. repairs.tex:11–27 · MAJOR · kinds 2, 3, 4.** "The three classes of repair differ … a cap on what one scheme
passes to another."

The paragraph opens on "the three classes" with no bridge from the switch rule of lines 3–9, which sorts the same
changes on another axis. Lines 11–16 then set the three definitions side by side, each sentence restarting on its
class ("A general repair", "A general method", "In a calibration"), and the comparison named in the topic
sentence, along what was fitted, is left for the reader to draw. Line 20 turns to a second convention, the line
between a repair and its setting, as if it followed from the gas-band case. Read through, the paragraph is a
definition series followed by a catalogue; the catalogue of lines 23–27 is genuine and stays.

```latex
Where that rule concerns how a change is switched, the three classes of repair differ in what was fitted to the
test world. A general repair contains no coefficient fitted to the test world or chosen for it, since its values
follow from a unit, a scaling law, a parameterization fitted over a stated range or the code's own intent, and its
limits are therefore those of its laws (Table~\ref{tab:reach}). One step nearer the world, a general method
computes a quantity of the world's own column offline and enters it as computed, as the curved-air terms enter as
differences between spherical and flat solutions of a design column. In a calibration, by contrast, PlaSim's own
coefficients are adjusted until its output matches the reference model on chosen columns of the test world. The
gas-band change has a part of each of these last two kinds: its coefficients were fitted to the reference beam's
loss above every level of the design column, a quantity computed for that column, and the Rayleigh and water
multipliers were then refitted with them until PlaSim's layers matched the reference, so the tables class it as a
calibration. A second convention separates a repair from its setting: the code change that turns an Earth value
into a parameter is counted as the repair and the lunar value entered in it as a setting, so CM1's gravity, Sun,
carbon dioxide and oxygen are general repairs with lunar settings, while CM1's zeroed trace gases and ozone and
SWAN's air density, entered as fixed values in the code, are settings alone. Beyond the three classes and the
settings, the remaining kinds of change are a capability, a process the released codes lack; a coupling, the use of
one model's fields to force another; an avoidance, a configuration of a released code chosen to keep the runs clear
of a defect or an Earth default; a bound, a value chosen between two rules that bracket an unsettled process; and a
mitigation, a cap on what one scheme passes to another.
```

**3. repairs.tex:29–42 · MAJOR · kinds 2, 3, 5.** "Two of ExoPlaSim's defects are removed in the code … reported to
ExoPlaSim's developers \autocite{goldman2026solang}."

After the two removals and the one avoidance (lines 29–33), four sentences each start a new item with its relation
unwritten: the calendar (line 33), SWAN's two avoidances (line 36), the two faults left open (line 38), and the
range of configurations the three ExoPlaSim repairs are built for (line 39), which belongs beside lines 29–33; the
swap test moves it there with no loss. Within lines 33–35 a semicolon leaves a concession unmarked (the means fall
at the same places every year, yet the synodic Sun shifts against them), and the semicolon at line 41 attaches the
report to ExoPlaSim's developers to that range. The rewrite brings the range up beside the ExoPlaSim repairs,
groups the avoidances by configuration, and marks the open faults as the contrast.

```latex
Two of ExoPlaSim's defects are removed in the code: the patched PlaSim turns the Sun at the synodic rate
continuously from the first step, a mode that assumes a steady, non-synchronous rotation, and converts convective
rain per 86,400~s. The third is avoided with ExoPlaSim's own \code{fixedorbit} switch, whose documentation
describes only the freezing of Milankovitch variations; set, it makes PlaSim use the configured orbit. These three
ExoPlaSim repairs are built for other configurations of the released code as well, the synodic clock for any
steady, non-synchronous rotation, the unit for any model day, a synchronous one included, and the switch for any
configured orbit, and the Sun clock has been reported to ExoPlaSim's developers \autocite{goldman2026solang}. The
calendar's slip is avoided by configuration in the same way: with a year of 17,160 half-hour steps, twelve whole
model days, the ten output means of each model day fall at the same places in every year, although the synodic Sun
still shifts 3.2\textdegree\ a model day against those means, so analyses sort the output by the Sun's position.
SWAN's defect and Earth default are likewise avoided by configuration, its uninitialised read of its breaker
parameter by keeping depth-induced breaking on in every run, and its default initial state, whose 2~s peak period
has Earth's dimensions, by starting from rest or from hotstart files. Two faults, however, stay open, the thread
race and PlaSim's cold lowest level, so CM1 runs that must repeat use one thread, and analyses of the lowest level
screen the cold windows.
```

**4. repairs.tex:44–52 · MAJOR · kinds 2, 4.** "The lunar runs were made with runners … generated from the runners'
edit lists.\claim{R01}"

Four sentences on four subjects (the runners, PlaSim's ten patches, CM1's constants and spare reals, the patch
series); the last returns to the runners' edit lists of the first after two sentences on other matters, and at line
47 "and" joins a confirmation to an exception. The paragraph is also placed apart from the one it elaborates: lines
3–9 state the switch rule and the patch-series record, while this paragraph follows the report to ExoPlaSim's
developers and opens with no bridge from it. Repair: place it directly after lines 3–9, fold the record sentence of
lines 7–9 into it, and write the relations.

```latex
The lunar runs were made with runners, scripts that configure, compile and run each model and insert each change
into the installed source at a marked anchor, and the patch series in the code repository were generated from the
runners' edit lists. In PlaSim the inserted changes are ten patches to its radiation, cloud and Sun code, each
adding a namelist switch written to reproduce the released code at its default; runs confirm that identity for five
of them (Table~\ref{tab:verification}), while the near-infrared water scaling reproduces the released code at its
default only for spectra like the design case's. CM1 takes its switches in two other forms: gravity and the air's
carbon dioxide and oxygen become preprocessor constants that default to 9.81~m\,s$^{-2}$, 400~ppm and Earth's
oxygen, and CM1's twenty spare namelist reals hold the lunar Sun, the forcing and the electrification's
settings.\claim{R01}
```

**5. repairs.tex:54–55 · MINOR · kind 5.** "In the fall-speed laws gravity enters … follows from a similarity
argument." Cause and consequence joined by "and"; write "Because gravity enters the fall-speed laws through the
balance of weight and drag, the repair follows from a similarity argument."

**6. repairs.tex:58–61 · MINOR · kind 5.** "The scaling is exact for particles … than the patch gives them." A
contrast set after a semicolon (exact for drops, graupel and hail; a larger exponent for snow and ice crystals);
mark it with "whereas".

**7. repairs.tex:61–69 · MAJOR · kinds 1, 3.** "The Morrison and NSSL schemes pass … restores the model's gravity
similarity.\claim{R04}"

After the fall-speed argument, three sentences each open on a different code (the microphysics schemes, CM1's
damping with WRF-ELEC's sub-step, SWAN), and the two turns between them go unmarked: from the particles to the
stretched dynamics at line 62, and from the storm model to the wave model at line 67. Within them, "and" at line
62 joins the NSSL exception as a plain addition, and the semicolon at line 66 leaves a concession unmarked (6.8 s
computed, 8 s run).

```latex
The Morrison and NSSL schemes pass the scaled speeds through their fall-speed laws and caps into collection and
ventilation, although in NSSL the ventilation needed its own scaling at eleven sites. Beyond the microphysics, the
repairs follow the sixfold stretch of the dry dynamics: CM1's Rayleigh damping rate and its boundary-layer length are
scaled by $g/g_\mathrm{E}$ and $g_\mathrm{E}/g$, and WRF-ELEC's sub-step lengthens from 0.75 to 6.8~s, so that
graupel settles through about 1\% of a layer per sub-step in the 2~km layers of the lunar charging zone, at 0.44 of
Earth's fall speed, though the boxes, rounding to whole sub-steps, run one 8~s sub-step per model step.\claim{R03}
SWAN's repair is a similarity scaling as well: the reduction above the knee takes $f\,g_\mathrm{E}/g$ in place of
$f$, which moves the knee to $g/g_\mathrm{E}$~Hz, reproduces stock SWAN at standard gravity and restores the model's
gravity similarity.\claim{R04}
```

**8. repairs.tex:71–85 · MAJOR · kind 2.** "Other general repairs remove an Earth value directly. … the optics are
extrapolated in size.\claim{R12}"

Six sentences hold seven repairs in three codes, in the order CM1 (gravity and Sun), WRF-ELEC, PlaSim, CM1,
WRF-ELEC, PlaSim; each sentence restarts on its own subject, and any two can trade places with no loss. The soil
(line 77) belongs with the Sun (line 72), whose day it follows; the flash log (line 78) with the breakdown cap
(line 74); the cloud water (line 75) with the ice optics (line 80). The closing semicolon (line 83) leaves a
concession about the ice optics' fitted range unmarked. The rewrite groups the repairs by code and writes the link
inside each group; `\claim{R16}`, which covers the soil, the cloud water and the flash log, moves to the last of
the three. Since Table `tab:repairs` already lists all seven, a shorter paragraph that keeps only what the table
lacks would serve as well.

```latex
Other general repairs remove an Earth value directly. CM1's gravity becomes one build constant for its dynamics, its
radiation, its CAPE diagnostic and both microphysics schemes, and its Sun follows a solar day, a flux and a starting
hour angle read from spare namelist reals, with each column of a ring at its own longitude; to match that Sun, CM1's
five soil layers are thickened to 5--80~cm, 1.55~m in all, so that they reach below the thermal wave of any solar
day from a few Earth days to the Moon's. In the electrification grafted into CM1, two limits set at Earth's values
are removed: lifting WRF-ELEC's 180~kV\,m$^{-1}$ cap lets the breakdown field's scaling with the air's density act
wherever flashes start, however dense the air there, and in the patched graft the flash log records each channel's
reach from the charge the flash hands to the ions, where the released code recorded it only above a charge threshold
set for Earth's storms. Two more concern PlaSim's cloud. The patched CCM3 formula counts heights and precipitable
water at Earth's gravity and scales the mixing ratio by $g/g_\mathrm{E}$, which gives each cloud the water path it
would hold at the same pressures on Earth,\claim{R16} while cloud colder than $-38$\,\textdegree C is given Ebert
and Curry's parameterized ice optics \autocite{ebert1992parameterization} through a delta-scaled two-stream, with an
effective radius from Kristjánsson and Mitchell's table \autocite{kristjansson2000impact}, in place of liquid
water's. The parameterization was, however, fitted to crystals of 10~\textmu m and larger, sizes the table gives
only above 190~K, so in the coldest lunar cloud the optics are extrapolated in size.\claim{R12}
```

**9. repairs.tex:87–90 · MINOR · kind 4.** "Both models read the curved geometry … with the differences tabulated."
The paragraph moves from the general repairs to the general method with the heading as its only bridge, and "Both
models" has no antecedent in the paragraph before, which treats CM1, the graft and PlaSim; name the class and the
models, e.g. "The general method serves the two atmospheric models: PlaSim and CM1 read the curved geometry from a
table …".

**10. repairs.tex:93–94 · MINOR · kind 5.** "…so that their twilight lacks scattered light; the infrared escape …
gives the channels' construction." The semicolon sets the infrared beside the sunlight as a parallel step, and "and
the appendix gives …" attaches a pointer about the channels to the infrared clause; mark the parallel ("The
infrared escape, for its part, was traced …") and move the pointer next to "10,697 spectral channels".

**11. repairs.tex:100–109 · MAJOR · kinds 1, 3.** "PlaSim's slant factor becomes the Moon's … 3\% of its radius
\autocite{vincendon2010spherical}."

After the terms are applied (lines 96–100), four sentences add items with their relations unwritten: the slant
factor (from the same shells), the solver difference inside the terms (a concession about lines 96–100, placed
after the slant factor so that it reads as a comment on it), the recomputation for another world, and the Mars and
Titan limits, whose bearing on that recomputation is left to the reader.

```latex
Fitted to straight rays through the same shells, PlaSim's slant factor becomes the Moon's,
$(\mu+a)/(\mu^2+b\mu+c)$, within 0.30\% for water vapour and 0.08\% for well-mixed air
(Figure~\ref{fig:slant}).\claim{R06} The daytime terms, however, include a difference of solvers as well as of
geometry: with the Sun overhead, where curvature leaves the beam's path unchanged, the spherical solver's ground
still receives 1.3\% less sunlight than the two-stream's, so by day the terms also move PlaSim from the two-stream
reference it was calibrated against toward the successive-orders solver.\claim{R07} Since the table is computed for
one column, for another world it is recomputed from that world's own column, and how close to the horizon a flat
treatment holds there depends on the height of the scattering layer against the radius: the plane-parallel codes
that separate surface and aerosol in remote sensing hold typically to about 80\textdegree\ from the zenith on Mars,
and to about 65\textdegree\ on Titan, whose haze has a scale height of about 80~km, 3\% of its radius
\autocite{vincendon2010spherical}.
```

**12. repairs.tex:133–135 · MINOR · kind 3.** "Three carbon dioxide and oxygen bands … from 1.71
(Figure~\ref{fig:layers})." The third step of a sequence the paragraph numbers ("The first", "The second") opens
on a new subject after the shortfall it remedies; mark it, e.g. "In a third step, three carbon dioxide and oxygen
bands … brought the layers …".

**13. repairs.tex:135–140 · MINOR · kinds 3, 5.** "In the longwave, the first calibration had fitted … only in the
longwave test.\claim{R11}" The extra escape remedies the misplaced cooling yet enters as a fresh subject, and the
closing semicolon attaches a restriction; open with the purpose ("To place that cooling by layer, an extra escape
…") and close with "although it runs only in the longwave test".

**14. repairs.tex:159–162 · MINOR · kind 5.** "For runs that last weeks, the graft was given leakage … scaled with
the air's density." By its syntax the purpose phrase "For runs that last weeks" governs both additions, yet it fits
the leakage alone; the condition for ground strikes has a reason of its own, the lunar heights of WRF-ELEC's two
Earth rules (line 163). Give the condition a clause of its own that states that reason.

**15. repairs.tex:162–168 · MAJOR · kinds 2, 3.** "The condition places the ground strikes … such as a giant host
planet's glow on a moon."

Point discharge, a further capability, is attached by a semicolon to the bound (line 164); the ice-size cap, a
mitigation (line 165), and PlaSim's infrared from above, a capability in the other model (line 166), follow as
separate sentences, each on a new subject, so the paragraph ends on three appended items.

```latex
The condition places the ground strikes between WRF-ELEC's two Earth rules, its stopping field, under which every
lunar channel stops 15--25~km up, and its $-7$\,\textdegree C rule alone. Point discharge from the ground was added to
the graft as well, as an option, and after running in one test window it stays off.\claim{R13} The graft's ice needed
a mitigation: where it outgrows RRTMG's optics, CM1's radiation reads sizes capped at 140~\textmu m and logs the
excess. PlaSim, too, is given a capability, a broadband downward infrared flux at the model top, by day and by night,
for a source above the air, such as a giant host planet's glow on a moon.
```

**16. repairs.tex:176–188 · MAJOR · kinds 2, 3, 5.** "CM1 receives what the slice lacks … built for a slice of any
world's GCM."

Lines 170–172 name five absences, two structural and three in stock CM1, and lines 177–183 supply the forcing in an
order different from theirs: the Sun, the Coriolis parameter, the nudging and the vertical wind in one
semicolon chain, then the heating and moistening that fills the two structural absences, then the terrain nudging
after another semicolon. SWAN and SWASH (line 183) follow with no marker of the turn from the storm model to the
waves, and the last sentence joins a cause and its consequence with "and". The rewrite takes the absences in the
order lines 170–172 name them.

```latex
CM1 receives what the slice lacks from the GCM's fields, and with those fields the Earth values that remain in the
GCM. For the two structural absences, a heating and moistening by local time and height, taken from the GCM, imposes
the effect of the day--night circulation a box lacks and, as a single local-time bin, of the transport across the
circle a ring lacks. The absences of stock CM1 are filled from the same fields: each ring column has its own Sun, a
box one Sun for all its columns, and on tilted rings each column has its own Coriolis parameter, acting on departures
from the base-state wind; CM1 is nudged toward the GCM only above 8--16~km, so that its boundary layer and convection
develop freely, and the GCM's mean vertical wind enters CM1's own large-scale advection; and over terrain each column
is nudged and forced at its own height above sea level.\claim{R14} The seas are forced from the GCM's surface: SWAN is
forced by the GCM's surface stress, converted through Wu's drag law inverted to an equivalent wind, so that its
friction velocity lies within $-2.5$ to $+1.2$\% of the GCM's, on spherical coordinates at the lunar radius and with
its frequency band scaled by $g/g_\mathrm{E}$, and SWASH, run unmodified, takes lunar gravity as an input and SWAN's
spectra at its boundary.\claim{R15} Since the methods impose only the GCM's fields and the slice's geometry, they are
built for a slice of any world's GCM.
```

### Verification (`paper/sections/verification.tex`)

**17. verification.tex:3 · MINOR · kind 4.** "Six kinds of check were made, in three steps of distance from the
code (Table~\ref{tab:verification})." Repairs closes on the slice methods built for any world's GCM, and
Verification opens on "the code" with no word on which code was checked; a clause naming the repaired codes would
bridge, e.g. "The repaired codes were checked in six kinds of check, in three steps of distance from the code …".

**18. verification.tex:4–11 · MINOR · kind 1.** "Identity and reproduction checks test the code alone … a scheme's
published behaviour on Earth." The three steps are set out as three parallel sentences, their order of distance
stated only in the predicates ("alone", "against a formula …", "outside it"), while lines 11 and 13 refer back to
"the first two steps" and "the third step", which the sentences leave unnumbered; mark the order ("In the first
step …; in the second …; the third, …"). Held to MINOR because the topic sentence sets the scale and lines 11–15
draw a consequence from it.

**19. verification.tex:11–13 · MINOR · kind 3.** "The checks of the first two steps concern … which it leaves
untested there." A concession joined by "and"; mark it with "although" ("…that hold on any world, although a
similarity test runs Earth's empirical laws …").

**20. verification.tex:20–21 · MINOR · kind 3.** "The infrared and ice-optics runs were compared against builds …"
A contrast with the first three runs, which link back to the release in sequence; mark it with "by contrast" or
"whereas".

**21. verification.tex:24–26 · MINOR · kind 5.** "…so the chain from these two checks … arithmetic on this
spectrum.\claim{V01}" The water scaling is an exception to the open chain, yet "and" adds it as a further step;
mark the contrast with "while" ("…closes once they are, while for the water scaling at its default the identity
already follows from arithmetic on this spectrum").

**22. verification.tex:26–37 · MAJOR · kinds 2, 3.** "Applied to the pinned upstream archives, the patch series
rebuild … the other CM1 and SWAN identity checks.\claim{V02}\claim{H26}"

The paragraph takes the three checks that lines 4–6 list in turn, yet marks neither move between them: line 26
opens the rebuilding of the sources with no sign that a second kind of check begins, and line 33 opens the
restarts the same way. From line 33, three sentences restart on new subjects (a GCM year, runs of CM1, the table),
and the GCM restart and the CM1 repeats can trade places with no loss; the semicolon at line 35 leaves
unmarked the contrast between runs that repeat and threaded boxes that part.

```latex
The recorded sources were checked next, against the pinned upstream archives: applied to them, the patch series
rebuild byte for byte the two patched sources of the deployed ExoPlaSim copy and the Fortran of the lunar CM1 builds
behind the results, eight rebuilt directly and the 45\textdegree\,N rings' build through sources identical to one of
them, while the Earth-gravity benchmark builds were compiled from earlier states of the runners' edit lists. The GCM
runs are traced to the same series through their source hashes: prefixes of the ExoPlaSim series reproduce the
source hashes of 32 of the 34 GCM runs that recorded one; of the states in Table~\ref{tab:states}, the uncalibrated
and first calibrated runs predate source hashing, and the convective-cover run compiled a draft of its patch whose
committed form repeats its first year byte for byte.\claim{V03} In the last kind of check the runs themselves are
restarted or repeated: a GCM year killed a minute in and resumed repeats the uninterrupted year's restart and every
variable of its output, runs of CM1 repeat bit for bit on one thread, and the Earth supercell, restarted on four
threads and on two, repeats its fields and its 41 flashes. In the lunar boxes, however, which ran on several threads,
runs part from one another after 3,000--7,400~s, so each box run is one realisation. Table~\ref{tab:verification}
lists the other CM1 and SWAN identity checks.\claim{V02}\claim{H26}
```

**23. verification.tex:39–41 · MINOR · kind 1.** "Gravity is the parameter of a sea … checks a wave model's gravity
numerically." A consequence left between two declaratives; write it with "so" ("…varied the air's density and the
wind \autocite{banfield2015winds}, so a wave model's gravity is checked numerically, by a similarity test").

**24. verification.tex:44–47 · MINOR · kind 3.** "SWASH reproduces the linear dispersion relation … run-up by
1.20\%.\claim{V05}" The second wave model's tests follow SWAN's as a parallel with no marker; mark it, e.g. "SWASH,
the model of the shore, was tested against theory and by the same scaling: it reproduces …".

**25. verification.tex:49–51 · MINOR · kind 5.** "…a lunar wave run is an Earth run scaled in gravity with Earth's
coefficients; the lunar runs' spherical grids … left unchecked." A limit set after a semicolon; mark the concession
with "while" (", while the lunar runs' spherical grids …").

**26. verification.tex:52–55 · MINOR · kind 3.** "In the arithmetic checks four implementations were compared … at
1.0000.\claim{V11}" The turn from the similarity tests, which end on CM1's untested microphysics, to the arithmetic
checks is unmarked; open it as the paragraph's second subject, e.g. "The arithmetic checks, the other half of this
step, compared four implementations …".

**27. verification.tex:60–69 · MAJOR · kinds 1, 3, 5.** "The refit with the gas bands and the longwave correction …
compared with an independent code.\claim{V16}"

After the one calibration tested beyond its fit, four sentences set limits side by side: the two calibrations known
through their residuals (a contrast left unmarked), a three-clause sentence of general limits whose first two
clauses are cause and consequence (clear-sky, so the clouds stay uncalibrated), the reference's checks, and
the reference's unchecked parts (a second contrast left unmarked). Read together they form a caveat list. The
rewrite writes the two contrasts and the cause, and makes the reference's accuracy the hinge into its checks.

```latex
The refit with the gas bands and the longwave correction, by contrast, are known through their fit residuals
(Table~\ref{tab:verification}). Whatever its test, every calibration is clear-sky, so PlaSim's clouds remain
uncalibrated, and the accuracy of each is bounded by the reference's own. That accuracy has been checked in part: the
reference's correlated-$k$ emulation reproduces the line-by-line outgoing longwave within 0.4--1.4~W\,m$^{-2}$, and
the line-by-line model has two recorded checks against other codes, kept as numbers alone, with their harness outside
the repository: PyRADS \autocite{koll2018earth}, for longwave with water vapour alone at constant gravity, and a Monte
Carlo calculation of Rayleigh scattering up to an optical depth of 1.5, where the lunar column's Rayleigh depth is
about 4 at 360~nm. Its carbon dioxide, oxygen, collision-induced absorption and sunlight on the lunar column, however,
have yet to be compared with an independent code.\claim{V16}
```

**28. verification.tex:75–87 · MAJOR · kinds 1, 3.** "In the Weisman--Klemp supercell … within 2--8\% from 5 to
30~km.\claim{V11}"

Each sentence pairs an agreement with a difference and leaves the turn unmarked ("and its hail differs", "; with
WRF-ELEC's ground rule on, 1.1\%"); the faster charging (line 82) is set as a fresh declarative after the agreement
it qualifies; and the conductivity benchmark (line 84) opens a separate test with no marker.

```latex
In the Weisman--Klemp supercell \autocite{weisman1982dependence} the electrified graft stays within 6\% of CM1's own
NSSL scheme in its largest updrafts, within 3.4~dBZ in reflectivity at every half hour and within 9\% in condensate,
although its hail differs by up to a factor of two, the two copies being different versions of the
scheme.\claim{V09} Set beside published runs of the same charging and lightning schemes
\autocite{macgorman2001lightning,kuhlman2006numerically,sun2023aerosol,salinas2021modeling}, the storm flashes first
at 28.5 minutes, where those runs flash first at 27--40 minutes, and its flash rates and median charge per flash fall
inside their ranges, while with WRF-ELEC's ground rule on, 1.1\% of its flashes strike the ground, against 0.33\% in
the run of \textcite{salinas2021modeling}. The storm does, however, separate charge several times faster than the
published storms, a difference traced to cloud ice reaching $2\times10^8$ crystals per kilogram where droplets freeze
homogeneously in 50~m\,s$^{-1}$ updrafts.\claim{V10} The leakage added for the lunar runs has an Earth benchmark of
its own: in the lunar runs the code leaks charge through a conductivity column whose ion chain, run for Earth at a
geomagnetic cutoff rigidity of 3~GV, reproduces Earth's measured fair-weather positive conductivity
\autocite{nicoll2012measurements} within 2--8\% from 5 to 30~km.\claim{V11}
```

**29. verification.tex:96–107 · MAJOR · kind 2.** "Four remain in reported runs. The first channels … falls below
what the pair resolves.\claim{H31}"

A genuine catalogue set as a paragraph: the four remaining defects follow as four sentences, each on its own
subject, in an order the prose leaves unexplained. AGENTS.md puts a genuine catalogue in a list or a table, and the
author's direction excludes facts chained into a paragraph, so two repairs serve: set the four as a list, or write
the order that governs them. The rewrite does the second; the original order already runs from whole sets of runs
to single comparisons, and the rewrite names that order.

```latex
Four remain in reported runs, two of them across whole sets of runs. The first channels of the curved-air table,
bisected on the whole column alone, put near-infrared sunlight too high, 19.0 against 10.7~W\,m$^{-2}$ at 66--85~km,
and the curved-air and gas-band runs of Table~\ref{tab:states} ran on them.\claim{H30} Every CM1 case set up before
2026-10-17, and so every CM1 run reported here, started from soundings that held the vapour of the GCM's top level,
near 130~km, constant above it, and on the 45\textdegree\,N rings, the only cases examined for it, the air began 6--15
times saturated over ice at 140--150~km and every column kept 1.1~g\,m$^{-2}$ of ice above 107~km through both lunar
days. The other two bear on single comparisons. The first lunar gravity patch scaled the NSSL fall speeds and left
the ventilation tied to them at Earth's values, so that lunar rain evaporated 1.3--1.5 times too fast for its size,
and a code review found the omission after the windows of the storm results that compare charging laws had run,
though before the main electrified run began.\claim{H29} Likewise, the 45\textdegree\,N rings with and without the
curved-air terms ran on builds compiled at different optimisation levels, so their 0.013--0.021~K difference falls
below what the pair resolves.\claim{H31}
```

**30. verification.tex:109–121 · MAJOR · kinds 2, 4.** "Three of the five shortfalls concern reported results. …
taken up with the next steps."

The paragraph opens on "the five shortfalls" with no antecedent, then sets the three that concern reported results
in three sentences, one per model (SWAN, SWASH, CM1), each restarting on its subject with no relation to the others
written. The two traced or bounded shortfalls (line 117) form a genuine catalogue after a colon and can stay. As
with finding 29, a list would serve; the rewrite orders the three along the chain from sea to shore to storm.

```latex
Five checks fell short, and three of the five shortfalls concern reported results, two of them along the wave chain
from the open sea to the shore. SWAN's early growth depends on the time step: halving it changes the first hours' wave
height by up to 33\%, while the 48-hour endpoints move under 0.3\%, and in the weather runs small seas fail their 5\%
time-step criterion where seas above 1~m pass, so the step's error lies in the sea states below 1~m. At the shore,
SWASH's control with irregular input, the kind of input from which the run-up was computed, misses its 5\% bound, at
5.22\% in height and 6.28\% in period.\claim{V12} The third shortfall is CM1's: rebuilt at a higher optimisation,
CM1 departs from its first build by 0.28--0.32~\textdegree C rms in the air at 2~m within a model day, inside the
spread of last-bit nudges, and since runs on several threads part from one another as well, two box runs that differ
in one setting compare as realisations. The other two shortfalls were traced or bounded: SWAN with depth breaking off
failed its repeatability test by about 2.5\%, a failure traced to the uninitialised breaker parameter and avoided in
every run by keeping breaking on, and the curved-air table's scattering orders reached their cap in one channel of
282, whose omitted tail is about $3\times10^{-4}$ of that channel's diffuse light at the ground.\claim{V13} The checks
still open are taken up with the next steps.
```

### Results (`paper/sections/results.tex`)

**31. results.tex:3–6 · MINOR · kind 4.** "The test world's results are of two kinds … each CM1 and wave result."
Verification ends on the checks left for the next steps, and Results opens with no bridge from the checked codes to
what they computed; a clause would supply it, e.g. "Run with these repairs, the codes gave results of two kinds
on the test world: …".

**32. results.tex:44 · MINOR · kind 4.** "From the Earth-orbit state, four changes were made in one step: …" The
chain of states jumps from the cloud repairs on the first calibrated run to the Earth-orbit state, which holds both
of them with new seas and sunlight (Table `tab:states`); a relative clause would mark the step, e.g. "From the
Earth-orbit state, which holds both cloud repairs, four changes were made …".

**33. results.tex:46–49 · MINOR · kind 5.** "Together they warmed the test world by 0.6~K … summer rain had reached
60\textdegree." A run of "and" holds a comparison (36\% with the Sun and tilt alone) and a cause (with Earth's
tilt, summer rain had reached 60°); mark both, e.g. "…grew from 9 to 42\%, and to 36\% with the Sun and tilt alone
in a two-year test, since with Earth's 23.7° tilt summer rain had reached 60°".

**34. results.tex:77–99 · MAJOR · kinds 3, 4.** "Changing two of PlaSim's Earth-tuned cloud settings … the
reference model and an independent GCM."

The longwave test (line 82) enters after the cloud settings as a new subject with no marker; the ranking (line 87)
then receives nothing from it, passing over the 11.5 K just reported; and the comparison of
\textcite{yang2023cloud} (line 91) opens with no bridge to the test world, its bearing on the cloud amount clear
only in the last sentence. The longwave sentence and the Yang et al. comparison can trade places with no loss. The
rewrite moves the ranking up to follow the cloud tests, bridges into the comparison, and places the longwave test
just before the closing sentence, which names cloud amount and cooling height in that order.

```latex
Changing two of PlaSim's Earth-tuned cloud settings from the Sun-and-tilt run, each to an end chosen to test an
explanation of the gap between the models, moves the global mean as far as the general repairs do or further:
counting convective cover per 2,400~s, which holds the convective cloud near its floor, warms the test world by
1.7~K over the years averaged and about 2.2~K as the run settles, and lowering the lowest layer's cloud threshold
from 0.983 to 0.6 cools it by 5.0~K and about 5.9~K, while cloud water at its full-column bound cools the first
calibrated run by 3.2~K and about 3.5~K.\claim{G05}\claim{G16} Ranked by form, then, the largest effects on the test
world came from the fits: the first calibration of the radiation's fits, used beyond the range they were fitted
over, moved the global mean by at least 20~K, and the cloud's Earth-tuned settings, pushed to the ends of these
tests, by up to about 6~K, while the two general repairs of units and constants measured singly moved it by
1.6--2.5~K and the geometry's curved-air terms, on the table's first channels, by 0.65~K. Parameterized and resolved
cloud have been set side by side on other worlds: \textcite{yang2023cloud} compared the cover of two GCMs that
parameterize it, as PlaSim does, with resolved cloud on two tidally locked planets, TRAPPIST-1e and K2-72e: CAM3
covered 94.8 and 81.7\% of the sky and ExoCAM 90.4 and 97.4\%, their cover following relative humidity, stability
and large-scale ascent, against 26.9 and 41.1\% in a quasi-global cloud-permitting model, which counts cloud by a
condensate threshold and ran over sea surfaces fixed from a coarser run of the same model. The planetary albedos lay
closer, however, 22.1--29.1 and 39.0--47.0\% in the GCMs against 18.1 and 37.4\%, and the authors judged the three
models' climates broadly similar. A test of the cooling by height moves the global mean more than any cloud setting:
the longwave correction with the ice optics, a calibration and a general repair switched on together and the one
change that moves the cooling by height, warms the design case by 11.5~K over years 10--19, toward a balance near
307~K, a sensitivity reached with a correction fitted at 295~K, with the warmer run's water vapour over years 15--19
twice the design case's, 348 against 170~kg\,m$^{-2}$, and its cloud covering 38\% of the sky in place of 20\%, most
of the gain in high cloud.\claim{G05} Given the reference's spectroscopy and these tests, the test world's climate is
least certain in its cloud amount and in the height at which its longwave cools the air, both set by Earth fits open
to constraint by cloud-resolving runs, the reference model and an independent GCM.
```

**35. results.tex:105–109 · MINOR · kinds 3, 5.** "…at the ring's estimated sensitivity of 4~W\,m$^{-2}$ per
kelvin; the ice that the ring's starting sounding left above 107~km adds a term still unquantified." A third term,
after "Two further terms are radiative", is joined by a semicolon as part of the second; mark it as an addition ("A
third term, from the ice that …, remains unquantified").

**36. results.tex:114–115 · MINOR · kind 3.** "At 45\textdegree\,N the dry-ground land test has yet to run." A
concession on the land-surface explanation is set alone after the list of three; attach it to the land item with
"though", or open it with "At 45°N, however, …".

**37. results.tex:122–129 · MAJOR · kinds 1, 3, 4.** "On rain the models differ by a factor of about four. … within
about a degree and 0.3~m\,s$^{-1}$.\claim{G15}"

The paragraph turns from temperature to rain with no bridge; a semicolon joins the box's evaporation to its rain
total and leaves the explanation unwritten; the two models' Earth fits (line 125) are set as a freestanding
declarative whose bearing on the factor of four goes unsaid; and the slice's direction (line 126) is added as a
further point with no marker. The rewrite's "for" at the evaporation states it as the explanation of the box's low
total; the author should keep it only if the runs support that reading, and "with" or "while" would mark the link
without the causal claim.

```latex
Beyond the temperature near the ground, the models differ on rain, by a factor of about four. A small box forced from
the Earth-orbit state brought 34~mm to the ground per lunar day, where the GCM that forced it rained 129~mm and the
Sun-and-tilt run 180~mm, for at lunar gravity 85\% of the water falling from the box's clouds evaporated on the way
down, against 64\% when the same drops fell at Earth's speeds.\claim{G08} Both rates are Earth-fitted: each model
computes its rain from Earth fits of its own, a convection scheme in the GCM and Morrison's Earth-fitted limits on
raindrop size and breakup in CM1. CM1's rain depends on the slice as well: in the rings forced from the Sun-and-tilt
state the direction of the slice alone changes the rain at a place by a factor of several, while temperature and wind
at that place agree between crossing rings within about a degree and 0.3~m\,s$^{-1}$.\claim{G15}
```

**38. results.tex:153–157 · MINOR · kinds 3, 4.** "The flash-rate laws with which \textcite{braam2022lightning}
estimated … the lunar runs' 55--80~km." The turn to the exoplanet estimates leaves its bearing on the lunar flash
rate to the final clause; lead with the relation, e.g. "Exoplanet estimates have used laws fitted to far lower
storms: the flash-rate laws with which …".

**39. results.tex:164 · MINOR · kind 3.** "They separated about as much charge, …" A concession after the inverted
arrangement, left unmarked; mark it with "Even so" or "Despite the inversion".

**40. results.tex:167–170 · MINOR · kind 3.** "With the NSSL microphysics in place of Morrison's, … by about a
factor of two.\claim{G11}" The second of the two results announced at line 159 opens unmarked; mark it, e.g. "The
second result depends on the scheme: with the NSSL microphysics …".

**41. results.tex:172–176 · MINOR · kind 3.** "The GCM's surface stress over the seas corresponds to light winds, …
build waves 4--5 times as high as on Earth, …" A concession between the light winds and the high waves, left
unmarked; mark it, e.g. "Light as these winds are, under Earth's laws for wind input, … the same 10 m wind, fetch
and duration build waves 4–5 times as high as on Earth".

**42. results.tex:179–181 · MINOR · kind 5.** "The waves keep Earth's steepness, and, computed by SWASH from SWAN's
spectra, they run up …" Two findings, one at sea and one at the shore, joined by "and"; mark the move to the shore
("At the shore, computed by SWASH from SWAN's spectra, they run up …") or give each its own sentence.

**43. results.tex:181 into reach.tex:3 · MINOR · kind 4.** Results ends "…on the exposed western face of the
eastern Smythii headland.\claim{G12}"; Reach opens "Table~\ref{tab:reach} gives, property by property, the range
each repair was built for; …". Results ends on one run-up figure and Reach opens on its table, with no sentence
that turns from the test world's results to the codes' range on other worlds; a bridging clause belongs at one end,
most naturally Reach's opening, which is outside this part.

### Passages read as genuine catalogues and left out

These are catalogues set after a colon inside one sentence, or a sequence whose order the text writes, and each
stays as it is: repairs.tex:23–27 (the remaining kinds of change); repairs.tex:154–159 (the parts of the graft);
verification.tex:90–96 (the six defects removed); verification.tex:117–120 (the two shortfalls traced or bounded);
results.tex:44–46 (the four changes made in one step); results.tex:109–114 (the three other explanations of the
gap). Results' paragraph at lines 36–60 runs through the GCM states in order, each sentence opening on the state it
starts from; the states write the sequence, so it has only findings 32 and 33.

## Summary

- **Counts:** 43 findings, 15 MAJOR and 28 MINOR. Repairs: 8 MAJOR, 8 MINOR. Verification: 5 MAJOR, 9 MINOR.
  Results: 2 MAJOR, 11 MINOR (one of them, finding 43, at the boundary with Reach).
- **The paragraphs that read most like lists:**
  1. repairs.tex:71–85, "Other general repairs remove an Earth value directly": seven repairs in three codes over
     six sentences, in an order the swap test leaves free (finding 8).
  2. repairs.tex:29–42, "Defects and Earth defaults removed or avoided": the calendar, SWAN's avoidances, the open
     faults and the range of the ExoPlaSim repairs follow one another unlinked, the last returning to the
     paragraph's first subject (finding 3).
  3. repairs.tex:170–188, "Forcing from the GCM": the couplings are given in semicolon chains in an order different
     from that of the absences the paragraph opens on, and the waves follow with no turn (finding 16).
  4. verification.tex:89–121, "Defects of the adaptation" and "Checks that fell short": two catalogues set as
     paragraphs, one defect or shortfall per sentence (findings 29 and 30).
  5. repairs.tex:11–27, the classes of repair: a definition series, then a convention set as if it followed, then a
     catalogue (finding 2).
- **Pattern:** the failures concentrate in Repairs, which reads as an inventory of changes sorted under run-in
  headings, with the relations inside each paragraph left to the heading. Verification fails mostly where it
  records many checks at once. Results flows best, ordered by the sequence of GCM states and by the term-by-term
  account of the gap; its failures are single unmarked turns, apart from the cloud-and-longwave paragraph
  (finding 34) and the rain paragraph (finding 37).
