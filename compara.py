'''
programa principal para comparacao entre os resultados da modelagem de ondas
para o mes de novembro de dezembro de 2014

carrega a 2 planilhas e concatena

#dados
Hm0	Tp	Dp	Dmean	Hmean	Tmean	H1/3	T1/3	H1/10	T1/10

#vamos trabalhar so com novembro que tem dados mais confiaveis


'''

import os
import numpy as np
from matplotlib import pylab as pl
import xlrd
from datetime import datetime
#import plotpoint_tab_ww3salv


from datetime import datetime


pathnamem = os.environ['HOME'] + '/Dropbox/ww3salvador/Modelagem/Validacao/'
pathnamed = os.environ['HOME'] + '/Dropbox/ww3salvador/Dados/Ondas/'

#carrega dados do modelo
#mod=np.loadtxt(pathnamem + 'mod_nov.ww3')
mod=np.loadtxt(pathnamem + 'mod_fev.ww3')

#data do modelo
datam = np.array([datetime(int(str(mod[i,0])[0:4]),int(str(mod[i,0])[4:6]),int(str(mod[i,0])[6:8]),int(mod[i,1])) for i in range(len(mod))])

#carrega dados de hs, tp e dp da planilha Ondas A1 Nov14 e Dez14
workbook_nov = xlrd.open_workbook(pathnamed + 'Ondas A1 Nov14.xls')
workbook_fev = xlrd.open_workbook(pathnamed + 'Ondas A1 Fev15.xls')

#seleciona planilha por indice (pode ser por nome tbm)
sheet_2_nov = workbook_nov.sheet_by_index(1) #planilha 2
sheet_2_fev= workbook_fev.sheet_by_index(1) #planilha 2

#pega as datas
data_nov = np.array([[sheet_2_nov.cell_value(r,c) for r in range(16,sheet_2_nov.nrows)] for c in [2]]).T
data_fev = np.array([[sheet_2_fev.cell_value(r,c) for r in range(16,sheet_2_fev.nrows)] for c in [2]]).T

#pega os dados
dd_nov = np.array([[sheet_2_nov.cell_value(r,c) for r in range(16,sheet_2_nov.nrows)] for c in range(4,sheet_2_nov.ncols)]).T
dd_fev = np.array([[sheet_2_fev.cell_value(r,c) for r in range(16,sheet_2_fev.nrows)] for c in range(4,sheet_2_fev.ncols)]).T

#concatena a data e os dados
#data = np.concatenate((data_nov,data_dez),axis=0)
#dd = np.concatenate((dd_nov,dd_dez),axis=0)

#caso nao concatena, escolhe o arquivo
data = data_fev
dd = dd_fev

#data com datetime no formato certo
datat = np.array([datetime(*xlrd.xldate_as_tuple(data[i],workbook_nov.datemode)) for i in range(len(data))])

#correcoes nos dados 'dd'
dd[np.where(dd=='')] = np.nan
dd = dd.astype(float)


##############################################################
##############################################################

#estatisticas individuais
#estat = (3,5)
#hs -- media desvpad min perc90 max 
#tp -- media desvpad min perc90 max
#dp -- media desvpad min perc90 max

#dado
estat_dd = np.zeros((3,5))
estat_dd[:,0] = [np.nanmean(dd[:,0]), np.nanmean(dd[:,1]), np.nanmean(dd[:,2])]
estat_dd[:,1] = [np.nanstd(dd[:,0]), np.nanstd(dd[:,1]), np.nanstd(dd[:,2])]
estat_dd[:,2] = [np.nanmin(dd[:,0]), np.nanmin(dd[:,1]), np.nanmin(dd[:,2])]
estat_dd[:,3] = [np.percentile(dd[:,0],90), np.percentile(dd[:,1],90), np.percentile(dd[:,2],90)]
estat_dd[:,4] = [np.nanmax(dd[:,0]), np.nanmax(dd[:,1]), np.nanmax(dd[:,2])]

#modelo
estat_mod = np.zeros((3,5))
estat_mod[:,0] = [np.nanmean(mod[:,4]), np.nanmean(1/mod[:,9]), np.nanmean(mod[:,10])]
estat_mod[:,1] = [np.nanstd(mod[:,4]), np.nanstd(1/mod[:,9]), np.nanstd(mod[:,10])]
estat_mod[:,2] = [np.nanmin(mod[:,4]), np.nanmin(1/mod[:,9]), np.nanmin(mod[:,10])]
estat_mod[:,3] = [np.percentile(mod[:,4],90), np.percentile(1/mod[:,9],90), np.percentile(mod[:,10],90)]
estat_mod[:,4] = [np.nanmax(mod[:,4]), np.nanmax(1/mod[:,9]), np.nanmax(mod[:,10])]


