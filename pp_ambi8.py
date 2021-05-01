#processamentos dos dados da mintriaxys e gx3
#
#Utilizacao de filtros nas series de aceleracoes
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

#Filtros

# ================================================================= #
# Passa-alta

#frequencia de corte
# lowcut = 0.08

#serie de aceleracao filtrada
# aczf_gx3 = butter_highpass_filter(acz_gx3, lowcut, order=6)

# ================================================================= #
# Obter a serie de heave pela integracao utilizando o metodo dos trapezios

# vz_gx3 = scipy.integrate.cumtrapz(t_gx3,aczf_gx3)

# # ================================================================= #
# # calcula os espectros a partir das series de heave

# #coloca zeros nos 2 ultimos indices (que ficou sem devido a intgracao)
# eta_gx3 = np.concatenate((eta_gx3,([0,0])))

# #calcula os espectros de heave da axys e gx3
# aa_eta_ax = espec.espec1(eta_ax[0:1024],nfft,fs_ax)
# aa_eta_gx3 = espec.espec1(eta_gx3,nfft,fs_gx3)


# ================================================================= #
# figuras

#compara aceleracoes brutas e filtradas
# pl.figure()
# pl.plot(acz_gx3 - np.mean(acz_gx3))
# pl.plot(aczf_gx3)

# pl.figure()
# pl.plot(vz_gx3)

# pl.show()

# pl.figure()
# pl.title('Series temporais de heave (axis e gx3 (integrada))')
# pl.subplot(211)
# pl.plot(eta_ax), pl.axis('tight'), pl.title('elevacao - axys')
# pl.subplot(212)
# pl.plot(eta_gx3), pl.axis('tight'), pl.title('elevacao - gx3')

# #plotagem do auto-espectro
# pl.figure()
# pl.plot(aa_eta_ax[:,0],aa_eta_ax[:,1])
# pl.plot(aa_eta_gx3[:,0],aa_eta_gx3[:,1])
# pl.plot(aa_eta_gx3[:,0],aa_eta1_gx3)
# pl.legend(['heave_ax','heave_gx3 (int(acz))','heave_gx3(acz/w4)'])
# pl.axis([0,0.5,0,0.2])

# pl.show()