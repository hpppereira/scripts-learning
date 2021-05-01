# Rotina processamento dos parametros de ondas

#em florianopolis nao veio dados do site (arq_st = 'pnboia.B69150_argos.dat')

import numpy as np
import pylab as pl
import os
from datetime import datetime

# pl.close('all')

# ================================================================================== #  
# Carrega os dados

local = 'recife'
local1 = 'Recife'
glib = '32'
arq_st = 'pnboia.B69153_argos.dat'

#diretorio de onda estao os dados
pathname = os.environ['HOME'] + '/Dropbox/ww3br/rot/saida/' + local + '/'
pathname_ax = os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/summary-axys/' + local + '/'
pathname_st = os.environ['HOME'] + '/Dropbox/pnboia/dados/axys/site/'

#LIOc (paramwp)
#   0  1   2   3    4     5    6  7  8    9       10     11  12  13   14  15  16
# data,hs,h10,hmax,tmed,thmax,hm0,tp,dp,sigma1p,sigma2p,hm01,tp1,dp1,hm02,tp2,dp2
matondab = np.loadtxt(pathname + 'paramwb_' + glib + '-' + local + '.out', delimiter=',', unpack = False)
matondap = np.loadtxt(pathname + 'paramwp_' + glib + '-' + local + '.out', delimiter=',', unpack = False)

#Axys (Summary)
#  0        1            2          3        4         5         6        7            8            
#Year/Julian Date/Zero Crossings/Ave. Ht./Ave. Per./Max Ht./Sig. Wave/Sig. Per./Peak Per.(Tp)
#          9        10     11           12       13      14         15  
# /Peak Per.(READ)/HM0/Mean Theta/Sigma Theta/ H1/10 / T.H1/10 /Mean Per.(Tz)

axys = np.loadtxt(pathname_ax + 'Summary_todos.txt',skiprows = 1, usecols = (range(2,18)))
ax_data = np.loadtxt(pathname_ax + 'Summary_todos.txt',dtype = str, skiprows = 1, usecols = (0,1))


#Saida site (baixado em 05/10/2014) - site goos/brasil
#  0   1   2   3     4    5    6   7   8   9
# ano mes dia hora minuto Hs Hmax Tp Dirm, Df
site = np.loadtxt(pathname_st + arq_st ,delimiter=',', skiprows = 1, usecols = (2,3,4,5,6,45,46,47,48,49))


# ================================================================================== #  
# Formata as datas com datetime

#lioc
#formata o vetor de datas pra long e depois string
data = matondab[:,0].astype(np.long)
datas = data.astype(np.str)
datam = [datetime( int(datas[i][0:4]),int(datas[i][4:6]), int(datas[i][6:8]), int(datas[i][8:10]) ) for i in range(len(datas))]


#axys
#deixa datas com numeros inteiros
ano_ax = [int(ax_data[i,0][0:4]) for i in range(len(ax_data))]
mes_ax = [int(ax_data[i,0][5:7]) for i in range(len(ax_data))]
dia_ax = [int(ax_data[i,0][8:10]) for i in range(len(ax_data))]
hora_ax = [int(ax_data[i,1][:2]) for i in range(len(ax_data))]
min_ax = [int(ax_data[i,1][3:]) for i in range(len(ax_data))]

datam_ax = []
for i in range(len(ax_data)):
	datam_ax.append(datetime(ano_ax[i],mes_ax[i],dia_ax[i],hora_ax[i],min_ax[i]))


# #site
#deixa os valores com -99999 (erro) com nan
for i in range(site.shape[1]):
	site[np.where(site[:,i] == -99999),i] = np.nan


ano_st = site[:,0]
mes_st = site[:,1]
dia_st = site[:,2]
hora_st = site[:,3] 
min_st = np.zeros(len(site))

datam_st = []
for i in range(len(site)):
	datam_st.append(datetime(int(ano_st[i]),int(mes_st[i]),int(dia_st[i]),int(hora_st[i]),int(min_st[i])))


# # ========================================================================== #
# #Correcao dos dados (para facilitar na visualizacao dos graficos
# #*pois tem valores de hs de 1200 no site)

site[(np.where(site[:,5]>30)),5] = np.nan #hs
site[(np.where(site[:,6]>30)),5] = np.nan #max


# ================================================================================== #  
# Parametros de ondas

#media
# medb = np.mean(matondab[:,1:],axis=0)
# medp = np.mean(matondap[:,1:],axis=0)

# #desvio padrao
# desvpadb = np.std(matondab[:,1:],axis=0)
# desvpadp = np.std(matondap[:,1:],axis=0)


#graficos

#lioc
# variav = ['data','hs','h10','hmax','tmed','thmax','hm0','tp','dp','sigma1p','sigma2p','hm01','tp1','dp1','hm02','tp2','dp2']
# labs = ['data','m','m','m','s','s','m','s','graus','graus','graus','m','s','graus','m','s','graus']

# for i in range(1,matondab.shape[1]):

# 	pl.figure()
# 	pl.plot(datam,matondab[:,i],'bo')
# 	pl.plot(datam,matondap[:,i],'r*')
# 	pl.title(variav[i])
# 	pl.ylabel(labs[i])
# 	pl.xticks(rotation=15)

