'''
Plota previsao para cada configuracao e cada dia de previsao

Data da ultima modificacao: 28/08/2015

'''

import numpy as np
import pylab as pl
import os
import taylor
import pandas as pd
import datetime as dt
import matplotlib.dates as dates
from matplotlib.dates import DayLocator, DateFormatter


pl.close('all')

pathname_ww3 = os.environ['HOME'] + '/Dropbox/ww3vale/TU/Previsao/Previsao_14maio/'
pathname_pnboia = os.environ['HOME'] + '/Dropbox/pnboia/dados/LIOc/'

#carrega dados do PNBOIA
df_sa = pd.read_csv(pathname_pnboia + 'B69150_onda.csv',parse_dates=['date'])
df_fl = pd.read_csv(pathname_pnboia + 'B69152_onda.csv',parse_dates=['date'])
df_rg = pd.read_csv(pathname_pnboia + 'B69153_onda.csv',parse_dates=['date'])

# df_sa = df_sa.set_index('date')
# df_fl = df_fl.set_index('date')
# df_rg = df_rg.set_index('date')

#confs = ['ww3v314gfs05', 'ww3v418st4gfs05', 'ww3v418st4mgfs25', 'ww3v418st6gfs25']
confs = ['ww3v314st2gfs05', 'ww3v418st4gfs05', 'ww3v418st4mgfs25', 'ww3v418st6gfs25',]

#dprev = '20150508'

dias = ['20150508', '20150509', '20150510', '20150511', '20150512', '20150513', '20150514']
dias = ['20150511']
cor = ['k-','k--', 'k.-', 'k.'] #cores para plotagem

lsf = 18 #fontsize para as figuras

# data limite
dateend = dt.datetime(2015,5,19)
dstart = dt.datetime(2015,5,10)
 

data_rg=[df_rg['date'][i].to_pydatetime() for i in range(len(df_rg['date'])) ]
data_fl=[df_fl['date'][i].to_pydatetime() for i in range(len(df_fl['date'])) ]
data_sa=[df_sa['date'][i].to_pydatetime() for i in range(len(df_sa['date'])) ]

#plotagem dos dados da boia
fig=pl.figure(figsize=(16,6))


#####################################################################################

for dprev in dias:

	c = -1
	for conf in confs:

		#varia cores para cada configuracao
		c += 1

		#carrega dados do ww3
		dd_wsa = np.loadtxt(pathname_ww3 + conf + '/' + dprev + '/Boiasantos.txt')
		dd_wfl = np.loadtxt(pathname_ww3 + conf + '/' + dprev + '/BoiaFl.txt')
		dd_wrg = np.loadtxt(pathname_ww3 + conf + '/' + dprev + '/BoiaRS.txt')

		#cria data em datetime com swan
		dtt = np.array([dt.datetime(int(dd_wsa[i,0]),int(dd_wsa[i,1]),int(dd_wsa[i,2]),
			int(dd_wsa[i,3])) for i in range(len(dd_wsa))])

		#cria um dicionario
		dsa = {'date' : dtt,
			   'hs'   : dd_wsa[:,5],
		 	   'tp'   : dd_wsa[:,6],
		 	   'dp'   : dd_wsa[:,7]}

		dfl = {'date' : dtt,
			   'hs'   : dd_wfl[:,5],
		 	   'tp'   : dd_wfl[:,6],
		 	   'dp'   : dd_wfl[:,7]}

		drg = {'date' : dtt,
			   'hs'   : dd_wrg[:,5],
		 	   'tp'   : dd_wrg[:,6],
		 	   'dp'   : dd_wrg[:,7]}

		#cria dataframe com os dados do ww3
		df_wsa = pd.DataFrame(dsa)
		df_wfl = pd.DataFrame(dfl)
		df_wrg = pd.DataFrame(drg)


		# df_wfl['date'] = df_wrg.date.astype('datetime64[ns]')
		data_wrg=[df_wrg['date'][i].to_pydatetime() for i in range(len(df_wrg['date'])) ]
		data_wfl=[df_wfl['date'][i].to_pydatetime() for i in range(len(df_wfl['date'])) ]
		data_wsa=[df_wsa['date'][i].to_pydatetime() for i in range(len(df_wsa['date'])) ]


		ax=pl.subplot(1,3,1)
		#ax = pl.figure(figsize=(14,10), dpi=300).add_subplot(111)
		pl.title('Rio Grande/RS')
		pl.plot(data_wrg,df_wrg['hs'],cor[c],linewidth=2)
		pl.plot(data_rg,df_rg['hs'],'k+')
		pl.ylabel('Hs (m)'), pl.ylim(0,7)
		pl.xlim(dstart, dateend)
		ax.xaxis.set_major_locator(DayLocator(interval=2))
		ax.xaxis.set_major_formatter(DateFormatter('%b %d')), pl.grid()

		#ax.xaxis.set_minor_formatter(dates.DateFormatter('%d\n%a'))

		ax=pl.subplot(1,3,2)
		pl.title('Florianopolis/SC')
		pl.plot(data_wfl,df_wfl['hs'],cor[c],linewidth=2)
		pl.plot(data_fl,df_fl['hs'],'k+')
		pl.ylabel('Hs (m)'), pl.ylim(0,7)
		pl.xlim(dstart, dateend)
		ax.xaxis.set_major_locator(DayLocator(interval=2))
		ax.xaxis_date() 
		ax.xaxis.set_major_formatter(DateFormatter('%b %d')), pl.grid()


		ax=pl.subplot(1,3,3)
		pl.title('Santos/SP')
		pl.plot(data_wsa,df_wsa['hs'],cor[c],linewidth=2)
		pl.plot(data_sa,df_sa['hs'],'k+'),
		pl.ylabel('Hs (m)'), pl.ylim(0,7)
		pl.xlim(dstart, dateend)
		ax.xaxis.set_major_locator(DayLocator(interval=2))
		ax.xaxis.set_major_formatter(DateFormatter('%b %d')), pl.grid()


	ax=pl.subplot(1,3,1)
	pl.grid()
	ax=pl.subplot(1,3,2)
	pl.grid()
	ax=pl.subplot(1,3,3)
	pl.grid()

	pl.savefig('fig/' + dprev + '.png')

	pl.show()
