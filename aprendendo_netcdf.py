## Aprendendo netcdf

from netCDF4 import Dataset

#nome do arquivo a ser carregado
arq1 = 'GW_L2P_ALT_CRYO_GDR_20100715_083816_20100715_091940_004_358.nc'

#carrega o arquivo
#O dataset serve para abrir e criar arquivos netcdf
rootgrp = Dataset('arq1', 'w', format='NETCDF4')

#imprimeo o formato do arquivo
print rootgrp.file_format

rootgrp.close()