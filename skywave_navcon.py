# -*- coding: utf-8 -*-
'''
Comparacao dos dados da BMOP 03 (Izabel)
enviados pelo site e software da NavCon

** Parece que a direcao das ondas enviados
pelo software esta errada (direcoes de 290 graus)

0   1   2           3                 4             5
id,mId,isn,ExprDataHoraOnixSat,ExprDataHoraBMOP,codigoBMOP,
   6         7              8                  9
latitude,longitude,temperaturaInterna,voltagemCarregamento,
     10          11         12             13             14
correntePS1,correntePS2,correntePS3,voltagemBateria,correnteBateria,
      15              16             17           18            19
correnteConsumo,velocidadeVento,direçãoVento,temperaturaAr,umidadeRelativa,
  20       21        22         23          24           25            26
pressão,flagProc,alturaOnda,periodoPico,direçãoPico,espaçoLivreHD,espaçoLivrePenDrive,
     27          28            29           30           31           32
LoggerTemp01,LoggerTemp02,LoggerTemp03,LoggerTemp04,LoggerTemp05,LoggerTemp06,
    33            34            35          36         37       38       39
LoggerTemp07,LoggerTemp08,LoggerTemp09,LoggerTemp10,EWCorr01,NSCorr01,EWCorr02,
   40        41       42      43       44       45       46      47        48      49
NSCorr02,EWCorr03,NSCorr03,EWCorr04,NSCorr04,EWCorr05,NSCorr05,EWCorr06,NSCorr06,EWCorr07,
   50       51       52      53       54       55        56
NSCorr07,EWCorr08,NSCorr08,EWCorr09,NSCorr09,EWCorr10,NSCorr10
'''

import os
import numpy as np
from datetime import datetime
import matplotlib.pylab as pl
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import matplotlib.dates as mdates

pl.close('all')

#pathname
pathname = os.environ['HOME'] + '/Dropbox/bmo/dados/Izabel/telemetria/'

#BMOP 03 - Izabel
izabel = 'Mensagens_01025968SKYF4AD.csv'
susana = 'Mensagens_01025968SKYF4AD.csv'

iza1 = np.loadtxt(pathname + izabel,dtype=str,skiprows=0,delimiter=',') #software
sus1 = np.loadtxt(pathname + susana,dtype=str,skiprows=0,delimiter=',') #software

#idem nas duas boias
cabec = iza1[0,:] #cabecalho

#restringe os dados, pra que?
# dados = dados[-100:]

#parametros meteo-oceanograficos (pula 17 linhas, primeira eh cabecalho e as outras estao ruins)
ini = 18
# 0    1      2       3     4   5   6   7   8   9   10  11   12   13   14    15   16    17     18     19    20
#lat, lon, tempint, volbat, ws, wd, at, rh, pr, hs, tp, dp, tm1, tm5, tm10, cew1, cns1, cew5, cns5, cew10, cns10
iza = iza1[ini:,[6,7,8,13,16,17,18,19,20,22,23,24,27,31,36,37,38,45,46,55,56]].astype(float)
sus = sus1[ini:,[6,7,8,13,16,17,18,19,20,22,23,24,27,31,36,37,38,45,46,55,56]].astype(float)

#coluna 3 para data da onixsat e coluna 4 para data da boia
dataiza = np.array([datetime.strptime(iza1[i,4],'%d/%m/%Y %H:%M:%S') for i in range(ini,len(iza1))])
datasus = np.array([datetime.strptime(sus1[i,4],'%d/%m/%Y %H:%M:%S') for i in range(ini,len(sus1))])

#coloca nan nas latlon = 0
iza[np.where(iza[:,0]==0)[0]] = np.nan
iza[np.where(iza[:,1]==0)[0]] = np.nan

#correcao da direcao (de onde vai para onde vem)
iza[:,11] = iza[:,11] - 180
sus[:,11] = sus[:,11] - 180
iza[pl.find(iza[:,11]<0),11] = iza[pl.find(iza[:,11]<0),11] + 360
sus[pl.find(sus[:,11]<0),11] = sus[pl.find(sus[:,11]<0),11] + 360


