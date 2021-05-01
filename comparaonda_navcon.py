'''
Comparacao dos dados da BMOP 03 (Izabel)
enviados pelo site e software da NavCon

** Parece que a direcao das ondas enviados
pelo software esta errada (direcoes de 290 graus)
'''

import os
import numpy as np
from datetime import datetime
import pylab as pl

pl.close('all')

#pathname
pathname = os.environ['HOME'] + '/Dropbox/navcon/dados/'

#BMOP 03 - Izabel
soft = 'Mensagens_01025968SKYF4AD.csv' #software
# site = 'dados_site_izabel_ondas.txt' #site

# b4 = 'Mensagens_01055388SKYE349.csv'

b3so = np.loadtxt(pathname + soft,dtype=str,skiprows=0,delimiter=',') #software
# b3si = np.loadtxt(pathname + site,dtype=str,skiprows=1) #site

# b3si = np.flipud(b3si) #inverte os dados do site
head_so = b3so[0,:] #cabecalho
b3so = b3so[1:,:] #retira o cabecalho da primeira linha

dataso = np.array([datetime.strptime(b3so[i,4],'%d/%m/%Y %H:%M:%S') for i in range(len(b3so))])

#cria vetor de data e hora dos dados do site
# datasi_aux = np.array([b3si[i,0] + ' ' +b3si[i,1] for i in range(len(b3si))])
# datasi = np.array([datetime.strptime(datasi_aux[i],'%d/%m/%Y %H:%M:%S') for i in range(len(b3si))])

#parametros do software
hs_so = b3so[:,22].astype(float)
tp_so = b3so[:,23].astype(float)
dp_so = b3so[:,24].astype(float)

#parametros do site
# hs_si = b3si[:,2].astype(float)
# tp_si = b3si[:,3].astype(float)
# dp_si = b3si[:,4].astype(float)

#correcao da direcao
#subtrai 180 dos dados do software
dp_so = dp_so - 180

#caso seja menor que zero, soma 360
dp_so[np.where(dp_so<0)[0]] = dp_so[np.where(dp_so<0)[0]] + 360


#janela para plotagem
jan = range(-48-24,0)

pl.figure()
pl.subplot(311)
pl.plot(dataso[jan],hs_so[jan],'bo',label='soft')
# pl.plot(datasi[jan],hs_si[jan],'r*',label='site')
pl.subplot(312)
pl.plot(dataso[jan],tp_so[jan],'bo')
# pl.plot(datasi[jan],tp_si[jan],'r*')
pl.subplot(313)
pl.plot(dataso[jan],dp_so[jan],'bo')
# pl.plot(datasi[jan],dp_si[jan],'r*')
pl.show()

pl.show()
