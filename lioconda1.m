%PROGRAMA ROGER1A.m
%experimentos com um arquivo raw do
%waverider de arraial do cabo

% o intervalo de amostragem é de .78125 
%e  N=1536 (em verdade 1535)
%são 1200 segundos de observação

%leitura do arquivo bruto
a=csvread('08100107.raw');

%o heave vem em cm
b2=a(:,2)/100;
%deslocamento EW
b3=a(:,3)/100;
%deslocamento NS
b4=a(:,4)/100;

%leitura do arquivo spt
b=csvread('08100107.spt',0,0);
%espectro
param=b(1:12,1);
espb=b(13:end,2);
cal=b(4,1);
espb=espb*cal;
	
%frequencias
fa=b(13:end,1);

%direção principal;
dirpb=b(13:end,3);
dirpb=dirpb-23;

%correção da declinação
g1=find(dirpb<0);
dirpb(g1)=dirpb(g1)+360;
%spread
sprb=b(13:end,4);

%cálculos com as séries brutas sem a 
%média e com 1536 pontos
b2=b2-mean(b2);b2=[b2;0];
b3=b3-mean(b3);b3=[b3;0];
b4=b4-mean(b4);b4=[b4;0];

f1=1/1200:1/1200:0.64;

m4=2*0.78125/1536;
z41=fft(b2);z41=z41(2:769);
z42=fft(b3);z42=z42(2:769);
z43=fft(b4);z43=z43(2:769);

zz=zeros(768,6);
zz(:,1)=m4*z41.*conj(z41);
zz(:,2)=m4*imag(z41.*conj(z42));
zz(:,3)=m4*imag(z41.*conj(z43));
zz(:,4)=m4*z42.*conj(z42);
zz(:,5)=m4*z43.*conj(z43);
zz(:,6)=m4*real(z42.*conj(z43));

for kk=1:6,
q1=reshape(zz(3:764,kk),6,127);q1=mean(q1);
q2=reshape(zz(6:761,kk),12,63);q2=mean(q2);
zz(1:64,kk)=real([q1(5:19)';q2(10:58)']);
end;

zz=zz(1:64,:);
espt=zz(:,1);	

c0=zz(:,3)+j*zz(:,2);
c0=angle(c0)*360/(2*pi);
c0=c0+90-23;
g1=find(c0<0);c0(g1)=c0(g1)+360;
g1=find(c0>360);c0(g1)=c0(g1)-360;
dirpt=c0;

%cálculo do spread;
check=sqrt(zz(:,1).*(zz(:,4)+zz(:,5)));

q1=zz(:,3)./check;q2=zz(:,2)./check;
q=sqrt(q1.^2+q2.^2);
sprt=sqrt(2-2*q);sprt=sprt*57.3;

heave=b2;
etaEW=b3;etaNS=b4;

%os valores de direção principal, nos dois casos,
%bóia e terra estão corrigidos da declinação magnética

%falta Hs para comparação