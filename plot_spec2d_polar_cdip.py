# https://cdip.ucsd.edu/themes/media/docs/documents/html_pages/polar.html
# https://matplotlib.org/cmocean/#solar
# https://cdip.ucsd.edu/themes/media/docs/documents/html_pages/period_rose.html
# https://scipy-lectures.org/intro/matplotlib/auto_examples/plot_polar.html
# https://matplotlib.org/3.1.0/gallery/pie_and_polar_charts/polar_scatter.html
# https://matplotlib.org/3.3.4/gallery/pie_and_polar_charts/polar_demo.html
# https://stackoverflow.com/questions/54208214/matplotlib-polar-contourf-plot-continuous-across-theta-origin

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import urllib
import time
import calendar
import datetime

stn = '071'
startdate = "03/06/2021 16:00"

urlarc = 'http://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/archive/' + stn + 'p1/' + stn + 'p1_historic.nc'

nc = netCDF4.Dataset(urlarc)

timevar = nc.variables['waveTime'][:]

# Find nearest value in numpy array
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

# Convert to unix timestamp
def getUnixTimestamp(humanTime,dateFormat):
    unixTimestamp = int(calendar.timegm(datetime.datetime.strptime(humanTime, dateFormat).timetuple()))
    return unixTimestamp

# Convert to human readable timestamp
def getHumanTimestamp(unixTimestamp, dateFormat):
    humanTimestamp = datetime.datetime.utcfromtimestamp(int(unixTimestamp)).strftime(dateFormat)
    return humanTimestamp

unixtimestamp = getUnixTimestamp(startdate, "%m/%d/%Y %H:%M")
unix_nearest = find_nearest(timevar, unixtimestamp)  # Find the closest unix timestamp
neardate = getHumanTimestamp(unix_nearest, '%Y%m%d%H%M') # Convert unix timestamp to string format to attach to URL

url = 'http://cdip.ucsd.edu/data_access/MEM_2dspectra.cdip?sp' + stn + '01' + neardate
# url = 'http://cdip.ucsd.edu/data_access/MEM_2dspectra.cdip?029'
# url = 'http://cdip.ucsd.edu/data_access/MEM_2dspectra.cdip?sp21501202103050000'

# data = urllib.request.urlopen(url)
# readdata = data.read() # Read text file of recent data
# datas = bytes(readdata.split("\n")) # Split text file into individual rows

# datas2 = []

for item in datas:
     line = item.strip().split()
     datas2.append(line) 
        
datas2[0].remove('<pre>')
datas2[64].remove('</pre>')
datas2 = filter(None, datas2)

Edarray = np.asarray(datas2, dtype=object)
Ednew = np.append(Edarray,Edarray[:,0:1],1)

