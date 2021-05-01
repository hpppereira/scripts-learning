'''
Calculo da serie e heave atraves
da IFFT do espectro de aceleracao
dividido por w4

Double integration of raw acceleration data is a pretty poor estimate for displacement.  The reason is that at each integration, you are compounding the noise in the data.  If you are dead set on working in the time-domain, the best results come from the following steps.
1. Remove the mean from your sample (now have zero-mean sample)
2. Integrate once to get velocity using some rule (trapezoidal, etc.)
3. Remove the mean from the velocity
4. Integrate again to get displacement.  
5. Remove the mean. Note, if you plot this, you will see drift over time.
6. To eliminate (some to most) of the drift (trend), use a least squares fit (high degree depending on data) to determine polynomial coefficients.
7. Remove the least squares polynomial function from your data.

A much better way to get displacement from acceleration data is to work in the frequency domain.  To do this, follow these steps...

1. Remove the mean from the accel. data
2. Take the Fourier transform (FFT) of the accel. data.
3. Convert the transformed accel. data to displacement data by dividing each element by -omega^2, where omega is the frequency band.
4. Now take the inverse FFT to get back to the time-domain and scale your result.  

This will give you a much better estimate of displacement.


'''


import numpy as np
from matplotlib import pylab as pl
from datetime import datetime
import os
import espec
import loadhne
import proconda
from scipy.signal import butter, lfilter


pl.close('all')

def butter_highpass_filter(data, lowcut, order=6):
    b, a = butter(order, lowcut, btype='high')
    y = lfilter(b, a, data)
    return y

#pathname

#gx3
pathname_gx3 = os.environ['HOME'] + '/Dropbox/lioc/ambid/dados/Mexilhao-axys_gx3_2014/gx3/'

dados_av_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbaclV.dat',
	dtype=str,delimiter=',',skiprows=4)

av_gx3_mat = dados_av_gx3[:,range(2,dados_av_gx3.shape[1])].astype(float).T
	
av_gx3 = av_gx3_mat[:,100] #arq-100 = "2014-06-11 04:00:00"'
av_gx3 = av_gx3 - np.mean(av_gx3)

#axys (a axys esta 3 horais a menos: gx3 = axys + 3)
axh = np.loadtxt(os.environ['HOME'] + '/Dropbox/lioc/ambid/dados/Mexilhao-axys_gx3_2014/axys/HNE/201406110400.HNE',
	skiprows=11)

hv_ax = axh[:,1]

#concatenar com zeros no inicio e fim
# aux = np.zeros(1068)
# aux[20:1044] = av_gx3
# av_gx3 = aux

data_gx3_str = dados_av_gx3[:,0] #data gx3 em string
data_arq = data_gx3_str[100]

#data (fazer listcompreh..)
#data_gx3.append(datetime.strptime(data_gx3_str[kk], '"%Y-%m-%d %H:%M:%S"'))

#parametros axys e gx3
fs_gx3 = 1
fs_axys = 1.28
nfft_gx3 = 128 #256-8gl ; 64-32gl
nfft_axys = 172
dt_gx3 = 1./fs_gx3
dt_axys = 1./fs_axys

#vetor de tempo
t_gx3 = np.arange(0,len(av_gx3),1/fs_gx3)
t_axys = np.arange(0,1382*dt_axys,dt_axys)

#vetor de frequencia#
n = av_gx3.size
timestep = dt_gx3
freq = np.fft.fftfreq(av_gx3.size, dt_gx3)
#freq = t

# filtro
# lowcut = 0.5
# y = butter_highpass_filter(av_gx3, lowcut, order=6)
# av_gx3 = y

#omega ^2
w2 = (2 * np.pi * freq) ** 2

#fft de acV
fft_av = np.fft.fft(av_gx3)

#divide por omega^2 (fft de heave)
fft_av_w2 = fft_av / (w2)

#serie temporal de acv
ifft_av = np.fft.ifft(fft_av)

#ifft - serie de heave (serie temporal reconstituida)
#*comeca do 1 pq o 0 eh nan
ifft_av_w2 = np.fft.ifft(fft_av_w2[10:1014])

hv_gx3 = np.conj(np.real(ifft_av_w2),np.imag(ifft_av_w2))

#espectro de aceleracao
aa_av_gx3 = espec.espec1(av_gx3,nfft_gx3,fs_gx3)

#calculo o espectro de heave
aa_hv_gx3 = espec.espec1(hv_gx3,nfft_gx3,0.5)
aa_hv_ax = espec.espec1(hv_ax,nfft_axys,fs_axys)

# pl.figure()
# pl.plot(fft_av)
# pl.plot(fft_av_w2,'-o')

pl.figure()
pl.plot(t_gx3,av_gx3)
pl.plot(t_axys,hv_ax)
pl.plot(range(10,1014),hv_gx3)

pl.figure()

pl.plot(aa_hv_ax[:,0],aa_hv_ax[:,1])
pl.plot(aa_hv_gx3[:,0],aa_hv_gx3[:,1]*100)

pl.show()