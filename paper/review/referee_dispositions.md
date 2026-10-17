# Dispositions of the technical referees' findings

Disposer: Claude Opus 5.5, the drafting assistant. Date: 2026-10-17. The reports are
`referee_technical_part1.md` (findings 1–44) and `referee_technical_part2.md` (F1–F50), committed unedited in
33eeb20 before any change. Every finding was read against its cited evidence; where a disposition rests on a
fresh check, the check is named. "Accepted" means the text, the claims register and, where named, the notes
were revised as the finding asked or to the same effect.

## Part 1: introduction, regime, hidden Earth, repairs

| # | Finding | Disposition |
|---|---|---|
| 1 | Convective similarity (S12) stated as fact | Accepted. The regime text now says the dry dynamics stretch sixfold, the microphysics and radiation keep their scales, and the gravity pair failed to convect; Table 1's row is "Grid for deep convection" with the caption calling it nominal |
| 2 | H30 misattributed the 58% to the ledger | Accepted. The sky model's 114 channels carry the 58%; the ledger's first channels put near-infrared sunlight too high (19.0 against 10.7 W/m² at 66–85 km), and the two 20-year curved-air tests ran on them |
| 3 | Point discharge said to be on | Accepted. It ran in one window and is off in the lunar runs |
| 4 | Identity exceptions incomplete | Accepted. The repairs opening names the 400 ppm CO₂ default, NSSL's 9.81 against 9.8, SWAN's identity only at 9.80665 set by input, the water-scaling guard and the scope of the beta-plane change and ice cap; Table 3 annotates each default |
| 5 | Classes contradicting the paper's rule | Accepted. Curved air and twilight: "Method, lunar table"; gas bands: Calibration; soil, air, SWAN density: Setting; leakage: Capability |
| 6 | "Two classes" against seven in the tables | Accepted. The introduction and the repairs opening name the other kinds (settings, capabilities, a bound, a mitigation, avoidances); both captions list every class |
| 7 | S06 cells against area | Accepted. "759 of the GCM's 2,048 cells, 40% of its surface" |
| 8 | Intro "seas and lakes over 28%" | Accepted. "seas over 28% of the surface with rain-fed lakes above them" |
| 9 | "About 1° on Earth" | Accepted. About 1° for a rotation near Earth's set away from one day; none at ExoPlaSim's default |
| 10 | Thread race and lowest-level artefact not shown Earth-hidden | Accepted. The paragraph (now "Defects in the released codes") counts three hidden by Earth and two whose tie to Earth's values is unknown; the defect log records the paper's reclassification of A3, A7 and A8 |
| 11 | "Every instance" | Accepted. Table 2 is scoped to the paths the lunar runs use, with the defect log for the rest; a flash-reach row (A8) is added |
| 12 | Gravity in more than four places | Accepted. "four places on the lunar cases' paths, and in several schemes those cases leave unselected" |
| 13 | WRF-ELEC conduction "off by default" | Accepted. "carries no conduction of charge through clear air, its screening option acting only at cloud edges"; Table 2 row "None in clear air", state Capability |
| 14 | Ledger baseline and "nearly all" | Accepted. "Against the same air in flat layers, with a pseudo-spherical direct beam for the sunlight"; the widening takes 6.5 and the curved light gives back 0.7 |
| 15 | Channel tolerance and beam channels | Accepted |
| 16 | Chronology of the 8.1-point shortfall | Accepted. "When the Sun-clock and orbit faults were found ... 7.7–8.2 points short; with the repair ..." |
| 17 | HITRAN edition | Accepted. "HITRAN lines as served in September 2026 (HITRAN2020 or a later edition)" in the introduction, repairs and claims |
| 18 | Table 3 Sun | Accepted. 1,198 W/m² for the corrected rings, 1,173.5 for the boxes, at equinox |
| 19 | H15 run identity | Accepted. "the first design run, with 25% seas under the undimmed shield ... in model year 12" |
| 20 | "becomes right for the Moon" | Accepted. "can be made right for the Moon as far as its lunar value is known" |
| 21 | "three thresholds" | Accepted. "two thresholds and a time step" |
| 22 | S04 sunlight | Accepted. "still lies above the Moon's geometric shadow"; the design-profile share was computed here (0.45; the referee gave 0.44) and added to `regime_calc.py` |
| 23 | "otherwise Earth's own" | Accepted. "close to Earth's own" |
| 24 | Prior ports | Accepted. They generalised "the gases, the star, the planet's constants and its calendar" |
| 25 | "Every change ... its switch" | Accepted. "Every source change ... with its switch where it has one, its default and the checks made on it" |
| 26 | "reproducibility" | Accepted. "identity" |
| 27 | "radiation every model must reproduce" | Accepted. "the radiation the GCM is calibrated to and CM1's is checked against" |
| 28 | Horizon air mass methods | Accepted. Table 1 gives Chapman's 34.5 and 7.2 for both; the text names the straight-ray method for 7.1 and 13.5 |
| 29 | A box's Sun | Accepted. "each ring column with its own Sun (a box takes one)" |
| 30 | SWAN's u* | Accepted. "to within a few per cent" |
| 31 | 8 s sub-step | Accepted |
| 32 | Table 2 WRF-ELEC effect | Accepted |
| 33 | Damping and mixing length form | Accepted. Own row, form Constant |
| 34 | Cloud water and gas-band forms | Accepted in part. Cloud water is now a Constant; the gas omission and liquid-only optics stay under the fourth form, renamed "fits and simplifications used beyond their range" (labelled Fit in Table 2) |
| 35 | H19 logic and layer | Accepted |
| 36 | H07 "rotation and orbit" | Accepted. "rotation counted in its 360-day year" |
| 37 | "checks found them" | Accepted. "some by checks ... and some in the course of the work" |
| 38 | H31 scope | Accepted. "in the 45° N rings" |
| 39 | H29 "at a discharge" | Accepted. "at a step's first discharge" |
| 40 | "Each absence showed in a run" | Accepted. "Two of these absences showed in runs" |
| 41 | S05 range and units | Accepted. 1.02–1.22 atm (A28_corrected_970, year 19); Table 1 keeps bar, labelled |
| 42 | Screening in the lunar setting | Accepted. "screening available, off" |
| 43 | Missing rows | Accepted. Beta plane and land and water along the domain added to Table 3 |
| 44 | "byte for byte" | Accepted. The ExoPlaSim copy and the Fortran of the eight lunar CM1 builds; older builds carry earlier states |

