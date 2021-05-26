clear,clc, close all
%Dados de corrente da TEPORI

%% Carregar os dados de pressao, temp...(arquivo.sen) - press�o na coluna 14
%Formato: Mes/Dia/Ano/Hora/Min/Seg
dados=load('pf420110610.sen');

%% Cria vetor de tempo em dias julianos
%Dados de entrada: Ano/Mes/Dia/Hora/Min/Seg

% ano=dados(:,3);
% mes=dados(:,1);
% dia=dados(:,2);
% hora=dados(:,4);
% minuto=dados(:,5);
% seg=dados(:,6);

% [j]=julian(ano,mes,dia,hora,minuto,seg);

%% Acha os m�ximos e minimos do nivel (pelo sensor de pressao)

dados=dados(find(dados(:,14)>1),:);

pr=dados(:,14);
pr_max=max(pr);
pr_min=min(pr);

% Como a profundidade minima � 15 metros, e o blank = 0.45 metros. As 32
% primeiras c�lulas que ficam sempre em baixo da �gua.
numcel=pr_min/2;
%% Carregar dados de velocidade U e V
% Entrar com a matriz no formato: linhas=amostras / colunas=c�lulas

u=load('pf420110610.v1');
v=load('pf420110610.v2');

%% Chama subrotina para passar u e v em velocidade e dire��o M�DIA

[vel,dire]=uvparaveldir(u,v); 

%15 min = 1 amostra
%1 hora = 4 amostras
%1 semana = 672 amostras

%Sa�da da rotina 'uvparaveldir' matriz velocidade (linhas=celulas / colunas=amostras)
%Escolher a quantidade de celulas na variavel 'cel' amostras na vari�vel 'tempo'
tempo=linspace(min(dados(:,4)),max(dados(:,4)),length(pr));
%tempo=1:length(pr);
cel=linspace(0,-pr_min,numcel);
vel1=vel(1:length(cel),13:length(vel));

% %% Chama arquivo de mar� da marinha (teste)
% mare=load('C:\Users\Henrique\Est�gio\Porto_Itajai\Teporti\mare.txt');

%Plot 1
figure (1)
subplot(3,1,1)
plot(tempo,pr), axis tight
title('ADCP - Bota fora 4 - 10/06/2011')
ylabel('Press�o (Db)')
subplot(3,1,2)
contourf(tempo,cel,vel1)
ylabel('Velocidade (m/s)')
subplot(3,1,3)
plot(tempo,dire(13:length(vel1))), axis tight, grid on
xlabel('Horas'),ylabel('Dire��o (graus)')

%% Chama subrotina para passar u e v em velocidade e dire��o PARA CADA C�LULA

% [velocidade,direcao]=transf_veldir(u,v);
% 
% velocidade=velocidade';
% direcao=direcao';

%Plot 2
% figure (2)
% subplot(3,1,1)
% plot(tempo,pr1), axis tight
% subplot(3,1,2)
% contourf(tempo,cel,velocidade(1:length(cel),1:length(tempo)))
% subplot(3,1,3)
% contourf(tempo,cel,direcao(1:length(cel),1:length(tempo))), grid on

%% Chama subrotina de Espectro rotat�rio

% % u1=u';
% % u1=mean(u1); %m�dia de todas as c�lulas
% % u1=u1(1:2048)'; %Potencia de 2
% % v1=v';
% % v1=mean(v1);
% % v1=v1(1:2048)';
% u1=u(1:2048,6); %a coluna indica a celula
% v1=v(1:2048,6);
% 
% deltat=15/(60*24); %Tempo em dias
% 
% [aa]=Especrot(u1,v1,deltat);
% 
% % Plot dos auto-espectros
% figure (3)
% 
% semilogx(aa(:,1),aa(:,2),'b'), hold on
% semilogx(aa(:,1),aa(:,3),'r'), hold off
% grid on
% axis tight
% title('Auto espectro das componentes U e V')
% xlabel('Frequ�ncia')
% ylabel('Energia')
% legend('Auto-espec U','Auto-espec de V')
% 
% % Plot do espectro total, hor�rio e anti hor�rio
% 
% figure (4)
% subplot(2,1,1)
% semilogx(aa(:,1),aa(:,6)), hold on
% semilogx(aa(:,1),aa(:,11),'r')
% semilogx(aa(:,1),aa(:,12),'r'), hold off
% legend('Espectro total','Limite de confian�a inferior','Limite de confian�a superior')
% title('Espectro total')
% axis tight, grid on
% subplot(2,1,2)
% semilogx(aa(:,1),aa(:,4)) %espectro hor�rio
% axis tight, grid on, hold on
% semilogx(aa(:,1),aa(:,5),'r') %espectro anti-hor�rio
% title('Espectro hor�rio e anti-hor�rio')
% xlabel('Frequ�ncia')
% legend('Espectro hor�rio','Espectro anti-hor�rio')
% 
% % Plot da dire��o da elipse, coef de rota��o, estabilidade da elipse e espectro total
% 
% figure (5)
% subplot(4,1,1)
% semilogx(aa(:,1),aa(:,6)), grid on
% title('espectro total'), axis tight
% subplot(4,1,2)
% semilogx(aa(:,1),aa(:,8)), grid on
% title('coeficiente de rota��o'), axis tight
% subplot(4,1,3)
% semilogx(aa(:,1),aa(:,9)), grid on
% title('dire��o da elipse'), axis tight
% subplot(4,1,4)
% semilogx(aa(:,1),aa(:,10)), grid on, hold on
% semilogx(aa(:,1),aa(:,13),'r'),hold off
% legend('Estabilidade da elipse','Limite de confian�a')
% title('estabilidade da elipse'), axis tight
% 



