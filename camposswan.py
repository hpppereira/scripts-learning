'''
Realiza a plotagem dos campos de ondas (Hs, Fp e Dp)
e ventos da grade do ES para o projeto ww3es

Resultados:
ww3es/Geral/modelagem/aguas_rasas/Casos/campos_onda/Data/grid_baciaES/
'''

# Pay attention to the pre-requisites and libraries.
import os
import netCDF4 as nc
from numpy import *
from pylab import *
from matplotlib import dates
import datetime
from datetime import timedelta, datetime
import numpy as np
from mpl_toolkits.basemap import Basemap, shiftgrid, interp
import mpl_toolkits.basemap
import matplotlib.pyplot as plt
from time import strptime
from calendar import timegm
from mpl_toolkits.basemap import cm # Palette and colors for plotting the figures
colormap = cm.GMT_polar
palette = plt.cm.OrRd
palette.set_bad('aqua', 10.0)
import matplotlib.colors as colors
import netCDF4 as nc
import os
import numpy as np
#matplotlib.use('Agg')

plt.close('all')

caso = 200507
diai=7
diaf=8

pathname = os.environ['HOME'] + '/Dropbox/ww3es/Geral/modelagem/aguas_rasas/Casos/campos_onda/' + str(caso) + '/grid_baciaES/'

fhs = nc.Dataset(pathname + 'ww3.'+str(caso)+'_hs.nc','r')
hs = fhs.variables['hs'][:]
ffp = nc.Dataset(pathname + 'ww3.'+str(caso)+'_fp.nc','r')
fp = ffp.variables['fp'][:]
tp = 1 / fp
fdp = nc.Dataset(pathname + 'ww3.'+str(caso)+'_dp.nc','r')
dp = fdp.variables['dp'][:]
fuwnd = nc.Dataset(pathname + 'ww3.'+str(caso)+'_wnd.nc','r')
uwnd = fuwnd.variables['uwnd'][:]
vwnd = fuwnd.variables['vwnd'][:]
ws = np.sqrt(uwnd**2 + vwnd**2)

lon = fhs.variables['longitude'][:]
lat = fhs.variables['latitude'][:]
time = fhs.variables['time'][:]

#data inicial da simulacao
start=datetime(int(str(caso)[0:4]),int(str(caso)[4:6]),01,00,00)
datat = np.array([start + timedelta(hours=i) for i in xrange(0,len(time))])
data = datat.astype(str)
datai = [data[i][:4]+data[i][5:7]+data[i][8:10]+data[i][11:13] for i in range(len(data))]

levhs = [0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.5,3,3.5,4,4.5,5,6,7]
levtp = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
levwnd = range(31)

#para plotagem lon_0 e lat_0 eh o centro do mapa
if lon[0] < 0 and lon[-1] <= 0:
	lon_0=-(abs(lon[-1])+abs(lon[0]))/2.0
else:
	lon_0=(lon[0]+lon[-1])/2.0

if lat[0] < 0 and lat[-1] <= 0:
	lat_0=-(abs(lat[-1])+abs(lat[0]))/2.0
else:
	lat_0=(lat[0]+lat[-1])/2.0

