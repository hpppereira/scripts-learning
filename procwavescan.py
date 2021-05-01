'''

### Processamento

Processamento dos dados brutos da boia Wavescan do projeto SIODOC
Processamento dos dados da boia do SIODOC com a DAAT/PLEDS

Dados brutos: heave, pitch, roll e compass

a) Verificar a necessidade da correcao
das series de heave, pitch e roll

b) Verificar com Parente ou Candella como corrige as series de pitch 
e roll com o compass (manual ndbc96 ?? )
c) As matrizes tem dimensao de 3020x1030 - as series estao em linha??

              0  1   2  3  4   5       6,7,8, ...
d) Formato: YYYY,MM,DD,hh,mm?,ss?, --> serie ....
'''

# ================================================================================== #
#### Modulos utilizados
# ================================================================================== #

import os
import sys
import numpy as np
import pylab as pl
import scipy.io
import time
from datetime import datetime
import proconda
import pandas as pd
# import consiste_bruto
# import consiste_espec
# import consiste_proc
# import daat
# import relatorio
# import graficos_axys
# import jonswap
import waveproc
reload(waveproc)
from waveproc import WaveProc

reload(proconda)
# reload(consiste_bruto)
# reload(consiste_espec)
# reload(consiste_proc)
# reload(daat)
# reload(relatorio)
# reload(graficos_axys)
# reload(jonswap)

# pl.close('all')

# ================================================================================== #
#### Dados de entrada
# ================================================================================== #

# #localizacao
# local = 'Arraial do cabo/RJ' # relatorio
# local1 = 'arrcabo_siodoc' #nome do arquivo salvo
# latlon = '-22.995 / -42.187 ' #relatorio
# idargos = '--'
# idwmo = '--'

#caminho onde estao os arquivos brutos (.mat)
pathname = os.environ['HOME'] + '/Dropbox/siodoc/dados/brutos/'

#inicia classe
w = WaveProc(pathname)

#escolha o mes para plotagem
periodo = '2014-10'

#carrega arquivos .mat
hvmat = scipy.io.loadmat(pathname + 'heave.mat')
ptmat = scipy.io.loadmat(pathname + 'pitch.mat')
rlmat = scipy.io.loadmat(pathname + 'roll.mat')
cpmat = scipy.io.loadmat(pathname + 'compass.mat')

#  0    1    2    3     4    5  
# ano, mes, dia, hora, min, seg
data_all = hvmat.values()[1][:,[0,1,2,3,4,5]]

#data de todos os arquivos com datetime
datat_all = [datetime(int(data_all[i,0]),int(data_all[i,1]),int(data_all[i,2]),
    int(data_all[i,3])) for i in range(len(data_all))]
datat1 = np.array(datat_all) #coloca datat em array

# #cria vetor de data em str (ex: '2014-07-16 16:00:00')
# data_allstr = datat_all.astype(str) 

#matriz com dados
hv1 = hvmat.values()[1][:,6:]
pt1 = ptmat.values()[0][:,6:]
rl1 = rlmat.values()[0][:,6:]
cp1 = cpmat.values()[0][:,6:]

#create dataframe - pandas
hv = pd.DataFrame(hv1, index=datat1)[periodo]
pt = pd.DataFrame(pt1, index=datat1)[periodo]
rl = pd.DataFrame(rl1, index=datat1)[periodo]
cp = pd.DataFrame(cp1, index=datat1)[periodo]



#faz a correcao de pitch e roll em slpEW e slpNS

# valores do compass em radianos
cp_rad = cp * (np.pi/180)

#?? teste
cp_rad = np.arctan(np.sin(cp_rad) / np.cos(cp_rad))

#correcao do compass (NDBC 96, pg.14)

#pitch
pitch_EW = ( (np.sin(cp_rad) * np.sin(pt)) / np.cos(pt) ) -  ( (np.cos(cp_rad) * np.sin(rl)) / (np.cos(pt) * np.cos(rl)) )

#roll
roll_NS = ( (np.cos(cp_rad) * np.sin(pt)) / np.cos(pt) ) +  ( (np.sin(cp_rad) * np.sin(rl)) / (np.cos(pt) * np.cos(rl)) )

# pt = pitch_EW
# rl = roll_NS

#parametrospara processamento

w.h = 60 #profundidade 
w.nfft = 256 #numero de dados para a fft (para nlin=1312 -- p/ 32gl, nfft=82 ; p/8 gl, nfft=328)
w.fs = 1 #freq de amostragem
w.dt = 1.0 / w.fs
nlin = hv.shape[1] #comprimento da serie temporal a ser processada
gl = (nlin/w.nfft) * 2 #graus de liberdade
t = range(1,1025) ##vetor de tempo

#processamento em batelada
d = []
for da in hv.index[::3]:

    print da

    #atribui series temporais as variaveis x e y da classe
    w.n1 = hv.ix[da] #heave
    w.n2 = pt.ix[da] #pitch
    w.n3 = rl.ix[da] #roll
    w.date = da #date

    w.timedomain()

    w.freqdomain()

    d.append({'date'   : w.date,
    		  'hs'     : w.hs,
    		  'h10'    : w.h10,
    		  'hmax'   : w.hmax,
    		  'tmed'   : w.tmed,
    		  'thmax'  : w.thmax,
    		  'hm0'    : w.hm0,
    		  'tp'     : w.tp,
    		  'dp'     : w.dp,
              'tzamax' : w.tzamax
    		})

    #espectro

    pl.figure()
    pl.plot(w.sn1[:,0], w.sn1[:,1],'-') #total
    pl.plot(w.sn1[:18,0], w.sn1[:18,1],'-') #fx1
    pl.plot(w.sn1[18:35,0], w.sn1[18:35,1],'-') #fx2
    pl.plot(w.sn1[35:70,0], w.sn1[35:70,1],'-') #fx3
    pl.plot(w.sn1[70:,0], w.sn1[70:,1],'-') #fx4
    pl.twinx()
    pl.plot(w.sn1[:,0], w.dire1,'.') #total
    pl.grid()
    pl.title(str(da))
    pl.xlabel('Freq. (Hz)')
    pl.ylabel('Energ. (m2/Hz)')
    pl.savefig(os.environ['HOME'] + '/Dropbox/siodoc/rot/fig/spec/' + str(da) + '.png')
    pl.close('all')

df = pd.DataFrame(d)
df = df.set_index('date')

df.to_csv(os.environ['HOME'] + '/Dropbox/siodoc/rot/out/SIDOC_201410.csv')
