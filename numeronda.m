%Rotina desenvolvida por João Luiz B. Carvalho

function [aa] = numeronda(h,deltaf,reg2)

g=9.8;
k=[];

kant=.001;
kpos=.0011;

for j=1:reg2;
   sigma=(2*pi*deltaf(j))^2;
   while abs(kpos-kant)>0.001
      kant=kpos;
      dfk=g*kant*h*sech(kant*h)^2+g*tanh(kant*h);
      fk=g*kant*tanh(kant*h)-sigma;
      kpos=kant-fk/dfk;
   end
   kant=kpos-0.002;
   k=[k kpos];
end

aa=k;