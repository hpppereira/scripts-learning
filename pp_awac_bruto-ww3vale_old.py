# -*- coding: utf-8 -*-
"""
Carrega e processa os dados brutos do ADCP da Vale

Data da ultima modificacao: 10/02/2015

"""

import numpy as np
import pylab as pl
import os
from datetime import datetime
import proconda

pl.close('all')

#pathname
pathname = os.environ['HOME'] + '/Dropbox/lioc/dados/ww3vale/ADCP/bruto/ADCP_Vale_1_2/'

paramw1 = [] #parametros de onda spara adcp1
paramw2 = [] #parametros de onda spara adcp2
paramw3 = [] #parametros de onda spara adcp3
paramw4 = [] #parametros de onda spara adcp4

#numero de resgates (pulamos o 7 e 13 pq nao tem dados de data (whd) e brutos (wad), respectivamente)
# resgates = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]


#loop para cada resgate range(1,16)
for resgate in range(4,5): 

	pathname1 = pathname + 'Resgate_' + str(resgate) + '/'

	print pathname1

	#loop para os 4 ADCPs (ST00x) - range(1,5)
	for adcp in range(1,2):

		data = [] #data com datetime

		pathname2 = pathname1 + 'ST00' + str(adcp) + '/Dados_Brutos/'

		arq_whd = 'PTU0' + str(adcp) + '_0' + str(resgate) + '.whd'
		# pathname_arq_whd = pathname2 + 'PTU0' + str(adcp) + '_0' + str(resgate) + '.whd'
		pathname_arq_whd = pathname2 + arq_whd

		#verifica se tem a pasta /Ondas_Direcionais/
		if ('Ondas_Direcionais' in os.listdir(pathname2)) == False: #os.listdir(pathname2) == []: #resgate-1, ST001
			print pathname2 + ' -- nao tem o diretorio /Ondas_Direcionais'
			pass

		#verifica se tem arquivos .wad na pasta /Ondas_Direcionas/
		elif os.listdir(pathname2 + 'Ondas_Direcionais/') == []:
			print pathname2 + ' -- Ondas_Direcionais -- diretorio vazio'
			pass
		
		#verifica se tem o arquivo .whd com as datas
		elif (arq_whd in os.listdir(pathname2)) == False:
			print pathname2 + ' -- nao tem o arquivo .whd'
			pass

		else:

			print pathname2

			# 1,   2,   3,   4,   5
			#mes, dia, ano, hora, min
			#carrega arquivo .whd
			# whd = np.loadtxt(pathname2 + 'PTU0' + str(adcp) + '_0' + str(resgate) + '.whd')
			whd = np.loadtxt(pathname_arq_whd)

			#carrega datas do arquivo whd
			month = whd[:,0]
			day = whd[:,1]
			year = whd[:,2]
			hour = whd[:,3]

			data = ( [datetime(int(year[k]),int(month[k]),int(day[k]),int(hour[k])) for k in range(len(whd))] )


			#cria variavel 'lista' com nome dos arquivos .wad
			lista = np.array(os.listdir(pathname2 + 'Ondas_Direcionais/'))

			#varia os arquivos de cada ADCP para cada resgate (numero de arquivos .wad)
			for arquivo in range(len(lista)): #range(len(lista))

				#condicao para arquivos inconsistentes (modifcar para as rotinas de consistencia)
				# if l == 0:
				# 	pass
				# else:

				print pathname2 + lista[arquivo] + ' --- ' + str(arquivo)

				wad = np.loadtxt(pathname2 + '/Ondas_Direcionais/' + lista[arquivo])

				#ver correcao da prof para decibar
				pr = wad[:,2] #pressao
				eta = wad[:,3] #ast (col 3 e 4)
				etax = wad[:,7] #vx #o correto para entrar na rotina de ondaf, a ordem eh eta,etax e etay
				etay = wad[:,8] #vy

				if len(eta) < 1024:

					print '---- ' + str(lista[arquivo]) + ' :ARQUIVO INCONSISTENTE -- comprimento do vetor < 1024'
					pass

				elif np.mean(pr) < 2:

					print '---- ' + str(lista[arquivo]) + ' :ARQUIVO INCONSISTENTE -- media da pressao < 2 mBar'
					pass

				else:

					pr = pr - np.mean(pr)
					eta = eta - np.mean(eta)
					etax = etax - np.mean(etax)
					etay = etay - np.mean(etay)

					#varia a freq de amostragem devido as diferencas na coleta (de 1 e 2 Hz)
					if len(eta) >= 2048:
						fs = 2
						nfft = 512 #128 para 32 gl; 512 para 8 gl
						eta = eta[:2048]
						etax = etax[:2048]
						etay = etay[:2048]

					elif len(eta) <= 1200:
						fs = 1
						nfft = 256
						eta = eta[:1024]
						etax = etax[:1024]
						etay = etay[:1024]


					#profundidade media (retirado da serie de pressao - ver correcao de dbar para metros)
					h = np.mean(pr) - 10

					#cria vetor de tempo (verificar tx de amostragem)
					t = range(1,len(eta)+1)

					#processamento no dominio do tempo
					hs,h10,hmax,tmed,thmax = proconda.ondat(t,eta,h)

					#processamento no dominio da frequencia
					hm0, tp, dp, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = \
					proconda.ondaf(eta,etax,etay,h,nfft,fs)

					#cria variaveis com parametros de ondas para cada adcp 
					#  0    1    2    3     4   5    6     7   8 
					# ano, mes, dia, hora, hs, hmax, hm0, tp, dp
					if adcp == 1:
						paramw1.append([year[arquivo],month[arquivo],day[arquivo],hour[arquivo],hs,hmax,hm0,tp,dp])
					elif adcp == 2:
						paramw2.append([year[arquivo],month[arquivo],day[arquivo],hour[arquivo],hs,hmax,hm0,tp,dp])
					elif adcp == 3:
						paramw3.append([year[arquivo],month[arquivo],day[arquivo],hour[arquivo],hs,hmax,hm0,tp,dp])
					elif adcp == 4:
						paramw4.append([year[arquivo],month[arquivo],day[arquivo],hour[arquivo],hs,hmax,hm0,tp,dp])

		# print whd[0,3]

