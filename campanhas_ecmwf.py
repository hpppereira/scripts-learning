'''Processamento dos dados do ECMWF
para o projeto ww3seal
'''


import os
import netCDF4 as nc
import pylab as pl
import numpy as np
import pandas as pd
import matplotlib as mpl
import datetime
#import xray


pathname = os.environ['HOME'] + '/Dropbox/ww3seal/ECMWF/'

#carrega dados do ECMWF
#dd1 = nc.Dataset(pathname + 'Ondas_ECMWF_SEAL_Eventos.nc')
dd = nc.Dataset(pathname + 'Ondas_ECMWF_SEAL_2010_2015.nc')
#dd3 = nc.Dataset(pathname + 'Ondas_ECMWF_SEAL_2008_AXYS.nc')

#aa = xray.open_dataset(pathname + 'Ondas_ECMWF_SEAL_2010_2015.nc')
#seleciona valores utilizando xray
#aa.sel(longitude=slice(-37,-38),latitude=(-40,-43))


#carrega dados da boia axys
#ax = pd.read_csv(os.environ['HOME']+ '/Dropbox/ww3seal/rot/out/axys.csv',parse_dates=['date'],index_col=['date']) #dados axys
#axm = pd.read_csv(os.environ['HOME']+ '/Dropbox/ww3seal/rot/out/axys_mod.csv',parse_dates=['date'],index_col=['date']) #ww3

#media movel nos dados
#ax['hs'] = pd.rolling_mean(ax.hs,2)

#lista o nome das variaveis
for v in dd.variables:
	print v

'''
longitude
latitude
time
swh
mwd
mwp
'''

pl.close('all')

#pl.num2date

time = dd.variables['time'][:]
lats = dd.variables['latitude'][:]
lons = - (360 - dd.variables['longitude'][:])
hs = dd.variables['swh'][:]
tp = dd.variables['mwp'][:]
dp = dd.variables['mwd'][:]

print dd.variables['time'].dimensions
print dd.variables['swh'].dimensions

#converte datas (divide por 24 para passar para dias
date = np.array(mpl.dates.num2date(time/24.0 + mpl.dates.date2num(datetime.datetime(1900,01,01,00))))

#dd.close()

# Because our lon and lat variables are 1D, 
# use meshgrid to create 2D arrays 
# Not necessary if coordinates are already in 2D arrays.
#lon, lat = np.meshgrid(lons, lats)
#xi, yi = m(lon, lat)

df = pd.DataFrame(np.array([date,hs[:,6,0],tp[:,6,0],dp[:,6,0]]).T, columns=['date','hs','tp','dp'])
df = df.set_index('date')

#cria variaveis com os eventos
df1 = df.loc['2010-11':'2010-12'] #evento 1
df2 = df.loc['2011-06'] #evento 2
df3 = df.loc['2014-05':'2014-06'] #evento 3
df4 = df.loc['2014-11':'2015-01'] #evento 4
df5 = df.loc['2013-03':'2013-04'] #evento 5
df6 = df.loc['2013-10':'2013-11'] #evento 6

#calcula valores medios, p90 e max de hs, tp e dp para cada evento
tab1 = [[df1.hs.mean(),df1.tp.mean(),df1.dp.mean()],
	   [np.percentile(df1.hs,90),np.percentile(df1.tp,90),np.percentile(df1.dp,90)],
	   [df1.hs.max(),df1.tp.max(),df1.dp.max()]]

tab2 = [[df2.hs.mean(),df2.tp.mean(),df2.dp.mean()],
	   [np.percentile(df2.hs,90),np.percentile(df2.tp,90),np.percentile(df2.dp,90)],
	   [df2.hs.max(),df2.tp.max(),df2.dp.max()]]

tab3 = [[df3.hs.mean(),df3.tp.mean(),df3.dp.mean()],
	   [np.percentile(df3.hs,90),np.percentile(df3.tp,90),np.percentile(df3.dp,90)],
	   [df3.hs.max(),df3.tp.max(),df3.dp.max()]]

tab4 = [[df4.hs.mean(),df4.tp.mean(),df4.dp.mean()],
	   [np.percentile(df4.hs,90),np.percentile(df4.tp,90),np.percentile(df4.dp,90)],
	   [df4.hs.max(),df4.tp.max(),df4.dp.max()]]

tab5 = [[df5.hs.mean(),df5.tp.mean(),df5.dp.mean()],
	   [np.percentile(df5.hs,90),np.percentile(df5.tp,90),np.percentile(df5.dp,90)],
	   [df5.hs.max(),df5.tp.max(),df5.dp.max()]]

tab6 = [[df6.hs.mean(),df6.tp.mean(),df6.dp.mean()],
	   [np.percentile(df6.hs,90),np.percentile(df6.tp,90),np.percentile(df6.dp,90)],
	   [df6.hs.max(),df6.tp.max(),df6.dp.max()]]

#pl.figure()
#pl.plot(ax.index,ax.hs,date,hs[:,6,6],axm.index,axm.hs)
#pl.legend(['AXYS','ECMWF','WW3'])

#tamanho da janela para plotagem
tj0 = df6.index[0]
tj1 = df6.index[-1]


pl.figure(figsize=(13,8))
pl.subplot(311)
pl.plot(df.index,df.hs,'b',df1.index,df1.hs,'r',df2.index,df2.hs,'r',df3.index,df3.hs,'r',df4.index,df4.hs,'r',df5.index,df5.hs,'r',df6.index,df6.hs,'r')
pl.ylabel('Hs (m)'), pl.grid(), pl.ylim(0.5,3.5), pl.xlim(tj0,tj1)
pl.subplot(312)
pl.plot(df.index,df.tp,'.b',df1.index,df1.tp,'.r',df2.index,df2.tp,'.r',df3.index,df3.tp,'.r',df4.index,df4.tp,'.r',df5.index,df5.tp,'.r',df6.index,df6.tp,'.r')
pl.ylabel('Tp (s)'), pl.grid(), pl.ylim(4,20), pl.xlim(tj0,tj1)
pl.subplot(313)
pl.plot(df.index,df.dp,'.b',df1.index,df1.dp,'.r',df2.index,df2.dp,'.r',df3.index,df3.dp,'.r',df4.index,df4.dp,'.r',df5.index,df5.dp,'.r',df6.index,df6.dp,'.r')
pl.ylabel('Dp (graus)'), pl.grid(), pl.yticks(range(0,360+45,45)), pl.xlim(tj0,tj1)



