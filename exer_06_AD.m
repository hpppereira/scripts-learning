% 
% exercicio #06
%
% Exemplo da FFT da funcao exponencial
% ambas as solucoes analiticas e numericas
% sao apresentadas
%
% nelson violante-carvalho
% n_violante@oceanica.ufrj.br
% https://sites.google.com/site/nviolantecarvalho/
%
% Introdução à Análise de Sinais para Oceanógrafos 
% (e demais interessados no oceano)
%
% Programa de Pos-Graduacao em Engenharia Oceanica
% PENO COPPE UFRJ
%
% 2o PERIODO 2015
%
%

% exemplo 
% fç exponencial
%
% memória de cálculo
% f_N = 1/(2*dT) = 5Hz
% f = 1/T = 1/(N*dT) = 0.1Hz
% 2*f_N = 1/dT = N/(N*dT) ~ (N-1)/(N*dT) ~ 10Hz

clear all, close all

% periodo de amostragem (s), freq de 10 Hz
dT= 0.1;    

% vetor tempo
t=0:dT:9.9;
%t=0:dT:9.9;
N=length(t); % intervalos de amostragem
T=N*dT; % duração

% funcao de interesse
% assuma os valores 
beta=1;
alfa=1;
fun=beta*exp(-alfa*t);

% plote a funcao 'fun'
figure

% solução com matlab
% use o comando fft

% crie o vetor de frequencias


% plote o spec de amplitude
figure
subplot(2,1,1)

% plote o spec de fase (veja o comando 'angle')
subplot(2,1,2)

% parte real e imaginária da TF
figure
subplot(2,1,1)

subplot(2,1,2)


% agora a soluçao analítica
% ver solucao analitica nas notas de aula
% amplitude = beta / sqrt (alfa^2 + 2 pi f1)^2)
% fase = atan (-2 pi f1/alfa)
 
% plote a fase e a amplitude da solucao analitica e compare com a numerica
figure
subplot(2,1,1)
subplot(2,1,2)


