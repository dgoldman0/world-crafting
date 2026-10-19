# Waterworlds: correctness, limits and room for improvement

Notes on the lab's tools for low-gravity waterworlds, `python/atmosphere/waterworlds/`, written for plan stage 9,
the reproduction of Arnscheidt, Wordsworth and Ding (2019), "Atmospheric Evolution on Low-gravity Waterworlds",
ApJ 881, 60 ([../lab/design/waterworlds.md](../lab/design/waterworlds.md)), whose arXiv source (1906.10561v2,
sha256 8d416543…f451) was read on 2026-10-19; equation numbers here are the arXiv version's. `body.py` sizes the
worlds and `escape.py` computes their isothermal wind; the steam column, its radiating surfaces and the energy
balance follow.

## What the tools compute

- **Bodies.** `Waterworld` follows the relation R/R⊕ = 1.258 (M/M⊕)^0.302 of Sotin, Grasset and Mocquet (2007), for
  waterworlds of 0.01 to 1 Earth mass, so that surface gravity grows as M^0.396 and fixes the world; 40% of its mass
  is water, as in the paper. Earth's mass is GM⊕/G and its radius 6,371 km, values the paper leaves unstated, on
  which 1.48 m/s² gives 0.02679 Earth masses and 2.3 m/s² gives 0.0816, against the paper's 0.0268 and "≃ 0.08".
- **The wind.** `escape.py` follows the paper's isothermal transonic wind (section 2.4): the sound speed at the
  surface temperature, the critical radius (eq. 8), the mass flux through a surface of saturated steam (eq. 9), the
  world's loss and its water's lifetime (eqs. 10 and 11), and below the critical radius the integrated wind equation
  solved in full (eq. A3), the speed with its kinetic term dropped (eq. A4) and the wind's inertia against gravity
  (eq. A5). `lifetime_gravity` finds the gravity, within the size relation's range, at which a world keeps its water
  a given time at a given surface temperature; at 273 K and 10⁹ years, that gravity is the paper's transition from
  planet-like to comet-like worlds. A factor on the square of the sound speed, 1 for the paper's equations as
  printed, serves the comparison below.
- **Choices the paper leaves open.** The vapour pressure is the column's own, Wagner and Pruß (2002) over liquid
  water and Wagner et al. (2011) over ice; steam at the surface is an ideal gas; a year is a Julian year.

## How they were checked

The tests (`python/atmosphere/tests/test_waterworlds.py`) check the masses the size relation gives at the paper's
gravities. They check that the full wind solves the wind equation (eq. 7) by central differences to 10⁻⁶, reaches
the sound speed at the critical radius and meets eq. A3's solution in 50-digit arithmetic to 10⁻⁹ on both sides of
each switch between its three methods (Lambert's W, a series at W's branch point near the critical radius, and the
exponential far below it); that eq. 9's flux equals the full wind's at the surface to 10⁻¹², the kinetic term it
drops there being smaller still; that eq. A4's speed is the full wind's times exp(−(w/w_c)²/2) at every radius; and
that eq. A5 is the inertia of eq. A4's wind. They check the code against the paper's equations; the comparison with
the paper's results follows.

## The printed escape against the paper's figures

By the paper's equations 9 to 11 as printed, with its stated inputs, its worlds keep their water far longer than its
figures and text report: 600 times longer at the paper's transition, 8,000 to 36,000 times at the lifetimes marked
on Figure 3's axis, and 60,000 to 310,000 times at Figure 5's. The transition world, at 1.48 m/s² and 273 K, keeps
its water 6.0 × 10¹¹ years, where the paper's transition has 10⁹, and the 10⁹-year lifetime meets 273 K at
1.29 m/s², 0.0190 Earth masses. At 2.3 m/s² the lifetimes on the axes of Figures 3 and 5, read from the images'
pixels against their ticks before stage 9 digitises them, fall at these surface temperatures (computed on
2026-10-19 and checked by the change's reviewer):

| At 2.3 m/s², about 0.08 Earth masses | 10¹¹ years | 10⁹ years | 10⁷ years |
|---|---|---|---|
| Figure 3's lifetime axis | 403 K | 445 K | 498 K |
| Figure 5's lifetime axis | 388 K | 427 K | 476 K |
| The printed equations | 497 K | 554 K | 628 K |
| The square of the sound speed taken as 4/3 kT/m | 397 K | 442 K | 500 K |

With the square of the sound speed taken as 4/3 kT/m, the adiabatic value for water molecules whose vibrations stay
unexcited, Figure 3's lifetimes fall within 6.4 K of the computed ones and the transition at 1.52 m/s². With a factor
of 1.272 the transition falls at the paper's 1.48 m/s²; matching Figure 3's three lifetimes takes factors of 1.31 to
1.34, and Figure 5's 1.37 to 1.42, so that no single factor matches every figure, at one gravity and one star. The
authors' code may have taken an adiabatic sound speed, and their figures may come from different stages of the work.
The change's reviewer tried other readings of the paper and found none that gives its numbers: a constant factor on
the density, the water or the year (the ratios above vary by a factor of 500), a density in grams, a loss through the
critical sphere, half the mass in water, or a factor on the sound speed together with one on the density. Reading the
authors' code, or asking them, would settle the cause. The evidence is a calculation of the printed equations against
values read from the paper; the author chooses how stage 9's acceptance check treats the difference
(`lab/design/plan.md`).

## Limits

- The wind keeps the surface temperature out to the critical radius, the paper's upper bound on the loss (section
  2.4). A wind heated by the star's high-energy light and cooling as it rises is planned for stage 10.
- In eq. A4 the kinetic term is dropped at every radius, which lowers the speed by the factor exp(−(w/w_c)²/2), 0.92
  at the paper's limit for it, w/w_c = 0.4.
- Saturated steam's density is 1.07 times an ideal gas's at 450 K, 1.15 at 500 K, 1.32 at 554 K and 2.09 at 628 K
  (Wagner and Pruß 2002). Taken in eq. 9, the real density moves the printed equations' temperatures in the table to
  495, 551 and 617 K, the row at 4/3 kT/m by 2 K at most, and leaves the transition, at 273 K, where it is.
- Sotin and colleagues gave the relation for ocean planets half water by mass, by their abstract as search indexes
  quote it (the lab has yet to read the paper itself), while the paper puts 40% of each world's mass in water; the
  radius is then that of a world of 50% water.
- Within the relation's range, at the sound speeds compared here, the critical radius lies above the surface at
  every temperature below water's critical point; the flux refuses a world whose critical radius lies at or below
  its surface, where eq. 9 has no derivation.

## Room for improvement

- The sound speed of the authors' calculation, from their code or their word.
- A real-gas density of saturated steam at the surface.
