# Processamentos dos arquivos netcdf baixados

import netCDF4 as nc
import numpy as np
import gzip

#carrega dado netcdf
f = nc.Dataset('/home/hppp/Dropbox/globwave/GW_L2P_ALT_CRYO_GDR_20120101_001215_20120101_005556_023_264.nc', 'r')

#lista o nome das variaveis
for v in f.variables:
	print v

print '\n'



## =============================================== ##

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


#'f eh um objeto representando o arquivo netcdf aberto
# variaveis eh um atributo de f, em particular eh um dicionario

#listar as dimensoes
#* todas as variaveis em netcdf tem uma dimensao associada, especificada por uma lista de dimensoes

for d in f.dimensions:
	print d

print '\n'

#obter mais informacao de cada variavel

#hs
swh = f.variables['swh']

print swh

print '\n'
#listar os atributos de uma variavel

for att in swh.ncattrs():
	print att

print '\n'

#saber o valor de uma variavel em determinada lat/long

#primeiro temos que entender a dimensao da variavel
# as variavels de coordenadas eh 1D e tem o mesmo nome das dimensoes
# as variaveis de coordenadas e as auxiliares localiza valores no tempo espaco

print 'Variables: '
for v in f.variables:
	print (v)

print

print 'Dimensions: '
for d in swh.dimensions:
	print (d)

tm = f.variables['time']
print tm


#le a variavel tempo (matriz de 1 dim)
tm[:]

#lat/long

lat = f.variables['lat']
lon = f.variables['lon']

print lat
print lon

#achar indices de array de lat/long o mais proximo de um ponto especifico

lat_pt, lon_pt = -50.5 , -146.1

#ler lat/lon em array
latvals = lat[:]
lonvals = lon[:]

#distancia minima??
distsq_min = 1.0e30

#dimensoes (apenas do tempo nos temos)
t = f.dimensions['time']

for tt in range(len(t)):

	latval = latvals[tt]

	#forma a lon para ficar entre +- 180
	lonval = (lonvals[tt] + 180) % 360 -180

	dist_sq = (latval - lat_pt) **2 + (lonval - lon_pt) **2

	if dist_sq < distsq_min:
		t_min, distsq_min = tt, dist_sq


