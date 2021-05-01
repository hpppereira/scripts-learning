function [VF,VS,VS0,VTPK,kVTPK,VSPK,VMTA,VMTB,VMTC,VMTD,VMTE,NDT,noverlap,w,nfft]=trat_freq(heave,DT,ngl,pi2)
%
% Funcao para geracao de parametros no dominio da frequencia
% a partir das series temporais de heave 
%
% C.I. Fisch / J.A. LIma 21/07/99
%
% ##########################################################################
%               Análise no Dominio da Frequencia (1-D)
%
%cálculo do espectro com "ngl" graus de liberdade;
nw = fix(length(heave)/(ngl/2)); % No. de pts. de cada segm. (Metodo do Welch)
if mod(nw,2) == 1                % Corrigindo o no. de pontos de um
   nw=nw-1;                      % segmento para um no. par
end
noverlap = nw/2;                 % 50% de "overlap".
w = hanning(nw);                 % Tipo de janela c/ "nw" pontos.
nfft = fix(length(heave)/nw)*nw; % no. de pontos da series a serem usados para calculo espectral
np=mod(nfft,2);if np == 1;nfft=nfft-1;end % Estabelecendo um numero par para o nfft
NDT=DT*nfft;                     % Extensao de tempo total da serie temporal
VF=(0:1/(nfft*DT):1/(2*DT));     % Vetor de frequências
VF=VF';
%f1 = frequência angular
f1=pi2*VF;

%
% Espectro VS calculado pela funcao "spectrum" do MATLAB dividindo
% a serie temporal em (length(heave)/nw) segmentos, conforme metodo de Welch
VS=spectrum(heave(1:nfft),nfft,noverlap,w,1/DT);VS=2*DT*VS(:,1);
%
% Espectro VS0 calculado pela funcao "spectrum" do MATLAB utilizando toda
% a serie temporal de heave, e alizando depois com a aplicacao de media movel
VS0=spectrum(heave(1:nfft),nfft,0,hanning(nfft),1/DT);VS0=2*DT*VS0(:,1);
VS0=smooth_ze(VS0,length(VS0),32); % Suavização através de médias móveis conservadoras de energia.
%
% Modulo para identificacao dos picos do espectro de elevacao
d=diff(VS);d=sign(d);d=diff(d);d=[0;d];
d=find(d==-2);
[d1 d2]=sort(VS(d));d1=flipud(d1);
d2=flipud(d2);
VTPK=1/VF(d(d2(1)));
kVTPK=d(d2(1));
VSPK=d1(1);
%cálculo de momentos m0,m1,m2,m3,m4 em termos de frequência VF;
VMTA=sum(VS.*(1/NDT));
VMTB=sum(VF.*VS)/NDT;
VMTC=sum(VF.^2.*VS)/NDT;
VMTD=sum(VF.^3.*VS)/NDT;
VMTE=sum(VF.^4.*VS)/NDT;
%numero de cruzamento de zeros ascendente por segundo (dominio da frequencia);
%n0c=sqrt(VMTC/VMTA);
%período médio de cruzamento de zeros ascendentes (dominio da frequencia);
%t0c=1/n0c;
%%largura espectral;nmp=num. máximos positivos/un.de tempo
%%e1=e;e2=parametro cnexo;e3=v(LH);e4=Qp(Goda)
%e1=sqrt(1-VMTC^2/(VMTA*VMTE));
%e2=sqrt(1-(max(size(a4))/max(size(a7)))^2);
%e3=sqrt((VMTA*VMTC/VMTB^2)-1);
%e4=sum(VF.*VS.^2)/64;e4=2*e4/VMTA^2;

%número total de cruzamentos no período de obs. (dominio da frequencia)
%n0t=n0c*length(heave)*DT
%numero de cruzamentos medido
%n0m=max(size(a4));

%onda significativa e onda média (dominio da frequencia);
%HS=4*sqrt(VMTA);
%HM=2.51*sqrt(VMTA);

% Listando parametros no dominio da frequencia para o SIMO
%Momento0_VMTA=VMTA
%Momento1_VMTB=VMTB
%Momento2_VMTC=VMTC
%Momento4_VMTE=VMTE
Periodo_Pico_VTPK=VTPK;
%Ordenada_de_Pico_VSPK=VSPK
% #########################################################################
