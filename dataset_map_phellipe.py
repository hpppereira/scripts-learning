

import os
import numpy as np
import matplotlib.pyplot as plt
import xray
import pandas as pd
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon




DATADIR = '/Users/Phellipe/Studies/Masters/Project/Thesis/Data'
FIGDIR  = '/Users/Phellipe/Studies/Masters/Project/Thesis/Text/Chapters/Chapter_3/fig_method/'


#### Bathymetry ########################################################################
########################################################################################

#### Rio de Janeiro Shelf - Nautical Charts
grd = '/Users/Phellipe/Studies/Masters/Datasets/Bathymetry/rio_grd.nc'
grd = xray.open_dataset(grd)
Gtopo = grd['hraw'].values
Glon = grd['lon_rho'].values
Glat = grd['lat_rho'].values

#### SE Shelf - Etopo1
Alims = [-48.95, -38.54, -25.14, -18.15]
etopo = '/Users/Phellipe/Studies/Masters/Datasets/Bathymetry/etopo1.nc'
etopo = xray.open_dataset(etopo).sel( lon=slice(Alims[0],Alims[1] ), lat=slice(Alims[2],Alims[3]) )
Etopo = etopo.topo.values
Elon, Elat = np.meshgrid( etopo.lon, etopo.lat )

#### Station coordinates ###############################################################
########################################################################################

# ASCAT ###############################################################################
Ascat = os.path.join(DATADIR, 'ascat_Daily_2008-2015_pcse.nc')
Ascat = xray.open_dataset(Ascat)

Alims = [-48.95, -38.54, -25.14, -18.15]
Ascat = Ascat.sel( longitude=slice(Alims[0],Alims[1] ), latitude=slice(Alims[2],Alims[3]) )
alon, alat = Ascat.longitude.values, Ascat.latitude.values 
Alon, Alat = np.meshgrid( alon, alat )

xmin, xmax = alon.min(), alon.max()
ymin, ymax = alat.min(), alat.max()

xs = [xmin,xmax,xmax,xmin,xmin]
ys = [ymin,ymin,ymax,ymax,ymin]

# SIODOC ###############################################################################
janis_wts = os.path.join(DATADIR, 'janis_wtsmeta_filter.pkl')
siodoc = pd.read_pickle(janis_wts).coordinate
sx, sy = siodoc.lon.mean(), siodoc.lat.mean()


# INMET ###############################################################################
inmet = { 'marambaia'  : [-23.05, -43.59],
          'copacabana' : [-22.98, -43.19],
          'arraial'    : [-22.97, -42.02] }

my, mx = inmet['marambaia']
cy, cx = inmet['copacabana']
ay, ax = inmet['arraial']

#### Basemap ###########################################################################
########################################################################################

# Remote Sensing area ####################################################################

m1 = Basemap(projection='cyl', resolution='f', llcrnrlon=Alims[0]+.5,\
            llcrnrlat=Alims[2]-.5, urcrnrlon=Alims[1]+.5, urcrnrlat=Alims[3]+.5)


# Arraial area ###########################################################################

Lims = [-45., -41.7, -23.70, -21.4 ]

m2 = Basemap(projection='cyl', resolution='f', llcrnrlon=Lims[0],\
                        llcrnrlat=Lims[2], urcrnrlon=Lims[1], urcrnrlat=Lims[3])

axmin, axmax = Lims[0], Lims[1]
aymin, aymax = Lims[2], Lims[3]

axs = [axmin,axmax,axmax,axmin,axmin]
ays = [aymin,aymin,aymax,aymax,aymin]

#########################################################################################

fig = plt.figure(figsize=(9,6), facecolor='w')



# Rio de Janeiro Shelf Area (Larger Map) #############################################################

ax1 = fig.add_subplot(111)

m2.drawcoastlines(linewidth=2)
cs = m2.contour( Elon, Elat, Etopo*-1, [50, 100, 125, 150, 200], colors='lightgray', linewidth=.7 )
cs.clabel(fmt='%i', fontsize=12)

m2.plot(sx, sy, 'o', markerfacecolor='k', markeredgecolor='grey', mew=2, markersize=10)
m2.plot(ax, ay, '^', markerfacecolor='dodgerblue', markeredgecolor='k', mew=2, markersize=12)
m2.plot(cx, cy, '^', markerfacecolor='dodgerblue', markeredgecolor='k', mew=2, markersize=12)
m2.plot(mx, my, '^', markerfacecolor='dodgerblue', markeredgecolor='k', mew=2, markersize=12)

m2lons = [ Lims[0], mx, cx, -42.098 ]
m2lats = [ Lims[2]+.2, sy, -22.13, -22.56, Lims[3]-.2 ]

m2.drawparallels( m2lats, labels=[1,0,0,0], fmt='%.02f', 
                    linewidth=0.2, fontsize=12, rotation=90, zorder=20)
m2.drawmeridians( m2lons, labels=[0,0,0,1], fmt='%.02f',
                    linewidth=0.2, fontsize=12, zorder=20)


# SE Shelf Area (Smaller Map) #######################################################################

ax2  = fig.add_axes([0.06, 0.47, 0.47, 0.5]) #l,b,w,h

m1.drawstates(linewidth=1, zorder=12)
m1.fillcontinents(color='w', zorder=11)
m1.drawcoastlines(linewidth=1.5, zorder=10)
m1.drawmapboundary(fill_color='gainsboro',zorder=9)

m1.plot(xs, ys, lw=4, color='k', latlon=True, zorder=2)
m1.plot(axs, ays, lw=2, color='r', linestyle='-.', latlon=True, zorder=13)
m1.plot(Alon, Alat, 'o', markersize=2, color='k', alpha=0.7, latlon=True, zorder=0)
cs1 = m1.contour( Elon, Elat, Etopo*-1, [200,200], lw=2, colors='w' )

### ASCAT & CPTEC Labels
polylabel = Polygon( [ (alon[-1],alat[0]), (alon[-22],alat[0]),
                        (alon[-22],alat[3]), (alon[-1],alat[3]) ], 
                          facecolor='gainsboro', edgecolor='gainsboro',linewidth=3 ) 
plt.gca().add_patch(polylabel) 
plt.annotate('ASCAT & CPTEC/INPE', fontweight='bold', fontsize=12,
                        xy=(0.43, 0.11), xycoords='axes fraction', zorder=4)


m1.drawparallels( (ymin+.35,ymax), labels=[0,1,1,1], fmt='%.02f', 
                    linewidth=0.2, fontsize=12, rotation=90, zorder=20)
m1.drawmeridians( (xmax-.35,-47.65), labels=[0,0,0,1], fmt='%.02f',
                    linewidth=0.2, fontsize=12, zorder=20)




fig.subplots_adjust(top=0.98, bottom=0.05, left=0.04, right=0.99, wspace=0.2, hspace=0.15)

fig.savefig( FIGDIR + 'dataset_map.png', dpi=200 )






