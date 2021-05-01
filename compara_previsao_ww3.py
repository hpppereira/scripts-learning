'''
Compara os resultados da previsao feita com o ww3v314 e vento GFS 0.5 
e ww3418 com GFS 0.25 para os pontos do PNBOIA

LIOc - Laboratorio de Instrumentacao Oceanografica

Data da ultima modificacao: 23/08/2015
'''

import numpy as np
from datetime import datetime
import pylab as pl
import os
import xlrd

#diretorio de onde estao os resultados do ww3v314
pathname  = os.environ['HOME'] + '/Dropbox/ww3vale/TU/Previsao/Previsao_14maio/ww3v314gfs05/'
direm = np.sort(os.listdir(pathname))

mds=np.array([[0,0,0,0,0,0,0,0,0]])
msantos=np.array([[0,0,0,0]])

mdr=np.array([[0,0,0,0,0,0,0,0,0]])
mrio=np.array([[0,0,0,0,0,0,0,0,0]])

mdf=np.array([[0,0,0,0,0,0,0,0,0]])
mflo=np.array([[0,0,0,0,0,0,0,0,0]])

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in direm:

	#ww3 - um arquivo para cada dia de previsao
	msantos = np.loadtxt(pathname + dto + '/Boiasantos.txt')
	mds=np.concatenate((mds,msantos[:,:]),axis=0)

	mrio = np.loadtxt(pathname + dto + '/BoiaRS.txt')
	mdr=np.concatenate((mdr,mrio[:,:]),axis=0)

	mflo = np.loadtxt(pathname + dto + '/BoiaFl.txt')
	mdf=np.concatenate((mdf,mflo[:,:]),axis=0)

mds = mds[1:,:]
mdr = mdr[1:,:]
mdf = mdf[1:,:]

#diretorio de onde estao os resultados do ww3v418 st4
pathname  = os.environ['HOME'] + '/Dropbox/ww3vale/TU/Previsao/Previsao_14maio/ww3v418st6gfs25/'
direm = np.sort(os.listdir(pathname))

mds4=np.array([[0,0,0,0,0,0,0,0,0]])
msantos4=np.array([[0,0,0,0,0,0,0,0,0]])

mdr4=np.array([[0,0,0,0,0,0,0,0,0]])
mrio4=np.array([[0,0,0,0,0,0,0,0,0]])

mdf4=np.array([[0,0,0,0,0,0,0,0,0]])
mflo4=np.array([[0,0,0,0,0,0,0,0,0]])

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in direm:

	#ww3 - um arquivo para cada dia de previsao
	msantos4 = np.loadtxt(pathname + dto + '/Boiasantos.txt')
	mds4=np.concatenate((mds4,msantos4[:,:]),axis=0)

	mrio4 = np.loadtxt(pathname + dto + '/BoiaRS.txt')
	mdr4=np.concatenate((mdr4,mrio4[:,:]),axis=0)

	mflo4 = np.loadtxt(pathname + dto + '/BoiaFl.txt')
	mdf4=np.concatenate((mdf4,mflo4[:,:]),axis=0)

mds4 = mds4[1:,:]
mdr4 = mdr4[1:,:]
mdf4 = mdf4[1:,:]

#diretorio de onde estao os resultados do ww3v418 st2
pathname  = os.environ['HOME'] + '/Dropbox/ww3vale/TU/Previsao/Previsao_14maio/ww3v418st4mgfs25/'
direm = np.sort(os.listdir(pathname))

mds2=np.array([[0,0,0,0,0,0,0,0,0]])
msantos2=np.array([[0,0,0,0,0,0,0,0,0]])

mdr2=np.array([[0,0,0,0,0,0,0,0,0]])
mrio2=np.array([[0,0,0,0,0,0,0,0,0]])

mdf2=np.array([[0,0,0,0,0,0,0,0,0]])
mflo2=np.array([[0,0,0,0,0,0,0,0,0]])

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in direm:

	#ww3 - um arquivo para cada dia de previsao
	msantos2 = np.loadtxt(pathname + dto + '/Boiasantos.txt')
	mds2=np.concatenate((mds2,msantos2[:,:]),axis=0)

	mrio2 = np.loadtxt(pathname + dto + '/BoiaRS.txt')
	mdr2=np.concatenate((mdr2,mrio2[:,:]),axis=0)

	mflo2 = np.loadtxt(pathname + dto + '/BoiaFl.txt')
	mdf2=np.concatenate((mdf2,mflo2[:,:]),axis=0)

