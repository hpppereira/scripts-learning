function pxxs = smooth(pxx,nd2,ndf)
% pxxs=smooth(pxx,nd2,ndf)
%
% An M-file to smooth a  time series pxx, that contains
% nd2 data points using averages over ndf/2 values.  
%
% IMPORTANT: This function performs the smoothing of a time series
%            with nd2 points without any consideration of a mean
%            value as the first position. This problem happens when
%            you are trying to smooth a spectrum taking into account
%            the first value of the FFT (k=0). To handle the mean
%            value as a first point, you should see the smoothing in
%            m_file pspec.m.
%
% Jose A. Lima - 28/08/96 
%
% Smooth the one-sided Power Spectra with ndf degrees of freedom
%    PS: The smoothing is performed using a running mean over
%        ndf/2 adjacent spectral points. In order to improve the
%        operation, it is done a convolution in the frequency 
%        domain between the non-smoothed power density function pxx
%        and a function rmean containing ndf/2 equal weigths.
%        The Matlab convolution function conv(a,b) runs the inverted
%        series b over series a, from left to right:
%                    b3 b2 b1 =>
%                          a1 a2 a3 a4 a5
%
if ndf > 2
   m=fix(ndf/2);
%  Calculating the weight function rmean
   rmean=ones(m,1)/m;
%  Generate an auxiliar vector to convolute 
   aux=[ flipud(pxx(1:fix(m/2))) 
         pxx(1:nd2) 
         flipud(pxx(nd2-m:nd2-1)) ];
   c=conv(aux,rmean);
%  Adjust the frequency position to generate the smoothed spectrum
   pxxs=[ c( m : m+nd2-1 ) ];
else
% For the case of ndf=2, there is no smoothing at all
  pxxs=pxx(1:nd2);
end
