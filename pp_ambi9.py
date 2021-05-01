''' Processamento dos dados de onda do sensor 
	gx3 e Axys em Mexilhao
	Projeto: GX3 - Ambidados

	Comparacao dos espectros de heave obtido
	por integracao do sensor GX3 e do espectro
	de heave da Axys
'''

import numpy as np
from matplotlib import pylab as pl
from datetime import datetime
import os
import espec
import loadhne


pl.close('all')

pathname_gx3 = os.environ['HOME'] + '/Dropbox/lioc/ambid/dados/Mexilhao-axys_gx3_2014/gx3/'
pathname_axys = os.environ['HOME'] + '/Dropbox/lioc/ambid/dados/Mexilhao-axys_gx3_2014/axys/HNE/'

az_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbacelZ.dat',
	dtype=str,delimiter=',',skiprows=4)
av_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbaclV.dat',
	dtype=str,delimiter=',',skiprows=4)
aew_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbaclEW.dat',
	dtype=str,delimiter=',',skiprows=4)
ans_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbaclNS.dat',
	dtype=str,delimiter=',',skiprows=4)

#numero de arquivos a serem processados
narq = 2323

data_gx3_str = az_gx3[0:narq,0] #data em string

#dados de acel. do gx3 em float (1024x2323)
az_gx3 = az_gx3[0:narq,range(2,az_gx3.shape[1])].astype(float).T
av_gx3 = av_gx3[0:narq,range(2,av_gx3.shape[1])].astype(float).T
aew_gx3 = aew_gx3[0:narq,range(2,aew_gx3.shape[1])].astype(float).T
ans_gx3 = ans_gx3[0:narq,range(2,ans_gx3.shape[1])].astype(float).T

#lista dos arquivos da axys
lista_axys = loadhne.lista_hne(pathname_axys)

data_axys_str = []
eta_axys = []
etay_axys = []
etax_axys = []

#loop para carregar todos os dados da axys, e monta matriz (1312x2328) ?
for i in range(len(lista_axys)):

	dados_axys = loadhne.dados_hne(pathname_axys, lista_axys[i])[0]
	data_axys_str.append(lista_axys[i][0:12])
	eta_axys.append(dados_axys[:,1])
	etay_axys.append(dados_axys[:,2])
	etax_axys.append(dados_axys[:,3])


#pega apenas os dados que tem axys e gx3
data_axys_str = data_axys_str[0:narq]
eta_axys = np.array(eta_axys[0:narq]).T
etay_axys = np.array(etay_axys[0:narq]).T
etax_axys = np.array(etax_axys[0:narq]).T

# -- datas com datetime -- #

# data_gx3 = [datetime.strptime(data[i], '%d.%m.%Y %H:%M:%S') for i in range(len(data))]
data_gx3 = [datetime.strptime(data_gx3_str[i], '"%Y-%m-%d %H:%M:%S"') for i in range(len(data_gx3_str))]
data_axys = [datetime.strptime(data_axys_str[i], '%Y%m%d%H%M%S') for i in range(len(data_axys_str))]

# -- definicao dos parametros de onda -- #

#parametros axys e gx3
fs_gx3 = 1
nfft_gx3 = 64 #256-8gl ; 64-32gl
fs_axys = 1.28
nfft_axys = 86 # 345-8gl ; 86-32gl

dt_gx3 = 1./fs_gx3
dt_axys = 1./fs_axys

# vetor de tempo de amostragem
t_gx3 = np.arange(0,len(az_gx3)*dt_gx3,dt_gx3)
t_axys = np.arange(0,len(eta_axys)*dt_axys,dt_axys)

#fazer timepstring nas datas da axys

#serie a ser processada
#series legais: 810, 110, 
s1 = 0 #primeiro arquivo a ser processado
s2 = narq #ultimo arquivo a ser processado
pp = 0 

# -- inicializacao -- #

eta_gx3_mat = [] #matriz com series de heave da gx3 (eta1)
aa_az_gx3 = [] #matriz do espectro de aceleracao
aa_eta_gx3 = [] #matriz com espectro de heave (/w4)
aa_eta1_gx3 = [] #matriz com espectro de heave integrando a serie de acZ
aa_eta_axys = [] #matriz com espectros da axys

