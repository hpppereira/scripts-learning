# -*- coding: utf-8 -*-
'''
Programa principal para 
Avaliacao dos dados processados pela
BMO BC-10 para o projeto ww3es
Concatena os dados de cada campanha, faz a consistencia dos
parametros calculados e salva um txt.
Abre os resultados do WW3 para o mesmo periodo e escreve um txt.

MNEMONICOS (utilizados):
Para obter Hs usar 4.01*sqrt(VMTA) ou 4.01*sqrt(VMTA1)

DATA ex: 05/11/2006
HORA ex: 13:00
VZMX Altura Máxima no dominio do tempo
VMTA Momento Espectral de Ordem 0
VTPK Período de Pico Espectral
VMED Direção Média de Propagação
VPED Direção Espectral
VCAR1 Altura Significativa do Pico 1 (Mais Energético)
VTPK1 Período de Pico Espectral do Pico 1 (Mais Energético)
VCAR2 Altura Significativa do Pico 2. O segundo mais energético.
VTPK2 Período de Pico Espectral do Pico 2. O segundo mais energético.

Observacoes:
a) Todos os arquivos (fases) tem o mesmo tamanho de matriz
com as mesmas variaveis

'''

import numpy as np
import pylab as pl
import os
from datetime import datetime
import consiste_proc

# pl.close('all')

#mnemonicos utilizados
mnem = ['DATA','HORA','VZMX','VMTA','VTPK','VMED','VPED','VCAR1','VTPK1','VCAR2','VTPK2']

# defini grau de liberdade de mentira
gl=8

#caminho de onde estao os dados
pathname = os.environ['HOME'] + '/Dropbox/lioc/dados/ww3es/BC-10/BMO/'

#caminho dos resultdaos da modelagem
pathname_mod = os.environ['HOME'] + '/Dropbox/ww3es/Geral/modelagem/' #Validacao/'

#carrega os dados
bc10_2 = np.loadtxt(pathname + 'BC-10_fase02_b.fim',dtype=str) #fase 2
bc10_3 = np.loadtxt(pathname + 'BC-10_fase03_a.fim',dtype=str) #fase 3
bc10_4 = np.loadtxt(pathname + 'BC-10_fase04_a.fim',dtype=str) #fase 4

#carrega resultados modelados
mod_t1=np.loadtxt(pathname_mod + 'bc10_f234.ww3',dtype=float)
hs_mod = mod_t1[:,4]
fp_mod = mod_t1[:,9]
tp_mod = 1./fp_mod
dp_mod = mod_t1[:,10]

#modelos
data_mod = mod_t1[:,0].astype(str)
data_mod_day = mod_t1[:,1].astype(int)

datam = [datetime(int(data_mod[i][0:4]),int(data_mod[i][4:6]),int(data_mod[i][6:8]),int(data_mod_day[i])) for i in range(len(data_mod))]

#modelo - data em AAAAMMDDHHMMSS
datami = np.array([str(int(mod_t1[i,0]))+str(int(data_mod_day[i])).zfill(2)+'00' for i in range(len(data_mod))])
datami = datami.astype(int)


#cabecalhos
head = bc10_2[0,:]

#cria matriz com variaveis de interesse (mnem)
ivar = []
for i in range(len(mnem)):
	ivar.append(int(np.where(head==mnem[i])[0]))

#variaveis de data e hora
data2 = bc10_2[1:,ivar[0:2]]
data3 = bc10_3[1:,ivar[0:2]]
data4 = bc10_4[1:,ivar[0:2]]

#            0      1      2      3      4      5       6       7       8
# dados = 'VZMX','VMTA','VTPK','VMED','VPED','VCAR1','VTPK1','VCAR2','VTPK2']

#nova matriz com variaveis de interesse
dados2 = bc10_2[1:,ivar[2:]].astype(float)
dados3 = bc10_3[1:,ivar[2:]].astype(float)
dados4 = bc10_4[1:,ivar[2:]].astype(float)

#concatenar os dados 2, 3 e 4
dados = np.concatenate((dados2,dados3,dados4),axis=0)
data = np.concatenate((data2,data3,data4),axis=0)

