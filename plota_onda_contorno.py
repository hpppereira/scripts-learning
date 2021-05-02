''' plota resultados do modelo WW3 para o contorno do sisbahia

'''

import os
import pylab as pl
import numpy as np
from datetime import datetime


import windrose
reload(windrose)
from windrose import WindroseAxes

pl.close('all')
pathname = os.environ['HOME'] + '/Dropbox/ww3vale/hidrodinamico/onda/'

onda = np.loadtxt(pathname + 'tab51.ww3',skiprows=3)

#modelo
data= onda[:,0].astype(str) #ano mes
data_h = onda[:,1].astype(int)
datam = np.array([datetime(int(data[i][0:4]),int(data[i][4:6]),int(data[i][6:8]),int(data_h[i])) for i in range(len(data))])

binshs=np.arange(0.6,1.8,0.2)

# windrose
def new_axes():
    fig = pl.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    pl.setp(l.get_texts(), fontsize=10,weight='bold')
    
  

#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
ax.bar(onda[:,10], onda[:,4], normed=True, bins=binshs, opening=1, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
pl.savefig('windrose', dpi=None, edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.01) 

pl.figure(figsize=(10,8))
pl.subplot(311)
pl.plot(datam,onda[:,4],'ro-')
pl.ylim([0,2])
pl.grid(), pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(datam,1/onda[:,9],'ro')
pl.ylim([0,22])
pl.grid(), pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(datam,onda[:,10],'ro')
pl.ylim([0,360])
pl.grid(), pl.ylabel('Dp (graus)')
pl.show()