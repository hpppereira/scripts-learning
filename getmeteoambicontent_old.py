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

import os
import numpy as np
import pandas as pd
import urllib
import pylab as pl
from datetime import datetime

pl.close('all')

target_url = 'http://www.ambidados.net/VALETIG/VALETIG.txt'

dd = []

# with urllib.request.urlopen(target_url) as f:
# 	content = f.read().splitlines()

content = np.load('content.npy')

for line in content:

	line = line.decode('utf-8')

	if line.startswith('3'):

#		print (line)

		#if line.endswith('$'):

		#	line1 = np.array(line[:-1].split(','))

		#else:

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


#		line1[np.where(line1 == '')[0]] = 'NAN'

#		line1 = line1.astype(float)

#		if len(line1) < 10:

#			print ('String com erro')

		# elif len(line1) > 73:

		# 	print (line1)
		# 	print (len(line1))

#		else:

#		dd.append(line1[:17])
		dd.append(line1)

#corrige shift nos dados (devido a uns dados faltando na coluna 2)
#linha 6086

dd = np.array(dd)

dd = dd.astype(float)

#date = [pd.to_datetime([dd[i,1] + '-' + dd[i,2] + '-' + dd[i,3] + ' ' + dd[i,4] + ':' + dd[i,5]]) for i in range(len(dd))]
date = [datetime(int(dd[i,1]), int(dd[i,2]), int(dd[i,3]), int(dd[i,4]), int(dd[i,5]) ) for i in range(len(dd))]

df = pd.DataFrame(dd, columns=['flagid','yr','mo','day','hour','min','bat','templogger','at','rh','pr','wd','ws','dirmed','intmax','chuvahora','chuvaacum'])

df['date'] = date

df = df.set_index('date')

df = df['2016-10':]

#figuras

titles = ['Bateria (V)', 'Temp. DataLogger (C)', 'Temp. Ar (C)', 'Umid. Rel (%)', 'Pressao Atm (hPa)', 'Dir Vento (graus)', 'Int Vento (m/s)', 
		  'Dir. Media (graus)', 'Int. Max', 'Chuva (hora)', 'Chuva (acum)']

cont = -1
for c in df.columns[6:]:

	cont += 1

	print (c)

	pl.figure(figsize=(12,8))
	pl.plot(df.index, df[c],'.')
	pl.ylabel(titles[cont])
	pl.grid()

	if c == 'wd':

		pl.ylim(0,360)

	elif c == 'ws':

		pl.plot(df.index, df.intmax,'.')
		pl.legend(['Int. Media', 'Int. Max'])
		pl.ylim(0,20)

	pl.savefig('fig/' + c + '.png')



pl.show()



#pega dados a partir de novembro (esta com a string correta)
#dd = dd[pl.find(dd[:,2]==11)[0]:,:]

#dd = dd[4000:5000]


#arruma coluna de mes
#dd[find(isnan(dd[:,2])),2] = dd[find(isnan(dd[:,2])),3]

#dd[6086:,3]

#dd[:6081:,2:] = dd[:6081:,1:-1]