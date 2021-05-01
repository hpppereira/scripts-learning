'''
Evento de
26/Agosto/2011

'''

import os
import pandas as pd
import matplotlib.pyplot as plt

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/proc/'

#carrega dados do modelo
fln = pd.read_csv(pathname + 'FLN_8.csv', parse_dates=['date'], index_col='date')


fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1.plot(fln.index,fln.hm0)

fig.show()