      SUBROUTINE SWELLSEPBUOY( 
cn      SUBROUTINE SWELLSEP( 
c             dimensions 
     &          MSPEC , NSPEC , MPART , NANG , NFRE ,
c             input  
     &          SPEC , U10 , THW , FRE1 , CO , LEVEL , CONTROL,
     &          LOWEST,
c             output
     &          NPART ,PART , PARTINFO ,
     &          MEANE , MEANANG , MEANFRE,
     &          spread)
c
c-------------------------------------------------------------------
c
c     purpose:
c     --------
c
c     partitioning of an array of 2-d wave spectra into windsea and
c     swell partitions.
c
c
c     methods:
c     --------
c
c     mountaineering concept: the hump domain of a spectral peak 
c     consists of all spectral points whose paths of steepest ascent
c     leads to that peak. (subroutine partitioning)
c
c     partitionings are combined to one if(subroutine combinepeaks):
c     - the peaks are only one grid point apart 
c             (subroutine onestepapart).
c     - the peak lies in last two frequency bins 
c             (subroutine lasttwobins).
c     - the distance between peaks is less than half the 
c              spread of the partitioning (subroutine halfspread).
c       
c     - the minimum energy between peaks is >level * the 
c       minimum peak energy (subroutine threshhold).
c     - the mean energy is < lowest.
c     all windsea peaks are combined to one.
c
c
c     references:
c     -----------
c
c     s. hasselmann, k. hasselmann, c. bruening, 1993:
c     extraction of wave spectra from sar image spectra. in:
c     dynamics and modeling of ocean waves. section v.4.3.
c     editor g. komen. kluwer & co, netherlands.
c
c     memorandum for wam group by klaus hasselmann 30/7/92.
c
c
c     author:
c     -------
c
c     susanne hasselmann, 1992
c     juergen waszkewitz, 1993
c
c     externals:
c     ----------
c
c     checkswellseppara -  check input parameters.
c     combinepeaks      -  combine peaks.
c     docombine         -  do the combining of two partitions to 
c                          one..
c     halfspread        -  combine peaks if distance between peaks 
c                          is less than half of spreads.
c     initswellsep      -  initialize arrays.
c     lasttwobins       -  combine peaks in last two bins with 
c                          closest peak.
c     lowenergy         -  combine partitionings with too low energy
c     means             -  compute mean angel and mean frequency.
c     onestepapart      -  combine peaks which are only one gtid 
c                          point apart.
c     partitioning      -  partition spectra.
c     sumenergy         -  compute energy and spread.
c     threshhold        -  combine peaks after thresshold check
c     windsea           -  windsea - swell separation.
c
c
c     subroutine tree:
c
c     swellsep
c       |
c       checkswellseppara
c       |
c       initswellsep
c       |
c       partitioning
c       |
c       combinepeaks
c       | |
c       | onestepapart
c       | |
c       | sumenergy
c       | |
c       | windsea
c       | | |
c       | | docombine
c       | |
c       | lasttwobins
c       | | |
c       | | docombine
c       | |
c       | halfspread
c       | | |
c       | | docombine
c       | |
c       | threshhold
c       | | |
c       | | docombine
c       | |
c       | lowenergy
c       |   |
c       |   docombine
c       |  
c       |
c       means
c
c------------------------------------------------------------------
c
      IMPLICIT NONE
c
c     interface:
c     ----------
c
      INTEGER MSPEC
c                      dimension of spectra.
      INTEGER NSPEC
c                      number of spectra to be partitioned
      INTEGER MPART
c                      dimension of parts
      INTEGER NPART(MSPEC)
c                      number of partitionings,
c                      where npart(ispec) is the number of 
c                      partitionings of spectrum ispec.
      INTEGER NANG
c                      number of spectral directions 
      INTEGER NFRE
c                      number of spectral frequencies
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c                      spectra
      INTEGER PART(MSPEC,NANG,NFRE)
c                      partitionings, where part(ispec,iang,ifre) is
c                      the number of the partitioning of the 
c                      spectrum ispec at direction iang and
c                      frequency ifre
      INTEGER PARTINFO(MSPEC,MPART)
c                      information about partitioning:
c                      0=swell , 3=old windsea, 2=mixed , 1=windsea
      DOUBLE PRECISION  LOWEST
c                      if hs is lower than lowest wave system is
c                      combined with closest system.
      DOUBLE PRECISION  MEANE(MSPEC,MPART)
c                      mean energies, where meane(ispec,ipart)
c                      is the energy of spectrum number ispec 
c                      partitioning ipart
      DOUBLE PRECISION  MEANANG(MSPEC,MPART)
c                      mean directions in radiance, like above
      DOUBLE PRECISION  MEANFRE(MSPEC,MPART)
c                      mean frequencies in hz, like above
      DOUBLE PRECISION  u10(mspec)
c                      u10, where u10(ispec) is u10
c                      of spectrum ispec
      DOUBLE PRECISION  THW(MSPEC)
c                      wind direction in degree
      DOUBLE PRECISION  FRE1
c                      lowest freqency
      DOUBLE PRECISION  CO
c                      ratio between two frequencies
c                      (co=peakfre(2)/peakfre(1))
      DOUBLE PRECISION  LEVEL
c                      the level for the threshhold check,
c                      see explanation of subroutine threshhold
      LOGICAL CONTROL
c                      standard output control messages on unit 6 ?
c                      .true. = yes , .false. = no
c
cn==
       INTEGER ISPEC, IPART
cn==       
c
c     parameter:
c     ----------
c
c                      array dimensions:
c                      dimspec >= mspec , dimpart >= mpart ,
c                      DIMANG >= NANG , DIMFRE >= NFRE
      INCLUDE "dimpar.par"
c
c
c     local variables:
c     ----------
c
      INTEGER EQUIPART( DIMSPEC , DIMANG*DIMFRE/2 )
c                      crossassigns side trails belonging to the 
c                      same main trail in the partitioning 
c                      technique. only used in subroutine partition.
      INTEGER PEAKANG( DIMSPEC , DIMANG*DIMFRE/2 )
c                      contains directional indeces of peaks.
      INTEGER PEAKFRE( DIMSPEC , DIMANG*DIMFRE/2 )
c                      contains frequency indeces of peaks.
c
      DOUBLE PRECISION  FX(DIMSPEC,DIMPART), FY(DIMSPEC,DIMPART)
c            mean wave numbers
c
      DOUBLE PRECISION  SPREAD( DIMSPEC , DIMPART )
c                      contains the squares of the spread.
      DOUBLE PRECISION  SUMX(DIMSPEC,DIMPART),SUMXX(DIMSPEC,DIMPART)
      DOUBLE PRECISION  SUMY(DIMSPEC,DIMPART),SUMYY(DIMSPEC,DIMPART)
c                      work space for summation while 
c                      computing meane and spread.
      DOUBLE PRECISION  SUM0( DIMSPEC , DIMPART ) ,
     &    SUMX0(DIMSPEC,DIMPART),SUMXX0(DIMSPEC,DIMPART),
     &    SUMY0(DIMSPEC,DIMPART),SUMYY0(DIMSPEC,DIMPART)
c                      work space only used in subroutine sumenergy.
      DOUBLE PRECISION  FRETAB( DIMFRE )
c                      frequency array.
      DOUBLE PRECISION  DFIM( DIMFRE )
c                      frequency increment/directional increment. 
      DOUBLE PRECISION  COSTAB( DIMANG ) , SINTAB( DIMANG )
c                      cosin and sin table
cn==
                integer  nn, cont
                DOUBLE PRECISION  MEANEAUX(MSPEC,MPART), 
     &                            MEANFREAUX(MSPEC,MPART),
     &                            MEANANGAUX(MSPEC,MPART)		
               INTEGER NPARTAUX(MSPEC), iang, ifre		
      INTEGER PARTAUX(MSPEC,NANG,NFRE), PARTINFOAUX(MSPEC,MPART)	       
      
cn==
c
c-------------------------------------------------------------------
c
      IF( CONTROL ) WRITE(6,*) 'CALL OF SUBROUTINE SWELLSEP'
cn      write(*,*)'U10(1,2)=',U10,'THW(1,2)=',THW
c
c     1. check input and parameter values.
c     ------------------------------------
c
      CALL CHECKSWELLSEPPARA( 
c                   dimensions to be checked
     &              DIMSPEC , MSPEC , DIMPART , MPART ,
     &              DIMANG , NANG , DIMFRE , NFRE )
c
c     2. initialization.
c     ------------------
c
      CALL INITSWELLSEP( 
c                  dimensions
     &               DIMANG , NANG , DIMFRE , NFRE ,
c                  input
     &               FRE1 , CO , 
c                  output
     &               FRETAB , COSTAB , SINTAB , DFIM )
c
c     3. partition spectra.
c     ---------------------
      CALL PARTITIONING( 
c                  dimensions
     &               DIMSPEC , MSPEC , NSPEC ,
     &               MPART , NPART , DIMANG , NANG , DIMFRE , NFRE,
c                  input
     &               SPEC , 
c                  output
     &               PART , EQUIPART , PEAKANG , PEAKFRE )
c
cn      write(*,*)'npart=',npart
c     4. combine peaks.
c     -----------------
c
      CALL COMBINEPEAKS(
c                  dimensions
     &               DIMSPEC , MSPEC , NSPEC ,
     &               DIMPART , MPART , NPART ,
     &               DIMANG , NANG , DIMFRE , NFRE ,
c                  input
     &               SPEC ,
c                  input and output 
     &               PART , PARTINFO , PEAKANG, PEAKFRE, FX, FY,
     &               LOWEST,MEANE , SPREAD , 
     &               MEANANG, MEANFRE ,
c                  work space
     &               SUMX , SUMY , 
     &               SUMXX , SUMYY ,
     &               SUM0 , SUMX0 , SUMY0 , SUMXX0 , SUMYY0 ,
c                  input of precomputed tables.
     &               U10 , THW , FRETAB , COSTAB , SINTAB , DFIM ,
     &               LEVEL , CONTROL )
c
c     5. compute integrated values hs,mean frequency,mean direction.
c     --------------------------------------------------------------
c
      CALL MEANS(
c                   dimensions
     &                DIMSPEC , MSPEC , NSPEC ,
     &                DIMPART , MPART , NPART ,
     &                DIMANG , NANG , DIMFRE , NFRE ,
c                   input
     &                SPEC , PART ,
c                   output
     &                MEANE , MEANANG , MEANFRE ,
c                   workspace
     &                SUM0 , SUMX0 , SUMY0 ,
c                   input of general parameters.
     &                FRETAB , COSTAB , SINTAB , DFIM )
CN
CN================
CN    
CN   i'm adding 2 extra tests
CN
CN   the first is an energy threshold test. 
CN   i'm removing (getting rid of) all partitions whose total energy is bellow a frequency dependent threshold level
CN   this energy level is
CN   30*10e-6/(fp^4+3*10e-3)
CN
CN   the second test is a high frequency cut off due to the buoy response
CN   i'm discarding everything beyond 0.3Hz (below 3.33s)
       nn=0
      DO ISPEC = 1,NSPEC
      
	cont=npart(ispec)
	
        DO IPART = 1,NPART(ISPEC)
     
	if(MEANE(ISPEC,IPART).gt.(20*10e-6/(meanfre(ISPEC,IPART)**4
     &                            +3*10e-3)).and.
     &   meanfre(ISPEC,IPART).lt.0.3) then
     
        nn=nn+1
        meaneaux(ispec,nn)=MEANE(ISPEC,IPART)
        meanfreaux(ispec,nn)=MEANFRE(ISPEC,IPART)
        meanangaux(ispec,nn)=MEANANG(ISPEC,IPART)
        partinfoaux(ispec,nn)=PARTINFO(ISPEC,IPART)
      
      DO IANG = 1,NANG
        DO IFRE = 1,NFRE
        partaux(ispec,iang,ifre)=PART(ISPEC,IANG,IFRE)
	END DO
      END DO        	

         else 
         cont=cont-1
	end if

	END DO
       npartaux(ispec)=cont
	nn=0
      END DO                     
CN
      DO ISPEC = 1,NSPEC

       NPART(ISPEC)=npartaux(ispec)
      
        DO IPART = 1,NPARTAUX(ISPEC)

	MEANE(ISPEC,IPART)=meaneaux(ispec,ipart)
	MEANFRE(ISPEC,IPART)=meanfreaux(ispec,ipart)
	MEANANG(ISPEC,IPART)=meanangaux(ispec,ipart)
	PARTINFO(ISPEC,IPART)=partinfoaux(ispec,ipart)
	
      DO IANG = 1,NANG
        DO IFRE = 1,NFRE
        PART(ISPEC,IANG,IFRE)=partaux(ispec,iang,ifre)
	END DO
      END DO 	
      
        END DO
      END DO	
      
CN
CN
CN================

      IF( CONTROL ) WRITE(6,*) 'ENDING SUBROUTINE SWELLSEP'

      RETURN

      END

C
C-------------------------------------------------------------------
C
      SUBROUTINE CHECKSWELLSEPPARA( 
c                  dimensions to be checked
     &                DIMSPEC , MSPEC , DIMPART , MPART ,
     &                DIMANG , NANG , DIMFRE , NFRE )
c
c-------------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c     check dimension parameters and input dimensions.
c
c-------------------------------------------------------------------
c     interface:
c     ----------
c
      IMPLICIT NONE
      INTEGER DIMSPEC, MSPEC, DIMPART, MPART,
     &        DIMANG, NANG, DIMFRE, NFRE
C
C     NO CHANGES
C
C
C     VARIABLES:
C     ----------
C
      LOGICAL ERROR
C
C-----------------------------------------------------------------------


      ERROR = .FALSE.
      IF( DIMSPEC.NE.MSPEC )THEN
        ERROR = .TRUE.
        WRITE(6,*) 'ERROR! SUBROUTINE SWELLSEP:'
        WRITE(6,*) 'PARAMETER DIMSPEC IS TOO SMALL!'
        WRITE(6,*) 'IT MUST BE DIMSPEC >= MSPEC = ',MSPEC,'!'
        WRITE(6,*) 'CHANGE PARAMETER DIMSPEC!'
      ENDIF
      IF( DIMPART.NE.MPART )THEN
        ERROR = .TRUE.
        WRITE(6,*) 'ERROR! SUBROUTINE SWELLSEP:'
        WRITE(6,*) 'PARAMETER DIMPART IS TOO SMALL!'
        WRITE(6,*) 'IT MUST BE DIMPART >= MPART = ',MPART,'!'
CN+++++++        
          WRITE(6,*)'DIMPART=',DIMPART, 'MPART =',MPART
CN+++++++        
        WRITE(6,*) 'CHANGE PARAMETER DIMPART!'
      ENDIF
      IF( DIMANG.NE.NANG )THEN
        ERROR = .TRUE.
        WRITE(6,*) 'ERROR! SUBROUTINE SWELLSEP:'
        WRITE(6,*) 'PARAMETER DIMANG IS TOO SMALL!'
        WRITE(6,*) 'IT MUST BE DIMANG >= NANG = ',NANG,'!'
        WRITE(6,*) 'CHANGE PARAMETER DIMANG!'
      ENDIF
      IF( DIMFRE.NE.NFRE )THEN
        ERROR = .TRUE.
        WRITE(6,*) 'ERROR! SUBROUTINE SWELLSEP:'
        WRITE(6,*) 'PARAMETER DIMFRE IS TOO SMALL!'
        WRITE(6,*) 'IT MUST BE DIMFRE >= NFRE = ',NFRE,'!'
        WRITE(6,*) 'CHANGE PARAMETER DIMFRE!'
      ENDIF
      IF( ERROR )THEN
        STOP 'ERROR IN SUBROUTINE SWELLSEP!'
      ENDIF

      RETURN

      END
c
c-------------------------------------------------------------------
c
      SUBROUTINE COMBINEPEAKS(
c                  dimensions
     &               DIMSPEC , MSPEC , NSPEC ,
     &               DIMPART , MPART , NPART ,
     &               DIMANG , NANG , DIMFRE , NFRE ,
c                  input
     &               SPEC ,
c                  input and output
     &               PART , PARTINFO , PEAKANG , PEAKFRE , FX, FY,
     &               LOWEST,MEANE , SPREAD ,  
     &               MEANANG, MEANFRE ,
c                  work space
     &               SUMX , SUMY ,SUMXX , SUMYY ,
     &               SUM0 , SUMX0 , SUMY0 , SUMXX0 , SUMYY0 ,
c                  input of general parameters.
     &               U10 , THW , FRETAB , COSTAB , SINTAB , DFIM , 
     &               LEVEL , CONTROL )
c
c-------------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c     combine partitionings if
c     - the peaks are only one grid point apart 
c         (subroutine onestepapart)
c     - the peak lies in last two frequency bins
c         (subroutine lasttwobins)
c     - the distance between peaks is less than half the spread of the
c       partitioning (subroutine halfspread)
c     - the minimum energy between peaks is higher than level * minimum
c       peak energy (subroutine threshhold)
c     all windsea peaks are combined to one.
c
c---------------------------------------------------------------------
      IMPLICIT NONE
c
c     interface:
c     ----------
c
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMPART, MPART, NPART(MSPEC),
     &  DIMANG, NANG, DIMFRE, NFRE
c          array dimensions.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c          2d input spectra to be partitioned.
      INTEGER PART(MSPEC,NANG,NFRE),
     &  PARTINFO(MSPEC,MPART),
     &  PEAKANG(DIMSPEC,DIMANG*DIMFRE/2),
     &  PEAKFRE(DIMSPEC,DIMANG*DIMFRE/2)
c          part(..) gives number of partitioning for each spectral bin.
c          partinfo =1 -> wind sea, =2 -> mixed wind sea-swell,
c                   =0 -> swell, , 3=old windsea
c                  index of peak direction and peak frequency of 
c                  partitionings.
      DOUBLE PRECISION  LOWEST
c                  wave system of wave height less than lowest is 
c                  combined with next system.
      DOUBLE PRECISION  FX(DIMSPEC,DIMPART), FY(DIMSPEC,DIMPART),
     &  MEANE(MSPEC,MPART),
     &  SPREAD(DIMSPEC,DIMPART),
c          mean wave numbers, mean energy and spread of partitionings.
     &  SUMX(DIMSPEC,DIMPART), SUMY(DIMSPEC,DIMPART),
     &  SUMXX(DIMSPEC,DIMPART), SUMYY(DIMSPEC,DIMPART)
c          work space.
      DOUBLE PRECISION  SUM0(DIMSPEC,DIMPART),
     &  SUMX0(DIMSPEC,DIMPART),SUMXX0(DIMSPEC,DIMPART),
     &  SUMY0(DIMSPEC,DIMPART),SUMYY0(DIMSPEC,DIMPART)
c          for temporary storage.
      DOUBLE PRECISION  U10(MSPEC), THW(MSPEC),
     &  FRETAB(DIMFRE), COSTAB(DIMANG), SINTAB(DIMANG),
     &  DFIM(DIMFRE)
c          u10, wind direction,frequencies,cos and sin tables 
c          frequ./directional increment.
      DOUBLE PRECISION  LEVEL
c          combine systems if minimum energy between peaks 
c          is higher than 
c          level * minimum peak energy (subroutine threshhold)
       
      DOUBLE PRECISION  MEANANG(MSPEC,MPART)
c                      mean directions in radiance, like above
      DOUBLE PRECISION  MEANFRE(MSPEC,MPART)
c                      mean frequencies in hz, like above
c
      INTEGER ISPEC,IPART
      LOGICAL CONTROL
c          controls print output.
c
c-----------------------------------------------------------------------
cn==
      DOUBLE PRECISION SPREADaux(50,65)
           common /spr/ spreadaux
cn==
c
c     1. combine partitionings if peaks are only one grid point apart 
c        the peak lies in last two frequency bins.
c     -----------------------------------------------------------------
c
      CALL ONESTEPAPART( 
c               dimensions
     &            DIMSPEC , MSPEC , NSPEC ,
     &            MPART , NPART , DIMANG , NANG , DIMFRE , NFRE ,
c               input/output
     &            SPEC , PART , PEAKANG , PEAKFRE )
c
c
c     2. initialize arrays fx and fy
c     -----------------------------------

      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          FX(ISPEC,IPART) = FRETAB(PEAKFRE(ISPEC,IPART))
     &        * COSTAB(PEAKANG(ISPEC,IPART))    
          FY(ISPEC,IPART) = FRETAB(PEAKFRE(ISPEC,IPART))
     &        * SINTAB(PEAKANG(ISPEC,IPART))    
        END DO
      END DO
c
c     3. compute mean energy of partitionings.
c     ----------------------------------------
c
cn	 write(*,*)'npart=',npart(1),'mspec=',mspec,'ispec=',ispec
	 CALL SUMENERGY( 
c               dimensions
     &            DIMSPEC , MSPEC , NSPEC ,
     &            DIMPART , MPART , NPART ,
     &            DIMANG , NANG , DIMFRE , NFRE ,
c               input
     &            SPEC , PART ,
c               output
     &            MEANE , SPREAD , SUMX , SUMY , SUMXX , SUMYY ,
c               work space
     &            SUM0 , SUMX0 , SUMY0 , SUMXX0 , SUMYY0 ,
c               precomputed tables for frequencies, cos,sin,
c               frequ.increment.
     &            FRETAB , COSTAB , SINTAB , DFIM )
c
      CALL MEANS(
c                   dimensions
     &                DIMSPEC , MSPEC , NSPEC ,
     &                DIMPART , MPART , NPART ,
     &                DIMANG , NANG , DIMFRE , NFRE ,
c                   input
     &                SPEC , PART ,
c                   output
     &                MEANE , MEANANG, MEANFRE ,
c                   workspace
     &                SUM0 , SUMX0 , SUMY0 ,
c                   input of general parameters.
     &                FRETAB , COSTAB , SINTAB , DFIM )
c
c     4. all windsea peaks are combined to one.
c     -----------------------------------------
c
      CALL WINDSEA( 
c               dimensions
     &            DIMSPEC , MSPEC , NSPEC ,
     &            DIMPART , MPART , NPART ,
     &            DIMANG , NANG , DIMFRE , NFRE ,
c               input/output
     &            SPEC , PART , PARTINFO , PEAKANG , PEAKFRE , FX, FY,
     &            MEANE ,  MEANANG, MEANFRE ,
     &            SPREAD , SUMX , SUMY , SUMXX , SUMYY ,
     &            U10 , THW , FRETAB , COSTAB , SINTAB , CONTROL )
c
c     5. combine if the peak lies in last two frequency bins.
c     -------------------------------------------------------
c
      CALL LASTTWOBINS( 
c                dimensions
     &             DIMSPEC , MSPEC , NSPEC ,
     &             DIMPART , MPART , NPART ,
     &             DIMANG , NANG , DIMFRE , NFRE ,
c                input/output
     &             SPEC , PART , PARTINFO , PEAKANG , PEAKFRE , FX, FY,
     &             MEANE , SPREAD , SUMX , SUMY , SUMXX , SUMYY ,
     &             FRETAB , CONTROL )
c
c     6. combine if distance between peaks is less than half 
c         the spread of the partitionings. 
c     ---------------------------------------------------------
c
      CALL HALFSPREAD( 
c                 dimensions
     &              DIMSPEC , MSPEC , NSPEC ,
     &              DIMPART , MPART , NPART ,
     &              DIMANG , NANG , DIMFRE , NFRE ,
c                 input/output
     &              SPEC , PART , PARTINFO , PEAKANG , PEAKFRE , FX, FY,
     &              MEANE , SPREAD , 
c                 work space
     &             SUMX , SUMY , SUMXX , SUMYY ,
c                 precomputed tables for frequencies.
     &              FRETAB , CONTROL )
c
c     7. combine if minimum energy between peaks is higher
c        than level * minimum peak energy.
c     -----------------------------------------------------
c
      CALL THRESHHOLD( 
c                 dimensions
     &              DIMSPEC , MSPEC , NSPEC ,
     &              DIMPART , MPART , NPART ,
     &              DIMANG , NANG , DIMFRE , NFRE ,
c                 input/output
     &              SPEC , PART , PARTINFO , PEAKANG , PEAKFRE , FX, FY,
     &              MEANE , SPREAD , SUMX , SUMY , SUMXX , SUMYY , 
c                 precomputed tables for frequencies,threshhold level..
     &              FRETAB , LEVEL , CONTROL )
c
c     6. low energy partitionings are combined with closest partitioning
c     ------------------------------------------------------------------
c
      CALL LOWENERGY( 
c                 dimensions.
     &              DIMSPEC , MSPEC , NSPEC ,
     &              DIMPART , MPART , NPART ,
     &              DIMANG , NANG , DIMFRE , NFRE ,
c                 input/output
     &              SPEC , PART , PARTINFO , PEAKANG , PEAKFRE , FX, FY,
     &              LOWEST, MEANE, SPREAD ,
c                 work space
     &              SUMX , SUMY , SUMXX , SUMYY,
c                 precomputed tables for frequencies.
     &              FRETAB , CONTROL )


      RETURN

      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE DOCOMBINE( 
c                 dimensions
     &              IPART , JPART , ISPEC ,
     &              DIMSPEC , MSPEC , NSPEC ,
     &              DIMPART , MPART , NPART ,
     &              DIMANG , NANG , DIMFRE , NFRE ,
c                 input/output
     &              SPEC , PART , PARTINFO , PEAKANG , PEAKFRE , FX, FY,
     &              MEANE , SPREAD , SUMX , SUMY , SUMXX , SUMYY ,
c                 precomputed tables for frequencies.
     &              FRETAB , CONTROL )
c
c-----------------------------------------------------------------------
c
c
c
c     purpose:
c     --------
c
c     combine partitions ipart and jpart of spectra ispec
c     (the part-index of the combined peak is min(ipart,jpart),
c     the part-index npart(ispec) is changed to max(ipart,jpart))
c
c----------------------------------------------------------------------
c
      IMPLICIT NONE 
c
c     interface:
c     ----------
c
      INTEGER IPART, JPART, ISPEC
c                  loop indexes.
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMPART, MPART, NPART(MSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
c                  dimensions.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c                  2d spectrua.
      INTEGER PART(MSPEC,NANG,NFRE),
     &        PARTINFO(MSPEC,MPART),
     &        PEAKANG(DIMSPEC,DIMANG*DIMFRE/2),
     &        PEAKFRE(DIMSPEC,DIMANG*DIMFRE/2)
c     part(..) gives number of partitioning for each spectral bin.
c     partinfo =1 -> wind sea, =2 -> mixed wind sea-swell, =0 -> swell.
c      , 3=old windsea
c     index of peak direction and peak frequency of partitionings.
cn      DOUBLE PRECISION SPREAD(50,65)
      DOUBLE PRECISION  FX(DIMSPEC,DIMPART), FY(DIMSPEC,DIMPART),
     &     MEANE(MSPEC,MPART),
     &     SPREAD(DIMSPEC,DIMPART),
c                  mean wave numbers, mean energy and 
c                  spread of partitionings.
     &     SUMX(DIMSPEC,DIMPART), SUMY(DIMSPEC,DIMPART),
     &     SUMXX(DIMSPEC,DIMPART), SUMYY(DIMSPEC,DIMPART)
c                  work space.
      DOUBLE PRECISION  FRETAB(DIMFRE)
c                  table of frequencies.
      LOGICAL CONTROL
C
c     local variables:
      INTEGER LPART, HPART, IANG, IFRE
c                  loop indexes.
c
cn==
      DOUBLE PRECISION SPREADaux(50,65)
           common /spr/ spreadaux
cn==
c-----------------------------------------------------------------------
c
      IF( IPART.EQ.JPART ) RETURN

      IF( CONTROL )THEN
        WRITE(6,*) ' COMBINING IN SPECTRA NUMBER ',ISPEC,' THE PEAKS'
        WRITE(6,'(''  FREQUENCY='',E8.2,'' ANGEL='',I3)')
     &      FRETAB(PEAKFRE(ISPEC,IPART)),
     &      NINT((PEAKANG(ISPEC,IPART)-1.)/NANG*360.)
        WRITE(6,'(''  FREQUENCY='',E8.2,'' ANGEL='',I3)')
     &      FRETAB(PEAKFRE(ISPEC,JPART)),
     &      NINT((PEAKANG(ISPEC,JPART)-1.)/NANG*360.)
      END IF

      LPART = MIN(IPART,JPART)
      HPART = MAX(IPART,JPART)
c
c     change hpart to lpart and npart(ispec) to hpart
c     -----------------------------------------------

      DO IANG = 1,NANG
        DO IFRE = 1,NFRE
          IF( PART(ISPEC,IANG,IFRE).EQ.HPART )THEN
            PART(ISPEC,IANG,IFRE) =LPART
          ELSE IF( PART(ISPEC,IANG,IFRE).EQ.NPART(ISPEC) )THEN
            PART(ISPEC,IANG,IFRE) = HPART
          END IF
        END DO
      END DO
c
      IF( SPEC(ISPEC,PEAKANG(ISPEC,HPART),PEAKFRE(ISPEC,HPART)).GT.
     &    SPEC(ISPEC,PEAKANG(ISPEC,LPART),PEAKFRE(ISPEC,LPART)) )THEN
        PEAKANG(ISPEC,LPART) = PEAKANG(ISPEC,HPART)
        PEAKFRE(ISPEC,LPART) = PEAKFRE(ISPEC,HPART)
        FX(ISPEC,LPART) = FX(ISPEC,HPART)
        FY(ISPEC,LPART) = FY(ISPEC,HPART)
      ENDIF
      PEAKANG(ISPEC,HPART) = PEAKANG(ISPEC,NPART(ISPEC))
      PEAKFRE(ISPEC,HPART) = PEAKFRE(ISPEC,NPART(ISPEC))
      FX(ISPEC,HPART) = FX(ISPEC,NPART(ISPEC))
      FY(ISPEC,HPART) = FY(ISPEC,NPART(ISPEC))

      IF(MEANE(ISPEC,HPART).GT.MEANE(ISPEC,LPART)) 
     &  PARTINFO(ISPEC,LPART)=PARTINFO(ISPEC,HPART)
      PARTINFO(ISPEC,HPART) = PARTINFO(ISPEC,NPART(ISPEC))

      MEANE(ISPEC,LPART) 
     &  = MEANE(ISPEC,LPART) + MEANE(ISPEC,HPART)
      MEANE(ISPEC,HPART) = MEANE(ISPEC,NPART(ISPEC))

      SUMX(ISPEC,LPART) = SUMX(ISPEC,LPART) + SUMX(ISPEC,HPART)
      SUMX(ISPEC,HPART) = SUMX(ISPEC,NPART(ISPEC))
      SUMY(ISPEC,LPART) = SUMY(ISPEC,LPART) + SUMY(ISPEC,HPART)
      SUMY(ISPEC,HPART) = SUMY(ISPEC,NPART(ISPEC))
      SUMXX(ISPEC,LPART) = SUMXX(ISPEC,LPART) + SUMXX(ISPEC,HPART)
      SUMXX(ISPEC,HPART) = SUMXX(ISPEC,NPART(ISPEC))
      SPREAD(ISPEC,LPART) = MAX
cn      SPREADaux(ISPEC,LPART) = MAX
     &    ( SUMXX(ISPEC,LPART)/MEANE(ISPEC,LPART)
     &    + SUMYY(ISPEC,LPART)/MEANE(ISPEC,LPART)
     &    - (SUMX(ISPEC,LPART)/MEANE(ISPEC,LPART))**2
     &    - (SUMY(ISPEC,LPART)/MEANE(ISPEC,LPART))**2
     &    , 0.D0)
      SPREAD(ISPEC,HPART) = SPREAD(ISPEC,NPART(ISPEC))
cn      SPREADaux(ISPEC,HPART) = SPREADaux(ISPEC,NPART(ISPEC))

      NPART(ISPEC) = NPART(ISPEC) - 1
c
      RETURN
c
      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE HALFSPREAD( 
c                  dimensions
     &               DIMSPEC , MSPEC , NSPEC ,
     &               DIMPART , MPART , NPART ,
     &               DIMANG , NANG , DIMFRE , NFRE ,
c                  input/output
     &               SPEC,PART,PARTINFO,PEAKANG,PEAKFRE ,FX,FY,
     &               MEANE , SPREAD ,
c                  work space
     &               SUMX , SUMY , SUMXX , SUMYY ,
c                  frequ. table
     &               FRETAB , CONTROL )
c
c-----------------------------------------------------------------------
c
c     purpose:
c     --------
c
c     combine peaks if distance between them is less than half 
c     their spread. 
c
c
c     exernals:
c     ---------
c
c     docombine - to do the combining of two partitions to one
c
c
c-----------------------------------------------------------------------
c
      IMPLICIT NONE
c     interface:
c     ----------
c
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMPART, MPART, NPART(MSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
c                  array dimensions.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c                  2d spectra.
      INTEGER PART(MSPEC,NANG,NFRE),
     &        PARTINFO(MSPEC,MPART),
     &        PEAKANG(DIMSPEC,DIMANG*DIMFRE/2),
     &        PEAKFRE(DIMSPEC,DIMANG*DIMFRE/2)
c     part(..) gives number of partitioning for each spectral bin.
c     partinfo =1 -> wind sea, =2 -> mixed wind sea-swell, =0 -> swell
c      , 3=old windsea.
c      index of peak direction and peak frequency of partitionings.
cn      DOUBLE PRECISION SPREAD(50,65)
      DOUBLE PRECISION  FX(DIMSPEC,DIMPART), FY(DIMSPEC,DIMPART),
     &     MEANE(MSPEC,MPART),
     &     SPREAD(DIMSPEC,DIMPART),
c                  mean wave numbers, mean energy and 
c                  spread of partitionings.
     &     SUMX(DIMSPEC,DIMPART), SUMY(DIMSPEC,DIMPART),
     &     SUMXX(DIMSPEC,DIMPART), SUMYY(DIMSPEC,DIMPART)
c                  work space.
      DOUBLE PRECISION  FRETAB(DIMFRE)
c                  table of frequencies.
      LOGICAL CONTROL
c
cn==
      DOUBLE PRECISION SPREADaux(50,65)
           common /spr/ spreadaux
cn==
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IPART, JPART
c                  loop indexes.
c
c-----------------------------------------------------------------------
c
      DO ISPEC = 1,NSPEC
        IPART = 1
        DO WHILE(IPART.LE.NPART(ISPEC)-1.AND.
     &                                  PARTINFO(ISPEC,IPART).EQ.0)
          JPART  = IPART + 1
          DO WHILE( IPART.NE.0 .AND. JPART.LE.NPART(ISPEC).AND.
     &                                  PARTINFO(ISPEC,JPART).EQ.0)
            IF( (FX(ISPEC,IPART)-FX(ISPEC,JPART))**2
     &          +(FY(ISPEC,IPART)-FY(ISPEC,JPART))**2
     &          .LT. 0.5*MIN(SPREAD(ISPEC,IPART),SPREAD(ISPEC,JPART))
cn     &      .LT. 0.5*MIN(SPREADaux(ISPEC,IPART),SPREADaux(ISPEC,JPART))
     &          )THEN
              CALL DOCOMBINE( 
c                     dimensions
     &                  IPART , JPART , ISPEC ,
     &                  DIMSPEC , MSPEC , NSPEC ,
     &                  DIMPART , MPART , NPART ,
     &                  DIMANG , NANG , DIMFRE , NFRE ,
c                     input/output
     &                  SPEC , PART , PARTINFO ,
     &                  PEAKANG , PEAKFRE , FX, FY,
     &                  MEANE , SPREAD , SUMX , SUMY , SUMXX , SUMYY ,
     &                  FRETAB , CONTROL )
              IF( CONTROL ) WRITE(6,*) ' REASON: ',
     &            'DISTANCE IS LESS THAN HALF OF MINIMAL SPREAD'
              IPART = 0
            ELSE
              JPART = JPART + 1
            END IF
          END DO
          IPART = IPART + 1
        END DO
      END DO
c
      RETURN
c
      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE INITSWELLSEP(
c                 dimensions
     &              DIMANG , NANG , DIMFRE , NFRE ,
c                 input
     &              FRE1 , CO , 
c                 output
     &              FRETAB , COSTAB , SINTAB , DFIM )
c
c-----------------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c     initialize arrays 
c
c 
c-----------------------------------------------------------------------
      IMPLICIT NONE
c     interface:
c     ----------
c
      INTEGER DIMANG, NANG, DIMFRE, NFRE
c               array dimensions.
      DOUBLE PRECISION  FRE1, CO
c               first frequency, fr(i)/fr(i+1)
      DOUBLE PRECISION  FRETAB(DIMFRE),COSTAB(DIMANG),SINTAB(DIMANG),
     &     DFIM( DIMFRE )
c                  table of frequencies,cos,sin,frequ. 
c                  increment/directional incr.
c     local  variable:
c     ----------------
c
      INTEGER IFRE, IANG
c                   loop indexes.
      DOUBLE PRECISION  PI
C
C-----------------------------------------------------------------------
c
      PI = 3.141592653589793
      FRETAB(1) = FRE1
      DFIM(1) = (CO-1) * PI / NANG * FRETAB(1)
      DO IFRE=2,NFRE-1
        FRETAB(IFRE) = FRETAB(IFRE-1) * CO
        DFIM(IFRE) = (CO-1) * PI / NANG * (FRETAB(IFRE)+FRETAB(IFRE-1))
cn      write(*,*)'DFIM(IFRE) = ',DFIM(IFRE)
      END DO
      FRETAB(NFRE) = FRETAB(NFRE-1)*CO
      DFIM(NFRE) = (CO-1) * PI / NANG * FRETAB(NFRE-1)
cn     write(*,*)'DFIM(NFRE) = ',DFIM(NFRE)
      DO IANG=1 , NANG
        COSTAB(IANG) = COS( 2*PI*(IANG-1)/NANG )
	write(*,*)'COSTAB(IANG) =',COSTAB(IANG)
        SINTAB(IANG) = SIN( 2*PI*(IANG-1)/NANG )
	write(*,*)'SINTAB(IANG) = ',SINTAB(IANG)
      END DO
 
      RETURN

      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE LASTTWOBINS(
c                  dimensions
     &               DIMSPEC , MSPEC , NSPEC ,
     &               DIMPART , MPART , NPART ,
     &               DIMANG , NANG , DIMFRE , NFRE ,
c                  input/output
     &               SPEC , PART , PARTINFO , PEAKANG , PEAKFRE ,FX,FY,
     &               MEANE, SPREAD ,
c                  work space
     &               SUMX , SUMY , SUMXX , SUMYY ,
c                  freq table.
     &               FRETAB , CONTROL )
c
c-----------------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c     if peak lies in last two frequency bins and is not windsea,
c     combine with nearest not windsea peak
c
c
c     exernals:
c     ---------
c
c     docombine - to do the combining of two partitions to one
c
c
c-----------------------------------------------------------------------
      IMPLICIT NONE
c     interface:
c     ----------
c
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMPART, MPART, NPART(MSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
c                  array dimensions.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c                  2d spectra.
      INTEGER PART(MSPEC,NANG,NFRE),
     &        PARTINFO(MSPEC,MPART),
     &        PEAKANG(DIMSPEC,DIMANG*DIMFRE/2),
     &        peakfre(dimspec,dimang*dimfre/2)
c      part(..) gives number of partitioning for each spectral bin.
c      partinfo =1 -> wind sea, =2 -> mixed wind sea-swell, =0 -> swell
c       , 3=old windsea.
c      index of peak direction and peak frequency of partitionings.
cn      DOUBLE PRECISION SPREAD(50,65)
      DOUBLE PRECISION  FX(DIMSPEC,DIMPART), FY(DIMSPEC,DIMPART),
     &     MEANE(MSPEC,MPART),
     &     SPREAD(DIMSPEC,DIMPART),
c                  mean wave numbers, mean energy and 
c                  spread of partitionings.
     &     SUMX(DIMSPEC,DIMPART), SUMY(DIMSPEC,DIMPART),
     &     SUMXX(DIMSPEC,DIMPART), SUMYY(DIMSPEC,DIMPART)
c                  work space.
      DOUBLE PRECISION  FRETAB(DIMFRE)
c                  table of frequencies.
      LOGICAL CONTROL
c
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IPART, JPART, KPART, KANG, KFRE
c                   loop indexes.
      DOUBLE PRECISION  F0, FX0, FY0
c                   work space.
      DOUBLE PRECISION  DIST, DIST0
c                   squares of distances
c
c-----------------------------------------------------------------------
c
c     1. find nearest neighbour.
c     ---------------------------
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          KPART = -1
          DO WHILE( PEAKFRE(ISPEC,IPART).GT.NFRE-2
     &        .AND. PARTINFO(ISPEC,IPART).EQ.0
     &        .AND. IPART.LE.NPART(ISPEC) .AND. KPART.NE.0 )
c           combine with nearest not windsea peak
c           first: find nearest not windsea peak to ipeak
            KPART = 0
            DIST = 0
            DO JPART = 1,NPART(ISPEC)
              IF( JPART.NE.IPART .AND. PARTINFO(ISPEC,JPART).EQ.0 
     &            .AND. PEAKFRE(ISPEC,JPART).LE.NFRE-2 )THEN
                DIST0 = (FX(ISPEC,IPART)-FX(ISPEC,JPART))**2
     &              + (FY(ISPEC,IPART)-FY(ISPEC,JPART))**2
                IF( KPART.EQ.0 .OR. DIST0.LT.DIST )THEN
                  KPART = JPART
                  DIST = DIST0
                END IF
              END IF
            END DO

c
c      2. combine wave systems.
c      ------------------------
c
            IF( KPART.NE.0 )THEN
              KANG = PEAKANG(ISPEC,KPART)
              KFRE = PEAKFRE(ISPEC,KPART)
              F0 = FRETAB(PEAKFRE(ISPEC,IPART))
              FX0 = FX(ISPEC,KPART)
              FY0 = FY(ISPEC,KPART)
              CALL DOCOMBINE( IPART , KPART , ISPEC ,
     &            DIMSPEC , MSPEC , NSPEC ,
     &            DIMPART , MPART , NPART ,
     &            DIMANG , NANG , DIMFRE , NFRE ,
     &            SPEC , PART , PARTINFO ,
     &            PEAKANG , PEAKFRE , FX, FY,
     &            MEANE , SPREAD , SUMX , SUMY , SUMXX , SUMYY ,
     &            FRETAB , CONTROL )
              IF( CONTROL) WRITE(6,*) ' REASON: FREQUENCY ',F0,
     &            ' IS IN LAST TWO FREQUENCY BINS'
c             the peak in the last two bins is unbelievable, so the combined
c             part is said to have the peak where the other part has its peak
c             (the part-index of the combined peak is min(ipart,kpart))
              PEAKANG(ISPEC,MIN(IPART,KPART)) = KANG
              PEAKFRE(ISPEC,MIN(IPART,KPART)) = KFRE
              FX(ISPEC,MIN(IPART,KPART)) = FX0
              FY(ISPEC,MIN(IPART,KPART)) = FY0
            END IF
          END DO
        END DO
      END DO
c
      RETURN
c
      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE LOWENERGY( 
c                 dimensions
     &              DIMSPEC , MSPEC , NSPEC ,
     &              DIMPART , MPART , NPART ,
     &              DIMANG , NANG , DIMFRE , NFRE ,
c                 input/output
     &              SPEC , PART , PARTINFO , PEAKANG , PEAKFRE , FX, FY,
     &              LOWEST, MEANE, SPREAD , 
c                 work space.
     &              SUMX , SUMY , SUMXX , SUMYY ,
c                 input table
     &              FRETAB , CONTROL )
c
c---------------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c     if mean energy of partitioning is < lowest
c     combine with nearest not windsea peak
c
c
c     exernals:
c     ---------
c
c     docombine - combines two partitionings.
c
c
c---------------------------------------------------------------------
      IMPLICIT NONE
c     interface:
c     ----------
c
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMPART, MPART, NPART(MSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
c                  array dimensions.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c                  2d spectra.
      INTEGER PART(MSPEC,NANG,NFRE),
     &        PARTINFO(MSPEC,MPART),
     &        PEAKANG(DIMSPEC,DIMANG*DIMFRE/2),
     &        PEAKFRE(DIMSPEC,DIMANG*DIMFRE/2)
c       part(..) gives number of partitioning for each spectral bin.
c       partinfo =1 -> wind sea, =2 -> mixed wind sea-swell =0 -> swell
c       , 3=old windsea.
c       index of peak direction and peak frequency of partitionings.
cn      DOUBLE PRECISION SPREAD(50,65)
      DOUBLE PRECISION  FX(DIMSPEC,DIMPART), FY(DIMSPEC,DIMPART),
     &     MEANE(MSPEC,MPART),
     &     SPREAD(DIMSPEC,DIMPART),
c             mean wave numbers, mean energy and spread of partitionings.
     &     SUMX(DIMSPEC,DIMPART), SUMY(DIMSPEC,DIMPART),
     &     SUMXX(DIMSPEC,DIMPART), SUMYY(DIMSPEC,DIMPART)
c                  work space.
      DOUBLE PRECISION  FRETAB(DIMFRE)
c                  table of frequencies.
      LOGICAL CONTROL
c
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IPART, JPART, KPART
c                   loop indexes.
      DOUBLE PRECISION  DIST, DIST0
c                   for squares of distances
      DOUBLE PRECISION  LOWEST
c                   the lowest wave height which is not combined
c
c-----------------------------------------------------------------------
c
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          KPART = -1
          DO WHILE( MEANE(ISPEC,IPART).LT.(LOWEST/4)**2
     &        .AND. PARTINFO(ISPEC,IPART).EQ.0
     &        .AND. IPART.LE.NPART(ISPEC) .AND. KPART.NE.0 )
c           combine with nearest not windsea peak
c           first: find nearest not windsea peak to ipeak
            KPART = 0
            DIST = 100.
            DO JPART = 1,NPART(ISPEC)
               IF( JPART.NE.IPART)THEN
                DIST0 = (FX(ISPEC,IPART)-FX(ISPEC,JPART))**2
     &              + (FY(ISPEC,IPART)-FY(ISPEC,JPART))**2
                IF( KPART.EQ.0 .OR. DIST0.LT.DIST )THEN
                  KPART = JPART
                  DIST = DIST0
                END IF
              END IF
            END DO
c           second: combine 
            IF( KPART.NE.0 )THEN
              CALL DOCOMBINE( 
c                    dimensions
     &                 IPART , KPART , ISPEC ,
     &                 DIMSPEC , MSPEC , NSPEC ,
     &                 DIMPART , MPART , NPART ,
     &                 DIMANG , NANG , DIMFRE , NFRE ,
c                    input/output
     &                 SPEC , PART , PARTINFO ,
     &                 PEAKANG , PEAKFRE , FX, FY,
     &                 MEANE , SPREAD , 
c                    work space 
     &                 SUMX , SUMY , SUMXX , SUMYY ,
c                    input table
     &                 FRETAB , CONTROL )
              IF( CONTROL) WRITE(6,*) ' REASON: MEAN ENERGY ',
     &            MEANE(ISPEC,IPART),' IS LOWER THAN ',(LOWEST/4)**2
            END IF
          END DO
        END DO
      END DO
c
      RETURN
c
      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE MEANS(
c                   dimensions
     &                DIMSPEC , MSPEC , NSPEC ,
     &                DIMPART , MPART , NPART ,
     &                DIMANG , NANG , DIMFRE , NFRE ,
c                   input
     &                SPEC , PART ,
c                   output
     &                MEANE , MEANANG , MEANFRE ,
c                   work space.
     &                SUM0 , SUMX0 , SUMY0 ,
c                   input tables
     &                FRETAB , COSTAB , SINTAB , DFIM )
c
c-----------------------------------------------------------------------
c
C
C     PURPOSE:
C     --------
C
C     COMPUTES MEAN DIRECTION AND MEAN FREQUENCYOF 2D SPECTRA.
C
c-----------------------------------------------------------------------
c
      IMPLICIT NONE
c     interface:
c     ----------
c
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMPART, MPART, NPART(MSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
c                 array dimensions.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c                 2d spectra.
      INTEGER PART(MSPEC,NANG,NFRE)
c          part(..) gives number of partitioning for each spectral bin.
      DOUBLE PRECISION  MEANE(MSPEC,MPART),
     &     MEANANG(MSPEC,MPART), MEANFRE(MSPEC,MPART)
c                 integrated values of partitionings.
      DOUBLE PRECISION  SUM0(DIMSPEC,DIMPART),
     &     SUMX0(DIMSPEC,DIMPART),SUMY0(DIMSPEC,DIMPART)
c                 for temporary sums
      DOUBLE PRECISION  FRETAB(DIMFRE),COSTAB(DIMANG),SINTAB(DIMANG),
     &     DFIM(DIMFRE)
c                  table of frequencies,cos,sin,freq.increment/directional 
c                  increment.
c
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IPART, IANG, IFRE
c                   loop indexes.
      DOUBLE PRECISION  PI, FACTOR
c
c-----------------------------------------------------------------------
c
      PI = 3.141592653589793D0
c
c     1. compute mean directions.
c     --------------------------

      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          SUMX0(ISPEC,IPART) = 0
          SUMY0(ISPEC,IPART) = 0
        END DO
      END DO

      DO IANG = 1,NANG
        DO ISPEC = 1,NSPEC
          DO IPART = 1,NPART(ISPEC)
            SUM0(ISPEC,IPART) = 0
          END DO
        END DO
        DO IFRE=1,NFRE
C
          DO ISPEC=1,NSPEC
            SUM0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          = SUM0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          + SPEC(ISPEC,IANG,IFRE) * DFIM(IFRE)
cn      write(*,*)'spec*dfim =',SPEC(ISPEC,IANG,IFRE) * DFIM(IFRE)
c        write(*,*)'dfim =',IFRE ,DFIM(IFRE)
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
          MEANANG(ISPEC,IPART)
     &        = ATAN2(SUMY0(ISPEC,IPART),SUMX0(ISPEC,IPART))
        END DO
      END DO
c
c----------------------------------------------------------------------
c
c    2. compute mean frequency.
c    --------------------------
c        
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          MEANFRE(ISPEC,IPART) = 0.1D-180
        END DO
      END DO

      DO IFRE = 1,NFRE
        DO ISPEC = 1,NSPEC
          DO IPART = 1,NPART(ISPEC)
            SUM0(ISPEC,IPART) = 0
          END DO
        END DO
        DO IANG = 1,NANG
C
          DO ISPEC = 1,NSPEC
            SUM0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          = SUM0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          + SPEC(ISPEC,IANG,IFRE)
          END DO
        END DO
        FACTOR = DFIM(IFRE) / FRETAB(IFRE)
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
          MEANFRE(ISPEC,IPART)
     &        = MEANE(ISPEC,IPART) / MEANFRE(ISPEC,IPART)
        END DO
      END DO
c
      RETURN
c
      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE ONESTEPAPART(
c                  dimensions
     &               DIMSPEC , MSPEC , NSPEC ,
     &               MPART , NPART , DIMANG , NANG , DIMFRE , NFRE ,
c                  input/output
     &               SPEC , PART , PEAKANG , PEAKFRE )
c
c-----------------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c     combine peaks which are only one index apart
c
c
c
c-----------------------------------------------------------------------
      IMPLICIT NONE
c     interface:
c     ----------
c     
      INTEGER DIMSPEC, MSPEC, NSPEC, MPART, NPART(MSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
c                  dimensions.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c                  2d spectra.
      INTEGER PART(MSPEC,NANG,NFRE),
     &        PEAKANG(DIMSPEC,DIMANG*DIMFRE/2),
     &        PEAKFRE(DIMSPEC,DIMANG*DIMFRE/2)
c       part(..) gives number of partitioning for each spectral bin.
c       partinfo =1 -> wind sea, =2 -> mixed wind sea-swell =0 -> swell
c        , 3=old windsea.
c       index of peak direction and peak frequency of partitionings.
c
c     local variables:
c     ----------------
      INTEGER ISPEC, IPART, JPART, IANG, IFRE
c                  loop indexes.
c
c-----------------------------------------------------------------------
c
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)-1
          DO JPART = IPART+1,NPART(ISPEC)
            DO WHILE( 
     &          ((ABS(PEAKANG(ISPEC,IPART)-PEAKANG(ISPEC,JPART)).EQ.1
     &          .OR.ABS(PEAKANG(ISPEC,IPART)-PEAKANG(ISPEC,JPART))
     &          .EQ.NANG-1)
     &          .AND.PEAKFRE(ISPEC,IPART).EQ.PEAKFRE(ISPEC,JPART)
     &          .OR.PEAKANG(ISPEC,IPART).EQ.PEAKANG(ISPEC,JPART)
     &          .AND.ABS(PEAKFRE(ISPEC,IPART)-PEAKFRE(ISPEC,JPART))
     &          .EQ.1)
     &          .AND. JPART.LE.NPART(ISPEC))
c             change jpart to ipart and npart(ispec) to jpart
              DO IANG = 1,NANG
                DO IFRE = 1,NFRE
                  IF( PART(ISPEC,IANG,IFRE).EQ.JPART )THEN
                    PART(ISPEC,IANG,IFRE) = IPART
                  ELSE IF( PART(ISPEC,IANG,IFRE).EQ.NPART(ISPEC) )THEN
                    PART(ISPEC,IANG,IFRE) = JPART
                  END IF
                END DO
              END DO
              PEAKANG(ISPEC,JPART) = PEAKANG(ISPEC,NPART(ISPEC))
              PEAKFRE(ISPEC,JPART) = PEAKFRE(ISPEC,NPART(ISPEC))
              NPART(ISPEC) = NPART(ISPEC) - 1
            END DO
          END DO
        END DO
      END DO
c
      RETURN
c
      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE PARTITIONING( 
c                  dimensions
     &               DIMSPEC , MSPEC , NSPEC ,
     &               MPART , NPART , DIMANG , NANG , DIMFRE , NFRE ,
c                  input
     &               SPEC , 
c                  output
     &               PART , EQUIPART , PEAKANG , PEAKFRE )
c
c-----------------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c     partions spectra.
c
c     susanne hasselmann, mpi hamburg, 1992.
c     juergen waszkewitz,mpi hamburg, 1993 (vectorization)
c
c     method:
c     -------
c
c     the spectral partitioning is achieved by first running through the array
c     of all spectral grid points, determining for each grid point its
c     highest neighbour. each point is assigned a part
c     number. the following cases occur:
c     - the grid point and its highest neighbour has no part number:
c       then both are assigned the same new part number.
c     - one of them has already a part number, the other does not.
c       then the other is assigned the same part number.
c     - both, the grid point and the highest neighbour, have part numbers
c       (which are different). then in a special list
c       part numbers are saved, that the part number of the grid point
c       is equivalent to the part number of the highest neighbour. 
c     after assigning the part numbers to each grid point, all equivalent
c     part numbers are changed to one unique part number.
c
c     to make this routine as fast as possible, the loop over all spectras
c     is a vectorized inner loop!
c
c     
c-----------------------------------------------------------------------
      IMPLICIT NONE
c     interface:
c     ----------
c     
      INTEGER DIMSPEC, MSPEC, NSPEC, MPART, NPART(MSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
c                  array dimensions.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c                  2d spectra. 
      INTEGER PART(MSPEC,NANG,NFRE),
     &        PEAKANG(DIMSPEC,DIMANG*DIMFRE/2),
     &        PEAKFRE(DIMSPEC,DIMANG*DIMFRE/2)
c       part(..) gives number of partitioning for each spectral bin.
c       partinfo =1 -> wind sea, =2 -> mixed wind sea-swell =0 -> swell
c        , 3=old windsea.
c       index of peak direction and peak frequency of partitionings.
      INTEGER EQUIPART( DIMSPEC , DIMANG*DIMFRE/2 )
c                  contains equivalent part numbers
c
c     local variables:
c     ----------------
      INTEGER ISPEC, IPART, JPART , IANG, IFRE
c                   loop indexes.
      INTEGER IANGP1, IANGM1
c                  "iang plus 1" , "iang minus 1"
      INTEGER HANG, HFRE
c                   angle and frequency index of highest neighbour
      DOUBLE PRECISION  HSPEC
c                   value of highest neighbour
      DOUBLE PRECISION  HSPEC0
c                   for temporary use
c
c-----------------------------------------------------------------------
c
c     1.intitialize.
c     --------------

      DO ISPEC = 1,NSPEC
        NPART(ISPEC) = 0
        DO IANG = 1,NANG
          DO IFRE = 1,NFRE
            PART(ISPEC,IANG,IFRE) = 0
          END DO
        END DO
        DO IPART = 1,NANG*NFRE/2
          EQUIPART(ISPEC,IPART) = 0
          PEAKANG(ISPEC,IPART) = 0
          PEAKFRE(ISPEC,IPART) = 0
        END DO
      END DO

c     2. partition spectra.
c     ---------------------
c
      DO IANG = 1,NANG
        DO IFRE = 1,NFRE
C
          DO ISPEC = 1,NSPEC

           IF( SPEC(ISPEC,IANG,IFRE).LT.0.1E-13 )THEN
             PART(ISPEC,IANG,IFRE) = 1
           ELSE
c
c           find heighest neighbour
c
            HANG = IANG
            HFRE = IFRE
            HSPEC = SPEC(ISPEC,HANG,HFRE)
            IF( IANG.NE.NANG )THEN
              IANGP1 = IANG + 1
            ELSE
              IANGP1 = 1
            ENDIF
            HSPEC0 = SPEC(ISPEC,IANGP1,IFRE)
            IF( HSPEC0.GT.HSPEC )THEN
              HANG = IANGP1
              HFRE = IFRE
              HSPEC = HSPEC0
            END IF
            IF( IANG.NE.1 )THEN
              IANGM1 = IANG - 1
            ELSE
              IANGM1 = NANG
            ENDIF
            HSPEC0 = SPEC(ISPEC,IANGM1,IFRE)
            IF( HSPEC0.GT.HSPEC )THEN
              HANG = IANGM1
              HFRE = IFRE
              HSPEC = HSPEC0
            END IF
            IF( IFRE.NE.NFRE )THEN
              HSPEC0 = SPEC(ISPEC,IANG,IFRE+1)
              IF( HSPEC0.GT.HSPEC )THEN
                HANG = IANG
                HFRE = IFRE+1
                HSPEC = HSPEC0
              END IF
            END IF
            IF( IFRE.NE.1 )THEN
              HSPEC0 = SPEC(ISPEC,IANG,IFRE-1)
              IF( HSPEC0.GT.HSPEC )THEN
                HANG = IANG
                HFRE = IFRE-1
              END IF
            END IF

c           set part number to point or neighbpour

            IF( IANG.EQ.HANG .AND. IFRE.EQ.HFRE )THEN
c             point is peak
              IF( PART(ISPEC,IANG,IFRE).EQ.0 )THEN
                NPART(ISPEC) = NPART(ISPEC) + 1
                PART(ISPEC,IANG,IFRE) = NPART(ISPEC)
              END IF
              PEAKANG(ISPEC,PART(ISPEC,IANG,IFRE)) = IANG
              PEAKFRE(ISPEC,PART(ISPEC,IANG,IFRE)) = IFRE
            ELSE
c             point is no peak
              IF( PART(ISPEC,IANG,IFRE).NE.0 )THEN
                IF( PART(ISPEC,HANG,HFRE).NE.0 )THEN
                  EQUIPART(ISPEC,PART(ISPEC,IANG,IFRE))
     &              = PART(ISPEC,HANG,HFRE)
                ELSE
                  PART(ISPEC,HANG,HFRE) = PART(ISPEC,IANG,IFRE)
                END IF
              ELSE
                IF( PART(ISPEC,HANG,HFRE).NE.0 )THEN
                  PART(ISPEC,IANG,IFRE) = PART(ISPEC,HANG,HFRE)
                ELSE
                  NPART(ISPEC) = NPART(ISPEC) + 1
                  PART(ISPEC,IANG,IFRE) = NPART(ISPEC)
                  PART(ISPEC,HANG,HFRE) = NPART(ISPEC)
                END IF
              END IF
            END IF
           END IF
          END DO
        END DO
      END DO

c    3. assign equivalent part numbers to one unique number.
c     ------------------------------------------------------

c     first: assign to every part number this unique number

      DO ISPEC = 1,NSPEC
        JPART = 0
        DO IPART = 1,NPART(ISPEC)
          IF( EQUIPART(ISPEC,IPART).EQ.0 )THEN
            JPART = JPART + 1
            EQUIPART(ISPEC,IPART) = -JPART
            PEAKANG(ISPEC,JPART) = PEAKANG(ISPEC,IPART)
            PEAKFRE(ISPEC,JPART) = PEAKFRE(ISPEC,IPART)
          END IF
        END DO
        NPART(ISPEC) = JPART
      
        IF( JPART.GT.MPART )THEN
          WRITE(6,*) 'ERROR! SUBROUTINE SWELLSEP:'
          WRITE(6,*) 'DIMENSION MPART IS TOO SMALL'
          WRITE(6,*) 'FOR THE PARTITIONING OF SPECTRA NUMBER ',ISPEC,'!'
          WRITE(6,*) 'IT MUST BE MPART >= ',JPART,'!'
          WRITE(6,*) 'CHANGE PARAMETER MPART'
          WRITE(6,*) 'IN THE SWELLSEP CALLING ROUTINE!'
          WRITE(6,*) '(DO NOT FORGET TO MAKE SURE,'
          WRITE(6,*) 'THAT DIMPART IN SUBROUTINE SWELLSEP IS >= MPART!)'
          STOP
        ENDIF

c       now npart(ispec) contains the number of partitions
c       and the list equipart( , ) ends with the first 0.

        IPART = 1
        DO WHILE( EQUIPART(ISPEC,IPART).NE.0.AND.IPART.LE.NANG*NFRE/2 ) 
          JPART = IPART
          DO WHILE( JPART.GE.0 )
            JPART = EQUIPART(ISPEC,JPART)
          END DO
          EQUIPART(ISPEC,IPART) = JPART
          IPART = IPART + 1
        END DO
      END DO

C     THEN: ASSIGN TO EVERY POINT THIS UNIQUE PART NUMBER

      DO IANG = 1,NANG
        DO IFRE = 1,NFRE
C
          DO ISPEC =1,NSPEC
            PART(ISPEC,IANG,IFRE) 
     &         = MAX( 1 , -EQUIPART(ISPEC,PART(ISPEC,IANG,IFRE)) )
          END DO
        END DO
      END DO
 
      RETURN

      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE SUMENERGY( 
c                  dimensions
     &               DIMSPEC , MSPEC , NSPEC ,
     &               DIMPART , MPART , NPART ,
     &               DIMANG , NANG , DIMFRE , NFRE ,
c                  input
     &               SPEC , PART ,
c                  output
     &               MEANE , SPREAD , 
c                  work space
     &               SUMX , SUMY , SUMXX , SUMYY ,
     &               SUM0 , SUMX0 , SUMY0 , SUMXX0 , SUMYY0 ,
c                  input tables.
     &               FRETAB , COSTAB , SINTAB , DFIM )
c
c-----------------------------------------------------------------------
c
C
C     PURPOSE:
C     --------
C
C     COMPUTE MEAN ENERGY AND SQUARES OF SPREAD FOR ALL PARTITIONINGS.
C
C
c-----------------------------------------------------------------------
      IMPLICIT NONE
c     interface:
c     ----------
c
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMPART, MPART, NPART(MSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
c                    array dimensions.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c                    2d spectra.
      INTEGER PART(MSPEC,NANG,NFRE)
c                    part(..) gives number of partitioning for each 
c                    spectral bin.
      DOUBLE PRECISION  MEANE(MSPEC,MPART),
     &     SPREAD(DIMSPEC,DIMPART),
c                    mean energy, spectral spread.
     &    SUMX(DIMSPEC,DIMPART), SUMY(DIMSPEC,DIMPART),
     &    SUMXX(DIMSPEC,DIMPART), SUMYY(DIMSPEC,DIMPART)
c                    work space.
      DOUBLE PRECISION  SUM0(DIMSPEC,DIMPART),
     &     SUMX0(DIMSPEC,DIMPART),SUMXX0(DIMSPEC,DIMPART),
     &     SUMY0(DIMSPEC,DIMPART),SUMYY0(DIMSPEC,DIMPART)
c                    temporary space.
      DOUBLE PRECISION  FRETAB(DIMFRE),COSTAB(DIMANG),SINTAB(DIMANG),
     &     DFIM(DIMFRE)
c                    table of frequencies,cos,sin,freq.increment/directional 
c                    increment.
c
c
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IPART, IANG, IFRE
c                  loop indexes.
      DOUBLE PRECISION  FX, FY
c                  wave numbers.
      DOUBLE PRECISION  PI, PI2NANG
c
c-----------------------------------------------------------------------
cn==
      DOUBLE PRECISION spreadaux(50,65)
cn      DOUBLE PRECISION spreadaux(DIMSPEC,DIMPART)
           common /spr/ spreadaux
cn==
c
c     compute sums and square sums
c     ---------------------------
c
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          MEANE(ISPEC,IPART) = 0.1D-90
          SUMX(ISPEC,IPART) = 0
          SUMY(ISPEC,IPART) = 0
          SUMXX(ISPEC,IPART) = 0
          SUMYY(ISPEC,IPART) = 0
        END DO
      END DO
      DO IFRE = 1,NFRE
        DO ISPEC = 1,NSPEC
          DO IPART = 1,NPART(ISPEC)
            SUM0(ISPEC,IPART) = 0
            SUMX0(ISPEC,IPART) = 0 
            SUMY0(ISPEC,IPART) = 0 
            SUMXX0(ISPEC,IPART) = 0 
            SUMYY0(ISPEC,IPART) = 0 
          END DO
        END DO
        DO IANG = 1,NANG
          FX = FRETAB(IFRE) * COSTAB(IANG)
          FY = FRETAB(IFRE) * SINTAB(IANG)
C
          DO ISPEC = 1,NSPEC
            SUM0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          = SUM0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          + SPEC(ISPEC,IANG,IFRE)
            SUMX0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          = SUMX0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          + FX * SPEC(ISPEC,IANG,IFRE)
            SUMXX0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          = SUMXX0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          + FX**2 * SPEC(ISPEC,IANG,IFRE)
            SUMY0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          = SUMY0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          + FY * SPEC(ISPEC,IANG,IFRE)
            SUMYY0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          = SUMYY0(ISPEC,PART(ISPEC,IANG,IFRE))
     &          + FY**2 * SPEC(ISPEC,IANG,IFRE)
          END DO
        END DO
        DO ISPEC = 1,NSPEC
          DO IPART = 1,NPART(ISPEC)
            MEANE(ISPEC,IPART) = MEANE(ISPEC,IPART)
     &          + DFIM(IFRE) * SUM0(ISPEC,IPART)
            SUMX(ISPEC,IPART) = SUMX(ISPEC,IPART)
     &          + DFIM(IFRE) * SUMX0(ISPEC,IPART)
            SUMY(ISPEC,IPART) = SUMY(ISPEC,IPART)
     &          + DFIM(IFRE) * SUMY0(ISPEC,IPART)
            SUMXX(ISPEC,IPART) = SUMXX(ISPEC,IPART)
     &          + DFIM(IFRE) * SUMXX0(ISPEC,IPART)
            SUMYY(ISPEC,IPART) = SUMYY(ISPEC,IPART)
     &          + DFIM(IFRE) * SUMYY0(ISPEC,IPART)
          END DO
        END DO
      END DO
c
c     add tail energy
c     ---------------
c
      PI = 3.141592653589793
      PI2NANG = PI / 2 / NANG
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          MEANE(ISPEC,IPART) = MEANE(ISPEC,IPART)
     &        + FRETAB(NFRE) * PI2NANG * SUM0(ISPEC,IPART)
        END DO
      END DO
c
c     compute spread
c     --------------
c
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          SPREAD(ISPEC,IPART) = MAX
cn          spreadaux(ISPEC,IPART) = MAX
     &        ( SUMXX(ISPEC,IPART)/MEANE(ISPEC,IPART)
     &        + SUMYY(ISPEC,IPART)/MEANE(ISPEC,IPART)
     &        - (SUMX(ISPEC,IPART)/MEANE(ISPEC,IPART))**2
     &        - (SUMY(ISPEC,IPART)/MEANE(ISPEC,IPART))**2
cn     &        , 0.D0)
     &        , 0.)
c      write(*,*)'spreadaux =',  spreadaux(ISPEC,IPART)
c      write(*,*)'spread =',  spread(ISPEC,IPART)
        END DO
      END DO
      RETURN
c
      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE THRESHHOLD( 
c                  dimensions
     &               DIMSPEC , MSPEC , NSPEC ,
     &               DIMPART , MPART , NPART ,
     &               DIMANG , NANG , DIMFRE , NFRE ,
c                  input/output
     &               SPEC,PART,PARTINFO,PEAKANG,PEAKFRE,FX,FY,
     &               MEANE,SPREAD,
c                  work space
     &               SUMX,SUMY,SUMXX,SUMYY,
c                  input tables
     &               FRETAB , LEVEL , CONTROL )
c
c-----------------------------------------------------------------------
c
c
c     purpose:
c     --------
c
c     combines parts if minimum energy between peaks is larger than
c     >level<  times the lowest energy of the peaks. 
c
c
c     method:
c     -------
c
c     for every spectrum and every pair of peaks "walk" the most 
c     direct way in the grid from one peak to the other. 
c
c
c     exernals:
c     ---------
c
c     docombine - combining of two partitions.
c
c-----------------------------------------------------------------------
c
      IMPLICIT NONE
c     interface:
c     ----------
c
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMPART, MPART, NPART(MSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
c                  array dimensions.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c                  2d spectrum.
      INTEGER PART(MSPEC,NANG,NFRE),
     &        PARTINFO(MSPEC,MPART),
     &        PEAKANG(DIMSPEC,DIMANG*DIMFRE/2),
     &        PEAKFRE(DIMSPEC,DIMANG*DIMFRE/2)
c      part(..) gives number of partitioning for each spectral bin.
c      partinfo =1 -> wind sea, =2 -> mixed wind sea-swell =0 -> swell
c       , 3=old windsea.
c      index of peak direction and peak frequency of partitionings.
c
cn      DOUBLE PRECISION  SPREAD(50,65)
      DOUBLE PRECISION  FX(DIMSPEC,DIMPART), FY(DIMSPEC,DIMPART),
     &     MEANE(MSPEC,MPART),
     &     SPREAD(DIMSPEC,DIMPART),
c                  mean wave numbers, mean energy and spread of 
c                  partitionings.
     &     SUMX(DIMSPEC,DIMPART), SUMY(DIMSPEC,DIMPART),
     &     SUMXX(DIMSPEC,DIMPART), SUMYY(DIMSPEC,DIMPART)
c                  work space.
      DOUBLE PRECISION  FRETAB(DIMFRE), LEVEL
c                  table of frequencies, threshhold level.
      LOGICAL CONTROL
c
c     local variables:
c     ----------------
c
      INTEGER ISPEC, IPART, JPART, IANG, IFRE
c                   loop indexes. 
      LOGICAL COMBINE
      INTEGER DISTANG, DISTFRE
c                   absolut value of distance in gridpoints between
c                   both peaks in angle or frequency rsp.
      INTEGER DIST
c                   the distance in gridpoints between two peaks. 
      INTEGER STEPANG, STEPFRE
c                   direction for "walking" in the grid from one peak to
c                   the other,contains -1 or 1.
      INTEGER IDIST
c                   counts steps while "walking" in the grid from one 
c                   peak to the other.
      INTEGER SUMANG, SUMFRE
c                  sums to decide if to make a ang-step or a fre-step
c                  while "walking" in the grid from one peak to 
c                  the other
      INTEGER DIST2ANG, DIST2FRE
c                  twice the value distang or distfre rsp. 
      DOUBLE PRECISION  PEAKENERGY
      INTEGER TEMP1, TEMP2,ipa,jpa
c                  for temporarily use
c
c---------------------------------------------------------------------
c
      DO ISPEC = 1,NSPEC
        IPART = 1
        DO WHILE( IPART.LE.NPART(ISPEC)-1 .AND.
     &                                PARTINFO(ISPEC,IPART).EQ.0)
          JPART = IPART + 1
          DO WHILE( IPART.NE.0 .AND. JPART.LE.NPART(ISPEC) .AND.
     &                                PARTINFO(ISPEC,JPART).EQ.0)
c           "walking" in the grid from peak i to peak j
            DISTANG = PEAKANG(ISPEC,JPART) - PEAKANG(ISPEC,IPART)
            IF( DISTANG.LT.0 ) DISTANG = DISTANG + NANG
            IF( DISTANG.LT.NANG/2 )THEN
c             "walk" from "left" to "right"
              STEPANG = 1
              COMBINE = .TRUE.
            ELSE IF( DISTANG.GT.NANG/2 )THEN
c             "walk" from "right" to "left"
              DISTANG = NANG - DISTANG
              STEPANG = -1
              COMBINE = .TRUE.
            ELSE
c             do not combine
              STEPANG = 0
              COMBINE = .FALSE.
            ENDIF
            DISTFRE = PEAKFRE(ISPEC,JPART)-PEAKFRE(ISPEC,IPART)
            STEPFRE = SIGN(1,DISTFRE)
            DISTFRE = ABS(DISTFRE)
            DIST = DISTANG  + DISTFRE
            PEAKENERGY = MIN( 
     &          SPEC(ISPEC,PEAKANG(ISPEC,IPART),PEAKFRE(ISPEC,IPART)),
     &          SPEC(ISPEC,PEAKANG(ISPEC,JPART),PEAKFRE(ISPEC,JPART)))
            IANG = PEAKANG(ISPEC,IPART)
            IFRE = PEAKFRE(ISPEC,IPART)
c
            IPA=PART(ISPEC,IANG,IFRE)
            JPA=PART(ISPEC,PEAKANG(ISPEC,JPART),PEAKFRE(ISPEC,JPART))
c
            SUMANG = ABS(DISTANG)
            SUMFRE = ABS(DISTFRE)
            DIST2ANG = 2 * DISTANG
            DIST2FRE = 2 * DISTFRE
            IDIST = 1
            DO WHILE( COMBINE .AND. IDIST.LT.DIST )
              IF( SUMANG.GT.SUMFRE )THEN
                IANG = IANG + STEPANG
                IF( IANG.LE.0 )THEN
                  IANG = IANG + NANG
                ELSE IF( IANG.GT.NANG )THEN
                  IANG = IANG - NANG
                END IF
                SUMFRE = SUMFRE + DIST2FRE
                IDIST = IDIST + 1
                IF( SPEC(ISPEC,IANG,IFRE).LT.LEVEL*PEAKENERGY )
     &              COMBINE = .FALSE.
              ELSE IF( SUMFRE.GT.SUMANG )THEN
                IFRE = IFRE + STEPFRE
                SUMANG = SUMANG + DIST2ANG
                IDIST = IDIST + 1
                IF( SPEC(ISPEC,IANG,IFRE).LT.LEVEL*PEAKENERGY )
     &              COMBINE = .FALSE.
              ELSE
                TEMP1 = IANG
                IANG = IANG + STEPANG
                IF( IANG.LE.0 )THEN
                  IANG = IANG + NANG
                ELSE IF( IANG.GT.NANG )THEN
                  IANG = IANG - NANG
                END IF
                IF( SPEC(ISPEC,IANG,IFRE).LT.LEVEL*PEAKENERGY )
     &              COMBINE = .FALSE.
                TEMP2 = IANG
                IANG = TEMP1
                IFRE = IFRE + STEPFRE
                IF( SPEC(ISPEC,IANG,IFRE).LT.LEVEL*PEAKENERGY )
     &              COMBINE = .FALSE.
                IANG = TEMP2
                SUMANG = SUMANG + DIST2ANG
                SUMFRE = SUMFRE + DIST2FRE
                IDIST = IDIST + 2
              END IF
                IF(PART(ISPEC,IANG,IFRE).NE.IPA.AND.
     1             PART(ISPEC,IANG,IFRE).NE.JPA) 
     &              COMBINE = .FALSE.
c
            END DO
            IF( COMBINE )THEN
              CALL DOCOMBINE( IPART , JPART , ISPEC ,
     &            DIMSPEC , MSPEC , NSPEC ,
     &            DIMPART , MPART , NPART ,
     &            DIMANG , NANG , DIMFRE , NFRE ,
     &            SPEC , PART , PARTINFO ,
     &            PEAKANG , PEAKFRE , FX, FY,
     &            MEANE , SPREAD , SUMX , SUMY , SUMXX , SUMYY ,
     &            FRETAB , CONTROL )
              IF( CONTROL ) WRITE(6,*) ' REASON: ',
     &            'MINIMUM ENERGY BETWEEN THEM IS HIGHER THAN ',
     &            LEVEL,' OF THE MINIMUM PEAK ENERGY'
              IPART = 0
            ELSE
              JPART = JPART + 1
            END IF
          END DO
          IPART = IPART + 1
        END DO
      END DO
c
      RETURN
c
      END
c
c-----------------------------------------------------------------------
c
      SUBROUTINE WINDSEA( 
c                  dimensions
     &               DIMSPEC , MSPEC , NSPEC ,
     &               DIMPART , MPART , NPART ,
     &               DIMANG , NANG , DIMFRE , NFRE ,
c                  input
     &               SPEC , PART , 
c                  output
     &               PARTINFO , 
c                  input
     &               PEAKANG , PEAKFRE , FX, FY,
     &               MEANE ,  MEANANG, MEANFRE ,
     &               SPREAD , 
c                  work space
     &               SUMX , SUMY , SUMXX , SUMYY ,
c                  input tables
     &               U10 , THW , FRETAB , COSTAB , SINTAB , CONTROL )
c
c-----------------------------------------------------------------------
c
C
C     PURPOSE:
C     --------
C
C     DECIDE, WHICH ARE WINDSEA (=1), MIXED (=2), AND 
C     SWELL (=0) , OLD WINDSEA (=3) SYSTEMS,
C     STORE THIS INFORMATION IN ARRAY PARTINFO AND
C     COMBINE ALL WINDSEA PEAKS.
C     (AS A SIDE EFFECT THE ARRAYS FX AND FY ARE INITIALIZED)
C
C
C     EXERNALS:
C     ---------
C
C     DOCOMBINE - TO DO THE COMBINING OF TWO PARTITIONS TO ONE
C
C
c-----------------------------------------------------------------------
      IMPLICIT NONE
C     INTERFACE:
C     ----------
C
      INTEGER DIMSPEC, MSPEC, NSPEC, DIMPART, MPART, NPART(MSPEC),
     &        DIMANG, NANG, DIMFRE, NFRE
c                  array dimensions.
      DOUBLE PRECISION  SPEC(0:MSPEC,NANG,NFRE)
c                  2d spectra.
      INTEGER PART(MSPEC,NANG,NFRE),
     &        PARTINFO(MSPEC,MPART),
     &        PEAKANG(DIMSPEC,DIMANG*DIMFRE/2),
     &        PEAKFRE(DIMSPEC,DIMANG*DIMFRE/2)
c                 part(..) gives number of partitioning for each spectral bin.
c                 partinfo =1 -> wind sea, =2 -> mixed wind sea-swell, 
c                 =0 -> swell , 3=old windsea.
c                 index of peak direction and peak frequency of partitionings.
c
cn      DOUBLE PRECISION  SPREAD(50,65)
      DOUBLE PRECISION  FX(DIMSPEC,DIMPART), FY(DIMSPEC,DIMPART),
     &     MEANE(MSPEC,MPART),MEANANG(MSPEC,MPART),
     &     MEANFRE(MSPEC,MPART),
     &     SPREAD(DIMSPEC,DIMPART),
c              mean wave numbers, mean energy and spread of partitionings.
     &     SUMX(DIMSPEC,DIMPART), SUMY(DIMSPEC,DIMPART),
     &     SUMXX(DIMSPEC,DIMPART), SUMYY(DIMSPEC,DIMPART)
c                  work space.
      DOUBLE PRECISION  U10(MSPEC) , THW(MSPEC)
c                  u10, wind direction.
      DOUBLE PRECISION  FRETAB(DIMFRE),COSTAB(DIMANG),SINTAB(DIMANG)
c                  table of frequencies,cos,sin,freq.increment/directional 
c                  increment.
      LOGICAL CONTROL
c
c     local variables:
c     ----------------
c
      INTEGER  ISPEC, IPART, JPART
c                   loop indexes.
      DOUBLE PRECISION PI,TWEG,DELTANG,THWQ,CM,CT,THQP,CTE,CMP, CTP,
     &     SQF, THQPP, THQPM, CTEP, CTEM,SQSPREAD, CTETWO
c
      LOGICAL WINSEA
c
c---------------------------------------------------------------------
cn==
      DOUBLE PRECISION SPREADaux(50,65)
           common /spr/ spreadaux
cn==
c
c     1. set array partinfo to zero.
c     ------------------------------
c
      DO ISPEC = 1,NSPEC
        DO IPART = 1,NPART(ISPEC)
          PARTINFO(ISPEC,IPART) = 0
        END DO
      END DO
c
c     2. find all windsea and mixed peaks.
c     ------------------------------------
c
      PI = 3.141592653589793
      TWEG = 2.*1.3* PI / 9.806
      DELTANG = 2 * PI / NANG
CN=============
      write(6,*)'i was here'
CN=============
c
      DO ISPEC = 1,NSPEC
         THWQ = THW(ISPEC)
	 write(*,*)'new u10=',U10(ISPEC),'dir=',THW(ISPEC)
         WINSEA=.FALSE.
         DO IPART = 1,NPART(ISPEC)
            THQP = DELTANG * (PEAKANG(ISPEC,IPART)-1)
            CM = TWEG * FRETAB(PEAKFRE(ISPEC,IPART))
            CT = CM * U10(ISPEC)
            CTE = CT * COS(THQP-THWQ) - 1.
            CTETWO = (2. / 1.3) * CT * COS(THQP-THWQ) - 1.
            IF ( CTE.GT.0 ) THEN
               WINSEA=.TRUE.
               PARTINFO(ISPEC,IPART) = 1
            ELSE IF ( CTETWO.GT.0 ) THEN
               WINSEA=.TRUE.
               PARTINFO(ISPEC,IPART) = 3               
            ENDIF
         END DO
         IF(.NOT.WINSEA) THEN
            DO IPART = 1,NPART(ISPEC)
               SQSPREAD = SQRT(SPREAD(ISPEC,IPART)/2.)
cn               SQSPREAD = SQRT(spreadaux(ISPEC,IPART)/2.)
               THQP = MEANANG(ISPEC,IPART)
               CM = TWEG * MEANFRE(ISPEC,IPART)
               CMP = CM + TWEG * SQSPREAD
               CTP = CMP * U10(ISPEC)
               SQF = SQSPREAD/
     &              (MEANFRE(ISPEC,IPART))
               THQPP = THQP + SQF
               THQPM = THQP - SQF
               CTEP = CTP * COS(THQPP-THWQ) - 1.
               CTEM = CTP * COS(THQPM-THWQ) - 1.
	       write(*,*)'CTEP=',CTEP	       
               IF( CTEP.GT.0. .OR. CTEM.GT.0. )THEN
                  PARTINFO(ISPEC,IPART) = 2
               END IF
            END DO
         END IF
      END DO
c
c     3.combine all windsea peaks.
c     ----------------------------
c
      DO ISPEC = 1,NSPEC
        IPART = 0
        DO JPART = 1,NPART(ISPEC)
          IF( PARTINFO(ISPEC,JPART).gt.0 )THEN
            IF( IPART.EQ.0 )THEN
              IPART = JPART
            ELSE
              DO WHILE( PARTINFO(ISPEC,JPART).gt.0
     &            .AND.JPART.LE.NPART(ISPEC) )
                CALL DOCOMBINE( 
c                      dimensions
     &                   IPART , JPART , ISPEC ,
     &                   DIMSPEC , MSPEC , NSPEC ,
     &                   DIMPART , MPART , NPART ,
     &                   DIMANG , NANG , DIMFRE , NFRE ,
c                      input/output
     &                   SPEC , PART , PARTINFO ,
     &                   PEAKANG , PEAKFRE , FX, FY,
     &                   MEANE , SPREAD , 
c                      work space
     &                   SUMX , SUMY , SUMXX , SUMYY ,
c                      tables.
     &                   FRETAB , CONTROL )
                IF( CONTROL )
     &              WRITE(6,*) ' REASON: BOTH ARE WINDSEA PEAKS'
              END DO
            END IF
          END IF
        END DO
      END DO
c
      RETURN
c
      END

