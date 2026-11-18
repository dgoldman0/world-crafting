# CM1's large-scale nudging climbs from its first window after a restart

A draft report to CM1's developer, George Bryan (NSF NCAR), for the author to review; nothing sends it. Before any
report goes, the CM1 forum's threads on large-scale nudging and the notes of any release after cm1r22.0 are read, and
the author decides whether to send it. The world-crafting lab found the defect on 2026-11-17 by reading cm1r22.0, the
archive whose sha256 begins `05f990bb`, while porting a coupling of the Terluna project's CM1 boxes, and found it in
Terluna's run logs; the lab's patch 12 fixes it (`models/cm1/README.md`, "The nudging's window after a restart";
defect log A12).

## Summary

After a restart, `lsnudge` nudges toward the first of its windows (`lsnudge_0001.dat`) and moves on by one window a
step until it reaches the window of the run's time. A run restarted N windows into its forcing therefore nudges its
wind, temperature and vapour toward N earlier windows over its first N steps, and parts from the run it continues.

## Where, in cm1r22.0

- `cm1.F`, line 3147: every run, a restart included, reads its windows by
  `call read_lsnudge(lsnudge_u,lsnudge_v,lsnudge_th,lsnudge_qv,sngl(mtime),zh)`; the argument `timenudge`
  (`lsnudge.F`, line 52) carries the run's time and is left unused.
- `lsnudge.F`, lines 413 and 414: after reading, `lsnudge_maxcount = lsnudge_count` and `lsnudge_count = 1`.
- `solve1.F`, lines 273 to 286: each step, with `timenudge = mtime+dt`, the count moves on by one window where
  `timenudge.gt.lsnudge_time2(lsnudge_count)`.
- `restart_write.F` keeps `ug` and `vg` for lsnudge (line 858 on) and no count of windows.

## Evidence

In the Terluna project's lunar box `box_near_side_sea_dgw`, run in segments of one day (86,400 s) with windows of 0.82
days, the log of the thirtieth segment, which starts at 2,505,600 s, moves the count on at each of its first 35 steps of
80 s, from window 2 to window 35, before it holds window 36, the run's own, for 539 steps. In the lab's compiled copy of
the block, a run restarted at 3,640 s with windows of 600 s and steps of 40 s climbs from the first window to the
seventh in six steps, where the run done whole holds the seventh. In a compiled lunar box of two hours with windows of
600 s, restarted at one hour, the restarted run nudged θ toward windows 2 to 7 over its first six steps where the run
done whole held the seventh, and parted from it in its state and output.

## Suggested fix and check

At the top of `solve1.F`, move the count on while `timenudge.gt.lsnudge_time2(lsnudge_count)` and
`lsnudge_count.lt.lsnudge_maxcount`, in place of the single step; or set the count by `timenudge` at the end of
`read_lsnudge`, which already receives the run's time. Either leaves the restart files as they are, and gives the
present count wherever each window spans a step or more. A run of two segments with a restart between them, with
several windows before the restart, then writes the output of the run done whole.
