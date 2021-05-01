'''
Concatenate PNBOIA's Argos data from buoy's memory card
- Fornecido pelo CHM

# sensor 0 - ???
# sensor 1 - ???
# sensor 2 - wind speed 1
# sensor 3 - wind gust 1
# sensor 4 - wind dir 1
# sensor 5 - air temp
# sensor 6 - relative humidity
# sensor 7 - dew point
# sensor 8 - pressure
# sensor 9 - sst
# sensor 10 - buoy heading
# sensor 11 - clorofila
# sensor 12 - turbidez
# sensor 13 - solar rad
# sensor 14 - CM velocity 1
# sensor 15 - CM direction 1
# sensor 16 - CM velocity 2
# sensor 17 - CM direction 2
# sensor 18 - CM velocity 3
# sensor 19 - CM direction 3
# sensor 20 - Hs
# sensor 21 - Hmax
# sensor 22 - Periodo
# sensor 23 - Mn dir
# sensor 24 - spread
# sensor 25 - spare ???
# sensor 26 - ???
# sensor 27 - ???
# sensor 28 - ???
# sensor 29 - ???
# sensor 30 - ???
# sensor 31 - ???
# sensor 32 - ???
'''

import os
import numpy as np
import pandas as pd
import re
import string
from matplotlib.cbook import is_numlike

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/cartao/argos/RIG/'

lis = np.sort(os.listdir(pathname))
lista = []
for l in lis:
	if l.endswith('.xls') == True:
		lista.append(l) 

df = pd.read_excel(pathname + lista[0])


df.index =  pd.to_datetime(df['Msg Date'])

for filename in lista[1:]:

	print filename

	df1 = pd.read_excel(pathname + filename)

	if 'Msg Date' in df1.columns:

		df1.index =  pd.to_datetime(df1['Msg Date'])

	elif 'Loc. date' in df1.columns and 'Msg Date' not in df1.columns:

		df1.index =  pd.to_datetime(df1['Loc. date'])

	df = pd.concat([df,df1])

df = df['2010':]

#first quality control
#coloca nan nos valores que nao sao numeros

#df = df.loc[df['SENSOR 02'] <> 'DF'] #ws > 0

#df['ws'] = df['SENSOR 02']

df['ws'] = np.nan
df['wg'] = np.nan
df['wd'] = np.nan
df['at'] = np.nan



for i in range(len(df)):
	print str(i) + ' - ' + str(len(df))

	try:
		print 'try' + str(df['SENSOR 02'][i])

		df['ws'][i]   = float(df['SENSOR 02'][i])
		df['wg'][i]   = float(df['SENSOR 03'][i])
		df['wd'][i]   = float(df['SENSOR 04'][i])
		df['at'][i]   = float(df['SENSOR 05'][i])
		df['rh'][i]   = float(df['SENSOR 06'][i])
		df['dw'][i]   = float(df['SENSOR 07'][i])
		df['pr'][i]   = float(df['SENSOR 08'][i])
		df['st'][i]   = float(df['SENSOR 09'][i])
		df['he'][i]   = float(df['SENSOR 10'][i])
		df['cla'][i]  = float(df['SENSOR 11'][i])
		df['tur'][i]  = float(df['SENSOR 12'][i])
		df['sr'][i]   = float(df['SENSOR 13'][i])
		df['cv1'][i]  = float(df['SENSOR 14'][i])
		df['cd1'][i]  = float(df['SENSOR 15'][i])
		df['cv2'][i]  = float(df['SENSOR 16'][i])
		df['cd2'][i]  = float(df['SENSOR 17'][i])
		df['cv3'][i]  = float(df['SENSOR 18'][i])
		df['cd3'][i]  = float(df['SENSOR 19'][i])
		df['hs'][i]   = float(df['SENSOR 20'][i])
		df['hmax'][i] = float(df['SENSOR 21'][i])
		df['tp'][i]   = float(df['SENSOR 22'][i])
		df['dp'][i]   = float(df['SENSOR 23'][i])
		df['spr'][i]  = float(df['SENSOR 24'][i])

		
	except:
		print 'except' + str(df['SENSOR 02'][i])