for kk in range(s1,s2):

	# -- obter o deslocamento pelo metodo dos trapezios -- #

	#metodo dos trapezios: ([Xi + Xi+1]/2)
	n1 = az_gx3

	#calcula a velocidade (a partir da aceleracao)
	vz_gx3 = []
	for i in range(len(az_gx3)-1):
		vz_gx3.append( (n1[i,kk] + n1[i+1,kk]) / 2 )
	vz_gx3 = np.array(vz_gx3 - np.mean(vz_gx3))

	#calcula o deslocamento (a partir da serie de velocidade)
	eta_gx3 = []
	for i in range(len(vz_gx3)-1):
		eta_gx3.append( (vz_gx3[i] + vz_gx3[i+1]) / 2 )
	eta_gx3 = np.array(eta_gx3 - np.mean(eta_gx3))

	#coloca dois zeros nos ultimos indices
	eta_gx3 = np.concatenate((eta_gx3,([0,0])))

	#matriz com series temporais de elevacao do gx3 - int
	eta_gx3_mat.append(eta_gx3)

	# -- espectros -- #

	#espectro de aceleracao - gx3
	aa_az_gx3_aux = espec.espec1(az_gx3[:,kk],nfft_gx3,fs_gx3)

	#omega a quarta
	w4 = (2 * np.pi * aa_az_gx3_aux[:,0]) ** 4

	#espectro de heave dividindo por w4
	aa_eta_gx3_aux = aa_az_gx3_aux[:,1] / w4

	#espectro de heave da serie de acZ integrada no tempo - gx3
	aa_eta1_gx3_aux = espec.espec1(eta_gx3,nfft_gx3,fs_gx3)

	#espectro de heave - axys
	aa_eta_axys_aux = espec.espec1(eta_axys[:,kk],nfft_axys,fs_axys)

	#cria matriz dos espectros de heave - gx3 e axys
	aa_az_gx3.append( aa_az_gx3_aux[:,1] ) #espectro de aceleracao - gx3
	aa_eta_gx3.append( aa_eta_gx3_aux ) #espectro de heave w4 - gx3
	aa_eta1_gx3.append( aa_eta1_gx3_aux[:,1] ) #espectro de heave int - gx3
	aa_eta_axys.append( aa_eta_axys_aux[:,1] ) #espectro de heave - axys

#matriz com espectros de heave do gx3	
aa_az_gx3 = np.array(aa_az_gx3).T #espectro de aceleracao - gx3
aa_eta_gx3 = np.array(aa_eta_gx3).T #espectro de heave w4 - gx3
aa_eta1_gx3 = np.array(aa_eta1_gx3).T #espectro de heave int - gx3
aa_eta_axys = np.array(aa_eta_axys).T #espectro de heave - axys
eta_gx3_mat = np.array(eta_gx3_mat).T #matriz com series temporais de heave - gx3

#vetor de frequencia
f_gx3 = aa_az_gx3_aux[:,0] #gx3 
f_axys = aa_eta_axys_aux[:,0] #axys 

# -- figuras -- #

# fig 1 - series temporais da axys e gx3

aux1 = 2000

pl.figure()
pl.title('Series temporais' + data_gx3[aux1].strftime('%Y-%m-%d %H:%M'))
pl.plot(t_gx3,az_gx3[:,aux1],'b',label='gx3')
pl.ylabel('gx3 - g'), pl.legend(loc=2)
pl.twinx()
pl.plot(t_axys,eta_axys[:,aux1],'r',label='axys')
pl.ylabel('axys - m'), pl.legend(loc=1)


# fig 2 - espectro de az, heave-w4 e heave-int

pl.figure()
pl.subplot(131)
pl.plot(f_gx3,aa_az_gx3[:,pp])
pl.title('Espectro de Ac.Z')
pl.ylabel('Energia')

pl.subplot(132)
pl.plot(f_gx3,aa_eta_gx3[:,pp])
pl.title('Espectro de Heave (/w4)') #' - ' + data[s2])
pl.axis([0,f_gx3[-1],0,0.01])
pl.xlabel('Frequencia')

pl.subplot(133)
pl.plot(f_gx3,aa_eta1_gx3[:,pp])
pl.title('Espectro de Heave (int)') #' - ' + data[s2])

# fig 3 - 

pl.figure()
pl.plot(f_gx3,aa_eta1_gx3[:,pp],'b',label='gx3-int')
pl.ylabel('gx3 - m2/Hz'), pl.legend(loc=2)
pl.twinx()
pl.plot(f_axys,aa_eta_axys[:,pp],'r',label='axys')
pl.ylabel('axys - m2/Hz'), pl.legend(loc=1)


