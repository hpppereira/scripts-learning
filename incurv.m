dado = input('Insira o nome do arquivo entre plics (''): ') %Entrar com o arquivo do tanque (elevação, tempo...(.gin.mat))
load(dado) %Carrega os dados

%converte os valores de elevação para metro
WAVE1=WAVE1*0.001;
WAVE1A=WAVE1A*0.001;
WAVE2A=WAVE2A*0.001;
WAVE3A=WAVE3A*0.001;
WAVE4A=WAVE4A*0.001;
WAVE5A=WAVE5A*0.001;
WAVE6A=WAVE6A*0.001;

figure (1)
subplot(5,1,1);
plot(WAVE1A); %Plot da elevação do sensor 1
ylabel('W1A')
title('Elevaçao')

subplot(5,1,2);
plot(WAVE2A); %%Plot da elevação do sensor 2
ylabel('W2A')

subplot(5,1,3);
plot(WAVE3A); %%Plot da elevação do sensor 3
ylabel('W3A')

subplot(5,1,4);
plot(WAVE4A); %Plot da elevação do sensor 4
ylabel('W4A')

subplot(5,1,5);
plot(WAVE5A); %Plot da elevação do sensor 5
ylabel('W5A')
xlabel('Registros')

pci = input('Defina o ponto de corte inicial da sua serie de dados: '); %Em qual registro vai começar
pcf = input('Defina o ponto de corte final da sua serie de dados: '); %Em qual registro vai terminar

w1acorte = WAVE1A(pci:pcf); % Atribui a elevação cortada à w1acorte 
w2acorte = WAVE2A(pci:pcf);
w3acorte = WAVE3A(pci:pcf);
w4acorte = WAVE4A(pci:pcf);
w5acorte = WAVE5A(pci:pcf);

'Numero de Pontos (NP)'
np=length(w1acorte) %Numero de pontos no registro cortado

figure (2)
subplot(5,1,1);
plot(w1acorte); %Plot da elevação cortada
ylabel('W1A-ct')
title('Elevaçao')

subplot(5,1,2);
plot(w2acorte);
ylabel('W2A-ct')

subplot(5,1,3);
plot(w3acorte);
ylabel('W3A-ct')

subplot(5,1,4);
plot(w4acorte);
ylabel('W4A-ct')

subplot(5,1,5);
plot(w5acorte);
ylabel('W5A-ct')
xlabel('Registros')


% INCLINAÇAO PONTOS EXTERNOS
%-----------------------------------------------

%Arranjo 1
n1a1 = w2acorte; %Origem
n2a1 = w3acorte; %Eixo x
n3a1 = w1acorte; %Eixo y
n4a1 = w4acorte; %Curvatura final
n5a1 = w5acorte; %Meio

%Lados
lxa1 = 1.005;
lya1 = 1.005;

%Inclinaçao A1
na1 = n1a1;
nxa1 = (n2a1-n1a1)/lxa1;
nya1 = (n3a1-n1a1)/lya1;
%-----------------------------------------------

%Arranjo 2
n1a2 = w1acorte; %Origem
n2a2 = w2acorte; %Eixo x
n3a2 = w4acorte; %Eixo y
n4a2 = w3acorte; %Curvatura final
n5a2 = w5acorte; %Curvatura inicial

%Lados
lxa2 = 1.010;
lya2 = 1.005;

%Inclinaçao A2
na2 = n1a2;
nxa2 = (n2a2-n1a2)/lxa2;
nya2 = (n3a2-n1a2)/lya2;

%-----------------------------------------------

%Arranjo 3
n1a3 = w1acorte; %Origem
n2a3 = w2acorte; %Eixo x
n3a3 = w4acorte; %Eixo y

%Lados
lxa3 = 1.010;
lya3 = 1.000;

%Inclinaçao A2
na3 = n1a3;
nxa3 = (n2a3-n1a3)/lxa3;
nya3 = (n3a3-n1a3)/lya3;
%-----------------------------------------------

%Arranjo 4
n1a4 = w3acorte; %Origem
n2a4 = w3acorte; %Eixo x
n3a4 = w2acorte; %Eixo y

%Lados
lxa4 = 1.005;
lya4 = 1.000;

%Inclinaçao A2
na4 = n1a4;
nxa4 = (n2a4-n1a4)/lxa4;
nya4 = (n3a4-n1a4)/lya4;
%-----------------------------------------------

%INCLINAÇAO PONTOS INTERNOS

%Arranjo interno 1
n1ai1 = w5acorte; %Origem
n2ai1 = w1acorte; %Eixo x
n3ai1 = w2acorte; %Eixo y

%Lados
lai1 = (1.010*sqrt(2))/2;

%Inclinaçao Ai1
nai1 = n1ai1;
nxai1 = (n2ai1-n1ai1)/lai1;
nyai1 = (n3ai1-n1ai1)/lai1;
%-----------------------------------------------

%Arranjo interno 2
n1ai2 = w5acorte; %Origem
n2ai2 = w3acorte; %Eixo x
n3ai2 = w2acorte; %Eixo y

%Lados
lai2 = (1.000*sqrt(2))/2;

%Inclinaçao Ai2
nai2 = n1ai2;
nxai2 = (n2ai2-n1ai2)/lai2;
nyai2 = (n3ai2-n1ai2)/lai2;
%-----------------------------------------------

%Arranjo interno 3
n1ai3 = w5acorte; %Origem
n2ai3 = w4acorte; %Eixo x
n3ai3 = w3acorte; %Eixo y

%Lados
lai3 = (1.005*sqrt(2))/2;

%Inclinaçao Ai2
nai3 = n1ai3;
nxai3 = (n2ai3-n1ai3)/lai3;
nyai3 = (n3ai3-n1ai3)/lai3;
%-----------------------------------------------

%Arranjo interno 4
n1ai4 = w5acorte; %Origem
n2ai4 = w4acorte; %Eixo x
n3ai4 = w1acorte; %Eixo y

%Lados
lai4 = (1.005*sqrt(2))/2;

%Inclinaçao Ai2
nai4 = n1ai4;
nxai4 = (n2ai4-n1ai4)/lai4;
nyai4 = (n3ai4-n1ai4)/lai4;
%-----------------------------------------------

%CURVATURA

%Curvatura Arranjo 1
nxxa1 = ((2*n1a1)-(2*n5a1)+n4a1)/(lxa1*sqrt(2));
nyya1 = ((2*n3a1)-(2*n5a1)+n2a1)/(lya1*sqrt(2));

%Curvatura Arranjo 2
nxxa2 = ((2*n1a2)-(2*n5a2)+n4a2)/(lxa2*sqrt(2));
nyya2 = ((2*n3a2)-(2*n5a2)+n2a2)/(lya2*sqrt(2));

n = na1;
nx = nxa1;
ny = nya1;
nxx = nxxa1;
nyy = nyya1;
registro = [n,nx,ny,nxx,nyy];
csvwrite('registroproc45.txt',registro)
%dirpr = cdir(na1,nxa1,nya1,nxxa1,nyya1);