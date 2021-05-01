'''
Processamento dos dados de ADCP
que enviam dados em tempo real para
o site da Vale

LIOc - Laboratorio de Instrumentacao Oceanografica
Henrique P P Pereira
Izabel C M Nogueira
Isabel Cabral
Talitha Lourenco
Tamiris Alfama

Ultima modificacao: 14/08/2015
'''

import numpy as np
import os
from datetime import datetime
import pylab as pl
import xlrd

pl.close('all')

pathname_site = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/operacional/' 
pathname_ww3  = os.environ['HOME'] + '/Dropbox/ww3vale/TU/Previsao/Previsao_14maio/'
pathname_swan = os.environ['HOME'] + '/Dropbox/ww3vale/TU/Previsao/Previsao_14maio/'
pathname_mb = os.environ['HOME'] + '/Dropbox/pnboia/dados/B69150/' #planilha excel baixada do site da MB

#############################################################################
#carrega dados dos ADCPs baixados operacionalmente (site)

#adcp - boia 4 e 10
adcp04 = 'TU_boia04.out' #fora do porto (mais fundo)
adcp10 = 'TU_boia10.out' #dentro do porto

# 0      1      2     3         4        5    6   7   8 9
#data,bateria,rumo,pressao,temperatura,pitch,roll,hs,tp,dp
ddadcp04 = np.loadtxt(pathname_site + adcp04,delimiter=',')
ddadcp10 = np.loadtxt(pathname_site + adcp10,delimiter=',')

dataa04 = [ datetime.strptime(str(int(ddadcp04[i,0])), '%Y%m%d%H%M') for i in range(len(ddadcp04)) ]
dataa10 = [ datetime.strptime(str(int(ddadcp10[i,0])), '%Y%m%d%H%M') for i in range(len(ddadcp10)) ]

#############################################################################
#carrega parametros de ondas do SWAN
#ADCP 1, 2, 3 e 4

#  0    1     2       3       4        5        6       7       
#Time, Hsig, PkDir, RTpeak, X-Windv, Y-Windv, Hswell, Dspr
# [ ]   [m]  [degr]  [sec]     [m/s], [m/s],    [m],  [degr]

ddswn1 = np.loadtxt(pathname_swan + '/20150508/table_point_ADCP01.out',comments='%')
ddswn3 = np.loadtxt(pathname_swan + '/20150508/table_point_ADCP03.out',comments='%')

#data com datetime
datas1 = np.array([ datetime.strptime(str(ddswn1[i,0]*100),'%Y%m%d%H.0') for i in range(len(ddswn1)) ])
datas3 = np.array([ datetime.strptime(str(ddswn3[i,0]*100),'%Y%m%d%H.0') for i in range(len(ddswn3)) ])


#############################################################################
#carrega parametros de ondas do WW3
#Boias Axys do PNBOIA: Santos, Rio Grande e Florianopolis

#  0    1    2    3     4   5   6    7    8 
# ano, mes, dia, hora, min, hs, tp, dp , spr

#ww3 - um arquivo para cada dia de previsao
ddw = np.loadtxt(pathname_ww3 + '20150508/' + 'Boiasantos.txt')

#data e hora - ww3
dataw = [datetime(int(ddw[i,0]),int(ddw[i,1]),int(ddw[i,2]),int(ddw[i,3])) for i in range(len(ddw))]


#############################################################################
#carrega parametros de ondas do WW3
#Boias Axys do PNBOIA: Santos, Rio Grande e Florianopolis

local = 'Santos/SP - PNBOIA'
mesboia = 'B69150_2015053123.xls' #MAI_ARGOS_69150_Santos.xls'

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



#############################################################################
#figuras

# * fazer comparacao com com o ADCP 10 e ponto 03 do swan

#ADCP 4 x SWAN-ADCP 1
pl.figure()
pl.title('ADCP 4 x SWAN-ADCP 1')
pl.plot(dataa04,ddadcp04[:,7],'o',label='adcp-04')
pl.plot(datas1,ddswn1[:,1],'o',label='swan-01')
pl.legend()

#ADCP 10 x SWAN-ADCP 3
pl.figure()
pl.title('ADCP 10 x SWAN-ADCP 3')
pl.plot(dataa10,ddadcp10[:,7],'o',label='adcp-10')
pl.plot(datas3,ddswn3[:,1],'o',label='swan-03')
pl.legend()

##BMO Santos x WW3-Santos
pl.figure()
pl.title('BMO Santos x WW3-Santos')
pl.plot(dt1,dd1[:,7],'o',label='pnboia-santos')
pl.plot(dataw,ddw[:,5],'o',label='ww3-santos')
pl.legend()




pl.show()


















