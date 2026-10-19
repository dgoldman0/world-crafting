# Editorial round 21, closing review: the front half, for its verbs

- **Snapshot.** Commit `a50e0b1` (`a50e0b177d089b6ccb232eafbf94cd157ae4a4af`), branch `paper/conclusion-development`;
  before I began, `git rev-parse HEAD` gave that commit and `git status --short` printed nothing. The PDF built from
  it, `paper/build/main.pdf`, has sha256 `f6ff147f7fb291d4acf5e80c24185bf8a006a7be3d64bc17c179b7507888623f`, which I
  checked with `sha256sum`; I built nothing and ran no LaTeX. Line numbers below are the snapshot's.
- **Reviewer.** A fresh Claude Opus 5.5 subagent, reading the front half for its verbs, at the close of round 21. A
  second fresh reviewer read the back half at the same time. This record is the only file I wrote; the paper's files
  stand as committed.
- **Date.** 19 October 2026.
- **The author's direction.** Having read the paper on 19 October 2026 and judged it good overall, the author named one
  remaining criticism, the repeated use of "verbs that don't really work well", with two examples in Assumptions,
  "Earth's day enters..." and "Earth's day in its Sun and its soil", and left this closing review to check the paper
  for them. This record covers the front half; the approved wording of the abstract and the note on terms goes to the
  author.
- **What I read.** `AGENTS.md` in full; the four Terluna sources behind its writing rules (`STYLE_NOTES.md`,
  `Jewish_Papers_Updated_Style_Notes.md`, `Agent_Working_State_Editorial_Gates.md`,
  `Open_Moon_Editorial_Charter_control-01.md`); the drafting assistant's notes of the author's directions
  (`writing-style-rules.md`, `author-direction-overrides-rules.md`, `paper-standalone-field-framing.md`,
  `abstract-attracts-reader.md`, `conclusion-as-discussion.md`, `credit-prior-work.md`,
  `standalone-paper-no-process-logs.md`); `editorial_round18_closing_prose.md`, `editorial_round19.md` and
  `editorial_round20.md`; then the whole paper in the order `main.tex` inputs it, the back half included, and the
  front half's changes since round 18 as a word diff (`git diff ffdedfe a50e0b1`). For the operations behind the
  fixes I read `paper/claims.json` and `notes/defect_log.md` whole, `notes/cm1.md`, `models/cm1/README.md`, the
  electrified graft's Fortran (`models/cm1/fortran/terluna_lightning.F`, `terluna_branched.F`, `terluna_elec.F`),
  CM1 r22.0's solar routines on the research drive (`cm1r22.0/src/radiation_driver.F` 530–559 and 832–913), and the
  source manifest's records and archived text of Way et al. (2017) and Tsigaridis et al. (2025).
- **Files the verb pass covered.** `main.tex` (title and front matter), `abstract.tex`, `terms.tex`,
  `introduction.tex`, `worlds.tex`, `assumptions.tex` and `repairs.tex`: every sentence, with the captions of
  Figures 1–4 and Tables 1–2, every cell of Tables 1 and 2, and Table 2's legend. These files have no footnotes;
  LaTeX comments, which print nothing, were left out.
- **Cadence.** Read silently, with no read-aloud review.

## Judgment

The author's two examples share one fault: each gives its subject an act the subject cannot perform and names none of
the operation behind the sentence. A day enters nothing, since ExoPlaSim and CM1 count their calendars in Earth days, and
CM1 keeps no day in a Sun, since its solar routine computes the Sun's position from Earth's 24-hour day, a 365-day
calendar and a 23.5° obliquity. Read verb by verb, the front half has 71 places of this kind. In most of them a
quantity, a law, a fit or a table is said to enter, take, keep, lie, meet, come from or need; four more sentences use
"enters" as the first example does (V28, V53, V56, V70), and CM1's patched Sun "follows" its namelist day as its
released Sun "follows" Earth's (V33, V60). In the rest, a code, a run or a configuration is given an act other than
the operation its source code specifies, as when RRTMG "meets" the lunar columns whose radiation it computes at the edges of its
tables (V38). The repository's records name every one of these operations, since the defect log, the CM1 notes, the
claims register and the source code state what each code computes, reads, scales, caps or writes, and so most fixes
change one verb, a subject or a voice. Two findings fall in the abstract's approved wording and go to the author (V1,
V2); V2 and its twin in the Introduction (V13) state the paper's main result through fits that "moved" the climate.
The fixes keep each claim's numbers, conditions, scope and evidence state and the sentences' transitions, and they
add no "not" and no "rather than"; the fix in V33 also mends a relative clause that gave Earth's diurnal wave the
0.6 m depth of the month-long day's wave. Beyond the verbs I found nothing BLOCKING or MAJOR in the front half, and the
text that rounds 19 and 20 changed is sound apart from its "lies in" (V45).

**Counts:** 71 verb findings, 2 of them for the author (V1, V2); other findings: 0 BLOCKING, 0 MAJOR, 0 MINOR.

## Verb findings

Each finding gives the clause with the verb in bold, what actually happens with its evidence, and the replacement as
it would stand in the file.

### `abstract.tex` (approved wording, for the author)

**V1** · `abstract.tex`:18–19 · for the author
- *As it stands.* "the constants, units of time and geometry that the codes set for Earth mostly **took** repairs that
  hold on other worlds within the limits of their laws, or tables recomputed from each world's own column"
- *What happens.* These values were repaired: general repairs replaced the constants and units, and the patched codes
  apply a table computed from the world's column for the geometry (W01; R05, R06).
- *Fix.*
  > Beyond the defects, the constants, units of time and geometry that the codes set for Earth were mostly given
  > repairs that hold on other worlds within the limits of their laws, or tables recomputed from each world's own
  > column.

**V2** · `abstract.tex`:20–21 · for the author
- *As it stands.* "and in the lunar runs they **moved** the climate furthest, by amounts of the order of the spreads
  measured among exoplanet GCMs"
- *What happens.* The fits compute absorption and cloud; the simulated global mean changed most when the radiation's
  fits were calibrated (at least 20 K, G14) and the cloud's settings varied (up to about 6 K, G05), the two operations
  the abstract's next sentence names.
