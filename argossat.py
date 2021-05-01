'''
Processamento dos dados baixados do
site ARGOS

O arquivo baixado a vem com todas as boias
selecionadas no site

Boias:
b69007: recife
b69009: baia de guanabara
b69150: florianopolis
b69151: santos
b69153: rio grande

Ultima modificacao: 25/08/2015

'''

import numpy as np
import os
import pylab as pl
from collections import defaultdict
from datetime import datetime
import consiste_proc

reload(consiste_proc)

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/ARGOS/sat/'
arqname = 'ArgosData_2014_11_19_14_57_24.csv'

f = open(pathname + arqname)

#habilita plotagem dos 28 sensores (gg = 1-plota, 0-nao) 
# boia a ser plotada (bb='ID_Argos')
gg = 1
bb = '69153'

#parametros para a consistencia
#observacoes: nao classifica como inconsistente os dados suspeitos

# b69153 - rio grande
# t1a, t1b, t1c, t1d = 0.25, 5, 0.25, 5
# t2a, t2b = 1, 2.5
# t3a = 5

# b69151 - santos
t1a, t1b, t1c, t1d = 0.25, 15, 0.25, 15
t2a, t2b = 1, 2.5
t3a = 5


#le cada linha
lines = f.read().splitlines()

#mnemonicos da matriz inteira (49 menonicos)
mnem = np.array(lines[0].split(';'))

#mnemonicos dos sensores
mnem1 = np.array(['???','hour','wind speed 1','wind gust1','wind dir 1','air temp','relative humidity','dew point',
	'pressure','sst','buoy heading','clorofila','turbidez','solar rad','CM velocity 1','CM direction 1','CM velocity 2',
	'CM direction 2','CM velocity 3','CM direction 3','Hs','Hmax','Periodo','Mn dir','spread','spare','???','???',
	'???','???','???','???'])

b69007 = [] #recife
b69009 = [] #baia de guanabara
b69150 = [] #florianopolis
b69151 = [] #santos
b69153 = [] #rio grande

for line in  lines:

	if 'DEFAULT' in line:

		continue

	elif '69007' in line: #recife

		b69007.append(line.split(';'))

	elif '69009' in line: #baia de guanabara

		b69009.append(line.split(';'))

	elif '69150' in line: #florianopolis

		b69150.append(line.split(';'))

	elif '69151' in line: #santos

		b69151.append(line.split(';'))

	elif '69153' in line: #rio grande

		b69153.append(line.split(';'))


b69007 = np.array(b69007)
b69009 = np.array(b69009)
b69150 = np.array(b69150)
b69151 = np.array(b69151)
b69153 = np.array(b69153)

b69007[np.where(b69007 == '')] = np.nan
b69009[np.where(b69009 == '')] = np.nan
b69150[np.where(b69150 == '')] = np.nan
b69151[np.where(b69151 == '')] = np.nan
b69153[np.where(b69153 == '')] = np.nan

#flag de localizacao 'Loc_quality' (1, 2 e 3)
loc_69007 = b69007[:,8].astype('float')
loc_69009 = b69009[:,8].astype('float')
loc_69150 = b69150[:,8].astype('float')
loc_69151 = b69151[:,8].astype('float')
loc_69153 = b69153[:,8].astype('float')

#variaveis - sensores
s69007 = b69007[:,range(17,len(mnem))].astype('float')
s69009 = b69009[:,range(17,len(mnem))].astype('float')
s69150 = b69150[:,range(17,len(mnem))].astype('float')
s69151 = b69151[:,range(17,len(mnem))].astype('float')
s69153 = b69153[:,range(17,len(mnem))].astype('float')

#datas
d69007 = [datetime.strptime(i, '%Y/%m/%d %H:%M:%S') for i in b69007[:,14]]
d69009 = [datetime.strptime(i, '%Y/%m/%d %H:%M:%S') for i in b69009[:,14]]
d69150 = [datetime.strptime(i, '%Y/%m/%d %H:%M:%S') for i in b69150[:,14]]
d69151 = [datetime.strptime(i, '%Y/%m/%d %H:%M:%S') for i in b69151[:,14]]
d69153 = [datetime.strptime(i, '%Y/%m/%d %H:%M:%S') for i in b69153[:,14]]

