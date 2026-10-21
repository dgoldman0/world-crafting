# Corrections found after the first released draft

The author has yet to decide whether the paper gets a v1.1. These are the findings, made after the first released
draft (tag `paper-v1`, PDF 1ce697ac), that a revision would carry, each with the passage it touches and its source.

| Passage in v1 | What v1 says | What later work found | Source |
|---|---|---|---|
| `sections/verification.tex`, line 72 (claim V08), and the table in `sections/appendix.tex`, line 147 | RRTMG cools 990 cloud-free columns of the 45° N ring by 4.5, 8.5 and 10.2 W/m² more than the correlated-k model at 0–1.8, 1.8–6.5 and 6.5–13.7 km | Under `eqtset = 2`, CM1 stores its radiative tendencies at constant volume, and Terluna's readers took them as rates at constant pressure, about 38–40% too large. Read so, and with the ground's temperature at the lowest level, CM1's longwave comes within 0.013 K a day of the correlated-k model in every layer (0.2–1.3 W/m²), and RRTMG run offline within 0.02 K a day | Terluna's correction of 20 October 2026 and its follow-up, `domain/atmosphere` fe49ad9 (conventions in `climate/crm/cm1_output.py`) |
| `sections/results.tex`, lines 113–126, and `sections/next.tex`, line 27 | Of the 3.7 K by which CM1's lowest 1.8 km at 45° N stays warmer than the GCM's, the GCM's longwave over-cooling beyond CM1's is worth about 1.5 K, at the ring's estimated 4 W/m² per kelvin | With CM1's radiation read at constant volume, Terluna's corrected budget puts the GCM's over-cooling near 2.7 K of the 3.7 K, at 3.9 W/m² per kelvin; the ring's heat budget had counted radiation 40% too large | The same |
| Every CM1 result from Terluna's rings and boxes, the near-ground gap above among them | CM1's boundary layer as run | CM1's simple boundary layer (`ipbl = 2`), which every ring ran, hands the solver its tendencies multiplied by the air's density: the boxes' boundary layer took 1.32–1.35 times the surface's evaporation and 1.46–1.51 times its sensible heat. The near-ground gap, the ring's heat budget and CM1's rain may all move; Terluna's reruns with the fix will size them | Terluna, `domain/climate` 13e7123; the lab's check in cm1r22.0, `lab` 0a2496f (`models/cm1/upstream-ipbl2-density.md`) |
| `notes/cm1.md`, lines 45–46 | RRTMG cools the air 0.15, 0.12 and 0.11 K a day more than the correlated-k model | As the first row | As the first row |

The third row interacts with the first two: the corrected near-ground gap waits for Terluna's reruns with both
fixes, so a revision would take its numbers from those reruns.
