# pip install netcdf4 matplotlib

from netCDF4 import Dataset
import matplotlib.pyplot as pl


dd = Dataset('/usr/local/tds/apache-tomcat-8.5.11/content/thredds/public/testdata/testData.nc')

stop

lon = buoy.variables['longitude'][:]
lat = buoy.variables['latitude'][:]

pl.plot(lon, lat)
pl.plot(lon[-1], lat[-1], 'r.', markersize=10)
pl.axis('equal')
pl.show()
