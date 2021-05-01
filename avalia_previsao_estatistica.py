'''

RT07 - VALE
Avaliacao dos resultados da previsao para aguas rasas 
Plota as comparacoes e calcula os erros percentuais 


- Analisar pitch e roll dos ADCP's / tira dados espurios
- Filtrar dados
- scatter plot
- Analisar o erro associado a cada percentil de hs
- ver com quais variaveis o erro esta mais associado
- ver qual a distribuicao que melhor ajusta aos dados
- para o ADCP10: analisar o erro de 1,5 m (0,8 - 1,70m)
- analisar erro por tempo de previsao

'''

import matplotlib
import os
import numpy as np
import matplotlib.pylab as pl
import pandas as pd
from datetime import *
from scipy.signal import savgol_filter #Savitzky-Golay filter p/ suavizar serie
from scipy.stats import gaussian_kde
from matplotlib.ticker import FuncFormatter

pl.close('all')
home=os.environ['HOME']
# DADOS ADCP (coletados pela AMBIDADOS)
pathname_adcp = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/operacional/' #dados
pathnamep = os.environ['HOME'] + '/Dropbox/Previsao/vale/resultados/'

prevs = np.sort(os.listdir(pathnamep))

#adcp - boia 4 e 10
adcp04 = 'TU_boia0401.out' #fora do porto (mais fundo)
adcp10 = 'TU_boia1001.out' #dentro do porto

#carrega dados
# 0      1      2     3         4        5    6   7   8 9
#data,bateria,rumo,pressao,temperatura,pitch,roll,hs,tp,dp
adcp04 = np.loadtxt(pathname_adcp + adcp04,delimiter=',')
adcp10 = np.loadtxt(pathname_adcp + adcp10,delimiter=',')

# somei 3 horas para ficar UTC
dadcp04 = [ datetime.strptime(str(int(adcp04[i,0])), '%Y%m%d%H%M') for i in range(len(adcp04)) ]
dadcp04 = [ dadcp04[i] + timedelta(hours=3) for i in range(len(dadcp04))]
dadcp10 = [ datetime.strptime(str(int(adcp10[i,0])), '%Y%m%d%H%M') for i in range(len(adcp10)) ]
dadcp10 = [ dadcp10[i] + timedelta(hours=3) for i in range(len(dadcp10))]

# ---------------------------------------------------
#                  DADOS - CQ
# ---------------------------------------------------
# analisar informacoes de pitch e roll e descartar dados com inclinacao acima de 10 graus
# # Plot bruto
# z2=np.ones(len(dadcp10))*-10;z5=np.ones(len(dadcp10))*10

# pl.figure(figsize=(12,14))
# pl.subplot(411)
# pl.plot(dadcp10,adcp10[:,7],'ro',markersize=5)
# pl.legend(['Hs (m)'],loc=2);pl.ylabel("Hs (m)",color='k')
# pl.ylim([-0.1,3.5]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp10[-1])
# pl.subplot(412)
# pl.plot(dadcp10,adcp10[:,8],'ro',markersize=5)
# pl.legend(['Tp (s)'],loc=2);pl.ylabel("Tp (s)",color='k')
# pl.ylim([-0.5,22]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp10[-1])
# pl.subplot(413)
# pl.plot(dadcp10,adcp10[:,9],'ro',markersize=5)
# pl.legend(['Dp (graus)'],loc=2);pl.ylabel("Dp (graus)",color='k')
# pl.ylim([-0.5,360]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp10[-1])
# pl.subplot(414)
# pl.plot(dadcp10,adcp10[:,5],'g.');pl.plot(dadcp10,adcp10[:,6],'y.')
# pl.plot(dadcp10,z2,'k--', linewidth=2);pl.plot(dadcp10,z5,'k--', linewidth=2)
# pl.ylabel('Inclinacao (graus)',color='k')
# pl.legend(['pitch (graus)','roll (graus)'],loc=3,ncol=2)
# pl.yticks(np.arange(-20,30,10),color='k')
# pl.ylim([-30,25]);pl.xlim(datetime(2015,9,1,1,0),dadcp10[-1])
# pl.grid()

# z2=np.ones(len(dadcp04))*-10;z5=np.ones(len(dadcp04))*10

# pl.figure(figsize=(12,14))
# pl.subplot(411)
# pl.plot(dadcp04,adcp04[:,7],'ro',markersize=5)
# pl.legend(['Hs (m)'],loc=2);pl.ylabel("Hs (m)",color='k')
# pl.ylim([-0.1,3.5]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp04[-1])
# pl.subplot(412)
# pl.plot(dadcp04,adcp04[:,8],'ro',markersize=5)
# pl.legend(['Tp (s)'],loc=2);pl.ylabel("Tp (s)",color='k')
# pl.ylim([-0.5,22]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp04[-1])
# pl.subplot(413)
# pl.plot(dadcp04,adcp04[:,9],'ro',markersize=5)
# pl.legend(['Dp (graus)'],loc=2);pl.ylabel("Dp (graus)",color='k')
# pl.ylim([-0.5,360]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp04[-1])
# pl.subplot(414)
# pl.plot(dadcp04,adcp04[:,5],'g.')
# pl.plot(dadcp04,adcp04[:,6],'y.')
# pl.plot(dadcp04,z2,'k--', linewidth=2);pl.plot(dadcp04,z5,'k--', linewidth=2)
# pl.ylabel('Inclinacao (graus)',color='k')
# pl.legend(['pitch (graus)','roll (graus)'],loc=3,ncol=2)
# pl.yticks(np.arange(-20,30,10),color='k')
# pl.ylim([-30,25]);pl.xlim(datetime(2015,9,1,1,0),dadcp04[-1])
# pl.grid()
# pl.show()

