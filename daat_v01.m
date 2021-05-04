% DAAT

close all;clear all;clc

load lyg2.mat;

pathname = '/home/hp/Dropbox/doutorado/dados/HNE_rio_grande_200912/';
titulo_pleds = 'DIRECTIONAL WAVE SPECTRUM (DAAT/PLEDS) - Rio Grande/RS - 2009/05';
figname = 'pleds_rio_grande_200905';

param_rig = dlmread('/home/hp/Dropbox/doutorado/dados/param_rig_201912.csv', ',', 1, 1);
ws = param_rig(:, 4);
wd = param_rig(:, 5);

% datet = [294+730*10-5,294+731*11-3]; %2017-10

a = dir([pathname,'*.HNE']);

% declinacao magnetica
dmag = -23;

% frequencia de amostragem
fs = 1.28;
dt = 1/fs;

% numero de pontos na fft (indica o graus de liberdade)
nfft = 165;

if1 = 7:12;
if2 = 12:17;
if3 = 18:33;
if4 = 34:65;

%preparo dos arquivos
dire=zeros(10,744);%direcao (2 valores, at�  5 faixas)
espe=zeros(10,744);%espectros(2 valores, at� 5 faixas)
energ=zeros(10,744);%Hs + 4 energias (uma por faixa), 4 picos (maiores)

% table of sines and cosines for the mem method - tecnica de maxima entropia
a26=[a23(311:360) a23 a23(1:50)];
a27=[a24(311:360) a24 a24(1:50)];
a30=[(311:360) (1:360) (1:50)];
grad1=0.0175;
% grad2=180/pi;

%par o caso de usar matr1 (matriz de ocorr�ncias)
% sa=[.5;.5;.5;.5;0.1];

