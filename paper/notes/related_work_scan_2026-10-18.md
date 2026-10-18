# Related work for the ensemble: a scan of literature and software, 18 October 2026

At the author's request, a scan for projects similar to the ensemble that the paper might compare itself with. The
scope is the modelling ensemble and its methods; the Open Moon itself lies outside it. Five fresh Claude subagents
searched five areas in parallel: GCM frameworks and the Earth values in adapted codes; resolved convection, cloud
and storm physics off Earth; nested and coupled model chains; oceans, waves and coasts off Earth; and tools for
building and checking radiation schemes. Each checked every item on Crossref, NASA ADS, arXiv, a publisher landing
page or the software's repository, and read abstracts and landing pages only. The drafting assistant then resolved
15 of the highest-ranked new DOIs on Crossref and compared every DOI with `references.bib` and with the works the
text cites.

Status marks: **cited** in the text; **bib**, in `references.bib` from the 17 October source search but uncited;
**new**, found by this scan. Nothing here is admitted as a source under G6, and no section has changed.

## 1. The closest matches to the ensemble's links

**Climate to storms, and back.**
- Rafkin, Lora, Soto & Battalio 2022, *Icarus* 373, 114755, doi:10.1016/j.icarus.2021.114755 (**bib**:
  rafkin2022interaction), with Battalio et al. 2022, Part 2, *Icarus* 373, 114623, doi:10.1016/j.icarus.2021.114623
  (**new**). On Titan, the cloud-resolving model TRAMS starts from 44 soundings of the TAM GCM, with its physical
  constants set identical to TAM's, and Part 2 then tunes TAM's convection scheme on the resolved runs. It is the
  one published GCM, cloud-model and GCM loop off Earth, the sequence the paper's next step plans for PlaSim's cloud.
- Song, Yang, Luo, Li & Fu 2022, *ApJ* 934, 149, doi:10.3847/1538-4357/ac7879 (**new**). A 2-D cloud-resolving model
  at 2 km along the day–night great circle of a tidally locked aquaplanet, set beside a 3-D GCM: the closest geometric
  match to the CM1 rings, with a record of where a 2-D model and a GCM agree and where they part.
- Lefèvre, Turbet & Pierrehumbert 2021, *ApJ* 913, 101, doi:10.3847/1538-4357/abf2c1 (**bib**). WRF's core with the
  LMD Generic model's radiation and cloud physics at 1 km over Proxima b's substellar region; its cloud feedback
  comes out much weaker than the GCMs'.
- Sergeev et al. 2020, *ApJ* 894, 84, doi:10.3847/1538-4357/ab8882 (**bib**), and Sergeev et al. 2024, *ApJ* 970, 7,
  doi:10.3847/1538-4357/ad4ecd (**bib**). The Unified Model with a nested 4 km dayside domain, then LFRic on a
  stretched global mesh refined to 4.7 km: two online alternatives to the ensemble's offline slices, from the group
  the paper already cites. With explicit convection the planet came out 5 K colder and 25% drier.

**Climate to seas.**
- Schneck, Detelich, Curcic, Ashton, Hayes & Perron 2026, *JGR Planets* 131, e2025JE009490,
  doi:10.1029/2025JE009490 (**bib**), and Detelich et al. 2026, *JGR Planets* 131, e2026JE009693,
  doi:10.1029/2026JE009693 (**new**). PlanetWaves, adapted from the University of Miami Wave Model, takes gravity, air
  density and the liquid's density, viscosity and surface tension as inputs, and Detelich et al. drive it with ten
  years of the TAM GCM's winds over Titan's lakes. It is the nearest counterpart to the ensemble's GCM-to-SWAN link,
  and its finding that storm winds, which the GCM averages, set the wave climate bears on driving SWAN from the GCM's
  mean stress.
- Rubin et al. 2022, *JGR Planets* 127, e2021JE007162, doi:10.1029/2021JE007162 (**bib**), with its public-domain USGS
  data release, doi:10.5066/P9AA8WKP. SWAN 40.72 inside Delft3D-WAVE at Mars' gravity, recompiled once per air
  density: the same code family and the same one-build-per-density approach. Its runs leave AGROW off.

