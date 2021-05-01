'''
Wave processing for Triaxys buoy from PNBOIA

use class WaveProc
'''

import os
import numpy as np
import pandas as pd
import waveproc
from matplotlib import reload
from waveproc import WaveProc
reload(waveproc)

#'rio_grande' 'florianopolis' 'santos'
#buoy =  'florianopolis'
savename = 'rcf_8_lioc.csv'

pathname = os.environ['HOME'] + '/Dropbox/database/historical/buoys/pnboia/rcf/hne_rcf/'
pathnamesave = 'out/'

w = WaveProc(pathname)

w.listdir()

#ini = np.where(w.filelist == '201202010000.HNE')[0][0]
#fim = np.where(w.filelist == '201206302300.HNE')[0][0]

ini = 0
fim = len(w.filelist)

d = []
for file in w.filelist[ini:fim]:

    w.read_HNE(filename = file,
     		   fs       = 1.28,
     		   nfft     = 328,
     		   h        = 200)

    if len(w.n1) > 1000 and np.sort(w.n1)[-100:].mean() > 0.5:

        print (w.date)

        #w.wavenumber()
    
        w.timedomain()
    
        w.freqdomain()

        d.append({'date'   : w.date,
        		  'hs'     : w.hs,
        		  'h10'    : w.h10,
        		  'hmax'   : w.hmax,
        		  'tmed'   : w.tmed,
        		  'thmax'  : w.thmax,
        		  'hm0'    : w.hm0,
        		  'tp'     : w.tp,
        		  'dp'     : w.dp,
                  'tzamax' : w.tzamax
        		})

    else:

    	print ('%s -- Reprovado' %w.date)


df = pd.DataFrame(d)
df = df.set_index('date')

df.to_csv(pathnamesave + savename)