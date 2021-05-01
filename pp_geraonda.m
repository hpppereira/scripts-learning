%% Programa principal para analisar os dados de onda gerado pela subrotina 'geraonda3'.

%
%Desenvolvido por:
% Henrique Patricio P. Pereira
% E-mail: henriqueppp@oceanica.ufrj.br
% Data da ultima modificacao: 11/11/2013

clear,clc,close all
%% parametros da rotina geraonda

%parametros de entrada
dt = 1;
num = 2048;
t = 1:num;
h = 1000;
gl = 16;
spread = 0.1;

%onda 1
tetamean1 = 1;
hsig1 = 0.7;                                    
tp1 = 13;

%onda 2
tetamean2 = 170;
hsig2 = 0.8;                                    
tp2 = 13;

[neta1,netax1,netay1] = geraonda(num,h,hsig1,tp1,tetamean1,spread);
[neta2,netax2,netay2] = geraonda(num,h,hsig2,tp2,tetamean2,spread);

%% soma as series (simula mar cruzado)
neta = neta1 + neta2;
netax = netax1 + netax2;
netay = netay1 + netay2;

%% Espectros
% [aan]=espec(neta,dt); %Espec. de neta

%% Calculo dos parametros de onda

%chama subrotina de processamento de onda no dominio do tempo (Tza, Hs..)
[Hs,H10,Hmed,Hmin,Hmax,Tmed,Tmin,Tmax,THmax,Lmed,Lmax,Lmin,Cmed]=onda_tempo(t,neta,h);

%chama subrotina de processamento de onda no dominio da frequencia (dir,hm0..)
[f,an,anx,any,a1,b1,diraz,dirm,Dp,fp,Tp,Hm0]=onda_freq(dt,h,neta,netax,netay,gl);


%% Plot do neta, netax, netay

% figure
% plot(neta(1:100),'b','linewidth',2.5)

fig = figure;
subplot(2,1,1)
plot(t,neta,'b'), grid on
xlabel('Tempo (s)')
ylabel('metros')
axis tight
title({['Onda 1 = ' num2str(hsig1) 'm / ' num2str(tp1) 's / ' num2str(tetamean1),'g'] ...
       ['Onda 2 = ',num2str(hsig2),'m / ',num2str(tp2),'s / ',num2str(tetamean2),'g'] ...
       ['Onda calculada = ',num2str(Hm0),'m / ',num2str(Tp),'s / ',num2str(Dp),'g']})
subplot(2,2,3)
plot(f,an), grid on
title('Auto-espec')
xlabel('Freq. (Hz)')
ylabel('m^2/Hz')
subplot(2,2,4)
plot(f,diraz), grid on
title('Direcao principal')
xlabel('Freq. (Hz)')
ylabel('graus')
%saveas(fig,'eta-8.png')


a = [t',neta',netax',netay'];