'''
Processamento dos dados de ADCP
que enviam dados em tempo real para
o site da Vale

Laboratorio de Instrumentacao Oceanografica - LIOc
Data da ultima modificacao: 18/02/2015
'''

import numpy as np
import os
import datetime
import pylab as pl

pl.close('all')
figsize1 = (15,9)


pathname_adcp = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/dados/ADCP/site_vale/' #dados
pathname_ww3_4 = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/Resultados_Previsao_RT1/boia4/ww3/' #b4-ww3
pathname_swn_10 = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/Resultados_Previsao_RT1/boia10/swan/'

#nome dos arquivos
#adcp - boia 4 e 10
adcp4 = 'vale_boia4.txt'
adcp10 = 'vale_boia10.txt'

#ww3
arqww3 = 'pointparameters_050.txt'

#swan
arqswn17 = 'table_point_BES20150217.out'
arqswn18 = 'table_point_BES20150218.out'
arqswn19 = 'table_point_BES20150219.out' #modificar para o dia 19

#carrega dados
#adcp - boia 4 e 10 (press, pitch, roll, hs, dp, tp)
dd4 = np.loadtxt(pathname_adcp + adcp4,skiprows=1,usecols=(4,6,7,8,9,10),dtype=float,unpack=False)
dd10 = np.loadtxt(pathname_adcp + adcp10,skiprows=1,usecols=(4,6,7,8,9,10),dtype=float,unpack=False)

#data e hora - adcp
data4 = np.loadtxt(pathname_adcp + adcp4 ,skiprows=1,usecols=(0,1),dtype=str) #boia 4
data10 = np.loadtxt(pathname_adcp + adcp10 ,skiprows=1,usecols=(0,1),dtype=str) #boia 10

#ww3 - previsao dos dias 16, 17, 18 e 19
# dw4_16 = np.loadtxt(pathname_ww3_4 + '20150216/' + arqww3,skiprows=2)
dw4_17 = np.loadtxt(pathname_ww3_4 + '20150217/' + arqww3,skiprows=2)
dw4_18 = np.loadtxt(pathname_ww3_4 + '20150218/' + arqww3,skiprows=2)
dw4_19 = np.loadtxt(pathname_ww3_4 + '20150219/' + arqww3,skiprows=2)
dw4_20 = np.loadtxt(pathname_ww3_4 + '20150220/' + arqww3,skiprows=2)
dw4_21 = np.loadtxt(pathname_ww3_4 + '20150221/' + arqww3,skiprows=2)


#data e hora - ww3
# dataw4_16 = [datetime.datetime(int(dw4_16[i,0]),int(dw4_16[i,1]),int(dw4_16[i,2]),int(dw4_16[i,3])) for i in range(len(dw4_16))]
dataw4_17 = [datetime.datetime(int(dw4_17[i,0]),int(dw4_17[i,1]),int(dw4_17[i,2]),int(dw4_17[i,3])) for i in range(len(dw4_17))]
dataw4_18 = [datetime.datetime(int(dw4_18[i,0]),int(dw4_18[i,1]),int(dw4_18[i,2]),int(dw4_18[i,3])) for i in range(len(dw4_18))]
dataw4_19 = [datetime.datetime(int(dw4_19[i,0]),int(dw4_19[i,1]),int(dw4_19[i,2]),int(dw4_19[i,3])) for i in range(len(dw4_19))]
dataw4_20 = [datetime.datetime(int(dw4_20[i,0]),int(dw4_20[i,1]),int(dw4_20[i,2]),int(dw4_20[i,3])) for i in range(len(dw4_20))]
dataw4_21 = [datetime.datetime(int(dw4_21[i,0]),int(dw4_21[i,1]),int(dw4_21[i,2]),int(dw4_21[i,3])) for i in range(len(dw4_21))]


#swan - previsao do dia 17 e 18
ds10_17 = np.loadtxt(pathname_swn_10 + arqswn17, skiprows=7)
ds10_18 = np.loadtxt(pathname_swn_10 + arqswn18, skiprows=7)
ds10_19 = np.loadtxt(pathname_swn_10 + arqswn19, skiprows=7)

