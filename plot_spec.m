function FT=plot_spec(data,T)
%
% PLOT_SPEC computa e plota o espectro da amplitude 
% PLOT_SPEC (DATA,T) computa e plota o espectro da amplitude da FFT
% do array DATA, amostrado com periodo de amostragem T
% FT = SPECPLOT(...) tambem computa o valor (geralmente complexo) 
% da FFT
%
% nelson violante-carvalho
% n_violante@oceanica.ufrj.br
% https://sites.google.com/site/nviolantecarvalho/
%
% Introdução à Análise de Sinais para Oceanógrafos 
% (e demais interessados no oceano)
%
%
% Programa de Pos-Graduacao em Engenharia Oceanica
% PENO COPPE UFRJ
%
% 2o PERIODO 2015
%
%

N=length(data); % num de pontos, com duracao NT

% computa FFT
FT=fft(data);  % simple like that!

% quais as freqs?
% veja tambem 'help freqspace' 
% usando a teoria...

f=0:1/(N*T):(N-1)/(N*T);

% abre nova figura
%figure

% plotando o spec de amplitude 
%plot(f,abs(FT),'g-',f,abs(FT),'.')
%xlabel('frequencia')

% poderiamos plotar tambem o espectro de fase...
%plot(f,angle(FT),'g-',f,angle(FT),'.')
%xlabel('frequency')

% ou poderiamos plotar da forma que eu prefiro, com a freq zero no
% centro do plot
f1=f-1/(2*T);

% plot spec de amplitude 
plot(f1,fftshift(abs(FT)),'g-',f1,fftshift(abs(FT)),'.')
xlabel('frequencia')

% plot spec fase 
%plot(f1,fftshift(angle(FT)),'g-',f1,fftshift(angle(FT)),'.')
%xlabel('frequencia')


return
