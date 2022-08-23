% Calcula o autoespectro e o intervalo de confianca para uma serie real
% utilizando a funcao 'spectrum'
%
% Elaborado por Henrique P. P. Pereira (henriqueppp@gmail.com)
%
% Ultima modificacao: 05/11/2014
%
% Dados de entrada: x - serie real com 1024 pontos (ex: elevacao do mar)
%                   nfft - numero de segmentos para fft
%                   fs - frequencia de amostragem
%
% Dados de saida: matriz ss - col 1 - vetor de frequencia
%                             col 2 - autoespectro de x


function [aa]=spec(x,nfft,fs)

%intervalo de amostragem
dt = 1 / fs;

%frequencia de nysquit (frequencia de corte)
fny = 1 /(2 * dt);

%vetor de frequencia
aux = dt * nfft;
f = [1/aux:1/aux:fny]';

%auto-espectro
sp = spectrum(x,nfft,nfft/2,'welch');
sp = 2 * dt * sp(2:length(sp),1);

[aa]=[f sp];


