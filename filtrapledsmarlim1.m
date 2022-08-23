
[b a]=butter(3,0.1);
ddir1=zeros(10,248);

for ik=1:10,    
    h=ddir(ik,:);
    hh=h;
    g=find(h>0);
    g1=diff(g);
    g2=find(g1>1);
    k=zeros(2,length(g2)-1);
    for i=1:length(g2),
        k(1,i)=g(g2(i));
        k(2,i)=g(g2(i))+g1(g2(i));
    end;
    g8=diff(k);
    if length(g8)>1,
    for i=1:length(k),
        if g8(i)<4,
            y=[h(k(1,i));h(k(2,i))];x=[k(1,i);k(2,i)];xi=(k(1,i):k(2,i))';
            yi=interp1(x,y,xi);
            hh(xi')=yi';
        end;
    end
    end
    hh=hh*2*pi/360;
    s1=[];s2=[];g3=[];
    for i=1:248,
        if hh(i)>0,
            s1=[s1;hh(i)];
            s2=[s2;i];
                     
        else;
            
            if length(s1)>9,
                z1=cos(s1);z1=filtfilt(b,a,z1);
                z2=sin(s1);z2=filtfilt(b,a,z2);
                g3=angle(z1+j*z2);g3=g3*360/(2*pi);
                             
                g4=find(g3<0);g3(g4)=g3(g4)+360;
                g4=find(g3>=360);g3(g4)=g3(g4)-360;
                                
                ddir1(ik,s2(1):s2(end))=g3;
                s1=[];s2=[];g3=[];
            else;
                if length(s1)>0,
                ddir1(ik,s2(1):s2(end))=s1*180/pi;
                s1=[];s2=[];g3=[];
                end;
            end;
        end;
    end;
end
