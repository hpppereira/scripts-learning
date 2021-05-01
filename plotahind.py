'''
Plota hindcast
'''

import matplotlib.pylab as pl
import numpy as np
import pandas as pd
import os
from datetime import datetime

pathname = os.environ['HOME'] + '/Dropbox/ww3seal/modelagem/analise/geral/'

dd = pd.read_table(pathname + 'geral.txt', sep='\s*', names=['year','month','day','hour','minu','hs','tp','dp','spr'])

dd.index = np.array([datetime(int(dd.year[i]),int(dd.month[i]),int(dd.day[i]),int(dd.hour[i])) for i in range(len(dd))])


pl.figure()
pl.subplot(311)
pl.plot(dd.index,dd.hs)
pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(dd.index,dd.tp,'.')
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(dd.index,dd.dp,'.')
pl.ylabel('Dp (graus)')

pl.show()