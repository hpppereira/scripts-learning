%**************************************************************************
% Rotina daatES2012.m para uso da DAAT com wavelets com dados da boia na
% Bacia do Espirito Santo
% intervalo de amostragem=1s
% tempo de registro=20min
% numero de pontos por registro=1200
%**************************************************************************
close all;clear all;clc
% -------------------------------------------------------------
%identifica arquivos
%escolher o mes
mes=11;
ano=2006;
%ler o diret�rio
!ls > lista
lista=textread('lista', '%s', 'delimiter', '\n','whitespace', '');
z=char(lista);
%seleciona os arquivos do mes
z2=find(z(:,1)=='O');
z3=z(z2,:);z3=z3(:,6:13);
g=str2num(z3(:,3:4));
g1=find(g==mes);
z3=z3(g1,:);%z3 contem os strings com os nomes dos registros
ho=str2num(z3(:,7:8));

% ------------------------------------------------------------
%preparo dos arquivos
dire=zeros(10,248);%dire��o (2 valores, at�  5 faixas)
espe=zeros(10,248);%espectros(2 valores, at� 5 faixas)
energ=zeros(10,248);%Hs + 5 energias (uma por faixa), 4 picos (maiores)
dire1=dire;espe1=espe;
% table of sines and cosines for the mem method - tecnica de maxima entropia
load lyg2.mat;
a26=[a23(311:360) a23 a23(1:50)];
a27=[a24(311:360) a24 a24(1:50)];
a30=[(311:360) (1:360) (1:50)];
grad1=0.0175;grad2=180/pi;
dt=1;%intervalo da amostragem (sgundos)
%par o saso de usar matr1 (matriz de ocorr�ncias)
sa=[.5;.5;.5;.5;0.1];

%ordem e valor dos picos por faixa - essa separa��o pode ser reajustada
%faixa 1    faixa 2     faixa 3     faixa 4     faixa 5
%10-20      19-10.52    24-8.33     28-7.1      51-3.92
%11=18.18   20-10       25-8.00     50-4.0      100-at� final
%12-16.66   21-9.52     26-7.69
%13-15.38   22-9.05     27-7.4
%14-14.28   23-8.69
%15-13.33
%16-12.5
%17-11.76
%18-11.11

% ------------------------------------------------------
% aplicados ao ES
%as wavelets ser�o calculadas para 3 ciclos - cada uma
%correspondendo a um pico do espectro de 1D - para um numero de pontos
%de uma wavelet de 3 ciclos multiplica--se o per�odo acima por 3 e
%divide-se por 1 exemplo para 20 segundos.

%preparam-se ent�o as wavelets para os per�odos das 5 faixas - com
%aproxima��o para numero inteiro de pontos
% ----------- ES -------------------------
% faixa 5: 9
% faixa 4: 21 21 20 19 19 18 18 17 17 16 16 15 15 15 14 14 14 13 13 13...
% faixa 3: 25 24 23 22
% faixa 2: 32 30 29 27 26
% faixa 1: 60 55 50 46 43 40 37 35 33
% --------- PECEM ---------------------------
%faixa 1: 77,70,64,59,55,51,48,46,43
%faixa 2: 40,38,37,35,33
%faixa 3: 32,31,30,28
%faixa 4: 27,26,26,25,24,23,23,22 (ate per�odo numero 36-5.5 segundos)
%faixa 5: 12 - correspondente a 3 segundos
% -----------------------------------------------------------


% o objetivo aqui � ter wavelets prontas para us�-las de acordo com
%o pico das faixas; caso n�o haja pico em uma faixa, usa-se  wavelets
%correspondentes a: faixa 1 - 14.28 s (55 pontos), faixa 2 - 9.52 s
%(37 pontos), faixa 3 - 7.76 s (30 pontos ) e faixa 5- 3 s (12 pontos)
% PECEM
%mm=[77;70;64;59;55;51;48;45;43;40;38;37;35;33;32;31;30;28;...
%    27;26;26;25;24;23;23;22;21;20;19;18;17;16;15;12];
% ES
mm=[60;55;50;46;43;40;38;35;33;32;30;29;27;26;25;24;23;22;21;21;20;19;...
    19;18;18;17;17;16;16;15;15;15;14;14;14;13;13;13;12;12;12;12;12;11;...
    11;11;11;11;10;10;10;10;10;10;9];