**One physics at every scale.**
- Spiga & Forget 2009, *JGR* 114, E02009, doi:10.1029/2008JE003242 (**bib**), and the Generic PCM, whose single physics
  package runs on three cores, LMDZ, DYNAMICO and a WRF box (wiki, lmdz-forge.lmd.jussieu.fr/mediawiki/Planets;
  CeCILL v2). This is the other route to consistency across scales: one physics written for every scale, where the
  ensemble adapts separately built codes to one another. The Generic PCM's overview also says, in its developers'
  words, that Earth-tuned parameterizations "can behave very poorly far from the parameter space where they have been
  validated", the paper's fourth form.

## 2. What the field has measured that frames the Earth-values problem

- THAI: Fauchez et al. 2020, *GMD* 13, 707–716, doi:10.5194/gmd-13-707-2020; Turbet et al. 2022 (Part I, dry), *PSJ* 3,
  211, doi:10.3847/PSJ/ac6cf0; Sergeev et al. 2022 (Part II, moist), *PSJ* 3, 212, doi:10.3847/PSJ/ac6cf2 (all
  **new**). Four GCMs on the same TRAPPIST-1e cases spread by 6–7 K dry and 14–24 K moist. THAI measures across models
  what the paper measures inside one: how far Earth-fitted cloud, convection and radiation move a rocky planet's
  climate.
- SAMOSA: Haqq-Misra, Wolf, Fauchez, Shields & Kopparapu 2022, *PSJ* 3, 260, doi:10.3847/PSJ/ac9479 (**new**). The one
  intercomparison found that runs ExoPlaSim itself, against ExoCAM, on 15-day synchronous rotators: cases where the
  convective-cover unit would act, and a ready benchmark for the test of the reach. CUISINES, its umbrella (Sohl et
  al. 2024, *PSJ* 5, 175, doi:10.3847/PSJ/ad5830, **new**), lists no project that couples a GCM to storm or wave models.
- Yang et al. 2016, *ApJ* 826, 222, doi:10.3847/0004-637X/826/2/222 (**new**). Five GCM band codes against SMART and
  LBLRTM on moist columns at 250–360 K: the band codes differ by up to 60 W m⁻² in the shortwave and 10–20 W m⁻² in the
  longwave, in the water bands where PlaSim's calibrations act; its columns are a ready test for the in-house
  reference. Yang et al. 2019, *ApJ* 875, 46, doi:10.3847/1538-4357/ab09f1 (**bib**), measures the same spread in
  3-D with cloud.
- Kopparla et al. 2021, *ApJ* 923, 39, doi:10.3847/1538-4357/ac2d27 (**new**). With THOR, GCM numerical errors vary
  across rotation periods of 0.1–100 days, and the abstract names the assumption that a model credible for a standard
  case stays credible everywhere. The GCM's diffusion and friction settings are a candidate Earth value the paper
  leaves undiscussed.
- Liu, Yang, Zhang & Tan 2023, *ApJ* 944, 45, doi:10.3847/1538-4357/aca965 (**bib**). A cloud-resolving model at
  several gravities; the scanned excerpts say it scales fall speeds by a single factor, (g/g_E)^0.5, where the paper
  scales each particle by its own power. Unconfirmed from the abstract.
- Single-model sweeps along the paper's axes, all **new**: Komacek & Abbot 2019, *ApJ* 871, 245,
  doi:10.3847/1538-4357/aafb33; Yang, Komacek & Abbot 2019, *ApJL* 876, L27, doi:10.3847/2041-8213/ab1d60 (radius and
  gravity); Xiong, Yang & Liu 2022, *GRL* 49, e2022GL099599, doi:10.1029/2022GL099599, which runs PlaSim beside CAM3,
  ExoCAM and SAM from 0.5 to 30 bar.

## 3. Tools and methods for the next steps

**Radiation.**
- ecCKD (Hogan & Matricardi 2022, *JAMES* 14, e2022MS003033, doi:10.1029/2022MS003033; github.com/ecmwf-ifs/ecckd,
  Apache-2.0) and CKDMIP (Hogan & Matricardi 2020, *GMD* 13, 6501–6521, doi:10.5194/gmd-13-6501-2020), both **new**: a
  tool that reduces line-by-line spectra to a k-distribution within a set error, and a protocol that scores the result
  by flux and heating rate at every level. Together they are the reduce-and-check workflow the paper proposes; their
  profiles are Earth's, so the in-house model would have to supply the spectra.
