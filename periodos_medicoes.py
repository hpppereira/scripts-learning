#Grafico com periodos de medicoes das boias
#
#dados de entrada: ano, mes, dia, hora
# *matriz de parametros calculados
#

import numpy as np
import datetime
import os
import matplotlib.pylab as pl

pl.close('all')

#carrega arquivos

#MINUANO - RS
d1 = np.loadtxt(os.environ['HOME'] + '/Dropbox/tese/cq/dados/minuano/saida_minuano.txt',skiprows=1);
#AXYS - RS
d2 = np.loadtxt(os.environ['HOME'] + '/Dropbox/tese/cq/dados/axys/rs/param_ondas_rs.txt',skiprows=1);
#AXYS - SC

#AXYS - SP

#AXYS - PE


#g1 = [datetime.datetime.toordinal(datetime.date(int(d1[i,0]),int(d1[i,1]),int(d1[i,2]))) for i in range(len(d1))]
g1 = [datetime.datetime(int(d1[i,0]),int(d1[i,1]),int(d1[i,2])) for i in range(len(d1))]
g2 = [datetime.datetime(int(d2[i,0]),int(d2[i,1]),int(d2[i,2])) for i in range(len(d2))]

v1 = np.linspace(1,1,len(g1))
v2 = np.linspace(2,2,len(g2))

pl.figure(); pl.hold('on')
pl.plot(g1,v1,'r',linewidth=5)
pl.plot(g2,v2,'b',linewidth=5)

pl.xticks(rotation=20)
pl.xlabel('Data'); pl.ylabel('Boias'); pl.title('Duracao dos dados de ondas das boias')
pl.legend(['MINUANO-RS','AXYS-RS'])
pl.ylim([0,6])
pl.grid('on')

#xlim([731217  734139]); ylim([0 6]); grid();

pl.show()
