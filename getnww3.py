# coding: utf-8

# # Retrieve WW3 model results for NDBC buoys location
# 
# All GRIB files can be retrieved from the directory ftp://polar.ncep.noaa.gov/pub/waves/. The GRIB directory format is YYYYMMDD.tHHz where YYYYMMDD is the date, tHHz is the run cycle identifier (t00z through t18z, respectively). The number of dates and cycles for which data are available may vary based upon available resources.
# 
# Alternatively, ftp://polar.ncep.noaa.gov/pub/waves/latest_run/ gives access to the most recent model results.
# 
# The file names for the GRIB files are model_ID.grib_ID.grb, where model_ID is a model identifier (nww3, akw, wna, nah or enp for global, Alaskan Waters Western North Atlantic, North Atlantic Hurricane and Easrern North Pacific model, respectively), and where grib_ID represents a GRIB identifier as in the table above. The file model_ID.all.grb contains all GRIB fields.
# 
# The global NWW3 model
# The regional Alaskan Waters (AKW) model
# The regional Western North Atlantic (WNA) model
# The regional North Atlantic Hurricane (NAH) model
# The regional Eastern North Pacific (ENP) model
# The regional North Pacific Hurricane (NPH) model
# 
# # Examples of NWW3 Model Data Processing with Python
# 
# The following examples use Python to extract and visualize the sea surface height and ocean temperature in the NWW3 model using data from the NOMADS data server and a downloaded NWW3 GRiB2 file.
# 
# Prerequisites
# 
# The examples make use of the following free software:
# 
# Python
# Numpy (Numerical Python
# netcdf4-python: A Python/numpy interface for NetCDF and OpenDAP
# Basemap: A module to plot data on map projections with matplotlib
# pygrib (python module for reading GRiB files)
# Example 1: Plot data from the NOMADS Data Server
# Example 2: Plot data from an NWW3 GRiB2 file

'''Extract and plot data from the NOMADS Data Server'''

# basic NOMADS OpenDAP extraction and plotting script
import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import netCDF4
import pandas as pd
import datetime as dt
import os

# plt.close('all')

pathname_nww3 = os.environ['HOME'] + '/Dropbox/database/NWW3/realtime/'
pathname_fig = os.environ['HOME'] + '/Dropbox/metocean/web/img/'

# Function to find index to nearest point
def near(array,value):
    idx=(abs(array-value)).argmin()
    return idx

# set up the URL to access the data server.
# See the NWW3 directory on NOMADS 
# for the list of available model run dates.

mydate = dt.datetime.now()# - dt.timedelta(days=1)
mydate = mydate.strftime('%Y%m%d')

url = 'http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'+mydate+'/nww3'+mydate+'_00z'

# Extract the significant wave height of combined wind waves and swell

nc = netCDF4.Dataset(url)
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
data_hs = nc.variables['htsgwsfc'][0, :, :]
data_tp = nc.variables['perpwsfc'][0,:,:]
time_var = nc.variables['time']
dtime = netCDF4.num2date(time_var[:],time_var.units)
#nc.close()

nc.variables.keys()

first = netCDF4.num2date(time_var[0],time_var.units)
last = netCDF4.num2date(time_var[-1],time_var.units)
print (first.strftime('%Y-%b-%d %H:%M'))
print (last.strftime('%Y-%b-%d %H:%M'))
print (lon.min(),lon.max())

# Specify desired station time series location
# note we add 360 because of the lon convention in this dataset

#lat, lon
stat  = {
		 'NDBC_32012':   [-19.425, -085.078 + 360], #east pacific ocean - very deep water
		 'NDBC_41002':   [+31.760, -074.840 + 360], 
		 'NDBC_41013':   [+33.436, -077.743 + 360],
		 'NDBC_41060':   [+14.825, -051.016 + 360],
		 'NDBC_41025':   [+35.006, -075.402 + 360],
		 'NDBC_41114':   [+27.551, -080.222 + 360],
		 'NDBC_42058':   [+14.923, -074.918 + 360],
		 'NDBC_44020':   [+41.443, -070.187 + 360],
		 'NDBC_46215':   [+35.204, -120.859 + 360],
		 'NDBC_46229':   [+43.766, -124.551 + 360],
		 'NDBC_51202':   [+21.415, -157.678 + 360], #hawaii (maybe the data is in one side of the island and the model in another)
		 'PNBOIA_BRN':   [+01.094, -046.350 + 360], #barra norte/am 
		 'PNBOIA_FTL':   [-02.987, -038.819 + 360], #fortaleza/ce
		 'PNBOIA_RCF':   [-08.149, -034.560 + 360], #recife/pe
		 'PNBOIA_PSG':   [-18.151, -037.944 + 360], #porto seguro/ba
		 'PNBOIA_VIX':   [-20.278, -039.727 + 360], #vitoria/es
		 'PNBOIA_CFR':   [-22.995, -042.187 + 360], #cabo frio/rj
		 'PNBOIA_BGA':   [-22.924, -043.150 + 360], #baia de guanabara/rj (nao esta dando valores corretos. pegar mais offhshore)
		 'PNBOIA_SAN':   [-25.283, -044.933 + 360], #santos/sp
		 'PNBOIA_FLN':   [-28.500, -047.366 + 360], #florianopolis/sc
		 'PNBOIA_RIG':   [-31.566, -049.966 + 360], #rio grande/rs
		 # 'REMO_CF01' :   [-23.770, -41.6106 + 360], #prof: 300 m
		 # 'REMO_CF02' :   [-24.190, -41.3414 + 360], #prof: 2000 m
		 # 'SIMCOSTA_RJ3': [-22.580, -43.1000 + 360],
		 # 'SIMCOSTA_RS1': [-32.100, -52.6000 + 360],
		 # 'SIMCOSTA_RS5': [-32.170, -52.1000 + 360],
		 # 'SIMCOSTA_SC1': [-27.160, -48.2500 + 360]
		 }

