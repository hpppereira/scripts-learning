#rotina para processamentos dos dados de onda da bacia de campos
#utilizando a proc. tradicional e a datt
#os dados estao a cada 3 horas.
#tentar fazer a plogam do dp total e os dp divididos por faixas,
#para identificar o sea e swell

import numpy as np
import pylab as pl
import datetime
import os
import proconda
import espec
import daat_oc1
import numeronda

reload(daat_oc1)

pl.close('all')

#caminho onde estao os arquivos .HNE
pathname = os.environ['HOME'] + '/Google Drive/bcampos_ondas/bcampos_jun92/'

ano = 1992
mes = 06

lista = []
# Lista arquivos do diretorio atual
for f in os.listdir(pathname):
	if f.endswith('.DAT'):
		lista.append(f)
lista=np.sort(lista)

h = 500 #profundidade
nfft = 64 #numero de dados para a fft
fs = 1 #freq de amostragem
nlin = 1024 #comprimento da serie temporal a ser processada
ncol = len(lista) #numero de arquivos a serem processados

espe1, energ, dire1 = daat_oc1.daat1(pathname,lista,nfft,fs,ncol)

matonda = []
datat = []
dp1 = []
dp2 = []
dp3 = []
dp4 = []

#define as faixas de frequencia para a LH
f1 = range(3,6)
f2 = range(6,10)
f3 = range(10,18)
f4 = range(18,32)

# lista = lista[0]

for i in range(len(lista)):

	print 'LH: ' + str(i)

	t, eta, etax, etay = np.loadtxt(pathname + lista[i], unpack=True)

	datat.append( datetime.datetime(ano,int(lista[i][2:4]),int(lista[i][4:6]),int(lista[i][6:8])) )

	#processamento no dominio do tempo
	pondat = proconda.ondat(t,eta,h)

	#processamento no dominio da frequencia
	pondaf = proconda.ondaf(eta,etax,etay,h,nfft,fs)

	#parametros de onda = [Hs,H10,Hmax,Tmed,THmax,Hm0,Tp,Dp]
	matonda.append(np.concatenate([pondat,pondaf]))

	#espectro simples
	sn = espec.espec1(eta,nfft,fs)
	sny = espec.espec1(etax,nfft,fs)
	snz = espec.espec1(etay,nfft,fs)

	#calculo dos espectros cruzados
	snnx = espec.espec2(eta,etax,nfft,fs)
	snny = espec.espec2(eta,etay,nfft,fs)
	snxny = espec.espec2(etax,etay,nfft,fs)

	#vetor de frequencia
	f = sn[:,0]

	#calculo do numero de onda
	k = numeronda.k(h,f,len(f))
	k = np.array(k)

	#calculo dos coeficientes de fourier
	a1 = snnx[:,3] / (k * np.pi * sn[:,1])
	b1 = snny[:,3] / (k * np.pi * sn[:,1])

	#calcula direcao de onda
	dire = np.array([np.angle(np.complex(b1[i],a1[i]),deg=True) for i in range(len(a1))])

	#condicao para valores maiores que 360 e menores que 0
	dire[np.where(dire < 0)] = dire[np.where(dire < 0)] + 360
	dire[np.where(dire > 360)] = dire[np.where(dire > 360)] - 360

    #indice da frequencia de pico para as 4 bandas (32 gl)
	aux1 = pl.find(sn[f1,1] == max(sn[f1,1]))
	aux2 = pl.find(sn[f2,1] == max(sn[f2,1]))
	aux3 = pl.find(sn[f3,1] == max(sn[f3,1]))
	aux4 = pl.find(sn[f4,1] == max(sn[f4,1]))

	#direcao do periodo de pico (para 32 gl)
	dp1.append( dire[np.where(f == f[f1][aux1])] )
	dp2.append( dire[np.where(f == f[f2][aux2])] )
	dp3.append( dire[np.where(f == f[f3][aux3])] )
	dp4.append( dire[np.where(f == f[f4][aux4])] )

matonda = np.array(matonda)

pl.figure()
pl.subplot(311), pl.grid('on')
pl.plot(datat,matonda[:,-3],'o'), pl.tick_params(labelbottom='off')
pl.title('Significant Wave Height (Hm0)'), pl.ylabel('meters')
pl.axis('tight')
pl.subplot(312), pl.grid('on')
pl.plot(datat,matonda[:,-2],'o'), pl.tick_params(labelbottom='off')
pl.title('Peak Period (Tp)'), pl.ylabel('seconds')
pl.axis('tight')
pl.subplot(313), pl.grid('on')
pl.plot(datat,matonda[:,-1],'o')
pl.title('Peak Direction (Dp)'), pl.ylabel('degrees')
pl.axis([727350.04166666663,727379.91666666663,0,360])

pl.figure()
pl.subplot(411), pl.grid('on')
pl.plot(datat,dp1,'o'),pl.tick_params(labelbottom='off')
pl.plot(datat,dire1[0,:],'ro'),pl.tick_params(labelbottom='off')
pl.title('Peak Direction (Dp)\n Range 1 - dir:1'), pl.ylabel('degrees')
pl.legend(['LH','DAAT'],loc=2,prop={'size':9})
pl.axis([727350.04166666663,727379.91666666663,0,360])
pl.subplot(412), pl.grid('on')
pl.plot(datat,dp2,'o'),pl.tick_params(labelbottom='off')
pl.plot(datat,dire1[2,:],'ro'), pl.tick_params(labelbottom='off')
pl.title('Range 2 - dir:1'), pl.ylabel('degrees')
pl.axis([727350.04166666663,727379.91666666663,0,360])
pl.subplot(413), pl.grid('on')
pl.plot(datat,dp3,'o'), pl.tick_params(labelbottom='off')
pl.plot(datat,dire1[4,:],'ro'), pl.tick_params(labelbottom='off')
pl.title('Range 3 - dir:1'), pl.ylabel('degrees')
pl.axis([727350.04166666663,727379.91666666663,0,360])
pl.subplot(414), pl.grid('on')
pl.plot(datat,dp4,'o')
pl.plot(datat,dire1[5,:],'ro')
pl.title('Range 3 - dir:2'), pl.ylabel('degrees')
pl.axis([727350.04166666663,727379.91666666663,0,360])

pl.show()