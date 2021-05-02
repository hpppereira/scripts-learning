%% Tatamento dos dados do derivador do bota fora 4 - dia 10/06/11
clear,clc,close all
%% Dados GPS
% bf4gps=load('bf4.txt');
% bf5gps=load('bf5.txt');
% % lat / long / mês	/ dia / ano	/ hora / min / seg

% figure
% plot(bf4gps(:,2),bf4gps(:,1),'.'), title('Bota fora 4 - Dados GPS')
% figure
% plot(bf5gps(:,2),bf5gps(:,1),'.'), title('Bota fora 5 - Dados GPS')
% 
% bf45gps=[bf4gps;bf5gps];
% 
% figure
% plot(bf45gps(:,2),bf45gps(:,1),'.'), title('Bota fora 4 e 5 - Dados GPS')

%% Dados do Caderno do Porto (Posições do derivador) separados por perfil

%Bota fora 4
bf4=load('derivador20110610.txt');
%bf5=load('bf5_decgrau.txt');
%Lat / Long
bf4=bf4*-1;
%Mapa Itajai-Açu
%mapa=load('mapa_itajaiacu_decgrau.txt');

%Peril 1
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 1'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(1:5,2),bf4(1:5,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 2
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 2'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(6:10,2),bf4(6:10,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 3
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 3'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 4
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 4'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 5
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 5'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 6
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 6'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 7
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 7'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 8
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 8'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 9
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 9'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 10
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 10'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 11
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 11'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 12
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 12'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 13
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 13'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

%Peril 14
figure
plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 14'),xlabel('Longitude'),ylabel('Latitude'), hold on
plot(bf4(6:10,2),bf4(6:10,1),'-*')
plot(bf4(11:15,2),bf4(11:15,1),'-*')
plot(bf4(16:20,2),bf4(16:20,1),'-*')
plot(bf4(21:25,2),bf4(21:25,1),'-*')
plot(bf4(26:30,2),bf4(26:30,1),'-*')
plot(bf4(31:35,2),bf4(31:35,1),'-*')
plot(bf4(36:40,2),bf4(36:40,1),'-*')
plot(bf4(41:45,2),bf4(41:45,1),'-*')
plot(bf4(46:50,2),bf4(46:50,1),'-*')
plot(bf4(51:55,2),bf4(51:55,1),'-*')
plot(bf4(56:60,2),bf4(56:60,1),'-*')
plot(bf4(61:65,2),bf4(61:65,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'-*')
plot(bf4(71:75,2),bf4(71:75,1),'-*')
plot(bf4(66:70,2),bf4(66:70,1),'r-*'), hold off
% Create textarrow
annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
    'TextEdgeColor','none',...
    'String',{'N'});
xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')

% %Peril 15
% figure
% plot(bf4(1:5,2),bf4(1:5,1),'-*'), title('Bota fora 4 / Perfil 15'),xlabel('Longitude'),ylabel('Latitude'), hold on
% plot(bf4(6:10,2),bf4(6:10,1),'-*')
% plot(bf4(11:15,2),bf4(11:15,1),'-*')
% plot(bf4(16:20,2),bf4(16:20,1),'-*')
% plot(bf4(21:25,2),bf4(21:25,1),'-*')
% plot(bf4(26:30,2),bf4(26:30,1),'-*')
% plot(bf4(31:35,2),bf4(31:35,1),'-*')
% plot(bf4(36:40,2),bf4(36:40,1),'-*')
% plot(bf4(41:45,2),bf4(41:45,1),'-*')
% plot(bf4(46:50,2),bf4(46:50,1),'-*')
% plot(bf4(51:55,2),bf4(51:55,1),'-*')
% plot(bf4(56:60,2),bf4(56:60,1),'-*')
% plot(bf4(61:65,2),bf4(61:65,1),'-*')
% plot(bf4(66:70,2),bf4(66:70,1),'-*')
% plot(bf4(71:75,2),bf4(71:75,1),'-*')
% plot(bf4(71:75,2),bf4(71:75,1),'r-*'), hold off
% % Create textarrow
% annotation('textarrow',[0.8813 0.8813],[0.8419 0.9129],...
%     'TextEdgeColor','none',...
%     'String',{'N'});
% xlabel('Longitude (Déc.grau)'),ylabel('Latitude (Déc.grau)')




