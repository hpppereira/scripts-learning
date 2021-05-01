'''
Avaliacao dos reusltados da prveisao para o periodo de Dez/Jan 2016 

Avalia a tendencia dos dados para saber se houve algum problema 

Compara com as medicoes da CB&I

'''

import matplotlib
import os
import numpy as np
import matplotlib.pylab as pl
import pandas as pd
from datetime import *
import xlrd
from scipy.signal import savgol_filter #Savitzky-Golay filter p/ suavizar serie
from pylab import FuncFormatter

########## DADOS AMBIDADOS

pl.close('all')
# DADOS ADCP
pathname_adcp = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/operacional/' #dados
pathnamep = os.environ['HOME'] + '/Dropbox/Previsao/vale/resultados/'

prevs = np.sort(os.listdir(pathnamep))

#nome dos arquivos
#adcp - boia 4 e 10
adcp04 = 'TU_boia04.out' #fora do porto (mais fundo)
adcp10 = 'TU_boia10.out' #dentro do porto

#carrega dados
# 0      1      2     3         4        5    6   7   8 9
#data,bateria,rumo,pressao,temperatura,pitch,roll,hs,tp,dp
adcp04 = np.loadtxt(pathname_adcp + adcp04,delimiter=',')
adcp10 = np.loadtxt(pathname_adcp + adcp10,delimiter=',')


# somei 3 horas para ficar UTC
dadcp04 = [ datetime.strptime(str(int(adcp04[i,0])), '%Y%m%d%H%M') for i in range(len(adcp04)) ]
dadcp04 = [ dadcp04[i] + timedelta(hours=3) for i in range(len(dadcp04))]
dadcp10 = [ datetime.strptime(str(int(adcp10[i,0])), '%Y%m%d%H%M') for i in range(len(adcp10)) ]
dadcp10 = [ dadcp10[i] + timedelta(hours=3) for i in range(len(dadcp10))]


model10=np.array([[0,0,0,0]])
mdd10_24=np.array([[0,0,0,0]])
mdd10_48=np.array([[0,0,0,0]])
mdd10_168=np.array([[0,0,0,0]])

model04=np.array([[0,0,0,0]])
mdd04_24=np.array([[0,0,0,0]])
mdd04_48=np.array([[0,0,0,0]])
mdd04_168=np.array([[0,0,0,0]])


for dto in prevs[0:-1]:

	model10= np.loadtxt(pathnamep + dto + '/table_point_ADCP10.out',skiprows=7,usecols=(0,1,3,2))
	mdd10_24=np.concatenate((mdd10_24,model10[0:25,:]),axis=0)
	mdd10_48=np.concatenate((mdd10_48,model10[25:49,:]),axis=0)
	mdd10_168=np.concatenate((mdd10_168,model10[145:169,:]),axis=0)
	

	model04= np.loadtxt(pathnamep + dto + '/table_point_ADCP01.out',skiprows=7,usecols=(0,1,3,2))
	mdd04_24=np.concatenate((mdd04_24,model04[0:25,:]),axis=0)
	mdd04_48=np.concatenate((mdd04_48,model04[25:49,:]),axis=0)
	mdd04_168=np.concatenate((mdd04_168,model04[145:169,:]),axis=0)



mdd10_24 = mdd10_24[1:,:]
mdd04_24 = mdd04_24[1:,:]
mdd10_48 = mdd10_48[1:,:]
mdd04_48 = mdd04_48[1:,:]
mdd10_168 = mdd10_168[1:,:]
mdd04_168 = mdd04_168[1:,:]

data_mod=mdd10_24[:,0]*100
data_mod = data_mod.astype(str) #ano mes dia hora
datam = np.array([datetime(int(data_mod[i][0:4]),int(data_mod[i][4:6]),int(data_mod[i][6:8]),int(data_mod[i][8:10])) for i in range(len(data_mod))])

data_mod04 = mdd04_24[:,0]*100
data_mod04 = data_mod04.astype(str) #ano mes dia hora
datam04 = np.array([datetime(int(data_mod04[i][0:4]),int(data_mod04[i][4:6]),int(data_mod04[i][6:8]),int(data_mod04[i][8:10])) for i in range(len(data_mod04))])


data_mod48=mdd10_48[:,0]*100
data_mod48 = data_mod48.astype(str) #ano mes dia hora
datam48 = np.array([datetime(int(data_mod48[i][0:4]),int(data_mod48[i][4:6]),int(data_mod48[i][6:8]),int(data_mod48[i][8:10])) for i in range(len(data_mod48))])

data_mod4804=mdd04_48[:,0]*100
data_mod4804 = data_mod4804.astype(str) #ano mes dia hora
datam4804 = np.array([datetime(int(data_mod4804[i][0:4]),int(data_mod4804[i][4:6]),int(data_mod4804[i][6:8]),int(data_mod4804[i][8:10])) for i in range(len(data_mod4804))])



data_mod168=mdd10_168[:,0]*100
data_mod168 = data_mod168.astype(str) #ano mes dia hora
datam168 = np.array([datetime(int(data_mod168[i][0:4]),int(data_mod168[i][4:6]),int(data_mod168[i][6:8]),int(data_mod168[i][8:10])) for i in range(len(data_mod168))])

