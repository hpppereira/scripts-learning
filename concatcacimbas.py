'''
Processamento dos dados de ADCP de Cacimbas-ES
Projeto: WW3ES
LIOc-COPPE/UFRJ

Concatena os dados de cada campanha, faz a consistencia dos
parametros calculados e salva um txt.

Utiliza processamento com 8 gl
Utilizar o resultado do modelo com 3 grades

prof em milimetros

##o arquivo salva nao desconta a declinacao magnetica: -23 graus
##lembrar de descontar na rotina de pos processamento
'''

import numpy as np
from datetime import datetime
import os
import pylab as pl
import consiste_proc

reload(consiste_proc)

dataset = [1,5,7,2,6,7,8,2,2,7,8,3,7,3,7,3,15,6]

#funcao para media movel
def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    #including valid will REQUIRE there to be enough datapoints.
    #for example, if you take out valid, it will start @ point one,
    #not having any prior points, so itll be 1+0+0 = 1 /3 = .3333
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array

#Will print out a 3MA for our dataset
# print movingaverage(dataset,3)

#declinacao magnetica
dmag = -23

#graus de liberdade calculado pelo adcp (8, 16 e 32)
gl = 8

#diretorio de onde estao os dados
pathname = os.environ['HOME'] + '/Dropbox/lioc/dados/ww3es/CACIMBAS/ADCP/param' + str(gl) + '/'
# pathname_mod2 = os.environ['HOME'] + '/Dropbox/ww3es/Geral/modelagem/resultados/Cacimbas/Cacimbas_2Grades/'
pathname_mod3 = os.environ['HOME'] + '/Dropbox/ww3es/Geral/modelagem/Validacao/Cacimbas/Cacimbas_3Grades/'

#lista os diretorios dentro de pathname
dires = np.sort(os.listdir(pathname))
direm = np.sort(os.listdir(pathname_mod3))

pl.close('all')

#dados concatenados
#      1   2   3   4   8   9   10   11     12    13     14  -- colunas da matriz original
#      0   1   2   3   4   5   6    7      8     9      10  -- colunas na matriz 'dd'
# dd = YY, MM, DD, HH, Hs, Tp, Dp, Depth, H/10, Tmean, Dmean
dd = np.array([[0,0,0,0,0,0,0,0,0,0,0]])

#         0     1   2   3   4
# ddm = Data, hora, Hs, Fp, Dp -- calcula o Tp mais abaixo
# ddm2 = np.array([[0,0,0,0,0]])
ddm = np.array([[0,0,0,0,0]])

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in dires:

	#carrega dados do ADCP
	dados = np.loadtxt(pathname + dto + '/' + 'WAVES_000_000_LOG8.TXT',delimiter=',',
		usecols=(1,2,3,4,8,9,10,11,12,13,14))

	dd = np.concatenate((dd,dados),axis=0)

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in direm:

	#carrega dados do modelo
	# dadosm2 = np.loadtxt(pathname_mod2 + dto + '/tab_southatl/tab50.ww3',skiprows=3,usecols=(0,1,4,9,10))
	# ddm2 = np.concatenate((ddm2,dadosm2),axis=0)

    #pula a primeira linha pois ja eh a mesma do ultima arquivo
	dadosm = np.loadtxt(pathname_mod3 + dto + '/tab_baciaES/tab50.ww3',skiprows=4,usecols=(0,1,4,9,10))
	ddm = np.concatenate((ddm,dadosm),axis=0)

#calcula periodo de pico a partir da freq de pico do modelo
# tp_m2 = dd

#retira a primeira linha que foi utilizada para concatenar (zeros)
dd = dd[1:,:]
dd[:,0] = dd[:,0] + 2000 #acrescenta 2000 para a data ficar correta
# ddm2 = ddm2[1:,:]
ddm = ddm[1:,:]

#define variaveis dos dados
hs = dd[:,4] #altura sig
tp = dd[:,5] #periodo de pico
dp = dd[:,6]# + dmag #direcao de pico
h = dd[:,7] * 10**-3 #profunidade (mm) para metros
h10 = dd[:,8] #altrua de 1/10
tm = dd[:,9] #periodo medio Tmean
dm = dd[:,10] #direcao media Dmean

#corrige dp
# dp[pl.find(dp < 0)] = dp[pl.find(dp < 0)] + 360

#data com a funcao datetime

#modelo
data_mod = ddm[:,0].astype(str) #ano mes
data_mod_day = ddm[:,1].astype(int)
datam = np.array([datetime(int(data_mod[i][0:4]),int(data_mod[i][4:6]),int(data_mod[i][6:8]),int(data_mod_day[i])) for i in range(len(data_mod))])

#modelo - data em AAAAMMDDHHMMSS
datami = np.array([str(int(ddm[i,0]))+str(int(data_mod_day[i])).zfill(2)+'00' for i in range(len(data_mod))])
datami = datami.astype(int)

