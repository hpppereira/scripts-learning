% ------------------------------------------------------------------
% -------------------  INTRA-ANUAL --------------------------------- 
%                       HS vs. TP

close all;clear all;clc

geral = dlmread('/home/hp/Dropbox/ww3br/rot/saida/recife/paramwp_32-recife.out',',',2);


%load geral.txt

hs=geral(:,7);tp=geral(:,8);dp=geral(:,9);

class{1}=0.5:1:24;class{2}=0:0.2:5.8;
%xb=class{1};yb=class{2};
X = [tp,hs];n=hist3(X,class);n1 = ((n'.*100)/length(hs)); 
n1( size(n,2) + 1 ,size(n,1) + 1 ) = 0; 
xb = linspace(0,24,size(n,1)+1);
yb = linspace(-0.1,5.9,size(n,2)+1);

figure1=figure(1);
clear axes1
axes1=axes('Parent',figure1,'FontSize',16,'FontWeight','b');
hold(axes1,'all');box(axes1,'on');grid(axes1,'on');
pcolor(xb,yb,n1);colormap(flipud(gray));
for a=1:length(n(:,1));
    for b=1:length(n(1,:));
        if (n(a,b)>0);
            label=num2str(n(a,b));
            text(xb(a)+0.3,yb(b)+0.1,label,'fontsize',14,'fontweight','b','color','r');
        end
    end
end
ylabel('Altura Significativa (m)','fontsize',19,'FontWeight','b')
xlabel('Periodo de Pico (s)','fontsize',19,'FontWeight','b')
cm=colorbar('FontWeight','bold','FontSize',16);
set(get(cm,'ylabel'),'String', 'Porcentagem de Ocorrencia (%)',...
    'fontsize',18);
% text(max(max(xb))-4,max(max(yb))-4,num2str(length(hs)),'fontsize',18,'color','r');
% text(max(max(xb))-4,max(max(yb))-4,'N_{total}: ','fontsize',18,'color','r');
text(17,5,['Total = ',num2str(length(geral))],'color','r')
ylim([0 5.9]);xlim([0 22])

%  csvwrite('csvlist.dat',m)


% fid = fopen('hstp.txt', 'w');
% for i=1:length();
%     fprintf(fid,'%6.2f %6.2f\r\n', vel_gfs10(i),dir_gfs10(i));
% end
% fclose(fid);
% 
% 


%                    HS vs, DP
clear n n1 xb yb X class axes1
class{1}=0:45:360;class{2}=0.2:0.2:5.8;
%xb=class{1};yb=class{2};
X = [dp,hs];n = hist3(X,class); 
n1 = ((n'.*100)/length(hs)); 
n1( size(n,2) + 1 ,size(n,1) + 1 ) = 0; 
xb = linspace(-22.5,382.5,size(n,1)+1);
yb = linspace(0.1,5.9,size(n,2)+1);

figure2=figure(2);
axes1=axes('Parent',figure2,'FontSize',16,'FontWeight','b',...
    'XTickLabel',{'N','NE','E','SE','S','SW','W','NW','N'},...
    'XTick',[-5 45 90 135 180 225 270 315 360 410]);
hold(axes1,'all');box(axes1,'on');grid(axes1,'on');    
pcolor(xb,yb,n1);colormap(flipud(gray));
for a=1:length(n(:,1));
    for b=1:length(n(1,:));
        if (n(a,b)>0);
            label=num2str(n(a,b));
            text(xb(a)+20,yb(b)+0.08,label,'fontsize',14,'fontweight','b','color','r');
        end
    end
end
ylabel('Altura Significativa (m)','fontsize',19,'FontWeight','b')
xlabel('Direcao de Pico (g)','fontsize',19,'FontWeight','b')
cm=colorbar('FontWeight','bold','FontSize',16);
set(get(cm,'ylabel'),'String', 'Porcentagem de Ocorrencia (%)',...
    'fontsize',18);
% text(max(max(xb))-130,max(max(yb))-4,num2str(length(hs)),'fontsize',18,'color','r');
% text(max(max(xb))-130,max(max(yb))-4,'N_{total}: ','fontsize',18,'color','r');
text(292.4,5,['Total = ',num2str(length(geral))],'color','r')
ylim([0 5.9]);xlim([-5 360])



%                TP vs. DP
clear n1 n xb yb X class axes1
class{1}=0:45:360;class{2}=0.5:1:24;
%xb=class{1};yb=class{2};
X = [dp,tp];n = hist3(X,class);
n1 = ((n'.*100)/length(hs)); 
n1( size(n,2) + 1 ,size(n,1) + 1 ) = 0; 
xb = linspace(-22.5,382.5,size(n,1)+1);
yb = linspace(0,24,size(n,2)+1);

figure3=figure(3);
axes1=axes('Parent',figure3,'FontSize',16,'FontWeight','b',...
    'XTickLabel',{'N','NE','E','SE','S','SW','W','NW','N'},...
    'XTick',[-5 45 90 135 180 225 270 315 360 410]);
hold(axes1,'all');box(axes1,'on');grid(axes1,'on');
pcolor(xb,yb,n1);colormap(flipud(gray));
for a=1:length(n(:,1));
    for b=1:length(n(1,:));
        if (n(a,b)>0);
            label=num2str(n(a,b));
            text(xb(a)+20,yb(b)+0.3,label,'fontsize',14,'fontweight','b','color','r');
        end
    end
end

ylabel('Periodo de Pico (s)','fontsize',19,'FontWeight','b')
xlabel('Direcao de Pico (g)','fontsize',19,'FontWeight','b')
cm=colorbar('FontWeight','bold','FontSize',16);
set(get(cm,'ylabel'),'String', 'Porcentagem de Ocorrencia (%)',...
    'fontsize',18);
% text(max(max(xb))-130,max(max(yb))-4,num2str(length(hs)),'fontsize',18,'color','r');
% text(max(max(xb))-130,max(max(yb))-4,'N_{total}: ','fontsize',18,'color','r');
text(292.4,18.5,['Total = ',num2str(length(geral))],'color','r')
ylim([0 5.9]);xlim([-5 360])
ylim([0 22]);xlim([-5 360])
