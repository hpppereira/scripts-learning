'''
Processamento dos dados brutos de Ondas do ADCP
da Vale

- Escolhe o ADCP e o Resgate a ser processado
- Compara com os dados da Planilha com dados
processados pela Vale 

LIOc - Laboratorio de Instrumentacao Oceanografica
Henrique P P Pereira
Izabel C M Nogueira
Isabel Cabral
Talitha Lourenco
Tamiris Alfama
'''

import os
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import proconda
from datetime import datetime

plt.close('all')

resgate = '6'
adcp = '3'


pathname = os.environ['HOME'] + '/Dropbox/lioc/dados/ww3vale/ADCP_Vale/Resgate_' + resgate + '/ST00' + adcp + '/Dados_Brutos/'

#   0   1    2     3     4     5    
# mes, dia, ano, hora, pitch, roll
whd = np.loadtxt(pathname + 'PTU0' + adcp + '_0' + resgate + '.whd',usecols=(0,1,2,3,12,13))

data1 = ( [datetime(int(whd[k,2]),int(whd[k,0]),int(whd[k,1]),int(whd[k,3])) for k in range(len(whd))] )

arqs = np.sort(np.array(os.listdir(pathname + '/Ondas_Direcionais')))

# aux = pl.find(arq[:,0]==1)

data = []
paramw = []
for i in range(len(arqs)):

	print str(i) + '  --  ' + str(arqs[i])

	wad = np.loadtxt(pathname + 'Ondas_Direcionais/' + arqs[i])

	#ver correcao da prof para decibar
	pr = wad[:,2] #pressao
	eta = wad[:,3] #ast (col 3 e 4)
	etay = wad[:,7] #vx #o correto para entrar na rotina de ondaf, a ordem eh eta,etax e etay
	etax = wad[:,8] #vy

	if len(eta) < 1024:

		print '----  :ARQUIVO INCONSISTENTE -- comprimento do vetor < 1024'
		#pass

	elif np.mean(pr) < 2:

		print '----  :ARQUIVO INCONSISTENTE -- media da pressao < 2 mBar'
		#pass

	else:

		data.append(data1[i])

		# pr = pr - np.mean(pr)
		# eta = eta - np.mean(eta)
		# etax = etax - np.mean(etax)
		# etay = etay - np.mean(etay)

		#varia a freq de amostragem devido as diferencas na coleta (de 1 e 2 Hz)
		if len(eta) >= 2048:
			fs = 2
			nfft = 128 #para 32 gl
			pr = pr[:2048]
			eta = eta[:2048]
			etax = etax[:2048]
			etay = etay[:2048]

		elif len(eta) <= 1200:
			fs = 1
			nfft = 64
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
		hm0, tp, dp, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx,snyny, a1, b1, a2, b2,\
		 dire1, dire2 = proconda.ondaf(eta,etax,etay,h,nfft,fs)
		
		paramw.append([hm0,tp,dp])

paramw = np.array(paramw)



############################################################################
#carrega dados processados pelo lioc a partir das planilhas processadas da vale

#diretorio de onde estao os dados processados
pathname  = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/proc/parametros/'

#   0    1    2     3     4      5       6      7   8
# data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02'
ddv = np.loadtxt(pathname + 'vale_adcp' + adcp + '.out',delimiter=',')

#data com datetime
datav = [datetime(int(str(ddv[i,0])[0:4]),int(str(ddv[i,0])[4:6]),int(str(ddv[i,0])[6:8]),
    int(str(ddv[i,0])[8:10]),int(str(ddv[i,0])[10:12])) for i in range(len(ddv))]

############################################################################


plt.figure()
plt.subplot(311)
plt.plot(datav,ddv[:,1],'b')
plt.plot(data,paramw[:,0],'r')
plt.subplot(312)
plt.plot(data,paramw[:,1],'b.')
plt.plot(datav,ddv[:,7],'r.')
plt.subplot(313)
plt.plot(data,paramw[:,2],'b.')
plt.plot(datav,ddv[:,4],'r.')


plt.show()