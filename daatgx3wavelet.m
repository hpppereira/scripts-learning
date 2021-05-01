% daatgx3wavelet.m calculates tet2 e sp2 for 3 series:
%aceleracao, pitch e roll do gx3

% eta=acos(fase);
% veloc=-awsen(fase);
% acele=-aw2cos(fase);
% pitch=-akcos(teta)sen(fase);
% roll= -aksen(teta)sen(fase);
% espectros cruzados:
% acel-pitch=imag(a2w2kcos(teta));
% acel-roll =imag(a2w2ksen(teta));
% teta=artg(acel-roll/acel-pitch);

%out1 é a wavelet coseno e out3 a wavelet seno

%aplica wavelets para as 3 series
a1=filter((out1-j*out3)',1,co);
a2=filter((out1-j*out3)',1,dd);
a3=filter((out1-j*out3)',1,dc);

%series após a convoluução
a1=a1(m:1024);
a2=a2(m:1024);
a3=a3(m:1024);

z41=a1;z42=a2;z43=a3;

%espectros brutos e cruzados
a4=m4*(z41.*conj(z41));
a8=m4*imag(z42.*conj(z41));
a9=m4*imag(z43.*conj(z41));

a20=m4*(z42.*conj(z42));
a21=m4*(z43.*conj(z43));

%soma dos dois espectros:a2k2; a7=sqrt(a4w4k2);
a34=a20+a21;
a7=sqrt(a4.*a34);
%espectro cruzado dos dois slopes
a12=m4*real(z42.*conj(z43));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%as seguintes operações serao feitas caso seja 
%necessario calcular parametros usando apenas os slopes 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %cálculo do espectro de aceleração
% %soma dos dois espectros=a2k2;dividindo por k2 da a2
% %espectro de aceleração
% g2=9.81^2;
% %k2=w4/g2 (teoria linear)
% esgama=g2*a34/w4;
% 
% %calculo do seno de 2teta
% 
% %espectro cruzado dos dois slopes:a2k2sen(teta)cos(teta)
% a12=m4*real(z42.*conj(z43));
% 
% %sen2(2teta)
% a36=2*a12./a34;
% %cos2(teta)
% a37=(a20-a21)./a34;  
% 
% a38=sqrt(a20./a34);
% a40=a20./a34;
% a39=sqrt(a21./a34);
% a41=a21./a34;
% %teta obtido de sqrt(sen2(teta)/cos2(teta)) - no primeiro
% %quadrante
% a42=angle(a38+j*a39);
% 
% %2teta obtido de sen(2teta) e cos(2teta)  
% a43=angle(a37+j*a36)*180/pi;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%cálculo da direção principal a partir de Kuik (sen(teta)/cos(teta))
c0=a8+j*a9;
c1=c0./a7;
	
c0=angle(c0)*360/(2*pi);
c0=ceil(c0);
c00=find(c0<=0);c0(c00)=c0(c00)+360;
c000=270-c0-23;g=find(c000<=0);c000(g)=c000(g)+360;

%cálculo da direção principal por maxima entropia (Bill O'Reilly)
%maxima entropia

c2=(a20-a21+j*2*a12)./a34;
p1=(c1-c2.*conj(c1))./(1-(abs(c1)).^2);
p2=c2-c1.*p1;

tet2=zeros(1,m3+2);

%in order to avoid the ambiguity caused by 2teta the main 
%direction calculated by Fourier techniques is used 
%as a reference; the mem value is calculated in an interval
%of 100 degrees around this value;

%cálculation for each segment
for kl=1:m3+2,
   p3=ceil(c0(kl));d=(p3:p3+100);

   z1=1-p1(kl)*a26(d)-p2(kl)*a27(d);
   z1=z1.*conj(z1);z1=z1';
   %mínimum of denominator is sufficient to
   %determine the maximum
     
   p5=find(z1==min(z1));p5=p5(1);
   p7=a30(p3+p5-1);
   %main direction (mem) for each segment
   tet2(1,kl)=grad1*p7;
   
end;

%spectrum for each segment
sp2=a4';






