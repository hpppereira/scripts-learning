%aprendendo a usar a funcao spectrum como espectro cruzado e deixar ela parecida com a funcao
%espec2 do joao luiz
clear,clc%,close all

% volunsd de saida da spectrum
% 1 - ordem
% 2 - spec 1
% 3 - spec 2
% 4 - espec cruzado
% 5 - funcao trans?
% 6 - coerencia
%

%% carrega os dados
dados=load('200904221400.txt');

%% cria vetores com 1024 linhas
eta=dados(1:2^10,2);
etax=dados(1:2^10,3); %deslocamento norte
etay=dados(1:2^10,4); %deslocamento leste

%% grafico das series temporais
figure
subplot(3,1,1)
plot(eta), title('elevacao')
subplot(3,1,2)
plot(etax), title('deslocamento norte')
subplot(3,1,3)
plot(etay), title('deslocamento leste')

%% deltat
dt=0.7813571 ;

%% frequencia de nysquit
fny=1/(2*dt);

%% cria vetor de frequencia em funcao da frequencia de nysquit
f=(2*fny/length(eta):2*fny/length(eta):fny)';

%% calculo o espectro pela funcao espec
[aa]=espec(eta',dt);

%% calculo o espectro pela funcao spectrum com diferentes graus de liberdade g.l
aas1=spectrum(eta,1024); %espectro bruto  1024/1024=1 -> 1*2=2 g.l - cria arq com 512 pontos -> 1024/g.l
aas2=spectrum(eta,512); %1024/512=2 -> 2*2=4 g.l - cria arq com 256 pontos -> 1024/g.l
aas3=spectrum(eta,256); %=spectrum(eta), padrao, 2*4=8 g.l -> 1024/length(aas1)-1
aas4=spectrum(eta,128); %1024/128=8 -> 8*2=16 g.l (8*2 pq sao 2 amostras, a2 e b2?) - cria arq com 64 pontos -> 1024/g.l
%obs: a primeira linha eh a media
%     A coluna 2 gerada na saida da funcao spectrum representa o intervalo de confianca

%% calcula os graus de liberdade a partir do comprimento das series geradas
gl1=length(eta)/(length(aas1)-1);
gl2=length(eta)/(length(aas2)-1);
gl3=length(eta)/(length(aas3)-1);
gl4=length(eta)/(length(aas4)-1);

%% aplicar janela, perguntar para o partente qual janela
%Eh razoavel fazer o espectro com 1024 pontos, dividido em 256, com 50 % de
%overlapping utilizando a alisamento? ou janela ? de welch
% na funcao nao precisa colocar o nome 'welch', mas vou colocar para  lembrar
aas1=spectrum(eta,1024,512,'welch'); %2 gl
aas2=spectrum(eta,512,256,'welch');  %4 gl
aas3=spectrum(eta,256,128,'welch');  %8 gl
aas4=spectrum(eta,128,64,'welch');   %16 gl

%% Correcoess necessarias para a funcao fft e spectrum (perguntar para o parente)
% fft: - nao divide por N
%      - nao multiplica por dt
% spectrum: - divide por N
%           - nao multiplica por dt
% qual coluna da funcao spectrum�� a certa, a 1 ou 2? respo: a col 1
% multiplica por 2, por que?? fator de escala?

aas1=2*dt*aas1;
aas2=2*dt*aas2;
aas3=2*dt*aas3;
aas4=2*dt*aas4;

%% Calcula as alturas a partir dos espectros com diferentes g.l
%Altura Hm0 calculado pela espectro de eta - funcao espec
df=f(2)-f(1);

m0=0;
%Integral do espectro de eta
for i=1:length(aa)

    m0=m0+(aa(i,2)*df);

end

%Calculo da alt. sig, usando  momento espectral zero
Hm0=4.01*sqrt(m0);

%% Altura Hm01 calculado pela espectro de eta - funcao spectrum aas1
f1=(linspace(0,max(f),length(aas1)-1))';
df1=f1(2)-f1(1);

m01=0;
%Integral do espectro de eta
for i=1:length(aas1)

    m01=m01+(aas1(i,1)*df1);

end

%Calculo da alt. sig, usando  momento espectral zero
Hm01=4.01*sqrt(m01);

%% Altura Hm02 calculado pela espectro de eta - funcao spectrum aas2
f2=(linspace(0,max(f),length(aas2)-1))';
df2=f2(2)-f2(1);

m02=0;
%Integral do espectro de eta
for i=1:length(aas2)

    m02=m02+(aas2(i,1)*df2);

end

%Calculo da alt. sig, usando  momento espectral zero
Hm02=4.01*sqrt(m02);

%% Altura Hm03 calculado pela espectro de eta - funcao spectrum aas3
f3=(linspace(0,max(f),length(aas3)-1))';
df3=f3(2)-f3(1);

m03=0;
%Integral do espectro de eta
for i=1:length(aas3)

    m03=m03+(aas3(i,1)*df3);

end

%Calculo da alt. sig, usando  momento espectral zero
Hm03=4.01*sqrt(m03);

%% Altura Hm04 calculado pela espectro de eta - funcao spectrum aas4
f4=(linspace(0,max(f),length(aas4)-1))';
df4=f4(2)-f4(1);

m04=0;
%Integral do espectro de eta
for i=1:length(aas4)

    m04=m04+(aas4(i,1)*df4);

end

%Calculo da alt. sig, usando  momento espectral zero
Hm04=4.01*sqrt(m04);

%% grafico comparando os espectros
figure
subplot(2,2,1)
plot(linspace(0,max(f),length(aas1)-1),aas1(2:length(aas1),1)), title(['spectrum(eta,1024) - 1024/1024=1 -> 1*2=2 g.l - length = 512 / Hs= ',num2str(Hm0),', Hs1= ',num2str(Hm01)]), hold on
plot(aa(:,1),aa(:,2),'r'), hold off
subplot(2,2,2)
plot(linspace(0,max(f),length(aas2)-1),aas2(2:length(aas2),1)), title(['spectrum(eta,512) - 1024/512=2 -> 2*2=4 g.l - length = 256 / Hs= ',num2str(Hm0),', Hs2= ',num2str(Hm02)]), hold on
plot(aa(:,1),aa(:,2),'r'), hold off
subplot(2,2,3)
plot(linspace(0,max(f),length(aas3)-1),aas3(2:length(aas3),1)), title(['spectrum(eta,256) - 1024/256=1 -> 4*2=8 g.l - length = 128 / Hs= ',num2str(Hm0),', Hs3= ',num2str(Hm03)]), hold on
plot(aa(:,1),aa(:,2),'r'), hold off
subplot(2,2,4)
plot(linspace(0,max(f),length(aas4)-1),aas4(2:length(aas4),1)), title(['spectrum(eta,128) - 1024/128=1 -> 8*2=16 g.l - length = 64 / Hs= ',num2str(Hm0),', Hs4= ',num2str(Hm04)]), hold on
plot(aa(:,1),aa(:,2),'r'), hold off

%% Calculo do espectro cruzado pela funcao spectrum

% spectrum(serie1,serie2,subdivisoes,overlapping,'metodo')
bbsnnx=spectrum(eta,etax,256,128,'welch');
% bbsnnx=[aax aay aaxy functrans coer intconf1 intconf2 intconf3]
% aax= amplitude do espectro x
% aay = amplitude do espectro y
% aaxy = amplitud do espectro x e y

[aa2]=espec2(eta',etax',dt);

%espectro de fase
figure
plot(aa2(:,7))
clc
