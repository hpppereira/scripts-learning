'''
programa principal para leitura dos dados de ADCP nas
planilhas em excel do porto de tubarao

LIOc - Laboratorio de Instrumentacao Oceanografica
Henrique P P Pereira
Izabel C M Nogueira
Isabela Cabral
Talitha Lourenco
Tamiris Alfama

Data da ultima modificacao: 14/08/2015
'''

import xlrd
import os
import numpy as np
from matplotlib import pylab as pl
import datetime

pl.close('all')

#opcoes das plotagens
# lsf = 18 #fontsize para as figuras
figsize1 = (15,9)

#variaveis de onda dos adcp
anemo = np.array([[0,0,0]])
adcp1 = np.array([[0,0,0,0,0,0,0,0,0]])
adcp2 = np.array([[0,0,0,0,0,0,0,0,0]])
adcp3 = np.array([[0,0,0,0,0,0,0,0,0]])
adcp4 = np.array([[0,0,0,0,0,0,0,0,0]])

#varia as 13 campanhas
for i in range(1,14):

	#campanha a ser processada (1 a 13)
	camp = i

	#deixa com 2 digitos
	camp = str(camp).zfill(2)

	#pathname = os.environ['HOME'] + 'C:Users/Cliente/Dropbox/ww3vale/Geral/TU/dados/Planilhas_Processadas/'
	pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/proc_vale/Planilhas/xls/'
	pathadcp = 'PTU_campanha_' + camp + '.xls'

	#Open an Excel workbook 
	workbook = xlrd.open_workbook(pathname + pathadcp)

	print pathadcp

	#imprime nome das planilhas
	# print workbook.sheet_names()

	#seleciona planilha por indice (pode ser por nome tbm)
	sheet_0 = workbook.sheet_by_index(0) #anemometro
	sheet_3 = workbook.sheet_by_index(5) #adcp-1
	sheet_5 = workbook.sheet_by_index(9) #adcp-2
	sheet_7 = workbook.sheet_by_index(13) #adcp-3
	sheet_9 = workbook.sheet_by_index(17) #adcp-4

	#pega os valores das celulas selecionadas
	#vento
	vento = np.array([[sheet_0.cell_value(r,c) for r in range(18,sheet_0.nrows)] for c in range(1,sheet_0.ncols)]).T
	
	#onda
	#  0    1    2     3      4     5      6      7    8
	# data hm0, h10, hmax, dirtp, SprTp, MeanDir, Tp, Tm02
	onda1 = np.array([[sheet_3.cell_value(r,c) for r in range(22,sheet_3.nrows)] for c in range(1,sheet_3.ncols)]).T
	onda2 = np.array([[sheet_5.cell_value(r,c) for r in range(22,sheet_5.nrows)] for c in range(1,sheet_5.ncols)]).T
	onda3 = np.array([[sheet_7.cell_value(r,c) for r in range(22,sheet_7.nrows)] for c in range(1,sheet_7.ncols)]).T
	onda4 = np.array([[sheet_9.cell_value(r,c) for r in range(22,sheet_9.nrows)] for c in range(1,sheet_9.ncols)]).T

	#data com datetime
	# data1 = [datetime.datetime(*xlrd.xldate_as_tuple(onda1[i,0],workbook.datemode)) for i in range(len(onda1))]
	# data2 = [datetime.datetime(*xlrd.xldate_as_tuple(onda2[i,0],workbook.datemode)) for i in range(len(onda2))]
	# data3 = [datetime.datetime(*xlrd.xldate_as_tuple(onda3[i,0],workbook.datemode)) for i in range(len(onda3))]
	# data4 = [datetime.datetime(*xlrd.xldate_as_tuple(onda4[i,0],workbook.datemode)) for i in range(len(onda4))]

	#  0     1    2     3      4     5        6   7
	# hm0, h10, hmax, dirtp, SprTp, MeanDir, Tp, Tm02
	# onda1 = onda1[:,1:]
	# onda2 = onda2[:,1:]
	# onda3 = onda3[:,1:]
	# onda4 = onda4[:,1:]

	#concatena as variaveis de cada adcp
	anemo = np.concatenate((anemo,vento),axis=0)
	adcp1 = np.concatenate((adcp1,onda1),axis=0)
	adcp2 = np.concatenate((adcp2,onda2),axis=0)
	adcp3 = np.concatenate((adcp3,onda3),axis=0)
	adcp4 = np.concatenate((adcp4,onda4),axis=0)

