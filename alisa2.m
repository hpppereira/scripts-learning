function[bb]=alisa2(coef)
  
reg2=length(coef);
gl=40;
gl2=gl/2;

coef1=[coef(reg2:-1:1) coef coef(reg2:-1:1)];    
coef2=coef1;

for i=gl2+1:length(coef1)-gl2-1
    coef2(i)=mean(coef1(i-gl2:i+gl2));
end    
  
bb=coef2(reg2+1:reg2+reg2);