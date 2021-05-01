% ROTINA AJUSTESP

% Ajusta o espectro de jonswap modificado com os parametros alfa, k  ^M
% e gama calculados

% in:   - freq de pico ^M
%       - vetor de freq f^M
%       - espectro medido strab^M
%       - decaimento a^M
%       - melhor ajuste de alfa^M
%       - melhor ajuste de gama^M
%       - melhor ajuste de k^M

% out:  - espectro ajustado S^M


for cont=1:1:length(C11),

pm=(alfa*g^2*2*pi)/((2*pi*f(cont))^(-a))*exp(-5/4*(f(cont)/fp)^(-4*k));

% valores medios de Jonswap para o parametro sigma

   if f(cont)<=fp
   sig=0.07;
   else
   sig=0.09;
   end

   jon=gama^(exp(-((f(cont)-fp)^2)/(2*sig^2*fp^2)));

   S(cont)=pm*jon; % espectro em fc dos parametros estimados

end % loop cont

clear pm jon cont sig gama2 alfa2 Sr soma op opm ans Spm kteste n alfa
