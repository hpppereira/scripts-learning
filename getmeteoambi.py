'''
Load meteorological data from Ambidados website
http://www.ambidados.net/VALETIG/VALETIG.txt

Developed by: Henrique P. P. Pereira
Last modification: 2016/11/11

1  - flag id 
2  - Ano
3  - Med
4  - Dia
5  - Hora
6  - Minuto
7  - Voltagem Bateria
8  - Temperatura Datalogger
9  - Temperatura Ar
10 - Umidade Relativa
11 - Pressão
12 - Direção Vento 
13 - Intensidade Vento
14 - Dir Med
15 - Intensidade Max
16 - Chuva hora
17 - Chuva acumulada

Perguntas:
Amostragem a cada 6 horas (144 amostragens no dia) 

Obsevacoes:
1) Se a linha i e linha i+1 for virgula, pular um dado
2) No minuto '0' cria um valor vazio (entre 2 virgulas)
3) Na hora de 0 a 9 (com 1 digito) cria valor vazio (entre 2 virgulas)
-- Todos que tem uma casa decimal cria um valor vazio (',,')
'''

import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
import os
import numpy as np
import pandas as pd
import urllib
import pylab as pl
from datetime import datetime


pl.close('all')

#pathname to save fig and data
pathname = os.environ['HOME'] + '/Dropbox/ambidados/web/meteorologia/'

target_url = 'http://www.ambidados.net/VALETIG/VALETIG.txt'

dd = []

with urllib.request.urlopen(target_url) as f:

	content = f.read().splitlines()

	for line in content:

		line = line.decode('utf-8')

		if line.startswith('3'):

			line1 = np.array(line.split(','))

			if line1[2] == '': #mes

				line1[2:-1] = line1[3:]
				line1 = line1[:-1]

			if line1[3] == '': #hora

				line1[3:-1] = line1[4:]
				line1 = line1[:-1]

			if line1[4] == '': #minuto

				line1[4:-1] = line1[5:]
				line1 = line1[:-1]

			if line1[5] == '': #minuto

				line1[5:-1] = line1[6:]
				line1 = line1[:-1]

			if line1.shape[0] > 17:

				print (line1.shape)

			dd.append(line1)

dd = np.array(dd)
dd = dd.astype(float)

date = [datetime(int(dd[i,1]), int(dd[i,2]), int(dd[i,3]), int(dd[i,4]), int(dd[i,5]) ) for i in range(len(dd))]

df = pd.DataFrame(dd, columns=['flagid','yr','mo','day','hour','min','bat','templogger','at','rh','pr','wd','ws','dirmed','intmax','chuvahora','chuvaacum'])

df['date'] = date

df = df.set_index('date')

df = df['2016-11-01':]

#figuras

titles = ['Bateria (V)', 'Temp. DataLogger (C)', 'Temp. Ar (C)', 'Umid. Rel (%)', 'Pressao Atm (hPa)', 'Dir Vento (graus)', 'Int Vento (m/s)', 
		  'Dir. Media (graus)', 'Int. Max', 'Chuva (hora)', 'Chuva (acum)']

cont = -1
for c in df.columns[6:]:

	cont += 1

	print (c)

	pl.figure(figsize=(12,8))
	pl.plot(df.index, df[c],'.')
	pl.title(str(df.index[-1]))
	pl.ylabel(titles[cont])
	pl.grid()
	pl.xticks(rotation=10)

	if c == 'wd':

		pl.ylim(0,360)

	elif c == 'ws':

		pl.plot(df.index, df.intmax,'.')
		pl.legend(['Int. Media', 'Int. Max'])
		pl.ylim(0,20)

	pl.savefig(pathname + 'img/' + c + '.png')

df.to_csv(pathname + 'data/meteorologia.csv')

pl.show()