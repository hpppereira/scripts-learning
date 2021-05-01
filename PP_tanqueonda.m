%PP tanqueonda
clear,clc,close all
[ufd,wfd]=simulacao_tanqueonda;
dt=1;
%% Chama subrotina de espectro cruzado
[aa]=espec2(ufd,wfd,dt);

%% Plot
subplot(2,2,1)
plot(aa(:,1),aa(:,2))
title('Auto-espectro de U')
subplot(2,2,2)
plot(aa(:,1),aa(:,3))
title('Auto-espectro de V')
subplot(2,2,3)
plot(aa(:,1),aa(:,7))
title('Espectro de fase entre U e V')
subplot(2,2,4)
plot(aa(:,1),aa(:,8))
title('Espectro de coerência entre U e V')