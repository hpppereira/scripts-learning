'''
DAAT

Carlos Eduardo Parente
Henrique P P Pereira
Izabel C M Nogueira

Ultima modificacao: 21/07/2015

Descricao:

As wavelets serao calculadas para 3 ciclos - cada uma
correspondendo a um pico do espectro de 1D - para um numero de pontos
de uma wavelet de 3 ciclos multiplica--se o periodo acima por 3 e
divide-se por 1 exemplo para 20 segundos.

preparam-se entao as wavelets para os periodos das 5 faixas - com
aproximacao para numero inteiro de pontos

tamanha das wavelets, 3 vezes o periodo da faixa. caso nao tenha pico em
uma faixa, calcula-se com o periodo central da faixa (dado pelo vetor
picos1)

'''


#importa bibliotecas
import os
import time
from numpy import *
from pylab import *
import numpy as np
import matplotlib.pylab as pl
from scipy.signal import lfilter, filtfilt, butter
import espec
import pleds

reload(pleds)

pl.close('all')

#################################################
#dados de entrada
pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/bruto/series/'

#lista arquivos do diretorio atual do periodo escolhido
lista = []

for f in os.listdir(pathname):
	if f.startswith('adcp2_201304'):
		lista.append(f)

lista=np.sort(lista)

#intervalo de amostragem
dt = 1
fs = 1 / dt
nfft = 64
ncol = lista.shape[0]
dmag = -0


################################################################################
################################################################################


#tempo de inicio
tic = time.clock()

dire = np.zeros((10,ncol)) #direcao (2 valores, ate 5 faixas)
espe = np.zeros((10,ncol)) #espectros (2 valores, ate 5 faixas)
energ = np.zeros((10,ncol)) #Hs + 5 energias (uma por faixa), 4 picos (maiores)

#tabela de senos e cossenos para o metodo da maxima entropia
#cria variaveis a23 e a24, com 360 linhas (no matlab eh colunas),
#que faz um circulo de 1 a -1
ar, ai, br, bi = np.loadtxt('lyg2.txt', unpack=True)
a23 = ar + 1j * ai
a24 = br + 1j * bi

#mesmo circulo agora com 460 linhas (no matlab eh colunas)
a26 = np.array( list(a23[310:360]) + list(a23) + list(a23[0:50]) )
a27 = np.array( list(a24[310:360]) + list(a24) + list(a24[0:50]) )

#cria vetor de 0 a 360 iniciando em 311 e terminando em 50
a30 = np.array( range(311,361) + range(1,361) + range(1,51) )

#??
grad1 = 0.0175 ; grad2 = 180/pi

#o objetivo aqui eh ter wavelets prontas para usa-las de acordo com
#o pico das faixas; caso nao haja pico em uma faixa, usa-se  wavelets
#correspondentes a: faixa 1 - 14.28 s (55 pontos), faixa 2 - 9.52 s
#(37 pontos), faixa 3 - 7.76 s (30 pontos ) e faixa 5- 3 s (12 pontos)
mm = range(64,5,-1)
ms=[];

#cria vetores de dim 64,34
wavecos = np.zeros((64,len(mm)))
wavesen = np.copy(wavecos)

for i in range(len(mm)):

    mn = mm[i]
    ms.append(mn)

    #cria vetor de -pi a pi do tamanho de mn que eh o tamanho da wavelet
    out2 = np.array([np.linspace(-3.14,3.14,mn)][:])

    #cria janela de hanning para o tamanho da wavelet
    gau = np.hanning(mn) ; gau = resize(gau,(1,len(gau)))

    #cria wavelet cos
    out1 = (gau * cos(3 * out2)).T

    #cria wavelet sen
    out3 = (gau * sin(3 * out2)).T

    #coloca em cada coluna a wavelet de determinado
    #tamanho. cria 34 wavelets?
    wavecos[0:mn,i] = out1[:,0]
    wavesen[0:mn,i] = out3[:,0]


kkl = 0