#retira a primeira linha com zeros devido a concatenacao
anemo = anemo[1:,:]
adcp1 = adcp1[1:,:]
adcp2 = adcp2[1:,:]
adcp3 = adcp3[1:,:]
adcp4 = adcp4[1:,:]

#data com datetime
datan = [datetime.datetime(*xlrd.xldate_as_tuple(anemo[i,0],workbook.datemode)) for i in range(len(anemo))] # anemometro
data1 = [datetime.datetime(*xlrd.xldate_as_tuple(adcp1[i,0],workbook.datemode)) for i in range(len(adcp1))]
data2 = [datetime.datetime(*xlrd.xldate_as_tuple(adcp2[i,0],workbook.datemode)) for i in range(len(adcp2))]
data3 = [datetime.datetime(*xlrd.xldate_as_tuple(adcp3[i,0],workbook.datemode)) for i in range(len(adcp3))]
data4 = [datetime.datetime(*xlrd.xldate_as_tuple(adcp4[i,0],workbook.datemode)) for i in range(len(adcp4))]

#consistencia
#coloca nan no lugar de 999
anemo[np.where(anemo==999)] = np.nan
adcp1[np.where(adcp1==999)] = np.nan
adcp2[np.where(adcp2==999)] = np.nan
adcp3[np.where(adcp3==999)] = np.nan
adcp4[np.where(adcp4==999)] = np.nan

#retira a primeira coluna com datas

# anemometro (deixa de hora em hora)
#  0    1
# int, dir
anemo = anemo[:,1:]

# adcp
#  0     1    2     3      4     5        6   7
# hm0, h10, hmax, dirtp, SprTp, MeanDir, Tp, Tm02
adcp1 = adcp1[:,1:]
adcp2 = adcp2[:,1:]
adcp3 = adcp3[:,1:]
adcp4 = adcp4[:,1:]

#acha indices das datas para plotagemm
#verao (fev)
inip_anemo = np.where(np.array(datan).astype(str)=='2013-02-01 00:00:00')[0]
fimp_anemo = np.where(np.array(datan).astype(str)=='2013-03-01 00:00:00')[0]

inip_adcp = np.where(np.array(data1).astype(str)=='2013-02-01 00:05:00')[0]
fimp_adcp = np.where(np.array(data1).astype(str)=='2013-03-01 00:05:00')[0]

#inverno (jul)
inip_anemo = np.where(np.array(datan).astype(str)=='2013-07-01 00:00:00')[0]
fimp_anemo = np.where(np.array(datan).astype(str)=='2013-08-01 00:00:00')[0]

inip_adcp = np.where(np.array(data1).astype(str)=='2013-07-01 00:05:00')[0]
fimp_adcp = np.where(np.array(data1).astype(str)=='2013-08-01 00:05:00')[0]

# inip_anemo = 0
# inip_anemo = len(datan)

# fimp_adcp = 0
# fimp_adcp = len(data1)

#cria arquivos ascii (.out) para cada adcp

#cria datas com numeros inteiros (verificar se esta correto)
datani = np.array([[int(datan[i].strftime('%Y%m%d%H%M')) for i in range(len(datan))]]).T
data1i = np.array([[int(data1[i].strftime('%Y%m%d%H%M')) for i in range(len(data1))]]).T
data2i = np.array([[int(data2[i].strftime('%Y%m%d%H%M')) for i in range(len(data2))]]).T
data3i = np.array([[int(data3[i].strftime('%Y%m%d%H%M')) for i in range(len(data3))]]).T
data4i = np.array([[int(data4[i].strftime('%Y%m%d%H%M')) for i in range(len(data4))]]).T

anemo1 = np.concatenate((datani,anemo),axis=1)
dados1 = np.concatenate((data1i,adcp1),axis=1)
dados2 = np.concatenate((data2i,adcp2),axis=1)
dados3 = np.concatenate((data3i,adcp3),axis=1)
dados4 = np.concatenate((data4i,adcp4),axis=1)



