%CODE daatwaverider21w calculates the main direction
%for each segment with wavelet (morlet type);
%the formulatuio of Lygre and Krogstad is used

%usa-se a convolu��o com a wavelet complexa
a1=filter((out1-1i*out3)',1,co);
a2=filter((out1-1i*out3)',1,dd);
a3=filter((out1-1i*out3)',1,dc);

m4=2*dt/(m*0.375);
a1=a1(m:1200); %1024
a2=a2(m:1200);
a3=a3(m:1200);

%espectros cruzados
z41=a1; z42=a2; z43=a3;
a4=m4*(z41.*conj(z41));
a8=m4*imag(z41.*conj(z42));
a9=m4*imag(z41.*conj(z43));

a20=m4*(z42.*conj(z42));
a21=m4*(z43.*conj(z43));

a25=a20+a21;
a7=sqrt(a4.*a25);

a12=m4*real(z42.*conj(z43));

%a8 � o coseno, proje��o no eixo W-E;
%a9 � seno proje��o no eixo S-N;
% o �ngulo c0 calculado � em rela��o ao eixo horizontal

c0=a8+j*a9;

c1=c0./a7;

c01=cos(c0);c02=sin(c0);           % Novos Parente
c03=angle(mean(c01)+j*mean(c02));  %
c03=ceil(c03*360/(2*pi));          %  

c2=(a20-a21+1i*2*a12)./a25;
c0=angle(c0)*360/(2*pi);
c0=ceil(c0);

c00=find(c0<=0);c0(c00)=c0(c00)+360;
pq=ceil(mean(c0));                 % Novos Parente 
pq=c03;                            %
g=find(pq<=0);pq(g)=pq(g)+360;     %

p1=(c1-c2.*conj(c1))./(1-(abs(c1)).^2);
p2=c2-c1.*p1;

tet2=zeros(1,m3+2);

%in order to avoid the ambiguity caused by 2teta the main 
%direction calculated by Fourier techniques is used 
%as a reference; the mem value is calculated in an interval
%of 100 degrees around this value;

%c�lculation for each segment
for kl=1:m3+2,
   p3=ceil(c0(kl));
   %p3=31;   
   d=(p3:p3+100);

   z1=1-p1(kl)*a26(d)-p2(kl)*a27(d);
   z1=z1.*conj(z1);z1=z1';
   %m�nimum of denominator is sufficient to
   %determine the maximum
     
   p5=find(z1==min(z1));p5=p5(1);
   p7=a30(p3+p5-1);
   %main direction (mem) for each segment
   tet2(1,kl)=grad1*p7;
   %z1=1./z1;z1=z1/max(z1);
   %if iwq==5,memarq(d',kl)=z1;arqc0(kl)=c0(kl);end;
   
end;


%spectrum for each segment
sp2=a4';

% sp5=sp2/max(sp2);
% tet6=90+tet2*180/pi-21;
% %tet6=tet6(sp5>0.5);
% sp5=sp2/max(sp2);
% g=find(tet6<=0);
% tet6(g)=tet6(g)+360;
% g=find(tet6>360);
% tet6(g)=tet6(g)-360;
% 
% [n1 n2]=hist(tet6,10);
% g=find(n1==max(n1));
% dire(iwq,kkl)=n2(g(1));
% espe(iwq,kkl)=ww55(iwq+1);

% teste14;
% g=find(x1==max(x1));

% %tet2=c0*grad1;
% 
% y=zeros(360,1530);
% y(1:50,:)=memarq(411:460,:);
% y(1:360,:)=y(1:360,:)+memarq(51:410,:);
% y(311:360,:)=y(311:360,:)+memarq(1:50,:);
% 
% xz=y(:,1);
% for k=2:length(y),
%    xz=xz.*(y(:,k)+ones(360,1));end;
% g=find(xz==max(xz));g=g(1);


%  x=sum(memarq');x=x';
%  y=zeros(360,1);
%  y(1:50)=x(411:460);
%  y(1:360)=y(1:360)+x(51:410);
%  y(311:360)=y(311:360)+x(1:50);
%  memy(:,kkl)=y; 
%  v6=find(y==max(y));v6=v6(1);
%  v6=90+v6-21;
%  if v6>200,v6=v6-360;end;
%  dire(5,kkl)=v6;

%[n1 n2]=butter(6,0.051);
% sp3=sp2/max(sp2);  
%g=find(tet4>360);tet4(g)=tet4(g)-360;
%[n1 n2]=hist(tet2,20);
% %   g=find(n1==max(n1));g=g(1);
% %if iwq>1,  
%   %  c0=c0*2*pi/360;

%  v3=mean(cos(tet2));v4=mean(sin(tet2)); 
%  v5=angle(v3+j*v4);
%  v5=v5*360/(2*pi); % 
%  v5=90+v5-21;
%  if v5<0,v5=v5+360;end
%  dire(iwq,kkl)=v5;
%  espe(iwq,kkl)=ww55(iwq+1); 
