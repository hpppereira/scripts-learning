% Rotina ESTK

% O quarto passo e' variar o valor de k em 1.0, 1.2, 1.5, 1.8 e 2.0 e calcular os erros medios quadraticos

% in:   - freq de pico fp
%       - vetor de freq f^M
%       - espectro medido strab^M
%       - decaimento a^M
%       - melhor ajuste de alfa^M
%       - melhor ajuste de gama^M

% out:  - melhor ajuste de k^M



for n=1:1:5,

if n==1
k=1;
elseif n==2
k=1.2;
elseif n==3
k=1.5;
elseif n==4
k=1.8;
else 
k=2;
end

cont=0;
for cont=1:1:length(C11),

    pm1=(alfa*g^2*2*pi)/((2*pi*f(cont))^(-a))*exp(-5/4*(f(cont)/fp)^(-4*k));

% valores medios de Jonswap para o parametro sigma

   if f(cont)<=fp
   sig=0.07;
   else
   sig=0.09;
   end

   jon1=gama^(exp(-((f(cont)-fp)^2)/(2*sig^2*fp^2)));

   Smod(cont)=pm1*jon1;

end % loop cont

clear cont jon1 pm1

   soma=0;
   for cont=1:1:length(C11),
   Sr=(C11(cont)-Smod(cont))^2;
   soma=soma+Sr;
   end
         
emq(n)=soma;
kteste(n)=k;     
end % loop n


% valor de k que proporciona o menor erro quadratico
pos=find(emq==min(emq));
k=kteste(pos);

clear pos emq cont Smod kteste n pm1 jon1 soma Sr gama alfa a fp
