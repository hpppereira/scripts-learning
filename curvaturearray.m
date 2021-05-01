function[dadosteste,dd]=curvaturearray(neta1,netax,netay,netaxx,netayy,deltat,donv,neta)

%calcula espectro direcional para ondografo de curvatura
%DADOS DE ENTRADA  
%                 eta1...eta5  = vetor de deslocamento vertical(potencia de 2)
%                 deltat = intervalo de amostragem
%                 donv = direçao que o eixo de origem (x) faz com o Norte
%                 Verdadeiro medido no sentido horario

%DADOS DE SAIDA
%MATRIZ CONTENDO: COLUNA 1 = frequencia
%                        2 = auto espectro de eta5 (central)
%                        3 = direcao principal
%                        4 = espalhamento angular 

%SUBRROTINAS CHAMADAS

%                  cortheta.m
%                  espec.m
%                  espec2.m





% Inicializaçao de constantes

reg=1024;
reg2=fix(reg/2);
gl=50;
dt=1.0;
donv=270;

% Dados de entrada
% % % load d:\users\joao\estagiarios\eduardo\registro1.txt
% % % 
% % % for n=1:5
% % %     registro(:,n)=registro1(:,n);
% % % end
% % % 
% % % 
% % % 
% % % 
% % % hv=registro(:,1)';
% % % ptew=registro(:,2)';
% % % ptns=registro(:,3)';
% % % curew=registro(:,4)'; %=>NOVO
% % % curns=registro(:,5)'; %=>NOVO

%outra maneira de se obter os dados de entrada
%load data neta netax netay netaxx netayy

hv=neta;
ptew=netax;
ptns=netay;
curew=netaxx; %=>NOVO
curns=netayy; %=>NOVO

%--------------------------
%Rotina gerdir-> subrotina
%--------------------------

%Parametros de Entrada(I) e Saida(O) 

%HV...................vetor de heave(I)
%HV2..................vetor de heave2(I)
%HV3..................vetor de heave3(I)
%ptns.................vetor de pitch norte/sul(I)
%ptew.................vetor de pitch leste/oeste (I)
%reg..................numero de pontos(I)
%donv.................direcao do eixo de origem em relaçao dao N.V. (I)
%gl...................graus de liberdade(I)
%dt...................taxa de amostragem(I)

%fpico................frequencia de pico(O)
%dirfp................direcao principal na frequencia de pico(O)
%theta................vetor de direcao principal
%thetom...............direcao media considerando todas as frequencias (O)
%ui...................indice de unidiretividade

% Variaveis internas

%I....................contador
%fc...................frequencia de corte
%delta f..............incremento em frequencia
%reg2.................numero de pontos em frequencia
%gl2..................metade do numero de graus de liberdade
%x1,x2,y1,...,z6......vetores reais e imaginarios
%zn1-zn14.............coeficiente de fourier
%autn1,autn2,autn3....vetor do espectro
%qdn1ew...............vetor do quad-espectro entre hv e ptew
%qdn1ns...............vetor do quad-espectro entre hv e ptns
%qdnews...............quad-espectro entre ptew e ptns
%coewew.................vetor do co-espectro de ptew
%consns.................vetor do co-espectro de ptns
%conews...............coespectro entre ptew e ptns
%fasens...............vetor de fase entre n1 e ptns
%faseew...............vetor de fase entre n1 e ptew
%fasenews.............vetor de fase entre ptew e ptns
%S....................vetor parametro de espalhamento
%F....................frequencia
%K....................vetor numero de onda
%KK...................numero de onda teoria linear
%R....................razao KK/K
%A1,B1................coeficiente de fourier
%intauxc,intauxs,intautn1........integrais do calculo de thetom
%auxc, auxs...........vetores auxiliares para calculo de thetom
%A,B..................variaveis utilizadas no calculo de thetom
%thetaux..............variavel auxiliar para calculo de thetom
%spico................ordenada espectral na frequencia de pico

% Inicializaçao de variaveis

