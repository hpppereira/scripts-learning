# Criar arquivos netCDF4 dos dados das boias

import os
import pandas as pd
import netCDF4 as nc

pathname = os.environ['HOME'] + \
    '/Dropbox/bmop/Processamento/data/CF1_BMOBR05_2016Nov/'

filename = 'cf1nov16.csv'

dd = pd.read_csv(pathname + filename, index_col='date', parse_dates=True)

cf1 = nc.Dataset('teste.nc', 'w', format='NETCDF4')

cf1.close()
# print (cf1)
# print (cf1.fileformat)