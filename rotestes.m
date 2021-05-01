%Rotina de testes de sistemas de onda direcional

clc %limpar tela
clear,clc

%Inicializaçao de constantes

reg=1024;
reg2=fix(reg/2);
gl=50;
dt=1.0;
donv=270;

%Entrada dos dados
arqin = 'registro50';
arqdat = [arqin, '.txt']
eval(['load ', arqdat])
eval(['hv= ',arqin,'(:,1);'])
eval(['ptx = ',arqin,'(:,2);'])
eval(['pty= ',arqin,'(:,3);'])
eval(['ptxx= ',arqin,'(:,4);'])
eval(['ptyy= ',arqin,'(:,5);'])

%--Dados de entrada--
%hv = vetor de heave
%ptx = vetor de pitch x
%pty = vetor de pitch y
%ptxx = vetor de pith xx
%ptyy = vetor de pith yy 
%reg = numero de pontos
%donv = direçao do eixo de origem em relaçao ao N.V.
%gl = graus de liberdade
%dt = taxa de amostragem

%--Dados de saida--
%fpico = frequencia de pico
%dirfp = direçao principal na frequencia de pico
%theta = vetor de direçao principal
%thetom = direçao media considerando todas as frequencias 
%ui = indice de unidiretividade

%--Variaveis internas--
%i = contador
%fc = frequencia de corte
%deltaf = incremento em frequencia 
%reg2 = numero de pontos em frequencia
%gl2 = metade do numero de graus de liberdade
%x1,y1...z6 = vetores reais e imaginarios
%zn1 - zn50 = coeficientes de fourier
%autn1,autn2,autn3,... = vetro do espectro
%qd__ = vetor do quadspectro entre dois pontos
%co__ = vetor do coespectro entre dois pontos
%fase__ = vetor de fase entre dois pontos
%s = vetor parametro de espalhamento
%f = frequencia
%k = vetor numero de onda
%kk = numero de onda (teoria linear)
%r = razao kk/k
%a1,b1,a2,b2, = coeficientes de fourier
%intauxc,intauxs,intautn1 = integrais do calculo de thetom
%auxc, auxs = vetores auxiliares para calculo de thetom
%a,b variaveis utilizadas para calculo de thetom
%thetaux = variael auxiliar para calculo de thetom
%spico = ordenada espectral na frequencia de pico

%--Inicializaçao de variaveis--

temp=2.*dt;
fc=1/temp;
deltaf=fc*2/reg;
gl2=fix(gl/2);
spico=35;

%--Inicializa os vetores para a rotina de FFT--

for i=1:reg;
    z1(i)=hv(i);
    %z3(i)=hv2(i);
    %z5(i)=hv3(i);
    x1(i)=ptx(i);
    y1(i)=pty(i);
    xx1(i)=ptxx(i); 
    yy1(i)=ptyy(i); 
    z2(i)=0;
    z4(i)=0;
    z6(i)=0;
    x2(i)=0;
    y2(i)=0;
    xx2(i)=0; 
    yy2(i)=0; 
end

%Transformada Discreta de Fourier
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

aa=fft(xx1); 
xx1=real(aa);
xx2=imag(aa);

aa=fft(yy1); 
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
    zn19(i)=x2(i)*xx1(i); 
    zn20(i)=x1(i)*xx2(i); 
    zn21(i)=x2(i)*yy1(i); 
    zn22(i)=x1(i)*yy2(i); 
    zn23(i)=y2(i)*xx1(i); 
    zn24(i)=y1(i)*xx2(i); 
    zn25(i)=y2(i)*yy1(i); 
    zn26(i)=y1(i)*yy2(i); 
    zn27(i)=xx1(i)*xx1(i);
    zn28(i)=xx2(i)*xx2(i);
    zn29(i)=yy1(i)*yy1(i);
    zn30(i)=yy2(i)*yy2(i);
    zn31(i)=xx2(i)*yy1(i);
    zn32(i)=xx1(i)*yy2(i);
    zn33(i)=xx1(i)*yy1(i);
    zn34(i)=xx2(i)*yy2(i);
    zn35(i)=x1(i)*xx1(i); 
    zn36(i)=x2(i)*xx2(i); 
    zn37(i)=y1(i)*yy1(i); 
    zn38(i)=y2(i)*yy2(i); 
    zn39(i)=y1(i)*xx1(i); 
    zn40(i)=y2(i)*xx2(i); 
    zn41(i)=y1(i)*yy1(i); 
    zn42(i)=y2(i)*yy2(i); 
    zn43(i)=z2(i)*xx1(i); 
    zn44(i)=z1(i)*xx2(i); 
    zn45(i)=z2(i)*yy1(i); 
    zn46(i)=z1(i)*yy2(i); 
    zn47(i)=z1(i)*xx1(i);%?
    zn48(i)=z2(i)*xx2(i);%?
    zn49(i)=z1(i)*yy1(i);%?
    zn50(i)=z2(i)*yy2(i);%?
