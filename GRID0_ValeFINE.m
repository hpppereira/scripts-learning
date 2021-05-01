% Rotina de de Izabel Nogueira (Adaptada para Lat Lon)
% GRID 0
% =========================================
% ROTINA PARA GERAR UM GRID DE UM YXZ DE BATIMETRIA
% Ideal é entrar com o dados em UTM ja, caso esteja em latlon usar a funcao
% deg2utm
% converter para UTM
% [xi,yi,utmzonei]=deg2utm(lati,loni);


% proximo passo: rodar GRID1.m (mudano do o nx e ny)

close all;clc;clear all

% % pegar a batimetria digitalizada
% load batimetriaWGS.txt;
% loni=batimetriaWGS(:,1);lati=batimetriaWGS(:,2);
% zi=batimetriaWGS(:,3);
% %converter para UTM
% [xi,yi,utmzonei]=deg2utm(lati,loni);

% obs: estava dando problema - transformei (graus para UTM) logo no GQGIS
batimetria=load ('BATIMETRIA_latlon_MERGE.txt');
xi=batimetria(:,1);
yi=batimetria(:,2);
zi=batimetria(:,3);

%%% No merge já tem linha de costa
% % pegar a linha de costa
% costa=load ('linha_costa_latlon');
% yl=costa(:,2);
% xl=costa(:,1);
% zl=costa(:,3);

% %concatenar dados
% x=[xi;xl];y=[yi;yl];z=[zi;zl];
x=xi;y=yi;z=zi;

% % interpolar UTM
xmin=min(x);xmax=max(x);
ymin=min(y);ymax=max(y);
dx=0.0002;%Cerca de 20m
dy=0.0002;
[X Y]=meshgrid(xmin:dx:xmax,ymin:dy:ymax);
[Z]=griddata(x,y,z,X,Y,'linear');%inverter x e y

nt=length(X(:,1))*length(X(1,:));

x1=reshape(X,[nt,1]);
y1=reshape(Y,[nt,1]);
z1=reshape(Z,[nt,1]);

fid1 = fopen('BATIMETRIA_latlon_MERGE_interp.txt', 'w');
for j=1:length(z1);
    fprintf(fid1,'%6.3f %6.3f %6.3f\r\n',x1(j),y1(j),z1(j));
end
fclose(fid1);

% stop
% clear x1 y1 z1
% % % interpolar LATLON
% zone='23 K'
% utmzone=cellstr(zone);
% % %convertendo para lat lon
% for i=1:length(x)-1;
%     utmzone1='23 K';
%     utmzone2=cellstr(utmzone1);
%     utmzone=[utmzone;utmzone2];
% end
% 
% utmzonef=char(utmzone);
% [Lati, Loni]=utm2deg(x,y,utmzonef);
% %linhadecosta
% load costaItaornaLatLon.txt
% Latl=costaItaornaLatLon(:,2);
% Lonl=costaItaornaLatLon(:,1);
% batl=costaItaornaLatLon(:,3);
% 
% Lat=[Lati;Latl];
% Lon=[Loni;Lonl];
% z=[z;batl];
% 
% xmin=min(Lon);xmax=max(Lon);
% ymin=min(Lat);ymax=max(Lat);
% dx=0.002;
% dy=0.002;
% [X Y]=meshgrid(xmin:dx:xmax,ymin:dy:ymax);
% [Z]=griddata(Lon,Lat,z,X,Y,'nearest');%inverter x e y
% 
% nt=length(X(:,1))*length(X(1,:));
% 
% x1=reshape(X,[nt,1]);
% y1=reshape(Y,[nt,1]);
% z1=reshape(Z,[nt,1]);
% 
% fid1 = fopen('batimetriaLATLON.txt', 'w');
% for j=1:length(z1);
%     fprintf(fid1,'%6.3f %6.3f %6.3f\r\n',x1(j),y1(j),z1(j));
% end
% fclose(fid1);
% 
% 
