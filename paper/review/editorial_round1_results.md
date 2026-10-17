# Editorial review, round 1: Verification and Results

**Reviewer.** A fresh Claude subagent (Claude Opus 5.5), started for this review with the text and its rules alone in
view. **Date.** 2026-10-17.

**Scope.** `paper/sections/verification.tex` and `paper/sections/results.tex`, with Table `tab:states` and the captions
of Figures `fig:repairs` and `fig:gap`, at commit 4d03a81 with a clean working tree.

| File | sha256 |
|---|---|
| `paper/sections/verification.tex` | a3ca68dc2de6007d42e0081a2bbbb4e1308dfea16e406b8d577fdee65ad3cfa5 |
| `paper/sections/results.tex` | a864fc868d6f3cd0aaa23015813cb2b5b7fbe214573be229c4ec3c0b7ee7bdc6 |

## What was read

**In full, before the paper.** `AGENTS.md` (e1f25bc04fd7…), its sections "The paper", "Writing" and "Review" above
all; Terluna's charter `ensemble/planning/Open_Moon_Editorial_Charter_control-01.md` (aac4a4f29402…), and in
`ensemble/planning/source_controls/`: `STYLE_NOTES.md` (659627e564bb…), `Jewish_Papers_Updated_Style_Notes.md`
(18f3d0db8a83…) and `Agent_Working_State_Editorial_Gates.md` (553e8957640a…). Their general requirements were taken;
their subject matter was set aside.

**In full, the paper.** `introduction.tex` (5d1b9cf839ea…) and `repairs.tex` (3bcef8a3a813…) for context;
`verification.tex` and `results.tex`, each whole and then sentence by sentence; `appendix.tex` (eaf27468e42b…), whose
Table `tab:verification` the verification section cites; `main.tex` (87c1cddb6bc6…).

**In part, for facts.** `paper/claims.json` (81d5ddce23c2…: S01–S08, S14, H15, H28–H32, V01–V16, G01–G15);
`paper/data/repairs.json` (d4fc5bce0b5f…) and `gap45n.json` (07f81b3860d3…); `paper/figures/figures.py`
(c4ed823173ea…, the two figure functions in scope) and the rendered `fig_repairs.png` (4bfc9570a5f5…) and
`fig_gap.png` (b8ef0b1a0aad…); `paper/references.bib` (58dbb71a3a3c…, by search); `worlds.tex` (46dc5b00bfd3…),
`assumptions.tex` (4b0f209c6aeb…), `reach.tex` (817ee9ed88c4…, lines 1–12) and `next.tex` (2c36f239634b…), by search.
From `notes/`: `verification_record.md` (983329688203…, whole), `defect_log.md` (92b3443dbe3d…: A1–A3, A6, C1–C14),
`electrification.md` (2cd81eb8edbd…: lines 40–144), `exoplasim.md` (707d97ef683d…: lines 140–286), `cm1.md`
(75502ec7070a…: lines 80–130), `waves.md` (9f7a775ed1b8…: lines 60–70, 108–120, 186–205, 236–262),
`reference_radiation.md` (348501fa28bb…: lines 14–30, 266–280). From `models/exoplasim/`: `README.md`
(9df6c4e78ba2…: lines 24–40, 60–90) and `runs.json` (59af02ab8d4b…).

**Terluna, for facts.** Working tree at f03b839; `git diff --stat 186b294 f03b839` is empty for the four files read, so
their lines match the commit the claims cite: `climate/crm/README.md` (95776d41c55b…: lines 1181–1196, 1420–1460,
1755–1780, 2064–2122, 2238–2246, 2405–2420), `climate/gcm/README.md` (267413c2aa24…: lines 1119–1160, 1209–1210),
`climate/waves/README.md` (87fe5f3621fe…: lines 1–30), `climate/waves/nearside.md` (a91e43b14998…: lines 140–170).

**Left unopened, as the brief directs.** `paper/review/` (its file names appeared in a directory listing) and
`paper/notes/`.

**Checks run.** sha256 of every file named here; read-only git commands (`rev-parse`, `log`, `status`, `diff --stat`);
a lexical screen of both files for negations, used as screening only; the two rendered figures viewed. Builds,
`lint.py` and state-changing git commands were left unused. The cadence pass was silent throughout.

**Method.** Each paragraph was read whole and then sentence by sentence, through the bead-string, inheritance,
reorderability, verb, transition, defensive-structure, redundancy and cadence passes, a names pass for terms a reader
outside the project would meet cold, and a technical pass that set each number and condition against the claims
register, the data extracts, the component notes and the Terluna records the claims cite. Every number in the two
sections agrees with its claims entry and data extract, with one exception, the convective-cover baseline in the caption
of Figure `fig:repairs` (finding 21). The rewrites below call the run the paper names "the pre-correction run" *the
Earth-orbit state* (finding 26).

**Severity.** BLOCKING: a rule breach that defeats a paragraph or misstates a fact or a condition. MAJOR: a clear breach
the author would object to. MINOR: polish.

## Findings

### 1. MAJOR · verification.tex:4–6

- **Text.** "Identity and reproduction checks test the code alone: a patch at its default leaves the arithmetic of the
  build without it unchanged along the trajectory tested, and the recorded code and results can be rebuilt."
- **Rule.** Technical meaning survives editing (reproducibility kept distinct); Claims stay within their evidence; G5.
- **Why.** In the reproduction checks, source was rebuilt, the deployed ExoPlaSim copy's two patched files and the
  Fortran of eight CM1 builds, and matched against recorded source hashes. In the repeat checks, one GCM year was killed
  and resumed, single-thread CM1 runs were repeated, and one Earth supercell was restarted on four threads and on two.
  Each reported lunar result comes from a single run, and the lunar boxes ran on several threads, where CM1 parts
  from itself (verification.tex:100;
  Table `tab:verification`, "The lunar boxes' race"; defect log A6). "results can be rebuilt" extends to the reported
  results a repeatability the checks measured for code, restarts and single-thread runs.
- **Rewrite** (the whole opening paragraph, which also repairs findings 2 and 3):

```latex
Six kinds of check were made, in three steps of distance from the code (Table~\ref{tab:verification}). Identity and
reproduction checks test the code alone: a patch at its default repeats, bit for bit along the trajectory tested, the
arithmetic of the same build before the patch; the recorded sources are rebuilt byte for byte from the pinned
archives; and a run restarted, or repeated on one thread, writes the same output. Arithmetic and similarity checks test
the code against a formula, a direct solution or itself, a similarity check comparing in dimensionless form a run at
scaled gravity, lengths and times with the original, to test whether gravity enters the code consistently.
Calibrations and benchmarks compare the code with something outside it: the reference model, on the columns a fit was
made on and a few beyond, and a scheme's published behaviour on Earth. The calibrations, similarity checks and
benchmarks each leave the lunar climate untested in their own way: the reference is a clear-sky model built on HITRAN
lines and the MT\_CKD continuum, a fit holds near its fitted state, in a similarity test Earth's empirical laws enter at
lunar gravity with their Earth coefficients, and the benchmarks were run in Earth's air.
```

### 2. MINOR · verification.tex:3–4, and the order of the section and its table

- **Text.** "Six kinds of check were made, each testing something further from the code than the one before
  (Table~\ref{tab:verification})."
- **Rule.** Claims stay within their evidence (the universal "each"); Inheritance and order (G1).
- **Why.** The next sentences pair identity with reproduction ("test the code alone") and calibrations with benchmarks
  ("compare with something outside the code"), so each pair of adjacent kinds shares one distance. The paragraphs then
  run identity, similarity, calibration, and benchmarks with arithmetic; Table `tab:verification` runs identity,
  similarity, calibration, benchmark, arithmetic. Arithmetic, second in the promised order, comes last in both.
- **Rewrite.** "Six kinds of check were made, in three steps of distance from the code (Table~\ref{tab:verification})."
  (full paragraph under finding 1), with the paragraphs and the table's groups in the same three steps: identity and
  reproduction; arithmetic beside similarity; calibration and benchmarks.

### 3. MINOR · verification.tex:7–8, 10–12, 54 (exact action)

- **Text and rewrite, item by item.**
  - 7–8, "by showing that a run at scaled gravity, lengths and times reproduces the original in dimensionless form":
    "showing" presupposes the outcome of the test the sentence defines. → "comparing, in dimensionless form, a run at
    scaled gravity, lengths and times with the original".
  - 10–12, "a clear-sky model resting on its spectroscopy", "similarity leaves Earth's empirical laws untested at lunar
    gravity", "a benchmark runs on Earth": an abstraction rests, leaves and runs. → "a clear-sky model built on HITRAN
    lines and the MT\_CKD continuum", "in a similarity test Earth's empirical laws enter at lunar gravity with their
    Earth coefficients", "the benchmarks were run in Earth's air".
  - 54, "No independent code has yet checked its carbon dioxide, oxygen, collision-induced absorption or sunlight on
    the lunar column": a code does the checking. → "Its carbon dioxide, oxygen, collision-induced absorption and
    sunlight on the lunar column have yet to be compared with an independent code."
