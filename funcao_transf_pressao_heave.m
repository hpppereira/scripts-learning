clear,clc

%f = 0.667; %hz

%T = 1/f; %seg
T = 10;

Lo = 1.56 * T^2;

L = Lo;

%d = 0.75; %m - prof
d = 20;

%fazer a iteracao 100 vezes
for i=1:100
  
    L(i)=Lo*tanh(((2*pi)/L(i))*d);
        
    L(i+1)=L(i);
        
end

%se convergiu, pegar o ultimo valor do vetor L
Li = L(end);

%plota figura de iteracao
plot(L,'-*')

%calculo de n de onda em aguas intermediarias
ki = 2 * pi / Li;

%pressao kilonewton/m2
P = 124;

%cota
z = -11.4;

rho = 1.025; %kg/m3

g = 9.8; %m/s2

eta = ( ( cosh(ki*d)/cosh(ki*(d+z) ) * (P + rho * g * z) ) / (rho * g) );

%altura da onda
H = eta * 2;