mds2 = mds2[1:,:]
mdr2 = mdr2[1:,:]
mdf2 = mdf2[1:,:]



#modelo (serve tanto para o ww3 quanto para o swan)
data_mod=mds[:,:]
#data_mod = data_mod.astype(str) #ano mes dia hora
datam = np.array([datetime(int(data_mod[i,0]),int(data_mod[i,1]),int(data_mod[i,2]),int(data_mod[i,3])) for i in range(len(data_mod[:,0]))])

#############################################################################
#carrega parametros de ondas do WW3
#Boias Axys do PNBOIA: Santos, Rio Grande e Florianopolis

# DADOS BOIA
pathname_mb = os.environ['HOME'] + '/Dropbox/ww3vale/Trocas/PNBOIA/dados/' #planilha excel baixada do site da MB


# local = 'Santos/SP - PNBOIA'
# mesboia = 'MAI_ARGOS_69150_Santos.xls'



# local = 'Florianopolis/SC - PNBOIA'
# mesboia = 'MAI_ARGOS_69152_SantaCatarina.xls'
local = 'Rio Grande/RS - PNBOIA'
mesboia = 'MAI_ARGOS_69153_RioGrande.xls'

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

#pl.close('all')
pl.figure()
pl.subplot(311)
pl.title('BOIA RIO GRANDE')
pl.plot(dt1[:],dd1[:,7],'or',label='RS')
#pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,1],'k.-',label='Prev08')
#pl.plot(datam[1*7*24+1:2*7*24+2],mdd[1*7*24+1:2*7*24+2,1],'b.-',label='Prev09')
#pl.plot(datam[2*7*24+2:3*7*24+3],mdd[2*7*24+2:3*7*24+3,1],'g.-',label='Prev10')
pl.plot(datam[3*7*24+3:4*7*24+4],mdr[3*7*24+3:4*7*24+4,5],'k-',label='Prev11_314',linewidth=2)
pl.plot(datam[3*7*24+3:4*7*24+4],mdr4[3*7*24+3:4*7*24+4,5],'ko',label='Prev11_st6')
pl.plot(datam[3*7*24+3:4*7*24+4],mdr2[3*7*24+3:4*7*24+4,5],'k--',label='Prev11_st4m')
pl.plot(datam[4*7*24+4:5*7*24+5],mdr[4*7*24+4:5*7*24+5,5],'b-',label='Prev12_314',linewidth=2)
pl.plot(datam[4*7*24+4:5*7*24+5],mdr4[4*7*24+4:5*7*24+5,5],'bo',label='Prev12_st6')
pl.plot(datam[4*7*24+4:5*7*24+5],mdr2[4*7*24+4:5*7*24+5,5],'b--',label='Prev12_st4m')
#pl.plot(datam[5*7*24+5:6*7*24+6],mdr[5*7*24+5:6*7*24+6,1],'b-',label='Prev13',linewidth=2)
#pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,1],'b.-',label='Prev14')
pl.legend(loc=0,fontsize=10)
pl.ylim([0,6])
pl.ylabel('Hs (m)'), pl.grid()

#pl.figure()
pl.subplot(312)
pl.plot(dt1[:],dd1[:,9],'or',label='RS')
#pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,2],'k.',label='Prev08')
#pl.plot(datam[1*7*24+2:2*7*24+1],mdd[1*7*24+2:2*7*24+1,2],'k.',label='Prev09')
#pl.plot(datam[2*7*24+2:3*7*24+1],mdd[2*7*24+2:3*7*24+1,2],'g.',label='Prev10')
pl.plot(datam[3*7*24+3:4*7*24+4],mdr[3*7*24+3:4*7*24+4,6],'k-',label='Prev11_314',linewidth=2)
pl.plot(datam[3*7*24+3:4*7*24+4],mdr4[3*7*24+3:4*7*24+4,6],'ko',label='Prev11_st6')
pl.plot(datam[3*7*24+3:4*7*24+4],mdr2[3*7*24+3:4*7*24+4,6],'k--',label='Prev11_st4m')
pl.plot(datam[4*7*24+4:5*7*24+5],mdr[4*7*24+4:5*7*24+5,6],'b-',label='Prev12_314',linewidth=2)
pl.plot(datam[4*7*24+4:5*7*24+5],mdr4[4*7*24+4:5*7*24+5,6],'bo',label='Prev12_st6')
pl.plot(datam[4*7*24+4:5*7*24+5],mdr2[4*7*24+4:5*7*24+5,6],'b--',label='Prev12_st4m')
#pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,2],'b.',label='Prev14')
pl.ylabel('Tp (s)'), pl.grid()
pl.legend(loc=0,fontsize=10)

