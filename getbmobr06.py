'''
Baixa dados da BMOBR05 de forma operacional

site: http://www.ambidados.net/BMOP/BMOP05.html
'''

import os
import pandas as pd
import numpy as np
import matplotlib.pylab as pl

#pathname de onde vai salvar os dados concatenados
pathname = os.environ['HOME'] + '/Dropbox/projects/BMOP/Processamento/dados/CF3_BMOBR06_2016Jun/op/'

#carrega arquivo antigo concatenado 
old = pd.read_table(pathname + 'Dados_BMOBR06.csv',sep=',',parse_dates=['date'],index_col=['date'])

#site de onde estao os dados
site = 'http://www.ambidados.net/BMOP/BMOP06.html'

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
	  'mag1' 	: html.ix[:,10], #magnitude da corrente a 43 m (mm/s)
	  'dir1' 	: html.ix[:,11], #direcao da corrente a 43 m (mm/s)
	  'mag2' 	: html.ix[:,12], #magnitude da corrente a 235 m (mm/s)
	  'dir2' 	: html.ix[:,13], #direcao da corrente a 235 (mm/s)
	  'mag3' 	: html.ix[:,14], #magnitude da corrente a 367 (mm/s)
	  'dir3' 	: html.ix[:,15], #direcao da corrente a 367 (mm/s)
	  'hs' 		: html.ix[:,16], #altura significativa (m)
	  'tp' 		: html.ix[:,17], #periodo de pico (s)
	  'dp' 		: html.ix[:,18], #direcao de pico (graus)
	  'con'     : html.ix[:,19], #consum (W)
	  'psbe10'  : html.ix[:,20], #pressao SBE a 10 m (hPa)
	  'psbe40'  : html.ix[:,21], #pressao SBE a 10 m (hPa)
	  'psbe70'  : html.ix[:,22], #pressao SBE a 10 m (hPa)
	  'psbe100' : html.ix[:,23], #pressao SBE a 100 m (hPa)
	  'tsbe10'  : html.ix[:,24], #temperatura SBE a 10 m (graus)
	  'tsbe20'  : html.ix[:,25], #temperatura SBE a 20 m (graus)
	  'tsbe30'  : html.ix[:,26], #temperatura SBE a 30 m (graus)
	  'tsbe40'  : html.ix[:,27], #temperatura SBE a 40 m (graus)
	  'tsbe50'  : html.ix[:,28], #temperatura SBE a 50 m (graus)
	  'tsbe60'  : html.ix[:,29], #temperatura SBE a 60 m (graus)
	  'tsbe70'  : html.ix[:,30], #temperatura SBE a 70 m (graus)
	  'tsbe80'  : html.ix[:,31], #temperatura SBE a 80 m (graus)
	  'tsbe90'  : html.ix[:,32], #temperatura SBE a 90 m (graus)
	  'tsbe100' : html.ix[:,33], #temperatura SBE a 100 m (graus)
	  'lat'     : html.ix[:,34], #latitude (decimos de graus)
	  'lon'     : html.ix[:,35], #longitude (decimos de graus)
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

df = df['2016-06-24':]

sbe = df[['tsbe10', 'tsbe20', 'tsbe30', 'tsbe40', 'tsbe50', 'tsbe60', 'tsbe70', 'tsbe80', 'tsbe90', 'tsbe100']]
mag = df[['mag1', 'mag2', 'mag3']]
dire = df[['dir1', 'dir2', 'dir3']]

#controle de qualidade
df.ix[pl.find(df.ws > 30),['ws','wd']] = np.nan
df.ix[pl.find(df.hs < 0),['hs','tp','dp']] = np.nan
df.ix[pl.find(df.mag1 < 0),['mag1','dir1']] = np.nan
df.ix[pl.find(df.mag2 < 0),['mag2','dir2']] = np.nan
df.ix[pl.find(df.mag3 < 0),['mag3','dir3']] = np.nan
df.ix[pl.find((df.tsup < 12) | (df.tsup > 29)),['tsup']] = np.nan

sbe = sbe[sbe < 30] ; sbe = sbe[sbe > 15]


df.to_csv(pathname + 'Dados_BMOBR06.csv')
df['rh'].to_csv(pathname + 'RH_BMOBR06.csv', header=['Pr. Atm'], index_label='Date')
df['bp'].to_csv(pathname + 'BP_BMOBR06.csv', header=['Pr. Atm'], index_label='Date')
df['hs'].to_csv(pathname + 'HS_BMOBR06.csv', header=['Pr. Atm'], index_label='Date')
df['tp'].to_csv(pathname + 'TP_BMOBR06.csv', header=['Pr. Atm'], index_label='Date')
df['dp'].to_csv(pathname + 'DP_BMOBR06.csv', header=['Pr. Atm'], index_label='Date')
df['ws'].to_csv(pathname + 'WS_BMOBR06.csv', header=['Int. Vento'], index_label='Date')
df['wd'].to_csv(pathname + 'WD_BMOBR06.csv', header=['Int. Vento'], index_label='Date')
df[['bat','con']].to_csv(pathname + 'BAT_BMOBR06.csv', header=['Bateria', 'Consumo'], index_label='Date')
df[['ate','tsup']].to_csv(pathname + 'ATE_BMOBR06.csv', header=['Temp. Ar', 'Temp. Água'], index_label='Date')
sbe.to_csv(pathname + 'SBE_BMOBR06.csv', header=['tsbe10', 'tsbe20', 'tsbe30', 'tsbe40', 'tsbe50', 'tsbe60',
												 'tsbe70', 'tsbe80', 'tsbe90', 'tsbe100'], index_label='Date')
mag.to_csv(pathname + 'MAG_BMOBR06.csv', header=['Mag.43m', 'Mag.235m', 'Mag.367m'], index_label='Date')
dire.to_csv(pathname + 'DIR_BMOBR06.csv', header=['Dir.43m', 'Dir.235m', 'Dir.367m'], index_label='Date')