#boia para plotagem
data = eval('d' + bb)
sens = eval('s' + bb)

hs = sens[:,20]
hmax = sens[:,21]
tp = sens[:,22]
dp = sens[:,23]

#numero de parametros a serem processados
npa = 4

#cria vetores de flags das series processadas (depende das qtdade de variaveis a serem consistidas + data) 
flagp = np.zeros((len(data),npa+1),dtype='|S32')
flagp[:,0] = data #listap[:]

# ================================================================================== #  
# Testes de consistencia dos dados processados

#Teste 1 - faixa
flagp[:,1] = consiste_proc.faixa(hs,t1a,t1b,t1c,t1d,flagp[:,1])
# flagp[:,2] = consiste_proc.faixa(hmax,0,35,0.5,20,flagp[:,2])
# flagp[:,3] = consiste_proc.faixa(tp,3,30,4,18,flagp[:,3])
# flagp[:,4] = consiste_proc.faixa(dp,0,360,0,360,flagp[:,4])

#Teste 2 - Variabilidade temporal		
flagp[:,1] = consiste_proc.variab(hs,t2a,t2b,flagp[:,1])
# flagp[:,2] = consiste_proc.variab(hmax,1,5,flagp[:,2])
# flagp[:,3] = consiste_proc.variab(tp,1,20,flagp[:,3])
# flagp[:,4] = consiste_proc.variab(dp,1,360,flagp[:,4])

#Teste 3 - Valores consecutivos iguais (*verificar num de arquivos em 'listac')
flagp[:,1] = consiste_proc.iguais(hs,t3a,flagp[:,1])
# flagp[:,2] = consiste_proc.iguais(hmax,15,flagp[:,2])
# flagp[:,3] = consiste_proc.iguais(tp,20,flagp[:,3])
# flagp[:,4] = consiste_proc.iguais(dp,20,flagp[:,4])


# ================================================================================== #  
# Coloca nan nos dados reprovados

#data em julianos
# matondap = np.array([pl.date2num(data),hs,hmax,tp,dp]).T
matondap = np.array([data,hs,hmax,tp,dp]).T

for c in range(1,flagp.shape[1]):

    for i in range(len(flagp)):

    #- 4 retira dados reprovados

        if '4' in flagp[i,c]:

            matondap[i,c] = np.nan	

    # - 3 retira dados suspeitos

        # elif '3' in flagp[i,c]:

        #     matondap[i,c] = np.nan


#cria variaveis consistentes
hs1, hmax1, tp1, dp1 = matondap[:,1:].T

#reprova todos os dados em que o hs foi reprovado
aux = np.where(np.isnan(list(hs1))==True)

dp1[aux] = np.nan
hmax1[aux] = np.nan
tp1[aux] = np.nan
dp1[aux] = np.nan

# -- fig1 (varias) -- #
# if bb == 1:

# 	for i in range(26):

# 		pl.figure()
# 		pl.plot(data,sens[:,i],'o')
# 		pl.title(mnem[i+17] + ' -- ' + mnem1[i])

# -- fig2 -- #

# pl.figure()

# pl.plot(data,hs,'ob',data,hmax,'or')
# pl.axis([data[0],data[-1],0,20])

# -- fig3 -- #
pl.figure()

pl.title('Hs - ' + bb)
pl.plot(data,hs,'ob',data,hs1,'or')
pl.legend(['bruto','cons'])
pl.xticks(rotation=20)
pl.ylabel('metros')

# -- fig4 -- #
pl.figure()

pl.title('Hmax - ' + bb)
pl.plot(data,hmax,'ob',data,hmax1,'or')
pl.legend(['bruto','cons'])
pl.xticks(rotation=20)
pl.ylabel('metros')

# -- fig5 -- #
pl.figure()

pl.title('Tp - ' + bb)
pl.plot(data,tp,'ob',data,tp1,'or')
pl.legend(['bruto','cons'])
pl.xticks(rotation=20)
pl.ylabel('segundos')

# -- fig6 -- #
pl.figure()

pl.title('Dp - ' + bb)
pl.plot(data,dp,'ob',data,dp1,'or')
pl.legend(['bruto','cons'])
pl.axis([data[0],data[-1],0,360])
pl.xticks(rotation=20)
pl.ylabel('graus')

pl.show()