# tira inclinacao acima do recomendado
# segundo manual o recomentado e entre -10 e 10

adcp10[np.where(np.logical_or(adcp10[:,5]<-10,adcp10[:,5]>10)),:] = np.nan;
adcp10[np.where(np.logical_or(adcp10[:,6]<-10,adcp10[:,6]>10)),:] = np.nan;

adcp04[np.where(np.logical_or(adcp04[:,5]<-10,adcp04[:,5]>10)),:] = np.nan;
adcp04[np.where(np.logical_or(adcp04[:,6]<-10,adcp04[:,6]>10)),:] = np.nan;

# tira valores de Hs e Dp espurios
adcp10[np.where(np.logical_or(adcp10[:,9]>270,adcp10[:,7]<0.25)),:] = np.nan;
adcp10[np.where(np.logical_or(adcp10[:,9]<5,adcp10[:,7]<0.25)),:] = np.nan;
adcp04[np.where(np.logical_or(adcp04[:,9]>270,adcp04[:,7]<0.5)),:] = np.nan;
adcp04[np.where(np.logical_or(adcp04[:,9]<5,adcp04[:,7]<0.5)),:] = np.nan;

# valores de hs acima do normal
adcp04[np.where(adcp04[:,7]>3),:] = np.nan;

# tira valores consecutivos iguais = isso pode me dar problema na hora da estatistica
# adcp10[np.where(np.diff(adcp10[:,7])==0),:] = np.nan;
# adcp04[np.where(np.diff(adcp04[:,7])==0),:] = np.nan;


# z2=np.ones(len(dadcp10))*-10;z5=np.ones(len(dadcp10))*10

# pl.figure(figsize=(12,14))
# pl.subplot(411)
# pl.plot(dadcp10,adcp10[:,7],'ro',markersize=5)
# pl.legend(['Hs (m)'],loc=2);pl.ylabel("Hs (m)",color='k')
# pl.ylim([-0.1,3.5]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp10[-1])
# pl.subplot(412)
# pl.plot(dadcp10,adcp10[:,8],'ro',markersize=5)
# pl.legend(['Tp (s)'],loc=2);pl.ylabel("Tp (s)",color='k')
# pl.ylim([-0.5,22]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp10[-1])
# pl.subplot(413)
# pl.plot(dadcp10,adcp10[:,9],'ro',markersize=5)
# pl.legend(['Dp (graus)'],loc=2);pl.ylabel("Dp (graus)",color='k')
# pl.ylim([-0.5,360]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp10[-1])
# pl.subplot(414)
# pl.plot(dadcp10,adcp10[:,5],'g.');pl.plot(dadcp10,adcp10[:,6],'y.')
# pl.plot(dadcp10,z2,'k--', linewidth=2);pl.plot(dadcp10,z5,'k--', linewidth=2)
# pl.ylabel('Inclinacao (graus)',color='k')
# pl.legend(['pitch (graus)','roll (graus)'],loc=3,ncol=2)
# pl.yticks(np.arange(-20,30,10),color='k')
# pl.ylim([-30,25]);pl.xlim(datetime(2015,9,1,1,0),dadcp10[-1])
# pl.grid()

# z2=np.ones(len(dadcp04))*-10;z5=np.ones(len(dadcp04))*10

# pl.figure(figsize=(12,14))
# pl.subplot(411)
# pl.plot(dadcp04,adcp04[:,7],'ro',markersize=5)
# pl.legend(['Hs (m)'],loc=2);pl.ylabel("Hs (m)",color='k')
# pl.ylim([-0.1,3.5]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp04[-1])
# pl.subplot(412)
# pl.plot(dadcp04,adcp04[:,8],'ro',markersize=5)
# pl.legend(['Tp (s)'],loc=2);pl.ylabel("Tp (s)",color='k')
# pl.ylim([-0.5,22]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp04[-1])
# pl.subplot(413)
# pl.plot(dadcp04,adcp04[:,9],'ro',markersize=5)
# pl.legend(['Dp (graus)'],loc=2);pl.ylabel("Dp (graus)",color='k')
# pl.ylim([-0.5,360]);pl.grid();pl.xlim(datetime(2015,9,1,1,0),dadcp04[-1])
# pl.subplot(414)
# pl.plot(dadcp04,adcp04[:,5],'g.')
# pl.plot(dadcp04,adcp04[:,6],'y.')
# pl.plot(dadcp04,z2,'k--', linewidth=2);pl.plot(dadcp04,z5,'k--', linewidth=2)
# pl.ylabel('Inclinacao (graus)',color='k')
# pl.legend(['pitch (graus)','roll (graus)'],loc=3,ncol=2)
# pl.yticks(np.arange(-20,30,10),color='k')
# pl.ylim([-30,25]);pl.xlim(datetime(2015,9,1,1,0),dadcp04[-1])
# pl.grid()
# pl.show()

#retira os dados com nan de cada variavel
ind = np.where(np.isnan(adcp10[:,7]) == False)[0];
adcp10=adcp10[ind,:]
dadcp10=[dadcp10[ind[i]] for i in range(len(ind))]

ind = np.where(np.isnan(adcp04[:,7]) == False)[0];
adcp04=adcp04[ind,:]
dadcp04=[dadcp04[ind[i]] for i in range(len(ind))]

