'''
Processamento dos dados brutos do ADCP de Cacimbas-ES
Projeto: WW3ES
LIOc-COPPE/UFRJ

Ultima modificacao: 23/02/2015
'''

import numpy as np
import pylab as pl
from datetime import datetime
import os
import proconda
import consiste_bruto
import consiste_proc
import jonswap

# reload(carrega_axys)
reload(proconda)
reload(consiste_bruto)
reload(consiste_proc)
reload(jonswap)

#diretorio de onde estao os dados
pathname = '/home/lioc/Dropbox/lioc/dados/ww3es/CACIMBAS/ADCP/series/preproc/'

#lista os diretorios dentro de pathname
dires = np.sort(os.listdir(pathname))

#cria vetor de tempo
t = np.arange(0,2048.5,0.5)

h = 20 #profunidade
nfft = 512 
fs = 2 #freq de amostragem
nlin = 2048
gl = (nlin/nfft) * 2

# def concatena():

eta = []
etax = []
etay = []
data = []
# data2 = []

# loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for d in range(len(dires)):

	# d = 10
	dto = dires[d]

	#lista os arquivos dentro de cada diretorio de ano e mes (STrk, Vel, ...)
	arquivos = np.sort(os.listdir(pathname + dto + '/WAVES/'))

	#loop de cada arquivo
	for arq in range(len(arquivos)):

		if arquivos[arq].startswith('STrk'):	

			#verifica o tamanho do arquivo (se for menor que 10 pula)
			if os.stat(pathname + dto + '/WAVES/' + arquivos[arq]).st_size > 10:

				print arquivos[arq]

				eta1 = np.loadtxt(pathname + dto + '/WAVES/' + arquivos[arq],skiprows=4,usecols=([0]))

				eta1 = eta1 / 1000 #passa de mm para metros

				data.append(arquivos[arq][-20:-4])

				#retira a data do nome do arquivo
				eta.append(eta1 - np.mean(eta1))

		elif arquivos[arq].startswith('Vel'):

			if os.stat(pathname + dto + '/WAVES/' + arquivos[arq]).st_size > 100000:

				print arquivos[arq]

				etax.append( np.loadtxt(pathname + dto + '/WAVES/' + arquivos[arq],skiprows=6,usecols=([0]),unpack=True) )
				etay.append( np.loadtxt(pathname + dto + '/WAVES/' + arquivos[arq],skiprows=6,usecols=([1]),unpack=True) )

				# data2.append(arquivos[arq][-20:-4])

	# return eta, etax, etay, data

#concatena os arquivos (desabilitar quando ja estiver carregado)
# eta, etax, etay, data = concatena()

matondab = []
for i in range(len(eta)):

	#loop para processar cada arquivo
	hs,h10,hmax,tmed,thmax = proconda.ondat(t,eta[i],h)

	#processamento no dominio da frequencia
	hm0, tp, dp, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
	    eta[i],etax[i],etay[i],h,nfft,fs)

	#processamento no dominio da frequencia particionado (sea e swell)
	hm01, tp1, dp1, hm02, tp2, dp2 = proconda.ondap(hm0,tp,dp,sn,dire1,df)

	gam = jonswap.gamma(tp)
	gam1 = jonswap.gamma(tp1)
	gam2 = jonswap.gamma(tp2)

	matondab.append([hs,h10,hmax,tmed,thmax,hm0,tp,dp,sigma1p,sigma2p,hm01,tp1,dp1,hm02,tp2,dp2,gam,gam1,gam2])

#  0  1   2    3    4     5    6   7     8       9      10    11   12   13    14   15
# hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2
dd = np.array(matondab)

datat = [datetime(int(data[i][0:4]),int(data[i][4:6]),int(data[i][6:8]),int(data[i][8:10])) for i in range(len(data))]
