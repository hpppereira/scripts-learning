%CODE daatmarlimwavelet2009.m calculates the main direction
%for each segment; the formula of Lygre and Krogstad is used
%  y=2;
%  a1=aa1(y+1,:);
%  a2=aa2(y+1,:);
%  a3=aa3(y+1,:);

a1=filter((out1+1i*out3)',1,co);
a2=filter((out1+1i*out3)',1,dd);
a3=filter((out1+1i*out3)',1,dc);%
a1=a1(m:1536);
a2=a2(m:1536);
a3=a3(m:1536);
% a11=filter(out1+j*out3,1,co);
% sf11
% a11=a11(m+1:1024);
% a12=filter(out1-j*out3,1,dd);
% a12=a12(m+1:1024);
% a13=filter(out1-j*out3,1,dc);
% a13=a13(m+1:1024);
% 
z41=a1;z42=a2;z43=a3;
a4=m4*(z41.*conj(z41));
a8=m4*imag(z41.*conj(z42));
%a88=m4*imag(a11.*conj(12));
a9=m4*imag(z41.*conj(z43));

%z41=a1w;z42=a2w;z43=a3w;
%a4w=(z41.*conj(z41));
%a8w=imag(z41.*conj(z42));
%a9w=imag(z41.*conj(z43));
%sf11

a20=m4*(z42.*conj(z42));
a21=m4*(z43.*conj(z43));

a25=a20+a21;
a7=sqrt(a4.*a25);

a12=m4*real(z42.*conj(z43));

c0=a9+1i*a8;

c1=c0./a7;
	
c0=angle(c0)*360/(2*pi);
c0=ceil(c0);
c00=find(c0<=0);c0(c00)=c0(c00)+360;
c000=270-c0-23;g=find(c000<=0);c000(g)=c000(g)+360;

c2=(a20-a21+1i*2*a12)./a25;

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
%tet2=grad1*c0';
%a15=ceil(tet2*360/(2*pi));
%a15=90+a15-22;
%g=find(a15>360);a15(g)=a15(g)-360;






