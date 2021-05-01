'''
Plota previsao do LIOc para os ADCPs e para  boias do PNBOIA

LIOc - Laboratorio de Instrumentacao Oceanografica

Data da ultima modificacao: 19/07/2015
'''

import numpy as np
from datetime import datetime
import pylab as pl
import os
import xlrd

#Saida SWAN
# 0   1   2    3   4   5  6  7   8
#tempo,hs,dp,tp,xwind,ywind,hsswell,sprd

# plotar para o adcp 01
#diretorio de onde estao os resultados
pathname  = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/Previsao/Previsao_14maio/'
direm = np.sort(os.listdir(pathname))

mdd=np.array([[0,0,0,0]])
madcp01=np.array([[0,0,0,0]])

mds=np.array([[0,0,0,0]])
msantos=np.array([[0,0,0,0]])

mdr=np.array([[0,0,0,0]])
mrio=np.array([[0,0,0,0]])

mdf=np.array([[0,0,0,0]])
mflo=np.array([[0,0,0,0]])

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in direm:

	madcp01= np.loadtxt(pathname + dto + '/table_point_ADCP10.out',skiprows=7,usecols=(0,1,3,2))
	mdd=np.concatenate((mdd,madcp01[:,:]),axis=0)

	#ww3 - um arquivo para cada dia de previsao
	msantos = np.loadtxt(pathname + dto + '/Boiasantos.txt',usecols=(0,5,6,7))
	mds=np.concatenate((mds,msantos[:,:]),axis=0)

	mrio = np.loadtxt(pathname + dto + '/BoiaRS.txt',usecols=(0,5,6,7))
	mdr=np.concatenate((mdr,mrio[:,:]),axis=0)

	mflo = np.loadtxt(pathname + dto + '/BoiaFl.txt',usecols=(0,5,6,7))
	mdf=np.concatenate((mdf,mflo[:,:]),axis=0)

mdd = mdd[1:,:]
mds = mds[1:,:]
mdr = mdr[1:,:]
mdf = mdf[1:,:]

#modelo (serve tanto para o ww3 quanto para o swan)
data_mod=mdd[:,0]*100
data_mod = data_mod.astype(str) #ano mes dia hora
datam = np.array([datetime(int(data_mod[i][0:4]),int(data_mod[i][4:6]),int(data_mod[i][6:8]),int(data_mod[i][8:10])) for i in range(len(data_mod))])


# DADOS ADCP
pathname_adcp = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/dados/ADCP/operacional/' #dados

#nome dos arquivos
#adcp - boia 4 e 10
adcp04 = 'TU_boia04.out' #fora do porto (mais fundo)
adcp10 = 'TU_boia10.out' #dentro do porto

#carrega dados
# 0      1      2     3         4        5    6   7   8 9
#data,bateria,rumo,pressao,temperatura,pitch,roll,hs,tp,dp
adcp04 = np.loadtxt(pathname_adcp + adcp04,delimiter=',')
adcp10 = np.loadtxt(pathname_adcp + adcp10,delimiter=',')

dadcp04 = [ datetime.strptime(str(int(adcp04[i,0])), '%Y%m%d%H%M') for i in range(len(adcp04)) ]
dadcp10 = [ datetime.strptime(str(int(adcp10[i,0])), '%Y%m%d%H%M') for i in range(len(adcp10)) ]

### achear data
#pl.find(np.array(dadcp10).astype(str)=='2015-02-23 14:40:00')


#############################################################################
#carrega parametros de ondas do WW3
#Boias Axys do PNBOIA: Santos, Rio Grande e Florianopolis

# DADOS BOIA
pathname_mb = os.environ['HOME'] + '/Dropbox/lioc/dados/pnboia/mb/' #planilha excel baixada do site da MB


local = 'Santos/SP - PNBOIA'
mesboia = 'MAI_ARGOS_69150_Santos.xls'

# local = 'Rio Grande/RS - PNBOIA'
# mesboia = 'MAI_ARGOS_69153_RioGrande.xls'

# local = 'Florianopolis/SC - PNBOIA'
# mesboia = 'MAI_ARGOS_69152_SantaCatarina.xls'

workbook = xlrd.open_workbook(pathname_mb + mesboia)

