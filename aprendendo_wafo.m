%aprendendo o wafo
%seguindo o tutorial

clear,clc,close all

%iniciar o wafo (toolboxes)
% initwafo
initwafo('full',1,1)

%carrega dados de onda
eta = load('/home/hp/Google Drive/wafo/dados/onda.txt');

% ====================================================== %
%simulacao de spectro e estimacao do espectro

%parametros de onda
Hm0 = 6;
Tp = 8;
plotflag = 1;% o plotflag = 1 mostra a figura (0 nao mostra)

%gera espectro
figure
S1 = torsethaugen([],[Hm0 Tp],plotflag);

% gera serie temporal a partir do espectro (S1)
dt = 0.1; N = 2000;
xs = spec2sdat(S1,N,dt);
 
% figure
% se der erro, tem que mudar o nome no toolbox em data/wafologoNewWithoutBorder.png
%no linux: mv wafoLogoNewWithBorder.png wafologoNewWithoutBorder.png
waveplot(xs,'-',3)
 
% ====================================================== %
%comparison between estimates and calculated spectrum

plotflag = 1;
Fs = 4; %sampe frequency (hz)
dt = 1/Fs; %sample interval (s)
N = fix(20*60*Fs); %number of points
xs = spec2sdat(S1,N,dt);

%Sest = estimated spectrum
% 400 - lag size of the Parzen window
Sest = dat2spec(xs,400); 

figure

%plot torsethaugen spectrum
plotspec(S1,plotflag), hold on
%plot estimated spectrum
plotspec(Sest,plotflag,'--')
axis([0 3 0 5]), hold off

%Figura: Solid: original Thorsethaugen spectrum. Dashed: spectrum estimated
%from data (20 minutes of observations). Maximum lag size of the Parzen
%window = 400.

% ====================================================== %
%plotting histogram of period

% NIT = 3; %accuracy of calculate
% paramt = [0 10 51];
% dtyex = spec2tpdf(S1,[],'Tt',paramt,0,NIT);
% dtyest = spec2tpdf(Sest,[],'Tt',paramt,0,NIT);
[T, index] = dat2wa(xs,0,'d2u');
histgrm(T,25,1,1), hold on
% pdfplot(dtyex), pdfplot(dtyest,'-.')
axis([0 10 0 0.35]), hold off

% 
% figure
% 
% [T, index] = dat2wa(xs,0,'d2u');
% histgrm(T,25,1,1), hold on
% axis([0 10 0 0.35]), hold off
xlabel('Peak Period (s)')

% ====================================================== %
%directional spectrum

figure

plotflag = 1;
Nt = 101;% number of angles
th0 = pi/2; % primary direction of waves
Sp = 15; % spreading parameter

%spreading calculado pcom cos2s
D1 = spreading(Nt,'cos',th0,Sp,[],0); %frequency independent
D12 = spreading(Nt,'cos',0,Sp,S1.w,1); %frequency dependent
SD1 = mkdspec(S1,D1); SD12 = mkdspec(S1,D12);
plotspec(SD1,plotflag), hold on
plotspec(SD12,plotflag,'-.'), hold off

%Figure: Directional spectrum. The frequency spectrum is a Torsethaugen spectrum and the
% spreading function is of cos-2s type with s = 15. Solid line: directional spectrum with
% frequency independent spreading. Dash dotted line: directional spectrum, using frequency
% dependent spreading function.
 
% ====================================================== %
%simulated sea on 128m by 128m for sea with directional
%spectra SD1 and SD12. The routine seasim is used for
% simulation

plotflag = 1; iseed = 1; Nx = 2^8; Ny = Nx; Nt = 1;
dx = 0.5; dy = dx; dt = 0.25; fftdim = 2;
randn('state',iseed)

figure
subplot(1,2,1)
Y1 = seasim(SD1,Nx,Ny,Nt,dx,dy,dt,fftdim,plotflag);
randn('state',iseed)
subplot(1,2,2)
Y12 = seasim(SD12,Nx,Ny,Nt,dx,dy,dt,fftdim,plotflag);

% ====================================================== %
%Statistical extreme value analysis

figure

xn = load('yura87.dat'); subplot(2,1,1);
plot(xn(1:30:end,1)/3600,xn(1:30:end,2),'.')
title('Water level'), ylabel('m')
yura = xn(1:85500,2);
yura = reshape(yura,300,285);
maxyura = max(yura);
subplot(2,1,2)
plot(xn(300:300:85500,1)/3600,maxyura,'.')
xlabel('Time (h)'), ylabel('m')
title('Maximum 5 min water level')

%Figure: Water level variation in the Japan Sea from the data set yura87 and maxima over
% 5 minute periods.
% It is clear from the figures that there is a trend in the data, with decreasing spreading
% with time

% shows cumulative distribution and density of the fitted
% GEV distribution together with diagnostic plots of empirical and model quantiles. We see
% that the non-stationarity gives a very bad fit in the upper tail of the distribution. The fitted
% GEV has shape parameter 0.1, with a 95% confidence interval (0.01, 0.18)

figure

phat = fitgev(maxyura,'plotflag',1);

%Figure: Diagnostic plots of extreme value analysis of yura87 with GEV distribution.


% ====================================================== %