#retrieve time series of a point
for st in np.sort(list(stat.keys())):

	print (st)

	# Find nearest point to desired location (no interpolation)
	ix = near(lon, stat[st][1])
	iy = near(lat, stat[st][0])
	print (ix,iy)

	# Get all time records of variable [vname] at indices [iy,ix]
	hs = nc.variables['htsgwsfc'][:,iy,ix]
	tp = nc.variables['perpwsfc'][:,iy,ix]
	dp = nc.variables['dirpwsfc'][:,iy,ix]
	ws = nc.variables['windsfc'][:,iy,ix]
	wd = nc.variables['wdirsfc'][:,iy,ix]
	tim = dtime[:]

	# Create Pandas time series object
	df = pd.DataFrame(np.array([hs, tp, dp, ws, wd]).T,index=pd.Series(tim, name='date'),columns=['hs', 'tp', 'dp', 'ws', 'wd'])

	#open existed file (use for new station)
	old = pd.read_csv(pathname_nww3 + 'NWW3_' + st + '.csv', sep=',', parse_dates=['date'], index_col=['date'])

	#concatenate new and old file
	df = pd.concat([old, df], axis=0)

	#remove valores repetidos lines
	aux, ind = np.unique(df.index, return_index=True)
	df = df.ix[ind,:]

	#coloca em ordem
	df = df.sort_index()

	#write to a CSV file
	df.to_csv(pathname_nww3 + 'NWW3_' + st + '.csv', na_rep='NaN')


#plot wave field
#############################################################
# Hs

plt.figure(figsize=(16,14))

m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(),
	urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(),resolution='c')

# convert the lat/lon values to x/y projections.
lons, lats = np.meshgrid(lon,lat)
x, y = m(*np.meshgrid(lon,lat))

x1, y1 = m(*np.meshgrid(stat[st][1], stat[st][0]))

# plot the field using the fast pcolormesh routine 
# set the colormap to jet.

m.pcolormesh(x,y,data_hs,shading='flat',cmap=plt.cm.jet)
m.colorbar(location='right')

# Add a coastline and axis values.

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])

#plot points
a = [ m(*np.meshgrid(stat[st][1], stat[st][0])) for st in stat ]
[m.plot(a[i][0], a[i][1], 'ko', markersize=9) for i in range(len(a))]
#[plt.text(a[i][0], a[i][1], stat.keys()[i]) for i in range(len(a))]

# Add a colorbar and title, and then show the plot.

plt.title('NWW3 Significant Wave Height from NOMADS - ' + dt.datetime.now().strftime('%Y-%m-%d 00Z'))

plt.savefig(pathname_fig + 'WaveField_Hs.png', bbox_inches='tight')

###################################################
#Tp

plt.figure(figsize=(16,14))

m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(),
	urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(),resolution='c')

# convert the lat/lon values to x/y projections.
#lons, lats = np.meshgrid(lon,lat)
# x, y = lons, lats
#x, y = m(*np.meshgrid(lon,lat))

#x1, y1 = m(*np.meshgrid(stat[st][1], stat[st][0]))

# plot the field using the fast pcolormesh routine 
# set the colormap to jet.

m.pcolormesh(x,y,data_tp,shading='flat',cmap=plt.cm.jet)
m.colorbar(location='right')

# Add a coastline and axis values.

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])

#plot points
#a = [ m(*np.meshgrid(stat[st][1], stat[st][0])) for st in stat ]
[m.plot(a[i][0], a[i][1], 'ko', markersize=9) for i in range(len(a))]
#[plt.text(a[i][0], a[i][1], stat.keys()[i]) for i in range(len(a))]

# Add a colorbar and title, and then show the plot.

plt.title('NWW3 Peak Period from NOMADS - ' + dt.datetime.now().strftime('%Y-%m-%d 00Z'))

plt.savefig(pathname_fig + 'WaveField_Tp.png', bbox_inches='tight')

plt.show()