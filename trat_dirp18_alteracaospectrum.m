function[VD,VPED,VNUM,VESP,VEPK] = trat_dirp18_alteracaospectrum(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,nfft,dboia,mgl)
%
% Funcao para geracao de parametros relativos a analise
% direcional das series temporais de heave 
%
% C.I. Fisch / J.A. LIma 21/07/99
% Ultima atualizacao:
% Carlos E. Parente Ribeiro 13/08/99
%   Adaptacao do codigo anterior para as series corrigidas pelas funcoes
% de transferencia da P18 (realizada no programa "corrseries.m")
% Carlos E. Parente Ribeiro 29/09/99
%   Atualização da rotina para utilizar os 4 coeficientes a1,b1,a2 e b2.
% Foi substituido um bloco do programa original do Parente, denominado
% "test52.b
%
%
% &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
%        Analise Direcional das Series Temporais Heave,Pitch,Roll (2-D)
%
% determinaçao da direcao principal dp por faixa de frequencia e
% spread pelo Metodo do KUIK(1988) usado nas "directional buoys da Waverider"
% 
j=sqrt(-1);

%==========================================================================
%cp: Alteração do VF para eliminar a frequencia zero
%==========================================================================
VF1=VF(2:nfft/2+1);

%==========================================================================
% Espectros cruzados para as series corrigidas da boia WAVESCAN da P-18
% OBS: A FUNÇÃO SPECTRUM TEM A CARACTERISTICA DE PRODUZIR ESPECTROS
%      CRUZADOS COM SINAISOPOSTOS DOS OBTIDOS USANDO DIRETAMENTE FFT:
%      FFT(etaEW).*conj(FFT(heave)) EQUIVALE A SPECTRUM(heave,etaEW)
%==========================================================================
%hh1=spectrum(heave(1:nfft),etaEW(1:nfft),nfft,noverlap,w,1/DT);
%hh2=spectrum(heave(1:nfft),etaNS(1:nfft),nfft,noverlap,w,1/DT);

n21=nfft/2+1;
Hk=fft(heave); EWk=fft(etaEW); NSk=fft(etaNS);
% Estimate the two-sided Auto Power spectrum
chh= (DT * (conj(Hk) .* Hk)) / nfft;
crr= (DT * (conj(EWk) .* EWk)) / nfft;
cpp= (DT * (conj(NSk) .* NSk)) / nfft;

% Estimate the two-sided Cross Power spectrum
php= (DT * (conj(Hk) .* NSk)) / nfft;
phr= (DT * (conj(Hk) .* EWk)) / nfft;
ppr= (DT * (conj(NSk) .* EWk)) / nfft; 

% Multiply by 2 in order to get the one-sided spectra
chh = 2 * chh(2:n21);
crr = 2 * crr(2:n21);
cpp = 2 * cpp(2:n21);
php = 2 * php(2:n21);
qhp=imag(php);chp=real(php);
phr = 2 * phr(2:n21);
qhr =imag(phr);chr=real(phr);
ppr = 2 * ppr(2:n21);
cpr = real(ppr);

% Suavizando utilizando funcao
chh = smooth(chh,n21-1,mgl);
crr = smooth(crr,n21-1,mgl);
cpp = smooth(cpp,n21-1,mgl);
qhp = smooth(qhp,n21-1,mgl);
chp = smooth(chp,n21-1,mgl);
qhr = smooth(qhr,n21-1,mgl);
chr = smooth(chr,n21-1,mgl);
cpr = smooth(cpr,n21-1,mgl);

%hh1=spectrum(etaEW(1:nfft),heave(1:nfft),nfft,noverlap,w,1/DT);
%hh2=spectrum(etaNS(1:nfft),heave(1:nfft),nfft,noverlap,w,1/DT);
%hh3=spectrum(etaEW(1:nfft),etaNS(1:nfft),nfft,noverlap,w,1/DT);

