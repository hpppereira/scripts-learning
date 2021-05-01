load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000100_Convertido.gin.mat')
eta1=WAVE1A(3400:3655);
load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000200_Convertido.gin.mat')
eta2=WAVE1A(3400:3655);
load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000300_Convertido.gin.mat')
eta3=WAVE1A(3400:3655);
load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000400_Convertido.gin.mat')
eta4=WAVE1A(3400:3655);

eta=[eta1;eta2;eta3;eta4]; %Varios T= 1,0 ; 1,7 ; 2,4 ; 3,1 ; 3.8
%%%% Cria eta com varios periodos

subplot(3,2,1)
plot(eta1);
subplot(3,2,2)
plot(eta2);
subplot(3,2,3)
plot(eta3);
subplot(3,2,4)
plot(eta4);
subplot(3,2,5)
plot(eta)

%Entrada para a rotina ESPEC

dt=0.04;
x=eta;

[aa]=espec(x,dt); %Calcula o espectro de eta
subplot(3,2,6)
plot(aa(:,1),aa(:,2))

%%% Gráfico 3D das ondas de varios periodos
figure
eta1=eta(1:100); %Eta com fase 1
eta2=eta(2:101); %Eta com fase 2
eta3=eta(3:102); %Eta com fase 3
eta4=eta(4:103); %Eta com fase 4

eta=[eta1 eta2 eta3 eta4]; %Cria matriz com 2 colunas de eta em diferença de fase
xx=(1:4)'; % Quantidade de colunas - necessario para criar grade
yy=(1:100)'; %Quantidade de linhas - necessario para crias grade
% [xx,yy]=meshgrid(xx,yy) % Interpolador para criar grade ??
%ribbon(eta) %Cria uma onda por coluna de eta
surf(xx,yy,eta) %Cria onda direcional devido a diferença de fase da col1 e col2 de eta
axis([1 4 1 150 -100 100]);