## Part 2: verification, results, reach, next work, conclusions, abstract, availability

| # | Finding | Disposition |
|---|---|---|
| F1 | 31.1% wrong | Accepted. "as the line-by-line model's air does"; `notes/verification_record.md` corrected |
| F2 | Total cloud reported as high cloud | Accepted. "cloud over 38% of the sky in place of 20%, most of the gain high"; `notes/exoplasim.md` corrected |
| F3 | Deciding charging measurement | Accepted. The sign rimed ice takes at 4–8 m/s in 0.02–0.2 g/m³ at −5 to −16 °C; `notes/electrification.md` corrected in three places |
| F4 | Impact speeds; "only measurement" | Accepted. The laws disagree on the sign in little cloud water; "measurement or theory"; Table 5 "Charging in little cloud water" |
| F5 | Identity against the released model | Accepted. "the same build without the patch"; one of five compares against the release |
| F6 | Missing identity runs | Accepted. Patches 07–09 off and the move into the twilight copy added (verification, Table 4, next work) |
| F7 | "every deployed source" | Accepted. ExoPlaSim copy and eight lunar CM1 builds; `models/cm1/builds.json` notes `earth_g_omp` |
| F8 | Sun-clock range | Accepted. N floored at 12, so 33° above 20 days; checked against `__init__.py` arithmetic in `regime_calc.py` (`exoplasim_slow_rotators`); note corrected (16° for 12–20 days) |
| F9 | Slow rotators untested | Accepted. "should need ... though none has been run", with the model-day drift (64 d: 69.8 against 77.6 d) |
| F10 | "soil to 80 cm" | Accepted. "soil layers 5–80 cm, 1.55 m deep" |
| F11 | "Each ... default reproduces" | Accepted. "Most" in the conclusions and abstract |
| F12 | "carries to any world" | Accepted. "within the limits Table 5 sets"; abstract "within stated limits" |
| F13 | Cleared suspects' conditions | Accepted. At the equatorial crossing on pre-correction forcing; the 45° N land test has yet to run |
| F14 | Attribution by elimination | Accepted. "a degree or two, is attributed by elimination" |
| F15 | 180 against 129 mm | Accepted. 129 mm from the forcing GCM, 180 mm corrected |
| F16 | Main electrified run's conditions | Accepted. Pre-correction forcing; ground strikes an upper bound; hail moved out of the Earth-like list |
| F17 | Window means against settled values | Accepted. 2.3 K (about 2.5 settled) and 1.8 K (about 1.6 settled), on run A |
| F18 | Cloud settings settled | Accepted. About +2.2, −5.9 and −3.5 K; "up to about 6 K" in the conclusions and next work |
| F19 | Figure baselines and the longwave bar | Accepted. The caption names the four baselines and the extrapolated balance; the longwave bar is redrawn grey with the tests (`extract.py` kind `test`) |
| F20 | Gas-band cloud loss | Accepted. High deck 16% to 12%, first-year 3.5 of 5.4 W/m², the cloud-free column's 0.57 K as the basis for "mostly" |
| F21 | 3.7 K range's conditions | Accepted |
| F22 | Abstract's 3.7 K | Accepted. "with the GCM's sideways transport imposed" |
| F23 | "layer by layer ... one design column" | Accepted. "on the design case's columns" |
| F24 | Mars below 1 bar | Accepted in part. "at its 1 bar level ... though ground standing below that level takes RRTMG past its tables"; the Martian topography figures are general knowledge outside the record and are left out |
| F25 | "any O₂" | Accepted. "O₂ and CO₂ near the design air's, refitted otherwise" |
| F26 | "other shields" | Accepted. Other dimmings as they stand; 1.0 atm (unrun) and other UV-blocking shields after refitting; UV-passing shields need ozone |
| F27 | SWAN's one constant | Accepted. "in the configuration used" |
| F28 | Regime figure legend | Accepted. Caption rewritten; the three slow rotators moved from `figures.py` into `worlds.json` |
| F29 | Gap figure years and share | Accepted. Years 10–19; 2.2 of 5.9 K, 37% |
| F30 | Snow exponent; 85% | Accepted. Snow takes the drops' exponent; 85% in boxes, 57–73% in rings (claim N03) |
| F31 | Prediction stated as result | Accepted. "could move ... up to about 6 K" |
| F32 | Rain and cloud direction | Accepted. "would change with it" |
| F33 | Microphysics similarity | Accepted. The pair "would measure how far the scaled microphysics departs from similarity" |
| F34 | Conclusions' "exact on Earth" | Accepted. "held on Earth"; fits named as fits; the clock exact at a one-day rotation; the tilt added to what the Moon moves |
| F35 | 1.1% ground strikes | Accepted. With the rule on, against 0.33% published; median charge per flash |
| F36 | "below 1,054 hPa" | Accepted. "past 1,053.63 hPa" |
| F37 | SWAN identity | Accepted. "with the wind-input patch ... at standard gravity" |
| F38 | Reflectivity | Accepted. "at every half hour" |
| F39 | "uncalibrated" | Accepted. "before its water recalibration" |
| F40 | Conductivity and ledger conditions | Accepted |
| F41 | Thread race | Accepted. "remains unlocated", "placed by elimination in its own loops" |
| F42 | SWASH three gravities | Accepted |
| F43 | "storms stand ... taller" | Accepted. The isotherms stand five to six times higher |
| F44 | Absorber paths against column | Accepted, in the text and on the regime figure ("Earth's column") |
| F45 | "Four limits" | Accepted. "Four limits bound most of the reach"; Table 5 adds the narrower ones |
| F46 | "only" | Accepted |
| F47 | Release register | Accepted. "will be recorded" |
| F48 | SWAN licence | Accepted |
| F49 | Unclaimed numbers | Accepted. Claims V15 (0.19 K) and G13 (306.8–307.1 K) added |
| F50 | 11.5 K with ice | Accepted. "with the ice optics" in the abstract, results and conclusions |

## The literature pass's flags (`notes/literature.md`)

| Flag | Disposition |
|---|---|
| Breaker index 0.73 is Battjes and Stive (1985), not Battjes and Janssen (1978) | Accepted; cited `battjes1985calibration` |
| PlaSim's longwave continuum is its own, fitted by the first calibration to the outgoing flux | Accepted; H17 rephrased |
| Morrison's breakup came in version 2.1 after Verlinde and Cotton | Accepted; verified in `morrison.F` line 27 and cited `verlinde1993fitting` |
| The convective cover is Slingo and Slingo (1991) by PlaSim's manual | Accepted; cited with the manual |
| The factor 35 traces to Rodgers (1967) through Lacis and Hansen | Accepted; both cited at the formula |
| ExoCAM's model paper | Accepted; `wolf2022exocam` added |
