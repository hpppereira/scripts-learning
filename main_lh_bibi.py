# -*- coding: utf-8 -*-
"""
Processamento das ondas BiBi coletadas 
em tanque de ondas

						Wave A	Wave B
Height	H (m)			0.10	0.16
Period	T (s)			1.60	2.10
Direction	D (°)		10.00	0.00
Depth	h (m)			0.60	0.60
Measured depth	d (m)	0.35	0.35

"""

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# importa bibliotecas

import os
import pandas as pd
import matplotlib.pyplot as plt
import waveproc
reload(waveproc)
from waveproc import WaveProc
from scipy import signal
import numpy as np

plt.close('all')


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# Dados de Entrada

# plota figura
make_plot = 1

# caminho do arquivo de dados
pathname = os.environ['HOME'] + '/Dropbox/daat/bibi/data/'
filename = 'BiBi_Waves_Data.xlsx'

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# Leitura dos dados


meas = pd.read_excel(pathname + filename, sheetname='Measured', header=0, 
				   skiprows=None, skip_footer=0, index_col=None,
				   names=['time','u','v','w'])


mod = pd.read_excel(pathname + filename, sheetname='Model', header=0, 
				   skiprows=None, skip_footer=0, index_col=None,
				   names=['time','u','v','w'])

meas = meas.set_index('time')
mod = mod.set_index('time')

# meas = meas.iloc[1200:13600,:]
# meas = meas.iloc[:15000,:]
# meas = meas.iloc[1000:2000,:]
# mod = mod[100:15000]

# stop
# divide os dados 
# uu = meas.u.values.reshape((248,len(meas)/248)).T
# vv = meas.v.values.reshape((248,len(meas)/248)).T
# ww = meas.w.values.reshape((248,len(meas)/248)).T
uu = meas.u.values
vv = meas.v.values
ww = meas.w.values

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# Dados de Entrada do Processamento

# dd = u

nfft = len(uu) / 2 
dt = meas.index[1]-meas.index[0] # intervalo de amostragem
fs = 1/dt
depth = 0.6

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# 1- Processamento com Longuet-Higgins

w = WaveProc(n1=uu, n2=vv, n3=ww,
			 fs=fs, nfft=nfft, h=depth)

# w = WaveProc(n1=u, n2=meas.v.values, n3=meas.w.values,
# 			 fs=fs, nfft=nfft, h=depth)

w.timedomain()
w.freqdomain()

w.s1 = w.aa1[:,1] # espectro 1d de veloc. verical

# amplifica sinal da infragravidade
# w.s1[:30] = w.s1[:30] * 100

# acha picos no espectro
peakind = signal.find_peaks_cwt(w.s1, np.arange(1,10))

# correcao da selecao de picos
# peakind[[1,2,3,5]] = peakind[[1,2,3,5]] - 1

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# Figuras

if make_plot == 1:

	plt.figure()
	ax1 = plt.subplot(211)
	plt.plot(w.f, w.s1,'-')
	plt.plot(w.f[peakind], w.s1[peakind],'ro')
	plt.plot(w.f[peakind[:2]], w.s1[peakind[:2]],'go')
	plt.xlim(0,2)
	plt.grid()
	plt.subplot(212, sharex=ax1)
	plt.plot(w.f, w.dire1)
	plt.plot(w.f[peakind], w.dire1[peakind],'ro')
	plt.xlim(0,2)
	plt.grid()

	plt.figure()
	plt.plot(w.f, w.sn1[:,1], w.f, w.sn2[:,1], w.f, w.sn3[:,1])
	plt.legend(['u','v','w'])
	plt.xlim(0,2)

plt.show()