# ----------------------------------------------------
#                     PREVISAO  - WW3
# ----------------------------------------------------
model10=np.array([[0,0,0,0]]);mdd10_24=np.array([[0,0,0,0]]);mdd10_48=np.array([[0,0,0,0]]);mdd10_72=np.array([[0,0,0,0]])
mdd10_96=np.array([[0,0,0,0]]);mdd10_121=np.array([[0,0,0,0]]);mdd10_145=np.array([[0,0,0,0]]);mdd10_168=np.array([[0,0,0,0]])
mdd10_192=np.array([[0,0,0,0]]);mdd10_216=np.array([[0,0,0,0]]);mdd10_240=np.array([[0,0,0,0]])

model04=np.array([[0,0,0,0]]);mdd04_24=np.array([[0,0,0,0]]);mdd04_48=np.array([[0,0,0,0]]);mdd04_72=np.array([[0,0,0,0]])
mdd04_96=np.array([[0,0,0,0]]);mdd04_121=np.array([[0,0,0,0]]);mdd04_145=np.array([[0,0,0,0]]);mdd04_168=np.array([[0,0,0,0]])
mdd04_192=np.array([[0,0,0,0]]);mdd04_216=np.array([[0,0,0,0]]);mdd04_240=np.array([[0,0,0,0]])


for dto in prevs[0:-12]:

	model10= np.loadtxt(pathnamep + dto + '/table_point_ADCP10.out',skiprows=7,usecols=(0,1,3,2))
	mdd10_24=np.concatenate((mdd10_24,model10[0:25,:]),axis=0);	mdd10_48=np.concatenate((mdd10_48,model10[25:49,:]),axis=0)
	mdd10_72=np.concatenate((mdd10_72,model10[49:73,:]),axis=0);mdd10_96=np.concatenate((mdd10_96,model10[73:97,:]),axis=0)
	mdd10_121=np.concatenate((mdd10_121,model10[97:122,:]),axis=0);mdd10_145=np.concatenate((mdd10_145,model10[122:146,:]),axis=0)
	mdd10_168=np.concatenate((mdd10_168,model10[146:169,:]),axis=0);mdd10_192=np.concatenate((mdd10_192,model10[169:193,:]),axis=0)
	mdd10_216=np.concatenate((mdd10_216,model10[193:217,:]),axis=0);mdd10_240=np.concatenate((mdd10_240,model10[217:240,:]),axis=0)
	

	model04= np.loadtxt(pathnamep + dto + '/table_point_ADCP01.out',skiprows=7,usecols=(0,1,3,2))
	mdd04_24=np.concatenate((mdd04_24,model04[0:25,:]),axis=0);mdd04_48=np.concatenate((mdd04_48,model04[25:49,:]),axis=0)
	mdd04_72=np.concatenate((mdd04_72,model04[49:73,:]),axis=0);mdd04_96=np.concatenate((mdd04_96,model04[73:97,:]),axis=0)
	mdd04_121=np.concatenate((mdd04_121,model04[97:122,:]),axis=0);mdd04_145=np.concatenate((mdd04_145,model04[122:146,:]),axis=0)
	mdd04_168=np.concatenate((mdd04_168,model04[146:169,:]),axis=0);mdd04_192=np.concatenate((mdd04_192,model04[169:193,:]),axis=0)
	mdd04_216=np.concatenate((mdd04_216,model04[193:217,:]),axis=0);mdd04_240=np.concatenate((mdd04_240,model04[217:240,:]),axis=0)



mdd10_24 = mdd10_24[1:,:];mdd04_24 = mdd04_24[1:,:];mdd10_48 = mdd10_48[1:,:];mdd04_48 = mdd04_48[1:,:]
mdd10_72 = mdd10_72[1:,:];mdd04_72 = mdd04_72[1:,:];mdd10_96 = mdd10_96[1:,:];mdd04_96 = mdd04_96[1:,:]
mdd10_121 = mdd10_121[1:,:];mdd04_121 = mdd04_121[1:,:];mdd10_145 = mdd10_145[1:,:];mdd04_145 = mdd04_145[1:,:]
mdd10_168 = mdd10_168[1:,:];mdd04_168 = mdd04_168[1:,:];mdd10_192 = mdd10_192[1:,:];mdd04_192 = mdd04_192[1:,:]
mdd10_216 = mdd10_216[1:,:];mdd04_216 = mdd04_216[1:,:];mdd10_240 = mdd10_240[1:,:];mdd04_240 = mdd04_240[1:,:]

# comparar diferentes tempos da previsao
# # pegar 24h
# data_mod24=mdd10_24[:,0]*100;data_mod24 = data_mod24.astype(str) #ano mes dia hora
# datam24 = np.array([datetime(int(data_mod24[i][0:4]),int(data_mod24[i][4:6]),int(data_mod24[i][6:8]),int(data_mod24[i][8:10])) for i in range(len(data_mod24))])
# # pegar 48h
# data_mod48=mdd10_48[:,0]*100;data_mod48 = data_mod48.astype(str) #ano mes dia hora
# datam48 = np.array([datetime(int(data_mod48[i][0:4]),int(data_mod48[i][4:6]),int(data_mod48[i][6:8]),int(data_mod48[i][8:10])) for i in range(len(data_mod48))])
# # pegar 168h
# data_mod168=mdd10_168[:,0]*100;data_mod168 = data_mod168.astype(str) #ano mes dia hora
# datam168 = np.array([datetime(int(data_mod168[i][0:4]),int(data_mod168[i][4:6]),int(data_mod168[i][6:8]),int(data_mod168[i][8:10])) for i in range(len(data_mod168))])


# ===========================  ESTATISTICA PREVISAO ====================================

# escolher antecedencia
print ''
print '               Previsao            '
print ''
mdd04=mdd04_24 # mudar
mdd10=mdd10_24 # mudar
name='24' # mudar
print '          Analisando',name,'horas   '
# ======================================================================================
# pegar dado solicitado
data_mod=mdd10[:,0]*100;data_mod = data_mod.astype(str) #ano mes dia hora
datam = np.array([datetime(int(data_mod[i][0:4]),int(data_mod[i][4:6]),int(data_mod[i][6:8]),int(data_mod[i][8:10])) for i in range(len(data_mod))])