#adcp
datat = np.array([datetime(int(dd[i,0]),int(dd[i,1]),int(dd[i,2]),int(dd[i,3])) for i in range(len(dd))])
#adcp - data em AAAAMMDDHHMMSS
datai = np.array([str(int(dd[i,0]))+str(int(dd[i,1])).zfill(2)+str(int(dd[i,2])).zfill(2)+str(int(dd[i,3])).zfill(2)+'00' for i in range(len(dd))])
datai = datai.astype(int)


#consistencia do adcp fora da agua (depth < 18)
#acha profundidades menores que 18 m (a prof do adcp eh ~20m)
indf = np.where(h < 18)[0]

#coloca nan onde para profundidades menores que 18 m
hs[indf] = np.nan
tp[indf] = np.nan
dp[indf] = np.nan
h10[indf] = np.nan
tm[indf] = np.nan
dm[indf] = np.nan

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
flagp[:,2] = consiste_proc.faixa(tp,2,25,3,20,flagp[:,2])
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
hs, tp , dp  = matonda[:,1:7].T

#media movel (diminui o comprimento do vetor)
wind = 5

hs = movingaverage(hs,wind)
tp = movingaverage(tp,wind)
dp = movingaverage(dp,wind)
h10 = movingaverage(h10,wind)
tm = movingaverage(tm,wind)
dm = movingaverage(dm,wind)

#cria array com o vetor de pontos reduzido
matondap = np.array([datai[:-wind+1],hs,tp,dp]).T

datat = datat[:-wind+1]

#cria variavel matondam com os parametros do modelo (hs, tp e dp)
matondam = np.array([datami,ddm[:,2],1./ddm[:,3],ddm[:,4]]).T

# deixa os vetores do mesmo tamanho
fim_adcp = np.where(datai==datami[-1])[0]
ini_mod = np.where(datami==datai[0])[0]

matondap = matondap[:fim_adcp,:]
datat = datat[:fim_adcp]
matondam = matondam[ini_mod:,:]
datam = datam[ini_mod:]

nest = np.zeros(len(datat)) #vetor de zeros do tamanho dos dados 
datas_cac = datat.astype(str)
datas_ww3 = datam.astype(str)

for idata in range(len(datas_cac)):
    nest[idata] = np.where(datas_ww3 == datas_cac[idata])[0]

nest = nest.astype(int)


#retira os dados com nan (para salvar e fazer as estatisticas)
# indhs = np.where(np.isnan(matondap[:,1]) == False)[0]
# indtp = np.where(np.isnan(matondap[:,2]) == False)[0]
# inddp = np.where(np.isnan(matondap[:,3]) == False)[0]

# matondap[:,1] = matondap[indhs,1]
# matondap[:,2] = matondap[indhs,2]
# matondap[:,3] = matondap[indhs,3]


#parametros de onda
# np.savetxt('saida/cacimbas/'+'param_'+str(gl)+'_cacimbas'+'.out',matondap,delimiter=',',fmt=['%i']+3*['%.2f'],
#     header='data,hs,tp,dp')

# #flags aplicados nos dados brutos
# np.savetxt('saida/cacimbas/'+'flag_'+str(gl)+'_cacimbas'+'.out',flagp,delimiter=',',fmt='%s',
#     header='data,hs,tp,dp')

# #parametros de ondas do modeloflags aplicados nos dados brutos
# np.savetxt('saida/ww3cacimbas/'+'param_'+str(gl)+'_ww3cacimbas'+'.out',matondam,delimiter=',',fmt=['%i']+3*['%.2f'],
#     header='data,hs,tp,dp')


# #parametros do modelo sem os tempos onde nao tem data
# np.savetxt('saida/ww3cacimbas/'+'param_'+str(gl)+'_ww3cacimbasnest'+'.out',matondam[nest,:],delimiter=',',fmt='%s',
#     header='data,hs,tp,dp')

#figuras
pl.figure(figsize=(12,9))
pl.subplot(3,1,1)
pl.plot(datat,matondap[:,1],'-r',datam,matondam[:,1],'-b')
pl.ylabel('Hs (m)',fontsize=12), pl.grid()
pl.legend(['CACIMBAS','WW3'],ncol=2)
pl.ylim(0,4)

pl.subplot(3,1,2)
pl.plot(datat,matondap[:,2],'.r',datam,matondam[:,2],'.b')
pl.ylabel('Tp (s)',fontsize=12), pl.grid()
pl.ylim(0,20)

pl.subplot(3,1,3)
pl.plot(datat,matondap[:,3],'.r',datam,matondam[:,3],'.b')
pl.ylabel('Dp (graus)',fontsize=12), pl.grid()
pl.yticks([0,45,90,135,180,225,270,315,360])
pl.ylim(0,360)

pl.show()