end

%Alisamento do espectro
zn1=alisa(zn1);
zn2=alisa(zn2);
zn3=alisa(zn3);
zn4=alisa(zn4);
zn5=alisa(zn5);
zn6=alisa(zn6);
zn7=alisa(zn7);
zn8=alisa(zn8);
zn9=alisa(zn9);
zn10=alisa(zn10);
%zn11=alisa(zn11);
%zn12=alisa(zn12);
%zn13=alisa(zn13);
%zn14=alisa(zn14);
zn15=alisa(zn15);
zn16=alisa(zn16);
zn17=alisa(zn17);
zn18=alisa(zn18);
zn19=alisa(zn19);
zn20=alisa(zn20); 
zn21=alisa(zn21);
zn22=alisa(zn22);
zn23=alisa(zn23);
zn24=alisa(zn24);
zn25=alisa(zn25);
zn26=alisa(zn26);
zn27=alisa(zn27);
zn28=alisa(zn28);
zn29=alisa(zn29);
zn30=alisa(zn30);
zn31=alisa(zn31);
zn32=alisa(zn32);
zn33=alisa(zn33);
zn34=alisa(zn34);
zn35=alisa(zn35);
zn36=alisa(zn36);
zn37=alisa(zn37);
zn38=alisa(zn38);
zn39=alisa(zn39);
zn40=alisa(zn40);
zn41=alisa(zn41);
zn42=alisa(zn42);
zn43=alisa(zn43);
zn44=alisa(zn44);
zn45=alisa(zn45);
zn46=alisa(zn46);
zn47=alisa(zn47);
zn48=alisa(zn48);
zn49=alisa(zn49);
zn50=alisa(zn50);

%Zera vetores
for i=1:reg2;
    autn1(i)=0;
   % autn2(i)=0;
   % autn3(i)=0;
    qdn1ew(i)=0;
    qdn1ns(i)=0;
    qdn1xx(i)=0;
    qdn1yy(i)=0;
    qdewxx(i)=0; 
    qdewyy(i)=0; 
    qdnsxx(i)=0; 
    qdnsyy(i)=0; 
    qdnews(i)=0; 
    qdxxyy(i)=0; 
    coewew(i)=0;
    consns(i)=0;
    coxxxx(i)=0; 
    coyyyy(i)=0; 
    conews(i)=0; 
    coxxyy(i)=0; 
    coewxx(i)=0; 
    coewyy(i)=0; 
    consxx(i)=0; 
    consyy(i)=0;
    con1xx(i)=0;
    con1yy(i)=0;
    theta(i)=0; 
    theta12(i)=0;
    theta13(i)=0;
    theta21(i)=0;
    theta22(i)=0;
    thetam(i)=0;
    auxc(i)=0;
    auxs(i)=0;
    k(i)=0;
    kk(i)=0;
    s(i)=0;
    r(i)=0;
    faseew(i)=0;
    fasens(i)=0;
    fasenews(i)=0;
    fasen1xx(i)=0; 
    fasen1yy(i)=0; 
    fasexxyy(i)=0; 
    faseewxx(i)=0; 
    faseewyy(i)=0; 
    fasensxx(i)=0; 
    fasensyy(i)=0; 
end