## Analise dos dados -----------
D04 = np.array([datetime.strftime(dadcp04[i],'%Y%m%d%H') for i in xrange(len(dadcp04))]).astype(int)

D10 = np.array([datetime.strftime(dadcp10[i],'%Y%m%d%H') for i in xrange(len(dadcp10))]).astype(int)

MOD = np.array([datetime.strftime(datam[i],'%Y%m%d%H') for i in xrange(len(datam))]).astype(int)

hs_mod04=np.array([[0]]);hs_04=np.array([[0]]);tp_mod04=np.array([[0]]);tp_04=np.array([[0]])
dp_mod04=np.array([[0]]);dp_04=np.array([[0]]);hs_mod10=np.array([[0]]);hs_10=np.array([[0]])
tp_mod10=np.array([[0]]);tp_10=np.array([[0]]);dp_mod10=np.array([[0]]);dp_10=np.array([[0]])
ddata04=np.array([[0]]);ddata10=np.array([[0]])


# # tirando os valores medidos em minutos quebrados
# aux,index=np.unique(D10,return_index=True)
# adcp10u=adcp10[index,:]
# dadcp10u=[dadcp10[index[i]] for i in xrange(len(index))]

# aux,index=np.unique(D04,return_index=True)
# adcp04u=adcp04[index,:]
# dadcp04u=[dadcp04[index[i]] for i in xrange(len(index))]

for j in range(len(MOD)):

	n=np.where(MOD[j]==D04)[0];
	if n.size:
		hsm=np.array([[mdd04[j,1]]])
		# verificar dado no range de 1 hora mais proximo
		indx=np.argmin(np.absolute(adcp04[n,7]-hsm));hs=np.array([[adcp04[n[indx],7]]])
		data=np.array([[D04[n[indx]]]]);hs_mod04=np.concatenate((hs_mod04,hsm),axis=0)
		hs_04=np.concatenate((hs_04,hs),axis=0)

		tpm=np.array([[mdd04[j,2]]]);tp=np.array([[adcp04[n[indx],8]]])
		tp_mod04=np.concatenate((tp_mod04,tpm),axis=0);tp_04=np.concatenate((tp_04,tp),axis=0)

		dpm=np.array([[mdd04[j,3]]]);dp=np.array([[adcp04[n[indx],9]]])
		dp_mod04=np.concatenate((dp_mod04,dpm),axis=0);dp_04=np.concatenate((dp_04,dp),axis=0)

		ddata04=np.concatenate((ddata04,data),axis=0)

	n=np.where(MOD[j]==D10)[0];
	if n.size:
		hsm=np.array([[mdd10[j,1]]])
		# verificar dado no range de 1 hora mais proximo
		indx=np.argmin(np.absolute(adcp10[n,7]-hsm));hs=np.array([[adcp10[n[indx],7]]])
		data=np.array([[D10[n[indx]]]]);hs_mod10=np.concatenate((hs_mod10,hsm),axis=0)
		hs_10=np.concatenate((hs_10,hs),axis=0)

		tpm=np.array([[mdd10[j,2]]]);tp=np.array([[adcp10[n[indx],8]]])
		tp_mod10=np.concatenate((tp_mod10,tpm),axis=0);tp_10=np.concatenate((tp_10,tp),axis=0)

		dpm=np.array([[mdd10[j,3]]]);dp=np.array([[adcp10[n[indx],9]]])
		dp_mod10=np.concatenate((dp_mod10,dpm),axis=0);dp_10=np.concatenate((dp_10,dp),axis=0)

		ddata10=np.concatenate((ddata10,data),axis=0)



hs_mod04=hs_mod04[1:];hs_04=hs_04[1:];tp_mod04=tp_mod04[1:];tp_04=tp_04[1:]
dp_mod04=dp_mod04[1:];dp_04=dp_04[1:];hs_mod10=hs_mod10[1:];hs_10=hs_10[1:]
tp_mod10=tp_mod10[1:];tp_10=tp_10[1:];dp_mod10=dp_mod10[1:];dp_10=dp_10[1:]
ddata04=ddata04[1:];ddata04=[ datetime.strptime(str(int(ddata04[i])), '%Y%m%d%H') for i in range(len(ddata04)) ]
ddata10=ddata10[1:];ddata10=[ datetime.strptime(str(int(ddata10[i])), '%Y%m%d%H') for i in range(len(ddata10)) ]


# valores espuridos nos resultados do modelo
# tira valores de Hs e Dp espurios
dp_mod04[np.where(np.logical_or(dp_mod04>270,dp_mod04<50)),:] = np.nan
dp_mod10[np.where(np.logical_or(np.diff(dp_mod10[:,0])<-20,np.diff(dp_mod10[:,0])>20))] = np.nan
dp_mod10[np.where(np.logical_or(np.diff(dp_mod10[:,0])<-20,np.diff(dp_mod10[:,0])>20))] = np.nan

# corrigindo declinacao magnetica do periodo de 2015
dp_10[0:717]=dp_10[0:717]-23.5

