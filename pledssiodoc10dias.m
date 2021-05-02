%programa para plotagem da evolução do espectro direcional
%para sensor gx3
%dados gx3 (dire e espe), mes e ano.
figure(2);
clf reset
ano=2014;mes=10;   
%local=input('stationname = ');
%mes = input('mes = ');
%ano= input ('ano = ');
%plotagem inicial e definição de eixos e outros parâmetros;
a=0;plot(a,'w');
c=[0 22.1 0 278];axis(c);
v6=hanning(15);v61=hanning(11);
ad1=[31;29;31;30;31;30;31;31;30;31;30;31];
axis('off'  )
%df=f(2)-f(1);
col=[0.5 0.5 0.5];
%linhas verticais;
y=[20;(32-1)*8+20];
for i=1:1:19,
    x=[i;i];line(x,y,'color',col,'linewidth',[0.2]);
end
%x=[22;22];line(x,y,'color',col,'linewidth',[0.2]);
%linhas horizontais com "tick";
%x=[0.9;22.1];
x=[0.9;19.1];
for i=20:8:(32-1)*8+20,
    y=[i;i];
    line(x,y,'color',col);
end

%linhas horizontais
x=[1;19];
for i=20:2:(32-1)*8+20,
    y=[i;i];
    line(x,y,'color',col);
end

%dias do mês de 1 a 9, eixo vertical
a=2.9+10;a=a-15;
for i=1:9,a=a+24;
    text(.73,a,num2str(i),'fontsize',8);
    %%text(22.1,a,num2str(i),'fontsize',7);
    text(19.1,a,num2str(i),'fontsize',8);
end;

%dias do mês, eixo vertical de 10 a 31;
for i=10:10,a=a+24;
    text(.57,a,num2str(i),'fontsize',8);
    %%text(22.1,a,num2str(i),'fontsize',10);
    text(19.1,a,num2str(i),'fontsize',8);
end;

%arquivo de mês
ad=['jan';'fev';'mar';'abr';'mai';'jun';'jul';'ago';'set';'out'];
ad=[ad;'nov';'dez'];

%cores das diferentes faixas de períodos
arq3=[[1 0 0];
    [1 1 0];
    [0 1 0];
    [0.3 0.7 1]];
% arq3=[[0.1 0.1 0.1];
%     [0.4 0.4 0.4];
%     [0.7 0.7 0.7];
%     [0.98 0.98 0.98]];

%plotagem do espectro direcional a cada dia por faixa de períodos
%plota de cima para baixo (de 31 para 1)

%eixo horizontal de direção
a=310:20:720;a=a';
a1=find(a>360);a(a1)=a(a1)-360;
for i=1:18,
    text(i+0.15,16,num2str(a(i)),'fontsize',10,'color','k')
    %,'fontweight','bold');
end;
ld=['NW';'N ';'NE';'E ';'SE';'S ';'SW';'W ';'SW';'W '];
k=1.55;
for i=1:8,
    text(k,22.5,ld(i,:),'fontsize',12,'color','r');
    k=k+2.25;
end;

text(1.0,7.5,'wave and wind (   )direction','fontsize',11,'color','k');
%text(0.17,40,['records every 3 hours-initial day=' num2str(dp1)],'fontsize',11,'rotation',90);
%text(1.3,2.3,'wind','fontsize',11,'color','k');
x=[3.85;3.97;3.97;3.85];y=[4;4;13;13];z=[1 1 1];
patch(x,y,z);
%codigo de cores para faixas de periodos
x=[1;3;3;1]+5.;y=[4;4;10;10];
patch(x,y,arq3(1,:));
x=x+2;patch(x,y,arq3(2,:));
x=x+2;patch(x,y,arq3(3,:));
x=x+2;patch(x,y,arq3(4,:));

k1=[];
k1=['20.0 a 10.2';...
    '10.2 a 7.75';...
    '7.75 a 3.93';...
    '3.93 a 2.50';];

k=4.05;
%faixas de periodos;
for i=1:4,k=k+2;
    text(k+0.15,-2.,k1(i,:),'fontsize',9,'fontweight','bold');
end;
text(14.2,7.5,'period band in seconds','fontsize',11,'color','k');

text(1,276,['ESPECTRO DIRECIONAL DE ONDAS' ' - ' 'C.FRIO - SIODOC '...
    ad(mes,:) '/' num2str(ano)],'fontsize',13,'color','b','fontweight','bold');

