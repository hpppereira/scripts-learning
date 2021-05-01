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
import datetime as dt
import datetime
import pylab as pl

pl.close('all')
figsize1 = (15,9)


pathname_adcp = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/operacional/' #dados
pathname_ww3_4 = os.environ['HOME'] + '/Dropbox/ww3vale/TU/Resultados_Previsao_RT1/boia4/ww3/' #b4-ww3
pathname_swn_10 = os.environ['HOME'] + '/Dropbox/ww3vale/TU/Resultados_Previsao_RT1/boia10/swan/'

#nome dos arquivos
#adcp - boia 4 e 10
adcp04 = 'TU_boia04.out'
adcp10 = 'TU_boia10.out'

#ww3
arqww3 = 'pointparameters_050.txt'

#swan
arqswn17 = 'table_point_BES20150217.out'
arqswn18 = 'table_point_BES20150218.out'
arqswn19 = 'table_point_BES20150219.out' #modificar para o dia 19

#carrega dados
#adcp - boia 4 e 10 (press, pitch, roll, hs, dp, tp)
dd04 = np.loadtxt(pathname_adcp + adcp04,skiprows=1,delimiter=',') 
dd10 = np.loadtxt(pathname_adcp + adcp10,skiprows=1,delimiter=',')

dt04 = np.array([ dt.datetime.strptime(str(int(dd04[i,0])), '%Y%m%d%H%M') for i in range(len(dd04)) ])
dt10 = np.array([ dt.datetime.strptime(str(int(dd10[i,0])), '%Y%m%d%H%M') for i in range(len(dd10)) ])



#################################################################
#ww3 - previsao dos dias 16, 17, 18 e 19

# dw4_16 = np.loadtxt(pathname_ww3_4 + '20150216/' + arqww3,skiprows=2)
dw4_17 = np.loadtxt(pathname_ww3_4 + '20150217/' + arqww3,skiprows=2)
dw4_18 = np.loadtxt(pathname_ww3_4 + '20150218/' + arqww3,skiprows=2)
dw4_19 = np.loadtxt(pathname_ww3_4 + '20150219/' + arqww3,skiprows=2)
dw4_20 = np.loadtxt(pathname_ww3_4 + '20150220/' + arqww3,skiprows=2)
dw4_21 = np.loadtxt(pathname_ww3_4 + '20150221/' + arqww3,skiprows=2)


#data e hora - ww3
# dataw4_16 = [datetime.datetime(int(dw4_16[i,0]),int(dw4_16[i,1]),int(dw4_16[i,2]),int(dw4_16[i,3])) for i in range(len(dw4_16))]
dataw4_17 = [dt.datetime(int(dw4_17[i,0]),int(dw4_17[i,1]),int(dw4_17[i,2]),int(dw4_17[i,3])) for i in range(len(dw4_17))]
dataw4_18 = [dt.datetime(int(dw4_18[i,0]),int(dw4_18[i,1]),int(dw4_18[i,2]),int(dw4_18[i,3])) for i in range(len(dw4_18))]
dataw4_19 = [dt.datetime(int(dw4_19[i,0]),int(dw4_19[i,1]),int(dw4_19[i,2]),int(dw4_19[i,3])) for i in range(len(dw4_19))]
dataw4_20 = [dt.datetime(int(dw4_20[i,0]),int(dw4_20[i,1]),int(dw4_20[i,2]),int(dw4_20[i,3])) for i in range(len(dw4_20))]
dataw4_21 = [dt.datetime(int(dw4_21[i,0]),int(dw4_21[i,1]),int(dw4_21[i,2]),int(dw4_21[i,3])) for i in range(len(dw4_21))]


#swan - previsao do dia 17 e 18
ds10_17 = np.loadtxt(pathname_swn_10 + arqswn17, skiprows=7)
ds10_18 = np.loadtxt(pathname_swn_10 + arqswn18, skiprows=7)
ds10_19 = np.loadtxt(pathname_swn_10 + arqswn19, skiprows=7)

#data e hora - swan
#dia 17
start = dt.datetime(2015,02,17,00)
fim = len(ds10_17) #24 horas
datas10_17 = [start + dt.timedelta(hours=i) for i in xrange(0,fim)]
#dia 18
start = datetime.datetime(2015,02,18,00)
fim = len(ds10_18) #24 horas
datas10_18 = [start + datetime.timedelta(hours=i) for i in xrange(0,fim)]
#dia 19
start = datetime.datetime(2015,02,19,00)
fim = len(ds10_19) #24 horas
datas10_19 = [start + datetime.timedelta(hours=i) for i in xrange(0,fim)]


#corrige datas dos adcp (mudam um dia na hora 23)
for i in range(len(dt04)):
	if str(dt04[i])[-8:-6] >= 23:
		dt04[i] = dt04[i] - datetime.timedelta(days=1)

for i in range(len(dt10)):
	if str(dt04[i])[-8:-6] >= 23:
		dt10[i] = dt10[i] - datetime.timedelta(days=1)

#coloca data dos adcp e utc (soma 3h)
dt04 = [dt04[i] + datetime.timedelta(hours=3) for i in range(len(dt04))]
dt10 = [dt10[i] + datetime.timedelta(hours=3) for i in range(len(dt10))]

