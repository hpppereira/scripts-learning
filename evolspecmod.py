'''
Evolucao espectral do modelo

'''

import pleds
reload(pleds)
import os
import numpy as np
import pylab as pl
import pleds
from datetime import datetime
import matplotlib.pyplot as plt

#pathname espec swan
#pathname = '/media/lioc/ISABELA/rodadas_tese/swan/'
pathname = '/home/lioc/Dropbox/ww3vale/trocas/msc_isa/Espectros/triad/201302/semtriad/'

#carrega resultado espectral do modelo
#filename = 'spec_point.out'
filename = 'spec_point_ADCP04.out'

######################################################################################################
######################################################################################################
######################################################################################################


def preppledsSWAN(pathname,filename):


	'''
	Programa principal para ler o arquivo do
	SWAN e fazer a PLEDS para 7 dias
	'''

	f = open(pathname + filename)

	#aux = (10,745)
	#espe = np.zeros(aux)
	#dire = np.zeros(aux)

	#define as faixas
	#fx1 = np.arange(0,7)
	#fx2 = np.arange(7,11)
	#fx3 = np.arange(11,16)
	#fx4 = np.arange(16,31)

	lines = f.readlines()

	latlon = lines[7]

	aa = [] #espec 1d concatenado
	date = [] #date (str)
	cont = -1
	for i in range(len(lines)):

		#recupera vetor de frequencia
		if lines[i][0:5]=='RFREQ':
			print 'Linha do vetor de frequencia: ' + str(i) 
			nfreq = int(lines[i+1][0:10]) #tamanho do vetor de freq
			vfreq = np.array(lines[i+2:i+2+nfreq]).astype(float)

		#recupera o vetor de direcao
		if lines[i][0:4]=='NDIR':
			print 'Linha do vetor de direcao: ' + str(i) 
			ndir = int(lines[i+1][0:10]) #tamanho do vetor de freq
			vdire = np.array(lines[i+2:i+2+ndir]).astype(float)

		#recupera os espectros, integra, corrige com o fator de correcao
		#separa as 4 faixas de frequencia, calcula a energia e direcao
		#para cada faixa

		if lines[i][0:6] == 'FACTOR':
			cont += 1
			print cont
			print 'Data do Espectro: ' + lines[i-1][0:15]

			date.append(lines[i-1][0:15])

			fator = float(np.array(lines[i+1]).astype(float))
			
			#cria array com o espe2d
			espec2d = []
			for j in range(nfreq):
				espec2d.append(lines[i+2+j].split())
			
			espe2d = np.array(espec2d).astype(float) * fator
			espe1d = np.sum(espe2d,axis=1)

			print str(4*np.sqrt(sum(espe1d)*0.0107))

			aa.append(espe1d)


	aa = np.array(aa).T

	return espe1d, espe2d, aa, date, vfreq, vdire


######################################################################################################
######################################################################################################
######################################################################################################


#recupera os espectros 1d e 2d (aa - 1d concatenado)
espe1d, espe2d, aa, date, vfreq, vdire = preppledsSWAN(pathname, '/' + filename)

espe1d = espe1d / (abs(vdire[3]-vdire[2])*(np.pi/180))

date = [datetime.strptime(date[i], '%Y%m%d.%H%M%S') for i in range(len(date))]

fig = plt.figure(figsize=(15,9))
ax1 = fig.add_subplot(411)
ax1.contour(date, vfreq, aa, 20) #[0.05,0.08,0.10, 0.15, 0.20])
ax1.set_xticklabels(ax1.get_xticklabels(), visible=False)
ax1.grid()
#ax1.set_axes('tight')
ax1.set_ylim(0.05,0.4)
ax1.set_ylabel('Freq. (Hz)')



np.savetxt(os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/mod/freq_mod_201302_semtriad_ADCP04.txt', vfreq)
np.savetxt(os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/mod/espe1d_mod_201302_semtriad_ADCP04.txt', aa)

