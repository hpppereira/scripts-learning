%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%              geraspecdirboia.m                %%%%%%%%%%%%%%
%%%%%%%%%%%%%% Dissertação de Mestrado                       %%%%%%%%%%%%%%
%%%%%%%%%%%%%% LIOc - PEnO/COPPE/UFRJ                        %%%%%%%%%%%%%%
%%%%%%%%%%%%%%                                    24/10/2012 %%%%%%%%%%%%%%
%%%%%%%%%%%%%%                            Adrieni de Andrade %%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%-------------------------------------------------------------------------%
% Gera espectro direcional a partir de dados brutos de boias              %
% --> Entradas:                                                           %
% --> Saídas:                                                             %
% - Matriz com espectro direcional;                                       %
% - Figuras com espectro direcional.                                      %
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
% OBS: Para Marlin - 91/92/93           Para Barracuda - 94/95            %
%      elevação --> arq(:,2)             elevação --> arq(:,1)            %
%      roll     --> arq(:,4)             roll     --> arq(:,2)            %
%      pitch    --> arq(:,3)             pitch    --> arq(:,3)            %
%-------------------------------------------------------------------------%
clear all; close all; clc;

%% Configurando dados de entrada
% cd('/home/adrieni/Documentos/anl_dados_boia/dados_felipe2008/92_marco_mar/com_wafo');

% for j = 24:26;
%     for ii = 10:3:22;
% eval(['load 9203',num2str(j),num2str(ii,'%2.0i'),'.DAT;']);
% eval(['arq = X9203',num2str(j),num2str(ii,'%2.0i'),';']); 
% eval(['clear X9203',num2str(j),num2str(ii,'%2.0i'),';']);
Hm0_wafo = [];
Hm0_2 = [];
Tp_wafo = [];
Tp_2 = [];
for j = 24:26;
    for ii = 1:3:22;
        if j<10 & ii<10
            eval(['load 92030',num2str(j),'0',num2str(ii,'%2.0i'),'.DAT;']);
            eval(['arq = X92030',num2str(j),'0',num2str(ii,'%2.0i'),';']);
            eval(['clear X92030',num2str(j),'0',num2str(ii,'%2.0i'),';']);
        else if j<10 & ii>=10
                eval(['load 92030',num2str(j),num2str(ii,'%2.0i'),'.DAT;']);
                eval(['arq = X92030',num2str(j),num2str(ii,'%2.0i'),';']);
                eval(['clear X92030',num2str(j),num2str(ii,'%2.0i'),';'])
            else if j>=10 & ii<10
                    eval(['load 9203',num2str(j),'0',num2str(ii,'%2.0i'),'.DAT;']);
                    eval(['arq = X9203',num2str(j),'0',num2str(ii,'%2.0i'),';']);
                    eval(['clear X9203',num2str(j),'0',num2str(ii,'%2.0i'),';']);
                 else if j>=10 & ii>=10
                    eval(['load 9203',num2str(j),num2str(ii,'%2.0i'),'.DAT;']);
                    eval(['arq = X9203',num2str(j),num2str(ii,'%2.0i'),';']);
                    eval(['clear X9203',num2str(j),num2str(ii,'%2.0i'),';'])
                    end
                end
            end
        end
% entrada da função dat2dspec.m
t = arq(:,1); % Número de amostras, tempo = 1s --> taxa de amostragem 1Hz
z = arq(:,2); % elevação
x = arq(:,4); % pitch
y = arq(:,3); % roll

W = [t z x y];
% W = arq; %teste

% posicionamento do sensor (boia)
lon = ones(3,1).*39.97; % em graus
lat = ones(3,1).*22.52;
z = zeros(3,1);
sensorpos = [lon lat z];
type = [1 4 5];%type = [1 4 5]; % comando para sensor de superfície
bfs = [1 0 0];
pos = [sensorpos type' bfs'];


% profundidade local
h = inf; % ou 1250 m

% nº da fft a ser utilizado
amost = 1024; % nº de amostras
partes = 16; % nº de subdivisões
gl = partes*2;
nfft = amost./partes; % 1024/4 = 256; default

% nº de ângulos -- default = 101;
nt = 101; % 24 ângulos de direção;

% Método da função de distribuição
% method = 'MEM';

