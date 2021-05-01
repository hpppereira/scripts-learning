function [VF2D,VDIR2D,VESP2D] = trat_dir_MLM(DT,heave,etaEW,etaNS,DONV)
%
% Rotina adaptada da trat_dir_EMEM, apenas susbtituindo para Metodo da
% Maxima Verossimilhanca
%
%
% Rotina para calculo do espectro direcional utilizando
% rotinas do WAFO pelo Metodo de Maxima Entropia
%
% 
% Autores: Ricardo Campos / Jose Antonio Jun/2012

%% Alterações
%>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
% 18/Mar/2011 - opcoes.bet=1;% Direção para onde a ONDA vai!!
% Transformação de ÂNGULO para AZIMUTE (direção de onde vem) e 
% correção da declinação magnetica DONV  
% auxd=(3*pi/2-S.theta)*180/pi+DONV;   (Eric O. Ribeiro).
%>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
%%

% -----------------------------------
% Dados de entrada da DAT2DSPEC
% -----------------------------------
t(:,1)=(0:DT:(length(etaEW)-1)*DT);
x=etaEW;  
y=etaNS; 
z=heave;
W=[t z x y];

sensorpos=zeros(3,3);
types= [1 16 17]; % Water particle displacement - caso TriAxys e Waverider
%types= [1 4 5];
bfs=[1 0 0];
% ------------------------
pos=[sensorpos types' bfs'];
% ------------------------
h=inf;     % considera-se por default agua profunda
NFFT=256;
Nt=65;    % numero de angulos
opcoes=specoptset('dat2dspec');
opcoes.nharm=10;
opcoes.gravity=9.8063;
opcoes.wdensity=1.0278e+003;
opcoes.bet=1;% Direção para onde a ONDA vai!!
opcoes.igam=1;
opcoes.x_axisdir=90; % referência para onde o eixo das abcissas aponta em termos de azimute!
opcoes.y_axisdir=0;  % referência para onde o eixo das ordenadas aponta em termos de azimute!
opcoes.plotflag='off';
opcoes.dflag='mean';
opcoes.ftype='f';
opcoes.maxiter=135;
opcoes.noverlap=floor(NFFT/2); % Faz muita diferença no cálculo da direção e um pouco no da frequência.

method='MLM';

%Plotflag='off';

%par = [opcoes.nharm,opcoes.gravity,opcoes.wdensity ,opcoes.bet,opcoes.igam,opcoes.x_axisdir,opcoes.y_axisdir];

%opcoes = [nharm,g,rho,bet,igam,thx,thy,plotflag,dflag,ftype,Plotflag];

% ------------------------------------------------
% Calculando espectro direcional pela rotina WAFO
% --------------------------------------------------
%[ourS,ourD,ourSw,ourFcof] = ourdat2dspec(W,pos,h,NFFT,Nt,par,opcoes.plotflag,method,opcoes.dflag,opcoes.ftype);
[S,D,Sw,Fcof] = dat2dspec(W,pos,h,NFFT,Nt,method,opcoes);
% OBS: A rotina original dat2spec do WAFO fornece o espectro direcional S.S com Nt linhas (direções)
%      por NFFT/2+1 colunas (frequencias). A primeira linha (-180 graus) é identica a ultima linha (+180).

% --------------------------------------------------
% Atribuindo variaveis para salvar resultados no programa "onda1h"
% --------------------------------------------------
VF2D=S.f(2:end);
%VF2D=S.w/(2*pi);
% +++++++ A linha abaixo converte de radianos para graus (-180,180) e corrige a
% Transformação de ÂNGULO para AZIMUTE (direção de onde vem) e 
% correção da declinação magnetica DONV +++++++++
auxd=((3*pi/2)-S.theta(1:end-1))*180/pi+DONV; %mod((90-S.theta*180/pi),360); % Angulo em graus (entre 0 e 360)(EOR/RMC - 17FEV2011)
% +++++++ A linha abaixo converte de (-180,180) para (0,360) com valores já
% corrigidos pela DONV +++++++++
auxd(auxd<0)=auxd(auxd<0)+360;%(EOR/RMC - 17FEV2011)
auxd(auxd>360)=auxd(auxd>360)-360;%(RMC - 08AGO2011)

%OBS: o vetor auxd já possui uma linha (ou direção a menos) para evitar a redundancia de valores iguais para
%    -180 e 180 (foi mantido a primeira linha da matriz S.S que equivale a direção -180 e retirada a ultima linha
%    que equivale a +180). Foi criada uma matriz auxliar Saux com menos uma coluna. 
Saux=S.S(1:Nt-1,2:end);

[auxd_crescente linhas]=sort(auxd); % Ordenando por ordem crescente as direções
% Ajustando a matriz S.S (que está originalmente com as direções nas
% linhas e frequencias nas colunas) para ficar em ordem crescente de
% direção
auxS=Saux(linhas,:);
auxS_transposto = auxS';  % Matriz transposta para que as linhas fiquem com as frequencias e as colunas com as direçoes.
%
% Fazendo interpolação das direções calculadas em "auxd_crescente" para direções padronizadas abaixo no vetor VDIR2D
VDIR2D=( 0:360/(Nt-1):360-(360/(Nt-1)) );
if min(auxd_crescente) ~= 0
    interpS=[auxS_transposto(:,1) auxS_transposto];
    auxd_crescente=[0 auxd_crescente']';
else
    interpS=auxS_transposto;
end
if max(auxd_crescente) ~= 360
    interpS=[interpS auxS_transposto(:,end)];
    auxd_crescente=[auxd_crescente' 360]';
end
[ml nc]=size(interpS);
VESP2D=[];
for k=1:ml
   VESP2D(k,:)=interp1(auxd_crescente,interpS(k,:),VDIR2D);
end

% Aplicando a diferença na declinação magnética DONV:
% aux=round(DONV/(360/(Nt-1)));
% if aux>0
%  for i=1:length(VDIR2D)-aux
%   VESP2D(:,i)=VESP2D1(:,i-aux);%+aux);(EOR/RMC - 17FEV2011)
%  end
%  j=1;
%  for i=length(VDIR2D)-aux+1:length(VDIR2D)
%   VESP2D(:,i)=VESP2D1(:,j); 
%   j=j+1;
%  end  
% else
%  for i=1:(aux*-1)
%   VESP2D(:,i)=VESP2D1(:,length(VDIR2D)+aux+i);
%  end
%  for i=1:length(VDIR2D)+aux
%   VESP2D(:,(aux*-1)+i)=VESP2D1(:,i);
%  end
% end
%
% % Plotando espectro direcional calculado pelo WAFO
%  for j=1:length(VDIR2D);for k=1:length(VF2D);xx(j,k)=VF2D(k)*cos(VDIR2D(j)*pi/180);end;end
%  for j=1:length(VDIR2D);for k=1:length(VF2D);yy(j,k)=VF2D(k)*sin(VDIR2D(j)*pi/180);end;end
%  % Calculando limite superior para plotar frequencia do espectro 2D na
%  % primeira casa decimal
%  supf=ceil(max(VF2D)*10 )/10;
%  figure;
%  mypolar2(pi/2,supf,'w.','w',0.1,supf);hold on
%  pcolor(xx',yy',VESP2D);shading flat;colormap(colormap_light_bottom);
%  contour(xx',yy',VESP2D,'k')
%  axis([-0.32 0.32 -0.32 0.32])
%  title('Espectro 2D - rotina dat2dspec do WAFO - Extended Maximum Entropy Method','fontsize',9)
