% 
% exercicio #03
% codigo simples para verificar o surgimento (ou nao) de aliasing
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
% obs.:
% necessita a subrotina plot_spec

clear, close all

% Lembrando da teoria que vimos em sala:
% Freq Nyquist f_N (Hz) = 1/2 dT
% freq_am > 2 * freq_max
% freq fundamental f_1 = 1 / (N dT)
% resolucao em frequencia delta_f = 1 / (N dT)
% numero max de componentes espectrais = f_N / f_1 = N/2
%
% Comecando....
% Vamos inserir alguns valores
dT=1; % periodo de amostragem Delta_t (s)
N=100; % num de pontos do sinal
t=0:dT:(N-1)*dT; % duracao do sinal (s)
%
% sinal = sin (w1*t);
% Gere uma onda senoidal s1 = sin (2 pi f_p1 t)
% com f_p1 =.4 Hz
% Gere uma onda senoidal s2 = sin (2 pi f_p2 t)
% com f_p2 =.25 Hz
%
% some as duas ondas senoidais sinal=s1+s2
% plote sinal
plot(t,sinal)
% calcule a FFT de sinal
% use a rotina plot_spec
plot_spec(sinal,dT);
%
% Muito bem, vamos responder juntos algumas perguntas.
%
% Primeiro, de uma olhada na serie temporal (fig 1) e no spec de amplitude (fig 2). Repare que ambos sao formas diferentes de representacao de um mesmo sinal, no dominio do tempo e no dominio da frequencia.
%
% baseado no que vimos em sala, qual a freq fundamental f_1? e a resolucao em frequencia delta_f? qual o numero de componentes espectrais podemos determinar dos dados? e quais sao elas? olhe para a figura do spec de amplitude e compare com seus resultados.
%
% i. qual a freq de nyquist (f_N) neste exemplo? a freq de amostragem satifaz o teorema de amostragem?
% ii. ha energia em 'sinal' alem de f_N? 
% iii. baseado em ii, qual a implicacao no spec de amplitude?
% iv. multiplique s1 por uma cte qq; multiplique s2 por uma outra cte qq; compute 'sinal' mais uma vez e calcule sua FFT? o que mudou?
% v. mude dT para 1.5 e compute de novo a FFT? o que acontece com a energia contida alem de f_N?
% vi. com dt ainda em 1.5, responda mais uma vez de i a iv
% vii. ainda com dT=1.5, responda: qual a freq fundamental f_1? e a resolucao em frequencia delta_f? qual o numero de componentes espectrais podemos determinar dos dados? e quais sao elas?
% viii. comparativamente, o que muda quando dT=1 e dT=1.5?
