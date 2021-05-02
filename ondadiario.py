'''
Programa para plotar o mapa da isa
eixo x - horas
eixo y - dias
'''

import numpy as np
from matplotlib import pyplot as plt

dd =np.loadtxt('/home/lioc/Dropbox/ww3vale/Trocas/Mapa_onda_diario/onda_julho2013_ADCP1.txt')

ndias = 31

u = np.cos(dd[:,3])
v = np.sin(dd[:,3])

ddr = np.reshape(dd[:,3],(ndias,24))

plt.figure()
plt.pcolor(ddr)
plt.quiver(np.arange(24)+.5,np.arange(ndias)+.5,u,v)

plt.show()



