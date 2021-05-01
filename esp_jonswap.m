function [epj aonde md hd ed]=esp_jonswap(VF,fp,alfa,gama)
%  Real Function "esp_jonswap.m":
%  function [epj]=esp_jonswap(VF,fp,alfa,gama)  
%
%  Gera a função analítica do modelo de JONSWAP (denominda "epj") 
%
g=9.81;
df = (VF(2)-VF(1));
epj(1)=0;         
%for j = 1:length(fp) ;
  for i = 2:length(VF)
    if VF(i) <= fp
      sigma=0.07;
    else
      sigma=0.09;
    end
    epj(i)=((alfa.*g.^2)./((2.*pi)^4.*VF(i).^5)).* ...
      exp(-1.25.*(fp./VF(i)).^4).* ...                  % Espectro de PM
      gama.^(exp(-((VF(i)-fp).^2)/(2.*sigma.^2.*fp.^2))); % Fator do Espectro de JONSWAP
  end
%   aonde{j}= find(VF > (0.7*fp(j)) & VF < (1.3*fp(j)));
%   md(j,1)   = sum(epj(j,aonde{j}))*df;
%   hd(j,1)   = 4*sqrt(md(j,1));
%   kp(j,1) = 2*pi*(fp(j).^2)/g;
%   ed(j,1) = 1/2 .*hd(j,1) .*kp(j,1);
% end
