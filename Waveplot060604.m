% waveplot.m  To plot output from wlet.m in freq. direction contour and mesh plots,
%				  and as a one-dimensional freq. spectrum

clear all
close all

av = 10;	% angle averaging (should be time for display settings below!)
I1 = 2;	% determines first directional slice at 2*fp
I2 = 4;	% determines second directional slice
pa = 1; %, sec, pause duration

%fname = input('the filename is ');
fname = 'l311823';
eval(['load ',fname]);
eval(['load h',fname(2:length(fname))]);

AA=AAp; clear AAp
ddd=mod360(ddd);
ii=find(ddd == 0); ddd(ii)=ddd(ii)+360;
[m,n]=size(ddd);
df=diff([0 f]);
if n>length(df),
   n = length(df);
end   
for j=1:n,
	j
	for k=1:360,
 		kk=k;
 		ii=find(ddd(:,j)==kk);
 		E(k,j)=sum(AA(ii,j).^2)/df(j);
	end
end
 
eval(['save g',fname(2:length(fname)),' E f np'])

for j=1:n,
   EE(j)=sum(E(:,j));%*df(j);
end
EE = EE./sum(EE.*df)*STm^2;

[EEm,i] = max(EE);
fp = f(i);  % peak frequency
%i11 = round(i*I1);
%i12 = round(i*I2);
i11 = find(f==fp*I1);
% i12 = find(f==fp*I2);
i12 = find(round(f*1000)==round(fp*I2*1000));

if i11 > length(EE),
    i11 = i;
    i12 = i;
elseif i12 > length(EE),
    i12 = i11;
end

Emn = E(:,i);
E1mn = E(:,i11);
E2mn = E(:,i12);
Emn=binavg(Emn,av);
E1mn=binavg(E1mn,av);
E2mn=binavg(E2mn,av);
Emn = Emn/max(Emn);
E1mn = E1mn/max(E1mn);
E2mn = E2mn/max(E2mn);

figure(1)
clf

for i2 = 1:np,
    
   subplot(1,np,i2);
   bar(x(:,i2),nn(:,i2));
   
   if i2 == round(np/2),
      title(['histograms for the ',fname,' record'])
   end
   
end

pause(pa)

figure(2)
axis([0 1 0 1])

subplot(231)
mesh(1:360,f(1:n),E')

subplot(232)
loglog(f(1:n),EE,'*-')
grid
xlabel('f, Hz')
title(['record no. ',fname])

subplot(233)
plot(10:10:360,Emn)
axis([0 360 0 1])
hold on
plot(10:10:360,E1mn,'--r')
plot(10:10:360,E2mn,'-.k')
xlabel('deg')
plot([1 50],[0.9 0.9],'-')
text(51,0.9,'f_p')
plot([1 50],[0.8 0.8],'--r')
text(51,0.8,[num2str(f(i11)/f(i)),'\cdotf_p'])
plot([1 50],[0.7 0.7],'-.k')
text(51,0.7,[num2str(f(i12)/f(i)),'\cdotf_p'])
hold off
grid

subplot(234)
contour(1:360,f(1:n),E'.*(f(1:n)'.^0*ones(1,360)),6)
axis([0 360 0 2])
grid
xlabel('degrees')

subplot(235)
contour(1:360,f(1:n),E'.*(f(1:n)'.^4*ones(1,360)),6);
axis([0 360 0 2])
grid
xlabel('*f^4')

subplot(236)
contour(1:360,f(1:n),E'.*(f(1:n)'.^5*ones(1,360)),6);
axis([0 360 0 2])
grid
xlabel('*f^5')