- Exo_k (Leconte 2021, *A&A* 645, A20, doi:10.1051/0004-6361/202039040, **new**; GPL-3.0): builds and bins k-tables
  from high-resolution spectra and writes the Generic PCM's format, the GCM the paper names for its independent check.
- SOCRATES (Edwards & Slingo 1996, *QJRMS* 122, 689–719, doi:10.1002/qj.49712253107; tested off Earth by Amundsen et al.
  2014, *A&A* 564, A59, doi:10.1051/0004-6361/201323169), both **new**. The UM and ROCKE-3D 2.0 run it for non-Earth
  air, and ROCKE-3D 2.0's abstract calls its older radiation "valid only for atmospheres similar to that of modern
  Earth".
- RTE+RRTMGP (Pincus, Mlawer & Delamere 2019, *JAMES* 11, 3074–3089, doi:10.1029/2019MS001621, **new**). RRTMG's
  successor reads its tables at run time, which makes it a natural target for an in-house scheme; its distributed
  tables end at 1,097 hPa, still short of the test world's 1,216 hPa.
- Curved air: Prather & Hsu 2019, *PNAS* 116, 19330–19335, doi:10.1073/pnas.1908198116 (**bib**), find that a round
  Earth intercepts 2.5 W m⁻² more sunlight than a flat one, and their Solar-J code's expanding-shell option matches the
  table's widening term. The pseudo-spherical method the in-house solver uses goes back to Dahlback & Stamnes 1991,
  *PSS* 39, 671–683, doi:10.1016/0032-0633(91)90061-E (**bib**), and Kylling, Stamnes & Tsay 1995, *J. Atmos. Chem.*
  21, 115–150, doi:10.1007/BF00696577 (**new**). The UM already runs pseudo-spherical sunlight (Manners 2024, AIP
  Conf. Proc. 2988, 030002, doi:10.1063/5.0185476; Christie et al. 2022, *MNRAS* 517, 1407–1421,
  doi:10.1093/mnras/stac2763; both **new**).
- Also: libRadtran (Emde et al. 2016, *GMD* 9, 1647–1672, doi:10.5194/gmd-9-1647-2016, **new**), a ready DISORT and
  spherical solver for the planned check; Takahashi et al. 2023, *JMSJ* 101, 39–66, doi:10.2151/jmsj.2023-003 (**new**),
  a line-by-line model and a correlated-k model built from it for planetary air; Ding & Wordsworth 2019, *ApJ* 878,
  117, doi:10.3847/1538-4357/ab204f (**new**), a GCM with line-by-line radiation, the opposite route to a reduced
  scheme; Pincus et al. 2020, *JGR Atmos.* 125, e2020JD033483, doi:10.1029/2020JD033483 (**new**), the spread to
  expect between line-by-line codes.

**Forcing a cloud model and calibrating a GCM against it.**
- Randall & Cripe 1999, *JGR* 104, 24527–24545, doi:10.1029/1999JD900765 (**new**): the standard comparison of ways to
  force single-column and cloud models from large-scale fields. CM1's forcing combines two of its three.
- Superparameterization: Grabowski 2001, *JAS* 58, 978–997, doi:10.1175/1520-0469(2001)058<0978:CCPWTL>2.0.CO;2;
  Khairoutdinov & Randall 2001, *GRL* 28, 3617–3620, doi:10.1029/2001GL013552; Khairoutdinov, Randall & DeMott 2005,
  *JAS* 62, 2136–2154, doi:10.1175/JAS3453.1 (all **new**). 2-D cloud models in every GCM column, coupled both ways:
  the two-way relative of the rings. No superparameterized model of another planet was found.
- Shen et al. 2022, *JAMES* 14, e2021MS002631, doi:10.1029/2021MS002631 (**new**): a public library of LES forced by
  GCMs at any site and climate, the Earth analogue of a cloud-calibration set built from CM1 boxes.
- Couvreux et al. 2021, *JAMES* 13, e2020MS002217, doi:10.1029/2020MS002217, and Hourdin et al. 2021, *JAMES* 13,
  e2020MS002225, doi:10.1029/2020MS002225 (both **new**): calibrating a GCM against LES by history matching.
