'''
baixar e processsar os dados do PNBOIA
enviado via sistema argos e disponibilizado
no site da marinha
mar.mil/dados/pnboia

LIOc - Laboratorio de Instrumentacao Oceanografica
Henrique P P Pereira
Izabel C M Nogueira
Isabel Cabral
Talitha Lourenco
Tamiris Alfama

Ultima modificacao: 14/08/2015

Observacoes:
Os dados baixados manualmente estao na pasta
/rot/opendap

verificar se da para baixar a partir desse endereco (idem infowaves)
https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/MAI_ARGOS_69008_Recife.xls
https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/JUL_ARGOS_69153_RioGrande.xls
'''

import numpy as np
import os
import xlrd
from datetime import datetime
import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
import matplotlib.pylab as pl


pl.close('all')

#local de onde estao os dados em xls baixados do site da marinha
pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/'


#############################################################################

local = 'Santos/SP - PNBOIA'
#mesboia = 'MAI_ARGOS_69150_Santos.xls'
mesboia = np.sort(os.listdir(pathname+'/B69150'))[-1]

workbook = xlrd.open_workbook(pathname + 'B69150/' + mesboia)

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

#retira linhas com datas igual a nan
dd0 = dd0[pl.find(dd0[:,1]<>u'nan'),:]
dd1 = dd1[pl.find(dd1[:,1]<>u'nan'),:]

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
#mesboia = 'MAI_ARGOS_69152_SantaCatarina.xls'
mesboia = np.sort(os.listdir(pathname+'/B69152'))[-1]

workbook = xlrd.open_workbook(pathname + 'B69152/' + mesboia)

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

#retira linhas com datas igual a nan
dd0 = dd0[pl.find(dd0[:,1]<>u'nan'),:]
dd1 = dd1[pl.find(dd1[:,1]<>u'nan'),:]

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
#mesboia = 'MAI_ARGOS_69153_RioGrande.xls'
mesboia = np.sort(os.listdir(pathname+'/B69153'))[-1]

workbook = xlrd.open_workbook(pathname + 'B69153/' + mesboia)

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

#retira os dados iniciais que estao com erros (neste caso finais pq ta com flipud)
dd1 = dd1[:-8,:]

#substitui 'xxxx' por nan
dd0[np.where(dd0=='xxxx')] = np.nan
dd1[np.where(dd1=='xxxx')] = np.nan
dd1[np.where(dd1=='')] = np.nan

#retira linhas com datas igual a nan
dd0 = dd0[pl.find(dd0[:,1]<>u'nan'),:]
dd1 = dd1[pl.find(dd1[:,1]<>u'nan'),:]

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

pathname_site = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/operacional/' 

#adcp - boia 4 e 10
adcp04 = 'TU_boia04.out' #dentro do porto
adcp10 = 'TU_boia10.out' #dentro do porto

# 0      1      2     3         4        5    6   7   8 9
#data,bateria,rumo,pressao,temperatura,pitch,roll,hs,tp,dp
ddadcp04 = np.loadtxt(pathname_site + adcp04,delimiter=',')
ddadcp10 = np.loadtxt(pathname_site + adcp10,delimiter=',')

#retira os valores repetidos
aux, ind = np.unique(ddadcp04[:,0], return_index=True)
ddadcp04 = ddadcp04[ind,:]
aux, ind = np.unique(ddadcp10[:,0], return_index=True)
ddadcp10 = ddadcp10[ind,:]


dataa04 = [ datetime.strptime(str(int(ddadcp04[i,0])), '%Y%m%d%H%M') for i in range(len(ddadcp04)) ]
dataa10 = [ datetime.strptime(str(int(ddadcp10[i,0])), '%Y%m%d%H%M') for i in range(len(ddadcp10)) ]

#tamanho da janela para plotagem
tj = 7 * 24

pl.figure(figsize=(16,9))
pl.subplot(311)
pl.title('Ondas TU')
pl.plot(dt1_rg,hs_rg,'b',label='Rio Grande')
pl.plot(dt1_fl,hs_fl,'r',label='Florian')
pl.plot(dt1_sa,hs_sa,'g',label='Santos')
pl.plot(dataa04,ddadcp04[:,7],'om',label='ADCP04')
pl.plot(dataa10,ddadcp10[:,7],'ok',label='ADCP10')
pl.xlim(dataa10[-tj],dataa10[-1]), pl.ylim(0.5,6), pl.grid()
pl.ylabel('Hs (m)')
pl.legend(loc=2,ncol=2,fontsize=10)
pl.xticks(visible=False)

pl.subplot(312)
pl.plot(dt1_rg,tp_rg,'b',label='Rio Grande')
pl.plot(dt1_fl,tp_fl,'r',label='Florian')
pl.plot(dt1_sa,tp_sa,'g',label='Santos')
pl.plot(dataa04,ddadcp04[:,8],'om',label='ADCP04')
pl.plot(dataa10,ddadcp10[:,8],'ok',label='ADCP10')
pl.xlim(dataa10[-tj],dataa10[-1]), pl.ylim(2,20), pl.grid()
pl.ylabel('Tp (s)')
pl.xticks(visible=False)

pl.subplot(313)
pl.plot(dt1_rg,dp_rg,'b',label='Rio Grande')
pl.plot(dt1_fl,dp_fl,'r',label='Florian')
pl.plot(dt1_sa,dp_sa,'g',label='Santos')
pl.plot(dataa04,ddadcp04[:,9],'om',label='ADCP04')
pl.plot(dataa10,ddadcp10[:,9],'ok',label='ADCP10')
pl.xlim(dataa10[-tj],dataa10[-1]), pl.ylim(0,360), pl.grid()
pl.yticks(np.arange(0,361,45))
pl.ylabel('Dp (graus)')

pl.savefig(os.environ['HOME'] + '/Dropbox/ww3vale/TU/reports/report_TU_' + datetime.now().strftime('%Y%m%d%H') + '.png')

pl.show()

