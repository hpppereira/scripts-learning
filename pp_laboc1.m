%programa para avaliacao de ondas na bacia de santos do cenpes para
%simulacao na mesa - tese do felipe
% as 2 series .mat enviadas pelo ze antonio estao iguais
%as series de heave foram cortadas em +- 0.3m

clear, clc, close all

%local de onda estao os dados
pathname = '/home/lioc/Dropbox/ensaios_laboc/dados';

%define arquivos a serem carregados
arq1 = [pathname,'/200807180959.HNE'];
arq2 = [pathname,'/200807182159.HNE'];

reg = 1312; %comprimento do registro
dt = 0.78; %intervalo de amostragem
gl = 32; %graus de liberdade

%carrega dados HNE, deixa com 1312 colunas
dado1 = carregaaxys_hne(arq1); dado1 = dado1(1:reg,:);
dado2 = carregaaxys_hne(arq2); dado2 = dado2(1:reg,:);

%cria variaveis que serao corrigidas
dado1c = dado1;
dado2c = dado2;

%correcao dos dados

%para os valores de heave maiores e menores que +-0.5, coloca +-0.5
dado1c(find(dado1(:,1)>0.5),1) = 0.5;
dado1c(find(dado1(:,1)<-0.5),1) = -0.5;
dado2c(find(dado2(:,1)>0.5),1) = 0.5;
dado2c(find(dado2(:,1)<-0.5),1) = -0.5;


%calcula os espectros da serie bruta e corrigida
sp1 = spec(dado1,dt,gl);
sp1c = spec(dado1c,dt,gl);


%figuras
% figure, hold all
% plot(dado1(:,1))
% plot(dado1(:,2))
% plot(dado1(:,3)), hold off
% 
% figure, hold all
% plot(dado1(:,1))
% plot(dado1(:,2))
% plot(dado1(:,3)), hold off

figure
subplot(2,2,1:2)
plot(dado1(:,1)), hold all
plot(dado1c(:,1)), hold all, axis('tight')
title('heave bruto e corrigido')
subplot(2,2,3)
plot(sp1(:,1),sp1(:,2),'b'), axis([0,sp1(end,1),0,0.6])
title('heave bruto')
subplot(2,2,4)
plot(sp1c(:,1),sp1c(:,2),'g'), axis([0,sp1(end,1),0,0.6])
title('heave corr')




