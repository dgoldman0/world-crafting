# Low-gravity waterworlds: the flagship study

At the author's direction of 2026-10-19, the lab's flagship study is a family of low-gravity waterworlds, after
Arnscheidt, Wordsworth and Ding (2019), "Atmospheric Evolution on Low-gravity Waterworlds", ApJ 881, 60
(arXiv:1906.10561, version 2, read in full that day). The Open Moon, compared with Terluna's results, remains the
lab's test case ([plan.md](plan.md)). The author set three aims, in order:

1. to evaluate the ensemble against the paper's findings, on worlds under steam alone, the class the authors
   studied;
2. to give the same worlds Gaean air, nitrogen and oxygen with water as its condensable, and find where that air
   lasts;
3. where it lasts too briefly, to work out the shield that would keep it.

The lab maps the family in one dimension first, then runs ExoPlaSim, CM1 and the wave model at a few worlds chosen
from the maps.

## The reference study

Arnscheidt and colleagues modelled a world whose water makes up 40% of its mass, under an atmosphere of water vapour
alone in equilibrium with its ocean, the temperature following the vapour curve at every height:

| Part | In the paper |
|---|---|
| Size | R/R⊕ = 1.258 (M/M⊕)^0.302, the relation of Sotin et al. (2007) for waterworlds of 0.01 to 1 Earth mass (eq. 1) |
| Radiation | A one-dimensional line-by-line model (Schaefer et al. 2016; Wordsworth et al. 2017) on HITEMP2010's water lines, truncated and accurate below 1,000 K, under clear skies, with clouds' reflection folded into a surface albedo of 0.2 |
| Radiating surfaces | The heights at which the optical depth from the top reaches one, averaged over the outgoing spectrum for the emitting surface and over a blackbody at the star's temperature for the absorbing one, with gravity falling as (r_s/r)² (eqs. 3 and 4) |
| Energy balance | (r_SW/r_s)² ¼ (1 − A) F − (g r_s + L) Φ = (r_LW/r_s)² F_out, solved for the surface temperature over gravity and starlight (eq. 2) |
| Escape | An isothermal, transonic wind at the surface temperature, an upper bound on the loss; the water lasts M_water/(4π r_s² Φ) (eqs. 5–11) |
| Stars | The Sun, a blackbody at 5,772 K, and AD Leonis, a blackbody whose temperature, luminosity and mass the paper leaves unstated |

Their findings are stage 9's comparisons:

- as the surface warms, the emitting surface gains area on the absorbing one, so the outgoing radiation keeps rising
  and these worlds meet no runaway greenhouse (Figure 3, at g = 2.3 m/s², about 0.08 Earth masses);
- a habitable zone, bounded by the 273 K contour and a water lifetime of 10⁹ years, is at most about 0.08 AU wide
  around the Sun and 0.008 AU around AD Leonis, its inner edge set by escape (Figure 4);
- the zone closes, by the authors' conservative estimate, at g ≈ 1.48 m/s², 0.0268 Earth masses, essentially the
  same for both stars; below that gravity, liquid water lasts less than a billion years at every distance from the
  star, and the authors call the change the transition from "planet-like" to "comet-like" worlds (Section 3.3);
- a snowball whose star brightens generally skips the long-lived habitable state, except at very low ice albedos
  (Figure 5, for a Sun-like star, at g = 2.3 m/s² and ice albedos of 0.25, 0.32 and 0.4).

The authors published no code or data tables with the paper, so stage 9 compares with its stated numbers and the
curves of its Figures 3 to 5. They set aside carbon dioxide's cycling, ocean chemistry and three-dimensional
dynamics, treat clouds through the albedo alone and the stars as blackbodies, and name more detailed escape and
three-dimensional cloud models as further work (Sections 2.1, 2.3, 4.1 and 4.3).

## The worlds

| Parameter | Values | Basis |
|---|---|---|
| Mass | About 0.016 to 0.1 Earth masses, g from 1.2 to 2.5 m/s² | The paper's Figure 4 |
| Water | 40% of the mass | The paper |
| Star and distance | The Sun at 0.9 to 1.15 AU; AD Leonis at about 0.145 to 0.18 AU | The paper's Figure 4 |
| Air | Steam alone; Gaean air | The author's direction of 2026-10-19; the Gaean air's composition and pressure are a choice for stage 11 |
| Rotation, in three dimensions | Locked to AD Leonis, turning once in about 36 days at 0.16 AU for a star of 0.42 solar masses, the seed's provisional mass; a stated day around the Sun | Proposed; the day around the Sun is a choice for stage 12 |
| Protection | None; then a shield where the Gaean air needs one | The author's direction of 2026-10-19; the lab proposes the least shield that keeps the air |

By the paper's relation, with Earth's air at 288 K for the scale height H and the horizon factor √(πR/2H):

| Mass (Earth masses) | Moon masses | g (m/s²) | Radius (km) | Escape speed (km/s) | H (km) | H/R | Horizon factor |
|---|---|---|---|---|---|---|---|
| 0.016 | 1.30 | 1.21 | 2,299 | 2.36 | 68.5 | 0.030 | 7.3 |
| 0.0268, the transition | 2.18 | 1.48 | 2,686 | 2.82 | 55.8 | 0.021 | 8.7 |
| 0.05 | 4.07 | 1.89 | 3,243 | 3.51 | 43.6 | 0.013 | 10.8 |
| 0.1 | 8.13 | 2.49 | 3,998 | 4.47 | 33.2 | 0.008 | 13.8 |

The Moon's escape speed is 2.38 km/s and Mars's 5.03 km/s. Below about 0.076 Earth masses H/R exceeds 0.01, where
the registry's thin-shell entry, B21, warns for both dynamical cores, and with horizon factors of 7 to 14, against
Earth's 35, every world of the family needs a curved-air ledger of its own (B13), as the Moon does.

