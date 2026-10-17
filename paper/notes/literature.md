# Literature rooting

Stage 2 of the paper's build: which published sources root which statements, what each source
establishes and what it leaves open, where this paper's own work appears to be first, and the search
record. Written 2026-10-17. Per-source records are in `paper/sources/manifest.json`; the bibliography
is `paper/references.bib`.

The G6 position stated plainly: **no source is admitted.** 70 of the 142 sources in the
bibliography have a legal local original archived in `paper/sources/originals/` (or a pinned upstream
archive) and are DEFERRED, because none has been read in full with its appendices and reference list.
72 are BLOCKED: no legal local original could be obtained from this machine. Of the 50 sources the
draft cites, 23 have an archived original and 27 are BLOCKED. Reading depth for the 50 cited sources is:

- claim-locators for 23: the passage behind each claim was read in an archived original or record;
- abstract-only for 24;
- not read for 3: zijlema2011swash, kiehl1996description (its PlaSim use is rooted in PlaSim's manual)
  and trenberth2005trends.

## How the sources were checked

- **Bibliographic verification.** Every candidate DOI was resolved at `api.crossref.org/works/<doi>`.
  Entries without a DOI were found with Crossref's bibliographic search and checked by DOI. The two
  NCAR technical notes were checked at DataCite. Software and manuals were checked against their
  release records: the PyPI release, the archive README, the GitHub commit and the PDF title page.
  The 60 sources added by the topic searches were checked the same way. The bib was built from those
  records, with sentence-case titles and brace-protected proper nouns. It passes a BibTeX `\nocite{*}`
  test.
- **Open access.**
  - Status comes from OpenAlex (`open_access`, `locations`), with Semantic Scholar for the closed
    remainder.
  - Downloads used curl's default user agent and went only to publisher open-access copies, arXiv,
    HAL, institutional and agency repositories, author pages and project sites.
  - No bot challenge was bypassed and no shadow library was used.
  - Each download was checked for a `%PDF` header, an `%%EOF` trailer and `qpdf --check`. Two
    truncated transfers (HITRAN2020 and Mayne 2019, both from HAL) were caught and repeated.
  - Nine PDFs fetched by delegated search agents were adopted with their source URLs recorded: five
    AMS scans and four author pages whose TLS chains this machine rejects.
- **Barriers met.** These hosts answered scripted requests with 403 or a challenge:
  - AMS (`journals.ametsoc.org`, CloudFront);
  - Wiley/AGU/RMetS (Cloudflare);
  - ScienceDirect, aanda.org, PNAS, the Royal Society, Europe PMC and eScholarship;
  - NCAR OpenSky (Turnstile) and the NOAA Institutional Repository;
  - IOP, after a few requests (Radware).

  Many of those articles are free to read in a browser, so a person can complete most BLOCKED items
  by hand.
- **Reading and quotes.** Every quote in the manifest is machine-checked against the text it cites
  (`quote_check`), after whitespace and typography normalisation: the archived text layer, the OCR of
  a scanned original, the stored Crossref/OpenAlex abstract, or the pinned source code.
  - Scanned equations (Lacis and Hansen 1974; Mitchell 1996) were read from page images.
  - Locators reported by the three search agents are labelled with the agent in the manifest. They
    were spot-checked where an archived text exists.

## Corrections to the candidate list

| Candidate as given | Verified record |
|---|---|
| Paradise et al. 2022, doi:10.1093/mnras/stab3804 | doi:10.1093/mnras/**stac172**, MNRAS 511(3), 3272–3303 (stab3804 is a radio-source paper) |
| Mayne et al. 2019, A&A 623, A79 | **ApJ 871(1), 56**, doi:10.3847/1538-4357/aaf6e9; A&A 623 A79 is Combes et al. 2019 |
| Mayne et al. 2014, A&A 561, A1 | correct; published online 2013 |
| Chapman 1931, Proc. Phys. Soc. 43, 483 | correct as **Part II, Grazing incidence**, 483–501, doi:10.1088/0959-5309/43/5/302 (Part I is 43, 26–45) |
| Lalande et al. 2002, C. R. Physique 3, 1375, "Leader properties…" | title **"Observations and modeling of lightning leaders"**, Lalande, Bondiou-Clergerie, Bacchiega, Gallimberti, 1375–1392, doi:10.1016/S1631-0705(02)01413-5 |
| Kiehl et al. 1996, doi:10.5065/D6FF3Q99 | correct, but a **DataCite** DOI (Crossref 404); NCAR/TN-420+STR |
| Collins et al. 2004, CAM3 note | DataCite doi:10.5065/D63N21CH, NCAR/TN-464+STR (DataCite's creator list may omit J. J. Hack) |
| Del Genio et al. 2019, "verify which" | the slow-rotator albedos are in **ApJ 884, 75** ("Albedos, equilibrium temperatures…"), Table 1 rows 32–37, not the Astrobiology Proxima b paper |
| Battjes and Janssen 1978, "Coastal Eng. Proc." | doi:10.9753/icce.v16.32 (ICCE, open access); also ASCE doi:10.1061/9780872621909.034, pp. 569–587 |
| Salameh et al. 2018 | correct; published online 2017 |
| Kristjánsson, Edwards and Mitchell 2000 as source of RRTMG `reicalc` | CM1/WRF RRTMG says "following Kristjansson and Mitchell" (module_ra_rrtmg_sw.F line 10947), and the 2000 abstract confirms "a temperature dependency of ice crystal size"; the identity of the tabulated values was not checked |
| Wolf and Toon 2015 as ExoCAM | a lineage reference; Wolf et al. 2022 (PSJ 3, 7) is ExoCAM's description and calls the 2015 model "a legacy version" (agent A) |
| Zdunkowski, Welch and Korb 1980 | authors, journal, volume and first page confirmed only through the reference list of Way et al. 2017, which also names it for SOCRATES's shortwave PIFM; the title was not verifiable, so it is **excluded from the bib** |
| "Yang et al. 2023" (CRM 27–41% vs CAM3/ExoCAM 82–97%) | **Yang, J., Zhang, Y., Fu, Z., Yan, M., Song, X., Wei, M., Liu, J., Ding, F., Tan, Z. 2023, Nature Astronomy 7(9), 1070–1080**, doi:10.1038/s41550-023-02015-8 |
| "Yang et al. 2019" five-GCM ocean world | Yang, Leconte, Wolf, Merlis, Koll, Forget, Abbot 2019, ApJ 875(1), 46, doi:10.3847/1538-4357/ab09f1 |
| Iacono et al. 2008 "D13103" | confirmed by the reference list of Borchert et al. 2019 (Crossref stores 2008JD009944) |
| Mansell et al. 2005 "D12101" | confirmed by WRF-ELEC's README |

Keys follow the main session's names where it already cited them: fraedrich2005planet,
way2017resolving, fierro2013implementation, booij1999third, morrison2005new, iacono2008radiative,
kiehl1996description.

## The need

**What the sources root.** Earth models have been carried to other worlds many times, and the
porting papers say in their own words that the models carried Earth inside them.

- *PlanetWRF.* WRF "was written to be exclusively applicable to the Earth"; the port redefined model
  seconds as 1/86400 of a planetary rotation and replaced the calendar (richardson2007planetwrf,
  Sect. 3, p. 3; Sect. 3.3, p. 4).
- *TitanWRF.* The port removed "hardwired 'Earth' settings from parameterizations of physical
  processes" (newman2011stratospheric, Sect. 2.3, p. 637).
- *WRF on Mars.* Spiga and Forget (2009) converted the constants, replaced the calendar and defined
  "1 h … as 1/24 sol" (spiga2009new, Sect. 2.1).
- *ROCKE-3D.*
  - Version 1.0 found "implicit (hardwired) constants appropriate to the lengths of modern Earth day
    and year" and solar assumptions "still hard-coded" (way2017resolving, arXiv pp. 10, 15).
  - Version 2.0 removes three "Earth-centric parameterizations", including a 50-hPa cloud-top cap
    (tsigaridis2025rocke3d, Sect. 3.3, p. 5834, agent A).
- *THOR 2.0* names the general problem: "planet-specific tunings are often built into the code and
  can be difficult to find and generalize" (deitrick2020thor, Sect. 1, agent A).
- *Generic PCM / LMD.* Simplifications "initially done for the Earth's case" must be questioned
  (forget2014possible, Sect. 4.2, agent A).
- *ExoPlaSim.* Its own paper concedes PlaSim's solar day "poses a challenge for modeling planets
  other than Earth" and that its near-infrared water absorptivity "is tuned to a solar spectrum"
  (paradise2022exoplasim, Sect. 2.1 p. 2; Sect. 5 p. 24).

**What they leave open.** Each paper reports the repairs its own world required. None classifies the
hidden Earth, separates repairs that hold anywhere from calibrations, or tests a world that moves
gravity, column mass, scale height and day length together. The five-form taxonomy and the
general/calibration distinction appear to be this paper's.

**The scenario.** The scenario rests on the author's own project record (goldman2026terluna, commit
186b294, present in the local checkout's history). The models are the pinned releases:

- ExoPlaSim 3.4.2 (paradise2025exoplasim; PyPI sdist sha256 fae502a9…);
- CM1 r22.0 (bryan2026cm1; README dated 21 September 2026);
- WRF-ELEC at MicroTed/wrf4-elec e43041b (mansell2026wrfelec);
- SWAN 41.51 and SWASH 12.01 (swan4151user, swan4151tech, swash1201user).

## The limitations and defects (the five forms)

### 1. Constants written into the code

These are primary technical records: the code itself and its documentation.

- **CM1 r22.0 (bryan2026cm1).**
  - Morrison fall-speed laws "V=AD^B" with AR = 841.99667, BR = 0.8 etc. (morrison.F lines
    397–413).
  - An 850-hPa reference density for the (ρ_su/ρ)^0.54 correction (lines 437, 1836).
  - Rain's mean diameter is bounded at 2.8 mm (`LAMMINR = 1./2800.E-6`, line 492).
  - Breakup begins at a 0.3-mm cutoff (line 495), "following Verlinde and Cotton (1993)" (line 27).
- **WRF-ELEC (mansell2026wrfelec).**
  - Breakdown field `ebrkdp = 284.e3*db/rho00`, then `Max(50.e3, Min(ebrkdp, 180.0e3))` for the
    default profile (module_discharge_msz.F lines ~667–674).
  - The README attributes the profiles to "Dwyer (2003, GRL)" (lines 115–117).
  - NSSL_EINTERNAL = 200 V/m and NSSL_TGRND = 266.16 K (−7 °C), the CG temperature threshold.
- **SWAN 41.51.**
  - `[grav] = 9.81` default (swan4151user).
  - Air density 1.28 kg m⁻³ in `swmod1.ftn` line 2634.
  - Wu drag as the default (`IDRAG = 1`, swanmain.ftn line 1370, and the user manual's GEN3 DRAG
    "This option is the default").
- **PlaSim (lunkeit2012plasim, p. 22, Eq. 3.28).** The slant factor M = 35/√(1224µ₀²+1) "after
  Rodgers (1967)".
  - Lacis and Hansen (1974, p. 122, Eq. 12) give the same factor, "accounting for the slant path and
    refraction", and attribute it to Rodgers' 1967 MIT report (Rept. A2).
  - Li and Shibata (2006) say most GCMs use it, that "it is not clear how (8) was derived", and that
    it overestimates the path factor for 10 < 1/µ₀ < 120 (p. 1367–1368).

### 2. Units of time

PlaSim's manual gives the convective cover as c = 0.245 + 0.125 ln P_c, 0.05 ≤ c ≤ 0.8, with P_c in
mm/d. It introduces the formula as "following the ideas of Slingo and Slingo (1991)"
(lunkeit2012plasim, Sect. 3.4.6, p. 35, Eq. 3.96).

That PlaSim's code counts the day as the model's solar day is a code-level finding. Paradise et al.
(2022) report removing the solar day from unit conversions, replacing it with 86400 s
(paradise2022exoplasim, Sect. 2.1, p. 2). The cloud formula's 'per day' is therefore a residue that
their pass did not reach, or that the code still defines through the model day; the paper should say
which.

### 3. Geometry

- **Flat sunlit-only radiation.**
  - Prather and Hsu (2019, PNAS; prather2019round) show that climate models stop solar heating at a
    zenith angle of 90°, miss twilight heating, and that a spherical column holds mass larger by
    1 + 4H/R. Read by agent C via PMC; BLOCKED here.
  - Li and Shibata (2006) give a rigorous layer-by-layer path. They find the effect small for Earth
    "since the thickness of the atmosphere is very small in comparison with the radius of the earth"
    (p. 1372). That is a limiting finding which the lunar H/R ≈ 0.03 reverses.
- **Chapman function at the horizon.** Ch(X, π/2) = X e^X K₁(X) (vasylyev2021accurate, p. 2,
  Eq. 5). With the K₁ asymptotic on p. 9, the leading term is √(πX/2) with a (1 + 3/(8X)) correction,
  X = R/H. Assumptions: exponential atmosphere, constant T and g, no refraction.
  - Agent C's evaluation: 34.8 for Earth (reproducing PlaSim's 35) and 7.3 for the Moon.
  - Chapman (1931) Part II is the original. BLOCKED; abstract only.
- **Deep atmospheres beyond the terminator.**
  - On Titan, dayside-only averaging is "a poor approximation" (lebonnois1999actinic, p. 22027).
  - The plane-parallel limit falls to about 80° for Mars and 65° for Titan (vincendon2010spherical,
    Sect. 1).
  - Pseudo-spherical transfer (Dahlback and Stamnes 1991) is BLOCKED and unread, so L10 is not
    rooted.
- **Constant g and thin shell.**
  - White et al. (2005) define the hydrostatic primitive equations' shallow approximation as
    "replacing r by a" and "neglecting vertical … variation of g", "justified by the shallowness of
    the atmosphere in relation to a" (white2005consistent, accepted manuscript Sect. 3(b), p. 10).
  - Mayne et al. (2014) adopt that nomenclature and run Full, Deep (constant g) and Shallow
    equation sets (mayne2014unified, Sect. 2).
  - Mayne et al. (2019) place the breakdown where the scale height "becomes significant compared to
    the assumed total planetary radius" (Sect. 1). Agent A adds that the primitive and full
    equations "differ significantly … where zU/Rp ∼ 20%" (Sect. 3.2.2).
  - Borchert et al. (2019) give Earth practice: the shallow form is "likely a very good
    approximation" below about 70–100 km.
  - Thomson and Vallis (2019) show that dry hydrostatic dynamics are invariant to g except through a
    vertical rescaling, an invariance "broken … by having a non-shallow atmosphere".

### 4. Fits beyond their range

- **Lacis and Hansen water absorptivity.** A_wv(y) = 2.9y/[(1+141.5y)^0.635 + 5.925y]
  "fits Yamamoto's absorption curve within ≲1% for 10⁻² ≲ y ≲ 10 cm" (lacis1974parameterization,
  Sect. 4, pp. 126–127, Eq. 21).
  - That is the fit's stated range. The asymptote 2.9/5.925 ≈ 0.49 is our arithmetic and supports
    the draft's "levels off toward half the sunlight".
  - PlaSim uses it unchanged (manual Eq. 3.30), and Paradise et al. note it is "tuned to a solar
    spectrum".
- **Sasamori broadband longwave.** PlaSim takes its H₂O, CO₂ and O₃ transmissivities "from Sasamori
  (1968)" (manual p. 26, Eq. 3.52) and adds a water-vapour continuum of its own (Eq. 3.55). The
  continuum's constant depends on resolution: 0.03 for T21L10 in the manual, while ExoPlaSim's
  radmod.f90 default is `th2oc = 0.024`. Sasamori's abstract describes analytic fits to Yamamoto's
  chart.
- **CCM3 cloud water.** The profile is q_l = (0.21×10⁻³ kg m⁻³/ρ) exp(−z/h_l) with
  h_l = 700 ln(1 + PW) m, "computed according to Kiehl et al. (1996)" (manual p. 35,
  Eqs. 3.99–3.100). The CCM3 note itself (kiehl1996description) is BLOCKED. Hack (1998) is the
  journal paper that introduced the diagnostic cloud water into CCM3; it is in the bib, abstract
  only.
- **Slingo's convective cover.** The constants come from PlaSim's manual, which cites Slingo and
  Slingo (1991). The Slingo (1987) original is BLOCKED; its abstract confirms only an empirical
  cloud–convection relation.
- **Liquid-only cloud optics in PlaSim.** "cloud parameters are derived from the cloud liquid water
  path WL" (manual p. 23).
- **RRTMG k-tables.** The 59 reference pressures start at 1053.63 hPa, with ln p stepping by 0.2
  (module_ra_rrtmg_lw.F lines 3840–3858, 13165–13170). The pressure index is clipped to [1, 58]
  (lines 3676–3682). Two independent groups flagged RRTM's table switch as a hazard in tall or wet
  atmospheres:
  - Seeley and Wordsworth (2021): "RRTM uses different lookup tables and approximations above and
    below a hard-coded pressure" (agent B).
  - Liu et al. (2023) avoided RRTM because of its 100-hPa switch.
- **Ice optics.** RRTMG's ICEFLAG = 1 computes ice optical depths "as in Ebert and Curry, JGR, 97,
  3831-3836 (1992)" (module_ra_rrtmg_lw.F lines 2756–2768). The functional forms named in L21 are
  in the BLOCKED article and are unverified.
- **Drop sizes.**
  - The maximum stable raindrop scales as √(σ/(g(ρ_c − ρ_air))), with r_max and r_min falling "like
    g^−0.5" (loftus2021physics, Sect. 4.3 p. 15, Eq. 26; Sect. 4.4 p. 16).
  - Limit: none of the methods are "expected to yield quantitatively exact values" (Sect. 3.4,
    p. 9).
  - Beard (1976) carries g explicitly in every terminal-velocity regime but fits the upper regime to
    Earth sea-level data up to 7 mm (agent C).
- **Fall speeds.** The Best number X = C_D Re² = 2mgρ_aD²/(Aη²) is proportional to g
  (mitchell1996use, Sect. 2a, p. 1711, Eq. 3). With Re = aX^b (Eqs. 18–21),
  v_t = aν(2αg/(ρ_aν²γ))^b D^{b(β+2−σ)−1} (Eq. 22, p. 1715). For Re > 425, v_t "depends only on air
  density, gravity, particle mass, area, and maximum dimension".
  - Khvorostyanov and Curry (2002) give the similarity parameter "among … various media and planets"
    (p. 1883, agent C).
- **Waves.**
  - SWAN's linear growth is "due to Cavaleri and Malanotte-Rizzoli (1981)" with a Pierson–Moskowitz
    filter (swan4151tech, Eq. 2.36).
  - Exponential growth and whitecapping follow Komen et al. (1984): C_ds = 2.36×10⁻⁵, δ = 0, p = 4
    (PDF pp. 28–30).
  - Wu's drag formula is Eq. (2.34). Wu's abstract gives C₁₀ = (0.8 + 0.065U₁₀)×10⁻³.
  - SWAN's breaker index γ = 0.73 is "the mean value of the data set of Battjes and Stive (1985)"
    (swan4151tech, PDF p. 25).
- **Charging laws.**
  - Saunders and Peck (1998) give the graupel charge sign as a function of rime accretion rate and
    temperature (abstract).
  - Takahashi (1978): sign and magnitude "highly dependent on the temperature and cloud water
    content" (abstract).
  - WRF-ELEC's default is "Brooks et al. RARcrit for T > −15" (README).

### 5. Latent defects

- **Orbit default.** With the default `fixedorbit=False`, ExoPlaSim writes NFIXORB = 0
  (`__init__.py` line 2681). PlaSim's `orb_params` then takes the Berger branch, which recomputes
  `obliq = 23.320556 + obsum` from Berger (1978) for year 1950 − iyrbp. This overwrites the
  configured obliquity (radmod.f90, lines ~2960–3000; p_exo.f90 prints "Using Berger orbit").
  - The `configure()` docstring says only that with False "variations such as Milankovich cycles
    will be computed by PlaSim" (lines 2188–2190).
  - berger1978long is BLOCKED; its abstract confirms the orbital-element series.
- **Sun clock.** See the issue-tracker record below.
- **SWAN's uninitialised KTETA.** This rests on the SWAN source and has no literature root. None was
  sought.

## The repairs

- **General repairs by similarity and scaling.**
  - Mitchell's Eq. (22) with β = 3, σ = 2 gives Re ∝ X^{(b+1)/3} for a fall-speed law V = aD^b, and
    X ∝ g. Hence V ∝ g^{(b+1)/3} for spheres; this is our derivation, stated as such. It does not
    hold for particles whose mass and area exponents differ by other than one.
  - Liu et al. (2023) scaled CRM fall speeds by (g/g_E)^0.5 citing Khvorostyanov and Curry (2002).
  - Loftus and Wordsworth (2021) root the g^−0.5 drop-size scaling.
  - Charnock (1955) roots z₀ ∝ u*²/g ("the simplest non-dimensional relation between them",
    abstract).
- **Processes added.**
  - Ice optics follow Ebert and Curry (1992) as implemented in RRTMG.
  - The effective radius follows a temperature table attributed in code to Kristjánsson and
    Mitchell.
  - WRF-ELEC's charging, discharge and screening: the README documents charge on cloud droplets,
    rain, ice, snow, graupel and hail (SCW…SCHL) plus residual ions (SCIONA), with non-inductive and
    inductive charging (nssl_ipelec = 3). It documents a cylindrical discharge "based on Ziegler and
    MacGorman (1994, JAS)" and a "3D discrete discharge adapted from MacGorman et al. (2001)"
    (lines 106–109).
  - Fierro et al. (2013) describe the WRF discharge as charge reduction "within a prescribed volume"
    (abstract).
  - The stochastic *branched* scheme is Mansell et al. (2002): "three‐dimensional, branched
    lightning discharges" (abstract).
- **Calibrations against a line-by-line reference.**
  - HITRAN2020 (gordon2022hitran2020; HAL copy, CC BY) and MT_CKD (mlawer2012development, abstract)
    are the dataset descriptions. If the in-house model runs MT_CKD 4.x, also cite
    mlawer2023inclusion.
  - The TSIS-1 HSRS (coddington2021tsis, abstract): 202–2730 nm, 0.3% uncertainty between 460 and
    2365 nm.
  - PyRADS (koll2018earth) is rooted by its README as "the Python line-by-line RADiation model for
    planetary atmosphereS". It is a longwave code using HITRAN 2016 and MT_CKD; the shortwave
    version is a separate repository.

## Verification

- Weisman and Klemp (1982) supplies the supercell sounding used for the Earth benchmark of the
  electrified graft (abstract only).
- Bryan and Fritsch (2002) is the moist benchmark. Its abstract establishes that "an equation set
  that conserves both mass and energy is crucial for obtaining the benchmark solution". It does not
  by itself establish that CM1 conserves exactly (L26 as worded overreaches).
- The SWAN/SWASH gravity-similarity tests have no external precedent beyond Banfield et al. (2015).
  They ran SWAN and UMWM on Mars with "no ad hoc calibration" (p. 370) and noted that their wind
  tunnel tests "did not allow us to explore varying gravity" (p. 373).
- The paper's identity regression (patch off = upstream byte for byte) is a software-engineering
  check with no literature root needed.

## Results

**Clouds against published models.**

- *Slow rotation.* Yang et al. (2014) find TS falls 20 K from 1 to 256 days because "the cloud
  albedo is much higher on slowly rotating planets" (arXiv p. 4).
- *Regime transition.* Way et al. (2018) place the transition to a day–night circulation between 32
  and 64 days and explain it by t_rad = pc_pT/(gF) (arXiv p. 14). At 1.2 atm and lunar gravity t_rad
  is about 7× Earth's: our arithmetic, per the project's GCM notes.
- *ROCKE-3D albedos at Earth's insolation and obliquity* (Del Genio et al. 2019, ApJ 884, 75,
  Table 1 rows 32–37): 0.306, 0.294, 0.273, 0.307, 0.328, 0.372 for 1, 8, 16, 64, 256 and 365 (1:1)
  days.
- *ECHAM6 aquaplanet.* Salameh et al. (2018) give global shortwave CRE from −62 W m⁻² at 1 day to
  −36 W m⁻² at 200 days for non-synchronous rotation, with sea ice expanding (p. 2402).
- *Absolute cover.* Yang et al. (2019) Table 2 gives 70–86% across five GCMs for the Earth-rotation
  aquaplanet, or 43–86% if LMDG with maximum overlap is counted (agent B).
- *Explicit convection.*
  - Yang et al. (2023) find 26.9% and 41.1% cover in SAM against 94.8%/81.7% (CAM3) and 90.4%/97.4%
    (ExoCAM) on two tidally locked planets.
  - Lefèvre et al. (2021): Bond albedo 0.06 in the convection-resolving box against 0.32 in the GCM.
  - Sergeev et al. (2024), the opposite finding: explicit convection *raised* low cloud and albedo
    in a global stretched-mesh model.
  - Sergeev et al. (2020): explicit convection in a nest raised substellar albedo about 3%.
  - Wei et al. (2020): refining ExoCAM's grid alone changes little.

**Lightning.**

- Explicit electrification has run off Earth only in Jovian (Yair et al. 1995, 1998) and Titan
  (Tokano et al. 2001) cloud models.
- Exoplanet studies diagnose flash rates from bulk cloud properties (Sergeev et al. 2025; Braam et
  al. 2022).
- Reviews: Aplin (2006); Helling et al. (2016). Settling under gravity separates the charged
  particles, so gravity enters directly.
- Breakdown scaling: WRF-ELEC's code and README (Dwyer 2003). Riousset et al. (2020) note the
  threshold depends on composition, charge density, pressure and temperature (abstract, agent B).
- Standler and Winn (1979) find that coronae from vegetation "limit the magnitude of the field at
  the ground to about 10kV m⁻¹" (abstract).

**Waves.** Earth-built wave growth adapted to other worlds:

- Ghafoor et al. (2000) scaled empirical models to Titan (abstract). Hayes et al. (2013) note it
  "ignored the effects of viscosity, density, and surface tension" (p. 403).
- Hayes et al. (2013) assume the dimensionless constants are "independent of changes in liquid
  and/or atmospheric properties" (p. 407).
- Banfield et al. (2015) ran SWAN on Mars.
- Rubin et al. (2022) patched SWAN 40.72 for Mars' air density (data release; agent C).
- Schneck et al. (2026) argue Earth's empirical models are confounded by other atmospheres, liquids
  and gravity (abstract).
- Lorenz and Hayes (2012) is BLOCKED and unread.

## Reach to other worlds

- **Mars.** WRF on Mars (spiga2009new; spiga2010structure LES, abstract); MarsWRF (toigo2012impact,
  not in bib).
- **Titan.** TitanWRF; TRAMS from RAMS (barth2007trams, "adapted from RAMS"); Rafkin et al. (2022)
  GCM-to-CRM workflow (abstract); Hueso and Sánchez-Lavega (2006) storms (abstract); Lora et al.
  (2015) TAM is plane-parallel (agent C).
- **Venus.** Lefèvre et al. (2018) LES of the cloud layer (abstract).
- **Jupiter.** Sugiyama et al. (2014) CRM (abstract).
- **Exoplanets.** ROCKE-3D, LMD generic (Wordsworth et al. 2011 uses correlated-k, arXiv p. 2),
  ExoCAM (Wolf et al. 2022), Isca ("provided that the thickness of the modelled atmosphere is small
  compared to the planetary radius", Vallis et al. 2018 Sect. 8.1, agent A), THOR, the UM.
- **Deep-atmosphere criteria for taller worlds.** White et al. (2005); Mayne et al. (2014 GMD,
  Table 1); Tort et al. (2015); Mayne et al. (2019); Borchert et al. (2019); Skamarock et al.
  (2021).
- **Lunar atmospheres.** Aleinov et al. (2019) ran ROCKE-3D for a ≤10-mbar volcanic paleo-atmosphere
  at 4°×5° and 40 layers (arXiv p. 6). Needham and Kring (2017) estimate up to ~1 kPa for ~70 Myr
  (abstract). Saxena et al. (2017) model a primordial rock-vapour atmosphere without a GCM.
- **Gravity sweeps.** Liu et al. (2023) is the only CRM gravity sweep (0.38–1.5 g_E); the model
  crashed at lower g. Lunar gravity (0.165 g_E) is outside every published CRM.

## Next work

- **Deep dynamics.** Rooted in White et al. (2005) and Mayne et al. (2014, 2019). Wood and
  Staniforth (2003) show a shallow model can be made deep without changing infrastructure (abstract;
  not in the bib). Skamarock et al. (2021) add a deep option to MPAS behind a switch at under 5%
  cost (agent A).
- **An independent GCM on the same scenario.** ROCKE-3D (way2017resolving; ROCKE-3D 2.0) or the LMD
  generic model (wordsworth2011gliese; forget2014possible).
- **A CRM at lunar gravity.** Nothing published reaches it (Liu et al. 2023).
- **Spherical radiation.** Li and Shibata (2006) Eq. (12); Prather and Hsu (2019);
  Dahlback and Stamnes (1991), BLOCKED.

## Where this paper appears to be first

Searches up to 2026-10-17 found none of the following. Each is stated as "none found", not as
proven absent.

- No GCM or cloud-resolving study of a breathable, terraformed or thick-atmosphere Moon. The only
  lunar GCM is Aleinov et al. (2019), at ≤10 mbar. A 2002 IAF abstract (Renn) and a 2025 blog
  running ExoPlaSim with lunar parameters are not admissible.
- No CRM or LES of a slowly rotating, non-synchronous (moving-sun) terrestrial planet. All CRM–GCM
  cloud comparisons found are 1:1 tidally locked, with periods of 6.1–60 days.
- No CRM in N₂/O₂ air at lunar gravity.
- No use of WRF-ELEC or NSSL explicit electrification off Earth.
- No GCM implementing spherical slant-path solar heating for a planet with large H/R. Agent C's
  search was not exhaustive.
- No published classification of hidden-Earth assumptions into forms. The individual phenomena are
  widely acknowledged (see The need).

**Not first:**

- CM1 has been used off Earth: Tan et al. (2021), "the first extraterrestrial use of the CM1", at
  Earth gravity; Habib and Pierrehumbert (2024) modified CM1's constants and buoyancy; Seeley and
  Wordsworth (2021) cross-checked with CM1, RRTMG and Morrison.
- SWAN has been run under Mars gravity and air: Banfield et al. 2015; Rubin et al. 2022.
- The ExoPlaSim solar-day problem was partly identified by its authors (Paradise et al. 2022,
  Sect. 2.1).

## Opposite and limiting findings

- **Curvature.** Li and Shibata (2006): negligible for Earth because the atmosphere is thin. This
  limits the Earth precedent; it does not cover the Moon.
- **Explicit convection.** Sergeev et al. (2024) find *more* low cloud, opposing the direction of
  Yang et al. (2023) and Lefèvre et al. (2021). Sergeev et al. attribute part of Yang's gap to a
  circulation-regime change.
- **Yang et al. (2023) caveats.**
  - The paper calls SAM "cloud-permitting".
  - Cloud fraction is a condensate threshold in SAM but humidity-based with overlap in the GCMs.
  - The gap is largest on the nightside and at dayside high latitudes.
  - SSTs were prescribed and the boundaries were walls.
- **Resolution.** Wei et al. (2020): resolution alone matters little.
- **Gravity.**
  - Thomson and Vallis (2019): dry hydrostatic dynamics depend on g only through vertical rescaling.
  - Mayne et al. (2019): the gravity difference alone did not significantly change the flow in their
    standard case (agent A; not re-checked).
- **Earth-centric tunings.** Tsigaridis et al. (2025): removing them changed Earth's simulated net
  radiation by only −1.27 W m⁻²; planet differences dominate (agent A).
- **Drops.**
  - Loftus and Wordsworth (2021): absolute r_max is uncertain by a factor of a few, and on Earth
    collisions, not stability, set the largest drops.
  - Beard (1976) is fitted only to 7 mm.
- **Waves.** No experiment has varied gravity (Banfield et al. 2015). Titan growth thresholds rest on
  scaled Earth observations (Hayes et al. 2013).
- **ExoPlaSim's own limitations section** concedes the solar-tuned water absorptivity and bottom-layer
  Rayleigh scattering (Paradise et al. 2022, Sect. 5).

## Flags for the draft

These are claims that the sources do not support as currently written.

1. **hidden_earth.tex H22, "a breaker index of 0.73 [battjes1978energy]".** Battjes and Janssen
   (1978) "chose" γ = 0.8 (p. 586). SWAN's documentation attributes 0.73 to "the mean value of the
   data set of Battjes and Stive (1985)" (swan4151tech, PDF p. 25). battjes1985calibration has been
   added to the bib (abstract not read; BLOCKED).
2. **H17, "Sasamori's broadband longwave has a continuum fitted to the outgoing flux".** The
   continuum is PlaSim's own (manual Eq. 3.55), with resolution-dependent defaults. Nothing read
   says it was fitted to the outgoing flux, so the fit needs its own source or a Terluna record.
3. **H21, Morrison's 2.8-mm and 0.3-mm values [morrison2005new].** These are in CM1's morrison.F
   (lines 492, 495). The breakup arrived in scheme version 2.1 "following Verlinde and Cotton (1993)",
   after the 2005 description. Cite the code (bryan2026cm1) and verlinde1993fitting.
4. **H07 and L4, Slingo's constants.** PlaSim's manual attributes them to Slingo and Slingo (1991);
   the Slingo (1987) paper is unread. The draft's choice of slingo1991response plus
   lunkeit2012plasim is correct.
5. **The "35" attribution.** PlaSim's manual cites Rodgers (1967, QJRMS). Lacis and Hansen (1974)
   and Li and Shibata (2006) cite Rodgers' 1967 MIT report. Cite Lacis and Hansen for the factor.
6. **"−0.03 to +0.04" albedo for slow rotators** (project GCM notes). ROCKE-3D's rows in Del Genio et
   al. (2019, Table 1) give −0.033 to +0.022 for 8–256 days and +0.066 for the synchronous case.
   Salameh et al. (2018) give CRE, not planetary albedo. Recompute or re-source before use.
7. **"Five GCMs give 43–86%".** That spans six configurations, and the 43% is a cloud-overlap
   choice. With random overlap the five GCMs give 70–86%.
8. **"A cloud-resolving model gave 27–41%".** The numbers are right, but Yang et al. (2023) call the
   model cloud-permitting and define cloud fraction differently.
9. **L1, "gravities, radii".** Paradise et al. present synchronous/slow rotation, stellar spectra and
   pressure as the modifications. Gravity and radius are configuration settings.
10. **L17, breakdown fields scaling with density.** Shown in WRF-ELEC's code. The Dwyer (2003, 2007)
    abstracts do not state it, and the bodies are unread.
11. **L18, "channel internal fields of order kV/m".** Not in Lalande et al.'s abstract; WRF-ELEC uses
    200 V/m. **L19, "onset of a few kV/m".** Standler and Winn give corona current at 8 kV/m and a
    ground-field limit near 10 kV/m.
12. **L20 (150–170% ice saturation) and L21 (Ebert–Curry functional forms)** are unverified; both
    sources are BLOCKED.
13. **L26.** Bryan and Fritsch (2002) establish the benchmark and the importance of mass-and-energy
    conservation, not CM1's design. Cite CM1's documentation for the latter.
14. **SWAN drag.** The user manual and code make Wu (1982) the 41.51 default. The technical
    documentation's "Since version 41.01 … Eq. (2.35)" is stale. Say which the runs used.
15. **R02, "(b+1)/3".** Holds for spheres (mass ∝ D³, area ∝ D²) via Mitchell's Eq. (22). Say so.
16. **wolf2015evolution as ExoCAM.** Add wolf2022exocam.
17. **S08, "about 25 kg m⁻²" [trenberth2005trends].** Unverified (not read).
18. **H03, "acts on Earth only below about 4.5 km".** A derived statement; its inputs are WRF-ELEC's
    284 kV/m × ρ/ρ₀ and the 180 kV/m cap.

## ExoPlaSim issue tracker (task 4h)

Searched on 2026-10-17 through the GitHub API:

- all 57 issues and pull requests of alphaparrot/ExoPlaSim (default branch master, last push
  2026-09-19) and all 174 issue comments;
- a keyword filter for obliq, fixedorbit, solang, hour angle, rotationperiod, rotspd, sidereal,
  synodic, solar day, day length, diurnal, zenith, czen, eccentric, keplerian, insolation,
  solar_day and n_days_per_year;
- GitHub-wide issue search: "solang rotspd", "plasim hour angle rotation", "exoplasim rotationperiod
  insolation", "exoplasim obliquity fixedorbit", "plasim nfixorb obliquity", "plasim solar day
  sidereal";
- the PlaSim upstream tracker HartmutBorth/PLASIM (3 issues, none relevant);
- the documentation landing page (exoplasim.readthedocs.io): no mention of these behaviours.

Findings:

- **Sun clock.** The only report is
  [issue #69](https://github.com/alphaparrot/ExoPlaSim/issues/69), "solang: Sun skips back once per
  model day when rotationperiod ≠ 1…". It was opened 2026-09-29 by **dgoldman0, the paper's author**.
  It is open, with no comments, as of 2026-10-17. It is therefore not an independent report.
  - It scopes the defect to non-synchronous runs with `keplerian=False`.
  - It quotes plasim.f90 lines 1296–1348 and radmod.f90 lines 1371–1409 on master.
  - It reports the Moon-like example: 392.5° swept per model day, a 32.5° skip, and time-mean
    insolation 0.917–1.174 of the zonal mean.
- **Related, earlier maintainer statements**
  ([PR #2](https://github.com/alphaparrot/ExoPlaSim/pull/2), 2023-05-02):
  - alphaparrot: "I think the older code has the solar day more or less constant", and "the math of
    how solar day is computed assumes the sidereal year is much longer than the sidereal day".
  - hersfeldtn: "the current model treats the solar and sidereal days as equivalent, or very
    similar".
  - These concern the solar-day definition, not the daily reset of the hour angle.
- **Obliquity in another code path.**
  [PR #5](https://github.com/alphaparrot/ExoPlaSim/pull/5) (open; hersfeldtn, 2023-07-31) reports
  that with `keplerian=True` and a fixed substellar point "the declination was being set to a
  constant value equal to the obliquity". This is a different behaviour.
- **fixedorbit and obliquity.** No issue reports the Berger override of a configured obliquity.
  - Users' configurations routinely set `fixedorbit=True`, and ExoPlaSim's tidally locked presets do
    so (`__init__.py` lines 4326–4374).
  - In PR #2 (2023-04-10) wizzeh wrote that "ExoPlaSim can optionally simulate Milankovich cycles …
    As long as you set `fixedorbit=True` … these calculations won't happen". This is community
    awareness that the default computes Earth's orbit, not a report that it discards the configured
    tilt.
  - The behaviour is consistent with the docstring but carries no warning, so "silently" is fair if
    phrased as "without a warning".

## Search log

All searches were run on 2026-10-17.

**This agent:**

- Crossref works and bibliographic queries for all 78 candidates and 66 added sources; DataCite for
  the two NCAR notes.
- OpenAlex and Semantic Scholar for open access and abstracts.
- arXiv API for versions.
- GitHub API for ExoPlaSim, PLASIM, MicroTed/wrf4-elec (README at e43041b) and danielkoll/PyRADS.
- Web fetch of the ExoPlaSim documentation and the SWAN release notes ("The current version number
  of SWAN is 41.51").
- Read & Lebonnois (2018, AREPS; HAL) and Showman et al. (2013) were checked for a planetary-parameter
  table and lack one. Read et al. (2016, QJRMS, CC BY) may have one, but the Bern repository returned
  503 and Wiley blocks.
- Fulchignoni et al. (2005, Nature 438, 785, Huygens HASI) was verified as a fallback source for
  Titan's surface values.

**Agent A (model adaptations; deep atmosphere).** 34 web queries:

- PlanetWRF/TitanWRF/MarsWRF;
- ROCKE-3D 1.0/2.0; Generic PCM description (none: "Forget et al., to be submitted", per Bhatnagar et
  al. 2026 GMD); ExoCAM 2022; THOR 2.0; UM;
- Mayne 2014/2019; Tort & Dubos 2014/2015; UA-ICON; MPAS deep;
- seven queries for a terraformed or thick-atmosphere Moon (none);
- CM1 planetary adaptation.

**Agent B (CRMs; lightning).** 15 queries, including:

- Yang 2023 identification;
- Lefèvre 2021; Sergeev 2024; CM1 off-Earth; CRM varying gravity; Rafkin/Barth TRAMS; Hueso 2006;
  Spiga 2017; Jupiter moist convection; NICAM tidally locked (an EPSC abstract only);
- planetary lightning reviews and Yair 2012;
- WRF-ELEC off-Earth (none).

Note: a search-engine summary misreported Yang 2023's numbers; only primary text was used.

**Agent C (curvature; raindrops; waves).** 27 queries, including:

- Li & Shibata 2006; Vasylyev 2021 (DLR elib); Huestis 2001; Prather & Hsu 2019; Fortney 2005;
  Barnes 2018; Lebonnois & Toublanc 1999;
- Loftus 2023 (none); Graves 2008;
- Lorenz & Hayes 2012 (paywalled; abstract withheld); Banfield 2015 (CNR copy) and from it the USGS
  SWAN-on-Mars data release; Schneck 2026 and the PlanetWaves code; Stähler 2019.

**Agent D (legal copies of blocked papers).** Results are to be merged when its report arrives; the
manifest marks the current state.
