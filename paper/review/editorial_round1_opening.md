# Editorial review, round 1: title, abstract, introduction and "Worlds beyond Earth's range"

## Reviewer and scope

A fresh Claude subagent (Claude Opus 5.5) wrote this record on 2026-10-17, reading for the author. The reviewer saw
the text, the author's rules and the sources listed below, and kept out of `paper/review/`, `paper/notes/` and
every record of the drafter's own verdicts.

Text reviewed, at commit 4d03a81 (the working tree matches it):

| File | sha256 | Read |
|---|---|---|
| `paper/main.tex` | 87c1cddb6bc6a68d5a7666d4f310f250389600a5e640c3ffd8470d9ada41371c | title (line 33) and date (line 35) |
| `paper/sections/abstract.tex` | b8b0f6fd8c184465454f7265f6870d2b5f8ac2c56386654d827c6f5595834921 | in full |
| `paper/sections/introduction.tex` | 5d1b9cf839ea398370c884d828d54fe45951ab79492e9f3c7a3fce6a70aff9e0 | in full |
| `paper/sections/worlds.tex` | 46dc5b00bfd347693c0f57929ee690f4db4cd1a4ac97b996b82af07f010ff0b2 | in full, with Figure 1 as rendered in `figures/fig_regimes.png` |
| `paper/sections/assumptions.tex` | 4b0f209c6aebcbc4c907778548d27c5dca9512e3d44347ccf7cdff2f98b9cfd7 | lines 1–38 (its first two paragraphs) for the transition; lines 148–202 (`tab:inventory`) to test claims in scope |

Rules, read in full before the paper:

- `AGENTS.md` at 4d03a81 (sha256 e1f25bc0…6d32), above all "The paper", "Writing" and "Review".
- Terluna `ensemble/planning/Open_Moon_Editorial_Charter_control-01.md` (aac4a4f2…80b0), with gates G1–G4 and
  section 11 read closely.
- Terluna `ensemble/planning/source_controls/STYLE_NOTES.md` (659627e5…5c46),
  `Jewish_Papers_Updated_Style_Notes.md` (18f3d0db…3eab) and `Agent_Working_State_Editorial_Gates.md`
  (553e8957…2464).

Consulted to test claims in scope:

- `paper/claims.json` (S01–S14, W02, W06, H23, G04, G05, G09, G10) and `paper/sources/manifest.json`.
- `paper/data/regime_calc.json`, `worlds.json`, `repairs.json`, `sun_clock.json`; `paper/figures/figures.py`
  (the axes of Figure 1).
- The archived originals behind the introduction's literature sentences, read at their abstracts and cited
  passages through pdftotext: Yang et al. 2014, Way et al. 2018, Thomson and Vallis 2019, Boutle et al. 2017,
  Way et al. 2017, Wolf et al. 2022, Paradise et al. 2022, Yang et al. 2023, Tan et al. 2021, Banfield et al.
  2015, Richardson et al. 2007, Newman et al. 2011, Tsigaridis et al. 2025, Deitrick et al. 2020, Fraedrich
  et al. 2005.
- Terluna at 186b294: `climate/gcm/README.md` lines 157–182, 508–520 and 958–965; `climate/crm/README.md` lines
  1452–1457, 2046–2060, 2365–2397 and 2506–2528.
- For consistency with claims in scope: `conclusions.tex` in full (for the arc), `repairs.tex` lines 1–25,
  `next.tex` lines 1–8, `results.tex` lines 30–40, and searches of `verification.tex` and `appendix.tex` for
  the check names, the rings and the table labels.

## Method and screening

Each paragraph was read whole, then sentence by sentence, for framing, claims against their evidence, the
excluded words and defensive structure, witticisms, expert audience, exact action, written dependencies,
inheritance, terms an outside reader lacks, and technical consistency within the scope. The reading was silent;
the read-aloud pass that G3 requires for the abstract, the introduction's landing and the two section boundaries
remains open.

`paper/tools/lint.py` on the three sections, as screening only, counted negative contrast 3, possible empty
action 4, universal claim 30 and generic verb 2, and counted zero occurrences of "not" and "rather than". Each hit
was read in context; the findings below come from the reading.

Severity: BLOCKING is a rule breach that defeats a paragraph or misstates a fact or a source; MAJOR is a clear
breach the author would object to; MINOR is polish. Counts: **3 BLOCKING, 17 MAJOR, 20 MINOR.**

## Literature checks

| introduction.tex | Source and locator | Result |
|---|---|---|
| 4–5, Yang et al. | Yang et al. 2014, arXiv v1, abstract and p. 2: CAM3, 1.0 bar mainly N₂ with 400 ppmv CO₂, rotation periods of 1 to 256 days, temperature and albedo against rotation period | Supported |
| 4–5, Way et al. | Way et al. 2018, arXiv v2, abstract: 1 bar N₂-dominated air, regime transitions "as day length increases" | Supported |
| 5–6, Thomson and Vallis | Thomson and Vallis 2019, arXiv v1, abstract ("moist and dry general circulation models"); Sect. 4, p. 6: surface pressure changes with gravity, "representing a constant atmospheric mass" | Supported; the runs hold Earth's air mass |
| 7, Boutle et al. | Boutle et al. 2017, arXiv v2, abstract: an "Earth-like" atmosphere and an N₂ and trace-CO₂ atmosphere on Proxima b | Supported |
| 8, McKay et al. | Archived as a bibliographic record alone; manifest: BLOCKED, "bibliographic record only" | Rests on the title (findings 11, 40) |
| 10–11, model lineages | Way et al. 2017, p. 1 ("Its parent model, known as ModelE2"); Wolf et al. 2022, abstract ("exoplanet branch of … CESM version 1.2.1"); Paradise et al. 2022, abstract | Supported |
| 11–13, SAM and CM1 | Yang et al. 2023, arXiv v1, p. 2 ("cloud-resolving or cloud-permitting models (CPM)", SAM quasi-global at 4 km); Tan et al. 2021, Sect. 2.1 | Supported; Yang et al. class their runs as cloud-permitting (finding 12) |
| 13–14, SWAN on Mars | Banfield et al. 2015, Sect. 3, p. 370 | Supported |
| 16–17, PlanetWRF's second | Richardson et al. 2007, p. 3 ("written to be exclusively applicable to the Earth") and p. 4, Sect. 3.3 ("defined as 1/86400 of a planetary rotational period") | Supported |
| 18, TitanWRF | Newman et al. 2011, p. 637, Sect. 2.3 | The source assigns the step to PlanetWRF (finding 14) |
| 18–21, ROCKE-3D | Way et al. 2017, p. 10; Tsigaridis et al. 2025, Sect. 3.3, pp. 5834–5836 and Table 2 | Day and year constants supported; "one by one … each" exceeds Table 2 (finding 15) |
| 22–24, ExoPlaSim | Paradise et al. 2022, Sect. 2.1, p. 2, and Sect. 5, p. 24 | Supported |
| 24, "In each of these ports …" | Richardson et al. 2007, pp. 3–4; Tsigaridis et al. 2025, Sect. 3.3 | Contradicted for PlanetWRF and ROCKE-3D 2.0 (finding 16) |
| 25–26, THOR | Deitrick et al. 2020, arXiv v3, Sect. 1 | Supported; the same passage states the field-level claim the abstract makes (findings 2, 12) |

