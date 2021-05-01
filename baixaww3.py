# -*- coding: utf-8 -*-
"""
Created on Sun Aug 09 16:13:42 2015

@author: MEUS DOCUMENTOS
"""

# basic NOMADS OpenDAP extraction and plotting script
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.mlab
import netCDF4
import csv


# set up the URL to access the  data server.
# See the NWW3 directory on NOMADS 
# for the list of available model run dates.

mydate='20150814'
url='http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'+ \
    mydate+'/nww3'+mydate+'_00z'

#Lat_input=float32([-30,-25])
#Lon_input=float32([310,315])

Lat_input=float32([-40,-22])
Lon_input=float32([300,345])


# Extract the significant wave height of combined wind waves and swell

file = netCDF4.Dataset(url)


## Global
#lat  = file.variables['lat'][:]
#lon  = file.variables['lon'][:]
#Hs = file.variables['htsgwsfc'][1,:,:]
#Tp = file.variables['perpwsfc'][1,:,:]
#Dir_pri = file.variables['dirpwsfc'][1,:,:]

# America do SUL
#lat  = file.variables['lat'][15:86]
#lon  = file.variables['lon'][232:288]
#Hs = file.variables['htsgwsfc'][1,15:86,232:288]
#Tp = file.variables['perpwsfc'][1,15:86,232:288]
#Dir_pri = file.variables['dirpwsfc'][1,15:86,232:288]

## Sul do Brasil
#lat  = file.variables['lat'][20:70]
#lon  = file.variables['lon'][232:288]
#Hs = file.variables['htsgwsfc'][1,20:70,232:288]
#Tp = file.variables['perpwsfc'][1,20:70,232:288]
#Dir_pri = file.variables['dirpwsfc'][1,20:70,232:288]

## Sul do Brasil
#lat  = file.variables['lat'][40:55]
#lon  = file.variables['lon'][240:260]
#Hs = file.variables['htsgwsfc'][1,40:55,240:260]
#Tp = file.variables['perpwsfc'][1,40:55,240:260]
#Dir_pri = file.variables['dirpwsfc'][1,40:55,240:260]

## Sul do Brasil
#lat  = file.variables['lat'][48:53]
#lon  = file.variables['lon'][248:253]
#Hs = file.variables['htsgwsfc'][1,48:53,248:253]
#Tp = file.variables['perpwsfc'][1,48:53,248:253]
#Dir_pri = file.variables['dirpwsfc'][1,48:53,248:253]







######################## cores da legenda
#color_Hs = np.arange(0., 10., 0.5)
#color_Tp = np.arange(0., 20., 0.5)
#color_Dir_pri = np.arange(0., 360., 0.5)


#timess  = file.variables['time'][:]
#direc_pri = file.variables['dirpwsfc'][1,:,:]
#direc_sec = file.variables['dirswsfc'][1,:,:]
#per_med_pri = file.variables['perpwsfc'][1,:,:]
#per_med_sec = file.variables['perswsfc'][1,:,:]
#vet_vento_u = file.variables['ugrdsfc'][1,:,:]
#vet_vento_v = file.variables['vgrdsfc'][1,:,:]
#vet_vento_w = file.variables['wdirsfc'][1,:,:]
#vel_vento = file.variables['windsfc'][1,:,:]
#vel_vento = file.variables['wvdirsfc'][1,:,:]


#
## Procurando as latiutude e longitudes
lat  = file.variables['lat'][:]
lon  = file.variables['lon'][:]
#Hs = file.variables['htsgwsfc'][1,:,:]
#Tp = file.variables['perpwsfc'][1,:,:]
#Dir_pri = file.variables['dirpwsfc'][1,:,:]

Lat_ind1 = find(lat[:]==Lat_input[0]);
Lat_ind2 = find(lat[:]==Lat_input[1]);
Lon_ind1 = find(lon[:]==Lon_input[0]);
Lon_ind2 = find(lon[:]==Lon_input[1]);

lat  = file.variables['lat'][Lat_ind1:Lat_ind2]
lon  = file.variables['lon'][Lon_ind1:Lon_ind2]
Hs = file.variables['htsgwsfc'][1,Lat_ind1:Lat_ind2,Lon_ind1:Lon_ind2]
Tp = file.variables['perpwsfc'][1,Lat_ind1:Lat_ind2,Lon_ind1:Lon_ind2]
Dir_pri = file.variables['dirpwsfc'][1,Lat_ind1:Lat_ind2,Lon_ind1:Lon_ind2]


file.close()




# Since Python is object oriented, you can explore the contents of the NOMADS
# data set by examining the file object, such as file.variables.

# The indexing into the data set used by netCDF4 is standard python indexing.
# In this case we want the first forecast step, but note that the first time 
# step in the RTOFS OpenDAP link is all NaN values.  So we start with the 
# second timestep

# Plot the field using Basemap.  Start with setting the map
# projection using the limits of the lat/lon data itself:

m=Basemap(projection='merc',lat_ts=10,llcrnrlon=lon.min(), \
  urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
  resolution='f')

# convert the lat/lon values to x/y projections.

x, y = m(*np.meshgrid(lon,lat))

# plot the field using the fast pcolormesh routine 
# set the colormap to jet.


#############################
# set up the figure
plt.figure()
plt.subplot(221)
m.pcolormesh(x,y,Hs,shading='flat',cmap=plt.cm.jet)
m.colorbar(location='right')
#m.colorbar(location='right',ticks=color_Hs)

# Add a coastline and axis values.

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,4.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,4.),labels=[0,0,0,1])


# Add a colorbar and title, and then show the plot.

plt.title('Altura Significativa pelo NOMADS')
plt.show()



##############################

# set up the figure
plt.subplot(222)
m.pcolormesh(x,y,Dir_pri,shading='flat',cmap=plt.cm.jet)
m.colorbar(location='right')
#m.colorbar(location='right',ticks=color_Tp)

# Add a coastline and axis values.

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,4.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,4.),labels=[0,0,0,1])


# Add a colorbar and title, and then show the plot.

plt.title('Direção Primária pelo NOMADS')
plt.show()



##############################

# set up the figure
plt.subplot(223)
m.pcolormesh(x,y,Tp,shading='flat',cmap=plt.cm.jet)
m.colorbar(location='right')
#m.colorbar(location='right',ticks=color_Dir_pri)

# Add a coastline and axis values.

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,4.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,4.),labels=[0,0,0,1])


# Add a colorbar and title, and then show the plot.

plt.title('Período Primária (médio) pelo NOMADS')
plt.show()
writer = csv.writer(open(str('Dado1.Csv'), "wb"))
writer.writerows(Hs)