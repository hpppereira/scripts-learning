'''
Processamento dos dados de vento do
hindcast
'''

import os
import pandas as pd
import espec
import matplotlib.pylab as pl
import numpy as np

pl.close('all')


pathname = os.environ['HOME'] + '/Dropbox/ww3seal/rot/out/'

dd = pd.read_csv(pathname + 'geral_wind.csv', parse_dates=['date'], index_col='date')

#separa meses (jan a dez)

for val in range(11):

	val = 10 #condicao para valores de hs
	df01 = dd.loc[(dd.index.month == 1) & (dd.ws > val)]
	df02 = dd.loc[(dd.index.month == 2) & (dd.ws > val)]
	df03 = dd.loc[(dd.index.month == 3) & (dd.ws > val)]
	df04 = dd.loc[(dd.index.month == 4) & (dd.ws > val)]
	df05 = dd.loc[(dd.index.month == 5) & (dd.ws > val)]
	df06 = dd.loc[(dd.index.month == 6) & (dd.ws > val)]
	df07 = dd.loc[(dd.index.month == 7) & (dd.ws > val)]
	df08 = dd.loc[(dd.index.month == 8) & (dd.ws > val)]
	df09 = dd.loc[(dd.index.month == 9) & (dd.ws > val)]
	df10 = dd.loc[(dd.index.month == 10) & (dd.ws > val)]
	df11 = dd.loc[(dd.index.month == 11) & (dd.ws > val)]
	df12 = dd.loc[(dd.index.month == 12) & (dd.ws > val)]

	pl.figure()
	pl.hist([df01.ws,df02.ws,df03.ws,df04.ws,df05.ws,
		df06.ws,df07.ws,df08.ws,df09.ws,df10.ws,df11.ws,df12.ws])

	#vetor com numero de ocorrencias
	noc = np.array([df01.shape[0],df02.shape[0],df03.shape[0],df04.shape[0],df05.shape[0],
		df06.shape[0],df07.shape[0],df08.shape[0],df09.shape[0],df10.shape[0],df11.shape[0],df12.shape[0]])

	#eixo x para o grafico bar
	x = np.arange(len(noc))

	pl.figure()
	pl.bar(x,noc)
	pl.title('WS > ' + str(val))
	pl.xlim(-0.2,12)
	pl.xticks(x+.4,['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'])
	pl.ylabel('Num. Ocorrencias')
	pl.savefig('fig/bar_wind_' + str(val) + '.png')

#f = pl.figure()
#ax = f.add_subplot(111)
#ax.bar(x,noc, align='center')
#ax.set_xticks(x)
#ax.set_xticklabels(['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'])
#f.show()


#dfws = pd.concat([df01.ws,df02.ws], axis=1)

dt = 1.0 / 24 #hora/24
fs = 1.0 / dt
nfft = len(dd) / 2

aaws = espec.espec1(dd.ws,nfft,fs)
aawd = espec.espec1(dd.wd,nfft,fs)

pl.figure()
pl.subplot(121)
pl.semilogx(aaws[:,0],aaws[:,1])
pl.title('Espectro de Intensidade do Vento')
pl.xlabel('cpd')
pl.grid()
pl.subplot(122)
pl.semilogx(aawd[:,0],aawd[:,1])
pl.title('Espectro de Direcao do Vento')
pl.xlabel('cpd')
pl.grid()

pl.show()