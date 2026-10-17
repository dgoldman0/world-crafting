# Ideation

Working notes for the model-development paper on carrying three Earth-built models to a breathable Moon.
Stage 1 of the paper's build (ideate, root in the literature, outline, write in components, review).
Started 2026-10-17 from the review of Terluna at commit 186b294.

## The question the paper owns

Terluna asks what weather, climate, storms and seas a breathable Moon would have: 1.2 atm of
nitrogen and oxygen at the water level, seas over 28% of the surface, sunlight filtered by a shield,
the native 1.62 m/s² gravity and the 29.53-day solar day. No observation can answer it, so every
answer passes through numerical models, and every available model was built and tuned on Earth.
The paper owns the question that sits underneath every Terluna climate result: what has to change in
an Earth-built model before its lunar answer can be trusted, and how far the changed models reach
beyond the Moon.

The Moon is a severe test because it moves several governing ratios at once:

- scale height against radius, H/R about 0.03 against Earth's 0.0013, so the air is tall against
  the curve of the ground and the twilight is long;
- mass per unit area, 7.3 times Earth's at 1.2 atm, so absorber paths run far past the range
  Earth-fitted radiation was fitted on;
- gravity, one sixth of Earth's, so drops fall slowly and every height in pressure terms stands six
  times higher;
- the solar day, 29.5 Earth days, and a rotation of 27.3 days that is synchronous with Earth and
  slow against the Sun;
- the tilt, 1.54°, which leaves the poles a grazing Sun all year.

## Thesis

Earth-built models carry Earth inside them in five forms, and the Moon exposed each:

1. **Dimensional constants written into the code**: g = 9.81 in CM1's dynamics, radiation, CAPE
   and microphysics; SWAN's 1 Hz growth knee and 1.28 kg/m³ air; PlaSim's horizon slant factor of
   35; WRF-ELEC's 180 kV/m breakdown cap and its −7 °C ground-strike level.
2. **Units of time**: PlaSim's convective cloud formula counts rain per model day; on the Moon the
   model day is 29.8 Earth days.
3. **Geometry**: flat, sunlit-only radiation columns; constant gravity and a thin shell in the
   dynamics.
4. **Empirical fits used outside their range**: Lacis and Hansen's water absorptivity, Sasamori's
   broadband longwave, the CCM3 cloud-water profile written in metres, Slingo's convective cover,
   liquid-only cloud optics, RRTMG's k-tables to 1054 hPa, Earth-fitted drop size limits, Wu drag,
   Komen growth, laboratory charging laws.
5. **Latent defects** that Earth's own parameters hide: ExoPlaSim's Sun clock (exact only at a
   one-day rotation), its orbit default (the configured tilt discarded silently), SWAN's
   uninitialised KTETA with breaking off.

The repairs fall into two classes with different reach. **General repairs** turn a hidden constant
into a parameter whose default reproduces the original model exactly, fix a unit, apply a scaling
law, add a missing geometry or process, or remove a defect; they hold on any world. **Calibrations**
fit multipliers or corrections to a reference model on the lunar design column; they hold near that
column and have to be refit for any other. The paper's most portable finding is that distinction,
and the record of which repair belongs to which class.

## Contribution, stated for the reader

- An inventory of every change made to ExoPlaSim 3.4.2, CM1 r22 (with WRF-ELEC's NSSL
  electrification grafted in) and SWAN 41.51, each classified by the form of Earth it removes, with
  its switch, its default and its verification.
- The verification strategy: identity regression (each patch off reproduces the unpatched model
  byte for byte), gravity-similarity tests (SWAN and SWASH at scaled gravity and time), calibration
  against an in-house line-by-line model on the GCM's own columns, and an Earth benchmark storm for
  the electrified build.
- What the adapted models have given: the size of each repair's effect on the lunar climate, the
  location of the remaining uncertainty (clouds and the lowest kilometres' longwave), the
  decomposition of the gap between the cloud-resolving model and the GCM, lunar storms and their
  lightning, lunar sea states.
- A map of reach: which found and crafted worlds the general repairs open, which need new
  calibrations, and which remain outside the adapted models.
- The next work, ordered by how much of the remaining uncertainty it removes.

## Audience and venue

Specialists in planetary and exoplanet climate modelling, cloud-resolving modelling and wave
modelling; modelling groups who port Earth codes to other worlds. The form follows a
Geoscientific Model Development "development and technical paper": the models, the changes, the
verification, the results that depend on the changes, code and data availability. Headings stay
unnumbered and few, by the author's instruction.

## Evidence discipline

The charter's G5 separates sourced observations, original calculations, conditional models and
designs. In this paper:

- Upstream code behaviour is a **sourced observation** of the pinned source, quoted by file and line.
- Lunar climate numbers are **conditional model results**: they hold given the scenario (1.2 atm,
  28% water, the shield and its dimming, placeholder land) and the models' remaining Earth-tuned
  parts.
- Agreement with the in-house line-by-line model is **calibration**, and agreement between patched
  and unpatched builds is **reproducibility**; neither is physical validation. Physical validation
  of a lunar climate is impossible without a lunar climate, so the paper states what each check
  establishes and stops there.
- Reach beyond the Moon is a **calculation of regimes** (scale height, column mass, rotation, gravity
  against the ranges each repair was built or fitted for). It names conditions; it predicts no other
  world's climate.

## What to leave out

Too rough to help another modelling group, by the author's instruction to skip anything rough:

- the CM1 gravity pair (it never convected; its next design was never built);
- the two-dimensional terrain ring (it turned to gales; its lesson enters as one sentence);
- the fine 2-km electrified box (its convection collapsed);
- the single-column lunar day (superseded by the GCM and CM1, and it lacks the twilight);
- the legacy exponential sky atlases (superseded by the solved-column sky);
- run bookkeeping, case set-up and analysis scripts (they stay in Terluna and enter as methods).

## Risks to the argument

- **The 307 K result** rests on a longwave correction fitted at 295 K and known to stray 5–7 W/m² per
  layer at 302 K. The paper reports it as the sensitivity it is, with that condition attached, and
  makes no climate claim from it.
- **Mixed builds**: the 45° N twilight pair ran its control at -O2 and its twilight ring at -O3. The
  twilight's local effect stands as below detection, with no figure claimed.
- **Unconverged scattering orders** in the curved-air ledger's solve: the ledger's terms carry that
  record.
- **The comfort gap** between CM1 and the GCM is a disagreement between models; the paper reports its
  decomposition and the part still unexplained.

## Title candidates

- The Earth inside the models: adapting a climate model, a storm model and a wave model to a
  breathable Moon
- Carrying ExoPlaSim, CM1 and SWAN to a breathable Moon: hidden Earth, general repairs and the
  worlds they reach
- Earth-built models on a breathable Moon: five forms of hidden Earth and the repairs that remove them

## Identity

Paper ID e8b42cb5-48da (UUIDv4 e8b42cb5-48da-402c-b261-4de808e9062a), checked against the five IDs in
Terluna's `ensemble/planning/paper_manifest.json` on 2026-10-17. The paper sits outside the five-paper
Open Moon ensemble; companions may cite it as the shared model package the charter allows. Author
metadata: Daniel S. Goldman, ORCID 0000-0003-2835-3521, no affiliation label.