%==========================================================================
% One-sided Power Spectra (espectro original multiplicado pelo DT)
% retirando a componente de frequencia zero
%==========================================================================
%hh1=2*DT*hh1(2:nfft/2+1,:);
%hh2=2*DT*hh2(2:nfft/2+1,:);
%hh3=2*DT*hh3(2:nfft/2+1,:);

%==========================================================================
% Formação de auto-espectros e espectros cruzados:
% chh = auto-espectro de heave
% crr = auto-espectro de etaEW
% cpp = auto-espectro de etaNS
% crh = parte real do espectro cruzado (co-espectro) de etaEW e heave
% cph= parte real do espectro cruzado (co-espectro) de etaNS e heave
% qrh = parte imaginaria do espectro cruzado (quad-espectro) de etaEW e heave
% qph = parte imaginaria do espectro cruzado (quad-espectro) de etaNS e heave
% crp = parte real do espectro cruzado (co-espectro) de etaEW e etaNS 
%==========================================================================
%chh=hh1(:,1);crr=hh1(:,2);cpp=hh2(:,2);
%qrh=imag(hh1(:,3));crh=real(hh1(:,3));
%crp=real(hh3(:,3));
%qph=imag(hh2(:,3));cph=real(hh2(:,3));

%chh=hh1(:,2);crr=hh1(:,1);
%qrh=imag(hh1(:,3));crh=real(hh1(:,3));
%cpp=hh2(:,1);
%qph=imag(hh2(:,3));cph=real(hh2(:,3));
%crp=real(hh3(:,3));

%==========================================================================
%coeficientes: a1,b1,a2 e b2, conforme Long (1980)
%==========================================================================
z=crr+cpp;

zz=sqrt(chh.*(crr+cpp));

g1=find(zz==0);zz(g1)=1;
g1=find(z==0);z(g1)=1;

a1=qhp./zz;
b1=qhr./zz;


a2=(cpp-crr)./z;
b2=2*cpr./z;

%==========================================================================
%cp: Trecho para escolher o ângulo theta obtido a partir de
%    2*theta entre as duas opções abaixo:
%     theta=(atan(b2/a2))/2 ou  theta=(atan(b2/a2))/2 +pi
%==========================================================================
dirp1=angle(a1+j*b1);    % Direcao principal obtida a partir de a1 e b1 (theta1)
dirp2=angle(a2+j*b2)/2;  % Direcao principal obtida a partir de a2 e b2 (theta2)

%figure;plot(VF1,dirp1,'b');hold on;grid on;plot(VF1,dirp2,'r')



dirp3=[dirp1';dirp2'];
dirp3=unwrap(dirp3);
dirp5=dirp3(1,:)-dirp3(2,:);

dirp4=[dirp1';dirp2'+pi];
dirp4=unwrap(dirp4);
dirp6=dirp4(1,:)-dirp4(2,:);

dirp11=zeros(nfft/2,1);
for i=1:nfft/2,
%    i,whos dirp5 % Isso e para ser DELETADO
   if abs(dirp5(i))<=abs(dirp6(i));
      dirp11(i)=dirp3(2,i);
   else;
      dirp11(i)=dirp4(2,i);
   end;
end;

%==========================================================================
% Montando os vetores a2 e b2 modificados para serem usados 
% no calculo da direção principal.
%==========================================================================
a3=cos(dirp11);b3=sin(dirp11);

%==========================================================================
%direção principal com 4 coeficientes
%==========================================================================
dirp7=angle(a1+j*b1+a3+j*b3);

%==========================================================================
% corrige direçao principal para graus e declinacao:
% dirp7=direção calculada com 4 coeficientes (a1,b1,a2,b2)
%==========================================================================
%dirp7=dirp7*360/(2*pi);
%dirp7=dirp7+DONV;                         % Corrige a declinacao magnetica
%g1=find(dirp7<0);dirp7(g1)=dirp7(g1)+360; % Corrige valores para 0-360 graus

