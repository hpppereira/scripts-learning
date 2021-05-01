'''
Processamento dos dados da boia de ilha rasa
retirado do modem

* a Hanna que nos mandou

comparacao com o .wave.dat que tem os parametros de ondas
calculados pela boia

- os dados da VAISALA estao todos com nan, a nao ser o yaw

'''


import numpy as np
import pylab as pl
from datetime import datetime
import os
# import espec
# import loadhne
import proconda
# from scipy.signal import butter, lfilter

pl.close('all')

#caminho dos dados do gx3
pathname_gx3 = os.environ['HOME'] + '/Dropbox/ambid/dados/IlhaRasa_gx3modem/'

#tem que fazer a leitura
param1 = np.genfromtxt(pathname_gx3 + 'CR1000_SEGEN_wave.dat',
	dtype=str,delimiter=',',skiprows=4)
# ax1 = np.genfromtxt(pathname_gx3 + 'TOA5_61689.microstrain_stbacelX.dat',
# 	dtype=str,delimiter=',',skiprows=4)
# ay1 = np.genfromtxt(pathname_gx3 + 'TOA5_61689.microstrain_stbacelY.dat',
# 	dtype=str,delimiter=',',skiprows=4)
# az1 = np.genfromtxt(pathname_gx3 + 'TOA5_61689.microstrain_stbacelZ.dat',
# 	dtype=str,delimiter=',',skiprows=4)
# pt1 = np.genfromtxt(pathname_gx3 + 'TOA5_61689.microstrain_pitch.dat',
# 	dtype=str,delimiter=',',skiprows=4)
# rl1 = np.genfromtxt(pathname_gx3 + 'TOA5_61689.microstrain_roll.dat',
# 	dtype=str,delimiter=',',skiprows=4)
aew1 = np.genfromtxt(pathname_gx3 + 'CR1000_SEGEN_microstrain_stbaclEW.dat',
	dtype=str,delimiter=',',skiprows=4)
ans1 = np.genfromtxt(pathname_gx3 + 'CR1000_SEGEN_microstrain_stbaclNS.dat',
	dtype=str,delimiter=',',skiprows=4)
av1 = np.genfromtxt(pathname_gx3 + 'CR1000_SEGEN_microstrain_stbaclV.dat',
	dtype=str,delimiter=',',skiprows=4)
# yaw1 = np.genfromtxt(pathname_gx3 + 'TOA5_61689.microstrain_yaw.dat',
# 	dtype=str,delimiter=',',skiprows=4)
# vai1 = np.genfromtxt(pathname_gx3 + 'TOA5_61689.VAISALA.dat',
# 	dtype=str,delimiter=',',skiprows=4)

#coloca nan que  o python entende
param1[np.where(param1=='"NAN"')] = np.nan
# ax1[np.where(ax1=='"NAN"')] = np.nan
# ay1[np.where(ay1=='"NAN"')] = np.nan
# az1[np.where(az1=='"NAN"')] = np.nan
# pt1[np.where(pt1=='"NAN"')] = np.nan
# rl1[np.where(rl1=='"NAN"')] = np.nan
aew1[np.where(aew1=='"NAN"')] = np.nan
ans1[np.where(ans1=='"NAN"')] = np.nan
av1[np.where(av1=='"NAN"')] = np.nan
# yaw1[np.where(yaw1=='"NAN"')] = np.nan
# vai1[np.where(vai1=='"NAN"')] = np.nan


#pega apenas os dados (sem data)
param = param1[:,range(2,param1.shape[1])].astype(float)
# ax = ax1[:,range(2,ax1.shape[1])].astype(float).T
# ay = ay1[:,range(2,ay1.shape[1])].astype(float).T
# az = az1[:,range(2,az1.shape[1])].astype(float).T
# pt = pt1[:,range(2,pt1.shape[1])].astype(float).T
# rl = rl1[:,range(2,rl1.shape[1])].astype(float).T
aew = aew1[:,range(2,aew1.shape[1])].astype(float).T
ans = ans1[:,range(2,ans1.shape[1])].astype(float).T
av = av1[:,range(2,av1.shape[1])].astype(float).T
# yaw = yaw1[:,range(2,yaw1.shape[1])].astype(float).T
# vai = vai1[:,range(2,vai1.shape[1])].astype(float).T