#retira os dados com nan de cada variavel
indhs = np.where(np.isnan(hs_04) == False)[0];hs_mod04 = hs_mod04[indhs];hs_04 = hs_04[indhs];ddata04=[ddata04[indhs[i]] for i in range(len(indhs))]
indhs10 = np.where(np.isnan(hs_10) == False)[0];hs_mod10 = hs_mod10[indhs10];hs_10 = hs_10[indhs10];ddata10=[ddata10[indhs10[i]] for i in range(len(indhs10))]
#inddp10 = np.where(np.isnan(dp_mod10) == False)[0];dp_mod10 = dp_mod10[inddp10];dp_10 = dp_10[inddp10];ddata10=[ddata10[inddp10[i]] for i in range(len(inddp10))]
#inddp04 = np.where(np.isnan(dp_mod04) == False)[0];dp_mod04 = dp_mod04[inddp04];dp_04 = dp_04[inddp04];ddata04=[ddata04[inddp04[i]] for i in range(len(inddp04))]

# filtro Savgol (nao vou aplicar filtro)
# hs_04s=hs_04;hs_10s=hs_10
# com filtro ou sem filtro (so comentar)
#hs_04 = savgol_filter(hs_04[:,0], 37, 2) # window size 73, polynomial order 2
#hs_mod04 = savgol_filter(hs_mod04[:,0], 37, 2) 
# hs_10 = savgol_filter(hs_10[:,0], 11, 3)

print '             Verificacao         '
print ''
print ' Maximo valor medido ADCP04 ',str(np.max(hs_04)),'m',str(np.max(tp_04)),'s'
print ' Minimo valor medido ADCP04 ',str(np.min(hs_04)),'m',str(np.min(tp_04)),'s'
print ''
print ' Maximo valor medido ADCP10 ',str(np.max(hs_10)),'m',str(np.max(tp_10)),'s'
print ' Minimo valor medido ADCP10 ',str(np.min(hs_10)),'m',str(np.min(tp_10)),'s'

spc=5

pl.figure(figsize=(10,8))
pl.subplot(311)
pl.plot(ddata04[0:-1:spc],hs_04[0:-1:5],'ro',linewidth=2.5)
pl.plot(ddata04[0:-1:spc],hs_mod04[0:-1:5],'bo',linewidth=1.5)
pl.legend(['Medido','Previsto ('+str(name)+' horas)'],loc=2,ncol=2)
pl.ylim([0,3.5]);pl.ylabel('Hs (m)');pl.grid()
pl.subplot(312)
pl.plot(ddata04[0:-1:spc],tp_04[0:-1:5],'ro',linewidth=2.5)
pl.plot(ddata04[0:-1:spc],tp_mod04[0:-1:5],'bo',linewidth=1.5)
pl.legend(['Medido','Previsto ('+str(name)+' horas)'],loc=2,ncol=2)
pl.ylim([0,20]);pl.ylabel('Tp (s)');pl.grid()
pl.subplot(313)
pl.plot(ddata04[0:-1:spc],dp_04[0:-1:5],'ro',linewidth=2.5)
pl.plot(ddata04[0:-1:spc],dp_mod04[0:-1:5],'bo',linewidth=1.5)
pl.legend(['Medido','Previsto ('+str(name)+' horas)'],loc=2,ncol=2)
pl.ylim([0,360]);pl.ylabel('Dp (graus');pl.grid()
pl.savefig(home + '/Dropbox/ww3vale/TU/doc/RT/RT07/fig/series/'+'compara_boia04_'+name+'.png', dpi=None, facecolor='w', edgecolor='w',papertype=None, format='png')


pl.figure(figsize=(10,8))
pl.subplot(311)
pl.plot(ddata10[0:-1:spc],hs_10[0:-1:spc],'ro',linewidth=2.5)
pl.plot(ddata10[0:-1:spc],hs_mod10[0:-1:spc],'bo',linewidth=1.5)
pl.legend(['Medido','Previsto ('+str(name)+' horas)'],loc=2,ncol=2)
pl.ylim([0,2.5]);pl.ylabel('Hs (m)');pl.grid()
pl.subplot(312)
pl.plot(ddata10[0:-1:spc],tp_10[0:-1:spc],'ro',linewidth=2.5)
pl.plot(ddata10[0:-1:spc],tp_mod10[0:-1:spc],'bo',linewidth=1.5)
pl.legend(['Medido','Previsto ('+str(name)+' horas)'],loc=2,ncol=2)
pl.ylim([0,20]);pl.ylabel('Tp (s)');pl.grid()
pl.subplot(313)
pl.plot(ddata10[0:-1:spc],dp_10[0:-1:spc],'ro',linewidth=2.5)
pl.plot(ddata10[0:-1:spc],dp_mod10[0:-1:spc],'bo',linewidth=1.5)
pl.legend(['Medido','Previsto ('+str(name)+' horas)'],loc=2,ncol=2)
pl.ylim([0,360]);pl.ylabel('Dp (graus');pl.grid()
pl.savefig(home + '/Dropbox/ww3vale/TU/doc/RT/RT07/fig/series/'+'compara_boia10_'+name+'.png', dpi=None, facecolor='w', edgecolor='w',papertype=None, format='png')


# juntando variaveis para colocar junto
datamod0424=ddata04;hs0424=hs_04 # dado
datamod1024=ddata10;hs1024=hs_10 # dado

hsmod0424=hs_mod04;datamod0424=ddata04;
hsmod1024=hs_mod10;datamod1024=ddata10;

spc=5
pl.figure(figsize=(8,6))
pl.plot(datamod0424[0:-1:spc],hs0424[0:-1:spc],'ro',linewidth=2.5)
pl.plot(datamod0424[0:-1:spc],hsmod0424[0:-1:spc],'bo',linewidth=1.5)
pl.plot(datamod0472[0:-1:spc],hsmod0472[0:-1:spc],'k-',linewidth=1.5)
pl.plot(datamod04168[0:-1:spc],hsmod04168[0:-1:spc],'g--',linewidth=1.5)
pl.legend(['Medido','Previsto +24h','Previsto +72h','Previsto +168h'],loc=2,ncol=2)
pl.ylim([0,3.5]);pl.ylabel('Hs (m)');pl.grid();pl.xlim(datetime(2015,12,22,00,0),datetime(2016,01,15,8,0))