#seleciona planilha por indice (pode ser por nome tbm)
sheet_0 = workbook.sheet_by_index(0) #planilha 1 - status + vento
sheet_1 = workbook.sheet_by_index(1) #planilha 2 - meteo + onda

#pega os valores das celulas selecionadas

#legenda
leg0 = np.array([[sheet_0.cell_value(r,c) for r in range(3,4)] for c in range(0,sheet_0.ncols)]).T
leg1 = np.array([[sheet_1.cell_value(r,c) for r in range(3,4)] for c in range(0,sheet_1.ncols)]).T

#dados - inverte - flipud
dd0 = np.flipud(np.array([[sheet_0.cell_value(r,c) for r in range(4,sheet_0.nrows)] for c in range(sheet_0.ncols)]).T)
dd1 = np.flipud(np.array([[sheet_1.cell_value(r,c) for r in range(4,sheet_1.nrows)] for c in range(sheet_1.ncols)]).T)

#substitui 'xxxx' por nan
dd0[np.where(dd0=='xxxx')] = np.nan
dd1[np.where(dd1=='xxxx')] = np.nan
dd1[np.where(dd1=='')] = np.nan

#dados da planilha 1 - dd1
# 7     8   9  10
# hs, hmax, tp dp

#data com datetime (nao sao iguais as datas das duas planilhas- deveria ser..)
dt0 = np.array([ datetime.strptime(dd0[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd0)) ])
dt1 = np.array([ datetime.strptime(dd1[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd1)) ])


pl.close('all')
pl.figure()
pl.subplot(311)
pl.title('ADCP-10             2015-05-13 06:00:00')
pl.plot(dadcp10[3:1234],adcp10[0:1234-3,7],'ro',label='ADCP10')
#pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,1],'k.-',label='Prev08')
#pl.plot(datam[1*7*24+1:2*7*24+2],mdd[1*7*24+1:2*7*24+2,1],'b.-',label='Prev09')
#pl.plot(datam[2*7*24+2:3*7*24+3],mdd[2*7*24+2:3*7*24+3,1],'g.-',label='Prev10')
pl.plot(datam[3*7*24+3:4*7*24+4],mdd[3*7*24+3:4*7*24+4,1],'k--',label='Prev11')
pl.plot(datam[4*7*24+4:5*7*24+5],mdd[4*7*24+4:5*7*24+5,1],'k',label='Prev12')
pl.plot(datam[5*7*24+5:6*7*24+6],mdd[5*7*24+5:6*7*24+6,1],'b-',label='Prev13',linewidth=3)
#pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,1],'b.-',label='Prev14')
pl.legend(loc=0,fontsize=10)
pl.ylabel('Hs (m)'), pl.grid()

#pl.figure()
pl.subplot(312)
pl.plot(dadcp10[3:1234],adcp10[0:1234-3,8],'or',label='ADCP10')
#pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,2],'k.',label='Prev08')
#pl.plot(datam[1*7*24+2:2*7*24+1],mdd[1*7*24+2:2*7*24+1,2],'k.',label='Prev09')
#pl.plot(datam[2*7*24+2:3*7*24+1],mdd[2*7*24+2:3*7*24+1,2],'g.',label='Prev10')
pl.plot(datam[3*7*24+3:4*7*24+4],mdd[3*7*24+3:4*7*24+4,2],'k--',label='Prev11')
pl.plot(datam[4*7*24+4:5*7*24+5],mdd[4*7*24+4:5*7*24+5,2],'k',label='Prev12')
pl.plot(datam[5*7*24+5:6*7*24+6],mdd[5*7*24+5:6*7*24+6,2],'b-',label='Prev13',linewidth=2)
#pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,2],'b.',label='Prev14')
pl.ylabel('Tp (s)'), pl.grid()
pl.legend(loc=0,fontsize=10)

