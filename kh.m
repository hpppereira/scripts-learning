clear
clc
% K1=[0.125:0.1:3]';
% K2=[0:0.1:3]';
k=linspace(0.05,3,100)'; 
h=10;
T=10;
fang=2*pi/T;
fang2=fang^2;
g=9.81;

for i=1:length(k)
    lin1(i,1)=tanh(k(i,1)*h);
    lin2(i,1)=(fang2*h)/(g*k(i,1)*h);
%     if lin1(i,1)==lin2(i,1)
%         disp('este é o valor de k.h)')
%     end
end

hold on
plot(lin1,'b.-');
plot(lin2,'r.-');
hold off

disp('Clique no ponto de cruzamento entre as duas curvas: ')

a=ginput(1);

KH=a(1,1);
disp(['O valor de k*h é: ',num2str(KH)])


