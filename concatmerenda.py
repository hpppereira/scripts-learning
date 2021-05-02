# -*- coding: utf-8 -*-
'''
Avaliacao dos dados processados pela
BMO BR-MERENDA para o projeto ww3es
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
pathname = os.environ['HOME'] + '/Dropbox/ww3es/Geral/dados/BR_ES_Merenda/'

#caminho dos resultdaos da modelagem
pathname_mod3 = os.environ['HOME'] + '/Dropbox/ww3es/Geral/modelagem/Validacao/Merenda/'
direm = np.sort(os.listdir(pathname_mod3))

#         0     1   2   3   4
# ddm = Data, hora, Hs, Fp, Dp -- calcula o Tp mais abaixo
# ddm2 = np.array([[0,0,0,0,0]])
ddm = np.array([[0,0,0,0,0]])

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in direm:

    #carrega dados do modelo
    # dadosm2 = np.loadtxt(pathname_mod2 + dto + '/tab_southatl/tab50.ww3',skiprows=3,usecols=(0,1,4,9,10))
    # ddm2 = np.concatenate((ddm2,dadosm2),axis=0)

    #pula a primeira linha pois ja eh a mesma do ultima arquivo
    dadosm = np.loadtxt(pathname_mod3 + dto + '/tab_southatl/tab50.ww3',skiprows=4,usecols=(0,1,4,9,10))
    ddm = np.concatenate((ddm,dadosm),axis=0)

#calcula periodo de pico a partir da freq de pico do modelo
# tp_m2 = dd

# ddm2 = ddm2[1:,:]
ddm = ddm[1:,:]
#data com a funcao datetime

#modelo
data_mod = ddm[:,0].astype(str) #ano mes
data_mod_day = ddm[:,1].astype(int)
datam = np.array([datetime(int(data_mod[i][0:4]),int(data_mod[i][4:6]),int(data_mod[i][6:8]),int(data_mod_day[i])) for i in range(len(data_mod))])

#modelo - data em AAAAMMDDHHMMSS
datami = np.array([str(int(ddm[i,0]))+str(int(data_mod_day[i])).zfill(2)+'00' for i in range(len(data_mod))])
datami = datami.astype(int)

#carrega os dados
Merenda = np.loadtxt(pathname + 'saida.out',dtype=str) 

#cabecalhos
head = Merenda[0,:]

#cria matriz com variaveis de interesse (mnem)
ivar = []
for i in range(len(mnem)):
	ivar.append(int(np.where(head==mnem[i])[0]))

#variaveis de data e hora
data = Merenda[1:,ivar[0:2]]
#            0      1      2      3      4      5       6       7       8
# dados = 'VZMX','VMTA','VTPK','VMED','VPED','VCAR1','VTPK1','VCAR2','VTPK2']

#nova matriz com variaveis de interesse
dados = Merenda[1:,ivar[2:]].astype(float)

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
matondam = np.array([datami,ddm[:,2],1./ddm[:,3],ddm[:,4]]).T

#data em string
data_str_bmo = np.array(datat).astype(str)
data_str_mod = np.array(datam).astype(str)
pl.plot(datam,matondam[:,1],'.b',datat,matonda[:,1],'-r')
pl.ylabel('Hs (m)',fontsize=12), pl.grid()
#indices das datas iniciais e final da boia e modelo
indi_bmo = np.where(data_str_bmo == '2006-10-12 00:00:00')[0]
indf_bmo = np.where(data_str_bmo == '2006-12-25 23:00:00')[0]

indi_mod = np.where(data_str_mod == '2006-10-12 00:00:00')[0]
indf_mod = np.where(data_str_mod == '2006-12-25 23:00:00')[0]


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
# np.savetxt('saida/Merenda/'+'param_'+str(gl)+'_Merenda'+'.out',matonda,delimiter=',',fmt=['%i']+3*['%.2f'],
#     header='data,hs,tp,dp')

# #flags aplicados nos dados brutos
# np.savetxt('saida/Merenda/'+'flag_'+str(gl)+'_Merenda'+'.out',flagp,delimiter=',',fmt='%s',
#     header='data,hs,tp,dp')

# #parametros de ondas do modeloflags aplicados nos dados brutos
# np.savetxt('saida/ww3Merenda/'+'param_'+str(gl)+'_ww3Merenda'+'.out',matondam,delimiter=',',fmt='%s',
#     header='data,hs,tp,dp')

# #parametros do modelo sem os tempos onde nao tem data
# np.savetxt('saida/ww3bc10/'+'param_'+str(gl)+'_ww3bc10nest'+'.out',matondam[nest,:],delimiter=',',fmt='%s',
#     header='data,hs,tp,dp')


#figuras
pl.figure(figsize=(12,9))
pl.subplot(3,1,1)
pl.plot(datat,matonda[:,1],'-r',datam,matondam[:,1],'-b')
pl.ylabel('Hs (m)',fontsize=12), pl.grid()
pl.legend(['BM02','WW3'],ncol=2)
pl.ylim(0,5)

pl.subplot(3,1,2)
pl.plot(datat,matonda[:,2],'.r',datam,matondam[:,2],'.b')
pl.ylabel('Tp (s)',fontsize=12), pl.grid()
pl.ylim(0,20)

pl.subplot(3,1,3)
pl.plot(datat,matonda[:,3],'.r',datam,matondam[:,3],'.b')
pl.ylabel('Dp (graus)',fontsize=12), pl.grid()
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.ylim(0,360)

pl.show()
