#Grafico com periodos de medicoes das boias
#
#dados de entrada: ano, mes, dia, hora
# *matriz de parametros calculados
#

import numpy as np
from datetime import datetime, timedelta
# import datetime
import os
import matplotlib.pylab as pl
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import matplotlib.dates as mdates

###???
# years = YearLocator()   # every year
# months = MonthLocator()  # every month
# yearsFmt = DateFormatter('%Y')


pl.close('all')

#carrega arquivos 'lista'
bc10 = np.loadtxt(os.environ['HOME'] + '/Dropbox/ww3es/Geral/rot/saida/bc10/param_8_bc10.out',delimiter=',')
cac = np.loadtxt(os.environ['HOME'] + '/Dropbox/ww3es/Geral/rot/saida/cacimbas/param_8_cacimbas.out',delimiter=',')
# mer = np.loadtxt(os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/santos/lista-santos.txt',dtype=str)
# ps = np.loadtxt(os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/porto_seguro/lista-porto_seguro.txt',dtype=str)
# re = np.loadtxt(os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/recife/lista-recife.txt',dtype=str)

#datas
dbc10 = np.array([datetime.strptime(str(int(bc10[i,0])), '%Y%m%d%H%M%S') for i in range(len(bc10))])
dcac = np.array([datetime.strptime(str(int(cac[i,0])), '%Y%m%d%H%M%S') for i in range(len(cac))])

#criar vetor de data da boia do merenda (BM02)
start = datetime(2006,10,12,00)
fim = 720
dmer=np.array([start + timedelta(hours=i) for i in xrange(fim)])


#datas
# drg = [datetime(int(rg[i][0:4]),int(rg[i][4:6]),int(rg[i][6:8])) for i in range(len(rg))]
# dfl = [datetime(int(fl[i][0:4]),int(fl[i][4:6]),int(fl[i][6:8])) for i in range(len(fl))]
# dsa = [datetime(int(sa[i][0:4]),int(sa[i][4:6]),int(sa[i][6:8])) for i in range(len(sa))]
# dps = [datetime(int(ps[i][0:4]),int(ps[i][4:6]),int(ps[i][6:8])) for i in range(len(ps))]
# dre = [datetime(int(re[i][0:4]),int(re[i][4:6]),int(re[i][6:8])) for i in range(len(re))]


vbc10 = np.linspace(1,1,len(bc10))
vmer = np.linspace(1.5,1.5,len(dmer))
vcac = np.linspace(2,2,len(cac))
# vps = np.linspace(4,4,len(ps))
# vre = np.linspace(5,5,len(re))

# pl.figure(figsize=(8,5))

fig, ax = pl.subplots(figsize=(10,4)); pl.hold('on')
ax.plot_date(dbc10,vbc10,'k.',markersize=25,label='BM01')
ax.plot(dmer,vmer,'b.',markersize=25,label='BM02')
ax.plot(dcac,vcac,'r.',markersize=25,label='Cacimbas')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))

pl.xticks(rotation=18)
pl.yticks(visible=False)
pl.legend(loc=0)
pl.ylim([0.5,2.5])
pl.grid('on')
pl.hold('off')

# #xlim([731217  734139]); ylim([0 6]); grid();

pl.savefig('fig/periodomedicao.png', dpi=1200, facecolor='w', edgecolor='w',
orientation='portrait',format='png') 

pl.savefig('fig/periodomedicao.eps', dpi=1200, facecolor='w', edgecolor='w',
orientation='portrait',format='eps') 

pl.show()
