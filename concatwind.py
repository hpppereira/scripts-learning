'''
Concatena dados de vento do CFSR
ww3seal

Henrique Pereira
Izabel Nogueira

26/10/2015
'''

import pandas as pd
import os
import numpy as np
import matplotlib.pylab as pl
from datetime import datetime
from matplotlib import pyplot as plt
import windrose
from windrose import WindroseAxes


pathname = os.environ['HOME'] + '/Dropbox/ww3seal/modelagem/hindcast/spc/dados/'

#lista os arquivos de vento
lista = np.sort(os.listdir(pathname))
listaw = []
b = []

for i in lista:
	if i.startswith('wind'):
		
		listaw.append(i)
		
		a = pd.read_table(pathname + listaw[-1], sep='\s*', comment='%', names=['ano','mes','dia','hora','minu','ws','wd'])
		
		a.index = np.array([datetime(int(a.ano[i]),int(a.mes[i]),int(a.dia[i]),int(a.hora[i])) for i in range(len(a))])
		
		b.append(a)

#dados concatenados
dd = pd.concat(b)

pl.figure()
pl.plot(dd.index,dd.ws,'-b')
pl.twinx()
pl.plot(dd.index,dd.wd,'r.')

dd.ix[:,['ws','wd']].to_csv('out/geral_wind.csv', index_label='date')


#conjunta hm0 dp - axys

def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=10,weight='bold')
    

#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
ax.bar(dd.wd,dd.ws, normed=True, bins=7, opening=0.8, edgecolor='white',nsector=16)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
#plt.savefig('hsdp_axys.png', dpi=None, facecolor='w', edgecolor='w',
#orientation='portrait', papertype=None, format='png',
#transparent=False, bbox_inches=None, pad_inches=0.1)    





pl.show()






