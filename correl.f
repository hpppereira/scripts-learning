      SUBROUTINE CORREL(
c            dimensions
     &         MSPEC , NSPEC , MPART , NANG , NFRE ,
c            input
     &         NPARTW , NPARTS , PARTS , DISMIN,
     &         MEANWE, MEANWANG , MEANWFRE ,
     &         MEANSE , MEANSANG , MEANSFRE ,
     &         CONTROL )
c
c----------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c
c     combine partitionings of inverted sar spectra if they belong
c     to the same partitioning of wam first guess spectra
c
c     to make this routine as fast as possible, the loop
c     over all spectras is a vectorized inner loop.
c
c
c     author:
c     -------
c
c     s.hasselmann, 1993 at mpi fuer meteorologie hamburg
c     j.waszkewtiz, 1993 at mpi fuer meteorologie hamburg
c
c
c
c     externals:
c     ----------
c
c     checkcorrelpara - check
c
c----------------------------------------------------------------
c
c     parameters:
c     -----------
c
c      integer dimspec, dimpart
c       dimension sizes of working arrays, it must be
c       dimspec >= mspec , dimpart >= mpart
c
      IMPLICIT NONE
      include "dimpar.par"
c
c
c     interface variables:
c     --------------------
c
      INTEGER MSPEC
c                     the maximal number (=dimension size) of spectra.
      INTEGER NSPEC
c                     the number of spectra.
      INTEGER MPART
c                     the maximal number (=dimension size)
c                     of partitionings.
      INTEGER NPARTW(MSPEC)
c                     number of partitionings
c                     in wam first guess spectra
      INTEGER NPARTS(MSPEC)
c                     number of partitionings
c                     in sar retrieved spectra.
      INTEGER NANG
c                     number of spectral directions.
      INTEGER NFRE
c                     number of frequencies.
      INTEGER PARTS(MSPEC,NANG,NFRE)
c                     partitioning number of the sar retrieved
c                     spectra for each spectral bin.
      DOUBLE PRECISION DISMIN
c                     2 sar wave systems are combined if the distance
c                     between both and a wam first guess partitioning
c                     is less than dismin.
c
      DOUBLE PRECISION MEANWE(MSPEC,MPART)
c                      mean energies of partitionings
c                      of wam first guess spectras,
      DOUBLE PRECISION MEANWANG(MSPEC,MPART)
c                     mean angles in radiance
c                     of partitionings of wam first guess spectra.
      DOUBLE PRECISION MEANWFRE(MSPEC,MPART)
c                     mean frequencies of partitionings
c                     of wam first guess spectra.
      DOUBLE PRECISION MEANSE(MSPEC,MPART)
c                     mean energies of partitionings
c                     of inverted sar spectra.
      DOUBLE PRECISION meansang(mspec,mpart)
c                     mean angles in radiance
c                     of partitionings of inverted sar spectra.
      DOUBLE PRECISION MEANSFRE(MSPEC,MPART)
c                     mean frequencies of partitionings
c                     of inverted sar spectras.
      LOGICAL CONTROL
c                     write control messeges on unit 6 ?
c                     .true. = yes , .false. = no
c
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IPARTW, IPARTS, IANG, IFRE
c             loop indexes
      INTEGER NPARTWMAX, NPARTSMAX
c             maximum value of npartw/nparts over all spectra
      DOUBLE PRECISION DIST(DIMSPEC,DIMPART,DIMPART)
c             the square of the distance between two wave systems
c             in k-space.
      DOUBLE PRECISION MINDIST
c             for searching a minimal distance for combining of sar
c             wave systems.
      DOUBLE PRECISION FWX(DIMSPEC,DIMPART), FWY(DIMSPEC,DIMPART)
c             kx ky of wam first guess spectral partitionings.
      DOUBLE PRECISION FSX(DIMSPEC,DIMPART), FSY(DIMSPEC,DIMPART)
c             kx,ky of the inverted sar spectral partitionings.
      INTEGER NEAREST(DIMPART,10)
c               nearest(ipartw,1) is combined with nearest(ipartw,>1).
      INTEGER LPARTS,HPARTS
c               hparts is combined with lparts.
      DOUBLE PRECISION PI, PI180,zpi,akabs

      INTEGER IST(DIMPART),IS, npartsh,ISH,flag(dimpart),IPWH