data_mod16804=mdd04_168[:,0]*100
data_mod16804 = data_mod16804.astype(str) #ano mes dia hora
datam16804 = np.array([datetime(int(data_mod16804[i][0:4]),int(data_mod16804[i][4:6]),int(data_mod16804[i][6:8]),int(data_mod16804[i][8:10])) for i in range(len(data_mod16804))])


pl.figure()
pl.plot(dadcp10,adcp10[:,7],'ro')
pl.plot(datam,mdd10_24[:,1],'k--')
pl.plot(datam48,mdd10_48[:,1],'k.-')
pl.plot(datam168,mdd10_168[:,1],'g-')
pl.legend(['Boia10','1 dia','2 dias','7 dias'],loc=2)
pl.ylim([0,3.5])
pl.grid()
pl.show()


pl.figure()
pl.plot(dadcp10,adcp10[:,7],'ro')
pl.plot(dadcp04,adcp04[:,7],'bo')
pl.legend(['Boia10','Boia04'],loc=2)
pl.ylim([0,3.5])
pl.grid()
pl.show()


pl.figure()
pl.plot(dadcp10,adcp10[:,7],'ro')
pl.plot(datam,mdd10_24[:,1],'k--',linewidth=3)
pl.legend(['Boia10','1 dia'],loc=2)
pl.yticks(np.arange(0,3+.5,.5),color='red')
pl.ylabel("Hs (m)",color='r')
pl.ylim([-2,3.5])
pl.grid()
pl.twinx()
pl.plot(dadcp10,adcp10[:,9],'go')
pl.ylabel('Direcao de pico (Dp) Boia10 em graus',color='g')
pl.legend(['Dp Boia10'],loc=4)
pl.yticks(np.arange(0,360+45,45),color='g')
pl.ylim([45,360])
pl.show()

zeros=np.zeros(len(dadcp10))
z1=np.ones(len(dadcp10))*-15
z2=np.ones(len(dadcp10))*-10
z3=np.ones(len(dadcp10))*-5
z4=np.ones(len(dadcp10))*5
z5=np.ones(len(dadcp10))*10
z6=np.ones(len(dadcp10))*15
z7=np.ones(len(dadcp10))*20
# h1=np.ones(len(dadcp10))*
# h2=np.ones(len(dadcp10))*1
# h3=np.ones(len(dadcp10))*2.5
# h4=np.ones(len(dadcp10))*1
# h4=np.ones(len(dadcp10))*1

pl.figure()
pl.plot(dadcp10,adcp10[:,7],'ro')
#pl.plot(datam,mdd10_24[:,1],'k--',linewidth=3)
pl.legend(['Boia10','1 dia'],loc=2)
pl.yticks(np.arange(0,3+.5,.5),color='red')
pl.ylabel("Hs (m)",color='r')
pl.ylim([-2,3.5])
pl.grid(color='k')
pl.twinx()
pl.plot(dadcp10,adcp10[:,5],'g.')
pl.plot(dadcp10,adcp10[:,6],'y.')
pl.plot(dadcp10,z1,'g--', linewidth=0.5)
pl.plot(dadcp10,z2,'g--', linewidth=2)
pl.plot(dadcp10,z3,'g--', linewidth=0.5)
pl.plot(dadcp10,z4,'g--', linewidth=0.5)
pl.plot(dadcp10,z5,'g--', linewidth=2)
pl.plot(dadcp10,z6,'g--', linewidth=0.5)
pl.plot(dadcp10,z7,'g--', linewidth=0.5)
pl.ylabel('Deslocamentos Boia10 (graus)',color='g')
pl.legend(['pitch','roll'],loc=4)
pl.yticks(np.arange(-15,25,5),color='g')
pl.ylim([-15,100])
pl.show()


pl.figure()
pl.subplot(211)
pl.plot(dadcp10,adcp10[:,7],'ro')
#pl.plot(datam,mdd10_24[:,1],'k--',linewidth=3)
pl.legend(['Boia10','1 dia'],loc=2)
pl.yticks(np.arange(0,3+.5,.5),color='k')
pl.ylabel("Hs (m)",color='k')
pl.ylim([0,2.5])
pl.grid(color='k')
pl.subplot(212)
pl.plot(dadcp10,adcp10[:,5],'g.')
pl.plot(dadcp10,adcp10[:,6],'y.')
#pl.plot(dadcp10,z1,'k--', linewidth=0.5)
pl.plot(dadcp10,z2,'k--', linewidth=2)
#pl.plot(dadcp10,z3,'k--', linewidth=0.5)
#pl.plot(dadcp10,z4,'k--', linewidth=0.5)
pl.plot(dadcp10,z5,'k--', linewidth=2)
#pl.plot(dadcp10,z6,'k--', linewidth=0.5)
#pl.plot(dadcp10,z7,'k--', linewidth=0.5)
pl.ylabel('Deslocamentos Boia10 (graus)',color='k')
pl.legend(['pitch','roll'],loc=2)
pl.yticks(np.arange(-25,25,5),color='k')
pl.ylim([-25,25])
pl.grid()
pl.show()

