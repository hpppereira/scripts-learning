%%%% Rotina de Análise de Dados de Onda no Domínio do Tempo %%%%
% Esta rotina cria umas matriz 'dados 5x6' onde estão os valores 
% de [hs hmax thmax tz tcc epsilont], e cada linha indica uma bateria 
% de teste, mudando apenas os período. A elevação é cte de 0.15 m (150 mm).
format bank
load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000100_Convertido.gin.mat');
% T=1s
a=WAVE1A;   %chama vetor de elevacao
dt=tempo(2)-tempo(1);   %intervalo de amostragem

dados(1,:)=ondatempo(a,dt);

load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000200_Convertido.gin.mat');
%T=1.7s
a=WAVE1A;   %chama vetor de elevacao
dt=tempo(2)-tempo(1);   %intervalo de amostragem

dados(2,:)=ondatempo(a,dt);

load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000300_Convertido.gin.mat');
% T=2.4s
a=WAVE1A;   %chama vetor de elevacao
dt=tempo(2)-tempo(1);   %intervalo de amostragem

dados(3,:)=ondatempo(a,dt);

load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000400_Convertido.gin.mat');
% T=3.1s
a=WAVE1A;   %chama vetor de elevacao
dt=tempo(2)-tempo(1);   %intervalo de amostragem

dados(4,:)=ondatempo(a,dt);

load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000500_Convertido.gin.mat');
% T=3.8s
a=WAVE1A;   %chama vetor de elevacao
dt=tempo(2)-tempo(1);   %intervalo de amostragem

dados(5,:)=ondatempo(a,dt);


