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
import pandas as pd

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/ww3seal/modelagem/analise/geral/'

# 0    1    2    3     4   5   6   7     8
#ano, mes, dia, hora, min, hs, tp, dp, spread
axys = np.loadtxt(pathname + 'geral.txt') #,usecols=(5,6,7)) 

estacao = 'inverno'

print 'Estacao de: ' + estacao

##########################################################################
#separa as estacoes de verao e inverno
# Primavera: 1 setembro ate 30 novembro
# Verao: 1 dezembro ate 28 fevereiro
# Outono: 1 marco ate 31 maio
# Inverno: 1 junho ate 31 agosto

#data geral em datetime
datat = np.array([ datetime(int(axys[i,0]),int(axys[i,1]),int(axys[i,2]),int(axys[i,3])) for i in range(len(axys))])

######################################
#salva arquivos gerais

#geral
hs_axys, tp_axys, dp_axys = axys[:,[5,6,7]].T
aux = zip(hs_axys,tp_axys,dp_axys)

df_geral = pd.DataFrame(aux, columns=['hs','tp','dp'])

df_geral['date'] = datat

df_geral = df_geral.set_index('date')

df_geral.to_csv('out/estacoes/axys_onda_geral.csv')


######################################
#separa as estacoes

if estacao == 'primavera':
    ind_axys = np.where((axys[:,1] == 9) | (axys[:,1] == 10) | (axys[:,1] == 11))[0] #primavera
elif estacao == 'verao':
    ind_axys = np.where((axys[:,1] == 12) | (axys[:,1] == 1) | (axys[:,1] == 2))[0] #verao
elif estacao == 'outono':
    ind_axys = np.where((axys[:,1] == 3) | (axys[:,1] == 4) | (axys[:,1] == 5))[0] #outono
elif estacao == 'inverno':
    ind_axys = np.where((axys[:,1] == 6) | (axys[:,1] == 7) | (axys[:,1] == 8))[0] #inverno
elif estacao == 'geral':
    ind_axys = np.arange(len(axys))

#salva arquivo da estacao de em axys
aux_axys = axys[ind_axys,:]
hs_axys, tp_axys, dp_axys = aux_axys[:,[5,6,7]].T

#aux = zip(hs_axys,tp_axys,dp_axys)
#pl.savetxt('out/estacoes/axys_onda_'+estacao+'.out',aux,fmt='%.3f')


df_estac = pd.DataFrame(aux_axys[:,[5,6,7]], columns=['hs','tp','dp'])

df_estac['date'] = datat[ind_axys]

df_estac = df_estac.set_index('date')

df_estac.to_csv('out/estacoes/axys_onda_' + estacao + '.csv')



##########################################################################


#histogram

fig = plt.figure(figsize=(16,12))
ax = fig.add_subplot(311)
binshs=np.arange(0,5.5,0.5)
counts,bins,patches = ax.hist(hs_axys[:],bins=binshs,facecolor='gray',edgecolor='black',hatch="/",label="Hs (m)")
ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,90,10): lima.append((i*len(hs_axys)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(hs_axys)) ) * 100, 0)) + ' %'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 0.25
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=13)

ax.legend(loc="upper right")
grid()
text(0.27, 21000,'A', fontsize=16,color='black',weight='bold',ha='center', va='center')



#####################################


ax = fig.add_subplot(312)
binstp=np.arange(0,22,2)
counts,bins,patches = ax.hist(tp_axys[:],bins=binstp,facecolor='gray',edgecolor='black',hatch="/",label="Tp (s)")
ax.set_xticks(bins)
#setar eixo y com porcentagem
lima=[]
for i in range(0,90,10): lima.append((i*len(tp_axys)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(tp_axys)) ) * 100.0, 0)) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1]-1
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0),weight='bold', xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=13)
        
ax.legend(loc="upper right")
text(1, 21000,'B', fontsize=16,color='black',weight='bold',ha='center', va='center')

grid()

############################################


ax = fig.add_subplot(313)
bins=arange(-22.5,360,45)
counts,bins,patches = ax.hist(dp_axys[:],bins=bins,facecolor='gray',edgecolor='black',hatch="/",label="Dp (graus)")

ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,90,10): lima.append((i*len(dp_axys)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(dp_axys)) ) * 100.0, 0)) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 22.5
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=13)
        
ax.legend(loc="upper right")
    
text(0, 1000,'N', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(45, 1000,'NE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(90, 1000,'E', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(135, 1000,'SE', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(180, 1000,'S', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(225, 1000,'SW', fontsize=14,color='red',weight='bold',ha='center', va='center')
text(270, 1000,'W', fontsize=14,color='red',weight='bold',ha='center', va='center')
grid()
text(-30, 21000,'C', fontsize=16,color='black',weight='bold',ha='center', va='center')


#################################


savefig('fig/hist/histww3_'+estacao+'.png', dpi=None, facecolor='w', edgecolor='w',
orientation='portrait', papertype=None, format='png',
transparent=False, bbox_inches=None, pad_inches=0.1)

savefig('fig/hist/histww3_'+estacao+'.eps', dpi=1200, facecolor='w', edgecolor='w',
orientation='portrait',format='eps')

plt.show()
#plt.close()

print 'axys','Hs','Tp','Dp'
print "Media  %.2f , %.2f , %.i " %(np.mean(hs_axys),np.mean(tp_axys),np.mean(dp_axys))
print "Desvio %.2f , %.2f , %.i " %(np.std(hs_axys),np.std(tp_axys),np.std(dp_axys))
print "90perc %.2f , %.2f , %.i " %(np.percentile(hs_axys,90),np.percentile(tp_axys,90),np.percentile(dp_axys,90))
print "maximo %.2f , %.2f , %.i " %(np.max(hs_axys),np.max(tp_axys),np.max(dp_axys))
print " "