# #swan - previsao do dia 17 e 18
# ds10_17 = np.loadtxt(pathname_swn_10 + arqswn17, skiprows=7)
# ds10_18 = np.loadtxt(pathname_swn_10 + arqswn18, skiprows=7)
# ds10_19 = np.loadtxt(pathname_swn_10 + arqswn19, skiprows=7)

# #data e hora - swan
# #dia 17
# start = datetime.datetime(2015,02,17,00)
# fim = len(ds10_17) #24 horas
# datas10_17 = [start + datetime.timedelta(hours=i) for i in xrange(0,fim)]
# #dia 18
# start = datetime.datetime(2015,02,18,00)
# fim = len(ds10_18) #24 horas
# datas10_18 = [start + datetime.timedelta(hours=i) for i in xrange(0,fim)]
# #dia 19
# start = datetime.datetime(2015,02,19,00)
# fim = len(ds10_19) #24 horas
# datas10_19 = [start + datetime.timedelta(hours=i) for i in xrange(0,fim)]

# #adcp
# #inverte os dados e pega de hora em hora (pois os mais recentes estao nas primeiras linhas)
# #* pega os dados de hora em hora (modificar o inicio para cada arquivo)
# dd4 = np.flipud(dd4[0:-1:6,:])
# data4 = np.flipud(data4[0:-1:6,:])

# dd10 = np.flipud(dd10[0:-1:6,:])
# data10 = np.flipud(data10[0:-1:6,:])

# #cria datas em string
# datastr4 = data4
# datastr10 = data10

# #com erro, pois os arquivos mudam de dia na hora=23
# data4 = [datetime.datetime(int(data4[i,0][6:10]),int(data4[i,0][3:5]),int(data4[i,0][0:2]),
# 	int(data4[i,1][0:2]),int(data4[i,1][3:5])) for i in range(len(data4))]

# data10 = [datetime.datetime(int(data10[i,0][6:10]),int(data10[i,0][3:5]),int(data10[i,0][0:2]),
# 	int(data10[i,1][0:2]),int(data10[i,1][3:5])) for i in range(len(data10))]

# #corrige datas dos adcp (mudam um dia na hora 23)
# for i in range(len(data4)):
# 	if int(datastr4[i,1][0:2]) >= 23:
# 		data4[i] = data4[i] - datetime.timedelta(days=1)

# for i in range(len(data10)):
# 	if int(datastr10[i,1][0:2]) >= 23:
# 		data10[i] = data10[i] - datetime.timedelta(days=1)

# #coloca data dos adcp e utc (soma 3h)
# data4 = [data4[i] + datetime.timedelta(hours=3) for i in range(len(data4))]
# data10 = [data10[i] + datetime.timedelta(hours=3) for i in range(len(data10))]

# #define variaveis
# #adcp
# pr4, pit4, rol4, hs4, dp4, tp4 = dd4[:,0], dd4[:,1], dd4[:,2], dd4[:,3], dd4[:,4], dd4[:,5]
# pr10, pit10, rol10, hs10, dp10, tp10 = dd10[:,0], dd10[:,1], dd10[:,2], dd10[:,3], dd10[:,4], dd10[:,5]

# #ww3
# # hsw4_16, dpw4_16, tpw4_16 = dw4_16[:,5], dw4_16[:,7], dw4_16[:,6]
# hsw4_17, dpw4_17, tpw4_17 = dw4_17[:,5], dw4_17[:,7], dw4_17[:,6]
# hsw4_18, dpw4_18, tpw4_18 = dw4_18[:,5], dw4_18[:,7], dw4_18[:,6]
# hsw4_19, dpw4_19, tpw4_19 = dw4_19[:,5], dw4_19[:,7], dw4_19[:,6]
# hsw4_20, dpw4_20, tpw4_20 = dw4_20[:,5], dw4_20[:,7], dw4_20[:,6]
# hsw4_21, dpw4_21, tpw4_21 = dw4_21[:,5], dw4_21[:,7], dw4_21[:,6]

# #swan
# hss10_17, dps10_17, tps10_17 = ds10_17[:,0], ds10_17[:,1], ds10_17[:,2]
# hss10_18, dps10_18, tps10_18 = ds10_18[:,0], ds10_18[:,1], ds10_18[:,2]
# hss10_19, dps10_19, tps10_19 = ds10_19[:,0], ds10_19[:,1], ds10_19[:,2]

