% Relatório final: filtros comuns x wavelets
 
% limpa graficos
close all;
clear all;
 
% gera funções sin e ruido
N=500;
T=1:N;
f=0.01;
f2=0.02;
A=1;
Anoise = 2;
fase = pi/2;
 
y1 = A*sin(2*pi*f*T);
y2 = Anoise*(rand(1,N)-0.5);  % ruído
comp = y1+y2;                    % composicao de sinais
observador = A*sin(2*pi*f2*T + fase);   % sinal que vai nos ajudar a recuperar
 
figure;
plot(comp);
title('composicao da senoide com ruido');
 
 
% convolução
 
taps = ones(1,50);
yconv = conv(taps, comp);
figure;
subplot(311);
plot(yconv(1:500));
title('Por convolução');
 
 
% filtro adaptativo
% erro = .001;       
% taps = 100;
% [ylms, e, hf] = lms(comp,taps,observador,erro);
% subplot(312);
% plot(ylms);
% title('Por LMS');
 
 
% wavelets
[thr,sorh,keepapp] = ddencmp('den','wv',comp); % obtem valores default
yhaar = wdencmp('gbl',comp,'haar',1,thr,sorh,keepapp); % retira ruído
subplot(313), plot(yhaar);
title('Por wavelets - Haar');
 
 
% FIR
taps = 10;
freq = [0 0.1 0.11   1    ];
ampl = [1 1   0.001  0.001];
coef = fir2(taps,freq,ampl,blackman(taps+1));
yfir = filter(coef,1,comp);
figure;
subplot(311),plot(yfir),title('Por FIR - Blackman');
 
% IIR
ord = 1 ;     
Fpt = 0.1;   
[n,d] = butter(ord, Fpt);
yiir = filter(n,d,comp);
subplot(312),plot(yiir),title('Por IIR - Butterworth');
 
% wavelets
[thr,sorh,keepapp] = ddencmp('den','wv',comp); % obtem valores default
xd = wdencmp('gbl',comp,'db2',2,thr,sorh,keepapp); % retira ruído
subplot(313), plot(xd);
title('Por wavelets - Daubechies');
 
 
figure,freqz(yconv),title('resp. freq. filtro convoluído');
figure,freqz(ylms),title('resp. freq. filtro LMS');
figure,freqz(yfir),title('resp. freq. filtro FIR');
figure,freqz(yiir),title('resp. freq. filtro IIR');
figure,freqz(xd),title('resp. freq. wavelets - Daubechies');
figure,freqz(yhaar),title('resp. freq. wavelets - Haar');