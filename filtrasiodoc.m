%rotina para filtrar dados do siodoc

[b a]=butter(3,0.15);
ddirsiodoc=zeros(10,744);

for ik=[1 3 5 7]
    h=dire(ik,:)';
    
    teste5
    
    hh=h*2*pi/360;

    s1=[];s2=[];g3=[];
    
    for i=1:744,
        if hh(i)>0,
            s1=[s1;hh(i)];
            disp(length(s1))
            s2=[s2;i];
                        
%        else;
            
            if length(s1)>9,
                z1=cos(s1);z1=filtfilt(b,a,z1);
                z2=sin(s1);z2=filtfilt(b,a,z2);
                g3=angle(z1+j*z2);g3=g3*360/(2*pi);
                             
                g4=find(g3<0);g3(g4)=g3(g4)+360;
                g4=find(g3>=360);g3(g4)=g3(g4)-360;
                                
                ddirsiodoc(ik,s2(1):s2(end))=g3;
                s1=[];s2=[];g3=[];
%            else;

                if length(s1)>0,
                ddirsiodoc(ik,s2(1):s2(end))=s1*180/pi;
                s1=[];s2=[];g3=[];
                end;
                
            end;        
        end;
        
    end;
    
    ss=ddirsiodoc(ik,:);
    for km=1:743,if abs(ss(km+1)-ss(km))>20,ddirsiodoc(ik,km+1)=0;end;end;
      
end

