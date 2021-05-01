'''
programa principal para leitura dos dados de ADCP nas
planilhas em excel do porto de tubarao

- arrumar as datas

'''

import xlrd
import os
import numpy as np
from matplotlib import pylab as pl
import datetime

pl.close('all')

#campanha a ser processada (1 a 13)
camp = 13

#opcoes das plotagens
# lsf = 18 #fontsize para as figuras
figsize1 = (15,9)

camp = str(camp).zfill(2)

#pathname = os.environ['HOME'] + 'C:Users/Cliente/Dropbox/ww3vale/Geral/TU/dados/Planilhas_Processadas/'
pathname = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/dados/ADCP/proc_vale/Planilhas/xls/'

#Open an Excel workbook 
workbook = xlrd.open_workbook(pathname + 'PTU_campanha_' + camp + '.xls')

#imprime nome das planilhas
# print workbook.sheet_names()

#seleciona planilha por indice (pode ser por nome tbm)
sheet_0 = workbook.sheet_by_index(0) #anemometro
sheet_3 = workbook.sheet_by_index(5) #adcp-1
sheet_5 = workbook.sheet_by_index(9) #adcp-2
sheet_7 = workbook.sheet_by_index(13) #adcp-3
sheet_9 = workbook.sheet_by_index(17) #adcp-4

#pega os valores das celulas selecionadas
#  0    1    2     3      4     5      6      7    8
# data hm0, h10, hmax, dirtp, SprTp, MeanDir, Tp, Tm02
onda1 = np.array([[sheet_3.cell_value(r,c) for r in range(22,sheet_3.nrows)] for c in range(1,sheet_3.ncols)]).T
onda2 = np.array([[sheet_5.cell_value(r,c) for r in range(22,sheet_5.nrows)] for c in range(1,sheet_5.ncols)]).T
onda3 = np.array([[sheet_7.cell_value(r,c) for r in range(22,sheet_7.nrows)] for c in range(1,sheet_7.ncols)]).T
onda4 = np.array([[sheet_9.cell_value(r,c) for r in range(23,sheet_9.nrows)] for c in range(1,sheet_9.ncols)]).T

#data com datetime
data1 = [datetime.datetime(*xlrd.xldate_as_tuple(onda1[i,0],workbook.datemode)) for i in range(len(onda1))]
data2 = [datetime.datetime(*xlrd.xldate_as_tuple(onda2[i,0],workbook.datemode)) for i in range(len(onda2))]
data3 = [datetime.datetime(*xlrd.xldate_as_tuple(onda3[i,0],workbook.datemode)) for i in range(len(onda3))]
data4 = [datetime.datetime(*xlrd.xldate_as_tuple(onda4[i,0],workbook.datemode)) for i in range(len(onda4))]

#  0     1    2     3      4     5        6   7
# hm0, h10, hmax, dirtp, SprTp, MeanDir, Tp, Tm02
onda1 = onda1[:,1:]
onda2 = onda2[:,1:]
onda3 = onda3[:,1:]
onda4 = onda4[:,1:]

#consistencia
#coloca nan no lugar de 999
onda1[np.where(onda1==999)] = np.nan
onda2[np.where(onda2==999)] = np.nan
onda3[np.where(onda3==999)] = np.nan
onda4[np.where(onda4==999)] = np.nan

pl.figure(figsize=figsize1)
pl.subplot(311)
pl.plot(data1,onda1[:,0],'b',data2,onda2[:,0],'k',data3,onda3[:,0],'r',data4,onda4[:,0],'g')
pl.legend(['ADCP-1','ADCP-2','ADCP-3','ADCP-4'],fontsize=10), pl.grid('on')
pl.axis('tight'), pl.title('Hm0'), pl.grid('on'), pl.xticks(visible=False)
pl.ylabel('metros')
pl.subplot(312)
pl.plot(data1,onda1[:,6],'.b',data2,onda2[:,6],'.k',data3,onda3[:,6],'.r',data4,onda4[:,6],'.g')
pl.axis('tight'), pl.title('Tp'), pl.grid('on'), pl.xticks(visible=False)
pl.ylabel('segundos')
pl.subplot(313)
pl.plot(data1,onda1[:,3],'.b',data2,onda2[:,3],'.k',data3,onda3[:,3],'.r',data4,onda4[:,3],'.g')
pl.axis('tight'), pl.title('DirTp'), pl.grid('on')
pl.ylabel('graus')
pl.ylim((0,360))
pl.xticks(rotation=10)

pl.savefig('saida/HsTpDp_camp' + camp)


pl.show()