'''
Avaliacao dos resultados do modelo ww3 da ClimaTempo
dados em .nc, disponivel em 
ftp://modelagem.climatempo.com.br/

Data da ultima modificacao: 25/08/2015

'''

#bibliotecas
import os
import netCDF4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

#diretorio dos dados
pathname = os.environ['HOME'] + '/Desktop/'

#carrega dados em nc
f = nc.Dataset(pathname + 'ww3_2014111000.nc', 'r') #hs, dirmn, peakp, peakd
f1 = nc.Dataset(os.environ['HOME'] + '/Dropbox/ww3br/resultados/Resultados_RT03/Espectros/' + 'ww310d_2014110112_avg_ATLASUL_spec.nc', 'r') #spec

#lista o nome das variaveis

print 'lista de variaveis:'
for v in f1.variables:
	print v
print '\n'

print 'lista de dimensoes:'
for d in f.dimensions:
	print d
print '\n'

#declara variaveis
t = f.variables['time']
lon = f.variables['longitude']
lat = f.variables['latitude']
hs = f.variables['hs']
dirmn = f.variables['dirmn']
# lev1 = f.variables['levels']
# loc1 = f.variables['loc001'] #(time, levels, lat, lon)

#lista os atributos de uma variavel
# print 'atributos:'
# for lont in lon1.ncattrs():
# 	print lont
# print '\n'

#cria array
t1 = t[:]
lon1 = lon[:]
lat1 = lat[:]
hs1 = hs[:]
# lev = lev1[:]
# loc = loc1[:]

# Get some parameters for the Stereographic Projection
lon_0 = lon1.mean()
lat_0 = lat1.mean()

plt.figure()

m = Basemap(width=5000000,height=3500000,
            resolution='l',projection='stere',\
            lat_ts=40,lat_0=lat_0,lon_0=lon_0)


# Because our lon and lat variables are 1D, 
# use meshgrid to create 2D arrays 
# Not necessary if coordinates are already in 2D arrays.
lon2, lat2 = np.meshgrid(lon1, lat1)
xi, yi = m(lon2, lat2)

# Plot Data
# cs = m.pcolor(lona,lata,hsa)
cs = m.pcolor(xi,yi,hs[0,:,:])

# Add Grid Lines
m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()

# Add Colorbar
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('metros')

# Add Title
plt.title('Significant Wave Height')

plt.show()

f.close()



