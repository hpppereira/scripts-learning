%Rotina de cria Ondas senoidais como o principio da superposição das ondas
clear
clc
T=[0:0.1:12.5] %Intervalo de amostragem
hold on
title('Principio da Superposição das Ondas')
xlabel('Quantidade de Registros')
ylabel('Y')
grid %Cria grade
axis([0 126 -1 1]) %Cria eixos nos limites de x e y
for i=1:6 %Quantidade de ondas senoidais
    %ti(i,:)=T*i; %Teste para fazer o somatorio das ondas
    Tseno(i,:)=sin(T*i); % Calcula os senos multiplicado pelos indices e salva 1 em cada linha
    plot(-Tseno(i,:)/i) %Faz o plot do seno dividindo cada onda pelo indice
end
hold off


Tseno(i+1,:)=sum(Tseno(:,:)); %somatorio dos senos
Tseno(i+2,:)=sin(Tseno(i+1,:)); % seno do somatorio dos senos


figure
plot(-Tseno((i+1),:)) %Tenta fazer o plot do somatório das 6 senoides
title('Somatório das Senoides')
xlabel('Quantidade de Registros')
ylabel('Y')