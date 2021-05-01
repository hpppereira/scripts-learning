'''
Compara dados da axys bruto e processado
'''

import pylab as pl
import pandas as pd
import numpy as np
import os
from datetime import datetime
pathname = os.environ['HOME'] + '/Dropbox/ww3seal/'

#carrega tabela do cenpes
parse = lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S')
dfax = pd.read_table(pathname + 'dados/Boia_AxysSEAL.txt',sep='\t', parse_dates=['DATAHORA'], date_parser=parse)

#carrega tabela do processamento do lioc
dfli = pd.read_table(pathname + 'rot/out/Axys_SEAL_16gl.csv',sep=',', parse_dates=['date'])

dfax = dfax.set_index('DATAHORA')
dfli = dfli.set_index('date')

dfax['hs'] = np.round(4.01 * np.sqrt(dfax['VMTA']),2)
dfax['tp'] = np.round(dfax['VTPK1'],1)
dfax['dp'] = np.round(dfax['VPED1'])


#### plotagens ####

pl.figure()
pl.subplot(311)
pl.plot(dfax.index,dfax.hs,'b',dfli.index,dfli.hs,'r')
pl.ylabel('Hm0 (m)')
pl.xlim(dfli.index[0],dfli.index[-1])
pl.subplot(312)
pl.plot(dfax.index,dfax.tp,'ob',dfli.index,dfli.tp,'or')
pl.ylabel('Tp (s)')
pl.xlim(dfli.index[0],dfli.index[-1])
pl.subplot(313)
pl.plot(dfax.index,dfax.dp,'ob',dfli.index,dfli.dp,'or')
pl.ylabel('Dp (graus)')
pl.xlim(dfli.index[0],dfli.index[-1])

pl.show()