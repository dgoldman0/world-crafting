# Waterworlds: correctness, limits and room for improvement

Notes on the lab's tools for low-gravity waterworlds, `python/atmosphere/waterworlds/`, written for plan stage 9,
the reproduction of Arnscheidt, Wordsworth and Ding (2019), "Atmospheric Evolution on Low-gravity Waterworlds",
ApJ 881, 60 ([../lab/design/waterworlds.md](../lab/design/waterworlds.md)), whose arXiv source (1906.10561v2,
sha256 8d416543…f451) was read on 2026-10-19; equation numbers here are the arXiv version's. `body.py` sizes the
worlds, `escape.py` computes their isothermal wind, and `steam.py`, `steam_optics.py` and `radiating.py` compute the
steam column, its absorption and its radiating surfaces, for which `hitemp.py` reads and cuts HITEMP2010's water
lines; `balance.py`, `steam_table.py` and `maps.py` compute the energy balance, the columns' table over gravity and
surface temperature, and the contours over gravity and distance; `figures.py` reads the paper's figures from the
images in its source and `comparison.py` sets the lab's results beside them.

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
  MT_CKD 4.3's self continuum. For the reproduction the optics take HITEMP2010's lines as `hitemp.py` cuts them, and
  with `hold` a layer warmer than 296 K takes the self continuum's coefficients at 296 K, its radiation term and
  density staying the layer's own (below). Up to 2 bar the radiative–convective column's multi-mesh line sum serves,
  its points within 0.4% of a direct sum on the thermal band's grid and 0.9% on the stellar band's. Above it, where
  steam's
  Lorentz widths pass about 0.5 cm⁻¹ and the multi-mesh sum's far wings, expanded in (γ/d)², err further, keeping
  only 27 to 85% of the lines' absorption at 26 bar, by window, every line is summed directly on the band's grid.
  Scattering enters through the albedo alone, as in the paper. A cache keeps each layer's cross-sections under a key
  of the lines, the partition sums' and the continuum's files, the continuum's hold, the band, the method and its
  version, and the layer's state.
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
- **The paper's figures.** `figures.py` reads the curves of the paper's Figures 2 to 5 from its arXiv source, which
  `fetch_inputs.py` restores by its sha256 into the git-ignored `inputs/`; since arXiv distributes the source under
  its non-exclusive licence, the lab keeps it outside Git and credits the values read from it to the authors. Each
  figure is an RGB image in a PDF, which the reader decodes from the PDF's bytes and calibrates axis by axis. A tick
  is found as the run of dark pixels nearest the middle of its label along the plot box's edge, translucent shading
  included, and a tick a curve hides is left out of the fit, linear in the labels, or in their square root for
  Figure 2's factors, which the reader refuses where it misses a tick by more than a pixel. A curve's points are the
  middles of the runs of its colour, column by column or row by row: the longest run, or the one nearest the last
  where a label in the line's colour stands beside it, a run that another curve crosses being left out. Figure 5's
  dotted arrows, where the snowballs thaw and the ocean freezes, are read as the columns their colour fills, and
  each snowball's last state as its curve extrapolated to its arrow. The reader writes the curves, with its code's
  hash, its environment and a statement of their evidence, to the store at `products/paper-figures/<key>/figures.json`.
- **The comparison.** `comparison.py` sets the lab's results beside the paper's figures at the same abscissas, the
  paper's curves read linearly between their points: Figure 2's factors from columns of 0.12 Earth masses computed
  directly; Figure 3's instellations with and without the expanding surfaces and its lifetimes; Figure 4's 273 K and
  10⁹-year contours for both stars, the transition and Ganymede's line; and Figure 5's ocean, the thawing of its
  snowballs and the ocean's freezing, at the paper's arrows. Each takes the wind's sound speed squared at kT/m, as
  printed, at 1.2722 kT/m, the value at which the transition falls at the paper's, and at 4/3 kT/m. The paper's AD
  Leonis takes the flux its own Figure 4 implies, the square of the ratio of the two stars' 273 K distances, 0.0242 of
  the Sun's, and a temperature of 3,400 K. The comparison goes to the store at
  `products/steam-comparison/<key>/comparison.json`, its key covering the table and figures it read, the optics' key,
  the Sun's flux, the red star's temperature and its producer, the code of every module it runs.
