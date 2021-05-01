% ------------------------------------------------------------------
% -------------------  INTRA-ANUAL --------------------------------- 
%                       HS vs. TP

close all;clear all;clc


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%dados de entrada

pathname = '/home/hp/Dropbox/pnboia/rot/out/';

%hind1 = load([pathname,'hindcast.txt']);
%hind2 = load([pathname,'hindcast2.txt']); 

%hind = vertcat(hind1,hind2);

filename='FLN_Wave'; %para as figuras

%dd = load([pathname,filename,'.out']);

dd = csvread([pathname,filename,'.csv'],1,1);

%define variaveis
hs = dd(:,6); hs(hs==0) = NaN;
tp = dd(:,7); tp(tp==0) = NaN;
dp = dd(:,8); dp(dp==0) = NaN;

%eixos
axhstp = 15;
axtpdp = 15;
axhsdp = 15;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Defaults for this blog post
width = 10;     % Width in inches
height = 4;    % Height in inches
alw = 0.75;    % AxesLineWidth
fsz = 15;      % Fontsize
lw = 1.5;      % LineWidth
msz = 8;       % MarkerSize

class{1}=2:2:22;class{2}=0.25:0.5:6;
X = [tp,hs];n=hist3(X,class);n1 = ((n'.*100)/length(hs)); 
n1( size(n,2) + 1 ,size(n,1) + 1 ) = 0; 
xb = linspace(0,22,size(n,1)+1);  %correcao dos eixos
yb = linspace(0,6,size(n,2)+1);

figure
pos = get(gcf, 'Position');
set(gcf, 'Position', [pos(1) pos(2) width*100, height*100]); %<- Set size
set(gca, 'FontSize', fsz, 'LineWidth', alw,'FontName','Arial'); %<- Set properties
pcolor(xb,yb,n1);colormap(flipud(gray));
for a=1:length(n(:,1));
    for b=1:length(n(1,:));
        if (n(a,b)*100/length(hs)>0.00);
            label=num2str(n(a,b)*100/length(hs),'%.2f');
            text(xb(a)+0.5,yb(b)+0.22,label,'fontsize',fsz,'fontweight','n','color','r');
        end
    end
end
ylabel('Hm0 (m)','fontsize',fsz,'FontWeight','n','fontname','Arial')
xlabel('Tp (s)','fontsize',fsz,'FontWeight','n','fontname','Arial')
cm=colorbar('FontWeight','n','FontSize',10,'fontname','Arial');
set(get(cm,'ylabel'),'String', 'Occurrence (%)',...
    'fontsize',fsz,'fontname','Arial');
caxis([0, axhstp])
ylim([0 6]);xlim([2 20])

% Here we preserve the size of the image when we save it.
set(gcf,'InvertHardcopy','on');
set(gcf,'PaperUnits', 'inches');
papersize = get(gcf, 'PaperSize');
left = (papersize(1)- width)/2;
bottom = (papersize(2)- height)/2;
myfiguresize = [left, bottom, width, height];
set(gcf,'PaperPosition', myfiguresize);

% Save the file as PNG
print(['hstp_',filename],'-dpng','-r300');
print(['hstp_',filename],'-depsc2','-r1200');

% 
% 
% %                    HS vs, DP
% % Defaults for this blog post
% width = 6;     % Width in inches
% height = 4;    % Height in inches
% alw = 0.75;    % AxesLineWidth
% fsz = 10;      % Fontsize
% lw = 1.5;      % LineWidth
% msz = 8;       % MarkerSize
% 
% clear n n1 xb yb X class axes1
% class{1}=0:45:360;class{2}=0.25:0.5:5.75;
% X = [dp,hs];n = hist3(X,class); 
% n1 = ((n'.*100)/length(hs)); 
% n1( size(n,2) + 1 ,size(n,1) + 1 ) = 0; 
% xb = linspace(-22.5,382.5,size(n,1)+1);
% yb = linspace(0,6,size(n,2)+1);
% 
% figure
% pos = get(gcf, 'Position');
% set(gcf, 'Position', [pos(1) pos(2) width*100, height*100]); %<- Set size
% set(gca, 'FontSize', fsz, 'LineWidth', alw,'FontName','Arial');
% pcolor(xb,yb,n1);colormap(flipud(gray));
% for a=1:length(n(:,1));
%     for b=1:length(n(1,:));
%         if (n(a,b)*100/length(hs)>0.01);
%             label=num2str(n(a,b)*100/length(hs),'%.2f');
%             text(xb(a)+10,yb(b)+0.15,label,'fontsize',9,'fontweight','b','color','r','fontname','Arial');
%         end
%     end
% end
% ylabel('Altura Significativa (m)','fontsize',10,'FontWeight','n','fontname','Arial')
% xlabel('Direcao de Pico (graus)','fontsize',10,'FontWeight','n','fontname','Arial')
% set(gca,'XTick',[-5,45,90,135,180,225,270,315,360],'XTickLabel',{'N','NE','E','SE','S','SW','W','NW','N'})  
% cm=colorbar('FontWeight','n','FontSize',10,'fontname','Arial');
% set(get(cm,'ylabel'),'String', 'Porcentagem de Ocorrencia (%)',...
%     'fontsize',10,'fontname','Arial');
% ylim([0 5]);xlim([-5 270])
% caxis([0, axhsdp])
% 
% % Here we preserve the size of the image when we save it.
% set(gcf,'InvertHardcopy','on');
% set(gcf,'PaperUnits', 'inches');
% papersize = get(gcf, 'PaperSize');
% left = (papersize(1)- width)/2;
% bottom = (papersize(2)- height)/2;
% myfiguresize = [left, bottom, width, height];
% set(gcf,'PaperPosition', myfiguresize);
% 
% % Save the file as PNG
% print(['hsdp_',filename],'-dpng','-r300');
% print(['hsdp_',filename],'-depsc2','-r1200');
% 

%                TP vs. DP
clear n1 n xb yb X class axes1
class{1}=0:45:360;class{2}=1:2:22;
X = [dp,tp];n = hist3(X,class);
n1 = ((n'.*100)/length(hs)); 
n1( size(n,2) + 1 ,size(n,1) + 1 ) = 0; 
xb = linspace(-22.5,382.5,size(n,1)+1);
yb = linspace(0,22,size(n,2)+1);


figure
pos = get(gcf, 'Position');
set(gcf, 'Position', [pos(1) pos(2) width*100, height*100]); %<- Set size
set(gca, 'FontSize', fsz, 'LineWidth', alw,'FontName','Arial');
pcolor(xb,yb,n1);colormap(flipud(gray));
for a=1:length(n(:,1));
    for b=1:length(n(1,:));
        if (n(a,b)*100/length(hs)>0.01);
            label=num2str(n(a,b)*100/length(hs),'%.2f');
            text(xb(a)+10,yb(b)+0.5,label,'fontsize',9,'fontweight','b','color','r','fontname','Arial');
        end
    end
end

ylabel('Periodo de Pico (s)','fontsize',10,'FontWeight','n','fontname','Arial')
xlabel('Direcao de Pico (graus)','fontsize',10,'FontWeight','n','fontname','Arial')
set(gca,'XTick',[-5,45,90,135,180,225,270,315,360],'XTickLabel',{'N','NE','E','SE','S','SW','W','NW','N'})  
cm=colorbar('FontWeight','n','FontSize',10);
set(get(cm,'ylabel'),'String', 'Porcentagem de Ocorrencia (%)',...
    'fontsize',10,'fontname','Arial');
ylim([2 22]);xlim([-5 270])
caxis([0, axtpdp])
% Here we preserve the size of the image when we save it.
set(gcf,'InvertHardcopy','on');
set(gcf,'PaperUnits', 'inches');
papersize = get(gcf, 'PaperSize');
left = (papersize(1)- width)/2;
bottom = (papersize(2)- height)/2;
myfiguresize = [left, bottom, width, height];
set(gcf,'PaperPosition', myfiguresize);

% Save the file as PNG
print(['tpdp_',filename],'-dpng','-r300');
print(['tpdp_',filename],'-depsc2','-r1200');
