function [corteta]=cortheta(a,b,donv);

% Reduz as direçoes de onda para o norte verdadeiro 

% Parametros de entrada (i) e saida (0)

% a,b.....................cordenadas do quadespectro
% donv....................direçao do eixo de origem em relaçao ao N.V.(i)

% Parametros Internos


corteta=atan(b/a)*180/pi;

%Reducao dos dados para o N.V.

corteta=corteta-donv-180;
corteta=mod(corteta,360);

%Retira valores negativos depois da reducao

if corteta<0
    corteta=360+corteta;
end
