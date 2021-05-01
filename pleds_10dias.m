% -----------------------------------------------------------------------
%programa pleds10dias para trabalho IBAMA
%plotagem para 10 dias
%dados de entrada: vetores dire e espe gerados
% ------------------------------------------------------------------------
%close all;clear all; clc
% ESCOLHER ANO E MES
mes=03;ano=92;
% ESCOLHER PERIODO DE PLOTAGEM
dp1=17;dp2=31;
% FILTRAGEM
%filtrapledsibama1
%filtravento2
% PLOTAR
f2=figure(2);
clf reset
%df=f1(2)-f1(1);

%local=input('stationname = ');
%mes = input('mes = ');
%ano= input('ano = ');
% mes=4;
% ano=1991
%plotagem inicial e defini��o de eixos e outros par�metros;
%mes=1;ano=2001;
a=0;plot(a,'w');
c=[0 24.1 0 143];axis(c);
v6=hanning(129);v61=hanning(60);
ad1=[31;29;31;30;31;30;31;31;30;31;30;31];
axis('off')
%df=f(2)-f(1);
col=[0.5 0.5 0.5];
%linhas ve7rticais;
y=[20;18*8+20];
for i=1:1:19,
    x=[i;i];line(x,y,'color',col,'linewidth',[0.2]);
end
%x=[22;22];line(x,y,'color',col,'linewidth',[0.2]);
%linhas horizontais com "tick";
%x=[0.9;22.1];
x=[0.9;19.1];
for i=20:8:15*8+20,
    y=[i;i];line(x,y,'color',col);
end

%linhas horizontais
x=[1;19];
for i=20:2:15*8+20+7,
    y=[i;i];line(x,y,'color',col);
end
x=[1;21.8];y=[19;19];line(x,y,'color',[0.6 0.6 0.6],'linewidth',3)
x=[1;21.8];y=[142;142];line(x,y,'color',[0.6 0.6 0.6],'linewidth',3)
x=[1;1];y=[19;142];line(x,y,'color',[0.6 0.6 0.6],'linewidth',3)
x=[19;19];y=[19;142];line(x,y,'color',[0.6 0.6 0.6],'linewidth',3)
x=[21.9;21.9];y=[19;142];line(x,y,'color',[0.6 0.6 0.6],'linewidth',3)
%dias de plotagem
dp=[dp1:dp2];
%dias do m�s de 1 a 9, eixo vertical
a=2.7+10;
for i=1:15,a=a+8;
    x=dp(i);x1=.50;
    if x<10,x1=0.66;end
    text(x1,a,num2str(x),'fontsize',13);
    %text(19.1,a,num2str(x),'fontsize',9);
end;

a=2.7+10+8;
for i=2:15,a=a+8;
    x=dp(i);x1=.50;
    if x<10,x1=0.66;end
    %text(x1,a,num2str(x),'fontsize',9);
    text(19.1,a,num2str(x),'fontsize',13);
end;
sf11
%arquivo de m�s
ad=['jan';'fev';'mar';'abr';'mai';'jun';'jul';'ago';'set';'out'];
ad=[ad;'nov';'dez'];

%cores das diferentes faixas de per�odos
%arq2=[[1 0 0];[1 0 0];[1 0.7 0];[1 0.7 0];[1 1 0];...
%         [1 1 0];[0.2 1 0.2];[0.2 1 0.2];...
%        [0.4 0.7 1];[0.4 0.7 1]];
        
arq3=[[1 0 0];
      [1 1 0];
      [0 1 0];
      [0.59 0.59 1]];
%plotagem do espectro direcional a cada dia por faixa de per�odos
%plota de cima para baixo (de 31 para 1)
set(gcf,'paperposition',[0 0 19  9.5],'papertype','A4');
%set (gcf,'position',[1 1 1 1]);
%eixo horizontal de dire��o
a=310:20:720;a=a';
a1=find(a>360);a(a1)=a(a1)-360;
for i=1:18,x2=0.15;
    if a(i)<100,x2=0.31;end;
    text(i+x2,21.5,num2str(a(i)),'fontsize',11,'color','k');
end;