%==========================================================================
% dirp1= direção principal calculada com b1/a1, a ser usada para
% altas frequencias (freq > 0.2 Hz ou periodos inferiores a 5 segundos).
%==========================================================================
%dirp1=dirp1*360/(2*pi);
%dirp1=dirp1+DONV;
%g1=find(dirp1<0);dirp1(g1)=dirp1(g1)+360;

%==========================================================================
% Monta o vetor dirp8 com as direções principais fazendo a composição de
% dirp1 e dirp7:
% - usa dirp7 com os 4 coeficientes só até a 0.2 hz
% - usa dirp1 com 2 coeficientes para freq maior que 0.2 hz
%==========================================================================
kf=find(VF1 > 0.2);
% dirp8=[dirp7(1:kf(1));dirp1(kf(1)+1:end)];
dirp8=dirp1(1:end);

% Ajuste da direcao dirp8 o sentido geografico (converte de rumo
% para direcao de onda a onda vem, e corrige a declinacao magnetica)
% Como resultado, a direcao dirp8 passa a ser medida em graus no 
% sentido horario a partir do NV (direcao de onde o trem de 
% onda está vindo).
if dboia == 0 % Boia da CONSUB 
    disp('Aqui'),pi/2

  % Converte de referencial trigonometrico (giro antihorario com origem
  % Leste) para rumo geografico (direacao para onde vai, sentido horario,
  % origem Norte)
   dirp8=3*pi/2 - dirp8;
   
elseif dboia == 2  % Boia Waverider
    disp('Waverider'),pi/2
   % dirp8=pi/2 + angle(dirp8); % Converte de rumo (para onde vai) para direcao de onde vem
   dirp8=pi/2+dirp8;
elseif dboia == 4 % Boia Triaxys
   disp('Triaxys')
   %dirp8=pi + angle(dirp8);
   dirp8=3*pi/2-dirp8 + pi;
end
% Corrigindo de rumo (direcao para onde vai) para direcao de onde vem
% (convencao adotada para onda), somando com declinacao magnetica
dirp8=(dirp8)*(180/pi) + DONV;
g1=find(dirp8<0);dirp8(g1)=dirp8(g1)+360;
g1=find(dirp8>360);dirp8(g1)=dirp8(g1)-360;




%==========================================================================
%cálculo do spread spr com os 4 coeficientes
%==========================================================================
d1=a1+j*b1;d1=d1.*conj(d1);
d2=a2+j*b2;d2=d2.*conj(d2);	

rr1=sqrt(d1+d2);
spr=sqrt(2-2*rr1);
spr=spr*57.3; % conversão de radianos para graus

spro=spr;a1o=a1;b1o=b1;a2o=a2;b2o=b2;d1o=d1;d2o=d2;
%rr1o=rr1;hh1o=hh1;hh2o=hh2;hh3o=hh3;
clear spro a1o b1o a2o b2o d1o d20 rr1o hh1o hh20 hh3o
 
%==========================================================================
%número de onda medido km e calculado kl
%==========================================================================
km=zeros(nfft/2,1);
kl=(2*pi.*VF1).^2/9.81;kl=kl'; % Calculado pela teoria linear
g1=find(chh~=0); 
km(g1)=sqrt((crr(g1)+cpp(g1))./chh(g1));

%==========================================================================
% Atribuindo os vetores a serem carregados no SIMO
% IMPORTANTE: Todos os vetores nesta rotina foram
% inicialmente calculados usando nfft/2 pontos espectrais,
% ou seja, suprimindo a frequencia zero. Para os vetores
% a serem carregados no SIMO, os dados associados a esta
% ferquencia zero são re-introduzidos, de forma as dimensões
% ficarem identicas ao do vetor VF original.
%==========================================================================
VD=[0;dirp8];       % direção de onda por faixa de frequência;
VPED=VD(kVTPK);
VNUM=[0;km];        % numero de onda
VESP=[0;spr];       % Espalhamento Angular por frequencia
VEPK=VESP(kVTPK);