#data e hora - swan
#dia 17
start = datetime.datetime(2015,02,17,00)
fim = len(ds10_17) #24 horas
datas10_17 = [start + datetime.timedelta(hours=i) for i in xrange(0,fim)]
#dia 18
start = datetime.datetime(2015,02,18,00)
fim = len(ds10_18) #24 horas
datas10_18 = [start + datetime.timedelta(hours=i) for i in xrange(0,fim)]
#dia 19
start = datetime.datetime(2015,02,19,00)
fim = len(ds10_19) #24 horas
datas10_19 = [start + datetime.timedelta(hours=i) for i in xrange(0,fim)]

#adcp
#inverte os dados e pega de hora em hora (pois os mais recentes estao nas primeiras linhas)
#* pega os dados de hora em hora (modificar o inicio para cada arquivo)
dd4 = np.flipud(dd4[0:-1:6,:])
data4 = np.flipud(data4[0:-1:6,:])

dd10 = np.flipud(dd10[0:-1:6,:])
data10 = np.flipud(data10[0:-1:6,:])

#cria datas em string
datastr4 = data4
datastr10 = data10

#com erro, pois os arquivos mudam de dia na hora=23
data4 = [datetime.datetime(int(data4[i,0][6:10]),int(data4[i,0][3:5]),int(data4[i,0][0:2]),
	int(data4[i,1][0:2]),int(data4[i,1][3:5])) for i in range(len(data4))]

data10 = [datetime.datetime(int(data10[i,0][6:10]),int(data10[i,0][3:5]),int(data10[i,0][0:2]),
	int(data10[i,1][0:2]),int(data10[i,1][3:5])) for i in range(len(data10))]

#corrige datas dos adcp (mudam um dia na hora 23)
for i in range(len(data4)):
	if int(datastr4[i,1][0:2]) >= 23:
		data4[i] = data4[i] - datetime.timedelta(days=1)

for i in range(len(data10)):
	if int(datastr10[i,1][0:2]) >= 23:
		data10[i] = data10[i] - datetime.timedelta(days=1)

#coloca data dos adcp e utc (soma 3h)
data4 = [data4[i] + datetime.timedelta(hours=3) for i in range(len(data4))]
data10 = [data10[i] + datetime.timedelta(hours=3) for i in range(len(data10))]

#define variaveis
#adcp
pr4, pit4, rol4, hs4, dp4, tp4 = dd4[:,0], dd4[:,1], dd4[:,2], dd4[:,3], dd4[:,4], dd4[:,5]
pr10, pit10, rol10, hs10, dp10, tp10 = dd10[:,0], dd10[:,1], dd10[:,2], dd10[:,3], dd10[:,4], dd10[:,5]

#ww3
# hsw4_16, dpw4_16, tpw4_16 = dw4_16[:,5], dw4_16[:,7], dw4_16[:,6]
hsw4_17, dpw4_17, tpw4_17 = dw4_17[:,5], dw4_17[:,7], dw4_17[:,6]
hsw4_18, dpw4_18, tpw4_18 = dw4_18[:,5], dw4_18[:,7], dw4_18[:,6]
hsw4_19, dpw4_19, tpw4_19 = dw4_19[:,5], dw4_19[:,7], dw4_19[:,6]
hsw4_20, dpw4_20, tpw4_20 = dw4_20[:,5], dw4_20[:,7], dw4_20[:,6]
hsw4_21, dpw4_21, tpw4_21 = dw4_21[:,5], dw4_21[:,7], dw4_21[:,6]

#swan
hss10_17, dps10_17, tps10_17 = ds10_17[:,0], ds10_17[:,1], ds10_17[:,2]
hss10_18, dps10_18, tps10_18 = ds10_18[:,0], ds10_18[:,1], ds10_18[:,2]
hss10_19, dps10_19, tps10_19 = ds10_19[:,0], ds10_19[:,1], ds10_19[:,2]