c
      DOUBLE PRECISION angdiff
c
c     difference between mean angles of partitionings.
c     ------------------------------------------------
c
      IF( CONTROL ) WRITE(3,*) 'CALL OF SUBROUTINE CORREL'
      PI = 3.141592653589793
      ZPI=2.*PI
      PI180 = 180. / PI
      NPARTWMAX = 0
      NPARTSMAX = 0
      DO ISPEC = 1,NSPEC
        IF( NPARTW(ISPEC).GT.NPARTWMAX ) NPARTWMAX = NPARTW(ISPEC)
        IF( NPARTS(ISPEC).GT.NPARTSMAX ) NPARTSMAX = NPARTS(ISPEC)
      END DO
c
c     1.1 compute wave number arrays.
c     ------------------------------
c
      DO ISPEC = 1,NSPEC
        DO IPARTW=1,NPARTWMAX
         FWX(ISPEC,IPARTW)=0.1E-10
         FWY(ISPEC,IPARTW)=0.1E-10
        END DO
        DO IPARTS=1,NPARTSMAX
         FSX(ISPEC,IPARTS)=0.1E-10
         FSY(ISPEC,IPARTS)=0.1E-10
        END DO
        DO IPARTW = 1,NPARTW(ISPEC)
          AKABS=(ZPI*MEANWFRE(ISPEC,IPARTW))**2/9.806
          FWX(ISPEC,IPARTW)
     &         = AKABS * COS( MEANWANG(ISPEC,IPARTW) )
          FWY(ISPEC,IPARTW)
     &         = AKABS * SIN( MEANWANG(ISPEC,IPARTW) )
        END DO
        DO IPARTS = 1,NPARTS(ISPEC)
          AKABS=(ZPI*MEANSFRE(ISPEC,IPARTS))**2/9.806
          FSX(ISPEC,IPARTS)
     &         = AKABS * COS( MEANSANG(ISPEC,IPARTS) )
          FSY(ISPEC,IPARTS)
     &         = AKABS * SIN( MEANSANG(ISPEC,IPARTS) )
        END DO
      END DO
c
c     1.2 compute distance between sar and wam peaks.
c     -----------------------------------------------
c
      DO IPARTW = 1,NPARTWMAX
        DO IPARTS = 1,NPARTSMAX
          DO ISPEC = 1,NSPEC
            AKABS=(0.5*(FWX(ISPEC,IPARTW)**2+FSX(ISPEC,IPARTS)**2+
     &           FWY(ISPEC,IPARTW)**2+FSY(ISPEC,IPARTS)**2))
            AKABS=MAX(AKABS,0.1D-10)
            DIST(ISPEC,IPARTW,IPARTS)
     &          =( ( FWX(ISPEC,IPARTW) - FSX(ISPEC,IPARTS) ) ** 2
     &          + ( FWY(ISPEC,IPARTW) - FSY(ISPEC,IPARTS) ) ** 2)/
     &          AKABS
          END DO
        END DO
      END DO
c
c     1.3 compute minimum distance for each wam to sar wave system.
c     -------------------------------------------------------------
c
      DO ISPEC = 1,NSPEC
        DO IPARTS=1,NPARTS(ISPEC)
         FLAG(IPARTS)=-1
        END DO
        DO IPARTW = 1,NPARTW(ISPEC)
          MINDIST = 1.D+100
          IS=0
          IST(IPARTW)=0
          DO IPARTS = 1,NPARTS(ISPEC)
            IF( DIST(ISPEC,IPARTW,IPARTS).LT.DISMIN )THEN
             IF(FLAG(IPARTS).LT.0) THEN
               IS=IS+1
               NEAREST(IPARTW,IS)=IPARTS
               FLAG(IPARTS)=1
             END IF
             DO ISH=IPARTS+1,NPARTS(ISPEC)
              ANGDIFF=ABS(MEANSANG(ISPEC,IPARTS)-MEANSANG(ISPEC,ISH))
              IF((ANGDIFF.LT.0.09.OR.ABS(ANGDIFF-360.).LT.0.09)
     &            .AND.FLAG(ISH).LT.0) THEN
                IS=IS+1
                NEAREST(IPARTW,IS)=ISH
                FLAG(ISH)=1
              END IF
             END DO
            END IF
          END DO
          IF(IS.LT.2) IS=0
          IST(IPARTW)=IS
        END DO