- **Choices the paper leaves open.** The vapour pressure is the column's own, Wagner and Pruß (2002) over liquid
  water and Wagner et al. (2011) over ice; steam is an ideal gas at every height; a year is a Julian year; the Sun
  gives 1,361 W/m² at 1 AU (shared/constants.json), on whose square root every distance from it depends. The
  column's top, its levels, its bands and their steps, the lines' floor, the continuum and the surface's emissivity
  of one are the lab's choices; the paper names its line list, HITEMP2010 truncated for use below 1,000 K, which
  `hitemp.py` reads and cuts as the paper's model cut it (below). Starlight beyond 25,000 cm⁻¹, where HITRAN2020
  gives water no lines and HITEMP2010's kept lines hold 3 × 10⁻⁸ of their strength, counts at the surface's height:
  it is 12.2% of a 5,772 K Planck curve and 0.6% of a 3,400 K one, and averaging over the computed range alone would
  raise the Sun's absorbing height by 14%. The paper names the heat of vaporisation in its escape term and leaves
  its value unstated; over liquid water L is the heat of vaporisation by the Clapeyron equation with the saturated
  liquid's and vapour's densities of Wagner and Pruß (2002), within 0.1% of the steam tables from 373 to 600 K,
  where the ideal gas's Clausius–Clapeyron slope runs 1.6% high at 373 K, 17% at 500 K and 84% at 600 K, which
  would raise the wind's power at 1.1 m/s² and 600 K by 28%; over ice, below 273.16 K, L is the heat of
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

The figure reader's tests (`python/atmosphere/tests/test_paper_figures.py`) check that a PDF's image reads back byte
for byte and that two images, another colour space, a predictor or a stream of the wrong length are refused; that an
axis fits its ticks linearly or in the square root of its labels and refuses two ticks or a tick astray; that ticks
are found beside their labels or on the edge, one under a curve left out; that a curve takes its longest run, tracks
past a label in its colour and leaves out the runs another curve crosses; that a product reads back with NaN as null
and its key follows its source and producer; and, with the paper's source restored, that Figure 2 at 300 and 400 K,
Figure 3's curves at 300 and 400 K, its ticks and shading, Figure 4's contours at three points, its lines and the
contour's lowest gravity, and Figure 5's ticks, band, arrows, curve ends and the ocean's temperatures at the arrows
read as recorded here. The comparison's tests (`python/atmosphere/tests/test_comparison.py`) check that the paper's
curves are read between their points and NaN beyond, that the red star's flux is the square of the ratio of its
273 K distance to the Sun's, that Figure 3's rows hold the balance at every factor, that Figure 5's snowballs thaw
where their branch reaches the thawing temperature into the ocean state the same instellation holds, found by
bisection, and, with the source restored, that the whole comparison runs and the transition, Ganymede's line and the
red star's flux stand as recorded.

