% Calcula o autoespectro e o intervalo de confianca para uma serie real
% utilizando a funcao 'spectrum'
%
% Elaborado por Henrique P. P. Pereira (henriqueppp@peno.coppe.ufrj.br)
%
% Ultima modificacao: 01/11/2012
%
% Dados de entrada: x - serie real com 1024 pontos (ex: elevacao do mar)
%                   dt - intervalo amostragem
%                   gl - graus de liberdade (padrao: 32)
%
% Dados de saida: matriz ss - col 1 - vetor de frequencia
%                             col 2 - autoespectro de x
%                             col 3 - int. confianca inferior

function [ss]=spec(x,dt,gl)


%seleciona 1024 registros da serie (pode variar desde que com mesmo comprimento)
x=x(1:1024);

%graus de liberdade (ex: 2, 4, 8, 32..) - alisa o espectro
% gl=32;

%comprimento do registro
reg=length(x);

%comprimento do vetor do espectro
N=reg/(gl/2);

%frequencia de nysquit (frequencia de corte)
fny=1/(2*dt);

%vetor de frequencia
% f=(fny/reg:(gl*fny)/reg:fny)';
f=(1/(N*dt):1/(N*dt):fny)';

%numero de subdivisoes para o calculo do espectro
subd=reg/(gl/2);

%overlaping de 50% para o calculo do espectro
ov=subd/2;

%chama subrotina spectrum
sp=spectrum(x,subd,ov,'welch');

% Corre��es necessarias para a funcao fft e spectrum (perguntar para o parente)
% fft: - nao divide por N
%      - nao multiplica por dt 
% spectrum: - divide por N
%           - nao multiplica por dt
% multiplica por 2, por que?? fator de escala?

sp=2*dt*sp;

%autoespectro de x
asp=sp(2:length(sp),1);

%intervalo de confianca
icinf=sp(2:length(sp),2);
icsup=icinf+asp; %verificar como se calculo o intervalo de conf superior

[ss]=[f asp icinf icsup];


