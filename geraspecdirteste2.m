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
for j = 26;
    for ii = 1;
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
x = arq(:,3); % pitch
y = arq(:,4); % roll

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
[S,D,Sw,Fcof] = dat2dspec(W, pos, h, nfft, nt,'MEM',options);
%  wspecplot(S)

%% Plotando os espectros direcionais
frequencia = S.f;
direcao = S.theta;
[df,ddir] = meshgrid(frequencia,direcao);
espec_2D= S.S;

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

%% Interpolando o espectro 2D para 24x25
[X,Y] = meshgrid(frequencia,direcao); % espectros originais
frequencia_25=[0.02:0.02:0.5]'; 
theta_24=[-pi:0.2618:pi]';
theta_plot = [theta_24; pi];
[Xi,Yi] = meshgrid(frequencia_25,theta_plot);% espectros interpolados
espec_2D_2425 = interp2(X,Y,espec_2D,Xi,Yi);

figure(2)
h = polar([0 2*pi], [0 0.8*max(frequencia_25)]);hold on;
delete(h);
%  set(gca,'View',[-90 90],'YDir','reverse');
% set(gca,'View',[90 -90]);
[px,py]=pol2cart(Yi,Xi);
m=max(max(espec_2D_2425));
v=logspace(log10(m/10), log10(m), 150);
contourf(px,py,real(espec_2D_2425),v,'linestyle','none');
title('Destino | Trigonometrico | Interpolado 24x25')

%% Transformando de trigonométrico para azimutal
theta_Az = ((5*pi)/2)-theta_plot; % trigonométrico para azimute

theta_deg = (theta_Az.*180)./pi; theta_deg = theta_deg-270; theta_deg = ceil(theta_deg);% radianos para graus

cont=0; % de 0->360
        for nn=1:25;
            theta_part(nn)=theta_deg(25-cont);
            cont = cont+1;
        end
theta_part=theta_part';
theta_plot2 = (theta_part.*pi)./180;
cont=0;
        for mm=1:25;
            S_2d_part(mm,:)=espec_2D_2425(25-cont,:);
            cont = cont+1;
        end
        
        [Xi,Yi] = meshgrid(frequencia_25,theta_plot2);
figure(3)
h = polar([0 2*pi], [0 0.8*max(frequencia_25)]);hold on;
delete(h);
%  set(gca,'View',[-90 90],'YDir','reverse');
% set(gca,'View',[90 -90]);
[px,py]=pol2cart(Yi,Xi);
m=max(max(S_2d_part));
v=logspace(log10(m/10), log10(m), 150);
contourf(px,py,real(S_2d_part),v,'linestyle','none'); 
title('Destino | Azimutal | Interpolado 24x25')

%% Transformando da direção de destino para direção de origem

aa = find(theta_part<180); % passa de direção de propagação da onda para direção de origem
bb = find(theta_part>=180);

theta_deg_origem = [theta_part(aa)+180;theta_part(bb)-180];
theta_origem = (theta_deg_origem.*pi)./180;

S_2d_origem = [S_2d_part(bb,:);S_2d_part(aa,:)];

[Xi,Yi] = meshgrid(frequencia_25,theta_plot2);
figure(4)
h = polar([0 2*pi], [0 0.8*max(frequencia_25)]);hold on;
delete(h);
%   set(gca,'View',[-90 90],'YDir','reverse');
% set(gca,'View',[90 -90]);
[px,py]=pol2cart(Yi,Xi);
m=max(max(S_2d_origem));
v=logspace(log10(m/10), log10(m), 150);
contourf(px,py,real(S_2d_origem),v,'linestyle','none'); 
title('Origem | Azimutal | Interpolado 24x25')

% % if j<10 & ii<10
% %             filename = ['espectro_92030',num2str(j),'0',num2str(ii)]
% %         else if j<10 & ii>=10
% %                 filename = ['espectro_92030',num2str(j),num2str(ii)]
%             else if j>=10 & ii<10
%                     filename = ['espectro_9203',num2str(j),'0',num2str(ii)]
%                  else if j>=10 & ii>=10
%                     filename = ['espectro_9203',num2str(j),num2str(ii)]
%                     end
%                         end
%             end
% end
% % print ('-depsc','-r300',filename)

% if j<10 & ii<10
%             eval(['save -ascii spec2425_92030',num2str(j),'0',num2str(ii,'%2.0i'),' espec_2D_2425_a'])
%         else if j<10 & ii>=10
%                 eval(['save -ascii spec2425_92030',num2str(j),num2str(ii,'%2.0i'),' espec_2D_2425_a'])
%             else if j>=10 & ii<10
%                     eval(['save -ascii spec2425_9203',num2str(j),'0',num2str(ii,'%2.0i'),' espec_2D_2425_a'])
%                  else if j>=10 & ii>=10
%                     eval(['save -ascii spec2425_9203',num2str(j),num2str(ii,'%2.0i'),' espec_2D_2425_a'])
%                      end
%                 end
%             end
% end
stop

clearvars -except ii j
% close all;
    end
end
% save frequencia_25.mat frequencia_25 -mat