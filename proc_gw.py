# Processamentos dos arquivos netcdf baixados
# As variaves de tempo esta em segundos inicando
# em 01/01/1985, como corrigir? funcao datetime?
# perguntas para ricardinho


#pode ser carregdo atraves do shell (wget_gw.sh)

#import sys
#import subprocess
import os# Processamentos dos arquivos netcdf baixados
# As variaves de tempo esta em segundos inicando
# em 01/01/1985, como corrigir? funcao datetime?
# perguntas para ricardinho


#pode ser carregdo atraves do shell (wget_gw.sh)

#import glob
import netCDF4 as nc
#from mpl_toolkits import basemap
import numpy as np
import dist_latlon
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

reload(dist_latlon)

plt.close('all')

## =============================================== ##

regua = '\n' + '##' + 20 * '==' + '##' + '\n'

## =============================================== ##

#latitude e longitude das boias (dec.graus)

#RS
lat_rs = -31.56667
lon_rs = -49.86667                

#SC
lat_sc = -28.50000
lon_sc = -47.36667

#SP
lat_sp = -25.28334
lon_sp = -44.93334

#PE
lat_pe = -8.149
lon_pe = -34.56


#diretorio do satelite
pathname = '/home/hppp/Documents/globwave/eftp.ifremer.fr/waveuser/globwave/data/l2p/altimeter/nrt/cryosat2/'

#lista diretorios de anos
dirano = os.listdir(pathname)
dirano = np.sort(dirano)

#arquivos em nc que passaramo no criterio de avaliacao
t1 = []
lat1 = []
lon1 = []
swh1 = []

arq_rs = []
arq_sc = []
arq_sp = []
arq_pr = []

param_rs = []

##Ano
for i in range(len(dirano)):

	#cria pathname para os dias
	pathname1 = pathname + dirano[i] + '/'

	#lista diretorios de dias
	dirdia = os.listdir(pathname1)
	dirdia = np.sort(dirdia)

	##Dia
	for i in ([1]): #in range(len(dirdia)):

		pathname2 = pathname1 + dirdia[i] + '/'

		#lista de arquivos
		larq = os.listdir(pathname2)
		larq = np.sort(larq)

		##Arquivos .nc
		for i in range(len(larq)):

			#carrega dados netcdf
			f = nc.Dataset(pathname2 + larq[i], 'r')

			#define variaveis
			t_nc = f.variables['time']
			lat_nc = f.variables['lat']
			lon_nc = f.variables['lon']
			swh_nc = f.variables['swh']
			swhc_nc = f.variables['swh_calibrated']

			#cria array das variaveis
			t = t_nc[:]
			lat = lat_nc[:]
			lon = lon_nc[:]
			swh = swh_nc[:]
			#swhc = swhc_nc[:]

			#vetor com todas as medicoes
			t1.append(list(t))
			lat1.append(list(lat))
			lon1.append(list(lon))
			swh1.append(list(swh))

			#chama funcao para verificar distancia em km

			#RS
			# for ii in range(len(lat)):

			# 	dist_rs = dist_latlon.distancia(lat[ii],lon[ii],lat_rs,lon_rs)
			# 	dist_sc = dist_latlon.distancia(lat[ii],lon[ii],lat_sc,lon_sc)
			# 	dist_sp = dist_latlon.distancia(lat[ii],lon[ii],lat_sp,lon_sp)
			# 	dist_pe = dist_latlon.distancia(lat[ii],lon[ii],lat_pe,lon_pe)

			# 	# ** fazer condicao de 1 hora do horario da boia

			# 	if dist_rs > 100:

			# 		param_rs.append([t,lat,lon,swh])

				# 	# i_arq = find

				# 	# arq_rs.append(larq[i])

				# if dist_sc < 100:

				# 	# arq_sc.append(larq[i])

				# if dist_sp < 100:

				# 	# arq_sp.append(larq[i])

				# if dist_pe < 100:

					# arq_pe.append(larq[i])



#figura do track do satelite

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines.
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(-90.,91.,30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='aqua')
plt.title("Equidistant Cylindrical Projection")

#plota as posicoes das boias

plt.plot(lon_rs,lat_rs,'r*',markersize=10)
plt.plot(lon_sc,lat_sc,'r*',markersize=10)
plt.plot(lon_sp,lat_sp,'r*',markersize=10)
plt.plot(lon_pe,lat_pe,'r*',markersize=10)

#plota lat/long do satelite
plt.plot(lon1,lat1,'o',markersize=5)


plt.show()









#carrega dado netcdf (fazer isso dentro de um for)
#f = nc.Dataset(filelist[0], 'r')


#lista o nome das variaveis
#for v in f.variables:
#	print v
### =============================================== ##

#lista de variaveis:

# time
# lat
# lon
# swh
# swh_calibrated
# swh_quality
# swh_standard_error
# sigma0
# sigma0_calibrated
# sigma0_quality
# wind_speed_alt
# wind_speed_alt_calibrated
# wind_speed_model_u
# wind_speed_model_v
# rejection_flags
# swh_rms
# swh_num_valid
# sigma0_rms
# off_nadir_angle_pf
# range_rms
# bathymetry
# distance_to_coast
# sea_surface_temperature
# surface_air_temperature
# surface_air_pressure

## =============================================== ##

# #listar dimensoes

# print 'Lista de dimensoes: '

# for d in f.dimensions:
# 	print d

# print regua

# ## =============================================== ##

# #declarar variaveis

# t1 = f.variables['time']
# swh1 = f.variables['swh']

# #cria array
# t = t1[:]
# swh = swh1[:]


