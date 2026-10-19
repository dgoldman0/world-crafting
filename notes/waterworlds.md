# Waterworlds: correctness, limits and room for improvement

Notes on the lab's tools for low-gravity waterworlds, `python/atmosphere/waterworlds/`, written for plan stage 9,
the reproduction of Arnscheidt, Wordsworth and Ding (2019), "Atmospheric Evolution on Low-gravity Waterworlds",
ApJ 881, 60 ([../lab/design/waterworlds.md](../lab/design/waterworlds.md)), whose arXiv source (1906.10561v2,
sha256 8d416543…f451) was read on 2026-10-19; equation numbers here are the arXiv version's. `body.py` sizes the
worlds, `escape.py` computes their isothermal wind, and `steam.py`, `steam_optics.py` and `radiating.py` compute the
steam column, its absorption and its radiating surfaces; `balance.py`, `steam_table.py` and `maps.py` compute the
energy balance, the columns' table over gravity and surface temperature, and the contours over gravity and distance.

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
- **The steam column.** `steam.py` builds the paper's column of steam alone, saturated at every height (section
  2.3): the vapour pressure at the surface temperature at the bottom and the vapour curve above, over liquid water at
  or above 273.16 K and over ice below, up to a top at 0.01 Pa. Its levels lie on one grid of ten per decade, shared
  by every column, so that columns of any gravity and surface temperature share the states, and with them the
  cross-sections, of every layer above their lowest. Heights follow from hydrostatic balance with gravity falling as
  GM/r² (eq. 3), through the radiative–convective column's `column_from_levels`. Above the critical radius of the
  isothermal wind at the surface temperature the steam flows faster than sound, so a column ends at the last level
  below that radius where the grid's top lies beyond it: at 1.15 m/s², inside the paper's Figure 4, from about 450 K,
  and at 500 K near 1.3 Pa.
- **Its absorption.** `steam_optics.py` computes pure steam's absorption on two bands, 1 to 3,500 cm⁻¹ at 0.01 cm⁻¹
  and 3,500 to 25,000 cm⁻¹ at 0.05 cm⁻¹: HITRAN2020's water lines stronger than 10⁻³⁰ cm per molecule at 296 K,
  403,685 of them, self-broadened, as Voigt profiles cut 25 cm⁻¹ from their centres less their value there, with
  MT_CKD 4.3's self continuum. Up to 2 bar the radiative–convective column's multi-mesh line sum serves, its points
  within 0.4% of a direct sum on the thermal band's grid and 0.9% on the stellar band's. Above it, where steam's
  Lorentz widths pass about 0.5 cm⁻¹ and the multi-mesh sum's far wings, expanded in (γ/d)², err further, keeping
  only 27 to 85% of the lines' absorption at 26 bar, by window, every line is summed directly on the band's grid.
  Scattering enters through the albedo alone, as in the paper. A cache keeps each layer's cross-sections under a key
  of the lines, the partition sums' and the continuum's files, the band, the method and its version, and the layer's
  state.
- **The radiating surfaces.** `radiating.py` finds, wavenumber by wavenumber, the height at which the vertical
  optical depth from the top reaches one, the absorber growing with pressure within a layer and the height with its
  logarithm, and takes the surface's height, 0, where the whole column stays thinner. The emitting surface's height
  is the mean of those heights over the outgoing spectrum, and the absorbing surface's their mean over the star's
  whole Planck curve (eq. 4). The outgoing spectrum is the column's plane-parallel flux at its top, from the
  radiative–convective column's longwave solver, four Gauss angles and a source linear in optical depth, over a black
  surface. Each mean is reported with the share of its weight whose depth reaches one within the top layer, where the
  absorber above the column's top would raise the height further.