## Findings

### 1. MINOR — `main.tex:35`

> `\date{Second draft, \today}`

Rule: release integrity (charter E4; AGENTS.md "The paper", exact artifact hashes) and G7's exact-build identity.

Why: `\today` prints the build date, so two builds of one source on different days differ in text and in PDF
hash, and the title block dates the build where it should date the draft. The draft's status belongs in the
release register.

Rewrite: `\date{17 October 2026}`, with "second draft" recorded in the register.

### 2. BLOCKING — `abstract.tex:2–4`

> Exoplanets and constructed worlds whose air and water resemble Earth's, while their gravity, size, day or
> starlight differ, are studied with models built for Earth, in which an Earth value left in the code runs
> without failing.

Rules: "Claims stay within their evidence" (a field characterised whole; the author rejected "Exoplanet climate
studies compute …" on the same ground); "Exact action" (a value given the verb "runs").

Why: The sentence states the practice of two whole fields as fact. The paper's evidence is four studies and four
ports, and the introduction itself cites THOR as "a model written for other planets from the start"
(introduction.tex:25), a counterexample to the claim as written. Two archived sources state a scoped version the
paper can attribute: Deitrick et al. (2020, arXiv v3, Sect. 1), "Most studies of exoplanet atmospheres using
GCMs (general circulation models) have adapted codes developed for Earth or solar system planets", and Paradise
et al. (2022, arXiv v2, Sect. 1), "many general circulation models (GCMs) were built for Earth-like climates".
These sources survey exoplanet GCM studies alone; constructed worlds enter through one unread paper and the
author's project. In the last clause a value runs, where the run is the agent, and the paper's inventory records
an Earth value that stopped a run (RRTMG's ice optics, "Run stopped at day 6.45", assumptions.tex:179), so the
premise holds as a possibility.

Rewrite: "Many of the GCMs used to study exoplanet atmospheres were developed for Earth or for solar-system
planets. On an exoplanet or constructed world whose air and water resemble Earth's while its gravity, size, day or
starlight differ, a run that keeps a value set for Earth can complete and return a plausible number, and the
error shows when the value is checked against the world's own." In the abstract the claim stands unattributed, so
"many" keeps it within what both sources state; the introduction attributes the stronger "most" to Deitrick et al.
(finding 12).

### 3. MAJOR — `abstract.tex:4–6`

> Four such models were adapted to a breathable Moon, which changes gravity, column mass, scale height and day
> length together: ExoPlaSim~3.4.2, CM1 release~22 with WRF-ELEC's electrification, SWAN~41.51 and SWASH~12.01.

Rules: "Exact action" (a world given "changes"); "Sentences carry their dependencies" (the colon's list attaches
to the nearest noun phrase).

Why: The verb gives the Moon an act; the sentence means that its gravity, column, scale height and day differ from
Earth's together. After the relative clause the colon reads as introducing what the Moon changes, and the list of
four codes reads as its object.
The introduction and Table~\ref{tab:regime} use the scale height over the radius, where the abstract has "scale
height".

Rewrite: "Four of these codes, ExoPlaSim 3.4.2, CM1 release 22 with WRF-ELEC's electrification, SWAN 41.51 and
SWASH 12.01, were adapted to a breathable Moon, whose gravity, column mass, day and scale height in proportion to
its radius all lie far from Earth's at once."

### 4. MINOR — `abstract.tex:6–7`; `introduction.tex:56–58`

> The adaptation found Earth values in four forms (constants, units of time, geometry, and fits beyond their
> range) and five defects in the released codes.

> Adapting the four models found Earth values in four forms, dimensional constants written into the code, units
> of time, geometry, and empirical fits and simplifications used beyond the range they were made for, and five
> defects in the released codes, three of which produce little or no error at Earth's values.

Rules: "Exact action" (a process noun and a gerund given "found"; the people who did the work stay visible);
"Technical meaning survives editing".

Why: The author found the values while adapting the codes. The abstract names the fourth form "fits beyond their
range", while the introduction and assumptions.tex:9 name it "fits and simplifications used beyond their range",
so the abstract drops the simplifications (the thin shell, the flat columns). In the introduction the four forms
stand in apposition between commas, and "and five defects" reads for a moment as a fifth form.

Rewrite (abstract): "In adapting them the author found Earth values in four forms (constants written into the
code, units of time, geometry, and fits and simplifications used beyond their range) and five defects in the
released codes."
Rewrite (introduction): "In adapting the four codes the author found Earth values in four forms (dimensional
constants written into the code, units of time, geometry, and empirical fits and simplifications used beyond the
range they were made for) and five defects in the released codes, three of which produce little or no error at
Earth's values."

### 5. MAJOR — `abstract.tex:7–10`

> Three defects produce little or no error at Earth's values and affect other users' runs: ExoPlaSim's Sun
> clock, which skipped back 32.5\textdegree\ each lunar model day;\claim{H23} its convective-cover unit, which
> also biases synchronous runs;\claim{W06} and its default orbit, which replaced the Moon's tilt with Earth's.

Rules: "Write for the expert" (project names an outside reader lacks); "Claims stay within their evidence" (the
scope of "other users' runs"); "Sentences carry their dependencies" (a concessive relation written as "and").

Why: "Sun clock", "lunar model day" and "convective-cover unit" are the project's own names, and the abstract
leaves the operation behind each of them unstated. "Affect other users' runs" leaves the runs unbounded; the
conclusion bounds them exactly (conclusions.tex:6–9), and claims.json W06 records the synchronous bias as a
calculation from the code (+0.23 in cover for TRAPPIST-1e, +0.31 for Proxima b). The two predicates stand in a
concessive relation, small error at Earth's values and larger error elsewhere, which "and" writes as a sum. The
verbs mix past ("skipped back", "replaced") and present ("biases") for three defects that remain in the released
code. The 32.5° itself checks: it matches `regime_calc.json#sun_clock_skip`, a model day of 1,430 half-hour
steps.

Rewrite: "Three ExoPlaSim defects produce little or no error at Earth's values and larger errors in other
configurations: its solar-angle arithmetic restarts each model day, setting the Sun back 32.5° a day on the Moon
and by steps of up to 33° in other non-synchronous runs whose rotation differs from a day; its conversion of
convective rain to cloud cover per model day biases synchronous runs as well; and its orbit default replaces a
configured tilt and eccentricity with Earth's in any run that leaves the orbit unfixed."

### 6. MAJOR — `abstract.tex:10–12`

> General repairs correct units, apply scaling laws or remove defects and serve other worlds unchanged; a method
> computes the curved geometry for each world's column; and calibrations to an in-house line-by-line model hold
> near the design case.

Rules: "Sentences carry their dependencies" and the swap test; "Technical meaning survives editing".