#data com a funcao datetime
#dados
datat = [datetime(int(data[i,0][6:10]),int(data[i,0][3:5]),int(data[i,0][0:2]),int(data[i,1][0:2])) for i in range(len(data))]
#adcp - data em AAAAMMDDHHMMSS
datai = np.array([str(int(data[i,0][6:10]))+str(int(data[i,0][3:5])).zfill(2)+str(int(data[i,0][0:2])).zfill(2)+str(int(data[i,1][0:2])).zfill(2)+'00' for i in range(len(data[:,0]))])
datai = datai.astype(int)

#calcula a altura significativa
hs = 4.01 * np.sqrt(dados[:,1])

#define variaveis
hmax = dados[:,0]
tp = dados[:,2]
tp1 = dados[:,6]
tp2 = dados[:,8]
dm = dados[:,3]
dp = dados[:,4]

#cria matriz com parametros de onda
matonda = np.array([datai,hs,tp,dp]).T

#consistencia dos dados processados (rotina consiste_proc)

#cria vetores de flags das series processadas (depende das qtdade de variaveis a serem consistidas + data) 
flagp = np.zeros((len(datai),3+1),dtype='|S32')
flagp[:,0] = datai

# # ================================================================================== #  
# # Testes de consistencia dos dados processados

#Teste 1 - faixa
flagp[:,1] = consiste_proc.faixa(hs,0.15,15,0.25,8,flagp[:,1])
flagp[:,2] = consiste_proc.faixa(tp,2,30,3,25,flagp[:,2])
flagp[:,3] = consiste_proc.faixa(dp,0,360,0,360,flagp[:,3])

#Teste 2 - variabilidade
flagp[:,1] = consiste_proc.variab(hs,1,5,flagp[:,1])
flagp[:,2] = consiste_proc.variab(tp,1,20,flagp[:,2])
flagp[:,3] = consiste_proc.variab(dp,1,360,flagp[:,3])

#Teste 3 - consecutivos iguais
flagp[:,1] = consiste_proc.iguais(hs,5,flagp[:,1])
flagp[:,2] = consiste_proc.iguais(tp,10,flagp[:,2])
flagp[:,3] = consiste_proc.iguais(dp,10,flagp[:,3])


# ================================================================================== #  
# Coloca nan nos dados reprovados e suspeitos (flag = 3 e 4)

# matondap = np.copy(matondab)

for c in range(1,flagp.shape[1]):
    for i in range(len(flagp)):
    	#elimina dados ruins
        if '4' in flagp[i,c]:
            matonda[i,c] = np.nan
    	#elimina dados suspeitos (se nao for para exluir, comentar esta parte)
        elif '3' in flagp[i,c]:
            matonda[i,c] = np.nan


# define variaveis com o nan nos dados com flag = 4
hs, tp , dp  = matonda[:,1:4].T

#cria variavel matondam com os parametros do modelo
matondam = np.array([datami,hs_mod,tp_mod,dp_mod]).T

#data em string
data_str_bmo = np.array(datat).astype(str)
data_str_mod = np.array(datam).astype(str)

#indices das datas iniciais e final da boia e modelo
indi_bmo = np.where(data_str_bmo == '2006-11-05 13:00:00')[0]
indf_bmo = np.where(data_str_bmo == '2008-06-18 00:00:00')[0]

indi_mod = np.where(data_str_mod == '2006-11-05 13:00:00')[0]
indf_mod = np.where(data_str_mod == '2008-06-18 00:00:00')[0]


matonda = matonda[indi_bmo:indf_bmo,:]
datat = datat[indi_bmo:indf_bmo]
matondam = matondam[indi_mod:indf_mod,:]
datam = datam[indi_mod:indf_mod]

# Pegando os pontos onde tenho dado e modelo
nest = np.zeros(len(data_str_bmo[indi_bmo:indf_bmo]))
data_str_bmo1=data_str_bmo[indi_bmo:indf_bmo]
data_str_mod1=data_str_mod[indi_mod:indf_mod]

for idata in range(len(data_str_bmo[indi_bmo:indf_bmo])):
    nest[idata]=np.where(data_str_mod1 == data_str_bmo1[idata])[0]

nest=nest.astype(int)

#parametros de onda
# np.savetxt('saida/bc10/'+'param_'+str(gl)+'_bc10'+'.out',matonda,delimiter=',',fmt=['%i']+3*['%.2f'],
#     header='data,hs,tp,dp')