%Calcula espectros derivados
for i=1:reg2;
    autn1(i)=2*dt/reg*(zn1(i)+zn2(i));
    %autn2(i)=2*dt/reg*(zn11(i)+zn12(i));
    %autn3(i)=2*dt/reg*(zn13(i)+zn14(i));
    qdn1ew(i)=2*dt/reg*(zn3(i)-zn4(i));
    qdn1ns(i)=2*dt/reg*(zn5(i)-zn6(i));
    qdn1xx(i)=2*dt/reg*(zn43(i)-zn44(i)); 
    qdn1yy(i)=2*dt/reg*(zn45(i)-zn46(i)); 
    qdewxx(i)=2*dt/reg*(zn19(i)-zn20(i)); 
    qdewyy(i)=2*dt/reg*(zn21(i)-zn22(i)); 
    qdnsxx(i)=2*dt/reg*(zn23(i)-zn24(i)); 
    qdnsyy(i)=2*dt/reg*(zn25(i)-zn26(i)); 
    coewew(i)=2*dt/reg*(zn7(i)+zn8(i));
    consns(i)=2*dt/reg*(zn9(i)+zn10(i));
    coxxxx(i)=2*dt/reg*(zn27(i)+zn28(i)); 
    coyyyy(i)=2*dt/reg*(zn29(i)+zn30(i)); 
    qdnews(i)=2*dt/reg*(zn15(i)-zn16(i));
    qdxxyy(i)=2*dt/reg*(zn31(i)-zn32(i)); 
    conews(i)=2*dt/reg*(zn17(i)+zn18(i));
    coxxyy(i)=2*dt/reg*(zn33(i)+zn34(i)); 
    coewxx(i)=2*dt/reg*(zn35(i)+zn36(i)); 
    coewyy(i)=2*dt/reg*(zn37(i)+zn38(i)); 
    consxx(i)=2*dt/reg*(zn39(i)+zn40(i)); 
    consyy(i)=2*dt/reg*(zn41(i)+zn42(i)); 
    con1xx(i)=2*dt/reg*(zn47(i)+zn48(i));
    con1yy(i)=2*dt/reg*(zn49(i)+zn50(i));
 
    k(i)=sqrt((coewew(i)+consns(i))/autn1(i));
    
    faseew(i)  =atan(qdn1ew(i)/coewew(i))*180/pi;
    fasens(i)  =atan(qdn1ns(i)/consns(i))*180/pi;
    fasenews(i)=atan(qdnews(i)/conews(i))*180/pi;
    fasen1xx(i)=atan(qdn1xx(i)/coxxxx(i))*180*pi; 
    fasen1yy(i)=atan(qdn1yy(i)/coyyyy(i))*180*pi; 
    fasexxyy(i)=atan(qdxxyy(i)/coxxyy(i))*180*pi; 
    faseewxx(i)=atan(qdewxx(i)/coewxx(i))*180*pi; 
    faseewyy(i)=atan(qdewyy(i)/coewyy(i))*180*pi; 
    fasensxx(i)=atan(qdnsxx(i)/consxx(i))*180*pi; 
    fasensyy(i)=atan(qdnsyy(i)/consyy(i))*180*pi; 
end

