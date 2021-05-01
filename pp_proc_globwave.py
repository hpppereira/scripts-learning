'''
Programa principal para baixar e processar dados
de satelite do globwave

Comando para lisar os dados de acordo com data e latlon inicial e final 
PNBOIA RIO GRANDE PERIODO DE 2009
python getgranulelist.py --product=GW_L2P_ALT_JAS2_GDR --date=2009-02-01T00:00:00,2010-01-02T00:00:00 --bbox=-31.56667,-31.56667,-49.86667,-49.86667 --url

Programa para baixar dados de ondas de satelite via ftp no servidor do globwave

Processamentos dos arquivos netcdf baixados
As variaves de tempo esta em segundos inicando
em 01/01/1985, como corrigir? funcao datetime?
perguntas para ricardinho

pode ser carregdo atraves do shell (wget_gw.sh)

As variaves de tempo esta em segundos inicando
em 01/01/1985, como corrigir? funcao datetime?
perguntas para ricardinho

# #latitude e longitude das boias (dec.graus)
# #RS
# lat_rs = -31.56667
# lon_rs = -49.86667                

# #SC
# lat_sc = -28.50000
# lon_sc = -47.36667

# #SP
# lat_sp = -25.28334
# lon_sp = -44.93334

# #PE
# lat_pe = -8.149
# lon_pe = -34.56

'''

########### biliotecas ###########

import distancialatlon
#import sys
#import subprocess
import os# Processamentos dos arquivos netcdf baixados
#import glob
import netCDF4 as nc
from mpl_toolkits import basemap
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from ftplib import FTP
import gzip
reload(distancialatlon)

# plt.close('all')
# regua = '\n' + '##' + 20 * '==' + '##' + '\n'

########### dados de entrada ###########


login = 'w1f612'
senha = 'tempo2'

#escolhe funcoes do programa: 0 = nao executa ; 1 = executa
baixadadoswget = 0
local = 'rio_grande'
lati = -31.79
loni = -50.09
latf = -31.39
lonf = -49.63
pathname = os.environ['HOME'] + '/Dropbox/globwave/'

arq = 'GW_L2P_ALT_JAS2_GDR_20090210_131809_20090210_141422_022_136.nc.gz'


pathnamearq = pathname + 'dados/' + local + '/' + arq


########### inicializacao ###########

#calcula distancia entre os pontos
dist = distancialatlon.dist(lati, loni, latf, lonf)
print 'Raio minimo para aceitar os pontos em ' + local + ': ' + str(dist/2.) + ' km'

########### carrega dados netcdf ###########

#baixa os dados em batelada do ftp a parir da lista especificada
#carrega a lista de dados com o tempo e latlon selecionados (saida da getgranulelist.py)
lista = np.loadtxt(pathname + 'listas/JAS2_riogrande_2009.txt',dtype=str)

#lista nome dos arquivos selecionados
listasel = []
listadir = []
for i in range(0,len(lista),2):
	listasel.append(lista[i])
	listadir.append(lista[i+1])

#baixa os arquivos selecionados
if baixadadoswget == 1:
	for i in range(len(listadir)):
		print 'Baixando ' + str(i) + ' de ' + str(len(listadir))
		os.system("wget -r " + listadir[i])
		os.system("cp " + listadir[i][20:] + " " + pathname + "dados/" + local)
 

########### carrega dados netcdf ###########

#nome do arquivo

#extrai os arquivos .nc dos zipados (.gz)
inF = gzip.open(pathnamearq, 'rb')
outF = open(pathnamearq[:-3], 'wb')
outF.write( inF.read() )
inF.close()
outF.close()

#carrega arquivo nc
f = nc.Dataset(pathnamearq[:-3], 'r')

#define variaveis
t_nc = f.variables['time']
lat_nc = f.variables['lat']
lon_nc = f.variables['lon']
swh_nc = f.variables['swh']
swhc_nc = f.variables['swh_calibrated']

#cria array das variaveis
t = t_nc[:]
lat = lat_nc[:]
lon = lon_nc[:] #- 180
swh = swh_nc[:]
swhc = swhc_nc[:]


########### figura do track do satelite ###########

plt.figure()
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

plt.plot(lon,lat,'r*',markersize=10)
# plt.plot(lon_sc,lat_sc,'r*',markersize=10)
# plt.plot(lon_sp,lat_sp,'r*',markersize=10)
# plt.plot(lon_pe,lat_pe,'r*',markersize=10)

# #plota lat/long do satelite
# plt.plot(lon1,lat1,'o',markersize=5)


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


