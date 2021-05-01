#processamentos em batelada dos dados da mintriaxys e gx3
#para a ambidados 
#
# 1 - Integral da divisao no tempo de acZ para obter o heave e
# comparar o espectro obtido com o espec de acZ / w4

import numpy as np
import pylab as pl
import os
import scipy.io
import espec

pl.close('all')

# =============================================================================== #
# Definicao das variaveis

pathname = os.environ['HOME'] + '/Dropbox/ambid/TEBIG-axys_gx3_20140522/'

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
eta_ax_mat = mat.values()[7]

#gx3
#a acZ da gx3 tem mais datas, ate a hora 18, vamos pegar os registros simultaneos
acz_gx3_mat = mat1[0:9,2:].astype(np.float) * -9.81

#parametros para a fft
nfft = 64
fs_ax = 1.28 #axys
fs_gx3 = 1 #gx3

# =============================================================================== #
cont = 0
for i in range(6):

	cont = cont + 1

	j = i + 3

	#seleciona arquivos simultaneos
	eta_ax = eta_ax_mat[i,:]
	acz_gx3 = acz_gx3_mat[j,:]

	# =============================================================================== #

	#1 - retira a media
	acz_gx3 = (acz_gx3 - np.mean(acz_gx3))

	#calcula a primeira integral atraves de loop (metodos dos trapezios)
	vz_gx3 = []
	for i in range(len(acz_gx3)-1):
		vz_gx3.append( (acz_gx3[i] + acz_gx3[i+1]) /2 )
	vz_gx3 = np.array(vz_gx3 - np.mean(vz_gx3))

	#calcula a segunda integral
	eta_gx3 = []
	for i in range(len(vz_gx3)-1):
		eta_gx3.append( (vz_gx3[i] + vz_gx3[i+1]) /2 )
	eta_gx3 = np.array(eta_gx3 - np.mean(eta_gx3))

	# =============================================================================== #

	#coloca zeros nos 2 ultimos indices (que ficou sem devido a intgracao)
	eta_gx3 = np.concatenate((eta_gx3,([0,0])))

	# =============================================================================== #

	#espectros
	aa_eta_ax = espec.espec1(eta_ax[0:1024],nfft,fs_ax)
	aa_eta_gx3 = espec.espec1(eta_gx3,nfft,fs_gx3)
	aa_acz_gx3 = espec.espec1(acz_gx3,nfft,fs_gx3)

	# =============================================================================== #
	#divide o espec de acZ por w4 para obter o espec de heave

	#w4
	w4_gx3 = (2 * np.pi * aa_acz_gx3[:,0])**4

	#divide o espec de acZ por w4 para obter o espec de heave
	aa_eta1_gx3 = aa_acz_gx3[:,1] / w4_gx3

	# =============================================================================== #
	#plotagem

	#power spectrum axys e gx3
	pl.subplot(3,2,str(cont))
	pl.plot(aa_eta_ax[:,0],aa_eta_ax[:,1],label='axys')
	pl.plot(aa_eta_gx3[:,0],aa_eta_gx3[:,1],label='gx3-int')
	pl.plot(aa_eta_gx3[:,0],aa_eta1_gx3,label='gx3-w4')
	pl.axis([0,0.5,0,0.2])
	pl.legend()

	# =============================================================================== #

pl.show()

