      SUBROUTINE CROSSAS2(
c             dimensions
     &          MSPEC , NSPEC , MPART , NPARTW, NPARTS ,
     &          NANG , NFRE ,
c             input
     &          DISMIN,
     &          MEANWE , MEANWANG, MEANWFRE ,
     &          MEANSE , MEANSANG, MEANSFRE ,
     &          CONTROL,
c             output
     &          CORRELTAW,CORRELTAS)

c
c-----------------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c     used in sar retrieval system.
c
c     crossassign wam and sar partitionings.
c
c     to make this routine as fast as possible, the loop over all
c     spectra is a vectorized inner loop.
c
c     
c     author:
c     -------
c
c     susanne hasselmann 1993 at mpi fuer meteorologie hamburg
c     juergen waszkewtiz 1993 at mpi fuer meteorologie hamburg
c
c     externals:
c     ----------
c
c     checkcorrelpara - check 
c
c
c
c-----------------------------------------------------------------------
c
      IMPLICIT NONE
c
c     parameters:
c     -----------
c
c      integer dimspec, dimpart
c             dimension sizes of working arrays, it must be
c             dimspec >= mspec , dimpart >= mpart
c
      include "dimpar.par"
c
c     interface:
c     ----------
c
      INTEGER MSPEC
c                     maximal number (=dimension size) of spectra.
      INTEGER NSPEC
c                     number of spectra.
      INTEGER MPART
c                     aximal number (=dimension size)
c                     of partitionings
      INTEGER NPARTW(MSPEC)
c                     number of partitionings
c                     of the wam first guess spectra
      INTEGER NPARTS(MSPEC)
c                     number of 
c                     partitionings of the inverted sar spectra
      INTEGER NANG
c                     number of directions in spectra.
      INTEGER NFRE
c                     number of spectral  frequencies.
      DOUBLE PRECISION DISMIN
c                     sar and wam wave systems are crossassigned if their 
c                     distance is less than dismin.
c
      INTEGER CORRELTAW(MSPEC,MPART)
c                     correlation table, where correltaw(ispec,ipartw)
c                     means, that partit. ipartw of wam first guess 
c                     spectrum ispec is correlated with 
c                     partitionig correltaw(ispec,ipartw)
c                     of inverted sar spectrum ispec
c                     (a zero means, no crossassignment)
      INTEGER CORRELTAS(MSPEC,MPART)
c                     >0 = correltaw
c                     <0 no crossassignment to a wam-partitioning.
      DOUBLE PRECISION  MEANWE(MSPEC,MPART)
c                     mean energies of partitionings
c                     of wam first guess spectra.
      DOUBLE PRECISION  MEANWANG(MSPEC,MPART)
c                     mean directions in radiance
c                     of partitionings of wam first guess spectra.
      DOUBLE PRECISION  MEANWFRE(MSPEC,MPART)
c                     mean frequencies of partitionings
c                     of wam first guess spectra.
      DOUBLE PRECISION  MEANSE(MSPEC,MPART)
c                     mean energies of partitionings
c                     of inverted sar spectras.
      DOUBLE PRECISION  MEANSANG(MSPEC,MPART)
c                     mean directions in radiance
c                     of partitionings of inverted sar spectra.
      DOUBLE PRECISION  MEANSFRE(MSPEC,MPART)
c                     mean frequencies of partitionings
c                     of inverted sar spectra.
      LOGICAL CONTROL
c                     (input) write control messages on unit 6 ?
c                     .true. = yes , .false. = no
c
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IPARTW, IPARTS
c                      loop indexes.
      INTEGER NPARTWMAX, NPARTSMAX
c                      maximum value of npartw/nparts over all 
c                      spectra
      DOUBLE PRECISION  DIST(DIMSPEC,DIMPART,DIMPART)
c                      the square of the distance between two systems
c                      in k-space.
      DOUBLE PRECISION  MINDIST
