function [ufd,wfd]=simulacao_tanqueonda
%clear,clc,close all
%Rotina de simula��o de par�metros de onda

%% Dados de entrada

%Quantidade de registros
x=(1:1024)'; 
%Intervalo de tempo de amostragem
t=1;
%Acelera��o da gravidade (m/s)
g=9.81;
%Altura da onda
H=input('Enre com a altura da onda (m): ');
%Periodo da onda
T=input('Enre com o per�odo da onda (s): ');
%Profundidade
h=input('Entre com a profundidade do local (m): ');
%Frequ�ncia angular
Fa=2*pi/T;
%Comprimento de onda (m) em �guas profundas
Lf=1.56*T^2;
%Numero de onda em �guas profundas
kf=2*pi/Lf;
%Comprimento de onda (m) em �guas rasas
Lr=Lf*tanh(kf*h);
%Numero de onda em �guas rasas
kr=2*pi/Lr;
%Celeridade em �guas profundas
Cf=1.56*T;
%Celeridade em �guas rasas
Cr=(Lf/T)*tanh(kf*h); %tanh do kf ou kr??
%Cota (z)
z=0;

%% Imprimir se a onda est� em �guas rasa ou funda

if h/Lf>=(1/2)
    disp('A onda est� se propagando em �guas profundas')
elseif h/Lf<(1/2) & h/Lf>(1/20)
    disp('A onda est� se propagando em �guas intermedi�rias')
    
    
    
elseif h/Lf<=(1/20)
    disp('A onda est� se propagando em �guas rasas')
end

%% Par�metros de onda