pl.figure()
pl.plot(dadcp04,adcp04[:,7],'ro')
pl.plot(datam,mdd04_24[:,1],'k--',linewidth=3)
pl.legend(['Boia04','1 dia'],loc=2)
pl.yticks(np.arange(0,3+.5,.5),color='red')
pl.ylabel("Hs (m)",color='r')
pl.ylim([-2,3.5])
pl.grid()
pl.twinx()
pl.plot(dadcp04,adcp04[:,5],'g.')
pl.plot(dadcp04,adcp04[:,6],'y.') 
# pl.plot(datam,z1,'g--', linewidth=0.5)
# pl.plot(datam,z2,'g--', linewidth=0.5)
# pl.plot(datam,z3,'g--', linewidth=0.5)
# pl.plot(datam,z4,'g--', linewidth=0.5)
# pl.plot(datam,z5,'g--', linewidth=0.5)
# pl.plot(datam,z6,'g--', linewidth=0.5)
# pl.plot(datam,z7,'g--', linewidth=0.5)
pl.ylabel('Deslocamentos Boia04 (graus)                                                             ',color='g')
pl.legend(['pitch','roll'],loc=4)
pl.yticks(np.arange(-20,25,5),color='g')
pl.ylim([-25,90])
pl.show()


z2=np.ones(len(dadcp10))*-10
z5=np.ones(len(dadcp10))*10

pl.figure()
pl.plot(dadcp10,adcp10[:,5],'g.')
pl.plot(dadcp10,adcp10[:,6],'y.')
pl.plot(dadcp10,z2,'g--', linewidth=1)
pl.plot(dadcp10,z5,'g--', linewidth=1)
pl.ylabel('Deslocamentos Boia10 (graus)',color='k')
pl.legend(['pitch','roll'],loc=4)
pl.yticks(np.arange(-20,25,5),color='k')
pl.ylim([-25,25])
pl.grid()
pl.show()


pl.figure()
pl.plot(dadcp04,adcp04[:,7],'ro')
pl.plot(datam04,mdd04_24[:,1],'k--')
pl.plot(datam4804,mdd04_48[:,1],'k.-')
pl.plot(datam16804,mdd04_168[:,1],'g-')
pl.legend(['Boia04','1 dia','2 dias','7 dias'],loc=2)
pl.ylim([0,3.5])
pl.grid()
pl.show()


pl.figure()
pl.plot(dadcp04,adcp04[:,8],'ro')
pl.plot(datam04,mdd04_24[:,2],'ko')
pl.legend(['Boia04','1 dia'],loc=2)
pl.ylim([0,20])
pl.grid()
pl.show()



pl.figure()
pl.plot(dadcp04,adcp04[:,8],'ro')
pl.plot(dadcp10,adcp10[:,8],'ko')
pl.legend(['Boia04','Boia10'],loc=2)
pl.ylim([-10,20])
pl.grid()
pl.twinx()
pl.plot(dadcp04,adcp04[:,9],'go')
pl.yticks(np.arange(45,360+45,20),color='g')
pl.show()

## Analise dos dados -----------

data04=adcp04[:,0].astype(int)
data04=data04.astype(str)
D04=[data04[i][0:10] for i in range(len(data04)) ]
D04=np.array([D04[i] for i in xrange(len(D04))]).astype(int)


data10=adcp10[:,0].astype(int)
data10=data10.astype(str)
D10=[data10[i][0:10] for i in range(len(data10)) ]
D10=np.array([D10[i] for i in xrange(len(D10))]).astype(int)

hs04c=np.array([[0]])
hs10c=np.array([[0]])
datac=np.array([[0]])
dp04c=np.array([[0]])
dp10c=np.array([[0]])

for j in range(len(D04)):

	n=np.where(D04[j]==D10)[0];
	if n.size:
		
		hs04=np.array([[adcp04[j,7]]])
		hs10=np.array([[adcp10[n[0],7]]])
		dp04=np.array([[adcp04[j,9]]])
		dp10=np.array([[adcp10[n[0],9]]])
		datacc=np.array([[D04[n[0]]]])
		datac=np.concatenate((datac,datacc),axis=0)
		hs04c=np.concatenate((hs04c,hs04),axis=0)
		hs10c=np.concatenate((hs10c,hs10),axis=0)
		dp04c=np.concatenate((dp04c,dp04),axis=0)
		dp10c=np.concatenate((dp10c,dp10),axis=0)



datac=datac[1:]
hs04c=hs04c[1:]
hs10c=hs10c[1:]
dp04c=dp04c[1:]
dp10c=dp10c[1:]

datac1 = [ datetime.strptime(str(int(datac[i])), '%Y%m%d%H') for i in range(len(datac)) ]

diff=hs04c-hs10c
x=diff.tolist()

g=np.diff(x)
g=np.sign(g)
g=np.diff(g)
g=np.insert(g,0,0)
g1=np.where(g==2)[0]
g2=np.where(g==-2)[0]

zeros=np.zeros(len(datac1))
z45=np.ones(len(datac1))*45
z90=np.ones(len(datac1))*90
z135=np.ones(len(datac1))*135
z180=np.ones(len(datac1))*180
z225=np.ones(len(datac1))*225
h1=np.ones(len(datac1))*-1
h2=np.ones(len(datac1))*-0.5
h3=np.ones(len(datac1))*0.5
h4=np.ones(len(datac1))*1

