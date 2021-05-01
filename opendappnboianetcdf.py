'''
Processamento dos dados
do PNBOIA baixados pelo
openDAP

B69008 - recife
B69007 - porto seguro
B69009 - baia guanabara
B69150 - santos
B69152 - florianopolis
B69153 - rio grande

site: goosbrasil.saltambiental

#exemplo para baixar os dados
from netCDF4 import Dataset
import matplotlib.pyplot as pl
buoy = Dataset('http://opendap.saltambiental.com.br/pnboia/B69153_argos.nc')
lon = buoy.variables['longitude'][:]
lat = buoy.variables['latitude'][:]
pl.plot(lon,lat)
pl.plot(lon[-1], lat[-1], 'r.', markersize=10)
pl.axis('equal')
pl.show()

As profundidades das camadas dos ADCPs foram retiradas dos dados
da planilha enviada pelo Ze antonio.

'''

from netCDF4 import Dataset
import numpy as np
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import os
import netCDF4 as nc
import windrose
reload(windrose)
from windrose import WindroseAxes
import math
import pandas as pd

pl.close('all')


boia = 'B69150'

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/bkp/'

#acha o ultimo arquivo baixado
lista = []
for f in np.sort(os.listdir(pathname + boia)):
	if f.endswith('.nc'):
		lista.append(f)

argosname = lista[-1]

# siteadress = 'http://opendap.saltambiental.com.br/pnboia/' + boia + '_argos.nc'

#opendap
buoy = nc.Dataset(pathname + boia + '/' + argosname)

#lista o nome das variaveis
for v in buoy.variables:
	print v

#cria dicionario com as variaveis

d = {}
d['time'] = pl.num2date(buoy.variables['time'][:])
d['lat'] = buoy.variables['latitude'][:]
d['lon'] = buoy.variables['longitude'][:]
d['bat'] = buoy.variables['battery'][:]
d['ws1'] = buoy.variables['avg_wind_int1'][:]
d['wg1'] = buoy.variables['wind_gust1'][:]
d['wd1'] = buoy.variables['wind_dir1'][:]
d['ws1_f2'] = buoy.variables['avg_wind_int1_f2'][:]
d['wg1_f2']= buoy.variables['wind_gust1_f2'][:]
d['wd1_f2'] = buoy.variables['wind_dir1_f2'][:]
d['ws2'] = buoy.variables['avg_wind_int2'][:]
d['wg2'] = buoy.variables['wind_gust2'][:]
d['wd2'] = buoy.variables['avg_dir2'][:]
d['airt'] = buoy.variables['temp_air'][:]
d['dewp'] = buoy.variables['dew_point'][:]
d['rad'] = buoy.variables['avg_radiation'][:]
d['rh'] = buoy.variables['rel_humid'][:]
d['sst'] = buoy.variables['sst'][:]
d['pr'] = buoy.variables['pressure'][:]
d['hs'] = buoy.variables['wave_hs'][:]
d['tp'] = buoy.variables['wave_period'][:]
d['dp'] = buoy.variables['wave_dir'][:]
d['hmax'] = buoy.variables['wave_h_max'][:]
d['cint1'] = buoy.variables['cm_int1'][:]
d['cdir1'] = buoy.variables['cm_dir1'][:]
d['cint2'] = buoy.variables['cm_int2'][:]
d['cdir2'] = buoy.variables['cm_dir2'][:]
d['cint3'] = buoy.variables['cm_int3'][:]
d['cdir3'] = buoy.variables['cm_dir3'][:]

df = pd.DataFrame(d, index=d['time'])

#cria coluna com nome da boia
df['buoy'] = boia


# #consistencia dos dados

#verifica posicoes das boias
if boia == 'B69153':
    df = df[(df.lat > -32.0) & (df.lat < -31.5)]
    df = df[(df.lon > -50.6) & (df.lon < -49.5)]
elif boia == 'B69152':
    df = df[(df.lat > -30.0) & (df.lat < -27.0)]
    df = df[(df.lon > -48.7) & (df.lon < -45.5)]
elif boia == 'B69150':
    df = df[(df.lat > -26.0) & (df.lat < -24.0)]
    df = df[(df.lon > -45.0) & (df.lon < -44.5)]

#acha indices dos valores inconsistentes

ind = np.where((df.cint1 == -99999.0) | (df.cint1 > 200))[0]
df.cint1[ind] = np.nan
df.cdir1[ind] = np.nan

ind = np.where((df.cint2 == -99999.0) | (df.cint2 > 200))[0]
df.cint2[ind] = np.nan
df.cdir2[ind] = np.nan

ind = np.where((df.cint3 == -99999.0) | (df.cint3 > 200))[0]
df.cint3[ind] = np.nan
df.cdir3[ind] = np.nan

ind = np.where((df.ws1 == -99999.0) | (df.ws1 > 20) | (df.ws1 == 0) )[0]
df.ws1[ind] = np.nan
df.ws1[ind] = np.nan