temp=2.*dt;
fc=1/temp;
deltaf=fc*2/reg;
reg2=fix(reg/2);
gl2=fix(gl/2);
spico=0;

%inicializa os vetores para a rotina de FFT

for i=1:reg;
    z1(i)=hv(i);
    %z3(i)=hv2(i);
    %z5(i)=hv3(i);
    x1(i)=ptew(i);
    y1(i)=ptns(i);
    xx1(i)=curew(i); %=>NOVO
    yy1(i)=curns(i); %=>NOVO
    z2(i)=0;
    z4(i)=0;
    z6(i)=0;
    x2(i)=0;
    y2(i)=0;
    xx2(i)=0; %=>NOVO
    yy2(i)=0; %=>NOVO
end

%-----------------------------------
%Chama rotina de fft -> subrotina
%-----------------------------------


aa = fft(x1);
x1=real(aa);
x2=imag(aa);

aa = fft(y1);
y1=real(aa);
y2=imag(aa);

aa = fft(z1);
z1=real(aa);
z2=imag(aa);

%aa = fft(z3);
%z3=real(aa);
%z4=imag(aa);

%aa = fft(z5);
%z5=real(aa);
%z6=imag(aa);

aa=fft(xx1); %=>NOVO
xx1=real(aa);
xx2=imag(aa);

aa=fft(yy1); %=>NOVO
yy1=real(aa);
yy2=imag(aa);

% Calcula os coeficientes da transformada de fourier

for i=1:reg2;
    zn1(i)=z1(i)*z1(i);
    zn2(i)=z2(i)*z2(i);
    zn3(i)=z2(i)*x1(i);
    zn4(i)=z1(i)*x2(i);
    zn5(i)=z2(i)*y1(i);
    zn6(i)=z1(i)*y2(i);
    zn7(i)=x1(i)*x1(i);
    zn8(i)=x2(i)*x2(i);
    zn9(i)=y1(i)*y1(i);
    zn10(i)=y2(i)*y2(i);
    %zn11(i)=z3(i)*z3(i);
    %zn12(i)=z4(i)*z4(i);
    %zn13(i)=z5(i)*z5(i);
    %zn14(i)=z6(i)*z6(i);
    zn15(i)=x2(i)*y1(i);
    zn16(i)=x1(i)*y2(i);
    zn17(i)=x1(i)*y1(i);
    zn18(i)=x2(i)*y2(i);
    %------------------------------------
    zn19(i)=x2(i)*xx1(i); %=>NOVO
    zn20(i)=x1(i)*xx2(i); %=>NOVO
    zn21(i)=x2(i)*yy1(i); %=>NOVO
    zn22(i)=x1(i)*yy2(i); %=>NOVO
    zn23(i)=y2(i)*xx1(i); %=>NOVO
    zn24(i)=y1(i)*xx2(i); %=>NOVO
    zn25(i)=y2(i)*yy1(i); %=>NOVO
    zn26(i)=y1(i)*yy2(i); %=>NOVO
    zn27(i)=xx1(i)*xx1(i); %=>NOVO
    zn28(i)=xx2(i)*xx2(i); %=>NOVO
    zn29(i)=yy1(i)*yy1(i); %=>NOVO
    zn30(i)=yy2(i)*yy2(i); %=>NOVO
    zn31(i)=xx2(i)*yy1(i); %=>NOVO
    zn32(i)=xx1(i)*yy2(i); %=>NOVO
    zn33(i)=xx1(i)*yy1(i); %=>NOVO
    zn34(i)=xx2(i)*yy2(i); %=>NOVO
    zn35(i)=x1(i)*xx1(i); %=>NOVO
    zn36(i)=x2(i)*xx2(i); %=>NOVO
    zn37(i)=y1(i)*yy1(i); %=>NOVO
    zn38(i)=y2(i)*yy2(i); %=>NOVO
    zn39(i)=y1(i)*xx1(i); %=>NOVO
    zn40(i)=y2(i)*xx2(i); %=>NOVO
    zn41(i)=y1(i)*yy1(i); %=>NOVO
    zn42(i)=y2(i)*yy2(i); %=>NOVO
    zn43(i)=z2(i)*xx1(i); %=>NOVO
    zn44(i)=z1(i)*xx2(i); %=>NOVO
    zn45(i)=z2(i)*yy1(i); %=>NOVO 
    zn46(i)=z1(i)*yy2(i); %=>NOVO
    zn47(i)=z1(i)*xx1(i);%????????
    zn48(i)=z2(i)*xx2(i);%????????????
    zn49(i)=z1(i)*yy1(i);%???????????????
    zn50(i)=z2(i)*yy2(i);%???????????????
  %-------------------------------------------------
