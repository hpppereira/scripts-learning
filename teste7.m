
w=tet2*180/pi;w=w/4;
[n,bi]=hist(w,20);
g=find(n==max(n));
w1=[bi(16:20) bi bi(1:5)];
g1=w1(g+5);
setor=w1(g:g+10);

xz=zeros(90,1);
g4=[];

for i=1:length(tet2),
    
    z=w(i);z=ceil(z);
    q=setor-z;
    q1=find(abs(q)<2);isempty(q1);
    if ans==0,g4=[g4 z];
    if z>90,z=z-90;end
    xz(z)=xz(z)+sp2(i);
    end;end
    g1=smooth(xz,8);g1=smooth(g1);
    g8=diff(g1);g8=sign(g8);g8=diff(g8);g8=[0;g8];
    g8=find(g8==-2);
    if iwq==1,angulo(:,kkl)=g1;end    
    %if iwq==1,if length(g8)<4,
    %g1=filtfilt(b,a,g1);
    g2=find(g1==max(g1));
    g2=g2*4;
    g2=270-g2-23;
    if g2<0,g2=g2+360;end
    %if energsio(6,kkl)>11.8,
    diresio(kkl,iwq)=g2;
    %end;
    %end;end;