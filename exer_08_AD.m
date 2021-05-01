% 
% exercicio #08
% Filtro
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
% precisa do arquivo 92051522.DAT

% usando dados de um ondografo fundeado na Bacia de Campos
% carregue o arquivo 92051522.DAT
%
clear, clc, close all

dados=load('92051522.DAT');
eta=dados(:,2)';

T=1;  % taxa de amostragem
N=length(eta);  % 1024 pontos ~17 min

% freq do filtro f1 e f2
f1=0.09; f2=0.10;

% vetor tempo t
t=...

% plote serie temporal
figure;
plot

% computando o spec
S=...

% computando vetor de freq
f=...

% plotando spectro de amplitude
figure
subplot(2,1,1)
plot

% vamos gerar um filtro H
% tem valor 1 para as freqs que queremos que passe
% e zero para as que serao filtradas

% 1o criando um vetor com zeros
% help zeros
H=...

% e com valor um para as freq entre f1 e f2
H(find(....

% repare que precisamos fazer o mesmo para as freq negativas, 
% sendo simetrico em relacao a origem
% significa dar o valor um para as freq entre 1/T-f2 e 1/T-f1
H(find(f>=....

% plotando o filtro
subplot(2,1,2)
plot(f,H,'r')

% aplicando o filtro, simplesmente multiplicando S por H
S_filt=....

% voltando para o dominio do tempo, com a transformada inversa
% help ifft
eta_filtrado=ifft....

% melhor ainda, considere somente a parte real, devido a ruido numerico
eta_filtrado=real(eta_filtrado);

% plote a nova serie filtrada
figure
plot(t,eta_filtrado,'-g',t,eta_filtrado,'.');
xlabel('tempo (s)'); ylabel('altura (m)')
axis('tight')

