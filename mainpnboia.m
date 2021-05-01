% Processamento de dados de ondas do PNBOIA
% Henrique Pereira

%Tratamento de dados de onda
%onda_freq / onda_tempo / daat

clear, clc, close all

%dados = heave(m) / dsp.north(m) / dsp.east(m)


%pathname de onde estao os dados
% pathname = '/home/lioc/Documents/pnboia/dados/axys/rio_grande/hne/'; %lnx
pathname = '/home/hp/Dropbox/pnboia/data/rio_grande/HNE/';

dmag = -23;

%listhne index to process
zz1 = 500;
zz2 = 600;
        
%profundidade
h=200;
        
%cria lista HNE
listhne1 = dir(pathname);
listhne2 = {listhne1.name};
listhne = listhne2(3:end);

%create datetime vector
for i = 1:length(listhne)
    
    date1 = char(listhne(i));
    date2(i,1) = eval(date1(1:4));
    date2(i,2) = eval(date1(5:6));
    date2(i,3) = eval(date1(7:8));
    date2(i,4) = eval(date1(9:10));

    %t(i,:) = datetime(date1(i,:),'InputFormat','yyyyMMdd.HNE')
    
end

%dia juliano
datej = datenum(date2(:,1), date2(:,2), date2(:,3), date2(:,4), 00, 00);

%date string
datet = datestr(datej, 'yyyy/mm/dd');

%parametros para o calculo do espectro
nfft = 82; %tamanho do segmento para a fft
fs = 1.28; %frequencia de amostragem
dt = 1/fs; %intervalo de amostragem

%acha os indices do primeiro e ultimo arquivo que deseja ser processado

%nome
% bp1=find(ap==200905010000);
% bp2=find(ap==200905312300); %final de maio: 200905312300

%posicao
% bp1 = find(listhne == listhne(1,:));
% bp2 = find(listhne == listhne(end,:));

%Matriz com arquivos a serem processados
% arqp=arqp(bp1:bp2,:);

%% DAAT

%processamento pela DAAT
% pp_daat_ambid

n = 0; %contador
nn = 0;

for zz = zz1:zz2
    
    %cria variavel com nome do arquivo a ser processado    
    pathfile = ([pathname, char(listhne(zz))]);
    
    dados = importdata(pathfile,' ', 11);
    ta = dados.data(:,1);
    n1 = dados.data(:,2);
    n3 = dados.data(:,3);
    n2 = dados.data(:,4);
    
    if length(find(abs(n1)>0.3)) < 100
        
        disp([pathfile, ' Arquivo com erro'])
        
    else
        
        disp([pathfile, ' Arquivo processado'])
        
        %contador
        n=n+1;
        
%         datet(n,:) = datet1(n,:);
    
        %lista string de datas
        dates(n,:) = listhne(zz);
        
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
end

t = 1:length(matonda);
tt = 1:round(length(t)/7):length(t);
datett = datet(tt,:);

subplot(3,1,1)
plot(t,matonda(6,:))
axis tight
ylim([0 5])
grid on
title('Altura Significativa')
xlabel('Dias')
ylabel('metros')
set(gca,'Xtick',tt,'XTickLabel',datett)

subplot(3,1,2)
plot(t,matonda(7,:))
axis tight
ylim([0 20])
grid on
title('Perdiodo de pico')
xlabel('Dias')
ylabel('segundos')
set(gca,'Xtick',tt,'XTickLabel',datett)

subplot(3,1,3)
plot(t,matonda(8,:))
axis tight
ylim([0 360])
grid on
title('Direção do periodo de pico')
xlabel('Dias')
ylabel('graus')
set(gca,'Xtick',tt,'XTickLabel',datett)

figure
mesh(t, f, bb), view(220 ,45)
title('Evolucao Espectral')
ylabel('Frequencia (Hz)')
zlabel('Energia (m2/Hz)')
colorbar
axis tight
% ylim([0 0.2])
set(gca,'Xtick',tt,'XTickLabel',datett)

figure
contour(t ,f, bb)
title('Evolucao Espectral')
ylabel('Frequencia (Hz)')
colorbar
axis tight
% ylim([0 0.3])
set(gca,'Xtick',tt,'XTickLabel',datett)

%salva figuras

% nome=(['evspmesh_' ad(5,:),'.jpg']);
% saveas(fig_mesh,nome)
% nome=(['evspcont_' ad(5,:),'.jpg']);
% saveas(fig_cont,nome)