#pl.figure()
pl.subplot(313)
pl.plot(dt1[:],dd1[:,10].astype(float)-23,'or',label='RS')
#pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,3],'k.',label='Prev08')
#pl.plot(datam[1*7*24+2:2*7*24+1],mdd[1*7*24+2:2*7*24+1,3],'k.',label='Prev09')
#pl.plot(datam[2*7*24+2:3*7*24+1],mdd[2*7*24+2:3*7*24+1,3],'g.',label='Prev10')
pl.plot(datam[3*7*24+3:4*7*24+4],mdr[3*7*24+3:4*7*24+4,7],'k-',label='Prev11_314',linewidth=2)
pl.plot(datam[3*7*24+3:4*7*24+4],mdr4[3*7*24+3:4*7*24+4,7],'ko',label='Prev11_st6')
pl.plot(datam[3*7*24+3:4*7*24+4],mdr2[3*7*24+3:4*7*24+4,7],'k--',label='Prev11_st4m')
pl.plot(datam[4*7*24+4:5*7*24+5],mdr[4*7*24+4:5*7*24+5,7],'b-',label='Prev12_314',linewidth=2)
pl.plot(datam[4*7*24+4:5*7*24+5],mdr4[4*7*24+4:5*7*24+5,7],'bo',label='Prev12_st6')
pl.plot(datam[4*7*24+4:5*7*24+5],mdr2[4*7*24+4:5*7*24+5,7],'b--',label='Prev12_st4m')
#pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,3],'b.',label='Prev14')
pl.ylabel('Dp (graus)'), pl.grid()
pl.legend(loc=0,fontsize=10)
pl.show()



# #pl.close('all')
# pl.figure()
# pl.subplot(311)
# pl.title('BOIA FLORIANOPOLIS')
# pl.plot(dt1[:],dd1[:,7],'or',label='FLORIPA')
# #pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,1],'k.-',label='Prev08')
# #pl.plot(datam[1*7*24+1:2*7*24+2],mdd[1*7*24+1:2*7*24+2,1],'b.-',label='Prev09')
# #pl.plot(datam[2*7*24+2:3*7*24+3],mdd[2*7*24+2:3*7*24+3,1],'g.-',label='Prev10')
# pl.plot(datam[3*7*24+3:4*7*24+4],mdf[3*7*24+3:4*7*24+4,5],'k-',label='Prev11_314',linewidth=2)
# pl.plot(datam[3*7*24+3:4*7*24+4],mdf4[3*7*24+3:4*7*24+4,5],'ko',label='Prev11_st6')
# pl.plot(datam[3*7*24+3:4*7*24+4],mdf2[3*7*24+3:4*7*24+4,5],'k--',label='Prev11_st4m')
# pl.plot(datam[4*7*24+4:5*7*24+5],mdf[4*7*24+4:5*7*24+5,5],'b-',label='Prev12_314',linewidth=2)
# pl.plot(datam[4*7*24+4:5*7*24+5],mdf4[4*7*24+4:5*7*24+5,5],'bo',label='Prev12_st6')
# pl.plot(datam[4*7*24+4:5*7*24+5],mdf2[4*7*24+4:5*7*24+5,5],'b--',label='Prev12_st4m')
# #pl.plot(datam[5*7*24+5:6*7*24+6],mdr[5*7*24+5:6*7*24+6,1],'b-',label='Prev13',linewidth=2)
# #pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,1],'b.-',label='Prev14')
# pl.legend(loc=0,fontsize=10)
# pl.ylim([0,8])
# pl.ylabel('Hs (m)'), pl.grid()