end

%---------------------------------------
%Chama rotina de alisamento do espectro -> subrotina
%---------------------------------------
zn1=alisa2(zn1);
zn2=alisa2(zn2);
zn3=alisa2(zn3);
zn4=alisa2(zn4);
zn5=alisa2(zn5);
zn6=alisa2(zn6);
zn7=alisa2(zn7);
zn8=alisa2(zn8);
zn9=alisa2(zn9);
zn10=alisa2(zn10);
%zn11=alisa2(zn11);
%zn12=alisa2(zn12);
%zn13=alisa2(zn13);
%zn14=alisa2(zn14);
zn15=alisa2(zn15);
zn16=alisa2(zn16);
zn17=alisa2(zn17);
zn18=alisa2(zn18);
zn19=alisa2(zn19); %=>NOVO
zn20=alisa2(zn20); %
zn21=alisa2(zn21);
zn22=alisa2(zn22);
zn23=alisa2(zn23);
zn24=alisa2(zn24);
zn25=alisa2(zn25);
zn26=alisa2(zn26);
zn27=alisa2(zn27);
zn28=alisa2(zn28);
zn29=alisa2(zn29);
zn30=alisa2(zn30);
zn31=alisa2(zn31);
zn32=alisa2(zn32);
zn33=alisa2(zn33);
zn34=alisa2(zn34);
zn35=alisa2(zn35);
zn36=alisa2(zn36);
zn37=alisa2(zn37);
zn38=alisa2(zn38);
zn39=alisa2(zn39);
zn40=alisa2(zn40);
zn41=alisa2(zn41);
zn42=alisa2(zn42);
zn43=alisa2(zn43);
zn44=alisa2(zn44);
zn45=alisa2(zn45);
zn46=alisa2(zn46);%=>NOVO
zn47=alisa2(zn47);
zn48=alisa2(zn48);
zn49=alisa2(zn49);
zn50=alisa2(zn50);

%Zera vetores


for i=1:reg2;
    autn1(i)=0;
   % autn2(i)=0;
   % autn3(i)=0;
    qdn1ew(i)=0;
    qdn1ns(i)=0;
    qdn1xx(i)=0;
    qdn1yy(i)=0;
    qdewxx(i)=0; %=>NOVO
    qdewyy(i)=0; %=>NOVO
    qdnsxx(i)=0; %=>NOVO
    qdnsyy(i)=0; %=>NOVO
    qdnews(i)=0; %=>NOVO
    qdxxyy(i)=0; %=>NOVO
    coewew(i)=0;
    consns(i)=0;
    coxxxx(i)=0; %=>NOVO
    coyyyy(i)=0; %=>NOVO
    conews(i)=0; %=>NOVO
    coxxyy(i)=0; %=>NOVO
    coewxx(i)=0; %=>NOVO
    coewyy(i)=0; %=>NOVO
    consxx(i)=0; %=>NOVO
    consyy(i)=0;%=>NOVO
    con1xx(i)=0;
    con1yy(i)=0;
    theta(i)=0; %=>NOVO
    k(i)=0;
    kk(i)=0;
    s(i)=0;
    r(i)=0;
    faseew(i)=0;
    fasens(i)=0;
    fasenews(i)=0;
    fasen1xx(i)=0; %=>NOVO
    fasen1yy(i)=0; %=>NOVO
    fasexxyy(i)=0; %=>NOVO
    faseewxx(i)=0; %=>NOVO
    faseewyy(i)=0; %=>NOVO
    fasensxx(i)=0; %=>NOVO
    fasensyy(i)=0; %=>NOVO
