!     The message-passing layer of a column of PlaSim's physics (climate/gcm/plasim_column.py), compiled in place of
!     PlaSim's single-process layer, mpimod_stub.f90 of ExoPlaSim 3.4.2, through its makefile's MPIMOD.
!
!     The column is one process of a decomposition with one latitude per process: PlaSim compiled with NPRO_ATM equal
!     to NLAT_ATM, so that NLPP is 1 and NHOR is one row of the GCM's grid, and this process stands for the process
!     that holds row nrow, counted from the north as PlaSim counts its rows. The routines keep the meaning that
!     mpimod.f90 gives them on that process. A scatter hands it its share of a global array, so the Gaussian
!     latitude, the surface files and the GCM's own restart reach PlaSim's routines at the row's grid points; a
!     gather places its share in a global array whose other rows hold 0; and the sums and maxima over processes
!     take this process alone. The process is also the root, so it reads the namelists and files as PlaSim's root
!     reads them. The routine list and the restart and surface routines follow mpimod.f90 and mpimod_stub.f90; the
!     shares and the module are the lab's. Distributed, as ExoPlaSim is, under the GNU GPL version 3.

      module colmod
      use pumamod
      integer :: nrow    = 0       ! the GCM's row the column stands in, 1 the northernmost
      integer :: nsteps  = 0       ! the steps the column runs
      integer :: nmode   = 1       ! 1: forced by windows of the dynamics' tendencies; 2: each step's state given
      integer :: nscheme = 1       ! with nmode 1, 1: the state the physics sees steps forward; 2: PlaSim's leapfrog
      integer :: ngp     = 0       ! the first grid point of the row in a global field, less 1
      integer :: nspo    = 0       ! the first spectral mode of the process's share, less 1
      namelist /column_nl/ nrow, nsteps, nmode, nscheme
      end module colmod

      subroutine mpstart(kworld) ! the column's settings, read from column_namelist
      use colmod
      open(11,file='column_namelist',form='formatted',status='old',iostat=io)
      if (io /= 0) then
         write(*,*) 'column: column_namelist is missing'
         stop 1
      endif
      read(11,column_nl,iostat=io)
      close(11)
      if (io /= 0) then
         write(*,*) 'column: column_namelist holds no readable namelist column_nl'
         stop 1
      endif
      if (NLPP /= 1) then
         write(*,*) 'column: PlaSim is compiled with',NLPP,' latitudes a process, where the column takes 1'
         stop 1
      endif
      if (nrow < 1 .or. nrow > NLAT) then
         write(*,*) 'column: the row',nrow,' lies outside the grid of',NLAT,' latitudes'
         stop 1
      endif
      if (nmode /= 1 .and. nmode /= 2) then
         write(*,*) 'column: nmode is 1 or 2, where it is',nmode
         stop 1
      endif
      if (nscheme /= 1 .and. nscheme /= 2) then
         write(*,*) 'column: nscheme is 1 or 2, where it is',nscheme
         stop 1
      endif
      ngp  = (nrow - 1) * NHOR
      nspo = (nrow - 1) * NSPP
      allocate(ympname(NPRO))          ! the processes' names, which prolog prints
      ympname(:) = ' '
      write(ympname(nrow),'("column of row",i4)') nrow
      return
      end

      subroutine mpstop
      return
      end

!     Broadcasts: the root's values are the process's own

      subroutine mpbci(k)
      return
      end

      subroutine mpbcin(k,n)
      integer :: k(n)
      return
      end

      subroutine mpbcr(p)
      return
      end

      subroutine mpbcrn(p,n)
      return
      end

      subroutine mpbcl(k)
      return
      end

!     Scatters: the process's share of n values a process

      subroutine mpscin(k,n)
      use colmod
      integer :: k(*)
      k(1:n) = k((nrow-1)*n+1:nrow*n)
      return
      end

      subroutine mpscrn(p,n)
      use colmod
      real :: p(*)
      p(1:n) = p((nrow-1)*n+1:nrow*n)
      return
      end

      subroutine mpscdn(p,n)
      use colmod
      real (kind=8) :: p(*)
      p(1:n) = p((nrow-1)*n+1:nrow*n)
      return
      end

      subroutine mpscsp(pf,pp,klev)
      use colmod
      real :: pf(NESP,klev)
      real :: pp(NSPP,klev)
      pp(1:NSPP,1:klev) = pf(nspo+1:nspo+NSPP,1:klev)
      return
      end

      subroutine mpscgp(pf,pp,klev)
      use colmod
      real :: pf(NUGP,klev)
      real :: pp(NHOR,klev)
      pp(1:NHOR,1:klev) = pf(ngp+1:ngp+NHOR,1:klev)
      return
      end

