# Geography: correctness, limits and room for improvement

Notes on the heights above the geoid, the seas and the lakes that the lab's surfaces start from:
`python/geography/` (`topography.py`, `basins.py`, `atlas.py`, `drainage.py`, `nomenclature.py`), the lab's
general versions of Terluna's lunar tools at 186b294 (`python/provenance.json` notes each change), and
`lab/worldlab/geography.py`, which reads a world's files through the data manifest and takes the geoid's terms
from its specification.

## What the tools compute

- **Heights above the geoid.** A global simple-cylindrical PDS3 image gives radii less a reference sphere, as
  LOLA's LDEM labels define them; a PDS SHADR table gives the gravity field's fully normalised coefficients, its
  GM and its reference radius. Each is read through its label, which names its file, sample type, unit,
  scaling, offset and projection. The geoid adds to the field, from degree 2 to the world's
  `surface.geoid_degree`, the centrifugal potential of the world's sidereal rotation and, where the world states
  `surface.tide`, the permanent tide of a host fixed in its sky, scaled by 1 + k2. The geoid is synthesised on
  the heights' own grid.
- **Seas.** One common level floods a share of the surface (`basins.level_for_area`), every closed depression
  below it counting as water; the seas are its 8-connected regions, joined across the 0/360 seam and the poles.
  The atlas lists the seas and lakes, the islands and, given the gazetteer's names, the flooded maria.
- **Lakes.** The drainage routes a climate run's runoff over the heights by steepest descent, finds each closed
  depression's spill level by a priority flood, and fills a depression to its spill level where its inflow and
  the rain on its lake exceed the lake's open-water evaporation, or to the smaller lake whose evaporation
  balances its inflow.

## Checks

On the Moon (`lab/tests/test_geography.py`, LOLA's 16 pixels per degree, GL0420A to degree 330):

- the geoid's area mean lies within 0.5 m of zero, with the equator above 150 m and the poles below −250 m, the
  shape of the Moon's flattening;
- the lowest point, −8,451 m, lies in the floor of South Pole-Aitken, and the highest stands at 10,107 m;
- the heights on the sphere at the Chang'e 3 and 4 landing sites lie within 40 m of the published −2,640 m and
  −5,935 m;
- at 28% water the centres of Oceanus Procellarum and Maria Imbrium, Serenitatis, Crisium and Nectaris stand in
  one sea;
- the 28% level, −1,653.84 m, lies 0.36 m above Terluna's atlas (−1,654.2 m), and the 25% and 35% levels within
  Terluna's 10 m of its finer level table;
- the runoff of Terluna's run A28_dim5_moon, routed over the lab's heights, fills lakes over 10.33% of the
  surface, where Terluna's routing of the same runoff over its own heights filled 10.34%: 99.6% of Terluna's lake
  area is lake in the lab's routing, and the lakes' count, their closed count and volume and the rivers' discharge
  to the sea agree within 0.2% (27,916 lakes against 27,865, 2,500 closed against 2,495, 3.10 against 3.11
  million km³, 229,469 against 229,410 m³/s), within the test's 1%. On the lake cells both routings share, the
  lab's lake surfaces lie within 10 m of Terluna's over 99.2% of the area, by 0.3 m at the median; where a pass
  between depressions moves with the heights, a lake spills at another level, by up to 2.6 km over 0.05% of that
  area. Run over Terluna's own heights at Terluna's level, the lab's drainage gives Terluna's lake cells, levels,
  spills and channels byte for byte, and its channels' discharges within 0.004 m³/s (2026-10-18).

With Terluna's choices, degree 200 and Earth fixed over the sub-Earth point at the mean distance, the general
code's geoid on Terluna's 4-pixel grid agrees with Terluna's to 1 × 10⁻¹³ m (2026-10-18), and its readers return
LOLA's heights and GL0420A's coefficients identical to Terluna's.

## Choices and their sizes

Heights and geoids below compare on LOLA's 16-pixel grid, their rms weighted by area.

- **The geoid's degree.** GL0420A's label applies a Kaula constraint to its coefficients above degree 330, so
  the lab takes the field to 330, where Terluna took 200. Degrees 201–330 add 1.9 m rms to the geoid and 31 m at
  most; they raise the 28% level by 0.2 m and turn 2,792 of LOLA's 16.6 million cells (0.016% of the surface)
  between land and sea. On the lab's laptop, with threaded BLAS, the synthesis takes 4.6 s at degree 330 and
  1.5 s at degree 200, its arrays peaking at 0.55 GB.
- **The geoid's grid.** Terluna synthesised the geoid at 4 pixels per degree and interpolated it bilinearly to
  16; at degree 200 that erred by 0.17 m rms and 2.4 m at most against a synthesis on the 16-pixel grid.
- **The tide's mean.** The permanent tide is the time mean of the host's degree-2 potential in the body's frame,
  taken over the mean anomaly and over the perigee's angle from the node, which the orbit's precession turns
  through. The Moon's orbit, of eccentricity 0.0549 and inclined 6.687° to its equator (5.145° to the ecliptic
  and the equator's 1.5424° beyond it, as Cassini's laws set them), moves Earth about the sub-Earth point in the
  optical librations, and carries it nearer and farther. Against Earth held over the sub-Earth point at the
  orbit's mean 1/r³, 1/(a³(1 − e²)^{3/2}), the librations lower the tide's zonal coefficient by 2.0% and its sectoral
  by 1.9%, moving the geoid by −0.26 m at the sub-Earth and far points, +0.12 m on the limbs and +0.14 m at the
  poles, and the 28% level by 5 mm. Against Terluna's tide, Earth held over the sub-Earth point at the mean
  distance, the changes are −0.20 m, +0.09 m and +0.11 m.
