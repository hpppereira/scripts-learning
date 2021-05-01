function [corteta]=cortheta(a,b,donv);

% Reduz as dire�oes de onda para o norte verdadeiro 

% Parametros de entrada (i) e saida (0)

% a,b.....................cordenadas do quadespectro
% donv....................dire�ao do eixo de origem em rela�ao ao N.V.(i)

% Parametros Internos


corteta=atan(b/a)*180/pi;

%Reducao dos dados para o N.V.

corteta=corteta-donv-180;
corteta=mod(corteta,360);

%Retira valores negativos depois da reducao

if corteta<0
    corteta=360+corteta;
end