stop
# --------------- polyfit scatter  - hs --------------------
pl.figure(figsize=(13,6))
pl.subplot(121)
zpoly=np.polyfit(hs_04[:,0],hs_mod04[:,0],1)
# calculando o histograma de densidade
xy = np.vstack([hs_04[:,0],hs_mod04[:,0]]);z = gaussian_kde(xy)(xy)
pl.scatter(hs_04, hs_mod04, c=z, s=30, vmax=6,vmin=0,edgecolor='')
pl.colorbar();pl.ylim([0,2.5]);pl.xlim([0,2.5])
pl.ylabel('Hs (m) Previsto',fontsize=12);pl.xlabel('Hs (m) Medido',fontsize=12)
pl.plot(np.arange(0,3.5,0.1),np.arange(0,3.5,0.1),'k-')
pl.plot(np.arange(0,3.5,0.1),np.arange(0,3.5,0.1)*zpoly[0]+zpoly[1],'k--',linewidth=2.0);pl.grid();
corr_hs = np.corrcoef(hs_mod04[:,0],hs_04[:,0])[0,1] # correlacao
rmse_hs = np.sqrt( pl.sum( (hs_mod04 - hs_04) ** 2 ) / len(hs_04) ) # rmse
si_hs = (rmse_hs / np.mean(hs_04))  #si
bias_hs = np.mean(hs_mod04 - hs_04) # bias
rse04=np.abs([hs_mod04[i,0]-hs_04[i] for i in range(len(hs_mod04))])
me90=np.percentile(rse04,90) # erro 90
N = len(hs_04[:,0])
textstr = '$\mathrm{RMSE}=%.2fm$\n$\mathrm{SI}=%.2f$\n$\mathrm{Bias}=%.2fm$\n$\mathrm{N}=%.0f$'%(rmse_hs, si_hs,bias_hs,N)
#textstr = '$\mathrm{corr}=%.2f$\n$\mathrm{RMSE}=%.2fm$\n$\mathrm{ME90}=%.2fm$\n$\mathrm{SI}=%.2f$\n$\mathrm{Bias}=%.2fm$\n$\mathrm{N}=%.0f$'%(corr_hs, rmse_hs,me90, si_hs,bias_hs,N)
props = dict(boxstyle='round', facecolor='darkgray', alpha=0.5)
pl.text(0.05, 2.4, textstr, fontsize=13,verticalalignment='top', bbox=props)
# ADCP10
pl.subplot(122)
zpoly=np.polyfit(hs_10[:,0],hs_mod10[:,0],1)
# calculando o histograma de densidade
xy = np.vstack([hs_10[:,0],hs_mod10[:,0]]);z = gaussian_kde(xy)(xy)
pl.scatter(hs_10, hs_mod10, c=z, s=30, vmax=10,vmin=0,edgecolor='')
pl.colorbar();pl.ylim([0,2.5]);pl.xlim([0,2.5])
pl.ylabel('Hs (m) Previsto',fontsize=12);pl.xlabel('Hs (m) Medido',fontsize=12)
pl.plot(np.arange(0,3.5,0.1),np.arange(0,3.5,0.1),'k-')
pl.plot(np.arange(0,3.5,0.1),np.arange(0,3.5,0.1)*zpoly[0]+zpoly[1],'k--',linewidth=2.0);pl.grid();
corr_hs = np.corrcoef(hs_mod10[:,0],hs_10[:,0])[0,1]
rmse_hs = np.sqrt( pl.sum( (hs_mod10 - hs_10) ** 2 ) / len(hs_10) )
si_hs = (rmse_hs / np.mean(hs_10))
bias_hs = np.mean(hs_mod10 - hs_10)
N = len(hs_10[:,0])
rse10=np.abs([hs_mod10[i,0]-hs_10[i] for i in range(len(hs_mod10))])
me90=np.percentile(rse10,90) # erro 90
textstr = '$\mathrm{RMSE}=%.2fm$\n$\mathrm{SI}=%.2f$\n$\mathrm{Bias}=%.2fm$\n$\mathrm{N}=%.0f$'%(rmse_hs, si_hs,bias_hs,N)
#textstr = '$\mathrm{corr}=%.2f$\n$\mathrm{RMSE}=%.2fm$\n$\mathrm{ME90}=%.2fm$\n$\mathrm{SI}=%.2f$\n$\mathrm{Bias}=%.2fm$\n$\mathrm{N}=%.0f$'%(corr_hs, rmse_hs,me90, si_hs,bias_hs,N)
props = dict(boxstyle='round', facecolor='darkgray', alpha=0.5)
pl.text(0.05, 2.4, textstr, fontsize=13,verticalalignment='top', bbox=props)
pl.savefig(home + '/Dropbox/ww3vale/TU/doc/RT/RT07/fig/scatter/'+'scatter_hs'+name+'.png', dpi=None, facecolor='w', edgecolor='w',papertype=None, format='png')