% text(1,12,'Escala vertical(onda)','fontsize',10,'color','k')
% text(1,7,'  Hs2 por faixa:','fontsize',10,'color','k')
% text(1,2,'25 div.=16m2=4m(Hs)','fontsize',9,'color','k')
% text(15.75,12,'Escala vertical(vento)','fontsize',10,'color','k')
% text(15.75,7,'  barras verticais:','fontsize',10,'color','k')
% text(15.75,2,'10 divisões=20 m/s','fontsize',10,'color','k')
% %text(0.2,10,'dia do mês','fontsize',8,'color','k','rotation',90)
%set(gcf,'paperposition',[-2 -2.5 13.5 9.5]);

bb=[0.5;0.5;0.5;0.5;0.5];
dp1=1;
dp=(dp1:dp1+247);dp=dp+dm;dp=dp';
%dr=ddir1(1:4,dp);

dpv=1:248;dpv=dpv+dm;
dr=ddirsiodoc(dp,1:4);dr=dr';
espe1=espesio(dp,1:4);


for t=248:-1:1,
    %arquivo geral do dia
    s1=dr(1:4,t);
    s2=espe1(t,1:4);
    
    %plotagem por faixa
    for i=[ 1 ],
        arq=arq3(i,:);%cor
        %s11=s1(:,i);
        %s12=s2(:,i);
        s11=s1(i);
        
        s12=s2(i);
               
        b1=s11/20;%direção
        b2=s12;%espectro
                
        if b1>0,
            %ajuste da direção
            b1=b1+3;
            if b1>18,b1=b1-18;
            end;
            b1=b1+1;%o "zero" começa em 1
            n1=t+9+10;%shift na escala vertical
            
            %por faixa: 1m de Hs na faixa=5 divisões
            %if t==151,if i==1,if k==1,b2=128;b1=11;end;end;end
            %b2=4*sqrt(b2*df);b2=2.5*b2^2;
            %b2=b2*10;
            xx=sum(energsio(2:5,t));
            if i==4,if b2>0.05*xx,b2=2*b2;else,b2=0;end;end;
            if i==3,b2=b2/2;end
            if i==2,b2=b2/2;end
            if i==1,b2=b2;end;
            v7=linspace(b1-bb(i),b1+bb(i),length(v6));v7=v7';
            %v7=b1-0.55:0.075:b1+0.55;v7=v7';
            
            x=[v7;flipud(v7)];
            
            
            y=[(n1+v6*b2);n1*ones(length(v6),1)];
            
            
            z1=1;z2=1;
            
            
            if b2.*b1>0,
                
              patch(x,y,arq);
            end;
            
            %if zz==1,text(b1-0.1,258,'+','color','g');
            
            
        end
    end;

end

veloc=www50(2,dpv)';
ventodire=ventosiodoc1(dpv)';
%ventodire=out14_wind(dpv,1);
%plotagem do vento
for t=248:-1:1,
    s1=ventodire(t);
    s2=veloc(t);
    if s1>0,
        %  if ano==94,if mes==7,
        %    s2=s2+180;end;end;%caso de julho de 1994;
        s1=s1/20;st=t+9+10;
        s1=s1+3;if s1>18,s1=s1-18;
        end;
        s1=s1+1;
        %calibraçao 20 m/s=10 divisoes:
        %if t==201,s1=20;s2=12;end;
        arq=[1 0 0];
        %a cor é branca entre 0 e 10m/s
        %e os tons de verde ficam mais fortes
        %if s2>=10,arq=[0.9 1 0];
        %end;
        %if s2>=15,arq=[0.5 1 0];
        %end;
        %if s2>=20,arq=[1 0.3 0.3];
        %end;
        
        if s2<2,s2=2;end;
        if s2>30,s2=0;end
        %s1 é a velocidade do vento, colocada na escala certa
        %1 divisão=2m/s
        %s2 é a direção em caixas de 18 graus
        % st é a posição de plotagem ao logo da vertical%
        
        
        x=[s1-0.055;s1+0.055;s1+0.055;s1-0.055];
        y=[st;st;st+s2;st+s2];
        if s1<2,x=NaN;y=NaN;end;
        if s1>18,x=NaN;y=NaN;end;
        
        
        
        if s2>0,
            patch(x,y,arq);
        end;
    end;
end;

 set(gcf,'paperposition',[0 0 11 6]);
