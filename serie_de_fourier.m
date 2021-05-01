% Série de Fourier
a=[1:5];
T=0.4; %periodo de onda
w=2*pi/T;
t=linspace(0,2*pi/w,5); %tempo
f=0;
for i=1:length(a);
    f=f-sin (a(i)*w*t)/a(i); % Série de Fourier
end
plot(t,f,':p');
xlabel('tempo');
ylabel('Fourier');
title('Série de Fourier','fontsize',14);
