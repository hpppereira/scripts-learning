#processamentos dos dados da mintriaxys e gx3 #para a ambidados
#
# 1 - Integral da divisao no tempo de acZ para obter o heave e
# comparar o espectro obtido com o espec de acZ / w4
# - Fazer isso para apenas 1 registro
#
# Procedimentos para obter o deslocamento
# 1. Remove the mean from your sample (now have zero-mean sample)
# 2. Integrate once to get velocity using some rule (trapezoidal, etc.)
# 3. Remove the mean from the velocity
# 4. Integrate again to get displacement.  
# 5. Remove the mean. Note, if you plot this, you will see drift over time.
# 6. To eliminate (some to most) of the drift (trend), use a least squares fit (high degree depending on data) to determine polynomial coefficients.
# 7. Remove the least squares polynomial function from your data.

import numpy as np
import pylab as pl
import os
import scipy
import espec

pl.close('all')

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

#axys
#vetor de tempo
t_ax = mat.values()[0][0,:]
eta_ax = mat.values()[7]

#gx3
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

# ================================================================= #
# Obter o deslocamento pelo metodo dos trapezios ([Xi + Xi+1]/2)

#calcula a velocidade (a partir da aceleracao)
vz_gx3 = []
for i in range(len(acz_gx3)-1):
	vz_gx3.append( (acz_gx3[i] + acz_gx3[i+1]) / 2 )
vz_gx3 = np.array(vz_gx3 - np.mean(vz_gx3))

#calcula o deslocamento (a partir da serie de velocidade)
eta_gx3 = []
for i in range(len(vz_gx3)-1):
	eta_gx3.append( (vz_gx3[i] + vz_gx3[i+1]) / 2 )
eta_gx3 = np.array(eta_gx3 - np.mean(eta_gx3))

# ================================================================= #
# Obter o espectro de heave pela divisao do acz por w4

aa_acz_gx3 = espec.espec1(acz_gx3,nfft,fs_gx3)

#w4
w4_gx3 = (2 * np.pi * aa_acz_gx3[:,0]) ** 4

#divide o espec de acZ por w4 para obter o espec de heave
aa_eta1_gx3 = aa_acz_gx3[:,1] / w4_gx3

# ================================================================= #
# calcula os espectros a partir das series de heave

#coloca zeros nos 2 ultimos indices (que ficou sem devido a intgracao)
eta_gx3 = np.concatenate((eta_gx3,([0,0])))

#calcula os espectros de heave da axys e gx3
aa_eta_ax = espec.espec1(eta_ax[0:1024],nfft,fs_ax)
aa_eta_gx3 = espec.espec1(eta_gx3,nfft,fs_gx3)


# ================================================================= #
# figuras

pl.figure()
pl.title('Series temporais de heave (axis e gx3 (integrada))')
pl.subplot(211)
pl.plot(eta_ax), pl.axis('tight'), pl.title('elevacao - axys')
pl.ylabel('metros')
pl.subplot(212)
pl.plot(eta_gx3), pl.axis('tight'), pl.title('elevacao - gx3')
pl.xlabel('Tempo (s)')
pl.ylabel('metros')

#plotagem do auto-espectro
pl.figure()
pl.title('Espectros de heave')
pl.plot(aa_eta_ax[:,0],aa_eta_ax[:,1])
pl.plot(aa_eta_gx3[:,0],aa_eta_gx3[:,1])
pl.plot(aa_eta_gx3[:,0],aa_eta1_gx3)
pl.legend(['heave_ax','heave_gx3 (int(acz))','heave_gx3(acz/w4)'])
pl.axis([0,0.5,0,0.1])
pl.xlabel('Frequencia (Hz)')
pl.ylabel('m^2/Hz')

pl.show()