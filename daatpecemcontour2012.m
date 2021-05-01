it=2*(iwq-1)+1;
n=contourc(matr,5);
g=1;lv1=[];nm5=0;
while g>0,nm5=nm5+1;
    lv1=[lv1;nm5];

    nm5=nm5+n(2,nm5);
    if nm5==length(n),g=0;end;
end;

lv2=n(2,lv1);lv3=n(1,lv1);
lv4=n(1,lv1+1);

a1=4*mean(n(1,lv1(end)+1:lv1(end)+n(2,lv1(end))));
a3=energ(iwq+1,kkl);
a2=0;a4=0;
dire(it,kkl)=a1;
espe(it,kkl)=a3;

if iwq>2,
    k1=1;k=0;
    while k1>0,k=k+1;
        v=4*lv4(end-k);
        if abs(v-a1)>40,
            a2=4*mean(n(1,lv1(end-k)+1:lv1(end-k)+n(2,lv1(end-k))));
            a4=lv3(end-k);
            k1=0;
        end;
        if k+1==length(lv4),k1=0;end;
    end;
    a3=lv3(end);
    if a4>0.1*a3,
        norm=a3+a4;a5=energ(iwq+1,kkl);
        dire(it+1,kkl)=a2;
        espe(it+1,kkl)=a4*a5/norm;
        espe1(it,kkl)=a3*a5/norm;
    end;
end;