% Example : (Sea data) In this example we use a series with wave data sea.dat with time
% argument in the first column and function values in the second column. The data used in
% the examples are wave measurements at shallow water location, sampled with a sampling
% frequency of 4 Hz, and the units of measurement are seconds and meters, respectively. The
% file sea.dat is loaded into M ATLAB and after the mean value has been subtracted the data
% are saved in the two column matrix xx

figure

xx = load('sea.dat');
me = mean(xx(:,2));
sa = std(xx(:,2));
xx(:,2) = xx(:,2) - me;
lc = dat2lc(xx);
plotflag = 2;
lcplot(lc,plotflag,0,sa)

%alturas de zero crossing, comparando com distribuicao gaussiana

% The observed crossings intnsity compared with the theoretically expected for Gaussian
% signals

% Here me and sa are the mean and standard deviation of the signal, respectively. The vari-
% able lc is a two column matrix with levels in the first column and the number of upcrossing
% of the level in the second. In Figure 2.1 the number of upcrossings of xx is plotted and
% compared with an estimation based on the assumption that xx is a realization of a Gaussian
% sea

% ====================================================== %
% Calculate wave parameters?

T = max(xx(:,1))-min(xx(:,1));
f0 = interp1(lc(:,1),lc(:,2),0)/T;

% zero up-crossing frequency

tp = dat2tp(xx);
fm = length(tp)/(2*T);
alfa = f0/fm;

figure 

waveplot(xx,tp,'k-','*',1,1)
axis([0 2 -inf inf])


% ====================================================== %
% To find possible spurious points of the dataset use the following commands.

dt = diff(xx(1:2,1));
dcrit = 5*dt;
ddcrit = 9.81/2*dt*dt;
zcrit = 0;
[inds indg] = findoutliers(xx,zcrit,dcrit,ddcrit);

% ====================================================== %
% Calculate de power spectrum

figure

Lmax = 9500; %numero de subdivisoes?
%Lmax = 256;
S = dat2spec(xx,Lmax);
plotspec(S)

% ====================================================== %
% Spectral moments

[mom text] = spec2mom(S,4);
[sa sqrt(mom(1))];

% The vector mom now contains spectral moments m0 , m2 , m4 , which are the variances of the
% signal and its first and second derivative

figure

Lmax0 = 200; Lmax1 = 50;
S1 = dat2spec(xx,Lmax0);
S2 = dat2spec(xx,Lmax1);
plotspec(S1,[],'-.'), hold on
plotspec(S2), hold off

% Figure: Estimated spectra in the data set sea.dat with varying degree of smoothing.

% ====================================================== %
% compute the covariance for the unimodal spectral density
% S1 and compare it with estimated covariance in the signal xx.

figure

Lmax = 80;
R1 = spec2cov(S1,1);
Rest = dat2cov(xx,Lmax);
covplot(R1,Lmax,[],'.'), hold on
covplot(Rest), hold off

% ====================================================== %
%Spectral densities of sea data

% Example 2. (Different forms of spectra) In this example we have chosen a J ONSWAP spec-
% trum with parameters defined by significant wave height Hm0 = 7[m] and peak period Tp
% = 11[s]. This spectrum describes the measurements of sea level at a fixed point (buoy).

Hm0 = 7; Tp = 11;
spec = jonswap([],[Hm0 Tp]);
spec.note

% In order to include the space dimension, i.e. the direction in which the waves propagate,
% we compute a directional spectrum by adding spreading; see dashed curves in Figure

D = spreading(101,'cos2s',0,[],spec.w,1);
Sd = mkdspec(spec,D);

% Next, we consider a vessel moving with speed 10[m/s] against the waves. The sea mea-
% sured from the vessel will have a different directional spectrum, called the encountered direc-
% tional spectrum. The following code will compute the encountered directional spectrum and
% plot it on top of the original directional spectrum. The result is shown as the solid curves in
% Figure

figure

Se = spec2spec(Sd,'encdir',0,10);
plotspec(Se), hold on
plotspec(Sd,1,'--'), hold off

figure

%unidimensional spectrum
Sd1 = spec2spec(Sd,'freq');
Sd2 = spec2spec(Se,'enc');
plotspec(spec), hold on
plotspec(Sd1,1,'.'),
plotspec(Sd2), hold off
 
% We can see in Figure that the spectra spec and Sd1 are identical (in numerical sense),
% while spectrum Sd2 contains more energy at higher frequencies.
% A similar kind of question is how much the wave length differs between a longcrested
% J ONSWAP sea and a J ONSWAP sea with spreading. The wavenumber spectra for both cases
% can be computed by the following code, the result of which is shown Figure below.

figure

Sk = spec2spec(spec,'k1d');
Skd = spec2spec(Sd,'k1d');
plotspec(Sk), hold on
plotspec(Skd,1,'--'), hold off

% Figure : The frequency J ONSWAP spectrum compared with encountered frequency
% spectrum for heading sea speed 10 [m/s] (solid line). (b) The wave number spectrum for
% longcrested J ONSWAP sea (solid line) compared with wave number spectrum for J ONSWAP
% with spreading.
 
% Finally, we shall show how the J ONSWAP spectrum can be corrected for a finite depth,
% see [12]. The W AFO phi1 computes the spectrum for water of finite depth, here 20[m].

figure

plotspec(spec,1,'--'), hold on
S20 = spec;
S20.S = S20.S.*phi1(S20.w,20);
S20.h = 20;
plotspec(S20), hold off


% Standard J ONSWAP spectrum (dashed line) compared with the spectrum on finite
% depth of 20 [m] (solid line)
