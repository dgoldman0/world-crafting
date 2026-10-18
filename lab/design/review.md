# Review record

Reviews of the design documents against the author's prose rules (Terluna
`ensemble/planning/source_controls/STYLE_NOTES.md`, `Jewish_Papers_Updated_Style_Notes.md`,
`Agent_Working_State_Editorial_Gates.md` and the Open Moon charter's G1–G4). Each reviewer was a fresh,
read-only agent briefed with the rules and the four sources. None had seen an earlier round's findings.
Lexical scans served as screening only. The author's question on draft 1's model configurations led to
draft 2, and the author's answers to the open questions led to draft 3.

| Round | Date | Reviewer and files | Blocking | Minor | Technical |
|---|---|---|---|---|---|
| 1 | 2026-10-17 | A: README, architecture, plan | 9 | 22 | 12 |
| 1 | 2026-10-17 | B: inventory, regeneration, world_spec | 9 | 28 | 11 |
| 2 | 2026-10-17 | A: README, architecture, plan | 5 | 27 | 7 |
| 2 | 2026-10-17 | B: inventory, regeneration, world_spec | 3 | 23 | 6 |
| 3 | 2026-10-17 | A: README, architecture, plan (confirmation round: blocking items and contradictions only) | 2 | — | 7 |
| 3 | 2026-10-17 | B: inventory, regeneration, world_spec (the same) | 1 | — | 6 |
| 4 | 2026-10-17 | A: README, architecture, plan (confirmation round) | 4 | — | 2 |
| 4 | 2026-10-17 | B: inventory, regeneration, world_spec (confirmation round) | 0 | — | 2 |
| 5 | 2026-10-17 | A: README, architecture, plan, with the new seeds for consistency | 4 | — | 10 groups |
| 5 | 2026-10-17 | B: world_spec, regeneration and every seed, schema against seeds | 0 prose; 10 schema and seed | 3 | — |
| 6 | 2026-10-17 | A: README, architecture, plan, with the seeds (confirmation round on draft 2 as revised) | 0 | — | 9 |
| 6 | 2026-10-17 | B: world_spec, regeneration, every seed and the registry (the same) | 1 prose; 4 schema and seed; 1 between the documents | 4 | — |
| 7 | 2026-10-17 | A: README, architecture, plan, with the seeds (confirmation round) | 2 prose; 5 technical | — | — |
| 7 | 2026-10-17 | B: world_spec, regeneration, every seed and the registry (the same) | 3 seed; 4 between the documents | 2 | — |
| 8 | 2026-10-17 | A: README, architecture, plan, with AGENTS.md and the seeds (the single round on draft 3) | 3 prose | — | 9, and 3 minor |
| 8 | 2026-10-17 | B: world_spec, regeneration, every seed and the registry (the same) | 2 prose; 3 seed; 2 between the documents | 1 | — |
| 9 | 2026-10-18 | A: README, architecture, plan, with AGENTS.md and the seeds (the single round on draft 4) | 6 prose | — | 10, and 4 typed values |
| 9 | 2026-10-18 | B: world_spec, regeneration, every seed and the registry (the same) | 1 prose; 8 seed; 6 between the documents; 3 typed values | 2 | — |
| 10 | 2026-10-18 | The final review before coding | pending | — | — |

## Round 1 dispositions

**Revised: every blocking item.** These were:

- self-description in the opening of the regeneration map;
- disclaimers in the inventory's opening and in the README's state line;
- "not", "instead" and "rather than" contrasts;
- abstractions given agency ("wait", "await", "reaches", "the design refuses");
- the five repeated "N things:" frames;
- a recap landing in the importer paragraph;
- a bead pair in the inventory's analyses section;
- the unclear landing on the CM1 side's two sources.

**Revised: every minor item, with one adapted.** The three gravity-scaling bullets in the architecture
stay as bullets, but their relation is now written in.

**Technical items, all adopted:**

- **Plan.** The fixpoint loop moved to a new stage 8, after jobs exist, and stage 7 gained a pass condition.
- **Envelopes.** Only fits record envelopes; the README had claimed every product does. The definition of
  staleness now covers the whole key.
- **Seeds.** The seed experiments gained the 45° N ring pair and the Jura box, and the cases add patch
  series consistently.