- **Rule.** Exact action: verbs of action belong to agents that act; generic verbs name the operation.
- **Why.** In each phrase an abstraction performs an act. The section's other empty actions (66–71 "Arithmetic checks
  rebuild … place … match … hold"; 73 "The adaptation introduced"; 94–95 "tracing the failure found"; 105 "the
  calibrations rest") are repaired in the paragraph rewrites of findings 8, 11, 12 and 13.

### 4. BLOCKING · verification.tex:17–19, 23–28 (Identity and reproduction)

- **Text.** "One of them compares against the released model itself, and the other four against builds that already
  had earlier patches, so the chain back to the release closes through those patches' own identities;" and "The Sun
  clock, the water scaling, and the curved-air, gas-band and longwave patches (07--09) were written to reproduce the
  released code at their off settings, and have yet to be run that way."
- **Rule.** G5 (an evidence state misstated); Claims stay within their evidence; Inheritance and order (G1, G3).
- **Why.** `models/exoplasim/runs.json` records the baselines. The infrared-from-space run
  (`A28_cal_control_patched`, patches 01–06) compares with `A28_cal_control` (01–05), and the ice-optics run
  (`A28_corrected_970_lwcheck_rebuilt`, 01–10) with `A28_corrected_970_lwcheck` (01–09). Their chains back to the
  release pass through patches 04, 05 and 07–09, the patches the paragraph's own last sentence lists as unrun at their
  off settings; the chain closes for patches 01–03 alone, and the "so" clause states more than the runs tested. The
  gap is stated four sentences after the claim it bounds, with the CM1 and SWAN sentence and the rebuild sentence
  between them, and those two sentences trade places without loss: an inventory that Table `tab:verification` already
  holds. Three facts in the record bear on the results and stay out of the text: the water scaling's identity at its
  default follows from arithmetic for this spectrum (`notes/verification_record.md`:48–50); of the states in Table
  `tab:states`, the uncalibrated and first calibrated runs predate source hashing, and the convective-cover run
  compiled a draft of patch 03 whose committed form repeats its first year (`models/exoplasim/README.md`:84–90); and
  the rebuild covers the deployed copy's two patched sources, `radmod.f90` and `rainmod.f90` (README:30–33), where the
  text says "the deployed ExoPlaSim installation".
- **Rewrite.**

```latex
\textbf{Identity and reproduction.} Five ExoPlaSim runs, each a model year from one restart, repeat byte for byte the
restart of the same build before the patch, with the patch at its neutral setting: the Rayleigh and continuum
calibration at the released values, the cloud-water and convective-day patches, infrared from space at zero, and the
ice optics off. The first three link back to the released model in sequence, each run against a build that holds only
the patches checked before it. The infrared and ice-optics runs compared against builds that already held patches 04
and 05, and for the ice optics 07--09 as well; those patches were written to reproduce the released code at their off
settings and have yet to be run that way, so the chain from these two checks back to the released model is complete
once they are, and for the water scaling (05) at its default the identity already follows from arithmetic on this
spectrum.\claim{V01} Applied to the pinned upstream archives, the patch series rebuild byte for byte the two patched
sources of the deployed ExoPlaSim copy and the Fortran of the eight lunar CM1 builds used for the results, and
prefixes of the ExoPlaSim series reproduce the source hashes of 32 of the 34 GCM runs that recorded one; of the states
in Table~\ref{tab:states}, the uncalibrated and first calibrated runs predate source hashing, and the convective-cover
run compiled a draft of patch 03 whose committed form repeats its first year byte for byte.\claim{V03} A GCM year
killed a minute in and resumed repeats the uninterrupted year's restart and every variable of its output. CM1 repeats
bit for bit on one thread and parts from itself on several, where the lunar boxes ran, so each box run is one
realisation; Table~\ref{tab:verification} lists the CM1 and SWAN identity checks.\claim{V02}
```

### 5. MINOR · verification.tex:20–21, 51–53 (recorded checks)

- **Text.** "In CM1 the tilted-ring patches and the local-time advection repeat an existing run's first model day bit
  for bit" and "the line-by-line model has two checks against other codes: PyRADS, for longwave with water vapour alone
  at constant gravity, and a Monte Carlo reference for Rayleigh scattering up to an optical depth of 1.5".
- **Rule.** File and evidence practice ("Report actual checks"); G5; a named code is cited.
- **Why.** The verification record's search found the two `ring_80n_lsw` comparisons in Terluna's written record alone
  (`notes/verification_record.md`:73), and the reference note records the PyRADS and Monte Carlo results as numbers in
  `validation.json` alone, with the harness that made them outside the repository (`notes/reference_radiation.md`:
  22–24). The text reports both in the voice of checks that can be rerun. PyRADS appears uncited, while its source,
  `koll2018earth`, is in `references.bib` and in `sources/originals/` and goes uncited throughout the sections; the
  Monte Carlo reference is unsourced.
- **Rewrite.** In the table row or the sentence that names the CM1 check: "by Terluna's record, which keeps the
  comparison's text alone". For the reference: "…and the line-by-line model has two checks against other codes,
  recorded as numbers alone and beyond rerunning from the repository: PyRADS \autocite{koll2018earth}, for longwave
  with water vapour alone at constant gravity, and a Monte Carlo reference for Rayleigh scattering [its source] up to
  an optical depth of 1.5, where the lunar column's Rayleigh depth is about 4 at 360~nm."

### 6. MAJOR · verification.tex:30, 36–38 (Similarity)

- **Text.** "The strongest evidence about gravity comes from the similarity checks." and "Each lunar wave run is
  therefore the gravity-scaled image of an Earth run with the same Earth-fitted coefficients, and whether those
  coefficients hold on lunar seas is untested."
- **Rule.** Claims stay within their evidence (the universal "Each"; an unscoped "strongest"); Write for the
  expert (an evaluative opener tells the reader what to conclude); a qualification attaches once.
- **Why.** The opener ranks evidence about gravity in general, and the paragraph's own last sentence reports that CM1's
  similarity pair failed to convect, so the ranking holds for the wave models alone. The SWAN similarity test exercised
  Komen input and whitecapping with Wu drag at a fixed wind, AGROW, DIA and depth breaking on Cartesian strips started
  from rest; spherical geometry, nesting and stationary iteration were checked separately or left unchecked
  (`notes/waves.md`:62–68). The lunar runs are spherical, nested and forced by the GCM's stress, so the words "Each
  lunar wave run" claim for untested paths what the tests established for tested ones. The second clause repeats the
  opening paragraph's statement about Earth's empirical laws (11–12) and the results' last sentence
  (results.tex:133–134). "misses its Earth twin" (32) coins a name for the scaled Earth run (finding 35).
- **Rewrite.**

```latex
\textbf{Similarity.} Stock SWAN, run at a sixth of Earth's gravity with lengths, depths and durations six times longer
and frequencies six times lower, differs from the Earth run it scales by 5.44\% in significant wave height and 3.91\%
in mean period; patched, it differs by 0.303\% and 0.326\%, against a 1\% criterion.\claim{V04} SWASH reproduces the
linear dispersion relation within 1.76\% in amplitude and 0.289\% in phase at lunar, four times lunar and Earth
gravity, preserves a linear waveform to 0.0009\% of its amplitude when gravity quadruples and the clock halves, and,
under the same scaling with breaking and a moving shoreline, changes its 98th-percentile run-up by 1.20\%.\claim{V05}
On the code paths these tests exercise, Komen growth and whitecapping under a fixed wind, DIA, the wind-input knee and
depth breaking on Cartesian strips started from rest, a lunar wave run is therefore an Earth run scaled in gravity with
Earth's coefficients; the lunar runs' spherical grids, nests and GCM forcing were checked separately or left
unchecked. CM1's gravity-scaled microphysics remains untested this way: the pair of runs designed to measure how far
lunar convection departs from Earth's stretched sixfold failed to convect.\claim{V06}
```

### 7. MAJOR · verification.tex:42–55 (Calibration and the reference)

- **Text.** "The calibrations hold on the columns they were fitted to and a little beyond."
- **Rule.** Claims stay within their evidence (a universal over every calibration); G5 (which version was checked);
  Inheritance and order (swap test).
- **Why.** The two beyond-fit checks that follow concern the split of sunlight in its fit of 2026-09-29
  (`SWH2OSCALE` 1.356, `RAYSCALE` 2.215; `notes/verification_record.md`:154), which the gas-band refit replaced (1.292,
  2.237; Table `tab:repairs`). The design case's calibration is known through its fit residuals, the gas bands have
  their residuals alone, and the longwave correction's accuracy beyond its 295 K fit is open (lines 107–108). The
  universal therefore rests on one calibration in an earlier version. The RRTMG sentence (45–49) reports a check of an
  uncalibrated scheme between the calibrations' evidence and the reference that bounds them, and it moves to the end of
  the paragraph without loss, so it interrupts the paragraph's relation from calibration to reference.
- **Rewrite.**

