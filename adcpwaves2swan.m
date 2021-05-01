%% CONVERTENDO LISTA DE ESPECTROS DO ADCP DA RDI PARA INPUT DO SWAN (.BND, Spec2D):
%- Guilherme Colaco Melo dos Passos-%
clear all,clc,close all,beep off

%% CARREGANDO INFORMACOES DO PROMPT DE COMANDO::
prompt={'Diretorio contendo os outputs do ADCP (DSpec....txt):',...
        'Diretorio de destino para dados processados:',...
        'Formato de Input desejado (SWAN ou Xbeach):',...
        'Formato para interpolacao dos Espectros (WW3, WAM, ou N/A):'};
       
name='Conversao: Espectros-2D ADCP RDI para input do SWAN';
numlines=1;
defaultanswer={'/home/izabel/Dropbox/lioc/dados/ww3es/CACIMBAS/ADCP/series_brutas/200501/WAVES/',...
               '/home/izabel/Dropbox/ww3es/Geral/modelagem/aguas_rasas/',...
               'SWAN',...
               'N/A'};
     
options.Resize='on';
options.WindowStyle='modal';
options.Interpreter='tex';
 
answer=inputdlg(prompt,name,numlines,defaultanswer,options);
% -------------------------------------------------------------------------

dados_adcp = (answer{1});
dados_xb = (answer{2});

lista = dir([dados_adcp 'DS*.txt']); % lista todos os arquivos texto (espectros) dentro da pasta

cd(answer{2})

interpolacao = answer{4};
% -------------------------------------------------------------------------


%% Carregando espectro direcional:
for k=1:length(lista);
sp2=load([dados_adcp lista(k).name]); sp2=(sp2*(10^-6))/360; % correcao de mm^2/Hz/Cycle para m^2/Hz/Degree
nome_arquivo{k,1} = lista(k).name;

%% INFORMACOES GERAIS DOS ESPECTROS - CONFIGURACOES DO ADCP:

%--Metodo usado: textread. Leio o arquivo e separo o conteudo em colunas.
%--Assim pode-se extrair a informacao do cabecalho apenas sabendo sua linha
%--e coluna:

[col1 col2 col3 col4 col5 col6 col7 col8 col9 col10 col11 col12 col13] =...
textread([dados_adcp lista(k).name],'%s%s%s%s%s%s%s%s%s%s%s%s%10s','delimiter',' ');
f1 = str2num(col13{4}); % primeira banda de frequencia
delta_f = str2num(col5{4}); % largura de banda de frequencia
n_f = str2num(col5{2}); % numero de frequencias
dir1 = str2num(col8{6}); % primeiro slice de direcao
delta_dir = 360/str2num(col2{2}); % resolucao de direcao
n_d = str2num(col2{2}); % numero de direcoes

%---------------------------------------
% Metodo alternativo (menos robusto):
% fid = fopen([dados_adcp lista(k).name],'r');
% [A,count] = fscanf(fid,'%c');
% delta_f = str2num(A(1,120:130));
% delta_dir = 360./str2num(A(1,30:32));
% f1 = str2num(A(1,175:184));
% dir1 = str2num(A(1,226:228));
% fclose(fid);
%----------------------------------------
% Metodo de input direto: Entrar com as config do ADCP manualmente:
% f1 = 0.01611328;
% delta_f = 0.03125000;
% dir1 = 77;
% delta_dir = 10;
%----------------------------------------
direcoes(:,1) = dir1:delta_dir:dir1+360-delta_dir;
ind=find(direcoes>360);
direcoes(ind)=direcoes(ind)-360; direcoes=sortrows(direcoes);
direcoes(1:n_d,2:n_d) = NaN;

%colocanco o espectro na ordem crescente:
g=length(find(direcoes<dir1));
sp2 = [sp2(:,(n_d -g+1):n_d) sp2(:,(1:(n_d - g)))];

frequencias = f1:delta_f:1; frequencias=frequencias';
frequencias(1:n_f,2:n_d) = NaN;

nfreq(1,1) = length(frequencias(:,1));
nfreq(1,2:n_d) = NaN;

ndir(1,1) = length(direcoes);
ndir(1,2:n_d) = NaN;


spec2d = [nfreq;frequencias;ndir;direcoes;sp2];

cabecalho_swan{1,1} = 'SWAN    1';      
cabecalho_swan{2,1} = 'TIME';      
cabecalho_swan{3,1} = '     1';         
cabecalho_swan{4,1} = 'LOCATIONS'; 
cabecalho_swan{5,1} = '1';
cabecalho_swan{6,1} = '233616.21     163369.50';
  
spec_swan = [cabecalho_swan;...
             'RFREQ';...
             num2str(nfreq(:,1));...
             cellstr(num2str(frequencias(:,1)));...
             'NDIR';...
             num2str(ndir(:,1));...
             cellstr(num2str(direcoes(:,1)));...
             'QUANT';...
             'VaDens';...
             'm2/Hz/degr';...
             '-9.9000e+01'];

spec_swan{end+1,1} = datestr([lista(k).date],'yyyymmdd.HHMMSS');
spec_swan{end+1,1} = 'FACTOR';
spec_swan{end+1,1} = '1e+00';

spec_swan = [spec_swan;cellstr(num2str(sp2))];


spec_adcp = strrep(cellstr(num2str(spec2d)),'NaN','');


