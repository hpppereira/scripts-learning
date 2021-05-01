# ----------------------------------------------------------------------------------------
# Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  
# MotorDePopa Wave Research Group
# Rio de Janeiro - Brazil
# ----------------------------------------------------------------------------------------
# Pay attention to the pre-requisites and libraries
import os
from datetime import datetime
import pylab as plt
import numpy as np
from pylab import *
from datetime import datetime
import pylab as pl

plt.close('all')


##########################################################################
#carrega os hindcasts

pathname = os.environ['HOME'] + '/Dropbox/ww3salvador/Modelagem/hindcast/'

# 0    1    2    3     4   5   6   7     8
#ano, mes, dia, hora, min, hs, tp, dp, spread
hind1 = np.loadtxt(pathname + 'hindcast.txt') #,usecols=(5,6,7)) 
hind2 = np.loadtxt(pathname + 'hindcast2.txt') #,usecols=(5,6,7)) 

hind = np.concatenate((hind1,hind2),axis=0)
hindp = hind[:,[5,6,7]] #hs, tp e dp
hs, tp, dp = hindp.T


##########################################################################
#separa as estacoes de verao e inverno
# Primavera: 1 setembro ate 30 novembro
# Verao: 1 dezembro ate 28 fevereiro
# Outono: 1 marco ate 31 maio
# Inverno: 1 junho ate 31 agosto

#data total em datetime
datat = [ datetime(int(hind[i,0]),int(hind[i,1]),int(hind[i,2]),int(hind[i,3])) for i in range(len(hind))]

prim = np.where((hind[:,1] == 9) | (hind[:,1] == 10) | (hind[:,1] == 11))[0]



##########################################################################


#histogram

fig = plt.figure(figsize=(12,13))
ax = fig.add_subplot(311)
binshs=np.arange(0,5.5,0.5)
counts,bins,patches = ax.hist(hs,bins=binshs,facecolor='gray',edgecolor='black',hatch="/",label="Hs (m)")
ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,80,10): lima.append((i*len(hs)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(hs)) ) * 100, 0)) + ' %'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 0.25
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)

ax.legend(loc="upper right")
grid()
#text(0.3, 145000,'A', fontsize=16,color='black',weight='bold',ha='center', va='center')


ax = fig.add_subplot(312)
binstp=np.arange(0,22,2)
counts,bins,patches = ax.hist(tp,bins=binstp,facecolor='gray',edgecolor='black',hatch="/",label="Tp (s)")
ax.set_xticks(bins)


#setar eixo y com porcentagem
lima=[]
for i in range(0,80,10): lima.append((i*len(tp)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(tp)) ) * 100.0, 0)) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1]-1
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0),weight='bold', xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)
        
ax.legend(loc="upper right")
#text(1, 60000,'C', fontsize=16,color='black',weight='bold',ha='center', va='center')

grid()

ax = fig.add_subplot(313)
bins=arange(-22.5,360,45)
counts,bins,patches = ax.hist(dp,bins=bins,facecolor='gray',edgecolor='black',hatch="/",label="Dp (graus)")

ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,80,10): lima.append((i*len(dp)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(dp)) ) * 100.0, 0)) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 22.5
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)
        
ax.legend(loc="upper right")
    
text(0, 8000,'N', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(45, 8000,'NE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(90, 8000,'E', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(135, 8000,'SE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(180, 8000,'S', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(225, 8000,'SW', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(270, 8000,'W', fontsize=14,color='red',weight='bold',ha='center', va='center')
grid()
#text(-30, 60000,'E', fontsize=16,color='black',weight='bold',ha='center', va='center')


savefig('histww3.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=False, bbox_inches=None, pad_inches=0.1)

savefig('histww3.eps', dpi=1200, facecolor='w', edgecolor='w',
orientation='portrait',format='eps')

plt.show()


print 'BC10','Hs','Tp','Dp'
print "Media",np.mean(hs),np.mean(tp),np.mean(dp)
print "Desvio",np.std(hs),np.std(tp),np.std(dp)
print "90perc",np.percentile(hs,90),np.percentile(tp,90),np.percentile(dp,90)
print "99perc",np.percentile(hs,99),np.percentile(tp,99),np.percentile(dp,99)
print "maximo",np.max(hs),np.max(tp),np.max(dp)
