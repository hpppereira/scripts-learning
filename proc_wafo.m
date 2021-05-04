% Simulacao de dados com WAFO
% Henrique Pereira
% Criado em: 18/03/2021
% Modificado em: 18/03/2021

clear, clc, close all

%  =============================================================================== #

% pathname = '/home/hp/Dropbox/doutorado/dados/HNE_rio_grande_200905/';
% W = dlmread([pathname, '200905252100.HNE'], '', 11, 0);
% geraonda
% W = load('registro.txt');

%  =============================================================================== #
% JONSWAP Calculates (and plots) a JONSWAP spectral density
% CALL:  S = jonswap(w,sdata,plotflag); 
%        S = jonswap(wc,sdata,plotflag); 
% S     = a struct containing the spectral density. See datastructures
% w     = angular frequency        (default linspace(0,wc,257))
% wc    = angular cutoff frequency (default 33/Tp)
% sdata = [Hm0 Tp gamma sa sb A], where
%        Hm0   = significant wave height (default 7 (m))
%        Tp    = peak period (default 11 (sec))
%        gamma = peakedness factor determines the concentraton
%                of the spectrum on the peak frequency,  1 <= gamma <= 7. 
%                (default depending on Hm0, Tp, see below)
%        sa,sb = spectral width parameters (default 0.07 0.09)
%        Ag    = normalization factor used when gamma>1, (default -1)
%                Ag<0  : Ag calculated by integration so that int S dw =Hm0^2/16
%                Ag==0 : Ag = (1+1.00*log(gamma)^1.16)/gamma  
%                Ag>0  : Ag = Ag
%     plotflag = 0, do not plot the spectrum (default).
%                1, plot the spectrum.

%  =============================================================================== #
% Simula espectro 1D

Hm0 = 5;
Tp = 10;
wc = 33/Tp;
w = linspace(0, wc, 257);
D = 0.036 - 0.0056 * Tp/sqrt(Hm0);
gamma = exp(3.484*(1-0.1975*D*Tp^4/(Hm0^2)));
sa = 0.07;
sb = 0.09;
A = -1;
plotflag = 0;
S = jonswap(w,[Hm0 Tp gamma sa sb A],plotflag);

%  =============================================================================== #
% Simulation from spectrum

% dt = 1;
% N = 1024;
% xs = spec2sdat(S, N, dt);
% waveplot(xs,'-')

%  =============================================================================== #
% DAT2SPEC Estimate one-sided spectral density from data.

%  CALL:  S = dat2spec(x,L,g,plotflag,p,method,dflag,ftype)

%          S = A structure containing:
%              S    = spectral density
%              w    = angular frequency
%              tr   = transformation g
%              h    = water depth (default inf)
%              type = 'freq'
%              note = Memorandum string
%              date = Date and time of creation 
%              L    = maximum lag size of the window function. 
%              CI   = lower and upper confidence constant  
%              p    = confidence level. (Default 0.95).
%              Bw   = Bandwidth of the smoothing window which is used 
%                     in the estimated spectrum. (rad/sec or Hz)
         
%          x =  m column data matrix with sampled times in the first column
%               and values the next columns.    

%          L = maximum lag size of the window function. 
%              If no value is given the lag size is set to
%              be the lag where the auto correlation is less than 
%              2 standard deviations. (maximum 300) 
                     
%          g = the transformation assuming that x is a sample of a 
%              transformed Gaussian process. If g is empty then
%              x  is a sample of a Gaussian process (Default)

%   plotflag = 1 plots the spectrum, S, 
%              2 plot 10log10(S) and
%              3 plots both the above plots

%   Method   = 'cov'   Frequency smoothing using a parzen window function
%                      on the estimated autocovariance function.  (default)
%              'psd'   Welch's averaged periodogram method with no overlapping 
%                      batches
%              'psdo'  Welch's averaged periodogram method with overlapping 
%                      batches
%              'pmem'  Maximum Entropy Method (psd using the Yule-Walker 
%                      AR method)
%              'pburg' Burg's method.

%   dflag    = specifies a detrending performed on the signal before estimation.
%              'mean','linear' or 'ma' (= moving average)  (default 'mean')   
%   ftype    = frequency type, 'w' or 'f'  (default 'w')

