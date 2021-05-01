#
# Routine for reading netcdf (.nc) bathymetry file and creating input text files for Wavewatch III. A particular case applied to ETOPO1 (1 minute). 
# Program thought for Linux/Unix environmental in case of using system calls (os.system). Otherwise it can be run on Windows or Linux. 
# 01/12/2011
# Author:
# Ricardo Martins Campos (PhD student) and Izabel Nogueira (MSc student)
# riwave@gmail.com     izabel.oceanografia@gmail.com
# +55 21 38654845 +55 21 84660434
# ----------------------------------------------------------------------------------------
# Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  
# MotorDePopa Wave Research Group
# Rio de Janeiro - Brazil
# ----------------------------------------------------------------------------------------
# Contributions: Luiz Alexandre Guerra (CENPES/PETROBRAS).
#                ...
# ------------------------------------------------------------------------------------------------------------------------------------

# Pay attention to the pre-requisites and libraries.
from pupynere import NetCDFFile as nc
from pylab import *
from mpl_toolkits.basemap import Basemap, shiftgrid, interp
import mpl_toolkits.basemap
import matplotlib.pyplot as plt



# Pay attention to the pre-requisites and libraries.
import matplotlib
import os
from pupynere import NetCDFFile as nc
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

# Paleta de cores para a plotagem
from mpl_toolkits.basemap import cm
colormap = cm.GMT_polar
palette = plt.cm.jet
palette.set_bad('aqua', 10.0)
import matplotlib.colors as colors



# -----------------------------------------------------------------
#   Defining grid domain, related to the input grid of WW3
# -----------------------------------------------------------------
# Resolution (minutes)
res=4  
# Latitudes: lati (initial) latf (final) - from south to north 
lati=-32.5
latf=-19.5
# Longitudes: loni (initial) lonf (final) - from east to west
loni=-53.0
lonf=-39.0
# Resolution (minutes) for reading netcdf file, due to the great size of matrix which can yield to memory problems
mini=1
# Name of you ETOPO1min global file. Pay attention to the longitude and latitude variable names! That must be 'lon' and 'lat'.
namef='ETOPO-REMO.nc'
# Variable with bathymetry files is called as 'z'. In case of different names, change line 92





# Descriptor file 
fl = open('log_bathymetry.txt', 'w')
fl.write('=========== Bathymetry description ===========\n')
fl.write(' \n')
# Calculating the intervall of meridians paralells
nx=(lonf-loni)/5;
ny=(latf-lati)/5;


# This program was thought to choose between 2 etopo files. If you don't have the second file, please delete the "else" part.

if loni<-70 or lonf>-20 or lati<-50 or latf>10:	


	# Global
	fl.write(' Opened Global ETOPO1 file \n')
	print "Opened Global ETOPO1 file"
	fu = nc(namef, 'r')
	lon = fu.variables['lon'][:]
	lat = fu.variables['lat'][:]
	indloni=find(abs(lon-loni)==min(abs(lon-loni)))
	indlonf=find(abs(lon-lonf)==min(abs(lon-lonf)))
	indlonf=indlonf+1
	indlati=find(abs(lat-lati)==min(abs(lat-lati)))
	indlatf=find(abs(lat-latf)==min(abs(lat-latf)))
	indlatf=indlatf+1
	lon = fu.variables['lon'][indloni:indlonf+1:mini]
	lat = fu.variables['lat'][indlati:indlatf+1:mini]
else:

	# Reginal (Brazil)------------
	fl.write(' Opened Regional ETOPO1 file \n')
	print "Opened Regional (Brazil) ETOPO1 file"
	fu = nc('ETOPO-REMO_BR.nc', 'r')
	lon = fu.variables['x'][:]
	lat = fu.variables['y'][:]
	indloni=find(abs(lon-loni)==min(abs(lon-loni)))
	indlonf=find(abs(lon-lonf)==min(abs(lon-lonf)))
	indlonf=indlonf+1
	indlati=find(abs(lat-lati)==min(abs(lat-lati)))
	indlatf=find(abs(lat-latf)==min(abs(lat-latf)))
	indlatf=indlatf+1
	lon = fu.variables['x'][indloni:indlonf+1:mini]
	lat = fu.variables['y'][indlati:indlatf+1:mini]


b = fu.variables['z'][indlati:indlatf+1:mini,indloni:indlonf+1:mini]
sk=int(round(res/mini))

[mnlon,mnlat]=np.meshgrid(lon[::sk],lat[::sk])
intg=mpl_toolkits.basemap.interp(b,lon,lat,mnlon,mnlat,checkbounds=False, masked=False, order=1)

#nintg=zeros((intg.shape[0],intg.shape[1]))
#for i in arange(0,intg.shape[0]+1):
#        nintg[i-1][:]=intg[-i][:]
nintg=flipud(intg)

fl.write(' \n')
fl.write('Number of points lat lon => ' + repr(nintg.shape) +'\n')
fl.write('Initial Latitude => ' + repr(lati) + ' degrees \n')
fl.write('Final Latitude => ' + repr(latf) + ' degrees \n')
fl.write('Initial Longitude => ' + repr(loni) + ' degrees \n')
fl.write('Final latitude => ' + repr(lonf) + ' degrees \n')
fl.write('Resolution => ' + repr(res) + ' minutes')
fl.close()


savetxt("bathymetry.txt",nintg,fmt="%6i",delimiter="\t")

b=b*(-1)
intg=intg*(-1)
nintg=nintg*(-1)

# Plotting the final figure 
plt.figure

# Making the bathymetry levels of bar 

if b.min() < 0:
	bmin=0
else:
	bmin=b.min()

levels=range(int(bmin),int(b.max())+int((b.max()-bmin)/15),int((b.max()-bmin)/15))
if levels[0]<0:
	levels[0]=0


# levels=[0,10,20,30,40,50,60,70,80,90,100,150,200]

if loni < 0 and lonf <= 0:
	lon_0=-(abs(lonf)+abs(loni))/2.0
else:
	lon_0=(loni+lonf)/2.0


if lati < 0 and latf <= 0:
	lat_0=-(abs(latf)+abs(lati))/2.0
else:
	lat_0=(lati+latf)/2.0

print 'Center longitude ',lon_0
print 'Center latitude ',lat_0


map = Basemap(llcrnrlat=lati,urcrnrlat=latf,\
llcrnrlon=loni,urcrnrlon=lonf,\
rsphere=(6378137.00,6356752.3142),\
resolution='h',area_thresh=1000.,projection='cyl',\
lat_1=lati,lon_1=loni,lat_0=lat_0,lon_0=lon_0)


x, y = map(mnlon,mnlat)

map.drawcoastlines()
map.drawcountries()
map.drawstates()
map.fillcontinents(color='grey')
map.drawmeridians(np.arange(lon[::sk].min(),lon[::sk].max(),nx),labels=[0,0,0,1])
map.drawparallels(np.arange(lat[::sk].min(),lat[::sk].max(),ny),labels=[1,0,0,0])
#map.bluemarble()


map.contourf(x,y,intg,levels)
# map.contourf(x,y,intg,levels,cmap=palette,norm=colors.normalize(vmin=0,vmax=200,clip=False))

plt.colorbar()
title('ETOPO Bathymetry')
plt.show()
#raw_input( '\n\nPress Enter to exit...' )

