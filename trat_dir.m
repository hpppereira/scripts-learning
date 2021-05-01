function[VD,VPED,VNUM,VESP,VEPK] = trat_dir(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,dboia)
%
% Funcao para geracao de parametros relativos a analise
% direcional das series temporais de heave 
%
% C.I. Fisch / J.A. LIma 21/07/99
%
% Ultima alteraçao: J.A. LIma / Eric  11/08/2004:
%  - Inclusao da opçao de processar dados gerados pela boia Waverider MK-II
%    nas linhas 36 ate 42
%  - Inclusao do calculo do Spreading por Krogstad et al (1998) nas linhas
%    84 ate 97
%    Krogstad, H.E. et al, 1998, Directional Distributions in Wave
%    Spectrum, Proc. WAVES97, Nov. 3-7 1997, 1, ASCE, 883-895.
%
% &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
%        Analise Direcional das Series Temporais Heave,Pitch,Roll (2-D)
%
% determinaçao da direcao principal dp por faixa de frequencia e
% spread pelo Metodo do KUIK(19XX) usado nas "directional buoys da Waverider"
% 
j=sqrt(-1);
%w1=spectrum(etaEW,heave,64,32);
w1=spectrum(etaEW,heave,length(heave),noverlap,w,VF');  %Original espectro cruzado E-W ,heave
%[Pxy,F] = csd(etax,eta,nfft,freq,w,noverlap);   q12 = imag(Pxy);
%w2=spectrum(etaNS,heave,64,32);
w2=spectrum(etaNS,heave,length(heave),noverlap,w,VF'); % Original espetro cruzado N-S, heave

% r4=parte imaginaria do espectro cruzado entre Roll(Pitch EW) e Heave
% r5=parte imaginaria do espectro cruzado entre Pitch(Pitch NS) e Heave
r4=2*DT*imag(w1(1:length(VF),3));r5=2*DT*imag(w2(1:length(VF),3));
% r1=direcao principal por faixa de frequencia (inicialmente
% como rumo em relacao ao eixo dos X(=eixo W-E) )
r1=r4+r5*j; % 

% Ajuste da direcao r1 o sentido geografico (converte de rumo
% para direcao de onda a onda vem, e corrige a declinacao magnetica)
% Como resultado, a direcao r1 passa a ser medida em graus no 
% sentido horario a partir do NV (direcao de onde o trem de 
% onda está vindo).
if dboia == 0 | dboia == 3  % Boia da CONSUB ou boia do ES (Rafael/NAVCON)
    disp('Aqui'),pi/2
    r1=3*pi/2 - angle(r1); % Converte de rumo (para onde vai) para direcao de onde vem
elseif dboia == 2  % Boia Waverider
    disp('Waverider'),pi/2
   r1=pi/2 + angle(r1); % Converte de rumo (para onde vai) para direcao de onde vem 
elseif dboia == 4 % Boia Triaxys
   disp('Triaxys')
   r1=pi + angle(r1);  
end
r1=r1+DONV*2*pi/360; % Converte de norte magnetico para norte verdadeiro
r1=round(r1*360/(2*pi));round(r1); % Converte de radianos para graus. 

% Converte as direcoes r1 para o intervalo 0 ate 360 graus, 
% e armazena no vetor VD
d1=find(r1>360);
if length(d1)>0,
r1(d1)=r1(d1)-360*ones(length(d1),1);else;end;
d1=find(r1<=0);
if length(d1)>0,
r1(d1)=360*ones(length(d1),1)+r1(d1);else;end;
VD=r1;% direção de onda por faixa de frequência;
VPED=VD(kVTPK);
Direcao_do_Pico_Espectral_VPED=VPED

% Calculo do vetor com o numero de onda VNUM por
% faixa de frequencia. O kl é o numero de onda
% por frequencia estimado pela teoria linear.
r20=[w1(1:length(VF),2)];
r10=sqrt((w1(:,1)+w2(:,1))./w1(:,2));r10=[r10(1:length(VF))];
kl=((2*pi*VF).^2)/9.81;
VNUM=r10;%número de onda por frequência;

% Calculo do spread VESP utilizando o metodo do momento
% circular (desvio padrao circular) aplicando sobre r4 e r5.
% (Metodo do KUIK)
% Obs. pelo Prof. Parente:
%"este cálculo de spread é problemático porque
%não inclue correções para as funções de transferência
%d%a bóia; acho que a única saída é a DAAT, a não ser que as
%séries da WAVESCAN já venham corrigidas, o que parece
%ser verdade!"
% 
% r4=r4./(r20.*r10);r5=r5./(r20.*r10);
% m1=sqrt(r4.^2+r5.^2);
% a13=sqrt(2*(1-m1));a13=a13*57.3;
% VESP=a13; % Espalhamento por frequencia
% VEPK=VESP(kVTPK);

%==========================================================================
% Calculo do Spreading Formula do Krogstad et all (1998)
%==========================================================================
wetaEW=2*DT*real(spectrum(etaEW,length(heave),noverlap,w,VF'));  % Auto espectro E-W 
wetaNS=2*DT*real(spectrum(etaNS,length(heave),noverlap,w,VF')); % Auto espectro N-S
wetaEWNS=2*DT*real(spectrum(etaEW,etaNS,length(heave),noverlap,w,VF'));  % Cross - espectro E-W,N-S

wetaEW   =   wetaEW(1:length(VF),1);
wetaNS   =   wetaNS(1:length(VF),1);
wetaEWNS = wetaEWNS(1:length(VF),3);

R = sqrt( ((wetaEW - wetaNS).^2 + 4.*wetaEWNS.^2)./((wetaEW+wetaNS).^2) );
VESP = sqrt( (1-R)./2 ).*180./pi;
VEPK = VESP(kVTPK);

%incluir direção por máxima entropia
% &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