- *Fix.*
  > The codes' empirical fits, by contrast, hold near the columns they were fitted on, and in the lunar runs their
  > effects on the climate were the largest, of the order of the spreads measured among exoplanet GCMs.

### `introduction.tex`

**V3** · `introduction.tex`:9–10
- *As it stands.* "ROCKE-3D **descends** from the GISS ModelE2, ExoCAM from NCAR's Community Atmosphere Model, and
  ExoPlaSim from the Planet Simulator, PlaSim"
- *What happens.* Each team developed its code from an Earth model (way2017resolving, wolf2022exocam,
  paradise2022exoplasim); descent is a figure of lineage for that work. The abstract's approved noun "descendants"
  can stay beside the plain verb.
- *Fix.*
  > ROCKE-3D was developed from the GISS ModelE2, ExoCAM from NCAR's Community Atmosphere Model, and ExoPlaSim from
  > the Planet Simulator, PlaSim

**V4** · `introduction.tex`:38–39
- *As it stands.* "ROCKE-3D's developers found constants **tied** to the lengths of Earth's day and year in its first
  release"
- *What happens.* Way et al. (2017, archived v2, p. 10) describe "implicit (hardwired) constants appropriate to the
  lengths of modern Earth day and year": the code's writers set the constants for those lengths.
- *Fix.*
  > ROCKE-3D's developers found constants set for the lengths of Earth's day and year in its first release

**V5** · `introduction.tex`:44–45
- *As it stands.* "ROCKE-3D's developers report that the changes their first release **made** from the Earth
  configuration went without systematic study"
- *What happens.* The developers made the changes, in the first release. Tsigaridis et al. (2025, p. 5834) write that
  in ROCKE-3D 1.0 "the changes from the tight Earth configuration to the more general one were not studied
  systematically".
- *Fix.*
  > ROCKE-3D's developers report that the changes from the Earth configuration in their first release went without
  > systematic study \autocite{tsigaridis2025rocke3d},

**V6** · `introduction.tex`:47–50
- *As it stands.* "a run can compute the familiar phases of water in nitrogen--oxygen air while **retaining** a
  constant set for Earth's gravity, or a formula that counts rain per Earth day"
- *What happens.* A run executes the code, and the code retains the Earth value in its source, whatever the run
  computes.
- *Fix.*
  > On a Gaean world, then, a run can compute the familiar phases of water in nitrogen--oxygen air while its code
  > retains a constant set for Earth's gravity, or a formula that counts rain per Earth day, and because its output is
  > plausible, the retained value can be hard to detect.

**V7** · `introduction.tex`:55–57
- *As it stands.* "requires identifying which changes follow from general laws and which **need** calculations or
  calibrations for each world"
- *What happens.* The modeller calculates or calibrates such a change for each world: a general method's table is
  recomputed and a calibration refitted (Repairs; W01).
- *Fix.*
  > Developing such an ensemble for Gaean exoplanets and constructed worlds therefore requires identifying which
  > changes follow from general laws and which must be calculated or calibrated for each world.

**V8** · `introduction.tex`:60–63
- *As it stands.* "four ratios on which the models' Earth values depend **lie** far from Earth's at once: each square
  metre **holds** 7.25 times Earth's air"
- *What happens.* The ratios are values far from Earth's. A square metre is an area, and the column over it holds the
  air (S02: 74,861 against 10,332 kg m⁻²).
- *Fix.*
  > Its air is close to Earth's in composition and surface pressure, while four ratios on which the models' Earth
  > values depend are far from Earth's at once: the column over each square metre holds 7.25 times Earth's
  > air,\claim{S02} the scale height of about 52~km is 23 times Earth's in proportion to the radius,\claim{S03}
  > gravity is a sixth of Earth's, and the solar day lasts 29.53 Earth days.

**V9** · `introduction.tex`:63–65
- *As it stands.* "A run of a natural planet that departs from Earth along one of these ratios, a slow rotator or a
  smaller world, **meets** the Earth values that depend on that ratio alone, whereas on the test world the values of
  all four err together"
- *What happens.* A run executes every Earth value in its code; on a planet that departs along one ratio, only the
  values that depend on that ratio err, which is the contrast the sentence draws with the test world.
- *Fix.*
  > In a run of a natural planet that departs from Earth along one of these ratios, a slow rotator or a smaller world,
  > only the Earth values that depend on that ratio err, whereas on the test world the values of all four err
  > together, by amounts large enough to measure.

**V10** · `introduction.tex`:68
- *As it stands.* "The global climate **comes** from ExoPlaSim~3.4.2"
- *What happens.* ExoPlaSim computes the global climate. The passive keeps ExoPlaSim at the end of the main clause,
  where the appositive and the relative clause that follow attach to it.
