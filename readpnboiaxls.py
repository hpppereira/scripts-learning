'''
Le dados em .xls do site do PNBOIA
'''

import os
import xlrd
import numpy as np
from datetime import datetime
import datetime as dt
import matplotlib.pylab as pl
import pandas as pd
pl.close('all')

filename = 'PNBOIA_SAN_201608.xls'

dmag = -23

csv_time_period = ('2016-08-01','2016-09-01')

pathname = os.environ['HOME'] + '/Dropbox/pnboia/data/xls/'

workbook = xlrd.open_workbook(pathname+filename)

#seleciona planilha por indice (pode ser por nome tbm)
sheet_0 = workbook.sheet_by_index(0) #planilha 1 - status + vento
sheet_1 = workbook.sheet_by_index(1) #planilha 2 - meteo + onda

#pega os valores das celulas selecionadas

#legenda
leg0 = np.array([[sheet_0.cell_value(r,c) for r in range(3,4)] for c in range(0,sheet_0.ncols)]).T
leg1 = np.array([[sheet_1.cell_value(r,c) for r in range(3,4)] for c in range(0,sheet_1.ncols)]).T

#dados - inverte - flipud
dd0 = np.flipud(np.array([[sheet_0.cell_value(r,c) for r in range(4,sheet_0.nrows)] for c in range(sheet_0.ncols)]).T)
dd1 = np.flipud(np.array([[sheet_1.cell_value(r,c) for r in range(4,sheet_1.nrows)] for c in range(sheet_1.ncols)]).T)

#substitui 'xxxx' por nan
dd0[np.where(dd0=='xxxx')] = np.nan
dd1[np.where(dd1=='xxxx')] = np.nan
dd0[np.where(dd0=='xxx')] = np.nan
dd1[np.where(dd1=='xxx')] = np.nan
dd0[np.where(dd0=='XXX')] = np.nan
dd1[np.where(dd1=='XXX')] = np.nan
dd0[np.where(dd0=='')] = np.nan
dd1[np.where(dd1=='')] = np.nan


df0 = pd.DataFrame(dd0[:,[1,3,5,6,7,8,9,10]],columns=['date','bat','ws1','wg1','wd1','ws2','wg2','wd2'])
df1 = pd.DataFrame(dd1[:,[1,2,3,4,5,6,7,8,9,10]],columns=['date','at','rh','dwp','pr','sst','hs','hmax','tp','dp'])

df0['date'] = pd.to_datetime(df0.date)
df1['date'] = pd.to_datetime(df1.date)

df0 = df0.set_index('date')
df1 = df1.set_index('date')

df0 = df0.astype(float)
df1 = df1.astype(float)

#corrige declinacao magnetica
df0[['wd1','wd2']] = df0[['wd1','wd2']] + dmag
df1['dp'] = df1['dp'] + dmag

#reamostra de hora em hora
df0 = df0.resample('H').mean()
df1 = df1.resample('H').mean()

#junta os dois dados
df = df1.join(df0)

#escolhe o periodo
df = df[csv_time_period[0]:csv_time_period[1]]

df.to_csv('../out/' + filename + '_metocean.csv',na_rep='nan')

pl.figure()
pl.subplot(211)
pl.plot(df.index,df.ws1,'bo')
pl.plot(df.index,df.ws1,'ro')
pl.title(filename)
pl.grid()
pl.ylabel('WS (m/s)')
pl.subplot(212)
pl.plot(df.index,df.wd1,'bo')
pl.plot(df.index,df.wd2,'ro')
pl.grid()
pl.ylabel('WD (deg)')

pl.figure()
pl.subplot(311)
pl.plot(df.index,df.hs,'o')
pl.title(filename)
pl.grid()
pl.ylabel('Hs (m)')
pl.subplot(312)
pl.plot(df.index,df.tp,'o')
pl.grid()
pl.ylabel('Tp (s)')
pl.subplot(313)
pl.plot(df.index,df.dp,'o')
pl.grid()
pl.ylabel('Dp (g)')

pl.show()