- **The regeneration map.** The time-step row was corrected, three edges were added to the graph, and the
  worked examples now match the matrix's loop marks.
- **Kinds.** Worlds gained a `kind` field, found or illustrative.
- **The inventory and specification.** Corrected: the units rule, `TH2OC`'s source, the separation of
  `A28_dim5` from `A28_dim5_moon`, and RRTMG's range at 1.2 atm.

**Found outside the reviews and corrected.** The CM1 wall times were summed again from each case's
`progress.json`: rings 1.8–12.3 h and boxes 2.3–27.2 h for two lunar days, where the earlier draft said
5.7–12 h and 7–27 h.

## Round 2 dispositions (reviewer A)

**Revised: every blocking item.**

- The registry row's self-reference.
- The Earth control's missing criterion; a criterion is now proposed, as open question 5.
- The paired Terluna-defect sentences in "Storage and records", now tied to what the importer does.
- The engine row's objection catalogue. The Snakemake wrapper now appears where the cluster scheduler
  enters.
- The plan's disguised list in its opening.

**Revised: every minor item.**

**Technical items, all adopted.** These include:

- the before-run envelope check limited to the dimensions a scenario fixes;
- the fixpoint's pass limit, and the evidence state for a loop that stops unconverged;
- the GCM cost corrected to 73–93 minutes;
- the read-only list in the plan completed with the runners and the yearly output.

## Round 2 dispositions (reviewer B)

**Revised: every blocking item.** These were:

- the regeneration map's opening, rebuilt so that its sentences depend on one another;
- the reuse of the reference model's caches, tied to its pinned inputs;
- the consumers of superseded products, joined to the numbers copied by hand.

**Revised: the minor items.** One judgement call stands as it was: three hand steps in the inventory repeat
rows of its products table, so that the list reads whole as a register.

**Technical items, all adopted.** These include:

- the "O2, CO2, Ar/N2" row of the matrix split, since Ar/N2 alone changes no compiled CM1 constant;
- a note under the graph that Terluna's builds read their air from a GCM run's record;
- PlaSim's levels limited to the three calibrations they enter;
- the scenario's definition widened to found states;
- the spectrum files named as written and as copied.

## Round 3 dispositions

**Revised: all three blocking items.**

- The README's sentence on the first worlds, moved to follow "described once".
- The architecture's opening paragraph. The refusal now joins the Earth-like air it bounds, and the new physics
  moved to the model adapters.
- The two notes under the regeneration graph, set as a legend.

**Technical items, all adopted.**

- **Architecture.**
  - The refusal list counts five cases, the declared pair among them.
  - A build's key covers its compiler, and specifications may be written by the lab's own commands.
  - The example session creates a new scenario at a sunlight scale of 0.960.
  - The envelope check before a run covers what the scenario and configuration fix.
  - The reach report is evaluated for a world, a scenario and a configuration.
- **The regeneration graph** gained the seven edges the matrix implies, and the matrix gained a row for the
  world's surface heights.
- **Numbers and rules.**
  - The 1.0 atm O2 mole fraction is corrected to 0.20949.
  - The star's total now marks the planet record.
  - The solar day left the list of compatibility quirks, since the seed states it with its basis.
  - "Run by hand" now covers the session scripts.

## Round 4 dispositions

**Revised: reviewer A's four blocking items.**

- The architecture's opening, where the Open Moon now joins the sentence on the first worlds.
- The adapter section's opening, which ties the new physics to the model versions.
- A because-clause that repeated its premise, which now names the cause.
- The cluster sentence, which had the agency reversed.

Reviewer B found no blocking item in the inventory, the regeneration map or the specification.

**Technical items, all adopted.**

- The decision on patches leaves the editing of Terluna's runners to Terluna.
- The job runner's free-disk test reads as a minimum.
- The regeneration matrix sends every change of the GCM experiment into the CM1 case inputs, and marks the
  longwave correction as directly dependent on gravity, pressure and the air, with the graph's edges to
  match.

## State after round 4

- **Inventory, regeneration map, specification:** came back with no blocking finding.
- **README, architecture, plan:** round 4's blocking items are revised, with no confirmation round run after
  them.

The next round is due once the author's answers to the open questions change the text.

## Draft 2

Draft 1 is tagged `lab-design-draft-1` (commit edcf5dd). The author asked on 2026-10-17 whether the model
configurations come from a base and where the unified set-up sits. Draft 2 answers with two changes:

