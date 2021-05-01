# -*- coding: utf-8 -*-
'''
Compara os dados da triaxys processado pelo lioc e 
resultado do ww3

Ultima modificacao: 09/05/2015

#Saida do Python
#         0   1   2   3    4     5    6   7   8     9       10       11   12   13   14    15   16   17    18   19
#header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')

#Saida WW3
# 0   1   2    3   4   5   6  7   8
#ano,mes,dia,hora,min,hs,tp,dp,spread
'''

import numpy as np
from matplotlib import pylab as pl
import matplotlib as mpl
from matplotlib import pyplot as plt
from datetime import datetime
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import os
import matplotlib.dates as mdates

plt.close('all')

local = 'Santos/SP'
local1 = 'santos'
latlon = '-25.28334 / -44.93334'
idargos = '69151'
idwmo = '31051'
glstr = '8'
dmag = -23

#triaxys_8_santos_jul13

#Saida do lioc
#         0   1   2   3    4     5    6   7   8     9       10       11   12   13   14    15   16   17    18   19
#header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')
py = np.loadtxt(os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/hindcast/Santos/' + 'triaxys_' + glstr + '_' + local1 + '.out',delimiter=',',skiprows = 0)

# carrega resultado do WW3
pathname_mod = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/hindcast/Santos/resultados/'
direm = np.sort(os.listdir(pathname_mod))

#Saida WW3
# 0   1   2    3   4   5  6  7   8
#ano,mes,dia,hora,min,hs,tp,dp,spread

# ddm = Data, hora, Hs, Fp, Dp -- calcula o Tp mais abaixo
ddm = np.array([[0,0,0,0,0,0,0,0,0]])

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in direm:

    #pula a primeira linha pois ja eh a mesma do ultima arquivo
	dadosm = np.loadtxt(pathname_mod + dto + '/santos.txt')
	ddm = np.concatenate((ddm,dadosm),axis=0)

ddm = ddm[1:,:]

datam_py = []
for i in range(len(py)):
	datam_py.append(datetime(int(str(py[i,0])[0:4]),int(str(py[i,0])[4:6]),int(str(py[i,0])[6:8]),int(str(py[i,0])[8:10])))

datam_ww3 = []
for i in range(len(ddm)):
	datam_ww3.append(datetime(int(ddm[i,0]), int(ddm[i,1]), int(ddm[i,2]), int(ddm[i,3]) ))


#figuras
fig = pl.figure()
ax = fig.add_subplot(311)
ax.plot(datam_py,py[:,6],'r',datam_ww3,ddm[:,5],'b')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
ax.set_ylabel('Hs (m)',fontsize=12), ax.grid()
ax.legend(['PNBOIA','WW3'],loc=0,ncol=4)
ax.set_ylim(0,8)
ax.set_xlim(datam_ww3[0],datam_ww3[-1])


ax2 = fig.add_subplot(312)
ax2.plot(datam_py,py[:,7],'r.',datam_ww3,ddm[:,6],'b.')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
ax2.set_ylabel('Tp (s)',fontsize=12), pl.grid()
ax2.set_ylim(0,22)
ax2.set_xlim(datam_ww3[0],datam_ww3[-1])

ax3 = fig.add_subplot(313)
ax3.plot(datam_py,py[:,8]+dmag,'r.',datam_ww3,ddm[:,7],'b.')
ax3.set_ylabel('Dp (graus)',fontsize=12), pl.grid()
ax3.set_ylim(0,360)
ax3.set_xlim(datam_ww3[0],datam_ww3[-1])

pl.show()

# plt.figure()
# plt.subplot(311)
# plt.plot(datam_py,py[:,6],'b')
# plt.plot(datam_ww3,ddm[:,5],'r')
# plt.ylabel('Hs (m)'), pl.grid()
# plt.xlim(datam_ww3[0],datam_ww3[-1])

# plt.subplot(312)
# plt.plot(datam_py,py[:,7],'b.')
# plt.plot(datam_ww3,ddm[:,6],'r.')
# plt.ylabel('Tp (s)'), pl.grid()
# plt.xlim(datam_ww3[0],datam_ww3[-1])

# plt.subplot(313)
# plt.plot(datam_py,py[:,8]+dmag,'b.')
# plt.plot(datam_ww3,ddm[:,7],'r.')
# plt.ylabel('Dp (graus)'), pl.grid()
# plt.xlim(datam_ww3[0],datam_ww3[-1])

# plt.show()