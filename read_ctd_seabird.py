#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

import glob
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import delaunay

pathname = '/Users/rsoutelino/Desktop/CursoPython/leste2_brutos/'
filelist = glob.glob(pathname + "*.cnv")


lon, lat, temp = [], [], []
begin, end = 0, 200

latFile = []
lonFile = []

for file in filelist:
	print file[-10:]
	f = open(file)
	lines = f.readlines()

	t = []

	for k in range(len(lines[begin:end])):
		# Gravando a latitude
		if "**" in lines[k] and " S" in lines[k]:
			latG = int(lines[k].split(' ')[3])
			latM = float(lines[k].split(' ')[4])
			lat.append( (-1) * (latG + latM / 60) )
			latFile.append(file)

		# Gravando a longitude		
		if "**" in lines[k] and " W" in lines[k]:
			lonG = int(lines[k].split(' ')[3])
			lonM = float(lines[k].split(' ')[4])
			lon.append( (-1) * (lonG + lonM / 60) )
			lonFile.append(file)

		if "*" not in lines[k] and "#" not in lines[k]:
			t.append( float(lines[k].split()[1] ) )



	
	t = np.array(t)	
	temp.append(t.mean())
	print str(t.mean()) + "\n"


lon = np.array(lon)
lat = np.array(lat)
temp = np.array(temp)


m = Basemap(projection='cyl', llcrnrlat=lat.min()-1, 
	        urcrnrlat=lat.max()+1,
            llcrnrlon=lon.min()-1, urcrnrlon=lon.max()+1, 
            lat_ts=0, resolution='i')


mlon, mlat = m(lon, lat)

plt.figure(facecolor='w', figsize=(6, 8))
m.bluemarble()
m.plot(mlon, mlat, '.y', markersize=10)
m.drawstates(linewidth=3)
m.drawrivers()
m.drawcoastlines()
m.drawparallels(np.arange(-25, -10, 2), color='gray', 
	            dashes=[1, 1], labels=[1, 1, 0, 0])

m.drawmeridians(np.arange(-60, 10, 3), color='gray', 
	            dashes=[1, 1], labels=[0, 0, 1, 1])

plt.savefig('mapa_estacoes.pdf')
plt.show()


# INTERPOLACAO

tri = delaunay.Triangulation(lon, lat)

interp = tri.linear_interpolator(temp)

xg = np.linspace(lon.min(), lon.max(), 60)
yg = np.linspace(lat.min(), lat.max(), 80)
xg, yg = np.meshgrid(xg, yg)

tempI = interp(xg, yg)

# for indices in tri.triangle_nodes:
# 	random_color = np.random.rand(3)
# 	plt.fill(lon[indices], lat[indices],facecolor=random_color)

mxg, myg = m(xg, yg)

plt.figure(facecolor='w', figsize=(6, 8))
m.fillcontinents(color='coral', lake_color='aqua')
m.contourf(mxg, myg, tempI, 60)
plt.colorbar()
m.drawstates(linewidth=3)
m.drawrivers()
m.drawcoastlines()
m.drawparallels(np.arange(-25, -10, 2), color='gray', 
	            dashes=[1, 1], labels=[1, 1, 0, 0])

m.drawmeridians(np.arange(-60, 10, 3), color='gray', 
	            dashes=[1, 1], labels=[0, 0, 1, 1])

plt.savefig('mapa_temperatura.pdf')
plt.show()