# --------------- polyfit scatter - tp -------------------
pl.figure(figsize=(13,6))
pl.subplot(121)
zpoly=np.polyfit(tp_04[:,0],tp_mod04[:,0],1)
# calculando o histograma de densidade
xy = np.vstack([tp_04[:,0],tp_mod04[:,0]]);z = gaussian_kde(xy)(xy)
pl.scatter(tp_04, tp_mod04, c=z, s=30,vmin=0,edgecolor='')
pl.colorbar();pl.ylim([0,20]);pl.xlim([0,20])
pl.ylabel('Tp (s) Previsto',fontsize=12);pl.xlabel('Tp (s) Medido',fontsize=12)
pl.plot(np.arange(0,22,0.1),np.arange(0,22,0.1),'k-')
pl.plot(np.arange(0,22,0.1),np.arange(0,22,0.1)*zpoly[0]+zpoly[1],'k--',linewidth=2.0);pl.grid();
corr_tp = np.corrcoef(tp_mod04[:,0],tp_04[:,0])[0,1] # correlacao
rmse_tp = np.sqrt( pl.sum( (tp_mod04 - tp_04) ** 2 ) / len(tp_04) ) # rmse
si_tp = (rmse_tp / np.mean(tp_04))  #si
bias_tp = np.mean(tp_mod04 - tp_04) # bias
rse04=np.abs([tp_mod04[i,0]-tp_04[i] for i in range(len(tp_mod04))])
me90=np.percentile(rse04,90) # erro 90
N = len(tp_04[:,0])
textstr = '$\mathrm{corr}=%.2f$\n$\mathrm{RMSE}=%.2fs$\n$\mathrm{ME90}=%.2fs$\n$\mathrm{SI}=%.2f$\n$\mathrm{Bias}=%.2fs$\n$\mathrm{N}=%.0f$'%(corr_tp, rmse_tp,me90, si_tp,bias_tp,N)
props = dict(boxstyle='round', facecolor='darkgray', alpha=0.5)
pl.text(13.5, 5.5, textstr, fontsize=13,verticalalignment='top', bbox=props)
# ADCP10
pl.subplot(122)
zpoly=np.polyfit(tp_10[:,0],tp_mod10[:,0],1)
# calculando o histograma de densidade
xy = np.vstack([tp_10[:,0],tp_mod10[:,0]]);z = gaussian_kde(xy)(xy)
pl.scatter(tp_10, tp_mod10, c=z, s=30,vmin=0,edgecolor='')
pl.colorbar();pl.ylim([0,20]);pl.xlim([0,20])
pl.ylabel('Tp (s) Previsto',fontsize=12);pl.xlabel('Tp (s) Medido',fontsize=12)
pl.plot(np.arange(0,22,0.1),np.arange(0,22,0.1),'k-')
pl.plot(np.arange(0,22,0.1),np.arange(0,22,0.1)*zpoly[0]+zpoly[1],'k--',linewidth=2.0);pl.grid();
corr_tp = np.corrcoef(tp_mod10[:,0],tp_10[:,0])[0,1]
rmse_tp = np.sqrt( pl.sum( (tp_mod10 - tp_10) ** 2 ) / len(tp_10) )
si_tp = (rmse_tp / np.mean(tp_10))
bias_tp = np.mean(tp_mod10 - tp_10)
N = len(tp_10[:,0])
rse10=np.abs([tp_mod10[i,0]-tp_10[i] for i in range(len(tp_mod10))])
me90=np.percentile(rse10,90) # erro 90
textstr = '$\mathrm{corr}=%.2f$\n$\mathrm{RMSE}=%.2fs$\n$\mathrm{ME90}=%.2fs$\n$\mathrm{SI}=%.2f$\n$\mathrm{Bias}=%.2fs$\n$\mathrm{N}=%.0f$'%(corr_tp, rmse_tp,me90, si_tp,bias_tp,N)
props = dict(boxstyle='round', facecolor='darkgray', alpha=0.5)
pl.text(13.5, 5.5, textstr, fontsize=13,verticalalignment='top', bbox=props)
pl.savefig(home + '/Dropbox/ww3vale/TU/doc/RT/RT07/fig/scatter/'+'scatter_tp'+name+'.png', dpi=None, facecolor='w', edgecolor='w',papertype=None, format='png')


# --------------- polyfit scatter - dp -------------------
inddp10 = np.where(np.isnan(dp_mod10) == False)[0];dp_mod10 = dp_mod10[inddp10];dp_10 = dp_10[inddp10];ddata10=[ddata10[inddp10[i]] for i in range(len(inddp10))]
inddp04 = np.where(np.isnan(dp_mod04) == False)[0];dp_mod04 = dp_mod04[inddp04];dp_04 = dp_04[inddp04];ddata04=[ddata04[inddp04[i]] for i in range(len(inddp04))]

