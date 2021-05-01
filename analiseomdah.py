'''
Processamentos dos parametros de ondas
processados pelo lioc da navcon

- compara com os dados do siodoc

'''

import pandas as pd
import os
import matplotlib.pylab as pl
from datetime import datetime
import numpy as np

pathname = os.environ['HOME'] + '/Dropbox/bmo/rot/out/'
pathname_siodoc = os.environ['HOME'] + '/Dropbox/siodoc/dados/proc/20151123/'

iz = pd.read_csv(pathname + 'omdah_waveparam_comb02_16gl.csv', parse_dates=['date'], index_col=['date'])
#dia, mes, ano, hora, hm0, hmax, tp, dp
si = pd.read_table(pathname_siodoc + 'janis_data.dat', sep='\s*',usecols=(0,1,2,3,27,30,38,57),names=['dia','mes','ano','hora','hm0','hmax','dp','tp'])

#retira valores que estao com ano menor que 2000
si = si.loc[si.ano > 2000]

#coloca os indices (pois ficaram desordenados no loc)
si = si.set_index(np.arange(len(si)))

#data com datetime
si['date'] = [datetime(int(si.ano[i]),int(si.mes[i]),int(si.dia[i]),int(si.hora[i])) for i in range(len(si))]

#data do siodoc como indice
si = si.set_index('date')



pl.figure()
pl.subplot(311)
pl.plot(si.index,si.hm0,'b',iz.index,iz.hm0,'r')
pl.xlim(iz.index[0],iz.index[-1])
pl.legend(['SIODOC','Izabel'])
pl.ylabel('Hm0 (m)')
pl.grid()
pl.subplot(312)
pl.plot(si.index,si.tp,'.b',iz.index,iz.tp,'.r')
pl.xlim(iz.index[0],iz.index[-1])
pl.ylim(0,25)
pl.ylabel('Tp (s)')
pl.grid()
pl.subplot(313)
pl.plot(si.index,si.dp-23,'.b',iz.index,iz.dp-90-23,'.r')
pl.xlim(iz.index[0],iz.index[-1])
pl.ylabel('Dp (graus)')
pl.yticks(range(0,360+45,45))
pl.ylim(0,360)
pl.grid()


pl.show()