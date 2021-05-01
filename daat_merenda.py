"""
Plotagem da PLEDS com Spreading
"""

import time as timem
from numpy import *
from pylab import *
import numpy as np
import matplotlib.pylab as pl
from scipy.signal import lfilter, filtfilt, butter
import espec
import os
import pandas as pd
from datetime import datetime
import matplotlib
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from datetime import datetime
import proconda

# pathname = '/media/hp/MOSKOWITZ/Database/Dados_PNBOIA_2017/data/recife/HNE/'
pathname = os.environ['HOME'] + '/GoogleDrive/AGES/data/boia_merenda/'

# data inicial e final para processar com base no nome do arquivo (YYMMDDHHMM.dat)
dat_ii = 'Onda_06110110.dat'
dat_ff = 'Onda_06113010.dat'


dmag = -23

h = 200 #profundidade 

nfft = 82 #numero de dados para a fft (p/ nlin=1312: 32gl;nfft=82, 16gl;nfft=164, 8gl;nfft=328)

fs = 1.28 #freq de amostragem

#intervalo de amostragem
dt = 1.0

#tempo de amostragem, pq 64? devido ao g.l?
x = dt * 64

# ------------------------------------------------------------------------------- #
# lis = np.sort(os.listdir(pathname))

# listap = []
# for li in lis:
# 	if li.startswith('201212'):
# 		listap.append(li)


list_dat = []
list_files = np.sort(os.listdir(pathname + 'brutos/'))
for l in list_files:
    if l.endswith('.dat'):
        list_dat.append(l)
list_dat = np.array(list_dat)


# lista de dados a serem processados

# indice do arquivo inidical e final para processar
ii = np.where(list_dat == dat_ii)[0][0]
ff = np.where(list_dat == dat_ff)[0][0]

listap = list_dat[ii:ff]

# stop

# stop

# local = pathname.split('/')[-3]

# print ('Processamento em... ' + local)

dire = np.zeros((10,len(listap))) #direcao (2 valores, ate 5 faixas)
espe = np.zeros((10,len(listap))) #espectros (2 valores, ate 5 faixas)
energ = np.zeros((10,len(listap))) #Hs + 5 energias (uma por faixa), 4 picos (maiores)
spread = np.zeros((len(listap),4)) #Hs + 5 energias (uma por faixa), 4 picos (maiores)

#dire1 = np.copy(dire)
#espe1 = np.copy(espe)

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
a30 = np.array( list(np.arange(311,361)) + list(np.arange(1,361)) + list(np.arange(1,51)) )

#??
grad1 = 0.0175 ; grad2 = 180/pi

#para o caso de usar matr1 (matriz de ocorrencias)
# sa=[.5,.5,.5,.5,0.1]

#o objetivo aqui eh ter wavelets prontas para usa-las de acordo com
#o pico das faixas; caso nao haja pico em uma faixa, usa-se  wavelets
#correspondentes a: faixa 1 - 14.28 s (55 pontos), faixa 2 - 9.52 s
#(37 pontos), faixa 3 - 7.76 s (30 pontos ) e faixa 5- 3 s (12 pontos)
# ES - 12 graus
# mm=[60;55;50;46;43;40;38;35;33;32;30;29;27;26;25;24;23;22;21;21;20;19;...
#     19;18;18;17;17;16;16;15;15;15;14;14;14;13;13;13;12;12;12;12;12;11;...
#     11;11;11;11;10;10;10;10;10;10;9];
# ES - 32 graus

#cria vetor com o tamanho das wavelets
# mm=[64;50;48;44;38;32;30;27;25;24;21;19;18;17;16;15;14;13;12;11;11;10;10;9;9;8;8;8;7;7;...
#     7;7;6;6;6];

# mm = range(64,5,-1)

# mm=[60,55,50,46,43,40,38,35,33,32,30,29,27,26,25,24,23,22,21,21,20,19,19,18,18,17,17,16,16,15,15,15,14,14,14,13,13,13,12,12,12,12,12,11,11,11,11,11,10,10,10,10,10,10,9]

mm=[64,50,48,44,38,32,30,27,25,24,21,19,18,17,16,15,14,13,12,11,10,9,8,7,6]

ms=[]

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


