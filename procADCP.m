%% Processamento dos dados de ADCP Nortek na praia da Reserva
% Data: 2016-01-28

%% Input

clear, clc, close all
pathname = '/home/hp/Dropbox/daat/data/ADCP_Reserva/';
filename = 'ADCP_REEF_28_01_2016';

fs = 2; %Hz
nfft = 512;
h = 5; %prof 5 m

%% Carrega dados de velocidades e pressao

wad = load([pathname, filename, '.wad']); 

%% Separa arquivos de heave (pressao), vx (leste), vy (norte) e vz (up)

for i=1:max(wad(:,1))-2 % nao processa os 2 ultimos pontos
    
    % carrega dados
    pr(:,i) = wad(find(wad(:,1)==i),3);
    vx(:,i) = wad(find(wad(:,1)==i),6);
    vy(:,i) = wad(find(wad(:,1)==i),7);
    vz(:,i) = wad(find(wad(:,1)==i),8);
    
    % retira a media da pressao
    pr(:,i) = pr(:,i) - mean(pr(:,i));
    
    %chama subrotina de processamento de onda no dominio do tempo (Tza, Hs..)
    [hs,h10,hmax,thmax,tmed]=ondat(pr(:,i),fs,h);

    %chama subrotina de processamento de onda no dominio da frequencia (dir,hm0..)
    [f,an,anx,any,a1,b1,diraz,dirm,dp,fp,tp,hm0]=ondaf(vz(:,i),vx(:,i),vy(:,i),nfft,fs,h);

    %salva os parametros de onda em uma matriz
    %      linha = 1   2   3     4    5    6   7 8
    matonda(i,:)=[hs,h10,hmax,thmax,tmed,hm0,tp,dp];
end




        
        