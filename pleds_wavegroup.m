
% fr3=[];fr4=[];mq=64;
% for ip=1:mq,
%     
%     fr3=[fr3;tet2(ip:m1-(mq-ip))];
%     fr4=[fr4;sp2(ip:m1-(mq-ip))];
% end;
g=find(tet2>4);
tet2(g)=tet2(g)-6.28;
tet9=tet2;tet9=tet9*57;
tet9=270-tet9-22;
c=hanning(8);

figure(1);clf;hold;
v=[-20 360 0 68];axis(v);
dl=0;
for i=1:667,
    dl=dl+0.1;
    x=[tet9(i)+(-3:4)];
%     g=find(x<0);x(g)=x(g)+360;
    y=0.05*sp2(i)*c+dl;
    plot(x,y,'color',[0 0 1]);
    
end
grid
xlabel('direção em graus')
ylabel('tempo e espectro')
title('evolução da direção para o registro 515')
text(0,30,'vento médio:')
text(0,27,'196 graus, 10.6 m/s')
    
figure(2);clf;hold;
v=[-20 360 0 68];axis(v); 
dl=0;
for i=668:1335,
    dl=dl+0.1;
    x=[tet9(i)+(-3:4)];
%     g=find(x<0);x(g)=x(g)+360;
    y=0.05*sp2(i)*c+dl;
    plot(x,y,'color',[0 0 1]);
    
end
grid;
xlabel('direção em graus')
ylabel('tempo e espectro')
title('evolução da direção para o registro 515')
text(0,30,'vento médio:')
text(0,27,'196 graus, 10.6 m/s')



figure(1);
v=[-20 360 0 68];axis(v);
dl=0;
for i=1:680,dl=dl+0.1;
x=[250+(-3:4)];x=x';
y=c+dl;
q=[1 0 0];kl=100;kl1=0;
for k=1:10,kl=kl-10;kl1=kl1+0.1;
if sp2(i)<kl,q=[1 kl1 kl1];end
end
plot(x,y,'color',q);
end


figure(2);
v=[-20 360 0 68];axis(v);
dl=0;
for i=681:1335,dl=dl+0.1;
x=[250+(-3:4)];x=x';
y=c+dl;
q=[1 0 0];kl=90;kl1=0;
for k=1:10,kl=kl-10;kl1=kl1+0.1;
if sp2(i)<kl,q=[1 kl1 kl1];end
end
plot(x,y,'color',q);
end









