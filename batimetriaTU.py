'''
Processamento dos dados de batimetria
do Porto de Tubarao
'''

import pandas as pd
import os
import matplotlib.pylab as pl
import numpy as np
import matplotlib as mpl


pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/batimetria/pi/BATIMETRIA_PORTO_TU/Todas_areas/'

dd = pd.read_table(pathname + 'XYZ.xyz')

print 'Iniciando o meshgrid...'
[lons,lats] = np.meshgrid(dd.X[0:-1:100],dd.Y[0:-1:100],sparse=False,copy=False)

print 'Iniciando o griddata de Z...'
Zs = mpl.mlab.griddata(dd.X,dd.Y,dd.Z,lons,lats,interp='linear');

pl.figure()
pl.pcolormesh(lons,lats,Zs,shading='flat',cmap=pl.cm.jet,vmin=np.nanmin(Zs),vmax=np.nanmax(Zs))



#pl.figure()
#pl.plot(dd.X,dd.Y,'.')

pl.show()