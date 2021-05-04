# Main DAAT program 
# Carlos E. Parente and Henrique P. P. Pereira 
# COPPE/UFRJ
# Created: 2018/11/19
# Last modification: 2021/03/05

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import mlab
from scipy.signal import lfilter, filtfilt, butter
from scipy.io import loadmat
from matplotlib.patches import Rectangle
from glob import glob
from IPython import get_ipython
import matplotlib.colors as mcolors
get_ipython().magic('reset -sf')
plt.close('all')
np.set_printoptions(suppress=True, precision=4) # print no terminal em notacao decimal

pathname_wave = '/home/hp/Dropbox/doutorado/dados/HNE_rio_grande_200905/'
listap = np.sort(glob(pathname_wave + '*.HNE'))
lyg2 = loadmat('lyg2.mat')

# criterio de aceitacao do desvio padrao dos segmentos
zm = 0.5

# table of sines and cosines for the MEM method - tecnica de maxima entropia
a23 = lyg2['a23']
a24 = lyg2['a24']
a26 = np.concatenate([a23[0][310:360],a23[0],a23[0][0:50]])
a27 = np.concatenate([a24[0][310:360],a24[0],a24[0][0:50]])
a30 = np.concatenate([np.arange(311,361),np.arange(1,361), np.arange(1,51)])

# frequencia de amostragem
fs = 1.28

# tamanho do segmento para fft
nfft = 328

# direcoes e espectro e spread
dire = np.zeros((10, 744)) * np.nan
espe = np.copy(dire)
spread = np.copy(dire)

# faixas dos espectros (periodo em segundos)
# fb = {'b1': [33.0, 10.6],
#       'b2': [10.6, 7.1],
#       'b3': [7.1, 4.2],
#       'b4': [4.2, 1.6]}

# indices das faixas
fb = {'b1': np.arange(8, 24),
      'b2': np.arange(24, 36),
      'b3': np.arange(36, 62),
      'b4': np.arange(62, 160)}

picos1 = np.array([43, 29, 23, 15, 9])

# # vetor do comprimento (frequencia) da wavelet
# mm = np.arange(70,8,-1)
# wavecos = np.zeros((mm[0], len(mm))) * np.nan
# wavesen = np.copy(wavecos)
# for i in np.arange(len(mm)):
#     out2_aux = np.linspace(-np.pi, np.pi, mm[i])
#     gau = np.hanning(mm[i]+2)[1:-1]
#     out1_aux = gau * np.cos(3*out2_aux)
#     out3_aux = gau * np.sin(3*out2_aux)
#     wavecos[:mm[i],i] = out1_aux
#     wavesen[:mm[i],i] = out3_aux

