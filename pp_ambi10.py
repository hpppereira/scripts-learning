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


# pl.close('all')

pathname_gx3 = os.environ['HOME'] + '/Dropbox/ambid/dados/Mexilhao_gx3_triaxys/gx3/'
pathname_axys = os.environ['HOME'] + '/Dropbox/ambid/dados/Mexilhao_gx3_triaxys/axys/HNE/'

# az_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbacelZ.dat',
# 	dtype=str,delimiter=',',skiprows=4)
av_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbaclV.dat',
	dtype=str,delimiter=',',skiprows=4)
aew_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbaclEW.dat',
	dtype=str,delimiter=',',skiprows=4)
ans_gx3 = np.loadtxt(pathname_gx3 + 'TOA5_55915.microstrain_stbaclNS.dat',
	dtype=str,delimiter=',',skiprows=4)

eta_gx3_mat = np.loadtxt('eta_gx3_mat.txt')

#lista dos arquivos da axys
lista_axys = loadhne.lista_hne(pathname_axys)

#arquivo a processar
j = 300

data_gx3_str = av_gx3[j,0] #data em string

#dados de acel. do gx3 em float 

# az_gx3 = az_gx3[0:narq,range(2,az_gx3.shape[1])].astype(float).T
av_gx3 = av_gx3[j,range(2,av_gx3.shape[1])].astype(float).T
aew_gx3 = aew_gx3[j,range(2,aew_gx3.shape[1])].astype(float).T
ans_gx3 = ans_gx3[j,range(2,ans_gx3.shape[1])].astype(float).T

#data com datetime
data_gx3 = datetime.strptime(data_gx3_str, '"%Y-%m-%d %H:%M:%S"') #for i in range(len(data_gx3_str))]

#axys
dados_axys = loadhne.dados_hne(pathname_axys, lista_axys[j])[0]
eta_axys = dados_axys[:,1]
etay_axys = dados_axys[:,2]
etax_axys = dados_axys[:,3]

data_axys_str = lista_axys[j][0:12]

data_axys = datetime.strptime(data_axys_str, '%Y%m%d%H%M%S')

# -- definicao dos parametros de onda -- #

#parametros axys e gx3
fs_gx3 = 1
nfft_gx3 = 64 #256-8gl ; 64-32gl
dt_gx3 = 1./fs_gx3

fs_axys = 1.28
nfft_axys = 86 # 345-8gl ; 86-32gl
dt_axys = 1./fs_axys

# vetor de tempo de amostragem
t_gx3 = np.arange(0,len(av_gx3)*dt_gx3,dt_gx3)
t_axys = np.arange(0,len(eta_axys)*dt_axys,dt_axys)

# -- espectros cruzados -- ##

# espec.espec2
# Dados de entrada: x = serie real 1 (potencia de 2)
#                   y = serie real 2 (potencia de 2)
#                   nfft - Numero de pontos utilizado para o calculo da FFT
#                   fs - frequencia de amostragem
#
#					col 0: vetor de frequencia
#   				col 1: amplitude do espectro cruzado
#                   col 2: co-espectro
#                   col 3: quad-espectro
#                   col 4: espectro de fase
#                   col 5: espectro de coerencia
#                   col 6: intervalo de confianca inferior do espectro cruzado
#                   col 7: intervalo de confianca superior do espectro cruzado
#                   col 8: intervalo de confianca da coerencia

# -  auto-espectros -- #

aa_av_gx3 = espec.espec1(av_gx3,nfft_gx3,fs_gx3)
aa_aew_gx3 = espec.espec1(aew_gx3,nfft_gx3,fs_gx3)
aa_ans_gx3 = espec.espec1(ans_gx3,nfft_gx3,fs_gx3)
aa_eta_axys = espec.espec1(eta_axys,nfft_axys,fs_axys)
aa_etax_axys = espec.espec1(etax_axys,nfft_axys,fs_axys)
aa_etay_axys = espec.espec1(etay_axys,nfft_axys,fs_axys)

# -- espectros cruzados -- #

