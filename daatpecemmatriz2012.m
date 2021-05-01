%CODE daatmarlimmatriz to select the segments for
%the directional spectrum composition
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Prepared by C.E. Parente
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
q1=cos(tet2);q2=sin(tet2);
pm=length(round(m/2):m1-(m-round(m/2)));
fr3=zeros(round(m/2),pm);
fr5=fr3;fr4=fr3;
for ip=1:round(m/2),
   fr3(ip,:)=q1(ip:m1-(m-ip));
   fr5(ip,:)=q2(ip:m1-(m-ip));
   fr4(ip,:)=sp2(ip:m1-(m-ip));
end;

fr2a=mean(fr3);fr2b=mean(fr5);
r=sqrt(fr2a.^2+fr2b.^2);
%circular deviation
fr9=sqrt(2*(1-r));   

fr2=angle(fr2a+j*fr2b);
g=find(fr2<0);fr2(g)=fr2(g)+2*pi;
g=size(fr2);g=g(2);

matr=zeros(20,90);
matr2=matr;
%direçao/4
qp=270-fr2*180/pi-21;
%qp=270-fr2*180/pi-23;qp1=qp;
gg=find(qp<=0);qp(gg)=qp(gg)+360;
gg=find(qp>360);qp(gg)=qp(gg)-360;
qp=ceil(qp/4);

%desvio padrao *20
fr10=round(fr9*20);

%preparando a matriz
for kk=1:g,
    a1=fr10(kk);
    a2=qp(kk);
    
    if a1*a2>0,
        if a1<20,if a2<90,
            matr(a1,a2)=matr(a1,a2)+fr45(kk);
            matr2(a1,a2)=matr2(a1,a2)+1;
        end;end;
    end;
end;