for ik in range(0,len(lista),3):
    print str(ik+1) + ' - ' + lista[ik]

    ano = lista[ik][6:10]
    mes = lista[ik][10:12]

    co, dd, dc = np.loadtxt(pathname + lista[ik],unpack=True)

    #reamostra a serie caso foi amostrada em 2 hz
    # if len(eta) > 1024:
    # 	eta = eta[0,-1,2]

    # a wavelet sera gerada com as regras acima
    # serao calculadas as energias em cada faixa mencionada a partir do
    # espectro de uma dimensao considerando que o espalhamento entre cada
    # frequencia seja de 1/T

    #calculo do espectro de uma dimensao

    ww55 = zeros((10,1))
    qq1 = espec.espec1(co,nfft,fs)
    f1 = qq1[:,0]
    qq1 = qq1[:,1] #auto-espectro

    #intervalo de frequencia
    df = f1[1] - f1[0]

    #onda significativa (coloca a altura na primeira linha de ww5)
    ww55[0] = 4 * sqrt(sum(qq1) * df)

    #espectros nas 4 faixas - 32 gl
    ww55[1] = sum(qq1[1:5])
    ww55[2] = sum(qq1[5:7])
    ww55[3] = sum(qq1[7:14])
    ww55[4] = sum(qq1[14:33])

    #picos1 eh o valor da duracao da wavelet que sera usada
    #correspondendo a 3 ciclos do periodo de interesse

    #quando nao ha pico na faixa: 48=16s ; 27=9s ; 
    #18=6s ; 9=3s
    picos1 = np.array([48,27,18,9])

    #calcula a diferenca do vetor qq1 (ex: qq1[2] - qq1[1] = g1[1] )
    g1 = np.diff(qq1)

    #coloca 1 p/ valores >1, 0 p/ =0 e -1  <0
    g1 = np.sign(g1)

    #calcula a diferenca
    g1 = np.diff(g1)

    #acrescenta um valor no inicio de g1
    g1 = np.array( [0] + list(g1) )

    #acha indices dos picos
    g1 = pl.find(g1 == -2)

    #serao calculados os 4 maiores picos
    #acha os valores dos picos (g4) e indices dos picos (g5)
    #fica igual ao g1 (matriz com picos em ordem crescente)
    #retira valores maiores que 14 (pra tirar os picos em alta freq?)

    g4 = sort(qq1[g1])
    g5 = argsort(qq1[g1])
    g6 = flipud(g1[g5])
    g7 = g6[g6<14]

    #cria faixas de frequencia (periodo) - pq nao usa faixa 4?
    #no matlab esta transposto
    faixa1 = np.array([2,3]); ff1 = faixa1
    faixa2 = np.array([4,5,6]); ff2 = faixa2
    faixa3 = np.array([7,8,9]); ff3 = faixa3
    faixa4 = np.array([9,10,11,13,14]); ff4 = faixa4

    #colocacao dos picos nas primeiras faixas para determinacao das wavelets
    picos2 = np.zeros((4,1))

    for gh in range(len(g7)):

        #se o valor de g7[gh] estiver dentro da faixa1
        if g7[gh] in array(faixa1):
            picos2[0] = g7[gh]
            faixa1 = 0        	

        if g7[gh] in array(faixa2):
            picos2[1] = g7[gh]
            faixa2 = 0

        if g7[gh] in array(faixa3):
            picos2[2] = g7[gh]
            faixa3 = 0

        if g7[gh] in array(faixa4):
            picos2[3] = g7[gh]
            faixa4 = 0

    picos3 = picos1

    #valores dos picos para o arquivo final
    g5 = flipud(g5)
    g5 = g1[g5]
    g5 = list(g5) + [0,0,0,0]
    g5 = array(g5[0:4])
    g = find(g5 > array(0))

    #correcao henrique - o que faz?
    g5aux = []
    for i in range(len(g)):
        g5aux.append(64 / float(g5[i]))
    if len(g5aux) < 4:
        g5 = array(g5aux + [0,0,0,0])
        g5 = g5[0:4]

    #transforma em matriz de 4 col e 1 lin
    g5 = resize(g5,(len(g5),1))

    #preparo final do energ
    ww55[6:11] = g5
    energ[:,kkl] = ww55[:,0]

    #serao calculadas 5 faixas com wavelets
    #para cada wavelet calcula-se uma matriz de direcao
    #e desvio padrao obtendo-se um D(teta) para cada faixa

    for iwq in range(4):

        #acha dentro de mm o indice do valor de picos[iwq]
        g11 = find(picos1[iwq] == mm)

        #acha o valor do periodo da wavelet
        m = mm[g11[0]]

        #cria variavel out com a wavelet a ser utilizada (pega
        #as linhas e colunas da wavelet)

        out1 = wavecos[0:m,g11[0]]
        out3 = wavesen[0:m,g11[0]]
        matr1 = ones((20,90))
        m1 = 1024 - m

        #parametros para o calculo de tet2 e sp2
        m3 = m1 ; m1 = m1 - 1 ; m3 = m1
        m4 = 2 * dt / (m * 0.375) #para corrigir a janela de hanning. como eu ja corrigi em espec1, preciso fazer?
        m2 = m - 1

        ################################################################################
        ################################################################################
        ################################################################################

        #chama subrotina da daat

        #CODE daatwaverider21w calculates the main direction
        #for each segment with wavelet (morlet type);
        #the formulatuio of Lygre and Krogstad is used

        #usa-se a convolucao com a wavelet complexa

        a1 = lfilter((out1 - 1j * out3), 1, co)
        a2 = lfilter((out1 - 1j * out3), 1, dd)
        a3 = lfilter((out1 - 1j * out3), 1, dc)
        m4 = 2*dt / (m*0.375) #precisa fazer?

        #pq pegar a partir de m?
        a1 = a1[m-1:1025]
        a2 = a2[m-1:1025]
        a3 = a3[m-1:1025]

        #espectros cruzados
        z41 = a1
        z42 = a2
        z43 = a3

        #espectros cruzados
        a4 = m4 * (z41 * conj(z41))
        a8 = m4 * imag(z41 * (- conj(z42)))
        a9 = m4 * imag(z41 * (- conj(z43)))
        a20 = m4 * (z42 * conj(z42))
        a21 = m4 * (z43 * conj(z43))
        a25 = a20 + a21
        a7 = sqrt(a4 * a25)
        a12 = m4 * real(z42 * conj(z43))

        #a8 eh o cosseno, projecao no eixo W-E
        #a9 eh o seno, projecao no wixo S-N
        #o angulo c0 calculado eh em relacao ao eixo horizontal

        c0 = a8 + 1j * a9
        c1 = c0 / a7
        c01 = cos(c0)
        c02 = sin(c0)
        c03 = angle(mean(c01) + 1j * mean(c02))
        c03 = ceil(c03 * 360 / (2 * pi))
        c2 = (a20 - a21 + 1j * 2 * a12) / a25
        c0 = angle(c0) * 360 / (2 * pi)
        c0 = ceil(c0)
        p1 = (c1 - c2 * conj(c1)) / (1 - abs(c1) ** 2)
        p2 = c2 - c1 * p1
        tet2 = zeros((1,m3+2))

        #in order to avoid the ambiguity caused by 2teta the main 
        #direction calculated by Fourier techniques is used 
        #as a reference; the mem value is calculated in an interval
        #of 100 degrees around this value;

        for kl in range(m3+2):

            p3 = ceil(c0[kl])
            d = list(arange(p3,p3+100))
            z1 = 1 - p1[kl] * conj(a26[d]) - p2[kl] * conj(a27[d])
            z1 = z1 * conj(z1)

            #minimum of denominator is sufficient to
            #determine the maximum

            p5 = find(z1 == min(z1))
            p5 = p5[0]
            p7 = a30[p3 + p5 - 1]
            tet2[0,kl] = grad1 * p7

        tet2 = tet2.T
        sp2 = a4

		################################################################################
        ################################################################################
        ################################################################################
        
        #CODE daatbcampos22.m to select the segments for
        #the directional spectrum composition
        ################################################
        #Prepared by C.E. Parente
        ################################################

        it = 2 * (iwq - 1 + 1) + 1 #verificar, que teria que dar 1 e ta dando -1

        q1 = cos(tet2).T
        q2 = sin(tet2).T

        #Preparing ensembles of m segments advancing one sample

        #fr3 ia a matrix of cos and fr5 of sines of the segments whose direction
        #stability will be investigated
        #fr4 is the spectrum matrix

        pm = len(arange(round(m/2.0),m1-(m-round(m/2.0))))+1

        fr3 = zeros((round(m/2.0),pm))

        fr5 = copy(fr3)
        fr4 = copy(fr3)

        for ip in arange(round(m/2.0)):

            fr3[ip,:] = q1[0,ip:m1-(m-ip)+1]
            fr5[ip,:] = q2[0,ip:m1-(m-ip)+1]
            fr4[ip,:] = real(sp2[ip:m1-(m-ip)+1])

        #using the mean and the standard circular deviation
        #to select the segments with a given stability

        fr2a = mean(fr3.T, axis=1)
        fr2b = mean(fr5.T, axis=1)

        r = sqrt(fr2a ** 2 + fr2b ** 2)

        #circular deviation
        fr9 = sqrt(2 * (1 - r))

        #espectro medio por coluna
        fr45 = mean(fr4.T, axis=1)

        fr2 = angle(fr2a + 1j * fr2b)  #original

        #correcao para os valores ficarem entre 0 e 2pi
        g = find(fr2 < 0) ; fr2[g] = fr2[g] + 2 * pi
        g = find(fr2 > 2 * pi) ; fr2[g] = fr2[g] - 2 * pi

        g = len(fr2)
        a15 = 0
        zm = 0.5

        #segments with values of the standard deviations smaller
        #than the threshold are selected

        er5 = copy(fr45)

        b7 = find(fr9 < zm)

        a15 = fr2[b7]

        er4 = mean(fr4[:,b7], axis=0)

        #Correcting for declination
        # a15 is the final vector with selected direction values

        a15 = ceil(a15 * 360 / (2 * pi))

        #a15 = 90 + a15 - 14 (waverider santa catarina)
        #a15 = 90 + a15 - 21 (waverider de arraial)
        #a15 = 270 - a15 #axys
        a15 = a15 - 180 + dmag #adcp - ww3vale

        #correcao para ficar entre 0 e 360
        g = find(a15<0) ; a15[g] = a15[g] + 360
        g = find(a15>360) ; a15[g] = a15[g] - 350

        #caixas para acumulo e obtencao de D(teta)

        w1 = zeros((360,1)) #direcao principal
        w2 = zeros((360,1)) #ocorrencias

        a16 = copy(a15)

        if len(a15) > 1: #caso existam valores selecionados

            b1 = find(a15<=0) ; a15[b1] = a15[b1] + 360
            b1 = find(a15>360) ; a15[b1] = a15[b1] - 360

            #a15 = round(a15)

            for k in range(len(a15)):

                bb = a15[k]
                w1[bb-1] = w1[bb-1] + real(sp2[k])
                w2[bb-1] = w2[bb-1] + 1

        [b,t1] = butter(6,0.075)
        #b = resize(b,(len(b),1))
        #t1 = resize(t1,(len(t1),1))

        #filtrando w1 para determinar o D(teta)
        xx = array(list(w1[321:361]) + list(w1) + list(w1[0:41]))
        xx = xx[:,0]

        x = filtfilt(b,t1,xx)
        x = x[41:401]
        g = find(x<0)
        x[g] = 0

        #calculando as duas direcoes
        g1 = diff(x)
        g1 = sign(g1)
        g1 = diff(g1)
        g1 = array([0] + list(g1) )
        g1 = find(g1 == -2)

        p1 = sort(x[g1])
        p2 = argsort(x[g1])

        if len(p1) > 0:

            p = array(list(flipud(g1[p2])) + [0])
            p = p[0:2]

            e = array(list(flipud(p1)) + [0])
            e = e[0:2]

        #joga fora valores espacados menos de 50 graus
        if abs(p[0] - p[1]) < 20:

            p[1] = 0
            p[1] = 0

        elif e[1] < 0.1 * e[0]:

            e[1] = 0
            p[1] = 0

        z1 = ww55[iwq + 1]

        p = array(list(p) + [0,0,0])
        p = p[0:2]

        e = array(list(p) + [0,0,0])
        e = e[0:2]

        e = e * z1 / sum(e)

        dire[it-1:it+1,kkl] = p
        espe[it-1:it+1,kkl] = e

    kkl = kkl + 1

toc = time.clock()
texec = toc - tic


print 'Tempo de execucao DAAT (s): ', texec

espe1, dire1, energ1 = espe*10, dire, energ

#espe1 = espe[:,:-1:3]*10
#dire1 = dire[:,:-1:3]
#energ1 = energ[:,:-1:3]

pleds.pleds(espe1,dire1)

#return espe1, energ, dire1


