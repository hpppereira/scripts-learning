function[VD,VPED,VNUM,VESP,VEPK,a1,b1,a2,b2,s1,s2,Rcheck,phi,s_phi,s1_VEPK,s2_VEPK] = trat_dir_fft_ndbc9601(VF,VS,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,nfft,dboia,ngl,prof)
%
% Profissionais responsáveis pela elaboração da rotina:
% - Jose Antonio M. Lima, Ricardo Campos Martins, Eric Oliveira
%
% Rotina baseada no manual NDBC
%
% DADOS DE ENTRADA DA ROTINA:
% VF       = vetor de frequencia iniciando pelo zero (0:1/(n*DT):1/(2*DT))
% noverlap = numero de pontos para overlap na janela de Welch
% w        = window ou janelamento para supressão de lobulos a ser usado
% heave    = serie temporal de heave, positivo para cima
% etaEW    = deta/dx (slope ou deslocamento na direção Leste), positivo Leste p/ cima
% etaNS    = deta/dy (slope ou deslocamento na direção Norte), positivo Norte p/ cima
% DT       = intervalo de tempo de amostragem da serie temporal (segundos)
% DONV     = declinação magnetica
% kVTPK    = indice de ordem do pico espectral no maximo do vetor VS
% nfft     = numero de pontos para FFT
% dboia    = tipo de boia (ver rotina de entrada) que afeta calculo da direçao final
% ngl     = numero de graus de liberdade (que dividido por 2 fornece a media para janelas espectrais
% -------------------------------------------------------------------------
% Os parametros de entrada da rotina SPECTRUM foram definidos na rotina
% trat_freq como abaixo:
% nw = fix(length(heave)/(ngl/2)); % No. de pts. de cada segm. (Metodo do Welch)
% if mod(nw,2) == 1                % Corrigindo o no. de pontos de um
%    nw=nw-1;                      % segmento para um no. par
% end
% noverlap = nw/2;                 % 50% de "overlap".
% w = hanning(nw);                 % Tipo de janela c/ "nw" pontos.
% nfft = fix(length(heave)/nw)*nw; % no. de pontos da series a serem usados para calculo espectral
% 
% -------------------------------------------------------------------------
%
% Codigo revisado por:
% Jose Antonio Moreira Lim e Ricardo Martins Campos. 04/Mar/2011
% 
% CODIGO VERIFICADO E MODIFICADO POR ANDRE MENDES EM 06/2012 VISANDO A TESE  
%
% IMPORTANTE: O teste desta rotina baseado no calculo de espectro pelo
% Metodo de Welch (usando a função SPECTRUM do Matlab) foi feito atraves de
% uma rotina denominada "testa_direcao2_com_FFT.m" onde foi utilizado o 
% metodo de Bartlett.

%% Alterações
%>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
% 18/Mar/2011 - Inserção da profundidade como parâmetro de entrada.
% restultados de saída de a1, a2, b1, b2 e Rcheck. Cálculo do Rcheck
%>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

%%
% Referencial para manter o processamento pradonizado, i.e., resultado da
% trat_dir_fft_ndbc9601 igual a trat_dir_EMEM 
heave=-heave;

j=sqrt(-1);

%==========================================================================
%cp: Alteracao do VF para eliminar a frequencia zero
%==========================================================================
VF1=VF(2:nfft/2+1);

%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
optspec=1; % Metodo de Welch para calculo espectral atraves da "spectrum"
%optspec=2; % Metodo de Bartlett para calculo espectral atraves da "fft"

if optspec == 1 
    % CALCULO ESPECTRAL PELO METODO DE WELCH
    %==========================================================================
    % Espectros cruzados para as series corrigidas 
    %==========================================================================
    hh1=spectrum(heave(1:nfft),etaEW(1:nfft),nfft,noverlap,w,1/DT);
    hh2=spectrum(heave(1:nfft),etaNS(1:nfft),nfft,noverlap,w,1/DT);
    hh3=spectrum(etaEW(1:nfft),etaNS(1:nfft),nfft,noverlap,w,1/DT);
    % testar esse calculo. Ou inverter a ordem da primeira e segunda entrada ou
    % colocar o sinal negativo no resultado.
    %==========================================================================
    % One-sided Power Spectra (espectro original multiplicado pelo DT)
    % retirando a componente de frequencia zero
    %==========================================================================
    hh1=2*DT*hh1(2:nfft/2+1,:);
    hh2=2*DT*hh2(2:nfft/2+1,:);
    hh3=2*DT*hh3(2:nfft/2+1,:);

    %==========================================================================
    % Formacao de auto-espectros e espectros cruzados:
    % chh = auto-espectro de heave
    % crr = auto-espectro de etaEW
    % cpp = auto-espectro de etaNS
    % chr = parte real do espectro cruzado (co-espectro) de heave e etaEW
    % chp= parte real do espectro cruzado (co-espectro) de heave e etaNS
    % qhr = parte imaginaria do espectro cruzado (quad-espectro) de heave e etaEW
    % qhp = parte imaginaria do espectro cruzado (quad-espectro) de heave e etaNS
    % crp = parte real do espectro cruzado (co-espectro) de etaEW e etaNS 
    %==========================================================================
    chh=hh1(:,1);crr=hh1(:,2);cpp=hh2(:,2);
    qhr=imag(hh1(:,3));chr=real(hh1(:,3));
    crp=real(hh3(:,3));
    qhp=imag(hh2(:,3));chp=real(hh2(:,3));
    
elseif optspec == 2
    % CALCULO ESPECTRAL PELO METODO DE BARTLETT
    % =====================================================================
    np=length(heave);
    if mod(np,2) == 1                % Corrigindo o no. de pontos total 
       np=np-1;                      % para um no. par
    end                                
    n21=np/2+1;
    Hk=fft(heave(1:np)); EWk=fft(etaEW(1:np)); NSk=fft(etaNS(1:np));
    % Estimate the two-sided Auto Power spectrum
    chh= (DT * (conj(Hk) .* Hk)) / nfft;
    crr= (DT * (conj(EWk) .* EWk)) / nfft;
    cpp= (DT * (conj(NSk) .* NSk)) / nfft;

    % Estimate the two-sided Cross Power spectrum
    % #########  Ver Bendat & Piersol pag 536  ################
    % espectro heave-pitch e heave-roll
    php= (DT * (conj(Hk) .* NSk)) / nfft;
    phr= (DT * (conj(Hk) .* EWk)) / nfft;
    % espectro roll-pitch
    prp= (DT * (conj(EWk) .* NSk)) / nfft; 
    % Multiply by 2 in order to get the one-sided spectra
    % autoespectros
    chh = 2 * chh(2:n21);
    crr = 2 * crr(2:n21);
    cpp = 2 * cpp(2:n21);
    % cross-espectros
    php = 2 * php(2:n21);qhp=imag(php);chp=real(php);
    phr = 2 * phr(2:n21);qhr =imag(phr);chr=real(phr);
    prp = 2 * prp(2:n21);crp = real(prp);
    %
    % Suavizando utilizando funcao
    chh = oursmooth(chh,n21-1,ngl);
    crr = oursmooth(crr,n21-1,ngl);
    cpp = oursmooth(cpp,n21-1,ngl);
    qhp = oursmooth(qhp,n21-1,ngl);chp = oursmooth(chp,n21-1,ngl);
    qhr = oursmooth(qhr,n21-1,ngl);chr = oursmooth(chr,n21-1,ngl);
    crp = oursmooth(crp,n21-1,ngl);
end

%==========================================================================
% coeficientes para calculo do espectro direcional: a1,b1,a2 e b2, 
% conforme Report NDBC_96_01 e Steele (1992)
%==========================================================================
z=crr+cpp;

zz=sqrt(chh.*(crr+cpp));

g1=find(zz==0);zz(g1)=1;
g1=find(z==0);z(g1)=1;

b1=qhp./zz;
a1=qhr./zz;

a2=(crr-cpp)./z;

b2=2*crp./z;

%==========================================================================
% Rcheck ou Ratio R = K_teorico(2*pi/L) / K_medido(pela boia)!!
%==========================================================================
% Necessários para  gerar o arquivo de entrada do Xwaves. Formatação
% similar a do Wavescan - GOM.
k = hunt(VF1,prof);
Rcheck = k.*sqrt(chh./(crr+cpp));

%==========================================================================
%cp: Trecho para escolher o angulo theta obtido a partir das duas opcoes abaixo:
%     theta1= atan2(b1,a1)
%     theta2=(atan(b2/a2))/2 ou  theta=(atan(b2/a2))/2 +pi
%==========================================================================
dirp1=atan2(b1,a1);    % Direcao principal obtida a partir de a1 e b1 (theta1)
dirp2=atan2(b2,a2)/2;  % Direcao principal obtida a partir de a2 e b2 (theta2)
%figure;plot(VF1,dirp1,'b');hold on;grid on;plot(VF1,dirp2,'r')

% O trecho abaixo de codigo foi elaborado pelo Parente para evitar
% ambiguidade de direção
dirp3=[dirp1';dirp2'];
dirp3=unwrap(dirp3);
dirp5=dirp3(1,:)-dirp3(2,:);

dirp4=[dirp1';dirp2'+pi];
dirp4=unwrap(dirp4);
dirp6=dirp4(1,:)-dirp4(2,:);

dirp11=zeros(nfft/2,1);
for i=1:nfft/2,
   if abs(dirp5(i))<=abs(dirp6(i));
      dirp11(i)=dirp3(2,i);
   else;
      dirp11(i)=dirp4(2,i);
   end;
end;

%==========================================================================
% Montando os vetores a2 e b2 modificados para serem usados 
% no calculo da direcao principal.
%==========================================================================
a3=cos(dirp11);b3=sin(dirp11);

%==========================================================================
%direcao principal com 4 coeficientes
%==========================================================================
dirp7=angle(a1+j*b1+a3+j*b3);

%==========================================================================
% Monta o vetor dirp8 com as direcoes principais fazendo a composicao de
% dirp1 e dirp7:
% - usa dirp7 com os 4 coeficientes ate freq 0.2 hz
% - usa dirp1 com 2 coeficientes para freq maior que 0.2 hz
%==========================================================================
% kf=find(VF1 > 0.2);
% dirp8=[dirp7(1:kf(1));dirp1(kf(1)+1:end)]; % Usando as 2 funcoes (dirp7  e dirp1)
dirp8=dirp1; % Usando  apenas a funçao dirp1

% A linha de comando abaixo (retirada da pagina 10 do manual "Nondirectional
% and Directional Wave Data Analysis Procedures" NDBC Technical Document 96-01)
% converte a direção de onde vai (referenciada no sentido antihorario a partir
% do eixo X ou leste E, conforme usada nas formulas Longuet-Higgins) para DIREÇÂO
% DE ONDE VEM REFERENCIADO AO NORTE VERDADEIRO NO SENTIDO HORARIO (REFERENCIAL PADRAO
% WMO DE ONDAS). 
dirp8=3*pi/2 - dirp8; 
   
% Correção da declinação magnetica
dirp8=dirp8*(180/pi)+DONV;
g1=find(dirp8<0);dirp8(g1)=dirp8(g1)+360;
g1=find(dirp8>360);dirp8(g1)=dirp8(g1)-360;
 
%==========================================================================
%numero de onda medido km e calculado kl
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
% ferquencia zero sao re-introduzidos, de forma as dimensÃµes
% ficarem identicas ao do vetor VF original.
%==========================================================================

%==========================================================================
% Calculo do Spreading: Desvio padrão circular Sigma e parametros s1,s2 
%==========================================================================

% Formula do sigma2 do Krogstad et all (1998) "Directional distribution in Wave Spectra", pag.3 
%wetaEW=2*DT*real(spectrum(etaEW,length(heave),noverlap,w,VF'));  % Auto espectro E-W 
%wetaNS=2*DT*real(spectrum(etaNS,length(heave),noverlap,w,VF')); % Auto espectro N-S
%wetaEWNS=2*DT*real(spectrum(etaEW,etaNS,length(heave),noverlap,w,VF'));  % Cross - espectro E-W,N-S
%wetaEW   =   wetaEW(1:length(VF),1);
%wetaNS   =   wetaNS(1:length(VF),1);
%wetaEWNS = wetaEWNS(1:length(VF),3);
% R = sqrt( ((wetaEW - wetaNS).^2 + 4.*wetaEWNS.^2)./((wetaEW+wetaNS).^2) );
% sigma2 = sqrt( (1-R)./2 ).*180./pi;
% VESP=sigma2;

% Formula do sigma1 do livro Tucker&Pitt(2001) "Waves in Ocean Engineering" pags 196-198
c1=sqrt(a1.^2 + b1.^2); c2=sqrt(a2.^2 + b2.^2); % formula 7.2-6 do Tucker&Pitt(2001)
s1= c1./(1-c1); % formula 7.2-11 do Tucker&Pitt(2001)
s2= (1+3*c2+sqrt(1+14*c2+c2.^2)) ./ (2*(1-c2)); % formula 7.2-12 do Tucker&Pitt(2001)
sigma1=sqrt(2-2*c1)*180/pi; % formula 7.2-13a do Tucker&Pitt(2001)
sigma2=sqrt( (1-c2)/2 )*180/pi; % formula do Krogstad(1998) pag.3
VESP=sigma1; % Desvio padrão circular (neste caso assumido como sigma1)
% 
% Preparando parametros de saida da rotina
a1=[0;a1];b1=[0;b1];a2=[0;a2];b2=[0;b2];Rcheck=[0;Rcheck];
VESP=[0;VESP];s1=[0;s1];s2=[0;s2]; 
VD=[0;dirp8];       % direcao de onda por faixa de frequencia;
% VDdirp1=[0;dirp1];
VPED=VD(kVTPK); % Direção dominante do pico espectral
% VPEDdirp1=VDdirp1(kVTPK);
VNUM=[0;km];        % numero de onda
% A questão do espalhamento caracteristico do espectro ("integrated
% circular rms spreading sigma") pode ser obtido por duas opções:
% (1) espalhamento do pico espectral (posição kVTPK) 
% (2) media ponderada pela função densidade espectral do espalhamento circular VESP
% OBS: esta segunda opção é a mais realistica, pois identifica o espalhamento das
% particulas de ondas de todo o estado de mar 
% opção 1 (não selecionada)
% VEPK=VESP(kVTPK); % Espalhamento ou desvio padrão circular no pico espectral
% opção 2 (selecionada)
df=VF(3)-VF(2);
m0=sum(VS.*df);
E=VS.*df/m0; % Calculo do espectro omni-direcional normalizado pela area espectral
VEPK=sum(VESP.*E); % Conforme seção "Circular rms spreading" do paper Forristal&Ewans(1998) equacao (80)
% e tambem no livro Tucker&Pitt(2001) equação (7.2-21)
s1_VEPK=sum(s1.*E); % Ponderando o fator s1 pelo espectro como descrito acima
s2_VEPK=sum(s2.*E); % Ponderando o fator s2 pelo espectro como descrito acima
% =========================================================================
% Calculo do spreding factor phi, conforme paper Forristall and Ewans
% (1998),Worldwide Measurements of Directional Wave Spreading, Journal of
% Atmospheric and Oceanic Technology,vo.15,pp.440-469 no proximo segmento:
% Espectro VS calculado pela funcao "spectrum" do MATLAB dividindo
% a serie temporal em (length(heave)/nw) segmentos, conforme metodo de Welch
% VS=spectrum(heave(1:nfft),nfft,noverlap,w,1/DT);VS=2*DT*VS(:,1);
% df=VF(end)-VF(end-1); % ja calculado anteriormente
alphauu2=0.5*sum(VS.*(1+a2).*df); % Formula (50) paper Forristall&Ewans
alphavv2=0.5*sum(VS.*(1-a2).*df); % Formula (51) paper Forristall&Ewans
alphauv2=0.5*sum(VS.*b2.*df);  % Formula (52) paper Forristall&Ewans
r_spread=sqrt( 0.25*(alphauu2-alphavv2)^2 + alphauv2^2 );  % Formula (27) paper Forristall&Ewans
alphaaa2= 0.5*(alphauu2 + alphavv2) + r_spread;  % Formula (25) paper Forristall&Ewans
alpha_spread= sqrt(alphauu2 + alphavv2);  % Formula (28) paper Forristall&Ewans
phi=sqrt(alphaaa2)/alpha_spread;  % Formula (29) paper Forristall&Ewans
% Os fatores "n" da funcao cos(theta).^n e "s" da funcao cos(theta/2).^2s
% sao calculados pela Table A.3 da norma ISO/FDIS 19901-1.2005(E)
% n_phi=(2*phi^2-1)/(1-phi^2);
s_phi=( 3*phi^2-1+sqrt(phi^4+6*phi^2-3) )/ (2-2*phi^2);

% calculo do circular rms spreading sigma_med
% m0=sum(VS.*df); % ja calculado acima
% E=VS.*df/m0;    % ja calculado acima
% % a1_med=sum(VS.*a1.*df); 
% % b1_med=sum(VS.*b1.*df);
% a1_med=sum(E.*a1); % Opção de multiplicar pelo E 
% b1_med=sum(E.*b1); % Opção de multiplicar pelo E 
% m1_med=sqrt(a1_med^2+b1_med^2);
% sigma_med=sqrt( 2*(1-m1_med) ); % Formula (80) paper Forristall&Ewans
% s_Krogstad=(2/(sigma_med)^2)-1;
% a=0.5*(1+s_Krogstad*(s_Krogstad-1)/((s_Krogstad+1)*(s_Krogstad+2)));
% n_Krogstad=(2*a-1)/(1-a);

% Calculo do spreading usando o desvio padrão circular VEPK da formulação
% do Krogstad
% Formula de Longuet-Higgins que relaciona desvio padrao circular com s
% obtido da tese do Andre Mendes
% s1_VEPK=(2/(VEPK*pi/180).^2)-1;
% Funcao que correlaciona o "s" com o "n"
%a=0.5*(1+s1_VEPK*(s1_VEPK-1)/((s1_VEPK+1)*(s1_VEPK+2)));
%n_VEPK=(2*a-1)/(1-a);
% ======== Fim do segmento de calculo do spreading factor =================
