clear, clc, close all
% curso wavelet coursera
% procurar por spectrgrama (time-freq analysis)

%carrega dados da axys
% dados = importdata('../dados/200905252100.HNE',' ',11);
% dados.data = dados.data(1:1024,:);
% t = dados.data(:,1);
% n1 = dados.data(:,2);
% n2 = dados.data(:,4);  
% n3 = dados.data(:,3); %combinacao para a triaxys

%serie de heave
% S = n1';
%n = length(t);


L = 10; %ime window
n = 2048;
t2 = linspace(0,L,n+1); t = t2(1:n);
k = (2*pi/L)*[0:n/2-1 -n/2:-1]; ks = ifftshift(k);

S = (3*sin(2*t)+0.5*tanh(0.5*(t-3))+0.28*exp(-(t-4).^2)+1.5*sin(5*t)+4*cos(3*(t-6).^2))/10+(t/20).^3;



St = fft(S);

%figure
%ubplot(3,1,1), plot(t,S)
%subplot(3,1,2), plot(ks,abs(fftshift(St))/max(abs(fftshift(St))))

figure
width = [10 1 0.2];
for j = 1:3
    f = exp(-width(j)*(t-4).^2);
    subplot(3,1,j), plot(t,S,'k',t,f,'m')
end

figure
width = 50; %quanto menor, mais resolucao em frequencia e menor em tempo
slide= 0:0.1:10;
spec = []; %spectrograma matrix
for j = 1:length(slide)
    f = exp(-width*(t-slide(j)).^2);
    Sf = f.*S;
    Sft = fft(Sf);
    
    subplot(3,1,1), plot(t,S,'k',t,f,'m')
    subplot(3,1,2), plot(t,Sf,'k')
    subplot(3,1,3), plot(ks,abs(fftshift(Sft))/max(abs(fftshift(Sft))))
    axis([-60 60 0 1])
    drawnow
    pause(0.1)
    
    spec = [spec ; abs(fftshift(Sft))];
end

figure
pcolor(slide,ks,spec.'), shading interp
set(gca, 'Ylim', [-60 60],'Fontsize',[14])
colormap(hot)
xlabel('t')
ylabel('omega')
colorbar