c                      minimal distance for cross assignment.
      DOUBLE PRECISION  FWX(DIMSPEC,DIMPART), FWY(DIMSPEC,DIMPART)
c                      mean wave numbers of wam partitionings.
      DOUBLE PRECISION  FSX(DIMSPEC,DIMPART), FSY(DIMSPEC,DIMPART)
c                      mean wave numbers of sar partitionings.
      DOUBLE PRECISION  PI, PI180,zpi,akabs
      INTEGER IPARWH,IPARWH1,IPARSH,IPSH
      DOUBLE PRECISION  MINDIS(DIMPART),MINDISH
c
c---------------------------------------------------------------------
c
      IF( CONTROL ) WRITE(6,*) 'CALL OF SUBROUTINE CORREL'
      CALL CHECKCORRELPAR( DIMSPEC , MSPEC , DIMPART , MPART )
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
c      compute wave number arrays.
c
      DO ISPEC = 1,NSPEC
        do ipartw=1,npartwmax
        FWX(ISPEC,IPARTW)=0.1e-10
        FWy(ISPEC,IPARTW)=0.1e-10
        end do
        do iparts=1,npartsmax
        FsX(ISPEC,IPARTs)=0.1e-10
        Fsy(ISPEC,IPARTs)=0.1e-10
        end do
        DO IPARTW = 1,NPARTW(ISPEC)
          akabs=(zpi*MEANWFRE(ISPEC,IPARTW))**2/9.806
          FWX(ISPEC,IPARTW)
     &         = akabs * COS( MEANWang(ISPEC,IPARTW) )
          FWY(ISPEC,IPARTW)
     &         = akabs * SIN( MEANWang(ISPEC,IPARTW) )
        END DO
        DO IPARTS = 1,NPARTS(ISPEC)
          akabs=(zpi*MEANsFRE(ISPEC,IPARTS))**2/9.806
          FSX(ISPEC,IPARTS)
     &         = akabs * COS( MEANSang(ISPEC,IPARTS) )
          FSY(ISPEC,IPARTS)
     &         = akabs * SIN( MEANSang(ISPEC,IPARTS) )
        END DO
      END DO
c
c     compute distance between sar and wam peaks.
c
      DO IPARTW = 1,NPARTWMAX
        DO IPARTS = 1,NPARTSMAX
          DO ISPEC = 1,NSPEC
            AKABS=(0.5*(FWX(ISPEC,IPARTW)**2+FSX(ISPEC,IPARTS)**2+
     &           FWY(ISPEC,IPARTW)**2+FSY(ISPEC,IPARTS)**2))
            AKABS=MAX(AKABS,0.1D-10)
            DIST(ISPEC,IPARTW,IPARTS)
     &          = (( FWX(ISPEC,IPARTW) - FSX(ISPEC,IPARTS) ) ** 2
     &          + ( FWY(ISPEC,IPARTW) - FSY(ISPEC,IPARTS) ) ** 2)/
     &         AKABS
          END DO
        END DO
      END DO
