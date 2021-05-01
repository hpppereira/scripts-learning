function [direcao]=corrige(ang)

%FUNCAO DE CORRECAO ANGULAR

%Reduz os angulos de entrada para o sistema de cordenadas utilizadas no modelo

%Variaveis de entrada e saida

% ANG..............Angulo a ser corrigido

if ang>=0 & ang<90;
    direcao=-(90+ang);
else 
    direcao=270-ang;
end
direcao=mod(direcao,360);