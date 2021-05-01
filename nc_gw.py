# Processamentos dos arquivos netcdf baixados

#pode ser carregdo atraves do shell (wget_gw.sh)

import sys
import subprocess
import os
import glob
import netCDF4 as nc
import numpy as np
#import gzip

## =============================================== ##

regua = '\n' + '##' + 20 * '==' + '##' + '\n'

## =============================================== ##

#diretorio de onda estao os arquivos (para baixar o ano inteiro, fazer um for no shell)
pathname = '/home/hppp/Dropbox/globwave/eftp.ifremer.fr/waveuser/globwave/data/l2p/altimeter/nrt/cryosat2/2013/001/'
# pathname1 = 

#lista arquivos dentro do diretorio
filelist = glob.glob(pathname + "*nc")

#quanidade de arquivos no dia
c_arq = len(filelist)

#carrega dado netcdf (fazer isso dentro de um for)
f = nc.Dataset(filelist[0], 'r')

#lista o nome das variaveis
for v in f.variables:
	print v

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

#listar dimensoes

print 'Lista de dimensoes: '

for d in f.dimensions:
	print d

print regua

## =============================================== ##

#declarar variaveis

t1 = f.variables['time']
swh1 = f.variables['swh']

#cria array
t = t1[:]
swh = swh1[:]


