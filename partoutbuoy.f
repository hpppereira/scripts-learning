      PROGRAM PARTOU2
c
c-----------------------------------------------------------------
c
c
c     susanne hasselmann max planck institut fuer meteorologie 
c                        in hamburg.
c     september 1993
c     juergen waszkewitz max planck institut fuer meteorologie 
c                        in hamburg.
c     changes for vectorization september 1993.
c
c
c     purpose:
c     --------
c
c     reads wam and sar spectra in format of sar inversion 
c     program. routine can be replaced.
c
c     seperates spectra into wave systems
c     and outputs partitionings for plotting ( specol,arrows)
c
c     the program crossassigns sar and wam partitionings and 
c     combines sar partitionings if the mean wave numbers both 
c     have a distance 
c     < 0.75 to the mean wave number of a wam partitioning.
c
c     if parameter "transorm" is set to .true., the partitionings 
c     of the
c     wam first guess spectra are transformed to the mean 
c     energy, mean angle, and mean frequency of the corresponding
c     partitioning of the retrieved sar spectrum.
c
c
c
c
c     externals:
c     ----------
c
c     readspec   - reads spectra in format of output of sar 
c                  inversion program.
c     """""""" or """"""""""
c     readspew   - reads spectra for one assimilation time window.
c                  output of prepsar.
c     correl     - crossassignment of wam and sar partitionings and
c                  combining of sar partitionings if distance to 
c                  wam partitionings is small.
c     crossas    - crossassignment of wam and sar partitionings .
c     meanst     - computes integrated values of total spectra.
c     swellsep   - partitions spectra.
c     tustre     - transforms partitionings of wam first 
c                  guess spectra to mean values of sar partitionings 
c                  and combines these to one spectrum.
c     writearrow - output of mean values of partitionings.
c     writemean  - output of integrated values of total spectra.
c     writespec  - output of spectra and their partitionings.
c     writespe   - output of corrected spectra in wam format.
c
c
c     interface:
c     ----------
c
c     input file:  unit 10 : spectra - output of sar inversion 
c                                      program. can be replaced!
c     
c
c     output files:
c
c     - unit 20 : partitionings of first guess spectra.
c     - unit 21 : hs of first guess spectra.
c     - unit 22 : mean wave length of first guess spectra.
c     - unit 23 : hs  of partitionings of first guess spectra.
c     - unit 24 : mean wave length of partitionings of first 
c                 guess spectra.
c     - unit 26 : hs of total corrected spectra.
c     - unit 27 : mean wave length of total corrected spectra.
c     - unit 28 : corrected spectra.
c
c     - unit 30 : partitionings of inverted spectra.
c     - unit 31 : hs of inverted spectra.
c     - unit 32 : mean wave length of inverted spectra.
c     - unit 33 : hs of partitionings of inverted spectra.
c     - unit 34 : mean wave length of partitionings of inverted 
c                 spectra
c
c       the following output is especially designed for MPI 
c       postprocessing.
c       ---------------------------------------------------
c        on units 43,44, and 46 the first six culumns are pairs
c        for first guess and sar inverted wave spectra:
c         1,2   added wind and old wind sea (1+3)
c         3,4   mixed sea (2)
c         5,6   swell  (3)
c         7,8   total spectrum 
c         9,10  number of partitionings   
c        11     spectrum number
c
c     - unit 42 : mean squared spread (sums of each wave system)
c     - unit 43 : mean frequency (sums of each wave system)
c     - unit 44 : mean direction (sums of each wave system)
c     - unit 46 : sign. waveheight (sums of each wave system)
c     - unit 45 : statistics: wrong correlations, no correlations 
c                 for wam, and no correlations for sar.
c     - unit 47 : wam partitionings: hs,fmean, thetamean, spread
c                  wavesysytem, correlated sar, and spectrum number 
c     - unit 48 : wam partitionings: hs,fmean, thetamean, spread,
c                  wavesysytem, correlated wam, and spectrum number 
c     - unit 49 : hs, fmean, thetamean, spread, system type, 
c                 and spectrum number of the correlated wave 
c                 systems. (wam and sar paired)
c-----------------------------------------------------------------------
c-----------------------------------------------------------------------
c
      IMPLICIT NONE
      INCLUDE "part2.par"
c
c     variables:
c     ----------
c
      INTEGER NSPEC
c                   the number of spectra.
      INTEGER NASPEC
c                   output starts at spectrum naspec.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE,2)
c                   spectra. last index stands for first guess 
c                   spectrum = 1, sar retrieved spectrum = 2.
      INTEGER PART(MSPEC,NANG,NFRE,2)
c                   to spec corresponding array of partitioning 
c                   information part(ispec,iang,ifre) =: p means, 
c                   that in spectra ispec the energy at angle iang
c                   AND FREQUENCY IFRE BELONGS TO PARTITION NUMBER P.  
      DOUBLE PRECISION  WORK(NANG,NFRE)
c                   intermediate storage for subroutine writespec.
      INTEGER NPART(MSPEC,2)
c                   number of partitionings
      INTEGER PARTINFO(MSPEC,MPART,2)
c                   information for windsea-swell:
c                   windsea (1), mixed (=2), or swell (=0)       
c                   (there is no more than one windsea partioning)
      DOUBLE PRECISION  LONG(MSPEC,2),
     &     LAT(MSPEC,2),
     &     DATE(MSPEC,2),
     &     HST(MSPEC,2),
     &     FMEANT(MSPEC,2),
     &     THQT(MSPEC,2),
     &     TRACK(MSPEC,2),
     &     COST(MSPEC,2),
     &     U10(MSPEC,2), 
     &     THW(MSPEC,2)
c                   longitude,latitude,time,significant wave 
c                   height, mean frequency,mean direction ,
c                   number of satellite track, final value of cost 
c                   function in inversion algorithm, u10, wind 
c                   direction for input spectra.
       DOUBLE PRECISION  
     &     SPREADT(MSPEC,2),
     &     SPREADP(MSPEC,MPART,2)
c                   spectral spread of total and partitioned spectra.
c                   after meanst and swellsep.
      INTEGER CORRELTAW(MSPEC,MPART)
c                   crossassigns wam and sar partitionings.
c                   correltaw(ispec,ipartwam)=ipartsar
      INTEGER CORRELTAS(MSPEC,MPART)
c                   as correltaw for sar - wam.
      DOUBLE PRECISION  LOWEST
c                   wave systems of  wave height less than lowest 
c                   are combined with next wave system.
      DOUBLE PRECISION  MEANE(MSPEC,MPART,2),
     &     MEANANG(MSPEC,MPART,2),
     &     MEANFRE(MSPEC,MPART,2)
c                   mean energy,mean direction, mean frequency for 
c                   all partitionigs and all spectra. last index 
c                   denotes wam if equal to 1 and sar if equal to 2.
      DOUBLE PRECISION  MEANTE(MSPEC),
     &     MEANTANG(MSPEC),
     &     MEANTFRE(MSPEC)
c                   mean energy, mean direction, mean frequency 
c                   of total spectrum.
      INTEGER INUNIT,OUT1UNIT,OUT2UNIT,OUT3UNIT,OUT4UNIT,OUT5UNIT
     &              ,OUTUNIT
c                   unit numbers of input resp. output file.
      DOUBLE PRECISION  TH0
c                   first direction in spectrum.
      DOUBLE PRECISION  FRE1
c                   lowest frequency.
      DOUBLE PRECISION  CO,ALEVEL,DISMIN
c                   coefficient between two frequencies
c                   factor for threhhold check, and minimum 
c                   distance between two wave systems in k-space
c                   for combining sar peaks.
      INTEGER ISPEC,ISPA
c                   loop indices.
      DOUBLE PRECISION  FRETAB(NFRE), COSTAB(NANG), SINTAB(NANG),
     &     DFIM(NFRE),DFIMW(NFRE)
c                    tables of frequencies, cos,sin of directions,
c                    frequency increments/directional increment, 
c                    respectively.
      DOUBLE PRECISION  SUM0(MSPEC,MPART), SUMX0(MSPEC,MPART),
     & SUMY0(MSPEC,MPART)
c                     work space for temporary sums.  
      INTEGER IS
      DOUBLE PRECISION  WEIGHT, PI, PI18
c       statistical parameters of the partitionings
c       variables for additional output
c       mean significant wave height
      DOUBLE PRECISION  XMEANHS(0:3,2)
c       energy weighted averages
      DOUBLE PRECISION  XMEANDIR(0:3,2), ANGLE
      DOUBLE PRECISION  XMEANSIN(0:3,2), XMEANCOS(0:3,2)
      DOUBLE PRECISION  XMEANFREQ(0:3,2)
      DOUBLE PRECISION  XMEANSPREAD(0:3,2)
c
c           iwrong   : number of cross assigned wave systems 
c                      of different kind
c           inopartw : number of BUOY/WAM wave partitionings 
c                      without cross assigned partner
c           inoparts :             SAR
c
      INTEGER INOPARTW, INOPARTS, IWRONG, I, J
c   workspace
      DOUBLE PRECISION      TMPSIN, TMPCOS
      DOUBLE PRECISION      WINADD_WAM, WINADD_SAR
      INTEGER  INDEX
c
c quality variables of the SAR inversion
       DOUBLE PRECISION  XCORWA(MSPEC), XCORFG(MSPEC), XCORBE(MSPEC)
       INTEGER     JQUAL(MSPEC)
       CHARACTER   CDATE*11
       DOUBLE PRECISION         XDIS
       DOUBLE PRECISION         HS_WAM, HS_SAR
c
c      real sphrds
c      external sphrds
      DOUBLE PRECISION RAD2DEG
      EXTERNAL RAD2DEG
      INTEGER IAN,IFR, IPART, JPART_MODE   
c
c------------------------------------------------------------------
c      
      PI = 4*ATAN(1.)
      PI18 = 180/PI
      INUNIT = 10

      TH0 = 0.
      FRE1 = 0.04177
      CO = 1.1
c
c     1.1 input of sar and wam first guess spectra at sar points.
c     ----------------------------------------------------------
C    READ WAM FIRST GUESS
      INUNIT = 10
      CALL READSPE1( 
C            INPUT UNIT
     &         INUNIT , 
C            DIMENSIONS
     &         MSPEC , NSPEC , NANG , NFRE , 
C            OUTPUT
     &         SPEC(0,1,1,1) ,LONG(1,1) , LAT(1,1) , DATE(1,1) ,
     &         HST(1,1),FMEANT(1,1),THQT(1,1),TRACK(1,1),COST(1,1), 
     &         U10(1,1) , THW(1,1) )
      WRITE(6,*) ' NUMBER OF SPECTRA FROM INVERSION PROGRAM: ',
     &             NSPEC
c
CN      CALL READSPEC( 
c            input unit
CN     &         INUNIT , 
c            dimensions
CN     &         MSPEC , NSPEC , NANG , NFRE , 
c            output
CN     &         SPEC ,LONG , LAT , DATE ,
CN     &         HST , FMEANT , THQT , TRACK , COST , 
CN     &         U10 , THW )
CN      WRITE(6,*) ' NUMBER OF SPECTRA FROM INVERSION PROGRAM: ',
CN     &             NSPEC
c
c     1.2 compute and output mean values of total wam spectrum.
c     ---------------------------------------------------------
c

      CALL MEANST(
c                  dimensions
     &                   MSPEC,NSPEC,NANG,NFRE,NFRE,
c                  input 
     &                   SPEC(0,1,1,1) ,
c                  output
     &                   HST(1,1), THQT(1,1), FMEANT(1,1), spreadt(1,1),
c                  work arrays
     &                   SUM0(1,1) , SUMX0(1,1) , SUMY0 (1,1),
c                  input from initialization routine
     &                   FRE1,CO ,FRETAB ,COSTAB ,SINTAB,DFIM )

      OUTUNIT=21
      CALL WRITEMEAN( 
c                  output unit
     &               OUTUNIT ,
c                  dimensions
     &               MSPEC , NSPEC ,
c                  input
     &               LONG(1,1),LAT(1,1),DATE(1,1),HST(1,1),THQT(1,1),
     &               FMEANT(1,1), CONTROL )
c
c------------------------------------------------------------------
c
c     2. partitioning of wam spectra.
c     -------------------------------
c
      LOWEST=0.2
      ALEVEL=0.85
CN      CALL SWELLSEP( 
      CALL SWELLSEPBUOY( 
c            dimensions
     &         MSPEC , NSPEC , MPART ,  NANG , NFRE ,
c            input
     &         SPEC(0,1,1,1),U10(1,1),THW(1,1),FRE1,CO,
     &         ALEVEL,.TRUE.,LOWEST,
c            output
     &         NPART(1,1) ,PART(1,1,1,1) ,
     &         PARTINFO(1,1,1) , MEANE(1,1,1) ,MEANANG(1,1,1) ,
     &         MEANFRE(1,1,1) , SPREADP(1,1,1) )
c
c------------------------------------------------------------------
CN=============
c      write(6,*)'i was here 2'
       write(*,*)'spreadp =',  SPREADP(1,1,1) 
CN=============
c
c
c     output of mean values of correlated wave systems for
c     postprocessing at the MPI.
c     -------------------------------------------------
c
      CALL  OUTPOPRO(
c                   dimensions
     &                MSPEC , MPART ,
c                   input
     &                SPREADT,SPREADP,NPART,NSPEC,PI,PARTINFO,
     &                CORRELTAW,CORRELTAS,MEANE,MEANFRE,HST,FMEANT
CN     &                ,MEANANG,THQT) 
     &                ,MEANANG,THQT,U10,THW)
c
c------------------------------------------------------------------
c
c     6.1 output 2d wam first guess spectra and partitionings for 
c     plotting.
c     --------------------------------------------------------
c
      NASPEC=1
      OUT1UNIT=20
      CALL WRITESPEC(
c            output unit
     &         OUT1UNIT ,
c            dimensions
     &         MSPEC , NASPEC,NSPEC , MPART , 
c    &       input 
     &         NPART(1,1) , NANG , NFRE , SPEC(0,1,1,1) , 
     &         PART(1,1,1,1) , WORK ,LONG(1,1) , LAT(1,1) ,
     &         DATE(1,1) , HST(1,1) , FMEANT(1,1) ,
     &         THQT(1,1) , TRACK(1,1) , COST(1,1) , U10(1,1) , 
     &         THW(1,1) ,MEANE(1,1,1) , MEANANG(1,1,1) ,
     &         MEANFRE(1,1,1) ,
     &         TH0 , FRE1 , CO )
c
c     6.3 output mean values of partitionings
c     ---------------------------------------
c
      OUT3UNIT=23
      CALL WRITEARROW( 
c            output unit
     &         OUT3UNIT , 
c            dimensions
     &         MSPEC , NSPEC , MPART ,
c            input 
     &         PARTINFO(1,1,1),
     &         NPART(1,1) , LONG(1,1) , LAT(1,1) , DATE(1,1) ,
     &         MEANE(1,1,1),MEANANG(1,1,1),MEANFRE(1,1,1),CONTROL)
cn     &MEANE(1,1,1),MEANANG(1,1,1),MEANFRE(1,1,1),CONTROL,spreadp(1,1,1))
C
      OUTUNIT=26
      CALL WRITEMEAN( 
c                  output unit
     &               OUTUNIT ,
c                  dimensions
     &               MSPEC , NSPEC ,
c                  input
     &               LONG(1,1),LAT(1,1),DATE(1,1),HST(1,1),THQT(1,1),
     &               FMEANT(1,1), CONTROL )
c
c------------------------------------------------------------------
c
c      8. output of corrected spectra.
c      -------------------------------
c
      NASPEC=1
      OUT5UNIT=28
      CALL WRITESPE(
c            output unit
     &         OUT5UNIT, 
c            dimensions
     &         MSPEC, NASPEC,NSPEC, NANG, NFRE, 
c            input
     &         SPEC(0,1,1,1),
     &         LONG(1,1) , LAT(1,1) ,DATE(1,1), TRACK(1,1), 
     &         COST(1,1) , U10(1,1) , THW(1,1) ,
     &         MEANTE , MEANTANG , MEANTFRE ,
     &         TH0 , FRE1 , CO , .FALSE. )

c
      WRITE(6,*) 'PROGRAM ENDS NORMALLY'
      STOP
      END

c
c------------------------------------------------------------------
c
      SUBROUTINE OPFIL(IDATE,IUNIT)
c
c--------------------------------------------------------------------
c
c      s.hasselmann mpm hamburg 8/93.
c
c      purpose.
c      --------
c
c      open file of sar retrieved and wam spectra for one time window
c
c      interface.
c      ----------
c      *call* *opfil(ctime,outun)*
c         *idate* - current output date.
c         *iunit* - output unit.
c
c      externals.
c      ----------
c      none
c
c      method.
c      -------
c      none.
c
c      references.
c      -----------
c      none.
c
c------------------------------------------------------------------
c
c      IMPLICIT NONE
c
      INTEGER IUNIT,IDATE
c
      CHARACTER FNAME*13,FID*3
c
c------------------------------------------------------------------
c
CN==
      open(321,file='/data/sudo/AVHRR/nvc/sarpaper/partout2.out',
     &          FORM='UNFORMATTED',status='unknown')
CN==
      FID='SAR'
      WRITE(FNAME(1:3),'(A)') FID
      WRITE(FNAME(4:13),'(I10.10)') IDATE
      OPEN(UNIT=IUNIT,FILE=FNAME,FORM='UNFORMATTED',
     1     ERR=4000)
      WRITE(6,*) 'FILE[',FNAME(1:13),']OPENED AND ASSIGNEDTOUNIT '
     1             ,IUNIT
      RETURN
 4000 CONTINUE
      RETURN
      END
c
CN=============================
C
      SUBROUTINE READSPE1( 
C            INPUT UNIT
     &         INUNIT , 
C            DIMENSIONS
     &         MSPEC , NSPEC , NANG , NFRE , 
C            OUTPUT
     &         SPEC ,LONG , LAT , DATE ,
     &         HST , FMEANT , THQT , TRACK , COST , 
     &         U10 , THW )
C
C
C------------------------------------------------------------------
      IMPLICIT NONE
C
C     PURPOSE:
C     --------
C
C     READS  SPECTRA IN WAM FORMAT.
C
C
C     INTERFACE:
C     ----------
C
      INTEGER INUNIT, MSPEC, NSPEC, NANG, NFRE
C              DIMENSIONS
cn      REAL SPEC(0:MSPEC,NANG,NFRE)
      double precision SPEC(0:MSPEC,NANG,NFRE)
C              2D SPECTRA (1 DENOTES WAM,2 DENOTES SAR RETRIEVED.
cn     REAL LONG(MSPEC),
      double precision LONG(MSPEC),
     &     LAT(MSPEC), 
     &     DATE(MSPEC),
     &     HST(MSPEC),
     &     FMEANT(MSPEC),
     &     THQT(MSPEC),
     &     TRACK(MSPEC),
     &     COST(MSPEC),
     &     U10(MSPEC), 
     &     THW(MSPEC)
C                   LONGITUDE,LATITUDE,TIME,SIGNIFICANT WAVE 
C                   HEIGHT, MEAN FREQUENCY,MEAN DIRECTION 
C                   OF INPUT SPECTRA.
C
C
C
C     VARIABLES:
C     ----------
C
      double precision PI, PI180
cn      REAL PI, PI180
      INTEGER ISPEC, IANG, IFRE
C                    LOOP INDICES
C
cn==
        integer*8 sub1, sub2
c        sub1=91030303.*100
c        sub2=91030315.*100
cn==
C------------------------------------------------------------------
C
C
C     READ INPUT FROM SAR INVERSION PROGRAM UNTIL END OF FILE IS 
C     REACHED.
C
C
CN==
CN    this is the way to read the file generated by matlab
cn   ../nvc/sarpaper/part/buoybatch.m
cn   if i'm reading the file fort.10 generated by fortran 
cn   this option should be unset
cn
      open(10,file='fort.10',
     1        status='unknown',form='binary')
cn   format to read a file generated by matlab     
CN==
      PI = ACOS(-1.)
      PI180 = 180. / PI
C
C

C      1.1 READ WAM AND OBSERVED SAR SPECTRA FOR ONE TIME WINDOW.
C      ----------------------------------------------------------
C
 1100 CONTINUE
C     
      ISPEC = 1
ctest
 200   continue
ctest
      DO WHILE (.TRUE.)


         READ(INUNIT,END = 100) LONG(ISPEC),LAT(ISPEC)
     &        ,DATE(ISPEC)
         write(32,*) ' long,lat,date ',ispec,LONG(ISPEC),
     &        LAT(ISPEC),DATE(ISPEC)
cn==
      write(*,*) ' heya long,lat,date ',ispec,LONG(ISPEC),
     &        LAT(ISPEC),DATE(ISPEC)
cn==
         READ(INUNIT) HST(ISPEC)
         write(32,*)'HST =', HST(ISPEC)
         write(*,*)'HST =', HST(ISPEC),'nang=', NANG, 'nfre=', NFRE
         READ(INUNIT) THQT(ISPEC)
         THQT(ISPEC) = THQT(ISPEC)/PI180
         READ(INUNIT) FMEANT(ISPEC)
         READ(INUNIT) U10(ISPEC)
         READ(INUNIT) THW(ISPEC)
         write(*,*)'THW =', THW(ISPEC)
         THW(ISPEC) = THW(ISPEC)/PI180
         READ(INUNIT) 
     &        ((SPEC(ISPEC,IANG,IFRE),IANG=1,NANG),IFRE=1,NFRE)
c         write(*,*) 
c     &        ((SPEC(ISPEC,IANG,IFRE),IANG=1,NANG),IFRE=1,NFRE)
            ISPEC = ISPEC + 1   
      END DO
C
ctest
 100  continue
      if(inunit.eq.11) then
        inunit=9
        go to 200
      end if
ctet
      NSPEC = ISPEC - 1
      RETURN

      END
CN=============================
c------------------------------------------------------------------
c
      SUBROUTINE READSPEC( 
c            input unit
     &         INUNIT , 
c            dimensions
     &         MSPEC , NSPEC , NANG , NFRE , 
c            output
     &         SPEC ,LONG , LAT , DATE ,
     &         HST , FMEANT , THQT , TRACK , COST , 
     &         U10 , THW )
c
c------------------------------------------------------------------
      IMPLICIT NONE
c
c     purpose:
c     --------
c
c     reads  spectra in the format of the sar inversion program.
c
c 
c     interface:
c     ----------
c
      INTEGER INUNIT, MSPEC, NSPEC, NANG, NFRE
C              DIMENSIONS
      DOUBLE PRECISION SPEC(0:MSPEC,NANG,NFRE,2)
C              2D SPECTRA (1 DENOTES WAM,2 DENOTES SAR RETRIEVED.
      DOUBLE PRECISION LONG(MSPEC,2),
     &     LAT(MSPEC,2), 
     &     DATE(MSPEC,2),
     &     HST(MSPEC,2), 
     &     FMEANT(MSPEC,2),
     &     THQT(MSPEC,2),
     &     TRACK(MSPEC,2),
     &     COST(MSPEC,2),
     &     U10(MSPEC,2), 
     &     THW(MSPEC,2)
c                   longitude,latitude,time,significant wave 
c                   height, mean frequency,mean direction 
c                   of input spectra.
c
c
c
c     variables:
c     ----------
c
      INTEGER I,ISPEC, JSPEC, IANG, IFRE
c                    loop indices
      INTEGER IANGP1, IANGM1, IFREP1, IFREM1
c                    "iang plus 1", "iang minus 1", 
c                    "ifre plus 1", "ifre minus 1"
      DOUBLE PRECISION DUMMY
      INTEGER INTDUMMY,NCOUNTE,JQUAL
      DOUBLE PRECISION HARR(192),XCORWA,XCORFG,XCORBE
      DOUBLE PRECISION PI, PI180
      LOGICAL ZERO1, ZERO2
c
CN===
       integer*8 sub
CN===
c------------------------------------------------------------------
c
      PI = 4*ATAN(1.)
      PI180 = 180. / PI
      ISPEC = 1
      JSPEC = 1
      ncounte=1
c
c     read input from sar inversion program until end of file is 
c     reached.
c
CN=== i had to do so 'cos i had an error of overflow operation on hydra
       sub = 1900000
       sub = sub*100000
CN===
      DO WHILE( .TRUE. )
       DO I = 1,2
         READ(INUNIT,END=1) LONG(ISPEC,I),LAT(ISPEC,I),DATE(ISPEC,I)
         IF( LONG(ISPEC,I).LT.0 ) LONG(ISPEC,I) = LONG(ISPEC,I) + 360.
         READ(INUNIT) HST(ISPEC,I), FMEANT(ISPEC,I), DUMMY,
     &        THQT(ISPEC,I), DUMMY, DUMMY
         THQT(ISPEC,I) = THQT(ISPEC,I) / PI180
CN         IF(DATE(ISPEC,I).GT.190000000000.) 
         IF(DATE(ISPEC,I).GT.sub) 
CN     &          DATE(ISPEC,I) = DATE(ISPEC,I) - 190000000000.
     &          DATE(ISPEC,I) = DATE(ISPEC,I) - sub
       END DO
       READ(INUNIT) DUMMY, DUMMY, DUMMY, DUMMY, DUMMY, DUMMY
       READ(INUNIT) DUMMY, DUMMY, DUMMY, DUMMY, DUMMY, DUMMY
       READ(INUNIT) DUMMY, DUMMY, DUMMY, DUMMY, DUMMY, DUMMY
       READ(INUNIT) TRACK(ISPEC,1), COST(ISPEC,1), U10(ISPEC,1),
     &      THW(ISPEC,1),xcorwa,xcorfg,xcorbe
       THW(ISPEC,1) = THW(ISPEC,1) / PI180
       TRACK(ISPEC,2) = TRACK(ISPEC,1)
       COST(ISPEC,2) = COST(ISPEC,1)
       U10(ISPEC,2) = U10(ISPEC,1)
       THW(ISPEC,2) = THW(ISPEC,1)
       READ(INUNIT) INTDUMMY, INTDUMMY,jqual, INTDUMMY
       READ(INUNIT)
     &      ((SPEC(ISPEC,IANG,IFRE,1),IANG=1,NANG),IFRE=1,NFRE)
       READ(INUNIT)
     &      ((SPEC(ISPEC,IANG,IFRE,2),IANG=1,NANG),IFRE=1,NFRE)
       READ(INUNIT) HARR
       ISPEC = MIN( ISPEC+1 , MSPEC )
       JSPEC = JSPEC + 1
      END DO
    1 JSPEC = JSPEC - 1
      IF( JSPEC.GT.MSPEC )THEN
        WRITE(6,*) 'WARNING! PARAMETER MSPEC IS TOO SMALL.'
        WRITE(6,*) 'COULD ONLY WORK WITH THE FIRST MSPEC SPECTRAS,'
        WRITE(6,*) 'BUT THE INPUT FILE CONTAINS ',JSPEC,' SPECTRAS.'
        WRITE(6,*) 'IT IS MSPEC = ',MSPEC,'.'
        WRITE(6,*) 'TO WORK WITH ALL SPECTRAS OF INPUT FILE'
        WRITE(6,*) 'CHANGE PARAMETER MSPEC IN PROGRAM PARTOUT!'
        WRITE(6,*) 'IT MUST BE MSPEC >= ',JSPEC,'!'
        WRITE(6,*) '(DO NOT FORGET TO MAKE SURE, THAT PARAMENTER'       
        WRITE(6,*) 'DIMSPEC IN SOBROUTINE SWELLSEP IS >= MSPEC!)'
      END IF

      NSPEC = MIN( JSPEC , MSPEC )
      WRITE(6,*) 'NSPEC = ',NSPEC
c
c     set cut off values caused by coding and decoding to zero.
c
      DO IANG = 1,NANG
        IF( IANG.LT.NANG )THEN
          IANGP1 = IANG + 1
        ELSE
          IANGP1 = 1
        END IF
        IF( IANG.GT.1 )THEN
          IANGM1 = IANG - 1
        ELSE
          IANGM1 = NANG
        END IF
        DO IFRE = 1,NFRE
          IFREP1 = MIN(IFRE+1,NFRE)         
          IFREM1 = MAX(IFRE-1,1)
          DO I = 1,2
            DO ISPEC = 1,NSPEC
              IF( SPEC(ISPEC,IANGP1,IFRE,I).LE.0.1E-2.AND.
     &            SPEC(ISPEC,IANGM1,IFRE,I).LE.0.1E-2.AND.
     &            SPEC(ISPEC,IANG,IFREP1,I).LE.0.1E-2.AND.
     &            SPEC(ISPEC,IANG,IFREM1,I).LE.0.1E-2
     &            ) SPEC(ISPEC,IANG,IFRE,I) = 0.
            END DO
          END DO
        END DO
      END DO
c
c     smooth sar spectra around 100m wave length cut off.
c
c
      DO ISPEC = 1,NSPEC
        ZERO1 = .TRUE.
        ZERO2 = .TRUE.
        IANG = 1
        DO WHILE( IANG.LE.NANG.AND.(ZERO1.OR.ZERO2) )
          IFRE = 1
          DO WHILE( IFRE.LE.NFRE.AND.(ZERO1.OR.ZERO2) )
            IF( SPEC(ISPEC,IANG,IFRE,1).NE.0. ) ZERO1 = .FALSE.
            IF( SPEC(ISPEC,IANG,IFRE,2).NE.0. ) ZERO2 = .FALSE.
            IFRE = IFRE + 1
          END DO
          IANG = IANG + 1
        END DO
        IF( ZERO1 ) WRITE(6,*) 'WARNING!',
     &    ' WAM FIRST GUESS SPECTRUM NUMBER ',ISPEC,' IS ZERO!'
        IF( ZERO2 ) WRITE(6,*) 'WARNING!',
     &    ' INVERTED SAR SPECTRUM NUMBER ',ISPEC,' IS ZERO!'
      END DO

      RETURN

      END

c
c------------------------------------------------------------------
c
      SUBROUTINE READSPEW( 
c            input unit
     &         INUNIT , 
c            dimensions
     &         MSPEC , NSPEC , NANG , NFRE , 
c            output
     &         SPEC ,LONG , LAT , DATE ,
     &         HST , FMEANT , THQT , TRACK , COST , 
     &         U10 , THW )
c
c------------------------------------------------------------------
c
c     purpose:
c     --------
c
c     reads  spectra in the format of the sar inversion program.
c
c
c     interface:
c     ----------
c
      IMPLICIT NONE
      INTEGER INUNIT, MSPEC, NSPEC, NANG, NFRE
c              dimensions
      DOUBLE PRECISION SPEC(0:MSPEC,NANG,NFRE,2)
c              2d spectra (1 denotes wam,2 denotes sar retrieved.
      DOUBLE PRECISION LONG(MSPEC,2),
     &     LAT(MSPEC,2), 
     &     DATE(MSPEC,2),
     &     HST(MSPEC,2),
     &     FMEANT(MSPEC,2),
     &     THQT(MSPEC,2),
     &     TRACK(MSPEC,2),
     &     COST(MSPEC,2),
     &     U10(MSPEC,2), 
     &     THW(MSPEC,2),
     &     CTIME
c                   longitude,latitude,time,significant wave 
c                   height, mean frequency,mean direction 
c                   of input spectra.time window.
c
c
c
c     variables:
c     ----------
c
      DOUBLE PRECISION PI, PI180
      INTEGER IANG, IFRE,ISP
c
c------------------------------------------------------------------
c------------------------------------------------------------------
c
c
c     read input from sar inversion program until end of file is 
c     reached.
c
c
      PI = 4*ATAN(1.)
      PI180 = 180. / PI
c
c     1.1 read wam and observed sar spectra for one time window.
c     ----------------------------------------------------------
c
 1100 CONTINUE
c
      READ(INUNIT) CTIME
      READ(INUNIT) NSPEC
      DO ISP=1,NSPEC
       READ(INUNIT) DATE(ISP,1),DATE(ISP,2)
       READ(INUNIT) LAT(ISP,1),LONG(ISP,1),U10(ISP,1),THW(ISP,1)
       THW(ISP,1) = THW(ISP,1)/PI180
       READ(INUNIT) ((SPEC(ISP,IANG,IFRE,1),IANG=1,NANG),
     &                                       IFRE=1,NFRE)
       READ(INUNIT) LAT(ISP,2),LONG(ISP,2),U10(ISP,2),THW(ISP,2)
       READ(INUNIT) ((SPEC(ISP,IANG,IFRE,2),IANG=1,NANG),
     &                                      IFRE=1,NFRE)
      END DO
c
      RETURN

      END

c
c------------------------------------------------------------------
c
      SUBROUTINE WRITEARROW( 
c            output unit
     &         OUTUNIT , 
c            dimensions
     &         MSPEC , NSPEC , MPART ,
c            input 
     &         PARTINFO,NPART , LONG, LAT , DATE,
     &         EMEAN,THQ,FMEAN,CONTROL)
cn     &         EMEAN,THQ,FMEAN,CONTROL,spreadp)
c
c------------------------------------------------------------------
c
c     purpose:
c     --------
c
c     writes out the arrows for program arrows on units
c     > outunit < - hs of partitionings
c     > outunit+1 < - mean wave length of partitionings
c
c
c     interface:
c     ----------
c
      IMPLICIT NONE
      INTEGER OUTUNIT 
c                output unit
      INTEGER MSPEC, NSPEC, MPART, NPART(MSPEC)
c                dimensions     
      INTEGER PARTINFO(MSPEC,MPART)
c             = 0 swell, =1 wind sea, =2 mixed wind sea swell.
      DOUBLE PRECISION LONG(MSPEC),
     &     LAT(MSPEC), 
     &     DATE(MSPEC),
     &     EMEAN(MSPEC,MPART),
     &     THQ(MSPEC,MPART), 
     &     FMEAN(MSPEC,MPART)
c                   longitude,latitude,time,significant wave 
c                   height, mean frequency,mean direction 
c                   of input spectra.
      LOGICAL CONTROL
c                   controls print output
c
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IPART
c                    loop indices
      INTEGER COLOR
      DOUBLE PRECISION ELOG, LAMBDA,TPG
c                    log of wave height > 0.5m, wave length
      DOUBLE PRECISION SHIFT, DEL
c                 assigns colors to the arrows (0<=shift<del|360)
      DOUBLE PRECISION PI, PI180, ZGRAV
c
c------------------------------------------------------------------
c

      PI = 4*ATAN(1.)
      PI180 = 180. / PI
      ZGRAV = 9.806
      TPG = ZGRAV/(2.*PI)
      SHIFT = 15.
      DEL = 60.

      WRITE(OUTUNIT+1,*) DATE(1)
      WRITE(OUTUNIT+1,*) 0
      WRITE(OUTUNIT,*) DATE(1)
      WRITE(OUTUNIT,*) 0
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          ELOG = 4.*SQRT(EMEAN(ISPEC,IPART))
c          ELOG = LOG(4.*SQRT(EMEAN(ISPEC,IPART))) + 0.5
c         IF( ELOG.LT.0 )THEN
          IF( .FALSE. )THEN
            IF( CONTROL )
     &        WRITE(6,*) 'DON''T WRITE OUT ARROW OF SPECTRA ',ISPEC,
     &        ' PARTITIONING ',IPART
          ELSE
            COLOR = PARTINFO(ISPEC,IPART) +1
CN            WRITE(OUTUNIT,*) LONG(ISPEC), LAT(ISPEC), ELOG,
         WRITE(OUTUNIT,*)ISPEC, LONG(ISPEC), LAT(ISPEC), ELOG,
     &          THQ(ISPEC,IPART)*PI180, COLOR
cn
cn         WRITE(*,*)'ispec =', ISPEC, spreadp(ispec,ipart,1)
            LAMBDA = TPG / (FMEAN(ISPEC,IPART)**2 )
            IF(LAMBDA.GT.900.) LAMBDA=1.
CN            WRITE(OUTUNIT+1,*) LONG(ISPEC), LAT(ISPEC), LAMBDA,
      WRITE(OUTUNIT+1,*)ISPEC, LONG(ISPEC), LAT(ISPEC), LAMBDA,
     &          THQ(ISPEC,IPART)*PI180, COLOR
          END IF
        END DO
      END DO
     
      RETURN

      END

c
c------------------------------------------------------------------
c
      SUBROUTINE WRITESPEC( 
c            output unit
     &         OUTUNIT , 
c            dimensions
     &         MSPEC , NASPEC,NSPEC , MPART , 
c            input 
     &       NPART , NANG , NFRE , SPEC , PART , WORK ,
     &       LONG , LAT , DATE , HST , FMEANT , THQT , TRACK , 
     &       COST ,U10 , THW , EMEAN , THQ , FMEAN , 
     &       TH0 , FRE1 , CO )
c
c------------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c     writes out spectra and their partitionings 
c     for program specol on unit
c     > outunit < 
c
c
c     interface:
c     ----------
c
      IMPLICIT NONE
      INTEGER OUTUNIT 
c               output unit
      INTEGER MSPEC, NSPEC, MPART, NANG, NFRE
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
C
C------------------------------------------------------------------
C
CN==
      write(321)NASPEC,NSPEC
      write(321)NPART
      write(321)EMEAN
CN==
      PI = 4*ATAN(1.)
      PI180 = 180 / PI
      ZGRAV = 9.806
      TWEG = 3 * PI / ZGRAV
      DELTANG = 2 * PI / NANG
      DO ISPEC = NASPEC,NSPEC
CN        WRITE(OUTUNIT) LONG(ISPEC),LAT(ISPEC),DATE(ISPEC),
       WRITE(OUTUNIT)ISPEC, LONG(ISPEC),LAT(ISPEC),DATE(ISPEC),
     &      DBLE(NANG),DBLE(NFRE),TH0,FRE1,CO
        WRITE(OUTUNIT) 4 * SQRT(HST(ISPEC))
        WRITE(OUTUNIT) THQT(ISPEC) * PI180
        WRITE(OUTUNIT) FMEANT(ISPEC)
        WRITE(OUTUNIT) U10(ISPEC)
        WRITE(OUTUNIT) THW(ISPEC)* PI180
        WRITE(OUTUNIT) 
     &    ((SPEC(ISPEC,IANG,IFRE),IANG=1,NANG),IFRE=1,NFRE)
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
          WRITE(OUTUNIT) LONG(ISPEC),LAT(ISPEC),DATE(ispec),
     &         DBLE(NANG), DBLE(NFRE),TH0,FRE1,CO
          WRITE(OUTUNIT) 4 * SQRT(EMEAN(ISPEC,IPART))
          WRITE(OUTUNIT) THQ(ISPEC,IPART)*PI180
          WRITE(OUTUNIT) FMEAN(ISPEC,IPART)
          WRITE(OUTUNIT) U10(ISPEC)
c          thwq = thw(ispec) / pi180
c          cm = tweg * fr1 * co ** (fmean(ispec,ipart)-1)
c          ct = cm * u10(ispec)
c          thqp = deltang * (thq(ispec,ipart)-1)
c          cte = ct * cos(thqp-thwq) - 1.
          WRITE(OUTUNIT) THW(ISPEC)* PI180
          WRITE(OUTUNIT) 
     &        ((WORK(IANG,IFRE),IANG=1,NANG),IFRE=1,NFRE)
         end if
        END DO
      END DO
     
      RETURN

      END
c     
c------------------------------------------------------------------
c
      SUBROUTINE WRITESPE( OUTUNIT , MSPEC , NASPEC,NSPEC ,
     &    NANG , NFRE , SPEC ,
     &    LONG , LAT , DATE , TRACK , COST , 
     &    U10 , THW , EMEAN , THQ , FMEAN , 
     &    TH0 , FRE1 , CO ,
     &    TRANSFORM )

c
c------------------------------------------------------------------
c
c     purpose:
c     --------
c
c     writes out the spectra for program specol on unit
c     > outunit < 
c
c
c     interface:
c     ----------
c
      IMPLICIT NONE
      INTEGER OUTUNIT 
c                   output unit
      INTEGER MSPEC, NSPEC, NANG, NFRE
c                   array dimensions.
      INTEGER NASPEC
c                   outpput starts at spectrum naspec.
      DOUBLE PRECISION SPEC(0:MSPEC,NANG,NFRE)
c                   2d spectrum
      DOUBLE PRECISION LONG(MSPEC),LAT(MSPEC),DATE(MSPEC),
     &TRACK(MSPEC),COST(MSPEC),U10(MSPEC), THW(MSPEC)
c                   longitude,latitude,time,
c                   satellite track,final cost,u10,wind direction.
      DOUBLE PRECISION EMEAN(MSPEC), THQ(MSPEC), FMEAN(MSPEC)
c                   integrated values of 2d spectrum.
      DOUBLE PRECISION TH0, FRE1, CO
      LOGICAL TRANSFORM
c
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IANG, IFRE
c                    loop indixes
      DOUBLE PRECISION PI, PI180, TWEG, DELTANG, ZGRAV
c
c--------------------------------------------------------------------
c
      PI = 4*ATAN(1.)
      PI180 = 180 / PI
      ZGRAV = 9.806
      TWEG = 3 * PI / ZGRAV
      DELTANG = 2 * PI / NANG

      DO ISPEC = NASPEC,NSPEC
        WRITE(OUTUNIT) LONG(ISPEC),LAT(ISPEC),DATE(ISPEC),
     &       DBLE(NANG), DBLE(NFRE),TH0,FRE1,CO
        WRITE(OUTUNIT) 4 * SQRT(EMEAN(ISPEC))
        WRITE(OUTUNIT) THQ(ISPEC) * PI180
        WRITE(OUTUNIT) FMEAN(ISPEC)
        WRITE(OUTUNIT) U10(ISPEC)
        WRITE(OUTUNIT) THW(ISPEC)* PI180
        WRITE(OUTUNIT) 
     &    ((SPEC(ISPEC,IANG,IFRE),IANG=1,NANG),IFRE=1,NFRE)
c
      END DO
     
      RETURN

      END
c
c------------------------------------------------------------------
c
      SUBROUTINE MEANST(
c                     dimensions
     &                  MSPEC , NSPEC , NANG , NFRE ,NFRE19,
c                     input
     &                  SPECW ,
c                     output
     &                  MEANTE , MEANTANG , MEANTFRE , SPREAD,
c                     work space
     &                  SUM0 , SUMX0 , SUMY0 ,
c                     input tables
     &                  FRE1 , CO , FRETAB , COSTAB , SINTAB,DFIM)
c
c------------------------------------------------------------------
c
c     purpose:
c     --------
c
c     mean values of spectra
c     computes mean energy,mean angle and mean frequency
c
c     interface:
c     ----------
c
      IMPLICIT NONE
      INTEGER  MSPEC, NSPEC, NANG, NFRE,NFRE100,NFRE19
      PARAMETER(NFRE100=12)
c                     dimensions.
      DOUBLE PRECISION SPECW(0:MSPEC,NANG,NFRE)
c                     2d spectrum.
      DOUBLE PRECISION MEANTE(MSPEC),
     &     MEANTANG(MSPEC), 
     &     MEANTFRE(MSPEC)
c                     mean parameters.
      DOUBLE PRECISION SPREAD(MSPEC)
c                     spectral spread
      DOUBLE PRECISION SUM0(MSPEC), SUMX0(MSPEC), SUMY0(MSPEC)
      DOUBLE PRECISION  SUMFXS(MSPEC), SUMFXQS(MSPEC),
     & SUMFYS(MSPEC), SUMFYQS(MSPEC), FXB(MSPEC), FYB(MSPEC),
     & SUM1, SUM2, FX, FY, SUMW1, SUMW2,
     & SUM1Q, SUM2Q, SUMW1Q,SUMW2Q
c                     work space for temporary sums.   
      DOUBLE PRECISION FRE1, CO
      DOUBLE PRECISION FRETAB(NFRE),COSTAB(NANG),SINTAB(NANG), 
     &DFIM(NFRE)
c                    tables of frequencies, cos,sine of directions,
c                    frequency increments/directional increment, 
c                    respectively.
c
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IANG, IFRE
c                     loop variables.
      DOUBLE PRECISION PI, PI2NANG, FACTOR
      DOUBLE PRECISION   EPSILON, SINTAVE, COSTAVE
c
c-------------------------------------------------------------------
c
c     initialize:
c     -----------

      PI = 4*ATAN(1.)
      PI2NANG = PI / 2 / NANG
c
      FRETAB(1) = FRE1
      DFIM(1) = (CO-1) * PI / NANG * FRETAB(1)
      DO IFRE = 2,NFRE-1
        FRETAB(IFRE) = FRETAB(IFRE-1) * CO
        DFIM(IFRE) = (CO-1) * PI / NANG * (FRETAB(IFRE)+
     &                                     FRETAB(IFRE-1))
      END DO
      FRETAB(NFRE) = FRETAB(NFRE-1) * CO
      DFIM(NFRE) = (CO-1) * PI / NANG * FRETAB(NFRE-1)
      DO IANG = 1,NANG
        COSTAB(IANG) = COS( 2*PI*(IANG-1)/NANG )
        SINTAB(IANG) = SIN( 2*PI*(IANG-1)/NANG )
      END DO
c
c     compute mean energies:
c     ----------------------
c
      DO ISPEC = 1,NSPEC
        MEANTE(ISPEC) = 0.
      END DO
      DO IFRE = 1,NFRE19
        DO ISPEC = 1,NSPEC
          SUM0(ISPEC) = 0.
        END DO
        DO IANG = 1,NANG
          DO ISPEC = 1,NSPEC
            SUM0(ISPEC) = SUM0(ISPEC) + SPECW(ISPEC,IANG,IFRE)
          END DO
        END DO
        DO ISPEC = 1,NSPEC
          MEANTE(ISPEC) = MEANTE(ISPEC) + DFIM(IFRE) * SUM0(ISPEC)
        END DO
      END DO
c
c     compute mean angles:
c     --------------------
c
c         sumx0    sin(theta) * meane
c         sumy0    cos(theta) * meane
c
      DO ISPEC = 1,NSPEC
        SUMX0(ISPEC) = 0.
        SUMY0(ISPEC) = 0.
      END DO

      DO IANG = 1,NANG
        DO ISPEC = 1,NSPEC
          SUM0(ISPEC) = 0.
        END DO
        DO IFRE=1,NFRE19
          DO ISPEC=1,NSPEC
            SUM0(ISPEC)
     &          = SUM0(ISPEC) + SPECW(ISPEC,IANG,IFRE) * DFIM(IFRE)
          END DO
        END DO
        DO ISPEC = 1,NSPEC
          SUMX0(ISPEC) = SUMX0(ISPEC) + COSTAB(IANG) * SUM0(ISPEC)
          SUMY0(ISPEC) = SUMY0(ISPEC) + SINTAB(IANG) * SUM0(ISPEC)
        END DO
      END DO

      DO ISPEC = 1,NSPEC
        IF( SUMY0(ISPEC).NE.0..OR.SUMX0(ISPEC).NE.0. )THEN
          MEANTANG(ISPEC) = ATAN2(SUMY0(ISPEC),SUMX0(ISPEC))
        ELSE
          MEANTANG(ISPEC) = 0.
        END IF
      END DO
C
C     COMPUTE SPECTRAL SPREAD: ref to S. Hasselmann (sumenery)
C     ------------------------
c      S. Hasselmann et.al. an improved algorithm...,JGR, 
c          101, C7 16615-16629,1996
c
c                  ---------   --------- 
c     ----------       --          --
c     delta(f)^2 = (fx-fx)^2 + (fy-fy)^2
c
c
c      with fx = f*cos(THETA), fy = f*sin(THETA)
c      The overbar denotes usual averages weighted with the 
c      spectral density.
c      preparations for the sprectral spread:
c      compute the energy weighted averages fxb and fyb
c 
c      sumw1 = X-angle sum
c      sumw2 = Y-angle sum
c      sum1  = X-frq sum
c      sum2  = Y-frq sum
c
c      the easy way
c
c      <(X - <X>)^2>  =  <X^2> - <X>^2
c
c      ie compute exptation values of X and X^2 and caculate the
c      difference
C                  
      DO ISPEC = 1,NSPEC
         SUM1 = 0.0
         SUM2 = 0.0
         SUM1Q = 0.0
         SUM2Q = 0.0
         DO IFRE = 1,NFRE
            SUMW1 = 0.0
            SUMW2 = 0.0  
            SUMW1Q = 0.0
            SUMW2Q = 0.0
            DO IANG = 1,NANG
               FX = FRETAB(IFRE) * COSTAB(IANG)
               FY = FRETAB(IFRE) * SINTAB(IANG)
               SUMW1 = SUMW1 + FX * SPECW(ISPEC,IANG,IFRE)
               SUMW2 = SUMW2 + FY * SPECW(ISPEC,IANG,IFRE)
               SUMW1Q = SUMW1Q + FX*FX * SPECW(ISPEC,IANG,IFRE)
               SUMW2Q = SUMW2Q + FY*FY * SPECW(ISPEC,IANG,IFRE)
            ENDDO
            SUM1 = SUM1+SUMW1*DFIM(IFRE)
            SUM2 = SUM2+SUMW2*DFIM(IFRE)
            SUM1Q = SUM1Q + SUMW1Q*DFIM(IFRE)
            SUM2Q = SUM2Q + SUMW2Q*DFIM(IFRE)               
         ENDDO
         SUM1 = SUM1/MEANTE(ISPEC)
         SUM2 = SUM2/MEANTE(ISPEC)
         SUM1Q = SUM1Q/MEANTE(ISPEC)
         SUM2Q = SUM2Q/MEANTE(ISPEC)
         SPREAD(ISPEC) = MAX(( SUM1Q - SUM1*SUM1 +
     &                         SUM2Q - SUM2*SUM2), 0.0D0)
         write(*,*)'SPREAD',SPREAD(1)
      ENDDO
c
c     compute mean frequencies:
c     -------------------------
        
      DO ISPEC = 1,NSPEC
        MEANTFRE(ISPEC) = 0.
      END DO

      DO IFRE = 1,NFRE19
        DO ISPEC = 1,NSPEC
          SUM0(ISPEC) = 0.
        END DO
        DO IANG = 1,NANG
          DO ISPEC = 1,NSPEC
            SUM0(ISPEC) = SUM0(ISPEC) + SPECW(ISPEC,IANG,IFRE)
          END DO
        END DO
        FACTOR = DFIM(IFRE) / FRETAB(IFRE)
        DO ISPEC = 1,NSPEC
          MEANTFRE(ISPEC) = MEANTFRE(ISPEC) + FACTOR * SUM0(ISPEC)
        END DO
      END DO

      FACTOR = 0.2 * 2 * PI / NANG
      DO ISPEC = 1,NSPEC
        MEANTFRE(ISPEC) = MEANTFRE(ISPEC) + FACTOR * SUM0(ISPEC)
        IF( MEANTFRE(ISPEC).NE.0. )THEN
          MEANTFRE(ISPEC) = MEANTE(ISPEC) / MEANTFRE(ISPEC)
        ELSE
          MEANTFRE(ISPEC) = 0.
        END IF
      END DO

      RETURN

      END
c
c-----------------------------------------------------------------
c
      SUBROUTINE WRITEMEAN( 
c                  output unit
     &               OUTUNIT ,
c                  dimensions
     &               MSPEC , NSPEC ,
c                  input
     &               LONG,LAT,DATE,EMEAN,THQ,FMEAN,CONTROL )
c
c------------------------------------------------------------------
c
c
c
c     purpose:
c     --------
c
c     output of 
c     > outunit   < - hs of total spectrum
c     > outunit+1 < - mean wave length of total spectrum
c
c
c     interface:
c     ----------
c
      IMPLICIT NONE
      INTEGER OUTUNIT
c                     output unit .
      INTEGER MSPEC, NSPEC
c                     array dimensions.
      DOUBLE PRECISION LONG(MSPEC),LAT(MSPEC),DATE(MSPEC),
     &EMEAN(MSPEC),THQ(MSPEC), FMEAN(MSPEC)
c                   longitude,latitude,time,
c                   integrated values.
      LOGICAL CONTROL
c
c     local  variables:
c     -----------------
c
      INTEGER ISPEC
c                    loop index.
      INTEGER COLOR
      DOUBLE PRECISION ELOG, LAMBDA
c                    log(hs), wave number.
      DOUBLE PRECISION SHIFT, DEL
c                    assigns colors to the arrows (0<=shift<del|360)
      DOUBLE PRECISION PI, PI180
c
c------------------------------------------------------------------
c
      PI = 4*ATAN(1.)
      PI180 = 180. / PI

      SHIFT = 15.
      DEL = 60.

      WRITE(OUTUNIT,*) DATE(1)
      WRITE(OUTUNIT,*) 0
      WRITE(OUTUNIT+1,*) DATE(1)
      WRITE(OUTUNIT+1,*) 0
      DO ISPEC = 1,NSPEC
       ELOG = 4.*SQRT(EMEAN(ISPEC))
       IF( .FALSE. )THEN
        IF( CONTROL )
     &     WRITE(6,*) 'DON''T WRITE OUT ARROW OF SPECTRA ',ISPEC
       ELSE
        COLOR = INT( (THQ(ISPEC)*PI180-SHIFT+DEL) / DEL )
        IF( COLOR.LE.0 ) COLOR = INT( (360.-SHIFT+DEL) / DEL )
CN        WRITE(OUTUNIT,*) LONG(ISPEC), LAT(ISPEC), ELOG,
        WRITE(OUTUNIT,*)ISPEC, LONG(ISPEC), LAT(ISPEC), ELOG,
     &          THQ(ISPEC)*PI180, COLOR,DATE(ISPEC)
        LAMBDA = 9.806 / (2.*PI*FMEAN(ISPEC)**2 )
        IF(LAMBDA.GT.900.) LAMBDA=1.
CN        WRITE(OUTUNIT+1,*) LONG(ISPEC), LAT(ISPEC), LAMBDA,
      WRITE(OUTUNIT+1,*)ISPEC, LONG(ISPEC), LAT(ISPEC), LAMBDA,
     &          THQ(ISPEC)*PI180, COLOR,DATE(ISPEC)
       END IF
      END DO
     
      RETURN

      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE MEAN100(
c                   dimensions
     &                DIMSPEC , MSPEC , NSPEC ,
     &                DIMPART , MPART , NPART ,
     &                DIMANG , NANG , DIMFRE , NFRE , NFRE100,
c                   input
     &                SPEC , PART ,
c                   output
     &                MEANE , MEANANG , MEANFRE ,
c                   work space.
     &                SUM0 , SUMX0 , SUMY0 ,
c                   input tables
     &                FRETAB , COSTAB , SINTAB , DFIM,DFIMW,WEIGHT )
c
c-----------------------------------------------------------------------
c
c     purpose:
c     --------
c
c     computes mean directions and mean frequencies of 2d spectra 
c     and their partitionings up to the wave number cut off of 
c     100m wave length.
c
c     interface:
c     ----------
c
      IMPLICIT NONE
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMPART, MPART, NPART(MSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
c                 array dimensions.
      DOUBLE PRECISION SPEC(0:MSPEC,NANG,NFRE)
c                 2d spectra.
      INTEGER PART(MSPEC,NANG,NFRE)
c                 part(..) gives number of partitioning for each 
c                 spectral bin.
      DOUBLE PRECISION MEANE(MSPEC,MPART),
     &     MEANANG(MSPEC,MPART), MEANFRE(MSPEC,MPART)
c                 integrated values of partitionings.
      DOUBLE PRECISION SUM0(DIMSPEC,DIMPART),
     &     SUMX0(DIMSPEC,DIMPART),SUMY0(DIMSPEC,DIMPART)
c                 for temporary sums
      DOUBLE PRECISION FRETAB(DIMFRE),COSTAB(DIMANG),SINTAB(DIMANG),
     &     DFIM(DIMFRE),DFIMW(DIMFRE)
c                  table of frequencies,cos,sin,
c                  freq.increment/directional increment.
c
c     local variables:
c     ----------------
c
      INTEGER NFRE100
      INTEGER ISPEC, IPART, IANG, IFRE
c                   loop indexes.
      DOUBLE PRECISION PI, FACTOR,PI2NANG,WEIGHT
c
c-----------------------------------------------------------------------
c
      PI = 4*ATAN(1.)
      PI2NANG = PI / 2 / NANG
c
c     0. compute mean energy
c     ----------------------
c
      IF(INT(WEIGHT).GT.1) THEN
       DO IFRE=1,NFRE100
        DFIMW(IFRE)=DFIM(IFRE)/FRETAB(IFRE)
       END DO
      ELSE
       DO IFRE=1,NFRE100
        DFIMW(IFRE)=DFIM(IFRE)
       END DO
      END IF
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
         MEANE(ISPEC,IPART) = 0.1D-90
        END DO
      END DO
      DO IFRE = 1,NFRE100
        DO ISPEC = 1,NSPEC
         DO IPART = 1,NPART(ISPEC)
          SUM0(ISPEC,IPART) = 0.
         END DO
        END DO
        DO IANG = 1,NANG
          DO ISPEC = 1,NSPEC
            SUM0(ISPEC,PART(ISPEC,IANG,IFRE)) = 
     1             SUM0(ISPEC,PART(ISPEC,IANG,IFRE))
     2             + SPEC(ISPEC,IANG,IFRE)
          END DO
        END DO
        DO ISPEC = 1,NSPEC
         DO IPART = 1,NPART(ISPEC)
          MEANE(ISPEC,IPART) = MEANE(ISPEC,IPART) + DFIMW(IFRE) * 
     &                         SUM0(ISPEC,IPART)
         END DO
        END DO
      END DO
c
c     add tail energy
c 
      IF(NFRE100.EQ.NFRE) THEN 
       DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
         MEANE(ISPEC,IPART)
     &       = MEANE(ISPEC,IPART) + FRETAB(NFRE) * PI2NANG * 
     &        SUM0(ISPEC,IPART)
        END DO
       END DO
      END IF
c
c     1. compute mean directions.
c     --------------------------

      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          SUMX0(ISPEC,IPART) = 0.1E-10
          SUMY0(ISPEC,IPART) = 0.1E-10
        END DO
      END DO
c
      DO IANG = 1,NANG
        DO ISPEC = 1,NSPEC
          DO IPART = 1,NPART(ISPEC)
            SUM0(ISPEC,IPART) = 0
          END DO
        END DO
        DO IFRE=1,NFRE100

         DO ISPEC=1,NSPEC
            SUM0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          = SUM0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          + SPEC(ISPEC,IANG,IFRE) * DFIMW(IFRE)
          END DO
        END DO
        DO ISPEC = 1,NSPEC
          DO IPART = 1,NPART(ISPEC)
            SUMX0(ISPEC,IPART) = SUMX0(ISPEC,IPART) 
     &          + COSTAB(IANG) * SUM0(ISPEC,IPART)
            SUMY0(ISPEC,IPART) = SUMY0(ISPEC,IPART) 
     &          + SINTAB(IANG) * SUM0(ISPEC,IPART)
          END DO
         END DO
      END DO

      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          IF(ABS(SUMY0(ISPEC,IPART)).LT.0.1E-10) 
     &      SUMY0(ISPEC,IPART)=0.1E-10
          IF(ABS(SUMX0(ISPEC,IPART)).LT.0.1E-10) 
     &      SUMX0(ISPEC,IPART)=0.1E-10
          MEANANG(ISPEC,IPART)
     &        = ATAN2(SUMY0(ISPEC,IPART),SUMX0(ISPEC,IPART))
        END DO
      END DO
c
c----------------------------------------------------------------------
c
c    2. compute mean frequency.
c    --------------------------
        
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          MEANFRE(ISPEC,IPART) = 0.1D-180
        END DO
      END DO

      DO IFRE = 1,NFRE100
        DO ISPEC = 1,NSPEC
          DO IPART = 1,NPART(ISPEC)
            SUM0(ISPEC,IPART) = 0
          END DO
        END DO
        DO IANG = 1,NANG


          DO ISPEC = 1,NSPEC
            SUM0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          = SUM0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          + SPEC(ISPEC,IANG,IFRE)
          END DO
        END DO
        FACTOR = DFIMW(IFRE) / FRETAB(IFRE)
        DO ISPEC = 1,NSPEC
          DO IPART = 1,NPART(ISPEC)
            MEANFRE(ISPEC,IPART) = MEANFRE(ISPEC,IPART)
     &          + FACTOR  * SUM0(ISPEC,IPART)
          END DO
        END DO
      END DO

      FACTOR = 0.2 * 2 * PI / NANG
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          MEANFRE(ISPEC,IPART) = MEANFRE(ISPEC,IPART)
     &        + FACTOR * SUM0(ISPEC,IPART)
          if(MEANFRE(ISPEC,IPART).lt.0.1e-10) then
           write(6,*) ' meanfre=0 ,ISPEC,IPART ',ISPEC,IPART
           MEANFRE(ISPEC,IPART)=1
           MEANE(ISPEC,IPART)=0.1e-10
c           stop7
          end if
          MEANFRE(ISPEC,IPART)
     &        = MEANE(ISPEC,IPART) / MEANFRE(ISPEC,IPART)
        END DO
      END DO

      RETURN

      END
c
c------------------------------------------------------------------
c
      FUNCTION RAD2DEG(ANGLE)
c
c    converts direction from radiant to degree
c    range (0,360)
c
c------------------------------------------------------------------
c------------------------------------------------------------------
      IMPLICIT NONE
      DOUBLE PRECISION PI
      PARAMETER (PI=3.141592653589797)
      DOUBLE PRECISION   RAD2DEG, ANGLE
c
      RAD2DEG = ANGLE*180.0/PI
      IF (RAD2DEG .LT. 0.0) RAD2DEG=360.0+RAD2DEG
      IF (RAD2DEG .GT. 360.0) RAD2DEG = DMOD(RAD2DEG,360.0D0)
c
c      rad2deg =90.0+rad2deg
c
      RETURN
      END
c
c----------------------------------------------------------------------
c
      SUBROUTINE OUTPOPRO(
c                   dimensions
     &                MSPEC , MPART ,
c                   input
     &                SPREADT,SPREADP,NPART,NSPEC,PI,PARTINFO,
     &                CORRELTAW,CORRELTAS,MEANE,MEANFRE,HST,FMEANT
CN     &                ,MEANANG,THQT)
     &                ,MEANANG,THQT,U10,THW)
c
c----------------------------------------------------------------------
c
c      purpose.
c      --------
c      special output for postprocessing at the MPI.
c
c----------------------------------------------------------------------
c
c     interface variables:
c     --------------------
c
      IMPLICIT NONE
      INTEGER  MSPEC, NSPEC, MPART, NPART(MSPEC,2)
c                   array dimensions.
      INTEGER PARTINFO(MSPEC,MPART,2)
c                   information for windsea-swell:
c                   windsea (1), mixed (=2), or swell (=0)       
c                   (there is no more than one windsea partioning)
      INTEGER CORRELTAW(MSPEC,MPART),CORRELTAS(MSPEC,MPART)
c                   crossassigns wam and sar partitionings.
c                   correltaw(ispec,ipartwam)=ipartsar
c                   correltas like correltaw sar - wam.
      DOUBLE PRECISION MEANE(MSPEC,MPART,2),
     &     MEANANG(MSPEC,MPART,2), MEANFRE(MSPEC,MPART,2)
c                 integrated values of partitionings.
      DOUBLE PRECISION  HST(MSPEC,2),FMEANT(MSPEC,2),
     &      THQT(MSPEC,2)
c                wave height, mean frequency,mean direction of 
C                input spectra.
      DOUBLE PRECISION 
     &     SPREADT(MSPEC,2),
     &     SPREADP(MSPEC,MPART,2)
c                   spectral spread of total and partitioned spectra.
c                   after meanst and swellsep.c
      DOUBLE PRECISION PI
CN==      
      DOUBLE PRECISION U10(MSPEC),THW(MSPEC)
CN==      
c      local variables.
c      -----------------
c       statistical parameters of the partitionings
c       variables for additional output
c       mean significant wave height
      DOUBLE PRECISION XMEANHS(0:3,2)
c       energy weighted averages
      DOUBLE PRECISION XMEANDIR(0:3,2), ANGLE
      DOUBLE PRECISION XMEANSIN(0:3,2), XMEANCOS(0:3,2)
      DOUBLE PRECISION XMEANFREQ(0:3,2)
      DOUBLE PRECISION XMEANSPREAD(0:3,2)
c
c           iwrong   : number of cross assigned wave systems 
c                      of different kind
c           inopartw : number of input wave partitionings 
c                      without cross assigned partner
c           inoparts :             SAR
c
      INTEGER INOPARTW, INOPARTS, IWRONG, I, J
c       workspace
      DOUBLE PRECISION     TMPSIN, TMPCOS
      DOUBLE PRECISION     WINADD_WAM, WINADD_SAR
      INTEGER  INDEX,ISPEC,ISPA
      DOUBLE PRECISION RAD2DEG
      EXTERNAL RAD2DEG
cn
      DOUBLE PRECISION  DATE(MSPEC,mpart,1)
c
c----------------------------------------------------------------------
      IWRONG = 0
      INOPARTW = 0
      INOPARTS = 0
      DO ISPEC = 1, NSPEC
c init meanhs
       DO I = 1, 2
        DO J = 0,3
         XMEANHS(J,I) = 0.0
         XMEANDIR(J,I) = 0.0
         XMEANSIN(J,I) = 0.0
         XMEANCOS(J,I) = 0.0
         XMEANFREQ(J,I) = 0.0
         XMEANSPREAD(J,I) = 0.0
        END DO
       END DO       
       DO ISPA = 1, NPART(ISPEC,1)
c       sum energy of swell, winsea etc 
        XMEANHS(PARTINFO(ISPEC,ISPA,1),1) = 
     =       XMEANHS(PARTINFO(ISPEC,ISPA,1),1) + MEANE(ISPEC,ISPA,1)
c       sum frequency energy weighted
        XMEANFREQ(PARTINFO(ISPEC,ISPA,1),1) = 
     &         XMEANFREQ(PARTINFO(ISPEC,ISPA,1),1) 
     &         + MEANFRE(ISPEC,ISPA,1)* MEANE(ISPEC,ISPA,1)
c
c       sum spread energy weighted
        XMEANSPREAD(PARTINFO(ISPEC,ISPA,1),1) = 
     &         XMEANSPREAD(PARTINFO(ISPEC,ISPA,1),1) 
     &         + SPREADP(ISPEC,ISPA,1)* MEANE(ISPEC,ISPA,1)
c
c       sum direction energy weighted
        ANGLE = MEANANG(ISPEC,ISPA,1)
        IF(ANGLE .LT. -PI) THEN
         PRINT*,ANGLE, ISPEC, ISPA
         STOP 'ERROR: ANGLE < -PI'
        ELSE IF(ANGLE .GT. PI) THEN
         PRINT*,ANGLE, ISPEC, ISPA
         STOP 'ERROR: ANGLE > PI'
        ENDIF
        XMEANSIN(PARTINFO(ISPEC,ISPA,1),1) = 
     &         XMEANSIN(PARTINFO(ISPEC,ISPA,1),1) 
     &         + SIN(ANGLE)*MEANE(ISPEC,ISPA,1)
        XMEANCOS(PARTINFO(ISPEC,ISPA,1),1) = 
     &         XMEANCOS(PARTINFO(ISPEC,ISPA,1),1) 
     &         + COS(ANGLE)*MEANE(ISPEC,ISPA,1)
c
c       if we found a correlating wave system
        IF(CORRELTAW(ISPEC,ISPA).NE.0) THEN 
         WRITE(49,'(2F10.6,1X,2F12.4,1X,2F10.6,1X,2F10.6,1X,3I3)') 
     &           4*SQRT(MEANE(ISPEC,ISPA,1)),
     &           4*SQRT(MEANE(ISPEC,CORRELTAW(ISPEC,ISPA),2)),
     &           RAD2DEG(MEANANG(ISPEC,ISPA,1)),
     &           RAD2DEG(MEANANG(ISPEC,CORRELTAW(ISPEC,ISPA),2)),
     &           MEANFRE(ISPEC,ISPA,1),
     &           MEANFRE(ISPEC,CORRELTAW(ISPEC,ISPA),2),
     &           SPREADP(ISPEC,ISPA,1),
     &           SPREADP(ISPEC,CORRELTAW(ISPEC,ISPA),2),
     &           PARTINFO(ISPEC,ISPA,1),
     &           PARTINFO(ISPEC,CORRELTAW(ISPEC,ISPA),2),
     &           ISPEC
c        count how many 'incorrect' correlations we have
         IF (PARTINFO(ISPEC,ISPA,1).NE.
     &            PARTINFO(ISPEC,CORRELTAW(ISPEC,ISPA),2)) 
     &            IWRONG = IWRONG + 1
        ELSE
c       count how many wave systems found no corresponding one
        INOPARTW = INOPARTW + 1
        END IF
c       write statistics of all input partitionings
c       to unit 47            
c        write(*,*)'SPREADP=',SPREADP(ISPEC,ISPA,1),
c     1   SQRT(SPREADP(ISPEC,ISPA,1))
CN        WRITE(47,'(F10.6,1X,F12.4,2(1X,F10.6),1X,3I3)')
        WRITE(47,'(F10.6,1X,F12.4,2(1X,F10.6),1X,3I3,1X,2(F8.4,2X) )')
     &           4*SQRT(MEANE(ISPEC,ISPA,1)),
     &           RAD2DEG(MEANANG(ISPEC,ISPA,1)),
     &           MEANFRE(ISPEC,ISPA,1),
     &           SQRT(SPREADP(ISPEC,ISPA,1)),
     &           PARTINFO(ISPEC,ISPA,1),
     &           CORRELTAW(ISPEC,ISPA), ISPEC
CN==     
     &           ,u10(ispec),thw(ispec)*180/3.141592
CN==     
       END DO
c
c      loop over all SAR partitionings
       DO ISPA = 1, NPART(ISPEC,2) 
c       sum energy of swell, winsea etc 
        XMEANHS(PARTINFO(ISPEC,ISPA,2),2) = 
     =      XMEANHS(PARTINFO(ISPEC,ISPA,2),2) + MEANE(ISPEC,ISPA,2)
c       sum  energy weighted direction
        ANGLE = MEANANG(ISPEC,ISPA,2)
       IF(ANGLE .LT. -PI) THEN
         PRINT*,ANGLE, ISPEC, ISPA
         STOP 'ERROR: ANGLE < -PI'
       ELSE IF(ANGLE .GT. PI) THEN
         PRINT*,ANGLE, ISPEC, ISPA
         STOP 'ERROR: ANGLE > PI'
       ENDIF
       XMEANSIN(PARTINFO(ISPEC,ISPA,2),2) = 
     &         XMEANSIN(PARTINFO(ISPEC,ISPA,2),2) 
     &         + SIN(ANGLE)*MEANE(ISPEC,ISPA,2)
       XMEANCOS(PARTINFO(ISPEC,ISPA,2),2) = 
     &         XMEANCOS(PARTINFO(ISPEC,ISPA,2),2) 
     &         + COS(ANGLE)*MEANE(ISPEC,ISPA,2)
c
c      sum energy weighted frequency
       XMEANFREQ(PARTINFO(ISPEC,ISPA,2),2) = 
     &         XMEANFREQ(PARTINFO(ISPEC,ISPA,2),2) 
     &         + MEANFRE(ISPEC,ISPA,2)* MEANE(ISPEC,ISPA,2)
c
c      sum energy weighted spread
       XMEANSPREAD(PARTINFO(ISPEC,ISPA,2),2) = 
     &         XMEANSPREAD(PARTINFO(ISPEC,ISPA,2),2) 
     &         + SPREADP(ISPEC,ISPA,2)* MEANE(ISPEC,ISPA,2)
c
       WRITE(48,'(F10.6,1X,F12.4,1X,2(F10.6,1X),3I3)')
     &           4*SQRT(MEANE(ISPEC,ISPA,2)),
     &           RAD2DEG(MEANANG(ISPEC,ISPA,2)),
     &           MEANFRE(ISPEC,ISPA,2),
     &           SQRT(SPREADP(ISPEC,ISPA,2)),
     &           PARTINFO(ISPEC,ISPA,2),
     &           CORRELTAS(ISPEC,ISPA),ISPEC
c      count how many wave systems found no corresponding one
       IF (CORRELTAS(ISPEC,ISPA).EQ.0) INOPARTS = INOPARTS + 1
      END DO
c       end loop over all sar partitionings
c       write energy of swell, windsea, etc. for each spectrum
        WRITE(46,'(8F12.5,X,3I3)') 
CN        WRITE(46,'(8F12.5,X,3I3,)') 
c       sum windsea (1) and old windsea (3) together
     &        4*SQRT(XMEANHS(1,1)+ XMEANHS(3,1)),
     &        4*SQRT(XMEANHS(1,2)+ XMEANHS(3,2)),
c       mixed (2)
     &        4*SQRT(XMEANHS(2,1)),
     &        4*SQRT(XMEANHS(2,2)),
c       swell (0)
     &        4*SQRT(XMEANHS(0,1)),
     &        4*SQRT(XMEANHS(0,2)),
c       full hs
     &        4*SQRT(HST(ISPEC,1)),
     &        4*SQRT(HST(ISPEC,2)),
c       number of partitionings
     &        NPART(ISPEC,1),
     &        NPART(ISPEC,2),
c       other mean values
     &        ISPEC
c
c       compute mean direction, frequency, and spread for different 
c       wave systems:
c-------------------------------------------------------------------
c        wind, old wind, swell, and mixed wind sea
c        the means are energy weighted means
c        normalize dir, freq and spread
c
         DO I = 1, 2
          DO J = 0,3
           IF (XMEANHS(J,I) .NE. 0.0) THEN
c           direction --> grad (0.0, 360]
             XMEANSIN(J,I) = XMEANSIN(J,I) / XMEANHS(J,I)
             XMEANCOS(J,I) = XMEANCOS(J,I) / XMEANHS(J,I)
             IF( XMEANSIN(J,I).NE.0..OR.XMEANCOS(J,I).NE.0. )THEN
              XMEANDIR(J,I) = ATAN2(XMEANSIN(J,I),XMEANCOS(J,I))
             ELSE
              XMEANDIR(J,I) = 0.0
             ENDIF
             XMEANDIR(J,I) = RAD2DEG(XMEANDIR(J,I))
             XMEANFREQ(J,I) = XMEANFREQ(J,I) / XMEANHS(J,I)
             XMEANSPREAD(J,I) = XMEANSPREAD(J,I) / XMEANHS(J,I) 
             XMEANSPREAD(J,I) = SQRT(XMEANSPREAD(J,I))
            ELSE
c            direction --> grad (0.0, 360]
             XMEANDIR(J,I) = 9999.9
             XMEANFREQ(J,I) = 9999.9
             XMEANSPREAD(J,I) = 9999.9
            ENDIF
           END DO
         END DO
c
c       compute mean direction
c       -----------------------
c       sum up windsea and old windsea directions for wam
        IF (XMEANHS(1,1) .NE. 0.0 .AND. XMEANHS(3,1) .NE. 0.0) THEN
         TMPSIN = 
     &          (XMEANSIN(1,1)*XMEANHS(1,1)+ XMEANSIN(3,1)*XMEANHS(3,1))
     &          / (XMEANHS(1,1)*XMEANHS(3,1))
         TMPCOS = 
     &          (XMEANCOS(1,1)*XMEANHS(1,1)+ XMEANCOS(3,1)*XMEANHS(3,1))
     &          / (XMEANHS(1,1)*XMEANHS(3,1))
         WINADD_WAM = RAD2DEG(ATAN2(TMPSIN, TMPCOS) )
        ELSE IF (XMEANHS(1,1) .NE. 0.0) THEN
         WINADD_WAM = XMEANDIR(1,1)
        ELSE IF (XMEANHS(3,1) .NE. 0.0) THEN
         WINADD_WAM = XMEANDIR(3,1)
        ELSE
         WINADD_WAM = 9999.9
        ENDIF
c
c sum up windsea and old windsea directions for sar
        IF (XMEANHS(1,2) .NE. 0.0 .AND. XMEANHS(3,2) .NE. 0.0) THEN
         TMPSIN = 
     &        (XMEANSIN(1,2)*XMEANHS(1,2)+ XMEANSIN(3,2)*XMEANHS(3,2))
     &          / (XMEANHS(1,2)*XMEANHS(3,2))
         TMPCOS = 
     &        (XMEANCOS(1,2)*XMEANHS(1,2)+ XMEANCOS(3,2)*XMEANHS(3,2))
     &          / (XMEANHS(1,2)*XMEANHS(3,2))
         WINADD_WAM = RAD2DEG(ATAN2(TMPSIN, TMPCOS))
        ELSE IF (XMEANHS(1,2) .NE. 0.0) THEN
         WINADD_SAR = XMEANDIR(1,2)
        ELSE IF (XMEANHS(3,2) .NE. 0.0) THEN
         WINADD_SAR = XMEANDIR(3,2)
        ELSE
         WINADD_SAR = 9999.9
        ENDIF
c
c       unit 44: directional data
c
        WRITE(44,'(8F12.5,X,3I3)') 
c       sum of windsea (1) and old windsea (3)
     &         WINADD_WAM, WINADD_SAR,
c       mixed (2)
     &        (XMEANDIR(2,1)),
     &        (XMEANDIR(2,2)),
c       swell (0)
     &        (XMEANDIR(0,1)),
     &        (XMEANDIR(0,2)),
c       total mean direction
     &        RAD2DEG(THQT(ISPEC,1)),
     &        RAD2DEG(THQT(ISPEC,2)),
c       number of partitionings
     &        NPART(ISPEC,1),
     &        NPART(ISPEC,2),
c       spectrum number
     &        ISPEC
c
c       compute mean frequency
c       ------------------------
c       sum up windsea (1) and old windsea (3) frequencies for wam
        IF (XMEANHS(1,1) .NE. 0.0 .AND. XMEANHS(3,1) .NE. 0.0) THEN
         WINADD_WAM = 
     &        (XMEANFREQ(1,1)*XMEANHS(1,1)+ XMEANFREQ(3,1)*XMEANHS(3,1))
     &       / (XMEANHS(1,1)*XMEANHS(3,1))
        ELSE IF (XMEANHS(1,1) .NE. 0.0) THEN
         WINADD_WAM = XMEANFREQ(1,1)
        ELSE IF (XMEANHS(3,1) .NE. 0.0) THEN
         WINADD_WAM = XMEANFREQ(3,1)
        ELSE
         WINADD_WAM = 9999.9
        ENDIF
c
c add windsea (1) and old windsea (3) frequencies for sar
        IF (XMEANHS(1,2) .NE. 0.0 .AND. XMEANHS(3,2) .NE. 0.0) THEN
         WINADD_SAR = 
     &        (XMEANFREQ(1,2)*XMEANHS(1,2)+ XMEANFREQ(3,2)*XMEANHS(3,2))
     &          / (XMEANHS(1,2)*XMEANHS(3,2))
        ELSE IF (XMEANHS(1,2) .NE. 0.0) THEN
         WINADD_SAR = XMEANFREQ(1,2)
        ELSE IF (XMEANHS(3,2) .NE. 0.0) THEN
         WINADD_SAR = XMEANFREQ(3,2)
        ELSE
         WINADD_SAR = 9999.9
        ENDIF
c
c       unit 43: frequency data
c
        WRITE(43,'(8F12.5,X,3I3)') 
c       sum of windsea (1) and old windsea (3)
     &     WINADD_WAM, WINADD_SAR,
c       mixed (2)
     &        (XMEANFREQ(2,1)),
     &        (XMEANFREQ(2,2)),
c       swell (0)
     &        (XMEANFREQ(0,1)),
     &        (XMEANFREQ(0,2)),
c       full mean frequency
     &        (FMEANT(ISPEC,1)),
     &        (FMEANT(ISPEC,2)),
c       number of partitionings
     &        NPART(ISPEC,1),
     &        NPART(ISPEC,2),
c       spectrum number
     &        ISPEC
c
c       compute mean spread
c       ---------------------
c       sum up windsea (1) and old windsea (3) spread for wam
        IF (XMEANHS(1,1) .NE. 0.0 .AND. XMEANHS(3,1) .NE. 0.0) THEN
         WINADD_WAM = 
     &   (XMEANSPREAD(1,1)*XMEANHS(1,1)+ XMEANSPREAD(3,1)*XMEANHS(3,1))
     &       / (XMEANHS(1,1)*XMEANHS(3,1))
        ELSE IF (XMEANHS(1,1) .NE. 0.0) THEN
         WINADD_WAM = XMEANSPREAD(1,1)
        ELSE IF (XMEANHS(3,1) .NE. 0.0) THEN
         WINADD_WAM = XMEANSPREAD(3,1)
        ELSE
         WINADD_WAM = 9999.9
        ENDIF
c
c       add windsea (1) and old windsea (3) spreads for sar
        IF (XMEANHS(1,2) .NE. 0.0 .AND. XMEANHS(3,2) .NE. 0.0) THEN
         WINADD_SAR = 
     &    (XMEANSPREAD(1,2)*XMEANHS(1,2)+ XMEANSPREAD(3,2)*XMEANHS(3,2))
     &          / (XMEANHS(1,2)*XMEANHS(3,2))
        ELSE IF (XMEANHS(1,2) .NE. 0.0) THEN
         WINADD_SAR = XMEANSPREAD(1,2)
        ELSE IF (XMEANHS(3,2) .NE. 0.0) THEN
         WINADD_SAR = XMEANSPREAD(3,2)
        ELSE
         WINADD_SAR = 9999.9
        ENDIF
c
c       unit 42: spread data
c
        WRITE(42,'(8F12.5,X,3I3)') 
c       sum of windsea (1) and old windsea (3)
     &     WINADD_WAM, WINADD_SAR,
c       mixed (2)
     &        (XMEANSPREAD(2,1)),
     &        (XMEANSPREAD(2,2)),
c       swell (0)
     &        (XMEANSPREAD(0,1)),
     &        (XMEANSPREAD(0,2)),
c       spread of total spectrum
     &         SQRT(SPREADT(ISPEC,1)),
     &         SQRT(SPREADT(ISPEC,2)),
c       number of partitionings
     &        NPART(ISPEC,1),
     &        NPART(ISPEC,2),
c       spectrum number
     &        ISPEC
c
      END DO
      WRITE(45,'(4I5)') NSPEC, IWRONG, INOPARTW, INOPARTS
      RETURN
      END

