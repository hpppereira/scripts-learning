% *************************************************************************
% calculo dos dados da boia ES - funcao spectrum
% calculo da direcao conforme utilizado no CENPES
%**************************************************************************
close all;clear all;clc
% -------------------------------------------------------------
%identifica arquivos
mes=11;% mes
ano=2006;% ano
dt=1;%frequencia de amostragem
%ler o diretorio
!ls /home/hp/GoogleDrive/ages/data/boia_merenda/brutos > lista
lista=textread('lista', '%s', 'delimiter', '\n','whitespace', '');
z=char(lista);
%seleciona os arquivos do mes
z2=find(z(:,1)=='O');z3=z(z2,:);z3=z3(:,6:13);g=str2num(z3(:,3:4));
g1=find(g==mes);z3=z3(g1,:);%z3 contem os strings com os nomes dos registros
% eixo de frequencia 32 graus
x=dt*64;
f1=1/x:1/x:32/x;%vetor de frequ�ncias

l=length(z3);%tamanho do arquivo
% comparando funcao spectrum com a cpsd
for ik=1:l;
    %carregando o arquivo
    a=eval(['load(''Onda_',num2str(z3(ik,:)) '.dat'')']);
    %heave, roll e pitch
    co=a(:,1); %os resultados vem em metros
    dc=-a(:,2); % roll
    dd=a(:,3); % pitch
    de=a(:,4); %compas
    %correcao
    dc= cos(pi*de/180) .* dc + sin(pi*de/180) .* dd;  
    dd= -sin(pi*de/180) .* dc + cos(pi*de/180) .*dd; 
    % ................ 1D .......................
    qq1=spectrum(co,100,50);qq1=2*qq1(2:51,1); 
    df=f1(2)-f1(1);
    m0_daat(ik)=sum(qq1*df);hs_daat(ik)=4*sqrt(sum(qq1)*df);
    g1=find(qq1==max(qq1));
    g5=1./f1(g1(1));g7=g1(1);  
    % periodo de pico 
    tp_daat(ik)=g5; %período para verificacao
     
    %............... DIRECAO .....................
    % ---- calculo usando spectrum ----
    co=-co;% heave negativo
    r1=2*spectrum(co,dc,100,50); % me da 8 colunas
    r2=2*spectrum(co,dd,100,50);
    ir1=imag(r1(2:51,3));% parte imaginaria 
    ir2=imag(r2(2:51,3));    
    c0=angle(ir1+j*ir2); % angulo    
    c0=c0*180/pi;
    c0=270-c0;
    c0=c0(g7);
    c00=find(c0<=0);c0(c00)=c0(c00)+360;
    c00=find(c0>=360);c0(c00)=c0(c00)-360;
    % direcao de pico
    dp_daat(ik)=c0;
    
    % ---- calculo usando a funcao cpsd ----
    r11=spectrum(co(1:1024,1),dc(1:1024,1),64,32); % me da 1 coluna
    r21=spectrum(co(1:1024,1),dd(1:1024,1),64,32);
    a8=imag(r11(2:33)); % parte imaginaria
    a9=imag(r21(2:33));
    c1=angle(a8+j*a9); % angulo    
    c1=c1*180/pi;
    c1=270-c1;
    c1=c1(g7);
    c11=find(c1<=0);c1(c11)=c1(c11)+360;
    c11=find(c1>=360);c1(c11)=c1(c11)-360;
    % direcao de pico
    dp_daat1(ik)=c1;
end;

% dados já processados CENPES
saida=load('saida.out');% selecionar dados do mes de novembro (481:1200)
%direcao de pico
dp=saida(481:1200,26);%Direcao Espectral 
dp_1=saida(481:1200,36);%Direcao do Pico 1 (Mais Energetico)  
%dp 
figure(1)
plot(dp,'r');hold on
plot(dp_daat,'k');plot(dp_daat1,'g');
h = legend('saida_cenpes','spectrum','cpsd');
set(h,'Interpreter','none','Orientation','vertical',...
    'fontsize',14,'fontweight','b','linewidth',3)

% % calculo NCBC
% for ik=1:l;
%     %carregando o arquivo
%     a=eval(['load(''Onda_',num2str(z3(ik,:)) '.dat'')']);
%     %heave, roll e pitch
%     co=a(1:1024,1); %os resultados vem em metros
%     dc=-a(1:1024,2); % roll
%     dd=a(1:1024,3); % pitch
%     
%     % ................ 1D .......................
%     qq1=spectrum(co,64,32);qq1=2*qq1(2:33,1); 
%     df=f1(2)-f1(1);
%     m0_daat(ik)=sum(qq1*df);hs_daat(ik)=4*sqrt(sum(qq1)*df);
%     g1=find(qq1==max(qq1));
%     g5=1./f1(g1(1));g7=g1(1);  
%     % periodo de pico 
%     tp_daat(ik)=g5; %período para verificacao
%      
%     %............... DIRECAO .....................
%     % ---- calculo usando spectrum ----
%     %co=-co;
%     r1=spectrum(co,dc,64,32);
%     r2=spectrum(co,dd,64,32);
%     r3=spectrum(dc,dd,64,32);
%     r1=2*r1(2:33,:);r2=2*r2(2:33,:);r3=2*r3(2:33,:);
%     %auto-espectro
%     autor1=r1(:,1);autor2=r1(:,2);autor3=r2(:,2);
%     %pegando imaginario do spc cruzado de heave e elevaçoes
%     ir1=imag(r1(:,3));ir2=imag(r2(:,3));
%     zz=sqrt(autor1.*(autor2+autor3));    
%     g1=find(zz==0);zz(g1)=1;
%     g1=find(z==0);z(g1)=1;
%     b1=ir2./zz;%heave/pitch
%     a1=ir1./zz;%heave/roll
%     c0=atan2(b1,a1);
% %    c0=angle(ir1+j*ir2);
%     c0=c0*180/pi;
%     c0=270-c0-23;
%     c0=c0(g7);
% 
%     c00=find(c0<=0);c0(c00)=c0(c00)+360;
%     c00=find(c0>=360);c0(c00)=c0(c00)-360;
%     % direcao de pico
%     dp_daat2(ik)=c0;
% end;
% 
% figure(2)
% plot(dp,'r');hold on
% plot(dp_daat,'k');plot(dp_daat2,'m*');
% h = legend('saida_cenpes','spectrum','spectrum_ncbc',1);
% set(h,'Interpreter','none','Orientation','vertical',...
%     'fontsize',14,'fontweight','b','linewidth',3)
