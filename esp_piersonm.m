function [epp]=esp_piersonm(VF,fp)
%  Real Function "esp_piersonm.m".
%
%  Gera a função analítica do modelo de Pierson-Moskovitz
%  (denominda "epp") 
%
g=9.81;alfa=0.0081;epp(1)=0;         
for i = 2:length(VF)
   epp(i)=((alfa*g^2)/((2*pi)^4*VF(i)^5))* ...
          exp(-1.25*(fp/VF(i))^4);      % Espectro de PM
end
