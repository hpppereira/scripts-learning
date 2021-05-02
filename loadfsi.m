%leitura dos dados do FSI do WW3ES

%arq = nome do arquivo .fsi
%ex: '27205_2014-01-01-00-39.fsi'

function [dados]=loadfsi(arq)

[fsi] = textread(arq,'%s','delimiter','  ','headerlines',25);

cont = 0;
for i=1:15:17960
    
    cont = cont + 1;

    dados(cont,1) = str2num(fsi{i+4});
    dados(cont,2) = str2num(fsi{i+13});
    dados(cont,3) = str2num(fsi{i+14});
        
end



