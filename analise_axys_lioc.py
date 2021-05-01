# Processamento dos dados da axys pelo calibrador de ondas do lioc
# Henrique e Fabio
# 18/09/2020

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import mlab
plt.close('all')

pathname = '/home/hp/Documents/lioc_axys/'
filename = 'ENSAIO-02-S1200P12T1200D45-200917_1850-MNH.TXT'
# filename = 'ENSAIO-03-S1200P12T1200D-45-200918_1015-MNH.TXT'
# filename = 'ENSAIO-04-S1200P12T1200D00-200918_1100-MNH.TXT'
# filename = 'ENSAIO-05-S1200P12T1200D90-200918_1150-MNH.TXT'
# filename = 'ENSAIO-06-GIRO_S640P10T300D00-200918_1310-MNH.TXT'

df = pd.read_csv(pathname + filename, skiprows=9, header=None)

df = df.iloc[:,:-3]

# intervalo de amostragem (segundos)
dt = 0.7813571

# series temporais de heave, norte e leste
h = df.iloc[0,0::3].values
n = df.iloc[0,1::3].values
e = df.iloc[0,2::3].values

# vetor de tempo (segundos)
t = np.arange(0, len(h) * dt, dt)[:-1]

# freq de amostragem
fs = 1.0 / dt

# tamanho do segmento para a fft
nfft = int(len(h)/4)

# calculo do espectro
sh, f = mlab.psd(h, NFFT=nfft, Fs=fs, detrend=mlab.detrend_mean,
                window=mlab.window_hanning, noverlap=nfft/2)

sn, f = mlab.psd(n, NFFT=nfft, Fs=fs, detrend=mlab.detrend_mean,
                window=mlab.window_hanning, noverlap=nfft/2)

se, f = mlab.psd(e, NFFT=nfft, Fs=fs, detrend=mlab.detrend_mean,
                window=mlab.window_hanning, noverlap=nfft/2)

# plotagem da serie temporal
plt.figure()
plt.plot(t, h, t, n, t, e)
plt.title(filename)
plt.legend(['heave', 'norte', 'leste'])
plt.xlabel('Tempo (segundos)')
plt.ylabel('metros')
plt.xlim(0, 100)

# plotagem do espectro
plt.figure()
plt.title(filename)
plt.plot(f, sh, f, sn, f, se)
plt.legend(['heave', 'norte', 'leste'])
plt.xlabel('Frequência (Hz)')
plt.ylabel('m²/Hz')
plt.grid()

plt.show()
