% 
% exercicio #04
% codigo simples para gerar onda quadrada e constatar os harmonicos que a compoe
%
% nelson violante-carvalho
% n_violante@oceanica.ufrj.br
% https://sites.google.com/site/nviolantecarvalho/
%
% Introdução à Análise de Sinais para Oceanógrafos 
% (e demais interessados no oceano)
%
% Programa de Pos-Graduacao em Engenharia Oceanica
% PENO COPPE UFRJ
%
% 2o PERIODO 2015
%
% obs.:
% necessita a subrotina plot_spec

clear, close all

% Lembrando da teoria que vimos em sala
% Freq Nyquist f_N (Hz) = 1/2 dT
% freq_am > 2 * freq_max
% freq fundamental f_1 = 1 / (N dT)
% resolucao em frequencia delta_f = 1 / (N dT)
% numero max de componentes espectrais = f_N / f_1 = N/2
%
% Comecando....
% Vamos inserir alguns valores
dT=.1; % periodo de amostragem Delta_t (s)
t = -3+dT:dT:3; % duracao do sinal (s)
N=length(t); % num de pontos do sinal
%
% gerando uma onda quadrada 
sq=square(1*t,50); % ver 'help square'
figure(1), plot(t,sq)
axis([-3 3 -2 2])
%
% calcule a FFT da onda quadrada
% use a rotina plot_spec
plot_spec(sq,dT);
%
% Muito bem, vamos responder juntos algumas perguntas.
% Primeiramente, na fig 2, espectro de amplitude, repare que os pontos azuis 
% correspondem a cada valor do vetor de frequencia.
% i. calcule a freq fundamental.
% ii. calcule as frequencias de seus harmonicos.
% iii. quais harmonicos (impares ou pares?) NAO tem energia?
% iv. se vc for reconstruir a onda quadrada usando suas componentes senoidais, quais harmonicos vc incluiria no seu calculo em funcao da energia de cada um deles apresentada na fig 2?
% v. empregando a expansao de fourier, uma onda quadrada pode ser expressa
% como uma serie infinita com a forma
% sq(t) = 4/pi * (1 sin (2*pi*t /T) + 1/3 (6*pi*t /T) + 1/5 (10*pi*t /T) + ... )
% baseado em sua resposta em iii, comente a equacao acima
% vi. baseado na figura 1, qual o valor de T?
% vii. baseado na equacao v, comente iv
% viii. reconstrua a onda quadrada usando suas componentes senoidas (eq v)
% primeiro, plote novamente a onda quadrada e em seguida use o comando 'hold'.
% em seguida, plote cada componente. comente seus resultados.


