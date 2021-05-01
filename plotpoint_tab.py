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

# BC10
file=open('test.txt','r')
tfile=file.readlines()
file.close()

nt=len(tfile)
ano_bc10=np.zeros(nt,'i2');mes_bc10=np.zeros(nt,'i2');dia_bc10=np.zeros(nt,'i2');
hs_bc10=np.zeros(nt,'f');tp_bc10=np.zeros(nt,'f');dp_bc10=np.zeros(nt,'f');
file=open('test.txt','r')
for i in range(0,nt):
    line=file.readline()
    ano_bc10[i]=int(line[0:4])
    mes_bc10[i]=int(line[5:7])
    dia_bc10[i]=int(line[8:10])
    hs_bc10[i]=float(line[18:24])
    tp_bc10[i]=float(line[25:32])
    dp_bc10[i]=(line[33:42])
    
file.close()

   
# dates = np.array([plt.date2num(datetime(aa,mm,dd,hh,mi)) for aa,mm,dd,hh,mi in zip(ano,mes,dia,hora,minu)])    

#histogram

fig = plt.figure(figsize=(16,12))
ax = fig.add_subplot(311)
binshs=np.arange(0,5.5,0.5)
counts,bins,patches = ax.hist(hs_bc10[:],bins=binshs,facecolor='gray',edgecolor='black',hatch="/",label="Hs (m)")
ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,60,10): lima.append((i*len(hs_bc10)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(hs_bc10)) ) * 100, 0)) + ' %'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 0.25
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)

ax.legend(loc="upper right")
grid()

ax = fig.add_subplot(312)
binstp=np.arange(0,22,2)
counts,bins,patches = ax.hist(tp_bc10[:],bins=binstp,facecolor='gray',edgecolor='black',hatch="/",label="Tp (s)")
ax.set_xticks(bins)
#setar eixo y com porcentagem
lima=[]
for i in range(0,60,10): lima.append((i*len(tp_bc10)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(tp_bc10)) ) * 100.0, 0)) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1]-1
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0),weight='bold', xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)
        
ax.legend(loc="upper right")


grid()


ax = fig.add_subplot(313)
bins=arange(-22.5,360,45)
counts,bins,patches = ax.hist(dp_bc10[:],bins=bins,facecolor='gray',edgecolor='black',hatch="/",label="Dp (graus)")

ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,60,10): lima.append((i*len(dp_bc10)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(dp_bc10)) ) * 100.0, 0)) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 22.5
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)
        
ax.legend(loc="upper right")
    
text(0, 2000,'N', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(45, 2000,'NE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(90, 2000,'E', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(135, 2000,'SE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(180, 2000,'S', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(225, 2000,'SW', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(270, 2000,'W', fontsize=14,color='red',weight='bold',ha='center', va='center')
grid()

savefig('histww3.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=False, bbox_inches=None, pad_inches=0.1)

savefig('histww3.eps', dpi=1200, facecolor='w', edgecolor='w',
orientation='portrait',format='eps')

plt.close()

print 'BC10','Hs','Tp','Dp'
print "Media",np.mean(hs_bc10),np.mean(tp_bc10),np.mean(dp_bc10)
print "Desvio",np.std(hs_bc10),np.std(tp_bc10),np.std(dp_bc10)
print "90perc",np.percentile(hs_bc10,90),np.percentile(tp_bc10,90),np.percentile(dp_bc10,90)
print "maximo",np.max(hs_bc10),np.max(tp_bc10),np.max(dp_bc10)
print " "

