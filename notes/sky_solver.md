# The spherical sky solver: correctness, limits and room for improvement

Notes for modellers on the spherical successive-orders sky solver from Terluna's `illumination/sky`.
This repository carries it because the curved-air ledger (Terluna `climate/gcm/twilight.py`), which
produces the GCM's and CM1's twilight terms, computes its multiple scattering with it.

References are `path:line` in Terluna at commit 186b294; JSON products are cited by key. Bulk run
files are on Terluna's research drive, outside Git. **Terluna** marks what Terluna's code, documents
and products state. **Finding** marks this review's own reading, arithmetic, or inspection of run
metadata (2026-10-17). No solver was run for these notes: the numbers marked Finding come from
committed products, run metadata and small arithmetic checks on committed inputs. The ledger itself
is covered in [reference_radiation.md](reference_radiation.md).

## Files and provenance

The five modules this repository takes, to sit under `python/` at their Terluna package paths:

| Terluna file | Role | sha256 (first 16) at 186b294 |
|---|---|---|
| `illumination/sky/solver.py` | Ray geometry, segment weights, the Rayleigh moment operator `transport`, the legacy exponential-profile driver | `4734f86860f38f65` |
| `illumination/sky/solved_transport.py` | Layered spherical transport: exact shell lengths, finite-disk beam table, per-altitude angular quadrature, order loop, ray evaluation, energy ledger | `3fe4c255e8ffe532` |
| `illumination/sky/solved_optics.py` | Layer optics from the solved columns, the spectral reduction and its beam audit | `9927832942de3f82` |
| `illumination/sky/atmospheres.py` | Legacy atmospheres and Bruneton's solar and ozone bins; imported by `solver.py` | `69065d459a41ef20` |
| `illumination/sky/colour_matching.py` | Analytic CIE 1931 functions (Wyman, Sloan and Shirley 2013), 683 lm/W | `485f65f4eccac4c9` |

Terluna: the solved-sky product records the same hashes for `solver.py`, `solved_transport.py`,
`solved_optics.py` and `colour_matching.py` (`illumination/sky/results/solved_sky.json`,
`producer.files`), so its checks describe this code. The checks run from four further modules not
listed above: `solved_reference.py` (`4d7dafbd3aacc0bb`), `reference_mc.py` (`7799178ae4be2670`),
`solved_checks.py` (`5afe8bf87653f7a2`) and `solved_sky.py` (`a5f6fb2b9960bf94`).

Licence: `atmospheres.py:10-15` holds arrays transcribed from Bruneton's BSD-3-Clause `demo.cc`
(`SOURCES.md:20-30`). A copy must keep the notice in Terluna `illumination/sky/LICENSES.txt`.

## What it computes

The steady radiance field of a clear, horizontally uniform, spherically symmetric atmosphere over a
Lambertian ground, lit by a distant Sun of finite angular size. It is computed per spectral channel
and per unit top-of-atmosphere normal irradiance. With uniform air and ground the field is
axisymmetric about the planet–Sun axis and depends only on radius r and local solar elevation a
(`validation/legacy_v1/METHODS_v1.md:66-68`).

**Stored per scattering order on an (r, a) grid:**
- the diffuse moments J = ∫I dΩ and K_ij = ∫I d_i d_j dΩ, in the local radial, sun-plane tangential
  and perpendicular frame (K_rr, K_tt, K_pp, K_rt; K_rp = K_tp = 0 by symmetry);
- the downward horizontal diffuse flux, and in the solved path also the upward flux
  (`solver.py:210-216`);
- a separate direct-beam table of normal and horizontal irradiance on a finer grid
  (`solver.py:103-129`; `solved_transport.py:48-77`).

**Derived from these:**
- sky radiance seen from the ground (`solved_transport.py:222-263`), or from a height and over
  finite distances (`aerial.py`);
- surface direct and diffuse flux;
- a whole-sphere energy ledger (`solved_transport.py:266-305`);
- in the product, XYZ atlases at 30 Sun elevations from −30° to 90° (`solved_sky.py:29-30, 79-169`).

**Two generations share the operator:**
- **Legacy exponential atlases** (2026-09-21). `solver.solve` (`solver.py:231-264`) runs on exp(−h/H)
  profiles at 22 wavelengths from 380 to 800 nm, for Earth, the Moon with 300 DU of ozone and the
  Moon without ozone (`atmospheres.py:33-37`). In Terluna they feed the month-of-light viewer and the
  immersion bake. They are not for new work here.
- **Solved-column sky** (2026-10-03, commit 36f124e). It runs on the atmosphere domain's 100-layer
  solved columns from 360 to 830 nm, for two cases (`SOLVED_COLUMN.md:9-31`). The design Moon has
  1.2 atm of dry air, a 294.9 K surface and titania-stack sunlight ×0.95. The Earth control has
  1 atm, 288 K and unfiltered sunlight. The product is `solved_sky.json`. This is the path the
  ledger uses.

