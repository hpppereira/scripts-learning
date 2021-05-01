function [Gs,ht,Gsi,hti,s1,s1p,g0]=FEA_cos2s(deltaf,a1,b1,diraz,dirrad,dirtp,fp,dt)
%% Cos^2s Mitsuyasu
%Passa a direção de pico para radianos
dirtprad=dirtp*180/pi;
%Cálculo de c1
c1=pi*sqrt(a1.^2+b1.^2);
%Cálculo de s1
s1=c1./(1.-c1);

%Calculo do s1 da frequencia de pico
fs1=[deltaf s1];    %Obs: Para se escolher o 's1' em outra frequência, ver na matriz fs1 o valor da frequencia e colocar no lugar de 'fp' da função 'find'
s1p=fs1(find(fs1(:,1)==fp),2);

%Cálculo de Gs para o s1 da frequencia de pico
Gs=2^(2*s1p-1)*((gamma(s1p+1))^2/(gamma(2*s1p+1)));

%Cálculo da função de espalhamento angular
for i=1:length(deltaf)

        ht(i,1)=Gs*abs((cos((dirrad(i,1)-dirtprad)/2))^(2*s1p));
    
end
figure
plot(diraz,ht,'.')  
title(['Função de Espalhamento Angular - cos^2s p/ "s1" de pico de: ',num2str(s1p)]),xlabel('Direção (graus)'),ylabel('h(teta)')
    
%% Função idealizada
s1i=[1:16]';

figure, hold all
for j=1:length(s1i)
    
    for i=1:length(deltaf)
    
        Gsi(i,j)=2^(2*s1i(j,1)-1)*((gamma(s1i(j,1)+1))^2/(gamma(2*s1i(j,1)+1)));
    
        hti(i,j)=Gsi(i,j)*(cos(dirrad(i,1)/2))^2;
    
    end
    
    plot(diraz,hti(:,j),'.')
    %axis([0 180 0 4])
    
end
title('Função de Espalhamento Angular Idealizada (Mitsuyasu - cos^2s)'),xlabel('Direção (graus)'),ylabel('h(teta)')
legend('s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s12','s12','s13','s14','s15','s16')

%% cos^2s paper joao luiz

for j=1:length(s1)
    
    for i=1:length(deltaf)
    
        g0(i,j)=((cos((dirrad(i,1)-dirtprad)/2))^(2*s1(j)))^-1;
    
    end
    
end

