# CM1's simple boundary layer adds density-weighted tendencies

A draft report to CM1's developer, George Bryan (NSF NCAR), for the author to review and send. The Terluna
project's climate work found the defect on 2026-10-21 through closed heat and water budgets of CM1 boxes (Terluna,
branch `domain/climate`, commit 13e7123); the world-crafting lab checked the lines below against cm1r22.0, the
archive whose sha256 begins `05f990bb`, the same day.

## Summary

With `ipbl = 2`, the simple boundary-layer scheme hands the solver its tendencies of potential temperature, the
mixing ratios and the wind multiplied by the air's density, and the solver adds them as changes per second. The
scheme therefore heats, moistens and mixes the boundary layer by a factor equal to the density in kg/m³ more than
its fluxes imply.

## Where, in cm1r22.0

- `turb.F`, the block opened at line 2152 (`if(ipbl.eq.2)then`), calls `turbsz` for θ, qv, qc and qi (from line
  2182) and `turbuz` and `turbvz` for the wind, writing `thpten`, `qvpten`, `qcpten`, `qipten`, `upten` and `vpten`.
- `turbtend.F`: `turbsz` (line 449) ends its implicit branches with
  `turbz(i,j,k) = rho(i,j,k)*(dumz(i,j,k)-s(i,j,k))*rdt` (lines 686 and 697), and `turbuz` and `turbvz` with the mean
  of the two neighbouring densities times the change of the wind (lines 1541 and 2333).
- `solve1.F` adds the arrays as changes per second: `thten1(i,j,k) = thten1(i,j,k) + thpten(i,j,k)` (line 1208) and
  `qten(i,j,k,nqv) = qten(i,j,k,nqv) + qvpten(i,j,k)` (line 1500).
- The other boundary-layer schemes fill the same arrays with WRF's tendencies per second: YSU through
  `RTHBLTEN=thpten` (`turb.F`, line 2264), MYNN and MYJ through `tmp2d` (lines 2619 and 2817). For them the
  addition in `solve1.F` is consistent.

## Evidence

In Terluna's lunar boxes, under 1.2 atm of air at the Moon's gravity with a surface density near 1.4 kg/m³, the
boundary layer's budgets from CM1's own diagnostics showed the air taking 1.32 to 1.35 times the surface's evaporation
and 1.46 to 1.51 times its sensible heat, with the drag inflated alike. With the density divided out at the end of
the `ipbl = 2` block, the boundary layer's water came to 0.995 to 1.000 of the evaporation. On Earth, where the
boundary layer's air weighs about 1.0 to 1.2 kg/m³, the same lines would inflate the scheme's tendencies by up to
about 20%; that figure follows from the code and awaits an Earth case.

## Suggested fix and check

At the end of the `ipbl = 2` block in `turb.F`, multiply `thpten`, `qvpten`, `qcpten` and `qipten` by the inverse
density `rr`, and `upten` and `vpten` by the inverse of the mean density at their points, so that the arrays hold
changes per second, as the other schemes' do. A dry convective boundary layer over a fixed surface heat flux, run
with `ipbl = 2`, shows the defect and its fix: the column's heating should equal the surface's flux.
