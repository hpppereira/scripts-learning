 # -*- coding: utf-8 -*-

'''
Plota os dados da BMOBR05 que sao baixados no site
da ambidados 'getbmobr05.py'
'''

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import matplotlib.pylab as pl
from math import radians, cos, sin, asin, sqrt
import datetime
import utm

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/projects/BMOP/Processamento/dados/CF3_BMOBR06_2016Jun/op/'
pathfig = os.environ['HOME'] + '/Dropbox/projects/BMOP/Processamento/fig/BMOBR06_CF2/'

#carrega os dados da boia
dd = pd.read_csv(pathname + 'Dados_BMOBR06.csv', index_col='date', parse_dates=True)

#pega dados quando a boia foi para agua
dd = dd['2016-06-24':]

#carrega os dados do geoforce
gc = pd.read_csv(pathname + 'Geoforce_BMOBR06_C.csv',sep=',',parse_dates=['date'],index_col=['date'])
gd = pd.read_csv(pathname + 'Geoforce_BMOBR06_D.csv',sep=',',parse_dates=['date'],index_col=['date'])

#corrige utc para local nos dados do geoforce
gc.index = gc.index - datetime.timedelta(hours=3)
gd.index = gd.index - datetime.timedelta(hours=3)

#converte posicoes para UTM
aux_dd = np.array([utm.from_latlon(dd.lat[i],dd.lon[i]) for i in range(len(dd))])
aux_gc = np.array([utm.from_latlon(gc.lat[i],gc.lon[i]) for i in range(len(gc))])
aux_gd = np.array([utm.from_latlon(gd.lat[i],gd.lon[i]) for i in range(len(gd))])

dd['lonu'],dd['latu'] = aux_dd[:,[0,1]].T
gc['lonu'],gc['latu'] = aux_gc[:,[0,1]].T
gd['lonu'],gd['latu'] = aux_gd[:,[0,1]].T

#data paras plotagens de contorno
dataplotx = list(np.linspace(0,len(dd)-1,10).astype(int)) #range(0,len(dd),intervalo)
dataploty = [dd.index[i].strftime('%Y/%m/%d \n %Hh') for i in dataplotx]

#arruma valores de consumo (divide por 100)
dd['con'] = dd.con * 0.01

#magnitude da corrente de mm/s para m/s
dd[['mag1','mag2','mag3']] = dd[['mag1','mag2','mag3']] / 1000

# #consistencia dos dados
# dd.ix[pl.find(dd.mag1 < 0),['mag1','dir1']] = np.nan
# dd.ix[pl.find(dd.mag2 < 0),['mag2','dir2']] = np.nan
# dd.ix[pl.find(dd.mag3 < 0),['mag3','dir3']] = np.nan
# dd.ix[pl.find((dd.tsup < 12) | (dd.tsup > 29)),['tsup']] = np.nan


dd['u1'] = dd.mag1 * np.sin(np.deg2rad(dd.dir1))
dd['v1'] = dd.mag1 * np.cos(np.deg2rad(dd.dir1))
dd['u2'] = dd.mag2 * np.sin(np.deg2rad(dd.dir2))
dd['v2'] = dd.mag2 * np.cos(np.deg2rad(dd.dir2))
dd['u3'] = dd.mag3 * np.sin(np.deg2rad(dd.dir3))
dd['v3'] = dd.mag3 * np.cos(np.deg2rad(dd.dir3))

#cria array com mag, u e v do ADCP
mag = np.flipud(np.array(dd[['mag1','mag2','mag3']].T))
u = np.flipud(np.array(dd[['u1','u2','u3']].T))
v = np.flipud(np.array(dd[['v1','v2','v3']].T))

#cria array com temp dos sbe - array com 12, coloca nan em 0 e -1 - apenas para 
#arrumar o grafico
sbe = np.flipud(np.array(dd[['tsbe10','tsbe10','tsbe20','tsbe30','tsbe40','tsbe50',
	'tsbe60','tsbe70','tsbe80','tsbe90','tsbe100','tsbe10']].T))
sbe[[0,-1],:] = np.nan

#cria array de pressao dos sbe
psbe = np.nan * np.ones(sbe.shape)
psbe[0,:] = dd.psbe10
psbe[3,:] = dd.psbe40
psbe[6,:] = dd.psbe70
psbe[-1,:] = dd.psbe100

#calcula distancia entre pontos (em kilometros)
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

dist_km = np.array([haversine(dd.lon[i],dd.lat[i],dd.lon[i+1],dd.lat[i+1]) for i in range(len(dd)-1)])
dist = dist_km * 1000

### figuras ###

