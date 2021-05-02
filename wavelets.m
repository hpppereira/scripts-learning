%% Aprendendo wavelets toolbox


%% cria wavelet Morlet
lb = -4;
ub = 4;
n = 1000;
[psi,xval] = morlet(lb,ub,n);
plot(xval,psi)
title('Morlet Wavelet');

