
import time as timem
from numpy import *
from pylab import *
import numpy as np
import matplotlib.pylab as pl
from scipy.signal import lfilter, filtfilt, butter
import espec
import os
import pleds
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
matplotlib.reload(pleds)


def daathne(local, pathname, dmag, listap, h, nfft, fs):

    def lista_hne(pathname):

        lista = []
        for f in os.listdir(pathname):
            if f.endswith('.HNE'):
                lista.append(f)
        lista=np.sort(lista)

        return lista

    def dados_hne(pathname,arq):

        #le os dados a partir da 11 linha que sao numeros
        dados=np.loadtxt(pathname+arq, skiprows = 11)

        ano = arq[0:4]
        mes = arq[4:6]
        dia = arq[6:8]
        hora = arq[8:10]
        minuto = arq[10:12]

        data = [ano, mes, dia, hora, minuto]

        return dados,data

    print ('Processamento em... ' + local)


    dire = np.zeros((10,len(listap))) #direcao (2 valores, ate 5 faixas)
    espe = np.zeros((10,len(listap))) #espectros (2 valores, ate 5 faixas)
    energ = np.zeros((10,len(listap))) #Hs + 5 energias (uma por faixa), 4 picos (maiores)
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

    #intervalo de amostragem
    dt = 0.78

    #tempo de amostragem, pq 64? devido ao g.l?
    x = dt * 64

    kkl = 0

    #for ik in range(0,len(lista),3):
    # for ik in range(p0,p1,3): #pula 3 arquivos para cada arq processado
    for ik in range(len(listap)):

        print (str(ik) + ' - DAAT - ' + listap[ik])


        #atribui as variaveis em 'dados' e a data em 'data'
        dados, data = dados_hne(pathname,listap[ik])

        if len(dados) > 1000:

            eta = dados[0:1024,1]
            etay = dados[0:1024,2]
            etax = dados[0:1024,3]

            co = eta
            dc = etay
            dd = etax

            ano = int(data[0])
            mes = int(data[1])

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

                c1 = c0 / a7

                c01 = cos(c0)
                c02 = sin(c0)
                c03 = angle(mean(c01) + 1j * mean(c02))
                c03 = ceil(c03 * 360 / (2 * pi))

                c2 = (a20 - a21 + 1j * 2 * a12) / a25
                c0 = angle(c0) * 360 / (2 * pi)
                c0 = ceil(c0)

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

                    p3 = ceil(c0[kl])

                    d = list(arange(p3,p3+100))

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

    # toc = timem.clock()
    # texec = toc - tic


    # espe1 = espe[:,:-1:3] * 2
    # dire1 = dire[:,:-1:3]
    # energ1 = energ[:,:-1:3]

    # ws1 = ws[:-1:3]
    # wd1 = wd[:-1:3]

    #chama a pleds
#    pleds.pleds(espe1,dire1,ws1=None,wd1=None)

    #plota energia de cada faixa
#    a = np.linspace(0,espe.shape[1]/24,espe.shape[1])

 #   pl.figure(figsize=(8,8))
 #   pl.plot(energ[4,:],a)
 #   pl.axis('tight')

    # print ('Tempo de execucao DAAT (s): ', texec)

    return espe, dire, energ


    #henr1p = np.array(henr1p)
    #henr2p = np.array(henr2p)