% Mudanças das opções do espectro
options =  specoptset('dat2dspec','ftype','f');

%% Gerando matriz com os espectros direcionais

%  [S,D,Sw,Fcof] = dat2dspec(W, pos, h, nfft, nt, method, options);
[S,D,Sw,Fcof] = dat2dspec(W, pos, h, nfft, nt,'MLM',options);
%  wspecplot(S)

%% Plotando os espectros direcionais e não direcionais
frequencia = S.f;
direcao = S.theta;
[df,ddir] = meshgrid(frequencia,direcao);
espec_2D= S.S;
espec_1D = Sw.S;

% calculando Hm0 e Tp

m0_1 = trapz(espec_1D).*mean(diff(frequencia));
hm0_1 = 4.*sqrt(m0_1);
Hm0_wafo = [Hm0_wafo;hm0_1];

maxE1D_1 = find(espec_1D == max(espec_1D));
tp_1 = 1./frequencia(maxE1D_1);
Tp_wafo = [Tp_wafo;tp_1];

% direção de destino (para onde vai) e ângulo trigonométrico
figure(1)
h = polar([0 2*pi], [0 max(frequencia)]);hold on;
delete(h);
%  set(gca,'View',[-90 90],'YDir','reverse');
% set(gca,'View',[90 -90]);
[px,py]=pol2cart(ddir,df);
m=max(max(espec_2D));
v=logspace(log10(m/10), log10(m), 150);
contourf(px,py,real(espec_2D),v,'linestyle','none');
title('Destino | Trigonométrico')

figure(2)
plot(frequencia,espec_1D); grid on;
title('Espectro 1D | Não Interpolado')
if j<10 & ii<10
            filename = ['espectro_92030',num2str(j),'0',num2str(ii),'_1Dwafomlm']
        else if j<10 & ii>=10
                filename = ['espectro_92030',num2str(j),num2str(ii),'_1Dwafomlm']
            else if j>=10 & ii<10
                    filename = ['espectro_9203',num2str(j),'0',num2str(ii),'_1Dwafomlm']
                 else if j>=10 & ii>=10
                    filename = ['espectro_9203',num2str(j),num2str(ii),'_1Dwafomlm']
                    end
                        end
            end
end
print ('-dpng','-r300',filename)


%% Interpolando o espectro 2D para 24x25
[X,Y] = meshgrid(frequencia,direcao); % espectros originais
frequencia_25=[0:0.0208:0.5]'; 
% frequencia_25 = [0.0412,0.0453,0.0498,0.0548,0.0603,0.0663,0.0730,0.0802,0.0883,0.0971,0.1070,0.1170,0.1290,...
% 0.1420,0.1560,0.1720,0.1890,0.2080,0.2290,0.2520,0.2770,0.3050,0.3350,0.3690,0.4060]';
theta_24=[-pi:0.2618:pi]';
theta_plot = [theta_24; pi];
[Xi,Yi] = meshgrid(frequencia_25,theta_plot);% espectros interpolados
espec_2D_2425 = interp2(X,Y,espec_2D,Xi,Yi);

% calculando Hm0 e Tp
espec_1D_25 = trapz(espec_2D_2425);
frequencia_2=frequencia_25/(2*pi);

m0_2 = trapz(espec_1D_25).*mean(diff(frequencia_2));
hm0_2 = 4.*sqrt(m0_2);
Hm0_2 = [Hm0_2;hm0_2];

maxE1D_2 = find(espec_1D_25 == max(espec_1D_25));
tp_2 = 1./frequencia_25(maxE1D_2);
Tp_2 = [Tp_2;tp_2];

figure(3)
h = polar([0 2*pi], [0 0.8*max(frequencia_25)]);hold on;
delete(h);
%  set(gca,'View',[-90 90],'YDir','reverse');
% set(gca,'View',[90 -90]);
[px,py]=pol2cart(Yi,Xi);
m=max(max(espec_2D_2425));
v=logspace(log10(m/10), log10(m), 150);
contourf(px,py,real(espec_2D_2425),v,'linestyle','none');
title('Destino | Trigonometrico | Interpolado 24x25')

figure(4)
plot(frequencia_25,espec_1D_25);grid on;
title('Espectro 1D | Interpolado')

