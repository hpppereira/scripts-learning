''' Processamento dos dados de onda do sensor 
	gx3 e Axys em Mexilhao
	Projeto: GX3 - Ambidados

	Calcula o periodo de pico para todos os periodos
	de medicao do gx3 e axys
'''

import numpy as np
from matplotlib import pylab as pl
from datetime import datetime
import os
import espec
import loadhne
import proconda


pl.close('all')

#pathname
pathname_gx3 = os.environ['HOME'] + '/Dropbox/ambid/dados/Mexilhao_gx3_triaxys/gx3/'
pathname_axys = os.environ['HOME'] + '/Dropbox/ambid/dados/Mexilhao_gx3_triaxys/axys/HNE/'

#carrega dados de aV do gx3
dados_av_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbaclV.dat',
	dtype=str,delimiter=',',skiprows=4)
dados_aew_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbaclEW.dat',
	dtype=str,delimiter=',',skiprows=4)
dados_ans_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbaclNS.dat',
	dtype=str,delimiter=',',skiprows=4)

av_gx3_mat = dados_av_gx3[:,range(2,dados_av_gx3.shape[1])].astype(float).T
aew_gx3_mat = dados_aew_gx3[:,range(2,dados_aew_gx3.shape[1])].astype(float).T
ans_gx3_mat = dados_ans_gx3[:,range(2,dados_ans_gx3.shape[1])].astype(float).T

#carrega dados de heave do gx3
eta_gx3_mat = np.loadtxt('eta_gx3_mat.txt')

#data gx3
data_gx3_str = dados_av_gx3[:,0] #data gx3 em string
# data_gx3 = [datetime.strptime(data_gx3_str[i], '"%Y-%m-%d %H:%M:%S"') for i in range(len(data_gx3_str))]

#lista dos arquivos da axys
lista_axys = loadhne.lista_hne(pathname_axys)
# lista_axys = lista_axys[0:len(data_gx3)]

#data da axys - verificar difenca entre gx3 e axys
# data_axys = [datetime.strptime(lista_axys[i][0:12], '%Y%m%d%H%M%S') for i in range(len(lista_axys))]

#parametros axys e gx3
fs_gx3 = 1
nfft_gx3 = 128 #256-8gl ; 64-32gl
dt_gx3 = 1./fs_gx3

fs_axys = 1.28
nfft_axys = 172 # 345-8gl ; 86-32gl
dt_axys = 1./fs_axys

# vetor de tempo de amostragem
t_gx3 = np.arange(0,1024*dt_gx3,dt_gx3)
t_axys = np.arange(0,1382*dt_axys,dt_axys)

h = 1500 #profundidade

#realiza o processamento em batelada
#ps: carrega os dados da axys dentro do loop

data_gx3 = []
data_axys = []
eta_axys_mat = []
paramt_gx3 = []
paramf_gx3 = []
paramp_gx3 = []
paramt_axys = []
paramf_axys = []
paramp_axys = []