%  Method == 'cov','psd':
%   As L decreases the estimate becomes smoother and Bw increases. If we
%   want to resolve peaks in S which is Bf (Hz or rad/sec) apart then Bw < Bf. 

%  Method == 'pmem','pburg':
%   L denotes the order of the AR (AutoRegressive) model. 

%   NOTE: The strings method,dflag and ftype may be given anywhere after x 
%         and in any order.

% L = 400;
% g = [];
% plotflag = 0;
% p = 0.95;
% method = 'cov';
% dflag = 'mean';
% ftype = 'w';
% Sest = dat2spec(xs, L, g, plotflag, p, method, dflag, ftype);
% Sest = dat2spec(xs, [], [], 0, [], 'psdo', 'mean', 'w');

%  =============================================================================== #
% Comparacao do espectro teorico e simulado

% plotflag = 0
% plotspec(S,plotflag), hold on
% plotspec(Sest,plotflag,'--'), hold off

%  =============================================================================== #
% SPREADING Directional spreading functions

%  CALL:  D = spreading(th,type,th0,data,w,def);
%         D = spreading(Nt,type,th0,data,w,def);

%       D    = spreading function, struct reminding of spectrum struct   
%       th   = vector of direction angles, (default linspace(-pi,pi,Nt))
%       Nt   = scalar defining the length of th. (default 101)
%       type = type of spreading function, see options below (default 'cos2s')
%       th0  = vector or a scalar defining average direction at every frequency.
%              (length 1 or length == length(w)) (default 0)
%       data = vector of spreading parameters, see options below.
%              (default [15   15   0.52 5    -2.5  0    1    inf])
%       w    = frequency vector, if frequency dependent spreading 
%              (default linspace(0,3,257))
%       def  = 0 No frequency dependence of spreading function                
%              1 Mitsuyasu et al., Hasselman et al (JONSWAP experiment)
%                frequency dependent parametrization (default)
          
%  The different types of spreading functions implemented are:
%   type = 'cos2s'  : cos-2s spreading    N(S)*[cos((th-th0)/2)]^(2*S)  (0 < S) 
%          'box'    : Box-car spreading   N(A)*I( -A < th-th0 < A)      (0 < A < pi)
%          'mises'  : von Mises spreading N(K)*exp(K*cos(th-th0))       (0 < K)
%          'poisson': Poisson spreading   N(X)/(1-2*X*cos(th-th0)+X^2)  (0 < X < 1)
%          'sech2'  : sech-2 spreading    N(B)*0.5*B*sech(B*(th-th0))^2 (0 < B)
%          'wnormal': Wrapped Normal      
%                   [1 + 2*sum exp(-(n*D1)^2/2)*cos(n*(th-th0))]/(2*pi)  (0 < D1)
%          (N(.) = normalization factor)       
%          (the first letter is enough for unique identification)  