pl.figure()
pl.plot(datac1,diff,'ro')
pl.plot(datac1,h3,'r--', linewidth=1.5)
pl.plot(datac1,h4,'r--', linewidth=1.5)
pl.plot(datac1,zeros,'k', linewidth=2)
pl.title('Dados coletados em 2015/2016')
pl.legend(['Diferenca (04-10)'],loc=3)
pl.ylabel('Diferenca do Hs entre as Boias 04 (externa) e 10 (interna) em metros',color='red')
pl.yticks(np.arange(-1,1.5+.5,.5),color='red')
pl.ylim([-1,1.5])
pl.grid(color='k',linestyle='-.',linewidth=0.2)
pl.twinx()
pl.plot(datac1,dp04c,'bo')
pl.plot(datac1,z45,'b--', linewidth=1.5)
pl.plot(datac1,z90,'b--', linewidth=1.5)
#pl.plot(datac1,z135,'b--', linewidth=1)
#pl.plot(datac1,z180,'b--', linewidth=1)
#pl.plot(datac1,z225,'b--', linewidth=1)
pl.ylabel('Direcao de pico (Dp) Boia04 em graus',color='blue')
pl.legend(['Dp Boia04'],loc=4)
pl.yticks(np.arange(0,360+45,45),color='blue')
pl.ylim([20,270])
pl.show()

stop

# diff1 = savgol_filter(diff[:,0], 35, 3) # window size 73, polynomial order 2
# dp04cf = savgol_filter(dp04c[:,0], 19, 3)

# pl.figure()
# #pl.plot(datac1,diff,'go')
# pl.plot(datac1,diff1,'ro')
# pl.plot(datac1,zeros,'k', linewidth=2)
# #pl.plot(datac1,h1,'r--', linewidth=1)
# #pl.plot(datac1,h2,'r--', linewidth=1)
# pl.plot(datac1,h3,'r--', linewidth=1)
# pl.plot(datac1,h4,'r--', linewidth=1)
# pl.title('Dados dos ADCPs coletados pela AMBIDADOS em campanha de 2015/2016 (filtrado)')
# pl.legend(['Diferenca (04-10)'],loc=3)
# pl.ylabel('Diferenca do Hs entre os ADCPs 04 (externo) e 10 (interno) em metros',color='red')
# pl.yticks(np.arange(-1,1.5+.5,.5),color='red')
# pl.ylim([-1,1.5])
# pl.grid(color='r',linestyle='-.')
# pl.twinx()
# pl.plot(datac1,dp04cf,'bo')
# pl.plot(datac1,z45,'b--', linewidth=1)
# pl.plot(datac1,z90,'b--', linewidth=1)
# #pl.plot(datac1,z135,'b--', linewidth=1)
# #pl.plot(datac1,z180,'b--', linewidth=1)
# #pl.plot(datac1,z225,'b--', linewidth=1)
# pl.ylabel('Direcao de pico (Dp) ADCP04 em graus',color='blue')
# pl.legend(['Dp ADCP04'],loc=4)
# pl.yticks(np.arange(0,360+45,45),color='blue')
# pl.ylim([20,270])
# #pl.grid()
# pl.show()

# deixar essas linhas para a comparacao no final com o modelo
dp04c1=dp04c
diff1=diff

# #retira os dados com nan de cada variavel
# ind = np.where(np.isnan(diff[:,0]) == False)[0]

# diff = diff[ind,0]
# dp04c = dp04c[ind,0]

# # Histograma 2D
# H, xedges, yedges = np.histogram2d(diff,dp04c,200)
 
# H = np.rot90(H)
# H = np.flipud(H)
 
# Hmasked = np.ma.masked_where(H==0,H) # Mask pixels with a value of zero
 
# # Plot 2D histogram using pcolor
# pl.figure()
# pl.pcolormesh(xedges,yedges,Hmasked)
# pl.xlabel('Diferenca (m)')
# pl.ylabel('Dp04 (graus)')
# pl.xlim([-1,2])
# cbar = pl.colorbar()
# cbar.ax.set_ylabel('Ocorrencia')

## Analise dos resultados do modelo -----------
diffm=mdd04_24[:,1] - mdd10_24[:,1]

zeros=np.zeros(len(datam))


pl.figure()
pl.plot(datac1,diff1,'ro')
pl.plot(datam,diffm,'go')
pl.plot(datam,zeros,'k', linewidth=2)
pl.title('Modelado e dados dos ADCPs coletados pela AMBIDADOS em campanha de 2015/2016')
pl.legend(['Medido (04-10)','Modelado (04-10)'],loc=3)
pl.ylabel('Diferenca do Hs entre os ADCPs 04 (externo) e 10 (interno) em metros',color='red')
pl.yticks(np.arange(-1,1.5+.5,.5),color='red')
pl.ylim([-1,1.5])
pl.grid(color='r',linestyle='-.')
pl.twinx()
pl.plot(datac1,dp04c,'bo')
pl.plot(datac1,z45,'b--', linewidth=1)
pl.plot(datac1,z90,'b--', linewidth=1)
pl.plot(datac1,z135,'b--', linewidth=1)
pl.plot(datac1,z180,'b--', linewidth=1)
pl.plot(datac1,z225,'b--', linewidth=1)
pl.ylabel('Direcao de pico (Dp) ADCP04 em graus',color='blue')
pl.legend(['Dp ADCP04'],loc=4)
pl.yticks(np.arange(0,360+45,45),color='blue')
pl.ylim([20,270])
#pl.grid()
pl.show()

