'''
Avaliacao dos dados do ADCP 04
'''

import os
import numpy as np
import pylab as pl

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/rot/out/bruto/series/ast/'


lista = np.sort(os.listdir(pathname))

#find adcp 04
lista = lista[pl.find(lista == 'adcp4_201302010000.out') : pl.find(lista == 'adcp3_201302282300.out')]
