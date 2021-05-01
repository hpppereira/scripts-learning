'''
baixar e processsar os dados do PNBOIA
enviado via sistema argos e disponibilizado
no site da marinha
mar.mil/dados/pnboia

Os dados baixados manualmente estao na pasta
/rot/opendap

'''


## verificar se da para baixar a partir desse endereco (idem infowaves)
## https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/MAI_ARGOS_69008_Recife.xls
## https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/JUL_ARGOS_69153_RioGrande.xls


import numpy as np
import matplotlib.pylab as pl
import os
import xlrd
from datetime import datetime

pl.close('all')

#local de onde estao os dados em xls baixados do site da marinha
pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/mb/'


#############################################################################

local = 'Santos/SP - PNBOIA'
mesboia = 'MAI_ARGOS_69150_Santos.xls'

workbook = xlrd.open_workbook(pathname + mesboia)

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


#data com datetime (nao sao iguais as datas das duas planilhas- deveria ser..)
dt0 = np.array([ datetime.strptime(dd0[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd0)) ])
dt1_sa = np.array([ datetime.strptime(dd1[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd1)) ])

#dados da planilha 1 - dd1
# 7     8   9  10
# hs, hmax, tp dp

#define parametros
hs_sa, hmax_sa, tp_sa, dp_sa = dd1[:,[7,8,9,10]].T

#############################################################################


local = 'Florianopolis/SC - PNBOIA'
mesboia = 'MAI_ARGOS_69152_SantaCatarina.xls'

workbook = xlrd.open_workbook(pathname + mesboia)

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


#data com datetime (nao sao iguais as datas das duas planilhas- deveria ser..)
dt0 = np.array([ datetime.strptime(dd0[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd0)) ])
dt1_fl = np.array([ datetime.strptime(dd1[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd1)) ])

#dados da planilha 1 - dd1
# 7     8   9  10
# hs, hmax, tp dp

#define parametros
hs_fl, hmax_fl, tp_fl, dp_fl = dd1[:,[7,8,9,10]].T

#############################################################################


local = 'Rio Grande/RS - PNBOIA'
mesboia = 'MAI_ARGOS_69153_RioGrande.xls'

workbook = xlrd.open_workbook(pathname + mesboia)

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


#data com datetime (nao sao iguais as datas das duas planilhas- deveria ser..)
dt0 = np.array([ datetime.strptime(dd0[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd0)) ])
dt1_rg = np.array([ datetime.strptime(dd1[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd1)) ])

#dados da planilha 1 - dd1
# 7     8   9  10
# hs, hmax, tp dp

#define parametros
hs_rg, hmax_rg, tp_rg, dp_rg = dd1[:,[7,8,9,10]].T


#############################################################################
#carrega dados dos ADCPs baixados operacionalmente (site)

pathname_site = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/dados/ADCP/operacional/' 

#adcp - boia 4 e 10
adcp10 = 'TU_boia10.out' #dentro do porto

# 0      1      2     3         4        5    6   7   8 9
#data,bateria,rumo,pressao,temperatura,pitch,roll,hs,tp,dp
ddadcp10 = np.loadtxt(pathname_site + adcp10,delimiter=',')

dataa10 = [ datetime.strptime(str(int(ddadcp10[i,0])), '%Y%m%d%H%M') for i in range(len(ddadcp10)) ]


pl.figure(figsize=(16,9))
pl.title('BMOs (PNBOIA) e ADCP10 (TU) - Altura Sig.')
pl.plot(dt1_rg,hs_rg,'b',label='Rio Grande')
pl.plot(dt1_fl,hs_fl,'r',label='Florian')
pl.plot(dt1_sa,hs_sa,'g',label='Santos')
pl.ylabel('BMOs - Hs (m)')
pl.legend(loc=2)
pl.grid()
pl.ylim(0,8)
pl.twinx()
pl.plot(dataa10,ddadcp10[:,7],'.k',label='TU')
pl.ylim(0,3)
pl.ylabel('ADCP 10 - Hs (m)')
pl.legend()

# pl.subplot(312)
# pl.plot(dt1_rg,tp_rg,'.b')
# pl.xticks(visible=False), pl.grid()
# pl.ylabel('Tp (s)'), pl.ylim(0,20)
# pl.subplot(313)
# pl.plot(dt1,dp,'.b')
# pl.xticks(visible=True), pl.grid()
# pl.ylabel('Dp (graus)'), pl.ylim(0,360)


pl.show()

