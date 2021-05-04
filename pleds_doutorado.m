% Programa para plotagem da evolucaoo do espectro direcional
% Boia Rio Grande do Sul - Junho de 2009

% ======================================================== #
% carrega dados ja rodados (espe e dire)

% param = readtable('/home/hp/Documents/pnboia/dados/fortaleza/pnboia_fortaleza.csv', 'HeaderLines', 0);

datet = [294+730*10-5,294+731*11-3]; %periodo: 2017-10

% ws = param.Wspd(datet(1):datet(2));
% wd = param.Wdir(datet(1):datet(2));

% espe = load('dados/espepy_pnboia_fortaleza.txt');
% dire = load('dados/direpy_pnboia_fortaleza.txt');


% reamostra para 3 horas (verificar se necessario)

% ws1 = ws(1:3:end);
% wd1 = wd(1:3:end);

% filtra onda e vento
% filtrapleds

% dire1 = ddir;
% wd1 = wd2;

% salva dados filtrados
% dlmwrite('dados/espe1py_pnboia_fortaleza_filtrado.txt', espe1)
% dlmwrite('dados/dire1py_pnboia_fortaleza_filtrado.txt', dire1)
% dlmwrite('dados/ws1.txt', ws1)
% dlmwrite('dados/wd1.txt', wd1)

% ======================================================== #

figure1=figure;

clf reset
% close all

%arquivo de m�s
ad=['Jan';'Feb';'Mar';'Apr';'May';'Jun';'Jul';'Aug';'Sep';'Oct'];
ad=[ad;'Nov';'Dec'];
a=0;plot(a,'w');
c=[0 22.1 0 300];axis(c);
v6=hanning(15);v61=hanning(11);
ad1=[31;29;31;30;31;30;31;31;30;31;30;31];
axis('off')
%df=f(2)-f(1);
arq2=[[1 0 0];[1 0 0];[1 0.55 0];[1 0.55 0];[1 1 0];...
      [1  1 0];[0 1 0];[0 1 0]];

arq2=[[1 0 0];[1 0.55 0];[1 1 0];[0 1 0]];


col=[0.7 0.7 0.7];
%text(1.5,14,'direcao verdadeira em graus - onda e vento','fontsize',16,'color','b');

set(gcf,'paperposition',[-0.5 -0.5 9.5 10.5]);
%codigo de cores para faixas de periodos
x=[0.5;3.4;3.4;0.5]+0.5;y=[1;1;12;12]-3.5;
patch(x,y,arq2(1,:));
x=x+2.9;patch(x,y,arq2(2,:));
x=x+2.9;patch(x,y,arq2(3,:));
x=x+2.9;patch(x,y,arq2(4,:));
%x=x+1.30;patch(x,y,arq2(9,:));
x=x+2.9;patch(x,y,[1 1 1]);
x=x+2.9;patch(x,y,[1 1 1]);
%y=y+16;patch(x,y,[1 1 1]);
%y=y+16;patch(x,y,[1 1 1]);
%y=y+16;patch(x,y,[1 1 1]);

%ad(mes,:) '/' num2str(ano)]); 


% k1=[];
k1=[
    '18.4 a 12.8';...
    '11.7 a 8.00';...
    '7.50 a 4.20';...
    '4.00 a 2.00';...
    '5 div=10m/s';...
    '5 div=0.1m2'
    ];

text(1.3,4,k1(1,:),'fontsize',14,'fontweight','bold','color','k');
text(4.2,4,k1(2,:),'fontsize',14,'fontweight','bold','color','k');
text(7.1,4,k1(3,:),'fontsize',14,'fontweight','bold','color','k');
text(10,4,k1(4,:),'fontsize',14,'fontweight','bold','color','k');
text(12.8,4,k1(5,:),'fontsize',14,'fontweight','bold','color','k');
text(15.7,4,k1(6,:),'fontsize',14,'fontweight','bold','color','k');