pl.figure(figsize=figsize1) #compara modelo e adcp (boia 4)
pl.subplot(311)
pl.plot(dataw4_17,hsw4_17,'g-',dataw4_18,hsw4_18,'k-',dataw4_19,hsw4_19,'b-',dataw4_20,hsw4_20,'m-',dataw4_21,hsw4_21,'y-',data4,hs4,'ro')
pl.title('Boia-04')
pl.ylabel('Hs (m)'), pl.legend(['17','18','19','20','21'],fontsize=10)
pl.axis([data4[-96],dataw4_19[-1],0.5,1.5])
pl.grid()
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(dataw4_17,tpw4_17,'g-',dataw4_18,tpw4_18,'k-',dataw4_19,tpw4_19,'b-',dataw4_20,tpw4_20,'m-',dataw4_21,tpw4_21,'y-',data4,tp4,'ro')
pl.ylabel('Tp (s)')
pl.axis([data4[-96],dataw4_19[-1],4,10])
pl.grid()
pl.xticks(visible=False)
pl.subplot(313)
pl.plot(dataw4_17,dpw4_17,'g-',dataw4_18,dpw4_18,'k-',dataw4_19,dpw4_19,'b-',dataw4_20,dpw4_20,'m-',dataw4_21,dpw4_21,'y-',data4,dp4,'ro')
pl.ylabel('Dp (graus)')
pl.axis([data4[-96],dataw4_19[-1],0,360])
pl.grid()

pl.figure(figsize=figsize1) #compara modelo e adcp (boia 10)
pl.subplot(311)
pl.plot(datas10_17,hss10_17,'g-',datas10_18,hss10_18,'k-',datas10_19,hss10_19,'b-',data10,hs10,'ro')
pl.title('Boia-10')
pl.ylabel('Hs (m)'), pl.legend(['17','18','19'],fontsize=10)
pl.axis([data10[-96],datas10_19[-1],0,1.2])
pl.grid()
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(datas10_17,tps10_17,'g-',datas10_18,tps10_18,'k-',datas10_19,tps10_19,'b-',data10,tp10,'ro')
pl.ylabel('Tp (s)')
pl.axis([data10[-96],datas10_19[-1],5,14])
pl.grid()
pl.xticks(visible=False)
pl.subplot(313)
pl.plot(datas10_17,dps10_17,'g-',datas10_18,dps10_18,'k-',datas10_19,dps10_19,'b-',data10,dp10,'ro')
pl.ylabel('Dp (graus)')
pl.axis([data10[-96],datas10_19[-1],0,360])
pl.grid()

pl.figure() #comparacao b4 (fundo) e b10 (raso)
pl.subplot(311)
pl.plot(datas10_17,hss10_17,datas10_18,hss10_18,'-g',data4,hs4,'-b',data10,hs10,'-r')
pl.legend(['SWN','B4','B10'])
pl.grid()
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(datas10_17,tps10_17,datas10_18,tps10_18,'-g',data4,tp4,'.b',data10,tp10,'.r')
pl.grid()
pl.xticks(visible=False)
pl.subplot(313)
pl.plot(datas10_17,dps10_17,datas10_18,dps10_18,'-g',data4,dp4,'.b',data10,dp10,'.r')
pl.ylim(0,360),pl.grid()

pl.figure()
pl.plot(dataw4_17,hsw4_17,'m-',dataw4_18,hsw4_18,'g-',dataw4_19,hsw4_19,'b-',data4,hs4,'ro')
leg1 = pl.legend(['Prev 17','Prev 18','Prev 19','Boia-4'],loc=1)
pl.gca().add_artist(leg1)
pl.plot(datas10_17,hss10_17,'m-',datas10_18,hss10_18,'g-',datas10_19,hss10_19,'b-',data10,hs10,'or')
leg2 = pl.legend(['Prev 17','Prev 18','Prev 19','Boia-10'],loc=4)
pl.grid()
pl.axis([data4[-96],dataw4_19[-1],0,1.5])
pl.ylabel('Hs (m)')

pl.figure() #pitch e roll das 2 boias
pl.subplot(211)
pl.plot(data4,pit4,'b-'), pl.legend(['pitch'],loc=6), pl.ylabel('pitch (graus)'), pl.grid()
pl.twinx()
pl.plot(data4,rol4,'r-'), pl.legend(['roll'],loc=5), pl.ylabel('roll (graus)')
pl.title('Boia 4')
pl.subplot(212)
pl.plot(data10,pit10,'b-'), pl.legend(['pitch'],loc=6), pl.ylabel('pitch (graus)'), pl.grid()
pl.twinx()
pl.plot(data10,rol10,'r-'), pl.legend(['roll'],loc=5), pl.ylabel('roll (graus)')
pl.title('Boia 10')

# mare
pl.figure() #mare
pl.subplot(211)
pl.plot(data4,pr4)
pl.subplot(212)
pl.plot(data10,pr10)

pl.show()









