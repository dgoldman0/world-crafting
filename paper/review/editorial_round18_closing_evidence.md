# Editorial round 18, closing review: evidence and scope, 19 October 2026

Snapshot: commit `ffdedfef8b373301c7597d0385d779f23798c2d5` (ffdedfe); the working tree of `paper/` is identical to it
(`git diff --quiet ffdedfe -- paper`). Reader: a fresh Claude Opus 5.5 subagent, reading the whole paper for evidence
and scope at the close of round 18, with priority on the changes since round 17's records (`git diff 406549d ffdedfe --
paper`) and on the five approved-wording fixes of 51ea569. This record is the only file the reader wrote.

**What was read and checked.** `AGENTS.md`; `paper/review/editorial_round18.md`; `editorial_round17_evidence.md` and
`editorial_round17_dispositions.md`; the diffs 406549d..ffdedfe and 1278887..51ea569, and 1278887..51a6a60 for the text
that round 17's dispositions changed after its readers had seen it; `paper/main.tex` and every section in full, the
note on terms among them. The lakes sentence and the oxygen clause were set against Terluna's ecology branch at
`origin/domain/ecology` (4e4f710): `research/studies/lake_oxygen/README.md` in full, the opening of
`research/studies/sea_oxygen/README.md`, the module description of `biosphere/ecology/lake.py` and the lines that name
its laws, and the message of commit 3a9aa27. The five fixes were set against H23, W06, N01, G11, H07 and W01 in
`paper/claims.json` and against the body passages they summarise, and W06's formula was recomputed for TRAPPIST-1e and
Proxima Centauri b. The curved-air table's use of the incoming spectrum was read in `python/climate/gcm/twilight.py`.
Where the changed text cites a source, the archived original was read where one exists (Needham and Kring 2017,
Boutle et al. 2017, by `pdftotext`) and the manifest record otherwise (Zahnle and Catling 2017, Sergeev et al. 2022).
V10's narrowed sentence was set against Terluna's benchmark table (`climate/crm/README.md`:1755–1771 at 186b294).
`python3 paper/tools/check.py` ran.

**Judgment.** Every sentence changed since round 17 claims only what the paper's evidence, its cited sources or
general physics supports, and the reader found no BLOCKING or MAJOR evidence problem anywhere in the paper. The lakes
sentence in Next steps gives a sound physical reason, since a given contrast of temperature yields a buoyancy
proportional to gravity, names what is to be tested in the paper's own term, and brings in no number or finding from
the Terluna lake work behind it; the Conclusion's clause, for its part, stays a prospect, claims an exchange of oxygen
and no oxygen content, and leaves the Earth-fit condition to Next steps, which states it once. Moved word for word, the
note on terms defines the class as the abstract describes it and as Reach bounds it, and its closing clause agrees with
the Introduction's argument that an ensemble for the class needs adapted models and adapted exchanges between them. The
five approved-wording fixes match H23, W06, N01 and the body. The seven MINOR findings ask for precision: the forcing the lake and sea columns would take, the waters their laws were fitted on, and the
one-dimensional column that their own reason puts in question; two approved Conclusion sentences, one open to a reading
of concurrent coupling and one that leaves the star's light out of the curved-air table; the review history, which
stops before the author's reading of the five findings and before this round; and a source's estimate in the
Introduction, added in round 17's dispositions, given as a flat duration and recorded without a locator.

Counts: BLOCKING 0, MAJOR 0, MINOR 7.

## The lakes and seas

**1. next.tex:121–122 and conclusions.tex:95–97. MINOR.** *What fails:* the fields named as the columns' forcing go
beyond those the ensemble computes for the lakes. The ensemble's sea states are SWAN's, computed over the nearside sea
and the Smythii–Marginis basin, while the rain-fed lakes stand at their own levels and would take waves raised over
their own fetches; the Conclusion's "the same winds and waves, mixing the lakes and seas" gives the lakes the waves that
the same sentence has just sent to "a particular shore". In Next steps, a column also needs the GCM's surface heating
and cooling, which set the contrast of temperature on which the sentence's reason turns, while the sentence names winds
and sea states alone. *Evidence:* results.tex:192–200 and appendix.tex:36 (SWAN's domains); worlds.tex:40–41 (lakes at
their own levels); the lake model behind the sentence takes, at each lake's GCM cell, sunlight, infrared, the lowest
level's air temperature, humidity and wind, and the surface pressure, with no wave field (`lake_oxygen/README.md`, "The
forcing"; `lake.py`, module description, lines 5–30). *Fix:* in Next steps, "Beneath the waves, the GCM's winds and
surface heat fluxes, with the sea states over the seas, could force columns of the lakes and seas, ..."; in the
Conclusion, "and the same winds, mixing the lakes and seas with the waves they raise, would drive the exchange of oxygen
between their waters and the air". Both keep the framing the author agreed, a use of the ensemble's winds and sea
states, and go to the author for decision.

**2. next.tex:123–124. MINOR.** *What fails:* "fitted on Earth's lakes" says where the laws were fitted, cites no
source, and narrows what a sea column would take. The model behind the sentence takes lake fits for the gas transfer
(Cole and Caraco 1998; the surface-renewal model of Tedford et al. 2014), for the mixed layer (the General Lake Model,
Hipsey et al. 2019) and for the wind's share of its energy below the mixed layer (Wüest et al. 2000), while its mixing
efficiency below the mixed layer is Osborn's, from ocean turbulence, and its Schmidt numbers are Wanninkhof's. Terluna
ran the lunar seas, held fresh at 0.14 g/kg, in the same lake model; the paper leaves the seas' salinity unstated, so a
reader of "columns of the lakes and seas" would expect a sea column to take the ocean's fits of transfer and mixing. The bibliography and the manifest hold none of these sources. *Evidence:* `lake.py`, module description and
lines 72, 267–269 and 343–356; `lake_oxygen/README.md`, "Assumptions and limits", "Earth's ranges extended";
`sea_oxygen/README.md`, lines 1–25; a search of `paper/references.bib` for these authors. *Fix:* "fitted on Earth's
lakes and seas", which the paper's own definition of an Earth value covers without a citation; or cite the lake laws,
with manifest records.

**3. next.tex:122–124. MINOR.** *What fails:* the reason the sentence gives bears on the columns' form as well as on
their laws. A contrast of temperature that resists the wind's mixing sixfold more weakly at lunar gravity lowers the
Lake number sixfold for the same water and wind stress, and once that number falls below about 1 the wind tilts a thermocline
to the surface and stirs the deep water by basin-scale motions, which a one-dimensional column leaves out. The paper
counts simplifications used beyond the range they were made for among its Earth values (introduction.tex:85–89), and
the sentence names only the laws as the values to test. *Evidence:* the Lake number of Imberger and Patterson (1990)
scales with gravity through the stratification's buoyancy; Terluna's lake study finds the 352 m lakes' Lake number
below 1 on 51–90% of days and names a basin-scale model as the test (`lake_oxygen/README.md`, "The stirring one column
cannot hold"), and its sea study leaves basins many Rossby radii across to a three-dimensional model (commit 3a9aa27).
Those results stay out of the paper, as the author directed; the finding concerns the structural point alone. *Fix:*
"..., the transfer and mixing laws such columns take, fitted on Earth's lakes and seas, and the one-dimensional column
itself would be among the Earth values to test." The phrase extends the agreed framing, so it goes to the author.

## The approved wording

**4. conclusions.tex:12–14. MINOR. Approved wording (round 17, prose F40).** *What fails:* "Run together" can be read
as concurrent, two-way coupling, whereas every coupling in the body runs one way and offline: slices of a GCM state
force CM1, the GCM's surface stress drives SWAN, and SWAN's spectra force SWASH. The Conclusion itself places a two-way
exchange in the future: "Cloud requires a further exchange between the models", and "Iterating between the two would
make the cloud calibration depend on weather simulated for the world itself". *Evidence:* introduction.tex:71–79;
repairs.tex:182–203; conclusions.tex:45–53. *Fix:* "Chained through their forcing, the global and resolved calculations
could follow ...". For the author's decision.

**5. conclusions.tex:27–29. MINOR. Approved wording (round 17, prose F41).** *What fails:* framed now as a procedure
for specifying another world, the clause "its radius and atmospheric column determine a new curved-air table, while its
spectrum and columns determine the targets for the radiation fits" assigns the spectrum to the fits alone. The table's
sunlight terms were computed with the shield-filtered TSIS-1 spectrum's energy in every channel, and the channels
themselves were bisected by that energy, so under another star the table needs that star's light as well as the
column. The body's wording, recomputed "from that world's own column" (repairs.tex:112–113; reach.tex:5–6), has the
same gap. *Evidence:* `python/climate/gcm/twilight.py`:91–117 (`near_infrared_optics`, "with the shielded sunlight's
energy"); appendix.tex:7–14; worlds.tex:31–36. *Fix:* "its radius, atmospheric column and starlight determine a new
curved-air table, and the same starlight and columns determine the targets for the radiation fits", with "from that
world's own column and starlight" in repairs.tex:112–113 and reach.tex:5–6 if the author takes it.

## Records

**6. availability.tex:79–84; paper/review/README.md:102–111 and 124. MINOR.** *What fails:* the review history ends
with round 17's findings on approved wording "left for the author". The author has since read those five findings and
had them applied (51ea569; `editorial_round17_dispositions.md`, "For the author's decision"), and round 18 followed: the
author's two directions, three light readings by fresh Claude Opus 5.5 subagents, and this closing review. The paper's
account of the five findings is therefore out of date, and `AGENTS.md` asks for the actual review history, with each of
the author's readings recorded as the author's review; the README's history and its row for the author stop at the
same point. *Fix:* at the round's close, a sentence or two after the seventeenth round in Availability naming the
author's reading and application of the five findings, round 18's directions, its light readings and its closing
readings; the same in the README's history and in its row for the author.

**7. introduction.tex:22–23; paper/sources/manifest.json, needham2017lunar. MINOR.** Text added in round 17's
dispositions, after its readers. *What fails:* "the Moon held the volcanic air of its youth, at most about 1 kPa, for
about 70 million years" gives the authors' estimate as a flat duration. Needham and Kring write that the atmosphere "may
have taken ∼70 million years to fully dissipate", and in the text that at a loss rate of 10⁴ g s⁻¹ it "would have
dissipated in ∼70 million years. The actual duration of the atmosphere may exceed this estimate". The manifest records
locators for the 1 kPa figure alone, and no use. *Evidence:* the archived original (sha256 `1ba300da…ee9a`, matching the
manifest), abstract and p. 178. *Fix:* "for an estimated 70 million years"; add the abstract's locator and the
Introduction's use to the record.

## Checked and found sound

**The lakes sentence.**
- For a given contrast of temperature the buoyancy is g·α·ΔT, so at a sixth of Earth's gravity the stratification
  resists a given wind stress about six times more weakly, and Wedderburn and Lake numbers scale the same way. The lake
  model behind the sentence carries gravity in every buoyancy term (`lake.py`, module description), and its own
  write-up gives the sixfold figure, which the paper leaves out.
- No number, result or finding from the ecology branch enters the paper: the oxygen contents, overturn counts, anoxia
  and the sixfold figure stay in Terluna, as round 18's record says the author agreed.
- "Would be among the Earth values to test" uses the paper's definition (introduction.tex:85–89), under which an
  empirical law fitted on Earth and used elsewhere is an Earth value of the fit form.
- "Could" keeps the columns a prospect: the ensemble the paper describes holds no lake or sea column, and the sentence
  claims none.

**The oxygen clause.** "Would drive the exchange of oxygen" claims a flux whose rate the winds and waves set, with no
oxygen content, magnitude or biology; the clause sits inside "Developed in this way, the ensemble could be used to
explore ...", and the Earth-fit condition stays in Next steps, stated once. It agrees with Next steps' "exchange of
gases", oxygen being one of those gases.

**The note on terms.**
- Its text matches the removed Introduction paragraph word for word (`git diff 406549d ffdedfe`), and the check script
  reads it among 14 TeX files.
- Its definition agrees with the abstract's description of the class: nitrogen–oxygen air, water as the principal
  condensable, and surface pressures and temperatures near Earth's that permit liquid water. The note names a physical
  class, Earth included, while the abstract applies the name to the exoplanets and constructed worlds it describes, and
  the Introduction (line 55) and the Conclusion (line 3) qualify the class the same way, "Gaean exoplanets and
  constructed worlds"; the note's "an active water cycle" and "rotation" stand beside the abstract's "liquid water" and
  "day" without conflict. Reach (line 75) uses the class to bound the implementation, as `AGENTS.md` asks: the class
  named once, each code's tested range given separately.
- The note's closing clause, "requires adapting both the component models and the fields exchanged within an
  ensemble", agrees with the Introduction's argument at lines 52–57 and with the couplings in Repairs; read as a
  statement about an ensemble for the class, it holds. The stage-2 reader's option of ending the note at "from Earth's"
  stays with the author.
- The Introduction now opens on the cited studies, whose descriptions rounds 14 and 17 checked; Boutle et al.'s
  Earth-like case carries oxygen (archived original, Sect. 2 and Table 2). "Gaean" first appears in the body at
  introduction.tex:47, after the note, and nothing in the paper points to the definition's old place.

**The five approved-wording fixes.**
- Abstract, "a test of the Earth values that depend on them": the wording of worlds.tex:14–15 (W02), and the four
  departures it names match the four ratios of Worlds.
- Abstract, "they bias its runs that meet their conditions, runs of slowly rotating and tidally locked planets among
  them": the Introduction's wording (lines 89–91). By H23 the Sun clock acts in non-synchronous runs on the default
  solar geometry; by W06 the cover unit biases synchronous runs and the orbit default acts in any run without the fixed
  orbit. Recomputed from W06's formula, the cover rises by +0.228 at 6.1 days (N = 60) and +0.306 at 11.2 days (N = 36),
  as Reach gives them (+0.23, +0.31). "Little or no error at Earth's values" agrees with H23 (none at one day, about 1°
  near Earth's rotation), H07 (0.125 ln 1 = 0) and the orbit default's fraction of a degree on Earth
  (assumptions.tex:126).
- Conclusion, "Comparing runs under each law locates ...": the body did so. N01 locates hail's collisions at
  4–8 m s⁻¹ in 0.02–0.2 g m⁻³ of cloud water at −5 to −16 °C, and graupel's at 1–4 m s⁻¹, in the two windows of G11
  (next.tex:100–109; results.tex:179–187).
- Conclusion, "a procedure for specifying another world": Reach (lines 3–10, W01) gives the procedure step by step, and
  the Conclusion's version follows it, with the gap of finding 5.
- Conclusion, "Run together, ...": "could" keeps the sentence a prospect; finding 4 concerns the coupling it implies.

**Round 17's disposition text, sampled.**
- V10, narrowed: the three cited runs that report a first flash give 32.5, 27–28 and 30–40 minutes (Terluna
  `climate/crm/README.md`:1762 at 186b294), within the paper's 27–40; the median 9.4 C lies inside MacGorman et al.'s
  2.7–39.6 C (line 1765); 0.33% to ground follows from Salinas et al.'s 99.67% in cloud (line 1764).
- N01 and G11 in next.tex:100–109 match their register entries; G10's 2.7 flashes per km² per year follows from 44 a
  second over Earth's area, as the register's calculation states.
- Zahnle and Catling's abstract has the exoplanets "crowd against the extrapolation", which "cluster near the same
  divide, extended to them" keeps; Sergeev et al.'s four GCMs simulating a temperate climate rests on the manifest's
  abstract-depth record, as round 17 checked it.
- Reach's classes for the three defects (two removed by general repairs, one avoided) and the Introduction's "Each team
  removed Earth values that mattered" carry out round 17's evidence findings 12 and 3.

**Numbers in the opening pages.** S15 (142–198 K; 0.61–1.4 kg s⁻¹; 64–148 billion years) stands behind "below 200 K",
"0.6–1.4 kg s⁻¹" and "60 to 150 billion years"; S02 (7.25) and S03 (52 km, 23 times) match; the abstract's at least
20 K, about 6 K and 1.6–2.5 K match G14 (295.5 K against 315.5 K and still warming), G05 (−4.98 K, about −5.9 K
settled) and G01 (+2.30 K, about 2.5 K settled; +1.76 K, about 1.6 K settled), as Results states them.

## Checks made and left undone

Made: the diffs named above; `python3 paper/tools/check.py` (exit 0; 14 TeX files; 96 cited keys of 167; 107 of 109
claims cited; the standing warnings on S01 and V14, uncited, and on the web source of H23 and N02, unchecked offline);
`git show` of the ecology branch's files and of Terluna's benchmark table; `pdftotext` on the archived originals of
Needham and Kring 2017 and Boutle et al. 2017, with the former's hash; reads of `twilight.py` and of the claims and
manifest records named; W06's formula recomputed.

Left undone: no PDF build, so the note's setting on page 1 and the layout after it are unchecked here, and the release
register records no build of ffdedfe yet; no web fetch; no drive file opened; `paper/tools/lint.py` unrun, prose lying
outside this reading; the ecology branch's results unchecked, since the paper keeps them out; Terluna sources beyond the
files and lines named unread.