# hs, tp e dp
pl.figure()
pl.subplot(311)
pl.title('Parametros de Ondas - ' + local1 + ' - LIOc e Axys')
pl.plot(datam_ax,axys[:,10],'bo')
pl.plot(datam,matondap[:,6],'r*')
pl.ylabel('Hm0 (m)')
pl.grid('on')
pl.xticks(visible=False)
pl.subplot(312)
pl.plot(datam_ax,axys[:,8],'bo')
pl.plot(datam,matondap[:,7],'r*')
pl.ylabel('Tp (s)')
pl.grid('on')
pl.xticks(visible=False)
pl.subplot(313)
pl.plot(datam_ax,axys[:,11],'bo')
pl.plot(datam,matondap[:,8],'r*')
pl.ylabel('Dp (g)')
pl.grid('on')
pl.xticks(rotation=15)

# tp, dp1, tp2, dp2

# pl.figure()
# pl.plot(datam,matondap[:,12],'bo')
# pl.plot(datam,matondap[:,15],'r*')
# pl.title('tp1,tp2')
# pl.legend(('tp1','tp2'))

# pl.figure()
# pl.plot(datam,matondap[:,13],'bo')
# pl.plot(datam,matondap[:,16],'r*')
# pl.title('dp1,dp2')
# pl.legend(('dp1','dp2'))


# #comparacao lioc, summary e site

# pl.figure()
# pl.plot(datam_ax,axys[:,10],'bo')
# pl.plot(datam,matondap[:,6],'r*')
# pl.plot(datam_st,site[:,5],'g*')
# pl.title('Hm0')
# pl.ylabel('m')
# pl.legend(('axys','python','site'))
# pl.xticks(rotation=15)

# pl.figure()
# pl.plot(datam_ax,axys[:,13],'bo')
# pl.plot(datam,matondap[:,2],'r*')
# # pl.plot(datam_st,site[:,5],'g*')
# pl.title('H 1/10')
# pl.ylabel('m')
# pl.legend(('axys','python','site'))
# pl.xticks(rotation=15)

# pl.figure()
# pl.plot(datam_ax,axys[:,5],'bo')
# pl.plot(datam,matondap[:,3],'r*')
# pl.plot(datam_st,site[:,6],'g*')
# pl.title('Hmax (Max. Ht.)')
# pl.ylabel('m')
# pl.legend(('axys','python','site'))
# pl.xticks(rotation=15)

# pl.figure()
# pl.plot(datam_ax,axys[:,8],'bo')
# pl.plot(datam,matondap[:,7],'r*')
# pl.plot(datam_st,site[:,7],'g*')
# pl.title('Tp (Peak Per.)')
# pl.ylabel('s')
# pl.legend(('axys','python','site'))
# pl.xticks(rotation=15)

# pl.figure()
# pl.plot(datam_ax,axys[:,11],'bo')
# pl.plot(datam,matondap[:,8],'r*')
# pl.plot(datam_st,site[:,8],'g*')
# pl.title('Dp (Mean Theta)')
# pl.ylabel('graus')
# pl.legend(('axys','python','site'))
# pl.xticks(rotation=15)

# pl.figure()
# pl.plot(datam_ax,axys[:,12],'bo')
# pl.plot(datam,matondap[:,9],'r*')
# # pl.plot(datam_st,site[:,9],'g*')
# pl.title('Df (Sigma Theta)')
# pl.ylabel('graus')
# pl.legend(('axys','python')) #,'site'))
# pl.xticks(rotation=15)






#   0  1   2   3    4     5    6  7  8    9       10     11  12  13   14  15  16
# data,hs,h10,hmax,tmed,thmax,hm0,tp,dp,sigma1p,sigma2p,hm01,tp1,dp1,hm02,tp2,dp2

#  0        1            2          3        4         5         6        7            8            
#Year/Julian Date/Zero Crossings/Ave. Ht./Ave. Per./Max Ht./Sig. Wave/Sig. Per./Peak Per.(Tp)
#          9        10     11           12       13      14         15  
# /Peak Per.(READ)/HM0/Mean Theta/Sigma Theta/ H1/10 / T.H1/10 /Mean Per.(Tz)

#  0   1   2   3     4    5    6   7   8   9
# ano mes dia hora minuto Hs Hmax Tp Dirm, Df








# pl.figure()
# pl.hist(hs,30,color='b',alpha=0.5)
# pl.hist(hm0,30,color='g',alpha=0.5)
# pl.title('Altura significativa (tempo e frequencia)')
# pl.xlabel('metros')
# pl.ylabel('N de ocorrencias')
# pl.legend(('Hs','Hm0','Hmax'))
# pl.axis([0,10,0,2000])

# pl.figure()
# pl.hist(h10,50,color='b',alpha=0.5)
# pl.hist(hmax,50,color='g',alpha=0.5)
# pl.title('Altura 1/10 e Maxima')
# pl.xlabel('metros')
# pl.ylabel('N de ocorrencias')
# pl.legend(('H10','Hmax'))
# pl.axis([0,10,0,2000])

# pl.figure()
# pl.hist(tmed,35,color='b',alpha=0.5)
# pl.hist(thmax,35,color='g',alpha=0.5)
# pl.hist(tp,20,color='r',alpha=0.5)
# pl.title('Periodo')
# pl.xlabel('segundos')
# pl.ylabel('N de ocorrencias')
# pl.legend(('Tmed','THmax','Tp'))
# pl.axis([2,18,0,5000])

# pl.figure()
# pl.hist(dp,36,color='b',alpha=0.5)
# pl.title('Direcao do periodo de pico')
# pl.xlabel('graus')
# pl.ylabel('N de ocorrencias')
# pl.legend(['Dp'])
# pl.axis([0,360,0,1500])

pl.show()