- **The first lakes.** The Open Moon's first lakes are routed by the lab from a pinned runoff, Terluna's
  climatology of run A28_dim5_moon, where Terluna's lakes from that runoff were routed over Terluna's own heights,
  1.9 m rms and up to 31 m from the lab's; set on the lab's heights, 0.36% of Terluna's lake area would have its
  surface below the ground. That run's runoff has Terluna's routing to compare with; the design run
  A28_corrected_970's own runoff gives lakes over 10.44% of the surface in 24,481 bodies, and the chain's later
  links come from the lab's own runs. The routing takes 15 s and 2.1 GB on LOLA's 16-pixel grid.
- **k2.** The tide takes GL0420A's own k2 of 0.0248, which its solution held fixed when it left the permanent
  tide out of the degree-2 coefficients, so that the tide returns as the field removed it; GRAIL's estimate,
  0.02405 (`shared/constants.json`), would change the geoid by under 1 cm.

## Limits

- The filling is hydrostatic. Rainfall, runoff, evaporation, groundwater, erosion and the crust's response to
  the water's load then move each shoreline.
- LOLA's heights are in the mean-Earth/polar-axis frame and GL0420A in DE421's principal-axis frame; the 0.02°
  between them, 0.6 km at the surface, is ignored against the 33 km shortest wavelength of a degree-330 geoid.
- The Sun's permanent tide, zonal about the Moon's axis, is left out: −3.8 cm at the poles and +1.9 cm at the
  equator, with k2. So are the Moon's physical librations, which turn its axes by under 0.1°.
- The image reader takes pixel-registered global maps of east longitudes from 0, at whole pixels per degree,
  every sample present, in a file that holds the image alone, with its heights radii less a sphere. It refuses
  heights measured from an equipotential already, as MOLA's MEGDR topography is, and designed height fields for
  constructed worlds take a format of their own.
- The drainage is a steady annual balance at the climate model's resolution; channels follow the grid, and
  groundwater, infiltration and travel time are absent.

## Room for improvement

- A reader for MOLA's MEGDR heights and a gravity field for Mars (GMM-3 or JGMRO_120F, both SHADR tables), and a
  format for designed height fields.
- The Sun's permanent tide, should a case need the geoid to centimetres.
