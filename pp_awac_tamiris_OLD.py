# -*- coding: utf-8 -*-
"""
Created on Mon Jan 05 15:40:05 2015

@author: Tamiris e nois!!

Observacoes:
- O Resgate_1 nao tem dados

"""

import numpy as np
import pylab as pl
import os
from datetime import datetime
import proconda

def lista_wad(pathname):

    ''' Lista arquivos com extensao .wad 
    que estao dentro do diretorio 'pathname' 

    Entrada: pathname - diretorio que estao os arquivos
    Saida: arq - variavel com o nome dos arquivos

    '''

    lista = []
    # Lista arquivos do diretorio atual
    for f in os.listdir(pathname):
        if f.endswith('.wad'):
            lista.append(f)
    lista=np.sort(lista)

    return lista


#pathname
pathname = '/media/lioc/Lioc1/dados/ww3vale/ADCP_Vale_1_2/'

data = []

#loop para cada resgate
for i in range(2,3): # (2,14):

	pathname1 = pathname + 'Resgate_' + str(i) + '/'

	print pathname1

	#loop para os 4 ADCPs (ST00x) - x = 1:4
	for j in range(1,2):

		pathname2 = pathname1 + 'ST00' + str(j) + '/Dados_Brutos/'

		#condicoes de para arquivos faltando
		if i == 1 and j == 1: #resgate-1, adcp-1
			pass
		else:

			print pathname2

			#carrega arquivo .whd
			whd = np.loadtxt(pathname2 + 'PTU0' + str(j) + '_0' + str(i) + '.whd')

			#carrega datas do arquivo whd
			month = whd[:,0]
			day = whd[:,1]
			year = whd[:,2]
			hour = whd[:,3]

			data.append( [datetime(int(year[k]),int(month[k]),int(day[k]),int(hour[k])) for k in range(len(whd))] )

			#cria variavel 'lista' com nome dos arquivos .wad
			lista = np.array(lista_wad(pathname2 + 'Ondas_Direcionais/'))

			#varia os arquivos de cada ADCP para cada resgate
			for l in range(6,7): #len(lista_wad)):

				#condicao para arquivos inconsistentes (modifcar para as rotinas de consistencia)
				# if l == 0:
				# 	pass
				# else:

				wad = np.loadtxt(pathname2 + '/Ondas_Direcionais/' + lista[l])

				pr = wad[:,2] #pressao
				eta = wad[:,4] #ast ?
				etax = wad[:,7] #vx #verificar qual eh o etax e etay
				etay = wad[:,8] #vy

				eta = eta - np.mean(eta)
				etax = etax - np.mean(etax)
				etay = etay - np.mean(etay)

				#varia a freq de amostragem devido as diferencas na coleta (de 1 e 2 Hz)
				if len(eta) >= 2048:
					fs = 2
					nfft = 128 #para 32 gl
					eta = eta[:2048]
					etax = etax[:2048]
					etay = etay[:2048]

				elif len(pr) <= 1200:
					fs = 1
					nfft = 64
					eta = eta[:1024]
					etax = etax[:1024]
					etay = etay[:1024]


				# #profundidade media (retirado da serie de pressao)
				h = np.mean(pr)

				# #cria vetor de tempo (verificar tx de amostragem)
				t = range(1,len(eta)+1)

				# #processamento no dominio do tempo
				hs,h10,hmax,tmed,thmax = proconda.ondat(t,eta,h)

				# #processamento no dominio da frequencia
				hm0, tp, dp, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
				eta,etax,etay,h,nfft,fs)



		# print whd[0,3]




data = np.array(data)





# #caminho linux
# wad = np.loadtxt('C:\Users\Cliente\Documents\LIOC\ST004\Dados_Brutos\Ondas_Direcionais/PTU04_05000.wad')
# whd = np.loadtxt('C:\Users\Cliente\Documents\LIOC\ST004\Dados_Brutos\PTU04_05.whd')

# #carrega datas do arquivo whd
# month = whd[:,0]
# day = whd[:,1]
# year = whd[:,2]
# hour = whd[:,3]

# nfft = 64 #para 32 gl, nfft=64 (16 segmentos calculados com 2 amostras , 'a' e 'b')
# fs = 1 #freq. de amostragem (verificar como automatizar, uma vez que as tx. de amst nao
# #sao as mesmas)

# #cria vetor de data com a funcao datetime
# datas = [datetime(int(year[i]),int(month[i]),int(day[i]),int(hour[i])) for i in range(len(whd))]

# pr = wad[:,2] #pressao
# eta = wad[:,4] #ast ?
# etay = wad[:,7] #vx #verificar qual eh o etax e etay
# etax = wad[:,8] #vy

# #profundidade media (retirado da serie de pressao)
# h = np.mean(pr)

# #cria vetor de tempo (verificar tx de amostragem)
# t = range(1,1025)

# #processamento no dominio do tempo
# hs,h10,hmax,tmed,thmax = proconda.ondat(t,eta,h)


# #processamento no dominio da frequencia
# hm0, tp, dp, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
# eta,etax,etay,h,nfft,fs)