##############################################################
##############################################################

#estatisticas comparativas - bias, rmse..

#achar pontos onde tem medicao

#acha no modelo apenas as datas que tem dados (deixa o vetor do modelo do mesmo comprimento do dado)
nest = np.zeros(len(dd)) #vetor de zeros do tamanho dos dados 
datas_dd = datat.astype(str)
datas_mod = datam.astype(str)
#pega so ate hora para ficar igual ao modelo
datas_modh = np.array([datas_mod[i][:13] for i in range(len(datas_mod))])

for idata in range(len(datas_dd)):
	nest[idata] = np.where(datas_modh == datas_dd[idata][:13])[0]

nest = nest.astype(int)
mod = mod[nest,:]
datat_mod = datam[nest]

#retira os dados com nan de cada variavel
indhs = np.where(np.isnan(dd[:,0]) == False)[0]
indtp = np.where(np.isnan(dd[:,1]) == False)[0]
inddp = np.where(np.isnan(dd[:,2]) == False)[0]

#define variaveis (sem nan e com o mesmo tamanho - utilizar para as estatisticas)
hs = dd[indhs,0]
hs_mod = mod[indhs,4]
tp = dd[indtp,1]
tp_mod = 1/mod[indtp,9]
dp = dd[inddp,2]
dp_mod = mod[inddp,10]



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

np.savetxt('estat_validacao.csv',est,delimiter=",",fmt='%2.2f')
np.savetxt('estat_dados.csv',estat1,delimiter=",",fmt='%2.2f')
np.savetxt('estat_modelo.csv',estat2,delimiter=",",fmt='%2.2f')


# scatter plot 
xi=hs
y=hs_mod
coefficients = np.polyfit(xi, y, 1)
polynomial = np.poly1d(coefficients) 
ys = polynomial(xi) 
pl.figure()
pl.subplot(3,1,1)
pl.plot(xi, y, '.')
pl.plot(xi, ys, 'r--')
pl.plot(range(0,7),range(0,7),'k')
pl.grid()
pl.xlabel('Hs (m) medido')
pl.ylabel('Hs (m) modelado')

xi=tp
y=tp_mod
coefficients = np.polyfit(xi, y, 1)
polynomial = np.poly1d(coefficients) 
ys = polynomial(xi) 
pl.subplot(3,1,2)
pl.plot(xi, y, '.')
pl.plot(xi, ys, 'r--')
pl.plot(range(0,21),range(0,21),'k')
pl.grid()
pl.xlabel('Tp (s) medido')
pl.ylabel('Tp (s) modelado')

xi=dp
y=dp_mod
coefficients = np.polyfit(xi, y, 1)
polynomial = np.poly1d(coefficients) 
ys = polynomial(xi) 
pl.subplot(3,1,3)
pl.plot(xi, y, '.')
pl.plot(xi, ys, 'r--')
pl.plot(range(0,250),range(0,250),'k')
pl.xlim(0,250)
pl.ylim(0,250)
#pl.axis('equal')
pl.grid()
pl.xlabel('Dp (graus) medido')
pl.ylabel('Dp (graus) modelado')
pl.show()



##############################################################
##############################################################

# comparacao
# 0    1   2    3      4      5     6     7      8      9
#Hm0, Tp, Dp, Dmean, Hmean, Tmean, H1/3, T1/3, H1/10, T1/10

#figuras
pl.figure(figsize=(12,10))
pl.subplot(3,1,1)
pl.plot(datat,dd[:,0],'bo',datam[0:-1],mod[:,4],'-r',linewidth=2)
pl.ylabel('Hs (m)',fontsize=12), pl.grid()
pl.legend(['ADCP','WW3'])
pl.ylim(0,3)
pl.subplot(3,1,2)
pl.plot(datat,dd[:,1],'ob',datam[0:-1],1./mod[:,9],'or')
pl.ylabel('Tp (s)',fontsize=12), pl.grid()
pl.ylim(0,22)
pl.subplot(3,1,3)
pl.plot(datat,dd[:,2],'ob',datam[0:-1],mod[:,10],'or')
pl.ylabel('Dp (graus)',fontsize=12), pl.grid()
pl.yticks([0,45,90,135,180,225,270,315,360])


#plotpoint_tab_ww3salv.hist(hs_mod,tp_mod,dp_mod)


pl.show()