from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl

plt.close('all')

def pleds(espe, dire, ws, wd, title=''):

    # cria figura
    fig = plt.figure(figsize=(8,9))
    ax = fig.add_subplot(111)
    plt.plot(0,'w')

    # limites dos eixos
    xmin, xmax, ymin, ymax = 0, 360, 0-9, 248+24
    plt.axis([xmin, xmax, ymin, ymax])
    plt.xticks([])
    plt.yticks([])

    # triangulos para plotagem
    ha = np.hanning(11)

    # titulo
    plt.text(22,248+30,'DIRECTIONAL WAVE SPECTRUM EVOLUTION (PLEDS) - %s' \
                      %(title))

    # cria retangulos
    ee = 5 #espacamento para comecar a escrever
    cr = 65 #comprimento dos retangulos
    at = 7 #altura dos triangulos

    ax.add_patch(Rectangle((0*cr, -8), cr, at, alpha=0.8, facecolor='r'))
    ax.text(ee+0*cr, -7, "21.3 - 16.0 s")

    ax.add_patch(Rectangle((1*cr, -8), cr, at, alpha=0.8, facecolor='y'))
    ax.text(ee+1*cr, -7, "12.8 - 07.1 s")

    ax.add_patch(Rectangle((2*cr, -8), cr, at, alpha=0.8, facecolor='g'))
    ax.text(ee+2*cr, -7, "06.4 - 04.0 s")

    ax.add_patch(Rectangle((3*cr, -8), cr, at,alpha=0.8, facecolor='b'))
    ax.text(ee+3*cr, -7, "03.7 - 01.5 s")

    plt.draw()

    # textos da legenda
    ax.text(ee+4*cr, -7, "5 div = 10 m/s & 0.1 m2", fontsize=9)

    #linhas verticais - divisoes a cada 20 graus - 18 setores
    # 1    2     3    4    5    6    7    8
    # N / NNE / NE / ENE / E / ESE / SE / SSE / S
    y = [10,248+24]
    for i in range(0,360,20):
        x = [i,i]
        plt.plot(x,y,'k',alpha=0.2)

    #linhas horizontais (dias)
    x = [0,360]
    dia = 0
    for i in range(10,248+10,8):
        dia += 1
        y = [i,i]
        plt.plot(x,y,'k',alpha=0.2)
        plt.text(-13,y[0]-2,str(dia).zfill(2))
        plt.text(363,y[0]-2,str(dia).zfill(2))

    #linhas horizontais (3 horas)
    x = [0, 360]
    for i in range(10,248+10,2):
        y = [i,i]
        plt.plot(x,y,'k',alpha=0.1)

    #plotagem do espectro direcional a cada dia por faixa de periodos
    #plota de cima para baixo (de 31 para 1)

    # coloca valores de direcao em graus
    for i in range(0, 360, 20):
        plt.text(i+3, 2, str(i).zfill(3), color='red', fontsize=10)

    # coloca valores de direcao rosa dos ventos
    ld = np.array(['N','NE','E','SE','S','SW','W','NW'])

    cont = 0
    for i in range(0, 360, 45):
        plt.text(i+2, 10, ld[cont], color='k', weight='bold')
        cont += 1

    # legenda dos dias
    plt.text(1.15,80,'days in a month',rotation=90)

    # contador para a plotagem na data correta
    cont = dire.shape[1]
    for t in range(dire.shape[1]-1,-1,-1):
        cont -= 1

        #indice das cores
        icor = -1

        #varia as 4 faixas
        for f in [0,2,4,6]:
            icor += 1
            arq5 = ['r','y','g','b']

            # eixo x (direcao) com largura fixa
            x = np.linspace(dire[f,t]-10, dire[f,t]+10, len(ha))

            # eixo y - hanning
            y = ha * espe[f, t] + cont

            # plotagem do triangulo
            plt.fill(x, y+10, arq5[icor], edgecolor='black', alpha=0.8)

    # vento (u e v)
    if ws != None:

        for t in np.arange(len(ws)-1,0,-1):
            s1 = ws[t]
            s2 = wd[t]

            if s1 > 0:
                s2 = s2/20
                st = t+9+10
                s2 = s2 + 3

                if s2 > 18:
                    s2 = s2 - 18

                s2 = s2 + 1

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

    return


if __name__ == '__main__':

    espe = np.loadtxt('../out/espe_buoy_merenda_200611.txt')
    dire = np.loadtxt('../out/dire_buoy_merenda_200611.txt')

    espe = espe * 2

    espe, dire = espe[:,::3], dire[:,::3]

    # coloca uma variacao randomica na direcao para melhor visualizacao
    dire = dire + np.random.rand(dire.shape[0],dire.shape[1]) * 20 - 20/2  #cria randomico
    # dire = pd.rolling(dire.T, 5, center=True).mean().T
    dire = pd.rolling_window(dire, window=5, win_type=None, min_periods=None, freq=None, center=False, mean=True, axis=1, how=None)

    #colocar 0.01 em vez nas direcoes igual a zero
    dire[np.where(dire == 0)] = 0.01

    title = 'BREMERENDA - Buoy - Nov/2006'

    pleds(espe, dire, ws=None, wd=None, title=title)

    # pl.savefig('../fig/%s' %figname ,format='png', bbox_inches='tight')
    plt.show()