- *Fix.*
  > The global climate is computed by ExoPlaSim~3.4.2 \autocite{paradise2022exoplasim,paradise2025exoplasim}, PlaSim
  > \autocite{fraedrich2005planet} extended for other worlds (the appendix gives each code's configuration), which
  > runs ...

**V11** · `introduction.tex`:87
- *As it stands.* "In the four codes the Earth values **take** four forms"
- *What happens.* The values have these forms; with "take", the sentence attributes to them an act of assuming a
  shape.
- *Fix.*
  > In the four codes the Earth values have four forms:

**V12** · `introduction.tex`:91–92
- *As it stands.* "Of the repairs made to these values and defects, most **fall** into three classes"
- *What happens.* The repairs were sorted into classes, and each belongs to one. V52 applies the same fix in
  Repairs.
- *Fix.*
  > Of the repairs made to these values and defects, most belong to three classes, which differ in the worlds they
  > hold for.

**V13** · `introduction.tex`:99–101
- *As it stands.* "Of the four forms, moreover, the fits **moved** the test world's climate furthest, by amounts of
  the order of the spreads measured among exoplanet GCMs"
- *What happens.* As in V2: calibrating the radiation's fits changed the global mean by at least 20 K, and varying the
  cloud's settings by up to about 6 K (G14, G05; Results, "Ranked by form").
- *Fix.*
  > Of the four forms, moreover, the fits had the largest effects on the test world's climate, of the order of the
  > spreads measured among exoplanet GCMs, and every lunar climate number is therefore a conditional model result,
  > holding given the scenario and the Earth values that remain.

### `worlds.tex`

**V14** · `worlds.tex`:4–6
- *As it stands.* "the mass of air over each square metre fixes the absorber paths, which PlaSim's broadband fits
  **took** from Earth's column, and the pressures, which RRTMG's tables cover to 1,053.63~hPa"
- *What happens.* The broadband absorptivities were fitted over the absorber paths of Earth's column (Lacis and
  Hansen's to 10 cm of water, H14); Figure 1's caption and Reach say the fits "were made near" Earth's column. With
  "cover", the two relative clauses are parallel.
- *Fix.*
  > Two govern the radiation's paths: the mass of air over each square metre fixes the absorber paths, which PlaSim's
  > broadband fits cover near Earth's column, and the pressures, which RRTMG's tables cover to 1,053.63~hPa;

**V15** · `worlds.tex`:9–10
- *As it stands.* "Along these four ratios, natural and constructed worlds **lie** off Earth's values in different
  directions"
- *What happens.* The worlds' ratios differ from Earth's, and Figure 1 plots each world as a point; the next sentences
  give that difference the paper's term ("Titan departs along all four").
- *Fix.*
  > Along these four ratios, natural and constructed worlds depart from Earth's values in different directions
  > (Figure~\ref{fig:regimes}).

**V16** · `worlds.tex`:26–27, Figure 1 caption
- *As it stands.* "Scale heights **use** each world's surface temperature and mean molar mass."
- *What happens.* The scale heights are computed from these two quantities (S03, W02; `paper/data/worlds.json`).
- *Fix.*
  > Scale heights are computed from each world's surface temperature and mean molar mass.

**V17** · `worlds.tex`:31–35
- *As it stands.* "The TSIS-1 solar spectrum ..., passed through a titania shield in space, **brings**
  1,235~W\,m$^{-2}$ to the top of the air, ... the sensitivity runs reported below **hold** their sunlight fixed."
- *What happens.* Filtered by the shield, the spectrum sums to 1,235 W m⁻² at the top of the air (S07). The sunlight
  was held fixed when the sensitivity runs were configured, and a run uses the sunlight it is given.
- *Fix.*
  > The TSIS-1 solar spectrum \autocite{coddington2021tsis}, passed through a titania shield in space, totals
  > 1,235~W\,m$^{-2}$ at the top of the air, dimmed evenly at every wavelength to 1,198~W\,m$^{-2}$ in the design
  > case, a scale of 0.970 chosen so that the GCM's global-mean surface temperature settles at the design value of
  > 295~K, and since the scale was set once, for the design case, the sunlight is held fixed in the sensitivity runs
  > reported below.

**V18** · `worlds.tex`:36–40
- *As it stands.* "Beneath the shield the air **holds** 1,216~hPa at the water level, ... and across the GCM's cells
  the surface pressure **runs** from 1.02 to 1.22~atm."
- *What happens.* The scenario sets the air's pressure at the water level at 121,590 Pa, and the GCM's surface
  pressure ranges from 1.02 to 1.22 atm across its cells (S05). Air contains gases; a pressure is a property it has.
- *Fix.* At lines 36–37:
  > Beneath the shield the air has a pressure of 1,216~hPa at the water level, with oxygen at Earth's partial pressure
  > of 212~hPa (17.5\% of the air), ...

  and at lines 39–40:
  > and across the GCM's cells the surface pressure ranges from 1.02 to 1.22~atm.\claim{S05}

**V19** · `worlds.tex`:46–50, Table 1 caption
- *As it stands.* "The quantities that **separate** the Open Moon from Earth, ... scale heights **use** the surface
  temperature and the air's mean molar mass"
- *What happens.* The Moon differs from Earth in these quantities; as in V16, the scale heights are computed from the
  two quantities named.
- *Fix.*
  > \caption{The quantities in which the Open Moon differs from Earth, and the model parts that depend on each. Lunar
  > values are for the 1.2~atm design case and are scenario inputs or calculations from them; scale heights are
  > computed from the surface temperature and the air's mean molar mass; horizon air masses are ...}

**V20** · `worlds.tex`:78–80
- *As it stands.* "and straight rays through that column **give** horizon air masses of 7.1 for well-mixed air and
  13.5 for water vapour"
- *What happens.* The horizon air masses are the slant paths along straight rays through the column's shells over the
  vertical path, computed in `python/climate/results/gcm/twilight.json` (S09); the rays are the paths of the
  calculation.
- *Fix.*
  > and along straight rays through that column the horizon air masses are 7.1 for well-mixed air and 13.5 for water
  > vapour, against the 35 of PlaSim's formula, written for Earth.\claim{S09}\claim{W02}

**V21** · `worlds.tex`:83–84
- *As it stands.* "and spherical shells with that gravity **raise** the excess to 11.5\% per square metre of ground"
- *What happens.* Counted in spherical shells with gravity falling as GM/r², the air over each square metre of ground
  is 11.5 % more than p_s/g_s (S10: 84,876 against 76,096 kg m⁻²); the excess is the result of that count.
- *Fix.*
  > and in spherical shells with that gravity the excess is 11.5\% per square metre of ground:

**V22** · `worlds.tex`:94–96
- *As it stands.* "so a 6~km column of a cloud-resolving model **stands** for about 1~km at Earth's scale, while the
  microphysics and the radiation **keep** their own scales"
- *What happens.* By the dry similarity a 6 km column corresponds to about 1 km at Earth's scale, the relation Results
  states with "correspond"; the microphysics and radiation have scales set by particle sizes, fall laws and
  absorption, outside the dry similarity (S12).
- *Fix.*
  > so a 6~km column of a cloud-resolving model corresponds to about 1~km at Earth's scale, while the microphysics and
  > the radiation have scales of their own.

**V23** · `worlds.tex`:103–105
- *As it stands.* "at 1.54\textdegree\ it **keeps** the Sun grazing at the poles all year, where ExoPlaSim's default
  orbit **puts** Earth's tilt of 1~AD, 23.7\textdegree"
- *What happens.* At a tilt of 1.54° the Sun's elevation at the poles stays within about 1.5° of the horizon all
  year; the tilt is a geometric property. ExoPlaSim's default orbit has Earth's obliquity for 1 AD (H24; defect log
  A2). "Whereas" states the contrast, which "where" also allowed to be read as a place at the poles.
- *Fix.*
  > The tilt, by contrast, is small: at 1.54\textdegree\ the Sun stays near the horizon at the poles all year, whereas
  > ExoPlaSim's default orbit has Earth's tilt of 1~AD, 23.7\textdegree.\claim{H24}

### `assumptions.tex`

**V24** · `assumptions.tex`:3–4
- *As it stands.* "ExoPlaSim's default orbit is one of the Earth values and defects **met** on the paths the lunar
  runs take through the four codes"
- *What happens.* These values and defects were found by reading the codes' source and the runs' records (the defect
  log, its opening and its section (b)); "met" names neither the finding nor the finders.
- *Fix.*
  > ExoPlaSim's default orbit is one of the Earth values and defects found on the paths the lunar runs take through
  > the four codes (Table~\ref{tab:inventory}).

**V25** · `assumptions.tex`:5–6
- *As it stands.* "and the log **adds** the entries found off the lunar runs' paths and the adaptation's own defects"
- *What happens.* The log also lists these entries, in its section (c) and in items such as B26 off the lunar paths;
  a document lists what its writers added.
- *Fix.*
  > and the log also lists the entries found off the lunar runs' paths and the adaptation's own defects.

**V26** · `assumptions.tex`:7–8
- *As it stands.* "so the inventory **reads** as well as a list of what to check on another world"
- *What happens.* Readers read; the inventory is such a list. "Reads as well as" also admits a comparative reading,
  "reads as well as a list does".
- *Fix.*
  > so the inventory is also a list of what to check on another world.

**V27** · `assumptions.tex`:8–11
- *As it stands.* "What a repair of an Earth value **needs**, however, follows from its form: a dimensional constant
  **needs** the world's own value or a law that gives it, ..."
- *What happens.* The modeller repairs each form by its own means, which Repairs names: general repairs, the
  curved-air table, calibrations.
- *Fix.*
  > How an Earth value is repaired, however, follows from its form: a dimensional constant is repaired with the
  > world's own value or a law that gives it, a unit of time with the world's own unit, a geometry with a method
  > computed for the world's own air, and a fit or simplification with a refit or a scheme that holds over the
  > world's range.

**V28** · `assumptions.tex`:13
- *As it stands.* "Gravity, the commonest constant, **enters** the codes as a number, a length and a frequency."
- *What happens.* The figure of the author's first example. The codes' writers wrote Earth's gravity into them as
  9.81 or 9.8 (H01, H02), as CCM3's height scale in metres (H18) and as SWAN's 1 Hz knee (H04); the paragraph's fourth
  sentence already says "it is written into SWAN".
- *Fix.*
  > Gravity, the commonest constant, is written into the codes as a number, a length and a frequency.

**V29** · `assumptions.tex`:13–17
- *As it stands.* "as well as in schemes those paths **leave** unselected, and 9.8, set twice, in WRF-ELEC's NSSL
  scheme, which also **ties** the ventilation of evaporating rain and depositing ice to Earth's fall speeds"
- *What happens.* The lunar cases' namelists leave these schemes unselected (H01: "schemes the lunar cases leave
  unselected"). The NSSL scheme computes rain's ventilation from the fixed fall-speed coefficients `ar` and `ax(lr)`
  and cloud ice's from a Reynolds number fitted on Earth (defect log B3; H02).
- *Fix.*
  > As a number it is 9.81~m\,s$^{-2}$ in four places on the lunar paths of CM1 release 22, its dynamics, the
  > conversion of pressure to layer mass in RRTMG \autocite{iacono2008radiative}, its CAPE diagnostic and the Morrison
  > microphysics, as well as in schemes the lunar cases leave unselected, and 9.8, set twice, in WRF-ELEC's NSSL
  > scheme, which also computes the ventilation of evaporating rain and depositing ice from Earth's fall
  > speeds.\claim{H01}\claim{H02}

**V30** · `assumptions.tex`:24–28
- *As it stands.* "wherever its frequency band **reaches** past the lower of two knees"
- *What happens.* A band is a set of frequencies, and the condition is that it includes frequencies above the knee
  (H04).
- *Fix.*
  > SWAN's sea at any gravity other than Earth's departs through that constant from the scaled image of an Earth sea
  > wherever its frequency band includes frequencies above the lower of two knees, the code's 1~Hz and the
  > $g/g_\mathrm{E}$~Hz that similarity would give, which is $g/g_\mathrm{E}$~Hz under weaker gravity and 1~Hz under
  > stronger.\claim{H04}

**V31** · `assumptions.tex`:37–38
- *As it stands.* "RRTMG **takes** carbon dioxide from the calendar year, with Earth's trace gases and ozone"
- *What happens.* RRTMG computes its carbon dioxide from the year by a formula, co2 = (280 + 90 exp(0.02 (yr − 2000)))
  × 10⁻⁶, and uses Earth's methane, nitrous oxide, halocarbons and ozone profile (defect log B8; H06); with "takes",
  the sentence omits the formula.
- *Fix.*
  > RRTMG computes carbon dioxide from the calendar year and uses Earth's trace gases and ozone, while CM1's beta plane
  > derives its gradient from Earth's rotation and radius.\claim{H06}

**V32** · `assumptions.tex`:40
- *As it stands.* "Earth's day **enters** as a unit of time in the calendars."
- *What happens.* The author's first example. ExoPlaSim counts its year as 360 Earth days of 48 half-hour steps,
  17,280 steps (H08), and CM1 counts its year in the days of a 365-day calendar and its day as 1,440 minutes
  (`radiation_driver.F` 539 and 895–898).
- *Fix.*
  > ExoPlaSim and CM1 count their calendars in Earth days.

**V33** · `assumptions.tex`:42–45
- *As it stands.* "CM1 **keeps** Earth's day in its Sun and its soil: its Sun **follows** Earth's 24-hour day, Earth's
  calendar and an obliquity of 23.5\textdegree, and its five soil layers, 1--16~cm thick, resolve Earth's diurnal
  thermal wave, which under the month-long day reaches about 0.6~m, below the deepest of them."
- *What happens.* The author's second example. In CM1 r22.0, `radconst` computes the Sun's declination from the day
  of a 365-day year with an obliquity of 23.5° (`radiation_driver.F` 832–874), and `calc_coszen` computes the hour
  angle from the time modulo 1,440 minutes, with Earth's equation of time (885–913); the five soil layers of 1–16 cm
  were sized for Earth's diurnal wave (defect log B10; H09). The relative clause also gives Earth's diurnal wave the
  0.6 m depth of the month-long day's wave (S13).
- *Fix.*
  > In CM1, the solar routine computes the Sun's position from Earth's 24-hour day, Earth's calendar and an obliquity
  > of 23.5\textdegree, and the five soil layers, 1--16~cm thick, are sized for Earth's diurnal thermal wave, whereas
  > under the month-long day the wave reaches about 0.6~m, below the deepest of them.\claim{H09}

**V34** · `assumptions.tex`:60–63
- *As it stands.* "and in the design case they **put** the top three layers above 107~km, at 81--107~km and at
  63--81~km, ..., and **leave** two layers for the lowest 6.5~km"
- *What happens.* The levels are fixed fractions of the surface pressure, and in the design case's tall air the
  layers between them are at these heights (H33).
- *Fix.*
  > PlaSim's vertical grid was laid out for Earth: its ten $\sigma$ levels are set at fractions of the surface
  > pressure chosen for Earth's air, and in the design case the top three layers are above 107~km, at 81--107~km and
  > at 63--81~km, each spanning about 25~K, with ice saturation changing 55-fold across the second, while the lowest
  > 6.5~km holds two layers, too few to resolve the boundary layer's day--night shape.\claim{H33}

**V35** · `assumptions.tex`:65–66
- *As it stands.* "and the test world's columns and filtered sunlight **lie** far from both"
- *What happens.* The lunar columns' absorber paths and the shield-filtered spectrum are far from those the schemes
  were fitted to (H14, H15).
- *Fix.*
  > The radiation schemes were fitted to Earth's columns and Earth's Sun, and the test world's columns and filtered
  > sunlight are far from both.

**V36** · `assumptions.tex`:66–67
- *As it stands.* "PlaSim's fits **erred** first in the column's totals, then in its split of sunlight, then in the
  heights at which it absorbs and cools."
- *What happens.* The three errors were present together; the order is that in which they were found and calibrated,
  the totals on 25 September, the split on 29 September and the heights from 14 October (defect log B16, B17, B15,
  B18; Repairs: "Each calibration was fitted to the residual of the one before"). As written, "erred first ..., then
  ..." says the fits erred in that sequence.
- *Fix.*
  > PlaSim's fits were found to err first in the column's totals, then in its split of sunlight, then in the heights
  > at which it absorbs and cools.

**V37** · `assumptions.tex`:76–79
- *As it stands.* "Sasamori's broadband absorptivities \autocite{sasamori1968radiative}, with a water continuum that
  the first calibration fitted to the outgoing flux, **cool** the lowest two layers 9.7--11.9~W\,m$^{-2}$ too much"
- *What happens.* The longwave scheme computes the cooling from these absorptivities and the continuum (H17:
  "PlaSim's longwave ... cools the lowest two layers"); an absorptivity is a fraction. The sentence's own subject,
  "PlaSim's longwave", is the agent of the cooling.
- *Fix.*
  > PlaSim's longwave errs by height as well: with Sasamori's broadband absorptivities
  > \autocite{sasamori1968radiative} and a water continuum that the first calibration fitted to the outgoing flux, it
  > cools the lowest two layers 9.7--11.9~W\,m$^{-2}$ too much against the reference model's correlated-$k$ emulation
  > and the air aloft up to 12~W\,m$^{-2}$ too little.\claim{H16}\claim{H17}

**V38** · `assumptions.tex`:85
- *As it stands.* "CM1's RRTMG **meets** the same columns at the edges of its tables"
- *What happens.* The example the charge for this review gives. RRTMG computes the radiation of the lunar columns,
  extrapolating its tables in ln p for layers at pressures above 1,053.63 hPa (defect log B22: index `jp` = 1 and a
  negative fraction `fp`) and reading ice sizes to its table's end at 140 µm (B23; H20).
- *Fix.*
  > In CM1, RRTMG computes the radiation of the same columns at the edges of its tables:

**V39** · `assumptions.tex`:91–93
- *As it stands.* "since gravity's part in each fall speed follows from the balance of weight and drag, a scaling law
  **extends** them to another gravity"
- *What happens.* The gravity patch multiplies each fitted coefficient and cap by (g/9.81)^((b+1)/3) (defect log B1,
  B2; R02).
- *Fix.*
  > since gravity's part in each fall speed follows from the balance of weight and drag, they can be extended to
  > another gravity by a scaling law.\claim{H01}

**V40** · `assumptions.tex`:96–97
- *As it stands.* "The wave and storm laws **come** from Earth's calibrations:"
- *What happens.* Their authors calibrated these laws on Earth's seas and storms and in laboratories (H22; defect log
  B7, B27).
- *Fix.*
  > The wave and storm laws were calibrated on Earth:

**V41** · `assumptions.tex`:102–104
- *As it stands.* "the charge that evaporating cloud **handed** to the small ions persisted for weeks"
- *What happens.* As cloud evaporated, the electrified scheme transferred its charge to the small ions (H10; defect
  log A7); "handed" personifies the cloud.
- *Fix.*
  > but in a month-long lunar run the charge that evaporating cloud transferred to the small ions persisted for weeks
  > and held the field at the ground near 20~kV\,m$^{-1}$ across the whole domain.\claim{H10}

**V42** · `assumptions.tex`:115
- *As it stands.* "The second **lies** in Slingo's convective cover"
- *What happens.* The defect is in the code that computes Slingo's cover, `zrfac = solar_day*1000` in `rainmod.f90`
  (defect log B11; H07); the charge for this review names "lies in" among the dead figures.
- *Fix.*
  > The second is in Slingo's convective cover,

**V43** · `assumptions.tex`:121–124
- *As it stands.* "ExoPlaSim's default orbit setting silently **replaces** the configured obliquity with that of
  Earth's orbit"
- *What happens.* Under the default setting (`fixedorbit` False), PlaSim replaces the namelist's orbit with Berger's
  orbit for 1 AD (defect log A2; H24). With PlaSim as the subject, the later "while on Earth it moves the tilt" names
  PlaSim too.
- *Fix.*
  > The third puts an Earth constant in place of a configured value: under ExoPlaSim's default orbit setting, PlaSim
  > silently replaces the configured obliquity with that of Earth's orbit for the model's starting year from Berger's
  > series \autocite{berger1978long}, 23.7\textdegree, which ...

**V44** · `assumptions.tex`:129–130
- *As it stands.* "although its usual configuration, with breaking on, **assigns** the parameter before the read"
- *What happens.* SWAN's `SINTGRL` assigns `KTETA`, through `BRKPAR`, when depth breaking is on (defect log A5); the
  configuration is the condition, and SWAN assigns.
- *Fix.*
  > so repeated Earth runs differed by about 2.5\% in wave height, although SWAN, in its usual configuration, with
  > breaking on, assigns the parameter before the read.\claim{H25}

**V45** · `assumptions.tex`:132–134 · text changed in round 20
- *As it stands.* "the fault most likely **lies** in CM1's own threaded loops, where it remains unlocated; a threaded
  run of stock CM1 with these boxes' options would test whether it **lies** there."
- *What happens.* The fault is in code, and "is in" states its place, most likely CM1's threaded loops (H26; defect
  log A6).
