'''
Wave processing for Triaxys buoy from PNBOIA

use class WaveProc
'''

import os
import numpy as np
import pandas as pd
import waveproc
reload(waveproc)
from waveproc import WaveProc

#'rio_grande' 'florianopolis' 'santos'
buoy =  'florianopolis'
savename = 'FLN_8.csv'

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/bruto/triaxys/pre_proc/' + buoy + '/hne/'
pathnamesave = os.environ['HOME'] + '/Dropbox/pnboia/dados/proc/'

w = WaveProc(pathname)

w.listdir()

ini = np.where(w.filelist == '201202010000.HNE')[0][0]
fim = np.where(w.filelist == '201206302300.HNE')[0][0]

d = []
for file in w.filelist[ini:fim]:

    w.read_HNE(filename = file,
     		   fs       = 1.28,
     		   nfft     = 328,
     		   h        = 200)

    if len(w.n1) > 1000 and np.sort(w.n1)[-100:].mean() > 0.5:

    	print w.date

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

    	print '%s -- Reprovado' %w.date


df = pd.DataFrame(d)
df = df.set_index('date')

df.to_csv(pathnamesave + savename)