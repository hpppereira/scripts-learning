'''
pleds swan aline e viviane
'''

import os
import pleds
import numpy as np
import importlib
importlib.reload(pleds)

pathname = os.environ['HOME'] + '/Dropbox/metocean/codes/'

filename = 'spec_WW3_side06.out'

espe1, dire1, vfreq, vdire, espe1d, espe1di, espe2d, espe2di, hm0, tp, dp, spc1dm = pleds.preppledsSWAN(pathname, filename)

pleds.pledsSWAN(espe1[:,::3]/20,dire1[:,::3],tit='teste',dia=1)