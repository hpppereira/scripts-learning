'''
Plota rosa dos ventos dos dados
da vale
isabela
'''



import os
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pylab as plt
import windrose
reload(windrose)
from windrose import WindroseAxes

plt.close('all')

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/proc_lioc/Dados/'

adcp = 'ADCP01.txt'

binshs=np.arange(0,4,0.5)
binstp=np.arange(0,22,2)

parse = lambda x: datetime.strptime(x, '%Y') #formato dos arquivos .txt

dd = pd.read_table(pathname + adcp, sep='\s*',header=None, index_col=False, names=['jdate','dia','mes','ano','hora','min','hs','h10','hmax','dp','spr','dm','tp','tm02'])

#cria data com datetime
dd['date'] = [datetime(int(dd.ano[i]),int(dd.mes[i]),int(dd.dia[i]),int(dd.hora[i])) for i in range(len(dd))]

dd = dd.set_index('date')


# windrose
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
ax.bar(dd.dp, dd.hs, normed=True, bins=binshs, opening=.8, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
plt.savefig('out/isa_hsdp.png', dpi=None, edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.01)    

ax = new_axes()
ax.bar(dd.dp, dd.tp, normed=True, bins=binstp, opening=.8, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
plt.savefig('out/isa_tpdp.png', dpi=None, edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.1)

plt.show()