pl.figure(figsize=(13,6))
pl.subplot(121)
zpoly=np.polyfit(dp_04[:,0],dp_mod04[:,0],1)
# calculando o histograma de densidade
xy = np.vstack([dp_04[:,0],dp_mod04[:,0]]);z = gaussian_kde(xy)(xy)
pl.scatter(dp_04, dp_mod04, c=z, s=30,vmin=0,edgecolor='')
pl.colorbar();pl.ylim([0,360]);pl.xlim([0,360])
pl.ylabel('Dp (graus) Previsto',fontsize=12);pl.xlabel('Dp (graus) Medido',fontsize=12)
pl.plot(np.arange(0,365,10),np.arange(0,365,10),'k-')
pl.plot(np.arange(0,365,10),np.arange(0,365,10)*zpoly[0]+zpoly[1],'k--',linewidth=2.0);pl.grid();
corr_dp = np.corrcoef(dp_mod04[:,0],dp_04[:,0])[0,1] # correlacao
rmse_dp = np.sqrt( pl.sum( (dp_mod04 - dp_04) ** 2 ) / len(dp_04) ) # rmse
si_dp = (rmse_dp / np.mean(dp_04))  #si
bias_dp = np.mean(dp_mod04 - dp_04) # bias
rse04=np.abs([dp_mod04[i,0]-dp_04[i] for i in range(len(dp_mod04))])
me90=np.percentile(rse04,90) # erro 90
N = len(dp_04[:,0])
textstr = '$\mathrm{corr}=%.2f$\n$\mathrm{RMSE}=%.2f graus$\n$\mathrm{ME90}=%.2fgraus$\n$\mathrm{SI}=%.2f$\n$\mathrm{Bias}=%.2f graus$\n$\mathrm{N}=%.0f$'%(corr_dp, rmse_dp,me90, si_dp,bias_dp,N)
props = dict(boxstyle='round', facecolor='darkgray', alpha=0.5)
pl.text(13.5, 350, textstr, fontsize=13,verticalalignment='top', bbox=props)
# ADCP10
pl.subplot(122)
zpoly=np.polyfit(dp_10[:,0],dp_mod10[:,0],1)
# calculando o histograma de densidade
xy = np.vstack([dp_10[:,0],dp_mod10[:,0]]);z = gaussian_kde(xy)(xy)
pl.scatter(dp_10, dp_mod10, c=z, s=30,vmin=0,edgecolor='')
pl.colorbar();pl.ylim([0,360]);pl.xlim([0,360])
pl.ylabel('Dp (graus) Previsto');pl.xlabel('Dp (graus) Medido')
pl.plot(np.arange(0,365,10),np.arange(0,365,10),'k-')
pl.plot(np.arange(0,365,10),np.arange(0,365,10)*zpoly[0]+zpoly[1],'k--',linewidth=2.0);pl.grid();
corr_dp = np.corrcoef(dp_mod10[:,0],dp_10[:,0])[0,1]
rmse_dp = np.sqrt( pl.sum( (dp_mod10 - dp_10) ** 2 ) / len(dp_10) )
si_dp = (rmse_dp / np.mean(dp_10))
bias_dp = np.mean(dp_mod10 - dp_10)
N = len(dp_10[:,0])
rse10=np.abs([dp_mod10[i,0]-dp_10[i] for i in range(len(dp_mod10))])
me90=np.percentile(rse10,90) # erro 90
textstr = '$\mathrm{corr}=%.2f$\n$\mathrm{RMSE}=%.2f graus$\n$\mathrm{ME90}=%.2fgraus$\n$\mathrm{SI}=%.2f$\n$\mathrm{Bias}=%.2f graus$\n$\mathrm{N}=%.0f$'%(corr_dp, rmse_dp,me90, si_dp,bias_dp,N)
props = dict(boxstyle='round', facecolor='darkgray', alpha=0.5)
pl.text(13.5, 350, textstr, fontsize=13,verticalalignment='top', bbox=props)
pl.savefig(home + '/Dropbox/ww3vale/TU/doc/RT/RT07/fig/scatter/'+'scatter_dp'+name+'.png', dpi=None, facecolor='w', edgecolor='w',papertype=None, format='png')




# # ------------------------------------------
# #                   Analise do Erro ADCP04
# # ------------------------------------------

# # analise do erro ADCP04
# er04 = hs_04-hs_mod04
# pl.figure()
# pl.subplot(211)
# pl.plot(ddata04,hs_04,'ro',linewidth=2.5)
# #pl.plot(ddata04,hs_04s,'ro')
# pl.plot(ddata04,hs_mod04,'bo',linewidth=2.5)
# pl.legend(['Boia04 (Corrigido)','Boia04 (Previsto)'],loc=2)
# pl.ylim([0,3])
# pl.grid()
# pl.subplot(212)
# pl.plot(ddata04,er04,'ro',linewidth=2.5)
# pl.legend(['dado-modelo'],loc=2)
# pl.ylim([-1.5,1.5])
# pl.grid()
# pl.show()


# #histogram

# fig = pl.figure(figsize=(16,12))
# ax = fig.add_subplot(211)
# binshs=np.arange(-1,1.2,0.2)
# counts,bins,patches = ax.hist(er04[:],bins=binshs,facecolor='gray',edgecolor='black',hatch="/",label="Erro Hs (m)")
# ax.set_xticks(bins)

# #setar eixo y com porcentagem
# lima=[]
# for i in range(0,70,10): lima.append((i*len(er04)/100))

# ax.set_yticks(lima)    
# to_percentage = lambda y, pos: str(round( ( y / float(len(er04)) ) * 100, 0)) + ' %'
# pl.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


# #bin_centers=np.diff(bins) + bins[:-1] - 0.25
# # for count, x in zip(counts,bin_centers):
# #     percent = '%0.1f%%' % (100 * float(count) / counts.sum())
# #     ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
# #         xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)

# ax.legend(loc="upper right")
# pl.grid()
# pl.show()


# ### RMSE ###
# print '------------ ADCP04 --------------'
# print 'RMSE'
# rmse_hs = np.sqrt( pl.sum( (hs_mod04 - hs_04) ** 2 ) / len(hs_04) )
# print rmse_hs

# ### SI ###
# print 'SI'
# si_hs = rmse_hs / np.mean(hs_04)
# print si_hs


# print 'RSE 90%'
# rse=np.abs([hs_mod04[i,0]-hs_04[i] for i in range(len(hs_mod04))])
# print np.percentile(rse,90)

# print '------------ ADCP10 --------------'
# ### RMSE ###
# print 'RMSE'
# rmse_hs = np.sqrt( pl.sum( (hs_mod10 - hs_10) ** 2 ) / len(hs_10) )
# print rmse_hs

# ### SI ###
# print 'SI'
# si_hs = rmse_hs / np.mean(hs_10)
# print si_hs

# print 'ME 90%'
# rse10=np.abs([hs_mod10[i,0]-hs_10[i] for i in range(len(hs_mod10))])
# print np.percentile(rse10,90)