pl.figure()
pl.plot(datam,diffm,'ro')
pl.plot(datam,zeros,'k', linewidth=2)
pl.title('Modelado e dados dos ADCPs coletados pela AMBIDADOS em campanha de 2015/2016')
pl.legend(['Modelado (04-10)'],loc=3)
pl.ylabel('Diferenca do Hs entre os ADCPs 04 (externo) e 10 (interno) em metros',color='red')
pl.yticks(np.arange(-1,1.5+.5,.5),color='red')
pl.ylim([-1,1.5])
pl.grid(color='r',linestyle='-.')
pl.twinx()
pl.plot(datac1,dp04c,'bo')
pl.plot(datam,mdd04_24[:,3],'go')
pl.plot(datac1,z45,'b--', linewidth=1)
pl.plot(datac1,z90,'b--', linewidth=1)
pl.plot(datac1,z135,'b--', linewidth=1)
pl.plot(datac1,z180,'b--', linewidth=1)
pl.plot(datac1,z225,'b--', linewidth=1)
pl.ylabel('Direcao de pico (Dp) ADCP04 em graus',color='blue')
pl.legend(['Dp ADCP04 Medida','Dp ADCP04 Modelada'],loc=4)
pl.yticks(np.arange(0,360+45,45),color='blue')
pl.ylim([20,270])
#pl.grid()
pl.show()

# pl.figure()
# pl.plot(diffm,mdd04_24[:,3],'bo')
# pl.ylabel('Dp04 (graus)')
# pl.xlabel('Diferenca (m)')
# pl.xlim([-1,2])
# pl.grid()
# pl.show()

# histograma da diferenca dos dados (para direcoes entre 45 e 90)
# ver a relacao entre os valores de direcao menores que 100 graus e a diferenca entre os hs
# 5200 dia 12/11/2015

n90=np.where(dp04c1[0:5200]<=90)[0]
diff90=diff1[n90]
#diff90m=diffm[n90]
dp04c90=dp04c1[n90]

#tirar valores espurios
diff90[np.where(diff90>=2)] = np.nan
diff90[np.where(diff90<=-1)] = np.nan

print np.nanmean(diff90)  # 0.50
#print np.nanmean(diff90m)  # 0.52


#histogram
fig = pl.figure(figsize=(16,12))
ax = fig.add_subplot(111)
pl.title('Histograma da diferenca entre os valores de Hs do ADCP04 e ADCP10 para ondas com Dp no ADCP04 entre 45 e 90 graus')
binshs=np.arange(-0.5,1.5,0.1)
counts,bins,patches = ax.hist(diff90,bins=binshs,facecolor='gray',edgecolor='black',hatch="/",label="Diferenca (m)")
ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,60,10): lima.append((i*len(diff90)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(diff90)) ) * 100, 0)) + ' %'
pl.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 0.25
# for count, x in zip(counts,bin_centers):
#     percent = '%0.1f%%' % (100 * float(count) / counts.sum())
#     ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
#         xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)

ax.legend(loc="upper right")
pl.grid()


# para medicoes pos datetime.datetime(2015, 12, 7, 0, 0)

n90=np.where(dp04c1[6280:-1]<=90)[0]
diff90=diff1[n90]
diff90m=diffm[n90]
dp04c90=dp04c1[n90]

#tirar valores espurios
diff90[np.where(diff90>=2)] = np.nan
diff90[np.where(diff90<=-1)] = np.nan

print np.nanmean(diff90)  # 0.25
print np.nanmean(diff90m)  # 0.52



#histogram
fig = pl.figure(figsize=(16,12))
ax = fig.add_subplot(111)
pl.title('Histograma da diferenca entre os valores de Hs do ADCP04 e ADCP10 para ondas com Dp no ADCP04 entre 45 e 90 graus')
binshs=np.arange(-0.5,1.5,0.1)
counts,bins,patches = ax.hist(diff90,bins=binshs,facecolor='gray',edgecolor='black',hatch="/",label="Diferenca (m)")
ax.set_xticks(bins)

#setar eixo y com porcentagem
lima=[]
for i in range(0,60,10): lima.append((i*len(diff90)/100))

ax.set_yticks(lima)    
to_percentage = lambda y, pos: str(round( ( y / float(len(diff90)) ) * 100, 0)) + ' %'
pl.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


bin_centers=np.diff(bins) + bins[:-1] - 0.25
# for count, x in zip(counts,bin_centers):
#     percent = '%0.1f%%' % (100 * float(count) / counts.sum())
#     ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
#         xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)

ax.legend(loc="upper right")
pl.grid()





# media para medicoes antes do dia 

# diffm=diffm[:,0]
# dir04=mdd04_24[:,3]
# # Histograma 2D
# H, xedges, yedges = np.histogram2d(diffm,dir04,200)
 
# H = np.rot90(H)
# H = np.flipud(H)
 
# Hmasked = np.ma.masked_where(H==0,H) # Mask pixels with a value of zero
 
# # Plot 2D histogram using pcolor
# pl.figure()
# pl.pcolormesh(xedges,yedges,Hmasked)
# pl.xlabel('Diferenca (m)')
# pl.ylabel('Dp04 (graus)')
# pl.xlim([-1,2])
# cbar = pl.colorbar()
# cbar.ax.set_ylabel('Ocorrencia')


#### ====================================    DADOS CBI ========================================

# #variaveis de onda dos adcp
# anemo = np.array([[0,0,0]])
# adcp1 = np.array([[0,0,0,0,0,0,0,0,0]])
# adcp2 = np.array([[0,0,0,0,0,0,0,0,0]])
# adcp3 = np.array([[0,0,0,0,0,0,0,0,0]])
# adcp4 = np.array([[0,0,0,0,0,0,0,0,0]])