The tests of HITEMP2010's lines (`python/atmosphere/tests/test_hitemp.py`) check that the lab's data manifest records
34 zips covering 0 to 30,000 cm⁻¹ without a gap and HITEMP2010's 114,241,164 lines; that records read field by
field, and that the cut keeps a line 2% over the floor at 1,000 K, drops one 2% short of it, one at 0 cm⁻¹ and one of
unknown lower-state energy, and sorts what it keeps; that the column's line sum integrates an isolated line at
1,000 K to the strength the cut takes, to 10⁻⁵; that zips of another layout, record length, molecule or isotopologue
code are refused; that the cut list is cached under a key that follows the zips' hashes and the cut, reads back with
the zips gone, and is rebuilt only from the zips of its record; that two processes cut as one does; and, where the
store holds the zips, that their first records read as HITEMP2010's, that the zip from 11,000 to 30,000 cm⁻¹ gives
its recorded cut, 622,109 lines kept with 19 of unknown energy among its records, that the store's cut list holds
the recorded count, and that the steam optics take it under a key of their own. With the continuum held, the optics
keep MT_CKD's own values at and below 296 K, and above it, at the continuum's 10 cm⁻¹ nodes, give the 296 K
coefficients times the layer's own density and radiation term to 10⁻¹²; a held table records its hold and its key.
The acceptance check's tests (`test_comparison.py`) hold a synthetic comparison to each row's tolerance, list a lab
value missing where the paper has one as a failure, place 450 K and 1.6 m/s² with the radiation, and find each value
outside a shifted bracket, the curves inside its widened form and a zone's width within its reading uncertainty; the
comparison refuses a table whose optics' key differs from its own. The column check's tests
(`test_column_check.py`) check that its columns are saturated over
1 bar of nitrogen, with the tropopause's water above it and gravity constant, the two gravities sharing their levels;
that its layer optics equal the column's own for water alone to 10⁻¹²; that it takes the first line list as its
reference, weaker lines letting more out; and, where a PyRADS checkout stands beside the store, that PyRADS's
columns take its 60 levels up to 10⁻⁴ of the surface's pressure, saturated over liquid water at 250 K, with a uniform
stratosphere. The sampling test's tests (`test_sampling.py`) check that its grid runs from 1 cm⁻¹ to five Wien peaks
in 5,000 points and that a grey column emits from the same height on that grid as on the lab's bands.

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
causes, and rerunning with HITEMP's lines will test the first, though their added opacity would raise the lab's
heights further. Without the continuum the lab's outgoing longwave at 2.3 m/s², on the thermal band, rises to 329
to 352 W/m² with the layers' masses at the local gravity and to 330 to 357 at the surface's, against the paper's
flat 248, so the paper's column also holds a continuum, or line wings, of comparable strength.

## The comparison with the paper's Figures 2 to 5

`comparison.py` ran on 2026-10-19 on the table `products/steam-table/23c1facbc05b5e7b/table.json` in the store
(sha256 36b66c6b…, 1,232 columns at 1.1 to 2.6 m/s² and 220 to 600 K, the layers' masses at the surface's gravity,
computed in 33 minutes on six processes with none failed) and on the figures as read by `figures.py`
(`products/paper-figures/e3a0471a01b233ca/figures.json`, sha256 7208144e…), and wrote
`products/steam-comparison/8ef344804c9e1ae0/comparison.json` (sha256 915dfb90…). The Sun gives 1,361 W/m² at 1 AU, a
value the paper leaves unstated, and the paper's AD Leonis 0.02417 of it, the square of the ratio of the two stars'
273 K distances in Figure 4, with a temperature of 3,400 K; that flux carries the paper's own ratio of the two stars'
absorbing factors near 273 K, which the lab's columns put 0.5 to 1.3% apart, so the AD Leonis rows lean on Figure 4
itself.

The radiation stands where the first look found it. The lab's emitting factors for Figure 2's world run 0.006 to
0.030 above the paper's from 300 to 598 K and its absorbing factors 0.001 to 0.019. At 2.3 m/s² the lab's
instellation with the expanding surfaces runs 1.0 to 1.6% above the paper's from 260 to 450 K, the most at 265 K,
and without them 0.6 to 0.7% above from 280 to 400 K and 1.1 to 1.6% above at 260 to 275 K; at 440 to 450 K the
paper's curve without expansion already holds its own escape. In the escape, the printed equations and the paper's
figures part, and a sound speed near the adiabatic one brings the lab within reach of the figures:

