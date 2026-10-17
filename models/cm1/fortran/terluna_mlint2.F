! WRF-ELEC (MicroTed/wrf4-elec e43041b, elec/module_boxmgsetup.F): mlint2, trilinear interpolation for lightmsz;
! taken out by climate/crm/cm1_elec.py
      subroutine mlint2                             &
       (idebug,ac,n1b,n1e,n2b,n2e,n3b,n3e,n4b,n4e,  &
        nx,ny,nz,aint,facx,facy,facz,ic,jc,kc,lc)
!
      integer  idebug
      integer  ic
      integer  kc
      integer  jc
      integer  lc
!
      real     acx1
      real     acx2
      real     acx3
      real     acx4
      real     acy1
      real     acy2
      real     aint
      real     facx
      real     facy
      real     facz
      real     ac(n1b:n1e,n2b:n2e,n3b:n3e,n4b:n4e)
      
      
      acx1 = 0.0
      acx2 = 0.0
      acx3 = 0.0
      acx4 = 0.0
      acy1 = 0.0
      acy2 = 0.0
      
!
!  x-direction interpolation
!
      if( nx .gt. 1 ) then
!
      acx1 = facx*(ac(ic+1,jc,kc,lc)-ac(ic,jc,kc,lc)) +  &
             ac(ic,jc,kc,lc)
      acx2 = facx*(ac(ic+1,jc,kc+1,lc)-ac(ic,jc,kc+1,lc)) + &
             ac(ic,jc,kc+1,lc)
!
      else if( nx .le. 1 .and. ny .gt. 1 ) then
!
      acy1 = facy*(ac(ic,jc+1,kc,lc)-ac(ic,jc,kc,lc)) +       &
             ac(ic,jc,kc,lc)
      acy2 = facy*(ac(ic,jc+1,kc+1,lc)-ac(ic,jc+1,kc+1,lc)) + &
            ac(ic,jc+1,kc+1,lc)
!
      
      else  ! 1-d vertical interpolation

      acy1 = ac(ic,jc,kc,lc)
      acy2 = ac(ic,jc,kc+1,lc)
      
      end if
!
!  y-direction interpolation of data interpolated in x-direction
!  for bottem of cube if in 3-d; eg x:y:z trajectory
!
      if( nx .gt. 1 .and. ny .gt.1 ) then
!
      acx3 = facx*(ac(ic+1,jc+1,kc,lc)-ac(ic,jc+1,kc,lc)) +     &
             ac(ic,jc+1,kc,lc)
      acx4 = facx*(ac(ic+1,jc+1,kc+1,lc)-ac(ic,jc+1,kc+1,lc)) + &
             ac(ic,jc+1,kc+1,lc)
!
! y-direction interpolation of x interpolated data
!
      acy1 = facy*(acx3-acx1) + acx1
      acy2 = facy*(acx4-acx2) + acx2
!
!  z-direction interpolation of data interpolated in x:y-directions
!
      aint = facz*(acy2-acy1) + acy1
!
!  z-direction interpolation of data interpolated in y-direction for
!  2-d y:z trajectory
!
      else if ( nx .le. 1 ) then
      aint = facz*(acy2-acy1) + acy1
!
!  z-direction interpolation of data interpolated in x-direction for
!  2-d x:z trajectory
!
      else if ( ny .le. 1 ) then
      aint = facz*(acx2-acx1) + acx1
      end if
!
      if ( idebug .ge. 2 ) then
      IF ( nx .gt. 1 ) print*,'acx1,acx2: ',acx1, acx2, facx
      print*,'acx3,acx4: ',acx3, acx4, facx
      print*,'acy1,acy2: ',acy1, acy2, facy
      print*,'aint: ', aint, facz
      end if
!
      return
      end
