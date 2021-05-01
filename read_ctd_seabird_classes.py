#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

import glob
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import delaunay


pathname = '/Users/rsoutelino/Desktop/CursoPython/leste2_brutos/'


class PlotSeaBird(object):
	""" Esta classe serve para plotar dados das estacoes de coleta dos CTD-Seabird"""

	def __init__(self, path):
	
		self.main_path = path
		self.filelist = glob.glob(path + "*.cnv")
	
		self.lon, self.lat, self.temp = [], [], []

		self.latFile = []
		self.lonFile = []


	def carregar_lat_lon_temp(self, begin=0, end=100):
		''' Esse metodo carrega os dados de temperatura 
			begin :: int
			end   :: int

			retorna nada
 		'''
		for file in self.filelist:
			print file[-10:]
			f = open(file)
			lines = f.readlines()

			t = []

			for k in range(len(lines[begin:end])):
				self.lat = list(self.lat)
				self.lon = list(self.lon)
				self.temp = list(self.temp)
				# Gravando a latitude
				if "**" in lines[k] and " S" in lines[k]:
					latG = int(lines[k].split(' ')[3])
					latM = float(lines[k].split(' ')[4])
					self.lat.append( (-1) * (latG + latM / 60) )
					self.latFile.append(file)

				# Gravando a longitude		
				if "**" in lines[k] and " W" in lines[k]:
					lonG = int(lines[k].split(' ')[3])
					lonM = float(lines[k].split(' ')[4])
					self.lon.append( (-1) * (lonG + lonM / 60) )
					self.lonFile.append(file)

				if "*" not in lines[k] and "#" not in lines[k]:
					t.append( float(lines[k].split()[1] ) )
			
			t = np.array(t)		
			self.temp.append(t.mean())
			print str(t.mean()) + "\n"
		self.lon = np.array(self.lon)
		self.lat = np.array(self.lat)
		self.temp = np.array(self.temp)	


	def plotar_mapa_base(self):

		m = Basemap(projection='cyl', llcrnrlat=self.lat.min()-1, 
			        urcrnrlat=self.lat.max()+1,
		            llcrnrlon=self.lon.min()-1, urcrnrlon=self.lon.max()+1, 
		            lat_ts=0, resolution='i')


		mlon, mlat = m(self.lon, self.lat)

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

		plt.show()

	def salvar_figura(self, filename):
		plt.savefig(filename)
		

	def interpolar(self):

		# INTERPOLACAO

		tri = delaunay.Triangulation(self.lon, self.lat)

		interp = tri.linear_interpolator(self.temp)

		xg = np.linspace(self.lon.min(), self.lon.max(), 60)
		yg = np.linspace(self.lat.min(), self.lat.max(), 80)
		xg, yg = np.meshgrid(xg, yg)

		self.tempI = interp(xg, yg)

		# for indices in tri.triangle_nodes:
		# 	random_color = np.random.rand(3)
		# 	plt.fill(lon[indices], lat[indices],facecolor=random_color)

		self.mxg, self.myg = m(xg, yg)

	def plotar_dados(self):

		self.fig = plt.figure(facecolor='w', figsize=(6, 8))
		m.fillcontinents(color='coral', lake_color='aqua')
		m.contourf(self.mxg, self.myg, self.tempI, 60)
		plt.colorbar()
		m.drawstates(linewidth=3)
		m.drawrivers()
		m.drawcoastlines()
		m.drawparallels(np.arange(-25, -10, 2), color='gray', 
			            dashes=[1, 1], labels=[1, 1, 0, 0])

		m.drawmeridians(np.arange(-60, 10, 3), color='gray', 
			            dashes=[1, 1], labels=[0, 0, 1, 1])
		plt.show()