- *Fix.*
  > since every patch in a threaded region writes only its own points, the fault is most likely in CM1's own threaded
  > loops, where it remains unlocated; a threaded run of stock CM1 with these boxes' options would test whether it is
  > there.\claim{H26}

**V46** · `assumptions.tex`:180, Table 2, row "Columns", column "On the Moon"
- *As it stands.* "**Miss** a net 5.8~W\,m$^{-2}$ loss"
- *What happens.* The flat, sunlit-only columns omit the net loss that the curved shells compute (H11); the text says
  PlaSim's bands "omit" gases in the same sense.
- *Fix.* `Omit a net 5.8~W\,m$^{-2}$ loss`

**V47** · `assumptions.tex`:182, Table 2, row "Shortwave gases"
- *As it stands.* "Their share **taken** by water"
- *What happens.* The water absorbed their share lower down, as the text at line 76 says.
- *Fix.* `Their share absorbed by water`

**V48** · `assumptions.tex`:187, Table 2, row "Cloud thresholds"
- *As it stands.* "**Moved** the climate up to about 6~K in tests"
- *What happens.* The threshold is a setting, and the test changed it: lowering the lowest layer's threshold from
  0.983 to 0.6 cooled the global mean by 5.0 K over the years averaged and about 5.9 K settled (G05, G16).