%  Here the S-parameter of the COS-2S spreading function is used as a
%  measure of spread. All the parameters of the other distributions are
%  related to this S-parameter throug the first Fourier coefficient, R1, of the
%  directional distribution as follows: 
%          R1 = S/(S+1) or S = R1/(1-R1).
%  where 
%          Box-car spreading  : R1 = sin(A)/A
%          Von Mises spreading: R1 = besseli(1,K)/besseli(0,K), 
%          Poisson spreading  : R1 = X
%          sech-2 spreading   : R1 = pi/(2*B*sinh(pi/(2*B))
%          Wrapped Normal     : R1 = exp(-D^2/2)

%  Use of data vector:
%    frequency dependent spreading:
%     data =  [spa spb wc ma mb wlim],
%            sp = maximum spread 
%            wc = cut over frequency (usually the peak frequency, wp or fp) 
%            m  = shape parameter defining the frequency dependent
%                 spreading parameter, S=S(w), where
%                 S(w) = sp *(w/wc)^m, with sp=spa, m=ma for wlim(1) <= w/wc < wlim(2)
%                                           sp=spb, m=mb for wlim(2) <= w/wc < wlim(3)
%                      = 0     otherwise 
%   frequency independent spreading:
%     data =  S,  default value: 15 which corresponds to 
%            'cos2s'  : S=15                      
%            'box'    : A=0.62   
%            'sech2'  : B=0.89      
%            'mises'  : K=8.3      
%            'poisson': X=0.94  
%            'wnormal': D=0.36

%  The 'cos2s' is the most frequently used spreading in engineering practice.
%  Apart from the current meter/pressure cell data in WADIC all
%  instruments seem to support the 'cos2s' distribution for heavier sea
%  states, (Krogstad and Barstow, 1999). For medium sea states
%  a spreading function between 'cos2s' and 'poisson' seem appropriate,
%  while 'poisson' seems appropriate for swell.
%    For the 'cos2s' Mitsuyasu et al. parameterized SPa = SPb =
%  11.5*(U10/Cp) where Cp = g/wp is the deep water phase speed at wp and
%  U10 the wind speed at reference height 10m. Hasselman et al. (1980)
%  parameterized  mb = -2.33-1.45*(U10/Cp-1.17).
%  Mitsuyasu et al. (1975) showed that SP for wind waves varies from 
%  5 to 30 being a function of dimensionless wind speed.
%  However, Goda and Suzuki (1975) proposed SP = 10 for wind waves, SP = 25
%  for swell with short decay distance and SP = 75 for long decay distance.
%  Compared to experiments Krogstad et al. (1998) found that ma = 5 +/- eps and
%  that -1< mb < -3.5. 
%  Values given in the litterature:        [spa  spb  wc   ma   mb      wlim(1:3)  ]
%       (Mitsuyasu: spa == spb)  (cos-2s)  [15   15   0.52 5    -2.5  0    1    inf]
%       (Hasselman: spa ~= spb)  (cos-2s)  [6.97 9.77 0.52 4.06 -2.52 0    1    inf]

%   NOTE: - by specifying NaN's in the data vector default values will be used.
%         - if length(data) is shorter than the parameters needed then the 
%           default values are used

%  Example:% Set  spa = 10,  wc = 0.43 and spb, ma, mb, wlim to their 
%          % default values, respectively: 

%    data = [10, nan, .43]; 
%    D = spreading(51,'cos2s',0,data);
%         % Frequency dependent direction
%    th0 = linspace(0,pi/2,257)';
%    D = spreading(51,'cos2s',th0,data);

% plotflag = 1;
Nt = 360; % number of angles
th0 = pi; % primary direction of waves
type = 'cos2s';
data = [15, 15, 0.52, 5, -2.5, 0, 1, inf];
w = S.w;
def = 1;
D = spreading(Nt, type, th0, data, w, def);

%  =============================================================================== #
% MKDSPEC Make a directional spectrum
%         frequency spectrum times spreading function

% CALL:  Snew=mkdspec(S,D,plotflag)

%       Snew = directional spectrum (spectrum struct)
%       S    = frequency spectrum (spectrum struct)
%                  (default jonswap)  
%       D    = spreading function (special struct)
%                  (default spreading([],'cos2s'))
%       plotflag = 1: plot the spectrum, else: do not plot (default 0)   

% Creates a directional spectrum through multiplication of a frequency
% spectrum and a spreading function: S(w,theta)=S(w)*D(w,theta)

% The spreading structure must contain the following fields:
%   .S (size [np 1] or [np nf])  and  .theta (length np)  
% optional fields: .w (length nf), .note (memo) .phi (rotation-azymuth)   

% NB! S.w and D.w (if any) must be identical.

% Example: 
%  S = jonswap;
%  D = spreading(linspace(-pi, pi, 51), 'cos2s');
%  Snew = mkdspec(S,D,1);

SD = mkdspec(S, D, 0);

%  =============================================================================== #
% SPEC2WAVE Spectral simulation of space-time Gaussian wave
        
% CALL: W = spec2wave(spec,options);

% W    = Gaussian wave structure W with fields 
%   .Z = matrix of size [Nx Nt] 
%   .x = space coordinates, length Nxalong x-axis 
%   .t = time coordinates, length Nt

% Spec = S, spectral density structure in 
%           angular frequency ('w') or frequency ('f') form 
% options = struct with fields 
%     .Nt  = giving  Nt  time points.  (default length(S)-1=n-1).
%              If Nt>n-1 it is assummed that  S.S(k)=0  for  k>n-1
%     .Nx  = giving  Nx  space points (defult = Nt)
%     .dt  = step in grid (default dt is defined by the Nyquist freq) 
%     .dx  = step in grid (default dx is defined by the Nyquist freq)
%    (.u     = if non-empty and = [u1 u2 Nu] the u-vector will be set to 
%              u = linspace(u1,u2,Nu), ONLY TESTED for ffttype='ffttime'
%              if empty, then u = linspace(0,(Nu-1)*du,Nu))
%     .iseed  - method or starting seed for the random number generator 
%              (default = 'shuffle')
%     .ffttype - 'fftspace', fft over space, loop over time
%                 generate space series with evolvement 
%                 over time (useful if Nu > Nt),  
%              - 'ffttime', fft over time, loop over space (default) 
%                 generate time series with evolvement 
%                 over space (useful if Nt > Nu),  
%              - 'ffttwodim', 2D-fft over time and space.  

% Example of spec2wave 

%  S=jonswap; opt=simoptset; 
%  opt=simoptset(opt,'dt',0.25,'dx',0.25);
%  w = spec2wave(S,opt)

% opt = simoptset;
% opt = simoptset(opt,'dt',0.25,'dx',0.25);
% w = spec2wave(S,opt);
% w = spec2wave(SD12);

%  =============================================================================== #
% Gera campo de onda

% rng('default'); clf
% opt = simoptset('Nt',20,'dt',1,'Nu',1024,'du',1,'Nv',512,'dv',1)
% W12 = spec2field(SD12, opt)

% figure(1); clf
% Movie12 = seamovie(W12,1,'GaussianSea12.avi')

%  =============================================================================== #
% SEASIM Spectral simulation of a Gaussian sea, 2D (x,t) or 3D (x,y,t)

%  CALL:  [Y, Mv]=seasim(spec,Nx,Ny,Nt,dx,dy,dt,fftdim,plotflag)

%        Y    = output struct with simulated path
%        Mv   = movie of output (run with movie(Mv))
%        spec = spectrum struct, must be two-dimensional spectrum
%        Nx,Ny,Nt = number of points in grid. Put Ny=0 for 2D simulation
%                   (default 2^7)
%        dx,dy,dt = steps in grid (default dx,dt by the Nyquist freq, dy=dx)
%        fftdim   = 1 or 2 gives one- or two dimensional FFT. (default 2) 
%                   If 1 then FFT over t and looping over x and y.
%                   If 2 then FFT2 over x and y, looping over t. 
%        plotflag = 0,1 or 2. If 0 no plot, if 2 movie (takes a couple of min.) 
%                   if 1 single (first) frame of movie (default 0)
                
%  The output struct contains:
%           .Z matrix of size [Ny Nx Nt], but with singleton dimensions removed 
%           .x, .t (and .y if Ny>1)  
%  For the removal of singleton dimensions, see SQUEEZE.

%  The output movie can also be created separately by calling SEAMOVIE.
%  Then can also different plot styles be chosen for the movie. The style
%  used here is a surf-plot.  

%  Limitations: memory demanding! fftdim=2 is in general better.
%  When fftdim=1 and NX*NY is large (the limit depends on spectrum, dt etc.) 
%  then a slower version with more looping is used. This version can be 
%  forced by putting fftdim to something greater than 2, then fftdim will equal
%  the number of extra loops. Try this after an interrupt by 'Out of Memory'. 

%  If the spectrum has a non-empty field .tr, then the transformation is 
%  applied to the simulated data, the result is a simulation of a transformed
%  Gaussian sea.

%  Example: % Simulate using demospec, plot the first frame 
%   Nx = 2^7; Ny = 2^7; Nt = 100; dx = 10; dy = 10;dt = 1;
%   S = demospec('dir');
%   plotflag = 1;
%   use_waitbar = 0;
%   Y=seasim(S,Nx,Ny,Nt,dx,dy,dt,2,plotflag,use_waitbar);  

% Nx = 1;
% Ny = 1;
% Nt = 1024;
% dx = 1;
% dy = 1;
% dt = 0.5;

% Nx = 1;
% Ny = 1;
% Nt = 2^14;
% dx = 1;
% dy = 1;
% dt = 0.5;

% Nx = 3;
% Ny = 2;
% Nt = 2^14;
% dx = 10;
% dy = 10;
% dt = 0.5;
% plotflag = 0;
% use_waitbar = 0;
% F = seasim(SD12, Nx, Ny, Nt, dx, dy, dt, 1, plotflag, use_waitbar); 

%  =============================================================================== #
% DAT2DSPEC Estimates the directional wave spectrum from timeseries 

% CALL: [S, D, Sw,Fcof] = dat2dspec(W,pos,h,Nfft,Nt,method,options);

%       S = a spectral density structure containing:
%           S      = 2D array of the estimated directional spectrum, size Nt x Nf. 
%           w      = frequency vector  0..2*pi*Nyquistfrequency of length Nf
%           theta  = angle vector -pi..pi of length Nt 
%                    (theta = 0 -> + x-axis, theta = pi/2 -> + y-axis) 
%           h      = water depth 
%                    ( S.S=D.S.*Sw.S(:,ones(:,Nt))' )
%      D  = estimate of spreading function as function of theta and w
%      Sw = angular frequency spectrum
%    Fcof = Fourier coefficients of the spreading function D(w,theta)
%           defined as int D(w,theta)*exp(i*n*theta) dtheta. n=0:nharm
%           size nharm+1 x Nf

%      W  = [t w1 w2 ... wM]  a M+1 column data matrix with sampled times 
%           and values in column 1 and column 2 to M+1, respectively.
%     pos = [x y z def bfs], matrix characterizing instruments and positions, size M x 5
%           x(j), y(j),z(j) = the coordinate positon of the j-th sensor (j=1:M)
%           def(j) = identifying parameter (1,2,... or 18) for the j-th time series  
%                    (See tran for options)
%           bfs(j) = 1, if j-th time series is to be used in final estimate of 
%                       "Best" Frequency Spectra.
%                    0, if j-th is to be excluded. (At least one must be set to 1)
%      h  = water depth (default is deep water,i.e., h = inf)
%    Nfft = length of FFT  (determines the smoothing and number of
%           frequencies, Nf = Nfft/2+1) (default 256)
%      Nt = number of angles (default 101)
%  method = 'BDM'  Bayesian Directional Spectrum Estimation Method 
%           'MLM'  Maximum Likelihood Method (default)
%           'IMLM' Iterative  Maximum Likelihood Method 
%           'MEM'  Maximum Entropy Method   (slow)
%           'EMEM' Extended Maximum Entropy Method
% options = optional options, see specoptset for details.
% Example:
% S  = jonswap;
% D  = spreading(linspace(-pi,pi,51),'cos2s');
% Sd = mkdspec(S,D,1);
% Nx = 3; Ny = 2; Nt = 2^14; dx = 10; dy = 10;dt = 0.5;
% plotflag = 0;
% use_waitbar = 0
% F = seasim(Sd,Nx,Ny,Nt,dx,dy,dt,1,plotflag, use_waitbar); 
% Z  = permute(F.Z,[3 1 2]);
% [X,Y] = meshgrid(F.x,F.y);
% N = Nx*Ny;
% types = repmat(sensortypeid('n'),N,1);
% bfs   = ones(N,1);
% pos   = [X(:),Y(:),zeros(N,1)];
% h = inf;
% Se = dat2dspec([F.t Z(:,:)],[pos types,bfs],h,256,101); % seasim is possibly wrong

% Z  = permute(F.Z, [3 1 2]);
% [X, Y] = meshgrid(F.x,F.y);
% N = Nx * Ny;
% types = repmat(sensortypeid('n'), N, 1);
% bfs = ones(N,1);
% pos = [X(:),Y(:), zeros(N,1)];
% Se = dat2dspec([F.t Z(:,:)], [pos types, bfs], h, 256, 101); % seasim is possibly wrong


% Nx = 3; Ny = 2; Nt = 2^14; dx = 10; dy = 10;dt = 0.5;


% h = 200
% opcoes = specoptset('dat2dspec');
% opcoes.nharm = 2;
% opcoes.gravity = 9.8063;
% opcoes.wdensity = 1.0278e+003;
% opcoes.bet = -1; % direcao para onde a onda vai
% opcoes.igam = 1;
% opcoes.x_axisdir = 90; % referencia para onde o eixo das abcissas aponta em termos de azimute
% opcoes.y_axisdir = 0; % referencia para onde o eixo das ordenadas aponta em termos de azimute
% opcoes.plotflag = 'off';
% opcoes.dflag = 'mean';
% opcoes.ftype = 'f';
% opcoes.maxiter = 135;
% opcoes.noverlap=floor(NFFT/2); % faz muta diferenca no calculo da direcao e um pouco no da frequencia
% method = 'EMEM';

Nang = 101; % numero de angulos
Nx = 3;
Ny = 3;
Nt = 2^14;
dx = 10;
dy = 10;
dt = 1;
plotflag = 0;
use_waitbar = 0;
h = inf;
NFFT = Nt / 24;

F = seasim(SD, Nx, Ny, Nt, dx, dy, dt, 1, plotflag, use_waitbar); 

% types = repmat(sensortypeid('n'),N,1);
% types = [1, 4, 6]
% bfs   = ones(N,1);
% pos   = [X(:),Y(:),zeros(N,1)];
% pos = [[0,0,0]', [1,0,0]', [2,0,0]', [1,1,1]', [1,1,1]'];

% W = [F.t, F.Z'];
% types = repmat(sensortypeid('n'),N,1);
% bfs   = ones(N,1);
% pos   = [X(:),Y(:),zeros(N,1)];
% h = inf;


Z  = permute(F.Z, [3 1 2]);
[X,Y] = meshgrid(F.x,F.y);
W = Z(:,:);
W1 = [F.t, W(:,1:3:end)];
pos = [[20, 0, 0]; [10, 0, 0]; [0, 0, 0]];
types = [1, 1, 1]';
bfs = [1, 0, 0]';

[Se, D, Sw, Fcof] = dat2dspec(W1, [pos, types, bfs]);

figure
plotspec(SD), hold all
plotspec(Se,'r-.'), hold off
shg

%  =============================================================================== #
% Calculo do espectro direcional utilizando os dados simulados na geraonda.m

% h = 200
% NFFT = 128;
% Nt = 360; % numero de angulos
% opcoes = specoptset('dat2dspec');
% % opcoes.nharm = 2;
% % opcoes.gravity = 9.8063;
% % opcoes.wdensity = 1.0278e+003;
% opcoes.bet = -1; % direcao para onde a onda vai
% % opcoes.igam = 1;
% % opcoes.x_axisdir = 90; % referencia para onde o eixo das abcissas aponta em termos de azimute
% % opcoes.y_axisdir = 0; % referencia para onde o eixo das ordenadas aponta em termos de azimute
% opcoes.plotflag = 'off';
% opcoes.dflag = 'mean';
% opcoes.ftype = 'f';
% % opcoes.maxiter = 135;
% opcoes.noverlap=floor(NFFT/2); % faz muta diferenca no calculo da direcao e um pouco no da frequencia
% method = 'EMEM';
% pos = [[0,0,0]', [0,0,0]', [0,0,0]', [1,4,5]', [1,0,0]'];

% [S, D, Sw, Fcof] = dat2dspec(W, pos, h, NFFT, Nt, method, opcoes);
% % S = dat2dspec(W, pos, h, NFFT, Nt, method, opcoes);

% % Se = dat2dspec([F.t Z(:,:)], [pos types, bfs], h, 256, 101); % seasim is possibly wrong
% plotspec(S), hold all
% plotspec(Se), hold off
% shg

% Nx = [];
% Ny = [];
% Nt = []];
% dx = 10;
% dy = 10;
% dt = 0.5;
% h = inf;

% [Y, Mv]=seasim(spec, Nx, Ny, Nt, dx, dy, dt, fftdim, plotflag)

% [F, Mv] = seasim(SD12, Nx, Ny, Nt, dx, dy, dt, 1, plotflag, use_waitbar); 

%  =============================================================================== #
% TRAN Computes transfer functions based on linear wave theory
%      of the system with input surface elevation, 
%      eta(x0,y0,t) = exp(i*(kx*x0+ky*y0-w*t)), 
%      and output Y determined by type and pos. 

%  CALL:  [Hw Gwt kw Hwt] = tran(w,theta,pos,type,h,g,rho,bet,igam,thx,thy,kw);

%    Hwt = Hw(ones(Nt,1),:).*Gwt matrix of transfer functions values as function of 
%          w (columns) and theta (rows)                   size Nt x Nf 
%    Hw  = a function of frequency only (not direction)   size  1 x Nf
%    Gwt = a function of frequency and direction          size Nt x Nf
%      w = vector of angular frequencies in Rad/sec. Length Nf
%  theta = vector of directions in radians           Length Nt   (default 0)
%          ( theta = 0 -> positive x axis theta = pi/2 -> positive y axis)
%    pos = [x,y,z] = vector giving coordinate position relative to [x0 y0 z0] (default [0,0,0])
%   type = Number or string defining the sensortype or transfer function in output. 
%          1,  'n'    : Surface elevation              (n=Eta)     (default)
%          2,  'n_t'  : Vertical surface velocity
%          3,  'n_tt' : Vertical surface acceleration
%          4,  'n_x'  : Surface slope in x-direction 
%          5,  'n_y'  : Surface slope in y-direction
%          6,  'n_xx' : Surface curvature in x-direction
%          7,  'n_yy' : Surface curvature in y-direction
%          8,  'n_xy' : Surface curvature in xy-direction
%          9,  'P'    : Pressure fluctuation about static MWL pressure 
%          10, 'U'    : Water particle velocity in x-direction
%          11, 'V'    : Water particle velocity in y-direction
%          12, 'W'    : Water particle velocity in z-direction
%          13, 'U_t'  : Water particle acceleration in x-direction
%          14, 'V_t'  : Water particle acceleration in y-direction
%          15, 'W_t'  : Water particle acceleration in z-direction
%          16, 'X_p'  : Water particle displacement in x-direction from its mean position
%          17, 'Y_p'  : Water particle displacement in y-direction from its mean position
%          18, 'Z_p'  : Water particle displacement in z-direction from its mean position
%          19, 'Dummy': Transfer function is zero
%     h  = water depth      (default inf) 
%     g  = acceleration of gravity (default see gravity)
%    rho = water density    (default see wdensity)
%    bet = 1, theta given in terms of directions toward which waves travel (default)
%         -1, theta given in terms of directions from which waves come 
%   igam = 1, if z is measured positive upward from mean water level (default)
%          2, if z is measured positive downward from mean water level
%          3, if z is measured positive upward from sea floor
%    thx = angle clockwise from true north to positive x-axis in degrees
%          (default 90)
%    thy = angle clockwise from true north to positive y-axis in degrees
%          (default 0)
%     kw = vector of wave numbers corresponding to angular frequencies, w
%          (default calculated with w2k)
%  Example:
%    N=5000;dt=0.4;f0=0.1;th0=0;h=50; w0 = 2*pi*f0;
%   t = linspace(0,1500,N)';
%   types = [1 4 5];
%   bfs   = [1 0 0];
%   pos   = zeros(3,3);
%   eta0 = exp(-i*w0*t);
%   [Hw Gwt] = tran(w0,th0,pos(1,:),'n',h); 
%   eta = real(Hw*Gwt*eta0)+0.001*rand(N,1);
%   [Hw Gwt] = tran(w0,th0,pos(2,:),'n_x',h); 
%   n_x = real(Hw*Gwt*eta0)+0.001*rand(N,1);
%   [Hw Gwt] = tran(w0,th0,pos(3,:),'n_y',h); 
%   n_y = real(Hw*Gwt*eta0)+0.001*rand(N,1);
%   S = dat2dspec([t eta n_x n_y],[pos types',bfs'],h,256,101);
%   plotspec(S)

% % N=5000;
% % dt=0.4;
% f0=0.1;
% th0=0;
% % h=50;
% w0 = 2*pi*f0;
% h = 200;

% % t = linspace(0,1500,N)';
% t = xs(:,1);

% types = [1 4 5];
% bfs   = [1 0 0];
% pos   = zeros(3,3);
% % eta0 = exp(-i*w0*t);
% eta0 = xs(:,2);

% [Hw Gwt] = tran(w0,th0,pos(1,:),'n',h); 
% eta = real(Hw*Gwt*eta0)+0.001*rand(N,1);

% [Hw Gwt] = tran(w0,th0,pos(2,:),'n_x',h); 
% n_x = real(Hw*Gwt*eta0)+0.001*rand(N,1);

% [Hw Gwt] = tran(w0,th0,pos(3,:),'n_y',h); 
% n_y = real(Hw*Gwt*eta0)+0.001*rand(N,1);

% S = dat2dspec([t eta n_x n_y],[pos types',bfs'],h);
% plotspec(S)
