
figure(1);clf;
v=[0 24 0 192];axis(v);
x=[0;24];y=[0;0];
for k1=1:25,
    line(x,y,'color',[0 0 0],'linewidth',0.4);
    y=y+8;
    
end
x=[-1;25];y=[0;0];
for k1=1:25,
    line(x,y,'color',[0 0 0],'linewidth',1.5);
    y=y+32;
end

x=[0;0];y=[0;192];
for k1=1:7,
    line(x,y,'color',[0 0 0],'linewidth',1.0);
    x=x+4;
end

x=[0;0];y=[0;192];
for k1=1:24,
    line(x,y,'color',[0 0 0],'linewidth',0.2);
    x=x+1;
end
axis off


k1=3;
hs1=[1.1;2.6;4.1;6.1];n=0;
for k2=1:8:25,k2=k2-1;n=n+1;hs=hs1(n);
    %cor(2:3)=cor(2:3)+0.3
    x=[k1;k1+1;k1+1;k1];
    y=[k2;k2;k2+8;k2+8];
    if hs>1,cor=[1 0.8 0.8];end
    if hs>2.5,cor=[1 0.6 0.6];end
    if hs>4,cor=[1 0.4 0.4];end
    if hs>6,cor=[0 0 0];end
    patch(x,y,cor)
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

k1=0;
hs1=[0.51;1.61;2.51;3.1];n=0;
for k2=1:8:25,k2=k2-1;n=n+1;hs=hs1(n);	
    %cor(2:3)=cor(2:3)+0.3
    x=[k1;k1+1;k1+1;k1];
    y=[k2;k2;k2+8;k2+8];
    if hs>0.5,cor=[0.9 0.9 1];end
    if hs>1.6,cor=[0.65 0.65 1];end
    if hs>2.5,cor=[0.4 0.4 1];end
    if hs>3.0,cor=[0 0 1];end
    patch(x,y,cor)
end

k1=1;
hs1=[0.51;1.61;2.51;3.1];n=0;
for k2=1:8:25,k2=k2-1;n=n+1;hs=hs1(n);
    %cor(2:3)=cor(2:3)+0.3
    x=[k1;k1+1;k1+1;k1];
    y=[k2;k2;k2+8;k2+8];
    if hs>0.5,cor=[0.9 1 0.9];end
    if hs>1.6,cor=[0.75 1 0.75];end
    if hs>2.5,cor=[0.45 1 0.45 ];end
    if hs>3.0,cor=[0 1 0 ];end
    patch(x,y,cor)
end

k1=2;
hs1=[1.1;2.1;3.1;4.1];n=0;
for k2=1:8:25,k2=k2-1;n=n+1;hs=hs1(n);
    %cor(2:3)=cor(2:3)+0.3
    x=[k1;k1+1;k1+1;k1];
    y=[k2;k2;k2+8;k2+8];
    if hs>1,cor=[0.9 1 1 ];end
    if hs>2,cor=[0.75 1 1];end
    if hs>3,cor=[0.45 1 1];end
    if hs>4,cor=[0 1 1 ];end
    patch(x,y,cor)
end

mes=['jan';'fev';'mar';'abr';'mai';'jun'];
k2=-1.5;k3=-16;
for k1=1:6,k3=k3+32;
    text(k2,k3,mes(k1,:));
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%;
ano=['1990';'1991';'1992';'1993';'1994';'1995'];
k2=-2.75;k3=-5;
for k1=1:6,k2=k2+4;
    text(k2,k3,ano(k1,:));
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Henrique, um folha A4 leva 6 meses e 4 anos; cada mes tem 4 semanas, 4
%faixas de frequencias e amplitudes de Hs média (cores) para cada semana;
%as faixas e as cores podem ser vistas no programa.