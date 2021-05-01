

import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

def calcula_media_var_std(dsar, zi):

    MEAN = np.zeros((len(dsar)-10, len(dsar)-10))
    VAR = np.copy(MEAN)

    for x in range(1,len(dsar)-10):
        for y in range(1,len(dsar)-10):
            print (x, y)

            MEAN[x,y] = 1/9*((zi[x-10,y-10])+
                        (zi[x,y-10])+
                        (zi[x+10,y-10])+
                        (zi[x-10,y])+
                        (zi[x,y])+
                        (zi[x+10,y])+
                        (zi[x-10,y+10])+
                        (zi[x,y+10])+
                        (zi[x+10,y+10]))

            VAR[x,y] = 1/9*((zi[x-10,y-10]-MEAN[x,y])**2+
                            (zi[x,y-10]-MEAN[x,y])**2+
                            (zi[x+10,y-10]-MEAN[x,y])**2+
                            (zi[x-10,y]-MEAN[x,y])**2+
                            (zi[x,y]-MEAN[x,y])**2+
                            (zi[x+10,y]-MEAN[x,y])**2+
                            (zi[x-10,y+10]-MEAN[x,y])**2+
                            (zi[x,y+10]-MEAN[x,y])**2+
                            (zi[x+10,y+10]-MEAN[x,y])**2)
    return MEAN, VAR

'C:\\Trabalho\\Diversos\\Python 3.7\\PSD/Teste4.wav'

dsar = pd.read_csv('s1a-20170130-5km.txt', skiprows=2, sep= '\s+')

SWH = dsar['SWH'].values

xi, yi = np.meshgrid(np.linspace(dsar.LON.min(),dsar.LON.max(),len(dsar)),
                     np.linspace(dsar.LAT.min(),dsar.LAT.max(),len(dsar)))

zi = griddata((dsar.LON, dsar.LAT), dsar.SWH, (xi, yi), method='linear')

MEAN, VAR = calcula_media_var_std(dsar, zi)


# retira pontos que estao no mar (melhorar..)
# zi[:,1100:] = np.nan

p = {}
p['MEAN'] = MEAN
p['VAR'] = VAR


#    STD = math.sqrt(VAR)

# plt.contourf(zi, cmap='jet')
# plt.colorbar()

# plt.contourf(xi, yi, zi)

plt.show()