ind = np.where((df.sst == -99999.0)  | (df.sst > 35) | (df.sst < 10) )[0]
df.sst[ind] = np.nan
df.sst[ind] = np.nan

ind = np.where((df.airt == -99999.0)  | (df.airt > 40) | (df.airt < 5) )[0]
df.airt[ind] = np.nan
df.airt[ind] = np.nan

ind = np.where((df.hs == -99999.0)  | (df.hs > 10) | (df.hs < 0.2) )[0]
df.hs[ind] = np.nan
df.hmax[ind] = np.nan
df.tp[ind] = np.nan
df.dp[ind] = np.nan


#calcula u e v (para o calculo as direcoes sao passadas para radianos)

df['u1'] = np.cos(np.radians(df.cdir1) ) * df.cint1
df['v1'] = np.sin(np.radians(df.cdir1) ) * df.cint1

df['u2'] = np.cos(np.radians(df.cdir2) ) * df.cint2
df['v2'] = np.sin(np.radians(df.cdir2) ) * df.cint2

df['u3'] = np.cos(np.radians(df.cdir3) ) * df.cint3
df['v3'] = np.sin(np.radians(df.cdir3) ) * df.cint3

#monta o vetor de direcao a partir de u e v (para conferir o calculo do u e v)

# dire1 = []
# for i in range(len(u1)):
# 	if u1[i] > 0 and v1[i] > 0:
# 		dire1.append(np.arctan(abs(v1[i])/abs(u1[i])) * 180/np.pi )
# 	elif u1[i] < 0 and v1[i] > 0:
# 		dire1.append(180 - ( (np.arctan(abs(v1[i])/abs(u1[i])) * (180/np.pi) ) ) )
# 	elif u1[i] < 0 and v1[i] < 0:
# 		dire1.append(180 + ( (np.arctan(abs(v1[i])/abs(u1[i])) * (180/np.pi) ) ) )
# 	elif u1[i] > 0 and v1[i] < 0:
# 		dire1.append(360 - ( (np.arctan(abs(v1[i])/abs(u1[i])) * (180/np.pi) ) ) )
	
# dire1 = np.array(dire1)

#u1 = u1[1000:2000]
#v1 = v1[1000:2000]

#dire1g = dire1 * 180/np.pi

#dire1g[pl.find(dire1g < 0)] = dire1g[pl.find(dire1g < 0)] + 360

pl.figure(figsize=(12,10))
pl.subplot(211)
pl.plot(df.index,df.cint1,'.')
pl.title(boia + ' -- Correntes (ADCP) - Camada 1 - 7 m')
pl.ylim(0,150)
pl.ylabel('Velocidade (cm/s)')
pl.grid()
pl.subplot(212)
pl.plot(df.index,df.cdir1,'.')
pl.ylabel('Direcao (graus)')
pl.ylim(0,360)
pl.grid()
#pl.savefig('fig/' + boia + '_ADCP1')


pl.figure(figsize=(12,10))
pl.subplot(211)
pl.plot(df.index,df.cint2,'.')
pl.title(boia + ' -- Correntes (ADCP) - Camada 2 - 30 m')
pl.ylim(0,150)
pl.ylabel('Velocidade (cm/s)')
pl.grid()
pl.subplot(212)
pl.plot(df.index,df.cdir2,'.')
pl.ylabel('Direcao (graus)')
pl.ylim(0,360)
pl.grid()
#pl.savefig('fig/' + boia + '_ADCP2')


pl.figure(figsize=(12,10))
pl.subplot(211)
pl.plot(df.index,df.cint3,'.')
pl.title(boia + ' -- Correntes (ADCP) - Camada 3 - 55 m')
pl.ylim(0,150)
pl.ylabel('Velocidade (cm/s)')
pl.grid()
pl.subplot(212)
pl.plot(df.index,df.cdir3,'.')
pl.ylabel('Direcao (graus)')
pl.ylim(0,360)
pl.grid()
#pl.savefig('fig/' + boia + '_ADCP3')


pl.figure(figsize=(12,10))
pl.subplot(211)
pl.plot(df.index,df.airt,'.')
pl.title(boia + ' -- Temperatura do Ar e da Sup. do Mar')
pl.ylim(10,35)
pl.ylabel('Temp. Ar (graus)')
pl.grid()
pl.subplot(212)
pl.plot(df.index,df.sst,'.')
pl.ylabel('Temp. Sup. Mar (graus)')
pl.ylim(10,35)
pl.grid()
#pl.savefig('fig/' + boia + '_AT_SST')

#Ondas
pl.figure(figsize=(12,10))
pl.subplot(311)
pl.title(boia + ' -- Ondas')
pl.plot(df.index,df.hs,'.')
pl.title(boia)
pl.ylim(0,7)
pl.ylabel('Hs (m)')
pl.grid()
pl.subplot(312)
pl.plot(df.index,df.tp,'.')
pl.ylabel('Tp (s)')
pl.ylim(3,20)
pl.grid()
pl.subplot(313)
pl.plot(df.index,df.dp,'.')
pl.ylabel('Dp (s)')
pl.grid()
pl.ylim(0,360)
#pl.savefig('fig/' + boia + '_HsTpDp')