**Why spherical** (Finding, from committed numbers):
- **Tall air.** H/R is 0.0279 for the Moon's legacy profile against 0.0013 for Earth. At a solar
  depression of 6° the planet's shadow covers the air above the observer up to 9.6 km on the Moon
  (0.20 H), against 35 km (4.4 H) on Earth; at 18°, 89 km (1.85 H) against 328 km (41 H). The horizon
  air mass √(πR/2H) is about 7.5 against 35.
- **Bright twilight.** In the solved product the Moon's diffuse horizontal light is 2,207 lx at Sun
  −6°, 838 lx at −12° and 268 lx at −18°. Earth's is 3.0 lx at −6° and 0.0057 lx at −12°
  (`worlds.*.samples`).
- **Flat-layer shortfall.** Terluna's pseudo-spherical two-stream falls short of the legacy
  spherical atlas by factors 1.35, 1.96 and 7.2 at Sun 10°, 5° and 1° on the Moon, against 1.00,
  1.06 and 2.23 on Earth (`illumination/surface_light/results/surface_light.json`,
  `checks.atlas_comparison`).

## Method

Terluna describes it as a newly written scalar solver informed by Bruneton's (2017) precomputed-
scattering reference for spherical transmittance, successive scattering orders, surface reflection
and spectral display conversion. It is not libRadtran/MYSTIC and not Bruneton's GPU code
(`SOURCES.md:4-7, 9-19`). Finding: it shares Bruneton's order-by-order formal solution in spherical
geometry. Where Bruneton tabulates 4-D lookup textures, it stores the field as angular moments on an
(r, a) grid and integrates explicit rays.

- **Rays.** Straight rays run through concentric shells. Every shell crossing splits a ray, tangent
  rays keep both crossings, and rays that meet the ground end there (`solver.py:41-71`). Extinction
  and source are constant in each segment, and the formal solution is exact for those values
  (`solver.py:74-83`; `solved_transport.py:81-93`).
  - Legacy: segment midpoints sample the continuous profile.
  - Solved: each of the 100 layers is a homogeneous shell that conserves its vertical optical depths
    (`SOLVED_COLUMN.md:18-20`). Transport shells are the layer edges plus a grid quadratic in height
    (`solved_transport.py:150`).
- **Source.** For p(Θ) = 3/(16π)(1 + cos²Θ) the scattering source is 3/(16π)(J + d_i K_ij d_j),
  which is exact for this phase function (`METHODS_v1.md:56-64`). The moments are interpolated
  bilinearly in (r, a) at each segment midpoint. The beam term (1 + ν²)F takes the beam from its own
  finer table (`solver.py:193-209`).
- **Orders.**
  - Order 1 is the beam's single scattering plus the ground's reflection of the direct beam. Order n
    takes order n−1's moments and downward flux as its source (`solver.py:170-217`).
  - Ray evaluation uses the moments without the last order, plus the beam. This reconstructs orders
    1…N (`solved_transport.py:260-263`; `SOLVED_COLUMN.md:49-51`).
- **Stopping.**
  - Legacy: stop when the last order adds less than 5×10⁻⁴ of the ground diffuse flux at every
    wavelength and every Sun elevation ≥ −24° (`solver.py:252-257`).
  - Solved: each channel stops after order 8 once two increments both fall below 2×10⁻⁵, with a cap
    at order 100 (`solved_transport.py:154, 167-197`). The increments are the ground increment
    (Sun ≥ −24°) and the field-maximum J increment.
  - `solved_checks.finish_orders` continues capped channels up to order 160
    (`solved_checks.py:112-152`). The export refuses an unconverged solution (`solved_sky.py:87-88`).
- **Sun.**
  - Uniform disk without limb darkening, integrated in 12 strips over the visible circular segment
    with its exact area. The phase function uses the disk-centre direction (`solver.py:103-129`;
    `solved_transport.py:48-77`; `METHODS_v1.md:48-54`).
  - Disk radius: 16′ in the legacy path; 0.2665° in the solved path, from `SUN_RADIUS/AU`
    (`solved_transport.py:19-21`).
  - Slant columns: legacy by 240-segment quadrature (`solver.py:86-100`); solved by exact shell
    lengths (`solved_transport.py:25-44`).
- **Ground.** Lambertian, spectrally neutral, albedo 0.1 in every product. A ground-hitting ray adds
  T·(A/π)·(F↓ + direct horizontal irradiance) (`solver.py:186-192`).
