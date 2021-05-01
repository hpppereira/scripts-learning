function [somat]=integral(reg2,fc,qd);

% Calcula a Integral de uma funçao por metodo de Newton

% Parametros de entrada (i) e saida (o)

% Reg2..............numeros de pontos do espectro (i)
%fc.................frequencia de corte(i)
%qd.................vetor de quadespectro(i)
%somat..............valor da integral (o)


% Variaveis Internas

% i............contador
% deltaf.......frequencia

somat=0.0;
deltaf=fc/reg2;
for i=2:reg2-1;
    somat=somat+qd(i)*deltaf;
end
somat=somat+(qd(1)+qd(reg2))/2*deltaf;