for ik in np.arange(0, len(listap), 1):
    print ('file - {}'.format(listap[ik]))

    # carrega os dados
    t, n1, n2, n3 = np.loadtxt(listap[ik], skiprows=11, unpack=True)


    qq1, f1 = mlab.psd(n1, NFFT=int(nfft), Fs=fs, detrend=mlab.detrend_mean,
                    window=mlab.window_hanning,noverlap=nfft/2)
    df = f1[3] - f1[2]

    # indices das faixas
    # ifb = {}
    # ifb['b1'] = np.where((1/f1<=fb['b1'][0]) & (1/f1>=fb['b1'][1]))[0]
    # ifb['b2'] = np.where((1/f1<=fb['b2'][0]) & (1/f1>=fb['b2'][1]))[0]
    # ifb['b3'] = np.where((1/f1<=fb['b3'][0]) & (1/f1>=fb['b3'][1]))[0]
    # ifb['b4'] = np.where((1/f1<=fb['b4'][0]) & (1/f1>=fb['b4'][1]))[0]

    # cria matriz varia
    ww55 = np.array([np.nan] * 10)
    ww55[0] = 4.01 * np.sqrt(np.sum(qq1) * df)
    ww55[1] = qq1[fb['b1'][0]]/2+sum(qq1[fb['b1']])+qq1[fb['b1'][-1]]/2
    ww55[2] = qq1[fb['b2'][0]]/2+sum(qq1[fb['b2']])+qq1[fb['b2'][-1]]/2
    ww55[3] = qq1[fb['b3'][0]]/2+sum(qq1[fb['b3']])+qq1[fb['b3'][-1]]/2
    ww55[4] = qq1[fb['b4'][0]]/2+sum(qq1[fb['b4']])+qq1[fb['b4'][-1]]/2

    qq2 = pd.Series(qq1).rolling(window=7, center=True).mean().bfill().ffill().values

    g1 = np.diff(qq2)
    g1 = np.sign(g1)
    g1 = np.diff(g1)
    g1 = np.r_[0, g1]
    g1 = np.where(g1 == -2)[0]
    energia_picos = qq2[g1]
    g5 = np.argsort(energia_picos) 
    g6 = g1[g5]
    g6 = np.flipud(g6)
    g6 = g6[g6>10]
    g5 = np.flipud(g5)
    g5 = g1[g5]
    g5 = np.r_[g5,0,0,0,0]
    g5 = g5[:4].astype(float)
    g = np.where(g5 > 0)[0]
    aux = g5[g].astype(float)
    g5[g] = 200./aux

    # faixa 1
    g7 = np.where(g6 > 9)[0]
    g8 = np.where(g6[g7] < 19)[0]
    g10 = g6[g7[g8]]
    if len(g10) > 0:
        picos1[0] = np.round(3.0*(1./f1[g10[0]]))
    # faixa 2
    g7 = np.where(g6 > 18)[0]
    g8 = np.where(g6[g7] < 24)[0]
    g10 = g6[g7[g8]]
    if len(g10) > 0:
        picos1[1] = np.round(3.0*(1./f1[g10[0]]))
    # faixa 3
    g7 = np.where(g6 > 23)[0]
    g8 = np.where(g6[g7] < 28)[0]
    g10 = g6[g7[g8]]
    if len(g10) > 0:
        picos1[2] = np.round(3.0*(1./f1[g10[0]]))
    # faixa 4
    g7 = np.where(g6 > 27)[0]
    g8 = np.where(g6[g7] < 51)[0]
    g10 = g6[g7[g8]]
    if len(g10) > 0:
        picos1[3] = np.round(3.0*(1./f1[g10[0]]))

    ww55[6:] = g5
    stop

    # loop for each frequency band
    for iwq in np.arange(len(picos1)):

        # acha o comprimento da wavelet
        g11 = np.where(picos1[iwq] == mm)[0]

        # 
        m = mm[g11[0]]

        out1 = wavecos[:m,g11[0]]
        out3 = wavesen[:m,g11[0]]
        # out3 = wavesen((1:m),g11(1));

        # ???
        m1 = 1200 - m


        # parametros para calculo de tet2 e sp2
        m3 = m1;
        m1 = m1-1;
        m3 = m1;
        m4 = 2*(1./fs)/(m*0.375); # acho que nao precisa
        m2=m-1;

        # %CODE daatwaverider21w calculates the main direction
        # %for each segment with wavelet (morlet type);
        # %the formulatuio of Lygre and Krogstad is used

        conv_n1 = lfilter((out1 + 1j * out3), 1, n1) #[wlsize-1:]
        conv_n2 = lfilter((out1 + 1j * out3), 1, n2) #[wlsize-1:]
        conv_n3 = lfilter((out1 + 1j * out3), 1, n3) #[wlsize-1:]


        m4 = 2*(1./fs)/(m*0.375) # idem ao de cima. retirar
        conv_n1 = conv_n1[m:1200]
        conv_n2 = conv_n2[m:1200]
        conv_n3 = conv_n3[m:1200]


        # length of wavelet (3 vezes o valor do periodo da faixa)
        # wlsize = int(3 * picos1[i])

        # x axis for wavelet
        # xwave = np.linspace(-np.pi, np.pi, wlsize)

        # gaussian wavelet format
        # gau = np.hanning(wlsize + 2)[1:-1]

        # create wavelet with sine and cossine
        # wavecos = gau * np.cos(3 * xwave)
        # wavesin = gau * np.sin(3 * xwave)

        # utiliza-se a convolucao com a wavelet complexa
        # conv_n1 = lfilter((wavecos + 1j * wavesin), 1, n1)[wlsize-1:]
        # conv_n2 = lfilter((wavecos + 1j * wavesin), 1, n2)[wlsize-1:]
        # conv_n3 = lfilter((wavecos + 1j * wavesin), 1, n3)[wlsize-1:]

        # espectros cruzados

        # correcao do espectro - ??
        # corr =  2.0 * (1/fs) / (wlsize * 0.375)
        corr = m4

        # espectros cruzados

        # espectro heave com wavelet - a4
        spec2_n1 = corr * np.real(conv_n1 * np.conj(conv_n1))

        # auto-spec roll - a20
        spec2_n2 = corr * np.real(conv_n2 * np.conj(conv_n2))

        # auto-spec pitch - a21
        spec2_n3 = corr * np.real(conv_n3 * np.conj(conv_n3))

        # cross-spec heave and roll, cosseno projecao no eixo W-E - a8
        spec2_n1n2 = corr * np.imag(conv_n1 * np.conj(conv_n2))

        # cross-spec heave and roll, seno projecao no eixo S-N - a9
        spec2_n1n3 = corr * np.imag(conv_n1 * np.conj(conv_n3))

        # espectro pitch e roll - a12
        spec2_n2n3 = corr * np.real(conv_n2 * np.conj(conv_n3))

        # sum of spec roll and pitch - a25
        sum_n2n3 = spec2_n2 + spec2_n3

        # raiz do auto-espec heave * soma espec de pitch e roll - a7
        square_n1_n2n3 = np.sqrt(spec2_n1 * sum_n2n3)

        # calculate direction with MEM

        # o angulo c0 calculado eh em relacao ao eixo horizontal - c0
        c0 = np.ceil(np.rad2deg(np.angle(spec2_n1n2 + 1j*spec2_n1n3)))

        # correcao para valores menores que zero
        c0[np.where(c0 <= 0)] = c0[np.where(c0 <= 0)] + 360

        # ???
        c1 = (spec2_n1n2 + 1j*spec2_n1n3) / square_n1_n2n3
        c2 = (spec2_n2 - spec2_n3 + 1j * 2 * spec2_n2n3) / sum_n2n3

        # ???
        p1 = (c1 - c2 * np.conj(c1)) / (1 - (np.abs(c1)) ** 2)

        # ???
        p2 = c2 - c1 * p1

        # in order to avoid the ambiguity caused by 2teta the main 
        # direction calculated by Fourier techniques is used 
        # as a reference; the mem value is calculated in an interval
        # of 100 degrees around this value

        tet2 = []
        # calculation for each segment
        for kl in np.arange(len(c0)):

           # arredonda para cima
           p3 = int(np.ceil(c0[kl]))

           # ???   
           d = np.arange(p3, p3+101).astype(int) - 1

           # ???
           z1_aux = 1 - p1[kl] * a26[d] - p2[kl] * a27[d]
           z1 = np.real(z1_aux * np.conj(z1_aux))

           # minimum of denominator is sufficient to determine the maximum     
           p5 = np.where(z1 == np.min(z1))[0][0]

           # p5=p5(1);
           p7 = a30[p3+p5-1]

           # main direction (MEM) for each segment
           tet2.append(np.deg2rad(p7))

        #
        sp2 = np.copy(spec2_n1)
        tet2 = np.array(tet2)

        #
        q1 = np.cos(tet2)
        q2 = np.sin(tet2)

        # Preparing ensembles of m segments advancing one sample
        # fr3 is a matrix of cos and fr5 of sines of the segments whose direction
        # stability will be investigated. fr4 is the spectrum matrix

        # comprimento do vetor descontando o comprimento da wavelet
        m1 = len(tet2) - 2

        #
        pm = len(np.arange(np.round(m/2), m1 - (m - 1 - np.round(m/2))))

        # cria matriz de zeros
        fr3 = np.zeros((int(np.round(m/2)), pm))
        fr4 = np.copy(fr3)
        fr5 = np.copy(fr3)

        #
        for ip in range(np.round(m/2).astype(int)):
            fr3[ip,:] = q1[ip:m1-(m-ip)+1]
            fr5[ip,:] = q2[ip:m1-(m-ip)+1]
            fr4[ip,:] = sp2[ip:m1-(m-ip)+1]

        # using the mean and the standard circular deviation
        # to select the segments with a given stability

        fr2a = np.mean(fr3, axis=0)
        fr2b = np.mean(fr5, axis=0)

        # 
        r = np.sqrt(fr2a** 2 + fr2b ** 2)

        # circular deviation
        fr9 = np.sqrt(2 * (1 - r))

        # indices dos valores que passaram no criterio
        b7 = np.where(fr9 < zm)[0]

        # selected spectrum values
        er4 = np.mean(fr4[:,b7], axis=0)

        # espectro medio por coluna
        fr2 = np.angle(fr2a + 1j * fr2b)

        # correcao para valores maiores ou menor que 2pi
        fr2[np.where(fr2 < 0)] = fr2[np.where(fr2 < 0)] + 2 * np.pi
        fr2[np.where(fr2 < 0)] = fr2[np.where(fr2 < 0)] - 2 * np.pi

        # selected directions(segments)
        a15_rad = fr2[b7]

        # a15 is the the final vector with selected direction values
        a15_deg = np.ceil(np.rad2deg(a15_rad))

        # correcao da declinacao e referencia
        a15_dmag = a15_deg -180 + dmag

        # correcao de direcao para valores maiores e menores que 0 e 360
        a15_dmag[np.where(a15_dmag < 0)] = a15_dmag[np.where(a15_dmag < 0)] + 360
        a15_dmag[np.where(a15_dmag > 360)] = a15_dmag[np.where(a15_dmag > 360)] - 360

        # caixas para acumulo e obtencao de D(teta)

        # direcao principal
        w1 = np.zeros(360)

        # ocorrencias
        w2 = np.zeros(360)

        # caso existam valores selecionados
        if len(a15_dmag[:1024]) > 1:

            # loop das direcoes
            for k in range(len(a15_dmag)):

                # valor da direcao em inteiro
                bb = int(a15_dmag[k])

                # soma as energias dentro da caixa de direcoes
                w1[bb] = w1[bb] + sp2[k]

                # soma as ocorrencias dentro da caixa de direcoes
                w2[bb] = w2[bb] + 1

        # filtrando w1 para determinar D(teta)
        [b, t1] = butter(6,0.075)        

        # concatena para fazer o overlap das janelas
        xx = np.concatenate((w1[320:360], w1, w1[0:40]))

        # filtra para os 2 lados. evita problemas de fase?
        x = filtfilt(b,t1,xx)

        # pega apenas o trecho da serie propria. remove a parte concatenada das extremidades
        x = x[40:400]

        # coloca zero nos valores negativos
        x[np.where(x < 0)] = 0

        # calculando 2 direcoes
        p_aux1 = np.diff(np.sign(np.diff(x)))
        p_aux2 = np.concatenate((np.array([0]), p_aux1))
        p_aux3 = np.where(p_aux2 == -2)[0]

        # ???
        pp1 = np.sort(x[p_aux3])
        pp2 = np.argsort(x[p_aux3])

        #
        if len(pp1) > 0:
            p = np.concatenate((np.flipud(p_aux3[pp2]), np.array([0])))[:2]
            e = np.concatenate((np.flipud(pp1), np.array([0])))[:2]

        # descarta valores espacados de menos de 20 graaus
        if np.abs(p[0] - p[1]) < 20:
            p[1] = 0
            e[1] = 0

        # descarta valores com energia pequena
        elif e[1] < 0.1 * e[0]:
            p[1] = 0
            e[1] = 0

        # normalizacao com as energias das faixas obtidas do espectro 1D
        # 
        # energia da faixa
        en = ww55[iwq+1]

        #
        pp = np.concatenate((p, np.array([0, 0, 0])))[:2]
        ee_aux1 = np.concatenate((e, np.array([0, 0, 0])))[:2]
        ee = ee_aux1 * en / np.sum(ee_aux1)

        # indice para montar o espe e dire
        it = 2 * (iwq - 1) + 2

        dire[it:it+2,kkl] = pp
        espe[it:it+2,kkl] = ee

    # return espe, dire





