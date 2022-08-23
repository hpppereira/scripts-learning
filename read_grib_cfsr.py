"""
Leitura e plotagem dos dados do CFSR em grib2
Henrique Pereira
25/01/2018

Links uteis
http://www.himpactwxlab.com/home/how-to-wiki/write-grib2-data-with-pygrib

"""

import os
import pygrib

#latlon recife
lat_rcf = -8.1536
lon_rcf = -34.5595 + 180 # se for negativo, soma 180

pathname = os.environ['HOME'] + '/Dropbox/Database/CFSR/'

filename = 'wnd10m.cdas1.201212.grb2'

grbs = pygrib.open(pathname + filename)

grb=grbs[1]

# extract the grib lat/lon values
# lat, lon = grb.latlons()

# extract data and get lat/lon values for a subset
data, lats, lons = grb.data(lat1=lat_rcf,lat2=lat_rcf+.1,lon1=lon_rcf,lon2=lon_rcf+.1)

# data.shape, lats.min(), lats.max(), lons.min(), lons.max()
