%Calculo do comprimento de onda em aguas intermediarias
%
%Curso Analise de Dados em Ondas de Gravidade (ADOG)

clear,clc,close all

%Dados de entrada:

%Profundidade (m)
h = 5;

%Periodo de pico (seg)
T = 10;

%Comprimento das ondas em aguas profundas
Lo = 1.56 * T^2;

%Iteracao para o calculo de L em aguas intermediaria

L = Lo;

%Faz a iteracao 100 vezes (verificar se convergiu)

%Mostra apenas o ultimo valor
% for i = 1:100
%     
%     L = Lo * tanh((2*pi/L)*h);
%         
% end
% %pega o ultimo valor
% L = L(1:end-1);


%Mostra os valores convergindo
for i = 1:100
    
    L(i) = Lo * tanh((2*pi/L(i))*h);
    
    L(i+1) = L(i);
    
end

%pega o ultimo valor
L = L(1:end-1);

Lint = L(end);

kint = 2 * pi / Lint;

disp(['O comprimento da onda na profundidade de ',num2str(h),' m é: ',num2str(Lint)])
disp(['O numero de onda (k) é: ',num2str(kint)])

plot(L)
    
    
%Entra com um vetor de comprimentos (periodos) de ondas

%Periodos de pico
% T1 = [5:20];
% 
% Lo1 = 1.56 .* (T1 .^2);
% 
% L1=Lo1;
% 
% for j=1:length(L1)
%         
%     for i=1:100
%   
%         L1(j)=Lo1(j)*tanh((2*pi)/L1(j)*h);
%    
%     end
% 
%     %
%     L1(j+1)=L1(j);
%     
% end
% L1=L1(1:end-1);

