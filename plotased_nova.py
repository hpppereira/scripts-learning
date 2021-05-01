'''
plota dados do campo de sedimentos (mobilizacao)

carrega os dados da coleta de sedimentos
- lat, lon, grao

carrega os dados do modelo para os pontos que se
tem coleta
- lat, lon, h, tp, dp
'''

import numpy as np
import matplotlib.pylab as pl
import pandas as pd
import os
import matplotlib as mpl
from matplotlib import pyplot as plt
import scipy.io
from scipy import interpolate
from scipy.interpolate import interp1d
import os
from matplotlib.collections import PolyCollection
from utmToLatLng import utmToLatLng


#cenario (media ou predominante)
cenario = 'mediana'
filename_mod = 'mod_latlon_grid_Hsprc90.csv'

pathname = os.environ['HOME'] + '/Dropbox/ww3seal/rot/out/'

mod = pd.read_csv(pathname + cenario + '/' + filename_mod)
sed = pd.read_csv(pathname + cenario + '/' + 'sed_latlon.csv')

sed['graocm'] = sed.grao
mod['ubot']= mod.ubot*100 # resultado do swan esta em m/s estamos tranformando para cm/s
#calculo da velocidade critica do sedimento
rhow = 1.04 #densidade da agua do mar - g/cm3
rhos = 2.65 #densidade do sedimento (sed quartzo) - g/cm3
s = rhos / rhow # s = rho do sed/rho da agua
g = 980. #aceleracao da gravidade (cm/s2)


ucw = []
for i in range(len(sed)):
	if sed.graocm[i] <= 0.05: #cm
		ucw.append( ((0.118 * g * (s - 1)) ** (2.0/3)) * (sed.graocm[i]**(1.0/3)) * (mod.tp[i]**(1.0/3)))
	else:
		ucw.append( ((1.090 * g * (s - 1)) ** (4.0/7)) * (sed.graocm[i]**(3.0/7)) * (mod.tp[i]**(1.0/7)))

mod['ucw'] = ucw

#exportando mobi = 1, nao mobi = 0

diff=mod.ubot-mod.ucw

mod['mob']=0

n=pl.find(diff >= 0)

mod['mob'][n] = 1

mod.to_csv('out/' + cenario + '/' + 'ucw_' + filename_mod[:-4] + '.csv')

sed.to_csv('out/' + cenario + '/' + 'sed_' + filename_mod[:-4] + '.csv')

'''
#calculo da mobilizacao de sedimento
loni = np.arange(min(mod.lon), max(mod.lon), 0.00025)
lati = np.arange(min(mod.lat), max(mod.lat), 0.00025)

print 'Iniciando o meshgrid...'
[lons,lats] = np.meshgrid(loni,lati,sparse=False,copy=False)

print 'Iniciando o griddata de do limite de velocidade...'
ms = mpl.mlab.griddata(mod.lon,mod.lat,ms,lons,lats,interp='linear'); #a interp linear e a nn ficaram praticamente iguais
'''