#cria data com datetime
data = [datetime.strptime(param1[i,0], '"%Y-%m-%d %H:%M:%S"') for i in range(len(param))]


### processamento em batelada ###

t = range(1,1025) #vetor de tempo
h = 40 #profundidade
nfft = 256
fs = 1 #freq amost

matonda = []
matonda_hv = []

for i in range(len(av)):

	print i

	#serie da maior onda
	# ss = 45

	eta = av[:,i]
	etax = aew[:,i]
	etay = ans[:,i]
	#calcula parametros de onda

	#onda no tempo
	# hs,h10,hmax,tmed,thmax = proconda.ondat(t,eta,h)

	#processamento no dominio da frequencia
	hm0, tp, dp, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
	    eta,etax,etay,h,nfft,fs)

	#processamento no dominio da frequencia particionado (sea e swell)
	# hm01, tp1, dp1, hm02, tp2, dp2 = proconda.ondap(hm0,tp,dp,sn,dire1,df)

	#divide o espectro de heave por w4
	w4 = (2 * np.pi * freq) ** 4

	#espectro de heave
	sn_hv = sn[:,1] / w4

	#acha o indice da frequencia de pico -- corrigido tirando o ruido em baixa
	cc = 10 #freq minima
	ind = np.where(sn_hv[cc:] == np.max(sn_hv[cc:]))[0]

	dire1_hv = dire2[cc:]

	#periodo de pico
	tp_hv = (1. / freq[cc:][ind])[0]
	dp_hv = dire1_hv[ind]

	#momento espectral de ordem zero total - m0
	m0 = np.sum(sn_hv[cc:]) * df

	#calculo da altura significativa
	hm0_hv = 4.01 * np.sqrt(m0)

	matonda.append([hm0,tp,dp])
	matonda_hv.append([hm0_hv,tp_hv,dp_hv])

matonda = np.array(matonda)
matonda_hv = np.array(matonda_hv)

#data de heave
data_hv = data[:len(matonda_hv)]

#declinacao magnetica
param[:,2] = param[:,2] - 22


#altura
pl.figure()
pl.subplot(311)
pl.title('Hs')
# pl.plot(data_hv,matonda[:,0],'b',label='lioc')
pl.plot(data_hv,matonda_hv[:,0],'r',label='lioc1')
pl.plot(data,param[:,3],'g',label='ambid')
pl.legend()
pl.ylim([0,5])

pl.subplot(312)
pl.title('Tp')
# pl.plot(data_hv,matonda[:,1],'b',label='lioc')
pl.plot(data_hv,matonda_hv[:,1],'r',label='lioc1')
pl.plot(data,param[:,1],'-g',label='ambid')

pl.subplot(313)
pl.title('Dp')
# pl.plot(data_hv,matonda[:,2],'b.',label='lioc')
pl.plot(data_hv,matonda_hv[:,2],'r.',label='lioc1')
pl.plot(data,param[:,2],'g.',label='ambid')


pl.show()

# pl.figure()
# pl.subplot(1,2,1)
# pl.plot(freq,sn[:,1],'-o')
# pl.subplot(1,2,2)
# pl.plot(freq,sn_hv,'-o')

# #calculo do parametro gamma - LIOc
# # gam = jonswap.gamma(tp)
# # gam1 = jonswap.gamma(tp1)
# # gam2 = jonswap.gamma(tp2)

# # #espectro de jonswap
# # s_js = jonswap.spec(hm0,tp,freq,gam)
# # s_js2 = jonswap.spec(hm02,tp2,freq,gam2)



# #figugras
# pl.figure() #series de hs, tp e dp
# pl.subplot(311)
# pl.plot(data,param[:,3])
# pl.axis([data[0],data[500],0,4])
# pl.subplot(312)
# pl.plot(data,param[:,0],'bo')
# pl.plot(data,param[:,1],'ro')
# pl.axis([data[0],data[500],0,15])
# pl.subplot(313)
# pl.plot(data,param[:,2],'o')
# pl.axis([data[0],data[500],0,360])




# pl.show()