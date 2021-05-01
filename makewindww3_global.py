# Routine for reading netcdf (.nc) wind fieds and creating input text files for Wavewatch III 
# Program thought for Linux/Unix environmental in case of using system calls (os.system). Otherwise it can be run on Windows or Linux. 
# 01/12/2011
# Author:
# Ricardo Martins Campos (PhD student) 
# riwave@gmail.com
# +55 21 38654845    +55 21 84660434
# ----------------------------------------------------------------------------------------
# Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  
# MotorDePopa Wave Research Group
# ASA - CENPES/PETROBRAS 
# Rio de Janeiro - Brazil
# ----------------------------------------------------------------------------------------
# Contributions: Izabel Nogueira (Lioc/PENO/COPPE/UFRJ), Marcelo Andrioni (CENPES/PETROBRAS), Luiz Alexandre Guerra (CENPES/PETROBRAS).
#                ...
# ------------------------------------------------------------------------------------------------------------------------------------
# Initially designed to deal with CFSR/NCEP Wind files, which contain one month data and have  
#                           Spatial Resolution ~ 0.3125
#                           Time resolution = 1 hour
# CFSR wind files are available at : http://nomads.ncdc.noaa.gov/data/cfsr/
#
# The program wgrib2 (NCEP/NOAA) is a great option to convert wgrb2 files into netcdf format  
# It can be downloaded at: http://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/
# Another very good program is CDO that can be easily installed with synaptic/Ubuntu (sudo apt-get install CDO)
# ----------------------------------------------------------------------------------------
# Examples:
# cdo -f nc copy wnd10m.gdas.199407.grb2 wnd10m.gdas.199407.nc
# wgrib2 wnd10m.gdas.199407.grb2 -netcdf wnd10m.gdas.199407.nc
# -----------------------------------------------------------------
#   Defining grid domain, related to the input grid of WW3
# -----------------------------------------------------------------
#latitude
lati=-82
latf=+82
# --------------------------------------------------------------------------
# Initial date. To avoid problems reading the time variable from netcdf file
iyear=1992
imonth=8
iday=1
ihour=0
# Time interval (hours)
dt=1 
# ---------------------------------------------------------------------------------------
# Flag for creating wind figures. cfig=1 create. cfig=0 does not create and save run time
cfig=1;
# ---------------------------------------------------------------------------------------------------------------
# For running program using just one netcdf input file, write the name here. Otherwise comment the following line
name='wnd10m.gdas.199208.nc';tn=1
rname='CFSR'
# Wind intensity range, for plotting figures. 
vmin=5; vmax=25
# svec is very important for figure wind vectors! If it is too poluted (too many vectors at the same figure range) increase this value
svec=20;
# If you want to modify the length of vector, chance the "scale" parameter at map.quiver plot 




# Pay attention to the pre-requisites and libraries.
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

from time import strptime
from calendar import timegm

# Paleta de cores para a plotagem
from mpl_toolkits.basemap import cm
colormap = cm.GMT_polar
palette = plt.cm.OrRd
palette.set_bad('aqua', 10.0)
import matplotlib.colors as colors


# leap years
p=array([1948,1952,1956,1960,1964,1968,1972,1976,1980,1984,1988,1992,1996,2000,2004,2008,2012,2016])
# Log file where processes will be written 
fl = open('log_windWW3.txt', 'w')
fl.write('=========== Tasks and processes done by makewindww3.py ===========\n')
fl.write('  \n')

# In case you are interested in concatenating more than one file (just for Linux, otherwise comment # the next lines):
# Pay attention if your netcdf files can be directly concatenated, i.e, if the end-time of previous file is exactly before the first time of next file
# If not, it is preferible to generate monthly files separetaly. This is why I commented # next lines
# listing files using bash commands 
# os.system("ls *.nc > list.txt")
# os.system("wc -l list.txt > nllist.txt")
# fl.write('Set up the list of files and its length \n')
# tm=open('nllist.txt')
# tline=tm.readline();tm.close()
# Number of files 
# tn=int(tline[0:-9])
# Opening the first file, just for taking the features, set some variables and save time inside the loop
# f = open('list.txt')
# name = f.readline();name=name[0:-1]
# f.close()



