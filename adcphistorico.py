
# coding: utf-8

# In[304]:

'''Processamento dos dados do ADCP da Vale
disponibilizados coletados pela Ambidados
Os dados estao em 
ww3vale/dados/historico/'''

import numpy as np
from matplotlib import pylab as pl
import os
import pandas as pd
import consistebruto


# In[531]:

'''Estrutura os dados em data frame --  adicionar a dp no data frame e
ajusta as datas com datetime - intermo os dados de hora em hora'''

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/historico/'

#le de ondas (Hs e Tp) dos arquivos em pandas
df04 = pd.read_table(pathname + 'onda_Boia4_01092014_03092015.txt',skiprows=1,sep='\t',header=0,\
                      names=['date','hs','tp'])

#le direcao
df04dir = pd.read_table(pathname + 'dirpp_Boia4_01092014_03092015.txt',skiprows=0,sep='\t',header=0,\
                      names=['date','dp'])

df10 = pd.read_table(pathname + 'onda_Boia10_01092014_03092015.txt',skiprows=1,sep='\t',header=0,\
                      names=['date','hs','tp'])

df10dir = pd.read_table(pathname + 'dirpp_Boia10_01092014_03092015.txt',skiprows=0,sep='\t',header=0,\
                      names=['date','dp'])


#colocar os valores com dia 0 idem ao dia anterior

#boia 04
#hs e tp
for i in range(len(df04)):
    if df04['date'][i][0] == '0':
        df04['date'][i] = df04['date'][i-1][0:11] + df04['date'][i][-8:]

#dp
for i in range(len(df04dir)):
    if df04dir['date'][i][0] == '0':
        df04dir['date'][i] = df04dir['date'][i-1][0:11] + df04dir['date'][i][-8:]

#boia 10
#boia 10
for i in range(len(df10)):
    if df10['date'][i][0] == '0':
        df10['date'][i] = df10['date'][i-1][0:11] + df10['date'][i][-8:]

#dp
for i in range(len(df10dir)):
    if df10dir['date'][i][0] == '0':
        df10dir['date'][i] = df10dir['date'][i-1][0:11] + df10dir['date'][i][-8:]

#deixa a coluna de datas com datetime

#hs e tp
df04['date'] = pd.to_datetime(df04['date'], format='%d/%m/%Y %H:%M:%S')
df10['date'] = pd.to_datetime(df10['date'], format='%d/%m/%Y %H:%M:%S')

#dp
df04dir['date'] = pd.to_datetime(df04dir['date'], format='%d/%m/%Y %H:%M:%S')
df10dir['date'] = pd.to_datetime(df10dir['date'], format='%d/%m/%Y %H:%M:%S')

#deixa as datas como indice
df04 = df04.set_index('date')
df04dir = df04dir.set_index('date')
df10 = df10.set_index('date')
df10dir = df10dir.set_index('date')

#reamostra os dados horarios
df04 = df04.resample('H')
df04dir = df04dir.resample('H')
df10 = df10.resample('H')
df10dir = df10dir.resample('H')

#coloca a direcao no array de hs e tp
df04['dp'] = df04dir['dp']
df10['dp'] = df10dir['dp']



# In[541]:

'''consistencia dos dados. todos
os dados que forem reprovados em algura reprova
o valor de tp e dp, assim como o tp e dp invalidam o hs'''

#nan nos valores com hs > 4 - nos 2 adcps
df04.hs[df04.hs > 4] = np.nan
df04.tp[df04.hs > 4] = np.nan
df04.dp[df04.hs > 4] = np.nan

df10.hs[df10.hs > 4] = np.nan
df10.tp[df10.hs > 4] = np.nan
df10.dp[df10.hs > 4] = np.nan

#remove valores de hs abaixo de 0.4 m
df04.hs[df04.hs < 0.4] = np.nan
df04.tp[df04.hs < 0.4] = np.nan
df04.dp[df04.hs < 0.4] = np.nan

df10.hs[df10.hs < 0.4] = np.nan
df10.tp[df10.hs < 0.4] = np.nan
df10.dp[df10.hs < 0.4] = np.nan

#remove valores de tp abaixo de 2 s
df04.hs[df04.tp < 2] = np.nan
df04.tp[df04.tp < 2] = np.nan
df04.dp[df04.tp < 2] = np.nan

df10.hs[df10.tp < 2] = np.nan
df10.tp[df10.tp < 2] = np.nan
df10.dp[df10.tp < 2] = np.nan

#remove tp > 20 s
df04.hs[df04.tp > 20] = np.nan
df04.tp[df04.tp > 20] = np.nan
df04.dp[df04.tp > 20] = np.nan

df10.hs[df10.tp > 20] = np.nan
df10.tp[df10.tp > 20] = np.nan
df10.dp[df10.tp > 20] = np.nan


#salva arquivo DataFrame
df04.to_csv('out/adcp04_hist.csv',na_rep='NaN')
df10.to_csv('out/adcp10_hist.csv',na_rep='NaN')


# In[542]:

'''plotagem'''
#pl.close('all')

pl.figure()
pl.subplot(311)
pl.plot(df04.index,df04.hs,'b.',df10.index,df10.hs,'r.')
pl.legend(['ADCP 04','ADCP 10'],ncol=2,loc='upper center')
pl.grid()
pl.subplot(312)
pl.plot(df04.index,df04.tp,'b.',df10.index,df10.tp,'r.')
pl.grid()
pl.subplot(313)
pl.plot(df04.index,df04.dp,'b.',df10.index,df10.dp,'r.')
pl.yticks(np.arange(0,360+45,45))
pl.grid()

pl.show()

