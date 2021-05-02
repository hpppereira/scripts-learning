''' pega dados do maregrafo e ajusta para 1hora

'''

import numpy as np
import matplotlib.pylab as pl
import os
from datetime import *
import xlrd

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/proc_vale/Planilhas/xls/'
pathadcp = 'PTU_campanha_01.xls'

workbook = xlrd.open_workbook(pathname + pathadcp)
sheet_1 = workbook.sheet_by_index(1) #maregrafo

#nivel 0 - data; nivel 1 - nivel bruto; nivel 2 - nivel referenciado
nivel = np.array([[sheet_1.cell_value(r,c) for r in range(18,sheet_1.nrows)] for c in range(1,sheet_1.ncols)]).T
nivel[np.where(nivel[:,2]>5),2] = np.nan;
nivel[np.where(nivel[:,2]<0),2] = np.nan;
data= [datetime(*xlrd.xldate_as_tuple(nivel[i,0],workbook.datemode)) for i in range(len(nivel))]

# juntando para escrever um unico arquivo
datas = np.array([[int(data[i].strftime('%Y%m%d%H')) for i in range(len(data))]]).T
nivel1=np.concatenate((datas[577:-1],nivel[577:-1,1:3]),axis=1) # pegando somente fev

# tirando os valores medidos de 30 em 30 min 
aux,index=np.unique(datas[577:-1],return_index=True)
nivel1=nivel1[index,:]

pl.figure()
pl.plot(data,nivel[:,2])
pl.ylim([-0.5,2])
pl.show()


out=file('out/nivel201302.txt','w')
out.write('#nivel de 1 em 1 hora')
out.write('\n')
np.savetxt(out,nivel1,fmt=['%i']+2*['%.2f'],delimiter=',')
out.close