for kk in range(eta_gx3_mat.shape[1]):
# for kk in range(108,109): #processa o arquivo 201406070700

	print 'LH - ' + str(kk)

	#axys -- soma 3 devido a defasagem entre as series
	dados_axys = loadhne.dados_hne(pathname_axys, lista_axys[kk+3])[0]
	eta_axys, etay_axys, etax_axys = dados_axys[:,[1,2,3]].T

	#datas (gx3 e axys)
	data_gx3.append(datetime.strptime(data_gx3_str[kk], '"%Y-%m-%d %H:%M:%S"'))
	data_axys.append(datetime.strptime(lista_axys[kk][0:12], '%Y%m%d%H%M%S'))

	#cria matriz com series de heave da axys
	eta_axys_mat.append(eta_axys)

	#dados do gx3
	eta_gx3 = eta_gx3_mat[:,kk]
	av_gx3 = av_gx3_mat[:,kk]
	aew_gx3 = aew_gx3_mat[:,kk]
	ans_gx3 = ans_gx3_mat[:,kk]

	# -- processamento gx3 -- #

	#tempo
	hs,h10,hmax,tmed,thmax = proconda.ondat(t_gx3,eta_gx3,1500)
	paramt_gx3.append([hs,h10,hmax,tmed,thmax])

	#frequencia
	hm0, tp, dp, sigma1p, sigma2p, f, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
	eta_gx3,aew_gx3,ans_gx3,h,nfft_gx3,fs_gx3)
	paramf_gx3.append([hm0, tp, dp])

	f_gx3, sn_eta_gx3 = sn[:,[0,1]].T

	#calcula o espectro da aceleracao vertical do gx3
	sn_acv_gx3 = espec.espec1(av_gx3,nfft_gx3,fs_gx3)
	sn_acv_gx3 = sn_acv_gx3[:,1]

	#espectro de heave do gx3 pela integracao
	sn_eta1_gx3 = sn_acv_gx3 / ((2*np.pi*f_gx3) ** 4)

	#particionamento
	hm01, tp1, dp1, hm02, tp2, dp2 = proconda.ondap(hm0,tp,dp,sn,dire1,df)
	paramp_gx3.append([hm01, tp1, dp1, hm02, tp2, dp2])

	# # -- processamento axys -- #

	#tempo
	hs,h10,hmax,tmed,thmax = proconda.ondat(t_axys,eta_axys,1500)
	paramt_axys.append([hs,h10,hmax,tmed,thmax])

	#frequencia
	hm0, tp, dp, sigma1p, sigma2p, f, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
	eta_axys,etax_axys,etay_axys,h,nfft_axys,fs_axys)
	paramf_axys.append([hm0, tp, dp])

	f_axys, sn_eta_axys = sn[:,[0,1]].T

	#particionamento
	hm01, tp1, dp1, hm02, tp2, dp2 = proconda.ondap(hm0,tp,dp,sn,dire1,df)
	paramp_axys.append([hm01, tp1, dp1, hm02, tp2, dp2])


paramt_gx3 = np.array(paramt_gx3)
paramf_gx3 = np.array(paramf_gx3)
paramp_gx3 = np.array(paramf_gx3)
paramt_axys = np.array(paramt_axys)
paramf_axys = np.array(paramf_axys)
paramp_axys = np.array(paramf_axys)
data_gx3 = np.array(data_gx3)
data_axys = np.array(data_axys)

# -- fim do processamento em batelada -- #
eta_axys_mat = np.array(eta_axys_mat).T


# -- figuras -- #

pl.figure()
pl.plot()
pl.title('Altura Significativa (Hm0)')
pl.plot(data_axys,paramf_axys[:,0],'ob',label='axys'), pl.ylabel('AXYS'), pl.legend(loc=2)
pl.twinx()
pl.plot(data_gx3,paramf_gx3[:,0],'or',label='gx3'), pl.ylabel('GX3')
pl.legend(loc=1)

pl.figure()
pl.plot()
pl.title('Periodo de Pico (Tp)')
pl.plot(data_axys,paramf_axys[:,1],'ob',label='axys')
pl.plot(data_gx3,paramf_gx3[:,1],'or',label='gx3')
pl.legend()

pl.figure()
pl.plot()
pl.title('Direcao de Pico (Dp)')
pl.plot(data_axys,paramf_axys[:,2],'ob',label='axys')
pl.plot(data_gx3,paramf_gx3[:,2],'or',label='gx3')
pl.legend()

pl.figure()
b = range(7,64)
pl.plot(f_axys[b],sn_eta_axys[b],label='axys')
pl.plot(f_gx3[b],sn_acv_gx3[b],label='gx3-acV')
pl.plot(f_gx3[b],sn_eta_gx3[b]*800,label='gx3-eta_int * 800')
pl.plot(f_gx3[b],sn_eta1_gx3[b]*6,label='gx3-eta_w4')
pl.legend(), pl.grid('on')

pl.show()