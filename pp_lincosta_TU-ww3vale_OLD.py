'''
Plotagem da linha de costa
do Porto de Tubarao'''

import os
import numpy as np
import pylab as pl
# from mpl_toolkits.basemap import Basemap
# import matplotlib.pyplot as plt
# from matplotlib.collections import PolyCollection
# from utmToLatLng import *
# import scipy.io as sio

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/dados/linhadecosta/'

latlon = np.loadtxt(pathname + 'linha_costa_TU_latlon.txt')
# latlon = np.loadtxt(pathname + 'latlon_TU.txt',delimiter=',')
# latlon = np.loadtxt(pathname + '/polig/latlon_cont_TU.txt')

lon = latlon[:,0]
lat = latlon[:,1]


cont = range(0,1191) #continente
il1 = range(1191,1211) #ilha1
il2 = range(1211,1222) #ilha2
il3 = range(1222,1228) #ilha3
il4 = range(1228,1238)
il5 = range(1238,1249)
il6 = range(1249,1256)
il7 = range(1256,1282)
il8 = range(1282,1297)
il9 = range(1297,1303)
il10 = range(1303,1321)
il11 = range(1321,1334)
il12 = range(1334,1345)
il13 = range(1345,1360)
il14 = range(1360,1368)
il15 = range(1368,1377)
il16 = range(1377,1391)
il17 = range(1391,1405)
il18 = range(1405,1412)
il19 = range(1412,1432)



pl.plot(lon[cont],lat[cont],'.-')
pl.plot(lon[il1],lat[il1],'.-')
pl.plot(lon[il2],lat[il2],'.-')
pl.plot(lon[il3],lat[il3],'.-')
pl.plot(lon[il4],lat[il4],'.-')
pl.plot(lon[il5],lat[il5],'.-')
pl.plot(lon[il6],lat[il6],'.-')
pl.plot(lon[il7],lat[il7],'.-')
pl.plot(lon[il8],lat[il8],'.-')
pl.plot(lon[il9],lat[il9],'.-')
pl.plot(lon[il10],lat[il10],'.-')
pl.plot(lon[il11],lat[il11],'.-')
pl.plot(lon[il12],lat[il12],'.-')
pl.plot(lon[il13],lat[il13],'.-')
pl.plot(lon[il14],lat[il14],'.-')
pl.plot(lon[il15],lat[il15],'.-')
pl.plot(lon[il16],lat[il16],'.-')
pl.plot(lon[il17],lat[il17],'.-')
pl.plot(lon[il18],lat[il18],'.-')
pl.plot(lon[il19],lat[il19],'.-')



# pl.fill(lon,lat,'-')
# pl.grid()


# pl.show()


# pl.savetxt('latlon_cont_TU.txt',latlon[lc1])

# for i in range(1,20):

# 	pl.savetxt('latlon_ilha_' + str(i) + '_TU.txt',eval('latlon[il' + str(i) + ']'))