#############################################################################
# windrose - vento
def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=10,weight='bold')
    

#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
ax.bar(df.wd1,df.ws1, normed=True, bins=np.arange(0,20,2), opening=.8, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
#plt.savefig('fig/'+boia+'_wind.png', dpi=None, edgecolor='w',
#orientation='portrait', papertype=None, format='png',
#transparent=True, bbox_inches=None, pad_inches=0.1)    


#############################################################################
# windrose - camada 1
def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=10,weight='bold')
    

#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
ax.bar(df.cdir1,df.cint1, normed=True, bins=np.arange(0,100,10), opening=.8, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
#plt.savefig('fig/'+boia+'_c1rose.png', dpi=None, edgecolor='w',
#orientation='portrait', papertype=None, format='png',
#transparent=True, bbox_inches=None, pad_inches=0.1)    


#############################################################################
# windrose - camada 2
def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=10,weight='bold')
    

#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
ax.bar(df.cdir2,df.cint2, normed=True, bins=np.arange(0,100,10), opening=.8, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
#plt.savefig('fig/'+boia+'_c2rose.png', dpi=None, edgecolor='w',
#orientation='portrait', papertype=None, format='png',
#transparent=True, bbox_inches=None, pad_inches=0.1)    


#############################################################################
# windrose - camada 3
def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=10,weight='bold')
    

#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
ax.bar(df.cdir3,df.cint3, normed=True, bins=np.arange(0,100,10), opening=.8, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
#plt.savefig('fig/'+boia+'_c3rose.png', dpi=None, edgecolor='w',
#orientation='portrait', papertype=None, format='png',
#transparent=True, bbox_inches=None, pad_inches=0.1)    


#salva arquivo de corrente
df[['buoy','airt','sst','cint1','cdir1','u1','v1','cint2','cdir2','u2','v2','cint3','cdir3','u3','v3']].to_csv('out/'+boia+'_ADCP.csv', na_rep='nan',
 date_format='%Y-%m-%d %H:%M', index=True, index_label='date', float_format='%.2f')




#############################################################################
# windrose - Hs x Dp
def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=10,weight='bold')
    

#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
ax.bar(df.dp,df.hs, normed=True, bins=np.arange(0,7,1), opening=.8, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
#plt.savefig('fig/'+boia+'_rosa_HsDp.png', dpi=None, edgecolor='w',
#orientation='portrait', papertype=None, format='png',
#transparent=True, bbox_inches=None, pad_inches=0.1)    


#############################################################################
# windrose - Tp x Dp
def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=10,weight='bold')
    

#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
ax.bar(df.dp,df.tp, normed=True, bins=np.arange(0,24,2), opening=.8, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
#plt.savefig('fig/'+boia+'_rosa_TpDp.png', dpi=None, edgecolor='w',
#orientation='portrait', papertype=None, format='png',
#transparent=True, bbox_inches=None, pad_inches=0.1)    



# #carrega as planilhas
# rg = pd.read_table('out/B69153_ADCP.csv',sep=',', parse_dates=['date'], index_col=0)
# fl = pd.read_table('out/B69152_ADCP.csv',sep=',', index_col=0)
# sa = pd.read_table('out/B69150_ADCP.csv',sep=',', index_col=0)

# pl.figure(figsize=(12,6))
# pl.plot(rg.index,np.ones(len(rg))*1,'b.',markersize=12, label='Rio Grande')
# pl.plot(fl.index,np.ones(len(fl))*2,'r.',markersize=12, label='Florianopolis')
# pl.plot(sa.index,np.ones(len(sa))*3,'g.',markersize=12, label='Santos')
# pl.legend(loc=0)
# pl.axis('tight')
# pl.ylim(0.8,3.2)
# pl.yticks(visible=False)
# pl.grid()


#separa e salva arquivos de 2013 pra ca para validacao do ww3 (enviar para jonas e izabel - 18/01/2016)

# df.loc['2013':][['hs','tp','dp','hmax','ws1','wd1','ws2','wd2']].to_csv('out/jonas/'+boia+'_metocean_2013.csv', na_rep='nan',
#  date_format='%Y-%m-%d %H:%M', index=True, index_label='date', float_format='%.2f')


pl.figure()
pl.subplot(211)
pl.title('Vento -- ' + boia)
df.loc['2013':].ws1.plot(color='b')
pl.ylim(0,20)
pl.subplot(212)
df.loc['2013':].wd1.plot(color='b')
pl.ylim(0,360)



pl.figure()
pl.subplot(311)
pl.title('Onda -- ' + boia)
df.loc['2013':].hs.plot()
pl.ylim(0,10)
pl.xticks(visible=False)
pl.twinx()
df.loc['2013':].hmax.plot(color='r')
pl.ylim(0,10)
pl.xticks(visible=False)
pl.subplot(312)
df.loc['2013':].tp.plot()
pl.xticks(visible=False)
pl.subplot(313)
df.loc['2013':].dp.plot()



pl.show()
