% Mfile para plotar funcao spreading dado um determinado valor de
% spreading VEPK calculado no "onda1h.m" pela formulação de
% Krogstad (1998)
%
% Obs: VEPK=desvio padrao circular (ou sigma_theta)
%
% Autores: Jose Antonio/Andre Mendes/Guisela/Ricardo 23/Ago/2011
%
ks=input('Selecione se deseja entra com sigma (opção 1) ou fator s (opção 2):')
if ks == 1
   vepk=input('Entre com um determinado angulo spreading VEPK [graus]: ');
   % Formula de Longuet-Higgins que relaciona desvio padrao circular com s
   % obtido da tese do Andre Mendes
   s=(2/(vepk*pi/180).^2)-1;
else
   s=input('Entre com o fator de espalhamento s: ');
   % Formula de Longuet-Higgins que relaciona desvio padrao circular com s
   % obtido da tese do Andre Mendes
   vepk=sqrt(2/(1+s));
end
x=(-pi/4:pi/100:pi/4); % Angulos em graus
%


% Funcao que correlaciona o "s" com o "n"
a=0.5*(1+s*(s-1)/((s+1)*(s+2)));
n=(2*a-1)/(1-a);

% calculo do Angulo de 3dB (para correlacionar o nivel 0.5 do grafico com
% angulo de espalhamento)
ang3dB=2*acos(0.5.^(1/(2*s)))*180/pi;
disp('   vesp         s       ang3dB        n')
disp([vepk s ang3dB n])


% Calculo das funcoes de espalhamento
y1=cos(x).^n; % Funcao com "n"
y2=cos(x/2).^(2*s); % Funcao com "s"
figure;plot(x*180/pi,y1);grid on;hold on
plot(x*180/pi,y2,'r')
title(' Funcoes de espalhamento ')
legend(['cos(theta)**n n=',num2str(n)],['cos(theta/2)**2*s s=',num2str(s)])
%
c1=gamma(n/2+1)/(sqrt(pi)*gamma(n/2+0.5));
d1=c1*cos(x).^n;
c2=gamma(s+1)/(2*sqrt(pi)*gamma(s+0.5));
d2=c2*cos(x/2).^(2*s);
figure;plot(x*180/pi,d1);grid on;hold on
plot(x*180/pi,d2,'r')
title(' Directional spreading function (norma ISO 19901-1) ')
legend(['cos(theta)**n n=',num2str(n)],['cos(theta/2)**2*s s=',num2str(s)])