# Open the netcdf file
fu = nc(name, 'r')  
# These variable names inside [] is defined by CFSR/wgrib2. If you have converted the grib file with another program rewrite these names 
lat=fu.variables['latitude'][:]
lon=fu.variables['longitude'][:]
uwnd=fu.variables['UGRD_10maboveground'][:]
# Taking the argument (index) of boundaries, i.e., initial/final latitudes and longitudes
# considering lat starting from north hemisphere (positive values) decreasing to the south
lixo,lon = shiftgrid(180.,uwnd[0,:,:],lon,start=False)

dife=abs(lat[:]-lati)
alati=dife.argmin()
if lati-lat[alati] < 0:
	alati=alati-1

dife=abs(lat[:]-latf)
alatf=dife.argmin()
if latf-lat[alatf] > 0:
	alatf=alatf+1



[mnlon,mnlat]=np.meshgrid(lon[:],lat[alati:alatf])
if lon[0] < 0 and lon[-1] <= 0:
	lon_0=-(abs(lon[-1])+abs(lon[0]))/2.0
else:
	lon_0=(lon[0]+lon[-1])/2.0

if lat[alati] < 0 and lat[alatf] <= 0:
	lat_0=-(abs(lat[alatf])+abs(lat[alati]))/2.0
else:
	lat_0=(lat[alati]+lat[alatf])/2.0





# writing informations to log_windWW3.txt
fl.write('Took the latitudes and longitudes related to wind grid arguments.\n')
fl.write('------------------------------------------------------------------------------\n')
fl.write('PAY ATTENTION. The real initial/final latitudes and longitudes are:\n')
fl.write('Latitudes:  Initial: '+repr(round(lat[alati],6))[0:10]+'   Final: '+repr(round(lat[alatf],6))[0:10]+'    Length='+repr(lat[alati:alatf+1].shape[0])+'   \n')
fl.write('Longitudes:  Initial: '+repr(round(lon[0],6))[0:10]+'   Final: '+repr(round(lon[-1],6))[0:10]+'    Length='+repr(lon[:].shape[0])+'  \n')
fl.write('------------------------------------------------------------------------------\n')


lat=fu.variables['latitude'][alati:alatf+1]
fu.close()
# levels for shaded fields at figures.
#levels=linspace(vmin,vmax,10)
levels=[0,2,4,6,8,10,12,14,16,18,20,25,30]

# f = open('list.txt')

# Output text file with the U and V wind components written according to wavewatch input text format
vf=file('windWW3.txt','w')  

fl.write('Program opened the files...Starting loops  \n')
fl.write('  \n')

