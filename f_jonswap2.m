function [epj,p_gama,p_alfa,Hs_mod,m0_mod]=f_jonswap2(freq,fp,ordp,m1,m2,nfft,deltat,m0,ordp_jwp);
%
% Rotina para ajuste de parametros p_alfa e p_gama do espectro JONSWAP
%
%
% OBS: A variável "difh",isto é, seu "menor valor" indicará o melhor par de
%      valores "alfa" e "gama" do modelo, ou seja, os que produzem o melhor
%      ajuste para aquela frequência de pico (ou período).
%
% Inicializando variaveis de trabalho
gamai=0.7;  lim=64;  step=0.1; g=9.81;  
sigmaA=0.07; sigmaB=0.09; % Parametro sigma de JONSWAP
mp=fix(fp*nfft*deltat)+1; % Abcissa associada a fp
nf=length(freq);          % No. total de pontos do espectro
Hs=4*sqrt(m0);            % Altura Significativa medida
% Vetor com parametro sigma
sigma=ones(nf,1);
sigma(1:mp)=sigmaA*sigma(1:mp);
sigma(mp+1:nf)=sigmaB*sigma(mp+1:nf);
gamaj=[];alfaj=[];difh=[];
% Loop para identificar o par (alfa,gama)
for k = 1:lim
   gama = gamai + (k-1)*step;
   gamaj(k) = gama;
   epj=zeros(nf,1);
   epj(2:nf)= 2*pi*(g^2)./((2*pi.*freq(2:nf)).^5).* ...
     exp(-1.25.*(fp./freq(2:nf)).^4).* ...
     (ones(nf-1,1)*gama).^exp( -((freq(2:nf)-fp).^2)./(2.*(sigma(2:nf).^2).*(fp^2)) );
   epjmax=max(epj);
   alfa0=ordp/epjmax;
   alfa=alfa0/((epjmax*alfa0+ordp_jwp)/(epjmax*alfa0));
   epj=alfa*epj;
   Hsj(k)=sqrt(16*( (sum(epj*(1/(nfft*deltat)))) )); % Linha para teste
   alfaj(k) = alfa;
   difh(k) = abs(Hs-Hsj(k));
   %if (k>1) 
      %if difh(k)>=difh(k-1)
      %   ind=k-1 
      %   break       % Encontrado par (alfa,gama)
      %end
   %end
   if(lim==61) ind=61; end
end
%figure(m1+1);plot(difh);
[hmim ind]=min(difh);
indice_do_vetor_gama_ind=ind;
% Corrige para obter apenas valores de gama superiores a 1
if gamaj(ind) < 1
   k=find(gamaj == 1.0);
   ind=k;
end
%   
% Parâmetros Alfa, Gama e Altura Significativa para
% espectro modelado
p_alfa=alfaj(ind);
p_gama=gamaj(ind);
Hs_mod=4*sqrt(sum(epj*(1/(nfft*deltat))));
m0_mod=(sum(epj*(1/(nfft*deltat))));
epj(2:nf)= p_alfa*2*pi*(g^2)./((2*pi.*freq(2:nf)).^5).* ...
     exp(-1.25.*(fp./freq(2:nf)).^4).* ...
     (ones(nf-1,1)*p_gama).^exp( -((freq(2:nf)-fp).^2)./(2.*(sigma(2:nf).^2).*(fp^2)) );