- **The energy balance, the table and the contours.** `balance.py` gives the instellation that holds a surface at
  T_s (eq. 12): the emitting surface's factor times the outgoing longwave, plus the power the wind carries away,
  (g_s r_s + L) Φ, over the absorbing surface's factor times (1 − A)/4, with A = 0.2; the steady temperatures at an
  instellation, every crossing of that curve; and for the paper's step to an ice albedo below 273 K (eq. 13) the
  steady temperatures of two branches, the water's curve at 0.2 holding at and above 273 K and the ice's at its own
  albedo below, so that no interpolation runs across the jump. `steam_table.py` computes the columns' outgoing
  longwave and factors once over a grid of gravity and surface temperature, as the paper does (section 3), for
  several stars' temperatures: it fills the optics' cache with each layer state once, runs each column in a worker
  of its own with a line of progress as it ends, records a failed column with its error, and writes the table to the
  store at `products/steam-table/<key>/table.json`, its key covering its inputs and its producer, the code of every
  module that makes it and the versions of Python, numpy and scipy, and its header stating its evidence. `maps.py`
  computes, gravity by gravity and for a star given by its temperature and its flux at 1 AU, the distance at which a
  world stands at 273 K, or at the temperature at which its water lasts a given time, interpolating the instellation
  linearly in T_s along the table; a temperature outside the table, or a lifetime no temperature from 150 to 640 K
  gives, yields NaN.
- **Choices the paper leaves open.** The vapour pressure is the column's own, Wagner and Pruß (2002) over liquid
  water and Wagner et al. (2011) over ice; steam is an ideal gas at every height; a year is a Julian year. The
  column's top, its levels, its bands and their steps, the lines' floor, the continuum and the surface's emissivity
  of one are the lab's choices; the paper names its line list, HITEMP2010 truncated for use below 1,000 K, which the
  lab adds when the author has downloaded it. Starlight beyond 25,000 cm⁻¹, where water has no lines, counts at the
  surface's height: it is 12.2% of a 5,772 K Planck curve and 0.6% of a 3,400 K one, and averaging over the computed
  range alone would raise the Sun's absorbing height by 14%. The paper names the heat of vaporisation in its escape
  term and leaves its value unstated; over liquid water L is the heat of vaporisation by the Clapeyron equation with
  the saturated liquid's and vapour's densities of Wagner and Pruß (2002), within 0.1% of the steam tables from 373
  to 600 K, where the ideal gas's Clausius–Clapeyron slope runs 1.6% high at 373 K, 17% at 500 K and 84% at 600 K,
  which would raise the wind's power at 1.1 m/s² and 600 K by 28%; over ice, below 273.16 K, L is the heat of
  sublimation, which adds about 7%, near 1 W/m², to the wind's power at 1.1 m/s² and 270 K.

## How they were checked

The tests (`python/atmosphere/tests/test_waterworlds.py`) check the masses the size relation gives at the paper's
gravities. They check that the full wind solves the wind equation (eq. 7) by central differences to 10⁻⁶, reaches
the sound speed at the critical radius and meets eq. A3's solution in 50-digit arithmetic to 10⁻⁹ on both sides of
each switch between its three methods (Lambert's W, a series at W's branch point near the critical radius, and the
exponential far below it); that eq. 9's flux equals the full wind's at the surface to 10⁻¹², the kinetic term it
drops there being smaller still; that eq. A4's speed is the full wind's times exp(−(w/w_c)²/2) at every radius; and
that eq. A5 is the inertia of eq. A4's wind. They check the code against the paper's equations; the comparison with
the paper's results follows.

The steam column's tests (`python/atmosphere/tests/test_steam_column.py`) check that the saturation temperature
inverts the vapour curve to 10⁻¹² over ice and liquid; that columns share every level above their lowest layer and
hold no layer thinner than half a grid step; that a column follows the vapour curve, stands taller than with
constant gravity, and holds Δp/g in its layers at their middle heights, or Δp/g_s at the surface's gravity with the
same heights; that a column ends below the wind's critical radius where the grid's top lies beyond it; that a grey
isothermal column reaches an optical depth of one exactly where the absorber above holds 1/σ; that the Planck mean
of a uniform height is that height, and of a step the curve's share below it; and that a transparent column emits
its surface's σT⁴ from the surface, through both bands to 10⁻⁸. Against the column's multi-mesh line sum the direct
sum agrees to 0.5% at 300 and 393 K, and over 1,200 to 1,260 cm⁻¹ at 500 K and 26 bar it keeps the third of the
lines' absorption the multi-mesh sum loses; below 2 bar the optics give the multi-mesh sum and the continuum, and
the cache's key follows the continuum. Once, on 2026-10-19, the direct sum was also compared with a brute-force Voigt
sum over 1,200 to 1,260 cm⁻¹, and again by the change's reviewer: it agrees to 1.4 × 10⁻⁵ at 2 bar and to
9 × 10⁻⁸ at 26 bar, where the multi-mesh sum's points err by up to 100%.