# if __name__ == "__main__":

    # pathname_wave = '/home/hp/Dropbox/doutorado/dados/HNE_rio_grande_200905/'
    # listap = np.sort(glob(pathname_wave + '*.HNE'))
    # lyg2 = loadmat('lyg2.mat')


    # df = pd.read_csv('/home/hp/Documents/pnboia/dados/fortaleza/pnboia_fortaleza.csv',
    #                  parse_dates=True, index_col='Datetime')
    # df = df['2017-01-01':'2017-11-30']
    # df = df.rolling(window=8, center=True).mean()
    # ws, wd = df.Wspd.values, df.Wdir.values

    # calcula o espe e dire com a daat
    # espe, dire = daat(lyg2, listap)

    # carrega o espe e dire ja calculado
    # espe = np.loadtxt('dados/espe1py_pnboia_fortaleza_filtrado.txt', delimiter=',')
    # dire = np.loadtxt('dados/dire1py_pnboia_fortaleza_filtrado.txt', delimiter=',')
    # ws1 = np.loadtxt('dados/ws1.txt', delimiter=',')
    # wd1 = np.loadtxt('dados/wd1.txt', delimiter=',')

    # dire1 = np.loadtxt('dados/direpy_pnboia_fortaleza.txt')

    # teste de direcao
    # espe[:,:] = np.nan
    # dire[:,:] = 0
    # espe[0,:] = 2
    # dire[0,:] = np.linspace(180,180,espe.shape[1])
    # ws[:] = np.nan

    # pleds('../fig/pledspy_pnboia', espe[:,::3], dire[:,::3], spread[:,::3], ws=None, wd=None, make_spread=False)

# pleds('pledspy', espe[:,::3]/3, dire[:,::3], spread=np.copy(dire), ws=None, wd=None, make_spread=False)
