close all
clear all
clc
%
%
%==========================================================================
%==========================================================================
%
% GRADE DO VIX_FINE
% Eixo X
mx=115;       % numero de pontos ao longo do eixo X
% Eixo Y
ny=95;       % numero de pontos ao longo do eixo Y
% % GRADE 2
% mx=48;       % numero de pontos ao longo do eixo X
% ny=36;       % numero de pontos ao longo do eixo Y
% % GRADE 3
% mx=40;       % numero de pontos ao longo do eixo X
% ny=30;       % numero de pontos ao longo do eixo Y
% % GRADE 3
% mx=30;       % numero de pontos ao longo do eixo X
% ny=23;       % numero de pontos ao longo do eixo Y
%
%==========================================================================
%==========================================================================
%==========================================================================
dx=1;             % nao mexer
dy=1;             % nao mexer
xmin=0;           % nao mexer
xmax=dx*(mx-1);   % nao mexer
ymin=0;           % nao mexer
ymax=dy*(ny-1);   % nao mexer
%
%==========================================================================
%==========================================================================
% Referencia: Definicao dos parametros no eixo Xi.
xi_0=0.;
%--------------------------------------------------------------------------
%calculo dos pontos da grade na direcao X
i=1;
xi(i)=xi_0;
while i <= mx-1
    s=i*dx;
    xi_s=xi_0+s;
    i=i+1;
    xi(i)=xi_s;
end
%--------------------------------------------------------------------------
%calculo dos pontos da grade na direcao y
j=1;
yj(j)=xi_0;
while j <= ny-1
    s=j*dy;
    xi_s=xi_0+s;
    j=j+1;
    yj(j)=xi_s;
end
%==========================================================================
% Geracao dos pontos da Grade X
save('xgrade.dat','xi','-ascii')
% Geracao dos pontos da Grade Y
save('ygrade.dat','yj','-ascii')
%==========================================================================
%Geracao da profundidade plana.
for j=1:ny
    y_j=yj(j);
    for i=1:mx
        x_i=xi(i);
        xg(j,i)=x_i;
        yg(j,i)=y_j;
        zg(j,i)=1.;
    end
end
mesh(xg,yg,-zg)
%==========================================================================
save('xg.dat','xg','-ascii')
save('yg.dat','yg','-ascii')
save('zg.dat','zg','-ascii')


