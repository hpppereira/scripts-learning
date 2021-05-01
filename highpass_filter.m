function [serie_filtrada] = highpass_filter (serie,dt,Thpass);
% Rotina para aplicar filtro high-pass (cos^32) em series temporais
% Dados de entrada:
% serie = serie temporal a ser filtrada com filtro passa-alta
% dt    = intervalo de tempo entre pontos da serie
% Thpass = periodo para atenuação da serie (mesma unidade de dt)
%          obs: frequencias com periodos maiores que este
%               valor Thpass serão atenuados
%
% Autores: J. Antonio / Ricardo Campos 01/Jun/2011
%

% Carregando dados da boia BMO-BR para teste (comentar depois)
% dado=load('serie_08_05_2011_08_55.dat');
% serie=dado(:,47); % heave
% serie=dado(:,44); % roll
% serie=dado(:,45); % pitch
nt=length(serie); % numero de pontos da serie temporal
n21=floor(nt/2)+1; % numero de pontos do espectro (nt/2 +1)
VF=(0:1/(nt*dt):1/(2*dt)); % Vetor de frequencias
%
Xs=fft(serie); % Calculando os coeficientes de Fourier Xs
[lin col]=size(Xs);if lin == 1;Xs=Xs';end
% 
% Aplicando filtro passa-alta (cos^32) para atenuar
% a função de transferência em frequencias mais baixas 
% que o valor fornecido pela variavel "Thpass"
k=find(VF <= 1/Thpass);kT=k(end);
highpass=ones(nt,1); % Criando vetor coluna com filtro passa-alta
filtro_passa_alta=(((1-cos(2*pi*(1:1:kT)./(2*kT)))/2).^32)'; %vetor coluna com filtro cos^32 
highpass(1:kT)= filtro_passa_alta; % primeiros kT pontos do filtro
highpass(nt-kT+1:end)=flipud(filtro_passa_alta); % ultimos kT pontos do filtro
%figure;plot(highpass,'b.');title('Funcao transferencia')
%
% Aplicando o filtro passa-alta nos primeiros n21 pontos dos
% coeficientes de Fourier
%disp(size(Xs))
%disp(size(highpass))
Xss=Xs.*highpass;
%figure(11);plot(abs(Xs),'b');hold on;plot(abs(Xss),'r');title('Coeficientes Xs'),legend('Xs original','Xss filtrado')
%
% Fazendo a transformada inversa de Fourier para recalcular a serie filtrada
serie_filtrada=real(ifft(Xss));
%figure;plot(serie,'b');hold on;plot(serie_filtrada,'r');legend('serie original','serie filtrada')
return