- *Fix.* `Up to about 6~K in the global mean in tests`

**V49** · `assumptions.tex`:207, Table 2, row "Gravity, ventilation"
- *As it stands.* "ventilation **tied** to Earth's fall speeds"
- *What happens.* As in V29.
- *Fix.* `9.8 twice; ventilation from Earth's fall speeds`

**V50** · `assumptions.tex`:212, Table 2, row "Flash reach"
- *As it stands.* "Weak flashes high in thin air **logged** no reach"
- *What happens.* The released `lightmsz` logged no reach for these flashes, whose charge stayed below its threshold
  `scth` (defect log A8).
- *Fix.* `No reach logged for weak flashes high in thin air`

### `repairs.tex`

**V51** · `repairs.tex`:16
- *As it stands.* "CM1 **takes** its switches in two other forms:"
- *What happens.* The patches implement CM1's switches as preprocessor constants and as spare namelist reals (R01;
  `models/cm1/README.md`).
- *Fix.*
  > In CM1 the switches have two other forms:

**V52** · `repairs.tex`:21
- *As it stands.* "Whatever their switches, most repairs **fall** into three classes"
- *What happens.* As in V12.
- *Fix.*
  > Whatever their switches, most repairs belong to three classes, which differ in what was fitted to the test world.

**V53** · `repairs.tex`:24–26
- *As it stands.* "a general method computes a quantity of the world's own column offline and **enters** it as
  computed, as the curved-air terms **enter** as differences between spherical and flat solutions of a design column"
