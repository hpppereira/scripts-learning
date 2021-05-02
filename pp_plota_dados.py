'''
Processamento dos dados de ADCP de Cacimbas-ES e boia BC10
Projeto: WW3ES
LIOc-COPPE/UFRJ

Faz histogramas e estatistica dos dados

'''

from numpy import * 
from datetime import datetime
import os
from pylab import *
from windrose import WindroseAxes

# escolha o dado: cacimbas ou bc10 ou ww3
namefile='Merenda'
namedir='Merenda'

pathname= os.environ['HOME'] + '/Dropbox/ww3es/Geral/rot/saida/' + namedir
home=os.environ['HOME']

data=np.loadtxt(pathname+ '/param_8_'+namefile+'.out',delimiter=',') # data,hs,tp,dp,h10,tm,dm

#histogram
fig = plt.figure(figsize=(15,12))
ax = fig.add_subplot(311)
binshs=arange(0,5.5,0.5)
counts,bins,patches = ax.hist(data[:,1],bins=binshs,facecolor='yellow',edgecolor='gray',label="Hs (m)")
ax.set_xticks(bins)
bin_centers=np.diff(bins) + bins[:-1] - 0.25
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -10), textcoords='offset points', va='top', ha='center')

title('Dados Espirito Santo - '+namefile,fontsize=16)
ax.legend(loc="upper right")
grid()

ax = fig.add_subplot(312)
binstp=arange(0,22,2)
counts,bins,patches = ax.hist(data[:,2],bins=binstp,facecolor='yellow',edgecolor='gray',label="Tp (s)")
ax.set_xticks(bins)
bin_centers=np.diff(bins) + bins[:-1]-1
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0),weight='bold', xycoords=('data', 'axes fraction'),
        xytext=(0, -10), textcoords='offset points', va='top', ha='center')
        
ax.legend(loc="upper right")
grid()

ax = fig.add_subplot(313)
bins=arange(-22.5,360,45)
counts,bins,patches = ax.hist(data[:,3],bins=bins,facecolor='yellow',edgecolor='gray',label="Dp (graus)")
ax.set_xticks(bins)
bin_centers=np.diff(bins) + bins[:-1] - 22.5
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -10), textcoords='offset points', va='top', ha='center')
        
ax.legend(loc="upper right")
txlim=200
    
text(0, txlim,'N', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(45, txlim,'NE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(90, txlim,'E', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(135, txlim,'SE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(180, txlim,'S', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(225, txlim,'SW', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(270, txlim,'W', fontsize=14,color='red',weight='bold',ha='center', va='center')
grid()

savefig(home + '/Dropbox/ww3es/Geral/fig/dados/' + 'hist'+namefile+'.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=False, bbox_inches=None, pad_inches=0.1)


# windrose
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
ax.bar(data[:,3], data[:,1], normed=True, bins=binshs, opening=0.8, edgecolor='white',nsector=8)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig(home + '/Dropbox/ww3es/Geral/fig/dados/' + 'hsdp'+namefile+'.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=False, bbox_inches=None, pad_inches=0.1)    
plt.close()

ax = new_axes()
ax.bar(data[:,3], data[:,2], normed=True, bins=binstp, opening=0.8, edgecolor='white',nsector=8)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig(home + '/Dropbox/ww3es/Geral/fig/dados/' + 'tpdp'+namefile+'.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=False, bbox_inches=None, pad_inches=0.1)
plt.close()