for i=1:length(x)
    
    %Eleva��o para �guas profundas (etaf) e rasas (etar)
    etaf(i,1)=H/2*cos((kf*x(i,1))-(Fa*t));  
    etar(i,1)=H/2*cos((kr*x(i,1))-(Fa*t));  

    %Potencial de velocidade da part�cula para �guas profundas (pvf) e rasas (pvr)
    pvf(i,1)=(-(H/2)*g*cosh(kr)*(h+z)*sinh(kf*x(i,1)-Fa*t))/(2*Fa*cosh(kf*h)); 
    pvr(i,1)=(-(H/2)*g*cosh(kr)*(h+z)*sinh(kr*x(i,1)-Fa*t))/(2*Fa*cosh(kr*h)); 
    
    %Potencial de velocidade da part�cula introduzindo a rela��o de dispers�o para �guas profundas (pvfd) e rasas (pvrd)
    pvfd(i,1)=(-(H/2)*Cf*cosh(kf)*(h+z)*sin(kf*x(i,1)-Fa*t))/(2*sinh(kf*h)); 
    pvrd(i,1)=(-(H/2)*Cr*cosh(kr)*(h+z)*sin(kr*x(i,1)-Fa*t))/(2*sinh(kr*h)); 
    
    %Velocidade horizontal da particula para �guas profundas (uf) e rasas (ur)
    uf(i,1)=(H*Fa*cosh(kf)*(h+z)*cos(kf*x(i,1)-Fa*t))/(2*sinh(kf*h));
    ur(i,1)=(H*Fa*cosh(kr)*(h+z)*cos(kr*x(i,1)-Fa*t))/(2*sinh(kr*h));
        
    %Velocidade horizontal da particula introduzindo a rela��o de dispers�o para �guas profundas (ufd) e rasas (urd)
    ufd(i,1)=(H*g*kf*cosh(kf)*(h+z)*cos(kf*x(i,1)-Fa*t))/(2*Fa*cosh(kf*h));
    urd(i,1)=(H*g*kr*cosh(kr)*(h+z)*cos(kr*x(i,1)-Fa*t))/(2*Fa*cosh(kr*h));
    
    %Acelera��o horizontal da particula  para �guas profundas (u1fd) e rasas (u1rd) -> utilizando a rela��o de dispers�o
    u1fd(i,1)=(H*g*kf*cosh(kf)*(h+z)*sin(kf*x(i,1)-Fa*t))/(2*cosh(kf*h));
    u1rd(i,1)=(H*g*kr*cosh(kr)*(h+z)*sin(kr*x(i,1)-Fa*t))/(2*cosh(kr*h));
    
    %Velocidade vertical da particula  para �guas profundas (wfd) e rasas (wrd) -> utilizando a rela��o de dispers�o
    wfd(i,1)=(H*g*kf*sinh(kf)*(h+z)*sin(kf*x(i,1)-Fa*t))/(2*Fa*cosh(kf*h));
    wrd(i,1)=(H*g*kr*sinh(kr)*(h+z)*sin(kr*x(i,1)-Fa*t))/(2*Fa*cosh(kr*h));
    
    %Acelera��o vertical da particula para �guas profundas (w1fd) e rasas (w1rd) -> utilizando a rela��o de dispers�o
    w1fd(i,1)=(H*g*kf*sinh(kf)*(h+z)*cos(kf*x(i,1)-Fa*t))/(2*cosh(kf*h));
    w1rd(i,1)=(H*g*kr*sinh(kr)*(h+z)*cos(kr*x(i,1)-Fa*t))/(2*cosh(kr*h));
    
    %Deslocamento horizontal da particula para �guas profundas (dhf) e rasas (dhr)
    dhf(i,1)=(-H*g*kf*cosh(kf)*(h+z)*sin(kf*x(i,1)-Fa*t))/(2*(Fa)^2*cosh(kf*h));
    dhr(i,1)=(-H*g*kr*cosh(kr)*(h+z)*sin(kr*x(i,1)-Fa*t))/(2*(Fa)^2*cosh(kr*h));
    
    %Deslocamento horizontal da particula para �guas profundas (dhfd) e rasas (dhrd) -> utilizando a rela��o de dispers�o
    dhfd(i,1)=(-H*cosh(kf)*(h+z)*sin(kf*x(i,1)-Fa*t))/(2*sinh(kf*h));
    dhrd(i,1)=(-H*cosh(kr)*(h+z)*sin(kr*x(i,1)-Fa*t))/(2*sinh(kr*h));
    
    %Deslocamento vertical da particula para �guas profundas (dvfd) e rasas (dvrd) -> utilizando a rela��o de dispers�o
    dvfd(i,1)=(-H*sinh(kf)*(h+z)*cos(kf*x(i,1)-Fa*t))/(2*sinh(kf*h));
    dvrd(i,1)=(-H*sinh(kr)*(h+z)*cos(kr*x(i,1)-Fa*t))/(2*sinh(kr*h));
    
end

%% Plot dos par�metros de onda
% figure (1)
% subplot(2,2,1)
% 
% plot(etaf,'b'), hold on
% plot(ufd,'r')
% plot(u1fd,'g')
% plot(wfd,'y')
% plot(w1fd,'k'), hold on
% axis tight
% title('Ondas em �guas profundas')
% legend('Eta','Vel.H','Acel.H','Vel.V','Acel.V')
% 
% subplot(2,2,2)
% plot(etar,'b'), hold on
% plot(urd,'r')
% plot(u1rd,'g')
% plot(wrd,'y')
% plot(w1rd,'k'), hold on
% axis tight
% title('Ondas em �guas rasas')
% legend('Eta','Vel.H','Acel.H','Vel.V','Acel.V')
% 
% subplot(2,2,3)
% plot(dhfd,dvfd)
% axis([min(dhfd) max(dhfd) min(dvfd) max(dvfd)])
% title('Deslocamento da part�cula em �guas profundas')
% 
% subplot(2,2,4)
% plot(dhrd,dvrd)
% axis([min(dhfd) max(dhfd) min(dvfd) max(dvfd)])
% title('Deslocamento da part�cula em �guas rasas')
    
 