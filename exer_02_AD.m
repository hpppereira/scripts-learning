% 
% exercicio #02
% dominio do tempo
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
% precisa do arq 92051522.DAT
% dados de heave de um ondografo fundeado na Bacia de Campos
% intervalo de amostragem de 1s
% 1024 pontos (~17min)
%
% 
clear, clc, close all
%
eta=load('92051522.DAT'); eta=eta(:,2);
%
% plotar a serie completa e um pequeno trecho usando subplot
%
figure
subplot(211)
subplot(212)

%
% identifique as ondas individualmente ao longo da serie temporal.
% busque uma forma de identificar quando ocorre o cruzamento do eixo horizontal.
% uma possivel maneira é determinar quando a serie muda de sinal 
% (de positivo para negativo e vice versa) ao cruzar o eixo horizontal.
% calcule primeiro considerando o cruzamento do eixo de forma ascendente.
% 

% plote a posicao dos pontos de cruzamento do eixo horizontal para se certificar
figure

% compute as alturas (diferencas de elevacao) entre os pontos de cruzamento
% compute os periodos de cada onda; a duracao entre os pontos de cruzamento


% compute o valor RMS, medio, maximo e a media do terco das maiores ondas (ou seja a altura significativa Hs)
% encontrei respectivamente
% 2.8m, 2.5m, 6.3m e 3.8m
% confira se as relacoes obtidas pela distribuicao de Rayleigh relacionando Hs com H_medio, H_rms com H_medio, etc.. (ver slides) estao de acordo com seus resultados

% plote o diagrama de dispersao de alturas X periodos

% plote o histograma da elevacao eta juntamente com o ajuste da distribuicao Normal
% help histfit
figure


% plote o histograma de altura de ondas juntamente com o ajuste da distribuicao de Rayleigh
% help histfit
figure

% Repita todo o procedimento assumindo o cruzamento descendente do eixo horizontal. Compare seus resultados.