def pleds(espe1,dire1,ws1,wd1,figname,date):

    #colocar 0.01 em vez nas direcoes igual a zero
    dire1[np.where(dire1 == 0)] = 0.01

    ad = np.array(['Jan','Fev','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])


    fig = plt.figure(figsize=(8,8))

    ax = fig.add_subplot(111)


    a = 0
    plt.plot(a,'w')
    plt.axis([-0.1,20.2,0,300])

    v6 = np.hanning(15)
    v61 = np.hanning(11)

    ad1 = np.array([31,29,31,30,31,30,31,31,30,31,30,31]) #???

    plt.axis('off')

    # arq2 = np.array(([ [1,0.00,0],
    #                  [1,0.00,0],
    #                  [1,0.55,0],
    #                  [1,0.55,0],
    #                  [1,1.00,0],
    #                  [1,1.00,0],
    #                  [0,1.00,0],
    #                  [0,1.00,0] ]))

    col = np.array([0.7,0.7,0.7])

    ax.set_position([0,0,1,1]) # set a new position

    # #codigo de cores para faixas de periodos
    # x = np.array([0.5,3,3,0.5]) + 0.5
    # y = np.array([1,1,12,12]) - 3.5


    ax.add_patch(Rectangle((0,3), 3.3, 8,alpha=0.8,facecolor='r'))
    ax.text(0.5,4.5, "21.3-16.0 s")

    ax.add_patch(Rectangle((3.3, 3), 3.3, 8,alpha=0.8,facecolor='y'))
    ax.text(3.8,4.5, "12.8-7.1 s")

    ax.add_patch(Rectangle((6.6, 3), 3.3, 8,alpha=0.8,facecolor='g'))
    ax.text(7.1,4.5, "6.4-4.0 s")

    ax.add_patch(Rectangle((9.9, 3), 3.3, 8,alpha=0.8,facecolor='b'))
    ax.text(10.4,4.5, "3.7-1.5 s")

    ax.add_patch(Rectangle((13.2, 3), 3.3, 8,alpha=0.8,facecolor='w'))
    ax.text(13.5,4.5, "5 div=10 m/s")

    ax.add_patch(Rectangle((16.5, 3), 3.3, 8,alpha=0.8,facecolor='w'))
    ax.text(16.8,4.5, "5 div=0.1 m2")

    plt.draw()

    #linhas verticais
    y = np.array([20,283])
    for i in range(1,20):
        x = [i,i]
        pl.plot(x,y,'k',alpha=0.2)

    #linhas horizontais (dias)
    x = np.array([0.9,19.1])
    dia = 0
    for i in range(20,260+8,8):
        dia += 1
        y = [i,i]
        pl.plot(x,y,'k',alpha=0.3)
        pl.text(0.3,y[0],str(dia))
        pl.text(19.3,y[0],str(dia))

    #linhas horizontais (3 horas)
    x = np.array([1,19])
    for i in range(20,284,2):
        y = [i,i]
        pl.plot(x,y,'k',alpha=0.2)

    pl.text(1.13,286,'DIRECTIONAL WAVE SPECTRUM - Santos ' + date + ' - PNBOIA (AXYS 3M)')


    #plotagem do espectro direcional a cada dia por faixa de periodos
    #plota de cima para baixo (de 31 para 1)

    #eixo horizontal de direcao
    a = np.arange(310,720,20)
    a[pl.find(a>360)] = a[pl.find(a>360)] - 360

    for i in range(1,19):
        pl.text(i+0.15,15,str(a[i-1]),color='red',fontsize=11)


    ld = np.array(['NW','N ','NE','E ','SE','S ','SW','W ','SW','W '])

    k = 1.55;
    d = np.arange(1.75,13,2.25)

    for i in range(8):
        pl.text(k,20.8,ld[i],weight='bold')
        k=k+2.25;
     
    pl.text(1.15,80,'days in a month',rotation=90)

    #w=[[1;6] [2;7] [3;8] [4;9]];
    #bb = np.array([0.3]*10) #utilizado para montar o triangulo??

    for t in range(dire1.shape[1]-1,0,-1):

        #define os vetores de direcao e espectro (energia)
        s1 = dire1[:,t]
        s2 = espe1[:,t]

        #varia as 4 faixas
        cor = -1
        for i in [0,2,4,6]:

            # arq5 = arq2[i,:] #cor - fazer com 'r', 'b', ... ??

            cor += 1
            arq5 = ['r','y','g','b']

            s11 = s1[i] #valor da direcao no tempo i
            s12 = s2[i] #valor do espectro no tempo i

            b1 = s11 / 20 #direcao (correcao para o eixo??)
            b2 = s12 / 2  #espectro

            if b1 > 0:
                b1 = b1 + 3 #ajuste da direcao

                if b1 > 18:
                    b1 = b1 - 18

                b1 = b1 + 1 #o zero comecaem 111 (ou 11??)
                n1 = t + 9 + 10 #shift na escala vertical

                #monta um triangulo (x)
                v7 = np.linspace(b1-0.3,b1+0.3,len(v61))
                x = np.array(list(v7) + list(np.flipud(v7)))

                #cria un hanning
                y = np.array( list(n1+v61*b2) + list(n1*np.ones(len(v61))))

                # ??
                z1 = 1
                z2 = 1

                if b2 * b1 > 0:

                    pl.fill(x,y,arq5[cor])



    #####################################################
    #vento (u e v)

    if ws1 != None:

        for t in np.arange(len(ws1)-1,0,-1):

            s1 = ws1[t]
            s2 = wd1[t]

            if s1 > 0:

                s2 = s2/20
                st = t+9+10
                s2 = s2 + 3

                if s2 > 18:

                    s2 = s2 - 18

                s2 = s2 + 1

                #s1 eh a velocidade do vento, colocada na escala certa
                #1 divisao=2m/s
                #s2 eha direcao em caixas de 18 graus
                #st eh a posicao de plotagem ao logo da vertical

                x = [s2-0.05,s2+0.05,s2+0.05,s2-0.05]
                y = [st,st,st+s1,st+s1]

                if s2 < 2:

                    x = np.nan
                    y = np.nan

                if s2 > 18:

                    x = np.nan
                    y = np.nan

                if s1 > 0:

                    pl.fill(x,y,'w')

                if s1 > 10:

                    pl.fill(x,y,'y')

                if s1 >20:

                    pl.fill(x,y,'g')




    #pl.savefig('pledspy.eps',format='eps', dpi=1200
    #pl.savefig('pledspy.pdf',format='pdf', dpi=1200)
    pl.savefig('fig/PLEDS_SAN_2013/pledspy_' + figname + date + '.png',format='png')
    
    plt.show()

    return


def pledscur(espe1,dire1,ws1,wd1):

    #colocar 0.01 em vez nas direcoes igual a zero
    dire1[np.where(dire1 == 0)] = 0.01

    ad = np.array(['Jan','Fev','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    
    
    fig = plt.figure(figsize=(8,10),facecolor='w')
    ax = fig.add_subplot(111)
    ax.set_position([0,0,1,1]) # set a new position
    
    ax.plot( 0, 'w')
    
    xaxis = [-0.1,20.2]
    yaxis = [0, 300]
    
    ax.set_xlim(xaxis)
    ax.set_ylim(yaxis)
    
    #ax.axis([-0.1,20.2,0,300])
    
    v6 = np.hanning(15)
    v61 = np.hanning(11)
    
    ad1 = np.array([31,29,31,30,31,30,31,31,30,31,30,31]) #???
    
    plt.axis('off')
    
    # arq2 = np.array(([ [1,0.00,0],
    #                  [1,0.00,0],
    #                  [1,0.55,0],
    #                  [1,0.55,0],
    #                  [1,1.00,0],
    #                  [1,1.00,0],
    #                  [0,1.00,0],
    #                  [0,1.00,0] ]))
    
    #col = np.array([0.7,0.7,0.7])
    
    
    # #codigo de cores para faixas de periodos
    # x = np.array([0.5,3,3,0.5]) + 0.5
    # y = np.array([1,1,12,12]) - 3.5
    
    
    ax.add_patch(Rectangle((0,0), 3.3, 8,alpha=0.8,facecolor='#2c7fb8'))
    ax.text(0.5,1.5, "Prof: 5 m")
    
    ax.add_patch(Rectangle((3.3, 0), 3.3, 8,alpha=0.8,facecolor='#41b6c4'))
    ax.text(3.8,1.5, "Prof: 16 m")
    
    ax.add_patch(Rectangle((6.6, 0), 3.3, 8,alpha=0.8,facecolor='#a1dab4'))
    ax.text(7.1,1.5, "Prof 36 m")
    
    ax.add_patch(Rectangle((9.9, 0), 3.3, 8,alpha=0.8,facecolor='#ffffcc'))
    ax.text(10.4,1.5, "Prof: 46 m")
    
    ax.add_patch(Rectangle((13.2, 0), 3.3, 8,alpha=0.8,facecolor='w'))
    ax.text(13.5,1.5, "5 div=10 m/s")
    
    ax.add_patch(Rectangle((16.5, 0), 3.3, 8,alpha=0.8,facecolor='w'))
    ax.text(16.8,1.5, "5 div=0.1 m2")
    
    pl.draw()
    
    #linhas verticais
    y = np.array([20,283])
    for i in range(1,20):
        x = [i,i]
        ax.plot(x,y,'k',alpha=0.2)
    
    #linhas horizontais (dias)
    x = np.array([0.9,19.1])
    dia = 0
    for i in range(20,260+8,8):
        dia += 1
        y = [i,i]
        ax.plot(x,y,'k',alpha=0.3)
        ax.text(0.3,y[0],str(dia))
        ax.text(19.3,y[0],str(dia))
    
    #linhas horizontais (3 horas)
    x = np.array([1,19])
    for i in range(20,284,2):
        y = [i,i]
        ax.plot(x,y,'k',alpha=0.2)
    
    # ax.text(1.13,286,'DIAGRAMA DE PARENTE - CORRENTES')
    
    
    #plotagem do espectro direcional a cada dia por faixa de periodos
    #plota de cima para baixo (de 31 para 1)
    
    #eixo horizontal de direcao
    # a = np.arange(310,720,20)
    # a[pl.find(a>360)] = a[pl.find(a>360)] - 360
    
    a = np.arange(350,760,20)
    a[pl.find(a>360)] = a[pl.find(a>360)] - 360
    
    for i in range(1,19):
        ax.text( i+0.15,15, str(a[i-1]), color='red', fontsize=11)
        if i == 18:
            ax.text( i+0.92,15, '[graus]', color='red', fontsize=8)
            ax.text( i+0.9,10, u'[direção]', color='black', fontsize=8)
    
    
    ld = np.array(['N ','NE','E ','SE','S ','SW','W ','NW', 'W ', 'NW'])
    
    k = 1.55;
    d = np.arange(1.75,13,2.25)
    
    for i in range(8):
        ax.text( k,10, ld[i], weight='bold')
        k = k+2.25
    
    
    ax.text( 1.15, 80, u'[dd/%s/%s]'%(ad[0],2015), fontsize=14, weight='bold', rotation=90)
    # Xaxis = np.linspace(xaxis[0],xaxis[1],espe1.shape[1])
    # ax.axvspan(0,10 , ymin=4*5, ymax=9*5, color='w') 
    
    
    for t in range(dire1.shape[1]-1,-1,-1):
        #define os vetores de direcao e espectro (energia)
        s1 = dire1[:,t]
        s2 = espe1[:,t]
    
        #varia as 4 faixas
        cor = -1
        for i in [0,2,6,8]:
    
            ## Cores das janelas hanning para cada profundidade
            cor += 1
            arq5 = ['#2c7fb8','#41b6c4','#a1dab4','#ffffcc']
    
    
    
            s11 = s1[i] #valor da direcao no tempo i
            s12 = s2[i] #valor do espectro no tempo i
    
            b1 = s11 / 20 # corrigindo direcao ao eixo
            b2 = s12 / 2  # espectro
    
            if b1 > 0:
                b1 = b1 + 1 # ajuste da direcao
    
                if b1 > 18:
                    b1 = b1 - 18
    
                b1 = b1 + 1     # o zero comecaem 111 (ou 11??)
                n1 = t + 9 + 10 # shift na escala vertical
    
                #monta um triangulo (x)
                v7 = np.linspace( b1-0.3, b1+0.3, len(v61))
                x = np.array( list(v7) + list( np.flipud(v7) ) )
    
                #cria un hanning
                y = np.array( list(n1+v61*b2) + list( n1*np.ones(len(v61)) ) )
    
                # ??
                z1 = 1
                z2 = 1
    
                if b2 * b1 > 0:
                    ax.fill(x,y,arq5[cor])
    
    
    
    #####################################################
    #vento (u e v)
    
    for t in np.arange( len(ws1)-1, -1, -1):
    
        s1 = ws1[t]
        s2 = wd1[t]
    
        if s1 > 0:
    
            s2 = s2/20
            st = t+9+10
            s2 = s2 + 1
    
            if s2 > 18:
    
                s2 = s2 - 18
    
            s2 = s2 + 1

            #s1 eh a velocidade do vento, colocada na escala certa
            #1 divisao=2m/s
            #s2 eha direcao em caixas de 18 graus
            #st eh a posicao de plotagem ao logo da vertical

            x = [s2-0.05,s2+0.05,s2+0.05,s2-0.05]
            y = [st,st,st+s1,st+s1]

            if s2 < 2:

                x = np.nan
                y = np.nan

            if s2 > 18:

                x = np.nan
                y = np.nan


            if s1 > 0:
                ax.fill(x,y,'k', lw=0.4, edgecolor='magenta')
            elif s1 > 10:
                ax.fill(x,y,'y')
            elif s1 >20:
                ax.fill(x,y,'r')

    
    # fig.savefig( FIGdir + 'pleds_jan2015.pdf', dpi=200 )
    
    # plt.show()


def preppledsSWAN(pathname,filename):

    '''
    Programa principal para ler o arquivo do
    SWAN e fazer a PLEDS para 7 dias

    '''

    f = open(pathname + filename)

    aux = (10,745)
    espe = np.zeros(aux)
    dire = np.zeros(aux)

    lines = f.readlines()

    latlon = lines[7]

    cont = -1
    hm0  = []
    tp   = []
    dp   = []
    datam = []
    spc1dm=np.zeros((745,25)) #########################################botar numero de frequencias do modelo

    for i in range(len(lines)):

        #recupera vetor de frequencia
        if lines[i][0:5]=='AFREQ':
            print ('Linha do vetor de frequencia: ' + str(i)) 
            nfreq = int(lines[i+1][0:10]) #tamanho do vetor de freq
            vfreq = np.array(lines[i+2:i+2+nfreq]).astype(float)

        #recupera o vetor de direcao
        if lines[i][0:4]=='NDIR':
            print ('Linha do vetor de direcao: ' + str(i))
            ndir = int(lines[i+1][0:10]) #tamanho do vetor de freq
            vdire = np.array(lines[i+2:i+2+ndir]).astype(float)

        #recupera os espectros, integra, corrige com o fator de correcao
        #separa as 4 faixas de frequencia, calcula a energia e direcao
        #para cada faixa

        if lines[i][0:6] == 'FACTOR':
            cont += 1
            print (cont)
            print ('Data do Espectro: ' + lines[i-1][0:15])

            datam.append(datetime.strptime(lines[i-1][0:15], '%Y%m%d.%H0000'))

            fator = float(np.array(lines[i+1]).astype(float))
            print ('fator') 
            print (fator)
            print ('')
            #cria array com o espe2d
            espec2d = []
            for j in range(nfreq):
                espec2d.append(lines[i+2+j].split())
            
            #transpoe o espe2d para ficar freqXdire
            espe2d = np.array(espec2d).T.astype(float) * fator
            espe1d = np.sum(espe2d,axis=0)

            #corrige o vetor de direcao
            #vdire[pl.find(vdire < 0)] = vdire[pl.find(vdire < 0)] + 360

            #cria matriz espe (para a pleds)
            #print cont, fx1, espe.shape

            #interpola vetor de frequencia e espectro 1d
            vfreqi   = np.arange(0, vfreq.max(), 0.001) #frequencia interp
            vdirei_aux = range(0,360,1)
            vdirei  = np.linspace(vdire.max(), vdire.min(), len(vdirei_aux)) 
            espe1di = np.interp(vfreqi, vfreq, espe1d) #espectro interp
            espe2di = np.array([np.interp(vfreqi, vfreq, espe2d[i,:]) for i in range(espe2d.shape[0])]) #freq
            espe2di = np.array([np.interp(vdirei_aux, np.linspace(0,360,len(espe2d)), espe2di[:,i]) for i in range(espe2di.shape[1])]).T #dire

            ####################################################################
            #frequency vector - linear???

            nf = len(vfreq)
            nd = len(vdire)
            freq = vfreq #np.linspace(min(vfreq),max(vfreq),len(vfreq))

            # DF in frequency (dfim) . Nelson Violante and Fred Ostritz       
            fretab = np.zeros((nf),'f')
            dfim   = np.zeros((nf),'f') 

            fre1 = freq[0] 
            fretab[0] = fre1
            co = freq[(nf-1)]/freq[(nf-2)] 
            dfim[0] = (co-1) * np.pi / nd * fretab[0] 

            for ifre in range(1,nf-1):
                fretab[ifre] = fretab[ifre-1] * co 
                dfim[ifre] = (co-1) * np.pi / nd * (fretab[ifre]+fretab[ifre-1]) 

            fretab[nf-1] = fretab[nf-2]*co
            dfim[nf-1] = (co-1) * np.pi / nd * fretab[(nf-2)]       
            
            ####################################################################

            #significant wave height
            #fator de correcao (espectros em m2/Hz/degr)
            #2*pi*rad=360;
            #1rad=360/(2*pi)=57.3;
            print (espe1d)
            espe1d=espe1d*57.3

            espe1d = espe1d *dfim 
            spc1dm[cont,:]=espe1d
            # pl.figure()
            # pl.plot(freq,spc1dm[0,:],'o')
            # pl.show()

            # stp
            hm0.append(4.01 * np.sqrt(sum(espe1d)))
            # print m0
            # print hm0
            # print dfim
            # pl.figure()
            # pl.plot(dfim,'o')
            # pl.figure()
            # pl.plot(freq,espe1d,'o-')
            # pl.twinx()
            # pl.plot(freq,m0,'ro-')
            # pl.show()

            # return

            tp.append(1/vfreq[pl.find(espe1d == espe1d.max())[0]])

            #direcao de pico
            sdp = espe2d.max(axis=1)
            idp = pl.find(sdp == max(sdp))[0]
            dp.append(vdire[idp])


            #w.dr = np.interp(w.fr, w.f, w.sn1[:,1]) #dire interp

            #define as faixas (automatizar em funcao do vetor de freq)
            fx1 = np.arange(0,7)
            fx2 = np.arange(7,11)
            fx3 = np.arange(11,16)
            fx4 = np.arange(16,len(vfreq))

            espe[0,cont] = np.sum(espe1d[fx1])
            espe[2,cont] = np.sum(espe1d[fx2])
            espe[4,cont] = np.sum(espe1d[fx3])
            espe[6,cont] = np.sum(espe1d[fx4])

            # achar a escala dos graficos em funcao do Hs
            hs01=4.01 * np.sqrt(espe[0,cont])
            hs02= 4.01 * np.sqrt(espe[2,cont])
            hs03= 4.01 * np.sqrt(espe[4,cont])
            hs04= 4.01 * np.sqrt(espe[6,cont])
            hst=np.sqrt(hs01**2 + hs02**2 + hs03**2 + hs04 **2)



            #print hs01,hs02,hs03,hs04,hst,cont,hm0

            #return

            #cria matriz de direcao (para a pleds)
            
            #interpola o espectro 2d
            
            #salva figura do espectro 2d
            # pl.figure()
            # pl.contour(vfreq, vdire, espe2d)
            # pl.xlabel('Freq (Hz)')
            # pl.ylabel('Dir (graus)')
            # pl.savefig('espe2d/' + lines[i-1][0:15] + '.png')
            # pl.close('all')

            #salva figura do espectro 1d
            # pl.figure()
            # pl.plot(vfreq,espe1d,'-o')
            # pl.plot(vfreq[fx1],espe1d[fx1],'-o')
            # pl.plot(vfreq[fx2],espe1d[fx2],'-o')
            # pl.plot(vfreq[fx3],espe1d[fx3],'-o')
            # pl.plot(vfreq[fx4],espe1d[fx4],'-o')
            # pl.savefig('espe1d/' + lines[i-1][0:15] + '.png')
            # pl.close('all')

            #faz o somatorio das energias de cada faixa para cada direcao (24 direcoes) - integra em frequencia
            #soma as linhas 
            #soma as energia das faixas (para verificar o indice da direcao)
            # s1 = np.sum(espe2d[:,fx1],axis=1)
            # is1 = pl.find(s1 == max(s1))[0]
            # s2 = np.sum(espe2d[:,fx2],axis=1)
            # is2 = pl.find(s2 == max(s2))[0]
            # s3 = np.sum(espe2d[:,fx3],axis=1)
            # is3 = pl.find(s3 == max(s3))[0]
            # s4 = np.sum(espe2d[:,fx4],axis=1)
            # is4 = pl.find(s4 == max(s4))[0]

            #indice da maxima energia
            is1 = pl.find(espe2d[:,fx1].max(axis=1) == espe2d[:,fx1].max(axis=1).max())[0]
            is2 = pl.find(espe2d[:,fx2].max(axis=1) == espe2d[:,fx2].max(axis=1).max())[0]
            is3 = pl.find(espe2d[:,fx3].max(axis=1) == espe2d[:,fx3].max(axis=1).max())[0]
            is4 = pl.find(espe2d[:,fx4].max(axis=1) == espe2d[:,fx4].max(axis=1).max())[0]

            dire[0,cont] = vdire[is1]
            dire[2,cont] = vdire[is2]
            dire[4,cont] = vdire[is3]
            dire[6,cont] = vdire[is4]

            #espectro integrado
            # espe_int = np.sum(espe2d, axis=0)

            # dire[0,cont] = vdire[fx1][pl.find(espe_int[fx1] == max(espe_int[fx1]))][0]
            # dire[2,cont] = vdire[fx2][pl.find(espe_int[fx2] == max(espe_int[fx2]))][0]
            # dire[4,cont] = vdire[fx3][pl.find(espe_int[fx3] == max(espe_int[fx3]))][0]
            # dire[6,cont] = vdire[fx4][pl.find(espe_int[fx4] == max(espe_int[fx4]))][0]


    #limita os valores para a quantidade valores

    #valores horarios
    espe1 = espe[:,:cont] #* 50
    aux = pl.rand(10,espe1.shape[1]) * 20 - 20/2  #cria randomico
    dire1 = dire[:,:cont] + aux

    #espectro a cada 3 horas com rand
    # espe1 = espe[:,0:-1:3] * 20
    # aux = pl.rand(10,espe1.shape[1]) * 10 - 5 
    # dire1 = dire[:,0:-1:3] + aux


    # return espe1, dire1, vfreq, vdire, espe1d, espe1di, espe2d, espe2di, hm0, tp, dp, spc1dm, dfim, datam
    return espe1, dire1, vfreq, vdire, espe1d, espe1di, espe2d, espe2di, hm0, tp, dp, spc1dm



def pledsSWAN(espe1,dire1,tit,dia):

    #colocar 0.01 em vez nas direcoes igual a zero
    dire1[np.where(dire1 == 0)] = 0.01

    ad = np.array(['Jan','Fev','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])


    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)

    a = 0
    plt.plot(a,'w')
    plt.axis([-0.1,20.2,0,300])

    v6 = np.hanning(15)
    v61 = np.hanning(11)

    ad1 = np.array([31,29,31,30,31,30,31,31,30,31,30,31]) #???

    plt.axis('off')

    # arq2 = np.array(([ [1,0.00,0],
    #                  [1,0.00,0],
    #                  [1,0.55,0],
    #                  [1,0.55,0],
    #                  [1,1.00,0],
    #                  [1,1.00,0],
    #                  [0,1.00,0],
    #                  [0,1.00,0] ]))

    col = np.array([0.7,0.7,0.7])

    ax.set_position([0,0,1,1]) # set a new position

    # #codigo de cores para faixas de periodos
    # x = np.array([0.5,3,3,0.5]) + 0.5
    # y = np.array([1,1,12,12]) - 3.5


    ax.add_patch(Rectangle((0,3), 3.3, 8,alpha=0.8,facecolor='r'))
    ax.text(0.5,4.5, "25.0-13.1 s")

    ax.add_patch(Rectangle((3.3, 3), 3.3, 8,alpha=0.8,facecolor='y'))
    ax.text(3.8,4.5, "11.8-08.5 s")

    ax.add_patch(Rectangle((6.6, 3), 3.3, 8,alpha=0.8,facecolor='g'))
    ax.text(7.1,4.5, "07.7-05.0 s")

    ax.add_patch(Rectangle((9.9, 3), 3.3, 8,alpha=0.8,facecolor='b'))
    ax.text(10.4,4.5, "04.5-01.0 s")

    ax.add_patch(Rectangle((13.2, 3), 3.3, 8,alpha=0.8,facecolor='w'))
    ax.text(13.5,4.5, "5 div=10 m/s")

    ax.add_patch(Rectangle((16.5, 3), 3.3, 8,alpha=0.8,facecolor='w'))
    ax.text(16.8,4.5, "5 div=0.1 m2")

    plt.draw()

    #linhas verticais
    y = np.array([20,284])
    for i in np.arange(1,20):
        x = [i,i]
        pl.plot(x,y,'k',alpha=0.2)

    #linhas horizontais (dias)
    x = np.array([0.9,19.1])
    #dia = 0
    for i in np.arange(20,284,37):
        dia += 1
        y = [i,i]
        pl.plot(x,y,'k',alpha=0.3)
        pl.text(0.3,y[0],str(dia))
        pl.text(19.3,y[0],str(dia))


    #linhas horizontais (1 hora)
    x = np.array([1,19])
    for i in np.arange(20,284,1.5416):
        y = [i,i]
        pl.plot(x,y,'k',alpha=0.2)


    #pl.text(1.13,286,'DIRECTIONAL WAVE SPECTRUM - Previsao - ADCP Vale')
    pl.text(1.13,286,tit)


    #plotagem do espectro direcional a cada dia por faixa de periodos
    #plota de cima para baixo (de 31 para 1)

    #eixo horizontal de direcao
    a = np.arange(310,720,20)
    a[pl.find(a>360)] = a[pl.find(a>360)] - 360

    for i in range(1,19):
        pl.text(i+0.15,15,str(a[i-1]),color='red',fontsize=11)


    ld = np.array(['NW','N ','NE','E ','SE','S ','SW','W ','SW','W '])

    k = 1.55;
    d = np.arange(1.75,13,2.25)

    for i in range(8):
        pl.text(k,20.8,ld[i],weight='bold')
        k=k+2.25;
     
    pl.text(1.15,80,'days in a month',rotation=90)

    #w=[[1;6] [2;7] [3;8] [4;9]];
    #bb = np.array([0.3]*10) #utilizado para montar o triangulo??

    #for t in range(dire1.shape[1]-1,-1,-1):
    t = dire1.shape[1]
    for tt in np.arange(278,20-1.542/2,-1.542):
        t -= 1
        print (t)
        print (tt)

        #define os vetores de direcao e espectro (energia)
        s1 = dire1[:,t]
        s2 = espe1[:,t]

        #varia as 4 faixas
        cor = -1
        for i in [0,2,4,6]:

            # arq5 = arq2[i,:] #cor - fazer com 'r', 'b', ... ??

            cor += 1
            arq5 = ['r','y','g','b']

            s11 = s1[i] #valor da direcao no tempo i
            s12 = s2[i] #valor do espectro no tempo i

            b1 = s11 / 20 #direcao (correcao para o eixo??)
            b2 = s12 / 2  #espectro

            if b1 > 0:
                b1 = b1 + 3 #ajuste da direcao

                if b1 > 18:
                    b1 = b1 - 18

                b1 = b1 + 1 #o zero comecaem 111 (ou 11??)
                n1 = tt #shift na escala vertical

                #monta um triangulo (x)
                v7 = np.linspace(b1-0.3,b1+0.3,len(v61))
                x = np.array(list(v7) + list(np.flipud(v7)))

                #cria un hanning
                y = np.array( list(n1+v61*b2) + list(n1*np.ones(len(v61))))
                

                # ??
                z1 = 1
                z2 = 1

                if b2 * b1 > 0:

                    pl.fill(x,y,arq5[cor],alpha=.9)



    pl.savefig('pledspy_SWAN.png')

    plt.show()

    return

