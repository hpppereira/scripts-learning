%Sobreposição de 2 ondas
clear,clc
%Eta1
x=(1:1024)';
t=1;
H=2;
T1=10;
L1=1.56*T1^2;
k1=2*pi/L1;
fa1=2*pi/T1;

for i=1:length(x)
    eta1(i,1)=(H/2)*cos((k1*x(i,1))-(fa1*t));
end

T2=5;
L2=1.56*T2^2;
k2=2*pi/L2;
fa2=2*pi/T2;

for i=1:length(x)
    eta2(i,1)=(H/2)*cos((k2*x(i,1))-(fa2*t));
end

eta3=eta1+eta2;

hold on
plot(eta1);
plot(eta2,'r');
hold off

figure
hold on
plot(eta3,'g');
%plot(eta1);
%plot(eta2,'r')
hold off

%Eta com diferença de fase

for i=1:length(x)
    eta4(i,1)=(H/2)*cos((k2*x(i,1))-(fa2*t)+180);
end

hold on
%plot(eta1);
%plot(eta4,'r');
hold off

%Chamar rotina espec
x=eta3;
dt=1;
[aa]=espec(x,dt);
figure
plot(aa(:,1),aa(:,2))
