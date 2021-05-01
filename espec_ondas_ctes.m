clear,clc
% Rotina que cria vetor de elevação e de tempo para ondas ctes, ou seja,
% quando elas já atigiram a Hmax. No caso, a partir de 139,04 seg (linha
% 3477) até 180 seg (linha 4500), sendo 1024 registro (2^10). Faz um plot 
% dessas ondas para os diferentes periodos.
% Roda a rotina ESPEC.m para 'x=w1 (onda cte ' e dt=0.04, e cria o vetor
% de auto espectro da componente x. E faz o grafico 


load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000100_Convertido.gin.mat');
% T=1s
w1=WAVE1A(3477:4500);   %vetor de elevação
t1=tempo(3477:4500);   %intervalo de amostragem


load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000200_Convertido.gin.mat');
%T=1.7s
w2=WAVE1A(3477:4500);   %vetor de elevação
t2=tempo(3477:4500);   %intervalo de amostragem


load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000300_Convertido.gin.mat');
% T=2.4s
w3=WAVE1A(3477:4500);   %vetor de elevação
t3=tempo(3477:4500);   %intervalo de amostragem


load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000400_Convertido.gin.mat');
% T=3.1s
w4=WAVE1A(3477:4500);   %vetor de elevação
t4=tempo(3477:4500);   %intervalo de amostragem


load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000500_Convertido.gin.mat');
% T=3.8s
w5=WAVE1A(3477:4500);   %vetor de elevação
t5=tempo(3477:4500);   %intervalo de amostragem

dados=[t1 w1 w2 w3 w4 w5];

%Plot Gráfico com ondas ctes
% hold on
% 
%  plot(t1,w1,'y');  %período 1.0s
figure (1) 
plot(t2,w2,'m');  %período 1.7s
%  plot(t3,w3,'c');  %período 2.4s
%  plot(t4,w4,'r');  %período 3.1s
%  plot(t5,w5,'g');  %período 3.8s
% 
% hold off


%Rodar a rotina ESPEC.m para w1

x=(dados(:,2));
dt=(dados(2,1)-dados(1,1));
        
[aa]=espec(x,dt);
autoespecx_w1=aa(:,2);

% Criar grafico de frequencia (eixo x) por autoespectro de x (eixo y).

figure (2) 

plot(aa(:,1),aa(:,2));  % eixo x em semilog

aaw1=aa;
title=('Periodo 1 segundo');
xlabel=('Frequencia');
ylabel=('Auto Espectro de x');

%Rodar a rotina ESPEC.m para w2

x=(dados(:,3));
dt=(dados(2,1)-dados(1,1));
        
[aa]=espec(x,dt);
autoespecx_w2=aa(:,2);


% Criar grafico de frequencia (eixo x) por autoespectro de x (eixo y).

figure (3)

plot(aa(:,1),aa(:,2));  % eixo x em semilog

aaw2=aa;

%Rodar a rotina ESPEC.m para w3

x=(dados(:,4));
dt=(dados(2,1)-dados(1,1));
        
[aa]=espec(x,dt);
autoespecx_w3=aa(:,2);

% Criar grafico de frequencia (eixo x) por autoespectro de x (eixo y).

figure (4)

plot(aa(:,1),aa(:,2));  % eixo x em semilog

aaw3=aa;

%Rodar a rotina ESPEC.m para w4

x=(dados(:,5));
dt=(dados(2,1)-dados(1,1));
        
[aa]=espec(x,dt);
autoespecx_w4=aa(:,2);

% Criar grafico de frequencia (eixo x) por autoespectro de x (eixo y).

figure (5)

plot(aa(:,1),aa(:,2));  % eixo x em semilog

aaw4=aa;

%Rodar a rotina ESPEC.m para w5

x=(dados(:,6));
dt=(dados(2,1)-dados(1,1));
        
[aa]=espec(x,dt);
autoespecx_w5=aa(:,2);

% Criar grafico de frequencia (eixo x) por autoespectro de x (eixo y).

figure (6)

plot(aa(:,1),aa(:,2));  % eixo x em semilog

aaw5=aa;

clear aa