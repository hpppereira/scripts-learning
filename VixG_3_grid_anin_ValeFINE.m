% %
close all;
clear all;
clc

%==========================================================================
%                               PARTE I
%GRADE GLOBAL : 
%==========================================================================
%
MXG=2053;%576;
NYG=1869;%165;
%Leitura da Batimetria
A=load('BATIMETRIA_latlon_MERGE_interp.txt');
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
% %GRADE 2
% X0= -40.0664;   %Grade paralela a batimetria
% Y0= -20.7232;   %Grade paralela a batimetria
% MX=48;
% NY=36;  
% DX=0.0125;
% DY=0.0125;
% ARG= 65.;
% 
% %GRADE 3
% X0= -40.0664;   %Grade paralela a batimetria
% Y0= -20.7232;   %Grade paralela a batimetria
% MX=40;
% NY=30;
% DX=0.015;
% DY=0.015;
% ARG= 65.;

% %GRADE 4
% X0= -40.0664;   %Grade paralela a batimetria
% Y0= -20.7232;   %Grade paralela a batimetria
% MX=30;
% NY=23;
% DX=0.02;
% DY=0.02;
% ARG= 65.;

%==========================================================================
%==========================================================================
%==========================================================================
%IMPRESSAO DOS DADOS DA GRADE
CMX=num2str(MX);
CNY=num2str(NY);
Gradename='';
Origemname='';
Origemname=['origem',CMX,'X',CNY,'.dat'];
Gradename=['grade',CMX,'X',CNY,'.dat'];
%
fid = fopen(Origemname,'w');
fprintf(fid,'    %16.6f    %16.6f\n',X0,Y0);
fclose(fid);
fid = fopen(Gradename,'w');
fprintf(fid,'%5.0f %5.0f %10.2f %10.2f %10.2f\n',MX,NY,DX,DY,ARG);
fclose(fid);
%=======================================================================
ARG=ARG*pi/180.
%=======================================================================
%============ COORDENADAS GLOBAIS EM RELACAO A GRADE ===================
XGX0=(XG-X0);
YGY0=(YG-Y0);
XG0= XGX0*cos(ARG)+YGY0*sin(ARG);
YG0=-XGX0*sin(ARG)+YGY0*cos(ARG);
%COORDENADAS GLOBAIS NA FORMA ADIMENCIONAL
XGA=XG0/DX;
YGA=YG0/DY;
%=======================================================================
%======= CAPTURA E IMPRESSAO DAS PROFUNDICADES DA GRADE MXxNY ==========
Depthname=['Depth',CMX,'X',CNY,'.dat']
fid = fopen(Depthname,'w');
i=0;
for IG=1:MXG
    j=0;
    for JG=1:NYG
        Xij=XGA(JG,IG);
        Yij=YGA(JG,IG);
        Zij=ZG(JG,IG);
        if ((Xij>=0-7) & (Xij<=MX+7)) & ((Yij>=0-13) & (Yij<=NY+13))
            if IG > i
                i=i+1;
            end
            j=j+1;
            fprintf(fid,'%16.6f %16.6f %16.6f\n',Xij,Yij,Zij);
        end
    end
end
fclose(fid);
%=======================================================================
%========== LEITURA DAS PROFUNDIDADES DA GRADE GLOBAL QUE SE ENCONTRAM
%========== NA REGIAO DE ESTUDO ........DepthMXxNY.dat     =============
%========== E GERANDO A GRADE DA REGIAO DE ESTUDO = X,Y,Z  =============
clear A;
A=load(Depthname);
%-----------------------------------------------------------------------
% Xmin=0.;
% Xmax=MX-1;
% Ymin=0.;
% Ymax=NY-1.;
% [X,Y] = meshgrid(Xmin:1:Xmax,Ymin:1:Ymax);
load 'xg.dat'
load 'yg.dat'
Xmin=min(min(xg));
Xmax=max(max(xg));
Ymin=min(min(yg));
Ymax=max(max(yg));
zg = griddata(A(:,1),A(:,2),A(:,3),xg,yg);

figure()
mesh(xg,yg,-zg)
% figure(2)
% contour(xg,yg,zg,30)
%=======================================================================
%======= FAZENDO ALGUM TIPO DE MANIPULACAO NAS PROFUNDIDADES DA   ======
%======= GRADE xg,yg,zg E SALVANDO A GRADE RESULTANTE PARA O FUNWAVE ======
Depthname=['Jurema',CMX,'X',CNY,'.dat']
fid = fopen(Depthname,'w');
hmin=-2.0;
for I=1:1:MX
    %     for I=MX:-1:1
    %     for J=NY:-1:1
    for J=1:1:NY
        Xij=xg(J,I);
        Yij=yg(J,I);
        SX=Xij*DX;
        SY=Yij*DY;
        XA=X0+SY*cos(ARG+pi/2.);
        YA=Y0+SY*sin(ARG+pi/2.);
        XB=XA+SX*cos(ARG);
        YB=YA+SX*sin(ARG);
        Zij=zg(J,I);
        if Zij < hmin
            Zij=hmin;
        end
        % fazendo uma translacao das coordenadas:
        % Mudando o referencial de coordenadas para o Funwave
        %         Xij=Xmax-Xij;
        %         Yij=Ymax-Yij;
        fprintf(fid,'%16.6f %16.6f %16.6f %16.6f %16.6f %16.6f\n',Xij,Yij,XB,YB,Zij,-Zij);
    end
end
fclose(fid);
% figure();
% %contour(xg,yg,zg,30);
% contour(zg,30);
%======== LEITURA DAS PROFUNDICADES DA GRADE BES MXxNY ====================
%======== VISUALIZACAO SEGUNDO O REFERENCIAL USADO NO SWAN ================
clear A;
clear X;
clear Y;
clear Z;
A=load(Depthname);
X = reshape(A(:,1),NY,MX);
Y = reshape(A(:,2),NY,MX);
Z = reshape(A(:,5),NY,MX);
figure()
contour(X,Y,Z,30)   % visualizacao da batimetria da regiao de estudo
%==========================================================================
% VISUALIZACAO DO Z 
figure()
mesh(X,Y,-Z)  % Visualizacao do arquivo depth.dat
% Forma que sera impressa a batimetria da
% regiao de estudo: SWAN

%save('Xd.dat','X','-ASCII')
%save('Yd.dat','Y','-ASCII')
save('depth.dat','Z','-ASCII')
%==========================================================================
