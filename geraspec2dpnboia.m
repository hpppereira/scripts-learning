clear, clc, close all
%Rotina para gerar os espectros 2D dos dados
%do PNBOIA

local = 'rio_grande'
dmag = -17

pathname = '/home/hp/Dropbox/pnboia/dados/bruto/triaxys/pre_proc/';

%carrega listas da axys
arq = load([pathname,'listas/list_RSFeb12.txt']);

% Gerando matriz com os espectros direcionais

% posicionamento do sensor (boia)
lon = ones(3,1).*39.97; % em graus
lat = ones(3,1).*22.52;
z = zeros(3,1);
sensorpos = [lon lat z];
type = [1 4 5];%type = [1 4 5]; % comando para sensor de superfície
bfs = [1 0 0];
pos = [sensorpos type' bfs'];

h=inf;     % considera-se por default agua profunda
NFFT=328;
Nt=65;    % numero de angulos
opcoes=specoptset('dat2dspec');
opcoes.nharm=10;
opcoes.gravity=9.8063;
opcoes.wdensity=1.0278e+003;
opcoes.bet=1;% Direção para onde a ONDA vai!!
opcoes.igam=1;
opcoes.x_axisdir=0; % referência para onde o eixo das abcissas aponta em termos de azimute!
opcoes.y_axisdir=90;  % referência para onde o eixo das ordenadas aponta em termos de azimute!
opcoes.plotflag='off';
opcoes.dflag='mean';
opcoes.ftype='f';
opcoes.maxiter=135;
opcoes.noverlap=floor(NFFT/2); % Faz muita diferença no cálculo da direção e um pouco no da frequência.
method='EMEM';

%filename list
arqstr = num2str(arq);

for i = 1:1 %length(arqstr)
    
    arq1 = [pathname,local,'/hne/',arqstr(i,:),'.HNE'];

    dados = importdata(arq1,' ',11);
    t = dados.data(:,1);
    n1 = dados.data(:,2);
    n3 = dados.data(:,3);
    n2 = dados.data(:,4);
    
    %rota eixo da boia - corrige declinacao magnetica
    n2 =  cos(pi*dmag/180) .* n2 + sin(pi*dmag/180) .* n3; 
    n3 = -sin(pi*dmag/180) .* n2 + cos(pi*dmag/180) .* n3;

    W = [t, n1, n2, n3];

    [S,D,Sw,Fcof] = dat2dspec(W,pos,h,NFFT,Nt,method,opcoes);
    
    [ndir, nfreq] = size(S.S);
    
    A.S(:,:,i) = S.S;
    
    A.date(i,:) = [arqstr(i,1:4),'-',arqstr(i,5:6),'-',arqstr(i,7:8),' ',arqstr(i,9:10),':',arqstr(i,11:12)];

    A.f = S.f;
    A.theta = S.theta;
    A.Sw = Sw.S;
    
%    figure
%    contour(A.f, A.theta, S.S)
%    grid
    
end

%save('out/spec2d/spec2d_RIG.mat','A','-mat') 