%% Lista 4 - Mec. das Ondas 1
clear,clc,close all
%% Dados de entrada
%Altura da onda
H=1.1;

%Amplitude da onda
a=H/2;

%Comprimento da onda
L=71.3;

%Numero de onda
k=2*pi/L;

%Profundidade
d=10.7;
%d=1000;

%Ac. gravidade
g=9.8;

%Calculo do periodo
T=2*pi/sqrt((g*k*tanh(k*d)));

%Freq. Angular
w=2*pi/T;

%% Velocidades e Aceleracoes

%Vetor espaco
x=0:pi/100:2*pi;

%%% superficie %%%

%Cota
z=0;
j=0;

for i=0:pi/100:2*pi
    j=j+1;
    
    %Velocidade horizontal
    u1(1,j)=(a*g*k/w)*(cosh(k*(d+z))/cosh(k*d))*sin(i);
    
    %Velocidade vertical
    w1(1,j)=(-a*g*k/w)*(sinh(k*(d+z))/cosh(k*d))*cos(i);
    
    %Aceleracao horizontal
    ah1(1,j)=(-a*g*k)*(cosh(k*(d+z))/cosh(k*d))*cos(i);
    
    %Aceleracao vertical
    av1(1,j)=(-a*g*k)*(sinh(k*(d+z))/cosh(k*d))*sin(i);
    
end

figure
plot(x,u1,'-b',x,w1,'-r',x,ah1,'-y',x,av1,'-k'), axis tight, grid on
legend('Vel.Hor','Vel.Vert','Ac.Hor','Ac.Vert')
title('Velocidade na superficie , z=0')

%%% fundo %%%

%Cota
z=-d;
j=0;

for i=0:pi/100:2*pi
    j=j+1;
    
    %Velocidade horizontal
    u2(1,j)=(a*g*k/w)*(cosh(k*(d+z))/cosh(k*d))*sin(i);
    
    %Velocidade vertical
    w2(1,j)=(-a*g*k/w)*(sinh(k*(d+z))/cosh(k*d))*cos(i);
    
    %Aceleracao horizontal
    ah2(1,j)=(-a*g*k)*(cosh(k*(d+z))/cosh(k*d))*cos(i);
    
    %Aceleracao vertical
    av2(1,j)=(-a*g*k)*(sinh(k*(d+z))/cosh(k*d))*sin(i);
    
end

figure
plot(x,u2,'-b',x,w2,'-r',x,ah2,'-y',x,av2,'-k'), axis tight, grid on
legend('Vel.Hor','Vel.Vert','Ac.Hor','Ac.Vert')
title('Velocidade no fundo , z=-d')

%%% profundidade -5m %%%

%Cota
z=-5;
j=0;

for i=0:pi/100:2*pi
    j=j+1;
    
    %Velocidade horizontal
    u3(1,j)=(a*g*k/w)*(cosh(k*(d+z))/cosh(k*d))*sin(i);
    
    %Velocidade vertical
    w3(1,j)=(-a*g*k/w)*(sinh(k*(d+z))/cosh(k*d))*cos(i);
    
    %Aceleracao horizontal
    ah3(1,j)=(-a*g*k)*(cosh(k*(d+z))/cosh(k*d))*cos(i);
    
    %Aceleracao vertical
    av3(1,j)=(-a*g*k)*(sinh(k*(d+z))/cosh(k*d))*sin(i);
    
end

figure
plot(x,u3,'-b',x,w3,'-r',x,ah3,'-y',x,av3,'-k'), axis tight, grid on
legend('Vel.Hor','Vel.Vert','Ac.Hor','Ac.Vert')
title('Velocidade na superficie - z=-5')

j=0;
x=0:pi/100:2*pi;
z=0;
for i=0:pi/100:2*pi
    j=j+1;
    
    n(j)=a*sin(i);
    
    %Velocidade horizontal
    u4(1,j)=(a*g*k/w)*(cosh(k*(d+z))/cosh(k*d))*sin(i);
    
    %Velocidade vertical
    w4(1,j)=(-a*g*k/w)*(sinh(k*(d+z))/cosh(k*d))*cos(i);
    
    %Aceleracao horizontal
    ah4(1,j)=(-a*g*k)*(cosh(k*(d+z))/cosh(k*d))*cos(i);
    
    %Aceleracao vertical
    av4(1,j)=(-a*g*k)*(sinh(k*(d+z))/cosh(k*d))*sin(i);    

end

figure
plot(x,n,'b',x,u4,'r',x,w4,'y',x,ah4,'g',x,av4','k'), axis tight, grid on
legend('Elevacao','Vel.Hor','Vel.Vert','Ac.Hor','Ac.Vert')

