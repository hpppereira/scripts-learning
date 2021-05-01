# -*- coding: utf-8 -*-
'''
Compara os dados da triaxys processado pelo lioc e 
resultado do ww3

Ultima modificacao: 09/05/2015

#Saida do Python
#         0   1   2   3    4     5    6   7   8     9       10       11   12   13   14    15   16   17    18   19
#header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')

#Saida WW3
# 0   1   2    3   4   5   6  7   8
#ano,mes,dia,hora,min,hs,tp,dp,spread
'''

import numpy as np
from matplotlib import pylab as pl
import matplotlib as mpl
from matplotlib import pyplot as plt
from datetime import datetime
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import os
import matplotlib.dates as mdates

plt.close('all')

local = 'Santos/SP'
local1 = 'santos'
latlon = '-25.28334 / -44.93334'
idargos = '69151'
idwmo = '31051'
glstr = '8'
dmag = -23

#triaxys_8_santos_jul13

#Saida do lioc
#         0   1   2   3    4     5    6   7   8     9       10       11   12   13   14    15   16   17    18   19
#header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')
py = np.loadtxt(os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/hindcast/Santos/' + 'triaxys_' + glstr + '_' + local1 + '.out',delimiter=',',skiprows = 0)

# carrega resultado do WW3
pathname_mod = os.environ['HOME'] + '/Dropbox/ww3vale/Geral/TU/hindcast/Santos/resultados/'
direm = np.sort(os.listdir(pathname_mod))

#Saida WW3
# 0   1   2    3   4   5  6  7   8
#ano,mes,dia,hora,min,hs,tp,dp,spread

# ddm = Data, hora, Hs, Fp, Dp -- calcula o Tp mais abaixo
ddm = np.array([[0,0,0,0,0,0,0,0,0]])

#loop de diretorios e arquivos (cada diretorio tem 1 arquivo)
for dto in direm:

    #pula a primeira linha pois ja eh a mesma do ultima arquivo
	dadosm = np.loadtxt(pathname_mod + dto + '/santos.txt')
	ddm = np.concatenate((ddm,dadosm),axis=0)

ddm = ddm[1:,:]

datam_py = []
for i in range(len(py)):
	datam_py.append(datetime(int(str(py[i,0])[0:4]),int(str(py[i,0])[4:6]),int(str(py[i,0])[6:8]),int(str(py[i,0])[8:10])))

datam_ww3 = []
for i in range(len(ddm)):
	datam_ww3.append(datetime(int(ddm[i,0]), int(ddm[i,1]), int(ddm[i,2]), int(ddm[i,3]) ))


###
#calculos dis indices estatisticos

per = 'fev2013' #periodo para salvar o arquivo

#cria matriz de dados com as datas escolhidas
#triaxys
dini = pl.find(np.array(datam_py).astype(str)=='2013-07-01 00:00:00') #data inicial
dfim = pl.find(np.array(datam_py).astype(str)=='2013-08-01 00:00:00') #data final
py1 = py[dini:dfim+1,:]

#modelo
dini = pl.find(np.array(datam_ww3).astype(str)=='2013-07-01 00:00:00') #data inicial
dfim = pl.find(np.array(datam_ww3).astype(str)=='2013-08-01 00:00:00') #data final
ddm1 = ddm[dini:dfim+1,:]

#retira os dados com nan de cada variavel
indhs = np.where(np.isnan(py1[:,6]) == False)[0]
indtp = np.where(np.isnan(py1[:,7]) == False)[0]
inddp = np.where(np.isnan(py1[:,8]) == False)[0]

#define variaveis (sem nan e com o mesmo tamanho - utilizar para as estatisticas)
hs = py1[indhs,6]
hs_mod = ddm1[indhs,5]
tp = py1[indtp,7]
tp_mod = ddm1[indtp,6]
dp = py1[inddp,8]
dp_mod = ddm1[inddp,7]


#calculo das estatisticas entre modelo e cacimbas

### BIAS ###
#hs
bias_hs = np.mean(hs_mod - hs)
#tp
bias_tp = np.mean(tp_mod - tp)
#dp
bias_dp = np.mean(dp_mod - dp)

### ERMS ###
#hs
rmse_hs = np.sqrt( pl.sum( (hs_mod - hs) ** 2 ) / len(hs) )
#tp
rmse_tp = np.sqrt( pl.sum( (tp_mod - tp) ** 2 ) / len(tp) )
#hs
rmse_dp = np.sqrt( pl.sum( (dp_mod - dp) ** 2 ) / len(dp) )

### SI ###
#hs
si_hs = rmse_hs / np.mean(hs)
#tp
si_tp = rmse_tp / np.mean(tp)
#dp
si_dp = rmse_dp / np.mean(dp)


### Correlacao ###
#hs
corr_hs = np.corrcoef(hs_mod,hs)[0,1]
#tp
corr_tp = np.corrcoef(tp_mod,tp)[0,1]
#dp
corr_dp = np.corrcoef(dp_mod,dp)[0,1]

### media boia ###
mean_adcp_hs = np.mean(hs)
mean_adcp_tp = np.mean(tp)
mean_adcp_dp = np.mean(dp)
### media modelo ###
mean_mod_hs = np.mean(hs_mod)
mean_mod_tp = np.mean(tp_mod)
mean_mod_dp = np.mean(dp_mod)

### maximo boia ###
max_adcp_hs = np.max(hs)
max_adcp_tp = np.max(tp)
max_adcp_dp = np.max(dp)
### maximo modelo ###
max_mod_hs = np.max(hs_mod)
max_mod_tp = np.max(tp_mod)
max_mod_dp = np.max(dp_mod)

# estatistica (matriz est)
# ---------------------------------------------
# Hs | BIAS   | RMSE    | SI      | CORR
# Tp | BIAS   | RMSE    | SI      | CORR
# Dp | BIAS   | RMSE    | SI      | CORR
# Hs | Med Obs| Med Mod | Max Obs | Max Mod
# Tp | Med Obs| Med Mod | Max Obs | Max Mod
# Dp | Med Obs| Med Mod | Max Obs | Max Mod

#estatistica 1 (hs, tp, dp) estat_dados.csv
# Hs  | Med | DesPad | Min | P90 | Max
# Tp  | Med | DesPad | Min | P90 | Max
# Dp  | Med | DesPad | Min | P90 | Max

estat1 = np.zeros((3,5))
estat1[0,0] = np.mean(hs)
estat1[1,0] = np.mean(tp)
estat1[2,0] = np.mean(dp)
estat1[0,1] = np.std(hs)
estat1[1,1] = np.std(tp)
estat1[2,1] = np.std(dp)
estat1[0,2] = np.min(hs)
estat1[1,2] = np.min(tp)
estat1[2,2] = np.min(dp)
estat1[0,3] = np.percentile(hs,90)
estat1[1,3] = np.percentile(tp,90)
estat1[2,3] = np.percentile(dp,90)
estat1[0,4] = np.max(hs)
estat1[1,4] = np.max(tp)
estat1[2,4] = np.max(dp)

#estatistica 2 (hs, tp, dp) estat_modelo.csv
# Hs  | Med | DesPad | Min | P90 | Max
# Tp  | Med | DesPad | Min | P90 | Max
# Dp  | Med | DesPad | Min | P90 | Max

estat2 = np.zeros((3,5))
estat2[0,0] = np.mean(hs_mod)
estat2[1,0] = np.mean(tp_mod)
estat2[2,0] = np.mean(dp_mod)
estat2[0,1] = np.std(hs_mod)
estat2[1,1] = np.std(tp_mod)
estat2[2,1] = np.std(dp_mod)
estat2[0,2] = np.min(hs_mod)
estat2[1,2] = np.min(tp_mod)
estat2[2,2] = np.min(dp_mod)
estat2[0,3] = np.percentile(hs_mod,90)
estat2[1,3] = np.percentile(tp_mod,90)
estat2[2,3] = np.percentile(dp_mod,90)
estat2[0,4] = np.max(hs_mod)
estat2[1,4] = np.max(tp_mod)
estat2[2,4] = np.max(dp_mod)
# perc90[0,1] = np.percentile(hs_mod,90)
# perc90[1,1] = np.percentile(tp_mod,90)
# perc90[2,1] = np.percentile(dp_mod,90)

est=np.zeros((6,4))
est[0,0]=bias_hs
est[1,0]=bias_tp
est[2,0]=bias_dp
est[3,0]=mean_adcp_hs
est[4,0]=mean_adcp_tp
est[5,0]=mean_adcp_dp
est[0,1]=rmse_hs
est[1,1]=rmse_tp
est[2,1]=rmse_dp
est[3,1]=mean_mod_hs
est[4,1]=mean_mod_tp
est[5,1]=mean_mod_dp
est[0,2]=si_hs
est[1,2]=si_tp
est[2,2]=si_dp
est[3,2]=max_adcp_hs
est[4,2]=max_adcp_tp
est[5,2]=max_adcp_dp
est[0,3]=corr_hs
est[1,3]=corr_tp
est[2,3]=corr_dp
est[3,3]=max_mod_hs
est[4,3]=max_mod_tp
est[5,3]=max_mod_dp

# np.savetxt(local1 + '_' + per + '_estat_validacao.csv',est,delimiter=",",fmt='%2.2f')
# np.savetxt(local1 + '_' + per + '_estat_dados.csv',estat1,delimiter=",",fmt='%2.2f')
# np.savetxt(local1 + '_' + per + '_estat_modelo.csv',estat2,delimiter=",",fmt='%2.2f')


###

#figuras
fig = pl.figure()
ax = fig.add_subplot(311)
ax.plot(datam_py,py[:,6],'b',datam_ww3,ddm[:,5],'r')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax.set_ylabel('Hs (m)',fontsize=12), ax.grid()
ax.legend(['PNBOIA','WW3'],loc=0,ncol=4)
ax.set_ylim(0,8)
ax.set_xlim(datam_ww3[dini],datam_ww3[dfim])


ax2 = fig.add_subplot(312)
ax2.plot(datam_py,py[:,7],'b.',datam_ww3,ddm[:,6],'r.')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax2.set_ylabel('Tp (s)',fontsize=12), pl.grid()
ax2.set_ylim(0,22)
ax2.set_xlim(datam_ww3[dini],datam_ww3[dfim])

ax3 = fig.add_subplot(313)
ax3.plot(datam_py,py[:,8]+dmag,'b.',datam_ww3,ddm[:,7],'r.')
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax3.set_ylabel('Dp (graus)',fontsize=12), pl.grid()
ax3.set_ylim(0,360)
ax3.set_xlim(datam_ww3[dini],datam_ww3[dfim])

pl.show()




# plt.figure()
# plt.subplot(311)
# plt.plot(datam_py,py[:,6],'b')
# plt.plot(datam_ww3,ddm[:,5],'r')
# plt.ylabel('Hs (m)'), pl.grid()
# plt.xlim(datam_ww3[0],datam_ww3[-1])

# plt.subplot(312)
# plt.plot(datam_py,py[:,7],'b.')
# plt.plot(datam_ww3,ddm[:,6],'r.')
# plt.ylabel('Tp (s)'), pl.grid()
# plt.xlim(datam_ww3[0],datam_ww3[-1])

# plt.subplot(313)
# plt.plot(datam_py,py[:,8]+dmag,'b.')
# plt.plot(datam_ww3,ddm[:,7],'r.')
# plt.ylabel('Dp (graus)'), pl.grid()
# plt.xlim(datam_ww3[0],datam_ww3[-1])

# plt.show()
