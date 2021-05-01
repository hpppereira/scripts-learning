function[aa]=onddir(eta,etax,etay,deltat,donv)

%calcula espectro direcional para ondografo datawell
%DADOS DE ENTRADA  
%                 eta  = vetor de deslocamento vertical(potencia de 2)
%                 etax = vetor de inclinacao em x (potencia de 2)
%                 etay = vetor de inclinacao em y (potencia de 2)
%                 deltat = intervalo de amostragem
%                 donv = direçao que o eixo de origem (x) faz com o Norte
%                 Verdadeiro medido no sentido horario

%DADOS DE SAIDA
%MATRIZ CONTENDO: COLUNA 1 = frequencia
%                        2 = auto espectro de eta
%                        3 = direcao principal
%                        4 = espalhamento angular 

%SUBRROTINAS CHAMADAS

%                  cortheta.m
%                  espec.m
%                  espec2.m

reg=length(eta);
pi=3.141593;
reg2=reg/2;
fc=1/(2*deltat);
deltaf=fc*2/reg:fc*2/reg:fc;

espeta = espec(eta,deltat);
auteta = espeta(:,2); 

espetax = espec(etax,deltat);
autetax = espetax(:,2); 

espetay = espec(etay,deltat);
autetay = espetay(:,2); 

espetaetax = espec2(eta,etax,deltat);
coetaetax = espetaetax(:,4);
qdetaetax = espetaetax(:,5); 

espetaetay = espec2(eta,etay,deltat);
coetaetay = espetaetay(:,4); 
qdetaetay = espetaetay(:,5); 

k=sqrt((autetax+autetay)./auteta);

%     CALCULA A DIRECAO PRINCIPAL

aa(1:reg2,1:5)=nan;

for i = 1:reg2
   
   if (auteta(i)>0.0001)
                       
      a1 = qdetaetax(i)/(pi*auteta(i)*k(i));
      b1 = qdetaetay(i)/(pi*auteta(i)*k(i));
           
      theta(i) = corthet3(a1,b1,donv);

      s(i) = pi*sqrt(a1*a1+b1*b1);
      s(i) = s(i)/(1-s(i));
      
      aa(i,:) = [deltaf(i) auteta(i) theta(i) s(i) k(i)];      
      
   end
end



