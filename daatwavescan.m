% Directional Analysis with Adaptive Techniques - DAAT
% Oceanographic Instrumentation Laboratory - LIOc-COPPE/UFRJ
% 
% Developed by:  Parente (1999)
% Contributions: Henrique P. P. Pereira
% Last modification: 2016/03/10
%

clear, clc, close all

%% carrega arquivos

%table of sines and cosines for the mem method - tecnica de maxima entropia
%cria variaveis a23 e a24, com 360 colunas, que faz um circulo de 1 a -1
load lyg2.mat;

%declinacao magnetica
dmag = -22; %santosrio grande

hv = load('heave.txt');
pt = load('pitch_corr.txt');
rl = load('roll_corr.txt');

wind = load('wind.txt');

ws = wind(:,1);
wd = wind(:,2) + dmag;

tic %inicia a contagem do tempo de processamento

%intervalo da amostragem (segundos)
fs = 1;
nfft = 128;

%% preparo dos arquivos

dire = zeros(10,744); %direcao (2 valores, ate  5 faixas)
espe = zeros(10,744); %espectros (2 valores, ate 5 faixas)
energ = zeros(10,744); %Hm0 + 4 energias (uma por faixa), valor zero, 4 picos (maiores)

%vetor de frequencias (verificar se esta correto)
dt = 1 / fs; %intervalo de amostragem
fny = 1 / (2 * dt); %freq de nysquit
x = dt * nfft; %auxiliar para o vetor de freq (pq 64)
f1 = 1/x:1/x:fny; %vetor de freq - verificar com parente
df=f1(2) - f1(1); %deltaf

%mesmo circulo mas agora com com 460 colunas
a26 = [a23(311:360) a23 a23(1:50)];
a27 = [a24(311:360) a24 a24(1:50)];

%cria vetor de 0 a 360, iniciando em 311 e terminando em 50
a30 = [(311:360) (1:360) (1:50)];

% ??
grad1 = 0.0175;
grad2 = 180/pi;

%para o caso de usar matr1 (matriz de ocorrencias)
sa = [.5;.5;.5;.5;0.1];

%as wavelets serao calculadas para 3 ciclos - cada uma
%correspondendo a um pico do espectro de 1D - para um numero de pontos
%de uma wavelet de 3 ciclos multiplica--se o periodo acima por 3 e
%divide-se por 1 exemplo para 20 segundos.

%preparam-se entao as wavelets para os periodos das 5 faixas - com
%aproximacao para numero inteiro de pontos

%tamanho das wavelets, 3 vezes o periodo da faixa. caso nao tenha pico em
%uma faixa, calcula-se com o periodo central da faixa (dado pelo vetor
%picos1)

%o objetivo aqui é ter wavelets prontas para usa-las de acordo com
%o pico das faixas; caso nao haja pico em uma faixa, usa-se wavelets
%correspondentes a: faixa 1 - 14.28 s (55 pontos), faixa 2 - 9.52 s
%(37 pontos), faixa 3 - 7.76 s (30 pontos ) e faixa 4 - 3 s (12 pontos)

%cria vetor com o tamanho das wavelets
mm = 64:-1:6;
ms = [];

%cria vetores de dim 64,34
wavecos = zeros(64,length(mm));
wavesen = wavecos;

