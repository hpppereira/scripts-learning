%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Rotina para processamento recompor componentes cartesianas
%  para sistema polar tipo velocidade e direção
%  
%  sintaxe: saida = uvparaveldir (entrada)
%
%  entrada = [u,v] sendo u - componente X ou lesteoeste e v - componente Y ou nortesul
%  saida = [vel,dir]
%
%  Schettini, 13 de agosto de 1999
%  Corrigido 9 de agosto de 2002
% problema com orienta'c~ao dos vetores de saida... 22 fev 2004
% problema com orientacao!!!! PORRRAAAAA!!!! 5 abr 2005 !!!!
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [vel,dire]=uvparaveldir(u,v);

if nargin == 1
   v=u(:,2);
   u=u(:,1);
end

vel=((u.^2 + v.^2).^.5)';

for i=1:length(u)
  if u(i) == 0 & v(i) ~= 0  
      u(i)=0.0001;
  elseif v(i) == 0 & u(i) ~= 0
      v(i)=0.0001;
  elseif u(i) == 0 & v(i) == 0
      u(i) = 0.0001;
  end
  
  if u(i) > 0 & v(i) > 0
      dire(i)=atan(u(i)/v(i))*180/pi;      
  elseif u(i) > 0 & v(i) < 0
      dire(i)= 180 - atan(abs(u(i)/v(i)))*180/pi;
  elseif u(i) < 0 & v(i) < 0
      dire(i)= 180 + atan(abs(u(i)/v(i)))*180/pi;
  elseif u(i) < 0 & v(i) > 0
      dire(i)= 360 - atan(abs(u(i)/v(i)))*180/pi;
      %  else u(i)==0 & v(i)==0
      %dire(i) = NaN    
  end
end

if nargout == 1
   vel=[vel' dire'];
end
%dire=dire';