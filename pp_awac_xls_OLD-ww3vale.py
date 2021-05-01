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

# pl.close('all')

#pathname = os.environ['HOME'] + 'C:Users/Cliente/Dropbox/ww3vale/Geral/TU/dados/Planilhas_Processadas/'
pathname = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/dados/ADCP/proc_lioc/Planilhas/xls/'

#Open an Excel workbook 
workbook = xlrd.open_workbook(pathname + 'PTU_campanha_04.xls')

#imprime nome das planilhas
# print workbook.sheet_names()

#seleciona planilha por indice (pode ser por nome tbm)
sheet_0 = workbook.sheet_by_index(0) #anemometro
sheet_3 = workbook.sheet_by_index(3) #adcp-1
sheet_5 = workbook.sheet_by_index(5) #adcp-2
sheet_7 = workbook.sheet_by_index(7) #adcp-3
sheet_9 = workbook.sheet_by_index(9) #adcp-4

#pega os valores das celulas selecionadas
#  0     1    2     3      4     5      6      7    8
# data, hm0, h10, hmax, dirtp, SprTp, MeanDir, Tp, Tm02
onda1 = np.array([[sheet_3.cell_value(r,c) for r in range(22,sheet_3.nrows)] for c in range(1,sheet_3.ncols)]).T
onda2 = np.array([[sheet_5.cell_value(r,c) for r in range(22,sheet_5.nrows)] for c in range(1,sheet_5.ncols)]).T
onda3 = np.array([[sheet_7.cell_value(r,c) for r in range(22,sheet_7.nrows)] for c in range(1,sheet_7.ncols)]).T
onda4 = np.array([[sheet_9.cell_value(r,c) for r in range(23,sheet_9.nrows)] for c in range(1,sheet_9.ncols)]).T

#consistencia
#coloca nan no lugar de 999
onda1[np.where(onda1==999)] = np.nan
onda2[np.where(onda2==999)] = np.nan
onda3[np.where(onda3==999)] = np.nan
onda4[np.where(onda4==999)] = np.nan

#datas
start = datetime.datetime(2013,01,20,00)
fim = onda4.shape[0]
data=np.array([start + datetime.timedelta(hours=i) for i in xrange(fim)])

#figuras

# pl.figure()
# pl.plot(onda1[:,0],onda1[:,1],'ob',onda2[:,0],onda2[:,1],'ok',onda3[:,0],onda3[:,1],'or',onda4[:,0],onda4[:,1],'og')
# pl.legend(['ADCP-1','ADCP-2','ADCP-3','ADCP-4']), pl.axis('tight')
# pl.title('Hm0'), pl.xlabel('Dias julianos'), pl.ylabel('metros')

# pl.figure()
# pl.plot(onda1[:,0],onda1[:,7],'ob',onda2[:,0],onda2[:,7],'ok',onda3[:,0],onda3[:,7],'or',onda4[:,0],onda4[:,7],'og')
# pl.legend(['ADCP-1','ADCP-2','ADCP-3','ADCP-4']), pl.axis('tight')
# pl.title('Tp'), pl.xlabel('Dias julianos'), pl.ylabel('segundos')

# pl.figure()
# pl.plot(onda1[:,0],onda1[:,4],'ob',onda2[:,0],onda2[:,4],'ok',onda3[:,0],onda3[:,4],'or',onda4[:,0],onda4[:,4],'og')
# pl.legend(['ADCP-1','ADCP-2','ADCP-3','ADCP-4']), pl.axis('tight')
# pl.title('DirTp'), pl.xlabel('Dias julianos'), pl.ylabel('graus')



pl.figure()
pl.subplot(311)
pl.plot(data,onda1[:fim,1],'b',data,onda2[:fim,1],'k',data,onda3[:fim,1],'r',data,onda4[:,1],'g')
pl.legend(['ADCP-1','ADCP-2','ADCP-3','ADCP-4'],fontsize=10), pl.grid('on')
pl.axis('tight'), pl.title('Hm0'), pl.grid('on'), pl.xticks(visible=False)
pl.ylabel('metros')
pl.subplot(312)
pl.plot(data,onda1[:fim,7],'.b',data,onda2[:fim,7],'.k',data,onda3[:fim,7],'.r',data,onda4[:fim,7],'.g')
pl.axis('tight'), pl.title('Tp'), pl.grid('on'), pl.xticks(visible=False)
pl.ylabel('segundos')
pl.subplot(313)
pl.plot(data,onda1[:fim,4],'.b',data,onda2[:fim,4],'.k',data,onda3[:fim,4],'.r',data,onda4[:fim,4],'.g')
pl.axis('tight'), pl.title('DirTp'), pl.grid('on')
pl.xlabel('Dias julianos')
pl.ylabel('graus')



pl.show()