aa_avaew_gx3 = espec.espec2(av_gx3,ans_gx3,nfft_gx3,fs_gx3)
aa_avans_gx3 = espec.espec2(av_gx3,aew_gx3,nfft_gx3,fs_gx3)
aa_aewans_gx3 = espec.espec2(aew_gx3,ans_gx3,nfft_gx3,fs_gx3)
aa_etaetax_axys = espec.espec2(eta_axys,etax_axys,nfft_axys,fs_axys)
aa_etaetay_axys = espec.espec2(eta_axys,etay_axys,nfft_axys,fs_axys)
aa_etaxetay_axys = espec.espec2(etax_axys,etay_axys,nfft_axys,fs_axys)


#vetor de frequencia
f_gx3 = aa_avaew_gx3[:,0]
f_axys = aa_etaetax_axys[:,0]


# -- figuras -- #

# fig 1 - espec fase acV e acEW
pl.figure()

pl.subplot(211)
pl.title('Auto-Espectros de Aceleracao - GX3')
pl.plot(f_gx3,aa_av_gx3[:,1],'b',label='acV-gx3')
pl.ylabel('acV'), pl.legend(loc=2), pl.grid('on')

pl.twinx()
pl.plot(f_gx3,aa_aew_gx3[:,1],'r',label='acEW-gx3')
pl.plot(f_gx3,aa_ans_gx3[:,1],'g',label='acNS-gx3')
pl.ylabel('acEW / acNS'), pl.legend(loc=1)

pl.subplot(212)
pl.title('Espectro de Fase - acV e acEW')
pl.plot(f_gx3,aa_avaew_gx3[:,4],'b',label='Fase-gx3')
pl.ylabel('graus'), pl.xlabel('freq. (Hz)'), pl.grid('on')

pl.savefig('saida/fase_acVacEW-gx3.png')

# fig 2 - espec fase acV e acNS
pl.figure()

pl.subplot(211)
pl.title('Auto-Espectros de Aceleracao - GX3')
pl.plot(f_gx3,aa_av_gx3[:,1],'b',label='acV-gx3')
pl.ylabel('acV'), pl.legend(loc=2), pl.grid('on')

pl.twinx()
pl.plot(f_gx3,aa_aew_gx3[:,1],'r',label='acEW-gx3')
pl.plot(f_gx3,aa_ans_gx3[:,1],'g',label='acNS-gx3')
pl.ylabel('acEW / acNS'), pl.legend(loc=1)

pl.subplot(212)
pl.title('Espectro de Fase - acV e acNS')
pl.plot(f_gx3,aa_avans_gx3[:,4],'b',label='Fase-gx3')
pl.ylabel('graus'), pl.xlabel('freq. (Hz)'), pl.grid('on')

pl.savefig('saida/fase_acVacNS-gx3.png')

# fig 3 - espec fase acEW e acNS
pl.figure()

pl.subplot(211)
pl.title('Auto-Espectros de Aceleracao - GX3')
pl.plot(f_gx3,aa_av_gx3[:,1],'b',label='acV-gx3')
pl.ylabel('acV'), pl.legend(loc=2), pl.grid('on')

pl.twinx()
pl.plot(f_gx3,aa_aew_gx3[:,1],'r',label='acEW-gx3')
pl.plot(f_gx3,aa_ans_gx3[:,1],'g',label='acNS-gx3')
pl.ylabel('acEW / acNS'), pl.legend(loc=1)

pl.subplot(212)
pl.title('Espectro de Fase - acEW e acNS')
pl.plot(f_gx3,aa_aewans_gx3[:,4],'b',label='Fase-gx3')
pl.ylabel('graus'), pl.xlabel('freq. (Hz)'), pl.grid('on')

pl.savefig('saida/fase_acEWacNS-gx3.png')

# fig 4 - espec fase eta e etax
pl.figure()

pl.subplot(211)
pl.title('Auto-Espectros de Heave e Disp. EW e NS - Axys')
pl.plot(f_axys,aa_eta_axys[:,1],'b',label='heave-axys')
pl.ylabel('heave'), pl.legend(loc=2), pl.grid('on')

