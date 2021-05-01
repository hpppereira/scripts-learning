'''
# ----------------------------------------------------------------------------------------
# Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  
processamento dos dados retirados da planilha em excel
os arquivos adcp1_vale.out foram gerados com a rotina pp_awac_concat

# ----------------------------------------------------------------------------------------
'''


# Pay attention to the pre-requisites and libraries
import os
from datetime import datetime
from windrose import WindroseAxes
from pylab import *
import pylab as plt
import pylab as pl
from matplotlib.ticker import FixedLocator
from matplotlib.dates import DateFormatter
import numpy as np
from datetime import datetime

#carrega dados processados dos 4 adcp

#escolha o numero do adcp (1 a 4)
numadcp = 2
figsize1=(15,12)

#diretorio de onde estao os dados processados
pathname  = os.environ['HOME'] + '/Dropbox/ww3vale_old/Geral/TU/rot/saida/proc/'

#   0    1    2     3     4      5       6      7   8
# data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02'
dd1 = np.loadtxt(pathname + 'adcp1_vale.out',delimiter=',')
dd2 = np.loadtxt(pathname + 'adcp2_vale.out',delimiter=',')
dd3 = np.loadtxt(pathname + 'adcp3_vale.out',delimiter=',')
dd4 = np.loadtxt(pathname + 'adcp4_vale.out',delimiter=',')

#data com datetime
datat1 = [datetime(int(str(dd1[i,0])[0:4]),int(str(dd1[i,0])[4:6]),int(str(dd1[i,0])[6:8]),
    int(str(dd1[i,0])[8:10]),int(str(dd1[i,0])[10:12])) for i in range(len(dd1))]

datat2 = [datetime(int(str(dd2[i,0])[0:4]),int(str(dd2[i,0])[4:6]),int(str(dd2[i,0])[6:8]),
    int(str(dd2[i,0])[8:10]),int(str(dd2[i,0])[10:12])) for i in range(len(dd2))]

datat3 = [datetime(int(str(dd3[i,0])[0:4]),int(str(dd3[i,0])[4:6]),int(str(dd3[i,0])[6:8]),
    int(str(dd3[i,0])[8:10]),int(str(dd3[i,0])[10:12])) for i in range(len(dd3))]

datat4 = [datetime(int(str(dd4[i,0])[0:4]),int(str(dd4[i,0])[4:6]),int(str(dd4[i,0])[6:8]),
    int(str(dd4[i,0])[8:10]),int(str(dd4[i,0])[10:12])) for i in range(len(dd4))]


dd = eval('dd' + str(numadcp))

dates = dd[:,0] #data em numero, ex: 201301200005 (AAAAMMDDHHMM)
hs = dd[:,1]
tp = dd[:,7]
dp = dd[:,4]

#cria data com datetime
datat = [datetime(int(str(dd[i,0])[0:4]),int(str(dd[i,0])[4:6]),int(str(dd[i,0])[6:8]),
    int(str(dd[i,0])[8:10])) for i in range(len(dd))]

#numero de pontos da serie
nt = len(hs)
ano = dates

#time series	
# if nt >= 4000:

fig = plt.figure(figsize=figsize1)
ax = fig.add_subplot(311)
ax.plot_date(datat,hs[:],'ro')
# #rc('xtick', labelsize=14) 
# #rc('ytick', labelsize=14)
# title(' Wavewatch III - '+repr(ano[nt-1])+'',fontsize=16)
# ylabel("Altura Significativa (m)", fontsize=14)
# ylim(0,3)
# grid()

# ax = fig.add_subplot(312)
# ax.plot_date(datat,tp[:])
# ylabel("Periodo de pico (s)", fontsize=14)
# ylim(0,20)
# grid()

# ax = fig.add_subplot(313)
# ax.plot_date(datat,dp[:])
# ylabel("Direcao de Pico (graus)", fontsize=14)
# ylim(0,360)
# grid()

# savefig('sww3_'+repr(ano[nt-1])+'.png', dpi=None, facecolor='w', edgecolor='w',
# orientation='portrait', papertype=None, format='png',
# transparent=False, bbox_inches=None, pad_inches=0.1)
# plt.close()


#plota todos os adcp
pl.figure(figsize=figsize1)
pl.subplot(311)
pl.plot(datat1,dd1[:,1],'b',datat2,dd2[:,1],'k',datat3,dd3[:,1],'r',datat4,dd4[:,1],'g')
pl.legend(['ADCP-1','ADCP-2','ADCP-3','ADCP-4'],fontsize=10), pl.grid('on')
pl.axis('tight'), pl.title('Hm0'), pl.grid('on'), pl.xticks(visible=False)
pl.ylabel('metros')
pl.subplot(312)
pl.plot(datat1,dd1[:,7],'.b',datat2,dd2[:,7],'.k',datat3,dd3[:,7],'.r',datat4,dd4[:,7],'.g')
pl.axis('tight'), pl.title('Tp'), pl.grid('on'), pl.xticks(visible=False)
pl.ylabel('segundos')
pl.subplot(313)
pl.plot(datat1,dd1[:,4],'.b',datat2,dd2[:,4],'.k',datat3,dd3[:,4],'.r',datat4,dd4[:,4],'.g')
pl.axis('tight'), pl.title('DirTp'), pl.grid('on')
pl.ylabel('graus')
pl.ylim((0,360))
pl.xticks(rotation=10)