# #varia as 13 campanhas
# for i in range(1,14):

# 	#campanha a ser processada (1 a 13)
# 	camp = i

# 	#deixa com 2 digitos
# 	camp = str(camp).zfill(2)

# 	#pathname = os.environ['HOME'] + 'C:Users/Cliente/Dropbox/ww3vale/Geral/TU/dados/Planilhas_Processadas/'
# 	pathname = os.environ['HOME'] + '/Dropbox/ww3vale/TU/dados/ADCP/proc_vale/Planilhas/xls/'
# 	pathadcp = 'PTU_campanha_' + camp + '.xls'

# 	#Open an Excel workbook 
# 	workbook = xlrd.open_workbook(pathname + pathadcp)

# 	print pathadcp

# 	#imprime nome das planilhas
# 	# print workbook.sheet_names()

# 	#seleciona planilha por indice (pode ser por nome tbm)
# 	sheet_0 = workbook.sheet_by_index(0) #anemometro
# 	sheet_3 = workbook.sheet_by_index(5) #adcp-1
# 	sheet_5 = workbook.sheet_by_index(9) #adcp-2
# 	sheet_7 = workbook.sheet_by_index(13) #adcp-3
# 	sheet_9 = workbook.sheet_by_index(17) #adcp-4

# 	#pega os valores das celulas selecionadas
# 	#vento
# 	vento = np.array([[sheet_0.cell_value(r,c) for r in range(18,sheet_0.nrows)] for c in range(1,sheet_0.ncols)]).T
	
# 	#onda
# 	#  0    1    2     3      4     5      6      7    8
# 	# data hm0, h10, hmax, dirtp, SprTp, MeanDir, Tp, Tm02
# 	onda1 = np.array([[sheet_3.cell_value(r,c) for r in range(22,sheet_3.nrows)] for c in range(1,sheet_3.ncols)]).T
# 	onda2 = np.array([[sheet_5.cell_value(r,c) for r in range(22,sheet_5.nrows)] for c in range(1,sheet_5.ncols)]).T
# 	onda3 = np.array([[sheet_7.cell_value(r,c) for r in range(22,sheet_7.nrows)] for c in range(1,sheet_7.ncols)]).T
# 	onda4 = np.array([[sheet_9.cell_value(r,c) for r in range(22,sheet_9.nrows)] for c in range(1,sheet_9.ncols)]).T

# 	#concatena as variaveis de cada adcp
# 	anemo = np.concatenate((anemo,vento),axis=0)
# 	adcp1 = np.concatenate((adcp1,onda1),axis=0)
# 	adcp2 = np.concatenate((adcp2,onda2),axis=0)
# 	adcp3 = np.concatenate((adcp3,onda3),axis=0)
# 	adcp4 = np.concatenate((adcp4,onda4),axis=0)

# #retira a primeira linha com zeros devido a concatenacao
# anemo = anemo[1:,:]
# adcp1 = adcp1[1:,:]
# adcp2 = adcp2[1:,:]
# adcp3 = adcp3[1:,:]
# adcp4 = adcp4[1:,:]

# #data com datetime
# datan = [datetime(*xlrd.xldate_as_tuple(anemo[i,0],workbook.datemode)) for i in range(len(anemo))] # anemometro
# data1 = [datetime(*xlrd.xldate_as_tuple(adcp1[i,0],workbook.datemode)) for i in range(len(adcp1))]
# data2 = [datetime(*xlrd.xldate_as_tuple(adcp2[i,0],workbook.datemode)) for i in range(len(adcp2))]
# data3 = [datetime(*xlrd.xldate_as_tuple(adcp3[i,0],workbook.datemode)) for i in range(len(adcp3))]
# data4 = [datetime(*xlrd.xldate_as_tuple(adcp4[i,0],workbook.datemode)) for i in range(len(adcp4))]


# #consistencia
# adcp1[np.where(adcp1==999)] = np.nan
# adcp2[np.where(adcp2==999)] = np.nan
# adcp3[np.where(adcp3==999)] = np.nan
# adcp4[np.where(adcp4==999)] = np.nan

# # adcp
# #  0     1    2     3      4     5        6   7
# # hm0, h10, hmax, dirtp, SprTp, MeanDir, Tp, Tm02
# adcp1 = adcp1[:,1:]
# adcp2 = adcp2[:,1:]
# adcp3 = adcp3[:,1:]
# adcp4 = adcp4[:,1:]



# ## Analise dos dados -----------

# #data01=(*xlrd.xldate_as_tuple(adcp1[i,0],workbook.datemode)).astype(int)

# D01 = np.array([datetime.strftime(data1[i],'%Y%m%d%H') for i in xrange(len(data1))]).astype(int)

# D03 = np.array([datetime.strftime(data3[i],'%Y%m%d%H') for i in xrange(len(data3))]).astype(int)

# hs01c=np.array([[0]])
# hs03c=np.array([[0]])
# datac=np.array([[0]])
# dp01c=np.array([[0]])
# dp03c=np.array([[0]])

# for j in range(len(D01)):

# 	n=np.where(D01[j]==D03)[0];
# 	if n.size:
		