| | The paper | Printed, kT/m | 1.2722 kT/m | 4/3 kT/m |
|---|---|---|---|---|
| Transition, m/s² (Figure 4) | 1.481 | 1.292 | 1.480 | 1.520 |
| Widest habitable zone around the Sun, AU, at its gravity | 0.085 at 2.1 | 0.108 at 1.8 | 0.087 at 2.1 | 0.084 at 2.2 |
| Widest around AD Leonis, AU | 0.0086 at 1.9 | 0.0105 at 1.7 | 0.0086 at 1.9 | 0.0083 at 2.0 |
| 10⁹-year contour around the Sun at 2.4 and 1.6 m/s², AU | 0.961, 1.004 | 0.945, 0.938 | 0.955, 0.993 | 0.957, 1.006 |
| Instellation without expansion at 2.3 m/s², 470, 480 and 490 K, W/m² | 1,262, 1,295, 1,365 | 1,247 at each | 1,252, 1,258, 1,271 | 1,267, 1,290, 1,337 |
| The ocean's temperature after each snowball thaws, ice albedos 0.25, 0.32 and 0.4, K (Figure 5) | 296, 424, 495 | 297, 425, above 600 | 297, 425, 518 | 297, 425, 500 |

The paper's text gives the widest zones as about 0.08 and 0.008 AU. With the square of the sound speed at 4/3 kT/m,
the lab's 10⁹-year contour lies within 0.0052 AU of the paper's around the Sun from 1.6 to 2.4 m/s² and within
0.0007 AU around AD Leonis, though below 1.6 m/s² it parts further, 0.024 AU at 1.4 m/s². Its widest zones come
within 0.002 and 0.0003 AU of the paper's, and its instellation without expansion within 0.4% of the paper's at
470 and 480 K and 2.1% below it at 490 K, where the paper's escape climbs faster still. By the printed equations
the transition falls at 1.29 m/s², the zones widen by about a quarter, the instellation stays flat where the
paper's climbs, and the snowball at an ice albedo of 0.4 thaws into an ocean hotter than the table's 600 K. Below
1.5 m/s² the paper's 273 K contour turns sunward, to 1.012 AU at 1.3 m/s², as the power its escape carries grows;
the lab's contour there lies at 1.026 AU by the printed equations and at 1.000 AU at 1.2722 kT/m, so that the paper's
bend, too, points to an escape stronger than printed.

Figure 5 is compared at the paper's own arrows, whose distances the reader takes from the image, and at the
temperatures where the paper's snowball curves end beside them, 270.6 to 272.1 K, short of the 273 K at which the
lab's branches thaw by definition. There, the lab's snowballs thaw 0.005 to 0.006 AU nearer the Sun than the
paper's, and its ocean freezes 0.007 AU nearer, at the paper's 275.1 K, as the lab's instellation near 273 K, 1.1 to
1.6% above the paper's, would place them. The ocean the lab's snowballs thaw into is the same on both counts: an
instellation that both branches share cancels from it, and at 4/3 kT/m it stands within 1 K of the paper's after the
two warmer snowballs and 6 K above it after the coldest, near 500 K, where the escape sets the curve. At 273 K the
lab's snowballs thaw 0.010, 0.008 and 0.010 AU nearer and into oceans 7, 10 and 7 K warmer than the paper draws.
Ganymede's line, at 1.428 m/s² in the paper, lies at 1.436 m/s² for Ganymede's mass, 1.482 × 10²³ kg, on the size
relation with the lab's Earth.

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
| The printed equations | 497 K | 554 K | 627 K |
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
values read from the paper; by the author's choice of 2026-10-19, stage 9's acceptance check compares both (below).

## The acceptance check

The author set stage 9's acceptance check on 2026-10-19 (`lab/design/plan.md`), and its tolerances on the radiation
come from outside the comparison, which the lab had already run. Yang et al. (2016) ran seven radiation codes on the
same columns of Earth-like air, 1 bar of nitrogen with 376 ppmv of CO₂ and saturated water on a moist adiabat under a
200 K stratosphere, at surface temperatures of 250 to 360 K, under the Sun and under a 3,400 K blackbody standing for
an M dwarf; their two line-by-line codes, SMART and LBLRTM, came up to 3% apart in the instellation that holds a
surface temperature. The author took that 3% as the tolerance on the instellation of the paper's columns of steam,
which run to 600 K. The tolerance on distances, which go as the inverse square root of the instellation, is half of
it, and so is the tolerance on each of Figure 2's radiating-surface factors, which enter the balance as a ratio, the
emitting factor over the absorbing one. The escape's tolerance comes from the paper's own figures, as the lab's fits
read them: they need sound speeds whose squares run from 1.27 to 1.42 kT/m, and the lab is held to that spread, each
of the paper's curves bound by the escape lying between the lab's at its two ends. Every number that depends on the
escape is compared twice, by the equations as printed and at 4/3 kT/m; the check passes on the second, and the
printed equations' departure is recorded as a finding. Under ASME V&V 20, a standard for validation against
experiment, each difference is reported beside a combined uncertainty, and the lab borrows that form for a
comparison of two codes: the uncertainty of reading the paper's figures is under 0.1%, and the lab's numerical
error, by the convergence checks above, about 0.1%. On the HITRAN2020 table of 2026-10-19 the comparison gives:

| What | Tolerance | The lab on HITRAN2020, at 4/3 kT/m |
|---|---|---|
| Instellation that holds a surface temperature at 2.3 m/s² (Figure 3) | 3% | 0.6 to 1.6% above the paper's up to 400 K; with expansion, within 2.0% up to 495 K |
| Distances: the contours from 1.6 m/s² up (Figure 4) and the arrows of Figure 5 | 1.5% | within 0.85%; the arrows 0.58 to 0.65% |
| Each radiating-surface factor of Figure 2 | 1.5% | 0.1 to 2.1% above, over 1.5% for the emitting factor from 500 K up and for the absorbing factor at 598 K, 1.54% |
| The escape: the lifetimes' temperatures (Figure 3) and the transition (Figure 4) | between the lab's results at 1.27 and 1.42 kT/m | 4/3 lies inside the range, the temperatures within 1.6% of the paper's and the transition 2.6% above; the comparison holds 1.2722 and 4/3 kT/m, and its rerun adds 1.42 |

Below about 1.6 m/s², and above about 450 K at 2.3 m/s², the escape sets the curves and its row applies; there
Figure 3's curve without expansion falls 8.3% below the paper's at 505 K. AD Leonis takes the paper's implied flux,
so the paper's 273 K contour fixes the star's flux, and the 10⁹-year contour and the zone's width test the lab. The
survey of stage 11 takes the star's measured values, 3,414 K and 0.0227 of the Sun's luminosity, which would move
its contours by about 3%.

`comparison.acceptance` applies the check to a comparison and writes it into the product. The radiation rows hold
the lab at 4/3 kT/m to their tolerances: Figure 3's instellation up to 450 K at 2.3 m/s²; the distances of the
Sun's 273 K contour and of both stars' 10⁹-year contours from 1.6 m/s² up, as the table above places them, with
Figure 5's arrows; and each factor of Figure 2. Each row gives its worst difference and where it lies, the
uncertainty of reading the figures, under 0.1%, and the lab's numerical error, about 0.1% by the convergence checks
above, and it fails where the lab lacks a value the paper has. AD Leonis's 273 K contour from 1.6 m/s² up, to which
its flux is fitted, is reported apart. The escape row holds the paper's values that the escape sets between the
lab's at 1.2722 and 1.42 kT/m: the lifetimes' temperatures, the transition, the temperature above which Figure 5's
waters are short-lived, Figure 3's curves above 450 K, Figure 4's contours below 1.6 m/s², the coldest snowball's
thawed ocean and both stars' widest zones. After the results on HITEMP2010's lines (below), the author decided on
2026-10-20 that the row passes on the bracket widened by the radiation's tolerance for the curves, which carry the
radiation's offset as well, so that the offset counts once, and that a value outside it by less than its reading
uncertainty agrees with the paper, as ASME V&V 20 has it. A zone's width, the difference of two distances each read
to 0.1%, has a reading uncertainty of 0.1% of their root-sum-square over the width. The plain bracket is
reported beside it, with the value nearest an end, and the same values by the printed equations are recorded as the
finding.

## HITEMP2010's lines

