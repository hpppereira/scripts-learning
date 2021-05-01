'''
Avaliacao dos resultados da previsao 

Plota as comparacoes e calcula os erros percentuais ate janeiro/16

'''

import matplotlib
import os
import numpy as np
import matplotlib.pylab as pl
import pandas as pd
from datetime import *
import xlrd
from scipy.signal import savgol_filter #Savitzky-Golay filter p/ suavizar serie
from pylab import FuncFormatter



########## DADOS AMBIDADOS

#pl.close('all')
# DADOS ADCP
pathname_adcp = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/operacional/' #dados
pathnamep = os.environ['HOME'] + '/Dropbox/Previsao/vale/resultados/'

prevs = np.sort(os.listdir(pathnamep))

#nome dos arquivos
#adcp - boia 4 e 10
adcp04 = 'TU_boia04.out' #fora do porto (mais fundo)
adcp10 = 'TU_boia10.out' #dentro do porto

#carrega dados
# 0      1      2     3         4        5    6   7   8 9
#data,bateria,rumo,pressao,temperatura,pitch,roll,hs,tp,dp
adcp04 = np.loadtxt(pathname_adcp + adcp04,delimiter=',')
adcp10 = np.loadtxt(pathname_adcp + adcp10,delimiter=',')


#dadcp10[6142]
#datetime.datetime(2015, 11, 27, 0, 0)
adcp10=adcp10[:,:]


# somei 3 horas para ficar UTC
dadcp04 = [ datetime.strptime(str(int(adcp04[i,0])), '%Y%m%d%H%M') for i in range(len(adcp04)) ]
dadcp04 = [ dadcp04[i] + timedelta(hours=3) for i in range(len(dadcp04))]
dadcp10 = [ datetime.strptime(str(int(adcp10[i,0])), '%Y%m%d%H%M') for i in range(len(adcp10)) ]
dadcp10 = [ dadcp10[i] + timedelta(hours=3) for i in range(len(dadcp10))]


model10=np.array([[0,0,0,0]]);mdd10_24=np.array([[0,0,0,0]]);mdd10_48=np.array([[0,0,0,0]]);mdd10_72=np.array([[0,0,0,0]])
mdd10_96=np.array([[0,0,0,0]]);mdd10_121=np.array([[0,0,0,0]]);mdd10_145=np.array([[0,0,0,0]]);mdd10_168=np.array([[0,0,0,0]])
mdd10_192=np.array([[0,0,0,0]]);mdd10_216=np.array([[0,0,0,0]]);mdd10_240=np.array([[0,0,0,0]])

model04=np.array([[0,0,0,0]]);mdd04_24=np.array([[0,0,0,0]]);mdd04_48=np.array([[0,0,0,0]]);mdd04_72=np.array([[0,0,0,0]])
mdd04_96=np.array([[0,0,0,0]]);mdd04_121=np.array([[0,0,0,0]]);mdd04_145=np.array([[0,0,0,0]]);mdd04_168=np.array([[0,0,0,0]])
mdd04_192=np.array([[0,0,0,0]]);mdd04_216=np.array([[0,0,0,0]]);mdd04_240=np.array([[0,0,0,0]])


# corrigir - estava com problemas no dropbox
for dto in prevs[0:-3]:

	model10= np.loadtxt(pathnamep + dto + '/table_point_ADCP10.out',skiprows=7,usecols=(0,1,3,2))
	mdd10_24=np.concatenate((mdd10_24,model10[0:25,:]),axis=0)
	mdd10_48=np.concatenate((mdd10_48,model10[25:49,:]),axis=0)
	mdd10_72=np.concatenate((mdd10_72,model10[49:73,:]),axis=0)
	mdd10_96=np.concatenate((mdd10_96,model10[73:97,:]),axis=0)
	mdd10_121=np.concatenate((mdd10_121,model10[97:122,:]),axis=0)
	mdd10_145=np.concatenate((mdd10_145,model10[122:146,:]),axis=0)
	mdd10_168=np.concatenate((mdd10_168,model10[146:169,:]),axis=0)
	mdd10_192=np.concatenate((mdd10_192,model10[169:193,:]),axis=0)
	mdd10_216=np.concatenate((mdd10_192,model10[193:217,:]),axis=0)
	mdd10_240=np.concatenate((mdd10_192,model10[217:240,:]),axis=0)
	

	model04= np.loadtxt(pathnamep + dto + '/table_point_ADCP01.out',skiprows=7,usecols=(0,1,3,2))
	mdd04_24=np.concatenate((mdd04_24,model04[0:25,:]),axis=0)
	mdd04_48=np.concatenate((mdd04_48,model04[25:49,:]),axis=0)
	mdd04_72=np.concatenate((mdd04_72,model04[49:73,:]),axis=0)
	mdd04_96=np.concatenate((mdd04_96,model04[73:97,:]),axis=0)
	mdd04_121=np.concatenate((mdd04_121,model04[97:122,:]),axis=0)
	mdd04_145=np.concatenate((mdd04_145,model04[122:146,:]),axis=0)
	mdd04_168=np.concatenate((mdd04_168,model04[146:169,:]),axis=0)
	mdd04_192=np.concatenate((mdd04_192,model04[169:193,:]),axis=0)
	mdd04_216=np.concatenate((mdd04_192,model04[193:217,:]),axis=0)
	mdd04_240=np.concatenate((mdd04_192,model04[217:240,:]),axis=0)



