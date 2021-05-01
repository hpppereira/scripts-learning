'''
Abre imagens de satelite
diretamente do site
'''

import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
import os
import espec

plt.close('all')
# filepath = '20071231153739-NODC-L3C_GHRSST-SSTskin-AVHRR_Pathfinder-PFV5.2_NOAA18_G_2007365_day-v02.0-fv01.0.nc'
# filepath = 'MYD11_L2.A2015056.1230.005.NRT.hdf'
# ftp://ftp.nodc.noaa.gov/pub/data.nodc/pathfinder/Version5.2/2007/20061231233901-NODC-L3C_GHRSST-SSTskin-AVHRR_Pathfinder-PFV5.2_NOAA18_G_2007001_night-v02.0-fv01.0.nc

pathname = os.environ['HOME'] + '/Dropbox/sat/pi/dados/'
filepath = pathname + 'aggregate__MODIS_AQUA_L3_CHLA_MONTHLY_4KM_R.ncml.nc' #clorofila modis

# ================================================================================================ #
#abre arquivos hdf
# import gdal
# import matplotlib.pyplot as plt

# ds = gdal.Open('HDF4_SDS:UNKNOWN:"MYD11_L2.A2015056.1230.005.NRT.hdf":6')
# data = ds.ReadAsArray()
# ds = None

# fig, ax = plt.subplots(figsize=(6,6))

# ax.imshow(data[0,:,:], cmap=plt.cm.Greys, vmin=1000, vmax=6000)

# %matplotlib inline
# plt.rcParams['figure.figsize'] = (12.0, 8.0)

# ================================================================================================ #

# filepath = /path/to/file.nc
# Read in dataset (using 'r' switch, 'w' for write)
dataset = Dataset(filepath,'r')

#mostra as variaveis
# print dataset.variables.keys()

# plt.show()

# -49.403 (indice=175) , -31.79 (indice=141)

#mostra as unidades

# Copy data to variables, '[:]'' also copies missing values mask
lons = dataset.variables["lon"][:]
lats = dataset.variables["lat"][:]
time = dataset.variables["time"][:]
cla = dataset.variables["l3m_data"][:]
dataset.close()

# ================================================================================================ #

# plt.contourf(cla[0], 20)

# lonvals = lon[:]
# latvals = lat[:]
# plt.title (pottmp.long_name + ' (' + pottmp.units + ')')
# plt.xlabel(lon.long_name    + ' (' + lon.units    + ')')
# plt.ylabel(lat.long_name    + ' (' + lat.units    + ')')
# plt.contourf(lonvals, latvals, data, 20, cmap=plt.get_cmap('YlGnBu_r'))
# plt.colorbar()
# plt.show()

# These lines do the actual plotting
# 

# ================================================================================================ #

# # Get some parameters for the Stereographic Projection
lon_0 = lons.mean()
lat_0 = lats.mean()

# m = Basemap(width=3000000,height=3500000,
#             resolution='l',projection='eqdc',\
#             lat_ts=40,lat_0=lat_0,lon_0=lon_0)

# Because our lon and lat variables are 1D, 
# use meshgrid to create 2D arrays 
# Not necessary if coordinates are already in 2D arrays.
lon, lat = np.meshgrid(lons, lats)
# xi, yi = m(lon, lat)


# ================================================================================================ #

# plt.figure()

# # # Plot Data
# # cs = m.pcolor(xi,yi,np.squeeze(cla[0]))
# cs = m.pcolor(lon,lat,np.squeeze(cla[0]))


# # Add Grid Lines
# m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
# m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

# # Add Coastlines, States, and Country Boundaries
# m.drawcoastlines()
# m.drawstates()
# m.drawcountries()

# # Add Colorbar
# cbar = m.colorbar(cs, location='bottom', pad="10%")
# # cbar.set_label(tmax_units)

# # Add Title
# plt.title('DJF Maximum Temperature')