- **Angles.**
  - Gauss–Legendre quadrature in μ, by sub-interval, with uniform azimuth.
  - Legacy: splits at −0.12, 0 and +0.12 at every altitude (`solver.py:138-145`).
  - Solved: also splits at each radius's geometric ground horizon μ_h = −√(1 − (R/r)²), so the
    ground–sky discontinuity is an interval end at every altitude (`solved_transport.py:96-108`;
    `SOLVED_COLUMN.md:41-45`). `test_solved_sky.py:47-56` checks the ground solid angle to 10⁻¹³.

Grids (`solver.py:220-229`; `solved_transport.py:138-151`):

| Quality | Radii | Solar-elevation step, −40° to +30° (5° outside) | μ nodes | Azimuths | Transport shells | Beam table |
|---|---|---|---|---|---|---|
| Legacy standard | 35 | 0.75° (−35° to +30°) | 5 × 4 intervals | 16 | 56 + ozone edges | 101 radii; 0.125° from −40° to +20° |
| Solved draft | 29 | 2° | 3 × 5 | 12 | 40 + layer edges | 161 radii; 0.125° from −40° to +20° |
| Solved standard | 45 | 1° | 5 × 5 | 16 | 72 + layer edges | as draft |
| Solved refined | 57 | 0.75° | 6 × 5 | 20 | 92 + layer edges | as draft |

Radii are spaced quadratically in height up to the top. That top is 10 H for the legacy profiles and
the column top for the solved ones: 575 km for the Moon and 92 km for Earth.

**Optics, legacy.**
- Rayleigh coefficient 1.24062×10⁻⁶ (λ/µm)⁻⁴ m⁻¹ times a density multiplier.
- Ozone at its 233 K cross section, in a triangle from 10 to 40 km scaled by H/8 km.
- Moon: H = 8 km × 9.80665/1.62 = 48.428 km, multiplier 1.2, top at 10 H (`atmospheres.py:17-47`).

**Optics, solved.** `fine_optics` (`solved_optics.py:69-123`) keeps all 100 layers of the solved
column (`SOLVED_COLUMN.md:23-31`):
- below 500 nm, the photolysis model's 1-nm molecular absorption and Rayleigh scattering, with
  Bodhaine et al. (1999) cross sections including the King factor;
- above 500 nm, H₂O and O₂ lines on a 0.05 cm⁻¹ grid, with the MT_CKD 4.3 continuum and HITRAN
  collision-induced absorption (CIA), plus the solved trace gases;
- TSIS-1 HSRS sunlight through the shield.

**Spectral reduction** (`solved_optics.py:126-166, 191-257`).
- Within each 10-nm band, wavelengths are ordered by whole-column extinction (one ordering for all
  layers) and grouped in solar-energy quantiles.
- Groups are bisected until the summed XYZ error on the training slant beams (34 for the Moon, 30 for
  Earth) meets the target. The production target is 1% (`solved_sky.py:52`).
- Result: 114 channels for the Moon, 90 for Earth.

**Use in the curved-air ledger** (Terluna; `twilight.py:9-26, 57-66, 234-372`;
`climate/gcm/README.md:975-985`):
- The ledger builds 10,697 energy-faithful channels from 360 nm to 5 µm.
- The 282 channels below 1,250 nm with whole-column absorption below 3 go through
  `solved_transport.solve` at standard quality and albedo 0.1, in 12 batches.
- The rest take the direct beam through the same shells, with the diffuse field of a
  pseudo-spherical two-stream column.
- Layer absorption comes from J, and ground absorption from F↓ of the retained series plus the beam.

## Correctness: checks and evidence state

Every check below is verification: it tests that the code solves its stated equations for its
stated inputs. The evidence state of each kind:
- **Analytic:** the implementation against a closed-form limit.
- **Independent sampling:** Monte Carlo with separate discretisation but the same physics.
- **Self-convergence:** the same code at another resolution.
- **Conservation:** the energy ledger.

### Unit tests (analytic)

- **`test_solver.py`** (21 tests of the legacy operator; `test_solver.py:8-81`):
  - vertical gas and ozone columns against analytic integrals; Earth's tangent column against the
    Chapman asymptote;
  - planet shadow and ray boundaries; segment conservation to 2×10⁻¹⁴; the absorbing-segment
    account; vacuum;
  - the finite disk half, full, hidden and with monotone contact;
  - Rayleigh normalisation and the isotropic-field trace; full-sphere quadrature; bilinear
    interpolation;
  - the CIE peak and equal-energy white; the lunar clock; ozone bounds.
- **`test_solved_sky.py`** (8 tests of the solved path; `test_solved_sky.py:15-121`):
  - shell lengths against an independent nested-sphere routine;
  - Beer–Lambert beam and weight closure; finite-Sun occultation in vacuum;
  - the per-altitude quadrature (ground solid angle and polynomials); vacuum transport and the moment
    trace;
  - the reduction conserves energy and XYZ, and splits at a saturated line; it fails when its budget
    cannot be met;
  - Monte Carlo wavelength sampling against an analytic absorbing Lambertian ground.