paramw1 = np.array(paramw1)
paramw2 = np.array(paramw2)
paramw3 = np.array(paramw3)
paramw4 = np.array(paramw4)

data1 = ( [datetime(int(paramw1[k,0]),int(paramw1[k,1]),int(paramw1[k,2]),int(paramw1[k,3])) for k in range(len(paramw1))] )
data2 = ( [datetime(int(paramw2[k,0]),int(paramw2[k,1]),int(paramw2[k,2]),int(paramw2[k,3])) for k in range(len(paramw2))] )
data3 = ( [datetime(int(paramw3[k,0]),int(paramw3[k,1]),int(paramw3[k,2]),int(paramw3[k,3])) for k in range(len(paramw3))] )
data4 = ( [datetime(int(paramw4[k,0]),int(paramw4[k,1]),int(paramw4[k,2]),int(paramw4[k,3])) for k in range(len(paramw4))] )

#paramwX
#  0    1    2     3   4    5     6    7  8
# ano, mes, dia, hora, hs, hmax, hm0, tp, dp

pl.figure()
pl.subplot(311)
pl.plot(data1,paramw1[:,4],'o',label='Hs')
pl.plot(data1,paramw1[:,5],'o',label='Hmax')
pl.plot(data1,paramw1[:,6],'o',label='Hm0')
pl.axis([data1[0],data1[-1],0,5])
pl.legend(), pl.grid()
pl.subplot(312)
pl.plot(data1,paramw1[:,7],'o',label='Tp')
pl.axis([data1[0],data1[-1],0,20])
pl.legend(), pl.grid()
pl.subplot(313)
pl.plot(data1,paramw1[:,8],'o',label='Dp')
pl.axis([data1[0],data1[-1],0,360])
pl.legend(), pl.grid()

pl.show()


#salva arquivos
pl.savetxt(os.environ['HOME'] + '/Dropbox/ww3vale_old/Geral/TU/rot/saida/bruto/paramw1.out',paramw1)
#pl.savetxt(os.environ['HOME'] + '/Dropbox/ww3vale_old/Geral/TU/rot/saida/bruto/paramw2.out',paramw2)
#pl.savetxt(os.environ['HOME'] + '/Dropbox/ww3vale_old/Geral/TU/rot/saida/bruto/paramw3.out',paramw3)
#pl.savetxt(os.environ['HOME'] + '/Dropbox/ww3vale_old/Geral/TU/rot/saida/bruto/paramw4.out',paramw4)

# pl.savetxt()

# data = np.array(data)
# datap = data[:arquivo] #data com datetime para plotagem

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

