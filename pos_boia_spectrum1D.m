% *************************************************************************
% calculo dos dados da boia ES - funcao spectrum
%**************************************************************************
close all;clear all;clc
% -------------------------------------------------------------
%identifica arquivos
mes=11;% mes
ano=2006;% ano
dt=1;%frequencia de amostragem
%ler o diretorio
!ls > lista
lista=textread('lista', '%s', 'delimiter', '\n','whitespace', '');
z=char(lista);
%seleciona os arquivos do mes
z2=find(z(:,1)=='O');z3=z(z2,:);z3=z3(:,6:13);g=str2num(z3(:,3:4));
g1=find(g==mes);z3=z3(g1,:);%z3 contem os strings com os nomes dos registros
% eixo de frequencia 32 graus
x=dt*64;
f1=1/x:1/x:32/x;%vetor de frequ�ncias

l=length(z3);%tamanho do arquivo

for ik=1:l;
    %carregando o arquivo
    a=eval(['load(''Onda_',num2str(z3(ik,:)) '.dat'')']);
    %heave, roll e pitch
    co=a(1:1024,1); %os resultados vem em metros
    dc=-a(1:1024,2); % 
    dd=a(1:1024,3); %
            
    qq1=spectrum(co,64,32);% 32 graus
    qq1=2*qq1(2:33,1); %2*spectrum*dt
    df=f1(2)-f1(1);
    m0_daat(ik)=sum(qq1*df);
    hs_daat(ik)=4*sqrt(sum(qq1)*df);

    %alisa-se mais o espectro para calcular os picos
    %qq2=smooth(qq1,8);
    g1=find(qq1==max(qq1));
    g5=1./f1(g1(1));
        
    %valor do pico para o arquivo final
    g7=g1(1);
        
    % periodo de pico 
    tp_daat(ik)=g5; %período para verificacao
    
    % calculo das direcoes com 32 graus
    r1=cpsd(co,dc,64,32);
    r2=cpsd(co,dd,64,32);
    a8=imag(r1(2:33));
    a9=imag(r2(2:33));
    %--
    c0=angle(a8+j*a9);
    c0=c0*180/pi;
    c0=270-c0-23;
    c0=c0(g7);
    c00=find(c0<=0);c0(c00)=c0(c00)+360;
    c00=find(c0>=360);c0(c00)=c0(c00)-360;
    % direcao de pico
    dp_daat(ik)=c0;
end;

% dados já processados CENPES
saida=load('saida.out');
dia=saida(:,1);mes=saida(:,2);ano=saida(:,3);hora=saida(:,4);min=saida(:,5);
% selecionar dados do mes de novembro (481:1200)
% altura significativa
hs=4.*sqrt(saida(481:1200,17));
m0=saida(481:1200,17);
% periodo de pico
tp=saida(481:1200,22);
%direcao de pico
dp=saida(481:1200,26);

%tp
figure(1)
plot(tp,'r')
hold on;plot(tp_daat,'k')
%dp 
figure(2)
plot(dp,'r');hold on
plot(dp_daat,'k')

figure(3)
plot(hs,'r');hold on
plot(hs_daat,'k')

figure(4)
plot(m0,'r');hold on
plot(m0_daat,'k')