- **Others:**
  - `test_atlas.py`: 10 invariants of the legacy atlases; skipped unless the atlases have been
    generated.
  - `test_aerial.py`: 3 tests; skipped unless the cached Moon solution is restored.
  - `illumination/tests/test_engine_atmosphere.py`: 5 tests.
  - Terluna collects the tests in `illumination/sky` only when numba is installed
    (`illumination/sky/conftest.py`).

### Monte Carlo spot checks (independent sampling)

The relative difference is the deterministic value divided by the Monte Carlo mean, minus 1. σ is the
Monte Carlo standard error over 40 photon groups.

| Set | Paths per spot | Result | Record |
|---|---|---|---|
| Legacy, 24 spots: Sun 3°, −3°, −9°; 440, 560 and 680 nm | 500,000 | Moon: \|Δ\| ≤ 0.66%, all within 1.5σ. Earth: up to 6.9% (Sun −9°, 0.9σ); resolved 5.3% at 5.6σ (Sun −3°, view 10°, azimuth 180°, 560 nm) and 3.4% at 3.5σ (Sun −3°, view 30°, 440 nm) | `validation/legacy_v1/monte_carlo_spots.json`; `METHODS_v1.md:149-153` |
| Legacy noon, 6 spots | 100,000 | Moon −0.30% to −0.78% (≤ 2.6σ); Earth −0.19% to +0.43% (≤ 0.4σ) | `validation/noon_monte_carlo.json` |
| Solved, single channel, Moon: 405, 544 and 647 nm on the standard grid; 5 radiances, 3 diffuse fluxes | 120,000 | Radiance: −0.98% (405 nm, zenith, noon, 2.8σ); the others −0.35% to +0.41% (≤ 1.2σ). Diffuse flux at 544 nm: −0.39% (noon, 1.4σ), −0.91% (Sun 10°, 2.3σ), −1.34% (Sun −6°, 1.7σ) | `solved_sky.json` `additional_checks["monte_carlo.json"]`; `solved_checks.py:84-97` |
| Solved, full spectrum: diffuse horizontal illuminance with wavelengths drawn from the unreduced 159,177-point optics | 240,000 (480,000 for two Earth spots) | Moon: −0.39% (90°, 2.2σ), −0.96% (10°, 4.0σ), −1.26% (1°, 3.7σ), −1.32% (−6°, 2.5σ), −0.99% (−12°, 1.0σ). Earth: +0.13% (90°), −0.06% (10°), −0.23% (0°), +0.05% (−2°), all within 1σ; at −6° unresolved (relative standard error 12.8%); at −12° no sampled contribution | `additional_checks["numerical_checks.json"].spectral_monte_carlo`; `solved_checks.py:98-109, 155-202` |

Terluna's summary is a largest resolved broadband difference of 1.32%, counting a comparison as
resolved when its relative standard error is at most 2% (`numerical_checks.json`;
`SOLVED_COLUMN.md:81-85`). The Monte Carlo uses a point Sun and the deterministic solver a finite
disk (flags in `monte_carlo.json`); the spots are chosen away from disk contact.

### Energy ledger (conservation)

The residual is 1 − escape − absorption in the air − absorption at the ground, per unit incident
power on the top-of-atmosphere disk (`solved_transport.py:266-305`; legacy `global_energy.py`).

| Calculation | Blue | Green | Red | Record |
|---|---|---|---|---|
| Legacy Earth, 440/560/680 nm | −0.12% | −0.19% | −0.27% | `validation/legacy_v1/global_energy.json` |
| Legacy Moon, 300 DU ozone | −4.52% | −2.27% | −0.98% | same |
| Legacy Moon, no ozone | −4.58% | −3.57% | −1.24% | same |
| Solved Moon, 3 channels (405/544/647 nm), draft | −3.38% | −2.49% | −0.95% | `additional_checks["grid_draft_audit.json"]` |
| same, standard | +2.17% | +0.76% | −0.16% | `["grid_standard_audit.json"]` |
| same, refined | +0.20% | +0.80% | +0.44% | `["grid_refined_audit.json"]` |

In the production standard solve over all channels, the Moon's largest residual is 2.26%, in the
bluest channels (16 of 114 exceed 1%); the energy-weighted residual is 0.67%. Earth's are 0.20% and
0.05% (`worlds.*.energy`).

### Self-convergence