# starting the loop for tn (number of netcdf data files)
# Pay attention to the variable names. It was set to cfsr data converted with wgrib2 program. 
for tn in range(0,tn):

	# open netcdf input file and read time variable.
	# name = f.readline();name=name[0:-1]
	fu = nc(name, 'r')
	# These name inside [] is defined by CFSR/wgrib2. If you have converted the grib file with another program rewrite these names 
	time=fu.variables['time'][:]

	for t in range(0,time.shape[0]):
	#for t in range(0,2):
		# These names inside [] is defined by CFSR/wgrib2. If you have converted the grib file with another program rewrite these names 
		uwnd=fu.variables['UGRD_10maboveground'][t,alati:alatf+1,:]
		vwnd=fu.variables['VGRD_10maboveground'][t,alati:alatf+1,:]
		magn=sqrt((uwnd*uwnd)+(vwnd*vwnd)) 
		# Converting longitudes to -180/180 instead of 0 360
		# These names inside [] is defined by CFSR/wgrib2. If you have converted the grib file with another program rewrite these names


		lon=fu.variables['longitude'][:]	
		magn,lon = shiftgrid(180.,magn,lon,start=False)
		lon=fu.variables['longitude'][:]
		uwnd,lon = shiftgrid(180.,uwnd,lon,start=False)
		lon=fu.variables['longitude'][:]
		vwnd,lon = shiftgrid(180.,vwnd,lon,start=False)


		# Writing and saving header and wind matrix 
		if imonth<10:
			rmonth='0'+repr(imonth)
		else:
			rmonth=repr(imonth)

		if iday<10:
			rday='0'+repr(iday)
		else:
			rday=repr(iday)

		if ihour<10:
			rhour='0'+repr(ihour)
		else:
			rhour=repr(ihour)	

		# write date using WW3 format
		vf.write(repr(iyear));vf.write(rmonth);vf.write(rday);vf.write('  ');vf.write(rhour);vf.write('0000');
		vf.write('\n')
		# write U component of wind using WW3 format
		np.savetxt(vf,flipud(uwnd[:,:]),fmt="%10.3f",delimiter='')   
		# write V component of wind using WW3 format
		np.savetxt(vf,flipud(vwnd[:,:]),fmt="%10.3f",delimiter='')   

		fl.write('Wrote date and U/V matrixes - '+repr(iyear)+rmonth+rday+'  '+rhour+'0000  \n')

		# Setting date/time 
		ihour=ihour+dt

		if ihour>23:
			ihour=0
			iday=iday+1

		if imonth==2:
			if min(abs(p-iyear))==0:
				if iday>29:   
					iday=1
					imonth=1
			else:
				if iday>28:   
					iday=1
					imonth=1

		if iday>31:
			iday=1
			imonth=imonth+1
              
		if imonth==4 or imonth==6 or imonth==9 or imonth==11:
			if iday>30:
				iday=1
				imonth=imonth+1

		if imonth>12:
			imonth=1
			iday=1
			iyear=iyear+1

		# ---------------------
		# Creating figures with basemap




		if cfig==1:


			fig=plt.figure(figsize=(10,6))	
			map = Basemap(llcrnrlat=lat[0],urcrnrlat=lat[-1],\
			llcrnrlon=lon[0],urcrnrlon=lon[-1],\
			rsphere=(6378137.00,6356752.3142),\
			resolution='l',area_thresh=1000.,projection='cyl',\
			lat_1=lat[0],lon_1=lon[0],lat_0=lat_0,lon_0=lon_0)

			map.drawcoastlines(linewidth=1.2)
			map.drawcountries()
#			map.fillcontinents(color='gray')
#			map.drawmeridians(np.arange(round(lon.min()),round(lon.max()),40),labels=[0,0,0,1])
#			map.drawparallels(np.arange(round(lat.min()),round(lat.max()),20),labels=[1,0,0,0])

#			plt.text(0.05, 0.05, "Ricardo Campos  Lioc-COPPE/UFRJ", ha="center",fontsize=6)

			map.imshow(magn,palette,norm=colors.normalize(vmin=vmin,vmax=vmax,clip=False))

			ax = plt.gca()
			pos = ax.get_position()
			l, b, w, h = pos.bounds
			cax = plt.axes([l+0.03, b+0.01, w-0.05, 0.03]) # setup colorbar axes.
			plt.colorbar(cax=cax,orientation='horizontal') # draw colorbar
			plt.axes(ax)  # make the original axes current again

			# plotagem dos vetores em cima do campo de intensidade do vento
			sk=7
			[mnlon,mnlat]=np.meshgrid(lon[::sk],lat[::sk])
			xx, yy = map(mnlon,mnlat)
			Q = map.quiver(xx,yy,uwnd[::sk,::sk],vwnd[::sk,::sk],width=0.001,scale=1000)


			title('Surface Wind (m/s) '+rname+'  '+repr(iyear)+rmonth+rday+'  '+rhour+' Z')
		        savefig('wind'+repr(iyear)+rmonth+rday+rhour+'.png', dpi=None, facecolor='w', edgecolor='w',
		        orientation='portrait', papertype=None, format='png',
		        transparent=False, bbox_inches=None, pad_inches=0.1)
		        plt.close()
			fl.write('Created figure: '+repr(iyear)+rmonth+rday+'  '+rhour+'0000  \n')




	fl.write('  \n')
	fl.write('Finished the file: '+name+'  \n')


	fu.close()







fl.close()
vf.close()
# f.close()
# In case you want to run an animation (only for linux):
# os.system("convert -delay 10 -loop 0 *.png animaion.gif")

