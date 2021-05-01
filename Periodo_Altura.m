clear
clc

            %%% Rotina de parametros de onda %%%
            
% Rotina para gerar ondas com a subrotina 'geraonda_alt_per' com Hs e Tp
% escolhida pelo usuário, e estimar esses parametros de onda pelo PP.
%%% Dados de entrada: 'Hs' e 'Tp'. O neta é atribuido à 'w1' e 1:length(neta) à 't1', respecativamente.
%%% Dados de saída: 2 matrizes: 'registro1' e 'registro2':
%[registro1]=[Hm Hmax Hmin Tc Tmax Tz celeridademed comprimentomed freqmed fangmed numondamed Tt]; do registro inteiro 
%[registro2]=[altura;periodo;frequencia;fang;comprimento;celeridade;numonda]; de cada onda 
%Obs: No registro2, cada linha está com a informação de um parametro para cada onda gerada no registro
%%% Cria Gráfico com o registro em 2D e 3D, e o espectro (freq,autoespec)
%%%SubRotinas chamadas: regressao / geraonda_alt_per / espec

%%% O comentario abaixo é para carregar os dados do tanque de ondas
%load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000100_Convertido.gin.mat');

% Achar a altura (H) máxima e minima e Periodo (T) da série temporal
% de ondas T000(dir=0º), do tanque de ondas do sensor WAVE1A

 %w1=WAVE1A(3477:4500);   %vetor de elevação de ondas ctes do tanque de ondas.
 %t1=tempo(3477:4500);   %vetor tempo do tanque de ondas

%Chamar sub rotina geraonda_alt_per para escolher altura e periodo.
% [neta,hsig]=geraonda_alt_per; %gera onda e cria as varias 'neta' e 'hsig'
% w1=neta; %Atribui a elevação 'neta' para 'w1'
% t1=(1:length(neta))'; %Cria registro de tempo para 1segundo=1registro

load('C:\Users\Henrique\Documents\MATLAB\T000\T000_000100_Convertido.gin.mat');
w1=WAVE1A(3477:4500);   %vetor de elevação de ondas ctes do tanque de ondas.
t1=tempo(3477:4500);   %vetor tempo do tanque de ondas

nm=mean(w1);    %elevação media
contza=0; %contador de zero ascendente
for i=1:1023 %se for usar os dados do tanque é melhor usar length(w1)
    if (w1(i)<nm & w1(i+1)>nm)
        contza=contza+1; %conta zero ascendente
        x=[t1(i) t1(i+1)]; %Cria vetor x(1x2) para fazer o calculo da regressao linear 
        y=[w1(i) w1(i+1)]; %%Cria vetor y(1x2) para fazer o calculo da regressao linear
        [b,a]=regressao(x,y); %chama subrotina de regressao linear
        xnm=(nm-b)/a; % Acha valor de x(tempo) para elevação=nm
        x_regonda(1,contza)=xnm; %coloca os valores do x para y=nm dos zeros ascendentes
        %matza(1,contza)=w1(i+1); %cria matriz com os valor de w1 (elevação) nos zeros ascendentes para f(x)=x+1
        matreg(1,i)=i; %Cria vetor com os indices de onde cruza o zero ascendente
    end
end
matreg=find(matreg); % Retira os zeros da matriz matreg, ficando só com os indices que cruza zero ascendente

for i=1:length(matreg)-1
    elmin(1,i)=min(w1(matreg(i):matreg(i+1))); %Acha elevação minima
    elmax(1,i)=max(w1(matreg(i):matreg(i+1))); %Acha elevação maxima
    altura(1,i)=elmax(1,i)-elmin(1,i); %Acha altura (el max - el min)
end

contonda=contza-1; % Conta quandas onda tem no registro
for i=1:contonda
    periodo(1,i)=x_regonda(1,i+1)-x_regonda(1,i); %Cria vetor com o periodo de cada onda
end

Hmax=max(altura); %Altura maxima do registro
Hmin=(min(altura)); % Altura minima do registro
Hm=mean(altura); %Altura média
Tmax=max(periodo); %Periodo maximo do registro
frequencia=1./periodo; %Frequencia 1/T (Hz)de cada onda
fang=2*pi./periodo; %Freq. Ang = 2pi/T de cada onda
comprimento=1.56*(periodo.^2); %comprimento de onda = 1.56T^2 (m)
celeridade=comprimento./periodo; %celeridade = L/T de cada onda (m/s)
celeridade1=1.56.*periodo; %celeridade =1.56*T de cada onda (m/s)
numonda=2*pi./comprimento; %vetor numero de onda de cada onda
Tt=length(t1); %Periodo total de amostragem
Tz=Tt/contza; %Periodo médio de zero ascendente (Tz=Tt/Nz) Tt= periodo total de amstragem / Nz= nº de onda de zero ascentente
Tc=Tt/contonda; %Periodo de crista
celeridademed=mean(celeridade); % celeridade media em m/s
comprimentomed=mean(comprimento); %comprimento medio
freqmed=mean(frequencia); %frequencia media
fangmed=mean(fang); %frequencia angular media
numondamed=mean(numonda); %num onda medio
[registro1]=[Hm Hmax Hmin Tc Tmax Tz celeridademed comprimentomed freqmed fangmed numondamed Tt];
[registro2]=[altura;periodo;frequencia;fang;comprimento;celeridade;numonda];
 

%Chama rotina de espectro
dt=t1(i)-t1(i-1); %Intervalo de tempo de amostragem para entrar na subrotina 'espec'
x=w1; %Coloca em x o valor de elevaçao para entrar na rotina 'espec'
[aa]=espec(x,dt); %chama subrotina espec
subplot(2,2,1:2)
plot(t1,x) %plot registro 2D
axis tight %Cria eixos nos limites de x e y
title('Registro de Ondas');
xlabel('Registros');
ylabel('Eta (m)'); % Se for com as ondas do tanque precisa mudar para 'mm'
subplot(2,2,3)
plot(aa(:,1),aa(:,2)) %Plot espectro
title('Espectro de Energia');
xlabel('Frequencia (Hz)');
ylabel('Auto Espectro de X');
subplot(2,2,4)
[x]=[w1 w1]; %Cria 2 colunas iguais com elevação para fazer a malha para plot 3D
sizex=size(x); %Para criar malha 3D
[xx,yy]=meshgrid(1:sizex(1,2),1:length(t1)); %Cria malha xx=nº colunas ; yy=nºlinhas
%mesh(xx,yy,x) % pode escolher entre mesh ou surf (1 ou outro)
surf(xx,yy,x) %Gráfico 3D
title('Registro de Ondas 3D')
ylabel('Registros');
zlabel('Eta (m)') % % Se for com as ondas do tanque precisa mudar para 'mm'
view(70,15) %Angulo para ver gráfico 3D
axis tight %Cria eixos nos limites de x e y


%Achar altura significativa (H1/3)
alt=sort(altura); %Colocar as alturas em ordem crescente
cont=length(altura); %Achar quantas alturas tem no vetor 'altura'
%sig=cont/3;
if rem(cont,3)==0
    sig=cont/3; %Separa as alturas em 1/3
    hsig=alt(cont-sig:length(alt));
    hsig=mean(hsig);
else
    cont=cont-1;
    if rem(cont,3)==0
       sig=cont/3;
       hsig=alt(cont-sig:length(alt));
       hsig=mean(hsig);
    else
        cont=cont-1;
        sig=cont/3;
        hsig=alt(cont-sig:length(alt));
        hsig=mean(hsig);
    end
end

        
        


    