The lab holds the family in two forms. It computes the one-dimensional survey over a grid of gravity and distance
within one product, as the authors computed theirs, and turns the few worlds chosen for the three-dimensional
models, the anchors, into world and scenario files of kind `illustrative`, each generated with its basis, as it
generates CM1's case families into explicit entries (architecture.md, "Specifications").

## The work, in order

1. **The reproduction** (plan stage 9). The lab rebuilds the paper's model in one dimension on its own
   radiative–convective column, whose non-dilute moist adiabat (Ding and Pierrehumbert 2016) holds from vapour-poor
   air to steam and which computes its heights with g = GM/r² (`python/atmosphere/radiative_convective/METHODS.md`).
   The stage adds hot water's lines, the radiating surfaces, the energy balance, the isothermal wind and the water's
   lifetime, and maps them as the authors did. Each difference from the paper's numbers and curves is listed with
   its cause, and an input the paper leaves unstated, such as AD Leonis's temperature, takes the value the author
   chooses, recorded with its source.
2. **The ensemble's physics on the steam worlds** (stages 10 and 11). The lab replaces the paper's simplifications
   with its own physics one at a time and measures how the maps change under each: measured or modelled stellar
   spectra, the Sun's TSIS-1 among them; escape driven by the star's X-rays and extreme ultraviolet, through stage
   10's tools; a wind that cools as it rises; and clouds beyond a fixed albedo. Around AD Leonis the star's brighter
   youth may strip such worlds of their water early, as the authors note (Section 4.1), so the lab follows the
   star's history of luminosity and of high-energy light.
3. **Gaean air** (stages 10 and 11). The lab then gives the same bodies Gaean air, holding their masses, water and
   orbits. Water condenses at a cold tropopause, and what passes it diffuses up to where its hydrogen escapes, while
   nitrogen and oxygen escape thermally, at rates the exobase's temperature sets, and as ions and the fragments of
   broken molecules. The lab maps four diagnostics apart for each star, since their boundaries may differ: liquid
   water at the surface, the water's lifetime, the lifetimes of the nitrogen and the oxygen, and a surface within the
   Gaean class's pressures and temperatures. A billion years is the first horizon, as the paper's is, and shorter and
   longer horizons are its sensitivities.
4. **Anchors in three dimensions** (stage 12). About three worlds for each star, chosen from the maps near the
   transition, inside the long-lived region and near its inner edge, run in Gaean air in ExoPlaSim: all ocean, over
   a slab ocean, locked to AD Leonis or turning around the Sun, their sunlight from the star's own spectrum. Each
   anchor's climate is compared with the survey's column at the same point. At one or two anchors CM1 resolves
   storms over the open ocean, under a star fixed in the sky where the world is locked, and SWAN computes the waves
   that the anchor's winds raise on the global ocean.
5. **Protection where it is needed** (stage 13). For each anchor whose Gaean air lasts less than the horizon, the
   lab finds the least attenuation of the star's ultraviolet, and the least shelter from its wind, that keep the
   air. It then designs the shield for a planet alone with its star: its station near the star–planet L1 point,
   where the star's light pushes on it as well, its size, its optics and its control. Terluna's designs for the
   Open Moon's shield and its loss response are the starting point.

## What the lab adds

- **Specifications** ([world_spec.md](world_spec.md)): rotation locked to the star, a surface all ocean and the
  star's GM, settled in stage 2; the water's share of the body's mass and air of steam alone, to come with stage 9.
- **ExoPlaSim's input writer** (stage 2, written): for an all-ocean world, ExoPlaSim's aquaplanet switch, with no
  surface files; for a world locked to its star, the synchronous mode and its substellar longitude, with PlaSim's
  own Sun clock; the star's light files from its own spectrum, checked on a seed waterworld of provisional values
  (`lab/worlds/waterworld-seed`); and, through patch 11, the ice-optics weights from that spectrum, which matter
  most around a red dwarf, whose light lies further into the near infrared than the Sun's.
- **The registry,** which refuses ExoPlaSim and CM1 for air whose main gas condenses, since both treat water vapour
  as a minor part of the air; a steam scenario runs in the one-dimensional column alone.
- **Tools in `python/`:** the steam column (stage 9), and Terluna's thermal column, exobase, escape and
  loss-response tools, brought over and generalised for any body and star (stage 10).
- **SWAN's adapter,** for the patched build in `models/swan/`, checked on the Open Moon against Terluna's wave
  records before it serves the anchors (stage 12).
- **Data,** each by pin after its rights review: hot water's lines from HITEMP, as the authors used; a spectrum of
  AD Leonis with its X-rays and extreme ultraviolet, and the history of its activity.

## Choices for the author, at their stage

- AD Leonis's temperature, luminosity and mass, which the paper leaves unstated (stage 9); stage 2's seed red dwarf
  takes provisional values until then.
- The reproduction's tolerances against the paper's numbers and its digitised curves (stage 9).
- The Gaean air's composition and pressure, such as Earth's at 1 atm or the Open Moon's at 1.2 atm (stage 11).
- The day of the worlds turning around the Sun, and the anchors themselves (stage 12).

## Possible later additions

- A three-dimensional model of steam, an air whose main gas condenses, for which the registry refuses ExoPlaSim and
  CM1.
- An ocean that carries heat sideways, beneath a locked world's day side.
- Water brought to a smaller rocky planet, with its changed mass, size and gravity.
- The Moon at 1.0 atm, Mars at 1 bar and a slowly rotating Earth-like planet (architecture.md, "Decisions").
