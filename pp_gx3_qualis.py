'''
	Processamento dos dados de ondas simuladas
	do Luiz Felipe. Serie de mar aleatorio simulada.
	O Luiz obteve a serie de heave a partir do acelerometro
	GX3 utilizando tecnicas de filtragem e integracao numerica

	- Comparar os espectros das series da qualis (padrao) com o 
	do sensor GX3
'''

import numpy as np
import pylab as pl
import scipy.io
import os
# import proconda
import espec
# import numeronda

# reload(numeronda)
reload(espec)
# reload(proconda)

pl.close('all')

# =============================================================================== #
# Definicao das variaveis

pathname = os.environ['HOME'] + '/Dropbox/ensaios_laboc/dados/'

mat = scipy.io.loadmat(pathname + 'mar_caso1.mat')

#dentro de 'mat', tem 'mar_caso1'. Dentro de 'mar_caso1' tem tres
#variaveis: 'dspZf', 'heave' e x - por isso faz: mat.values()[0][0][0][0]
# o [:,0] eh para deixar um arrray de uma dimensao
dspZf = mat.values()[0][0][0][0][:,0]
heave = mat.values()[0][0][0][1][:,0]
x = mat.values()[0][0][0][2][:,0]

# 32 gl
nfft_dspZf = 5606
nfft_heave = 67
nfft_x = 5606

fs_dspZf = 100
fs_heave = 1.28 ##verificar com luiz
fs_x = 100

#calculo dos espectros

aa_dspZf = espec.espec1(dspZf,nfft_dspZf,fs_dspZf)
aa_heave = espec.espec1(heave,nfft_heave,fs_heave)
aa_x = espec.espec1(x,nfft_x,fs_x)


#figuras

pl.plot(aa_dspZf[0:20,0],aa_dspZf[0:20,1],label='dspZf')
pl.plot(aa_heave[:,0],aa_heave[:,1],label='heave')
pl.plot(aa_x[0:20,0],aa_x[0:20,1],label='x')
pl.legend()

pl.show()