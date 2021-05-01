% =============================================================
%              PROJETO BACIA ES
% =============================================================
% ler os arquivos da boia do ES
% coordenadas: lat 19.57'
%              lon 39°32'
% intervalo de dados: 1 hora
% inicio:2006-10-12 00h
% final: 2007-01-15 23h
% =============================================================
close all
clc
clear all

work='/home/izabel/Espirito_Santo/Dados';
% --
saida=load('saida.out');
% --
dia=saida(:,1);mes=saida(:,2);ano=saida(:,3);hora=saida(:,4);min=saida(:,5);
% --
% altura significativa
hs=4.*sqrt(saida(:,17));
%%%%%%
saida=load('saida.out');
% periodo de pico
tp=decimate(saida(457:1176,22),3);
%direcao de pico
dp=decimate(saida(457:1176,26),3);
%tp
plot(tp(9:end,1),'r')
hold on;plot(tp_daat(1:end-9)./0.78125,'k')
%dp 
plot(dp(9:end,1),'r');hold on
plot(dp_daat(1:end-9),'k')
% ===========================================================
%                 PLOTAR RESULTADOS
% ===========================================================

% Altura Significativa 
figure1=figure(1);
subplot1 = subplot(3,1,1,'Parent',figure1,...
    'YTickLabel',{'0','2','4','5','1','3'},...
    'YTick',[0 2 4 5 1 3],...
    'XTickLabel',{'12/10/2006','01/11/2006','15/11/2006','01/12/2006','15/12/2006','25/12/2006'},...
    'XTick',[1 457 817 1201 1537 1777],...
    'FontWeight','bold',...
    'FontSize',14,'LineWidth',2,'GridLineStyle','--');
box(subplot1,'on');
grid(subplot1,'on');
hold(subplot1,'all');
plot(hs,'--bx','LineWidth',2)
%title('Altura Significativa','FontWeight','Bold','fontsize', 16)
ylim ([0 5])
%xlabel('data','fontsize',12,'fontweight','b')
ylabel('HS (m)','fontsize',14,'fontweight','b')
grid on


% Periodo de pico

subplot1 = subplot(3,1,2,'Parent',figure1,'YTick',[0 4 8 12 16],...
    'XTickLabel',{'12/10/2006','01/11/2006','15/11/2006','01/12/2006','15/12/2006','25/12/2006'},...
    'XTick',[1 457 817 1201 1537 1777],...
    'FontWeight','bold',...
    'FontSize',14,'LineWidth',2,'GridLineStyle','--');
box(subplot1,'on');
grid(subplot1,'on');
hold(subplot1,'all');
plot(tp,'--bx','LineWidth',2)
%title('Período Médio','FontWeight','Bold','fontsize', 16)
ylim ([0 20])
%xlabel('Registro','fontsize',12,'fontweight','b')
ylabel('TP (s)','fontsize',14,'fontweight','b')
grid on

% Direcao de pico

subplot1 = subplot(3,1,3,'Parent',figure1,'YTick',[0 45 90 135 180],...
    'XTickLabel',{'12/10/2006','01/11/2006','15/11/2006','01/12/2006','15/12/2006','25/12/2006'},...
    'XTick',[1 457 817 1201 1537 1777],...
    'FontWeight','bold',...
    'FontSize',14,'LineWidth',2,'GridLineStyle','--');
box(subplot1,'on');
grid(subplot1,'on');
hold(subplot1,'all');
plot(dp,'--bx','LineWidth',2)
%title('Direção Média','FontWeight','Bold','fontsize', 16)
%xlabel('Data','fontsize',12,'fontweight','b')
ylabel('DP(°)','fontsize',14,'fontweight','b')
ylim([0 210])
grid on