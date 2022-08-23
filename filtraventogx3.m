load out14_wind.mat
out14_wind(:,2)=out14_wind(:,2)*(10/4)^(1/7);

out14_wind(:,1)=out14_wind(:,1)-22;
g=find(out14_wind(:,1)<0);out14_wind(g,1)=out14_wind(g,1)+360;
ggg=size(out14_wind);ggg=ggg(1);
[b a]=butter(3,0.1);
ventodir1=zeros(1,ggg);
www50(1,:)=out14_wind(:,1)';

g=find(www50(1,:)<=0);www50(1,g)=www50(1,g)+360;

www50(2,:)=out14_wind(:,2)';
for ik=1:1,
    h=www50(1,:);
    hh=h;
    hhh=www50(2,:);
    %fase de interpolação
    g=find(h>0);
    g1=diff(g);
    g2=find(g1>1);
    k=zeros(2,length(g2)-1);
    for i=1:length(g2),
        k(1,i)=g(g2(i));
        k(2,i)=g(g2(i))+g1(g2(i));
    end;
    g8=diff(k);
    for i=1:length(k),
        if g8(i)<4,
            y=[h(k(1,i));h(k(2,i))];x=[k(1,i);k(2,i)];xi=(k(1,i):k(2,i))';
            yi=interp1(x,y,xi);
            hh(xi')=yi';
        end;
    end
    
    hh=hh*2*pi/360;
    s1=[];s2=[];g3=[];
    ss1=[];
    %fase de filtragem
    for i=1:744,
        
            s1=[s1;hh(i)];ss1=[ss1;hhh(i)];
            s2=[s2;i];
                     
    end
            
       
                z1=ss1.*cos(s1);z1=filtfilt(b,a,z1);
                z2=ss1.*sin(s1);z2=filtfilt(b,a,z2);
                g3=angle(z1+j*z2);g3=g3*360/(2*pi);
                             
                g4=find(g3<0);g3(g4)=g3(g4)+360;
                g4=find(g3>=360);g3(g4)=g3(g4)-360;
                                
                ventodir1(ik,s2(1):s2(end))=g3;
                %s1=[];s2=[];g3=[];ss1=[];
%             else;
%                 if length(s1)>0,
%                 ventodir1(ik,s2(1):s2(end))=s1*180/pi;
%                 s1=[];s2=[];g3=[];ss1=[];
%                 end;
%             end;
        end;
    %ventodir1=ventodir1-22;
    g=find(ventodir1<0);ventodir1(g)=ventodir1(g)+360;

    data=[datenum(0,10,1):1/24:datenum(0,10,31,23,0,0)];
figure (1)
plot(data,ventodir1,'ob')
title('Direção do vento da Ilha Rasa - OUT/2014')
ylabel('Direção do vento (°)')

axis([data(1) data(end) 0 360])   
datetick('x','dd/mmm')
grid on
axis([data(1) data(end)+1/24 0 360])  

    
    