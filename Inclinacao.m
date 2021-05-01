clear
clc
%Rotina para achar inclinação interna e externa e a curvatura com os 
%5 sensores. Chama a suborina 'curvaturearray' para achar o espectro
%direcional. Load do Tanque de ondas.

load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000100_Convertido.gin.mat')
w1a=WAVE1A(2000:3023);
w2a=WAVE2A(2000:3023);
w3a=WAVE3A(2000:3023);
w4a=WAVE4A(2000:3023);
w5a=WAVE5A(2000:3023);

eta1=WAVE1A(2000:3023);
eta2=WAVE2A(2000:3023);
eta3=WAVE3A(2000:3023);
eta4=WAVE4A(2000:3023);
eta5=WAVE5A(2000:3023);
neta=WAVE1A(2000:3023); %Para ser o hv na subrotina 'curvaturearray'- vetor de heave(I)

L=1000; %1 metro = 1000 mm. - Para ficar na mesma unidade que a elevação

% Achar inclinação etax e etay dos sensores externos
for i=1:length(w1a)
    netax(i)=(w1a(i)-w2a(i))/L;
    netay(i)=(w4a(i)-w1a(i))/L;
end
netax=netax';
netay=netay';

% Achar Curvatura
for i=1:length(w1a)
    netaxx(i)=2*((w1a(i)-2*w5a(i)+w3a(i))/(L*sqrt(2)/2));
    netayy(i)=2*((w4a(i)-2*w5a(i)+w2a(i))/(L*sqrt(2)/2));
end
netaxx=netaxx';
netayy=netayy';

% % Achar inclinação etax_int e etay_int dos sensores internos
% for i=1:length(w1a)
%     netax_int(i)=(w1a(i)-w5a(i))/(L*sqrt(2)*2);
%     netay_int(i)=(w2a(i)-w5a(i))/(L*sqrt(2)*2);
% end
% netax=netax';
% netay=netay';

            %%% Chamar rotina de curvaturearray.m %%%
%DADOS DE ENTRADA  
%                 eta1...eta5  = vetor de deslocamento vertical(potencia de 2)
%                 deltat = intervalo de amostragem
%                 donv = direçao que o eixo de origem (x) faz com o Norte
%                 Verdadeiro medido no sentido horario

%DADOS DE SAIDA
% Matriz [dadosteste]=[theta f especx' s kk r];
% Em que: 1º coluna: theta = vetor de direção principal
%         2º coluna: f = frequencia
%         3º coluna:especx = espectro x
%         4º coluna:s = vetor parametro de espalhamento   
%         5º coluna:kk = numero de onda teoria linear ??
%         6º coluna:r = razao kk/k -- para k=vetor numero de onda ??
    
deltat=tempo(2)-tempo(1);
donv=270;
% % % 
% % % [dadosteste,dd]=curvaturearray(neta,netax,netay,netaxx,netayy,deltat,donv,neta);
    

            



