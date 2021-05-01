#funcao de espectro utilizando funcoes do matplotlib.mb


import numpy as np
import os
import espectro
from matplotlib import mlab
from matplotlib import pylab as pl

pl.close('all')

hne = np.loadtxt(os.environ['HOME'] + '/Google Drive/ambidados/200905172200.HNE',skiprows=16)

dt = 0.78

eta = np.array(hne[0:1024,1])
dspy = np.array(hne[0:1024,2])
dspx = np.array(hne[0:1024,3])

eta1 = np.array(hne[:,1])
dspy1 = np.array(hne[:,2])
dspx1 = np.array(hne[:,3])

#espectro calculado pelo modulo espectro
aa = espectro.espec2(eta,dspx,dt,32,1)

## =================================================== ##
# Espectro simples

# Dados de entrada para o calculo do espectro

# NFFT - Numero de pontos utilizado para o calculo da FFT
# Ps - frequencia de amostragem
# detrend - tirar a tendencia (entra com uma funcao)
# window - janela aplicada (default=hanning)
# noverlap - comprimento de overlap (0=sem overlap)

aa1 = mlab.psd(eta1,NFFT=256,Fs=1.28,detrend=mlab.detrend_mean,window=mlab.window_hanning,noverlap=128)
aa1 = np.array(aa1).T

f = aa1[:,1]
sp = aa1[:,0]

## =================================================== ##
# Espectro cruzado

#espectro cruzado (amplitude do espec cruzado?)
aa2 = mlab.csd(eta1,dspx1,NFFT=256,Fs=1.28,detrend=mlab.detrend_mean,window=mlab.window_hanning,noverlap=128)
aa2 = np.array(aa2).T

#calcula o modulo do espectro
aa2[:,0] = abs(aa2[:,0])

#espectro de coerencia
aa3 = mlab.cohere(eta1,dspx1,NFFT=256,Fs=1.28,detrend=mlab.detrend_mean,window=mlab.window_hanning,noverlap=128)
aa3 = np.array(aa3).T


## Figuras

#autoespectro
pl.figure()
pl.plot(aa[:,0],aa[:,1])
pl.plot(f,sp)
pl.legend(['hp','py'])
pl.title('espectro de elevacao')

#amplitude do espectro cruzado
pl.figure()
pl.plot(aa[:,0],aa[:,3])
pl.plot(aa2[:,1],aa2[:,0])
pl.legend(['hp','py'])
pl.title('amplitude do espec cruzado')

#espectro de coerencia
pl.figure()
pl.plot(aa[:,0],aa[:,7])
pl.plot(aa3[:,1],aa3[:,0])
pl.legend(['hp','py'])
pl.title('espec de coerencia')


pl.show()