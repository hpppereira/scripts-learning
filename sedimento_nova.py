'''
Pegar no modelo os resultados de onda
nos pontos onde se tem dados de sedimento
'''

import os
import numpy as np
import matplotlib.pylab as pl
import pandas as pd
from utmToLatLng import *
from scipy import spatial


pl.close('all')

cenario = 'mediana'
filename_mod = 'grid_Hsprc90'

pathname_mod = os.environ['HOME'] + '/Dropbox/ww3seal/modelagem/ressuspensao/SWAN/' + cenario + '/'
pathname_sed = os.environ['HOME'] + '/Dropbox/ww3seal/dados/batimetria/'

#carrega dados da modelagem e dos dados de sedimento
mod = pd.read_table(pathname_mod + filename_mod +'.out', sep='\s*',comment='%',header=None, usecols=(0,1,2,3,4,5,10), names=['lon','lat','h','hs','dp','tp','ubot'])
sed = pd.read_csv(pathname_sed + 'granulometria_nova.csv') # D50 esta em mm

#retira os dados que nao tem valor
sed = sed.loc[sed.D50.isnull() == False]

#cria variavel com tamanho do grao
sed['grao'] = sed.D50

#converte utm para latlon
a = [utmToLatLng(24,mod.lon[i],mod.lat[i],northernHemisphere=False) for i in range(len(mod))]
mod['latg'] = np.array(a)[:,0]
mod['long'] = np.array(a)[:,1]

sed['latg'] = sed.LAT
sed['long'] = sed.LONG

# escala do diametro do grao (D50) de mm para cm
sed.grao = sed.grao * 0.1

#monta array com latlon do modelo
A = np.array([mod.latg,mod.long]).T

ind = []
dd_sed = []
dd_mod = []

#acha os valores mais proximos
for i in range(len(sed)):
	print str(i) + ' - ' + str(len(sed))
	pt = np.array([sed.latg[i],sed.long[i]])
	#aux.append(A[spatial.KDTree(A).query(pt)[1]]) # <-- the nearest point 
	distance,index = spatial.KDTree(A).query(pt)
	if distance < 0.003:
		ind.append(index)
		dd_sed.append(list(sed.ix[i,['latg','long','grao']]))
		dd_mod.append(list(mod.ix[index,['latg','long','h','hs','tp','dp','ubot']]))
		print 'Distancia menor que 3 km'
	print distance, index


#dataframe do modelo e sedimento apenas com posicoes coincidentes e na mesma ordem de latlon
dfm = pd.DataFrame(np.array(dd_mod), columns=[['lat','lon','h','hs','tp','dp','ubot']])
dfs = pd.DataFrame(np.array(dd_sed), columns=[['lat','lon','grao']])

#salva dataframes com as mesmas lat e lon
dfm.to_csv('out/' + cenario + '/mod_latlon_' + filename_mod + '.csv')
dfs.to_csv('out/' + cenario + '/sed_latlon.csv')


pl.figure()
pl.plot(mod.long[ind],mod.latg[ind],'bo')
pl.plot(sed.long,sed.latg,'r.')

pl.figure()
pl.plot(dfm.lon,dfm.lat,'o')
pl.plot(dfs.lon,dfs.lat,'r.')

pl.show()
