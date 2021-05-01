clear,clc
load bmo.mat

%programa para sincronizar os dados da triaxis com os do microstrain
%vetor de tempo d o gx3
x3=1:1024;
%vetor de tempo da axys iniciando no zero (60.16 eh o tempo inicial da axys)
x0=axys_time(1,:)-60.16;
%novo matriz para triaxys (vetores corrigidos?)
novotri=zeros(9,1024);

%variando a quantidade de arquivos
for k=1:9,
    %x1=x0(k,:);
    for i=1:1024,
        x4=x3(i)-x0;x4=abs(x4);
        [a1 a2]=sort(x4);
        a3=a2(1:2);
        novotri(k,i)=(axys_heave(k,a3(1))+axys_heave(k,a3(2)))/2;
    end;
end;

%usando os dois slopes
n1=gx3_ac_NS(4,:);
n2=gx3_ac_EW(4,:);
f=1/64:1/64:32/64;%frequencia para 32 valores de frequencia
w3=(2*pi.*f').^2;%omega ao quadrado
w2=w3.^2;%omega a quarta
sn1=spectrum(n1,64);sn1=2*sn1(2:33,1);
sn2=spectrum(n2,64);sn2=2*sn2(2:33,1);
%aqui a soma dos dois espectros e igual a a2k2
%para o calculo de a2 (espectro de heave)
%a soma precisa ser dividido por k2 (k ao quadrado) 
%k=w2/gtanh(kd);%transcendental, pode ser resolvida
%de forma simplificada. k2=w2/g^2.tanh(kd)^2
%calculo de tgh(kd) por formula simplificada de Eckart
g=9.81;d=22;
t=1./f;
p1=g*t.^2/(2*pi);
p2=tanh(d*2*pi./p1);
%calculo do comprimento de onda
lambda=p1.*sqrt(p2);
tt1=tanh(2*pi*d./lambda);

%formula de Eckart por Holthuisen
% kd=alfa(tanh(alfa)^(-1/2); alfa=k0d=w3*d/gf1alfa=w3*d/g;
alfa=w3*d/g;
kd=alfa.*tanh(alfa).^(-1/2);
tt2=tanh(kd);

%formuls de Fenton (Holthuisen)
beta=kd;
kd=(alfa+beta.^2.*cosh(beta).^(-2))/(tanh(beta)+beta.*cosh(beta).^(-2));
tt3=tanh(kd);

%usando o espectro do triaxis para correcao
%espectro de heave do triaxis
sn3=spectrum(novotri(1,:),64);sn3=2*sn3(2:33,1);
novok=sqrt((sn1+sn2)./sn3);
tt3=tanh(novok*d);

%calculo da correcao;
k2=w2./(g^2.*tt1'.^2);k3=w2./(g^2.*tt3.^2);
k=sqrt(k2);

%a2=espectro de heave
a2=(sn1+sn2)./k2;
a3=(sn1+sn2)./k3;

%usando o espectro da bmo para obter o k
sn4=spectrum(gx3_ac_V(4,:),64);sn4=2*sn4(2:33,1);
novok1=sqrt((sn1+sn2)./sn4);
tt4=tanh(novok1*d);

%calculo da correcao;
k4=w2./(g^2.*tt4.^2);
a4=(sn1+sn2)./k4;
a5=sn4./w2;

%spectrum de heave do triaxys
dt=1024/1382;
f1=1/(64*dt):1/(64*dt):32/(64*dt);
q=spectrum(axys_heave(1,1:1024),64);q=2*0.741*q(2:33,1);
d=4:32;