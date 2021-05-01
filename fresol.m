function [resol]=fresol(eta);


valor= fix(eta*1000);        
AA=abs(mod(valor,3));    
while AA>=1            
    valor=valor-1;   
    AA=abs(mod(valor,3)); 
end                      
resol=valor/100;   