Why: The three clauses trade places without loss. The relation that orders them, the worlds each class holds for,
stays unwritten, though the introduction names it ("three classes with different reach") and the conclusion lands
on it. repairs.tex:15–16 bounds the first class ("another world takes it unchanged within the limits of
Table~\ref{tab:reach}"); the abstract drops those limits and the "physical law" of the introduction's definition.
"The design case" and "in-house" appear here undefined.

Rewrite: "The repairs differ in the worlds they hold for: a general repair, which corrects a unit, applies a
scaling or physical law or removes a defect, holds on another world within stated limits; a general method holds
wherever its table is computed from that world's own column, as for the curved geometry of the lunar air; and a
calibration, fitted to the author's line-by-line radiative–convective model on columns of the lunar design case,
holds near those columns."

### 7. MINOR — `abstract.tex:12–13`

> Identity, reproduction, similarity and benchmark checks test the code; the lunar climate is unobserved.

Rules: "Write for the expert" (bare labels); "Sentences carry their dependencies".

Why: "Identity" and "similarity" checks are the paper's labels, defined at verification.tex:4–12; the reader of
the abstract needs the operations. The second clause states the consequence for the evidence state, and the
semicolon leaves that relation to the reader.

Rewrite: "Checks that each patch reproduces the released code at its default, that runs repeat byte for byte,
that a run at scaled gravity, lengths and times reproduces the original in dimensionless form, and that the
electrified code matches Earth benchmarks test the code; with the lunar climate unobserved, its numbers are
conditional model results."

### 8. MAJOR — `abstract.tex:13–16`

> On the case, the general repairs moved the global mean by a few kelvin and the distribution of rain further,
> the calibrations and PlaSim's Earth-tuned cloud and longwave cooling moved it most,\claim{G05} and the storms'
> freezing level stood five to six times higher than Earth's, their lightning rarer and larger.\claim{G09}\claim{G10}

Rules: "Sentences carry their dependencies" (three results of different kinds coordinated as equals); "Technical
meaning survives editing" (evidence states and conditions).

Why: One coordinated sentence sets applied repairs, sensitivity tests and CM1's conditional results side by side.
claims.json records G05 as a sensitivity (the longwave correction with ice optics warms by about 11.5 K "in a run
outside the correction's fitted state", conclusions.tex:15–16) and G10 as the "main electrified run on
pre-correction forcing", with ground strikes an upper bound; the abstract reports both as plain outcomes. The
comparison the conclusion lands on, that the parts fitted to Earth or to the lunar columns moved the climate
most, stays implicit. "On the case" reads as the idiom; "further" leaves the rain's change unquantified, where
the conclusion gives it (rain cut by nearly a quarter); and the freezing level belongs to the environment the
storms rise through.

Rewrite: "In the lunar design case the general repairs moved the global-mean surface temperature by a few kelvin
at most and cut the rain by nearly a quarter, while the parts fitted to Earth or to the lunar design columns moved
it most: the first calibration by at least 20 K, and in sensitivity tests PlaSim's Earth-tuned cloud by up to
about 6 K and its corrected longwave cooling by about 11.5 K. Where CM1 forms its own cloud at lunar gravity, the
freezing level stands five to six times higher than Earth's, and in the main electrified run, on pre-correction
forcing, lightning is rarer and larger than Earth's."

### 9. MAJOR — `abstract.tex:16–17`

> Building those parts from the reference's physics and from cloud-resolving runs would narrow the Moon's
> uncertainty and widen the models' reach together.

Rules: "No witticisms" (a balanced antithetical landing built for quotation); "Exact action" ("the Moon's
uncertainty", "the models' reach"); "Write for the expert" ("those parts", "the reference").

Why: "Narrow … and widen … together" closes on a symmetry, where the conclusion (conclusions.tex:21–22) states
the same consequence plainly. The uncertainty belongs to the lunar results, and "reach" names by figure the set of
worlds a part holds for. "Those parts" has two candidate antecedents, and "the reference" appears here for the
first time.

Rewrite: "Rebuilding the calibrated radiation from the line-by-line model's spectroscopy, and the cloud settings
from cloud-resolving runs, would reduce the largest uncertainties in the lunar results and make the same parts
hold on other Earth-like worlds."

### 10. MINOR — `introduction.tex:3`

> Some exoplanet climate studies hold a planet's air close to Earth's and change the planet around it.

Rules: "No witticisms"; "Say what is".

Why: "The planet around it" inverts the physical image (the air surrounds the planet) for effect, and the
operation lies in the variables the next sentence supplies. The author's direction for this sentence names them:
"some hold the air near Earth's and vary rotation, gravity or star".

Rewrite: "Some exoplanet climate studies hold a planet's air close to Earth's and vary its rotation, gravity or
star."

### 11. MAJOR — `introduction.tex:8–9`

> Work on constructed worlds asks how a planet could be made habitable \autocite{mckay1991making} and, for a
> designed world, what its climate would be \autocite{goldman2026terluna}.

Rules: "Claims stay within their evidence"; "Exact action" ("Work … asks"); the paper's framing ("Terluna enters
as provenance only"; the author's direction "name the project once, as the source of the case").

Why: The sentence states what a body of work asks from two citations. One is the author's own project, presented
here as the field's literature and cited again at line 33 as the source of the case. The other exists in the
archive only as a bibliographic record (manifest: BLOCKED, "bibliographic record only"), so its content rests on
its title.

Rewrite, once the source is read: "McKay, Toon and Kasting asked how Mars could be made habitable
\autocite{mckay1991making}." The Terluna citation then stands once, at line 33.

### 12. MAJOR — `introduction.tex:9–14`

> Many of the models used in such work descend from Earth models: ROCKE-3D from the GISS ModelE2, ExoCAM from
> NCAR's Community Atmosphere Model and ExoPlaSim from the Planet Simulator
> \autocite{way2017resolving,wolf2022exocam,paradise2022exoplasim}; the cloud-resolving models SAM and CM1 have
> simulated convection on tidally locked planets and in pure-steam air \autocite{yang2023cloud,tan2021convection};
> and SWAN, a coastal wave model, has been run for the ancient seas of Mars \autocite{banfield2015winds}.

Rules: "Claims stay within their evidence" ("Many" over a field); "Sentences carry their dependencies" (a colon
list whose later items fall outside its heading).

Why: The colon announces examples of descent from Earth models, and the semicolons add two items of another kind,
Earth-built models run elsewhere, so punctuation joins an inventory. "Many of the models used in such work" rests
on three examples, while Deitrick et al. (2020) and Paradise et al. (2022) state the field-level claim themselves
(finding 2) and can carry it by attribution. Yang et al. (2023, arXiv v1, p. 2) class their quasi-global 4 km
SAM runs among "cloud-resolving or cloud-permitting models (CPM)".

Rewrite: "By the account of THOR's developers, most GCM studies of exoplanet atmospheres adapt codes developed for
Earth or for solar-system planets \autocite{deitrick2020thor}: ROCKE-3D descends from the GISS ModelE2, ExoCAM
from NCAR's Community Atmosphere Model and ExoPlaSim from the Planet Simulator
\autocite{way2017resolving,wolf2022exocam,paradise2022exoplasim}. Convection and wave models built for Earth have
been run off Earth as well: SAM in cloud-permitting runs on tidally locked planets, CM1 in pure-steam air, and the
coastal wave model SWAN on the ancient seas of Mars \autocite{yang2023cloud,tan2021convection,banfield2015winds}."

### 13. MINOR — `introduction.tex:16`

> The developers of several such ports found values fixed for Earth in the code.

Rule: inheritance (each sentence receives something from the one before).

Why: "Such" points back to "ports", a word the previous sentence lacks; that sentence speaks of models descended
from Earth models and of models run off Earth, and the reader has to equate them with ports.

Rewrite: "Developers who ported Earth models to other planets found values fixed for Earth in the code."

### 14. MAJOR — `introduction.tex:18`

> TitanWRF's removed hard-wired Earth settings from the physics;

Rule: "Claims stay within their evidence" (attribution to the cited source).

Why: Newman et al. (2011, p. 637, Sect. 2.3) assign the step to PlanetWRF: "major modifications to produce a
planetary version (PlanetWRF) included removing hard-wired 'Earth' settings from parameterizations of physical
processes (e.g., boundary layer mixing schemes) and adding planet-specific treatments of radiative transfer for
Mars, Titan and Venus", after which they introduce "The Titan version of PlanetWRF, TitanWRF". The sentence
credits TitanWRF with PlanetWRF's step and so counts one team's generalisation twice. The elliptical "TitanWRF's"
also leaves its noun to the reader.

Rewrite: "PlanetWRF's developers, finding WRF written to apply to Earth alone, redefined its second as 1/86,400
of the planet's rotation period and removed hard-wired Earth settings from its physics, and built TitanWRF on the
result \autocite{richardson2007planetwrf,newman2011stratospheric};"

### 15. MINOR — `introduction.tex:18–21`

> and ROCKE-3D's found constants tied to the lengths of Earth's day and year, then eliminated or generalised its
> Earth-centric options one by one in a second release, measuring the effect of each

Rule: "Claims stay within their evidence" ("each", "one by one", and "then" joining two different sets).

Why: Tsigaridis et al. (2025, Sect. 3.3, pp. 5834–5836) present "which options we have either eliminated or
generalized, as well as their individual impact on model results", and their Table 2 removes three Earth-specific
settings in one run (P2GApM40_notEarth, −1.27 W m⁻² in net planetary radiation together), and their text runs
the cloud-top change incrementally with the SOCRATES radiation alone. The second release's options (the cloud
inhomogeneity map, the 50 hPa cloud-top limit, the shortwave water-absorption increase, Earth-specific longwave
optimisations) differ from the day and year constants of the first release (Way et al. 2017, p. 10), so "then"
links two different sets.

Rewrite: "and ROCKE-3D's developers found constants tied to the lengths of Earth's day and year in its first
release and, in its second, removed or generalised a set of Earth-centric options, measuring their effects in a
sequence of incremental runs \autocite{way2017resolving,tsigaridis2025rocke3d}."

### 16. BLOCKING — `introduction.tex:24–26`

> In each of these ports the developers repaired what their own world required, and the developers of THOR, a
> model written for other planets from the start, describe planet-specific tunings as often built into codes and
> hard to find \autocite{deitrick2020thor}.

Rules: "Claims stay within their evidence" ("each" over the cited ports); "Sentences carry their dependencies".

Why: The sources for two of the cited ports contradict the summary. Richardson et al. (2007, p. 3) built PlanetWRF as "a flexible
and general workhorse for planetary atmospheric/climate system modeling", "generalizing the specification of
planetary constants and timing conventions", and (p. 4, Sect. 3.3) gathered the constants in one module so that
setting them "up for any arbitrary planet" is "very straightforward"; Tsigaridis et al. (2025, Sect. 3.3)
eliminated or generalised Earth-centric options for rocky planets in general. "What their own world required"
therefore misstates both sources, and the sentence is the paragraph's step toward "which repairs made for one
world hold on another". The "and" then sets THOR's statement beside that summary with their relation unwritten.
Tsigaridis et al. also supply the evidence the paragraph needs: the first release left its changes from the Earth
configuration to a general one without systematic study (p. 5834).

Rewrite: "Each team repaired the Earth values that mattered for the worlds it set out to model, and the rest could
stay in the code: ROCKE-3D's developers report that their first release left its changes from the Earth
configuration to a general one without systematic study \autocite{tsigaridis2025rocke3d}, and THOR's developers,
who wrote their model for other planets from the start, describe planet-specific tunings as often built into
adapted codes and hard to find \autocite{deitrick2020thor}."

### 17. MAJOR — `introduction.tex:26–29`

> On an Earth-like world, an Earth value left in the code can go unnoticed: the air and water stay within the
> regime the model was built for, so a constant set for Earth's gravity, or a formula that counts rain per Earth
> day, runs to completion and returns a plausible number.

Rules: "Exact action" (a constant and a formula "run to completion"); "Technical meaning survives editing".

Why: A run completes; a constant and a formula enter its arithmetic. "The air and water stay within the regime the
model was built for" overstates the paper's own case: the lunar column holds 7.25 times Earth's air, and RRTMG's
tables end at 1.05 bar under a 1.22 bar surface (Table~\ref{tab:regime}). What stays within the models' range is
the air's composition and temperature and the water's phases.

Rewrite: "On an Earth-like world an Earth value left in the code can pass unseen: the air's composition and
temperature and the water's phases stay within the range the model was built for, so a run that keeps a constant
set for Earth's gravity, or a formula that counts rain per Earth day, can complete and return a plausible number."

### 18. MINOR — `introduction.tex:32–33`

> The work reported here took up both questions on one world, a breathable Moon designed in an open project
> \autocite{goldman2026terluna},

Rules: the paper's framing (the author's direction "name the project once, as the source of the case"); "Exact
action"; self-reference.

Why: "An open project" gives the reader a citation and withholds the name, which the reference list prints as
Terluna. The author took up the questions, and the sentence gives that act to "the work".

Rewrite: "Both questions are taken up here on one world, a breathable Moon designed in the Terluna project
\autocite{goldman2026terluna}, with …"

### 19. MINOR — `introduction.tex:35–38`

> Its air is close to Earth's, while four ratios on which the models' Earth values depend lie far from Earth's at
> once: the air over each square metre is 7.25 times Earth's,\claim{S02} the scale height of about 52~km is 23
> times Earth's in proportion to the radius,\claim{S03} gravity is a sixth of Earth's, and the solar day lasts
> 29.5 Earth days.

Rules: "Technical meaning survives editing"; "Write for the expert" (redundancy).

Why: Read together, the clauses say the air is close to Earth's and the column holds 7.25 times Earth's air; the
closeness lies in composition and surface pressure. Gravity and the day appear one sentence earlier with their
values (1.62 m s⁻², 29.53 days) and return here, the day as 29.5.

Rewrite: end the previous sentence at "a shield in space", then: "Its air is close to Earth's in composition and
surface pressure, while four ratios on which the models' Earth values depend lie far from Earth's at once: each
square metre holds 7.25 times Earth's air, the scale height of about 52 km is 23 times Earth's in proportion to
the radius, gravity, at 1.62 m s⁻², is a sixth of Earth's, and the solar day lasts 29.53 Earth days."

### 20. MINOR — `introduction.tex:38–40`

> Adapting models to this world exercised many of the Earth values they hold, with errors large enough to
> measure:

Rule: "Exact action" (a gerund agent; a software-testing figure for the operation).

Why: The lunar runs computed with the values, and the author measured their errors; "exercised" borrows a testing
figure for that operation.

Rewrite: "On this world many of those values are wrong by amounts large enough to measure: PlaSim fixes the
horizon air mass at Earth's 35, where the Moon's well-mixed air has about 7."

### 21. MINOR — `introduction.tex:42–54` (the models paragraph)

> (a) diagnoses its clouds and convection from formulas fitted to Earth (44–45); where it resolves the convection
> the GCM diagnoses (47)
> (b) on rings of columns along latitude circles or tilted great circles (46)
> (c) and SWAN's spectra drive SWASH~12.01 \autocite{zijlema2011swash,swash1201user} up the shore (49–50)
> (d) Each model's grid, levels, time step and runs are given in Table~\ref{tab:config}. (53–54)

Rules: (a) "Technical meaning survives editing"; (b) "Write for the expert"; (c) "No witticisms"; (d) paragraph
landing.

Why: (a) PlaSim parameterizes cumulus convection with a Kuo-type scheme (Fraedrich et al. 2005, p. 3: "The cumulus
convection is parameterized by a Kuo-type convection scheme") and diagnoses its cloud cover. (b) The appendix
gives the rings as two-dimensional domains (appendix.tex:18: the equatorial ring 10,916 km round in 1,816
columns), which the phrase leaves the reader to guess. (c) "Drive SWASH … up the shore" moves the model where the
waves go. (d) The paragraph follows a forcing chain from the GCM to the shore and ends on a table pointer.

Rewrites: (a) "parameterizes its convection with a Kuo-type scheme and diagnoses its clouds from formulas fitted to
Earth", and "where it resolves the convection the GCM parameterizes"; (b) "on two-dimensional rings of columns
around latitude circles or tilted great circles"; (c) "and SWASH 12.01, forced by SWAN's spectra, computes the
waves at the shore"; (d) open the paragraph "ExoPlaSim 3.4.2 … computes the global climate
(Table~\ref{tab:config} gives the four codes' configurations)" and end it on the radiation sentence, whose
calibration leads into the next paragraph's three classes.

### 22. MINOR — `introduction.tex:61`; `worlds.tex:45`

> as for the curved geometry of a tall air
> for an isothermal air

Rule: precise nouns.

Why: The paper uses "air" as a mass noun everywhere else; "a tall air" and "an isothermal air" read as slips for
"atmosphere".

Rewrite: "as for the curved geometry of a tall atmosphere"; "for an isothermal atmosphere".

### 23. BLOCKING — `introduction.tex:58–63`

> Each repair falls into one of three classes with different reach: a general repair, which corrects a unit,
> applies a scaling law or a physical law, or removes a defect, and which another world takes unchanged; a
> general method with a table computed for each world's column, as for the curved geometry of a tall air; and a
> calibration, whose coefficients were fitted to the reference model on the columns of the lunar design case and
> are fitted again for any other world.

Rules: "Claims stay within their evidence" ("Each"); the author's rejected example "The repairs follow one rule
…", whose direction reads "The main rule, with the other kinds of repair beside it"; "Exact action" ("another
world takes"); "Technical meaning survives editing".

Why: The repairs section lists further kinds of change beside the three classes: "Beside the three classes stand
settings, which give the scenario's values; capabilities, which add a process or a forcing the released codes
lack; a bound, where the physics is unsettled; a mitigation; avoidances by configuration; and a coupling method"
(repairs.tex:22–25). The Repair column of `tab:inventory` marks them (Setting, Capability, Bound, Mitigation,
Avoided, Bypassed, Open). The introduction's "each" therefore misstates the paper's own classification.
repairs.tex:15–16 also bounds the first class ("within the limits of Table~\ref{tab:reach}"), a limit the
introduction drops; the clause gives a world the act of taking a repair; and "are fitted again for any other
world" reports as done a refit that awaits each new world.

Rewrite: "Three classes of repair differ in the worlds they hold for: a general repair, which corrects a unit,
applies a scaling or physical law, or removes a defect, holds on another world within stated limits; a general
method holds wherever its table is computed from that world's own column, as for the curved geometry of a tall
atmosphere; and a calibration, whose coefficients were fitted to the reference model on columns of the lunar
design case, holds near those columns and must be refitted for another world. Settings, added capabilities, a
bound, a mitigation, avoidances by configuration and a coupling method make up the remaining changes."

### 24. MAJOR — `introduction.tex:63–67`

> On the case, the repaired models measure how far each Earth value moved the climate and which of those that
> remain move it most, and the three classes set which other worlds the adapted models can reach. Every lunar
> climate number is a conditional model result, holding given the scenario and the Earth values that remain; with
> the lunar climate unobserved, the strongest test open to these numbers is agreement among independent models.

Rules: "Exact action" ("models measure", "classes set", "models can reach"); "Claims stay within their evidence"
("each Earth value"); "Conclusions and the arc" (the opening promises the contribution the conclusion lands on);
paragraph landing.

Why: The author measured with paired runs of the repaired models and sorted the changes into classes; the
sentence gives those acts to the models and the classes, and "reach" names a set of worlds by figure. "Each Earth value" exceeds the evidence: next.tex:3–5 leaves the later steps unordered "since
their effects on the climate remain unmeasured". The conclusion's governing relation, the parts sorted "by how far
each moved the Moon and by how far each travels, and the two orders run against each other"
(conclusions.tex:10–11), is absent from the opening. The introduction closes on the evidence state and on a
test, agreement among independent models, that the paper lists as work to come (verification.tex:110;
next.tex:20). "On the case" reads as the idiom.

Rewrite: "With repairs switched off and on in paired runs, the author measured how far the lunar climate moved as
the main Earth values were repaired, and bounded several that remain with sensitivity tests; every lunar climate
number is a conditional model result, given the scenario and those remaining values. Ranked by the worlds they
hold for, the same changes fall in the opposite order: the general repairs moved the case's global mean by a few
kelvin, while the parts fitted to Earth or to the lunar design columns moved it most."

### 25. MAJOR — `worlds.tex:3–4`

> An Earth value in a model holds where a world's governing ratios equal Earth's, and its error grows with the
> world's distance from them.

Rules: "Write for the expert" (delete test: the first clause restates the definition); "Claims stay within their
evidence" (an unexamined law for every Earth value).

Why: A value set for Earth holds at Earth's values by its definition, so the first clause tells the expert reader
what that reader already holds. The second clause states a law for every value, while the paper's records show
thresholds and plateaus: RRTMG's tables hold to 1,053.63 hPa and are extrapolated beyond (assumptions.tex:178),
and ExoPlaSim's Sun clock skips 32.7° for every rotation slower than 20 days (claims.json W02;
`regime_calc.json#exoplasim_slow_rotators`). The sentence also uses "governing ratios" one sentence before naming
them.

Rewrite: delete the sentence and open on the ratios (finding 26). If the growth of the error stays, give its
forms: "Their errors start at Earth's values and grow in different ways: ExoPlaSim's Sun clock skips by steps
that reach 32.7° at a rotation of 20 days and stay there for every slower rotation, while RRTMG's pressure tables
hold to 1.05 bar and are extrapolated beyond."

### 26. MAJOR — `worlds.tex:4–9`

> Four ratios govern most of the values found in these models (Table~\ref{tab:regime}): the scale height over
> the radius, which fixes the geometry of the sunlit and radiating air; the mass of air over each square metre,
> which fixes the absorber paths that broadband radiation fits were made on and the pressures that radiation
> tables span; the gravity, which fixes the height of each pressure level and the fall of every particle; and the
> solar day, which fixes whatever a formula counts per day.

Rules: G1's "definition series" and "A genuine catalogue goes in a table or a list"; "Sentences carry their
dependencies" (four mechanically parallel "which fixes" frames); "Claims stay within their evidence" ("most",
"every").

Why: The four clauses trade places without loss, and their content repeats Table~\ref{tab:regime}'s rows and
right-hand column. "Most" is unexamined: many rows of `tab:inventory` depend on composition, spectrum,
temperature, laboratory laws, rotation or tilt (RRTMG's gases and Sun, PlaSim's shortwave gases and Rayleigh
normalisation, cloud phase, saturation, the charging laws, SWAN's air density, the beta plane, the orbit
default), so a count decides between "most" and "many". "Fixes" overstates gravity's part in fall speed, which
drag and the air's density share. The column clause conflates two columns: Earth's fixed the paths the fits were
made on, and the Moon's fixes the paths the fits now meet.

Rewrite: give the physical roles a column in Table~\ref{tab:regime}, open the paragraph with the count of
inventory rows that depend on the four ratios, and keep one sentence for the grouping the table leaves implicit:
"Two of these ratios set the radiation's paths and two the scales of height and time (Table~\ref{tab:regime}).
The column mass sets the absorber paths, which PlaSim's broadband fits took from Earth's column, and the
pressures, which RRTMG's tables cover to 1.05 bar; the scale height over the radius sets how far the sunlit and
radiating air departs from a flat column; gravity sets the height of each pressure level and, with drag and the
air's density, each particle's fall speed; and the solar day sets whatever a formula counts per day."

### 27. MINOR — `worlds.tex:9`; caption at line 22

> Found and constructed worlds lie off Earth's values in different directions
> Grey filled points are found worlds

Rules: "No witticisms" (coined terms); precise nouns.

Why: "Found worlds" is a coinage paired with "constructed"; the introduction speaks of exoplanets, and the figure
shows solar-system bodies.

Rewrite: "Natural and constructed worlds lie off Earth's values in different directions"; "Grey filled points are
natural worlds".

### 28. MAJOR — `worlds.tex:10–13`

> Titan's air holds ten times Earth's mass over each square metre and Venus's a hundred times, and their solar
> days of 16 and 117 Earth days place both far along the day axis; present Mars departs mainly in its thin
> column, and Earth-like planets that rotate slowly depart along the day axis alone. The breathable Moon departs
> along all four at once, in air close to Earth's.\claim{W02}

Rules: "Technical meaning survives editing" (the comparison omits departures the figure shows); "Exact action"
("solar days … place"); inheritance (the landing's distinction rests on a trailing phrase).

Why: Titan departs along all four ratios. `paper/data/worlds.json` gives its gravity as 1.352 m s⁻² (0.14 of
Earth's, below the Moon's 1.62) and its scale height over radius as 0.008 (six times Earth's), and
Figure~\ref{fig:regimes} draws Titan beside the Moon in the right panel. Set against "mainly" and "alone", the
landing reads as if the Moon alone departs along all four, and the sentence states its real distinction,
Earth-like air, in a trailing phrase.

Rewrite: "Titan departs along all four ratios, with ten times Earth's air over each square metre, a gravity below
the Moon's and a 16-day solar day, and Venus along the column and the day, with a hundred times Earth's air and a
117-day solar day; present Mars departs mainly in its thin column, and slowly rotating Earth-like planets along
the day alone. Among these worlds the breathable Moon is the one that departs along all four in air close to
Earth's."

### 29. MINOR — `worlds.tex:18–25` (caption and labels of Figure~\ref{fig:regimes})

> Found and constructed worlds against the ratios on which the models' Earth assumptions depend. Left: scale
> height over radius against the air's mass per unit area, relative to Earth's; … Right: solar day against
> surface gravity; … Grey filled points are found worlds; open points are constructed or illustrative ones (Mars
> held at 1~bar; …)

Rules: precise nouns; captions and figures receive the same review as the prose (charter G4; G7 for the rendered
labels).

Why: (1) "Y against X" conventionally places Y on the vertical axis; figures.py:51–52 and 59–60 put H/R and the
solar day on the horizontal axes, so the caption reverses both panels. (2) "Earth assumptions" adds a second term
for "Earth values". (3) In the right panel present Mars and Mars at 1 bar share one open point labelled "Mars,
present and at 1 bar", while the caption reserves filled points for natural worlds. (4) The panels' annotations
read "PlaSim's horizon air mass, 35: right here" and "PlaSim's per-day formulas right", colloquial for a figure
the rules read like prose.

Rewrite: "Natural and constructed worlds against the ratios on which the models' Earth values depend. Left: the
air's mass per unit area, relative to Earth's, against scale height over radius; … Right: surface gravity
against solar day; …"; annotations "PlaSim's horizon factor of 35 holds on this line" and "PlaSim's per-day
formulas exact"; present Mars drawn as a filled point in the right panel.

### 30. MINOR — `worlds.tex:31–33`

> a scale of 0.970 chosen so that the GCM's global-mean surface settles at the design temperature of 295~K

Rule: precise nouns.

Why: The surface temperature settles; the sentence has the surface settle at a temperature.

Rewrite: "a scale of 0.970 chosen so that the GCM's global-mean surface temperature settles at the design value of
295 K".

### 31. MINOR — `worlds.tex:34–38`; Table~\ref{tab:regime}, line 56

> Beneath the shield the air holds 121,590~Pa at the water level, … because the land stands above the water
> level, the surface pressure averages 1.16~atm over the globe and ranges from 1.02 to 1.22~atm.\claim{S05}
> Surface pressure at the water level (bar) & 1.01 & 1.22

Rule: "Technical meaning survives editing".

Why: 121,590 Pa is 1.20 atm and 1.22 bar. The table gives the water-level pressure as 1.22 bar, and the text gives
the surface maximum as 1.22 atm, about 123,600 Pa and 1.7% above the water-level pressure. Land above the water
level explains the mean and the minimum; the maximum needs its own cause (dry ground below the water level, or
the circulation's highs). A reader comparing table and text meets "1.22" in two units for two quantities.
Terluna's GCM README at 186b294 (lines 161–163) gives 1.03–1.22 atm for its runs, and claims.json S05 cites run
A28_corrected_970, year 19, for 1.02.

Rewrite: one unit across text and table (atm, as the scenario's 1.2 atm), and "…; land standing above the water
level lowers the global-mean surface pressure to 1.16 atm and the lowest to 1.02 atm, and [its cause] raises the
highest to 1.22 atm."

### 32. MINOR — `worlds.tex:39–40`

> so that 759 of the GCM's 2,048 cells, 40\% of its surface, hold water

Rule: "Technical meaning survives editing".

Why: 759 of 2,048 cells is 37%; the 40% is the share of the area, larger because the grid's cells differ in area.
A reader who divides meets a discrepancy.

Rewrite: "so that 759 of the GCM's 2,048 cells, 40% of its area, hold water".

### 33. MINOR — `worlds.tex:43–48` (caption of Table~\ref{tab:regime})

> The ratios that separate the breathable Moon from Earth, and the model parts that depend on each. … Rows marked
> $^\dagger$ are CM1 results for the case, conditional model results;

Rules: precise nouns; redundancy.

Why: Most rows hold dimensional quantities (gravity in m s⁻², pressure in bar, heights in km) under the column
heading "Quantity", and "results … results" repeats.

Rewrite: "The quantities that separate the breathable Moon from Earth, and the model parts that depend on each. …
Rows marked † are conditional results of CM1 for the case;"

### 34. MAJOR — `worlds.tex:72–83` (the paths paragraph)

> Every path through the case's air is longer than its counterpart on Earth (Table~\ref{tab:regime}). …
> Gravity at the 86~km tropopause is 9\% below its surface value, a column with gravity falling as $GM/r^2$ holds
> about 5\% more air per unit area than $p_s/g_s$, and spherical shells with that gravity hold 11.5\% more over
> each square metre of ground than $p_s/g_s$.\claim{S10}

Rules: each paragraph develops one movement and lands on its completion (G1); "Sentences carry their
dependencies" (the landing's three coordinated figures); "Claims stay within their evidence" ("Every path").

Why: The opening sentence governs the column, slant and twilight sentences; the last two sentences turn to the
dynamics' thin shell and to gravity's fall with height, which the opening leaves out, and the paragraph lands on
three coordinated figures and leaves unstated their consequence for the models, which take the column as
$p_s/g_s$. The table
cited for "every path is longer" shows the Moon's horizon air mass as 7.2 against Earth's 34.5; the slant path is
longer in absolute terms (about 540 t m⁻² against 355), a product the reader has to form.

Rewrite: open "Every absorber path through the case's air is longer than its counterpart on Earth, and every
layer the models treat as flat is curved (Table~\ref{tab:regime})." and land "Gravity falls 9% by the 86 km
tropopause, so a column with gravity falling as $GM/r^2$ holds about 5% more air than the $p_s/g_s$ the codes
assume, and the widening spherical shells raise the excess to 11.5% per square metre of ground: for the same
surface pressure, the lunar air holds about a tenth more mass than the models count."

### 35. MINOR — `worlds.tex:75–77`

> A scale height of about 52~km against a radius of 1,737~km places the air's mass on average 48.6~km above the
> ground, where a shell has 5.8\% more area than the ground beneath it,

Rules: "Exact action" ("A scale height … places"); "Technical meaning survives editing".

Why: The mass-mean height follows from the profile, and the sentence gives the act of placing to the scale height.
The 5.8% belongs to a shell
50 km up (claims.json S09; Terluna GCM README line 963, "a shell 50 km up has 5.8% more area"); at 48.6 km the
excess is 5.7%. `regime_calc.json#column_with_falling_gravity` also records a mass-mean height of 46.9 km for the
design profile, so the paper's data hold two values for the one quantity.

Rewrite, once 48.6 and 46.9 km are reconciled: "With a scale height of about 52 km over a radius of 1,737 km, the
air's mass lies on average 48.6 km above the ground, where a shell has 5.7% more area than the ground beneath
it,"

### 36. MINOR — `worlds.tex:79–80`

> a full Earth day after sunset, about half the air above a place still lies above the Moon's geometric
> shadow.\claim{S04}

Rule: "Technical meaning survives editing" (a condition dropped).

Why: claims.json S04 and `regime_calc.json#one_day_after_sunset` compute the shadow with refraction ignored.
Refraction bends the light toward the ground and raises the lit share, so "about half" is a lower estimate whose
condition belongs beside it.

Rewrite: "a full Earth day after sunset, about half the air above a place still lies above the Moon's geometric
shadow, before refraction adds more."

### 37. MAJOR — `worlds.tex:85–89`

> A sixth of Earth's gravity raises every pressure level sixfold in height, so a formula written in metres places
> its features six times too low; it slows the fall of droplets sixfold, of rain about threefold and of graupel
> 2.3-fold; it lengthens the roughness of a wind-driven sea sixfold for the same friction velocity
> \autocite{charnock1955wind}; and it slows a deep-water wave of a given length to 0.41 of its speed on
> Earth.\claim{S11}

Rules: "Sentences carry their dependencies" (four "it [verb]s" clauses of equal weight); the swap test; "Exact
action" ("a formula … places").

Why: After the first clause, the remaining clauses trade places without loss and repeat
Table~\ref{tab:regime}'s gravity row with numbers. The relation they share is the power of gravity each follows
($g^{(b+1)/3}$ for a fall speed with fall-speed exponent $b$, $1/g$ for Charnock's roughness, $\sqrt{g}$ for the
deep-water phase speed; `regime_calc.json#fall_speed_slowdown` and `#sea`), which sorts them into heights, fall
speeds and the sea. The code computes a feature's height from the formula, and the sentence gives the placing to
the formula.

Rewrite: "A sixth of Earth's gravity raises every pressure level sixfold in height, so a code that sets a feature's
height in metres puts it at a sixth of its lunar height. Fall speeds follow gravity to powers set by each
particle's fall-speed law, slowing droplets sixfold, rain about threefold and graupel 2.3-fold; at the sea,
Charnock's roughness grows sixfold for the same friction velocity, and a deep-water wave of a given length travels
at 0.41 of its speed on Earth."

### 38. MAJOR — `worlds.tex:89–92`

> The dry dynamics stretch about sixfold in size and duration at the same speeds, so a 6~km column of a
> cloud-resolving model stands for about 1~km at Earth's scale, while the microphysics and the radiation keep
> their own scales; a pair of runs designed to measure how far lunar convection departs from Earth's convection
> stretched sixfold failed to convect.\claim{S12}

Rules: "Sentences carry their dependencies" (an evidentiary relation behind a semicolon); "Technical meaning
survives editing" (evidence state); syntax.

Why: The semicolon sets the failed test beside the similarity as one more fact. The relation is evidentiary: the
pair was the test of how far lunar convection departs from the stretched Earth case, and its failure leaves that
departure unmeasured, so the 6 km to 1 km equivalence stands as a nominal scale, as the table caption (line 47)
says. "Earth's convection stretched sixfold failed to convect" reads first as a single noun phrase.

Rewrite: "The dry dynamics stretch about sixfold in size and duration at the same speeds, so a 6 km column of a
cloud-resolving model stands for about 1 km at Earth's scale, while the microphysics and the radiation keep their
own scales. How far lunar convection departs from Earth's, stretched sixfold, remains unmeasured: the pair of runs
designed to measure it failed to convect, and the 6 km grid is justified by the dry similarity alone."

### 39. MAJOR — `worlds.tex:92–96`, and the boundary with `assumptions.tex:3`

> The 29.53-day solar day deepens the soil's thermal wave to about 0.6~m, … and multiplies nearly thirtyfold
> whatever a formula counts per day; the 27.32-day rotation sets a Coriolis parameter of \SI{5.2e-6}{s^{-1}} at
> 80\textdegree, an inertial period of 14 Earth days.\claim{S13} The tilt of 1.54\textdegree\ gives the poles a
> grazing Sun all year.
>
> (next section) An Earth value is a value or form in a model that agrees with Earth because it was set or fitted
> there; …

Rules: each paragraph develops one movement, and its last sentence completes it or sets up the next (G1, G3);
inheritance across sections; "Sentences carry their dependencies"; "Exact action" ("the solar day …
multiplies"; the generic "gives").

Why: The paragraph opens on gravity ("Gravity's surface value matters more") and, after the gravity pair, appends
the day, the rotation and the tilt in the table's row order, the first two joined by a semicolon. The section ends
on the tilt's grazing polar Sun, and the next section opens on a definition of "Earth value", a term the
abstract, the introduction and this section have used throughout, so the next section starts afresh where the
rules ask it to inherit an actor, quantity or condition. The sentence gives 80° with its reason unstated.

Rewrite: give the day, rotation and tilt a paragraph of their own, opening on the solar-day sentence, and land it
on an Earth value the next section takes up: "The 29.53-day solar day deepens the soil's thermal wave to about
0.6 m, √29.53 ≈ 5.4 times the depth of Earth's diurnal wave, and a formula that counts per day counts nearly
thirty times as much in each lunar day; the 27.32-day rotation sets a Coriolis parameter of 5.2 × 10⁻⁶ s⁻¹ at
80° [the latitude's reason], an inertial period of 14 Earth days; and the 1.54° tilt keeps the Sun grazing at the
poles all year, where ExoPlaSim's orbit default sets Earth's tilt of 1 AD, 23.7°." Move the definition of "Earth
value" to the introduction, where the term first appears in the body (introduction.tex:27), so the next section
can open on the inventory.

### 40. MINOR — sources cited in scope that await full reading

Locations: introduction.tex:8 (mckay1991making, BLOCKED, record only); worlds.tex:75 (trenberth2005trends,
BLOCKED, record only); worlds.tex:88 (charnock1955wind, BLOCKED, abstract only). Cited for the codes'
descriptions: booij1999third, bryan2002benchmark, fierro2013implementation and mlawer2012development (BLOCKED,
abstract only), and zijlema2011swash (DEFERRED, unread).

Rules: "Claims stay within their evidence"; charter G6, recorded here for the author.

Why: The first three carry content in the scope: what McKay et al. asked, Earth's column water vapour of about
25 kg m⁻², and the roughness law. The manifest's summary list `cited_blocked` omits mckay1991making, which its own
entry marks BLOCKED.

Action: read the three content-bearing sources before release, or recast their sentences on admitted sources, and
regenerate the manifest summary.

## Paragraphs examined and found sound

These passages hold their movement and evidence; any MINOR findings on them are listed.

- `main.tex:33`, the title: it names the subject the author directed and the four codes.
- `introduction.tex:4–7`, the studies sentence: each clause checks against its source (literature table), and the
  sentence stands as a purposeful list of evidence.
- `introduction.tex:16–18` (the PlanetWRF clause) and `22–24` (ExoPlaSim): both check against their sources.
- `introduction.tex:29–30`: the need completes the second paragraph and hands "both questions" to the third.
- `introduction.tex:32–40`, the case paragraph: its order (the case, its ratios, a measured error) holds;
  findings 18–20.
- `introduction.tex:42–54`, the models paragraph: the forcing chain from the GCM to the shore orders it; finding
  21.
- `worlds.tex:29–40`, the scenario paragraph: it descends from the shield in space through the air to the ground,
  each sentence placed by the one above, and the dimming clause supplies an inferential step (a change in the
  physics appears as a change in the dimming the design needs); findings 30–32.
- `worlds.tex:55–67`, the rows of Table~\ref{tab:regime}: each value checks against `regime_calc.json`,
  `worlds.json` and claims S02, S03, S11, S12, S13 and G09.
- `worlds.tex:72–75`, the water-vapour sentence: 170 kg m⁻² matches the column mass at Earth-like specific
  humidity (7.25 × 25 ≈ 180) and claim S08.
- `worlds.tex:85`, "Gravity's surface value matters more.": an earned hinge that takes gravity from the sentence
  before.
- `abstract.tex:8`, the 32.5° skip: consistent with `regime_calc.json#sun_clock_skip`.

## Gate notes for this scope (findings only)

**G1, argument and reorderability.** The introduction's paragraphs follow an order with reasons: the studies and
their models, the ports' Earth values and the need they leave, the case, the codes, the findings; the second,
third and fourth paragraphs develop their movements. Reorderable passages: abstract 10–12 and 13–16 (findings 6,
8); introduction 9–14 (12); worlds 4–9 (26), 72–83 (34), 85–89 (37) and 92–96 (39). Purposeful catalogues: the
studies sentence (introduction 4–7), the ports sentence (16–21) and Table~\ref{tab:regime}.

**G2, audience and explanatory economy.** Delete-test failures: worlds 3–4 (25); worlds 4–9 and 85–89 repeat
Table~\ref{tab:regime} (26, 37). Terms an outside reader lacks: the abstract's "Sun clock", "lunar model day",
"convective-cover unit", "design case", "the reference", "in-house", and the "identity" and "similarity" checks
(5, 6, 7, 9); "an open project" (18); "rings of columns" (21); "found worlds" (27). Self-reference appears once,
"The work reported here" (18). The premise at introduction 26–29 earns its place: it supplies the mechanism by
which an Earth value escapes notice.

**G3, inheritance, syntax and cadence.** Boundary failures: introduction 14 to 16, "such ports" (13); the
introduction's last paragraph, which lands on the evidence state (24); worlds to assumptions (39). Coordination
over unequal propositions: abstract 7–8, 12–13 and 13–16; introduction 24–26; worlds 81–83 and 89–92. The cadence
check was silent; the read-aloud pass remains open.

**G4, affirmative stance and exact action.** "Not" and "rather than" are absent from the scope, and the remaining
negations ("little or no error", "holds none", "failed to convect", "runs without failing") follow their
propositions; finding 2 recasts the last. Empty actions: abstract 3–4, 4–5, 6 and 16–17; introduction 8, 28–29,
32, 38–39, 56, 60 and 63–65; worlds 11, 75, 86 and 93–94. Witticisms: the abstract's landing (9), "change the
planet around it" (10), "drive SWASH … up the shore" (21), "found worlds" (27) and the figure's "right here" (29).
Over-wide claims: abstract 2–4; introduction 8–9, 9–14, 24–26, 58–63 and 63–65; worlds 3–4 and 4. Promotional
framing, self-praise and caveat walls are absent; the introduction states the evidence state once, and
finding 24 moves it beside the measurements it bounds.