mdd10_24 = mdd10_24[1:,:];mdd04_24 = mdd04_24[1:,:];mdd10_48 = mdd10_48[1:,:];mdd04_48 = mdd04_48[1:,:]
mdd10_72 = mdd10_72[1:,:];mdd04_72 = mdd04_72[1:,:];mdd10_96 = mdd10_96[1:,:];mdd04_96 = mdd04_96[1:,:]
mdd10_121 = mdd10_121[1:,:];mdd04_121 = mdd04_121[1:,:];mdd10_145 = mdd10_145[1:,:];mdd04_145 = mdd04_145[1:,:]
mdd10_168 = mdd10_168[1:,:];mdd04_168 = mdd04_168[1:,:];mdd10_192 = mdd10_192[1:,:];mdd04_192 = mdd04_192[1:,:]
mdd10_216 = mdd10_216[1:,:];mdd04_216 = mdd04_216[1:,:];mdd10_240 = mdd10_240[1:,:];mdd04_240 = mdd04_240[1:,:]

# ===========================  ESTATISTICA PREVISAO ====================================

# escolher antecedencia
print ''
print '               24 Horas             '
print ''
mdd04=mdd04_24
mdd10=mdd10_24

# ======================================================================================
# pegar dado solicitado
data_mod=mdd10[:,0]*100
data_mod = data_mod.astype(str) #ano mes dia hora
datam = np.array([datetime(int(data_mod[i][0:4]),int(data_mod[i][4:6]),int(data_mod[i][6:8]),int(data_mod[i][8:10])) for i in range(len(data_mod))])


# pl.figure()
# pl.plot(dadcp10,adcp10[:,7],'ro')
# pl.plot(datam,mdd10[:,1],'k--',linewidth=2.5)
# pl.legend(['Boia10','Previsto'],loc=2)
# pl.xlim(datam[0],datam[-1])
# pl.ylim([0,3.5])
# pl.grid()
# pl.show()

# pl.figure()
# pl.plot(dadcp04,adcp04[:,7],'ro')
# pl.plot(datam,mdd04[:,1],'k--',linewidth=2.5)
# pl.legend(['Boia04','Previsto'],loc=2)
# pl.xlim(datam[0],datam[-1])
# pl.ylim([0,3.5])
# pl.grid()
# pl.show()

## Analise dos dados -----------
D04 = np.array([datetime.strftime(dadcp04[i],'%Y%m%d%H') for i in xrange(len(dadcp04))]).astype(int)

D10 = np.array([datetime.strftime(dadcp10[i],'%Y%m%d%H') for i in xrange(len(dadcp10))]).astype(int)

MOD = np.array([datetime.strftime(datam[i],'%Y%m%d%H') for i in xrange(len(datam))]).astype(int)

hs_mod04=np.array([[0]])
hs_04=np.array([[0]])
hs_mod10=np.array([[0]])
hs_10=np.array([[0]])
ddata04=np.array([[0]])
ddata10=np.array([[0]])

for j in range(len(MOD)):

	n=np.where(MOD[j]==D04)[0];
	if n.size:
		hsm=np.array([[mdd04[j,1]]])
		hs=np.array([[adcp04[n[0],7]]])
		data=np.array([[D04[n[0]]]])
		hs_mod04=np.concatenate((hs_mod04,hsm),axis=0)
		hs_04=np.concatenate((hs_04,hs),axis=0)
		ddata04=np.concatenate((ddata04,data),axis=0)

	n=np.where(MOD[j]==D10)[0];
	if n.size:
		hsm=np.array([[mdd10[j,1]]])
		hs=np.array([[adcp10[n[0],7]]])
		data=np.array([[D10[n[0]]]])
		hs_mod10=np.concatenate((hs_mod10,hsm),axis=0)
		hs_10=np.concatenate((hs_10,hs),axis=0)
		ddata10=np.concatenate((ddata10,data),axis=0)



hs_mod04=hs_mod04[1:];hs_04=hs_04[1:]
hs_mod10=hs_mod10[1:];hs_10=hs_10[1:]
ddata04=ddata04[1:];ddata04=[ datetime.strptime(str(int(ddata04[i])), '%Y%m%d%H') for i in range(len(ddata04)) ]
ddata10=ddata10[1:];ddata10=[ datetime.strptime(str(int(ddata10[i])), '%Y%m%d%H') for i in range(len(ddata10)) ]