% mm = [70,43,40,38,37,35,33,32,31,30,29,27,26,25,24,23,22,21,20,19,18,17,16,15,9];
mm = [70:-1:8];
ms=[];
wavecos=zeros(60,length(mm));
wavesen=wavecos;
for i=1:length(mm)
    mn=mm(i);
    ms=[ms;mn];
    out2=linspace(-3.14,3.14,mn);
    gau=hanning(mn);
    out1 =gau'.* cos(3*out2);
    out3 =gau'.* sin(3*out2);
    wavecos((1:mn)',i)=out1';
    wavesen((1:mn)',i)=out3';
end

for ik=1:length(a)
    disp (a(ik).name)

    hne = dlmread([pathname, char(a(ik).name)], '', 11, 0);
    co=hne(:,2); 
    dc=hne(:,4); 
    dd=hne(:,3); 

    [qq1 f1]=pwelch(co, hanning(nfft), round(nfft/2), nfft, fs);
    df = f1(3) - f1(2);

    ww55=zeros(10,1);
    ww55(1)=4*sqrt(sum(qq1)*df);
    ww55(2)=qq1(if1(1)-1)/2+sum(qq1(if1))+qq1(if1(end)+1)/2;
    ww55(3)=qq1(if2(1)-1)/2+sum(qq1(if2))+qq1(if2(end)+1)/2;
    ww55(4)=qq1(if3(1)-1)/2+sum(qq1(if3))+qq1(if3(end)+1)/2;
    ww55(5)=qq1(if4(1)-1)/2+sum(qq1(if4))+qq1(if4(end)+1)/2;

    %picos1 eh o valor do periodo que corresponde
    %a wavelet que sera usada
    %quando nao ha pico na faixa:
    % 43 = 14.3 s;
    % 29 = 9.52 s;
    % 23 = 7.69s;
    % 15 = 5s;
    % 9 = 3s;
    % picos1 = [43; 29; 23; 15; 9];
    % picos1 = [43; 29; 23; 15; 9];
    % picos1 = [48; 24; 14; 8];
    picos1 = [51; 30; 18; 9];

    %alisa-se mais o espectro para calcular os picos
    qq2=smooth(qq1,8);
    
    g1=diff(qq2);
    g1=sign(g1);
    g1=diff(g1);
    g1=[0;g1];
    g1=find(g1==-2);

    %serao calculados os 4 maiores picos
    [g4 g5]=sort(qq2(g1));
    g6=flipud(g1(g5));
    g6=g6(g6>10);      

    %colocacao dos picos nas faixas para determina��o das
    %wavelets
    g7=find(g6>9);g8=find(g6(g7)<19);g10=g6(g7(g8));
    isempty(g10);if ans==0,
        picos1(1)=round(3*(1./f1(g10(1))));end

    g7=find(g6>18);g8=find(g6(g7)<24);g10=g6(g7(g8));
    isempty(g10);if ans==0,
        picos1(2)=round(3*(1./f1(g10(1))));end

    g7=find(g6>23);g8=find(g6(g7)<28);g10=g6(g7(g8));
    isempty(g10);if ans==0,
        picos1(3)=round(3*(1./f1(g10(1))));end

    g7=find(g6>27);g8=find(g6(g7)<51);g10=g6(g7(g8));
    isempty(g10);if ans==0,
        picos1(4)=round(3*(1./f1(g10(1))));end

    % disp(picos1)

    %valores dos picos para o arquivo final
    g5=flipud(g5);g5=g1(g5);
    g5=[g5;0;0;0;0];g5=g5(1:4);
    g=find(g5>0);g5(g)=200./g5(g);

    %preparo final do energ
    ww55(7:10)=g5;

    % energ(:,kkl)=ww55;
    energ(:,ik)=ww55;

    %serao calculadas 5 faixas com wavelets
    %para cada wavelet calcula-se uma matriz de dire��o e desvio
    %padrao obtendo-se um D(teta) para cada faixa

    for iwq=1:length(picos1),

        g11=find(picos1(iwq)==mm);

        m=mm(g11(1));
        out1=wavecos((1:m)',g11(1));
        out3=wavesen((1:m)',g11(1));

        % matr1=ones(20,90);

        m1=1200-m;

        %parametros para calculo de tet2 e sp2
        m3=m1;
        m1=m1-1;
        m3=m1;
        m4=2*dt/(m*0.375);
        m2=m-1;

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        %CODE daatwaverider21w calculates the main direction
        %for each segment with wavelet (morlet type);
        %the formulatuio of Lygre and Krogstad is used

        %usa-se a convolu��o com a wavelet complexa
        a1=filter((out1-1i*out3)',1,co);
        a2=filter((out1-1i*out3)',1,dd);
        a3=filter((out1-1i*out3)',1,dc);

        m4=2*dt/(m*0.375);
        a1=a1(m:1200); %1024
        a2=a2(m:1200);
        a3=a3(m:1200);

        %espectros cruzados
        z41=a1;
        z42=a2;
        z43=a3;
        
        a4=m4*(z41.*conj(z41));
        a8=m4*imag(z41.*conj(z42));
        a9=m4*imag(z41.*conj(z43));

        a20=m4*(z42.*conj(z42));
        a21=m4*(z43.*conj(z43));

        a25=a20+a21;
        a7=sqrt(a4.*a25);

        a12=m4*real(z42.*conj(z43));


        %a8 � o coseno, proje��o no eixo W-E;
        %a9 � seno proje��o no eixo S-N;
        % o �ngulo c0 calculado � em rela��o ao eixo horizontal

        c0=a8+j*a9;


        c1=c0./a7;

        c01=cos(c0);c02=sin(c0);           % Novos Parente
        c03=angle(mean(c01)+j*mean(c02));  %
        c03=ceil(c03*360/(2*pi));          %  

        c2=(a20-a21+1i*2*a12)./a25;

        c0=angle(c0)*360/(2*pi);
        c0=ceil(c0);

        c00=find(c0<=0);c0(c00)=c0(c00)+360;
        pq=ceil(mean(c0));                 % Novos Parente 
        pq=c03;                            %
        g=find(pq<=0);pq(g)=pq(g)+360;     %

        p1=(c1-c2.*conj(c1))./(1-(abs(c1)).^2);
        p2=c2-c1.*p1;

        tet2=zeros(1,m3+2);

        %in order to avoid the ambiguity caused by 2teta the main 
        %direction calculated by Fourier techniques is used 
        %as a reference;
        % the mem value is calculated in an interval
        %of 100 degrees around this value;

        %c�lculation for each segment
        for kl=1:m3+2,
           p3=ceil(c0(kl));
           %p3=31;   
           d=(p3:p3+100);

           z1=1-p1(kl)*a26(d)-p2(kl)*a27(d);
           z1=z1.*conj(z1);
           z1=z1';

           %m�nimum of denominator is sufficient to
           %determine the maximum
             
           p5=find(z1==min(z1));
           p5=p5(1);
           p7=a30(p3+p5-1);
           %main direction (mem) for each segment
           tet2(1,kl)=grad1*p7;
           %z1=1./z1;z1=z1/max(z1);
           %if iwq==5,memarq(d',kl)=z1;arqc0(kl)=c0(kl);end;
        end;

        %spectrum for each segment
        sp2=a4';

        % sp5=sp2/max(sp2);
        % tet6=90+tet2*180/pi-21;
        % %tet6=tet6(sp5>0.5);
        % sp5=sp2/max(sp2);
        % g=find(tet6<=0);
        % tet6(g)=tet6(g)+360;
        % g=find(tet6>360);
        % tet6(g)=tet6(g)-360;
        % 
        % [n1 n2]=hist(tet6,10);
        % g=find(n1==max(n1));
        % dire(iwq,kkl)=n2(g(1));
        % espe(iwq,kkl)=ww55(iwq+1);

        % teste14;
        % g=find(x1==max(x1));

        % %tet2=c0*grad1;
        % 
        % y=zeros(360,1530);
        % y(1:50,:)=memarq(411:460,:);
        % y(1:360,:)=y(1:360,:)+memarq(51:410,:);
        % y(311:360,:)=y(311:360,:)+memarq(1:50,:);
        % 
        % xz=y(:,1);
        % for k=2:length(y),
        %    xz=xz.*(y(:,k)+ones(360,1));end;
        % g=find(xz==max(xz));g=g(1);


        %  x=sum(memarq');x=x';
        %  y=zeros(360,1);
        %  y(1:50)=x(411:460);
        %  y(1:360)=y(1:360)+x(51:410);
        %  y(311:360)=y(311:360)+x(1:50);
        %  memy(:,kkl)=y; 
        %  v6=find(y==max(y));v6=v6(1);
        %  v6=90+v6-21;
        %  if v6>200,v6=v6-360;end;
        %  dire(5,kkl)=v6;

        %[n1 n2]=butter(6,0.051);
        % sp3=sp2/max(sp2);  
        %g=find(tet4>360);tet4(g)=tet4(g)-360;
        %[n1 n2]=hist(tet2,20);
        % %   g=find(n1==max(n1));g=g(1);
        % %if iwq>1,  
        %   %  c0=c0*2*pi/360;

        %  v3=mean(cos(tet2));v4=mean(sin(tet2)); 
        %  v5=angle(v3+j*v4);
        %  v5=v5*360/(2*pi); % 
        %  v5=90+v5-21;
        %  if v5<0,v5=v5+360;end
        %  dire(iwq,kkl)=v5;
        %  espe(iwq,kkl)=ww55(iwq+1); 

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        % dire1(iwq,kkl)=mean(tet2*180/pi);

        %CODE daatbcampos22.m to select the segments for
        %the directional spectrum composition
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %Prepared by C.E. Parente
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        it=2*(iwq-1)+1;

        q1=cos(tet2);
        q2=sin(tet2);

        %Preparing ensembles of m segments advancing one sample

        %fr3 ia a matrix of cos and fr5 of sines of the segments whose direction
        %stability will be investigated
        %fr4 is the spectrum matrix

        pm=length(round(m/2):m1-(m-round(m/2)));
        fr3=zeros(round(m/2),pm);
        fr5=fr3;
        fr4=fr3;

        for ip=1:round(m/2),
           fr3(ip,:)=q1(ip:m1-(m-ip));
           fr5(ip,:)=q2(ip:m1-(m-ip));
           fr4(ip,:)=sp2(ip:m1-(m-ip));
        end;

        %using the mean and the standard circular deviation
        %to select the segments with a given stability
        fr2a=mean(fr3);
        fr2b=mean(fr5);
        r=sqrt(fr2a.^2+fr2b.^2);

        %circular deviation
        fr9=sqrt(2*(1-r));

        %fr99=fr9;fr2aa=fr2a;fr3a=fr3;q1a=q1;tet2a=tet2;

        %espectro medio por coluna
        fr45=mean(fr4);
        fr2=angle(fr2a+1i*fr2b);
        g=find(fr2<0);fr2(g)=fr2(g)+2*pi;
        g=find(fr2>2*pi);fr2(g)=fr2(g)-2*pi;
        g=size(fr2);g=g(2);

        a15=0;
        zm=0.5;
        %segments with values of the standard deviations smaller
        %than the threshold are selected
        er5=mean(fr4);

        b7=find(fr9<zm);
        %selected directions(segments)
        a15=fr2(b7);

        %selected spectrum vales
        er4=mean(fr4(:,b7));

        %Correcting for declination
        % a15 is the the final vector with selected direction values
        a15=ceil(a15*360/(2*pi));
        %a15=90+a15-14;(waverider de Santa Catarina)
        %a15=90+a15-21;%(waverider de Arraial)
        % BOIA ES dmag -23

        % correcao do azimute 
        % a15 = 270 - a15 + dmag;
        a15 = a15 -180 + dmag;

        g=find(a15<0);
        a15(g)=a15(g)+360;
        g=find(a15>360);
        a15(g)=a15(g)-360;

        %caixas para ac�mulo e obten��o de D(teta)
        w1=zeros(360,1);%dire��o principal
        w2=zeros(360,1);%ocorr�ncias
        a16=a15;
        %w4=w2;%dire��o sem overlapping
        %w2a=w2;%ocorrencias sem    overlapping

        if length(a15)>1,%caso existam valores selecionados
            b1=find(a15<=0);a15(b1)=a15(b1)+360;
            b1=find(a15<=0);a15(b1)=a15(b1)+360;
            b1=find(a15>360);a15(b1)=a15(b1)-360;
            b1=find(a15>360);a15(b1)=a15(b1)-360;

            %algoritmo para reduzir overlapping para
            %c�lculo de spread
            %   [p1 p2]=sort(er4');p1=flipud(p1);
            %   p2=flipud(p2);

            %      maxdir=[p2(1)];
            %   for i=2:length(p2),
            %      q=p2(i);
            %      q1=abs(maxdir-p2(i));
            %      g=find(q1<(m/2));
            %      isempty(g);
            %      if ans==1,
            %         maxdir=[maxdir;p2(i)];
            %      end;
            %   end

            %dire��o e espectro sem overlapping
            %  a16=a15(maxdir);
            %  er5=er4(maxdir);
            a15=round(a15);
            %storing spectrum values in 1 degree boxes;
            for k=1:length(a15),
                bb=a15(k);
                w1(bb)=w1(bb)+sp2(k);
                w2(bb)=w2(bb)+1;
            end
        end


        %filtrando w1 para determinar D(teta)

        [b,t1]=butter(6,0.075);
        xx=[w1(321:360);w1;w1(1:40)];

        x=filtfilt(b,t1,xx);
        x=x(41:400);
        g=find(x<0);
        x(g)=0;

        %calculando 2 direcoes
        g1=diff(x);
        g1=sign(g1);
        g1=diff(g1);
        g1=[0;g1];
        g1=find(g1==-2);

        [p1 p2]=sort(x(g1));
        isempty(p1);
        if ans==0,
            p=[flipud(g1(p2));0];
            p=p(1:2);
            e=[flipud(p1);0];
            e=e(1:2);
        end

        %jogo fora valores espacados de menos de 50 graaus
        if abs(p(1)-p(2))<20,
            e(2)=0;
            p(2)=0;
        else
            %ou pequenos
            if e(2)<0.1*e(1)
                e(2)=0;p(2)=0;
            end
        end

        %normalizacao com as energias das faixas obtidas do espectro 1D
        z1=ww55(iwq+1);
        p=[p;0;0;0];
        p=p(1:2);
        e=[e;0;0;0];e=e(1:2);
        e=e*z1/sum(e);
        dire(it:it+1,ik)=p;
        espe(it:it+1,ik)=e;

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    end
end


% filtragem da daat
% onda
ik1 = 0;
for ik=1:10
    ik1=ik1+1;
    [b a]=butter(4,0.03);
    y=dire(ik,:);
    y=y*2*pi/360;
    y=unwrap(y);
    w1=y*360/(2*pi);
    y1=cos(y);y2=sin(y);
    w=zeros(1,length(dire));
    for i=5:length(dire)-5,
        g1=mean(y1(i-4:i+4));
        g2=mean(y2(i-4:i+4));
        g3=angle(g1+j*g2);g3=g3*360/(2*pi);
        if g3<0
            g3=g3+360;
        end;
        if g3>=360,
            g3=g3-360;
        end;
        w(i)=g3;
    end;
    g=find(w>360);
    w(g)=w(g)-360;
    g=find(w>360);
    w(g)=w(g)-360;
    g=find(w<0);
    w(g)=w(g)+360;
    dire(ik1,1:length(w))=w;
end

% vento
[b a]=butter(4,0.03);
y=wd
y=y*2*pi/360;
y=unwrap(y);
w1=y*360/(2*pi);
y1=cos(y);
y2=sin(y);
w=zeros(1,length(wd));
for i=5:length(wd)-5,
    g1=mean(y1(i-4:i+4));
    g2=mean(y2(i-4:i+4));
    g3=angle(g1+j*g2);
    g3=g3*360/(2*pi);
    if g3<0
        g3=g3+360;
    end;
    if g3>=360,
        g3=g3-360;
    end;
    w(i)=g3;
end;
g=find(w>360);
w(g)=w(g)-360;
g=find(w>360);
w(g)=w(g)-360;
g=find(w<0);
w(g)=w(g)+360;
wd(1:length(w))=w;

espe1 = espe;
dire1 = dire;

ws1 = ws(1:3:end);
wd1 = wd(1:3:end);
wd1(end) = wd1(end-1)

pleds

% dlmwrite('dados/espemat_pnboia_fortaleza.txt', espe)
% dlmwrite('dados/diremat_pnboia_fortaleza.txt', dire)

% dire1 = dire(:,1:3:end); 
% espe1 = espe(:,1:3:end); 
% energ1 = energ(:,1:3:end);
% ws1 = ws(1:3:744);
% wd1 = wd(1:3:744);

% filtrapleds
% dire1 = ddir;
% wd1 = wd2;

% dlmwrite('dados/espemat_pnboia_fortaleza.txt', espe)
% dlmwrite('dados/diremat_pnboia_fortaleza.txt', dire)

