'''
Plota resultados da grade nao estruturada em comparacao aos dados do ADCP

LIOc - Laboratorio de Instrumentacao Oceanografica

Data da ultima modificacao: 30/11/2015
'''

import numpy as np
from datetime import datetime, timedelta
import pylab as pl
import os
import xlrd

#Saida SWAN
# 0   1   2    3   4   5  6  7   8
#tempo,hs,dp,tp,xwind,ywind,hsswell,sprd

# plotar para o adcp 01
#diretorio de onde estao os resultados
pathname  = os.environ['HOME'] + '/Dropbox/ww3vale/SWAN_NAOESTRUTURADO_paralelo/Rodada_paralelo/Resultados/201505/'

mdd= np.loadtxt(pathname + 'table_point_adcp10.out',skiprows=7,usecols=(0,1,3,2))

#diretorio de onde estao os resultados
pathname2  = '/media/lioc/Parente/SWAN/BES_65X45/output/201505/'

mdd2= np.loadtxt(pathname2 + 'table_point_ADCP10.out',skiprows=7,usecols=(0,1,3,2))

data_mod=mdd[:,0]*100
data_mod = data_mod.astype(str) #ano mes dia hora
datam = np.array([datetime(int(data_mod[i][0:4]),int(data_mod[i][4:6]),int(data_mod[i][6:8]),int(data_mod[i][8:10])) for i in range(len(data_mod))])
datam = datam - timedelta(hours=3)

data_mod2=mdd2[:,0]*100
data_mod2 = data_mod2.astype(str) #ano mes dia hora
datam2 = np.array([datetime(int(data_mod2[i][0:4]),int(data_mod2[i][4:6]),int(data_mod2[i][6:8]),int(data_mod2[i][8:10])) for i in range(len(data_mod2))])
datam2 = datam2- timedelta(hours=3)

# DADOS ADCP
pathname_adcp = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/operacional/' #dados

#nome dos arquivos
#adcp - boia 4 e 10
adcp04 = 'TU_boia04.out' #fora do porto (mais fundo)
adcp10 = 'TU_boia10.out' #dentro do porto

#carrega dados
# 0      1      2     3         4        5    6   7   8 9
#data,bateria,rumo,pressao,temperatura,pitch,roll,hs,tp,dp
adcp04 = np.loadtxt(pathname_adcp + adcp04,delimiter=',')
adcp10 = np.loadtxt(pathname_adcp + adcp10,delimiter=',')

dadcp04 = [ datetime.strptime(str(int(adcp04[i,0])), '%Y%m%d%H%M') for i in range(len(adcp04)) ]
dadcp10 = [ datetime.strptime(str(int(adcp10[i,0])), '%Y%m%d%H%M') for i in range(len(adcp10)) ]


pl.close('all')
pl.figure()
pl.subplot(311)
pl.plot(dadcp10,adcp10[:,7],'ro',label='ADCP10')
pl.plot(datam,mdd[:,1],'bo',label='SWAN')
pl.plot(datam2,mdd2[:,1],'ko',label='SWAN2')
pl.legend(loc=0,fontsize=10)
pl.ylabel('Hs (m)'), pl.grid()
pl.ylim([0,4])

pl.subplot(312)
pl.plot(dadcp10,adcp10[:,8],'or',label='ADCP10')
pl.plot(datam,mdd[:,2],'+b',label='SWAN')
pl.plot(datam2,mdd2[:,2],'ko',label='SWAN2')
pl.ylabel('Tp (s)'), pl.grid()
pl.legend(loc=0,fontsize=10)

pl.subplot(313)
pl.plot(dadcp10,adcp10[:,9]-23,'or',label='ADCP10')
pl.plot(datam,mdd[:,3],'+b',label='SWAN')
pl.plot(datam2,mdd2[:,3],'ko',label='SWAN2')
pl.ylabel('Dp (graus)'), pl.grid()
pl.legend(loc=0,fontsize=10)
pl.show()