%Calcula direcao principal
for i=1:reg2
    if autn1(i)>0.0000000001

        %Coeficientes de primeira ordem
        a1 =(1/pi)*qdn1ew(i)/(autn1(i)*k(i));
        a12=(4/(3*pi))*qdewxx(i)/(autn1(i)*k(i)^3);
        a13=(4/pi)*qdewyy(i)/(autn1(i)*k(i)^3); 
   
        b1 =(1/pi)*qdn1ns(i)/(autn1(i)*k(i));  
        b12=(4/(3*pi))*qdnsyy(i)/(autn1(i)*k(i)^3); 
        b13=(4/pi)*qdnsxx(i)/(autn1(i)*k(i)^3); 
        
       
        %coeficientes de  ordem
        a21=2/pi*((con1xx(i)/(autn1(i)*k(i)^2))+1/2);
        a22=-2/pi*((con1yy(i)/(autn1(i)*k(i)^2))+1/2);
        
        b2 =2/pi*(conews(i)/(autn1(i)*k(i)^2));
        
        a23 = 2/pi*((consns(i)/(autn1(i)*k(i)^2))-1/2);
        a24 = 2/pi*((coewew(i)/(autn1(i)*k(i)^2))-1/2);
        a25 = 2/pi*((coyyyy(i)/(autn1(i)*k(i)^4))-3/8);
        a26 = 2/pi*((coxxxx(i)/(autn1(i)*k(i)^4))-3/8);

        aa1(i) = a1;
        aa12(i) =a12;
        aa13(i)= a13;
          
        bb1(i) = b1;
        bb12(i) = b12;
        bb13(i) = b13;

        aa21(i) = a21;
        aa22(i) = a22;
        aa23(i) = a23;
        aa24(i) = a24;
        aa25(i) = a25;
        aa26(i) = a26;
            
        bb2(i)= b2;
        
        %media dos coeficientes
        am1=(a1+a12+a13)/3;
        bm1=(b1+b12+b13)/3;
        bm2=b2;
        am2=(a21+a22)/2;
        
        %Theta utilizando os coeficientes de primeira ordem      
        theta(i)=cortheta(a1,b1,donv);
        theta12(i)=cortheta(a12,b12,donv);
        theta13(i)=cortheta(a13,b13,donv);
        thetamm(i) = (theta(i)+theta12(i)+theta13(i))/3;
        %thetam(i)=cortheta(am1,bm1,donv);

        %Theta utilizando os coeficientes de segunda ordem
        theta21(i)=cortheta(a21,b2,donv);
        theta22(i)=cortheta(a22,b2,donv);
        theta23(i)=cortheta(a23,b2,donv);
        theta24(i)=cortheta(a24,b2,donv);
        theta25(i)=cortheta(a25,b2,donv);
        theta26(i)=cortheta(a26,b2,donv);
        
               
        thetam2(i)=(theta21(i)+theta22(i)+theta23(i)+theta24(i)+theta25(i)+theta26(i))/6;
        
        thetaux=atan(b1/a1);
        auxc(i)=autn1(i)*cos(thetaux);
        auxs(i)=autn1(i)*sin(thetaux);

        %Espalhamento angular
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
   maxautn1 = max(autn1);
   if autn1(i)==maxautn1;
       aa21max = aa21(i);
       aa22max = aa22(i);
       aa23max = aa23(i);
       aa24max = aa24(i);
       aa25max = aa25(i);
       aa26max = aa26(i);
       bb2max = bb2(i);
       
       abfp = [aa21max aa22max aa23max aa24max aa25max aa26max bb2max];
      
       fpico=f;
       spico=autn1(i);
       dirfp=theta(i);
       dirfp12=theta12(i);
       dirfp13=theta13(i);
       dirfpm=thetamm(i);
       dirfp21=theta21(i);
       if dirfp>=10 & dirfp<=120;
           dirfpc21 = ((-0.4982)*dirfp21)+131.41;
       end
       if dirfp>=130 & dirfp<=310;
           dirfpc21 = ((-0.4983)*dirfp21)+314.31;
       end
       if dirfp>=320 & dirfp<=350
           dirfpc21 = ((-0.583)*dirfp21)+523.37;
       end
       
       dirfp22=theta22(i);
       if dirfp>=10 & dirfp<=120;
           dirfpc22 = ((-0.4967)*dirfp22)+131.9;
       end
       if dirfp>=130 & dirfp<=310;
           dirfpc22 = ((-0.4972)*dirfp22)+314.1;
       end
       if dirfp>=320 & dirfp<=350
           dirfpc22 = ((-0.5132)*dirfp22)+498.33;
       end

       dirfp23=theta23(i);
       
       if dirfp>=10 & dirfp<=120;
           dirfpc23 = ((-0.4986)*dirfp23)+131.9;
       end
       if dirfp>=130 & dirfp<=310;
           dirfpc23 = ((-0.4991)*dirfp23)+314.45;
       end
       if dirfp>=320 & dirfp<=350
           dirfpc23 = ((-0.5696)*dirfp23)+518.45;
       end
       
       dirfp24=theta24(i);

       if dirfp>=10 & dirfp<=120;
           dirfpc24 = ((0.4986)*dirfp24)-47.601;
       end
       if dirfp>=130 & dirfp<=310;
           dirfpc24 = ((0.4991)*dirfp24)+134.78;
       end
       if dirfp>=320 & dirfp<=350
           dirfpc24 = ((-0.5696)*dirfp24)+313.4;
       end
       
       dirfp25=theta25(i);
       
       if dirfp>=10 & dirfp<=140;
           dirfpc25 = ((-0.5177)*dirfp25)+134.77;
       end
       if dirfp>=150 & dirfp<=320;
           dirfpc25 = ((-0.4962)*dirfp25)+314.51;
       end
       if dirfp>=320 & dirfp<=350
           dirfpc25 = ((-1.0017)*dirfp25)+649.78;
       end
       
       dirfp26=theta26(i);

       if dirfp>=10 & dirfp<=120;
           dirfpc26 = ((0.4933)*dirfp26)-46.062;
       end
       if dirfp>=130 & dirfp<=300;
           dirfpc26 = ((0.5105)*dirfp26)+132.85;
       end
       if dirfp>=310 & dirfp<=350
           dirfpc26 = (0.6838*dirfp26)+307.11;
       end

       
       dirfpm2=thetam2(i);
       format bank
       dfp = [dirfp dirfp12 dirfp13 dirfpm dirfpc21 dirfpc22 dirfpc23 dirfpc24 dirfpc25 dirfpc26]
   end
   
