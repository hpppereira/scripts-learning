'''
Concatena resultados do modelo WW3

pathname = os.environ['HOME'] + '/Dropbox/pnboia/modelagem/resultados/'

'''

import numpy as np
import pandas as pd
import os
from datetime import datetime


def ww3(pathname, filename):


	#concatena resultados da modelagem

	direm = np.sort(os.listdir(pathname))

	mod = np.array([[0,0,0,0,0,0,0,0,0]])

	for dire in direm:

		mod1 = np.loadtxt(pathname + '/' + dire + '/' + filename)
		mod = np.concatenate((mod,mod1),axis=0)

	#retira a primeira linha que foi utilizada para concatenar (zeros)
	mod = mod[1:,:]

	#data do modelo
	dmod = np.array([datetime(int(mod[i,0]),int(mod[i,1]),int(mod[i,2]),int(mod[i,3])) for i in range(len(mod))])
	
	#cria data frame com os resultados concatenados do modelo
	mod = pd.DataFrame({'date': dmod, 'hm0': mod[:,5], 'tp': mod[:,6], 'dp': mod[:,7]})
	mod = mod.set_index('date')

	return mod


