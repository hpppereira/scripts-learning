# -*- coding: utf-8 -*-
"""
Created on Mon Jan 05 15:40:05 2015

@author: Tamiris e nois!!
"""

import numpy as np
import pylab as pl
from datetime import datetime
import proconda

#caminho windows
# wad = np.loadtxt('C:\Users\Cliente\Documents\LIOC\ST004\Dados_Brutos\Ondas_Direcionais/PTU04_05000.wad')
# whd = np.loadtxt('C:\Users\Cliente\Documents\LIOC\ST004\Dados_Brutos\PTU04_05.whd')

#caminho linux
wad = np.loadtxt('C:\Users\Cliente\Documents\LIOC\ST004\Dados_Brutos\Ondas_Direcionais/PTU04_05000.wad')
whd = np.loadtxt('C:\Users\Cliente\Documents\LIOC\ST004\Dados_Brutos\PTU04_05.whd')

#carrega datas do arquivo whd
month = whd[:,0]
day = whd[:,1]
year = whd[:,2]
hour = whd[:,3]

nfft = 64 #para 32 gl, nfft=64 (16 segmentos calculados com 2 amostras , 'a' e 'b')
fs = 1 #freq. de amostragem (verificar como automatizar, uma vez que as tx. de amst nao
#sao as mesmas)

#cria vetor de data com a funcao datetime
datas = [datetime(int(year[i]),int(month[i]),int(day[i]),int(hour[i])) for i in range(len(whd))]

pr = wad[:,2] #pressao
eta = wad[:,4] #ast ?
etay = wad[:,7] #vx #verificar qual eh o etax e etay
etax = wad[:,8] #vy

#profundidade media (retirado da serie de pressao)
h = np.mean(pr)

#cria vetor de tempo (verificar tx de amostragem)
t = range(1,1025)

#processamento no dominio do tempo
hs,h10,hmax,tmed,thmax = proconda.ondat(t,eta,h)


#processamento no dominio da frequencia
hm0, tp, dp, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
eta,etax,etay,h,nfft,fs)
