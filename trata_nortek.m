
clc
clear


%carregando dados
sen = load ('C:\projetos\2011\Porto\dados corrente\cepsul\cps_0104.sen');

a1 = load ('C:\projetos\2011\Porto\dados corrente\cepsul\cps_0104.a1');
a2 = load ('C:\projetos\2011\Porto\dados corrente\cepsul\cps_0104.a2');
a3 = load ('C:\projetos\2011\Porto\dados corrente\cepsul\cps_0104.a3');

u = load ('C:\projetos\2011\Porto\dados corrente\cepsul\cps_0104.v1');
v = load ('C:\projetos\2011\Porto\dados corrente\cepsul\cps_0104.v2');
v3 = load ('C:\projetos\2011\Porto\dados corrente\cepsul\cps_0104.v3');

%35 celulas de 0,5 metros

pres=sen(:,14);
u=u(:,1:9);
v=v(:,1:9);
a1=a1(:,1:9);
a2=a2(:,1:9);
a3=a3(:,1:9);

%ajustando tempo
for i=1:length(sen)
    decdia(i)= sen(i,2) + sen(i,4)/24 + sen(i,5)/(24*60);
end

for i=1:length(decdia)
    tempo(i)=juliano2(decdia(i),sen(i,1),sen(i,3));
end


%transformando u e v para velocidade e direçao
[a,b]=size(u);

u1=reshape(u,a*b,1);
v1=reshape(v,a*b,1);

[vel,dire]=uvparaveldir(u1,v1);

vel=vel';

ang=declina2(2011);
dire=dire-ang;

for i=1:length(dire)
    if dire(i) < 0
        dire(i)=dire(i)+360;
    else 
        dire(i)=dire(i);
    end
end

% vel=reshape(vel,a,b);
% dire=reshape(dire,a,b);

%separando em enchente e vazante
for i=1:length(vel)
    if dire(i) > 28 & dire(i) < 208
       vel(i)= -vel(i);
   end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%calculo mps
[REA]=pororoca(a1,a2,a3,30,0.5,0.41,0.42,22);
    
REO=148.2374-7.6152*REA+0.0999*(REA).^2;
    
MPS=3.2410+2.38469*REO;

[a,b]=size(MPS);
mps1=reshape(MPS,a*b,1);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

t=tempo;
z=1:.5:5;

[tt,zz]=meshgrid(t,z);
[a,b]=size(tt);

tt=reshape(tt,a*b,1);
zz=reshape(zz,a*b,1);
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear a1 a2 a3 u v a b ang i j 
figure

%fazendo poligono para pintar a superficie
x2=tempo;
p2=pres';
x2=[x2 x2(end) x2(1) x2(1)];
p2=[p2 max(p2)+.2 max(p2)+.2 p2(1)];


subplot(2,1,1)
xi=linspace(min(tt),max(tt),60);
yi=linspace(1,5,30);
veli=griddata(tt,zz,vel,xi',yi);

contourf(xi,yi,veli);
colorbar

hold on
fill(x2,p2,'k')
plot(tempo,FILTBIN(pres,5),'k')
hold off
% set(gca,'xlim',[5 31])
title('Velocidade de Correntes (m/s)')
ylabel('Distancia do fundo (m)')

subplot(2,1,2)
mpsi=griddata(tt,zz,mps1,xi',yi);

contourf(xi,yi,mpsi);
colorbar

hold on
fill(x2,p2,'k')
plot(tempo,filtbin(pres,5),'k')
hold off
%set(gca,'xlim',[5 31])
title('Material Particulado em Suspensao (mg/L)')
ylabel('Distancia do fundo (m)')
xlabel('Dias Julianos')

figure %(figura de vel media, mps medio, e profundidade)
vell=nanmean(veli);
mps11=nanmean(mpsi);
subplot(3,1,1);plot(tempo,filtbin(pres-min(pres),5),'k')
%set(gca,'ylim',[6 8])
ylabel('Nivel de agua (m)')
set(gca,'xticklabel',[])
set(gca,'xlim',[266.43 271.6])
subplot(3,1,2);plot(xi,vell,'k')
%set(gca,'ylim',[-5 5])
set(gca,'xticklabel',[])
set(gca,'xlim',[266.43 271.6])
ylabel('Velocidade (m/s)')
subplot(3,1,3);plot(xi,mps11,'k')
%set(gca,'ylim',[30 500])
set(gca,'xlim',[266.43 271.6])
ylabel('MPS (mg/L)')
xlabel('Dias Julianos')