% d=1.5:1:19.5;
%for i=1:18,text(d(i),20.2,'|','fontsize',6,'color','r','fontweight','bold');end;

ld=['NW';'N ';'NE';'E ';'SE';'S ';'SW';'W ';'SW';'W '];
k=1.55;

d1=[1.75;4;6.25;8.5;10.75;13;15.25;17.5];
d2=[1.67;4;6.15;8.52;10.65;13.0;15.15;17.45];
for i=1:8,
    text(d2(i)-0.12,140,ld(i,:),'fontsize',12,'color','b');
    text(d1(i),142,'|','fontsize',6,'color','r','fontweight','bold')
    k=k+2.25;
end;

%text(1.1,15,'dire��o onda e vento','fontsize',10,'color','k');
%text(1.3,70,['---- ' 'dia do m�s' ' ----'],'fontsize',11,'rotation',90);
%text(1.1,12,['periodos em segundos' '-->'],'fontsize',10,'color','k');
col=[0.9 0.9 0.9];xx=8.13;
%codigo de cores para faixas de periodos
x=[19.8;21.8;21.8;19.8];y=[11.8;11.8;20.;20.];
y=y+xx;patch(x,y,col);
y=y+xx;patch(x,y,col);
y=y+xx;patch(x,y,col);
y=y+xx;patch(x,y,arq3(1,:));
y=y+xx;patch(x,y,arq3(2,:));
y=y+xx;patch(x,y,arq3(3,:));
y=y+xx;patch(x,y,arq3(4,:));
%x=x+2.5;patch(x,y,arq3(5,:));
y=y+xx;patch(x,y,col);
y=y+xx;patch(x,y,col);
y=y+xx;patch(x,y,[0.6 0.6 0.6]);
y=y+xx;patch(x,y,col);
y=y+xx;patch(x,y,col);
y=y+xx;patch(x,y,col);
y=y+xx;patch(x,y,col);
y=y+xx;patch(x,y,col);

x1=[19.0;19.8];y1=[21;21];
line(x1,y1,'color',[0 0 0],'linewidth',2)
x1=[18.9;19.2];y1=[21;22.1];
line(x1,y1,'color',[0 0 0],'linewidth',2)
x1=[18.9;19.2];y1=[21;20.1];
line(x1,y1,'color',[0 0 0],'linewidth',2)
%y=y+16;patch(x,y,[1 1 1]);
%y=y+16;patch(x,y,[1 1 1]);

% k1=['18.6 a 11.2';'11.2 a 8.0 ';'8.0 a 4.80 '];
% k1=[k1;'4.80 a 3.40';'3.40 a 2.66';'T em seg.  '];
% k1=['20.0 a 10.2';...
%     '10.2 a 7.75';...
%     '7.75 a 3.93';...
%     '3.93 a 2.50';];
% %k1=[];
k1=['20.0-10.2';...
    '10.2-7.75';...
    '7.75-3.93';...
    '3.93-2.50';];

k=40;
% %faixas de periodos;
 for i=1:4,k=k+xx;
     text(19.9,k,k1(i,:),'fontsize',16);
 end;

 x1=[21.61;21.61];y1=[36;43];
line(x1,y1,'color',[0 0 0],'linewidth',2)
x1=[21.78;21.6];y1=[40;44];
line(x1,y1,'color',[0 0 0],'linewidth',2)
x1=[21.41;21.6];y1=[40;44];
line(x1,y1,'color',[0 0 0],'linewidth',2)

 text(19.9,34.5+xx,'faixas em','fontsize',13)
 text(19.9,30.5+xx,'segundos','fontsize',13)
 text(19.9,34.5-xx,'direção','fontsize',13)
 text(19.9,30.5-xx,'onda/vento','fontsize',13)
 local='MARLIM';pp=14;pp2=0.02;
 if ano>1993,
     local='BARRACUDA';pp=11;pp2=0.02;
 end