# fig 4 - comparacao axys e heave integrado

fig1 = 100
fig2 = 500
fig3 = 1000
fig4 = 2000

pl.figure()
pl.subplot(221)
pl.title(data_gx3[fig1].strftime('%Y-%m-%d %H:%M'))
pl.plot(f_gx3,aa_eta1_gx3[:,fig1],'b',label='gx3-int')
pl.ylabel('gx3 - m2/Hz'), pl.legend(loc=2)
pl.twinx()
pl.plot(f_axys,aa_eta_axys[:,fig1],'r',label='axys')
pl.ylabel('axys - m2/Hz'), pl.legend(loc=1)

pl.subplot(222)
pl.title(data_gx3[fig2].strftime('%Y-%m-%d %H:%M'))
pl.plot(f_gx3,aa_eta1_gx3[:,fig2],'b',label='gx3-int')
pl.ylabel('gx3 - m2/Hz'), pl.legend(loc=2)
pl.twinx()
pl.plot(f_axys,aa_eta_axys[:,fig2],'r',label='axys')
pl.ylabel('axys - m2/Hz'), pl.legend(loc=1)

pl.subplot(223)
pl.title(data_gx3[fig3].strftime('%Y-%m-%d %H:%M'))
pl.plot(f_gx3,aa_eta1_gx3[:,fig3],'b',label='gx3-int')
pl.ylabel('gx3 - m2/Hz'), pl.legend(loc=2)
pl.twinx()
pl.plot(f_axys,aa_eta_axys[:,fig3],'r',label='axys')
pl.ylabel('axys - m2/Hz'), pl.legend(loc=1)

pl.subplot(224)
pl.title(data_gx3[fig4].strftime('%Y-%m-%d %H:%M'))
pl.plot(f_gx3,aa_eta1_gx3[:,fig4],'b',label='gx3-int')
pl.ylabel('gx3 - m2/Hz'), pl.legend(loc=2)
pl.twinx()
pl.plot(f_axys,aa_eta_axys[:,fig4],'r',label='axys')
pl.ylabel('axys - m2/Hz'), pl.legend(loc=1)

# fig 5 - comparacao axys e espec heave / w4

pl.figure()
pl.subplot(221)
pl.title(data_gx3[fig1].strftime('%Y-%m-%d %H:%M'))
pl.plot(f_gx3,aa_eta_gx3[:,fig1],'b',label='gx3-w4'), pl.axis([0,f_gx3[-1],0,0.015])
pl.ylabel('gx3 - m2/Hz'), pl.legend(loc=2)
pl.twinx()
pl.plot(f_axys,aa_eta_axys[:,fig1],'r',label='axys')
pl.ylabel('axys - m2/Hz'), pl.legend(loc=1)

pl.subplot(222)
pl.title(data_gx3[fig2].strftime('%Y-%m-%d %H:%M'))
pl.plot(f_gx3,aa_eta_gx3[:,fig2],'b',label='gx3-w4'), pl.axis([0,f_gx3[-1],0,0.004])
pl.ylabel('gx3 - m2/Hz'), pl.legend(loc=2)
pl.twinx()
pl.plot(f_axys,aa_eta_axys[:,fig2],'r',label='axys')
pl.ylabel('axys - m2/Hz'), pl.legend(loc=1)

pl.subplot(223)
pl.title(data_gx3[fig3].strftime('%Y-%m-%d %H:%M'))
pl.plot(f_gx3,aa_eta_gx3[:,fig3],'b',label='gx3-w4'), pl.axis([0,f_gx3[-1],0,0.02])
pl.ylabel('gx3 - m2/Hz'), pl.legend(loc=2)
pl.twinx()
pl.plot(f_axys,aa_eta_axys[:,fig3],'r',label='axys')
pl.ylabel('axys - m2/Hz'), pl.legend(loc=1)

pl.subplot(224)
pl.title(data_gx3[fig4].strftime('%Y-%m-%d %H:%M'))
pl.plot(f_gx3,aa_eta_gx3[:,fig4],'b',label='gx3-w4'), pl.axis([0,f_gx3[-1],0,0.15])
pl.ylabel('gx3 - m2/Hz'), pl.legend(loc=2)
pl.twinx()
pl.plot(f_axys,aa_eta_axys[:,fig4],'r',label='axys')
pl.ylabel('axys - m2/Hz'), pl.legend(loc=1)



pl.show()