if j<10 & ii<10
            filename = ['espectro_92030',num2str(j),'0',num2str(ii),'_1Dintepmlm']
        else if j<10 & ii>=10
                filename = ['espectro_92030',num2str(j),num2str(ii),'_1Dwafointepmlm']
            else if j>=10 & ii<10
                    filename = ['espectro_9203',num2str(j),'0',num2str(ii),'_1Dwafointepmlm']
                 else if j>=10 & ii>=10
                    filename = ['espectro_9203',num2str(j),num2str(ii),'_1Dwafointepmlm']
                    end
                        end
            end
end
print ('-dpng','-r300',filename)

%% Transformando de trigonométrico para azimutal

%theta em graus 
theta_deg= (theta_plot.*180)./pi;
% theta Azimutal direção de destino
theta_Az = 450-theta_deg; % 270:-90% trigonométrico para azimute
theta_Az_rad = (theta_Az.*pi)./180;
%theta Azimutal direção de origem
 theta_origem = (theta_Az).*(-1); %-270:90
 theta_origem_rad = (theta_origem.*pi)./180;
 
[df3,ddir3] = meshgrid(frequencia_25,theta_Az_rad);
figure(5)
h = polar([0 2*pi], [0 0.8*max(frequencia_25)]);hold on;
delete(h);
[px3,py3]=pol2cart(ddir3,df3);
m=max(max(espec_2D_2425));
v=logspace(log10(m/10), log10(m), 150);
contourf(px3,py3,real(espec_2D_2425),v,'linestyle','none');
% get(findall(gcf, 'type', 'text'), 'string');
% thext = {'0' '1' '2' '3' '4' '30' '60' '90' '120' '150' '180' '210' '240' '270' '300' '330' '360'};
% for r=1:length(thext)
%     delete(findall(gcf, 'string', thext{r}))
% end
title('Destino| Interpolado | AZIMUTAL')
% pause
if j<10 & ii<10
            filename = ['espectro_92030',num2str(j),'0',num2str(ii),'_2Dmlm']
        else if j<10 & ii>=10
                filename = ['espectro_92030',num2str(j),num2str(ii),'_2Dmlm']
            else if j>=10 & ii<10
                    filename = ['espectro_9203',num2str(j),'0',num2str(ii),'_2Dmlm']
                 else if j>=10 & ii>=10
                    filename = ['espectro_9203',num2str(j),num2str(ii),'_2Dmlm']
                    end
                        end
            end
end
print ('-depsc','-r300',filename)

[df4,ddir4] = meshgrid(frequencia_25,theta_origem_rad);
figure(6)
h = polar([0 2*pi], [0 0.8*max(frequencia_25)]);hold on;
delete(h);
[px4,py4]=pol2cart(ddir4,df4);
m=max(max(espec_2D_2425));
v=logspace(log10(m/10), log10(m), 150);
contourf(px4,py4,real(espec_2D_2425),v,'linestyle','none');
% get(findall(gcf, 'type', 'text'), 'string');
% thext = {'0' '1' '2' '3' '4' '30' '60' '90' '120' '150' '180' '210' '240' '270' '300' '330' '360'};
% for r=1:length(thext)
%     delete(findall(gcf, 'string', thext{r}))
% end
title('Origem | Interpolado | AZIMUTAL')


if j<10 & ii<10
            eval(['save -ascii mlmspec2425_92030',num2str(j),'0',num2str(ii,'%2.0i'),' espec_2D_2425'])
        else if j<10 & ii>=10
                eval(['save -ascii mlmspec2425_92030',num2str(j),num2str(ii,'%2.0i'),' espec_2D_2425'])
            else if j>=10 & ii<10
                    eval(['save -ascii mlmspec2425_9203',num2str(j),'0',num2str(ii,'%2.0i'),' espec_2D_2425'])
                 else if j>=10 & ii>=10
                    eval(['save -ascii mlmspec2425_9203',num2str(j),num2str(ii,'%2.0i'),' espec_2D_2425'])
                     end
                end
            end
end
stop
clearvars -except ii j Hm0_wafo Hm0_2 Tp_wafo Tp_2
close all;
    end
end
save Hm0_wafomlm.mat Hm0_wafo -mat
save Hm0_interpmlm.mat Hm0_2 -mat
save Tp_wafomlm.mat Tp_wafo -mat
save Tp_interpmlm.mat Tp_2 -mat