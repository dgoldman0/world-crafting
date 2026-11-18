!     A column of PlaSim's physics (climate/gcm/plasim_column.py): the time loop that takes the place of PlaSim's
!     master, and the dynamics' vapour tendency that takes the place of mkdqtgp.
!
!     PlaSim's own program starts the column: plasim_main calls mpstart and prolog of plasim.f90, compiled from the
!     lab's patched source with one latitude a process (plasim_column_mpi.f90), so that prolog reads the GCM run's
!     namelists, surface files and restart at the row of the GCM's grid the column stands in. The column's master then
!     steps every grid point of that row through the physics in the order of gridpointd, the humidity fixer
!     (miscstep), the surface fluxes and vertical diffusion (fluxstep), the radiation (radstep, where nrad is on),
!     convection, condensation and clouds (rainstep), the land, sea, ice and slab sea (surfstep), the carbon cycle
!     (carbonstep) and the storm diagnostics (hurricanestep), and ends the program at the end of its loop, before
!     plasim_main reaches epilog. The state the physics sees comes from the GCM.
!
!     With nmode 1 the state starts from the GCM's at the column's first step and steps on under the dynamics'
!     tendencies of each window of the GCM's forcing (patch 21), which the GCM writes as the storage of the state its
!     physics sees less its physics' tendencies. With nscheme 1, the default, that state steps forward, by the step
!     times the window's tendencies and the physics' own, so that over each window the column's storage equals the
!     GCM's wherever its physics equals the GCM's, and with windows of one step the column retraces the GCM's states.
!     With nscheme 2 it steps on PlaSim's leapfrog with Robert and Asselin's filter (spectrala and spectrald), the
!     window's tendencies in place of the adiabatic step. With nmode 2 each step's state is the GCM's at that step,
!     and the column's physics can be set beside the GCM's step for step. Each step writes the state the physics saw
!     and what the physics made of it to column_output in the layout of the GCM's plasim_column (patch 21 of the
!     lab's series), at the grid points of the row the column was asked for.
!
!     The lab's own file, distributed, as ExoPlaSim is, under the GNU GPL version 3.

      module colforce
      use colmod
      integer :: nwin = 0                    ! the forcing's windows (nmode 1) or steps (nmode 2)
      integer :: ncols = 0                   ! the grid points of the row written to column_output
      integer, allocatable :: icol(:)        ! their places in the row
      real :: cdqt(NHOR,NLEV) = 0.           ! the dynamics' vapour tendency mkdqtgp hands Kuo's scheme (kg/kg/s)
      integer, parameter :: NIN = 46, NOUT = 47
      end module colforce

