% 
% exercicio #01
% Funcoes de Autocorrelacao
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
%
%
% gerar uma série aleatoria com 128 pontos denominada de a
% normalmente distribuida com media zero e desvio padrao 0.3
a=normrnd(0,.3,128,1);
% gere uma funcao cosseno (denominada de 'b') com 128 pontos de amplitude 1, freqüência 0.1 e dt = 1s --> w=2*pi*f
b=1*cos(2*pi*0.1.*(1:128))';
%
% calcule a media, desvio padrao e variancia de 'a'
% 
% plote o histograma de 'a' com a distribuicao normal sobreposta
% help histfit
% --------------------
% Gráficos das séries
% --------------------
% empregando o comando subplot, plote na parte superior da figura a serie 'a' e na parte inferior a serie 'b'
% help plot, xlabel, ylabel, title, legend, subplot
figure
subplot(211)
subplot(212)

% Series para autocorrelacao
% Mais quatro series para analisar
c=a+10.*b;
d=a+b;
e=a+0.1.*b;
f=a+0.01.*b;

% -----------------------------------------------------------------------------
% Calcular e plotar as funcoes de autocorrelacao das series 
% -----------------------------------------------------------------------------
% veja o comando autocorr
% help autocorr
% usando subplot, plote na parte de cima da figura a serie 'b' e na parte inferior sua autocorrelacao
figure
subplot(211)
subplot(212)

% idem para a serie 'c'
figure
subplot(211)
subplot(212)

% idem para a serie 'd'
figure
subplot(211)
subplot(212)

% idem para a serie 'e'
figure
subplot(211)
subplot(212)

% idem para a serie 'f'
figure
subplot(211)
subplot(212)
%
%
% gerar uma série aleatoria com 138 pontos denominada de w
% normalmente distribuida com media zero e desvio padrao 0.3
w=normrnd(0,.3,138,1);
% ---------------------------------------------------------------------------
% Calcular e plotar a correlacao cruzada entre as series w(11:138) e w(1:128)
% 
% veja o comando crosscorr
% help crosscorr
%
%
% usando subplot, plote na parte de cima da figura w(11:138) juntamente com w(1:128). Na parte inferior a correlacao de w(11:138) com w(1:128)
figure
subplot(211)
subplot(212)