#define variaveis
#adcp
pr4, pit4, rol4, hs4, dp4, tp4 = dd04[:,0], dd04[:,1], dd04[:,2], dd04[:,3], dd04[:,4], dd04[:,5]
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
pl.plot(dataw4_17,hsw4_17,'g-',dataw4_18,hsw4_18,'k-',dataw4_19,hsw4_19,'b-',dataw4_20,hsw4_20,'m-',dataw4_21,hsw4_21,'y-',dt04,hs4,'ro')
pl.title('Boia-04')
pl.ylabel('Hs (m)'), pl.legend(['17','18','19','20','21'],fontsize=10)
pl.axis([dt04[-96],dataw4_19[-1],0.5,1.5])
pl.grid()
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(dataw4_17,tpw4_17,'g-',dataw4_18,tpw4_18,'k-',dataw4_19,tpw4_19,'b-',dataw4_20,tpw4_20,'m-',dataw4_21,tpw4_21,'y-',dt04,tp4,'ro')
pl.ylabel('Tp (s)')
pl.axis([dt04[-96],dataw4_19[-1],4,10])
pl.grid()
pl.xticks(visible=False)
pl.subplot(313)
pl.plot(dataw4_17,dpw4_17,'g-',dataw4_18,dpw4_18,'k-',dataw4_19,dpw4_19,'b-',dataw4_20,dpw4_20,'m-',dataw4_21,dpw4_21,'y-',dt04,dp4,'ro')
pl.ylabel('Dp (graus)')
pl.axis([dt04[-96],dataw4_19[-1],0,360])
pl.grid()

pl.figure(figsize=figsize1) #compara modelo e adcp (boia 10)
pl.subplot(311)
pl.plot(datas10_17,hss10_17,'g-',datas10_18,hss10_18,'k-',datas10_19,hss10_19,'b-',dt10,hs10,'ro')
pl.title('Boia-10')
pl.ylabel('Hs (m)'), pl.legend(['17','18','19'],fontsize=10)
pl.axis([dt10[-96],datas10_19[-1],0,1.2])
pl.grid()
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(datas10_17,tps10_17,'g-',datas10_18,tps10_18,'k-',datas10_19,tps10_19,'b-',dt10,tp10,'ro')
pl.ylabel('Tp (s)')
pl.axis([dt10[-96],datas10_19[-1],5,14])
pl.grid()
pl.xticks(visible=False)
pl.subplot(313)
pl.plot(datas10_17,dps10_17,'g-',datas10_18,dps10_18,'k-',datas10_19,dps10_19,'b-',dt10,dp10,'ro')
pl.ylabel('Dp (graus)')
pl.axis([dt10[-96],datas10_19[-1],0,360])
pl.grid()

pl.figure() #comparacao b4 (fundo) e b10 (raso)
pl.subplot(311)
pl.plot(datas10_17,hss10_17,datas10_18,hss10_18,'-g',dt04,hs4,'-b',dt10,hs10,'-r')
pl.legend(['SWN','B4','B10'])
pl.grid()
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(datas10_17,tps10_17,datas10_18,tps10_18,'-g',dt04,tp4,'.b',dt10,tp10,'.r')
pl.grid()
pl.xticks(visible=False)
pl.subplot(313)
pl.plot(datas10_17,dps10_17,datas10_18,dps10_18,'-g',dt04,dp4,'.b',dt10,dp10,'.r')
pl.ylim(0,360),pl.grid()

pl.figure()
pl.plot(dataw4_17,hsw4_17,'m-',dataw4_18,hsw4_18,'g-',dataw4_19,hsw4_19,'b-',dt04,hs4,'ro')
leg1 = pl.legend(['Prev 17','Prev 18','Prev 19','Boia-4'],loc=1)
pl.gca().add_artist(leg1)
pl.plot(datas10_17,hss10_17,'m-',datas10_18,hss10_18,'g-',datas10_19,hss10_19,'b-',dt10,hs10,'or')
leg2 = pl.legend(['Prev 17','Prev 18','Prev 19','Boia-10'],loc=4)
pl.grid()
pl.axis([dt04[-96],dataw4_19[-1],0,1.5])
pl.ylabel('Hs (m)')

pl.figure() #pitch e roll das 2 boias
pl.subplot(211)
pl.plot(dt04,pit4,'b-'), pl.legend(['pitch'],loc=6), pl.ylabel('pitch (graus)'), pl.grid()
pl.twinx()
pl.plot(dt04,rol4,'r-'), pl.legend(['roll'],loc=5), pl.ylabel('roll (graus)')
pl.title('Boia 4')
pl.subplot(212)
pl.plot(dt10,pit10,'b-'), pl.legend(['pitch'],loc=6), pl.ylabel('pitch (graus)'), pl.grid()
pl.twinx()
pl.plot(dt10,rol10,'r-'), pl.legend(['roll'],loc=5), pl.ylabel('roll (graus)')
pl.title('Boia 10')

# mare
pl.figure() #mare
pl.subplot(211)
pl.plot(dt04,pr4)
pl.subplot(212)
pl.plot(dt10,pr10)

pl.show()