% k=-1.3;
% %faixas de periodos;
% for i=1:6,k=k+2.7;
%     text(k,4,k1(i,:),'fontsize',14,'fontweight','bold','color','k');
% end

%text(15.9,11.5,'Ventos','fontsize',12,'color','k')
%text(16.2,6.6,'Ondas(Hs por faixa)','fontsize',12,'color','k')
text(3.83,-2.9,'Range of wave period (seconds)','fontsize',14,'color','k')
text(14,-2.9,'Wind/Wave scale','fontsize',14,'color','k')
%text(7.75,2,'10 divis�es=20 m/s','fontsize',10,'color','k')
%text(0.2,10,'dia do m�s','fontsize',8,'color','k','rotation',90)

% if (mes==10);
%     %linhas verticais;
%     y=[20;(20-1)*8+20+25];
%     for i=1:1:19,
%       x=[i;i];line(x,y,'color',col,'linewidth',[0.2]);
%     end

%     %linhas horizontais com "tick";
%     x=[0.9;19.1];
%     for i=20:8:(20-1)*8+20,
%       y=[i;i];line(x,y,'color',col,'linewidth',[0.4]);
%     end

%     x=[0.5;19.5];
%     line(x,y,'color','k','linewidth',[0.6]);

%     %linhas horizontais
%     x=[1;19];
%     for i=20:2:(20-1)*8+20+7+20,
%        y=[i;i];line(x,y,'color',col);
%     end

%     %dias do mês de 1 a 9, eixo vertical
%     a=2.9+10;
%     %dias do mês, eixo vertical de 10 a 31;
%     for i=12:31,a=a+8;
%       text(.47,a,num2str(i),'fontsize',14,'fontweight','b');
%       text(19.15,a,num2str(i),'fontsize',14,'fontweight','b');
%     end;    
%     text(1,205,['DIRECTIONAL WAVE SPECTRUM (32g) - RS - ' ad(mes,:) '/' num2str(ano)],...
%     'fontsize',18,'color','b')
% else

%linhas verticais;
y=[20;(32-1)*8+20+15];
for i=1:1:19,
  x=[i;i];line(x,y,'color',col,'linewidth',[0.2]);
end

%linhas horizontais com "tick";
x=[0.9;19.1];
for i=20:8:(32-1)*8+15,
  y=[i;i];line(x,y,'color',col,'linewidth',[0.4]);
end

x=[0.5;19.5];
line(x,y,'color','k','linewidth',[0.6]);

%linhas horizontais
x=[1;19];
for i=20:2:(31-1)*8+20+7+15,
   y=[i;i];line(x,y,'color',col);
end

%dias do mês de 1 a 9, eixo vertical
a=2.9+10;
for i=1:9,a=a+8;
  text(.63,a,num2str(i),'fontsize',14,'fontweight','b');
  text(19.15,a,num2str(i),'fontsize',14,'fontweight','b');
end;

%dias do mês, eixo vertical de 10 a 31;
for i=10:31,a=a+8;
  text(.47,a,num2str(i),'fontsize',14,'fontweight','b');
  text(19.15,a,num2str(i),'fontsize',14,'fontweight','b');
end;
text(1,290,['DIRECTIONAL WAVE SPECTRUM (DAAT/PLEDS) - Rio Grande/RS - 2009/12'], 'fontsize',18,'color','b')

% end

%cores das diferentes faixas de per�odos

%plotagem do espectro direcional a cada dia por faixa de per�odos
%plota de cima para baixo (de 31 para 1)

%eixo horizontal de dire��o
a=310:20:720;a=a';
a1=find(a>360);a(a1)=a(a1)-360;
for i=1:18,
  text(i+0.15,16,num2str(a(i)),'fontsize',16,'color','r','fontweight','bold');
end;
ld=['NW';'N ';'NE';'E ';'SE';'S ';'SW';'W ';'SW';'W '];
k=1.55;
d=1.75:2.25:13;
 for i=1:8,
   text(k,20.8,ld(i,:),'fontsize',18,'color','k','fontweight','bold');
   k=k+2.25;
 end;
