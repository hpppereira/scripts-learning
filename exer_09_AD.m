% 
% exercicio #09
%
% Exemplo sobre a Transformada Wavelet Continua
%
% nelson violante-carvalho
% n_violante@oceanica.ufrj.br
% https://sites.google.com/site/nviolantecarvalho/
%
% Introdução à Análise de Sinais para Oceanógrafos 
% (e demais interessados no oceano)
%
%
% Programa de Pos-Graduacao em Engenharia Oceanica
% PENO COPPE UFRJ
%
% 2o PERIODO 2015
%
% obs.: necessita os arqs
% wt.m
% formatts.m
% ar1.m
% gammest.m
% parseArgs.m
% wavelet.m
% wave_bases.m
% wave_signif.m
% chisquare_inv.m


clear, close all

% insira valores
dt=1; % periodo de amostragem Delta_t (s)
N=400; % num de pontos do sinal
f=0:1/(N*dt):(N-1)/(N*dt); % vetor freq
f1=f-1/(2*dt);

% somatorio de ondas senoidais, cada uma com N pontos, de o nome de w1
% freqs: 0.02 Hz (50s), 0.05 Hz (20s), 0.1 Hz (10s) e 0.25 Hz (4s)
w_1=50;
w_2=20;
w_3=10;
w_4=4;
w1= w_1+ w_2 + w_3 + w_4;

% computando a sua FFT

% plote a serie temporal e sua FFT


%%%%%

% ondas senoidais em intervalos de N/4 pontos, de o nome de w2
% freqs: 0.02 Hz (50s), 0.05 Hz (20s), 0.1 Hz (10s) e 0.25 Hz (4s)
w_1=50;
w_2=20;
w_3=10;
w_4=4;
w2=[w_1 w_2 w_3 w_4];


% plote a serie temporal e a FFT


%%%%%%
% compute a CWT de w1
figure

d1(:,1)=1:length(w1); % poderia ser o vetor tempo
d1(:,2)=w1;
wt(d1)

% compute a CWT de w2
figure

d2(:,1)=1:length(w2); % 
d2(:,2)=w2;
wt(d2)