| Test | Change | Record |
|---|---|---|
| Moon 3-channel radiance, standard → refined: worst of 12 directions and 3 channels, by Sun elevation | 90°: 0.23%; 30°: 0.23%; 10°: 0.15%; 0°: 0.37%; −3°: 0.52%; −6°: 0.70%; −12°: 1.13%; −18°: 1.58% | `numerical_checks.json` `three_channel_refinement` |
| Broadband diffuse flux, draft → standard | Moon ≤ 0.35% (Sun ≥ 0°), ≤ 1.06% (down to −18°), 1.82% at −30°. Earth ≤ 0.97% (Sun ≥ 0°), up to 82% (down to −18°; see Limitations) | `broadband_grid_changes`; `worlds.*.samples` |
| Line grid 0.05 → 0.025 cm⁻¹, direct beams | ≤ 0.010% Moon, ≤ 0.004% Earth | `line_grid_checks.json` |
| Atlas angles 41 × 65 → 81 × 129, diffuse flux | ≤ 0.014% Moon, ≤ 0.19% Earth | `angular_readout_checks.json` |
| Spectral reduction against the fine grid, direct beams (4 heights × 9 Sun elevations) | Moon ≤ 1.11% in lux, ≤ 0.00046 in xy; Earth ≤ 1.07%, ≤ 0.00053 | `worlds.*.spectral_check` |
| Legacy ray shells 64 → 128 | ≤ 0.65% above the radiance threshold | `validation/legacy_v1/ray_resolution.json` |
| Legacy combined change of grid, disk strips and stopping | ≤ 1.16% Moon, ≤ 7.0% Earth; Terluna notes it is not a pure grid test | `validation/legacy_v1/exploratory_grid_sensitivity.json` |

### Scattering orders

| Run | Criterion | Orders |
|---|---|---|
| Legacy Moon / Earth | 5×10⁻⁴, Sun ≥ −24° | 55 / 14 (`validation/legacy_v1/*_iterations.json`) |
| Solved Moon, 114 channels | 2×10⁻⁵ | median 16; maximum 104, the bluest channel, continued past the cap of 100 (`worlds.moon_1.2atm.settings`) |
| Solved Earth, 90 channels | 2×10⁻⁵ | maximum 20 |
| Calendar point source, 114 channels | 10⁻⁶ over the whole −90° to +90° range | 182 (`illumination/calendar/README.md:105-106`) |
| Ledger, 282 channels | 2×10⁻⁵, no continuation | 281 converged; the 366-nm channel stopped at 100 (Finding, below) |

### Findings on the checks

1. **The lunar diffuse flux is low by about 1%.**
   - In the solved path, all eight lunar diffuse-flux comparisons put the deterministic value below
     the Monte Carlo: the three single-channel ones and the five full-spectrum ones.
   - The gap is 0.39% to 1.34%, and five of the comparisons lie 2.2σ to 4.0σ out. That is a resolved
     bias of about 1%, the size of the grid-refinement changes, not a sampling fluctuation.
   - Radiance spots show no consistent sign. Terluna reports the magnitude (1.32%) but not the sign
     pattern, and the cause has not been identified.
2. **The energy residual is not a convergence measure.**
   - It changes sign between the draft and standard grids and does not fall steadily with refinement
     (544 nm: −2.49%, +0.76%, +0.80%).
   - The term that moves most is diffuse escape at the top (405 nm: 0.540, 0.483 and 0.502 of the
     incident power).
   - Read it as a closure indicator of the order of 1% at refined quality and 2% at standard quality
     in the blue.
3. **The stopping tests cover Sun ≥ −24° only** (`solver.py:253`; `solved_transport.py:167`).
   - The second solved criterion is normalised by the field's maximum J, so it does not control
     relative convergence where the field is faint.
   - Yet the product exports samples down to −30°, and the ledger's terms reach down to −40°
     (`twilight.py:73`).
   - The calendar's full-range test needed 182 orders to reach 10⁻⁶.
4. **The ledger's unconverged orders are negligible.**
   - The ledger records `orders_converged: false` (`climate/results/gcm/twilight.json`, line 25)
     without saying by how much.
   - Batch metadata (`/media/projectspace/terluna-research/gcm-runs/twilight/sky/sky_a6acd69c82efba01_*.npz`):
     281 of the 282 channels met the test. The 366-nm channel stopped at order 100 with a last ground
     increment of 2.75×10⁻⁵, against a tolerance of 2×10⁻⁵.
   - Its increments fell by a near-constant factor of 0.914 per order over the last ten orders. The
     missing tail is therefore about 2.9×10⁻⁴ of that channel's ground diffuse flux, at the worst
     sampled Sun elevation.
5. **The Monte Carlo references share the physics.**
   - Both use the scalar Rayleigh phase function, the same layer optics and the same Lambertian
     ground.
   - The solved reference computes sunlight with the same shell-length routine, `layer_lengths`
     (`solved_reference.py:12-21`).
   - They test the deterministic discretisation, not the physics and not that routine.

### What none of the checks establishes