The author downloaded HITEMP2010's water lines from HITRANonline with their own sign-in on 2026-10-19: 34 zips,
3.40 GB, holding the 114,241,164 lines HITEMP gives for water from 0 to 30,000 cm⁻¹ in HITRAN's 160-character
records. The lab's data manifest records each zip's size and sha256 after a review of its rights
(`lab/data/manifest.toml`, entry `hitemp2010-h2o`; HITRANonline's HITEMP page states no terms of redistribution, so
the zips stay in the store, outside Git), and the store keeps them at `data/<digest>/`. The paper's model, as
Schaefer et al. (2016) describe it, drops every line whose strength at 1,000 K falls below 10⁻³⁰ cm/molecule, cuts
the rest 25 cm⁻¹ from centre and, outside MT-CKD's temperature range of validity, holds the continuum at its value
for the warmest temperature given. The lab's MT_CKD 4.3 continuum weakens above its reference temperature, 296 K,
by its own exponents, so for columns warmer than about 300 K the continuum is a second candidate cause of the lab's
offset; the colder columns, where the offset is largest, 1.1 to 1.6% at 260 to 275 K, lie below 296 K at every
level, and a held continuum leaves them as they are. The lab proposes to hold MT_CKD 4.3's self continuum at 296 K,
the one temperature its file gives. Schaefer and colleagues also computed their spectra on 5,000 points from 1 cm⁻¹
to five times the Wien peak of the surface's Planck curve, and whether the paper's runs kept that grid is unstated.

On 2026-10-19 `hitemp.py` cut the zips on four processes. Of the 114,241,164 lines it kept 6,617,956, from 0.072 to
29,661.8 cm⁻¹, 99.5% of them of the main isotopologue, and cached them in the store
(`caches/hitemp-lines/7d5cc459f2d2bca3.npz`, 476 MB). By a floor of 10⁻³⁰ at 296 K, the lab's HITRAN2020 files, from 0
to 25,000 cm⁻¹, hold 403,685 water lines; the cut at 1,000 K keeps sixteen times as many. Nineteen lines of H₂¹⁷O
and H₂¹⁸O between 11,800 and 14,420 cm⁻¹ carry HITRAN's −1 for an unknown lower-state energy, which leaves their
strength without a temperature scaling; eleven of them would pass the floor, and the cut drops all nineteen,
10⁻¹¹ of the kept lines' strength at 296 K. Of the lines kept, 76,483, holding 2.5% of their strength at 296 K, give
a temperature exponent of zero or below for their air-broadened width, which the steam optics apply to the
self-broadened width, as they do for HITRAN's lines.

On 2026-10-20 the author approved the continuum's hold, as the lab reads Schaefer and colleagues' sentence: the
warmest temperature MT_CKD 4.3's file gives is its reference, 296 K, and the hold keeps the self continuum's
coefficients there, the radiation term and the density staying the layer's own, as the file keeps the coefficients
apart from both. The change's reviewer measured how far the other readings would move the held continuum at
1,000 cm⁻¹: holding the radiation term at 296 K as well raises it by 7% at 450 K and 18% at 600 K, and holding the
whole of it, the density included, by 62% and 140%, while the hold itself stands 10.6 and 54 times above MT_CKD 4.3's
own values there. The author also approved 3% as the tolerance of the check on the radiative–convective column's own
columns, which `column_check.py` makes: it builds saturated columns of water over 1 bar of nitrogen at 250 to 360 K,
at 9.8 m/s² and at the Moon's gravity, to the description of the column's validation against PyRADS
(`radiative_convective/validation.json`), and computes their outgoing longwave with the column's own lines, grid
and continuum, then with HITEMP2010's lines, beside the outgoing longwave the validation records on PyRADS's own
profiles.

## The reproduction on HITEMP2010's lines

