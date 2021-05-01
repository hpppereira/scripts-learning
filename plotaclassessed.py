'''
Cria grafico de classes
'''

import os
import pandas as pd
import pylab as pl

#cenario (media ou predominante)
cenario = 'predominante'
filename1 = 'ucw_mod_latlon_grid_Hsprc10.csv'
filename2 = 'ucw_mod_latlon_grid_Hsprc50.csv'
filename3 = 'ucw_mod_latlon_grid_Hsprc90.csv'

pathname = os.environ['HOME'] + '/Dropbox/ww3seal/rot/out/'

mod1 = pd.read_csv(pathname + cenario + '/' + filename1)
mod2 = pd.read_csv(pathname + cenario + '/' + filename2)
mod3 = pd.read_csv(pathname + cenario + '/' + filename3)

mod = mod1
n = pl.find(mod2.mob == 0)
mod.mob[n] = mod2.mob[n]