- *What happens.* The intransitive "enter" is the author's first example again. The method computes the table offline,
  and the patched codes read it and apply the terms to every column and hour (R06; the paragraph "Curved air": "the
  terms are applied in the patched codes").
- *Fix.*
  > One step nearer the world, a general method computes a quantity of the world's own column offline, and the
  > patched codes apply it as computed, as they apply the curved-air terms, differences between spherical and flat
  > solutions of a design column.

**V54** · `repairs.tex`:30–31
- *As it stands.* "so the tables **class** it as a calibration"
- *What happens.* The change was classed as a calibration, and Tables 2 and 6 list it under that class.
- *Fix.*
  > so the tables list it as a calibration.

**V55** · `repairs.tex`:48–49
- *As it stands.* "the ten output means of each model day **fall** at the same places in every year"
- *What happens.* PlaSim writes ten output means each model day, and with twelve whole model days a year it writes them
  at the same places in every year (defect log A3).
- *Fix.*
  > with a year of 17,160 half-hour steps, twelve whole model days, the ten output means of each model day are written
  > at the same places in every year, although the synodic Sun still shifts ...

**V56** · `repairs.tex`:57–58
- *As it stands.* "Because gravity **enters** the fall-speed laws through the balance of weight and drag"
- *What happens.* The author's first example again. The laws depend on gravity through that balance: the Best number of
  a particle of fixed size is proportional to g (R02; `notes/cm1.md`, "Fall speeds").
- *Fix.*
  > Because the fall-speed laws depend on gravity through the balance of weight and drag, their repair follows from a
  > similarity argument.

**V57** · `repairs.tex`:63–64
- *As it stands.* "whereas snow and ice crystals, whose mass and area follow other powers, **take** a larger gravity
  exponent than the patch gives them"
- *What happens.* For snow and ice the exponent is (B + 1)/(β_m + 2 − σ_A), larger than the patch's (`notes/cm1.md`,
  "Fall speeds"); the crystals have it by their mass and area laws.
- *Fix.*
  > whereas snow and ice crystals, whose mass and area follow other powers, have a larger gravity exponent than the
  > patch gives them.

**V58** · `repairs.tex`:65–66
- *As it stands.* "although in NSSL the ventilation **needed** its own scaling at eleven sites"
- *What happens.* Rain's and cloud ice's ventilation were scaled as the fall speeds scale, at all eleven sites (defect
  log B3).
