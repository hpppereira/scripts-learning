%
% Gera dados para teste de ajuste exponecial de dados
%xdata = (0:.1:10)'; 
%ydata = 40 * exp(-.5 * xdata) + randn(size(xdata));

% Carrega dados para ajuste exponencial
%dado=load('vcar1_s2VTPK1.dat');
dado=load('vcar1_s2VTPK1.dat');
xdata=dado(:,1);
ydata=dado(:,4);

% Ajuste exponencial usando funçaõ fitcurvedemo
[estimates, model] = fitcurvedemo(xdata,ydata);
A=estimates(1);B=estimates(2);
disp('Ajuste exponencial para curva y=A*exp(-B*x):');
disp(['A=',num2str(A),'    B=',num2str(B)])

% Plotando resultados
plot(xdata, ydata, '*')
hold on
[sse, FittedCurve] = model(estimates);
plot(xdata, FittedCurve, 'r')
 
xlabel('xdata')
ylabel('f(estimates,xdata)')
title(['Fitting to function ', func2str(model)]);
legend('data', ['fit using ', func2str(model)])
hold off

% Plotando figura com grafico de Hs1 x s2_VTPK1
x=(1:0.5:max(xdata));y=A*exp(-B*x);figure;plot(x,y);grid on;
xlabel('x');ylabel('s2')
title('Ajuste exponencial');
legend(['y=',num2str(A),'*(-',num2str(B),'*x'])