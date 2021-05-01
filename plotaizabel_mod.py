'''
Processamento dos dados das
boias da NavCon, do site:
http://200.220.139.178:8082/Mensagem4DadosOnda.aspx?msg=Izabel
'''

import os
import numpy as np
import datetime as dt
import pylab as pl


pathname = os.environ['HOME'] + '/Dropbox/lioc/instrumentacao/navcon/dados/izabel/'

arq = 'dados_izabel_ondas_20150802.txt' #site

dados = np.loadtxt(pathname + arq,dtype=str,skiprows=0) #site

#cria vetor de data com datetime
data_aux = np.array([dados[i,0] + ' ' + dados[i,1] for i in range(len(dados))])
data = np.array([dt.datetime.strptime(data_aux[i],'%d/%m/%Y %H:%M:%S') for i in range(len(data_aux))])

#dd = hs, tp, dp
dd = dados[:,2:].astype(np.float)


#figuras
pl.figure()
pl.subplot(211)
pl.title('02/08/2015 - 11h - Boia: LIOc 01 (Lat: -23.81 ; Lon: -41.59)')
pl.plot(data,dd[:,0])
pl.xticks(visible=False)
pl.grid()
pl.ylabel('Hs (m)')
pl.subplot(212)
pl.plot(data,dd[:,1])
pl.grid()
pl.ylabel('Tp (s)')
# pl.subplot(313)
# pl.plot(data,dd[:,2])
# pl.grid()
# pl.ylabel('Dp (graus)')

# fig, ax = pl.subplots() #figsize=(10,4)); pl.hold('on')
# ax.plot_date(dbc10,vbc10,'k.',markersize=25,label='BM01')
# ax.plot(dmer,vmer,'b.',markersize=25,label='BM02')
# ax.plot(dcac,vcac,'r.',markersize=25,label='Cacimbas')
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))

pl.show()


