# The program reads the output wave field files from wavewatch III v 3.14. Regional grid 2
# It allocates the matrix and generates the figures (if cfig=1). At the end, the program builds the netcdf output file. 
# Program thought for Linux/Unix environmental in case of using system calls (os.system). Otherwise it can be run on Windows or Linux.
#
# Ricardo Martins Campos (PhD student) 
# riwave@gmail.com
# +55 21 38654845    +55 21 84660434
# ----------------------------------------------------------------------------------------
# Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  
# MotorDePopa Wave Research Group
# ASA - CENPES/PETROBRAS 
# Rio de Janeiro - Brazil
# ----------------------------------------------------------------------------------------
# Contributions: Marcelo Andrioni (CENPES/PETROBRAS), Luiz Alexandre Guerra (CENPES/PETROBRAS).
# ----------------------------------------------------------------------------------------
# cfig=1 (build the figures), cfig=0 (no figures)
cfig=1









# Pay attention to the pre-requisites and libraries.
import os
from string import *
from numpy import *
from pylab import *

import datetime
from datetime import *
from time import strptime
from calendar import timegm
from matplotlib import dates


from mpl_toolkits.basemap import Basemap, shiftgrid, interp
import mpl_toolkits.basemap
import matplotlib.pyplot as plt

# Palette and colors for plotting the figures
from mpl_toolkits.basemap import cm
colormap = cm.GMT_polar
palette = plt.cm.jet
palette.set_bad('aqua', 10.0)
import matplotlib.colors as colors




levels=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,8]

# Make a list of files to read, organized and concatenated
os.system("ls *.hs > listahs.txt")
# Number of output files of ww3
os.system("wc -l listahs.txt > tamlistahs.txt")
# Allocate this number into a variable narq, which is the number of times
ft = open('tamlistahs.txt')
line = ft.readline()
line=line[0:-12]  # Name of nc file
narq=int(line)
os.system("rm -f tamlistahs.txt")

# Create markers position
lat_ms = [-42.1,-41.2,-40.3,-39.4,-38.5,-37.6,-36.7,-35.8,-34.9,-34.0];
lon_ms = [-29.0,-29.0,-29.0,-29.0,-29.0,-29.0,-29.0,-29.0,-29.0,-29.0];

# Take the grid parameters using the header of the first file     
fl = open('listahs.txt')
# Taking the name
line = fl.readline();name=line[0:-1];
# Openning the file
fa = open(name)
# Header
cabc=fa.readline()
# Initial date
datain=cabc[15:28];
# Name of the model
modelo=cabc[1:14];

grade=cabc[30:-44];
grade=grade.strip().split()
# Definitions of simulation grid
loni=float(grade[0])
lonf=float(grade[1])
nx=int(grade[2])
lati=float(grade[3])
latf=float(grade[4])
ny=int(grade[5])

# Latitudes and Longitudes
lon=linspace(loni,lonf,nx)
lat=linspace(lati,latf,ny)


if lon[0] < 0 and lon[-1] <= 0:
	lon_0=-(abs(lon[-1])+abs(lon[0]))/2.0
else:
	lon_0=(lon[0]+lon[-1])/2.0

if lat[0] < 0 and lat[-1] <= 0:
	lat_0=-(abs(lat[-1])+abs(lat[0]))/2.0
else:
	lat_0=(lat[0]+lat[-1])/2.0



# Multiplicative factor
ftm=float(cabc[76:83])

# Wavewatch writes the files using 6 columns.
nl=nx/6
# If the number of longitudes not divisible by 6
sobra=nx-(nx/6)*6
# Matrix containing the results
m=zeros((narq,ny,nx))

jday = []

# Loop to mount and concatenate the results
fl = open('listahs.txt')