#pl.figure()
pl.subplot(313)
pl.plot(dadcp10[3:1234],adcp10[0:1234-3,9]-23,'or',label='ADCP10')
#pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,3],'k.',label='Prev08')
#pl.plot(datam[1*7*24+2:2*7*24+1],mdd[1*7*24+2:2*7*24+1,3],'k.',label='Prev09')
#pl.plot(datam[2*7*24+2:3*7*24+1],mdd[2*7*24+2:3*7*24+1,3],'g.',label='Prev10')
pl.plot(datam[3*7*24+3:4*7*24+4],mdd[3*7*24+3:4*7*24+4,3],'k--',label='Prev11')
pl.plot(datam[4*7*24+4:5*7*24+5],mdd[4*7*24+4:5*7*24+5,3],'k',label='Prev12')
pl.plot(datam[5*7*24+5:6*7*24+6],mdd[5*7*24+5:6*7*24+6,3],'b-',label='Prev13',linewidth=2)
#pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,3],'b.',label='Prev14')
pl.ylabel('Dp (graus)'), pl.grid()
pl.legend(loc=0,fontsize=10)
pl.show()



#pl.close('all')
pl.figure()
pl.subplot(311)
pl.title('BOIA SANTOS             2015-05-13 06:00:00')
pl.plot(dt1[:],dd1[:,7],'or',label='Santos')
#pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,1],'k.-',label='Prev08')
#pl.plot(datam[1*7*24+1:2*7*24+2],mdd[1*7*24+1:2*7*24+2,1],'b.-',label='Prev09')
#pl.plot(datam[2*7*24+2:3*7*24+3],mdd[2*7*24+2:3*7*24+3,1],'g.-',label='Prev10')
pl.plot(datam[3*7*24+3:4*7*24+4],mds[3*7*24+3:4*7*24+4,1],'k--',label='Prev11')
pl.plot(datam[4*7*24+4:5*7*24+5],mds[4*7*24+4:5*7*24+5,1],'k',label='Prev12')
pl.plot(datam[5*7*24+5:6*7*24+6],mds[5*7*24+5:6*7*24+6,1],'b-',label='Prev13',linewidth=2)
#pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,1],'b.-',label='Prev14')
pl.legend(loc=0,fontsize=10)
pl.ylim([0,6])
pl.ylabel('Hs (m)'), pl.grid()

#pl.figure()
pl.subplot(312)
pl.plot(dt1[:],dd1[:,9],'or',label='Santos')
#pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,2],'k.',label='Prev08')
#pl.plot(datam[1*7*24+2:2*7*24+1],mdd[1*7*24+2:2*7*24+1,2],'k.',label='Prev09')
#pl.plot(datam[2*7*24+2:3*7*24+1],mdd[2*7*24+2:3*7*24+1,2],'g.',label='Prev10')
pl.plot(datam[3*7*24+3:4*7*24+4],mds[3*7*24+3:4*7*24+4,2],'k--',label='Prev11')
pl.plot(datam[4*7*24+4:5*7*24+5],mds[4*7*24+4:5*7*24+5,2],'k',label='Prev12')
pl.plot(datam[5*7*24+5:6*7*24+6],mds[5*7*24+5:6*7*24+6,2],'b-',label='Prev13',linewidth=2)
#pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,2],'b.',label='Prev14')
pl.ylabel('Tp (s)'), pl.grid()
pl.legend(loc=0,fontsize=10)

#pl.figure()
pl.subplot(313)
pl.plot(dt1[:],dd1[:,10].astype(float)-23,'or',label='Santos')
#pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,3],'k.',label='Prev08')
#pl.plot(datam[1*7*24+2:2*7*24+1],mdd[1*7*24+2:2*7*24+1,3],'k.',label='Prev09')
#pl.plot(datam[2*7*24+2:3*7*24+1],mdd[2*7*24+2:3*7*24+1,3],'g.',label='Prev10')
pl.plot(datam[3*7*24+3:4*7*24+4],mds[3*7*24+3:4*7*24+4,3],'k--',label='Prev11')
pl.plot(datam[4*7*24+4:5*7*24+5],mds[4*7*24+4:5*7*24+5,3],'k',label='Prev12')
pl.plot(datam[5*7*24+5:6*7*24+6],mds[5*7*24+5:6*7*24+6,3],'b-',label='Prev13',linewidth=2)
#pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,3],'b.',label='Prev14')
pl.ylabel('Dp (graus)'), pl.grid()
pl.legend(loc=0,fontsize=10)
pl.show()