# #flags aplicados nos dados brutos
# np.savetxt('saida/bc10/'+'flag_'+str(gl)+'_bc10'+'.out',flagp,delimiter=',',fmt='%s',
#     header='data,hs,tp,dp')

# #parametros de ondas do modeloflags aplicados nos dados brutos
# np.savetxt('saida/ww3bc10/'+'param_'+str(gl)+'_ww3_bc10'+'.out',matondam,delimiter=',',fmt='%s',
#     header='data,hs,tp,dp')

# #parametros do modelo sem os tempos onde nao tem data
# np.savetxt('saida/ww3bc10/'+'param_'+str(gl)+'_ww3bc10nest'+'.out',matondam[nest,:],delimiter=',',fmt='%s',
#     header='data,hs,tp,dp')

#figuras
pl.figure(figsize=(12,9))
pl.subplot(3,1,1)
pl.plot(datat,matonda[:,1],'-r',datam,matondam[:,1],'-b')
pl.ylabel('Hs (m)',fontsize=12), pl.grid()
pl.legend(['BM01','WW3'],ncol=2)
pl.ylim(0,6)

pl.subplot(3,1,2)
pl.plot(datat,matonda[:,2],'.r',datam,matondam[:,2],'.b')
pl.ylabel('Tp (s)',fontsize=12), pl.grid()
pl.ylim(0,20)

pl.subplot(3,1,3)
pl.plot(datat,matonda[:,3],'.r',datam,matondam[:,3],'.b')
pl.ylabel('Dp (graus)',fontsize=12), pl.grid()
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.ylim(0,360)


# --------------------------- histogram --------------------------
hs=matondam[:,1]
tp=matondam[:,2]
dp=matondam[:,3]

fig = pl.figure(figsize=(15,12))
ax = fig.add_subplot(311)
binshs=np.arange(0,6.5,0.5)
counts,bins,patches = ax.hist(hs[:],bins=binshs,facecolor='yellow',edgecolor='gray',label="Hs (m)")
ax.set_xticks(bins)
bin_centers=np.diff(bins) + bins[:-1] - 0.25
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -10), textcoords='offset points', va='top', ha='center')

pl.title(' Wavewatch III - BRMerenda - 1996 a 2010',fontsize=16)
ax.legend(loc="upper right")
pl.grid()


ax = fig.add_subplot(312)
binstp=np.arange(0,22,2)
counts,bins,patches = ax.hist(tp[:],bins=binstp,facecolor='yellow',edgecolor='gray',label="Tp (s)")
ax.set_xticks(bins)
bin_centers=np.diff(bins) + bins[:-1]-1
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0),weight='bold', xycoords=('data', 'axes fraction'),
        xytext=(0, -10), textcoords='offset points', va='top', ha='center')
        
ax.legend(loc="upper right")
pl.grid()

ax = fig.add_subplot(313)
bins=np.arange(-22.5,360,45)
counts,bins,patches = ax.hist(dp[:],bins=bins,facecolor='yellow',edgecolor='gray',label="Dp (graus)")
ax.set_xticks(bins)
bin_centers=np.diff(bins) + bins[:-1] - 22.5
for count, x in zip(counts,bin_centers):
    percent = '%0.1f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
        xytext=(0, -10), textcoords='offset points', va='top', ha='center')
        
ax.legend(loc="upper right")
    
pl.text(0, 500,'N', fontsize=14,color='red',weight='bold',ha='center', va='center')
pl.text(45, 500,'NE', fontsize=14,color='red',weight='bold',ha='center', va='center')
pl.text(90, 500,'E', fontsize=14,color='red',weight='bold',ha='center', va='center')
pl.text(135, 500,'SE', fontsize=14,color='red',weight='bold',ha='center', va='center')
pl.text(180, 500,'S', fontsize=14,color='red',weight='bold',ha='center', va='center')
pl.text(225, 500,'SW', fontsize=14,color='red',weight='bold',ha='center', va='center')
pl.text(270, 500,'W', fontsize=14,color='red',weight='bold',ha='center', va='center')
pl.grid()

# pl.savefig('saida/histww3.png', dpi=None, facecolor='w', edgecolor='w',
# orientation='portrait', papertype=None, format='png',
# transparent=False, bbox_inches=None, pad_inches=0.1)


#plt.close()

pl.show()
