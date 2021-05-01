
% Rotina de An�lise de Dados de Onda no Dom�nio do Tempo
function [aa]=ondatempo(a,dt)
% load('T000_000100_Convertido.gin.mat');
% a=WAVE1A;
% dt=0.04;
%Calcula par�metros de onda no dom�nio do tempo
%Autor: Jo�o Luiz Baptista de Carvalho (carvalho@cttmar.univali.br)

% DADOS DE ENTRADA
%         a = vetor de eleva��es
%         dt = intervalo de amostragem



% DADOOS DE SAIDA
%         hs = altura significativa
%         hmax = altura maxima
%         thmax = per�odo associado � altura maxima
%         tz = per�odo m�dio
%         tcc = periodo crista-cava
%         epsilont = largura espectral

% retira m�dia e tend�ncia
a=a-mean(a);
a=dtrend(a);

%identifica zeros descendentes
b=sign(a);
c=diff(b);
d=find(c<0);
n=length(d);

for j=1:n-1
    
    %calcula a altura de crista e cava de cada onda
    crista(j)=max(a(d(j):d(j+1)));
    cava(j)=min(a(d(j):d(j+1)));
    
    %interpola o inicio de cada onda
    x(1)=d(j);
    y(1)=a(d(j));
    x(2)=d(j)+1;
    y(2)=a(d(j)+1);
    
    p=polyfit(x,y,1);
    t1=roots(p);
    
    %interpola o final de cada onda
    
    x(1)=d(j+1);
    y(1)=a(d(j+1));
    x(2)=d(j+1)+1;
    y(2)=a(d(j+1)+1);
    
    p=polyfit(x,y,1);
    t2=roots(p);
    
    %calcula o per�odo de cada onda
    periodo(j)=(t2-t1)*dt;
end

%coloca as ondas em ordem crescente e calcula o hs

[e k]=sort(crista-cava);
hs=mean(e(2*n/3:n-1));

%calcula o per�odo m�dio
tz=mean(periodo);

%calcula o per�odo m�ximo
[hmax k]=max(crista-cava);

%calcula o per�odo associado � altura maxima
thmax=periodo(k);

%calcula per�odo crista-cava

b=diff(a);
c=sign(b);
d=diff(c);
e=find(d<0);
n=length(e);
tempo=(e(n)-e(1))*dt;
tcc=tempo/(n-1);

epsilont=sqrt(1-(tcc/tz)^2);

aa=[hs hmax thmax tz tcc epsilont];


    
    