c
c     compute minimum distance for each wam to sar peaks and 
c     cross assign wam and sar wave systems.
c
      DO ISPEC = 1,NSPEC
        DO IPARTS=1,NPARTS(ISPEC)
         CORRELTAS(ISPEC,IPARTS)=-1
         MINDIS(IPARTS)=100.
        END DO
        DO IPARTW = 1,NPARTW(ISPEC)
          CORRELTAW(ISPEC,IPARTW)=0
          MINDIST=100.
          DO IPARTS = 1,NPARTS(ISPEC)
            IF( DIST(ISPEC,IPARTW,IPARTS).LT.DISMIN )THEN
               IF(DIST(ISPEC,IPARTW,IPARTS).LT.MINDIST) THEN
                IF(CORRELTAS(ISPEC,IPARTS).LT.0 ) THEN
                   IF(CORRELTAW(ISPEC,IPARTW).GT.0) THEN
                    CORRELTAS(ISPEC,CORRELTAW(ISPEC,IPARTW))=-1
                    MINDIS(CORRELTAW(ISPEC,IPARTW))=100.
                   END IF
                   MINDIST=DIST(ISPEC,IPARTW,IPARTS)
                   CORRELTAW(ISPEC,IPARTW) = IPARTS
                   CORRELTAS(ISPEC,IPARTS)=ipartw
                   MINDIS(IPARTS)=MINDIST
                 ELSEIF(DIST(ISPEC,IPARTW,IPARTS).LT.MINDIS(IPARTS))
     &                         THEN
                   MINDIST=DIST(ISPEC,IPARTW,IPARTS)
                   CORRELTAW(ISPEC,IPARTW) = IPARTS
                   IF(CORRELTAS(ISPEC,IPARTS).NE.IPARTW.AND.
     &                CORRELTAS(ISPEC,IPARTS).GT.0)THEN
                    CORRELTAW(ISPEC,CORRELTAS(ISPEC,IPARTS)) = 0
                    MINDISH=DISMIN
                    IPARWH=CORRELTAS(ISPEC,IPARTS)
                    IPSH=0
                    IPARWH1=-1
                    DO IPARSH=1,NPARTS(ISPEC)
                     IF(CORRELTAS(ISPEC,IPARSH).LT.0.AND.
     &                  DIST(ISPEC,IPARWH,IPARSH).
     &                  LT.MINDISH.AND.IPARSH.NE.IPARTS) THEN
                      MINDISH=DIST(ISPEC,IPARWH,IPARSH)
                      IPSH=IPARSH
                      IPARWH1=IPARWH
                     END IF
                    END DO
                    IF(IPSH.GT.0) THEN
                     CORRELTAW(ISPEC,IPARWH1) = IPSH
                     CORRELTAS(ISPEC,IPSH)=IPARWH1
                     MINDIS(IPSH)=MINDISH
                    END IF
                   END IF
                   CORRELTAS(ISPEC,IPARTS)=ipartw
c                 ELSE
c                   CORRELTAW(ISPEC,IPARTW) = 0
                 END IF
               END IF
            ELSEIF(MINDIST.EQ.100.) THEN
                CORRELTAW(ISPEC,IPARTW) = 0
            END IF
           END DO
        END DO
       END DO
c
      IF( CONTROL ) WRITE(6,*) 'ENDING SUBROUTINE CROSSAS'
c
      RETURN
c
      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE CHECKCORRELPAR( DIMSPEC , MSPEC , DIMPART , MPART )
c
c-----------------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c     checks if parameters are big enough
c
c
c-----------------------------------------------------------------------
      IMPLICIT NONE
c
c     interface:
c     ----------
c
      INTEGER DIMSPEC, MSPEC, DIMPART, MPART
c
c     local variables:
c     ----------------
c
      LOGICAL ERROR
c
c-----------------------------------------------------------------------
c
      ERROR = .FALSE.
      IF( DIMSPEC.NE.MSPEC )THEN
        ERROR = .TRUE.
        WRITE(6,*) 'ERROR! SUBROUTINE TUSTRE:'
        WRITE(6,*) 'PARAMETER DIMSPEC IS TOO SMALL!'
        WRITE(6,*) 'IT MUST BE DIMSPEC >= MSPEC = ',MSPEC,'!'
        WRITE(6,*) 'CHANGE PARAMETER DIMSPEC!'
      END IF
      IF( DIMPART.NE.MPART )THEN
        ERROR = .TRUE.
        WRITE(6,*) 'ERROR! SUBROUTINE TUSTRE:'
        WRITE(6,*) 'PARAMETER DIMPART IS TOO SMALL!'
        WRITE(6,*) 'IT MUST BE DIMPART >= MPART = ',MPART,'!'
        WRITE(6,*) 'CHANGE PARAMETER DIMPART!'
      ENDIF
      IF( ERROR )THEN
        STOP 'ERROR IN SUBROUTINE TUSTRE!'
      END IF

      RETURN

      END











