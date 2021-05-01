'''
Processamento dos dados do cartao de memoria
do ADCP da BMOBR03 - CF01

Nome do arquivo: DPL3_034.txt

Pings/Ens = 120
Time/Ping = 00:05.00
First Ensemble Date = 15/08/29
First Ensemble Time = 20:07:17.17
Ensemble Interval (s) = 3600
1st Bin Range (m) = 39.73
Bin Size (m) = 32

Data da ultima modificacao: 2016/02/11

Henrique P P Pereira
'''

import os
import pandas as pd
import datetime
import numpy as np
import matplotlib.pylab as pl

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/Sistemas-BMOP/Dados/BMOBR03/cartao/ADCP/txt/'

dd = pd.read_table(pathname + 'DPL3_034.txt',skiprows=15,names=['Ens','YR','MO','DA','HH','MM','SS','NAN','NAN','Pit','Rol','Hea','Tem','Dep','Ori','BIT','Bat',
																'Eas1','Eas2','Eas3','Eas4','Eas5','Eas6','Eas7','Eas8','Eas9','Eas10',
																'Nor1','Nor2','Nor3','Nor4','Nor5','Nor6','Nor7','Nor8','Nor9','Nor10',
																'Ver1','Ver2','Ver3','Ver4','Ver5','Ver6','Ver7','Ver8','Ver9','Ver10',
																'Err1','Err2','Err3','Err4','Err5','Err6','Err7','Err8','Err9','Err10',
																'Mag1','Mag2','Mag3','Mag4','Mag5','Mag6','Mag7','Mag8','Mag9','Mag10',
																'Dir1','Dir2','Dir3','Dir4','Dir5','Dir6','Dir7','Dir8','Dir9','Dir10'])

#remove colunas com nan
dd = dd.drop(['NAN'],axis=1)

#soma 2000 no vetor de ano
dd.YR = dd.YR + 2000

#cria vetor de data
dd['date'] = [datetime.datetime(int(dd.YR[i]),int(dd.MO[i]),int(dd.DA[i]),int(dd.HH[i])) for i in range(len(dd))]

#deixa data como indice
dd = dd.set_index('date')

#vetor de profundidades
prof = np.flipud(np.arange(-45,-45-32*10,-32))

#cria matriz de velocidade e direcao (para grafico de contorno)
mag = np.flipud(np.array(dd[['Mag1','Mag2','Mag3','Mag4','Mag5','Mag6','Mag7','Mag8','Mag9','Mag10']].T)) / 1000.0
dire = np.flipud(np.array(dd[['Dir1','Dir2','Dir3','Dir4','Dir5','Dir6','Dir7','Dir8','Dir9','Dir10']].T))
u = np.flipud(np.array(dd[['Eas1','Eas2','Eas3','Eas4','Eas5','Eas6','Eas7','Eas8','Eas9','Eas10']].T)) / 1000.0
v = np.flipud(np.array(dd[['Nor1','Nor2','Nor3','Nor4','Nor5','Nor6','Nor7','Nor8','Nor9','Nor10']].T)) / 1000.0


fig = pl.figure(figsize=(14,9),facecolor='w')
ax = fig.add_subplot(111)
con = ax.contourf(mag,np.arange(0,1,0.001),color='k')
pl.colorbar(con,label=r'ms$^{-1}$')
qwind = ax.quiver(u, v, units='xy', scale=0.05, headwidth=0, pivot='tail', width=0.25, linewidths=(0.001,), edgecolors='k', color='k', alpha=1)
pl.xticks(range(0,len(dd),50),dd[0:-1:50].index,rotation=5)
pl.yticks(range(0,10),prof)
pl.ylabel('Depth (m)')
pl.axis('tight')
pl.ylim(-1,10)
pl.quiverkey(qwind,230,9.3,1,r'1 ms$^{-1}$',coordinates='data')


fig = pl.figure(figsize=(14,9),facecolor='w')
ax1 = fig.add_subplot(211)
con1 = ax1.contourf(dd.index,prof,mag,np.arange(0,1,0.001))
pl.colorbar(con1)
pl.xticks(rotation=10)
ax2 = fig.add_subplot(212)
con2 = ax2.contourf(dd.index,prof,dire,np.arange(0,360,1))
pl.xticks(rotation=10)
pl.colorbar(con2)


pl.show()