```latex
\textbf{Calibration and the reference.} Of the calibrations, the split of sunlight has been tested beyond its fit, in
the version fitted before the gas bands: on eleven columns outside the fit's set it held within 0.6 points rms, and a
303~K column carrying 338~kg\,m$^{-2}$ of vapour, warmer and wetter than any fitted, fell 0.7 points short, where the
scheme before its water recalibration fell 9.7 short.\claim{V07} The refit with the gas bands and the longwave
correction are known through their fit residuals (Table~\ref{tab:verification}). Every calibration is clear-sky,
PlaSim's clouds remain uncalibrated, and the accuracy of each is bounded by the reference's own. The reference's
correlated-$k$ emulation reproduces the line-by-line outgoing longwave within 0.4--1.4~W\,m$^{-2}$, and the
line-by-line model has two checks against other codes, recorded as numbers alone and beyond rerunning from the
repository: PyRADS \autocite{koll2018earth}, for longwave with water vapour alone at constant gravity, and a Monte
Carlo reference for Rayleigh scattering [its source] up to an optical depth of 1.5, where the lunar column's Rayleigh
depth is about 4 at 360~nm. Its carbon dioxide, oxygen, collision-induced absorption and sunlight on the lunar column
have yet to be compared with an independent code.\claim{V16} Against the same reference RRTMG, checked and left
uncalibrated, lies within 2.5 points of the line-by-line shares of reflected, air-absorbed and ground-absorbed
sunlight at the site where the rings cross the
equator at 0\textdegree~E, and on 990 cloud-free columns of the 45\textdegree\,N ring cools the air more than the
correlated-$k$ model does, by 4.5~W\,m$^{-2}$ in the lowest 1.8~km, 8.5 at 1.8--6.5~km and 10.2 at
6.5--13.7~km.\claim{V08}
```

### 8. MAJOR · verification.tex:57–71 (Benchmarks and arithmetic)

- **Text.** The paragraph, ending "Arithmetic checks rebuild the uneven sunlight of the Sun-clock defect from PlaSim's
  solar-position arithmetic with correlation 1.0000, place a tilted ring's Sun within $8\times10^{-7}$ of the spherical
  formula and its Coriolis parameter within $3\times10^{-12}$~s$^{-1}$ of $2\Omega\sin\phi$, match the field solver to a
  direct solve to one part in $10^5$, and hold the curved-air ledger's channels within 0.9~W\,m$^{-2}$ of the fine
  spectral grid in every layer with the Sun overhead."
- **Rule.** Sentences carry their dependencies (bead string; a genuine catalogue goes in a table or a list); Exact
  action; Technical meaning (a number missing its quantity).
- **Why.** The heading names two kinds that the opening paragraph places at opposite ends, a benchmark outside the
  code and arithmetic inside it. The conductivity sentence and the arithmetic sentence trade places with the benchmark's
  sentences without loss, and the paragraph ends on a four-item inventory whose subject, "Arithmetic checks", rebuilds,
  places, matches and holds, operations of the code or of the people who ran it. The quantity and unit of
  "$8\times10^{-7}$" are missing; the record calls it the Sun's elevation. The conductivity check is filed under
  arithmetic in `claims.json` (V11, state "implementation") and under benchmarks in Table `tab:verification`.
  Findings 9 and 10 cover the published runs and the conductivity sentence.
- **Rewrite.** A benchmark paragraph that develops one relation, the graft behaving as the published scheme does on
  Earth with one divergence traced to its cloud ice, and the arithmetic checks moved beside similarity as a list or into
  the table alone:

```latex
\textbf{Benchmarks on Earth.} In the Weisman--Klemp supercell \autocite{weisman1982dependence} the electrified graft
stays within 6\% of CM1's own NSSL scheme in its largest updrafts, within 3.4~dBZ in reflectivity at every half hour
and within 9\% in condensate, and its hail differs by up to a factor of two, the two copies being different versions of
the scheme.\claim{V09} Beside published runs of the same charging and lightning schemes on similar storms
\autocite{macgorman2001lightning,[the other runs, once admitted]}, the storm flashes first at 28.5 minutes, where those
runs flash first at 27--40 minutes, and its flash rates and median charge per flash fall inside their ranges; with
WRF-ELEC's ground rule on, 1.1\% of its flashes strike the ground, against 0.33\% in [Salinas et al.]'s run of
[Brothers et al.]'s storm. The storm separates charge several times faster than the published storms do, a difference
traced to cloud ice reaching $2\times10^8$ crystals per kilogram where droplets freeze homogeneously in
50~m\,s$^{-1}$ updrafts.\claim{V10} In the lunar runs the code leaks charge through a conductivity column whose ion
chain, run for Earth at a geomagnetic cutoff rigidity of 3~GV, reproduces Earth's measured fair-weather positive
conductivity within 2--8\% from 5 to 30~km.

\textbf{Arithmetic.} Four implementations were compared with the arithmetic they encode:
\begin{itemize}
\item rebuilt from PlaSim's solar-position routine alone, the uneven sunlight of the Sun-clock defect correlates with
  the run's at 1.0000;
\item a tilted ring's solar elevation agrees with the spherical formula to $8\times10^{-7}$ [unit], and its Coriolis
  parameter with $2\Omega\sin\phi$ to $3\times10^{-12}$~s$^{-1}$;
\item the field solver agrees with a direct solve to one part in $10^5$;
\item with the Sun overhead, the curved-air ledger's channels come within 0.9~W\,m$^{-2}$ of the fine spectral grid in
  every layer.\claim{V11}
\end{itemize}
```

### 9. MAJOR · verification.tex:60–63 (published runs uncited)

- **Text.** "Against published runs of the same charging and lightning schemes, the first flash comes at 28.5 minutes
  against a published 27--40, and the flash rates and the median charge per flash fall within the published ranges;
  with WRF-ELEC's ground rule on, 1.1\% of flashes struck the ground, against 0.33\% in a published run."
- **Rule.** Claims stay within their evidence (a statement about published work names the works and is scoped to
  them); G5, with source admission under G6.
