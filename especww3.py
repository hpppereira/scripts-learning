'''
Carrega espectros 2D do modelo
e integra para obter o especro 1D
'''

import numpy as np
import matplotplib.pylab as pl
import os
import pandas as pd

pathname = os.environ['HOME'] + '/Dropbox/ww3seal/rot/out/'

f = np.array([0.0418, 0.0459, 0.0505, 0.0556, 0.0612, 0.0673, 0.0740, 
	0.0814, 0.0895, 0.0985, 0.1080, 0.1190, 0.1310, 0.1440, 0.1590, 0.1740, 0.1920, 
	0.2110, 0.2320, 0.2550, 0.2810, 0.3090, 0.3400, 0.3740, 0.4110])

sp2 = pd.read_table(pathname + 'pspec_1D_200810.txt', comment='%', sep='\s*')