!     ================
!     SUBROUTINE MASTER
!     ================

      subroutine master
      use colforce
      use rainmod, only: nstorain
      real :: zxs(NHOR,NLEV,4)     ! the state the physics sees: temperature, vapour and the two winds
      real :: zxsp(NHOR)           ! and the surface pressure's log
      real :: zx(NHOR,NLEV,4)      ! the leapfrog's present state (nscheme 2)
      real :: zxp(NHOR)
      real :: zxm(NHOR,NLEV,4)     ! its filtered state a step back
      real :: zxmp(NHOR)
      real :: zxn(NHOR,NLEV,4)     ! the filtered state being formed
      real :: zxnp(NHOR)
      real :: zd(NHOR,NLEV,4)      ! the window's dynamics' tendencies
      real :: zdp(NHOR)
      real :: zp(NHOR,NLEV,4)      ! the physics' tendencies of the step
      real :: zgq(NHOR,NLEV)       ! the vapour tendency in gqdt's units, as gridpointd forms it
      real :: zpin(NHOR)           ! the surface pressure as given (Pa)
      real :: zps                  ! the GCM's psurf
      real, allocatable :: zall(:) ! a part's values at the output's grid points
      integer :: iwin, ileft, jstep, ioff

      if (nrestart /= 1) call mpabort('column: the column starts from a GCM restart, plasim_restart')
      if (nqspec /= 1) call mpabort('column: the column takes spectral humidity, NQSPEC 1')
      if (l_aero > 0) call mpabort('column: the column takes no aerosols, L_AERO 0')
      if (nstratosponge > 0) call mpabort('column: the column takes no stratospheric cooling, NSTRATOSPONGE 0')
      if (nkits > 0) call mpabort('column: the column takes no initial short steps, NKITS 0')
      if (nstorain > 0) call mpabort('column: the column takes no stochastic rain, whose numbers PlaSim draws by &
     &process, NSTORAIN 0')

!     PlaSim's step, as master sets it

      deltsec  = day_24hr / mtspd
      deltsec2 = deltsec + deltsec
      delt     = TWOPI / ntspd
      delt2    = delt + delt
      call updatim(nstep)
      nstep1 = nstep
      nhcstp = 1

      open(NIN,file='column_input',form='unformatted',status='old',iostat=io)
      if (io /= 0) call mpabort('column: column_input is missing')
      read(NIN) nwin, ncols
      if (ncols < 1 .or. ncols > NHOR) call mpabort('column: the output takes 1 to NHOR grid points')
      allocate(icol(ncols))
      read(NIN) icol
      if (minval(icol) < 1 .or. maxval(icol) > NHOR) call mpabort('column: an output grid point lies off the row')
      read(NIN) zps
      psurf = zps
      open(NOUT,file='column_output',form='unformatted')

      if (nmode == 1) then
       read(NIN) zxs, zpin
       zxsp(:) = log(zpin(:))
       read(NIN) ileft
       read(NIN) zd, zdp
       iwin = 1
       do while (ileft == 0 .and. iwin < nwin)       ! windows of no steps, the first with output at every step
        iwin = iwin + 1
        read(NIN) ileft
        read(NIN) zd, zdp
       enddo
!      The leapfrog starts from rest a step back, so that its first step gives the GCM's state
       zxm(:,:,:) = zxs(:,:,:) - deltsec2 * zd(:,:,:)
       zxmp(:)    = zxsp(:) - deltsec2 * zdp(:)
       zx(:,:,:)  = zxm(:,:,:)
       zxp(:)     = zxmp(:)
      endif

      do jstep = 1 , nsteps
       if (nmode == 1) then
        if (ileft == 0) then
         iwin = iwin + 1
         if (iwin > nwin) call mpabort('column: the forcing ends before the column')
         read(NIN) ileft
         read(NIN) zd, zdp
        endif
        ileft = ileft - 1
        if (nscheme == 2) then
!        The adiabatic step of spectrala, its tendencies the window's, and the filter's first part
         zxs(:,:,:) = zxm(:,:,:) + deltsec2 * zd(:,:,:)
         zxsp(:)    = zxmp(:) + deltsec2 * zdp(:)
         zxn(:,:,:) = pnu21 * zx(:,:,:) + pnu * zxm(:,:,:)
         zxnp(:)    = pnu21 * zxp(:) + pnu * zxmp(:)
        endif
        cdqt(:,:)  = zd(:,:,2) + zxs(:,:,2) * spread(zdp(:),2,NLEV)
       else
        if (jstep > nwin) call mpabort('column: the given states end before the column')
        read(NIN) zxs, zpin, cdqt
       endif

!      The state the physics sees, as gridpointd sets it

       dt(:,1:NLEV) = zxs(:,:,1)
       dq(:,1:NLEV) = zxs(:,:,2)
       du(:,1:NLEV) = zxs(:,:,3)
       dv(:,1:NLEV) = zxs(:,:,4)
       if (nmode == 1) then
        dp(:) = exp(zxsp(:))
       else
        dp(:) = zpin(:)
       endif
       gudt(:,:) = 0.
       gvdt(:,:) = 0.
       gtdt(:,:) = 0.
       gqdt(:,:) = 0.
       dudt(:,:) = 0.
       dvdt(:,:) = 0.
       dtdt(:,:) = 0.
       dqdt(:,:) = 0.
       call colwrite(1)

!      The physics, in gridpointd's order

       call miscstep
       call fluxstep
       if (nrad > 0) call radstep
       call rainstep
       call surfstep
       call carbonstep
       call hurricanestep

!      The physics' tendencies as gridpointd hands them to the spectral step, the vapour's with the fixer's part

       do jlev = 1 , NLEV
        zgq(:,jlev) = dqdt(:,jlev)*dp(:)/ww/psurf                       &
     &              + gqdt(:,jlev)
       enddo
       call colwrite(2)

       if (nmode == 1) then
        zp(:,:,1) = dtdt(:,1:NLEV)
        zp(:,:,3) = dudt(:,1:NLEV)
        zp(:,:,4) = dvdt(:,1:NLEV)
        do jlev = 1 , NLEV
         zp(:,jlev,2) = zgq(:,jlev) * ww * psurf / dp(:)
        enddo
        if (nscheme == 1) then
!        The state the physics sees, a step on
         zxs(:,:,:) = zxs(:,:,:) + deltsec * (zd(:,:,:) + zp(:,:,:))
         zxsp(:)    = zxsp(:) + deltsec * zdp(:)
        else
!        The diabatic step of spectrald and the filter's second part
         zx(:,:,:) = zxs(:,:,:) + deltsec2 * zp(:,:,:)
         zxp(:)    = zxsp(:)
         zxm(:,:,:) = zxn(:,:,:) + pnu * zx(:,:,:)
         zxmp(:)    = zxnp(:) + pnu * zxp(:)
        endif
       endif

!      The clock, as master advances it

       iyea  = ndatim(1)
       imon  = ndatim(2)
       nstep = nstep + 1
       nhcstp = nhcstp + 1
       mstep = mstep + 1
       call updatim(nstep)
       if (imon /= ndatim(2)) mstep = 0
      enddo

      close(NIN)
      close(NOUT)
      if (mypid == NROOT) write(nud,*) 'column: ',nsteps,' steps of row ',nrow
      stop

      contains

!     The state the physics sees (kpart 1) and what the physics made of it (kpart 2) at the output's grid points, in
!     the layout of coldump in plasim.f90 (patch 21)

      subroutine colwrite(kpart)
      integer :: kpart
      integer :: ihead(6)
      integer :: icount
      if (kpart == 1) then
       icount = 2 * ncols * NLEP + 2 * ncols * NLEV + ncols + 1
      else
       icount = 7 * ncols * NLEV + 2 * ncols * NLEP + 8 * ncols
      endif
      allocate(zall(icount))
      ioff = 0
      if (kpart == 1) then
       call colput(dt,NLEP)
       call colput(dq,NLEP)
       call colput(du,NLEV)
       call colput(dv,NLEV)
       call colput(dp,1)
       zall(ioff+1) = psurf
       ioff = ioff + 1
      else
       call colput(dtdt,NLEV)
       call colput(dqdt,NLEV)
       call colput(dudt,NLEV)
       call colput(dvdt,NLEV)
       call colput(dqt,NLEV)
       call colput(zgq,NLEV)
       call colput(dt,NLEP)
       call colput(dq,NLEP)
       call colput(dprc,1)
       call colput(dprl,1)
       call colput(dprs,1)
       call colput(devap,1)
       call colput(dshfl,1)
       call colput(dlhfl,1)
       call colput(dswfl(:,NLEP),1)
       call colput(dlwfl(:,NLEP),1)
       call colput(dcc,NLEV)
      endif
      ihead(:) = (/ nstep, kpart, ncols, NLEV, icount, nrow /)
      write(NOUT) ihead
      write(NOUT) zall
      deallocate(zall)
      end subroutine colwrite

      subroutine colput(pf,klev)
      integer :: klev
      real :: pf(NHOR,klev)
      do jl = 1 , klev
       zall(ioff+1:ioff+ncols) = pf(icol(:),jl)
       ioff = ioff + ncols
      enddo
      end subroutine colput

      end subroutine master

!     =================
!     SUBROUTINE MKDQTGP
!     =================

!     The dynamics' vapour tendency Kuo's scheme reads as the moisture's convergence. In the GCM, mkdqtgp brings the
!     adiabatic step's tendency of the spectral humidity, the vapour times the surface pressure, to the grid and
!     divides it by the surface pressure; the column takes it from its forcing in the same form, the vapour's
!     tendency plus the vapour times the tendency of the surface pressure's log, or with nmode 2 as the GCM gave it

      subroutine mkdqtgp
      use colforce
      dqt(:,1:NLEV) = cdqt(:,:)
      return
      end subroutine mkdqtgp

!     ===================
!     SUBROUTINE MAKEAREAS
!     ===================

!     The areas of the row's cells, for the carbon cycle's global means. utilities.f90, which a GCM on several processes
!     compiles, gathers every process's latitudes and sets the areas between the midpoints of the latitudes;
!     utilities_stub.f90, which the column compiles, reads latitudes that a process with one row lacks. Here the
!     Gaussian latitudes of the whole grid are found as prolog finds them, with inigau, and utilities.f90's formula
!     sets the areas

      subroutine makeareas
      use carbonmod
      real (kind=8) :: zsid(NLAT)          ! the Gaussian latitudes' sines and weights
      real (kind=8) :: zgwd(NLAT)
      real :: zdeglat(NLAT)
      real :: lat1(NLAT)
      real :: lat2(NLAT)

      call inigau(NLAT,zsid,zgwd)
      do jlat = 1 , NLAT
         zdeglat(jlat) = 180.0 / PI * asin(zsid(jlat))
      enddo
      lat1(1) = 0.5*PI
      lat1(NLAT) = 0.5*(zdeglat(NLAT-1)+zdeglat(NLAT))*PI/180.0
      lat2(1) = 0.5*(zdeglat(1)+zdeglat(2))*PI/180.0
      lat2(NLAT) = -0.5*PI
      do jlat=2,NLAT-1
         lat1(jlat) = 0.5*(zdeglat(jlat-1)+zdeglat(jlat))*PI/180.0
         lat2(jlat) = 0.5*(zdeglat(jlat+1)+zdeglat(jlat))*PI/180.0
      enddo
      call mpscrn(lat1,NLPP)
      call mpscrn(lat2,NLPP)
      do jlat=1,NLPP
         do jlon=1,NLON
            dglobe((jlat-1)*NLON+jlon) = 0.5/NLON*(sin(lat1(jlat))-sin(lat2(jlat)))
         enddo
      enddo
      return
      end subroutine makeareas

!     ================
!     SUBROUTINE OROINI
!     ================

!     The rivers' routing. PlaSim's oroini gathers the whole grid's orography, land and latitudes and sets the speed
!     at which each cell's runoff moves to its neighbours, a field the rivers alone use: their water reaches the sea
!     and returns nothing to the air or to the slab sea. A process with one row gathers no neighbours, so the column
!     keeps the speeds and areas the GCM wrote to its restart, which landini has read, and which oroini recomputes
!     unchanged while the orography stays fixed; it empties the rivers as oroini does. Glaciers, which reshape the
!     orography, stop the column

      subroutine oroini
      use glaciermod
      if (nglacier > 0.5) call mpabort('column: the column takes no glaciers, NGLACIER 0')
      driver(:)  = 0.
      drunoff(:) = 0.
      return
      end subroutine oroini
