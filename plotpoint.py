# ----------------------------------------------------------------------------------------
# Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  
# ----------------------------------------------------------------------------------------
# Pay attention to the pre-requisites and libraries
import os
from datetime import datetime
from windrose import WindroseAxes
from pylab import *
import pylab as plt
from matplotlib.ticker import FixedLocator
from matplotlib.dates import DateFormatter
import numpy as np
from datetime import datetime
f=open('anoplot.txt','r')
line=f.readline()
name=line[0:8];
file=open(name,'r')
tfile=file.readlines()
file.close()

nt=len(tfile)
ano=zeros(nt,'i2');mes=zeros(nt,'i2');dia=zeros(nt,'i2');hora=zeros(nt,'i2');minu=zeros(nt,'i2')
hs=zeros(nt,'f');tp=zeros(nt,'f');dp=zeros(nt,'f');
file=open(name,'r')
for i in range(0,nt):
    line=file.readline()
    ano[i]=int(line[0:4])
    mes[i]=int(line[5:7])
    dia[i]=int(line[8:10])
    hora[i]=int(line[11:13])
    minu[i]=int(line[14:16])
    hs[i]=float(line[18:24])
    tp[i]=float(line[25:32])
    dp[i]=(line[33:42])
    
file.close()
    
dates = np.array([plt.date2num(datetime(aa,mm,dd,hh,mi)) for aa,mm,dd,hh,mi in zip(ano,mes,dia,hora,minu)])    

#time series	
if nt >= 4000:
    fig = plt.figure(figsize=(15,12))
    ax = fig.add_subplot(311)
    ax.plot_date(dates,hs[:],'ro')
    #rc('xtick', labelsize=14) 
    #rc('ytick', labelsize=14) 
    title(' Wavewatch III - '+repr(ano[nt-1])+'',fontsize=16)
    ylabel("Altura Significativa (m)", fontsize=14)
    ylim(0,5)
    grid()
    
    ax = fig.add_subplot(312)
    ax.plot_date(dates,tp[:])
    ylabel("Periodo de pico (s)", fontsize=14)
    ylim(0,20)
    grid()
    
    ax = fig.add_subplot(313)
    ax.plot_date(dates,dp[:])
    ylabel("Direcao de Pico (graus)", fontsize=14)
    ylim(0,250)
    grid()
    
    savefig('sww3_'+repr(ano[nt-1])+'.png', dpi=None, facecolor='w', edgecolor='w',
    orientation='portrait', papertype=None, format='png',
    transparent=False, bbox_inches=None, pad_inches=0.1)
    plt.close()

#histogram
fig = plt.figure(figsize=(15,12))
ax = fig.add_subplot(311)
binshs=arange(0,5.5,0.5)
counts,bins,patches = ax.hist(hs[:],bins=binshs,facecolor='yellow',edgecolor='gray',label="Hs (m)")
ax.set_xticks(bins)
bin_centers=np.diff(bins) + bins[:-1] - 0.25
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -10), textcoords='offset points', va='top', ha='center')

title(' Wavewatch III - '+repr(ano[nt-1])+'',fontsize=16)
ax.legend(loc="upper right")
grid()

if nt >= 4000:
	ylim(0,4500)
else:
    ylim(0,1500)

ax = fig.add_subplot(312)
binstp=arange(0,22,2)
counts,bins,patches = ax.hist(tp[:],bins=binstp,facecolor='yellow',edgecolor='gray',label="Tp (s)")
ax.set_xticks(bins)
bin_centers=np.diff(bins) + bins[:-1]-1
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0),weight='bold', xycoords=('data', 'axes fraction'),
        xytext=(0, -10), textcoords='offset points', va='top', ha='center')
        
ax.legend(loc="upper right")
grid()
if nt >= 4000:
	ylim(0,4500)
else:
    ylim(0,1500)

ax = fig.add_subplot(313)
bins=arange(-22.5,360,45)
counts,bins,patches = ax.hist(dp[:],bins=bins,facecolor='yellow',edgecolor='gray',label="Dp (graus)")
ax.set_xticks(bins)
bin_centers=np.diff(bins) + bins[:-1] - 22.5
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -10), textcoords='offset points', va='top', ha='center')
        
ax.legend(loc="upper right")
if nt >= 4000:
	txlim=250
else:
    txlim=100
    
text(0, txlim,'N', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(45, txlim,'NE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(90, txlim,'E', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(135, txlim,'SE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(180, txlim,'S', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(225, txlim,'SW', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(270, txlim,'W', fontsize=14,color='red',weight='bold',ha='center', va='center')
grid()
if nt >= 4000:
	ylim(0,4500)
else:
    ylim(0,1500)

savefig('histww3_'+repr(ano[nt-1])+'.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=False, bbox_inches=None, pad_inches=0.1)
plt.close()

# windrose
def new_axes():
    fig = plt.figure(figsize=(10, 8), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(axespad=-0.10)
    plt.setp(l.get_texts(), fontsize=8)
    
  
if nt <= 4000:
    #windrose like a stacked histogram with normed (displayed in percent) results
    ax = new_axes()
    ax.bar(dp, hs, normed=True, bins=binshs, opening=0.8, edgecolor='white',nsector=8)
    set_legend(ax)
    savefig('hsdp_'+repr(ano[nt-1])+'.png', dpi=None, facecolor='w', edgecolor='w',
    orientation='portrait', papertype=None, format='png',
    transparent=False, bbox_inches=None, pad_inches=0.1)    
    ax = new_axes()
    ax.bar(dp, tp, normed=True, bins=binstp, opening=0.8, edgecolor='white',nsector=8)
    set_legend(ax)
    savefig('tpdp_'+repr(ano[nt-1])+'.png', dpi=None, facecolor='w', edgecolor='w',
    orientation='portrait', papertype=None, format='png',
    transparent=False, bbox_inches=None, pad_inches=0.1)
    plt.close()