- **Why.** The sentence is uncited. Terluna's record (`climate/crm/README.md`:1760–1771) draws the ranges from
  MacGorman et al. 2001, Kuhlman et al. 2006, Ziegler et al. 2014, Sun et al. 2023, Mansell 2014, Brothers et al. 2018,
  Calhoun et al. 2014 and Salinas et al. 2021; the bounds come from particular runs (27 min from Kuhlman et al., 40 from
  Sun et al., 0.33% from Salinas et al. on Brothers et al.'s storm). Of these, `references.bib` holds MacGorman et al.
  2001 alone (`macgorman2001lightning`, cited at repairs.tex:141).
- **Rewrite.** The second sentence of the benchmark paragraph under finding 8, with each run admitted and cited where
  its number enters.

### 10. MAJOR · verification.tex:65–66 (conductivity)

- **Text.** "The lunar conductivity column reproduces Earth's measured fair-weather positive conductivity within
  2--8\% from 5 to 30~km at a 3~GV cutoff."
- **Rule.** Technical meaning survives editing (the object and condition of a check); Write for the expert (a term from
  another field enters through its use).
- **Why.** The check ran the column's ion chain for Earth: "The ion chain reproduces Earth's measured fair-weather
  positive conductivity within 2–8% from 5 to 30 km at a 3 GV cutoff" (`notes/electrification.md`:114–116). The
  sentence makes the lunar column reproduce an Earth measurement, which misstates the object and leaves the Earth
  condition implicit. "a 3 GV cutoff" is a geomagnetic cutoff rigidity, a cosmic-ray term this reader may lack, and the
  sentence omits the use that justifies the check, the leakage in the lunar runs (Table `tab:repairs`).
- **Rewrite.** "In the lunar runs the code leaks charge through a conductivity column whose ion chain, run for Earth at
  a geomagnetic cutoff rigidity of 3~GV, reproduces Earth's measured fair-weather positive conductivity within 2--8\%
  from 5 to 30~km."

### 11. MAJOR · verification.tex:73–92 (What the checks caught)

- **Text.** "\textbf{What the checks caught.} The adaptation introduced defects of its own, found by these checks or in
  the course of the work." … "The last two remain in the runs made before they were found."
- **Rule.** Inheritance and order (swap test; a genuine catalogue goes in a table); headings say what they name; Exact
  action; G5 (a defect's reach into reported results).
- **Why.** Ten defects follow one another model by model, and their sentences trade places without loss. The heading
  names the checks as the finders, while the first sentence and the record name other routes for several: a code
  review found the ventilation (line 81), the sounding came to light while columns were chosen for a radiation check
  (defect log C4), and the mixed builds came from a reading of the build records (C8). In "The adaptation introduced"
  an abstraction performs the act. At the landing the reader must identify both the defects and the runs: the
  constant-vapour sounding is in every CM1 case set up before 2026-10-17 (C4), which takes in every CM1 run behind the
  results, and its effect was examined on the 45°N rings alone. The paragraph's account of the ventilation
  ("until a code review found the omission") reads as closed, while the Takahashi windows of the storm results ran on
  2026-10-05, before the repair of
  2026-10-06 (C12; Terluna `climate/crm/README.md`:2072–2073). The first-channel defect fed the curved-air and gas-band
  runs that the results report as repair effects (finding 19).
- **Rewrite.** Sort the defects by what they leave in the reported results:

```latex
\textbf{Defects of the adaptation.} The patches and runners written for the Moon contained defects of their own, found
by these checks, by code review or in the course of the work. Six were removed before the runs reported here: the GCM
runner's first solar spectrum, whose tail held its last value past 2.73~\textmu m, put 86\% of the sunlight in the near
infrared and warmed the first run past 320~K;\claim{H28} the first electrified build discharged once per step after all
the step's charging, multiplied memory the scheme had left unset and made private a variable its threads shared; the
first terrain build placed its forcing by a corner column 2.9~km up; and the sky solver's production grid of 114
channels absorbed 58\% too much sunlight above 500~nm with the Sun overhead, which had made PlaSim look short of its
calibration. Four remain in reported runs. The curved-air ledger's first channels, bisected on the whole column alone,
put near-infrared sunlight too high, 19.0 against 10.7~W\,m$^{-2}$ at 66--85~km, and the curved-air and gas-band runs of
Table~\ref{tab:states} ran on them.\claim{H30} Every CM1 case set up before 2026-10-17, and so every CM1 run reported
here, started from soundings that held the vapour of the GCM's top level, near 130~km, constant above it; on the
45\textdegree\,N rings, the only cases examined for it, the air began 6--15 times saturated over ice at 140--150~km and
every column kept 1.1~g\,m$^{-2}$ of ice above 107~km through both lunar days. The first lunar gravity patch scaled the
NSSL fall speeds and left the ventilation tied to them at Earth's values, so that lunar rain evaporated 1.3--1.5 times
too fast for its size; a code review found the omission after the Takahashi windows of the storm results had run and
before the main electrified run began.\claim{H29} The 45\textdegree\,N rings with and without the curved-air terms ran
on builds compiled at different optimisation levels, so their 0.013--0.021~K difference falls below what the pair
resolves.\claim{H31}
```

### 12. BLOCKING · verification.tex:94–102 (Checks that fell short)

- **Text.** The paragraph: SWAN with breaking off; SWAN's early growth; SWASH's irregular-input control; CM1 rebuilt
  and on several threads; the ledger's scattering orders.
- **Rule.** G1 (disconnected evaluation items are a blocking failure); Sentences carry their dependencies (bead
  string); Inheritance and order (swap test).
- **Why.** Five shortfalls in four models follow one another as equal-weight declaratives. Every sentence can move to
  any position without loss, and the paragraph ends on its fifth item, a list's end in place of a landing. The items
  differ in weight and consequence, and the text leaves that difference unrecorded: two concern reported wave results;
  one, the divergence on several threads, concerns every paired box comparison; one was traced to a defect that every
  run avoids; and one is negligible ($3\times10^{-4}$). Table `tab:verification` already lists most of them.
- **Rewrite.**

```latex
\textbf{Checks that fell short.} Three of the five shortfalls concern reported results. SWAN's early growth depends on
the time step: halving it changes the first hours' wave height by up to 33\%, while the 48-hour endpoints move under
0.3\%, and in the weather runs small seas fail their 5\% time-step criterion where seas above 1~m pass, so the step's
error is concentrated in the sea states below 1~m. SWASH's control with irregular input, the kind of input from which
the Smythii run-up was computed, misses its 5\% bound, at 5.22\% in height and 6.28\% in period.\claim{V12} CM1 rebuilt
at a higher optimisation departs from its first build by 0.28--0.32~\textdegree C rms in the air at 2~m within a model
day, inside the spread of last-bit nudges, and on several threads, where the lunar boxes ran, it departs from itself,
so two box runs that differ in one setting compare as realisations. The other two shortfalls were traced or bounded:
SWAN with depth breaking off failed its repeatability test by about 2.5\%, a failure traced to the uninitialised
breaker parameter and avoided in every run by keeping breaking on; and the ledger's scattering orders reached their cap
in one channel of 282, whose omitted tail is about $3\times10^{-4}$ of that channel's diffuse light at the
ground.\claim{V13}
```

### 13. MAJOR · verification.tex:104–111 (Checks still to make), and the section's repeated qualifications

- **Text.** "The longwave correction, fitted at 295~K, ran in a test that settled near 307~K with twice the water
  vapour, and its accuracy there is unchecked. The twilight pair lacks a control on the same build and an estimate of
  its realisation noise. CM1's thread race remains unlocated, RRTMG's extrapolation past its tables and CM1's
  gravity-scaled microphysics remain untested on their own, and an independent GCM has yet to run the scenario."
- **Rule.** Inheritance and order (a genuine catalogue goes in a table or a list); Say what is (a qualification
  attaches once to the claim it bounds; caveat walls); G1, G4; Technical meaning ("settled").
- **Why.** Eight open checks follow one another in an arbitrary order, and any two sentences trade places. Five
  repeat qualifications the text has already attached: the reference's independent check (10–11, 54–55), CM1's
  microphysics similarity (38–40), the curved-air pair's builds (89–91), the 307 K state (results.tex:72–73) and the
  thread race (100; repairs.tex:33–35). Read with those, the section states its open checks two or three times over, a
  caveat wall assembled from repetitions. "settled near 307~K" misstates the run's state: it ends at 306.77 K in year
  19, warming 0.08 K a year, and extrapolates to 306.8–307.1 K (claims G13), as the results and the caption of Figure
  `fig:repairs` say. Table `tab:verification`'s "Leaves open" column lacks three of the eight: CM1 forced from the
  longwave-corrected GCM, an independent GCM, and the curved-air pair's control.
- **Rewrite.** Add the three missing items to the table's "Leaves open" column, keep each qualification at the claim it
  bounds, and let the paragraph rank the open checks by the results they would test:

```latex
\textbf{Checks still to make.} Of the open checks, two would test the headline results: forcing CM1 from the
longwave-corrected GCM would test whether the corrected physics closes the 3.7~K gap at 45\textdegree\,N, and refitting
the longwave correction near 307~K, where its test was still warming slowly with twice the water vapour of the 295~K
fit, would test that state. The others, an independent radiation code on the full design column, an independent GCM
run of the scenario, a same-build control for the CM1 curved-air pair, the location of CM1's thread race, and tests of
RRTMG's extrapolation and of CM1's gravity-scaled microphysics, are listed in Table~\ref{tab:verification}, each beside
the check it would extend.\claim{V14}
```

### 14. MINOR · results.tex:3–5 (opening)

- **Text.** "The first results of the adapted models are sensitivities: how far the case's climate moves when each
  Earth value is removed, and which of the values that remain move it most."
- **Rule.** Claims stay within their evidence ("each Earth value"); an opening promises what the section develops (G1).
- **Why.** Sensitivities fill the first two paragraphs; the gap between the models, rain, storms and seas are model
  results under particular GCM states. The removed Earth values are the seven of Figure `fig:repairs`, a part of
  Table `tab:inventory`.
- **Rewrite.** "The case's results are of two kinds: sensitivities, measured as the change in its climate as Earth
  values were removed one repair at a time and as values that remain were varied, and the climate that CM1, SWAN and
  SWASH compute when forced from the GCM. Table~\ref{tab:states} lists the GCM states behind both, by the names used
  below, and the state that forced each CM1 and wave result."

### 15. MINOR · results.tex:9, 19 (Table caption against its first row)

- **Text.** Caption: "surface temperatures are global means over the years given." Row: "To 12; 315.5~K, warming".
- **Rule.** Technical meaning survives editing (the averaging window).
- **Why.** For the uncalibrated run 315.5 K is the value in model year 12 of a run still warming (claims H15, G14), a
  single year.
- **Rewrite.** Row: "Year 12; 315.5~K, warming". Caption: "…surface temperatures are global means over the years
  given, or in the single year given for the uncalibrated run, still warming."

### 16. BLOCKING · results.tex:19–23 (Table `tab:states`) and 33–39

- **Text.** Row 23, "What it adds": "Both cloud repairs, with PlaSim's Sun clock and Earth's orbit". Prose: "On the
  first calibrated run, counting cloud water by pressure warmed the Moon by 2.3~K over the years averaged and about
  2.5~K as the run settled, and counting convective rain per Earth day warmed it by a further 1.8~K, about 1.6~K
  settled."
- **Rule.** Technical meaning survives editing; G5 (each result tied to the GCM state that produced it).
- **Why.** Every run before 2026-09-29 ran with PlaSim's Sun clock (defect log A1), and every run's log, the
  calibration runs' included, reported Earth's orbit, obliquity 23.695° (A2). The four 25% states, the full-column
  bound and the pre-correction state all ran with both. The table names them in the fifth row's "What it adds" column,
  where they read as entering there, and the prose for the first calibration (at least 20 K) and the two cloud repairs
  (2.3 and 1.8 K) omits both. The next sentence of the paragraph reports what the Sun clock and tilt do to the rain
  (2.91 to 2.24 mm a day, dry land from 9 to 42%), so the cloud repairs' effects were measured in a climate with
  Earth's seasons, whose summer rain reached 60° (A2).
- **Rewrite.** Caption, added: "The four 25\% states, the full-column bound and the Earth-orbit state ran with PlaSim's
  Sun clock and Earth's orbit, which the Sun-and-tilt state replaced." Row 23, "What it adds": "Both cloud repairs".
  Prose:

```latex
\textbf{What each repair changed.} Fitting the first calibration cooled the climate more than any later change. In the
first design runs, with 25\% seas under the undimmed shield and with PlaSim's Sun clock and Earth's orbit, the
uncalibrated run passed 310~K and was still warming at 315.5~K in model year 12, while the same configuration,
calibrated, settled at 295.5~K, at least 20~K cooler.\claim{H15}\claim{G14} The later repairs' effects on the
global-mean surface temperature are plotted beside the sensitivity tests in Figure~\ref{fig:repairs}, each pair of runs
averaged over the years of Table~\ref{tab:states}, several of them still drifting. On the first calibrated run, still in
Earth's seasons, counting cloud water by pressure warmed the Moon by 2.3~K over the years averaged and about 2.5~K as
the run settled, and counting convective rain per Earth day warmed it by a further 1.8~K, about 1.6~K
settled.\claim{G01}
```

### 17. MINOR · results.tex:33–37, 75–76 (exact action)

- **Text and rewrite, item by item.**
  - 33, "The first calibration moved the climate furthest": a calibration performs the act. → "Fitting the first
    calibration cooled the climate more than any later change" (in finding 16's rewrite).
  - 35–37, "Figure~\ref{fig:repairs} sets the later repairs' effects … beside the sensitivity tests, each pair of runs
    averaged over set years": a figure sets, and "set years" leaves the windows unnamed. → "The later repairs' effects
    on the global-mean surface temperature are plotted beside the sensitivity tests in Figure~\ref{fig:repairs}, each
    pair of runs averaged over the years of Table~\ref{tab:states}".
  - 75–76, "forcing CM1 from the GCM allowed the disagreement to be taken apart": the generic "allowed" in place of the
    operation. → "and with CM1 forced from the GCM the disagreement was taken apart term by term".
- **Rule.** Exact action; generic analytical verbs earn their place.
- **Why.** In each phrase an abstraction acts, or a generic verb replaces the operation. The other empty actions in
  the results, "the geometry removed" (43), "a cloud-free column moves its ground" (44–45), "Earth fits … move the
  Moon" (62),
  "resting on" (72), "Rain shows" (91), "rests on" (94), "SWAN raises" (127) and "come with" (133), are repaired in
  findings 19, 22, 23, 28 and 34.

### 18. MINOR · results.tex:39–42 (the drying and its mechanism)

- **Text.** "From the pre-correction run, the Sun clock, the Moon's own tilt and the recalibrated split of sunlight
  warmed the Moon by only 0.6~K, yet cut its rain from 2.91 to 2.24~mm per day and raised the share of land receiving
  under 0.5~mm per day from 9 to 42\%."
- **Rule.** Each paragraph develops a mechanism or consequence; Write for the expert (supply the inferential step the
  reader lacks).
- **Why.** The sentence reports the largest change in the rain field in the section and stops at the numbers. The record
  holds the mechanism and most of the separation: under Earth's seasons summer rain had reached 60°, and the Sun and tilt
  alone gave 36% of land dry within two years (defect log A2).
- **Rewrite.** "From the Earth-orbit state, the Sun clock, the Moon's own tilt and the recalibrated split of sunlight
  warmed the Moon by 0.6~K and cut its rain from 2.91 to 2.24~mm per day, and the land receiving under 0.5~mm per day
  grew from 9 to 42\%, 36\% within two years of the Sun and tilt alone: with Earth's 23.7\textdegree\ tilt, summer rain
  had reached 60\textdegree.\claim{G02}"

### 19. BLOCKING · results.tex:42–46, with Table rows 25–26 and Figure `fig:repairs`

- **Text.** "The curved air then cooled it by 0.65~K, its clouds offsetting in the first year 3.5 of the
  5.4~W\,m$^{-2}$ that the geometry removed from the clear sky, and the carbon dioxide and oxygen bands cooled it by a
  further 2.2~K, mostly through PlaSim's high cloud, since a cloud-free column moves its ground only 0.57~K: the high
  deck fell from 16 to 12\% of the sky, and the top layer's cirrus from 2.0 to 0.05\% as that layer warmed by 7~K."
- **Rule.** Technical meaning survives editing; G5 (a result tied to its conditions: the code state, settled or
  drifting).
- **Why.** Both runs, `A28_dim5_moon_geometry` and `A28_dim5_moon_geometry_gases`, ran on the ledger's first channels,
  which put near-infrared sunlight too high, 19.0 against 10.7 W/m² at 66–85 km and 27.7 against 35.1 at 35–49 km with
  the Sun overhead, and both remain on those channels (defect log C3). The design case uses the corrected terms only in
  combination with the bands and the eased dimming, so each repair's corrected form appears in that combination
  alone. Under the heading "What each repair changed", in the figure's group "Repairs" and in this sentence,
  −0.65 K and −2.2 K read as the repairs' effects; the table's words "the ledger's first channels" and the
  verification's defect sentence a section
  earlier are the only signs. The gas-band run was still cooling 0.3 K a decade over its averaged years
  (`paper/data/repairs.json`), and the prose leaves its drift unstated while it states settled values for the 25% runs.
  The 5.4 W/m² is a first-channels, first-year GCM figure, repairs.tex states −6.5 and +0.7 W/m² for the corrected
  design column, and the text leaves the two unlinked; "a cloud-free column moves its ground" leaves the column and
  the calculation unnamed.
- **Rewrite.** Table row 25: "Curved-air terms from the ledger's first channels, which put near-infrared sunlight too
  high"; row 26: "Carbon dioxide and oxygen bands, on the first channels". The figure marks the two bars "first
  channels", or the caption says so (finding 21). Prose:

```latex
The curved air, on the ledger's first channels, which put near-infrared sunlight too high in the middle atmosphere,
then cooled it by 0.65~K, its clouds returning in the first year 3.5 of the clear sky's 5.4~W\,m$^{-2}$ loss under
those terms. On the same channels the carbon dioxide and oxygen bands cooled it by a further 2.2~K over years 10--19,
still cooling 0.3~K a decade, mostly through PlaSim's high cloud: computed cloud-free, the column's ground moves
0.57~K with the bands, while the high deck fell from 16 to 12\% of the sky and the top layer's cirrus from 2.0 to
0.05\% as that layer warmed by 7~K.\claim{G03} The corrected terms have run only together with the bands and the eased
dimming, in the design case.
```

### 20. MAJOR · results.tex:46–47 (the design temperature, held by tuning)

- **Text.** "With the ledger's corrected terms and the dimming eased from 5.0 to 3.0\%, the design case settles at
  295.0~K, with 2.31~mm of rain a day."
- **Rule.** G5 (a tuned target presented as an outcome); a condition stated once, far away.
- **Why.** worlds.tex:31–33 states that the scale 0.970 was "chosen so that the GCM's global-mean surface settles at the
  design temperature of 295 K; a change in the physics therefore appears as a change in the dimming the design needs",
  and Terluna's record says "The design temperature needs a sunlight scale near 0.970" (`climate/gcm/README.md`:1157).
  Here the sentence reads as the outcome of the corrections, and the paragraph's consequence, the dimming the corrected
  physics needs, goes unstated at the point where the worlds section said it would appear.
- **Rewrite.** "Holding the design temperature on the ledger's corrected terms with the gas bands took easing the
  dimming from 5.0 to 3.0\%, and at that dimming the design case settles at 295.0~K, with 2.31~mm of rain a
  day.\claim{G04}"

### 21. BLOCKING · results.tex:52–58 (caption of Figure `fig:repairs`)

- **Text.** "the first calibrated run for the cloud water, the convective cover and the full-column bound;"
- **Rule.** Technical meaning survives editing (a figure's baseline misstated).
- **Why.** In `paper/data/repairs.json` the convective cover's baseline is `A_earth_path_clouds`, the cloud-water run
  (years 10–14, 297.812 K), and the plotted +1.76 K is the change from that run, as the prose's "a further 1.8 K" says.
  Against the first calibrated run (295.511 K) the bar would read +4.07 K. Two smaller points: "each general repair and
  calibration after the first" leaves out, by the paper's own classes, the curved air, a general method with a lunar
  table (Table `tab:repairs`); and the figure labels its bar "Curved air: twilight, cone and slant path", with a "cone"
  that the caption and the text leave undefined.
- **Rewrite.**

```latex
\caption{Change in the global-mean surface temperature from each repair after the first calibration, and from four
sensitivity tests, each against its own baseline in Table~\ref{tab:states}: the first calibrated run for the cloud
water and the full-column bound; the cloud-water run for the convective cover; the Earth-orbit state for the Sun, the
tilt and the split; the Sun-and-tilt run for the curved air and the two cloud settings; the curved-air run for the gas
bands; and the design case for the longwave test. The curved-air and gas-band runs used the ledger's first channels.
Bars are means over the years in Table~\ref{tab:states} and the accompanying data, against each baseline's own years;
several runs were still drifting, and the longwave test extrapolates to balance at 306.8--307.1~K.\claim{G13}}
```

  In the figure, "cone" becomes "shell widening", the term repairs.tex:81–82 uses.

### 22. MAJOR · results.tex:62–66, 69–72 (the cloud settings)

- **Text.** "The Earth fits that remain in PlaSim's clouds and longwave move the Moon further than any general repair
  did. Two of PlaSim's Earth-tuned cloud settings, varied as tests from the Sun-and-tilt run, move it as far as the
  general repairs do or further: thinner convective cloud warms it by 1.7~K over the years averaged and about 2.2~K as
  the runs settle, and more low cloud cools it by 5.0~K and about 5.9~K, …"
- **Rule.** Claims stay within their evidence ("any"); a comparison states its baseline; Exact action.
- **Why.** The topic sentence says "further than any general repair"; the next sentence says "as far as … or further";
  the numbers bear out the second, since thinner convective cloud (+1.7 K, about 2.2 K settled) moves the surface less
  than cloud water by pressure (+2.3 K, about 2.5 K settled). The comparison's baseline is the size of each test, and
  the text omits it: Terluna's record (`climate/gcm/README.md`:1209–1210) counts convective cover per 2,400 s, "the
  convective cloud near its floor", and lowers the lowest layer's cloud threshold from 0.983 to 0.6, each to test an
  explanation of the gap between the models. A setting's effect grows with how far it is pushed, so both "as far as the
  general repairs" and the later "least certain in its cloud amount" (69–72) depend on the ends chosen. In "Earth fits …
  move the Moon" an abstraction performs the act, with the Moon as its object.
- **Rewrite.** Delete the topic sentence (62) and write:

```latex
Changing two of PlaSim's Earth-tuned cloud settings from the Sun-and-tilt run, each to an end chosen to test an
explanation of the gap between the models, moves the global mean as far as the general repairs do or further: counting
convective cover per 2,400~s, which holds the convective cloud near its floor, warms the Moon by 1.7~K over the years
averaged and about 2.2~K as the run settles, and lowering the lowest layer's cloud threshold from 0.983 to 0.6 cools it
by 5.0~K and about 5.9~K, while cloud water at its full-column bound cools the first calibrated run by 3.2~K and about
3.5~K.\claim{G05}
```

  and at 69–72: "Given the reference's spectroscopy, and with the cloud settings at the ends chosen for these tests, the
  case's climate is therefore least certain in its cloud amount and in the height at which its longwave cools the air,
  both set by Earth fits open to constraint by cloud-resolving runs, the reference model and an independent GCM."

### 23. MINOR · results.tex:66–73 (the longwave test's conditions and the paragraph's landing)

- **Text.** "toward a balance near 307~K with twice the water vapour, 348 against 170~kg\,m$^{-2}$, and cloud over 38\%
  of the sky in place of 20\%, most of the gain in high cloud." and "The 307~K state is a sensitivity, resting on a
  correction used beyond the 295~K at which it was fitted."
- **Rule.** A qualification attaches once to the claim it bounds; Technical meaning (averaging years); Exact action
  ("resting on").
- **Why.** The vapour figures are means over years 15–19 of each run (claims S08), from a run still warming 0.08 K a
  year (G13); the sentence attaches them to "a balance". The fit temperature, which bounds the 307 K figure, arrives
  three sentences after it as the paragraph's last sentence, after the paragraph's consequence, so the paragraph lands
  on a qualification.
- **Rewrite.** "The longwave correction with the ice optics, the one change that moves the cooling by height, warms the
  design case by 11.5~K over years 10--19, toward a balance near 307~K, a sensitivity reached with a correction fitted
  at 295~K; the warmer run's water vapour over years 15--19 is twice the design case's, 348 against
  170~kg\,m$^{-2}$, and its cloud covers 38\% of the sky in place of 20\%, most of the gain in high cloud.\claim{G05}"
  The paragraph then lands on the sentence rewritten under finding 22, and lines 72–73 go.

### 24. MAJOR · results.tex:79–87 (taking the gap apart)

- **Text.** "PlaSim's longwave over-cooling of its own lowest layers is estimated at about 1.5~K of the rest, from a
  6~W\,m$^{-2}$ difference at the ring's 4~W\,m$^{-2}$ per kelvin, and the remainder, a degree or two, is attributed by
  elimination to the two models' upward transport of the ground's heat: …"
- **Rule.** A comparison states its terms; Write for the expert (a premise the reader lacks); Inheritance and order
  (premises before the inference drawn from them); No witticisms (personified "suspects … cleared").
- **Why.** The 6 W/m² is the excess of PlaSim's longwave cooling of its lowest layer over RRTMG's, each measured
  against the correlated-k model: 10.6 W/m² on 151 cloud-free three-day means at 47°N against 4.5 W/m² on the ring
  (Terluna `climate/crm/README.md`:1188–1191). The 4.5 appears at verification.tex:48–49 and the 10.6 nowhere in the
  paper, and "the ring's 4 W/m² per kelvin" names a rate the paper leaves undefined. The attribution "by elimination"
  comes before the eliminations (83–87), with the unquantified ice term between them, so the inference precedes its
  premises; the three "suspects" appear only through their test outcomes, and the reader must infer that Earth-speed
  rain tests the slow fall of lunar rain.
- **Rewrite** (79–87, with findings 26 and 27):

```latex
Two further terms are radiative. Against the correlated-$k$ model, PlaSim's longwave cools its lowest layer
10.6~W\,m$^{-2}$ too much on cloud-free columns at 47\textdegree\,N, and RRTMG cools CM1's lowest 1.8~km 4.5~W\,m$^{-2}$
too much on the ring, so the GCM sheds about 6~W\,m$^{-2}$ more than CM1, worth about 1.5~K of the remaining 3.7~K at
the ring's [named rate] of 4~W\,m$^{-2}$ per kelvin; the ring's starting-sounding ice above 107~km adds a term still
unquantified. Three other explanations were tested at the site where the rings cross the equator at
0\textdegree~E, in boxes forced from the Earth-orbit state, which brought 12\% too little sunlight there, and run on
several threads, so each pair compares two realisations: the ring's two dimensions, since a three-dimensional box ran
warmer still; the land surface, which moved the air by at most 0.3~\textdegree C; and the slow fall of lunar rain, since
rain falling at Earth's speeds warmed the air by a further 1.0~\textdegree C. At 45\textdegree\,N the dry-ground land
test has yet to run.\claim{G07} The remainder, a degree or two, is attributed by elimination to the two models' upward
transport of the ground's heat: CM1 mixes its lower air 14--19~km deep by day, where the GCM, with two layers in its
lowest 6.5~km, stays stable.
```

### 25. MAJOR · results.tex:87–89 (the landing on a range)

- **Text.** "The warmth and humidity of the air near the ground, where people and plants would live, are therefore best
  given as a range between the two models, 3.7~K wide in the lowest 1.8~km at 45\textdegree\,N with the transport
  imposed."
- **Rule.** Claims stay within their evidence; G5 (a range's evidence state and conditions).
- **Why.** The 3.7 K is the disagreement of two models under one forcing state, the design case with the longwave
  correction off, at one latitude over its second lunar day. The paragraph's own decomposition puts about 1.5 K of it in a
  known GCM error, and Terluna's record finds both schemes over-cooling the lower air against the reference, PlaSim by
  about 2.5 K's worth and RRTMG by about 1 K's (`climate/crm/README.md`:1190–1192), so a reference-consistent value
  would exceed the GCM's end. The previous paragraph puts the GCM's longwave-by-height sensitivity at 11.5 K, three
  times the spread. "best given as a range between the two models" offers the inter-model spread as the best statement
  of near-ground warmth, a claim larger than one forcing state measures; and the sentence names humidity and leaves
  its range unstated.
- **Rewrite.** "Under the design-case forcing, with the longwave correction off, the two models bracket the warmth of
  the air where people and plants would live, the lowest 1.8~km at 45\textdegree\,N, within 3.7~K once the transport is
  imposed; about 1.5~K of the bracket is the GCM's own over-cooling, so the bracket measures the models' disagreement in
  that one GCM state."

### 26. MAJOR · results.tex:84–85, 91, 110, and Table row 23 ("the pre-correction run")

- **Text.** "forced from the pre-correction run, which brought 12\% too little sunlight there" (84–85); "A small box
  forced from the pre-correction run" (91); "two lunar days of a box at 0\textdegree~E forced from the pre-correction
  run" (110).
- **Rule.** Names a reader outside the project can follow; Write for the expert; G5 (a condition attached at the
  results it bounds).
- **Why.** "Pre-correction" names the state by its place in the project's history; its content (PlaSim's Sun clock,
  Earth's orbit, 28% seas with lakes, 5% dimming, the split before its recalibration) is in the table and in
  assumptions.tex:134. Its consequence at the box site, 12% too little sunlight at 0°E (defect log C2: 328 of the
  373 W/m² due), appears once, attached to the explanation tests. The rain comparison at 91 and the storm and
  lightning results at 108–117 come from boxes at the same site forced from the same state and share the
  shortfall, unstated.
- **Rewrite.** Rename the state for what it holds, "the Earth-orbit state" (row label "Earth orbit"), beside "the
  Sun-and-tilt state", and state the shortfall where the box results begin: at 91, "A small box forced from the
  Earth-orbit state, which brought 12\% too little sunlight to 0\textdegree~E, …"; at 110, "…two lunar days of a box at
  0\textdegree~E forced from the same Earth-orbit state, …".

### 27. MAJOR · results.tex:85–87, 123–125 (paired box runs are realisations)

- **Text.** "a three-dimensional box ran warmer still, the land surface moved the air by at most 0.3~\textdegree C, and
  rain falling at Earth's speeds warmed the air by a further 1.0~\textdegree C" and "with the NSSL microphysics in place
  of Morrison's the same box runs 1.0~\textdegree C warmer at 2~m and its night fog at the ground covers 29\% of the box
  in place of 56\%".
- **Rule.** G5 (the evidence state of a paired difference); Technical meaning (which runs, which day).
- **Why.** The boxes ran on several threads (Terluna `climate/crm/README.md`:2064, 2174, `--threads 4`), where CM1
  parts from itself, and the record's own rule is that "Paired runs that differ in one setting compare as realizations"
  (defect log A6; verification.tex:100; Table `tab:verification`, "The lunar boxes' race"). The spread was measured for
  the electrification windows, with several Saunders and Peck runs of the same days (README:2079–2091), and stays
  unmeasured for the other pairs. The results report each difference as an effect. "the same box" joins two different
  runs: the main electrified run under NSSL and Morrison's `box_0e`, compared over the second lunar day
  (README:2409–2414).
- **Rewrite.** At 84–87, the rewrite under finding 24. At 123–125: "and with the NSSL microphysics in place of
  Morrison's, the main electrified run over its second lunar day is 1.0~\textdegree C warmer at 2~m than Morrison's box
  at the same site and forcing, one realisation against another, and its night fog at the ground covers 29\% of the box
  in place of 56\%, so the lunar night fog depends on the microphysics by about a factor of two.\claim{G11}"

### 28. MINOR · results.tex:91–97 (rain)

- **Text.** "Rain shows a larger disagreement." and "The rain of each model rests on Earth fits of its own, a convection
  scheme in the GCM and Earth's drop limits in CM1, and rain at a place in the rings changes by a factor of several with
  the slice's direction, while temperature, humidity and wind agree within about a degree and 0.3~m\,s$^{-1}$ between
  crossing rings."
- **Rule.** Exact action; Sentences carry their dependencies (coordination joins only equal propositions); Technical
  meaning.
- **Why.** In "Rain shows" and "rests on" abstractions perform acts, and "larger" compares a factor of four with a
  temperature offset. The last sentence joins two independent propositions with "and", the models' Earth fits and the
  rings' geometry. "humidity" shares two numbers that belong to temperature and wind, and "Earth's drop limits"
  leaves the scheme and the limit unnamed (finding 35).
- **Rewrite.**

```latex
On rain the models differ by a factor of about four. A small box forced from the Earth-orbit state brought 34~mm to the
ground per lunar day, where the GCM that forced it rained 129~mm and the Sun-and-tilt run 180~mm; at lunar gravity 85\%
of the water falling from the box's clouds evaporated on the way down, against 64\% when the same drops fell at Earth's
speeds.\claim{G08} Each model computes its rain from Earth fits of its own, a convection scheme in the GCM and
Morrison's Earth-fitted limits on raindrop size and breakup in CM1. In the rings the direction of the slice alone
changes the rain at a place by a factor of several, while temperature and wind at that place agree between crossing
rings within about a degree and 0.3~m\,s$^{-1}$.\claim{G15}
```

### 29. MINOR · results.tex:102–104 (caption of Figure `fig:gap`)

- **Text.** "CM1 alone, CM1 with the GCM's transport across the circle imposed, and the design case on the same row,
  years 10--19."
- **Rule.** Captions receive the same review as body prose; names say what they name.
- **Why.** The plot's legend reads "CM1 ring" and "GCM". "CM1 alone" suggests an unforced run, while this ring is
  nudged above 8–16 km and forced from the design case; "the design case on the same row" names the GCM run and its
  latitude row and leaves out the word GCM.
- **Rewrite.** "Layer-mean air temperature over the second lunar day on the 45\textdegree\,N ring: the CM1 ring forced
  from the design case, the same ring with the GCM's transport across the circle imposed, and the GCM's design case on
  the same latitude row, years 10--19. The imposed transport removes 2.2 of the 5.9~K warm offset in the lowest 1.8~km,
  37\%."

### 30. MAJOR · results.tex:108–109 (freezing levels and their runs)

- **Text.** "At lunar gravity the 0\,\textdegree C and $-40$\,\textdegree C levels stand five to six times higher than in
  Earth's tropics, near 25 and 60~km, and cloud tops reach 55--80~km."
- **Rule.** G5 (each lunar climate result tied to the runs and GCM state behind it).
- **Why.** Terluna's record states these heights "in every run" of six Morrison runs over their second lunar day, the two
  equatorial boxes, a twin with Earth's fall speeds and the three flat rings (`climate/crm/README.md`:1436–1456). By
  their set-up dates these were forced from the Earth-orbit state (defect log A1–A2, C7); the author should confirm
  this for the three flat rings. The sentence leaves the runs and the forcing unnamed and assigns the heights to
  lunar gravity alone, while they also follow from the surface temperature of the forcing state.
- **Rewrite.** "Over the second lunar day of six Morrison runs forced from the Earth-orbit state, the two equatorial
  boxes, a twin with Earth's fall speeds and the three flat rings, the 0\,\textdegree C and $-40$\,\textdegree C levels
  stand near 25 and 60~km, five to six times their heights in Earth's tropics, and cloud tops reach
  55--80~km.\claim{G09}"

### 31. MAJOR · results.tex:110–117 (storms and lightning)

- **Text.** "The main electrified run, two lunar days of a box at 0\textdegree~E forced from the pre-correction run, made
  530 flashes, a density over the box of 0.022 per square kilometre per year, about a hundredth of Earth's average. Up
  to a fifth were negative ground strikes, counted under WRF-ELEC's rule with the leader's crossing as an upper bound,
  and none was positive. Each ground strike lowered a median 149~C, where Earth's lower 5--30~C, while in-cloud flashes
  neutralised a median 108~C. The charge takes Earth's arrangement at five to six times its height: …"
- **Rule.** Sentences carry their dependencies (results that list number after number; swap test); Claims stay within
  their evidence (uncited Earth baselines; "Each … a median"); G5 (a condition on the comparison with Earth); Say what
  is ("none was positive").
- **Why.** Six declaratives follow one another, freezing levels, flash count, ground strikes, charge per strike, charge
  arrangement and hail's share, and the third, fourth and sixth trade places freely. The paragraph's governing relation
  appears in its fifth sentence (Earth's arrangement at five to six times the height) and the comparisons with Earth come
  before it. Both comparisons with Earth, "about a hundredth of Earth's average" and "Earth's lower 5–30 C", are
  unsourced; `references.bib` lacks a lightning climatology and `claims.json` (G10) cites Terluna records alone. On the
  Earth benchmark a coarser grid gave fewer, larger flashes (`notes/electrification.md`:97–99), and the box's 6 km
  columns correspond to about 1 km at Earth's scale (worlds.tex:90), so part of both differences from Earth may come
  from the grid, a condition the paper leaves out. "Each ground strike lowered a median" sets a
  universal over a distribution. The leader's crossing appears here as an upper bound and at repairs.tex:143–145 as a
  count between two of WRF-ELEC's bounds; the reader meets two descriptions of one count.
- **Rewrite.**

```latex
In the main electrified run, two lunar days of a box at 0\textdegree~E forced from the same Earth-orbit state, the
charge takes Earth's arrangement at five to six times its height: flashes start a median 35.8~km up, and the main
negative charge lies at 40--42~km, at $-13$ to $-14$\,\textdegree C, just above the $-7$\,\textdegree C level, as on
Earth, while hail, which rimes faster than the lunar graupel, does 87\% of the non-inductive charging. Its 530 flashes
come to 0.022 per square kilometre per year over the box, about a hundredth of Earth's average [source], and the
flashes move large charges: in-cloud flashes neutralised a median 108~C, and the ground strikes, all negative and at
most a fifth of the flashes under the leader's crossing, lowered a median 149~C, where Earth's lower 5--30~C [source].
Part of both differences from Earth may come from the grid, since the box's 6~km columns correspond to about 1~km at
Earth's scale and on the Earth benchmark a coarser grid gave fewer, larger flashes.\claim{G10}
```

  The upper-bound wording at repairs.tex:143–145 and here should name one relation: the 1 kV/m crossing places the
  count between WRF-ELEC's two rules, and the processes it leaves out make it an upper bound.

### 32. MAJOR · results.tex:119–123 (the Takahashi comparison)

- **Text.** "Under Takahashi's charging law \autocite{takahashi1978riming} in place of Saunders and Peck's
  \autocite{saunders1998laboratory} the storms separate as much charge with their polarity inverted, so the sign of the
  lightning depends on laboratory laws that disagree on the sign rimed ice takes in the little cloud water of the lunar
  storms;"
- **Rule.** G5 (each result tied to its runs and conditions).
- **Why.** "the storms" follows the main electrified run, which ran after the ventilation repair and with leakage. The
  comparison ran in two windows of an earlier electrified run, days 10.5–12 and 40.5–42, on 2026-10-05, before the
  ventilation repair of 2026-10-06 and with leakage off, each beside Saunders and Peck runs of the same days and judged
  within the spread of those realisations (Terluna `climate/crm/README.md`:2072–2080, 2097–2099, 2242; defect log
  C12).
- **Rewrite.** "In two windows of an earlier electrified run, days 10.5--12 and 40.5--42, made before the ventilation
  repair and with leakage off, the storms under Takahashi's charging law \autocite{takahashi1978riming} separate as much
  charge as under Saunders and Peck's \autocite{saunders1998laboratory}, within the spread of the Saunders and Peck runs
  of the same days, with their polarity inverted; the sign of the lightning therefore depends on laboratory laws that
  disagree on the sign rimed ice takes in the little cloud water of the lunar storms."

### 33. MAJOR · results.tex:127–129 (the wave-height ratio and its drag law)

- **Text.** "the same wind, fetch and duration build waves 4--5 times as high as on Earth, with periods five times as
  long."
- **Rule.** G5 (a condition that moves the number); Technical meaning ("the same wind").
- **Why.** The ratio uses Wu's drag law at both gravities. With Charnock's law at each gravity, lunar drag exceeds
  Earth's by 1.23–1.51 times at the three winds, which raises the height ratio by about 11–23% for fetch-limited seas
  and 23–51% for developed seas, if Charnock's constant is independent of gravity (`notes/waves.md`:191–196). The
  sentence states the ratio as a property of lunar gravity alone. "the same wind" means the same 10 m wind speed.
- **Rewrite.** "With Wu's drag law at both gravities, the same 10~m wind, fetch and duration build waves 4--5 times as
  high as on Earth, with periods five times as long; with Charnock's roughness at each gravity the lunar drag would be
  larger and the ratio higher, by about a tenth to a half." (in the paragraph rewrite under finding 34)

### 34. MINOR · results.tex:127–134 (Seas, and the section's last sentence)

- **Text.** "SWAN raises big, slow waves under the light lunar winds:" … "Lunar waves keep Earth's steepness and travel
  at 0.41 of the speed of an Earth wave of the same length," … "These wave results come with Earth's laws for wind
  input, whitecapping and breaking scaled to lunar gravity by similarity."
- **Rule.** Exact action ("SWAN raises", "come with"); Write for the expert (a ratio this reader derives from deep-water
  dispersion); a qualification attaches once; Inheritance and order (the landing).
- **Why.** The model raises waves in the prose, and the paper leaves the speed of "the light lunar winds" unstated;
  Terluna's record states 2.6 m/s at 10 m at the median over the equatorial seas (`climate/waves/README.md`:14–16).
  The 0.41 is $1/\sqrt{6}$, a consequence of the dispersion relation that the reader supplies. The statistics come
  from one measured lunar cycle after one cycle of spin-up (`notes/waves.md`:240–242), a condition left out. The last
  sentence
  repeats verification.tex:36–38 and closes the section on a qualification, while reach.tex opens on the
  sensitivities of the first two paragraphs.
- **Rewrite** (with finding 33):

```latex
\textbf{Seas.} The GCM's surface stress over the seas corresponds to light winds, 2.6~m\,s$^{-1}$ at 10~m at the
median over the equatorial seas. Under Earth's laws for wind input, whitecapping and breaking, scaled to lunar gravity
by similarity, and with Wu's drag law at both gravities, the same wind, fetch and duration build waves 4--5 times as
high as on Earth, with periods five times as long. Forced by sixty days of the Sun-and-tilt run's surface stress, the
first lunar cycle a spin-up and the second measured, SWAN computes a mean significant wave height of 1.39~m over the
nearside sea, 5.29 million~km$^2$, with 68\% of its area and time at or above 1~m, and its largest sea reaches 4.9~m
with a 19.3~s mean period. The waves keep Earth's steepness, and, computed by SWASH from SWAN's spectra, they run up
today's steep slopes to a 98th-percentile run-up of 2.1~m on the exposed western face of the eastern Smythii
headland.\claim{G12}
```

### 35. MINOR · names across both files

- **Text and rewrite, item by item.**
  - verification.tex:90, 108, "the twilight pair": a project nickname for the 45°N rings with and without the curved-air
    terms, whose result the results section omits. → "the 45\textdegree\,N rings with and without the curved-air terms"
    at first use, "the curved-air pair" after.
  - verification.tex:32, "its Earth twin". → "the Earth run it scales".
  - results.tex:25, 27, 46; verification.tex:84, "the ledger's first channels" and "the ledger's corrected terms": the
    versions are introduced only in the verification's defect list. → at first use in the results, "the ledger's first
    channels, later found to put near-infrared sunlight too high".
  - results.tex:95, "Earth's drop limits in CM1". → "Morrison's Earth-fitted limits on raindrop size and breakup in
    CM1".
  - Figure `fig:repairs`, bar label "cone". → "shell widening" (finding 21).
- **Rule.** Coined terms say what they name; Write for the expert.
- **Why.** A reader outside the project meets each of these undefined at the point of use.

## Parts found sound

Every paragraph in the scope drew at least one finding. These parts held under the passes named:

- verification.tex:30–36, the SWAN and SWASH similarity results: the numbers agree with claims V04 and V05 and with the
  verification record, and the order from evidence to inference holds under the swap test.
- verification.tex:57–60, the supercell benchmark against CM1's NSSL scheme: the numbers agree with V09 and the record,
  and the participial clause on hail names its cause.
- results.tex:75–79, the gap paragraph's first two sentences: the offsets agree with `gap45n.json` (5.87 K, cut to
  3.70 K; 2.17 K removed, 37%), and the imposed transport governs the decomposition that follows.
- results.tex:119, the storm-choices paragraph's topic sentence, which names what would settle each dependence, and
  121–122 and 124–125, which land each half of the paragraph on its consequence.
- results.tex:108–117, the human and physical presence: the storms, hail, graupel and flashes act in their own verbs,
  and results.tex:88 places people and plants in the air the models compute.
- Table `tab:states`, columns "Seas; sunlight" and "Years; surface": every window and temperature agrees with
  `repairs.json` and the claims (295.511, 297.812, 299.576, 294.311, 294.897, 294.243, 292.015, 295.023 and
  306.524 K).
- Figure `fig:gap`'s caption: its numbers agree with `gap45n.json`.
- Both files are free of "not" and "rather than"; the negations present state required propositions, apart from
  finding 31's "none was positive".

## Gates G1–G5 for this scope

**G1, argument and reorderability.** Findings 4, 8, 11, 12 (BLOCKING: disconnected evaluation items), 13 and 31 locate
paragraphs whose sentences trade places without loss. From its identity paragraph to its open checks, the verification
section renders Table `tab:verification` and the defect log in prose. Finding 24 locates an inference stated ahead of
its premises. The results' repair sequence (33–47) holds a cumulative order of runs.

**G2, audience and economy.** Findings 6 (an evaluative opener), 10 (a cosmic-ray term entering unexplained), 24 (an
undefined rate), 34 (a ratio the reader derives from dispersion) and 14 (an opening that misdescribes the section).

**G3, inheritance, syntax and cadence.** Findings 4 (a gap stated four sentences from the claim it bounds), 7 (an
interrupting sentence), 28 (unequal propositions joined by "and") and 34 (the section's last sentence a qualification,
with reach.tex opening on the first two paragraphs). The cadence reading was silent throughout, and the read-aloud
review of these sections stays pending.

**G4, affirmative stance and exact action.** Both files are free of "not" and "rather than". Findings 3 and 17 list
empty actions and generic verbs; finding 13 locates qualifications stated two or three times across the section, a
caveat wall built from repetition; finding 24 records the personified "suspects … cleared"; finding 31's "none was
positive" has an affirmative form.

**G5, technical meaning and evidence states.** The BLOCKING findings 4, 16, 19 and 21 misstate an evidence state, a GCM
state's conditions, a defect's reach into reported results and a figure's baseline. The MAJOR findings 1, 7, 9, 10, 20,
22, 25, 26, 27, 30, 31, 32 and 33 locate results whose conditions are missing, stated once far away, or carried past
their evidence. The prose's numbers agree with `claims.json` and the data extracts, apart from finding 21.

## Numbers the rewrites add, for the claims register

- 10.6 W/m², PlaSim's lowest-layer excess over correlated-k on 151 cloud-free three-day means at 47°N
  (`notes/verification_record.md`:158; Terluna `climate/crm/README.md`:1188–1190), and a definition of the ring's
  4 W/m² per kelvin (finding 24).
- Convective cover per 2,400 s; the lowest layer's threshold from 0.983 to 0.6 (Terluna `climate/gcm/README.md`:
  1209–1210; finding 22).
- 36% of land dry within two years of the Sun and tilt; Earth's 23.7° tilt; summer rain to 60° (defect log A2;
  finding 18).
- The uncalibrated and first calibrated states unhashed; the convective-cover run on a draft of patch 03; the water
  scaling's identity by arithmetic (`models/exoplasim/README.md`:84–90, `runs.json`, `notes/verification_record.md`:
  48–50; finding 4).
- Every CM1 case set up before 2026-10-17 on the constant-vapour sounding (defect log C4); the Takahashi windows'
  days, date and settings, and the ventilation repair's date (Terluna `climate/crm/README.md`:2072–2080, 2242; defect
  log C12; findings 11, 32).
- Fewer, larger flashes on a coarser grid in the Earth benchmark (`notes/electrification.md`:97–99; finding 31).
- Wu's drag at both gravities, and the Charnock comparison, 1.23–1.51 times the drag and 11–51% on the height ratio
  (`notes/waves.md`:191–196; finding 33).
- The 2.6 m/s median 10 m wind over the equatorial seas (Terluna `climate/waves/README.md`:14–16; finding 34).
- Sources to admit and cite: the published electrification runs (finding 9), Earth's average flash density and charge
  per ground strike (finding 31), the Monte Carlo Rayleigh reference (findings 5, 7).
