%Tratamento de dados de onda
%onda_freq / onda_tempo / daat

clear, clc, close all

%dados = heave(m) / dsp.north(m) / dsp.east(m)


%pathname de onde estao os dados
% pathname = '/home/lioc/Documents/pnboia/dados/axys/rio_grande/hne/'; %lnx
pathname = 'C:\Users\lioc\Documents\pnboia\dados\axys\rio_grande\hne\'; %win

%carrega lista com nome dos arquivos .HNE e passa para string
arq=load('list_RSmay09.txt'); arqp=num2str(arq); 

%parametros para o calculo do espectro
nfft = 82; %tamanho do segmento para a fft
fs = 1.28; %frequencia de amostragem

%acha os indices do primeiro e ultimo arquivo que deseja ser processado

%nome
% bp1=find(ap==200905010000);
% bp2=find(ap==200905312300); %final de maio: 200905312300

%posicao
bp1=find(arq==arq(1,:));
bp2=find(arq==arq(end,:));

%Matriz com arquivos a serem processados
arqp=arqp(bp1:bp2,:);

%% DAAT

%processamento pela DAAT
% pp_daat_ambid

dt = 1/fs; %intervalo de amostragem
n=0; %contador
for zz=bp1:bp2
    
    %contador
    n=n+1;
    
    %cria variavel com nome do arquivo a ser processado    
    arq1=[pathname,arqp(zz,1:end),'.HNE'];
   
    %chama subrotina para leitura do arquivo 'arq1'
    %[eta etaNS etaEW]
    [n1, n2, n3]=carregaaxys_hne(arq1);

    %profundidade
    h=200;

    %chama subrotina de processamento de onda no dominio da frequencia (dir,hm0..)
    [f,an,anx,any,a1,b1,diraz,dirm,dp,fp,tp,hm0]=ondaf(n1,n2,n3,nfft,fs,h);

    %chama subrotina de processamento de onda no dominio do tempo (Tza, Hs..)
    [hs,h10,hmax,thmax,tmed]=ondat(n1,fs,h);

    %salva os parametros de onda em uma matriz
    %      linha = 1   2   3     4    5    6   7 8
    matonda(:,n)=[hs,h10,hmax,thmax,tmed,hm0,tp,dp]';

    % Salva os autoespectro (cada coluna representa 1 hora) - utilizado na
    % rotina de evolucao espectral (evol_espec)
    bb(:,n)=an;

end

%cria vetor de tempo horario
tt=[1:length(sai_onda)]./24;
    
%grafics onda tempo e frequencia
grafonda(tt,matonda);

%Grafico da evolucao espectral
% evol_espec(f,bb);