Physical validity.
- There is no lunar sky to observe.
- The Earth control has not been compared with measured skylight or twilight, nor with an independent
  spherical radiative-transfer code (`METHODS_v1.md:138-162`; `SOURCES.md:4-7, 46-48`).
- The inputs — the solved columns and the shield spectrum — are themselves model products.

The outputs are therefore conditional predictions for a prescribed clear molecular atmosphere under
scalar transport.

## Limitations

### Physics in the core solver

- **Scalar Rayleigh scattering only.**
  - There is no polarisation. Published comparisons for Rayleigh atmospheres put the radiance error
    from neglecting polarisation at up to about 10% at some geometries, with fluxes much less
    affected (e.g. Mishchenko, Lacis and Travis 1994, JQSRT 51, 491; literature, not evaluated for
    these columns).
  - The phase function omits molecular depolarisation. The solved optics use the King factor only in
    the cross section.
- **No refraction.** Rays are straight (`METHODS_v1.md:48-54`; `solved_sky.json` `assumptions`).
  - Finding (estimate): horizontal refraction at the design surface is about 0.15° (Earth 0.58°).
  - At the Moon's 0.508° per hour that shifts sunrise and sunset by about 18 minutes. It is small
    for energy but not for timing.
- **No aerosol, cloud or other non-Rayleigh scatterer.**
  - Finding: the J and K moments represent the source exactly only for the Rayleigh phase function. A
    forward-peaked phase function needs higher angular moments or stored directional radiance, which
    is a structural change.
  - Terluna treats cloud light with a separate Monte Carlo (`illumination/cloud_light`).
- **Uniform world.**
  - The air is horizontally uniform; the axial symmetry depends on it. There is no day–night
    contrast along twilight paths.
  - The ground is uniform and Lambertian with albedo 0.1, with no terrain.
  - The solar disk is uniform, without limb darkening.
