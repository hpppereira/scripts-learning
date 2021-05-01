% ROTINA DECAI

% calculo da regressao logaritmica dos pontos
% acima da freq de pico
% decaimento logaritmico da cauda do espectro em ALTAS 
% frequencias => f^(-a) do paper de McCarthy, T. J.
% Spectral Fitting procedure for Double Peaked Spectra
% Dock and Harbour Engineering Conference 1989

% in:   - freq de pico fp
%       - vetor de freq f
%       - espectro medido strab
%       - trecho do espectro 'y' p/ calculo do decaimento
%       - trecho da freq 'x' p/ calculo do decaimento

% out:  - decaimento logaritmico a



logx=log10(x);
logy=log10(y);

n=length(x);

somaxy=sum(logx'*logy);
somax=sum(logx);
somay=sum(logy);
xm=sum(logx)/n;
ym=sum(logy)/n;
x2=logx.^2;
somax2=sum(x2);

% regressao logaritmica dos pontos acima da freq de pico

a1=(n*somaxy-somax*somay)/(n*somax2-(somax^2));
a0=ym-a1*xm;
a2=10^(a0);
y1=a2*x.^(a1);
a=a1; % decaimento logaritmico

clear somaxy somax somay xm ym x2 somax2 a0 a1 y1 logx logy n
