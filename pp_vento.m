clear, clc, close all
dados=load('vento.txt')

[sai,sai2]=veldirparauv(dados(:,3),dados(:,4));

figure
z=1; %Tamanho do vetor
quiver(dados(1:697,2),dados(1:697,1),sai(1:697),sai2(1:697),z)
title('Ventos - Junho 2011'),xlabel('Horas'),ylabel('Dias'),axis tight

figure
z=1; %Tamanho do vetor
quiver(dados(698:1441,2),dados(698:1441,1),sai(698:1441),sai2(698:1441),z)
title('Ventos - Julho 2011'),xlabel('Horas'),ylabel('Dias'),axis tight

figure
z=1; %Tamanho do vetor
quiver(dados(1442:2181,2),dados(1442:2181,1),sai(1442:2181),sai2(1442:2181),z)
title('Ventos - Agosto 2011'),xlabel('Horas'),ylabel('Dias'),axis tight

figure
% Para outra convenção, trocar 'meteo' por 'oceano'
wind_rose1(dados(1:697,4),dados(1:697,3),'dtype','meteo') 
figure
wind_rose1(dados(698:1441,4),dados(698:1441,3),'dtype','meteo')
figure
wind_rose1(dados(1442:2181,4),dados(1442:2181,3),'dtype','meteo')