pl.twinx()
pl.plot(f_axys,aa_etax_axys[:,1],'r',label='dspEW-axys')
pl.plot(f_axys,aa_etay_axys[:,1],'g',label='etaNS-axys')
pl.ylabel('dspEW / dspNS'), pl.legend(loc=1)

pl.subplot(212)
pl.title('Espectro de Fase - Heave e dspEW')
pl.plot(f_axys,aa_etaetax_axys[:,4],'b',label='Fase-axys')
pl.ylabel('graus'), pl.xlabel('freq. (Hz)'), pl.grid('on')

pl.savefig('saida/fase_etaetax-axys.png')

# fig 5 - espec fase eta e etay
pl.figure()
pl.subplot(211)
pl.title('Auto-Espectros de Heave e Disp. EW e NS - Axys')
pl.plot(f_axys,aa_eta_axys[:,1],'b',label='heave-axys')
pl.ylabel('heave'), pl.legend(loc=2), pl.grid('on')

pl.twinx()
pl.plot(f_axys,aa_etax_axys[:,1],'r',label='dspEW-axys')
pl.plot(f_axys,aa_etay_axys[:,1],'g',label='etaNS-axys')
pl.ylabel('dspEW / dspNS'), pl.legend(loc=1)

pl.subplot(212)
pl.title('Espectro de Fase - Heave e dspNS')
pl.plot(f_axys,aa_etaetay_axys[:,4],'b',label='Fase-axys')
pl.ylabel('graus'), pl.xlabel('freq. (Hz)'), pl.grid('on')

pl.savefig('saida/fase_etaetay-axys.png')

# fig 6 - espec fase etax e etay
pl.figure()

pl.subplot(211)
pl.title('Auto-Espectros de Heave e Disp. EW e NS - Axys')
pl.plot(f_axys,aa_eta_axys[:,1],'b',label='heave-axys')
pl.ylabel('heave'), pl.legend(loc=2), pl.grid('on')

pl.twinx()
pl.plot(f_axys,aa_etax_axys[:,1],'r',label='dspEW-axys')
pl.plot(f_axys,aa_etay_axys[:,1],'g',label='etaNS-axys')
pl.ylabel('dspEW / dspNS'), pl.legend(loc=1)

pl.subplot(212)
pl.title('Espectro de Fase - dspEW e dspNS')
pl.plot(f_axys,aa_etaxetay_axys[:,4],'b',label='Fase-axys')
pl.ylabel('graus'), pl.xlabel('freq. (Hz)'), pl.grid('on')

pl.savefig('saida/fase_etaxetay-axys.png')

#fig 7 - series temporais de aceleracao
pl.figure()

pl.subplot(211)
pl.title('Series Temporais - GX3')
pl.plot(t_gx3[0:78],av_gx3[0:78],label='acV-gx3') #[0:78] para ir o mesmo tempo da axys, pois sao diferentes dt
pl.ylabel('m/s2'), pl.legend(loc=2), pl.grid('on')

pl.twinx()
pl.plot(aew_gx3[0:78],'r',label='acEW-gx3')
pl.plot(ans_gx3[0:78],'g',label='acNS-gx3')
pl.ylabel('m/s2'), pl.legend(loc=1)

pl.subplot(212)
pl.title('Series Temporais - Axys')
pl.plot(t_axys[0:100],eta_axys[0:100],label=('heave-axys'))
pl.ylabel('metros'), pl.legend(loc=2), pl.grid('on')

pl.twinx()
pl.plot(t_axys[0:100],etay_axys[0:100],'r',label='dspNS-axys')
pl.plot(t_axys[0:100],etax_axys[0:100],'g',label='dspEW-axys')
pl.ylabel('metros'), pl.legend(loc=1)
pl.ylabel('metros')
pl.xlabel('Tempo (s)')

pl.savefig('saida/series-gx3_axys.png')

pl.show()