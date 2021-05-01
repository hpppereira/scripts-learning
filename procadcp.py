'''
Processamento dos dados de corrente
da boia Susana (CF2)
ADCP 75 kHz
'''

import pandas as pd
import numpy as np
import pylab as pl
import os
import datetime as datetime

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/Sistemas-BMOP/Processamento/dados/CF02/ADCP/txt/'

dd = np.loadtxt(pathname + 'ADCP_20150510.txt', skiprows=26)
#dd = pd.read_csv(pathname + 'ADCP_20150510.txt', sep='\t', skiprows=26)

datat = [datetime.datetime(int(dd[i,1]+2000), int(dd[i,2]), int(dd[i,3]), int(dd[i,4])) for i in range(len(dd))]

pit = dd[:,8]
rol = dd[:,9]
hea = dd[:,10]
tem = dd[:,11]
dep = dd[:,12]

pl.figure()
pl.plot(datat,pit,'b',datat,rol,'g')
pl.twinx()
pl.plot(datat,hea,'r')

pl.figure()
pl.plot(datat,tem)
pl.title('Temperatura')


pl.show()