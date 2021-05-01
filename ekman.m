%Programa para resolver o modelo de Ekman
%Turma de Ocn Fis 3 2o sem 2011 - 31/8/2011
% ue = Vo cos ((pi/4)+((pi/De)*z))*exp((pi/De)*z)
% ve = Vo sin ((pi/4)+((pi/De)*z))*exp((pi/De)*z)
% 
clear all;clc

lat=-23*pi/180;
omega=2*pi/(24*60*60);
f=2*omega*sin(lat);
Av=1e-2; %valor de viscosidade vertical típica no oceano.
De= pi*sqrt(2*Av/abs(f));
z=0:-1:-De;
tau=1e-1;%tensão de cisalhamento do vento 
rho=1020; %valor típico de densidade da água do mar em kg/m3
Vo=(sqrt(2)*pi*tau)/(De*rho*abs(f));
ue = Vo.* cos ((pi./4)+((pi./De).*z)).*exp((pi./De).*z);
ve = Vo.* sin ((pi./4)+((pi./De).*z)).*exp((pi./De).*z);

plot(ue,z);
plot(ve,z);

%artimanha pra plotar em 3D

for m=1:59;
 x3(1,m) = 0.;
 x3(2,m) = ue(m);
 y3(1,m) = 0.;
 y3(2,m) = ve(m);
 z3(1,m) = z(m);
 z3(2,m) = z(m); 
end;

figure(3);
plot3(x3,y3,z3)