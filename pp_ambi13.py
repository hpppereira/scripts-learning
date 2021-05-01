''' Processamento dos dados de onda do sensor 
	gx3 e Axys em Mexilhao
	Projeto: GX3 - Ambidados

	- Verificar a escala do espectro de heave da axys
	e do gx3 integrado e dividido por w4
	- Comparar o espectro de heave da axys do arquivo
	NONDIRSPEC e HNE.
'''

import numpy as np
from matplotlib import pylab as pl
from datetime import datetime
import os
import espec
import loadhne
import proconda

pl.close('all')

#carrega dados HNE
axh = np.loadtxt(os.environ['HOME'] + '/Dropbox/lioc/ambid/dados/Mexilhao-axys_gx3_2014/axys/HNE/201406070700.HNE',
	skiprows=11)

#carrega dados NONDIRSPEC (O Parente tirou o cabecalho - nao precisa pular linhas)
axs = np.loadtxt(os.environ['HOME'] + '/Dropbox/lioc/ambid/dados/Mexilhao-axys_gx3_2014/axys/NONDIRSPEC/201406070700.NONDIRSPEC')
axs = axs[1:,:]


#cria variavel 'lista' com nome dos arquivos HNE
lista = np.array(loadhne.lista_hne(os.environ['HOME'] + '/Dropbox/lioc/ambid/dados/Mexilhao-axys_gx3_2014/axys/HNE/'))

#escolhe a data inicial e final para ser processada (opcional, no 'p0' e 'p1')
z0 = '201406111500.HNE'
z1 = z0

#numero dos arq para processar (modificar p0=0 e p1=len(lista) para todos)
p0 = np.where(lista == z0)[0][0]
p1 = np.where(lista == z1)[0][0]

#define variaveis da axys
eta,etax,etay = axh[:,[1,2,3]].T


fs = 1.28
nfft = 172 # 345-8gl ; 86-32gl ; 172-16gl
dt = 1./fs
h = 1500 #profundidade

#processamento dos dados no dominio da frequencia
hm0, tp, dp, sigma1p, sigma2p, f, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
eta,etax,etay,h,nfft,fs)

#figuras

pl.figure()
pl.plot(f,sn[:,1],axs[:,0],axs[:,1],'r')
pl.legend(['hne','nondirspec'])
pl.title('201406070700')

pl.show()