#figuras
pl.figure(figsize=figsize1)
pl.subplot(311)
pl.plot(data1,adcp1[:,0],'b',data2,adcp2[:,0],'k',data3,adcp3[:,0],'r',data4,adcp4[:,0],'g')
pl.legend(['ADCP-1','ADCP-2','ADCP-3','ADCP-4'],fontsize=10), pl.grid('on')
pl.axis('tight'), pl.title('Hs'), pl.grid('on'), pl.xticks(visible=False)
pl.ylabel('metros')
pl.subplot(312)
pl.plot(data1,adcp1[:,6],'.b',data2,adcp2[:,6],'.k',data3,adcp3[:,6],'.r',data4,adcp4[:,6],'.g')
pl.axis('tight'), pl.title('Tp'), pl.grid('on'), pl.xticks(visible=False)
pl.ylabel('segundos')
pl.subplot(313)
pl.plot(data1,adcp1[:,3],'.b',data2,adcp2[:,3],'.k',data3,adcp3[:,3],'.r',data4,adcp4[:,3],'.g')
pl.axis('tight'), pl.title('Dp'), pl.grid('on')
pl.ylabel('graus')
pl.ylim((0,360))
pl.xticks(rotation=10)

pl.figure(figsize=figsize1)
pl.subplot(211)
pl.plot(datan[inip_anemo:fimp_anemo],anemo[inip_anemo:fimp_anemo,0],'b')
#pl.legend(['Int. Vento'],fontsize=10), pl.grid('on')
pl.axis('tight'), pl.title('Intensidade do Vento'), pl.grid('on'), pl.xticks(visible=False)
pl.ylabel('m/s')
pl.subplot(212)
pl.plot(datan[inip_anemo:fimp_anemo],anemo[inip_anemo:fimp_anemo,1],'.b') #,data1[inip_adcp:fimp_adcp],adcp1[inip_adcp:fimp_adcp,3],'.r')
pl.axis('tight'), pl.title('Direcao do Vento'), pl.grid('on')#, pl.xticks(visible=False)
pl.ylabel('graus')#, pl.legend(['Vento','Onda'])

#direcoes dos adcp e vento
pl.figure(figsize=figsize1)
pl.plot(datan[inip_anemo:fimp_anemo],anemo[inip_anemo:fimp_anemo,1],'.y',data1[inip_adcp:fimp_adcp],adcp1[inip_adcp:fimp_adcp,3],'.b',
	data2[inip_adcp:fimp_adcp],adcp2[inip_adcp:fimp_adcp,3],'.k',data3[inip_adcp:fimp_adcp],adcp3[inip_adcp:fimp_adcp,3],'.r',
	data4[inip_adcp:fimp_adcp],adcp4[inip_adcp:fimp_adcp,3],'.g')
pl.grid()
pl.ylim((0,360))
pl.ylabel('Dir. Vento/Onda (graus)')
pl.legend(['Vento','ADCP-1','ADCP-2','ADCP-3','ADCP-4'],fontsize=10)


################################################################################
#salva parametros de cada adcp
pathnameout = 'out/proc/parametros/'
np.savetxt(pathnameout+'anemo_vale.out',anemo1,delimiter=',',fmt=['%i']+2*['%.2f'],
    header='data, ws, wd')

np.savetxt(pathnameout+'adcp01_vale.out',dados1,delimiter=',',fmt=['%i']+8*['%.2f'],
    header='data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02')

np.savetxt(pathnameout+'adcp02_vale.out',dados2,delimiter=',',fmt=['%i']+8*['%.2f'],
    header='data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02')

np.savetxt(pathnameout+'adcp03_vale.out',dados3,delimiter=',',fmt=['%i']+8*['%.2f'],
    header='data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02')

np.savetxt(pathnameout+'adcp04_vale.out',dados4,delimiter=',',fmt=['%i']+8*['%.2f'],
    header='data, hm0, h10, hmax, dirtp, sprtp, meandir, tp, tm02')



pl.show()
