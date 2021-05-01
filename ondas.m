function [registro]=ondas(t1,w1)

% Saida com alguns registros de ondas
%Dados de entrada , vetor elevação e tempo
% Ex:
%  t1=tempo(3477:4500);   %vetor tempo
%  w1=WAVE1A(3477:4500);   %vetor de elevação de ondas ctes.

nm=mean(w1);    %elevação media
contza=0;
for i=1:1023
    if (w1(i)<nm & w1(i+1)>nm)
        contza=contza+1;
        x=[t1(i) t1(i+1)];
        y=[w1(i) w1(i+1)];
        [b,a]=regressao(x,y); %chama subrotina de regressao linear
        xnm=(nm-b)/a;
        x_regonda(1,contza)=xnm; %coloca os valores do x para y=nm dos zeros ascendentes
        %matza(1,contza)=w1(i+1); %cria matriz com os valor de w1 (elevação) nos zeros ascendentes para f(x)=x+1
        matreg(1,i)=i;
    end
end
matreg=find(matreg); % Elementos do começo de cada onda

for i=1:length(matreg)-1
    elmin(1,i)=min(w1(matreg(i):matreg(i+1)));
    elmax(1,i)=max(w1(matreg(i):matreg(i+1)));
    altura(1,i)=elmax(1,i)-elmin(1,i);
end

contonda=contza-1;
for i=1:contonda
    periodo(1,i)=x_regonda(1,i+1)-x_regonda(1,i); %Periodo de ondas
end

Hmax=max(altura); %Altura maxima do registro
Hm=mean(altura); %Altura média
Tmax=max(periodo); %Periodo maximo do registro
frequencia=1./periodo; %Frequencia 1/T (Hz)de cada onda
fang=2*pi./periodo; %Freq. Ang = 2pi/T de cada onda
comprimento=1.56*(periodo.^2); %comprimento de onda = 1.56T^2 (m)
celeridade=comprimento./periodo; %celeridade = L/T de cada onda
celeridade1=1.56.*periodo; %celeridade =1.56*T de cada onda
numonda=2*pi./comprimento; %vetor numero de onda de cada onda
Tt=max(t1)-min(t1); %Periodo total de amostragem
Tz=Tt/contza; %Periodo médio de zero ascendente (Tz=Tt/Nz) Tt= periodo total de amstragem / Nz= nº de onda de zero ascentente
Tc=Tt/contonda; %Periodo de crista

[registro]=[altura;periodo;frequencia;fang;comprimento;celeridade;numonda];