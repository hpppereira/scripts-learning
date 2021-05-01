function[VD,VPED,VNUM,VESP,VEPK] = trat_dir_atual(VF,noverlap,w,heave,etaEW,etaNS,DT,DONV,kVTPK,nfft,dboia)
%
% Metodologia de processamento de dados de boias direcionais, conforme
% descrita pelo Tucker (1989), ocean enginnering vol. 16, pp.173-192.
% Funcao final para analise direcional de dados de diferentes tipos de boia
% Baseia-se no calculo do espectro cruzado de heave/pitch, heave/roll e pitch/roll calculado pela antiga trat_dirp18
% Calculo do spreading retirado da trat_dir, o qual utiliza o metodo de Krogstad et al (1998)
% Codigo revisado por:
% Jose Antonio Moreira Lima, Carlos Eduardo Parente Ribeiro, Ricardo Martins Campos e Andre Mendes.


j=sqrt(-1);

%==========================================================================
%cp: Alteracao do VF para eliminar a frequencia zero
%==========================================================================
VF1=VF(2:nfft/2+1);

%==========================================================================
% Espectros cruzados para as series corrigidas 
% OBS: A FUNCAO SPECTRUM TEM A CARACTERISTICA DE PRODUZIR ESPECTROS
%      CRUZADOS COM SINAIS OPOSTOS DOS OBTIDOS USANDO DIRETAMENTE FFT:
%      FFT(etaEW).*conj(FFT(heave)) EQUIVALE A SPECTRUM(heave,etaEW)
%==========================================================================
hh1=-spectrum(heave(1:nfft),etaEW(1:nfft),nfft,noverlap,w,1/DT);
hh2=-spectrum(heave(1:nfft),etaNS(1:nfft),nfft,noverlap,w,1/DT);
hh3=-spectrum(etaNS(1:nfft),etaEW(1:nfft),nfft,noverlap,w,1/DT);
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
% crh = parte real do espectro cruzado (co-espectro) de etaEW e heave
% cph= parte real do espectro cruzado (co-espectro) de etaNS e heave
% qrh = parte imaginaria do espectro cruzado (quad-espectro) de etaEW e heave
% qph = parte imaginaria do espectro cruzado (quad-espectro) de etaNS e heave
% crp = parte real do espectro cruzado (co-espectro) de etaEW e etaNS 
%==========================================================================
chh=hh1(:,1);crr=hh1(:,2);cpp=hh2(:,2);
qrh=imag(hh1(:,3));crh=real(hh1(:,3));
crp=real(hh3(:,3));
qph=imag(hh2(:,3));cph=real(hh2(:,3));

%==========================================================================
%coeficientes: a1,b1,a2 e b2, conforme Long (1980) e Tucker (1989)
%==========================================================================
z=crr+cpp;

zz=sqrt(chh.*(crr+cpp));

g1=find(zz==0);zz(g1)=1;
g1=find(z==0);z(g1)=1;

b1=qrh./zz;
a1=qph./zz;

a2=(cpp-crr)./z;

b2=2*crp./z;

%==========================================================================
%cp: Trecho para escolher o anngulo theta obtido a partir de
%    2*theta entre as duas opcoes abaixo:
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
% - usa dirp7 com os 4 coeficientes só até a 0.2 hz
% - usa dirp1 com 2 coeficientes para freq maior que 0.2 hz
%==========================================================================
kf=find(VF1 > 0.2);
dirp8=[dirp7(1:kf(1));dirp1(kf(1)+1:end)];

% Ajuste da direcao dirp8 o sentido geografico (converte de rumo
% para direcao de onda a onda vem e corrige a declinacao magnetica)
% Como resultado, a direcao dirp8 passa a ser medida em graus no 
% sentido horario a partir do NV (direcao de onde o trem de 
% onda esta vindo).

% if dboia == 0   % Boia da CONSUB 
%     disp('Aqui'),pi/2
%    dirp8=3*pi/2 - angle(dirp8); % Converte de rumo (para onde vai) para direcao de onde vem
%    dirp8=dirp8;
% elseif dboia == 2  % Boia Waverider
%     disp('Waverider'),pi/2
%    dirp8=pi/2 + angle(dirp8); % Converte de rumo (para onde vai) para direcao de onde vem
%    dirp8=2*pi-dirp8;
% elseif dboia == 1  % Boia P18
%    disp('Boia do ES'),3*pi/2  
%      dirp8=3*pi/2 - dirp8;
% elseif dboia == 4 % Boia Triaxys
%    disp('Triaxys')
%    dirp8=pi + angle(dirp8);

   dirp8=3*pi/2 - dirp8;
   
% end

dirp8=dirp8*(180/pi)+DONV;
g1=find(dirp8<0);dirp8(g1)=dirp8(g1)+360;
g1=find(dirp8>360);dirp8(g1)=dirp8(g1)-360;




%==========================================================================
%calculo do spread spr com os 4 coeficientes
%==========================================================================
%d1=a1+j*b1;d1=d1.*conj(d1);
%d2=a2+j*b2;d2=d2.*conj(d2);	

%rr1=sqrt(d1+d2);
%spr=sqrt(2-2*rr1);
%spr=spr*57.3; % conversão de radianos para graus

%spro=spr;a1o=a1;b1o=b1;a2o=a2;b2o=b2;d1o=d1;d2o=d2;rr1o=rr1;hh1o=hh1;hh2o=hh2;hh3o=hh3;
%clear spro a1o b1o a2o b2o d1o d20 rr1o hh1o hh20 hh3o
 
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
% ferquencia zero são re-introduzidos, de forma as dimensões
% ficarem identicas ao do vetor VF original.
%==========================================================================



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



VD=[0;dirp8];       % direcao de onda por faixa de frequencia;
VPED=VD(kVTPK);
VNUM=[0;km];        % numero de onda
VEPK=VESP(kVTPK);
