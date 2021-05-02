curso_aula3

import glob #lista os arquivos que tem em uma pasta

pathname = '/Users/rsoutelino/'
filelist = glob.glob(pathname + "*.cnv") #lista os arquvos que tem .cnv

lon, lat, temp = [], [], []
intervalo = 1000

for file in filelist:

	f = open(file)
	lines = f.readlines()

	for k in range(len(lines)):
			.
			.
			.
			.
			.





#observações

para dar um tab em um bloco do script, selecionar
o bloco e dar tab. para fazer o contrario, dar shft+tab

#instalar o base map. está no EPD dentro do matplotlib
se for instalar separado ele nao está no matplotlib

from mpltoolkit import Basemap

m = Basemap(projection='cyl', ........)



#interpolacao
from matplotlib import delaunay

tri = delaunay.Triangulation(lon, lat)

#cria interpolador
interp = tri.nn.interpolator(temp)

xg = linspace(lon.min(), lon.max(), 60)
yg = linspace(lat.min(), lat.max(), 80)
xg, yg = meshgrid(xg, yg)

tempI = interp(xg, yg)

m.countourf(xg, yg, tempI, 60); colorbar()


#para saber como fazer o grafico
ir no site matplotlib.org, na galeria, e la mostra o tipo do grafico
e o script

#para importar biblioteca de plotagem 3d tem que 
#importar da biblioteca mpl_toolkit

# matplotlib.org/basemap/

#TRABALHANDO COM NETCDF E MAPAS

import netCDF4 as nc

datafile = nc.Dataset('.....')

#importar datetime

import datetime as dt

data = dt.date.today()