c
c      2. combine all "nearest" sar partitionings.
c      -------------------------------------------
c
        IPARTS = 1
        IPARTW = 0
        NPARTSH=NPARTS(ISPEC)
        DO IPARTW=1,NPARTW(ISPEC)
         DO IS=2,IST(IPARTW)
c           combine nearest(ipartw,1) and nearest(ipartw,is)
            IF( CONTROL )THEN
                WRITE(3,*) ' COMBINE FOR SPECTRUM ',ISPEC,' PEAKS ',
     &                       IPARTW,NEAREST(IPARTW,IS),NEAREST(IPARTW,1)
     &                   ,' DIST ',DIST(ISPEC,IPARTW,NEAREST(IPARTW,IS))
             WRITE(3,*) ' MEAN ENERGY ',MEANSE(ISPEC,NEAREST(IPARTW,1)),
     &                       MEANSE(ISPEC,NEAREST(IPARTW,IS))
               WRITE(3,*) ' MEAN ENERGY WAM ',MEANWE(ISPEC,IPARTW)
            END IF
            LPARTS = NEAREST(IPARTw,1)
            HPARTS = NEAREST(IPARTw,IS)
            IF(LPARTS.NE.HPARTS) THEN
c
c           combine lparts and hparts to lparts and change nparts
c           nparts-1
c
            IF( PARTS(1,1,1).NE.0 )THEN
              DO IANG = 1,NANG
                DO IFRE = 1,NFRE
                  IF( PARTS(ISPEC,IANG,IFRE).EQ.HPARTS )THEN
                    PARTS(ISPEC,IANG,IFRE) = LPARTS
                  ELSE IF( PARTS(ISPEC,IANG,IFRE).GT.HPARTS )THEN
                    PARTS(ISPEC,IANG,IFRE) = PARTS(ISPEC,IANG,IFRE)-1
                  END IF
                END DO
              END DO
            END IF
             IPWH=IPARTW
            DO IPWH=IPARTW,NPARTW(ISPEC)
             DO ISH=1,IST(IPWH)
              IF(NEAREST(IPWH,ISH).EQ.HPARTS)NEAREST(IPWH,ISH)=LPARTS
              IF(NEAREST(IPWH,ISH).GT.HPARTS) THEN
               NEAREST(IPWH,ISH)=NEAREST(IPWH,ISH)-1
              END IF
             END DO
            END DO
            NPARTSH=NPARTSH-1
            END IF
          END DO
        END DO
        NPARTS(ISPEC) = NPARTSH
      END DO
      IF( CONTROL ) WRITE(3,*) 'ENDING SUBROUTINE CORREL'
c
      RETURN
c
      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE CHECKCORRELPARA( DIMSPEC , MSPEC , DIMPART , MPART )
c
c-----------------------------------------------------------------------
c
c     purpose:
c     --------
c
c     checks input parameters and dummy dimensions.
c
c
c
c-----------------------------------------------------------------------
c
      IMPLICIT NONE
c     interface:
c     ----------
c
      INTEGER DIMSPEC, MSPEC, DIMPART, MPART
c
c     local variables:
c     ----------------
c
      logical error
c-----------------------------------------------------------------------
      ERROR = .FALSE.
      IF( DIMSPEC.NE.MSPEC )THEN
        ERROR = .TRUE.
        WRITE(3,*) 'ERROR! SUBROUTINE TUSTRE:'
        WRITE(3,*) 'PARAMETER DIMSPEC IS TOO SMALL!'
        WRITE(3,*) 'IT MUST BE DIMSPEC >= MSPEC = ',MSPEC,'!'
        WRITE(3,*) 'CHANGE PARAMETER DIMSPEC!'
      END IF
      IF( DIMPART.NE.MPART )THEN
        ERROR = .TRUE.
        WRITE(3,*) 'ERROR! SUBROUTINE TUSTRE:'
        WRITE(3,*) 'PARAMETER DIMPART IS TOO SMALL!'
        WRITE(3,*) 'IT MUST BE DIMPART >= MPART = ',MPART,'!'
        WRITE(3,*) 'CHANGE PARAMETER DIMPART!'
      ENDIF
      IF( ERROR )THEN
        STOP 'ERROR IN SUBROUTINE TUSTRE!'
      END IF
c
      RETURN
c
      END


