'''
Junta arquivos da reconstituicao VALE de 2011/02 a 2015/07
plota histogramas e rosa das ondas

LIOc - Laboratorio de Instrumentacao Oceanografica

Data da ultima modificacao: 17/08/2015
'''

import numpy as np
from datetime import datetime
import pylab as plt
from pylab import *
import os
import windrose
reload(windrose)
from windrose import WindroseAxes


#diretorio de onde estao os resultados do ADCP01
pathname = os.environ['HOME'] + '/Dropbox/ww3vale_info/TU/hindcast/output/VIX/'
#pathname  = '/media/lioc/lioc6/hindcastVale/VIX_60X45/'
#pathname  = '/media/lioc/Parente/SWAN/VIX_60X45/output/'

direm = np.sort(os.listdir(pathname))

#diretorio de onde estao os resultados do ADCP02 3 4
#pathname2  = '/media/lioc/lioc6/hindcastVale/BES_65X45/'
pathname2 = os.environ['HOME'] + '/Dropbox/ww3vale_info/TU/hindcast/output/BES/'
#pathname2  = '/media/lioc/Parente/SWAN/BES_65X45/output/'
direm2 = np.sort(os.listdir(pathname2))

md1=np.array([[0,0,0,0]])
madcp01=np.array([[0,0,0,0]])

md2=np.array([[0,0,0,0]])
madcp02=np.array([[0,0,0,0]])

md3=np.array([[0,0,0,0]])
madcp03=np.array([[0,0,0,0]])

md4=np.array([[0,0,0,0]])
madcp04=np.array([[0,0,0,0]])


#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in direm:

	madcp01= np.loadtxt(pathname + dto + '/table_point_ADCP01.out',skiprows=7,usecols=(0,1,3,2))
	md1=np.concatenate((md1,madcp01[:,:]),axis=0)

for dto in direm2:

	madcp02= np.loadtxt(pathname2 + dto + '/table_point_ADCP02.out',skiprows=7,usecols=(0,1,3,2))
	md2=np.concatenate((md2,madcp02[:,:]),axis=0)

	madcp03= np.loadtxt(pathname2 + dto + '/table_point_ADCP03.out',skiprows=7,usecols=(0,1,3,2))
	md3=np.concatenate((md3,madcp03[:,:]),axis=0)

	madcp04= np.loadtxt(pathname2 + dto + '/table_point_ADCP04.out',skiprows=7,usecols=(0,1,3,2))
	md4=np.concatenate((md4,madcp04[:,:]),axis=0)



md1 = md1[1:,:] #adcp01
md2 = md2[1:,:] #adcp02
md3 = md3[1:,:] #adcp03
md4 = md4[1:,:] #adcp04


# =================================================
#ecolha o ponto : ADCP01; ADCP02; ADCP03; ADCP04
name = 'ADCP04'
dado=md4; #dado por adcp md1; md2; md3; md4
# ==================================================

#salva arquivo todo
savetxt('out/hindcast/'+name+'hindcast.out',dado,fmt='%.2f')

# ===============================================================================
# ================= histogram  ==================================================

aux=rand(1,dado.shape[0])*10-5
dire=aux+dado[:,3]


fig = plt.figure(figsize=(16,12))
ax = fig.add_subplot(311)
binshs=np.arange(0,4,0.5)
counts,bins,patches = ax.hist(dado[:,1],bins=binshs,facecolor='gray',edgecolor='black',hatch="/",label="Hs (m)")
ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,100,10): lima.append((i*len(dado[:,1])/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(dado[:,1])) ) * 100, 0)) + ' %'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 0.25
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)

ax.legend(loc="upper right")
grid()
#text(0.3, 18000,'A', fontsize=16,color='black',weight='bold',ha='center', va='center')

ax = fig.add_subplot(312)
binstp=np.arange(0,22,2)
counts,bins,patches = ax.hist(dado[:,2],bins=binstp,facecolor='gray',edgecolor='black',hatch="/",label="Tp (s)")
ax.set_xticks(bins)
#setar eixo y com porcentagem
lima=[]
for i in range(0,100,10): lima.append((i*len(dado[:,2])/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(dado[:,2])) ) * 100.0, 0)) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1]-1
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0),weight='bold', xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)
        
ax.legend(loc="upper right")
#text(1, 18000,'C', fontsize=16,color='black',weight='bold',ha='center', va='center')

grid()

ax = fig.add_subplot(313)
bins=arange(-22.5,360,45)
counts,bins,patches = ax.hist(dado[:,3],bins=bins,facecolor='gray',edgecolor='black',hatch="/",label="Dp (graus)")

ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,100,10): lima.append((i*len(dado[:,3])/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(dado[:,3])) ) * 100.0, 0)) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 22.5
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)
        
ax.legend(loc="upper right")
    
text(0, 1000,'N', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(45, 1000,'NE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(90, 1000,'E', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(135, 1000,'SE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(180, 1000,'S', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(225, 1000,'SW', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(270, 1000,'W', fontsize=14,color='red',weight='bold',ha='center', va='center')
grid()

#text(-30, 18000,'E', fontsize=16,color='black',weight='bold',ha='center', va='center')

savefig('out/hindcast/histww3_'+name+'.png', dpi=None, facecolor='w', edgecolor='w',
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
ax.bar(dado[:,3], dado[:,1], normed=True, bins=binshs, opening=.8, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig('out/hindcast/hsdp'+name+'.png', dpi=None, edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.1)    
plt.close()

ax = new_axes()
ax.bar(dado[:,3], dado[:,2], normed=True, bins=binstp, opening=.8, edgecolor='white',nsector=32)
ax.grid(True,linewidth=1.5,linestyle='dotted')
set_legend(ax)
savefig('out/hindcast/tpdp'+name+'.png', dpi=None, edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=True, bbox_inches=None, pad_inches=0.1)


plt.close()

# estatistica
f = open('out/hindcast/estatistica'+name+'.txt','w')
f.write('Estatistica para a reconstituicao \n')

f.write(''+name+'   Hs     Tp    Dp  \n')
f.write('Media:  ' + '%.2f' %np.mean(dado[:,1]) +'  '+ '%.2f' %np.mean(dado[:,2]) +'  ''%.2f' %np.mean(dado[:,3])+' \n')
f.write('\n')
f.write('Desvio:  '+'%.2f' %np.std(dado[:,1])+'  '+'%.2f' %np.std(dado[:,2])+'  '+'%.2f' %np.std(dado[:,3])+' \n')
f.write('\n')
f.write('90perc:  '+'%.2f' %np.percentile(dado[:,1],90)+'  '+'%.2f' %np.percentile(dado[:,2],90)+'  '+'%.2f' %np.percentile(dado[:,3],90)+' \n')
f.write('\n')
f.write('Maximo:  '+'%.2f' %np.max(dado[:,1])+'  '+'%.2f' %np.max(dado[:,2])+'  '+'%.2f' %np.max(dado[:,3])+' \n')
f.write('\n')
f.close()
# print "Desvio",np.std(dado[:,1]),np.std(dado[:,2]),np.std(dado[:,3])
# print "90perc",np.percentile(dado[:,1],90),np.percentile(dado[:,2],90),np.percentile(dado[:,3],90)
# print "maximo",np.max(dado[:,1]),np.max(dado[:,2]),np.max(dado[:,3])
# print " "