- **Shared defaults for each model,** stated for any world (`lab/configs/<model>/defaults.toml`). CM1's
  defaults carry named variants (twilight, terrain, sea, electrified) and give their lengths and time step at a
  reference gravity, the Moon's, which the adapter scales by g_ref/g.
- **One study file per scenario,** setting up the whole chain (`lab/studies/open-moon.toml`): the GCM runs and
  the CM1 cases forced from them, each extending its model's defaults, with Terluna's quirks held as the
  study's compatibility settings.

The architecture, the specification schema, the plan, the regeneration graph, the README and the registry's
conditions changed with them, and those sections reopen for review in round 5.

## Round 5 dispositions

**Revised: reviewer A's four blocking prose items.** These were:

- the excluded scenarios, now stated as what the adapted models exclude;
- the pair check's counterfactual and restatement, now one sentence of what the importer does;
- the doubled "give" in the gravity-scaling bullet;
- the run-length sentence, now its own bullet with the reason the pair scaled it.

**Adopted: every technical item from both reviewers.** These were:

- **The lw_ice pair's initial state,** which moved into its declared delta. A set value now replaces the
  parent's whole, and descriptive fields may sit outside the delta (world_spec rule 6).
- **Byte-for-byte reproduction.** The study's compatibility settings now hold:
  - Terluna's typed calibration values and eccentricity;
  - the products its runs read, by recorded hash, which carry the reference tools' Ar/N2 and the 0.95
    design column with them (rule 8).
- **Stage targets.** Stage 2 holds only the study's two runs, the other 32 move to stage 7 with the
  importer, and stage 3 names the builds the study's cases resolve to.
- **Keys.** A run's product key names its folder, and Terluna's run key stays beside it as a guard.
- **"Default".** "Identity default" now names a patch's released behaviour, and the lab's model defaults
  switch repairs on for every world.
- **Scaling with gravity** applies where a grid follows the scale height, as CM1's does; ExoPlaSim's
  defaults hold no scaled lengths.
- **CM1's damping rate and boundary-layer length** are values at the reference gravity, unrounded, which
  scale to 1/300 per second and 75 m on Earth.
- **Variants** change settings through `set`, so the electrified variant switches the microphysics.
- **Registry tolerances** are relative. The refused schemes' gravity test (0.5%, proposed) passes the Earth
  control. B13 credits patch 08 for the air's slant factor, and A1's skip angles are corrected at 12 days.
- **The Moon's orbit** follows Earth's file, and the Earth control's geometry is the model's own.
- **Units, sources and fields.**
  - Units follow their suffixes (rule 1), and `from_days` gains its suffix.
  - The Earth control names its sources.
  - `none` is allowed for a filter, and the Earth and Mars scenarios state their infrared from space.
- **The regeneration matrix** marks the derived quantities for the shield, the scale and the CM1 grid, and
  the graph feeds the CM1 settings into them.

**Corrected: three numbers.** Earth's CM1 lengths are given at CM1's 9.81 m/s², H/R is 0.03015, and the Sun
clock's step lies just above 12 days.

## Round 6 dispositions

Reviewer A found no blocking prose in the README, the architecture or the plan.

**Revised: reviewer B's prose item.** Rule 8's sentence on the Moon's solar day joined rule 2's Moon bullet.

**Adopted: every schema and seed item.**

- **The twilight variant** sets `physics.twilight`, which the CM1 defaults now define as `none`.
- **Byte-for-byte reproduction** covers a run's inputs and its builds' sources (rule 8).
  - The study holds the labels of the deployed builds whose sources its cases' builds reproduce.
  - The lab compiles at its defaults' flags, so the -O2 control of the 45° N pair (C8) is reproduced in its
    inputs alone.
  - CM1's namelist writer rounds the boundary-layer length and the damping rate as Terluna's does, on every
    world (rule 7).
- **The Earth control's sunlight** is the world's TSIS-1 spectrum at 1361 W/m², and the released run of the
  comparison takes the same sunlight and air through ExoPlaSim's own interface. Released ExoPlaSim's default
  is 1367 W/m².
- **Registry entry A1** tests `exoplasim_rotationperiod_days`, a quantity the specification now names. The
  adapter passes `rotationperiod` = 1 for a world whose stated solar day is exactly one day (rule 7), so A1
  stays silent on Earth.
