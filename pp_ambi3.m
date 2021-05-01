%processamento dos dados de ondas de Mexilhao
%por enquanto so abre os arquivo .dat

clear,clc,close all

pathname = '/home/hp/Dropbox/lioc/ambid/dados/Mexilhao-axys_gx3_2014//gx3/';

% av_mat = dlmread([pathname,'TOA5_55915.microstrain_stbaclV.dat'],',',4,2)';

av = av_mat(:,100);
dt = 1; %intervalo de amostragem
%funcao iomega
dataout =  iomega(av, dt, 3, 1);