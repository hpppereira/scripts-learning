%Calculo da altura significativa (Hs) e periodo significativo (Ts) de
%acordo com Kang(1982) e Seymour(1997)
%Autor: Henrique Patricio
%clear,clc

%Variaveis de entrada
%Profundidade (H)
H=input('Entre com a profundidade do local (m): ');
%Módulo da velocidade do vento (W) em m/s
W=input('Entre com a velocidade do vento (m/s): ');
%Comprimento de pista (F) em metros
F=input('Entre com o comprimento da pista (m): ');
%Aceleração da gravidade
g=9.81;

%Calculo da Hs
Hs=(W^2/g)*0.283*tanh(0.53*(g*H/(W^2))^0.75)*tanh((0.0125*(g*F/(W^2))^0.42)/(tanh(0.53*(g*H/(W^2))^0.75)));

%Calculo do Ts
Ts=(2*pi*W/g)*1.2*tanh(0.833*(g*H/(W^2))^0.375)*tanh((0.077*(g*F/(W^2))^0.25)/(tanh(0.833*(g*H/(W^2))^0.375)));

disp(['Hs=',num2str(Hs),'e Ts=',num2str(Ts)])

%Plotar a evolução da Hs e Ts em função da velocidade do vento (W1)
W1=linspace(0,200,1000);

for i=1:length(W1)
    Hs1(1,i)=(W1(1,i)^2/g)*0.283*tanh(0.53*(g*H/(W1(1,i)^2))^0.75)*tanh((0.0125*(g*F/(W1(1,i)^2))^0.42)/(tanh(0.53*(g*H/(W1(1,i)^2))^0.75)));
    Ts1(1,i)=(2*pi*W1(1,i)/g)*1.2*tanh(0.833*(g*H/(W1(1,i)^2))^0.375)*tanh((0.077*(g*F/(W1(1,i)^2))^0.25)/(tanh(0.833*(g*H/(W1(1,i)^2))^0.375)));
end

subplot(3,1,1)
plotyy(W1,Hs1,W1,Ts1)
[AX,H1,H2]=plotyy(W1,Hs1,W1,Ts1,'plot','plot');
set(get(AX(1),'Ylabel'),'String','Hs (m)') 
set(get(AX(2),'Ylabel'),'String','Ts (s)')
grid on
hold on
plot(W,Hs,'o')
%plot(W,Ts,'o')
xlabel('Velocidade do vento (m/s)') 
title(['Hs e Ts em função da velocidade do vento (Profundidade de ',num2str(H),' metros e comprimento de pista de ',num2str(F),' metros)']) 
hold off

%Plotar a evolução da Hs e Ts em função do comprimento de pista (F1)
F1=linspace(0,200000,1000);

for i=1:length(F1)
    Hs2(1,i)=(W^2/g)*0.283*tanh(0.53*(g*H/(W^2))^0.75)*tanh((0.0125*(g*F1(1,i)/(W^2))^0.42)/(tanh(0.53*(g*H/(W^2))^0.75)));
    Ts2(1,i)=(2*pi*W/g)*1.2*tanh(0.833*(g*H/(W^2))^0.375)*tanh((0.077*(g*F1(1,i)/(W^2))^0.25)/(tanh(0.833*(g*H/(W^2))^0.375)));
end

subplot(3,1,2)
plotyy(F1,Hs2,F1,Ts2)
[AX,H1,H2]=plotyy(F1,Hs2,F1,Ts2,'plot');
set(get(AX(1),'Ylabel'),'String','Hs (m)') 
set(get(AX(2),'Ylabel'),'String','Ts (s)') 
xlabel('Comprimento da pista (m)') 
title(['Hs e Ts em função do comprimento de pista (Profundidade de ',num2str(H),' metros e velocidade do vento de ',num2str(W),' m/s)']) 
hold on
grid on
plot(F,Hs,'ob')
%plot(F,Ts,'or')
hold off

%Plotar a evolução da Hs e Ts em função da profundidade (H1)
H1=linspace(0,500,1000);

for i=1:length(H1)
    Hs3(1,i)=(W^2/g)*0.283*tanh(0.53*(g*H1(1,i)/(W^2))^0.75)*tanh((0.0125*(g*F/(W^2))^0.42)/(tanh(0.53*(g*H1(1,i)/(W^2))^0.75)));
    Ts3(1,i)=(2*pi*W/g)*1.2*tanh(0.833*(g*H1(1,i)/(W^2))^0.375)*tanh((0.077*(g*F/(W^2))^0.25)/(tanh(0.833*(g*H1(1,i)/(W^2))^0.375)));
end

subplot(3,1,3)
plotyy(H1,Hs3,H1,Ts3)
[AX,H1,H2]=plotyy(H1,Hs3,H1,Ts3,'plot');
set(get(AX(1),'Ylabel'),'String','Hs (m)') 
set(get(AX(2),'Ylabel'),'String','Ts (s)')
xlabel('Profundidade (m)') 
title(['Hs e Ts em função da profundidade (Comprimento de pista de ',num2str(F),' metros e velocidade do vento de ',num2str(W),' m/s)']) 
hold on
grid on
plot(H,Hs,'ob')
%plot(H,Ts,'or')
hold off