#calcula da velocidade e direcao das correntes
vel1 = np.sqrt(iza[:,15]**2 + iza[:,16]**2) * 10**(-3) #m/s
dir1 = np.arctan(iza[:,16] / iza[:,15]) * 180 / np.pi #graus  #### verificar trigonometrico e azimute
dir1 = dir1 + 180

vel5 = np.sqrt(iza[:,17]**2 + iza[:,18]**2) * 10**(-3) #m/s
dir5 = np.arctan(iza[:,18] / iza[:,17]) * 180 / np.pi #graus  #### verificar trigonometrico e azimute
dir5 = dir5 + 180

vel10 = np.sqrt(iza[:,19]**2 + iza[:,20]**2) * 10**(-3) #m/s
dir10 = np.arctan(iza[:,20] / iza[:,19]) * 180 / np.pi #graus  #### verificar trigonometrico e azimute
dir10 = dir10 + 180


########################################################################

#posicao da boia izabel
pl.figure()
for i in range(400,len(iza)):
	if np.isnan(iza[i,1])==False and np.isnan(iza[i,1])==False:
		pl.plot(iza[i,1],iza[i,0],'ko')
		pl.text(iza[i,1],iza[i,0],dataiza.astype(str)[i])


#comparacao das boias izabel e susana
pl.figure()
pl.subplot(311)
pl.plot(dataiza,iza[:,9],'b',label='izabel')
pl.plot(datasus,sus[:,9],'r',label='susana')
pl.axis([datasus[0],datasus[-1],0,5])
pl.legend(loc=0,fontsize='10')
pl.grid()
pl.subplot(312)
pl.plot(dataiza,iza[:,10],'bo')
pl.plot(datasus,sus[:,10],'ro')
pl.axis([datasus[0],datasus[-1],4,12])
pl.grid()
pl.subplot(313)
pl.plot(dataiza,iza[:,11],'bo')
pl.plot(datasus,sus[:,11],'ro')
pl.axis([datasus[0],datasus[-1],0,360])
pl.grid()

#avaliacao dos utlimos dados enviados pela boia izabel
fig = pl.figure()
ax = fig.add_subplot(3,1,1)
ax.plot(dataiza,iza[:,9],'b',label='Hs')
ax.set_ylabel('Hs (m)'), ax.legend(loc=2,fontsize='10')
ax.set_ylim(0,5)
ax.grid()
pl.xticks(visible=False)
ax1 = ax.twinx()
ax1.plot(dataiza,iza[:,4],'r',label='Vel.vento')
ax1.set_ylabel('Vel.vento (m/s)'), pl.legend(loc=1,fontsize='10')
ax1.set_xlim(dataiza[368],dataiza[-1])
ax1.set_ylim(0,15)
pl.xticks(visible=False)

ax2 = fig.add_subplot(3,1,2)
ax2.plot(dataiza,vel1,'b',label='cel.01')
ax2.plot(dataiza,vel5,'r',label='cel.05')
ax2.plot(dataiza,vel10,'g',label='cel.10')
ax2.set_ylim(0,1)
ax2.set_xlim(dataiza[368],dataiza[-1])
pl.xticks(visible=False)
pl.legend(loc=0,fontsize='10')
ax2.grid()
ax2.set_ylabel('Vel.corrente (m/s)')

ax3 = fig.add_subplot(3,1,3)
ax3.plot(dataiza,dir1,'b',label='cel.01')
ax3.plot(dataiza,dir5,'r',label='cel.05')
ax3.plot(dataiza,dir10,'g',label='cel.10')
ax3.set_ylim(0,360)
ax3.set_xlim(dataiza[368],dataiza[-1])
pl.xticks(visible=False)
pl.legend(loc=0,fontsize='10')
ax3.grid()
ax3.set_ylabel('Dir.corrente (m/s)')



ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y \n %H:%M'))








pl.show()
