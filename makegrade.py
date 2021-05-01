# -----------------------------------------------------------------
#   Defining grid domain, related to the input grid of WW3
# -----------------------------------------------------------------
#latitude
lati=-13.3
latf=-12.
#longitude  Defined as -180 to 180 instead of 0 to 360, Pay attention
loni=-39
lonf=-38

#latitude
lati=-10
latf=5
#longitude  Defined as -180 to 180 instead of 0 to 360, Pay attention
loni=-61
lonf=-35
# --------------------------------------------------------------------------
# Initial date. To avoid problems reading the time variable from netcdf file
iyear=2004
imonth=9
iday=1
ihour=0
# Time interval (hours)
dt=12
# ---------------------------------------------------------------------------------------
# Flag for creating wind figures. cfig=1 create. cfig=0 does not create and save run time
cfig=1;
# ---------------------------------------------------------------------------------------------------------------
# For running program using just one netcdf input file, write the name here. Otherwise comment the following line
name='wnd10m.cdas.201112.nc';tn=1
rname='CFSR'
# Wind intensity range, for plotting figures. 
vmin=5; vmax=25
# svec is very important for figure wind vectors! If it is too polute (too many vectors at the same figure range) increase this value
svec=5;
# If you want to modify the length of vector, chance the "scale" parameter at map.quiver plot 




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

# Palette and colors for plotting the figures
from mpl_toolkits.basemap import cm
colormap = cm.GMT_polar
palette = plt.cm.OrRd
palette.set_bad('aqua', 10.0)
import matplotlib.colors as colors

# leap years
p=array([1948,1952,1956,1960,1964,1968,1972,1976,1980,1984,1988,1992,1996,2000,2004,2008,2012,2016])
# Log file where processes will be written 
fl = open('log_windWW3.txt', 'w')
fl.write('=========== Tasks and processes done by makewindww3.py ===========\n')
fl.write('  \n')

# In case you are interested in concatenating more than one file (just for Linux, otherwise comment # the next lines):
# Pay attention if your netcdf files can be directly concatenated, i.e, if the end-time of previous file is exactly before the first time of next file
# If not, it is preferible to generate monthly files separetaly. This is why I commented # next lines
# listing files using bash commands 
# os.system("ls *.nc > list.txt")
# os.system("wc -l list.txt > nllist.txt")
# fl.write('Set up the list of files and its length \n')
# tm=open('nllist.txt')
# tline=tm.readline();tm.close()
# Number of files 
# tn=int(tline[0:-9])
# Opening the first file, just for taking the features, set some variables and save time inside the loop
# f = open('list.txt')
# name = f.readline();name=name[0:-1]
# f.close()



# Open the netcdf file
fu = nc.Dataset(name, 'r')  
# These variable names inside [] is defined by CFSR/wgrib2. If you have converted the grib file with another program rewrite these names 
lat=fu.variables['latitude'][:]
lon=fu.variables['longitude'][:]
uwnd=fu.variables['UGRD_10maboveground'][:]

# Taking the argument (index) of boundaries, i.e., initial/final latitudes and longitudes
# considering lat starting from north hemisphere (positive values) decreasing to the south

dife=abs(lat[:]-lati)
alati=dife.argmin()
if lati-lat[alati] < 0:
	alati=alati-1

dife=abs(lat[:]-latf)
alatf=dife.argmin()
if latf-lat[alatf] > 0:
	alatf=alatf+1

# considering lon starting from west (negative values) increasing eastwards.
lixo,lon = shiftgrid(180.,uwnd[0,:,:],lon,start=False)

dife=abs(lon[:]-loni)
aloni=dife.argmin()
if loni-lon[aloni] < 0:
	aloni=aloni-1

dife=abs(lon[:]-lonf)
alonf=dife.argmin()
if lonf-lon[alonf] > 0:
	alonf=alonf+1

# Setting variables to basemap figures
[mnlon,mnlat]=np.meshgrid(lon[aloni:alonf],lat[alati:alatf])
if lon[aloni] < 0 and lon[alonf] <= 0:
	lon_0=-(abs(lon[alonf])+abs(lon[aloni]))/2.0
else:
	lon_0=(lon[aloni]+lon[alonf])/2.0

if lat[alati] < 0 and lat[alatf] <= 0:
	lat_0=-(abs(lat[alatf])+abs(lat[alati]))/2.0
else:
	lat_0=(lat[alati]+lat[alatf])/2.0



lat=fu.variables['latitude'][alati:alatf]
fu.close()

fig=plt.figure(figsize=(8,6))
#map = Basemap(llcrnrlat=lat[0],urcrnrlat=lat[np-1],\
#	llcrnrlon=lon[0]-dl,urcrnrlon=lon[np-1]+dl,\
#	resolution='h',area_thresh=0.1,projection='merc',\
#	lat_0=lat_0,lon_0=lon_0)
 
map = Basemap(llcrnrlat=lat[0],urcrnrlat=lat[-1],\
llcrnrlon=lon[aloni],urcrnrlon=lon[alonf],\
rsphere=(6378137.00,6356752.3142),\
resolution='h',area_thresh=1,projection='merc',\
lat_1=lat[0],lon_1=lon[aloni],lat_0=lat_0,lon_0=lon_0)

xx, yy = map(mnlon,mnlat)

map.drawmeridians(arange(lon.min(),lon.max(),0.1),labels=[0,0,0,1],fmt="%2.2f")
map.drawparallels(arange(lat.min(),lat.max(),0.1),labels=[1,0,0,0],fmt="%2.2f")
map.fillcontinents(color='grey')
map.drawstates(linewidth=1)


map.plot(xx,yy,'bo',markersize=10)




# f.close()
# In case you want to run an animation (only for linux):
# os.system("convert -delay 10 -loop 0 *.png animaion.gif")