# 		hs01=np.array([[adcp1[j,0]]])
# 		hs03=np.array([[adcp3[n[0],0]]])
# 		dp01=np.array([[adcp1[j,3]]])
# 		dp03=np.array([[adcp3[n[0],3]]])
# 		datacc=np.array([[D03[n[0]]]])
# 		datac=np.concatenate((datac,datacc),axis=0)
# 		hs01c=np.concatenate((hs01c,hs01),axis=0)
# 		hs03c=np.concatenate((hs03c,hs03),axis=0)
# 		dp01c=np.concatenate((dp01c,dp01),axis=0)
# 		dp03c=np.concatenate((dp03c,dp03),axis=0)



# datac=datac[1:]
# hs01c=hs01c[1:]
# hs03c=hs03c[1:]
# dp01c=dp01c[1:]
# dp03c=dp03c[1:]

# datac1 = [ datetime.strptime(str(int(datac[i])), '%Y%m%d%H') for i in range(len(datac)) ]

# diff=hs01c-hs03c

# zeros=np.zeros(len(datac1))
# z45=np.ones(len(datac1))*45
# z90=np.ones(len(datac1))*90
# z135=np.ones(len(datac1))*135
# z180=np.ones(len(datac1))*180
# z225=np.ones(len(datac1))*225


# pl.figure()
# pl.plot(datac1,diff,'ro')
# pl.plot(datac1,zeros,'k', linewidth=2)
# pl.title('Dados dos ADCPs coletados pela CB&I em campanha de 2013/2014')
# pl.legend(['Diferenca (01-03)'],loc=3)
# pl.ylabel('Diferenca do Hs entre os ADCPs 01 (externo) e 03 (interno) em metros',color='red')
# pl.yticks(np.arange(-1,1.5+.5,.5),color='red')
# pl.ylim([-1,1.5])
# pl.grid(color='r',linestyle='-.')
# pl.twinx()
# pl.plot(datac1,dp01c,'bo')
# pl.plot(datac1,z45,'b--', linewidth=1)
# pl.plot(datac1,z90,'b--', linewidth=1)
# pl.plot(datac1,z135,'b--', linewidth=1)
# pl.plot(datac1,z180,'b--', linewidth=1)
# pl.plot(datac1,z225,'b--', linewidth=1)
# pl.ylabel('Direcao de pico (Dp) ADCP01 em graus',color='blue')
# pl.legend(['Dp ADCP01'],loc=4)
# pl.yticks(np.arange(0,360+45,45),color='blue')
# pl.ylim([20,270])
# #pl.grid()
# pl.show()



# # histograma da diferenca dos dados (para direcoes entre 45 e 90)

# n90=np.where(dp01c<=90)[0]
# diff90=diff[n90]

# #tirar valores espurios
# diff90[np.where(diff90>=2)] = np.nan
# diff90[np.where(diff90<=-1)] = np.nan

# print np.nanmean(diff90)  # 0.60


# #histogram
# fig = pl.figure(figsize=(16,12))
# ax = fig.add_subplot(111)
# pl.title('Histograma da diferenca entre os valores de Hs do ADCP01 e ADCP03 para ondas com Dp no ADCP04 entre 45 e 90 graus')
# binshs=np.arange(-0.5,1.5,0.1)
# counts,bins,patches = ax.hist(diff90,bins=binshs,facecolor='gray',edgecolor='black',hatch="/",label="Diferenca (m)")
# ax.set_xticks(bins)

# #setar eixo y com porcentagem
# lima=[]
# for i in range(0,60,10): lima.append((i*len(diff90)/100))

# ax.set_yticks(lima)    
# to_percentage = lambda y, pos: str(round( ( y / float(len(diff90)) ) * 100, 0)) + ' %'
# pl.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


# bin_centers=np.diff(bins) + bins[:-1] - 0.25
# for count, x in zip(counts,bin_centers):
#     percent = '%0.1f%%' % (100 * float(count) / counts.sum())
#     ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
#         xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)

# ax.legend(loc="upper right")
# pl.grid()
# pl.show()


# # histograma da diferenca dos dados (para direcoes entre 90 e 135)

# n90=np.where(dp01c>=90)[0]
# n135=np.where(dp01c[n90]<=135)[0]

# diff135=diff[n90[n135]]

# #tirar valores espurios
# diff135[np.where(diff135>=2)] = np.nan
# diff135[np.where(diff135<=-1)] = np.nan

# print np.nanmean(diff135)  # 0.60


# #histogram
# fig = pl.figure(figsize=(16,12))
# ax = fig.add_subplot(111)
# pl.title('Histograma da diferenca entre os valores de Hs do ADCP01 e ADCP03 para ondas com Dp no ADCP04 entre 90 e 135 graus')
# binshs=np.arange(-0.5,1.5,0.1)
# counts,bins,patches = ax.hist(diff135,bins=binshs,facecolor='gray',edgecolor='black',hatch="/",label="Diferenca (m)")
# ax.set_xticks(bins)

# #setar eixo y com porcentagem
# lima=[]
# for i in range(0,60,10): lima.append((i*len(diff135)/100))

# ax.set_yticks(lima)    
# to_percentage = lambda y, pos: str(round( ( y / float(len(diff135)) ) * 100, 0)) + ' %'
# pl.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))


# bin_centers=np.diff(bins) + bins[:-1] - 0.25
# for count, x in zip(counts,bin_centers):
#     percent = '%0.1f%%' % (100 * float(count) / counts.sum())
#     ax.annotate(percent, xy=(x, 0), weight='bold',xycoords=('data', 'axes fraction'),
#         xytext=(0, -20), textcoords='offset points', va='top', ha='center',fontsize=10)

