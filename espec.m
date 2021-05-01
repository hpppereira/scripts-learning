function [aa]=espec(x,dt)

%calcula espectro simples uma serie real
%elaborado por Joao Luiz Baptista de Carvalho (carvalho@cttmar.univali.br)
%DADOS DE ENTRADA  
%                 x = vetor de componentes horizontais (potencia de 2)
%                 dt = intervalo de amostragem
%DADOS DE SAIDA
%MATRIZ CONTENDO: COLUNA 1 = frequencia
%                        2 = auto espectro da componente x
%                        3 = limite de confianca inferior
%                        4 = limite de confianca superior
%SUBROTINAS CHAMADAS
%                 alisa.m


reg=length(x);
reg2=reg/2;
fc=1/(2*dt);
deltaf=fc*2/reg:fc*2/reg:fc;

%calcula fft

x1=fft(x-mean(x));

%separa componente real e imaginaria

z1=real(x1);
z2=imag(x1);

zn1 = z1.*z1;
zn2 = z2.*z2;

%alisa o espectro

zn1=alisa(zn1);
zn2=alisa(zn2);

%calcula o espectro 

autn1 = 2*dt/reg.*(zn1+zn2);

%calcula os limites para 95% de conficanca

icinf = autn1*14/26.12;
icsup = autn1*14/5.63;

%aa=[deltaf' autn1(1:reg2) icinf(1:reg2) icsup(1:reg2)];
aa=[deltaf' autn1(1:reg2)' icinf(1:reg2)' icsup(1:reg2)'];

