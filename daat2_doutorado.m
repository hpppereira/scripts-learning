%CODE daatgx322a.m to select the segments for
%the directional spectrum composition
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Prepared by C.E. Parente 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Preparing ensembles of m/2 segments advancing one sample
fr3=[];fr4=[];
%fr3 ia a matrix with the segments whose direction
%stability will be investigated
%fr4 is the spectrum matrix
%mq=round(m/2);
for ip=1:mq,

   fr3=[fr3;tet2(ip:m1-(mq-ip))];
   fr4=[fr4;sp2(ip:m1-(mq-ip))];
end;

%using the mean and the standard circular deviation
%to select the segments with a given stability
fr2a=mean(cos(fr3));fr2b=mean(sin(fr3));
r=sqrt(fr2a.^2+fr2b.^2);
%circular deviation
fr9=sqrt(2*(1-r));
%mean
fr2=angle(fr2a+j*fr2b);
g=find(fr2<0);
fr2(g)=fr2(g)+2*pi;

fr7=angle(mean(fr2a)+j*mean(fr2b));
fr7=fr7*360/(2*pi);
%fr7=270-fr2*360/(2*pi)-22;

a15=0;

%segments with values of the standard deviations smaller
%than the threshold are selected
zm=0.5;
b7=find(fr9<zm);
a15=fr2(b7);
er4=mean(fr4(:,b7));
ffr4=std(fr4(:,b7));
compa15(kkl,iwq)=length(a15);
a16=a15;

%Correcting for declination
% a15 is the the final vector with selected direction values 
a15=ceil(a15*360/(2*pi));
a15=270-a15-22;

g=find(a15>0);a15(g)=a15(g)-360;
g=find(a15<0);a15(g)=a15(g)+360;

w1=zeros(360,1);%direção principal
w2=zeros(360,1);%ocorrências

if length(a15)>1,%caso existam valores selecionados
   b1=find(a15<=0);a15(b1)=a15(b1)+360;
   b1=find(a15<=0);a15(b1)=a15(b1)+360;
   b1=find(a15>360);a15(b1)=a15(b1)-360;
   b1=find(a15>360);a15(b1)=a15(b1)-360;
   
   %storing spectrum values in 1 degree boxes;   
   for k=1:length(a15),
      bb=a15(k);
      w1(bb)=w1(bb)+er4(k);
      w2(bb)=w2(bb)+1;   
   end;
end;


%filtrando w1 para determinar d(teta)
xx=[w1(321:360);w1;w1(1:40)];
[b a]=butter(6,0.15);
x=filtfilt(b,a,xx);
x=x(41:400);

% figure
% plot(w1), hold all
% plot(x)
% shg