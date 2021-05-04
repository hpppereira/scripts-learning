% DAAT Doutorado Henrique Pereira

clear all
clc

% load lyg2.mat;

pathname = '/home/hp/Dropbox/doutorado/dados/HNE_rio_grande_200912/';
% figname = 'pleds_rio_grande_200912';

param = dlmread('/home/hp/Dropbox/doutorado/dados/param_rig_201912.csv', ',', 1, 1);
ws = param(:, 4);
wd = param(:, 5);

% datet = [294+730*10-5,294+731*11-3]; %2017-10

aa = dir([pathname,'*.HNE']);


%possibilidades de entrada de dados:

%arquivos TOA55 de medicoes com as boias
%é melhor preparar os dados fora, com dlmread ou
%importdata e depois carregar com load dadosgx3, por exemplo.

%arquivos iniciais - uma direçaõ e um espectro para cada frequencia
%energ: Hs "de aceleração", energia em 4 faixas + 4 maiores
%periodos de pico
%angulo=zeros(744,4);
dire=zeros(744,4);%direção
espe=zeros(744,4);%espectros
energ=zeros(9,744);%Hs(?)+4 energias(uma por faixa)+4 maiores picos
%picpic=zeros(1,744);
%compa15=zeros(744,4);

% load wind.txt
% load pitch1.txt
% load heave.txt
% load roll1.txt

 % frequencia de amostragem
Fs = 1.28;
dt = 1/Fs;

 % tamanho do segmento para fft
NFFT = 165;

 % declinacao magnetica
dmag = -23;

 % vetor de frequencia
f1 = linspace(0, 0.6363, 83);
f1 = f1(2:end);

df =f1(2) - f1(1);
% dt = 1./df;

% zco=heave;
% zdd=roll1;
% zdc=pitch1;

%dados iniciais
% df=1/128;dt=1;
%vetor de frequencias
% f=df:df:0.5;
w4=(2*pi*f1).^4;
fa=1/dt;

% %para o triaxis
% dt1=0.78;s
% f1=1/(256*0.78):1/(256*0.78):128/(256*0.78);%triaxis
% w5=(2*pi*f1').^4;

%preparo de wavelets com 3 ciclos correspondentes a
%periodos de ordem 6 até 64 - correspondem a uma analise
%de 128 pontos com dt=1 segundo - são 59 wavelets.

t1=1./f1';
t2=round(3*t1);
% t2=t2(2:end);
wavecos=zeros(t2(1), length(f1));
wavesen=wavecos;
%wavelets do tipo morlet com janela de hanning
%as wavwlwts são calculadas apenas uma vez para toda a campnha
for i=1:length(t2),
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
    disp (aa(kkl).name)

    ww55=zeros(9,1);%para o energ


    % co=zco(:,kkl);co=co-mean(co);
    % dd=zdd(:,kkl);dd=dd-mean(dd);
    % dc=zdc(:,kkl);dc=dc-mean(dc);
    % if sum(co)*sum(dd)*sum(dc)>0,

    hne = dlmread([pathname, char(aa(kkl).name)], '', 11, 0);
    co=hne(:,2); 
    dc=hne(:,3); 
    dd=hne(:,4);

    %espectro de aceleração
    %qq1=spectrum(co,128,64);
    %qq1=2*dt*qq1(2:65,1);
    %usando pwelch
    % [qq1 F]=pwelch(co,hanning(128), 64, 128, fa);
    [qq1 F]=pwelch(co, hanning(NFFT), round(NFFT/2), NFFT, Fs);
    qq1=qq1(2:end,1);
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
    ww55(2)=sum(qq1(7:9))+qq1(10)/2;              % 18.4 a 12.8
    ww55(3)=qq1(10)/2+sum(qq1(11:15))+qq1(16)/2;   % 11.7 a 8.00
    ww55(4)=qq1(16)/2+sum(qq1(17:30))+qq1(31)/2;  % 7.50 a 4.20
    ww55(5)=qq1(31)/2+sum(qq1(32:64));            % 4.00 a 2.00
    
    %caso queira alisar mais o espectro
    % qq2=smooth(qq1,6);
    
    %se necessario, espectros dos slopes
    
    %     qq3=spectrum(dd,128,64);qq3=2*qq3(2:65,1);
    %     qq4=spectrum(dc,128,64);qq4=2*qq4(2:65,1);
    %     ss1(kkl)=96.23*(qq3(8)+qq4(8))/w4(8);
    %     ss2(kkl)=qq1(8)/w4(8);
    %     ss(kkl)=ss2(kkl)/ss1(kkl);
    
    
    %cálculo dos picos
    g2=diff(qq1);
    g2=sign(g2);
    g2=diff(g2);
    g2=[0;g2];
    g2=find(g2==-2);
    
    %escolhendo os 4 maiores
    % [g4 g5]=sort(qq2(g2));
    [g4 g5]=sort(qq1(g2));
    g5=flipud(g5);
    
    g5=g2(g5);
    g20=g5;
    g5=[g5;0;0;0;0];
    g5=g5(1:4);
    g=find(g5<13);

    isempty(g);
    if ans==0,
        picpic(kkl)=g5(g(1));
    end;
      
    g=find(g5>0);g6=g5(g);
    g5=128./g5(g);
    w55(6:5+length(g5))=g5;
    %os 4 maiores picos (se maiores do que zero)
    %foram colocados em ww55, de forma sequencial.
    
    %picos1 contem os valores (ordem) dos picos do
    %centro das faixas
    picos1=[8;14;21;42];
    picos2=picos1;
    

    %se em g20 houver picos nas faixas os valores serão
    %colocados em picos1
    
    g7=[13;17;33;60];
    for i=1:length(g7),
        g=find(g20<g7(i));
        g11=isempty(g);
        if g11==0,
            picos1(i)=g20(g(1));
            g20(g)=80;
        end
    end;

    % figure
    % plot(qq1)
    % hold all
    % plot(picos1, qq1(picos1), 'o')
    % shg


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
        s1=wavecos(:,s);
        g=find(s1)>0;
        out1=wavecos(g,s);
        out3=wavesen(g,s);
        m=length(g);
        m1=1024-m;

        %parâmetros para cálculo de tet2 e sp2
        m3=m1;
        m1=m1-1;
        m3=m1;
        m4=2*dt/(m*.375);
        m2=m-1;
        mq=round(m/2);
        daat1_doutorado
        %testegx34
        
        %na faixa 1 usa-se a tecnica de contour
        %if iwq==1,daatgx3matriz,
        %else;
        daat2_doutorado
        %valor maximo do d(teta)
        e=find(x==max(x));

        dire(kkl,iwq)=e(1);
        %energia obtida do espectro de aceleração/w4;
        espe(kkl,iwq)=energ(iwq+1,kkl);
    end
end

dlmwrite('/home/hp/Dropbox/doutorado/dados/espe_mat.txt', espe)
dlmwrite('/home/hp/Dropbox/doutorado/dados/dire_mat.txt', dire)

espe = espe(1:3:end,:);
dire = dire(1:3:end,:);

filtradaat

espe1 = espe;
dire1 = dire;

ws1 = ws(1:3:end);
wd1 = wd(1:3:end);
wd1(end) = wd1(end-1);

pleds_doutorado