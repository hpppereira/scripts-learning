
%preparadadosgx3.m ---- para preparar dados de gx3: acelera��o e 
%dois slopes

zco=dlmread('TOA5_61689.microstrain_stbaclV.dat',',',4,2);
zdd=dlmread('TOA5_61689.microstrain_stbaclEW.dat',',',4,2);
zdc=dlmread('TOA5_61689.microstrain_stbaclNS.dat',',',4,2);
save dadosgx32 zco zdd zdc
