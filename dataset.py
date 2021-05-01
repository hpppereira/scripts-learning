# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
import xray
import pandas as pd
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

plt.close('all')


#DATADIR = '/Users/Phellipe/Studies/Masters/Project/Thesis/Data'
#FIGDIR  = '/Users/Phellipe/Studies/Masters/Project/Thesis/Text/Chapters/Chapter_3/fig_method/'

DATADIR = os.environ['HOME'] + '/Dropbox/publ/waveobs/dados/'

#### Bathymetry ########################################################################
########################################################################################

#### Rio de Janeiro Shelf - Nautical Charts
#grd = DATADIR + 'rio_grd.nc'
#grd = xray.open_dataset(grd)
#Gtopo = grd['hraw'].values
#Glon = grd['lon_rho'].values
#Glat = grd['lat_rho'].values

#### SE Shelf - Etopo1
#Alims = [-48.95, -38.54, -25.14, -18.15]
Alims = [-56., -33, -36.00, 2.00]
etopo = DATADIR + 'ETOPO-REMO.nc'
etopo = xray.open_dataset(etopo).sel( lon=slice(Alims[0],Alims[1] ), lat=slice(Alims[2],Alims[3]) )
Etopo = etopo.z.values
Elon, Elat = np.meshgrid( etopo.lon, etopo.lat )


#### Station coordinates ###############################################################
########################################################################################

# # ASCAT ###############################################################################
# Ascat = os.path.join(DATADIR, 'ascat_Daily_2008-2015_pcse.nc')
# Ascat = xray.open_dataset(Ascat)

# Alims = [-48.95, -38.54, -25.14, -18.15]
# Ascat = Ascat.sel( longitude=slice(Alims[0],Alims[1] ), latitude=slice(Alims[2],Alims[3]) )
# alon, alat = Ascat.longitude.values, Ascat.latitude.values 
# Alon, Alat = np.meshgrid( alon, alat )

# xmin, xmax = alon.min(), alon.max()
# ymin, ymax = alat.min(), alat.max()

# xs = [xmin,xmax,xmax,xmin,xmin]
# ys = [ymin,ymin,ymax,ymax,ymin]

#henrique
#xs = [-48.95, -38.54, -25.14, -18.15]
#ys = [-48.95, -38.54, -25.14, -18.15]


# # SIODOC ###############################################################################
# janis_wts = os.path.join(DATADIR, 'janis_wtsmeta_filter.pkl')
# siodoc = pd.read_pickle(janis_wts).coordinate
# sx, sy = siodoc.lon.mean(), siodoc.lat.mean()

#henrique
sx, sy = [-47.4,-28.5]

# INMET ###############################################################################
pnboia = {'riogrande'  : [-31.566, -49.966],
          'florian'    : [-28.500, -47.366],
          'santos'     : [-25.283, -44.933],
          'bguan'      : [-22.924, -43.150], 
          'cabofrio'   : [-22.995, -42.187], 
          'vitoria'    : [-20.278, -39.727], 
          'portoseg'   : [-18.151, -37.944], 
          'recife'     : [-08.149, -34.560], 
          'fortaleza'  : [-02.987, -38.819],
          'barranorte' : [+01.094, -46.350] }

ay, ax = pnboia['riogrande']
by, bx = pnboia['florian']
cy, cx = pnboia['santos']
dy, dx = pnboia['bguan']
ey, ex = pnboia['cabofrio']
fy, fx = pnboia['vitoria']
gy, gx = pnboia['portoseg']
hy, hx = pnboia['recife']
iy, ix = pnboia['fortaleza']
jy, jx = pnboia['barranorte']



#### Basemap ###########################################################################
########################################################################################

# Remote Sensing area ####################################################################

m1 = Basemap(projection='cyl', resolution='h', llcrnrlon=Alims[0]+.5,\
            llcrnrlat=Alims[2]-.5, urcrnrlon=Alims[1]+.5, urcrnrlat=Alims[3]+.5)

#m1 = Basemap(projection='ortho', resolution='i', lat_0=-25, lon_0=-42, area_thresh=500.0)

# Arraial area ###########################################################################

#Lims = [-45., -41.7, -23.70, -21.4 ]
Lims = [-55.0, -41.0, -33.0, -22.0 ]

m2 = Basemap(projection='cyl', resolution='l', llcrnrlon=Lims[0],\
                        llcrnrlat=Lims[2], urcrnrlon=Lims[1], urcrnrlat=Lims[3])

axmin, axmax = Lims[0], Lims[1]
aymin, aymax = Lims[2], Lims[3]

axs = [axmin,axmax,axmax,axmin,axmin]
ays = [aymin,aymin,aymax,aymax,aymin]

#########################################################################################

fig = plt.figure(figsize=(9,6), facecolor='w')

# Rio de Janeiro Shelf Area (Larger Map) #############################################################

ax1 = fig.add_subplot(111)

m2.drawcoastlines(linewidth=1)
m2.drawstates(linewidth=1, zorder=12)
cs = m2.contour( Elon, Elat, Etopo*-1, [50, 100, 200, 500, 1500, 2500, 3500, 4000], colors='lightgray', linewidth=.7, alpha=0.8 )
cs.clabel(fmt='%i', fontsize=12)