#subdivisao para o quiver
sk = 7 # onda
skw = 7 #vento
for k in range((diai-1)*24,diaf*24,6): #len(time)):

	print str(k)

	# Taking direction components (from which the waves are coming)
	dp[k,:,:] = mod(dp[k,:,:],360)
	U = -1*np.sin(dp[k,:,:]*np.pi/180) 
	V = -1*np.cos(dp[k,:,:]*np.pi/180)
	# U[m[k,:,:]<0.01]=0
	# V[m[k,:,:]<0.01]=0
	uw = uwnd[k,:,:]
	vw = vwnd[k,:,:]


	##########################################################################################
	#Hs x Dp
	##########################################################################################
	fig=plt.figure(figsize=(7,6))

	map = Basemap(llcrnrlat=lat[0],urcrnrlat=lat[-1],\
	llcrnrlon=lon[40],urcrnrlon=lon[-40],\
	rsphere=(5378137.00,6356752.3142),\
	resolution='h',area_thresh=1000.,projection='cyl',\
	lat_1=lat[0],lon_1=lon[0],lat_0=lat_0,lon_0=lon_0)

	[mnlon,mnlat]=np.meshgrid(lon,lat)

	xx, yy = map(mnlon,mnlat)
	map.contourf(xx,yy,hs[k,:,:],levhs,cmap=plt.cm.jet,extend="max")
	plt.plot(-39.6917,-19.5372,'ko',markersize=6);text(-39.6917,-19.5372,'Cacimbas',fontsize=11)
	plt.plot(-39.5358,-19.9538,'ko',markersize=6);text(-39.5358,-19.9538,'BM02',fontsize=11)
	map.drawmeridians(np.arange(round(lon.min()),round(lon.max()),2),labels=[0,0,0,1],linewidth=0.3,fontsize=7)
	map.drawparallels(np.arange(round(lat[0]),round(lat.max()),2),labels=[1,0,0,0],linewidth=0.3,fontsize=7)
	ax = plt.gca()
	pos = ax.get_position()
	l, b, w, h = pos.bounds
	cax = plt.axes([l+0.07, b-0.05, w-0.15, 0.025]) # setup colorbar axes.
	cbar = plt.colorbar(cax=cax, orientation='horizontal') # draw colorbar
	cbar.ax.text(0.5,3.5,'Altura Significativa (m) e Direcao  ' + datat[k].strftime("%d-%m-%Y %H:%M:%S") + 'Z', fontsize=11,va='top',ha='center')
	plt.axes(ax)  # make the original axes current again

	map.quiver(xx[:-1:sk,:-1:sk],yy[:-1:sk,:-1:sk],U[:-1:sk,:-1:sk],V[:-1:sk,:-1:sk],width=0.002,scale=40)

	map.fillcontinents(color='grey')
	map.drawcoastlines(color='white',linewidth=0.5)
	map.drawcountries(linewidth=0.5)
	map.drawstates(linewidth=0.2)

	savefig(pathname + '/fig/campo_hsdp_'+str(datai[k])+'.jpg', dpi=None, facecolor='w', edgecolor='w',
	orientation='portrait', papertype=None, format='jpg',
	transparent=False, bbox_inches=None, pad_inches=0.1)

	savefig(pathname + '/fig/campo_hsdp_'+str(datai[k])+'.eps', dpi=1200, facecolor='w', edgecolor='w',
		orientation='portrait',format='eps') 


	# ##########################################################################################
	# #Tp x Dp
	# ##########################################################################################
	# fig=plt.figure(figsize=(7,6))

	# map = Basemap(llcrnrlat=lat[0],urcrnrlat=lat[-1],\
	# llcrnrlon=lon[40],urcrnrlon=lon[-40],\
	# rsphere=(6378137.00,6356752.3142),\
	# resolution='h',area_thresh=1000.,projection='cyl',\
	# lat_1=lat[0],lon_1=lon[0],lat_0=lat_0,lon_0=lon_0)

	# [mnlon,mnlat]=np.meshgrid(lon,lat)

	# xx, yy = map(mnlon,mnlat)
	# map.contourf(xx,yy,tp[k,:,:],levtp,cmap=plt.cm.jet,extend="max")
	# plt.plot(-39.6917,-19.5372,'ko',markersize=6);text(-39.6917,-19.5372,'Cacimbas',fontsize=11)
	# plt.plot(-39.5358,-19.9538,'ko',markersize=6);text(-39.5358,-19.9538,'BM02',fontsize=11)
	# map.drawmeridians(np.arange(round(lon.min()),round(lon.max()),2),labels=[0,0,0,1],linewidth=0.3,fontsize=7)
	# map.drawparallels(np.arange(round(lat[0]),round(lat.max()),2),labels=[1,0,0,0],linewidth=0.3,fontsize=7)
	# ax = plt.gca()
	# pos = ax.get_position()
	# l, b, w, h = pos.bounds
	# cax = plt.axes([l+0.07, b-0.05, w-0.15, 0.025]) # setup colorbar axes.
	# cbar = plt.colorbar(cax=cax, orientation='horizontal') # draw colorbar
	# cbar.ax.text(0.5,3.5,'Periodo de Pico (s) e Direcao  ' + datat[k].strftime("%d-%m-%Y %H:%M:%S") + 'Z', fontsize=11,va='top',ha='center')
	# plt.axes(ax)  # make the original axes current again

	# map.quiver(xx[:-1:sk,:-1:sk],yy[:-1:sk,:-1:sk],U[:-1:sk,:-1:sk],V[:-1:sk,:-1:sk],width=0.002,scale=40)

	# map.fillcontinents(color='grey')
	# map.drawcoastlines(color='white',linewidth=0.5)
	# map.drawcountries(linewidth=0.5)
	# map.drawstates(linewidth=0.2)

	# #plt.title('Altura Significativa (m) e Direcao / Significant Wave Height and Direction      ' + data[k] + 'Z', fontsize=7)

	# savefig(pathname + '/fig/campo_tpdp_'+str(datai[k])+'.jpg', dpi=None, facecolor='w', edgecolor='w',
	# orientation='portrait', papertype=None, format='jpg',
	# transparent=False, bbox_inches=None, pad_inches=0.1)

	# savefig(pathname + '/fig/campo_tpdp_'+str(datai[k])+'.eps', dpi=1200, facecolor='w', edgecolor='w',
	# 	orientation='portrait',format='eps') 


	# ##########################################################################################
	# #Velocidade e Direcao do vento
	# ##########################################################################################
	# fig=plt.figure(figsize=(7,6))

	# map = Basemap(llcrnrlat=lat[0],urcrnrlat=lat[-1],\
	# llcrnrlon=lon[40],urcrnrlon=lon[-40],\
	# rsphere=(6378137.00,6356752.3142),\
	# resolution='h',area_thresh=1000.,projection='cyl',\
	# lat_1=lat[0],lon_1=lon[0],lat_0=lat_0,lon_0=lon_0)

	# [mnlon,mnlat]=np.meshgrid(lon,lat)

	# xx, yy = map(mnlon,mnlat)
	# map.contourf(xx,yy,ws[k,:,:],levtp,cmap=plt.cm.jet,extend="max")
	# plt.plot(-39.6917,-19.5372,'ko',markersize=6);text(-39.6917,-19.5372,'Cacimbas',fontsize=11)
	# plt.plot(-39.5358,-19.9538,'ko',markersize=6);text(-39.5358,-19.9538,'BM02',fontsize=11)
	# map.drawmeridians(np.arange(round(lon.min()),round(lon.max()),2),labels=[0,0,0,1],linewidth=0.3,fontsize=7)
	# map.drawparallels(np.arange(round(lat[0]),round(lat.max()),2),labels=[1,0,0,0],linewidth=0.3,fontsize=7)
	# ax = plt.gca()
	# pos = ax.get_position()
	# l, b, w, h = pos.bounds
	# cax = plt.axes([l+0.07, b-0.05, w-0.15, 0.025]) # setup colorbar axes.
	# cbar = plt.colorbar(cax=cax, orientation='horizontal') # draw colorbar
	# cbar.ax.text(0.5,3.5,'Velocidade (m/s) e Direcao do Vento  ' + datat[k].strftime("%d-%m-%Y %H:%M:%S") + 'Z', fontsize=11,va='top',ha='center')
	# plt.axes(ax)  # make the original axes current again

	# map.quiver(xx[:-1:skw,:-1:skw],yy[:-1:skw,:-1:skw],uw[:-1:skw,:-1:skw],vw[:-1:skw,:-1:skw],width=0.002,scale=300)

	# map.fillcontinents(color='grey')
	# map.drawcoastlines(color='white',linewidth=0.5)
	# map.drawcountries(linewidth=0.5)
	# map.drawstates(linewidth=0.2)

	# #plt.title('Altura Significativa (m) e Direcao / Significant Wave Height and Direction      ' + data[k] + 'Z', fontsize=7)

	# savefig(pathname + '/fig/campo_wind_'+str(datai[k])+'.jpg', dpi=None, facecolor='w', edgecolor='w',
	# orientation='portrait', papertype=None, format='jpg',
	# transparent=False, bbox_inches=None, pad_inches=0.1)

	# savefig(pathname + '/fig/campo_wind_'+str(datai[k])+'.eps', dpi=1200, facecolor='w', edgecolor='w',
	# 	orientation='portrait',format='eps') 


#plt.show()
