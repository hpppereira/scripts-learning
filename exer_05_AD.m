% 
% exercicio #05
%
% Exemplo sobre Análise de Fourier
% solucao do problema apresentado no excelente
% `data analysis methods in physical oceanography`
% emery & thomson (pag 387 na 1a edicao)
% dados de TSM
%
% nelson violante-carvalho
% n_violante@oceanica.ufrj.br
% https://sites.google.com/site/nviolantecarvalho/
%
% Introdução à Análise de Sinais para Oceanógrafos 
% (e demais interessados no oceano)
% em exer_05.pdf estao descritas as equacoes usadas no exercicio
% Programa de Pos-Graduacao em Engenharia Oceanica
% PENO COPPE UFRJ
%
% 2o PERIODO 2015
%

clear, close all

% Considere a seguinte série temporal abranjendo dois anos de valores médios mensais da Temperatura da Superfície do Mar (TSM). Cada valor mensal é obtido pela média de valores diários obtidos em torno do meio dia.

temp=[7.6 7.4 8.2 9.2 10.2 11.5 12.4 13.4 13.7 11.8 10.1 9.0 8.9 9.5 10.6 11.4 12.9 12.7 13.9 14.2 13.5 11.4 10.9 8.1];

% Formulação Matemática pare Séries Temporais Discretas

% Consideraremos que a série temporal da TSM, y(t), seja determinada em pontos discretos definidos por amostragem com espaçamento delta_t. Uma vez que ela tem duração T, teremos um total de N=T/delta_t intervalos de amostragem e N+1 pontos localizados em y(tn)=y(n delta_t) para (n=0,1,...N). Portanto temos N valores nos tempos tn=t1,t2,...tN. Os coeficientes de Fourier são definidos através dos seguintes somatórios (ver nota de aula)

N=length(temp);
n=1:N;
p=1:N/2;

a0=2/N*sum(temp); % eq 1 na nota de aula

% uma dica para a resolucao do problema
% os termos `cos` e `sin` quando p=1 ficam
% cos1=cos(2*pi*n/N);
% sen1=sin(2*pi*n/N);

% com os coeficientes quando p=1 ficando
% a1=2/N*sum(temp.*cos1);
% b1=2/N*sum(temp.*sen1);

% Os coeficientes da Série de Fourier são obtidos multiplicando-se a série temporal yn por funções seno e cosseno múltiplas da freqüência fundamental 1/T.

% Portanto na série temporal em questão N=24, n varia de 1 a 24 e p varia de 0 a 12.

% faca um loop para calcular todos os coeficientes
% primeiro crie uma matriz de zeros para cos_p e sin_p
cos_p=zeros(length(p),length(n));
sen_p=zeros(length(p),length(n));

% agora faca o loop variando o valor de p (use o que foi apresentado
% acima como modelo)
% vc vai empregar as eqs 2 e 3 na nota de aula
%
% usando 
% subplot(4,1,1), subplot(4,1,2), subplot(4,1,3) e subplot(4,1,4)
% plote a serie original (no topo), seguida da frequencia fundamental,
% do segundo e do terceiro harmonicos respectivamente
figure(1)

% compare a serie de TSM original com a recuperada usando os 3 1as
% componentes de fourier (ou seja, somando as 3 1as componentes)
% eq 4 na nota de aula
figure(2)

% plote o espectro de amplitude de cada componente
% veja nota de aula
figure(3)

