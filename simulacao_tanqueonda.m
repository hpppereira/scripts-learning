function [ufd,wfd]=simulacao_tanqueonda
%clear,clc,close all
%Rotina de simulação de parâmetros de onda

%% Dados de entrada

%Quantidade de registros
x=(1:1024)'; 
%Intervalo de tempo de amostragem
t=1;
%Aceleração da gravidade (m/s)
g=9.81;
%Altura da onda
H=input('Enre com a altura da onda (m): ');
%Periodo da onda
T=input('Enre com o período da onda (s): ');
%Profundidade
h=input('Entre com a profundidade do local (m): ');
%Frequência angular
Fa=2*pi/T;
%Comprimento de onda (m) em águas profundas
Lf=1.56*T^2;
%Numero de onda em águas profundas
kf=2*pi/Lf;
%Comprimento de onda (m) em águas rasas
Lr=Lf*tanh(kf*h);
%Numero de onda em águas rasas
kr=2*pi/Lr;
%Celeridade em águas profundas
Cf=1.56*T;
%Celeridade em águas rasas
Cr=(Lf/T)*tanh(kf*h); %tanh do kf ou kr??
%Cota (z)
z=0;

%% Imprimir se a onda está em águas rasa ou funda

if h/Lf>=(1/2)
    disp('A onda está se propagando em águas profundas')
elseif h/Lf<(1/2) & h/Lf>(1/20)
    disp('A onda está se propagando em águas intermediárias')
    
    
    
elseif h/Lf<=(1/20)
    disp('A onda está se propagando em águas rasas')
end

%% Parâmetros de onda

for i=1:length(x)
    
    %Elevação para águas profundas (etaf) e rasas (etar)
    etaf(i,1)=H/2*cos((kf*x(i,1))-(Fa*t));  
    etar(i,1)=H/2*cos((kr*x(i,1))-(Fa*t));  

    %Potencial de velocidade da partícula para águas profundas (pvf) e rasas (pvr)
    pvf(i,1)=(-(H/2)*g*cosh(kr)*(h+z)*sinh(kf*x(i,1)-Fa*t))/(2*Fa*cosh(kf*h)); 
    pvr(i,1)=(-(H/2)*g*cosh(kr)*(h+z)*sinh(kr*x(i,1)-Fa*t))/(2*Fa*cosh(kr*h)); 
    
    %Potencial de velocidade da partícula introduzindo a relação de dispersão para águas profundas (pvfd) e rasas (pvrd)
    pvfd(i,1)=(-(H/2)*Cf*cosh(kf)*(h+z)*sin(kf*x(i,1)-Fa*t))/(2*sinh(kf*h)); 
    pvrd(i,1)=(-(H/2)*Cr*cosh(kr)*(h+z)*sin(kr*x(i,1)-Fa*t))/(2*sinh(kr*h)); 
    
    %Velocidade horizontal da particula para águas profundas (uf) e rasas (ur)
    uf(i,1)=(H*Fa*cosh(kf)*(h+z)*cos(kf*x(i,1)-Fa*t))/(2*sinh(kf*h));
    ur(i,1)=(H*Fa*cosh(kr)*(h+z)*cos(kr*x(i,1)-Fa*t))/(2*sinh(kr*h));
        
    %Velocidade horizontal da particula introduzindo a relação de dispersão para águas profundas (ufd) e rasas (urd)
    ufd(i,1)=(H*g*kf*cosh(kf)*(h+z)*cos(kf*x(i,1)-Fa*t))/(2*Fa*cosh(kf*h));
    urd(i,1)=(H*g*kr*cosh(kr)*(h+z)*cos(kr*x(i,1)-Fa*t))/(2*Fa*cosh(kr*h));
    
    %Aceleração horizontal da particula  para águas profundas (u1fd) e rasas (u1rd) -> utilizando a relação de dispersão
    u1fd(i,1)=(H*g*kf*cosh(kf)*(h+z)*sin(kf*x(i,1)-Fa*t))/(2*cosh(kf*h));
    u1rd(i,1)=(H*g*kr*cosh(kr)*(h+z)*sin(kr*x(i,1)-Fa*t))/(2*cosh(kr*h));
    
    %Velocidade vertical da particula  para águas profundas (wfd) e rasas (wrd) -> utilizando a relação de dispersão
    wfd(i,1)=(H*g*kf*sinh(kf)*(h+z)*sin(kf*x(i,1)-Fa*t))/(2*Fa*cosh(kf*h));
    wrd(i,1)=(H*g*kr*sinh(kr)*(h+z)*sin(kr*x(i,1)-Fa*t))/(2*Fa*cosh(kr*h));
    
    %Aceleração vertical da particula para águas profundas (w1fd) e rasas (w1rd) -> utilizando a relação de dispersão
    w1fd(i,1)=(H*g*kf*sinh(kf)*(h+z)*cos(kf*x(i,1)-Fa*t))/(2*cosh(kf*h));
    w1rd(i,1)=(H*g*kr*sinh(kr)*(h+z)*cos(kr*x(i,1)-Fa*t))/(2*cosh(kr*h));
    
    %Deslocamento horizontal da particula para águas profundas (dhf) e rasas (dhr)
    dhf(i,1)=(-H*g*kf*cosh(kf)*(h+z)*sin(kf*x(i,1)-Fa*t))/(2*(Fa)^2*cosh(kf*h));
    dhr(i,1)=(-H*g*kr*cosh(kr)*(h+z)*sin(kr*x(i,1)-Fa*t))/(2*(Fa)^2*cosh(kr*h));
    
    %Deslocamento horizontal da particula para águas profundas (dhfd) e rasas (dhrd) -> utilizando a relação de dispersão
    dhfd(i,1)=(-H*cosh(kf)*(h+z)*sin(kf*x(i,1)-Fa*t))/(2*sinh(kf*h));
    dhrd(i,1)=(-H*cosh(kr)*(h+z)*sin(kr*x(i,1)-Fa*t))/(2*sinh(kr*h));
    
    %Deslocamento vertical da particula para águas profundas (dvfd) e rasas (dvrd) -> utilizando a relação de dispersão
    dvfd(i,1)=(-H*sinh(kf)*(h+z)*cos(kf*x(i,1)-Fa*t))/(2*sinh(kf*h));
    dvrd(i,1)=(-H*sinh(kr)*(h+z)*cos(kr*x(i,1)-Fa*t))/(2*sinh(kr*h));
    
end

%% Plot dos parâmetros de onda
% figure (1)
% subplot(2,2,1)
% 
% plot(etaf,'b'), hold on
% plot(ufd,'r')
% plot(u1fd,'g')
% plot(wfd,'y')
% plot(w1fd,'k'), hold on
% axis tight
% title('Ondas em águas profundas')
% legend('Eta','Vel.H','Acel.H','Vel.V','Acel.V')
% 
% subplot(2,2,2)
% plot(etar,'b'), hold on
% plot(urd,'r')
% plot(u1rd,'g')
% plot(wrd,'y')
% plot(w1rd,'k'), hold on
% axis tight
% title('Ondas em águas rasas')
% legend('Eta','Vel.H','Acel.H','Vel.V','Acel.V')
% 
% subplot(2,2,3)
% plot(dhfd,dvfd)
% axis([min(dhfd) max(dhfd) min(dvfd) max(dvfd)])
% title('Deslocamento da partícula em águas profundas')
% 
% subplot(2,2,4)
% plot(dhrd,dvrd)
% axis([min(dhfd) max(dhfd) min(dvfd) max(dvfd)])
% title('Deslocamento da partícula em águas rasas')
    
 