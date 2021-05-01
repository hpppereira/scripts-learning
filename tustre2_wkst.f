C------------------------------------------------
C @(#)Last modified by:   Christian Bennefeld
C Module name:        tustre2.f
C @(#)Version:      2.2
C Qualified:          Sources
C @(#)Module type:  FORTRAN-Source-Code
C Fetch date:         97/02/24
C @(#)Last update:  97/02/10 17:49:37
C Sourcepath:         /pf/m/m210012/sar_cycle_2/part/SCCS/s.tustre2.f
C------------------------------------------------
C-------------------------------------------------------------------
C
      SUBROUTINE TUSTRE(
C           DIMENSIONS
     &            MSPEC , NSPEC , MPART , NPARTW ,NPARTS,
     &            NANG , NFRE ,
C           INPUT (FOR SPECTRUM ALSO OUTPUT)
     &            SPECW ,SPECS , PARTW , PARTS, CORRELTAW ,  
     &            CORRELTAS, MEANWE , MEANWANG , 
     &            MEANWFRE, MEANSE , MEANSANG , MEANSFRE ,
C           OUTPUT
     &            MEANTE , MEANTANG , MEANTFRE ,
C           INPUT PARAMETERS 
     &            FRE1 , CO , CONTROL )
C
C-------------------------------------------------------------------
      IMPLICIT NONE
C
C
C     PURPOSE:
C     --------
C
C     FOR SAR RETRIEVAL
C
C     TRANSFORMS PARTITIONINGS OF WAM FIRST GUESS SPECTRA TO MEAN 
C     PARAMETERS OF INVERTED SAR SPECTRA.
C
C     TO MAKE THIS ROUTINE AS FAST AS POSSIBLE, THE LOOP OVER 
C     ALL SPECTRA ARE VECTORIZED INNER LOOP.
C
C
C     METHOD:
C     -------
C
C     THE WAM FIRST GUESS PARTITIONINGS ARE ROTATED,
C     STRETCHED TO MATCH THE MEAN ENERGY, MEAN DIRECTION,
C     AND MEAN FREQUENCY OF THE PARTITIONINGS OF THE 
C     INVERTED SAR SPECTRA. THE PARTITIONINGS ARE SUPER IMPOSED 
C     TO DERIVE ONE COMBINED WAVE SPECTRUM. 
C     GAPS BETWEEN TWO PARTITIONINGS ARE 
C     INTERPOLATED BY A 2D PARABOLIC INTERPOLATION. FOR OVERLAPPING 
C     PARTITIONINGS THE MAXIMAL VALUE IS TAKEN.
C
C     LOOPS OVER ALL SPECTRA ARE VECTORIZED.
C   
C     BEFORE THIS ROUTINE IS CALLED THE CROSS CORRELATION OF 
C     WAM FIRSRT GUESS AND INVERTED SAR PARTITIONINGS
C     HAS TO BE CARRIED OUT (CORRELTAW)!
C
C     
C     PARAMETERS FOR DIMENSIONS:
C     --------------------------
C
c      INTEGER DIMSPEC, DIMGAP, DIMPART, DIMANG, DIMFRE
C             IT MUST BE:
C             DIMSPEC >= MSPEC , DIMPART >= MPART ,
C             DIMANG >= NANG , DIMFRE >= NFRE
C
      include "dimpar.par"
C
C     AUTHOR:
C     -------
C
C     SUSANNE HASSELMANN, 1993 MPI FUER METEOROLOGIE HAMBURG
C     JUERGEN WASZKEWTIZ, 1993 MPI FUER METEOROLOGIE HAMBURG
C
C
C     INTERFACE:
C     ----------
C
      INTEGER MSPEC
C                     (INPUT) THE MAXIMAL NUMBER (=DIMENSION) 
C                      OF SPECTRA.
      INTEGER NSPEC
C                     (INPUT) THE ACTUAL NUMBER OF SPECTRA.
      INTEGER MPART
C                     (INPUT) THE MAXIMAL NUMBER (=DIMENSION)
C                     OF PARTITIONINGS.
      INTEGER NPARTW(MSPEC)
      INTEGER NPARTS(MSPEC)
C                     (INPUT) ARRAY OF THE ACTUAL NUMBERS OF 
C                     PARTITIONINGS OF THE ISPEC(TH) WAM FIRST GUESS
C                     SPECTRUM.
      INTEGER NANG
C                     (INPUT) THE ACTUAL NUMBER OF SPECTRAL
C                     DIRECTION AND THE DIMENSION.
      INTEGER NFRE
C                     THE ACTUAL NUMBER OF SPECTRAL FREQUENCY BINS
C                      AND THE DIMENSION.
      DOUBLE PRECISION  SPECW(0:MSPEC,NANG,NFRE)
      DOUBLE PRECISION  SPECS(0:MSPEC,NANG,NFRE)
C                     (INPUT,OUTPUT) AT INPUT: WAM FIRST GUESS 
C                     SPECTRA.
C                     AT OUTPUT: CORRECTED WAM SPECTRA
      INTEGER PARTW(MSPEC,NANG,NFRE)
      INTEGER PARTS(MSPEC,NANG,NFRE)
C                     (INPUT) PARTITIONINGS OF WAM FIRST GUESS (SAR)
C                     SPECTRA, WHERE PARTW(ISPEC,IANG,IFRE) IS 
C                     THE NUMBER OF THE PARTITION OF THE WAM 
C                     FIRST GUESS SPECTRUM (SAR) ISPEC
C                     AT DIRECTION IANG AND FREQUENCY IFRE
      INTEGER CORRELTAW(MSPEC,MPART)
C                     (INPUT) CROSS ASSIGNMENT OF WAM AND SAR 
C                     PARTITIONINGS, WHERE CORRELTAW(ISPEC,IPARTW) 
C                     MEANS THE PARTITIONING IPARTW
C                     OF THE WAM FIRST GUESS SPECTRUM ISPEC
C                     IS ASSIGNED TO PARTITIONING CORRELTAW(IPARTW)
C                     OF THE INVERTED SAR SPECTRUM
C                     (A ZERO MEANS, THAT THERE IS NO CROSS 
C                     ASSIGNMENT.
      INTEGER CORRELTAS(MSPEC,MPART)
C                     AS CORRELTAW BUT SAR - WAM
      DOUBLE PRECISION  MEANWE(MSPEC,MPART)
C                     (INPUT) MEAN ENERGIES OF PARTITIONINGS OF WAM 
C                     FIRST GUESS SPECTRA, WHERE MEANWE(ISPEC,IPART)
C                     IS THE ENERGY OF SPECTRUM ISPEC 
C                     PARTITIONING IPART
      DOUBLE PRECISION  MEANWANG(MSPEC,MPART)
C                     (INPUT) MEAN DIRECTIONS IN RADIANCE OF 
C                     PARTITIONINGS OF WAM FIRST GUESS SPECTRA.
      DOUBLE PRECISION  MEANWFRE(MSPEC,MPART)
C                     (INPUT) MEAN FREQUENCIES OF PARTITIONINGS
C                     OF WAM FIRST GUESS SPECTRA.
      DOUBLE PRECISION  MEANSE(MSPEC,MPART)
C                     (INPUT) MEAN ENERGIES OF PARTITIONINGS
C                     OF INVERTED SAR SPECTRA, 
      DOUBLE PRECISION  MEANSANG(MSPEC,MPART)
C                     (INPUT) MEAN DIRECTIONS IN RADIANCE OF 
C                     PARTITIONINGS OF INVERTED SAR SPECTRA.
      DOUBLE PRECISION  MEANSFRE(MSPEC,MPART)
C                     (INPUT) MEAN FREQUENCIES OF PARTITIONINGS
C                     OF INVERTED SAR SPECTRAS.
      DOUBLE PRECISION  MEANTE(MSPEC)
C                     (OUTPUT) ARRAY OF TOTAL MEAN ENERGIES OF 
C                     TRANSFORMED WAM FIRST GUESS SPECTRA
      DOUBLE PRECISION  MEANTANG(MSPEC)
C                     (OUTPUT) ARRAY OF MEAN DIRECTIONS IN RADIANCE C                     OF TRANSFORMED WAM FIRST GUESS SPECTRA
      DOUBLE PRECISION  MEANTFRE(MSPEC)
C                     (OUTPUT) MEAN FREQUENCIES OF TRANSFORMED
C                     WAM FIRST GUESS SPECTRA.
      DOUBLE PRECISION  FRE1
C                     (INPUT) LOWEST FREQUENCY.
      DOUBLE PRECISION  CO
C                     (INPUT) RATIO BETWEEN FREQUENCIES 
C                     (CO=FRE(2)/FRE(1))
      LOGICAL CONTROL
C                     (INPUT) CONTROLS  OUTPUT MESSAGES ON UNIT 6 ?
C                     .TRUE. = YES , .FALSE. = NO
C
C
C
C     EXTERNALS:
C     ----------
C
C     AVOIDPEAKS     - REDUCES SIZE OF FRAMES AROUND GAPS TO 
C                      AVOID PEAKS INSIDE A FRAME.
C     CHECKTUSTREPARA- CHECK PARAMETERS AND INPUT DIMENSIONS.
C     F04JGE         - FIND SOLUTION OF LINEAR LEAST SQUARES 
C                      PROBLEM (NAG)
C     FILLGAPS       - FILL GAPS BETWEEN PARTITIONINGS OF CORRECTED 
C                      SPECTRA WITH A 2D PARABOLIC INTERPOLATION.
C     GAPINTERPOL    - 2D PARABOLIC INTERPOLATION.
C     INITTUSTRE     - INITIALIZATION.
C     MAKEFRAMES     - BUILDS FRAMES AROUND GAPS BETWEEN WAVE 
C                      SYSTEMS.
C     TRANSFORM      - TRANSFORMS SPECTRAL PARTITIONINGS.
C     TRANSMEANS     - COMPUTES MEANS OF TRANSFORMED TOTAL SPECTRA
C
C     SUBROUTINE TREE:
C
C     TUSTRE
C       |
C       CHECKTUSTREPARA
C       |
C       INITTUSTRE
C       |
C       TRANSFORM
C       |
C       FILLGAPS
C       | |
C       | MAKEFRAMES
C       | |
C       | AVOIDPEAKS
C       | |
C       | GAPINTERPOL
C       |   |
C       |   F04JGE
C       |
C       MEANST
C      
C       
C     VARIABLES:
C     ----------
C
      DOUBLE PRECISION  COPO(DIMFRE),
     &     COPODIFF(DIMFRE)
C                       POWERS OF CO AND DIFFERENCES OF POWERS OF 
C                       CO, ONLY USED IN SUBROUTINE TRANSFORM.
      DOUBLE PRECISION  SPECT(DIMSPEC,DIMANG,DIMFRE)
C                       WORKING ARRAY FOR TRANSFORMATION OF 
C                       SPECTRA, ONLY USED IN SUBROUTINE TRANSFORM.
      DOUBLE PRECISION  ADJUST(DIMSPEC,DIMPART)
C                       ENERGY ADJUSTMENT PARAMETER.
      INTEGER INTROTATE(DIMSPEC,DIMPART)
C                       DIRECTIONAL GRIDPOINT ADJUSTMENT PARAMETER.
C                       (GRID POINTS), ONLY USED IN SUBROUTINE 
C                       TRANSFORM.
      DOUBLE PRECISION  FRACROTATE(DIMSPEC,DIMPART)
C                       DIRECTIONAL GRIDPOINT ADJUSTMENT PARAMETER.
C                       (FRACTIONAL PART), ONLY USED IN SUBROUTINE 
C                       TRANSFORM
      DOUBLE PRECISION  STRETCH(DIMSPEC,DIMPART)
C                       FREQUENCY ADJUSTMENT PARAMETER.
      INTEGER INTLOGSTRETCH(DIMSPEC,DIMPART)
C                       INTLOGSTRETCH = INT(LOG(STRETCH)/LOGCO), 
C                       ONLY USED IN SUBROUTINE TRANSFORM
      INTEGER PEAKANG(DIMSPEC,DIMPART), 
     &        PEAKFRE(DIMSPEC,DIMPART)
C                       DIRECTIONAL AND FREQUENCY INDEX OF PEAKS, 
C                       ONLY USED IN SUBROUTINE AVOIDPEAKS
      INTEGER NPEAK(DIMSPEC)
C                       THE NUMBER OF PEAKS, ONLY USED IN 
C                       SUBROUTINE AVOIDPEAKS
      DOUBLE PRECISION  FX(DIMANG,DIMFRE),
     &     FY(DIMANG,DIMFRE)
C                       TABLE OF FREQUENCY-DIRECTIONAL 
C                       POLAR COORDINATES.
C                       SET IN ROUTINE INITTUSTRE AND USED
C                       IN SUBROUTINE GAPINTERPOL AND TRANSMEANS
      DOUBLE PRECISION  FRETAB(DIMFRE)
C                       FREQUENCIES, IS SET IN SUBROUTINE 
C                       INITTUSTRE AND USED IN MEANST AND FILLGAPS
      DOUBLE PRECISION  COSTAB(DIMANG),
     &     SINTAB(DIMANG)
C                       COSINE AND SINE, SET IN SUBROUTINE 
C                       INITTUSTRE AND USED ONLY IN SUBROUTINE 
C                       MEANST.
      DOUBLE PRECISION  DFIM(DIMFRE)
C                       FREQUENCY INCREMENT / DIRECTIONAL INCREMENT.
C                       INITIALIZED IN SUBROUTINE INITTUSTRE AND 
C                       USED ONLY IN SUBROUTINE MEANST.
      DOUBLE PRECISION  SUM0(DIMSPEC), SUMX0(DIMSPEC), SUMY0(DIMSPEC)
C                       TEMPORARILY STORAGE, ONLY USED IN 
C                       SUBROUTINE TRANSMEANS.
      INTEGER LANG(DIMSPEC,DIMGAP), HANG(DIMSPEC,DIMGAP),
     &        LFRE(DIMSPEC,DIMGAP), HFRE(DIMSPEC,DIMGAP)
C                       LOWER LEFT AND UPPER RIGHT CORNERS OF THE 
C                       FRAME AROUND A GAP BETWEEN 2 PARTITIONINGS.
C                       ONLY USED IN SUBROUTINE MAKEFRAMES.
      INTEGER GAP(DIMSPEC,DIMANG,DIMFRE)
C                       THE GAP NUMBER ASSIGNED TO A DIRECTIONAL-
C                       FREQUENCY BIN. ONLY USED IN SUBROUTINE 
C                       MAKEFRAMES
      INTEGER NGAP(DIMSPEC)
C                       THE NUMBER OF GAPS
      LOGICAL EQUIGAP(DIMSPEC,DIMGAP,DIMGAP)
C                       EQUIVALENCE OF GAPS, WHERE 
C                       EQUIGAP(ISPEC,IGAP,GAP) = .TRUE. MEANS, 
C                       THAT IN SPECTRUM NUMBER ISPEC THE GAP 
C                       NUMBERS IGAP AND JGAP ARE EQUIVALENT, 
C                       ONLY USED IN SUBROUTINE MAKEFRAMES
C
      integer ispec,iparts,iang,ifre
C
C-------------------------------------------------------------------
C
      IF( CONTROL ) WRITE(6,*) 'CALL OF SUBROUTINE TUSTRE'
C
C    1. INPUT PARAMETERS FOR DIMENSIONS ARE COMPARED WITH PARAMETER 
C       DIMENSION.
C    ---------------------------------------------------------------
C
      CALL CHECKTUSTREPARA( DIMSPEC , MSPEC , DIMPART , MPART ,
     &                      DIMANG , NANG , DIMFRE , NFRE )
C
C-------------------------------------------------------------------
C
C
C     2. INITIALIZATION OF GENERAL PARAMETERS AND ARRAYS.
C     ----------------------------------------------------

      CALL INITTUSTRE( 
C                  DIMENSIONS
     &                 DIMANG , NANG , DIMFRE , NFRE ,
C                  OUTPUT
     &                 FRE1 , CO , FRETAB , COSTAB , SINTAB , 
     &                 DFIM , FX , FY )
C
C-------------------------------------------------------------------
C
C     3. CORRECT PARTITIONINGS OF MODEL FIRST GUESS SPECTRA 
C        ACCORDING TO MEAN VALUES OF PARTITIONINGS OF SAR 
C        INVERTED SPECTRA.
C     ------------------------------------------------------
c
       CALL TRANSFORM( 
C                    DIMENSIONS
     &                 DIMSPEC , MSPEC , NSPEC , DIMPART , MPART , 
     &                 NPARTW , DIMANG , NANG , DIMFRE , NFRE ,
C                    INPUT/OUTPUT
     &                 SPECW , 
C                    WORK SPACE
     &                 SPECT , 
C                    INPUT
     &                 PARTW ,CORRELTAW ,MEANWE,MEANWANG,MEANWFRE, 
     &                 MEANSE , MEANSANG , MEANSFRE ,
     &                 FRE1 , CO,
C                    OUTPUT
     &                 ADJUST , INTROTATE , FRACROTATE , 
     &                 STRETCH , INTLOGSTRETCH ,
     &                 COPO , COPODIFF  )
c      superimpose extra wave systems from SAR retrieval over 
c      first guess spectrum.
c
       do ispec=1,nspec
        do iparts=1,nparts(ispec)
         if(correltas(ispec,iparts).lt.0) then
          do iang=1,nang
           do ifre=1,12
            if(parts(ispec,iang,ifre).eq.iparts) then
             specw(ispec,iang,ifre)=specs(ispec,iang,ifre)
            end if
           end do
          end do
         end if
        end do
       end do
C
C-------------------------------------------------------------------
C
C     4. INTERPOLATE GAPS BETWEEN SUPERIMPOSED PARTITIONINGS BY 
C        2D PARABOLIC INTERPOLATION.
C     ---------------------------------------------------------

      CALL FILLGAPS( 
C                  DIMENSIONS
     &                  DIMSPEC , MSPEC , NSPEC , DIMGAP , NGAP ,
     &                  DIMPART , DIMANG , NANG , DIMFRE , NFRE , 
C                  INPUT (SPECW ALSO OUTPUT)
     &                  SPECW , 
C                  COMPUTED INTERNALLY
     &                  GAP ,
     &                  NPEAK , PEAKANG , PEAKFRE ,
     &                  LANG, HANG , LFRE , HFRE ,
C                  INPUT FROM INITIALIZATION ROUTINE.
     &                  FX , FY , FRETAB , EQUIGAP , CONTROL )
C
C-------------------------------------------------------------------
C
C     5. COMPUTE MEAN PARAMETERS OF TOTAL CORRECTED SPECTRA.
C     ------------------------------------------------------
C

      CALL TRANSMEANS(
C                  DIMENSIONS
     &                   DIMSPEC , MSPEC , NSPEC ,
     &                   DIMANG , NANG , DIMFRE , NFRE ,
C                  INPUT 
     &                   SPECW ,
C                  OUTPUT
     &                   MEANTE , MEANTANG , MEANTFRE ,
C                  WORK ARRAYS
     &                   SUM0 , SUMX0 , SUMY0 ,
C                  INPUT FROM INITIALIZATION ROUTINE
     &                   FRE1,CO ,FRETAB ,COSTAB ,SINTAB,DFIM )
C
      IF( CONTROL ) WRITE(6,*) 'END OF SUBROUTINE TUSTRE'

      RETURN

      END


C-------------------------------------------------------------------
C
      SUBROUTINE AVOIDPEAKS( 
C                   DIMENSIONS
     &                 DIMSPEC ,MSPEC ,NSPEC, DIMGAP ,NGAP,
     &                 DIMPART , DIMANG ,NANG ,DIMFRE,NFRE,
C                   INPUT 
     &                 SPEC ,
     &                 NPEAK , PEAKANG , PEAKFRE ,
C                   ARRAYS TO BE ADJUSTED
     &                 LANG, HANG , LFRE , HFRE )
C
C-------------------------------------------------------------------
C
      IMPLICIT NONE
C
C
C     PURPOSE:
C     --------
C
C     THE FRAMES AROUND THE GAPS ARE REDUCED TO AVOID PEAKS 
C     OTHERWISE THE PARABOLA FIT CANNOT BE COMPUTED.
C
C
C     METHOD:
C     -------
C
C     IF A PEAK LIES INSIDE A FRAME, THE FRAME IS SPLIT INTO TWO
C     FRAMES TO AVOID PEAKS.
C
C     AUTHOR.
C     -------
C
C     S.HASSELMANN MPI HAMNBURG. 1993
C
C     INTERFACE:
C     ----------
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMGAP, NGAP(DIMSPEC),
     &        DIMPART, DIMANG, NANG, DIMFRE, NFRE
C                 DIMENSIONS.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
C                 2D SPECTRUM.
      INTEGER LANG(DIMSPEC,DIMGAP), 
     &        HANG(DIMSPEC,DIMGAP),
     &        LFRE(DIMSPEC,DIMGAP),
     &        HFRE(DIMSPEC,DIMGAP)
C                 THE LEFT LOWER AND RIGHT UPPER CORNER OF THE FRAME
C                 IN ANG AND FRE, WILL BE ADJUSTED.
      INTEGER NPEAK(DIMSPEC)
C                 NUMBER OF PEAKS
      INTEGER PEAKANG(DIMSPEC,DIMPART),
     &        PEAKFRE(DIMSPEC,DIMPART)
C                 THE DIRECTIONAL AND FREQUENCY INDICES OF THE PEAK
C 
C     VARIABLES:
C     ----------
C
      INTEGER ISPEC, IGAP, IANG, IFRE
C                  LOOP INDICES.
      INTEGER IANGP1, IANGM1, IFREP1, IFREM1
C                  LOOP INDICES + OR - 1
      DOUBLE PRECISION  SPEC0
C                  TEMPORARY STORAGE
      LOGICAL ERROR, READY
C
C-------------------------------------------------------------------
C
C     IF PEAK FOUND IN FRAME BOUNDARY MOVED TO PEAK.
C     ----------------------------------------------
C
      DO ISPEC=1,NSPEC
       DO IGAP=1,NGAP(ISPEC)
        DO IANG=LANG(ISPEC,IGAP),HANG(ISPEC,IGAP)
         DO IFRE=LFRE(ISPEC,IGAP),HFRE(ISPEC,IGAP)
          IANGP1 = IANG + 1
          IF( IANGP1.GT.NANG ) IANGP1 = 1
          IANGM1 = IANG - 1
          IF( IANGM1.EQ.0 ) IANGM1 = NANG
          IFREP1 = IFRE + 1
          IF( IFREP1.GT.NFRE ) IFREP1 = NFRE
          IFREM1 = IFRE - 1
          IF( IFREM1.EQ.0 ) IFREM1 = 1
           SPEC0 = SPEC(ISPEC,IANG,IFRE)
           IF( SPEC0.GT.0..AND.
     &          SPEC0.GE.SPEC(ISPEC,IANG  ,IFREM1).AND.
     &          SPEC0.GE.SPEC(ISPEC,IANG  ,IFREP1).AND.
     &          SPEC0.GE.SPEC(ISPEC,IANGP1,IFRE  ).AND.
     &          SPEC0.GE.SPEC(ISPEC,IANGM1,IFRE  ) )THEN
            IF((IANG-LANG(ISPEC,IGAP)).LT.
     &          (HANG(ISPEC,IGAP)-IANG)) THEN
              LANG(ISPEC,IGAP) =IANG
            ELSE
              HANG(ISPEC,IGAP) =IANG
            END IF
           END IF
         END DO
        END DO
       END DO
      END DO
      RETURN
      END
C
C-------------------------------------------------------------------
C
      SUBROUTINE CHECKTUSTREPARA( 
C               INPUT
     &                DIMSPEC , MSPEC , DIMPART , MPART ,
     &                DIMANG , NANG , DIMFRE , NFRE )
C
C-------------------------------------------------------------------
C
      IMPLICIT NONE
C
C     PURPOSE:
C     --------
C
C     CROSS CHECKS  PARAMETERS FOR DIMENSIONS.
C
C
C     INTERFACE:
C     ----------
C
      INTEGER DIMSPEC, MSPEC, DIMPART, MPART,
     &        DIMANG, NANG, DIMFRE, NFRE
C
C
C
C     VARIABLES:
C     ----------
C
      LOGICAL ERROR
C
C-------------------------------------------------------------------
C


      ERROR = .FALSE.
      IF( DIMSPEC.NE.MSPEC )THEN
        ERROR = .TRUE.
        WRITE(6,*) 'ERROR! SUBROUTINE TUSTRE:'
        WRITE(6,*) 'PARAMETER DIMSPEC IS TOO SMALL!'
        WRITE(6,*) 'IT MUST BE DIMSPEC >= MSPEC = ',MSPEC,'!'
        WRITE(6,*) 'CHANGE PARAMETER DIMSPEC!'
      ENDIF
      IF( DIMPART.NE.MPART )THEN
        ERROR = .TRUE.
        WRITE(6,*) 'ERROR! SUBROUTINE TUSTRE:'
        WRITE(6,*) 'PARAMETER DIMPART IS TOO SMALL!'
        WRITE(6,*) 'IT MUST BE DIMPART >= MPART = ',MPART,'!'
        WRITE(6,*) 'CHANGE PARAMETER DIMPART!'
      ENDIF
      IF( DIMANG.NE.NANG )THEN
        ERROR = .TRUE.
        WRITE(6,*) 'ERROR! SUBROUTINE TUSTRE:'
        WRITE(6,*) 'PARAMETER DIMANG IS TOO SMALL!'
        WRITE(6,*) 'IT MUST BE DIMANG >= NANG = ',NANG,'!'
        WRITE(6,*) 'CHANGE PARAMETER DIMANG!'
      ENDIF
      IF( DIMFRE.NE.NFRE )THEN
        ERROR = .TRUE.
        WRITE(6,*) 'ERROR! SUBROUTINE TUSTRE:'
        WRITE(6,*) 'PARAMETER DIMFRE IS TOO SMALL!'
        WRITE(6,*) 'IT MUST BE DIMFRE >= NFRE = ',NFRE,'!'
        WRITE(6,*) 'CHANGE PARAMETER DIMFRE!'
      ENDIF
      IF( ERROR )THEN
        STOP 'ERROR IN SUBROUTINE TUSTRE!'
      ENDIF

      RETURN

      END
C
C-------------------------------------------------------------------
C
      SUBROUTINE FILLGAPS( 
C                  DIMENSIONS
     &                DIMSPEC , MSPEC , NSPEC , DIMGAP , NGAP ,
     &                DIMPART , DIMANG , NANG , DIMFRE , NFRE , 
C                  INPUT (FOR SPEC ALSO OUTPUT)
     &                SPEC , GAP ,
     &                NPEAK , PEAKANG , PEAKFRE ,
     &                LANG, HANG , LFRE , HFRE ,
     &                FX , FY , FRETAB , EQUIGAP , CONTROL )
C
C-------------------------------------------------------------------
C
      IMPLICIT NONE
C
C
C     PURPOSE:
C     --------
C
C     FILL GAPS (=HOLES) IN THE TRANSFORMED SPECTRA 
C     (BUT SOME ZEROS COULD SURVIVE THIS ROUTINE)
C
C
C     METHOD:
C     -------
C
C     ROUTINE BUILDS FRAMES AROUND GAPS,
C     FRAMES ARE REDUCED TO AVOID PEAKS, 
C     AND THEN AN INTERPOLATION IS MADE FOR FILLING THE GAPS.
C
C
C     EXTERNALS:
C     ----------
C
C     MAKEFRAMES  - MAKES THE FRAME.
C     AVOIDPEAKS  - REDUCES SIZE OF FRAMES TO AVOID PEAKS.
C     GAPINTERPOL - INTERPOLATES TO FILL THE GAPS.
C
C     AUTHOR.
C     -------
C     S.HASSELMANN, MPI HAMBURG, 1993.
C     J.WASZKEWITZ, MPI HAMBURG, 1993.
C
C     INTERFACE:
C     ----------
C
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMGAP, NGAP(DIMSPEC),
     &        DIMPART, DIMANG,NANG,  DIMFRE, NFRE
C               ARRAY DIMENSIONS.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
C               2D SPECTRA.
      INTEGER GAP(DIMSPEC,DIMANG,DIMFRE)
C               GAP INDEX.
      INTEGER NPEAK(DIMSPEC)
C               NUMBER PF PARTITIONINGS IN A SPECTRUM.
      INTEGER PEAKANG(DIMSPEC,DIMPART), 
     &        PEAKFRE(DIMSPEC,DIMPART)
C               FREQ-DIRECT. INDEX OF PEAKS
      INTEGER LANG(DIMSPEC,DIMGAP), 
     &        HANG(DIMSPEC,DIMGAP),
     &        LFRE(DIMSPEC,DIMGAP),
     &        HFRE(DIMSPEC,DIMGAP)
C               LOWER LEFT AND UPPER RIGHT CORNER OF GAP.
      DOUBLE PRECISION  FX(DIMANG,DIMFRE), 
     &     FY(DIMANG,DIMFRE), 
     &     FRETAB(DIMFRE)
C                POLAR COORDINATES AND FREQYEBCIES.
      LOGICAL EQUIGAP(DIMSPEC,DIMGAP,DIMGAP)
C                EQUIVALENCE OF GAPS, WHERE 
C                EQUIGAP(ISPEC,IGAP,GAP) = .TRUE. MEANS, 
C                THAT IN SPECTRUM NUMBER ISPEC THE GAP 
C                NUMBERS IGAP AND JGAP ARE EQUIVALENT, 
C                ONLY USED IN SUBROUTINE MAKEFRAMES
C                
      LOGICAL CONTROL
C
C
C     VARIABLES:
C     ----------
C
      INTEGER ISPEC, IGAP
C                LOOP INDICES
C
C-------------------------------------------------------------------
C      
C
C     1.1 BUILD FRAMES AROUND GAPS.
C     ----------------------------
C
      CALL MAKEFRAMES( 
C          DIMENSIONS
     &             DIMSPEC , MSPEC , NSPEC , DIMGAP , NGAP ,
     &             DIMANG , NANG , DIMFRE , NFRE , 
C          INPUT
     &             SPEC , GAP ,
C          OUTPUT
     &             LANG, HANG , LFRE , HFRE , EQUIGAP )

      IF( CONTROL )THEN
        DO ISPEC = 1,NSPEC
          WRITE(6,*) 'SPECTRA NUMBER ',ISPEC,':'
          WRITE(6,*) NGAP(ISPEC),' GAPS before avoidpeaks '
          IF( NGAP(ISPEC).GT.0 ) WRITE(6,*) 'CORNERS OF FRAMES:'
          DO IGAP = 1,NGAP(ISPEC)
            WRITE(6,'(''  FREQUENCIES = '',E8.2,'' , '',E8.2,
     &                ''  ANGLES 
     &= '',I3,'' , '',I3)')
     &          FRETAB(LFRE(ISPEC,IGAP)),FRETAB(HFRE(ISPEC,IGAP)),
     &          NINT((LANG(ISPEC,IGAP)-1.)/NANG*360.),
     &          NINT((HANG(ISPEC,IGAP)-1.)/NANG*360.)
          END DO
        END DO
      END IF
C
C     1.2 REDUCE SIZE OF FRAMES IF PEAKS ARE CONTAINED.
C     -------------------------------------------------
C
      CALL AVOIDPEAKS( 
C          DIMENSIONS
     &             DIMSPEC , MSPEC , NSPEC , DIMGAP , NGAP , 
     &             DIMPART , DIMANG , NANG , DIMFRE , NFRE , 
C          INPUT
     &             SPEC ,
     &             NPEAK , PEAKANG , PEAKFRE ,
C          ARRAYS TO BE ADJUSTED
     &             LANG, HANG , LFRE , HFRE )

      IF( CONTROL )THEN
        DO ISPEC = 1,NSPEC
          WRITE(6,*) 'SPECTRA NUMBER ',ISPEC,':'
          WRITE(6,*) NGAP(ISPEC),' GAPS'
          IF( NGAP(ISPEC).GT.0 ) WRITE(6,*) 'CORNERS OF FRAMES:'
          DO IGAP = 1,NGAP(ISPEC)
            WRITE(6,'(''  FREQUENCIES = '',E8.2,'' , '',E8.2,
     &                ''  ANGLES 
     &= '',I3,'' , '',I3)')
     &          FRETAB(LFRE(ISPEC,IGAP)),FRETAB(HFRE(ISPEC,IGAP)),
     &          NINT((LANG(ISPEC,IGAP)-1.)/NANG*360.),
     &          NINT((HANG(ISPEC,IGAP)-1.)/NANG*360.)
          END DO
        END DO
      END IF
C
C-------------------------------------------------------------------
C
C     2. INTERPOLATE FRAMES WITH 2D PARABOLA FIT.
C     -------------------------------------------
C

      CALL GAPINTERPOL( 
C          DIMENSIONS
     &             DIMSPEC , MSPEC , NSPEC , DIMGAP , NGAP ,
     &             DIMANG , NANG , DIMFRE , NFRE , 
C          INPUT ( SPEC ALSO OUTPUT)
     &             SPEC ,
     &             FX , FY , LANG, HANG , LFRE , HFRE )

      RETURN
      END

C
C-------------------------------------------------------------------
C
      SUBROUTINE GAPINTERPOL( 
C              DIMENSIONS
     &             DIMSPEC , MSPEC , NSPEC , DIMGAP , NGAP ,
     &             DIMANG , NANG , DIMFRE , NFRE , 
C              INPUT ( SPEC ALSO OUTPUT)
     &             SPEC ,
     &             FX , FY , LANG, HANG , LFRE , HFRE )
C
C-------------------------------------------------------------------
C
      IMPLICIT NONE
C
C
C     PURPOSE:
C     --------
C
C     INTERPOLATE GAPS.
C
C
C      AUTHOR.
C      -------
C      S.HASSELMANN, MPI HAMBURG, 1993.
C      J. WASZKEWITZ,MPI HAMBURG, 1993.
C
C     INTERFACE:
C     ----------
C
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMGAP, NGAP(DIMSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
C                 DIMENSIONS.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
C                 2D SPECTRUM.
      DOUBLE PRECISION  FX(DIMANG,DIMFRE), 
     &     FY(DIMANG,DIMFRE)
C                 POLAR COORDINATES.
      INTEGER LANG(DIMSPEC,DIMGAP), 
     &        HANG(DIMSPEC,DIMGAP),
     &        LFRE(DIMSPEC,DIMGAP),
     &        HFRE(DIMSPEC,DIMGAP)
C                 LOWER LEFT AND UPPER RIGHT CORNER OF GAP.
C
C     METHOD.
C     -------
C     COMPUTE THE 6 COEFFICIENTS OF A 2D PARABOLA FIT BY MINIMIZING 
C     A COST FUNCTION OVER ALL SOLUTIONS GAINED AT SPECTRAL POINTS 
C     WITH VALUES > 0.
C     DERIVATIVES OF THE COST FUNCTION WITH RESPECT TO THE PARABOLA 
C     COEFFICIENTS DELIVER A SET OF 6 EQUATIONS WITH 6 UNKNOWNS 
C     WHICH ARE SOLVED WITH NAG ROUTINE F04JGE.
C 
C     VARIABLES:
C     ----------
C
      INTEGER ISPEC, IGAP, IANG, IFRE, I12, I, J
C                 LOOP INDICES.
      INTEGER LANG0(2),HANG0(2),LFRE0,HFRE0
C                 CORNERS OF FRAMES FOR TEMPORARILY USE
      DOUBLE PRECISION  X, Y
C                 FREQUENCY VALUES IN CARTHESIAN COORDINATES
      DOUBLE PRECISION  A(6,6), B(6), T(6), WORK(24), w(6), v(6,6)
      LOGICAL DUMMY1
      DOUBLE PRECISION  DUMMY2
      INTEGER DUMMY3
      INTEGER FAIL
C                 CONTAINS AN ERROR FLSG AFTER CALLING THE NAG 
C                 ROUTINE F04JGE
      REAL ARe(6,6),BRe(6),wRe(6),vRe(6,6)
C
C-------------------------------------------------------------------
C
C
C     1.1 CHECK POSITION OF CORNERS WITH RESPECT TO 0 DEGREE.
C     ------------------------------------------------------
C
C     LOOP OVER SPECTRA.
      DO ISPEC = 1,NSPEC
        DO IGAP = 1,NGAP(ISPEC)
C     LOOP OVER GAPS.
          IF( LANG(ISPEC,IGAP).EQ.1.AND.HANG(ISPEC,IGAP).EQ.NANG.OR.
     &        LANG(ISPEC,IGAP)-HANG(ISPEC,IGAP).EQ.2.OR.
     &        LANG(ISPEC,IGAP)-HANG(ISPEC,IGAP)+NANG.EQ.2 )THEN
            LANG0(1) = 1
            HANG0(1) = NANG
            LANG0(2) = 1
            HANG0(2) = 0
          ELSE
            IF( LANG(ISPEC,IGAP).GT.HANG(ISPEC,IGAP) )THEN
              LANG0(1) = 1
              HANG0(1) = HANG(ISPEC,IGAP) + 1
              LANG0(2) = LANG(ISPEC,IGAP) - 1
              HANG0(2) = NANG
            ELSE
              LANG0(1) = MAX( LANG(ISPEC,IGAP)-1 , 1 )
              HANG0(1) = MIN( HANG(ISPEC,IGAP)+1 , NANG )
              IF( LANG(ISPEC,IGAP).EQ.1 )THEN
                LANG0(2) = NANG
                HANG0(2) = NANG
              ELSE IF( HANG(ISPEC,IGAP).EQ.NANG )THEN
                LANG0(2) = 1
                HANG0(2) = 1
              ELSE
                LANG0(2) = 1
                HANG0(2) = 0
              END IF
            END IF
          END IF
          LFRE0 = MAX(1,LFRE(ISPEC,IGAP)-1)
          HFRE0 = MIN(NFRE,HFRE(ISPEC,IGAP)+1)
C
C     1.2 COMPUTE COEFFICIENT MATRIX FOR LINEAR SYSTEM OF 6 
C         EQUATIONS.
C     ---------------------------------------------------------
C
          DO I = 1,6
            DO J = 1,6
              A(I,J) = 0.
            END DO
            B(I) = 0.
          END DO
          DO I12 = 1,2
            DO IANG = LANG0(I12),HANG0(I12)
              DO IFRE = LFRE0,HFRE0
                IF( SPEC(ISPEC,IANG,IFRE).NE.0. )THEN
                  X = FX( IANG , IFRE )
                  Y = FY( IANG , IFRE )
                  T(1) = 1.
                  T(2) = X
                  T(3) = Y
                  T(4) = X*X
                  T(5) = Y*Y
                  T(6) = X*Y
                  DO I = 1,6
                    DO J= 1,6
                      A(I,J) = A(I,J) + T(I) * T(J)
                    END DO
                    B(I) = B(I) + T(I) * SPEC(ISPEC,IANG,IFRE)
                  END DO
                END IF
              END DO
            END DO
          END DO
          FAIL = 0
C
C      1.3 SOLVE SYSTEM OF EQUATIONS WITH RESPECT TO COEFFICIENTS 
C          FOR 2D PARABOLA FIT.
C      ------------------------------------------------------------
          ARe = REAL(A)
          BRe = REAL(B)
          wRe = REAL(w)
          vRe = REAL(v)
          CALL leastsquare(ARe,BRe,BRe,6,6,wRe,vRe)
          A = DBLE(ARe)
          B = DBLE(BRe)
          w = DBLE(wRe)
          v = DBLE(vRe)
C
c          CALL F04JGE(6,6,A,6,B,5.E-4,DUMMY1,DUMMY2,DUMMY3,WORK,24,
c     &                FAIL)
C         SEE NAG LIBARY DOCUMENTATION ROUTINE F04JGF (!)
          IF( FAIL.EQ.1 )THEN
            WRITE(6,*) 'ERROR! SUBROUTINE TUSTRE:'
            WRITE(6,*) 'SOMEBODY MADE A MISTAKE WHILE CHANGING'
            WRITE(6,*) 'THIS ROUTINE.'
            WRITE(6,*) 'SEE NAG LIBARY DOCUMENTATION ROUTINE F04JGF'
            WRITE(6,*) 'TO FIND AND CORRECT THIS MISTAKE! SORRFY!'
            STOP 'ERROR  IN SUBROUTINE TUSTRE!'
          END IF
          IF( FAIL.EQ.0 )THEN
            B(1) = MAX(B(1),0.D0)
            DO I12 = 1,2
              DO IANG = LANG0(I12),HANG0(I12)
                DO IFRE = LFRE0,HFRE0
                  IF( SPEC(ISPEC,IANG,IFRE).EQ.0.1e-19 )THEN
                    X = FX( IANG , IFRE )
                    Y = FY( IANG , IFRE )
                    SPEC(ISPEC,IANG,IFRE) = MAX( 0.D0 ,
     &                B(1)+B(2)*X+B(3)*Y+B(4)*X*X+B(5)*Y*Y+B(6)*X*Y)
                  END IF
                END DO
              END DO
            END DO
          END IF
C
C       END OF LOOPS OVER NUMBER OF GAPS.
C
        END DO
C    
C     END OF LOOP OVER NUMBER OF SPECTRA.
C
      END DO

      RETURN
      END

C
C-------------------------------------------------------------------
C
      SUBROUTINE MAKEFRAMES( 
C                  DIMENSIONS
     &               DIMSPEC , MSPEC ,NSPEC ,DIMGAP ,NGAP ,
     &               DIMANG , NANG , DIMFRE , NFRE , 
C                  INPUT
     &               SPEC , GAP ,
C                  OUTPUT
     &               LANG, HANG , LFRE , HFRE , EQUIGAP )
C
C-------------------------------------------------------------------
C
      IMPLICIT NONE
C
C     PURPOSE:
C     --------
C
C     BUILDS FRAMES AROUND GAPS
C
C     AUTHOR.
C     -------
C     S.HASSELMANN, MPI HAMBURG, 1993.
C     J.WASZKEWITZ, MPI HAMBURG, 1993.
C
C     INTERFACE:
C     ----------
C
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMGAP, NGAP(DIMSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
C                  ARRAY DIMENSIONS.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
C                   2D SPECTRUM.
      INTEGER GAP(DIMSPEC,DIMANG,DIMFRE)
C                   ASSIGNMENT OF A GAP NUMBER TO A 
C                   FREQUENCY-DIRECTIONAL BIN.
      INTEGER LANG(DIMSPEC,DIMGAP), 
     &        HANG(DIMSPEC,DIMGAP),
     &        LFRE(DIMSPEC,DIMGAP),
     &        HFRE(DIMSPEC,DIMGAP)
C                   LOWER LEFT AND UPPER RIGHT CORNER OF A GAP.
      LOGICAL EQUIGAP(DIMSPEC,DIMGAP,DIMGAP)
C                   FLAG INDICATING WHETHER GAPS ARE CONTAINED IN 
C                   ONE ANOTHER OR OVERLAPPING.
C
C
C     VARIABLES:
C     ----------
C
      INTEGER ISPEC, IGAP, JGAP, KGAP, IANG, IFRE
C                    LOOP INDICES.
      INTEGER IANGP1, IANGM1, IFREM1
C                    "IANG PLUS 1" , "IANG MINUS 1" , "IFRE PLUS 1".
      INTEGER LANG0, HANG0, LFRE0, HFRE0
C                    FOR TEMPORARILY STORAGE.
      INTEGER MAXNGAP
C                    THE MAXIMAL NUMBER OF GAPS OCCURING IN ONE 
C                    SPECTRUM.
      INTEGER GAP0
C                    TEMPORARILY USE.
      LOGICAL NEWGAP, ERROR
      LOGICAL WRAPI, WRAPJ
C                    FLAG INDICATING IF GAPI RESP. GAPJ WRAPP 
C                    AROUND 0 DEGREE ?
C
C
C-------------------------------------------------------------------
C
C
C     1. INITIALIZATION OF ARRAYS:
C     -------------------------
C
      DO IANG = 1,NANG
        DO IFRE = 1,NFRE
          DO ISPEC = 1,NSPEC
            GAP(ISPEC,IANG,IFRE) = 0
          END DO
        END DO
      END DO
      DO ISPEC = 1,NSPEC
        NGAP(ISPEC) = 0
      END DO
      DO IGAP = 1,DIMGAP
        DO JGAP = 1,DIMGAP
          DO ISPEC = 1,NSPEC
            EQUIGAP(ISPEC,IGAP,JGAP) = .FALSE.
          END DO
        END DO
      END DO
      ERROR = .FALSE.
C
C------------------------------------------------------------------
C
C     2. FIND CORNERS OF FRAMES:
C     ---------------------------
C
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
C
C         "CDIR$ IVDEP" IS A COMPILER DIRECTIVE TO FORCE CFT77
C         TO VECTORIZE THE NEXT LOOP
          DO ISPEC = 1,NSPEC
            IF( SPEC(ISPEC,IANG,IFRE).EQ.0.1E-19 )THEN
              NEWGAP = .TRUE.
              IF( IFRE.GT.1 )THEN
                IFREM1 = IFRE - 1
                IF( GAP(ISPEC,IANG,IFREM1).NE.0 )THEN
                  NEWGAP = .FALSE.
                  GAP0 = GAP(ISPEC,IANG,IFREM1)
                  GAP(ISPEC,IANG,IFRE) = GAP0
                  IF( HFRE(ISPEC,GAP0).EQ.IFREM1 )
     &                HFRE(ISPEC,GAP0) = IFRE
                END IF
              END IF
              IF( GAP(ISPEC,IANGM1,IFRE).NE.0 )THEN
                NEWGAP = .FALSE.
                IF( GAP(ISPEC,IANG,IFRE).EQ.0 )THEN
                  GAP0 = GAP(ISPEC,IANGM1,IFRE)
                  GAP(ISPEC,IANG,IFRE) = GAP0
                  IF( HANG(ISPEC,GAP0).EQ.IANGM1
     &                .AND.LANG(ISPEC,GAP0).NE.IANG )
     &                HANG(ISPEC,GAP0) = IANG
                ELSE
                  EQUIGAP(ISPEC,
     &                GAP(ISPEC,IANGM1,IFRE),GAP(ISPEC,IANG,IFRE))
     &                = .TRUE.
                END IF
              END IF
              IF( GAP(ISPEC,IANGP1,IFRE).NE.0 )THEN
                NEWGAP = .FALSE.
                IF( GAP(ISPEC,IANG,IFRE).EQ.0 )THEN
                  GAP0 = GAP(ISPEC,IANGP1,IFRE)
                  GAP(ISPEC,IANG,IFRE) = GAP0
                  IF( LANG(ISPEC,GAP0).EQ.IANGP1
     &                .AND.HANG(ISPEC,GAP0).NE.IANG )
     &                LANG(ISPEC,GAP0) = IANG
                ELSE
                  EQUIGAP(ISPEC,
     &                GAP(ISPEC,IANGP1,IFRE),GAP(ISPEC,IANG,IFRE))
     &                = .TRUE.
                END IF
              END IF
              IF( NEWGAP )THEN
                NGAP(ISPEC) = NGAP(ISPEC) + 1
                IF( NGAP(ISPEC).GT.DIMGAP ) ERROR = .TRUE.
                GAP0 = MIN(DIMGAP,NGAP(ISPEC))
                GAP(ISPEC,IANG,IFRE) = GAP0
                LANG(ISPEC,GAP0) = IANG
                HANG(ISPEC,GAP0) = IANG
                LFRE(ISPEC,GAP0) = IFRE
                HFRE(ISPEC,GAP0) = IFRE
              END IF
            END IF
          END DO
        END DO
      END DO

      MAXNGAP = 0
      DO ISPEC = 1,NSPEC
        MAXNGAP = MAX(MAXNGAP,NGAP(ISPEC))
      END DO

      IF( ERROR )THEN
        WRITE(6,*) 'ERROR!  SUBRUTINE TUSTRE:'
        WRITE(6,*) 'PARAMETER DIMGAP IS TOO SMALL!'
        WRITE(6,*) 'IT MUST BE DIMGAP >= ',MAXNGAP,'!'
        WRITE(6,*) 'CHANGE PARAMETER DIMGAP!'
        STOP 'ERROR IN SUBROUTINE TUSTRE!'
      END IF
C
C------------------------------------------------------------------
C
C
C     2.1 COMBINE FRAMES THAT OVERLAP OR ARE CONTAINED IN ONE 
C         ANOTHER.
C     --------------------------------------------------------------
C
      DO IGAP = 1,MAXNGAP
        DO JGAP = 1,MAXNGAP

C
C         "CDIR$ IVDEP" IS A COMPILER DIRECTIVE TO FORCE CFT77
C         TO VECTORIZE THE NEXT LOOP
          DO ISPEC = 1,NSPEC
            IF( EQUIGAP(ISPEC,IGAP,JGAP).AND.IGAP.NE.JGAP )THEN
              IF( HANG(ISPEC,IGAP)+1.EQ.LANG(ISPEC,IGAP) )THEN
                LANG(ISPEC,IGAP) = 1
                HANG(ISPEC,IGAP) = NANG
              END IF
              IF( HANG(ISPEC,JGAP)+1.EQ.LANG(ISPEC,JGAP) )THEN
                LANG(ISPEC,JGAP) = 1
                HANG(ISPEC,JGAP) = NANG
              END IF
              WRAPI = LANG(ISPEC,IGAP).GT.HANG(ISPEC,IGAP)
              WRAPJ = LANG(ISPEC,JGAP).GT.HANG(ISPEC,JGAP)
              IF( .NOT.WRAPI.AND..NOT.WRAPJ )THEN
C               CASES:
C               |III     |  |IIIII   |  | IIII   |  |  IIII  |
C               |     JJJ|  |   JJJJJ|  |   JJJJ |  | JJJJJJ |
C
C               | IIIIII |  |   IIII |  |   IIIII|  |     III|
C               |  JJJJ  |  | JJJJ   |  |JJJJJ   |  |JJJ     |
                IF( MIN(HANG(ISPEC,IGAP),HANG(ISPEC,JGAP))+1 .LT.
     &              MAX(LANG(ISPEC,IGAP),LANG(ISPEC,JGAP)) )THEN
                  LANG0 = MAX( LANG(ISPEC,IGAP),LANG(ISPEC,JGAP) )
                  HANG0 = MIN( HANG(ISPEC,IGAP),HANG(ISPEC,JGAP) )
                ELSE
                  LANG0 = MIN(LANG(ISPEC,IGAP),LANG(ISPEC,JGAP))
                  HANG0 = MAX(HANG(ISPEC,IGAP),HANG(ISPEC,JGAP))
                END IF
              ELSE IF( WRAPI.AND..NOT.WRAPJ )THEN
C               CASES:
C               |IIIII  I|  |III    I|  |III  III|  |I    III|  |I   IIIII|
C               | JJJ    |  | JJJJ   |  | JJJJJJ |  |   JJJJ |  |     JJJ |
                IF( HANG(ISPEC,JGAP)+1.LT.LANG(ISPEC,IGAP) )THEN
                  LANG0 = LANG(ISPEC,IGAP)
                ELSE
                  LANG0 = MIN(LANG(ISPEC,IGAP),LANG(ISPEC,JGAP))
                END IF
                IF( LANG(ISPEC,JGAP)-1.GT.HANG(ISPEC,IGAP) )THEN
                  HANG0 = HANG(ISPEC,IGAP)
                ELSE
                  HANG0 = MAX(HANG(ISPEC,IGAP),HANG(ISPEC,JGAP))
                END IF
                IF( LANG0.LE.HANG0 )THEN
                  LANG0 = 1
                  HANG0 = NANG
                END IF
              ELSE IF( WRAPJ.AND..NOT.WRAPI )THEN
C               CASES:
C               |JJJJJ  J|  |JJJ    J|  |JJJ  JJJ|  |J    JJJ|  |J   JJJJJ|
C               | III    |  | IIII   |  | IIIIII |  |   IIII |  |     III |
                IF( HANG(ISPEC,IGAP)+1.LT.LANG(ISPEC,JGAP) )THEN
                  LANG0 = LANG(ISPEC,JGAP)
                ELSE
                  LANG0 = MIN(LANG(ISPEC,IGAP),LANG(ISPEC,JGAP))
                END IF
                IF( LANG(ISPEC,IGAP)-1.GT.HANG(ISPEC,JGAP) )THEN
                  HANG0 = HANG(ISPEC,JGAP)
                ELSE
                  HANG0 = MAX(HANG(ISPEC,IGAP),HANG(ISPEC,JGAP))
                END IF
                IF( LANG0.LE.HANG0 )THEN
                  LANG0 = 1
                  HANG0 = NANG
                END IF
              ELSE
C               CASES:
C               |IIIII  I|  |III    I|  |I      I|
C               |J  JJJJJ|  |J    JJJ|  |JJJ  JJJ|
C
C               |III  III|  |I    III|  |I  IIIII|
C               |J      J|  |JJJ    J|  |JJJJJ  J|
                LANG0 = MIN(LANG(ISPEC,IGAP),LANG(ISPEC,JGAP))
                HANG0 = MAX(HANG(ISPEC,IGAP),HANG(ISPEC,JGAP))
                IF( LANG0.LE.HANG0 )THEN
                  LANG0 = 1
                  HANG0 = NANG
                END IF
              END IF
              LFRE0 = MIN(LFRE(ISPEC,IGAP),LFRE(ISPEC,JGAP))
              HFRE0 = MAX(HFRE(ISPEC,IGAP),HFRE(ISPEC,JGAP))
              LANG(ISPEC,IGAP) = LANG0
              LANG(ISPEC,JGAP) = LANG0
              HANG(ISPEC,IGAP) = HANG0
              HANG(ISPEC,JGAP) = HANG0
              LFRE(ISPEC,IGAP) = LFRE0
              LFRE(ISPEC,JGAP) = LFRE0
              HFRE(ISPEC,IGAP) = HFRE0
              HFRE(ISPEC,JGAP) = HFRE0
            END IF
          END DO
        END DO
      END DO


C     2.2 REDUCE INDICES OF FRAMES :
C     ------------------------------
C
      DO ISPEC = 1,NSPEC
        DO IGAP = 1,NGAP(ISPEC)-1
          JGAP = IGAP+1
          DO WHILE( JGAP.LE.NGAP(ISPEC) )
            DO WHILE( (EQUIGAP(ISPEC,IGAP,JGAP)
     &          .OR.EQUIGAP(ISPEC,JGAP,IGAP))
     &          .AND. JGAP.LE.NGAP(ISPEC) )
C             COMBINE IGAP AND JGAP TO IGAB AND TRANSFER NGAP(ISPEC) TO JGAP
              LANG(ISPEC,JGAP) = LANG(ISPEC,NGAP(ISPEC))
              HANG(ISPEC,JGAP) = HANG(ISPEC,NGAP(ISPEC))
              LFRE(ISPEC,JGAP) = LFRE(ISPEC,NGAP(ISPEC))
              HFRE(ISPEC,JGAP) = HFRE(ISPEC,NGAP(ISPEC))
              DO KGAP = 1,NGAP(ISPEC)
                EQUIGAP(ISPEC,IGAP,KGAP) = EQUIGAP(ISPEC,IGAP,KGAP)
     &              .OR.EQUIGAP(ISPEC,JGAP,KGAP)
                EQUIGAP(ISPEC,JGAP,KGAP)
     &              = EQUIGAP(ISPEC,NGAP(ISPEC),KGAP)
              END DO
              DO KGAP = 1,NGAP(ISPEC)
                EQUIGAP(ISPEC,KGAP,IGAP) = EQUIGAP(ISPEC,KGAP,IGAP)
     &              .OR.EQUIGAP(ISPEC,KGAP,JGAP)
                EQUIGAP(ISPEC,KGAP,JGAP)
     &              = EQUIGAP(ISPEC,KGAP,NGAP(ISPEC))
              END DO
              NGAP(ISPEC) = NGAP(ISPEC) - 1
            END DO
            JGAP = JGAP + 1
          END DO
        END DO
C
C       2.3 COMBINE GAPS IF CORNERS COINCIDE.
C       -------------------------------------
C
        IGAP=1
        DO WHILE(IGAP.LE.NGAP(ISPEC))
         IF(LANG(ISPEC,IGAP).EQ.HANG(ISPEC,IGAP).OR.
     1      LFRE(ISPEC,IGAP).EQ.HFRE(ISPEC,IGAP)) THEN
          DO JGAP=igap,NGAP(ISPEC)
           LANG(ISPEC,JGAP) = LANG(ISPEC,JGAP+1)
           HANG(ISPEC,JGAP) = HANG(ISPEC,JGAP+1)
           LFRE(ISPEC,JGAP) = LFRE(ISPEC,JGAP+1)
           HFRE(ISPEC,JGAP) = HFRE(ISPEC,JGAP+1)
          END DO
           NGAP(ISPEC)=NGAP(ISPEC)-1
         else
          igap=igap+1
         END IF
        END DO
      END DO

      RETURN

      END

C
C-------------------------------------------------------------------
C
      SUBROUTINE INITTUSTRE( 
C                    DIMENSIONS
     &                 DIMANG , NANG , DIMFRE , NFRE ,
C                    OUTPUT
     &                 FRE1 , CO , FRETAB , COSTAB , SINTAB , 
     &                 DFIM , FX , FY )
C
C-------------------------------------------------------------------
C
      IMPLICIT NONE
C
C     PURPOSE:
C     --------
C
C     INITIALIZE SOME ARRAYS 
C
C     AUTHOR.
C     -------
C     S.HASSELMANN, MPI HAMBURG, 1993.
C     J.WASZKEWITZ, MPI HAMBURG, 1993.
C 
C     INTERFACE:
C     ----------
C
      INTEGER DIMANG, NANG, DIMFRE, NFRE
C                   DIMENSIONS.
      DOUBLE PRECISION  FRE1, CO
C                   FREQUENCIES, RATIO OF ADJACENT FREQUENCIES.
      DOUBLE PRECISION  FRETAB(DIMFRE), 
     &     COSTAB(DIMANG), 
     &     SINTAB(DIMANG),
     &     DFIM( DIMFRE ), 
     &     FX(DIMANG,DIMFRE), 
     &     FY(DIMANG,DIMFRE)
C                    TABLES FOR FREQENCIES,COSINE AND SINE OF 
C                    DIRECTIONS, FREQUENCY INCREMENTS/DIRECTIONAL 
C                    INCREMENT, POLAR COORDINATES.
C
C     VARIABLE:
C     ---------
C
      INTEGER IFRE, IANG
      DOUBLE PRECISION  PI
C
C-------------------------------------------------------------------
C

      PI = ACOS(-1.)
C
C     LOGARITHMIC FREQUENCY ARRAY.
C
      FRETAB(1) = FRE1
      DFIM(1) = (CO-1) * PI / NANG * FRETAB(1)
      DO IFRE=2,NFRE-1
        FRETAB(IFRE) = FRETAB(IFRE-1) * CO
        DFIM(IFRE) = (CO-1) * PI / NANG * (FRETAB(IFRE)+
     &                                     FRETAB(IFRE-1))
      END DO
      FRETAB(NFRE) = FRETAB(NFRE-1)*CO
      DFIM(NFRE) = (CO-1) * PI / NANG * FRETAB(NFRE-1)
      DO IANG=1 , NANG
        COSTAB(IANG) = COS( 2*PI*(IANG-1)/NANG )
        SINTAB(IANG) = SIN( 2*PI*(IANG-1)/NANG )
      END DO
      DO IANG = 1,NANG
        DO IFRE = 1,NFRE
          FX(IANG,IFRE) = FRETAB(IFRE) * COSTAB(IANG)
          FY(IANG,IFRE) = FRETAB(IFRE) * SINTAB(IANG)
        END DO
      END DO
 
      RETURN

      END

C
C------------------------------------------------------------------
C
      SUBROUTINE TRANSMEANS(
C                     DIMENSIONS
     &                  DIMSPEC , MSPEC , NSPEC ,
     &                  DIMANG , NANG , DIMFRE , NFRE ,
C                     INPUT
     &                  SPECW ,
C                     OUTPUT
     &                  MEANTE , MEANTANG , MEANTFRE ,
C                     WORK SPACE
     &                  SUM0 , SUMX0 , SUMY0 ,
C                     INPUT TABLES
     &                  FRE1 , CO , FRETAB , COSTAB , SINTAB,DFIM)
C
C-------------------------------------------------------------------
C
      IMPLICIT NONE
C
C     PURPOSE:
C     --------
C
C     MEAN VALUES OF TRANSFORMED SPECTRA
C     COMPUTES MEAN ENERGY,MEAN ANGLE AND MEAN FREQUENCY
C
C     INTERFACE:
C     ----------
C
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMANG, NANG, DIMFRE, NFRE
C                     DIMENSIONS.
      DOUBLE PRECISION  SPECW(0:MSPEC,NANG,NFRE)
C                     2D SPECTRUM.
      DOUBLE PRECISION  MEANTE(MSPEC),
     &     MEANTANG(MSPEC), 
     &     MEANTFRE(MSPEC)
C                     MEAN PARAMETERS.
      DOUBLE PRECISION  SUM0(DIMSPEC), SUMX0(DIMSPEC), SUMY0(DIMSPEC)
C                     WORK SPACE FOR TEMPORARY SUMS.   
      DOUBLE PRECISION  FRE1, CO
      DOUBLE PRECISION  FRETAB(DIMFRE), COSTAB(DIMANG), SINTAB(DIMANG),
     &    DFIM(DIMFRE)
C                     TABLES OF FREQUENCIES, COS,SINE OF DIRECTIONS,
C                     FREQUENCY INCREMENTS/DIRECTIONAL INCREMENT, 
C                     RESPECTIVELY.
C
C     VARIABLES:
C     ----------
C
      INTEGER ISPEC, IANG, IFRE
C                     LOOP VARIABLES.
      DOUBLE PRECISION  PI, PI2NANG, FACTOR
C
C-------------------------------------------------------------------
C


C     INITIALIZE:
C     -----------

      PI = ACOS(-1.)
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


C     COMPUTE MEAN ENERGIES:
C     ----------------------

      DO ISPEC = 1,NSPEC
        MEANTE(ISPEC) = 0.
      END DO
      DO IFRE = 1,NFRE
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

c      PI = 3.141592653589793
      PI2NANG = PI / 2 / NANG
      DO ISPEC = 1,NSPEC
        MEANTE(ISPEC)
     &      = MEANTE(ISPEC) + FRETAB(NFRE) * PI2NANG * SUM0(ISPEC)
      END DO


C     COMPUTE MEAN ANGLES:
C     --------------------

      DO ISPEC = 1,NSPEC
        SUMX0(ISPEC) = 0.
        SUMY0(ISPEC) = 0.
      END DO

      DO IANG = 1,NANG
        DO ISPEC = 1,NSPEC
          SUM0(ISPEC) = 0.
        END DO
        DO IFRE=1,NFRE
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


C     COMPUTE MEAN FREQUENCIES:
C     -------------------------
        
      DO ISPEC = 1,NSPEC
        MEANTFRE(ISPEC) = 0.
      END DO

      DO IFRE = 1,NFRE
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
C
C-----------------------------------------------------------------------
C
      SUBROUTINE TRANSFORM( 
C                    DIMENSIONS
     &                 DIMSPEC , MSPEC , NSPEC , DIMPART , MPART , 
     &                 NPARTW , DIMANG , NANG , DIMFRE , NFRE ,
C                    INPUT/OUTPUT
     &                 SPECW , 
C                    WORK SPACE
     &                 SPECT , 
C                    INPUT
     &                 PARTW ,CORRELTAW ,MEANWE,MEANWANG,MEANWFRE, 
     &                 MEANSE , MEANSANG , MEANSFRE ,
     &                 FRE1 , CO,
C                    OUTPUT
     &                 ADJUST , INTROTATE , FRACROTATE , 
     &                 STRETCH , INTLOGSTRETCH ,
     &                 COPO , COPODIFF  )
C
C-------------------------------------------------------------------
C
      IMPLICIT NONE
C
C
C     PURPOSE:
C     --------
C
C     TRANSFORMS PARTITIONINGS OF WAM FIRST GUESS SPECTRA TO 
C     MATCH THE MEAN VALUES TO THE PARTITIONINGS OF THE SAR 
C     RETRIEVED SPECTRA
C
C     S. HASSELMANN, MPI HAMBURG, 1993.
C     J. WASZKEWITZ, MPI HAMBURG, 1993.
C
C     INTERFACE:
C     ----------
C
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMPART, MPART,
     &    NPARTW(MSPEC), DIMANG, NANG, DIMFRE, NFRE
C                   DIMENSIONS.
      DOUBLE PRECISION  SPECW(0:MSPEC,NANG,NFRE), 
     &     SPECT(DIMSPEC,DIMANG,DIMFRE)
C                   WAM SPECTRM BEFORE AND AFTER CORRECTION 
C                   AND WORK SPACE.
      INTEGER PARTW(MSPEC,NANG,NFRE)
C                   ASSIGNMENT OF A PARTITIONING NUMBER TO EACH 
C                   DIRECTIONAL-FREQUENCY BIN.
      INTEGER CORRELTAW(MSPEC,MPART)
C                   CROSSASSIGNMENT OF WAM PARTITIONINGS TO SAR
C                   PARTITIONINGS.
      DOUBLE PRECISION  MEANWE(MSPEC,MPART),
     &     MEANWANG(MSPEC,MPART),
     &     MEANWFRE(MSPEC,MPART),
     &     MEANSE(MSPEC,MPART),
     &     MEANSANG(MSPEC,MPART), 
     &     MEANSFRE(MSPEC,MPART)
C                   MEAN VALUES FOR WAM AND SAR PARTITIONINGS.
      DOUBLE PRECISION  ADJUST(DIMSPEC,DIMPART)
C                   FACTOR FOR ENERGY ADJUSTMENT.
      INTEGER INTROTATE(DIMSPEC,DIMPART)
C                   ROTAION PARAMETER(NUMBER OF GRID POINTS)
      DOUBLE PRECISION  FRACROTATE(DIMSPEC,DIMPART)
C                   FRACTIONAL ROTATION PARAMETER.
      DOUBLE PRECISION  STRETCH(DIMSPEC,DIMPART)
C                   FREQUENCY TRANSFORMATION PARAMETER.
      INTEGER INTLOGSTRETCH(DIMSPEC,DIMPART)
C                   FREQUENCY TRANSFORMATION PARAMETER(GRID)
      DOUBLE PRECISION  COPO(DIMFRE), COPODIFF(DIMFRE)
      DOUBLE PRECISION  FRE1, CO
C
C
C     VARIABLES:
C     ----------
C
      INTEGER ISPEC, IPARTW, IPARTS, IANG, IFRE
C                    LOOP INDICES.
      INTEGER JANG, JANGP1, JFRE, JFREP1
C                    GRIDPOINT INDICES AFTER INTERPOLATED
C                    JANGP1 = "JANG PLUS 1" , JFREP1 = "JFRE PLUS 1"
      DOUBLE PRECISION  AANG, BANG, AFRE, BFRE
C                    FOR INTERPOLATION
      DOUBLE PRECISION  ROTATE
C                    THE NUMBER OF GRIDPOINTS THE PARTITIONING 
C                    MUST BE ROTATED
      DOUBLE PRECISION  PI, PI2, DELTANG, LOGCO, ENERGY,srotate
C
C-------------------------------------------------------------------
C
C     INITIALIZATION:
C     ---------------

      PI = ACOS(-1.)
      PI2 = 2 * PI
      DELTANG = PI2 / NANG
      LOGCO = LOG(CO)
      COPO(1) = CO
      DO IFRE = 2,NFRE
        COPO(IFRE) = COPO(IFRE-1) * CO
        COPODIFF(IFRE) = COPO(IFRE) - COPO(IFRE-1)
      END DO
      DO ISPEC = 1,NSPEC
        INTROTATE(ISPEC,1)=0
        DO IPARTW = 1,NPARTW(ISPEC)
          IPARTS = CORRELTAW(ISPEC,IPARTW)
          IF( IPARTS.EQ.0 )THEN
            ADJUST(ISPEC,IPARTW) = 1.
            INTROTATE(ISPEC,IPARTW) = 0.
            FRACROTATE(ISPEC,IPARTW) = 0.
            STRETCH(ISPEC,IPARTW) = 1.
            INTLOGSTRETCH(ISPEC,IPARTW) = 0.
          ELSE
            ADJUST(ISPEC,IPARTW)
     &        = MEANSE(ISPEC,IPARTS) / MEANWE(ISPEC,IPARTW)
            ROTATE
     &        = ( MEANSANG(ISPEC,IPARTS) - MEANWANG(ISPEC,IPARTW) )
            ROTATE=ROTATE/ DELTANG
            INTROTATE(ISPEC,IPARTW) = INT(ROTATE)
            FRACROTATE(ISPEC,IPARTW) = ROTATE - INT(ROTATE)
            STRETCH(ISPEC,IPARTW)
     &        = MEANSFRE(ISPEC,IPARTS) / MEANWFRE(ISPEC,IPARTW)
            INTLOGSTRETCH(ISPEC,IPARTW)
     &        = INT( LOG(STRETCH(ISPEC,IPARTW))/LOGCO+10000 ) - 10000
          END IF
        END DO
      END DO
C
C     ROTATE, STRETCH AND ADJUST THE WAM FIRST GUESS PARTITIONINGS
C     IN ONE STEP AND ADD THEM TO ARRAY SPECT:
C     ------------------------------------------------------------

      DO JANG = 1,NANG
        DO JFRE = 1,NFRE
          DO ISPEC = 1,NSPEC
            SPECW(ISPEC,JANG,JFRE) = max(SPECW(ISPEC,JANG,JFRE),
     &                                   0.1D-15)
            SPECT(ISPEC,JANG,JFRE) = 0.1D-19
          END DO
        END DO
      END DO

      DO IANG = 1,NANG
        DO IFRE = 1,NFRE
C
C         ("CDIR$ IVDEP" IS A COMPILER DIRECTIVE TO FORCE CFT77
C         TO VECTORIZE THE NEXT LOOP)
          DO ISPEC = 1,NSPEC
            IPARTW = PARTW(ISPEC,IANG,IFRE)           
            JANG = IANG + INTROTATE(ISPEC,IPARTW)
            IF( JANG.GT.NANG ) JANG = JANG - NANG
            IF( JANG.LT.1 ) JANG = JANG + NANG
            IF((INTROTATE(ISPEC,IPARTW)+
     &          FRACROTATE(ISPEC,IPARTW)).GT.0) THEN
             JANGP1 = JANG + 1
            ELSE
             JANGP1 = JANG - 1
            END IF
            IF( JANGP1.GT.NANG ) JANGP1 = JANGP1 - NANG
            IF( JANGP1.LT.1 ) JANGP1 = JANGP1 + NANG
            JFRE = IFRE + INTLOGSTRETCH(ISPEC,IPARTW)
            JFREP1 = JFRE + 1
            IF( JFRE.GE.1 .AND. JFREP1.LE.NFRE )THEN
              BANG = abs(FRACROTATE(ISPEC,IPARTW))
              AANG = 1 - BANG
C             AFRE = (CO**(JFRE+1)-CO**IFRE*STRETCH))/(CO**(JFRE+1)-
c     1                CO**JFRE))
              AFRE = ( COPO(JFREP1)
     &            - COPO(IFRE) * STRETCH(ISPEC,IPARTW) )
     &            / COPODIFF(JFREP1)    
              BFRE = 1 - AFRE
              ENERGY = SPECW(ISPEC,IANG,IFRE) * ADJUST(ISPEC,IPARTW)
              SPECT(ISPEC,JANG  ,JFRE  )
     &            = SPECT(ISPEC,JANG  ,JFRE  ) +
     &                   ENERGY * AANG * AFRE 
              SPECT(ISPEC,JANG  ,JFREP1)
     &            = SPECT(ISPEC,JANG  ,JFREP1) +
     &                   ENERGY * AANG * BFRE 
              SPECT(ISPEC,JANGP1,JFRE  ) 
     &            = SPECT(ISPEC,JANGP1,JFRE  ) +
     &                   ENERGY * BANG * AFRE 
              SPECT(ISPEC,JANGP1,JFREP1) 
     &            =  SPECT(ISPEC,JANGP1,JFREP1) +
     &                   ENERGY * BANG * BFRE 
            END IF 
          END DO
        END DO
      END DO

C     TRANSFER SPECT TO SPECW
C     -----------------------

      DO IANG = 1,NANG
        DO IFRE = 1,NFRE
          DO ISPEC = 1,NSPEC
            SPECW(ISPEC,IANG,IFRE) = SPECT(ISPEC,IANG,IFRE)
          END DO
        END DO
      END DO
 
      RETURN

      END