The energy balance's tests (`python/atmosphere/tests/test_balance_and_maps.py`) check that the instellation holds
eq. 2 with the wind's power; that the heat of vaporisation meets the steam tables at 373, 500 and 600 K to 0.1% and
over ice is the ice curve's heat of sublimation; that the steady temperatures are every crossing of a table's curve,
an exact meeting counted once, and that the hysteresis's branches keep their states on their sides of 273 K; that
the instellation takes each star's own absorbing factor and refuses a star the table lacks; that the 273 K contour
of blackbody worlds meets its closed form to 10⁻⁴ and a temperature outside the table yields NaN; that the lifetime
temperatures invert the wind, giving 273 K at the printed transition, 1.29 m/s², and NaN where no temperature from
150 to 640 K gives the lifetime; that a grid stops at or below its end; that a table reads back as written and its
key follows its inputs and producer; and that the table, computed in one process and in two, holds each column's
surfaces, a capped column among them, as the column alone gives them, the second computing no cross-section
anew.

The column's numerical choices were tested once at 2.3 m/s², at 300 and 450 K, against finer settings, with the
layers' masses at the local gravity. The base settings give an outgoing longwave of 246.77 and 240.95 W/m², emitting
factors of 1.0920 and 1.3947, and absorbing factors of 1.0140 and 1.1628 for a star at 5,772 K and 1.0302 and
1.2555 for one at 3,400 K; the finer settings change them by at most:

| Setting | Outgoing longwave | Emitting factor | Absorbing factors |
|---|---|---|---|
| Thermal band's step, 0.01 to 0.005 cm⁻¹ | −0.015 W/m² | +1.5 × 10⁻⁵ | 0 |
| Stellar band's step, 0.05 to 0.02 cm⁻¹ | 0 | 0 | −1.5 × 10⁻⁵ at most |
| Levels, 10 to 20 per decade | +0.13 W/m² | −4.4 × 10⁻⁵ at most | −3.0 × 10⁻⁵ at most |
| Top, 0.01 to 0.001 Pa | −0.011 W/m² | −4 × 10⁻⁶ at most | +7.2 × 10⁻⁵ at most |
| Angles, 4 to 8 | +0.021 W/m² | 0 | 0 |

Each moves the outgoing longwave by 0.06% or less and the factors by less than 10⁻⁴, against differences from the
paper of about 1%. The share of the emitting surface's weight whose depth reaches one within the top layer stays
below 2 × 10⁻⁴, and the absorbing surface's at most 5 × 10⁻⁴; those shares count too few, since the gas above the top
holds 3.9 times the top layer's mass, and the change with the top, at most 7.2 × 10⁻⁵, measures the top's effect. The layers' masses at the surface's gravity, a choice of physics in place of a numerical setting,
raise the outgoing longwave by 2.5 W/m² at 300 K and 8.4 W/m² at 450 K, to 249.3 and 249.4 W/m².

## The radiation against the paper's Figures 2 and 3, a first look

Read from the images' pixels against their ticks on 2026-10-19, before the digitiser reads whole curves, the
paper's scaling factors for a world of 0.12 Earth masses around the Sun (Figure 2) compare with the lab's columns,
the layers' masses at the surface's gravity:

