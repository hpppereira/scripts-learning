# ----------------------------------------------------------------------------------------
# Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  
# ----------------------------------------------------------------------------------------
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
from windrose import WindroseAxes

plt.close('all')

#diretorio de onde estao os dados processados
pathname  = '/home/lioc/Dropbox/ww3vale/Geral/TU/rot/out/proc/parametros/'

#   0    1    2     3     4      5       6      7   8
# data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02'
ddv1 = np.loadtxt(pathname + 'vale_adcp1.out',delimiter=',')
ddv2 = np.loadtxt(pathname + 'vale_adcp2.out',delimiter=',')
ddv3 = np.loadtxt(pathname + 'vale_adcp3.out',delimiter=',')
ddv4 = np.loadtxt(pathname + 'vale_adcp4.out',delimiter=',')

#data com datetime
datav1 = np.array([ datetime.strptime(str(int(ddv1[i,0])), '%Y%m%d%H%M') for i in range(len(ddv1)) ])
datav2 = np.array([ datetime.strptime(str(int(ddv2[i,0])), '%Y%m%d%H%M') for i in range(len(ddv2)) ])
datav3 = np.array([ datetime.strptime(str(int(ddv3[i,0])), '%Y%m%d%H%M') for i in range(len(ddv3)) ])
datav4 = np.array([ datetime.strptime(str(int(ddv4[i,0])), '%Y%m%d%H%M') for i in range(len(ddv4)) ])

#figuras
pl.figure(figsize=(15,12))
pl.subplot(311)
pl.plot(datav1,ddv1[:,1],'b',datav2,ddv2[:,1],'k',datav3,ddv3[:,1],'r',datav4,ddv4[:,1],'g')
pl.legend(['ADCP-1','ADCP-2','ADCP-3','ADCP-4'],fontsize=10), pl.grid('on')
pl.axis('tight'), pl.title('Hm0'), pl.grid('on'), pl.xticks(visible=False)
pl.ylabel('metros')
pl.subplot(312)
pl.plot(datav1,ddv1[:,7],'.b',datav2,ddv2[:,7],'.k',datav3,ddv3[:,7],'.r',datav4,ddv4[:,7],'.g')
pl.axis('tight'), pl.title('Tp'), pl.grid('on'), pl.xticks(visible=False)
pl.ylabel('segundos')
pl.subplot(313)
pl.plot(datav1,ddv1[:,4],'.b',datav2,ddv2[:,4],'.k',datav3,ddv3[:,4],'.r',datav4,ddv4[:,4],'.g')
pl.axis('tight'), pl.title('DirTp'), pl.grid('on')
pl.ylabel('graus')
pl.ylim((0,360))
pl.xticks(rotation=10)


###########################################################################################
# windrose

### ADCP 01 ###
def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=10,weight='bold')
    
#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
binshs=arange(0,5.5,0.5)
ax.bar(ddv1[:,4], ddv1[:,1], normed=True, bins=binshs, opening=0.8, edgecolor='white',nsector=8)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig('fig/adcp1_201304_hsdp.png', dpi=None, edgecolor=None,
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.1)    
plt.close()

ax = new_axes()
binstp=arange(0,22,2)
ax.bar(ddv1[:,4], ddv1[:,7], normed=True, bins=binstp, opening=0.8, edgecolor='white',nsector=8)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig('fig/adcp1_201304_tpdp.png', dpi=None, edgecolor=None,
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.1)
plt.close()


### ADCP 02 ###
def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=10,weight='bold')
    
#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
binshs=arange(0,5.5,0.5)
ax.bar(ddv2[:,4], ddv2[:,1], normed=True, bins=binshs, opening=0.8, edgecolor='white',nsector=8)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig('fig/adcp2_201304_hsdp.png', dpi=None, edgecolor=None,
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.1)    
plt.close()

ax = new_axes()
binstp=arange(0,22,2)
ax.bar(ddv2[:,4], ddv2[:,7], normed=True, bins=binstp, opening=0.8, edgecolor='white',nsector=8)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig('fig/adcp2_201304_tpdp.png', dpi=None, edgecolor=None,
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.1)
plt.close()


### ADCP 03 ###
def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=10,weight='bold')
    
#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
binshs=arange(0,5.5,0.5)
ax.bar(ddv3[:,4], ddv3[:,1], normed=True, bins=binshs, opening=0.8, edgecolor='white',nsector=8)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig('fig/adcp3_201304_hsdp.png', dpi=None, edgecolor=None,
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.1)    
plt.close()

ax = new_axes()
binstp=arange(0,22,2)
ax.bar(ddv3[:,4], ddv3[:,7], normed=True, bins=binstp, opening=0.8, edgecolor='white',nsector=8)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig('fig/adcp3_201304_tpdp.png', dpi=None, edgecolor=None,
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.1)
plt.close()



### ADCP 04 ###
def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(loc="center right",borderaxespad=-10.8)
    # l.get_frame().set_fill(False) #transparent legend
    plt.setp(l.get_texts(), fontsize=10,weight='bold')
    
#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
binshs=arange(0,5.5,0.5)
ax.bar(ddv4[:,4], ddv4[:,1], normed=True, bins=binshs, opening=0.8, edgecolor='white',nsector=8)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig('fig/adcp4_201304_hsdp.png', dpi=None, edgecolor=None,
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.1)    
plt.close()

ax = new_axes()
binstp=arange(0,22,2)
ax.bar(ddv4[:,4], ddv4[:,7], normed=True, bins=binstp, opening=0.8, edgecolor='white',nsector=8)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig('fig/adcp4_201304_tpdp.png', dpi=None, edgecolor=None,
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.1)
plt.close()

###########################################################################################


plt.show()