%**************************************************************************
% Rotina daatcassino.m para uso da DAAT com wavelets com dados da bóia
% directional waverider
%**************************************************************************

%1. preparo de variaveis
%2. carrega variaveis auxiliares
%3. os arquivos a serem analisados estão no vetor g27 preparado
%por arrumabcampos.m e consistidos por spikesbcampos.m
%4. gera arquivos sucessivos a cada tres horas
%5. separa as tres series de heave pitch e roll
%6. calcula espectro e separa as faixas de energia
%7. Sao 5 faixas; para cada faixa prepara-se a funçao basica para a convoluçao,
%   faz-se a convolucao, e obtem-se  tet2(direçao principal)
%   e sp2 (espectro) com tecnicas de maxima entropia - programa
%   daatbcampos21.m
%8. Seleciona-se os segmentos para o calculo de d(teta) - daatmarlim22
%9. este programa calcula direçao principal e espectro para cada faixa
%   (ate 2 valores)

%possibilidades de entrada de dados:
%1) arquivo g27 com o nome dos files obtidos a partir do script tipo
%arruma
%2) arquivo individual - fazer load depois do for (iv)
%a15size=zeros(5,248);%quantidade de sementos selecionados por faixa
%direcao=zeros(360,30);%caso se deseje guardar o arquivo
%de direção correspondente a uma faixa
%sa=[1;1;1;1;0.1];
%mm=[[64;60;56;52;47] [34;33;0;0;0]...
%          [24;22;20;18;0] [13;12;10;0;0]];
f=1/128:1/128:0.5;
%load ff
ff=[7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;...
    22;24;25;27;29;32;35;39;43;49;55;62];
mn=round(3*1./f(ff));
wavecos=zeros(55,27);wavesen=wavecos;
for i=1:length(ff),
    out2=linspace(-3.14,3.14,mn(i));
    gau=hanning(mn(i));
    out1 =gau'.* cos(3*out2);
    out3 =gau'.* sin(3*out2);
    wavecos((1:mn(i))',i)=out1';wavesen((1:mn(i))',i)=out3';
    
end;



espe=zeros(27,1024-6);%espectros(2 valores, até 5 faixas)
energ=zeros(10,248);

% table of sines and cosines for the mem method
% load lyg2.mat;
% a26=[a23(311:360) a23 a23(1:50)];
% a27=[a24(311:360) a24 a24(1:50)];
% a30=[(311:360) (1:360) (1:50)];
grad1=0.0175;grad2=180/pi;

%ano e mes
% mh1='92';
% mh2='03';
% ano=mh1;
% mes=mh2;
% dt=1;
% ano=str2num(mh1);
% mes=str2num(mh2);
% ad1=[mh2];
load 92032522.DAT
co=X92032522(:,2);
qq1=spectrum(co,128,64);

%faixas em segundos
%2     3    4
%4     6    7.2
%7.14  8    10.8
%10.3  16   20.0

qq1=2*qq1(2:65,1);
% df=1/128;
% %onda significativa
% ww55(1)=4*sqrt(sum(qq1)*df);
% %energias nas 4 faixas
% ww55(2)=sum(qq1(5:10))+qq1(11)/2;
% ww55(3)=qq1(11)/2+sum(qq1(12:15))+sum(qq1(16:17))/2;
% ww55(4)=sum(qq1(16:17))/2+sum(qq1(18:22))+sum(qq1(23:24))/2;
% ww55(5)=sum(qq1(23:24))/2+sum(qq1(25:30))+qq1(31)/2;
% ww55(6)=qq1(31)/2+sum(qq1(32:end));
% 
g1=diff(qq1);g1=sign(g1);g1=diff(g1);
g1=[0;g1];
g1=find(g1==-2);
% 
% 
[g4 g5]=sort(qq1(g1));
g5=flipud(g5);g5=g1(g5);

%g6=[g5;80*ones(20,1)];
%g6=g5(1:20);
%picos(:,kkl)=g6(1:20);

g5=[g5;0;0;0;0];g5=g5(1:4);

%g=find(g5>0);
g5=128./g5(g);

% ww55(7:10)=g5;
% energ(:,kkl)=ww55;

%as wavelets serão calculadas para as 4 faixas
%de acordo com a tabela abaixo,
%varre-se a faixa com wavelets de diferentes periodos
%para cada wavelet calcula-se uma matriz de direçaõ e desvio
%padrao com valores de espectro nas "caixas". Multiplicam-se
%as matrizes de cada wavelet

%mm=[[64;60;56;52;47] [34;33;0;0;0]...
%    [24;22;20;18;0] [13;12;10;0;0]];
%s1=[1.5;1.5;1.5;1.5];
%sa=[1;1;1;0.1];
dt=1;
matri=zeros(27,1024-6);
for iwq=1:27,
    
    out1=wavecos((1:mn(iwq))',iwq);
    out3=wavesen((1:mn(iwq))',iwq);
    
    
    m=mn(iwq);
    m1=1024-m;
    %parâmetros para cálculo de tet2 e sp2
    m3=m1;m1=m1-1;m3=m1;
    m4=2*dt/m;
    m2=m-1;
    
    a1=filter((out1-j*out3)',1,co);
    a1=a1(m:1024);
    z41=a1;
    a4=m4*(z41.*conj(z41));
    matri(iwq,1:length(a4))=a4;
end;
v=[1 1019 0.05 0.3];
contour(1:1019,f(ff),matri(:,1:1019),8);grid
%mesh(1:1019,f(ff),matri(:,1:1019));view(0,90);shg
x=[1;1019];y=[1/g5(1);1/g5(1)];line(x,y,'color','r','linewidth',2);
axis(v);
hold on
if g5(2)>0,x=[1;1019];y=[1/g5(2);1/g5(2)];line(x,y,'color','r','linewidth',2);end
if g5(3)>0,x=[1;1019];y=[1/g5(3);1/g5(3)];line(x,y,'color','r','linewidth',2);end
if g5(4)>0,x=[1;1019];y=[1/g5(4);1/g5(4)];line(x,y,'color','r','linewidth',2);end
hold off
shg