- **Homogeneous optical layers** (Finding, estimate).
  - The lowest of the 100 lunar layers is 7.3 km thick and holds 12.6% of the 552-nm optical depth.
  - A smooth reconstruction (extinction log-linear between layer midpoints, renormalised to each
    layer's vertical depth) serves as the comparison. Against it, the homogeneous layers understate
    the 552-nm slant optical depth by 0.9% at Sun 0°, 0.6% at 1° and 0.2% at 5°. That overstates the
    direct beam by 5%, 3% and 0.7%. The figures depend on the assumed within-layer shape.
  - No Terluna check refines the optical layering: the grid tests refine the radiance grids and
    shells within fixed layer optics.
- **Spectral range.** The sky product covers 360–830 nm; the ledger sends channels up to 1,250 nm
  through the solver.

### Legacy exponential atlases

Terluna describes the profiles as convenient optical proxies, not solved hydrostatic columns
(`METHODS_v1.md:13-24`). It records the rounded gravity as a known inconsistency
(`shared/constants.json:74-83`; `shared/README.md:14-18`).

Findings, by component:
- **1.62 m/s².** Against GM/R² = 1.62422 m/s², the scale height, column and optical depth are all
  0.26% high.
- **8 km and Bruneton's coefficient.** With H = 8 km, Earth's Rayleigh optical depth at 550 nm is
  0.1085. Terluna's solved Earth column gives 0.0983 (`worlds.earth_control.optical_column.column`):
  the proxy is 10% high.
- **Constant g.** exp(−h/H) ignores the fall of gravity with height.
  - For an isothermal atmosphere in g ∝ r⁻², the column is n₀H(1 + 2H/R + …): +5.6% on the Moon,
    +0.25% on Earth. The solved Moon column holds 80,278 kg/m² against p_s/g_s = 76,096 kg/m² (+5.5%).
  - With H = 48.4 km, the isothermal density at 100, 200 and 300 km is 1.12, 1.53 and 2.49 times
    exp(−h/H). The proxy starves the high air that lights deep twilight.
  - Terluna's A1 reference finds the lunar column 11.62% longer than the 1.2 × 48.4 km proxy
    (`illumination/references/A1_METHODS.md:23`).
- **Net effect.** In total optical depth these biases nearly cancel for the Moon: the legacy τ at
  550 nm is 0.788, against 0.757 solved (+4%). The gap between Earth's +10% and the Moon's +4% is the
  constant-g deficit. The biases do not cancel in the vertical distribution of the air.
- **Ozone.** The default lunar atlas carries 300 DU; the solved design column has about 10⁻¹¹ DU.
- **Energy residual.**
  - Terluna leaves the legacy lunar residual of up to 4.6% unresolved (`METHODS.md:44-45`;
    `validation/full_cycle_checks.json` `legacy_global_residual_resolved: false`;
    `research/status.json:357`).
  - Finding: with the fixed splits, the share of μ assigned to ground-bound directions is wrong by up
    to 0.12 of the interval [−1, 1] at lunar altitudes (median 0.047). On Earth the error is up to
    0.037 (median 0.008).
  - That is consistent with the larger lunar residual but does not prove it is the cause. The
    per-altitude split removes this source.

`atmospheres.py` comes with `solver.py`, which imports it (`solver.py:22-25`). Use its EARTH and MOON
definitions as test fixtures only, and do not generate new exponential atlases.

### The 114 production channels overstate absorbed energy

Terluna (`climate/gcm/README.md:987-991`): with the Sun overhead, the 114 channels absorb 104.5 W/m²
above 500 nm against the fine grid's 66.2 W/m² — 58% too much. The stated mechanism is that each
channel's optical depth is averaged over wavenumbers mixing windows with opaque water and O₂ lines,
and an averaged depth absorbs more than its members. The ledger's faithful channels agree with the
fine grid within 0.4–0.8%. The `illumination/sky` documents and the product's reading rule do not
mention this.

Finding, why the reduction never splits those channels:
- **The error budget is photometric.** Y is normalised by itself, and X and Z by X + Y + Z
  (`solved_optics.py:211-214`). Wavelengths with no CIE weight therefore never trigger a split.
- **Every band above 720 nm stays a single channel.** The 15 channels at or above 700 nm carry 22% of
  the 360–830 nm solar energy but only 3.5×10⁻⁴ of the Y weight
  (`research/runs/optical_comfort/spherical/moon_1.2atm_production_optics.npz`).
- **The O₂ A band is averaged shut.** The 760–770 nm channel averages the band's lines and windows to
  a whole-column absorption depth of 37, which is opaque, although much of that band's energy passes
  between the lines.

Use the production channels for photometry and colour only. For heating, use energy-faithful
channels (`twilight.py:234-302`).

The single wavelength ordering for all layers (`solved_optics.py:131`) is a further correlated-k-type
assumption, checked only on slant beams.

### Earth-control convergence

Terluna reports the Earth draft-to-standard broadband change through −18° as 82%. It notes that
deeper Earth twilight needs importance sampling in the Monte Carlo (`numerical_checks.json`;
`SOLVED_COLUMN.md:81-85`).

Finding:
- **The 82% is an interpolation artefact.** It occurs at −5°, between the draft grid's 2° nodes,
  where linear interpolation in solar elevation fails for a flux that falls about threefold per
  degree. The same happens at −3° (48%) and −1° (12%).
- **At shared nodes the change grows with depth:** 0.1–4% down to −6°, then 8.5% at −12°, 23% at
  −18° and 66% at −30°.
- **The other checks agree.** Earth's full-spectrum Monte Carlo is unresolved at −6° and empty at
  −12°, and the legacy Earth spots show resolved errors of 3–5% at −3°.
- **So Earth twilight below about −3° is not converged in either generation.** The Moon converges
  because its twilight varies on a scale of √(2H/R) ≈ 13.5°, against Earth's 2.9°.
- This matters for Earth–Moon comparisons in twilight, not for the lunar ledger.

### Provenance gap

Finding:
- The ledger's sky-batch cache key and its input record hash `solved_transport.py` and
  `solved_optics.py`, but not `solver.py` (`twilight.py:310-312`; `twilight.json` `inputs`).
- Yet `transport`, `ray_path`, `bracket` and `interpolate` live in `solver.py`.
- At 186b294, `solver.py` is unchanged since commit 36f124e, so the cached batches match the code. A
  later edit to `solver.py` would not invalidate them.

## Runnable copy: dependency chain

### Transport only (what the ledger needs from the solver)

- **Modules:** `solver.py`, `solved_transport.py`, `atmospheres.py` (imported by `solver.py`), and
  Terluna's `shared/constants.py` with `shared/constants.json` (for AU and SUN_RADIUS).
- **Requirements:** numpy ≥ 2.0 (`np.trapezoid`) and numba ≥ 0.61
  (`illumination/sky/requirements.txt`).
- **Versions Terluna's runs used:** Python 3.13.7, numpy 2.3.3, numba 0.68.0 with llvmlite 0.50.0,
  scipy 1.16.2 (`solved_sky.json` `software`; the research drive's `venvs/optics`).
- **Input:** a dict of layer optical depths:
  - `height` in metres, at levels;
  - `scattering` and `absorption`, layers × channels;
  - `energy`, `xyz`, `wavelength` and `band`, carried through to the outputs.

### Optics (`solved_optics.fine_optics`)

- **Modules:**
  - `illumination/surface_light/model.py`;
  - `illumination/cloud_light/model.py`, for `MolecularColumn.path` only (`layer_lengths` duplicates
    it);
  - `colour_matching.py`, `shared/provenance.py`, `shared/external_inputs.py`;
  - `atmosphere/radiative_convective/{optics, spectroscopy, shortwave, longwave, thermodynamics,
    climate, ck, fetch_inputs}.py`;
  - `atmosphere/middle_atmosphere/{photolysis, equilibrium, chemistry, fetch_inputs}.py`;
  - scipy, for netCDF reading, Voigt profiles and sparse solves.
- **Committed Terluna data:**
  - `atmosphere/middle_atmosphere/results/middle_atmosphere.json`, with the profiles and cases of
    `moon_1.2atm_titania_stack`, `moon_1.2atm_titania_stack_ts298` and `earth_control`;
  - `protection/spectra/shield_transmission.json`;
  - every file `solved_optics.inputs()` hashes (`solved_optics.py:37-52`); these must exist.
- **External data**, fetched and hash-pinned, not in Git:
  - from `atmosphere/radiative_convective/inputs.json`: HITRAN H₂O lines (two files, 70 MB) and O₂
    lines, partition sums, the CIA files (N₂–N₂, O₂–N₂, O₂–O₂, N₂–H₂O), MT_CKD 4.3, and TSIS-1 HSRS at
    stride 100;
  - from `atmosphere/middle_atmosphere/inputs.json`: the JPL-2010 cross sections from the MPI-Mainz
    atlas.
  - `inputs()` verifies whichever pinned files are present and stops on a mismatch
    (`solved_optics.py:53-64`).

### Checks and products

- **Modules:** `solved_reference.py`; `reference_mc.py`, for `rotate_direction` (it imports the
  legacy solver); `solved_checks.py`; `solved_sky.py`.
- **Data:** the cached fields in Terluna's `research/runs/optical_comfort/spherical/`, on the
  research drive.

### Cost

| Run | Time | Documented settings; record |
|---|---|---|
| Moon standard solve | 2,945 s, plus 17 s continuation | `NUMBA_NUM_THREADS=3 OPENBLAS_NUM_THREADS=1` (`SOLVED_COLUMN.md:101-110`); times from `worlds.*.settings` |
| Moon draft solve | 406 s | as above |
| Earth standard / draft | 534 s / 85 s | as above |
| Ledger, 12 batches | 2,229 s, about 40 minutes on 6 threads | `twilight.json` `channels.solve_seconds`; `climate/gcm/README.md:971` |

Fine-optics caches are 0.2–0.4 GB each. Set the thread variables explicitly on shared machines.

## Room for improvement, by value

1. **Benchmark against an independent spherical code.** The in-house Monte Carlo shares the physics
   and the shell-length routine.
   - Run a full-spherical Monte Carlo on the solved lunar column: MYSTIC in libRadtran's spherical
     mode, SASKTRAN or SCIATRAN.
   - Use three to five wavelengths and Sun elevations of +30°, +10°, 0°, −6° and −12°. Compare
     radiance, surface flux and layer absorption.
   - Add a published spherical Earth-twilight case.
   - This would turn "self-consistent" into "verified by an independent code". It is still not
     physical validation.
2. **Energy-faithful channels in the sky product.** Add an energy or absorption term to the
   reduction budget, or adopt the ledger's faithful channels in `solved_optics`. Until then, state in
   `SOLVED_COLUMN.md` and in the product's reading rule that the channels serve photometry only.
3. **A self-contained copy with honest caches.**
   - Add `solver.py` to the ledger's batch key.
   - Replace `MolecularColumn.path` with `layer_lengths`.
   - Let `inputs()` take a manifest instead of Terluna paths.
   - Carry the Bruneton notice.
4. **Scattering-order tails.** Increments decay geometrically (0.914 per order at 366 nm), so
   estimate and record the tail, or accelerate it, instead of stopping at a cap. Extend the stopping
   test to the full solar-elevation range used downstream.
5. **A bound on the scalar error.** Add a vector single-scattering or vector Monte Carlo comparison at
   a few spots, and use the depolarised Rayleigh phase function.
6. **Twilight interpolation.** Interpolate positive fields in log space in solar elevation, or tie the
   grid spacing to √(2H/R). This fixes the Earth control and changes little for the Moon.
7. **Blue-channel energy closure at standard quality** (2.2%). Find which ledger term carries it
   (diffuse escape moves most). Then refine the radial and angular grids near the top, or compute the
   escape by formal integration.
8. **Optical layering near the ground.** For grazing beams, split the 7.3-km bottom layer or use
   exponential profiles within layers.
9. **Refraction**, using the Bouguer invariant n·r·sin z along rays, for sunrise and sunset timing
   and deep twilight.
10. **Non-Rayleigh scatterers and horizontal structure.** Aerosol, cloud and day–night contrast need a
    different angular representation or a non-axisymmetric solver. Take this on only if the GCM or
    CM1 show that these terms matter for the twilight heating.
