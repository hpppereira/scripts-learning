

% filtragem da daat
% onda
ik1 = 0;
for ik=1:4
    ik1=ik1+1;
    [b a]=butter(4,0.03);
    y=dire(:,ik);
    y=y*2*pi/360;
    y=unwrap(y);
    w1=y*360/(2*pi);
    y1=cos(y);y2=sin(y);
    w=zeros(length(dire),1);
    for i=5:length(dire)-5,
        g1=mean(y1(i-4:i+4));
        g2=mean(y2(i-4:i+4));
        g3=angle(g1+j*g2);g3=g3*360/(2*pi);
        if g3<0
            g3=g3+360;
        end;
        if g3>=360,
            g3=g3-360;
        end;
        w(i)=g3;
    end;
    g=find(w>360);
    w(g)=w(g)-360;
    g=find(w>360);
    w(g)=w(g)-360;
    g=find(w<0);
    w(g)=w(g)+360;
    dire(1:length(w),ik1)=w;
end


[b a]=butter(4,0.03);
y=wd;
y=y*2*pi/360;
y=unwrap(y);
w1=y*360/(2*pi);
y1=cos(y);
y2=sin(y);
w=zeros(1,length(wd));
for i=5:length(wd)-5,
    g1=mean(y1(i-4:i+4));
    g2=mean(y2(i-4:i+4));
    g3=angle(g1+j*g2);
    g3=g3*360/(2*pi);
    if g3<0
        g3=g3+360;
    end;
    if g3>=360,
        g3=g3-360;
    end;
    w(i)=g3;
end;
g=find(w>360);
w(g)=w(g)-360;
g=find(w>360);
w(g)=w(g)-360;
g=find(w<0);
w(g)=w(g)+360;
wd(1:length(w))=w;
