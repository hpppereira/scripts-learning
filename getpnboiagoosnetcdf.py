'''
Baixa dados do PNBOIA em .nc, concatena e salva em
/dados/op/
'''

import netCDF4 as nc
import matplotlib.pyplot as plt


buoy = nc.Dataset('http://goosbrasil.org/pnboia/dados/B69153_argos.nc')


import urllib
from netCDF4 import Dataset
import matplotlib.pyplot as pl
import os

dirout = os.environ['HOME'] + '/Dropbox/pnboia/dados/op/nc/'

site = 'http://www.goosbrasil.org/pnboia/dados/'

#site adress
siteB69008 = site + 'B69008_argos.nc' #recife
siteB69007 = site + 'B69007_argos.nc' #porto seguro
siteB69009 = site + 'B69009_argos.nc' #baia guanabara
siteB69150 = site + 'B69150_argos.nc' #santos
siteB69152 = site + 'B69152_argos.nc' #florianopolis
siteB69153 = site + 'B69153_argos.nc' #rio grande

#baixa o dado
print 'Baixando dado de Recife - B69008_argos'
urllib.urlretrieve(siteB69008, filename=dirout+"B69008_argos.nc")
print 'Baixando dado de Porto Seguro - B69007_argos'
urllib.urlretrieve(siteB69007, filename=dirout+"B69007_argos.nc")
print 'Baixando dado da Baia de Guanabara - B69009_argos'
urllib.urlretrieve(siteB69009, filename=dirout+"B69009_argos.nc")
print 'Baixando dado de Santos - B69150_argos'
urllib.urlretrieve(siteB69150, filename=dirout+"B69150_argos.nc")
print 'Baixando dado de Florianopolis - B69152_argos'
urllib.urlretrieve(siteB69152, filename=dirout+"B69152_argos.nc")
print 'Baixando dado de Rio Grande - B69153_argos'
urllib.urlretrieve(siteB69153, filename=dirout+"B69153_argos.nc")



#lon = buoy.variables['longitude'][:]
#lat = buoy.variables['latitude'][:]
