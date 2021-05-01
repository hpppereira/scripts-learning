import os
import matplotlib
import pandas as pd
import numpy as np
from datetime import datetime
try:
	os.environ["DISPLAY"]
except:
	matplotlib.use('Agg')

pathname = os.environ['HOME'] + '/Dropbox/pnboia/data/realtime/mb/'
anomes = datetime.now().strftime('%y%m')
boias = ['rg', 'sc', 'st', 'bg', 'cf', 'vt', 'ps', 'rc', 'fo']
boias1 = ['PNBOIA_RIG','PNBOIA_FLN','PNBOIA_SAN','PNBOIA_BGA','PNBOIA_CFR','PNBOIA_VIX','PNBOIA_PSG','PNBOIA_RCF','PNBOIA_FTL']
				       
dd = {}

cont = -1
for boia in boias:
	cont += 1

	try:

		for sheet in ['sheet001', 'sheet002']:

			url = 'https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/' + boia + anomes + '_ficheiros/' + sheet + '.htm'

			print url

			aux = pd.read_html(url, thousands='.')[0][5:].astype(str)

			aux = np.array([aux.ix[:,i].apply(lambda x: x.replace(',','.')) for i in aux.columns]).T

			aux[np.where(aux == 'xxx')] = np.nan
			aux[np.where(aux == 'xxxx')] = np.nan
			aux[np.where(aux == 'xxxxx')] = np.nan
			aux[np.where(aux == 'nan')] = np.nan

			if sheet == 'sheet001':

				dd1 = pd.DataFrame(aux[:,:11], columns=['argos_id', 'date', 'position', 'battery', 'flooding', 'ws1', 'wg1', 'wd1', 'ws2', 'wg2', 'wd2'])
				dd1['date'] = pd.to_datetime(dd1.date)
				dd1 = dd1.loc[dd1.date.isnull()==False]
				dd1 = dd1.set_index('date')
				dd1 = dd1.astype(float)
				dd1 = dd1.resample('H').mean()

			elif sheet == 'sheet002':

				dd2 = pd.DataFrame(aux[:,1:11], columns=['date', 'at', 'rh', 'dew_point', 'pr', 'sst', 'hs', 'hmax', 'tp', 'dp'])
				dd2['date'] = pd.to_datetime(dd2.date)
				dd2 = dd2.loc[dd2.date.isnull()==False]
				dd2 = dd2.set_index('date')
				dd2 = dd2.astype(float)
				dd2 = dd2.resample('H').mean()

		new = pd.concat((dd1,dd2),axis=1)

		old = pd.read_csv(pathname + boias1[cont] + '.csv', sep=',', parse_dates=['date'], index_col=['date'])

		#concatena dado antigo com novo
		dd[boia] = pd.concat([old,new])

		#retira dados repetidos (verifica a data)
		u, ind = np.unique(dd[boia].index, return_index=True)
		dd[boia] = dd[boia].ix[ind]

		#inverte os dados
		# dd[boia] = dd[boia][-1:0:-1]

		# dd[boia] = new
		dd[boia].to_csv(pathname + boias1[cont] + '.csv', na_rep='NaN')

	except Exception as e: print (e)