end

%Teste utilizando o espectro de uma serie de ondas 

%especx = espectro X
%Mo = area interna do espectro X
%Hs = altura significativa calculada a partir do espectro

espectro=espec(hv,dt);
especx=espectro(:,2);
especx=alisa(especx);
mo=integral(reg2,fc,especx);
Hs=4.01*sqrt(mo);

%Imrpime dados 

% figure(1)
% plot(f,thetamm,'b',f,theta,'y', f,theta12,'g', f,theta13,'r')
% %plot(f,thetamm,'b')
% title('theta')
% xlabel('frequencia')
% ylabel('angulo')
% legend('thetamm','theta','theta12','theta13')
% %legend('thetamm')
% 
% figure(2)
% plot(f,aa1,'b',f,bb1,'b',f,aa12,'g',f,bb12,'g',f,aa13,'r',f,bb13,'r')
% title('a e b')
% xlabel('frequencia')
% legend('a1','b1','a12','b12','a13','b13')
% 
% figure(3)
% plot(f,especx,'.-')
% title('espectro unidirecional')
% xlabel('frequencia')
% ylabel('DEP')
% 
% figure (4)
% plot(f,aa1,':b',f,aa12,':g',f,aa13,':r',f,aa21,'b',f,aa22,'g',f,aa23,'y',f,aa24,'k',f,aa25,'c',f,aa26,'m',f,bb2,'r')
% %plot(f,aa24,'k',f,aa26,'m', f,bb2,'b',f,bb12,'y',f,bb13,'g')
% %  title('a2 e b2')
% legend('a1','a12','a13','a21','a22','a23','a24','a25','a26','b2')
% 
% figure(5)
% plot(f,theta21,'b', f,theta22,'g', f,theta23,'r', f,theta24,'m', f,theta25,'k', f,theta26,'y',f,thetam2,':r')
% %plot(f,thetam2,'k')
% title('theta')
% xlabel('frequencia')
% ylabel('angulo')
% legend('theta21', 'theta22', 'theta23', 'theta24', 'theta25', 'theta26','thetam2')
% %legend('thetam2')
% % figure(6)
% % plot(ptx,'r')
% % hold on
% % plot(pty,'b')
% 
% % figure(4)
% % subplot(2,1,1)
% % plot(f,k)
% % title('numero de onda')
% % subplot(2,1,2)
% % plot(f,r)
% % title('check ratio')
% % xlabel('frequencia')
% 
% %Armazena resultados

theta=theta';
theta12=theta12';
theta13=theta13';
thetam=thetam';
f=f';
s=s';
kk=kk';
r=r';

%Saida dos dados
saidateste=[theta theta12 theta13 thetam f especx s kk r];

%Salva arquivo
%csvwrite('21dirfp340.txt',dirfpc21)