for k in range(0, narq):

	# Take the name from the list
	line = fl.readline();name=line[0:-1];
	# Open
	fa = open(name)
	# Header
	cabc=fa.readline()
	# Date
	data=cabc[15:28];

	jday.append((timegm( strptime(data[0:8]+data[9:11], '%Y%m%d%H') ) - timegm( strptime('01/01/1950', '%d/%M/%Y') )) / 3600. / 24.)


	for j in range(0,ny):

		a=0
		for i in range(0,nl):
			l=fa.readline()
			l=l.strip().split()
			for n in range(0,6):
				m[k,ny-j-1,a]=int(l[n])*ftm
				a=a+1

		if sobra>0:
			l=fa.readline()
			l=l.strip().split()
			for n in range(0,sobra):
				m[k,ny-j-1,a]=int(l[n])*ftm
				a=a+1


	# Build the figures for each grid/time
	if cfig>0:

		fig=plt.figure(figsize=(7,8))
        
		map = Basemap(llcrnrlat=lat[0],urcrnrlat=lat[-1],\
		llcrnrlon=lon[0],urcrnrlon=lon[-1],\
		rsphere=(6378137.00,6356752.3142),\
		resolution='l',area_thresh=1000.,projection='cyl',\
		lat_1=lat[0],lon_1=lon[0],lat_0=lat_0,lon_0=lon_0)


		[mnlon,mnlat]=np.meshgrid(lon[:],lat[:])
		xx, yy = map(mnlon,mnlat)

		map.drawcoastlines(linewidth=1.2)
		map.drawcountries()
		map.drawstates()
                map.fillcontinents(color='#cc9966')
                map.drawmeridians(np.arange(-70,60,20),labels=[0,0,0,1],fontsize=10)
                map.drawparallels(np.arange(-90,90,20),labels=[1,0,0,0],fontsize=10)
               
		field = map.contourf(xx,yy,m[k,:,:],levels,cmap=palette,norm=colors.normalize(vmin=0,vmax=8,clip=False))

		map.scatter(lon_ms,lat_ms,2,marker='o',color='r')

		ax = plt.gca()
		pos = ax.get_position()
		l, b, w, h = pos.bounds
		cb = map.colorbar(field,"bottom", size="5%", pad="5%")
	#	cax = plt.axes([l+0.03, b-0.03, w-0.05, 0.03]) # setup colorbar axes.
	#	plt.colorbar(cax=cax)#,orientation='horizontal') # draw colorbar
		plt.axes(ax)  # make the original axes current again

		title(modelo+' Altura Significativa - Hs (m) '+data[0:8]+' '+data[9:11]+'Z')
		savefig('hs'+data[0:8]+data[9:11]+'.png', dpi=None, facecolor='w', edgecolor='w',
		orientation='portrait', papertype=None, format='png',
		transparent=False, bbox_inches=None, pad_inches=0.1)

		plt.close()




os.system("rm -rf listahs.txt")


from pupynere import netcdf_file
from numpy import array
from numpy import arange, dtype 


# open a new netCDF file for writing.
ncfile = netcdf_file('hs'+datain[0:8]+datain[9:11]+'.nc','w')

# create the lat and lon dimensions.
ncfile.createDimension( 'time' , m.shape[0] )
ncfile.createDimension( 'latitude' , m.shape[1] )
ncfile.createDimension( 'longitude' , m.shape[2] )
# Define the coordinate variables. They will hold the coordinate
# information, that is, the latitudes and longitudes.
ti = ncfile.createVariable('time',dtype('float32').char,('time',))
lats = ncfile.createVariable('latitude',dtype('float32').char,('latitude',))
lons = ncfile.createVariable('longitude',dtype('float32').char,('longitude',))
# Assign units attributes to coordinate var data. This attaches a
# text attribute to each of the coordinate variables, containing the
# units.
ti.units     = 'days since 1950-01-01 00:00:00' 
lats.units = 'degrees_north'
lons.units = 'degrees_east'
# write data to coordinate vars.
ti [:] = jday
lats[:] = lat
lons[:] = lon
# create  variable
hs = ncfile.createVariable('hs',dtype('float32').char,('time','latitude','longitude'))
# set the units attribute.
hs.units = 'm'
# write data to variables.
hs[:,:,:] = m[:,:,:]
# close the file
ncfile.close()