pl.figure(figsize=(10,12),facecolor='w')
ax1 = pl.subplot2grid((3,1), (0,0), colspan=3)
ax1.plot(dd.index[1:],dist,'b-', alpha=0.4)
ax1.plot(dd.index[1:],dist,'g.', alpha=0.5)
ax1.plot(dd.index[-24:],dist[-24:],'r-', alpha=0.6)
ax1.set_title(str(dd.index[-1]))
pl.xticks(rotation=10)
ax1.set_ylabel('Distancia (m)')
ax1.set_ylim(0,200)
pl.grid()
ax2 = pl.subplot2grid((3,1), (1,0), rowspan=2)
ax2.plot(dd.lonu,dd.latu,'b-', alpha=0.3)
ax2.plot(dd.lonu[-24:],dd.latu[-24:],'r-', alpha=0.6)
# ax2.plot(gc.lonu[-3:],gc.latu[-3:],'k*') #geoforce A
# ax2.plot(gd.lonu[-3:],gd.latu[-3:],'k*') #geoforce B
# ax2.text(gc.lonu[-3],gc.latu[-3],str(gc.index[-3])[0:-6]+'h')
# ax2.text(gc.lonu[-2],gc.latu[-2],str(gc.index[-2])[0:-6]+'h')
# ax2.text(gc.lonu[-1],gc.latu[-1],str(gc.index[-1])[0:-6]+'h')
ax = pl.gca()
ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax2.plot(dd.lonu,dd.latu,'.', color='g', alpha=0.5)
ax2.plot(dd.lonu[-1],dd.latu[-1],'ro')
ax2.set_xlabel('Longitude (UTM)')
ax2.set_ylabel('Latitude (UTM)')
# ax2.set_ylim(7342000,7344000)
# ax2.set_xlim(260500, 262500)
# ax2.set_axes('equal')
ax2.set_aspect('equal', adjustable='box')
pl.grid()
pl.savefig(pathfig + 'loc.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.bat,'-o')
pl.title(str(dd.index[-1]))
pl.xticks(rotation=10)
pl.ylabel('Bateria (V)')
pl.legend(['Bat'],loc=2)
pl.grid()
pl.twinx()
pl.plot(dd.index,dd.con,'-ro')
pl.ylabel('Consumo (W)')
pl.legend(['Con'],loc=1)
pl.savefig(pathfig + 'batcon.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.tdl,'-o')
pl.title(str(dd.index[-1]))
pl.xticks(rotation=10)
pl.ylabel('Temperatura do data logger (graus Celsius)')
pl.grid()
pl.savefig(pathfig + 'tdl.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.ws,'-o')
pl.title(str(dd.index[-1]))
pl.ylim(0,20)
pl.xticks(rotation=10)
pl.ylabel('Intensidade do vento (m/s)')
pl.grid()
pl.savefig(pathfig + 'ws.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.wd,'o')
pl.title(str(dd.index[-1]))
pl.xticks(rotation=10)
pl.yticks(range(0,360+45,45))
pl.ylim(0,360)
pl.ylabel('Direcao do vento (m/s)')
pl.grid()
pl.savefig(pathfig + 'wd.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.ate,'-bo')
pl.plot(dd.index,dd.tsup,'-ro')
pl.title(str(dd.index[-1]))
pl.ylim(20,30)
pl.legend(['Ar','Agua'])
pl.xticks(rotation=10)
pl.ylabel('Temperatura do ar / agua (graus Celsius)')
pl.grid()
pl.savefig(pathfig + 'awt.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.rh,'-o')
pl.title(str(dd.index[-1]))
pl.ylim(50,100)
pl.xticks(rotation=10)
pl.ylabel('Umidade relativa (%)')
pl.grid()
pl.savefig(pathfig + 'rh.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.bp,'-o')
pl.title(str(dd.index[-1]))
pl.xticks(rotation=10)
pl.ylabel('Pressao atmosferica (hPa)')
pl.grid()
pl.savefig(pathfig + 'bp.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.tsup,'-o')
pl.title(str(dd.index[-1]))
pl.ylim(20,30)
pl.xticks(rotation=10)
pl.ylabel('Temperatura da agua a 5 m (ADCP) (graus Celsius)')
pl.grid()
pl.savefig(pathfig + 'tsup.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.mag1,'-o')
pl.title(str(dd.index[-1]))
pl.ylim(0,1)
pl.xticks(rotation=10)
pl.ylabel('Intensidade da corrente a 25 m (m/s)')
pl.grid()
pl.savefig(pathfig + 'mag1.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.dir1,'o')
pl.title(str(dd.index[-1]))
pl.yticks(range(0,360+45,45))
pl.ylim(0,360)
pl.xticks(rotation=10)
pl.ylabel('Direcao da corrente a 25 m (graus Celsius)')
pl.grid()
pl.savefig(pathfig + 'dir1.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.mag2,'-o')
pl.title(str(dd.index[-1]))
pl.ylim(0,1)
pl.xticks(rotation=10)
pl.ylabel('Intensidade da corrente a 263 m (m/s)')
pl.grid()
pl.savefig(pathfig + 'mag2.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.dir2,'o')
pl.title(str(dd.index[-1]))
pl.yticks(range(0,360+45,45))
pl.ylim(0,360)
pl.xticks(rotation=10)
pl.ylabel('Direcao da corrente a 263 m (graus Celsius)')
pl.grid()
pl.savefig(pathfig + 'dir2.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.mag3,'-o')
pl.title(str(dd.index[-1]))
pl.ylim(0,1)
pl.xticks(rotation=10)
pl.ylabel('Intensidade da corrente a 280 m (m/s)')
pl.grid()
pl.savefig(pathfig + 'mag3.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.dir3,'o')
pl.title(str(dd.index[-1]))
pl.yticks(range(0,360+45,45))
pl.ylim(0,360)
pl.xticks(rotation=10)
pl.ylabel('Direcao da corrente a 280 m (graus Celsius)')
pl.grid()
pl.savefig(pathfig + 'dir3.png')

fig = pl.figure(figsize=(12,7),facecolor='w')
ax = fig.add_subplot(111)
ax.set_title(str(dd.index[-1]))
con = ax.contourf(mag,np.arange(0,1,0.001),color='k')
pl.colorbar(con,label=r'ms$^{-1}$')
qwind = ax.quiver(u, v, units='xy', scale=0.05, headwidth=0, pivot='tail', width=0.25, linewidths=(0.001,), edgecolors='k', color='k', alpha=1)
pl.xticks(dataplotx,dataploty,rotation=10)
pl.yticks([0,1,2],[-280,-268,-25])
pl.ylabel('Intensidade e Direcao das Correntes (m/s e graus)')
pl.axis('tight')
pl.ylim(-0.2,2.3)
pl.quiverkey(qwind,100,2.15,1,''.ljust(5) + r'1 ms$^{-1}$',coordinates='data')
pl.savefig(pathfig + 'adcp.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.subplot(311)
pl.plot(dd.index,dd.hs,'-o')
pl.title(str(dd.index[-1]))
pl.xticks(visible=False)
pl.ylabel('Hs (m)')
pl.ylim(0,6)
pl.grid()
pl.subplot(312)
pl.plot(dd.index,dd.tp,'-o')
pl.xticks(visible=False)
pl.ylabel('Tp (s)')
pl.ylim(0,20)
pl.grid()
pl.subplot(313)
pl.plot(dd.index,dd.dp,'-o')
pl.ylabel('Dp (graus)')
pl.yticks(range(0,360+45,45))
pl.ylim(0,360)
pl.xticks(rotation=10)
pl.grid()
pl.savefig(pathfig + 'onda.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,-dd.psbe10+10)
pl.plot(dd.index,-dd.psbe40+40)
pl.plot(dd.index,-dd.psbe70+70)
pl.plot(dd.index,-dd.psbe100+100)
pl.grid()
pl.legend(['10 m','100 m'])
pl.ylim(-20,20)
pl.xticks(rotation=10)
pl.ylabel('Pressao SBEs (dbar)')
pl.savefig(pathfig + 'psbe.png')

pl.figure(figsize=(12,7),facecolor='w')
pl.contourf(sbe,np.arange(15,30,0.05),color='k')
pl.title(str(dd.index[-1]))
pl.ylabel('Temperatura (graus) / Pressao (dbar) \n Profundidade (m)')
pl.colorbar(label='graus')
pl.ylim(0,11)
pl.xticks(dataplotx,dataploty,rotation=10)
pl.yticks(range(0,11),np.arange(-110,10,10))
pl.twinx()
pl.plot(-psbe.T,'k')
pl.ylim(-110,0)
pl.yticks(visible=False)
pl.savefig(pathfig + 'sbe.png')

pl.figure(figsize=(12,14),facecolor='w')
pl.plot(dd.index,dd.tsbe10,'-')
pl.plot(dd.index,dd.tsbe20,'-')
pl.plot(dd.index,dd.tsbe30,'-')
pl.plot(dd.index,dd.tsbe40,'-')
pl.plot(dd.index,dd.tsbe50,'-')
pl.plot(dd.index,dd.tsbe60,'-')
pl.plot(dd.index,dd.tsbe70,'-')
pl.plot(dd.index,dd.tsbe80,'-')
pl.plot(dd.index,dd.tsbe90,'-')
pl.plot(dd.index,dd.tsbe100,'-')
pl.legend(['10 m','20 m','30 m','40 m','50 m','60 m','70 m','80 m','90 m','100 m'],ncol=5,loc=9)
pl.xticks(rotation=10)
pl.ylim(15,30)
pl.ylabel('Temperatura da agua (graus Celsius)')
pl.grid()
pl.savefig(pathfig + 'tsbe.png')

pl.show()