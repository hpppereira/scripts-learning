'''
Processamento dos dados de vento do INMET

- Calcula o espectro para ver sinal de brisa

a coluna da direcao esta a velocidade e vice-versa
'''

import pandas as pd
import os
import espec
import pylab as pl

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/vento_INMET/'

dd = pd.read_csv(pathname + 'vento_inmet_20150822_20151022.csv', parse_dates={'datetime': ['data','hora']})

nfft = len(dd) / 8
dt = 1. / 24 #dt em dias
fs = 1. / dt

aav = espec.espec1(dd.vento_direcao,nfft,fs)
aad = espec.espec1(dd.vento_vel,nfft,fs)


pl.figure()
pl.plot(aav[:,0],aav[:,1],'b')
pl.legend(['vel'],loc=2)
pl.xlabel('cpd')
pl.grid()
pl.twinx()
pl.plot(aad[:,0],aad[:,1],'r')
pl.legend(['dir'],loc=1)

pl.show()