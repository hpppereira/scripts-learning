'''
Baixa dados da BMOBR05 de forma operacional

site: http://www.ambidados.net/BMOP/BMOP05.html
'''

import os
import pandas as pd
import numpy as np
import matplotlib.pylab as pl

#pathname de onde vai salvar os dados concatenados
pathname = os.environ['HOME'] + '/Dropbox/projects/BMOP/Sistemas-BMOP/Processamento/dados/BMOBR05_CF1/op/'

#carrega arquivo antigo concatenado 
old = pd.read_table(pathname + 'Dados_BMOBR05.csv',sep=',',parse_dates=['date'],index_col=['date'])

#site de onde estao os dados
site = 'http://www.ambidados.net/BMOP/BMOP05.html'

#carrega tabela em html
html = pd.read_html(site,thousands=".")[1]
#html = pd.read_html(site,infer_types=False,thousands=".")[1]

#transforma em dataframe e inverte os dados (mais recentes no final)
html = pd.DataFrame(np.flipud(html))

#troca virgula por ponto
html = html.replace(',','.',regex=True)

#cria dicionario
dd = {
	  'date' 	: [pd.to_datetime(html.ix[i,0] + ' ' + str(html.ix[i,1]), format='%d/%m/%Y %H') for i in range(len(html))], #data em datetime
	  'bat'  	: html.ix[:,2], #bateria (V)
	  'tdl'  	: html.ix[:,3], #temperatura do data logger (graus)
	  'ws'   	: html.ix[:,4], #intensidade do vento (m/s)
	  'wd'   	: html.ix[:,5], #direcao do vento (graus)
	  'ate'   	: html.ix[:,6], #temperatura do ar (graus)
	  'rh'   	: html.ix[:,7], #umidade relativa (%)
	  'bp'   	: html.ix[:,8], #pressao atm (hPa)
	  'tsup' 	: html.ix[:,9], #temperatura ADCP (graus)
	  'mag1' 	: html.ix[:,10], #magnitude da corrente a 25 m (mm/s)
	  'dir1' 	: html.ix[:,11], #direcao da corrente a 25 m (mm/s)
	  'mag2' 	: html.ix[:,12], #magnitude da corrente a 263 m (mm/s)
	  'dir2' 	: html.ix[:,13], #direcao da corrente a 263 (mm/s)
	  'mag3' 	: html.ix[:,14], #magnitude da corrente a 280 (mm/s)
	  'dir3' 	: html.ix[:,15], #direcao da corrente a 280 (mm/s)
	  'hs' 		: html.ix[:,16], #altura significativa (m)
	  'tp' 		: html.ix[:,17], #periodo de pico (s)
	  'dp' 		: html.ix[:,18], #direcao de pico (graus)
	  'con'     : html.ix[:,19], #consum (W)
	  'psbe10'  : html.ix[:,20], #pressao SBE a 10 m (hPa)
	  'psbe100' : html.ix[:,21], #pressao SBE a 100 m (hPa)
	  'tsbe10'  : html.ix[:,22], #temperatura SBE a 10 m (graus)
	  'tsbe20'  : html.ix[:,23], #temperatura SBE a 20 m (graus)
	  'tsbe30'  : html.ix[:,24], #temperatura SBE a 30 m (graus)
	  'tsbe40'  : html.ix[:,25], #temperatura SBE a 40 m (graus)
	  'tsbe50'  : html.ix[:,26], #temperatura SBE a 50 m (graus)
	  'tsbe60'  : html.ix[:,27], #temperatura SBE a 60 m (graus)
	  'tsbe70'  : html.ix[:,28], #temperatura SBE a 70 m (graus)
	  'tsbe80'  : html.ix[:,29], #temperatura SBE a 80 m (graus)
	  'tsbe90'  : html.ix[:,30], #temperatura SBE a 90 m (graus)
	  'tsbe100' : html.ix[:,31], #temperatura SBE a 100 m (graus)
	  'lat'     : html.ix[:,32], #latitude (decimos de graus)
	  'lon'     : html.ix[:,33], #longitude (decimos de graus)
	  }


#substituir **** do hs por nan e multiplicar hs por .01
#dd['hs'][np.where(dd['hs'] == '0,0 *****')[0]] = np.nan
#dd['hs'] = dd['hs'].astype(float) * .01

#transforma dicionario em dataframe
df = pd.DataFrame(dd)

#deixa data como indice
df = df.set_index('date')

#transforma em float
df = df.astype(float)

#corrige declinacao magnetica
df.dp = df.dp - 23 #onda
df.wd = df.wd - 23 #vento
df.dir1 = df.dir1 - 23
df.dir2 = df.dir2 - 23
df.dir3 = df.dir3 - 23

df.dp.loc[df.dp < 0] = df.dp.loc[df.dp < 0] + 360
df.wd.loc[df.wd < 0] = df.wd.loc[df.wd < 0] + 360
df.dir1.loc[df.dir1 < 0] = df.dir1.loc[df.dir1 < 0] + 360
df.dir2.loc[df.dir2 < 0] = df.dir2.loc[df.dir2 < 0] + 360
df.dir3.loc[df.dir3 < 0] = df.dir3.loc[df.dir3 < 0] + 360

#concatena o dado antigo com o novo
df = pd.concat([old,df])

#retira dados repetidos (verifica a data)
u, ind = np.unique(df.index, return_index=True)
df = df.ix[ind]

#converte serie de vento em float
df.ws = df.ws.astype(float)

#controle de qualidade
df.ix[pl.find(df.ws > 30),['ws','wd']] = np.nan
df.ix[pl.find(df.hs < 0),['hs','tp','dp']] = np.nan
df.ix[pl.find(df.mag1 < 0),['mag1','dir1']] = np.nan
df.ix[pl.find(df.mag2 < 0),['mag2','dir2']] = np.nan
df.ix[pl.find(df.mag3 < 0),['mag3','dir3']] = np.nan
df.ix[pl.find((df.tsup < 12) | (df.tsup > 29)),['tsup']] = np.nan

df.to_csv(pathname + 'Dados_BMOBR05.csv')
df['hs'].to_json(pathname + 'Hs_BMOBR05.json', orient='values')
df['tp'].to_json(pathname + 'Tp_BMOBR05.json', orient='values')
df['dp'].to_json(pathname + 'Dp_BMOBR05.json', orient='values')
df['ws'].to_json(pathname + 'WS_BMOBR05.json', orient='values')
df['wd'].to_json(pathname + 'WD_BMOBR05.json', orient='values')