- **The regeneration matrix** marks the planet record for a change in the star spectrum's shape.

**Adopted: reviewer A's technical items.** These were:

- CM1's run length counting the world's solar days, with its intervals in seconds;
- stage 1's comparison of the CM1 lengths after the rounding of Terluna's namelist writer;
- the build labels, as above;
- the MYNN refusal at more than 0.5% from 9.81 m/s²;
- a world's stated gravity, with its basis, in the principles;
- the calendar's consequences: the steps per model day, the run length, the steps per mean and the output
  count;
- stage 8's first runs of the lab's own, the fixpoint's GCM runs on the 1.2 atm Open Moon;
- the twilight ring's segments at 275 s;
- the session example, whose extended study inherits the runs and cases and earns keys of its own.

**Minor items.** Adopted: Earth's semi-major axis names its source, the 1.0 atm scenario is called an
extension, and worked example (c) notes the registry entries beyond the seed that stage 6 adds. The citation of
ExoPlaSim's calendar moved to lines 2618–2619. One item stands: `droplets_cm3` keeps Terluna's name, which
rule 1 allows.

**Checked while revising.** Terluna's deployed builds carry their labels in the Makefile's OPTS comment
(`cm1/build/<label>/src/Makefile:81`), and `cm1_run.py:2004-2005` rounds `rdalpha` to eight decimals and
`l_inf` to one.

## State after round 6

- **README, architecture, plan:** no blocking finding in round 6. Its nine technical items are revised.
- **Specification, regeneration map, seeds and registry:** round 6's blocking items are revised. Round 7
  confirms them.

## Round 7 dispositions

**Revised: reviewer A's two prose items.** The scaling bullet's parallel now runs "by 1 on the Moon … and by
0.166 at CM1's Earth gravity", and CM1's run length "is set in the world's solar days".

**Adopted: every technical item from both reviewers.**

- **The Earth control** opens plan stage 8, with its study and its two runs.
- **A box's forcing from a ring** enters the architecture's definition of a case and its coupling.
- **Build labels** stay outside the pair check, since a label is a Makefile comment that leaves the
  executable unchanged.
- **Calibration products** are read where a run's switches use them, so the design case leaves the
  longwave fit unread.
- **The water continuum** joins the architecture's producers and calibrations, and the regeneration graph,
  producers table and matrix, where it shares the longwave correction's marks.
- **The design run's starting state** moved to the study's compatibility settings beside the lw_ice run's.
  A run of the lab's own starts from ExoPlaSim's own state unless it branches from another run of its
  study.
- **The 1.0 atm scenario** cites the architecture's decisions and regeneration example (b).
- **The Earth control's sources.** Its ocean, sunlight and forcing name their bases, rule 3 asks a basis
  of a model choice in any scenario, and Earth's stated solar day rests on the mean solar day.
- **The regeneration graph** gained the edges from CM1's variants to its builds and from the surface
  geometry to the planet record. The matrix marks the planet record as produced again by a change in the
  heights or the seas, and by a stated solar day, and the GCM run where that day crosses one day.

**Adopted: reviewer B's two minor items.** The box names its site by `latitude_deg` and `longitude_deg`,
and the model day takes PlaSim's one-day branch, so registry entry B11 stays silent on Earth.

## Draft 3

Draft 2 is tagged `lab-design-draft-2` (commit 42a0ef3). The author answered the open questions on
2026-10-17, and draft 3 carries the answers with round 7's revisions:

- **Self-contained.** World-crafting becomes a standalone project: what the lab uses for its own work lives
  here and in its store, and Terluna's files serve its tests alone. Stage 1 copies the data the seeds pin,
  with their provenance, and AGENTS.md's rule on case set-up and runs changed on this branch.
- **CM1 compiled once.** A planned core patch reads gravity, CO2 and O2 from the namelist. Stage 3 checks
  it against Terluna's lunar build and against the build compiled with the macros' defaults.
- **Accepted as proposed:** the order after the 1.2 atm Moon, the refusal outside an envelope with an
  explicit override and a clear warning, and the Earth control's test.
- **The longwave correction** is refitted with ice optics on.
- **The engine.** The author leaned against draft 2's in-house engine, and draft 3 proposes Snakemake to
  schedule and run the stages, for the author to confirm. The three registry thresholds remain proposed.
