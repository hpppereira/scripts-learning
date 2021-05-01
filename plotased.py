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
cenario = 'predominante'
filename_mod = 'mod_latlon_grid_Hsprc90.csv'

pathname = os.environ['HOME'] + '/Dropbox/ww3seal/rot/out/'

mod = pd.read_csv(pathname + cenario + '/' + filename_mod)
sed = pd.read_csv(pathname + cenario + '/' + 'sed_latlon.csv')

#escala do diametro do grao de phi para mm, e depois para cm
#sed['graocm'] = 1 * (2 ** - sed.grao) * 0.1

#velocidade do fundo em cm (metro para cm)
mod['ubot']= mod.ubot * 100

#calculo da velocidade critica do sedimento
rhow = 1.04 #densidade da agua do mar - g/cm3
rhos = 2.65 #densidade do sedimento (sed quartzo) - g/cm3
s = rhow / rhos #relacao densidade da agua e do sedimento - g/cm3
g = 980. #aceleracao da gravidade (cm/s2)


ucw = []
for i in range(len(sed)):
	if sed.grao[i] <= 0.05: #cm
		aux = 0.118 * g * (s - 1) #tem que fazer isso para elevar ao quadrado numero negativo
		#print aux
		ucw.append( (-abs(aux) ** (2.0/3)) * (sed.grao[i]**(1.0/3)) * (mod.tp[i]**(1.0/3)))
	else:
		aux = 1.090 * g * (s - 1)
		#print aux
		ucw.append( (-abs(aux) ** (4.0/7)) * (sed.grao[i]**(3.0/7)) * (mod.tp[i]**(1.0/7)))

mod['ucw'] = ucw

#exportando mobi = 1, nao mobi = 0

diff=mod.ubot+mod.ucw

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