!     Gathers: the process's share in place, the other processes' shares 0

      subroutine mpgasp(pf,pp,klev)
      use colmod
      real :: pf(NESP,klev)
      real :: pp(NSPP,klev)
      pf(:,:) = 0.0
      pf(nspo+1:nspo+NSPP,1:klev) = pp(1:NSPP,1:klev)
      return
      end

      subroutine mpgagp(pf,pp,klev)
      use colmod
      real :: pf(NUGP,klev)
      real :: pp(NHOR,klev)
      pf(:,:) = 0.0
      pf(ngp+1:ngp+NHOR,1:klev) = pp(1:NHOR,1:klev)
      return
      end

      subroutine mpgacs(pcs)
      return
      end

      subroutine mpgallsp(pf,pp,klev)
      use colmod
      real :: pf(NESP,klev)
      real :: pp(NSPP,klev)
      pf(:,:) = 0.0
      pf(nspo+1:nspo+NSPP,1:klev) = pp(1:NSPP,1:klev)
      return
      end

!     Sums and maxima over processes: the process's own

      subroutine mpsum(psp,klev)
      return
      end

      subroutine mpsumsc(psf,psp,klev)
      use colmod
      real :: psf(NESP,klev)
      real :: psp(NSPP,klev)
      psp(1:NSPP,1:klev) = psf(nspo+1:nspo+NSPP,1:klev)
      return
      end

      subroutine mpsumr(pr,kdim)
      return
      end

      subroutine mpsumbcr(pr,kdim)
      return
      end

      subroutine mpmaxval(p,kdim,klev,pmax)
      real :: p(kdim,klev)
      pmax = maxval(p(:,:))
      return
      end

      subroutine mpsumval(p,kdim,klev,psum)
      real :: p(kdim,klev)
      psum = sum(p(:,:))
      return
      end

      subroutine mpabort(ym)
      use pumamod
      character (len=*) :: ym
      open(44,file='Abort_Message')
      write(44,'(A)') 'Program aborted'
      write(44,'(A)') trim(ym)
      close(44)
      write(nud,'(/,A,/,A)') 'Program aborted', trim(ym)
      write(*,'(A,/,A)') 'Program aborted', trim(ym)
      stop 1
      end

      subroutine ompi_info(nprocess,pid)
      use pumamod
      integer nprocess, pid
      nprocess = NPRO
      pid = 0
      return
      end subroutine ompi_info

!     The process's own arrays read and written

      subroutine mpreadsp(ktape,p,kdim,klev)
      real p(kdim,klev)
      read (ktape) p
      return
      end

      subroutine mpreadgp(ktape,p,kdim,klev)
      real p(kdim,klev)
      read (ktape) p
      return
      end

      subroutine mpwritesp(ktape,p,kdim,klev)
      real p(kdim,klev)
      write (ktape) p
      return
      end

      subroutine mpwritegp(ktape,p,kdim,klev)
      real p(kdim,klev)
      write (ktape) p
      return
      end

      subroutine mpwritegph(ktape,p,kdim,klev,ihead)
      real p(kdim,klev)
      real(kind=4) zp(kdim,klev)
      integer ihead(8)
      write(ktape) ihead
      zp(:,:)=p(:,:)
      write(ktape) zp
      return
      end

!     The restart and the surface files: the global record read whole and the process's share scattered, and the
!     share gathered into a global record, as mpimod.f90 reads and writes them

      subroutine mpgetsp(yn,p,kdim,klev)
      use pumamod
      character (len=*) :: yn
      real :: p(kdim,klev)
      real :: z(NESP,klev)
      z(:,:) = 0.0
      call get_restart_array(yn,z,NRSP,NESP,klev)
      call mpscsp(z,p,klev)
      return
      end subroutine mpgetsp

      subroutine mpgetgp(yn,p,kdim,klev)
      use pumamod
      character (len=*) :: yn
      real :: p(kdim,klev)
      real :: z(NUGP,klev)
      call get_restart_array(yn,z,NUGP,NUGP,klev)
      call mpscgp(z,p,klev)
      return
      end subroutine mpgetgp

      subroutine mpputsp(yn,p,kdim,klev)
      use pumamod
      character (len=*) :: yn
      real :: p(kdim,klev)
      real :: z(NESP,klev)
      call mpgasp(z,p,klev)
      call put_restart_array(yn,z,NRSP,NESP,klev)
      return
      end subroutine mpputsp

      subroutine mpputgp(yn,p,kdim,klev)
      use pumamod
      character (len=*) :: yn
      real :: p(kdim,klev)
      real :: z(NUGP,klev)
      call mpgagp(z,p,klev)
      call put_restart_array(yn,z,NUGP,NUGP,klev)
      return
      end subroutine mpputgp

      subroutine mpsurfgp(yn,p,kdim,klev)
      use pumamod
      character (len=*) :: yn
      real :: p(kdim,klev)
      real :: z(NUGP,klev)
      integer :: iread
      call get_surf_array(yn,z,NUGP,klev,iread)
      if (iread == 1) call mpscgp(z,p,klev)
      return
      end subroutine mpsurfgp

!     Coupled runs of two models, which the column never makes

      subroutine mrsum(k)
      return
      end

      subroutine mrbci(k)
      return
      end

      subroutine mrdiff(p,d,n)
      real :: p(n)
      real :: d(n)
      return
      end

      subroutine mrdimensions
      return
      end
