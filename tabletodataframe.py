'''
Reamostrar os dados do PNBOIA baixados
do site interpolando os dados e deixando eles
de hora em hora (em horas cheias)

Data da ultima modificacao: 25/08/2015
'''

import os
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import datetime as dt

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/LIOc/'

boia = 'B69150'

#carrega os dados em data frame
dd = pd.read_table(pathname + boia + '_onda.out',sep=',',header=0,names=['date','hs','tp','dp','hmax'])

#como acessa uma coluna
#data = dd['data']

dd['date'] = [dt.datetime.strptime(str(int(dd['date'][i])), '%Y%m%d%H%M') for i in range(len(dd))]

#define a data como indices (necessario para reamostrar de hora em hora)
df = dd.set_index('date')

#retira a data em inteiro
#df = df.ix[:,[0,]]

#reamostra os dados de hora em hora
df = df.resample('H')

#salva arquivo DataFrame
df.to_csv('out/' + boia + '_onda.csv',na_rep='')