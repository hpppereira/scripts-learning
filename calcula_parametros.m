%% calculo dos parametros de ondas adimensionais para JONSWAP

clear g1

[b a]=butter(6,0.2);
s2=filtfilt(b,a,hs_daat);
%s2=hs_daat;

g1=diff(s2);
g1=sign(g1);
g1=diff(g1);
g1=[0;g1'];
g2=find(g1==-2);
g3=find(s2(g2)==max(s2(g2)));

hs=zeros(length(g2),1);tp=zeros(length(g2),1);wi=zeros(length(g2),1);
fn=zeros(length(g2),1);pn=zeros(length(g2),1);X=zeros(length(g2),1);
hs2=hs;hs3=hs;


for i=1:length(g2)-1,
   a1=hs_daat(g2(i)-3:g2(i)+3);
   g4=find(a1==max(a1));g4=g4(1);
   g5=g2(i)-3+g4-1;
   hs(i)=hs_daat(g5);
   tp(i)=tp_daat(g5);
   wi(i)=wind(g5,6);
   hs2(i)=hsfaixa(g5,2);
   hs3(i)=hsfaixa(g5,3);
   fn(i)=(1/tp(i))*wi(i)/9.81;
   % P=24.9*fn^-3.33
   pn=fn(i)^-3.33;pn=pn/0.039;
   % P=g*X/U^2
   x=pn*wi(i)^2/9.81;x=x/1000;
   X(i)=fix(x);
end;

gm1=find(fn>0.12);gm2=find(fn(gm1)<0.14);

g1=find(pn>700);pn(g1)=NaN;
figure()
subplot(1,2,1)
plot(fn,X,'o');hold
plot(fn(gm1(gm2)),X(gm1(gm2)),'or');shg
grid
xlabel('frequencia normalizada')
ylabel('pista em km')

subplot(1,2,2)
plot(hs,wi,'o')
xlabel('Hs total')
ylabel('intensidade dos ventos')
grid


figure()
subplot(1,2,1)
plot(hs2,wi,'o');hold on
plot(hs3,wi,'ro')
xlabel('Hs')
legend('Faixa 2','Faixa 3')
ylabel('intensidade dos ventos')
grid

subplot(1,2,2)
plot(hs2,tp,'o');hold on
plot(hs3,tp,'ro')
xlabel('Hs')
legend('Faixa 2','Faixa 3')
ylabel('Tp (s)')
grid

stop
s23(gm1(gm2))=s21(gm1(gm2));s26(gm1(gm2))=1;
g3=find(s15==0);s15(g3)=11;
s10=[s10;0];s11=[s11;s11(end)];s10=round(s10*10)/10;
s16=round(s16*10)/10;
s16=round(s16*10)/10;
s17=round(s17*10)/10;
s19=round(s19*10)/10;
s18=round(s18*10)/10;
s20=round(s20*10)/10;
s21=round(s21*1000)/1000;
s24=round(s24*10)/10;
s25=round(s25*10)/10;



%frequencia normmalizada
fn=(1./tp_ddat)*ws/9.81;