end

%Calcula espectros derivados

for i=1:reg2;
    autn1(i)=2*dt/reg*(zn1(i)+zn2(i));
    %autn2(i)=2*dt/reg*(zn11(i)+zn12(i));
    %autn3(i)=2*dt/reg*(zn13(i)+zn14(i));
    qdn1ew(i)=2*dt/reg*(zn3(i)-zn4(i));
    qdn1ns(i)=2*dt/reg*(zn5(i)-zn6(i));
    qdn1xx(i)=2*dt/reg*(zn43(i)-zn44(i)); %=>NOVO
    qdn1yy(i)=2*dt/reg*(zn45(i)-zn46(i)); %=>NOVO
    qdewxx(i)=2*dt/reg*(zn19(i)-zn20(i)); %=>NOVO
    qdewyy(i)=2*dt/reg*(zn21(i)-zn22(i)); %=>NOVO
    qdnsxx(i)=2*dt/reg*(zn23(i)-zn24(i)); %=>NOVO
    qdnsyy(i)=2*dt/reg*(zn25(i)-zn26(i)); %=>NOVO
    coewew(i)=2*dt/reg*(zn7(i)+zn8(i));
    consns(i)=2*dt/reg*(zn9(i)+zn10(i));
    coxxxx(i)=2*dt/reg*(zn27(i)+zn28(i)); %=>NOVO
    coyyyy(i)=2*dt/reg*(zn29(i)+zn30(i)); %=>NOVO
    qdnews(i)=2*dt/reg*(zn15(i)-zn16(i));
    qdxxyy(i)=2*dt/reg*(zn31(i)-zn32(i)); %=>NOVO
    conews(i)=2*dt/reg*(zn17(i)+zn18(i));
    coxxyy(i)=2*dt/reg*(zn33(i)+zn34(i)); %=>NOVO
    coewxx(i)=2*dt/reg*(zn35(i)+zn36(i)); %=>NOVO
    coewyy(i)=2*dt/reg*(zn37(i)+zn38(i)); %=>NOVO
    consxx(i)=2*dt/reg*(zn39(i)+zn40(i)); %=>NOVO
    consyy(i)=2*dt/reg*(zn41(i)+zn42(i)); %=>NOVO
    con1xx(i)=2*dt/reg*(zn47(i)+zn48(i));%=====================
    con1yy(i)=2*dt/reg*(zn49(i)+zn50(i));%=====================
 
    k(i)=sqrt((coewew(i)+consns(i))/autn1(i));
    
    faseew(i)  =atan(qdn1ew(i)/coewew(i))*180/pi;
    fasens(i)  =atan(qdn1ns(i)/consns(i))*180/pi;
    fasenews(i)=atan(qdnews(i)/conews(i))*180/pi;
    fasen1xx(i)=atan(qdn1xx(i)/coxxxx(i))*180*pi; %=>NOVO
    fasen1yy(i)=atan(qdn1yy(i)/coyyyy(i))*180*pi; %=>NOVO
    fasexxyy(i)=atan(qdxxyy(i)/coxxyy(i))*180*pi; %=>NOVO
    faseewxx(i)=atan(qdewxx(i)/coewxx(i))*180*pi; %=>NOVO
    faseewyy(i)=atan(qdewyy(i)/coewyy(i))*180*pi; %=>NOVO
    fasensxx(i)=atan(qdnsxx(i)/consxx(i))*180*pi; %=>NOVO
    fasensyy(i)=atan(qdnsyy(i)/consyy(i))*180*pi; %=>NOVO
    
end

%Calcula direcao principal

