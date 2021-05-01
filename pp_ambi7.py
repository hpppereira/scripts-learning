#processamentos dos dados da mintriaxys e gx3
#
#Obter a serie temporal e espectro de heave do gx3 atraves da integracao
#utilizando o meteodo dos trapezios
#
# Ref: http://www.mathworks.com/matlabcentral/newsreader/view_thread/305134
#
# Funcao: scipy.integrate.cumtrapz(t_gx3,acz_gx3)

import numpy as np
import pylab as pl
import os
import scipy.io
from scipy.signal import butter, lfilter
import espec

pl.close('all')

#Define funcoes

def butter_highpass_filter(data, lowcut, order=6):
    b, a = butter(order, lowcut, btype='high')
    y = lfilter(b, a, data)
    return y

# =============================================================================== #
# Definicao das variaveis

pathname = os.environ['HOME'] + '/Dropbox/ambid/TEBIG-axys_gx3_20140522/'
# pathname = 'C:/Users/henrique/Dropbox/ambid/TEBIG-axys_gx3_20140522/'

#variaveis da axys e gx3
mat = scipy.io.loadmat(pathname + 'bmo.mat')

#aceleracao z do gx3 (brutos)
mat1 = np.loadtxt(pathname + 'CR1000_microstrain_stbacelZ_2014_05_22_15_17_00.dat',
    delimiter=',',skiprows=4,dtype=str)

#profundidade
h = 22

#hora para comparar (0 - 6)
hr = 0

#AXYS
#vetor de tempo
t_ax = mat.values()[0][0,:]
t_ax = t_ax - t_ax[0]
eta_ax = mat.values()[7]

#GX3
#a acZ da gx3 tem mais datas, ate a hora 18, vamos pegar os registros simultaneos
acz_gx3 = mat1[0:9,2:].astype(np.float) 
t_gx3 = np.arange(0,acz_gx3.shape[1])

#seleciona primeiro arquivo simultaneo
eta_ax = eta_ax[hr,:]
acz_gx3 = acz_gx3[hr+3,:] * -9.81 #para ficar em m/s2

#parametros para a fft
nfft = 64
fs_ax = 1.28 #axys
fs_gx3 = 1 #gx3

# =============================================================================== #
# 1 - Deriva 2 vezes a serie de heave da axys para obter a aceleracao

v_ax = np.diff(eta_ax)
az_ax = np.diff(v_ax)
# az_ax = az_ax * -1 #para ficar mais parecido com a serie da gx3

# =============================================================================== #
#calcula os espectros

aa_ax = espec.espec1(az_ax,nfft,fs_ax)
aa_gx3 = espec.espec1(acz_gx3,nfft,fs_gx3)

# =============================================================================== #

#series temporais de aceleracao (axys e gx3)
pl.figure()
pl.subplot(211)
pl.plot(t_ax[:-2]-t_ax[0],az_ax-np.mean(az_ax),label='axys')
pl.legend()
pl.subplot(212)
pl.plot(t_gx3,acz_gx3-np.mean(acz_gx3),color='g',label='gx3')
pl.legend()

pl.figure()
pl.plot(aa_ax[:,0],aa_ax[:,1],label='axys')
pl.plot(aa_gx3[:,0],aa_gx3[:,1],label='gx3')
pl.legend()

pl.show()
