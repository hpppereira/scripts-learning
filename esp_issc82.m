function [epi]=esp_issc82(VF,Hs,Tz)
%  Real Function "esp_issc82.m":
%  function [epj]=esp_issc82(VF,Hs,Tz)
%  
%  Gera a função analítica do modelo de ISSC/82 (denominda "epi") 
%  Entrada: VF (em Hertz); Hs (em m) e Tz (em seg)
%  Saida:   epi (em m2/Hertz)
g=9.81;
epi(1)=0;
% Converte frequencia de Hz para Rad/s
w=2*pi.*VF;
A=124.03*(Hs^2)/(Tz^4);
B=496.10/(Tz^4);
% Gerando espectro em m2*seg/rad
for k = 2:length(VF)
   epi(k)=A*exp(-B/(w(k)^4))/(w(k)^5); % Espectro do ISSC
end
% Converte espectro de m2*seg/rad para m2/Hz
epi=epi*2*pi;

