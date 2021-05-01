%   Pororoca eh uma funçao para encontrar o Retro Espalhamento Acustico (REA)
%   a partir do sinal acustico coletado por Perfiladores Acusticos de 
%   Corrente por efeito Doppler (PACD).
%
%   IMPORTANTE: Verifique se as informaçoes dos 3 transdutores estao parecidas, caso nao, 
%   use apenas as informaçoes dos transdutores cujos dados estao "bons". Mar com ondas e PACD 
%   instalado muito na superficie, podem gerar muitos spikes com informaçoes incorretas.  
% 
%   USO: [REA]=pororoca(a1,a2,a3,ncels,celsize,blank, som);
% 
%   a1,a2 e a3 = Matrizes brutas com os dados de amplitude acustica coletado pelo PACD.
%   ncels = Numero de celulas 
%   celsize = Tamanho das celulas em metros
%   blank = Blank distance do equipamento.
%   som = Valor da absorçao do sinal acustico pela agua na unidade de (dB/m). 
%   Para sal = 35 e freq = 1MHz som = 0.42; Para sal = 35 e freq = 1.5 MHz som = 0.65;
%
%   ruido = Valor medio de a1, a2 e a3 enquanto o equipamento opera fora da agua. 
%   Para o ADP 1.5 MHz ruido = 24 counts e para NDP 1MHz = 22 counts
%
%   ************************************************************************************************
%   Depois de encontrado o REA, as informaçoes podem ser convertidas em MPS atraves das seguintes 
%   equaçoes para o "estuario do Rio Itajai-açu":
%
%   ADP Sontek:
%
%   REO=0.0005519*exp(0.1497*REA);
%   MPS=3.2410+2.38469*REO;
%___
%
%   Aquadopp Nortek:
%
%   REO=148.2374-7.6152*REA+0.0999*(REA)^2;
%   MPS=3.2410+2.38469*REO;
%___
%
%
%   Alexsandro Rodrigo Zaleski, junho de 2005
%   atualizada: 04/07/2005; O Help foi melhorado... 
%   
%/////////////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

function [REA]=pororoca(a1,a2,a3,ncels,celsize,blank,som,ruido);

amp=(a1(:,2:end)+a2(:,2:end)+a3(:,2:end))/3;

z=blank+celsize+.5:celsize:celsize*ncels+celsize+.5;                            %0.5 = valor medio da profundidade do sendor 


for i=1:length(amp(1,:));
   REA(:,i)=(amp(:,i)-ruido)*0.43 + 20*log10(z(:,i)/cos(25*pi/180)) + ...       %0.43 = fator escalar pra trasformar
      2*som* ((z(:,i))/cos(25*pi/180));                                         %counts pra dB's.
end;

