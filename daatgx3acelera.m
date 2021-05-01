%**************************************************************************
% Rotina daatgx3acelera.m para uso da DAAT com series
% de aceleracao + Pitch + roll do sensor gx3
%******************************************************


%possibilidades de entrada de dados:

%arquivos TOA55 de medicoes com as boias
%é melhor preparar os dados fora, com dlmread ou
%importdata e depois carregar com load dadosgx3, por exemplo.

%arquivos iniciais - uma direçaõ e um espectro para cada frequencia
%energ: Hs "de aceleração", energia em 4 faixas + 4 maiores
%periodos de pico

dire=zeros(744,4);%direção
espe=zeros(744,4);%espectros
energ=zeros(9,744);%Hs(?)+4 energias(uma por faixa)+4 maiores picos
picpic=zeros(1,744);
compa15=zeros(744,4);
load out14_V.mat
load out14_EW.mat
load out14_NS.mat
load out14_wind.mat
% 
zco=out14_V; zco=zco';
zdd=out14_NS;zdd=zdd';
zdc=out14_EW;zdc=zdc';

%dados iniciais
df=1/128;dt=1;
%vetor de frequencias
f=df:df:0.5;
w4=(2*pi*f').^4;
fa=1/dt;
% %para o triaxis
% dt1=0.78;s
% f1=1/(256*0.78):1/(256*0.78):128/(256*0.78);%triaxis
% w5=(2*pi*f1').^4;

%preparo de wavelets com 3 ciclos correspondentes a
%periodos de ordem 6 até 64 - correspondem a uma analise
%de 128 pontos com dt=1 segundo - são 59 wavelets.

t1=1./f';t2=round(3*t1);
t2=t2(6:64);
wavecos=zeros(64,59);wavesen=wavecos;
%wavelets do tipo morlet com janela de hanning
%as wavwlwts são calculadas apenas uma vez para toda a campnha
for i=1:59,
    out2=linspace(-3.14,3.14,t2(i));
    gau=hanning(t2(i));
    out1 =gau'.* cos(3*out2);
    out3 =gau'.* sin(3*out2);
    wavecos((1:t2(i))',i)=out1';
    wavesen((1:t2(i))',i)=out3';
end;

%dados auxiliares para a analise de máxima entropia
% table of sines and cosines for the mem method
load lyg2.mat;
a26=[a23(311:360) a23 a23(1:50)];
a27=[a24(311:360) a24 a24(1:50)];
a30=[(311:360) (1:360) (1:50)];
grad1=0.0175;grad2=180/pi;

%carregar arquivos de aceleração, pitch e roll


%de 88 a 744 ou um registro

for kkl=1:744,
    ww55=zeros(9,1);%para o energ
    co=zco(:,kkl);co=co-mean(co);
    dd=zdc(:,kkl);dd=dd-mean(dd);
    dc=zdd(:,kkl);dc=dc-mean(dc);
    if sum(co)*sum(dd)*sum(dc)>0,
    %espectro de aceleração
    %qq1=spectrum(co,128,64);
    %qq1=2*dt*qq1(2:65,1);
    %usando pwelch
    [qq1 F]=pwelch(co,hanning(128),64,128,fa);
    qq1=qq1(2:65,1);
    qq1(1:5)=0;
    %faixas em segundos
    %2     3    4
    %4     6    8
    %8     9    10.66
    %10.66 16   21.33
    
    %onda significativa - valor ficticio pois é de aceleração
    ww55(1)=4*sqrt(sum(qq1)*df);%Hs hipotetico
    %energias nas 4 faixas (relativas a aceleração); em principio
    %para a normalizaçaõ das faixas 2, 3 e 4
    ww55(2)=sum(qq1(6:11))+qq1(12)/2;
    ww55(3)=qq1(12)/2+sum(qq1(13:15))+qq1(16)/2;
    ww55(4)=qq1(16)/2+sum(qq1(17:31))+qq1(32)/2;
    ww55(5)=qq1(32)/2+sum(qq1(33:end));
    
    %caso queira alisar mais o espectro
    qq2=smooth(qq1,6);
    
    %se necessario, espectros dos slopes
    
    %     qq3=spectrum(dd,128,64);qq3=2*qq3(2:65,1);
    %     qq4=spectrum(dc,128,64);qq4=2*qq4(2:65,1);
    %     ss1(kkl)=96.23*(qq3(8)+qq4(8))/w4(8);
    %     ss2(kkl)=qq1(8)/w4(8);
    %     ss(kkl)=ss2(kkl)/ss1(kkl);
    
    
    %cálculo dos picos
    g2=diff(qq2);g2=sign(g2);g2=diff(g2);g2=[0;g2];
    g2=find(g2==-2);
    
    %escolhendo os 4 maiores
    [g4 g5]=sort(qq2(g2));
    g5=flipud(g5);
    
    g5=g2(g5);
    g20=g5;
    g5=[g5;0;0;0;0];g5=g5(1:4);
    g=find(g5<13);isempty(g);if ans==0,picpic(kkl)=g5(g(1));end;
      
    g=find(g5>0);g6=g5(g);
    g5=128./g5(g);
    w55(6:5+length(g5))=g5;
    %os 4 maiores picos (se maiores do que zero)
    %foram colocados em ww55, de forma sequencial.
    
    %picos1 contem os valores (ordem) dos picos do
    %centro das faixas
    picos1=[8;14;21;42];picos2=picos1;
    
    %se em g20 houver picos nas faixas os valores serão
    %colocados em picos1
    
    g7=[13;17;33];
    for i=1:3,
        g=find(g20<g7(i));g11=isempty(g);if g11==0,
            picos1(i)=g20(g(1));g20(g)=80;end
    end;
    
    %arredondando os valores de pico
    ww55(6:9)=round(g5*10)/10;
    
    %kkl é a ordem do registro
    energ(1:9,kkl)=ww55;
    
    %calculo das direções por faixa; a wavelet corrsponde
    %ao pico na faixa (se houver) ou ao centro da faixa,
    %sempre em picos1
    
    for iwq=1:4,
        s=picos1(iwq);
        
         s=s-5;
        s1=wavecos(:,s);g=find(s1)>0;
        out1=wavecos(g,s);
        out3=wavesen(g,s);
        m=length(g);
        m1=1024-m;
        %parâmetros para cálculo de tet2 e sp2
        m3=m1;m1=m1-1;m3=m1;
        m4=2*dt/(m*.375);
        m2=m-1;
        mq=round(m/2);
        daatgx3wavelet
        %testegx34
        
        %na faixa 1 usa-se a tecnica de contour
        %if iwq==1,daatgx3matriz,
        %else;
            daatgx322a;
            %valor maximo do d(teta)
            e=find(x==max(x));
            dire(kkl,iwq)=e(1);
            %energia obtida do espectro de aceleração/w4;
            espe(kkl,iwq)=energ(iwq+1,kkl)/w4(picos1(iwq));
        %end
    end;

end;
end;