- Colaïtis et al. 2013, *JGR Planets* 118, 1468–1487, doi:10.1002/jgre.20104 (**new**): Earth's thermal-plume scheme
  carried to Mars and refitted against LES, the same finding of Earth tuning by comparison with resolved runs.
- Daleu et al. 2015, *JAMES* 7, 1576–1601, doi:10.1002/2015MS000468 (**new**): weak-temperature-gradient and
  damped-gravity-wave coupling, the main alternative to imposing the GCM's vertical wind.
- COAWST (Warner et al. 2010, *Ocean Modelling* 35, 230–244, doi:10.1016/j.ocemod.2010.07.010, **new**;
  github.com/DOI-USGS/COAWST, which bundles SWAN 41.51A): the reference coupling of WRF to SWAN on Earth, and a check on
  the ensemble's conversion of stress to wind.

## 4. Citations the paper needs for what it already describes

- The two flash-rate laws Results describes: Price & Rind 1992, *JGR* 97, 9919–9933, doi:10.1029/92JD00719 (cloud-top
  height), and McCaul et al. 2009, *Wea. Forecasting* 24, 709–729, doi:10.1175/2008WAF2222152.1 (graupel flux and ice
  water path). Both **new**; Braam 2022 and Sergeev 2025, which use them, are cited.
- The correlated-k method behind the reference's emulation: Lacis & Oinas 1991, *JGR* 96, 9027–9063,
  doi:10.1029/90JD01945 (**new**).
- The pseudo-spherical two-stream the in-house solver uses: Dahlback & Stamnes 1991 (**bib**) and Kylling et al. 1995
  (**new**).
- The current sources for two of the reference's inputs: Mlawer et al. 2023, *JQSRT* 306, 108645,
  doi:10.1016/j.jqsrt.2023.108645 (**bib**: mlawer2023inclusion), for MT_CKD, and Karman et al. 2019, *Icarus* 328,
  160–175, doi:10.1016/j.icarus.2019.02.034 (**new**), for collision-induced absorption.

## 5. Points the scans raised about the text, to check

- `verification.tex`, "Gravity is the parameter of a sea that stays fixed in a laboratory on Earth": surface-wave
  experiments in a centrifuge and on parabolic flights varied gravity (Cazaubiel et al. 2019, *PRL* 123, 244501,
  doi:10.1103/PhysRevLett.123.244501), though for mechanically forced waves; the sentence holds if scoped to wind
  waves.
- `assumptions.tex`, the SWAN knee and "the ancient seas of Mars among them": the knee acts only with AGROW's linear
  input on, and Rubin et al.'s Mars runs had it off; Banfield et al.'s configuration is unchecked.
- A global run at 6 km on a Moon-sized world needs about 1.05 million columns, about 7% of Earth's (the coupling
  scan's arithmetic). The choice of offline slices over a global storm-resolving run may deserve a sentence.
- Matched constants across a model chain have precedents (TAM and TRAMS; the LMD mesoscale model), so the novelty the
  paper claims is safest on the classification of Earth values and the split between general repairs and per-world
  calibrations, as `literature.md` already scopes it.
- Published ExoPlaSim ensembles (SAMOSA; Paradise et al. 2021, *Icarus* 358, 114301, doi:10.1016/j.icarus.2020.114301;
  the ThousandWorlds benchmark, arXiv:2606.18338, a preprint, whose 1,117 ExoPlaSim runs feed climate emulators) span
  the rotations and columns where the Sun clock, the cover unit and the Earth-column fits act. That gives the defects a
  concrete audience, once those runs' configurations are checked.

## 6. Software