| Surface temperature | 300 K | 400 K | 500 K | 600 K |
|---|---|---|---|---|
| Emitting surface, the paper | 1.059 | 1.197 | 1.313 | 1.41 |
| Emitting surface, the lab | 1.066 | 1.210 | 1.333 | 1.446 |
| Absorbing surface, the paper | 1.009 | 1.068 | 1.143 | 1.21 |
| Absorbing surface, the lab | 1.010 | 1.073 | 1.155 | 1.234 |

The paper's values at 600 K are read at 598 K, where its curves meet the axis. In Figure 2's right panel the ticks
stand where the plotted quantity would be r/r_s, labelled with its square, while in its left panel the altitude
labels stand where the same quantity, at the same rows, would be (r/r_s)², so that at 400 K the emitting surface
stands at 195 km by the left panel and at 398 km by the right. The right panel's reading agrees with the lab's
heights, 422 km there, with the figure's caption, which puts the emitting surface at 260 K, a temperature the lab's
column reaches at 430 km, and with the paper's own energy balance in Figure 3; the left panel's labels are the slip.

At 2.3 m/s² around the Sun, with an albedo of 0.2 and the escape of the printed equations, which adds nothing below
450 K, the instellation holding each surface temperature (Figure 3, W/m²) compares as follows:

| Surface temperature | 260 K | 280 K | 300 K | 350 K | 400 K | 450 K |
|---|---|---|---|---|---|---|
| Expanding surfaces, the paper | 1,156 | 1,277 | 1,326 | 1,402 | 1,445 | 1,477 |
| Expanding surfaces, the lab, the surface's gravity | 1,169 | 1,291 | 1,341 | 1,419 | 1,464 | 1,492 |
| Expanding surfaces, the lab, the local gravity | 1,167 | 1,284 | 1,329 | 1,394 | 1,428 | 1,445 |
| No expansion, the paper | 1,140 | 1,232 | 1,239 | 1,239 | 1,239 | 1,243 |
| No expansion, the lab, the surface's gravity | 1,155 | 1,240 | 1,247 | 1,247 | 1,247 | 1,247 |
| No expansion, the lab, the local gravity | 1,153 | 1,233 | 1,234 | 1,223 | 1,213 | 1,205 |

At 450 K the paper's curves already hold its own escape, stronger than the printed equations', which lifts its
curve without expansion to 1,243 W/m². With the layers' masses at the surface's gravity the lab's instellation
without expansion stays flat above 300 K, as the paper's does up to 400 K, 0.6% above it, and with expansion runs
1.0 to 1.3% above the paper's; with the masses at the local gravity the curve without expansion falls 2.4% between
300 and 450 K. The authors therefore appear to have computed their optical depths at the surface's gravity and their
heights by eq. 3, and the reproduction does the same, keeping the local gravity as one of the lab's own changes for
stage 11. The lab's heights run 6 to 8% above the paper's at 400 to 500 K, which raises its factors by 0.005 to 0.02;
the line lists (HITRAN2020 here, HITEMP2010 there), the continuum's version and the spectral sampling are candidate
causes, and rerunning with HITEMP's lines will test the first. Without the continuum the lab's outgoing longwave at
2.3 m/s², on the thermal band, rises to 329 to 352 W/m² with the layers' masses at the local gravity and to 330 to 357
at the surface's, against the paper's flat 248, so the paper's column also holds a continuum, or line wings, of
comparable strength.

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

- MT_CKD's self continuum is fitted near Earth's temperatures, and its temperature exponents, from 1.4 to 6.4 below
  3,500 cm⁻¹ and up to 10.3 above, are extrapolated over the column's 184 to 600 K. The continuum sets about
  100 W/m² of the outgoing longwave at 2.3 m/s².
- Steam is an ideal gas at every height; by the real densities below, a rough estimate of the change's reviewer puts
  the emitting height 1 to 2% too high at 500 K, and more at 600 K.
- The columns are capped at the wind's critical radius where their grid's top lies beyond it, so at low gravity and
  high temperature the gas above the cap, which the paper's hydrostatic heights would include, is left out; the
  share of each mean reaching the top layer reports where that matters.
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