- **Review cadence.** The author asked for fewer rounds: from round 8, one round follows each substantive
  revision, and its findings are acted on without a confirmation round.

## Round 8 dispositions

**Revised: the five prose items.** Reviewer A's were the engine row's signpost, the Earth control's two
joined propositions, and the plan's cost bullet, whose rewrite also corrected the stages that run on one
core. Reviewer B's were rule 7's solar-day sentence, whose "then" now follows the one-day world, and the
regeneration legend's turn back to Terluna.

**Adopted: reviewer A's technical items.**

- **Keys before runs.** Each stage declares its read set, so a product's key follows from the
  specifications before the product exists, and the tracking view refuses a read outside the declaration.
  Stage 4 tests the planner by the `open-moon` study's keys before and after each worked change, and the
  lw_ice envelope check moved to stage 7, after the import.
- **One test of staleness.** Snakemake runs with its file-time trigger alone on key-named,
  write-protected products. A long run declares its record, and downstream stages read the folder the
  record names. A build at `-march=native` keys the CPU type.
- **The electrified build** gains a companion namelist patch, and stage 3 compares it with `moon_omp_elec`.
- **Reproduction after the namelist patches.** A CM1 build names its point in each series, and the study's
  compatibility settings hold the point before the namelist patches: core 17, electrified 9.
- **Stage 3's thresholds.** Output that differs from the compiled build's passes within a last-bit nudge's
  difference, Terluna's test for its `-O3` rebuild, and the timing is the best of three on a quiet machine.
- **The fixpoint** starts from the lab's own run of the design case, and stage 5 reproduces Terluna's
  correction.
- **The Earth control's calibrations** are the released model's own shortwave multipliers and water
  continuum, with the ledger and gas-band fits of Earth's own column.
- **Earth's calendar.** At `rotationperiod` 1 the year sets the days, 365 for Earth, and stage 1 checks it.
- **Envelopes** include the switches in force, so a fit made with ice optics off flags a run with them on.
- **Minor items.** The lab's own runs wait for stage 7's machine budget, `shared/constants.json` is in the
  repository already, and Snakemake appears as proposed in the opening and in stages 4 and 7.

**Adopted: reviewer B's seed and technical items.**

- **A reference temperature,** `air.reference_temperature_k`, enters the schema and every scenario seed:
  294.9 K for the Open Moon's design column, 288 K for Earth and for the Mars illustration. The regeneration
  matrix gains its row, and stage 1 derives the paper's rows at the temperatures `paper/data/worlds.json`
  states.
- **Pins.** Rule 4 defines `terluna:`, `terluna-drive:`, `#` and `@`, and separates the manifest's copies
  from the files that the reproduction tests open in place.
- **Units.** `model_years` and `model_year` replace `years` and `year`, and rule 1 names the `model_`
  prefix.
- **Bases.** The Mars illustration's level, pressure, ocean, sunlight and forcing, and the Earth control's
  CO2, give their bases.
- **The solar-day row** marks the GCM run where the stated day becomes or ceases to be exactly one day.
- **B21's threshold** is about 7.5 times Earth's H/R.

## State after round 8

Round 8 was the single round on draft 3, at the author's direction, and its findings are revised with no
confirmation round after them. Before stage 1, the author's confirmations of the engine and the three
registry thresholds remain.

## Draft 4

Draft 3, as revised after round 8, is tagged `lab-design-draft-3` (commit 4b313c3). On 2026-10-18 the
author asked whether raindrop size was hard-coded, and then for a look over every value the lab should
compute from a world's base parameters. Draft 4 carries the answers:

- **Raindrops.** Morrison's breakup diameter and its cap on rain's mean diameter scale with the capillary
  length, through the namelist's `brkup_db` and a planned patch, with NSSL's limits alike; the cloud
  droplets per cm³ moved from CM1's defaults to the scenario's air.
- **In the schema.** The sunlight scale may follow the reference temperature through a target stage; CM1's
  lengths, times and rates follow the scale height; gravity carries the spin term; the air may be given by
  mole fraction; ExoPlaSim's output interval is given in days and its time step checked against the
  advective limit.
