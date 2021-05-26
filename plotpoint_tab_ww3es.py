'''
Separa estacoes do ano de acordo com os dias e
faz graficos 

- salva arquivo com o nome de cada estacao
- gera figuras

# ----------------------------------------------------------------------------------------
# Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  
# MotorDePopa Wave Research Group
# Rio de Janeiro - Brazil

'''

# ----------------------------------------------------------------------------------------
# Pay attention to the pre-requisites and libraries
import os
from datetime import datetime
import pylab as plt
import numpy as np
from pylab import *
from datetime import datetime
import pylab as pl

pathname = os.environ['HOME'] + '/Dropbox/ww3es/Geral/modelagem/Hindcast/Analise/geral/'

# 0    1    2    3     4   5   6   7     8
#ano, mes, dia, hora, min, hs, tp, dp, spread
bc10 = np.loadtxt(pathname + 'BC10.txt') #,usecols=(5,6,7)) 
br = np.loadtxt(pathname + 'BRMerenda.txt') #,usecols=(5,6,7)) 

estacao = 'primavera'

print 'Estacao de: ' + estacao

##########################################################################
#separa as estacoes de verao e inverno
# Primavera: 1 setembro ate 30 novembro
# Verao: 1 dezembro ate 28 fevereiro
# Outono: 1 marco ate 31 maio
# Inverno: 1 junho ate 31 agosto

#data total em datetime
#datat = [ datetime(int(hind[i,0]),int(hind[i,1]),int(hind[i,2]),int(hind[i,3])) for i in range(len(hind))]

######################################
#salva arquivos gerais

#geral
hs_bc10, tp_bc10, dp_bc10 = bc10[:,[5,6,7]].T
aux = zip(hs_bc10,tp_bc10,dp_bc10)
pl.savetxt('out/estacoes/bc10_onda_geral.out',aux,fmt='%.3f')

hs_br, tp_br, dp_br = br[:,[5,6,7]].T
aux = zip(hs_br,tp_br,dp_br)
pl.savetxt('out/estacoes/br_onda_geral.out',aux,fmt='%.3f')


######################################
#separa as estacoes

if estacao == 'primavera':
    ind_bc10 = np.where((bc10[:,1] == 9) | (bc10[:,1] == 10) | (bc10[:,1] == 11))[0] #primavera
    ind_br = np.where((br[:,1] == 9) | (br[:,1] == 10) | (br[:,1] == 11))[0] #inverno
elif estacao == 'verao':
    ind_bc10 = np.where((bc10[:,1] == 12) | (bc10[:,1] == 1) | (bc10[:,1] == 2))[0] #verao
    ind_br = np.where((br[:,1] == 12) | (br[:,1] == 1) | (br[:,1] == 2))[0] #inverno
elif estacao == 'outono':
    ind_bc10 = np.where((bc10[:,1] == 3) | (bc10[:,1] == 4) | (bc10[:,1] == 5))[0] #outono
    ind_br = np.where((br[:,1] == 3) | (br[:,1] == 4) | (br[:,1] == 5))[0] #inverno
elif estacao == 'inverno':
    ind_bc10 = np.where((bc10[:,1] == 6) | (bc10[:,1] == 7) | (bc10[:,1] == 8))[0] #inverno
    ind_br = np.where((br[:,1] == 6) | (br[:,1] == 7) | (br[:,1] == 8))[0] #inverno


#salva arquivo da estacao de em bc10
aux_bc10 = bc10[ind_bc10,:]
hs_bc10, tp_bc10, dp_bc10 = aux_bc10[:,[5,6,7]].T
aux = zip(hs_bc10,tp_bc10,dp_bc10)
pl.savetxt('out/estacoes/bc10_onda_'+estacao+'.out',aux,fmt='%.3f')

#salva arquivo da estacao de em bc10
aux_br = br[ind_br,:]
hs_br, tp_br, dp_br = aux_br[:,[5,6,7]].T
aux = zip(hs_br,tp_br,dp_br)
pl.savetxt('out/estacoes/br_onda_'+estacao+'.out',aux,fmt='%.3f')


##########################################################################


#histogram

fig = plt.figure(figsize=(16,12))
ax = fig.add_subplot(321)
binshs=np.arange(0,5.5,0.5)
counts,bins,patches = ax.hist(hs_bc10[:],bins=binshs,facecolor='gray',edgecolor='black',hatch="/",label="Hs (m)")
ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,70,10): lima.append((i*len(hs_bc10)/100))

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
text(0.3, 18000,'A', fontsize=16,color='black',weight='bold',ha='center', va='center')

