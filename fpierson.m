function [pierson]=fpierson(f,fp,gama,hsig)

%FUNCTION PIERSON

%VARIAVEIS DE ENTRADA E SAIDA

%F.........FREQUENCIA
%FP........FREQUENCIA DE PICO
%GAMA......CONSTANTE GAMA
%HSIG......ALTURA SIGNIFICATIVA

%VARIAVEIS INTERNAS

%ALFA_0....pARCELA DO ESPECTRO DE P.M.
%SIGMA.....
%TP........PERIODO DE PICO

tp=1/fp;
alfa_0=0.0624/(0.23+0.0336*gama-0.185/(1.9+gama));
if f<=fp;
    sigma=0.07;
else
   sigma=0.09;
end
uu=tp*f-1;
oo=-(uu^2)/(2*sigma^2); 
if oo<-300;
    aa=1.0;
else
    aa=gama^(exp(oo));  
end
ee=tp*f;
pierson=alfa_0*(hsig^2)*(1./tp^4)*(1./f^5)*exp(-1.25*(1./ee^4))*aa; 
    





