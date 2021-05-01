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

pathname = os.environ['HOME'] + '/Dropbox/database/historical/buoys/remo/CF3_BMOBR06_2016Jun/op/'
pathfig  = os.environ['HOME'] + '/Dropbox/atmosmarine/websites/cf3jun16/img/'

#carrega os dados da boia
dd = pd.read_csv(pathname + 'cf3jun16.csv', index_col='date', parse_dates=True)

#pega dados quando a boia foi para agua
#dd = dd['2016-11-05 20:00':]

#carrega dados da previsao 
nww3 = pd.read_csv(os.environ['HOME'] + '/Dropbox/database/forecast/nww3/NWW3_LIOc_CF01.csv',
        sep=',', parse_dates=['date'], index_col=['date'])

#carrega os dados do geoforce
#gc = pd.read_csv(pathname + 'Geoforce_BMOBR06_C.csv',sep=',',parse_dates=['date'],index_col=['date'])
#gd = pd.read_csv(pathname + 'Geoforce_BMOBR06_D.csv',sep=',',parse_dates=['date'],index_col=['date'])

#corrige utc para local nos dados do geoforce
#gc.index = gc.index - datetime.timedelta(hours=3)
#gd.index = gd.index - datetime.timedelta(hours=3)

#converte posicoes para UTM
aux_dd = np.array([utm.from_latlon(dd.lat[i],dd.lon[i]) for i in range(len(dd))])
#aux_gc = np.array([utm.from_latlon(gc.lat[i],gc.lon[i]) for i in range(len(gc))])
#aux_gd = np.array([utm.from_latlon(gd.lat[i],gd.lon[i]) for i in range(len(gd))])

dd['lonu'],dd['latu'] = aux_dd[:,[0,1]].T
#gc['lonu'],gc['latu'] = aux_gc[:,[0,1]].T
#gd['lonu'],gd['latu'] = aux_gd[:,[0,1]].T

#data paras plotagens de contorno
dataplotx = list(np.linspace(0,len(dd)-1,10).astype(int)) #range(0,len(dd),intervalo)
dataploty = [dd.index[i].strftime('%Y/%m/%d \n %Hh') for i in dataplotx]

#arruma valores de consumo (divide por 100)
dd['con'] = dd.con * 0.01

#magnitude da corrente de mm/s para m/s
dd['mag1'] = dd['mag1'] / 1000

# #consistencia dos dados
# dd.ix[pl.find(dd.mag1 < 0),['mag1','dir1']] = np.nan
# dd.ix[pl.find(dd.mag2 < 0),['mag2','dir2']] = np.nan
# dd.ix[pl.find(dd.mag3 < 0),['mag3','dir3']] = np.nan
# dd.ix[pl.find((dd.tsup < 12) | (dd.tsup > 29)),['tsup']] = np.nan


dd['u1'] = dd.mag1 * np.sin(np.deg2rad(dd.dir1))
dd['v1'] = dd.mag1 * np.cos(np.deg2rad(dd.dir1))
#dd['u2'] = dd.mag2 * np.sin(np.deg2rad(dd.dir2))
#dd['v2'] = dd.mag2 * np.cos(np.deg2rad(dd.dir2))
#dd['u3'] = dd.mag3 * np.sin(np.deg2rad(dd.dir3))
#dd['v3'] = dd.mag3 * np.cos(np.deg2rad(dd.dir3))

#cria array com mag, u e v do ADCP
#mag = np.flipud(np.array(dd[['mag1','mag2','mag3']].T))
#u = np.flipud(np.array(dd[['u1','u2','u3']].T))
#v = np.flipud(np.array(dd[['v1','v2','v3']].T))

#cria array com temp dos sbe - array com 12, coloca nan em 0 e -1 - apenas para 
#arrumar o grafico
sbe = np.flipud(np.array(dd[['tsbe10','tsbe10','tsbe20','tsbe30','tsbe40','tsbe50',
	'tsbe60','tsbe70','tsbe80','tsbe90','tsbe100','tsbe10']].T))
sbe[[0,-1],:] = np.nan

#cria array de pressao dos sbe
psbe = np.nan * np.ones(sbe.shape)
psbe[0,:] = dd.psbe10
#psbe[3,:] = dd.psbe40
#psbe[6,:] = dd.psbe70
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

pl.figure(figsize=(11,12),facecolor='w')
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
ax2.set_ylim(7342000, 7344500)
ax2.set_xlim(260500, 263000)
# ax2.set_axes('equal')
# ax2.set_ylim(7364560,7365100)
# ax2.set_xlim(236282 , 236800)
ax2.set_aspect('equal', adjustable='box')
pl.grid()
pl.savefig(pathfig + 'loc.png', bbox_inches='tight')

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
pl.savefig(pathfig + 'batcon.png', bbox_inches='tight')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.tdl,'-o')
pl.title(str(dd.index[-1]))
pl.xticks(rotation=10)
pl.ylabel('Temperatura do data logger (graus Celsius)')
pl.grid()
pl.savefig(pathfig + 'tdl.png', bbox_inches='tight')