for i = 1:length(mm)
    
    %wavelet atual
    mn = mm(i); 
    ms = [ms;mn];
    
    %cria vetoer de -pi a pi no tamanho de mn, que é o tamanho da wavelet
    out2 = linspace(-3.14,3.14,mn);
    
    %cria janela de hanning para o tamanho da wavelet
    gau = hanning(mn);
    
    %cria wavelet cos e sen
    out1 = gau'.* cos(3 * out2);
    out3 = gau'.* sin(3 * out2);
    
    %coloca em cada coluna a wavelet de determinado tamanho
    wavecos((1:mn)',i) = out1';
    wavesen((1:mn)',i) = out3';
end;

%% processamento

kkl = 0;

for ik = 1:744
    
    kkl = kkl + 1;

    co=hv(:,ik);
    dc=pt(:,ik);
    dd=rl(:,ik);

    %limite superior (3db) e limite inferior (3 db)
    % 1) 20     11.1
    % 2) 11.1   8.69
    % 3) 8.69   7.4
    % 4) 7.4    4.0
    % 5) 4.0    end
    % a wavelet sera gerada com as regras acima

    %serao calculadas as energias em cada faixa mencionada a partir do
    %espectro de uma dimensao considerando que o espalhamento entre cada
    %frequencia seja de 1/T

    %calculo do espectro de 1 dimensao
    ww55 = zeros(8,1);

    %calculo do espec (32 gl, 50% de overlap, alisamento de Welch)
    qq1 = spectrum(co,nfft,nfft/2,'welch');

    %correcao do fator de escala
    qq1 = 2 * qq1(2:end,1); 

    %coloca a altura significativa (hm0) na primeira linha de ww55)
    ww55(1) = 4 * sqrt(sum(qq1) * df);

    %cria faixas de freq (periodo)
    faixa1 = [6:11]'; % 21.3 - 11.6 s
    faixa2 = [12:15]'; % 10.6 - 8.5 s
    faixa3 = [16:31]'; % 8 - 4.1 s
    faixa4 = [32:length(qq1)]'; % 4 - 2 s

    %espectros nas 4 faixas - 32 graus
    ww55(2) = sum(qq1(faixa1)); 
    ww55(3) = sum(qq1(faixa2)); 
    ww55(4) = sum(qq1(faixa3)); 
    ww55(5) = sum(qq1(faixa4)); 
    %picos1 é o valor da duracao da wavelet que será usada
    %correspondendo a 3 ciclos do periodo de interesse

    %quando nao ha pico na faixa:
    % 48--16s
    % 27--9s
    % 18--6s
    % 9--3s

    picos1=[48;27;18;9];

    %picos calculados a partir de qq1        

    %calcula a diferença do vetor qq1 (ex qq1(2)-qq1(1)=g1(1) )
    g1 = diff(qq1);
    %coloca 1 para valores >1, 0 p/ =0 e -1 p/<0
    g1 = sign(g1);
    %calcula diferença (g1 ficou com 30 elementos)
    g1 = diff(g1);
    %deixa o vetor com 31 elementos
    g1 = [0;g1];
    %acha o indice do pico
    g1 = find(g1 == -2);

    %serao calculados os 4 maiores picos

    %acha os valores de energia dos picos (g4) e indices dos picos (g5)
    [g4 g5] = sort(qq1(g1));

    %coloca os indices em ordem crescente de energia
    g6 = flipud(g1(g5));
    %inicia criacao do vetor de picos (coloca zeros caso soh tiver 1
    %pico)
    g6 = [g6;0;0;0;0];
    %escolhe os 4 primeiros (maiores) picos
    g6 = g6(1:4);
    %retira valores maiores que 14 (para tirar picos na alta freq??)
    g7 = g6(g6<14);

    %colocacao dos picos nas primeiras faixas para determinacao das
    %wavelets

    picos2 = zeros(4,1);

    for gh = 1:length(g7)

        %acha o indice da faixa1 que esta o valor g7(gh)
        g8 = find(g7(gh)==faixa1);
        
        %se não for matriz vazia, cria variavel logica: ans = 0 e
        %picos2(1) recebe o valor do pico, se nao nao faz nada
        isempty(g8);
        if ans == 0
            picos2(1) = g7(gh);
            faixa1 = 0;
        end
            
        %acha o indice da faixa2 que esta o valor g7(gh)
        g8 = find(g7(gh)==faixa2);
        
        %se não for matriz vazia, cria variavel logica: ans = 0 e
        %picos2(2) recebe o valor do pico, se nao nao faz nada
        isempty(g8);
        if ans == 0
            picos2(2) = g7(gh);
            faixa2 = 0;
        end
            
        %acha o indice da faixa3 que esta o valor g7(gh)
        g8 = find(g7(gh)==faixa3);
        
        %se não for matriz vazia, cria variavel logica: ans = 0 e
        %picos2(3) recebe o valor do pico, se nao nao faz nada
        isempty(g8);
        if ans == 0
            picos2(3) = g7(gh);
            faixa3 = 0;
        end      

        %acha o indice da faixa4 que esta o valor g7(gh)
        g8 = find(g7(gh)==faixa4);
        
        %se não for matriz vazia, cria variavel logica: ans = 0 e
        %picos2(4) recebe o valor do pico, se nao nao faz nada
        isempty(g8);
        if ans == 0
            picos2(4) = g7(gh);
            faixa4 = 0;
        end      
            
    end

    %coloca o valor arredondado do pico * 3 em 'picos1'
    picos3 = picos1;    
    for gh = 1:4
         if picos2(gh) > 0
             picos1(gh) = round(3*1/f1(picos2(gh)));
         end
    end

    %valores dos picos para o arquivo final
    g5 = flipud(g5); %indices dos picos em ordem decrescente
    g5 = g1(g5); %indices dos picos em ordem crescente
    g5 = [g5;0;0;0;0]; %coloca zeros caso nao tiver picos?
    g5 = g5(1:4); %acha os 4 maiores picos
    g = find(g5>0); %acha valores de picos maior que zero
    g5(g) = 64./g5(g); %acha os periodos dos picos em ordem crescente 
    % (pq divide por 64?)

    %coloca os 4 periodos de pico na linha 7 a 10 do ww55
    ww55(7:10) = g5;

    % o valor do vetor ww5 (10 linhas) contem:
    % ww55 = [hm0, sp1, sp2, sp3, sp4, 0 , tp1, tp2, tp3, tp4]
    % hm0 - altura significativa
    % sp - somatorio do vetor de energia por faixa
    % tp - periodo de pico de cada faixa

    %preparo final do energ

    %coloca o valor de ww55 na coluna kkl do energ
    energ(:,kkl) = ww55;

    %serao calculadas 5 faixas com wavelets
    %para cada wavelet calcula-se uma matriz de direcao e desvio
    %padrao obtendo-se um D(teta) para cada faixa

    %faixas variando de 1 a 4
    for iwq = 1:4

        %acha dentro de 'mm' o indice do valor de picos1(iwq)
        g11 = find(picos1(iwq) == mm);

        %acha o valor da wavelet
        m=mm(g11(1));

        %cria variavel out com a wavelet com o tamanho de 'm' a ser
        %utilizada (pega as linhas e coluna da wavelet)
        out1=wavecos((1:m)',g11(1));
        out3=wavesen((1:m)',g11(1));

        %cria matriz de 1
        matr1=ones(20,90);

        %perguntar para o parente
        m1=1024-m;

        %parametros para o calculo de tet2 e sp2
        m3=m1;
        m1=m1-1;
        m3=m1;
        m2=m-1;

        daat1
        daat2

    end;
end;  

tempo_rodada = toc;

filtraventosiodoc
wd = ventosiodoc;

filtrasiodoc
dire = ddirsiodoc;

%matriz de saida a cada 3 horas
dire1 = dire(:,1:3:end); 
espe1 = espe(:,1:3:end) * 2; 
energ1 = energ(:,1:3:end);

ws1 = ws(1:3:end);
wd1 = wd(1:3:end);

%a pleds entra com o dire1 e espe1 que sao os dados espacados a cada 3h
pleds31dias

