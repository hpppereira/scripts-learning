'''
Faz grafico de spectrograma
com Short Fourier Transform
'''

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

plt.close('all')

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/bruto/triaxys/pre_proc/rio_grande/hne/'

s1 = pd.read_table(pathname + '/200907241900.HNE',skiprows=11,sep='\s*',names=['time','n1','n2','n3'])
s2 = pd.read_table(pathname + '/201203281400.HNE',skiprows=11,sep='\s*',names=['time','n1','n2','n3'])
s2 = s2[:len(s1)]

dt = 0.78
t = np.arange(0,len(s1)*dt,dt)

nfft = 50       # the length of the windowing segments
Fs = 1 / dt  # the sampling frequency


spectrum1, freqs1, t1 = mlab.specgram(s1.n1, NFFT=nfft, Fs=Fs,detrend=mlab.detrend_none,
        window=mlab.window_hanning, noverlap=nfft/2)

spectrum2, freqs2, t2 = mlab.specgram(s2.n1, NFFT=nfft, Fs=Fs,detrend=mlab.detrend_none,
        window=mlab.window_hanning, noverlap=nfft/2)

#spectrograma
plt.figure(figsize=(11,7))

plt.subplot(221)
plt.plot(t,s1.n1,'k')
plt.title(r'$2009/07/24\ -\ 19h$',fontsize=15)
plt.xlim(400,700)
plt.ylim(-7,7)
plt.ylabel(r'$Heave\ (m)$',fontsize=15)
plt.grid()
plt.subplot(223)
plt.contour(t1,freqs1,spectrum1,shading='flat',colors='k',levels=np.arange(spectrum1.min(),spectrum1.max(),12))
plt.ylim(0,0.3)
plt.xlim(400,700)
plt.grid()
plt.ylabel(r'$Frequency\ (Hz)$',fontsize=15)
plt.xlabel(r'$Time\ (s)$',fontsize=15)

plt.subplot(222)
plt.plot(t,s2.n1,'k')
plt.title(r'$2012/03/28\ -\ 14h$',fontsize=15)
plt.xlim(700,1000)
plt.ylim(-7,7)
plt.grid()
plt.subplot(224)
plt.contour(t2,freqs2,spectrum2,shading='flat',colors='k',levels=np.arange(spectrum2.min(),spectrum2.max(),12))
plt.ylim(0,0.3)
plt.xlim(700,1000)
plt.grid()
plt.xlabel(r'$Time\ (s)$',fontsize=15)


plt.show()

'''
# Pxx is the segments x freqs array of instantaneous power, freqs is
# the frequency vector, bins are the centers of the time bins in which
# the power is computed, and im is the matplotlib.image.AxesImage
# instance

plt.figure(figsize=(12,8))
ax1 = plt.subplot(221)
plt.plot(t, s1.n1)
plt.ylim(-8,8)
plt.ylabel(r'$Elevation\ (m)$',fontsize=15)
plt.grid()
plt.subplot(223, sharex=ax1)
Pxx, freqs, bins, im = plt.specgram(s1.n1, NFFT=NFFT, Fs=Fs, noverlap=NFFT/2,
                                cmap=plt.cm.jet)
plt.colorbar(orientation='horizontal',extend='both',fraction=0.1, pad=0.2)
plt.xlabel(r'$Time\ (s)$',fontsize=15)
plt.ylabel(r'$Frequency\ (Hz)$',fontsize=15)
plt.ylim(0,0.6)
plt.xlim(500,700)
plt.show()

ax2 = plt.subplot(222)
plt.plot(t, s2.n1)
plt.ylim(-8,8)
#plt.ylabel(r'$Elevation\ (m)$',fontsize=15)
plt.grid()
plt.subplot(224, sharex=ax2)
Pxx, freqs, bins, im = plt.specgram(s2.n1, NFFT=NFFT, Fs=Fs, noverlap=NFFT/2,
                                cmap=plt.cm.jet)
plt.colorbar(orientation='horizontal',extend='both',fraction=0.1, pad=0.2,ticks=[-90, 0, 10])
plt.xlabel(r'$Time\ (s)$',fontsize=15)
#plt.ylabel(r'$Frequency\ (Hz)$',fontsize=15)
plt.ylim(0,0.6)
plt.xlim(800,1000)
plt.show()
'''
