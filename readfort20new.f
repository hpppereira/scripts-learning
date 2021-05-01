      PROGRAM READFORT30

C read output fort.30 from /data/sudo/AVHRR/nvc/SAR_CYCLE_DLR/sar_cycle_4/part/partout2.f

C fort.30 is in /data/sudo/AVHRR/nvc/SAR_CYCLE_DLR/sar/19.../0.it(1.it,2.it,3.it...)/part

c check ../res/foo.idx to see the index of the best iterarion

C fort.321 = /data/sudo/AVHRR/nvc/SAR_CYCLE_DLR/sar/19.../0.it(1.it,2.it,3.it...)/part

C so copy fort.321 and fort.30 to the present dir

c output: 
c        fort.345    => the whole 2d spec
c        fort.345+1  => 1st partition
c        fort.345+2  => 2nd partition
c        ...

c  the programs ../sarpaper/readfort345.m, readfort346.m, etc read these outputs in matlab



      PARAMETER( MSPEC=50, MPART=65, NANG=24, NFRE=25, NFRE19=19)

C      IMPLICIT NONE
      INTEGER OUTUNIT 
c               output unit
      INTEGER MSPEC, NSPEC, MPART, NANG, NFRE, DUMMY
c               dimensions
      INTEGER NASPEC
c               output starts at spectrum naspec
      INTEGER NPART(MSPEC)
c               number of partitionings for each spectrum.
      DOUBLE PRECISION SPEC(0:MSPEC,NANG,NFRE)
c               2d spectrum.
      INTEGER PART(MSPEC,NANG,NFRE)
c               gives number of partitioning for each freq-dir bin.
      DOUBLE PRECISION WORK(NANG,NFRE)
c               work space.
      DOUBLE PRECISION LONG(MSPEC),
     &     LAT(MSPEC), 
     &     DATE(MSPEC),
     &     HST(MSPEC),
     &     FMEANT(MSPEC), 
     &     THQT(MSPEC),
     &     EMEAN(MSPEC,MPART),
     &     THQ(MSPEC,MPART), 
     &     FMEAN(MSPEC,MPART),
     &     TRACK(MSPEC), 
     &     COST(MSPEC),
     &     U10(MSPEC), 
     &     THW(MSPEC)
c                   longitude,latitude,time,significant wave 
c                   height, mean frequency,mean direction 
c                   of input spectra and partitionings, 
c                   satellite track,u10,wind direction.
      DOUBLE PRECISION TH0, FRE1, CO
c
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IPART, IANG, IFRE,nparte
c                   loop indices
      DOUBLE PRECISION PI, PI180, TWEG, DELTANG, ZGRAV
      integer unit
C
C------------------------------------------------------------------
c unit 30 (fort.30) partitionings of inverted spec
c unit 20 (fort.20) partitionings of 1st guess spec
C
      unit=20   ! 1st guess spec

      OUTUNIT=245

      PI = 4*ATAN(1.)
      PI180 = 180 / PI
      ZGRAV = 9.806
      TWEG = 3 * PI / ZGRAV
      DELTANG = 2 * PI / NANG


       read(321)NASPEC,NSPEC
       read(321)NPART
       read(321)EMEAN
c       write(*,*)'NASPEC,NSPEC =',NASPEC,NSPEC,NPART
c       write(*,*)'EMEAN =',EMEAN

      DO ISPEC = NASPEC,NSPEC
        

c       write(*,*)'outunit =', outunit
        
	READ(unit) LONG(ISPEC),LAT(ISPEC),DATE(ISPEC),
     &       DUMMY, DUMMY,TH0,FRE1,CO
        WRITE(OUTUNIT) LONG(ISPEC),LAT(ISPEC),DATE(ISPEC),
     &       NANG, NFRE,TH0,FRE1,CO

        READ(unit) HST(ISPEC)
        WRITE(OUTUNIT)HST(ISPEC)
c        WRITE(*,*)HST(ISPEC)
	
        READ(unit) THQT(ISPEC) 
        WRITE(OUTUNIT) THQT(ISPEC) 
	
        READ(unit) FMEANT(ISPEC)
        WRITE(OUTUNIT) FMEANT(ISPEC)

        READ(unit) U10(ISPEC)
        WRITE(OUTUNIT) U10(ISPEC)
	
        READ(unit) THW(ISPEC)
        WRITE(OUTUNIT) THW(ISPEC)
	
        READ(unit) 
     &    ((SPEC(ISPEC,IANG,IFRE),IANG=1,NANG),IFRE=1,NFRE)

        WRITE(OUTUNIT) 
C        WRITE(OUTUNIT,20) 
     &    ((SPEC(ISPEC,IANG,IFRE),IANG=1,NANG),IFRE=1,NFRE)
C20      format(F15.10)
C20      format(24F15.10)
c

        nparte=NPART(ISPEC)
        DO IPART = 1,nparte
         if(4 * SQRT(EMEAN(ISPEC,IPART)).gt.0.) then
          DO IANG = 1,NANG
            DO IFRE = 1,NFRE
              IF( PART(ISPEC,IANG,IFRE).EQ.IPART )THEN
                WORK(IANG,IFRE) = SPEC(ISPEC,IANG,IFRE)
              ELSE
                WORK(IANG,IFRE) = 0.
              END IF
            END DO
          END DO
        
c        OUTUNIT=OUTUNIT+ISPEC
c        OUTUNIT=OUTUNIT+1

c       write(*,*)'outunit =', outunit

          READ(unit) LONG(ISPEC),LAT(ISPEC),DATE(ispec),
     &         DUMMY, DUMMY,TH0,FRE1,CO
c        WRITE(*,*) LONG(ISPEC),LAT(ISPEC),DATE(ISPEC),
c     &       NANG, NFRE,TH0,FRE1,CO
        WRITE(OUTUNIT) LONG(ISPEC),LAT(ISPEC),DATE(ISPEC),
     &       NANG, NFRE,TH0,FRE1,CO
     
          READ(unit) EMEAN(ISPEC,IPART)
c          WRITE(*,*) EMEAN(ISPEC,IPART)
          WRITE(OUTUNIT) EMEAN(ISPEC,IPART)
 	  
          READ(unit) THQ(ISPEC,IPART)
c        WRITE(*,*) THQ(ISPEC,IPART) 
        WRITE(OUTUNIT) THQ(ISPEC,IPART) 
	  
          READ(unit) FMEAN(ISPEC,IPART)
c        WRITE(*,*) FMEAN(ISPEC,IPART)
        WRITE(OUTUNIT) FMEAN(ISPEC,IPART)
	  
          READ(unit) U10(ISPEC)
c        WRITE(*,*) U10(ISPEC)
        WRITE(OUTUNIT) U10(ISPEC)
	  
          READ(unit) THW(ISPEC)
        WRITE(OUTUNIT) THW(ISPEC)
c        WRITE(*,*) THW(ISPEC)
	  
          READ(unit) 
     &        ((WORK(IANG,IFRE),IANG=1,NANG),IFRE=1,NFRE)
        WRITE(OUTUNIT) 
C        WRITE(OUTUNIT,20) 
     &    ((WORK(IANG,IFRE),IANG=1,NANG),IFRE=1,NFRE)
C20      format(F15.10)
20      format(24F15.10)
     

         end if
        END DO
c	outunit=outunit+1
      END DO          

      stop
      end
