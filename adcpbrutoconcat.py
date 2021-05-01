# -*- coding: utf-8 -*-
"""
Carrega, processa e concatena todos os dados brutos
de ondas dos ADCPs
- salva os dados de heave, velx e vely 

LIOc - Laboratorio de Instrumentacao Oceanografica
Henrique P P Pereira
Izabel C M Nogueira
Isabel Cabral
Talitha Lourenco
Tamiris Alfama

Ultima modificacao: 14/08/2015

Observacoes
- Cria variaveis com parametros de ondas para cada ADCP
lioc_adcp1, lioc_adcp2, lioc_adcp3 e lioc_adpc4, com:

  0    1    2    3     4  5  
 data, hs, hmax, hm0, tp, dp

Data da ultima modificacao: 15/07/2015
"""

import numpy as np
import pylab as pl
import os
from datetime import datetime
import proconda

pl.close('all')

#pathname
pathname = os.environ['HOME'] + '/Dropbox/lioc/dados/ww3vale/ADCP_Vale/'

paramw1 = [] #parametros de onda para adcp1
paramw2 = [] #parametros de onda para adcp2
paramw3 = [] #parametros de onda para adcp3
paramw4 = [] #parametros de onda para adcp4

#numero de resgates (pulamos o 7 e 13 pq nao tem dados de data (whd) e brutos (wad), respectivamente)
# resgates = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

#loop para cada resgate range(1,16)
for resgate in range(1,16): 

	pathname1 = pathname + 'Resgate_' + str(resgate) + '/'

	print pathname1

	#loop para os 4 ADCPs (ST00x) - range(1,5)
	for adcp in range(1,5):

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

			#cria variavel 'lista' com nome dos arquivos .wad
			lista = np.array(np.sort(os.listdir(pathname2 + 'Ondas_Direcionais/')))

			#varia os arquivos de cada ADCP para cada resgate (numero de arquivos .wad)
			for arquivo in range(len(lista)): #range(len(lista))

				print pathname2 + lista[arquivo] + ' --- ' + str(arquivo)

				wad = np.loadtxt(pathname2 + '/Ondas_Direcionais/' + lista[arquivo])

				#ver correcao da prof para decibar
				pr = wad[:,2] #pressao
				ast = wad[:,3] #ast (col 3 e 4)
				vz = wad[:,9] #velocidade vertical
				
				eta = ast #escolhe se vai processar com vz ou eta
				etay = wad[:,7] #vx #o correto para entrar na rotina de ondaf, a ordem eh eta,etax e etay
				etax = wad[:,8] #vy

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
						nfft = 512 #para 32 gl
						pr = pr[:2048]
						eta = eta[:2048]
						etax = etax[:2048]
						etay = etay[:2048]

					elif len(eta) <= 1200:
						fs = 1
						nfft = 256
						pr = pr[:1024]
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
					hm0, tp, dp, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx,\
					 snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(eta,etax,etay,h,nfft,fs)
					
					# hs = hm0; hmax = hm0 #correcao para o calculo do eta=pressao - erro no procondatempo

					#data em numero inteiro - para salvar .out
					datai = int(str(int(year[arquivo]))+str(int(month[arquivo])).zfill(2)+\
					str(int(day[arquivo])).zfill(2)+str(int(hour[arquivo])).zfill(2)+'00')

					#data com datetime
					datat = ( [datetime(int(year[k]),int(month[k]),int(day[k]),int(hour[k]))\
					 for k in range(len(whd))] )

					#salva arquivos eta, etax e etay
					a = zip(eta,etax,etay)
					np.savetxt('out/bruto/series/ast/adcp'+str(adcp)+'_'+str(datai)+'.out',a,fmt='%.2f',delimiter='\t')

					#cria variaveis com parametros de ondas para cada adcp 
					#  0    1    2    3     4  5  
					# data, hs, hmax, hm0, tp, dp
					if adcp == 1:
						paramw1.append([datai,hs,hmax,hm0,tp,dp])
					elif adcp == 2:
						paramw2.append([datai,hs,hmax,hm0,tp,dp])
					elif adcp == 3:
						paramw3.append([datai,hs,hmax,hm0,tp,dp])
					elif adcp == 4:
						paramw4.append([datai,hs,hmax,hm0,tp,dp])

paramw1 = np.array(paramw1)
paramw2 = np.array(paramw2)
paramw3 = np.array(paramw3)
paramw4 = np.array(paramw4)

#salva arquivos com parametros de onda
pl.savetxt(os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/bruto/parametros/adcp01_lioc_vel.out',paramw1,\
	delimiter=',',fmt=['%i']+5*['%.2f'],header='data,hs,hmax,hm0,tp,dp')
pl.savetxt(os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/bruto/parametros/adcp02_lioc_vel.out',paramw2,\
	delimiter=',',fmt=['%i']+5*['%.2f'],header='data,hs,hmax,hm0,tp,dp')
pl.savetxt(os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/bruto/parametros/adcp03_lioc_vel.out',paramw3,\
	delimiter=',',fmt=['%i']+5*['%.2f'],header='data,hs,hmax,hm0,tp,dp')
pl.savetxt(os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/bruto/parametros/adcp04_lioc_vel.out',paramw4,\
	delimiter=',',fmt=['%i']+5*['%.2f'],header='data,hs,hmax,hm0,tp,dp')