ms=[];
wavecos=zeros(60,55);wavesen=wavecos;
for i=1:55,mn=mm(i);ms=[ms;mn];
    out2=linspace(-3.14,3.14,mn);
    gau=hanning(mn);
    out1 =gau'.* cos(3*out2);
    out3 =gau'.* sin(3*out2);
    wavecos((1:mn)',i)=out1';
    wavesen((1:mn)',i)=out3';
end;
x=dt*200;
f1=1/x:1/x:100/x;%vetor de frequ�ncias

ik=length(z3);
kkl=0;
for ik=1:ik;

    kkl=kkl+1;
    media=0;
    %carregando o arquivo
    a=eval(['load(''Onda_',num2str(z3(ik,:)) '.dat'')']);

    %heave, roll e pitch
    co=a(:,1); %os resultados vem em metros
    dc=a(:,2); % ROLL
    dd=a(:,3); % PITCH

    if length(co)==1200,
    %verificando qualidade dos dados
    media=abs(mean(co))+abs(mean(dd))+abs(mean(dc));

    if media>0.1,


        %limite superior (3db) e limite inferior (3 db)
        % 1) 20     11.1
        % 2) 11.1   8.69
        % 3) 8.69   7.4
        % 4) 7.4    4.0
        % 5) 4.0    end

        % a wavelet ser� gerada com as regras acima

        % ser�o calculadas as energias em cada faixa mencionada a pertir do
        % espectro de uma dimens�o considerando que o espa�amento entre cada
        % frequ�ncia � de 1/T

        %Calculo do espectro de 1 dimens�o
        ww55=zeros(10,1);
        %espectro calculado com 200 pontos e 100 de overlapping;
        % grau de liberdade = 12
        % equivale a 6 segmentos de 200s
stop
        %[qq1,f2]=pwelch(co,200,100);
        qq1=spectrum(co,200,100);

        %faixas em segundos
        %2     3    4
        %4     6    7.2
        %7.14  8    10.8
        %10.3  16   20.0

        qq1=2*qq1(2:101,1);

        df=1/200;
        %onda significativa
        ww55(1)=4*sqrt(sum(qq1)*df);
        %espectros nas 4 faixas
        ww55(2)=sum(qq1(10:17))+qq1(18)/2;
        ww55(3)=qq1(18)/2+sum(qq1(19:22))+qq1(23)/2;
        ww55(4)=qq1(23)/2+sum(qq1(24:26))+qq1(27)/2;
        ww55(5)=qq1(27)/2+sum(qq1(28:49))+qq1(50)/2;
        ww55(6)=qq1(50)/2+sum(qq1(51:100));

        %picos1 � o valor do per�odo que corresponde
        %� wavelet que ser� usada
        %quando n�o h� pico na faixa: 43=14.3 s;29=9.52 s;23=7.69s;
        %15=5s;%9=3s;
        picos1=[43;29;23;15;9];
        %alisa-se mais o espectro para calcular os picos
        qq2=smooth(qq1,8);
        g1=diff(qq2);g1=sign(g1);g1=diff(g1);
        g1=[0;g1];
        g1=find(g1==-2);

        %ser�o calculados os 4 maiores picos
        [g4 g5]=sort(qq2(g1));
        g6=flipud(g1(g5));
        g6=g6(g6>10);      
        %coloca��o dos picos nas faixas para determina��o das
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

        %valores dos picos para o arquivo final
        g5=flipud(g5);g5=g1(g5);
        g5=[g5;0;0;0;0];g5=g5(1:4);
        g=find(g5>0);g5(g)=200./g5(g);

        %preparo final do energ
        ww55(7:10)=g5;
        
        energ(:,kkl)=ww55;


        %ser�o calculadas 5 faixas com wavelets
        %para cada wavelet calcula-se uma matriz de dire��o e desvio
        %padrao obtendo-se um D(teta) para cada faixa

        for iwq=1:5,

            g11=find(picos1(iwq)==mm);

            m=mm(g11(1));
            out1=wavecos((1:m)',g11(1));
            out3=wavesen((1:m)',g11(1));

            matr1=ones(20,90);

            m1=1200-m;
            %par�metros para c�lculo de tet2 e sp2
            m3=m1;m1=m1-1;m3=m1;
            m4=2*dt/(m*0.375);
            m2=m-1;
             daatES21

             %dire1(iwq,kkl)=mean(tet2*180/pi);

             daatES22



        end;
    end;
    end;
end;
       

  
    
    
    