# pl.figure(figsize=figsize1) #compara modelo e adcp (boia 4)
# pl.subplot(311)
# pl.plot(dataw4_17,hsw4_17,'g-',dataw4_18,hsw4_18,'k-',dataw4_19,hsw4_19,'b-',dataw4_20,hsw4_20,'m-',dataw4_21,hsw4_21,'y-',data4,hs4,'ro')
# pl.title('Boia-04')
# pl.ylabel('Hs (m)'), pl.legend(['17','18','19','20','21'],fontsize=10)
# pl.axis([data4[-96],dataw4_19[-1],0.5,1.5])
# pl.grid()
# pl.xticks(visible=False)
# pl.subplot(312)
# pl.plot(dataw4_17,tpw4_17,'g-',dataw4_18,tpw4_18,'k-',dataw4_19,tpw4_19,'b-',dataw4_20,tpw4_20,'m-',dataw4_21,tpw4_21,'y-',data4,tp4,'ro')
# pl.ylabel('Tp (s)')
# pl.axis([data4[-96],dataw4_19[-1],4,10])
# pl.grid()
# pl.xticks(visible=False)
# pl.subplot(313)
# pl.plot(dataw4_17,dpw4_17,'g-',dataw4_18,dpw4_18,'k-',dataw4_19,dpw4_19,'b-',dataw4_20,dpw4_20,'m-',dataw4_21,dpw4_21,'y-',data4,dp4,'ro')
# pl.ylabel('Dp (graus)')
# pl.axis([data4[-96],dataw4_19[-1],0,360])
# pl.grid()

# pl.figure(figsize=figsize1) #compara modelo e adcp (boia 10)
# pl.subplot(311)
# pl.plot(datas10_17,hss10_17,'g-',datas10_18,hss10_18,'k-',datas10_19,hss10_19,'b-',data10,hs10,'ro')
# pl.title('Boia-10')
# pl.ylabel('Hs (m)'), pl.legend(['17','18','19'],fontsize=10)
# pl.axis([data10[-96],datas10_19[-1],0,1.2])
# pl.grid()
# pl.xticks(visible=False)
# pl.subplot(312)
# pl.plot(datas10_17,tps10_17,'g-',datas10_18,tps10_18,'k-',datas10_19,tps10_19,'b-',data10,tp10,'ro')
# pl.ylabel('Tp (s)')
# pl.axis([data10[-96],datas10_19[-1],5,14])
# pl.grid()
# pl.xticks(visible=False)
# pl.subplot(313)
# pl.plot(datas10_17,dps10_17,'g-',datas10_18,dps10_18,'k-',datas10_19,dps10_19,'b-',data10,dp10,'ro')
# pl.ylabel('Dp (graus)')
# pl.axis([data10[-96],datas10_19[-1],0,360])
# pl.grid()

# pl.figure() #comparacao b4 (fundo) e b10 (raso)
# pl.subplot(311)
# pl.plot(datas10_17,hss10_17,datas10_18,hss10_18,'-g',data4,hs4,'-b',data10,hs10,'-r')
# pl.legend(['SWN','B4','B10'])
# pl.grid()
# pl.xticks(visible=False)
# pl.subplot(312)
# pl.plot(datas10_17,tps10_17,datas10_18,tps10_18,'-g',data4,tp4,'.b',data10,tp10,'.r')
# pl.grid()
# pl.xticks(visible=False)
# pl.subplot(313)
# pl.plot(datas10_17,dps10_17,datas10_18,dps10_18,'-g',data4,dp4,'.b',data10,dp10,'.r')
# pl.ylim(0,360),pl.grid()

# pl.figure()
# pl.plot(dataw4_17,hsw4_17,'m-',dataw4_18,hsw4_18,'g-',dataw4_19,hsw4_19,'b-',data4,hs4,'ro')
# leg1 = pl.legend(['Prev 17','Prev 18','Prev 19','Boia-4'],loc=1)
# pl.gca().add_artist(leg1)
# pl.plot(datas10_17,hss10_17,'m-',datas10_18,hss10_18,'g-',datas10_19,hss10_19,'b-',data10,hs10,'or')
# leg2 = pl.legend(['Prev 17','Prev 18','Prev 19','Boia-10'],loc=4)
# pl.grid()
# pl.axis([data4[-96],dataw4_19[-1],0,1.5])
# pl.ylabel('Hs (m)')

# pl.figure() #pitch e roll das 2 boias
# pl.subplot(211)
# pl.plot(data4,pit4,'b-'), pl.legend(['pitch'],loc=6), pl.ylabel('pitch (graus)'), pl.grid()
# pl.twinx()
# pl.plot(data4,rol4,'r-'), pl.legend(['roll'],loc=5), pl.ylabel('roll (graus)')
# pl.title('Boia 4')
# pl.subplot(212)
# pl.plot(data10,pit10,'b-'), pl.legend(['pitch'],loc=6), pl.ylabel('pitch (graus)'), pl.grid()
# pl.twinx()
# pl.plot(data10,rol10,'r-'), pl.legend(['roll'],loc=5), pl.ylabel('roll (graus)')
# pl.title('Boia 10')

# # mare
# pl.figure() #mare
# pl.subplot(211)
# pl.plot(data4,pr4)
# pl.subplot(212)
# pl.plot(data10,pr10)

# pl.show()