ax = fig.add_subplot(322)
binshs=np.arange(0,5.5,0.5)
counts,bins,patches = ax.hist(hs_br[:],bins=binshs,facecolor='gray',edgecolor='black',hatch="/",label="Hs (m)")
ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,70,10): lima.append((i*len(hs_bc10)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(hs_bc10)) ) * 100, 0)) + ' %'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 0.25
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)

ax.legend(loc="upper right")
text(.3, 18000,'B', fontsize=16,color='black',weight='bold',ha='center', va='center')
grid()


ax = fig.add_subplot(323)
binstp=np.arange(0,22,2)
counts,bins,patches = ax.hist(tp_bc10[:],bins=binstp,facecolor='gray',edgecolor='black',hatch="/",label="Tp (s)")
ax.set_xticks(bins)
#setar eixo y com porcentagem
lima=[]
for i in range(0,70,10): lima.append((i*len(tp_bc10)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(tp_bc10)) ) * 100.0, 0)) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1]-1
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0),weight='bold', xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)
        
ax.legend(loc="upper right")
text(1, 18000,'C', fontsize=16,color='black',weight='bold',ha='center', va='center')

grid()

ax = fig.add_subplot(324)
binstp=np.arange(0,22,2)
counts,bins,patches = ax.hist(tp_br[:],bins=binstp,facecolor='gray',edgecolor='black',hatch="/",label="Tp (s)")
ax.set_xticks(bins)
#setar eixo y com porcentagem
lima=[]
for i in range(0,70,10): lima.append((i*len(tp_bc10)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(tp_bc10)) ) * 100.0, 0)) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1]-1
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0),weight='bold', xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)
        
ax.legend(loc="upper right")
text(1, 18000,'D', fontsize=16,color='black',weight='bold',ha='center', va='center')

grid()

ax = fig.add_subplot(325)
bins=arange(-22.5,360,45)
counts,bins,patches = ax.hist(dp_bc10[:],bins=bins,facecolor='gray',edgecolor='black',hatch="/",label="Dp (graus)")

ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,70,10): lima.append((i*len(dp_bc10)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(dp_bc10)) ) * 100.0, 0)) + '%'
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
text(-30, 18000,'E', fontsize=16,color='black',weight='bold',ha='center', va='center')


ax = fig.add_subplot(326)
bins=arange(-22.5,360,45)
counts,bins,patches = ax.hist(dp_br[:],bins=bins,facecolor='gray',edgecolor='black',hatch="/",label="Dp (graus)")

ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,70,10): lima.append((i*len(dp_bc10)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(dp_bc10)) ) * 100.0, 0)) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 22.5
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)
        
ax.legend(loc="upper right")
    
text(0, 1000,'N', fontsize=13,color='red',weight='bold',ha='center', va='center')
text(45, 1000,'NE', fontsize=13,color='red',weight='bold',ha='center', va='center')
text(90, 1000,'E', fontsize=13,color='red',weight='bold',ha='center', va='center')
text(135, 1000,'SE', fontsize=13,color='red',weight='bold',ha='center', va='center')
text(180, 1000,'S', fontsize=13,color='red',weight='bold',ha='center', va='center')
text(225, 1000,'SW', fontsize=13,color='red',weight='bold',ha='center', va='center')
text(270, 1000,'W', fontsize=13,color='red',weight='bold',ha='center', va='center')
grid()
text(-30, 18000,'F', fontsize=16,color='black',weight='bold',ha='center', va='center')


savefig('histww3_'+estacao+'.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=False, bbox_inches=None, pad_inches=0.1)

savefig('histww3_'+estacao+'.eps', dpi=1200, facecolor='w', edgecolor='w',
orientation='portrait',format='eps')

plt.close()

print 'BC10','Hs','Tp','Dp'
print "Media",np.mean(hs_bc10),np.mean(tp_bc10),np.mean(dp_bc10)
print "Desvio",np.std(hs_bc10),np.std(tp_bc10),np.std(dp_bc10)
print "90perc",np.percentile(hs_bc10,90),np.percentile(tp_bc10,90),np.percentile(dp_bc10,90)
print "maximo",np.max(hs_bc10),np.max(tp_bc10),np.max(dp_bc10)
print " "

print 'MERENDA','Hs','Tp','Dp'
print "Media",np.mean(hs_br),np.mean(tp_br),np.mean(dp_br)
print "Desvio",np.std(hs_br),np.std(tp_br),np.std(dp_br)
print "90perc",np.percentile(hs_br,90),np.percentile(tp_br,90),np.percentile(dp_br,90)
print "maximo",np.max(hs_br),np.max(tp_br),np.max(dp_br)