| Software | Where | Licence | Note |
|---|---|---|---|
| PlanetWaves | github.com/Cornell-MIT/PlanetWaves; Zenodo doi:10.5281/zenodo.18906357 | CC BY 4.0 (Zenodo) | MATLAB; ships TAM winds for two Titan lakes |
| UMWM | github.com/umwm/umwm | MIT | PlanetWaves' parent; computes stress from the wave field |
| Generic PCM | svn.lmd.jussieu.fr/Planeto/trunk | CeCILL v2 | One physics on LMDZ, DYNAMICO and WRF cores |
| LFRic | github.com/MetOffice/lfric_core, lfric_apps | BSD-3-Clause | The UM's successor; planetary tests in Sergeev et al. 2023, *GMD* 16, 5601–5626 |
| Isca | github.com/ExeClim/Isca | GPL-3.0 | Planet as a set of parameters (Vallis et al. 2018, **bib**) |
| ecCKD, ecRad | github.com/ecmwf-ifs | Apache-2.0 | k-distribution generator and solver |
| Exo_k | gitlab.in2p3.fr/LAB/whiplash-public/exo_k; PyPI | GPL-3.0 | k-tables from spectra |
| RTE+RRTMGP | github.com/earth-system-radiation | BSD-3-Clause | Tables read at run time |
| ExoRT | github.com/storyofthewolf/ExoRT | Author's own licence | ExoCAM's radiation; no O2 absorption listed |
| HELIOS-K | github.com/exoclime/HELIOS-K | GPL-3.0 | GPU opacity calculator |
| libRadtran | libradtran.org | GPL | DISORT, pseudo-spherical and Monte Carlo solvers |
| COAWST | github.com/DOI-USGS/COAWST | Public domain (CC0) | WRF, ROMS and SWAN 41.51A coupled |
| Canoe/SNAP | github.com/chengcli/canoe | MIT | Cloud-resolving model for planetary air, so far giant planets |
| ThousandWorlds | github.com/edstevenson/ThousandWorlds | MIT (code), CC BY 4.0 (data) | Pooled exoplanet GCM runs |

## 7. Other verified items, lower priority

- Waves and oceans: Lorenz & Hayes 2012, doi:10.1016/j.icarus.2012.03.002 (**bib**); Lorenz et al. 2005, wind-tunnel
  wave growth at 15–1000 mbar, doi:10.1016/j.icarus.2004.11.019 (**new**); Hayes et al. 2013 and Ghafoor et al. 2000
  (**bib**); Tokano & Lorenz 2015, doi:10.1002/2014JE004751, and Vincent et al. 2018, doi:10.1016/j.icarus.2017.12.018,
  ocean and tide models on Titan (**new**); Palermo et al. 2024, wave erosion of Titan's coasts,
  doi:10.1126/sciadv.adn4192 (**new**); Yang, Ji & Zeng 2020, sea-ice drift, doi:10.1038/s41550-019-0883-z (**new**);
  Del Genio et al. 2019, a dynamic ocean in ROCKE-3D, doi:10.1089/ast.2017.1760 (**bib**); Blackledge et al. 2020,
  tides on other Earths, doi:10.1029/2019GL085746 (**new**); Studholme et al. 2021, waves in aquaplanet oceans,
  doi:10.1029/2020MS002202 (**new**).
- Storms and lightning: Seeley & Wordsworth 2021 (**bib**) and 2023, doi:10.3847/PSJ/acb0cb (**new**); Yair et al. 1995
  (**bib**) and 1998, doi:10.1029/98JD00310; Romps 2019, doi:10.1029/2019GL085748; Yang et al. 2026, bin microphysics
  across rotation in CAM6, doi:10.3847/1538-4357/ae40b5; Spiga et al. 2017, Martian snowstorms,
  doi:10.1038/ngeo3008; Komacek, Chavas & Abbot 2020 and Garcia et al. 2024, tropical cyclones on exoplanets (all
  **new** unless marked).
- Chains and frameworks: Charnay et al. 2015, Titan storms setting dune orientation, doi:10.1038/ngeo2406; Kuang,
  Blossey & Bretherton 2005, DARE, doi:10.1029/2004GL021024; Lebonnois et al. 2010, a Venus GCM from an Earth core with
  temperature-dependent specific heat, doi:10.1029/2009JE003458; Isca, Vallis et al. 2018 (**bib**); Forget & Leconte
  2014 (**bib**); MRAMS and the Jezero simulations of Newman et al. 2021 (all **new** unless marked).

## 8. Limits

Each scan exhausted its web-search budget near the end and finished on Crossref, arXiv and repository pages. Wiley,
ScienceDirect, AMS and IOP pages often blocked direct reading, so details the scans marked as taken from search
excerpts (Liu et al.'s fall-speed factor, libRadtran's solver list, some model names) await a reading of the paper
itself. No full paper was read; three PDFs that the fetch tool cached outside the repository were left unread.
