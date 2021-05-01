

ddir=zeros(10,length(dire1));

%cc=[1;9;17;25;33];

for ik=1:10
    
    [b a]=butter(4,0.03);
    y=dire1(ik,:);
    y=y*2*pi/360;
    y=unwrap(y);
    w1=y*360/(2*pi);
    y1=cos(y);y2=sin(y);
    w=zeros(1,length(dire1));

    for i=5:length(ddir)-5
        
        g1=mean(y1(1,i-4:i+4));
        g2=mean(y2(1,i-4:i+4));
        g3=angle(g1+j*g2);g3=g3*360/(2*pi);
        
        if g3<0,g3=g3+360;end;
        
        if g3>=360,g3=g3-360;end;
        w(i)=g3;
        
    end

    x=diff(w1);
    x=abs(x);
    g=find(x>30);
    w(g+1)=w1(g+1);

    g=find(w>360);
    w(g)=w(g)-360;
    g=find(w>360);
    w(g)=w(g)-360;

    g=find(w<0);
    w(g)=w(g)+360;
    g=find(w<0);
    w(g)=w(g)+360;
    ddir(ik,1:length(w))=w;
end;

dire1 = ddir;






