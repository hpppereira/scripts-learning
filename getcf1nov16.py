'''
Baixa dados da BMOBR05 de forma operacional

site: http://www.ambidados.net/BMOP/BMOP05.html
'''

import os
import pandas as pd
import numpy as np
import matplotlib.pylab as pl

#pathname de onde vai salvar os dados concatenados
pathname = os.environ['HOME'] + '/Dropbox/database/realtime/buoys/remo/CF1_BMOBR05_2016Nov/'

#carrega arquivo antigo concatenado 
old = pd.read_table(pathname + 'cf1nov16.csv',sep=',',parse_dates=['date'],index_col=['date'])

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
	  'mag1' 	: html.ix[:,10], #magnitude da corrente a 40 m (mm/s)
	  'dir1' 	: html.ix[:,11], #direcao da corrente a 40 m (mm/s)
	  'err' 	: html.ix[:,12], #Erro (ADCP)
	  'hs_ax'	: html.ix[:,13], #Hs da Axys
	  'tp_ax' 	: html.ix[:,14], #Tp da Axys
	  'dp_ax' 	: html.ix[:,15], #Dp da Axys
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
df.dp = df.dp - 23 #direcao onda
df.dp_ax = df.dp_ax - 23 #direcao onda axys
df.wd = df.wd - 23 #direcao vento
df.dir1 = df.dir1 - 23 #direcao corrente

df.dp.loc[df.dp < 0] = df.dp.loc[df.dp < 0] + 360
df.dp_ax.loc[df.dp_ax < 0] = df.dp_ax.loc[df.dp_ax < 0] + 360
df.wd.loc[df.wd < 0] = df.wd.loc[df.wd < 0] + 360
df.dir1.loc[df.dir1 < 0] = df.dir1.loc[df.dir1 < 0] + 360

#concatena o dado antigo com o novo
df = pd.concat([old,df])

#retira dados repetidos (verifica a data)
u, ind = np.unique(df.index, return_index=True)
df = df.ix[ind]

#converte serie de vento em float
df.ws = df.ws.astype(float)

#pega dados a partir de novembro
df = df['2016-11-06':]

#controle de qualidade
df.ix[pl.find(df.ws > 30),['ws','wd']] = np.nan
df.ix[pl.find(df.hs < 0),['hs','tp','dp']] = np.nan
df.ix[pl.find(df.mag1 < 0),['mag1','dir1']] = np.nan
df.ix[pl.find((df.tsup < 12) | (df.tsup > 28)),['tsup']] = np.nan
df.ix[pl.find((df.ate < 12) | (df.ate > 29)),['ate']] = np.nan
df.ix[pl.find((df.bp < 900) | (df.bp > 1030)),['bp']] = np.nan
df.ix[pl.find((df.tsbe10 < 10) | (df.tsbe10 > 28)),['tsbe10']] = np.nan
df.ix[pl.find((df.tsbe20 < 10) | (df.tsbe20 > 28)),['tsbe20']] = np.nan
df.ix[pl.find((df.tsbe30 < 10) | (df.tsbe30 > 28)),['tsbe30']] = np.nan
df.ix[pl.find((df.tsbe40 < 10) | (df.tsbe40 > 28)),['tsbe40']] = np.nan
df.ix[pl.find((df.tsbe50 < 10) | (df.tsbe50 > 28)),['tsbe50']] = np.nan
df.ix[pl.find((df.tsbe60 < 10) | (df.tsbe60 > 28)),['tsbe60']] = np.nan
df.ix[pl.find((df.tsbe70 < 10) | (df.tsbe70 > 28)),['tsbe70']] = np.nan
df.ix[pl.find((df.tsbe80 < 10) | (df.tsbe80 > 28)),['tsbe80']] = np.nan
df.ix[pl.find((df.tsbe90 < 10) | (df.tsbe90 > 28)),['tsbe90']] = np.nan
df.ix[pl.find((df.tsbe100 < 10) | (df.tsbe100 > 28)),['tsbe100']] = np.nan


#magnitude das correntes de mm/s para m/s
df.mag1 = df.mag1 / 1000

df.to_csv(pathname + 'cf1nov16.csv')

#df['hs'].to_json(pathname + 'Hs_BMOBR05.json', orient='values')
#df['tp'].to_json(pathname + 'Tp_BMOBR05.json', orient='values')
#df['dp'].to_json(pathname + 'Dp_BMOBR05.json', orient='values')
#df['ws'].to_json(pathname + 'WS_BMOBR05.json', orient='values')
#df['wd'].to_json(pathname + 'WD_BMOBR05.json', orient='values')


df[['hs','tp']].to_csv(path_or_buf=pathname + 'HsTp_CF01.csv', sep=',', na_rep='', float_format='%.2f',
		  columns=None, header=['Hs','Tp'], index=True, index_label='Date')

df[['dp']].to_csv(path_or_buf=pathname + 'Dp_CF01.csv', sep=',', na_rep='', float_format='%.2f',
		  columns=None, header=['Dp'], index=True, index_label='Date')

df[['ws','wd']].to_csv(path_or_buf=pathname + 'WIND_CF01.csv', sep=',', na_rep='', float_format='%.2f',
		  columns=None, header=['Int. Vento','Dir. Vento'], index=True, index_label='Date')

df[['ate','tsup']].to_csv(path_or_buf=pathname + 'AWT_CF01.csv', sep=',', na_rep='', float_format='%.2f',
		  columns=None, header=['Temp. Ar','Temp. Agua'], index=True, index_label='Date')

df[['rh','bp']].to_csv(path_or_buf=pathname + 'RHBP_CF01.csv', sep=',', na_rep='', float_format='%.2f',
		  columns=None, header=['Umid. Rel','P. Atm'], index=True, index_label='Date')

df[['mag1','dir1']].to_csv(path_or_buf=pathname + 'CURR_CF01.csv', sep=',', na_rep='', float_format='%.2f',
		  columns=None, header=['Int. Corr','Dir. Corr'], index=True, index_label='Date')

df[['tsbe10','tsbe20','tsbe30','tsbe40','tsbe50','tsbe60','tsbe70','tsbe80','tsbe90','tsbe100']].to_csv(
	path_or_buf=pathname + 'SBE_CF01.csv', sep=',', na_rep='', float_format='%.2f',
	columns=None, header=['10m','20m','30m','40m','50m','60m','70m','80m','90m','100m',], index=True, index_label='Date')

df.to_csv(pathname + 'Dados_CF01.csv', sep=',', na_rep='', float_format='%.2f',
		  columns=None, header=True, index=True, index_label='Date')