# plt.figure()

# for i in range(20):

# 	plt.figure()
# 	plt.contourf(lon,lat,cla[i])

# 	plt.show()

#-55.88 (19)/ -35.40 (227)
#-47.98 (210) / -27.53 (38)
# plt.show()				


#tempo, lat, lon

p1 = cla[:,141,175] #ponto 1: lon -49.403 (indice=175) , lat -31.79 (indice=141)
p2 = cla[:,227,19] #ponto 2: lon -55.88(indice=19) , lat -35.40 (indice=227)
p3 = cla[:,37,210] #ponto 3: lon -47.98(indice=210) , lat -27.53 (indice=38) 

#calcula o espectro
ap1 = espec.espec1(p1,len(p1)/2,1./31)
ap2 = espec.espec1(p2,len(p2)/2,1./31)
ap3 = espec.espec1(p3,len(p3)/2,1./31)

plt.figure ()
plt.subplot (221)
plt.plot (p1)
plt.subplot (222)
plt.plot (p2)
plt.subplot (223)
plt.plot (p3)




plt.figure ()
plt.subplot (221)
plt.plot (ap1[:,0],ap1[:,1])
plt.subplot (222)
plt.plot (ap2[:,0],ap2[:,1])
plt.subplot (223)
plt.plot (ap3[:,0],ap3[:,1])
plt.show ()

# def getnetcdfdata(data_dir, nc_var_name, min_lon, max_lon, min_lat, max_lat, data_time_start, data_time_end):
# '''Extracts subset of data from netCDF file
# based on lat/lon bounds and dates in the iso format '2012-01-31' '''
# # Create list of data files to process given date-range

# Processing Remote Sensing Data with Python Documentation, Release 1
# file_list = np.asarray(os.listdir(data_dir))
# file_dates = np.asarray([datetime.datetime.strptime(re.split('-', filename)[0], '%Y%m%d%H%M%S') for filename 9 data_files = np.sort(file_list[(file_dates >= data_time_start)&(file_dates <= data_time_end)])

# # Get Lat/Lon from first data file in list
# dataset = Dataset(os.path.join(data_dir,file_list[0]),'r')
# lons = dataset.variables["lon"][:]
# lats = dataset.variables["lat"][:]
# # Create indexes where lat/lons are between bounds
# lons_idx = np.where((lons > math.floor(min_lon))&(lons < math.ceil(max_lon)))[0]
# lats_idx = np.where((lats > math.floor(min_lat))&(lats < math.ceil(max_lat)))[0]
# x_min = lons_idx.min()
# x_max = lons_idx.max()
# y_min = lats_idx.min()
# y_max = lats_idx.max()

# # Create arrays for performing averaging of files
# vals_sum = np.zeros((y_max-y_min + 1, x_max-x_min + 1))
# vals_sum = ma.masked_where(vals_sum < 0 , vals_sum)
# mask_sum = np.empty((y_max-y_min + 1, x_max-x_min + 1))
# dataset.close()
# # Get average of chlorophyl values from date range
# file_count = 0
# for data_file in data_files:
# current_file = os.path.join(data_dir,data_file)
# dataset = Dataset(current_file,'r') # by default numpy masked array
# vals = np.copy(dataset.variables[nc_var_name][0 ,y_min:y_max + 1, x_min:x_max + 1])
# #vals = ma.masked_where(vals < 0, vals)
# #ma.set_fill_value(vals, -999)
# vals = vals.clip(0)
# vals_sum += vals
# file_count += 1
# dataset.close()
# vals_mean = vals_sum/file_count #TODO simple average
# # Mesh Lat/Lon the unravel to return lists
# lons_mesh, lats_mesh = np.meshgrid(lons[lons_idx],lats[lats_idx])
# lons = np.ravel(lons_mesh)
# lats = np.ravel(lats_mesh)
# vals_mean = np.ravel(vals_mean)

# return lons, lats, vals_mean