text(1.15,40,'day of month','fontsize',14,'rotation',90); % ??dire1(3,:)=dire1(7,:);
w=[[1;6] [2;7] [3;8] [4;9]];
bb=[0.3;0.3;0.3;0.3;0.3;0.3;0.3;0.3;0.3;0.3];

for t=248:-1:1, %era ateh 1

    s1=dire1(t,:);
    s2=espe1(t,:);

    % teste
    % s1=[180,nan,120,nan,20,nan,90,nan]; % direcao
    % s2=[1,nan,3,nan,5,nan,7,nan];        % espectro

    %s1=reshape(s1,2,5);
    %s2=reshape(s2,2,5);
    %plotagem por faixa

    % plotagem de cada faixa
    for i=[1,2,3,4],

        arq5=arq2(i,:);%cor

        %s11=s1(:,i);
        %s12=s2(:,i);
        
        %w1=w(k,i);
        s11=s1(i); % direcao
        s12=s2(i); % espectro
        
        b1=s11/20; %direcao
        b2=s12/2; %espectro

        if b1>0,
            %ajuste da dire��o
            b1=b1+3;
            if b1>18
                b1=b1-18;
            end

            b1=b1+1;%o "zero" come�a em 111
            n1=t+9+10;%shift na escala vertical

            %por 11: 1m de Hs na faixa=5 divis�es
            %if t==151,if i==1,if k==1,b2=128;b1=11;end;end;end
            %b2=4*sqrt(b2*df);b2=b2*5;
            
            b2=2*b2;
            b2=b2/2;

            % ???            
            % if t==1
            %     b2=10;
            %     b1=10;
            %     arq=arq2(3,:);
            % end;

            %if i==5,b2=2*b2;end;
            v7=linspace(b1-bb(i),b1+bb(i),length(v61));
            v7=v7';
            %v7=b1-0.55:0.075:b1+0.55;v7=v7';

            x=[v7;flipud(v7)];

            y=[(n1+v61*b2);n1*ones(length(v61),1)];

            z1=1;
            z2=1;

            %if b2<100*0.4*energ(i+1,t),b2=0;end;
            
            if b2.*b1>0
                patch(x,y,arq5)
            end
        end
        %if zz==1,text(b1-0.1,258,'+','color','g');
    end
end

%plotagem do vento
for t=248:-1:1,
    s1=ws1(t);
    s2=wd1(t);
    if s1>0,
        %  if ano==94,if mes==7,
        %    s2=s2+180;end;end;%caso de julho de 1994;
        s2=s2/20;st=t+9+10;
        s2=s2+3;
        if s2>18,s2=s2-18;end;
        s2=s2+1;
        %    %calibra�ao 20 m/s=10 divisoes:
        %if t==201,s1=20;s2=12;end;
        arq=[1 1 1];
        %a cor � branca entre 0 e 10m/s
        %e os tons de verde ficam mais fortes
        if s1>=10,arq=[0.9 1 0];
        end;
        if s1>=15,arq=[0.5 1 0];
        end;
        if s1>=20,arq=[0 1 0.7];
        end;
        if s1<2,s1=2;end;
        %s1 � a velocidade do vento, colocada na escala certa
        %1 divis�o=2m/s
        %s2 � a dire��o em caixas de 18 graus
        % st � a posi��o de plotagem ao logo da vertical%
        x=[s2-0.05;s2+0.05;s2+0.05;s2-0.05];
        y=[st;st;st+s1;st+s1];
        if s2<2,x=NaN;y=NaN;end;
        if s2>18,x=NaN;y=NaN;end;
        if s1>0,
           patch(x,y,arq);
        end;
    end;
end;


set(gcf,'paperOrientation','portrait','paperposition',[1 1 15 15],...
     'paperSize',[15 15]);

% eval(['print(figure1,''-dpcx256'',''pleds_lioc',''')'])

saveas(gcf, 'pledsmat_rio_grande_200912', 'png')


