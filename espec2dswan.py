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
pathname = os.environ['HOME'] + '/Dropbox/Previsao/vale/resultados/20151108/'

data = pathname[-9:-1]
datat = datetime.strptime(data,'%Y%M%d')

filenames = ['spec_point_ADCP01.out',
		     'spec_point_ADCP02.out',
		     'spec_point_ADCP03.out',
		     'spec_point_ADCP10.out']

for filename in filenames:



	#titulo da figura
#	tit = 'DIRECTIONAL WAVE SPECTRUM - Previsao - ' + filename[-10:-4] + ' - Vale - ' + str(datat)[:-9]

	#dia = int(pathname[-3:-1]) - 2
	f = open(pathname + filename)

#	aux = (10,744)
#	espe = np.zeros(aux)
#	dire = np.zeros(aux)

	#define as faixas
#	fx1 = np.arange(0,7)
#	fx2 = np.arange(7,11)
#	fx3 = np.arange(11,16)
#	fx4 = np.arange(16,31)

	lines = f.readlines()

#	latlon = lines[7]


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
			#print cont
			print 'Data do Espectro: ' + lines[i-1][0:15]

			datae = datetime.strptime(lines[i-1][0:15],'%Y%m%d.%H%M%S')
			datae1 = datetime.strftime(datae,'%d/%m/%Y - %Hh')
			datae2 = datetime.strftime(datae,'%Y%m%d%H')
			
			fator = float(np.array(lines[i+1]).astype(float))

			#cria array com o espe2d
			espec2d = []
			for j in range(nfreq):
				espec2d.append(lines[i+2+j].split())
			
			espe2d = np.array(espec2d).astype(float) * fator
			espe1d = np.sum(espe2d,axis=1)
			print str(4*np.sqrt(sum(espe1d)*0.155))
                        nf = np.where(espe1d == np.max(espe1d))
			fp = vfreq[nf]
			print str(1./fp)
			
                        


			pl.figure()
			pl.plot(vfreq,espe1d)
			pl.title('Espectro Unidirecional - ' + datae1)
			pl.xlabel('Freq. (Hz)')
			pl.ylabel('m2/Hz')
			pl.savefig(os.environ['HOME'] + '/Dropbox/Previsao/vale/espectro/espec1d_' + filename[:-4] + '_' + datae2 + '.png')
			
			pl.figure()
			pl.contourf(vfreq,np.linspace(0,360,len(vdire)),espe2d.T)
			pl.title('Espectro Direcional - ' + datae1)
			pl.xlabel('Freq. (Hz)')
			pl.ylabel('Dir. (Graus)')
			pl.colorbar(label='m2/Hz')
			pl.yticks(range(0,360+45,45))
			pl.savefig(os.environ['HOME'] + '/Dropbox/Previsao/vale/espectro/espec2d_' + filename[:-4] + '_' + datae2 + '.png')
			
			#pl.show()
			
			pl.close('all')




