% 
close all;
clear all;
clc 
%==========================================================================
%                               PARTE I
%GRADE GLOBAL : 
%==========================================================================

%Leitura da Batimetria litoral_lon_lat
A=load('BATIMETRIA_latlon_MERGE_interp.txt');

% % leitura da linha de costa
% AL=load('latlon_costa_izabel.txt');
% XL=AL(:,1);
% YL=AL(:,2);
% ZL=ones(length(XL),1)*-99;
% 
% % retirando linha de costa anterior
% nL=find(ZB>=0);
% XB1=XB(nL);
% YB1=YB(nL);
% ZB1=ZB(nL);
% 
% XB=[XB1;XL];
% YB=[YB1;YL];
% ZB=[ZB1;ZL];

% % % interpolar UTM
% xmin=min(XB);xmax=max(XB);
% ymin=min(YB);ymax=max(YB);
% dx=0.001;
% dy=0.001;
% [X Y]=meshgrid(xmin:dx:xmax,ymin:dy:ymax);
% [Z]=griddata(XB,YB,ZB,X,Y,'nearest');%inverter x e y

%
MXG=2053;%818;%576;
NYG=1869;%1009;%165;

NG=0;
for i=1:MXG
    for j=1:NYG
        NG=NG+1;
        XG(j,i)=A(NG,1);  %1,2  eh o indice (i,j) da grade
        YG(j,i)=A(NG,2);  %3,4 sao as coordenada UTM e 5 é a profundidade
        ZG(j,i)=A(NG,3);  %positivo para abaixo do nivel medio da agua.
    end
end

figure()
[C,h]=contour(XG,YG,ZG,30);
clabel(C,h)

%==========================================================================
%=========================== PARTE II =====================================
%GRADE 1
% X0= -40.06;   %Grade paralela a batimetria
% Y0= -20.65;   %Grade paralela a batimetria
% MX=85;
% NY=82;
% DX=0.005;
% DY=0.005;
% ARG= 60.;

% %GRADE 2   %%%% Grade do SWAN_FINE (pegar informações do SWAN)
X0= -40.2613;
Y0= -20.34;
MX=115;%60;
NY=95;%45;
DX=0.0005;%0.01;
DY=0.0005;%0.01;
ARG= 30;
% 
% %GRADE 3
% X0= -40.0664;   %Grade paralela a batimetria
% Y0= -20.7232;   %Grade paralela a batimetria
% MX=40;
% NY=30;
% DX=0.015;
% DY=0.015;
% ARG= 65.;
% % 
% %GRADE 4
% X0= -40.0664;   %Grade paralela a batimetria
% Y0= -20.7232;   %Grade paralela a batimetria
% MX=30;
% NY=23;
% DX=0.02;
% DY=0.02;
% ARG= 65.;
%=======================================================================
ARG=ARG*pi/180.;
%=======================================================================
LX=DX*(MX-1);
LY=DY*(NY-1);

X(1)=X0;
Y(1)=Y0;

X(2)=X(1)+LX*cos(ARG);
Y(2)=Y(1)+LX*sin(ARG);

X(3)=X(2)-LY*sin(ARG);
Y(3)=Y(2)+LY*cos(ARG);

X(4)=X0-LY*sin(ARG);
Y(4)=Y0+LY*cos(ARG);

X(5)=X0;
Y(5)=Y0;

hold on
plot(X,Y,'--rs','LineWidth',2,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g',...
    'MarkerSize',10)
% axis equal
hold on
xadcp=[-40.2086;-40.2419;-40.2600;-40.2793];
yadcp=[-20.3402;-20.2978;-20.2972;-20.3167];
plot(xadcp,yadcp,'k*','markersize',9)

figure()
Xmin=min(X);
Xmax=max(X);
Ymin=min(Y);
Ymax=max(Y);
contourf(XG,YG,ZG,15);

hold on;
plot(X,Y,'--rs','LineWidth',2,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g',...
    'MarkerSize',10)
axis equal
%axis([Xmin Xmax Ymin Ymax]);
xlim([Xmin Xmax]);
ylim([Ymin Ymax]);
zlim([0 100]);
hold off

