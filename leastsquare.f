      SUBROUTINE leastsquare(A,b,x,M,N,w,v)
C
C *************************************************
C *******  Solves A x = b in the least square sense
C *************************************************
C
      PARAMETER(EPS=1.E-10, NMAX=300)
      REAL skal, sum, rezw,wmax
      INTEGER i,j,k,M,N
      REAL A(M,N), B(M), W(N), v(N,N), X(N),coeff(NMAX)
C
C =====================================================
C --  Compute singular value decomposition
C =====================================================
      CALL SVDCMP(A,M,N,M,N,W,V)    
C =====================================================
C --------------  FIND largest W(i) ------------------
C =====================================================
      wmax = ABS(W(1))
      DO i=2,N
         IF (ABS(W(i)).GT.wmax) wmax = ABS(W(i))
      END DO 
C =====================================================
C -- Calculate coefficients for linear combination of 
C -- columns of V. If W(i) is too small 1/W(i) is set 
C -- to zero
C =====================================================           
      DO i=1,N    
         IF (ABS(W(i)).LT.(N*EPS*wmax)) THEN
            rezw = 0.
         ELSE
            rezw = 1./W(i)
         END IF 
         skal = 0.
         DO k=1,M
               skal=skal+A(k,i)*B(k)
         END DO
         coeff(i) = skal*rezw
      END DO     
C =======================================================
C - calculate solution x as linear combination of columns
C - of v
C =======================================================
      DO j=1,N
         sum = 0.
         DO i=1,M
            sum = sum + coeff(i)*V(j,i)
         END DO
         X(j) = sum
      END DO
C                  
      END
          
