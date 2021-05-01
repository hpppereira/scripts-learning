% 
% exercicio #07
% exemplos de espectros
%
% nelson violante-carvalho
% n_violante@oceanica.ufrj.br
% https://sites.google.com/site/nviolantecarvalho/
%
% Introducao a Analise de Sinais para Oceanografos 
% (e demais interessados no oceano)
%
% Programa de Pos-Graduacao em Engenharia Oceanica
% PENO COPPE UFRJ
%
% 2o PERIODO 2015
%
%
clear, clc, close all

% periodo de amostragem
T= 0.1;    % fs=10 Hz

% vetor tempo
t=0:T:9.9;

% num amostras
N=length(t);   % N=100

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% 1o exemplo - funcao retangular
s=zeros(size(t));
s([1:11 91:100])=1;

% plote a funcao vs tempo
figure;plot

% plote espectro
plot_spec(s,T)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 2o exemplo - constante

s=ones....

% plote funcao no tempo
figure;plot

% plote espectro

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 3o exemplo - delta de Dirac
% zero em todos os pontos com excecao de um único
% mude a posicao do ponto diferente de zero

s=zeros(size(s));
s(1)=1;
%
% plote funcao no tempo
figure;plot

% plote espectro

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 4o exemplo - exp(t^2)

t1=-5:.1:4.9;
s=exp(-t1.^2);
s=s([51:100 1:50]);

% plote funcao no tempo
figure;plot

% plote espectro

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 5o exemplo - funcao exp(t^2) deslocada em relacao ao exercicio anterior

t1=-5:.1:4.9;
s=exp(-t1.^2);
s=s([48:100 1:47]);

% plote funcao no tempo
figure;plot

% plote espectro

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 6o exemplo - funcao cosseno com fase igual a zero
% depois com leakage, p ex T0=2.3

T0=2.0;     
s=cos(....

% plote funcao no tempo
figure;plot

% plote espectro

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 7o exemplo - funcao cosseno com fase diferente de zero
T0=2.0;     
s=cos(....;

% plote funcao no tempo
figure;plot

% plote espectro



