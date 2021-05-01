%Cinematica com valores ctes
clear,clc
x=(1:1024)';
t=0;
H=2;
T=12;
h=1; %Quanto maior a profundidade, menor o raio do trajetoria
L=1.56*T^2;
k=2*pi/L; %Quando se coloca este comprimento de onda(aguas profundas) ocorre sobreposição no deslocamento
z=0;
fa=2*pi/T;


for i=1:length(x)
    
%deslocamento horizontal
deshd(i,1)=(-H*cosh(k)*(h+z)*sin(k*x(i,1)-fa*t))/(2*sinh(k*h));

%deslocamento vertical
desvd(i,1)=(-H*sinh(k)*(h+z)*cos(k*x(i,1)-fa*t))/(2*sinh(k*h));

end

plot(deshd,desvd)
axis([-40 40 -1 1])
