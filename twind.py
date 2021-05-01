# Take a time series wind at some pre-defined point of a netcdf input data
# It always find the nearest grid point to your desired point (never interpolating). 
# Ricardo Martins Campos (PhD student)  13/11/2012
# riwave@gmail.com
# +1 202 5531739 
# ----------------------------------------------------------------------------------------
# Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  - Rio de Janeiro - Brazil 
# MotorDePopa Wave Research Group
# NCEP / NOAA - National Weather Service 
# ----------------------------------------------------------------------------------------
# Edited by: 
# ----------------------------------------------------------------------------------------
# Contributions:
# ----------------------------------------------------------------------------------------

# Position (latitude longitude) of your point.
latp=-32.8652
lonp=-50.8879
# --------------------------------------------------------------------------



import matplotlib
matplotlib.use('Agg')

import os
from pupynere import NetCDFFile as nc
from numpy import *
from pylab import *
from matplotlib import dates
import datetime
from datetime import timedelta, datetime
import numpy as np

from mpl_toolkits.basemap import Basemap, shiftgrid, interp
import mpl_toolkits.basemap
import matplotlib.pyplot as plt

import time
from calendar import timegm



os.system("wc -l lista.txt > tamlista.txt")
ft = open('tamlista.txt')
line = ft.readline()
narq=int(line.split()[0])
ft.close()
os.system("rm tamlista.txt")

f = open('lista.txt')
nt=0;
for i in range(0,narq):
	line = f.readline() 
	nomed=line[0:-1]  
	fu = nc(nomed, 'r')
	nt=nt+int(shape(fu.variables['time'][:])[0])
	fu.close()
f.close()


f = open('lista.txt')
line = f.readline() 
nomed=line[0:-1] 
fu = nc(nomed, 'r')  
lat=fu.variables['latitude'][:]     
lon=fu.variables['longitude'][:] 
u=fu.variables['UGRD_10maboveground'][0,:,:]
u,lon = shiftgrid(180.,u,lon,start=False)

indlon=find(abs(lon-lonp)==min(abs(lon-lonp)))
indlat=find(abs(lat-latp)==min(abs(lat-latp)))

up=zeros(nt,'f')
vp=zeros(nt,'f')
magp=zeros(nt,'f')
dirp=zeros(nt,'f')
ano=zeros(nt,'i4')
mes=zeros(nt,'i2')
dia=zeros(nt,'i2')
hora=zeros(nt,'i2')

k=0;
# loop of files
for t in range(0,narq):

	print(t+1)
	tempo=fu.variables['time'][:]
	for i in range(0,int(shape(fu.variables['time'])[0])):
		u=fu.variables['UGRD_10maboveground'][i,:,:]  
		v=fu.variables['VGRD_10maboveground'][i,:,:] 
		lon=fu.variables['longitude'][:] 
		u,lon = shiftgrid(180.,u,lon,start=False)		
		lon=fu.variables['longitude'][:] 
		v,lon = shiftgrid(180.,v,lon,start=False)

		up[k]=u[indlat,indlon]
		vp[k]=v[indlat,indlon]
		magp[k]=sqrt( (up[k]*up[k]) + (vp[k]*vp[k]) )
		dirp[k]=180+arctan2(up[k],vp[k])*180/pi

		ano[k]=int(time.gmtime(tempo[i])[0])
		mes[k]=int(time.gmtime(tempo[i])[1])
		dia[k]=int(time.gmtime(tempo[i])[2])
		hora[k]=int(time.gmtime(tempo[i])[3])
#		print(k)
		k=k+1;

	fu.close()	
	if t<(narq-1):
		line = f.readline() 
		nomed=line[0:-1]  
		fu = nc(nomed, 'r')


f.close()




# Text output with the date and values of U, V, Wind Int., Wind Dir.

vf=file('localwind.txt','w')
vf.write('% Surface Wind CFSR at point  Lat: '+repr(round(lat[indlat],4))+'  Lon: '+repr(round(lon[indlon],4)) )
vf.write('\n')
vf.write('%     Date          U_Wind(m/s)    V_Wind(m/s)   Wind_Int(m/s)    Wind_Dir(m/s)')
vf.write('\n')
np.savetxt(vf,zip(ano,mes,dia,hora,up,vp,magp,dirp),fmt="%4i %2i %2i %2i %14.3f %14.3f %14.3f %16.1f",delimiter='/t') 
vf.close


