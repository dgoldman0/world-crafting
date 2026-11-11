# ExoPlaSim's low-I/O output holds the humidity from the start of each interval

The report posted to ExoPlaSim's developers on 2026-11-11 as issue #71 of `github.com/alphaparrot/ExoPlaSim`, under
the title "Low-I/O output: `hus` holds the humidity at the start of each output interval in place of the interval
mean". Terluna's climate work found the fault on 2026-10-27 (branch `domain/climate`, commit 984606a5), and the lab
read the code on 2026-11-11. On the day of posting each line reference was checked against the pinned 3.4.2 archive,
the three source files were found identical on upstream's `master`, and the run settings were read from the namelists
of Terluna's runs. The defect log's A10 gives the lab's account, with the reader's rule the lab's tools follow.

**Outcome.** ExoPlaSim's maintainer closed the issue the same day as redundant: upstream's pull requests #53 and
#54, open since 2026-08-19, already state the fault and fix it, #54's change to `gridpointd` with a comment that
names the cause. The check ahead of posting had searched upstream's issues and had read #54 for its fix alone. The
fix is unmerged, so the released model and `master` keep the fault, and the lab's handling of it stands. The file
stays as the record of what was sent; a later report to any upstream project follows a reading of its open pull
requests as well as its issues. The issue's text follows as posted.

---

**Summary**

With `NLOWIO = 1` and `NQSPEC = 1` (both defaults), `outaccu` adds `sqout` to its sum at every step, while `gridpointd` recomputes `sqout` once per output interval. Each `hus` record therefore holds the humidity at about the start of its interval, beside temperature, pressure, winds and fluxes that are interval means. `sqout` also starts each model call at zero, so the first record after a restart can lose most of its vapour; in the runs examined it keeps about 2%.

**Where** (read in the 3.4.2 source from PyPI; the three files are identical on `master`)

`plasim.f90` line 3218, in `gridpointd`:

```fortran
      if (mod(nstep,nafter)==0 .and. nqspec == 1) then
       do jlev=1,NLEV
        zqout(:,jlev)=gq(:,jlev)/exp(gp(:))
        call gp2fc(zqout(1,jlev),NLON,NLPP)
        call fc2sp(zqout(1,jlev),sqout(1,jlev))
       enddo
       call mpsum(sqout,NLEV)
      endif
```

`outmod.f90` line 2556, in `outaccu`; `outsp` writes the sum as code 133:

```fortran
          aasqout(:,j) = aasqout(:,j) + sqout(:,j)
```

`sqout` is declared `= 0.0` (`plasimmod.f90` line 302), and the restart carries the sum `aasqout` (`plasim.f90` line 860) but leaves `sqout` itself out. The write test counts `nhcstp`, which restarts at 1 in each call (`plasim.f90` line 607), while the recompute test counts `nstep`, so every step ahead of a call's first recompute adds zeros to the sum. A call whose `nstep` starts on a multiple of `nafter` recomputes at its first step and writes a complete first record.

**In the output** (measured in the runs examined)

The column sum of `hus` can be set against `prw` (code 230, which `outaccu` sums at every step). A record's column vapour matched the average of that record's `prw` and the previous record's to 7.6 kg/m² rms, against 10.4 kg/m² for its own `prw`. With one model call per year, the first `hus` record of each year's file held about 0.02 of the second's vapour while `prw` stayed steady.

**Consequence**

The model's state is unaffected. Read as interval means, the `hus` records lag the other fields by half an output interval, and a long mean that includes a depleted first record is biased low. For existing output, the average of each record with the next, with each file's first and last records left out, estimates each interval's mean.

**Possible fix**

Recomputing `sqout` at every step in low-I/O mode would make `hus` an interval mean and complete the first record after a restart. Open PR #54 already contains that change:

```fortran
      if ((nlowio > 0 .or. mod(nstep,nafter)==0) .and. nqspec == 1) then
```

PR #54 builds on #53, which broadcasts `nlowio` so that every rank takes the same branch around the `mpsum`. Neither has been built or tested for this report. Alternatively, `outgp` could write `aadq`, the gridpoint sum that `outaccu` already keeps (`outmod.f90` line 2562), for `nqspec == 1` as well; the patched copy used for these runs writes that mean as a further field behind a switch.

**Setup**

ExoPlaSim 3.4.2 with gfortran 13.3 and Open MPI 4.1.6 on Linux: T21, 30-minute steps, `NSTPW = 143`, and one model call per year of 17,160 steps (120 records). The fault was found while adapting ExoPlaSim to a slowly rotating, low-gravity world. The runs used a patched copy; the excerpts above are from the unmodified source.

**Note**

This fault was found and written up with the help of an AI assistant (Claude), and each code reference above was checked against the 3.4.2 source.
