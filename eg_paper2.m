% novo exemplo
% dados de onda
clear, clc, close all

%carrega dados de onda
%dados=load('92051522.DAT');
dados1=importdata('/home/hp/Dropbox/publicacoes/brbuoys/dados/200907241900.HNE',' ',11);
n1 = dados1.data(:,2);
dados2=importdata('/home/hp/Dropbox/publicacoes/brbuoys/dados/201203281400.HNE',' ',11);
n2 = dados2.data(:,2);
n2 = n2(1:1313);

n1 = n1 - mean(n1);
n2 = n2 - mean(n2);

%intervalo de amostragem (segundos)
dt=0.78;

%vetor de tempo
t = 0:0.78:length(n1)*0.78-0.78;


figure
subplot(221)
plot(t,n1)
grid('on')
axis('tight')
ylabel('Elevation (m)')
xlim([400,900])
subplot(223)
spectrogram(n1,hamming(10),8,100,1,'yaxis')
shading interp
xlabel('Time (s)')
xlim([400,900])

subplot(222)
plot(n2)
grid('on')
axis('tight')
ylabel('Elevation (m)')
xlim([1100,1300])
subplot(224)
spectrogram(n2,hamming(10),8,100,1,'yaxis')
shading interp
xlabel('Time (s)')
xlim([1100,1300])