text(19.9,139.5,'DIREC.','fontsize',12,'color','r','fontweight','bold')
text(19.9,135.6,'DE ONDAS','fontsize',12','color','r','fontweight','bold')
% 
%text(15,92,['MARLIM' '  ' ad(mes,:) '/' num2str(ano)],'fontsize',10','color','b','fontweight','bold')

text(19.9+pp2,130,local,'fontsize',pp);
np=num2str(mes);
if mes<10,np=[num2str(0) np];end
np1=num2str(ano);
text(20.2,122,[np1 '/' np],'fontsize',17   ,'fontweight','bold')
text(19.95,115.3,'ESCALA','fontsize',13);
text(19.9,111.5,'DE ONDA','fontsize',13);
text(20.1,107,'Hs faixa','fontsize',13)
text(20.05,103.5,'4div=1m','fontsize',13)
text(19.9,32,'dia do mes','fontsize',14)

x1=[19.8;19.3];y1=[32;32];
line(x1,y1,'color',[0 0 0],'linewidth',2)
x1=[19.3;19.5];y1=[32;33];
line(x1,y1,'color',[0 0 0],'linewidth',2)
x1=[19.3;19.5];y1=[32;31];
line(x1,y1,'color',[0 0 0],'linewidth',2) 

text(20.2,91.5,'vento','fontsize',13);
text(20.1,87,'10m/s=4div','fontsize',12);
x=[19.91;20.01;20.01;19.91];
y=[86;86;92;92];
patch(x,y,[1 1 1]);

x=[20.;20.1;20.1;20.];
y=[80;80;84;84];
patch(x,y,[0.9 1 0]);
text(19.9,78.5,'>10','fontsize',8)

x=[20.7;20.8;20.8;20.7];
y=[80;80;84;84];
patch(x,y,[0.5 1 0]);
text(20.6,78.5,'>15','fontsize',8)

x=[21.4;21.5;21.5;21.4];
y=[80;80;84;84];
patch(x,y,[1 0.2 0.2]);
text(21.3,78.5,'>20','fontsize',8)
% x=[17.2;17.35;17.35;17.2];
% y=[k+14;k+14;k+17;k+17];
% patch(x,y,[0.9 1 0]);
% 
% x=[17.2;17.35;17.35;17.2];
% y=[k+14;k+14;k+17;k+17];
% patch(x,y,[0.5 1 0]);
% 
% x=[17.2;17.35;17.35;17.2];
% y=[k+14;k+14;k+17;k+17];
% patch(x,y,[0 1 0.7]);

% text(15,27,'Escala de Espectro','fontsize',10);
% text(14.8,24,'32 m2/Hz = 4 divis�es','fontsize',10)
% text(14.8,21,'Hs -- 1 m = 4 divis�es','fontsize',10)
% 

% text(2.5,-5,['ESPECTRO DIRECIONAL DE ONDAS' '-MARLIM-' ...
%     ad(mes,:) '/' num2str(ano)],'fontsize',13,'color','b','fontweight','bold');

% text(1,12,'Escala vertical(onda)','fontsize',10,'color','k')
% text(1,7,'  Hs2 por faixa:','fontsize',10,'color','k')
% text(1,2,'25 div.=16m2=4m(Hs)','fontsize',9,'color','k')

%text(15.75,12,'Escala vertical(vento)','fontsize',10,'color','k')
%text(15.75,7,'  barras verticais:','fontsize',10,'color','k')
%text(15.75,2,'10 divis�es=20 m/s','fontsize',10,'color','k')
%text(0.2,10,'dia do m�s','fontsize',8,'color','k','rotation',90)

tt1=121;
% for t=31*8:-1:1,c=round(energ(:,t)*10)/10;tt1=tt1-1;

bb=[0.6;0.6;0.6;0.6;0.6;0.6;0.6;0.6;0.6;0.6];
for t=dp2*8:-1:(dp1-1)*8+1,tt1=tt1-1;
%for t=107:107,
%     for k=5:5,
%         gh1=[ggh(1,t);ggh(1,t);ggh(2,t);ggh(2,t);ggh(3,t);...
%             ggh(3,t);ggh(4,t);ggh(4,t);ggh(5,t);ggh(5,t)];
%         gh2=ones(10,1);
%         q=energ(k+1,t);r=(k-1)*2+1;
%         if q<0.1*sum(energ(2:6,t)),gh2(r)=0;
%             gh2(r+1)=0;end
% 
%     end;
    %arquivo geral do dia
    s1=[ddir1(:,t)/20];
    s2=[energ(2:5,t)];
    %if t==1,sf1;end
    for i=1:4,
        
        arq=arq3(i,:);%cor
        %s11=s1(:,i);
        %s12=s2(:,i);
        s11=s1(i);
        s12=s2(i);
        % i>8,s12=10*s12;end;
        %s12=s2(i)*gh2(i);
        
        %g=find(pic>12);
        %g1=isempty(g);
         
         
    
         %if i==1, 
         %if s12<0.05*sum(energ(2:6,t)),s12=0;end;
         %if i==2,g=10ind(picos(:,t))<11;isempty(g);
         %if ans==1,s12=0;end;end;
         %if i==2,
         if i<3,
         if s12<0.1*sum(energ(2:5,t)),s12=0;end;end;
     
     
     %    if i==2,if pic(2)==0,s12=0;end;end;
%         if i==1,
%         if energ(3,t)<0.025*sum(energ(2:6,t)),s12=0;end;end;
%     
         b1=s11;%dire��o
         %if i==1,if t==121,b1=16;s12=128;end;end;
         b2=s12/4;%espectro
         if i==4,b2=b2*2;end;
         
         if b1>0,
            %ajuste da dire��o
            b1=b1+3;
            if b1>18,b1=b1-18;
            end;
            b1=b1+1;%o "zero" come�a em 1
            n1=tt1+9+10;%shift na escala vertical

            %por faixa: 1m de Hs na faixa=5 divis�es
            if t==1,if i==1,if k==1,b2=30;b1=11;end;end;end
            %b2=4*sqrt(b2*df);b2=2.5*b2^2;b2=b2*4;
            %b2=b2*10;
            %if i==5,b2=2*b2;end;
            %v7=linspace(b1-bb(i),b1+bb(i),length(v61));v7=v7';
            v7=b1-0.55:0.00858:b1+0.55;v7=v7';
             
            x=[v7;flipud(v7)];  


            y=[(n1+v6*b2);n1*ones(length(v6),1)];

            %y=[(n1+v61*b2);n1*ones(length(v61),1)];


            z1=1;z2=1;


            if b2*b1>0,

                patch(x,y,arq,'edgecolor',[0.5 0.5 0.5],'linewidth',0.6);
            end;
      
            %if zz==1,text(b1-0.1,258,'+','color','g');

            %if t==247,sf11;end
        end
    end;
end;

tt1=121;
%plotagem do vento
for t=dp2*8:-1:(dp1-1)*8+1,tt1=tt1-1;
    s1=www50(1,t);
    s2=ventodir(t);
    if s1>0,
        %  if ano==94,if mes==7,
        %    s2=s2+180;end;end;%caso de julho de 1994;
        s2=s2/20;st=tt1+9+10;
        s2=s2+3;if s2>18,s2=s2-18;
        end;
        s2=s2+1;
        %    %calibra�ao 20 m/s=10 divisoes:
        if t==59,s1=10;s2=12;end;
        arq=[1 1 1];
        %a cor � branca entre 0 e 10m/s
        %e os tons de verde ficam mais fortes
        if s1>=10,arq=[0.9 1 0];
        end;
        if s1>=15,arq=[0.5 1 0];
        end;
        if s1>=20,arq=[0 1 0.7];
        end;
        s1=s1/1.25;
        if s1<2,s1=2;end;
         
        %s1 � a velocidade do vento, colocada na escala certa
        %1 divis�o=2m/s
        %s2 � a dire��o em caixas de 18 graus
        % st � a posi��o de plotagem ao logo da vertical%


        x=[s2-0.065;s2+0.065;s2+0.065;s2-0.065];
        y=[st;st;st+s1;st+s1];
        if s2<2,x=NaN;y=NaN;end;
        if s2>18,x=NaN;y=NaN;end;



        if s1>0,
            patch(x,y,arq);
        end;
    end;
end;
% cd('/home/izabel/Bacia_Campos/dados/figuras')
% saveas(f2,'figura.eps')

