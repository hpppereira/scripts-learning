%% programa principal para mostrar espectros de fase e coerencia
% em series simuladas pela rotina geraonda3

%
%Desenvolvido por:
% Henrique Patricio P. Pereira
% E-mail: henriqueppp@oceanica.ufrj.br
% Data da ultima modificacao: 11/11/2013

%%
clear,clc,close all

%escolhe a direção para simular as ondas
tetamean = 90;

[neta,netax,netay,netaxx,netayy,velx,vely,velz,velzz,velzzz,pr,dt,h,z,d,g] = geraonda3(tetamean);

%calcula o espectro cruzado
a = rand(1024,1);
[aa] = espec2(neta,a',1);

figure
subplot(2,1,1)
plot(neta)
axis('tight')
title('Elevacao')
ylabel('metros')
subplot(2,1,2)
plot(a)
axis('tight')
title('Serie randomica')
xlabel('Tempo (s)')

figure
subplot(3,1,1)
plot(aa(:,1),aa(:,2))
title('S(f) - neta')
subplot(3,1,2)
plot(aa(:,1),aa(:,3))
title('S(f) - serie randômica')
subplot(3,1,3)
plot(aa(:,1),aa(:,8))
title('Espectro de coerência')
xlabel('Frequência')