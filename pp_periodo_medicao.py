#Grafico com periodos de medicoes das boias
#
#dados de entrada: ano, mes, dia, hora
# *matriz de parametros calculados
#

import numpy as np
from datetime import datetime
import os
import matplotlib.pylab as pl

pl.close('all')

#carrega arquivos 'lista'
rg = np.loadtxt(os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/rio_grande/lista-rio_grande.txt',dtype=str)
fl = np.loadtxt(os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/florianopolis/lista-florianopolis.txt',dtype=str)
sa = np.loadtxt(os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/santos/lista-santos.txt',dtype=str)
ps = np.loadtxt(os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/porto_seguro/lista-porto_seguro.txt',dtype=str)
re = np.loadtxt(os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/recife/lista-recife.txt',dtype=str)

#datas
drg = [datetime(int(rg[i][0:4]),int(rg[i][4:6]),int(rg[i][6:8])) for i in range(len(rg))]
dfl = [datetime(int(fl[i][0:4]),int(fl[i][4:6]),int(fl[i][6:8])) for i in range(len(fl))]
dsa = [datetime(int(sa[i][0:4]),int(sa[i][4:6]),int(sa[i][6:8])) for i in range(len(sa))]
dps = [datetime(int(ps[i][0:4]),int(ps[i][4:6]),int(ps[i][6:8])) for i in range(len(ps))]
dre = [datetime(int(re[i][0:4]),int(re[i][4:6]),int(re[i][6:8])) for i in range(len(re))]

vrg = np.linspace(1,1,len(rg))
vfl = np.linspace(2,2,len(fl))
vsa = np.linspace(3,3,len(sa))
vps = np.linspace(4,4,len(ps))
vre = np.linspace(5,5,len(re))

pl.figure(); pl.hold('on')
pl.title('Periodos de medicoes das BMOs')
pl.plot(dre,vre,'y.',markersize=25)
pl.plot(dps,vps,'g.',markersize=25)
pl.plot(dsa,vsa,'c.',markersize=25)
pl.plot(dfl,vfl,'b.',markersize=25)
pl.plot(drg,vrg,'r.',markersize=25)

pl.xticks(rotation=20)
pl.yticks(visible=False)
pl.xlabel('Data')
pl.legend(['Recife','Porto Seguro','Santos','Florianopolis','Rio Grande'],loc=2)
pl.ylim([0,6])
pl.grid('on')
pl.hold('off')

#xlim([731217  734139]); ylim([0 6]); grid();

pl.show()