- **In the models and tools.** CM1's soil layers follow the solar day and its Sun the season, through
  planned versions of patches 08 and 05; the ledger takes the scenario's ground albedo, the reference
  tools the scenario's air, and patch 10's ice-optics weights the spectrum at the top of the air.
- **Producers.** The geography producer derives the seas from the heights and the lakes from runoff, and
  the glow producer the infrared from space, both brought from Terluna.
- **Compatibility.** The `open-moon` study holds Terluna's values for each: its gravity, sunlight scale,
  soil layers, rain limits and ice-optics weights, and its seas and lakes by hash.
- **Registry.** Two entries joined the seed, `cm1-soil-day` and `cm1-equinox-sun`, and B28 names its
  planned repair.

## Round 9 dispositions

**Revised: the seven prose items.** Reviewer A's were these:

- the guard sentence, which now ends at the guard, with the output interval moved to the calendar;
- the orphan sentence on cloud droplets, deleted;
- the principles' unequal coordination, now two sentences;
- the plan's time-step item, now a check of its own;
- the decision row's "margin", now its basis;
- the CM1 header's "3%", now 2.8% for the length and 1.4% for the rate.

Reviewer B's was "Not timed", now "Untimed in Terluna".

**Adopted: the technical, seed and typed-value items.**

- **The reference state** of CM1's scaling is derived from `moon/open-moon` under Terluna's gravity, so the
  factors are exactly 1 in the reproduction study. The typed molar mass, which moved the model top by
  0.25 m, is gone.
- **Planned patches** follow core 17 and electrified 9, and each identity default reproduces the build
  without it, patch 08's 5 cm top soil layer included. A setting whose patch the build lacks resolves to
  what the build does, so the equinox-Sun and rain entries warn until the patches land, and B28 fires on
  anything short of the full capillary scaling.
- **Patch 10's weights** move to a planned ExoPlaSim patch 11, which reads them from the namelist (stage 2).
- **NSSL's two-moment rain** has its explicit breakup off, and stage 3 searches it for other limits.
- **Compatibility.** Quirks with fields of their own sit in `[compatibility.set]` by dotted path, so the
  registry tests what the reproduction runs, and rule 6 names the channel. The restart pins name their
  files, `MOST_REST.00019`, with their hashes.
- **Pins.** The shield's pin names its file, and the Moon's heights take a plain pinned name from the PDS.
- **Lakes** form a keyed chain: the scenario pins the first link, a study's run names `lakes_from`, and a
  derived run keeps its parent's lakes.
- **The target stage** averages the last ten model years and stops within 0.1 K or after six runs, first in
  each fixpoint pass; stage 5 builds it, and its runs follow stage 7.
- **Output steps** take the divisor of the steps per model day nearest the interval.
- **Seasons.** A case starts at its own sunrise, and its GCM reference averages ±15° of solar longitude
  about its season. The box's day–night forcing averages one solar day of the ring's output up to the
  scaled `day_night_top_m`. Terluna's whole years and 29.5 days are compatibility settings.
- **Mars** takes the reference temperature `settled`, which the fixpoint finds under the real Sun.
- **Regeneration.**
  - The target stage and the runoff chain add marks by rule.
  - The lab computes the design column at the reference temperature.
  - The spin term leaves a stated gravity as stated.
  - The ledger's albedo weights the mask's water, lakes included.
  - Patch 10's weights follow the shield as well as the star.
  - Mars's example names B11, B12 and the cloud droplets.
- **States and names.** The documents say draft 4, and CM1's defaults hold a reference state. The Earth
  control's comments name the fraction behind Terluna's partial pressure and its own Ar/N2 of 0.011963.

**Kept: ExoPlaSim's 30-minute step,** a stated model choice that the guard checks; a step derived from a
design wind would add a choice of its own.

## State after round 9

Round 9 was the single round on draft 4, and its findings are revised with no confirmation round after them.
Before stage 1, the author's confirmations of the engine and the proposed thresholds remain.

## The engine and the workflow

On 2026-10-18, with a user interface in view, the author chose a custom runner: a small local service that
keeps its job queue in the store, with the command line as its first client. Snakemake left the design. The
author also set the workflow for what follows. AGENTS.md now confines drafts and review rounds to the paper
(commit 6d3997c on main, merged into `lab`), and the lab's code follows a conventional software workflow.
Round 10 is the design's final review; after it, the design documents change with the code they describe.