# #histogram
# fig = plt.figure(figsize=(15,12))
# ax = fig.add_subplot(311)
# binshs=arange(0,5.5,0.5)
# counts,bins,patches = ax.hist(hs[:],bins=binshs,facecolor='yellow',edgecolor='gray',label="Hs (m)")
# ax.set_xticks(bins)
# bin_centers=np.diff(bins) + bins[:-1] - 0.25
# for count, x in zip(counts,bin_centers):
#     percent = '%0.1f%%' % (100 * float(count) / counts.sum())
#     ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
#         xytext=(0, -10), textcoords='offset points', va='top', ha='center')

# title(' Wavewatch III - ',fontsize=16)
# ax.legend(loc="upper right")
# grid()

# if nt >= 4000:
# 	ylim(0,4500)
# else:
#     ylim(0,1500)

# ax = fig.add_subplot(312)
# binstp=arange(0,22,2)
# counts,bins,patches = ax.hist(tp[:],bins=binstp,facecolor='yellow',edgecolor='gray',label="Tp (s)")
# ax.set_xticks(bins)
# bin_centers=np.diff(bins) + bins[:-1]-1
# for count, x in zip(counts,bin_centers):
#     percent = '%0.1f%%' % (100 * float(count) / counts.sum())
#     ax.annotate(percent, xy=(x, 0),weight='bold', xycoords=('data', 'axes fraction'),
#         xytext=(0, -10), textcoords='offset points', va='top', ha='center')
        
# ax.legend(loc="upper right")
# grid()

# if nt >= 4000:
# 	ylim(0,4500)
# else:
#     ylim(0,1500)

# ax = fig.add_subplot(313)
# bins=arange(-22.5,360,45)
# counts,bins,patches = ax.hist(dp[:],bins=bins,facecolor='yellow',edgecolor='gray',label="Dp (graus)")
# ax.set_xticks(bins)
# bin_centers=np.diff(bins) + bins[:-1] - 22.5
# for count, x in zip(counts,bin_centers):
#     percent = '%0.1f%%' % (100 * float(count) / counts.sum())
#     ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
#         xytext=(0, -10), textcoords='offset points', va='top', ha='center')
        
# ax.legend(loc="upper right")
# if nt >= 4000:
# 	txlim=250
# else:
#     txlim=100
    
# text(0, txlim,'N', fontsize=14,color='red',weight='bold',ha='center', va='center')
# text(45, txlim,'NE', fontsize=14,color='red',weight='bold',ha='center', va='center')
# text(90, txlim,'E', fontsize=14,color='red',weight='bold',ha='center', va='center')
# text(135, txlim,'SE', fontsize=14,color='red',weight='bold',ha='center', va='center')
# text(180, txlim,'S', fontsize=14,color='red',weight='bold',ha='center', va='center')
# text(225, txlim,'SW', fontsize=14,color='red',weight='bold',ha='center', va='center')
# text(270, txlim,'W', fontsize=14,color='red',weight='bold',ha='center', va='center')
# grid()
# if nt >= 4000:
# 	ylim(0,4500)
# else:
#     ylim(0,1500)

# savefig('histww3_'+repr(ano[nt-1])+'.png', dpi=None, facecolor='w', edgecolor='w',
# orientation='portrait', papertype=None, format='png',
# transparent=False, bbox_inches=None, pad_inches=0.1)
# plt.close()

# # windrose
# def new_axes():
#     fig = plt.figure(figsize=(10, 8), dpi=80, facecolor='w', edgecolor='w')
#     rect = [0.1, 0.1, 0.8, 0.8]
#     ax = WindroseAxes(fig, rect, axisbg='w')
#     fig.add_axes(ax)
#     return ax

# def set_legend(ax):
#     l = ax.legend()
#     plt.setp(l.get_texts(), fontsize=8)
    
  
# # if nt <= 4000:
# #windrose like a stacked histogram with normed (displayed in percent) results
# ax = new_axes()
# ax.bar(dp, hs, normed=True, bins=binshs, opening=0.8, edgecolor='white',nsector=8)
# set_legend(ax)
# # savefig('hsdp_'+repr(ano[nt-1])+'.png', dpi=None, facecolor='w', edgecolor='w',
# # orientation='portrait', papertype=None, format='png',
# # transparent=False, bbox_inches=None, pad_inches=0.1)    

# ax = new_axes()
# ax.bar(dp, tp, normed=True, bins=binstp, opening=0.8, edgecolor='white',nsector=8)
# set_legend(ax)

# # savefig('tpdp_'+repr(ano[nt-1])+'.png', dpi=None, facecolor='w', edgecolor='w',
# # orientation='portrait', papertype=None, format='png',
# # transparent=False, bbox_inches=None, pad_inches=0.1)
# plt.close()

plt.show()