- *Fix.*
  > although in NSSL the ventilation had to be scaled separately at eleven sites.

**V59** · `repairs.tex`:69–70
- *As it stands.* "though the boxes, **rounding** to whole sub-steps, run one 8~s sub-step per model step"
- *What happens.* The graft's driver rounds each model step to whole sub-steps, `nsub = max(1, nint(dtp/dts))`
  (`models/cm1/fortran/terluna_elec.F` 234; defect log B6); the boxes run what the driver sets.
- *Fix.*
  > though, with the graft's driver rounding each model step to whole sub-steps, the boxes run one 8~s sub-step per
  > model step.\claim{R03}

**V60** · `repairs.tex`:76–77
- *As it stands.* "and its Sun **follows** a solar day, a flux and a starting hour angle read from spare namelist
  reals"
- *What happens.* The figure of the author's second example. Core patch 05 computes the Sun from a solar day of
  `var19` seconds, a flux of `var17` W m⁻² and an hour angle starting at `var18` and growing along the ring
  (`models/cm1/README.md`; defect log B10).
- *Fix.*
  > and its Sun is computed from a solar day, a flux and a starting hour angle read from spare namelist reals, with
  > each column of a ring at its own longitude;

**V61** · `repairs.tex`:81–82
- *As it stands.* "the flash log records each channel's reach from the charge the flash **hands** to the ions"
- *What happens.* The branched lightning neutralises charge and adds the opposite charge to the small ions
  (`models/cm1/fortran/terluna_branched.F`, header; defect log A8); "hands" personifies the flash.
- *Fix.*
  > and in the patched graft the flash log records each channel's reach from the charge the flash adds to the ions,
  > where the released code recorded it only above a charge threshold set for Earth's storms.

**V62** · `repairs.tex`:111–112
- *As it stands.* "so by day the terms also **move** PlaSim from the two-stream reference it was calibrated against
  toward the successive-orders solver"
- *What happens.* The daytime terms include a solver difference, 1.3 % of the sunlight at the ground with the Sun
  overhead (R07), so adding them shifts PlaSim's sunlight toward the successive-orders solver's.
- *Fix.*
  > so by day the terms also shift PlaSim's sunlight from the two-stream reference that PlaSim was calibrated against
  > toward the successive-orders solver's.\claim{R07}

**V63** · `repairs.tex`:125–126, Figure 3 caption
- *As it stands.* "the Moon's factors for water vapour and for well-mixed air **come** from straight rays through the
  design column's shells"
- *What happens.* The factors were computed along straight rays through the shells (S09, R06).
- *Fix.*
  > the Moon's factors for water vapour and for well-mixed air are computed along straight rays through the design
  > column's shells.

**V64** · `repairs.tex`:160, Figure 4 caption
- *As it stands.* "With the bands the layers **come** within 0.97~W\,m$^{-2}$ rms of the reference"
- *What happens.* With the bands, PlaSim's absorption by layer agrees with the reference within 0.97 W m⁻² rms, from
  1.71 (R10).
- *Fix.*
  > With the bands the layers agree with the reference within 0.97~W\,m$^{-2}$ rms, against 1.71 as run;

**V65** · `repairs.tex`:172–173
- *As it stands.* "Ground strikes **needed** a bound, because WRF-ELEC's two Earth rules bracket them widely on the
  Moon"
- *What happens.* The count of ground strikes was bounded between the two rules by a leader-crossing condition (R13;
  defect log B5).
- *Fix.*
  > Ground strikes had to be bounded, because WRF-ELEC's two Earth rules bracket them widely on the Moon:

**V66** · `repairs.tex`:175
- *As it stands.* "only if its potential can **carry** a leader the rest of the way down"
- *What happens.* `terluna_crosses` (`models/cm1/fortran/terluna_lightning.F` 34–63) takes the potential where the
  flash started, less the drop along the channel at the leader's internal field scaled with density, and counts a
  strike only if that potential exceeds the air's by the streamer zone's need at every level down to the ground; the
  potential drives the leader, a physical cause.
- *Fix.*
  > as a strike only if its potential can drive a leader the rest of the way down, at an internal field of
  > 1~kV\,m$^{-1}$ at sea-level density, scaled with the air's density.

**V67** · `repairs.tex`:177–178
- *As it stands.* "The graft's ice **needed** a mitigation:"
- *What happens.* The ice size the radiation reads was capped at 140 µm, with the excess logged (defect log B23).
- *Fix.*
  > For the graft's ice a mitigation was added: where the ice outgrows RRTMG's optics, CM1's radiation reads sizes
  > capped at 140~\textmu m and logs the excess.

**V68** · `repairs.tex`:185
- *As it stands.* "Two of these absences **showed** in the runs."
- *What happens.* The runs showed the effects of two absences: the first box rained in the mornings until it was
  stopped at day 47, and the missing transport accounts for about a third of the 45° N ring's warm offset (H32).
- *Fix.*
  > Two of these absences had visible effects in the runs.

**V69** · `repairs.tex`:188–189
- *As it stands.* "CM1 **receives** what the slice lacks from the GCM's fields, and with those fields the Earth values
  that remain in the GCM."
- *What happens.* CM1 reads the GCM's fields, which the GCM computed with its remaining Earth values; the values
  themselves stay in PlaSim's code.
- *Fix.*
  > CM1 receives what the slice lacks from the GCM's fields, which the GCM computed with the Earth values that remain
  > in it.

**V70** · `repairs.tex`:195
- *As it stands.* "while the GCM's mean vertical wind **enters** CM1's own large-scale advection"
- *What happens.* The author's first example again. Core patches 10–14 give CM1's own large-scale vertical advection
  the GCM's mean vertical wind, against height or by column (`models/cm1/README.md`).
- *Fix.*
  > while CM1's own large-scale advection uses the GCM's mean vertical wind;

**V71** · `repairs.tex`:196–198
- *As it stands.* "Beyond the storms, the seas **take** their forcing from the GCM as well: ... so that its friction
  velocity **lies** within $-2.5$ to $+1.2$\% of the GCM's"
- *What happens.* The GCM's surface stress drives SWAN, and SWAN's spectra drive SWASH (R15); the GCM forces the
  modelled seas, and the friction velocity is within that range of the GCM's.
