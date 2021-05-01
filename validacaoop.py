'''
Validacao Operacional dos resultados da modelagem
de Ondas no Porto de Tubarao (TU) utilizando
os ADCP 04 (fora) e 10 (dentro) operacionais da Vale

- Utiliza os dados que sao baixados de forma
operacional do site da Vale atraves da rotina:
'getadcpvale.py e getadcpvale.sh' que rodam
pelo crontab

- Carrega o arquivo com resultados do modelo
WW3 e SWAN

Autores:
Henrique P. P. Pereira
Izabel C. M. Nogueira

Data da ultima modificao: 03/06/2015

'''

import numpy as np
import os
from datetime import datetime
import pylab as pl
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import matplotlib.dates as mdates

pl.close('all')

#inicio da janela para plotagem (horas)
j = 0

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

#figuras

#Hs, Tp e Dp
pl.figure(figsize=(16,10))
pl.subplot(311)
pl.title('Parametros de Ondas - TU')
pl.plot(dadcp04[j:],adcp04[j:,7],'b.',label='B04')
pl.plot(dadcp10[j:],adcp10[j:,7],'r.',label='B10')
pl.legend(loc=2,fontsize=10)
pl.ylabel('Hs (m)'), pl.grid()
pl.xticks(visible=False)

pl.subplot(312)
pl.plot(dadcp04[j:],adcp04[j:,8],'b.',label='B04')
pl.plot(dadcp10[j:],adcp10[j:,8],'r.',label='B10')
pl.ylabel('Tp (s)'), pl.grid()
pl.xticks(visible=False)

ax = pl.subplot(313)
pl.plot(dadcp04[j:],adcp04[j:,9],'b.',label='B04')
pl.plot(dadcp10[j:],adcp10[j:,9],'r.',label='B10')
pl.ylabel('Dp (graus)'), pl.grid()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y \n %H:%M'))


#rumo, pitch e roll
pl.figure(figsize=(16,10))
pl.subplot(311)
pl.title('Movimentos do ADCP - TU')
pl.plot(dadcp04[j:],adcp04[j:,2],'b.',label='B04')
pl.plot(dadcp10[j:],adcp10[j:,2],'r.',label='B10')
pl.legend(loc=2,fontsize=10)
pl.ylabel('Rumo (graus)'), pl.grid()
pl.xticks(visible=False), pl.ylim(0,360)

pl.subplot(312)
pl.plot(dadcp04[j:],adcp04[j:,5],'b.',label='B04')
pl.plot(dadcp10[j:],adcp10[j:,5],'r.',label='B10')
pl.ylabel('Pitch (graus)'), pl.grid()
pl.xticks(visible=False)

ax = pl.subplot(313)
pl.plot(dadcp04[j:],adcp04[j:,6],'b.',label='B04')
pl.plot(dadcp10[j:],adcp10[j:,6],'r.',label='B10')
pl.ylabel('Roll (graus)'), pl.grid()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y \n %H:%M'))

#rumo, pitch e roll
pl.figure(figsize=(16,10))
pl.subplot(211)
pl.title('Pressao e Temperatura - TU')
pl.plot(dadcp04[j:],adcp04[j:,3],'b',label='B04')
pl.plot(dadcp10[j:],adcp10[j:,3],'r',label='B10')
pl.legend(loc=2,fontsize=10)
pl.ylabel('Pressao (hPa)'), pl.grid()
pl.xticks(visible=False)

ax = pl.subplot(212)
pl.plot(dadcp04[j:],adcp04[j:,4],'b.',label='B04')
pl.plot(dadcp10[j:],adcp10[j:,4],'r.',label='B10')
pl.ylabel('Temperatura (graus)'), pl.grid()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y \n %H:%M'))
pl.ylim(0,30)




pl.show()