#m2.plot(ax, ay, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=10)

m2.plot(ax, ay, '^', markerfacecolor='dodgerblue', markeredgecolor='k', mew=2, markersize=12)
ax1.text(ax+0.3, ay, 'RIG', fontsize=14)
m2.plot(bx, by, '^', markerfacecolor='dodgerblue', markeredgecolor='k', mew=2, markersize=12)
ax1.text(bx+0.3, by, 'FLN', fontsize=14)
m2.plot(cx, cy, '^', markerfacecolor='dodgerblue', markeredgecolor='k', mew=2, markersize=12)
ax1.text(cx+0.3, cy, 'SAN', fontsize=14)


#m2lons = [ Lims[0], mx, cx, -42.098 ]
#m2lats = [ Lims[2]+.2, sy, -22.13, -22.56, Lims[3]-.2 ]
m2lons = [ax, bx, cx]
m2lats = [ay, by, cy]


m2.drawparallels( m2lats, labels=[1,0,0,0], fmt='%.02f', 
                    linewidth=0.2, fontsize=12, rotation=90, zorder=20)
m2.drawmeridians( m2lons, labels=[0,0,0,1], fmt='%.02f',
                    linewidth=0.2, fontsize=12, zorder=20)


# SE Shelf Area (Smaller Map) #######################################################################

ax2  = fig.add_axes([0.0, 0.365, 0.5, 0.6]) #l,b,w,h

#ax2  = fig.add_axes([0, 0, 0.5, 1]) #l,b,w,h

m1.drawstates(linewidth=1, zorder=12)
m1.fillcontinents(color='w', zorder=11)
m1.drawcoastlines(linewidth=1, zorder=10)
#m1.drawmapboundary(fill_color='w',zorder=9)

cs = m1.contour( Elon, Elat, Etopo*-1, [200, 3000, 4500], colors='lightgray', linewidth=.7, alpha=0.8 )
#cs.clabel(fmt='%i', fontsize=12)

#m1.plot(xs, ys, lw=4, color='k', latlon=True, zorder=2)
m1.plot(axs, ays, lw=2, color='r', linestyle='-.', latlon=True, zorder=13)
#m1.plot(Alon, Alat, 'o', markersize=2, color='k', alpha=0.7, latlon=True, zorder=0)
#cs1 = m1.contour( Elon, Elat, Etopo*-1, [200,200], lw=2, colors='w' )

mk = 6

m1.plot(ax, ay, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=mk, zorder=14)
m1.plot(bx, by, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=mk, zorder=14)
m1.plot(cx, cy, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=mk, zorder=14)
m1.plot(dx, dy, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=mk, zorder=14)
m1.plot(ex, ey, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=mk, zorder=14)
m1.plot(fx, fy, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=mk, zorder=14)
m1.plot(gx, gy, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=mk, zorder=14)
m1.plot(hx, hy, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=mk, zorder=14)
m1.plot(ix, iy, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=mk, zorder=14)
m1.plot(jx, jy, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=mk, zorder=14)


#m1.plot(ax, ay, '^', markerfacecolor='dodgerblue', markeredgecolor='k', mew=2, markersize=12)
#m1.plot(bx, by, '^', markerfacecolor='dodgerblue', markeredgecolor='k', mew=2, markersize=12)
#m1.plot(cx, cy, '^', markerfacecolor='dodgerblue', markeredgecolor='k', mew=2, markersize=12)



### ASCAT & CPTEC Labels
# polylabel = Polygon( [ (alon[-1],alat[0]), (alon[-22],alat[0]),
#                         (alon[-22],alat[3]), (alon[-1],alat[3]) ], 
#                           facecolor='gainsboro', edgecolor='gainsboro',linewidth=3 ) 
# plt.gca().add_patch(polylabel) 
# plt.annotate('ASCAT & CPTEC/INPE', fontweight='bold', fontsize=12,
#                         xy=(0.43, 0.11), xycoords='axes fraction', zorder=4)


m1.drawparallels( [cy, hy], labels=[0,1,1,1], fmt='%.02f', 
                    linewidth=0.2, fontsize=10, rotation=90, zorder=20)
m1.drawmeridians( [cx, hx], labels=[0,0,0,1], fmt='%.02f',
                    linewidth=0.2, fontsize=10, zorder=20)



fig.subplots_adjust(top=0.98, bottom=0.05, left=0.04, right=0.99, wspace=0.2, hspace=0.15)


#fig.savefig('dataset_map_pnboia.png', dpi=200 )
#fig.savefig('dataset_map_pnboia.eps', dpi=200 )
#fig.savefig('fig_OD/dataset.pdf', format='pdf', dpi=1200 )
#fig.savefig('fig_OD/dataset.eps', format='eps', dpi=1200, bbox_inches='tight')
#fig.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/dataset.eps', format='eps', dpi=1200, bbox_inches='tight')
#fig.savefig(os.environ['HOME'] + '/Dropbox/waveobs/latex/fig/dataset.pdf', format='pdf', dpi=1200, bbox_inches='tight')



plt.show()