# #pl.figure()
# pl.subplot(312)
# pl.plot(dt1[:],dd1[:,9],'or',label='FLORIPA')
# #pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,2],'k.',label='Prev08')
# #pl.plot(datam[1*7*24+2:2*7*24+1],mdd[1*7*24+2:2*7*24+1,2],'k.',label='Prev09')
# #pl.plot(datam[2*7*24+2:3*7*24+1],mdd[2*7*24+2:3*7*24+1,2],'g.',label='Prev10')
# pl.plot(datam[3*7*24+3:4*7*24+4],mdf[3*7*24+3:4*7*24+4,6],'k-',label='Prev11_314',linewidth=2)
# pl.plot(datam[3*7*24+3:4*7*24+4],mdf4[3*7*24+3:4*7*24+4,6],'ko',label='Prev11_st6')
# pl.plot(datam[3*7*24+3:4*7*24+4],mdf2[3*7*24+3:4*7*24+4,6],'k--',label='Prev11_st4m')
# pl.plot(datam[4*7*24+4:5*7*24+5],mdf[4*7*24+4:5*7*24+5,6],'b-',label='Prev12_314',linewidth=2)
# pl.plot(datam[4*7*24+4:5*7*24+5],mdf4[4*7*24+4:5*7*24+5,6],'bo',label='Prev12_st6')
# pl.plot(datam[4*7*24+4:5*7*24+5],mdf2[4*7*24+4:5*7*24+5,6],'b--',label='Prev12_st4m')
# #pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,2],'b.',label='Prev14')
# pl.ylabel('Tp (s)'), pl.grid()
# pl.legend(loc=0,fontsize=10)

# #pl.figure()
# pl.subplot(313)
# pl.plot(dt1[:],dd1[:,10].astype(float)-23,'or',label='FLORIPA')
# #pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,3],'k.',label='Prev08')
# #pl.plot(datam[1*7*24+2:2*7*24+1],mdd[1*7*24+2:2*7*24+1,3],'k.',label='Prev09')
# #pl.plot(datam[2*7*24+2:3*7*24+1],mdd[2*7*24+2:3*7*24+1,3],'g.',label='Prev10')
# pl.plot(datam[3*7*24+3:4*7*24+4],mdf[3*7*24+3:4*7*24+4,7],'k-',label='Prev11_314',linewidth=2)
# pl.plot(datam[3*7*24+3:4*7*24+4],mdf4[3*7*24+3:4*7*24+4,7],'ko',label='Prev11_st6')
# pl.plot(datam[3*7*24+3:4*7*24+4],mdf2[3*7*24+3:4*7*24+4,7],'k--',label='Prev11_st4m')
# pl.plot(datam[4*7*24+4:5*7*24+5],mdf[4*7*24+4:5*7*24+5,7],'b-',label='Prev12_314',linewidth=2)
# pl.plot(datam[4*7*24+4:5*7*24+5],mdf4[4*7*24+4:5*7*24+5,7],'bo',label='Prev12_st6')
# pl.plot(datam[4*7*24+4:5*7*24+5],mdf2[4*7*24+4:5*7*24+5,7],'b--',label='Prev12_st4m')
# #pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,3],'b.',label='Prev14')
# pl.ylabel('Dp (graus)'), pl.grid()
# pl.legend(loc=0,fontsize=10)
# pl.show()



# #pl.close('all')
# pl.figure()
# pl.subplot(311)
# pl.title('BOIA SANTOS')
# pl.plot(dt1[:],dd1[:,7],'or',label='SANTOS')
# #pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,1],'k.-',label='Prev08')
# #pl.plot(datam[1*7*24+1:2*7*24+2],mdd[1*7*24+1:2*7*24+2,1],'b.-',label='Prev09')
# #pl.plot(datam[2*7*24+2:3*7*24+3],mdd[2*7*24+2:3*7*24+3,1],'g.-',label='Prev10')
# pl.plot(datam[3*7*24+3:4*7*24+4],mds[3*7*24+3:4*7*24+4,5],'k-',label='Prev11_314',linewidth=2)
# pl.plot(datam[3*7*24+3:4*7*24+4],mds4[3*7*24+3:4*7*24+4,5],'ko',label='Prev11_st6')
# pl.plot(datam[3*7*24+3:4*7*24+4],mds2[3*7*24+3:4*7*24+4,5],'k--',label='Prev11_st4m')
# pl.plot(datam[4*7*24+4:5*7*24+5],mds[4*7*24+4:5*7*24+5,5],'b-',label='Prev12_314',linewidth=2)
# pl.plot(datam[4*7*24+4:5*7*24+5],mds4[4*7*24+4:5*7*24+5,5],'bo',label='Prev12_st6')
# pl.plot(datam[4*7*24+4:5*7*24+5],mds2[4*7*24+4:5*7*24+5,5],'b--',label='Prev12_st4m')
# #pl.plot(datam[5*7*24+5:6*7*24+6],mdr[5*7*24+5:6*7*24+6,1],'b-',label='Prev13',linewidth=2)
# #pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,1],'b.-',label='Prev14')
# pl.legend(loc=0,fontsize=10)
# pl.ylim([0,6])
# pl.ylabel('Hs (m)'), pl.grid()

