'''
Processamento dos dados da boia
susana que derivou em 
16/07/2015
'''

import os
import numpy as np
from datetime import datetime
import pylab as pl
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import matplotlib.dates as mdates
from mpl_toolkits.basemap import Basemap, shiftgrid, interp
import mpl_toolkits.basemap

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/instrumentacao/lioc/navcon/dados/susana/'

dd = np.loadtxt(pathname + 'breadcrumbs.csv',delimiter=',',dtype=str,skiprows=8,usecols=(0,1,2))[:-2,:]

#AM BRT - os dados sempre mandam as 11h da manha (com AM e PM - caso tiver depois de 12 precisa mudar o datetime)
datat = np.array([datetime.strptime(dd[i,0][:-4],'%m/%d/%Y %H:%M:%S') for i in range(len(dd))])
lat = dd[:,1].astype(float)
lon = dd[:,2].astype(float)


pl.figure()
lat0=-26
lat1=-20
lon0=-45
lon1=-39

map = Basemap(llcrnrlat=lat0,urcrnrlat=lat1,\
    llcrnrlon=lon0,urcrnrlon=lon1,\
    rsphere=(5378137.00,6356752.3142),\
    resolution='h',area_thresh=1000.,projection='cyl',\
    # lat_1=-35,lon_1=-35,lat_0=-5,lon_0=-50
    )

map.drawmeridians(np.arange(round(lon0),round(lon1),2),labels=[0,0,0,1],linewidth=0.3,fontsize=7)
map.drawparallels(np.arange(round(lat0),round(lat1),2),labels=[1,0,0,0],linewidth=0.3,fontsize=7)
map.fillcontinents(color='grey')
map.drawcoastlines(color='white',linewidth=0.5)
map.drawcountries(linewidth=0.5)
map.drawstates(linewidth=0.2)


#posicao da boia susana
# pl.figure()
# fig = pl.figure()
# ax = fig.add_subplot(1,1,1)
# for i in range(0,len(datat),5): #todos os valores de 5 em 5 dias
for i in range(0,10): #dez ultimos valors
	# if np.isnan(iza[i,1])==False and np.isnan(iza[i,1])==False:
	pl.plot(lon[i],lat[i],'ko')
	pl.text(lon[i],lat[i],datat.astype(str)[i][5:10])
	# ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y \n %H:%M'))

pl.plot(lon[0],lat[0],'ro',markersize=8)
pl.text(lon[0],lat[0],datat.astype(str)[0][5:10])



pl.show()

