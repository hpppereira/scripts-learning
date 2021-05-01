% ESTGAMA1

% Em funcao desta estimativa inicial de estagama e' calculado um novo valor de gama pela rotina estgama1


n=0;clear emq;

% estimativa em torno de gama2 (calculado em estgama)

%for gnovo=0.1:.1:7*gama2, %version before 14/09/2000
%for gnovo=0.1:.1:7
for gnovo=1:.1:7
%if (gama2-2) < 0
%range=0:.1:gama2+2;
%else
%range=(gama2-2):.1:gama2+2;
%end

%for gnovo=range,
n=n+1;

% espectro de jonswap modificado (Smod)


      for cont=1:1:length(strab),

                if f(cont)<=fp
                    sig=0.07;
                    else
                    sig=0.09;
                end

 jon=gnovo^(exp(-((f(cont)-fp)^2)/(2*sig^2*fp^2)));

 pm=(alfa*g^2*2*pi)/((2*pi*f(cont))^(-a))*exp(-5/4*(f(cont)/fp)^(-4));

Smod(cont)=pm*jon;   

     end % loop cont

clear cont alf 

   soma=0;
   for cont=1:1:length(strab),
   Sr=(strab(cont)-Smod(cont))^2;
   soma=soma+Sr;
   end

emq(n)=soma;
gama(n)=gnovo;
end % loop gnovo

clear i b c d e h j l Sr soma cont gama2 pos n 

% valor de gama que proporciona o menor erro quadratico
pos=find(emq==min(emq));
gama3=gama(pos);
	
clear Smod cont
clear emq pos gnovo soma linha posfp posfpm inf linf kteste n fpm sup gama range