# #pl.figure()
# pl.subplot(312)
# pl.plot(dt1[:],dd1[:,9],'or',label='SANTOS')
# #pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,2],'k.',label='Prev08')
# #pl.plot(datam[1*7*24+2:2*7*24+1],mdd[1*7*24+2:2*7*24+1,2],'k.',label='Prev09')
# #pl.plot(datam[2*7*24+2:3*7*24+1],mdd[2*7*24+2:3*7*24+1,2],'g.',label='Prev10')
# pl.plot(datam[3*7*24+3:4*7*24+4],mds[3*7*24+3:4*7*24+4,6],'k-',label='Prev11_314',linewidth=2)
# pl.plot(datam[3*7*24+3:4*7*24+4],mds4[3*7*24+3:4*7*24+4,6],'ko',label='Prev11_st6')
# pl.plot(datam[3*7*24+3:4*7*24+4],mds2[3*7*24+3:4*7*24+4,6],'k--',label='Prev11_st4m')
# pl.plot(datam[4*7*24+4:5*7*24+5],mds[4*7*24+4:5*7*24+5,6],'b-',label='Prev12_314',linewidth=2)
# pl.plot(datam[4*7*24+4:5*7*24+5],mds4[4*7*24+4:5*7*24+5,6],'bo',label='Prev12_st6')
# pl.plot(datam[4*7*24+4:5*7*24+5],mds2[4*7*24+4:5*7*24+5,6],'b--',label='Prev12_st4m')
# #pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,2],'b.',label='Prev14')
# pl.ylabel('Tp (s)'), pl.grid()
# pl.legend(loc=0,fontsize=10)

# #pl.figure()
# pl.subplot(313)
# pl.plot(dt1[:],dd1[:,10].astype(float)-23,'or',label='SANTOS')
# #pl.plot(datam[0:1*7*24+1],mdd[0:1*7*24+1,3],'k.',label='Prev08')
# #pl.plot(datam[1*7*24+2:2*7*24+1],mdd[1*7*24+2:2*7*24+1,3],'k.',label='Prev09')
# #pl.plot(datam[2*7*24+2:3*7*24+1],mdd[2*7*24+2:3*7*24+1,3],'g.',label='Prev10')
# pl.plot(datam[3*7*24+3:4*7*24+4],mds[3*7*24+3:4*7*24+4,7],'k-',label='Prev11_314',linewidth=2)
# pl.plot(datam[3*7*24+3:4*7*24+4],mds4[3*7*24+3:4*7*24+4,7],'ko',label='Prev11_st6')
# pl.plot(datam[3*7*24+3:4*7*24+4],mds2[3*7*24+3:4*7*24+4,7],'k--',label='Prev11_st4m')
# pl.plot(datam[4*7*24+4:5*7*24+5],mds[4*7*24+4:5*7*24+5,7],'b-',label='Prev12_314',linewidth=2)
# pl.plot(datam[4*7*24+4:5*7*24+5],mds4[4*7*24+4:5*7*24+5,7],'bo',label='Prev12_st6')
# pl.plot(datam[4*7*24+4:5*7*24+5],mds2[4*7*24+4:5*7*24+5,7],'b--',label='Prev12_st4m')
# #pl.plot(datam[6*7*24+6:7*7*24+7],mdd[6*7*24+6:7*7*24+7,3],'b.',label='Prev14')
# pl.ylabel('Dp (graus)'), pl.grid()
# pl.legend(loc=0,fontsize=10)
# pl.show()