# stop
kkl = 0
# spread = [	]
# for ik in range(0,len(listap),3):
# for ik in range(p0,p1,3): #pula 3 arquivos para cada arq processado
for ik in range(len(listap)):

    filename = listap[ik]

    print (str(ik) + ' - DAAT - ' + filename)


    #atribui as variaveis em 'dados' e a data em 'data'
    # dados, data = dados_hne(pathname,listap[ik])

    # dd = np.loadtxt(pathname + listap[ik], skiprows=11)

    dff = pd.read_table(pathname + 'brutos/' + filename, skiprows=13, sep='\s+',
                       names=['heave','roll','pitch','compass'])

            # date in timestamp
    datet = pd.to_datetime(filename[-12:-4], format='%y%m%d%H')

    if len(dff) >= 1024 and dff.heave.max() > 0.5:

        # eta = dd[:,1]
        # etay = dados[0:1024,2]
        # etax = dados[0:1024,3]

        # print dd

        co = dff.heave.values
        dd = dff.roll.values
        dc = dff.pitch.values

        # stop

        ano = datet.year
        mes = datet.month

        ###################################################################
        # Calculo do Spreading

        hm0, tp, dp, sigma1, sigma2, sigma1p, sigma2p, f, df, \
        k, sn, snx, sny, snn, snnx, snny, snxny, snxnx, snyny, \
        a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(co,dd,dc,h,nfft,fs)

        spread[ik,:] = [hm0, tp, dp, sigma1p]

        # stop


        ###################################################################
        

        #limite superior (3db) e limite inferior (3 db)
        # 1) 20     11.1
        # 2) 11.1   8.69
        # 3) 8.69   7.4
        # 4) 7.4    4.0
        # 5) 4.0    end

        # a wavelet sera gerada com as regras acima

        # serao calculadas as energias em cada faixa mencionada a partir do
        # espectro de uma dimensao considerando que o espalhamento entre cada
        # frequencia seja de 1/T

        #calculo do espectro de uma dimensao

        ww55 = zeros((10,1))

        han = 1 #aplicacao da janela: han = 1 hanning ; han = 0 retangular

        gl = 32

        qq1 = espec.espec1(co,nfft,fs)

        f1 = qq1[:,0]

        qq1 = qq1[:,1] #auto-espectro

        #faixas em segundos
        #2     3    4
        #4     6    7.2
        #7.14  8    10.8
        #10.3  16   20.0

        #intervalo de frequencia
        df = f1[1] - f1[0]

        #onda significativa (coloca a altura na primeira linha de ww5)
        ww55[0] = 4 * sqrt(sum(qq1) * df)

        #cria faixas de frequencia (periodo) - pq nao usa faixa 4?
        #no matlab esta transposto
        faixa1 = np.array([2,3,4]) # 21.3 - 16.0
        faixa2 = np.array([5,6,7,8]) #12.8 - 8.0 
        faixa3 = np.array(range(9,16)) #7.1 - 4
        faixa4 = np.array(range(16,len(f1))) #3.7 - 1.5

        #espectros nas 4 faixas - 32 gl
        ww55[1] = sum(qq1[faixa1])
        ww55[2] = sum(qq1[faixa2])
        ww55[3] = sum(qq1[faixa3])
        ww55[4] = sum(qq1[faixa4])

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
        g4 = sort(qq1[g1])

        g5 = argsort(qq1[g1])

        #g5 = range(len(g4)-1,-1,-1)

        #fica igual ao g1 (matriz com picos em ordem crescente)
        g6 = flipud(g1[g5])

        #comeca criando a matriz com picos , pq??
        #g6 = array( list(g6)+[0,0,0,0] )

        #escolhe os 4 primeiros maiores?
        #g6 = g6[0:4]

        #retira valores maiores que 14 (pra tirar os picos em alta freq?)
        g7 = g6[g6<14]



        #colocacao dos picos nas primeiras faixas para determinacao das wavelets
        picos2 = np.zeros((4,1))

        for gh in range(len(g7)):

            #se o valor de g7[gh] estiver dentro da faixa1
            if g7[gh] in array(faixa1):

                #acha o indice da faixa1 que esta o g7(gh)
                #g8 = find(g7[gh] == faixa1)

                picos2[0] = g7[gh]

                faixa1 = 0          

            if g7[gh] in array(faixa2):

                #acha o indice da faixa1 que esta o g7(gh)
                #g8 = find(g7[gh] == faixa2)

                picos2[1] = g7[gh]

                faixa2 = 0

            if g7[gh] in array(faixa3):

                #g8 = find(g7[gh] == faixa3)

                picos2[2] = g7[gh]

                faixa3 = 0
            # print gh

        picos3 = picos1

        # # o que faz isso? (esta dando erro no proc do mes de maio de 2009)
        # for gh in range(4):

        #     if picos2[gh] > 0:

        #         picos1[gh] = round(3 * 1./f1[int(picos2[gh])-1])

        #valores dos picos para o arquivo final
        g5 = flipud(g5)
        g5 = g1[g5]
        g5 = list(g5) + [0,0,0,0]
        g5 = array(g5[0:4])
        g = find(g5 > array(0))

        #correcao henrique
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

            #acha o valor do periodo? da wavelet
            m = mm[g11[0]]

            #cria variavel out com a wavelet a ser utilizada (pega
            #as linhas e colunas da wavelet)

            out1 = wavecos[0:m,g11[0]]
            out3 = wavesen[0:m,g11[0]]

            #cria matriz com valores 1
            matr1 = ones((20,90))

            #perguntar p parente??
            m1 = 1024 - m

            #parametros para o calculo de tet2 e sp2
            m3 = m1 ; m1 = m1 - 1 ; m3 = m1
            m4 = 2 * dt / (m * 0.375) #para corrigir a janela de hanning
            #como eu ja corrigi em espec1, preciso fazer?

            m2 = m - 1

    # ==============================================================================#
    # ==============================================================================#
    #daatRS21_32.m

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

            # #a8 eh o cosseno, projecao no eixo W-E
            # #a9 eh o seno, projecao no wixo S-N
            # #o angulo c0 calculado eh em relacao ao eixo horizontal

            c0 = a8 + 1j * a9

            c0 = 270 - c0

            c1 = c0 / a7

            c01 = cos(c0)
            c02 = sin(c0)
            c03 = angle(mean(c01) + 1j * mean(c02))
            c03 = ceil(c03 * 360 / (2 * pi))

            c2 = (a20 - a21 + 1j * 2 * a12) / a25
            c0 = angle(c0) * 360 / (2 * pi)
            c0 = ceil(c0)
            # stop
            # c0 = 270 - c0 # correcao merenda

            c0[pl.find(c0 < 0)] = c0[pl.find(c0 < 0)] + 360

            # c00 = find(c0<=0)         ##pra que utiliza??
            # c0[c00] = c0[c00] + 360   ## nenhuma variavel criada aqui esta sendo utilizada
            # pq = ceil(mean(c0)) ##nao utiliza
            # pq = c03
            # g = find(pq <= 0)
            # pq[g] = pq[g] + 360

            p1 = (c1 - c2 * conj(c1)) / (1 - abs(c1) ** 2)
            p2 = c2 - c1 * p1

            tet2 = zeros((1,m3+2))

            #in order to avoid the ambiguity caused by 2teta the main 
            #direction calculated by Fourier techniques is used 
            #as a reference; the mem value is calculated in an interval
            #of 100 degrees around this value;

            henr1p = []
            henr2p = []

            for kl in range(m3+2):

                p3 = int(ceil(c0[kl]))

                d = list(arange(p3,p3+100))#.astype(int))

                z1 = 1 - p1[kl] * conj(a26[d]) - p2[kl] * conj(a27[d])

                z1 = z1 * conj(z1)

                #z1 = array([round(v,7) for v in real(z1)])

                #minimum of denominator is sufficient to
                #determine the maximum

                p5 = find(z1 == min(z1))
                p5 = p5[0]
                p7 = a30[p3 + p5 - 1]

                tet2[0,kl] = grad1 * p7


                #teste
                henr1p.append(p3)
                henr2p.append(tet2[0,kl] * 180/np.pi)

            tet2 = tet2.T

            sp2 = a4

            # ==============================================================================#
            # ==============================================================================#
            # daatRS22_32.m

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

            fr3 = zeros((int(round(m/2.0)),pm))

            fr5 = copy(fr3)
            fr4 = copy(fr3)

            for ip in arange(round(m/2.0)):

            	ip = int(ip)

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

            fr2 = angle(fr2a + 1j * fr2b)

            #correcao para os valores ficarem entre 0 e 2pi
            g = find(fr2 < 0) ; fr2[g] = fr2[g] + 2 * pi
            g = find(fr2 > 2 * pi) ; fr2[g] = fr2[g] - 2 * pi

            #g vai ser o comprimento do vetor
            g = len(fr2)

            #a15 = 0
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
            #usando o EtaEW e EtaNS ja esta descontado a dmag

            #corrige a declinacao magnetica
            a15 = a15 + dmag

            #correcao de convencao
            a15 = 270 - a15

            #corrige valores menores e maiores que 360
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

                    bb = int(a15[k])
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


spread = np.array(spread)

np.savetxt('espe.txt',espe, fmt='%.2f')
np.savetxt('dire.txt',dire, fmt='%.2f')
np.savetxt('energ.txt',energ, fmt='%.2f')
np.savetxt('spread.txt',spread, fmt='%.2f')