pl.figure(figsize=(12,9),facecolor='w')
pl.subplot(211)
pl.plot(dd.index,dd.ws,'-o')
pl.title(str(dd.index[-1]))
pl.ylim(0,20)
pl.xticks(rotation=10)
pl.ylabel('Intensidade do vento (m/s)')
pl.grid()
pl.subplot(212)
pl.plot(dd.index,dd.wd,'o')
#pl.title(str(dd.index[-1]))
pl.xticks(rotation=10)
pl.yticks(range(0,360+45,45))
pl.ylim(0,360)
pl.ylabel('Direcao do vento (m/s)')
pl.grid()
pl.savefig(pathfig + 'wind.png', bbox_inches='tight')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.ate,'-bo')
pl.plot(dd.index,dd.tsup,'-ro')
pl.title(str(dd.index[-1]))
pl.ylim(15,30)
pl.legend(['Ar','Agua'])
pl.xticks(rotation=10)
pl.ylabel('Temperatura do ar / agua (graus Celsius)')
pl.grid()
pl.savefig(pathfig + 'awt.png', bbox_inches='tight')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.rh,'-o')
pl.title(str(dd.index[-1]))
pl.ylim(50,100)
pl.xticks(rotation=10)
pl.ylabel('Umidade relativa (%)')
pl.grid()
pl.savefig(pathfig + 'rh.png', bbox_inches='tight')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.bp,'-o')
pl.title(str(dd.index[-1]))
pl.xticks(rotation=10)
pl.ylim(1000,1035)
pl.ylabel('Pressao atmosferica (hPa)')
pl.grid()
pl.savefig(pathfig + 'bp.png', bbox_inches='tight')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,dd.tsup,'-o')
pl.title(str(dd.index[-1]))
pl.ylim(20,30)
pl.xticks(rotation=10)
pl.ylabel('Temperatura da agua a 5 m (ADCP) (graus Celsius)')
pl.grid()
pl.savefig(pathfig + 'tsup.png', bbox_inches='tight')

pl.figure(figsize=(12,9),facecolor='w')
pl.subplot(211)
pl.plot(dd.index,dd.mag1,'-o')
pl.title(str(dd.index[-1]))
pl.ylim(0,1)
pl.xticks(rotation=10)
pl.ylabel('Int. corrente 40 m (m/s)')
pl.grid()
pl.subplot(212)
pl.plot(dd.index,dd.dir1,'o')
#pl.title(str(dd.index[-1]))
pl.yticks(range(0,360+45,45))
pl.ylim(0,360)
pl.xticks(rotation=10)
pl.ylabel('Dir. corrente 40 m (C)')
pl.grid()
pl.savefig(pathfig + 'curr.png', bbox_inches='tight')

pl.figure(figsize=(12,7),facecolor='w')
pl.subplot(311)
pl.plot(dd.index,dd.hs,'.', label='GX4')
# pl.plot(dd.index,dd.hs_ax,'.', label='Axys')
pl.plot(nww3.index,nww3.hs,'.', label='NWW3')
pl.xlim(dd.index[0],dd.index[-1])
pl.legend(ncol=3)
pl.title(str(dd.index[-1]))
pl.xticks(visible=False)
pl.ylabel('Hs (m)')
pl.ylim(0,8)
pl.grid()
pl.subplot(312)
pl.plot(dd.index,dd.tp,'.', label='GX4')
# pl.plot(dd.index,dd.tp_ax,'.', label='Axys')
pl.plot(nww3.index,nww3.tp,'.', label='NWW3')
pl.xlim(dd.index[0],dd.index[-1])
pl.xticks(visible=False)
pl.ylabel('Tp (s)')
pl.ylim(0,20)
pl.grid()
pl.subplot(313)
pl.plot(dd.index,dd.dp,'.', label='GX4')
# pl.plot(dd.index,dd.dp_ax,'.', label='Axys')
pl.plot(nww3.index,nww3.dp,'.', label='NWW3')
pl.xlim(dd.index[0],dd.index[-1])
pl.ylabel('Dp (graus)')
pl.yticks(range(0,360+45,45))
pl.ylim(0,360)
pl.xticks(rotation=10)
pl.grid()
pl.savefig(pathfig + 'wave.png', bbox_inches='tight')

pl.figure(figsize=(12,7),facecolor='w')
pl.plot(dd.index,-dd.psbe10+10)
#pl.plot(dd.index,-dd.psbe40+40)
#pl.plot(dd.index,-dd.psbe70+70)
pl.plot(dd.index,-dd.psbe100+100)
pl.grid()
pl.legend(['10 m','100 m'])
pl.ylim(-20,20)
pl.xticks(rotation=10)
pl.ylabel('Pressao SBEs (dbar)')
pl.savefig(pathfig + 'psbe.png', bbox_inches='tight')

pl.figure(figsize=(12,11),facecolor='w')
pl.contourf(sbe,np.arange(15,30,0.05),color='k')
pl.title(str(dd.index[-1]))
pl.ylabel('Temperatura (graus) / Pressao (dbar) \n Profundidade (m)')
pl.colorbar(label='graus', orientation='horizontal')
pl.ylim(0,11)
pl.xticks(dataplotx,dataploty,rotation=10)
pl.yticks(range(0,11),np.arange(-110,10,10))
pl.twinx()
pl.plot(-psbe.T,'k')
pl.ylim(-110,0)
pl.yticks(visible=False)
pl.savefig(pathfig + 'sbe.png', bbox_inches='tight')

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
pl.savefig(pathfig + 'tsbe.png', bbox_inches='tight')

pl.show()