- *Fix.*
  > Beyond the storms, the GCM forces the seas as well: SWAN is driven by the GCM's surface stress, converted through
  > Wu's drag law inverted to an equivalent wind, so that its friction velocity is within $-2.5$ to $+1.2$\% of the
  > GCM's, ...

## Figures let stand

- **Physical agents and processes**, as the charge allows: gravity "raises every pressure level", "roughens the
  surface and slows the waves"; the solar day "deepens the soil's thermal wave"; the shield "removes the
  ultraviolet"; sunlight, a lightning channel and a thermal wave "reach"; bodies "keep" and "hold" their air; Earth's
  tilt "brought Earth's seasons and summer rain to 60°"; the Moon's slow rotation and small tilt "made all three
  large".
- **Matter at a place**: the air's mass "lies on average 48.6 km above the ground", half the air "still lies above the
  Moon's geometric shadow", and the lowest 7.5 km of air "lie beyond" RRTMG's reference pressures
  (`assumptions.tex`:86), with pressure as the vertical coordinate.
- **Runs as agents of their own trajectories**, on `AGENTS.md`'s model "the run warmed 2.3 K": a run "passed 310 K",
  runs "part from one another", the first box "rained in the mornings", "the paths the lunar runs take".
- **Code in code's own verbs**: codes take, read and pass inputs ("SWASH ... takes lunar gravity as an input", "take the
  curved geometry from the general method", "pass forcing to one another", "passed 157 µm to the radiation", the
  formula "reads lunar rain as about 30 times heavier"); namelist reals "hold" values; a patched value "becomes" a
  parameter; a repair "corrects", "applies" and "removes"; and the modelling usage in which a model "forms its own
  clouds and rain", "separates charge" and "conducts no charge", and fields "drive" or "force" a model.
- **Results of a computation**: the cloud-water profile "leaves cloud too wet aloft", the absorptivity "left the air
  absorbing" too little, the skip "left sunlight ... short", the longwave correction "leaves 1--5 W m⁻² from column to
  column"; each states the outcome of arithmetic that its sentence or the one before names.
- **Relations stated exactly**: "hold(s)" for validity, by which the paper defines its classes and which the approved
  abstract uses, and for containment (a column, a year, a cell); "err"; "depart(s) from" and "along", the paper's term
  for a world's distance from Earth along a ratio of Figure 1, also in approved wording; "meet their conditions"
  (satisfy); "govern", "fix(es)", "set(s)", "determine", "depend on", "follow from", "accounts for"; "measures", for
  the scale height over the radius as the measure of curvature; "binds", for an active bound; "cover" and "begin", for
  a table's range; "slips", the offset of 120 steps a year that Table 2 and Repairs name; "respond" and "stretch" for
  fall speeds and the dry dynamics, the second approved by the author in the Conclusion.
- **Procedures and documents in their own acts**: a calibration "fitted" and "brought ... within" its tolerance; the
  fit "placed sunlight low"; the appendix and tables "give"; the defect log and ExoPlaSim's description "record";
  source comments "call".
- **Approved wording and the author's directions**: the ensemble "could then follow the consequences" (abstract; the
  ensemble computes each link of the chain, each model forcing the next); "errors that go unnoticed", an idiomatic
  passive; "Some exoplanet climate studies hold ... and vary", the wording of `AGENTS.md`'s direction of repair, with
  the authors named in the next sentence; "Most repairs follow one rule", whose verb the author's direction of repair
  kept.
- **Read and kept for their own reasons**: "PlaSim's lowest model level ... reads up to 20 K too cold"
  (`assumptions.tex`:134), since the defect log places the artefact in the written output (A4) and "is" would place
  it in the model's air; "the world that needs it", where the same clause names the operation, switching the repair
  on; "comes first", for the order of planned work; "a convention separates", "the absences ... are filled", "Running
  CM1 ... adds structural limits"; "cluster", "combine" and "linking", for a distribution, a possession and a
  coupling.

## Other findings

None. I found nothing BLOCKING or MAJOR in the front half's prose or evidence, and nothing MINOR beyond its verbs in
the text that rounds 19 and 20 changed: the count of four defects in the abstract, the Introduction and Assumptions,
the two faults of uncertain cause in Assumptions, Repairs and Table 2, the note on terms, the Moon's ancient air
(checked against Needham and Kring's archived text, "may exceed this estimate") and the curved-air table recomputed
from another world's column and starlight. The one error of meaning I met, the relative clause in V33, the verb fix
mends.

## Checks

- **Snapshot.** `git rev-parse HEAD` gave `a50e0b177d089b6ccb232eafbf94cd157ae4a4af` and `git status --short` printed
  nothing before I began; `sha256sum paper/build/main.pdf` gave `f6ff147f…3f`, the hash in the charge. I used
  `pdftotext -layout` on that PDF only to confirm the numbers of its tables and figures.
- **Diff.** `git diff --word-diff ffdedfe a50e0b1` over `main.tex` and the front half's files, read whole.
- **Word screens.** A `grep` of the front half for the verbs the charge names (enter, keep, carry, hold, meet, bring,
  take, reach, pass, sit, lie, hide, live, answer, ask, tell, see, decide, need, play, come) and for a second list
  (show, move, drive, give, make, let, add, become, count, cover, span, put, leave, read, govern, measure, respond,
  stretch, stand, separate, raise, lower, tie, descend, combine, link, cluster, and the generic analytical verbs); I
  read every hit in context, and the sentence-by-sentence reading covered the verbs on neither list.
- **Lint screen**, screening only: `python3 paper/tools/lint.py` on the six front files, which reads and prints. It
  gave 11 "possible empty action" candidates, of which my reading flagged two (V30, V66); the rest are physical
  "reach" (sunlight, a channel, a thermal wave, soil layers) and the noun "reach" in Table 2 and the flash log. It
  gave no "not" and no "rather than". Its word list lacks the verbs of the other 69 findings, which the reading
  found.
- **Evidence for the fixes.** Each "What happens" cites the claim, note, README or code line it rests on; for V32–V33 I
  read CM1 r22.0's `radconst` and `calc_coszen` in the pinned source, for V59, V61 and V66 the graft's Fortran, and
  for V4–V5 the archived text of the two ROCKE-3D papers.
- **Fixes screened** for "not" and "rather than": none present.
- **Cadence.** Silent reading only.