% Interpolar para as frequencias e direcoes que desejo utilizar:
if strcmp(interpolacao,'WAM') == 1;
        f_xb = [0.04177 0.0459 0.0505 0.0556 0.0612 0.0673 0.0740...
        0.0814 0.0895 0.0985 0.1083 0.1192 0.1311 0.1442...
        0.1586 0.1745 0.1919 0.2111 0.2323 0.2555 0.2810...
        0.3091  0.3400 0.3740 0.4114];
        % f_xb = linspace(0.01611328,frequencias(end,1),n); f_xb =f_xb';
        % dir_xb = (dir1:15:(dir1+360-10)); dir_xb = dir_xb';
        dir_xb = 10:15:360;
        % direcoes(1,1):15:direcoes(end,1)
        [DIR,F]=meshgrid(direcoes(:,1),frequencias(:,1));
        [DIR_xb,F_xb]=meshgrid(dir_xb,f_xb);

        sp2_xb = interp2(DIR,F,sp2,DIR_xb,F_xb);
        
            %% MONTANDO A LISTA DE ESPECTROS INTERPOLADOS PARA LEITURA NO XBEACH
            direcoes_xb(:,1) = dir_xb;
            direcoes_xb(1:24,2:24) = NaN;
            frequencias_xb(:,1) = f_xb';
            frequencias_xb(1:25,2:24) = NaN;

            nfreq_xb(1,1) = length(frequencias_xb(:,1));
            nfreq_xb(1,2:24) = NaN;

            ndir_xb(1,1) = length(direcoes_xb(1,:));
            ndir_xb(1,2:24) = NaN;

            spec2d_xb = [nfreq_xb;frequencias_xb;ndir_xb;direcoes_xb;sp2_xb];
            spec_adcp_xb = strrep(cellstr(num2str(spec2d_xb)),'NaN','');

            fmane = lista(k,1).name;
            fid = fopen(lista(k,1).name,'w');

            [nrows,ncols]=size(spec_adcp_xb);


            for row = 1:nrows;
                fprintf([fid],'%s\r\n',spec_adcp_xb{row,:});
            end
            fclose(fid);
        
else
    
    spec_adcp_xb = strrep(cellstr(num2str(spec2d)),'NaN','');

fmane = lista(k,1).name;
fid2 = fopen(lista(k,1).name,'w');

[nrows,ncols]=size(spec_swan);


for row = 1:nrows;
    fprintf([fid2],'%s\r\n',spec_swan{row,:});
end
fclose(fid2);
end

%convert domain to meshgrid format
% [d f]=meshgrid(direcoes(:,1),frequencias(:,1));
%nail it on an equally spaced grid
% [di fi]=meshgrid(linspace(min(D),max(D),72),linspace(min(F),max(F),30));
%use that grid to interpolate
% Si=interp2(d,f,S,di,fi);

%some plots
% figure()
% subplot(4,1,1:2)
%     mesh(d,f,sp2); shading interp
%     xlabel('dir (deg)'); ylabel('freq (Hz)')
% subplot(4,1,3:4)
%     contour(d,f,sp2); 
%     grid on
%        xlabel('dir (deg)'); ylabel('freq (Hz)')
%           
% Get direction and frequency differential        
% d_teta=mean(unique(diff(d(1,:)))); %mean is for wipe away machine precision
% d_f=mean(unique(diff(f(:,1))));       
% 
% 
% Use them to integrate numerically and get zero order momentum
% Armed with that information, calculate spectral wave height, 
% a.k.a. Hm0:       
% format long
% disp('Spectral wave height (Hm0) extracted from 2D spectrum. [In meters?] ')
% Hm0(k)=4*sqrt(sum(sum(sp2)).*d_f.*d_teta);
% 
% Sd=sum(sp2); w= find(Sd==max(Sd));
% 
% Tp(k)=1/f(w);
% 
% Dp(k) = direcoes(w);
% close all
end

break
%% CRIANDO A FILELIST COM O NOME E DURACAO DE ATUACAO DOS ESPECTROS:

cabecalho = 'FILELIST';
duracao = 1800;
nvezes = 1';

for i = 1:length(lista)
 filelist(1,1:8)=cabecalho;
 filelist(i+1,1:26) =([num2str(duracao) ' ' num2str(nvezes) ' ' nome_arquivo{i}]);
end

dlmwrite('filelist.txt',filelist,'delimiter','','newline','pc');

break
%% CONFERINDO SE OS ESPECTROS FOI CONFERINDO DE MANEIRA CORRETA::
spec = (sp2_xb'); % corrigindo a orientacao da matriz e a unidade (de mm2 para m2)
fretab = f_xb;
nfre = length(fretab);
dfim(1:25) = (fretab(2)-fretab(1));
nang = length(dir_xb);

spec = rot90(sp2*(10^-06)); % corrigindo a orientacao da matriz e a unidade (de mm2 para m2)
fretab = frequencias(:,1);
nfre = length(fretab);
dfim(1:32) = delta_f;
nang = length(direcoes(:,1));


S=zeros(1,25);

% 2d to 1d spec
for ifre=1:nfre

S(ifre)=sum(spec(:,ifre));

end
figure, plot(fretab,S)


% SWH of 1d and 2d spec

% SWH of the 2d spec

meante=0;

     for ifre=1:nfre
     
sum0=0;

       for iang=1:nang
       sum0 = sum0 + spec(iang,ifre);
       end 

    meante = meante + dfim(ifre) * sum0;
     end 
    
swh_2d=4.01*sqrt(meante);

% SWH of the 1d spec

swh_1d=4.01*sqrt(sum(S.*dfim));