The table on HITEMP2010's lines with the continuum held ran on 2026-10-20 (`products/steam-table/4cfc4b1d6e241978/
table.json`, its 1,232 columns all computed). Filling its cache took 12,205 s on seven processes, the 58 layer states
above 2 bar, summed directly over HITEMP's 6.6 million lines, taking about 300 s each on one core, and its columns
about 30 minutes more. The radiation barely moves. At 2.3 m/s² the outgoing longwave rises by 0.04%, from 249.38 to
249.47 W/m² at 450 to 600 K; the emitting factors keep their fourth decimal and the absorbing factors move by up to
0.12%, and by up to 0.51% across the whole table, at 1.1 m/s². The line list and the continuum's version, two of the
causes the first look named, therefore account for almost none of the lab's offsets from the paper: the columns'
radiating surfaces sit high, where the steam is colder than 296 K, and there HITEMP's hot lines add little while the
held continuum equals MT_CKD's own.

The paper's spectral grid gives the same emitting factors as well. `sampling.py` sampled the lab's cross-sections
for Figure 2's world at Schaefer and colleagues' 5,000 points from 1 cm⁻¹ to five times the Wien peak, taken as the
peak of the Planck curve in wavenumber, 1.96 cm⁻¹ per kelvin, and its emitting factors stayed within 0.0004 of those
on the lab's bands at every temperature (`products/steam-sampling/f37063474887d1a3/
sampling.json`). One candidate remains untested, the model's top: Schaefer and colleagues ran 30 layers up to 1 Pa,
where the lab's column runs to 0.01 Pa, and a top at 1 Pa caps the heights of the strongest lines' cores, which would
lower the emitting factor more than the absorbing one, and most at high temperatures, as Figure 2's differences run.
The test takes a few minutes on one core from the cache and waits for machine time.

On this table the acceptance check (`products/steam-comparison/b57e618e9da365c7/comparison.json`) passes three of
its four rows:

| Row | Tolerance | The lab on HITEMP2010, at 4/3 kT/m |
|---|---|---|
| Instellation (Figure 3), up to 450 K | 3% | worst 1.62%, at 265 K: passes |
| Distances (Figures 4 and 5) | 1.5% | worst 0.86%, the Sun's 273 K contour at 1.6 m/s²: passes |
| Radiating-surface factors (Figure 2) | 1.5% | the emitting factor 2.09% above the paper's at 598 K, the absorbing factor 1.49%, within it: fails on the emitting factor |
| The escape, between the lab's at 1.2722 and 1.42 kT/m | the bracket widened, within reading uncertainty | one value outside, AD Leonis's widest zone, by 0.15% against a reading uncertainty of 2.6%: passes |

The plain bracket leaves 13 of the escape row's 38 values outside, by up to 1.2%: Figure 3's curves at 455 to 470 K,
Figure 4's 273 K contours from 1.3 to 1.5 m/s², where the escape is weakest, and AD Leonis's widest zone. By the printed equations all 37 of the
values the escape sets, to which the lab's figures give a number, fall outside the paper's, by up to 32%. Stage 9's
check therefore fails on Figure 2's emitting factor alone.

The check on the radiative–convective column's own columns passes (`products/hitemp-column-check/88a4ac0336d0d3aa/
check.json`): with HITEMP2010's lines, the columns' outgoing longwave stands 0.08 to 0.23% above that with the
column's own, HITRAN2020's, at every temperature and at both gravities, against 3%. The rebuilt columns themselves
give 1.1 to 4.0% more outgoing longwave than the validation records on PyRADS's profiles, because PyRADS builds its
columns otherwise. PyRADS (Koll and Cronin 2018, MIT licence), checked out at the validation's commit c0a8647 in
`/media/projectspace/world-crafting-research/external/PyRADS`, saturates its air over liquid water at every
temperature, by a Clausius–Clapeyron curve of constant latent heat, where the column saturates over ice below
273.16 K, so that its stratosphere holds 2.2 to 2.8 times the water at 250 to 360 K, by the two columns' levels as
`column_check` builds them; its dry air is Earth's; and its 60 levels stop at 10⁻⁴ of the surface's pressure, 10 to
17 Pa. `column_check.py --pyrads` runs the check on PyRADS's own columns, built
by its own code; that run, about two hours on six processes, waits for machine time.

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
- Saturated steam's density is 1.07 times an ideal gas's at 450 K, 1.15 at 500 K, 1.32 at 554 K and 2.09 at 627 K
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
- Figure 2's factors with the column's top at 1 Pa, and the check on PyRADS's own columns, both waiting for machine
  time (above).
- A real-gas density of saturated steam at the surface.