# ax.legend(loc="upper right")
# pl.grid()
# pl.show()


# diff1 = savgol_filter(diff[:,0], 35, 3) # window size 73, polynomial order 2
# dp01cf = savgol_filter(dp01c[:,0], 19, 3)

# pl.figure()
# #pl.plot(datac1,diff,'go')
# pl.plot(datac1,diff1,'ro')
# pl.plot(datac1,zeros,'k', linewidth=2)
# #pl.plot(datac1,h1,'r--', linewidth=1)
# #pl.plot(datac1,h2,'r--', linewidth=1)
# pl.plot(datac1,h3,'r--', linewidth=1)
# pl.plot(datac1,h4,'r--', linewidth=1)
# pl.title('Dados dos ADCPs coletados pela CB&I em campanha de 2013/2014 (filtrado)')
# pl.legend(['Diferenca (01-03)'],loc=3)
# pl.ylabel('Diferenca do Hs entre os ADCPs 01 (externo) e 03 (interno) em metros',color='red')
# pl.yticks(np.arange(-1,1.5+.5,.5),color='red')
# pl.ylim([-1,1.5])
# pl.grid(color='r',linestyle='-.')
# pl.twinx()
# pl.plot(datac1,dp01cf,'bo')
# pl.plot(datac1,z45,'b--', linewidth=1)
# pl.plot(datac1,z90,'b--', linewidth=1)
# #pl.plot(datac1,z135,'b--', linewidth=1)
# #pl.plot(datac1,z180,'b--', linewidth=1)
# #pl.plot(datac1,z225,'b--', linewidth=1)
# pl.ylabel('Direcao de pico (Dp) ADCP01 em graus',color='blue')
# pl.legend(['Dp ADCP01'],loc=4)
# pl.yticks(np.arange(0,360+45,45),color='blue')
# pl.ylim([20,270])
# #pl.grid()
# pl.show()

# # pegar modelado
# #diretorio de onde estao os resultados do ADCP01
# pathname = os.environ['HOME'] + '/Dropbox/ww3vale_info/TU/hindcast/output/VIX/'

# direm = np.sort(os.listdir(pathname))

# pathname2 = os.environ['HOME'] + '/Dropbox/ww3vale_info/TU/hindcast/output/BES/'
# direm2 = np.sort(os.listdir(pathname2))

# md1=np.array([[0,0,0,0]])
# madcp01=np.array([[0,0,0,0]])

# md2=np.array([[0,0,0,0]])
# madcp02=np.array([[0,0,0,0]])

# md3=np.array([[0,0,0,0]])
# madcp03=np.array([[0,0,0,0]])

# md4=np.array([[0,0,0,0]])
# madcp04=np.array([[0,0,0,0]])


# #loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
# for dto in direm:

# 	madcp01= np.loadtxt(pathname + dto + '/table_point_ADCP01.out',skiprows=7,usecols=(0,1,3,2))
# 	md1=np.concatenate((md1,madcp01[:,:]),axis=0)

# for dto in direm2:

# 	madcp03= np.loadtxt(pathname2 + dto + '/table_point_ADCP03.out',skiprows=7,usecols=(0,1,3,2))
# 	md3=np.concatenate((md3,madcp03[:,:]),axis=0)




# md1 = md1[1:,:] #adcp01
# md3 = md3[1:,:] #adcp03

# data_mod=md1[:,0]*100
# data_mod = data_mod.astype(str) #ano mes dia hora
# datam = np.array([datetime(int(data_mod[i][0:4]),int(data_mod[i][4:6]),int(data_mod[i][6:8]),int(data_mod[i][8:10])) for i in range(len(data_mod))])

# ## Analise dos resultados do modelo -----------
# diffm=md1[:,1] - md3[:,1]

# zeros=np.zeros(len(datam))
# h1=np.ones(len(datam))*0.5
# h2=np.ones(len(datam))*1

# pl.figure()
# pl.plot(datac1,diff,'ro')
# pl.plot(datam,diffm,'go')
# pl.plot(datam,h1,'--r')
# pl.plot(datam,h2,'--r')
# pl.plot(datam,zeros,'k', linewidth=2)
# pl.title('Dados dos ADCPs coletados pela CB&I em campanha de 2013/2014')
# pl.legend(['Diferenca (01-03)','Modelado (01-03)'],loc=2)
# pl.ylabel('Diferenca do Hs entre os ADCPs 01 (externo) e 03 (interno) em metros',color='red')
# pl.yticks(np.arange(0,1.5+.5,.5),color='red')
# pl.ylim([-2,1.5])
# pl.grid(color='r',linestyle='-.')
# pl.twinx()
# pl.plot(datac1,dp01c,'bo')
# pl.plot(datac1,z45,'b--', linewidth=1)
# pl.plot(datac1,z90,'b--', linewidth=1)
# pl.plot(datac1,z135,'b--', linewidth=1)
# pl.plot(datac1,z180,'b--', linewidth=1)
# pl.ylabel('Direcao de pico (Dp) ADCP01 em graus',color='blue')
# pl.legend(['Dp ADCP01'],loc=4)
# pl.yticks(np.arange(0,360+45,45),color='blue')
# pl.ylim([45,270])
# #pl.grid()
# pl.show()


