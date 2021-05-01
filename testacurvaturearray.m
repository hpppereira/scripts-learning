reg=1024;
reg2=fix(reg/2);
gl=50;
deltat=1.0;
donv=270;

load d:\users\joao\orientandos\eduardo\registro1.txt

for n=1:5
    registro(:,n)=registro1(:,n);
end

eta=registro(:,1);
etax=registro(:,2);
etay=registro(:,3);
etaxx=registro(:,4);
etayy=registro(:,5);

aa=curvaturearray_emconstrucao(eta, etax, etay, etaxx, etayy, deltat, donv) 

plot(aa(:,1), aa(:,2))