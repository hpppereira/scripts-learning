%Gráficos de onda

load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000100_Convertido.gin.mat')
eta=WAVE1A(3400:3655);

etalc=size(eta);
x=(1:etalc(1,1))';
y=(1:etalc(1,1))';
ribbon(x,y,eta)