for i=1:reg2;
    
    if autn1(i)>0.001;

        %Coeficientes de primeira ordem
        
        a1 =1/pi*qdn1ew(i)/(autn1(i)*k(i));
        a12=-4/(3*pi)*qdewxx(i)/(autn1(i)*k(i)^3);%=>NOVO
        a13=-4/pi*qdewyy(i)/(autn1(i)*k(i)^3); %=>NOVO
   
        b1 =1/pi*qdn1ns(i)/(autn1(i)*k(i));  
        b12=-4/(3*pi)*qdnsyy(i)/(autn1(i)*k(i)^3); %=>NOVO
        b13=-4/pi*qdnsxx(i)/(autn1(i)*k(i)^3); %=>NOVO
        %coeficientes de segunda ordem
        
        a21=-2/pi*((con1xx(i)/(autn1(i)*k(i)^2))+1/2);% observar o coespectro => Coespec N e Nxx
        a22=2/pi*((con1yy(i)/(autn1(i)*k(i)^2))+1/2);% observar o coespectro => Coespec N e Nxx
        b2 =2/pi*(conews(i)/autn1(i)*k(i)^2);
               
        %media dos coeficientes %=>NOVO
        
        am1=(a1+a12+a13)/3;
        bm1=(b1+b12+b13)/3;
        am2=(a21+a22)/2;
        bm2=b2;
        
        %Theta utilizando os coeficientes de primeira ordem      
        
        theta(i)=cortheta(a1,b1,donv);

        theta12(i)=cortheta2(a12,b12,donv);
        theta13(i)=cortheta2(a13,b13,donv);
        thetam(i)=cortheta2(am1,bm1,donv);

        %Theta utilizando os coeficientes de segunda ordem
        
        theta21(i)=cortheta(a21,b2,donv);
        theta22(i)=cortheta(a22,b2,donv);
        thetam2(i)=cortheta(am2,bm2,donv);
        
        thetaux=atan(b1/a1);
        auxc(i)=autn1(i)*cos(thetaux);
        auxs(i)=autn1(i)*sin(thetaux);
        s(i)=pi*sqrt(a1*a1+b1*b1);
        s(i)=s(i)/(1-s(i));
    end
end

% Calcula Direcao Media Geral
intauxc=integral(reg2,fc,auxc);
intauxs=integral(reg2,fc,auxs);
intautn1=integral(reg2,fc,autn1);

a=intauxc/intautn1; 
b=intauxs/intautn1;

ui=sqrt(a*a+b*b);
thetom=cortheta(a,b,donv);

% Grava Resultados

for i=1:reg2;
    
   %a.......frequencia
   %b.......densidade espectral serie 1 
   %c.......spectral ratio serie 2
   %d.......spectral ratio serie 3
   %e.......vetor numero de onda
   %f.......numero de onda (teoria linear)
   %g.......check ratio
   %h.......vetor direcao principal
   %i.......parametro de espalhamento
   %j.......fase N1xNS
   %l.......fase EWxNS
   
   f(i)=i*deltaf;
   kk(i)=4*f(i)*f(i)*1.006075882;
   r(i)=kk(i)/k(i);
   
   % Gera Direcao Principal da Frequencia de Pico
   if autn1(i)>spico;
       fpico=f;
       spico=autn1(i);
       dirfp=theta(i);
       dirfp12=theta12(i);
       dirfp13=theta13(i);
       dirfpm=thetam(i);
       dirfp21=theta21(i);
       dirfp22=theta22(i);
       dirfpm2=thetam2(i);
       dd=[dirfp dirfp12 dirfp13 dirfpm dirfp21 dirfp22 dirfpm2] 
   end
end
%----------------------------------------------------
%Teste utilizando o espectro de uma serie de ondas  %=>NOVO
%----------------------------------------------------
%especx........espectro X
%Mo............´area interna do espectro X
%Hs............altura significativa calculada a partir do espectro

espectro=espec(hv,dt);
especx=espectro(:,2);
especx=alisa2(especx);
mo=integral(reg2,fc,especx);
Hs=4.01*sqrt(mo);


%Armazena resultados
theta=theta';
f=f';
s=s';
kk=kk';
r=r';

dadosteste=[theta f especx' s kk r];

% save d:\users\joao\estagiarios\eduardo\dadosteste1.txt -ascii dadosteste 
% save d:\users\joao\estagiarios\eduardo\dirfp1.txt -ascii dirfp
