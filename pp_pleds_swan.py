'''
Programa principal para ler o arquivo do
SWAN e fazer a PLEDS para 7 dias

'''

import os
import numpy as np
import pylab as pl
import pleds
from datetime import datetime 

reload(pleds)

#onde estao os arquivo do espectro
pathname = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/Previsao/Previsao_14maio/20150513/'
filename = 'spec_point_ADCP10.out'

data = pathname[-9:-1]
datat = datetime.strptime(data,'%Y%M%d')

#titulo da figura
tit = 'DIRECTIONAL WAVE SPECTRUM - Previsao - ' + filename[-10:-4] + ' - Vale - ' + str(datat)[:-9]

dia = int(pathname[-3:-1]) - 1
f = open(pathname + filename)

aux = (10,744)
espe = np.zeros(aux)
dire = np.zeros(aux)

#define as faixas
fx1 = np.arange(0,7)
fx2 = np.arange(7,11)
fx3 = np.arange(11,16)
fx4 = np.arange(16,31)

lines = f.readlines()

latlon = lines[7]


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

		fator = float(np.array(lines[i+1]).astype(float))

		#cria array com o espe2d
		espec2d = []
		for j in range(nfreq):
			espec2d.append(lines[i+2+j].split())
		
		espe2d = np.array(espec2d).astype(float) * fator
		espe1d = np.sum(espe2d,axis=1)
		print str(4*np.sqrt(sum(espe1d)*0.0107))

		#cria matriz espe (para a pleds)
		espe[0,cont] = np.sum(espe1d[fx1])
		espe[2,cont] = np.sum(espe1d[fx2])
		espe[4,cont] = np.sum(espe1d[fx3])
		espe[6,cont] = np.sum(espe1d[fx4])

		#cria matriz de direcao (para a pleds)

		#soma as energia das faixas (para verificar o indice da direcao)
		s1 = np.sum(espe2d[fx1],axis=0)
		is1 = pl.find(s1 == max(s1))
		s2 = np.sum(espe2d[fx2],axis=0)
		is2 = pl.find(s2 == max(s2))
		s3 = np.sum(espe2d[fx3],axis=0)
		is3 = pl.find(s3 == max(s3))
		s4 = np.sum(espe2d[fx4],axis=0)
		is4 = pl.find(s4 == max(s4))

		dire[0,cont] = np.mean(vdire[is1])
		dire[2,cont] = np.mean(vdire[is2])
		dire[4,cont] = np.mean(vdire[is3])
		dire[6,cont] = np.mean(vdire[is4])


#limita os valores para a quantidade valores

#valores horarios
espe1 = espe[:,:cont] * 50
aux = pl.rand(10,espe1.shape[1]) * 20 - 20/2 
dire1 = dire[:,:cont] + aux

#espectro a cada 3 horas com rand
# espe1 = espe[:,0:-1:3] * 20
# aux = pl.rand(10,espe1.shape[1]) * 10 - 5 
# dire1 = dire[:,0:-1:3] + aux

#chama a pleds
pleds.pledsSWAN(espe1,dire1,tit,dia)