# retirar valores espurios
hs_04[np.where(hs_04>=4)] = np.nan; hs_04[np.where(hs_04<=0.5)] = np.nan
hs_10[np.where(hs_10>=4)] = np.nan; hs_10[np.where(hs_10<=0.5)] = np.nan

#retira os dados com nan de cada variavel
indhs = np.where(np.isnan(hs_04) == False)[0];hs_mod04 = hs_mod04[indhs];hs_04 = hs_04[indhs];ddata04=[ddata04[indhs[i]] for i in range(len(indhs))]
indhs10 = np.where(np.isnan(hs_10) == False)[0];hs_mod10 = hs_mod10[indhs10];hs_10 = hs_10[indhs10];ddata10=[ddata10[indhs10[i]] for i in range(len(indhs10))]

# filtro
hs_04s=hs_04;hs_10s=hs_10
# com filtro ou sem filtro (so comentar)
hs_04 = savgol_filter(hs_04[:,0], 11, 3) # window size 73, polynomial order 2
hs_10 = savgol_filter(hs_10[:,0], 11, 3)

z2=np.ones(len(dadcp10))*-10
z3=np.ones(len(dadcp10))*-5
z4=np.ones(len(dadcp10))*5
z5=np.ones(len(dadcp10))*10


pl.figure()
pl.subplot(211)
pl.plot(ddata04,hs_04,'k-',linewidth=2.5)
pl.plot(ddata04,hs_04s,'ro')
pl.plot(ddata04,hs_mod04,'b--',linewidth=2.5)
pl.legend(['Boia04 (Filtrado)','Boia04 (Bruto)','Boia04 (Previsto)'],loc=2)
pl.ylim([0,3])
pl.grid()
pl.subplot(212)
pl.plot(dadcp04,adcp04[:,5],'g.')
pl.plot(dadcp04,adcp04[:,6],'y.')
pl.plot(dadcp10,z2,'g--', linewidth=2)
pl.plot(dadcp10,z3,'g--', linewidth=0.5)
pl.plot(dadcp10,z4,'g--', linewidth=0.5)
pl.plot(dadcp10,z5,'g--', linewidth=2)
pl.ylabel('Deslocamentos Boia04 (graus)',color='g')
pl.legend(['pitch','roll'],loc=4)
pl.yticks(np.arange(-15,25,5),color='g')
pl.ylim([-20,20])
pl.xlim([ddata04[0],ddata04[-1]])
pl.grid()
pl.show()

pl.figure()
pl.subplot(211)
pl.plot(ddata10,hs_10,'k-',linewidth=1.5)
pl.plot(ddata10,hs_10s,'ro')
pl.plot(ddata10,hs_mod10,'b--',linewidth=2.5)
pl.legend(['Boia10 (Filtrado)','Boia10 (Bruto)','Boia10 (Previsto)'],loc=2)
pl.ylim([0,2.5])
pl.grid()
pl.subplot(212)
pl.plot(dadcp10,adcp10[:,5],'g.')
pl.plot(dadcp10,adcp10[:,6],'y.')
pl.plot(dadcp10,z2,'g--', linewidth=2)
pl.plot(dadcp10,z3,'g--', linewidth=0.5)
pl.plot(dadcp10,z4,'g--', linewidth=0.5)
pl.plot(dadcp10,z5,'g--', linewidth=2)
pl.ylabel('Deslocamentos Boia10 (graus)',color='g')
pl.legend(['pitch','roll'],loc=4)
pl.yticks(np.arange(-15,25,5),color='g')
pl.ylim([-20,20])
pl.xlim([ddata10[0],ddata10[-1]])
pl.grid()
pl.show()

### RMSE ###
print '------------ ADCP04 --------------'
print 'RMSE'
rmse_hs = np.sqrt( pl.sum( (hs_mod04 - hs_04) ** 2 ) / len(hs_04) )
print rmse_hs

### SI ###
print 'SI'
si_hs = rmse_hs / np.mean(hs_04)
print si_hs


print 'RSE 90%'
rse=np.abs([hs_mod04[i,0]-hs_04[i] for i in range(len(hs_mod04))])
print np.percentile(rse,90)

print '------------ ADCP10 --------------'
### RMSE ###
print 'RMSE'
rmse_hs = np.sqrt( pl.sum( (hs_mod10 - hs_10) ** 2 ) / len(hs_10) )
print rmse_hs

### SI ###
print 'SI'
si_hs = rmse_hs / np.mean(hs_10)
print si_hs

print 'RSE 90%'
rse10=np.abs([hs_mod10[i,0]-hs_10[i] for i in range(len(hs_mod10))])
print np.percentile(rse10,90)
