function [alfa,gama,Hsmod,lm,epj1,epj2,epj3]=modelo_jonsw2(fSpico,Spico,fScava,Scava,VS,VF,DT,VMTA1,VMTA2,VMTA3,nfft,pdir,fig);
%
% Rotina para estimativa dos parametros Alfa
% e Gama do espectro de JONSWAP
%
% Elaborada pelo Jose A. Lima 07/08/99
%
% Chama a funcao f_jonswap2.m
%                
% Inicializando arrays alfa e gama
alfa=zeros(length(Spico),1);gama=zeros(length(Spico),1);g=9.81;
% Ordenando os vetores com valores de pico em 
% ordem crescente de frequencia
[auxfp k]=sort(fSpico);
auxS=Spico(k);
auxfc=fScava(k)';
% Calculando o vetor lm com posicao do pico no eixo de
% frequencias VF (abcissa)
lm=auxfp*(nfft*DT)+1;
% Calculando o vetor lc com posicao da cava espectral no
% eixo de frequencias VF (abcissa)
lc=[auxfc 1/(2*DT)]*(nfft*DT)+1;
% Atribuindo valores a um vetor com momentos medidos
vmt=[];
j=0;
while j < length(auxS)
   j=j+1;
   if k(j) == 1
      vmt(j)=VMTA1;
   elseif k(j) == 2
      vmt(j)=VMTA2;
   elseif k(j) == 3
      vmt(j)=VMTA3;
   end
end
% Inicializando os vetores com espectros de JONSWAP
epj1=zeros(length(VF),1);epj2=zeros(length(VF),1);epj3=zeros(length(VF),1);
%
% -------------------------------------------------------
% Bloco para calculo de Alfas e Gamas para cada pico
% definido pelo vetor auxS
if length(auxS) == 1 % Apenas um pico espectral significativo
   % Modelagem do unico pico
   m1=lc(1); m2=lc(2);  % Abcissas com regiao espectral para modelagem
   Sp_jwp=0;            % Inicializacao da ordenada de pico modelada por JONSWAP
   [epj1,gama,alfa,Hsmod,VMT_model]=f_jonswap2(VF,auxfp(1),auxS(1),m1,m2,nfft,DT,vmt(1),Sp_jwp);
   
elseif length(auxS) == 2 % Dois picos espectrais significativos
   % Modelagem do pico de mais baixa frequencia
   m1=lc(1); m2=lc(2);           % Abcissas com regiao espectral para modelagem
   Sp_jwp=0;                     % Inicializacao da ordenada de pico modelada por JONSWAP
   [epj1,p_gama,p_alfa,Hsmod,VMT_model]=f_jonswap2(VF,auxfp(1),auxS(1),m1,m2,nfft,DT,vmt(1),Sp_jwp);
   alfa(k(1))=p_alfa;gama(k(1))=p_gama;
   % Modelagem do pico em mais alta frequencia
   m1=lc(2); m2=lc(3);           % Abcissas com regiao espectral para modelagem
   % Inicializacao da ordenada de pico modelada por JONSWAP
   if auxfp(2) <= auxfp(1);sigma=0.07;else;sigma=0.09;end
   Sp_jwp=alfa(k(1))*( 2*pi*(g^2)./((2*pi.*auxfp(2)).^5).* ...
     exp(-1.25.*(auxfp(1)./auxfp(2)).^4).* ...
     gama(k(1)).^exp( -((auxfp(2)-auxfp(1)).^2)./(2.*(sigma.^2).*(auxfp(1)^2)) ));
   [epj2,p_gama,p_alfa,Hsmod,VMT_model]=f_jonswap2(VF,auxfp(2),auxS(2),m1,m2,nfft,DT,vmt(2),Sp_jwp);
   alfa(k(2))=p_alfa;gama(k(2))=p_gama;

else   % Tres picos espectrais significativos
   % Modelagem do pico de mais baixa frequencia
   m1=lc(1);m2=lc(2);            % Abcissas com regiao espectral para modelagem
   Sp_jwp=0;                     % Inicializacao da ordenada de pico modelada por JONSWAP
   [epj1,p_gama,p_alfa,Hsmod,VMT_model]=f_jonswap2(VF,auxfp(1),auxS(1),m1,m2,nfft,DT,vmt(1),Sp_jwp);
   alfa(k(1))=p_alfa;gama(k(1))=p_gama;
   % Modelagem do segundo pico por ordem de frequencia)
   m1=lc(2); m2=lc(3);           % Abcissas com regiao espectral para modelagem
   % Inicializacao da ordenada de pico modelada por JONSWAP
   if auxfp(2) <= auxfp(1);sigma=0.07;else;sigma=0.09;end
   Sp_jwp=alfa(k(1))*( 2*pi*(g^2)./((2*pi.*auxfp(2)).^5).* ...
     exp(-1.25.*(auxfp(1)./auxfp(2)).^4).* ...
     gama(k(1)).^exp( -((auxfp(2)-auxfp(1)).^2)./(2.*(sigma.^2).*(auxfp(1)^2)) ));
   [epj2,p_gama,p_alfa,Hsmod,VMT_model]=f_jonswap2(VF,auxfp(2),auxS(2),m1,m2,nfft,DT,vmt(2),Sp_jwp);
   alfa(k(2))=p_alfa;gama(k(2))=p_gama;
   % Modelagem do treceiro pico Spico(3)
   m1=lc(3); m2=lc(4);           % Abcissas com regiao espectral para modelagem
   % Inicializacao da ordenada de pico modelada por JONSWAP
   if auxfp(3) <= auxfp(1);sigma=0.07;else;sigma=0.09;end
   Sp_jwp=alfa(k(1))*( 2*pi*(g^2)./((2*pi.*auxfp(3)).^5).* ...
     exp(-1.25.*(auxfp(1)./auxfp(3)).^4).* ...
     gama(k(1)).^exp( -((auxfp(3)-auxfp(1)).^2)./(2.*(sigma.^2).*(auxfp(1)^2)) ));
   if auxfp(3) <= auxfp(2);sigma=0.07;else;sigma=0.09;end
   Sp_jwp=Sp_jwp+alfa(k(2))*( 2*pi*(g^2)./((2*pi.*auxfp(3)).^5).* ...
     exp(-1.25.*(auxfp(2)./auxfp(3)).^4).* ...
     gama(k(2)).^exp( -((auxfp(3)-auxfp(2)).^2)./(2.*(sigma.^2).*(auxfp(2)^2)) ));
   [epj3,p_gama,p_alfa,Hsmod,VMT_model]=f_jonswap2(VF,auxfp(3),auxS(3),m1,m2,nfft,DT,vmt(3),Sp_jwp);
   gama(k(3))=p_gama;alfa(k(3))=p_alfa;
   
end
