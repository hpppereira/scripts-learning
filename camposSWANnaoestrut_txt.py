'''
cria grafico de contorno
da saida do swan com grade nao estruturada
'''

# import pylab as pl
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import scipy.io
from scipy import interpolate
from scipy.interpolate import interp1d
import os
from matplotlib.collections import PolyCollection
from utmToLatLng import utmToLatLng

# plt.close('all')

# -------------------------------------------------------------- #
#diretorio dos resultados
pathname = os.environ['HOME'] + '/Dropbox/SWAN/NEST_VIX/'
name='table_grid.out'

#pathname da linha de costa
pathnamel = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/dados/linhadecosta/polig/'

pols = os.listdir(pathnamel)

#??
numpoly, numverts = 100, 6

print 'Criando mapa base...'
verts = []
for p in pols:
    #carrega cada latlon
    dd = np.loadtxt(pathnamel + p)
    verts.append(zip(dd[:,0],dd[:,1]))

#???
# z = np.random.random(numpoly) * 500
z = np.ones(100) *3

# -------------------------------------------------------------- #
#dados

# dd1 = scipy.io.loadmat('teste_gradepequena.mat')
dd = scipy.io.loadmat('teste.mat')

#ver os indices
#dd.viewkeys()

# -------------------------------------------------------------- #

#double para mudar o formato do array - tira o float32
print 'Carregando dados...'
lon = np.double(dd.values()[7][0])
lat = np.double(dd.values()[6][0])
hs = np.double(dd.values()[0][0])
dp = np.double(dd.values()[10][0])

#converte utm para latlon
zone = 24
easting = lon
northing = lat
latlon = []
for i in range(len(easting)):
	latlon.append(utmToLatLng(zone, easting[i] ,northing[i], northernHemisphere=False))

latlon = np.array(latlon)
lat = latlon[:,0]
lon = latlon[:,1]

#latitude e longitude interpolada
loni = np.arange(min(lon), max(lon), 0.00025)
lati = np.arange(min(lat), max(lat), 0.00025)
# loni = lon
# lati = lat

print 'Iniciando o meshgrid...'
[lons,lats] = np.meshgrid(loni,lati,sparse=False,copy=False)

print 'Iniciando o griddata de Hs...'
hss = mpl.mlab.griddata(lon,lat,hs,lons,lats,interp='linear'); #a interp linear e a nn ficaram praticamente iguais
print 'Iniciando o griddata de Dp...'
dps = mpl.mlab.griddata(lon,lat,dp,lons,lats,interp='linear');

print 'Iniciando o pcolormesh...'
fig, ax = plt.subplots()
cs = plt.pcolormesh(lons,lats,hss,shading='flat',cmap=plt.cm.jet,vmin=np.nanmin(hs),vmax=np.nanmax(hs))

print 'Iniciando o quiver...'
quiversca=35
quirverwi=0.003
e = 50 #espacamento para o quiver
plt.quiver(lons[0:-1:e,1:-1:e],lats[0:-1:e,1:-1:e],np.cos(dps[0:-1:e,1:-1:e]*np.pi/180),np.sin(dps[0:-1:e,1:-1:e]*np.pi/180),scale=quiversca,width=quirverwi)

cb = plt.colorbar(cs)
coll = PolyCollection(verts, edgecolors='black',facecolor='gray',closed=False)
ax.add_collection(coll)
ax.autoscale_view()
plt.axis([np.min(lon),np.max(lon),np.min(lat),np.max(lat)])
plt.title(' SWAN Hs Swell (m) e Direcao de pico / Hs Swell and Peak Direction  ') #+datetime.datetime.strftime(datat[t],"%d/%m/%Y %H")+'Z', fontsize=7)

plt.savefig('hs_swan_naoestr_semdif.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=False, bbox_inches=None, pad_inches=0.1)



plt.show()


#     fig, ax = plt.subplots()
#     cs=plt.contourf(xx[:,:],yy[:,:],Hsswell1[:,:],levelsswell)
#     plt.quiver(xx[1:ny:dyn,1:nx:dxn],yy[1:ny:dyn,1:nx:dxn],dir_x[1:ny:dyn,1:nx:dxn],dir_y[1:ny:dyn,1:nx:dxn],scale=quiversca,width=quirverwi)

#     cb=plt.colorbar(cs)
#     cb.set_label('Hs Swell (m)',size=13)
#     # Make the collection and add it to the plot.
#     coll = PolyCollection(verts, edgecolors='black',facecolor='gray',closed=False)
#     ax.add_collection(coll)
#     ax.autoscale_view()
#     axis([lonini, lonfi, latini, latfi])
#     title(' SWAN Hs Swell (m) e Direcao de pico / Hs Swell and Peak Direction  '+datetime.datetime.strftime(datat[t],"%d/%m/%Y %H")+'Z', fontsize=7)
